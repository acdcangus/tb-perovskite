"""V&V for topology.py (spec F2, Wilson loop / WCC).

Validated against the Qi-Wu-Zhang Chern insulator (PRB 74, 085308 (2006)):
the Chern number from the Wilson-loop / Wannier-charge-center winding must (a)
be an integer, (b) match the independent Fukui plaquette Chern of berry.py, and
(c) follow the QWZ phase diagram.  Cross-validating two independent methods
(Wilson loop vs link-variable plaquette) pins both implementations.
"""

import numpy as np
import pytest

from perovskite_tb import berry, topology

SX = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
SY = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
SZ = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)


def _qwz_H(kx, ky, u):
    return (np.sin(kx) * SX + np.sin(ky) * SY
            + (u + np.cos(kx) + np.cos(ky)) * SZ)


def _qwz_occ_grid(u, N):
    """occ_grid[i_perp(ky), j_par(kx), :, 0] = lower-band eigenvector."""
    grid = np.empty((N, N, 2, 1), dtype=complex)
    ks = np.linspace(0.0, 2.0 * np.pi, N, endpoint=False)
    for i, ky in enumerate(ks):       # axis 0 = k_perp = ky
        for j, kx in enumerate(ks):   # axis 1 = k_par  = kx
            _, evecs = np.linalg.eigh(_qwz_H(kx, ky, u))
            grid[i, j, :, 0] = evecs[:, 0]
    return grid


@pytest.mark.parametrize("u", [1.0, -1.0, 3.0, -3.0])
def test_chern_from_wcc_is_integer(u):
    C = topology.chern_from_wcc(_qwz_occ_grid(u, 32))
    assert np.isclose(C, round(C), atol=1e-6), f"u={u}: Chern {C} not integer"


@pytest.mark.parametrize("u", [1.0, -1.0, 1.5, 3.0, -3.0])
def test_wcc_chern_matches_fukui(u):
    """Wilson-loop Chern == Fukui plaquette Chern (two independent methods)."""
    grid_wcc = _qwz_occ_grid(u, 32)
    # berry.link_variable_chern wants (Nx, Ny, dim, n_occ); orientation-agnostic for integer C
    C_wcc = topology.chern_from_wcc(grid_wcc)
    C_fukui = berry.link_variable_chern(grid_wcc)
    assert np.isclose(round(C_wcc), round(C_fukui), atol=1e-6), \
        f"u={u}: WCC C={C_wcc:.3f} vs Fukui C={C_fukui:.3f}"


def test_wcc_phase_diagram():
    C_pos = round(topology.chern_from_wcc(_qwz_occ_grid(1.0, 32)))   # 0<u<2
    C_neg = round(topology.chern_from_wcc(_qwz_occ_grid(-1.0, 32)))  # -2<u<0
    C_triv = round(topology.chern_from_wcc(_qwz_occ_grid(3.0, 32)))  # |u|>2
    assert abs(C_pos) == 1 and abs(C_neg) == 1
    assert C_pos == -C_neg          # sign flip across u=0
    assert C_triv == 0


def test_wilson_loop_unitary_and_gauge_invariant():
    grid = _qwz_occ_grid(1.0, 16)
    W = topology.wilson_loop(grid[3])  # single k_perp line
    # Wilson loop of a single occupied band is a 1x1 unitary (|W|=1)
    assert np.isclose(abs(W[0, 0]), 1.0, atol=1e-10)
    # random U(1) gauge on each eigenvector leaves the polarization phase invariant
    rng = np.random.default_rng(1)
    line = grid[3].copy()
    phases = np.exp(1j * rng.uniform(0, 2 * np.pi, size=line.shape[0]))
    line_g = line * phases[:, None, None]
    assert np.isclose(topology.polarization_phase(topology.wilson_loop(line)),
                      topology.polarization_phase(topology.wilson_loop(line_g)),
                      atol=1e-10)


def test_wcc_in_unit_interval():
    grid = _qwz_occ_grid(1.0, 16)
    wcc = topology.wannier_charge_centers(topology.wilson_loop(grid[0]))
    assert np.all(wcc > -0.5 - 1e-12) and np.all(wcc <= 0.5 + 1e-12)
