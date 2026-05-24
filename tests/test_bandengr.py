"""V&V for bandengr.py (spec F12): hydrostatic strain band engineering.

Structural anchors (rigorous within the SK-TB + Harrison model):
  * epsilon=0 recovers the unstrained R-point gap.
  * Harrison scaling: t_* -> t_*(1+eps)^-2 exactly (on-site/SOC unchanged).
  * E_g(eps) is linear for small eps (well-defined deformation potential),
    with opposite sign for tension vs compression.
The absolute deformation potential is a model estimate (flagged), not asserted
against DFT.
"""

import numpy as np
import pytest

from perovskite_tb import bandengr
from perovskite_tb.io_params import get_material, load_parameter_file

K13 = "data/parameters/kashikar2021_cubic_13orb.json"
MATS = ["CsPbI3", "CsPbBr3", "CsSnI3", "CsGeCl3"]


def _mat(name):
    m = get_material(load_parameter_file(K13), name)
    return m["params"], m["a"]


def test_harrison_scaling_rule():
    p, _ = _mat("CsPbI3")
    sp = bandengr.strained_hopping_params(p, 0.01)
    s = (1.01) ** -2
    for k, v in p.items():
        if k.startswith("t_"):
            assert np.isclose(sp[k], v * s), f"{k} not scaled"
        else:
            assert sp[k] == v, f"{k} should be unchanged (on-site/SOC)"


def test_zero_strain_recovers_unstrained_gap():
    p, a = _mat("CsPbI3")
    g0 = bandengr.gap_at_R(p, a)
    gs = bandengr.gap_under_hydrostatic_strain(p, a, 0.0)
    assert np.isclose(g0, gs, atol=1e-12)
    assert np.isclose(g0, 0.6298, atol=1e-3)  # matches theme_F TB gap@R


@pytest.mark.parametrize("name", MATS)
def test_gap_linear_in_strain(name):
    p, a = _mat(name)
    g0 = bandengr.gap_at_R(p, a)
    ag = bandengr.hydrostatic_deformation_potential(p, a)
    # linear model E_g(eps) ~ g0 + ag*eps should hold for small eps
    for eps in (0.004, -0.004):
        g = bandengr.gap_under_hydrostatic_strain(p, a, eps)
        assert np.isclose(g, g0 + ag * eps, atol=0.02 * abs(ag) + 1e-4), \
            f"{name}: nonlinear at eps={eps}"
    assert abs(ag) > 1e-6  # gap does respond to strain


def test_tension_compression_opposite_sign():
    p, a = _mat("CsPbI3")
    g0 = bandengr.gap_at_R(p, a)
    g_tens = bandengr.gap_under_hydrostatic_strain(p, a, 0.01)
    g_comp = bandengr.gap_under_hydrostatic_strain(p, a, -0.01)
    assert np.sign(g_tens - g0) == -np.sign(g_comp - g0)


def test_deformation_potential_finite_all_materials():
    for name in MATS:
        p, a = _mat(name)
        ag = bandengr.hydrostatic_deformation_potential(p, a)
        assert np.isfinite(ag) and abs(ag) < 100.0  # eV/strain, sane magnitude
