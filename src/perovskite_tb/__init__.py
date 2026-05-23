"""perovskite_tb - tight-binding band structure of cubic halide perovskites.

All models and parameters are grounded in published literature; see
``data/parameters/SOURCES.md`` for provenance. No parameter is invented.

Implemented models
------------------
* ``kashikar13`` : 13-orbital Slater-Koster model (B-{s,p} + 3x X-p) with SOC,
  cubic CsBX3.  Source: Kashikar, Gupta & Nanda, arXiv:2101.08562.
* ``kashikar4``  : 4-orbital minimal model (B-{s,p}) with SOC.  Same source.
* ``nestoklon``  : Jancu sp3 / sp3d5s* nearest-neighbour ETB for cubic CsPbI3.
  Source: Nestoklon, arXiv:2012.14705.
"""

from .bandstructure import (
    BandStructure,
    compute_band_structure,
    direct_gap,
    eigenvalues_at_k,
)
from .io_params import load_parameter_file, get_material
from . import kpath

__all__ = [
    "BandStructure",
    "compute_band_structure",
    "direct_gap",
    "eigenvalues_at_k",
    "load_parameter_file",
    "get_material",
    "kpath",
]

__version__ = "0.1.0"
