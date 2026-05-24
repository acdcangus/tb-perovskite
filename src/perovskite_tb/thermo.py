# SPDX-License-Identifier: MIT
# Copyright (c) 2026 tk
"""Boltzmann transport: Seebeck, electrical & electronic-thermal conductivity.

Spec F9 (extention/03_tb-perovskite_spec.md); future_themes Theme (thermoelectric).
Semiclassical Boltzmann transport in the constant-relaxation-time approximation
(CRTA), built on the existing band structure + group velocities (velocity.py).

Source (verified real & open-access, 2026-05-24):
* G. K. H. Madsen, D. J. Singh, "BoltzTraP. A code for calculating
  band-structure dependent quantities", Comput. Phys. Commun. 175, 67 (2006),
  DOI 10.1016/j.cpc.2006.03.007 (arXiv:cond-mat/0602203).

Transport distribution function (CRTA, tau factored out):
    Sigma_xx(e) = (1/N_k) sum_{n,k} v_x(n,k)^2 delta(e - E_{n,k}) .
Moments  L^(a)(mu,T) = int de (-df/de) (e-mu)^a Sigma_xx(e)  give
    sigma_xx / tau   = e^2 L^(0)
    S_xx             = -(1/(e T)) L^(1)/L^(0)
    kappa^e_xx / tau = (1/T) [ L^(2) - (L^(1))^2 / L^(0) ] .
The Lorenz number kappa^e/(sigma T) -> (pi^2/3)(k_B/e)^2 in the degenerate
(Sommerfeld) limit -- the Wiedemann-Franz law, used here as an exact V&V anchor
independent of band details.

Units: energies in eV, T in Kelvin, k_B in eV/K.  Seebeck is returned in units
of k_B/e (= 86.173 uV/K); the Lorenz number in units of (k_B/e)^2; sigma and
kappa^e are returned divided by tau and by e^2 (relative units) -- absolute
values require a material/scattering-specific relaxation time tau, which is
out of scope (honest limitation, like the absolute SHC/shift-current).
"""

from __future__ import annotations

import numpy as np

from . import berry

KB_EV = 8.617333262e-5  # Boltzmann constant, eV/K


def _minus_dfde(egrid: np.ndarray, mu: float, T: float) -> np.ndarray:
    """-df/dE for the Fermi-Dirac function (numerically stable)."""
    x = (np.asarray(egrid) - mu) / (KB_EV * T)
    # -df/dE = 1/(4 k_B T) * sech^2(x/2);  sech(y)=1/cosh(y)
    return 1.0 / (KB_EV * T) * 0.25 / np.cosh(np.clip(x, -350, 350) / 2.0) ** 2


def transport_distribution(
    energies: np.ndarray, vx: np.ndarray, egrid: np.ndarray, eta: float
) -> np.ndarray:
    """CRTA transport distribution Sigma_xx(e) (Gaussian-broadened delta).

    energies, vx : flattened arrays over (n, k); vx is the band group velocity
        v_x = dE/dk_x (eV.Angstrom).  eta : Gaussian smearing width (eV).
    """
    E = np.asarray(energies).ravel()
    v = np.asarray(vx).ravel()
    eg = np.asarray(egrid)
    norm = 1.0 / (eta * np.sqrt(2.0 * np.pi))
    Sigma = np.zeros_like(eg)
    for Ei, vi in zip(E, v):
        Sigma += vi * vi * norm * np.exp(-0.5 * ((eg - Ei) / eta) ** 2)
    return Sigma / E.size


def transport_coefficients(
    egrid: np.ndarray, Sigma: np.ndarray, mu: float, T: float
) -> dict:
    """Boltzmann transport coefficients from Sigma(e) at (mu, T).

    Returns dict: sigma_over_tau (e^2 L0, rel.), seebeck_kB_e (S in k_B/e units),
    kappa_e_over_tau (rel.), lorenz_kB_e2 (Lorenz number in (k_B/e)^2 units).
    """
    eg = np.asarray(egrid)
    w = _minus_dfde(eg, mu, T)
    de = eg[1] - eg[0]
    L0 = np.sum(w * Sigma) * de
    L1 = np.sum(w * (eg - mu) * Sigma) * de
    L2 = np.sum(w * (eg - mu) ** 2 * Sigma) * de
    kappa = (L2 - L1 * L1 / L0) / T
    return {
        "sigma_over_tau": float(L0),                       # e^2 = 1
        "seebeck_kB_e": float(-(L1 / L0) / (KB_EV * T)),   # S in units of k_B/e
        "kappa_e_over_tau": float(kappa),
        "lorenz_kB_e2": float((L2 - L1 * L1 / L0) / (L0 * (KB_EV * T) ** 2)),
    }


def band_group_velocities_kashikar13(kpts, params, a, alpha: int = 0):
    """(E, v_alpha) over k points for the 26-band Kashikar-13 model.

    v_alpha(n,k) = <n k| dH/dk_alpha |n k> (group velocity, eV.Angstrom).
    Returns (energies (Nk,26), v (Nk,26)).
    """
    E_all, v_all = [], []
    for k in np.asarray(kpts):
        H, dHx, dHy, dHz = berry.kashikar13_at_k(k, params, a)
        dH = (dHx, dHy, dHz)[alpha]
        evals, evecs = np.linalg.eigh(H)
        V = berry.velocity_matrix(evecs, dH)
        E_all.append(evals)
        v_all.append(np.real(np.diag(V)))
    return np.array(E_all), np.array(v_all)
