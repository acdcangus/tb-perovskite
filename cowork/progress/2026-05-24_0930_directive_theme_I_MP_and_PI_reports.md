# Directive: Theme I option (C') 実行 + 完了 4 テーマの PI 向け解説報告書 — 2026-05-24 09:30 JST

**発行元:** Cowork (supervisor)
**発行先:** Claude Code
**優先度:** 中-高（PI からの新規指示 2 件）
**前回 directive:** `2026-05-24_0715_directive_theme_I_hybrid_and_license.md` 等
**背景:** Theme I は 09:25 の自走 closeout で option (D') 完了。今回 PI から (a) MP API キー提供、(b) PI 向け丁寧解説報告書の発注、の 2 件が入った。

---

## Part 1. Theme I option (C') — Materials Project DFPT ε_∞ で 9 材料の絶対 E_b マップを確定

### 1.1 背景（PI 指示の経緯）

- 09:15 の web research で「文献の bare ε_∞ ≠ Wannier-Mott が要する effective ε_eff」と判明し、絶対 9 材料 E_b マップは見送り（option D'）にした。
- PI がこれを受けて **Materials Project API キーを提供**（09:25 後の chat）。これにより、**単一手法（DFPT）の ε_∞ を 9 材料で consistent に取得**できるようになった（option C'）。
- C' でも依然「bare ε_∞ ≠ ε_eff」の限界は残るが、(a) **手法が一貫**しているため**相対トレンドの defensibility は最高**、(b) Pb 系は ε_eff に近い値（フォノン寄与小）になるので絶対値もある程度信頼できる、(c) Sn/Ge 系は **bare ε_∞ ベースの「上限的」E_b マップ**として明示すれば論文化可能。

### 1.2 キーファイル（gitignore 対象）

```
data/parameters/mp_api_key.json   # ← Cowork が今 patrol で配置
  → .gitignore に追加済み: data/parameters/mp_api_key.json, secrets/, *.api_key, .env
  → 必ず gitignore されていることを git check-ignore で確認してから作業開始
```

**セキュリティ要件（必須）:**
- API キーは **絶対に commit / log / MANIFEST.json / 報告書に書かない**
- ロード方法: `import json; key = json.load(open('data/parameters/mp_api_key.json'))['api_key']; os.environ['MP_API_KEY'] = key` の形に統一
- provenance は **'Materials Project DFPT, mp-<id>'** の文字列のみ MANIFEST/JSON に残す（キー本体は禁止）

### 1.3 実装ステップ

**C-1. MP API クライアント書き出し（`src/perovskite_tb/materials_project.py`）**
- `pymatgen.ext.matproj.MPRester` または `mp-api`（新 API）を使用
- 関数 `fetch_eps_inf_for_formula(formula: str, space_group: str = 'Pm-3m') -> dict`
  - 戻り値: `{'mp_id': ..., 'eps_inf_tensor': [[xx,xy,xz],...], 'eps_inf_scalar': trace/3, 'method': 'DFPT', 'source_url': ...}`
- 9 材料（CsBX₃, B∈{Ge,Sn,Pb}, X∈{Cl,Br,I}）を 1 秒 sleep 挟んで順次取得
- 立方相が無い材料（CsGeI₃ は rhombohedral 等）は `status: 'no_cubic_phase_in_MP'` として記録、推定値は使わない

**C-2. `eps_inf_external.json` 更新（option C' 版を追加）**
- 既存 entries は残し、新たに `materials.<formula>.eps_inf_MP_DFPT` フィールドを追加（既存の `eps_inf`/`status` と並列）
- MP から取れなかった材料は `null` + 明確な not-found 理由
- 新 `_KEY_FINDING_C` を追加: 「DFPT bare ε_∞ は ε_eff より小さい（フォノン寄与なし）が、9 材料 single-method で相対トレンドは defensible」

**C-3. `scan_theme_I_binding_energy.py` 再実行（C' プロファイル）**
- 入力に `eps_inf_MP_DFPT` を選ぶオプションを追加（既存 `eps_inf` 経路と切替可能に）
- Production 実行: `python scripts/scan_theme_I_binding_energy.py --profile MP_DFPT --production`
- 出力: `results/production/theme_I_exciton_MP_DFPT/2026-05-24_<hash>/`
  - MANIFEST.json（git_dirty:false 必須、8 フィールド完備）
  - key_numbers に 9 材料の `mu, eps_inf_MP_DFPT, E_b_meV, mp_id, mp_source_url` を入れる
  - **API キーは絶対に MANIFEST に入れない**

**C-4. `theme_I_exciton.md` 報告書を § 3.3「option C' MP-DFPT 9 材料 E_b マップ」として追記**
- 旧 §3.1（μ map）/ §3.2（web research finding）はそのまま残す
- §3.3 で C' 結果と「bare ε_∞ 由来 → 絶対 E_b の上限解釈」を明記
- CsPbI₃ で E_b(MP-DFPT) と E_b(exp~15-20 meV) を比較し、Pb 系の overestimate 度合いを定量化

**C-5. テスト追加（`tests/test_materials_project.py`, optional）**
- MP API モック or オフライン JSON で `fetch_eps_inf_for_formula` の戻り値スキーマ確認
- 実 API 呼び出しテストは `pytest.mark.network` で skip 可能に

### 1.4 受け入れ条件

- [ ] `data/parameters/mp_api_key.json` が `git check-ignore` で除外確認
- [ ] `git log --all` で API キー文字列 `<REDACTED_MP_API_KEY>` が **commit に一度も入っていない**ことを `git log --all -S '<REDACTED>' --oneline` で確認
- [ ] MP API で 9 材料中**最低 6 材料**の DFPT ε_∞ 取得（無いものは not-found 明記）
- [ ] Production bundle `theme_I_exciton_MP_DFPT/` 作成（git_dirty:false, MANIFEST 完備, 収束プロット）
- [ ] 報告書 §3.3 追記、option (C') の結果と限界を **defensible に**記述（捏造ゼロ、出典明記）
- [ ] 既存 228 テスト全通過維持

---

## Part 2. PI 向け丁寧解説報告書（PI 新規指示 09:27）

### 2.1 PI からの指示（原文）

> あるていどやり切った研究については、PI がわかるレベル（この分野はそこまでしらない）に丁寧に丁寧に解説した報告をあげてください。目的、なぜこれをやらないといけないのか、結果、手順解釈など

### 2.2 対象テーマ（「あるていどやり切った」=完了 4 テーマ）

| テーマ | 状態 | 既存報告書 |
|---|---|---|
| Theme A: Landé g 因子 9 材料マップ | ✅ Production | `cowork/reports/theme_A_g_factor.md`（155行、専門家向け） |
| Phase 1.5 (A5): 光学応答 ε(ω) | ✅ Production | `cowork/reports/theme_A5_optical.md`（71行、専門家向け） |
| Theme F: shift current / BPVE | ✅ Production | `cowork/reports/theme_F_shift_current.md`（131行、専門家向け） |
| Theme I: 有効質量 + 励起子 E_b | ✅ Production (D') / +今回 (C') | `cowork/reports/theme_I_exciton.md`（82行、専門家向け） |

### 2.3 何が足りないか（PI 視点）

既存の `cowork/reports/theme_*.md` はいずれも「実装済み・専門家がレビューする」ことを前提に書かれており、PI（分野非専門）には:
- **なぜこの量を計算する価値があるのか** が抜けている（背景が薄い）
- **物理量の意味**（g 因子、shift current、励起子結合エネルギー、有効質量）が一言で説明されていない
- **デバイス応用（太陽電池/LED/光検出器）との結びつき** が明示されていない
- **論文化したときに何が新しいと言えるのか** が技術寄りの記述になっている
- **数式が密**で、「これは何を計算しているのか」の物理直観が薄い

### 2.4 成果物（必須）

各テーマについて `cowork/reports/PI_explained_<theme>.md` を新規作成（既存 `theme_*.md` は技術仕様として残す）。

**必須セクション構成（全テーマ共通テンプレート）:**

```
# PI 向け解説: <テーマ名>

## 0. 30 秒サマリ（テーマ全体）
- 何を計算したか（1 文）
- 何が新しいか（1 文）
- デバイス応用との繋がり（1 文）

## 1. 物理的背景（なぜこの量が重要か）
### 1.1 計算対象の物理量とは何か
- 中学物理〜学部初年度レベルから説明（例: g 因子 = 電子スピンが磁場でどれだけエネルギーシフトするかの係数）
- 日常的なアナロジー、可能なら絵で説明
### 1.2 なぜハライドペロブスカイトでこれを調べる価値があるか
- 太陽電池・LED・光検出器・量子情報など、応用先を具体的に
- 既存材料（GaAs, Si）との比較
### 1.3 なぜ「TB（タイトバインディング）」なのか
- 第一原理計算（DFT）との違い（速い・パラメータ化済み・大規模可能）
- 経験的 TB の限界（パラメータ依存）も honest に

## 2. 何を計算したか（手順、図解付き）
### 2.1 入力（材料、パラメータ、近似）
### 2.2 計算手順（フローチャートで）
- Mermaid 図で「入力 → ハミルトニアン → 何々を解く → 出力」を可視化
### 2.3 計算規模（材料数・k 点数・実行時間など）

## 3. 結果（数値 + 物理的解釈）
### 3.1 主結果の表（9 材料 × 主要量）
- key_numbers は **Production MANIFEST.json から直接引用**（PRODUCTION_RULES.md §8）
### 3.2 結果の物理的読み解き
- 「Cl→Br→I で〜になるのは、ハロゲン軌道が〜だから」のように **化学的・物理的直観で説明**
- 「Sn 系で〜なのは、Pb との違いが〜」のように比較
### 3.3 既知文献・実験値との比較
- 表で「本研究値 vs 文献値 vs 実験値」を並べる
- どこまで一致して、どこから外れるかを正直に

## 4. 何が新しいか（論文化視点）
- 既存研究のレビュー（2-3 件）と本研究の差別化点
- novelty assessment との対応（`cowork/novelty_assessment.md` 参照）

## 5. 限界と今後の課題
- TB の構造的限界（Blount 1962 の TB 不完全性など）を honest に
- 改善の道筋（DFT-Wannier 化、励起子効果、フォノン寄与など）

## 6. 用語集（PI が知らないかもしれない単語）
- バンドギャップ、有効質量、Berry connection、Kubo-Greenwood 公式、Wannier-Mott、Roth-Lax、Slater-Koster、…
- 各語を 1-2 文で

## 7. 出典
- 主要参考文献を 5-10 件、なぜ重要かのコメント付きで
- 本研究の Production bundle へのパス
```

### 2.5 書き方ガイド（重要）

- **数式を多用しない**: 必要最小限。意味を日本語で先に書き、数式は補足として最後に置く。
- **専門用語を初出で必ず定義**: 「g 因子（電子スピンが磁場に対して感じる結合の強さの係数。自由電子で 2.0023）」のように。
- **比喩・アナロジーを積極的に**: 「励起子 = 電子と正孔が水素原子のようにペアを組んだ状態」「shift current = 光が当たった瞬間に、波動関数の重心が空間的にズレることで流れる電流」など。
- **図を増やす**: Mermaid 図（手順）、表（材料×物性）、可能なら ASCII プロット概略。
- **「なぜ重要か」を各セクションの冒頭で 1 文**: 読み飛ばし可能な構成に。
- **PRODUCTION_RULES 準拠**: 数値はすべて Production MANIFEST.json からの引用、引用元パスを明記。
- **honesty 維持**: 限界・不確かさ・未確定を明確に。Cowork 既存 directive 群（特に `references/CLAUDE.md`「ハルシネーション防止」）に従う。

### 2.6 推奨作業順序

1. Theme A（g 因子）— 一番完成度高く、説明も書きやすい（4 時間目安）
2. Theme F（shift current）— 物理が面白く、PI 興味度高い見込み（5 時間目安）
3. Phase 1.5（光学）— A の派生で短く済む（3 時間目安）
4. Theme I（有効質量 + 励起子）— **Part 1 の C' 結果を反映してから書く**（4 時間目安、C' 完了待ち）

合計目安 16 時間（並列化・素材流用で短縮可能）。

### 2.7 受け入れ条件

- [ ] `cowork/reports/PI_explained_theme_A.md` 作成、必須 8 セクション網羅
- [ ] `cowork/reports/PI_explained_phase_1.5_optical.md` 作成
- [ ] `cowork/reports/PI_explained_theme_F.md` 作成
- [ ] `cowork/reports/PI_explained_theme_I.md` 作成（C' 結果含む）
- [ ] 各報告書冒頭に「30 秒サマリ」あり
- [ ] 数値はすべて Production MANIFEST.json 引用、出典明記
- [ ] 限界・honest 記述あり
- [ ] 既存技術報告書（`theme_*.md`）は削除せず併存（技術仕様として価値）

---

## Part 3. 全体スケジュールの示唆

- **今夜の自走**: Part 1（C' 実行、~3 時間）→ Part 2（PI 報告書 4 本、~16 時間並走）
- **支配的なボトルネック**: MP API rate limit、Production scan の収束確認
- **5 分巡回ループ**継続、Cowork 巡回は 15 分 cycle で進捗確認

## Part 4. 質問・blocker があれば

- `cowork/progress/YYYY-MM-DD_HHMM_question.md` または `BLOCKED_*.md` を作成
- Cowork は次回巡回（15 分以内）で対応

---

**Cowork 署名:** supervisor patrol 2026-05-24 09:25
**Claude Code 確認後:** `cowork/progress/YYYY-MM-DD_HHMM_directive_received.md` で簡単に受領確認をお願いします。
