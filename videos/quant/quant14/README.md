# Quant, Built — Part 14: Rough and Path-Dependent Volatility

Part 14 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), in Act III, Derivatives. It is the series' frontier part on volatility: a lecture of
about 65 minutes, with every number computed by the series' own code ([`compute.py`](compute.py) and the House's
[`rough`](../../../explainer/quant/house/rough.py) module, tested in `tests/test_quant_house.py`).

The data: the Surface and 102 original-manifest Deribit BTC option-mark dates (2024–2025); Binance BTCUSDT 1-minute (2018–2020),
5-minute (2024–2025) and daily (2018–2025); Deribit DVOL (hourly and daily); FRED VIXCLS and NIKKEI225; Ken French's
daily market return; Part 13's cached Heston, Bates and forward variance curve.

*An education in methods, not investment advice.*

## Chapters (about 65 minutes of narration)

* **Hook.** Finite-grid Brownian and H=0.1 paths under a ×256, independently range-normalized zoom. Both theoretical processes are self-similar and nondifferentiable; apparent straight segments are a resolution limit.
* **1. Finite-maturity skew magnitudes.** All 102 original manifest dates are retained: 101 Wednesdays and one Thursday, from 3 January 2024 to 11 December 2025. Eight power-fit exponents are negative; 410 of 812 signed skew observations are positive. The histogram preserves negative exponents and the log plot preserves magnitudes down to 0.00104. These finite-window absolute-value fits do not establish a persistent-sign zero-maturity explosion. Weekly optimization uses record-count weights but reports unweighted log RMSE; power and shifted exponents have different bounds, so the families are not fully nested. The 0.01 improvement threshold is descriptive, without a significance test or complexity penalty.
* **2. Skew from a kernel.** Signed s(T)=∂kσ_imp(0,T), plotted ψ=|s|. Flat-forward-variance, small-vol-of-vol leading formulas distinguish exponential and singular power kernels. The roof is scaled/capped for visibility; right-hand integrals are analytical and uncapped. Fukasawa's theorem has positive continuous Itô prices, positive Hölder variance, persistent-sign near-ATM limiting skew and frictionless continuum-option assumptions; these data do not verify them. The illustrative κ=2 differs from Part 13's fitted κ≈14.77. The red model has constant diffusion plus Bates jump parameters, not jumps alone.
* **3. Measuring roughness.** Actual free-intercept regression of empirical ζq on q; known-H checks use one fixed simulated path per H, not a bias study. Two-era realized-variance estimates describe finite lags, aggregation and noise, not a directly observed instantaneous or risk-neutral H. Full path ranges and the worked ζ2/2=1/2 answer are shown.
* **4. Rough predictor and HAR.** Conditional-mean fBm formula, then finite-window normalized weights. The latest weight uses today's observation. Coefficients expand/refit every 20 days, but H uses each entire era, including test dates: a retrospective comparison, not fully real-time forecasting. Rough wins 2 of 6 head-to-heads with HAR. R² uses each test period's own mean; all 20-day scores are negative. Predictive tails, local roughness and conventional long-range dependence are distinct.
* **5. Rough Bergomi.** Riemann–Liouville driver, not full stationary-increment fBm. Gaussian compensation matches the supplied expected-variance curve; fixed-future-date forward variance is a martingale. Neither statement makes instantaneous variance or the stock a martingale automatically. Standard stock results require separate conditions, including the nonpositive-correlation case discussed here. Headline fit H≈0.0326, η≈2.0478, ρ≈−0.5608, same-date IV error≈0.8338 points on fresh paths. The variance curve is an additional finite-strike market input. Fresh RNG seeds are not unseen market dates. Full saved replay smiles and paths are retained.
* **6. Hybrid scheme.** Exact nearest-cell Wiener integral and optimal cell-average points for remaining cells; FFT convolution. The sliding illustration uses truncated far-end weights and a standardized output. Recorded hybrid and Riemann comparisons have finite-grid/MC error. Cholesky timing uses full fBm covariance whereas hybrid timing uses the Volterra driver, so the cost comparison is not an identical-law accuracy benchmark.
* **7. Rough Heston.** Affine Volterra formulation and fractional Riccati representation. The initial memory illustration caps only the singular kernel; all numerical variance excursions are preserved, including negatives from the floored-square-root simulation. Free and fixed-H fits are local numerical calibrations, without statistical equivalence or latent-H identification.
* **8. Adams.** Predictor/corrector weights, memory fan, observed order≈1.76 against a 1,600-step reference, and Heston-limit check≈7.11×10⁻⁷. No universal convergence rate follows from this experiment. Characteristic-function modulus cannot determine skewness sign. The nine-point H profile preserves the H=0.05 error≈4.44 and expiry errors above 10, previously hidden by limits at 2.4 and 6. The time-series band is descriptive, not a risk-neutral-H confidence interval.
* **9. Hawkes mechanism.** Stationary branching identities are separated from empty-history finite simulations. The heavy-tail nearly critical theorem requires α∈(1/2,1) and coordinated baseline/time/amplitude scaling, yielding an integrated fractional-CIR limit. One normalized/downsampled zoom is not that limit. Fixed-bin estimates near zero can reflect count noise; increasing fitted H does not mean increasing local roughness. The original tail sweep does not recover H=α−1/2 for all tails.
* **10. Markovian lifts.** Positive geometric quantization of the exact continuum exponential mixture. Six decades suggesting six factors is only a heuristic, not an accuracy guarantee. Thin factor curves below 0.1 are omitted explicitly; the sum contains every factor. The path reference is cell-averaged Volterra Euler, not an exact continuous path. Root mean squared coupled distance is≈0.911 at N=1,≈0.505 at N=50 and≈0.346 at N=200, in reference standard deviations. Smile comparisons use numerical Adams/COS and finite Riccati/COS solvers.
* **11. Measurement debate.** Weekday effects, three Brownian-regular variance examples and a 64-cell map averaging four fixed seeds per cell. Interpolated equal-reading contours are not confidence sets or equal-law proofs. A simple independent additive log-noise floor is stated for q=2. The parametric high-frequency-price minimax rate n^{−1/(4H+2)} gets faster as H decreases; it does not certify the daily estimator.
* **12. Options debate.** Weekly shifted fits are an in-sample comparison. Published horse races retain their model/sample scope; Livieri et al. study temporal implied-volatility proxies. Several exponential scales can imitate power-like behavior over finite windows for suitable amplitudes; two decay rates do not fix a unique exponent. Same-date model errors have different numerical methods and parameter restrictions.
* **13. Path-dependent volatility.** Return-history regressions track DVOL, an implied index. Training is 2021–2023, then coefficients freeze for later dates; features include the target day's return, so this is contemporaneous held-out-date tracking. Power-law R²≈0.424 and four-factor R²≈0.524 are not advance forecasts or evidence that all independent volatility innovations vanish. Component standard deviations are correlated and are not causal/incremental contributions; the trend exponent hits a bound. Continuous feedback-SDE theorems require a specified sign/parameter domain and positive initial activity; positivity and stock martingality are separate from existence. The unconstrained daily regression does not verify those hypotheses.
* **14. VIX and August 2024.** Ken French's market return is a proxy for SPX, aligned with the same day's VIX close. The frozen 2000–2018 fit tracks 2019–2025 with R²≈0.849, against≈0.562 for the realized-volatility baseline. A regression residual is not everything any possible path model misses. August 5's close and pre-open VIX high are different timestamps; the PDV estimate includes that day's return. BIS/DERA quote-mechanism studies do not causally decompose this close residual. Bitcoin daily realized volatility and thirty-day DVOL also have different horizons.
* **15. Joint modeling and transport.** Part 13 used a Bitcoin volatility-index illustration, without joint SPX/VIX calibration. qRH paths use the paper's six quoted parameters plus η=1 chosen here, a 10-factor lift and daily discretization. Weak Zumbach correlations compare illustrative Q simulations with overlapping historical P windows, without a statistical test; leverage alone can also generate weak asymmetry. The transport illustration truncates/discretizes SVI densities and adjusts the second support to convex order. Entropic objectives≈0.06653/0.16002 are interior values; the unregularized LP grid extrema≈0.06393/0.16230 are wider. These are not rigorous bounds on the full original smiles. Separate rough-Bergomi MC≈0.14484 is a comparison, not a marginal-matching certificate. There is no VIX marginal or conditional-log-contract constraint in this solver.
* **16. Signature volatility.** Depth-3 time/Brownian signature, 15 loadings plus correlation, log S=ℓᵀA−½ℓᵀBℓ. Option calibration remains nonlinear. Universality requires increasing depth on suitable compact path sets and topology. Loadings may be signed. Each simulated terminal sample is normalized by its mean: this numerical correction does not prove one dynamically consistent true-martingale model. Same-date IV error≈0.8848 on calibration paths and≈1.4815 on fresh paths, with no future-market validation.
* **17. Numerical speed and the lab.** Single pricing-map timings, not whole calibrations. The Part 17 neural/MC ratio belongs to its own original synthetic benchmark; it excludes training and is not directly interchangeable with the other bars' outputs/accuracy. Surrogate domains, optimizer work and curve hedging assumptions remain material. Same-date fits, retrospective predictors and contemporary index tracking do not by themselves pass Rule 14's adoption requirement.
* **18. Selected research, 2023–2025.** Bayer–Breneis superpolynomial strong convergence uses Gaussian quadrature and Lipschitz coefficients, not a universal rate for the implemented geometric lift. Forest expansions need convergence/truncation assumptions. Regularity structures address singular expansions; the adapted stock Itô integral still exists. Bounded kernels need not generate differentiable volatility.
* **Research.** For 0<H<1/2, a uniform grid and fixed admissible within-cell rules give RMSE of order n⁻ᴴ; fixed κ exact hybrid cells reduce the constant. This is not a lower bound for every mesh or approximation class; growing κ is a different regime. The cached `riemann_opt` variant still uses a far-end first cell and optimal points only from cell 2; it is not plotted as the globally optimal step scheme. Four price grids share the stock Euler step, so comparison with an exact-grid Gaussian driver excludes continuous stock-discretization error. The driver variance deficit has order n⁻²ᴴ; no universal price rate follows. Bayer–Hall–Tempone's H+1/2 weak result concerns linear rough Stein–Stein under payoff assumptions. The closing implementation questions do not claim an exhaustive current-literature list of open problems. Halving asymptotic error requires 2¹/ᴴ times the steps: 1,024 at H=0.1, 5.66 at H=0.4.
* **Outro.** Qualified recap, four desk questions and ten worked problems, preserving original calculations and adding visible answers.

