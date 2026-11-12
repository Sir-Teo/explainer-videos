

# Quant, Built — Part 13: Stochastic Volatility and Jumps

Part 13 of the forty-three-part series ([plan](../README.md), [syllabus](../SYLLABUS.md)). About 61 minutes of narration: an opening, eighteen chapters, a research chapter and an outro. Calculations come from the original [compute module](compute.py) and [House library](../../../explainer/quant/house/stochvol.py). This pass changes explanations and displays; it does not change pricing algorithms, run new strategy trials or open holdouts.

The Surface pools Deribit option **marks from 00–12 UTC on 10 December 2025**, with an 08 UTC reference, then filters to 193 observations. These are not simultaneous executable trades. The five models use the same input but have unequal vanilla errors. LV and SLV target an SSVI projection; global Heston, Bates and VG fits differ. Exotic-price spreads therefore contain dynamics, fitting and numerical errors, and are not confidence intervals.

*An education in methods, not investment advice.*

## Chapters (about 61 minutes)

* **Opening.** DVOL history and a four-coupon cliquet: LV 13.73%, Heston 13.04%, Bates 13.31%, VG 14.23%, SLV 13.67% of notional, about 9% across the range relative to the mean. Unequal fits limit attribution of that range to dynamics.
* **1. Why volatility moves.** Realized volatility ranged 17–122%; DVOL log-change volatility was about 89% annualized. Same-day return correlation and its squared value describe a linear association; residuals do not establish independent volatility shocks or reject GARCH. Small return ACF is not no memory; positive absolute-return ACF on this finite grid is not proof of asymptotic long memory. The 54-day AR(1) half-life is empirical. The 1987 Gaussian tail probability uses the preceding 250-day fixed-volatility benchmark, not a real-world crash probability.
* **2. Mixing.** Forty conditional Gaussian paths illustrate a finite mixture; the lower IV curve is a separately computed COS result. Thin density peaks outside the stated viewport are not flattened into a plateau. Taylor expansion is in variance: for w=σ², C_ww=vega(d₁d₂−1)/(4σ³). Heston conditional log returns remain Gaussian at nonzero correlation, with a shifted mean and residual variance. The numerical conditional estimator uses 91 QE steps and trapezoidal integration; its approximately sevenfold narrower sampling errors exclude discretization bias. COS is a numerical benchmark.
* **3. Heston CF.** Affine ansatz, Riccati solution, branch convention and the little trap; the Fang–Oosterlee price benchmark. Slow transform decay alone does not diagnose every tail property.
* **4. Heston sensitivities and fit.** Interacting parameters; full saved loss ranges from all three starts, including initial losses above 25. The short-time ATM skew ρξ/(4√v₀) is a local regular-model result. The BBF small-time relation is harmonic in local volatility; the arithmetic local-variance expression is only its first-order near-ATM expansion. Heston's ξ is not directly comparable with percentage log-DVOL volatility.
* **5. Simulation.** The CIR zero boundary is attainable below the Feller threshold, but with positive mean reversion level its positive-time distribution has no zero atom. QE's atom is numerical. QE matches conditional population moments, not each finite sample exactly; QE-M also needs the branch moment-generating function to exist. The variance histograms explicitly disclose their zoomed heights.
* **6. SABR.** dF=αF^βdW; the displayed ρν/2 skew specializes to β=1 at leading short time. Hagan is an asymptotic pricing formula. Independent expiry fits have 27 parameters and no automatic calendar-arbitrage certificate. Black and normal quoting conventions differ, and the earlier sticky-rule regression does not identify β.
* **7. SABR density.** The one-year peak and ten-year negative tail are shown without clipping. A finite-interval integral near 0.63 excludes boundary mass. The effective one-dimensional PDE approximates full SABR; its finite-domain grid retains both boundary masses. Nonnegative probabilities and conserved mass do not make it the exact two-dimensional law. Shifted or normal quoting alone does not repair every asymptotic-formula defect. Bartlett's adjustment is an instantaneous covariance projection.
* **8. Jumps.** Merton, Kou and Bates under Q. Merton intensity is about 0.29/year and its mean log jump is about −44%; this is not a 44% mean proportional fall. Kou's reported IV RMSE is about 2.28 points. Bates approaches the finite intensity ceiling 20 and jump-size floor 0.01; this remains a jump model and does not prove the absence of crash risk. Its saved replay retains 300 observations from each longer evaluation trace, rather than every call.
* **9. Lévy clocks.** VG's gamma clock is strictly increasing despite finite-grid apparent flats. Real martingale drift requires 1−θν−σ²ν/2>0. An independent integrated CIR clock yields uncorrelated Heston. CGMY activity and variation regimes distinguish Y<0, 0≤Y<1 and 1≤Y<2; plotted counts use a 0.1% cutoff. The restored VG has ν≈0.0148 and MC call 0.05343±0.00018 versus COS 0.05352. The above-one CGMY fit gives Y≈1.67 and reported IV error≈2.49 points. Neither fit ranking identifies the true activity class. Full saved losses and signed log-density ranges are preserved.
* **10. Skew across maturities.** Finite-window regressions describe this calibration. Cumulants scale linearly when they exist; near-Gaussian Gram–Charlier gives a 1/T skew heuristic, not a universal short-time Lévy theorem. Regular positive-v₀ Heston has a finite ATM short-time limit. Other jump and rough regimes need their own analysis.
* **11. SLV.** Marginal matching is an ideal identity under existence and regularity assumptions. Particle repricing also contains Euler, kernel, subsampling, interpolation, floor and local-volatility errors. The original algorithm uses raw Euler variance in the kernel, floors conditional variance at 10⁻⁶ and has no leverage cap. All saved particles, including small negative Euler values, are shown. Log leverage preserves early wing estimates above 2,700 and the full 3D grid; unsupported wings are numerical, not identified market spikes. Three-seed ranges are descriptive. Reisinger–Tsianni's fixed-bandwidth regularized particle result uses Feller≥1 and a critical-time restriction; its separate Euler-time rate near 1/2 requires Feller>2+√3. Default η=1/2 gives effective Feller≈1.48; other theorem assumptions remain unverified.
* **12. Mixing fraction.** The saved cliquet grid is nonmonotone. Recalibration changes spatial leverage as well as variance diffusion: d(L√v)_diff=SLvL_SdW¹+(Lηξ/2)dW². There is no general monotone-price theorem in η. Exact vanilla invariance belongs to the ideal model; mean numerical repricing error reaches 3.4 points at η=1. FX exotic quotes can supply extra calibration information.
* **13. Bergomi.** A finite SSVI strip and linear total-variance interpolation produce a piecewise-constant forward curve. One weekend interval plus physical seasonality does not identify a weekend premium. Fixed absolute-date forward variance is a Q martingale; rolling-tenor slices are different. Omega uses a kernel-average heuristic, not exact index diffusion weighting or a joint DVOL calibration. The full Heston relative forward-variance diffusion peak near 958% is shown. At 90 days the illustrative curves give about 74% and 21%; these are variance diffusion magnitudes. SSR→2 is a local nonzero-skew short-time limit, not equality of full smile dynamics.
* **14. Forward starts and cliquets.** Contracts use fixed-notional ratio payoffs (S₂/S₁−K)⁺ at zero rates. The ordinary-Q CIR mixture applies to that contract; an S₁-weighted contract changes the weighting. Lévy stationarity repeats its own current smile, not the SSVI target. Current forward skews are LV 3.4, Heston 5.5, Bates 6.0, VG 5.3, SLV 5.1 points. The maximum three-seed MC-mean versus integral difference is about 0.8 points, a descriptive numerical check. Locally floored/capped coupons form call spreads; an additional active global floor needs joint information. The observed cliquet price range is about 9%, with the fit-error qualifications above.
* **15. Volatility-index illustration.** Q Heston simulations imply index vol of vol near 193%, versus historical DVOL near 89%. There are no Bitcoin volatility-option quotes or joint calibration test here. Girsanov preserves conditional instantaneous diffusion at a state, not unconditional daily variance, state occupancy or filtered-index statistics. Jensen compares matching Q dates, forward windows and index definitions; it does not bound an arbitrary spot-start variance swap. The floor and upward option smile are calibration-specific.
* **16. Calibration.** The full profile-loss landscape and weekly error range are retained. Price-over-vega residuals differ from reported vega-weighted IV RMSE. JᵀJ is Gauss–Newton in log first-four coordinates and raw ρ; profiling uses a Schur complement. The displayed 12% κ standard error requires independent correctly scaled errors and an adequate model, unverified here. For raw parameter coordinates, the code adds NλWᵀW to Gauss–Newton curvature (λWᵀW for the normalized objective); log-coordinate diagnostics require transforming those weights. This is not a uniform eigenvalue shift. Weekly and single-day maturity filters differ (>6 versus >2 days). Parameter stability does not itself establish improved hedging.
* **17. Industry and hedging.** Historical research affiliations and published results retain their dataset scope. The Bitcoin exercise is a synthetic 30-day ATM Black call proxy aged to 29 days using DVOL, without executable option marks, costs or funding. Fixed β uses 2021–22; rolling β uses strictly prior observations. In the numerical Heston experiment, MV error s.d.≈0.0254 versus unhedged≈0.080 removes about 90% of variance. Residuals include orthogonal shocks, discrete hedging and numerical grid effects. Heston uses C_S+C_vρξ/S with a variance Greek. EU Article 11's prudent exit-value procedure is not a five-model min–max confidence interval.
* **18. Frontier.** A finite κ sweep is not proof of the reversionary model's particular NIG scaling (H≤−1/2). Quintic OU uses six effective parameters plus an input curve; neural joint fits are reported on selected datasets. Choi–Kwok includes exact and approximate schemes. Wang et al. (2026) report synthetic 98.5 versus 0.6 ms, including 0.53 ms Dupire input, excluding quote ingestion and training. Exotic point errors without confidence intervals do not establish equivalence.
* **Research.** Analytic Riccati explosion controls continuous-model inverse-power integrability. Finite QE sample paths cannot prove explosion or finiteness. A bounded put and variance-swap/log payoffs are not inverse-power examples. All finite saved explosion times and sample means are shown. Lee gives a limsup ratio w(k)/|k|; actual ratio/derivative limits require additional tail results. Inverted finite quoted slopes are extrapolation proxies, not identified market moments. Rough Heston has a fractional/Volterra Riccati equation. A worked pause gives β(2)≈0.202, β(0⁺)=2 and β(∞)=0.
* **Recap and exercises.** Ten scoped conclusions, three desk questions and nine solved problems. The part counter remains **312**; the global counter remains **23,562**. Full continuous production-voice listening is a separate pending check.

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

