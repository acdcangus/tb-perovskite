"""g-factor verification (Theme A, A3).

What is rigorously validated here:
  * k.p universal relation (Kirstein 2021 Eqs.5,6) reproduces the Nestoklon
    Table S2 *electron* anchor g_e(CsPbI3) = +3.23 and the Eg->infinity limits.
  * The atomistic Roth-Lax g-tensor is cubic-isotropic (g_xx=g_yy=g_zz).
  * The spin-only limit (no interband/orbital coupling) gives g -> g0 = 2.0023.

NOT asserted (documented as an open item, see docs/g-factor-formulation.md and
progress/): the *magnitude* of the atomistic Roth-Lax g_e via TB dH/dk
under-shoots Table S2 (1.06 vs 3.23), attributed to the intra-atomic orbital
moment missing from a k-independent on-site SOC.  Per directive: values are not
falsified to force agreement.
"""

import numpy as np
import pytest

from perovskite_tb import models_nestoklon as mn
from perovskite_tb import velocity as vel
from perovskite_tb.g_factor import G0, compute_g_factor, g_factor_kp
from perovskite_tb.io_params import get_material, load_parameter_file

NES = "data/parameters/nestoklon2021_CsPbI3.json"


def test_kp_reproduces_electron_anchor():
    """k.p (Kirstein Eq.6) with Table S2 inputs gives g_e = +3.23 for CsPbI3."""
    r = g_factor_kp(Eg=1.652, Delta=1.258, P=6.8, dg_e=-1.0)
    assert r["g_e"] == pytest.approx(3.23, abs=0.05)


@pytest.mark.parametrize("mat,Eg,Delta,ge_ref", [
    ("CsPbCl3", 3.090, 1.526, 0.95),
    ("CsPbBr3", 2.352, 1.436, 1.77),
    ("CsPbI3", 1.652, 1.258, 3.23),
])
def test_kp_reproduces_pb_electron_table_s2(mat, Eg, Delta, ge_ref):
    """k.p g_e reproduces Nestoklon Table S2 for all 3 Pb halides to ~meV (A4-4).

    (g_h is reproduced only approximately by the 2-band k.p, especially for the
    iodide -- the known limitation; not asserted tightly here.)
    """
    g = g_factor_kp(Eg, Delta, P=6.8, dg_e=-1.0)
    assert g["g_e"] == pytest.approx(ge_ref, abs=0.02), f"{mat}: g_e={g['g_e']:.3f}"


def test_kp_large_gap_limits():
    """Eg -> infinity: g_e -> -2/3 + dg_e = -5/3, g_h -> +2 (Kirstein Sec. text)."""
    r = g_factor_kp(Eg=1e6, Delta=1.5, P=6.8, dg_e=-1.0)
    assert r["g_e"] == pytest.approx(-2.0 / 3.0 - 1.0, abs=1e-3)
    assert r["g_h"] == pytest.approx(2.0, abs=1e-3)


def test_atomistic_cubic_isotropy():
    """Roth-Lax g-tensor is isotropic in the cubic phase (g_xx=g_yy=g_zz)."""
    m = get_material(load_parameter_file(NES), parameter_set="experiment_corrected")
    p, a, basis = m["params"], m["a"], m["basis"]
    builder = mn.make_builder(p, a, basis)
    dHdk = vel.make_dH_dk_nestoklon(p, a, basis)
    kR = np.array([np.pi / a] * 3)
    H = builder(kR)
    dH = (dHdk(kR, 0), dHdk(kR, 1), dHdk(kR, 2))
    for band_index in (24, 26):  # VBM doublet, CBM doublet (n_filled=26)
        g = compute_g_factor(H, dH, band_index=band_index)
        assert g["delta_g"] < 1e-6, f"anisotropy {g['delta_g']:.2e} at band {band_index}"


def test_spin_only_limit_gives_g0():
    """With no interband (orbital) coupling, a pure-spin doublet gives g = g0.

    Synthetic 1-orbital x 2-spin Hamiltonian (spin-major): H = diag(0,0); the
    two states are a pure Kramers spin doublet, velocity = 0 -> g = g0 = 2.0023.
    """
    H = np.zeros((2, 2), dtype=complex)
    zero = np.zeros((2, 2), dtype=complex)
    g = compute_g_factor(H, (zero, zero, zero), band_index=0)
    assert g["g_iso"] == pytest.approx(G0, abs=1e-6)
    assert g["g_zz"] == pytest.approx(G0, abs=1e-6)


def test_roth_lax_vs_kp_within_remote_band_tolerance():
    """Roth-Lax (atomistic, incl. intra-atomic L) agrees with the k.p universal
    g_e within the remote-band tolerance (~1.5), per Cowork review 2026-05-23.

    The residual difference is the contribution of conduction bands above the
    model space (Kirstein's Delta_g_e ~ -1); it is a physical result, not a bug.
    """
    m = get_material(load_parameter_file(NES), parameter_set="experiment_corrected")
    p, a, basis = m["params"], m["a"], m["basis"]
    builder = mn.make_builder(p, a, basis)
    dHdk = vel.make_dH_dk_nestoklon(p, a, basis)
    kR = np.array([np.pi / a] * 3)
    H = builder(kR)
    dH = (dHdk(kR, 0), dHdk(kR, 1), dHdk(kR, 2))
    ev = np.sort(np.linalg.eigvalsh(H).real)
    nf = 26
    Eg, Delta = ev[nf] - ev[nf - 1], ev[nf + 2] - ev[nf]

    from perovskite_tb.g_factor import onsite_L_operators
    L = onsite_L_operators(len(basis), 4, (1, 2, 3))
    ge_rl = compute_g_factor(H, dH, band_index=26, orbital_L=L)["g_iso"]
    ge_kp = g_factor_kp(Eg, Delta)["g_e"]
    assert abs(ge_rl - ge_kp) < 1.5, f"|{ge_rl:.2f}-{ge_kp:.2f}| = {abs(ge_rl-ge_kp):.2f}"


def test_atomistic_returns_finite_isotropic_values():
    """Smoke test: atomistic g_e, g_h are finite and isotropic (magnitude is an
    open item, not asserted here)."""
    m = get_material(load_parameter_file(NES), parameter_set="experiment_corrected")
    p, a, basis = m["params"], m["a"], m["basis"]
    builder = mn.make_builder(p, a, basis)
    dHdk = vel.make_dH_dk_nestoklon(p, a, basis)
    kR = np.array([np.pi / a] * 3)
    H = builder(kR)
    dH = (dHdk(kR, 0), dHdk(kR, 1), dHdk(kR, 2))
    ge = compute_g_factor(H, dH, band_index=26)
    gh = compute_g_factor(H, dH, band_index=24)
    assert np.isfinite(ge["g_iso"]) and np.isfinite(gh["g_iso"])
