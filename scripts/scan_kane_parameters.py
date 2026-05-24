#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 tk
"""Theme A / A6 -- TB-derived Kane parameter P for the 9 CsBX3 (+ Nestoklon CsPbI3).

Extracts the bare Kane momentum parameter P (eV.A) from the analytic TB velocity
operator at the R point (kane_parameter.extract_kane_parameter), making the
g-factor prediction fully TB-based (both Delta and P from the Hamiltonian).

Output: results/g_factors/kane_parameters.csv
"""

from __future__ import annotations

import csv
import os

import numpy as np

from perovskite_tb import models_kashikar as mk
from perovskite_tb import models_nestoklon as mn
from perovskite_tb import velocity as vel
from perovskite_tb.io_params import get_material, load_parameter_file
from perovskite_tb.kane_parameter import extract_kane_parameter

OUTDIR = "results/g_factors"
MATS = ["CsGeCl3", "CsGeBr3", "CsGeI3", "CsSnCl3", "CsSnBr3", "CsSnI3",
        "CsPbCl3", "CsPbBr3", "CsPbI3"]
P_UNIVERSAL = 6.8


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    rows = []
    d = load_parameter_file("data/parameters/kashikar2021_cubic_13orb.json")
    for mat in MATS:
        m = get_material(d, mat)
        p, a = m["params"], m["a"]
        kR = np.array([np.pi / a] * 3)
        H = mk.kashikar13_hamiltonian(kR, p, a)
        dz = vel.dH_dk_kashikar13(kR, p, a, 2)
        r = extract_kane_parameter(H, dz, 20, 3, 13)
        rows.append({"material": mat, "model": "kashikar13",
                     "P_raw_eVA": round(r["P_raw"], 3),
                     "sin2theta": round(r["sin2theta"], 3),
                     "P_bare_eVA": round(r["P_bare"], 3),
                     "P_universal_eVA": P_UNIVERSAL,
                     "P_bare/P_universal": round(r["P_bare"] / P_UNIVERSAL, 3)})

    dn = load_parameter_file("data/parameters/nestoklon2021_CsPbI3.json")
    for ps in ["sp3d5sstar", "experiment_corrected"]:
        m = get_material(dn, parameter_set=ps)
        p, a, basis = m["params"], m["a"], m["basis"]
        kR = np.array([np.pi / a] * 3)
        H = mn.make_builder(p, a, basis)(kR)
        dz = vel.make_dH_dk_nestoklon(p, a, basis)(kR, 2)
        r = extract_kane_parameter(H, dz, 26, 3, 40)
        rows.append({"material": "CsPbI3", "model": f"nestoklon_{ps}",
                     "P_raw_eVA": round(r["P_raw"], 3),
                     "sin2theta": round(r["sin2theta"], 3),
                     "P_bare_eVA": round(r["P_bare"], 3),
                     "P_universal_eVA": P_UNIVERSAL,
                     "P_bare/P_universal": round(r["P_bare"] / P_UNIVERSAL, 3)})

    path = os.path.join(OUTDIR, "kane_parameters.csv")
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"wrote {path}")
    for r in rows:
        print(f"  {r['material']:8s} {r['model']:22s} P_bare={r['P_bare_eVA']:.2f} "
              f"(sin2θ={r['sin2theta']:.3f}, P/Puniv={r['P_bare/P_universal']:.2f})")
    return rows


if __name__ == "__main__":
    main()
