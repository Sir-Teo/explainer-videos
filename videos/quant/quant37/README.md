# Quant, Built — Part 37: Market Impact and Execution

Part 37 of the [43-part series](../README.md) studies what large orders cost and how execution schedules depend on the model. The [syllabus](../SYLLABUS.md) and [reading map](../READING.md) give the broader context. The lesson distinguishes signed terminal price displacement, quantity-weighted average execution shortfall and causal mechanical impact.

The unchanged original computations use Binance BTCUSDT perpetual aggregate trades dated 16–25 May 2023, four best-quote files reduced to a 100-millisecond grid, 2023 one-minute bars, and specified mathematical and queue simulations. A public post-2020 archive is distinct from a sealed strategy experiment. No strategy is registered or opened here. Existing registrations total **23,552 through Part 37 and 23,562 globally**.

## What the evidence can establish

- A same-minute signed-volume association has finite-bin slope about 0.81. Public trades do not identify parent orders, mechanical execution costs or a held-out forecast. The tape's minute windows, nearest populated bin centers and day weighting are the implemented conventions.
- Terminal square-root impact and average impact cost require different coefficients. If the execution path is (I(q)=c\sqrt q), total impact cost is (2cQ^{3/2}/3), and average shortfall grows as (2c\sqrt Q/3). Average cost per share does **not** fall as order size grows.
- Static latent density ρ(x)=Lx gives displacement Δ=√(2Q/L). Diffusive latent-book simulation, finite-grid exponent fits and asymptotic arguments are distinct. Dimensions alone do not determine the square-root function. Two-thirds permanent displacement additionally requires a fair-pricing relation and a compatible execution path.
- The response function averages signed future displacement over all starting trades. The propagator is a truncated linear projection fitted on four date files, using the second preceding quote-grid index, boundary clipping and event-time joins. It does not isolate a causal trade effect. The fitted positive-parameter shifted-power-law surrogate removes the raw kernel's initial rise and imposes regularity.
- The relation β=(1−γ)/2 follows under long-memory, regular-kernel scaling assumptions. Diffusive variance does not establish a martingale. Finite-lag fits without uncertainty do not verify asymptotic efficiency.
- Positive definiteness of the quadratic energy is sufficient for nonnegative round-trip cost. Positivity restricted to zero-total directions, strict convexity, existence of a measure-valued optimum and absence of intermediate sales are separate questions. Bochner's theorem uses a spectral measure; an ordinary Fourier density needs further assumptions. Fine Gaussian matrices can be severely ill-conditioned.
- Almgren–Chriss uses independent zero-mean price innovations, deterministic holdings, matching interval conventions and positive effective coefficient η̃=η−γτ/2. Sigma is price per square root of time. The descriptive flow calibration of eta is not an identified cost curve. The urgency time 1/κ is an e-folding time; log(2)/κ is only the long-horizon exponential half-life.
- The positive-ρ exponential candidate proves existence and uniqueness by explicit verification. A general continuous integrally strictly positive-definite kernel gives **at most one** minimizer; it does not alone guarantee attainment over all finite signed measures. The Fredholm potential includes past and future trades and is not the causal displacement process.
- Quote-grid jumps of at least ten ticks are selected events, not identified message-level sweeps. Median normalized depth recovery and mean signed price drift are distinct. A clipped one-step depth proxy is not an identified resilience rate or confidence bound; subsequent drift does not identify news.
- The Q-learning comparison uses one fitted simulator, specified training/evaluation seeds and restricted observations/actions. Individual Monte Carlo standard errors omit model and training uncertainty. Matching seeds alone does not align innovations after policies consume different numbers of draws. The chosen-sales profile sums to **16.656**, excluding the forced final liquidation that is included in evaluation costs.
- VWAP follows expected volume; realized participation need not remain constant. POV completion uses a volume **rate**, rather than a daily total without a time conversion. Benchmarks require independently fixed timestamps and price sources. A first-fill benchmark is endogenous.
- Rule 37 is a proposed research protocol, with a cost convention, uncertainty, schedule and order record. Break-even illustrations omit other trading legs and uncertainties and are not approved capacity or optimal sizing.

## Chapters and sources

