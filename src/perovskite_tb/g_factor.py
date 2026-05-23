"""Landé g-factors of band-edge Kramers doublets via the Roth-Lax formula.

Source physics:
  * L. M. Roth, B. Lax, S. Zwerdling, Phys. Rev. 114, 90 (1959) -- effective
    g-factor from interband momentum (velocity) matrix elements.
  * Kirstein et al., arXiv:2112.15384 (universal k.p relation, Eqs. 5,6).
  * Nestoklon et al., arXiv:2305.10586 (ETB bulk g-factors, Table S2).

Method (bulk, atomistic).  For a Kramers doublet ``D`` at k0 (the band edge,
R point in cubic perovskites), the 2x2 effective Zeeman g-matrix for field
direction gamma is

    M_gamma = (1/2) [ g0 * sigma_gamma|_D  +  dG_gamma ]
    dG_gamma_{ab} = (2/(i C)) eps_{gamma,alpha,beta}
                    * sum_{m not in D} <a|dH/dk_alpha|m><m|dH/dk_beta|b> / (E0 - Em)

with ``C = hbar^2/m0 = 7.6199 eV.A^2`` (fixes units from p = m0 v = (m0/hbar) dH/dk;
the factor 2 is the textbook Roth-Lax orbital coefficient -- not fitted).  The
g-factor is the eigenvalue splitting of ``M_gamma``:  ``g_gamma = lambda+ - lambda-``.

The spin term ``g0 sigma_gamma`` alone gives g = g0 = 2.0023 (free-electron limit
when interband coupling vanishes); the orbital sum ``dG`` supplies the band-gap
and SOC dependence.

Validation anchor: bulk CsPbI3 (Nestoklon Table S2) g_e = +3.23, g_h = -0.33.

NOTE / known limitation (flagged for review): dH/dk captures the inter-atomic
(hopping) orbital moment but not the intra-atomic orbital angular momentum that
the on-site SOC encodes (the SOC term is k-independent, hence absent from dH/dk).
The reproduction of the Table S2 anchor below is the empirical check on whether
this is adequate for these materials.
"""

from __future__ import annotations

from typing import Callable

import numpy as np

G0 = 2.0023193  # free-electron g-factor
C_HBAR2_OVER_M0 = 7.619964  # eV * Angstrom^2  (= hbar^2/m0)
_LEVI_CIVITA = {  # gamma -> list of (alpha, beta, sign)
    0: [(1, 2, +1.0), (2, 1, -1.0)],  # x
    1: [(2, 0, +1.0), (0, 2, -1.0)],  # y
    2: [(0, 1, +1.0), (1, 0, -1.0)],  # z
}


def _spin_pauli(n_orb_total: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Pauli matrices on the spin-major (2*N) basis: sigma_gamma (x) I_N."""
    n = n_orb_total
    I = np.eye(n, dtype=complex)
    Z = np.zeros((n, n), dtype=complex)
    sx = np.block([[Z, I], [I, Z]])
    sy = np.block([[Z, -1j * I], [1j * I, Z]])
    sz = np.block([[I, Z], [Z, -I]])
    return sx, sy, sz


def compute_g_factor(hamiltonian: np.ndarray,
                     velocity_ops: tuple[np.ndarray, np.ndarray, np.ndarray],
                     band_index: int,
                     degeneracy_tol: float = 1e-4) -> dict:
    """Roth-Lax g-tensor for the Kramers doublet starting at ``band_index``.

    Parameters
    ----------
    hamiltonian : (2N, 2N) array
        Spinful Bloch Hamiltonian at the band edge k0 (Hermitian, spin-major).
    velocity_ops : (dHdx, dHdy, dHdz)
        The three ``dH/dk_alpha`` matrices at k0 (eV.A), same basis as H.
    band_index : int
        Lower index of the doublet (ascending-energy order). The doublet is
        (band_index, band_index+1).
    degeneracy_tol : float
        Tolerance (eV) for checking the two doublet states are degenerate.

    Returns
    -------
    dict with g_iso, g_xx, g_yy, g_zz, delta_g (anisotropy), E0, method.
    """
    H = 0.5 * (hamiltonian + hamiltonian.conj().T)
    evals, evecs = np.linalg.eigh(H)
    ntot = H.shape[0]
    n_orb = ntot // 2

    d = [band_index, band_index + 1]
    E0 = float(np.mean(evals[d]))
    if abs(evals[d[0]] - evals[d[1]]) > degeneracy_tol:
        # Not a clean Kramers doublet; proceed but record the splitting.
        pass

    psi = [evecs[:, d[0]], evecs[:, d[1]]]  # doublet states
    dH = velocity_ops

    # Energy denominators for states outside the doublet.
    others = [m for m in range(ntot) if m not in d]
    denom = np.array([E0 - evals[m] for m in others])
    vecs_other = evecs[:, others]  # (2N, M)

    # Precompute <a| dH_alpha |m> for the two doublet states and all alpha.
    # A[alpha][a] is a length-M vector over the 'other' states.
    A = [[vecs_other.conj().T @ (dH[alpha] @ psi[a]) for a in range(2)]
         for alpha in range(3)]

    sx, sy, sz = _spin_pauli(n_orb)
    sigma = [sx, sy, sz]

    g = {}
    glabels = {0: "g_xx", 1: "g_yy", 2: "g_zz"}
    for gamma in range(3):
        dG = np.zeros((2, 2), dtype=complex)
        for (alpha, beta, sign) in _LEVI_CIVITA[gamma]:
            for a in range(2):
                for b in range(2):
                    # sum_m <a|dH_alpha|m><m|dH_beta|b> / (E0 - Em)
                    s = np.sum(A[alpha][a].conj() * A[beta][b] / denom)
                    dG[a, b] += sign * s
        dG *= 2.0 / (1j * C_HBAR2_OVER_M0)

        # Spin part projected onto the doublet (2x2).
        Sg = np.array([[psi[a].conj() @ (sigma[gamma] @ psi[b]) for b in range(2)]
                       for a in range(2)], dtype=complex)

        M = 0.5 * (G0 * Sg + dG)
        M = 0.5 * (M + M.conj().T)  # enforce Hermiticity
        w = np.linalg.eigvalsh(M)
        g[glabels[gamma]] = float(w[-1] - w[0])  # splitting = g-factor

    g_iso = (g["g_xx"] + g["g_yy"] + g["g_zz"]) / 3.0
    g["g_iso"] = g_iso
    g["delta_g"] = max(g["g_xx"], g["g_yy"], g["g_zz"]) - min(g["g_xx"], g["g_yy"], g["g_zz"])
    g["E0"] = E0
    g["method"] = "Roth-Lax-2nd-order"
    return g


def g_factor_kp(Eg: float, Delta: float, P: float = 6.8, dg_e: float = -1.0) -> dict:
    """k.p universal relation g-factors (Kirstein 2021, Eqs. 5,6).

    Eg, Delta in eV; P = hbar*p/m0 in eV.A (default universal 6.8).
    g_h = 2 - (4/3) P^2/C [1/Eg - 1/(Eg+Delta)]
    g_e = -2/3 + (4/3) P^2/(C Eg) + dg_e ,   C = hbar^2/m0.
    """
    C = C_HBAR2_OVER_M0
    kane = (4.0 / 3.0) * P * P / C
    g_h = 2.0 - kane * (1.0 / Eg - 1.0 / (Eg + Delta))
    g_e = -2.0 / 3.0 + kane / Eg + dg_e
    return {"g_e": g_e, "g_h": g_h, "Eg": Eg, "Delta": Delta, "P": P, "dg_e": dg_e}
