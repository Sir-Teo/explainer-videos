# Quant, Built — Part 34: Inside a Quant Firm

Part 34 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth part of Act V, Portfolios, Strategies and the Firm (30–38), built to the
series' PhD layer. Parts 30–33 built portfolios, risk models and strategies. This part steps back to the firm that runs
them: its business model, capital, limits, technology, compliance, people, and the arithmetic of the drawdown stop that
decides how long a manager keeps their seat.

This is the industry part. Its facts about firms come from the public record only: filings, regulators' orders,
court records, books, and press reports labelled "as reported". Allegations are labelled as allegations. What is
computed is the firm's arithmetic:

* what a disclosed statistic implies;
* how a drawdown stop behaves, exactly and by simulation;
* what a platform of managers earns;
* how much the House's own registered books shrank on sealed years;
* whether drawdown stops help real factor premia (Kenneth French's factors, 1966–2020).

The part covers:

* **Six business models:**
  * proprietary trading (Jane Street, HRT, Jump, XTX);
  * market making (Citadel Securities, Virtu, Optiver), and payment for order flow;
  * multi-manager platforms (Millennium, Citadel, Balyasny, Point72);
  * systematic funds (Renaissance, D. E. Shaw, AQR, Two Sigma, Man AHL);
  * bank desks after the Volcker rule;
  * China's quant private funds.
* **What firms have disclosed:**
  * Virtu's one losing day in 1,238, read as a Sharpe ratio, with fat tails, a confidence bound and the law of large
    numbers;
  * Jane Street's revenue, as reported;
  * Medallion's returns, as reported, with the fees checked against them.
* **The pod model:**
  * structure, sizing by volatility budget, the reported 5%/7.5% drawdown rules, pass-through fees;
  * a simulated platform with and without stops, under heterogeneous and identical skill;
  * selection, netting risk, the talent market.
* **From idea to capital:** the review's questions, the House's own Track Record as a haircut regression,
  incubation, a posterior-sized capital ramp, retirement.
* **Risk at the firm level:** layers of control, limits, liquidity in days, stress tests, correlations in a crisis,
  Knight Capital (2012), pre-trade controls and the market access rule, Archegos (2021).
* **Technology:** the stack, OCaml at Jane Street, C++ and FPGAs, point-in-time data and kdb+, the speed of light from
  Aurora to Carteret, colocation, frequent batch auctions, research computing, reproducibility.
* **Surveillance and the cases:**
  * spoofing, layering, marking the close and wash trades;
  * Sarao, J.P. Morgan's $920m resolution and the CAT;
  * detection;
  * SEBI's 2025 interim order on Jane Street (allegations, contested).
* **The interview:** with computed answers:
  * the maximum of two dice;
  * a market on three dice, with an informed counterparty;
  * St. Petersburg with a cap;
  * Kelly;
  * a Fermi estimate;
  * the one-pass drawdown.
* **Founding stories, as told in public:** Thorp, Simons, Shaw, Griffin, Jane Street, Englander, AQR and Two Sigma,
  and their survivorship.
* **Do drawdown stops help?** Six factors and six rules, each against an i.i.d. shuffle null.
* **For the researcher: how long a seat lasts.**
  * The Taylor–Lehoczky formulas for the expected stop time and the exponential peak, proved from the reflected
    drawdown's Dynkin equation and the scale function.
  * Regimes, the distribution of the stop time, simulations and the stop's power as a test.

There is no registered strategy in this part. The House adds a compliance desk and Rule 34; the trial counter stands at
23,550.

*An education in methods, not investment advice.*

## Chapters (about 55 minutes)

* **Hook: how long a seat lasts** (2.8).
  * A Sharpe-1 manager under a 5% stop at 10% volatility lasts about 4 months on average.
  * Three findings; where this sits; fifty years of firms; the plan.
* **1. Six ways to be a quant firm** (4.2). The economics in one line; the six models; payment for order flow; a
  comparison.
* **2. What the firms have disclosed** (4.8).
  * Virtu: daily Sharpe 3.15 under normality, about 50 a year, at least 42 at the 95% bound; 5.4 and 6.3 with t(4)
    and t(3) tails.
  * Losing days fall from 47% to 0.05% as trades a day rise from 100 to 100,000.
  * Jane Street (about $10.6bn net trading revenue in 2023, as reported); Medallion (66% and 39%, as reported; the fee
    check gives 34%).
* **3. The pod model** (5.1).
  * Sizing; the reported rules; pass-through arithmetic.
  * The simulation (200 seats, 30 years, 8 runs). When skill varies, investors' Sharpe is 1.90 with stops against
    1.19 without. With identical skill, 1.30 against 1.23.
  * Fired managers average Sharpe 0.34, seated ones 0.83; 25% of gross P&L is paid to pods.
* **4. From idea to capital** (3.5).
  * The review; the Track Record (22 books): sealed = 0.10 + 0.75 × research; mean 0.57 → 0.53; 87% positive.
  * Incubation; the posterior ramp (0.2, 0.5, 0.71 at 1, 4 and 10 years); retirement.
* **5. Risk at the level of the firm** (4.0).
  * Layers; limits; days to exit (6 days, 63 bp).
  * Correlation from 0.05 to 0.4 multiplies a 50-desk firm's volatility by 2.4.
  * Knight; controls; Archegos.
* **6. Technology** (3.4). The stack; languages; data; 1,185 km at 3.95 ms in vacuum, 5.8 ms in fibre; colocation;
  research computing; the House's manifest.
* **7. Surveillance and the cases** (3.5). Abuses; a stylised layering book; Sarao; J.P. Morgan; the CAT; detection;
  SEBI and Jane Street; the compliance desk.
* **8. The interview** (4.0). 161/36; 10.5 ± 2.96; the informed six; $31 with a $1bn cap; Kelly 0.2, growth 0.020
  against −0.002 at twice Kelly; about 24 million trades a day; the drawdown in one pass.
* **9. Founding stories, as told in public** (2.8). Six founders and two successors; what the stories share; culture.
* **10. Do drawdown stops help?** (3.0).
  * The null S√(1 − time out).
  * HML 0.20 → 0.28 with a 15%/12-month stop; UMD 0.60 → 0.56, at its shuffle.
  * No combination lost to its shuffle by two standard deviations.
  * Why, and 36 trials.
* **11. Rule 34: the firm** (3.0). The first sheet; labs (`stop_time`, `apply_stop`, `platform`); the module; Rule 34;
  three cases.
* **For the researcher: how long a seat lasts, exactly** (6.9).
  * The setup; two lemmas; the theorem; the table; three regimes.
  * The stop-time distribution at S = 1, δ = 1: simulated median 1.8 and mean 2.5 years, against the theorem's mean 2.2.
  * Simulations; power; design; the seat's P&L before the stop; related results; open problems.
* **Recap, desk questions, problems** (3.8). Fourteen lines; six desk questions; the pause questions answered; twelve
  problems, two of qualifying-exam level, solved below.

## Hands-on

* **Built and run here:**
  * the implied Sharpe ratio of a disclosed loss rate;
  * the drawdown-stop formulas, simulated with step-size extrapolation;
  * the stop's power curve;
  * a multi-manager platform with stops, payouts and a common shock;
  * the Track Record's research-to-holdout regression;
  * drawdown stops on six factors against shuffle nulls;
  * interview answers computed exactly.
* **Labs, from the House's source:** `stop_time` and `peak_at_stop`, `apply_stop`, `platform`, and `max_drawdown`.

## Textbook audit

| Textbook | Sections | Chapters |
|---|---|---|
| Narang, *Inside the Black Box* (2013) | the parts of a quant system, research to execution | 4, 6 |
| Isichenko, *Quantitative Portfolio Management* (2021) | research process, data, trading infrastructure | 4, 6 |
| Paleologo, *Advanced Portfolio Management* (2021) | pods, risk budgets, drawdown rules, sizing | 3, 5 |
| Zuckerman, *The Man Who Solved the Market* (2019) | Renaissance, as reported | 2, 9 |
| Patterson, *The Quants* (2010); Derman, *My Life as a Quant* (2004); Thorp, *A Man for All Markets* (2017) | the firms' histories as told | 9 |

## Papers and the public record, chapter by chapter

* ch. 2: Virtu Financial, Form S-1 (2014); Bloomberg's report of Jane Street's offering documents (2024).
* ch. 3: the Wall Street Journal on Millennium's drawdown rules (2024); Jane Street v. Millennium (2024, settled), as
  reported.
* ch. 5: SEC order, Knight Capital Americas (2013); SEC Rule 15c3-5 (2010); Credit Suisse's Archegos report (2021).
* ch. 6: Minsky, "OCaml for the masses", *ACM Queue* (2011); Budish, Cramton and Shim (2015), *QJE*.
* ch. 7: the Dodd–Frank Act §747; US v. Sarao; CFTC, DOJ and SEC on J.P. Morgan (2020); SEC Rule 613 (CAT); SEBI's
  interim order (July 2025; allegations, contested).
* ch. 10: Kenneth French's data library.
* Research: Taylor (1975), *Annals of Probability*; Lehoczky (1977), *Annals of Probability*; Grossman and Zhou (1993),
  *Mathematical Finance*; Magdon-Ismail, Atiya, Pratap and Abu-Mostafa (2004), *J. Applied Probability*.

## For the researcher

* **The theorem.**
  * For P&L X_t = μt + σW_t with peak M_t and drawdown D_t = M_t − X_t, the stop τ_d = inf{t : D_t ≥ d} has
    E[τ_d] = σ²/(2μ²)(e^a − 1 − a), with a = 2μd/σ².
  * In Sharpe units, E[τ] = (e^{2Sδ} − 1 − 2Sδ)/(2S²) years.
  * M_τ is exponential with mean σ²(e^a − 1)/(2μ), and E[X_τ] = E[M_τ] − d = μ E[τ].
* **The proof.**
  * D is a Brownian motion with drift −μ reflected at 0, so f(y) = E_y[τ] solves (σ²/2) f'' − μ f' = −1, with
    f(d) = 0 and f'(0) = 0.
  * Solving gives f' = (1 − e^{2μy/σ²})/μ; integrate from d back to 0.
  * At each new peak the process restarts. The scale function s(x) = e^{−2μx/σ²} gives the chance of a stop before
    the peak rises by ε as λε, with λ = (2μ/σ²)/(e^a − 1), so M_τ ~ Exp(λ).
* **Regimes.** E[τ] ≈ δ/|S| for S < 0, δ² for S = 0, and e^{2Sδ}/(2S²) for Sδ ≫ 1: the stop is a test whose power
  comes from a large-deviation rate 2Sδ.
* **Measured.**
  * Simulations at daily and eighth-day steps, extrapolated in √Δt, come within a few percent of the theorem at six
    (S, δ) points, peaks included.
  * Within three years, a stop 1.5 volatilities deep fires on 72% of zero-skill managers and 24% of Sharpe-1 managers.
    At δ = 1 the figures are 95% and 67%.
* **Simplifications.**
  * Brownian P&L with constant skill and volatility.
  * The platform's skill pool is normal, its correlation fixed at 0.1, and its payouts annual with no claw-back.
  * The factor stops use trailing-volatility scaling and count flat months in the Sharpe ratio.
* **Open problems.**
  * The Bayes-optimal stop boundary under learning.
  * The equilibrium with a strategic manager who sees the stop.
  * Stop times for returns with persistent regimes.

## Build it

```bash
python -m videos.quant.quant34.compute                            # every item; under a minute
python -m pytest -q tests/test_quant_house.py -k firm
EXPLAINER_TTS=silent python tools/qa_scene.py quant34 Research     # one chapter, silent, with a contact sheet
python tools/build.py quant34                                      # the narrated part
```

## Desk questions, with solutions

1. **One losing day in 1,238?** Φ(−s) = 1/1,238 gives s = 3.15 a day, about 50 a year. A firm gets there with
   s = r√N: N very small, nearly independent trades.
2. **A Sharpe-1 manager under a stop half a volatility deep?** E[τ] = (e − 2)/2 ≈ 0.36 years. One volatility deep,
   (e² − 3)/2 ≈ 2.2 years.
3. **Why stop managers who may be good?** Skill is unknown, and the stop is a sequential test. In the simulation it
   lifts investors' Sharpe from 1.19 to 1.90 when skill varies, and changes little when it does not.
4. **Netting risk?** Pay = 0.2 Σ max(P&L_i, 0) while investors own Σ P&L_i, so the share paid out (25% simulated)
   exceeds 20%.
5. **What would have stopped Knight?** Price, size and rate checks, a credit limit per algorithm (Rule 15c3-5), and a
   kill switch.
6. **Is a high cancel ratio spoofing?** No. The evidence is intent: large orders cancelled on one side, in step with
   fills on the other.

## Problems, with solutions

1. **Disclosed loss rate.** Φ^{-1}(0.004) = −2.65, so s = 2.65 a day, about 42 a year.
2. **Fees at 15% gross.** Classic: (15 − 2) × 0.8 = 10.4%. Pass-through: (15 − 6) × 0.8 = 7.2%.
3. **Netting.** P&L 0, pay 0.2 × 10% = 2% of one pod's capital: an infinite share of a zero profit.
4. **Posterior Sharpe.** The factor is Tτ²/(1 + Tτ²): 0.2 at one year, giving 0.4; 0.5 at four years, giving 1.0.
5. **Liquidity in a crisis.** At a fixed participation rate, days to exit double. The cost σ√(participation) doubles
   with σ. Trading faster to keep the days raises the cost by a further √2.
6. **Re-roll.** Keep 4, 5 or 6: E = ½ × 5 + ½ × 3.5 = 4.25.
7. **Maximum of two dice.** Σ k(2k − 1)/36 = 161/36 ≈ 4.47.
8. **Capped St. Petersburg.** 20 tosses pay 1 each, and the tail pays 2^{20} × 2^{-20} = 1: about $21.
9. **Kelly at 55%.** f = 0.1. g = 0.55 ln 1.1 + 0.45 ln 0.9 = 0.00501; at f = 0.2, g = 0.55 ln 1.2 + 0.45 ln 0.8 = −0.00013.
10. **Stopped i.i.d. strategy.** The mean scales by 0.75 and the volatility by √0.75, so S = 0.6 × √0.75 ≈ 0.52.
11. **(qual) The stop time.**
    * **Reflection.** By Tanaka/Skorokhod, D_t = M_t − X_t satisfies dD = −μ dt − σ dW + dM, with dM supported on
      {D = 0}.
    * **Dynkin.** For f ∈ C² with f'(0) = 0, Itô gives f(D_t) − ∫_0^t (σ²/2 f'' − μ f')(D_s) ds as a martingale; the
      dM term vanishes because f'(0) = 0. With generator −1 and f(d) = 0, optional stopping (E τ < ∞ by comparison)
      gives f(0) = E[τ].
    * **Solution.** g = f' solves (σ²/2) g' − μ g = −1 with g(0) = 0, so g = (1 − e^{2μy/σ²})/μ, and
      f(0) = ∫_0^d (e^{2μy/σ²} − 1)/μ dy = σ²/(2μ²)(e^a − 1 − a).
    * **Driftless limit.** e^a − 1 − a = a²/2 + O(a³) gives σ²/(2μ²) × 2μ²d²/σ⁴ = d²/σ².
