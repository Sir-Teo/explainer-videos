# Quant, Built — Part 15: Exotics and Structured Products

Part 15 of the [43-part series](../README.md), in Act III, Derivatives. A hook, eighteen chapters, a research chapter and an outro; approximately 65 minutes of narration before animation and reading pauses. English and Mandarin narration use the same assumptions, numbers and qualifications.

The central example is a **stylized snowball**, not a reconstruction of an actual traded contract. Specify its cash flows before interpreting its coupon, Greeks or a dealer's hedge. Numerical examples come from the original fixed-seed [`compute.py`](compute.py) and the House's [`exotics.py`](../../../explainer/quant/house/exotics.py). Public episode figures come from the dated sources below.

## Chapters

| # | Chapter | Experiment |
|---|---|---|
| — | The snowball | Actual ETF path, hypothetical note barriers, historical context |
| 1 | Anatomy of a note, and the margin | Pathwise decomposition; funding-spread illustration |
| 2 | Who buys, and what they earned | 84 overlapping hypothetical vintages; investor research |
| 3 | Barriers: reflection, the closed form, the PDE | Grid-reflection illustration, count histograms, value and delta surfaces |
| 4 | Discrete monitoring and static vanilla hedges | BGK approximation; finite static portfolios; conditional put–call symmetry |
| 5 | Digitals, one-touches and the call-spread hedge | Near-expiry delta; discrete hedge errors; first passage; smile chain rule |
| 6 | Averages and extremes: Asians and lookbacks | Geometric control variate; all 1,500 saved scatter points; Vecer PDE |
| 7 | The snowball, priced | Redemption states; 40,000 paths; affine coupon solve |
| 8 | The issuer's Greeks, in three dimensions | Full displayed grids; state and sign conventions; bump-size replay |
| 9 | January 2024: the snowballs melt | Hypothetical 36-note hedge on the actual ETF path |
| 10 | Korea's ELS, twice, and a dealer's loss | Stylized 2015/2021 vintages; dated FSC/FSS record; Natixis disclosure |
| 11 | Worst-of, correlation and the correlation skew | Unequal-volatility cloud; worst-of put and autocall; conditional correlations |
| 12 | Cliquets: the risk vega cannot see | Local caps, finite-grid vega maximum, volatility uncertainty |
| 13 | Uncertain volatility: the price of not knowing | Finite BSB solver; non-additivity; finite Lagrangian optimization |
| 14 | One market surface, different exotic prices | Four approximate fits; empirical entropy tilt |
| 15 | Dealer flows: when the hedges move the market | Fixed-parameter book sensitivities; conditional hedge and impact mechanisms |
| 16 | A neural pricer for the book, trained on screen | Three training seeds, polynomial baseline, original synthetic references |
| 17 | Industry: how desks mark, reserve and report | Prudent valuation, day-one recognition, capital, conduct, model validation |
| 18 | Frontier, 2023–2026 | Digital-delta estimators over five seeds; scoped paper findings |
| R | What the vanillas alone say about a one-touch | Martingale superhedge; terminal atoms and gaps; finite empirical illustration |
| — | Recap, desk questions, problems | Three spoken desk questions, an extra dependence question, ten worked problems |

## Contract and numerical conventions

Normalize initial spot and notional to one. On observations corresponding to months **3 through 24 inclusive**, spot at or above **1.03** redeems the note for `1 + c m/12`. A daily close **strictly below 0.75** sets a persistent knock-in flag. Knock-out can still occur afterward. At maturity, a surviving note without knock-in pays `1 + 2c`; a surviving knocked-in note pays `min(S_T,1)` without coupon. Recovery can therefore restore par. Coupons are paid on redemption or qualifying maturity, rather than in monthly installments.

The original convention is **21 trading observations per month**, hence 504 over two model years, rather than exact calendar-month schedules. Historical simple returns are annualized by holding months divided by twelve; they are not compounded portfolio returns. Historical volatility uses a 244-day annualization while pricing uses a 252-step model year; this retained convention is an approximation. Korean ELS examples use 123 trading observations per half-year. First-redemption events are conditional on survival, and redemption cancels the loss leg.

| Original cached result | Value and interpretation |
|---|---|
| 2021–23 CSI 500 ETF volatility | 19.98%; retrospectively fixed for the reconstruction |
| Fair snowball coupon | 13.3537%; `A = 0.93828165`, `B = 0.46218164`, `c* = (1−A)/B` |
| Decomposition | Bond 0.96078944 + earlier repayment 0.02295316 + redemption coupons 0.05161465 + maturity coupon 0.01010370 − autocall-cancelled loss 0.04546095 = 1 |
| Outcome frequencies | 78.415% knock out; 17.6475% survive after knock-in; 3.9375% survive without knock-in |
| Expected life | 9.895 months; this is different from discounted coupon-accrual coefficient B |
| Historical buyers | 26 losses among 84 overlapping hypothetical vintages; worst simple return −31.94%; 25 beat the ETF's price change over their own holding periods |
| 2024 ETF fall | −17.83%, 29 December 2023 to 5 February 2024; an ETF proxy, not the index itself |
| Hypothetical book | Cash hedge exposure peaks at 25.19 note-notionals; at the ETF low it is 14.59. After the initial hedge, modeled purchases total 24.86 and sales 24.44 |
| Worst-of autocall | Coupon 23.26% at correlation 0.3 and 13.57% at 1, under the specified unequal asset volatilities |
| UVM book | Finite-solver lower/upper 0.31373/0.62340; with the selected vanilla hedge 0.41175/0.52007; separate leg uppers sum to 1.00055 |
| Neural proxy | Original 150-reference in-model RMSE 0.01661, maximum absolute error 0.10381; polynomial RMSE 0.01084 |
| Proxy timing | 0.304 microseconds per output averaged over repeated 150-output batches; original 40,000-path single-price timing 0.309 s. Training labels 51.19 s and training 2.26 s are separate |

