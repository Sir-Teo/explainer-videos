# Quant, Built — Part 42: Machines in the Market

Part 42 of the forty-three-part series asks how trading rules, learning and shared inputs interact through a market. A simulator can demonstrate a mechanism without identifying the mechanism behind real prices. This distinction connects the artificial markets, herding chain, dealer learner, pricing game and common-signal crowd throughout this part.

The only downloaded market input is Kenneth French's daily research-window data through 2020. All other numerical examples are fixed-seed simulations or algebra from the existing algorithms. The seven audited ordinary calculations were each invoked once successfully. No financial algorithm or `compute.py` was changed, no new market trial was registered, and no sealed strategy result was opened. No language-model trader was executed.

## Chapters

| Chapter | Main question and scope |
|---|---|
| Opening | What do these experiments actually establish? Profit indices, interactive execution and variance shares have different meanings. |
| 1. Artificial markets | Selected switching-agent models produce tails and volatility clustering. Matching moments is descriptive; the original 81-point research grid is neither a held-out validation nor unique mechanism identification. |
| 2. Herding | Kirman's finite chain has an exact beta-binomial law. The Beta limit holds with fixed alpha, requiring the spontaneous-switching probability to scale with population. Sampled crossings differ from exact-state passage times. |
| 3. Simulators | ABIDES, response metrics and the Lucas critique. A model counterfactual is conditional on its assumptions. Objectives do not automatically establish real causal validity. |
| 4. Learning to trade | The dealer has 39 compressed observations, not a fully observed MDP. Scores include inventory penalties. Finite constant-step learning and one training seed do not establish convergence, equivalence or universal method rankings. |
| 5. Language models | Historical contamination is possible, not certain. Synthetic novelty is insufficient by itself. Prospective timing, version and trial controls remain necessary. |
| 6. Pricing learners | Fifteen prices and finite training produce supra-competitive profit indices and conditional retaliation. A 200-step recurrence cap is shorter than the 225-state space. Frozen recurrence does not certify equilibrium or legal agreement. |
| 7. Common signals | Independent unit-variance components give a common variance fraction of about 86% at N=100, w=0.2. A deliberately inserted positive signal increment illustrates amplification, not crash frequency. |
| 8. Stability | Dated 2024 IMF/FSB assessments, selected historical rules and distinct operational/liquidity episodes. Historical reports do not establish current prevalence or absence of AI instability. |
| 9. Rule 42 | Proposed stress tests and governance, rather than a completed deployment-approval system. |
| Research | One-shot deviations, grim trigger and a specified finite punishment. Continuous-action benchmarks are distinguished from discrete learning and mixed-domain illustrative ratios. |
| Outro | Qualifications, six desk questions and twelve fully solved problems. |

## Mechanisms and their limits

For Kirman's chain, N>1, epsilon>0, 0≤delta<1 and valid transition probabilities are required. With c=(1-delta)/(N-1) and alpha=epsilon/c,

\[
 u(k)=\frac{N-k}{N}c(\alpha+k),\qquad d(k)=\frac{k}{N}c(\alpha+N-k).
\]

Spontaneous switching and imitation are additive. The remaining probability is a self-loop. Detailed balance gives

\[
 \pi(k)=\binom Nk\frac{B(k+\alpha,N-k+\alpha)}{B(\alpha,\alpha)}.
\]

At fixed alpha, k/N converges in law to Beta(alpha,alpha), and the two-endpoint mass is asymptotic to 2 Gamma(2alpha)/Gamma(alpha) times N^(-alpha). Keeping epsilon fixed is a different asymptotic regime. The exact 90→10 mean passage time is not precisely the same estimand as inspecting a path every ten steps for a crossing from at least 90 to at most 10.

The dealer's informed traders observe current latent value, not the next innovation. That innovation occurs after the trading decision. Inventory and last trade omit the mid-minus-value gap, so state aliasing matters. The score is latent-value marked P&L less an inventory penalty. The best evaluated fixed rule is a finite-grid selection, rather than an independently confirmed optimum. Fixed-fill replay estimates a different object from interactive execution because changing quotes changes fills. Sequential importance evaluation needs overlap, correctly recorded propensities and suitable identification assumptions; products of ratios can have severe variance.

The pricing index is (profit − Nash profit)/(monopoly profit − Nash profit), using the stated benchmarks. It is not the fraction of the price gap. Punishment percentages condition on the fixed-point subset; recovery of an average does not imply recovery in every session. Independent additive payoff noise is not an adverse-selection model. Simulated high prices and retaliation are coordination diagnostics, not a proof of subgame perfection or a legal conclusion. The August 2024 RealPage complaint is cited as a historical allegation, without asserting its current procedural status.

