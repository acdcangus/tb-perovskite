"""Complex dielectric function eps(omega) in the independent-particle approximation.

Implements Apergi 2023 (arXiv:2309.14002) Eq.(3) (imaginary part) with the
electric-dipole velocity matrix element Eq.(4), which is exactly the tight-binding
``dH/dk`` operator from ``velocity.py`` (shared with the g-factor module).  The
real part follows from a Kramers-Kronig transform.  Excitonic effects are NOT
included (independent-particle / RPA-free).

Imaginary part (velocity gauge, SI, photon energy E = hbar*omega in eV):

    eps_i^aa(E) = (pi e^2/eps0) / (E^2 N_k V)
                  * sum_k sum_{v,c} |<c k| dH/dk_a |v k>|^2 * L(E_cv - E; eta)

with the bands v occupied (v < n_occ), c empty (c >= n_occ), E_cv = E_c - E_v,
L the normalized Lorentzian (integral 1), V the cell volume (A^3) and the matrix
element in eV.A.  Constant: pi e^2/eps0 = pi * (4 pi * 14.39964) eV.A = 568.41 eV.A.

Spin is explicit in the spin-major basis (bands are not spin-degenerate-doubled),
so no extra spin factor of 2 is applied.

Verification (tests/test_optical.py): absorption edge == band gap; cubic isotropy
eps_xx=eps_yy=eps_zz; Kramers-Kronig self-consistency; f-sum rule (approximate).
"""

from __future__ import annotations

from typing import Callable

import numpy as np

from ._constants import COULOMB_EV_ANG, HBAR2_OVER_M0  # eV.A / eV.A^2 (single source)

# pi * e^2 / eps0 in eV.Angstrom.  e^2/(4 pi eps0) = COULOMB_EV_ANG = 14.39964 eV.A.
PI_E2_OVER_EPS0 = np.pi * (4.0 * np.pi * COULOMB_EV_ANG)  # = 568.41 eV.A


def monkhorst_pack(n: int) -> np.ndarray:
    """Gamma-centred Monkhorst-Pack grid of reduced coords in [0,1)^3, shape (n^3,3)."""
    pts = (np.arange(n) + 0.5) / n - 0.5  # centred, avoids Gamma exactly
    gx, gy, gz = np.meshgrid(pts, pts, pts, indexing="ij")
    return np.stack([gx.ravel(), gy.ravel(), gz.ravel()], axis=1)


def _lorentzian(x: np.ndarray, eta: float) -> np.ndarray:
    return (eta / np.pi) / (x * x + eta * eta)


