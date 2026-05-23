#!/usr/bin/env python3
"""Regenerate every band-structure figure under results/.

Reproducible entry point: regenerates the Kashikar (13- and 4-orbital, 9
materials each) and Nestoklon (3 parameter sets) band structures, each with a
reproducibility-metadata JSON sidecar.

Usage:
    PYTHONPATH=src python scripts/generate_all_bands.py
"""

from __future__ import annotations

import subprocess
import sys

KASHIKAR_MATERIALS = ["CsGeCl3", "CsGeBr3", "CsGeI3", "CsSnCl3", "CsSnBr3",
                      "CsSnI3", "CsPbCl3", "CsPbBr3", "CsPbI3"]
NESTOKLON_SETS = ["sp3", "sp3d5sstar", "experiment_corrected"]
CONFIG = "configs/cubic_MRGXM.json"


def run(args):
    print("  $ python -m perovskite_tb", *args)
    subprocess.run([sys.executable, "-m", "perovskite_tb", *args], check=True)


def main():
    for label, pf in [("kashikar13", "data/parameters/kashikar2021_cubic_13orb.json"),
                      ("kashikar4", "data/parameters/kashikar2021_cubic_4orb.json")]:
        print(f"# {label}")
        for mat in KASHIKAR_MATERIALS:
            run(["band", "--params", pf, "--material", mat, "--config", CONFIG,
                 "--out", f"results/{label}/{mat}.png"])

    print("# nestoklon")
    for ps in NESTOKLON_SETS:
        run(["band", "--params", "data/parameters/nestoklon2021_CsPbI3.json",
             "--parameter-set", ps, "--config", CONFIG,
             "--out", f"results/nestoklon/CsPbI3_{ps}.png"])
    print("done.")


if __name__ == "__main__":
    main()
