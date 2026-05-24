# SPDX-License-Identifier: MIT
# Copyright (c) 2026 tk
"""Strain band engineering: hydrostatic deformation of the gap (spec F12).

Applies uniform (hydrostatic) strain to the cubic Kashikar-13 SK-TB model and
computes the band-gap response E_g(epsilon) and the hydrostatic deformation
potential a_g = dE_g/d(epsilon) at the R point.

Method / source:
* Strain scaling of the two-centre hopping integrals follows the **Harrison
  d^-2 universal rule** (W. A. Harrison, *Electronic Structure and the
  Properties of Solids*, Freeman, 1980): V(d) = V_0 (d_0/d)^2, so under a
  uniform strain epsilon (all bond lengths -> d_0(1+epsilon)) every hopping
  scales by (1+epsilon)^-2.  On-site energies and the (atomic) SOC lambda are
  strain-independent.
* Deformation-potential framework: G. L. Bir, G. E. Pikus, *Symmetry and
  Strain-Induced Effects in Semiconductors*, Wiley (1974).
* Experimental band-gap pressure coefficient (sign/magnitude benchmark):
  A. Pieniazek et al., "Bandgap Pressure Coefficient of a CH3NH3PbI3 Thin Film
  Perovskite", J. Phys. Chem. Lett. 14, 6470 (2023), DOI 10.1021/acs.jpclett.3c01258
  -- dEg/dP < 0 (gap decreases under pressure: -13.3 meV/GPa at 120 K to
  -36.3 at 40 K; DFT 0 K -41), verified web 2026-05-24.
* Cubic bulk modulus (for the dEg/deps -> dEg/dP conversion): Y. Liu et al.,
  Molecules 28, 7643 (2023), DOI 10.3390/molecules28227643 -- CsPbI3 9.87,
  CsPbBr3 13.36, CsPbCl3 16.01 GPa (verified 2026-05-24).

Citation correction (no-hallucination, 2026-05-24): earlier drafts cited
"Buin, Nano Lett. 14, 6281 (2014)" and "Grumet, PRB 98, 155143 (2018)" as the
strain/deformation-potential references.  Verified via web/crossref these are
NOT about strain deformation potentials -- Buin 2014 is "Materials Processing
Routes to Trap-Free Halide Perovskites" (defect/trap states) and Grumet 2018 is
"Beyond the quasiparticle approximation: Fully self-consistent GW calculations"
(a GW-method paper).  Both removed; the Pieniazek/Liu references above replace
them.

Note on the R point: at R = (pi/a, pi/a, pi/a) the Bloch phases are pinned to pi
independent of the lattice constant, so the *R-point* gap depends only on the
(scaled) hopping integrals -- the lattice-constant change enters elsewhere in
the band structure but not in this gap; the strain response here is therefore
the Harrison hopping renormalisation.

Honesty / scope: this is a **SK-TB + Harrison-scaling ESTIMATE**.  The structural
behaviour (epsilon=0 recovery, linearity) is rigorous within the model.

The SIGN is physically correct and matches experiment: the TB gives dEg/deps > 0
(tensile/expansion RAISES the gap, so compression LOWERS it), equivalently
dEg/dP < 0 -- the well-documented red-shift of lead-halide-perovskite gaps under
hydrostatic pressure (Pieniazek 2023; CsPbI3 DFT gap drops 1.85 -> 0.35 eV over
0-55 GPa).  This is because the VBM is the antibonding Pb-s / X-p state, which
rises under bond compression faster than the CBM.

The MAGNITUDE is overestimated and only order-of-magnitude.  Converted with the
cited cubic bulk moduli, the TB gives dEg/dP ~ -210 meV/GPa for CsPbX3, vs the
experimental MAPbI3 -13..-41 meV/GPa: TB is ~5-16x too steep.  The dominant
reason is physical, not just SK-TB crudeness: the cubic-frozen TB has NO
octahedral-tilting degree of freedom, so it captures only the (steep) bond-length
contribution, whereas real perovskites relieve pressure largely by tilting, which
partially compensates the gap change.  (Material also differs: CsPbI3 TB vs
MAPbI3 experiment.)  Absolute a_g is therefore NOT a quantitative match; only the
sign and order are claimed.  See tests/test_bandengr.py::test_strain_gap_sensitivity_lit.
"""

from __future__ import annotations

from typing import Mapping

import numpy as np

from . import models_kashikar as mk

N_OCC_13 = 20  # occupied bands of the spinful 26-band Kashikar-13 model


def strained_hopping_params(params: Mapping[str, float], eps: float) -> dict:
    """Hopping integrals under uniform strain (Harrison d^-2): t_* *= (1+eps)^-2.

    On-site energies (E_*) and SOC (lambda_SOC) are unchanged.
    """
    scale = (1.0 + eps) ** (-2)
    return {k: (v * scale if k.startswith("t_") else v) for k, v in params.items()}


def gap_at_R(params: Mapping[str, float], a: float, n_occ: int = N_OCC_13) -> float:
    """Fundamental gap E[n_occ] - E[n_occ-1] at the R point (eV)."""
    R = np.array([np.pi / a, np.pi / a, np.pi / a])
    ev = np.linalg.eigvalsh(mk.kashikar13_hamiltonian(R, params, a))
    return float(ev[n_occ] - ev[n_occ - 1])


def gap_under_hydrostatic_strain(params, a, eps, n_occ: int = N_OCC_13) -> float:
    """R-point gap under hydrostatic strain ``eps`` (Harrison-scaled hoppings)."""
    return gap_at_R(strained_hopping_params(params, eps), a * (1.0 + eps), n_occ)


def hydrostatic_deformation_potential(params, a, *, deps: float = 5e-3,
                                      n_occ: int = N_OCC_13) -> float:
    """a_g = dE_g/d(epsilon) at epsilon=0 (eV per unit strain), central difference.

    Positive epsilon = tensile (expansion).  SK-TB + Harrison estimate (see
    module docstring); absolute magnitude is approximate.
    """
    gp = gap_under_hydrostatic_strain(params, a, +deps, n_occ)
    gm = gap_under_hydrostatic_strain(params, a, -deps, n_occ)
    return (gp - gm) / (2.0 * deps)


def pressure_coefficient(params, a, bulk_modulus_GPa: float, *, deps: float = 5e-3,
                         n_occ: int = N_OCC_13) -> float:
    """Band-gap pressure coefficient dE_g/dP in meV/GPa from the TB a_g and B.

    Hydrostatic linear strain ``epsilon`` gives volumetric strain ``dV/V = 3*eps``
    and pressure ``P = -B*(dV/V) = -3 B eps``, so
        dE_g/dP = (dE_g/d eps) * (-1 / (3 B)) .
    With a_g in eV/strain and B in GPa, the result is in meV/GPa (negative for
    these perovskites: the gap drops under pressure).  ``bulk_modulus_GPa`` must
    come from a cited source (e.g. Liu et al., Molecules 28, 7643 (2023)).
    """
    a_g = hydrostatic_deformation_potential(params, a, deps=deps, n_occ=n_occ)  # eV/strain
    return (a_g * 1000.0) * (-1.0 / (3.0 * bulk_modulus_GPa))
