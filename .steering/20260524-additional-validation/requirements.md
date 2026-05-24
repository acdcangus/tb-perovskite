# 追加検証タスク（09_additional_validation_tasks.md 由来）— requirements

**作成日**: 2026-05-24
**起点**: `extention/09_additional_validation_tasks.md`（PI 指示）＋ `extention/08_validation_status_quantitative.md`
**ユーザ追加制約 (2026-05-24)**: 追加機能は **基本的にコアの TB（Kashikar/Nestoklon）が計算したエネルギー・波動関数を使う**。論文値は検算（cross-check）用。トイモデルは手法検証（B カテゴリ）専用で、材料の物性予測（A 比較）はコア TB から導く。

## 目的
F1–F14 の検証を「内部アンカー(B)」中心から「論文値との定量比較(A)」へ可能な範囲で拡充する。ただし **SK-TB / Blount caveat により絶対値が構造的に未検証な量は honest に維持**し、比・符号・トレンド・量子化での比較を厳密化する。

## タスク（09 より）
- **T1-1 (F5 slab)**: 2D RP 量子閉じ込め E_g(n) のトレンドを Blancon 2018（自由粒子ギャップ）と比較。
- **T1-2 (F12 strain)**: dE_g/dε を文献 DFT 値と符号厳密一致＋大きさ比較。
- **T1-3 (F6 polaron)**: 9 CsBX₃ 材料の α マップを **TB 由来 m\*** ＋ 引用済み誘電/LO データで完成。
- **T2-1 (F4 Rashba)**: バルク極性相 α_R を DFT 値と桁レベル比較。
- **T2-2 (F1/F2)**: Fu-Kane-Mele 3D 模型で Z₂ 相＋Berry 曲率符号反転、Z₂ parity 法実装。
- **T2-3 (F14-B 分極)**: 強誘電 PE→FE の ΔP（電子寄与, gauge 不変）を DFT 値と桁・符号一致。
- **T2-4 (F11 Edelstein)**: τ がキャンセルする χ_yx/σ_xx 比を実装し Rashba 解析値と一致確認。

## 受け入れ条件（honest 版）
1. 既存 314 テスト **不変**。追加検証は新規テスト or 既存テストへの append。
2. **新規引用文献の DOI を全件 web 事前確認**（サイクル A）。誤引用は訂正、根拠が立たなければ SKIP。
3. 各比較の **真のカテゴリ（A/B/C/D）を honest に記録**。SK-TB 限界由来の絶対値は D を維持。
4. benchmark JSON に文献値を出典付きで保管。比較プロットを `results/figures/` に保存。
5. `docs/numerical-methods.md` の該当 V&V 節、`08_*` 報告書を更新。

## 文献の事前確認結果（サイクル A, 2026-05-24）
- **Blancon「Scaling law」= Nat. Commun. 9, 2254 (2018), DOI 10.1038/s41467-018-04659-x**。
  指示書の「Science 355,1288 (2017) / 10.1126/science.aal4211」は **edge-states 論文との取り違え（訂正）**。
- 自由粒子ギャップ（Fig.3a caption, 検証済 exact）: n=1: 2.540±0.004, n=4: 2.078±0.012, n=5: 1.846±0.004 eV。
- Buin 2014 (Nano Lett. 14, 6281, DOI 10.1021/nl502612m) 実在確認。ただし内容は **trap-free 合成**で、strain dE_g/dε の出典としては不適の疑い → T1-2 で精査。
- Grumet PRB 98, 155143 (2018)（Grumet, Liu, Kaltak, Klimeš, Kresse）実在確認。内容（strain/deformation potential か）は要精査 → T1-2。
