#!/usr/bin/env python3
"""Phase 1.5 / B2 -- dielectric function & absorption of CsPbI3.

Computes eps(omega), alpha(omega) (independent-particle, TB) and saves a plot to
results/optical/.  Demonstrates the absorption edge tracking the band gap.
Absolute intensities are limited by the TB f-sum incompleteness (Blount 1962);
see docs/optical-formulation.md.
"""

from __future__ import annotations

import os

import numpy as np

from perovskite_tb import models_nestoklon as mn
from perovskite_tb import velocity as vel
from perovskite_tb.io_params import get_material, load_parameter_file
from perovskite_tb.optical import compute_dielectric, f_sum_rule_check

OUTDIR = "results/optical"


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    m = get_material(load_parameter_file(
        "data/parameters/nestoklon2021_CsPbI3.json"), parameter_set="experiment_corrected")
    p, a, basis = m["params"], m["a"], m["basis"]
    Hfn = mn.make_builder(p, a, basis)
    dHdk = vel.make_dH_dk_nestoklon(p, a, basis)
    omega = np.linspace(0.3, 6.0, 300)
    res = compute_dielectric(Hfn, lambda k, al: dHdk(k, al), a, 26, omega,
                             n_kpts=12, smearing_eta=0.05)
    Eg = 1.65
    fs = f_sum_rule_check(omega, res["eps_imag"], 26, a ** 3)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.6))
    ax1.plot(omega, res["eps_real"], "C0-", label=r"$\varepsilon_1$ (real)")
    ax1.plot(omega, res["eps_imag"], "C3-", label=r"$\varepsilon_2$ (imag)")
    ax1.axvline(Eg, color="grey", ls="--", lw=0.8, label=f"$E_g$ = {Eg} eV")
    ax1.set_xlabel("Photon energy (eV)"); ax1.set_ylabel(r"$\varepsilon$")
    ax1.set_title("CsPbI$_3$ dielectric function (TB, independent particle)")
    ax1.legend(fontsize=8); ax1.grid(alpha=0.3)

    ax2.plot(omega, res["alpha"] / 1e4, "C2-")
    ax2.axvline(Eg, color="grey", ls="--", lw=0.8)
    ax2.set_xlabel("Photon energy (eV)")
    ax2.set_ylabel(r"$\alpha$ (10$^4$ cm$^{-1}$)")
    ax2.set_title("Absorption coefficient (edge tracks $E_g$)")
    ax2.grid(alpha=0.3)
    fig.suptitle("CsPbI$_3$ optical response (Nestoklon sp$^3$d$^5$s* ETB; "
                 f"f-sum captured ~{fs['ratio']:.0%}, TB-incomplete)")
    fig.tight_layout()
    path = os.path.join(OUTDIR, "CsPbI3_dielectric.png")
    fig.savefig(path, dpi=150); plt.close(fig)
    print(f"wrote {path}  (eps_inf~{res['eps_real'][0]:.2f}, f-sum ratio {fs['ratio']:.2f})")


if __name__ == "__main__":
    main()