The twelve scenes cover the opening question, metaorders and shortfall, the square-root law, propagators, no dynamic arbitrage, Almgren–Chriss, exponential resilience, a learned executor, execution algorithms and TCA, Rule 37, variational execution and a recap. Ten numerical pauses specify their units, horizons and assumptions.

Textbooks: Bouchaud, Bonart, Donier and Gould, *Trades, Quotes and Prices* (2018); Cartea, Jaimungal and Penalva, *Algorithmic and High-Frequency Trading* (2015); Guéant, *The Financial Mathematics of Market Liquidity* (2016); Lehalle and Laruelle, *Market Microstructure in Practice* (2018).

Paper trail: Perold (1988); Loeb (1983); Torre (1997); Bertsimas and Lo (1998); Almgren and Chriss (2000); Almgren (2003); Almgren, Thum, Hauptmann and Li (2005); Bouchaud, Gefen, Potters and Wyart (2004); Huberman and Stanzl (2004); Gatheral (2010); Alfonsi, Fruth and Schied (2010); Alfonsi, Schied and Slynko (2012); Gatheral, Schied and Slynko (2012); Obizhaeva and Wang (2013); Moro et al. (2009); Bershova and Rakhlin (2013); Tóth et al. (2011); Donier and Bonart (2015); Donier, Bonart, Mastromatteo and Bouchaud (2015); Zarinelli et al. (2015); Kyle and Obizhaeva (2016); Patzelt and Bouchaud (2018); Bucci et al. (2019); Nevmyvaka, Feng and Kearns (2006); Ning, Lin and Jaimungal (2021); Lehalle and Neuman (2019); Cardaliaguet and Lehalle (2018); Brunnermeier and Pedersen (2005). Literature findings are attributed examples, not claims to have reproduced proprietary order records.

## Twelve complete problems and solutions

Problems 1–6 are basic, 7–10 advanced and 11–12 qualifying-exam level. All cost calculations below omit spread and fees unless explicitly stated.

1. **Square-root scaling.** One percent of daily volume has terminal displacement 10 bp; keep Y, volatility and daily volume fixed. At 4% and 9%, (I=10\sqrt{Q/0.01V}), giving **20 and 30 bp**. Linear scaling gives **40 and 90 bp**. These are terminal displacements. Under a path c√q, average displacement is two-thirds of the peak; a different measured average-cost coefficient must be calibrated accordingly.

2. **Static latent book.** Offer density is ρ(x)=Lx for x≥0, with L=2 units/tick² and Q=9 units. Integrate Q=∫₀^Δ 2x dx=Δ², hence **Δ=3 ticks**. This assumes the profile is static and linear over the consumed region; it is not a dynamic refill result.

3. **Propagator exponent.** Assume sign correlation proportional to ℓ^−0.6 and flow variance exponent 2−γ−2β. Setting this exponent to one yields 2−0.6−2β=1, hence **β=0.2**. This is a conditional scaling calculation. Linear variance growth alone does not imply zero conditional expected returns, nor identify the market's causal mechanism.

4. **A four-leg round trip.** Let G(t)=1 for 0≤t<τ and zero afterwards, including G(0)=1. Take v=(1,−1,1,−1) at spacing 0.7τ. Net quantity is zero and absolute turnover four. Only adjacent off-diagonal pairs interact. Thus ½vᵀΓv=½[4+2(−1−1−1)]=**−1**, or −0.25 per unit absolute turnover. This is a frictionless negative expected model cost; executable spread and fees could offset it. A single two-leg buy/sell pair would not provide this counterexample.

5. **Continuous AC urgency and half-life.** Set T=60 minutes and λσ²/η=0.01/min². Then κ=**0.1/min** and x(t)/X=sinh[0.1(60−t)]/sinh(6). At t=20, the fraction is sinh(4)/sinh(6)≈**0.13529**. Exact half-life is (60-\operatorname{asinh}(\tfrac12\sinh6)/0.1\approx6.9313) minutes. The e-folding time is 10 minutes, while the long-horizon exponential half-life is log(2)/0.1≈6.93147 minutes. Distinguish the approximation from the exact finite-horizon value.

