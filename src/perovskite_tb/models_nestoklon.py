"""Nestoklon empirical tight-binding model for cubic CsPbI3 (and isostructural).

Source: M. O. Nestoklon, "Tight-binding description of inorganic lead halide
perovskites in cubic phase", arXiv:2012.14705, Table I.  Jancu-Scholz-Beltram-
Bassani sp3d5s* nearest-neighbour Slater-Koster scheme (PRB 57, 6493 (1998)).

Geometry (cubic, lattice constant a):
    * cation c (Pb) at the origin,
    * three anions a (I) on the cubic axes at a/2: I_x, I_y, I_z,
    * nearest-neighbour cation-anion bonds only (length a/2 along the axes),
    * no cation-cation and no anion-anion hopping (nearest-neighbour model).

Each atom carries the basis given in the parameter set (sp3 = 4 orbitals;
sp3d5s* = 10 orbitals).  Atomic gauge is used (see models_kashikar for the
rationale).  Spin-orbit coupling lambda*L.S acts on the p-orbitals of *both*
sublattices, with lambda = Delta_a/3 (anion) and Delta_c/3 (cation), in the
Chadi/Jancu convention where the p-splitting is 3*lambda = Delta
(see _soc.soc_p_from_lambda3).
"""

from __future__ import annotations

from typing import Callable, Mapping, Sequence

import numpy as np

from ._soc import soc_p_from_lambda3
from .slater_koster import sk_element

# Anion sublattices: axis index -> (atom index, unit bond direction cation->anion).
_AXIS_DIR = {0: (1.0, 0.0, 0.0), 1: (0.0, 1.0, 0.0), 2: (0.0, 0.0, 1.0)}


def _otype(orb: str) -> str:
    if orb in ("s", "sstar"):
        return orb
    if orb in ("px", "py", "pz"):
        return "p"
    return "d"


def _bond_integrals(cation_orb: str, anion_orb: str, p: Mapping[str, float]):
    """Return (sigma, pi, delta) for an ordered (cation-orb, anion-orb) pair.

    Integral names follow the Nestoklon JSON convention; zeroed integrals
    (Table I caption) default to 0 if absent.
    """
    ta, tb = _otype(cation_orb), _otype(anion_orb)
    g = lambda k: float(p.get(k, 0.0))  # noqa: E731

    key = (ta, tb)
    if key == ("s", "s"):
        return g("ss_sigma"), 0.0, 0.0
    if key == ("s", "p"):
        return g("sc_pa_sigma"), 0.0, 0.0
    if key == ("s", "d"):
        return g("sc_da_sigma"), 0.0, 0.0
    if key == ("s", "sstar"):
        return g("sc_sstar_a_sigma"), 0.0, 0.0
    if key == ("p", "s"):
        return g("sa_pc_sigma"), 0.0, 0.0
    if key == ("p", "p"):
        return g("pp_sigma"), g("pp_pi"), 0.0
    if key == ("p", "d"):
        return g("pc_da_sigma"), g("pc_da_pi"), 0.0
    if key == ("p", "sstar"):
        return g("sstar_a_pc_sigma"), 0.0, 0.0
    if key == ("d", "s"):
        return g("sa_dc_sigma"), 0.0, 0.0
    if key == ("d", "p"):
        return g("pa_dc_sigma"), g("pa_dc_pi"), 0.0
    if key == ("d", "d"):
        return g("dd_sigma"), g("dd_pi"), g("dd_delta")
    if key == ("d", "sstar"):
        return g("sstar_a_dc_sigma"), 0.0, 0.0
    if key == ("sstar", "s"):
        return g("sa_sstar_c_sigma"), 0.0, 0.0
    if key == ("sstar", "p"):
        return g("sstar_c_pa_sigma"), 0.0, 0.0
    if key == ("sstar", "d"):
        return g("sstar_c_da_sigma"), 0.0, 0.0
    if key == ("sstar", "sstar"):
        return g("sstar_sstar_sigma"), 0.0, 0.0
    raise ValueError(f"no integral mapping for {key}")


