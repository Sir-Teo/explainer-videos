# Quant, Built · Part 31: Risk Models, Costs and Trading Through Time

Part 31 connects forecasts, covariance assumptions, execution costs and decisions through time. It is a retrospective methods lesson with labelled mathematical illustrations. Public-data calculations do not establish an executable point-in-time investment record or future profitability.

## Data and interpretation

Nine unchanged ordinary originals were restored once: `model`, `vasicek`, `law`, `costs`, `gp`, `combine`, `attribution`, `quake`, and `theory`. There were nine wrapper invocations, no failed attempts or retries, no new market trials and no registry changes. The strategy experiment is excluded before counted/cache access; no sealed strategy cache, payload, outcome or diagnostic is used in this review. The existing cumulative registration metadata is 23,535 through Part 31, versus 23,562 globally; ten existing charges belong to this part. Counts describe research history, not independent performance evidence.

The Binance examples use Part 29's frozen public USDT-pair grid and its 2018–2020 research mask. The inherited reader loads public 2017–2025 daily arrays before masking. Those public raw arrays are distinct from sealed strategy payloads. The frozen late-2026 listing is retrospective, with survivorship, listing availability, asset classification and other point-in-time limitations. Eligibility requires 60 days of history and median quote volume of at least 250,000 USDT. The factor model has a median 34 eligible coins per day; model warm-up and complete-case selection alter the observations available to individual calculations. Dollar labels assume USDT parity.

The quake replay uses Kenneth French's 49 daily US industry portfolios through 2020. It is an industry proxy, not individual stock execution, actual fund holdings or the original Khandani–Lo experiment. Missing industry returns are filled by zero. Its arithmetic P&L excludes fees, borrowing and market impact.

Quoted study findings, reported historical fund losses, saved research calculations, fixed simulations and chosen arithmetic inputs have separate scopes. Sharpe annualisation uses the stated independent-period convention; no selection-adjusted, dependence-robust confidence interval is estimated here. Full continuous production listening and pronunciation review remain pending separately from visual QA.

## Chapters and scientific boundaries

