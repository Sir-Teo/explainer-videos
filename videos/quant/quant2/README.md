# Quant, Built — Part 2: The Machinery of Markets

Part 2 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)); the second part of Act I, Markets and Money. It follows a trade from the button to
settlement and measures what the market's plumbing does to anyone who trades: futures and their carry, the order
book, auctions and dealers, clearing and settlement, margin (liquidation on a real crash, and the models that size
margin), short selling, repo and haircuts, prime brokerage, fees and smoothed returns, indices, and the rules of
markets around the world. Every number is computed by the series' own code ([`compute.py`](compute.py), the House's
funding desk in [`explainer/quant/house/funding.py`](../../../explainer/quant/house/funding.py)) from public data
(Binance, FRED, Kenneth French) or from simulations whose generating model is stated on screen. Firms and events are
described from the public record, with allegations labelled as allegations.

*An education in methods, not investment advice.*

## Chapters (about 64 minutes)

* **What happens when you press buy?** A trade's life with a collateral clock; 27–28 January 2021 from the SEC staff
  report: NSCC's intraday calls of $6.9 bn on 36 members ($2.1 bn mark-to-market, $4.8 bn special charge), $25.5 bn
  required in all; the waived excess-capital-premium charge that would have been "more than double" one retail
  broker-dealer's $1.4 bn margin requirement; GameStop short interest 122.97% of float; the history strip (1602–2024).
* **1. Instruments and how they are quoted.** Six instruments; clean and dirty bond prices drawn live; contract specs
  (E-mini: $50 × index, 0.25-point tick; equity options: 100 shares, cleared by the OCC); notional, DV01, leverage.
* **2. Futures: carry, basis and the hedge.** F = Se^{(r−q)T} by cash-and-carry and reverse carry; Binance's
  coin-margined March-2021 BTC future against spot, hour by hour (10 Feb 2021: 5.09% over spot, 40.9% a year; mean
  24.7%, max 57.2% with more than 10 days left); the minimum-variance hedge h* = ρσ_S/σ_F and effectiveness ρ²; 3D:
  hedge variance over (h, ρ); lab: ETH hedged with BTC, h* = 1.11 (bootstrap 1.01–1.22), 68% of variance removed in
  2021–22, 65% out of sample in 2023.
* **3. The order book.** Order types, validity, hidden and iceberg orders, price–visibility–time precedence; a
  zero-intelligence book (Smith et al. 2003) running as queues; the cost of walking the book (half-spread plus walk)
  against simulated books (concave); spreads 2.0 / 3.1 / 5.4 ticks as the market-order rate rises; Rule 612 (2024),
  compliance moved to November 2027.
* **4. Auctions: one price for everyone.** 300 orders building the staircases live; proof that the crossing maximizes
  volume; a 2,000-share market-on-close buy moves the clearing price 100.07 → 100.14 (walking the book instead:
  average 100.13, last 100.17); closing auctions 7.5% of US volume in 2018 (Bogousslavsky–Muravyev); lab:
  `call_auction`.
* **5. Dealers, RFQ and wholesalers.** Best of n quotes (order statistics, √(2 ln n)) against leakage λ: n* = 4 at
  λ = 0.15σ; simulated markouts (retail against informed flow); wholesaler economics; GameStop internalization (SEC);
  Ernst–Spatt; Battalio–Corwin–Jennings.
* **6. Clearing: novation, netting, the waterfall.** The netting graph collapsing into the CCP ($11.0 bn → $3.1 bn →
  $1.0 bn, −91%); proof of M ≤ B ≤ G; NSCC's 98%; Duffie–Zhu (clearing one of K classes helps only if
  N − 1 > (√K − √(K−1))⁻²: N ≥ 39 for K = 10), Monte Carlo against the formula; a default waterfall under 10⁵ t-shocks
  (the worst-hit member's loss passes its margin on 9.3% of days, reaches survivors' money on 2.8%); cover-2; lab:
  `netting`.