def _sk_block(basis: Sequence[str], direction, p: Mapping[str, float]) -> np.ndarray:
    """10x10 (or n_orb^2) SK block <cation-basis[i] | H | anion-basis[j]>."""
    l, m, n = direction
    n_orb = len(basis)
    blk = np.zeros((n_orb, n_orb), dtype=complex)
    for i, oc in enumerate(basis):
        for j, oa in enumerate(basis):
            sig, pi, dl = _bond_integrals(oc, oa, p)
            if sig == 0.0 and pi == 0.0 and dl == 0.0:
                continue
            blk[i, j] = sk_element(oc, oa, l, m, n, sig, pi, dl)
    return blk


def _onsite(basis: Sequence[str], p: Mapping[str, float], role: str) -> np.ndarray:
    """Diagonal on-site energy vector for an atom of the given role ('c' or 'a')."""
    diag = np.zeros(len(basis))
    for i, orb in enumerate(basis):
        t = _otype(orb)
        if t == "s":
            diag[i] = p[f"E_s_{role}"]
        elif t == "p":
            diag[i] = p[f"E_p_{role}"]
        elif t == "d":
            diag[i] = p[f"E_d_{role}"]
        elif t == "sstar":
            diag[i] = p[f"E_sstar_{role}"]
    return diag


def make_builder(params: Mapping[str, float], a: float,
                 basis: Sequence[str]) -> Callable[[np.ndarray], np.ndarray]:
    """Return a Hamiltonian builder H(kvec_cart) -> (N,N) for the Nestoklon model.

    ``basis`` is the per-atom orbital list (4 for sp3, 10 for sp3d5s*).  The
    JSON basis label 'dx2-y2' is normalised to 'dx2y2'.
    """
    _norm = {"dx2-y2": "dx2y2", "s*": "sstar"}
    basis = [_norm.get(b, b) for b in basis]
    n_orb = len(basis)
    n_atom = 4  # cation + 3 anions
    N = n_orb * n_atom

    # Precompute the direction-dependent SK blocks (independent of k).
    plus_blocks = {}
    minus_blocks = {}
    for axis, direction in _AXIS_DIR.items():
        dminus = tuple(-x for x in direction)
        plus_blocks[axis] = _sk_block(basis, direction, params)
        minus_blocks[axis] = _sk_block(basis, dminus, params)

    onsite_c = _onsite(basis, params, "c")
    onsite_a = _onsite(basis, params, "a")

    # Spin-orbit: p indices within an atom block, and lambda for each sublattice.
    p_idx = [i for i, b in enumerate(basis) if b in ("px", "py", "pz")]
    lam_c = params.get("Delta_c_over_3", 0.0)
    lam_a = params.get("Delta_a_over_3", 0.0)
    soc_c = soc_p_from_lambda3(lam_c)  # 6x6 on (px,py,pz)x(up,down)
    soc_a = soc_p_from_lambda3(lam_a)

    def slc(atom: int):
        return slice(atom * n_orb, (atom + 1) * n_orb)

    def builder(kvec: np.ndarray) -> np.ndarray:
        k = np.asarray(kvec, dtype=float)
        H0 = np.zeros((N, N), dtype=complex)
        # On-site blocks.
        H0[slc(0), slc(0)] = np.diag(onsite_c).astype(complex)
        for ax in range(3):
            H0[slc(ax + 1), slc(ax + 1)] = np.diag(onsite_a).astype(complex)
        # Cation-anion hopping (atomic gauge): e^{+i k_d a/2} (home) + e^{-i k_d a/2}.
        for axis, direction in _AXIS_DIR.items():
            kd = float(np.dot(k, direction))  # k_d (cartesian along the axis)
            phase = np.exp(1j * kd * a / 2.0)
            block = plus_blocks[axis] * phase + minus_blocks[axis] * np.conj(phase)
            H0[slc(0), slc(axis + 1)] = block
            H0[slc(axis + 1), slc(0)] = block.conj().T

        # Spinful Hamiltonian (spin-major): block-diag(H0, H0) + SOC.
        H = np.kron(np.eye(2, dtype=complex), H0)
        if p_idx:
            # Embed atom-resolved SOC on p-orbitals of every atom.
            for atom, soc in [(0, soc_c), (1, soc_a), (2, soc_a), (3, soc_a)]:
                full_idx = [s * N + atom * n_orb + o for s in (0, 1) for o in p_idx]
                for ai, A in enumerate(full_idx):
                    for bi, B in enumerate(full_idx):
                        H[A, B] += soc[ai, bi]
        return H

    return builder
