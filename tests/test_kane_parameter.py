"""TB-derived Kane parameter P verification (Theme A / A6).

Validated:
  * cubic isotropy P_x = P_y = P_z;
  * the CB cation-p_z weight sin^2(theta) = 1/3, matching the analytic cubic
    perovskite CB Bloch structure (Nestoklon 2023 SI Eq.S1b, sin(theta)=sqrt(1/3));
  * the sp3d5s* CsPbI3 bare Kane P lies within ~1.5 eV.A of Kirstein's universal
    6.8 eV.A.

Documented (not forced): TB-derived P from band-structure-fit Hamiltonians
underestimates the g-factor-effective 6.8 eV.A; the minimal Kashikar 13-orbital
basis underestimates more than the sp3d5s* basis.
"""

import numpy as np
import pytest

from perovskite_tb import models_kashikar as mk
from perovskite_tb import models_nestoklon as mn
from perovskite_tb import velocity as vel
from perovskite_tb.io_params import get_material, load_parameter_file
from perovskite_tb.kane_parameter import extract_kane_parameter, kane_parameter_anisotropy

K13 = "data/parameters/kashikar2021_cubic_13orb.json"
NES = "data/parameters/nestoklon2021_CsPbI3.json"


def _kashikar_PR(material):
    m = get_material(load_parameter_file(K13), material)
    p, a = m["params"], m["a"]
    kR = np.array([np.pi / a] * 3)
    H = mk.kashikar13_hamiltonian(kR, p, a)
    dz = vel.dH_dk_kashikar13(kR, p, a, 2)
    return H, dz, p, a


@pytest.mark.parametrize("material", ["CsGeI3", "CsSnI3", "CsPbI3"])
def test_kane_cubic_isotropy(material):
    H, _dz, p, a = _kashikar_PR(material)
    kR = np.array([np.pi / a] * 3)
    dxyz = [vel.dH_dk_kashikar13(kR, p, a, al) for al in range(3)]
    r = kane_parameter_anisotropy(H, dxyz, 20)
    assert max(r.values()) - min(r.values()) < 1e-6


@pytest.mark.parametrize("material", ["CsGeCl3", "CsSnBr3", "CsPbI3"])
def test_cb_pz_weight_one_third(material):
    """CB edge cation-p_z weight sin^2(theta) = 1/3 (Nestoklon Eq.S1b)."""
    H, dz, p, a = _kashikar_PR(material)
    r = extract_kane_parameter(H, dz, 20, 3, 13)
    assert r["sin2theta"] == pytest.approx(1.0 / 3.0, abs=0.02)


def test_nestoklon_cspbi3_P_near_universal():
    """sp3d5s* CsPbI3 bare Kane P within 1.5 eV.A of Kirstein universal 6.8."""
    m = get_material(load_parameter_file(NES), parameter_set="sp3d5sstar")
    p, a, basis = m["params"], m["a"], m["basis"]
    kR = np.array([np.pi / a] * 3)
    H = mn.make_builder(p, a, basis)(kR)
    dz = vel.make_dH_dk_nestoklon(p, a, basis)(kR, 2)
    r = extract_kane_parameter(H, dz, 26, 3, 40)
    assert abs(r["P_bare"] - 6.8) < 1.5, f"P_bare={r['P_bare']:.2f}"


def test_nestoklon_vs_kashikar_cspbi3_cross_check():
    """CsPbI3 bare P from sp3d5s* vs 13-orbital agree within ~35% (different bases).

    Both underestimate the g-factor-effective 6.8 (band-fit, not g-fit params);
    the richer sp3d5s* basis gives the larger (closer-to-6.8) value.
    """
    Hk, dzk, _p, _a = _kashikar_PR("CsPbI3")
    Pk = extract_kane_parameter(Hk, dzk, 20, 3, 13)["P_bare"]
    m = get_material(load_parameter_file(NES), parameter_set="sp3d5sstar")
    p, a, basis = m["params"], m["a"], m["basis"]
    kR = np.array([np.pi / a] * 3)
    Hn = mn.make_builder(p, a, basis)(kR)
    dzn = vel.make_dH_dk_nestoklon(p, a, basis)(kR, 2)
    Pn = extract_kane_parameter(Hn, dzn, 26, 3, 40)["P_bare"]
    assert Pn > Pk  # richer basis -> larger P
    assert abs(Pn - Pk) / max(Pn, Pk) < 0.35
