#!/usr/bin/env python3
"""Build a Production-mode result bundle per cowork/PRODUCTION_RULES.md.

Creates results/production/<theme>/<date>_<commit>/ with the mandated structure
(MANIFEST.json, inputs/, outputs/{raw,figures}, convergence/, logs/, README.md),
copying existing result files, recording git info / env / checksums / software
versions. Reusable across themes (Theme A, Phase 1.5 optical, Theme F, ...).

Usage: import build_bundle(spec) or run __main__ to (re)build Theme A & Phase 1.5.
The calculations are NOT re-run -- existing outputs are copied and indexed
(retroactive Production-ization, cowork/PRODUCTION_RULES.md sec.9).
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import platform
import shutil
import subprocess


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout.strip()


def _software():
    out = {"python": platform.python_version()}
    for m in ("numpy", "scipy", "matplotlib"):
        try:
            out[m] = __import__(m).__version__
        except Exception:
            out[m] = "not installed"
    return out


def build_bundle(spec: dict) -> str:
    """spec keys: theme, subtask, physics_method, mode(default Production),
    outputs(list of (src, dest_rel_under_outputs)), inputs(list of (src, dest_rel
    under inputs)), convergence(dict), key_numbers(dict), references(list),
    notes(str), readme(str)."""
    commit = _git("rev-parse", "--short", "HEAD") or "unknown"
    full_commit = _git("rev-parse", "HEAD") or "unknown"
    # "dirty" = uncommitted work OTHER than the production bundles being created
    # (so retroactive bundling of committed results reports a clean working tree).
    porcelain = [ln for ln in _git("status", "--porcelain").splitlines()
                 if "results/production/" not in ln]
    dirty = bool(porcelain)
    date = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    root = os.path.join("results", "production", spec["theme"], f"{date}_{commit}")
    for sub in ("inputs", "outputs/raw", "outputs/figures", "convergence", "logs"):
        os.makedirs(os.path.join(root, sub), exist_ok=True)

    # copy outputs
    out_index = {"raw": [], "figures": []}
    for src, dest_rel in spec.get("outputs", []):
        dest = os.path.join(root, "outputs", dest_rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(src, dest)
        kind = "figures" if dest_rel.startswith("figures") else "raw"
        out_index[kind].append(os.path.relpath(dest, root))

    # copy inputs (parameter/config files)
    for src, dest_rel in spec.get("inputs", []):
        shutil.copy2(src, os.path.join(root, "inputs", dest_rel))

    # generated input metadata
    with open(os.path.join(root, "inputs", "cli.txt"), "w") as fh:
        fh.write(spec.get("cli", "# see README.md / scripts referenced in MANIFEST\n"))
    with open(os.path.join(root, "inputs", "git_info.txt"), "w") as fh:
        fh.write(f"commit: {full_commit}\nbranch: {_git('branch', '--show-current')}\n"
                 f"dirty: {dirty}\n\n{_git('log', '-1', '--pretty=fuller')}\n")
    freeze = subprocess.run(["python3", "-m", "pip", "freeze"], capture_output=True, text=True).stdout
    with open(os.path.join(root, "inputs", "requirements.txt"), "w") as fh:
        fh.write(freeze)

    # checksums over everything copied
    checks = {}
    for dirpath, _d, files in os.walk(os.path.join(root, "outputs")):
        for f in files:
            p = os.path.join(dirpath, f)
            checks[os.path.relpath(p, root)] = _sha256(p)
    total = sum(os.path.getsize(os.path.join(dp, f))
                for dp, _d, fs in os.walk(root) for f in fs)

    manifest = {
        "manifest_version": "1.0",
        "theme": spec["theme"],
        "subtask": spec.get("subtask", ""),
        "date_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "git_commit": full_commit,
        "git_branch": _git("branch", "--show-current"),
        "git_dirty": dirty,
        "executor": "Claude Code (Opus 4.7 via CLI)",
        "mode": spec.get("mode", "Production"),
        "retroactive": spec.get("retroactive", True),
        "physics_method": spec.get("physics_method", ""),
        "convergence": spec.get("convergence", {}),
        "inputs": {"cli": "inputs/cli.txt", "git_info": "inputs/git_info.txt",
                   "requirements": "inputs/requirements.txt"},
        "outputs": out_index,
        "key_numbers": spec.get("key_numbers", {}),
        "checksums_sha256": checks,
        "data_size_total_bytes": total,
        "software": _software(),
        "machine": {"platform": platform.platform()},
        "notes": spec.get("notes", ""),
        "references": spec.get("references", []),
    }
    with open(os.path.join(root, "MANIFEST.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)
    with open(os.path.join(root, "README.md"), "w") as fh:
        fh.write(spec.get("readme", "") + "\n")
    print(f"wrote {root}/  ({len(checks)} output files, {total} bytes, dirty={dirty})")
    return root


# --------------------------------------------------------------------------- #
THEME_A = {
    "theme": "theme_A_g_factor",
    "subtask": "A4 9-material k.p g-factor scan + A6 TB-derived Kane P + A7",
    "physics_method": "k.p universal relation (Kirstein 2021 Eq.5,6) with literature Eg, "
                      "Delta from Nestoklon Table S2 (Pb) / Kashikar Eq.9 3*lambda (Sn,Ge); "
                      "P_universal=6.8 eV.A; TB-derived P from velocity operator (A6).",
    "convergence": {"k_grid": "Not applicable (R-point band-edge evaluation)",
                    "eta_eV": "Not applicable"},
    "outputs": [
        ("results/g_factors/g_factor_9material.csv", "raw/g_factor_9material.csv"),
        ("results/g_factors/kane_parameters.csv", "raw/kane_parameters.csv"),
        ("results/g_factors/kirstein_universal_plot.png", "figures/kirstein_universal_plot.png"),
        ("results/g_factors/material_grid.png", "figures/material_grid.png"),
        ("results/g_factors/ge_universality.png", "figures/ge_universality.png"),
        ("results/g_factors/gh_delta_dependence.png", "figures/gh_delta_dependence.png"),
    ],
    "inputs": [
        ("data/parameters/experimental_band_data.json", "experimental_band_data.json"),
        ("data/parameters/kashikar2021_cubic_13orb.json", "kashikar2021_cubic_13orb.json"),
        ("data/parameters/nestoklon2021_CsPbI3.json", "nestoklon2021_CsPbI3.json"),
    ],
    "cli": ("PYTHONPATH=src python scripts/scan_g_factors.py\n"
            "PYTHONPATH=src python scripts/scan_kane_parameters.py\n"
            "PYTHONPATH=src python scripts/plot_ge_universality.py\n"
            "PYTHONPATH=src python scripts/plot_gh_delta_dependence.py\n"),
    "key_numbers": {
        "CsPbI3_g_e": 3.01, "CsPbBr3_g_e": 1.76, "CsPbCl3_g_e": 0.99,
        "CsSnI3_g_e": 4.56, "CsGeI3_g_e": 3.39,
        "CsGeI3_gh_deviation": 1.86, "CsSnI3_gh_deviation": 1.81,
        "CsPbI3_TB_P_nestoklon": 5.44, "P_universal": 6.8,
    },
    "references": ["Kirstein 2021 arXiv:2112.15384 Eq.5,6",
                   "Nestoklon 2023 arXiv:2305.10586 Table S2",
                   "Kashikar 2021 arXiv:2101.08562 Eq.9"],
    "notes": "Retroactive Production-ization. g_e on single universal curve; g_h of "
             "lead-free Sn/Ge deviates +0.5..+1.9 (smaller CB SOC Delta). TB-derived P "
             "underestimates 6.8 (Blount-1962 incompleteness).",
    "readme": "Theme A g-factor production bundle (retroactive). k.p universal relation "
              "with TB-derived Delta and P for 9 CsBX3. Main result: lead-free g_h "
              "breakdown of the universal relation. See cowork/reports/theme_A_g_factor.md.",
}

PHASE15 = {
    "theme": "phase_1.5_optical",
    "subtask": "B4 convergence + B5 9-material dielectric scan",
    "physics_method": "Independent-particle (Kubo-Greenwood) eps(omega) from velocity "
                      "operator (Apergi 2023 Eq.3,4); KK for eps_1; Lorentzian eta.",
    "convergence": {"k_grid": "6^3, 8^3, 12^3 (results/optical/convergence.md)",
                    "eta_eV": "0.03, 0.05, 0.08",
                    "result": "absorption edge -> Eg with finer k; f-sum ~0.21 stable "
                              "(Blount-1962 TB incompleteness, not numerical)"},
    "outputs": [
        ("results/optical/9material_optical_summary.csv", "raw/9material_optical_summary.csv"),
        ("results/optical/convergence.md", "raw/convergence.md"),
        ("results/optical/9material_eps_imag.png", "figures/9material_eps_imag.png"),
        ("results/optical/CsPbI3_dielectric.png", "figures/CsPbI3_dielectric.png"),
    ],
    "inputs": [
        ("data/parameters/kashikar2021_cubic_13orb.json", "kashikar2021_cubic_13orb.json"),
        ("data/parameters/nestoklon2021_CsPbI3.json", "nestoklon2021_CsPbI3.json"),
    ],
    "cli": ("PYTHONPATH=src python scripts/optical_convergence.py\n"
            "PYTHONPATH=src python scripts/scan_optical_9materials.py\n"
            "PYTHONPATH=src python scripts/scan_optical.py\n"),
    "key_numbers": {"CsPbI3_eps_inf": 3.46, "CsPbBr3_eps_inf": 2.35, "CsPbCl3_eps_inf": 1.46,
                    "f_sum_ratio": 0.21, "CsPbI3_abs_edge_12cubed_eV": 1.79},
    "references": ["Apergi 2023 arXiv:2309.14002 Eq.3,4",
                   "Cho 2019 arXiv:1908.09436", "Blount 1962 Phys.Rev.126,1636"],
    "notes": "Retroactive. Absorption edge tracks gap; eps_inf ordering "
             "CsPbI3>CsPbBr3>CsPbCl3 matches experiment; absolute values low (Blount-1962).",
    "readme": "Phase 1.5 optical production bundle (retroactive). Independent-particle "
              "dielectric function of 9 CsBX3. See cowork/reports/theme_A5_optical.md.",
}


if __name__ == "__main__":
    build_bundle(THEME_A)
    build_bundle(PHASE15)
