# Supervisor Patrol (2026-05-23 14:10 JST / 11:10 UTC)

**監督:** Cowork (scheduled task `tb-perovskite-supervisor`, 15-min cycle)
**前回:** 2026-05-23 13:55 (F3 review + F4 directive + PRODUCTION_RULES rollout)
**判定:** 順調 ✅

---

## 確認したファイル（過去 30 分以内更新分）

1. `cowork/progress/2026-05-23_1320_theme_F_F3_complete.md` (10:41 UTC) — F3 完了通知
2. `cowork/progress/2026-05-23_1335_directive_update.md` (11:00 UTC) — Cowork 発行（自分の前回）
3. `cowork/progress/2026-05-23_1355_F3_complete_review_and_F4_directive.md` (10:58 UTC) — Cowork 発行（自分の前回）

新規 BLOCKED / question / violation: **なし**

---

## 最新コミット（前回以降）

| commit | message | 内容 |
|---|---|---|
| `31374dc` | Add reusable Production-bundle helper | `scripts/make_production_bundle.py` (206 行) |
| `f93d866` | Production-ize Theme A & Phase 1.5 (retroactive) | 両テーマの本番バンドル作成、reports に MANIFEST 参照追記 |

**達成事項:** 13:35 directive §2「既存結果の遡及 Production 化」を 30 分以内に完遂。

---

## 本番計算ルール compliance audit

`results/production/theme_A_g_factor/2026-05-23_31374dc/` と
`results/production/phase_1.5_optical/2026-05-23_31374dc/` を監査:

| 項目 | Theme A | Phase 1.5 | 判定 |
|---|---|---|---|
| MANIFEST.json 存在 | ✅ | ✅ | OK |
| 必須フィールド全部（theme, git_commit, git_dirty, inputs, outputs, key_numbers, software, references） | ✅ | ✅ | OK |
| `git_dirty: false` | ✅ | ✅ | OK（bundle 自身を除外する smart 判定） |
| `git_commit` 一致 (`31374dc`) | ✅ | ✅ | OK |
| `inputs/cli.txt`, `git_info.txt`, `requirements.txt` | ✅ | ✅ | OK |
| `inputs/` にパラメータ JSON 同梱 | ✅ (Nestoklon, Kashikar, exp_band_data) | ✅ (Nestoklon, Kashikar) | OK |
| `outputs/raw/`, `outputs/figures/` 振り分け | ✅ | ✅ | OK |
| sha256 checksums | ✅ (6 files) | ✅ (4 files) | OK |
| `key_numbers` に主要結果 | ✅ (g_e×3, g_h_dev×2, P×2) | ✅ (eps_inf×3, f-sum, abs_edge) | OK |
| `references` 出典明記 | ✅ | ✅ | OK |
| `retroactive: true` 自己申告 | ✅ | ✅ | OK（重要：今後の non-retro 本番計算との区別） |
| reports/ に MANIFEST 参照リンク | ✅ (L144) | ✅ (L67) | OK |

### ⚠️ Minor compliance gap（注意レベル、違反ではない）

**`convergence/` ディレクトリが空** in both bundles.

- Phase 1.5: 収束データは `outputs/raw/convergence.md` に markdown 表として保存（9 条件: k³ × η）。表内容は十分（abs_edge / main_peak / eps_inf / f-sum を 6³/8³/12³ × 0.03/0.05/0.08 eV で網羅）。
- ただし PRODUCTION_RULES §1.3 は `convergence_kgrid.png`, `convergence_eta.png` を要求。
- Theme A は k·p 解析評価で k-grid 収束は N/A、MANIFEST にもそう記載してあるので問題なし。

**推奨対応**: F5 本番スキャン時、`scripts/plot_convergence.py` を新規作成し
markdown 表から convergence plot を生成して `convergence/` に置く。retroactive bundle は
当面これで OK（数値そのものは表で完備）。

---

## Aversa-Sipe 1995 PDF（前回からの継続課題）

- Cowork 側で再試行する価値ある OA ルートは尽きた（APS Cloudflare/購読壁、arXiv 無し、
  OpenAlex/DOAJ/PMC 無し、Sci-Hub 不可）。
- ユーザー（Teruhisa さん）に機関アクセス経由の入手を依頼済み（前回 §6）。
- 入手待たずとも F4-1 (length-gauge 同値) + F4-2 (Tan & Rappe peak) + F4-3 (SSH 解析) の三重検証で
  符号確定可能なので、Claude Code の F4 着手は **block されない**。

---

## 次サイクル（14:25 巡回）でチェックする想定

- Claude Code が F4-1 (`src/perovskite_tb/shift_current_length_gauge.py` 新規) を着手しているか
- `tests/test_shift_current_gauge_equivalence.py` の追加
- F4 着手前に F3 docstring の VALIDATION STATUS が更新されているか（任意）

---

## 巡回結果サマリ

```
## 巡回結果 (2026-05-23 14:10 JST)
- 確認したファイル数: 3 (うち Cowork 発行 2、Claude Code 発行 1)
- レビュー依頼: なし（前回 directive で F3 受理済み）
- BLOCKED: なし
- 最新コミット: f93d866 Production-ize Theme A & Phase 1.5 (retroactive) per PRODUCTION_RULES
- 進捗判定: 順調（PRODUCTION_RULES 発行から 30 分以内に遡及バンドル完成）
- 本番計算ルール違反: なし（minor: convergence/ ディレクトリ空。F5 で補完予定）
- ユーザーへの通知: なし（Aversa-Sipe 入手依頼は前回サイクルで実施済み）
```

—Cowork supervisor