Decomposition and coupon solve use the **same seeds and paths**, so their sample identity is exact up to rounding. A fresh sample need not price at exactly one. The loss claim is an **autocall-cancelled knock-in loss**, rather than an unconditional down-and-in put. Initial model margin excludes hedge costs, reserves and other expenses. Discounting the promise at `r+s` while pricing the option at `r` is a funding heuristic, not a default/recovery/wrong-way-risk model.

The historical buyer observations overlap. They are neither independent trials nor actual client trades. ETF price comparisons omit index dividends. A lower absolute issue price does not mechanically increase the initial distance to a barrier defined relative to that same issue price.

## What the experiments establish

Barrier monitoring matters. The constant-coefficient, continuously monitored zero-rebate DOC is 7.28087; the original monthly monitored MC is 7.44370 and the 2,520-step grid MC is 7.29390. The latter is still a discrete grid. BGK is an asymptotic correction, particularly delicate near a barrier. Displayed twice-naive-standard-error bands are diagnostics, rather than confidence guarantees for dependent antithetic observations. The saved weekly schedule also has a terminal remainder. The reflection fan is a grid illustration, not an exact pathwise continuous reflection construction.

Exact Carr–Ellis–Gupta static replication requires conditional put–call symmetry **at every potential touch**, not simply a symmetric initial smile. The skew comparison contains Monte Carlo and monitoring errors. A finite portfolio's convergence is a numerical example, rather than a universal replication proof.

A digital has a continuous frictionless Black–Scholes replication; its finite-time delta is smooth. Near expiry, discrete replication becomes difficult. A held call spread's **terminal payoff dominance** does not imply a safer discrete dynamic hedge in every regime. With zero rates/dividends, its delta is bounded by `1/ε`. Where a differentiable implied-volatility smile slopes downward, the digital is dearer than Black–Scholes **at the same strike volatility**, by the chain rule. A comparison against a fixed ATM volatility also changes the volatility level.

For continuous geometric averaging, log variance is `σ²T/3`; this is not a universal half-price rule for arithmetic Asians. The fixed population-optimal control coefficient gives the familiar `1−ρ²` variance ratio. A coefficient estimated from the same sample adds estimation effects. The displayed scatter includes all 1,500 saved points, while the coefficient and correlation use the original 4,000 observations. The Vecer transform is shown for continuous averaging and `r=q=0`.

Issuer position delta is the negative of the positive underlying hedge. Units and cash exposure differ. The 2024 rebalancing bars use **current price × change in underlying units**, after the initial hedge; differencing cash exposure would also count mark-to-market changes. The cached knock-in-day exposure diagnostic contains spot and aging effects, rather than a pure state jump. Model Greeks, hypothetical hedge policies, actual orders and causal market impact are separate objects. The longer book reconstruction interpolates a fixed Greek table and retains its endpoint clamping; it is not observed dealer inventory or a hedge P&L.

The buyer of a typical worst-of note sells the loss put and is long correlation; its issuer owns the loss put and is short correlation. Unequal asset volatilities prevent correlation one from making the normalized paths identical. Historical correlations are not risk-neutral correlation quotes; conditioning alone changes correlation. The reported regimes provide no universal crash-correlation law or formal significance test.

Cliquet aggregate vega can be near zero while other risks remain. A finite grid maximum is not an exact zero, and a local Taylor argument about a random constant volatility is not a theorem for arbitrary stochastic volatility. UVM values have grid error, and the finite optimizer is not a global optimality certificate.

The four models fit the observed surface with **different residual errors**. Their exotic-price spread includes fit, simulation and discretization differences; it is not a certified range over models sharing identical vanilla marginals. The KL calculation tilts empirical payoffs without imposing martingale or calibration constraints. Its ambiguity radius is assumed, not validated as plausible, a confidence level or a regulatory AVA. Its threshold compares present value with `0.97 exp(−0.04)`, rather than measuring a uniform three-percent realized loss.

The proxy has three variable inputs with contract, carry, coupon and volatility fixed. Its original synthetic test references were inspected repeatedly; they are not an untouched market holdout. A local label-noise estimate of 0.00310 at one state is below the observed errors, rather than a global error floor. Batch inference timing excludes label generation, training, calibration and individual-request overhead.

## Desk questions and solutions

