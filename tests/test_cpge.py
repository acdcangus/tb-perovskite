"""V&V for cpge.py (spec F7): circular photogalvanic / injection current.

Anchors:
  * Formula reduction (de Juan 2017): for two bands the cross-gap-connection
    object eps_jkl r^k_12 r^l_21 equals the lower-band Berry-curvature vector
    Omega^j_1 -> the general and two-band CPGE expressions must agree.
  * Inversion symmetry: a centrosymmetric (even-d, non-degenerate) model gives
    beta = 0.
  * Topological quantization (de Juan 2017): for a Weyl node the CPGE trace is a
    frequency-INDEPENDENT plateau proportional to the Chern number C
    (Tr ~ pi e^3/h^2 * C), so it is ~constant in omega and flips sign with the
    node chirality.
"""

import numpy as np

from perovskite_tb import berry, cpge

from _helpers import SX, SY, SZ  # noqa: E402


def test_connection_reduces_to_berry_curvature():
    """eps_jkl r^k_12 r^l_21 == Omega^j_1 (de Juan two-band reduction)."""
    rng = np.random.default_rng(3)
    for _ in range(5):
        d = rng.normal(size=3) + 0.3  # generic 2-band H = d.sigma
        H = d[0] * SX + d[1] * SY + d[2] * SZ
        dH = [SX, SY, SZ]  # dH/dk if d = k (Weyl-like); generic vertices
        evals, U = np.linalg.eigh(H)
        V = [U.conj().T @ dH[a] @ U for a in range(3)]
        r12 = cpge.cross_gap_connection(V, evals, 0, 1)
        r21 = cpge.cross_gap_connection(V, evals, 1, 0)
        rr = np.array([-np.imag(sum(cpge._EPS[j, k, l] * r12[k] * r21[l]
                                    for k in range(3) for l in range(3)))
                       for j in range(3)])  # -Im(eps r r) = Omega (Xiao convention)
        Om = cpge.berry_curvature_vector(evals, U, dH, band=0)
        assert np.allclose(rr, Om, atol=1e-10), f"rr={rr}, Omega={Om}"


def test_general_equals_two_band():
    """General CPGE formula == two-band Berry-curvature form (Weyl model)."""
    vF = 1.0
    H_fn = lambda k: vF * (k[0] * SX + k[1] * SY + k[2] * SZ)   # noqa: E731
    dH_fn = lambda k, a: vF * [SX, SY, SZ][a]                    # noqa: E731
    rng = np.random.default_rng(0)
    kpts = rng.uniform(-1, 1, size=(400, 3))
    bg = cpge.cpge_tensor(kpts, H_fn, dH_fn, omega=1.0, eta=0.1, n_occ=1)
    b2 = cpge.cpge_tensor_2band(kpts, H_fn, dH_fn, omega=1.0, eta=0.1)
    assert np.allclose(bg, b2, atol=1e-12), f"max diff {np.max(np.abs(bg-b2)):.2e}"


def test_centrosymmetric_zero():
    """Even d(k) -> inversion symmetric -> beta = 0 (non-degenerate model)."""
    M = 0.7
    H_fn = lambda k: np.cos(k[0]) * SX + np.cos(k[1]) * SY + (M + np.cos(k[2])) * SZ  # noqa: E731
    dH_fn = lambda k, a: [-np.sin(k[0]) * SX, -np.sin(k[1]) * SY, -np.sin(k[2]) * SZ][a]  # noqa: E731
    ks = np.linspace(-np.pi, np.pi, 12, endpoint=False)
    kpts = np.array([[a, b, c] for a in ks for b in ks for c in ks])
    beta = cpge.cpge_tensor(kpts, H_fn, dH_fn, omega=2.0, eta=0.2, n_occ=1)
    assert np.max(np.abs(beta)) < 1e-10, f"centrosym beta max {np.max(np.abs(beta)):.2e}"


def _weyl_trace(chirality, omega, n=41, kmax=1.0):
    sz = chirality * SZ
    H_fn = lambda k: k[0] * SX + k[1] * SY + k[2] * sz       # noqa: E731
    dH_fn = lambda k, a: [SX, SY, sz][a]                      # noqa: E731
    ks = np.linspace(-kmax, kmax, n)
    dk = ks[1] - ks[0]
    kpts = np.array([[a, b, c] for a in ks for b in ks for c in ks])
    measure = (dk ** 3) / (2 * np.pi) ** 3 * len(kpts)  # cpge_tensor divides by Nk
    beta = cpge.cpge_tensor(kpts, H_fn, dH_fn, omega, eta=0.08, n_occ=1, measure=measure)
    return np.trace(beta)


def test_weyl_quantization_plateau_and_chirality():
    tr_08 = _weyl_trace(+1, 0.8)
    tr_10 = _weyl_trace(+1, 1.0)
    tr_neg = _weyl_trace(-1, 1.0)
    # frequency-independent plateau (quantization): Tr(0.8) ~ Tr(1.0)
    assert np.isclose(tr_08, tr_10, rtol=0.15), f"plateau: {tr_08:.4f} vs {tr_10:.4f}"
    # chirality sign flip
    assert np.isclose(tr_10, -tr_neg, rtol=0.05), f"chirality: {tr_10:.4f} vs {tr_neg:.4f}"
    # nonzero plateau
    assert abs(tr_10) > 1e-3
    # bonus: absolute value near the de Juan value pi e^3/h^2 = 1/(4pi) (e=hbar=1)
    assert np.isclose(abs(tr_10), 1.0 / (4 * np.pi), rtol=0.2), \
        f"|Tr|={abs(tr_10):.4f} vs 1/(4pi)={1/(4*np.pi):.4f}"
