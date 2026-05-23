#!/usr/bin/env python3
"""Theme A / A7 -- is g_e universality real or apparent?

Plots g_e vs 1/Eg for the 9 CsBX3:
  * black line: universal-P (6.8 eV.A) k.p prediction (Kirstein) -- linear in 1/Eg;
  * coloured points: g_e from TB-derived material-specific P (kane_parameters.csv);
  * Pb anchors: g_e from Nestoklon Table S2.

Also reports the 'inverse' Kane parameter that reproduces each Pb Table-S2 g_e,
showing it is ~constant (6.8) while the TB-derived P underestimates and varies.
Output: results/g_factors/ge_universality.png and a short stdout summary.
"""

from __future__ import annotations

import csv
import json
import os

import numpy as np

from perovskite_tb.g_factor import C_HBAR2_OVER_M0 as C
from perovskite_tb.g_factor import g_factor_kp

OUTDIR = "results/g_factors"
DGE = -1.0
B_COLOR = {"Ge": "C2", "Sn": "C1", "Pb": "C0"}
TABLE_S2_GE = {"CsPbCl3": 0.95, "CsPbBr3": 1.77, "CsPbI3": 3.23}
TABLE_S2_EG = {"CsPbCl3": 3.090, "CsPbBr3": 2.352, "CsPbI3": 1.652}


def _inverse_P(g_e, Eg, dge=DGE):
    """Kane P (eV.A) reproducing a given g_e at band gap Eg."""
    return float(np.sqrt((g_e + 2.0 / 3.0 - dge) * C * Eg / (4.0 / 3.0)))


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    with open("data/parameters/experimental_band_data.json") as fh:
        eg = {k: v["Eg"] for k, v in json.load(fh)["materials"].items()}
    P_tb = {}
    with open(os.path.join(OUTDIR, "kane_parameters.csv")) as fh:
        for r in csv.DictReader(fh):
            if r["model"] == "kashikar13":
                P_tb[r["material"]] = float(r["P_bare_eVA"])

    print("Inverse Kane P from Pb Table-S2 g_e (should be ~constant if universality real):")
    for mat in ("CsPbCl3", "CsPbBr3", "CsPbI3"):
        Pinv = _inverse_P(TABLE_S2_GE[mat], TABLE_S2_EG[mat])
        print(f"  {mat}: g_e={TABLE_S2_GE[mat]:+.2f} Eg={TABLE_S2_EG[mat]} -> P_inv={Pinv:.2f} "
              f"(TB-derived {P_tb[mat]:.2f}, universal 6.8)")

    from matplotlib.lines import Line2D
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(7.5, 8.5))

    # --- Top panel: g_e vs 1/Eg ---
    invEg = np.linspace(0.28, 0.65, 100)
    ge_uni = [-2 / 3 + (4 / 3) * 6.8 ** 2 / C * x + DGE for x in invEg]
    ax.plot(invEg, ge_uni, "k-", lw=1.4, label="universal P=6.8 (Kirstein)")
    for mat, Eg in eg.items():
        B = mat[2:4]
        ge_mat = g_factor_kp(Eg, 1.5, P=P_tb[mat])["g_e"]
        ax.scatter(1 / Eg, ge_mat, c=B_COLOR[B], marker="o", s=70, edgecolor="k", zorder=5)
    for mat in TABLE_S2_GE:
        ax.scatter(1 / TABLE_S2_EG[mat], TABLE_S2_GE[mat], facecolor="none",
                   edgecolor="k", marker="s", s=130, zorder=6)
    handles = [Line2D([0], [0], color="k", lw=1.4, label="universal P=6.8")]
    handles += [Line2D([0], [0], marker="o", color="w", markerfacecolor=B_COLOR[b],
                       markeredgecolor="k", markersize=9, label=f"{b} (TB-P)") for b in B_COLOR]
    handles += [Line2D([0], [0], marker="s", color="w", markeredgecolor="k",
                       markersize=10, label="Pb Table-S2 $g_e$")]
    ax.legend(handles=handles, fontsize=8)
    ax.set_xlabel(r"$1/E_g$ (eV$^{-1}$)"); ax.set_ylabel(r"$g_e$")
    ax.set_title("(a) $g_e$: universal-P line vs TB-derived material-specific P")
    ax.grid(alpha=0.3)

    # --- Bottom panel: Kane P vs material ---
    mats = list(eg.keys())
    x = np.arange(len(mats))
    ax2.axhline(6.8, color="grey", ls="--", lw=1.2, label="universal P = 6.8 (Kirstein)")
    ax2.bar(x, [P_tb[m] for m in mats], color=[B_COLOR[m[2:4]] for m in mats],
            edgecolor="k", alpha=0.85, label="TB-derived P (Kashikar 13)")
    for mat in TABLE_S2_GE:  # inverse-P (Pb only) ~ 6.80 constant
        i = mats.index(mat)
        Pinv = _inverse_P(TABLE_S2_GE[mat], TABLE_S2_EG[mat])
        ax2.scatter(i, Pinv, facecolor="none", edgecolor="k", marker="s", s=120, zorder=6)
    ax2.set_xticks(x); ax2.set_xticklabels(mats, rotation=45, ha="right", fontsize=8)
    ax2.set_ylabel("Kane P (eV·Å)")
    ax2.set_title("(b) TB-derived P underestimates universal 6.8; "
                  "Pb inverse-P (□) ≈ 6.80 constant")
    ax2.legend(fontsize=8, loc="lower right"); ax2.grid(alpha=0.3, axis="y")
    ax2.set_ylim(0, 7.5)

    fig.tight_layout()
    path = os.path.join(OUTDIR, "ge_universality.png")
    fig.savefig(path, dpi=150); plt.close(fig)
    print(f"wrote {path} (2-panel)")


if __name__ == "__main__":
    main()
