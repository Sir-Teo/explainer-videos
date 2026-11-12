

# Quant, Built — Part 33: Statistical Arbitrage

Pairs, cointegration screens, OU spreads, factor residuals, adaptive hedge ratios, reversal, liquidity and a band theorem. Part 33 of the [43-part series](../README.md). The financial algorithms in `compute.py` and the House are preserved. This review uses nine verified ordinary outputs and no sealed-year strategy result. It establishes research diagnostics and a mathematical policy theorem, not a live allocation.

## Evidence and scope

Each unchanged original was invoked once: `pairs`, `coint`, `pca`, `kalman`, `lomac`, `nagel`, `deep`, `theory`, `smallc`. All nine passed the public-input barriers. No function retry, refresh, new market trial, registry mutation or sealed strategy payload access occurred. The loader rejects every envelope-prefixed name before cache metadata or counted access, and rendering requires existing ordinary caches.

French industry and size data are restricted to research through 2020 by the original readers. The BTC/ETH example uses 2018–2020 after public raw assembled bars are parsed; those raw public files extend beyond 2020. Public raw parsing is distinct from accessing a sealed strategy experiment. Cboe VIX supports a descriptive industry regression. Complete-history coverage selects universes retrospectively rather than supplying point-in-time membership. Reported stock-paper results and firm histories are attributed, not reproduced.

Verified ordinary values include:

| Diagnostic | Value | Interpretation |
|---|---:|---|
| Distance proxy, 43 complete-history industries, 1964–2020 | Sharpe −0.248 | Negative sample mean under this implementation; not a GGR stock replication |
| Annual fixed-critical cointegration screen | 7.29% passes | Same seeded 300 industry pairs each year |
| Independent random-walk controls | 3.67% passes | 300 simulated 252-step controls; uncertain calibration |
| Pass next year conditional on passing | 8.14% | Descriptive persistence with repeated assets and tests |
| Fixed-band synthetic residual proxy | Gross 0.879; charged −0.392 Sharpe | Fitted residual P&L and incomplete cost accounting |
| Mathematical-band synthetic proxy | Gross 1.134; charged 0.211 Sharpe | Same reused research sample; no independent band validation |
| Three-seed MLP, nominal 2017–2020 test | IC 0.003409; charged Sharpe −7.222 | Synthetic target, retrospective universe and a chronological research split |
| Pure OU illustration, dimensionless cost 0.3 | Numerical band 1.032879 widths | Bounded grid optimizer, not an exact symbolic root |

The restoration logs, source audit, public-input events, checksums and protected-file checks are in `renders/qa/quant33/`. The artifact-bound completion evidence below distinguishes construction diagnostics, final visual reviews and sampled CPU speech checks. A silent preview or sampled speech analysis does not establish continuous production listening.

## Chapters

1. Hook: common trends and a chosen mean-reverting log gap; statistical and economic claims.
2. History: Thorp, Morgan Stanley, D. E. Shaw, Renaissance and PDT, as reported.
3. Distance pairs: formation and trading conventions, retrospective coverage, shorting and cost limits.
4. Cointegration: fixed-critical screens, noisy controls, selection, persistence, baskets and economic hypotheses.
5. OU: exact regular-interval AR(1) map, s-scores, slope bias and nonlinear half-life uncertainty.
6. PCA residuals: eigenportfolios, constrained cumulative residual endpoints, synthetic P&L and cost omissions.
7. Kalman: prior-state innovation, current regressor, retrospective fixed ratio and the scalar memory analogy.
8. Lead-lag: population covariance identity, finite-sample boundary correction, five-observation blocks and microstructure.
9. Deep: a small MLP, chronological research split, prediction targets and trading objectives.
10. Liquidity: descriptive lagged-VIX regression, conventional errors, crowding and limits of arbitrage.
11. Evaluation protocol: information clock, holdings, cash, actual turnover, research selection and precision; no sealed verdict.
12. House: source excerpts, interpretation, risk design, capacity and proposed monitoring.
13. Research: symmetric OU cycle, first-passage times, unique positive-cost optimum, frictionless supremum and cube-root asymptotics.
14. Recap, six desk questions and twelve exercises: six basic, four advanced, two qualifying.

## Implementation conventions that affect interpretation