1. **What sets Heston's skew and curvature?** For positive initial variance and regular short-time ATM asymptotics, skew tends to ρξ/(4√v₀). Finite-expiry skew and curvature depend on interacting parameters; an exponential damping multiplier is not a general exact formula.
2. **Which model for a cliquet?** A sum of locally capped/floored ratio returns depends on forward-start prices. Compare plausible calibrated joint dynamics and reconcile unequal vanilla and numerical errors before interpreting the observed price range. The local-volatility flattening in this example is calibration-specific.
3. **Which Jensen bound?** Under matching Q, date, window and index definition, E[I_T]≤√E[I_T²]. For small dispersion the gap is approximately Var(I_T)/(2E[I_T]). This is not an ordering of arbitrary market quotes or differently timed variance swaps.

## Problems, with solutions

1. **Heston's Riccati equations.**
   * Write x = ln S and τ = T − t. The price of a claim on x_T solves
     ∂_τ f = ½v(f_xx − f_x) + ρξv f_xv + ½ξ²v f_vv + κ(θ − v)f_v.
   * Substituting f = exp(C(τ) + D(τ)v + iux) and collecting the terms in v gives
     D′ = ½ξ²D² − (κ − ρξiu)D − ½(u² + iu), with D(0) = 0.
   * The terms without v give C′ = κθD, with C(0) = 0.
   * The solution is the little-trap form used in the House: d = √((κ − ρξiu)² + ξ²(iu + u²)).
