# Quant, Built — Part 13: Stochastic Volatility and Jumps

Part 13 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), in Act III, Derivatives: about 56 minutes, a hook, eighteen chapters and an outro.
It covers:

* why volatility must move, and why random volatility makes a smile (Hull–White, Renault–Touzi, Romano–Touzi);
* Heston's model: the characteristic function derived, the little trap, the fit replayed, the short-maturity skew,
  Feller's condition and Andersen's QE scheme;
* SABR: Hagan's expansion, the backbone, the negative density, arbitrage-free SABR solved as a PDE, Bartlett's delta;
* jumps (Merton's series, Kou, Bates) and Lévy models as time changes (VG, NIG, CGMY, Carr–Wu); the skew's term
  structure across every model;
* stochastic local volatility by the particle method, its convergence, and the mixing fraction;
* Bergomi's forward variance curves, the vol-of-vol term structure and the SSR;
* forward smiles and cliquets; the SPX/VIX puzzle measured on bitcoin;
* calibration as an inverse problem (the Hessian, 100 weekly refits, regularisation); how desks judge a model by its
  hedge; the 2023–2026 frontier.

Every number is computed by the series' own code ([`compute.py`](compute.py), and the House's
[`stochvol`](../../../explainer/quant/house/stochvol.py) library, tested in `tests/test_quant_house.py`). The data
are Deribit's trades (the Surface and 100 weekly surfaces), Binance's BTCUSDT (daily and hourly), Deribit's DVOL, and
the S&P 500's daily closes for 1986–1987 (Yahoo).

*An education in methods, not investment advice.*

## Chapters

* **The second river (hook).** DVOL 2021–2025 with its floods. Five models fitted to the same options price one
  cliquet 8% apart. How we got here, 1973–2022. Objectives; the calibrator.
* **1. Why volatility must move.** 30-day realized vol ranged 17–122%; DVOL's vol of vol is 89% a year. The daily
  return/ΔlogDVOL scatter, live: −0.58 in 2022, +0.30 in 2023, −0.23 overall, so returns explain about 5% of DVOL's
  daily variance. |r| autocorrelation 0.15 at lag one and still positive at 60 days; AR(1) on log DVOL gives a
  half-life of 54 days. Crisis file: 19 October 1987, a −22.9% log return, a 22σ day (probability ~10⁻¹⁰⁴ under a
  constant-volatility normal model).
* **2. Random volatility makes a smile.** The mixing crowd of conditional Gaussians; doubling the vol of vol (ρ = 0)
  lifts the wings (61% → 68%) and lowers the ATM vol (46.6% → 40.4%). Hull–White, the second-order expansion, the sign
  of ∂²C/∂σ², Romano–Touzi's formula. The conditional estimator: errors 7× smaller than plain Monte Carlo, all 13
  strikes within 0.8 s.e. of COS.
* **3. Heston I: the characteristic function.** Feynman–Kac, the affine ansatz, the Riccati equations solved. The CF
  as a 3D helix. The little trap: Heston's original form crosses the branch cut at u = 1.67 (T = 1) on our fit and
  prices a one-year ATM call at 66% vol instead of 48%. Lab: `heston_cf`, the Fang–Oosterlee benchmark to 10⁻⁸.
* **4. Heston II: what each parameter does.** 3D sliders for v₀, θ, κ, ρ, ξ. The calibration replayed from three
  starts (all end at loss 1.296; implied-vol RMSE 1.33). The fit: κ = 14.8, ξ = 4.6, ρ = −0.31, Feller 0.37; 3-day
  expiry missed by 5.3. The short-maturity skew ρξ/(4√v₀) derived: −0.731 against −0.742 from the model at 2 days.
* **5. Heston III: simulating it honestly.** One step of the variance: Euler puts 22% of draws below zero; QE's atom
  and exponential tail match the mean exactly. Transport distance to the exact law: QE better in 9 of 9 cases, by a
  median factor of 16. QE derived by moment matching. Lab: `heston_qe` (2 steps: Euler +20%, QE −1%). Broadie–Kaya,
  Choi–Kwok, moment explosions.