def compute_dielectric(hamiltonian_fn: Callable[[np.ndarray], np.ndarray],
                       dHdk_fn: Callable[[np.ndarray, int], np.ndarray],
                       a_lattice: float,
                       n_occ: int,
                       omega_grid: np.ndarray,
                       n_kpts: int = 8,
                       smearing_eta: float = 0.05,
                       volume: float | None = None) -> dict:
    """Compute eps(omega) over a Monkhorst-Pack grid.

    Parameters
    ----------
    hamiltonian_fn : H(kvec_cart) -> (N,N)
    dHdk_fn : (kvec_cart, alpha) -> (N,N)   (e.g. velocity.dH_dk_kashikar13 wrapped)
    a_lattice : cubic lattice constant (A); cartesian k = reduced * 2pi/a.
    n_occ : number of occupied (valence) spin-bands.
    omega_grid : photon energies hbar*omega (eV), shape (Nw,).
    n_kpts : Monkhorst-Pack subdivisions per axis (n^3 points).
    smearing_eta : Lorentzian broadening (eV).
    volume : cell volume (A^3); default a_lattice**3.

    Returns dict: omega, eps_imag (avg of xx,yy,zz), eps_imag_tensor (3,Nw),
    eps_real, alpha (1/cm), n_refractive.
    """
    V = float(a_lattice ** 3 if volume is None else volume)
    kred = monkhorst_pack(n_kpts)
    kcart = kred * (2.0 * np.pi / a_lattice)
    Nk = kcart.shape[0]
    Nw = omega_grid.shape[0]

    eps_i = np.zeros((3, Nw))
    for k in kcart:
        H = hamiltonian_fn(k)
        H = 0.5 * (H + H.conj().T)
        E, U = np.linalg.eigh(H)
        occ = U[:, :n_occ]
        emp = U[:, n_occ:]
        Eo = E[:n_occ]
        Ec = E[n_occ:]
        # transition energies E_cv (Nc, No)
        Ediff = Ec[:, None] - Eo[None, :]
        # 1/E_cv^2 belongs *inside* the sum (evaluated at the transition energy,
        # where the delta function pins hbar*omega = E_cv). Placing 1/omega^2
        # outside would create a spurious sub-gap 1/omega^2 tail.
        inv_E2 = (1.0 / (Ediff * Ediff)).ravel()      # (T,)
        trans = Ediff.ravel()                          # (T,) transition energies
        # Lorentzian over the full omega grid, shared by all 3 directions.
        diff = trans[:, None] - omega_grid[None, :]    # (T, Nw)
        L = (smearing_eta / np.pi) / (diff * diff + smearing_eta * smearing_eta)
        for a in range(3):
            dH = dHdk_fn(k, a)
            M = emp.conj().T @ dH @ occ                # M[c,v] = <c|dH|v>
            w = (np.abs(M) ** 2).ravel() * inv_E2      # (T,)
            eps_i[a] += w @ L                          # (Nw,)
    eps_i *= PI_E2_OVER_EPS0 / (Nk * V)

    eps_i_avg = eps_i.mean(axis=0)
    eps_r_avg = _kramers_kronig(omega_grid, eps_i_avg)

    # absorption coefficient alpha (1/cm) and refractive index from averaged eps.
    eps_c = eps_r_avg + 1j * eps_i_avg
    n_ref = np.sqrt((np.abs(eps_c) + eps_r_avg) / 2.0)
    kappa = np.sqrt((np.abs(eps_c) - eps_r_avg) / 2.0)
    # alpha = 2 omega kappa / c ; omega = E/hbar. In 1/cm:
    # E[eV]/(hbar c) with hbar c = 1973.27 eV.A -> 1/A, x1e8 -> 1/cm
    alpha = 2.0 * (omega_grid / 1973.269804) * kappa * 1e8

    return {
        "omega": omega_grid,
        "eps_imag": eps_i_avg,
        "eps_imag_tensor": eps_i,
        "eps_real": eps_r_avg,
        "alpha": alpha,
        "n_refractive": n_ref,
    }


def _kramers_kronig(omega: np.ndarray, eps_i: np.ndarray) -> np.ndarray:
    """Real part via KK: eps_r(w) = 1 + (2/pi) P int w' eps_i(w')/(w'^2 - w^2) dw'."""
    Nw = omega.shape[0]
    dw = np.gradient(omega)
    eps_r = np.ones(Nw)
    for i, w in enumerate(omega):
        denom = omega ** 2 - w ** 2
        mask = np.abs(denom) > 1e-12
        integrand = np.zeros_like(omega)
        integrand[mask] = (omega[mask] * eps_i[mask] * dw[mask]) / denom[mask]
        eps_r[i] += (2.0 / np.pi) * np.sum(integrand)
    return eps_r


def f_sum_rule_check(omega: np.ndarray, eps_i: np.ndarray, n_occ: int,
                     volume: float) -> dict:
    """Check the f-sum rule int_0^inf E eps_i(E) dE = (pi/2) (hbar w_p)^2.

    (hbar w_p)^2 = n_e (e^2/eps0)(hbar^2/m0), n_e = n_occ_electrons / V.
    Returns the measured integral, the expected value, and their ratio.
    """
    lhs = np.trapezoid(omega * eps_i, omega)
    n_e = n_occ / volume
    hbar_wp2 = n_e * (4.0 * np.pi * COULOMB_EV_ANG) * HBAR2_OVER_M0
    rhs = 0.5 * np.pi * hbar_wp2
    return {"integral": float(lhs), "expected": float(rhs),
            "ratio": float(lhs / rhs) if rhs else float("nan")}
