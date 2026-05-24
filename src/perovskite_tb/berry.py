# SPDX-License-Identifier: MIT
# Copyright (c) 2026 tk
"""Berry curvature core -> anomalous Hall (AHC) and spin Hall (SHC) conductivity.

Spec F1 (extention/03_tb-perovskite_spec.md); future_themes Theme H.  Builds a
Berry-curvature core on top of the existing velocity operator (velocity.py).

Sources (all verified real & open-access, 2026-05-24):

* D. Xiao, M.-C. Chang, Q. Niu, Rev. Mod. Phys. 82, 1959 (2010),
  DOI 10.1103/RevModPhys.82.1959 (arXiv:0907.2021).
  Berry curvature Kubo formula, **Eq. (1.13)** (confirmed against the source):
      Omega^n_{mu nu} = i sum_{m!=n}
          [<n|dH/dk_mu|m><m|dH/dk_nu|n> - (mu<->nu)] / (E_n - E_m)^2 .
  Because dH/dk is Hermitian this reduces to the real form used here,
      Omega^n_{xy} = -2 sum_{m!=n} Im( V^x_{nm} V^y_{mn} ) / (E_n - E_m)^2 ,
  with V^a = U^dagger (dH/dk_a) U.

* T. Fukui, Y. Hatsugai, H. Suzuki, J. Phys. Soc. Jpn. 74, 1674 (2005),
  DOI 10.1143/JPSJ.74.1674 (arXiv:cond-mat/0503172).  Manifestly
  gauge-invariant (spin) Hall / Chern number on a discretized Brillouin zone
  via link variables; non-Abelian (multiband) determinant form used here.

* J. Sinova, S. O. Valenzuela, J. Wunderlich, C. H. Back, T. Jungwirth,
  Rev. Mod. Phys. 87, 1213 (2015), DOI 10.1103/RevModPhys.87.1213
  (arXiv:1411.3249).  Intrinsic spin Hall conductivity; spin-current operator
  j^{s_gamma}_alpha = (1/2){ s_gamma, v_alpha }.

Units: hbar = 1, so v_alpha = dH/dk_alpha (eV.Angstrom).  Berry curvature has
units Angstrom^2.  The *_sum helpers return the dimensionless Brillouin-zone
sum of curvature over occupied bands; physical conductivity prefactors
(e^2/hbar, with a (2pi)^{-d} BZ measure) are applied by the caller.

Known limitation (honest, as in g_factor.py / shift_current.py): the TB
position operator omits intra-atomic contributions (Blount, Solid State Phys.
13, 305 (1962)); absolute Berry-curvature / SHC *magnitudes* may be
underestimated.  Symmetry results (AHC = 0 by P*T), integer-quantized Chern
numbers, and relative trends are robust.
"""

from __future__ import annotations

from typing import Mapping, Sequence

import numpy as np

from . import models_kashikar as mk
from . import velocity as vel

# --------------------------------------------------------------------------- #
# Core: band-basis velocity and Kubo Berry curvature
# --------------------------------------------------------------------------- #


def velocity_matrix(evecs: np.ndarray, dHk: np.ndarray) -> np.ndarray:
    """Band-basis matrix V = U^dagger (dH/dk) U (eigenvector columns in U)."""
    return evecs.conj().T @ dHk @ evecs


def berry_curvature_kubo(
    evals: np.ndarray,
    evecs: np.ndarray,
    dHx: np.ndarray,
    dHy: np.ndarray,
    *,
    degen_tol: float = 1e-6,
) -> np.ndarray:
    """Band-resolved Berry curvature Omega^n_{xy}, Xiao 2010 Eq. (1.13).

    Parameters
    ----------
    evals, evecs : eigenvalues (n,) and eigenvectors (dim, n) of H(k); columns
        of ``evecs`` are the eigenstates (np.linalg.eigh convention).
    dHx, dHy : (dim, dim) velocity operators dH/dk_x, dH/dk_y at the same k.
    degen_tol : pairs with |E_n - E_m| < degen_tol are excluded from the sum
        (their term is gauge-dependent/singular).  For degenerate *occupied*
        manifolds the multiplet-summed curvature is still gauge invariant
        because sum_{n in M} V^x_{nm} V^y_{mn} = <m|v_y P_M v_x|m> depends only
        on the projector P_M; use ``link_variable_chern`` for the non-Abelian
        integer invariant.

    Returns
    -------
    omega : (n,) real array, Omega^n_{xy} for every band n.
    """
    E = np.asarray(evals, dtype=float)
    Vx = velocity_matrix(evecs, dHx)
    Vy = velocity_matrix(evecs, dHy)
    n = E.size
    dE = E[:, None] - E[None, :]  # dE[n, m] = E_n - E_m
    # Im( Vx[n,m] * Vy[m,n] ); Vy.T[n,m] = Vy[m,n]
    num = np.imag(Vx * Vy.T)
    contrib = np.zeros((n, n), dtype=float)
    mask = np.abs(dE) > degen_tol
    contrib[mask] = num[mask] / dE[mask] ** 2
    np.fill_diagonal(contrib, 0.0)
    return -2.0 * contrib.sum(axis=1)