12. **(qual) The peak.**
    * **Exponential law.** From a new peak m, the chance of falling to m − d before reaching m + ε is
      (s(ε) − s(0))/(s(ε) − s(−d)) = λε + o(ε). By the strong Markov property at successive peaks, P(M_τ > x + ε) =
      P(M_τ > x)(1 − λε + o(ε)), so P(M_τ > x) = e^{−λx}.
    * **Earning x.** The chance the manager earns x before the stop is e^{−λx}.
    * **Wald.** E[M_τ] = 1/λ = σ²(e^a − 1)/(2μ), and X_τ = M_τ − d. Wald's identity for the martingale X_t − μt gives
      E[X_τ] = μE[τ] = σ²(e^a − 1 − a)/(2μ) = σ²(e^a − 1)/(2μ) − d, since σ²a/(2μ) = d.

## Data and reproducibility

* **Computed:**
  * from the formulas and simulations in [`explainer/quant/house/firm.py`](../../../explainer/quant/house/firm.py);
  * from the Track Record (`videos/quant/data/track_record.json`, the 23 rows registered through Part 33; Part 25's
    in-sample SDF row is excluded from the regression);
  * from Kenneth French's monthly five factors and momentum (checked by SHA-256).
* **No registration in this part.** The trial counter stands at 23,550. The 36 factor-stop combinations are research,
  stated with their trial count, and no stop is added to any registered book.