2. **The short-maturity skew.**
   * For smooth positive local volatility, the BBF small-time relation is σ_imp(k)≈[∫₀¹du/σ_loc(uk)]⁻¹.
     Expanding to first order near k=0 gives the arithmetic local-variance expression below. The local variance is E[v | S]. Over a short time v − v₀ ≈ ξ√v₀W², and
     x ≈ √v₀W¹, so E[v | x] ≈ v₀ + ρξx.
   * Averaging along the line gives σ²_imp(k) ≈ v₀ + (ρξ/2)k, and hence ∂_kσ_imp = (ρξ/2)/(2√v₀) = ρξ/(4√v₀).
3. **The Lévy forward smile.**
   * The forward-start payoff (S_{t+τ}/S_t − e^k)⁺ depends only on the increment X_{t+τ} − X_t.
   * For a Lévy process that increment has the law of X_τ and is independent of the past.
   * At zero rates, the fixed-notional ratio price equals the model's own normalized current τ-option. An S_t-weighted contract needs a different weighting; this does not identify the SSVI target.
4. **Feller's condition.**
   * The scale density of CIR is s′(v) = v^{−2κθ/ξ²}·e^{2κv/ξ²}.
   * For v₀>0 and κθ>0, zero is reached with positive probability exactly when ∫₀ s′(v)dv < ∞, that is, when 2κθ/ξ² < 1.
