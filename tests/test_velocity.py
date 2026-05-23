"""Validate analytic velocity operators dH/dk against finite differences.

The analytic derivatives in ``velocity.py`` must match a central finite
difference of the corresponding Hamiltonian builder to high precision, at
generic (low-symmetry) k.  This guards the g-factor / optical modules that
consume the velocity operator.
"""

import numpy as np
import pytest

from perovskite_tb import models_kashikar as mk
from perovskite_tb import models_nestoklon as mn
from perovskite_tb import velocity as vel
from perovskite_tb.io_params import get_material, load_parameter_file

K13 = "data/parameters/kashikar2021_cubic_13orb.json"
K4 = "data/parameters/kashikar2021_cubic_4orb.json"
NES = "data/parameters/nestoklon2021_CsPbI3.json"


@pytest.mark.parametrize("material", ["CsPbI3", "CsSnI3", "CsGeCl3"])
@pytest.mark.parametrize("alpha", [0, 1, 2])
def test_kashikar13_velocity_matches_fd(material, alpha):
    m = get_material(load_parameter_file(K13), material)
    p, a = m["params"], m["a"]
    k = np.array([0.13, -0.21, 0.37]) * (2 * np.pi / a)  # generic k
    builder = lambda kk: mk.kashikar13_hamiltonian(kk, p, a)  # noqa: E731
    ana = vel.dH_dk_kashikar13(k, p, a, alpha)
    num = vel.dH_dk_numerical(builder, k, alpha)
    assert np.allclose(ana, num, atol=1e-5), f"{material} a={alpha}: max {np.max(np.abs(ana-num)):.2e}"
    assert np.allclose(ana, ana.conj().T, atol=1e-10)  # Hermitian


@pytest.mark.parametrize("alpha", [0, 1, 2])
def test_kashikar4_velocity_matches_fd(alpha):
    m = get_material(load_parameter_file(K4), "CsPbBr3")
    p, a = m["params"], m["a"]
    k = np.array([0.05, 0.29, -0.4]) * (2 * np.pi / a)
    builder = lambda kk: mk.kashikar4_hamiltonian(kk, p, a)  # noqa: E731
    ana = vel.dH_dk_kashikar4(k, p, a, alpha)
    num = vel.dH_dk_numerical(builder, k, alpha)
    assert np.allclose(ana, num, atol=1e-5)


@pytest.mark.parametrize("pset", ["sp3", "sp3d5sstar", "experiment_corrected"])
@pytest.mark.parametrize("alpha", [0, 1, 2])
def test_nestoklon_velocity_matches_fd(pset, alpha):
    m = get_material(load_parameter_file(NES), parameter_set=pset)
    p, a, basis = m["params"], m["a"], m["basis"]
    k = np.array([0.11, -0.23, 0.31]) * (2 * np.pi / a)
    builder = mn.make_builder(p, a, basis)
    dHdk = vel.make_dH_dk_nestoklon(p, a, basis)
    ana = dHdk(k, alpha)
    num = vel.dH_dk_numerical(builder, k, alpha)
    assert np.allclose(ana, num, atol=1e-5), f"{pset} a={alpha}: max {np.max(np.abs(ana-num)):.2e}"
    assert np.allclose(ana, ana.conj().T, atol=1e-10)
