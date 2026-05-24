# SPDX-License-Identifier: MIT
# Copyright (c) 2026 tk
"""Berry-phase electronic polarization (KSV) -- spec F14 mode B.

Modern-theory-of-polarization Berry/Zak phase of the occupied bands, reusing the
Wilson-loop machinery of :mod:`topology`.  The electronic polarization along z
is P_z = (e/2pi) <phi_Zak>(k_x,k_y) (averaged over the transverse BZ), where
phi_Zak is the Berry phase of the occupied manifold along the k_z string.

Sources (verified real & open-access, 2026-05-24):
* R. D. King-Smith, D. Vanderbilt, "Theory of polarization of crystalline
  solids", Phys. Rev. B 47, 1651 (1993), DOI 10.1103/PhysRevB.47.1651.
* W. P. Su, J. R. Schrieffer, A. J. Heeger, "Solitons in Polyacetylene", Phys.
  Rev. Lett. 42, 1698 (1979), DOI 10.1103/PhysRevLett.42.1698 (SSH test model;
  Zak phase quantized to 0/pi under inversion symmetry).

Symmetry / quantization: for a one-band-convention inversion-symmetric model
(SSH) the Zak phase is quantized to 0 or pi (mod 2pi), and the topological
*difference* is exactly pi -- this is the rigorous, validated content here.

Honesty (important): the quantity returned for the real perovskite is only the
*electronic* Berry phase in a fixed orbital gauge.  The physical, quantized
polarization in the modern theory (King-Smith-Vanderbilt) additionally requires
(i) the ionic point-charge contribution and (ii) the polarization quantum
(e R / V_cell); only the *total* is gauge-invariant and quantized for a
centrosymmetric crystal.  Empirically the bare electronic Zak phase of the cubic
perovskite is NOT 0/pi (it carries a gauge offset from the X_z orbital position
at z=a/2), so we do NOT assert its quantization -- the clean quantization is
demonstrated on SSH, and physical polarization *differences* (delta P, the
gauge-invariant observable) are the intended use.  Usual SK-TB/Blount caveats
apply to absolute magnitudes.
"""

from __future__ import annotations

import numpy as np

from . import models_kashikar as mk
from . import slab, topology


def zak_phase(occ_loop: np.ndarray) -> float:
    """Berry/Zak phase of an occupied manifold around a closed k-loop.

    occ_loop : (N, dim, n_occ) occupied eigenvectors along the loop (the loop
    closes by Hamiltonian periodicity).  Returns Im ln det(Wilson loop) in
    (-pi, pi].
    """
    return topology.polarization_phase(topology.wilson_loop(occ_loop))


def occupied_along_kz(params, a, kx, ky, n_occ, n_kz):
    """Occupied eigenvectors of the (gauge-fixed, 2pi/a-periodic) H along k_z."""
    z2 = slab._orbital_z(a)
    kzs = (2.0 * np.pi / a) * np.arange(n_kz) / n_kz
    occ = np.empty((n_kz, 26, n_occ), dtype=complex)
    for i, kz in enumerate(kzs):
        H = mk.kashikar13_hamiltonian(np.array([kx, ky, kz]), params, a)
        U = np.diag(np.exp(-1j * kz * z2))
        _, vecs = np.linalg.eigh(0.5 * (U @ H @ U.conj().T + (U @ H @ U.conj().T).conj().T))
        occ[i] = vecs[:, :n_occ]
    return occ


def polarization_phase_z(params, a, *, n_occ=slab.N_OCC_PER_CELL, n_kxy=6, n_kz=24):
    """Transverse-BZ-averaged Zak phase along z (the KSV electronic P_z, mod 2pi)."""
    kxy = (2.0 * np.pi / a) * np.arange(n_kxy) / n_kxy
    phis = []
    for kx in kxy:
        for ky in kxy:
            phis.append(zak_phase(occupied_along_kz(params, a, kx, ky, n_occ, n_kz)))
    # average on the unit circle (phase is mod 2pi)
    mean = np.angle(np.mean(np.exp(1j * np.array(phis))))
    return float(mean), np.array(phis)