1. **Fundamental law.** The conditional diagonal-risk identity needs calibrated forecasts, fixed score norm and an appropriate risk metric. Realised unconditional information ratios require more assumptions. The displayed long-only transfer coefficient is a fixed Gaussian-score heuristic relative to equal weights, not a universal loss of skill. The equicorrelation breadth formula concerns a mean-equivalent count under equal variances, equal weights and common expected payoff.
2. **Factor risk models.** `X F Xᵀ + Δ` assumes factor–residual orthogonality and diagonal residual covariance. The 4,830-versus-4,501,500 parameter comparison conditions on X; estimated beta and volatility exposures still carry uncertainty. The House uses square-root-quote-volume WLS weights and a fixed 10⁻⁶ ridge. Exact unit-exposure mimicking portfolios require the unregularised full-rank case. EWMA squares and outer products are uncentred second moments. Daily date coordinates retain day-level spacing, including late-2017 warm-up. Factor paths are arithmetic sums, not wealth; displayed t statistics use an IID reference without serial or selection adjustment.
3. **Calibration and betas.** The median forecast factor fraction is a median across dates of within-date median fractions, about 71.7%; it is not realised R². All four saved bias statistics fall outside the approximate IID Gaussian 95% reference half-width √(2/652)≈.0554. Actual fat tails, dependence, conditional means and adaptive holdings limit that reference; the discrepancies identify no unique cause. Specific-risk shrinkage is a fixed .3 toward the overall cross-sectional mean. Vasicek's empirical prior variance is floored at 10⁻⁸. The 12 beta comparisons use consecutive 60-calendar-day blocks and require eligibility in both, selecting survivors; their targets are noisy future estimated betas. Saved MSE is .04960 raw versus .04066 shrunk. Dimson's joint lead/lag regression differs from Scholes–Williams' separate regressions and market-autocorrelation adjustment. Leads are ex post estimation devices.
4. **Execution costs.** Distinguish average execution shortfall from terminal peak impact. For currency notionals Q,V, average cost fraction `Y_avg σ√(Q/V)` gives money cost `Q×fraction`. Integrating a particular square-root peak-impact path instead introduces a 2/3 factor. The worked example uses separate pooled asset-date medians of ADV and volatility, not one actual median coin. The chosen average-cost coefficient is one. Saved size scenarios use fixed targets, target differences rather than drift-adjusted trades, and five-basis-point fees; financing, borrow, spread, delay and execution are incomplete. Large-participation extrapolation is uncertain. Net Sharpe need not scale as √A because its denominator changes too.
5. **Inaction and dynamic trading.** Smooth `|Δh|^(3/2)` impact has derivative zero at zero and generically creates no exact no-trade band. A separate proportional cost κᵢ|Δhᵢ| yields the whole-book condition `|αᵢ−γ(Σh₀)ᵢ|≤κᵢ` in the unconstrained fixed concave problem. Classical κ^(1/3) band and κ^(2/3) utility-loss asymptotics need their continuous-diffusion, interior-target, nondegeneracy and small-cost assumptions. They are a different model.
6. **Gârleanu–Pedersen.** Use the stated Bellman timing: operating return/risk and continuation are discounted by d=1−ρ, while current trade cost is paid now. Known fixed positive-definite covariance/cost, linear conditional dynamics, finite second moments, unconstrained holdings and a well-posed horizon underlie the Riccati policy. The √(γ/λ) rate approximation needs zero or negligible discount, roughly γ≪λ≪γ/ρ². At fixed positive ρ as λ→∞ the rate is γ(1−ρ)/(ρλ). General cost matrices create coupled risk/liquidity modes. The empirical φ is one minus average cross-sectional Pearson score correlation, a geometric-persistence proxy. Coefficients, persistence and volatility scaling reuse research data. Both aim multipliers are at most one for positive decay; slow signals are favoured relatively, not amplified above raw forecasts. The zero-cost row uses a numerical near-free limit. Value iteration checks algebra, not market optimality.
7. **Multi-period optimisation.** The unchanged fixed toy uses L-BFGS-B and smoothed three-halves impact. Its 1-, 5- and 40-period solves all converged; first positions are .08812, .26382 and .24069. Terminal holdings are free, not forced to zero. The complete 40-period path is shown with aligned forecast indexing. Different horizons have different objectives and boundary effects, not a universal ranking. Borrowing is a holding cost, not solely a trade-increment cost. A variance floor changes a risk input rather than defining a position constraint. Replanning does not correct an incorrect model. Recovery of GP requires matching costs, timing, discount and forecasts.
8. **Combination.** The population multiple-correlation formula uses finite-variance standardised Pearson objects, a positive-definite C and a feasible joint covariance; it does not accept measured rank ICs interchangeably. Ridge shrinks coefficients toward zero. With L¹ normalisation its large-penalty direction tends toward Xᵀy, not equal weights. The saved pooled raw-return squared-error fit has no intercept and zero-fills missing scores; it does not optimise average daily rank IC. Mining, multiple ridge choices and repeated 2020 validation are reused research. A winning marginal signal does not prove the others lack conditional information. The geometric horizon-IC formula is a weak-signal approximation and eventually decays as h⁻¹/² for positive decay. Separate signal books can still centrally net orders; coupled risk, costs and constraints generally distinguish separate and joint optima.
9. **Capacity and incentives.** √(2φ) is RMS change for a stationary matched unit-variance score pair, not directly portfolio turnover. Absolute-turnover scaling needs a fixed increment distribution, normalisation and universe. Four-ninths capacity and one-third net edge hold in the fixed positive-g,c profit model without other costs or a risk objective. The plot shows net/g and four times normalised profit, including its full negative tail. Berk–Green's ideal rational-flow equilibrium has zero expected risk-adjusted net alpha, not zero realised or total return. Fees capture rents after trading costs. The a/3 fee is specific to the known-skill square-root-cost extension. Observational fund findings do not identify a universal cause of closures.
10. **Quake.** The proxy uses `wᵢ=−(Rᵢ−R̄)/Σ|Rⱼ−R̄|`, giving zero net dollars and gross one when defined, not beta neutrality. Paths sum daily P&L. Reference daily SD uses January 2006–June 2007 and is not a confidence interval. The stylised factor-neutral risk example is separate from the replay; diagonal residual risk need not be small under leverage or concentration. The unwind account is a hypothesis. Comomentum is a proxy with sample associations, not a direct fund count or guaranteed predictor. The industry Sharpe does not identify a universal reversal premium or crash exposure.
11. **Attribution.** Multiplying a fitted return identity by aligned holdings gives exact model-relative accounting. Specific return is not automatically skill. The displayed Brinson-style selection term uses portfolio sector weights, combining selection and interaction. Factor-component variance divided by total variance is descriptive, can exceed one, and is not additive Euler attribution when component covariance matters. Timing uses sample covariance with divisor T; it establishes no repeatable skill. Euler volatility contributions need fixed PSD covariance and positive portfolio volatility; factor terms assume factor–residual orthogonality.
12. **Protocol and limits.** Specify data timing, universe, forecasts, risk, costs, constraints and selection before evaluation. Outcome-informed changes need honest new evaluation. The fixed example chooses α=(10⁻⁵,10⁻⁵), γ=1, σ²=(10⁻⁸,4×10⁻⁴), book=1. Unconstrained positions are (1000,.025); a 10⁻⁴ variance floor gives (.1,.025); a .05 absolute book cap gives (.05,.025); chosen ADV=(.5,.1) with .1 participation-based position cap gives (.05,.01). These are existing library functions on chosen arithmetic, not a calibrated rule, a market trial or a historical repair. Clipping is not a general constrained multi-asset optimum. Position bounds do not validate forecasts or establish profitability.

