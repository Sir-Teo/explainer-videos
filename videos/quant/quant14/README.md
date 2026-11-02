# Quant, Built — Part 14: Rough and Path-Dependent Volatility

Part 14 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), in Act III, Derivatives. It is the series' frontier part on volatility: a lecture of
about 58 minutes, with every number computed by the series' own code ([`compute.py`](compute.py) and the House's
[`rough`](../../../explainer/quant/house/rough.py) module, tested in `tests/test_quant_house.py`).

The data: the Surface and 102 weekly Deribit BTC option days (2024–2025); Binance BTCUSDT 1-minute (2018–2020),
5-minute (2024–2025) and daily (2018–2025); Deribit DVOL (hourly and daily); FRED VIXCLS and NIKKEI225; Ken French's
daily market return; Part 13's cached Heston, Bates and forward variance curve.

*An education in methods, not investment advice.*

## Chapters (about 58 minutes)

* **Hook: Rough (2.4).** A Brownian path and an H = 0.1 path under a continuous ×256 zoom (pause and predict); how
  we got here, 1968–2024; objectives; the rough lab.
* **1. The fact: an exploding skew (2.5).** A 3D "loom" of 102 weekly skew term structures; the median power-law
  exponent is 0.56 (interquartile 0.37–0.70), steeper than ½, so read literally H < 0; the bounded form
  (Guyon–El Amrani) wins by more than 0.01 in log error in 31% of weeks (median shift 27 days). The Dec-2025 close-up:
  T^−0.49 against (T + 21 d)^−0.88.
