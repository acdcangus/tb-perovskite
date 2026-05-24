# 参考文献索引（PDFと仕様書の対応表）

**作成日**: 2026-05-24

本索引は、`references_pdf/` フォルダの PDF ファイルと、各仕様書中で引用している論文との対応を一覧化したものである。コーディングエージェントはまずここを起点に文献を確認すること。

---

## A. `references_pdf/` に同梱した PDF（D:\Research\Papers\Paper および tb-perovskite/references/pdfs/ から）

| ファイル名 | 出典 | 関連仕様書 |
|---|---|---|
| `Foreman1997_PRB56_R12748.pdf` | B. A. Foreman, PRB 56, R12748 (1997) | QW / QDSL（k·p symmetric ordering）|
| `Burt_EnvelopeFunction.pdf` | M. G. Burt, J. Phys.: Condens. Matter 4, 6651 (1992) | QW / QDSL（envelope function 厳密形）|
| `Burt_Superlattice.pdf` | M. G. Burt, Phys. Rev. B 50, 7518 (1994) | QW / QDSL |
| `8bandHamiltonian_reference.pdf` | k·p 8-band 系総説（出典確認要） | QW / QDSL |
| `Asada1984_IEEE_JQE20_745.pdf` | M. Asada, A. Kameyama, Y. Suematsu, IEEE JQE 20, 745 (1984) | QW（利得式の基礎）|
| `Kotani2014_JAP115_143501.pdf` | T. Kotani et al., JAP 115, 143501 (2014) | **QDSL ベース論文** |
| `Kotani2013_APL102_011128.pdf` | T. Kotani et al., APL 102, 011128 (2013) | **QW ベース論文** |
| `ChowKoch_SemiconductorLaserFundamentals.pdf` | W. W. Chow, S. W. Koch, Springer (1999) | QW F1（多体補正利得 Padé）|
| `Sirtori_QCL.pdf` | C. Sirtori et al.（QCL 関連） | **未使用**（F6 QCL 削除に伴い、参考のみ） |
| `Luque2006_JAP99_094503.pdf` | A. Luque et al., JAP 99, 094503 (2006) | QDSL F8（IBSC）|
| `Luque2012_ProgPhotovolt.pdf` | A. Luque, A. Marti, Prog. Photovolt. 20 (2012) | QDSL F8（IBSC review）|
| `arxiv_2101.08562.pdf` | R. Kashikar et al., arXiv:2101.08562 (2021) | **TB ベース論文** |
| `arxiv_2012.14705.pdf` | M. O. Nestoklon, arXiv:2012.14705 (2021) | **TB ベース論文** |
| `arxiv_1908.09436.pdf` | Y. Cho, T. C. Berkelbach, arXiv:1908.09436 (2019) | TB F3（BSE 励起子）|
| `arxiv_1704.04211.pdf` | Halide perovskite topology 系（出典確認要） | TB F2（トポロジー）|
| `arxiv_1811.11081.pdf` | 同上 | TB F2 |
| `arxiv_2210.01324.pdf` | Halide perovskite nanocrystals 系 | TB F3, F5 |
| `Kopteva2026_arxiv_2605.15807.pdf` | E. A. Kopteva et al., arXiv:2605.15807 (2026) | TB F5（2D RP g-factor 実験）|
| `Nestoklon2023_arxiv_2305.10586.pdf` | M. O. Nestoklon, arXiv:2305.10586 (2023) | TB F5 |
| `Abramovitch2021_polaron_arxiv_2105.06525.pdf` | Abramovitch et al., arXiv:2105.06525 (2021) | TB F6（polaron）|
| `Apergi2023_chiral_arxiv_2309.14002.pdf` | Apergi et al., arXiv:2309.14002 (2023) | TB F7（CPGE, chiral）|
| `classic_Roth1960_PR118_1534.pdf` | L. M. Roth et al., Phys. Rev. 118, 1534 (1960) | QW F4 / QDSL F3（g-factor 古典）|
| `Marti1997_PRL78_5014.pdf` | A. Luque, A. Marti, PRL 78, 5014 (1997) | QDSL F8（IBSC 原典）|
| `Chichibu_Presen.pdf` | S. Chichibu InGaN PL | QW Validation 用 |
| `Mendez1988_PRL60_2426.pdf` | E. E. Mendez et al., PRL 60, 2426 (1988) | **QW F12 (Mode B Wannier–Stark)** |
| `Bleuse1988_PRL60_220.pdf` | J. Bleuse et al., PRL 60, 220 (1988) | **QW F12 (Mode B Wannier–Stark)** |

## B. 仕様書内で参照しているがPDF未同梱の文献

実装エージェントは必要に応じて DOI/arXiv 経由で取得すること。

### B0. 追加機能 F11/F12/F13/F14 系（2026-05-24 追記）

