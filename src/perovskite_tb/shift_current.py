"""Shift-current bulk photovoltaic effect (BPVE) for halide perovskites.

Implements the shift-current conductivity sigma^(2)_abc(omega) (Young & Rappe 2012,
PRL 109, 116601 / arXiv:1202.3168, Eqs. 1-3; Sipe-Shkrebtii 2000, PRB 61, 5337;
velocity-gauge formulation Passos et al. 2018, arXiv:1712.04924).

Young & Rappe Eq.(1)-(3) factorised form:
    sigma_{rsq}(w) = e * sum_{vc} Int dk  I_{rs}(v,c,k;w) * R_q(v,c,k)
    I_{rs}  ~ (f_v - f_c) <v|P_r|c><c|P_s|v> delta(w_cv - w)         (transition intensity ~ Im eps)
    R_q     = -d_q arg(<v|P_r|c>) - (chi^q_c - chi^q_v)             (shift vector)

We compute the diagonal component sigma_{zzz}(omega). The momentum matrix element
P_r = m0 v_r = (m0/hbar) dH/dk_r is reused from velocity.py (same operator as the
g-factor and optical modules).

The production routine ``shift_current_zzz`` uses the **velocity-gauge
sum-over-states** form of the generalized (covariant) derivative (Aversa-Sipe 1995;
Sipe-Shkrebtii 2000; Passos 2018) -- it needs no k-derivative gauge fixing and
handles the Kramers (SOC) degeneracy by skipping degenerate intermediate states, so
the centrosymmetric vanishing at delta=0 holds to machine precision (~1e-15). The
earlier Abelian discrete-link routine (``shift_current_zzz_abelian_deprecated``)
fails this because the band-diagonal link is ill-defined for degenerate bands; it
is kept only for regression comparison.

Symmetry (docs/shift-current-formulation.md sec.4): cubic Pm-3m is centrosymmetric
=> sigma^(2) == 0.  We break inversion with a [001] **polar displacement** of the B
cation (Pb) by delta (Angstrom) against the halide cage (-> P4mm), scaling the
asymmetric Pb-I_z bond hoppings by the Harrison law t(d)=t(d0)(d0/d)^eta with the
universal eta=2.0 (W. A. Harrison, Electronic Structure and the Properties of
Solids, Dover 1989, Eq. 20-5; valid for the s,p basis of Kashikar/Nestoklon).

Units: sigma_{zzz} here is in *relative* units (consistent prefactor); absolute
calibration to uA/V^2 vs Tan & Rappe 2016 is deferred to F4.  Limitation: like the
g-factor and optical f-sum, the TB velocity operator omits intra-atomic position
contributions (Blount 1962), so absolute amplitudes are expected low; the
*symmetry* (vanishing at delta=0) and *spectral shape / band-edge onset* are robust.
"""

from __future__ import annotations

from typing import Callable

import numpy as np

from . import models_nestoklon as mn
from ._soc import soc_p_from_lambda3


def harrison_scaled_hopping(t0: float, d0: float, d: float, eta: float = 2.0) -> float:
    """Harrison universal distance scaling of a TB hopping integral.

    t(d) = t(d0) * (d0/d)^eta.
    Ref: W. A. Harrison, *Electronic Structure and the Properties of Solids*
    (Dover, 1989), Eq. (20-5). Default eta=2 is the universal value for s-p
    systems (no d-orbitals in the Kashikar/Nestoklon basis).
    """
    return t0 * (d0 / d) ** eta


