# PI 起床サマリ — 2026-05-24 朝

PI 不在中（5/23 14:40〜）の自走成果まとめ。**この1本 + `RESULTS.md` で全体把握できます。**
（Cowork 監督 + Claude Code 実装、ハルシネーション禁止・論文値検証最優先で進行）

---

## 1. TL;DR（最大の発見）

1. **★ Theme F (shift current/BPVE) 完了。鉛フリー Sn/Ge ハライド（特にヨウ化物）が Pb 系より大きい
   shift current** を示した（CsSnI₃ 3.43 > CsGeI₃ 2.67 ≫ CsPbI₃ 0.97、相対単位）。毒性 Pb 代替の光起電候補。
2. **★ 検証で F3 のバグを自力検出・修正。** TB の shift-current 一般化微分には Fregoso 2017 Eq.(C2) の
   **第2微分 w 項が必須**（連続形では 2-band で σ≡0）。Rice-Mele 閉形式 Eq.(D15)/(D16) と**機械精度一致で
   符号・prefactor 確定**。旧 F3 値は符号逆・~2.4× 過小だったため破棄・置換。
3. 性能: batched eigh が multithread BLAS で病的に遅い問題を発見 → single-thread で **~48× 高速化**。

## 2. 何をやったか（時系列ハイライト）

- F4-3: Rice-Mele 解析閉形式照合 → w 項欠落バグ検出 → Fregoso C2 で修正・検証（`tests/test_shift_current_rice_mele.py`）。
- F4-2: Tan & Rappe 2016 の対称則（δ→−δ で符号反転 等）を多バンドで確認。
- F5: polar Kashikar-13 builder（k 方向ベクトル化）+ 9 材料 × δ スキャン（Production）。
- F6: 報告書 `cowork/reports/theme_F_shift_current.md`、定式化 `docs/shift-current-formulation.md` 更新。
- 品質: 全 **228 テスト通過**、`RESULTS.md` 更新、Production bundle 3 本すべて git_dirty:false。

## 3. Production bundle 3 本（key_numbers 要約）

| bundle | 主数値 |
|---|---|
| `theme_A_g_factor/2026-05-23_31374dc` | g_e: CsPbI₃ 3.01 / CsSnI₃ 4.56 / CsGeI₃ 3.39。g_h 乖離（鉛フリー上方）: CsGeI₃ +1.86, CsSnI₃ +1.81。TB 導出 P(CsPbI₃)=5.44（普遍 6.8） |
| `phase_1.5_optical/2026-05-23_31374dc` | ε_∞: CsPbI₃ 3.46 / CsPbBr₃ 2.35 / CsPbCl₃ 1.46。吸収端 CsPbI₃ 1.79 eV。f-sum=0.21（Blount 過小、既知） |
| `theme_F_shift_current/2026-05-23_ef575e3` | ピーク |σ_zzz|（δ=0.15, rel）: CsSnI₃ 3.43 > CsGeI₃ 2.67 > CsSnBr₃ 1.31 ≈ CsGeBr₃ 1.30 > CsPbI₃ 0.97。σ は gap と逆相関。δ=0 で σ=7e-15 |

## 4. 新規性の確信度（2 大 finding）

- **g_h 普遍関係の破れ（Theme A）**: Kirstein 2021 の正孔 g 因子普遍関係は Pb 系で成立するが、
  **鉛フリー Sn/Ge で上方乖離（Δ→0 で g_h→+2）**。TB（Roth-Lax + k·p）で系統的に示した。確信度：高（9 材料で一貫）。
- **Sn/Ge ハライドの大 shift current（Theme F）**: 確信度：中〜高（相対比較は頑健、順位は n_kpts 24↔48 で不変）。
  ただし絶対値は未較正（§5）、立方相 + 単一極性モードの簡略化。

## 5. 未解決・要 PI 判断

1. **shift current 絶対値較正**: 相対単位を一次成果として deferred。recipe は文書化済み
   （Hughes-Sipe 1996 PRB 53 Eqs.B6/B7 の prefactor + Tan & Rappe 2015 の公表 σ にアンカー）。
   規約敏感 + Blount 限界のため、慎重な専用パスで実施したい。**PI 判断: 絶対較正を次に回すか、相対のまま論文化するか。**
2. **D ドライブ古典原典 16 本（Kane/Vogl/Luttinger 等）**: **私の実行環境（Linux コンテナ）から D: にアクセス不可**
   （`/mnt/d` 無し）。**PI 側で `references/pdfs/classic_*.pdf` に配置をお願いします**（または書誌情報引用で代替）。
3. **次テーマ選択（next_directive 優先 8 / future_themes）**: 下記推奨。

## 6. 次のおすすめテーマ

- **Theme I（Wannier-Mott 励起子結合エネルギー）**: 軽量（100-150 行）。既存の有効質量（Theme A 枠組み）+ ε_∞
  （Phase 1.5 出力）を流用、`E_b=(μ/m₀)/ε_∞²×13.6 eV`。文献 Cho 2019 GW-BSE 等で照合可。Production 化込みで 2-3h 見込み。
- 余力があれば shift current 絶対較正（§5-1）も価値大。

## 付記（Cowork へ）
2155 status check / 2225 BLOCKED は **セッション一時中断**によるものでした（I/O ではなく長時間ギャップ）。
復帰済み。本サマリ作成をもって 2125 nudge の Option A に対応。Theme F は完了、次は PI 判断待ち or Theme I。