#### QW F11 (QWSL), F12 (DC バイアス)
- L. Esaki, R. Tsu, IBM J. Res. Dev. 14, 61 (1970) — Esaki-Tsu 原典
- F. Capasso, Science 235, 172 (1987) — Band-gap engineering review
- H. T. Grahn, *Semiconductor Superlattices*, World Scientific (1995)
- G. H. Wannier, PR 117, 432 (1960) — Wannier 関数 in field 原典
- E. E. Mendez, F. Agulló-Rueda, J. M. Hong, PRL 60, 2426 (1988) [PDF 同梱]
- J. Bleuse, G. Bastard, P. Voisin, PRL 60, 220 (1988) [PDF 同梱]
- G. Bastard, J. A. Brum, R. Ferreira, Solid State Phys. 44, 229 (1991)
- K. Leo, *High-field transport in semiconductor superlattices*, Springer (2003)

#### QDSL F11 (Berry phase 分極)
- R. D. King-Smith, D. Vanderbilt, PRB 47, 1651 (1993) — KSV 原典
- D. Vanderbilt, R. D. King-Smith, PRB 48, 4442 (1993)
- R. Resta, RMP 66, 899 (1994)
- R. Resta, PRL 80, 1800 (1998)
- R. W. Nunes, X. Gonze, PRB 63, 155107 (2001)
- D. Vanderbilt, *Berry Phases in Electronic Structure Theory*, Cambridge UP (2018)

#### TB F13 (2D RP infinite stack), F14 (Stark slab + Berry bulk)
- D. L. Smith, C. Mailhiot, RMP 62, 173 (1990) — Superlattice TB review
- D. Smith, C. Mailhiot, JAP 62, 2545 (1987) — Type-II SL
- J. Even, L. Pedesseau, C. Katan, JPC C 118, 11566 (2014)
- C. Katan, N. Mercier, J. Even, Chem. Rev. 119, 3140 (2019)
- J.-C. Blancon et al., Science 355, 1288 (2017)
- J. Neugebauer, M. Scheffler, PRB 46, 16067 (1992) — dipole correction
- L. Bengtsson, PRB 59, 12301 (1999) — dipole correction
- P. Umari, A. Pasquarello, PRL 89, 157602 (2002) — finite E field AIMD
- I. Souza, J. Iniguez, D. Vanderbilt, PRL 89, 117602 (2002)

### B1. QW 関連
- L. C. Andreani, A. Pasquarello, PRB 42, 8928 (1990) — Andreani 励起子
- C. Bauer et al., PRB 96, 245206 (2017) — many-body laser theory
- A. R. Beattie, P. T. Landsberg, Proc. R. Soc. A 249, 16 (1959) — Auger 原典
- B. A. Bernevig et al., Science 314, 1757 (2006) — BHZ
- C. E. Pryor, M. E. Flatté, PRL 96, 026804 (2006) — g-tensor k·p
- R. Vaxenburg et al., Nano Lett. 16, 2503 (2016) — Auger in nanocrystals
- L. Fu, C. L. Kane, PRB 76, 045302 (2007) — Z₂ parity
- R. Yu et al., PRB 84, 075119 (2011) — Wilson loop
- S. Klembt et al., Nature 562, 552 (2018) — topological polariton
- F. H. Julien et al., Sci. Rep. 2, 654 (2012) — GaN ISB
- M. König et al., Science 318, 766 (2007) — HgTe QSH 実験
- C. Liu et al., PRL 100, 236601 (2008) — InAs/GaSb QSH 理論
- B. Krummheuer, V. M. Axt, T. Kuhn, PRB 65, 195313 (2002) — exciton-phonon
- R. Winkler, PRB 51, 14395 (1995) — 2D exciton with VB mixing
- ~~J. Faist, *Quantum Cascade Lasers*, Oxford (2013)~~ — F6 QCL 削除に伴い不要

### B2. QDSL 関連
- M. Bayer et al., PRB 65, 195315 (2002) — FSS
- A. Schliwa et al., PRB 79, 075443 (2009) — CI multi-exciton
- T. Takagahara, PRB 62, 16840 (2000) — exchange anisotropy
- G. Bester, S. Nair, A. Zunger, PRB 67, 161306(R) (2003) — FSS atomistic
- R. Trotta et al., Nat. Commun. 7, 10375 (2016) — strain-tuned FSS
- D. Huber et al., PRL 121, 033902 (2018) — entangled photon
- D. A. B. Miller et al., PRB 32, 1043 (1985) — QCSE 原典
- F. Findeis et al., APL 78, 2958 (2001); P. W. Fry et al., PRL 84, 733 (2000) — QD QCSE
- T. Takagahara, PRB 60, 2638 (1999) — phonon coupling exciton
- A. Reigue et al., PRL 118, 233602 (2017) — single QD T2
- S. Tomic et al., APL 93, 263105 (2008); M. Y. Levy, C. Honsberg, PRB 78, 165122 (2008) — IBSC
- A. Luque, A. Marti, PRL 78, 5014 (1997) — detailed balance IBSC
- J. D. Plumhof et al., PRB 83, 121302(R) (2011) — strain tuning
- F. Ding et al., PRL 104, 067405 (2010) — strain tuning
- J.-M. Gérard et al., PRL 81, 1110 (1998) — Purcell QD
- P. Senellart et al., Nat. Nanotech. 12, 1026 (2017) — review
- C. E. Pryor, M. E. Flatté, PRL 96, 026804 (2006) — g-tensor
- T. Andlauer, P. Vogl, PRB 79, 045307 (2009) — g-tensor QD
- M. Grundmann, D. Bimberg, PRB 55, 9740 (1997) — carrier capture QD
- T. R. Nielsen et al., PRB 69, 235314 (2004) — relaxation

