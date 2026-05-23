#!/usr/bin/env python3
"""F5: shift-current sigma_zzz(omega) scan over the 9 cubic CsBX3 (B=Ge/Sn/Pb,
X=Cl/Br/I) under a [001] polar B-cation displacement (P4mm), Kashikar-13 model.

Main question: do lead-free (Sn/Ge) compositions have a large shift-current
response?  Output is in CONSISTENT RELATIVE units (same prefactor for all
materials -> valid cross-material comparison).  Absolute uA/V^2 calibration
(Young & Rappe 2012 Eq.1 prefactor pi e^3 / (hbar^4 V_cell)) is deferred /
documented separately because it is convention-heavy and Blount-1962 limited.

Method validated in Theme F: Fregoso 2017 Eq.(C2) TB generalized derivative
(w-term), sign anchored on the Rice-Mele closed form Eq.(D15)/(D16) (F4-3) and
Tan & Rappe 2016 Eq.14 symmetry laws (F4-2).

IMPORTANT (performance): batched eigh of tiny matrices is pathologically slow
under multithreaded BLAS, so single-thread BLAS is forced *before* importing
numpy (n_kpts=24 sigma: 281s -> 5.9s).

Usage:
    python scripts/scan_shift_current_9materials.py convergence   # k/eta/omega study
    python scripts/scan_shift_current_9materials.py scan          # 9-material x delta
"""
import os
# Force single-thread BLAS BEFORE numpy import (see module docstring).
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import csv
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from perovskite_tb import shift_current as sc                       # noqa: E402
from perovskite_tb import models_kashikar as mk                     # noqa: E402
from perovskite_tb.io_params import get_material, load_parameter_file  # noqa: E402

# --- Cowork 5-min autonomous-polling hook (layer 2) -------------------------- #
# Long Production scans call _check_cowork_progress() in their main loop so that
# (a) a liveness line lands in cowork/polling_logs every 5 min and (b) a new
# directive is detected within 5 min.  Detection only -- never stops the scan
# (stopping would abort a Production run). See cowork/PRODUCTION_RULES.md and
# cowork/progress/2026-05-24_0655_autonomous_5min_polling_directive.md (X3a).
import datetime as _dt                                             # noqa: E402
from pathlib import Path                                           # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parents[1]
_LAST_POLL = _dt.datetime.now()


def _check_cowork_progress(project_root: Path = PROJECT_ROOT) -> None:
    """Every ~5 min: log liveness and warn on new cowork/ directives (no stop)."""
    global _LAST_POLL
    now = _dt.datetime.now()
    if (now - _LAST_POLL).total_seconds() < 300:
        return
    _LAST_POLL = now
    progress = project_root / "cowork" / "progress"
    logdir = project_root / "cowork" / "polling_logs"
    if not progress.is_dir():
        return
    cutoff = now - _dt.timedelta(minutes=10)
    new = [p.name for p in progress.glob("*.md")
           if _dt.datetime.fromtimestamp(p.stat().st_mtime) > cutoff
           and any(t in p.name for t in ("directive_", "code_review", "question", "BLOCKED"))]
    try:
        logdir.mkdir(parents=True, exist_ok=True)
        with open(logdir / f"poll_{now:%Y-%m-%d}.log", "a") as fh:
            fh.write(f"{now:%H:%M} scan alive" + (f" | NEW: {new}" if new else "") + "\n")
    except OSError:
        pass
    if new:
        print(f"[cowork-poll {now:%H:%M}] new directive(s): {new}", flush=True)

KAS13 = "data/parameters/kashikar2021_cubic_13orb.json"
MATERIALS = ["CsGeCl3", "CsGeBr3", "CsGeI3",
             "CsSnCl3", "CsSnBr3", "CsSnI3",
             "CsPbCl3", "CsPbBr3", "CsPbI3"]
N_OCC = 20  # B-s^2 + 3 x X-p^6 (filled), CBM = B-p


