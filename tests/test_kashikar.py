"""Verification of the Kashikar-Gupta-Nanda models against the paper.

Source: arXiv:2101.08562.

The decisive check is that the numerically diagonalized 13-orbital spinless
Bloch Hamiltonian at the R point reproduces the analytic eigenvalues of Eq. (9)
to machine precision -- for every one of the nine CsBX3 compounds.  This pins
down the entire Slater-Koster construction (geometry, gauge, integral table)
because Eq. (9) is derived independently in the paper.
"""

import numpy as np
import pytest

from perovskite_tb import models_kashikar as mk
from perovskite_tb.io_params import get_material, load_parameter_file

MATERIALS = ["CsGeCl3", "CsGeBr3", "CsGeI3", "CsSnCl3", "CsSnBr3",
             "CsSnI3", "CsPbCl3", "CsPbBr3", "CsPbI3"]


@pytest.fixture(scope="module")
def data13():
    return load_parameter_file("data/parameters/kashikar2021_cubic_13orb.json")


@pytest.fixture(scope="module")
def data4():
    return load_parameter_file("data/parameters/kashikar2021_cubic_4orb.json")


@pytest.mark.parametrize("material", MATERIALS)
def test_eq9_R_point(data13, material):
    """13-orbital H(R) eigenvalues == analytic Eq. (9), to ~1e-12."""
    m = get_material(data13, material)
    p, a = m["params"], m["a"]
    kR = np.array([np.pi / a] * 3)  # R = (pi/a, pi/a, pi/a)

    H0 = mk.kashikar13_spinless(kR, p, a)
    assert np.allclose(H0, H0.conj().T, atol=1e-12), "H not Hermitian"

    num = np.sort(np.linalg.eigvalsh(H0))
    ana = mk.kashikar13_R_eigenvalues(p)
    analytic = []
    for _key, (val, deg) in ana.items():
        analytic += [val] * deg
    analytic = np.sort(np.array(analytic))

    assert np.allclose(num, analytic, atol=1e-10), (
        f"{material}: numeric {num}\n vs analytic {analytic}")


@pytest.mark.parametrize("material", MATERIALS)
def test_hamiltonian_hermitian_generic_k(data13, material):
    """The spinful Hamiltonian is Hermitian at a generic (low-symmetry) k."""
    m = get_material(data13, material)
    p, a = m["params"], m["a"]
    k = np.array([0.17, 0.31, -0.23]) * (2 * np.pi / a)
    H = mk.kashikar13_hamiltonian(k, p, a)
    assert H.shape == (26, 26)
    assert np.allclose(H, H.conj().T, atol=1e-12)


@pytest.mark.parametrize("material", MATERIALS)
def test_R_point_degeneracies(data13, material):
    """At R the spinless spectrum shows the 1-8-3-1 degeneracy pattern of Eq. 9."""
    m = get_material(data13, material)
    p, a = m["params"], m["a"]
    kR = np.array([np.pi / a] * 3)
    ev = np.sort(np.linalg.eigvalsh(mk.kashikar13_spinless(kR, p, a)))
    # Count degeneracies by clustering close eigenvalues.
    clusters = []
    for e in ev:
        if clusters and abs(e - clusters[-1][0]) < 1e-6:
            clusters[-1][1] += 1
            clusters[-1][0] = e
        else:
            clusters.append([e, 1])
    degens = sorted(c[1] for c in clusters)
    # Expect degeneracies {1,1,3,8} (E2 is 8-fold, E3 3-fold, E1/E4 singlets).
    assert degens == [1, 1, 3, 8], f"{material}: got {degens}"


@pytest.mark.parametrize("material", MATERIALS)
def test_cb_soc_splitting_at_R(data13, material):
    """Conduction-band SO splitting at R equals 3*lambda (Eq. 10 convention).

    At R the B-p triplet (CB) is isolated at E3 (the B-X p-p coupling vanishes
    there), so ``lambda L.S`` (implemented as 2*lambda*L.S) splits the 6 CB
    spin-states into a 4-fold j=3/2 level at E3+lambda and a 2-fold j=1/2 level
    at E3-2*lambda: splitting = 3*lambda.  For CsPbI3 (lambda=0.50) this gives
    1.50 eV, close to the 1.48 eV reported by Nestoklon (arXiv:2012.14705).
    """
    m = get_material(data13, material)
    p, a = m["params"], m["a"]
    lam = p["lambda_SOC"]
    kR = np.array([np.pi / a] * 3)
    ev = np.sort(np.linalg.eigvalsh(mk.kashikar13_hamiltonian(kR, p, a)))
    # The 6 CB states are spin-states 20..25 (n_filled = 20).
    cb = ev[20:26]
    lower = cb[:2]   # j=1/2 doublet
    upper = cb[2:]   # j=3/2 quartet
    assert np.allclose(lower, lower[0], atol=1e-9)
    assert np.allclose(upper, upper[0], atol=1e-9)
    splitting = upper[0] - lower[0]
    assert abs(splitting - 3.0 * lam) < 1e-9, f"{material}: {splitting} vs {3*lam}"


@pytest.mark.parametrize("material", MATERIALS)
def test_4orbital_gap_formula(data4, material):
    """4-orbital model: closed-form no-SOC gap == numeric (E[CBM]-E[VBM]) at R.

    In the minimal model the s-derived band (1 spatial, n_filled=2 with spin) is
    the valence-band top and the B-p triplet is the conduction band.  Without SOC
    the gap at R must equal Eg = eps_p - eps_s - 2*tppsigma - 4*tppi + 6*tss.
    """
    m = get_material(data4, material)
    p, a = m["params"], m["a"]
    kR = np.array([np.pi / a] * 3)
    H0 = mk.kashikar4_spinless(kR, p, a)
    ev = np.sort(np.linalg.eigvalsh(H0))
    # spinless: 1 s-band (VBM) + 3 p-bands (CB). gap = ev[1] - ev[0].
    numeric_gap = ev[1] - ev[0]
    formula_gap = mk.kashikar4_gap_no_soc(p)
    assert abs(numeric_gap - formula_gap) < 1e-9, (
        f"{material}: numeric {numeric_gap} vs formula {formula_gap}")
