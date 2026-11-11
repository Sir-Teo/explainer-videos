# Quant, Built — Part 16: Computing Prices

This part studies numerical prices, sensitivities and exercise policies on synthetic textbook contracts. It distinguishes sampling uncertainty, discretization and truncation bias, numerical-reference error, and model assumptions. An error bar or agreement between two implementations does not certify total pricing accuracy.

The 22 scenes contain an opening, 19 numbered chapters, a research chapter and a closing exercise set. The current English narration estimate is about 66 minutes; rendered duration includes animation and pauses. Both narration languages follow the same scientific qualifications.

## Scope and reproducibility

The existing [compute driver](compute.py) and House numerical algorithms are unchanged in this polish. All 37 original Part 16 cache items were restored through their ordinary fixed-seed commands. The referenced Part 17 stopping result was also restored normally. No market data, new market-strategy trials, cache refreshes or sealed holdouts were used. Part 16's historical trial counter remains **312**, and the series counter remains **23,562**.

Examples include Black–Scholes calls and puts, discretely monitored Asian options, the Heston model with initial and long-run variance 0.04, mean reversion 1.5, volatility of variance 0.5 and correlation −0.7, and a five-asset Bermudan max-call. Different examples use different rates and dividends; the opening Heston comparison uses zero rates and zero dividends.

These are CPU experiments with varying configurations. In particular, the parallel workload uses process pools and the Part 17 stopping reference uses two training threads. Timings depend on implementation, repetition policy, workload, host and container quota. Published bank examples and quantum resource estimates are external claims with their own scope.

The completed source pass preserves full saved display ranges. Some panels intentionally select observations: the American path fan shows the first 150 saved paths, and each date's regression panel shows the first 300 saved in-the-money observations. The nested-path illustration selects a positive-payoff example from up to 40 candidates. Neither selection is a representative performance estimate. ADI surfaces are explicitly shown as separately rescaled shapes with actual ranges printed. The finite-difference instability plot uses a signed logarithmic vertical coordinate. The Chebyshev error surface retains the cache's declared censoring at 10⁻¹².

## Chapters and qualifications