1. **Price a strict digital using a call spread.** Buy `1/ε` calls at `K−ε` and sell the same number at K. The payoff dominates `1{S_T>K}`. Under a smooth density, excess price is approximately `ε/2` times the discounted density at K. Wider spreads trade more overpayment for a lower maximum delta; the simulated hedge-error comparison is specific to the rebalancing experiment.
2. **What is the snowball issuer's vega?** Differentiate every contingent leg: loss minus earlier-redemption and coupon vegas. The displayed above-barrier region is often positive, but sign and peak depend on state, model and contract. Knock-in does not universally eliminate vega or mandate an option buyback.
3. **A one-touch from a digital?** For centered log price with zero drift, reflection gives twice the matching terminal digital for a maturity-paid touch. Zero stock drift is a different assumption: with `r=q=0`, log drift is `−σ²/2`. At `S=100,H=90,T=0.5,σ=25%`, the continuous touch price is 0.58015, against twice the terminal digital 0.61172.
4. **A worst-of on three indices?** Owning the worst-of loss put generally benefits from lower correlation in the specified model. A note buyer selling that put has the opposite exposure. Dependence smiles, basis, contract states and model uncertainty need more than a single historical correlation estimate.

## Ten problems, with worked solutions

1. **Reflection and a DOC.** For constant Black–Scholes coefficients, `S>H`, `K≥H`, zero rebate and `r=q=0`, change measure for the reflected log process. The image term is `(S/H) C(H²/S,K)`, so `DOC=C(S,K)−(S/H)C(H²/S,K)`. Both terms satisfy the PDE, their difference vanishes at H, and the image payoff is zero on the allowed terminal domain. These conditions are essential.
2. **BGK correction.** A sampled path can cross and return between observations. The Gaussian random-walk overshoot contributes `βσ√Δt`, with `β=−ζ(1/2)/√(2π)≈0.5826`. Move a down barrier down to `H exp(−βσ√Δt)` (an up barrier up) in the continuous approximation. The finite monitoring comparison illustrates convergence; it does not prove an exact identity or an error bound near the barrier.
3. **Geometric Asian.** `log G=n⁻¹Σ log S_ti` is Gaussian with mean `log S₀+(r−q−σ²/2)t̄` and variance `σ²n⁻²Σ min(t_i,t_j)`. The double sum converges to `σ²T/3` for continuous uniform averaging. For log mean m and variance v, the discounted call is `e^(−rT)[e^(m+v/2)N(d₁)−K N(d₂)]`, where `d₂=(m−log K)/√v` and `d₁=d₂+√v`.
4. **Call-spread bound and its boundary.** The payoff is zero below `K−ε`, a linear ramp on `[K−ε,K]`, and one at or above K. It dominates the strict digital everywhere. Its pointwise limit is **`1{S_T≥K}`**, including one at K. Thus price convergence to a strict digital needs **no terminal atom at K**; otherwise the limiting excess is `e^(−rT)Pr(S_T=K)`.
5. **Decompose the snowball.** Start with a maturity bond; add the value of earlier principal repayment and coupons conditional on first redemption or survival without knock-in; subtract terminal loss only on surviving knocked-in paths. Knock-out cancels that loss. Differentiate all these legs for vega. A plain down-and-in put alone omits autocall cancellation and is insufficient.
6. **Solve the coupon.** Every discounted path payoff is `a+c b`, with coupon-independent a and b. At first redemption m, `b=D_m m/12`; at surviving no-knock-in maturity, `b=2D_T`; otherwise b is zero. Hence `V(c)=A+cB` and, when `B>0`, `c*=(1−A)/B`. Original values give 13.3537%. Selling three percentage points below that coupon creates `0.03B=0.01386545` initial model margin before costs and reserves.
7. **Chooser parity.** Assume identical strike K and expiry T for both choices at `t₁≤T`, deterministic r and q. At `t₁`, `max(C,P)=C+e^(−q(T−t₁))(K e^(−(r−q)(T−t₁))−S_t₁)⁺`. Its initial value is a call to T plus `e^(−q(T−t₁))` puts to t₁ at strike `K e^(−(r−q)(T−t₁))`.
8. **Margrabe.** For two positive tradable GBMs with zero dividends and constant coefficients, use S₂ as numeraire. Their ratio is a martingale under the associated measure with variance rate `σ_X²=σ₁²+σ₂²−2ρσ₁σ₂`. The exchange call is `S₁(0)N(d₁)−S₂(0)N(d₂)`, with `d₁=[log(S₁/S₂)+σ_X²T/2]/(σ_X√T)` and `d₂=d₁−σ_X√T`. Take the deterministic payoff limit when `σ_X=0`; dividends require the corresponding prepaid-forward adjustment.
9. **Down-touch bounds (advanced).** Assume a nonnegative uniformly integrable price martingale, zero rates/dividends, frictionless admissible trading and maturity payment, with `B<S₀`. Terminal price at or below B implies a prior touch, giving `Pr(S_T≤B)≤OT`. For any `K>B`, hold `1/(K−B)` puts and buy that many forwards at first passage `τ`. At a touch, `S_τ≤B`, so terminal portfolio payoff is at least `[(K−S_T)⁺+S_T−B]/(K−B)≥1`; without touch it is nonnegative. Optional sampling makes the forward strategy zero cost under the stated integrability conditions. Thus `OT≤inf_(K>B) P(K)/(K−B)`. At a smooth interior minimizer, `(K*−B)P′(K*)=P(K*)`. With atoms use the convex subgradient condition; neither uniqueness nor attainment follows from convexity alone. The terminal floor is the **right put derivative** at B when there is an atom. Sharpness of the upper bound under suitable continuous-model/marginal assumptions does not prove sharpness of the floor or attainability of every intermediate value.
10. **Up-touch bound (advanced).** For `B>S₀`, hold `1/(B−K)` calls at `K<B` and sell the same number of forwards at first up-touch. On touch the payoff is at least `(S_τ−K)/(B−K)≥1`; an upward overshoot helps. Hence `OT_up≤inf_(K<B) C(K)/(B−K)` under the same martingale and trading conditions. In the specified zero-rate/dividend Black–Scholes example `S₀=1,σ=50%,T=0.25,B=1.2`, numerical strike minimization gives approximately `K*=0.973`, upper bound 0.494, model touch 0.424 and terminal digital 0.196. Finite minimization is an illustration, rather than a proof of an attained global optimum.

