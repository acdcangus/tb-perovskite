#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 tk
"""Theme I (Y1-c-3): Wannier-Mott exciton binding energy E_b for cubic CsBX3.

Hybrid: the reduced mass mu is TB-derived (R-point band curvature, same as Y1-a /
scan_theme_I_effective_mass.py), while eps_inf is EXTERNALLY sourced from literature
(data/parameters/eps_inf_external.json) to bypass the Blount-1962 systematic
underestimate of the TB-optical f-sum (~0.21).  This separates the error sources:
mu = TB, eps_inf = external citation.

E_b = (mu/m0) / eps_inf^2 * Ry  (upper-bound screening; physical screening lies
between eps_inf and eps_static via the phonon contribution -- Tanaka 2003 / Yang 2017).

Only materials with a usable (non-null, non-pending) eps_inf in the JSON are included
(partial production OK per directive supplement 2026-05-24_0735); the rest await
Cowork's Claude-in-Chrome search.  Re-run automatically picks up newly-filled values.

Usage:  python scripts/scan_theme_I_binding_energy.py production
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from perovskite_tb import exciton as ex                              # noqa: E402
from perovskite_tb import models_kashikar as mk                      # noqa: E402
from perovskite_tb.io_params import get_material, load_parameter_file  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parents[1]
KAS13 = "data/parameters/kashikar2021_cubic_13orb.json"
EPS_JSON = "data/parameters/eps_inf_external.json"
N_OCC = 20
# statuses whose eps_inf value is usable for production (non-null, cited)
_USABLE = {"found", "proxy_lead_iodide_effective", "experimental", "dft_rpa", "cited"}


def _mu(mat, dk=1e-3):
    m = get_material(load_parameter_file(KAS13), mat)
    p, a = m["params"], m["a"]
    H = lambda k, p=p, a=a: mk.kashikar13_hamiltonian(k, p, a)        # noqa: E731
    me = ex.effective_mass(H, a, N_OCC, dk=dk)
    mh = ex.effective_mass(H, a, N_OCC - 1, dk=dk)
    return ex.reduced_mass(me, mh)


def compute(outdir):
    os.makedirs(outdir, exist_ok=True)
    eps_db = json.load(open(EPS_JSON))["materials"]
    rows, skipped = [], []
    for mat, rec in eps_db.items():
        eps = rec.get("eps_inf")
        status = rec.get("status", "")
        if eps is None or (status not in _USABLE):
            skipped.append((mat, status))
            continue
        mu = _mu(mat)
        Eb = ex.wannier_mott_binding_eV(mu, eps) * 1000.0
        rows.append({"material": mat, "mu": round(mu, 4), "eps_inf": eps,
                     "eps_inf_source": rec.get("source", ""), "status": status,
                     "E_b_meV": round(Eb, 1)})
        print(f"{mat:9s} mu={mu:.4f} eps_inf={eps:.2f} E_b={Eb:.0f} meV  [{status}]", flush=True)
    for mat, st in skipped:
        print(f"{mat:9s} SKIPPED (eps_inf {st})", flush=True)
    with open(f"{outdir}/binding_energy_9materials.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["material", "mu", "eps_inf",
                                           "eps_inf_source", "status", "E_b_meV"])
        w.writeheader(); w.writerows(rows)
    if rows:
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar([r["material"] for r in rows], [r["E_b_meV"] for r in rows])
        ax.set_ylabel("E_b (meV)"); ax.set_title("Theme I: Wannier-Mott E_b (TB mu + external eps_inf)")
        plt.xticks(rotation=45, ha="right"); fig.tight_layout()
        fig.savefig(f"{outdir}/binding_energy_summary.png", dpi=130); plt.close(fig)
    return rows, skipped


def run_production():
    import glob
    import shutil
    import subprocess
    import tempfile
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from make_production_bundle import build_bundle

    porcelain = [ln for ln in subprocess.run(["git", "status", "--porcelain"],
                 capture_output=True, text=True).stdout.splitlines()
                 if "results/production/" not in ln and "polling_logs" not in ln]
    if porcelain:
        sys.stderr.write("ERROR: working tree dirty -- commit first:\n" + "\n".join(porcelain) + "\n")
        sys.exit(1)

    stage = tempfile.mkdtemp(prefix="binde_")
    rows, skipped = compute(stage)
    if not rows:
        sys.stderr.write("No usable eps_inf yet (all pending Cowork Chrome search). "
                         "Bundle not created; re-run after data/parameters/eps_inf_external.json is filled.\n")
        sys.exit(2)
    shutil.copy2(EPS_JSON, f"{stage}/eps_inf_external.json")

    key = {f"{r['material']}_E_b_meV": r["E_b_meV"] for r in rows}
    key.update({f"{r['material']}_mu": r["mu"] for r in rows})
    key["materials_included"] = [r["material"] for r in rows]
    key["materials_pending_eps_inf"] = [m for m, _ in skipped]
    eps_sources = {r["material"]: r["eps_inf_source"] for r in rows}

    spec = {
        "theme": "theme_I_binding_energy",
        "subtask": "Y1-c-3: Wannier-Mott E_b (TB mu + external eps_inf)",
        "physics_method": "E_b = (mu/m0)/eps_inf^2 * Ry; mu = TB R-point curvature, eps_inf = external literature",
        "mode": "Production", "retroactive": False,
        "convergence": {"mu_convergence": "inherited from theme_I_effective_mass bundle "
                        "(dk<0.01%, isotropic); E_b formula is closed-form (no extra convergence)"},
        "outputs": [(f"{stage}/binding_energy_9materials.csv", "raw/binding_energy_9materials.csv")]
                   + ([(f"{stage}/binding_energy_summary.png", "figures/binding_energy_summary.png")]
                      if os.path.exists(f"{stage}/binding_energy_summary.png") else []),
        "inputs": [(KAS13, "kashikar13_params_9materials.json"),
                   (f"{stage}/eps_inf_external.json", "eps_inf_external.json")],
        "key_numbers": key,
        "references": ["Yang et al. 2017 PRB 96 035301", "Tanaka et al. 2003 SSC 127 619",
                       "Cho et al. 2019 (arXiv:1908.09436)", "Kashikar 2021 (arXiv:2101.08562)",
                       *[f"eps_inf({m}): {s}" for m, s in eps_sources.items()]],
        "notes": ("Hybrid production: effective masses (mu) are TB-derived from R-point band "
                  "curvature (Theme A k.p framework). eps_inf values are externally sourced from "
                  "literature (see references and inputs/eps_inf_external.json) to bypass the "
                  "Blount-1962 systematic underestimate of the TB-optical f-sum (~0.21, see "
                  "results/optical). The Wannier-Mott formula E_b=(mu/m0)/eps_r^2*Ry uses "
                  "eps_r=eps_inf (upper-bound screening; physical screening lies between eps_inf "
                  "and eps_static via phonon contribution -- Tanaka 2003 / Yang 2017). Absolute E_b "
                  "is therefore an upper bound; relative trends across materials are robust. "
                  "Materials with pending eps_inf are excluded (partial production)."),
        "readme": ("# Theme I (Y1-c-3): Wannier-Mott exciton binding E_b (hybrid)\n\n"
                   "E_b = (mu/m0)/eps_inf^2 * Ry. mu = TB R-point curvature; eps_inf = external "
                   "literature (data/parameters/eps_inf_external.json, cited). Partial set = "
                   "materials with a usable eps_inf.\n\nReproduce: OMP_NUM_THREADS=1 PYTHONPATH=src "
                   "python scripts/scan_theme_I_binding_energy.py production\n"),
        "cli": "OMP_NUM_THREADS=1 PYTHONPATH=src python scripts/scan_theme_I_binding_energy.py production",
    }
    root = build_bundle(spec)
    shutil.rmtree(stage, ignore_errors=True)
    print(f"PRODUCTION BUNDLE -> {root}  ({len(rows)} materials, {len(skipped)} pending)", flush=True)
    return root


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["compute", "production"])
    ap.add_argument("--outdir", default="results/theme_I_binding")
    args = ap.parse_args()
    if args.mode == "compute":
        compute(args.outdir)
    else:
        run_production()
