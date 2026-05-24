# Theme I (Y1-c-3, option C'): Wannier-Mott E_b with Materials Project DFPT eps_inf

E_b = (mu/m0)/eps_inf^2 * Ry. mu = TB cubic R-point curvature; eps_inf = MP DFPT (single method, 8/9 materials, phases noted). BARE eps_inf -> absolute E_b is an upper bound; relative trend defensible.

Reproduce: PYTHONPATH=src python scripts/fetch_mp_eps_inf.py  # needs data/parameters/mp_api_key.json
PYTHONPATH=src python scripts/scan_theme_I_binding_energy.py production --profile MP_DFPT

