# Quant, Built — Part 9: No Arbitrage

Part 9 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), opening Act III, Derivatives. Two ways to get the same payoff must cost the same.
From that one idea it covers:

* put–call parity and where it breaks: borrow, GameStop, box spreads;
* the fundamental theorem of asset pricing, proved in one period with a separating hyperplane;
* state prices, the stochastic discount factor and the risk-neutral measure;
* the binomial tree, completeness and super-replication as a linear program;
* the continuous-time theorems and changing numeraire;
* the risk-neutral density inside the Surface;
* Ross recovery and its critique;
* model-free bounds by martingale optimal transport.

Every number is computed by the series' own code ([`compute.py`](compute.py), the House's
[`arbitrage`](../../../explainer/quant/house/arbitrage.py) checker, tested) from the Surface: Deribit BTC option
trades on 10 December 2025.

*An education in methods, not investment advice.*

## Chapters (about 40 minutes)

* **One price.** The desk question: call 10, put 7, strike 100, spot 103, no rates. There is no arbitrage, since
  C − P = 3 = S − K. Parity on Bitcoin options, which are inverse, reads C − P = 1 − K/F in BTC.
  * 339 call–put pairs at one strike within ten minutes imply a forward. Half agree with their expiry's median to
    within 3.4 bp on trade prices (1.5 bp on marks), and nine in ten to within 9.9 bp.
  * The implied basis rises from about 3% a year at a few days to 4.8% at six months: crypto's interest rate.

  Then the objectives, and the House's arbitrage checker.
* **1. Arbitrage, parity, and where it breaks.** The definition, and the law of one price. With a borrow fee h,
  C − P = Se^{−hT} − Ke^{−rT}, and option prices reveal h (Ofek, Richardson and Whitelaw 2004). The GameStop crisis
  file, from the SEC staff report (October 2021) and Reuters:
  * about +2,700% from the 8 January intraday low to the 28 January high, then −86% into February;
  * Melvin Capital's $2.75 billion infusion and its −53% January;
  * the staff's finding that enthusiasm, not short covering, sustained the rise.

  Box spreads are loans, but only with European exercise; Robinhood banned them in 2019 after a customer's American
  box was exercised early.
* **2. The fundamental theorem, in one period.** The cone picture has two assets (a bond, and a stock paying 80, 100 or
  125) and three states.
  * At a stock price of 100, positive state prices exist. At 130 the price is outside the cone, and the LP returns
    the separating portfolio θ = (+1.79 bonds, −0.0143 stock), costing −0.071 and paying (0.64, 0.36, 0) in the three
    states.
  * Arrow–Debreu state prices, the SDF m = ψ/π, and Q = (1 + r)ψ (Ross 1978).
* **3. The tree, completeness, and super-replication.** CRR (1979) folding back a four-step call (K = 100,
  σ = 25%, one year), at 9.35.
  * With two states the price is a point. With three or more, the interval for an at-the-money call is [0, 0.197],
    whatever the number of states.
  * Trading the option completes the market. Black–Scholes at 20% gives 0.080 inside the interval.
* **4. Continuous time, and changing numeraire.** The history cards: Harrison–Kreps (1979), Harrison–Pliska (1981),
  Dalang–Morton–Willinger (1990), and Delbaen–Schachermayer (1994, NFLVR). Then Geman–El Karoui–Rochet (1995): the
  T-forward and annuity measures, and Bitcoin as the numeraire of Deribit's inverse options.
* **5. The density inside the Surface.** Breeden–Litzenberger (1978) on SVI fits to the 26 December 2025 expiry
  (16 days) and the 27 March 2026 expiry (107 days).
  * Q(down 20%) is 2.9% at 16 days and 19.1% at 107, against Q(up 20%) of 1.9% and 18.4%.
  * The static and calendar checks pass.
* **6. Ross recovery, and its critique.** In a nine-state CRRA economy, Perron–Frobenius recovers the true transition
  matrix to 1e−15. Add a permanent (martingale) component to the kernel and the recovered matrix is wrong by up to
  0.051, and pessimistic: long-run consumption 2.5% below trend against a true 2.0% above (Borovička, Hansen and
  Scheinkman 2016).
* **7. Bounds without a model.** Martingale optimal transport (Hobson 1998; Beiglböck, Henry-Labordère and Penkner
  2013) uses the House's `mot_bounds`, an LP solved with HiGHS.
  * The marginals are the two densities above, discretized to 25 and 81 atoms. Coarse bins for the earlier marginal
    keep convex order, which is checked.
  * A forward-start straddle |S₂/S₁ − 1| lies in [0.137, 0.218]. Independent log-normal returns at the implied
    forward volatility of 45% give 0.180.
  * The extreme couplings are shown.
