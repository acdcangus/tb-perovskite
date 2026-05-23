"""Velocity (momentum) operators dH/dk for the tight-binding models.

The velocity operator is ``v_alpha(k) = (1/hbar) dH/dk_alpha``.  For g-factors
and optical response the quantity that actually enters is the **interband
momentum matrix element** ``p = m0 v``, equivalently the Kane parameter
``P = hbar*p/m0 = dH/dk`` (units eV.A when k is in 1/A).  We therefore expose
``dH_dk`` directly (eV.A) and a thin ``velocity`` wrapper.

This module only *reads* the existing Hamiltonian structure; it does not modify
any model (pure extension).  Analytic derivatives are provided for the models
used in Theme A and validated against finite differences in
``tests/test_velocity.py``.

Convention: same atomic gauge and spin-major (all spin-up, then spin-down)
ordering as ``models_kashikar`` / ``models_nestoklon``.  The on-site SOC term is
k-independent, so it does not contribute to dH/dk.
"""

from __future__ import annotations

from typing import Callable, Mapping

import numpy as np

from . import models_kashikar as mk
from ._soc import soc_p_from_lambda3  # noqa: F401  (kept for parity/documentation)

# hbar^2 / m0 in eV * Angstrom^2  (= 2 * 3.80998 eV.A^2). Used to convert the
# momentum matrix element P = hbar*p/m0 [eV.A] into the Kane term P^2/(hbar^2/m0).
HBAR2_OVER_M0 = 7.619964  # eV * Angstrom^2


# --------------------------------------------------------------------------- #
# Generic numerical reference (oracle for tests; not the production path)
# --------------------------------------------------------------------------- #
def dH_dk_numerical(builder: Callable[[np.ndarray], np.ndarray], kvec: np.ndarray,
                    alpha: int, h: float = 1e-6) -> np.ndarray:
    """Central finite-difference dH/dk_alpha of an arbitrary builder (eV.A)."""
    k = np.asarray(kvec, dtype=float).copy()
    kp = k.copy(); kp[alpha] += h
    km = k.copy(); km[alpha] -= h
    return (builder(kp) - builder(km)) / (2.0 * h)


# --------------------------------------------------------------------------- #
# Kashikar 13-orbital analytic dH/dk
# --------------------------------------------------------------------------- #
def dH_dk_kashikar13_spinless(kvec: np.ndarray, params: Mapping[str, float],
                              a: float, alpha: int) -> np.ndarray:
    """Analytic d(H0)/dk_alpha for the 13-orbital spinless Hamiltonian (eV.A).

    Mirrors :func:`models_kashikar.kashikar13_spinless`, differentiating each
    k-dependent factor:
        d/dk_a [2i sin(k_d a/2)] = delta_{da} * i a cos(k_d a/2)
        d/dk_a [2  cos(k_d a/2)] = -delta_{da} * a sin(k_d a/2)
        d/dk_a [cos(k_d a)]      = -delta_{da} * a sin(k_d a)
        d/dk_a [sin(k_d a)]      =  delta_{da} * a cos(k_d a)
    """
    ka = [float(kvec[d]) * a for d in range(3)]
    t_sp = params["t_BX_sp"]
    t_pps = params["t_BX_ppsigma"]
    t_ppp = params["t_BX_pppi"]
    tbb_ss = params["t_BB_ss"]
    tbb_sp = params["t_BB_spsigma"]
    tbb_pps = params["t_BB_ppsigma"]
    tbb_ppp = params["t_BB_pppi"]

    H = np.zeros((mk.N_ORB_13, mk.N_ORB_13), dtype=complex)

    # Derivatives of the B-X factors, nonzero only for d == alpha.
    dS = 1j * a * np.cos(ka[alpha] / 2.0)        # d/dk_alpha of S[alpha]
    dC = -a * np.sin(ka[alpha] / 2.0)            # d/dk_alpha of C[alpha]

    base = mk._HALIDE_BLOCK[alpha]               # halide on this axis
    # B-s <-> X_alpha-p_alpha (only this halide's pσ depends on k_alpha via S)
    H[0, base + alpha] = t_sp * dS
    # B-p_i <-> X_alpha-p_i  (sigma if i==alpha else pi), factor C[alpha]
    for i in range(3):
        tval = t_pps if i == alpha else t_ppp
        H[1 + i, base + i] = tval * dC

    # B-B diagonal dispersion derivatives.
    dcos = -a * np.sin(ka[alpha])                # d/dk_alpha cos(k_alpha a)
    # h1 (s) depends on cos(k_alpha a) with coeff 2*tbb_ss
    H[0, 0] = 2.0 * tbb_ss * dcos
    # h2,h3,h4: diagonal p-orbital d for d-th p couples sigma to its own axis.
    # h_{1+d} = 2 tpps cos(k_d a) + 2 tppp sum_{e!=d} cos(k_e a)
    for d in range(3):
        coeff = (2.0 * tbb_pps) if (d == alpha) else (2.0 * tbb_ppp)
        H[1 + d, 1 + d] = coeff * dcos
    # B-s <-> B-p_alpha second-neighbour: 2i tbb_sp sin(k_alpha a)
    H[0, 1 + alpha] = tbb_sp * 2j * a * np.cos(ka[alpha])

    # Hermitian completion (diagonal entries are real here, but use generic form).
    H = H + H.conj().T - np.diag(np.diag(H).real).astype(complex)
    return H


