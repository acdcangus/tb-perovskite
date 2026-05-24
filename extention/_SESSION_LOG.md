# セッションログ（リキャップ・引継ぎ用）

**最終更新**: 2026-05-24（セッション中断時点）
**ユーザー**: ktmailmg@gmail.com (Teruhisa Kotani)
**作業目的**: 半導体物性数値計算コード3本に対し、ここ10年の研究トレンドを踏まえた追加機能仕様書を作成し、コーディングエージェントへ渡す。

---

## 1. 元依頼（原文）

> 複数のプロジェクトで半導体の物性を数値計算するコードを開発しています。いくつかは、現在も研究プロジェクトを続けており開発はつづいています。あなたは、俯瞰的な目でみて、ここ１０年の、量子井戸、量子ワイヤ、量子ドット、ペロブスカイトなどの研究トレンドを鑑みて、論文が出せるクオリティの数値計算をするためにあらたに付け加えるべき機能をそれぞれのプログラム開発エージェントに渡すための仕様として作ってください。アルゴリズム実装についてはハルシネーションを避けるため、アルゴリズムが記載されている論文を参考文献としてつけることを必須としてください。2017年以前の論文はD:\Research\Papers\Paperにもあります。成果物はC:\Users\kteru\OneDrive\Desktop\成果物にmdファイルと参考文献のPDFファイルをいれてください。ただ、成果物については批判的にレビューを行い、３回程度指摘がなくなって初めてOKとします。大規模計算環境がないので、計算は通常の個人が持っているコンピュータレベルの規模を想定しています。
>
> C:\Users\kteru\kp8band-qdsl
> C:\Users\kteru\kp-qw-simulator
> C:\Users\kteru\tb-perovskite

## 2. ユーザの追加指示（経過順）

1. **こまめに成果物を保存** すること（制限近接対応）
2. 別セッションでもリキャップできるよう本ログを残すこと
3. **QCL は不要**（kp-qw-simulator F6 削除済み）
4. **磁場応答は全部保持**（g-tensor, AHC, Edelstein, 励起子磁場シフト）
5. **デスクトップで厳しい機能は他にも削除可**（→ tb-perovskite F10 動的無秩序削除済み）
6. 「2次元の方向のバンド構造とか、3次元でも実空間とか、そういうのはいける」
7. 「2次元とか3次元実空間は私の意見も聞きたい」 → 私の意見回答済み（後述）
8. 「あとは周期境界入れるとか、バイアスをかけるとか」
9. 「周期境界を入れるならミニバンドの計算もいるよね」 — **その通り**
10. （最後）AskUserQuestion がツールエラーで失敗 → セッション再起動

## 3. 確認済みのユーザー選好

| 項目 | 選択 |
|---|---|
| 仕様書の言語 | 日本語（説明）＋英語（技術用語） |
| 重視する研究テーマ | 光物性、輸送・電子状態、デバイス応用、新材料・トポロジカル・非エルミート（全選択） |
| 参考文献PDF収集方針 | D:のPDFをコピー＋新しい論文もできる限りarXiv等から入手 |
| 「論文が出せる」基準 | 数値精度＋検証可能性と新規性の両方バランスよく |
| 磁場応答 | 全部保持 |
| QCL | 削除 |

## 4. 接続済みフォルダ

- `C:\Users\kteru\kp8band-qdsl`
- `C:\Users\kteru\kp-qw-simulator`
- `C:\Users\kteru\tb-perovskite`
- `D:\Research\Papers\Paper` — 2017以前の論文倉庫（125サブフォルダ）
- `C:\Users\kteru\OneDrive\Desktop\成果物` — 出力先

## 5. 完成済みファイル（current state, r5 として最新）

```
成果物/
├── 00_README.md                    ← 全体構造・ファイル一覧・統一単位系・受入基準・統合方針・レビュー方針
├── _SESSION_LOG.md                 ← 本ファイル
├── 01_kp-qw-simulator_spec.md      ← QW 仕様（F1–F12、F6 QCL削除済み、F11/F12 追加済み）
├── 02_kp8band-qdsl_spec.md         ← QDSL 仕様（F1–F11、F11 Berry phase 分極追加済み）
├── 03_tb-perovskite_spec.md        ← TB 仕様（F1–F14、F10削除、F13/F14 追加済み）
├── 04_review_log.md                ← 3回レビュー + 削除機能 + r4 追加機能
├── 05_references_index.md          ← PDF↔仕様書 文献索引（B0 節に r4 追加分）
├── 06_validation_references.md     ← 妥当性検証用 文献リスト
├── 07_agent_handoff.md             ← **NEW** 開発エージェント引渡し指示書
└── references_pdf/                 ← 参考文献 PDF 26 ファイル
```

