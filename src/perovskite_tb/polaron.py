# SPDX-License-Identifier: MIT
# Copyright (c) 2026 tk
"""Frohlich polaron coupling and weak-coupling polaron mass (spec F6).

Dimensionless Frohlich electron-phonon coupling alpha from the high-frequency
and static dielectric constants, the LO-phonon frequency, and the band effective
mass; plus the leading weak-coupling polaron mass renormalisation.

Sources (verified real & open-access, 2026-05-24; formula read from the source):
* H. Frohlich, Adv. Phys. 3, 325 (1954), DOI 10.1080/00018735400101213.
* R. P. Feynman, Phys. Rev. 97, 660 (1955) / R. P. Feynman et al., Phys. Rev.
  127, 1004 (1962).  Variational polaron; weak-coupling mass m_p/m_b ~ 1+alpha/6.
* J. M. Frost, "Calculating polaron mobility in halide perovskites", Phys. Rev.
  B 96, 195202 (2017), DOI 10.1103/PhysRevB.96.195202 (arXiv:1704.05404).
  Frohlich alpha formula (read from ar5iv) and the MAPbI3 benchmark used here:
      alpha = (1/4 pi eps0) * (1/2)(1/eps_inf - 1/eps_static)
              * (e^2 / (hbar Omega)) * sqrt(2 m_b Omega / hbar) ,
  with Omega the LO-phonon *angular* frequency and m_b the band mass.
  Frost MAPbI3: eps_inf=4.5, eps_static=24.1, nu_LO=2.25 THz, m*=0.12 (e)/0.15
  (h) -> alpha = 2.39 (e), 2.68 (h).

TB-driven application (T1-3): the band mass m_b can be taken from the CORE TB
(``bandstructure.effective_mass`` at the R point) rather than a literature value,
so alpha is computed end-to-end from the TB.  For CsPbBr3 the TB R-point mass
m_e=0.151 (lighter than the m*=0.22 Sendner adopted) gives alpha_TB~1.66 vs the
literature alpha~2.0; since alpha ~ sqrt(m_b), the -17% difference is exactly the
mass ratio sqrt(0.151/0.22)=0.83.  TB masses for all 9 CsBX3 are tabulated in
results/tb_effective_masses.json.

Scope / honesty:
  * alpha and the *leading* weak-coupling mass (1+alpha/6) are implemented and
    validated (alpha reproduces the Frost MAPbI3 benchmark to <1%; the alpha
    formula also reproduces Sendner's CsPbBr3 alpha given m*=0.22).
  * The full finite-temperature mobility (Feynman variational + Osaka free
    energy + Hellwarth-Biaggio / Kadanoff transport) is intricate and is NOT
    implemented (cf. PolaronMobility.jl); 1+alpha/6 is only leading-order
    (alpha<~1), so the intermediate-coupling MAPbI3 mass/mobility are flagged as
    requiring the full variational treatment.
  * Applying alpha to CsBX3 needs each material's static dielectric and LO
    frequency; values used in scans must come from cited sources (no fabrication).
"""

from __future__ import annotations

import numpy as np

# SI constants (CODATA)
_E = 1.602176634e-19        # C
_HBAR = 1.054571817e-34     # J.s
_EPS0 = 8.8541878128e-12    # F/m
_ME = 9.1093837015e-31      # kg
_MEV_J = _E * 1e-3          # 1 meV in J


def omega_from_THz(nu_THz: float) -> float:
    """LO-phonon angular frequency (rad/s) from a frequency in THz."""
    return 2.0 * np.pi * nu_THz * 1e12


def omega_from_meV(hbar_omega_meV: float) -> float:
    """LO-phonon angular frequency (rad/s) from the phonon energy in meV."""
    return hbar_omega_meV * _MEV_J / _HBAR


def frohlich_alpha(eps_inf: float, eps_static: float,
                   omega_LO_rad_s: float, m_eff_rel: float) -> float:
    """Dimensionless Frohlich coupling alpha (Frost 2017, Eq. read from source).

    Parameters
    ----------
    eps_inf, eps_static : high-frequency and static (relative) dielectric constants.
    omega_LO_rad_s : LO-phonon ANGULAR frequency (rad/s) -- use omega_from_THz/meV.
    m_eff_rel : band effective mass in units of the free-electron mass.
    """
    if eps_static <= eps_inf:
        raise ValueError("eps_static must exceed eps_inf for a polar coupling")
    mb = m_eff_rel * _ME
    coulomb = 1.0 / (4.0 * np.pi * _EPS0)
    diel = 0.5 * (1.0 / eps_inf - 1.0 / eps_static)
    e2_over_hOmega = _E ** 2 / (_HBAR * omega_LO_rad_s)
    inv_length = np.sqrt(2.0 * mb * omega_LO_rad_s / _HBAR)
    return float(coulomb * diel * e2_over_hOmega * inv_length)


def weak_coupling_polaron_mass(alpha: float) -> float:
    """Leading weak-coupling polaron mass ratio m_p/m_b = 1 + alpha/6 (Feynman).

    Leading order only (valid for alpha << 1); the intermediate/strong regime
    requires the full Feynman variational solution (not implemented).
    """
    return 1.0 + alpha / 6.0