6. **Continuous TWAP risk.** Let X=5,000 BTC, T=60 minutes and sigma=$12/(BTC√min). With x(t)=X(1−t/T), Var(IS)=σ²∫₀ᵀx(t)²dt=σ²X²T/3. Thus sd=12×5,000×√20=**$268,328**. Units reduce to dollars. An N-step post-trade convention uses σ²(T/N)Σxₖ² and is slightly smaller; this is a clock convention, not a discrepancy to hide.

7. **Exponential resilience.** Set X=T=q=1 and ρ=2, allowing finite signed measures with half-self-impact. Each endpoint atom is a=X/(2+ρT)=**1/4** and the interior rate is b=ρa=**1/2 per unit time**. Total mass 2a+bT=1. The full symmetric potential is f(t)=a(e^−2t+e^−2(1−t))+(b/2)(2−e^−2t−e^−2(1−t))=1/2. Cost is ½fX=**1/4**. Continuous TWAP cost is ½[1−(1−e^−2)/2]≈**0.283834**. Saving relative to TWAP is 1−0.25/0.283834≈**11.9203%**. TWAP's excess relative to the optimum is 0.283834/0.25−1≈**13.5335%**. Merely specifying ρT would fix bT, not the dimensional rate b.

8. **A VWAP hour.** Expected hourly share is 7.5% and parent quantity 1,000 BTC. Allocate **75 BTC** to that hour. If actual volume differs from the forecast, the realized participation rate differs from the plan. A schedule using expected volume is not the same as adaptive fixed-share POV.

9. **Participation.** Let Q=0.02V_day and a constant market rate V_day per day. At participation 5%, T=0.02/0.05=**0.4 day**; at 20%, **0.1 day**. Under a size-only square-root terminal model both have Yσ√0.02. A diffusive root-duration risk scale is **twice as large** for the slower order. This comparison assumes the same shape of schedule, constant volatility and no separate rate-dependent impact.

10. **Simplified one-leg break-even.** Expected alpha is 10 bp=0.001, daily return volatility 0.02, dollar daily volume $10bn, and average-impact coefficient Y=1. The inequality 0.02√(Q/V)<0.001 gives Q/V<0.0025, hence **Q<$25m**. Equality is break-even for the single modeled component. Spreads, fees, other legs, changing conditions and alpha uncertainty reduce useful capacity; this is neither an optimal position nor approval to trade.

11. **Qualifying: conditional variational theorem and exponential existence.** Work with finite signed Borel measures μ on [0,T], total mass X, a continuous symmetric G, and integral strict positivity of energy for nonzero measures (strict positivity on zero-mass directions suffices for uniqueness). Write C(μ)=½B(μ,μ). If two distinct minimizers existed, their midpoint would have cost lower by C(μ−ν)/4, a contradiction. This proves **at most one**, without proving existence or boundedness of total variation along minimizing sequences. At an existing minimum μ*, every zero-mass variation ε(δ_a−δ_b) is admissible with either sign. Its derivative is f(a)−f(b), where f(t)=∫₀ᵀG(|t−s|)dμ*(s), so f is constant λ. Conversely, for any equal-mass ν, C(ν)=C(μ*)+∫f d(ν−μ*)+C(ν−μ*)=C(μ*)+C(ν−μ*)≥C(μ*). The constant-potential candidate is therefore optimal, uniquely under strict positivity. Integrating f gives C*=λX/2.

    For G(t)=e^−ρt/q with ρ,q,T>0, propose μ*=aδ₀+b dt+aδ_T. Its potential is [a(E₀+E_T)+(b/ρ)(2−E₀−E_T)]/q. Set b=ρa and 2a+bT=X to get a=X/(2+ρT), b=ρX/(2+ρT). Potential is λ=2a/q and C*=X²/[q(2+ρT)]. This explicit candidate proves existence. For X>0 it has no sales. Narrow rate bursts approximating the atoms preserve mass, have bounded total variation and converge in energy by continuity of G; rate-only strategies have the same infimum but cannot attain the unique atomic optimum. At ρ=0, all schedules cost X²/(2q) and uniqueness fails. Large ρT gives X²/(qρT); matching nonzero temporary η requires holding 1/(qρ) fixed. The full symmetric potential is a marginal cost, **not** the causal displacement process.

