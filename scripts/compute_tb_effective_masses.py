# SPDX-License-Identifier: MIT
# Copyright (c) 2026 tk
"""Compute band-edge effective masses m*/m0 for the 9 CsBX3 from the core TB.

Uses bandstructure.effective_mass (parabolic fit of E(k) around the R-point band
edges of the Kashikar-13 model).  These masses are TB outputs (no fabrication)
and feed the TB-driven Frohlich polaron alpha (spec F6, T1-3).  Output carries
provenance metadata (commit, parameter file) per docs/data-management.md.

Run from the repo root:  python scripts/compute_tb_effective_masses.py
Writes: results/tb_effective_masses.json
"""

from __future__ import annotations

import datetime as _dt
import json
import subprocess

import numpy as np

from perovskite_tb import bandstructure as bs
from perovskite_tb import models_kashikar as mk
from perovskite_tb.io_params import get_material, load_parameter_file

K13 = "data/parameters/kashikar2021_cubic_13orb.json"
MATERIALS = ["CsGeCl3", "CsGeBr3", "CsGeI3", "CsSnCl3", "CsSnBr3", "CsSnI3",
             "CsPbCl3", "CsPbBr3", "CsPbI3"]
N_FILLED = 20  # 26-band spinful Kashikar-13: CBM = band 20, VBM = band 19


def _commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
    except Exception:
        return "unknown"


def main() -> None:
    data = load_parameter_file(K13)
    rows = {}
    for name in MATERIALS:
        m = get_material(data, name)
        p, a = m["params"], m["a"]
        H = lambda k: mk.kashikar13_hamiltonian(np.asarray(k, float), p, a)  # noqa: E731
        R = np.array([np.pi / a] * 3)
        me = bs.effective_mass(H, R, N_FILLED, dk=1e-3)
        mh = bs.effective_mass(H, R, N_FILLED - 1, dk=1e-3)
        rows[name] = {
            "a_Angstrom": round(a, 4),
            "m_e_rel": round(me["mean"], 4),
            "m_h_rel_magnitude": round(abs(mh["mean"]), 4),
            "isotropic": bool(np.allclose([me["100"], me["110"], me["111"]],
                                          me["mean"], rtol=3e-3)),
        }
        print(f"{name:9s}  m_e*={rows[name]['m_e_rel']:.4f}  "
              f"m_h*={rows[name]['m_h_rel_magnitude']:.4f}  "
              f"isotropic={rows[name]['isotropic']}")

    out = {
        "_README": "Band-edge effective masses m*/m0 computed from the core "
                   "Kashikar-13 TB (parabolic fit at the R point). TB outputs, "
                   "not literature values. Used for the TB-driven Frohlich alpha.",
        "_provenance": {
            "parameter_file": K13,
            "model": "kashikar2021_cubic_13orb (arXiv:2101.08562)",
            "method": "bandstructure.effective_mass, dk=1e-3 /Angstrom, 7-pt parabola at R",
            "commit": _commit(),
            "generated_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        },
        "effective_masses": rows,
    }
    with open("results/tb_effective_masses.json", "w") as f:
        json.dump(out, f, indent=2)
    print("wrote results/tb_effective_masses.json")


if __name__ == "__main__":
    main()