* **Quoted, not computed:**
  * Virtu's S-1;
  * Jane Street's revenue and the Millennium case, as reported;
  * Medallion's returns, as reported by Zuckerman;
  * the WSJ's report of Millennium's rules;
  * the SEC, CFTC, DOJ and SEBI documents named above;
  * firm founding facts as reported.

---

# 量化金融，从零搭建 — 第34部分：走进量化公司

这是一套共四十三部分的量化金融系列的第34部分（见[系列计划](../README.md)与[教学大纲](../SYLLABUS.md)），也是第五幕"组合、策略与公司"（第30–38部分）的第五部分，按系列的博士层次构建。第30–33部分构建了组合、风险模型和策略；这一部分退后一步，看运作它们的公司：商业模式、资本、限额、技术、合规、人，以及决定一位基金经理能保住席位多久的回撤止损算术。

这是行业部分。关于公司的事实只取自公开记录：文件、监管命令、法庭记录、书籍，以及标注为"据报道"的媒体报道；指控均标注为指控。计算的部分是公司的算术：

* 一个披露的统计量意味着什么；
* 回撤止损的精确行为及其模拟；
* 一个多基金经理平台能赚多少；
* 本系列公司自己登记的组合在封存年份上缩水多少；
* 回撤止损对真实因子溢价是否有帮助（Kenneth French的因子，1966–2020年）。