def spin_current_operator(s_gamma: np.ndarray, v_alpha: np.ndarray) -> np.ndarray:
    """Conventional spin-current operator j = (1/2){s_gamma, v_alpha} (Sinova 2015)."""
    return 0.5 * (s_gamma @ v_alpha + v_alpha @ s_gamma)


def spin_berry_curvature_kubo(
    evals: np.ndarray,
    evecs: np.ndarray,
    j_spin_x: np.ndarray,
    dHy: np.ndarray,
    *,
    degen_tol: float = 1e-6,
) -> np.ndarray:
    """Spin Berry curvature Omega^{s,n}_{xy} for SHC (Sinova 2015).

    Same as :func:`berry_curvature_kubo` but the x-vertex is the spin-current
    operator ``j_spin_x`` = (1/2){s_z, v_x} instead of the bare velocity v_x.
    """
    E = np.asarray(evals, dtype=float)
    Jx = velocity_matrix(evecs, j_spin_x)
    Vy = velocity_matrix(evecs, dHy)
    n = E.size
    dE = E[:, None] - E[None, :]
    num = np.imag(Jx * Vy.T)
    contrib = np.zeros((n, n), dtype=float)
    mask = np.abs(dE) > degen_tol
    contrib[mask] = num[mask] / dE[mask] ** 2
    np.fill_diagonal(contrib, 0.0)
    return -2.0 * contrib.sum(axis=1)


def occupied_curvature_sum(
    omega: np.ndarray,
    n_occ: int | None = None,
    *,
    evals: np.ndarray | None = None,
    e_fermi: float | None = None,
) -> float:
    """Sum of band-resolved curvature over occupied bands.

    Occupancy is set either by ``n_occ`` (lowest n bands) or by ``e_fermi``
    (bands with E < e_fermi; requires ``evals``).  Prefer ``e_fermi`` placed in
    a real gap: then the occupied set spans complete (Kramers) multiplets at
    every k, so the sum is gauge invariant -- partial band counts that *cut
    through* a degenerate multiplet give a gauge-dependent (meaningless) value.
    """
    if e_fermi is not None:
        if evals is None:
            raise ValueError("e_fermi requires evals")
        return float(np.sum(omega[np.asarray(evals) < e_fermi]))
    if n_occ is None:
        raise ValueError("provide n_occ or e_fermi")
    return float(np.sum(omega[:n_occ]))


# --------------------------------------------------------------------------- #
# Discretized gauge-invariant Chern number (Fukui-Hatsugai-Suzuki 2005)
# --------------------------------------------------------------------------- #


def _link(u_a: np.ndarray, u_b: np.ndarray) -> complex:
    """U(1) link variable det<u_a|u_b> / |det<u_a|u_b>| for occupied blocks.

    ``u_a``, ``u_b`` have shape (dim, n_occ); the overlap is the n_occ x n_occ
    matrix M = u_a^dagger u_b (non-Abelian / determinant form, Fukui 2005).
    """
    m = u_a.conj().T @ u_b
    d = np.linalg.det(m)
    return d / abs(d)


def link_variable_chern(occ_grid: np.ndarray) -> float:
    """Chern number of an occupied manifold on a 2D periodic k-mesh.

    Fukui-Hatsugai-Suzuki (2005) lattice field strength
        F_12(k) = Im ln[ U_1(k) U_2(k+1) U_1(k+2)^{-1} U_2(k)^{-1} ] in (-pi,pi]
    summed over plaquettes, C = (1/2pi) sum F_12.  Manifestly gauge invariant
    and integer-valued even on a coarse mesh.

    Parameters
    ----------
    occ_grid : (Nx, Ny, dim, n_occ) complex array of occupied eigenvectors over
        a Brillouin zone covered once (periodic; the wrap-around point is *not*
        duplicated -- index Nx maps to 0).
    """
    occ = np.asarray(occ_grid)
    Nx, Ny = occ.shape[0], occ.shape[1]
    total = 0.0
    for i in range(Nx):
        ip = (i + 1) % Nx
        for j in range(Ny):
            jp = (j + 1) % Ny
            u00 = occ[i, j]
            u10 = occ[ip, j]
            u01 = occ[i, jp]
            u11 = occ[ip, jp]
            U1 = _link(u00, u10)         # +x link at (i,j)
            U2_kx = _link(u10, u11)      # +y link at (i+1,j)
            U1_ky = _link(u01, u11)      # +x link at (i,j+1)
            U2 = _link(u00, u01)         # +y link at (i,j)
            f12 = np.log(U1 * U2_kx / (U1_ky * U2))
            total += float(np.imag(f12))
    # Sign convention: with the Berry connection A = i<u|d_k u>, the link-loop
    # field strength Im ln(plaquette) -> -Omega_xy dk^2 in the continuum, so the
    # Chern C = (1/2pi) int Omega_xy d^2k = -(1/2pi) sum Im ln(plaquette).  The
    # extra minus makes this consistent with berry_curvature_kubo (Xiao 2010);
    # verified by the Kubo<->Fukui cross-check and the massive-Dirac sign.
    return -total / (2.0 * np.pi)


