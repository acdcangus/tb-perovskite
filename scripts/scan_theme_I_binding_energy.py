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


def compute(outdir, profile="effective"):
    """profile='effective': use the cited web-research eps_inf (CsPbI3/CsPbCl3 only).
    profile='MP_DFPT': use the Materials Project DFPT eps_inf (single-method, 8/9)."""
    os.makedirs(outdir, exist_ok=True)
    eps_db = json.load(open(EPS_JSON))["materials"]
    rows, skipped = [], []
    for mat, rec in eps_db.items():
        if profile == "MP_DFPT":
            mpd = rec.get("eps_inf_MP_DFPT") or {}
            eps = mpd.get("value")
            status = "MP_DFPT"
            src = mpd.get("method", "")
            phase = mpd.get("phase_note", "")
        else:
            eps = rec.get("eps_inf")
            status = rec.get("status", "")
            if status not in _USABLE:
                eps = None
            src = rec.get("source", "")
            phase = rec.get("notes", "")
        if eps is None:
            skipped.append((mat, status if profile != "MP_DFPT" else (rec.get("eps_inf_MP_DFPT") or {}).get("status", "no_value")))
            continue
        mu = _mu(mat)
        Eb = ex.wannier_mott_binding_eV(mu, eps) * 1000.0
        rows.append({"material": mat, "mu": round(mu, 4), "eps_inf": eps,
                     "eps_inf_source": src, "status": status, "E_b_meV": round(Eb, 1),
                     "phase_note": phase})
        print(f"{mat:9s} mu={mu:.4f} eps_inf={eps:.2f} E_b={Eb:.0f} meV  [{status}]", flush=True)
    for mat, st in skipped:
        print(f"{mat:9s} SKIPPED (eps_inf {st})", flush=True)
    with open(f"{outdir}/binding_energy_9materials.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["material", "mu", "eps_inf",
                                           "eps_inf_source", "status", "E_b_meV", "phase_note"])
        w.writeheader(); w.writerows(rows)
    if rows:
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar([r["material"] for r in rows], [r["E_b_meV"] for r in rows])
        ax.set_ylabel("E_b (meV)"); ax.set_title("Theme I: Wannier-Mott E_b (TB mu + external eps_inf)")
        plt.xticks(rotation=45, ha="right"); fig.tight_layout()
        fig.savefig(f"{outdir}/binding_energy_summary.png", dpi=130); plt.close(fig)
    return rows, skipped


def run_production(profile="MP_DFPT"):
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
    rows, skipped = compute(stage, profile=profile)
    if not rows:
        sys.stderr.write("No usable eps_inf for this profile.\n")
        sys.exit(2)
    shutil.copy2(EPS_JSON, f"{stage}/eps_inf_external.json")

    key = {f"{r['material']}_E_b_meV": r["E_b_meV"] for r in rows}
    key.update({f"{r['material']}_mu": r["mu"] for r in rows})
    key.update({f"{r['material']}_eps_inf": r["eps_inf"] for r in rows})
    key["materials_included"] = [r["material"] for r in rows]
    key["materials_pending_eps_inf"] = [m for m, _ in skipped]
    key["profile"] = profile
    eps_sources = {r["material"]: r["eps_inf_source"] for r in rows}
    theme = "theme_I_exciton_MP_DFPT" if profile == "MP_DFPT" else "theme_I_binding_energy"

    spec = {
        "theme": theme,
        "subtask": f"Y1-c-3 ({profile}): Wannier-Mott E_b (TB mu + {profile} eps_inf)",
        "physics_method": "E_b = (mu/m0)/eps_inf^2 * Ry; mu = TB R-point curvature, eps_inf = Materials Project DFPT (single method)",
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
                       "Materials Project (Jain et al. 2013 APL Mater. 1, 011002), DFPT dielectric",
                       *[f"eps_inf({m}): {s}" for m, s in eps_sources.items()]],
        "notes": ("Option C' hybrid production: effective masses (mu) are TB-derived from R-point "
                  "band curvature (cubic Kashikar-13). eps_inf is the Materials Project DFPT "
                  "ELECTRONIC (bare) dielectric -- a SINGLE, consistent method across materials, so "
                  "the RELATIVE E_b trend is maximally defensible. CAVEAT: bare eps_inf < effective "
                  "exciton eps_eff (no phonon/ionic screening), so the Wannier-Mott E_b="
                  "(mu/m0)/eps_inf^2*Ry is an UPPER BOUND (overestimate); e.g. CsPbI3 here ~41 meV vs "
                  "experiment ~15-20 meV. MP computed DFPT dielectric for the cubic phase for some "
                  "materials (CsGeBr3/CsSnBr3/CsSnI3) and for ortho/rhombo/monoclinic ground states "
                  "for others; mu is cubic-phase, so eps_inf is used as a ~phase-insensitive proxy "
                  "(phase recorded per material in inputs/eps_inf_external.json). CsSnCl3 has no MP "
                  "dielectric (excluded). API key never stored; provenance = mp-id + URL only."),
        "readme": ("# Theme I (Y1-c-3, option C'): Wannier-Mott E_b with Materials Project DFPT eps_inf\n\n"
                   "E_b = (mu/m0)/eps_inf^2 * Ry. mu = TB cubic R-point curvature; eps_inf = MP DFPT "
                   "(single method, 8/9 materials, phases noted). BARE eps_inf -> absolute E_b is an "
                   "upper bound; relative trend defensible.\n\nReproduce: "
                   "PYTHONPATH=src python scripts/fetch_mp_eps_inf.py  # needs data/parameters/mp_api_key.json\n"
                   "PYTHONPATH=src python scripts/scan_theme_I_binding_energy.py production --profile MP_DFPT\n"),
        "cli": "PYTHONPATH=src python scripts/scan_theme_I_binding_energy.py production --profile MP_DFPT",
    }
    root = build_bundle(spec)
    shutil.rmtree(stage, ignore_errors=True)
    print(f"PRODUCTION BUNDLE -> {root}  ({len(rows)} materials, {len(skipped)} pending)", flush=True)
    return root


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["compute", "production"])
    ap.add_argument("--profile", choices=["effective", "MP_DFPT"], default="MP_DFPT")
    ap.add_argument("--outdir", default="results/theme_I_binding")
    args = ap.parse_args()
    if args.mode == "compute":
        compute(args.outdir, profile=args.profile)
    else:
        run_production(profile=args.profile)
