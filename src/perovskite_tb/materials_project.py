# SPDX-License-Identifier: MIT
# Copyright (c) 2026 tk
"""Materials Project DFPT high-frequency dielectric (eps_inf) fetch (Theme I, C').

Fetches the electronic (high-frequency) dielectric constant eps_inf computed by
Materials Project via DFPT, giving a SINGLE-METHOD, consistent set across the
9 cubic CsBX3 -> the relative E_b trend is maximally defensible.  Note eps_inf is
the BARE electronic dielectric (not the exciton effective eps_eff), so absolute E_b
remains an upper-bound overestimate (see theme_I_exciton.md sec.3.2).

Security: the MP API key is loaded from data/parameters/mp_api_key.json (gitignored)
and is NEVER logged, returned, committed, or written to any output.  Only the
provenance string 'Materials Project DFPT, <mp_id>' and the public source URL are
recorded downstream.

The new MP API sits behind Cloudflare which 1010-blocks the default urllib User-Agent;
a browser User-Agent header is required.  eps_electronic is propagated to the
/materials/summary/ endpoint (scalar = trace/3 of the DFPT dielectric tensor).
"""
from __future__ import annotations

import json
import time
import urllib.request
from typing import Optional

_KEY_FILE = "data/parameters/mp_api_key.json"
_BASE = "https://api.materialsproject.org/materials/summary/"
_UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
       "Chrome/124.0 Safari/537.36")


def _load_key(path: str = _KEY_FILE) -> str:
    """Load the MP API key from the gitignored JSON. Never log/print the return."""
    with open(path) as fh:
        return json.load(fh)["api_key"]


def _query_summary(formula: str, key: str, limit: int = 40) -> list:
    url = (f"{_BASE}?formula={formula}"
           f"&_fields=material_id,symmetry,e_electronic,e_total,band_gap,energy_above_hull"
           f"&_limit={limit}")
    req = urllib.request.Request(url, headers={"X-API-KEY": key, "accept": "application/json",
                                               "User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r).get("data", [])


def fetch_eps_inf_for_formula(formula: str, prefer_spacegroup: str = "Pm-3m",
                              key: Optional[str] = None) -> dict:
    """Return DFPT eps_inf for ``formula`` from Materials Project.

    Picks the entry that HAS a computed dielectric, preferring ``prefer_spacegroup``
    (cubic Pm-3m); otherwise the lowest energy-above-hull phase with a dielectric.

    Returns dict: {formula, mp_id, spacegroup, crystal_system, eps_inf_scalar,
    eps_total_scalar, band_gap_mp, e_above_hull, phase_note, source_url, method,
    status}.  On no dielectric available: eps_inf_scalar=None, status set.
    The API key is never included in the return value.
    """
    if key is None:
        key = _load_key()
    docs = _query_summary(formula, key)
    cand = [d for d in docs if d.get("e_electronic") is not None]
    cubic = [d for d in cand if (d.get("symmetry") or {}).get("symbol") == prefer_spacegroup]
    if cubic:
        pick, note = cubic[0], f"cubic {prefer_spacegroup} (DFPT dielectric available)"
    elif cand:
        pick = sorted(cand, key=lambda d: d.get("energy_above_hull") or 9.0)[0]
        note = (f"no {prefer_spacegroup} dielectric in MP; lowest-Ehull phase with a "
                f"DFPT dielectric used (eps_inf ~phase-insensitive; mu is cubic-phase)")
    else:
        return {"formula": formula, "mp_id": None, "eps_inf_scalar": None,
                "status": "no_dielectric_in_MP",
                "phase_note": f"{len(docs)} MP phases, none with a DFPT dielectric"}
    sym = pick.get("symmetry") or {}
    mp_id = pick["material_id"]
    return {
        "formula": formula, "mp_id": mp_id, "spacegroup": sym.get("symbol"),
        "crystal_system": sym.get("crystal_system"),
        "eps_inf_scalar": round(float(pick["e_electronic"]), 3),
        "eps_total_scalar": round(float(pick["e_total"]), 3) if pick.get("e_total") else None,
        "band_gap_mp": pick.get("band_gap"), "e_above_hull": pick.get("energy_above_hull"),
        "phase_note": note, "source_url": f"https://materialsproject.org/materials/{mp_id}",
        "method": f"Materials Project DFPT, {mp_id}", "status": "found_MP_DFPT",
    }


def fetch_all(formulas, sleep_s: float = 1.0) -> dict:
    """Fetch eps_inf for several formulas (rate-limited). Returns {formula: dict}."""
    key = _load_key()
    out = {}
    for f in formulas:
        try:
            out[f] = fetch_eps_inf_for_formula(f, key=key)
        except Exception as e:  # noqa: BLE001 - record, don't fabricate
            out[f] = {"formula": f, "mp_id": None, "eps_inf_scalar": None,
                      "status": f"fetch_error:{type(e).__name__}"}
        time.sleep(sleep_s)
    return out
