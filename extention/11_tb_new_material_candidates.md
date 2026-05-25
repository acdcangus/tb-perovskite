# 新材料 TB 実装候補の整理（references/pdfs/Tight_Binding 精読）

**作成日**: 2026-05-25
**目的**: コア TB を CsBX₃ 以外の材料系へ拡張するため、`references/pdfs/Tight_Binding/` の論文を**実際に精読**し、実装可能な TB パラメータ源を「結晶系 / 基底軌道 / SOC / 近接範囲 / 対象材料 / SK パラメータ表の有無＋見積もり法 / 格子定数」で整理する。
**方針（no-hallucination）**: 記載はすべて PDF 本文から抽出（ページ引用）。本文に無い値は「無し」と明記。スキャン画像で読めない論文は**内容を推測せず OCR 要としてフラグ**。

> 重要な検証例: ファイル名 `PhysRevB.28.935.pdf` を記憶では「Vogl」と取り違えがちだが、**原典を読むと Kobayashi et al.（ウルツ鉱 AlN/CdS/CdSe/ZnS/ZnO）**。記憶ではなく原典で確認した。

---

## 1. 実装可能候補（自前で SK パラメータ表を持つ＝一次パラメータ源）

| # | 文献（原典確認） | 結晶系 | 基底軌道 | SOC | 近接 | 対象材料 | SK表 | 見積もり法 | 格子定数 | 実装可否 |
|---|---|---|---|---|---|---|---|---|---|---|
| A | **Kobayashi, Sankey, Volz, Dow, PRB 28, 935 (1983)** | ウルツ鉱 | sp³ | なし | 1NN | AlN, CdS, CdSe, ZnS, ZnO | Table I（9 param/材料）| Γ点で band 計算＋実験に fit; on-site は Vogl 則, off-site は Harrison d⁻² | **数値なし**（記号のみ）| △ 可（格子定数を外部調達＋Table I の一部 OCR 乱れを要再確認）|
| B | **Boykin, Klimeck, Oyafuso, PRB 69, 115201 (2004)** | ダイヤモンド | sp³d⁵s\* | **あり** | 1NN | Si, Ge | Table IV | 実験（gap・有効質量, 300K）に fit（GA＋手調整, Jancu 出発）| 無し（記号 a のみ）| ◎ 可（**既存 Nestoklon の sp³d⁵s\* 機構を再利用可**; 格子定数のみ要）|
| C | **Boykin, PRB 56, 9613 (1997)** | 閃亜鉛鉱 | sp³s\* | **あり** | 2NN | GaAs, AlAs, GaSb, AlSb, InAs, InP | Table I | 実験（300K の gap・有効質量）に手 fit; [001] ヘテロ向け | 無し | ○ 可（2NN sp³s\* Hamiltonian＋格子定数を要）|
| D | **Sapra, Shanthi, Sarma, PRB 66, 205202 (2002)** | 閃亜鉛鉱 | sp³d⁵ | なし | 1NN（+任意で 2NN 陰イオン間）| ZnS,ZnSe,ZnTe,CdS,CdSe,CdTe,HgS,HgSe,HgTe（II-VI 9種）| Table I, II | **LMTO（DFT/ASA）band に fit** | **結合長 d を付属**（例 ZnS 2.34Å）| ◎ 可（パラメータ＋距離＋Hamiltonian 明記; SOC 無し）|
| E | **Viswanatha, Sapra, Saha-Dasgupta, Sarma, PRB 72, 045333 (2005)** | 閃亜鉛鉱 | III-V: 陽イオン sp³ / 陰イオン sp³d⁵（GaN は逆）; II-VI: 両 sp³d⁵ | なし | 1NN + 2NN（陽-陽・陰-陰）| III-V: AlP,AlAs,AlSb,GaN,GaP,GaAs,GaSb,InP,InAs / II-VI: ZnS,ZnSe,ZnTe,CdS,CdSe,CdTe | Table I, II | **FP-LAPW（LDA）band に fit**（gap 過小）| 無し | ○ 可（格子定数を外部調達; σ/π ラベルが抽出で混在→要再確認）|
| F | **Tuncay, Tomak, phys. stat. sol. (b) 127, 543 (1985)** | ウルツ鉱 | sp³ | なし | 1NN 型 | SiC, ZnSe, ZnTe（wz）| Table 1（ただし抽出で**行ラベル欠落**）| 経験的（zincblende からスケール, Vogl 則）| 数値なし | ✗→△ 要 PDF 表の再確認（記号-値対応が抽出不能）|
| G | **Laref, Sekkal, Laref, Luo, JAP 104, 033103 (2008)** | ウルツ鉱 | sp³s\* | なし | 1NN | ZnSe, Si（wz）| Table I | on-site=HF 原子値, hopping=GW band に fit | 無し（格子不整合 4.25% のみ）| △ bulk param あり（一部抽出乱れ要確認, 格子定数要）|