| Scene | Subject and interpretation |
| --- | --- |
| Opening | Separate recorded timings; Monte Carlo height is one sampling standard error, while grid and Fourier heights are absolute differences from a COS reference. These are different metrics. The history retains all 13 events. |
| 1. Monte Carlo | Pointwise asymptotic intervals, finite-replicate coverage, centred Berry–Esseen moment, and variance times work. Coverage at many running sample sizes is not simultaneous coverage. |
| 2. Paths | Inverse normal, Box–Muller, covariance factors and a power-of-two Brownian bridge. Philox uses path-indexed keys `[2026, j]`; the reproducibility demonstration does not prove independent streams or cross-platform identity. |
| 3. Controls and strata | Fixed population coefficient versus a coefficient estimated from the same sample; antithetic comparisons at equal payoff evaluations; common histogram bins and denominators; empirical stratification and Latin-hypercube ratios. Moment matching can bias nonlinear estimates. |
| 4. Importance sampling | Support and moment conditions; full variance-ratio curve; a best tested shift on a finite grid rather than an exact optimum. Cross-entropy optimizes a divergence and uses the strike through the payoff. Freeze a learned proposal before independent production evaluation. |
| 5. QMC | Aligned dyadic elementary boxes, rather than arbitrary equal-area shapes. Koksma–Hlawka requires finite Hardy–Krause variation. Measured L2-star discrepancy differs from its supremum counterpart. Ten-scramble normal intervals are approximate. Finite-bit scrambling can produce zero; the normal transform clamps endpoints at 10⁻¹². |
| 6. Bridge and PCA | Different factors preserve the joint Gaussian law, rather than individual paths. Reported coordinate shares concern a linear Brownian average. PCA maximizes discrete path energy, not variance capture for every payoff. Replicate standard deviation excludes bias. |
| 7. MLMC | Telescoping, independent-level MSE decomposition, variance/work allocation and the full conditional complexity theorem. Last-correction bias is an adaptive proxy. The standard comparison estimates step work, rather than measuring matched total RMSE or seconds. |
| 8. LSM | Simulated paths and 25 exercise dates: a Bermudan contract. A fixed policy's expectation is a lower bound; a noisy evaluation and an in-sample mean need not be. Polynomial sweeps reuse evaluation paths; seed bands are minima and maxima. |
| 9. Duality | Finite-grid optional stopping; ideal Doob martingale versus noisy nested approximation; conditional Jensen comparison. Both reported point estimates have Monte Carlo error. The fresh policy evaluation replaces the in-sample lower label. |
| 10. Greeks | Thirty-seed RMSE, smoothness conditions for central bumps, regularity for common numbers, and differentiation-under-expectation conditions. A digital's derivative is undefined at its strike; the Dirac derivative is distributional. Score identities need regular density/support and direct terms when the payoff explicitly depends on the parameter. |
| 11. AAD | A scalar-output gradient in work proportional to the executed tape, with memory costs. One-path derivatives require pathwise conditions before becoming expectation Greeks. The derivative with respect to maturity is not calendar theta. Element-count proxies are not literal FLOPs. |
| 12. Finite differences | The diffusion-only number σ²Smax²Δt/ΔS² has threshold one; the heat-equation number aΔt/Δx² has threshold one half. Drift, reaction and boundaries need further checks. Signed-log plots retain the unstable high-stock region. |
| 13. LCP | Pure alternating mode and weak CN damping; two implicit half steps have a different factor from one full step. Full gamma ranges, conditional PSOR convergence, finite penalty error and update size versus residual. |
| 14. ADI | Directional tridiagonal solves, mixed terms and conditional time order. Separately normalized price and derivative shapes show actual ranges. The variance-state partial derivative is not standard volatility vega. COS is a numerical reference. |
| 15. Fourier | Relative log strike k=log(K/S₀), normalized call c=C/S₀ and a log-return characteristic function. Half-line inversion takes a real part. The Lewis formula shown assumes zero rates/dividends and uses exp(−iuk). Saved absolute-log-strike transform arrays are changed exactly to these coordinates. |
| 16. COS | A high-term numerical density reference, finite density errors, L2 expansion conditions, tail/coefficient/series/roundoff errors and conditional exponential convergence. At L=40 the discrepancy is zero by construction against the same reference. COS recursion extensions can handle some barriers and Bermudans. |
| 17. Industry | Dated primary accounts, scoped SIMM/FRTB statements, distinct timing workloads, and actual selected test tolerances. No invented nightly automation or model-validation certificate. |
| 18. Quantum | Ideal binomial measurements for toy amplitude 0.3; no financial circuit was built. Oracle-query counts differ from runtime. Likelihood curves are maximum-normalized; percentile bands are not confidence intervals. Separate logical qubits, T-count, T-depth and assumed T-layer clocks. |
| 19. Research selection | Chebyshev maximum over 200 fixed test sites, not a box supremum. Build-time break-even includes the actual build. The RQMC plateau is consistent with a 30-bit grid bias, not double precision. Theorems require their analytic and repetition-growth conditions. |
| Research | A single Gram-diagonal RMS diagnostic is not a universal regression path budget. Unconditional moments differ from the in-the-money design. Exercise-loss bounds need policy occupancy, uniform continuation error and a margin condition. A worked halving-error answer follows the pause. |
| Closing | Consistent recap, four desk questions and ten exercises with the assumptions below. |

## Selected restored results

These values identify the saved experiment. They are not promises for other products or machines.

