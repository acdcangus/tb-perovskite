# Theme I (Y1-c-3, option C'): Wannier-Mott E_b with Materials Project DFPT eps_inf

E_b = (mu/m0)/eps_inf^2 * Ry. mu = TB cubic R-point curvature; eps_inf = MP DFPT (single method, 8/9 materials, phases noted). BARE eps_inf -> absolute E_b is an upper bound; relative trend defensible.

Reproduce: PYTHONPATH=src python scripts/fetch_mp_eps_inf.py  # needs data/parameters/mp_api_key.json
PYTHONPATH=src python scripts/scan_theme_I_binding_energy.py production --profile MP_DFPT


## Correction note (2026-05-24, review protocol R2-1)
The MANIFEST.json `notes` field says "CsPbI3 here ~41 meV vs experiment ~15-20 meV".
The experimental figure is superseded: per Cho et al. 2019 (arXiv:1908.09436) the cited
CsPbI3-type exciton binding range is **7.4-50 meV** (Cho's own value: eps=6.1, mu=0.10 ->
37 meV). The MANIFEST is kept as the immutable run snapshot; this note is the authoritative
correction (no fabricated experimental value).
