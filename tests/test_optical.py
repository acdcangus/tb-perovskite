"""Optical (dielectric function) verification (Phase 1.5 / B3).

Verifiable for a TB model:
  * absorption edge of eps_i coincides with the band gap (sub-gap eps_i ~ 0);
  * cubic isotropy eps_xx = eps_yy = eps_zz;
  * Kramers-Kronig real part is finite with eps_r(low omega) > 1.

Documented limitation (NOT asserted as =1): the f-sum rule is violated by a TB
model because dH/dk omits intra-atomic currents (Blount 1962) -- the same
incompleteness as the g-factor; the captured fraction is ~0.2 and is reported,
not forced.
"""

import numpy as np
import pytest

from perovskite_tb import models_nestoklon as mn
from perovskite_tb import velocity as vel
from perovskite_tb.io_params import get_material, load_parameter_file
from perovskite_tb.optical import compute_dielectric, f_sum_rule_check

NES = "data/parameters/nestoklon2021_CsPbI3.json"


@pytest.fixture(scope="module")
def cspbi3_dielectric():
    m = get_material(load_parameter_file(NES), parameter_set="experiment_corrected")
    p, a, basis = m["params"], m["a"], m["basis"]
    Hfn = mn.make_builder(p, a, basis)
    dHdk = vel.make_dH_dk_nestoklon(p, a, basis)
    omega = np.linspace(0.3, 5.0, 95)
    res = compute_dielectric(Hfn, lambda k, al: dHdk(k, al), a, 26, omega,
                             n_kpts=6, smearing_eta=0.06)
    return res, a


def test_absorption_edge_matches_gap(cspbi3_dielectric):
    """eps_i is negligible below the 1.65 eV gap and large well above it."""
    res, _a = cspbi3_dielectric
    om, ei = res["omega"], res["eps_imag"]
    ei_below = ei[om < 1.3].max()       # below the gap
    ei_above = ei[(om > 2.5) & (om < 4.5)].max()  # above the gap
    assert ei_below < 0.05 * ei_above, f"sub-gap {ei_below:.3f} vs above {ei_above:.3f}"


def test_cubic_isotropy(cspbi3_dielectric):
    res, _a = cspbi3_dielectric
    t = res["eps_imag_tensor"]
    assert np.max(np.abs(t[0] - t[1])) < 1e-9
    assert np.max(np.abs(t[0] - t[2])) < 1e-9


def test_kramers_kronig_real_part(cspbi3_dielectric):
    res, _a = cspbi3_dielectric
    er = res["eps_real"]
    assert np.all(np.isfinite(er))
    assert er[0] > 1.0  # static/low-frequency dielectric constant exceeds 1


def test_f_sum_rule_tb_incomplete():
    """Document (not force) the TB f-sum rule violation (~0.2 of the full value).

    The ratio < 1 reflects the missing intra-atomic oscillator strength
    (Blount 1962), consistent with the g-factor incompleteness.
    """
    m = get_material(load_parameter_file(NES), parameter_set="experiment_corrected")
    p, a, basis = m["params"], m["a"], m["basis"]
    Hfn = mn.make_builder(p, a, basis)
    dHdk = vel.make_dH_dk_nestoklon(p, a, basis)
    omega = np.linspace(0.3, 35.0, 350)
    res = compute_dielectric(Hfn, lambda k, al: dHdk(k, al), a, 26, omega, n_kpts=6)
    fs = f_sum_rule_check(omega, res["eps_imag"], 26, a ** 3)
    # captured fraction is positive and well below 1 (TB incompleteness).
    assert 0.05 < fs["ratio"] < 0.6, f"ratio={fs['ratio']:.3f}"
