"""Wannier-Mott exciton binding energy from TB effective masses + optical eps.

Theme I.  Combines two existing ingredients:
  * band-edge effective masses m_e, m_h from the TB band curvature (this module), and
  * the optical dielectric constant eps (Phase 1.5, optical.py, eps_real[0]),
into the hydrogenic Wannier-Mott estimate

    E_b = (mu / m0) / eps_r^2 * Ry ,   Ry = 13.6057 eV,   1/mu = 1/m_e + 1/|m_h|.

Refs: Yang et al., PRB 96, 035301 (2017); Tanaka et al., Solid State Commun. 127,
619 (2003); Cho et al. 2019 (arXiv:1908.09436, GW-BSE benchmark).

CAVEAT: using the high-frequency (electronic) eps_inf gives an UPPER BOUND on E_b;
the physical exciton is screened additionally by the lattice (ionic/phonon)
contribution, so the effective screening lies between eps_inf and the static eps_0
and the true E_b is smaller (often 3-4x for halide perovskites).  Relative trends
across materials are the robust deliverable.  Absolute magnitude is further limited
by the TB intra-atomic incompleteness (Blount 1962), same as the other themes.

Effective mass: m*/m0 = (hbar^2/m0) / (d^2E/dk^2), with hbar^2/m0 = 7.619964 eV.Ang^2.
"""

from __future__ import annotations

from typing import Callable, Sequence

import numpy as np

RYDBERG_EV = 13.605693       # hydrogen Rydberg (eV)
HBAR2_OVER_M0 = 7.619964     # hbar^2/m0 in eV.Ang^2 (same constant as velocity.py)


def effective_mass(H_fn: Callable[[np.ndarray], np.ndarray], a: float, band_idx: int,
                   k_point: Sequence[float] | None = None, dk: float = 1e-3,
                   directions: Sequence[Sequence[float]] | None = None) -> float:
    """Band effective mass m*/m0 (signed) from the curvature of band ``band_idx``.

    Central second difference of E(k) along each Cartesian direction at ``k_point``
    (default the R-point pi/a (1,1,1), the direct-gap edge of cubic CsBX3), averaged
    over directions (isotropic for the cubic point group).  Sign is kept: conduction
    edges give +, valence edges give - (use abs() for the hole mass).
    """
    if k_point is None:
        k_point = np.array([1.0, 1.0, 1.0]) * np.pi / a
    k0 = np.asarray(k_point, float)
    if directions is None:
        directions = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]

    def E(k):
        Hk = H_fn(k)
        Hk = 0.5 * (Hk + Hk.conj().T)
        return np.sort(np.linalg.eigvalsh(Hk).real)[band_idx]

    masses = []
    for d in directions:
        dvec = np.asarray(d, float)
        dvec = dvec / np.linalg.norm(dvec)
        h = dk * (2.0 * np.pi / a) * dvec            # step in Cartesian k (1/Ang)
        step = dk * (2.0 * np.pi / a)
        d2E = (E(k0 + h) - 2.0 * E(k0) + E(k0 - h)) / step ** 2   # eV.Ang^2
        masses.append(HBAR2_OVER_M0 / d2E)
    return float(np.mean(masses))


def reduced_mass(m_e: float, m_h: float) -> float:
    """Exciton reduced mass mu/m0 = 1 / (1/|m_e| + 1/|m_h|)."""
    return 1.0 / (1.0 / abs(m_e) + 1.0 / abs(m_h))


def wannier_mott_binding_eV(mu_over_m0: float, eps_r: float) -> float:
    """Hydrogenic Wannier-Mott exciton binding energy (eV).

    E_b = (mu/m0) / eps_r^2 * Ry.  Pass eps_r = eps_inf for the electronic-screening
    upper bound (see module caveat)."""
    return mu_over_m0 / eps_r ** 2 * RYDBERG_EV