12. **Qualifying: discrete Almgren–Chriss.** Fix deterministic x₀=X, x_N=0, τ=T/N, η̃=η−γτ/2>0 and λ≥0. Apart from the schedule-independent permanent term, minimize J=(η̃/τ)Σₖ₌₁^N(xₖ₋₁−xₖ)²+λσ²τΣₖ₌₁^Nxₖ² under the post-trade noise convention. For each interior j, differentiation gives (2η̃/τ)(2x_j−x_{j−1}−x_{j+1})+2λσ²τx_j=0. Therefore x_{j+1}−2x_j+x_{j−1}=(λσ²τ²/η̃)x_j. The characteristic roots are e^±κτ with cosh(κτ)=1+λσ²τ²/(2η̃); boundaries yield x_j=X sinh[κ(T−jτ)]/sinh(κT). Strict convexity of the positive quadratic form ensures the unique solution. As λ→0, x_j→X(1−j/N), TWAP. At fixed grid and λ→∞, every interior holding tends to zero and liquidation occurs in the first interval. As τ→0 with η̃→η>0, κ→√(λσ²/η), giving the continuous sinh solution. The finite-grid urgency uses arcosh, not the continuous square-root expression exactly.

## 数据、方法与十二道完整解答

本部分研究市场冲击与执行，但区分终点价格位移、每单位平均执行差额及因果机械冲击。十个不改动的常规原始计算使用公开成交、最优报价、K线及指定模拟；不登记或打开策略。第37部分累计既有试验为23,552，全局23,562。公开2023年原始档案不是封存策略结果。

同分钟成交量与价格的幂律斜率是描述性相关，不识别母订单成本。传播子来自有限滞后线性拟合，报价使用第二个先前网格索引并截断边界；拼接日期、短样本与陈旧报价都会影响结果。正参数平移幂律是另行选择的规则化模型，不能把模型的正定性当成市场无操纵的证明。

平方根路径的每单位平均成本随规模增加，不是下降。公平定价的三分之二需要额外均衡条件；量纲不能单独决定函数。AC的波动率是每平方根时间的价格波动，1/κ是e倍时间，不是精确半衰期。严格凸性只给出至多一个最小解；一般核仍需存在性论证。指数核通过直接构造证明存在与唯一。弗雷德霍姆势包含未来交易的边际成本，不等于因果价格位移。

报价网格跳跃不是逐笔已识别扫单；深度恢复与价格恢复是不同统计。Q学习的误差条是单个策略的蒙特卡洛误差，不包含模型与训练不确定性；同种子不等于同路径。选择出售曲线合计16.656单位，没有计入费用评估中包含的强制终端清仓。第37条规则是研究流程建议，不是部署、容量批准或实盘业绩。

以下1–6为基础题，7–10为进阶题，11–12为资格考试题。未特别说明时忽略价差与费用。

1. **平方根缩放。** 已知日成交量1%的终点位移10基点，固定Y、波动率及日成交量。4%为10√4=**20基点**，9%为10√9=**30基点**；线性分别为40与90。若路径为c√q，平均成交位移是终点的三分之二，总成本为2cQ^(3/2)/3。平均每单位成本仍按√Q增加。

2. **静态潜在簿。** ρ(x)=Lx，L=2单位/跳²，买入9单位。Q=∫₀^Δ 2x dx=Δ²=9，故**Δ=3跳**。假设消耗范围内密度线性且不恢复；不能直接当作动态扩散模型结论。

3. **传播子指数。** 假设符号相关指数γ=0.6，方差幂指数为2−γ−2β。令其等于1得**β=0.2**。条件缩放结论不证明价格是鞅，也不唯一识别真实机制。

4. **四腿往返。** 方框核在滞后小于τ时为1，其余为0，自冲击为1。以0.7τ间隔交易(1,−1,1,−1)，总量零、绝对换手四。仅相邻异号相互作用，成本½[4+2(−1−1−1)]=**−1**，每单位绝对换手−0.25。价差费用可能抵消模型收益；两腿简单买卖不能给出这个反例。

