"""V&V for thermo.py (spec F9): Boltzmann transport in the CRTA.

Exact anchors (independent of band details):
  * Wiedemann-Franz: in the degenerate limit the Lorenz number
    kappa^e/(sigma T) -> (pi^2/3)(k_B/e)^2.
  * Sommerfeld Seebeck: S ~ -(pi^2/3)(k_B T)(d ln Sigma/de)|_mu.

The transport-coefficient core is validated on the analytic transport
distribution Sigma(e) = e^{3/2} of a 3D parabolic band (decoupled from
k-sampling); the Sigma builder is checked separately for the e^{3/2} shape.
"""

import numpy as np

from perovskite_tb import thermo
from perovskite_tb.thermo import KB_EV

PI2_3 = np.pi ** 2 / 3.0


def _analytic_sigma(emax=6.0, n=6000):
    """Sigma(e) = e^{3/2} for e>0 (3D parabolic electron band), fine grid."""
    egrid = np.linspace(1e-3, emax, n)
    Sigma = egrid ** 1.5
    return egrid, Sigma


def test_wiedemann_franz_degenerate_limit():
    egrid, Sigma = _analytic_sigma()
    out = thermo.transport_coefficients(egrid, Sigma, mu=3.0, T=300.0)
    assert np.isclose(out["lorenz_kB_e2"], PI2_3, rtol=5e-3), \
        f"Lorenz {out['lorenz_kB_e2']:.5f} vs pi^2/3={PI2_3:.5f}"


def test_seebeck_sign_and_sommerfeld():
    egrid, Sigma = _analytic_sigma()
    mu, T = 3.0, 300.0
    out = thermo.transport_coefficients(egrid, Sigma, mu, T)
    assert out["seebeck_kB_e"] < 0.0  # electron-like (Sigma increasing)
    s_analytic = -(PI2_3) * (KB_EV * T) * (1.5 / mu)  # d lnSigma/de = 1.5/mu
    assert np.isclose(out["seebeck_kB_e"], s_analytic, rtol=0.05), \
        f"S {out['seebeck_kB_e']:.4e} vs Sommerfeld {s_analytic:.4e}"


def test_hole_band_positive_seebeck():
    # decreasing Sigma near mu -> hole-like -> S > 0; WF still holds
    egrid = np.linspace(1e-3, 6.0, 6000)
    Sigma = (6.0 - egrid) ** 1.5
    out = thermo.transport_coefficients(egrid, Sigma, mu=3.0, T=300.0)
    assert out["seebeck_kB_e"] > 0.0
    assert np.isclose(out["lorenz_kB_e2"], PI2_3, rtol=5e-3)


def test_sigma_and_kappa_positive():
    egrid, Sigma = _analytic_sigma()
    out = thermo.transport_coefficients(egrid, Sigma, mu=2.5, T=300.0)
    assert out["sigma_over_tau"] > 0.0
    assert out["kappa_e_over_tau"] > 0.0


def test_transport_distribution_shape():
    """Sigma builder on a 3D parabolic band ~ e^{3/2} in a smooth region."""
    hbar2_over_m0 = 7.619964
    c = hbar2_over_m0 / 0.5
    ks = np.linspace(-1.4, 1.4, 61)
    KX, KY, KZ = np.meshgrid(ks, ks, ks, indexing="ij")
    E = 0.5 * c * (KX ** 2 + KY ** 2 + KZ ** 2)
    vx = c * KX
    egrid = np.linspace(0.05, 3.0, 400)
    Sigma = thermo.transport_distribution(E.ravel(), vx.ravel(), egrid, eta=0.08)
    # fit log Sigma vs log e in a well-sampled mid-range -> slope ~ 1.5
    sel = (egrid > 0.5) & (egrid < 2.0) & (Sigma > 0)
    slope = np.polyfit(np.log(egrid[sel]), np.log(Sigma[sel]), 1)[0]
    assert 1.2 < slope < 1.8, f"Sigma exponent {slope:.2f} (expected ~1.5)"


def test_perovskite_runs_sensible():
    from perovskite_tb.io_params import get_material, load_parameter_file
    m = get_material(load_parameter_file("data/parameters/kashikar2021_cubic_13orb.json"), "CsPbI3")
    p, a = m["params"], m["a"]
    rng = np.random.default_rng(0)
    kpts = rng.uniform(-0.5, 0.5, size=(200, 3)) * (2 * np.pi / a)
    E, vx = thermo.band_group_velocities_kashikar13(kpts, p, a)
    egrid = np.linspace(E.min(), E.max(), 400)
    Sigma = thermo.transport_distribution(E, vx, egrid, eta=0.1)
    out = thermo.transport_coefficients(egrid, Sigma, mu=float(np.median(E)), T=300.0)
    assert out["sigma_over_tau"] >= 0.0
    assert np.isfinite(out["seebeck_kB_e"])
    assert out["lorenz_kB_e2"] > 0.0
