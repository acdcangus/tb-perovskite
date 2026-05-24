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

from ._constants import HBAR2_OVER_M0
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


_PRINCIPAL_DIRS = {
    "100": np.array([1.0, 0.0, 0.0]),
    "110": np.array([1.0, 1.0, 0.0]),
    "111": np.array([1.0, 1.0, 1.0]),
}


def effective_mass(builder: Callable[[np.ndarray], np.ndarray], k0, band: int,
                   *, directions=None, dk: float = 1e-3, npts: int = 7) -> dict:
    r"""Band-edge effective mass m*/m0 from a parabolic fit of E(k) around ``k0``.

    Fits :math:`E(k_0 + t\,\hat d) = E_0 + \tfrac12 (d^2E/dk^2)\, t^2` along each
    unit direction :math:`\hat d` and returns the curvature mass
    :math:`m^*/m_0 = (\hbar^2/m_0) / (d^2E/dk^2)` with
    :math:`\hbar^2/m_0 = 7.62\ \mathrm{eV\,\AA^2}` (``HBAR2_OVER_M0``).

    The returned mass is SIGNED: positive at a conduction-band minimum, negative
    at a valence-band maximum (the hole mass is its magnitude).  ``band`` is the
    index into the ascending eigenvalue list at ``k0`` (e.g. CBM = n_filled,
    VBM = n_filled - 1).  ``k0`` must be in the same (Cartesian, 1/Angstrom)
    units as the builder expects, so curvatures come out in eV*Angstrom^2.

    Parameters
    ----------
    directions : mapping label -> 3-vector, or None for the cubic principal set
        {100, 110, 111}.  Vectors are normalised internally.
    dk, npts : finite-difference step (1/Angstrom) and number of sample points
        (odd; symmetric about k0).

    Returns dict: ``{label: m_rel}`` plus ``"mean"`` (signed average over
    directions) and ``"curvatures"`` (the fitted d^2E/dk^2 per direction).
    """
    k0 = np.asarray(k0, dtype=float)
    dirs = _PRINCIPAL_DIRS if directions is None else {
        k: np.asarray(v, float) for k, v in directions.items()}
    ts = (np.arange(npts) - npts // 2) * dk
    out, curv = {}, {}
    for lab, d in dirs.items():
        dhat = d / np.linalg.norm(d)
        e = np.array([eigenvalues_at_k(builder, k0 + t * dhat)[band] for t in ts])
        c2 = np.polyfit(ts, e, 2)[0] * 2.0  # d^2E/dk^2 (eV*Angstrom^2)
        curv[lab] = float(c2)
        out[lab] = float(HBAR2_OVER_M0 / c2) if abs(c2) > 1e-12 else float("inf")
    out["mean"] = float(np.mean([out[l] for l in dirs]))
    out["curvatures"] = curv
    return out


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
