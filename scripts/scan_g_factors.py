#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 tk
"""Theme A / A4 -- k.p g-factor scan over the 9 cubic CsBX3 perovskites.

Method (Cowork directive v2 sec.2): apply the Kirstein 2021 universal k.p
relation (arXiv:2112.15384 Eqs.5,6) to literature band gaps Eg and SO
splittings Delta (data/parameters/experimental_band_data.json).

Two evaluations per material:
  (i)  universal Delta = 1.5 eV  -> "does the Pb-based universal curve hold?"
  (ii) material-specific Delta   -> "how does weaker Sn/Ge SOC shift g?"

Physics note: g_e depends only on Eg (Eq.6), so every material lies on a single
universal g_e(Eg) curve (given universal P). g_h depends on Eg AND Delta (Eq.5),
so the smaller Sn/Ge conduction-band SO splitting makes their hole g-factor
deviate from the Pb-based universal curve -- the central lead-free result.

Outputs (results/g_factors/):
  g_factor_9material.csv, kirstein_universal_plot.png, material_grid.png
"""

from __future__ import annotations

import csv
import json
import os

import numpy as np

from perovskite_tb.g_factor import g_factor_kp

OUTDIR = "results/g_factors"
DATA = "data/parameters/experimental_band_data.json"
B_SITES = ["Ge", "Sn", "Pb"]
X_SITES = ["Cl", "Br", "I"]
P_UNIVERSAL = 6.8
DGE_UNIVERSAL = -1.0
DELTA_UNIVERSAL = 1.5


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    with open(DATA) as fh:
        data = json.load(fh)
    mats = data["materials"]
    du = data.get("delta_uncertainty_frac", 0.20)

    rows = []
    for B in B_SITES:
        for X in X_SITES:
            mat = f"Cs{B}{X}3"
            Eg = mats[mat]["Eg"]
            Delta = mats[mat]["Delta"]
            # g_e depends on Eg only; g_h on (Eg, Delta).
            uni = g_factor_kp(Eg, DELTA_UNIVERSAL, P_UNIVERSAL, DGE_UNIVERSAL)
            msp = g_factor_kp(Eg, Delta, P_UNIVERSAL, DGE_UNIVERSAL)
            # Delta uncertainty -> g_h range (Sn/Ge only carry the +/-20%; Pb literature).
            frac = du if mats[mat]["Delta_method"] == "kashikar_3lambda" else 0.05
            gh_lo = g_factor_kp(Eg, Delta * (1 - frac), P_UNIVERSAL, DGE_UNIVERSAL)["g_h"]
            gh_hi = g_factor_kp(Eg, Delta * (1 + frac), P_UNIVERSAL, DGE_UNIVERSAL)["g_h"]
            rows.append({
                "material": mat, "B": B, "X": X, "Eg": Eg, "Delta": Delta,
                "g_e": round(msp["g_e"], 3),
                "g_h_universalDelta": round(uni["g_h"], 3),
                "g_h_materialDelta": round(msp["g_h"], 3),
                "g_h_deviation": round(msp["g_h"] - uni["g_h"], 3),
                "g_h_lo": round(min(gh_lo, gh_hi), 3),
                "g_h_hi": round(max(gh_lo, gh_hi), 3),
                "Delta_method": mats[mat]["Delta_method"],
            })

    csv_path = os.path.join(OUTDIR, "g_factor_9material.csv")
    with open(csv_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {csv_path}")
    for r in rows:
        print(f"  {r['material']:9s} Eg={r['Eg']:.2f} D={r['Delta']:.2f}  "
              f"g_e={r['g_e']:+.2f}  g_h(uniD)={r['g_h_universalDelta']:+.2f}  "
              f"g_h(matD)={r['g_h_materialDelta']:+.2f}  dev={r['g_h_deviation']:+.2f}")

    _plot(rows)
    _plot_grid(rows)
    return rows


def _plot(rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    Egc = np.linspace(1.2, 3.6, 300)
    ge_curve = [g_factor_kp(e, DELTA_UNIVERSAL, P_UNIVERSAL, DGE_UNIVERSAL)["g_e"] for e in Egc]
    gh_curve = [g_factor_kp(e, DELTA_UNIVERSAL, P_UNIVERSAL, DGE_UNIVERSAL)["g_h"] for e in Egc]
    color = {"Ge": "C2", "Sn": "C1", "Pb": "C0"}
    marker = {"Cl": "o", "Br": "s", "I": "^"}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))
    # electron g
    ax1.plot(Egc, ge_curve, "k-", lw=1.2, label="universal $g_e(E_g)$ (Kirstein)")
    ax1.axhline(-5 / 3, color="grey", ls=":", lw=0.8)
    for r in rows:
        ax1.scatter(r["Eg"], r["g_e"], c=color[r["B"]], marker=marker[r["X"]],
                    s=70, edgecolor="k", zorder=5)
    ax1.set_xlabel("$E_g$ (eV)"); ax1.set_ylabel("$g_e$")
    ax1.set_title("Electron g-factor (depends on $E_g$ only)\nall 9 materials on one curve")
    ax1.grid(alpha=0.3)

    # hole g
    ax2.plot(Egc, gh_curve, "k-", lw=1.2, label="Pb-based universal $g_h$ ($\\Delta$=1.5)")
    ax2.axhline(2.0, color="grey", ls=":", lw=0.8)
    for r in rows:
        yerr = [[r["g_h_materialDelta"] - r["g_h_lo"]], [r["g_h_hi"] - r["g_h_materialDelta"]]]
        ax2.errorbar(r["Eg"], r["g_h_materialDelta"], yerr=yerr, fmt=marker[r["X"]],
                     color=color[r["B"]], ms=8, mec="k", capsize=3, zorder=5)
    ax2.set_xlabel("$E_g$ (eV)"); ax2.set_ylabel("$g_h$")
    ax2.set_title("Hole g-factor (depends on $E_g$ and $\\Delta$)\nSn/Ge deviate from Pb curve (weaker SOC)")
    ax2.grid(alpha=0.3)

    # shared legend for B/X
    from matplotlib.lines import Line2D
    handles = [Line2D([0], [0], marker="o", color="w", markerfacecolor=color[b],
                      markeredgecolor="k", markersize=9, label=b) for b in B_SITES]
    handles += [Line2D([0], [0], marker=marker[x], color="w", markerfacecolor="grey",
                       markeredgecolor="k", markersize=9, label=x) for x in X_SITES]
    ax2.legend(handles=handles, fontsize=8, ncol=2, title="B / X")
    ax1.legend(fontsize=8)
    fig.suptitle("k·p universal g-factors of cubic CsBX$_3$ (Kirstein 2021 relation, literature $E_g$)")
    fig.tight_layout()
    p = os.path.join(OUTDIR, "kirstein_universal_plot.png")
    fig.savefig(p, dpi=150); plt.close(fig)
    print(f"wrote {p}")


