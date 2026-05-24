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
  Strain-Induced Effects in Semiconductors*, Wiley (1974).  Perovskite strain
  context: A. Buin et al., Nano Lett. 14, 6281 (2014); M. Grumet et al., PRB 98,
  155143 (2018).

Note on the R point: at R = (pi/a, pi/a, pi/a) the Bloch phases are pinned to pi
independent of the lattice constant, so the *R-point* gap depends only on the
(scaled) hopping integrals -- the lattice-constant change enters elsewhere in
the band structure but not in this gap; the strain response here is therefore
the Harrison hopping renormalisation.

Honesty / scope: this is a **SK-TB + Harrison-scaling ESTIMATE**.  The structural
behaviour (epsilon=0 recovery, linearity, sign) is rigorous within the model;
the absolute deformation-potential magnitude is approximate (Harrison scaling of
a DFT-fitted TB model is crude) and is NOT claimed to match DFT/experiment
quantitatively -- it requires comparison to first-principles a_g (not asserted
here).  Reported as a model estimate with the approximation flagged.
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
