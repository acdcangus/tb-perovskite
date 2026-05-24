# 開発エージェントへの引渡し指示書

**作成日**: 2026-05-24
**対象読者**: 各プロジェクトのコーディングエージェント（Claude Code 等）
**作成者**: Claude（仕様化担当, 本会話のアシスタント）

---

## 0. 全エージェント共通の必須遵守事項

### 0.1 ハルシネーション絶対防止

本仕様書群は、Claude（汎用 LLM）の **知識（May 2025 cutoff）に基づいて作成された** ものであり、以下のリスクを内包する：

- 論文タイトル・著者・DOI・巻号・年が **記憶ベース** で生成されている部分がある
- 一部の物理式・公式・係数は **記憶を辿った再構成** であり、原典との照合が未完
- ハルシネーション（存在しない論文の引用、誤った式の生成）の可能性ゼロではない

**実装エージェントの責務**：

1. **すべての引用文献について、実装着手前に DOI / arXiv ID を実際に確認する**
   - WebSearch / mcp__workspace__web_fetch で論文タイトル + 著者 + 年 を検索
   - DOI が解決するか確認
   - PDF が `references_pdf/` に同梱されている場合はそれを優先
2. **アルゴリズムの式は仕様書本文ではなく、原典論文の式番号を参照して実装する**
   - 仕様書本文の式は要約・概略であり、原典こそが正典
3. **実在しない・確認できない引用を見つけた場合、即座にユーザに報告**
   - 該当機能の実装を **保留** し、代替論文を探す
   - 勝手に類似論文に差し替えない

### 0.2 3 回の批判的レビュー

ユーザ指示（2026-05-24）：

> すべてのレポート類は、claude code およびあなた（Claude）それぞれで批判的にレビューして、3 回指摘がなくなるまで何度もレビューしなおしてね。特に、ハルシネーションは絶対ダメ。記憶じゃなくて、文献など事実に基づいて確認は必須。

実装中・実装後の各レポート（progress notes, novelty assessment, code review）は：

1. **Claude Code（実装エージェント）が自己批判的にレビュー** → 修正
2. **別の Claude（汎用、本会話継続セッション等）にレビューを依頼** → 修正
3. **3 ラウンド指摘がなくなるまで反復**

レビュー観点：
- 物理的整合性（次元解析、保存則、対称性）
- 数値的整合性（収束、安定性、ベンチマーク）
- 引用文献の実在性・正確性（DOI チェック）
- 既存実装との後方互換性
- PC スケール制約遵守（≤ 32 GB, ≤ 24 h, ≤ 16 コア）

### 0.3 統合しない方針（2026-05-24 ユーザ確定）

> 波動関数の形とか違うから、統合せずに別にやりましょう。

3 プロジェクトは **独立に開発・維持** する。共通コアライブラリ化は **将来の可能性として保留** （Berry curvature / g-tensor / BSE などのアルゴリズム実装重複は当面許容）。

別プロジェクトの実装を **参考にしない**：
- QW で実装した Berry curvature を TB に流用しない（波動関数基底が異なる）
- QDSL の Coulomb 行列要素を QW に流用しない（基底・形状積分が異なる）
- 各プロジェクトは独自にゼロから実装し、独自にテストする

---

## 1. プロジェクト別の引渡しファイル

### 1.1 kp-qw-simulator（量子井戸 k·p シミュレータ）

**渡すファイル**：
1. `01_kp-qw-simulator_spec.md` — メイン仕様（F1–F12、F6 削除）
2. `04_review_log.md` — レビュー記録、削除機能、追加機能、注意事項
3. `05_references_index.md` — 参考文献索引、未検証文献マーク
4. `06_validation_references.md` — 妥当性検証用文献（QW 関連の §1, §4 表）
5. `00_README.md` — 全体方針、計算規模制約、Acceptance 基準
6. `07_agent_handoff.md` — 本ファイル
7. `references_pdf/` — 関連 PDF（特に Foreman1997, Asada1984, Chow-Koch, Mendez1988, Bleuse1988）