For the repeated-game theorem, assume common action domains, perfect public monitoring, bounded stage payoffs, 0≤delta<1, a collusive payoff pi_c, best current deviation payoff pi_d>pi_c, and a credible static-Nash payoff pi_n<pi_c. Grim trigger is subgame perfect iff

\[
 \delta\ge\frac{\pi_d-\pi_c}{\pi_d-\pi_n}.
\]

For a T-period Nash punishment, specify that any deviation during punishment restarts the clock. On-path deterrence is

\[
 \pi_d-\pi_c\le(\pi_c-\pi_n)\sum_{j=1}^T\delta^j.
\]

A threshold strictly below one exists only when T(pi_c−pi_n)>pi_d−pi_c. During punishment, Nash best response prevents a current gain and restarting delays the better continuation. The continuous logit benchmark gives grim 0.3931 and T=1,2,3,5 thresholds 0.6477, 0.4475, 0.4103, 0.3954. These do not automatically certify the fifteen-price learners.

The reported pure-grid min-best-response value 0.2041, combined with continuous collusion/deviation payoffs, produces the illustrative ratio 0.3574. This is a mixed-domain calculation, not a general Abreu bound, a mixed-action minmax calculation or an established attainable penal code. Credible continuation punishments and consistent domains require separate analysis.

For x_i=w s+(1−w)e_i, assume s,e_1,...,e_N are mutually independent, zero mean and unit variance. The orders are correlated. Then

\[
 V=N^2w^2+N(1-w)^2,\qquad C=\frac{Nw^2}{Nw^2+(1-w)^2}.
\]

C is a variance fraction, not a realised trade fraction. V is minimised at w=1/(N+1), so it is not monotone from zero. The simulated volatility dots include an inserted shock in 5,000 observations, whereas the stationary reference uses unmodified signals. The selected shock adds +4 to an already random common signal. Under impact kappa/sqrt(N), its added return is kappa sqrt(N) w·4: eight zero-common volatility units at N=100,w=0.2. The selected day's total return also includes its baseline random components. There is still private-signal return at w=0. A flow-factor variance fraction additionally needs factor-residual orthogonality. Shared news and rebalancing can produce common flow without AI uniformity.

## Six desk questions, with solutions

1. **Do wide spreads and a forced-undercut response prove collusion?** No. They motivate coordination analysis. Check individual policies, profitable deviations at relevant histories, information exchange and applicable law. The simulated fixed-point subset and its conditional punishment rate cannot support a universal economic or legal conclusion.
2. **Why is a tape not a new quoting policy's environment?** Quotes alter participation and adverse selection. Adding two ticks to every old fill holds the response fixed; it does not reconstruct the trades the wider quote would receive. The example's replay score is about 445 versus 129 in interactive simulation.
3. **What should simulator-trained policies face?** Alternative regimes, opponents and copies, plus response metrics rather than unconditional moments alone. Report hidden-state omissions, model assumptions, independent training variability and the cost/information protocol needed for real deployment.
4. **How can switching create clustered volatility?** Persistent group shares alter conditional innovation variance under the complete state. Conditioning on a share alone may leave additional state-dependent variance. This is one possible mechanism, not unique identification of actual volatility.
5. **Why can a small common coefficient matter?** At N=100,w=0.2, common variance is 400 and private variance 64, giving 400/464≈86.2%. Private components diversify but do not cancel exactly. A +4 common increment adds eight baseline volatility units under the specified impact rule; it is not a frequency estimate.
6. **When does grim trigger sustain monopoly?** Under the theorem's game and monitoring assumptions, compare pi_c/(1−delta) with pi_d+delta pi_n/(1−delta). Rearrangement gives the stated threshold, about 0.3931 for the continuous logit benchmark.

## Twelve problems, with full solutions

The first six are foundations, the next four are advanced, and the last two are qualifying-exam problems.

1. **Foundations — volatility without linear return memory.** Let r_t=sigma_t epsilon_t. The epsilon are centred IID, independent of the entire volatility process, with finite moments. Let X_t=log sigma_t be stationary Gaussian AR(1), variance v>0 and coefficient 0<rho<1. Find the lag-h return and absolute-return covariance.

   **Solution.** For h>0, independence and E epsilon=0 give E[r_t r_(t−h)]=E[sigma_t sigma_(t−h)]E[epsilon_t epsilon_(t−h)]=0; the means are zero. Write m=E X and c_h=v rho^h. Gaussian exponential moments give E sigma=exp(m+v/2) and E[sigma_t sigma_(t−h)]=exp(2m+v+c_h). Thus Cov(sigma_t,sigma_(t−h))=exp(2m+v)(exp(c_h)−1)>0. Therefore Cov(|r_t|,|r_(t−h)|)=(E|epsilon|)^2 exp(2m+v)(exp(v rho^h)−1)>0. Positivity needs the stated rho and innovation independence; an arbitrary stochastic-volatility specification does not suffice.