* **6. SABR I.** The model, the expansion term by term (skew ρν/2, curvature ∝ ν²/α, backbone αF^(β−1)), the slice-by-
  slice replay (0.38 vol points with 27 parameters; ν ∝ T^−0.49), the 3D ribbon, the backbone and local vol's wrong-way
  dynamics.
* **7. SABR II.** Hagan's 10-year density goes negative and integrates to 0.63. Arbitrage-free SABR (the effective
  forward PDE, absorbing boundary) solved on 480 cells: mass 1 to 10⁻¹⁰, density ≥ 0, 14% absorbed at zero by ten
  years; ATM 21.6% against Hagan's 22.0%, 46% against 53% at a 0.5% strike. Obłój, free-boundary SABR, shifted SABR,
  Bartlett's delta.
* **8. Jumps.** Merton's layer cake and series; Bates as Heston × jumps; Kou. Fits: Merton 2.16 vol points (λ = 0.25 a
  year, mean jump −49%), Kou 2.41, Heston 1.33, Bates 1.31 with λ at its bound of 20 and σ_J at its floor: a second
  diffusion, replayed from three starts. SVCJ; Hou et al. (2020) on bitcoin; jump to default.
* **9. Lévy models and time changes.** The gamma clock, live; VG's CF derived; CGMY's fine structure (Y = −0.5, 0.5,
  1.5); Carr–Wu. Lab: `vg_cf`/`vg_paths`, COS 0.05352 against MC 0.05346 ± 0.00018. Race: VG 2.89, NIG 2.70, CGMY
  2.64 with Y at the bound 0.95, 2.51 with Y = 1.57 (infinite variation).
* **10. The skew across maturities.** Small multiples as expiry shrinks; local power-law slopes (2–14 days / 60–365
  days): market −0.34 / −0.76 (−0.49 overall), Heston −0.09 / −0.75, VG −1.05 / −1.01, NIG −0.73 / −0.98, Merton
  −0.11 / −0.43, Kou −0.12 / −0.58, CGMY (Y = 1.57) −0.48 / −0.78. Cumulant scaling; Sato processes; Abi Jaber–De
  Carvalho.
* **11. SLV: the particle method.** The McKean–Vlasov loop; particles live with E[v | x] and the leverage; the
  leverage surface in 3D. Lab: `slv_paths` (repricing 0.68 vol points at 30 days, 0.44 at 120). Convergence: mean
  error 1.25 (2,000 particles), 0.72 (8,000), 0.51 (40,000); bandwidth ×½ and ×2 both slightly worse. PDE route;
  Reisinger–Tsianni (2025).
* **12. The mixing fraction.** η from 0 to 1: forward skew 2.6 → 7.1 points, cliquet 13.77% → 12.85% (not
  monotone), vanilla repricing below 1 vol point up to η = ½ and 3.4 at η = 1; three seeds at η = ½ differ by 4 bp. FX
  desks set η from barrier and no-touch prices (Clark 2011).
* **13. Bergomi.** The Surface's forward variance curve and its weekend dip (Saturday realized 29% against 54% on
  weekdays). The two-factor model; one simulated curve over 120 days (ω = 2.32 so the 30-day index has DVOL's vol of
  vol; martingale within 1.4%); Heston's single exponential. Vol-of-vol term structure at 90 days: 74% against 21%.
  SSR of the fitted Heston: 1.93 at 2 days, 1.20 at a year.
* **14. Forward smiles and cliquets.** Heston's forward smile by a 1D integral against MC (within 0.4 vol points,
  inside the seed spread). Forward skews: LV 3.4, Heston 6.1, Bates 6.3, VG 5.0, SLV 5.1 against 6.5 today. The cliquet
  as forward-start call spreads; 13.1–14.2% across models (8% apart); the forward start 11% apart.
* **15. The SPX/VIX puzzle on bitcoin.** Cboe VIX futures (2004) and options (2006); Gatheral (2008); Guyon (2020);
  Cont–Kokholm (2013). The fitted Heston's own 30-day index has a vol of vol of 193% against DVOL's 89% (2.2×);
  correlation −0.25 against −0.23. Jensen's gap (variance-swap vol 51.2%, future 47.9%, floor 34%); options on the
  index: ATM 125% at 30 days, 74% at 90. Bates: 186%.
