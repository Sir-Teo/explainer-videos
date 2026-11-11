# Quant, Built — Part 35: Who Trades With Whom

Part 35 of the [forty-three-part series](../README.md), following the [syllabus](../SYLLABUS.md) and [reading list](../READING.md). This chapter distinguishes equilibrium models from descriptive order-flow measurements. Current narration is approximately 60 minutes; rendering and actual visual review are pending.

## Models, observations and limits

The fourteen scenes cover dealer inventory; binary Glosten–Milgrom quotes; one-auction and continuous Gaussian Kyle; daily-price liquidity proxies; same-bar flow regressions; PIN and VPIN; two-market information shares; market structure; high-frequency trading; historical liquidity stress; proposed House controls; continuous-time verification; and worked questions.

Nine unchanged ordinary originals succeeded once each: `dealer`, `gm`, `kyle`, `flow`, `vpin`, `discovery`, `cross`, `daily` and `acf`. The unchanged `measures` original failed once because `yahoo/bars/SPY/2015-01-01_2020-12-31` differed from its frozen checksum. Its ten-ETF table, BTC Roll result and Amihud scatter are unavailable and omitted. That key is never retried or refreshed; no replacement historical backtest is introduced. The scenes permit only exact hashes of the nine verified outputs. Sensitive House/envelope/track/holdout prefixes are rejected before cache or counter access.

Public Binance spot/perpetual minute archives cover BTCUSDT in 2021–2024, and five spot coins in 2024. These raw observations are distinct from sealed strategy outcomes. There are no new strategy trials, registrations, registry writes or sealed strategy accesses. Existing counts remain **23,552 through Part 35; 23,562 globally**. All 98 protected file hashes remain unchanged.

The audit maps 154 possible immutable public keys before dispatch; it does not assert every possible key was read. Eight earlier rejected keys were carried into a persistent barrier; none overlapped this part's closures. The new SPY rejection is added to that barrier, which blocks every unstarted dependent before invocation.

Scientific distinctions used throughout:

- Inventory diffusion can exit fixed inventory bounds; financial ruin additionally needs wealth and capital assumptions. The simulated shading rule is a heuristic, and terminal across-seed mean/SD is not an annualized Sharpe.
- GM paths condition on true value one and record pretrade beliefs. Their crossing index is capped at 80 for non-hits. A drift-based learning-time calculation is a heuristic, not the same median or an uncensored expectation.
- Close times base-asset taker imbalance approximates dollar flow. Same-bar OLS, selected conditional means, aggregation slopes and cross-coin scaling are descriptive/endogenous. Classical t-statistics are not HAC inference. Missing observations can compress return, aggregation and lag clocks. These outputs identify neither causal parent-order cost nor a public-information variance share.
- Roll needs constant spread, appropriate independent trade signs and efficient-price dynamics. Nonnegative covariance makes its formula undefined, rather than proving zero spread. Corwin–Schultz clips negative estimates in the preserved original. Amihud is an unsigned return-per-dollar proxy, mechanically related to volume. A tick, a quoted spread and an effective spread are distinct.
- VPIN uses full-sample return SD and average volume, so this is ex-post construction. Its mean absolute equal-volume-bucket imbalance differs from the comparator's absolute aggregate taker imbalance over approximate whole-bar windows. Their correlation is not classifier validation or informed probability. Selected crash windows establish neither prediction nor causality. Every finite saved VPIN value and daily stress slope is displayed without clipping.
- Information shares condition on a cointegration/VECM specification and innovation covariance. Cholesky-order ranges are attribution bounds within that model, not confidence intervals or guaranteed causal bounds. Finer timestamps need not resolve all ambiguity. Common-trend weights are not information shares.
- Fee arithmetic specifies maker versus taker, one-way versus round trip, and full versus half spread. A maker rebate does not determine a taker fee. Historical rules and legal accounts remain dated; current proceedings, rules and compliance dates are not verified here.
- Own-generated turnover does not establish independent execution capacity. The cascade condition is local amplification in a stipulated linear feedback model, not a necessary-and-sufficient real-crash test. Batch-auction benefits require their design assumptions.
- The continuous theorem assumes Gaussian value independent of Brownian noise, risk-neutral competitive dealers, a fixed noise clock and admissible insider orders. A quadratic verification potential gives a bound with a nonnegative terminal penalty; formal HJB cancellation alone is insufficient. Posterior variance falls linearly, unlike Shannon information. Euler terminal prices retain fresh noise, and selected simulations have no numerical error bound or Monte Carlo interval.

