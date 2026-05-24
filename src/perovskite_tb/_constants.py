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