* **16. Calibration.** The (κ, ξ) landscape and its valley; the profile Hessian (curvature ratio 27; full condition
  number 1,024; s.e. of κ about 12%). 100 weekly refits as a walk along the valley; κ at its bound in 20% of weeks,
  Feller failing in 91%, ρ > 0 in 54%. Lab: `calibrate_reg`; λ = 0.03 and 0.3 cut the median weekly parameter change
  only from 12.7% to 10.6% (κ 25% → 18%, ξ 15% → 9%) for 0.01 vol points of fit.
* **17. Industry.** Société Générale's research (Bergomi, Guyon, Henry-Labordère); Cboe and Deribit. The
  minimum-variance delta (Hull–White 2017) derived and tested on bitcoin, 2021–2025: a β fixed on 2021–22 cuts hedge
  variance 23% in sample and raises it 55% in 2023–25; a rolling 60-day β cuts it 9% (not every year). Inside the
  fitted Heston: hedge-error s.d. BS 0.0256, Heston delta 0.0268, MV 0.0255, unhedged 0.082. Bakshi–Cao–Chen (1997);
  Matic–Packham–Härdle (2023); the EU model-risk AVA (Delegated Regulation 2016/101, Art. 11). The House's module.
* **18. Frontier.** Reversionary Heston refitted with κ = 15, 30, 60, 120: ξ = 4.7, 7.0, 11.0, 18.5 (ξ/√κ 1.20 → 1.69),
  3-day error 5.3 → 3.3–3.6 while the overall fit worsens 1.33 → 1.78. The quintic OU model; Guyon–Mustapha;
  Choi–Kwok; Reisinger–Tsianni; Wang et al. (2026).
* **Recap, desk questions, problems.** Rule 13; the trial counter stays at 73.

## Build it

```bash
python -m videos.quant.quant13.compute                   # every number (resumable; ~1.5 CPU-hours on one core)
EXPLAINER_TTS=silent python tools/qa_scene.py quant13 Heston  # one chapter, silent, with a contact sheet
python tools/make.py quant13 --cpu-voice -q m            # English and Chinese, narrated by Kokoro on the CPU
```

The long items (`slv_particles`, `mixing_sweep`, `history_reg`) save their pieces as they go and resume if killed.

## Textbook audit

| Book · chapter | Where |
|---|---|
| Gatheral 1 SV and LV (the SV PDE) | ch3; LV → Part 12 |
| Gatheral 2 The Heston model (CF, branch cut, simulation, fit) | ch3, ch4, ch5 |
| Gatheral 3 The implied volatility surface (Heston skew, term structure of skew) | ch4, ch10; the power law → Part 14 |
| Gatheral 4 Heston–Nandi / local variance of SV | ch4, ch11 (E[v \| S]); Part 12 ch7 |
| Gatheral 5 Adding jumps (SVJ, SVJJ) | ch8, ch10; variance swaps with jumps → Part 12 |
| Gatheral 6 Modeling default | ch8 card; Part 20 |
| Gatheral 7 Asymptotics | ch4, ch10; Lee → Part 12; power law → Part 14 |
| Gatheral 8 Dynamics of the volatility surface | ch13 (SSR); empirical → Part 12 |
| Gatheral 10 Exotic cliquets | ch14; structuring → Part 15 |
| Gatheral 11 Volatility derivatives | ch15; VIX and swaps → Part 12 |
| Bergomi 3 Forward-start options | ch14 |
| Bergomi 4 Stochastic volatility, introduction | ch2, ch17 |
| Bergomi 6 The Heston model | ch4, ch13 |
| Bergomi 7 Forward variance models | ch13; calibrated two-factor → Part 14 |
| Bergomi 8 The smile of SV models | ch2, ch10; full expansion → Part 14 |
| Bergomi 9 Linking static and dynamic properties (SSR) | ch13 |
| Bergomi 10 What causes equity smiles? | ch1, ch2, ch10 |
| Bergomi 11 Multi-asset SV | Part 15 |
| Bergomi 12 Local-stochastic volatility | ch11, ch12 |
| Cont–Tankov 4 Building Lévy processes | ch9 |
| Cont–Tankov 6 Simulating Lévy processes | ch9 (gamma clock, CGMY paths), lab |
| Cont–Tankov 11 Exponential Lévy models | ch9, ch10 |
| Cont–Tankov 13 Inverse problems and calibration | ch16 |
| Cont–Tankov 14 Time-inhomogeneous jump processes | ch10 card |
| Cont–Tankov 15 SV models with jumps | ch8, ch9 |
| Cont–Tankov 1–3, 5, 7–10, 12 | Part 5 (2–3, 6, 8), Parts 5 and 11 (9–10), Part 16 (12); 5 (multivariate) → Part 15 |
| Lewis 1–2 The fundamental transform | ch3; pricing formula → Part 16 |
| Lewis 3–5 Vol-of-vol series, mixing, the smile | ch2 |
| Lewis 6 Term structure of implied volatility | ch10 |
| Lewis 7 Utility-based equilibrium | ch15 (P against Q); VRP → Part 12 |
| Lewis 8 Duality and changes of numéraire | ch14 (forward starts) |
| Lewis 9 Volatility explosions | ch5 card (moment explosions); Lee → Part 12 |
| Guyon–Henry-Labordère, *Nonlinear Option Pricing* (McKean SDEs, LSV calibration by particles) | ch11, ch12 |
| Oosterlee–Grzelak (Heston, QE, Lévy) | ch5, ch9; COS → Part 16 |
| Shreve II 11.7 (a call in a jump model) | ch8 |
| Hull, "More on models" (jump-diffusion, SV, CEV) | ch8, ch2, ch6 |