### B3. TB Perovskite 関連
- D. Xiao, M.-C. Chang, Q. Niu, RMP 82, 1959 (2010)
- T. Fukui, Y. Hatsugai, H. Suzuki, JPSJ 74, 1674 (2005)
- J. Sinova et al., RMP 87, 1213 (2015)
- Y. Yao et al., PRL 92, 037204 (2004)
- A. A. Soluyanov, D. Vanderbilt, PRB 83, 235401 (2011)
- H. Jin et al., PRB 86, 121102(R) (2012)
- G. Onida, L. Reining, A. Rubio, RMP 74, 601 (2002)
- M. R. Filip, F. Giustino, PRB 90, 245145 (2014)
- G. Cappellini et al., PRB 47, 9892 (1993)
- D. Niesner et al., PRL 117, 126401 (2016)
- M. Kim et al., PNAS 111, 6900 (2014)
- F. Zheng et al., Nano Lett. 15, 7794 (2015)
- J.-C. Blancon et al., Science 355, 1288 (2017)
- C. Katan, N. Mercier, J. Even, Chem. Rev. 119, 3140 (2019)
- J. Even, L. Pedesseau, C. Katan, J. Phys. Chem. C 118, 11566 (2014)
- H. Fröhlich, Adv. Phys. 3, 325 (1954)
- R. P. Feynman et al., Phys. Rev. 127, 1004 (1962)
- R. W. Hellwarth, I. Biaggio, PRB 60, 299 (1999)
- J. M. Frost, PRB 96, 195202 (2017)
- F. Giustino, RMP 89, 015003 (2017)
- F. de Juan et al., Nat. Commun. 8, 15995 (2017)
- J. E. Sipe, A. I. Shkrebtii, PRB 61, 5337 (2000)
- E. Ghahramani, D. J. Moss, J. E. Sipe, PRB 43, 9700 (1991)
- C. Aversa, J. E. Sipe, PRB 52, 14636 (1995)
- L. Z. Tan et al., npj Comput. Mater. 2, 16026 (2016)
- G. K. H. Madsen, D. J. Singh, CPC 175, 67 (2006)
- L. D. Whalley et al., APL Mater. 4, 091502 (2016)
- ~~T. Whalley et al., PRB 95, 094112 (2017)~~ — TB F10 削除に伴い不要
- ~~J. Lahnsteiner, M. Bokdam, PRB 102, 134314 (2020)~~ — TB F10 削除に伴い不要
- ~~M. Zacharias, F. Giustino, PRB 94, 075125 (2016)~~ — TB F10 削除に伴い不要
- V. M. Edelstein, SSC 73, 233 (1990)
- J. C. R. Sánchez et al., Nat. Commun. 4, 2944 (2013)
- A. Buin et al., Nano Lett. 14, 6281 (2014)
- M. Grumet et al., PRB 98, 155143 (2018)
- G. L. Bir, G. E. Pikus, *Symmetry and Strain-Induced Effects*, Wiley (1974)

## C. 未検証文献の取扱い

下記は仕様書で引用したが、DOI/年/著者の組合せが完全には確認できていないもの。実装エージェントは着手前に確認すること（**ハルシネーション防止のため必須**）。

- W. Schwan et al., PRB 84, 161310(R) (2011) — 出典確認要
- T. Stranski et al., PRL 103, 257402 (2009) — 出典確認要
- A. Mohan et al., Nat. Photonics 4, 302 (2010) — 出典確認要
- 一部の文献はタイトル・年が「主要文献として一般的に知られる範囲」であり、実装前に追加検証を推奨

## D. 文献追加が望ましい領域

実装エージェントが進める際に、不足を感じたら以下も追加候補：

- 量子井戸ポラリトン: A. Imamoglu et al., PRA 53, 4250 (1996)
- exciton-polariton condensation: J. Kasprzak et al., Nature 443, 409 (2006)
- 2D moiré in perovskite: 最新2025–2026
- Topological insulator k·p model: H. Zhang et al., Nat. Phys. 5, 438 (2009)