5. **连续AC与半衰期。** T=60分钟，λσ²/η=0.01/分钟²，故κ=**0.1/分钟**。x(t)/X=sinh[0.1(60−t)]/sinh6。20分钟剩余sinh4/sinh6≈**13.529%**。精确半衰期为60−asinh(sinh6/2)/0.1≈**6.9313分钟**；e倍时间为10分钟，长时限指数近似半衰期为log2/0.1≈6.93147分钟。

6. **连续TWAP风险。** X=5000BTC、T=60分钟、σ=12美元/(BTC√分钟)。持仓X(1−t/T)，方差σ²∫x²dt=σ²X²T/3，标准差12×5000×√20=**268,328美元**。离散成交后持仓约定使用σ²τΣx_k²，数值略小；需保留时点约定。

7. **指数恢复。** X=T=q=1、ρ=2。两端各a=**1/4**，中间速率b=**1/2每单位时间**，2a+bT=1。对称边际势f=a(E₀+E_T)+(b/2)(2−E₀−E_T)=1/2，成本fX/2=**1/4**。连续TWAP成本½[1−(1−e^−2)/2]≈**0.283834**。相对TWAP节省**11.9203%**；TWAP相对最优成本多**13.5335%**，分母不同。只有ρT不能确定有单位的速率，必须给出T。

8. **VWAP小时。** 母订单1000BTC，该小时预期成交量占7.5%，计划交易**75BTC**。预测误差会改变实际参与率；按预期曲线分配不等于按实际成交量自适应POV。

9. **参与率。** Q=0.02V_day，市场恒定每日期间交易V_day。5%参与率需**0.4天**，20%需**0.1天**。仅含规模的平方根模型两者终点冲击均Yσ√0.02；扩散时机风险之比√(0.4/0.1)=**2**。这依赖相同轨迹形状、恒定波动率及忽略独立速率效应。

10. **单腿简化盈亏平衡。** α=0.001、σ_day=0.02、V_day=100亿美元、平均冲击Y=1。由0.02√(Q/V)<0.001得Q/V<0.0025，故**Q<2500万美元**。价差、手续费、其他交易腿、模型及信号不确定性会降低实际可用容量；这不是最优仓位或批准。

11. **资格题：条件唯一性与指数核存在性。** 在紧区间有限带符号Borel测度、总量X上，令G连续对称且对非零测度积分严格正定；零质量方向严格正定已足够给出唯一性。若两个不同最小解存在，中点成本会比两者平均低C(μ−ν)/4，矛盾，故至多一个。这个论证不保证存在，也不控制极小序列总变差。若μ*是最小解，任意正负ε(δ_a−δ_b)均可行，一阶导数f(a)−f(b)=0，故全区间对称势f=λ。反过来，任意同总量ν有C(ν)=C(μ*)+∫f d(ν−μ*)+C(ν−μ*)≥C(μ*)，因此恒势候选足够。积分得C*=λX/2。

    对G=e^−ρt/q，ρ,q,T>0，取μ*=aδ₀+b dt+aδ_T。势为[a(E₀+E_T)+(b/ρ)(2−E₀−E_T)]/q。令b=ρa并满足2a+bT=X，得a=X/(2+ρT)、b=ρX/(2+ρT)、λ=2a/q，成本X²/[q(2+ρT)]。直接候选证明存在与唯一；X>0时无卖出。用窄速率脉冲逼近端点原子，保持质量与有界总变差，由核连续性得能量收敛。仅速率类有相同下确界但不达到原子最优解。ρ=0时所有轨迹成本X²/(2q)，唯一性失败；大ρT渐近X²/(qρT)，保持非零暂时成本η需同时缩放q使1/(qρ)固定。势包含未来交易，并非过去成交造成的因果位移。

12. **资格题：离散AC。** 固定x₀=X、x_N=0、τ=T/N、η̃=η−γτ/2>0、λ≥0。去掉恒定永久项后最小化J=(η̃/τ)Σ(x_{k−1}−x_k)²+λσ²τΣx_k²，采用成交后持仓噪声约定。内点求导得(2η̃/τ)(2x_j−x_{j−1}−x_{j+1})+2λσ²τx_j=0，因此二阶差分等于(λσ²τ²/η̃)x_j。特征根e^±κτ满足cosh(κτ)=1+λσ²τ²/(2η̃)，边界给出x_j=X sinh[κ(T−jτ)]/sinh(κT)。正二次型严格凸，解唯一。λ→0时为线性TWAP；固定网格λ→∞时内点持仓趋零，第一区间卖完。小步长且η̃→η>0时κ→√(λσ²/η)，得到连续解；有限网格应使用arcosh形式。

