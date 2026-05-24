# SPDX-License-Identifier: MIT
# Copyright (c) 2026 tk
"""Circular photogalvanic effect (CPGE) / injection current (spec F7).

Second-order injection-current response to circularly polarized light in
inversion-broken systems.  Built on the velocity operator and the Berry
curvature of :mod:`berry`.

Sources (verified real & open-access, 2026-05-24; formula read from the source):
* J. E. Sipe, A. I. Shkrebtii, "Second-order optical response in
  semiconductors", Phys. Rev. B 61, 5337 (2000), DOI 10.1103/PhysRevB.61.5337.
  Injection ("circular") current formalism.
* F. de Juan, A. G. Grushin, T. Morimoto, J. E. Moore, "Quantized circular
  photogalvanic effect in Weyl semimetals", Nat. Commun. 8, 15995 (2017),
  DOI 10.1038/ncomms15995 (arXiv:1611.05887).  CPGE injection tensor and its
  topological quantization.

CPGE injection tensor (de Juan 2017; read from ar5iv:1611.05887):
    beta_{ij}(omega) = (pi e^3 / hbar V) eps_{jkl} sum_{k,n,m} f_{nm}
                       Delta^i_{nm} r^k_{nm} r^l_{mn} delta(hbar omega - E_{mn})
with the cross-gap Berry connection  r^a_{nm} = -i v^a_{nm} / E_{nm}  (n != m),
the band-velocity difference  Delta^i_{nm} = d(E_n - E_m)/dk_i = v^i_{nn}-v^i_{mm},
and  f_{nm} = f_n - f_m.  For two bands this reduces (de Juan Eq.) to
    beta_{ij} = (i pi e^3 / hbar^2 V) sum_k (d E_{12}/dk_i) Omega^j_1
                delta(hbar omega - E_{21}),
i.e. the velocity difference times the lower-band Berry-curvature vector
(reusing berry.berry_curvature_kubo).  Both forms are implemented and shown to
agree.

Topological quantization (de Juan 2017): for a single Weyl node of Chern number
C, Tr[beta] = i pi (e^3/h^2) C in the resonant window -> the trace is a
frequency-INDEPENDENT plateau proportional to C.

Units: hbar = e = 1.  beta is returned as the real coefficient (the physical
tensor is i*beta_real).  The absolute prefactor follows de Juan (pi e^3/h^2);
we validate the formula reduction (r -> Omega), the inversion symmetry
(beta = 0), and the quantization STRUCTURE (omega-independent plateau, chirality
sign flip).  Absolute magnitude for a real material additionally carries the TB
position-operator (Blount) limitation -> relative/structural use.
"""

from __future__ import annotations

import numpy as np

from . import berry

# Levi-Civita symbol
_EPS = np.zeros((3, 3, 3))
for _i, _j, _k in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
    _EPS[_i, _j, _k] = 1.0
    _EPS[_i, _k, _j] = -1.0


def cross_gap_connection(V, evals, n, m):
    """Cross-gap Berry connection r^a_{nm} = -i v^a_{nm}/(E_n-E_m), a=x,y,z.

    ``V`` is the list/array of three band-basis velocity matrices V[a]=U^dag dH_a U.
    """
    Enm = evals[n] - evals[m]
    return np.array([-1j * V[a][n, m] / Enm for a in range(3)])


def berry_curvature_vector(evals, evecs, dH, band):
    """Berry-curvature vector (Omega_yz, Omega_zx, Omega_xy) of ``band``."""
    ox = berry.berry_curvature_kubo(evals, evecs, dH[1], dH[2])[band]
    oy = berry.berry_curvature_kubo(evals, evecs, dH[2], dH[0])[band]
    oz = berry.berry_curvature_kubo(evals, evecs, dH[0], dH[1])[band]
    return np.array([ox, oy, oz])


def _gaussian(x, eta):
    return np.exp(-0.5 * (x / eta) ** 2) / (eta * np.sqrt(2.0 * np.pi))