**実装の優先順序**（仕様書 §5 のロードマップに基づく）：
1. Phase A: F4 g-テンソル（軽量、既存 8-band 上に Pryor–Flatté 公式実装）
2. Phase B: F2 励起子（Andreani–Pasquarello）
3. Phase C: F1 多体補正利得（Padé 軽量版から）
4. Phase D: F3 Auger（OpenMP 必須）
5. Phase E: F5 トポロジー（HgTe, InAs/GaSb 2D-TI）
6. **Phase F: F11 QWSL ミニバンド**
7. **Phase G: F12 DC バイアス（Mode A → Mode B の順）**
8. Phase H: F7–F9 オプション（非エルミート、合金揺らぎ、ポラリトン）

**スコープ外（明示的除外）**：
- F6 QCL / Intersubband — デスクトップで NEGF 不可
- 可視化スイート — 別仕様に分離

### 1.2 kp8band-qdsl（量子ドット超格子 8-band k·p）

**渡すファイル**：
1. `02_kp8band-qdsl_spec.md` — メイン仕様（F1–F11、F11 Berry phase 追加済み）
2. `04_review_log.md`
3. `05_references_index.md`
4. `06_validation_references.md`（§2, §4 表）
5. `00_README.md`
6. `07_agent_handoff.md` — 本ファイル
7. `references_pdf/`（特に Kotani2014, Foreman1997, Burt, 8bandHamiltonian, Luque/Marti）

**実装の優先順序**：
1. Phase A: F3 g-テンソル
2. Phase B: F1 FSS + bright/dark
3. Phase C: F4 QCSE
4. Phase D: F2 CI 多体励起子（N_e=N_h≤4 active space）
5. Phase E: F5 励起子–フォノン
6. Phase F: F8 IBSC 効率計算
7. **Phase G: F11 Berry 位相分極（KSV 1993）**
8. Phase H: F6, F7, F9, F10 オプション

**既存ベンチマーク維持**：
- Kotani 2014 JAP の単粒子近似結果は **`enable_excitons=False` の既定モード** で従来通り再現
- Fortran クロスチェック（`.steering/20260524-fortran-crosscheck-and-wz-sweep`）と矛盾しないこと

**スコープ外**：
- 完全周期下の一様 DC バイアス（物理的不整合）→ F11 Berry phase 形式で代替

### 1.3 tb-perovskite（ハライドペロブスカイト TB）

**渡すファイル**：
1. `03_tb-perovskite_spec.md` — メイン仕様（F1–F14、F10 削除）
2. `04_review_log.md`
3. `05_references_index.md`
4. `06_validation_references.md`（§3, §4 表）
5. `00_README.md`
6. `07_agent_handoff.md` — 本ファイル
7. `references_pdf/`（特に arxiv_2101.08562 Kashikar, arxiv_2012.14705 Nestoklon, classic_Roth1960, Kopteva2026）

**実装の優先順序**：
1. Phase A: F1 Berry curvature → AHC/SHC/OH（既存 velocity operator 拡張）
2. Phase B: F2 トポロジー（Z₂, Wilson loop）
3. Phase C: F4 Rashba 解析
4. Phase D: F6 Polaron 移動度
5. Phase E: F3 BSE 励起子（model dielectric）
6. Phase F: F5 2D RP slab
7. Phase G: F7 CPGE, F8 SHG
8. Phase H: F9, F11, F12 オプション
9. **Phase I: F13 2D RP infinite stack**
10. **Phase J: F14 電場（Mode A slab → Mode B bulk）**

**既存テーマとの整合**：
- `cowork/future_themes.md` の Theme H, I, J, K, L はそれぞれ F1, F3 経由, F7, F5+F13, F6 に対応
- Theme A (g-factor), Theme F (shift current) は既実装。本仕様の F1, F8 はそれらの再構築/拡張ではなく、**Berry curvature 統合インフラ** という別の枠組み

**スコープ外**：
- F10 動的無秩序 (MD-TB 結合) — AIMD 必須でデスクトップ不可

---

