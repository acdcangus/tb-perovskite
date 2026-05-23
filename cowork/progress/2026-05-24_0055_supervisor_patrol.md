# Supervisor patrol — 2026-05-24 06:55 JST (21:53 UTC, 5/23)

**監督:** Cowork (scheduled task `tb-perovskite-supervisor`, 15-min cycle)
**前回:** 2026-05-24 0040 patrol — silent ~238 分・セッション中断確定・verify only
**今回判定:** 🟢 **セッション復帰確認** — BLOCKED close、Theme I exploratory 完了・PI 判断待ち

---

## 1. 復帰サイン（前回判定の覆し）

`2225_BLOCKED_session_stalled.md` 以降 7 連続 patrol で「silent 沈黙継続」判定だったが、
本 patrol（0055）で **Claude Code 側から 3 連続 commit を確認**:

| commit | UTC | 内容 |
|---|---|---|
| `9c21a18` | 21:45 | PI morning summary + recovery from session gap; track accumulated supervisor patrols/directives |
| `2a4fe38` | 21:49 | Theme I: Wannier-Mott exciton module (effective_mass + binding) + tests |
| `1a93de0` | 21:50 | cowork/progress: Theme I exciton exploratory — effective masses solid, E_b absolute needs PI judgment |

→ **silent ~253 分（4h13m）で復帰**。`PI_summary_2026-05-24.md`（57 行）と Theme I exploratory ノートを同セッション内で消化。
2125 nudge の Option A（PI summary）と Option B（Theme I）を **両方着手**、判断指針通りの順序。

**BLOCKED 状態は本 patrol をもって close**。

## 2. 新規ファイル（過去 30 分）

- `cowork/PI_summary_2026-05-24.md`（57 行、PI 起床用 1 枚物・付記まで完備）
- `src/perovskite_tb/exciton.py`（76 行、Wannier-Mott Eb 一式）
- `tests/test_exciton.py`（1895 B、3 ケース通過記載）
- `cowork/progress/2026-05-24_0050_theme_I_exciton_exploratory.md`（43 行、9 材料 E_b 一覧 + PI 判断依頼）
- `cowork/COWORK_CLAUDECODE_PATTERN.md` 編集中（uncommitted、4h gap 振り返り + 3 層 wake-up 仕組みの追記）

cowork/progress に新たな `BLOCKED_*`, `*_review_request.md`, `*_question.md` は無し。0050 ノートは review 依頼ではなく **PI 判断依頼**。

## 3. 軽量コードレビュー（exciton.py / 0050 exploratory ノート）

レビュー依頼が出ているわけではないので「補助所見」レベル。

**物理的に妥当な点（go）**
- `effective_mass(...)` は R 点 (π/a,π/a,π/a)・3 方向中央差分。CsBX₃ 立方相の直接ギャップ edge として正しい
  選択（Theme A の k·p 抽出と同じ枠組み）。h = dk·(2π/a) で k-スケール無次元化済み、Cartesian step に変換。
- `m*/m0 = (ℏ²/m0) / (d²E/dk²)` で `HBAR2_OVER_M0 = 7.619964 eV·Å²`（`velocity.py` と同一値再利用）→ 単位一貫。
- `reduced_mass` は `1/(1/|m_e|+1/|m_h|)`、`wannier_mott_binding_eV` は `(μ/m0)/eps_r²·Ry`、Ry=13.605693 eV。
  正しい hydrogenic 形。
- Docstring に **CAVEAT（ε_∞ 上限の物理）と Blount 限界**を明記、Yang 2017 / Tanaka 2003 / Cho 2019 引用済み
  → CLAUDE.md「docstring 出典・限界記載」遵守。
- 結果トレンドは物理に整合（Cl→Br→I で E_b 減、Sn-I が最小、CsPbI₃ の m_e≈0.11 が文献整合）。

**注意点（要対応 / 0050 ノート §3 と同内容を確認）**
- 絶対 E_b は実験を **~3-4× 過大**（CsPbI₃ 67 meV vs 実験 ~15-20 meV）。0050 ノートが既に正しく自己診断:
  (i) Wannier-Mott の正しい遮蔽は ε_∞ と ε_static の中間（フォノン寄与）。ε_∞ 単独は上限。
  (ii) 本実装の ε_∞ は **TB-optical KK の eps_real[0]**、これは Phase 1.5 既知の **f-sum=0.21（Blount 5× 過小）**
       を継承 → ε_imag 過小 → ε_∞ 過小 → E_b 過大、特に **広 gap Cl で破綻**（CsPbCl₃ ε_∞=1.45 / E_b=743 meV
       は非物理）。
  → **Production 化前停止は正しい判断**。

**符号規約**
- `effective_mass` は符号保持（CB は +、VB は −）。`reduced_mass` で `abs` を取るので、上位は |m_h| を使う。OK。

**検証十分性（exploratory 段階）**
- 合成放物線で m* 厳密回復（unit test ①）。
- CsPbI₃ で m_e>0 / m_h<0、物理的順位（unit test ②）。
- 公式の算術（unit test ③）。
- → exploratory としては妥当。Production 化時には収束テスト（n_kpts 段階、dk 段階、direction 平均の異方性）
  が PRODUCTION_RULES §1 で必要。

