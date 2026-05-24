"""V&V for rashba.py (spec F4): inversion-breaking spin splitting.

Anchors:
  * Analytic 2-band Rashba H = (hbar^2 k^2/2m) I + alpha_R(k_x sigma_y - k_y sigma_x):
    the extraction recovers the input alpha_R, and the spin is locked
    perpendicular to k (Bychkov-Rashba 1984).
  * Cubic CsBX3 (Pm-3m, centrosymmetric): Kramers degeneracy -> splitting = 0.
  * [001] polar CsBX3 (P4mm): inversion broken -> nonzero k-linear splitting,
    vanishing at the TRIM k=0.
"""

import numpy as np
import pytest

from perovskite_tb import berry, rashba
from perovskite_tb.io_params import get_material, load_parameter_file
from perovskite_tb.shift_current import make_polar_kashikar13_builders

K13 = "data/parameters/kashikar2021_cubic_13orb.json"


@pytest.mark.parametrize("alpha,kmag,axis", [
    (0.5, 0.01, 0), (1.2, 0.02, 0), (0.8, 0.01, 1), (2.0, 0.005, 1),
])
def test_analytic_rashba_extraction(alpha, kmag, axis):
    H_fn = rashba.analytic_rashba_builder(alpha)
    got = rashba.rashba_coefficient(H_fn, band_index=0, k_mag=kmag, axis=axis)
    assert np.isclose(got, alpha, rtol=1e-9), f"alpha_R {got} vs {alpha}"


def test_analytic_rashba_spin_perpendicular_to_k():
    H_fn = rashba.analytic_rashba_builder(1.0)
    _, _, _ = None, None, None
    Sx = 0.5 * np.array([[0, 1], [1, 0]], complex)
    Sy = 0.5 * np.array([[0, -1j], [1j, 0]], complex)
    k = np.array([0.05, 0.0, 0.0])  # k along x
    _, U = np.linalg.eigh(H_fn(k))
    sx = rashba.spin_texture(U, Sx)
    sy = rashba.spin_texture(U, Sy)
    # spin along +/- y (perpendicular to k=x); no x-component
    assert np.allclose(sx, 0.0, atol=1e-9)
    assert np.max(np.abs(sy)) > 0.4  # ~ +/- 1/2


def test_cubic_perovskite_no_splitting():
    """Centrosymmetric cubic -> Kramers degenerate -> alpha_R = 0."""
    m = get_material(load_parameter_file(K13), "CsPbI3")
    p, a = m["params"], m["a"]
    H_fn, _, _ = make_polar_kashikar13_builders(p, a, polar_displacement_z=0.0)
    for bi in (6, 12, 18):  # several doublets
        alpha = abs(rashba.rashba_coefficient(H_fn, bi, k_mag=0.02 * (2 * np.pi / a)))
        assert alpha < 1e-6, f"cubic band {bi}: alpha_R={alpha:.2e} (expected 0)"


def test_polar_perovskite_splits_and_vanishes_at_gamma():
    """[001] polar displacement breaks inversion -> nonzero k-linear splitting."""
    m = get_material(load_parameter_file(K13), "CsPbI3")
    p, a = m["params"], m["a"]
    H_fn, _, _ = make_polar_kashikar13_builders(p, a, polar_displacement_z=0.4)
    kb = 2 * np.pi / a
    # transverse k (x) splits the doublet; scan a band that shows splitting
    splits = {bi: rashba.doublet_splitting(H_fn(np.array([0.03 * kb, 0, 0])), bi)
              for bi in range(0, 24, 2)}
    max_bi = max(splits, key=splits.get)
    s_k = rashba.doublet_splitting(H_fn(np.array([0.03 * kb, 0, 0])), max_bi)
    s_half = rashba.doublet_splitting(H_fn(np.array([0.015 * kb, 0, 0])), max_bi)
    s_gamma = rashba.doublet_splitting(H_fn(np.array([0.0, 0, 0])), max_bi)
    assert s_k > 1e-4, f"polar: no splitting found (max={s_k:.2e})"
    assert s_gamma < 1e-6, f"splitting at Gamma should vanish (Kramers), got {s_gamma:.2e}"
    assert s_half < s_k  # grows with |k| (k-linear-like)


def test_spin_operators_reused_from_berry():
    Sx, Sy, Sz = berry.spin_operators(13)
    assert Sx.shape == (26, 26)