## 2. 各エージェントが守るべきワークフロー

各機能の実装で、以下のサイクルを必須とする：

### サイクル A: 引用文献の事前確認（着手前, 全機能）

```
[エージェント] 仕様書を読む
       ↓
[エージェント] 各引用文献の DOI / arXiv ID を WebSearch で確認
       ↓
   実在する? ────── No ─→ [エージェント] ユーザに報告、保留
       ↓ Yes
[エージェント] 該当 PDF（同梱 or 外部取得）から該当式番号・節を読む
       ↓
[エージェント] 仕様書本文の式と原典を照合（差異あれば原典優先）
       ↓
[実装着手]
```

### サイクル B: 単体テスト + 解析解照合（実装後）

仕様書 §「検証」節および `06_validation_references.md` の最低再現対象に基づく。

### サイクル C: 3 回批判的レビュー

```
[Claude Code] 自己批判的レビュー
   →  PR / progress note を生成
       ↓
[別の Claude（汎用）] レビューを依頼（外部セッション）
   → 指摘事項を抽出
       ↓
[修正]
       ↓
3 回反復、指摘がなくなったら "Reviewed-by: Claude (assistant) × 3" タグ
```

レビュー観点チェックリスト：

- [ ] 物理：次元解析が通る？ 保存則が成立？ 対称性が破れていない？
- [ ] 数値：収束テストの order-of-convergence は期待通り？
- [ ] 引用：DOI が解決する？ 式番号が原典と一致？
- [ ] 互換：既存ゴールデン回帰が破壊されていない？
- [ ] 規模：メモリ ≤ 32 GB、時間 ≤ 24 h、コア数 ≤ 16？
- [ ] ハルシネーション：すべての数値・公式が文献由来で記憶由来でない？

---

## 3. ハルシネーション疑い箇所の見つけ方

仕様書を読みながら以下をチェック：

| 疑いの種類 | 確認方法 |
|---|---|
| 論文タイトル・著者の組合せが不自然 | Google Scholar で著者 + 年 + キーワードで検索 |
| DOI のフォーマットが不正 | crossref.org / doi.org で resolve 確認 |
| 古い論文（< 2010）の volume/page 番号 | JPS / APS / IEEE の公式ジャーナルサイト |
| 新しい論文（> 2018）の arXiv ID | arxiv.org で番号を直接入力 |
| 数値（例: g* = -0.44）の出典 | 原典の表 / 図番号まで遡って確認 |

**赤旗（red flag）**：
- 「Wang 2017」のような著者と年だけのアバウトな引用
- 「F. Sacconi et al., PRB 86, 085210 (2012)」のように年は古いが内容（合金揺らぎ MC）が新しめ
- arXiv ID が 5 桁台で年と矛盾（例: arXiv:1234.5678 (2024) は不可。2024 なら 24xx.xxxxx）

---

## 4. 修正・差分の反映先

実装エージェントが仕様書の誤り・補強を発見した場合：

- **誤植・式の符号誤り等の小修正**：当該 spec ファイルを直接 PR
- **追加機能の提案**：当該プロジェクトの `.steering/[YYYYMMDD]-[作業タイトル]/requirements.md` として独立
- **本仕様書群（00–07）の改訂**：`C:\Users\kteru\OneDrive\Desktop\成果物` に直接コミット、`_SESSION_LOG.md` の改訂履歴を更新

---

## 5. 最後に — エージェントへのメッセージ

本仕様書群はあくまで **「研究の方向性と必須参考文献を整理した出発点」** です。実装の細部・パラメータ選択・テスト戦略は、原典論文と既存コードを読みながら **自律的に判断** してください。

ただし、以下は絶対に守ること：

1. **ハルシネーションをしない**：DOI / 式番号を必ず原典で確認
2. **既存ベンチマーク（U1 ゴールデン、Fortran クロスチェック、PRODUCTION_RULES）を壊さない**
3. **PC スケール制約を超えない**：HPC や AIMD は外部入力に分離
4. **3 回の批判的レビューを通す**

幸運を祈ります。
