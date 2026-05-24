# requirements — F1 Berry curvature コア → AHC / SHC

**発行元:** `extention/03_tb-perovskite_spec.md` F1（★★★, Phase A）+ `extention/07_agent_handoff.md`
**日付:** 2026-05-24
**作業ブランチ方針:** main で逐次 commit（PI 監視）

## 背景・目的
既存の velocity operator (`velocity.py`) を使い、Berry curvature Ω(k) を計算するコア基盤 `berry.py` を新設し、その上に
anomalous Hall conductivity (AHC) と spin Hall conductivity (SHC) を構築する。立方 CsBX₃ は空間反転 P と時間反転 T を
ともに持つため Ω(k)=0（→ AHC=0）だが、スピン Berry 曲率は非ゼロ可（→ SHC≠0 が許される）。

## スコープ（本作業）
- **実施:** F1 のみ（Berry curvature コア + AHC + SHC + 離散 Chern）。paper-quality（解析解 V&V 付き）。
- **保留（roadmap 化）:** F2–F14。理由 = 14 機能は数ヶ月規模。F1 は handoff の最優先 Phase A で、全引用が実在確認済み、解析 V&V が明快。berry.py の離散 Chern/Wilson 基盤は将来 F2（topology）が再利用可。

## 引用文献（**全て実在確認済み 2026-05-24, web 検証**）
| 文献 | 用途 | 確認 |
|---|---|---|
| Xiao, Chang, Niu, RMP 82, 1959 (2010), DOI 10.1103/RevModPhys.82.1959 (arXiv:0907.2021) | Berry 曲率 Kubo 公式 **Eq. (1.13)**（原典 ar5iv で式を確認） | ✅ |
| Fukui, Hatsugai, Suzuki, JPSJ 74, 1674 (2005), DOI 10.1143/JPSJ.74.1674 (arXiv:cond-mat/0503172) | 離散 BZ link 変数法（gauge 不変・整数 Chern） | ✅ |
| Sinova, Valenzuela, Wunderlich, Back, Jungwirth, RMP 87, 1213 (2015), DOI 10.1103/RevModPhys.87.1213 (arXiv:1411.3249) | SHC・スピン流演算子 j^z_α=½{s_z,v_α} | ✅ |
| Qi, Wu, Zhang, PRB 74, 085308 (2006), DOI 10.1103/PhysRevB.74.085308 (arXiv:cond-mat/0505308) | テスト模型（QWZ Chern 絶縁体, 整数 Chern 検証） | ✅ |

ハルシネーション防止: 上記以外の式・数値は使わない。本仕様の TB 部は既存 in-repo（Kashikar arXiv:2101.08562）に依拠。

## 受け入れ条件（CLAUDE.md §共通 Acceptance + spec §6）
1. **解析解一致（unit test, green）**:
   - 質量 Dirac H=d·σ (d=(kx,ky,m)) の下バンド Berry 曲率が **Ω₋(k)=+m/(2(kx²+ky²+m²)^{3/2})**（Xiao 規約, 当方で解析導出）に一致。
   - QWZ 格子 Chern 絶縁体で **整数 Chern**（C=−1 for 0<m<2, +1 for −2<m<0, 0 for |m|>2; Fukui 法）。
2. **対称性（V&V）**:
   - 立方 CsBX₃ (Kashikar-13, SOC on) で一般 k において **Ω(k)=0**（P·T）→ AHC=0 機械精度。
   - Ω は実数、Vα Hermitian。
3. **収束**: Kubo Ω の BZ 積分 ≈ Fukui Chern（gapped 平滑模型での 2 手法相互一致）。
4. **回帰**: 既存 231 テスト不変（berry.py は新規・既存に非侵襲）。
5. **PC スケール**: 立方 9 材料 SHC スキャンは ≤ 数 GB・≤ 1h（本作業ではコア+V&V を優先、9 材料 production scan は任意 follow-up）。

## 制約・honest 記述
- SHC の**絶対値**は in-repo にベンチマーク材料（Pt, Bi₂Se₃）が無いため検証不可 → 既存 shift_current/g_factor と同様に「相対・対称性・構造は信頼、絶対値は要外部ベンチ」と honest に明記。
- TB 位置演算子の Blount 限界（intra-atomic 欠落）は Berry 曲率の絶対値にも効く可能性 → 限界として記載。
