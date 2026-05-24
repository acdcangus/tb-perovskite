"""V&V for bandengr.py (spec F12): hydrostatic strain band engineering.

Structural anchors (rigorous within the SK-TB + Harrison model):
  * epsilon=0 recovers the unstrained R-point gap.
  * Harrison scaling: t_* -> t_*(1+eps)^-2 exactly (on-site/SOC unchanged).
  * E_g(eps) is linear for small eps (well-defined deformation potential),
    with opposite sign for tension vs compression.
The absolute deformation potential is a model estimate (flagged), not asserted
against DFT.
"""

import json

import numpy as np
import pytest

from perovskite_tb import bandengr
from perovskite_tb.io_params import get_material, load_parameter_file

K13 = "data/parameters/kashikar2021_cubic_13orb.json"
STRAIN_BENCH = "data/parameters/strain_benchmark.json"
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


def test_strain_gap_sensitivity_lit():
    """T1-2: compare the core-TB pressure coefficient to verified experiment.

    SIGN (rigorous, verified): tensile strain RAISES the gap (dEg/deps > 0), i.e.
    dEg/dP < 0 -- the lead-halide red-shift under pressure (Pieniazek 2023; CsPbI3
    DFT). MAGNITUDE (order only): the cubic-frozen TB overestimates because it
    lacks octahedral-tilting pressure relief; only sign + order are claimed.
    """
    bench = json.load(open(STRAIN_BENCH))
    B = bench["cubic_bulk_modulus_GPa"]
    exp = bench["experimental_pressure_coefficient"]["dEg_dP_meV_per_GPa"]
    exp_mag_max = max(abs(v) for v in exp.values())  # ~41 meV/GPa

    for name in ("CsPbI3", "CsPbBr3", "CsPbCl3"):
        p, a = _mat(name)
        # (1) sign: tensile raises gap
        ag = bandengr.hydrostatic_deformation_potential(p, a)
        assert ag > 0, f"{name}: expected dEg/deps > 0 (tensile raises gap), got {ag}"
        # (2) pressure coefficient is negative (gap drops under pressure) = exp sign
        dEdP = bandengr.pressure_coefficient(p, a, B[name])
        assert dEdP < 0, f"{name}: expected dEg/dP < 0, got {dEdP:.1f} meV/GPa"
        # (3) same order of magnitude as experiment (within ~20x; TB overestimates)
        ratio = abs(dEdP) / exp_mag_max
        assert 1.0 < ratio < 20.0, \
            f"{name}: |dEg/dP|={abs(dEdP):.0f} meV/GPa, ratio to exp={ratio:.1f} (expect 1-20x)"

    # consistency: pressure_coefficient == a_g*(-1/(3B)) by construction
    p, a = _mat("CsPbI3")
    ag = bandengr.hydrostatic_deformation_potential(p, a)
    assert np.isclose(bandengr.pressure_coefficient(p, a, 9.870),
                      ag * 1000.0 * (-1.0 / (3.0 * 9.870)), rtol=1e-9)