## Research illustration

The displayed band uses **Heston's own empirical puts** and a finite strike grid. The other approximate fits have different marginals. Their plotted touch values lying inside this band therefore do not test a theorem about a shared terminal law.

| Down barrier | Heston terminal floor | Heston daily-grid touch | Heston empirical put upper |
|---|---:|---:|---:|
| 0.70 | 0.08465 | 0.14360 | 0.21359 |
| 0.80 | 0.16360 | 0.28550 | 0.41431 |
| 0.90 | 0.29875 | 0.53555 | 0.72117 |

These are original 20,000-path, 79-day simulations. At B=0.8, other fitted models' daily touch values run from 0.28045 to 0.29965. The Heston superhedge at K=0.96 has minimum sampled surplus zero and mean 0.12707. Its priced gap is 0.12881; the difference is the sample mean forward gain, rather than an exact finite-sample expectation identity. Histogram shares divide by all 20,000 paths; 127 observations outside the displayed range are omitted without renormalizing. Daily monitoring and finite strike/Monte Carlo errors prevent a numerical certificate for continuous-model sharp bounds.

## Reproduce and validate

```bash
# Restore or build original fixed-seed caches; do not force new market trials.
python -m videos.quant.quant15.compute
EXPLAINER_TTS=silent python tools/qa_series.py quant15 --cached-only
python tools/make.py quant15 --cpu-voice -q m
```

`modelrisk` depends on Part 13 calibrations and `digital_skew` on Part 12's Surface. Build those dependencies first. China Southern CSI 500 ETF (510500.SS), China CSI 1000 ETF (512100.SS), and HSCEI (^HSCE) closes come from the checksummed Yahoo chart windows. Correlations involving 512100 begin in 2017 after the saved 2016 rebasing discontinuity. The Surface is Deribit, 10 December 2025. Model algorithms, the House, frozen manifest, envelope and trial ledger are preserved during presentation polish. Normal restoration adds no market trials or sealed holdout access.

The polish evidence records actual endpoint and motion renders, inspected artifacts, numerical tests and sampled CPU speech integrity. Sampled signal and token timing checks do **not** complete full continuous production-voice pronunciation and synchronization listening.

## Primary sources and dated context

