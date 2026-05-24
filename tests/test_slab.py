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

import json

import numpy as np
import pytest

from perovskite_tb import models_kashikar as mk
from perovskite_tb import slab
from perovskite_tb.io_params import get_material, load_parameter_file

K13 = "data/parameters/kashikar2021_cubic_13orb.json"
BLANCON = "data/parameters/blancon2018_2drp_gaps.json"


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


def _confinement_exponent(ns, gaps, e_inf):
    """Power-law exponent p of the confinement shift Delta = E_g(n) - E_inf ~ n^-p.

    Returns the slope of log(Delta) vs log(n) (a negative number; we report |p|).
    """
    ns = np.asarray(ns, float)
    delta = np.asarray([gaps[n] for n in ns.astype(int)], float) - e_inf
    assert np.all(delta > 0), f"non-positive confinement shift for E_inf={e_inf}"
    return -np.polyfit(np.log(ns), np.log(delta), 1)[0]


def test_blancon_layer_dependence():
    """F5 quantum-confinement TREND vs Blancon 2018 free-particle gaps.

    The TB slab (core Kashikar-13 CsPbI3, hard-barrier idealisation) confinement
    gap E_g(N) at the in-plane M point is compared to the verified free-particle
    band gaps of (BA)2(MA)_{n-1}Pb_nI_{3n+1} (Blancon et al., Nat. Commun. 9, 2254
    (2018); n=1,4,5 exact from Fig. 3a/4).

    HONEST scope (category C->B): only the confinement-decay SHAPE (power-law
    exponent p in Delta E_g ~ n^-p) is compared.  Absolute gaps are NOT compared:
    the TB models the *inorganic* CsPbI3 analog, the experiment is the MAPbI3-based
    RP with butylammonium spacers, and the SK-TB/Blount caveat applies.  The
    experimental exponent is sensitive to the 3D baseline E_inf:
        E_inf=1.60 -> p_exp~0.71 ; 1.65 -> ~0.80 ; 1.70 -> ~0.91 .
    The free-particle 3D gap (= optical 1.60 eV + binding) lies in [1.60,1.70] eV.
    """
    p, a = _mat()
    kx = ky = np.pi / a  # in-plane projection of the bulk R-point gap
    tb = {N: slab.slab_gap(p, a, kx, ky, N) for N in (1, 2, 3, 4, 5)}
    R = np.array([np.pi / a] * 3)
    ev_R = np.linalg.eigvalsh(mk.kashikar13_hamiltonian(R, p, a))
    e_inf_tb = float(ev_R[slab.N_OCC_PER_CELL] - ev_R[slab.N_OCC_PER_CELL - 1])

    # (1) TB confinement: monotonic decrease toward the 3D limit.
    vals = [tb[N] for N in (1, 2, 3, 4, 5)]
    assert all(x > y for x, y in zip(vals, vals[1:])), f"not monotone: {tb}"
    assert vals[-1] > e_inf_tb, "slab gap must sit above the 3D bulk gap"

    # (2) TB confinement exponent in the physical quantum-well regime.
    p_tb = _confinement_exponent([1, 2, 3, 4, 5], tb, e_inf_tb)
    assert 0.6 <= p_tb <= 1.3, f"TB confinement exponent out of range: {p_tb:.3f}"

    # (3) Experimental free-particle gaps (verified) -> same confinement regime,
    #     and the exponent agrees with TB within 15% at the free-particle baseline.
    exp = json.load(open(BLANCON))["free_particle_gaps_eV"]
    exp_gaps = {int(k[1:]): v["value"] for k, v in exp.items()}  # {1:2.540,4:2.078,5:1.846}
    for e_inf in (1.60, 1.65, 1.70):
        p_exp = _confinement_exponent(sorted(exp_gaps), exp_gaps, e_inf)
        assert 0.6 <= p_exp <= 1.1, f"exp exponent out of regime at E_inf={e_inf}: {p_exp:.3f}"
    # central free-particle baseline 1.65-1.70 eV: |p_tb - p_exp| within 15%
    p_exp_central = _confinement_exponent(sorted(exp_gaps), exp_gaps, 1.675)
    rel = abs(p_tb - p_exp_central) / p_exp_central
    assert rel < 0.15, f"trend mismatch: p_tb={p_tb:.3f}, p_exp={p_exp_central:.3f}, rel={rel:.2f}"


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
