"""F4-3: analytic validation of the shift-current generalized derivative against
the Rice-Mele closed form (Fregoso 2017, arXiv:1701.00172, Appendix D).

This is the *decisive* sign/prefactor check for Theme F.  The 1D two-band
Rice-Mele model has a fully analytic shift current, so it pins down both the
SIGN and the magnitude of our velocity-gauge generalized-derivative integrand --
something the centrosymmetric (delta=0) vanishing test cannot do (0 = 0 trivially).

It also documents the key physics finding (F4-3): the tight-binding generalized
derivative needs the off-diagonal second-derivative term w^{aa}_nm = <n|d2H/dk2|m>
(Fregoso Eq.(C2)); the continuum Sipe-Shkrebtii form (w diagonal) gives ZERO for a
2-band model and is wrong for TB.  Dropping w (d2Hdk_fn=None / Waa=0) is checked to
reproduce that erroneous ~0 result.

Fregoso conventions (Eq.(D2)):
    H(k) = t cos(ka/2) sigma_x - delta sin(ka/2) sigma_y + Delta sigma_z
    E(k) = sqrt(t^2 cos^2(ka/2) + delta^2 sin^2(ka/2) + Delta^2)
    Eq.(D15):  Im[r^z_cv r^z_vc;z] = a^3 t delta Delta / (32 E^3)   (Fregoso sign)
    Eq.(D16):  sigma_zzz < 0 for t, delta, Delta > 0.
Our shift_current_integrand_aaa uses the textbook r^a_cv = v_cv/(i w_cv) phase
convention and returns the NEGATIVE of Eq.(D15); the physical sigma sign still
matches Eq.(D16) (Fregoso Eq.(D14): |r|^2 R = -Im[r r;]).
"""

import numpy as np
import pytest

from perovskite_tb import shift_current as sc

PARAM_SETS = [
    dict(t=1.0, delta=0.5, Delta=0.5, a=1.0),
    dict(t=1.0, delta=1.0, Delta=0.3, a=1.0),
    dict(t=1.2, delta=0.4, Delta=0.7, a=1.3),
]


def _band_arrays(k, t, delta, Delta, a):
    H = sc.rice_mele_hamiltonian(k, t, delta, Delta, a)
    E, U = np.linalg.eigh(0.5 * (H + H.conj().T))
    Va = U.conj().T @ sc.rice_mele_dHdk(k, t, delta, Delta, a) @ U
    Waa = U.conj().T @ sc.rice_mele_d2Hdk(k, t, delta, Delta, a) @ U
    return E, Va, Waa


@pytest.mark.parametrize("ps", PARAM_SETS)
def test_energy_matches_eigenvalues(ps):
    """E(k) closed form == eigenvalues of H_RM(k)."""
    for k in np.linspace(-np.pi / ps["a"], np.pi / ps["a"], 11):
        E = np.linalg.eigvalsh(sc.rice_mele_hamiltonian(k, **ps))
        Ean = sc.rice_mele_energy(k, **ps)
        assert E[0] == pytest.approx(-Ean, abs=1e-12)
        assert E[1] == pytest.approx(+Ean, abs=1e-12)


@pytest.mark.parametrize("ps", PARAM_SETS)
def test_integrand_matches_fregoso_D15(ps):
    """Per-k integrand == -(Fregoso D15), to machine precision, at all k.

    This validates the generalized derivative INCLUDING the second-derivative w
    term: magnitude AND relative sign are fixed by the closed form."""
    for k in np.linspace(0.05, np.pi / ps["a"] - 0.05, 13):
        E, Va, Waa = _band_arrays(k, **ps)
        g, wcv = sc.shift_current_integrand_aaa(E, Va, Waa, n_occ=1, deg_tol=1e-12)
        analytic = sc.rice_mele_integrand_analytic(k, **ps)   # Fregoso +D15
        assert g[0, 0] == pytest.approx(-analytic, rel=1e-7, abs=1e-14)
        # gap == 2 E(k)
        assert wcv[0, 0] == pytest.approx(2.0 * sc.rice_mele_energy(k, **ps), abs=1e-12)


@pytest.mark.parametrize("ps", PARAM_SETS)
def test_dropping_w_term_gives_zero(ps):
    """Continuum form (Waa=0) erroneously yields ~0 integrand for the 2-band model
    -- the documented F4-3 finding that the TB w term is essential."""
    for k in np.linspace(0.1, np.pi / ps["a"] - 0.1, 5):
        E, Va, _ = _band_arrays(k, **ps)
        g0, _ = sc.shift_current_integrand_aaa(E, Va, np.zeros_like(Va),
                                               n_occ=1, deg_tol=1e-12)
        assert abs(g0[0, 0]) < 1e-12


def test_inversion_symmetric_limits_vanish():
    """delta=0 (no dimerization) or Delta=0 (no staggered potential) restores
    inversion symmetry => integrand and sigma vanish."""
    omega = np.linspace(0.5, 4.0, 80)
    for ps in (dict(t=1.0, delta=0.0, Delta=0.5, a=1.0),
               dict(t=1.0, delta=0.6, Delta=0.0, a=1.0)):
        for k in np.linspace(0.1, np.pi - 0.1, 7):
            E, Va, Waa = _band_arrays(k, **ps)
            g, _ = sc.shift_current_integrand_aaa(E, Va, Waa, n_occ=1, deg_tol=1e-12)
            assert abs(g[0, 0]) < 1e-12
        sig = sc.shift_current_1d_two_band(omega_grid=omega, n_kpts=2000,
                                           smearing_eta=0.03, **ps)
        assert np.max(np.abs(sig)) < 1e-9


@pytest.mark.parametrize("ps", PARAM_SETS)
def test_sigma_sign_and_peak_position(ps):
    """Full sigma_zzz(omega): SIGN must be negative (Fregoso D16, t,delta,Delta>0),
    and the dominant peak sits at the lower band edge omega ~ 2 E_min."""
    t, delta, Delta, a = ps["t"], ps["delta"], ps["Delta"], ps["a"]
    # E_min: if t>delta the minimum of E is at ka/2=pi/2 (E^2=delta^2+Delta^2),
    # else at ka/2=0 (E^2=t^2+Delta^2).
    Emin = np.sqrt((delta ** 2 if t > delta else t ** 2) + Delta ** 2)
    edge = 2.0 * Emin
    omega = np.linspace(edge - 0.6, edge + 2.5, 400)
    eta = 0.03
    sig = sc.shift_current_1d_two_band(t, delta, Delta, a, omega,
                                       n_kpts=6000, smearing_eta=eta)
    ipeak = np.argmax(np.abs(sig))
    assert sig[ipeak] < 0.0, f"sign should be negative, got {sig[ipeak]:.3e}"
    assert abs(omega[ipeak] - edge) < 0.15, \
        f"peak at {omega[ipeak]:.3f}, expected near band edge {edge:.3f}"
