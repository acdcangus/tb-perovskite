"""V&V for berry.py (spec F1): Berry curvature, Chern, AHC, SHC.

Verification anchors (analytic / exact):
  * Massive 2-band Dirac H = kx sx + ky sy + m sz: the lower-band Berry
    curvature has the closed form Omega_-(k) = +m / (2 (kx^2+ky^2+m^2)^{3/2})
    in the Xiao-2010 convention (derived directly from the Kubo formula).
  * Qi-Wu-Zhang lattice Chern insulator (PRB 74, 085308 (2006))
    H = sin kx sx + sin ky sy + (u + cos kx + cos ky) sz: the lower band has
    Chern number +/-1 for |u|<2 (sign flips across u=0) and 0 for |u|>2;
    the Fukui-Hatsugai-Suzuki (2005) link-variable method must return integers.
  * Cubic CsBX3 (Kashikar-13, SOC on) is P*T symmetric -> AHC = 0.
"""

import numpy as np
import pytest

from perovskite_tb import berry
from perovskite_tb.io_params import get_material, load_parameter_file

K13 = "data/parameters/kashikar2021_cubic_13orb.json"

from _helpers import SX, SY, SZ, qwz_hamiltonian  # noqa: E402


# --------------------------------------------------------------------------- #
# 1. Massive Dirac: analytic Berry curvature
# --------------------------------------------------------------------------- #
def _dirac_curvature_lower(kx, ky, m):
    """Code Berry curvature of the lower band of H = kx sx + ky sy + m sz."""
    H = kx * SX + ky * SY + m * SZ
    evals, evecs = np.linalg.eigh(H)
    omega = berry.berry_curvature_kubo(evals, evecs, SX, SY)
    return omega[0]  # lower band


@pytest.mark.parametrize("kx,ky,m", [
    (0.0, 0.0, 1.0), (0.3, 0.0, 1.0), (0.0, -0.4, 1.0),
    (0.5, 0.7, 2.0), (-0.6, 0.2, 0.5), (1.1, -0.9, 1.3),
])
def test_dirac_berry_curvature_matches_analytic(kx, ky, m):
    d = np.sqrt(kx * kx + ky * ky + m * m)
    analytic = +m / (2.0 * d ** 3)
    got = _dirac_curvature_lower(kx, ky, m)
    assert np.isclose(got, analytic, rtol=1e-6, atol=1e-12), \
        f"Dirac Omega_- mismatch: got {got:.8e}, analytic {analytic:.8e}"


def test_dirac_upper_lower_opposite():
    H = 0.4 * SX - 0.3 * SY + 1.2 * SZ
    evals, evecs = np.linalg.eigh(H)
    omega = berry.berry_curvature_kubo(evals, evecs, SX, SY)
    assert np.isclose(omega[0], -omega[1], rtol=1e-10, atol=1e-12)


def test_curvature_is_real():
    H = 0.4 * SX - 0.3 * SY + 1.2 * SZ
    evals, evecs = np.linalg.eigh(H)
    omega = berry.berry_curvature_kubo(evals, evecs, SX, SY)
    assert omega.dtype == np.float64


# --------------------------------------------------------------------------- #
# 2. Qi-Wu-Zhang: integer Chern via Fukui method + phase diagram
# --------------------------------------------------------------------------- #
_qwz_H = qwz_hamiltonian  # QWZ Chern-insulator H(k), shared


def _qwz_lower_occ_grid(u, N):
    grid = np.empty((N, N, 2, 1), dtype=complex)
    ks = np.linspace(0.0, 2.0 * np.pi, N, endpoint=False)
    for i, kx in enumerate(ks):
        for j, ky in enumerate(ks):
            _, evecs = np.linalg.eigh(_qwz_H(kx, ky, u))
            grid[i, j, :, 0] = evecs[:, 0]  # lower band
    return grid


@pytest.mark.parametrize("u", [1.0, -1.0, 3.0, -3.0, 1.5, -1.5])
def test_qwz_chern_is_integer(u):
    C = berry.link_variable_chern(_qwz_lower_occ_grid(u, 24))
    assert np.isclose(C, round(C), atol=1e-9), f"u={u}: Chern {C} not integer"


def test_qwz_phase_diagram():
    C_in_pos = berry.link_variable_chern(_qwz_lower_occ_grid(1.0, 24))   # 0<u<2
    C_in_neg = berry.link_variable_chern(_qwz_lower_occ_grid(-1.0, 24))  # -2<u<0
    C_out_pos = berry.link_variable_chern(_qwz_lower_occ_grid(3.0, 24))  # u>2
    C_out_neg = berry.link_variable_chern(_qwz_lower_occ_grid(-3.0, 24)) # u<-2
    assert abs(round(C_in_pos)) == 1
    assert abs(round(C_in_neg)) == 1
    assert round(C_in_pos) == -round(C_in_neg)  # sign flip across u=0
    assert round(C_out_pos) == 0
    assert round(C_out_neg) == 0