本部分没有登记新策略；本系列公司新增合规部门和第34条规则，试验计数器为23,550。

*这是方法的教育，不是投资建议。*

## 章节（约55分钟）

* **开篇：一个席位能坐多久**（2.8）。在10%波动率下设5%止损，一位夏普为一的基金经理平均坚持约4个月。
* **1. 量化公司的六种形态**（4.2）。一句话的经济学；六种模式；订单流付费；比较。
* **2. 公司披露了什么**（4.8）。
  * Virtu：正态下日度夏普3.15，年化约50，95%置信界下至少42；t(4)和t(3)尾部下为5.4和6.3。
  * 每日交易笔数从100增至100,000时，亏损日比例从47%降到0.05%。
  * Jane Street（据报道2023年净交易收入约106亿美元）；大奖章（据报道66%与39%，费用核对得34%）。
* **3. 多策略平台模式**（5.1）。
  * 规模确定；报道中的规则；费用转嫁的算术。
  * 模拟（200个席位、30年、8次运行）：技能有差异时，投资者夏普有止损1.90、无止损1.19；技能相同时，1.30对1.23。
  * 被解聘者平均夏普0.34，在任者0.83；毛损益的25%付给各组。
* **4. 从想法到资本**（3.5）。
  * 审查；业绩记录（22个组合）：封存期 = 0.10 + 0.75 × 研究期；均值0.57 → 0.53；87%为正。
  * 孵化；后验资本爬坡；退役。