## Research: exact normalised-score identity

Let N≥2, Σzᵢ=0, Σzᵢ²=N and bounded latent ρ∈[−1,1]. Conditional noise has mean zero, unit variance and zero cross-asset covariance. Let μ=Eρ, s²=Varρ, with Eρ²=μ²+s²<1. For `rᵢ=ρzᵢ+√(1−ρ²)εᵢ` and `π=N⁻¹Σzᵢrᵢ`,

`Eπ=μ`, `Varπ=s²+(1−μ²−s²)/N`, and `IR=μ/√Varπ`.

The unchanged House helper omits `−s²/N` and is labelled approximate. The saved simulator clips Gaussian latent draws at ±.99; its input moments are pre-clipping, while the identity requires actual post-clipping moments. Measured finite-sample Pearson or rank IC is not latent ρ. Observed IC dispersion already includes cross-sectional sampling noise, so adding another noise term can double count. The empirical table is a heuristic comparison, not an exact plug-in correction.

For zero-sum weights, `π=N sd_cs(w) sd_cs(r) Corr_P(w,r)`, using population-divisor cross-sectional SDs. The scale changes with normalisation and universe. Spearman and Pearson differ even under Gaussian distributions. Pooled excess kurtosis can reflect heteroskedastic mixtures. The four saved empirical ratios change definitions on selected reused data; numerical proximity is neither a causal explanation nor an uncertainty interval. No HAC or selection-adjusted interval was estimated. Memory changes annual scaling; specified linear-quadratic models can still have Riccati solutions. Known finite μ,Σ retain the formal mean–variance solution even under heavy tails; robust estimation and realistic constraints are distinct difficulties.

## Six desk checks

1. Fixed latent toy μ=.05,s=.10,N=500 with independent months: benchmark .05√6000=3.873; exact annual IR `√12×.05/√(.01+.9875/500)=1.5828`.
2. Bias statistic1.30 means standardised-return SD is30% above one. AtT=504, the approximate IID Gaussian95% reference is1±√(2/504)=1±.0630. Dependence, tails and nonzero conditional means require further analysis.
3. A4% annual volatility forecast is not a loss bound; a10% weekly loss can reflect jumps, omitted covariance, leverage or changing risk.
4. Holding gross return and cost technology fixed, four times size doubles2% costs to4%;8% gross nets4%, before other costs.
5. Quadrupling λ roughly halves speed only in the negligible-discount regime. At fixed positive discount and extreme λ, speed scales as1/λ instead.
6. The fixed variance floor changes the risk input; the independent cap bounds positions. Neither establishes future profitability.

## Problems 1–6: complete solutions

**1. Hook.** Scores and latent moments satisfy the research model. Monthly variance is .10²+(1−.05²−.10²)/500=.011975, so monthly IR=.05/√.011975=.45691. Independent months give annual√12 times this,1.5828. The usual small-correlation constant-IC benchmark is.05√(500×12)=3.8730; the exact constant-IC toy also divides by√(1−.05²).

**2. Bias reference.** If zₜ are independent standard normals and b is their sample SD, `(T−1)b²` has χ²(T−1) law. The delta method gives SD(b)≈1/√[2(T−1)]; multiplying by1.96 gives approximate95% half-width .0618 atT=504, close to the shorthand√(2/T)=.0630. Thus1.30 lies outside either Gaussian reference. This is not an actual-data confidence statement without those assumptions.

**3. Vasicek.** Known Gaussian observation variance and known Gaussian prior variance are both .3²=.09. Posterior precision is2/.09 and precision-weighted mean is `(1.8/.09+1/.09)/(2/.09)=1.4`. Actual empirical Bayes estimates its prior and standard errors rather than knowing them.

**4. Size.** Assume fixed8% gross return and costs proportional to√A. Costs at400m are2%√(400/100)=4%; net8%−4%=4%. Financing and any other costs are excluded by the question.

**5. Capacity.** ForΠ=gA−cA^(3/2), g,c>0, break-evenA₀=(g/c)². SettingΠ′=g−(3/2)c√A=0 givesA*=(2g/3c)²=(4/9)A₀=400m. Π″=−3c/(4√A)<0. Net returnΠ/A atA* isg−2g/3=g/3 before management fees.

**6. Rate.** Withρ=0, a solvesa²+γa−γλ=0, so `a=[−γ+√(γ²+4γλ)]/2`. Forλ≫γ, a≈√(γλ) and ratea/λ≈√(γ/λ). Quadrupling λ approximately halves the rate and approximately doubles a. At fixedρ>0 the extreme-cost approximation differs; no universal half-speed statement follows.

## Problems 7–10: complete solutions

