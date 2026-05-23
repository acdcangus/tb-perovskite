# Supervisor patrol — 2026-05-23 17:25 JST (14:22 UTC)

**監督:** Cowork (scheduled task `tb-perovskite-supervisor`, 15-min cycle)
**前回:** 1710 (14:13 UTC) — F4-3 fix commit `ffe2940` を APPROVE
**今回判定:** ✅ **F4-2 / polish 両方とも APPROVE — F5 (Production 9 材料 × δ スキャン) 着手 OK**

---

## 1. 直近 30 分の進捗確認

| 時刻 (UTC) | ファイル | 内容 | 判定 |
|---|---|---|---|
| 14:06 | `2026-05-23_1510_F4-3_fix_committed_review_request.md` | F4-3 fix のレビュー依頼 | 前回 patrol 1710 で APPROVE 済み |
| 14:13 | `2026-05-23_1535_F4-2_complete_sign_confirmed.md` | F4-2 完了報告（多バンド符号確定） | 本パトロールで **APPROVE** |
| 14:13 | `2026-05-23_1710_code_review.md` | (Cowork 側 1710 patrol 出力) | 自己発行 |
| 14:14 | (commit `69f5c63`) F4-2 polar 符号反転テスト追加 | 4 ファイル変更 | **APPROVE** |
| 14:15 | (commit `7dc525e`) review §7 polish 反映 | wvc/wcv コメント + defensive guard | **APPROVE** |
| 14:19 | `2026-05-23_1410_directive_update.md` | (Cowork 側) D ドライブから古典原典コピー依頼 | Claude Code 未着手（後述 §4） |

最新コミット: `7dc525e` "shift_current: address review polish — wvc/wcv sign comment + defensive guard"。

## 2. F4-2 多バンド符号確認のレビュー

`tests/test_shift_current.py::test_polar_sign_reverses_under_displacement_flip` を `git show HEAD:` で読み、以下を確認:

```python
for delta in (-0.12, 0.12):
    Hp, dHp, d2Hp = sc.make_polar_nestoklon_builders(p, a, basis, polar_displacement_z=delta)
    out[delta] = sc.shift_current_zzz(Hp, dHp, a, 26, omega, n_kpts=4,
                                       smearing_eta=0.10, direction=2, d2Hdk_fn=d2Hp)
assert np.max(np.abs(out[-0.12] + out[0.12])) < 1e-9 * max(scale, 1.0)
```

**チェック項目:**

| # | 項目 | 結果 |
|---|---|---|
| 1 | 符号反転が機械精度で成立（[001] δ→−δ は空間反転） | ✅ tol = 1e-9 × scale |
| 2 | 多バンド (CsPbI₃ Nestoklon 26-band) → 2-band Rice-Mele では捕捉できない virtual sum の符号 bug を排除 | ✅ patrol 1655 §2.5 の懸念をカバー |
| 3 | scale > 1e-3（trivial vanishing でない） | ✅ assertion で保証 |
| 4 | Tan & Rappe 2016 Eq.14 の 3 則すべて | ✅ δ=0 消失 / 符号反転 / |δ| 増大（報告書 §2） |
| 5 | d2Hdk_fn を明示渡し（continuum form 誤用を排除） | ✅ |

**物理:** Tan & Rappe 2016 は 1D Rice-Mele を解析模型に採用しており、Fregoso D2 と同型なので F4-3 の closed-form anchor と整合。MAPbI₃ (DFT) vs CsPbI₃-polar (経験 TB) の絶対振幅は別ものだが、**対称則・スケーリングの定性照合**としては教科書例。報告書 §3 の「絶対振幅は F5 で Eq.(D12) prefactor を付与」も方針として正しい。

**F4 完了を承認**。符号 TBD はこれで完全解除（2-band closed form + 多バンド対称則の二重 anchor）。

## 3. Polish commit (`7dc525e`) のレビュー

私の 1710 review §7 の 3 提案のうち 1, 2 が反映済み:

| § | 提案 | 反映 |
|---|---|---|
| §7.1 | `wvc/wcv` の符号コメント | ✅ `# sign bookkeeping: wvc = E_v - E_c < 0 ...` |
| §7.2 | `d2Hdk_fn=None` のとき raise（`allow_continuum_form: bool = False` opt-out） | ✅ 実装通り。Docstring も「WRONG for tight-binding」→ raise に修正 |
| §7.3 | `shift_current_zzz_abelian_deprecated` 削除 | 未対応（非必須なので問題なし、F5 とは独立） |