## Reproducibility status

The original `compute.py` and financial library remain unchanged. Routine rendering uses exact pinned ordinary caches and rejects house/envelope/track/holdout prefixes before cache access. Ten audited originals each succeeded once. One existing pure execution test and chosen arithmetic are recorded locally. Final bilingual construction, artifact-bound visual evidence and completion status will be linked after their actual reviews. Full production listening remains a separate task.

## Current visual review

Visual review is complete on source `d0bb9fd9ac5066e147b4216e8e90b7ec4a68a26e`, fingerprint `b67d34676c5aa8aed7b6435de5ec8ee275842388d246a9cdae44380b92c89158`. [Artifact-bound evidence](../../../docs/qa/quant37-polish-evidence.json) binds all 24 bilingual endpoint sheets, 12 English forty-frame motion sheets and 13 native frames actually inspected across twelve scenes. Exact flagged intervals and manually noticed concerns have individual observations and decisions. All 24 current bilingual construction sheets were actually reviewed; their 88 formatted fields and 44 plotted ranges agree with actual runtime values. Earlier diagnostic rounds preserve independent source and mutable-output bytes at their actual execution fingerprints and confer no final approval.

All 149 actual narration contexts agree across construction, bilingual endpoints and English motion: 95 manual Mandarin revisions and 54 exact unchanged English/Chinese pairs. English narration contains 9,769 words, about 58.1 minutes at 168 words per minute. Twelve complete bilingual solutions retain 6/4/2 grouping and three enlarged problem pages. The 134 additive captions preserve all 35,209 baseline values, yielding 35,343. One existing pure execution test and eight QA regression tests pass. The QA voiceover wrapper now captures narration-end after the underlying context completes its speech padding; its regression tests exercise that actual wrapper order.

Ten audited unchanged ordinary originals succeeded once each. Twenty-six possible public Binance keys have a shared immutable-key rejection barrier, including nine inherited rejections, before the original checker. Possible dependencies do not assert every key was read by every original. Four reused public derived grids are independently authenticated against prior provenance and current bytes. Ten ordinary cache hashes are pinned, and sensitive prefixes are rejected before cache/count access. All 98 protected files and financial algorithms remain unchanged. No original was rerun, no rejected key retried, and there was no refresh, new market trial or sealed strategy access. Existing registrations remain 23,552 through Part 37 and 23,562 globally.

The twelve-chapter silent timing preview is 71:54, with English subtitles. Eleven actual CPU speech reports cover 135 sampled lines, and the actual narrated opening lasts 225.867 seconds. Full continuous production listening and pronunciation review remain separately pending.

## 当前视觉审阅

已实际审阅全部24张双语旁白节点画面表、12张英文四十帧动画表及13张原尺寸重点画面，覆盖十二个场景；每个标记区间与人工关注点均有绑定文件的观察与决定。先前诊断保留真实执行指纹、独立源文件与可变输出，不向最终画面转移批准。

全部149处实际旁白在各模式一致，含95处人工修订中文与54处英文中文均未变的复用；实际核对88个格式字段及44处曲线范围。十二道题按六道基础、四道进阶、两道资格考级提供完整双语解答。新增134条字幕保留此前全部35,209个值，总计35,343条。一个既有执行数学测试及八个画面检查回归测试通过。

十个经审计的常规原始计算各执行一次且成功，98个受保护文件及原金融算法未改变；没有原函数重跑、失败键重试、刷新、新市场试验或访问封存策略。四个既有公开派生网格经独立来源与字节哈希认证。既有登记量为本部分累计23,552、全局23,562。十二章静音预览71:54并含英文字幕；十一份CPU报告检查135个句段，另实际检查配音开场。完整成片连续听审及发音审阅仍单独待办。