* **7. Settlement and the deposit.** DVP, CNS, the clearing fund (99% parametric VaR, MTM, special charges, ECP); the
  settlement conveyor: a volatility spike to 400% multiplies the deposit 6.8×; T+2 → T+1 cuts it 50% for one-way flow
  but 30% for two-way flow; the real T+1 after-action numbers (clearing fund −$2.4 bn, −20%; affirmation 73% → ~95%).
* **8. Margin and liquidation.** IM/VM/maintenance; P_liq = P₀(1 − 1/L)/(1 − m); March 2020 run live hour by hour with
  three accounts' equity (10× on 9 March, 3× on 12 March, 2× on 13 March at $4,063, $271 below zero); lab:
  `margin_account`; funding 17% a year in 2020; the reflection principle P = 2Φ(−d/σ√H); 3D: the empirical
  liquidation surface over leverage × horizon from BTC hourly lows 2020–25 against the formula (10×, 19 days: 37% in
  data, 50% by the formula; fat tails at short horizons, drift at long ones).
* **9. How much margin?** SPAN's 16 scenarios; EWMA VaR margin; 1987 as a breathing band (2-day margin 3.5% on 16 Oct
  → 11.7% on 20 Oct); λ fitted by likelihood, replayed (0.936 for the US market, 0.973 for BTC); breaches 2.09% vs 1%
  (Kupiec LR 226); procyclicality (×5.9 in 1987, ×4.0 in 2008, ×7.6 in 2020); EMIR anti-procyclicality tools; LME
  nickel 2022; UK LDI 2022; lab: `ewma_margin`.
* **10. Short selling and the squeeze.** Fee, rebate, dividends, specials (100 → 90: +14.84 at GC, −5.30 at a 20% fee);
  D'Avolio's numbers; short interest above 100% by relending; a squeeze against free float (runaway above about
  1.1× the free float); Volkswagen, October 2008 (about 6% free float).
* **11. Repo, lending and specials.** Repo arithmetic, tri-party and bilateral (Copeland–Martin–Walker); the
  collateral tower (1/h) and its crumble (sales 50, 24.7, 6.1 … = 1.63× the first round); ten funds' spiral
  (Brunnermeier–Pedersen; 5.8×/2.6×/1.7× at 3/4/6% haircuts); specials (Duffie 1996); lab: `deleverage`.
* **12. The day repo broke.** The SOFR percentile fan (99th percentile 2.40% → 4.60% → 9.00% on 13/16/17 Sep 2019,
  median 5.25%); reserves; the reserve demand curve fitted by Gauss–Newton and replayed with bootstrap bands
  (+15.3 bp mean, +82.6 bp max below $1.5 tn; −9.6 bp above $3.5 tn); Afonso et al. (2021).
* **13. Prime brokers and the race to sell.** TRS economics; the race L_j = λq²(j − ½), the last seller losing
  (2K − 1)× the first; square-root impact with random orders (loss by rank, 8 seeds); the prisoner's dilemma;
  Archegos (SEC allegations; Credit Suisse ~$5.5 bn, Nomura ~$2.9 bn as reported); Duffie (2010).
* **14. Who earns what.** Sell and buy side; 2 and 20 on 1927–2020 ($7,893 → $360, the investor keeps 4.5% of the
  profit); the performance fee as a call; Fung–Hsieh; Getmansky–Lo–Makarov smoothing (Sharpe ×1.62 for
  θ = (0.5, 0.3, 0.2)); smallest size decile AC1 0.40 (1963–89) vs 0.04 (1990–2020); the MLE fit replayed over five
  seeds against the moment estimator.
* **15. Benchmarks and indices.** Cap, float and price weights; inclusion demand; the Russell gate; Shleifer,
  Harris–Gurel, Chang–Hong–Liskovich, Pavlova–Sikorskaya, Greenwood–Sammon; a simulated regression discontinuity (true
  jump 1.5%, recovered at every bandwidth, s.d. 0.12 → 0.45 points as the bandwidth shrinks).
* **16. Markets around the world.** US, EU/UK T+1 (11 Oct 2027), Japan, India (SEBI: 93% FY22–24, 91% FY25), China
  (T+1, ±10%/±20%, 2024 rules); the price-limit spring; simulated limits create AC1 0.12 at ±10% (0.04 at ±20%).