2. **Foundations — the herding parameter.** N=50, epsilon=0.01 and delta=0.02. Compute alpha and interpret it.

   **Solution.** c=0.98/49=0.02 and alpha=epsilon/c=0.5. The beta-binomial is symmetric and endpoint-heavy; its fixed-alpha Beta limit is U-shaped. This describes the specified chain, not independent agents or an empirical investor estimate. Check the resulting up/down probabilities and remaining self-loop define a valid chain before simulation.

3. **Foundations — detailed balance.** Verify the beta-binomial law for the rates above.

   **Solution.** Adjacent beta-binomial masses satisfy pi(k+1)/pi(k)=(N−k)(alpha+k)/[(k+1)(alpha+N−k−1)], using the binomial and Beta-function recurrences. Dividing u(k) by d(k+1) yields exactly this ratio. Hence pi(k)u(k)=pi(k+1)d(k+1). The stated normalisation follows by summing the beta-binomial pmf. For positive rates the finite irreducible chain has this unique stationary law; self-loops satisfy balance automatically.

4. **Foundations — an isolated fill-income optimum.** Noise fill intensity is lambda exp(−kd), k>0. Maximise d lambda exp(−kd) over d≥0.

   **Solution.** The derivative is lambda exp(−kd)(1−kd), positive below 1/k and negative above it. Income is zero at d=0 and tends to zero at infinity, so d*=1/k is the global optimum for this isolated objective. At k=0.5 it is two ticks. Inventory, discrete actions, latent value and adverse selection alter the actual dealer problem; this derivative does not prove its optimum is two or three ticks.

5. **Foundations — what replay assumes.** A two-tick tape has n fills and score R. Explain the estimate R+2n for a four-tick rule.

   **Solution.** It assumes identical trade times, quantities, sides and subsequent inventory/value path, then adds two units per old fill. In the simple noise fill component, raising distance by two changes participation by exp(−2k), while informed fills and inventory also respond. Thus the fixed-fill construction does not identify the counterfactual. In the illustrated cache it is optimistic, about 445 versus 129. That sign is an observed feature here; absent further assumptions, replay bias has no universal sign.

6. **Foundations — symmetric logit Nash.** Let q_i=exp((a−p_i)/mu)/(exp((a−p_1)/mu)+exp((a−p_2)/mu)+exp(a_0/mu)), with a=2,a_0=0,mu=0.25,c=1. Derive and check the symmetric first-order condition.

   **Solution.** Partial q_i/partial p_i=−q_i(1−q_i)/mu. Differentiating (p_i−c)q_i gives q_i[1−(p_i−c)(1−q_i)/mu], so an interior best response satisfies p_i−c=mu/(1−q_i). At equal p≈1.472927, exp((2−p)/0.25)≈8.234 and q≈0.47136. Then 0.25/(1−q)≈0.472927=p−1. This checks the stated continuous symmetric benchmark; grid equilibria require discrete best-response comparisons.

7. **Advanced — punishment length.** Let pi_c=3,pi_d=4,pi_n=2. Find the grim threshold and whether one-period Nash punishment can work for delta<1.

   **Solution.** Grim gives (4−3)/(4−2)=1/2. For T=1, the incentive condition is 1≤delta(3−2)=delta, impossible for delta<1. For a general T it is 1≤sum_(j=1)^T delta^j. A feasible finite threshold requires T>1. The off-path rule must be specified, for example restarting the Nash-punishment clock on any further deviation; under the assumed ordering, this prevents gain during punishment.

8. **Advanced — half common.** Under the independent unit-variance signal assumptions, solve C=1/2 for w in [0,1].

   **Solution.** Equality requires Nw²=(1−w)². Taking nonnegative square roots gives sqrt(N)w=1−w, so w=1/(1+sqrt(N)). For N=100 it is 1/11≈0.09091. This is a coefficient threshold for a variance fraction; no statement about realised order-volume shares follows. Differentiating total variance gives its different minimum w=1/(N+1).

