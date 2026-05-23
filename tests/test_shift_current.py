"""Shift-current (Theme F / F3) tests.

VALIDATED here:
  * Harrison distance scaling t(d)=t(d0)(d0/d)^eta;
  * the polar-displaced Nestoklon builder reduces *exactly* to the centrosymmetric
    base builder at delta=0 (so any non-vanishing sigma at delta=0 is a shift-vector
    bug, not a Hamiltonian bug);
  * time-reversal E(k)=E(-k) holds for the polar (delta>0) builder.

The production sigma_zzz uses the velocity-gauge sum-over-states generalized
derivative (Cowork review 2026-05-23 1300, option B), which recovers the
centrosymmetric vanishing at delta=0 (machine precision) by skipping degenerate
intermediate states. The deprecated Abelian routine (which fails this) is retained
only for regression. Absolute sign/prefactor are F4 (relative units here).
"""

import numpy as np
import pytest

from perovskite_tb import models_kashikar as mk
from perovskite_tb import models_nestoklon as mn
from perovskite_tb import shift_current as sc
from perovskite_tb import velocity as vel
from perovskite_tb.io_params import get_material, load_parameter_file

NES = "data/parameters/nestoklon2021_CsPbI3.json"
KAS13 = "data/parameters/kashikar2021_cubic_13orb.json"


@pytest.fixture(scope="module")
def cspbi3():
    m = get_material(load_parameter_file(NES), parameter_set="experiment_corrected")
    return m["params"], m["a"], m["basis"]


@pytest.fixture(scope="module")
def cspbi3_kashikar():
    m = get_material(load_parameter_file(KAS13), "CsPbI3")
    return m["params"], m["a"]


def test_polar_kashikar_reduces_to_base_at_zero(cspbi3_kashikar):
    """delta=0 polar Kashikar-13 builder == base kashikar13_hamiltonian (bit-exact);
    dH/d2H Hermitian and match central finite differences for all axes."""
    p, a = cspbi3_kashikar
    H, dH, d2H = sc.make_polar_kashikar13_builders(p, a, polar_displacement_z=0.0)
    k = np.array([0.11, 0.23, 0.31]) * (2 * np.pi / a)
    assert np.allclose(H(k), mk.kashikar13_hamiltonian(k, p, a), atol=1e-12)
    for alpha in (0, 1, 2):
        eps = 1e-5
        ek = np.zeros(3)
        ek[alpha] = eps
        assert np.allclose(dH(k, alpha), dH(k, alpha).conj().T, atol=1e-12)
        assert np.allclose(d2H(k, alpha), d2H(k, alpha).conj().T, atol=1e-12)
        assert np.allclose(dH(k, alpha), (H(k + ek) - H(k - ek)) / (2 * eps), atol=1e-3)
        assert np.allclose(d2H(k, alpha),
                           (dH(k + ek, alpha) - dH(k - ek, alpha)) / (2 * eps), atol=1e-3)


def test_polar_kashikar_shift_current_symmetry(cspbi3_kashikar):
    """Polar Kashikar-13 (9-material model) shift current: delta=0 vanishes;
    sigma_zzz(-delta) = -sigma_zzz(+delta) (Tan&Rappe sign reversal); P4mm forbids
    sigma_xxx.  n_occ=20 (Pb-s^2 + 3 I-p^6)."""
    p, a = cspbi3_kashikar
    omega = np.linspace(0.5, 3.5, 14)

    def sigma(delta, direction):
        H, dH, d2H = sc.make_polar_kashikar13_builders(p, a, polar_displacement_z=delta)
        return sc.shift_current_zzz(H, dH, a, 20, omega, n_kpts=4, smearing_eta=0.08,
                                    direction=direction, d2Hdk_fn=d2H)

    s0 = sigma(0.0, 2)
    sp = sigma(0.12, 2)
    sm = sigma(-0.12, 2)
    sx = sigma(0.12, 0)
    assert np.max(np.abs(s0)) < 1e-10
    assert np.max(np.abs(sp)) > 1e-3
    assert np.max(np.abs(sp + sm)) < 1e-9 * max(np.max(np.abs(sp)), 1.0)  # sign reversal
    assert np.max(np.abs(sx)) < 1e-8                                       # P4mm forbids xxx


