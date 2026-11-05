# Quant, Built — Part 39: Crypto and DeFi

Part 39 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the last part of Act VI, Market Microstructure, built to the series' PhD layer. It
finds the dealer, the book, the executor and the market maker of Parts 35–38 again in crypto:
* pools that are market makers by formula;
* perpetual futures held to spot by funding;
* stablecoins that are banks without insurance;
* venues whose failure no backtest contains.

Measurement uses Binance's public archive:
* hourly spot and USD-M perpetual candles and eight-hourly funding for BTC and ETH, January 2020 to December 2025;
* one-minute ETHUSDT candles for 2023;
* USDCUSDT in March 2023;
* USTUSDT, LUNAUSDT and FTTUSDT around their collapses.

It also uses Yahoo Finance bars for GBTC and IBIT. The models are constant-product and concentrated pools traded by
the House's arbitrage simulator, a sandwich solver, Binance's funding rule and the perpetual's no-arbitrage price,
and a learned liquidity provider in simulation.

The part covers:

* **Blockchains and exchanges:**
  * ledgers, proof of work and of stake, gas, and who orders a block;
  * centralised and decentralised venues; 24/7 trading;
  * the exchange as broker, venue and clearing house, with insurance funds and auto-deleveraging.
  * **FTX, as reported and as established at trial:** FTT went from $26 to $1.23 in November 2022 on Binance. The
    lessons are venue risk, collateral and own-token balance sheets.
  * Stablecoins as the cash leg.
* **Automated market makers:**
  * **The constant product x·y = k.** On a 5,000 ETH / $10m pool, buying 10, 100, 500 and 1,000 ETH costs 0.5%,
    2.3%, 11.4% and 25.4% above $2,000 (0.3% fee).
  * General CFMMs, Balancer and stableswap; arbitrage; the pool as an oracle (Angeris and Chitra 2020) and flash loans.
  * Impermanent loss, 2√r/(1 + r) − 1: −5.7% at r = 2 or ½, and −20% at r = 4.
* **What liquidity providers lose (Milionis, Moallemi, Roughgarden and Zhang 2022):**
  * hold, pool and rebalancing portfolios on ETH's 2023 path: 1.454, 1.381 and 1.413 of the start;
  * impermanent loss decomposed into LVR (−0.032) and a market part (−0.041);
  * LVR measured minute by minute: 2.659% of value against σ²/8 = 2.659%, equal month by month;
  * 2.55–2.77% at any arbitrage frequency, from one minute to one day.
  * **Break-even volume.** A 0.3% pool needed about nine times its value in non-arbitrage volume, 2.4% a day.
  * A hedged LP is short gamma (Part 11).
* **Concentrated liquidity (Uniswap v3):**
  * reserves on a range, and the covered-call shape;
  * capital efficiency 1/(1 − w^−1/2): 201× at ±1%, 41× at ±5%, 21× at ±10%, 3.4× at ×2;
  * how often ETH left daily-centred ranges in 2023: 89% of days at ±1%, 13% at ±5%;
  * LVR and fees both scale with efficiency.
  * **A learned LP**, by tabular one-step Q-learning in a two-regime simulation. Every fixed range lost on 2,000 test
    days (−13 to −30 bp a day). The learned policy, narrow when calm and out when stormy, earned +17 bp a day,
    against +21 for a regime oracle.
* **Order is worth money:**
  * proposer-builder separation and MEV;
  * **a sandwich, worked.** In Chapter 2's pool a $10k trade is not worth attacking at any tolerance. $100k at 1%
    yields $700 and $1m at 3% yields $31.7k;
  * the kinds of MEV (Daian et al. 2020); LVR as the largest MEV; defences, including batch auctions (CoW Swap).
* **Perpetual futures:**
  * funding mechanics and Binance's rule (premium plus a clamped 0.01% interest term);
  * the no-arbitrage price F = κS/(κ − (r − q)) (He, Manela, Ross and von Wachter 2022);
  * six years of funding.
    * Bitcoin averaged 12.8% a year: 31% in 2021, 4% in 2022 and 5% in 2025. Ether averaged 15.3%.
    * 37% of BTC settlements sat at exactly 0.01%. In 2022, 22% were negative. In 2025 the rate never rose above
      0.01%.
    * Binance's rule applied to the hourly premium correlates 0.86 with the rate set (0.93 for ETH).
