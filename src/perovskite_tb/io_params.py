"""Loading of parameter files (JSON) and material lookup.

Parameter files live in ``data/parameters/`` and carry full provenance
(source paper, table, units) alongside the numeric values.  See
``data/parameters/SOURCES.md``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping


def load_parameter_file(path: str | Path) -> dict[str, Any]:
    """Load a parameter JSON file and return its full contents."""
    path = Path(path)
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if "model_id" not in data:
        raise ValueError(f"{path}: missing 'model_id'")
    return data


def list_materials(data: Mapping[str, Any]) -> list[str]:
    """Return the material names available in a Kashikar-style parameter file."""
    if "materials" in data:
        return sorted(data["materials"].keys())
    # Nestoklon-style single-material file.
    return [data.get("model_id", "<single-material>")]


def get_material(data: Mapping[str, Any], material: str | None = None,
                 parameter_set: str | None = None) -> dict[str, Any]:
    """Return a flat dict of numeric parameters plus context for one material.

    For multi-material files (Kashikar) ``material`` selects the compound.
    For the Nestoklon file ``parameter_set`` selects one of
    {sp3, sp3d5sstar, experiment_corrected}.

    Returns a dict with keys:
        model_id, model_kind, params (flat numeric mapping), a (lattice const),
        basis (list of orbital labels, when defined), extra (raw entry).
    """
    model_kind = data.get("model_kind", "")

    if "materials" in data:
        if material is None:
            raise ValueError("This parameter file requires a 'material' selection. "
                             f"Available: {list_materials(data)}")
        if material not in data["materials"]:
            raise KeyError(f"Material '{material}' not found. "
                           f"Available: {list_materials(data)}")
        entry = data["materials"][material]
        return {
            "model_id": data["model_id"],
            "model_kind": model_kind,
            "params": dict(entry["params"]),
            "a": float(entry["a"]),
            "basis": None,
            "extra": entry,
            "material": material,
        }

    # Nestoklon-style: parameter_sets + structure.
    if "parameter_sets" in data:
        if parameter_set is None:
            raise ValueError("This parameter file requires a 'parameter_set' selection. "
                             f"Available: {sorted(data['parameter_sets'].keys())}")
        if parameter_set not in data["parameter_sets"]:
            raise KeyError(f"parameter_set '{parameter_set}' not found. "
                           f"Available: {sorted(data['parameter_sets'].keys())}")
        pset = data["parameter_sets"][parameter_set]
        flat: dict[str, float] = {}
        for group in ("onsite", "two_center", "spin_orbit"):
            flat.update(pset.get(group, {}))
        a = float(data["structure"]["lattice_constant_angstrom"])
        return {
            "model_id": data["model_id"],
            "model_kind": model_kind,
            "params": flat,
            "a": a,
            "basis": pset.get("basis"),
            "extra": {"data": data, "parameter_set": parameter_set,
                      "verification_targets": data.get("verification_targets", {}),
                      "zeroed_integrals": data.get("zeroed_integrals", {})},
            "material": data.get("structure", {}).get("cation_c", "") +
                        data.get("structure", {}).get("anion_a", ""),
        }

    raise ValueError("Unrecognized parameter file layout (no 'materials' or "
                     "'parameter_sets').")
