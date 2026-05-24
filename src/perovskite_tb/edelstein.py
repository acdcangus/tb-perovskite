# SPDX-License-Identifier: MIT
# Copyright (c) 2026 tk
"""Edelstein effect: current-induced spin polarization (spec F11).

Linear-response spin density induced by a charge current / electric field in
inversion-broken systems, in the constant-relaxation-time (CRTA) Boltzmann
approximation.  Reuses the Fermi window of :mod:`thermo`, the spin operators of
:mod:`berry`, and the spin texture of :mod:`rashba`.

Source (verified real & open-access, 2026-05-24):
* V. M. Edelstein, "Spin polarization of conduction electrons induced by
  electric current in two-dimensional asymmetric electron systems", Solid State
  Commun. 73, 233 (1990), DOI 10.1016/0038-1098(90)90963-C.

CRTA (Boltzmann) response  delta S_a = chi_{ab} E_b  with
    chi_{ab}/(e tau) = -(1/N_k) sum_{n,k} (-df/dE_{nk}) <S_a>_{nk} v_b(nk) .
This is a Fermi-surface average of <S_a> v_b.

Symmetry: in a centrosymmetric system <S_a>(-k)=<S_a>(k) (spin even) while
v_b(-k)=-v_b(k) (velocity odd), so the integrand is odd and chi=0.  A Rashba
(inversion-broken) system gives chi perpendicular to the current (chi_{yx}!=0,
chi_{xx}=0) -- the Rashba-Edelstein effect.

Validity / honesty:
  * The per-band formula assumes NON-DEGENERATE bands; for a degenerate
    (Kramers) manifold the multiplet trace is required, and the per-band
    diagonal <S_a><v_b> is gauge dependent.  The cubic Pm-3m perovskite is
    Kramers-degenerate at every k, so its (vanishing, by symmetry) Edelstein
    response is *not* evaluated band-by-band here; use the inversion-broken
    polar (P4mm) case, whose bands are non-degenerate for k>0.
  * Absolute magnitude needs a material/scattering tau (out of scope) -> the
    response is returned divided by (e tau); trust symmetry/structure (chi=0 vs
    perpendicular chi) and relative trends.  Blount TB limitation applies.
  * The tau-INDEPENDENT Edelstein EFFICIENCY chi_{ab}/sigma_{bb}
    (:func:`edelstein_ratio`) removes the relaxation time and the k-grid
    normalisation; for the 2D Rashba model it reduces to the analytic
    m*alpha_R/(4 mu) (small alpha, S=sigma/2), which is verified in the tests,
    making the ratio a quantitatively-anchored figure of merit.
"""

from __future__ import annotations

import numpy as np

from . import berry, rashba, thermo


def edelstein_susceptibility(
    energies: np.ndarray, spin_a: np.ndarray, velocity_b: np.ndarray,
    mu: float, T: float,
) -> float:
    """chi_{ab}/(e tau) = -(1/N_k) sum_{n,k} (-df/dE) <S_a> v_b  (Edelstein 1990).

    energies, spin_a, velocity_b : arrays of identical shape (N_k, n_bands) --
    band energies (eV), spin expectation <S_a> (hbar units), and group velocity
    v_b = dE/dk_b (eV.Angstrom).
    """
    w = thermo._minus_dfde(np.asarray(energies), mu, T)
    return -float(np.sum(w * np.asarray(spin_a) * np.asarray(velocity_b))) / energies.shape[0]


def longitudinal_conductivity(
    energies: np.ndarray, velocity_b: np.ndarray, mu: float, T: float,
) -> float:
    """CRTA longitudinal conductivity sigma_bb/(e^2 tau) = (1/N_k) sum (-df/dE) v_b^2.

    Same Fermi window and k-measure as :func:`edelstein_susceptibility`, so the
    ratio chi_{ab}/sigma_bb is independent of the relaxation time tau and of the
    overall k-grid normalisation (the Edelstein "efficiency").
    """
    w = thermo._minus_dfde(np.asarray(energies), mu, T)
    return float(np.sum(w * np.asarray(velocity_b) ** 2)) / energies.shape[0]


def edelstein_ratio(
    energies: np.ndarray, spin_a: np.ndarray, velocity_b: np.ndarray,
    mu: float, T: float,
) -> float:
    """tau-independent Edelstein efficiency chi_{ab}/sigma_bb (= delta S_a per unit j_b).

    Equals [chi_{ab}/(e tau)] / [sigma_bb/(e^2 tau)] with e=1; the relaxation time
    and the k-grid normalisation cancel.  For the 2D Rashba model this reduces to
    the analytic m*alpha_R/(4 mu) (small alpha, S = sigma/2); see tests.
    """
    sig = longitudinal_conductivity(energies, velocity_b, mu, T)
    chi = edelstein_susceptibility(energies, spin_a, velocity_b, mu, T)
    return chi / sig


def band_data_polar_kashikar13(
    kpts, params, a, polar_displacement_z: float, spin_axis: int, vel_axis: int
):
    """(E, <S_spin_axis>, v_vel_axis) per (k, band) for the polar Kashikar-13 model."""
    from .shift_current import make_polar_kashikar13_builders

    H_fn, dHdk_fn, _ = make_polar_kashikar13_builders(params, a, polar_displacement_z)
    S = berry.spin_operators(13)[spin_axis]
    E_all, spin_all, vel_all = [], [], []
    for k in np.asarray(kpts):
        H = H_fn(k)
        evals, evecs = np.linalg.eigh(0.5 * (H + H.conj().T))
        dH = dHdk_fn(k, vel_axis)
        E_all.append(evals)
        spin_all.append(rashba.spin_texture(evecs, S))
        vel_all.append(np.real(np.diag(berry.velocity_matrix(evecs, dH))))
    return np.array(E_all), np.array(spin_all), np.array(vel_all)