# --------------------------------------------------------------------------- #
# Polar-displaced Nestoklon Hamiltonian ([001] Pb off-centering, P4mm)
# --------------------------------------------------------------------------- #
def make_polar_nestoklon_builders(params, a: float, basis,
                                  polar_displacement_z: float = 0.0,
                                  eta: float = 2.0):
    """Return (H_fn, dHdk_fn) for Nestoklon with the B cation displaced by
    ``polar_displacement_z`` (Angstrom) along [001].

    Only the Pb-I_z bonds are made asymmetric (the dominant polar mode): the +z
    bond length becomes d0-delta, the -z becomes d0+delta (d0=a/2), and their SK
    hopping blocks are scaled by the Harrison law.  At delta=0 the builder is
    bit-for-bit the centrosymmetric one, so sigma^(2) vanishes exactly.
    x,y bonds are left at d0 (their change is O(delta^2) and inversion-even).
    """
    _norm = {"dx2-y2": "dx2y2", "s*": "sstar"}
    basis = [_norm.get(b, b) for b in basis]
    n_orb = len(basis)
    N = n_orb * 4
    delta = float(polar_displacement_z)
    d0 = a / 2.0

    plus_blocks, minus_blocks = {}, {}
    for axis, direction in mn._AXIS_DIR.items():
        dminus = tuple(-x for x in direction)
        plus_blocks[axis] = mn._sk_block(basis, direction, params)
        minus_blocks[axis] = mn._sk_block(basis, dminus, params)

    # z-bond (axis 2) Harrison scaling for the displaced cation.
    d_plus = d0 - delta   # Pb moved +z toward the +z halide -> shorter bond
    d_minus = d0 + delta  # -> longer bond on the -z side
    s_plus = (d0 / d_plus) ** eta
    s_minus = (d0 / d_minus) ** eta

    onsite_c = mn._onsite(basis, params, "c")
    onsite_a = mn._onsite(basis, params, "a")
    p_idx = [i for i, b in enumerate(basis) if b in ("px", "py", "pz")]
    soc_c = soc_p_from_lambda3(params.get("Delta_c_over_3", 0.0))
    soc_a = soc_p_from_lambda3(params.get("Delta_a_over_3", 0.0))

    def slc(atom):
        return slice(atom * n_orb, (atom + 1) * n_orb)

    def _bond_phase_lengths(axis):
        """Per-axis (block_plus, phase_plus_len, block_minus, phase_minus_len)."""
        if axis == 2:
            return (s_plus * plus_blocks[2], d_plus,
                    s_minus * minus_blocks[2], d_minus)
        return (plus_blocks[axis], d0, minus_blocks[axis], d0)

    def _spinful_with_soc(H0):
        H = np.kron(np.eye(2, dtype=complex), H0)
        for atom, soc in [(0, soc_c), (1, soc_a), (2, soc_a), (3, soc_a)]:
            full_idx = [s * N + atom * n_orb + o for s in (0, 1) for o in p_idx]
            for ai, A in enumerate(full_idx):
                for bi, B in enumerate(full_idx):
                    H[A, B] += soc[ai, bi]
        return H

    def H_fn(kvec):
        k = np.asarray(kvec, float)
        H0 = np.zeros((N, N), dtype=complex)
        H0[slc(0), slc(0)] = np.diag(onsite_c).astype(complex)
        for ax in range(3):
            H0[slc(ax + 1), slc(ax + 1)] = np.diag(onsite_a).astype(complex)
        for axis, direction in mn._AXIS_DIR.items():
            kd = float(np.dot(k, direction))
            bp, lp, bm, lm = _bond_phase_lengths(axis)
            block = bp * np.exp(1j * kd * lp) + bm * np.exp(-1j * kd * lm)
            H0[slc(0), slc(axis + 1)] = block
            H0[slc(axis + 1), slc(0)] = block.conj().T
        return _spinful_with_soc(H0)

    def dHdk_fn(kvec, alpha):
        k = np.asarray(kvec, float)
        dH0 = np.zeros((N, N), dtype=complex)
        direction = mn._AXIS_DIR[alpha]
        kd = float(np.dot(k, direction))
        bp, lp, bm, lm = _bond_phase_lengths(alpha)
        dblock = bp * (1j * lp) * np.exp(1j * kd * lp) + bm * (-1j * lm) * np.exp(-1j * kd * lm)
        dH0[slc(0), slc(alpha + 1)] = dblock
        dH0[slc(alpha + 1), slc(0)] = dblock.conj().T
        return np.kron(np.eye(2, dtype=complex), dH0)

    return H_fn, dHdk_fn