**7. Combination.** With unit-variance target and scores, feasible joint covariance andC=[[1,.5],[.5,1]], the best linear Pearson squared correlation isicᵀC⁻¹ic. EqualIC=.04 gives2×.04²/(1+.5)=.00213333; square root=.046188. Equal positive weights attain it here. This identity does not substitute average rank ICs.

**8. RMS change.** For stationary unit-variance matched scores with correlation1−φ, E[(zₜ−zₜ₋₁)²]=2φ. The RMS ratio is√(.32/.02)=4. With zero-mean Gaussian increments E|Δz|=√(2/π)×RMS, so the same ratio applies to absolute score changes. Portfolio turnover additionally needs fixed holdings scale, gross normalisation, matched universe and consistent treatment of drift; the proxy alone does not establish it.

**9. Attribution.** The sample identity uses the covariance term with divisorT. Static market contribution=.4×20%=8%; adding2% timing leaves12%−8%−2%=2% model-relative residual. The residual does not by itself prove skill.

**10. Ceiling and crossover.** In the bounded-latent toy, μ=.03,s=.06. The per-month limit μ/s=.5; independent months give annual√12/2=1.73205. Equating s² with(1−μ²−s²)/N gives `N*=(1−.0009−.0036)/.0036=276.5278`, about277. This continuous crossover is a model reference, not an estimated effective market breadth.

## Problems 11–12: qualifying solutions

**11. Moving-latent-correlation theorem.** Substitute returns: `π=ρ N⁻¹Σzᵢ²+√(1−ρ²)N⁻¹Σzᵢεᵢ`. Normalisation makes the first termρ. Conditional noise payoff has mean0 and variance(1−ρ²)/N, from the stated conditional unit variances and zero cross-covariances. Thus Eπ=Eρ=μ. Total variance gives `Varπ=Varρ+E[(1−ρ²)/N]=s²+(1−μ²−s²)/N`. Writeb=1−μ²−s²>0. Forμ>0, `IR(N)=μ(s²+b/N)^−1/2`, with derivative `μb/[2N²(s²+b/N)^(3/2)]>0`. For s>0 its limit isμ/s; for s=0 the exact ratio isμ√N/√(1−μ²). For positive s the continuous crossoverN*=b/s² gives variance2s², soIR(N*)=μ/(s√2) exactly. IfN*<2, the crossover lies below feasible normalised-score breadth. Independent periods permit√T annual scaling; serial dependence generally changes it. The proof concerns latent moments, not measured sample rank ICs.

**12. Scalar GP derivation.** Letd=1−ρ∈(0,1), c=1−φ, variancev>0, λ,γ>0 and known linear conditional forecastβcf. Current trade costs are paid now; operating return/risk and continuation are discounted:

`V(x₋,f)=max_x{d[βcfx−γvx²/2]−λv(x−x₋)²/2+d E[V(x,f⁺)|f]}`, withE[f⁺|f]=cf and finite innovation variance. Use `V=−Axx x₋²/2+Axf x₋f−Aff f²/2+constant`. Let`H=dγv+λv+dAxx`. The first-order condition gives`x=(λv/H)x₋+[dc(β+Axf)/H]f`. Matching x₋² gives `Axx=λv−(λv)²/H`. Writek=1−λv/H andAxx=λvk. Algebra yields `dλk²+(dγ+ρλ)k−dγ=0`; the stable root has0<k<1, witha=λk and

`a=[−(dγ+ρλ)+√((dγ+ρλ)²+4d²γλ)]/(2d)`.

Matching x₋f givesAxf=λv times the policy's f coefficient. Solving this linear relation gives coefficient`dcβ/(H−dcλv)`. Dividing byk expresses the policy as`(1−k)x₋+k aim`. Since`k(H−dcλv)=dv(γ+φa)`, the aim is `[βcf/(γv)]/[1+φa/γ]`: Markowitz's conditional-next-return target times the displayed discount. Forρ=0 andλ≫γ, k≈√(γ/λ). At fixedρ>0 asλ→∞, the positive-root equation instead givesa→dγ/ρ andk≈dγ/(ρλ). Known fixed risk, unconstrained notional holdings, linear dynamics, appropriate moments, timing and well-posedness are essential; the saved Riccati check validates this specified mathematics.

## Readings and verification

Textbooks: Grinold–Kahn, *Active Portfolio Management*; Isichenko, *Quantitative Portfolio Management*; Paleologo, *The Elements of Quantitative Investing*; Narang, *Inside the Black Box*. Foundational studies include Blume(1971,1975), Vasicek(1973), Rosenberg(1974), Connor–Korajczyk(1986), Brinson–Hood–Beebower(1986), Perold(1988), Grinold(1989), Clarke–de Silva–Thorley(2002), Berk–Green(2004), Qian–Hua(2004), Khandani–Lo(2007,2011), Ding(2010), Gârleanu–Pedersen(2013), Berk–van Binsbergen(2015), Novy-Marx–Velikov(2016), Boyd et al.(2017), Ding–Martin(2017), Frazzini–Israel–Moskowitz(2018), and Lou–Polk's comomentum work. Their empirical findings remain specific to their datasets and methods.

