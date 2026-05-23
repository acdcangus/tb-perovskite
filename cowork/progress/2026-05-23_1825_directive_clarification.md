# Directive clarification — F5 status ping & 並行作業オファー

**発行:** Cowork (supervisor), 2026-05-23 18:25 JST (15:22 UTC)
**契機:** F5 builder commit (`9eeff23`, 14:37 UTC) から 45 分経過。3 連続 patrol で新規 commit / progress ログ / design.md なし
**性質:** **status ping（強い催促ではない）+ 並行作業オファー**

---

## 1. 確認したいこと（簡潔回答で OK）

F5 の現在ステータスはどれに該当しますか？ どれでも問題ありません、把握だけしたいです。

- (A) `.steering/<...>-theme_F_shift_current/design.md` を起草中（フル document、もう少しで提出）
- (B) 9 材料の δ（B-cation 変位）値の出典を文献調査中（Sn/Ge は文献値が少ない可能性）
- (C) 9 材料の `kashikar13_*_params.json` の準備中（`data/parameters/` 配下を確認・整備中）
- (D) F5 Production 投入前の k 収束テスト計画を構築中
- (E) その他 / 詰まっている → 内容を `cowork/progress/.../F5_blocked_<topic>.md` で書いてください
- (F) 別作業に切り替えた（例: 1410 directive の classic コピー、Theme A 論文化準備など）

**返答形式:** `cowork/progress/2026-05-23_<HHMM>_F5_status.md` に 1–3 行で十分。

---

## 2. design.md は段階提出で OK

フル design.md が完成するまで待つ必要はありません。例えば以下のような **中間版**でも Cowork は順次レビューできます：

1. **draft v0.5 (skeleton):** 章立てだけ + 各章の予定内容を 1 行ずつ
2. **draft v0.7 (numbers TBD):** 各章本文記述 + 9 材料 δ 値テーブルは `TBD` のまま
3. **draft v1.0 (final):** δ 値 + n_kpts 収束計画 + MANIFEST references 確定

中間版を `progress/` に出してくれれば、各段階で Cowork が文献整合や物理妥当性を確認します。

---

## 3. 並行作業オファー（idle time にどうぞ）

F5 Production の k 収束計算は CPU 時間が長い見込み（n_kpts ≥ 32 × 9 材料 × 3 段収束 = 数十分〜数時間）。**Production 実行中の並行作業**として以下を提案：

### 3.1 1410 directive: D ドライブ classic 15 件コピー（連続 6 patrol 未着手）

- 既に `references/pdfs/classic_Roth1960_PR118_1534.pdf` は 1 件取り込み済み
- 残り **15 件**（Kane-1957 ×2, Kane-1963, Vogl-1983, Luttinger-1955/56, Wannier-1937, Dresselhaus-1955, Ando-1982, Hjarmarson-1980, Bouckaert-1936, Cardona-1966, Cohen-1966, Chelikowsky-1974, Brust-1964, Kohn-1955 ×2）
- 詳細は `cowork/progress/2026-05-23_1410_directive_update.md` 参照
- 用途: Theme A 論文化時の Methods/Introduction で **歴史的引用の重み**を出すため
- 優先度: 中（必須ではないが、論文化フェーズで必要になる）

### 3.2 既存 Production の `references` フィールド点検

- `results/production/theme_A_g_factor/2026-05-23_31374dc/MANIFEST.json`
- `results/production/phase_1.5_optical/2026-05-23_31374dc/MANIFEST.json`
- 上記 2 つの MANIFEST.json の `references` リストに、新規取得した Boyer-Richard 2016・Hughes-Sipe 1996・Tan&Rappe 2015/2016・Roth-Lax 1960 を遡及追加（必要な場合のみ）

---

## 4. 文献調査で詰まっていれば Cowork が引き受けます

F5 で必要な数値で文献ソースが見つからないものがあれば、`cowork/progress/.../F5_literature_request.md` に書いてください：

- 9 材料の **B-cation [001] 変位量 δ** の DFT 計算文献値（特に Sn/Ge）
- prefactor 規約（Tan&Rappe vs Cook-Fregoso vs Young-Rappe の単位系差）の決定的出典
- Pb/Sn/Ge perovskite の **n_occ** 確認（Kashikar 13 軌道で全 9 材料が 20 で良いか）

Cowork が web search + arXiv で探します。

---

## 5. エスカレーション cadence（透明性のため明示）

- 1840 patrol（次回）で **何かしらの progress ログ**（A〜F いずれかの返答 or 中間 design.md）があれば → ✅ 静穏脱出、通常運用継続
- 1840 patrol でも 0 アクションなら → ⚠️ ユーザー通知 + より明示的な status 要求にエスカレート
- 別作業（1410 classic コピー等）に切り替えた場合も **その旨を progress に書く**だけで OK（責めません）

---

## 6. まとめ

- **強い催促ではない**。「設計フェーズが長い」自体は OK
- ただし **何をしているかの 1 行報告**だけ欲しい（透明性のため）
- design.md は段階提出 OK、中間版で順次レビュー可
- 並行作業として 1410 classic コピーが残っている（連続 6 patrol 未着手）
- 文献調査で詰まっていれば Cowork が引き受ける

無理せず進めてください。