| Quantity | Saved result and limit |
| --- | --- |
| Plain-call payoff standard deviation | 14.7242; normal-approximation sampling half-width ±0.01 suggests 8.329 million iid paths. Bias is separate. |
| Empirical interval coverage | 944 of 1,000 repetitions; this coverage estimate itself has sampling uncertainty. |
| Geometric Asian control | Mean empirical variance ratio 1,299.7 across five seeds; stock control 2.836. Fitting and setup affect comparisons. |
| Normal-shift importance sampling | Strike-centred shift ≈2.200; best tested grid shift 2.75, empirical ratio 133.0. Cross-entropy is a different optimization problem. |
| 25-date policy evaluation | 6.070952 ±0.011418, one estimated s.e., on 400,000 fresh paths. In-sample mean 6.060957 is not the lower expectation estimate. |
| Nested upper expectation estimate | 6.414419 ±0.056730 with 50 inner paths; 6.075002 ±0.009047 with 1,600. Each uses 400 outer paths; nested bias is additional. |
| Same-date tree reference | 6.066965 at 5,000 steps; finite tree error remains. Point estimates need not enclose it. |
| Five-asset policies | LSM with 200,000 fitting paths: 26.103290 ±0.013914 on two million evaluation paths. Part 17 network: 26.108393 ±0.019744 on one million. Evaluation errors do not measure training uncertainty or prove equivalence. |
| AAD at 128 inputs | 0.7035 NumPy-price-baseline times versus 259.67 for central bumps. Different implemented computations and timing effects explain why a measured ratio may be below one; a gradient is not free. |
| Parallel timing scope | Loop: 100,000 timed then ×10; NumPy: one million pre-generated values; pool: draw plus price. Best-of counts are 2, 5 and 3 respectively. Recorded host count 5 logical CPUs; container quota 4 CPU equivalents. |
| Chebyshev | 32×32 labels; sampled maximum 3.7051×10⁻⁶ at 200 sites. Build 0.316876 s, fixed query 0.108865 ms versus COS 0.286893 ms; break-even ≈1,780 queries if these timings persist. |
| RQMC median | Fixed 11 repetitions, 30 experiments and 30-bit Sobol grids. Leading uniform-grid bias for ∫exp(u)du is approximately −8.0014×10⁻¹⁰. |

## Ten worked solutions — English

1. **A fixed control coefficient.** For iid pairs with finite second moments and Var(C)>0,
   Var(Ȳ−b(C̄−EC)) = [Var(Y)−2bCov(Y,C)+b²Var(C)]/n. Completing the square gives b*=Cov(Y,C)/Var(C), and minimum Var(Y)(1−ρ²)/n. This identity concerns a deterministic population coefficient. Same-sample fitting can bias the estimator; a frozen independent pilot preserves conditional unbiasedness.

2. **Normal-shift importance sampling.** With p=N(0,1), qθ=N(θ,1), p(z)/qθ(z)=exp(−θz+θ²/2). Evaluate under qθ and weight every payoff. For zero dividend yield, log ST=log S₀+(r−σ²/2)T+σ√T z, so the strike threshold is zK=[log(K/S₀)−(r−σ²/2)T]/(σ√T). Setting θ=zK centres the proposal on the threshold. It need not minimize variance, and cross-entropy need not find that minimum either. Support and required moments must hold.

3. **Finite-grid dual upper expectation.** Let h be integrable discounted rewards on a finite horizon and M an admissible integrable martingale with M₀=0. Optional stopping gives EMτ=0 for every admissible stopping time. Thus Ehτ=E(hτ−Mτ)≤E maxᵢ(hᵢ−Mᵢ). Take the supremum over τ. The maximum must be integrable. A noisy nested process is not automatically a martingale; its expected-maximum argument uses the separate conditional-unbiasedness/Jensen construction. Finite Monte Carlo estimates are not sure bounds.