def test_harrison_scaling():
    assert sc.harrison_scaled_hopping(2.0, 3.0, 3.0) == pytest.approx(2.0)
    # shorter bond -> larger |hopping|
    assert abs(sc.harrison_scaled_hopping(2.0, 3.0, 2.7)) > 2.0
    # eta=2 universal value
    assert sc.harrison_scaled_hopping(1.0, 2.0, 1.0, eta=2.0) == pytest.approx(4.0)


def test_polar_builder_reduces_to_base_at_zero(cspbi3):
    """delta=0 polar builder == centrosymmetric base Nestoklon builder (exactly)."""
    p, a, basis = cspbi3
    Hp, dHp, d2Hp = sc.make_polar_nestoklon_builders(p, a, basis, polar_displacement_z=0.0)
    Hb = mn.make_builder(p, a, basis)
    dHb = vel.make_dH_dk_nestoklon(p, a, basis)
    k = np.array([0.13, 0.21, 0.31]) * (2 * np.pi / a)
    assert np.allclose(Hp(k), Hb(k), atol=1e-12)
    assert np.allclose(dHp(k, 2), dHb(k, 2), atol=1e-12)
    # d2H/dk_z^2 is Hermitian and matches a central finite difference of dH/dk_z
    eps = 1e-4
    ez = np.array([0.0, 0.0, 1.0])
    fd = (dHp(k + eps * ez, 2) - dHp(k - eps * ez, 2)) / (2 * eps)
    assert np.allclose(d2Hp(k, 2), fd, atol=1e-3)
    assert np.allclose(d2Hp(k, 2), d2Hp(k, 2).conj().T, atol=1e-12)


def test_polar_builder_breaks_inversion(cspbi3):
    """delta>0 modifies the Hamiltonian (inversion broken) but keeps TRS E(k)=E(-k)."""
    p, a, basis = cspbi3
    Hp, _, _ = sc.make_polar_nestoklon_builders(p, a, basis, polar_displacement_z=0.2)
    Hb = mn.make_builder(p, a, basis)
    k = np.array([0.1, 0.2, 0.3]) * (2 * np.pi / a)
    assert not np.allclose(Hp(k), Hb(k), atol=1e-6)          # inversion broken
    Ek = np.sort(np.linalg.eigvalsh(Hp(k)).real)
    Emk = np.sort(np.linalg.eigvalsh(Hp(-k)).real)
    assert np.allclose(Ek, Emk, atol=1e-10)                  # time-reversal


def test_centrosymmetric_vanishes(cspbi3):
    """delta=0 => sigma_zzz == 0 by centrosymmetry (sum-over-states, to ~1e-10)."""
    p, a, basis = cspbi3
    Hp, dHp, d2Hp = sc.make_polar_nestoklon_builders(p, a, basis, polar_displacement_z=0.0)
    omega = np.linspace(1.0, 4.0, 25)
    sig = sc.shift_current_zzz(Hp, dHp, a, 26, omega, n_kpts=6, smearing_eta=0.08,
                               d2Hdk_fn=d2Hp)
    assert np.max(np.abs(sig)) < 1e-10, f"max|sigma|={np.max(np.abs(sig)):.2e}"


def test_polar_displacement_turns_on_and_scales(cspbi3):
    """sigma_zzz vanishes at delta=0, is nonzero at delta>0, and grows with delta
    (approximately linear for small delta). Output is real."""
    p, a, basis = cspbi3
    omega = np.linspace(1.0, 4.5, 25)
    peaks = {}
    for delta in (0.0, 0.05, 0.10):
        Hp, dHp, d2Hp = sc.make_polar_nestoklon_builders(p, a, basis, polar_displacement_z=delta)
        sig = sc.shift_current_zzz(Hp, dHp, a, 26, omega, n_kpts=6, smearing_eta=0.08,
                                   d2Hdk_fn=d2Hp)
        assert np.all(np.isreal(sig))
        peaks[delta] = np.max(np.abs(sig))
    assert peaks[0.0] < 1e-10
    assert peaks[0.05] > 1e-3
    assert peaks[0.10] > peaks[0.05]                       # grows with delta
    # approximately linear: sigma(0.1)/sigma(0.05) ~ 2 (allow 1.5-3)
    assert 1.5 < peaks[0.10] / peaks[0.05] < 3.0


