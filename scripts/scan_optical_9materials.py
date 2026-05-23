#!/usr/bin/env python3
"""Phase 1.5 / B5 -- optical response of all 9 cubic CsBX3 (Kashikar 13-orbital).

Computes eps(omega), alpha(omega), n(omega) and eps_inf for the 9 materials,
verifying that each absorption edge tracks that material's TB band gap.  Outputs
a summary CSV and a combined eps_i spectrum plot.

Note: Kashikar reproduces mBJ+SOC gaps (smaller than experiment); the absolute
intensities are limited by the TB f-sum incompleteness (Blount 1962). The edge
positions and relative trends are the reliable outputs.
"""

from __future__ import annotations

import csv
import os

import numpy as np

from perovskite_tb import models_kashikar as mk
from perovskite_tb import velocity as vel
from perovskite_tb.io_params import get_material, load_parameter_file
from perovskite_tb.optical import compute_dielectric

OUTDIR = "results/optical"
MATS = ["CsGeCl3", "CsGeBr3", "CsGeI3", "CsSnCl3", "CsSnBr3", "CsSnI3",
        "CsPbCl3", "CsPbBr3", "CsPbI3"]
COLOR = {"Ge": "C2", "Sn": "C1", "Pb": "C0"}


def _gap(p, a):
    kR = np.array([np.pi / a] * 3)
    ev = np.sort(np.linalg.eigvalsh(mk.kashikar13_hamiltonian(kR, p, a)).real)
    return ev[20] - ev[19]


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    data = load_parameter_file("data/parameters/kashikar2021_cubic_13orb.json")
    omega = np.linspace(0.1, 6.0, 280)
    rows = []
    fig, ax = plt.subplots(figsize=(8, 5))
    for mat in MATS:
        m = get_material(data, mat)
        p, a = m["params"], m["a"]
        Eg = _gap(p, a)
        builder = lambda k, p=p, a=a: mk.kashikar13_hamiltonian(k, p, a)  # noqa: E731
        dhdk = lambda k, al, p=p, a=a: vel.dH_dk_kashikar13(k, p, a, al)  # noqa: E731
        res = compute_dielectric(builder, dhdk, a, 20, omega, n_kpts=8, smearing_eta=0.05)
        ei = res["eps_imag"]
        thr = 0.05 * ei.max()
        edge = float(omega[np.argmax((ei > thr) & (omega > max(0.3, Eg - 0.3)))])
        B = mat[2:4]
        ax.plot(omega, ei, color=COLOR[B], lw=1.2, alpha=0.8,
                label=f"{mat} (Eg={Eg:.2f})")
        rows.append({"material": mat, "Eg_TB": round(Eg, 3),
                     "abs_edge_eV": round(edge, 3),
                     "eps_inf": round(float(res["eps_real"][0]), 3),
                     "eps_i_max": round(float(ei.max()), 3),
                     "peak_eV": round(float(omega[np.argmax(ei)]), 3)})
        print(f"  {mat:9s} Eg={Eg:.2f} edge={edge:.2f} eps_inf={rows[-1]['eps_inf']:.2f}")

    ax.set_xlabel("Photon energy (eV)"); ax.set_ylabel(r"$\varepsilon_2$")
    ax.set_title("Imaginary dielectric function of CsBX$_3$ (Kashikar 13-orb, TB-IPA)")
    ax.legend(fontsize=7, ncol=3); ax.grid(alpha=0.3); ax.set_xlim(0, 6)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, "9material_eps_imag.png"), dpi=150)
    plt.close(fig)

    csv_path = os.path.join(OUTDIR, "9material_optical_summary.csv")
    with open(csv_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"wrote {csv_path} and 9material_eps_imag.png")


if __name__ == "__main__":
    main()
