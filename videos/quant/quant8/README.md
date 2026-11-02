# Quant, Built — Part 8: Decisions and Control

Part 8 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the last part of Act II, the Mathematical Toolkit. Part 7 forecast how much the market
will move; this part asks how much to bet. It covers:

* expected utility, risk aversion and certainty equivalents;
* dynamic programming and the Hamilton–Jacobi–Bellman equation, solved on a grid;
* Merton's problem on 94 years of US data;
* Kelly, fractional Kelly and Thorp; Samuelson's objection; ergodicity;
* leverage beyond Kelly, with LTCM in 1998;
* optimal stopping;
* prospect theory and ambiguity;
* three frontiers: BSDEs, mean-field games, and a reinforcement learner checked against Merton.

Every number is computed by the series' own code ([`compute.py`](compute.py), the House's
[`control`](../../../explainer/quant/house/control.py) module, tested against closed forms), from Kenneth French's
monthly US market returns and from seeded simulations, labeled on screen.

*An education in methods, not investment advice.*

## Chapters (about 45 minutes)

* **How much to bet.** Haghani and Dewey (2016) gave 61 people $25 and a 60% coin at even odds for 30 minutes, with
  winnings capped at $250. About 30% went bust.
  * Kelly's growth curve, p log(1 + f) + q log(1 − f), peaks at f* = 20%, at about 2.0% a flip. At 40% growth stops.
  * We simulated 20,000 players at each fraction over 300 flips:

    | Fraction bet | Reach $250 | Go bust (under a cent) |
    |---|---|---|
    | 10% | 94.1% | 0% |
    | 20% | 93.8% | 0% |
    | 40% | 70.3% | 11.7% |
    | 100% | 13.0% | 87.0% |

  Then the objectives, and the House's sizing module.
* **1. Utility and risk aversion.** The chapter starts with Bernoulli (1738) and von Neumann–Morgenstern (1944).
  * A coin flip leaves you with 50 or 150. At log utility its certainty equivalent is 86.6, a risk premium of 13.4.
  * CRRA utility and the Arrow–Pratt premium ≈ ½γσ²/W.
  * The certainty equivalent falls as γ rises: 93.3 at γ = ½, 86.6 at 1, 67.1 at 3, 54.0 at 10 and 51.2 at 30.
* **2. Dynamic programming and the HJB equation.** Bellman's recursion, the HJB equation, and the first-order
  condition that gives Merton's fraction; viscosity solutions in brief.
  * The House's grid solver runs backward induction with Gauss–Hermite expectations, interpolating the certainty
    equivalent. It reproduces Merton's 61.7% (μ = 8%, r = 2%, σ = 18%, γ = 3) at every step size.
  * With a floor of 0.6 at year 10, it reproduces portfolio insurance, π* = π_M (w − F e^{−r(T−t)})/w, to within
    0.005. The policy surface π*(t, w) is shown in 3D.
* **3. Merton's problem.** French's US market, July 1926 to December 2020: an excess return of 8.2% a year with a
  standard error of 1.9%, and volatility of 18.5%.
  * The Merton fraction is 238% at γ = 1, 79% at γ = 3 and 24% at γ = 10.
  * With ±2 standard errors on the premium, γ = 3 allows anything from 42% to 116%.
