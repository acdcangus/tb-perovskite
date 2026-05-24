# SPDX-License-Identifier: MIT
# Copyright (c) 2026 tk
"""Wilson loop / Wannier charge centers (spec F2 topology, partial).

Builds on the link-variable machinery of :mod:`berry`.  Computes the
non-Abelian Wilson loop of an occupied manifold around a non-contractible
Brillouin-zone loop, its eigenphases (hybrid Wannier charge centers, WCC), and
the Chern number from the WCC / polarization winding -- an independent
cross-check of the Fukui plaquette Chern in :mod:`berry`.

Sources (verified real & open-access, 2026-05-24):
* R. Yu, X. L. Qi, A. Bernevig, Z. Fang, X. Dai, Phys. Rev. B 84, 075119
  (2011), DOI 10.1103/PhysRevB.84.075119 (arXiv:1101.2011).  Z2 / topological
  invariant from the non-Abelian Berry connection (Wilson loop / Wannier-center
  "partner switching").
* A. A. Soluyanov, D. Vanderbilt, Phys. Rev. B 83, 235401 (2011),
  DOI 10.1103/PhysRevB.83.235401 (arXiv:1102.5600).  Hybrid Wannier charge
  centers; topological invariants without inversion symmetry.

* L. Fu, C. L. Kane, "Topological insulators with inversion symmetry", Phys.
  Rev. B 76, 045302 (2007), DOI 10.1103/PhysRevB.76.045302 (arXiv:cond-mat/
  0611341).  The parity (Fu-Kane) criterion: for an inversion-symmetric insulator
  (-1)^nu = prod_i delta_i, with delta_i the product of the parity eigenvalues of
  the occupied Kramers pairs at the time-reversal-invariant momenta (TRIM).
* L. Fu, C. L. Kane, E. J. Mele, "Topological Insulators in Three Dimensions",
  Phys. Rev. Lett. 98, 106803 (2007), DOI 10.1103/PhysRevLett.98.106803.  The
  3D Z2 (nu0;nu1nu2nu3) and the standard inversion-symmetric test models.

Scope / honesty note:
  Implemented and validated here:
  * Wilson loop, WCC, Chern-from-WCC winding (against the Qi-Wu-Zhang Chern
    insulator).
  * Fu-Kane PARITY Z2 (z2_invariant_from_parities / parity_delta_at_trim),
    validated on the standard inversion-symmetric Wilson-Dirac (BHZ-type) Z2
    model against its analytic strong-TI phase diagram (test_topology.py).
  Still deferred (to avoid unfounded results):
  * Z2 of the REAL Kashikar perovskite -- needs the inversion-operator
    representation in the Kashikar orbital basis, not derivable from in-repo
    information without guessing.  The METHOD above is ready; only the
    perovskite-specific parity operator is missing and is NOT fabricated.  (The
    cubic perovskite is P*T-symmetric with a large trivial gap, so nu=0 is
    expected, but asserting it requires the sourced operator.)

Convention: strictly-periodic TB Hamiltonians (H(k+G)=H(k)) are assumed so the
loop closes with u(k_N)=u(k_0); the QWZ and Kashikar models satisfy this.
"""

from __future__ import annotations

import numpy as np


def wilson_loop(occ_line: np.ndarray) -> np.ndarray:
    """Non-Abelian Wilson loop matrix around a closed k-loop.

    Parameters
    ----------
    occ_line : (N, dim, n_occ) complex array of occupied eigenvectors at N
        points along a non-contractible loop (the (N)-th point is identified
        with the 0-th via Hamiltonian periodicity; do *not* duplicate it).

    Returns
    -------
    W : (n_occ, n_occ) unitary Wilson loop matrix.  Each overlap
        M_i = <u_i|u_{i+1}> is replaced by its unitary part (polar/SVD,
        M = U S V^dagger -> U V^dagger) so the loop is exactly unitary at finite
        N (Yu 2011); this leaves det's phase -- hence the polarization and Chern
        -- unchanged (S is positive real).
    """
    occ = np.asarray(occ_line)
    N, _, n_occ = occ.shape
    W = np.eye(n_occ, dtype=complex)
    for i in range(N):
        M = occ[i].conj().T @ occ[(i + 1) % N]
        U, _, Vh = np.linalg.svd(M)
        W = W @ (U @ Vh)
    return W