- Petra Vokata, [“Engineering Lemons,” JFE 142(2), 737–755 (2021)](https://petravokata.com/research). Its sample and fee estimates are not assumptions about Chinese snowballs. Calvet, Célérier, Sodini and Vallée (2023), JF 78(4), study Swedish capital-guarantee products and model-dependent household welfare.
- Korea FSC, [21 January 2016 release](https://www.fsc.go.kr/eng/pr010101/22122?curPage=6&srchBeginDt=&srchCtgry=1&srchEndDt=&srchKey=&srchText=): knock-in is different from realized maturity loss. Later press figures and November 2025 preliminary penalty notices are labeled with their historical status.
- Natixis, [18 December 2018 announcement](https://www.globenewswire.com/news-release/2018/12/18/1668988/0/en/natixis-natixis-confirms-its-strategic-ambitions-and-the-payment-of-a-1-5bn-special-dividend-despite-negative-non-recurring-items-in-4q18.html): €100m revenue reduction plus €160m provision. The [4Q2018 results](https://natixis.groupebpce.com/wp-content/uploads/2022/08/natixis_4q18.pdf) report a €259m non-recurring charge. Initial estimates, final accounting charges and realized cash losses are different quantities.
- [EU 2016/101, Article 11](https://www.legislation.gov.uk/eur/2016/101/article/11) addresses model-risk AVAs and 90% certainty of prudent exit value. A coupon spread between different contracts is not that calculation. [EBA's official day-one/AVA Q&A](https://www.eba.europa.eu/single-rule-book-qa/qna/view/publicId/2019_4458) and [AASB 9 B5.1.2A, the Australian IFRS 9 equivalent](https://standards.aasb.gov.au/aasb-9-feb-2025) specify the active-identical-quote or observable-input recognition condition. Deferral is conditional; release follows relevant valuation-factor changes, including time, rather than a universal straight-line rule.
- [Basel market-risk framework, MAR23](https://www.bis.org/committees/bcbs/basel-framework/standard/mar), residual-risk scope and exemptions; [FINRA Notice 12-03 (2012)](https://www.finra.org/sites/default/files/NoticeDocument/p125397.pdf), complex-product supervision. Local implementation and applicability matter.
- Federal Reserve [SR 26-2, 17 April 2026](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm), supersedes SR 11-7 and SR 21-8; risk-based, tailored guidance, most relevant to institutions above $30bn. Existing House tests are evidence, rather than independent validation of every function.
- Hobson (1998) and Brown, Hobson and Rogers (2001), [author copy of “Robust hedging of barrier options”](https://www.skokholm.co.uk/wp-content/uploads/2013/02/barriers.pdf). See the martingale, marginal and trading assumptions above.
- Frontier sources: [Zeron–Wu–Ruiz, 2023 preprint / 2025 revision](https://arxiv.org/abs/2305.06215); Sharma et al. [distributional RL](https://arxiv.org/abs/2407.10903) and [multi-asset pricing](https://arxiv.org/abs/2411.01121); [Cibrario et al. 2025](https://arxiv.org/abs/2507.19039); [Goudenège–Molent–Zanette, 2025 preprint / 2026 publication](https://arxiv.org/abs/2502.10300); [Glasserman–Karmarkar, 2025 preprint / April 2026 revision](https://arxiv.org/abs/2512.05301); [Higgins 2026](https://arxiv.org/abs/2602.01376); [Che–Lim–Sun 2026](https://arxiv.org/abs/2602.02996); [Lakshtanov 2026](https://arxiv.org/abs/2609.06137); [Fukasawa 2026](https://arxiv.org/abs/2610.00340); [Lopez-Piqueres et al., 30 October 2026](https://arxiv.org/abs/2610.42119). Their benchmarks and regularity conditions differ. Payoff-circuit depth, high-order Greek accuracy and simulated hedge results are not end-to-end hardware or general live-market guarantees.

The wider textbook and paper map is in [READING.md](../READING.md).

## Textbook audit

| Book · section | Where |
|---|---|
| Hull, *OFOD* 11th ed., "Exotic options" (ch. 27; ch. 26 in the Global Edition): packages | ch. 1 |
| — gap options; nonstandard American | gap = digital + call (ch. 5); American → Part 16 |
| — forward start; cliquets | ch. 12 |
| — compound; chooser | chooser by parity (problem 7); compound options as equity on assets → Part 20 |
| — barrier; binary; lookback; shout; Asian | ch. 3–4; ch. 5; ch. 6 (shout named as the lookback's cousin) |
| — exchange options; options on several assets | ch. 11 (Margrabe derived; Stulz named) |
| — volatility and variance swaps | Part 12 |
| — static options replication | ch. 4 (Derman–Ergener–Kani built, Carr–Ellis–Gupta derived and tested) |
| Hull, "More on models and numerical procedures" (path-dependent numerics) | ch. 6 (state augmentation, Vecer), Part 16 |
| Shreve II ch. 7: 7.2 maximum of BM with drift; 7.3 knock-out barriers | ch. 3 (reflection, Girsanov, the PDE) |
| — 7.4 lookbacks; 7.5 Asians (augmentation, change of numéraire) | ch. 6 |
| Bouzoubaa–Osseiran ch. 2 (structured products); 3.10 (structuring) | ch. 1–2 |
| — 3.9 Asians; 5.7–5.8 vanna, volga, multi-asset sensitivities | ch. 6; ch. 8, 11 |
| — ch. 7 correlation; ch. 8–9 dispersion, worst-of, best-of, rainbow | ch. 11; dispersion trading → Part 11; quantos → Part 22 |
| — ch. 10 barriers; ch. 11 digitals; ch. 12 autocallables | ch. 3–4; ch. 5; ch. 7–8, 11 |
| — ch. 13–14 cliquets (reverse, Napoleon) | ch. 12 |
| — ch. 15 mountain range | ch. 11 (named) |
| — ch. 16 volatility derivatives; ch. 17–21 hybrids, dynamic strategies | Part 12; Parts 19, 21, 22, 32 |
| Guyon–Henry-Labordère: the uncertain volatility model; local correlation, particle method | ch. 13; ch. 11 (named); LSV → Part 13; BSDEs → Part 17 |
| Wilmott, *PWOQF*: exotic and path-dependent options, barriers, Asians, lookbacks, uncertain parameters, static hedging | ch. 3–6, 12–13, 4 |
| Gatheral, *The Volatility Surface*: barrier options (put–call symmetry, static hedge); exotic cliquets | ch. 4; ch. 12 |
| Taleb, *Dynamic Hedging*: binaries, barriers, multi-asset options | ch. 5, 3–4, 11 |


---

# 量化金融，从零搭建 — 第15部分：奇异期权与结构化产品

本部分包括开场、十八章、研究篇与结尾，讲稿约65分钟，动画与阅读停顿另计。英文与中文采用相同的假设、数值及适用范围。核心例子是**示意雪球合约**，并非某笔真实成交。先写清现金流，再解释票息、希腊字母及发行人的对冲。

## 章节

| 章 | 内容 |
|---|---|
| 开场 | 雪球：真实ETF路径、假设票据障碍与历史背景 |
| 1–2 | 票据拆解、融资与初始模型利润；84个重叠的假设发行批次与投资者研究 |
| 3–4 | 反射、闭式解与PDE；离散观察与静态香草对冲 |
| 5–6 | 数字期权、一触期权与看涨价差；亚式、回望、控制变量与Vecer变换 |
| 7–8 | 雪球定价、状态与线性票息求解；完整展示网格上的发行人希腊字母 |
| 9–10 | 2024年1月的假设对冲账；韩国ELS两次事件与Natixis的历史披露 |
| 11–12 | 最差表现、相关性及条件相关性；棘轮与总vega以外的风险 |
| 13–14 | 不确定波动率与有限优化；同一市场曲面的不同近似拟合及熵倾斜 |
| 15–16 | 交易商流量的条件机制；三个种子的神经网络训练与多项式基线 |
| 17–18 | 审慎估值、首日利润、资本与模型验证；2023–2026年文献前沿 |
| 研究篇 | 香草期权能够给出的一触上界：鞅、原子、跳空与超对冲 |
| 结尾 | 三道口述交易台题、一道补充相关性题及十道有解习题 |

## 合约与数值约定

初始价格与本金均归一化为1。第**3至24个月，含两端**，观察价达到或超过1.03时，首次敲出，支付`1+c m/12`。某个日收盘价**严格低于0.75**时，敲入标记永久保留，但以后仍可敲出。到期未敲出的票据，若从未敲入，支付`1+2c`；若曾敲入，支付`min(S_T,1)`且无票息。因此，到期反弹仍可能恢复本金。票息在赎回或符合条件的到期日支付，并非按月现金分红。

原始计算每月使用**21个交易观察日**，两年共504日，不是严格的日历月安排。历史简单收益用持有月数除以12年化，既不是复利组合收益，也不是独立样本。历史波动率按244日年化，定价采用252步模型年；保留的这一约定属于近似。韩国ELS每半年使用123个交易观察日，各赎回事件以此前未赎回为条件，赎回会取消损失腿。

| 原始缓存结果 | 数值与含义 |
|---|---|
| 2021–2023年中证500ETF波动率 | 19.98%；在历史重建中固定使用 |
| 公平雪球票息 | 13.3537%；A=0.93828165，B=0.46218164，c*=(1−A)/B |
| 逐路径拆解 | 债券0.96078944＋提前还本0.02295316＋敲出票息0.05161465＋到期票息0.01010370−自动赎回取消的损失腿0.04546095＝1 |
| 模拟结局 | 78.415%敲出；17.6475%曾敲入后存续到期；3.9375%从未敲入并存续到期 |
| 预期寿命 | 9.895个月；与折现票息累积系数B不同 |
| 假设历史买家 | 84个重叠批次中26个亏损，最差简单收益−31.94%；25个在各自持有期内超过ETF价格涨幅 |
| 2024年ETF跌幅 | 2023年12月29日至2024年2月5日为−17.83%；ETF代理并非指数本身 |
| 假设账簿 | 现金对冲敞口最高25.19个票据本金，在ETF低点为14.59；初始对冲之后，模型买入24.86、卖出24.44 |
| 最差表现自动赎回 | 指定的不等波动率下，相关性0.3时票息23.26%，相关性1时13.57% |
| UVM账簿 | 有限求解器下界/上界0.31373/0.62340；加入所选香草对冲后0.41175/0.52007；逐腿上界之和1.00055 |
| 神经网络替代器 | 原始150个模型内参考点RMSE为0.01661，最大绝对误差0.10381；多项式RMSE为0.01084 |
| 速度 | 重复150点批量推断平均每输出0.304微秒；原始单次4万路径估值约0.309秒。训练标签51.19秒、训练2.26秒另计 |

拆解与票息求解使用**相同种子及路径**，因此样本恒等式只差舍入；换一批路径不保证恰好为1。损失腿会被自动赎回取消，不能直接当作一只无条件敲入看跌期权。初始模型利润未扣除对冲成本、准备金及其他费用。以r+s折现承诺、以r定价期权只是融资利差示意，并未联合模拟违约、回收与错向风险。

84个历史发行批次并非真实客户交易，彼此重叠，也不是84次独立市场试验。ETF价格比较不含指数股息。若障碍按发行价比例定义，较低的绝对发行价不会机械地扩大初始相对障碍距离。

## 各实验的适用范围

**障碍与静态对冲。** 常系数、连续观察、零返还DOC价格为7.28087；月度观察MC为7.44370，2520步网格MC为7.29390，后者仍不是连续观察。BGK是渐近修正，靠近障碍时尤其需要谨慎。显示的两倍朴素标准误不能在相关的对偶路径下直接当作置信保证。原始周度安排存在期末余数。路径反射图是网格示意。精确Carr–Ellis–Gupta复制需要**每个潜在触障时刻的条件看涨看跌对称性**，而非只有初始微笑对称；偏斜实验还含MC与观察网格误差。

**数字与亚式。** 连续、无摩擦Black–Scholes中数字期权可以复制，剩余期限大于零时delta平滑。临近到期难点在离散对冲。持有看涨价差的终值逐状态支配，不等于所有情况下离散动态对冲误差更小。零利率零股息时，其delta上界为1/ε。微笑斜率为负处的数字价格比较，应使用**相同行权价的波动率**；若和固定平值波动率比较，还混入波动率水平变化。连续几何平均的对数方差为σ²T/3，不代表算术亚式普遍只值香草的一半。1−ρ²方差公式假定固定的总体最优控制系数；同一样本估计系数还带来估计效应。散点显示全部1500个保存点，统计系数来自原始4000条路径。Vecer PDE限定连续平均且r=q=0。

**对冲与流量。** 发行人头寸delta等于正向标的对冲数量的负值；单位数与现金敞口不同。重平衡柱形图计算**当前价格乘标的数量变化**，不包含初始建仓。直接差分现金敞口还会算入盯市变化。缓存中的敲入日敞口变化混合了价格与时间变化，不是纯粹状态跳变。模型希腊字母、假设对冲策略、真实订单及因果市场冲击需要分别识别。长时期账簿使用固定希腊字母表插值，并保留端点截断；它不是实际库存或对冲损益。

**相关性、棘轮与不确定波动率。** 最差表现票据买家卖出损失看跌腿，因此做多相关性；发行人持有该腿，方向相反。两资产波动率不同时，相关性1也不会让归一化路径相同。历史相关性不是风险中性报价；条件筛选本身也会改变相关性，样本危机区间不能证明普遍规律或统计显著性。棘轮的总vega接近零仍有其他风险，有限网格最大值不等于精确零；随机常数波动率的局部Taylor分析不等于任意随机波动率定理。UVM存在网格误差，有限优化也不是全局证书。

**模型与替代器。** 四种曲面的近似拟合残差不同，奇异期权差价还混入拟合、模拟及离散化误差，不能当作共享完全相同香草边际分布的模型区间。KL只倾斜经验支付，没有施加鞅与校准约束；半径是指定参数，不是经验证的合理性、置信度或监管AVA。阈值比较现值与0.97 exp(−0.04)，不是统一的3%实际亏损。替代器只变三个输入，其余合约参数固定；150个合成参考点被反复查看，不能称为未触碰的市场留出集。单个状态的标签噪声0.00310低于观察误差，不能当作全局误差下限。批量推断速度不含标签、训练、校准及单次请求开销。

## 交易台题与解答

1. **用价差定价严格数字期权。** 买入K−ε看涨、卖出K看涨，各1/ε份；终值处处支配1{S_T>K}。光滑密度下，多付价格约为ε/2乘折现终值密度。更宽价差以较高价格换取较低最大delta；所示离散对冲误差只属于指定实验。
2. **发行人的vega符号与峰值？** 对所有现金流求导：损失腿减去提前还本及条件票息的vega。展示的障碍以上区域通常为正，但符号与峰值依赖状态、模型和合约；敲入不保证vega归零，也不强制回购期权。
3. **从数字价格得到一触价格？** 居中对数价格零漂移时，反射给出到期支付一触价格为匹配数字价格的两倍。标的零漂移是另一条件：r=q=0时，对数漂移为−σ²/2。S=100、H=90、T=0.5、σ=25%时，连续一触为0.58015，终值数字两倍为0.61172。
4. **三个指数的最差表现？** 在指定模型中，持有最差表现损失看跌通常受益于相关性下降；卖出该腿的票据买家方向相反。依赖微笑、基差、合约状态和模型风险不能由一个历史相关系数概括。

## 十道习题及推导

1. **反射与DOC。** 假设常系数Black–Scholes、S>H、K≥H、零返还、r=q=0。反射对数过程并换测度得到镜像项(S/H)C(H²/S,K)，故DOC=C(S,K)−(S/H)C(H²/S,K)。两项均满足PDE，差在H处为零，镜像项在允许的终值区域支付为零。结论依赖这些条件。
2. **BGK。** 离散观察会漏掉观察间触障后返回的路径。高斯随机游走的超越量带来βσ√Δt，β=−ζ(1/2)/√(2π)≈0.5826。下障碍移到H exp(−βσ√Δt)，上障碍向上移，用连续公式近似。有限模拟展示收敛，不证明精确恒等式或障碍附近误差界。
3. **几何亚式。** log G=n⁻¹Σ log S_ti为高斯，均值log S₀+(r−q−σ²/2)t̄，方差σ²n⁻²Σ min(t_i,t_j)，连续均匀平均极限为σ²T/3。对数均值m、方差v时，价格e^(−rT)[e^(m+v/2)N(d₁)−KN(d₂)]，其中d₂=(m−log K)/√v，d₁=d₂+√v。
4. **价差上界与边界。** 终值在K−ε以下为零，在[K−ε,K]线性上升，在K及以上为1。因此处处支配严格数字期权，但逐点极限是**1{S_T≥K}**，在K处仍为1。价格收敛到严格数字需要**K处没有终值原子**；否则极限多出e^(−rT)Pr(S_T=K)。
5. **雪球拆解。** 从到期债券开始，加提前还本价值、首次赎回票息及未敲入存续到期票息；仅在敲入后仍未赎回的路径扣除终值损失。赎回取消该损失腿。vega需对所有腿求导，仅用普通敲入看跌会漏掉取消条件。
6. **线性票息。** 每条折现支付为a+c b。第m个月首次赎回时b=D_m m/12；从未敲入并到期时b=2D_T；其他情况为零。故V=A+cB，B>0时c*=(1−A)/B=13.3537%。少给三个百分点票息产生0.03B=0.01386545的初始模型利润，尚未扣成本和准备金。
7. **选择期权。** 在t₁≤T选择，两个期权同K、同T，r与q确定。看涨看跌平价给出max(C,P)=C+e^(−q(T−t₁))(K e^(−(r−q)(T−t₁))−S_t₁)⁺。初始价格为一只到T的看涨，加e^(−q(T−t₁))份到t₁、行权价K e^(−(r−q)(T−t₁))的看跌。
8. **Margrabe。** 两个正的可交易GBM、零股息、常系数，以S₂为计价物。比值在对应测度下为鞅，方差率σ_X²=σ₁²+σ₂²−2ρσ₁σ₂。交换看涨价格S₁(0)N(d₁)−S₂(0)N(d₂)，d₁=[log(S₁/S₂)+σ_X²T/2]/(σ_X√T)，d₂=d₁−σ_X√T。σ_X=0取确定性极限；有股息需调整预付远期。
9. **下触界（进阶）。** 非负一致可积价格鞅、零利率股息、无摩擦且允许相应策略、一触到期支付、B<S₀。S_T≤B必已触障，故Pr(S_T≤B)≤OT。任取K>B，持有1/(K−B)份看跌，在首次下触τ买入等量远期。触障时S_τ≤B，终值至少[(K−S_T)⁺+S_T−B]/(K−B)≥1；未触障时非负。可选抽样在可积条件下使远期策略零初始成本，所以OT≤inf_(K>B)P(K)/(K−B)。光滑内点最优满足(K*−B)P′(K*)=P(K*)；有原子时用凸次梯度，凸性本身不保证唯一或达到最优。B处有原子时，终值下界使用看跌的**右导数**。适当连续模型及边际条件下上界尖锐，不代表该下界也尖锐或中间每个价格都可达到。
10. **上触界（进阶）。** B>S₀，任取K<B，持有1/(B−K)份看涨，在首次上触时卖出等量远期。触障后的终值至少(S_τ−K)/(B−K)≥1，上跳超越量只会增加保护。相同鞅及交易条件下，OT_up≤inf_(K<B)C(K)/(B−K)。零利率股息、S₀=1、σ=50%、T=0.25、B=1.2时，数值结果约K*=0.973、上界0.494、模型一触0.424、终值数字0.196；有限数值最小化不是全局最优达到性的证明。

## 研究篇的数据解释

图中带状范围来自**Heston自身的经验看跌价格**与有限行权价网格。其他模型近似拟合的终值边际不同，落在同一带内不是共享边际定理的检验。

| 下障碍 | Heston终值下界 | Heston日网格一触 | Heston经验看跌上界 |
|---|---:|---:|---:|
| 0.70 | 0.08465 | 0.14360 | 0.21359 |
| 0.80 | 0.16360 | 0.28550 | 0.41431 |
| 0.90 | 0.29875 | 0.53555 | 0.72117 |

原始模拟为2万条路径、79天。B=0.8时，其他模型一触为0.28045至0.29965。K=0.96的Heston超对冲最小样本盈余为零、平均0.12707；价格差为0.12881，两者差是远期收益的样本均值，不是有限样本中严格为零的恒等式。直方图均除以全部2万路径，展示窗口以外127个样本不重新归一化。日观察、有限行权价与MC误差使该例不能成为连续模型尖锐界的数值证书。

## 复现、来源与验证状态

上方命令使用原始固定种子缓存。modelrisk依赖第13部分校准，digital_skew依赖第12部分曲面。价格数据是带校验和的Yahoo窗口：510500.SS、512100.SS与^HSCE；512100的相关性从2017年开始，以避开保存数据中的2016年重定基准。曲面来自2025年12月10日Deribit。展示润色保持原算法、House、冻结市场清单、风险约束与试验台账，不增加市场试验或读取封存留出集。

英文上方提供主来源链接。Petra Vokata的《Engineering Lemons》发表于2021年JFE，不能继续标为未确认工作论文；瑞典福利研究的结论依赖模型。FSC 2016区分敲入与实际损失；2025年罚款通知按当时初步状态描述。Natixis 2018年12月初始披露为1亿欧元收入减少加1.6亿准备，最终季度报告为2.59亿非经常费用；这些不是同一种已实现现金损失。

EU 2016/101第11条的90%审慎退出价值要求不等于不同合约票息之差。IFRS 9及AASB等效准则B5.1.2A的首日确认条件包括相同工具活跃报价或仅使用可观察市场输入；不满足时的递延与释放取决于相关估值因素变化，并非所有雪球都直线摊销。MAR23的范围、豁免与本地实施均需核对。美联储2026年4月17日SR 26-2取代SR 11-7与SR 21-8，强调风险及规模相称。现有代码测试不等于每个函数均经独立验证。前沿论文各有正则性与基准条件，支付电路深度、模拟对冲或特定高阶希腊字母结果不能外推成端到端硬件优势或实盘保证。

润色证据区分实际端点/运动渲染、人工查看、数值测试与抽样CPU语音信号检查。抽样信号及词时序检查**不能代替完整生产语音的连续发音与同步听审**；该项继续单独跟踪。