5. **Why the leverage function works.**
   * The density p(S, t) of dS/S = L√v dW solves ∂_t p = ½∂_SS(S²L² E[v | S] p) (Gyöngy's mimicking theorem).
   * That is Dupire's forward equation exactly when L²E[v | S] = σ²_loc.
   * Under existence, regularity and the relevant forward-equation uniqueness assumptions, the ideal models share one-date marginals and vanilla prices. Finite particle approximations retain repricing errors.
6. **Merton's series.**
   * With zero rates, dS/S₋ = −λk̄dt + σdW + (e^J − 1)dN, J ~ N(μ_J, σ_J²), k̄ = e^{μ_J+σ_J²/2} − 1.
   * Given N_T = n, ln S_T is normal with mean ln S₀ − λk̄T − ½σ²T + nμ_J and variance σ²T + nσ_J²: a lognormal with
     forward F_n = S₀e^{−λk̄T + n(μ_J + σ_J²/2)} and volatility σ_n² = σ² + nσ_J²/T.
   * So C = Σ_n e^{−λT}(λT)^n/n! · C_BS(F_n, K, T, σ_n) (the House's `merton_series`, equal to COS to 10⁻⁸).
7. **The variance gamma characteristic function.**
   * X_t = θG_t + σW_{G_t}, with G_t ~ Γ(shape t/ν, scale ν).
   * Given G_t, X_t is normal: E[e^{iuX_t} | G_t] = e^{G_t(iuθ − σ²u²/2)}.
   * The gamma mgf E[e^{sG_t}] = (1 − νs)^{−t/ν} at s = iuθ − σ²u²/2 gives φ(u) = (1 − iuθν + ½σ²νu²)^{−t/ν}.
   * The martingale correction ω = (1/ν)ln(1 − θν − ½σ²ν) is real when 1−θν−σ²ν/2>0 and is added to the drift so that E[e^{X_t + ωt}] = 1.
8. **(qual) The explosion time.** With a, c > 0 and 4ac − b² = r² > 0, complete the square:
   ψ′ = a[(ψ + b/2a)² + r²/4a²]. Substituting ψ = (r/2a)tan θ − b/2a gives θ′ = r/2, so θ(t) = rt/2 + θ₀ with
   tan θ₀ = b/r (from ψ(0) = 0). ψ reaches infinity when θ = π/2: T* = (2/r)(π/2 − arctan(b/r)). For Heston,
   a = ξ²/2, b = ρξp − κ, c = (p² − p)/2, so 4ac − b² = −Δ. Moments of order p > 1 are finite for ever exactly when the
   quadratic has real roots (Δ ≥ 0) and b ≤ 0, so that ψ climbs to the smaller root and stops; with ρ < 0, b < 0
   always, and for κ = 2, ξ = 1, ρ = −0.7, Δ = −0.51p² + 3.8p + 4 ≥ 0 up to p = 8.39.
9. **(qual) Lee's formula inverted.** Write β = 2 − 4(√(q² + q) − q) and u = (2 − β)/4, so √(q² + q) = q + u;
   squaring, q = u² + 2qu, q(1 − 2u) = u², and 1 − 2u = β/2: q = (2 − β)²/(8β). At q = 2, √6 − 2 = 0.449, β = 0.202.
   As q → 0, β → 2 (the steepest wing Lee allows: fat tails). As q → ∞, √(q² + q) − q → ½ − 1/(8q), so β ≈ 1/(2q) → 0:
   a vanishing asymptotic total-variance ratio, which does not require a literally flat IV wing.

## For the researcher

* **The theorems.** Andersen and Piterbarg (2007), "Moment explosions in stochastic volatility models," *Finance
  Stoch.* 11; Lee (2004), "The moment formula for implied volatility at extreme strikes," *Math. Finance* 14;
  Benaim and Friz (2008, 2009) on regular variation and the lim sup as a limit; Gulisashvili and Stein (2010); Friz,
  Gerhold, Gulisashvili and Sturm (2011) for Heston's refined wing expansion; Keller-Ressel (2011) for affine models.
* **Simplifications.** Zero rates; the explosion time for the price's moments only (variance moments are another
  question); finite outer-quarter wing slopes are extrapolation proxies and need not equal asymptotic slopes;
  the critical exponent alone does not settle boundary integrability.
* **Open problems.** Wings beyond affine models (rough, SLV); robust extrapolation using second-order terms; the
  gap between risk-neutral and real-world tails.

## Reading guide

Every paper of Part 13's list in [`READING.md`](../READING.md) appears on screen; the newest ones:
Abi Jaber–De Carvalho (2023, reversionary Heston, chapter 18), Abi Jaber–Illand–Li (2023, quintic OU), Guyon–Mustapha
(2023, neural joint SPX/VIX), Choi–Kwok (2024, Poisson-conditioned simulation), Reisinger–Tsianni (2025, the particle
system's convergence), Wang–Després–Dureau–Buet-Golfouse (2026, neural operators for LSV, synthetic tests as reported),
Hou et al. (2020) and Matic–Packham–Härdle (2023) on bitcoin options.

Selected primary sources for the qualifications above: [Reisinger–Tsianni](https://arxiv.org/html/2504.14343v1), [reversionary Heston](https://arxiv.org/abs/2303.07222), [Choi–Kwok](https://arxiv.org/abs/2301.02800), [Wang et al.](https://arxiv.org/html/2608.01217v1), and [EU 2016/101 Article 11](https://eur-lex.europa.eu/eli/reg_del/2016/101/2016-01-28/eng).

## Data and reproducibility

* The Surface: pooled Deribit BTC option marks on 10 December 2025 (193 quotes, expiries from 3 to 289 days).
* Weekly surfaces: every Wednesday from 3 January 2024 to 26 November 2025 (100 days), as in Part 12.
* Binance BTCUSDT daily (2021-04 to 2025-11) and hourly (2024–2025); Deribit DVOL daily; S&P 500 daily 1986–1987.
* No strategy was tested (the minimum-variance delta is descriptive hedging); the trial counter is unchanged at 312.

---

# 量化金融，从零搭建 — 第13部分：随机波动率与跳跃

约61分钟，包含开场、十八章、研究者章节与结尾。采用原始计算和House算法；本轮只修改说明与显示，不运行新策略试验或打开留出样本。输入为2025年12月10日00–12 UTC汇集的Deribit期权标记，参考时点08 UTC，筛选后193个观测，并非同时可执行成交。五种模型的普通期权拟合误差不同，因此奇异价差同时包含动态、拟合和数值误差，不是置信区间。

*讲的是方法，不构成投资建议。*

## 各章（约61分钟）

* **开场。** 棘轮占本金价格：局部波动率13.73%、赫斯顿13.04%、Bates 13.31%、方差伽马14.23%、SLV 13.67%，相对均值范围约9%；不能把全部价差归为纯动态风险。
* **1. 波动率变化。** 已实现波动率17%–122%，DVOL对数变化波动率约89%。同期相关与其平方只描述线性关系；残差不能证明独立冲击，也不能排除GARCH。有限绝对收益自相关不等于渐近长记忆。54天半衰期是经验AR(1)结果；1987年高斯尾概率采用此前250天固定波动率，并非真实崩盘概率。
* **2. 混合。** 40条条件高斯路径是有限混合示意，下图IV另由COS计算。对w=σ²展开时，C_ww=vega(d₁d₂−1)/(4σ³)。非零相关赫斯顿给定方差路径仍为高斯，但均值平移，剩余方差缩放。91步QE与梯形积分的条件估计仍有离散偏差；约七倍抽样误差改善不包含该偏差。
* **3. 赫斯顿特征函数。** 仿射猜测、黎卡提解、分支约定与小陷阱，以及价格基准。变换衰减本身不能诊断所有尾部性质。
* **4. 参数与拟合。** 参数相互作用，完整显示三个起点保存的损失，包括超过25的初值。ρξ/(4√v₀)是正则短时局部平值极限。BBF关系对局部波动率采用调和形式，算术局部方差式仅是一阶平值展开。ξ与DVOL百分数不可直接相比。
* **5. 模拟。** CIR费勒条件不满足时零点可达，但正回复水平下正时点分布没有零点原子。QE原子是数值产物；匹配条件总体矩并不保证有限样本精确均值，QE-M还需分支矩生成函数存在。
* **6. SABR。** dF=αF^βdW，ρν/2斜率针对β=1的领先短时近似。哈根公式是渐近近似；27参数独立切片不自动保证日历无套利。布莱克与正态报价不同，黏性回归不能识别β。
* **7. SABR密度。** 完整显示一年峰与十年负尾。约0.63的有限区间积分不含边界质量。有效一维PDE近似完整SABR，保留两侧边界质量；网格非负与质量守恒不代表精确二维分布。平移或改正态报价本身不能修复所有公式缺陷，巴特利特修正是瞬时协方差投影。
* **8. 跳跃。** 默顿Q强度约0.29/年，平均对数跳约−44%，并非平均价格跌幅44%。寇IV误差约2.28点。Bates接近强度上限20、跳幅下限0.01，仍为有限跳跃模型，不能证明无崩盘风险；回放每条保存300个评估观测，并非每次调用。
* **9. 莱维时钟。** 伽马时钟严格递增，表面平坦源于有限分辨率。VG鞅修正需1−θν−σ²ν/2>0；独立积分CIR时钟只给出零相关赫斯顿。CGMY区分有限活动、有限变差与无限变差，显示跳数采用0.1%截断。恢复的VG ν约0.0148，MC价格0.05343±0.00018，COS 0.05352；CGMY Y约1.67、IV误差约2.49。拟合排序不能识别真实活动类别。
* **10. 期限斜率。** 有限窗口幂回归只描述本次拟合。存在时累积量线性缩放，近高斯Gram–Charlier的一除以T是启发式，并非普遍莱维短时定理。其他跳跃与粗糙情形需要单独分析。
* **11. SLV粒子。** 精确边缘匹配要求存在性与正则条件。有限粒子还有欧拉、核、子采样、插值、下限与局部波动率误差。原算法以原始欧拉方差做核估计，条件方差下限10⁻⁶，没有杠杆上限；保留全部保存粒子和少量负方差。对数显示早期稀疏翼部超过2700的杠杆及完整三维网格，不能视为经济尖峰。固定带宽正则化粒子定理要求费勒比至少一及临界时间限制；另一个欧拉时间收敛结果要求费勒比大于二加根号三。默认eta为一半时约1.48，其他假设未验证。
* **12. 混合比例。** 保存的棘轮网格非单调。总波动率扩散包含空间杠杆导数，重新校准也改变L，因此没有普遍eta单调价格定理。理想普通期权不变，不等于粒子数值不变；eta为一时平均误差达3.4点。
* **13. Bergomi。** 有限SSVI条带和总方差线性插值给出分段常数远期方差；一个周末区间不能识别风险溢价。固定绝对日期方差是Q鞅，滚动期限切片不同。omega采用核平均启发式，并非精确指数加权或联合校准。完整显示赫斯顿约958%的相对远期方差扩散；90天约74%对21%，单位针对方差。SSR趋于二只是局部非零斜率短时极限。
* **14. 远期与棘轮。** 零利率固定本金比率收益(S₂/S₁−K)⁺采用普通Q的CIR方差混合；乘S₁的合约需要不同权重。莱维重复自己当前微笑，并非SSVI目标。当前远期斜率分别为3.4、5.5、6.0、5.3、5.1点；MC均值与积分最大约差0.8点，是描述性检查。局部保底封顶票息为看涨价差；另加生效全局保底需联合信息。棘轮范围约9%，含拟合与数值误差。
* **15. 指数示例。** Q模拟指数波动率之波动率约193%，历史DVOL约89%；没有比特币指数期权报价，不能进行联合校准检验。吉尔萨诺夫只保留同一状态的条件瞬时扩散，不保证无条件日方差或过滤指数统计一致。詹森要求同一Q、日期、窗口和指数定义。
* **16. 校准。** 保留完整损失地形与每周误差范围。价格除以vega残差不同于报告的vega加权IV误差。高斯–牛顿矩阵采用前四参数对数坐标和原始rho，剖面使用舒尔补；12%的kappa标准误差依赖未经验证的独立正确尺度误差与适当模型。原始参数坐标中，代码增加N lambda W转置W；归一化目标则为lambda W转置W，对数坐标还需转换权重，并非统一特征值平移。每周和单日期限过滤分别超过六天、两天；稳定性不是实测对冲改善。
* **17. 业界与对冲。** 历史任职与论文结论保留各自范围。比特币练习是DVOL驱动的30天平值布莱克代理，次日剩29天，无可执行标记、成本或融资。固定beta使用2021–22，滚动beta严格使用过去数据。数值赫斯顿中，MV标准差约0.0254，未对冲约0.080，移除约九成方差；残差还含离散与网格误差。公式使用方差敏感度C_v。欧盟第11条审慎退出价值不是五模型最小最大置信区间。
* **18. 前沿。** 有限kappa扫描不能证明特定NIG缩放极限H≤−1/2。五次OU为六有效参数加输入曲线，神经联合拟合仅对报告数据集成立。Choi–Kwok含精确和近似方案。Wang等（2026）合成基准98.5对0.6毫秒，含0.53毫秒杜皮尔输入，不含接入与训练；无置信区间的奇异点误差不证明统计等价。
* **研究者。** 解析黎卡提爆炸决定连续模型负幂可积性，有限QE样本不能证明爆炸或有限。有界看跌、方差互换和对数收益不能当作负幂例子。显示全部有限爆炸时间与样本均值。Lee给出w(k)/|k|上极限；导数极限需更强尾部条件。反演有限报价斜率只得到外推代理；粗糙赫斯顿有分数阶或Volterra黎卡提方程。暂停题给出完整答案0.202、二与零。
* **结尾。** 十点回顾、三个交易台问题、九道完整解答。分部计数312，全局23,562。连续生产语音完整聆听仍需单独完成。

## 交易台问题与解答

1. **什么决定赫斯顿斜率？** 正初始方差下，正则短时平值极限为ρξ/(4√v₀)；有限期限斜率和曲率涉及参数相互作用，指数衰减乘子不是一般精确公式。
2. **如何选择棘轮模型？** 比较合理联合动态，在解释奇异价差之前核对普通期权拟合与数值误差。本例局部波动率远期变平不是普遍定理。
3. **詹森上界如何使用？** 同一Q、日期、远期窗口与指数定义下，E[I_T]≤√E[I_T²]。小离散程度时差值近似Var(I_T)/(2E[I_T])；不能对任意市场报价或不同时段方差互换排序。

## 习题与解答

1. **赫斯顿的里卡蒂方程。**
   * 记x = ln S，τ = T − t。关于x_T的权益价格满足∂_τ f = ½v(f_xx − f_x) + ρξv f_xv + ½ξ²v f_vv + κ(θ − v)f_v。
   * 代入f = exp(C(τ) + D(τ)v + iux)，收集含v的项得D′ = ½ξ²D² − (κ − ρξiu)D − ½(u² + iu)，D(0) = 0。
   * 不含v的项给出C′ = κθD，C(0) = 0。
   * 其解就是公司使用的“小陷阱”形式：d = √((κ − ρξiu)² + ξ²(iu + u²))。
2. **短期限偏斜。**
   * 光滑正局部波动率下，BBF短时关系为σ_imp(k)≈[∫₀¹du/σ_loc(uk)]⁻¹。对k=0作一阶展开，才得到下述算术局部方差近似。局部方差是E[v | S]；短时间内v − v₀ ≈ ξ√v₀W²，x ≈ √v₀W¹，所以E[v | x] ≈ v₀ + ρξx。
   * 沿直线平均得σ²_imp(k) ≈ v₀ + (ρξ/2)k，从而∂_kσ_imp = (ρξ/2)/(2√v₀) = ρξ/(4√v₀)。
3. **莱维模型的远期微笑。**
   * 远期起始收益(S_{t+τ}/S_t − e^k)⁺只依赖增量X_{t+τ} − X_t。
   * 对莱维过程，这个增量与X_τ同分布，且独立于过去。
   * 零利率、固定本金比率收益的价格，等于模型自己当期标准化τ期价格。若乘S_t，需要不同权重；这不能识别SSVI目标。
4. **费勒条件。**
   * CIR的尺度密度为s′(v) = v^{−2κθ/ξ²}·e^{2κv/ξ²}。
   * v₀>0、κθ>0时，当且仅当∫₀ s′(v)dv < ∞，即2κθ/ξ² < 1时，零点可达。
5. **杠杆函数为什么有效。**
   * dS/S = L√v dW的密度p(S, t)满足∂_t p = ½∂_SS(S²L² E[v | S] p)（久永的模仿定理）。
   * 当L²E[v | S] = σ²_loc时，这正是杜皮尔的前向方程。
   * 在存在性、正则性及相应前向方程唯一性假设下，理想模型具有相同单时点边缘分布和普通期权价格。有限粒子近似仍有误差。
6. **默顿级数。**
   * 零利率下dS/S₋ = −λk̄dt + σdW + (e^J − 1)dN，J ~ N(μ_J, σ_J²)，k̄ = e^{μ_J+σ_J²/2} − 1。
   * 给定N_T = n，ln S_T服从均值ln S₀ − λk̄T − ½σ²T + nμ_J、方差σ²T + nσ_J²的正态分布：远期F_n = S₀e^{−λk̄T + n(μ_J + σ_J²/2)}，波动率σ_n² = σ² + nσ_J²/T。
   * 所以C = Σ_n e^{−λT}(λT)^n/n! · C_BS(F_n, K, T, σ_n)（公司的`merton_series`，与COS相差小于10⁻⁸）。
7. **方差伽马的特征函数。**
   * X_t = θG_t + σW_{G_t}，G_t ~ Γ(形状t/ν，尺度ν)。
   * 给定G_t，X_t是正态的：E[e^{iuX_t} | G_t] = e^{G_t(iuθ − σ²u²/2)}。
   * 伽马分布的矩母函数E[e^{sG_t}] = (1 − νs)^{−t/ν}在s = iuθ − σ²u²/2处取值，得φ(u) = (1 − iuθν + ½σ²νu²)^{−t/ν}。
   * 要求1−θν−σ²ν/2>0后，将实数鞅修正ω = (1/ν)ln(1 − θν − ½σ²ν)加到漂移上，使E[e^{X_t + ωt}] = 1。
8. **（资格考试）爆炸时间。** a, c > 0且4ac − b² = r² > 0时配方：ψ′ = a[(ψ + b/2a)² + r²/4a²]。代入ψ = (r/2a)tan θ − b/2a得θ′ = r/2，θ(t) = rt/2 + θ₀，由ψ(0) = 0得tan θ₀ = b/r。θ = π/2时ψ达到无穷：T* = (2/r)(π/2 − arctan(b/r))。对赫斯顿，a = ξ²/2，b = ρξp − κ，c = (p² − p)/2，所以4ac − b² = −Δ。p > 1阶矩永远有限，恰当二次式有实根（Δ ≥ 0）且b ≤ 0，此时ψ爬到较小的根并停下；ρ < 0时b总为负，κ = 2、ξ = 1、ρ = −0.7时Δ = −0.51p² + 3.8p + 4 ≥ 0直到p = 8.39。
9. **（资格考试）反解李的公式。** 记β = 2 − 4(√(q² + q) − q)，u = (2 − β)/4，则√(q² + q) = q + u；平方得q(1 − 2u) = u²，而1 − 2u = β/2：q = (2 − β)²/(8β)。q = 2时√6 − 2 = 0.449，β = 0.202。q → 0时β → 2（李允许的最陡的翼：肥尾）。q → ∞时√(q² + q) − q → ½ − 1/(8q)，β ≈ 1/(2q) → 0：渐近总方差比率趋于零，并不要求IV翼部严格水平。

## 写给研究者

* **定理。** 安德森与皮捷尔巴格（2007），*Finance Stoch.* 11；李（2004），*Math. Finance* 14；贝纳伊姆与弗里茨（2008、2009）论正则变化与上极限即极限；Gulisashvili与Stein（2010）；Friz、Gerhold、Gulisashvili与Sturm（2011）论赫斯顿两翼的精细展开；Keller-Ressel（2011）论仿射模型。
* **简化。** 零利率；只讨论价格矩的爆炸时间（方差的矩是另一个问题）；有限行权价外侧四分之一的斜率只是外推代理，不必等于渐近斜率；临界指数也不能独自判断边界可积性。
* **开放问题。** 仿射模型之外的两翼（粗糙、SLV）；用二阶项稳健外推；风险中性尾部与现实尾部之差。

*Review log of the earlier QA passes on this part: [`docs/qa/quant/part13.md`](../../../docs/qa/quant/part13.md).*