* **2. Why a power law (3.4).** The kernel over the triangle in 3D; the first-order skew ψ(T) ≈ ρ/(2σ³T²)∫∫σξK
  (Bergomi–Guyon 2012; checked against SABR's ρν/2); exponential kernels give a flat then 1/T skew, power kernels
  T^{H−½}; rough Bergomi's constant; Fukasawa (2021). Computed local exponents (2–14 days / 2 months+): Heston
  0.09/0.76, jumps only 0.93/1.00, Bates 0.28/0.70, rough Heston (H = 0.1) 0.44/0.66, the market 0.34/0.76. The
  first-order formula overstates rough Bergomi's level 1.8× at η = 2.
* **3. Volatility is rough, re-measured (3.0).** Live paths; the scaling derivation; **Lab 1** (`log_rv_scaling`):
  fBm 0.05→0.01, 0.1→0.09, 0.3→0.31, 0.5→0.50; bitcoin H = 0.13 (2018–20, 1,074 days) and 0.08 (2024–25; 0.12 with
  weekdays evened out).
* **4. Forecasting with a rough memory (3.0).** GJR's forecast weights under a horizon slider, against HAR's
  staircase; the Nuzman–Poor formula with its cos(Hπ)/π constant derived; an expanding-window race at 1, 5 and 20
  days in two eras: HAR wins 4 of 6 head-to-heads, by small margins; at 20 days nothing beats the test mean.
  Comte–Renault's long memory against roughness.
* **5. Rough Bergomi (3.2).** The model, the martingale proof, live paths; **replay** of the calibration on three
  seeds (H 0.03–0.04, re-priced error 0.88–0.94 on 10,000 paths); the headline 20,000-path fit H = 0.03, η = 2.0,
  ρ = −0.56, error 0.83 vol points against Heston's 1.37.
* **6. The hybrid scheme (2.8).** The kernel's spike, naive bars against the exact first cell and optimal points
  b_k; the convolution sliding; **Lab 2** (`rbergomi_paths`): Var W^H₁ (exact 1) hybrid 1.03 / Riemann 0.40 at
  H = 0.05; 30-day ATM vol 44.9% (hybrid) against 25.2% (Riemann); timing against Cholesky (competitive at these
  sizes on this machine).
* **7. Rough Heston (3.1).** The kernel morphing from Heston's constant to the power law with one path redrawn; the
  affine Volterra derivation to the fractional Riccati equation; the free fit (H = 0.45, error 1.28) against H = 0.1
  (1.49).
* **8. The fractional Adams scheme (3.2).** The predictor/corrector with memory arrows; **Lab 3** (`frac_riccati`):
  max error 1.8e-3 (25 steps) to 3.8e-6 (800), order 1.76; Heston matched to 7e-7 at H = ½; |φ(u, T)| in 3D; a
  nine-point H profile (2.25 at H = 0.05 down to 1.28 at 0.5) with errors by expiry.
* **9. Where roughness comes from (3.4).** Hawkes activity filling; a family tree; Jaisson–Rosenbaum derived to the
  Mittag-Leffler kernel; zoom-out of a 0.9999-ratio process; the branching sweep: estimated H 0.005 (n = 0.5) →
  0.12 (n = 0.999), but tails α = 0.6/0.75/0.9 all read ≈ 0.1, not α − ½.
* **10. Markovian lifts (3.2).** Exponentials summing into the power law; the identity derived; one path under N = 1,
  5, 20, 50, 200 factors against a fine Volterra scheme (pathwise distance 0.92 → 0.36 s.d.); the 30-day smile error
  4.70 → 0.26 vol points (N = 1 → 50).
* **11. The debate I (3.2).** The weekend trap (0.08 → 0.12); three smooth models (0.38, 0.42, 0.02); the **bias map
  in 3D** (64 cells × 4 seeds): a smooth H = ½ with a one-day half-life reads 0.094, H = 0.05 without mean reversion
  reads 0.17; the gold contour at bitcoin's 0.08; why (error floor, fOU flattening, minimax rate); the statistics
  literature.
* **12. The debate II (2.8).** The weekly fans with bounded-better weeks in gold; the published horse races; the
  two-factor kernel's skew; our own **replayed** two-factor Bergomi fit: 0.89 vol points against rough Bergomi's
  0.83 (half-lives 3.6 and 25 days).
* **13. Path-dependent volatility (3.3).** The model; the two memories filling live along bitcoin's path;
  **replay** of the kernel fit; DVOL R² 0.88 in sample, 0.42 out (baseline −0.27); **Lab 4** (`pdv4_step`): the
  4-factor Markovian PDV, R² 0.89 / 0.52 out of sample; well-posedness.
* **14. PDV on the S&P 500, and 5 August 2024 (3.3).** The VIX 1993–2025 traced against PDV from market returns:
  R² 0.94 in, 0.85 out (baseline 0.81, 0.56); the trend term negative (leverage), trend kernel exponent at its
  bound; the crisis file: Nikkei −12.4%, VIX close 38.57 against PDV 25.4, above 65 pre-market on put quotes (SEC
  DERA; BIS 95); bitcoin's DVOL hourly high 92.7, realized vol 219%, DVOL close 63 against PDV 61.
* **15. Joint SPX/VIX (3.4).** Guyon's puzzle (models fitted to the SPX skew give VIX implied vols too high; Part 13
  measures it); quadratic rough Heston with GJR's calibrated parameters, a dot riding the parabola; the Zumbach
  effect: qRH 0.54 forward against 0.14 backward, the US market 0.45/0.27, rough Bergomi 0.11/0.09; the DMSP;
  **Lab 5** (`entropic_mot`): on the Surface's 51- and 107-day smiles, any martingale prices |log S₂/S₁| between
  0.067 and 0.160 (LP 0.064–0.162); rough Bergomi 0.145 inside. An illustration, not Guyon's algorithm.
* **16. Signature volatility (2.2).** The signature bars growing; log S = ℓᵀA − ½ℓᵀBℓ; **Lab 6** (`sigvol_logS`);
  **replay** of the 16-parameter fit: 0.88 in sample, 1.50 on fresh paths (overfits; rough Bergomi still lowest).
* **17. What desks use, and the rough lab (3.0).** Calibration speed timed on this machine; the surrogate lineage;
  Risk Awards (2021 Quants of the Year; 2023 Rising Star Rømer); VIX1D; hedging with forward variance; the House's
  functions and Rule 14 applied to the part's scoreboard.
* **18. The frontier, 2023–2026 (2.2).** Eight results; forest expansion and regularity structures; the closing board.
* **Outro (2.8).** Twelve-line recap, four desk questions, eight problems, payoffs, references.

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
2024 (13); Abi Jaber–Li 2025 (12, 18); Cuchiero–Gazzani–Möller–Svaluto-Ferro 2025 (16). Industry: BIS Bulletins 90
and 95 (2024), Li–Askanazi SEC DERA working paper (2025), Cboe VIX1D (2023).

## Build it

