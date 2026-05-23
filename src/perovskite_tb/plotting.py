"""Band-structure plotting (matplotlib, non-interactive Agg backend)."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from .bandstructure import BandStructure  # noqa: E402


def plot_band_structure(bs: BandStructure, title: str = "", ax=None,
                        shift_to_vbm: bool = True, gap_info: dict | None = None):
    """Plot a band structure. Returns the matplotlib Axes."""
    if ax is None:
        _fig, ax = plt.subplots(figsize=(6, 5))

    energies = bs.energies.copy()
    ylabel = "Energy (eV)"
    if shift_to_vbm:
        vbm = float(energies[:, bs.n_filled - 1].max())
        energies = energies - vbm
        ylabel = "Energy − E$_{VBM}$ (eV)"

    for b in range(bs.n_bands):
        color = "tab:blue" if b < bs.n_filled else "tab:red"
        ax.plot(bs.distances, energies[:, b], color=color, lw=1.0)

    # High-symmetry node guide lines and labels.
    for x in bs.kpath.tick_positions:
        ax.axvline(x, color="k", lw=0.5, alpha=0.4)
    ax.set_xticks(bs.kpath.tick_positions)
    ax.set_xticklabels(bs.kpath.tick_labels)
    ax.set_xlim(bs.distances[0], bs.distances[-1])
    ax.axhline(0.0 if shift_to_vbm else None, color="grey", lw=0.5, ls="--")

    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    if gap_info is not None:
        txt = f"gap = {gap_info['gap']:.3f} eV ({'direct' if gap_info['direct'] else 'indirect'})"
        ax.text(0.02, 0.02, txt, transform=ax.transAxes, fontsize=9,
                va="bottom", ha="left",
                bbox=dict(boxstyle="round", fc="white", alpha=0.7))
    return ax


def save_band_structure(bs: BandStructure, path: str | Path, title: str = "",
                        gap_info: dict | None = None, **kwargs):
    """Plot and save a band structure to ``path``."""
    ax = plot_band_structure(bs, title=title, gap_info=gap_info, **kwargs)
    fig = ax.get_figure()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path
