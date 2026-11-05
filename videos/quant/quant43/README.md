# Quant, Built — Part 43: Can You Beat the Market?

Part 43 is the last of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)). It closes Act VII, The System, and the series, built to the series' PhD layer. It asks
the question the House was built to answer. It opens the Track Record in full, closes the Surface's scoreboard, and
ends where Part 1 began, with Bachelier.

Data:
* Kenneth French's daily and monthly US factors, 1926–2020, for adaptive efficiency and the House's ensemble.
* The House's own Track Record and envelope: 25 rows, each opened once on the sealed 2021–25 hold-out.
* The Surface's cached fits from Parts 10–14.
* CME's public notices of April 2020.

The fund populations in Chapters 2 and 3 are **simulated** with fixed seeds, where the truth is known. Fund-level
databases are licensed, so the counting of skill was not run on real funds. The House's new library is
`explainer/quant/house/skill.py`. Firms and episodes are described only from the public record. Nothing here is
investment advice: the House's "portfolio" is a teaching example.

## Chapters (about 53 minutes)

| | Chapter | What it shows |
|---|---|---|
| 0 | Hook | four findings; the desk question, skill or luck?; Act VII's last part; a century of the debate |
| 1 | Sharpe's arithmetic | market = passive + active, so before costs active earns the market, proved; with a 1% cost and 5% tracking error a zero-skill manager is ahead after 15 years 22% of the time (theory against simulation, 1–30 years); years to t = 2 are (2/IR)²; fees compounded; the loser's game; scorecards; Pedersen's exception; Grossman–Stiglitz |
| 2 | Luck or skill? | streaks; 2,000 simulated funds over 20 years; the best of the nulls has t = 3.58 and 64 nulls clear 1.96; Barras–Scaillet–Wermers' shares: π0 0.756 (truth 0.746), skilled 1.2% (1.1%), unskilled 22.7% (24.4%); of the 58 significant winners, 36% are skilled; persistence: the top decile's next alpha +0.2%, 11% skilled; the bottom −2.8% |
| 3 | Skill, scale and money | Berk–Green: flows chase skill until investors' net alpha is zero; asset-weighted net alpha −0.4%; corr(skill, assets) 0.86, corr(skill, net alpha) 0.02; the top 40 have skill 5.1% and gross alpha 1.1%; value added goes to managers as fees; Berk–van Binsbergen |
| 4 | Adaptive markets | Lo's adaptive markets; the rolling daily autocorrelation of the US market, 0.29 in the 1970s and −0.04 in the 2010s; variance ratios, VR5 1.51 against 0.92, VR20 1.60 against 0.74; why it fell; Fama, Shiller and Hansen (2013); McLean–Pontiff; the House's crypto carry halved out of sample |
| 5 | The Track Record, opened in full | the protocol; 25 rows in order; research against hold-out: slope 0.555 (0.704 on the 21 long-history rows); by family; the deflated Sharpe ratio before the hold-out; 23,560 trials counted; the hold-out's own luck bar, 0.90, cleared by 6 rows; what held and what did not; the zoo's caveat; the House's ensemble of ten premia (research 1.03, 0.71 net; hold-out 0.76 ± 0.46, 0.46 net; worst drawdown −6.4%); the verdict: 88% positive, 24% significant alone, π0 0.24 |
| 6 | The Surface's scoreboard | nine models on one Bitcoin surface: Black–Scholes 3.89 vol points, jumps about 2.1–2.7, Heston 1.33, rough Heston 1.28, rough Bergomi 0.83, SSVI 0.74; tomorrow: path-dependent volatility 0.88 → 1.50 while rough Bergomi holds (0.93 → 0.91); how the desk uses it; three lessons; why this surface |
| 7 | What we still do not know | open problems in markets, models, the system and the method; three things the series did settle; what it could not test (real fund records, other surfaces, a long hold-out, language models as traders); the method |
| 8 | Back to Bachelier | WTI settled at −$37.63 on 20 April 2020, and CME switched options on several energy contracts to the Bachelier model from 22 April; negative rates and normal vols; the two models side by side (the zero-strike call 10.10); the fair game; the thesis of 1900; the whole arc |
| 9 | The House's journey | the seven acts, what each built and proved, and its lesson; the count: 59 registrations, 25 Track Record rows, 23,560 configurations |
| 10 | Rule 43: the market is the default | the last rule; the last evening report; the rules that got here; what the House does with its money (a teaching example); the House complete; advice to analysts, PMs and researchers; the code; three last tests |
| R | For the researcher | Storey's estimator: unbiased upward without independence, proved by linearity and checked by simulation; the bias–variance choice of λ; the corollary for skill; dependence; Benjamini–Hochberg and q-values; the House's record; the Berk–Green no-persistence theorem, proved and checked; open problems |
| 11 | Outro | thirteen lines, the series in one picture, three lessons, formulas, six desk questions, problems, references, how to check it all |