* **17. Industry: who runs the machine.** The money map; firm files (CME, Virtu, Robinhood, Citadel Securities),
  the basis trade, regulators (SEC, FCA, SEBI's Jane Street interim order: allegations); the quant map and roles.
* **18. Frontier, 2023 to 2026.** Six papers and the rule changes (T+1, Rule 612's delay, Treasury clearing, 13f-2 and
  10c-1a, EU/UK T+1).
* **For the researcher: backtesting a margin model.** Kupiec's likelihood ratio and Wilks's $\chi^2_1$ limit, proved by a second-order expansion; at 250 days the exact size of the nominal 5% test is 9.5% (it rejects 0 and 7 or more breaches; 12 distinct values), 5.5% at 1,000 days; the Basel traffic light puts a correct model in yellow or red 10.8% of years. Christoffersen's Markov independence and conditional-coverage tests. Simulated GARCH(1,1): a constant margin with the right long-run variance is breached 1.5% of days and fails $\text{LR}_{uc}$ 54% of the time but $\text{LR}_{ind}$ only 26%; EWMA 8% and 6%. The US market 1926–2020 (24,876 days): EWMA breached 2.1% of days ($\text{LR}_{ind}$ 34), the constant margin 1.9% with 195 breaches in the 1930s ($\text{LR}_{ind}$ 94). Three open problems (duration tests; backtesting expected shortfall; estimation error).
* **The funding desk; recap, desk questions, problems.**

## Build it

```bash
python -m videos.quant.quant2.compute                     # every number, cached in .cache/quant2/ (~6 CPU-minutes)
EXPLAINER_TTS=silent python tools/qa_scene.py quant2 Margin  # one chapter, silent, with a contact sheet
python tools/make.py quant2                               # English and Chinese
```

## Textbook audit

| Book · section | Where |
|---|---|
| Hull OFOD 1 (forwards, futures, options; types of traders) | ch. 1, 2, 17 |
| Hull 2 (futures markets: specs, convergence, daily settlement, margin, CCPs, delivery, forwards vs futures) | ch. 1, 2, 6, 8 |
| Hull 3 (hedging: basis risk, cross hedge, minimum-variance ratio, beta hedge, stack and roll) | ch. 2 |
| Hull 5 (forward and futures prices: carry, known yield, valuing forwards) | ch. 2; FX and commodities → Part 22 |
| Hull 5 (short selling) | ch. 10 |
| Hull 4, 6, 7 (interest rates, rate futures, swaps) | quoting in ch. 1 → Part 18 |
| Hull 10 (mechanics of options markets: specs, OCC, margin on written options) | ch. 1, 9; strategies → Part 11 |
| Harris 1–2 (introduction; the trading industry) | ch. 14, 17 |
| Harris 3 (orders: market, limit, stop; DAY/GTC/IOC/FOK; hidden, iceberg) | ch. 3 |
| Harris 4 (market structures: quote- and order-driven, brokered; continuous vs call; transparency) | ch. 3, 4, 5 |
| Harris 5 (order-driven markets: precedence rules; uniform vs discriminatory pricing) | ch. 3, 4 |
| Harris 6 (brokers: principal–agent, best execution) | ch. 5 |
| Harris 7–8 (why people trade; good markets) | Part 1; Part 35 |
| Tuckman–Serrat, repo (GC and special, specialness, tri-party, leverage) | ch. 11, 12 |
| Pedersen 1 (hedge funds, fees, high-water mark) | ch. 14 |
| Pedersen 5 (trading and financing: margin, funding liquidity, spirals) | ch. 8, 9, 11, 13; Part 41 |
| Pedersen 2–4 (performance measures, backtesting, portfolio construction) | Parts 26, 30 |
| Mishkin (the financial system, money markets) | ch. 11, 12 (overview) |

## Papers and sources (reading guide)

Every paper on this part's list in [`READING.md`](../READING.md) appears on screen: Shleifer (1986), Harris–Gurel
(1986) and Chang–Hong–Liskovich (2015) in ch. 15; D'Avolio (2002) in ch. 10; Duffie (1996) and Copeland–Martin–Walker
(2014) in ch. 11; Brunnermeier–Pedersen (2009) in ch. 11; Duffie (2010) in ch. 13; Battalio–Corwin–Jennings (2016)
and Ernst–Spatt (2022, NBER WP 29883) in ch. 5; Fung–Hsieh (1997) and Getmansky–Lo–Makarov (2004) in ch. 14;
Smith–Farmer–Gillemot–Krishnamurthy (2003) in ch. 3; Bogousslavsky–Muravyev (2023, *Journal of Financial Markets*)
in ch. 4; Duffie–Zhu (2011) in ch. 6; Afonso et al. (2021) in ch. 12; the SEC staff report (2021) in the hook and
ch. 5, 7, 10; Rule 612 (2024) in ch. 3 and 18; SEBI's studies in ch. 16; and the frontier papers (Greenwood–Sammon
2025, Pavlova–Sikorskaya 2023, Bryzgalova–Pavlova–Sikorskaya 2023, Schwarz et al. 2025, Glicoes et al. 2024 and
Monin 2026, Pinter 2023, Duffie 2023) in ch. 18. Facts checked against primary sources for this edition: the SEC staff
report's NSCC figures (section 3.5) and footnote 75; SEC exemptive order 34-105656 (11 June 2026: Rule 612 and the
access-fee cap delayed to the first business day of November 2027); CME's SPAN risk arrays (16 scenarios, extremes at
3 scan ranges counting 30%); ESMA's guidelines on EMIR Art. 28 (25% buffer; 10-year look-back floor); NSCC's 98%
netting; D'Avolio (2002), p. 271–272; the SIFMA–ICI–DTCC T+1 after-action report; the FCA's LME fine (£9.2 m, March
2025); SEC press release 2022-70; SEBI's interim order (allegations; the matter is pending).

