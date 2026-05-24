# tasklist — 追加検証タスク（09）

## DOI 事前検証（サイクルA）✅
- [x] Blancon「Scaling law」= **Nat. Commun. 9, 2254 (2018)**（09の Science 355,1288/10.1126/science.aal4211 は edge-states 別論文＝訂正）
- [x] Buin 2014 (Nano Lett. 14, 6281) = **trap-free 合成**（歪み無関係）→ 削除
- [x] Grumet PRB 98,155143 (2018) = **GW 手法論文**（crossref 確認, 歪み無関係）→ 削除
- [x] Pieniazek 2023 (JPCL 14,6470)・Liu 2023 (Molecules 28,7643)・Bhumla 2021 (arXiv:2108.03683)・Fu-Kane(PRB76,045302)・Fu-Kane-Mele(PRL98,106803) 検証

## 実装・V&V ✅
- [x] **T1-1 F5**: `bandstructure`不要; `test_blancon_layer_dependence`（p_TB≈0.93 vs p_exp≈0.85, 15%以内）; 図 blancon_E_g_n.png; benchmark JSON。**C→B**
- [x] **T1-2 F12**: `bandengr.pressure_coefficient`; `test_strain_gap_sensitivity_lit`（符号一致C / 大きさ~5-16×過大D）; strain_benchmark.json
- [x] **T1-3 F6**: `bandstructure.effective_mass`（全9材料 m*, results/tb_effective_masses.json）; CsPbBr₃ TB駆動 α=1.66; test_polaron 7→10。**A公式/B**
- [x] **T2-1 F4**: `test_bulk_dft_comparison`（CBM>VBM順序C / 絶対~40×小D）; rashba_bulk_benchmark.json; test_rashba 8→9
- [x] **T2-2 F1/F2**: `topology.parity_delta_at_trim`/`z2_invariant_from_parities`; Wilson-Dirac 相図再現; Berry符号反転; test_topology 12→18。**B**「未実装」解消
- [x] **T2-3 F14-B**: `polarization.ferroelectric_polarization_difference`; ΔP符号反転+DFTと同オーダ; polarization_fe_benchmark.json; test_polarization 4→6。**C→B**
- [x] **T2-4 F11**: `edelstein.longitudinal_conductivity`/`edelstein_ratio`; χ/σ=mα/(4μ) 15%以内; test_edelstein 4→6。**B**

## docs（CLAUDE.md）✅
- [x] `docs/numerical-methods.md` §10/§12/§13/§15/§16/§17 更新
- [x] `extention/08_validation_status_quantitative.md` §7（マトリックス更新・引用訂正）
- [x] `extention/08_tb-perovskite_implementation_report.md` §7（タスク別詳細）
- [x] `extention/10_additional_features_report.md`（ユーザ向け解説・検証レポート）

## 完了条件 ✅
- [x] 全 **330 テスト pass**（314 + 新規16）, 既存不変
- [x] 新規引用 DOI 全件 web/crossref 検証済
- [x] commit/push: 7eef9b5(T1-1), b8baaca(T1-3), a4f1fc1(T1-2), 591b3a9(T2-2), 163d8d1(T2-4), be6dcc0(T2-1), 251140f(T2-3), c38899b/860cd3d(docs), 0c83a13(report10)

## honest 結論
真のA(論文値%)は polaron α・WF・Weyl 量子化。多くは SK-TB/Blount で B/C/D 維持（捏造回避）。9材料αマップは Cs系無機の誘電データ非存在で部分。
