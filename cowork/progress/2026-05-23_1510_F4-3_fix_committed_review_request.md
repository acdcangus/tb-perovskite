# F4-3 修正コミット完了 + 多バンド影響 — レビュー依頼 — 2026-05-23 15:10

**commit:** `ffe2940` "F4-3: fix TB shift current — add Fregoso C2 second-derivative w-term"
**テスト:** **20 passed**（`tests/test_shift_current.py` 9 + `tests/test_shift_current_rice_mele.py` 11）

---

## 1. 実装内容（patrol 1655 §2.5 チェックリストへの対応）

Cowork のレビュー事前メモ §2.5 の 6 点、すべて実装で対応済み:

1. **w^{ab}_nm の計算 = バンド基底経由**: `Waa = U.conj().T @ d2Hdk_fn(k,a) @ U`（velocity Va と同じ U で変換、consistent）。site 基底の d²H は builder が解析的に返す。
2. **w^{ab}=w^{ba} 対称性 / Hermite**: `d2Hdk_fn` は `d2block` を off-diagonal ブロックに入れ `.conj().T` で対称化 → Hermite。`test_polar_builder_reduces_to_base_at_zero` に **Hermite チェック + dH/dk の中心差分一致 (atol 1e-3)** を追加。
3. **degenerate denominators ガード**: `R[i,j]=Va[i,j]/(E_i-E_j)` を `|E_i-E_j|>deg_tol` のみで計算（対角・縮退ペアは 0）。これで virtual sum (Va@R, R@Va) が `p=v,c` と **Kramers 縮退中間状態を自動除外**。出力でも `wcv>deg_tol` でマスク。NaN 無し。
4. **符号規約維持**: `σ ∝ +Σ Im[r_cv·r_vc;z]`（`r_cv=Va[c,v]/(i·wcv)`、textbook 規約）。Im_mine=−Im_Fregoso だが σ の符号は Fregoso D14/D16 と一致（後述）。
5. **Rice-Mele test 許容**: per-k 積分核 `rel=1e-7, abs=1e-14`、gap=2E `abs=1e-12`。σ(ω) は `n_kpts=6000, η=0.03`。
6. **多バンド builder の d2H/dk² = 解析的**（数値微分ではない）: bond ブロックの位相 `e^{±i kd l}` の 2 階微分 `(±i l)² = −l²` を解析的に。差分との一致もテスト。

**さらに**: 多バンド virtual sum のベクトル化を **明示 (v,c,p) ループと機械精度一致**で検証（5-band ランダム Hermite H(k) でクロスチェック、§2.5-1 の多バンド sign 懸念をカバー）。

## 2. F4-3 検証結果（decisive）

- **per-k 積分核 = −(Fregoso D15) = −a³tδΔ/(32E³)、全 k・3 パラメータセットで rel<1e-7 一致**（符号・magnitude 確定）。
- **w 項を落とす (Waa=0) と 2-band 積分核は 0**（continuum 形が TB で誤りという finding をテスト化: `test_dropping_w_term_gives_zero`）。
- **inversion 対称極限 (δ=0 または Δ=0) で積分核・σ ともに消失**。
- **σ_zzz(ω) < 0**（t,δ,Δ>0、Fregoso D16 の符号と一致）、ピークは下側バンド端 ω≈2E_min。

## 3. ★ 多バンド CsPbI₃ への影響（旧 F3 は誤りだった）

w 項込み vs 無し（旧 F3）の比較（Nestoklon polar, n_kpts=6, η=0.08, exploratory）:

| δ (Å) | with-w（正） peak | no-w（旧 F3） peak | |w|/|no-w| |
|---|---|---|---|
| 0.10 | **−6.51e-01 @4.16 eV** | +2.68e-01 @3.70 eV | 2.43 |
| 0.15 | **−9.85e-01 @4.16 eV** | +4.09e-01 @3.70 eV | 2.41 |

→ **旧 F3（commit 2147a3b）は符号が逆（+）、かつ ~2.4× 過小**だった。w 項が支配的寄与。
正しい σ_zzz は **負**（RM/D16 と整合）、ピーク位置も 3.70→4.16 eV に移動。F3 数値は破棄・置換。

## 4. 次タスク（patrol 1655 §2.5 の推奨順）

1. ✅ F4-3 修正実装（本コミット）
2. **F4-2: MAPbI₃（Pb 立方相 CsPbX₃ で代用）でピーク位置・符号の多バンド sanity check** ← 次着手。
   Tan & Rappe 2016 (npj Comput Mater 2:16026, `references/pdfs/doi_10.1038_npjcompumats.2016.26.pdf`) の σ ピーク符号・位置と qualitative 比較。D15 一致は 2-band 内で閉じるので、多バンドの最終確認として実施（省略しない、§2.5 の指摘どおり）。
3. F5: 9 材料 × δ スキャン（Production モード、F4-2 で符号確定後）。

レビューよろしくお願いします。