* **5. 公司层面的风险**（4.0）。
  * 层次；限额；退出天数（6天，63个基点）。
  * 相关性从0.05升至0.4，使50个交易台的公司波动率乘以2.4。
  * 骑士资本；控制；Archegos。
* **6. 技术**（3.4）。技术栈；语言；数据；1,185公里，真空3.95毫秒、光纤5.8毫秒；托管机房；研究计算；本系列公司的清单。
* **7. 监控与案例**（3.5）。违规行为；分层挂单示意；Sarao；摩根大通；CAT；检测；SEBI与Jane Street；合规部门。
* **8. 面试**（4.0）。161/36；10.5 ± 2.96；知情的六；上限10亿美元时31美元；凯利0.2；每天约2400万笔交易；一遍扫描的回撤。
* **9. 公开讲述的创业故事**（2.8）。六位创始人和两家后继公司；共同点；文化。
* **10. 回撤止损有用吗？**（3.0）。
  * 零假设S√(1 − 空仓时间)。
  * HML在15%/12个月止损下由0.20升至0.28；UMD由0.60降至0.56，与打乱版本持平。
  * 没有任何组合以两个标准差输给其打乱版本；原因；36次试验。
* **11. 第34条规则：公司**（3.0）。第一张汇总表；代码实验；模块；第34条规则；三个案例。
* **写给研究者：一个席位能坐多久，精确解**（6.9）。
  * 设定；两个引理；定理；表格；三种情形。
  * 止损时间分布（S = 1、δ = 1时模拟中位数1.8年、均值2.5年，定理均值2.2年）。
  * 模拟；检验功效；设计；止损前的损益；相关结果；开放问题。
