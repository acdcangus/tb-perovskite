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

Scope / honesty note:
  Implemented and validated here (against the Qi-Wu-Zhang Chern insulator):
  Wilson loop, WCC, and Chern-from-WCC winding.
  NOT implemented (deliberately skipped to avoid unfounded results):
  * Fu-Kane parity Z2 -- requires the inversion-operator representation in the
    Kashikar orbital basis, which is not derivable from in-repo information
    without guessing (would risk hallucination; per project no-hallucination
    rule it is deferred until the inversion representation is sourced).
  * Soluyanov-Vanderbilt time-reversal Z2 "partner switching" for the real
    perovskite -- the method is implementable but a *validated* result needs a
    known 3D-Z2 reference model; deferred.

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
