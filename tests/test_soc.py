"""Spin-orbit coupling matrix: physics sanity checks."""

import numpy as np

from perovskite_tb._soc import soc_p_matrix


def test_p_soc_eigenvalues():
    """lambda L.S on p-orbitals: eigenvalues +lambda/2 (x4, j=3/2), -lambda (x2, j=1/2)."""
    lam = 0.37
    ev = np.sort(np.linalg.eigvalsh(soc_p_matrix(lam)))
    expected = np.sort(np.array([-lam, -lam, lam / 2, lam / 2, lam / 2, lam / 2]))
    assert np.allclose(ev, expected, atol=1e-12)


def test_p_soc_traceless_and_hermitian():
    lam = 1.23
    H = soc_p_matrix(lam)
    assert np.allclose(H, H.conj().T, atol=1e-14)          # Hermitian
    assert abs(np.trace(H).real) < 1e-12                    # traceless
    # j=3/2 / j=1/2 splitting is 3*lambda/2
    ev = np.sort(np.linalg.eigvalsh(H))
    assert abs((ev[-1] - ev[0]) - 1.5 * lam) < 1e-12


def test_zero_lambda_gives_zero():
    assert np.allclose(soc_p_matrix(0.0), 0.0)
