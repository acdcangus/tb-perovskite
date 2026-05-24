"""Shared test helpers (Pauli matrices, standard test models, material loader).

Imported by the property-module test files to avoid duplicating the same small
constants / model builders.  pytest runs with ``tests`` on the path (prepend
import mode), so ``from _helpers import ...`` resolves.
"""

import numpy as np

from perovskite_tb.io_params import get_material, load_parameter_file

# Pauli matrices (used by the 2-band test models).
SX = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
SY = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
SZ = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)

_K13 = "data/parameters/kashikar2021_cubic_13orb.json"


def load_kashikar13(name="CsPbI3"):
    """Return (params, a) for a cubic CsBX3 material (Kashikar-13 dataset)."""
    m = get_material(load_parameter_file(_K13), name)
    return m["params"], m["a"]


def qwz_hamiltonian(kx, ky, u):
    """Qi-Wu-Zhang 2-band Chern-insulator Bloch Hamiltonian (PRB 74, 085308 (2006))."""
    return (np.sin(kx) * SX + np.sin(ky) * SY
            + (u + np.cos(kx) + np.cos(ky)) * SZ)