4. **Heat-equation stability.** For u_t=a u_xx, the explicit centred update has amplification g=1−4λsin²(ξ/2), λ=aΔt/Δx². For a≥0, |g|≤1 at all frequencies exactly when 0≤λ≤1/2, under the periodic/infinite-grid Fourier setup. In Black–Scholes, a=σ²S²/2, so its diffusion-only criterion is σ²Smax²Δt/ΔS²≤1. A full pricing scheme must also handle drift, reaction and boundaries.

5. **Reverse-tape work.** For scalar output y and differentiable elementary operations, seed ȳ=1. Each edge i→j contributes v̄ⱼ ∂vⱼ/∂vᵢ to v̄ᵢ. Visiting each edge once costs O(W) for tape work W under the operation model, with storage or recomputation costs. Computing all n input directions by separate forward sweeps costs O(nW). The tape's own W can grow with n; there is no universal wall-clock factor, and many output components can require more reverse sweeps.

6. **Hybrid call gamma.** In Black–Scholes with S₀,σ,T>0, let D=e^(−rT)(ST/S₀)1{ST>K}, the pathwise delta integrand. For the lognormal terminal density, the spot score is Z/(S₀σ√T). D also has explicit dependence 1/S₀ at fixed ST. Differentiating its expectation by the score method therefore gives
   Γ=E[e^(−rT)ST/S₀² ·1{ST>K}·(Z/(σ√T)−1)].
   The −1 term is essential. Density differentiation and integrability conditions justify the identity. A sample average estimates gamma with its own sampling variance; a discontinuous integrand should not be differentiated naively pathwise again.

7. **MLMC when β=γ.** Assume the theorem's positive bias, correction-variance and work exponents, independent level estimates, α≥min(β,γ)/2 and appropriate integer-allocation/regularity conditions. With bias O(M^(−αL)), L=O(log ε⁻¹). Each √(VₗCₗ)=O(1) when β=γ, so the sum is O(L+1). Optimal continuous allocation gives cost proportional to ε⁻²(Σ√(VₗCₗ))², hence O(ε⁻²(log ε)²), including the theorem's allocation treatment. This does not certify an adaptive bias proxy.

8. **FFT spacing.** Set uⱼ=jη and kₘ=−b+mλ. In exp(−iuⱼkₘ), exp(ijηb) is a pre-factor, while the j,m kernel is exp(−ijmηλ). Matching the N-point FFT kernel exp(−2πijm/N) requires ηλ=2π/N. At fixed η, doubling N halves strike spacing and extends frequency cutoff. At fixed N, changing η trades spacing, truncation and aliasing effects.

9. **Gram diagonal and lognormal moments.** For iid states and finite Eψₖ⁴, Ĝₖₖ=N⁻¹Σψₖ(Xₙ)² has variance [Eψₖ⁴−(Eψₖ²)²]/N. If Eψₖ²=1 its standard deviation is √[(Eψₖ⁴−1)/N]. For S=exp(σW_t−σ²t/2), ESᵖ=exp[(p²−p)σ²t/2]. Therefore, for ψₖ=Sᵏ/√ES²ᵏ, Eψₖ⁴=ES⁴ᵏ/(ES²ᵏ)²=exp(4σ²tk²). This single-diagonal diagnostic does not control the full inverse Gram matrix or price error, and the unconditional law differs from in-the-money regression sampling.

10. **One-date margin bound.** Given true continuation C, payoff h and fitted continuation Ĉ, a wrong decision loses Δ=|C−h| and requires Δ≤|C−Ĉ|. If |C−Ĉ|≤ε uniformly, expected loss ≤E[Δ1{0<Δ≤ε}]≤εP(0<Δ≤ε). A margin bound P(0<Δ≤u)≤Auᵅ gives loss ≤Aε^(1+α). Zero-gap atoms incur no loss and need not be excluded from the state distribution. Linear margin α=1 gives a quadratic bound with units and constants. Halving ε quarters this bound, not necessarily the realised loss. In multiple dates, use the Snell continuation and the policy-occupancy identity; dropping occupancy gives a sum of per-date bounds, rather than a naive equality over every wrong decision.

