# Supervisor Patrol — F4-3 caught F3 bug (decisive win) (2026-05-23 16:55 JST / 13:54 UTC)

**監督:** Cowork (scheduled task `tb-perovskite-supervisor`, 15-min cycle)
**前回:** 2026-05-23 16:40 JST（F4-3 静観継続、check-in 依頼に応答待ち）

---

## 1. 確認結果

過去 30 分以内に更新された progress ファイル: **3 件**（うち 1 件が新規 Claude Code 活動）。

| ファイル | 時刻 (UTC) | 種別 |
|---|---|---|
| `2026-05-23_1625_supervisor_patrol.md` | 13:24 | 自己発行 |
| `2026-05-23_1640_supervisor_patrol.md` | 13:39 | 自己発行 |
| **`2026-05-23_1445_F4-3_caught_missing_w_term.md`** | **13:50** | **★ Claude Code 重要報告** |

**新規コミット:** `b9b7739` (13:50 UTC, 4 分前)

```
b9b7739 cowork/progress: F4-3 caught missing w-term in F3 shift current
        (Fregoso C2); fix verified on Rice-Mele
```

中身は progress note のみ（`src/`・`tests/` 変更なし、`shift_current.py` 最終更新は依然 10:09 UTC）。code fix と Rice-Mele テストは「実装中」。

---

## 2. ★ 重要トピック: F4-3 が F3 のバグを検出（decisive な検証成功）

### 2.1 検出内容（要約）

`shift_current_zzz` の現行 sum-over-states 形に **Fregoso 2017 Eq.(C2) の第2微分項 `w^{ab}_nm = ⟨n|∂²H/∂k_a∂k_b|m⟩` が欠落**していた。

- **症状:** 2-band Rice-Mele に適用 → 積分核 ~1e-19 (≈ 0)、Fregoso D15 解析値 ~5e-3 と不一致。
- **原因の分析:** 2-band では virtual sum (p≠n,m) が空、かつ第1項 `2 r Δ/ω` は `Im[実数] = 0`。w 項が無いと per-k 積分核全体が消える。
- **これまで F3 で正しく見えた理由:** Nestoklon δ=0 vanishing は **対称性（0=0）で通っていただけ**で、w 項を持つ正しい formula を解いて 0 になったわけではなかった。

### 2.2 影響範囲

- **F3 commit `2147a3b` (CsPbI₃ Nestoklon-polar σ_zzz 数値)** — w 項込みで再計算が必要。**多バンドでは virtual sum 非ゼロのため、現行 σ_zzz 値は不完全（過小評価の可能性）。**
- **F4-4 commit `6de2224` (cubic δ=0 / P4mm σ_zzz 対称性チェック)** — δ=0 vanishing は対称性論理で再現可能（0=0 のまま）、P4mm σ_zzz ≠ 0 と σ_xxx ≈ 0 も対称選択則に縛られて変わらない見込みだが、**数値そのものは w 項込みで再回す必要あり**。

### 2.3 ★ Production-rules への影響: **なし（不幸中の幸い）**

| bundle | content | 影響 |
|---|---|---|
| `theme_A_g_factor/2026-05-23_31374dc` | Roth-Lax g-factor | 無関係 ✅ |
| `phase_1.5_optical/2026-05-23_31374dc` | ε(ω) Kubo-Greenwood (linear absorption) | 無関係 ✅ |

**shift current σ_zzz は Production bundle に未昇格**（F3-F4 は exploratory）。`cowork/reports/` にも σ_zzz の数値は含まれず。

→ **PRODUCTION_RULES §8 違反ゼロ。** 検証段階（F4）で bug を検出し Production promotion を未然に防いだ形になり、これは PRODUCTION_RULES が想定する「正しい運用」そのもの。

### 2.4 修正方針の評価（Claude Code 案）

```
r^a_{nm;b} = -(1/(iω_nm))[ (v^a_nm Δ^b + v^b_nm Δ^a)/ω_nm
                          − w^{ab}_nm
                          + Σ_{p≠n,m}(v^a_np v^b_pm/ω_pm − v^b_np v^a_pm/ω_np) ]
```
出典: Fregoso 2017 (arXiv:1701.00172) Eq.(C2)。

- **数式は正しい**。Fregoso 原論文の式番号・形と一致（in-repo `references/texts/arxiv_1701.00172.txt` で確認可能）。
- **Rice-Mele D15 と比較で magnitude 比 = 1.0、全 k で一致、符号も D14 と一致** という報告 — これは符号・prefactor を含めた **絶対値レベルでの確定**。F4-3 の主目的（「SSH 閉形式で σ_zzz 符号確定」）達成。
- **builder への影響:** `d2Hdk_fn(k, a, b)` を builder インタフェースに追加する必要あり。既存 builder（Nestoklon polar など）すべての d2H/dk² を実装する手間が発生するが、`(t₁+t₂ cos k) σ_x + ...` 型の解析 builder は微分は機械的に出る。

