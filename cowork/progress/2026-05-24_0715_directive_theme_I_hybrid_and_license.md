# Directive — Theme I hybrid (a)+(c) Production + LICENSE 追加

**発行元:** Cowork supervisor（PI 起床判断に基づく）
**発行時刻:** 2026-05-24 07:15 JST (22:15 UTC, 5/23)
**対象 commit:** `f35208d`（5 分巡回ループ導入直後）
**背景:** PI 判断 2 件到着 — (iii) Theme I は (a)+(c) ハイブリッド OK、(ii) LICENSE は無料ライセンスなら追加 OK。
**残る open question:** (i) `claude --continue` 動作検証 + 巡回トークンコスト最適化（別 directive で対応予定、本 directive とは独立）

---

## 1. Task Y1: Theme I hybrid Production 化

### Y1-a: 有効質量マップ Production 化

**目的:** TB 由来で完結する信頼可な物理量（m_e, m_h, μ）を 9 材料で Production bundle 化。

**スクリプト:** `scripts/scan_theme_I_effective_mass.py`（新規）

**仕様:**
- 9 材料スキャン: CsBX₃, B ∈ {Pb, Sn, Ge}, X ∈ {Cl, Br, I}
- 既存 `src/perovskite_tb/exciton.py::effective_mass` を呼び出し
- **収束テスト**（PRODUCTION_RULES §1）:
  - `n_kpts ∈ {6, 8, 12, 16}` で R 点中央差分の安定性
  - `dk` step variation（例: dk × 0.5, 1.0, 2.0）で 2 次差分の数値安定性
  - 結果を `convergence/` に CSV + プロット保存
- **出力**:
  - `outputs/raw/effective_masses_9materials.csv`: 材料 / m_e_x / m_e_y / m_e_z / m_e_avg / m_h_{xyz,avg} / μ / 異方性比
  - `outputs/figures/effective_mass_summary.png`: trend プロット（halide vs B-cation で）
- **MANIFEST**:
  - `theme: theme_I_effective_mass`
  - `key_numbers`: 9 材料の (m_e_avg, m_h_avg, μ) を辞書で
  - `references`: Theme A k·p, Yang 2017, Cho 2019, exciton.py docstring 出典
  - `notes`: "TB-derived effective masses from R-point d²E/dk². Direct band-gap material set (CsBX₃ cubic phase). m_e/m_h consistent with literature (~0.1-0.15 m₀ for CsPbI₃)."
- **bundle 先**: `results/production/theme_I_effective_mass/<date>_<hash>/`

### Y1-c: 外部 ε_∞ extraction + E_b Production 化

**目的:** Wannier-Mott E_b を Production 化するが、ε_∞ は TB-optical KK の Blount-1962 過小（f-sum=0.21）を回避するため **既収集文献から抽出**して bundle する。m_e, m_h は TB 由来、ε_∞ は外部 — この **誤差ソースの明確な分離**を MANIFEST と報告書に明示する。

#### Y1-c-1: ε_∞ 抽出（文献調査）

**手順:**
1. `references/texts/` に pdftotext 出力が無ければ `scripts/pdf_to_text.py`（既存ならそれ、無ければ作成）で `references/pdfs/arxiv_*.pdf` を一括テキスト化（`references/texts/arxiv_<id>.txt`）。**`references/texts/` は `.gitignore` 済み**（CLAUDE.md 規約）。
2. `references/texts/*.txt` を以下のキーワードで grep して ε_∞ 候補値を拾う:
   - `"epsilon_\?\(inf\|infty\)"`, `"\\eps_\\?\\infty"`, `"\\epsilon_\\\\infty"`, `"high.\\?frequency dielectric"`, `"optical dielectric constant"`, `"ε∞"`, `"ε_∞"`, `"\\u03B5_\\u221E"`
   - 数値とともに材料名（CsPbBr3, CsPbI3, CsSnI3, ...）が併記されている箇所を優先
3. 候補抽出を `data/parameters/eps_inf_external.json` にまとめる:
   ```json
   {
     "CsPbI3": {
       "eps_inf": 6.32,
       "source": "Author Year, arXiv:xxxx.xxxxx Eq.(N) / Table M",
       "method": "experimental ellipsometry | DFT-RPA | Pekar(eps_static-eps_LO_phonon contribution)",
       "temperature_K": 300,
       "phase": "cubic",
       "notes": "..."
     },
     ...
   }
   ```