The existing pure House risk-model test passed; scientific source revision and visual review are distinct checks. For this task use only the audited ordinary-original restoration, cached-only guarded QA and explicit scene selection. The unrestricted compute-all command includes the excluded experiment and is not a rebuild instruction for this review. Evidence and current review status are maintained in `docs/qa/` and the series polish ledger.

---

# 量化金融，从零搭建 · 第31部分：风险模型、成本与跨期交易

本部分连接预测、协方差假设、执行成本和跨期决策。公开数据计算是回顾性的方法演示；它不建立可按历史信息实时执行的投资记录，也不证明未来盈利。

## 数据及解释边界

九项未改动的普通原始计算已各恢复一次：model、vasicek、law、costs、gp、combine、attribution、quake、theory。共九次包装器调用，没有失败或重试，没有新增市场试验，没有修改登记文件。策略实验在计数及缓存访问前被排除；本次审阅没有读取其封存缓存、载荷、结果或诊断。第31部分既有累计登记计数为23,535，全局23,562，其中十次既有计费属于本部分；计数描述研究历史，不代表独立业绩证据。

币安例子沿用第29部分冻结的公开USDT交易对网格和2018–2020研究掩码。继承的读取器先加载2017–2025公开日数组再筛选研究期；公开原始数据与封存策略载荷不同。2026年末冻结名单具有回顾性，存在幸存者、上市可得性、资产分类等时点问题。日度资格要求60天历史及至少25万USDT成交额中位数。风险模型每日合格币种数量中位数为34；预热及完整案例筛选进一步改变各项计算的样本。美元标签假设USDT平价。

量化地震回放使用Kenneth French截至2020年的49个美国日度行业组合，是行业代理，不是实际基金持仓、个股执行或Khandani–Lo原实验。缺失收益填零；算术损益不含费用、借券或冲击。文献引用、历史报道、保存的研究计算、模拟及选定算术输入各有不同适用范围。年化使用所述独立期数约定；未估计选择调整或依赖稳健的置信区间。完整连续成片试听及发音审阅仍单独待完成。

## 章节及科学边界

