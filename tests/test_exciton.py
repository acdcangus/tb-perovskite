"""Theme I: Wannier-Mott exciton binding tests."""

import numpy as np
import pytest

from perovskite_tb import exciton as ex
from perovskite_tb import models_kashikar as mk
from perovskite_tb.io_params import get_material, load_parameter_file


def test_wannier_mott_and_reduced_mass():
    # 1/mu = 1/0.1 + 1/0.1 -> mu = 0.05
    assert ex.reduced_mass(0.1, 0.1) == pytest.approx(0.05)
    assert ex.reduced_mass(0.1, -0.1) == pytest.approx(0.05)        # sign-insensitive
    # E_b = mu/eps^2 * Ry
    assert ex.wannier_mott_binding_eV(0.05, 1.0) == pytest.approx(0.05 * 13.605693)
    assert ex.wannier_mott_binding_eV(0.05, 4.0) == pytest.approx(0.05 / 16 * 13.605693)


def test_effective_mass_recovers_synthetic_parabola():
    """For E(k) = (hbar^2/2m*)|k-R|^2 the extractor must return m*/m0 = m_target."""
    a = 6.0
    R = np.array([1.0, 1.0, 1.0]) * np.pi / a
    for m_target in (0.2, 0.5, 1.3):
        c = ex.HBAR2_OVER_M0 / (2.0 * m_target)   # E = c |k-R|^2 -> d2E/dk2 = 2c

        def H_fn(k, c=c):
            return np.array([[c * np.sum((np.asarray(k, float) - R) ** 2)]], dtype=complex)

        m = ex.effective_mass(H_fn, a, band_idx=0, dk=1e-3)
        assert m == pytest.approx(m_target, rel=1e-3)


def test_cspbi3_effective_masses_physical():
    """CsPbI3 (Kashikar-13): conduction edge m_e>0, valence edge m_h<0, both ~0.1 m0
    (literature ~0.1-0.15), reduced mass O(0.05)."""
    m = get_material(load_parameter_file("data/parameters/kashikar2021_cubic_13orb.json"), "CsPbI3")
    p, a = m["params"], m["a"]
    H_fn = lambda k: mk.kashikar13_hamiltonian(k, p, a)   # noqa: E731
    m_e = ex.effective_mass(H_fn, a, band_idx=20)         # CBM (n_occ=20)
    m_h = ex.effective_mass(H_fn, a, band_idx=19)         # VBM
    assert m_e > 0 and m_h < 0
    assert 0.03 < abs(m_e) < 0.4 and 0.03 < abs(m_h) < 0.4
    assert 0.005 < ex.reduced_mass(m_e, m_h) < 0.2
