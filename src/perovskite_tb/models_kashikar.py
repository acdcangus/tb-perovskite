"""Kashikar-Gupta-Nanda Slater-Koster tight-binding models for cubic CsBX3.

Source: R. Kashikar, M. Gupta, B. R. K. Nanda, "A Generic Slater-Koster
Description of the Electronic Structure of Centrosymmetric Halide Perovskites",
arXiv:2101.08562.  Hamiltonian: Eqs. (1)-(8); analytic R-point eigenvalues: Eq. (9).

Geometry (cubic Pm-3m, lattice constant ``a``):
    * B (Ge/Sn/Pb) cation forms a simple-cubic sublattice (B-B distance ``a``).
    * Three halides per cell, one on each cubic axis at distance ``a/2`` from B:
      X1 on x, X2 on y, X3 on z.
    * B-X coupling is nearest-neighbour (bond length a/2).
    * B-B coupling is the (simple-cubic) nearest neighbour at distance ``a``
      (called the "second neighbour" interaction in the paper because B-X at a/2
      is the first).
    * X-X coupling is neglected: the X-p block is on-site diagonal (Eq. 7).

Gauge: we use the *atomic* gauge ``H_ab(k) = sum_R t_ab(R) exp(i k.(R + tau_b - tau_a))``.
With B at the origin this reproduces the paper's compact factors exactly:
    S_d = 2 i sin(k_d a / 2)   (B-X, odd s-p sigma coupling)
    C_d = 2   cos(k_d a / 2)   (B-X, even p-p coupling)
and full-``a`` phases for the B-B block (so that the B-p triplet stays clean at
R, as required by Eq. 9).

Orbital order (spinless, 13 orbitals):
    0: B-s
    1,2,3: B-px, B-py, B-pz
    4,5,6: X1(x)-px, X1-py, X1-pz
    7,8,9: X2(y)-px, X2-py, X2-pz
    10,11,12: X3(z)-px, X3-py, X3-pz

With spin we use spin-major ordering (all 13 spin-up, then all 13 spin-down);
SOC ``lambda L.S`` acts only on the B-p orbitals (indices 1,2,3).
"""

from __future__ import annotations

from typing import Mapping

import numpy as np

from ._soc import soc_p_from_lambda3

# Indices of the three halides and the cubic axis each sits on.
# axis index: 0 -> x, 1 -> y, 2 -> z
_HALIDE_BLOCK = {0: 4, 1: 7, 2: 10}  # axis -> first orbital index of that halide
N_ORB_13 = 13


