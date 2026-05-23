"""Band-structure computation: diagonalize a Bloch Hamiltonian along a k-path.

Numerical-methods notes (see docs/numerical-methods.md):
    * Eigenvalues of the Hermitian Bloch Hamiltonian are obtained with
      ``numpy.linalg.eigvalsh`` (and ``eigh`` when eigenvectors are needed),
      which uses a backward-stable LAPACK divide-and-conquer routine.
    * All comparisons of floating-point energies use absolute tolerances
      (never ``==``); see tests.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from .kpath import KPath


@dataclass
class BandStructure:
    distances: np.ndarray  # (nk,)
    energies: np.ndarray  # (nk, nbands) sorted ascending per k
    kpath: KPath
    n_filled: int

    @property
    def n_bands(self) -> int:
        return self.energies.shape[1]


def eigenvalues_at_k(builder: Callable[[np.ndarray], np.ndarray],
                     kvec: np.ndarray) -> np.ndarray:
    """Return sorted (ascending) eigenvalues of the Hamiltonian at ``kvec``."""
    H = builder(np.asarray(kvec, dtype=float))
    # Enforce Hermiticity numerically before diagonalizing.
    H = 0.5 * (H + H.conj().T)
    return np.linalg.eigvalsh(H)


def compute_band_structure(builder: Callable[[np.ndarray], np.ndarray],
                           kpath: KPath, n_filled: int) -> BandStructure:
    """Diagonalize along a k-path and return a :class:`BandStructure`."""
    energies = np.array([eigenvalues_at_k(builder, k) for k in kpath.kpoints_cart])
    return BandStructure(distances=kpath.distances, energies=energies,
                         kpath=kpath, n_filled=n_filled)


def direct_gap(builder: Callable[[np.ndarray], np.ndarray], kvec: np.ndarray,
               n_filled: int) -> float:
    """Direct gap at a single k-point: E[n_filled] - E[n_filled-1]."""
    ev = eigenvalues_at_k(builder, kvec)
    return float(ev[n_filled] - ev[n_filled - 1])


def fundamental_gap(bs: BandStructure) -> dict:
    """Find the fundamental (possibly indirect) gap from a sampled band structure.

    Returns a dict with VBM, CBM (energies), the gap, and the path distances at
    which they occur.  Note: this is limited to the sampled k-points; for a
    direct gap at a known point use :func:`direct_gap`.
    """
    nf = bs.n_filled
    vb = bs.energies[:, nf - 1]
    cb = bs.energies[:, nf]
    i_vbm = int(np.argmax(vb))
    i_cbm = int(np.argmin(cb))
    vbm = float(vb[i_vbm])
    cbm = float(cb[i_cbm])
    return {
        "vbm": vbm,
        "cbm": cbm,
        "gap": cbm - vbm,
        "vbm_distance": float(bs.distances[i_vbm]),
        "cbm_distance": float(bs.distances[i_cbm]),
        "direct": i_vbm == i_cbm,
    }