* **回顾、交易台问题与习题**（3.8）。十四行回顾；六个交易台问题；暂停题答案；十二道习题，其中两道为资格考试水平，解答见下。

## 写给研究者

* **定理。** 对损益X_t = μt + σW_t，历史高点为M_t，回撤为D_t = M_t − X_t，止损τ_d = inf{t : D_t ≥ d}满足
  * E[τ_d] = σ²/(2μ²)(e^a − 1 − a)，其中a = 2μd/σ²；以夏普为单位，E[τ] = (e^{2Sδ} − 1 − 2Sδ)/(2S²)年。
  * M_τ服从指数分布，均值σ²(e^a − 1)/(2μ)；E[X_τ] = μE[τ]。
* **证明。**
  * D是在0处反射、漂移为−μ的布朗运动，f(y) = E_y[τ]满足(σ²/2) f'' − μ f' = −1，f(d) = 0，f'(0) = 0。
  * 在每个新高处过程重新开始，尺度函数给出止损发生的速率λ = (2μ/σ²)/(e^a − 1)。
* **测量。**
  * 按√Δt外推的模拟，在六个(S, δ)点上与定理相差几个百分点以内。
  * 1.5个波动率深的止损三年内淘汰72%的零技能基金经理和24%的夏普为一的基金经理。
* **简化。** 布朗损益，技能与波动率不变；平台的技能池为正态，相关系数固定为0.1，年度报酬不追回。
* **开放问题。**
  * 学习下的贝叶斯最优止损边界。
  * 看得到止损的策略性基金经理的均衡。
  * 持续性状态下收益的止损时间。

## 交易台问题与解答