def test_polar_sign_reverses_under_displacement_flip(cspbi3):
    """F4-2 (multi-band sanity check vs Tan & Rappe 2016, npj Comput Mater 2:16026):
    flipping the [001] Pb displacement delta -> -delta applies a spatial inversion,
    so sigma_zzz(-delta) = -sigma_zzz(+delta) exactly (their statement: 'changing
    the sign of delta changes the direction of the shift current'). Independent
    multi-band confirmation of the sign, complementing the 2-band Rice-Mele/Fregoso
    closed-form check."""
    p, a, basis = cspbi3
    omega = np.linspace(2.0, 4.5, 12)
    out = {}
    for delta in (-0.12, 0.12):
        Hp, dHp, d2Hp = sc.make_polar_nestoklon_builders(p, a, basis, polar_displacement_z=delta)
        out[delta] = sc.shift_current_zzz(Hp, dHp, a, 26, omega, n_kpts=4,
                                          smearing_eta=0.10, direction=2, d2Hdk_fn=d2Hp)
    scale = np.max(np.abs(out[0.12]))
    assert scale > 1e-3
    assert np.max(np.abs(out[-0.12] + out[0.12])) < 1e-9 * max(scale, 1.0)


def test_cubic_all_diagonal_components_vanish(cspbi3):
    """F4-4: in the centrosymmetric cubic phase (delta=0), sigma_xxx = sigma_yyy =
    sigma_zzz = 0 (rank-3 polar tensor forbidden by inversion)."""
    p, a, basis = cspbi3
    Hp, dHp, d2Hp = sc.make_polar_nestoklon_builders(p, a, basis, polar_displacement_z=0.0)
    omega = np.linspace(1.0, 4.0, 20)
    for direction in (0, 1, 2):
        sig = sc.shift_current_zzz(Hp, dHp, a, 26, omega, n_kpts=6,
                                   smearing_eta=0.08, direction=direction, d2Hdk_fn=d2Hp)
        assert np.max(np.abs(sig)) < 1e-10, f"dir={direction}: {np.max(np.abs(sig)):.2e}"


def test_p4mm_only_polar_axis_nonzero(cspbi3):
    """F4-4: under [001] polar displacement (P4mm), sigma_zzz != 0 but sigma_xxx,
    sigma_yyy ~ 0 (4mm symmetry forbids x-/y-polarised diagonal shift current)."""
    p, a, basis = cspbi3
    Hp, dHp, d2Hp = sc.make_polar_nestoklon_builders(p, a, basis, polar_displacement_z=0.15)
    omega = np.linspace(1.0, 4.5, 25)
    s_zzz = np.max(np.abs(sc.shift_current_zzz(Hp, dHp, a, 26, omega, n_kpts=6,
                                               smearing_eta=0.08, direction=2, d2Hdk_fn=d2Hp)))
    s_xxx = np.max(np.abs(sc.shift_current_zzz(Hp, dHp, a, 26, omega, n_kpts=6,
                                               smearing_eta=0.08, direction=0, d2Hdk_fn=d2Hp)))
    s_yyy = np.max(np.abs(sc.shift_current_zzz(Hp, dHp, a, 26, omega, n_kpts=6,
                                               smearing_eta=0.08, direction=1, d2Hdk_fn=d2Hp)))
    assert s_zzz > 1e-3
    assert s_xxx < 1e-9 and s_yyy < 1e-9, f"xxx={s_xxx:.2e}, yyy={s_yyy:.2e}"
