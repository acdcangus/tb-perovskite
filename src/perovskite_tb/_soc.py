"""Atomic spin-orbit coupling (SOC) matrices for real orbitals.

The on-site SOC term is ``H_SO = lambda * L . S`` with ``S = sigma / 2``
(hbar = 1).  For p-orbitals this is the textbook construction; we build it from
the action of the orbital angular-momentum operators on the *real* p-orbitals
``(px, py, pz)``:

    Lx|py> =  i|pz>,  Lx|pz> = -i|py>
    Ly|pz> =  i|px>,  Ly|px> = -i|pz>
    Lz|px> =  i|py>,  Lz|py> = -i|px>

(see e.g. Slater-Koster construction; consistent with L acting on l=1).

Eigenvalues of ``lambda * L.S`` on the 6-dim p-spin space are:
    +lambda/2 (4-fold, j = 3/2)  and  -lambda (2-fold, j = 1/2),
so the j=3/2 / j=1/2 splitting is ``3*lambda/2`` and the trace is zero.
This is asserted in tests/test_soc.py.

Spin ordering convention used throughout the package: **spin-major**, i.e. all
spin-up components first, then all spin-down.  Within each spin block the
orbital order is (px, py, pz).
"""

from __future__ import annotations

import numpy as np

# Orbital angular momentum operators in the real (px, py, pz) basis (hbar = 1).
_LX = np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex)
_LY = np.array([[0, 0, 1j], [0, 0, 0], [-1j, 0, 0]], dtype=complex)
_LZ = np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex)

# Pauli matrices.
_SX = np.array([[0, 1], [1, 0]], dtype=complex)
_SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
_SZ = np.array([[1, 0], [0, -1]], dtype=complex)


def soc_p_matrix(lam: float) -> np.ndarray:
    """Return the 6x6 ``lambda * L.S`` matrix on (px,py,pz) x (up,down).

    Spin-major ordering: rows/cols are
    (px-up, py-up, pz-up, px-down, py-down, pz-down).
    """
    # S = sigma / 2 ; build L.S = Lx (x) Sx + Ly (x) Sy + Lz (x) Sz
    # with spin as the outer (block) index -> kron(spin, orbital).
    ls = (
        np.kron(_SX / 2.0, _LX)
        + np.kron(_SY / 2.0, _LY)
        + np.kron(_SZ / 2.0, _LZ)
    )
    return lam * ls
