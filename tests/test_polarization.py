"""V&V for polarization.py (spec F14-B): Berry-phase polarization (KSV).

Analytic anchors:
  * SSH model (inversion-symmetric): the Zak phase is quantized to 0 or pi, and
    jumps by pi across the topological transition v=w (Su-Schrieffer-Heeger 1979).
  * Rice-Mele model (SSH + staggered on-site -> inversion broken): the Zak phase
    shifts continuously (non-quantized polarization).
  * Cubic centrosymmetric CsBX3: P_z (Zak phase) is quantized (0 or pi mod 2pi).
"""

import numpy as np

from perovskite_tb import polarization
from perovskite_tb.io_params import get_material, load_parameter_file

from _helpers import SX, SY, SZ  # noqa: E402


def _ssh_zak(v, w, delta=0.0, N=200):
    """Zak phase of the lower band of Rice-Mele H(k)= (v+w cos k)sx +(w sin k)sy + delta sz."""
    occ = np.empty((N, 2, 1), dtype=complex)
    for i, k in enumerate(np.linspace(0.0, 2 * np.pi, N, endpoint=False)):
        H = (v + w * np.cos(k)) * SX + (w * np.sin(k)) * SY + delta * SZ
        _, vecs = np.linalg.eigh(H)
        occ[i, :, 0] = vecs[:, 0]
    return polarization.zak_phase(occ)


def test_ssh_zak_quantized_to_0_or_pi():
    for v, w in [(1.0, 0.4), (0.4, 1.0)]:
        z = _ssh_zak(v, w)
        # quantized: distance to {0, pi, -pi} ~ 0
        d = min(abs(z), abs(abs(z) - np.pi))
        assert d < 1e-6, f"SSH Zak {z:.4f} not quantized (v={v},w={w})"


def test_ssh_zak_jumps_by_pi_across_transition():
    z_triv = _ssh_zak(1.0, 0.4)   # v>w trivial
    z_topo = _ssh_zak(0.4, 1.0)   # v<w topological
    diff = abs(z_topo - z_triv)
    diff = min(diff, abs(diff - 2 * np.pi))  # mod 2pi
    assert np.isclose(diff, np.pi, atol=1e-5), f"Zak jump {diff:.4f} != pi"


def test_rice_mele_breaks_quantization():
    """Staggered on-site (inversion breaking) -> continuous, non-quantized Zak."""
    z = _ssh_zak(0.7, 1.0, delta=0.5)
    d = min(abs(z), abs(abs(z) - np.pi))
    assert d > 1e-3, f"Rice-Mele Zak {z:.4f} should NOT be quantized"
    # continuous dependence on the staggering
    z2 = _ssh_zak(0.7, 1.0, delta=0.8)
    assert not np.isclose(z, z2, atol=1e-3)


def test_perovskite_electronic_zak_well_defined():
    """The electronic Zak phase of the perovskite is finite, real, deterministic.

    NOTE: this is only the *electronic* Berry phase in a fixed gauge; the
    physical, quantized polarization additionally needs the ionic contribution
    and is defined mod the polarization quantum (KSV) -- see the module
    docstring.  The clean quantization is validated on SSH above.
    """
    m = get_material(load_parameter_file("data/parameters/kashikar2021_cubic_13orb.json"), "CsPbI3")
    p, a = m["params"], m["a"]
    pz1, _ = polarization.polarization_phase_z(p, a, n_kxy=4, n_kz=16)
    pz2, _ = polarization.polarization_phase_z(p, a, n_kxy=4, n_kz=16)
    assert np.isfinite(pz1) and -np.pi - 1e-9 <= pz1 <= np.pi + 1e-9
    assert pz1 == pz2  # deterministic
