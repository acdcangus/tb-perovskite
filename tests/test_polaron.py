"""V&V for polaron.py (spec F6): Frohlich coupling + weak-coupling mass.

Primary anchor: the alpha formula reproduces the published Frost (2017) MAPbI3
benchmark (eps_inf=4.5, eps_static=24.1, nu_LO=2.25 THz, m*=0.12 e / 0.15 h)
-> alpha = 2.39 (electron), 2.68 (hole).  This pins the SI prefactor.
"""

import numpy as np
import pytest

from perovskite_tb import polaron


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
