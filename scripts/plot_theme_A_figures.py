#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 tk
"""Theme A publication figures (Priority 4 #2): Lande g-factor universality.

Reads the Production g-factor table and renders publication-quality PDFs:
  Fig 1: g_e and g_h vs band gap E_g, 9 materials, with the Kirstein 2021 k.p
         universal curves overlaid -> g_e "apparent universality" vs the g_h
         lead-free (Sn/Ge) UPWARD deviation (the main Theme A finding).
  Fig 2: g_h deviation (material-Delta minus universal-Delta) vs SOC Delta,
         showing the deviation grows as Delta -> 0 (Sn/Ge), ~0 for Pb.

Data: results/production/theme_A_g_factor/<...>/outputs/raw/g_factor_9material.csv
(numbers are quoted from the Production bundle; no hand-entered values).
"""
import csv
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV = ("results/production/theme_A_g_factor/2026-05-23_31374dc/"
       "outputs/raw/g_factor_9material.csv")
OUTDIR = "results/g_factors/figures"
COL = {"Ge": "#1b9e77", "Sn": "#7570b3", "Pb": "#d95f02"}   # colourblind-safe
MARK = {"Cl": "o", "Br": "s", "I": "^"}

# Kirstein 2021 k.p universal constants (see docs/g-factor-formulation.md)
P, C, DG_E, DELTA_KP = 6.8, 7.619964, -1.0, 1.5   # eV.Ang, eV.Ang^2, -, eV


def g_e_universal(Eg):
    return -2.0 / 3.0 + (4.0 / 3.0) * P ** 2 / (C * Eg) + DG_E


def g_h_universal(Eg, Delta=DELTA_KP):
    return 2.0 - (4.0 / 3.0) * (P ** 2 / C) * (1.0 / Eg - 1.0 / (Eg + Delta))


def load():
    with open(CSV) as fh:
        return list(csv.DictReader(fh))


def fig1(rows):
    fig, (axe, axh) = plt.subplots(1, 2, figsize=(11, 4.4))
    Eg_curve = np.linspace(1.2, 3.6, 200)
    axe.plot(Eg_curve, [g_e_universal(e) for e in Eg_curve], "k--", lw=1,
             label="k·p universal (P=6.8)")
    axh.plot(Eg_curve, [g_h_universal(e) for e in Eg_curve], "k--", lw=1,
             label="k·p universal (Δ=1.5 eV)")
    for r in rows:
        B, X, Eg = r["B"], r["X"], float(r["Eg"])
        axe.scatter(Eg, float(r["g_e"]), c=COL[B], marker=MARK[X], s=70,
                    edgecolor="k", lw=0.4)
        axh.scatter(Eg, float(r["g_h_materialDelta"]), c=COL[B], marker=MARK[X], s=70,
                    edgecolor="k", lw=0.4)
    axe.set_xlabel("band gap $E_g$ (eV)"); axe.set_ylabel("electron $g_e$")
    axe.set_title("(a) $g_e$: apparent universality"); axe.legend(fontsize=8)
    axh.set_xlabel("band gap $E_g$ (eV)"); axh.set_ylabel("hole $g_h$")
    axh.set_title("(b) $g_h$: lead-free (Sn/Ge) deviate upward"); axh.legend(fontsize=8)
    # legend for B-cation colours
    handles = [plt.Line2D([], [], marker="o", ls="", color=COL[b], label=b,
                          mec="k") for b in ("Ge", "Sn", "Pb")]
    axh.add_artist(axh.legend(handles=handles, title="B", fontsize=8, loc="lower right"))
    fig.tight_layout()
    fig.savefig(f"{OUTDIR}/fig1_g_factor_universality.pdf"); plt.close(fig)


def fig2(rows):
    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    for r in rows:
        ax.scatter(float(r["Delta"]), float(r["g_h_deviation"]), c=COL[r["B"]],
                   marker=MARK[r["X"]], s=80, edgecolor="k", lw=0.4)
        ax.annotate(r["material"].replace("Cs", ""), (float(r["Delta"]), float(r["g_h_deviation"])),
                    fontsize=6, xytext=(4, 2), textcoords="offset points")
    ax.axhline(0, color="grey", lw=0.6)
    ax.set_xlabel("spin-orbit splitting $\\Delta$ (eV)")
    ax.set_ylabel("$g_h$ deviation (material $\\Delta$ $-$ universal)")
    ax.set_title("Fig 2: $g_h$ universal-relation breakdown grows as $\\Delta\\to0$")
    handles = [plt.Line2D([], [], marker="o", ls="", color=COL[b], label=b, mec="k")
               for b in ("Ge", "Sn", "Pb")]
    ax.legend(handles=handles, title="B", fontsize=8)
    fig.tight_layout()
    fig.savefig(f"{OUTDIR}/fig2_gh_deviation_vs_delta.pdf"); plt.close(fig)


if __name__ == "__main__":
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
    os.makedirs(OUTDIR, exist_ok=True)
    rows = load()
    fig1(rows)
    fig2(rows)
    print(f"wrote {OUTDIR}/fig1_g_factor_universality.pdf, fig2_gh_deviation_vs_delta.pdf "
          f"({len(rows)} materials)")