4. **重要**: 各値の **出典は arXiv ID + 式番号 or 表番号**まで明記（CLAUDE.md「docstring 出典・限界記載」と同様の厳格さ）。値だけ抜くのは禁止（後で検証不能になる）。
5. 9 材料すべて見つかれば理想。**見つからない材料があれば**:
   - `eps_inf: null, status: "not_found_in_references", searched: [arxiv_id list]` で明記
   - その材料は Y1-c-3 の E_b production 対象から外す（部分 production OK）
   - PI に報告（progress notification）し、後で PI 入力 or DFT-RPA database 引きで補完判断

#### Y1-c-2: 抽出結果のサニティチェック

抽出した ε_∞ を以下で検証してから Y1-c-3 へ:
- **物理的範囲**: 1 < ε_∞ < 20（halide perovskite で典型 3-8）
- **トレンド**: 同じ B-cation 内で Cl < Br < I（バンドギャップが狭くなると ε_∞ 大）— 反例があれば出典再確認
- **2 つ以上のソースから取れた場合**: 値の散らばり（±20% 以内ならどちらか採用 + notes に記載、それ以上ならどちらが信頼できるか PI 判断）

#### Y1-c-3: E_b Production scan

**スクリプト:** `scripts/scan_theme_I_binding_energy.py`（新規）

**仕様:**
- 入力: Y1-a の μ + `data/parameters/eps_inf_external.json` の ε_∞
- 計算: 既存 `wannier_mott_binding_eV(μ/m0, ε_∞)` を呼ぶだけ
- **convergence は Y1-a の μ 収束を継承**（E_b 公式自体は閉じた形なので追加 convergence 不要、ただし μ の n_kpts 依存を bundle 内で参照）
- **出力**:
  - `outputs/raw/binding_energy_9materials.csv`: 材料 / μ / ε_∞ / ε_∞_source / E_b_meV
  - `outputs/figures/binding_energy_summary.png`: 材料別 E_b trend
- **MANIFEST**:
  - `theme: theme_I_binding_energy`
  - `inputs`: `data/parameters/eps_inf_external.json` を必ず inputs に含める（外部値の追跡）
  - `references`: ε_∞ 出典をすべて列挙（material → source の辞書も含める）
  - **`notes`（最重要）**: 以下を明記
    > "Hybrid production: effective masses (μ) are TB-derived from R-point band curvature (Theme A k·p framework). ε_∞ values are externally sourced from literature (see references and data/parameters/eps_inf_external.json) to bypass the Blount-1962 systematic underestimate of TB-optical f-sum (~0.21, see results/optical/convergence.md). The Wannier-Mott formula E_b = (μ/m₀)/ε_r² · Ry uses ε_r = ε_∞ (upper-bound screening; physical screening lies between ε_∞ and ε_static via phonon contribution — see Tanaka 2003 / Yang 2017). Absolute E_b is therefore an upper bound; relative trends across the 9 materials are robust."
- **bundle 先**: `results/production/theme_I_binding_energy/<date>_<hash>/`

### Y1-d: テーマ I 報告書

**ファイル:** `cowork/reports/theme_I_exciton.md`（新規）

**構成:**
1. Background（Wannier-Mott 励起子、ハライドペロブスカイトでの位置付け）
2. Method（TB 有効質量 + 外部 ε_∞ hybrid、誤差ソース分離の説明）
3. Results
   - 表: 9 材料の m_e, m_h, μ, ε_∞ (source), E_b
   - プロット: trend
   - **本番値はすべて `results/production/theme_I_*/MANIFEST.json` の `key_numbers` から引用**（PRODUCTION_RULES §8 遵守）
4. Discussion
   - 信頼性: μ は TB 信頼可、ε_∞ は外部依存、E_b は組み合わせ
   - 比較: 実験報告値（CsPbI₃ ~15-20 meV 等）との比較、Wannier-Mott 上限という位置付け
   - Limits: phonon screening 未考慮、Frenkel-Wannier transition 領域材料での妥当性
5. Conclusions
6. References

---

## 2. Task Y2: LICENSE ファイル追加 + SPDX 差し替え

**目的:** PI 判断 (ii) に基づき、無料の OSS ライセンスを付与。

**手順:**
1. `LICENSE` ファイルを repo ルートに追加
   - **推奨: MIT License**（科学計算リポジトリで最も一般的、特許条項なし、論文付随コードに最適）
   - Apache-2.0 や BSD-3-Clause も可。PI に最終判断（チャットで確認 OK）
   - Copyright holder: `Teruhisa Kotani` または `tb-perovskite contributors`（PI 確認）
