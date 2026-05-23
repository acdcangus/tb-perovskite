#!/usr/bin/env python3
"""Theme A / A4 -- g-factor scan over the 9 cubic CsBX3 perovskites.

Outputs (results/g_factors/):
  * g_factor_table.csv  -- per material: TB-computed Eg, Delta (Kashikar 13orb),
    k.p universal g_e/g_h at the TB gap, and (Pb only, where a repo-sourced
    realistic gap exists) the k.p g at the realistic gap.
  * kirstein_plot.png   -- universal g_e(Eg), g_h(Eg) curves with the realistic
    Pb anchors (Nestoklon Table S2) overlaid.
  * material_grid.png   -- 3x3 (B x X) heatmaps of TB Eg and Delta.

IMPORTANT (no hallucination):
  * The Kashikar parametrisation reproduces the mBJ+SOC DFT gaps, which are
    known to *underestimate* the experimental gaps (e.g. CsPbI3 ~0.6 eV vs
    experiment ~1.7 eV).  The k.p g-factor formula needs the *realistic* gap, so
    g-values computed at the small mBJ gaps are unphysically large and are
    reported only for completeness.
  * Realistic gaps are repo-sourced ONLY for the 3 Pb halides (Nestoklon
    arXiv:2012.14705 / Table S2).  Realistic CsGeX3 / CsSnX3 gaps are NOT in the
    repository -> flagged for Cowork (see progress/). Those rows are left blank
    in the realistic columns rather than guessed.
"""

from __future__ import annotations

import csv
import os

import numpy as np

from perovskite_tb import models_kashikar as mk
from perovskite_tb.g_factor import g_factor_kp
from perovskite_tb.io_params import get_material, load_parameter_file

OUTDIR = "results/g_factors"
K13 = "data/parameters/kashikar2021_cubic_13orb.json"
B_SITES = ["Ge", "Sn", "Pb"]
X_SITES = ["Cl", "Br", "I"]

# Repo-sourced realistic (experimental/DFT-combined) cubic gaps and CB SO
# splittings, in eV. Pb: Nestoklon arXiv:2012.14705 Table S2. Others: not in
# repository (None -> flagged for Cowork, NOT guessed).
REALISTIC = {
    "CsPbCl3": {"Eg": 3.090, "Delta": 1.526, "src": "Nestoklon Table S2"},
    "CsPbBr3": {"Eg": 2.352, "Delta": 1.436, "src": "Nestoklon Table S2"},
    "CsPbI3": {"Eg": 1.652, "Delta": 1.258, "src": "Nestoklon Table S2"},
}


def tb_gap_delta(params, a):
    """R-point gap Eg and CB spin-orbit splitting Delta from Kashikar 13orb."""
    nf = 20
    kR = np.array([np.pi / a] * 3)
    ev = np.sort(np.linalg.eigvalsh(mk.kashikar13_hamiltonian(kR, params, a)).real)
    return ev[nf] - ev[nf - 1], ev[nf + 2] - ev[nf]


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    data = load_parameter_file(K13)
    rows = []
    for B in B_SITES:
        for X in X_SITES:
            mat = f"Cs{B}{X}3"
            m = get_material(data, mat)
            Eg_tb, D_tb = tb_gap_delta(m["params"], m["a"])
            kp_tb = g_factor_kp(Eg_tb, D_tb)
            row = {
                "material": mat, "B": B, "X": X,
                "Eg_TB_mBJ": round(Eg_tb, 4), "Delta_TB": round(D_tb, 4),
                "g_e_kp_TB": round(kp_tb["g_e"], 3), "g_h_kp_TB": round(kp_tb["g_h"], 3),
                "Eg_realistic": "", "Delta_realistic": "",
                "g_e_kp_realistic": "", "g_h_kp_realistic": "", "realistic_src": "",
            }
            if mat in REALISTIC:
                r = REALISTIC[mat]
                kp_r = g_factor_kp(r["Eg"], r["Delta"])
                row.update({
                    "Eg_realistic": r["Eg"], "Delta_realistic": r["Delta"],
                    "g_e_kp_realistic": round(kp_r["g_e"], 3),
                    "g_h_kp_realistic": round(kp_r["g_h"], 3),
                    "realistic_src": r["src"],
                })
            rows.append(row)

    csv_path = os.path.join(OUTDIR, "g_factor_table.csv")
    with open(csv_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {csv_path}")

    _plot_kirstein(rows)
    _plot_grid(rows)
    return rows


def _plot_kirstein(rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    Eg = np.linspace(0.8, 3.6, 300)
    ge = [g_factor_kp(e, 1.5)["g_e"] for e in Eg]
    gh = [g_factor_kp(e, 1.5)["g_h"] for e in Eg]
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(Eg, ge, "C0-", label="$g_e$ universal (Kirstein, $\\Delta$=1.5)")
    ax.plot(Eg, gh, "C3-", label="$g_h$ universal")
    ax.axhline(-5 / 3, color="C0", ls=":", lw=0.8)
    ax.axhline(2.0, color="C3", ls=":", lw=0.8)
    # realistic Pb anchors
    for r in rows:
        if r["g_e_kp_realistic"] != "":
            ax.scatter(r["Eg_realistic"], r["g_e_kp_realistic"], c="C0", s=60, zorder=5,
                       edgecolor="k")
            ax.scatter(r["Eg_realistic"], r["g_h_kp_realistic"], c="C3", s=60, zorder=5,
                       edgecolor="k", marker="^")
            ax.annotate(r["material"], (r["Eg_realistic"], r["g_e_kp_realistic"]),
                        fontsize=8, xytext=(3, 4), textcoords="offset points")
    ax.set_xlabel("Band gap $E_g$ (eV)")
    ax.set_ylabel("Landé g-factor")
    ax.set_title("g-factor vs band gap: universal relation + Pb anchors (realistic $E_g$)")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    p = os.path.join(OUTDIR, "kirstein_plot.png")
    fig.savefig(p, dpi=150)
    plt.close(fig)
    print(f"wrote {p}")


def _plot_grid(rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    Eg = np.zeros((3, 3)); D = np.zeros((3, 3))
    for r in rows:
        i = B_SITES.index(r["B"]); j = X_SITES.index(r["X"])
        Eg[i, j] = r["Eg_TB_mBJ"]; D[i, j] = r["Delta_TB"]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for ax, M, title in [(axes[0], Eg, "TB $E_g$ (mBJ+SOC, eV)"),
                         (axes[1], D, "TB CB SO splitting $\\Delta$ (eV)")]:
        im = ax.imshow(M, cmap="viridis", origin="upper")
        ax.set_xticks(range(3)); ax.set_xticklabels(X_SITES)
        ax.set_yticks(range(3)); ax.set_yticklabels(B_SITES)
        for i in range(3):
            for j in range(3):
                ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center",
                        color="w", fontsize=10)
        ax.set_title(title)
        fig.colorbar(im, ax=ax, fraction=0.046)
    fig.suptitle("Kashikar 13-orbital CsBX$_3$ (B rows: Ge/Sn/Pb, X cols: Cl/Br/I)")
    fig.tight_layout()
    p = os.path.join(OUTDIR, "material_grid.png")
    fig.savefig(p, dpi=150)
    plt.close(fig)
    print(f"wrote {p}")


if __name__ == "__main__":
    main()