# --------------------------------------------------------------------------- #
# 13-orbital model
# --------------------------------------------------------------------------- #
def kashikar13_spinless(kvec: np.ndarray, params: Mapping[str, float], a: float) -> np.ndarray:
    """Return the 13x13 spinless Bloch Hamiltonian H0(k).

    Parameters
    ----------
    kvec : array-like, shape (3,)
        Cartesian wavevector (units of 1/length consistent with ``a``).
    params : mapping
        Keys: E_B_s, E_B_p, E_X_p, t_BX_sp, t_BX_ppsigma, t_BX_pppi,
        t_BB_ss, t_BB_spsigma, t_BB_ppsigma, t_BB_pppi.
    a : float
        Cubic lattice constant.
    """
    kx, ky, kz = (float(kvec[0]) * a, float(kvec[1]) * a, float(kvec[2]) * a)
    ka = (kx, ky, kz)  # k_d * a for d = x, y, z

    eps_s = params["E_B_s"]
    eps_p = params["E_B_p"]
    eps_X = params["E_X_p"]
    t_sp = params["t_BX_sp"]
    t_pps = params["t_BX_ppsigma"]
    t_ppp = params["t_BX_pppi"]
    tbb_ss = params["t_BB_ss"]
    tbb_sp = params["t_BB_spsigma"]
    tbb_pps = params["t_BB_ppsigma"]
    tbb_ppp = params["t_BB_pppi"]

    H = np.zeros((N_ORB_13, N_ORB_13), dtype=complex)

    # --- B-X nearest-neighbour block (bond length a/2) --------------------- #
    # S_d = 2 i sin(k_d a/2), C_d = 2 cos(k_d a/2)
    S = [2j * np.sin(ka[d] / 2.0) for d in range(3)]
    C = [2.0 * np.cos(ka[d] / 2.0) for d in range(3)]
    for axis, base in _HALIDE_BLOCK.items():  # axis = d (the halide's own axis)
        # B-s  <->  X_d-p_d  : sigma s-p, factor S_d
        H[0, base + axis] = t_sp * S[axis]
        # B-p_i <-> X_d-p_i  : sigma if i == axis else pi, factor C_d
        for i in range(3):
            tval = t_pps if i == axis else t_ppp
            H[1 + i, base + i] = tval * C[axis]

    # --- B-B block (simple cubic, bond length a, full-a phases) ------------ #
    cos_ka = [np.cos(ka[d]) for d in range(3)]
    sin_ka = [np.sin(ka[d]) for d in range(3)]
    # diagonal dispersions h1..h4 (Eq. 8)
    h1 = 2.0 * tbb_ss * (cos_ka[0] + cos_ka[1] + cos_ka[2])
    h2 = 2.0 * tbb_pps * cos_ka[0] + 2.0 * tbb_ppp * (cos_ka[1] + cos_ka[2])
    h3 = 2.0 * tbb_pps * cos_ka[1] + 2.0 * tbb_ppp * (cos_ka[0] + cos_ka[2])
    h4 = 2.0 * tbb_pps * cos_ka[2] + 2.0 * tbb_ppp * (cos_ka[0] + cos_ka[1])
    H[0, 0] = eps_s + h1
    H[1, 1] = eps_p + h2
    H[2, 2] = eps_p + h3
    H[3, 3] = eps_p + h4
    # B-s <-> B-p_d second-neighbour sigma coupling: 2 i t sin(k_d a)
    for d in range(3):
        H[0, 1 + d] = tbb_sp * 2j * sin_ka[d]

    # --- X-X block: on-site only (Eq. 7) ----------------------------------- #
    for base in _HALIDE_BLOCK.values():
        for i in range(3):
            H[base + i, base + i] = eps_X

    # Hermitian completion (lower triangle from upper).
    H = H + H.conj().T - np.diag(np.diag(H).real).astype(complex)
    return H


def kashikar13_hamiltonian(kvec: np.ndarray, params: Mapping[str, float], a: float) -> np.ndarray:
    """Return the 26x26 spinful Bloch Hamiltonian (13 orbitals x 2 spin) with SOC."""
    H0 = kashikar13_spinless(kvec, params, a)
    H = np.kron(np.eye(2, dtype=complex), H0)  # spin-major: block-diag(H0, H0)

    lam = params["lambda_SOC"]
    soc = soc_p_from_lambda3(lam)  # Eq. 10 convention: p-splitting = 3*lambda
    # B-p orbital indices in the spinless basis are 1,2,3.
    p_idx = [1, 2, 3]
    full_idx = [s * N_ORB_13 + o for s in (0, 1) for o in p_idx]  # spin-major
    for a_i, A in enumerate(full_idx):
        for b_i, B in enumerate(full_idx):
            H[A, B] += soc[a_i, b_i]
    return H


