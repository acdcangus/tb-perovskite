"""V&V for edelstein.py (spec F11): current-induced spin polarization.

Anchors:
  * Centrosymmetric (non-degenerate) model d(k)=(cos kx, cos ky, M), d even ->
    <S> even, v odd -> chi = 0.
  * Rashba model -> chi perpendicular to current (chi_yx != 0, chi_xx ~ 0) and
    chi_yx flips sign with the Rashba coefficient alpha (Edelstein 1990).
"""

import numpy as np

from perovskite_tb import edelstein, rashba

from _helpers import SX, SY, SZ  # noqa: E402


def _grid_2d(N=40):
    ks = np.linspace(-np.pi, np.pi, N, endpoint=False)
    KX, KY = np.meshgrid(ks, ks, indexing="ij")
    return KX.ravel(), KY.ravel()


def _band_data(H_of_k, dHx_of_k, S_op, kx, ky):
    """Assemble (E, <S>, v_x) arrays over the 2D grid for a 2-band model."""
    nb = 2
    E = np.empty((kx.size, nb))
    spin = np.empty((kx.size, nb))
    vel = np.empty((kx.size, nb))
    half = 0.5 * np.array([[1, 0], [0, 1]])  # noqa: F841 (placeholder)
    for i, (a, b) in enumerate(zip(kx, ky)):
        H = H_of_k(a, b)
        evals, U = np.linalg.eigh(H)
        E[i] = evals
        spin[i] = rashba.spin_texture(U, S_op)
        vel[i] = np.real(np.diag(U.conj().T @ dHx_of_k(a, b) @ U))
    return E, spin, vel


def test_centrosymmetric_zero():
    M = 0.6
    H = lambda a, b: np.cos(a) * SX + np.cos(b) * SY + M * SZ          # noqa: E731
    dHx = lambda a, b: -np.sin(a) * SX                                  # noqa: E731
    kx, ky = _grid_2d(40)
    E, sy, vx = _band_data(H, dHx, 0.5 * SY, kx, ky)
    chi = edelstein.edelstein_susceptibility(E, sy, vx, mu=0.0, T=300.0)
    assert abs(chi) < 1e-10, f"centrosymmetric chi_yx={chi:.2e} (expected 0)"


def test_rashba_perpendicular():
    alpha = 1.0
    H = lambda a, b: alpha * (a * SY - b * SX)                          # noqa: E731
    dHx = lambda a, b: alpha * SY                                       # noqa: E731
    kx, ky = _grid_2d(60)
    # use small-k region (linear Rashba); restrict to a ring near E_F
    E, sy, vx = _band_data(H, dHx, 0.5 * SY, kx, ky)
    _, sx, _ = _band_data(H, dHx, 0.5 * SX, kx, ky)
    chi_yx = edelstein.edelstein_susceptibility(E, sy, vx, mu=0.0, T=300.0)
    chi_xx = edelstein.edelstein_susceptibility(E, sx, vx, mu=0.0, T=300.0)
    # Rashba-Edelstein: spin response perpendicular to the current
    assert abs(chi_yx) > 1e-4, f"Rashba chi_yx={chi_yx:.2e} should be nonzero"
    assert abs(chi_xx) < 1e-3 * abs(chi_yx), \
        f"chi_xx={chi_xx:.2e} should be << chi_yx={chi_yx:.2e} (perpendicular)"


def test_rashba_sign_flips_with_alpha():
    def chi(alpha):
        H = lambda a, b: alpha * (a * SY - b * SX)                      # noqa: E731
        dHx = lambda a, b: alpha * SY                                   # noqa: E731
        kx, ky = _grid_2d(60)
        E, sy, vx = _band_data(H, dHx, 0.5 * SY, kx, ky)
        return edelstein.edelstein_susceptibility(E, sy, vx, mu=0.0, T=300.0)
    cp, cm = chi(1.0), chi(-1.0)
    assert np.isclose(cp, -cm, rtol=1e-6), f"chi(+a)={cp:.4e}, chi(-a)={cm:.4e}"


