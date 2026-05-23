#!/usr/bin/env python3
"""Theme A Fig.2 (polish c) -- hole g-factor deviation vs conduction-band SOC Delta.

Visualises the central lead-free result: g_h deviates from the Pb-based universal
curve because Sn/Ge have a much smaller conduction-band spin-orbit splitting Delta.
We plot the deviation  dg_h = g_h(material Delta) - g_h(universal Delta=1.5)  vs
Delta, with +/-20% Delta uncertainty bands for Sn/Ge (Kashikar 3*lambda estimate).

Sources: g_h from Kirstein 2021 Eq.(5) (g_factor.g_factor_kp); Eg/Delta from
data/parameters/experimental_band_data.json. Output: results/g_factors/gh_delta_dependence.png
"""

from __future__ import annotations

import json
import os

import numpy as np

from perovskite_tb.g_factor import g_factor_kp

OUTDIR = "results/g_factors"
DELTA_UNIVERSAL = 1.5
B_COLOR = {"Ge": "C2", "Sn": "C1", "Pb": "C0"}
B_MARK = {"Ge": "^", "Sn": "s", "Pb": "o"}


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    with open("data/parameters/experimental_band_data.json") as fh:
        data = json.load(fh)["materials"]

    fig, ax = plt.subplots(figsize=(7.5, 5))
    for mat, d in data.items():
        B = mat[2:4]
        Eg, Delta = d["Eg"], d["Delta"]
        dgh = (g_factor_kp(Eg, Delta)["g_h"]
               - g_factor_kp(Eg, DELTA_UNIVERSAL)["g_h"])
        # +/-20% Delta band for Kashikar-3lambda (Sn/Ge); ~0 for Pb (literature).
        frac = 0.20 if d.get("Delta_method") == "kashikar_3lambda" else 0.0
        if frac:
            d_lo = (g_factor_kp(Eg, Delta * (1 - frac))["g_h"]
                    - g_factor_kp(Eg, DELTA_UNIVERSAL)["g_h"])
            d_hi = (g_factor_kp(Eg, Delta * (1 + frac))["g_h"]
                    - g_factor_kp(Eg, DELTA_UNIVERSAL)["g_h"])
            xerr = [[Delta - Delta * (1 - frac)], [Delta * (1 + frac) - Delta]]
            yerr = [[abs(dgh - min(d_lo, d_hi))], [abs(max(d_lo, d_hi) - dgh)]]
            ax.errorbar(Delta, dgh, xerr=xerr, yerr=yerr, fmt=B_MARK[B],
                        color=B_COLOR[B], ms=9, mec="k", capsize=3, zorder=5)
        else:
            ax.scatter(Delta, dgh, marker=B_MARK[B], color=B_COLOR[B], s=90,
                       edgecolor="k", zorder=6)
        ax.annotate(mat, (Delta, dgh), fontsize=7, xytext=(4, 4),
                    textcoords="offset points")

    ax.axhline(0.0, color="grey", ls="--", lw=1.0, label="Pb-based universal ($\\Delta$=1.5)")
    ax.axvline(DELTA_UNIVERSAL, color="grey", ls=":", lw=0.8)
    ax.set_xlabel(r"Conduction-band SO splitting $\Delta$ (eV)")
    ax.set_ylabel(r"$\Delta g_h = g_h(\Delta_{\rm mat}) - g_h(\Delta{=}1.5)$")
    ax.set_title("Hole g-factor deviation grows as the (lead-free) SOC $\\Delta$ shrinks\n"
                 "(Ge $\\Delta$≈0.21, Sn ≈0.45, Pb ≈1.3-1.5 eV)")
    from matplotlib.lines import Line2D
    handles = [Line2D([0], [0], marker=B_MARK[b], color="w", markerfacecolor=B_COLOR[b],
                      markeredgecolor="k", markersize=9, label=b) for b in B_COLOR]
    handles.append(Line2D([0], [0], color="grey", ls="--", label="universal (no deviation)"))
    ax.legend(handles=handles, fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    path = os.path.join(OUTDIR, "gh_delta_dependence.png")
    fig.savefig(path, dpi=150); plt.close(fig)
    print(f"wrote {path}")
    # also print the values
    for mat, d in data.items():
        dgh = g_factor_kp(d["Eg"], d["Delta"])["g_h"] - g_factor_kp(d["Eg"], 1.5)["g_h"]
        print(f"  {mat:9s} Delta={d['Delta']:.2f}  dg_h={dgh:+.2f}")


if __name__ == "__main__":
    main()