## 5.5 r5（2026-05-24 セッション継続）の決定事項

| 項目 | 決定 |
|---|---|
| 3 プロジェクトの統合 | **しない**（波動関数基底が異なる） |
| 共通コアライブラリ化 | **将来の可能性のみ**（今は重複実装許容） |
| 可視化スイート (V series) | **別仕様に分離**（保留） |
| 3 回批判的レビュー方針 | Claude Code + 別 Claude で 3 ラウンド、指摘がなくなるまで反復 |
| ハルシネーション防止 | 全引用文献の DOI 事前確認を実装エージェントの責務として明文化 |
| エージェント引渡し | `07_agent_handoff.md` に集約 |

## 6. 既に削除済みの機能（2026-05-24 ユーザ指示）

| プロジェクト | 機能 | 理由 |
|---|---|---|
| kp-qw-simulator | F6 ISB/QCL | QCLは現代的解析にNEGF/Monte Carlo 必須、デスクトップ不可 |
| tb-perovskite | F10 動的無秩序 (MD-TB 結合) | AIMD 多数スナップショット必要、HPC 必須 |

## 6.5 r4 追加機能（2026-05-24 セッション再開後に確定）

| プロジェクト | 機能 | 状態 |
|---|---|---|
| QW | F11 QWSL ミニバンド | ✅ 追加済 |
| QW | F12 DC バイアス（Mode A 有限N + Mode B Wannier-Stark） | ✅ 追加済 |
| QDSL | F11 Berry 位相分極（KSV 1993） | ✅ 追加済 |
| TB | F13 2D RP infinite stack | ✅ 追加済 |
| TB | F14 電場（Stark slab + Berry bulk） | ✅ 追加済 |
| 全 | V series 可視化 | 📌 別仕様に分離（保留） |

## 7. **未確定の追加候補（次セッションの作業）**

ユーザ指示8–9で追加が依頼された下記機能を仕様書に取り込む必要がある。AskUserQuestion がエラーで止まったため、ユーザに最終確認を取れていない。

### 7.1 可視化・解析モジュール（V series）— 全コード対象

私の意見（既にチャットで送付済み）：
- **2D 面内分散・BZ スライス** ★★★ — kp-qw-simulator（`ksampling/full2d.py` 拡張）/ tb-perovskite（新規）
- **3D 実空間波動関数 ψ²・励起子密度** ★★★ — kp8band-qdsl（核心）/ QW は限定的 / TB は MLWF が必要
- **3D アイソエネルギー面（k 空間）** ★★ — TB の Berry curvature ホットスポット可視化
- **空間分解 LDOS / k-投影 spectral function** ★★ — 全コード（ARPES比較）
- **Wannier 関数（MLWF）** ★ — tb-perovskite オプション（既に SK 基底なので限定的）

### 7.2 周期境界 + ミニバンド + バイアス

#### kp-qw-simulator
- **新規 F11 QW Superlattice (QWSL) — 成長方向周期境界 + ミニバンド**
  - 物理：Esaki–Tsu 1970 の QWSL。InGaAs/InAlAs, GaN/AlGaN MQW を有限N周期 vs 無限周期で比較。**ミニバンド分散 E(k_z), DOS, ミニギャップ**
  - 参考文献：Esaki–Tsu, IBM J. Res. Dev. 14, 61 (1970); H. T. Grahn et al., PRB 51, 17827 (1995); F. Capasso, Science 235, 172 (1987)

- **新規 F12 外部 DC バイアス：Stark ladder / Wannier–Stark 局在**
  - 物理：QWSL 印加電場での Wannier–Stark ladder, Bloch oscillation
  - 参考文献：G. H. Wannier, PR 117, 432 (1960); E. E. Mendez et al., PRL 60, 2426 (1988); J. Bleuse et al., PRL 60, 220 (1988)

#### kp8band-qdsl
**重要な物理的制約（2026-05-24 ユーザ指摘）**：
QDSL は完全 3D 周期境界条件下にあるため、**一様 DC 電場と整合しない**（ポテンシャルが発散）。したがって従来想定の「外部 DC バイアス印加」機能は実装不可。

代わりに以下のいずれかで「電場応答」を扱う：

- **新規 F11 Modern theory of polarization（Berry phase 形式）**
  - 物理：King-Smith–Vanderbilt 1993, Resta 1994 によるバルク分極の Berry 位相公式
  - polarizability、自発分極、ピエゾ分極の **周期境界整合な** 評価
  - F4 QCSE と統合可能（local field 効果の補強）
  - 参考文献：R. D. King-Smith, D. Vanderbilt, PRB 47, 1651 (1993); R. Resta, RMP 66, 899 (1994); R. W. Nunes, X. Gonze, PRB 63, 155107 (2001)

