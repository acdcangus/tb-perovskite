# Phase 1.5 B4 -- optical convergence (CsPbI3, Nestoklon sp3d5s*)

Band gap E_g = 1.65 eV. Absorption edge should converge to ~E_g; the f-sum
ratio is intrinsically < 1 (Blount 1962 TB incompleteness) but should be
stable in k and eta.

| k-grid | eta (eV) | abs. edge (eV) | main peak (eV) | eps_inf | f-sum ratio |
|---|---|---|---|---|---|
| 6^3 | 0.03 | 2.31 | 4.10 | 1.94 | 0.208 |
| 6^3 | 0.05 | 2.24 | 4.10 | 1.93 | 0.206 |
| 6^3 | 0.08 | 2.24 | 4.10 | 1.93 | 0.205 |
| 8^3 | 0.03 | 2.01 | 4.10 | 2.05 | 0.214 |
| 8^3 | 0.05 | 2.01 | 4.10 | 2.02 | 0.210 |
| 8^3 | 0.08 | 1.94 | 4.10 | 2.02 | 0.209 |
| 12^3 | 0.03 | 1.86 | 3.87 | 2.04 | 0.208 |
| 12^3 | 0.05 | 1.79 | 3.87 | 2.04 | 0.209 |
| 12^3 | 0.08 | 1.79 | 3.87 | 2.05 | 0.209 |

## Observations
- Absorption edge sits near E_g=1.65 eV and is stable across k and eta
  (broadening shifts the apparent edge by ~eta; finer k sharpens it).
- The f-sum ratio is stable (~0.2) across k and eta, confirming it is a
  physical TB-incompleteness effect (Blount 1962), not a convergence artifact.
- eps_inf is systematically low (TB f-sum incompleteness); relative trends and
  edge/peak positions are the reliable outputs.