* **The carry trade, registered:**
  * long spot, short perpetual, a third margin, 15 bp a switch; nine variants on 2020, the only year the public
    funding files allow;
  * the best (ETH, always on: 22.0%, Sharpe 4.6) was registered with nine trials (counter 23,559) and opened on
    2021–2025: 10.2% a year, Sharpe 2.16 ± 0.23, worst drawdown −1.2%.
    * By year: +32.2%, +0.5%, +6.2%, +10.2%, +3.8%.
  * Why it decayed: crowding (Ethena's USDe, as reported) and the rule's cap.
  * **The tail the returns omit.** The margin at the venue is 25% of capital, about 2.5 years of carry.
  * A premium, not an arbitrage.
* **Stablecoins and runs:**
  * three kinds; Diamond and Dybvig (1983) on chain, with numbers;
  * **USDC in March 2023.** Binance's series opens at 0.882, spends 33 hours below 98 cents and is back above
    99.5 cents 52 hours after the low. 8% of reserves at SVB implies 0.92 even with zero recovery: liquidity, not
    solvency;
  * peg arbitrage (Lyons and Viswanath-Natraj);
  * Terra's mint-and-burn spiral: UST to 0.23 and LUNA from $78 to $0.00004;
  * contagion and the courts, as reported; MiCA and the GENIUS Act.
* **Venues, funds and the cross-section:**
  * Makarov and Schoar (2020) on cross-border premiums; price discovery on the perpetual (Part 35);
  * GBTC's discount: its price over Bitcoin's rose 74% from end-2022 to the ETF approval;
  * spot ETFs: IBIT traded $1.0bn on day one and $1.4bn a day in 2024;
  * the crypto cross-section (Liu, Tsyvinski and Wu 2022; Part 27);
  * firms from the public record: the SEC's settled order with Tai Mo Shan; token market-maker cases; Binance's 2023
    plea.
* **Rule 39: count the risks the returns do not show.** The sheet; venues, contracts and keys; four labs; three cases.
* **For the researcher: loss-versus-rebalancing.**
  * The theorem by the envelope lemma and Itô.
  * An exact discrete identity with its expectation.
  * The fee band's stationary law and the trade probability.
  * Five checks, including real ETH prices, on which arbitrageurs keep 2.3 times the Brownian share at a 0.3% fee.

One strategy is registered in this part; the trial counter stands at 23,559.

*An education in methods, not investment advice.*

## Chapters (about 57 minutes)

* **Hook: an LP's loss when the price doubles.** The question; three findings; why it matters; where this sits;
  seventeen years; the plan.
* **1. Blockchains and exchanges.** The ledger; consensus; two venues; always open; clearing; FTX; lessons; the cash
  leg.
* **2. Automated market makers.** The invariant; a trade on the curve; slippage; the general form; arbitrage; the
  oracle; impermanent loss and its curve.
* **3. What liquidity providers lose.** Three benchmarks; ETH's 2023 paths; the decomposition; why rebalancing; the
  formula; by frequency; break-even; short gamma.
* **4. Concentrated liquidity.** Ranges; holdings; efficiency; leaving the range; LVR scaling; a learned LP (setup,
  values, results, caveats).
* **5. Order is worth money.** The pipeline; a sandwich step by step; its limit; the prize table; kinds of MEV; LVR as
  MEV; defences.
* **6. Perpetual futures.** Mechanics; Binance's rule; the no-arbitrage price; the interest term; six years; by year;
  rule against data; who pays.
* **7. The carry trade, registered.** The book; risks; nine variants; registration; the envelope; by year; the curve;
  decay; the hidden tail; a premium.
* **8. Stablecoins and runs.** Kinds; Diamond–Dybvig; numbers; USDC by the minute; reading the price; peg arbitrage;
  Terra's mechanism and collapse; lessons; rules.
* **9. Venues, funds and the cross-section.** Makarov–Schoar; price discovery; the trust; GBTC's discount; the ETFs;
  the cross-section; firms.
* **10. Rule 39.** The answer; the sheet; venues; contracts; keys; four labs; the module; three cases.
* **For the researcher: loss-versus-rebalancing.**
  * Model; two lemmas; the theorem and its proof; corollaries.
  * The exact discrete version; checks by simulation, concentrated position and ETH.
  * Fees and blocks; the stationary law; the second theorem; checks with Poisson blocks, fixed blocks and real prices.
  * Meaning; related work; open problems.
* **Outro.** Thirteen lines; three lessons; the part on one card; connections; six desk questions; the pause answer;
  twelve problems (two of qualifying-exam level, solved below); payoffs; references.

## Hands-on

* **Built and run here:**
  * a constant-product pool and slippage;
  * LVR on 525,520 ETH minutes;
  * the arbitrage simulator with fees, for Poisson, fixed and real blocks;
  * concentrated ranges on 2023's days;
  * a tabular learned LP;
  * a sandwich solver;
  * six years of BTC and ETH funding against the premium;
  * the cash-and-carry book, registered and opened;
  * USDC, UST, LUNA and FTT through their crises;
  * GBTC and IBIT.
* **Labs, from the House's source:** `arb_pool`, `lvr_step_cpmm` with `lvr_rate_cpmm` and `p_trade_theory`, `sandwich`,
  and `binance_funding_rule` with `perp_multiplier`.

## Textbook audit

| Textbook | Sections | Chapters |
|---|---|---|
| Harvey, Ramachandran and Santoro, *DeFi and the Future of Finance* (2021) | DEXs, lending, stablecoins, risks | 2, 5, 8 |
| Narayanan, Bonneau, Felten, Miller and Goldfeder, *Bitcoin and Cryptocurrency Technologies* (2016) | ledgers, consensus, custody | 1 |

## Papers, chapter by chapter

* ch. 1: Nakamoto (2008); Buterin (2014).
* ch. 2: Adams et al., Uniswap v2/v3 whitepapers (2020, 2021); Angeris and Chitra (2020), *ACM AFT*; Egorov (2019),
  stableswap whitepaper.
* ch. 3: Milionis, Moallemi, Roughgarden and Zhang (2022).
* ch. 4: Adams et al. (2021); Lehar and Parlour (2025), *JF* *(verify)*.
* ch. 5: Daian et al. (2020), *IEEE S&P*; Qin, Zhou and Gervais (2022), *IEEE S&P*.
* ch. 6: He, Manela, Ross and von Wachter (2022); Ackerer, Hugonnier and Jermann (2024) *(verify)*.
* ch. 7: the series' sealed envelope (Part 1).
* ch. 8: Diamond and Dybvig (1983), *JPE*; Lyons and Viswanath-Natraj (2023), *J. International Money and Finance*;
  Liu, Makarov and Schoar (2023), NBER WP.
* ch. 9: Makarov and Schoar (2020), *JFE*; Liu and Tsyvinski (2021), *RFS*; Liu, Tsyvinski and Wu (2022), *JF*.
* Research: Milionis, Moallemi, Roughgarden and Zhang (2022); Milionis, Moallemi and Roughgarden (2023); Capponi and
  Jia (2021).

## For the researcher

* **Theorem 1 (LVR).**
  * A CFMM arbitraged continuously holds x*(P) = argmin{Px + y : φ(x, y) = k}, with value V(P) = Px* + y*.
  * Let dP = σP dW, and let the rebalancing portfolio satisfy dR = x*(P) dP.
  * Then R_t − V_t = ∫₀ᵗ ℓ(P_s) ds, where ℓ(P) = ½σ²P²|x*′(P)| ≥ 0.
  * For constant product, ℓ = σ²V/8. For a concentrated position, ℓ = ¼σ²L√P inside the range and 0 outside.
* **The proof.**
  * Lemma 1: V is a minimum of functions linear in P, hence concave, and V′ = x* by the envelope theorem.
  * Lemma 2: V″ = x*′ ≤ 0.
  * Itô gives dV = x* dP − ½|x*′|σ²P² dt; subtract dR.
* **The exact discrete version (this part).**
  * For constant product with one arbitrage per step, ΔLVR = (V₀/2)(√(P₁/P₀) − 1)², exactly.
  * For a lognormal step with mean one, E[ΔLVR] = V₀(1 − e^{−σ²Δt/8}) → σ²V₀Δt/8.
* **Theorem 2 (fees and blocks).**
  * With a fee γ and Poisson blocks of rate λ, the mispricing z = log(p/P) has a stationary density that is flat on
    |z| ≤ γ and decays like e^{−a(|z| − γ)} outside, with a = √(2λ)/σ (Lemma 3).
  * So P_trade = 1/(1 + γ√(2λ)/σ), and to leading order ARB = P_trade × LVR (Milionis, Moallemi and Roughgarden 2023).
* **Measured.**
  * **Simulation.** Over 400,000 steps the exact identity equals the simulated loss to rounding; the continuous
    formula is within 0.03%. The concentrated range is within 0.6%.
  * **ETH 2023.** 2.659% against 2.659%, month by month (0.10% to 0.42%).
  * **Poisson blocks** (80% volatility, 12-s blocks). P_trade is 0.776, 0.411, 0.260, 0.106 and 0.035 against
    0.777, 0.411, 0.259, 0.104 and 0.034 for fees of 0.01%–1%; ARB/LVR tracks it.
  * **Fixed blocks.** Trades are slightly more frequent and ARB/LVR is lower (0.087 against 0.104 at 0.3%).
  * **Real ETH minutes.** Fewer trades (0.069 against 0.130 at 0.3%), but ARB/LVR is 0.30, 2.3 times the formula:
    jumps carry the mispricing far outside the band.
* **Simplifications.**
  * Arbitrage only, with no uninformed flow in the checks.
  * Fees outside the curve.
  * One pool, with Binance's price taken as the true price.
  * The ETH checks use one-minute blocks.
* **Open problems.**
  * The trade probability and arbitrage share for jump processes, and the fee that should follow.
  * The best mechanism for recovering LVR: auctions of the arbitrage right, or dynamic fees.
  * LVR across many pools and venues with routing.

## Build it

```bash
python -m videos.quant.quant39.compute                            # every item; a few minutes; ~0.2 GB of Binance files
python -m pytest -q tests/test_quant_house.py -k defi
EXPLAINER_TTS=silent python tools/qa_scene.py quant39 Research     # one chapter, silent, with a contact sheet
python tools/build.py quant39                                      # the narrated part
```

## Desk questions, with solutions

1. **An LP in an x·y = k pool; the price doubles. Loss against holding?**
   * 2√2/3 − 1 = −5.7%.
   * But the measure that matters is LVR, σ²/8 of value per unit of time, which accrues along the path.
2. **What does a pool lose to arbitrage?** ℓ = ½σ²P²|x*′(P)|; for constant product, σ²V/8. ETH's 2023: 2.66%.
3. **Why concentrate, and when not to?**
   * Concentration multiplies fees and LVR by the efficiency (41× at ±5%).
   * It is a bet that fees beat variance, so withdraw when volatility is high.
4. **What keeps a perpetual near spot?**
   * Funding paid by longs when it trades above: F = κS/(κ − (r − q)).
   * On Binance, 0.01% per eight hours whenever the premium is small.
5. **Is cash-and-carry free money?**
   * No: it is a premium for supplying leverage, with a hold-out Sharpe ratio of 2.2.
   * Its tail is the venue and the stablecoin.
6. **When does a stablecoin break?** When reserves are illiquid at the moment of redemption (USDC at 88 cents on a
   weekend), or are its own token (UST and LUNA).

## Problems, with solutions

1. **Impermanent loss.** At r = 4, 2·2/5 − 1 = −20%. The same holds at r = ¼.
2. **A trade on the curve.**
   * k = 1,000 × 2,000,000 = 2 × 10⁹, and after the trade y′ = k/950 = 2,105,263.
   * So 50 ETH cost $105,263, an average of $2,105.26, 5.3% above $2,000.
3. **LVR in dollars.** 0.64/8 × $10m = $800,000 a year, about $2,192 a day.
4. **One block, a doubling.**
   * Exactly, (V₀/2)(√2 − 1)² = 0.0858 V₀.
   * The continuous estimate with (ln 2)² as the variance is 0.0601 V₀; the exact loss is larger for a large step.
5. **Efficiency.**
   * w = 1.21 gives 1/(1 − 1/1.1) = 11×.
   * Near the centre, LVR per dollar is 11 times the full-range rate.
6. **Trade probability.**
   * λ = 7,200 blocks a day and σ = 0.05 a day give η = 0.003 × √14,400/0.05 = 7.2.
   * So P_trade = 1/8.2 = 0.12.
7. **Carry book.** 0.01% × 3 × 365 = 10.95% on notional. With 1.33 of capital per unit, that is 8.2% on capital.
8. **Perpetual premium.**
   * κ = 3 a day = 1,095 a year, so F/S = 1,095/(1,095 − 0.05) = 1.0000457.
   * The premium is about 0.46 bp: perpetuals sit almost on spot.
9. **Venue risk.**
   * p × 25% = 10% gives p = 40% a year.
   * If all capital sits at the venue, p = 10% cancels it.
10. **A run.**
    * A full run leaves 0.7 + 0.3 × 0.7 = $0.91 per dollar.
    * Under first come, first served, the first 91% receive $1 and the last 9% nothing, so running first is the best
      reply.
11. **(qual) The LVR theorem.**
    * **Concavity and the envelope.** V(P) = min_{φ = k}(Px + y) is a minimum of affine functions of P, so it is
      concave. Where the minimiser is unique, V′(P) = x*(P) (envelope theorem), so V″ = x*′ ≤ 0.
    * **Itô.** dV = x* dP + ½x*′σ²P² dt.
    * **Subtract.** With dR = x* dP, d(R − V) = ½σ²P²|x*′| dt.
    * **Constant product.** x* = √(k/P) and |x*′| = ½√k P^{−3/2}, so ℓ = ¼σ²√(kP) = σ²V/8.
    * **Concentrated.** Inside the range x* = L(P^{−1/2} − p_b^{−1/2}), so |x*′| = ½LP^{−3/2} and ℓ = ¼σ²L√P.
      Outside the range x* is constant, so ℓ = 0.
    * **Discrete.** With x₀ = √(k/P₀), x₀(P₁ − P₀) − 2√k(√P₁ − √P₀) = √k(√P₁ − √P₀)²/√P₀ = (V₀/2)(√R − 1)².
      For R lognormal with E R = 1, E√R = e^{−σ²Δt/8}, so the expectation is V₀(1 − e^{−σ²Δt/8}).
12. **(qual) Fees and Poisson blocks.**
    * **Dynamics.** Between blocks z is a Brownian motion with variance σ² per unit time. At rate λ a block resets any
      |z| > γ to ±γ.
    * **Stationary density f.** Inside the band, σ²f″/2 = 0, so f = c by symmetry.
    * **Outside the band.** σ²f″/2 = λf, so f = c e^{−a(|z| − γ)} with a = √(2λ)/σ, continuous at ±γ. The removed mass
      returns at the edges, which carry no density of their own.
    * **Normalise.** 2γc + 2c/a = 1.
    * **The trade probability.** By PASTA, P_trade = mass outside = (2c/a) = 1/(1 + aγ) = 1/(1 + γ√(2λ)/σ).
    * **Limits.**
      * γ → 0: P_trade → 1. Every block trades and arbitrageurs keep all of LVR.
      * λ → ∞: P_trade → 0 like σ/(γ√(2λ)). Arbitrageurs' profit vanishes and fees recover LVR in full.

## Data and reproducibility

* **Binance.**
  * Public monthly files:
    * hourly spot and USD-M perpetual klines for BTCUSDT and ETHUSDT (perpetual files from January 2020);
    * eight-hourly funding (from January 2020);
    * one-minute ETHUSDT for 2023;
    * USDCUSDT one-minute for March 2023;
    * hourly USTUSDT and LUNAUSDT (May 2022, before the 13 May suspension) and FTTUSDT (November 2022).
  * All are checked against Binance's published SHA-256 files.
* **Yahoo Finance.** Daily bars for GBTC (2022–2024) and IBIT (2024).
* **Simulation.** Lognormal and Poisson-block paths with seeds fixed in `compute.py`, and the two-regime world of the
  learned LP.
* **Registration.** `carry_basis_part39`, with nine trials, opened on 2021–2025 (counter 23,559; `track_record.json`).
* **Quoted, not computed.**
  * Reserves and disclosures (Circle, Terra), MEV shares and token-market-maker cases.
  * Makarov–Schoar's premiums, Ethena's size, and the court and regulatory record.
  * All as reported.

---

# 量化金融，从零搭建 — 第39部分：加密货币与去中心化金融

四十三部分量化金融系列的第39部分，第六幕“市场微观结构”的最后一部分，按本系列的博士层次构建。它在加密市场里重新找到第35至38部分的交易商、订单簿、执行者和做市商：
* 按公式做市的池子；
* 靠资金费率拴在现货上的永续合约；
* 没有保险的银行式稳定币；
* 任何回测都装不下的交易场所倒闭。

测量使用币安的公开数据档案：
* 比特币和以太币的现货与永续合约小时K线、资金费率，2020–2025；
* 以太币2023年的分钟K线；
* USDC、UST、LUNA和FTT的危机期数据。

另外使用雅虎财经的GBTC与IBIT日线。

本部分涵盖：
* **区块链与交易所**：FTX，FTT在币安上从26美元跌到1.23美元。
* **自动做市商**：恒定乘积、滑点、预言机；价格翻倍时无常损失为−5.7%。
* **流动性提供者亏掉了什么**：以太币2023年，相对再平衡损失实测2.659%，sigma平方的八分之一给出2.659%。
* **集中流动性**：
  * 正负5%区间的资本效率为41倍；
  * 学习型提供者每天+17个基点，而所有固定区间都亏钱。
* **MEV与三明治攻击**：十万美元、1%容忍度时攻击者赚700美元。
* **永续合约与资金费率**：
  * 比特币平均每年12.8%；
  * 37%的结算恰好为0.01%；
  * 无套利价格F = κS/(κ − (r − q))。
* **期现套利，登记在案**：
  * 研究期夏普4.6，留出期2.16（每年10.2%）；
  * 交易场所保证金占资本25%，约等于2.5年的收益。
* **稳定币与挤兑**：
  * 2023年3月USDC低至0.882；
  * Terra的铸造与销毁螺旋。
* **交易场所、基金与横截面**：GBTC折价收窄74%；IBIT首日成交约10亿美元。
* **第39条规则**：清点收益里看不到的风险。
* **写给研究者**：
  * LVR定理与精确离散恒等式；
  * 手续费与区块下的交易概率；
  * 在真实价格上，套利者拿走的份额是布朗理论的2.3倍。

本部分登记一个策略，试验计数为23,559。

*这是方法教育，不是投资建议。*

## 章节（约57分钟）

* **开场**：交易台问题、三个发现、为什么重要、十七年的历史、计划。
* **1. 区块链与交易所**：账本、共识、两类场所、永不收盘、清算、FTX、教训、现金腿。
* **2. 自动做市商**：不变量、曲线上的交易、滑点、一般形式、套利、预言机、无常损失。
* **3. 流动性提供者亏掉了什么**：三个基准、以太币2023年的路径、分解、公式、按频率、盈亏平衡、负伽马。
* **4. 集中流动性**：区间、持仓、资本效率、离开区间、LVR的放大、学习型提供者。
* **5. 顺序就是钱**：流程、三明治攻击、限度、奖金表、MEV的种类、LVR即MEV、防御。
* **6. 永续合约**：机制、币安规则、无套利价格、利息项、六年数据、逐年、规则与数据、谁付钱。
* **7. 期现套利，登记在案**：组合、风险、九个变体、登记、信封、逐年、曲线、衰减、隐藏的尾部、溢价。
* **8. 稳定币与挤兑**：类型、Diamond–Dybvig、数字、USDC逐分钟、读懂价格、锚定套利、Terra、教训、规则。
* **9. 交易场所、基金与横截面**：Makarov–Schoar、价格发现、信托、GBTC折价、ETF、横截面、公司。
* **10. 第39条规则**：汇总表、交易场所、合约、密钥、四个实验、模块、三个案例。
* **写给研究者**：
  * 模型、两个引理、定理与证明、推论、离散版本；
  * 三项检验；
  * 手续费与区块、平稳分布、第二个定理；
  * 泊松、固定和真实区块的检验；
  * 意义、相关工作、开放问题。
* **结尾**：回顾、教训、公式卡、联系、交易台问题、习题（两道资格考试题，解答见下文）。

## 写给研究者

* **定理一（LVR）**：
  * 连续套利的恒定函数做市商持有x*(P)；
  * 再平衡组合与池子之差为∫½σ²P²|x*′(P)|dt ≥ 0；
  * 恒定乘积池为σ²V/8，集中头寸在区间内为¼σ²L√P。
* **证明**：
  * 包络定理给出V′ = x*；
  * 凹性给出V″ ≤ 0；
  * 再用伊藤公式。
* **精确离散版本（本部分）**：ΔLVR = (V₀/2)(√(P₁/P₀) − 1)²，期望为V₀(1 − e^{−σ²Δt/8})。
* **定理二（手续费与区块）**：
  * 错价的平稳密度在区间内平坦、区间外指数衰减；
  * P_trade = 1/(1 + γ√(2λ)/σ)，ARB ≈ P_trade × LVR。
* **检验**：
  * 模拟中恒等式与模拟损失在舍入误差内相等；
  * 以太币2023年逐月相等；
  * 泊松区块与公式吻合，固定区块下套利者留下更少；
  * 真实分钟数据上，0.3%费率时套利者拿走LVR的0.30，为公式的2.3倍。
* **开放问题**：
  * 跳跃过程下的交易概率与手续费；
  * 挽回LVR的最佳机制；
  * 多池多场所。

## 交易台问题与解答

1. 价格翻倍：无常损失−5.7%；但正确的度量是LVR，即每单位时间价值的σ²/8。
2. 池子输给套利的是σ²V/8；以太币2023年为2.66%。
3. 集中把手续费和LVR同时放大（正负5%时为41倍）；波动率高时撤出。
4. 资金费率；F = κS/(κ − (r − q))；溢价很小时为每八小时0.01%。
5. 不是白送的钱：留出期夏普2.2，但尾部在交易场所和稳定币。
6. 储备在赎回时缺乏流动性（USDC周末跌到88美分），或储备就是自己的代币（UST与LUNA）。

## 习题与解答

1. r = 4或¼：−20%。
2. 成本105,263美元，均价2,105.26美元，高出5.3%。
3. 每年80万美元，每天约2,192美元。
4. 精确值0.0858V₀，连续估计0.0601V₀。
5. 11倍；每美元LVR为全区间的11倍。
6. η = 7.2，P_trade = 0.12。
7. 名义收益10.95%，资本收益8.2%。
8. 溢价约0.46个基点。
9. p = 40%；若全部资本都在交易场所，p = 10%。
10. 每美元剩0.91；前91%拿到1美元，最后9%一无所有，所以先跑是最优反应。
11. **（资格考试）LVR定理**：
    * 包络定理与凹性，再用伊藤公式，减去再平衡组合；
    * 恒定乘积与集中头寸的速率；
    * 离散恒等式与其期望。
12. **（资格考试）手续费与泊松区块**：
    * 区间内密度平坦，区间外以√(2λ)/σ的速率指数衰减；
    * 归一化后由PASTA得P_trade = 1/(1 + γ√(2λ)/σ)；
    * γ → 0时为1，λ → ∞时趋于0，手续费挽回全部LVR。

## 数据与复现

* **币安公开数据**：均与币安公布的SHA-256核对。
* **雅虎财经**：GBTC与IBIT的日线。
* **登记**：carry_basis_part39，九次试验，留出期2021–2025已打开，计数器23,559。
* **引用而非计算**：储备披露、MEV份额、法院与监管记录，均按报道表述。
