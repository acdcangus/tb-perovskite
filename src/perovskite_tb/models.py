"""Model registry: map a parameter-file ``model_kind`` to a Hamiltonian builder.

A *Hamiltonian builder* is a callable ``H(kvec_cart) -> (N, N) complex ndarray``
already specialised to a material's parameters and lattice constant.  Each model
also declares ``n_filled`` (number of occupied spin-bands per cell), used to
locate the fundamental gap.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping

import numpy as np

from . import models_kashikar as mk


@dataclass
class ModelSpec:
    builder: Callable[[np.ndarray], np.ndarray]
    n_filled: int
    n_bands: int
    description: str


def build_model(loaded: Mapping) -> ModelSpec:
    """Build a :class:`ModelSpec` from an :func:`io_params.get_material` result."""
    kind = loaded["model_kind"]
    params = loaded["params"]
    a = loaded["a"]

    if kind == "slater_koster_13orbital":
        return ModelSpec(
            builder=lambda k: mk.kashikar13_hamiltonian(k, params, a),
            n_filled=20,  # VEC = 20 electrons per formula unit (Kashikar Sec. II)
            n_bands=26,
            description="Kashikar 13-orbital (B-{s,p} + 3x X-p) + SOC",
        )
    if kind == "slater_koster_4orbital_minimal":
        return ModelSpec(
            builder=lambda k: mk.kashikar4_hamiltonian(k, params, a),
            n_filled=2,  # only the s-derived anti-bonding band is filled
            n_bands=8,
            description="Kashikar 4-orbital minimal (B-{s,p}) + SOC",
        )
    if kind == "empirical_tight_binding_jancu_spds":
        from . import models_nestoklon as mn

        basis = loaded.get("basis")
        builder = mn.make_builder(params, a, basis)
        n_orb = len(basis)
        return ModelSpec(
            builder=builder,
            # Occupied manifold: I-s (3) + Pb-s (1) + I-p (9) = 13 spatial bands
            # -> 26 spin-bands (Pb(2+) 6s^2 and three I(-) 5s^2 5p^6).
            n_filled=26,
            n_bands=2 * n_orb * 4,  # n_orb per atom x 4 atoms x 2 spin
            description=f"Nestoklon Jancu sp3d5s* ETB ({n_orb} orb/atom) + SOC",
        )

    raise ValueError(f"Unknown model_kind '{kind}'.")
