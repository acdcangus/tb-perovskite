# SPDX-License-Identifier: MIT
# Copyright (c) 2026 tk
"""Rashba / inversion-breaking spin-splitting analysis (spec F4).

Spin texture <S>(k) and the linear-in-k spin-splitting coefficient for systems
with broken inversion symmetry.  Reuses the spin operators of :mod:`berry` and
the spinful polar (P4mm) Kashikar-13 Hamiltonian of :mod:`shift_current`.

Sources (verified real & open-access, 2026-05-24):
* Y. A. Bychkov, E. I. Rashba, "Properties of a 2D electron gas with lifted
  spectral degeneracy", JETP Lett. 39, 78 (1984).  Rashba Hamiltonian
  H_R = alpha_R (sigma x k).z_hat ; the band-edge doublet splits as
  Delta E = 2 alpha_R |k| with the spin locked perpendicular to k.
* D. Niesner et al., "Giant Rashba Splitting in CH3NH3PbBr3 ...", Phys. Rev.
  Lett. 117, 126401 (2016), DOI 10.1103/PhysRevLett.117.126401
  (arXiv:1606.05867).  SURFACE Rashba (~11 eVA) -- NOT a bulk benchmark.
* P. Bhumla, D. Gill, S. Sheoran, S. Bhattacharya, "Origin of Rashba
  Spin-Splitting and Strain Tunability in Ferroelectric Bulk CsPbF3",
  arXiv:2108.03683 (2021).  BULK DFT Rashba for an inorganic Cs perovskite (the
  right comparison class): alpha_R(CBM)=1.05, alpha_R(VBM)=0.41 eVA, P=34
  uC/cm^2 (verified web 2026-05-24).

Symmetry: cubic Pm-3m CsBX3 is centrosymmetric (P) and time-reversal (T)
invariant -> Kramers degeneracy at every k -> alpha_R = 0.  A [001] polar
displacement (P4mm, shift_current.make_polar_kashikar13_builders) breaks P and
lifts the degeneracy for |k|>0 (the degeneracy at the TRIM k=0 is protected by
Kramers' theorem).

Bulk DFT comparison (T2-1, see data/parameters/rashba_bulk_benchmark.json):
  * QUALITATIVE (category C): the TB reproduces alpha_R=0 (cubic) -> !=0 (polar),
    spin-momentum locking, and the CBM Rashba DOMINATING over the VBM -- the same
    ordering as the CsPbF3 DFT (CBM 1.05 > VBM 0.41 eVA).
  * MAGNITUDE (category D): the TB CBM alpha_R ~ 0.03 eVA (polar displacement 0.4)
    is ~40x SMALLER than the bulk DFT ~1 eVA, and does not reach order-of-
    magnitude agreement.  The polar model is a crude rigid sublattice displacement
    (uncalibrated to a real ferroelectric distortion) and the SK-TB position
    operator lacks covalent (Blount) corrections -> the absolute alpha_R is
    underestimated.  Surface values (Niesner ~11 eVA) are a different system and
    are excluded.  Trust the sign, spin-locking, and CBM>VBM ordering; the
    absolute alpha_R is indicative only.
"""

from __future__ import annotations

import numpy as np

from ._constants import HBAR2_OVER_M0


def spin_texture(evecs: np.ndarray, s_op: np.ndarray) -> np.ndarray:
    """Per-band spin expectation <n|S|n> = Re diag(U^dagger S U)."""
    return np.real(np.diag(evecs.conj().T @ s_op @ evecs))


def doublet_splitting(H: np.ndarray, band_index: int) -> float:
    """Energy splitting E[band_index+1] - E[band_index] of a (Kramers) doublet."""
    ev = np.linalg.eigvalsh(0.5 * (H + H.conj().T))
    return float(ev[band_index + 1] - ev[band_index])


def rashba_coefficient(H_fn, band_index: int, k_mag: float, axis: int = 0) -> float:
    """Linear-in-k spin-splitting coefficient alpha_R = Delta E / (2|k|).

    Evaluated for the doublet (band_index, band_index+1) at k = k_mag along
    ``axis`` (units of H_fn's k).  For the analytic Rashba model this returns
    alpha_R exactly; for a real band it is the local linear coefficient (valid
    for small k_mag, where the splitting is linear).
    """
    k = np.zeros(3)
    k[axis] = k_mag
    return doublet_splitting(H_fn(k), band_index) / (2.0 * k_mag)


def analytic_rashba_builder(alpha_R: float, meff: float = 1.0):
    """H(k) = (hbar^2 k^2 / 2 m*) I + alpha_R (k_x sigma_y - k_y sigma_x).

    The textbook 2D Rashba Hamiltonian (Bychkov-Rashba 1984); for validation.
    """
    sx = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    sy = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
    c = HBAR2_OVER_M0 / meff  # hbar^2/m* (eV.A^2), single source of truth

    def H_fn(kvec):
        k = np.asarray(kvec, dtype=float)
        kin = 0.5 * c * float(k @ k) * np.eye(2, dtype=complex)
        return kin + alpha_R * (k[0] * sy - k[1] * sx)

    return H_fn