# --------------------------------------------------------------------------- #
# Shift-current conductivity sigma_zzz(omega)
# --------------------------------------------------------------------------- #
def _eig(H):
    H = 0.5 * (H + H.conj().T)
    return np.linalg.eigh(H)


def shift_current_zzz_abelian_deprecated(H_fn: Callable, dHdk_fn: Callable, a: float,
                                         n_occ: int, omega_grid: np.ndarray,
                                         n_kpts: int = 8, smearing_eta: float = 0.05,
                                         dk: float = 1e-3) -> np.ndarray:
    """DEPRECATED Abelian band-diagonal shift vector -- DO NOT USE for results.

    Kept only for regression comparison. Fails the centrosymmetric vanishing at
    delta=0 because SOC makes every band Kramers-doubly-degenerate and the
    band-diagonal link Ov[c,c] is ill-defined within the degenerate subspace
    (|sigma_zzz| ~ O(10) instead of 0). Superseded by ``shift_current_zzz``
    (velocity-gauge sum-over-states). See cowork/progress/2026-05-23_1300_code_review.md.
    """
    from .optical import monkhorst_pack
    kred = monkhorst_pack(n_kpts)
    kcart = kred * (2.0 * np.pi / a)
    Nw = omega_grid.shape[0]
    sigma = np.zeros(Nw)
    ez = np.array([0.0, 0.0, 1.0])
    kz_step = dk * (2.0 * np.pi / a)

    for k in kcart:
        E, U = _eig(H_fn(k))
        dHz = dHdk_fn(k, 2)
        Mz = U.conj().T @ dHz @ U          # Mz[n,m] = <n|dH/dk_z|m>
        # neighbour k for the discrete shift vector along z.
        kp = k + ez * kz_step
        Ep, Up = _eig(H_fn(kp))
        dHzp = dHdk_fn(kp, 2)
        Mzp = Up.conj().T @ dHzp @ Up
        # link variables <u_n(k+dk)|u_n(k)> per band (diagonal overlap).
        Ov = Up.conj().T @ U               # Ov[n,n'] = <u_n(kp)|u_{n'}(k)>

        for v in range(n_occ):
            for c in range(n_occ, U.shape[1]):
                Ecv = E[c] - E[v]
                if Ecv < 1e-6:
                    continue
                m_vc = Mz[v, c]
                if abs(m_vc) < 1e-12:
                    continue
                # gauge-invariant discrete shift vector R_z:
                #   loop = M(k)^* M(k+dk) <u_c(kp)|u_c(k)> <u_v(k)|u_v(kp)>
                Lc = Ov[c, c]                       # <u_c(kp)|u_c(k)>
                Lv = np.conj(Ov[v, v])              # <u_v(k)|u_v(kp)>
                loop = np.conj(m_vc) * Mzp[v, c] * Lc * Lv
                R_z = -np.angle(loop) / kz_step
                intensity = (abs(m_vc) ** 2) / (Ecv ** 2)
                # Lorentzian-broadened delta(Ecv - hw)
                L = (smearing_eta / np.pi) / ((Ecv - omega_grid) ** 2 + smearing_eta ** 2)
                sigma += intensity * R_z * L
    sigma /= kcart.shape[0]
    return sigma