凡例: ◎ 高（パラメータ自己完結に近い）, ○ 可（標準 Hamiltonian＋格子定数を補えば可）, △ 条件付き（再確認・外部値が必要）。

**コードベースとの整合**: 既存 `slater_koster.py`（二中心積分）と `models_nestoklon.py`（sp³/sp³d⁵s\* の閃亜鉛鉱型 + SOC）が既にあるため、**B/C/D/E（ダイヤモンド・閃亜鉛鉱）は既存 SK エンジンを再利用して比較的容易**。ウルツ鉱（A/F/G）は4原子/セルの新しい結晶構造ジオメトリ実装が必要。

---

## 2. 本フォルダに無いが重要な一次パラメータ源（複数の応用論文が参照）

実装の際に取得を検討すべき原典（**本フォルダには PDF が無い**＝現時点で内容は未確認・要収集）:

| 文献 | 内容（参照論文の記述より）| 用途 |
|---|---|---|
| **Vogl, Hjalmarson, Dow, J. Phys. Chem. Solids 44, 365 (1983)** | sp³s\*, 12 種の四面体半導体 | 閃亜鉛鉱/ダイヤ sp³s\* の古典的標準源（Persson, レビュー Goringe が言及）|
| Jenkins, Dow, PRB 39, 3317 (1989) | GaN sp³s\* | Niwa が GaN params に使用 |
| Yang, Nakajima, Sakai, JJAP 34, 5913 (1995) | wz GaN/InN の h_llm | Jogai が参照（＝下記スキャン論文 5912 と隣接）|
| Caro, Schulz, O'Reilly, PRB 88, 214103 (2013) | wz sp³, **HSE-DFT に fit** | Schulz 2015 の TB params 本体 |

> これらは「記憶で値を書かない」。実装段階で原典 PDF を入手し精読してから採用する。

---

## 3. 応用 / 手法 / 歪みモデル論文（パラメータ源ではないが有用）

| 文献 | 種別 | 有用な点 |
|---|---|---|
| Jogai, PRB 57, 2382 (1998) | 応用（wz GaN 歪み）| sp³d⁵/sp³ の歪み手法; params は Yang 1995 |
| Niwa, APL 70, 2159 (1997) | 応用（wz GaN/AlGaN QW, SOC）| c/a, u, GaN a=3.18/c=5.17Å, 弾性定数 |
| Baer, APL 87, 231114 (2005) | 応用（wz InN/GaN QD）| params は bulk band に fit（非掲載）|
| Schulz, PRB 92, 235419 (2015) | 応用（wz InGaN/GaN QW）| params は Caro 2013（HSE-DFT fit）|
| Persson, Xu, PRB 70, 161310 (2004) | 応用（InP NW）| params は Vogl 1983 |
| Santoprete, PRB 68, 235311 (2003) | 応用＋**歪み recipe**（InAs/GaAs QD）| sp³s\* 2NN+SOC; 歪みは hopping を d⁻ⁿ（n=3.40, DFT-LAPW に fit）; **格子定数 GaAs 5.653/InAs 6.055Å** |
| Marquardt, PRB 78, 235302 (2008) | 手法比較（cubic GaN/AlN QD）| **k·p 入力**（cubic GaN a=4.5/AlN a=4.38Å, Eg, γ, Δso）; SK 表は無し |
| Béré, PRB 71, 125211 (2005) | DFTB（GaN 粒界）| SCC-DFTB（経験的 SK 表ではない）|
| Pedersen, PRB 63, 201101 (2001) | 手法（光学行列要素）| p→(m0/ℏ)∇_k H + 原子内補正 |
| Mönch, JAP 80, 5076 (1996) | branch-point（多数材料）| Harrison universal（独自 SK 表は無し）|
| **Camacho, Niquet（KeatingWZ）, Physica E 42, 1361 (2010)** | 歪み VFF | **wz 窒化物の格子定数 a,c,u ＋ VFF 力定数**（GaN a=3.189/c=5.185/u=0.3768 等）— 歪み・原子位置生成に有用 |
| Goringe, Bowler, Hernández, Rep. Prog. Phys. 60, 1447 (1997) | レビュー | TB パラメータ源の道標（Vogl 1983 等）|