1. **一千二百三十八天里一天亏损？** Φ(−s) = 1/1,238，s = 每天3.15，年化约50；由s = r√N，靠大量几乎独立的小交易达到。
2. **半个波动率深的止损下，夏普为一的基金经理？** E[τ] = (e − 2)/2 ≈ 0.36年；一个波动率深时(e² − 3)/2 ≈ 2.2年。
3. **为什么要让可能优秀的基金经理止损？** 技能未知，止损是序贯检验；模拟中技能有差异时，投资者夏普从1.19升到1.90；技能相同时变化不大。
4. **轧差风险？** 报酬 = 0.2 Σ max(P&L_i, 0)，而投资者拥有Σ P&L_i，所以支付比例（模拟中25%）高于20%。
5. **什么本可以阻止骑士资本？** 价格、规模和频率检查，每个算法的信用限额（15c3-5规则），以及熔断开关。
6. **高撤单比率是幌骗吗？** 不是；证据是意图：一侧的大额订单与另一侧的成交同步撤销。

## 习题与解答

1. **披露的亏损率。** Φ^{-1}(0.004) = −2.65：每天2.65，年化约42。
2. **15%毛收益下的费用。** 传统：(15 − 2) × 0.8 = 10.4%；转嫁：(15 − 6) × 0.8 = 7.2%。
3. **轧差。** 损益为0，报酬为一个组资本的0.2 × 10% = 2%：零利润中的无穷大比例。
4. **后验夏普。** 收缩因子Tτ²/(1 + Tτ²)：一年为0.2，得0.4；四年为0.5，得1.0。
5. **危机中的流动性。** 参与率不变时退出天数翻倍；成本σ√(参与率)随σ翻倍。若加快交易以保持天数，成本再乘以√2。
6. **重掷。** 保留4、5、6：E = ½ × 5 + ½ × 3.5 = 4.25。
7. **两颗骰子的最大值。** Σ k(2k − 1)/36 = 161/36 ≈ 4.47。
8. **有上限的圣彼得堡游戏。** 前20次每次贡献1，尾部贡献2^{20} × 2^{-20} = 1：约21美元。
9. **55%胜率下的凯利。** f = 0.1；g = 0.00501；f = 0.2时g = −0.00013。
10. **被止损的独立收益策略。** S = 0.6 × √0.75 ≈ 0.52。
11. **（资格考试）止损时间。**
    * **反射。** dD = −μ dt − σ dW + dM，dM只在{D = 0}上增加。
    * **迪金。** 对f'(0) = 0的f，伊藤公式中的dM项消失；由可选停止定理得f(0) = E[τ]。
    * **求解。** 解g = f' = (1 − e^{2μy/σ²})/μ，积分得公式。
    * **无漂移极限。** μ → 0时e^a − 1 − a ≈ a²/2，给出d²/σ²。
12. **（资格考试）高点。**
    * **指数分布。** 在每个新高处，先跌d再升ε的概率为λε + o(ε)；由强马尔可夫性，P(M_τ > x) = e^{−λx}，即赚到x的概率。
    * **瓦尔德恒等式。** E[X_τ] = μE[τ] = E[M_τ] − d。

## 数据与复现

* **计算来源。**
  * [`firm.py`](../../../explainer/quant/house/firm.py)中的公式与模拟；
  * 业绩记录（截至第33部分的23行，回归中剔除第25部分的样本内SDF一行）；
  * Kenneth French的月度五因子与动量因子（SHA-256校验）。
* **本部分没有登记。** 计数器为23,550；36种因子止损组合作为研究记录并注明试验次数，不给任何登记组合加止损。
* **引用、未计算。**
  * Virtu的S-1；
  * Jane Street的收入与Millennium案（据报道）；
  * Zuckerman报道的大奖章收益；
  * 《华尔街日报》对Millennium规则的报道；
  * 上述SEC、CFTC、DOJ与SEBI文件；
  * 公司创立事实（据报道）。
