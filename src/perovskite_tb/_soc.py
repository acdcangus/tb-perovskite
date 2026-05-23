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

    Here ``lam`` is the coefficient of ``L.S`` itself, so the eigenvalues are
    ``+lam/2`` (4-fold) and ``-lam`` (2-fold) and the j=3/2 / j=1/2 splitting is
    ``3*lam/2``.

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


def soc_p_from_lambda3(lam3: float) -> np.ndarray:
    """SOC matrix for the "lambda = Delta/3" convention used by the source papers.

    Both Kashikar et al. (arXiv:2101.08562, Eq. 10) and the Jancu sp3d5s* scheme
    adopted by Nestoklon (arXiv:2012.14705) parametrise the p-orbital SOC by a
    coefficient ``lambda`` (= Delta/3, with Delta the atomic p-splitting) such
    that the **p1/2 / p3/2 splitting equals 3*lambda = Delta**.  Kashikar's
    explicit 6x6 matrix (Eq. 10) has entries of magnitude {0, 1} = 2*(L.S), i.e.
    ``H_SO = lambda * (2 L.S)``.  We implement exactly that:

        H_SO = 2 * lambda * L.S    ->    eigenvalues {+lambda (x4), -2 lambda (x2)},
        splitting = 3*lambda.

    Sanity: Pb 6p with lambda = 0.5413 (Nestoklon Delta_c/3) gives an atomic
    splitting 3*0.5413 = 1.62 eV, consistent with the paper's CB SO splitting of
    1.48 eV at R (reduced from atomic by Pb-I hybridisation).
    """
    return soc_p_matrix(2.0 * lam3)