1. **基本定律。** 条件对角风险恒等式要求预测校准、固定分数范数和适当风险度量；实现的无条件信息比率需要更多假设。只做多转移系数是固定高斯分数、相对等权的启发式示例。等相关广度只对应等方差、等权、同预期收益的均值等价计数。
2. **因子风险模型。** XFXᵀ+Δ假设因子与残差正交且残差协方差对角。4,830对4,501,500的参数比较以X给定为条件；贝塔和波动率暴露自身也被估计。公司使用成交额平方根WLS权重及固定10⁻⁶岭；精确单位暴露模拟组合要求无正则且满秩。EWMA平方和外积是未中心化二阶矩。日期保留逐日间距及2017年末预热；曲线为算术累加，不是财富。t统计量使用独立日参考，未调整序列相关或选择。
3. **校准及贝塔。** 约71.7%是先取每日币种预测方差因子占比中位数，再跨日期取中位数，不是实现R²。四个保存的偏差统计量都在独立高斯参考半宽√(2/652)≈.0554外；肥尾、依赖、条件均值和自适应持仓限制该参考，也不能识别唯一原因。特质风险固定按.3向整体横截面均值收缩；Vasicek经验先验方差设10⁻⁸下限。12组比较是连续60个日历日区块，要求两块都合格，选择了未来幸存者；目标是带噪声的未来贝塔估计。MSE原值.04960，收缩后.04066。Dimson联合领先滞后回归不同于Scholes–Williams分别回归及市场自相关调整；领先收益只用于事后估计。
4. **执行成本。** 区分平均执行落差与终点峰值冲击。Q,V为货币名义额时，平均成本比例Y_avg σ√(Q/V)乘Q才是货币成本；对特定平方根峰值路径积分则出现2/3因子。例子取ADV与波动率各自的混合资产日中位数，不是某个实际中位币种。平均成本系数选为1。规模情景固定目标，以目标差代替漂移调整交易，并加5基点费用；融资、借券、价差、延迟及执行不完整。高参与率外推不确定，净夏普的分母也变动，故不必按√A下降。
5. **不交易与动态交易。** 光滑|Δh|^(3/2)在零点导数为零，通常不产生精确不交易区间。另加比例成本κᵢ|Δhᵢ|，在无约束固定凹问题中整本不交易条件是|αᵢ−γ(Σh₀)ᵢ|≤κᵢ。经典κ^(1/3)区间及κ^(2/3)效用损失渐近，需要连续扩散、内部目标、非退化及小成本假设，是另一个模型。
6. **Gârleanu–Pedersen。** 贝尔曼时间约定中经营收益、风险及续值乘d=1−ρ，当前交易成本立即支付。Riccati策略以已知固定正定风险及成本、线性条件动态、有限二阶矩、无约束名义持仓及适定时域为前提。√(γ/λ)速率近似要求零或可忽略贴现，约γ≪λ≪γ/ρ²；固定正ρ且λ趋于无穷时速率约γ(1−ρ)/(ρλ)。一般成本矩阵产生耦合风险流动性模式。经验φ是1减相邻日分数横截面Pearson相关均值，只是几何持续性代理。系数、持续性及波动率尺度重用研究数据。正衰减时两种目标乘数都不超过1，慢信号只是相对受重视。零成本行使用数值上的近乎免费极限。值迭代验证代数，不验证市场最优性。
7. **多期优化。** 原固定玩具使用L-BFGS-B及光滑3/2次方冲击近似。1、5、40期求解都收敛，首仓位.08812、.26382、.24069。终端持仓自由，不强制归零。展示完整40期路径并对齐预测期。时域目标与边界效应不同，不存在通用排序。借券是持仓成本；方差下限修改风险输入而非定义仓位约束。重规划不会修正错误模型；恢复GP必须匹配成本、时序、贴现和预测。
8. **合成。** 总体多重相关公式使用有限方差、标准化Pearson对象、正定C和可行联合协方差，不能互换为平均秩IC。岭将原始系数向零收缩，L¹归一化后大惩罚方向趋于Xᵀy而非等权。保存的回归拟合原始收益平方误差、无截距、缺失分数填零，不优化日均秩IC。挖掘、多档岭和反复2020验证都重用了研究数据。最强边际信号胜出不能证明其他信号无条件信息。几何时域IC仅为弱信号近似，正衰减时最终按h⁻¹/²下降。分开子组合也可以集中净额交易；耦合风险、成本与约束通常使单独最优与联合最优不同。
9. **容量及激励。** √(2φ)是平稳单位方差匹配分数的均方根变化，不直接等于换手；绝对换手比例需要固定增量分布、归一化和资产池。四分之九容量及三分之一净优势属于固定正g,c、无其他成本或风险目标的利润模型。图示net/g及四倍归一化利润，保留完整负尾。Berk–Green理想理性流量均衡为预期风险调整净阿尔法零，不是实现收益或总收益零；费用攫取交易成本后的租金。a/3费率属于已知技能平方根成本扩展；基金样本观察不识别所有关闭原因。
10. **量化地震。** 代理wᵢ=−(Rᵢ−R̄)/Σ|Rⱼ−R̄|，定义良好时净美元零、总敞口1，不保证贝塔中性。曲线累加日损益；参考日标准差来自2006年1月至2007年6月，不是置信区间。风格中性风险算例与回放分开；杠杆和集中度可使对角特质风险很大。平仓解释是一个假说。共动量是具有样本关联的代理，不是基金人数或预测保证。行业夏普不识别普遍反转溢价或崩盘暴露。
11. **归因。** 拟合收益恒等式乘对齐持仓产生模型相对的精确会计。特质收益不自动等于技能。Brinson式选股项使用组合行业权重，包含选股及交互。因子分量方差除总方差可超过1；分量协方差存在时并非可加Euler归因。择时用除数T的样本协方差，不证明可重复技能。Euler波动率归因要求固定半正定协方差及正组合波动率；因子项假设因子残差正交。
12. **协议及限额。** 评估前明确时点、资产池、预测、风险、成本、约束及选择程序；受已见结果影响的改动需要诚实的新评估。固定α=(10⁻⁵,10⁻⁵)、γ=1、σ²=(10⁻⁸,4×10⁻⁴)、账本1：无约束仓位(1000,.025)，10⁻⁴方差下限给(.1,.025)，.05独立仓位上限给(.05,.025)，选定ADV=(.5,.1)及.1成交量仓位上限给(.05,.01)。这是既有函数上的选定算术，不是校准规则、市场试验或历史修补。裁剪不是一般多资产约束最优解，限额不验证预测或盈利。

## 研究：精确标准化分数恒等式

N≥2、Σzᵢ=0、Σzᵢ²=N，有界潜在ρ∈[−1,1]。条件噪声均值零、方差1、跨资产协方差零。μ=Eρ、s²=Varρ、μ²+s²<1。在rᵢ=ρzᵢ+√(1−ρ²)εᵢ及π=N⁻¹Σzᵢrᵢ下，Eπ=μ，Varπ=s²+(1−μ²−s²)/N，IR=μ/√Varπ。