**コード品質**
- 型ヒント完備、PEP 8 準拠、マジックナンバー回避（定数は名前付き）、docstring に式・出典・限界。OK。

## 4. Production bundle 健全性（30 連続 patrol で clean）

```
phase_1.5_optical/2026-05-23_31374dc/MANIFEST.json:     git_commit=31374dc914, dirty=False, missing=[]
theme_A_g_factor/2026-05-23_31374dc/MANIFEST.json:      git_commit=31374dc914, dirty=False, missing=[]
theme_F_shift_current/2026-05-23_ef575e3/MANIFEST.json: git_commit=ef575e3cad, dirty=False, missing=[]
```

- 8 必須フィールド完備、`git_dirty:false`、`convergence/` 完備、3 本とも継続して健全
- **PRODUCTION_RULES.md §8 違反は引き続きゼロ（30 連続 patrol）**

Theme I は **まだ Production 化されていない（保留中）**ので bundle は 3 本のまま。これは 0050 ノート §4 の
方針（非物理な Cl ε_∞ を bundle に混ぜない）と一貫していて適切。

## 5. PI 判断要請（最重要・本 patrol の主目的）

`0050_theme_I_exciton_exploratory.md` §3 で **3 択の PI 判断**を要求中:

> (a) 有効質量マップだけ Production 化（信頼可・publishable）
> (b) E_b は相対トレンドのみ報告（絶対値は出さず順位だけ）
> (c) Production E_b には **実験/DFT の ε_∞ を外部入力**として使う（TB-optical KK の Blount 過小を回避）

**Cowork supervisor の所見（指示ではなく観測）:**
- (a)+(c) のハイブリッドが情報量・科学的健全性ともに最大: 有効質量マップは TB 由来で完結、E_b は外部
  ε_∞（実験 or DFT-RPA）を入力にして Production 化、出典を MANIFEST.references に明記。
  → ε_∞ 由来の系統誤差を Theme I 報告書から切り離せる（"TB が出すのは μ、ε_∞ は外部入力" と明確化）。
- (a) のみは最安全だが情報量が下がる。(b) のみは絶対値を捨てる正しさはあるが、Cl で物理破綻が残り続け
  bundle に乗せにくい。
- いずれにせよ **Production 化前に PI 判断必須**（PI 不在で勝手に Production 化しないのは正しい）。

→ **新規 directive は発行しない**。PI 起床判断を待つ。

## 6. 本 patrol のアクション

- ✅ `2225_BLOCKED_session_stalled.md` を **close**（本 patrol 結果として明示）
- ✅ Production bundle 3 本の verify は継続実施・clean
- ✅ Theme I exploratory コードを軽量レビュー（補助所見、本 §3）
- ✅ PI 判断要請を本 patrol で PI に通知（scheduled task return で）
- ❌ 新規 directive 発行は **しない**（PI 判断要素を含むため、Cowork が勝手に決めない）

## 7. 次回 patrol (0110) での扱い

- **PI 判断到着** → 該当 directive を即発行（(a)/(b)/(c) または (a)+(c) ハイブリッドのいずれか）
- **PI 不在継続 + Claude Code が自走（例: 有効質量マップだけ先 Production 化）** → patrol で verify、Production
  bundle 健全性チェック追加
- **沈黙再発（>30 分新規 commit/progress なし）** → verify only モードに復帰、ただし 4h gap 経験を踏まえて
  30 分時点で軽い ping を 1 回だけ出す（圧は最弱・無視可）

---

## 巡回結果 (2026-05-24 06:55 JST / 21:53 UTC 5/23)
- 確認したファイル数: 8（0050 exploratory ノート、PI_summary、exciton.py、test_exciton.py、git log 直近3コミット、3 Production MANIFESTs、convergence dirs、working tree diff）
- レビュー依頼: なし（exploratory ノートは PI 判断依頼、本 patrol で軽量コードレビュー所見のみ補助）
- BLOCKED: **CLOSE**（2225_BLOCKED_session_stalled.md を本 patrol で解除、復帰 commit 確認済み）
- 最新コミット: `1a93de0` cowork/progress: Theme I exciton exploratory — effective masses solid, E_b absolute needs PI judgment（3 分前）
- 進捗判定: 🟢 **順調**（session 復帰、Option A+B 両方消化、Theme I は Production 化前で正しく PI 判断停止）
- 本番計算ルール違反: **なし（30 連続 patrol でクリーン）**
- ユーザーへの通知: あり — (1) セッション復帰、(2) Theme I で **PI 判断 3 択待ち** ((a) eff-mass のみ / (b) E_b 相対のみ / (c) 外部 ε_∞ で Production)
- 発行 directive: **なし**（PI 判断要素のため Cowork からは出さない）
- 次の patrol（0110）の期待: PI 判断到着 → 即 directive 発行 / 自走継続 → 通常 verify / 沈黙再発 → 軽 ping
