# tasklist — F1 berry.py

## 実装 ✅
- [x] `src/perovskite_tb/berry.py` 新規（SPDX, docstring に Xiao2010 Eq.1.13 / Fukui2005 / Sinova2015 / QWZ2006 引用）
  - [x] `velocity_matrix`
  - [x] `berry_curvature_kubo`（Xiao Eq.1.13, 縮退除外）
  - [x] `spin_berry_curvature_kubo` + `spin_current_operator`（j^z_α=½{s_z,v_α}, Sinova2015）
  - [x] `link_variable_chern`（Fukui2005, 非アーベル=行列式形; 符号を Kubo 規約に整合）
  - [x] `anomalous_hall_sum` / `spin_hall_sum`（n_occ または e_fermi 占有）
  - [x] `kashikar13_at_k`, `spin_operators`, `occupied_curvature_sum`（既存再利用）
## V&V ✅
- [x] `tests/test_berry.py`（22 ケース）
- [x] Dirac 解析一致 / QWZ 整数 Chern+相図 / Kubo↔Fukui 一致 / 立方 P·T → AHC=0（~1e-15）/ su(2) 代数
- [x] `pytest` 全体 **253 passed**（既存 231 + 新規 22）, 回帰ゼロ
## docs（CLAUDE.md）✅
- [x] `docs/numerical-methods.md` §9 Berry/AHC/SHC/Chern 節
- [x] `docs/repository-structure.md` に berry.py + 物性モジュール群
## 実装中の発見・修正（記録）
- Berry 曲率符号: ar5iv で Xiao Eq.(1.13) を確認、Kubo 規約で下バンド Dirac Ω₋=+m/(2|d|³) を解析導出 → 一致。
- Fukui Chern 符号: 連続極限導出（A=i⟨u|∂u⟩ で Im ln(plaquette)→−Ω dk²）より −(1/2π)Σ に修正、Kubo と整合。
- 立方ペロブスカイト: 0.96 eV に halide-p flat band（多重縮退）。AHC=0 検証は固定バンド数でなく**実ギャップ内 Fermi 準位**で占有選択（縮退多重項を割らない）。
## commit
- [ ] key leak ガード, push

## deferred（roadmap, 別 .steering で着手）
- F2 topology（Fu-Kane parity Z₂ / Wilson loop / slab）— berry.py の Fukui 基盤を再利用可
- F3 BSE / F4 Rashba / F5 2D RP slab / F6 polaron / F7 CPGE / F8 SHG / F9 thermo / F11 Edelstein / F12 strain / F13 stack / F14 Efield
- 各機能は着手前に引用 DOI を web 検証（handoff サイクル A）