def cpge_tensor(kpts, H_fn, dHk_fn, omega, eta, *, n_occ=None, e_fermi=None,
                measure=1.0):
    """CPGE injection tensor beta_ij(omega) via the general de Juan formula.

    Returns the real 3x3 coefficient (physical tensor = i*beta_real), in units
    with hbar=e=1 and prefactor pi; ``measure`` multiplies (e.g. dk^3/(2pi)^3
    for an absolute BZ integral, else the per-k average is returned).
    """
    kpts = np.asarray(kpts, dtype=float)
    nk = len(kpts)

    # Build (K, d, d) stacks for H and dH/dk (use a batch-aware builder if the
    # callable advertises it, else stack per-k); then batched eigh + velocities.
    def _stack(fn, *args):
        if getattr(fn, "_batched", False):
            return np.asarray(fn(kpts, *args))
        return np.stack([fn(k, *args) for k in kpts])

    Hs = _stack(H_fn)
    Hs = 0.5 * (Hs + Hs.conj().transpose(0, 2, 1))
    evals, evecs = np.linalg.eigh(Hs)                       # (K,d), (K,d,d)
    Uh = evecs.conj().transpose(0, 2, 1)
    V = [Uh @ _stack(dHk_fn, a) @ evecs for a in range(3)]  # band-basis velocities

    d = evals.shape[1]
    if e_fermi is not None:
        occ = evals < e_fermi                               # (K,d)
    else:
        occ = np.broadcast_to(np.arange(d)[None, :] < n_occ, evals.shape)

    # Pairwise (n,m) tensors, vectorised over k (this replaces the n,m,k loops).
    En, Em = evals[:, :, None], evals[:, None, :]           # E_n, E_m at [k,n,m]
    Emn, dE = Em - En, En - Em
    valid = (occ[:, :, None] & ~occ[:, None, :]) & (Emn > 1e-9)   # n occ, m unocc, resonant
    w = _gaussian(omega - Emn, eta) * valid                 # 0 where invalid
    safe_dE = np.where(np.abs(dE) > 1e-12, dE, 1.0)
    # Delta^a_nm = V^a_nn - V^a_mm ; cross-gap connections r^a_nm, r^a_mn
    Vd = [np.real(np.diagonal(V[a], axis1=1, axis2=2)) for a in range(3)]   # (K,d)
    Delta = np.stack([Vd[a][:, :, None] - Vd[a][:, None, :] for a in range(3)], axis=-1)
    r_nm = np.stack([-1j * V[a] / safe_dE for a in range(3)], axis=-1)       # -i V_nm/(E_n-E_m)
    r_mn = np.stack([-1j * V[a].transpose(0, 2, 1) / (-safe_dE) for a in range(3)], axis=-1)
    rr = -np.imag(np.cross(r_nm, r_mn, axis=-1))            # = Omega^j_n (Xiao convention)
    beta = np.pi * np.einsum("knmi,knmj->ij", Delta * w[..., None], rr)
    return beta * measure / nk


def cpge_tensor_2band(kpts, H_fn, dHk_fn, omega, eta, *, measure=1.0):
    """CPGE tensor via the two-band Berry-curvature form (lower band occupied).

    beta_ij = pi sum_k (dE12/dk_i) Omega^j_1 delta(omega - E21) ; for validation
    against :func:`cpge_tensor` on two-band models.
    """
    beta = np.zeros((3, 3))
    nk = len(kpts)
    for kv in kpts:
        H = H_fn(kv)
        evals, evecs = np.linalg.eigh(0.5 * (H + H.conj().T))
        dH = [dHk_fn(kv, a) for a in range(3)]
        V = [evecs.conj().T @ dH[a] @ evecs for a in range(3)]
        Delta = np.array([V[a][0, 0].real - V[a][1, 1].real for a in range(3)])
        Om = berry_curvature_vector(evals, evecs, dH, band=0)
        E21 = evals[1] - evals[0]
        beta += np.pi * np.outer(Delta, Om) * _gaussian(omega - E21, eta)
    return beta * measure / nk
