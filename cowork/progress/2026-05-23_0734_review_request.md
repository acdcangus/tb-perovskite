# Code Review Request: 2026-05-23 07:34

- **対象:**
  - `src/perovskite_tb/velocity.py` (commit 354e5be) — 解析的 `dH/dk`
  - `src/perovskite_tb/g_factor.py` (commit 354e5be) — Roth-Lax atomistic g因子 + k·p 公式
  - `docs/g-factor-formulation.md` §3, §8（定式化と A2 結果）
- **急ぎ度:** 通常（A4 スキャン着手前に方針確認したい）

## 観点（physics 検証をお願いしたい）

### Q1【最重要・Roth-Lax の intra-atomic 項】
atomistic Roth-Lax（TB `∂H/∂k` から軌道モーメントを構成）で CsPbI₃ の
**|g_e| が Table S2 を大きく下回る（本実装 +1.06 vs Nestoklon Table S2 +3.23）**。
立方等方性は厳密（1e-15）、速度行列要素も十分大（|⟨CBM|∂_zH|VBM⟩|=2.97 eV·Å）。
- 仮説: オンサイト SOC が k 非依存 → `∂H/∂k` に **原子内軌道角運動量**が入らない
  （intra-atomic current / 不完全基底問題）。
- **依頼:** TB で g因子を正しく出す標準手順を確認したい。具体的には
  (a) 速度演算子に原子内項 `v → v + (i/ℏ)[H_onsite, r_intra]` を加えるべきか、
  (b) Roth-Lax の代わりに **Peierls+Zeeman を磁場超格子**で回すのが本筋か、
  (c) Nestoklon の bulk ETB g因子の具体式（論文 Ref.9 = arXiv 1902.06646 か Nat.Commun. の SI）
      の手続きを紙で展開して、本実装の落とし方が合っているか確認いただけるか。

### Q2【パラメータ入手依頼】
Nestoklon 2023 Table S2 を厳密再現するベースは **M. Nestoklon, Comput. Mater. Sci. 196,
110535 (2021)**（arXiv:2012.14705 のジャーナル版、CsPbX₃ 全ハライドの sp³d⁵s\* パラメータ）。
リポジトリには CsPbI₃ のみ。**Br/Cl のベースパラメータ**（および Table S1 の修正適用後の完全表）が
あると、A4 で 3 ハライドの g因子を厳密検証できる。Cowork 側で入手可能か（OpenAlex / 出版社 OA）。

### Q3【方法方針の承認】
directive A2 の「Roth-Lax」を主軸にしつつ、絶対値が未決着の間は **A4 の 9材料スキャンを
k·p 公式（材料ごとに計算した Eg, Δ ＋ 普遍 P=6.8, Δg_e=−1）主体**で進める方針で良いか。
ただし**現実的な Eg が全9材料で必要**（Kashikar の mBJ Eg は小さすぎる; CsPbI₃=0.63 eV など）。
→ Sn/Ge 系の現実的 Eg をどう用意するか（Q2 のパラメータ入手 or 実験 Eg の文献値採用）も相談したい。

## 添付・根拠
- 数値: `docs/g-factor-formulation.md` §8 の比較表。
- テスト: `tests/test_velocity.py`(21), `tests/test_g_factor.py`(5) 全通過、既存163本維持（計189）。
- k·p 公式は anchor 再現（g_e: 計算 Eg,Δ で +3.24 vs Table S2 +3.23）。

## 追試結果（intra-atomic L を加えてみた）
オンサイト軌道角運動量項（SOC と同じ L 演算子を p 軌道に、`onsite_L_operators`）を Zeeman 行列に
加法追加した結果：**g_e は +1.06→+2.27（target +3.23 へ改善）だが g_h は +0.45→+0.67（target −0.33 と逆）**。
→ 単一欠落項では決着せず、inter/intra の符号・準縮退多重項の摂動論を含む総合的定式化が必要と判断。
**これ以上の単独推測はハルシネーション risk のため停止**（directive ルール5/30分ルールに従う）。
intra-L 項は物理的に正しいのでオプション実装として残置（default off, 既存テストに影響なし）。

## 私の次アクション（Cowork 回答待ち）
- **本サブタスク（atomistic g因子の絶対値決着）は一旦停止**し、Cowork の式検証（Q1）と
  パラメータ入手（Q2）・方針承認（Q3）を待つ。
- 回答が来たら: (Q1) 正しい定式化を実装→CsPbI₃ で 3.23/−0.33 を再現できるか確認、
  (Q3 OK なら) k·p 主体で A4 の 9材料スキャンに着手。
- それまでに安全に進められる範囲（k·p 経路での A4 試作、現実的 Eg の文献値整理）は検討するが、
  物理の未決着部分には踏み込まない。