## Textbook audit

| Textbook section | Chapter |
|---|---|
| *Rough Volatility* (SIAM 2023) ch. 1, Volatility is rough (Gatheral–Jaisson–Rosenbaum) | 3, 4 |
| ch. 2, Pricing under rough volatility (Bayer–Friz–Gatheral) | 5 |
| ch. 3, No-arbitrage implies power-law impact and rough volatility (Jusselin–Rosenbaum) | 9 (card; impact → Part 37) |
| ch. 4, Rough Heston (Gerhold–Jacquier–Rosenbaum) | 7, 8 |
| ch. 5, Rough affine models (Keller-Ressel–Larsson–Pulido) | 7, 10 |
| ch. 6, Hedging under rough volatility (Fukasawa–Horvath–Tankov) | 17 |
| ch. 7, Hybrid scheme (Bennedsen–Lunde–Pakkanen) | 6 |
| ch. 8, Asymptotics (Bayer–Friz–Fukasawa–Jacquier) | 2 |
| ch. 9, Forest expansion (Friz–Gatheral) | 2, 18 |
| ch. 10, Regularity structures (Bayer–Friz–Gassiat–Martin–Stemper) | 18 (card; the theory is beyond the series) |
| Guyon–Henry-Labordère, *Nonlinear Option Pricing* ch. 10–11 (McKean SDEs; particle calibration of LSV) | 13 (calibrating PDV to smiles is a McKean problem; README note); Part 13 |
| GHL ch. 9 (UVM), ch. 12 (local correlation), ch. 4–7 (nonlinear PDEs, BSDEs) | Parts 15, 16, 17 |
| GHL ch. 8 (uncertain lapse and mortality) | not covered (insurance) |
| Bergomi, *Stochastic Volatility Modeling*: forward variance models; the smile at first order in vol of vol | 2, 5, 12 |
| Gatheral, *The Volatility Surface*: skews of stochastic volatility and jump models | 2 |
| Friz–Hairer, *A Course on Rough Paths* (2nd ed. 2020) §14.5 | 18 |