def wannier_charge_centers(W: np.ndarray) -> np.ndarray:
    """Hybrid Wannier charge centers = eigenphases of the Wilson loop / 2pi.

    Returned in ascending order within (-1/2, 1/2] (units of the lattice
    constant along the loop direction).
    """
    theta = np.angle(np.linalg.eigvals(W))
    return np.sort(theta / (2.0 * np.pi))


def polarization_phase(W: np.ndarray) -> float:
    """U(1) Berry phase of the occupied manifold along the loop = Im ln det W."""
    return float(np.angle(np.linalg.det(W)))


def chern_from_wcc(occ_grid: np.ndarray) -> float:
    """Chern number from the winding of the Wilson-loop polarization.

    The Wilson loop is taken along axis 1 (k_parallel) at each fixed value of
    axis 0 (k_perp); the net winding of the polarization phase as k_perp sweeps
    the BZ equals the Chern number (Yu 2011).  Sign is set to match the Fukui /
    Xiao Berry-curvature convention of :mod:`berry` (verified by cross-check).

    Parameters
    ----------
    occ_grid : (N_perp, N_par, dim, n_occ) occupied eigenvectors over a BZ
        covered once (periodic; wrap-around points not duplicated).
    """
    occ = np.asarray(occ_grid)
    n_perp = occ.shape[0]
    phis = np.array([polarization_phase(wilson_loop(occ[i])) for i in range(n_perp)])
    # close the perpendicular loop, unwrap, net change / 2pi
    closed = np.concatenate([phis, phis[:1]])
    dphi = np.diff(np.unwrap(closed))
    return -float(np.sum(dphi) / (2.0 * np.pi))


# --- Fu-Kane parity Z2 (inversion-symmetric insulators) -----------------------

def parity_delta_at_trim(H_trim: np.ndarray, parity_op: np.ndarray,
                         n_occ: int, *, tol: float = 1e-6) -> int:
    """Fu-Kane delta = product of occupied Kramers-pair parities at one TRIM.

    At a time-reversal-invariant momentum the Bloch Hamiltonian commutes with the
    parity (inversion) operator ``parity_op`` (P^2 = 1, P^dagger = P).  The two
    members of each Kramers pair share a parity eigenvalue; ``delta`` is the
    product over the ``n_occ/2`` occupied pairs (Fu-Kane, PRB 76, 045302).

    Parameters
    ----------
    H_trim : (d, d) Bloch Hamiltonian at the TRIM (must commute with parity_op).
    parity_op : (d, d) Hermitian, involutory (P^2 = I) parity matrix.
    n_occ : number of occupied bands (must be even -- Kramers pairs).

    Returns +1 or -1.
    """
    if n_occ % 2 != 0:
        raise ValueError("n_occ must be even (Kramers pairs) for the parity Z2")
    H = 0.5 * (H_trim + H_trim.conj().T)
    if not np.allclose(H @ parity_op, parity_op @ H, atol=1e-8):
        raise ValueError("Hamiltonian does not commute with parity at this TRIM")
    evals, U = np.linalg.eigh(H)
    occ = U[:, :n_occ]
    xi = np.real(np.einsum("ai,ab,bi->i", occ.conj(), parity_op, occ))  # <u|P|u>
    if not np.allclose(np.abs(xi), 1.0, atol=1e-3):
        raise ValueError(f"parity eigenvalues not +-1 (degenerate mixing?): {xi}")
    signs = np.round(xi).astype(int)
    n_plus = int(np.sum(signs > 0))
    n_minus = int(np.sum(signs < 0))
    if n_plus % 2 or n_minus % 2:
        raise ValueError(f"parities not Kramers-paired: +{n_plus}/-{n_minus}")
    # each pair contributes one factor -> (+1)^(n_plus/2) * (-1)^(n_minus/2)
    return int((-1) ** (n_minus // 2))


def z2_invariant_from_parities(deltas) -> int:
    """Strong Z2 index nu in {0,1} from the TRIM parity products (Fu-Kane).

    (-1)^nu = prod_i delta_i  over all TRIM (4 in 2D, 8 in 3D for nu0).
    """
    prod = int(np.prod([int(d) for d in deltas]))
    if prod not in (1, -1):
        raise ValueError(f"delta product must be +-1, got {prod}")
    return 0 if prod == 1 else 1
