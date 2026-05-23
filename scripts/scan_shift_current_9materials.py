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
from perovskite_tb.io_params import get_material, load_parameter_file  # noqa: E402

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
    gaps = {}
    for mat in MATERIALS:
        p, a = load(mat)
        ev = np.sort(np.linalg.eigvalsh(
            __import__("perovskite_tb.models_kashikar", fromlist=["kashikar13_hamiltonian"])
            .kashikar13_hamiltonian(np.array([1, 1, 1]) * np.pi / a, p, a)).real)
        gaps[mat] = float(ev[N_OCC] - ev[N_OCC - 1])
        for d in deltas:
            results[(mat, d)] = sigma_zzz(p, a, d, omega, n_kpts, eta)
        peak = results[(mat, 0.15)][np.argmax(np.abs(results[(mat, 0.15)]))]
        print(f"{mat}: gap(R)={gaps[mat]:.3f} eV  sigma_zzz peak(delta=0.15)={peak:+.3e}")

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
        w.writerow(["material", "gap_R_eV"] + [f"peak_d{d}" for d in deltas]
                   + [f"peak_omega_d{d}" for d in deltas])
        for mat in MATERIALS:
            row = [mat, f"{gaps[mat]:.4f}"]
            for d in deltas:
                s = results[(mat, d)]; ip = np.argmax(np.abs(s))
                row.append(f"{s[ip]:.6e}")
            for d in deltas:
                s = results[(mat, d)]; ip = np.argmax(np.abs(s))
                row.append(f"{omega[ip]:.4f}")
            w.writerow(row)
    print(f"scan -> {outdir}  (settings n_kpts={n_kpts}, eta={eta}, deltas={deltas})")
    return results, gaps


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["convergence", "scan"])
    ap.add_argument("--outdir", default="results/shift_current")
    ap.add_argument("--n_kpts", type=int, default=48)
    ap.add_argument("--eta", type=float, default=0.10)
    args = ap.parse_args()
    if args.mode == "convergence":
        run_convergence(f"{args.outdir}/convergence")
    else:
        run_scan(args.outdir, n_kpts=args.n_kpts, eta=args.eta)