9. **Advanced — an inserted common increment.** With return r=(kappa/sqrt(N)) sum_i x_i, add e to the existing common signal, holding the private components fixed. Express the added return in zero-common volatility units.

   **Solution.** Aggregate flow increases by Nwe, so Delta r=kappa sqrt(N)we. At w=0, Var(r)=kappa² under independent unit-variance private signals. For kappa>0, the ratio to that standard deviation is sqrt(N)we. N=100,w=0.2,e=4 gives eight. The selected total return also contains the original common and private noise. The sign follows e; the construction supplies no event probability and is not necessarily a crash.

10. **Advanced — a positive index with zero discounting.** Explain why a finite-grid learner can exceed a continuous Nash profit reference without a repeated-game equilibrium.

    **Solution.** First, discretisation changes best responses and one-shot equilibria: the listed grid indices are about −0.0238 and 0.1166, so one grid equilibrium is already above the continuous reference. Second, finite learning, exploration, coupled value estimates and state visitation can prevent convergence to any equilibrium. Here about 88.5% of reported myopic sessions exceed the higher listed grid-equilibrium index. That statistic does not identify one causal mechanism. At delta=0, any frozen outcome with a profitable current deviation is not a stage-game Nash equilibrium, whatever its reported profit index.

11. **Qualifying — one-shot deviations and trigger strategies.** State the assumptions, prove the principle, then derive grim and finite-punishment incentives.

    **Solution.** Consider a standard perfectly monitored discounted repeated game, with |stage payoff|≤M and delta<1, and strategies defined after every history. If a continuation deviation gains epsilon>0, truncating it after T periods changes its value by at most 2M delta^T/(1−delta). Choose T to make this below epsilon, retaining a profitable finite deviation. If every one-shot deviation is unprofitable after every history, remove its last deviating date without decreasing expected payoff, including at histories reached off the original path. Repeat backwards through the finite horizon. The resulting baseline strategy cannot be strictly worse, a contradiction. Necessity follows because a one-shot deviation is itself a permitted deviation. For grim trigger, off-path repetition of static Nash is credible. On-path compliance gives pi_c/(1−delta); deviation gives at most pi_d+delta pi_n/(1−delta), yielding delta≥(pi_d−pi_c)/(pi_d−pi_n). For Nash punishment lasting T periods and restarting after any deviation, on-path payoff loss is (pi_c−pi_n)sum_(j=1)^T delta^j. Comparing it with pi_d−pi_c gives the finite condition. During punishment, a unilateral deviation cannot improve current Nash profit and restarts a weakly worse continuation. Domain consistency and public detection are essential; a visually similar learned response does not establish these constraints.

12. **Qualifying — the complete stationary law and population limit.** Derive the law, prove the fixed-alpha limit and find unanimity's asymptotic probability.

    **Solution.** Detailed balance gives the ratio and normalised beta-binomial pmf in problem 3. A convenient complete limit proof uses its mixture representation: draw P~Beta(alpha,alpha), then K_N|P~Binomial(N,P). Conditional variance of K_N/N is P(1−P)/N, so E[(K_N/N−P)²]≤1/(4N). Thus K_N/N converges to P in L² under this coupling, hence in distribution. This proof includes endpoint behaviour, rather than relying only on an interior Stirling approximation. For fixed alpha>0, pi(0)=B(alpha,N+alpha)/B(alpha,alpha)=Gamma(2alpha)Gamma(N+alpha)/[Gamma(alpha)Gamma(N+2alpha)]. Symmetry doubles this value for unanimity. The gamma-ratio asymptotic gives 2 Gamma(2alpha)/Gamma(alpha) N^(−alpha). In the microscopic chain, hold alpha fixed by taking epsilon=(1−delta)alpha/(N−1), with valid rates. Fixing epsilon instead would change alpha and invalidate this limit statement.

## Sources and reproducibility

The displayed numerical algorithms remain in `compute.py` and `explainer/quant/house/agents.py`. Ordinary cache reads in `common.py` require the seven audited names and exact output hashes before the counted loader can run. Unknown, missing, changed or excluded outputs cannot trigger implicit computation. Do not rerun the once-only original dispatcher to rebuild presentation evidence.

Selected sources: Kirman (1993); Gode and Sunder (1993); Arthur et al. (1997); Brock and Hommes (1997, 1998); Lux and Marchesi (1999); Bikhchandani, Hirshleifer and Welch (1992); Franke and Westerhoff (2012); Byrd, Hybinette and Balch (2020); Vyetrenko et al. (2020); Hambly, Xu and Yang (2023); Levine et al. (2020); Calvano et al. (2020); Friedman (1971); Abreu (1988); Banchio and Mantegazza (2023). Published papers describe their own settings; these simulations are limited reproductions, not exact replications of every experiment.