def dH_dk_kashikar13(kvec: np.ndarray, params: Mapping[str, float], a: float,
                     alpha: int) -> np.ndarray:
    """Analytic dH/dk_alpha for the 26x26 spinful Kashikar-13 Hamiltonian (eV.A).

    SOC is k-independent, so dH/dk is block-diagonal in spin: kron(I2, dH0/dk).
    """
    dH0 = dH_dk_kashikar13_spinless(kvec, params, a, alpha)
    return np.kron(np.eye(2, dtype=complex), dH0)


# --------------------------------------------------------------------------- #
# Kashikar 4-orbital analytic dH/dk
# --------------------------------------------------------------------------- #
def dH_dk_kashikar4_spinless(kvec: np.ndarray, params: Mapping[str, float],
                             a: float, alpha: int) -> np.ndarray:
    """Analytic d(H0)/dk_alpha for the 4-orbital minimal spinless Hamiltonian."""
    ka = [float(kvec[d]) * a for d in range(3)]
    tss = params["t_ss"]
    tsp = params["t_sp"]
    tpps = params["t_ppsigma"]
    tppp = params["t_pppi"]
    dcos = -a * np.sin(ka[alpha])

    H = np.zeros((mk.N_ORB_4, mk.N_ORB_4), dtype=complex)
    H[0, 0] = 2.0 * tss * dcos
    for d in range(3):
        coeff = (2.0 * tpps) if (d == alpha) else (2.0 * tppp)
        H[1 + d, 1 + d] = coeff * dcos
    H[0, 1 + alpha] = tsp * 2j * a * np.cos(ka[alpha])
    H = H + H.conj().T - np.diag(np.diag(H).real).astype(complex)
    return H


def dH_dk_kashikar4(kvec, params, a, alpha):
    return np.kron(np.eye(2, dtype=complex), dH_dk_kashikar4_spinless(kvec, params, a, alpha))


# --------------------------------------------------------------------------- #
# Nestoklon analytic dH/dk
# --------------------------------------------------------------------------- #
def make_dH_dk_nestoklon(params: Mapping[str, float], a: float, basis):
    """Return ``dHdk(kvec, alpha) -> (N,N)`` for the Nestoklon model (eV.A).

    Re-uses the precomputed direction SK blocks; only the atomic-gauge phase
    e^{+/- i k_d a/2} depends on k, with
        d/dk_alpha [plus * e^{i k_d a/2} + minus * e^{-i k_d a/2}]
          = delta_{d,alpha} * (i a/2) [plus * e^{i k_d a/2} - minus * e^{-i k_d a/2}].
    On-site and SOC blocks are k-independent.
    """
    from . import models_nestoklon as mn

    _norm = {"dx2-y2": "dx2y2", "s*": "sstar"}
    basis = [_norm.get(b, b) for b in basis]
    n_orb = len(basis)
    N = n_orb * 4

    plus_blocks, minus_blocks = {}, {}
    for axis, direction in mn._AXIS_DIR.items():
        dminus = tuple(-x for x in direction)
        plus_blocks[axis] = mn._sk_block(basis, direction, params)
        minus_blocks[axis] = mn._sk_block(basis, dminus, params)

    def slc(atom):
        return slice(atom * n_orb, (atom + 1) * n_orb)

    def dHdk(kvec: np.ndarray, alpha: int) -> np.ndarray:
        k = np.asarray(kvec, dtype=float)
        dH0 = np.zeros((N, N), dtype=complex)
        # Only the halide on axis `alpha` contributes (phase depends on k_alpha).
        direction = mn._AXIS_DIR[alpha]
        kd = float(np.dot(k, direction))
        phase = np.exp(1j * kd * a / 2.0)
        dblock = (1j * a / 2.0) * (plus_blocks[alpha] * phase
                                   - minus_blocks[alpha] * np.conj(phase))
        dH0[slc(0), slc(alpha + 1)] = dblock
        dH0[slc(alpha + 1), slc(0)] = dblock.conj().T
        return np.kron(np.eye(2, dtype=complex), dH0)

    return dHdk


def velocity_from_dHdk(dHdk_alpha: np.ndarray, hbar: float = 1.0) -> np.ndarray:
    """v_alpha = (1/hbar) dH/dk_alpha. With hbar=1 the matrix is dH/dk (eV.A)."""
    return dHdk_alpha / hbar