---

## 4. スキャン画像（OCR 必須・現状内容未確認）

以下は**全ページ画像で本文テキスト抽出不可**。パラメータを推測しない（no-hallucination）。実装に使うなら OCR か別ソース取得が必要:

| ファイル | 推定（表紙/文脈のみ; 本文未確認）|
|---|---|
| `1347-4065_34_11R_5912.pdf` / `JJAP-34-5912.pdf` | 表紙: "Electronic Structures of Wurtzite GaN, InN and Ga₁₋ₓInₓN, Tight-Binding, JJAP 34, 5912 (1995)"（本文画像）|
| `PhysRevB[1].16.790.pdf` | PRB 16, 790（応用論文が SOC 形式で Chadi 1977 を引用; 本文未確認）|
| `PhysRevB[1].18.1780.pdf` | PRB 18, 1780（本文未確認）|
| `PhysRevB[1].47.15500.pdf` | PRB 47, 15500（本文未確認）|
| `PhysRevB[1].49.2121.pdf` | PRB 49, 2121（本文未確認）|
| `p4940_1.pdf` | 本文未確認 |

（`.ppt` 2本は発表資料のため対象外。）

---

## 5. 推奨実装順（実現性・コード再利用性で）

1. **II-VI 閃亜鉛鉱（Sapra, PRB 66, 205202）** — sp³d⁵, パラメータ＋結合長が自己完結, Hamiltonian 明記。SOC 無しだが最も confident。
2. **III-V 閃亜鉛鉱（Boykin, PRB 56, 9613, sp³s\*+SOC 2NN / または Viswanatha 72,045333）** — 既存 SK エンジン再利用。格子定数を cited 値で補う。
3. **Si/Ge ダイヤモンド（Boykin, PRB 69, 115201, sp³d⁵s\*+SOC）** — Nestoklon の sp³d⁵s\* 機構を流用。
4. **ウルツ鉱（Kobayashi 28,935 / 要 Yang1995 OCR）** — 4原子/セルの新ジオメトリ実装が必要（後回し）。

各実装で**不足する格子定数は cited 一次出典から補い**（Madelung 等; §3 の値も活用可）、採用 SK 表は **OCR/抽出乱れがある箇所を PDF 原図と突き合わせて検証**してから JSON 化する。

---

## 6. 提案：構造化入力スキーマ（実装時; 不正な組み合わせを弾く）

ユーザ要望（結晶系 / 基底軌道 / 材料(文献ごとの TB パラメータ・格子定数) / 来歴）に沿った JSON 構造案:

```jsonc
{
  "model_id": "sapra2002_II-VI_sp3d5",
  "crystal_system": "zincblende",          // 許容: diamond|zincblende|wurtzite|rocksalt...
  "basis": {"orbitals": "sp3d5", "spin_orbit": false},
  "neighbor_range": "1NN+2NN_anion",
  "reference": {
    "citation": "Sapra, Shanthi, Sarma, PRB 66, 205202 (2002)",
    "doi": "10.1103/PhysRevB.66.205202",
    "param_source": "Table I/II",
    "estimation_method": "fit to LMTO (DFT, ASA) band dispersions"   // DFT/GW/experiment 等を必須記載
  },
  "materials": {
    "ZnS": {
      "lattice_constant_A": null,           // 値 or 出典付き; 無ければ null + lattice_source
      "nn_distance_A": 2.34,                 // 論文掲載
      "lattice_source": "…(cited)",
      "params_eV": { "E_s_c": "...", "V_sssigma": "..." }   // SK 記号で
    }
  }
}
```

**妥当性検証ルール（不正な組み合わせで動かさない）案**:
- `crystal_system` と `basis.orbitals` と `materials[*].params` の整合（例: ウルツ鉱に閃亜鉛鉱用 param を渡したらエラー）。
- 必須キー（結晶系・基底・近接範囲・各材料の SK パラメータ・格子定数 or 結合長）が揃わなければ計算前に reject。
- `reference.estimation_method` 未記載は reject（来歴必須）。
- スキーマ JSON は `data/parameters/` に置き、ローダ（`io_params`）でバリデーション。

---

**(EOF)** — 全記述は `references/pdfs/Tight_Binding/` の原典本文から抽出（ページ引用は各サブ抽出ログに準拠）。スキャン7本は OCR 未実施のため内容未確認としてフラグ。次段: 実装着手前に §5 の優先材料について SK 表を PDF 原図と突き合わせ検証＋格子定数の cited 値を確定。
