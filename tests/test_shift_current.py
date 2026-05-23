"""Shift-current (Theme F / F3) tests.

VALIDATED here:
  * Harrison distance scaling t(d)=t(d0)(d0/d)^eta;
  * the polar-displaced Nestoklon builder reduces *exactly* to the centrosymmetric
    base builder at delta=0 (so any non-vanishing sigma at delta=0 is a shift-vector
    bug, not a Hamiltonian bug);
  * time-reversal E(k)=E(-k) holds for the polar (delta>0) builder.

KNOWN ISSUE (xfail): the Abelian discrete shift vector does not give the required
centrosymmetric vanishing at delta=0 because the bands are Kramers-doubly-degenerate
(SOC); a non-Abelian (degenerate-subspace) shift vector is needed. See
src/perovskite_tb/shift_current.py docstring. Not falsified to pass.
"""

import numpy as np
import pytest

from perovskite_tb import models_nestoklon as mn
from perovskite_tb import shift_current as sc
from perovskite_tb import velocity as vel
from perovskite_tb.io_params import get_material, load_parameter_file

NES = "data/parameters/nestoklon2021_CsPbI3.json"


@pytest.fixture(scope="module")
def cspbi3():
    m = get_material(load_parameter_file(NES), parameter_set="experiment_corrected")
    return m["params"], m["a"], m["basis"]


def test_harrison_scaling():
    assert sc.harrison_scaled_hopping(2.0, 3.0, 3.0) == pytest.approx(2.0)
    # shorter bond -> larger |hopping|
    assert abs(sc.harrison_scaled_hopping(2.0, 3.0, 2.7)) > 2.0
    # eta=2 universal value
    assert sc.harrison_scaled_hopping(1.0, 2.0, 1.0, eta=2.0) == pytest.approx(4.0)


def test_polar_builder_reduces_to_base_at_zero(cspbi3):
    """delta=0 polar builder == centrosymmetric base Nestoklon builder (exactly)."""
    p, a, basis = cspbi3
    Hp, dHp = sc.make_polar_nestoklon_builders(p, a, basis, polar_displacement_z=0.0)
    Hb = mn.make_builder(p, a, basis)
    dHb = vel.make_dH_dk_nestoklon(p, a, basis)
    k = np.array([0.13, 0.21, 0.31]) * (2 * np.pi / a)
    assert np.allclose(Hp(k), Hb(k), atol=1e-12)
    assert np.allclose(dHp(k, 2), dHb(k, 2), atol=1e-12)


def test_polar_builder_breaks_inversion(cspbi3):
    """delta>0 modifies the Hamiltonian (inversion broken) but keeps TRS E(k)=E(-k)."""
    p, a, basis = cspbi3
    Hp, _ = sc.make_polar_nestoklon_builders(p, a, basis, polar_displacement_z=0.2)
    Hb = mn.make_builder(p, a, basis)
    k = np.array([0.1, 0.2, 0.3]) * (2 * np.pi / a)
    assert not np.allclose(Hp(k), Hb(k), atol=1e-6)          # inversion broken
    Ek = np.sort(np.linalg.eigvalsh(Hp(k)).real)
    Emk = np.sort(np.linalg.eigvalsh(Hp(-k)).real)
    assert np.allclose(Ek, Emk, atol=1e-10)                  # time-reversal


@pytest.mark.xfail(reason="Abelian shift vector invalid for Kramers-degenerate (SOC) "
                          "bands; needs non-Abelian treatment. Escalated to Cowork.",
                   strict=True)
def test_centrosymmetric_vanishes(cspbi3):
    """delta=0 must give sigma_zzz ~ 0 by centrosymmetry (currently FAILS -- Kramers)."""
    p, a, basis = cspbi3
    Hp, dHp = sc.make_polar_nestoklon_builders(p, a, basis, polar_displacement_z=0.0)
    omega = np.linspace(1.0, 4.0, 30)
    sig = sc.shift_current_zzz(Hp, dHp, a, 26, omega, n_kpts=6, smearing_eta=0.08)
    assert np.max(np.abs(sig)) < 1e-6
