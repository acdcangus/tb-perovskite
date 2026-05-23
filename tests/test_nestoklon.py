"""V&V: reproduction of the published values in Nestoklon, arXiv:2012.14705.

The paper states explicit numbers we reproduce here:
  * DFT band gap at R = 1.017 eV (sp3 and sp3d5s* fits to the DFT band structure).
  * Experiment-corrected gaps: R = 1.65 eV, M = 2.75 eV.
  * Conduction-band spin-orbit splitting at R = 1.48 eV (sp3d5s* sets).
  * The fundamental gap of cubic halide perovskites is direct, at R.
"""

import numpy as np
import pytest

from perovskite_tb import kpath as kp
from perovskite_tb.bandstructure import compute_band_structure, fundamental_gap
from perovskite_tb.io_params import get_material, load_parameter_file
from perovskite_tb.models import build_model

PARAM_FILE = "data/parameters/nestoklon2021_CsPbI3.json"


@pytest.fixture(scope="module")
def data():
    return load_parameter_file(PARAM_FILE)


def _spec(data, pset):
    m = get_material(data, parameter_set=pset)
    return build_model(m), m["a"], m["params"]


def _eig_at(spec, kvec):
    H = spec.builder(np.asarray(kvec, float))
    assert np.allclose(H, H.conj().T, atol=1e-10), "Hamiltonian not Hermitian"
    return np.sort(np.linalg.eigvalsh(H).real)


def _gap_at(spec, kvec):
    ev = _eig_at(spec, kvec)
    nf = spec.n_filled
    return ev[nf] - ev[nf - 1]


@pytest.mark.parametrize("pset", ["sp3", "sp3d5sstar"])
def test_dft_gap_at_R(data, pset):
    """R-point gap reproduces the DFT value Eg = 1.017 eV."""
    spec, a, _ = _spec(data, pset)
    kR = np.array([np.pi / a] * 3)
    gap = _gap_at(spec, kR)
    assert gap == pytest.approx(1.017, abs=0.01), f"{pset}: R gap {gap:.4f}"


def test_experiment_corrected_gaps(data):
    """Experiment-corrected set reproduces R = 1.65 eV and M = 2.75 eV."""
    spec, a, _ = _spec(data, "experiment_corrected")
    kR = np.array([np.pi / a] * 3)
    kM = np.array([np.pi / a, np.pi / a, 0.0])
    assert _gap_at(spec, kR) == pytest.approx(1.65, abs=0.01)
    assert _gap_at(spec, kM) == pytest.approx(2.75, abs=0.02)


@pytest.mark.parametrize("pset", ["sp3d5sstar", "experiment_corrected"])
def test_cb_so_splitting_at_R(data, pset):
    """Conduction-band SO splitting at R is ~1.48 eV for the sp3d5s* sets.

    The CB bottom at R is a j=1/2 doublet; the next CB level (j=3/2) sits
    ~1.48 eV above it.
    """
    spec, a, _ = _spec(data, pset)
    kR = np.array([np.pi / a] * 3)
    ev = _eig_at(spec, kR)
    nf = spec.n_filled
    so = ev[nf + 2] - ev[nf]
    assert so == pytest.approx(1.48, abs=0.03), f"{pset}: CB SO splitting {so:.4f}"


@pytest.mark.parametrize("pset", ["sp3", "sp3d5sstar", "experiment_corrected"])
def test_fundamental_gap_is_direct_at_R(data, pset):
    """The fundamental gap is direct and located at the R point."""
    spec, a, _ = _spec(data, pset)
    path = kp.make_kpath(["M", "R", "G", "X", "M", "G"], a, 60)
    bs = compute_band_structure(spec.builder, path, spec.n_filled)
    gi = fundamental_gap(bs)
    # R is the second node on the M-R-... path.
    r_distance = path.tick_positions[1]
    assert gi["direct"], f"{pset}: gap not direct"
    assert gi["vbm_distance"] == pytest.approx(r_distance, abs=1e-6)
    assert gi["cbm_distance"] == pytest.approx(r_distance, abs=1e-6)


def test_hermitian_generic_k(data):
    spec, a, _ = _spec(data, "sp3d5sstar")
    k = np.array([0.13, -0.27, 0.41]) * (2 * np.pi / a)
    H = spec.builder(k)
    assert H.shape == (80, 80)
    assert np.allclose(H, H.conj().T, atol=1e-10)
