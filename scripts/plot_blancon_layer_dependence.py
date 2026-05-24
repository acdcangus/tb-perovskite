# SPDX-License-Identifier: MIT
# Copyright (c) 2026 tk
"""Plot the F5 quantum-confinement trend: TB slab E_g(N) vs Blancon 2018.

Compares the core Kashikar-13 CsPbI3 slab confinement gap E_g(N) (hard-barrier
idealisation) to the verified free-particle band gaps of the 2D-RP series
(BA)2(MA)_{n-1}Pb_nI_{3n+1} (Blancon et al., Nat. Commun. 9, 2254 (2018)).

This is a TREND (confinement-decay shape) comparison only; absolute gaps differ
(inorganic CsPbI3 analog vs MAPbI3-based RP; SK-TB caveat).  Outputs:
    results/figures/blancon_E_g_n.png

Run from the repo root:  python scripts/plot_blancon_layer_dependence.py
"""

from __future__ import annotations

import json
import subprocess

import numpy as np

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from perovskite_tb import models_kashikar as mk  # noqa: E402
from perovskite_tb import slab  # noqa: E402
from perovskite_tb.io_params import get_material, load_parameter_file  # noqa: E402

K13 = "data/parameters/kashikar2021_cubic_13orb.json"
BLANCON = "data/parameters/blancon2018_2drp_gaps.json"


def _commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
    except Exception:
        return "unknown"


def main() -> None:
    m = get_material(load_parameter_file(K13), "CsPbI3")
    p, a = m["params"], m["a"]
    kx = ky = np.pi / a
    Ns = np.arange(1, 9)
    tb = np.array([slab.slab_gap(p, a, kx, ky, int(N)) for N in Ns])
    R = np.array([np.pi / a] * 3)
    ev = np.linalg.eigvalsh(mk.kashikar13_hamiltonian(R, p, a))
    e_inf_tb = float(ev[slab.N_OCC_PER_CELL] - ev[slab.N_OCC_PER_CELL - 1])

    bj = json.load(open(BLANCON))["free_particle_gaps_eV"]
    exp_n = np.array([int(k[1:]) for k in bj])
    exp_g = np.array([v["value"] for v in bj.values()])
    exp_e = np.array([v["uncertainty"] for v in bj.values()])
    e_inf_exp = 1.675  # free-particle 3D baseline (MAPbI3), midpoint of [1.60,1.70]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4))

    ax1.plot(Ns, tb, "o-", label="TB slab (CsPbI3, core Kashikar-13)")
    ax1.axhline(e_inf_tb, ls=":", color="C0", lw=1, label=f"TB 3D limit {e_inf_tb:.3f} eV")
    ax1.errorbar(exp_n, exp_g, yerr=exp_e, fmt="s", color="C3",
                 label="Blancon 2018 free-particle gap")
    ax1.axhline(e_inf_exp, ls=":", color="C3", lw=1, label=f"3D baseline {e_inf_exp:.2f} eV")
    ax1.set_xlabel("layer number n"); ax1.set_ylabel(r"$E_g$ (eV)")
    ax1.set_title("Absolute gaps (differ: material + SK-TB caveat)")
    ax1.legend(fontsize=7); ax1.grid(alpha=0.3)

    # log-log of the confinement shift Delta = E_g - E_inf
    dtb = tb[:5] - e_inf_tb
    dexp = exp_g - e_inf_exp
    ax2.loglog(Ns[:5], dtb, "o-", label="TB (CsPbI3 slab)")
    ax2.loglog(exp_n, dexp, "s", color="C3", label="Blancon 2018")
    p_tb = -np.polyfit(np.log(Ns[:5]), np.log(dtb), 1)[0]
    p_exp = -np.polyfit(np.log(exp_n), np.log(dexp), 1)[0]
    ax2.set_xlabel("layer number n"); ax2.set_ylabel(r"$\Delta E_g = E_g(n)-E_\infty$ (eV)")
    ax2.set_title(f"Confinement decay: $p_{{TB}}$={p_tb:.2f}, $p_{{exp}}$={p_exp:.2f}")
    ax2.legend(fontsize=8); ax2.grid(alpha=0.3, which="both")

    fig.suptitle(f"F5 confinement trend  |  commit {_commit()}  |  "
                 "TREND comparison only (no absolute claim)", fontsize=9)
    fig.tight_layout()
    out = "results/figures/blancon_E_g_n.png"
    fig.savefig(out, dpi=130)
    print(f"wrote {out}  (p_TB={p_tb:.3f}, p_exp={p_exp:.3f})")


if __name__ == "__main__":
    main()
