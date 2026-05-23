"""Validation of the general Slater-Koster two-centre engine.

External check: hand-derived matrix elements for a bond along +x (l,m,n)=(1,0,0),
worked out from Slater-Koster (1954) Table I.
Internal check: the fundamental two-centre relation E_ab(d) = E_ba(-d).
"""

import itertools
import math

import numpy as np
import pytest

from perovskite_tb.slater_koster import sk_element

SQRT3 = math.sqrt(3.0)
ALL_ORB = ["s", "px", "py", "pz", "dxy", "dyz", "dzx", "dx2y2", "dz2", "sstar"]


def test_x_bond_ss_sp():
    assert sk_element("s", "s", 1, 0, 0, sigma=0.7) == pytest.approx(0.7)
    assert sk_element("s", "px", 1, 0, 0, sigma=0.5) == pytest.approx(0.5)
    assert sk_element("s", "py", 1, 0, 0, sigma=0.5) == pytest.approx(0.0)
    assert sk_element("s", "pz", 1, 0, 0, sigma=0.5) == pytest.approx(0.0)
    # p first -> sign flip
    assert sk_element("px", "s", 1, 0, 0, sigma=0.5) == pytest.approx(-0.5)


def test_x_bond_pp():
    assert sk_element("px", "px", 1, 0, 0, sigma=2.0, pi=0.3) == pytest.approx(2.0)
    assert sk_element("py", "py", 1, 0, 0, sigma=2.0, pi=0.3) == pytest.approx(0.3)
    assert sk_element("pz", "pz", 1, 0, 0, sigma=2.0, pi=0.3) == pytest.approx(0.3)
    assert sk_element("px", "py", 1, 0, 0, sigma=2.0, pi=0.3) == pytest.approx(0.0)


def test_x_bond_sd():
    sd = 0.6
    assert sk_element("s", "dx2y2", 1, 0, 0, sigma=sd) == pytest.approx(SQRT3 / 2 * sd)
    assert sk_element("s", "dz2", 1, 0, 0, sigma=sd) == pytest.approx(-0.5 * sd)
    for d in ("dxy", "dyz", "dzx"):
        assert sk_element("s", d, 1, 0, 0, sigma=sd) == pytest.approx(0.0)


def test_x_bond_pd():
    pds, pdp = 1.0, 0.0
    assert sk_element("px", "dx2y2", 1, 0, 0, sigma=pds, pi=pdp) == pytest.approx(SQRT3 / 2)
    assert sk_element("px", "dz2", 1, 0, 0, sigma=pds, pi=pdp) == pytest.approx(-0.5)
    # d first -> sign flip
    assert sk_element("dx2y2", "px", 1, 0, 0, sigma=pds, pi=pdp) == pytest.approx(-SQRT3 / 2)
    assert sk_element("dz2", "px", 1, 0, 0, sigma=pds, pi=pdp) == pytest.approx(0.5)


def test_x_bond_dd():
    s, p, d = 1.3, 0.5, -0.2
    assert sk_element("dxy", "dxy", 1, 0, 0, s, p, d) == pytest.approx(p)
    assert sk_element("dyz", "dyz", 1, 0, 0, s, p, d) == pytest.approx(d)
    assert sk_element("dzx", "dzx", 1, 0, 0, s, p, d) == pytest.approx(p)
    assert sk_element("dx2y2", "dx2y2", 1, 0, 0, s, p, d) == pytest.approx(0.75 * s + 0.25 * d)
    assert sk_element("dz2", "dz2", 1, 0, 0, s, p, d) == pytest.approx(0.25 * s + 0.75 * d)
    assert sk_element("dx2y2", "dz2", 1, 0, 0, s, p, d) == pytest.approx(-SQRT3 / 4 * s + SQRT3 / 4 * d)


def test_sstar_behaves_like_s_angularly():
    # s* has the same angular form as s.
    for d in (1, 0, 0), (0, 1, 0), (0.3, -0.4, 0.5):
        l, m, n = d
        assert sk_element("sstar", "px", l, m, n, sigma=0.9) == pytest.approx(
            sk_element("s", "px", l, m, n, sigma=0.9))


@pytest.mark.parametrize("orbA,orbB", list(itertools.product(ALL_ORB, ALL_ORB)))
def test_two_centre_parity_relation(orbA, orbB):
    """E_ab(l,m,n) == E_ba(-l,-m,-n) for arbitrary direction and integrals."""
    rng = np.random.default_rng(0)
    v = rng.normal(size=3)
    v /= np.linalg.norm(v)
    l, m, n = v
    s, p, d = 1.1, -0.4, 0.25
    e1 = sk_element(orbA, orbB, l, m, n, s, p, d)
    e2 = sk_element(orbB, orbA, -l, -m, -n, s, p, d)
    assert e1 == pytest.approx(e2, abs=1e-12)