## Desk questions, with solutions

1. **Make me a market on the number of trading days in a US year.** 365 days less 104 weekend days is 261 weekdays;
   the NYSE closes for 9 or 10 holidays, so a year has about 250–252 trading days. A tight market, say 249 bid at 252
   offered, shows you know the answer; the game is how you move the quote when you are hit.
2. **Future 102, spot 100, six months, 3%, no yield.** Fair value is 100e^{0.03×0.5} = 101.51. The future is rich:
   borrow 100, buy spot, sell the future at 102; at expiry deliver, receive 102, repay 101.51: 0.49 locked in, less
   costs (and the margin the short future needs along the way).
3. **Short interest at 120% of float.** Shares are lent, sold, and lent again by their buyers, so the same share is
   counted short more than once (SEC staff report, footnote 75). Every short is a future buyer of a float that may run
   out: the risk is a squeeze, plus recalls and rising borrow fees.

## Problems, with solutions

1. **Liquidation odds.** d = −ln[(1 − 1/L)/(1 − m)]: 0.218 at 5×, 0.100 at 10×. With σ = 4% a day and H = 30,
   σ√H = 0.219, so P = 2Φ(−d/σ√H): 2Φ(−0.995) = 32% at 5×, 2Φ(−0.458) = 65% at 10×. Doubling leverage more than
   halves the distance (the maintenance margin eats into it) and doubles the odds.
2. **Netting.** G = 10 + 10 + 10 + 5 = 35. Bilateral: A–B 10, B–C 10, C–A 10 against 5 leaves 5: B = 25. Net
   positions: A −5, B 0, C +5, so M = 5 ≤ 25 ≤ 35.
3. **The deleveraging loop.** At the new haircut h′ the fund must cut assets to E/h′: a first sale s₀ = A(1 − h/h′).
   Each unit sold lowers the price by λ, which costs equity ≈ Aλ per unit and forces a further sale ≈ Aλ/h′ per unit:
   a loop with gain g = Aλ/h′. If g < 1 the sales converge to s₀/(1 − g); if g ≥ 1 there is no fixed point short of
   selling everything, and the equity is gone once the cumulative price fall exceeds E/A.
