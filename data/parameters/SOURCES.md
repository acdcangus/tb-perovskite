# パラメータの出典 (SOURCES)

このフォルダの各 JSON は、査読論文 / arXiv プレプリントの **表をそのまま転記**したものです。
転記方針は「**論文に印字された値をそのまま**記録する」こと。明らかな誤植が疑われる場合も
値は改変せず、各 JSON の `anomaly` フィールドに注記します（**ハルシネーション防止**）。

すべての元論文 PDF は `references/pdfs/arxiv_<id>.pdf`、一覧は `references/references.md`。

---

## kashikar2021_cubic_13orb.json / kashikar2021_cubic_4orb.json

- **出典:** R. Kashikar, M. Gupta, B. R. K. Nanda,
  "A Generic Slater-Koster Description of the Electronic Structure of Centrosymmetric
  Halide Perovskites", arXiv:2101.08562 (v1, 2021-01-21).
- **転記元:** Table II（13軌道モデル）, Table IV（4軌道最小モデル）, Table I（格子定数）。
- **DFT 基準:** PBE-GGA + Tran-Blaha mBJ ポテンシャル。
- **モデル式:** 本文 Eq.(1)-(8)。R 点の固有値の解析式は Eq.(9)。
- **検証アンカー:** 13軌道ハミルトニアンを R = (π/a,π/a,π/a) で対角化した固有値が、
  Eq.(9) の解析式（SOC なし）と一致すること。これは構築の厳密な自己無撞着チェック。
  - Eq.(9): `E1=(EXp+EBs)/2 - 3*tss - eta`, `E2=EXp (8重縮退)`,
    `E3=EBp - 2*tppσ - 4*tppπ (3重縮退)`, `E4=(EXp+EBs)/2 - 3*tss + eta`,
    `eta = sqrt((EXp-EBs+6*tss)^2 + 48*tsp^2)/2`。
- **誤植注記:**
  - `CsGeI3` の `t_BX_sp` が +1.00（他は全て負, -0.94〜-1.29）。符号の誤植の可能性。
  - `CsPbI3` の `t_BB_ss`(+0.01) と `t_BB_spsigma`(+0.12) が、他の Pb 化合物
    （Cl: -0.03,-0.13 / Br: -0.02,-0.12）と符号が逆。誤植の可能性。
  - いずれも**値は改変せず**転記。Eq.(9) 検証はパラメータ値に依らず成立するため、
    これらの注記は物理的妥当性に関する注意であり、実装の正しさの検証には影響しない。

## nestoklon2021_CsPbI3.json

- **出典:** M. O. Nestoklon, "Tight-binding description of inorganic lead halide
  perovskites in cubic phase", arXiv:2012.14705 (v2, 2021-01-06).
- **転記元:** Table I（sp3 / sp3d5s* / 実験補正 の3パラメータセット）。
- **手法:** Jancu-Scholz-Beltram-Bassani の sp3d5s* 最近接 Slater-Koster
  (Phys. Rev. B 57, 6493 (1998))。Cs は基底から除外、cation c=Pb / anion a=I のみ。
- **DFT 基準:** WIEN2k + 修正 Becke-Johnson (Tran-Blaha) / Jishi パラメータ化。
- **格子定数:** a = 6.289 Å。
- **検証アンカー（本文に明示された数値）:**
  - DFT バンドギャップ（R点）= **1.017 eV**（Sec. II）。
  - 実験補正ギャップ: R点 = **1.65 eV**, M点 = **2.75 eV**（Sec. V）。
  - 伝導帯の SO 分裂（R点）= **1.48 eV**（Sec. V）。
  - 実験ピーク: 1.65 (R), 2.75 (M), 3.40 (X) eV（Yuan et al., ref.35）。
- **零に固定される積分:** `s*s*σ = sc_s*a_σ = s*a_dc_σ = pc_da_σ = pa_dc_π = pc_da_π = 0`
  （Table I キャプション）。

---

## 補助文献（未実装・参考）

- S. Ashhab et al., "Effect of disorder on transport properties in a tight-binding model
  for lead halide perovskites", arXiv:1703.03574 — 鉛ハライドペロブスカイトの TB モデル。
- 破損ダウンロード（後日再取得して確認予定）:
  arxiv_2209.13267 / arxiv_2302.13773 / arxiv_2501.06503。
  特に 2501.06503（DFT-leveraged TB insights into inorganic halide perovskites）は要確認。