```bash
python -m videos.quant.quant14.compute                    # every number (~2 CPU-hours; long items resume)
EXPLAINER_TTS=silent python tools/qa_scene.py quant14 Rough   # one chapter, silent, with a contact sheet
python tools/make.py quant14 --cpu-voice -q m             # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **With H ≈ 0.1, a one-day option against a one-month one?** The ATM skew scales like T^{H−½}, so
   (1/30)^{−0.4} ≈ 3.9: the one-day skew is about four times the one-month. Volatility moves by about Δ^H over Δ, so
   short-dated options carry most of the vol-of-vol exposure.
2. **Roughness or fast mean reversion?** Several measurements, each cleaned of seasonality and noise: the bias map
   (chapter 11: a smooth one-day half-life reads like bitcoin's 0.08), the scaling at sub-daily lags and the curvature
   of the scaling line, the skew's term structure at the shortest expiries (chapter 12), and out-of-sample forecasts
   and hedges, rough against multi-factor. Any one can be fooled.
3. **Calibrating in milliseconds.** A neural surrogate trained once on the model's prices (Horvath–Muguruza–Tomas
   2021; Part 17: about 400 times faster than the Monte Carlo it imitates), a Markovian lift with a few factors, or
   rough Heston's Fourier form with a coarse Adams grid. Check the surrogate against the full model regularly.
4. **Why can't a one-factor Markov SV model fit a 1-week skew?** Its first-order skew is
   (ρη/2)(1/(κT) − (1 − e^{−κT})/(κT)²): flat (≈ ρη/4) for T ≪ 1/κ and ∝ 1/(κT) beyond. To be steep at one week it needs
   κ ≈ 50 a year, and then the skew at three months has already collapsed by a factor of about κT ≈ 12. A power law
   needs all time scales at once (chapter 2); two factors imitate it over the range between them (chapter 12).

## Problems, with solutions

1. **Variance of W^H.** By the Itô isometry, Var W^H_t = 2H ∫₀ᵗ (t − s)^{2H−1} ds = t^{2H}.
2. **Scaling.** fBm has stationary Gaussian increments with variance Δ^{2H}, so B^H_{t+Δ} − B^H_t has the law of Δ^H Z
   and E|·|^q = Δ^{qH} E|Z|^q; hence ζ_q = qH.
3. **Rough Bergomi's martingale property.** W^H_t is Gaussian with variance t^{2H}, so E[exp(ηW^H_t − ½η²t^{2H})] = 1
   and E[v_t] = ξ₀(t). Conditionally on F_s, the part of the integral after s is independent Gaussian with variance
   ∫_s^t 2H(t − u)^{2H−1}du; the same computation makes ξ_s(t) = E_s[v_t] an exponential martingale in s.
4. **The lift's identity.** Substituting y = xt, ∫₀^∞ e^{−xt}x^{−α}dx = Γ(1 − α)t^{α−1}; dividing by Γ(α)Γ(1 − α)
   gives t^{α−1}/Γ(α). Quantising x^{−α}dx/(Γ(α)Γ(1 − α)) on a geometric grid gives the weights c_i and nodes x_i.
5. **The Hawkes mean rate.** At stationarity Λ = μ + Λ‖φ‖₁, so Λ = μ/(1 − ‖φ‖₁); as ‖φ‖₁ → 1 the rate and each
   event's expected number of descendants ‖φ‖₁/(1 − ‖φ‖₁) explode: "nearly unstable".
6. **The rough double integral.** ∫_t^T (u − t)^{H−½}du = (T − t)^{H+½}/(H + ½); integrating again in t gives
   T^{H+3/2}/((H + ½)(H + 3/2)). Divided by T², the first-order skew is ∝ T^{H−½}.
7. **The hybrid scheme's b_k.** The cell k steps back covers lags [(k − 1)Δ, kΔ]; the kernel's average there is
   (1/Δ)∫ x^{H−½}dx = Δ^{H−½}(k^{H+½} − (k − 1)^{H+½})/(H + ½). Setting (b_kΔ)^{H−½} equal to it gives
   b_k = ((k^{H+½} − (k − 1)^{H+½})/(H + ½))^{1/(H−½)}.
8. **The 4-factor PDV.** With K(τ) = λe^{−λτ}, R_t = ∫ λe^{−λ(t−u)} r_u^n du (returns per unit time); differentiating,
   dR = λ(r_t^n − R_t)dt: an exponential moving average, Markov. A convex mix of two such kernels is a mix of two
   EMAs: four factors for R₁ and R₂.

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
* No strategy was tested; the trial counter is unchanged at 73.

---

# 量化金融，从零搭建 — 第14部分：粗糙与路径依赖波动率

本系列四十三部分中的第14部分，属于第三幕“衍生品”，是本系列关于波动率的前沿部分：一堂约58分钟的课，所有数字都由本系列自己的代码计算
（[`compute.py`](compute.py)，以及经过测试的我们公司的 [`rough`](../../../explainer/quant/house/rough.py) 模块）。

数据：基准曲面和2024—2025年102个每周的Deribit比特币期权交易日；币安BTCUSDT一分钟（2018—2020）、五分钟（2024—2025）和日度
（2018—2025）数据；Deribit DVOL（小时和日度）；FRED的VIXCLS和NIKKEI225；肯·弗伦奇的日度市场收益；第13部分缓存的赫斯顿、
贝茨拟合和远期方差曲线。

*这是方法的教育，不是投资建议。*

## 各章（约58分钟）

* **开场：粗糙。** 布朗路径和H = 0.1路径在连续放大256倍下的对比；1968—2024年的来龙去脉；本部分目标；粗糙实验室。
* **1. 事实：爆炸的偏斜。** 102条每周偏斜期限结构的三维“织布机”；中位幂律指数0.56（四分位0.37—0.70），比二分之一更陡，按字面读
  H < 0；有界形式在31%的周里以超过0.01的对数误差获胜（中位平移27天）。2025年12月的近景：T^−0.49对(T + 21天)^−0.88。
* **2. 为什么是幂律。** 三角形上的核（三维）；一阶偏斜公式（贝尔戈米—居永2012，用SABR的ρν/2检验）；指数核给出先平后1/T的偏斜，
  幂律核给出T^{H−½}；深泽（2021）。计算出的局部指数（2—14天／2个月以上）：赫斯顿0.09/0.76，纯跳跃0.93/1.00，贝茨0.28/0.70，
  粗糙赫斯顿（H = 0.1）0.44/0.66，市场0.34/0.76。
* **3. 波动率是粗糙的，重新测量。** 实验一（`log_rv_scaling`）：分数布朗运动的检验；比特币H = 0.13（2018—20）和0.08（2024—25）。
* **4. 用粗糙的记忆做预测。** 预测权重与HAR的台阶；推导cos(Hπ)/π常数；两个时代、扩展窗口的比赛：HAR在六场正面对决中赢四场，
  差距很小。孔特—勒诺的长记忆与粗糙性的区别。
* **5. 粗糙贝尔戈米。** 鞅性质的证明；三个随机种子的校准回放；主拟合H = 0.03，误差0.83个波动率点，赫斯顿为1.37。
* **6. 混合格式。** 实验二（`rbergomi_paths`）：H = 0.05时方差（精确值1）混合格式1.03、朴素黎曼和0.40；30天平值波动率44.9%对25.2%。
* **7. 粗糙赫斯顿。** 由仿射沃尔泰拉结构推导分数阶里卡蒂方程；自由拟合H = 0.45（误差1.28）对H = 0.1（1.49）。
* **8. 分数阶亚当斯格式。** 实验三（`frac_riccati`）：收敛阶1.76，H = ½时与赫斯顿相差7e-7；三维|φ(u, T)|；九点H剖面。
* **9. 粗糙从何而来。** 家族树；贾森—罗森鲍姆极限；分支扫描：分支比接近一时粗糙性出现，但有限样本不能恢复α − ½。
* **10. 马尔可夫提升。** 指数逐个相加成幂律；逐路径距离0.92 → 0.36个标准差（N = 1 → 200）；30天微笑误差4.70 → 0.26。
* **11. 争论之一。** 三维偏差图：一天半衰期的光滑波动率读出0.094，正是比特币的数字；金色等值线。统计文献。
* **12. 争论之二。** 已发表的赛马；我们回放的两因子贝尔戈米：0.89对粗糙贝尔戈米0.83。
* **13. 路径依赖波动率。** 两个记忆的实时填充；核拟合回放；DVOL样本外R² 0.42；实验四（`pdv4_step`）：四因子马尔可夫版本样本外0.52。
* **14. 标普500上的PDV与2024年8月5日。** VIX样本外R² 0.85；危机档案：日经−12.4%，VIX收盘38.57对PDV 25.4，开盘前超过65；
  比特币DVOL收盘63对PDV 61。
* **15. 标普/VIX联合。** 居永的难题；二次粗糙赫斯顿；宗巴赫效应；实验五（`entropic_mot`）：鞅传输界0.067—0.160，粗糙贝尔戈米0.145在其中。
* **16. 签名波动率。** 实验六（`sigvol_logS`）；十六参数拟合样本内0.88、新路径1.50（过拟合）。
* **17. 交易台用什么。** 校准速度；替代模型的谱系；Risk奖项；VIX1D；用远期方差对冲；第十四条规则。
* **18. 前沿，2023—2026。** 八个结果；森林展开与正则结构；最后的记分牌。
* **结尾。** 十二句回顾、四个交易台问题、八道习题。

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

1. **H ≈ 0.1时，一天期与一个月期期权？** 平值偏斜按T^{H−½}缩放，(1/30)^{−0.4} ≈ 3.9：一天期偏斜约为一个月期的四倍；
   波动率在Δ内移动约Δ^H，短期期权承担了大部分波动率的波动率风险。
2. **粗糙还是快速均值回复？** 用多种测量并清除季节性和噪声：偏差图（第11章：一天半衰期的光滑过程读起来像比特币的0.08）、
   日内滞后上的标度及标度线的曲率、最短到期日的偏斜期限结构（第12章），以及样本外预测和对冲。任何单一测量都可能被愚弄。
3. **几毫秒内校准。** 一次训练的神经替代模型（霍瓦特—穆古鲁萨—托马斯2021；第17部分：比它模仿的蒙特卡洛快约400倍），
   少量因子的马尔可夫提升，或用粗网格亚当斯的粗糙赫斯顿傅里叶形式。并定期用完整模型检查替代模型。
4. **为什么单因子马尔可夫模型拟合不了一周的偏斜？** 它的一阶偏斜是(ρη/2)(1/(κT) − (1 − e^{−κT})/(κT)²)：T ≪ 1/κ时为常数，
   之后按1/(κT)下降。要在一周处变陡需要κ ≈ 每年50，那么三个月处的偏斜已经塌缩了约κT ≈ 12倍。幂律需要同时具备所有时间尺度。

## 习题与解答

1. **W^H的方差。** 由伊藤等距，Var W^H_t = 2H ∫₀ᵗ (t − s)^{2H−1} ds = t^{2H}。
2. **标度。** 分数布朗运动的增量平稳、高斯、方差为Δ^{2H}，故E|·|^q = Δ^{qH} E|Z|^q，ζ_q = qH。
3. **粗糙贝尔戈米的鞅性质。** W^H_t为方差t^{2H}的高斯变量，所以E[exp(ηW^H_t − ½η²t^{2H})] = 1，E[v_t] = ξ₀(t)；
   在F_s条件下，s之后的部分独立且为高斯，同样的计算说明ξ_s(t)是s上的指数鞅。
4. **提升的恒等式。** 代入y = xt，∫₀^∞ e^{−xt}x^{−α}dx = Γ(1 − α)t^{α−1}；除以Γ(α)Γ(1 − α)即得t^{α−1}/Γ(α)。
5. **霍克斯平均速率。** 平稳时Λ = μ + Λ‖φ‖₁，所以Λ = μ/(1 − ‖φ‖₁)；‖φ‖₁ → 1时发散，“近乎不稳定”。
6. **粗糙二重积分。** 先对u积分得(T − t)^{H+½}/(H + ½)，再对t积分得T^{H+3/2}/((H + ½)(H + 3/2))；除以T²得T^{H−½}。
7. **混合格式的b_k。** 令(b_kΔ)^{H−½}等于核在第k个格子上的平均Δ^{H−½}(k^{H+½} − (k − 1)^{H+½})/(H + ½)，解出b_k。
8. **四因子PDV。** 对K(τ) = λe^{−λτ}，R_t对t求导得dR = λ(r_t^n − R_t)dt：指数移动平均，马尔可夫；两个这样的核的凸组合就是两个EMA。

## 数据与可复现性

* 所有数字由`compute.py`计算并缓存在`.cache/quant14/`；长计算项会保存中间结果并可续算。
* 事实均对照一手来源核实（见英文部分）。开盘前的VIX数字引用为“超过65”（美国证券交易委员会工作人员论文）。
* 本部分没有检验任何策略；试验计数器仍为73。
