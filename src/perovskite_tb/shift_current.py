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
    """Return (H_fn, dHdk_fn, d2Hdk_fn) for Nestoklon with the B cation displaced
    by ``polar_displacement_z`` (Angstrom) along [001].

    Only the Pb-I_z bonds are made asymmetric (the dominant polar mode): the +z
    bond length becomes d0-delta, the -z becomes d0+delta (d0=a/2), and their SK
    hopping blocks are scaled by the Harrison law.  At delta=0 the builder is
    bit-for-bit the centrosymmetric one, so sigma^(2) vanishes exactly.
    x,y bonds are left at d0 (their change is O(delta^2) and inversion-even).

    ``d2Hdk_fn(kvec, alpha)`` returns the second k-derivative d^2H/dk_alpha^2,
    REQUIRED for the tight-binding shift current: the generalized derivative for a
    TB Hamiltonian carries an off-diagonal w^{ab}_nm = <n|d^2H/dk_a dk_b|m> term
    that the continuum (H=p^2/2m+V) sum-over-states form omits (Fregoso 2017,
    arXiv:1701.00172, Eq.(C2) and remark after it).
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

    def d2Hdk_fn(kvec, alpha):
        """d^2 H / dk_alpha^2 (second k-derivative, same axis twice)."""
        k = np.asarray(kvec, float)
        d2H0 = np.zeros((N, N), dtype=complex)
        direction = mn._AXIS_DIR[alpha]
        kd = float(np.dot(k, direction))
        bp, lp, bm, lm = _bond_phase_lengths(alpha)
        # d^2/dk^2 of  bp e^{i kd lp} + bm e^{-i kd lm}:
        #   bp (i lp)^2 e^{...} + bm (-i lm)^2 e^{...} = -bp lp^2 e^{...} - bm lm^2 e^{...}
        d2block = (bp * (1j * lp) ** 2 * np.exp(1j * kd * lp)
                   + bm * (-1j * lm) ** 2 * np.exp(-1j * kd * lm))
        d2H0[slc(0), slc(alpha + 1)] = d2block
        d2H0[slc(alpha + 1), slc(0)] = d2block.conj().T
        return np.kron(np.eye(2, dtype=complex), d2H0)

    return H_fn, dHdk_fn, d2Hdk_fn


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


def shift_current_integrand_aaa(E: np.ndarray, Va: np.ndarray, Waa: np.ndarray,
                                n_occ: int, deg_tol: float = 1e-5):
    """Per-k shift-current integrand g_{vc} = Im[ r^a_cv r^a_{vc;a} ] and gaps w_cv.

    Inputs are in the BAND (eigenstate) basis at one k-point:
        E    : (Nb,)    band energies
        Va   : (Nb,Nb)  velocity matrix  v^a_nm = <n|dH/dk_a|m>
        Waa  : (Nb,Nb)  second derivative w^aa_nm = <n|d^2H/dk_a^2|m>
    Returns (g, wcv) each shaped (n_occ, n_unocc).

    Generalized (covariant) derivative -- Fregoso 2017 (arXiv:1701.00172) Eq.(C2),
    the velocity form *valid for tight-binding* (keeps the off-diagonal second-
    derivative term w^aa, unlike the continuum Sipe-Shkrebtii form):

        r^a_{vc;a} = -(1/(i w_vc)) [ 2 v^a_vc Delta^a_vc / w_vc - w^aa_vc
                                     + sum_{p!=v,c} v^a_vp v^a_pc (1/w_pc - 1/w_vp) ]
        w_vc = E_v - E_c,  w_pc = E_p - E_c,  w_vp = E_v - E_p
        Delta^a_vc = v^a_vv - v^a_cc          r^a_cv = v^a_cv / (i w_cv)

    The virtual sum is vectorised with R[i,j] = v^a_ij/(E_i-E_j) (diagonal and
    degenerate pairs zeroed, |E_i-E_j| < deg_tol): then
        sum_{p!=v,c} v_vp v_pc (1/w_pc - 1/w_vp)
            = (Va @ R)_vc - (R @ Va)_vc - Delta^a_vc v^a_vc / w_vc,
    so the combined bracket is  v^a_vc Delta/w_vc - w^aa_vc + (Va@R - R@Va)_vc.
    Validated to machine precision vs the explicit (v,c,p) loop and, for the
    2-band Rice-Mele model, against Fregoso's closed form Eq.(D15)
    Im[r^z_cv r^z_vc;z] = a^3 t delta Delta /(32 E^3) (see tests).
    """
    Nb = E.shape[0]
    dEij = E[:, None] - E[None, :]                     # E_i - E_j
    mask = np.abs(dEij) > deg_tol
    R = np.zeros((Nb, Nb), dtype=complex)
    R[mask] = Va[mask] / dEij[mask]                    # R[i,j] = v_ij/(E_i-E_j)
    T1 = Va @ R
    T2 = R @ Va
    vdiag = np.real(np.diag(Va))

    v = slice(0, n_occ)
    c = slice(n_occ, Nb)
    # sign bookkeeping: wvc = E_v - E_c < 0 (occupied below unoccupied);
    #                   wcv = E_c - E_v > 0 (the positive transition energy).
    wvc = E[v, None] - E[None, c]                      # E_v - E_c  (<0)
    wcv = -wvc                                         # E_c - E_v  (>0)
    Delta = vdiag[v, None] - vdiag[None, c]            # Delta^a_vc
    bracket = Va[v, c] * Delta / wvc - Waa[v, c] + (T1[v, c] - T2[v, c])
    r_vc_a = -bracket / (1j * wvc)
    r_cv = Va[c, v].T / (1j * wcv)                     # r^a_cv, shape (n_occ,n_unocc)
    g = np.imag(r_cv * r_vc_a)
    return g, wcv


def _shift_integrand_aaa_batched(E: np.ndarray, Va: np.ndarray, Waa: np.ndarray,
                                 n_occ: int, deg_tol: float):
    """Batched (over a leading k-axis) version of ``shift_current_integrand_aaa``.

    E:(K,Nb), Va,Waa:(K,Nb,Nb).  Returns g,wcv each (K,n_occ,n_unocc).  Identical
    math to the per-k function (regression-tested to ~1e-12); see its docstring.
    """
    K, Nb = E.shape
    dEij = E[:, :, None] - E[:, None, :]               # (K,Nb,Nb) E_i - E_j
    mask = np.abs(dEij) > deg_tol
    R = np.zeros_like(Va)
    np.divide(Va, dEij, out=R, where=mask)             # R[i,j]=v_ij/(E_i-E_j), 0 if degenerate
    T1 = Va @ R
    T2 = R @ Va
    vdiag = np.real(np.diagonal(Va, axis1=1, axis2=2))  # (K,Nb)
    v = slice(0, n_occ)
    c = slice(n_occ, Nb)
    wvc = E[:, v, None] - E[:, None, c]                # E_v - E_c (<0)
    wcv = -wvc                                         # E_c - E_v (>0)
    Delta = vdiag[:, v, None] - vdiag[:, None, c]
    bracket = Va[:, v, c] * Delta / wvc - Waa[:, v, c] + (T1[:, v, c] - T2[:, v, c])
    r_vc_a = -bracket / (1j * wvc)
    r_cv = np.transpose(Va[:, c, v], (0, 2, 1)) / (1j * wcv)  # r^a_cv -> (K,n_occ,n_unocc)
    g = np.imag(r_cv * r_vc_a)
    return g, wcv


def shift_current_zzz(H_fn: Callable, dHdk_fn: Callable, a: float, n_occ: int,
                      omega_grid: np.ndarray, n_kpts: int = 8,
                      smearing_eta: float = 0.05, deg_tol: float = 1e-5,
                      direction: int = 2,
                      d2Hdk_fn: Callable | None = None,
                      allow_continuum_form: bool = False,
                      chunk_size: int = 512) -> np.ndarray:
    """Diagonal shift-current conductivity sigma_aaa(omega) -- velocity-gauge, TB form.

    ``direction`` selects the Cartesian polarisation/current axis a (0=x,1=y,2=z;
    default z).  ``d2Hdk_fn(k, alpha)`` must return d^2H/dk_alpha^2 (REQUIRED for the
    tight-binding generalized derivative; see ``shift_current_integrand_aaa`` and
    Fregoso 2017 Eq.(C2)).  Omitting it drops the second-derivative term (w=0), which
    is WRONG for tight-binding -- so this raises ValueError unless the caller opts in
    with ``allow_continuum_form=True`` (kept only for the continuum-regression check).

        sigma_aaa(w) = (1/N_k) sum_k sum_{v in occ, c in unocc}
                          Im[ r^a_cv r^a_{vc;a} ] * Lorentzian(w_cv - w)

    The Kramers (SOC) degeneracy is handled by zeroing degenerate-pair Berry
    connections (deg_tol), so the centrosymmetric vanishing at delta=0 holds to
    machine precision.

    Refs: Fregoso 2017 (arXiv:1701.00172) Eq.(C2)/(D12)/(D15) [in-repo, primary for
    the TB form]; Sipe & Shkrebtii, PRB 61, 5337 (2000) Eq.(4.5) [continuum form,
    missing off-diagonal w]; Young & Rappe 2012 (arXiv:1202.3168) Eq.(1).

    *** VALIDATION STATUS (F4-3) ***
    The integrand Im[r^z_cv r^z_vc;z] is validated to machine precision against
    Fregoso's closed-form Rice-Mele result Eq.(D15) (sign AND magnitude), and the
    full sigma_zzz(w) reproduces Fregoso Eq.(D16) (negative for t,delta,Delta>0).
    The centrosymmetric vanishing at delta=0 holds to ~1e-15.  Output is in the
    natural units of Fregoso Eq.(C2)/(D12) up to the global prefactor (the e^3,
    hbar, pi factors of Eq.(D12)); ABSOLUTE calibration to uA/V^2 is deferred to F5.
    Absolute magnitude is additionally limited by the Blount-1962 TB intra-atomic
    incompleteness (same as g-factor / optical); *symmetry, sign, spectral shape*
    are robust.
    """
    if d2Hdk_fn is None and not allow_continuum_form:
        raise ValueError(
            "d2Hdk_fn (d^2H/dk^2) is required for the tight-binding shift current "
            "(Fregoso 2017 Eq.(C2) off-diagonal w-term). Pass it, or set "
            "allow_continuum_form=True only for the documented continuum regression.")
    from .optical import monkhorst_pack
    kred = monkhorst_pack(n_kpts)
    kcart = kred * (2.0 * np.pi / a)
    sigma = np.zeros(omega_grid.shape[0])
    inv_pi_eta = smearing_eta / np.pi

    # Process k-points in batches: batched eigh + batched band-basis transform +
    # batched integrand (BLAS-bound; ~3x faster than the per-k loop). chunk_size
    # bounds memory (a chunk holds a few (chunk, Nb, Nb) complex arrays).
    for k0 in range(0, kcart.shape[0], chunk_size):
        kb = kcart[k0:k0 + chunk_size]
        Hs = np.stack([H_fn(k) for k in kb])           # (nb_k, Nb, Nb)
        Hs = 0.5 * (Hs + np.conj(np.transpose(Hs, (0, 2, 1))))
        E, U = np.linalg.eigh(Hs)                      # (nb_k,Nb),(nb_k,Nb,Nb)
        Uh = np.conj(np.transpose(U, (0, 2, 1)))
        dHs = np.stack([dHdk_fn(k, direction) for k in kb])
        Va = Uh @ dHs @ U
        if d2Hdk_fn is not None:
            d2Hs = np.stack([d2Hdk_fn(k, direction) for k in kb])
            Waa = Uh @ d2Hs @ U
        else:
            Waa = np.zeros_like(Va)                    # continuum form (WRONG for TB)
        g, wcv = _shift_integrand_aaa_batched(E, Va, Waa, n_occ, deg_tol)
        valid = wcv > deg_tol                          # (nb_k, n_occ, n_unocc)
        wflat = wcv[valid]
        gflat = g[valid]
        diff = wflat[:, None] - omega_grid[None, :]
        Lor = inv_pi_eta / (diff * diff + smearing_eta * smearing_eta)
        sigma += gflat @ Lor
    sigma /= kcart.shape[0]
    return sigma


# --------------------------------------------------------------------------- #
# Rice-Mele 1D two-band model -- analytic validation of the shift current
# (Fregoso 2017, arXiv:1701.00172, Appendix D)
# --------------------------------------------------------------------------- #
_SX = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
_SY = np.array([[0.0, -1j], [1j, 0.0]], dtype=complex)
_SZ = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)


def rice_mele_hamiltonian(k: float, t: float, delta: float, Delta: float,
                          a: float = 1.0) -> np.ndarray:
    """Rice-Mele Bloch Hamiltonian, Fregoso 2017 Eq.(D2):
    H(k) = t cos(ka/2) sigma_x - delta sin(ka/2) sigma_y + Delta sigma_z.

    t = mean hopping, delta = dimerization, Delta = staggered (ionic) potential.
    Inversion symmetry is broken iff delta != 0 and Delta != 0.
    """
    ka2 = k * a / 2.0
    return t * np.cos(ka2) * _SX - delta * np.sin(ka2) * _SY + Delta * _SZ


def rice_mele_dHdk(k: float, t: float, delta: float, Delta: float,
                   a: float = 1.0) -> np.ndarray:
    """dH_RM/dk (Delta sigma_z is k-independent)."""
    ka2 = k * a / 2.0
    return (-t * (a / 2.0) * np.sin(ka2) * _SX
            - delta * (a / 2.0) * np.cos(ka2) * _SY)


def rice_mele_d2Hdk(k: float, t: float, delta: float, Delta: float,
                    a: float = 1.0) -> np.ndarray:
    """d^2H_RM/dk^2."""
    ka2 = k * a / 2.0
    return (-t * (a / 2.0) ** 2 * np.cos(ka2) * _SX
            + delta * (a / 2.0) ** 2 * np.sin(ka2) * _SY)


def rice_mele_energy(k: float, t: float, delta: float, Delta: float,
                     a: float = 1.0) -> float:
    """Conduction-band energy +E(k), Fregoso Eq.(D2):
    E = sqrt(t^2 cos^2(ka/2) + delta^2 sin^2(ka/2) + Delta^2)."""
    ka2 = k * a / 2.0
    return np.sqrt(t ** 2 * np.cos(ka2) ** 2 + delta ** 2 * np.sin(ka2) ** 2
                   + Delta ** 2)


def rice_mele_integrand_analytic(k: float, t: float, delta: float, Delta: float,
                                 a: float = 1.0) -> float:
    """Fregoso Eq.(D15): Im[r^z_cv r^z_vc;z] = a^3 t delta Delta / (32 E^3).

    NOTE this is Fregoso's sign convention for Im[r r;]; our
    ``shift_current_integrand_aaa`` uses the textbook r^a_cv = v_cv/(i w_cv)
    convention and returns the NEGATIVE of this (the shift-current-relevant
    combination |r|^2 R = -Im[r r;], so the physical sigma sign agrees -- see
    Fregoso Eq.(D14)/(D16))."""
    E = rice_mele_energy(k, t, delta, Delta, a)
    return a ** 3 * t * delta * Delta / (32.0 * E ** 3)


def shift_current_1d_two_band(t: float, delta: float, Delta: float, a: float,
                              omega_grid: np.ndarray, n_kpts: int = 4000,
                              smearing_eta: float = 0.02,
                              deg_tol: float = 1e-9) -> np.ndarray:
    """sigma_zzz(omega) for the 1D Rice-Mele model via the same generalized-
    derivative integrand as the 3D code (``shift_current_integrand_aaa``).

    Used to validate sign/shape against Fregoso Eq.(D16):
        sigma_zzz = -(e^3 a^3 t delta Delta)/(8 hbar^4 omega^3) sum_i 1/|dE/dk(k_i)|
    (negative for t,delta,Delta>0).  Returned in the natural units of the integrand
    (no e^3/hbar^4 prefactor), so compare SIGN and SHAPE, not absolute magnitude.
    """
    kgrid = (np.arange(n_kpts) + 0.5) / n_kpts * (2.0 * np.pi / a) - np.pi / a
    sigma = np.zeros(omega_grid.shape[0])
    inv_pi_eta = smearing_eta / np.pi
    for k in kgrid:
        E, U = _eig(rice_mele_hamiltonian(k, t, delta, Delta, a))
        Va = U.conj().T @ rice_mele_dHdk(k, t, delta, Delta, a) @ U
        Waa = U.conj().T @ rice_mele_d2Hdk(k, t, delta, Delta, a) @ U
        g, wcv = shift_current_integrand_aaa(E, Va, Waa, n_occ=1, deg_tol=deg_tol)
        valid = wcv > deg_tol
        wflat = wcv[valid]
        gflat = g[valid]
        diff = wflat[:, None] - omega_grid[None, :]
        Lor = inv_pi_eta / (diff * diff + smearing_eta * smearing_eta)
        sigma += gflat @ Lor
    sigma /= kgrid.shape[0]
    return sigma