4. **Hedge ratio.** h* = ρσ_S/σ_F = 0.8 × 1.25 = 1.0; effectiveness ρ² = 0.64.
5. **Smoothing.** Σθ² = 0.36 + 0.09 + 0.01 = 0.46. True Sharpe = reported × √0.46 = 1.5 × 0.678 = 1.02. Reported
   ρ₁ = (θ₀θ₁ + θ₁θ₂)/Σθ² = (0.18 + 0.03)/0.46 = 0.46.

6. **(qual) Wilks for Kupiec.** With $\ell(q) = x\ln q + (T - x)\ln(1 - q)$, $\text{LR}_{uc} = 2[\ell(\hat p) -
   \ell(p)]$. Taylor-expand $\ell(p)$ around $\hat p$: $\ell'(\hat p) = 0$ and $\ell''(\hat p) = -T/(\hat p(1 - \hat p))$,
   so $\text{LR}_{uc} = T(\hat p - p)^2/(\hat p(1 - \hat p)) + O_p(T^{-1/2})$, and $\hat p \to p$ makes the denominator
   $p(1 - p)$. Under $H_0$, $\sqrt T(\hat p - p)/\sqrt{p(1 - p)} \Rightarrow N(0, 1)$ (the CLT for Bernoulli draws), so
   its square, and $\text{LR}_{uc}$ by Slutsky, tends to $\chi^2_1$.