def _plot_grid(rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    R = {r["material"]: r for r in rows}
    GE = np.zeros((3, 3)); GH = np.zeros((3, 3))
    for i, B in enumerate(B_SITES):
        for j, X in enumerate(X_SITES):
            r = R[f"Cs{B}{X}3"]; GE[i, j] = r["g_e"]; GH[i, j] = r["g_h_materialDelta"]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for ax, M, title, cmap in [(axes[0], GE, "$g_e$", "viridis"),
                              (axes[1], GH, "$g_h$ (material $\\Delta$)", "coolwarm")]:
        im = ax.imshow(M, cmap=cmap, origin="upper")
        ax.set_xticks(range(3)); ax.set_xticklabels(X_SITES)
        ax.set_yticks(range(3)); ax.set_yticklabels(B_SITES)
        for i in range(3):
            for j in range(3):
                ax.text(j, i, f"{M[i, j]:+.2f}", ha="center", va="center",
                        color="k", fontsize=11)
        ax.set_title(title); fig.colorbar(im, ax=ax, fraction=0.046)
    fig.suptitle("Predicted g-factors, CsBX$_3$ (rows Ge/Sn/Pb, cols Cl/Br/I)")
    fig.tight_layout()
    p = os.path.join(OUTDIR, "material_grid.png")
    fig.savefig(p, dpi=150); plt.close(fig)
    print(f"wrote {p}")


if __name__ == "__main__":
    main()