- Distance pairs normalize each formation path by its first observed price. Trading indices restart each half-year. Lagged discrete positions multiply half the return difference; these are not fixed-share buy-and-hold pairs. The `trips` field counts openings, including positions not explicitly liquidated at the final boundary. `cost_year` is a rough conversion, not reconstructed net wealth.
- The cointegration screen uses a constant, one lagged difference and a fixed residual critical value −3.34. It is not a universal 5% calibration or a false-discovery probability. Selected half-lives are estimated on the selection window. A representation theorem does not identify a causal economic force.
- OU mapping requires a positive regular interval and 0 < b < 1. The helper drops nonfinite values, compressing gaps, and estimates innovation deviation with two regression degrees of freedom. Kendall's slope-bias formula is a stationary intercept-fitted asymptotic approximation. Applying a nonlinear half-life map to an expected slope does not give the expected fitted half-life.
- PCA correlations use trailing 252 observations through the current close and refit every 21 observations. Residual OLS includes an intercept: its residuals sum to approximately zero, tying the cumulative path down at its window endpoint. Apparent reversion can partly be a finite-window fitting constraint.
- Next-period synthetic residual P&L subtracts the intercept as well as factor returns; an asset-minus-hedge cash account does not automatically receive that subtraction. Normalization is by active industry signals, not total industry-plus-hedge gross capital.
- The cost proxy is twice fixed one-way cost times discrete-signal changes divided by the new active count. It misses rescaling of continuing positions as that count changes. When the new book is empty, net P&L is set to zero and the final exit charge is omitted. Separate hedge approximations can overstate other costs. There is no proven conservative direction for the combined error.
- Nine residual configurations reuse research data. The mathematical band's lookup uses 31 cost points with endpoint clipping. This is not independent discovery or a globally optimal portfolio policy.
- Kalman gain depends on both state covariance and the current loading vector (1, log BTC price). The √(r/q) memory analogy assumes a scalar state with constant unit loading and small q/r; it is not a universal window for the two-state regression. An innovation observed at today's close is not prior tradable wealth. Fixed-residual test critical values do not calibrate an adaptive generated innovation.
- “Weekly” output uses consecutive blocks of five observations, not calendar weeks. An era is assigned by the block's first date. The population Lo–MacKinlay identity is exact; its sample estimates can differ from realized profit because full-sample centering and lagged endpoint means differ. Moment terms do not identify overreaction or news diffusion causally.
- The VIX regression sums daily gross-normalized contrarian P&L arithmetically within months. It uses the previous month's final VIX close and conventional independent homoskedastic errors, not HAC errors. VIX quintiles are descriptive research-sample groups. This is not a replication of Nagel's stock design.
- The MLP averages three seeds, trains through 2012, validates in 2013–2016 and uses nominal test dates 2017–2020. Each 30-component path ends in zero by construction. Complete-history coverage and research reuse limit independence. Demeaned, unit-gross forecasts and a fixed two-leg cost proxy do not establish full financed wealth.

## The band theorem

Assume dX = −κX dt + σ dW with κ, σ > 0, known constant parameters and continuous monitoring. Wait flat from 0 until |X| = m, hold one unit against the displacement, and exit at 0. Pay a constant round-trip cost c ≥ 0 in spread units. There is no risk budget, stop, discounting, financing cost or structural break. The objective is long-run expected profit per time within this symmetric policy family, not Sharpe or a return on invested capital.

Let s = σ/√(2κ), u = m/s, d = c/s, a = √(π/2), and I(u) = ∫₀ᵘ exp(z²/2) dz. The mean cycle time is a I(u)/κ, so

\[
R(m)=\frac{\kappa s}{a}\frac{u-d}{I(u)}.
\]

For d > 0 the unique optimum solves I(u*) = (u* − d) exp(u*²/2), with u* > d. For d = 0 the supremum is approached as m ↓ 0, with R(0⁺) = σ√(κ/π); no positive band attains it. At fixed s and c, changing κ scales the rate but leaves the band fixed. Holding σ instead changes s and therefore the dimensionless cost.

The library evaluates first-passage integrals by Simpson quadrature and uses a bounded grid optimizer (0.02s to 3s with one refinement). A returned zero-cost positive band is a grid artifact, not the attained frictionless optimum. `band_curve` replaces zero cost by a small positive value. Stored grid simulations use exact OU transitions between dates but credit each completed cycle m − c at the ideal band/mean, excluding execution overshoots. They illustrate crossing-time discretization. Twice fine minus coarse is a heuristic square-root-step extrapolation, not certified continuous-time execution; equal seeds do not couple the Brownian paths, and the nine-row rate table has no Monte Carlo error bars.

## Six desk questions, answered