## 中文说明与十题解答

本部分在合成教材合约上研究数值定价、敏感度和行权策略，区分抽样不确定性、离散与截断偏差、数值参考误差和模型假设。标准误或两个实现相符，都不能认证总精度。二十二个场景包含开场、十九章、研究章和结尾。当前英文旁白估计约六十六分钟，成片还包含动画和停顿。

本轮没有修改计算驱动或定价引擎算法。三十七项原始缓存及第十七部分停止参考按原有固定种子正常恢复，没有刷新缓存、读取密封保留集或新增市场策略试验。本部分累计计数为312，全系列为23,562。处理器配置因实验而异，并行案例使用多个进程，停止参考使用两个训练线程。

图中保留保存数据的完整显示范围。部分图明确抽取子集：行权图显示前150条路径，各日期回归显示前300个保存价内观察值；嵌套路径特意选取有正支付的例子。它们不代表性能抽样。二维方向分裂曲面分别缩放形状，并显示实际数值范围；不稳定差分图采用带符号对数；插值曲面的原缓存明确在10⁻¹²处截尾。

研究章的四阶矩公式只诊断单个格拉姆对角项，不是通用路径预算。价内设计分布、矩阵维度、非对角误差和条件数都重要。继续价值的一致误差与边界概率条件可给出行权损失上界，但不能把百分之二误差直接变成百分之零点零四价格损失。研究暂停题随后给出“误差减半，上界缩为四分之一”的条件解答。

1. **固定控制系数。** 对独立同分布样本对且二阶矩有限，控制估计方差等于[Var(Y)−2bCov(Y,C)+b²Var(C)]/n。控制方差为正时，配方得到b*=Cov(Y,C)/Var(C)，最小方差为Var(Y)(1−ρ²)/n。它针对固定总体系数。同样本估计系数可能有偏；独立试验拟合后固定系数，可保持条件无偏。

2. **正态平移。** 原密度为标准正态，提议密度均值为θ时，似然比为exp(−θz+θ²/2)。在提议分布下抽样并加权。零股息下，支付开始的正态阈值为[log(K/S₀)−(r−σ²/2)T]/(σ√T)。把θ设为该阈值，使提议中心对准支付区域，但未必方差最优。交叉熵最小化另一种目标，也未必找到方差最优值；还需支撑和可积条件。

3. **有限网格对偶。** 支付已折现，期限有限，鞅可积且初值为零。可选停止给出EMτ=0，所以Ehτ=E(hτ−Mτ)≤E maxᵢ(hᵢ−Mᵢ)，再对策略取上确界。最大值也须可积。含噪嵌套过程不自动为鞅；相应上界期望依赖另外的条件无偏和詹森论证。有限蒙特卡洛点估计不是必然上界。

4. **热方程稳定性。** 显式中心格式增长因子为1−4λsin²(ξ/2)，λ=aΔt/Δx²。在周期或无限网格傅里叶分析下，非负扩散系数的全频稳定条件是λ≤1/2。布莱克斯科尔斯扩散系数为σ²S²/2，因此纯扩散条件为σ²Smax²Δt/ΔS²≤1。漂移、反应和边界仍需检查。

5. **反向计算带。** 标量输出伴随量从一开始，每条边把下游伴随量乘局部导数，累加到输入。通常基本运算成本模型下，每条边访问一次，工作量为计算带工作量的同阶，还需存储或重计算。分别传播全部n个输入方向需要n次前向扫描。计算带本身可随输入数增大，不存在通用墙钟倍数；多个输出可能需要更多反向扫描。

