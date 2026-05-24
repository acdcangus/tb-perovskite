"""V&V for slab.py (spec F5/F13/F14-A): perovskite z-slab / superlattice.

Rigorous model-internal anchors:
  * Exact reconstruction: H_par + T e^{i kz a} + T^dag e^{-i kz a} == 3D H (gauge
    transform is unitary -> same eigenvalues), to machine precision.
  * Periodic N-cell stack eigenvalues == union of the 3D bands at the discrete
    kz = 2*pi*m/(N a) (F13).
  * inter_layer_scale -> 0 collapses the kz dispersion (flat mini-bands).
  * Open slab: gap converges as N grows (quantum-confinement bulk limit, F5).
  * Stark (F14-A): E=0 recovers the field-free slab; finite E broadens the
    spectrum by ~ e*E*(N-1)*a.
"""

import numpy as np
import pytest

from perovskite_tb import models_kashikar as mk
from perovskite_tb import slab
from perovskite_tb.io_params import get_material, load_parameter_file

K13 = "data/parameters/kashikar2021_cubic_13orb.json"


def _mat(name="CsPbI3"):
    m = get_material(load_parameter_file(K13), name)
    return m["params"], m["a"]


def _gauge_H(params, a, kx, ky, kz):
    z2 = slab._orbital_z(a)
    H = mk.kashikar13_hamiltonian(np.array([kx, ky, kz]), params, a)
    U = np.diag(np.exp(-1j * kz * z2))
    return U @ H @ U.conj().T


def test_layer_block_reconstruction():
    p, a = _mat()
    kx, ky = 0.13 * 2 * np.pi / a, -0.21 * 2 * np.pi / a
    Hpar, T = slab.layer_blocks(p, a, kx, ky)
    for kz in [0.0, 0.4, 1.3, 2.7]:
        rec = slab.reconstruct_3d(Hpar, T, kz, a)
        assert np.allclose(rec, _gauge_H(p, a, kx, ky, kz), atol=1e-10), \
            f"reconstruction failed at kz={kz}"


@pytest.mark.parametrize("N", [3, 5, 8])
def test_periodic_stack_equals_3d_bands(N):
    p, a = _mat()
    kx, ky = 0.13 * 2 * np.pi / a, -0.21 * 2 * np.pi / a
    ev_slab = np.sort(slab.slab_eigenvalues(p, a, kx, ky, N, periodic=True))
    ev_3d = []
    for m in range(N):
        kz = 2 * np.pi * m / (N * a)
        ev_3d.extend(np.linalg.eigvalsh(mk.kashikar13_hamiltonian(np.array([kx, ky, kz]), p, a)))
    ev_3d = np.sort(ev_3d)
    assert np.allclose(ev_slab, ev_3d, atol=1e-9), \
        f"N={N}: max diff {np.max(np.abs(ev_slab-ev_3d)):.2e}"


def test_miniband_collapse_weak_coupling():
    """inter_layer_scale -> 0 : periodic stack bands collapse to H_par levels."""
    p, a = _mat()
    kx, ky = 0.2 * 2 * np.pi / a, 0.1 * 2 * np.pi / a
    Hpar, _ = slab.layer_blocks(p, a, kx, ky)
    h_levels = np.sort(np.linalg.eigvalsh(Hpar))
    ev = np.sort(slab.slab_eigenvalues(p, a, kx, ky, 4, periodic=True, inter_layer_scale=0.0))
    # each H_par level appears N times (no dispersion)
    assert np.allclose(ev, np.repeat(h_levels, 4), atol=1e-9)


def test_open_slab_gap_converges_with_thickness():
    p, a = _mat()
    kx = ky = np.pi / a  # in-plane M point (above the R-point gap)
    gaps = {N: slab.slab_gap(p, a, kx, ky, N) for N in (2, 4, 8, 16)}
    assert all(g > 0 for g in gaps.values())
    # convergence: successive change shrinks
    d_small = abs(gaps[16] - gaps[8])
    d_large = abs(gaps[4] - gaps[2])
    assert d_small < d_large, f"gap not converging: {gaps}"


def test_stark_field_zero_recovers_and_broadens():
    p, a = _mat()
    kx, ky = 0.1 * 2 * np.pi / a, 0.0
    N = 8
    ev0 = slab.slab_eigenvalues(p, a, kx, ky, N, e_field_z=0.0)
    ev0b = slab.slab_eigenvalues(p, a, kx, ky, N)
    assert np.allclose(ev0, ev0b, atol=1e-12)  # E=0 == field-free
    E = 0.02  # V/Angstrom
    evE = slab.slab_eigenvalues(p, a, kx, ky, N, e_field_z=E)
    spread0 = ev0.max() - ev0.min()
    spreadE = evE.max() - evE.min()
    # potential drop across the slab ~ E*(N-1)*a broadens the spectrum
    assert spreadE > spread0
    assert np.isclose(spreadE - spread0, E * (N - 1) * a, rtol=0.5)