1. **What is traded in a cointegrated pair?** A fixed linear combination such as y − βx is a statistical spread. A trade requires actual shares, normalization and cash flows. The relation can break; β is estimated; screening creates selection; funding and shorting can bind.
2. **What is an s-score?** (X − θ̂)/ŝ for a specified fitted OU spread, with a valid regular-interval fit. It measures distance in fitted equilibrium-width units, not the probability of a profitable trade. Historical thresholds are policy choices.
3. **Does a short-lived Kalman innovation prove cointegration?** No. Its adaptation can produce stationary-looking forecast errors without a stable fixed linear combination or profitable rebalanced holdings. Check the information set and the return objective.
4. **Where can contrarian expected profit come from?** Weighted own lag covariance, off-diagonal lag covariance and a negative mean-dispersion term. These are moment contributions, not identified causal mechanisms.
5. **Why do residual results need a cost audit?** The stored algorithm charges a proxy, omits some rescaling and exits, and does not establish full hedge and cash holdings. Actual trades, financing and gross capital must be reconstructed before an investment claim.
6. **How does the OU band depend on cost?** Under the stated fixed policy and known-parameter assumptions, u* depends on d alone. For d ↓ 0, u* ∼ (3d)^(1/3). Speed comparisons hold equilibrium width fixed; this is conditional scaling.

## Twelve exercises with complete solutions

### Basic 1 — Speed from a daily slope

Given b = 0.9 and Δt = one day, b = exp(−κΔt) implies κ = −ln(0.9) = 0.1053605 per day. Since the conditional mean displacement decays as exp(−κt), halving requires exp(−κh) = 1/2. Thus h = ln 2/κ = 6.5788 trading days. This is decay of the conditional mean, not a guaranteed hitting time. The mapping assumes a stationary OU sampled regularly.

### Basic 2 — False passes and a family-wise bound

Forty-nine assets give M = 49×48/2 = 1,176 unordered pairs. If every null is true and each test has calibrated size α = 0.05, linearity of expectation gives E[V] = ΣPr(reject null j) = 1,176×0.05 = 58.8 false passes; cross-pair independence is unnecessary. To bound the probability of any false pass by 0.05, the union bound permits marginal level α/M = 0.000042517 = 4.2517×10⁻⁵. This is Bonferroni, valid under dependence for valid individual tests. The fixed −3.34 screen is not automatically calibrated at that adjusted level; it needs appropriate critical values or valid p-values.

### Basic 3 — A cost-scaled band

Choose equilibrium width s = 2% and fixed round-trip spread cost c = 0.6%, so d = c/s = 0.3. The stored numerical policy calculation gives u ≈ 1.032879, hence m = su ≈ 0.02065758 = 2.065758%. This number is a bounded quadrature/grid approximation. The leading small-cost law gives u ≈ (0.9)^(1/3) = 0.965489, or m ≈ 1.930979%. Cost 0.3 is not infinitesimal, so the asymptotic error is unsurprising. The units are spread displacement, not gross portfolio capital.

### Basic 4 — A specified residual cost illustration

Choose annual gross Sharpe 0.8, annual volatility 4%, daily turnover τ = 0.2 per leg, two legs and one-way cost k = 5 bp per traded dollar. Gross mean is 0.8×0.04 = 0.032 = 3.2% annually. Under constant turnover and 252 trading days, annual cost is 2kτ×252 = 2×0.0005×0.2×252 = 0.0504 = 5.04%. Net mean is −0.0184 = −1.84%. If costs are deterministic and volatility unchanged, net Sharpe is −0.0184/0.04 = −0.46. This chosen arithmetic does not fix the stored algorithm's missing holdings and turnover.

### Basic 5 — One cross-covariance

For N = 2, choose zero means and zero own lag covariances; let the only nonzero element of Γ = Cov(r_t,r_{t−1}) be Γ₂₁ = γ. The contrarian weights are w_i = −(r_{i,t−1} − r̄_{t−1})/2. Explicitly, w₂ = (r₁,t−1 − r₂,t−1)/4 and w₁ = −w₂. Taking E[w₁r₁,t + w₂r₂,t] leaves γ/4. Equivalently the off-diagonal term is γ/N², own and mean-dispersion terms vanish. Profit is positive only if γ > 0, before implementation costs; no own-price reversal is required.

### Basic 6 — Correlated innovations

An innovation with AR(1) slope 0.3 retains positive serial dependence under that descriptive fit. It may indicate misspecification or unmodeled dynamics, but does not uniquely identify a slow filter. Cointegration instead requires integrated price series with a stable stationary fixed combination under the relevant definition. Adaptive residual stationarity, or its failure, is insufficient. Specify a fixed spread, estimate with prior information, check stability, and evaluate actual subsequent holdings after costs. The innovation statistic alone supplies no verdict.

### Advanced 7 — Turnover units

Choose gross mean 2 bp/day and define τ = Σ|Δw_j| = 0.4 as total one-way traded gross weight. With k = 5 bp per dollar, cost is kτ = 2 bp/day and net mean is 0 bp/day. If “turnover” instead means half that sum, use 2kτ, producing 4 bp cost and −2 bp net. If τ is specified separately for two legs, add both legs. No extra round-trip factor is justified without a definition. The stated answer zero uses the first convention and deterministic linear costs; financing and impact are excluded.

