# 用語・記号定義 (glossary)

## 略語

| 略語 | 意味 |
|---|---|
| TB | Tight-Binding（タイトバインディング） |
| ETB | Empirical Tight-Binding（経験的 TB） |
| SK | Slater-Koster（二中心近似） |
| SOC | Spin-Orbit Coupling（スピン軌道相互作用） |
| DFT | Density Functional Theory（密度汎関数理論） |
| mBJ | modified Becke-Johnson（交換ポテンシャル） |
| BZ | Brillouin Zone（ブリルアンゾーン） |
| VBM / CBM | 価電子帯頂上 / 伝導帯底 |
| VEC | Valence Electron Count（価電子数） |
| V&V | Verification & Validation |

## 結晶・材料

| 用語 | 意味 |
|---|---|
| ペロブスカイト `ABX₃` | A=Cs等, B=Pb/Sn/Ge, X=Cl/Br/I の結晶 |
| cation (c) | B サイト陽イオン（Pb 等）。本実装では原点 |
| anion (a) | X サイト陰イオン（ハライド）。各軸 a/2 に1個ずつ |
| 立方相 (α, Pm-3m) | 高対称相。本実装の対象 |

## 高対称点（単純立方 BZ, 単位 2π/a）

| 記号 | 簡約座標 |
|---|---|
| Γ | (0,0,0) |
| X | (½,0,0) |
| M | (½,½,0) |
| R | (½,½,½) — 立方ハライドペロブスカイトの直接ギャップ位置 |

## 物理量・記号 → 変数名（コード対応）

| 記号 | 意味 | 変数/キー | 単位 |
|---|---|---|---|
| `a` | 立方格子定数 | `a` | Å |
| `E^B_s, E^B_p, E^X_p` | オンサイトエネルギー（Kashikar） | `E_B_s, E_B_p, E_X_p` | eV |
| `E_{s/p/d}^{c/a}` | オンサイト（Nestoklon, c=cation/a=anion） | `E_s_c, E_p_a, …` | eV |
| `t^{BX}_{sp}` 等 | B–X 最近接ホッピング | `t_BX_sp, t_BX_ppsigma, t_BX_pppi` | eV |
| `t^{BB}_{ss}` 等 | B–B 第二近接ホッピング | `t_BB_ss, t_BB_spsigma, …` | eV |
| `λ` | SOC 係数（= Δ/3, p 分裂 = 3λ） | `lambda_SOC` | eV |
| `Δ_c/3, Δ_a/3` | SOC（cation/anion, Nestoklon） | `Delta_c_over_3, Delta_a_over_3` | eV |
| `η` | Eq.9 の補助量 | （`models_kashikar`内） | eV |
| `S_d, C_d` | Bloch 簡約因子 `2i sin(k_d a/2)`, `2cos(k_d a/2)` | （実装内） | — |
| `n_filled` | 占有スピンバンド数 | `n_filled` | — |

## Slater-Koster 二中心積分（σ/π/δ）

`⟨α(原子1)|H|β(原子2)⟩` を方向余弦 `(l,m,n)` と σ/π/δ 積分で表す（Slater-Koster 1954）。
極性結合のため**順序対ごと**に積分が異なる。Nestoklon の命名規約（`SOURCES.md` 参照）:

| キー | 意味 |
|---|---|
| `ss_sigma` | (s_c)–(s_a) σ |
| `sc_pa_sigma` | (s_cation)–(p_anion) σ |
| `sa_pc_sigma` | (s_anion)–(p_cation) σ |
| `pp_sigma, pp_pi` | (p_c)–(p_a) σ, π |
| `sc_da_sigma`, `sa_dc_sigma` | (s_c)-(d_a), (s_a)-(d_c) σ |
| `pa_dc_sigma` | (p_anion)–(d_cation) σ |
| `dd_sigma, dd_pi, dd_delta` | (d_c)–(d_a) σ, π, δ |
| `sa_sstar_c_sigma` 他 s\* 系 | s\* を含む σ 積分 |
| 零固定 | `s*s*σ, sc_sstar_a_σ, sstar_a_dc_σ, pc_da_σ, pa_dc_π, pc_da_π = 0`（Table I） |

## 軌道ラベル（コード内正規化）

`s, px, py, pz, dxy, dyz, dzx, dx2y2 (=d_{x²-y²}), dz2 (=d_{3z²-r²}), sstar (=s*)`。
JSON の `dx2-y2`, `s*` は読み込み時に `dx2y2`, `sstar` へ正規化。