## Desk questions, with solutions

1. **In Heston, what sets the skew? And the curvature?**
   * The correlation ρ sets the skew, scaled by the vol of vol: at short maturity the ATM slope is ρξ/(4√v₀) (chapter
     4: −0.731 on our fit, −0.742 from the model at two days).
   * The curvature grows with ξ²; mean reversion κ damps both beyond 1/κ.
2. **Local vol and an SV model both fit today's surface. You must price a cliquet.**
   * Not local vol alone: a cliquet is a strip of forward-start call spreads, priced off forward smiles, and local
     vol flattens them (3.4 points against 6.5 today).
   * Use an SV or SLV model with a stated mixing fraction, and report the spread across models (8% here) as model risk.
3. **Why can a VIX future never trade above the 30-day variance-swap volatility?**
   * The future is E[VIX_T]; the variance-swap vol is √E[VIX²_T], fixed by the S&P strip. The square root is concave,
     so Jensen gives E[VIX] ≤ √E[VIX²].
   * The gap is about Var(VIX)/(2E[VIX]): futures and options on the index price the vol of vol.

## Problems, with solutions

1. **Heston's Riccati equations.**
   * Write x = ln S and τ = T − t. The price of a claim on x_T solves
     ∂_τ f = ½v(f_xx − f_x) + ρξv f_xv + ½ξ²v f_vv + κ(θ − v)f_v.
   * Substituting f = exp(C(τ) + D(τ)v + iux) and collecting the terms in v gives
     D′ = ½ξ²D² − (κ − ρξiu)D − ½(u² + iu), with D(0) = 0.
   * The terms without v give C′ = κθD, with C(0) = 0.
   * The solution is the little-trap form used in the House: d = √((κ − ρξiu)² + ξ²(iu + u²)).
2. **The short-maturity skew.**
   * As T → 0, the implied variance at log-moneyness k is the local variance averaged along the straight line to k
     (Berestycki–Busca–Florent). The local variance is E[v | S]. Over a short time v − v₀ ≈ ξ√v₀W², and
     x ≈ √v₀W¹, so E[v | x] ≈ v₀ + ρξx.
   * Averaging along the line gives σ²_imp(k) ≈ v₀ + (ρξ/2)k, and hence ∂_kσ_imp = (ρξ/2)/(2√v₀) = ρξ/(4√v₀).
3. **The Lévy forward smile.**
   * The forward-start payoff (S_{t+τ}/S_t − e^k)⁺ depends only on the increment X_{t+τ} − X_t.
   * For a Lévy process that increment has the law of X_τ and is independent of the past.
   * So the price equals today's τ-option at the same moneyness, and the forward smile is today's smile.