### Advanced 8 — IC sample size

For a small correlation from n independent, comparable forecast/target pairs, use se(IC) ≈ 1/√n. To separate IC = 0.01 from zero by two standard errors requires 0.01√n ≥ 2, so n ≥ 40,000. With 49 independent pairs each day, T ≥ 40,000/49 = 816.3265 days; 252 days/year gives 3.2394 years. Cross-sectional correlation, overlapping targets, serial dependence and selection reduce effective information, so this pooled iid calculation is a conditional planning illustration. It is neither guaranteed power nor proof after 3.24 years.

### Advanced 9 — Sharpe precision

Under the basic iid-return, low-Sharpe approximation, annual Sharpe standard error is about 1/√Y for Y years. For true annual Sharpe 0.3, set 0.3√Y = 2, giving Y = (2/0.3)² = 44.4444 years. This equates expected signal to two approximate standard errors; it is not a 95% power calculation. Higher moments, serial dependence, varying risk, estimator details and research selection alter it. Five years would give approximate error 0.4472, larger than 0.3, even before those complications.

### Advanced 10 — Small-cost arithmetic

Choose d = 0.01. The leading asymptotic band is u = (3d)^(1/3) = 0.3107233. The leading retained frictionless rate is 1 − (3d)^(2/3)/2 = 0.9517255, about 95.17%. The unchanged bounded optimizer gives u ≈ 0.3129916 and rate 0.7598024 in κ = s = 1 units. Dividing by R(0⁺) = √(2/π) = 0.7978846 gives approximately 0.95227. This is a numerical comparison against an asymptotic prediction, not an exact finite-cost equality or evidence from market data.

### Qualifying 11 — Passage times, renewal and a unique optimum

Assume the OU model and policy stated above, start flat at zero, and take m > 0. Each cycle first hits either ±m and then returns to zero. Strong Markov and symmetry make successive full-cycle durations identically distributed and independent; their expectations are finite for this positive recurrent OU process and finite m. A full cycle has fixed reward m − c. The renewal-reward theorem gives almost-sure long-run completed-cycle rate R = (m−c)/(E₀τ_m + E₋ₘT₀). Incomplete-cycle mark-to-market needs its own accounting if one defines a wealth process; this policy formula concerns the renewal reward.

For a hitting-time expectation f(x), Dynkin's equation is (σ²/2)f″ − κxf′ = −1 in the continuation region, with zero value at the target boundary. Multiplying by exp(−κx²/σ²) yields

