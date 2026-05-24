# SPDX-License-Identifier: MIT
# Copyright (c) 2026 tk
"""Finite z-slab / superlattice of the cubic perovskite (spec F5/F13/F14-A).

Builds a finite-thickness (or periodically-stacked) slab of the cubic
Kashikar-13 perovskite with the in-plane momentum (k_x, k_y) kept as good
quantum numbers and z made real-space (open or periodic boundary).  Used for
2D-Ruddlesden-Popper-style quantum confinement E_g(N) (F5), the periodic
mini-band stack (F13), and the slab Stark effect under a z field (F14 mode A).

Method: the 3D Bloch Hamiltonian is gauge-transformed by
U(k_z) = diag(exp(-i k_z z_alpha)) (z_alpha = the intra-cell z position of each
orbital; the X_z halide orbitals sit at z = a/2, the rest at z = 0) so that it
becomes 2pi/a-periodic in k_z, and is then decomposed by an exact Fourier
transform into the intra-cell block H_par(k_x,k_y) and the inter-cell hopping
T(k_x,k_y): H(k) = H_par + T e^{i k_z a} + T^dagger e^{-i k_z a}.  The slab is the
block-tridiagonal matrix built from these (open or periodic in z).  The
decomposition is verified to machine precision (reconstruction test) -- this is
a self-correcting check on the layer split.

Sources (verified real, 2026-05-24):
* D. L. Smith, C. Mailhiot, "Theory of semiconductor superlattice electronic
  structure", Rev. Mod. Phys. 62, 173 (1990), DOI 10.1103/RevModPhys.62.173.
  (Tight-binding / boundary-condition superlattice electronic structure.)
* J. Even, L. Pedesseau, C. Katan, "Understanding Quantum Confinement of Charge
  Carriers in Layered 2D Hybrid Perovskites", ChemPhysChem 15, 3733 (2014),
  DOI 10.1002/cphc.201402428.  (2D-RP quantum confinement; the organic spacer
  is treated here as a hard barrier = open boundary.)
* J.-C. Blancon et al., Science 355, 1288 (2017) -- n-dependent 2D-RP gap.
* (F14-A field) J. Neugebauer, M. Scheffler, PRB 46, 16067 (1992) -- dipole/
  scalar-potential treatment of a field across a slab.

Scope/honesty: the spacer/passivation is the hard-barrier (open-BC) idealisation
(Even 2014); no explicit organic-cation orbitals or surface reconstruction.
Validation is model-internal (exact reconstruction, periodic-slab == 3D bands,
bulk limit); the n-dependent gap follows the confinement trend qualitatively
(Blancon 2017) but absolute E_g(n) carries the usual SK-TB/Blount caveats.
"""

from __future__ import annotations

import numpy as np

from . import models_kashikar as mk

N_OCC_PER_CELL = 20  # occupied bands per 26-band spinful cell


def _orbital_z(a: float) -> np.ndarray:
    """Intra-cell z position of each of the 26 spin-major orbitals (X_z at a/2)."""
    z = np.zeros(mk.N_ORB_13)
    base_z = mk._HALIDE_BLOCK[2]
    for i in range(3):
        z[base_z + i] = a / 2.0
    return np.concatenate([z, z])  # spin-major


def layer_blocks(params, a, kx, ky, *, n_z: int = 12):
    """Intra-cell block H_par and inter-cell hopping T at (kx, ky).

    H(kx,ky,kz) (gauge-transformed) = H_par + T e^{i kz a} + T^dagger e^{-i kz a}.
    """
    z2 = _orbital_z(a)
    kzs = (2.0 * np.pi / a) * np.arange(n_z) / n_z
    Hs = np.empty((n_z, 26, 26), dtype=complex)
    for i, kz in enumerate(kzs):
        H = mk.kashikar13_hamiltonian(np.array([kx, ky, kz]), params, a)
        U = np.diag(np.exp(-1j * kz * z2))
        Hs[i] = U @ H @ U.conj().T
    Hpar = Hs.mean(axis=0)
    T = (Hs * np.exp(-1j * kzs * a)[:, None, None]).mean(axis=0)
    Hpar = 0.5 * (Hpar + Hpar.conj().T)
    return Hpar, T


def reconstruct_3d(Hpar, T, kz, a):
    """H_par + T e^{i kz a} + T^dagger e^{-i kz a} (gauge-transformed 3D H)."""
    return Hpar + T * np.exp(1j * kz * a) + T.conj().T * np.exp(-1j * kz * a)


def slab_hamiltonian(Hpar, T, N, *, periodic=False, onsite_shift=None):
    """Block-tridiagonal N-cell slab from intra-cell H_par and inter-cell T.

    onsite_shift : optional length-N array added (×I) to each cell's diagonal
        block (e.g. a Stark scalar potential).  periodic=True wraps cell N-1->0.
    """
    D = Hpar.shape[0]
    H = np.zeros((N * D, N * D), dtype=complex)
    for j in range(N):
        blk = Hpar if onsite_shift is None else Hpar + onsite_shift[j] * np.eye(D)
        H[j * D:(j + 1) * D, j * D:(j + 1) * D] = blk
    for j in range(N - 1):
        H[j * D:(j + 1) * D, (j + 1) * D:(j + 2) * D] = T
        H[(j + 1) * D:(j + 2) * D, j * D:(j + 1) * D] = T.conj().T
    if periodic and N > 1:
        H[(N - 1) * D:N * D, 0:D] = T
        H[0:D, (N - 1) * D:N * D] = T.conj().T
    return 0.5 * (H + H.conj().T)


def slab_eigenvalues(params, a, kx, ky, N, *, periodic=False, e_field_z=0.0,
                     inter_layer_scale=1.0):
    """Slab eigenvalues at (kx, ky) for N cells.

    e_field_z : z electric field (V/Angstrom); adds the Stark scalar potential
        V_n = -e E z_n with z_n = n*a (e=1, energies in eV) (F14 mode A).
    inter_layer_scale : multiply the inter-cell hopping T (weak coupling ->
        narrow mini-bands, the 2D-RP-with-spacer limit) (F13).
    """
    Hpar, T = layer_blocks(params, a, kx, ky)
    T = inter_layer_scale * T
    shift = None
    if e_field_z != 0.0:
        shift = np.array([-e_field_z * (n * a) for n in range(N)])
    H = slab_hamiltonian(Hpar, T, N, periodic=periodic, onsite_shift=shift)
    return np.linalg.eigvalsh(H)


def slab_gap(params, a, kx, ky, N, *, periodic=False, n_occ_per_cell=N_OCC_PER_CELL):
    """Fundamental gap of the N-cell slab at (kx, ky)."""
    ev = slab_eigenvalues(params, a, kx, ky, N, periodic=periodic)
    n_occ = n_occ_per_cell * N
    return float(ev[n_occ] - ev[n_occ - 1])
