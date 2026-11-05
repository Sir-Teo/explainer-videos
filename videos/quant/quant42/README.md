# Quant, Built — Part 42: Machines in the Market

Part 42 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third part of Act VII, The System, built to the series' PhD layer. It asks what
happens when the traders are programs that learn, and the market is made of them.

Data: Kenneth French's daily US market return, 1926–2020, for the stylised facts and the simulated-moments fit; the
research window only, and the sealed hold-out is not opened. Everything else is simulation with fixed seeds, in the
House's new `explainer/quant/house/agents.py`:
* a Franke–Westerhoff-type market of fundamentalists and chartists who switch by herding and by mispricing;
* Kirman's ant model, with its exact stationary law and passage times;
* Bikhchandani–Hirshleifer–Welch information cascades;
* a Glosten–Milgrom dealer market with an exponential fill law and a tabular Q-learning market maker;
* Calvano–Calzolari–Denicolò–Pastorello's logit pricing game, with 96 sessions of 1.5 million periods per setting;
* a crowd mixing a shared model's signal with its own.

No language model was run, as a trader or otherwise (Chapter 5 explains why), and nothing here is investment advice.
Papers and cases are cited as reported; the RealPage case is an allegation.

## Chapters (about 53 minutes)

| | Chapter | What it shows |
|---|---|---|
| 0 | Hook | four findings; the desk question; Act VII; thirty years of machines in markets |
| 1 | Artificial markets | the Santa Fe market; a fundamentalist–chartist market with herding; stylised facts (kurtosis 16.7 real, 5.0 agents, 0 Gaussian; lag-20 \|r\| autocorrelation 0.23, 0.23, 0.00); simulated moments (best kurtosis 7.1; the extrapolation parameter unidentified); Brock–Hommes; zero intelligence |
| 2 | Herding | Kirman's ants; the theorem: the stationary law is exactly beta-binomial(N, α, α), α = ε(N − 1)/(1 − δ), proved; checked (TV 0.009, 0.005); swing times 52,945 against 52,128 simulated; unanimity 38% at N = 100, falling like N^−α; a herding market; Lux–Marchesi; LSV; cascades: wrong with probability q²/(p² + q²), 15.5% at p = 0.7 (15.7% simulated) |
| 3 | Simulators | ABIDES; realism metrics; simulated moments and learned simulators; the three gaps (artefacts, the counterfactual, adaptation); the Lucas critique; the House's dealer market and what it leaves out |
| 4 | Learning to trade | RL in finance; the maker's MDP; a sample session; every fixed rule (best: three ticks, skewed, 157 at 15% informed); learners at 85% of the best rule, and no better when trained in the right regime (88 against 89 at 30% informed; the best rule 113); the learning curve wanders; model-based quotes; the replay bias (445 predicted, 129 live); offline RL; why a table |
| 5 | Language models as traders | readers, planners, populations; simulators as a clean bench; what an honest test needs; chronological consistency; shared foundation models; what LLM traders could do to markets; what the House did not do |
| 6 | Algorithmic collusion | the logit game (p^N = 1.473, p^M = 1.925); Q-learners: collusion index 0.23 (δ = 0) to 0.81 (δ = 0.95); per-session prices; 95% of fixed-point sessions punish a forced undercut and all return; the average impulse response; Colliard–Foucault–Lovo, Dou–Goldstein–Ji; profit noise lowers the index to 0.43; facilitating factors; 1 − 1/n; the law (Harrington); Assad et al.; RealPage (alleged) |
| 7 | When everyone shares a model | Gensler–Bailey; Danielsson–Macrae–Uthemann; the common share Nw²/(Nw² + (1 − w)²), 86% at w = 0.2; volatility 2.2× and a model error 11× the diverse market's daily volatility; measuring it from flows; diversity as a public good |
| 8 | AI and financial stability | IMF (October 2024) and FSB (November 2024); MiFID II RTS 6, the market access rule, the EU AI Act, the withdrawn SEC proposal; Moore vs Murphy; machine-speed failures; model risk management; three layers of controls |
| 9 | Rule 42 | four tests; the scorecard; the collusion audit; governance; the agent registry; the House's code |
| R | For the researcher | the stage-game numbers; the one-shot deviation principle with a proof sketch; grim trigger proved; the T-period corollary; thresholds for the logit game (0.39; T = 1: 0.65, T = 5: 0.40); Abreu's minmax bound 0.36; the learners against the threshold; learned punishments; spontaneous coupling; the folk theorem, Green–Porter, Brown–MacKay; open problems |
| 10 | Outro | thirteen lines, lessons, formulas, desk questions, problems, references |