4. **Feller's condition.**
   * The scale density of CIR is s′(v) = v^{−2κθ/ξ²}·e^{2κv/ξ²}.
   * Zero is reached exactly when ∫₀ s′(v)dv < ∞, that is, when 2κθ/ξ² < 1.
5. **Why the leverage function works.**
   * The density p(S, t) of dS/S = L√v dW solves ∂_t p = ½∂_SS(S²L² E[v | S] p) (Gyöngy's mimicking theorem).
   * That is Dupire's forward equation exactly when L²E[v | S] = σ²_loc.
   * The two models then share every marginal, and so every vanilla price.
6. **Merton's series.**
   * With zero rates, dS/S₋ = −λk̄dt + σdW + (e^J − 1)dN, J ~ N(μ_J, σ_J²), k̄ = e^{μ_J+σ_J²/2} − 1.
   * Given N_T = n, ln S_T is normal with mean ln S₀ − λk̄T − ½σ²T + nμ_J and variance σ²T + nσ_J²: a lognormal with
     forward F_n = S₀e^{−λk̄T + n(μ_J + σ_J²/2)} and volatility σ_n² = σ² + nσ_J²/T.
   * So C = Σ_n e^{−λT}(λT)^n/n! · C_BS(F_n, K, T, σ_n) (the House's `merton_series`, equal to COS to 10⁻⁸).
7. **The variance gamma characteristic function.**
   * X_t = θG_t + σW_{G_t}, with G_t ~ Γ(shape t/ν, scale ν).
   * Given G_t, X_t is normal: E[e^{iuX_t} | G_t] = e^{G_t(iuθ − σ²u²/2)}.
   * The gamma mgf E[e^{sG_t}] = (1 − νs)^{−t/ν} at s = iuθ − σ²u²/2 gives φ(u) = (1 − iuθν + ½σ²νu²)^{−t/ν}.
   * The martingale correction ω = (1/ν)ln(1 − θν − ½σ²ν) is added to the drift, so that E[e^{X_t + ωt}] = 1.

## Reading guide

Every paper of Part 13's list in [`READING.md`](../READING.md) appears on screen; the newest ones:
Abi Jaber–De Carvalho (2023, reversionary Heston, chapter 18), Abi Jaber–Illand–Li (2023, quintic OU), Guyon–Mustapha
(2023, neural joint SPX/VIX), Choi–Kwok (2024, Poisson-conditioned simulation), Reisinger–Tsianni (2025, the particle
system's convergence), Wang–Després–Dureau–Buet-Golfouse (2026, neural operators for LSV, synthetic tests as reported),
Hou et al. (2020) and Matic–Packham–Härdle (2023) on bitcoin options.

## Data and reproducibility

* The Surface: Deribit BTC option trades on 10 December 2025 (193 quotes, expiries from 3 to 289 days).
* Weekly surfaces: every Wednesday from 3 January 2024 to 26 November 2025 (100 days), as in Part 12.
* Binance BTCUSDT daily (2021-04 to 2025-11) and hourly (2024–2025); Deribit DVOL daily; S&P 500 daily 1986–1987.
* No strategy was tested (the minimum-variance delta is descriptive hedging); the trial counter is unchanged at 73.

---

# 量化金融，从零搭建 — 第13部分：随机波动率与跳跃

本部分讲：

* 波动率为什么必须变动：波动率的波动率、杠杆效应，以及1987年以后的偏斜；
* 赫斯顿模型、它的特征函数、费勒条件和安德森的QE格式；
* SABR：哈根公式、骨架，以及它在长期限处的套利；
* 跳跃与莱维模型：默顿、寇、贝茨、方差伽马、NIG、CGMY，以及时间变换；
* 用粒子方法实现的随机局部波动率；
* 贝尔戈米的远期方差曲线；
* 远期微笑、棘轮期权与模型风险，以及在比特币上测量的SPX/VIX难题；
* 校准：损失地形与参数的不稳定。

*讲的是方法，不构成投资建议。*

## 各章（约56分钟）

* **第二条河（开场）。** 2021–2025年的DVOL；五个模型拟合同一组期权，给同一份棘轮期权的定价相差8%；1973–2022年的历史；本部分目标与校准器。
* **1. 波动率为什么必须变动。** 30天实现波动率在17%–122%之间；DVOL的波动率的波动率为每年89%；收益与DVOL变化的散点（2022年−0.58，2023年+0.30）；|r|的长记忆；对数DVOL的半衰期54天；危机档案：1987年10月19日，−22.9%，22个标准差。
* **2. 随机波动率产生微笑。** 条件高斯分布群；赫尔–怀特、二阶展开、罗马诺–图齐公式的推导；条件蒙特卡罗的误差约为普通蒙特卡罗的七分之一。
* **3. 赫斯顿之一：特征函数。** 仿射猜测与里卡蒂方程的推导；三维螺旋；“小陷阱”：原始形式在u = 1.67处跨过分支切割，一年期平值期权给出66%而非48%；实验：`heston_cf`。
* **4. 赫斯顿之二：每个参数做什么。** 三维滑块；三个起点的校准回放；拟合结果κ = 14.8、ξ = 4.6；短期偏斜ρξ/(4√v₀)的推导（−0.731对−0.742）。
* **5. 赫斯顿之三：老老实实地模拟。** 一步方差：欧拉格式22%的抽样为负；QE用矩匹配推导，传输距离中位数好16倍；实验：`heston_qe`。
* **6. SABR之一。** 展开式逐项解读、逐切片拟合回放（ν ∝ T^−0.49）、三维带状曲面、骨架。
* **7. SABR之二。** 哈根十年密度为负；无套利SABR偏微分方程：质量为1，密度非负，十年时14%被吸收于零；巴特利特Delta。
* **8. 跳跃。** 默顿级数（千层蛋糕）、寇、贝茨；默顿2.16点（λ = 0.25，平均跳跃−49%），贝茨的跳跃变成第二个扩散（回放）。
* **9. 莱维模型与时间变换。** 伽马时钟；方差伽马特征函数推导；CGMY精细结构（Y = 1.57，无界变差）；实验：`vg_cf`/`vg_paths`。
* **10. 跨期限的偏斜。** 各模型的局部幂次：市场−0.34/−0.76，赫斯顿−0.09/−0.75，方差伽马约−1。
* **11. 随机局部波动率：粒子方法。** 粒子实时演示、三维杠杆曲面、收敛性（2000个粒子1.25点，40000个0.51点）；实验：`slv_paths`。
* **12. 混合比例。** η从0到1：远期偏斜2.6→7.1点，棘轮期权13.77%→12.85%，香草期权几乎看不到这个旋钮。
* **13. 贝尔戈米。** 周末凹陷；两因子模型的曲线模拟（鞅性在1.4%以内）；波动率的波动率期限结构；赫斯顿的偏斜粘性比（两天1.93，一年1.20）。
* **14. 远期微笑与棘轮期权。** 一维积分与蒙特卡罗一致；棘轮期权是远期起始看涨价差的组合；模型间相差8%。
* **15. SPX/VIX难题。** 拟合的赫斯顿模型自身指数的波动率的波动率为193%，DVOL为89%；詹森缺口；指数期权平值隐含波动率125%。
* **16. 校准。** 山谷与黑塞矩阵（曲率比27）；一百周的漫步；正则化（`calibrate_reg`）只把周度变化从12.7%降到10.6%。
* **17. 业界。** 法国兴业银行的研究团队；最小方差Delta在比特币上的检验（固定β样本外变差55%，滚动β改善9%）；赫斯顿世界中的对冲；欧盟模型风险估值调整。
* **18. 前沿。** 回复型赫斯顿（κ = 15到120，ξ/√κ从1.20到1.69）；五次OU模型、居永–穆斯塔法、崔–郭、赖辛格–齐亚尼、王等（2026）。

## 交易台问题与解答

1. **在赫斯顿模型里，什么决定偏斜？曲率呢？**
   * 相关系数ρ决定偏斜，并由波动率的波动率放大：短期限时平值斜率约为ρξ/(4√v₀)。在曲面的拟合上这是−0.73，模型在两天期给出−0.74。
   * 曲率来自ξ²。
   * 均值回复κ让两者随期限变平。
2. **局部波动率和一个随机波动率模型都拟合今天的曲面，你要给棘轮期权定价。**
   * 不能只用局部波动率：棘轮期权押注的是未来的微笑，而局部波动率把它压平（这里为3.4点，今天为6.5点）。
   * 用随机或随机局部波动率模型，并说明混合比例；把各模型之间的差距（这里8%）作为模型风险报告。
3. **为什么VIX期货永远不能交易在30天方差互换波动率之上？**
   * 期货是E[VIX_T]，方差互换波动率是√E[VIX²_T]，由标普期权组合固定。平方根是凹函数，由詹森不等式E[VIX] ≤ √E[VIX²]。
   * 差距约为Var(VIX)/(2E[VIX])：指数的期货和期权给波动率的波动率定价。

## 习题与解答

1. **赫斯顿的里卡蒂方程。**
   * 记x = ln S，τ = T − t。关于x_T的权益价格满足∂_τ f = ½v(f_xx − f_x) + ρξv f_xv + ½ξ²v f_vv + κ(θ − v)f_v。
   * 代入f = exp(C(τ) + D(τ)v + iux)，收集含v的项得D′ = ½ξ²D² − (κ − ρξiu)D − ½(u² + iu)，D(0) = 0。
   * 不含v的项给出C′ = κθD，C(0) = 0。
   * 其解就是公司使用的“小陷阱”形式：d = √((κ − ρξiu)² + ξ²(iu + u²))。
2. **短期限偏斜。**
   * 当T → 0时，对数价值状态k处的隐含方差是沿直线到k的局部方差的平均（Berestycki–Busca–Florent）。局部方差是E[v | S]；短时间内v − v₀ ≈ ξ√v₀W²，x ≈ √v₀W¹，所以E[v | x] ≈ v₀ + ρξx。
   * 沿直线平均得σ²_imp(k) ≈ v₀ + (ρξ/2)k，从而∂_kσ_imp = (ρξ/2)/(2√v₀) = ρξ/(4√v₀)。
3. **莱维模型的远期微笑。**
   * 远期起始收益(S_{t+τ}/S_t − e^k)⁺只依赖增量X_{t+τ} − X_t。
   * 对莱维过程，这个增量与X_τ同分布，且独立于过去。
   * 所以价格等于今天同一价值状态的τ期期权，远期微笑就是今天的微笑。
4. **费勒条件。**
   * CIR的尺度密度为s′(v) = v^{−2κθ/ξ²}·e^{2κv/ξ²}。
   * 当且仅当∫₀ s′(v)dv < ∞，即2κθ/ξ² < 1时，零点可达。
5. **杠杆函数为什么有效。**
   * dS/S = L√v dW的密度p(S, t)满足∂_t p = ½∂_SS(S²L² E[v | S] p)（久永的模仿定理）。
   * 当L²E[v | S] = σ²_loc时，这正是杜皮尔的前向方程。
   * 于是两个模型的每个边际分布都相同，每个香草期权价格也都相同。
6. **默顿级数。**
   * 零利率下dS/S₋ = −λk̄dt + σdW + (e^J − 1)dN，J ~ N(μ_J, σ_J²)，k̄ = e^{μ_J+σ_J²/2} − 1。
   * 给定N_T = n，ln S_T服从均值ln S₀ − λk̄T − ½σ²T + nμ_J、方差σ²T + nσ_J²的正态分布：远期F_n = S₀e^{−λk̄T + n(μ_J + σ_J²/2)}，波动率σ_n² = σ² + nσ_J²/T。
   * 所以C = Σ_n e^{−λT}(λT)^n/n! · C_BS(F_n, K, T, σ_n)（公司的`merton_series`，与COS相差小于10⁻⁸）。
7. **方差伽马的特征函数。**
   * X_t = θG_t + σW_{G_t}，G_t ~ Γ(形状t/ν，尺度ν)。
   * 给定G_t，X_t是正态的：E[e^{iuX_t} | G_t] = e^{G_t(iuθ − σ²u²/2)}。
   * 伽马分布的矩母函数E[e^{sG_t}] = (1 − νs)^{−t/ν}在s = iuθ − σ²u²/2处取值，得φ(u) = (1 − iuθν + ½σ²νu²)^{−t/ν}。
   * 鞅修正ω = (1/ν)ln(1 − θν − ½σ²ν)加到漂移上，使E[e^{X_t + ωt}] = 1。