def shift_current_zzz(H_fn: Callable, dHdk_fn: Callable, a: float, n_occ: int,
                      omega_grid: np.ndarray, n_kpts: int = 8,
                      smearing_eta: float = 0.05, deg_tol: float = 1e-5) -> np.ndarray:
    """Shift-current conductivity sigma_zzz(omega) -- velocity-gauge sum-over-states.

    Recommended method (Cowork review cowork/progress/2026-05-23_1300_code_review.md,
    option B). Avoids the k-derivative gauge fixing and handles the Kramers (SOC)
    degeneracy by skipping degenerate intermediate states, so the centrosymmetric
    vanishing at delta=0 is recovered.

    sigma_zzz(w) ~ sum_{v in occ, c in unocc} Im[ r^z_cv * r^z_{vc;z} ] delta(w_cv - w)

    with the interband Berry connection (TEXTBOOK convention) and the
    Aversa-Sipe / Sipe-Shkrebtii generalized (covariant) derivative:

        r^z_nm   = i <n|dH/dk_z|m> / (E_m - E_n)           (n != m)
        Delta^z_nm = <n|dH/dk_z|n> - <m|dH/dk_z|m>          (band-velocity difference)
        r^z_{vc;z} = 2 r^z_vc Delta^z_vc / (E_v - E_c)
                   - (i/(E_v-E_c)) sum_{l != v,c} (w_lc - w_vl) r^z_vl r^z_lc
        w_lc = E_l - E_c,  w_vl = E_v - E_l

    Degenerate intermediate states (|E_l - E_c| < deg_tol or |E_v - E_l| < deg_tol)
    are skipped (removes the Kramers partner contributions, which are ill-defined).

    Refs: Aversa & Sipe, PRB 52, 14636 (1995) Eq.(39) [primary, NOT in repo];
    Sipe & Shkrebtii, PRB 61, 5337 (2000) Eq.(4.5); Fregoso 2017 (arXiv:1701.00172)
    Eq.(A6); Passos 2018 (arXiv:1712.04924) Sec. II-B; Young & Rappe 2012
    (arXiv:1202.3168) Eq.(1).

    *** VALIDATION STATUS ***
    The STRUCTURE is validated by the centrosymmetric vanishing at delta=0 (sign-
    robust) and the emergence/peak at delta>0 (tests/test_shift_current.py).  The
    ABSOLUTE sign and prefactor (-pi e^3/hbar^2) are NOT independently verified
    against the primary source (Aversa-Sipe 1995, not obtainable here); output is in
    relative units and the overall sign is convention-dependent -> deferred to F4
    (re-requested from Cowork). Absolute magnitude is additionally limited by the
    Blount-1962 TB intra-atomic incompleteness (same as g-factor / optical).
    """
    from .optical import monkhorst_pack
    kred = monkhorst_pack(n_kpts)
    kcart = kred * (2.0 * np.pi / a)
    sigma = np.zeros(omega_grid.shape[0])

    for k in kcart:
        E, U = _eig(H_fn(k))
        Vz = U.conj().T @ (dHdk_fn(k, 2)) @ U          # Vz[n,m] = <n|dH/dk_z|m>
        Nb = E.shape[0]
        # interband Berry connection r^z[n,m] = i Vz[n,m]/(E[m]-E[n]) (0 on diagonal)
        dE = E[None, :] - E[:, None]                   # dE[n,m] = E[m]-E[n]
        with np.errstate(divide="ignore", invalid="ignore"):
            rz = 1j * Vz / dE
        np.fill_diagonal(rz, 0.0)
        rz[~np.isfinite(rz)] = 0.0
        vdiag = np.real(np.diag(Vz))                   # band velocities v^z_nn

        for v in range(n_occ):
            for c in range(n_occ, Nb):
                wcv = E[c] - E[v]
                if wcv < deg_tol:
                    continue
                # generalized derivative r^z_{vc;z}
                Delta = vdiag[v] - vdiag[c]            # Delta^z_vc
                gd = 2.0 * rz[v, c] * Delta / (E[v] - E[c])
                # virtual sum over l != v,c, skipping degenerate partners
                l = np.arange(Nb)
                mask = (l != v) & (l != c)
                mask &= np.abs(E - E[c]) > deg_tol      # |w_lc| > tol
                mask &= np.abs(E[v] - E) > deg_tol      # |w_vl| > tol
                w_lc = E - E[c]
                w_vl = E[v] - E
                ssum = np.sum(((w_lc - w_vl) * rz[v, :] * rz[:, c])[mask])
                gd += -1j * ssum / (E[v] - E[c])
                integrand = np.imag(rz[c, v] * gd)
                Lor = (smearing_eta / np.pi) / ((wcv - omega_grid) ** 2 + smearing_eta ** 2)
                sigma += integrand * Lor
    sigma /= kcart.shape[0]
    return sigma
