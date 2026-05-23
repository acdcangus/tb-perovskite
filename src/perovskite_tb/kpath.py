"""High-symmetry k-paths for the simple-cubic Brillouin zone.

High-symmetry points (reduced coordinates, in units of the reciprocal lattice
vectors b_i = 2*pi/a):
    Gamma (G) = (0,   0,   0  )
    X         = (1/2, 0,   0  )
    M         = (1/2, 1/2, 0  )
    R         = (1/2, 1/2, 1/2)

Cartesian wavevector = reduced * (2*pi/a) for each component.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

# Reduced coordinates of the simple-cubic high-symmetry points.
HIGH_SYMMETRY = {
    "G": (0.0, 0.0, 0.0),
    "Gamma": (0.0, 0.0, 0.0),
    "X": (0.5, 0.0, 0.0),
    "M": (0.5, 0.5, 0.0),
    "R": (0.5, 0.5, 0.5),
}

# Pretty labels for plotting.
LABELS = {"G": r"$\Gamma$", "Gamma": r"$\Gamma$", "X": "X", "M": "M", "R": "R"}


@dataclass
class KPath:
    """A sampled path through the Brillouin zone."""

    kpoints_cart: np.ndarray  # (nk, 3) cartesian wavevectors [1/length]
    distances: np.ndarray  # (nk,) cumulative path length for plotting
    tick_positions: list  # distances of the high-symmetry nodes
    tick_labels: list = field(default_factory=list)


def reduced_to_cartesian(reduced, a: float) -> np.ndarray:
    """Convert reduced coordinates to cartesian wavevector (cubic lattice)."""
    return np.asarray(reduced, dtype=float) * (2.0 * np.pi / a)


def make_kpath(segments, a: float, n_per_segment: int = 100) -> KPath:
    """Build a sampled k-path.

    Parameters
    ----------
    segments : list[str]
        Sequence of high-symmetry point labels, e.g. ["M","R","G","X","M","G"].
    a : float
        Cubic lattice constant (sets cartesian scaling).
    n_per_segment : int
        Number of samples per segment (endpoints shared between segments).
    """
    pts = [HIGH_SYMMETRY[s] for s in segments]
    cart = [reduced_to_cartesian(p, a) for p in pts]

    kpoints = []
    distances = []
    ticks = []
    d_acc = 0.0
    for i in range(len(cart) - 1):
        k0, k1 = cart[i], cart[i + 1]
        seg_len = float(np.linalg.norm(k1 - k0))
        ticks.append(d_acc)
        ts = np.linspace(0.0, 1.0, n_per_segment, endpoint=(i == len(cart) - 2))
        for t in ts:
            kpoints.append(k0 + t * (k1 - k0))
            distances.append(d_acc + t * seg_len)
        d_acc += seg_len
    ticks.append(d_acc)

    labels = [LABELS.get(s, s) for s in segments]
    return KPath(
        kpoints_cart=np.array(kpoints),
        distances=np.array(distances),
        tick_positions=ticks,
        tick_labels=labels,
    )
