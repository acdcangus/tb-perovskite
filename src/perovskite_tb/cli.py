"""Command-line interface for perovskite_tb.

Examples
--------
Compute & plot a band structure (with a reproducibility-metadata sidecar JSON)::

    python -m perovskite_tb band \
        --params data/parameters/kashikar2021_cubic_13orb.json \
        --material CsPbI3 \
        --config configs/cubic_MRGXM.json \
        --out results/CsPbI3_kashikar13.png

Report the fundamental gap(s)::

    python -m perovskite_tb gap \
        --params data/parameters/kashikar2021_cubic_13orb.json --material all
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from . import kpath as kp
from ._meta import run_metadata
from .bandstructure import compute_band_structure, direct_gap, fundamental_gap
from .io_params import get_material, list_materials, load_parameter_file
from .models import build_model


def _load_config(path: str | None):
    if path is None:
        # default: cubic M-R-G-X-M-G path
        return {"name": "cubic_MRGXM", "segments": ["M", "R", "G", "X", "M", "G"],
                "n_per_segment": 120}
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _prepare(args):
    data = load_parameter_file(args.params)
    loaded = get_material(data, material=getattr(args, "material", None),
                          parameter_set=getattr(args, "parameter_set", None))
    spec = build_model(loaded)
    return data, loaded, spec


def cmd_band(args):
    data, loaded, spec = _prepare(args)
    cfg = _load_config(args.config)
    a = loaded["a"]
    path = kp.make_kpath(cfg["segments"], a, cfg.get("n_per_segment", 120))
    bs = compute_band_structure(spec.builder, path, spec.n_filled)
    gi = fundamental_gap(bs)

    title = f"{loaded.get('material','')} — {spec.description}"
    out = args.out or f"results/{loaded.get('material','band')}.png"
    from .plotting import save_band_structure
    save_band_structure(bs, out, title=title, gap_info=gi)

    # Reproducibility sidecar.
    sidecar = Path(out).with_suffix(".json")
    meta = run_metadata({
        "model_id": loaded["model_id"],
        "model_kind": loaded["model_kind"],
        "material": loaded.get("material", ""),
        "parameter_set": getattr(args, "parameter_set", None),
        "lattice_constant_a": a,
        "params": loaded["params"],
        "kpath_segments": cfg["segments"],
        "n_per_segment": cfg.get("n_per_segment", 120),
        "n_filled": spec.n_filled,
        "fundamental_gap": gi,
    })
    with sidecar.open("w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)
    print(f"wrote {out}")
    print(f"wrote {sidecar}")
    print(f"  gap = {gi['gap']:.4f} eV ({'direct' if gi['direct'] else 'indirect'})")


def cmd_gap(args):
    data, _loaded, _spec = _prepare(args) if args.material not in ("all", None) else (
        load_parameter_file(args.params), None, None)

    materials = (list_materials(data) if (args.material in ("all", None) and "materials" in data)
                 else [args.material])

    print(f"# {data['model_id']}")
    print(f"{'material':10s} {'a(A)':>6s} {'gap_R(eV)':>10s} {'fundamental_gap(eV)':>20s}")
    for mat in materials:
        loaded = get_material(data, material=mat if "materials" in data else None,
                              parameter_set=getattr(args, "parameter_set", None))
        spec = build_model(loaded)
        a = loaded["a"]
        kR = np.array([np.pi / a] * 3)
        g_R = direct_gap(spec.builder, kR, spec.n_filled)
        # fundamental gap from a path sample
        path = kp.make_kpath(["M", "R", "G", "X", "M", "G"], a, 80)
        bs = compute_band_structure(spec.builder, path, spec.n_filled)
        gi = fundamental_gap(bs)
        print(f"{mat:10s} {a:6.2f} {g_R:10.4f} {gi['gap']:20.4f}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="perovskite-tb",
                                description="Tight-binding band structure of cubic halide perovskites.")
    sub = p.add_subparsers(dest="command", required=True)

    pb = sub.add_parser("band", help="compute and plot a band structure")
    pb.add_argument("--params", required=True, help="parameter JSON file")
    pb.add_argument("--material", help="material name (for multi-material files)")
    pb.add_argument("--parameter-set", dest="parameter_set",
                    help="parameter set (Nestoklon: sp3 / sp3d5sstar / experiment_corrected)")
    pb.add_argument("--config", help="k-path config JSON (default: M-R-G-X-M-G)")
    pb.add_argument("--out", help="output image path")
    pb.set_defaults(func=cmd_band)

    pg = sub.add_parser("gap", help="report fundamental and R-point gaps")
    pg.add_argument("--params", required=True)
    pg.add_argument("--material", default="all", help="material name or 'all'")
    pg.add_argument("--parameter-set", dest="parameter_set")
    pg.set_defaults(func=cmd_gap)

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