def sigma_zzz(params, a, delta, omega, n_kpts, eta):
    H, dH, d2H = sc.make_polar_kashikar13_builders(params, a, polar_displacement_z=delta)
    return sc.shift_current_zzz(H, dH, a, N_OCC, omega, n_kpts=n_kpts,
                                smearing_eta=eta, direction=2, d2Hdk_fn=d2H)


def load(material):
    m = get_material(load_parameter_file(KAS13), material)
    return m["params"], m["a"]


def run_convergence(outdir):
    """3-step convergence (k, eta, omega) on CsPbI3, delta=0.15. Saves plots+table."""
    os.makedirs(outdir, exist_ok=True)
    p, a = load("CsPbI3")
    delta = 0.15
    rows = []

    # (1) k-grid convergence at eta=0.10
    omega = np.linspace(0.3, 5.0, 300)
    fig, ax = plt.subplots(figsize=(7, 4))
    prev = None
    for nk in (24, 32, 48):
        s = sigma_zzz(p, a, delta, omega, nk, 0.10)
        l2 = "" if prev is None else f"{np.linalg.norm(s - prev) / np.linalg.norm(s):.4f}"
        rows.append({"study": "k", "n_kpts": nk, "eta": 0.10, "n_omega": 300,
                     "peak": float(s[np.argmax(np.abs(s))]),
                     "L2rel_vs_prev": l2})
        ax.plot(omega, s, label=f"n_kpts={nk}")
        prev = s
    ax.set_xlabel("hbar omega (eV)"); ax.set_ylabel("sigma_zzz (rel. units)")
    ax.set_title("CsPbI3 (delta=0.15) k-grid convergence, eta=0.10")
    ax.legend(); fig.tight_layout(); fig.savefig(f"{outdir}/sigma_vs_nkpts.png", dpi=130)
    plt.close(fig)

    # (2) eta sensitivity at n_kpts=48
    fig, ax = plt.subplots(figsize=(7, 4))
    for eta in (0.05, 0.08, 0.15):
        s = sigma_zzz(p, a, delta, omega, 48, eta)
        rows.append({"study": "eta", "n_kpts": 48, "eta": eta, "n_omega": 300,
                     "peak": float(s[np.argmax(np.abs(s))]), "L2rel_vs_prev": ""})
        ax.plot(omega, s, label=f"eta={eta}")
    ax.set_xlabel("hbar omega (eV)"); ax.set_ylabel("sigma_zzz (rel. units)")
    ax.set_title("CsPbI3 (delta=0.15) smearing sensitivity, n_kpts=48")
    ax.legend(); fig.tight_layout(); fig.savefig(f"{outdir}/sigma_vs_eta.png", dpi=130)
    plt.close(fig)

    # (3) omega-resolution convergence at n_kpts=48, eta=0.10
    fig, ax = plt.subplots(figsize=(7, 4))
    for nw in (150, 300, 600):
        og = np.linspace(0.3, 5.0, nw)
        s = sigma_zzz(p, a, delta, og, 48, 0.10)
        rows.append({"study": "omega_res", "n_kpts": 48, "eta": 0.10, "n_omega": nw,
                     "peak": float(s[np.argmax(np.abs(s))]), "L2rel_vs_prev": ""})
        ax.plot(og, s, label=f"n_omega={nw}")
    ax.set_xlabel("hbar omega (eV)"); ax.set_ylabel("sigma_zzz (rel. units)")
    ax.set_title("CsPbI3 (delta=0.15) omega-resolution, n_kpts=48 eta=0.10")
    ax.legend(); fig.tight_layout(); fig.savefig(f"{outdir}/sigma_vs_omega_res.png", dpi=130)
    plt.close(fig)

    with open(f"{outdir}/convergence_table.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["study", "n_kpts", "eta", "n_omega",
                                           "peak", "L2rel_vs_prev"])
        w.writeheader(); w.writerows(rows)
    print(f"convergence study -> {outdir}")
    for r in rows:
        print(r)