6. **混合伽马。** 现价、波动率和期限为正时，看涨路径德尔塔被积函数为D=exp(−rT)(ST/S₀)1{ST>K}。对终端对数正态密度求现价导数，得分为Z/(S₀σ√T)。固定ST时，D还显式含1/S₀，因此伽马为E[exp(−rT)ST/S₀²·1{ST>K}·(Z/(σ√T)−1)]。减一项不可遗漏。恒等式需要密度微分和可积条件；样本均值仍有抽样方差，不能再次直接对指标函数做朴素路径微分。

7. **多层复杂度。** 假设定理的正偏差、方差和成本指数，各层独立，并满足阿尔法至少为贝塔与伽马较小值一半等正则和整数分配条件。偏差按M的负阿尔法L次方下降，所以层数为误差倒数对数阶。贝塔等于伽马时，每项方差成本乘积的平方根有界，求和为层数阶。最优连续分配成本与误差负二次方乘该和的平方成比例，得到误差负二次方乘对数平方的复杂度。它不能认证自适应偏差代理量。

8. **快速傅里叶步长。** 设频率为jη，对数执行价为−b+mλ。反演指数中，与j、m同时相关的核为exp(−ijmηλ)。要匹配N点快速傅里叶核exp(−2πijm/N)，必须ηλ=2π/N。固定η把N翻倍，执行价间距减半并扩展频率范围；固定N改变η则要权衡步长、截断和混叠。

9. **格拉姆矩与对数正态矩。** 独立同分布状态且四阶矩有限时，样本对角项方差为[Eψ⁴−(Eψ²)²]/N。二阶矩归一为一时，标准差为四阶矩减一除路径数后开平方。对S=exp(σW_t−σ²t/2)，p阶矩为exp[(p²−p)σ²t/2]。代入归一化单项式，四阶矩为exp(4σ²tk²)。这只是单个对角项诊断，不能控制完整逆矩阵或价格误差；无条件分布也不同于价内回归分布。

10. **单日期边界概率界。** 真实继续价值与支付的差距为Δ。错误决策要求Δ不超过继续价值估计误差；零差距不产生损失。若一致误差不超过ε，则期望损失至多为εP(0<Δ≤ε)。若概率不超过Aε的阿尔法次方，损失上界就是Aε的一加阿尔法次方。线性边界条件产生带单位和常数的二次上界；误差减半使这个上界变为四分之一，不保证实际损失同比变化。多日期问题必须使用最优斯内尔继续价值和策略访问权重；去掉访问权重只能给出逐日期上界之和，不能写成朴素的全日期错误决策等式。

## Primary references and dated claims