7. **(qual) Christoffersen.** The Markov likelihood is $(1 - \pi_{01})^{n_{00}}\pi_{01}^{n_{01}}(1 - \pi_{11})^{n_{10}}
   \pi_{11}^{n_{11}}$; each factor is a Bernoulli likelihood, so $\hat\pi_{01} = n_{01}/(n_{00} + n_{01})$ and $\hat\pi_{11} =
   n_{11}/(n_{10} + n_{11})$. Independence is the one restriction $\pi_{01} = \pi_{11}$, so Wilks gives $\chi^2_1$ (with
   $p$ interior, the chain ergodic and both rows' counts growing). For 4 breaches in 250 days, three in a row:
   $n_{01} = 2$, $n_{11} = 2$, $n_{10} = 2$, $n_{00} = 243$, $\hat\pi_{01} = 0.008$, $\hat\pi_{11} = 0.5$;
   $\text{LR}_{uc} = 0.77$ (the count is fine), $\text{LR}_{ind} = 12.2$, $\text{LR}_{cc} = 13.0$ ($p$ = 0.002):
   independence rejects. With so few breaches the $\chi^2$ approximation is rough, and an exact or simulated $p$-value
   is better.

## For the researcher

* **The theorems.** Wilks (1938) for both likelihood ratios; Kupiec (1995) and Christoffersen (1998) for the tests.
  Their asymptotics need many breaches: at $p$ = 1% and $T$ = 250 there are about 2.5, so exact binomial (or
  simulated Markov) distributions should replace $\chi^2$ in practice.
* **Simplifications.** The video ignores the estimation of the margin's parameters (Escanciano and Olmo 2010 show the
  test's size changes), and its GARCH simulation uses normal shocks; Student-$t$ shocks raise the breach rate of any
  normal-quantile margin further.
* **Reading.** Wilks (1938); Kupiec (1995); Christoffersen (1998); Christoffersen and Pelletier (2004); Engle and
  Manganelli (2004); Escanciano and Olmo (2010); Gneiting (2011); Fissler and Ziegel (2016); Acerbi and Szekely (2014);
  Basel Committee, *Supervisory framework for the use of backtesting* (1996).
* **Open problems.** Tests with power against realistic, longer-lag clustering; backtesting expected shortfall;
  inference that accounts for an estimated margin.

## Data and reproducibility

* Binance's public archive (data.binance.vision), each file checked against Binance's SHA-256 and recorded in
  [`videos/quant/data/manifest.json`](../data/manifest.json): USD-M BTCUSDT perpetual hourly and daily candles and
  funding (2020); **coin-margined BTCUSD_210326 hourly (December 2020 – March 2021), new in this edition**; spot
  BTCUSDT hourly 2020–25 and daily 2018–25; spot ETHUSDT daily 2021–23.
* FRED: SOFR, **SOFR1, SOFR25, SOFR75, SOFR99 (new)**, DFF, IOER, IORB, WRESBAL; frozen windows through 2025.
* Kenneth French: daily US market and size deciles, research window to 2020.
* Simulations (seeded): the zero-intelligence book, the auction, RFQ and markouts, the netting day, Duffie–Zhu, the
  waterfall, the settlement belt, the squeeze, the spiral, the fire sale, GLM fits, the Russell RD, price limits.
* The House's new functions (`funding.py`, tested in `tests/test_quant_house.py`): `min_var_hedge`,
  `hedge_effectiveness`, `implied_carry`, `ewma_var`, `ewma_margin`, `ewma_loglik`, `fit_ewma_lambda`, `kupiec`,
  `liquidation_probability`, `ccp_waterfall`, `short_pnl`, `deleverage`, `fire_sale`, `glm_smooth`, `glm_fit`.

---

# 量化金融，从零搭建 — 第2部分：市场的机器

本部分跟随一笔交易从按下按钮直到结算，并测量市场的“管道”对每个交易者做了什么：期货与持有成本、订单簿、集合竞价与交易商、清算与结算、
保证金（真实崩盘中的强平，以及确定保证金的模型）、卖空、回购与折扣率、主经纪商、费用与平滑收益、指数，以及世界各地市场的规则。
所有数字都由本系列自己的代码根据公开数据或注明模型的模拟算出；公司和事件取自公开记录，指控均注明为指控。

*讲的是方法，不构成投资建议。*

## 各章（约60分钟）

开场：一笔交易的生命周期，以及SEC工作人员报告中的2021年1月27–28日（NSCC对36家会员日内追缴69亿美元，总要求255亿美元；
被豁免的超额资本溢价对一家零售经纪商而言“超过其14亿美元保证金要求的两倍”；GameStop空头仓位达流通股的122.97%）。
1. 金融工具及其报价（净价与全价、合约规格、名义本金）。2. 期货：持有成本、基差与对冲（比特币季度期货逐小时收敛；最小方差对冲比率，
三维方差曲面；以太坊用比特币对冲的实验）。3. 订单簿（零智能模型、吃单成本、612规则推迟到2027年11月）。4. 集合竞价（成交量最大化的证明、
收盘市价单）。5. 交易商、询价与批发商。6. 清算（净额结算图、M ≤ B ≤ G的证明、达菲–朱、违约瀑布）。7. 结算与保证金存款（传送带、
T+1的实际效果）。8. 保证金与强平（2020年3月逐小时、反射原理、三维强平概率曲面）。9. 保证金该收多少（SPAN、EWMA、似然拟合、
库皮耶克检验、顺周期性）。10. 卖空与轧空（大众汽车）。11. 回购、证券借贷与特殊券（抵押品之塔与螺旋）。12. 回购市场崩坏的那一天
（SOFR百分位扇形、准备金需求曲线）。13. 主经纪商与抛售竞赛（Archegos）。14. 谁赚什么钱（费用、平滑收益）。15. 基准与指数
（罗素断点回归）。16. 世界各地的市场（涨跌停弹簧）。17. 行业。18. 前沿。结尾：资金台、回顾、交易台问题与习题。

## 交易台问题与解答

1. **给美国一年的交易日数报个价。** 365天减去104个周末日是261个工作日；纽交所每年休市9到10天，所以约250到252个交易日。
   报一个窄的价差，比如249买、252卖；这个游戏真正考的是被成交之后你如何调整报价。
2. **期货102，现货100，六个月，利率3%，无收益。** 公允价值100e^{0.015} = 101.51。期货偏贵：借100买入现货，以102卖出期货；
   到期交割收102，还101.51：锁定0.49，扣除成本（以及期货空头途中所需的保证金）。
3. **空头仓位是流通股的120%。** 股票被借出、卖出，买方又再借出，同一股被重复计为空头（SEC工作人员报告脚注75）。
   每个空头都是未来的买家，而可买的流通股可能耗尽：风险是轧空，以及召回和借券费上升。

## 习题与解答

1. **强平概率。** d = −ln[(1 − 1/L)/(1 − m)]：5倍为0.218，10倍为0.100。σ = 每天4%、H = 30时σ√H = 0.219，
   P = 2Φ(−d/σ√H)：5倍为2Φ(−0.995) = 32%，10倍为2Φ(−0.458) = 65%。杠杆翻倍，距离缩短超过一半（维持保证金吃掉一部分），概率翻倍。
2. **净额结算。** G = 10 + 10 + 10 + 5 = 35。双边：A–B 10，B–C 10，C–A 10与5相抵剩5：B = 25。净头寸：A −5，B 0，C +5，
   所以M = 5 ≤ 25 ≤ 35。
3. **降杠杆循环。** 新折扣率h′下，基金必须把资产降到E/h′：第一轮卖出s₀ = A(1 − h/h′)。每卖一单位价格下跌λ，权益约损失Aλ，
   又需多卖约Aλ/h′：循环增益g = Aλ/h′。g < 1时总卖出收敛到s₀/(1 − g)；g ≥ 1时没有不动点，只能全部卖出，
   累计跌幅超过E/A时权益归零。
4. **对冲比率。** h* = ρσ_S/σ_F = 0.8 × 1.25 = 1.0；有效性ρ² = 0.64。
5. **平滑。** Σθ² = 0.36 + 0.09 + 0.01 = 0.46。真实夏普 = 报告值 × √0.46 = 1.5 × 0.678 = 1.02。报告收益的一阶自相关
   ρ₁ = (θ₀θ₁ + θ₁θ₂)/Σθ² = (0.18 + 0.03)/0.46 = 0.46。

6. **（资格考试）库皮耶克检验的威尔克斯定理。** 令$\ell(q) = x\ln q + (T - x)\ln(1 - q)$，$\text{LR}_{uc} = 2[\ell(\hat p) -
   \ell(p)]$。在$\hat p$处泰勒展开，$\ell'(\hat p) = 0$，$\ell''(\hat p) = -T/(\hat p(1 - \hat p))$，所以$\text{LR}_{uc} =
   T(\hat p - p)^2/(\hat p(1 - \hat p)) + O_p(T^{-1/2})$。原假设下$\sqrt T(\hat p - p)/\sqrt{p(1 - p)} \Rightarrow N(0, 1)$，
   其平方以及$\text{LR}_{uc}$都趋于$\chi^2_1$。
7. **（资格考试）克里斯托弗森检验。** 马尔可夫似然的每个因子都是伯努利似然，所以$\hat\pi_{01} = n_{01}/(n_{00} + n_{01})$，
   $\hat\pi_{11} = n_{11}/(n_{10} + n_{11})$；独立性是一个约束$\pi_{01} = \pi_{11}$，由威尔克斯定理得$\chi^2_1$。250天内4次击穿、
   其中三次连续：$n_{01} = 2$，$n_{11} = 2$，$n_{10} = 2$，$n_{00} = 243$；$\text{LR}_{uc} = 0.77$，$\text{LR}_{ind} = 12.2$，
   $\text{LR}_{cc} = 13.0$（$p$ = 0.002）：独立性检验拒绝。击穿这么少时卡方近似很粗糙，最好用精确或模拟的$p$值。

## 数据与复现

币安公开数据（逐文件SHA-256校验并记入`videos/quant/data/manifest.json`），其中本版新增币本位季度合约BTCUSD_210326；
FRED（新增SOFR1、SOFR25、SOFR75、SOFR99）；肯尼斯·弗伦奇数据库；所有模拟均固定随机种子。

## 写给研究者

两个似然比都依赖威尔克斯定理（1938）；检验来自库皮耶克（1995）和克里斯托弗森（1998）。它们的渐近理论需要很多次击穿：$p$ = 1%、
$T$ = 250时只有约2.5次，所以实践中应改用精确的二项分布（或模拟的马尔可夫分布）。开放问题：对现实中更长滞后的聚集有功效的检验；
预期短缺的回测；考虑保证金参数估计误差的推断。