# --------------------------------------------------------------------------- #
# 3. Kubo <-> Fukui consistency (QWZ, gapped)
# --------------------------------------------------------------------------- #
def test_kubo_vs_fukui_chern():
    u, N = 1.0, 48
    C_fukui = berry.link_variable_chern(_qwz_lower_occ_grid(u, N))
    # Kubo: C = (1/2pi) int Omega d^2k  ~  (1/2pi) sum_k Omega(k) (2pi/N)^2
    ks = np.linspace(0.0, 2.0 * np.pi, N, endpoint=False)
    acc = 0.0
    for kx in ks:
        for ky in ks:
            evals, evecs = np.linalg.eigh(_qwz_H(kx, ky, u))
            acc += berry.berry_curvature_kubo(evals, evecs,
                                              np.cos(kx) * SX - np.sin(kx) * SZ,
                                              np.cos(ky) * SY - np.sin(ky) * SZ)[0]
    C_kubo = acc * (2.0 * np.pi / N) ** 2 / (2.0 * np.pi)
    assert np.isclose(C_kubo, C_fukui, atol=0.05), \
        f"Kubo {C_kubo:.4f} vs Fukui {C_fukui:.1f}"


# --------------------------------------------------------------------------- #
# 4. Cubic CsBX3 (Kashikar-13): P*T -> AHC = 0
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("material", ["CsPbI3", "CsSnI3", "CsGeCl3"])
def test_cubic_perovskite_ahc_zero(material):
    m = get_material(load_parameter_file(K13), material)
    p, a = m["params"], m["a"]
    rng = np.random.default_rng(0)
    base = rng.uniform(-0.4, 0.4, size=(6, 3)) * (2 * np.pi / a)
    # +/-k symmetric mesh -> TRS forces the occupied-summed curvature to cancel
    kpts = np.vstack([base, -base])
    # Fermi level in the wide gap above the metal-p bands (~1.3-1.6 eV) and below
    # the high (~5 eV) bands -> occupied = complete Kramers multiplets at every k.
    e_fermi = 2.5
    H_g, Hx_g, Hy_g = [], [], []
    for k in kpts:
        H, dHx, dHy, _ = berry.kashikar13_at_k(k, p, a)
        H_g.append(H); Hx_g.append(dHx); Hy_g.append(dHy)
    ahc = berry.anomalous_hall_sum(H_g, Hx_g, Hy_g, e_fermi=e_fermi)
    assert abs(ahc) < 1e-10, f"{material}: AHC={ahc:.3e} (expected 0 by P*T)"


def test_cubic_perovskite_curvature_total_zero():
    # sum over ALL bands of Omega vanishes identically (antisymmetry) -- sanity
    m = get_material(load_parameter_file(K13), "CsPbI3")
    p, a = m["params"], m["a"]
    k = np.array([0.13, -0.21, 0.07]) * (2 * np.pi / a)
    H, dHx, dHy, _ = berry.kashikar13_at_k(k, p, a)
    evals, evecs = np.linalg.eigh(H)
    omega = berry.berry_curvature_kubo(evals, evecs, dHx, dHy)
    assert abs(np.sum(omega)) < 1e-8


# --------------------------------------------------------------------------- #
# 5. Spin Hall: spin Berry curvature is real, finite, generally non-zero
# --------------------------------------------------------------------------- #
def test_spin_operators_structure():
    Sx, Sy, Sz = berry.spin_operators(13)
    assert Sx.shape == (26, 26)
    # S_z^2 = (1/2)^2 I = 0.25 I  (eigenvalues +/- 1/2)
    assert np.allclose(Sz @ Sz, 0.25 * np.eye(26), atol=1e-12)
    # [Sx, Sy] = i Sz  (su(2) algebra)
    assert np.allclose(Sx @ Sy - Sy @ Sx, 1j * Sz, atol=1e-12)


def test_spin_berry_curvature_real_and_runs():
    m = get_material(load_parameter_file(K13), "CsPbI3")
    p, a = m["params"], m["a"]
    k = np.array([0.13, -0.21, 0.07]) * (2 * np.pi / a)
    H, dHx, dHy, _ = berry.kashikar13_at_k(k, p, a)
    _, _, Sz = berry.spin_operators(13)
    jx = berry.spin_current_operator(Sz, dHx)
    assert np.allclose(jx, jx.conj().T, atol=1e-10)  # j is Hermitian
    evals, evecs = np.linalg.eigh(H)
    omega_s = berry.spin_berry_curvature_kubo(evals, evecs, jx, dHy)
    assert omega_s.dtype == np.float64
    assert np.all(np.isfinite(omega_s))
    # spin Berry curvature is NOT forced to zero by P*T (unlike charge AHC)
    assert np.max(np.abs(omega_s)) > 0.0