## For the researcher

* **Theorem (herding's stationary law).** Kirman's chain on k ∈ {0, …, N}: each step one agent switches alone with
  probability ε or is converted by a random other with probability 1 − δ. Its stationary law is exactly
  beta-binomial(N, α, α) with α = ε(N − 1)/(1 − δ).
  * **Proof.** A birth–death chain is reversible, so π(k + 1)/π(k) = u(k)/d(k + 1). With c = (1 − δ)/(N − 1):
    u(k) = (1 − k/N)c(α + k) and d(k + 1) = ((k + 1)/N)c(α + N − k − 1). The ratio is
    (N − k)(α + k)/((k + 1)(α + N − k − 1)), the beta-binomial's.
  * **Corollary.** k/N → Beta(α, α), U-shaped iff α < 1. P(k ∈ {0, N}) ~ 2Γ(2α)/Γ(α) · N^−α.
  * **Mean passage times.** m_k = (1 + u(k)m_{k+1})/d(k) and E T_{a→b} = Σ_{k=b+1}^{a} m_k.
* **Theorem (grim trigger; Friedman 1971).** In the infinitely repeated stage game with collusive, deviation and Nash
  profits π^c < π^d and π^n < π^c, grim trigger is subgame perfect iff δ ≥ (π^d − π^c)/(π^d − π^n).
  * **Proof** by the one-shot deviation principle. Off the path, repeated static Nash is subgame perfect. On the path,
    π^c/(1 − δ) ≥ π^d + δπ^n/(1 − δ).
  * **The one-shot deviation principle**, sketched. A profitable deviation gaining ε can be truncated after T periods
    at a loss of at most 2Mδ^T/(1 − δ). The shortest profitable deviation's last step is a profitable one-shot
    deviation.
  * **Corollary (T-period punishment).** It deters iff π^d − π^c ≤ (π^c − π^n)(δ + … + δ^T).
  * **Abreu's bound.** No punishment beats the minmax profit, so δ ≥ (π^d − π^c)/(π^d − π_minmax) is necessary for any
    scheme.
* **Measured.**
  * **Thresholds.** For the logit game at monopoly: grim 0.393; T = 1, 2, 3, 5: 0.648, 0.447, 0.410, 0.395; Abreu
    0.357.
  * **The learners.** At δ = 0.5, above the threshold, the collusion index is 0.21; it is 0.70 at 0.9 and 0.81 at
    0.95. Learning needs far more patience than equilibrium does.
  * **Punishments.** The learners punish for about 5 periods, and a 5-period punishment needs δ ≥ 0.395.
  * **Myopic learners (δ = 0)** end at a median index of 0.24. The grid has one-shot equilibria at −0.02 and 0.12;
    89% of sessions end above both.
* **Simplifications.**
  * One-period memory and 15 prices.
  * Tabular learners.
  * A dealer market with one maker and no book.
  * Stylised parameters.
* **Open problems.**
  * A theory of which equilibria learners reach.
  * Detecting learned collusion from data.
  * Market designs that defeat it.
  * Measuring model monoculture.

## Build it

```bash
python -m videos.quant.quant42.compute                            # every item; about 15 minutes (collusion and the maker)
python -m pytest -q tests/test_quant_house.py -k agents
EXPLAINER_TTS=silent python tools/qa_scene.py quant42 Research     # one chapter, silent, with a contact sheet
python tools/build.py quant42                                      # the narrated part
```

## Desk questions, with solutions

1. **Two algorithms that never communicate end up quoting wide spreads. Is that collusion?**
   * Economically, it is collusion if supra-competitive prices are sustained by reward and punishment. Test it by
     forcing one algorithm to undercut once: here 95% of sessions punish and all return.
   * Legally, competition law mostly prohibits agreements, and tacit coordination is generally lawful. Whether
     learned coordination is an agreement is open (Harrington 2018).
2. **Why is a backtest not an environment for a market maker?**
   * Its quotes change who trades with it.
   * Replaying a two-tick rule's fills at four-tick prices predicts 445 per session; live, the four-tick rule earns
     129.
3. **Your agent was trained in a simulator. What would you check?**
   * Responses to orders, not only stylised facts.
   * Regimes and rivals it never saw.
   * The simulator's identifying assumptions: here two moments identified only one of two behaviours.
4. **How does herding produce volatility clustering?**
   * The chartists' share moves slowly because each switch depends on the others', and variance rises with that
     share.
5. **A fifth of every order comes from one model. Why does it matter?**
   * The shared parts add coherently, so the common share is 4/4.64 = 86% for 100 traders.
   * A 4σ model error moves the market about √N·w·4 = 8 diverse-market daily vols in expectation; 11 here.
6. **When can grim trigger sustain the monopoly price?**
   * When δ ≥ (π^d − π^c)/(π^d − π^n) = 0.39 in this part's logit game.

## Problems, with solutions

1. **Size is predictable when returns are not.**
   * Cov(r_t, r_{t−k}) = E[σ_tσ_{t−k}]E[ε_tε_{t−k}] = 0.
   * Cov(|r_t|, |r_{t−k}|) = (E|ε|)² Cov(σ_t, σ_{t−k}) > 0, because log σ is a positively autocorrelated AR(1).
2. **Kirman's α.** α = 0.01 × 49/0.98 = 0.5 < 1: the crowd herds, and its law is U-shaped.
3. **Detailed balance.** Substitute u(k) and d(k + 1) as in the theorem. The ratio equals the beta-binomial's
   π(k + 1)/π(k) = (N − k)(α + k)/((k + 1)(α + N − k − 1)).
4. **The best spread.** Maximise dλe^{−kd}: d* = 1/k, which is 2 ticks at k = 0.5. Adverse selection widens it,
   to 3 here.
5. **The replay bias.** R + 2n assumes the same n fills at the wider quote. But noise fills fall by a factor e^{−2k}
   and informed fills change, so the estimate is biased upward. Here it is 445 against 129.
6. **The logit Nash price.** The first-order condition is p − c = μ/(1 − q). At p = 1.473, q = e^{2.108}/(2e^{2.108} + 1)
   = 0.471, so μ/(1 − q) = 0.473 = p − c.
7. **Thresholds.** Grim: (4 − 3)/(4 − 2) = 0.5. One period: 1 ≤ δ, so no δ < 1 deters with a one-period punishment.
8. **Half common.** Nw² = (1 − w)², so w = 1/(1 + √N) = 1/11 ≈ 0.091.
9. **A model error.** The expected extra move is κ√N·w·e in units where the diverse market's daily vol is κ: a ratio
   of √N·w·e. That is 8 for N = 100, w = 0.2 and e = 4.
10. **Collusion on a grid at δ = 0.**
    * The discretised one-shot game has equilibria above the continuous Nash price: indices of −0.02 and 0.12 here.
    * ε-greedy learners' estimates couple (Banchio–Mantegazza), holding prices higher still: 89% of sessions end above
      0.12.
11. **(qual) The one-shot deviation principle and grim trigger.**
    * Let σ be a profile with no profitable one-shot deviation, and suppose σ' gains ε > 0 at some history.
    * Payoffs are bounded by M, so the version of σ' that reverts to σ after T periods gains at least
      ε − 2Mδ^T/(1 − δ) > 0 for large T.
    * Among finite profitable deviations take one of minimal length. At its last deviating history, deviating once and
      returning gains, otherwise dropping that step would leave a shorter profitable deviation. This contradicts the
      hypothesis.
    * Grim trigger and the T-period corollary then follow by comparing the two payoff streams at a single history.
12. **(qual) Kirman's law in full.**
    * The beta-binomial law follows by detailed balance, as above.
    * Convergence: by Stirling, C(N, k)B(k + α, N − k + α) ~ N^{−1} x^{α−1}(1 − x)^{α−1} uniformly on compacts of
      (0, 1), with x = k/N. So the share converges in law to Beta(α, α).
    * Unanimity: π(0) = B(α, N + α)/B(α, α) = Γ(2α)Γ(N + α)/(Γ(α)Γ(N + 2α)) ~ Γ(2α)/Γ(α) · N^{−α}.

## Data and reproducibility

* Kenneth French's daily factors (through 2020), cached and checksummed in `videos/quant/data/manifest.json`.
* Every simulation uses fixed seeds. Every figure comes from `compute.py`, cached in `.cache/quant42/`, and from
  `explainer/quant/house/agents.py`.
* The Calvano et al. design (logit demand a = 2, a₀ = 0, μ = 0.25, c = 1; 15 prices with ξ = 0.1; α = 0.15;
  β = 4×10⁻⁶) follows the published paper.

---

# 量化金融，从零搭建 — 第42部分：市场中的机器

本系列共四十三部分，这是第42部分，属于第七幕“体系”的第三部分，按博士层标准构建。它追问：当交易者是会学习的程序、市场由它们组成时，会发生什么。
数据只有肯尼斯·弗伦奇1926—2020年的美国市场日收益（研究窗口内，样本外数据未打开）；其余全部是随机种子固定的模拟，代码在本系列公司新的
`explainer/quant/house/agents.py`中。本部分没有运行任何语言模型。论文和案件按报道引用，RealPage案仅为指控。这里的内容不构成投资建议。

## 章节（约53分钟）

| | 章节 | 内容 |
|---|---|---|
| 0 | 开场 | 四个发现；交易台问题；三十年的市场机器 |
| 1 | 人工市场 | 圣塔菲市场；带羊群效应的基本面—图表交易者市场；典型事实；模拟矩方法（外推参数不可识别）；布洛克—霍姆斯；零智能 |
| 2 | 羊群效应 | 柯曼的蚂蚁；定理：平稳分布恰为贝塔二项分布，给出证明与检验；摆动时间；N = 100时38%的时间完全一致；信息瀑布：p = 0.7时错误概率15.5% |
| 3 | 模拟器 | ABIDES；真实性指标；三种差距；卢卡斯批判；本系列公司的交易商市场 |
| 4 | 学习交易 | 学习者达到最好固定规则的约85%；在正确的状态里训练也没有更好；学习曲线游荡不定；回放偏差（预测445，实盘129）；离线强化学习 |
| 5 | 作为交易者的语言模型 | 用法、诚实检验的要求、时间一致性、共享基础模型；本系列公司没有做什么 |
| 6 | 算法合谋 | 合谋指数从0.23（δ = 0）到0.81（δ = 0.95）；95%的场次惩罚被迫降价；利润噪声使指数降到0.43；1 − 1/n；法律与案例 |
| 7 | 当所有人共用一个模型 | 共同份额Nw²/(Nw² + (1 − w)²)，w = 0.2时为86%；模型错误造成11倍的波动 |
| 8 | 人工智能与金融稳定 | IMF与FSB报告；现有规则；摩尔对墨菲；机器速度的失败；模型风险管理 |
| 9 | 第42条规则 | 四项检验；记分卡；合谋审计；治理；智能体登记簿 |
| R | 写给研究者 | 单次偏离原则；冷酷触发定理及证明；T期推论；阿布鲁界；与学习者对照 |
| 10 | 结尾 | 回顾、交易台问题、习题、参考文献 |

## 写给研究者

* **定理（羊群效应的平稳分布）：** 柯曼链的平稳分布恰为贝塔二项分布(N, α, α)，α = ε(N − 1)/(1 − δ)；证明：生灭链可逆，细致平衡的相邻概率比与
  贝塔二项分布的相同。推论：份额收敛到Beta(α, α)，当且仅当α < 1时呈U形；完全一致的概率约为2Γ(2α)/Γ(α)·N^−α。平均通过时间由递推m_k给出。
* **定理（冷酷触发）：** 当且仅当δ ≥ (π^d − π^c)/(π^d − π^n)时，冷酷触发是子博弈完美均衡；用单次偏离原则证明。T期惩罚的推论；阿布鲁的最小最大界。
* **测量：** logit博弈中冷酷触发阈值0.393，一期惩罚0.648，五期0.395，阿布鲁界0.357；学习者在δ = 0.5时指数仅0.21：学习需要的耐心远多于均衡；
  学到的惩罚约5期；短视学习者中位数0.24，其中89%高于网格上的两个一次性均衡。
* **开放问题：** 学习者到达哪个均衡的理论；从数据中检测学来的合谋；挫败合谋的市场设计；度量模型单一化。

## 交易台问题与解答

1. **两个从不交流的算法最终报出很宽的价差，这算合谋吗？** 经济学上，若高价由奖惩维持就算：强迫一方降价一次，这里95%的场次会惩罚并全部回归；
   法律上，竞争法主要禁止协议，默契协调通常合法，学来的协调是否算协议尚无定论。
2. **为什么回测不是做市商的环境？** 报价会改变谁与你交易；把两单位规则的成交按四单位价格回放，预测445，实盘只有129。
3. **在模拟器里训练的智能体要检查什么？** 对订单的响应，而不只是典型事实；从未见过的状态和对手；模拟器的识别假设。
4. **羊群效应如何让波动率聚集？** 图表交易者份额变化缓慢，而方差随份额上升。
5. **每笔订单有五分之一来自一个模型，为什么重要？** 共享部分相干叠加：一百个交易者时共同份额为86%；4σ的模型错误平均造成约8倍的日波动，这里为11倍。
6. **冷酷触发何时能维持垄断价格？** δ ≥ (π^d − π^c)/(π^d − π^n)，本部分的logit博弈中为0.39。

## 习题与解答

1. Cov(r_t, r_{t−k}) = 0，而Cov(|r_t|, |r_{t−k}|) = (E|ε|)²Cov(σ_t, σ_{t−k}) > 0。
2. α = 0.01 × 49/0.98 = 0.5 < 1：人群跟风，分布呈U形。
3. 代入u(k)与d(k + 1)，比值等于贝塔二项分布的相邻概率比。
4. 最大化dλe^{−kd}得d* = 1/k；k = 0.5时为2个单位，逆向选择把它加宽到3。
5. R + 2n假定更宽的报价下成交不变，但噪声成交按e^{−2k}减少，所以向上偏；这里445对129。
6. 一阶条件p − c = μ/(1 − q)；p = 1.473时q = 0.471，μ/(1 − q) = 0.473 = p − c。
7. 冷酷触发：(4 − 3)/(4 − 2) = 0.5；一期惩罚需要δ ≥ 1，不可能。
8. Nw² = (1 − w)²，w = 1/(1 + √N) = 1/11 ≈ 0.091。
9. 期望额外变动与多样化市场日波动之比为√N·w·e，N = 100、w = 0.2、e = 4时为8。
10. 离散网格上的一次性博弈有高于连续纳什价格的均衡（−0.02和0.12）；ε贪婪学习者的估计相互耦合，使89%的场次高于0.12。
11. **（资格考试）** 单次偏离原则：截断T期后损失至多2Mδ^T/(1 − δ)；取最短的有利偏离，其最后一步就是有利的单次偏离；由此推出冷酷触发定理和T期推论。
12. **（资格考试）** 由细致平衡得贝塔二项分布；由斯特林公式得份额收敛到Beta(α, α)；π(0) = Γ(2α)Γ(N + α)/(Γ(α)Γ(N + 2α)) ~ Γ(2α)/Γ(α)·N^{−α}。

## 数据与复现

肯尼斯·弗伦奇日度因子（截至2020年），在`videos/quant/data/manifest.json`中校验；所有模拟随机种子固定；每个数字来自`compute.py`（缓存于
`.cache/quant42/`）和`explainer/quant/house/agents.py`。卡尔瓦诺等人的实验设定沿用已发表论文。
