# 拡張機能タスク サマリ — F1–F14 評価と実装結果 — Claude Code — 2026-05-24 16:35

PI 依頼「`extention/` 仕様を熟読・検討し、拡張可能なら実装（標準ルール・ハルシネーション厳禁・
文献欠落ならスキップ可・承認不要で完了まで）」への最終サマリ。**全 14 機能を評価**し、
**paper-quality + フル V&V + 引用実在確認** を満たせる 2 機能を実装、残りは具体的理由付きで保留。

## 実装済み（this session, push 済）
| 機能 | 成果 | V&V | commit |
|---|---|---|---|
| **F1 Berry 曲率 → AHC/SHC/Chern** | `berry.py` + 22 テスト + docs §9 | Dirac 解析一致 / QWZ 整数 Chern / Kubo↔Fukui / 立方 AHC=0 (~1e-15) | `24fa03a` |
| **F2 (部分) Wilson ループ/WCC** | `topology.py` + 12 テスト + docs §10 | Wilson Chern == Fukui Chern（2 独立手法）/ QWZ 相図 / gauge 不変 | `981f1f8` |

全テスト **265 passed**（既存 231 不変 + 新規 34）。引用 6 件すべて web で実在確認
（Xiao2010 / Fukui2005 / Sinova2015 / QWZ2006 / Yu2011 / SoluyanovVanderbilt2011）。記憶ベースの式・数値ゼロ。

## 保留（理由付き — 推測せずスキップ, PI 指示準拠）
| 機能 | 判定 | 理由・必要な前提 |
|---|---|---|
| F2 残（Fu-Kane parity Z₂） | **要文献** | Kashikar 基底の**空間反転演算子の表現**が in-repo で未確定 → 推測=捏造リスク。一次文献で確定後に実装。 |
| F2 残（時間反転 Z₂, partner switching） | **要検証模型** | 手法は実装可だが**既知 3D-Z₂ 参照模型**が無く検証不能 → 保留。 |
| F3 BSE 励起子 | **大規模** | 4–6 週。TB 基底 Coulomb 行列 + model dielectric (Cappellini 1993)。引用は実在(Onida2002/Filip2014/Cho2019)。MAPbI₃ E_b 検証は別材料要。 |
| F4 Rashba | **検証 anchor 弱** | 既存 polar builder 再利用で実装可・立方→α_R=0 は厳密検証可。だが絶対値の文献 anchor は「表面 α_R」で本実装(bulk polar)と幾何不一致 → novelty を主張するには anchor 要再選定。 |
| F5 2D RP slab | **大規模** | slab 構築 + passivation。Kopteva2026 PDF は in-repo。 |
| F6 Polaron 移動度 | **データ要収集** | 材料ごとの ω_LO・ε_s・ε_∞ 文献値が必要（記憶で入れると捏造）→ 一次収集後。Frost2017 MAPbI₃ μ~100 検証も別材料。 |
| F7 CPGE / F8 SHG | 実装可 | shift_current/optical 拡張。優先後段。 |
| F9 熱電 / F11 Edelstein / F12 strain | 実装可/一部データ要 | F9/F11 は velocity・berry 再利用可。F12 は変形ポテンシャル文献値要。 |
| F13 2D RP stack / F14 電場 | F5 依存 | F14 の bulk Berry 位相 (KSV1993) は topology.py の Wilson/分極を一部再利用可。 |

## 方針の根拠
F1–F14 は spec 自身が「数ヶ月規模ロードマップ」と明記。1 セッションで全機能を paper-quality + 無捏造で
完遂は不可能。よって handoff 最優先 Phase A/B（F1, F2）を**完全実装**し、残りは**着手前提（文献/データ/検証模型）を
明示**した。各保留機能は前提が満たされ次第、同じ規律（引用 DOI を web 検証 → 解析/既知模型で V&V → docs/steering）で実装可能。

## CLAUDE.md 準拠
- `.steering/20260524-berry-curvature-shc/`, `.steering/20260524-topology-wilson-loop/`（requirements/design/tasklist）。
- `docs/numerical-methods.md` §9・§10、`docs/repository-structure.md` 更新。
- honest 限界記述（SHC 絶対値はベンチ材料無く未検証 + Blount 限界）を spec の流儀（既存 g_factor/shift_current）と統一。
