"""General two-centre Slater-Koster integrals for s, p, d (and s*) orbitals.

Reference: J. C. Slater and G. F. Koster, "Simplified LCAO Method for the
Periodic Potential Problem", Phys. Rev. 94, 1498 (1954), Table I.

We compute ``<orbA(atom1) | H | orbB(atom2)>`` where ``(l, m, n)`` are the
direction cosines of the bond vector from atom1 to atom2, given the two-centre
integrals (sigma, pi, delta) appropriate to the *ordered* orbital pair.

Heteropolar bonds: the (sigma, pi, delta) values may differ for (s1,p2) versus
(p1,s2); the caller supplies the correct values for the ordered pair, so this
module only handles the angular part.  Orbitals of higher angular momentum
placed first are handled via the parity relation

    E_{beta,alpha}(l,m,n) = (-1)^(l_alpha + l_beta) E_{alpha,beta}(l,m,n),

so we only implement the canonical table for (sA <= sB) and flip otherwise.

Orbital name convention:
    s-type : 's', 'sstar'  (angular momentum 0; identical angular form)
    p-type : 'px', 'py', 'pz'
    d-type : 'dxy', 'dyz', 'dzx', 'dx2y2', 'dz2'   (dz2 == d_{3z^2-r^2})
"""

from __future__ import annotations

import math

SQRT3 = math.sqrt(3.0)

_S = {"s", "sstar"}
_P = {"px", "py", "pz"}
_D = {"dxy", "dyz", "dzx", "dx2y2", "dz2"}


def _ang_mom(orb: str) -> int:
    if orb in _S:
        return 0
    if orb in _P:
        return 1
    if orb in _D:
        return 2
    raise ValueError(f"unknown orbital '{orb}'")


def _p_comp(orb: str):
    return {"px": 0, "py": 1, "pz": 2}[orb]


def sk_element(orbA: str, orbB: str, l: float, m: float, n: float,
               sigma: float = 0.0, pi: float = 0.0, delta: float = 0.0) -> float:
    """Two-centre matrix element <orbA(1)|H|orbB(2)>, bond direction (l,m,n) 1->2.

    ``sigma, pi, delta`` are the two-centre integrals for this ordered pair.
    """
    la, lb = _ang_mom(orbA), _ang_mom(orbB)
    if la > lb:
        # Use parity relation; same integral values, swapped orbitals.
        sign = (-1.0) ** (la + lb)
        return sign * sk_element(orbB, orbA, l, m, n, sigma, pi, delta)

    # Canonical orderings: (s,s), (s,p), (s,d), (p,p), (p,d), (d,d).
    if la == 0 and lb == 0:           # s - s
        return sigma
    if la == 0 and lb == 1:           # s - p
        return (l, m, n)[_p_comp(orbB)] * sigma
    if la == 0 and lb == 2:           # s - d
        return _s_d(orbB, l, m, n, sigma)
    if la == 1 and lb == 1:           # p - p
        i, j = _p_comp(orbA), _p_comp(orbB)
        di = (l, m, n)[i]
        dj = (l, m, n)[j]
        return di * dj * (sigma - pi) + (1.0 if i == j else 0.0) * pi
    if la == 1 and lb == 2:           # p - d
        return _p_d(orbA, orbB, l, m, n, sigma, pi)
    if la == 2 and lb == 2:           # d - d
        return _d_d(orbA, orbB, l, m, n, sigma, pi, delta)
    raise AssertionError("unreachable")


def _s_d(d: str, l: float, m: float, n: float, sigma: float) -> float:
    if d == "dxy":
        return SQRT3 * l * m * sigma
    if d == "dyz":
        return SQRT3 * m * n * sigma
    if d == "dzx":
        return SQRT3 * l * n * sigma
    if d == "dx2y2":
        return (SQRT3 / 2.0) * (l * l - m * m) * sigma
    if d == "dz2":
        return (n * n - (l * l + m * m) / 2.0) * sigma
    raise ValueError(d)