\[
(e^{-\kappa x^2/\sigma^2}f')'=-\frac{2}{\sigma^2}e^{-\kappa x^2/\sigma^2}.
\]

For hitting zero from x < 0, exclude the explosive homogeneous solution at the natural left boundary (the bounded-slope solution suffices). Then
f′(y) = −(2/σ²)exp(κy²/σ²)∫₋∞ʸ exp(−κz²/σ²)dz. Integrate from −m to 0, using f(0)=0, to obtain

\[
E_{-m}T_0=\frac{2}{\sigma^2}\int_{-m}^0e^{\kappa y^2/\sigma^2}\int_{-\infty}^y e^{-\kappa z^2/\sigma^2}dz\,dy.
\]

For exit from (−m,m), the expectation is even, so f′(0)=0; integrating the same equation from 0 gives the inner lower limit 0. With f(m)=0,

\[
E_0\tau_m=\frac{2}{\sigma^2}\int_0^m e^{\kappa y^2/\sigma^2}\int_0^y e^{-\kappa z^2/\sigma^2}dz\,dy.
\]

Set x = sz and τ = κt. The scaled SDE is dZ = −Z dτ + √2 dB, with generator ∂²_z − z∂_z (not ½∂²_z − z∂_z). Mean physical times scale by 1/κ. Reflecting the negative integral and adding it to the positive one cancels their variable inner pieces, leaving
κ(E₀τ_m + E₋ₘT₀) = a∫₀ᵘ exp(z²/2)dz = aI(u). Thus R = (κs/a)(u−d)/I(u).

For u > d, differentiate: the sign of R′ is the sign of I(u) − (u−d)exp(u²/2). Define H(u)=u−exp(−u²/2)I(u). The first-order equation is H(u)=d. H(0)=0 and H′(u)=u exp(−u²/2)I(u)>0 for u>0; also H(u)→∞ because exp(−u²/2)I(u)∼1/u. There is exactly one root for d>0, above d since H(u)<u. The derivative is positive before it and negative after it, and the rate tends to zero as u→∞, establishing the unique global maximum in this policy family. Its dimensionless band depends on d alone.

### Qualifying 12 — Frictionless limit and cube-root asymptotics

Expand in u=m/s, keeping κ times the expected times dimensionless. With a=√(π/2), the integrand exp(y²/2)∫₋∞ʸ exp(−z²/2)dz equals a+y+ay²/2+y³/3+ay⁴/8+… . Integrating over [−u,0] gives
κE₋ₘT₀ = au − u²/2 + au³/6 − u⁴/12 + au⁵/40 + O(u⁶).
The waiting integral gives κE₀τ_m = u²/2 + u⁴/12 + O(u⁶). Even terms cancel; their sum is aI(u)=a(u+u³/6+u⁵/40+…). With d=0,
R=(κs/a)u/I(u)→κs/a=σ√(κ/π). Since I(u)>u for u>0, this value is strictly above every positive-band rate: it is a supremum, not an attained finite optimum.

For positive small d, expand the exact first-order relation d=H(u)=u−exp(−u²/2)I(u). Multiplying series gives exp(−u²/2)I(u)=u−u³/3+u⁵/15+O(u⁷). Hence d=u³/3−u⁵/15+O(u⁷), and the unique root satisfies u*³=3d+O(d^(5/3)), so u*∼(3d)^(1/3).

The rate divided by its frictionless limit is (u−d)/I(u)=(1−d/u)/(1+u²/6+O(u⁴)). At the optimum d/u=u²/3+O(u⁴), yielding 1−u²/2+O(u⁴)=1−½(3d)^(2/3)+o(d^(2/3)). The exponent resembles a quadratic-risk holdings band, but here it comes from the OU cycle-time expansion and fixed renewal reward. It is not a universal transaction-cost theorem.

## A finite-sample correction for the lead-lag table

Let μ be the full-T sample mean, X_t=r_t−μ, H=I−11ᵀ/N, and Γ̂=(T−k)⁻¹Σ X_tX_{t−k}ᵀ. The plug-in total is −tr(Γ̂H)/N − μᵀHμ/N. Expanding the realized −(T−k)⁻¹Σr_tᵀHr_{t−k}/N gives that plug-in plus

\[
\delta=-\frac1N\mu^\top H(\overline X_{\rm now}+\overline X_{\rm lag}).
\]

The lagged endpoint subarrays need not have zero means even though the full array does. That is why rounded sample equality is not an exact identity. Stationary population expectations remove the centering cross terms under their assumptions, without supplying causal attribution.

## Build and verification

The ordinary computations have already been run once for this review. Do not run the unqualified compute command: it includes the excluded experiment. Do not refresh inputs or rerun missing/failed originals. Scene rendering must use verified caches, with the loader barrier in place.

```bash
python -m pytest -q tests/test_quant_house.py::test_statarb_ou_band_and_decomposition
EXPLAINER_TTS=silent python tools/qa_scene.py quant33 Research
python tools/build.py quant33 --lang en
python tools/build.py quant33 --lang zh
```

The pure mathematical test is already recorded for this review; commands above explain the workflow, not permission for repeated originals. English and Chinese final visual receipts must bind current source. Sampled CPU speech checks and an actual narrated opening are separate from continuous production listening.

## Reading

Vidyamurthy, *Pairs Trading* (2004); Pole, *Statistical Arbitrage* (2007); Chan, *Algorithmic Trading* (2013); Pedersen, *Efficiently Inefficient* (2015); Leung and Li, *Optimal Mean Reversion Trading* (2016). Papers include Engle–Granger (1987), Grossman–Miller (1988), Lehmann and Lo–MacKinlay (1990), Johansen (1991), Gatev–Goetzmann–Rouwenhorst (2006), Khandani–Lo (2007/2011), Avellaneda–Lee and Bertram (2010), Nagel (2012), Krauss–Do–Huck (2017), and Guijarro-Ordonez–Pelger–Zanotti (2021). Firm histories are public reported accounts. This is education in methods.

---

# 量化金融，从零搭建 — 第33部分：统计套利

本部分讨论配对、协整筛选、OU价差、因子残差、动态对冲、反转、流动性及交易区间定理。保留`compute.py`与公司金融算法，使用九个已核验的普通计算结果，不使用封存年份的策略结果，也不据此建立实际配置。

## 证据与解释边界

`pairs、coint、pca、kalman、lomac、nagel、deep、theory、smallc`各执行一次并通过冻结公共输入检查；没有重试、刷新、新市场试验、登记修改或封存策略载荷访问。加载器先拒绝所有以envelope开头的名称，再检查普通缓存。French研究数据截止2020年；BTC/ETH读入的公共原始文件延伸至2025年，之后按原代码筛到2018–2020年。这与读取封存策略载荷不同。完整研究历史决定资产覆盖，属于事后完整性筛选，并非当时可得的成员表。

核验值包括：43行业距离代理夏普−0.248；年度协整通过率7.29%，300条随机游走对照通过率3.67%，次年再次通过8.14%；标准区间残差代理毛夏普0.879、扣代理成本后−0.392，数学区间为1.134与0.211；小网络名义测试期IC为0.003409，扣代理成本后夏普−7.222。它们是指定实现的描述统计，不证明可实施财富。普通结果、输入事件与哈希记录保存在`renders/qa/quant33/`。

关键约定如下：距离法每半年重启交易指数，滞后离散仓位乘收益差的一半；`trips`统计开仓，不保证全部完成往返或期末平仓。协整使用同一批300行业对、常数和一个差分滞后及固定−3.34门槛；不是普适的5%校准。OU映射要求规则正间隔及0<b<1，删除缺失值会压缩时间。肯德尔斜率偏差的近似经过非线性半衰期映射后，不等于平均半衰期。

PCA用截至当日的252观测窗口，每21观测重估。含截距OLS残差和约为零，累计残差的窗口终点因此被钉住，表观回归可部分来自拟合约束。次期合成残差扣掉截距及因子收益，不能直接视为资产减对冲的真实现金流。分母是活跃行业信号数，不是全部对冲后的总敞口。成本按离散信号变化除以新活跃数估计，遗漏活跃数改变时持续仓位的缩放；新仓位全空时又把净利润设零，漏掉退出费用。单独对冲近似可能向另一方向偏误，合计误差没有已证实的保守方向。

卡尔曼两状态增益受当前载荷向量与价格单位影响，√(r/q)记忆长度只属标量恒定单位载荷的小噪声比近似。当前创新不是先前可交易财富，也不能用固定协整检验的临界值直接校准。所谓周度是连续五观测块，不是日历周。Lo–MacKinlay总体恒等式精确，但样本全期中心化与滞后子样本端点均值不同，实际利润可含边界修正。协方差分解不识别因果。VIX月结果是日代理利润的算术和，使用前月末VIX和常规独立同方差误差，不是HAC，也不是Nagel股票设计的复现。三种子MLP使用截至2012年训练、2013–16验证及2017–20名义测试；研究期复用和事后覆盖限制独立性，30维路径末项恒零。

章节依次为开篇、历史、距离配对、协整、OU、PCA、卡尔曼、领先滞后、网络、流动性、评估协议、公司代码与风险、研究定理、回顾和习题。第十章说明信息时钟、真实持仓与现金、成本、选择和精度，不给封存期结论。

## 区间定理与六个交易台问题

假定κ、σ为已知正常数，连续监控dX=−κXdt+σdW。空仓等到|X|=m，逆向持有一个单位，到零退出，支付固定往返成本c≥0，单位与价差相同。目标是这个对称规则族的长期期望利润每时间，不是夏普或资本回报；没有融资、止损、风险预算、折现或断裂。令s=σ/√(2κ)、u=m/s、d=c/s、a=√(π/2)、I(u)=∫₀ᵘexp(z²/2)dz。周期期望为aI(u)/κ，故R=(κs/a)(u−d)/I(u)。正成本时唯一最优解满足I(u*)=(u*−d)exp(u*²/2)，且u*>d。零成本的σ√(κ/π)是m趋零时的上确界，不由任何正区间取得。固定s及c时，速度只缩放利润；固定σ则s也会变。

1. **协整时交易什么？** 固定线性价差是统计对象；实际交易还需份额、现金和分母。联系可能断裂，估计与筛选有误，借券融资也可能受限。
2. **s分数是什么？** 对指定OU拟合的(X−θ̂)/ŝ，表示相对拟合宽度的偏离，不是获利概率；阈值是政策选择。
3. **短命卡尔曼创新证明协整吗？** 不证明。动态修正可以形成平稳外观，但并未给出稳定固定组合或盈利的调仓财富。
4. **逆向期望利润来自哪里？** 自身滞后协方差、非对角滞后协方差和负均值离散项，是矩的贡献而非已识别因果。
5. **残差结果为何需要成本审计？** 现有代理缺少部分缩放和退出交易，也未建立完整现金和对冲持仓；必须重构实际交易与融资。
6. **区间如何依赖成本？** 在指定已知参数规则下，u*只取决于d，小成本时u*∼(3d)^(1/3)。这不是一般投资组合控制定理。

数值库用辛普森积分和0.02s至3s的有界网格加一次细化，不是符号精确根。零成本返回的正下界不是数学最优值。网格模拟在观测日期间使用精确OU转移，但按理想区间与零点给每次交易计m−c，不按超调成交；两倍细网格减粗网格是平方根步长偏差的启发式外推，同种子并未耦合布朗路径，九行速率表没有蒙特卡洛误差条。

## 十二道完整解答：六基础、四进阶、两资格题

### 基础1 — 斜率与速度

给定b=0.9、间隔一天，由b=exp(−κΔt)得κ=−ln0.9=每天0.1053605。条件期望偏离按exp(−κt)衰减，令其为1/2得半衰期h=ln2/κ=6.5788交易日。它描述条件均值减半，不保证实际首达时间。必须满足规则采样及平稳OU映射的假设。

### 基础2 — 假通过与家族错误

49个资产有M=49×48/2=1176个无序对。若全部原假设为真且各检验真实大小为0.05，期望假拒绝数E[V]=ΣPr(拒绝第j个真原假设)=58.8，不要求不同配对独立。要使至少一次假拒绝的概率不超过0.05，用并集上界将每项水平设为0.05/1176=4.2517×10⁻⁵，即Bonferroni校正。相关检验仍可使用，但单项p值或临界值必须有效；固定−3.34不自动提供这个调整后的水平。

### 基础3 — 成本尺度

指定s=2%、固定价差单位往返费c=0.6%，得d=0.3。已核验普通数值计算给u≈1.032879，故m=su≈0.02065758，即2.065758%。这是假定规则下的有界积分网格近似。小成本首项给u≈0.9^(1/3)=0.965489，即m≈1.930979%；d并非无穷小，存在近似误差。这里百分比是价差位移，不是投资组合资本收益。

### 基础4 — 指定成本算例

指定年毛夏普0.8、年波动4%、每条腿日换手0.2、两条腿、每交易一美元单向费5基点。毛均值0.8×0.04=3.2%/年。252日恒定换手的成本为2×0.0005×0.2×252=5.04%/年，净均值−1.84%。若费用确定且波动不变，净夏普为−0.0184/0.04=−0.46。这个指定算术不修复原残差算法缺少的持仓与换手。

### 基础5 — 单一交叉协方差

N=2、均值零、自身滞后协方差零，仅Γ₂₁=Cov(r₂,t,r₁,t−1)=γ非零。逆向权重w₂=(r₁,t−1−r₂,t−1)/4，w₁=−w₂。展开E[w₁r₁,t+w₂r₂,t]，仅保留γ/4；也等于非对角项γ/N²。只有γ>0时该毛期望为正，不要求任何资产自身反转，执行成本还未计入。

### 基础6 — 创新相关

创新的描述AR(1)斜率0.3说明仍有正序列依赖，可能涉及模型误设或遗漏动态，并不唯一说明滤波过慢。协整要求积分价格之间存在稳定的固定平稳线性组合。自适应误差平稳或不平稳均不足以单独判断。应先定义固定价差、使用先前信息估计、检查稳定性，再评价实际后续持仓和成本。仅凭这个创新统计没有协整结论。

### 进阶7 — 换手定义

给毛均值每日2基点，并定义τ=Σ|Δw_j|=0.4为单向总交易权重，费k=5基点，则成本kτ=2基点，净均值为零。如果换手指绝对变化和的一半，应使用2kτ，成本4基点、净−2基点；若每条腿各有0.4，须另加两条腿。没有明确约定就不能再随意乘往返倍数。答案零使用第一种定义，排除融资与冲击。

### 进阶8 — IC需要多少样本

小相关的n个独立且可比预测目标对，近似标准误为1/√n。令0.01√n≥2，得n≥40000。若每天49对相互独立，则需要40000/49=816.3265天，除以252为3.2394年。相关资产、时间依赖、目标重叠及选择降低有效信息。该合并独立同分布计算只是条件规划，不保证检验功效，也不是三点二四年后必然证明。

### 进阶9 — 夏普精度

在基本独立同分布、低夏普近似下，以年计标准误约1/√Y。对真实年夏普0.3，令0.3√Y=2，得Y=(2/0.3)²=44.4444年。这是期望信号达到两个近似标准误，不是95%检验功效计算。高阶矩、自相关、变化风险、估计器与选择均会改变它。五年的近似误差0.4472已大于0.3，尚未考虑这些复杂因素。

### 进阶10 — 小成本算术

指定d=0.01，渐近区间u=(3d)^(1/3)=0.3107233。保留的无摩擦速率近似1−(3d)^(2/3)/2=0.9517255，即95.17%。原有界优化器给u≈0.3129916，κ=s=1时速率0.7598024；除以无摩擦极限√(2/π)=0.7978846得约0.95227。这是渐近预测与数值近似的比较，不是有限成本精确等式，也不是市场证据。

### 资格11 — 首达、更新与唯一最优

采用上述正常数OU模型，从零空仓开始，m>0。每个周期先到±m之一，再回零。强马尔可夫性和对称性使完整周期时长独立同分布；正再生OU对有限区间有有限的这些期望。每周期固定报酬m−c，更新报酬定理给长期完成周期利润率R=(m−c)/(E₀τ_m+E₋ₘT₀)。如要定义包括未完成周期浮盈亏的财富，还须明确其现金与记账；此式针对更新报酬。

首达期望f(x)在继续区间满足(σ²/2)f″−κxf′=−1，目标边界f=0。乘exp(−κx²/σ²)得
(exp(−κx²/σ²)f′)′=−(2/σ²)exp(−κx²/σ²)。从x<0到零时，在自然左边界排除爆炸齐次解，采用有界斜率解，可得
f′(y)=−(2/σ²)exp(κy²/σ²)∫₋∞ʸexp(−κz²/σ²)dz。
从−m积分到零并用f(0)=0，得到
E₋ₘT₀=(2/σ²)∫₋ₘ⁰exp(κy²/σ²)∫₋∞ʸexp(−κz²/σ²)dzdy。
从零退出(−m,m)时f为偶函数，f′(0)=0；同一微分方程从零积分，内积分下限变零，再用f(m)=0，得到
E₀τ_m=(2/σ²)∫₀ᵐexp(κy²/σ²)∫₀ʸexp(−κz²/σ²)dzdy。

设x=sz、τ=κt，尺度过程为dZ=−Zdτ+√2dB，生成元∂²_z−z∂_z；此处二阶项前不是1/2。实际时间按1/κ缩放。将负向积分反射后与正向积分相加，内积分的变量部分抵消，剩κE[周期]=a∫₀ᵘexp(z²/2)dz=aI(u)。因此R=(κs/a)(u−d)/I(u)。

在u>d上，R导数符号等于I(u)−(u−d)exp(u²/2)的符号。定义H(u)=u−exp(−u²/2)I(u)，最优条件是H(u)=d。H(0)=0，且H′(u)=u exp(−u²/2)I(u)>0；由exp(−u²/2)I(u)∼1/u，H趋无穷。因此正d恰有一个解；因H(u)<u，解大于d。解前R增加、解后减少，u趋无穷时速率趋零，故为此规则族唯一全局最大值。无量纲最优区间只依赖d。

### 资格12 — 无摩擦与立方根

用u=m/s展开κ乘期望时间。令a=√(π/2)，被积式exp(y²/2)∫₋∞ʸexp(−z²/2)dz=a+y+ay²/2+y³/3+ay⁴/8+… 。在[−u,0]积分得
κE₋ₘT₀=au−u²/2+au³/6−u⁴/12+au⁵/40+O(u⁶)。等待积分给
κE₀τ_m=u²/2+u⁴/12+O(u⁶)。偶次项抵消，总和为aI(u)=a(u+u³/6+u⁵/40+…)。
零成本时R=(κs/a)u/I(u)趋κs/a=σ√(κ/π)。u>0时I(u)>u，所有正区间速率都严格小于该值，因此这是上确界而非可达到的正区间最优值。

对正小d，精确一阶条件d=H(u)。级数相乘得exp(−u²/2)I(u)=u−u³/3+u⁵/15+O(u⁷)，故d=u³/3−u⁵/15+O(u⁷)。唯一根满足u*³=3d+O(d^(5/3))，即u*∼(3d)^(1/3)。

相对无摩擦速率为(u−d)/I(u)=(1−d/u)/(1+u²/6+O(u⁴))。最优点上d/u=u²/3+O(u⁴)，所以比值为1−u²/2+O(u⁴)=1−½(3d)^(2/3)+o(d^(2/3))。指数与二次风险下的持仓区间相似，但此处来自OU周期时间与固定更新报酬，不能据此声称通用成本定理。

## 样本边界修正与构建

令μ为全T样本均值、X_t=r_t−μ、H=I−11ᵀ/N，滞后协方差Γ̂使用T−k对。代入总体式的总项为−tr(Γ̂H)/N−μᵀHμ/N。实际利润展开后还多
δ=−μᵀH(平均X_now+平均X_lag)/N。完整数组X均值零，不代表两个滞后端点子数组均值零，故不能声称样本最后一位必然相等。总体平稳矩假设去掉期望交叉项，并不识别因果。

本次普通原计算已各执行一次，不要无参数运行compute，因为它还包含排除的实验；不刷新、不重试。构建使用已有核验缓存：`python tools/build.py quant33 --lang en`或`--lang zh`。纯数学检验为`tests/test_quant_house.py::test_statarb_ou_band_and_decomposition`，本次已记录。双语最终视觉回执必须绑定当前源码；抽样CPU语音检查、实际配音开篇与整片连续听审是不同证据。引文包括Vidyamurthy、Pole、Chan、Pedersen、Leung–Li及上述论文；公司历史属于公开报道。这是方法教育。

*Review log of the earlier QA passes on this part: [`docs/qa/quant/part33.md`](../../../docs/qa/quant/part33.md).*