Official historical sources reviewed for this revision:

- [IMF, October 2024 Global Financial Stability Report](https://www.imf.org/en/Publications/GFSR/Issues/2024/10/22/global-financial-stability-report-october-2024).
- [FSB, 14 November 2024 AI assessment](https://www.fsb.org/2024/11/fsb-assesses-the-financial-stability-implications-of-artificial-intelligence/).
- [EU algorithmic-trading organisational requirements, Regulation 2017/589](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32017R0589) and [ESMA kill-functionality clarification](https://www.esma.europa.eu/publications-data/questions-answers/1612).
- [EU AI Act, Regulation 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj), including scope, application dates and Annex III examples. These examples do not categorically exempt trading.
- [SEC's 2013 Knight Capital findings](https://www.sec.gov/newsroom/press-releases/2013-222): deployment/routing failure and losses above $460 million, distinct from a liquidity-withdrawal mechanism.
- [2015 joint Treasury-market staff report](https://home.treasury.gov/system/files/136/archive-documents/Joint_Staff_Report_Treasury_10-15-2014.pdf): the narrow October 2014 event window and multiple contributing market features.
- [SEC's June 2025 predictive-analytics proposal withdrawal](https://www.sec.gov/rules-regulations/2025/06/s7-12-23). A historical withdrawal is not a complete statement of applicable duties.

---

# 量化金融，从零搭建 — 第42部分：市场中的机器

这是四十三部分系列的第42部分，研究交易规则、学习和共同输入如何通过市场相互作用。模拟器能证明一种机制存在，却不能单凭相似图形识别真实价格的成因。这个区别贯穿人工市场、羊群链、交易商学习者、定价博弈和共同信号群体。

唯一下载的市场输入是肯尼斯·弗伦奇截至二〇二〇年的日频研究窗口数据。其余数字来自原有固定种子模拟或代数。七项经审计的普通计算各成功调用一次，没有修改金融算法或 `compute.py`，没有登记新的市场试验，没有打开封存策略结果，也没有执行语言模型交易者。

## 章节与适用范围

| 章节 | 关键区别 |
|---|---|
| 开场 | 利润插值指数、交互执行与方差份额不是同一种量。 |
| 1. 人工市场 | 选定模型能产生厚尾和波动聚集；八十一点原始矩网格不构成样本外验证或唯一机制识别。 |
| 2. 羊群效应 | 精确贝塔二项平稳分布；固定阿尔法的极限要求自发切换率随人数缩放；采样越界不同于精确状态通过时间。 |
| 3. 模拟器 | ABIDES、响应指标与卢卡斯批判；模型反事实依赖假设，有目标函数也不自动获得真实因果有效性。 |
| 4. 学习交易 | 三十九种压缩观测不是完全可观测状态；得分含库存惩罚；单个训练种子和恒定步长不证明收敛或普遍优劣。 |
| 5. 语言模型 | 历史污染是可能性，不是必然；合成新颖性不足以构成干净推理测试；仍需时间、版本与试验纪律。 |
| 6. 定价算法 | 十五价格、有限训练；惩罚比例以固定点子样本为条件；两百步搜索不足以保证发现两百二十五状态中的循环。 |
| 7. 共同信号 | 独立单位方差分量下，人数一百、共同系数点二给出约百分之八十六的总方差；人为正向增量不是崩盘频率。 |
| 8. 金融稳定 | 二〇二四年监管报告与选定历史规则；不同操作或流动性事件不能归为同一已证原因。 |
| 9. 第42条规则 | 建议的压力测试与治理，而非已完成的部署批准。 |
| 研究章 | 完美监测、统一动作域下的冷酷触发及有限惩罚；与离散学习、混合动作域的示例比率区分。 |
| 结尾 | 六个交易台问题和十二道完整解答习题。 |

## 机制、公式与限制

柯曼链要求 N>1、epsilon>0、0≤delta<1，且转移概率有效。记 c=(1−delta)/(N−1)、alpha=epsilon/c，则

\[
 u(k)=\frac{N-k}{N}c(\alpha+k),\quad d(k)=\frac{k}{N}c(\alpha+N-k).
\]

自发切换与模仿是相加的，余下概率是停留。细致平衡得到

\[
 \pi(k)=\binom Nk B(k+\alpha,N-k+\alpha)/B(\alpha,\alpha).
\]

固定 alpha 时，份额收敛到 Beta(alpha,alpha)，完全一致概率渐近为 2Gamma(2alpha)/Gamma(alpha)·N^(−alpha)。这需要 epsilon 随 N−1 的倒数缩放。固定 epsilon 是另一种极限。每十步检查“至少九十到不超过十”的采样通过时间，包含延迟与越界，不等于精确九十到十的理论量。

交易商中的知情者看到当前潜在价值，不知道下一次创新；创新发生在交易决策后。库存和上一笔方向遗漏中价与价值的缺口，因此有隐藏状态混叠。得分是潜在价值计价损益减库存惩罚，不只是现金利润。最佳测试固定规则是有限网格选择，不是独立确认的全局最优。沿用固定成交记录不能重现新报价下的成交。序贯重要性评估需要重叠、可靠倾向概率和适当识别假设；概率比连乘可能方差极大。

定价指数是“利润减纳什利润”除以“垄断利润减纳什利润”，不是价格差距百分比。惩罚比例以固定点子样本为条件；均值恢复不代表每场恢复。独立加性利润噪声不是逆向选择。高价与报复是协调诊断，不证明子博弈完美均衡或法律协议。二〇二四年八月RealPage起诉仅作为当时的指控引用，不说明案件当前程序状态。

重复博弈定理假设统一动作域、完美公开监测、有界收益、0≤delta<1，且 pi_d>pi_c>pi_n，静态纳什惩罚可信。冷酷触发成立当且仅当

\[
 \delta\ge(\pi_d-\pi_c)/(\pi_d-\pi_n).
\]

有限T期纳什惩罚必须规定：惩罚中再次偏离就重新计时。合作路径的条件为

\[
 \pi_d-\pi_c\le(\pi_c-\pi_n)\sum_{j=1}^{T}\delta^j.
\]

存在严格小于一的阈值，需要 T(pi_c−pi_n)>pi_d−pi_c。惩罚期里，纳什最佳响应阻止当前收益提高，重启又推迟较好的延续。连续logit基准的冷酷阈值约0.3931；T为1、2、3、5时分别为0.6477、0.4475、0.4103、0.3954。这些数不自动认证十五价格学习者。

纯网格“最小最佳响应”值0.2041，与连续合作和偏离利润组合，得到示例比率0.3574。动作域混合，因此它不是一般阿布鲁界、混合动作最小最大值，也不是已证明可达到的惩罚机制。可信延续与一致动作域须另外分析。

共同信号模型 x_i=w s+(1−w)e_i 中，信号分量相互独立、均值零、方差一；订单本身相关。总方差为 N²w²+N(1−w)²，共同方差份额为 Nw²/[Nw²+(1−w)²]。这不是实际成交份额。总方差在 w=1/(N+1) 最小，并非从零起单调增加。模拟五千观测中含一次人为冲击，理论线则使用未改动的信号。所选日是在已有随机共同信号上加正四；在 kappa/sqrt(N) 冲击规则下，额外收益为 kappa sqrt(N)w·4。人数一百、权重点二时为八个零共同基准波动单位。总收益还包括原随机分量；w=0时也有私有订单收益。订单流因子份额还需因子与残差正交，共享新闻或再平衡也能造成共同变化，不能直接归因人工智能。

## 六个交易台问题与完整解答

1. **宽价差和被迫降价后的响应证明合谋吗？** 不证明。它们提示应检查个体策略、相关历史处有利偏离、信息交换和适用法律。固定点子样本的条件惩罚比例不能支持普遍的经济或法律结论。
2. **行情记录为什么不是新报价策略的环境？** 报价改变参与率和逆向选择。每笔旧成交加两跳，固定了对手反应，并未重建宽报价会收到的成交。示例回放约445，交互模拟约129；这里的“实时”指模拟交互，不是真实资金交易。
3. **模拟器训练的策略应面对什么？** 不同环境、对手、复制品，以及干预响应指标，不只是无条件矩。还应说明隐藏状态遗漏、识别假设、独立训练变异，以及实际部署所需信息和成本协议。
4. **切换怎样聚集波动？** 完整状态下，持续的群体份额改变创新方差。只给定份额仍可能遗漏其他状态变化。这是一种可能机制，不是对真实波动的唯一识别。
5. **小共同系数为何重要？** 人数一百、权重点二时，共同方差400，私有方差64，比例400/464≈86.2%。私有分量部分分散，不精确抵消。指定冲击规则下，正四增量增加八个基准波动单位，不提供频率。
6. **冷酷触发何时维持垄断？** 在定理假设下，比较 pi_c/(1−delta) 与 pi_d+delta pi_n/(1−delta)，整理得阈值；连续logit示例约0.3931。

## 十二道习题与完整解答

前六道为基础，接着四道为进阶，最后两道为资格考试题。

1. **基础：收益无线性记忆，幅度却有。** 设 r_t=sigma_t epsilon_t，epsilon 独立同分布、均值零、与整个波动过程独立，且相关矩存在。X_t=log sigma_t 是平稳高斯AR(1)，均值m、方差v>0、系数0<rho<1。求h>0的两种协方差。

   **解：** E[r_t r_(t−h)]=E[sigma_t sigma_(t−h)]E[epsilon_t epsilon_(t−h)]=0，收益均值也为零。记 c_h=v rho^h，高斯指数矩给出 E sigma=exp(m+v/2)，E[sigma_t sigma_(t−h)]=exp(2m+v+c_h)。因此波动协方差为 exp(2m+v)(exp(c_h)−1)>0，绝对收益协方差是它乘(E|epsilon|)²。这依赖正rho和创新独立性，不能对任意随机波动过程直接声称正相关。

2. **基础：羊群参数。** N=50、epsilon=0.01、delta=0.02，求alpha并解释。

   **解：** c=0.98/49=0.02，alpha=epsilon/c=0.5。对称贝塔二项分布更偏两端，固定alpha的贝塔极限呈U形。这是指定链的结论，不代表独立参与者或实际投资者估计；还须确认上、下和停留概率构成有效链。

3. **基础：细致平衡。** 验证贝塔二项平稳分布。

   **解：** 二项系数和贝塔函数递推给出 pi(k+1)/pi(k)=(N−k)(alpha+k)/[(k+1)(alpha+N−k−1)]。计算u(k)/d(k+1)得到同一比率，故相邻细致平衡成立。贝塔二项概率总和为一，提供归一化。有限不可约链的平稳分布唯一，停留项自动满足平衡。

4. **基础：单独的成交收入最优值。** 最大化 d lambda exp(−kd)，其中d≥0、k>0。

   **解：** 导数是 lambda exp(−kd)(1−kd)，在1/k以下为正、以上为负。零点与无穷远收入为零，所以d*=1/k是这个独立目标的全局最优；k=0.5时为两跳。库存、离散动作、潜在价值与逆向选择会改变完整交易商问题，不能由此证明其最优为两跳或三跳。

5. **基础：回放到底假设什么？** 两跳行情有n笔成交、得分R，解释四跳估计R+2n。

   **解：** 它固定时间、数量、方向，以及后续库存和价值路径，然后每笔加两单位。噪声成交分量在距离增加两跳后乘exp(−2k)，知情成交与库存也会响应。因此它不识别反事实。所示缓存例子中，约445比129乐观；这是该例结果，没有额外假设时，回放偏差方向并非普遍固定。

6. **基础：对称logit纳什。** 取a=2、a_0=0、mu=0.25、c=1，推导并检查连续对称一阶条件。

   **解：** q_i为正文logit份额，有偏导 dq_i/dp_i=−q_i(1−q_i)/mu。利润(p_i−c)q_i的导数为 q_i[1−(p_i−c)(1−q_i)/mu]，内点条件是p_i−c=mu/(1−q_i)。对称p≈1.472927时，exp((2−p)/0.25)约8.234，q约0.47136，0.25/(1−q)约0.472927，等于p−1。这验证连续基准；网格均衡需要离散最佳响应比较。

7. **进阶：惩罚长度。** pi_c=3、pi_d=4、pi_n=2，求冷酷阈值与一期惩罚可行性。

   **解：** 冷酷阈值(4−3)/(4−2)=1/2。T=1时要求1≤delta，对delta<1不可能。一般T要求1≤sum_(j=1)^T delta^j；小于一的有限阈值要求T>1。还须规定路径外规则，例如再次偏离就重启纳什惩罚时钟；在给定收益排序下，这阻止惩罚期间获利。

8. **进阶：一半方差共同。** 在独立单位方差信号假设下解共同份额为二分之一。

   **解：** Nw²=(1−w)²，非负平方根给出sqrt(N)w=1−w，所以w=1/(1+sqrt(N))。N=100时为1/11≈0.09091。这是方差份额的系数阈值，不是已实现成交量比例。总方差求导得到另一个位置：最小值在1/(N+1)。

9. **进阶：共同信号增量。** 收益为(kappa/sqrt(N))sum_i x_i，在已有共同信号上加e、固定私有信号，以零共同波动为单位求增量。

   **解：** 总订单增加Nwe，收益增加kappa sqrt(N)we。w=0时收益方差kappa²；kappa>0时标准化增量为sqrt(N)we。N=100、w=0.2、e=4得到八。所选日总收益还含原共同与私有噪声；符号随e，不提供事件概率，也不必是崩盘。

10. **进阶：零折扣为何也可有正指数？** 解释有限网格学习者高于连续纳什参考，却不构成重复博弈均衡。

    **解：** 第一，离散化改变最佳响应和单期均衡；列出网格指数约−0.0238和0.1166，其中一个已高于连续参考。第二，有限学习、探索、耦合估计和访问分布可能阻碍到达任何均衡。这里约88.5%的短视场次指数高于较高网格均衡，统计本身不识别原因。delta=0时，只要有利的当前偏离存在，冻结结果就不是单期纳什，无论利润指数多高。

11. **资格考试：单次偏离与触发策略。** 说明假设、证明原则并推导两类激励条件。

    **解：** 标准完美监测折扣重复博弈中，各期收益绝对值≤M、delta<1，策略定义于每个历史。若某延续偏离获益epsilon>0，T期后截断的收益变化≤2M delta^T/(1−delta)，选足够大T保留正收益。若任何历史处单次偏离都不盈利，就能不降低期望收益地删除最后一个偏离日期，包括原路径外历史，再向前删除全部有限偏离，得到矛盾。必要性直接来自单次偏离也是合法偏离。冷酷策略路径外重复静态纳什可信；路径上比较pi_c/(1−delta)与pi_d+delta pi_n/(1−delta)，整理得阈值。T期惩罚且再次偏离重启时，合作路径损失为(pi_c−pi_n)sum_(j=1)^T delta^j，需不小于pi_d−pi_c。惩罚中当前纳什利润无法单独提高，重启又延迟更优延续。动作域一致和公开检测十分关键，学习响应外观相似不验证这些约束。

12. **资格考试：完整平稳律与人口极限。** 推导分布，证明固定alpha极限与完全一致概率。

    **解：** 第三题细致平衡给出归一化贝塔二项分布。完整极限证明可用混合表示：先抽P~Beta(alpha,alpha)，再令K_N|P~Binomial(N,P)。条件方差为P(1−P)/N，故E[(K_N/N−P)²]≤1/(4N)，在该耦合下均方收敛，从而分布收敛。这个证明包含边界行为，不只依赖内点斯特林近似。固定alpha>0时，pi(0)=Gamma(2alpha)Gamma(N+alpha)/[Gamma(alpha)Gamma(N+2alpha)]，对称性让完全一致概率加倍。伽马比渐近给出2Gamma(2alpha)/Gamma(alpha)·N^(−alpha)。微观链中需取epsilon=(1−delta)alpha/(N−1)，并保证概率有效；若固定epsilon，alpha会变，不能使用这个固定参数极限。

## 来源与复现

金融算法保留原样。`common.py`只允许七个经审计名称及其精确缓存哈希；未知、缺失、更改或排除项目在路径或计数访问前被阻止，不会隐式计算。不要再次运行已完成的一次性原始计算调度器来重建演示。

上方英文来源区给出论文和官方历史链接。二〇二四年IMF、FSB报告是当时潜在脆弱性与数据缺口的评估；欧盟规则适用范围、人工智能法的分阶段实施与美国具体市场准入义务需分别分析。SEC二〇一三年Knight报告描述部署路由故障及超过四亿六千万美元损失，不是所有事件都属流动性撤走。二〇一四年国债十二分钟事件的“没有明显新公开催化信息”只针对该窗口。二〇二五年预测分析提案撤回，不等于其他责任消失。以上是教学历史材料，不是当前完整法律意见。

## Current visual review

The current visual pass is complete at fingerprint `d484a049dc426860456a804f467bf46e8c96b99bb07bf33b143249933e99bf94`. All 24 bilingual endpoint sheets, twelve English forty-frame motion sheets, scene-native frames, exact flagged/manual concern intervals, current bilingual construction captures and the narrated opening were actually inspected. The versioned evidence is `docs/qa/quant42-polish-evidence.json`; generated artifacts and the twelve-chapter silent timing preview remain in the workspace. Eleven actual CPU speech reports check sampled signal/timing. Full continuous production-voice listening, pronunciation and mastering remain separately pending. Dense derivations/references and brief staged entrances/page fades remain documented presentation limitations.

当前视觉检查已完成：已实际查看全部二十四张双语端点图、十二张英文四十帧运动图、每个场景的原始帧、自动标记与人工发现问题的精确区间，以及当前双语构建图和带旁白开场。证据文件为 `docs/qa/quant42-polish-evidence.json`。十一份实际CPU语音报告检查抽样信号和时序；完整制作语音的连续听审、发音审查和母带制作仍单独待做。密集推导与参考文字、短暂分阶段入场和页面淡出保留为已记录的呈现限制。