def _p_d(p: str, d: str, l: float, m: float, n: float, sigma: float, pi: float) -> float:
    s3 = SQRT3
    # Map by (p-component, d-orbital). Standard Slater-Koster Table I (p first).
    table = {
        ("px", "dxy"): s3 * l * l * m * sigma + m * (1 - 2 * l * l) * pi,
        ("px", "dyz"): s3 * l * m * n * sigma - 2 * l * m * n * pi,
        ("px", "dzx"): s3 * l * l * n * sigma + n * (1 - 2 * l * l) * pi,
        ("py", "dxy"): s3 * m * m * l * sigma + l * (1 - 2 * m * m) * pi,
        ("py", "dyz"): s3 * m * m * n * sigma + n * (1 - 2 * m * m) * pi,
        ("py", "dzx"): s3 * l * m * n * sigma - 2 * l * m * n * pi,
        ("pz", "dxy"): s3 * l * m * n * sigma - 2 * l * m * n * pi,
        ("pz", "dyz"): s3 * n * n * m * sigma + m * (1 - 2 * n * n) * pi,
        ("pz", "dzx"): s3 * n * n * l * sigma + l * (1 - 2 * n * n) * pi,
        ("px", "dx2y2"): (s3 / 2.0) * l * (l * l - m * m) * sigma + l * (1 - l * l + m * m) * pi,
        ("py", "dx2y2"): (s3 / 2.0) * m * (l * l - m * m) * sigma - m * (1 + l * l - m * m) * pi,
        ("pz", "dx2y2"): (s3 / 2.0) * n * (l * l - m * m) * sigma - n * (l * l - m * m) * pi,
        ("px", "dz2"): l * (n * n - (l * l + m * m) / 2.0) * sigma - s3 * l * n * n * pi,
        ("py", "dz2"): m * (n * n - (l * l + m * m) / 2.0) * sigma - s3 * m * n * n * pi,
        ("pz", "dz2"): n * (n * n - (l * l + m * m) / 2.0) * sigma + s3 * n * (l * l + m * m) * pi,
    }
    return table[(p, d)]


def _d_d(d1: str, d2: str, l: float, m: float, n: float,
         sigma: float, pi: float, delta: float) -> float:
    s3 = SQRT3
    ll, mm, nn = l * l, m * m, n * n
    lm2 = ll - mm  # (l^2 - m^2)
    # Diagonal entries.
    diag = {
        "dxy": 3 * ll * mm * sigma + (ll + mm - 4 * ll * mm) * pi + (nn + ll * mm) * delta,
        "dyz": 3 * mm * nn * sigma + (mm + nn - 4 * mm * nn) * pi + (ll + mm * nn) * delta,
        "dzx": 3 * nn * ll * sigma + (nn + ll - 4 * nn * ll) * pi + (mm + nn * ll) * delta,
        "dx2y2": (3.0 / 4.0) * lm2 * lm2 * sigma + (ll + mm - lm2 * lm2) * pi
                 + (nn + 0.25 * lm2 * lm2) * delta,
        "dz2": (nn - (ll + mm) / 2.0) ** 2 * sigma + 3 * nn * (ll + mm) * pi
               + (3.0 / 4.0) * (ll + mm) ** 2 * delta,
    }
    if d1 == d2:
        return diag[d1]

    # Off-diagonal entries (symmetric: order within the pair does not matter for d-d).
    pair = frozenset((d1, d2))
    off = {
        frozenset(("dxy", "dyz")): 3 * l * mm * n * sigma + l * n * (1 - 4 * mm) * pi
                                   + l * n * (mm - 1) * delta,
        frozenset(("dxy", "dzx")): 3 * ll * m * n * sigma + m * n * (1 - 4 * ll) * pi
                                   + m * n * (ll - 1) * delta,
        frozenset(("dyz", "dzx")): 3 * m * nn * l * sigma + m * l * (1 - 4 * nn) * pi
                                   + m * l * (nn - 1) * delta,
        frozenset(("dxy", "dx2y2")): (3.0 / 2.0) * l * m * lm2 * sigma
                                     + 2 * l * m * (mm - ll) * pi
                                     + 0.5 * l * m * lm2 * delta,
        frozenset(("dyz", "dx2y2")): (3.0 / 2.0) * m * n * lm2 * sigma
                                     - m * n * (1 + 2 * lm2) * pi
                                     + m * n * (1 + lm2 / 2.0) * delta,
        frozenset(("dzx", "dx2y2")): (3.0 / 2.0) * n * l * lm2 * sigma
                                     + n * l * (1 - 2 * lm2) * pi
                                     - n * l * (1 - lm2 / 2.0) * delta,
        frozenset(("dxy", "dz2")): s3 * l * m * (nn - (ll + mm) / 2.0) * sigma
                                   - 2 * s3 * l * m * nn * pi
                                   + (s3 / 2.0) * l * m * (1 + nn) * delta,
        frozenset(("dyz", "dz2")): s3 * m * n * (nn - (ll + mm) / 2.0) * sigma
                                   + s3 * m * n * (ll + mm - nn) * pi
                                   - (s3 / 2.0) * m * n * (ll + mm) * delta,
        frozenset(("dzx", "dz2")): s3 * l * n * (nn - (ll + mm) / 2.0) * sigma
                                   + s3 * l * n * (ll + mm - nn) * pi
                                   - (s3 / 2.0) * l * n * (ll + mm) * delta,
        frozenset(("dx2y2", "dz2")): (s3 / 2.0) * lm2 * (nn - (ll + mm) / 2.0) * sigma
                                     + s3 * nn * (mm - ll) * pi
                                     + (s3 / 4.0) * (1 + nn) * lm2 * delta,
    }
    return off[pair]
