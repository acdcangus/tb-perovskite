# Supervisor patrol — 2026-05-23 17:40 JST (14:37 UTC)

**監督:** Cowork (scheduled task `tb-perovskite-supervisor`, 15-min cycle)
**前回:** 1725 (14:22 UTC) — F4-2 完了 + polish 両方 APPROVE、F5 design レビュー待ち
**今回判定:** ✅ **F5 ビルダー (`9eeff23`) APPROVE — 9 材料 Production スキャン着手 OK（ただし design.md 提出推奨）**

---

## 1. 直近 30 分の進捗確認

| 時刻 (UTC) | イベント | 内容 | 判定 |
|---|---|---|---|
| 14:13 | commit `7dc525e` | polish (wvc/wcv comment + guard) | 前回 APPROVE 済み |
| 14:14 | commit `69f5c63` | F4-2 multi-band sign-reversal test | 前回 APPROVE 済み |
| 14:25 | `2026-05-23_1425_critical_references_obtained.md` | Hughes-Sipe 1996 / Tan&Rappe 2016 / Tan&Rappe 2015 取り込み報告 | Cowork 自己発行 |
| 14:36 | `2026-05-23_1435_boyer_richard_2016_added.md` | Boyer-Richard 2016 (HAL OA) 取り込み報告 | Cowork 自己発行 |
| 14:37 | **commit `9eeff23`** | **F5: polar Kashikar-13 builder** | **本パトロールで APPROVE** |

最新コミット: `9eeff23` "F5: polar Kashikar-13 builder for 9-material shift-current scan"（patrol 時点で 43 秒前）。

## 2. F5 ビルダー (`9eeff23`) のレビュー

`make_polar_kashikar13_builders` を `git show HEAD -- src/perovskite_tb/shift_current.py` で精読。

### 2.1 物理・幾何の正しさ

| # | 項目 | 結果 |
|---|---|---|
| 1 | 軌道基底 = Kashikar-13（Pb-{s,p}+3×I-p、spin 込み 26） | ✅ `mk.N_ORB_13 = 13`、`Hf = np.kron(I_2, H)` で spinful 化 |
| 2 | [001] B 変位で **B-X3 z-bond のみ**非対称化（x,y は対称のまま） | ✅ axes 0,1 は `S(d), C(d)`、axis 2 のみ `Zpol(sign)` |
| 3 | 結合長: `d_plus = a/2 - delta`、`d_minus = a/2 + delta`（B が +z 側 X に近づく規約） | ✅ 物理的に妥当 |
| 4 | Harrison スケーリング: `s = (a/2/d)^η`、η=2.0（既定） | ✅ Harrison 1980 標準 |
| 5 | s-p σ は odd（`sign=-1`）、p-p は even（`sign=+1`） | ✅ Slater-Koster 規約と整合 |
| 6 | SOC は k 非依存 → order=0 のみに寄与（dH/d2H には入らない） | ✅ `if o0: ... soc_p_from_lambda3(...)` 分岐正しい |
| 7 | エルミート化: `H = H + H† − diag(diag(H).real)`（対角の二重カウント除去） | ✅ Nestoklon 版と同型、既に F4 で検証済みパターン |
| 8 | δ=0 で `kashikar13_hamiltonian` と bit-exact 一致 | ✅ test `test_polar_kashikar_reduces_to_base_at_zero` で `atol=1e-12` |
| 9 | dH/d2H が Hermitian かつ 中心差分と一致 | ✅ 同テスト内、`atol=1e-3` の FD 比較 |

### 2.2 対称性テストの妥当性

`test_polar_kashikar_shift_current_symmetry`（n_occ=20, ω∈[0.5,3.5] eV, n_kpts=4, η=0.08）:

| 主張 | 物理的根拠 | 数値 tol | 評価 |
|---|---|---|---|
| `s0 < 1e-10`（δ=0 で σ_zzz 消失） | Pm-3m は inversion を持つ → σ^{(2)}=0 (Neumann) | 厳しい | ✅ |
| `sp + sm < 1e-9 × max(|sp|,1)`（δ→−δ で符号反転） | [001] δ→−δ は空間反転 → σ_zzz は odd | 機械精度 | ✅ Tan&Rappe 2016 Eq.14 則 2 |
| `sx < 1e-8`（P4mm で σ_xxx 禁止） | P4mm の polar 軸は [001]、x 方向は σ_v 鏡映で禁止 | 妥当 | ✅ |
| n_occ=20（Pb-s² + 3×I-p⁶ = 2 + 18） | Pb²⁺ (6s²) + 3 I⁻ (5p⁶) = 半導体閉殻 | — | ✅ |

**n_occ=20 の確認:** Kashikar 13 軌道 = Pb-s(1) + Pb-p(3) + I1-p(3) + I2-p(3) + I3-p(3) = 13。spinful で 26。占有は Pb-s(2)+I-p(6)×3 = 20。伝導帯 = Pb-p×2 = 6。妥当。

### 2.3 残課題（design.md で確認したい）

| 項目 | 状況 |
|---|---|
| 9 材料の polar δ 値の決め方 | 未明示。Cs(Pb/Sn/Ge)(Cl/Br/I)₃ で同じ δ にするか、材料ごとに DFT 平衡値を使うか? |
| Harrison η = 2.0 固定の妥当性 | 標準値だが Cs(Pb/Sn/Ge) で揃えるなら sensitivity check 1 回欲しい |
| `d2Hdk_fn` を必ず渡す（continuum form 禁止） | F4-3 で guard 追加済み、F5 でも適用される |
| k グリッド収束: shift current は 8/12/16 では足りない | F5 design.md で n_kpts ≥ 32 から開始する旨を patrol 1725 §6 で要請済み |
| Production: MANIFEST.references に Hughes-Sipe 1996 / Tan&Rappe 2015/2016 / Fregoso 2017 / Kashikar 2021 を列挙 | design.md で確認 |

