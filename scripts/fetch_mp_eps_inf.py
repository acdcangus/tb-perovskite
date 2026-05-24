#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 tk
"""Theme I (C-2): fetch Materials Project DFPT eps_inf for the 9 cubic CsBX3 and
merge into data/parameters/eps_inf_external.json (adds an eps_inf_MP_DFPT block per
material, alongside the existing web-research eps_inf). API key never logged/written.
Usage: PYTHONPATH=src python scripts/fetch_mp_eps_inf.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from perovskite_tb import materials_project as mp   # noqa: E402

MATERIALS = ["CsGeCl3", "CsGeBr3", "CsGeI3", "CsSnCl3", "CsSnBr3", "CsSnI3",
             "CsPbCl3", "CsPbBr3", "CsPbI3"]
JSON = "data/parameters/eps_inf_external.json"


def main():
    res = mp.fetch_all(MATERIALS)
    db = json.load(open(JSON))
    db["_KEY_FINDING_C"] = (
        "Option C' (Materials Project DFPT eps_inf): single-method, consistent across "
        "materials -> RELATIVE E_b trend is maximally defensible. BUT MP eps_inf is the "
        "BARE electronic dielectric (no phonon/ionic contribution), i.e. eps_inf < eps_eff, "
        "so absolute E_b is an UPPER BOUND (overestimate). Also MP computed the DFPT "
        "dielectric only for certain phases (cubic for some, ortho/rhombo/monoclinic for "
        "others); mu here is cubic-phase, so eps_inf is used as a ~phase-insensitive proxy "
        "(phase recorded per material). Key never stored; provenance = mp-id + URL only."
    )
    n_found = 0
    for f in MATERIALS:
        r = res.get(f, {})
        rec = db["materials"].setdefault(f, {})
        if r.get("eps_inf_scalar") is not None:
            n_found += 1
            rec["eps_inf_MP_DFPT"] = {
                "value": r["eps_inf_scalar"], "mp_id": r["mp_id"],
                "spacegroup": r.get("spacegroup"), "crystal_system": r.get("crystal_system"),
                "eps_total": r.get("eps_total_scalar"), "method": r["method"],
                "source_url": r["source_url"], "phase_note": r["phase_note"],
            }
        else:
            rec["eps_inf_MP_DFPT"] = {"value": None, "status": r.get("status", "unknown"),
                                      "phase_note": r.get("phase_note", "")}
        print(f"{f}: MP eps_inf = {r.get('eps_inf_scalar')} "
              f"({r.get('spacegroup')}, {r.get('mp_id')})", flush=True)
    json.dump(db, open(JSON, "w"), indent=2)
    print(f"--- {n_found}/9 materials got MP DFPT eps_inf; wrote {JSON} ---", flush=True)


if __name__ == "__main__":
    main()