def test_polar_perovskite_runs():
    from perovskite_tb.io_params import get_material, load_parameter_file
    m = get_material(load_parameter_file("data/parameters/kashikar2021_cubic_13orb.json"), "CsPbI3")
    p, a = m["params"], m["a"]
    rng = np.random.default_rng(0)
    kpts = rng.uniform(-0.4, 0.4, size=(150, 3)) * (2 * np.pi / a)
    E, sy, vx = edelstein.band_data_polar_kashikar13(kpts, p, a, 0.4, spin_axis=1, vel_axis=0)
    chi = edelstein.edelstein_susceptibility(E, sy, vx, mu=float(np.median(E)), T=300.0)
    assert np.isfinite(chi)


# --- T2-4: tau-independent Edelstein efficiency chi_yx/sigma_xx ----------------

def _rashba_parabolic_band_data(m, alpha, N, kmax):
    """Batched 2D Rashba H = (k^2/2m) I + alpha(kx sy - ky sx); S = sigma/2."""
    ks = np.linspace(-kmax, kmax, N)
    KX, KY = np.meshgrid(ks, ks, indexing="ij")
    kx, ky = KX.ravel(), KY.ravel()
    I2 = np.eye(2)
    H = ((kx ** 2 + ky ** 2)[:, None, None] / (2 * m)) * I2 \
        + alpha * (kx[:, None, None] * SY - ky[:, None, None] * SX)
    E, U = np.linalg.eigh(H)
    Sy = np.real(np.einsum("kan,ab,kbn->kn", U.conj(), 0.5 * SY, U))
    Sx = np.real(np.einsum("kan,ab,kbn->kn", U.conj(), 0.5 * SX, U))
    dHx = (kx[:, None, None] / m) * I2 + alpha * SY
    vx = np.real(np.einsum("kan,kab,kbn->kn", U.conj(), dHx, U))
    return E, Sy, Sx, vx


def test_rashba_edelstein_ratio_analytic():
    """chi_yx/sigma_xx == m*alpha/(4 mu) for the 2D Rashba model (S=sigma/2).

    Derived leading-order (small alpha, both subbands at mu>0); tau and the
    k-grid normalisation cancel in the ratio.
    """
    from perovskite_tb._constants import KB_EV
    m, mu, N = 1.0, 2.0, 251
    T = 0.02 / KB_EV   # thermo uses T in Kelvin; k_B T = 0.02 eV
    alpha = 0.05
    kmax = 1.8 * np.sqrt(2 * m * mu) + 4 * alpha * m + 1.0
    E, Sy, Sx, vx = _rashba_parabolic_band_data(m, alpha, N, kmax)
    ratio = edelstein.edelstein_ratio(E, Sy, vx, mu, T)
    analytic = m * alpha / (4 * mu)
    assert np.isclose(ratio, analytic, rtol=0.15), f"ratio={ratio:.5f} vs {analytic:.5f}"
    # no longitudinal spin response
    chi_xx = edelstein.edelstein_susceptibility(E, Sx, vx, mu, T)
    sig = edelstein.longitudinal_conductivity(E, vx, mu, T)
    assert abs(chi_xx) / sig < 1e-6, f"chi_xx/sigma={chi_xx / sig:.2e} (expected 0)"
    # linear in alpha: doubling alpha doubles the efficiency
    E2, Sy2, _, vx2 = _rashba_parabolic_band_data(m, 2 * alpha, N, kmax)
    ratio2 = edelstein.edelstein_ratio(E2, Sy2, vx2, mu, T)
    assert np.isclose(ratio2 / ratio, 2.0, rtol=0.15), f"not linear: {ratio2 / ratio:.3f}"


def test_polar_perovskite_efficiency_finite():
    """chi_yx/sigma_xx (tau-independent) for the core-TB polar perovskite is finite."""
    from perovskite_tb.io_params import get_material, load_parameter_file
    m = get_material(load_parameter_file("data/parameters/kashikar2021_cubic_13orb.json"), "CsPbI3")
    p, a = m["params"], m["a"]
    rng = np.random.default_rng(1)
    kpts = rng.uniform(-0.4, 0.4, size=(200, 3)) * (2 * np.pi / a)
    E, sy, vx = edelstein.band_data_polar_kashikar13(kpts, p, a, 0.4, spin_axis=1, vel_axis=0)
    mu = float(np.percentile(E, 80))  # sit in the conduction states
    ratio = edelstein.edelstein_ratio(E, sy, vx, mu, T=300.0)
    assert np.isfinite(ratio)
