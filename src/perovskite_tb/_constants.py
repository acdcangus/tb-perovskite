# SPDX-License-Identifier: MIT
# Copyright (c) 2026 tk
"""Shared physical constants (single source of truth).

Centralised here so the value is defined once (DRY); previously duplicated in
exciton.py / optical.py / velocity.py / g_factor.py.
"""

from __future__ import annotations

# hbar^2 / m0 in eV * Angstrom^2  (= 2 * 3.80998 eV.A^2).
# Converts the momentum matrix element P = hbar*p/m0 [eV.A] into the Kane term
# P^2 / (hbar^2/m0), and the band curvature d^2E/dk^2 into m*/m0.
HBAR2_OVER_M0 = 7.619964  # eV * Angstrom^2

# Hydrogen Rydberg (eV) -- Wannier-Mott binding scale.
RYDBERG_EV = 13.605693

# Free-electron Lande g-factor.
G0 = 2.0023193

# Boltzmann constant in eV/K.
KB_EV = 8.617333262e-5

# Coulomb constant e^2/(4 pi eps0) in eV * Angstrom.
COULOMB_EV_ANG = 14.39964