# --------------------------------------------------------------------------- #
# Brillouin-zone integrals (dimensionless sums; caller applies e^2/hbar etc.)
# --------------------------------------------------------------------------- #


def anomalous_hall_sum(
    h_grid: Sequence[np.ndarray],
    dHx_grid: Sequence[np.ndarray],
    dHy_grid: Sequence[np.ndarray],
    *,
    n_occ: int | None = None,
    e_fermi: float | None = None,
    degen_tol: float = 1e-6,
) -> float:
    """BZ-averaged occupied Berry curvature (AHC integrand), mean over k points.

    Returns (1/N_k) sum_k sum_{occ} Omega^n_{xy}(k) in Angstrom^2 (occupancy by
    ``n_occ`` or ``e_fermi``; prefer ``e_fermi`` in a gap).  For a
    time-reversal-invariant system this is 0 to machine precision on a
    +/-k-symmetric mesh.
    """
    acc = 0.0
    nk = len(h_grid)
    for H, dHx, dHy in zip(h_grid, dHx_grid, dHy_grid):
        evals, evecs = np.linalg.eigh(H)
        omega = berry_curvature_kubo(evals, evecs, dHx, dHy, degen_tol=degen_tol)
        acc += occupied_curvature_sum(omega, n_occ, evals=evals, e_fermi=e_fermi)
    return acc / nk


def spin_hall_sum(
    h_grid: Sequence[np.ndarray],
    jx_grid: Sequence[np.ndarray],
    dHy_grid: Sequence[np.ndarray],
    *,
    n_occ: int | None = None,
    e_fermi: float | None = None,
    degen_tol: float = 1e-6,
) -> float:
    """BZ-averaged occupied spin Berry curvature (SHC integrand), mean over k.

    Returns (1/N_k) sum_k sum_{occ} Omega^{s,n}_{xy}(k) (occupancy by ``n_occ``
    or ``e_fermi``).  Not forced to zero by P*T (unlike AHC).  Absolute
    magnitude lacks an in-repo benchmark material -- treat as a
    relative/structural quantity (see module docstring).
    """
    acc = 0.0
    nk = len(h_grid)
    for H, jx, dHy in zip(h_grid, jx_grid, dHy_grid):
        evals, evecs = np.linalg.eigh(H)
        omega = spin_berry_curvature_kubo(evals, evecs, jx, dHy, degen_tol=degen_tol)
        acc += occupied_curvature_sum(omega, n_occ, evals=evals, e_fermi=e_fermi)
    return acc / nk


# --------------------------------------------------------------------------- #
# Kashikar-13 helpers (reuse existing model + velocity)
# --------------------------------------------------------------------------- #


def spin_operators(n_orb: int = mk.N_ORB_13) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(Sx, Sy, Sz) = (1/2) sigma (x) I_norb in the spin-major basis (hbar=1).

    Matches the spin-major layout of ``kashikar13_hamiltonian`` =
    kron(I2, H0) + SOC, i.e. the first ``n_orb`` rows are spin-up.
    """
    sx = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    sy = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
    sz = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    eye = np.eye(n_orb, dtype=complex)
    return (0.5 * np.kron(sx, eye), 0.5 * np.kron(sy, eye), 0.5 * np.kron(sz, eye))


def kashikar13_at_k(
    kvec: np.ndarray, params: Mapping[str, float], a: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return (H, dHx, dHy, dHz) for the 26x26 spinful Kashikar-13 model at k."""
    H = mk.kashikar13_hamiltonian(kvec, params, a)
    dH = tuple(vel.dH_dk_kashikar13(kvec, params, a, alpha) for alpha in (0, 1, 2))
    return (H, dH[0], dH[1], dH[2])
