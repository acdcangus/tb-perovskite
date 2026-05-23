"""TB-derived Kane momentum parameter P from the analytic velocity operator.

Motivation (Cowork directive update 2026-05-23): make Theme A fully TB-based by
extracting, in addition to the conduction-band SO splitting Delta (Kashikar Eq.9,
Delta = 3*lambda), the Kane interband momentum parameter P from the TB velocity
operator -- staying within the 2/3-band Kirstein-Nestoklon k.p framework.

Definition (Nestoklon 2023 SI Eq.(S2)): P = i<Z|p_z|S> = i<X|p_x|S> = i<Y|p_y|S>,
the interband momentum matrix element between the S-like valence-band edge and
the Z-like conduction-band component.  In the velocity gauge P (= hbar*p/m0, the
quantity Kirstein 2021 lists as 6.8 eV.A) equals the velocity-operator matrix
element <c|dH/dk_z|v> (eV.A), since hbar*p/m0 = hbar*v = dH/dk.

The cubic CB edge is SOC-mixed (Nestoklon Eq.S1b): u_cb = sin(theta) Z|up> +
cos(theta)(X+iY)/sqrt2 |down>, with sin^2(theta) the cation-p_z weight.  The raw
doublet matrix element is therefore sin(theta)*P; we divide by sin(theta)
(measured from the CBM eigenvector) to recover the bare Kane P.

We report BOTH the raw element and the sin(theta)-corrected bare P, with full
transparency: with band-structure-fit Hamiltonians (Kashikar mBJ; Nestoklon
arXiv experiment_corrected) P typically *underestimates* the g-factor-effective
6.8 eV.A, because those parameters were not tuned to g-factors (Nestoklon's
g-tuned Table S1 set, with larger pp_sigma -> larger velocity -> larger P, is
paywalled).  Values are reported, not forced.
"""

from __future__ import annotations

import numpy as np


def extract_kane_parameter(H: np.ndarray, dHdk_z: np.ndarray, n_filled: int,
                           pz_orbital_index: int, n_orb_spinless: int) -> dict:
    """Extract the TB Kane parameter P at the band edge (eV.A).

    Parameters
    ----------
    H : (2N,2N) Hermitian Bloch Hamiltonian at the band edge (R point), spin-major.
    dHdk_z : (2N,2N) analytic dH/dk_z at the same k (eV.A).
    n_filled : number of occupied spin-bands (CBM = n_filled, VBM = n_filled-1).
    pz_orbital_index : index of the cation p_z orbital in the *spinless* basis.
    n_orb_spinless : number of spinless orbitals (so spin-down p_z is at
        pz_orbital_index + n_orb_spinless in the spin-major full basis).

    Returns dict: P_raw (max doublet |<c|dHz|v>|), sin2theta (CBM cation-pz weight),
    P_bare (= P_raw / sin(theta)), and per-component check.
    """
    H = 0.5 * (H + H.conj().T)
    E, U = np.linalg.eigh(H)
    vbm = [n_filled - 2, n_filled - 1]
    cbm = [n_filled, n_filled + 1]

    # Raw interband velocity coupling over the doublets (z-direction).
    elems = []
    for c in cbm:
        for v in vbm:
            elems.append(abs(U[:, c].conj() @ (dHdk_z @ U[:, v])))
    P_raw = float(max(elems))

    # CBM cation-p_z weight = sin^2(theta).
    pz_up = pz_orbital_index
    pz_dn = pz_orbital_index + n_orb_spinless
    sin2 = 0.0
    for c in cbm:
        sin2 += abs(U[pz_up, c]) ** 2 + abs(U[pz_dn, c]) ** 2
    sin2 /= len(cbm)  # average over the doublet
    sintheta = np.sqrt(sin2) if sin2 > 1e-9 else float("nan")
    P_bare = P_raw / sintheta if sintheta == sintheta and sintheta > 0 else float("nan")

    return {"P_raw": P_raw, "sin2theta": float(sin2), "P_bare": float(P_bare),
            "doublet_elements": [float(x) for x in elems]}


def kane_parameter_anisotropy(H: np.ndarray, dHdk_xyz, n_filled: int) -> dict:
    """Return the max raw doublet |<c|dH/dk_a|v>| for a=x,y,z (cubic isotropy check)."""
    H = 0.5 * (H + H.conj().T)
    E, U = np.linalg.eigh(H)
    vbm = [n_filled - 2, n_filled - 1]
    cbm = [n_filled, n_filled + 1]
    out = {}
    for a, lab in zip(range(3), ("Px", "Py", "Pz")):
        elems = [abs(U[:, c].conj() @ (dHdk_xyz[a] @ U[:, v])) for c in cbm for v in vbm]
        out[lab] = float(max(elems))
    return out