- **オプション：周期性破り supercell + dipole correction**
  - 「実効的バイアス」をかけたい場合、PBC を破り finite supercell + Neugebauer-Scheffler dipole correction
  - 参考文献：J. Neugebauer, M. Scheffler, PRB 46, 16067 (1992)

- **AC 応答** は既存 absorption / F8 IBSC で対応済み

#### tb-perovskite
- **新規 F13 2D RP の無限周期化（z 方向 stacking周期）**
  - F5 slab の natural extension。n 層 RP を周期 stack させ「type-II 様」ミニバンド計算
  - 参考文献：Smith, Mailhiot, JAP 62, 2545 (1987); Even 2014

- **新規 F14 外部電場印加（Peierls phase or scalar potential）**
  - Stark shift, BPVE 補強（F8 と統合可能）
  - 参考文献：R. W. Nunes, X. Gonze, PRB 63, 155107 (2001); P. Umari, A. Pasquarello, PRL 89, 157602 (2002)

## 8. 次セッションでの最初の質問（必須）

ユーザに以下を確認してから作業再開：

1. 7.1 可視化機能の **追加範囲**（全部 or 2D dispersion + BZ slice のみ or 全部スキップ）
2. 7.2 周期境界・ミニバンド・バイアスの **追加範囲**
   - 7.2 の追加が決まったら、各仕様書の機能リスト・ロードマップ・受け入れテスト・BibTeX・references_index.md を更新する

## 9. 仕様書の章立て（各 spec ファイル共通）

1. 既存機能サマリ
2. 研究トレンド分析（2015-2026）
3. 追加機能群（F1, F2, ...）：目的 / Novelty Statement / 入出力 / アルゴリズム / 必須参考文献 / 計算規模 / 検証
4. アーキテクチャ統合方針
5. 段階的実装ロードマップ
6. 参考文献（BibTeXキー）
7. 受け入れテスト

## 10. ハルシネーション防止指針（既に00_README.mdに記載）

- 仕様書に書かれた参考文献の **DOI/arXiv ID を事前に確認** すること
- 「未検証文献マーク」（`05_references_index.md` C節）の文献は **着手前に必ず実在確認**
- アルゴリズムは仕様書の **参考文献に基づいて実装**

## 11. 各プロジェクトの既知情報

### kp8band-qdsl
- ベース論文: T. Kotani et al., JAP 115, 143501 (2014) [PDF: Kotani2014_JAP115_143501.pdf]
- src/qdsl/ に absorption, exciton, hamiltonian(zb/wz), strain, piezo, poisson, matfree_zb, qdsl_hamiltonian
- **完全3D周期、ミニバンド計算は本来の主出力**
- 既に WZ 実装、matrix-free preconditioner、Fortran クロスチェック進行中

### kp-qw-simulator
- WZ 6-band（c面・非極性／半極性）U1 完了、ZB 4/6/8-band U2 進行中
- U3 (WZ 8-band)、U4 (ZB 非[001] piezo)、U5 (MQW) 計画
- 面内のみ周期、成長方向は閉じ込め
- **MQW 拡張 + 成長方向周期 + ミニバンドが自然な拡張**
- ベース論文: Kotani et al. APL 102, 011128 (2013) [PDF: Kotani2013_APL102_011128.pdf]

### tb-perovskite
- ベース論文: Kashikar arXiv:2101.08562, Nestoklon arXiv:2012.14705
- 立方相 CsBX₃ (B=Ge/Sn/Pb, X=Cl/Br/I) sp³d⁵s* TB
- velocity operator, g-factor, shift current, optical 実装済み
- references/pdfs/ に arxiv 論文多数

## 12. 統一単位系（全仕様で同一）

- エネルギー: eV
- 長さ: Å
- 電場: V/Å
- 磁場: Tesla
- 温度: K

## 13. 共通 Acceptance 基準（全機能）

1. 解析解または既知 limit との一致テスト（unit test）
2. 論文 figure/table の再現テスト（regression test）
3. 収束テスト（mesh, basis size, cutoff）

## 14. 共通計算規模制約

- メモリ ≤ 32 GB
- 計算時間 ≤ 24 h（パラメータスキャンを除く）
- 並列: OpenMP / マルチプロセス（最大16コア）
- GPU: 任意
- HPC・MPI 分散はスコープ外

## 15. 残課題（実装中の注意, 04_review_log.md からの抜粋）

| ID | 内容 | 担当 |
|---|---|---|
| R-1 | F3 Auger は OpenMP 並列必須 | QW |
| R-2 | F1, F2 共通 `core/coulomb.py` の API 設計は事前レビュー | QW |
| R-3 | F2 CI は active space を default 制限 | QDSL |
| R-4 | F3 BSE の screening は model dielectric 限定 | TB |
| R-5 | F10 動的無秩序は削除済み | TB |
| R-6 | 「未検証文献マーク」の実在確認を着手前に | All |