**判定: ビルダー実装は physics・symmetry・bit-exact reduction 全て揃って APPROVE**。F5 本体（9 材料 Production スキャン）に進んで OK。ただし **design.md を Production 実行前に提出**してください（patrol 1725 §6 のチェックリスト 6 項目）。

## 3. Boyer-Richard 2016 / Hughes-Sipe 1996 / Tan&Rappe 2015/2016 取り込み確認

Cowork 側で 4 本の重要文献を `references/pdfs/` に取り込み完了:

```
doi_10.1021_acs.jpclett.6b01749_BoyerRichard2016.pdf   (884 KB, HAL OA)
doi_10.1103_PhysRevB.53.10751.pdf                       (Hughes-Sipe 1996)
doi_10.1038_npjcompumats.2016.26.pdf                    (Tan&Rappe 2016 npj CM)
arxiv_1508.03564.pdf                                     (Tan&Rappe 2015 CsPbI3+BiTeI)
```

**Theme F への影響:** Tan&Rappe 2016 Eq.14 が既に F4-2 の符号確定に活用済み。Hughes-Sipe 1996 は **F5 で絶対前因子 e³/ℏ⁴ を docstring に明記する際の primary source** になる。

**Theme A への影響:** Boyer-Richard 2016 は MAPbI₃ symmetry-based TB の歴史的先行論文として `reports/theme_A_g_factor.md` の §1 (動機) or §6 (論文化見通し) に追記推奨。

**Claude Code へのリマインド:** `references/references.md` 末尾に「### arXiv 外 OA 追加（2026-05-23 ユーザー提供）」セクションを作って 4 本を追記してください（patrol 1425 / 1435 で詳細フォーマット提示済み）。

## 4. Production rules チェック (PRODUCTION_RULES.md §8)

| 項目 | 結果 |
|---|---|
| 既存 production bundle | 2 件（`theme_A_g_factor/2026-05-23_31374dc`, `phase_1.5_optical/2026-05-23_31374dc`） |
| MANIFEST.json 必須 8 フィールド | 両方とも 21 keys（theme/git_commit/git_dirty/inputs/outputs/key_numbers/software/references 完備）✅ |
| `git_dirty: true` の bundle | なし ✅ |
| `convergence/` ディレクトリ | 両方存在 ✅ |
| Theme F 関連 production run | まだなし（F5 でこれから） |
| `cowork/reports/` の Theme F 数値引用 | なし ✅ |

**違反ゼロ。** F5 で Theme F の最初の Production bundle が生まれる予定。

## 5. テスト状況

`__pycache__`/`.pytest_cache` を全消去後にクリーン再実行:

```
tests/ -k shift  →  20 passed, 205 deselected in 35.56s
```

内訳: `test_shift_current.py` 7 個（うち F5 で +2: `test_polar_kashikar_reduces_to_base_at_zero`, `test_polar_kashikar_shift_current_symmetry`） + `test_shift_current_rice_mele.py` 13 個（F4-3 sign anchor 群）。**回帰ゼロ**。

## 6. 未着手タスク（リマインド、3 連続）

**Cowork 1410 directive: D ドライブからの古典原典コピー（15 ファイル）**
- 1725 patrol でも未着手とリマインド済み → 今回も未着手
- 優先度: 中（Theme A・G の引用強化）
- Claude Code は F4-2 → polish → F5 ビルダーと連続で集中していたため自然
- F5 Production 実行待ち時間（k グリッド大きいので数十分〜）で並行作業として消化可能

無理に催促はしませんが、**F5 Production 実行 → 待ち時間に classic コピー**の順がスムーズです。

## 7. ユーザーへの通知判断

| 項目 | 通知要否 |
|---|---|
| 物理判断に迷い | なし（F5 builder は教科書的） |
| 新規 PDF 必要性 | なし（Boyer-Richard 2016 で task #18 重要部分解消、Hughes-Sipe で task #26 代替確保） |
| フェーズ移行判断 | なし（F4 → F5 は既決定パス） |
| 本番計算ルール大違反 | なし |

**通知不要。** Cowork ↔ Claude Code 内で完結。F5 Production 完了時にまとめて報告予定（patrol 1725 と同方針）。

---

## 巡回結果 (2026-05-23 17:40 JST)
- 確認したファイル数: 5（progress 4 + 新規 commit 1）
- レビュー依頼: **暗黙あり**（commit `9eeff23` は self-documenting） → §2 で **APPROVE**
- BLOCKED: なし
- 最新コミット: `9eeff23` F5 polar Kashikar-13 builder (43 秒前)
- テスト状況: shift_current 系 20 passed（F5 新規 2 含む）/ 回帰ゼロ
- 進捗判定: **加速・健全** — F4 完了 → F5 ビルダー実装 → 9 材料 Production スキャン待機
- 本番計算ルール違反: なし（F5 はまだ exploratory phase）
- ユーザーへの通知: なし
- 未着手リマインド: 1410 directive (D ドライブ classic 15 ファイルコピー、3 連続未着手・低中優先度)
- 次の patrol で見たいもの: F5 design.md（n_kpts ≥ 32, prefactor 規約, MANIFEST.references リスト）または F5 Production bundle
