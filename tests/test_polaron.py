"""V&V for polaron.py (spec F6): Frohlich coupling + weak-coupling mass.

Primary anchor: the alpha formula reproduces the published Frost (2017) MAPbI3
benchmark (eps_inf=4.5, eps_static=24.1, nu_LO=2.25 THz, m*=0.12 e / 0.15 h)
-> alpha = 2.39 (electron), 2.68 (hole).  This pins the SI prefactor.
"""

import numpy as np
import pytest

from perovskite_tb import bandstructure as bs
from perovskite_tb import models_kashikar as mk
from perovskite_tb import polaron
from perovskite_tb._constants import HBAR2_OVER_M0
from perovskite_tb.io_params import get_material, load_parameter_file

K13 = "data/parameters/kashikar2021_cubic_13orb.json"


def _tb_builder(name):
    m = get_material(load_parameter_file(K13), name)
    p, a = m["params"], m["a"]
    return (lambda k: mk.kashikar13_hamiltonian(np.asarray(k, float), p, a)), a


def test_frost_mapbi3_electron_alpha():
    a = polaron.frohlich_alpha(4.5, 24.1, polaron.omega_from_THz(2.25), 0.12)
    assert np.isclose(a, 2.39, atol=0.03), f"alpha_e={a:.3f} (Frost 2.39)"


def test_frost_mapbi3_hole_alpha():
    a = polaron.frohlich_alpha(4.5, 24.1, polaron.omega_from_THz(2.25), 0.15)
    assert np.isclose(a, 2.68, atol=0.03), f"alpha_h={a:.3f} (Frost 2.68)"


def test_cspbbr3_sendner_alpha():
    # second independent benchmark: Sendner et al., Nat. Commun. 12, 4945 (2021)
    # (PMC8494801): eps_inf=4.8, eps_static=20.5, LO=19.2 meV, m*=0.22(e) -> alpha~2
    a = polaron.frohlich_alpha(4.8, 20.5, polaron.omega_from_meV(19.2), 0.22)
    assert np.isclose(a, 2.0, atol=0.15), f"CsPbBr3 alpha={a:.3f} (Sendner ~2)"


def test_omega_unit_conversions_consistent():
    # 2.25 THz corresponds to ~9.3 meV
    w_thz = polaron.omega_from_THz(2.25)
    w_mev = polaron.omega_from_meV(9.3)
    assert np.isclose(w_thz, w_mev, rtol=0.01)


def test_alpha_scaling_monotonic():
    base = polaron.frohlich_alpha(4.5, 24.1, polaron.omega_from_THz(2.25), 0.12)
    # larger (1/eps_inf - 1/eps_static) -> larger alpha
    more_polar = polaron.frohlich_alpha(3.0, 24.1, polaron.omega_from_THz(2.25), 0.12)
    assert more_polar > base
    # heavier mass -> larger alpha (sqrt(m))
    heavier = polaron.frohlich_alpha(4.5, 24.1, polaron.omega_from_THz(2.25), 0.48)
    assert np.isclose(heavier, base * np.sqrt(0.48 / 0.12), rtol=1e-6)


def test_alpha_requires_polar():
    with pytest.raises(ValueError):
        polaron.frohlich_alpha(5.0, 4.0, polaron.omega_from_THz(2.0), 0.1)


def test_weak_coupling_mass_limit():
    assert polaron.weak_coupling_polaron_mass(0.0) == 1.0
    assert polaron.weak_coupling_polaron_mass(0.6) > 1.0
    # leading order: m_p/m_b - 1 = alpha/6
    assert np.isclose(polaron.weak_coupling_polaron_mass(0.6) - 1.0, 0.6 / 6.0)


# --- effective mass from the core TB (band curvature) -------------------------

def test_effective_mass_synthetic_parabola():
    """Method check: E(k)=(hbar^2/2m)|k|^2 with m_rel=0.25 -> recovered exactly."""
    m_rel = 0.25
    builder = lambda k: np.array([[(HBAR2_OVER_M0 / (2 * m_rel)) * (np.asarray(k, float) @ np.asarray(k, float))]])  # noqa: E731
    r = bs.effective_mass(builder, [0.0, 0.0, 0.0], 0, dk=1e-3)
    assert np.isclose(r["mean"], m_rel, rtol=1e-4), f"got {r['mean']}"
    for lab in ("100", "110", "111"):
        assert np.isclose(r[lab], m_rel, rtol=1e-4)


def test_tb_effective_mass_isotropic_at_R():
    """Cubic CsPbBr3 R-point band edges are isotropic (m* equal along 100/110/111)."""
    H, a = _tb_builder("CsPbBr3")
    R = np.array([np.pi / a] * 3)
    me = bs.effective_mass(H, R, 20, dk=1e-3)   # CBM = n_filled (20)
    mh = bs.effective_mass(H, R, 19, dk=1e-3)   # VBM = n_filled - 1
    assert np.allclose([me["100"], me["110"], me["111"]], me["mean"], rtol=2e-3)
    assert np.allclose([mh["100"], mh["110"], mh["111"]], mh["mean"], rtol=2e-3)
    assert me["mean"] > 0 and mh["mean"] < 0, "CBM mass > 0, VBM mass < 0"


def test_cspbbr3_alpha_from_core_tb_mass():
    """TB-DRIVEN polaron alpha: m* from the core TB + cited Sendner dielectric/LO.

    The Frohlich alpha is computed end-to-end from the core TB (band-edge mass at
    R) and the cited CsPbBr3 dielectric/LO data (Sendner, Nat. Commun. 12, 4945
    (2021): eps_inf=4.8, eps_static=20.5, LO=19.2 meV).  The TB band mass
    m_e~0.151 is LIGHTER than the m*=0.22 Sendner adopted, so alpha_TB~1.66 is
    below Sendner's alpha~2.0.  HONEST accounting: the whole discrepancy is the
    mass ratio, since alpha ~ sqrt(m_b):  alpha_TB/alpha(0.22) == sqrt(m_TB/0.22).
    The alpha FORMULA itself reproduces Sendner given m*=0.22 (separate test).
    """
    H, a = _tb_builder("CsPbBr3")
    R = np.array([np.pi / a] * 3)
    m_e_tb = bs.effective_mass(H, R, 20, dk=1e-3)["mean"]
    assert np.isclose(m_e_tb, 0.151, atol=0.01), f"TB m_e={m_e_tb:.4f}"

    eps_inf, eps_s, lo_meV = 4.8, 20.5, 19.2
    alpha_tb = polaron.frohlich_alpha(eps_inf, eps_s, polaron.omega_from_meV(lo_meV), m_e_tb)
    alpha_022 = polaron.frohlich_alpha(eps_inf, eps_s, polaron.omega_from_meV(lo_meV), 0.22)
    assert np.isclose(alpha_tb, 1.66, atol=0.1), f"alpha_TB={alpha_tb:.3f}"
    # the deviation from Sendner is fully the band-mass ratio (sqrt scaling)
    assert np.isclose(alpha_tb / alpha_022, np.sqrt(m_e_tb / 0.22), rtol=1e-6)