The proposed Rule 35 is a review requirement, not a deployed surveillance, execution or counterparty-identification system. CPU signal checks and rendered-image inspection cannot certify pronunciation or full continuous production listening.

## Twelve worked problems: six basic, four advanced, two qualifying

All inputs below are explicit mathematical models. No problem restores a failed source, runs a market backtest or calibrates a firm.

### Basic 1 — Quote shading

Take mid (v-\gamma q), bid/ask mid (\mp s/2), inventory (q=40), shading coefficient (\gamma=0.05), full spread (s=1). The mid is (v-2), so **bid (v-2.5), ask (v-1.5)**. Lowering both quotes encourages inventory reduction in the specified arrival model. This arithmetic establishes neither optimality nor survival for an arbitrary dealer.

### Basic 2 — One buy in Glosten–Milgrom

Values are 0 and 1, prior (p=1/2), informed-arrival share (\mu=0.4), and independent noise traders buy/sell equally. Thus (P(B\mid V=1)=0.7), (P(B\mid V=0)=0.3). Bayes gives posterior (p'=0.7); the executed ask was 0.7. For the **next** trader,

\[
a'={0.7\cdot0.7\over0.7\cdot0.7+0.3\cdot0.3}={49\over58}=0.8448276,
\qquad b'={0.7\cdot0.3\over0.7\cdot0.3+0.3\cdot0.7}=0.5.
\]

These are competitive conditional zero-profit quotes, not unconditional estimates of a real informed share.

### Basic 3 — More noise in one-auction Kyle

With fixed positive value variance and independent Gaussian noise, equilibrium has (\lambda=\sigma_v/(2\sigma_u)), (\beta=\sigma_u/\sigma_v), (x=\beta(v-p_0)), and (E\pi=\sigma_v\sigma_u/2). Doubling **noise variance** replaces (\sigma_u) by (\sqrt2\sigma_u). Hence (\lambda' =\lambda/\sqrt2), (\beta'=\sqrt2\beta), fixed-gap order (x'=\sqrt2x), and (E\pi'=\sqrt2E\pi). This compares equilibria; deviations against a fixed pricing rule are a separate problem.

### Basic 4 — Roll's identity

For lag-one covariance (-0.0004) dollars squared, the estimated full spread is (2\sqrt{0.0004}=\mathbf{0.04}) dollars. The square root restores dollar units. Identification requires constant spread and a price decomposition with independent suitable trade signs and independent efficient-price innovations. Reversal, correlated signs and sampling noise can contaminate the estimate; a negative sample covariance alone does not establish the assumptions. Nonnegative covariance leaves this real-valued formula undefined.

### Basic 5 — Fitted change versus execution cost

A descriptive slope (4.6) bp per $1m times observed net flow $10m gives **46 bp fitted same-bar change**. It does not identify the causal change from adding a $10m parent order.

Separately stipulate deterministic permanent linear execution impact (p(q)-p_0=\lambda q), with no outside flow, spread, fees, decay or opportunity cost. For quantity (Q), the mean shortfall is (Q^{-1}\int_0^Q\lambda q\,dq=\lambda Q/2=\mathbf{23\ bp}), while terminal change is 46 bp. This extra path assumption is not estimated by a same-minute regression or concave minute bins; their shape does not prove real execution is cheaper or prescribe slicing.

### Basic 6 — Bulk classification

For volume 1000 BTC and standardized price change +2, bulk buys are (1000\Phi(2)=\mathbf{977.2499}) BTC; bulk sells are **22.7501** BTC. These are assigned volumes. Recorded taker volumes could be 500/500 because price change does not determine trade side. Neither number is the probability of private information. Comparing average absolute bucket imbalance with absolute imbalance after aggregating buckets changes the estimand: cancellation matters.

### Advanced 7 — Trend weights and information shares

Assume a stable two-market VECM with cointegrating vector ((1,-1)) and loadings (\alpha=(-0.9,0.1)). An orthogonal common-trend vector is ((0.1,0.9)), already summing to one. Thus B has **common-trend weight 0.9**, as it adjusts less to the discrepancy.

Information shares additionally depend on innovation covariance. With equal independent innovation variances, the variance contributions are proportional to (0.1^2) and (0.9^2). B's information share is (0.81/(0.01+0.81)=\mathbf{81/82=0.9878049}). If residuals correlate, Cholesky ordering affects attribution. Weight 0.9 is not information share 0.9, and neither is an unconditional causal leadership claim.

### Advanced 8 — Tick and fees

At price $20, a one-cent **full** spread gives half-spread $0.005/$20 × 10,000 = **2.5 bp**. A maker rebate of 0.2 cent does not specify the taker fee, so all-in taker cost is initially unidentified.

Now separately stipulate a taker fee of 0.2 cent per share. One-way taker cost relative to the midpoint is 0.5 + 0.2 = **0.7 cent = 3.5 bp**. A hypothetical natural full spread of one-third cent has half-spread one-sixth cent = **0.833333 bp**. The binding tick alone multiplies half-spread by 3; tick plus the stipulated fee multiplies it by **4.2**, not 3. A half-cent tick permits finer quotes but need not produce that spread: competition, costs, queues and fill probability matter. Maker spread revenue adds its rebates before other costs; taker round-trip cost adds its two fees.

### Advanced 9 — Per-execution adverse loss

In a chosen competitive risk-neutral per-fill model, each execution earns half-spread (s/2) and has adverse loss (J=3) ticks with probability (p=0.02); other costs are zero. Break-even gives (s/2-pJ=0), so expected adverse loss is **0.06 tick** and required full spread is **0.12 tick**. Tick-size constraints may force a larger feasible quote. Unconditional news frequency alone does not give adverse probability conditional on execution. A batch mechanism reduces this component only under its update, timing and competitive assumptions; other losses can remain.

### Advanced 10 — Participation and the volume clock

Stipulate exogenous tradable volume rate 1 ADV/day and execution rate 9% of that clock, for order 0.05 ADV. Time is (0.05/0.09=\mathbf{5/9}) day. An **independent** doubling of that rate yields (5/18) day at unchanged participation and other conditions.

Turnover generated by this order is endogenous, so observing double turnover does not establish double outside liquidity. If participation instead means 9% of total volume **including the order**, and outside rate is (V), solve (q=0.09(V+q)), giving (q=(0.09/0.91)V). The same 0.05 ADV then takes (0.05\cdot0.91/0.09=0.505556) day at outside rate 1 ADV/day. This is a different denominator, not a contradiction or a safe real execution prescription. A feedback response to prints can accelerate without creating external capacity.

### Qualifying 11 — Verification, admissibility and the bridge

Fix positive constant (\lambda) and noise diffusion (\sigma_u>0), on ([0,1]). Value (v) is known in the insider filtration and independent of its Brownian noise. Under the fixed price rule (dp=\lambda\theta\,dt+\lambda\sigma_u\,dW), let (g=v-p) and

\[
J(t,p;v)={g^2+\lambda^2\sigma_u^2(1-t)\over2\lambda}.
\]

Require predictable locally integrable trading, (E\int_0^1g_t^2dt<\infty), (E\int_0^1|g_t\theta_t|dt<\infty), and terminal convergence allowing the expected potential identity to pass to time 1. These are sufficient conditions for this proof; localization without justified limits is insufficient. The formal HJB rate term (g\theta+J_p\lambda\theta) cancels, and (J_t+J_{pp}\lambda^2\sigma_u^2/2=0). Ito gives the stronger identity

\[
dJ=-g\theta\,dt-\sigma_u g\,dW,\qquad
\pi=J_0-J_1-\sigma_u\int_0^1g_t\,dW_t.
\]

The stochastic integral is square-integrable and mean zero. Since (J_1=g_1^2/(2\lambda)\ge0), (E\pi=EJ_0-EJ_1\le EJ_0). This is a verification bound, not proof that every arbitrary strategy is optimal. (J(1,p)) is a terminal **penalty** in this argument, not a literal remaining-horizon payoff at arbitrary terminal price. Zero terminal penalty attains the bound only within the admissible class and the fixed price-rule deviation problem.

For the Gaussian candidate take (\lambda=\sigma_v/\sigma_u), (\theta=g/[\lambda(1-t)]). Its solution is

\[
p_t=v+(p_0-v)(1-t)+\lambda\sigma_u(1-t)\int_0^t{dW_s\over1-s}.
\]

With (v\sim N(p_0,\sigma_v^2)) independent of (W), (Eg_t^2=\sigma_v^2(1-t)). Consequently (E\int g^2dt=\sigma_v^2/2), (E\int|g\theta|dt=\sigma_v^2/\lambda), and (E\int|\theta|dt\le2\sigma_v/\lambda<\infty). The terminal gap converges to zero in mean square; terminal penalties converge in mean, profit in (L^1), and the martingale in (L^2). The bound is attained, yielding (E\pi=\sigma_v\sigma_u).

However (E\theta_t^2=\sigma_u^2/(1-t)), whose integral diverges. Imposing globally square-integrable **rate** would exclude this equilibrium; it is the integrated squared **gap** that controls the verification martingale. Pricing consistency is a further equilibrium requirement, proved in Problem 12. The preserved Euler scheme has last-step error (p_N-v=\lambda\sigma_u\sqrt{\Delta t}\,Z), so finite-step endpoint learning is not exact.

### Qualifying 12 — Equilibrium and horizon units

One auction: independent (v-p_0\sim N(0,\sigma_v^2)), (u\sim N(0,\sigma_u^2)); insider chooses (x=\beta(v-p_0)) before seeing noise; competitive risk-neutral dealers price (p=p_0+\lambda(x+u)). At fixed (\lambda>0), conditional profit is ((v-p_0)x-\lambda x^2); its maximizer gives (\beta=1/(2\lambda)). Gaussian conditional expectation gives

\[
\lambda={\beta\sigma_v^2\over\beta^2\sigma_v^2+\sigma_u^2}.
\]

Combining yields (\beta=\sigma_u/\sigma_v), (\lambda=\sigma_v/(2\sigma_u)), (E\pi=\sigma_v\sigma_u/2). Expected noise loss at that post-auction price is (E[(p-v)u]=\lambda\sigma_u^2=\sigma_v\sigma_u/2). Dealers break even unconditionally; posterior variance is (\sigma_v^2/2).

For continuous horizon (T>0), noise diffusion (\sigma_u) has quantity per square-root-time units. Take (\lambda=\sigma_v/(\sigma_u\sqrt T)), (\beta_t=1/[\lambda(T-t)]), (\Sigma_t=\sigma_v^2(1-t/T)). Then Gaussian filtering gain (\beta_t\Sigma_t/\sigma_u^2=\lambda), and (\dot\Sigma=-\lambda^2\sigma_u^2=-\sigma_v^2/T). This verifies the candidate conditional-expectation pricing rule, together with the strategy/filtration assumptions. The bridge satisfies the preceding admissibility checks after rescaling time, so expected insider profit is **(\sigma_v\sigma_u\sqrt T)**. Instantaneous price diffusion is **(\lambda\sigma_u=\sigma_v/\sqrt T)**.

Value SD 2 and noise diffusion 1 give ((\lambda,\text{price diffusion},E\pi)=(2,2,2)) at (T=1), versus ((1,1,4)) at (T=4). The one-auction comparison over horizon (T) must use noise-order SD (\sigma_u\sqrt T), giving half the continuous profit. If total noise variance is held fixed when changing (T), profit no longer rises with (\sqrt T). Linear posterior-variance decline gives Gaussian mutual information (\tfrac12\log(T/(T-t))), not constant information release. Any continuous noise-trader profit statement must also specify an execution convention: the post-trade discrete-auction limit differs from a naive Ito integral at pre-trade prices.

## Sources and review status

Textbooks: O'Hara, *Market Microstructure Theory* (1995); Hasbrouck, *Empirical Market Microstructure* (2007); Foucault, Pagano and Röell, *Market Liquidity* (2013); Harris, *Trading and Exchanges* (2003).

The [series reading list](../READING.md) supplies the full bibliography: Garman; Ho–Stoll; Roll; Kyle; Glosten–Milgrom; Back; Holden–Subrahmanyam; Hasbrouck; Easley and coauthors; Amihud; Back–Baruch; Hendershott–Jones–Menkveld; Corwin–Schultz; Menkveld; Andersen–Bondarenko; Brogaard and coauthors; Budish–Cramton–Shim; Collin-Dufresne–Fos; Kirilenko and coauthors; Yang–Zhu; Aquilina–Budish–O'Neill; Zhu; Duarte–Young; and the dated CFTC–SEC and Treasury joint staff reports. Attributed historical/legal claims are separate from computed results. Actual current bilingual construction, final frame/motion inspection and speech checks remain pending at this source stage.

---

# 第35部分：谁与谁交易

这是[四十三部分系列](../README.md)的第35部分，依据[教学大纲](../SYLLABUS.md)与[阅读表](../READING.md)。十四个场景分别讨论库存、Glosten–Milgrom报价、Kyle模型、流动性代理、同期订单流回归、PIN/VPIN、信息份额、市场结构、高频交易、流动性压力、拟议规则、连续时间验证及习题。当前英文旁白约60分钟；双语构建与最终画面审阅仍待实际执行。

九个未经修改的常规原始计算各成功执行一次。`measures`在首次核对2015—2020年SPY冻结数据时失败，因此十只ETF表、比特币Roll结果与Amihud散点图均未产生并已省略。没有重试失败键、刷新校验和或替代历史回测。只允许加载九个成功输出的精确哈希；House、envelope、track、holdout前缀在查询缓存路径或计数器之前即被拒绝。

154个可能的公开数据键在调用前建立完整依赖映射；这不表示每个键都被读取。八个此前被拒绝的键被继承，本部分没有交集；新SPY拒绝加入共享屏障，阻止所有尚未启动的依赖。公开原始行情不同于封存策略结果。没有新市场试验、注册、登记表写入或封存策略访问。累计计数至第35部分为**23,552**，全系列为**23,562**；98个受保护文件不变。

必须区分：库存扩散与财务破产；条件于真实高价值的GM路径与先验混合下的鞅；封顶的交易前信念索引与未删失学习时间；同期回归与因果冲击；最小价格单位、报价价差与有效价差；平均分桶绝对失衡与合并后取绝对值的失衡；共同趋势权重与信息份额；maker返佣与taker费用；独立外部成交能力与自身制造的成交量。缺失时点可能压缩收益、聚合和滞后时钟。完整样本校准的VPIN是事后研究构造，不是已验证的实时信号。选定危机窗口和经典iid t统计量不能提供因果或稳健预测结论。

连续Kyle定理要求高斯价值独立于布朗噪声、风险中性竞争定价、明确的噪声时钟及可容许策略。二次函数是验证上界的势函数，其终值是惩罚；不能凭HJB形式抵消就宣称任意策略最优。后验方差线性下降，不代表香农信息匀速释放。有限Euler路径末步保留新噪声，不会精确到达价值。拟议规则不代表已经部署的交易、监控或对手身份识别系统。历史法规与案例不构成当前法律状态核实；信号检查也不等于完整成片听审或发音认证。

## 十二道完整解答：六道基础、四道进阶、两道资格题

以下都是明确给定的数学模型，不恢复失败来源、不拟合公司，也不开展新市场回测。

### 基础1：库存报价

设中间报价 (v-\gamma q)，买卖报价为中间报价减/加半价差。代入 (q=40,\gamma=0.05,s=1)，中间报价为 (v-2)，**买价 (v-2.5)，卖价 (v-1.5)**。这只是指定线性启发式规则的运算；库存对成交概率的影响取决于到达模型，不能据此证明任意做市商最优或永不破产。

### 基础2：一次买单后的GM报价

价值为0或1，先验各半，知情交易比例0.4，非知情交易独立等概率买卖。因此高价值时买单概率0.7，低价值时0.3。贝叶斯后验为**0.7**，该次成交卖价也是0.7。对于**下一位**交易者，卖价为 (0.7^2/(0.7^2+0.3^2)=49/58=\mathbf{0.8448276})，买价为 (0.7\cdot0.3/(0.7\cdot0.3+0.3\cdot0.7)=\mathbf{0.5})。不要把本次成交价与下一次报价混同。这是模型内条件零利润报价，不是现实知情比例的无条件估计。

### 基础3：单次Kyle的噪声增加

保持价值方差不变，噪声独立且为高斯分布。均衡有 (\lambda=\sigma_v/(2\sigma_u))、(\beta=\sigma_u/\sigma_v)、(x=\beta(v-p_0))、(E\pi=\sigma_v\sigma_u/2)。噪声**方差**翻倍使标准差乘 (\sqrt2)，所以冲击系数除 (\sqrt2)，策略系数、固定价值差下的订单以及无条件期望利润均乘 (\sqrt2)。这是不同均衡的比较；固定价格规则下改变订单属于另一问题。

### 基础4：Roll价差

若样本一阶自协方差为 (-0.0004) 美元平方，完整价差估计为 (2\sqrt{0.0004}=\mathbf{0.04}) 美元。开平方恢复美元单位。经济识别要求恒定价差、适当独立的成交方向及独立有效价格创新等假设。价格反转、相关订单和采样误差都可能污染估计。负样本协方差不证明模型成立；非负协方差使该实数公式无定义，不证明价差为零。

### 基础5：拟合变化与执行成本

同期描述性斜率每百万美元4.6基点，乘一千万美元净流量，得到**46基点拟合收益变化**，不是额外加入一笔母订单的因果成本。

另行假设永久线性执行路径 (p(q)-p_0=\lambda q)，忽略外部流量、价差、费用、衰减和机会成本，则平均执行偏离为 (Q^{-1}\int_0^Q\lambda q\,dq=\lambda Q/2=\mathbf{23基点})，终点变化仍是46基点。这个路径是新增数学假设，不是分钟回归或凹形分组图估计出来的。后者不能证明现实大单更便宜，也不能推出最优拆单方案。

### 基础6：批量分类

成交量1000 BTC，标准化价格变化为+2时，分配的买量 (1000\Phi(2)=\mathbf{977.2499}) BTC，卖量**22.7501** BTC。实际主动买卖量仍可能各500，因为价格变化不决定成交方向。这些量也不是私有信息概率。先在每个桶内取绝对值再平均，与先合并多个桶再取绝对值不同：相反方向的失衡会在后者抵消。

### 进阶7：趋势权重与信息份额

在稳定的双市场VECM中，协整向量取 ((1,-1))，调整载荷 (\alpha=(-0.9,0.1))。与其正交且和为1的共同趋势向量为 ((0.1,0.9))，因此B的趋势权重为**0.9**。

信息份额还依赖创新协方差。若两市场创新等方差且独立，贡献正比于权重平方，所以B的信息份额为 (0.9^2/(0.1^2+0.9^2)=81/82=\mathbf{0.9878049})，不是0.9。创新相关时Cholesky排序影响归属；这些都是模型内统计对象，不是无条件的因果领先判决。

### 进阶8：最小价格单位与费用

股价20美元，完整报价价差1美分，半价差为0.5美分，即**2.5基点**。maker得到0.2美分返佣，并不告诉我们taker费用，因此起初不能确定taker全部成本。

另行指定taker每股收费0.2美分，则相对中点的单边成本为0.5+0.2=**0.7美分=3.5基点**。假设自然完整价差为三分之一美分，其半价差为六分之一美分，即**0.833333基点**。单独由约束性tick导致的半价差倍数为3；加上指定taker费后倍数为**4.2**。半美分tick只允许更细报价，不保证实际价差或每位交易者都获益。maker跨买卖价的毛收入加返佣，taker往返成本则加两次费用；还需考虑成交概率、排队、信息与库存损失。

### 进阶9：按成交条件化的逆向损失

指定风险中性竞争模型：每次成交赚半价差 (s/2)，以概率0.02承受3tick逆向损失，其余成本为零。盈亏平衡 (s/2=0.02\cdot3=\mathbf{0.06tick})，所以完整价差**0.12tick**。实际可报价格还受tick限制。无条件新闻频率不是“给定成交后遭遇逆向损失”的概率。批量竞价只有在及时更新、竞价规则和竞争等假设下才减少这一成分，其他风险不会自动消失。

### 进阶10：参与率的分母

先规定外生可交易成交量为每天1 ADV，执行率为这个外生时钟的9%，目标0.05 ADV，则用时 (0.05/0.09=\mathbf{5/9天})。若独立外部流动性翻倍，其他条件不变，用时变为**5/18天**。

自身订单制造的成交量是内生变量，观察到总成交量翻倍不证明外部承接能力翻倍。若把参与率改定义为“含自身订单在内的总成交量的9%”，外部速率为 (V)，则需解 (q=0.09(V+q))，得到 (q=0.09V/0.91)。在每天外部1 ADV时，同一订单用时 (0.05\cdot0.91/0.09=\mathbf{0.505556天})。这是不同分母，不是前一答案矛盾，也不是安全执行建议。程序对成交打印的反馈可以加速，而不创造独立流动性。

### 资格11：验证、可容许性与布朗桥

在单位区间固定正系数 (\lambda,\sigma_u)，内部人知道价值 (v)，其噪声布朗运动独立于价值；价格规则固定为 (dp=\lambda\theta dt+\lambda\sigma_u dW)。记 (g=v-p)，取势函数 (J=[g^2+\lambda^2\sigma_u^2(1-t)]/(2\lambda))。要求交易率可预测且局部可积、(E\int g^2dt<\infty)、(E\int|g\theta|dt<\infty)，并要求足以通过终点期望极限的收敛。只写局部化而不证明极限合法是不够的。

形式HJB中 (g\theta+J_p\lambda\theta=0)，且 (J_t+J_{pp}\lambda^2\sigma_u^2/2=0)。更有力的是伊藤恒等式 (dJ=-g\theta dt-\sigma_u g,dW)，积分后

\[
\pi=J_0-J_1-\sigma_u\int_0^1g_t,dW_t.
\]

平方可积保证随机积分均值为零。因此 (E\pi=EJ_0-EJ_1\le EJ_0)，因为 (J_1=g_1^2/(2\lambda)\ge0)。这是可容许策略的期望利润上界；只有终值惩罚为零且极限成立时才取等号。(J(1,p))不是任意终点价格下还剩交易时间的真实价值函数，形式抵消也不使任意交易率可容许或最优。

取 (\lambda=\sigma_v/\sigma_u)、(\theta=g/[\lambda(1-t)])，桥解为

\[
p_t=v+(p_0-v)(1-t)+\lambda\sigma_u(1-t)\int_0^t(1-s)^{-1}dW_s.
\]

先验 (v\sim N(p_0,\sigma_v^2)) 且独立于噪声，故 (Eg_t^2=\sigma_v^2(1-t))。于是 (E\int g^2dt=\sigma_v^2/2)，(E\int|g\theta|dt=\sigma_v^2/\lambda)，且 (E\int|\theta|dt\le2\sigma_v/\lambda<\infty)。终点差均方趋于零；惩罚在均值中、利润在 (L^1) 中、随机积分在 (L^2) 中收敛。上界被达到，无条件期望利润为 (\sigma_v\sigma_u)。

但是 (E\theta_t^2=\sigma_u^2/(1-t)) 的积分发散；若强加整个区间交易率平方可积，就排除了该均衡。验证鞅由“价值差的平方积分”控制，不能与“交易率平方积分”混同。价格是否等于市场条件期望，还需下一题的过滤一致性。原始Euler算法末步保留误差 (p_N-v=\lambda\sigma_u\sqrt{\Delta t}Z)，所以有限步数不会精确学习终值。

### 资格12：均衡与期限单位

单次拍卖中，价值差与噪声订单独立高斯，方差分别 (\sigma_v^2,\sigma_u^2)。内部人先于观察噪声选择 (x=\beta(v-p_0))，风险中性竞争做市商价格为 (p_0+\lambda(x+u))。固定正 (\lambda) 时条件利润为 ((v-p_0)x-\lambda x^2)，一阶条件给出 (\beta=1/(2\lambda))。高斯条件期望又给出 (\lambda=\beta\sigma_v^2/(\beta^2\sigma_v^2+\sigma_u^2))。联立得 (\beta=\sigma_u/\sigma_v)、(\lambda=\sigma_v/(2\sigma_u))，内部人期望利润 (\sigma_v\sigma_u/2)。在同一成交后价格下，噪声交易者期望损失 (E[(p-v)u]=\lambda\sigma_u^2=\sigma_v\sigma_u/2)，做市商无条件盈亏平衡；后验方差为初始的一半。

连续期限 (T>0) 时，(\sigma_u) 的单位是数量/时间平方根。取 (\lambda=\sigma_v/(\sigma_u\sqrt T))、(\beta_t=1/[\lambda(T-t)])、(\Sigma_t=\sigma_v^2(1-t/T))。代入高斯过滤增益有 (\beta_t\Sigma_t/\sigma_u^2=\lambda)，且 (\dot\Sigma=-\lambda^2\sigma_u^2=-\sigma_v^2/T)。结合信息结构与候选策略，这验证市场条件期望定价。桥的可容许性按时间缩放由上一题得到，期望利润为**(\sigma_v\sigma_u\sqrt T)**，瞬时价格扩散系数为**(\lambda\sigma_u=\sigma_v/\sqrt T)**。

价值标准差2、噪声扩散1时，(T=1) 给出 ((\lambda,价格扩散,期望利润)=(2,2,2))，(T=4) 给出 ((1,1,4))。比较同一期限的单次拍卖，必须把噪声订单标准差取成 (\sigma_u\sqrt T)，此时利润恰为连续情形的一半。若改变期限时固定总噪声方差，而非固定方差率，利润不再随期限平方根增加。高斯互信息为 (\frac12\log[T/(T-t)])，不是匀速释放。连续噪声交易损益还必须说明执行价格约定；成交后离散拍卖极限不同于直接采用成交前价格的朴素伊藤积分。

## 来源与审阅状态

教材为O'Hara（1995）、Hasbrouck（2007）、Foucault、Pagano与Röell（2013）、Harris（2003）。完整论文和历史报告列表见[系列阅读表](../READING.md)。历史归因与代码计算须分开。当前仍需实际双语构建、所有最终节点与动画画面检查以及配音抽样；任何成功渲染都不能自动视为视觉批准。完整成片连续听审与发音审阅单独待办。

## Current visual review

Scientific presentation, bilingual construction and actual visual review are complete on `quantitative-finance`, source `c77897af01980389769c99a688ee699bdab60582`, fingerprint `0aba85399aed1c943007b501bf98c3bcc1678d45bb01daa057871c94236e1fd1`. All 28 bilingual endpoint sheets, 14 English forty-frame motion sheets and 28 native frames were actually inspected across fourteen scenes. Every exact flagged interval has an artifact-bound observation and decision. Earlier diagnostic rounds retain exact independent source and mutable-output copies at their real execution fingerprints; those observations do not transfer final approval. Actual construction caught two plain-TeX underscores, a crowded plot label, small module text and stray recap quotation marks; final checks use fresh corrected renders.

All 148 runtime narration contexts agree across current bilingual construction, bilingual endpoints and English motion. The 98 manual Chinese revisions and 50 exact unchanged English/Chinese reuses pass runtime comparison. All 53 actual formatted fields and 58 captured plot ranges pass. English narration contains 9,880 words, approximately 58.8 minutes at 168 words per minute. One existing pure mathematical test passes. The 172 additive captions preserve all 34,886 previous values, yielding 35,058. All 98 protected files remain unchanged.

Ten distinct audited ordinary originals were invoked once each: nine succeeded; `measures` failed frozen SPY validation and is omitted without retry or substitute. No original reruns, repeated rejected-key checks, refresh, new market trials or sealed strategy access occurred. Sensitive prefixes are rejected before cache/count access, and only nine exact cache hashes are permitted. Existing registrations remain 23,552 through Part 35 and 23,562 globally. The chaptered silent timing preview is 71:31, with fourteen chapters and English subtitles. Eleven CPU speech reports cover 130 sampled lines, and the actual narrated opening lasts 175.800 seconds. Full continuous production listening and pronunciation review remain separately pending. [Artifact-bound evidence](../../../docs/qa/quant35-polish-evidence.json).

## 当前视觉审阅

科学表述、双语构建与实际画面审阅已完成。实际检查全部28张双语旁白节点画面表、14张英文四十帧动画表及28张原尺寸重点画面，覆盖十四个场景。所有精确标记区间都有绑定文件的观察与决定。此前诊断保留独立源文件、可变输出原始字节及真实执行指纹，不向新渲染转移批准。

全部148处实际旁白在当前双语构建、双语节点及英文动画之间一致；98处人工修订中文与50处英文中文均未变化的复用通过核对，53个格式化字段和58处曲线范围检查通过。英文约58.8分钟。新增172条字幕保留此前全部34,886个值，总计35,058条；98个受保护文件未改变。

十个常规原始计算各执行一次，九个成功，一个因冻结标普输入验证失败而省略，没有重试或替代计算。没有重复拒绝键检查、刷新、新市场试验或访问封存策略。分章静音预览71:31，含十四章及英文字幕；十一份CPU报告覆盖130个抽样句段，并检查实际配音开场。完整成片连续听审与发音审阅仍单独待办。
