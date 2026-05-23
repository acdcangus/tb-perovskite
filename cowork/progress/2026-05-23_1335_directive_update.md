# Directive Update: 本番計算ルール発行 + Theme F F3 レビュー応答

**発行:** Cowork, 2026-05-23 13:35
**契機:** (a) ユーザーから「本番計算は刻みなどしっかり収束、計算データ全保存、入力ファイル保存」のルール化要望、(b) Theme F F3 完了通知（2026-05-23_1320）への応答
**優先度:** 高（本番計算ルールは今後の全テーマに適用）

---

## 1. 本番計算ルール（PRODUCTION_RULES.md）の発行

**新規ファイル:** `cowork/PRODUCTION_RULES.md` — 本リポで実行する計算のうち、論文掲載・公開・最終報告書に使うものに適用される運用ルール

### 要点（必ず一読してから次のタスクに進んでください）

1. **計算は明示的に 2 モード:**
   - **Exploratory**: 試行錯誤、粗い解像度、データ消して良い
   - **Production**: 論文・公開・最終報告書用、全データ保存、再現可能

2. **Production の必須要件:**
   - **収束確認 3 段階**（k グリッド、smearing η、ω 分解能を各 3 ステップ）
   - **全データ保存** in `results/production/<theme>/<date>_<commitHash>/`（生数値・収束プロット・ログ・乱数シード）
   - **入力ファイル一式**（config, parameters, env.yml, git_info.txt, cli.txt, seeds.json）
   - **MANIFEST.json**（中心索引、テンプレ §4）
   - **uncommitted modification なし**で実行
   - **削除禁止**（古い結果は `_archived/` に移動のみ）

3. **`reports/` で引用する数値は MANIFEST.json への参照付き**

4. **supervisor の自動チェック:** 違反検出時に `cowork/progress/.../production_violation.md` で警告

---

## 2. 既存結果の遡及 Production 化

以下を **Theme F F4 着手前**に実施してください（短時間で済むはず）:

### Theme A の Production 化
- `results/g_factors/` の主要結果（g_e/g_h スキャン、TB-derived P、A7）を
  `results/production/theme_A_g_factor/2026-05-23_<hash>/` にコピー
- `MANIFEST.json` 作成（key_numbers に CsPbI3/CsSnI3/CsGeI3 の g_e, g_h を記載）
- 入力 JSON、cli.txt、git_info.txt、env.yml を `inputs/` に
- 報告書 `cowork/reports/theme_A_g_factor.md` に MANIFEST 参照を追記

### Phase 1.5（光学）の Production 化
- `results/optical/` の 9 材料スキャン結果を
  `results/production/phase_1.5_optical/2026-05-23_<hash>/` にコピー
- 収束プロット（既に η・k 収束テストはやっているはず）を `convergence/` に整理
- MANIFEST.json、inputs/ 一式

### 注意
- 既に走った計算を **再実行する必要は基本的に無い**（コピー + メタデータ整備）
- ただし、もし η や k グリッドの収束確認が **3 段階揃ってない**なら、足りないステップを追加実行してください（これは Production の必須要件）

---

## 3. Theme F F3 レビュー応答

### 主要評価 ✅

Cowork 推奨 (B) sum-over-states を実装し、**Kramers 縮退問題を解決**、**δ=0 で σ ≈ 4.6e-15（機械精度 vanishing）** を達成したのは見事です。これは中心対称 → shift current 消失という対称性原理の厳密な数値再現で、実装の構造的正しさを強力に裏付けます。

5 テスト通過、線形性 δ→σ も確認済み。F3 は完了として OK。

### ⚠️ Aversa-Sipe 1995 の符号・prefactor

正直な申し送り（"絶対符号と prefactor は primary source で未検証、δ=0 vanishing で構造検証のみ"）は **完璧な対応**です。これがハルシネーション防止のあるべき姿。

**Cowork の継続調査タスク（task #26）:**
- Aversa-Sipe 1995 (PRB 52, 14636) を入手試行
  - arXiv 探索（無いことを再確認）
  - APS の OA preprint server
  - 著者 ResearchGate / 機関リポジトリ
  - Tan & Rappe 2016 の式と突き合わせて間接確認
- 入手できなければ **Sipe-Shkrebtii 2000 (PRB 61, 5337)** で代替（arXiv:cond-mat/9709185 が前駆論文）
- 解決まで Theme F の絶対値・符号は「相対単位、符号 TBD」で進める

F4 で論文値との照合に進む際、**絶対符号が確定するまで論文の主結果は「相対比較」のみで論じる**方針が安全です。

### 性能の件

sum-over-states の Python ループで shift_current テストが ~100s — 正しさ優先で現状維持で OK。F5（9 材料 × δ スキャン）の前にベクトル化最適化を検討してください。numpy.einsum での書き直しで 10-100 倍速くなる見込み。

---

## 4. 次のタスク（優先順）

1. **PRODUCTION_RULES.md を読む**（必須、5 分）
2. **既存 Theme A 結果の遡及 Production 化**（30-60 分）
3. **既存 Phase 1.5 光学結果の遡及 Production 化**（30-60 分）
4. **F4: Tan & Rappe 2016 MAPbI₃ shift current ピーク照合**（光学+TB のクロスチェック）
   - ただし MAPbI₃ は本リポにパラメータがないため、まず Pb 立方相 CsBX₃ で MAPbI₃ 同様の δ で σ_zzz を出して、Tan & Rappe Fig.? のピーク位置・形状を qualitative に比較
   - **Production モード**で実施（収束確認 + MANIFEST.json）
5. **F5: 9 材料 × δ スキャン**（Production モード）
   - ベクトル化最適化を先に
   - 9 材料 × δ ∈ {0.05, 0.10, 0.15, 0.20} で σ_zzz(ω) を計算
   - 鉛フリー（Sn/Ge）で σ が大きい組成があるか
6. **F6: Theme F 報告書 draft**（reports/theme_F_shift_current.md）

---

## 5. Theme F の物理的注意点（先回り指示）

shift current は時間反転対称性 (TRS) と空間反転対称性の両方に依存：

- **中心対称材料（CsBX₃ 無歪み）**: shift current = 0（既に F3 で確認）
- **空間反転を破る歪み**: σ ≠ 0 になる
- **TRS が保たれる限り**、shift current は実数（既に確認済み）
- **磁性が入る**: TRS 破れ → 別の現象（injection current 等）も発生、本研究では考慮外

F5 で δ を入れる方法は **uniaxial strain** が物理的に分かりやすい：
- a 軸方向に圧縮、b/c 軸変えず
- 八面体傾斜（octahedral tilting）も別の歪みパターン
- Tan & Rappe 2016 は内部歪み（Pb の中心 off-centering）を使っている

**まずは uniaxial strain で実装**、後で octahedral tilting も追加するか判断（F5 内部判断で OK）。

---

## 6. その他

- supervisor タスクが PRODUCTION_RULES.md に基づく違反チェックを開始しています。`MANIFEST.json` 欠落や `git_dirty: true` Production などがあれば警告がきます
- novelty-watch (月・木 9:00) は次回 5/25 月曜
- 質問・行き詰まりは `cowork/progress/` に書いてください

引き続きお願いします。素晴らしいペースです。