未改动的公司辅助函数省略−s²/N，明确标为近似。保存的模拟将高斯潜在参数截在±.99；输入矩是截断前参数，精确恒等式要求截断后真实矩。测得有限横截面Pearson或秩IC不等于潜在ρ。IC离散度已含抽样噪声，再加入噪声项可能重复计算；经验表是启发式比较。零和权重下π=N sd_cs(w) sd_cs(r) Corr_P(w,r)，横截面标准差除以N；规模随归一化及资产池变动。高斯下Spearman与Pearson也不同；混合波动率可造成混合峰度。四个经验比率改变定义并重用已选择数据，接近不代表因果分解或置信区间；未估计HAC或选择调整区间。记忆改变年化，但特定线性二次模型仍可有Riccati解；有限矩已知时肥尾不抹掉形式上的均值方差解，稳健估计与现实约束是不同难题。

## 六个交易台检查

1. 固定潜在玩具μ=.05、s=.10、N=500，月份独立：通常小相关基准.05√6000=3.873；精确年IR=√12×.05/√(.01+.9875/500)=1.5828。
2. 偏差统计量1.30表示标准化收益标准差高于1达30%；T=504的独立高斯95%近似参考1±√(2/504)=1±.0630，实际依赖、尾部和非零条件均值需另行分析。
3. 4%年度波动预测不是损失上限；一周损失10%可能与跳跃、遗漏协方差、杠杆或风险变化有关。
4. 毛收益及技术固定时四倍规模使每美元2%成本翻倍至4%；毛8%净4%，未计其他成本。
5. 成本四倍只在可忽略贴现区间使速率约减半；固定正贴现的极端成本区间速率按1/λ变化。
6. 固定例子的方差下限修改风险输入，独立限额约束仓位；两者都不证明未来盈利。

## 习题1–6：完整解答

**1. 开篇。** 指定潜在模型下月方差=.10²+(1−.05²−.10²)/500=.011975，月IR=.05/√.011975=.45691。独立月份年化乘√12，得1.5828。通常常IC小相关基准=.05√(500×12)=3.8730；精确常IC玩具还需除√(1−.05²)。

**2. 偏差参考。** 若zₜ独立标准正态，样本标准差b满足(T−1)b²服从χ²(T−1)。Delta方法给SD(b)≈1/√[2(T−1)]；T=504乘1.96的95%半宽约.0618，与简写√(2/T)=.0630接近。1.30在两者之外；没有分布假设就不是实际数据的置信结论。

**3. Vasicek。** 已知高斯观测方差与已知高斯先验方差都为.09，后验精度2/.09，均值(1.8/.09+1/.09)/(2/.09)=1.4。实际经验贝叶斯需估计先验及标准误。

**4. 规模。** 固定毛收益8%、成本随√A变化：四亿美元成本2%√(400/100)=4%，净8%−4%=4%。题设排除其他成本。

**5. 容量。** Π=gA−cA^(3/2)，g,c>0，盈亏平衡A₀=(g/c)²。Π′=g−(3/2)c√A=0给A*=(2g/3c)²=(4/9)A₀=四亿美元；Π″=−3c/(4√A)<0。此处每美元净收益g−2g/3=g/3，为管理费前。

**6. 速率。** ρ=0时a²+γa−γλ=0，a=[−γ+√(γ²+4γλ)]/2。λ≫γ时a≈√(γλ)，速率a/λ≈√(γ/λ)；λ四倍使速率约减半、a约加倍。固定正ρ的极端成本极限不同，不能普遍声称减半。

## 习题7–10：完整解答

**7. 合成。** 目标及分数单位方差、联合协方差可行且C=[[1,.5],[.5,1]]时，最佳线性Pearson相关平方为icᵀC⁻¹ic。两者IC=.04，得2×.04²/1.5=.00213333，开方=.046188，此处正等权达到最优。不能代入平均秩IC。

**8. 均方根变化。** 平稳单位方差匹配分数的滞后相关为1−φ，则E[(zₜ−zₜ₋₁)²]=2φ，比值√(.32/.02)=4。若增量为零均值高斯，E|Δz|=√(2/π)乘均方根，故绝对分数变化也同比。换手还需要固定持仓尺度、总敞口归一化、匹配资产池及一致漂移处理，代理本身不能证明换手比。

**9. 归因。** 样本协方差用除数T。静态贡献.4×20%=8%，择时2%，故模型相对残差12%−8%−2%=2%。残差本身不证明技能。

**10. 上限与交点。** 潜在玩具μ=.03、s=.06，月极限μ/s=.5，独立月份年化√12/2=1.73205。令s²=(1−μ²−s²)/N，得N*=(1−.0009−.0036)/.0036=276.5278，约277。这是连续模型参考，不是市场有效广度估计。

## 习题11–12：资格题完整证明