def kashikar13_R_eigenvalues(params: Mapping[str, float]) -> dict:
    """Analytic R-point eigenvalues (no SOC), Eq. (9) of arXiv:2101.08562.

    Returns a dict with keys E1, E2, E3, E4 and their stated degeneracies.
    """
    EBs = params["E_B_s"]
    EBp = params["E_B_p"]
    EXp = params["E_X_p"]
    tss = params["t_BB_ss"]
    tsp = params["t_BX_sp"]
    tpps = params["t_BB_ppsigma"]
    tppp = params["t_BB_pppi"]

    eta = np.sqrt((EXp - EBs + 6.0 * tss) ** 2 + 48.0 * tsp ** 2) / 2.0
    center = (EXp + EBs) / 2.0 - 3.0 * tss
    return {
        "E1": (center - eta, 1),
        "E2": (EXp, 8),
        "E3": (EBp - 2.0 * tpps - 4.0 * tppp, 3),
        "E4": (center + eta, 1),
    }


# --------------------------------------------------------------------------- #
# 4-orbital minimal model
# --------------------------------------------------------------------------- #
N_ORB_4 = 4


def kashikar4_spinless(kvec: np.ndarray, params: Mapping[str, float], a: float) -> np.ndarray:
    """Return the 4x4 spinless minimal-basis Bloch Hamiltonian (Eqs. 11-12, no SOC).

    Basis: B-{s, px, py, pz}.  The X-p contribution is folded into effective
    B-B (second-neighbour) interactions; on-site energies are anti-bonding band
    centres.  Dispersions h_i are the same functions as Eq. (8).
    """
    kx, ky, kz = (float(kvec[0]) * a, float(kvec[1]) * a, float(kvec[2]) * a)
    ka = (kx, ky, kz)

    eps_s = params["eps_s"]
    eps_p = params["eps_p"]
    tss = params["t_ss"]
    tsp = params["t_sp"]
    tpps = params["t_ppsigma"]
    tppp = params["t_pppi"]

    cos_ka = [np.cos(ka[d]) for d in range(3)]
    sin_ka = [np.sin(ka[d]) for d in range(3)]

    H = np.zeros((N_ORB_4, N_ORB_4), dtype=complex)
    h1 = 2.0 * tss * (cos_ka[0] + cos_ka[1] + cos_ka[2])
    h2 = 2.0 * tpps * cos_ka[0] + 2.0 * tppp * (cos_ka[1] + cos_ka[2])
    h3 = 2.0 * tpps * cos_ka[1] + 2.0 * tppp * (cos_ka[0] + cos_ka[2])
    h4 = 2.0 * tpps * cos_ka[2] + 2.0 * tppp * (cos_ka[0] + cos_ka[1])
    H[0, 0] = eps_s + h1
    H[1, 1] = eps_p + h2
    H[2, 2] = eps_p + h3
    H[3, 3] = eps_p + h4
    for d in range(3):
        H[0, 1 + d] = tsp * 2j * sin_ka[d]
    H = H + H.conj().T - np.diag(np.diag(H).real).astype(complex)
    return H


def kashikar4_hamiltonian(kvec: np.ndarray, params: Mapping[str, float], a: float) -> np.ndarray:
    """Return the 8x8 spinful minimal-basis Bloch Hamiltonian with SOC.

    SOC is the canonical ``lambda L.S`` on the B-p orbitals (indices 1,2,3).
    """
    H0 = kashikar4_spinless(kvec, params, a)
    H = np.kron(np.eye(2, dtype=complex), H0)
    lam = params["lambda_SOC"]
    soc = soc_p_from_lambda3(lam)
    p_idx = [1, 2, 3]
    full_idx = [s * N_ORB_4 + o for s in (0, 1) for o in p_idx]
    for a_i, A in enumerate(full_idx):
        for b_i, B in enumerate(full_idx):
            H[A, B] += soc[a_i, b_i]
    return H


def kashikar4_gap_no_soc(params: Mapping[str, float]) -> float:
    """Minimal-model band gap without SOC (Eq. in Sec. III.C):

        Eg = eps_p - eps_s - 2 t_ppsigma - 4 t_pppi + 6 t_ss
    """
    return (
        params["eps_p"]
        - params["eps_s"]
        - 2.0 * params["t_ppsigma"]
        - 4.0 * params["t_pppi"]
        + 6.0 * params["t_ss"]
    )