def run_scan(outdir, n_kpts=48, eta=0.10, deltas=(0.10, 0.15, 0.20)):
    """9 materials x delta -> sigma_zzz(omega), CSV + comparison plot (relative units)."""
    os.makedirs(outdir, exist_ok=True)
    omega = np.linspace(0.3, 5.0, 300)
    results = {}        # (material, delta) -> sigma array
    gaps = {}           # material -> gap at R-point (eV)  [R, not necessarily CBM/VBM]
    for mat in MATERIALS:
        p, a = load(mat)
        ev = np.sort(np.linalg.eigvalsh(
            mk.kashikar13_hamiltonian(np.array([1, 1, 1]) * np.pi / a, p, a)).real)
        gaps[mat] = float(ev[N_OCC] - ev[N_OCC - 1])
        for d in deltas:
            results[(mat, d)] = sigma_zzz(p, a, d, omega, n_kpts, eta)
        peak = results[(mat, 0.15)][np.argmax(np.abs(results[(mat, 0.15)]))]
        print(f"{mat}: gap_at_R={gaps[mat]:.3f} eV  sigma_zzz peak(delta=0.15)={peak:+.3e}",
              flush=True)
        _check_cowork_progress()    # layer-2 5-min poll hook (liveness + new directives)

    # CSV: omega + each (material, delta) column
    cols = ["omega_eV"] + [f"{m}_d{d}" for m in MATERIALS for d in deltas]
    with open(f"{outdir}/sigma_zzz_9materials.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(cols)
        for i, om in enumerate(omega):
            w.writerow([f"{om:.5f}"] + [f"{results[(m, d)][i]:.6e}"
                                        for m in MATERIALS for d in deltas])

    # comparison plot at delta=0.15 grouped by B cation
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = {"Ge": "tab:green", "Sn": "tab:blue", "Pb": "tab:red"}
    styles = {"Cl": ":", "Br": "--", "I": "-"}
    for mat in MATERIALS:
        B = mat[2:4]; X = mat[4:].rstrip("3")
        ax.plot(omega, results[(mat, 0.15)], color=colors[B], ls=styles[X],
                label=f"{mat} (Eg={gaps[mat]:.2f})")
    ax.set_xlabel("hbar omega (eV)"); ax.set_ylabel("sigma_zzz (rel. units)")
    ax.set_title(f"Shift current sigma_zzz, [001] polar delta=0.15 A "
                 f"(Kashikar-13, n_kpts={n_kpts}, eta={eta})")
    ax.legend(fontsize=7, ncol=3); ax.axhline(0, color="k", lw=0.5)
    fig.tight_layout(); fig.savefig(f"{outdir}/sigma_zzz_9materials.png", dpi=130)
    plt.close(fig)

    # peak summary CSV (relative units)
    with open(f"{outdir}/peak_summary.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["material", "gap_at_R_eV"] + [f"peak_d{d}" for d in deltas]
                   + [f"peak_omega_d{d}_eV" for d in deltas])
        for mat in MATERIALS:
            row = [mat, f"{gaps[mat]:.4f}"]
            for d in deltas:
                s = results[(mat, d)]; ip = np.argmax(np.abs(s))
                row.append(f"{s[ip]:.6e}")
            for d in deltas:
                s = results[(mat, d)]; ip = np.argmax(np.abs(s))
                row.append(f"{omega[ip]:.4f}")
            w.writerow(row)
    print(f"scan -> {outdir}  (settings n_kpts={n_kpts}, eta={eta}, deltas={deltas})",
          flush=True)
    return results, gaps, omega


def run_production(allow_dirty=False, n_kpts=48, eta=0.10, deltas=(0.10, 0.15, 0.20)):
    """Full Production bundle (PRODUCTION_RULES): git-clean check -> convergence +
    9-material scan -> results/production/theme_F_shift_current/<date>_<hash>/ with
    MANIFEST.json, inputs/, outputs/, convergence/, logs/, README.md."""
    import glob
    import json
    import shutil
    import subprocess
    import tempfile
    import time
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from make_production_bundle import build_bundle

    porcelain = [ln for ln in subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True).stdout.splitlines()
        if "results/production/" not in ln]
    if porcelain and not allow_dirty:
        sys.stderr.write("ERROR: working tree dirty -- commit first or pass --allow-dirty:\n"
                         + "\n".join(porcelain) + "\n")
        sys.exit(1)

    stage = tempfile.mkdtemp(prefix="f5_")
    t0 = time.time()
    run_convergence(f"{stage}/convergence")
    results, gaps, omega = run_scan(stage, n_kpts=n_kpts, eta=eta, deltas=deltas)
    # delta=0 null check (centrosymmetric -> sigma=0)
    p, a = load("CsPbI3")
    null = float(np.max(np.abs(sigma_zzz(p, a, 0.0, omega, n_kpts, eta))))
    runtime = time.time() - t0

    key = {"runtime_seconds": round(runtime, 1),
           "settings": f"n_kpts={n_kpts}, eta={eta}, deltas={list(deltas)}, n_occ={N_OCC}",
           "delta0_null_max_abs_sigma_zzz_rel": null,
           "units_note": ("relative (consistent prefactor across all 9 materials -> valid "
                          "cross-material comparison); absolute uA/V^2 deferred (Young&Rappe "
                          "2012 Eq.1 prefactor pi e^3/(hbar^4 V_cell); Blount-1962 limited)")}
    for mat in MATERIALS:
        s = results[(mat, 0.15)]; ip = int(np.argmax(np.abs(s)))
        Eg = gaps[mat]; band = (omega >= Eg) & (omega <= 2 * Eg)
        key[f"{mat}_peak_sigma_zzz_rel_d0.15"] = float(s[ip])
        key[f"{mat}_peak_omega_eV_d0.15"] = float(omega[ip])
        key[f"{mat}_omega_integral_Eg_2Eg_rel_d0.15"] = (
            float(np.trapezoid(s[band], omega[band])) if int(band.sum()) > 1 else None)
        key[f"{mat}_gap_at_R_eV"] = float(Eg)

    json.dump({"n_kpts": n_kpts, "eta": eta, "omega_min": 0.3, "omega_max": 5.0,
               "n_omega": 300, "deltas": list(deltas), "n_occ": N_OCC,
               "model": "Kashikar-13 polar [001] (P4mm)", "harrison_eta": 2.0,
               "single_thread_blas": True},
              open(f"{stage}/scan_config.json", "w"), indent=2)
    json.dump({"materials": MATERIALS, "B_cations": ["Ge", "Sn", "Pb"],
               "halides": ["Cl", "Br", "I"]}, open(f"{stage}/materials.json", "w"), indent=2)
    json.dump({"random_seeds": "not used (deterministic eigh + uniform Monkhorst-Pack k-grid)"},
              open(f"{stage}/seeds.json", "w"), indent=2)

    cli = ("OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONPATH=src "
           "python scripts/scan_shift_current_9materials.py production")
    readme = (
        "# Theme F (F5): shift current sigma_zzz for 9 cubic CsBX3 under [001] polar displacement\n\n"
        "sigma_zzz(omega) for B=Ge/Sn/Pb x X=Cl/Br/I (Kashikar-13 TB, P4mm, delta in {0.10,0.15,0.20} A).\n"
        "Method: Fregoso 2017 Eq.(C2) TB generalized derivative (w-term); sign anchored on Rice-Mele\n"
        "Eq.(D15)/(D16) (F4-3) and Tan&Rappe 2016 Eq.14 symmetry laws (F4-2). Relative units.\n\n"
        f"Reproduce:\n    {cli}\n\n"
        "Outputs: outputs/raw/sigma_zzz_9materials.csv, outputs/figures/sigma_zzz_9materials.png,\n"
        "convergence/ (k/eta/omega studies). See MANIFEST.json key_numbers.\n")
    spec = {
        "theme": "theme_F_shift_current",
        "subtask": "F5 9-material x delta shift-current scan",
        "physics_method": ("Fregoso 2017 Eq.(C2) TB shift current (w-term) | Kashikar-13 [001] "
                           "polar (P4mm) Harrison eta=2.0 | velocity gauge, sum-over-states"),
        "mode": "Production", "retroactive": False,
        "convergence": {"k_grid": [24, 32, 48], "eta_eV": [0.05, 0.08, 0.15],
                        "omega_resolution": [150, 300, 600], "production_n_kpts": n_kpts,
                        "production_eta_eV": eta, "L2rel_k32_to_k48_at_eta0.10": 0.019,
                        "note": "eta=0.05 too sharp for these grids; eta>=0.08 converges (see convergence/)"},
        "outputs": [(f"{stage}/sigma_zzz_9materials.csv", "raw/sigma_zzz_9materials.csv"),
                    (f"{stage}/peak_summary.csv", "raw/peak_summary.csv"),
                    (f"{stage}/sigma_zzz_9materials.png", "figures/sigma_zzz_9materials.png")],
        "inputs": [(KAS13, "kashikar13_params_9materials.json"),
                   (f"{stage}/scan_config.json", "scan_config.json"),
                   (f"{stage}/materials.json", "materials.json"),
                   (f"{stage}/seeds.json", "seeds.json")],
        "key_numbers": key,
        "references": ["Fregoso, Morimoto, Moore 2017 PRB 96 075421 (arXiv:1701.00172) Eq.(C2)/(D12)/(D15)",
                       "Tan, Zheng, Young, Wang, Liu, Rappe 2016 npj Comput Mater 2:16026",
                       "Young & Rappe 2012 PRL 109 116601 (arXiv:1202.3168) Eq.(1)",
                       "Kashikar, Gupta, Nanda 2021 (arXiv:2101.08562)"],
        "notes": ("Relative units are the primary deliverable; absolute uA/V^2 is Blount-1962 "
                  "limited (TB intra-atomic position contributions missing -- same systematic "
                  "underestimate as the g-factor and optical f-sum). Single-thread BLAS forced "
                  "before numpy import (n_kpts=24 sigma 281s->5.9s). delta=0 null sigma_zzz max "
                  f"|.|={null:.2e} (centrosymmetric vanishing). gap is the R-point N_OCC gap "
                  "(not guaranteed CBM-VBM for all materials)."),
        "readme": readme, "cli": cli,
    }
    root = build_bundle(spec)
    for f in glob.glob(f"{stage}/convergence/*"):
        shutil.copy2(f, os.path.join(root, "convergence", os.path.basename(f)))
    with open(os.path.join(root, "logs", "run.log"), "w") as fh:
        fh.write(f"runtime_seconds={runtime:.1f}\nn_kpts={n_kpts} eta={eta} deltas={list(deltas)}\n"
                 f"delta0_null_max_abs={null:.3e}\n")
    shutil.rmtree(stage, ignore_errors=True)
    print(f"PRODUCTION BUNDLE -> {root}  (runtime {runtime:.0f}s)", flush=True)
    return root


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["convergence", "scan", "production"])
    ap.add_argument("--outdir", default="results/shift_current")
    ap.add_argument("--n_kpts", type=int, default=48)
    ap.add_argument("--eta", type=float, default=0.10)
    ap.add_argument("--allow-dirty", action="store_true")
    args = ap.parse_args()
    if args.mode == "convergence":
        run_convergence(f"{args.outdir}/convergence")
    elif args.mode == "scan":
        run_scan(args.outdir, n_kpts=args.n_kpts, eta=args.eta)
    else:
        run_production(allow_dirty=args.allow_dirty, n_kpts=args.n_kpts, eta=args.eta)
