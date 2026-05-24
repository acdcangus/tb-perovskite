"""V&V for edelstein.py (spec F11): current-induced spin polarization.

Anchors:
  * Centrosymmetric (non-degenerate) model d(k)=(cos kx, cos ky, M), d even ->
    <S> even, v odd -> chi = 0.
  * Rashba model -> chi perpendicular to current (chi_yx != 0, chi_xx ~ 0) and
    chi_yx flips sign with the Rashba coefficient alpha (Edelstein 1990).
"""

import numpy as np

from perovskite_tb import edelstein, rashba

SX = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
SY = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
SZ = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)


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
