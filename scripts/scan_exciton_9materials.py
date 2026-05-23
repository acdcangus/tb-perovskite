#!/usr/bin/env python3
"""Theme I: effective-mass map + Wannier-Mott exciton binding for the 9 cubic CsBX3.

PRIMARY (reliable) deliverable: the band-edge effective masses m_e, m_h and the
exciton reduced mass mu, all TB-derived (no dielectric input).  These are the
publishable Theme-I numbers.

SECONDARY (caveated): E_b = (mu/m0)/eps_r^2 * Ry.  Computed here with the
TB-optical eps_inf (optical.compute_dielectric KK static limit), which inherits
the Blount-limited f-sum (~0.21) and so UNDER-estimates eps_inf -> OVER-estimates
E_b, badly for the wide-gap Cl materials (see Cowork patrol 2026-05-24_0055 and
cowork/progress/2026-05-24_0050_theme_I_exciton_exploratory.md).  E_b is therefore
reported as a RELATIVE TREND only; absolute E_b with an external (DFT/exp) eps_inf
is option (c), pending PI decision.

Single-thread BLAS recommended (set OMP_NUM_THREADS=1 ... before python).

Usage:
    python scripts/scan_exciton_9materials.py convergence   # dk + direction study
    python scripts/scan_exciton_9materials.py production     # bundle (masses primary)
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

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from perovskite_tb import exciton as ex                              # noqa: E402
from perovskite_tb import models_kashikar as mk                      # noqa: E402
from perovskite_tb import velocity as vel                            # noqa: E402
from perovskite_tb.optical import compute_dielectric                 # noqa: E402
from perovskite_tb.io_params import get_material, load_parameter_file  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parents[1]
KAS13 = "data/parameters/kashikar2021_cubic_13orb.json"
MATERIALS = ["CsGeCl3", "CsGeBr3", "CsGeI3", "CsSnCl3", "CsSnBr3", "CsSnI3",
             "CsPbCl3", "CsPbBr3", "CsPbI3"]
N_OCC = 20
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
            fh.write(f"{now:%H:%M} exciton-scan alive" + (f" | NEW: {new}" if new else "") + "\n")
    except OSError:
        pass
    if new:
        print(f"[cowork-poll {now:%H:%M}] new directive(s): {new}", flush=True)


def _builders(p, a):
    H = lambda k, p=p, a=a: mk.kashikar13_hamiltonian(k, p, a)        # noqa: E731
    dh = lambda k, al, p=p, a=a: vel.dH_dk_kashikar13(k, p, a, al)    # noqa: E731
    return H, dh


def masses_and_eps(mat, dk=1e-3, with_eps=True):
    m = get_material(load_parameter_file(KAS13), mat)
    p, a = m["params"], m["a"]
    H, dh = _builders(p, a)
    m_e = ex.effective_mass(H, a, N_OCC, dk=dk)       # CBM
    m_h = ex.effective_mass(H, a, N_OCC - 1, dk=dk)   # VBM
    mu = ex.reduced_mass(m_e, m_h)
    eps = None
    if with_eps:
        omega = np.linspace(0.1, 6.0, 280)
        eps = float(compute_dielectric(H, dh, a, N_OCC, omega, n_kpts=8,
                                       smearing_eta=0.05)["eps_real"][0])
    return m_e, m_h, mu, eps


def run_convergence(outdir):
    """dk (finite-difference step) + direction-anisotropy convergence on CsPbI3."""
    os.makedirs(outdir, exist_ok=True)
    m = get_material(load_parameter_file(KAS13), "CsPbI3")
    p, a = m["params"], m["a"]
    H, _ = _builders(p, a)
    rows = []
    for dk in (2e-2, 1e-2, 5e-3, 1e-3):
        me = ex.effective_mass(H, a, N_OCC, dk=dk)
        mh = ex.effective_mass(H, a, N_OCC - 1, dk=dk)
        rows.append({"study": "dk", "dk": dk, "m_e": round(me, 5), "m_h": round(mh, 5)})
    for d, lbl in (([(1, 0, 0)], "100"), ([(1, 1, 0)], "110"), ([(1, 1, 1)], "111")):
        me = ex.effective_mass(H, a, N_OCC, dk=1e-3, directions=d)
        mh = ex.effective_mass(H, a, N_OCC - 1, dk=1e-3, directions=d)
        rows.append({"study": "direction", "dk": lbl, "m_e": round(me, 5), "m_h": round(mh, 5)})
    with open(f"{outdir}/effmass_convergence.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["study", "dk", "m_e", "m_h"])
        w.writeheader(); w.writerows(rows)
    for r in rows:
        print(r, flush=True)
    return rows


def run_scan(outdir, dk=1e-3):
    os.makedirs(outdir, exist_ok=True)
    rows = []
    print(f"{'mat':9s} {'m_e':>6s} {'m_h':>7s} {'mu':>6s} {'eps_inf_TB':>10s} {'E_b_rel(meV)':>12s}",
          flush=True)
    for mat in MATERIALS:
        me, mh, mu, eps = masses_and_eps(mat, dk=dk)
        Eb = ex.wannier_mott_binding_eV(mu, eps) * 1000.0
        rows.append({"material": mat, "m_e": round(me, 4), "m_h": round(mh, 4),
                     "mu": round(mu, 4), "eps_inf_TB": round(eps, 3),
                     "E_b_rel_meV": round(Eb, 1)})
        print(f"{mat:9s} {me:+6.3f} {mh:+7.3f} {mu:6.3f} {eps:10.2f} {Eb:12.0f}", flush=True)
        _check_cowork_progress()
    with open(f"{outdir}/exciton_9materials.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["material", "m_e", "m_h", "mu",
                                           "eps_inf_TB", "E_b_rel_meV"])
        w.writeheader(); w.writerows(rows)
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

    stage = tempfile.mkdtemp(prefix="exc_")
    t0 = time.time()
    conv = run_convergence(f"{stage}/convergence")
    rows = run_scan(stage)
    runtime = time.time() - t0

    key = {"runtime_seconds": round(runtime, 1),
           "primary": "effective masses m_e, m_h, mu (TB-derived, reliable)",
           "secondary_caveat": ("E_b uses TB-optical eps_inf (Blount-limited f-sum~0.21 -> "
                                "eps_inf underestimated -> E_b overestimated, esp. Cl); "
                                "RELATIVE TREND ONLY. Absolute E_b needs external DFT/exp eps_inf (option c)."),
           "dk_converged": conv[2]["m_e"]}
    for r in rows:
        m = r["material"]
        key[f"{m}_m_e"] = r["m_e"]
        key[f"{m}_m_h"] = r["m_h"]
        key[f"{m}_mu"] = r["mu"]
        key[f"{m}_E_b_rel_meV"] = r["E_b_rel_meV"]

    json.dump({"materials": MATERIALS, "n_occ": N_OCC, "dk": 1e-3,
               "k_point": "R = pi/a (1,1,1)", "directions": "[100],[010],[001] averaged",
               "model": "Kashikar-13"}, open(f"{stage}/scan_config.json", "w"), indent=2)

    spec = {
        "theme": "theme_I_exciton",
        "subtask": "effective-mass map + Wannier-Mott E_b (9 materials)",
        "physics_method": ("band-edge effective mass m*/m0 = (hbar^2/m0)/(d2E/dk2) at R "
                           "(Kashikar-13); Wannier-Mott E_b = (mu/m0)/eps_r^2 * Ry"),
        "mode": "Production", "retroactive": False,
        "convergence": {"dk": [2e-2, 1e-2, 5e-3, 1e-3], "directions": ["100", "110", "111"],
                        "note": "single-point curvature at R; dk & direction-anisotropy converged"},
        "outputs": [(f"{stage}/exciton_9materials.csv", "raw/exciton_9materials.csv")],
        "inputs": [(KAS13, "kashikar13_params_9materials.json"),
                   (f"{stage}/scan_config.json", "scan_config.json")],
        "key_numbers": key,
        "references": ["Yang et al. 2017 PRB 96 035301", "Tanaka et al. 2003 SSC 127 619",
                       "Cho et al. 2019 (arXiv:1908.09436, GW-BSE)",
                       "Kashikar, Gupta, Nanda 2021 (arXiv:2101.08562)"],
        "notes": ("PRIMARY = TB effective masses (reliable, publishable). SECONDARY = E_b "
                  "with TB-optical eps_inf is RELATIVE-TREND only (Blount-limited; Cl unphysical). "
                  "Absolute E_b deferred to option (c): external DFT/exp eps_inf input."),
        "readme": ("# Theme I: effective-mass map + Wannier-Mott exciton binding (9 cubic CsBX3)\n\n"
                   "Primary: TB band-edge effective masses m_e,m_h,mu (reliable). Secondary: E_b "
                   "(relative trend only; TB-optical eps_inf is Blount-limited).\n\n"
                   "Reproduce: OMP_NUM_THREADS=1 PYTHONPATH=src python scripts/scan_exciton_9materials.py production\n"),
        "cli": "OMP_NUM_THREADS=1 PYTHONPATH=src python scripts/scan_exciton_9materials.py production",
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
    ap.add_argument("--outdir", default="results/exciton")
    args = ap.parse_args()
    if args.mode == "convergence":
        run_convergence(f"{args.outdir}/convergence")
    elif args.mode == "scan":
        run_scan(args.outdir)
    else:
        run_production()