**defensive guard の意義:** F3→F4 の歴史で「continuum 形 (w=0)」のまま runs を作ってしまった経緯があるので、API 上で再発を物理的にブロックするのは PRODUCTION_RULES と整合（exploratory bug の再侵入を未然に防ぐ）。`allow_continuum_form=True` の opt-out も regression test 用としては妥当な escape hatch。

**APPROVE**。

## 4. Production rules チェック (PRODUCTION_RULES.md §8)

| 項目 | 結果 |
|---|---|
| 既存 production bundle | 2 件（`theme_A_g_factor/2026-05-23_31374dc`, `phase_1.5_optical/2026-05-23_31374dc`） |
| MANIFEST.json 必須 8 フィールド | 両方とも揃い ✅（21 keys; theme/git_commit/git_dirty/inputs/outputs/key_numbers/software/references all present） |
| `git_dirty: true` で commit されている bundle | なし ✅ |
| `convergence/` ディレクトリ | 両方存在 ✅ |
| `cowork/reports/` で shift-current の数値引用 | なし ✅（F4 は exploratory 段階、未昇格） |

**違反ゼロ。** F4 exploratory で sign bug を発見し production 汚染を未然に防いだ運用パターンは継続。

## 5. 未着手タスク（リマインド）

**Cowork 1410 directive: D ドライブからの古典原典コピー**
- Kane 1957/1963、Vogl 1983、Luttinger 1955/56、Wannier 1937、Dresselhaus 1955、Ando 1982、Hjarmarson 1980 ほか合計 15 ファイル
- 優先度: 中（Theme A・G 論文化の引用強化用、F5 とは独立）
- Claude Code は F4 完了に集中していたため後回しでも問題なし。**F5 着手前 / F5 と並行のどちらでも OK**

このリマインドだけ。Claude Code 側で F5 着手前に 5 分で済むコピー作業として消化推奨。

## 6. 次タスク (F5) の事前確認

F4-2 完了報告 §5 で示された F5 プラン:
- 9 材料 × δ スキャン（Production モード）
- 絶対 prefactor `e³/ℏ⁴`（Fregoso Eq.(D12)）を付与
- k グリッド収束 3 段階 + η 3 段階 + ω 分解能 → PRODUCTION_RULES 準拠
- `results/production/theme_F_shift_current/<date>_<hash>/` に MANIFEST.json + inputs/
- 主問い: 鉛フリー（Sn/Ge）で σ が大きい組成があるか

**事前確認すべき点（F5 design.md に書いてほしい）:**

1. **`allow_continuum_form` は使わない**（defensive guard 通過のため d2Hdk_fn を必ず渡す）
2. **MANIFEST.references** に Fregoso 2017 PRB 96 075421 (式 D12, C2) + Tan & Rappe 2016 npj CM 2:16026 を明記
3. **収束プロット** を `convergence/sigma_vs_nkpts.png`, `convergence/sigma_vs_eta.png` に必ず出力
4. **inputs/** に Nestoklon SK パラメータ・polar δ 値・物質一覧 (9 種類) を JSON で保存
5. **k グリッド** shift current は遅収束なので n_kpts ≥ 32（できれば 48）から始める想定。F4 で使っていた 8/12/16 は exploratory レベル
6. **絶対値 vs 相対値** の併記方針（Blount 1962 由来の系統的過小は g因子・光学と同根、注釈を MANIFEST.notes に）

design.md 提出時に Cowork 側でレビューします。

---

## 巡回結果 (2026-05-23 17:25 JST)
- 確認したファイル数: 6 (直近 30 分: progress 3 + commit 3)
- レビュー依頼: **あり** (F4-2 完了 + polish) → 本ファイル §2-§3 で **両方 APPROVE**
- BLOCKED: なし
- 最新コミット: `7dc525e` shift_current polish (7 分前)
- テスト状況: 前回 patrol で 20 passed (shift_current 系) / 225 passed (全 suite, 回帰ゼロ) 再現確認済み
- 進捗判定: **加速・健全** — F4 完了、符号 2 重 anchor (closed-form + 対称則)、polish 完了、F5 着手準備中
- 本番計算ルール違反: なし
- ユーザーへの通知: **なし**（Cowork ↔ Claude Code 内で完結。F5 完了時にまとめて報告予定）
- 未着手リマインド: 1410 directive の古典原典コピー（中優先度、F5 と並行で OK）