## 16. 別セッション継続時の手順

1. 本ファイル `_SESSION_LOG.md` を最初に読む（全文）
2. 成果物フォルダ `C:\Users\kteru\OneDrive\Desktop\成果物` のファイル一覧と各 md の章立てを確認
3. **セクション 7「未確定の追加候補」と セクション 8「最初の質問」をユーザに確認**
4. 確認が取れたら、該当する仕様書を更新（F11, F12, F13, F14 などを追加）
5. 追加機能には必ず参考文献を DOI 付きで紐づけ
6. PCスケール（≤32GB, ≤24h, ≤16コア）の制約を維持
7. 必要なら参考文献 PDF を D:\Research\Papers\Paper から追加コピー
8. 大きな変更後は 04_review_log.md に「レビュー4回目」セクションを追記

## 17. 既に作成済みの主要ファイルの章立て概要

### 01_kp-qw-simulator_spec.md（最新状態）
- F1 多体補正利得（Padé/HF+plasmon-pole）
- F2 BSE 励起子（磁場下オプション含む）
- F3 Auger（OpenMP 必須）
- F4 g-tensor（Pryor-Flatté）
- F5 Z₂ topology（HgTe + InAs/GaSb）
- F6 **削除済み（QCL）**
- F7 非エルミート PT-symmetric QW
- F8 合金統計揺らぎ MC
- F9 ポラリトン/マイクロキャビティ

### 02_kp8band-qdsl_spec.md（最新状態）
- F1 FSS + bright/dark exciton
- F2 Active-space CI（N≤4）
- F3 g-tensor
- F4 QCSE
- F5 Huang-Rhys + exciton-phonon
- F6 キャリア捕獲・緩和（WL→QD）
- F7 Purcell 自発放出
- F8 QDSL ミニバンド + IBSC 効率
- F9 Strain engineering
- F10 配向自由化（[111] QD）

### 03_tb-perovskite_spec.md（最新状態）
- F1 Berry curvature（AHC/SHC/OH）
- F2 トポロジカル不変量（Z₂, Wilson loop）
- F3 BSE 励起子（model dielectric）
- F4 Rashba 解析
- F5 2D RP slab
- F6 Fröhlich Polaron 移動度
- F7 CPGE
- F8 SHG / NLO
- F9 熱電・熱輸送
- F10 **削除済み（MD-TB）**
- F11 Edelstein / Inverse Edelstein
- F12 歪み・電場バンド工学

## 18. 重要参照論文（既に特定済み）

### k·p QW
- Vurgaftman, Meyer, Ram-Mohan, JAP 89, 5815 (2001)
- Gershoni, Henry, Baraff, IEEE JQE 29, 2433 (1993)
- Asada, Kameyama, Suematsu, IEEE JQE 20, 745 (1984) [PDF同梱]
- Meney, Gonul, O'Reilly, PRB 50, 10893 (1994)
- Foreman, PRB 56, R12748 (1997) [PDF同梱]
- Chuang, Chang, PRB 54, 2491 (1996)
- Kotani et al., APL 102, 011128 (2013) [PDF同梱]

### k·p QD
- Kotani et al., JAP 115, 143501 (2014) [PDF同梱]
- Stier, Grundmann, Bimberg, PRB 59, 5688 (1999)
- Bester, Zunger, Wu, Vanderbilt, PRB 74, 081305 (2006)
- Andreev, O'Reilly, PRB 62, 15851 (2000)
- Bayer et al., PRB 65, 195315 (2002)

### TB Perovskite
- Kashikar et al., arXiv:2101.08562 (2021) [PDF同梱]
- Nestoklon, arXiv:2012.14705 (2021) [PDF同梱]
- Xiao, Chang, Niu, RMP 82, 1959 (2010)
- Sinova et al., RMP 87, 1213 (2015)
- Frost, PRB 96, 195202 (2017)

## 19. 次セッションで使うフレーズ例

新しいセッションでユーザが「再開して」と言ったら、以下のような流れで応答する：

> 引継ぎログ（C:\Users\kteru\OneDrive\Desktop\成果物\_SESSION_LOG.md）を確認しました。
> 前回 QCL（QW F6）と動的無秩序（TB F10）を削除した後、以下の追加候補について
> ユーザに確認を取る直前で中断しました：
> 
> 1. 可視化機能（V series）: 2D dispersion, 3D 実空間 ψ², 3D iso-energy 等
> 2. QW: F11 QWSL ミニバンド、F12 Wannier-Stark
> 3. QDSL: F11 外部 DC バイアス
> 4. TB: F13 2D RP 無限周期、F14 Peierls 電場
> 
> どこから着手しますか？