* **4. Kelly, fractional Kelly and Thorp.** The history comes first: Kelly (1956), Breiman (1961), and Thorp's
  Princeton Newport Partners (about 15% a year after fees, 1969–1988, by Thorp's account). Then the realized growth
  of monthly-rebalanced fixed fractions of the US market, borrowing at the T-bill rate:
  * 100% grew at 9.7% a year, and the best fraction, 218%, at 12.6%;
  * at 348%, the worst month (September 1931, −28.7%) would have wiped the account out;
  * in a 12-month block bootstrap, the best fraction's 5th and 95th percentiles are 116% and 302%;
  * the registered split-sample test chose 198% on 1926–1972, which grew 13.4% a year over 1973–2020; half of it grew
    10.2%, and the best in hindsight (254%) 14.0%;
  * at 2× leverage, 19 October 1987 (−17.4%) alone would have cost about 35%.

  On fractional Kelly: c times Kelly earns (2c − c²) of Kelly's excess growth. Simulated over 10 years with μ − r = 6%
  and σ = 18%, the chance of a 50% drawdown is 10% at half Kelly, 80% at full Kelly and 100% at twice Kelly.
* **5. Samuelson's objection, and ergodicity.** Kelly (185%) against the γ = 3 Merton fraction (62%):
  * the chance Kelly ends richer is 64% at 10 years, 73% at 30 and 87% at 100;
  * yet the γ = 3 investor's certainty-equivalent growth is −3.6% a year under Kelly and +3.9% under Merton.

  Peters' coin (+50% / −40%), 100,000 players over 60 flips:
  * the ensemble average grows ×1.05 a flip, while the typical player shrinks;
  * 82% of players lose money, and the top 1% hold 86% of the wealth.

  Peters (2019) and the reply of Doctor, Wakker and Wang (2020).
* **6. Leverage beyond Kelly: LTCM, 1998.** The crisis file (President's Working Group, April 1999): $129 billion of
  assets on $4.7 billion of capital at the end of 1997, about 28:1, and $1.3 trillion of derivatives notional.
  Capital was under $1 billion by mid-September 1998, and on 23 September fourteen banks put in $3.6 billion.
  * An illustration, not LTCM's books: a trade earning 1% with 1% volatility has a Kelly leverage of 100.
  * Triple the volatility and Kelly falls to 11. At 28:1, growth then goes from +24% to −7% a year.
* **7. Optimal stopping.** The secretary problem with n = 100: reject 37, then success is 37.1%, against the 1/e
  limit, simulated and exact. The Snell envelope: an American put (K = 100, σ = 30%, r = 5%, one year) on a 500-step
  tree is worth 9.87 against the European 9.35, with its exercise boundary.
* **8. How people decide.** Prospect theory: Tversky and Kahneman's (1992) value function (α = 0.88, λ = 2.25) and
  probability weighting (γ = 0.61), with the disposition effect and lottery stocks. Ambiguity: Ellsberg's urn,
  Gilboa–Schmeidler maxmin, Hansen–Sargent robust control, and Maenhout's robust Merton fraction
  (μ − r)/((γ + θ)σ²).
* **9. Frontiers.**
  * **BSDEs.** Pardoux–Peng and El Karoui–Peng–Quenez. A call spread (S − 95)⁺ − 2(S − 105)⁺ priced with borrowing at
    6% and lending at 1% (Bergman 1995). Least-squares Monte Carlo with a piecewise-linear basis converges to the
    nonlinear PDE's 1.230 (1.165, 1.211, 1.215 and 1.225 at 5k, 20k, 100k and 300k paths), above both Black–Scholes
    prices (1.050 at r, 0.605 at R). A degree-6 polynomial basis is biased low (1.194).
  * **Mean-field games.** The HJB/Fokker–Planck pair.
  * **PPO.** On Merton's problem with log utility, with 300 iterations of 1,024 ten-year quarterly episodes, the policy
    climbs from 48% to the discrete-time optimum of 184%, flat over time and wealth. Learned exploration noise and
    reward-to-go advantages both stalled near 150%. A fixed exploration noise and one-step TD advantages were needed.
* **10. The sizing module.** Rule 9: no position is sized above the Kelly fraction of its estimated edge, the default
  is half of that, and sizes are recomputed whenever the volatility forecast changes. The trial counter reads 72.
* **Recap, desk questions, problems.**

## Build it

```bash
python -m videos.quant.quant8.compute                    # every number, cached in .cache/quant8/ (about 10 minutes)
EXPLAINER_TTS=silent python tools/qa_scene.py quant8 Kelly    # one chapter, silent, with a contact sheet
python tools/make.py quant8 --cpu-voice -q m             # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **A 60% coin at even odds.** Maximize g(f) = 0.6 log(1 + f) + 0.4 log(1 − f): g′(f) = 0.6/(1 + f) − 0.4/(1 − f) = 0
   gives f* = 0.2, and g(0.2) = 0.6 log 1.2 + 0.4 log 0.8 ≈ 2.0% a flip. g(0.4) ≈ −0.2%: twice Kelly no longer
   grows. With a cap and a time limit the target is reaching the cap, not long-run growth, so slightly less than Kelly
   does as well. In 300 flips with a $250 cap, 10% and 20% both reach it about 94% of the time.
2. **Sharpe 1 at 10% volatility.** f* = (μ − r)/σ² = SR/σ = 10, and Kelly's excess growth is SR²/2 = 50% a year on
   paper. But a Sharpe ratio measured over four years has a standard error near √(1.5/4) ≈ 0.6 (Part 6). If the true
   Sharpe is 0.5, ten times leverage is twice Kelly and grows no faster than cash. Volatility can also triple, which
   divides Kelly by nine (chapter 6). Use half Kelly or less on the estimate, and recompute as the volatility forecast
   changes.
3. **Why not Kelly.** Kelly maximizes E log W, the expected utility of an investor with γ = 1. For γ = 3 the optimal
   fraction is a third of Kelly's at every horizon. Kelly ends richer with a probability that tends to one, but its
   rare losses are so large in that investor's utility that its certainty equivalent is lower (chapter 5:
   −3.6% against +3.9% a year).

## Problems, with solutions

1. **Kelly for any odds.** g(f) = p log(1 + bf) + q log(1 − f). g′(f) = pb/(1 + bf) − q/(1 − f) = 0 gives
   pb(1 − f) = q(1 + bf), so f* = (pb − q)/b = p − q/b. For a small edge, expand to second order:
   g(f) ≈ f(pb − q) − f²(pb² + q)/2. This is zero again at f ≈ 2(pb − q)/(pb² + q), which for b = 1 is 2(p − q) = 2f*.
2. **Merton's value function.** HJB: V_t + max_π {(r + π(μ − r))wV_w + ½π²σ²w²V_ww} = 0. Substitute
   V = e^{a(T−t)}w^{1−γ}/(1 − γ), so that V_t = −aV, wV_w = (1 − γ)V and w²V_ww = −γ(1 − γ)V. Dividing by (1 − γ)V,
   the HJB becomes −a/(1 − γ) + max_π {r + π(μ − r) − ½γπ²σ²} = 0. The maximum is at π* = (μ − r)/(γσ²), where it
   equals r + (μ − r)²/(2γσ²). So a = (1 − γ)(r + (μ − r)²/(2γσ²)), and V(T) = u(w).
3. **Fractional Kelly.** Excess growth is g(f) − r = f(μ − r) − ½f²σ², maximized at f* = (μ − r)/σ² with
   g* − r = (μ − r)²/(2σ²). At f = cf* it is c(μ − r)²/σ² − ½c²(μ − r)²/σ² = (2c − c²)(g* − r). The volatility is
   cf*σ. At c = ½: 75% of the growth and half the volatility. At c = 2: none of the growth and twice the volatility.
4. **The secretary.** If the best candidate is at position j > k, the rule picks them exactly when the best of the
   first j − 1 lies among the first k, which has probability k/(j − 1). So P(k) = (k/n)Σ_{j=k+1}^{n} 1/(j − 1). With
   x = k/n this is a Riemann sum for x∫_x^1 dt/t = −x log x. Its derivative, −log x − 1, is zero at x = 1/e, where
   the value is 1/e ≈ 36.8%. For n = 100 the best k is 37, with 37.1%.
5. **Peters' coin.** Staking a fraction f each flip gives g(f) = ½log(1 + 0.5f) + ½log(1 − 0.4f).
   g′(f) = 0.25/(1 + 0.5f) − 0.2/(1 − 0.4f) = 0 gives 0.25 − 0.1f = 0.2 + 0.1f, so f* = 0.25. Then
   g = ½log(1.125 × 0.9) = ½log 1.0125 ≈ +0.62% a flip, where staking everything loses ½log(1/0.9) ≈ 5.3%. Staking a
   quarter turns a losing gamble into a growing one.

## Data and reproducibility

* Kenneth French's monthly Fama–French factors (market excess return and T-bill), July 1926 to December 2020. The
  hold-out from 2021 is sealed (Part 6).
* Registered with the trial counter: the split-sample Kelly test (1).
* The networks are small (two 32-unit hidden layers for the policy and value), train in about two minutes on a CPU
  with one thread, and are seeded.
* Facts about LTCM come from the President's Working Group report (1999); those about Haghani and Dewey from their
  paper (2016, arXiv 1701.01427); those about Princeton Newport Partners from Thorp's own account.

---

# 量化金融，从零搭建 — 第8部分：决策与控制

第7部分预测了市场会动多大，本部分问该下多大的注。内容包括：

* 期望效用、风险厌恶与确定性等价；
* 动态规划与HJB方程，并在网格上求解；
* 用九十四年美国数据求解默顿问题；
* 凯利、分数凯利与索普；萨缪尔森的反驳；遍历性；
* 超越凯利的杠杆，以1998年的LTCM为例；
* 最优停止；
* 前景理论与模糊性；
* 三个前沿：BSDE、平均场博弈，以及一个对照默顿检验的强化学习器。

所有数字都由本系列自己的代码算出：历史部分用肯尼斯·弗伦奇的月度美国市场收益，其余用带种子的模拟，并在屏幕上标明。

*讲的是方法，不构成投资建议。*

## 交易台问题与解答

1. **六成的硬币，赔率一赔一。** 最大化g(f) = 0.6 log(1 + f) + 0.4 log(1 − f)。令g′(f) = 0.6/(1 + f) − 0.4/(1 − f) = 0，得f* = 0.2，
   g(0.2) ≈ 每次2.0%。g(0.4) ≈ −0.2%：两倍凯利就不再增长。有上限和时间限制时，目标是达到上限而不是长期增长，略低于凯利同样好。
   在300次、上限250美元的设定下，押10%和20%达到上限的概率都约为94%。
2. **波动率10%、夏普为1。** f* = (μ − r)/σ² = SR/σ = 10，纸面上凯利的超额增长为SR²/2 = 每年50%。但四年测得的夏普比率，
   标准误约为√(1.5/4) ≈ 0.6（第6部分）。若真实夏普为0.5，十倍杠杆就是两倍凯利，增长不比现金快。波动率还可能变成三倍，
   使凯利杠杆除以九（第6章）。应按估计值用半凯利或更低，并随波动率预测重新计算。
3. **为什么不用凯利。** 凯利最大化E log W，即伽马为1的投资者的期望效用。对伽马为3的投资者，最优比例在每个期限上都是凯利的三分之一。
   凯利最终更富的概率趋于一，但它少见的亏损在该投资者的效用中代价极大，所以它的确定性等价更低（第5章：每年−3.6%对+3.9%）。

## 习题与解答

1. **任意赔率下的凯利。** g(f) = p log(1 + bf) + q log(1 − f)。令g′(f) = pb/(1 + bf) − q/(1 − f) = 0，得pb(1 − f) = q(1 + bf)，
   即f* = (pb − q)/b = p − q/b。小优势时展开到二阶：g(f) ≈ f(pb − q) − f²(pb² + q)/2，在f ≈ 2(pb − q)/(pb² + q)处再次为零，
   b = 1时即2(p − q) = 2f*。
2. **默顿的价值函数。** HJB方程为V_t + max_π {(r + π(μ − r))wV_w + ½π²σ²w²V_ww} = 0。代入V = e^{a(T−t)}w^{1−γ}/(1 − γ)，
   则V_t = −aV，wV_w = (1 − γ)V，w²V_ww = −γ(1 − γ)V。除以(1 − γ)V后，HJB化为−a/(1 − γ) + max_π {r + π(μ − r) − ½γπ²σ²} = 0。
   最大值在π* = (μ − r)/(γσ²)处取得，等于r + (μ − r)²/(2γσ²)。所以a = (1 − γ)(r + (μ − r)²/(2γσ²))，且V(T) = u(w)。
3. **分数凯利。** 超额增长g(f) − r = f(μ − r) − ½f²σ²，在f* = (μ − r)/σ²处取最大，此时g* − r = (μ − r)²/(2σ²)。
   在f = cf*处它等于(2c − c²)(g* − r)，波动率为cf*σ。c = ½时得到75%的增长和一半的波动率；c = 2时增长为零，波动率翻倍。
4. **秘书问题。** 若最佳者在位置j > k，当且仅当前j − 1人中最好的那位落在前k人之中时规则会选中他，概率为k/(j − 1)。
   所以P(k) = (k/n)Σ_{j=k+1}^{n} 1/(j − 1)。记x = k/n，这是x∫_x^1 dt/t = −x log x的黎曼和。其导数−log x − 1在x = 1/e处为零，
   此时值为1/e ≈ 36.8%。n = 100时最优k为37，成功率37.1%。
5. **彼得斯的硬币。** 每次押比例f，增长率g(f) = ½log(1 + 0.5f) + ½log(1 − 0.4f)。令g′(f) = 0.25/(1 + 0.5f) − 0.2/(1 − 0.4f) = 0，
   得0.25 − 0.1f = 0.2 + 0.1f，即f* = 0.25。此时g = ½log(1.125 × 0.9) = ½log 1.0125 ≈ 每次+0.62%，而全押每次损失½log(1/0.9) ≈ 5.3%。
   只押四分之一，就把一个亏损的赌博变成了增长的赌博。
