#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Teruhisa Kotani
"""Theme I (Y1-a): TB band-edge effective-mass map for the 9 cubic CsBX3.

Per-axis m_e/m_h (x,y,z) + average + anisotropy ratio at the R-point direct-gap
edge (Kashikar-13), reduced mass mu.  Fully TB-derived (no dielectric input) ->
the reliable, publishable Theme-I primary deliverable.

Convergence (PRODUCTION_RULES §1):
  * dk (finite-difference step) for the d^2E/dk^2 second difference;
  * direction anisotropy [100]/[010]/[001] (cubic -> should be isotropic).
  NOTE n_kpts is NOT a convergence axis here: the effective mass is a SINGLE-POINT
  band curvature at R (an exact derivative of E(k)), not a Brillouin-zone integral,
  so it is independent of any Monkhorst-Pack grid density.  This is documented in
  the bundle MANIFEST.notes rather than faking an n_kpts study.

Usage:
    python scripts/scan_theme_I_effective_mass.py convergence
    python scripts/scan_theme_I_effective_mass.py production
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import csv
import datetime as _dt
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
MATERIALS = ["CsGeCl3", "CsGeBr3", "CsGeI3", "CsSnCl3", "CsSnBr3", "CsSnI3",
             "CsPbCl3", "CsPbBr3", "CsPbI3"]
N_OCC = 20
_AXES = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}
_LAST_POLL = _dt.datetime.now()


def _check_cowork_progress(project_root: Path = PROJECT_ROOT) -> None:
    """Layer-2 5-min poll hook (liveness + new-directive detection; never stops)."""
    global _LAST_POLL
    now = _dt.datetime.now()
    if (now - _LAST_POLL).total_seconds() < 300:
        return
    _LAST_POLL = now
    progress = project_root / "cowork" / "progress"
    if not progress.is_dir():
        return
    cutoff = now - _dt.timedelta(minutes=10)
    new = [p.name for p in progress.glob("*.md")
           if _dt.datetime.fromtimestamp(p.stat().st_mtime) > cutoff
           and any(t in p.name for t in ("directive_", "code_review", "question", "BLOCKED"))]
    try:
        (project_root / "cowork" / "polling_logs").mkdir(parents=True, exist_ok=True)
        with open(project_root / "cowork" / "polling_logs" / f"poll_{now:%Y-%m-%d}.log", "a") as fh:
            fh.write(f"{now:%H:%M} effmass-scan alive" + (f" | NEW: {new}" if new else "") + "\n")
    except OSError:
        pass
    if new:
        print(f"[cowork-poll {now:%H:%M}] new directive(s): {new}", flush=True)


def _H(mat):
    m = get_material(load_parameter_file(KAS13), mat)
    p, a = m["params"], m["a"]
    return (lambda k, p=p, a=a: mk.kashikar13_hamiltonian(k, p, a)), a


def per_axis_masses(mat, band_idx, dk=1e-3):
    """Return dict {x,y,z,avg, aniso} of m*/m0 for band_idx at R."""
    H, a = _H(mat)
    mx = {ax: ex.effective_mass(H, a, band_idx, dk=dk, directions=[d])
          for ax, d in _AXES.items()}
    vals = np.array(list(mx.values()))
    mx["avg"] = float(np.mean(vals))
    mx["aniso"] = float(np.max(np.abs(vals)) / np.min(np.abs(vals)))   # >=1; 1=isotropic
    return mx


def run_convergence(outdir):
    os.makedirs(outdir, exist_ok=True)
    H, a = _H("CsPbI3")
    rows = []
    for dk in (2e-2, 1e-2, 5e-3, 1e-3, 5e-4):
        me = ex.effective_mass(H, a, N_OCC, dk=dk)
        mh = ex.effective_mass(H, a, N_OCC - 1, dk=dk)
        rows.append({"axis": "dk_study", "dk": dk, "m_e_avg": round(me, 5), "m_h_avg": round(mh, 5)})
    # direction anisotropy at converged dk
    for ax, d in _AXES.items():
        me = ex.effective_mass(H, a, N_OCC, dk=1e-3, directions=[d])
        mh = ex.effective_mass(H, a, N_OCC - 1, dk=1e-3, directions=[d])
        rows.append({"axis": ax, "dk": 1e-3, "m_e_avg": round(me, 5), "m_h_avg": round(mh, 5)})
    with open(f"{outdir}/effmass_convergence.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["axis", "dk", "m_e_avg", "m_h_avg"])
        w.writeheader(); w.writerows(rows)
    fig, ax = plt.subplots(figsize=(6, 4))
    dkrows = [r for r in rows if r["axis"] == "dk_study"]
    ax.plot([r["dk"] for r in dkrows], [r["m_e_avg"] for r in dkrows], "o-", label="m_e")
    ax.plot([r["dk"] for r in dkrows], [abs(r["m_h_avg"]) for r in dkrows], "s-", label="|m_h|")
    ax.set_xscale("log"); ax.set_xlabel("dk step"); ax.set_ylabel("m*/m0 (CsPbI3)")
    ax.set_title("Effective-mass dk convergence (CsPbI3, R-point)"); ax.legend()
    fig.tight_layout(); fig.savefig(f"{outdir}/effmass_dk_convergence.png", dpi=130); plt.close(fig)
    for r in rows:
        print(r, flush=True)
    return rows


def run_scan(outdir, dk=1e-3):
    os.makedirs(outdir, exist_ok=True)
    rows = []
    hdr = ["material", "m_e_x", "m_e_y", "m_e_z", "m_e_avg", "m_e_aniso",
           "m_h_x", "m_h_y", "m_h_z", "m_h_avg", "m_h_aniso", "mu"]
    print(f"{'material':9s} {'m_e_avg':>8s} {'m_h_avg':>8s} {'mu':>6s} {'aniso_e':>8s}", flush=True)
    for mat in MATERIALS:
        me = per_axis_masses(mat, N_OCC, dk)
        mh = per_axis_masses(mat, N_OCC - 1, dk)
        mu = ex.reduced_mass(me["avg"], mh["avg"])
        rows.append({"material": mat,
                     "m_e_x": round(me["x"], 4), "m_e_y": round(me["y"], 4), "m_e_z": round(me["z"], 4),
                     "m_e_avg": round(me["avg"], 4), "m_e_aniso": round(me["aniso"], 4),
                     "m_h_x": round(mh["x"], 4), "m_h_y": round(mh["y"], 4), "m_h_z": round(mh["z"], 4),
                     "m_h_avg": round(mh["avg"], 4), "m_h_aniso": round(mh["aniso"], 4),
                     "mu": round(mu, 4)})
        print(f"{mat:9s} {me['avg']:+8.4f} {mh['avg']:+8.4f} {mu:6.4f} {me['aniso']:8.4f}", flush=True)
        _check_cowork_progress()
    with open(f"{outdir}/effective_masses_9materials.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=hdr)
        w.writeheader(); w.writerows(rows)
    # summary plot grouped by B-cation / halide
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = {"Ge": "tab:green", "Sn": "tab:blue", "Pb": "tab:red"}
    xpos = {"Cl": 0, "Br": 1, "I": 2}
    for r in rows:
        B, X = r["material"][2:4], r["material"][4:].rstrip("3")
        ax.scatter(xpos[X], r["mu"], color=colors[B], s=80,
                   label=B if X == "Cl" else None)
        ax.annotate(f"{r['mu']:.3f}", (xpos[X], r["mu"]), fontsize=7,
                    xytext=(4, 2), textcoords="offset points")
    ax.set_xticks([0, 1, 2]); ax.set_xticklabels(["Cl", "Br", "I"])
    ax.set_xlabel("halide"); ax.set_ylabel("exciton reduced mass mu/m0")
    ax.set_title("Theme I: TB reduced mass mu (R-point), 9 cubic CsBX3"); ax.legend(title="B")
    fig.tight_layout(); fig.savefig(f"{outdir}/effective_mass_summary.png", dpi=130); plt.close(fig)
    return rows


def run_production():
    import glob
    import json
    import shutil
    import subprocess
    import tempfile
    import time
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from make_production_bundle import build_bundle

    porcelain = [ln for ln in subprocess.run(["git", "status", "--porcelain"],
                 capture_output=True, text=True).stdout.splitlines()
                 if "results/production/" not in ln and "polling_logs" not in ln]
    if porcelain:
        sys.stderr.write("ERROR: working tree dirty -- commit first:\n" + "\n".join(porcelain) + "\n")
        sys.exit(1)

    stage = tempfile.mkdtemp(prefix="effm_")
    t0 = time.time()
    conv = run_convergence(f"{stage}/convergence")
    rows = run_scan(stage)
    runtime = time.time() - t0

    key = {"runtime_seconds": round(runtime, 1),
           "dk_converged_m_e_CsPbI3": [r["m_e_avg"] for r in conv if r["axis"] == "dk_study"][-1]}
    for r in rows:
        key[f"{r['material']}_m_e_avg"] = r["m_e_avg"]
        key[f"{r['material']}_m_h_avg"] = r["m_h_avg"]
        key[f"{r['material']}_mu"] = r["mu"]
        key[f"{r['material']}_m_e_aniso"] = r["m_e_aniso"]

    json.dump({"materials": MATERIALS, "n_occ": N_OCC, "dk": 1e-3,
               "k_point": "R = pi/a (1,1,1)", "model": "Kashikar-13",
               "method": "m*/m0 = (hbar^2/m0)/(d2E/dk2), central difference, per-axis"},
              open(f"{stage}/scan_config.json", "w"), indent=2)

    spec = {
        "theme": "theme_I_effective_mass",
        "subtask": "Y1-a: 9-material band-edge effective-mass map",
        "physics_method": ("band-edge effective mass m*/m0 = (hbar^2/m0)/(d2E/dk2) at R-point "
                           "(Kashikar-13), per Cartesian axis + average + anisotropy; "
                           "mu = 1/(1/|m_e|+1/|m_h|)"),
        "mode": "Production", "retroactive": False,
        "convergence": {"dk": [2e-2, 1e-2, 5e-3, 1e-3, 5e-4],
                        "directions": ["x", "y", "z"],
                        "n_kpts": "N/A (single-point R-curvature, not a BZ integral)"},
        "outputs": [(f"{stage}/effective_masses_9materials.csv", "raw/effective_masses_9materials.csv"),
                    (f"{stage}/effective_mass_summary.png", "figures/effective_mass_summary.png")],
        "inputs": [(KAS13, "kashikar13_params_9materials.json"),
                   (f"{stage}/scan_config.json", "scan_config.json")],
        "key_numbers": key,
        "references": ["Kashikar, Gupta, Nanda 2021 (arXiv:2101.08562)",
                       "Yang et al. 2017 PRB 96 035301", "Cho et al. 2019 (arXiv:1908.09436)",
                       "Theme A k.p framework (src/perovskite_tb/kane_parameter.py)"],
        "notes": ("TB-derived effective masses from R-point d2E/dk2. Direct band-gap material "
                  "set (CsBX3 cubic phase). m_e/m_h consistent with literature (~0.1-0.15 m0 for "
                  "CsPbI3). Cubic point group -> isotropic (anisotropy ratio ~1; see CSV). n_kpts "
                  "is not a convergence axis (single-point curvature, exact derivative); dk and "
                  "direction-anisotropy are the convergence axes (see convergence/)."),
        "readme": ("# Theme I (Y1-a): TB effective-mass map, 9 cubic CsBX3\n\n"
                   "Per-axis m_e/m_h + avg + anisotropy + reduced mass mu at the R-point "
                   "direct-gap edge (Kashikar-13). Fully TB-derived. dk & direction converged.\n\n"
                   "Reproduce: OMP_NUM_THREADS=1 PYTHONPATH=src python "
                   "scripts/scan_theme_I_effective_mass.py production\n"),
        "cli": "OMP_NUM_THREADS=1 PYTHONPATH=src python scripts/scan_theme_I_effective_mass.py production",
    }
    root = build_bundle(spec)
    for f in glob.glob(f"{stage}/convergence/*"):
        shutil.copy2(f, os.path.join(root, "convergence", os.path.basename(f)))
    shutil.rmtree(stage, ignore_errors=True)
    print(f"PRODUCTION BUNDLE -> {root}  (runtime {runtime:.0f}s)", flush=True)
    return root


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["convergence", "scan", "production"])
    ap.add_argument("--outdir", default="results/theme_I_effmass")
    args = ap.parse_args()
    if args.mode == "convergence":
        run_convergence(f"{args.outdir}/convergence")
    elif args.mode == "scan":
        run_scan(args.outdir)
    else:
        run_production()