2. `scripts/cowork_5min_poll.ps1` の SPDX 行を `NOASSERTION` から **正しいライセンス識別子**に差し替え:
   ```powershell
   # SPDX-License-Identifier: MIT
   ```
3. **オプション（推奨）**: `src/perovskite_tb/*.py` と `scripts/*.py` の主要ファイルにも SPDX header 追加:
   ```python
   # SPDX-License-Identifier: MIT
   # Copyright (c) 2026 Teruhisa Kotani
   ```
   全ファイル必須ではないが、論文化想定で公開時に推奨される。

**commit メッセージ例:**
```
docs: add MIT LICENSE + SPDX headers for source files

PI が無料ライセンス追加を承認 (2026-05-24)。MIT を採用:
- 科学計算リポジトリで最も一般的
- 特許条項なし、論文付随コードに適する
- cowork_5min_poll.ps1 の SPDX を NOASSERTION から MIT に修正

Refs cowork/progress/2026-05-24_0715_directive_theme_I_hybrid_and_license.md
```

---

## 3. 優先順位と並列性

| Task | 推定時間 | 依存 |
|---|---|---|
| Y2 (LICENSE) | 10 分 | なし（ウォームアップに最適） |
| Y1-a (effective mass) | 30-45 分 | なし |
| Y1-c-1 (ε_∞ extraction) | 30-60 分 | references/texts/ 生成（必要なら） |
| Y1-c-2 (sanity check) | 15 分 | Y1-c-1 完了 |
| Y1-c-3 (E_b production) | 15 分 | Y1-a + Y1-c-2 完了 |
| Y1-d (report) | 30-45 分 | Y1-a + Y1-c-3 完了 |

**推奨順序:** Y2 → Y1-a → Y1-c-1 → Y1-c-2 → Y1-c-3 → Y1-d

Y1-a と Y1-c-1 は独立なので **並列実行可**（Claude Code 内部のサブタスクとして同時進行できれば時短）。

---

## 4. 完了通知

各 Task 完了後に以下のいずれかで通知:

- Y2 完了: `cowork/progress/2026-05-24_<HHMM>_Y2_license_added.md`
- Y1-a 完了: `cowork/progress/2026-05-24_<HHMM>_Y1a_effective_mass_production.md`
- Y1-c-1 完了（ε_∞ 抽出結果）: `cowork/progress/2026-05-24_<HHMM>_Y1c1_eps_inf_extracted.md`
   - **特に**: 見つからなかった材料があれば明示、PI 入力 or DFT-RPA フォールバックの判断要請
- Y1-c-3 完了: `cowork/progress/2026-05-24_<HHMM>_Y1c3_binding_energy_production.md`
- Y1-d 完了（全 Theme I 完了）: `cowork/progress/2026-05-24_<HHMM>_theme_I_complete.md`

各通知で commit hash、bundle path、key_numbers ハイライト、PRODUCTION_RULES 違反チェック結果（git_dirty=false, MANIFEST fields complete）を記載。

---

## 5. PRODUCTION_RULES 厳守事項

- `git_dirty: false` で commit してから production bundle 作成
- MANIFEST の 8 必須フィールド完備
- 収束プロット → `convergence/` 配下（Y1-a は必須、Y1-c-3 は μ 収束継承の旨を MANIFEST.notes に記載）
- 報告書の数値は **すべて MANIFEST.json から引用**（手書きの数値は禁止）

---

## 6. 残る PI 判断（本 directive スコープ外）

以下は別 directive で対応予定:

1. **(i) `claude --continue` 動作検証**: PI 環境で 1 回手動起動して挙動確認後、必要なら `-p` のみに切り替える directive
2. **巡回トークンコスト最適化**: PowerShell 側で「ファイル変更ありの時だけ claude 起動」フィルタを追加 → 99% の巡回が 0 トークン。PI 承認得られたら別途 directive 化

これらは本 directive と独立なので、本 directive の進行を妨げない。

---

**本 directive は PI（ktmailmg@gmail.com）の起床判断 (ii)+(iii) に基づきます。Y2 → Y1-a → Y1-c の順で進め、Y1-c-1 の ε_∞ 抽出結果が想定外（多数の材料で見つからない等）なら一旦止めて PI 確認してください。**