## For the researcher

* **Theorem (Storey's estimator is conservative, under any dependence).** m tests, m0 true nulls, each null p-value
  uniform on (0, 1). Let W(λ) = #{i : p_i > λ} and π̂0(λ) = W(λ)/(m(1 − λ)). Then
  E π̂0(λ) = π0 + Σ_{i alt} P(p_i > λ)/(m(1 − λ)) ≥ π0.
  * **Proof.** W is a sum of indicators, so EW = Σ_i P(p_i > λ) by linearity, whatever the joint law. Each null
    contributes 1 − λ; each alternative contributes P(p_i > λ) ≥ 0. Divide by m(1 − λ).
  * **The bias** is zero only if no alternative's p-value can exceed λ. It falls as λ rises, while the variance rises:
    Storey chose λ by a bootstrap estimate of the mean squared error.
  * **Corollary (the skilled share errs low).** BSW's skilled share is S⁺ − π̂0·γ/2. Its expectation is at most the true
    share, so the estimated share of skilled funds is, on average, a lower bound.
  * **Variance.** Under independence, Var π̂0 = [m0λ(1 − λ) + Σ_alt q_i(1 − q_i)]/(m(1 − λ))², where
    q_i = P(p_i > λ). It is O(1/m). Under equicorrelation the cross terms do not vanish, so the variance has a positive
    limit and π̂0 is not consistent.
* **Measured (1,000 tests, π0 = 0.8, 400 samples per setting).**
  * Weak alternatives (μ = 1): the mean is 0.930 at λ = 0.5, against a theory of 0.930.
  * Strong alternatives (μ = 3): 0.805.
  * Every simulated mean lies on the theorem's line at every λ ∈ {0.1, 0.3, 0.5, 0.7, 0.9}.
  * Dependence (equicorrelated z-scores, μ = 2):
    * ρ = 0: mean 0.835, spread 0.027.
    * ρ = 0.3: 0.834 and 0.140.
    * ρ = 0.6: 0.810 and 0.251.
* **Using it.**
  * On Chapter 2's population, testing each fund at 5% declares 94 funds, 78% of them falsely.
  * Benjamini–Hochberg at q = 10% declares 13, none false. Storey's version declares 14.
  * The best funds' q-values are about 0.001.
  * On the House's 25 rows, π̂0 = 0.24, with a bootstrap 90% range of 0.08–0.48. The rows are correlated factor
    portfolios, so the true uncertainty is wider still.
* **Theorem (Berk–Green: no persistence for investors).** Suppose competitive flows set size A_t so that
  E[α_{t+1} − bA_t − f | F_t] = 0. Then investors' net alpha η_{t+1} is a martingale difference with respect to the
  public filtration F_t, so Cov(η_{t+1}, X) = 0 for every F_t-measurable X, past net alphas included.
  * **Proof.** Write η_{t+1} = (a − E[a | F_t]) + ε_{t+1}. The first term has mean zero given F_t, because E[a | F_t]
    is the posterior mean; the second is noise. By the tower property, E[η_{t+1}X] = E[X·E[η_{t+1} | F_t]] = 0.
  * **Checked**, among funds with investors in both years (2,256 fund-years):
    * slope of next year's net alpha on this year's: −0.020 ± 0.022.
    * With sizes fixed: 0.238 ± 0.012, against the theory's 0.265. That theory is the skill share of a fund's
      return variance, σ_a²/(σ_a² + σ_ε²) = 0.0009/0.0034.
* **Simplifications.**
  * Normal returns and Gaussian test statistics.
  * A three-group fund population.
  * Berk–Green with a known prior and linear decreasing returns.
  * Twenty-five hold-out rows over only five years.
* **Open problems.**
  * Estimators of π0 with controlled variance when every test shares one market factor.
  * Time-varying skill.
  * Counting the nulls among a whole field's published results.

## Build it

```bash
python -m videos.quant.quant43.compute                            # every item; a few minutes
python -m pytest -q tests/test_quant_house.py -k skill
EXPLAINER_TTS=silent python tools/qa_scene.py quant43 Research     # one chapter, silent, with a contact sheet
python tools/build.py quant43                                      # the narrated part
```

## Desk questions, with solutions

1. **A fund beat the market for five years. Skill or luck?**
   * By itself the record says little. With a 5% tracking error and no skill, five years gives a t-statistic of noise.
   * Count how many tried, against what luck would give. Among 2,000 zero-skill funds, about 50 clear t = 1.96, and
     the best reaches about t = 3.6.
   * Ask whether the record was registered before it was run.
2. **Why must active trail passive?**
   * The arithmetic: the market is passive plus active, and passive earns the market, so active does too before
     costs.
   * After costs, active earns less on average.
3. **Who benefits from skill?** The manager, through size: flows grow the fund until investors' net alpha is zero, so
   skill ends up as fees (corr(skill, assets) 0.86 against corr(skill, net alpha) 0.02 here).
4. **A strategy worked for fifty years. What do you check?**
   * Whether the market that paid it still exists. The US market's daily autocorrelation fell from 0.29 to −0.04, and
     published anomalies lose about half after publication.
5. **Your research Sharpe is 2. What do you expect out of sample?**
   * About half the excess over the average. On the Track Record, 0.20 + 0.55 × 2 ≈ 1.3.
   * The five-year standard error is about 0.45.
6. **Why is Storey's estimate conservative?**
   * Linearity of expectation: alternatives can only add to the count of large p-values, under any dependence.

## Problems, with solutions

1. **Active earns 8%.** 8 = 0.4 × 8 + 0.6 × r_A, so r_A = 8%.
2. **Luck over ten years.** P = Φ(−c√T/s) = Φ(−0.0075 × √10/0.04) = Φ(−0.593) = 0.277.
3. **How many look significant.** Taking t > 1.96 one-sided: 2,000 × 0.025 = 50. For t > 3: 2,000 × 0.00135 = 2.7.
4. **Storey.** π̂0(0.5) = 300/(1,000 × 0.5) = 0.6.
5. **The skilled share.** 0.09 − π̂0·γ/2 = 0.09 − 0.8 × 0.1 = 0.01, so 1%.
6. **Berk–Green size.**
   * Investors' net alpha is a − bA − f = 0, so A* = (a − f)/b = (4% − 1%)/0.1% = 30 units.
   * Investors' net alpha is 0. The manager earns fA* = 0.3 units a year.
7. **Variance ratios.** VR(q) = 1 + 2Σ_{k<q}(1 − k/q)ρ_k.
   * VR(2) = 1 + ρ₁ = 1.2.
   * VR(5) = 1 + 2 × 0.8 × 0.2 = 1.32.
8. **A hold-out's standard error.** SE ≈ √((1 + SR²/2)/T) = √(1.125/5) = 0.47.
9. **Predicting out of sample.** 0.2 + 0.55 × 1.5 = 1.03.
10. **Bachelier at the money.** C = σ_N√T·φ(0) = 10/√(2π) = 3.99.
11. **(qual) Storey's estimator in full.**
    * Mean: as in the theorem. W = Σ1{p_i > λ}, so EW = m0(1 − λ) + Σ_alt q_i by linearity, with no independence
      used.
    * Variance under independence: the indicators are independent Bernoullis, so
      Var W = m0λ(1 − λ) + Σ_alt q_i(1 − q_i). Then Var π̂0 = Var W/(m(1 − λ))². Under the full null this is
      λ/(m(1 − λ)).
    * Equicorrelation: let z_i = μ_i + √ρ·F + √(1 − ρ)·e_i. The mean is unchanged, because each z_i has the same
      marginal law, so each P(p_i > λ) is unchanged. Given F, the indicators are independent with probabilities
      g_i(F), so π̂0 → Σg_i(F)/(m(1 − λ)) as m grows. This is a random limit with variance of order ρ, not 1/m. The
      estimator stays honest on average, but no number of tests makes it reliable.
12. **(qual) Sharpe's arithmetic and Pedersen's exception.**
    * Proof: let w_P be the passive share, holding the market portfolio throughout. Then
      r_M = w_P·r_M + (1 − w_P)·r_A, so r_A = r_M. This is an identity in returns before costs.
    * The exception: "passive" investors do not hold the market portfolio at every moment. Index additions, deletions,
      issues and buybacks force them to trade at announced dates. Pedersen (2018) shows active investors as a group
      can then beat passive ones.
    * Example: a stock worth 100 is to join the index. Active investors buy it at 100 after the announcement. At
      inclusion, passive funds must buy it, and the price is pushed to 105. The actives sell it to them at 105.
    * Taking the stock to be 1% of passive's holdings, passive loses 5% × 1% = 0.05% that year to active, and active
      in aggregate beats passive by exactly that transfer.
    * The identity fails because passive did not hold the stock before inclusion: the market portfolio changed.

## Data and reproducibility

* Kenneth French's factors (through 2020), cached and checksummed in `videos/quant/data/manifest.json`.
* The Track Record and the envelope's registry are committed files under `videos/quant/data/`. The ensemble
  (`house_ensemble_part43`) was registered with one trial before its hold-out was opened.
* The fund populations, Berk–Green markets and Storey checks are simulations with fixed seeds in `compute.py`, cached
  in `.cache/quant43/`, using `explainer/quant/house/skill.py`.
* The WTI settlement and CME's switch to the Bachelier model are from CME's public notices of April 2020.

---

# 量化金融，从零搭建 — 第43部分：你能战胜市场吗？

本系列共四十三部分，这是最后一部分，结束第七幕“体系”以及整个系列，按博士层标准构建。它回答本系列公司被建来回答的问题：完整打开业绩记录，关闭曲面的
记分板，并回到第1部分的起点巴舍利耶。数据：肯尼斯·弗伦奇1926—2020年的美国因子；本系列公司自己的业绩记录与信封（25行，每行在封存的2021—25年
样本外上只打开一次）；第10—14部分的曲面缓存拟合；芝商所2020年4月的公开通知。第2、3章的基金总体是**模拟**的（随机种子固定，真相已知）：基金层面的
数据库需要授权，所以技能的计数没有在真实基金上运行。新代码在`explainer/quant/house/skill.py`中。公司和事件只按公开记录描述。这里的内容不构成投资
建议，本系列公司的“投资组合”只是教学示例。

## 章节（约53分钟）

| | 章节 | 内容 |
|---|---|---|
| 0 | 开场 | 四个发现；交易台问题：技能还是运气？；一个世纪的争论 |
| 1 | 夏普的算术 | 市场 = 被动 + 主动，所以扣除成本前主动恰好赚到市场收益（证明）；成本1%、跟踪误差5%的无技能经理15年后领先的概率为22%；达到t = 2需要(2/IR)²年；费用复利；输家的游戏；佩德森的例外；格罗斯曼—斯蒂格利茨 |
| 2 | 运气还是技能？ | 2000只模拟基金；零假设中最好的t = 3.58，64只超过1.96；BSW比例：π0 0.756（真值0.746）、有技能1.2%（1.1%）、无技能22.7%（24.4%）；58只显著赢家中36%有技能；持续性 |
| 3 | 技能、规模与资金 | 伯克—格林：资金追逐技能直到投资者净阿尔法为零；资产加权净阿尔法−0.4%；技能与资产相关0.86，与净阿尔法相关0.02；价值增值以费用形式归经理 |
| 4 | 适应性市场 | 罗闻全的适应性市场；美国市场日自相关一九七〇年代0.29、二〇一〇年代−0.04；方差比VR5 1.51对0.92，VR20 1.60对0.74；2013年诺贝尔奖；麦克莱恩—庞蒂夫；加密套息在样本外减半 |
| 5 | 完整打开的业绩记录 | 协议；25行；研究对样本外斜率0.555（长历史21行为0.704）；按类别；紧缩夏普；23560次试验；样本外自己的运气门槛0.90，6行越过；本系列公司的十因子组合（研究1.03，扣成本0.71；样本外0.76 ± 0.46，扣成本0.46；最大回撤−6.4%）；结论：88%为正，24%单独显著，π0 0.24 |
| 6 | 曲面的记分板 | 同一比特币曲面上的九个模型：布莱克—斯科尔斯3.89个波动率点，Heston 1.33，粗糙Bergomi 0.83，SSVI 0.74；第二天：路径依赖波动率0.88 → 1.50；交易台的用法；三个教训 |
| 7 | 我们仍然不知道的 | 市场、模型、系统与方法中的开放问题；本系列确实解决的三件事；本系列无法检验的东西；方法 |
| 8 | 回到巴舍利耶 | 2020年4月20日WTI结算价−37.63美元，芝商所自22日起把若干能源期权改用巴舍利耶模型；负利率与正态波动率；两个模型并排（零行权价看涨10.10）；公平博弈；1900年的论文 |
| 9 | 本系列公司的历程 | 七幕各自建了什么、证明了什么、教训是什么；计数：59次登记，25行业绩记录，23560个配置 |
| 10 | 第43条规则：市场是默认选项 | 最后一条规则；最后的晚间报告；本系列公司如何处置资金（教学示例）；给分析师、投资组合经理和研究者的话；三个最后的检验 |
| R | 写给研究者 | 斯托里估计量在任意相关性下都偏保守（线性证明，模拟检验）；λ的偏差—方差权衡；对技能比例的推论；相关性；BH与q值；本系列公司的记录；伯克—格林无持续性定理（证明与检验）；开放问题 |
| 11 | 结尾 | 十三句话、整个系列一张图、三个教训、公式、六个交易台问题、习题、参考文献、如何检验 |

## 写给研究者

* **定理（斯托里估计量在任意相关性下都偏保守）：** m个检验，m0个真零假设，零假设的p值服从(0, 1)上的均匀分布。令W(λ) = #{p_i > λ}，
  π̂0 = W/(m(1 − λ))，则E π̂0 = π0 + Σ_备择 P(p_i > λ)/(m(1 − λ)) ≥ π0。证明：W是示性函数之和，由期望的线性性EW = Σ P(p_i > λ)，与联合分布无关。
  推论：BSW的技能比例S⁺ − π̂0·γ/2平均而言偏低，是技能的下界。独立时方差为O(1/m)；等相关时交叉项不消失，π̂0不相合。
* **测量（1000个检验，π0 = 0.8，每种设定400个样本）：** 弱备择（μ = 1）λ = 0.5时均值0.930（理论0.930）；强备择（μ = 3）0.805；每个λ上模拟均值都在
  理论线上。相关性（μ = 2）：ρ = 0时均值0.835、离散0.027；ρ = 0.6时0.810、0.251。
* **应用：** 每只基金按5%检验宣布94只，78%是错的；BH在q = 10%宣布13只，无一错误；本系列公司25行的π̂0 = 0.24，自助法90%区间0.08—0.48。
* **定理（伯克—格林：投资者所得无持续性）：** 若竞争性资金流使E[α_{t+1} − bA_t − f | F_t] = 0，则投资者净阿尔法是关于公开信息流的鞅差，与任何
  F_t可测变量（包括过去的净阿尔法）不相关。证明：η_{t+1} = (a − E[a | F_t]) + ε_{t+1}，后验均值误差条件均值为零，再用塔性质。检验（两年都有投资者的
  2256个基金年）：斜率−0.020 ± 0.022；规模固定时0.238 ± 0.012，理论值0.265。
* **开放问题：** 所有检验共享一个市场因子时方差受控的π0估计量；随时间变化的技能；计数整个领域已发表结果中的零假设。

## 交易台问题与解答

1. **一只基金五年跑赢市场，是技能还是运气？** 单凭记录说明不了多少；与运气给出的数量相比：2000只无技能基金中约50只越过t = 1.96，最好的约t = 3.6；
   并问记录是否事先登记。
2. **为什么主动必然落后于被动？** 算术：市场 = 被动 + 主动，被动赚市场收益，所以扣成本前主动也赚市场收益，扣成本后更少。
3. **谁从技能中获益？** 经理，通过规模：资金流入直到投资者净阿尔法为零（这里技能与资产相关0.86，与净阿尔法相关0.02）。
4. **一个策略有效了五十年，检查什么？** 支付它的市场是否仍然存在：美国市场日自相关从0.29降到−0.04；已发表异象发表后损失约一半。
5. **研究夏普为2，样本外预期多少？** 约保留超额部分的一半：0.20 + 0.55 × 2 ≈ 1.3，五年标准误约0.45。
6. **为什么斯托里的估计是保守的？** 期望的线性性：在任意相关性下，备择假设只会增加大p值的计数。

## 习题与解答

1. 8 = 0.4 × 8 + 0.6 × r_A，所以r_A = 8%。
2. P = Φ(−0.0075 × √10/0.04) = Φ(−0.593) = 0.277。
3. 单侧t > 1.96：2000 × 0.025 = 50；t > 3：2000 × 0.00135 = 2.7。
4. π̂0 = 300/(1000 × 0.5) = 0.6。
5. 0.09 − 0.8 × 0.1 = 0.01，即1%。
6. a − bA − f = 0，A* = (4% − 1%)/0.1% = 30个单位；投资者净阿尔法为0，经理每年赚fA* = 0.3个单位。
7. VR(2) = 1 + ρ₁ = 1.2；VR(5) = 1 + 2 × 0.8 × 0.2 = 1.32。
8. SE ≈ √((1 + SR²/2)/T) = √(1.125/5) = 0.47。
9. 0.2 + 0.55 × 1.5 = 1.03。
10. C = σ_N√T·φ(0) = 10/√(2π) = 3.99。
11. **（资格考试）** 均值：由线性性EW = m0(1 − λ) + Σq_i；独立时Var W = m0λ(1 − λ) + Σq_i(1 − q_i)，全零假设下Var π̂0 = λ/(m(1 − λ))；
    等相关模型z_i = μ_i + √ρF + √(1 − ρ)e_i中边际分布不变故均值不变，但给定F时π̂0收敛到随机极限，方差为ρ的量级而非1/m。
12. **（资格考试）** 证明：r_M = w_P·r_M + (1 − w_P)·r_A，故r_A = r_M。例外（佩德森2018）：被动投资者并非时时持有市场组合；指数调整迫使其在公告
    日期交易。例：一只价值100的股票将纳入指数，主动投资者在公告后以100买入，纳入时以105卖给必须买入的被动基金；若它占被动持仓的1%，被动当年
    向主动转移0.05%，主动整体恰好以此跑赢被动。

## 数据与复现

肯尼斯·弗伦奇因子（截至2020年），在`videos/quant/data/manifest.json`中校验；业绩记录与信封登记表是`videos/quant/data/`下提交的文件，组合
`house_ensemble_part43`在打开样本外之前只尝试一次即登记；基金总体、伯克—格林市场和斯托里检验都是`compute.py`中随机种子固定的模拟（缓存于
`.cache/quant43/`），使用`explainer/quant/house/skill.py`；WTI结算价与芝商所改用巴舍利耶模型来自芝商所2020年4月的公开通知。