### 2.5 F4-2 の位置付け再評価

Claude Code は「これにより F4-3 で符号確定 → F4-2（Tan & Rappe）は補助確認に格下げ可」と書いていますが、**条件付きで賛成**：

- Fregoso D15 は per-k 積分核レベルで一致 → **数学的に確定**。F4-2 は実材料 (MAPbI₃) でのピーク位置・符号の sanity check に格下げで OK。
- **ただし** F4-3 の D15 一致は 2-band model 内で閉じている。多バンド (CsPbI₃ 4-band) で w 項の実装に bug があると検出できない（virtual sum 部分の sign）。F4-2 を「多バンドでの最終 sanity check」として **省略はしない方が良い**。
- 推奨優先度: **F4-3 修正実装 → 多バンド CsPbI₃ で再計算 → F4-2 で MAPbI₃ ピーク符号確認 → F5 (9 材料 × δ)**。

---

## 3. 次サイクル（17:10 JST / 14:09 UTC）の判断基準

| 状況 | アクション |
|---|---|
| **Code fix commit 出現** | コードレビューへ移行（特に w 項の符号・builder インタフェース・degenerate denominators 処理を厳しくチェック） |
| 13:50 から 30 分以上沈黙 | F4-3 修正実装の status ping |
| `tests/test_shift_current_rice_mele.py` 単独 commit | テスト先行 OK、本体実装待ち |

**コードレビューで特に見る点（事前メモ）:**
1. `w^{ab}_nm` の `⟨n|·|m⟩` 計算: バンド基底 (eigenvector) 経由か、site 基底経由か、どちらも consistent か。
2. `w^{ab} = w^{ba}` 対称性（Hermite 演算子の二階微分なので）。
3. degenerate denominators: virtual sum 内 `ω_pm = E_p - E_m → 0` のとき NaN にならないか、`p ≠ n, m` だけでなく `p` が `n` or `m` と縮退している場合のガード。
4. 符号規約: 現在の `σ ∝ +∫ Im_mine`（Im_mine = −Im_Fregoso）が新実装でも維持されているか。
5. Rice-Mele test の許容: `magnitude=1.0, 全 k で一致` の閾値（rel. err < 1e-6? 1e-10?）と smearing 設定。
6. 多バンド builder への `d2Hdk_fn` 追加: Nestoklon polar の d2H/dk² が解析的か数値微分か、後者なら step size の妥当性。

---

## 4. Production-rules compliance

差分なし。

| bundle | git_dirty | MANIFEST keys | convergence/ |
|---|---|---|---|
| `theme_A_g_factor/2026-05-23_31374dc` | `False` ✅ | 21 ✅ | dir 存在 ✅ |
| `phase_1.5_optical/2026-05-23_31374dc` | `False` ✅ | 21 ✅ | dir 存在 ✅ |

**違反なし。** §2.3 で詳述のとおり、shift current の bug は exploratory 段階で検出されたため Production 汚染ゼロ。

---

## 5. ユーザー通知

**通知: あり（informational、緊急性なし）**

内容:

- **F4-3 verification machinery が F3 shift current の missing w-term bug を検出。** これは PRODUCTION_RULES が想定する「Production 昇格前に検証で bug を捕まえる」流れの教科書的成功例。
- **既存 Production bundle は無事**（shift current は未昇格、ε(ω) と g-factor は別物理）。
- **Claude Code は Fregoso 2017 Eq.(C2) で fix を識別、Rice-Mele D15 で magnitude=1.0 一致を確認済み**。コード commit は実装中。
- ユーザー側で取るべきアクション: なし。次の patrol で fix commit のレビューを行います。Aversa-Sipe 1995 PDF 機関アクセス依頼は **継続有効**ですが、F4-3 が独立に sign 確定を出したため緊急度は低下。

---

## 巡回結果 (2026-05-23 16:55 JST)
- 確認したファイル数: 3（直近 30 分、うち 1 件が ★ 重要報告）
- レビュー依頼: 暗黙的にあり（F4-3 bug 検出 + 修正方針の妥当性）→ 本回答 §2 で評価・承認
- BLOCKED: なし
- 最新コミット: `b9b7739` cowork/progress: F4-3 caught missing w-term（4 分前）
- 進捗判定: **加速・健全** — F4-3 verification が想定どおり F3 の隠れた bug を検出。検証戦略（F4-3 + F4-2 の 2 段照合）の妥当性が実証された
- 本番計算ルール違反: なし（むしろ PRODUCTION_RULES の意図どおり Production 昇格前に bug 捕捉）
- ユーザーへの通知: あり（informational、§5 参照）