* **8. The arbitrage checker.** Rule 10: no model is fitted to a surface that fails the checker, and a model whose
  prices fail it is rejected. The trial counter stays at 72.
* **Recap, desk questions, problems.**

## Build it

```bash
python -m videos.quant.quant9.compute                    # every number, cached in .cache/quant9/ (a minute; the Surface's trades are cached)
EXPLAINER_TTS=silent python tools/qa_scene.py quant9 MOT      # one chapter, silent, with a contact sheet
python tools/make.py quant9 --cpu-voice -q m             # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **Call 10, put 7, K = 100, S = 103, r = 0.** C − P = 3 and S − K = 3: no arbitrage. If the put were 6
   (C − P = 4 > 3), sell the call, buy the put and buy the stock, for a cost of 103 + 6 − 10 = 99, and borrow 99. At
   expiry the package is worth exactly 100 whatever S_T is, so you keep 1. If the put were 8, reverse every leg.
2. **A box on 100/110, one year, r = 4%.** It pays 110 − 100 = 10 in every state, so it is worth 10e^{−0.04} ≈ 9.61.
   Buying a box below that lends at more than 4%; selling it above that borrows at less.
3. **A box of American options.** The short call or short put can be exercised early, leaving a stock position to
   finance and a hedge that no longer offsets. Parity and the box identity assume European exercise.

## Problems, with solutions

1. **Parity with a borrow fee.** The long side of a short sale earns the fee h, so a share held from 0 to T and lent
   out grows to e^{hT} shares. Portfolio A is a call plus Ke^{−rT} in bonds. Portfolio B is a put plus e^{−hT} shares,
   lent out. Both pay max(S_T, K) at T, so C + Ke^{−rT} = P + Se^{−hT}. If C − P > Se^{−hT} − Ke^{−rT}: sell the
   call, buy the put, buy e^{−hT} shares and lend them, and borrow the rest. That takes in the positive difference
   today and pays nothing at T.
2. **The one-period FTAP from Stiemke's lemma.** Consider the subspace L = {(−θ·p, D^⊤θ)} ⊂ ℝ^{1+m}. An arbitrage is
   a θ with L ∋ x ≥ 0, x ≠ 0. No arbitrage means L meets the non-negative orthant only at 0. By Stiemke's lemma (a
   separating-hyperplane theorem), there is then a strictly positive λ ⊥ L: λ₀(−θ·p) + Σ_j λ_j(D^⊤θ)_j = 0 for all θ.
   So p = Dψ with ψ = λ/λ₀ > 0. Conversely, if p = Dψ with ψ > 0, any θ with D^⊤θ ≥ 0 and not 0 has
   θ·p = ψ·D^⊤θ > 0. So not both.
3. **The binomial probability.** Replication or discounting gives S = e^{−rΔt}(qSu + (1 − q)Sd), so
   q = (e^{rΔt} − d)/(u − d). It lies in (0, 1) iff d < e^{rΔt} < u. If e^{rΔt} ≤ d the stock beats the bond in every
   state (buy stock, borrow); if e^{rΔt} ≥ u the bond beats the stock (short stock, lend). Either way there is an
   arbitrage.
4. **Butterflies and the density.** [C(K − h) − 2C(K) + C(K + h)]/h² → C″(K). From C(K) = e^{−rT}∫_K^∞(s − K)q(s)ds,
   C′(K) = −e^{−rT}∫_K^∞ q(s)ds and C″(K) = e^{−rT}q(K). The butterfly's payoff, scaled by 1/h, is a triangle of
   area one around K. So its price tends to the discounted density there.
5. **The trinomial interval.** With S ∈ {80, 100, 125}, r = 0 and K = 100, the call pays (0, 0, 25).
   * Super-replicate with Δ shares and b bonds: b + Δ·S ≥ payoff. The cheapest is Δ = 25/45 = 5/9 and
     b = −80·5/9 ≈ −44.44, paying (0, 11.11, 25) at a cost of 100/9 ≈ 11.11. Below, the zero portfolio is always
     dominated, so the lower bound is 0.
   * The dual: risk-neutral q with 80q₁ + 100q₂ + 125q₃ = 100 and q summing to 1. The call is worth 25q₃, maximized at
     q₃ = 4/9 (with q₂ = 0), giving 11.11, and minimized as q₃ → 0.
   * The interval is (0, 100/9). Its ends are not reached by strictly positive state prices, so they are open.

## Data and reproducibility

* The Surface: Deribit BTC option trades on 10 December 2025, 00:00–12:00 UTC (see
  [`surface.py`](../../../explainer/quant/house/surface.py)); checksummed in [`../data/manifest.json`](../data/manifest.json).
* The Ross economies and the incompleteness example are synthetic, with known truths, and labeled as such on screen.
* No strategy was tested; the trial counter stays at 72.
* GameStop facts come from the SEC staff report (October 2021) and Reuters. The box-spread episode comes from
  Robinhood's public statement; the loss figures reported for it disagree and are not used.

---

# 量化金融，从零搭建 — 第9部分：无套利

衍生品篇的开篇：得到同一收益的两种方法必须同价。由这个想法出发，本部分讲：

* 看涨看跌平价及其失效：借券、游戏驿站、箱式组合；
* 用分离超平面在单期中证明资产定价基本定理；
* 状态价格、随机贴现因子与风险中性测度；
* 二叉树、完备性，以及作为线性规划的超复制；
* 连续时间的定理与计价单位变换；
* 曲面中的风险中性密度；
* 罗斯复原及其批评；
* 用鞅最优传输得到不依赖模型的界。

数据是Deribit在2025年12月10日的比特币期权成交。

*讲的是方法，不构成投资建议。*

## 交易台问题与解答

1. **看涨10、看跌7、执行价100、现价103、利率为零。** C − P = 3，S − K = 3：没有套利。若看跌为6（C − P = 4 > 3），卖出看涨、买入看跌、买入股票，
   成本103 + 6 − 10 = 99，借入99。到期时这个组合无论S_T如何都恰好值100，你留下1。若看跌为8，把每一腿反过来。
2. **100/110的箱式组合，一年，利率4%。** 它在每种状态下都支付10，所以价值10e^{−0.04} ≈ 9.61。低于此价买入，相当于以高于4%的利率放贷；
   高于此价卖出，相当于以低于4%的利率借款。
3. **美式期权的箱式组合。** 卖出的看涨或看跌可能被提前行权，留下需要融资的股票头寸和不再对冲的另一腿。平价和箱式恒等式都假设欧式行权。

## 习题与解答

1. **含借券费用的平价。** 卖空的出借方赚取费用h，所以从0持有到T并出借的一股会增长为e^{hT}股。组合A为一份看涨加Ke^{−rT}的债券；
   组合B为一份看跌加e^{−hT}股并出借。两者在T都支付max(S_T, K)，所以C + Ke^{−rT} = P + Se^{−hT}。若C − P > Se^{−hT} − Ke^{−rT}：卖出看涨、
   买入看跌、买入e^{−hT}股并出借，其余借入。今天收入正的差额，到T不支付任何东西。
2. **由施蒂姆克引理证明单期基本定理。** 考虑子空间L = {(−θ·p, D^⊤θ)} ⊂ ℝ^{1+m}。套利就是使L中的x ≥ 0且x ≠ 0的θ。
   无套利意味着L与非负象限只在0处相交。由施蒂姆克引理（一个分离超平面定理），存在严格为正的λ ⊥ L：对所有θ，
   λ₀(−θ·p) + Σ_jλ_j(D^⊤θ)_j = 0。所以p = Dψ，其中ψ = λ/λ₀ > 0。反过来，若p = Dψ且ψ > 0，任何满足D^⊤θ ≥ 0且不为0的θ
   都有θ·p = ψ·D^⊤θ > 0。所以两者不能同时成立。
3. **二叉树概率。** 由复制或贴现得S = e^{−rΔt}(qSu + (1 − q)Sd)，所以q = (e^{rΔt} − d)/(u − d)。它在(0, 1)中当且仅当d < e^{rΔt} < u。
   若e^{rΔt} ≤ d，股票在每种状态下都胜过债券（买股票、借款）；若e^{rΔt} ≥ u，债券胜过股票（卖空股票、放贷）。两种情况都存在套利。
4. **蝶式价差与密度。** [C(K − h) − 2C(K) + C(K + h)]/h² → C″(K)。由C(K) = e^{−rT}∫_K^∞(s − K)q(s)ds，得C′(K) = −e^{−rT}∫_K^∞q(s)ds，
   C″(K) = e^{−rT}q(K)。蝶式价差的收益除以h后，是K附近面积为一的三角形，所以它的价格趋于那里的贴现密度。
5. **三叉区间。** S ∈ {80, 100, 125}，r = 0，K = 100，看涨期权支付(0, 0, 25)。
   * 用Δ股和b债券超复制：b + Δ·S ≥ 收益。最便宜的是Δ = 5/9、b ≈ −44.44，支付(0, 11.11, 25)，成本100/9 ≈ 11.11。
     下方，零组合总是被看涨期权支配，所以下界为0。
   * 对偶：满足80q₁ + 100q₂ + 125q₃ = 100且q之和为1的风险中性q。看涨期权价值25q₃，在q₃ = 4/9（q₂ = 0）时最大，为11.11；
     在q₃ → 0时最小。
   * 区间是(0, 100/9)。严格为正的状态价格达不到它的两端，所以区间是开的。