## Papers

Comte–Renault 1998 (4); Alòs–León–Vives 2007 (2); Fukasawa 2011, 2021 (2); Bayer–Friz–Gatheral 2016 (2, 5);
Jaisson–Rosenbaum 2016 (9); Bennedsen–Lunde–Pakkanen 2017 (6); Gatheral–Jaisson–Rosenbaum 2018 (3, 4); El Euch–
Fukasawa–Rosenbaum 2018 (9); Livieri–Mouti–Pallavicini–Rosenbaum 2018 (12); Bayer–Stemper 2018 (17); El Euch–Rosenbaum
2019 (7, 8); Abi Jaber–El Euch 2019, Abi Jaber 2019 (10); Gatheral–Jusselin–Rosenbaum 2020 (15); Guyon 2020 (15);
Horvath–Muguruza–Tomas 2021 (17); Fukasawa–Takabatake–Westphal 2022 (11); Rømer 2022 (12, 17); Rosenbaum–Zhang 2022
(17); Guyon–El Amrani 2023 (Risk, 1, 12); Guyon–Lekeufack 2023 (13, 14); Cuchiero–Gazzani–Svaluto-Ferro 2023 (16);
Bolko–Christensen–Pakkanen–Veliyev 2023 (11); Bayer–Breneis 2023 (18); Guyon 2024, *Finance Stoch.* 28(1) (15);
Cont–Das 2024 (11); Chong–Hoffmann–Liu–Rosenbaum–Szymanski 2024 (11); Nutz–Riveros Valdevenito 2024, Andrès–Jourdain
2025 (13); Abi Jaber–Li 2025 (12, 18); Cuchiero–Gazzani–Möller–Svaluto-Ferro 2025 (16). Industry: BIS Bulletins 90
and 95 (2024), Li–Askanazi SEC DERA working paper (2025), Cboe VIX1D (2023).

## Build it

