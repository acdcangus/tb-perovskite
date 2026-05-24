# requirements — code-quality findings R4-STD（標準6観点レビュー由来）

**発行元:** PI「通常のきじゅんでレビューして」→ Cowork 標準6観点レビュー `cowork/progress/2026-05-24_1445_review_standard6.md`
**日付:** 2026-05-24

## 背景
PI レビュープロトコル（standing rule 1200）の標準6観点で Cowork が **総合合格**判定。
新規は code-quality minor 3 件（R4-STD-1〜3）のみ。物理・数値・テスト・本番計算ルールは違反ゼロ。

## 今回の作業対象（要求）
| ID | 内容 | 本サイクルで実施? |
|---|---|---|
| R4-STD-2 | `HBAR2_OVER_M0 = 7.619964` が exciton/optical/velocity/g_factor の4箇所で重複 → `_constants.py` に一元化（DRY） | **実施** |
| R4-STD-3 | `g_factor.py` 公開関数 docstring に式番号 anchor（`g_factor_kp` は既出 → `compute_g_factor` に Roth-Lax-Zwerdling 1959 anchor 追加） | **実施** |
| R4-STD-1 | `shift_current.py` 内部 helper 17 関数の型ヒント追加 | **deferred**（Cowork 推奨 (b)。各関数の戻り値型を未検証で付けると新たな不正確記述になるため、後続コード整備でまとめて慎重に。本 steering で追跡） |

## 受け入れ条件
- 定数値は **不変**（7.619964）→ 数値結果・Production に影響ゼロ。
- 全公開名（`exciton.HBAR2_OVER_M0`, `g_factor.C_HBAR2_OVER_M0`）は維持（test_exciton.py / scripts/plot_ge_universality.py が参照）。
- **既存 231 テスト全通過**を確認。
- docstring 追加は in-repo の出典（モジュール docstring 記載の Roth-Lax-Zwerdling 1959）に限定（ハルシネーション禁止）。