- Glasserman, *Monte Carlo Methods in Financial Engineering* (2003); Savine, *Modern Computational Finance* (2018); Andersen and Piterbarg, *Interest Rate Modeling*, volume I; Duffy, *Finite Difference Methods in Financial Engineering*; Oosterlee and Grzelak, *Mathematical Modeling and Computation in Finance*.
- [Glasserman and Yu, “Number of Paths versus Number of Basis Functions in American Option Pricing” (2004)](https://business.columbia.edu/sites/default/files-efs/pubfiles/1372/Glasserman_number_of_paths.pdf), DOI 10.1214/105051604000000846. Worst-case polynomial settings, not a universal per-option budget.
- [Pan and Owen, “Super-polynomial accuracy of one dimensional randomized nets using the median of means”](https://arxiv.org/abs/2111.12676), v3 July 2022, published 2023. The one-dimensional theorem assumes derivative bounds of the form |f⁽ᵏ⁾|≤Aαᵏk! with α<2, and a median of 2k−1 replicates with k=Ω(m) for n=2ᵐ points. Eleven fixed replicates do not satisfy that growing-repetition asymptotic condition.
- [Junike, “On the number of terms in the COS method for European option pricing” (2024)](https://link.springer.com/article/10.1007/s00211-024-01402-1). Error control is conditional on its regularity and bounds.
- [Bayer, Pelizzari and Schoenmakers, “Primal and dual optimal stopping with signatures”](https://arxiv.org/abs/2312.03444v2), revised February 2025.
- [Glau, Kressner and Statti, “Low-Rank Tensor Approximation for Chebyshev Interpolation in Parametric Option Pricing” (2020)](https://doi.org/10.1137/19M1244172); [author preprint](https://arxiv.org/abs/1902.04367).
- [Chakrabarti et al., “A Threshold for Quantum Advantage in Derivative Pricing” (2021)](https://quantum-journal.org/papers/q-2021-06-01-463/). Autocallable Table 1 case: three assets, 20 steps, target error 0.002, about 8,000 logical qubits, T-count 1.2×10¹⁰ and T-depth 5.4×10⁷. TARF is a different case. These are resource estimates, not measured execution.
- [Stamatopoulos and Zeng, “Derivative Pricing using Quantum Signal Processing” (2024)](https://quantum-journal.org/papers/q-2024-04-30-1322/). Stated QSP case: about 4,700 logical qubits, total T-count 2.4×10⁹, T-depth 4.5×10⁷; 45 MHz sequential T-layer rate to match an assumed classical second. The 16-fold count and four-fold qubit improvements compare this paper's arithmetic reference, not the 2021 headline. Amplitude error 0.001 and confidence 0.68 belong to that resource construction.
- [Dalzell et al., “Quantum algorithms: A survey of applications and end-to-end complexities”](https://arxiv.org/abs/2310.03011v2), revised August 2025; Cambridge book edition April 2025.
- [Risk.net, Danske Bank's 2015 in-house system award](https://www.risk.net/derivatives/2387869/house-system-year-danske-bank). Reported firm episode, not a local benchmark.
- [University REF case study on Maxeler/JPMorgan](https://impact.ref.ac.uk/casestudies/CaseStudy.aspx?Id=42142), citing Weston et al. (2012), DOI 10.1002/cpe.1778. The eight-hour to under-four-minute example is specific to the described computation.
- [Official STAC-A2 report](https://docs.stacresearch.com/news/2014/09/08/stac-reports-intels-new-haswell-server-chip-and-without-xeon-phi-stac-a2). Multi-asset, path-dependent Heston Greeks with early exercise; results concern specified implementations and include STAC-audited work.
- [OCC margin methodology](https://www.theocc.com/risk-management/margin-methodology). STANS is a full-portfolio Monte Carlo system introduced in 2006.
- [ISDA SIMM 2.9+2606 publication](https://www.isda.org/?p=1283022). Methodology publication is distinct from a firm's implementation or jurisdictional applicability. [Basel market-risk standard, MAR20.4](https://www.bis.org/publications/201901-standards-minimum-capital-requirements-market-risk.pdf): standardized capital sums its sensitivities-based requirement, default-risk charge and residual-risk add-on. Local applicability and effective dates require the applicable jurisdictional rules.

## Local verification

Ten existing `test_engine` tests passed during this review. They check selected fixed examples with their own tolerances, including stochastic allowances, covariance, stopping, adjoint, finite-difference, Fourier and toy amplitude/interpolation cases. Passing them does not establish every function's correctness, financial model adequacy or a bank's production controls.

The visual pass is complete: 44 current English/Chinese narration-beat renders and 22 English motion renders were inspected, with zero unresolved warnings. The [sequential QA log](../../../docs/qa/quantitative-finance-polish.md) and [artifact-bound evidence](../../../docs/qa/quant16-polish-evidence.json) record the checks, 13 sampled CPU speech reports and the actual narrated opening. The silent preview runs 75:30, including animation and pauses. Full continuous production-voice listening remains a separate pending pass.

From the repository root, with the Manim environment active and original caches available:

```bash
python tools/qa_series.py quant16 --cached-only --resume --timeout 1800
python tools/qa_series.py quant16 --lang zh --cached-only --resume --timeout 1800
python tools/qa_series.py quant16 --motion --cached-only --resume --timeout 1800
python tools/lecture_length.py quant16 --floor 50
```