```bash
python -m videos.quant.quant14.compute                    # every number (~2 CPU-hours; long items resume)
EXPLAINER_TTS=silent python tools/qa_scene.py quant14 Rough   # one chapter, silent, with a contact sheet
python tools/make.py quant14 --cpu-voice -q m             # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **One-day versus one-month skew at H≈0.1?** Conditional on the appropriate power approximation holding over that interval, the magnitude ratio is 30^0.4≈3.9. This does not order total risk: Greeks, notional and payoff matter.
2. **Roughness or fast mean reversion?** Use several noise-aware measurements, sub-daily lags, expiry structure and truly prospective forecasts/hedges. A daily proxy exponent or one calibrated H is insufficient.
3. **Faster calibration?** Benchmark surrogates, lifts and Fourier methods at matched output/accuracy. Include offline training, approximation domain, optimizer work and data handling. A single fast evaluation is not a completed calibration.
4. **Does one factor rule out a one-week fit?** No. Regular positive-variance Itô models have bounded local short-time skew under standard conditions, but can fit finite observations. A single exponential's leading flat-to-1/T transition is a restricted illustration; other scales, amplitudes and initial curves matter. One week is not T→0.

## Problems, with solutions

1. **Variance of W^H.** By the Itô isometry, Var W^H_t = 2H ∫₀ᵗ (t − s)^{2H−1} ds = t^{2H}.
2. **Scaling.** fBm has stationary Gaussian increments with variance Δ^{2H}, so B^H_{t+Δ} − B^H_t has the law of Δ^H Z
   and E|·|^q = Δ^{qH} E|Z|^q; hence ζ_q = qH.
3. **Rough Bergomi's forward-variance identity.** W^H_t is Gaussian with variance t^{2H}, so E[exp(ηW^H_t − ½η²t^{2H})] = 1
   and E[v_t] = ξ₀(t). Conditionally on F_s, the part of the integral after s is independent Gaussian with variance
   ∫_s^t 2H(t − u)^{2H−1}du; the same computation makes ξ_s(t) = E_s[v_t] an exponential martingale in s for each fixed future t. This is separate from stock true-martingality and does not make v a martingale.
4. **The lift's identity.** Substituting y = xt, ∫₀^∞ e^{−xt}x^{−α}dx = Γ(1 − α)t^{α−1}; dividing by Γ(α)Γ(1 − α)
   gives t^{α−1}/Γ(α). Quantising x^{−α}dx/(Γ(α)Γ(1 − α)) on a geometric grid gives the weights c_i and nodes x_i.
5. **The Hawkes mean rate.** At stationarity Λ = μ + Λ‖φ‖₁, so Λ = μ/(1 − ‖φ‖₁); as ‖φ‖₁ → 1 the rate and each
   event's expected number of descendants ‖φ‖₁/(1 − ‖φ‖₁) explode: "nearly unstable".
6. **The rough double integral.** ∫_t^T (u − t)^{H−½}du = (T − t)^{H+½}/(H + ½); integrating again in t gives
   T^{H+3/2}/((H + ½)(H + 3/2)). Divided by T², the first-order skew is ∝ T^{H−½}.
7. **The hybrid scheme's b_k.** The cell k steps back covers lags [(k − 1)Δ, kΔ]; the kernel's average there is
   (1/Δ)∫ x^{H−½}dx = Δ^{H−½}(k^{H+½} − (k − 1)^{H+½})/(H + ½). Setting (b_kΔ)^{H−½} equal to it gives
   b_k = ((k^{H+½} − (k − 1)^{H+½})/(H + ½))^{1/(H−½)}.
8. **The 4-factor PDV.** With K(τ) = λe^{−λτ}, R_t = ∫ λe^{−λ(t−u)} (r_u^n/Δt) du (piecewise-held daily return-rate input); differentiating,
   dR = λ(r_t^n/Δt − R_t)dt: an exponential moving average, Markov. A convex mix of two such kernels is a mix of two
   EMAs: four factors for R₁ and R₂.
9. **(qual) The exact strong error.** Y₁ − Ŷ₁ = √(2H)Σ_j∫_{cell j}((1 − s)^a − (c_jΔ)^a)dW_s, so by Itô's isometry
   E|Y₁ − Ŷ₁|² = 2HΣ_j∫_{(j−1)Δ}^{jΔ}(r^a − (c_jΔ)^a)²dr; with r = xΔ this is 2HΔ^{2a+1}Σ_j∫_{j−1}^{j}(x^a − c_j^a)²dx
   and 2a + 1 = 2H. For a fixed admissible within-cell rule and 0<H<1/2, for large j, x^a − c_j^a ≈ a c_j^{a−1}(x − c_j), so the j-th term is O(j^{2a−2}), summable since
   2a − 2 < −1. Each cell's term is minimized over c_j when c_j^a equals the cell average of x^a, which is
   (j^{a+1} − (j − 1)^{a+1})/(a + 1): c_j = b_j.
10. **(qual) The naive scheme's bias.** Var Ŷ₁ = 2HΔ^{2H}Σ_{j≤n}j^{2a}, and for s = −2a = 1 − 2H ∈ (0, 1),
   Σ_{j≤n}j^{−s} = n^{1−s}/(1 − s) + ζ(s) + O(n^{−s}). So Var Ŷ₁ = 1 + 2Hζ(1 − 2H)Δ^{2H} + o(Δ^{2H}), with ζ(1 − 2H) < 0.
   Then E[exp(ηŶ₁ − ½η²)] = exp(½η²(Var Ŷ₁ − 1)) = exp(−η²H|ζ(1 − 2H)|Δ^{2H} + o(Δ^{2H})): at H = 0.1, ζ(0.8) = −4.44, and
   with η = 1.9 the leading-order factor is exp(−1.60Δ^{0.2}), about 0.50 at n = 64. Using Var Ŷ in the exponent instead removes this bias.

## For the researcher

* **The theorems.** Bennedsen, Lunde and Pakkanen (2017), "Hybrid scheme for Brownian semistationary processes,"
  *Finance Stoch.* 21(4); Bayer, Hall and Tempone (2022), "Weak error rates for option pricing under linear rough
  volatility," *IJTAF* 25 (linear rough Stein–Stein, payoff assumptions; not a universal rough-Bergomi weak rate); Gassiat (2022), arXiv:2203.09298, on weak rates
  of rough schemes.
* **Simplifications.** The error at one time, t = 1; the price experiment fixes the price step and varies only the
  volatility's discretization, with the exact Y on the grid as reference, so the S-step's own error is not measured.
* **Implementation questions.** Check the applicable theorem, coupling cost and target-specific error expansion. This part does not establish rates for general nonlinear or path-dependent targets, and does not claim a complete current-literature survey.

## Data and reproducibility

* Every number is computed by `compute.py` and cached in `.cache/quant14/`; long items (`skew_weekly`, `rb_replay`,
  `rh_profile9`, `bias_map`) save their pieces and resume.
* Facts checked against primary sources: the qRH parameters (Gatheral–Jusselin–Rosenbaum, arXiv 2001.01789:
  α = 0.51, λ = 1.2, a = 0.384, b = 0.095, c = 0.0025, Z₀ = 0.1; η is not among the calibrated six, we take η = 1);
  the forecast constant cos(Hπ)/π (GJR 2018, eq. 5.1, Nuzman–Poor theorem 4.2); Fukasawa (2021)'s theorem; the SEC
  DERA paper ("surged from 23.9 to over 65 during pre-market hours, while VIX futures remained below 35"); BIS 95's
  findings (biggest one-day spike; quotes and put bid–ask spreads; ETFs and dispersion unlikely main drivers); BIS 90
  (leveraged-trade unwinding amplified the reaction); Cboe's VIX1D release; Risk's awards. The pre-market figure is
  quoted as "above 65" (SEC); BIS 95's "around 66" could not be read from the PDF and is not used.
* No strategy was tested; the part counter is unchanged at 312; the global counter remains 23,562.

---

# 量化金融，从零搭建 — 第14部分：粗糙与路径依赖波动率

本系列四十三部分中的第14部分，属于第三幕“衍生品”，是本系列关于波动率的前沿部分：一堂约65分钟的课，所有数字都由本系列自己的代码计算
（[`compute.py`](compute.py)，以及经过测试的我们公司的 [`rough`](../../../explainer/quant/house/rough.py) 模块）。

数据：基准曲面和2024—2025年102个原始清单Deribit比特币期权标记日期；币安BTCUSDT一分钟（2018—2020）、五分钟（2024—2025）和日度
（2018—2025）数据；Deribit DVOL（小时和日度）；FRED的VIXCLS和NIKKEI225；肯·弗伦奇的日度市场收益；第13部分缓存的赫斯顿、
贝茨拟合和远期方差曲线。

*这是方法的教育，不是投资建议。*

## 各章（约65分钟旁白）

* **开场。** 布朗与H=0.1路径均自相似、不可微；每段按极差重新归一化的有限网格放大，不能证明路径变直。
* **1. 有限期限偏斜。** 保留原始102个日期（101个周三、1个周四），2024年1月3日至2025年12月11日。812个带符号观测中410个为正，八个拟合指数为负。直方图保留负值，对数图保留低至0.00104的绝对值。这不验证持续同号的零期限发散。逐周优化记录数加权，报告对数均方根误差却不加权；两种指数约束不同，不完全嵌套，0.01门槛不是统计检验。
* **2. 核与偏斜。** 区分带符号s与绝对值psi；平坦远期方差、小波动率的波动率首阶近似。显示屋顶缩放并截顶，解析积分不截顶。深泽定理要求正连续伊藤价格、正赫尔德方差、同号近到期幂律及无摩擦连续期权市场；本数据不验证这些条件。示意kappa=2不同于拟合约14.77；红线是常数扩散加贝茨跳跃参数。
* **3. 测量。** 显示真实自由截距回归；每个已知H只有一条模拟路径，不能证明统计偏差。两时期已实现方差估计混合有限滞后、聚合与噪声，不能直接识别瞬时或风险中性H。保留完整路径与可见解答。
* **4. 预测。** 有限窗口归一化分数预测器对比HAR。回归系数按已知目标扩展重估，但H使用全时期、包括测试日期，故为回顾性比较。粗糙胜HAR六次中的两次。R平方分母用测试期均值，二十天得分均为负。预测记忆、局部粗糙度与传统长程依赖分别讨论。
* **5. 粗糙贝尔戈米。** 黎曼—刘维尔驱动不是完整平稳增量分数布朗运动。高斯补偿匹配输入期望方差曲线；固定未来日期远期方差为鞅，不代表瞬时方差或股票自动为鞅。主拟合H约0.0326、eta约2.0478、rho约−0.5608；新路径同日误差约0.8338点。外部市场方差曲线是额外输入，新种子不是未见市场日期。
* **6. 混合格式。** 最近格精确积分，其余用格平均最优点；FFT卷积。滑动示意用截断远端权重并标准化。乔列斯基与混合计时驱动规律不同，不能作同规律精度比较。
* **7. 粗糙赫斯顿。** 仿射沃尔泰拉与分数Riccati。核示意截顶，但模拟负方差保留，平方根内用非负下限。单日局部校准不构成统计等价或H识别。
* **8. 亚当斯。** 相对1600步参考观测阶约1.76，赫斯顿极限差约7.11乘10的负7次方，不是普遍收敛定理。特征函数模不能识别偏度符号。完整保留H=0.05时约4.44的误差与超过10的期限误差。绿色区域不是风险中性H置信区间。
* **9. 霍克斯。** 平稳分枝恒等式不同于空历史有限模拟。重尾近临界定理要求alpha在二分之一与一之间，协调缩放基准、时间和振幅，得到积分分数CIR极限。归一化动画不能证明极限；固定分箱估计不能普遍恢复alpha减二分之一，H变大不表示局部更粗糙。
* **10. 提升。** 正几何量化与连续指数混合；每数量级一因子只是启发。单因子贡献低于0.1时不显示，但总和含全部因子。路径参考为格平均沃尔泰拉欧拉，不是连续精确解；N=1、50、200的耦合距离约0.911、0.505、0.346个参考标准差。微笑参考也是数值解。
* **11. 测量争论。** 星期效应、布朗正则模型及每格四种子的64格参数图。等读数插值曲线不是置信集合或同规律证明。独立加性对数噪声的简单底部只针对二阶矩。参数模型高频价格下的极小极大速率，H越小指数对应速度越快，不能认证每日估计量。
* **12. 期权争论。** 保留文献各自模型与样本范围。多个指数尺度可在有限窗口近似幂律，但幅度与杠杆也重要。单日模型误差的数值方法和约束不同。
* **13. 路径依赖。** DVOL训练2021至2023年，固定系数用于后续日期；特征包含目标当天收益，是同期留出日期跟踪，不是提前预测。幂律R平方约0.424，四因子约0.524。相关分量标准差不是因果贡献，趋势指数触及边界。连续反馈方程适定性有符号、参数、核与正初始活动条件，正性与股票鞅性另需证明；无符号约束每日回归不验证这些条件。
* **14. VIX与危机。** Ken French收益代理SPX，使用同日收益重构VIX收盘。2000至2018年训练、2019至2025年留出R平方约0.849，基准约0.562。残差针对该代理，并非所有路径模型无法解释的部分。八月五日收盘与开盘前高点时间不同；该回归不能因果分解BIS及DERA讨论的报价机制。每日已实现波动率与三十天DVOL期限也不同。
* **15. 联合与运输。** 第十三部分只有比特币指数示例，没有SPX与VIX联合市场校准。二次模型采用论文六参数，加自行选eta=1、十因子提升与每日离散。弱Zumbach比较Q模拟与P历史重叠窗口，没有统计检验；无显式收益反馈的杠杆也可产生弱不对称。运输边际经截断、离散及凸序修正；熵正则内部值约0.06653至0.16002，线性规划网格极值约0.06393至0.16230。不是完整原始微笑严格界，也不认证独立粗糙贝尔戈米数值约0.14484匹配边际；没有VIX边际或条件对数合约约束。
* **16. 签名。** 十五载荷加相关，期权校准仍非线性。普适性需要深度增加及适当紧路径集与拓扑。载荷可有符号，各到期终值除以样本均值不能证明单一动态一致真鞅。样本内约0.8848点，新路径约1.4815点，仍为同日标记价格。
* **17. 数值速度。** 单次定价映射不是完整校准；第十七部分神经与蒙特卡洛比仅属于其原始合成基准，不含训练。其他柱形输出与精度不同。同日拟合、回顾预测和同期指数跟踪本身不足以通过模型采用规则。
* **18. 研究选读，2023至2025年。** 高斯求积超多项式定理有Lipschitz条件，并非本几何提升普遍阶数。森林展开需要收敛和截断条件；正则结构处理奇异展开，股票适应伊藤积分仍存在。有界核不等于可微波动率。
* **研究者。** 0小于H小于二分之一、均匀网格及固定适当格内规则下，均方根误差为n的负H次方阶；固定kappa精确格降低常数，不是所有网格或近似类的下界。缓存riemann_opt首格仍取远端，从第二格起最优，未作为全局最优阶梯图示。四价格网格共享股票欧拉步，不检验连续价格离散误差。驱动方差缺口阶数不能自动迁移到价格；H加二分之一弱结果针对带收益条件的线性粗糙模型。末尾是本实现尚未验证的问题，不穷尽当前文献。减半需二的一除以H次方倍步数。
* **结尾。** 有条件回顾、四个交易台问题与十道习题。

## 教材对照

| 教材章节 | 本部分章节 |
|---|---|
| 《Rough Volatility》（SIAM 2023）第1章（盖瑟尔—贾森—罗森鲍姆） | 3、4 |
| 第2章（拜尔—弗里茨—盖瑟尔） | 5 |
| 第3章（朱瑟兰—罗森鲍姆） | 9（卡片；冲击见第37部分） |
| 第4章（粗糙赫斯顿）、第5章（粗糙仿射模型） | 7、8、10 |
| 第6章（粗糙波动率下的对冲） | 17 |
| 第7章（混合格式） | 6 |
| 第8章（渐近）、第9章（森林展开） | 2、18 |
| 第10章（正则结构） | 18（卡片；理论超出本系列） |
| 居永—亨利-拉博代尔《非线性期权定价》第10—11章 | 13（README说明）；第13部分 |
| 贝尔戈米《随机波动率建模》：远期方差模型、一阶微笑展开 | 2、5、12 |
| 盖瑟尔《波动率曲面》：随机波动率与跳跃的偏斜 | 2 |
| 弗里茨—海尔《粗糙路径教程》第2版 §14.5 | 18 |

## 交易台问题与解答

1. **一天对一个月？** 假设相应幂律在该区间适用，偏斜绝对值比为30的0.4次方，约3.9；总风险还取决于希腊字母、名义金额与收益结构。
2. **粗糙或快速回复？** 多种考虑噪声的测量、日内滞后、期限结构与真正前瞻的预测和对冲；单个每日代理指数或拟合H不足以区分。
3. **加速校准？** 在匹配输出与精度下比较替代器、提升和傅里叶方法，计入离线训练、近似域、优化与数据处理；一次快速求值不等于完整校准。
4. **单因子不能拟合一周？** 不是。通常条件下正方差正则伊藤模型局部短时偏斜有界，但可拟合有限观测。单指数的平坦至一除以T只是受限示意，其他尺度、振幅和初始曲线很重要。一周不是零期限极限。

## 习题与解答

1. **W^H的方差。** 由伊藤等距，Var W^H_t = 2H ∫₀ᵗ (t − s)^{2H−1} ds = t^{2H}。
2. **标度。** 分数布朗运动的增量平稳、高斯、方差为Δ^{2H}，故E|·|^q = Δ^{qH} E|Z|^q，ζ_q = qH。
3. **粗糙贝尔戈米远期方差恒等式。** W^H_t为方差t^{2H}的高斯变量，所以E[exp(ηW^H_t − ½η²t^{2H})] = 1，E[v_t] = ξ₀(t)；
   在F_s条件下，s之后的部分独立且为高斯，同样的计算说明固定未来t时ξ_s(t)是s上的指数鞅；股票真鞅性另需证明，v本身不因此成为鞅。
4. **提升的恒等式。** 代入y = xt，∫₀^∞ e^{−xt}x^{−α}dx = Γ(1 − α)t^{α−1}；除以Γ(α)Γ(1 − α)即得t^{α−1}/Γ(α)。
5. **霍克斯平均速率。** 平稳时Λ = μ + Λ‖φ‖₁，所以Λ = μ/(1 − ‖φ‖₁)；‖φ‖₁ → 1时发散，“近乎不稳定”。
6. **粗糙二重积分。** 先对u积分得(T − t)^{H+½}/(H + ½)，再对t积分得T^{H+3/2}/((H + ½)(H + 3/2))；除以T²得T^{H−½}。
7. **混合格式的b_k。** 令(b_kΔ)^{H−½}等于核在第k个格子上的平均Δ^{H−½}(k^{H+½} − (k − 1)^{H+½})/(H + ½)，解出b_k。
8. **四因子PDV。** 对K(τ) = λe^{−λτ}，R_t对t求导得dR = λ(r_t^n/Δt − R_t)dt：指数移动平均，马尔可夫；两个这样的核的凸组合就是两个EMA。

9. **（资格考试）精确的强误差。** Y₁ − Ŷ₁ = √(2H)Σ_j∫_{格子j}((1 − s)^a − (c_jΔ)^a)dW_s，由伊藤等距E|Y₁ − Ŷ₁|² = 2HΣ_j∫(r^a − (c_jΔ)^a)²dr；令r = xΔ得2HΔ^{2H}Σ_j∫_{j−1}^{j}(x^a − c_j^a)²dx。固定适当格内规则且0<H<1/2时，j大时x^a − c_j^a ≈ a c_j^{a−1}(x − c_j)，第j项为O(j^{2a−2})，因2a − 2 < −1而可和。每个格子的项在c_j^a等于x^a的格子平均(j^{a+1} − (j − 1)^{a+1})/(a + 1)时最小：c_j = b_j。
10. **（资格考试）朴素格式的偏差。** Var Ŷ₁ = 2HΔ^{2H}Σ_{j≤n}j^{2a}，对s = 1 − 2H ∈ (0, 1)有Σ_{j≤n}j^{−s} = n^{1−s}/(1 − s) + ζ(s) + O(n^{−s})。所以Var Ŷ₁ = 1 + 2Hζ(1 − 2H)Δ^{2H} + o(Δ^{2H})，ζ(1 − 2H) < 0。于是E[exp(ηŶ₁ − ½η²)] = exp(−η²H|ζ(1 − 2H)|Δ^{2H}+o(Δ^{2H}))：H = 0.1时ζ(0.8) = −4.44，η = 1.9时领先阶因子为exp(−1.60Δ^{0.2})，n = 64时约为0.50。在指数中改用Var Ŷ就消除了这个偏差。

## 数据与可复现性

* 所有数字由`compute.py`计算并缓存在`.cache/quant14/`；长计算项会保存中间结果并可续算。
* 事实均对照一手来源核实（见英文部分）。开盘前的VIX数字引用为“超过65”（美国证券交易委员会工作人员论文）。
* 本部分没有检验任何策略；分部计数器仍为312，全局仍为23,562。

## 写给研究者

* **定理。** 本内德森、伦德与帕卡宁（2017），*Finance Stoch.* 21(4)；拜尔、霍尔与坦蓬内（2022），*IJTAF* 25（线性粗糙Stein–Stein及收益条件，不能普遍迁移到粗糙贝尔戈米）；Gassiat（2022），arXiv:2203.09298，论粗糙格式的弱速率。
* **简化。** 只看一个时刻t = 1的误差；价格实验固定价格步、只改变波动率的离散化，以网格上的精确Y为参照，所以不度量价格步自身的误差。
* **实现问题。** 核查适用定理、耦合成本及目标相关误差展开。本部分不确定一般非线性或路径依赖目标阶数，也不宣称穷尽当前文献。

## Scope and source audit for this pass

The original computation modules, House algorithms, global data manifest, trial envelope and track record remain unchanged. Original missing caches were restored through their normal commands without force/refresh or extra market experiments. Part 14's speed chapter also needs Part 17's original fixed-seed synthetic pricing dataset and 40-epoch training benchmark, including its existing synthetic validation split. Restoring that benchmark does not open a sealed market holdout. The dated input and cache hashes are recorded with the QA evidence.

The model-skew table uses different windows and stencils: most model curves use 2–14 / 60–365 days and ±0.02 log-moneyness; market SVI uses 2–16 / 50–365 days and ±0.01; rough Bergomi uses a nine-strike quadratic fit over ±0.08 and 60–183 days at the long end. Recorded short/long exponents are Heston 0.092/0.764, constant diffusion+jumps 0.935/0.998, Bates 0.284/0.700, rough Heston 0.427/0.618, rough Bergomi 0.133/0.573 and market 0.343/0.763. Their difference is not a pure model-class comparison. Skew signs and full observed magnitudes are preserved; explicitly labeled illustrative kernel caps and factor-contribution visibility thresholds remain display choices.

Primary checks: [Fukasawa theorem](https://arxiv.org/html/2002.09215v1), [nearly critical Hawkes](https://arxiv.org/abs/1504.03100), [linear rough weak rates](https://arxiv.org/abs/2009.01219), [PDV SDE](https://arxiv.org/html/2307.01319v2), [general PDV kernels](https://arxiv.org/html/2408.02477v2), [minimax inference](https://arxiv.org/abs/2210.01214), [model comparison](https://arxiv.org/abs/2401.03345), [Markovian approximation](https://arxiv.org/abs/2108.05048), [DERA working paper](https://www.sec.gov/files/dera-vix-working-paper-2504.pdf). Publication/award/index details were checked against publishers, Risk, Baruch and Cboe. DERA statements are the authors' research findings.

本次保持原计算模块、House算法、全局数据清单与试验记录不变；仅以正常命令恢复原缓存。速度章依赖第十七部分固定种子合成数据与原40轮训练及合成验证划分，并未打开封存市场留出集。不同偏斜曲线使用不同窗口与差分方法，不能将表格差异完全归因于模型类别；原始符号与完整观测绝对值均保留。明确标出的示意核截顶与单因子可见阈值属于显示选择。全部21章英中导出标题已核对。完整连续生产语音聆听需另行完成，不能以静态图或音频信号检查代替。


## Validation in this polish pass

All 21 English and 21 Mandarin narration-beat checks and 21 English silent motion
checks pass against the frozen source. All 63 receipts have zero automated warnings. Their sheets were visually
reviewed. Chinese source coverage is 123/123; the narration estimate is
64.2 minutes. Twelve sampled speech reports cover 71 lines. The actual
166.4-second narrated English opening has a reviewed contact sheet,
dead-air scan and verified audio stream. Full continuous production-voice
listening and synchronization remain pending.

The local silent preview is `renders/quant14_polished_silent.mp4` (73:51,
21 embedded chapters and English subtitles). See
[the evidence record](../../../docs/qa/quant14-polish-evidence.json) and
[the sequential QA log](../../../docs/qa/quantitative-finance-polish.md).

本轮通过21个英文与21个中文叙述节点检查，以及21个英文静音动画检查，联系表均已人工审阅。
中文覆盖123/123，叙述估计64.2分钟。12份实际语音报告检查71句的信号与时间标记，
实际英文开场也已审阅。完整连续生产语音聆听和同步仍待单独完成；这些检查不证明发音正确。