**11. 潜在相关变动定理。** 代入π=ρN⁻¹Σzᵢ²+√(1−ρ²)N⁻¹Σzᵢεᵢ。归一化使第一项为ρ。给定ρ及分数，噪声收益均值0，方差(1−ρ²)/N，来自条件单位方差及零跨协方差。因此Eπ=μ。全方差公式给Varπ=s²+E(1−ρ²)/N=s²+(1−μ²−s²)/N。记b=1−μ²−s²>0，μ>0时IR(N)=μ(s²+b/N)^−1/2，导数μb/[2N²(s²+b/N)^(3/2)]>0。s>0时极限μ/s；s=0时精确值μ√N/√(1−μ²)。正s下连续交点N*=b/s²使方差2s²，故IR(N*)=μ/(s√2)精确成立。N*<2则交点低于可行分数广度。独立期才允许√T年化，序列依赖通常改变比例。证明针对潜在矩，不是测得样本秩IC。

**12. 标量GP。** d=1−ρ∈(0,1)、c=1−φ、方差v>0、λ,γ>0、已知线性条件预测βcf。当前交易成本立即支付，经营收益风险及续值贴现：

`V(x₋,f)=max_x{d[βcfx−γvx²/2]−λv(x−x₋)²/2+d E[V(x,f⁺)|f]}`，E[f⁺|f]=cf，创新方差有限。猜测V=−Axx x₋²/2+Axf x₋f−Aff f²/2+常数。H=dγv+λv+dAxx，一阶条件x=(λv/H)x₋+[dc(β+Axf)/H]f。比较x₋²得Axx=λv−(λv)²/H。记k=1−λv/H，Axx=λvk，整理得dλk²+(dγ+ρλ)k−dγ=0。稳定根0<k<1，a=λk：

`a=[−(dγ+ρλ)+√((dγ+ρλ)²+4d²γλ)]/(2d)`。

比较x₋f得Axf=λv乘策略的f系数，解得系数dcβ/(H−dcλv)。除以k写成(1−k)x₋+k aim。利用k(H−dcλv)=dv(γ+φa)，目标为[βcf/(γv)]/[1+φa/γ]，即条件下一期收益的Markowitz目标乘持续性折扣。ρ=0且λ≫γ时k≈√(γ/λ)；固定ρ>0且λ趋无穷时a趋dγ/ρ，k≈dγ/(ρλ)。已知固定风险、无约束名义持仓、线性动态、适当矩、时序和适定性至关重要；保存的Riccati检查只验证这一指定数学问题。

## 阅读与验证

教材及逐章论文列于英文书目，中文叙述遵循同样的样本及假设边界。现有公司风险模型纯测试已通过；科学源文件审阅与视觉验证是不同检查。本任务只用已审计普通原始计算恢复、受保护的仅缓存QA和明确场景选择。无参数compute-all会包括被排除实验，不是本次重建指令。实际证据及当前状态在docs/qa及系列打磨台账维护。

## Current visual review

Scientific presentation revision, bilingual construction and actual rendered visual review are complete on `quantitative-finance`, source `70ec582e14fb870c9708de30588ba3ca81988bb5`, fingerprint `4dd7a2450d8f062b900f9f040faac8e3c6f335e324b37e5552de2fa868c18dfd`. All 30 bilingual endpoint sheets, 15 English forty-frame motion sheets and 29 focused native frames were actually inspected across all fifteen scenes. Every exact flagged interval has an artifact-bound decision. Earlier diagnostics retain their own execution fingerprints; no diagnostic approval transfers to final renders.

All 134 narration contexts translate at runtime, and actual raw narration agrees across bilingual endpoints, English motion and current construction captures. The 79 actual computed fields and 42 captured curve ranges pass. One existing pure numerical test passes. The 190 additive captions preserve all 34,105 prior strings, yielding 34,295. All 98 protected files remain unchanged.

The chaptered silent timing preview runs 62:48, with fifteen chapters and English subtitles. Eleven CPU speech reports cover 101 sampled lines; the actual narrated opening lasts 231.067 seconds. Full continuous production listening and pronunciation review remain separately pending. [Artifact-bound evidence](../../../docs/qa/quant31-polish-evidence.json).

## 当前视觉审阅

科学表述、双语构建与实际画面审阅已完成。本轮实际检查全部 30 张双语旁白节点画面表、15 张英文四十帧动画表及 29 张重点原尺寸画面，覆盖十五个场景。每个标记区间均有绑定实际文件的审阅决定；构建诊断保留原执行指纹，不转移为最终批准。

全部 134 处旁白均经运行时翻译与实际文本核对，79 个实际格式化字段及 42 处曲线范围检查通过。新增 190 条字幕保留此前全部 34,105 条，共 34,295 条；98 个受保护文件未改变。九个常规原始计算仅恢复一次，无失败、重试、新增市场试验、登记修改或封存实验访问。

分章静音预览为 62:48，含十五章及英文字幕。十一份 CPU 语音报告覆盖 101 个抽样句段，并检查实际配音开场。画面与信号检查不替代完整成片连续听审或发音认证，后两项仍单独待办。
