# Quant, Built — Part 22: FX, Commodities and the Basis

Part 22 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the last part of Act III, Derivatives (Q), and the last of its five parts on rates,
credit and the basis (18–22). It prices moving money across borders and moving oil and gas across time, and finds,
in currencies, commodities and Treasuries alike, prices held apart by the cost of something scarce. It covers:

* covered interest parity derived, measured on thirty years of sterling, and its breakdown after 2008 (Du, Tepper and
  Verdelhan); the price of balance sheet;
* uncovered parity and Fama's forward premium puzzle on nine currencies; the carry trade, its crash risk
  (Brunnermeier, Nagel and Pedersen) and its factor (Lustig, Roussanov and Verdelhan); the yen in August 2024;
* FX options: Garman–Kohlhagen, the four delta conventions, the delta-neutral straddle, the smile from ATM, risk
  reversal and butterfly, vanna–volga;
* pegs and attacks: Krugman's first-generation model, Obstfeld's second, Black Wednesday and the Swiss franc floor;
* commodities: the cost of carry and the convenience yield on forty years of the WTI curve, Working's curve, the roll
  and the commodity premium (Gorton and Rouwenhorst); gas seasonality, Amaranth, Europe's gas crisis, a power plant as
  spread options; negative oil and Bachelier;
* the Treasury basis trade: futures delivery and its options, implied repo, leverage, the CFTC's positions, March 2020
  and the Fed's estimates; inflation breakevens, their premia, and inflation swaps.

Every number is computed by the series' own code ([`compute.py`](compute.py), and the House's new
[`macro`](../../../explainer/quant/house/macro.py) module). Data: FRED (the Fed's noon exchange rates, OECD 3-month
rates, the TED spread and bills, TIPS breakevens, CPI, the IMF's gas prices, Henry Hub, the Nikkei), the Bank of
England (sterling spot and forwards, the Deutsche mark), the EIA (NYMEX WTI and Henry Hub futures, contracts 1–4) and
the CFTC (Traders in Financial Futures).

*An education in methods, not investment advice. Firms and episodes are described from the public record, as
reported by the sources named.*

## Chapters (about 54 minutes)

* **A floor that broke** (2.9 min). EUR/CHF 2010–2016 and the 1.20 floor (6 September 2011); 15 January 2015: 1.2009 →
  1.0357 at New York noon, −13.8%, about 80 daily standard deviations of 2012–14; FXCM's $275 million of client debit
  balances and Leucadia's $300 million loan; Alpari UK; the history strip (1983–2024); the plan; the macro desk opens.
* **1. Covered interest parity** (4.1). The two routes from a dollar today to a dollar in three months; the forward
  derived; the basis (Du–Tepper–Verdelhan); June 2016 worked (x = −18 bp); sterling 1986–2016 with LIBOR on both
  sides (+7 ± 8 bp to mid-2007, −147 bp in November 2008, −12 ± 11 bp in 2010–16); why: balance sheet's capital cost,
  quarter-ends; who pays and who could arbitrage; the Fed's swap lines.
* **2. Uncovered parity and the forward premium puzzle** (2.8). UIP; Fama's regression and its decomposition; nine
  currencies, 1999–2025 (six slopes negative; pooled −0.15, three standard errors below one); the Australian dollar's
  scatter; risk premium, peso problem, slow money (Chinn–Meredith).
* **3. The carry trade and its crashes** (3.6). The sort (June 2007); 1999–2025: 2.9% a year, 7.0% volatility, Sharpe
  0.41, skew −0.80; October 2008 −11.2%, March 2020 −5.7%; the distribution (worst month −5.7σ); skewness against the
  interest differential (correlation −0.67); the yen in 2024 (161.7 on 10 July → 144.0 on 5 August; the Nikkei −12.4%,
  then +10.2%); the HML_FX factor.
* **4. FX options: two rates and four deltas** (3.5). Garman–Kohlhagen derived; put–call parity as CIP; the call–put
  symmetry; an illustrative EUR/USD (ATM call 160 pips); the four deltas of the 25-delta call (0.2488, 0.2500, 0.2433,
  0.2445); the premium-adjusted delta's peak (0.88 for an illustrative USD/JPY); the ATM delta-neutral straddle.
* **5. The FX smile** (3.5). RR and BF to pillar vols; strikes from deltas (1.0776, 1.1071, 1.1353); vanna–volga
  derived (Castagna–Mercurio) and drawn; a term structure of smiles; why not Heston or SABR; barriers.
* **6. Pegs and attacks** (3.3). Krugman–Flood–Garber derived and run (the attack at T* = 8 against reserves lasting
  to 10); sterling in the ERM, 1990–93 (2.7812 on 15 September 1992, 2.6323 on the 17th, 13% lower within six weeks;
  10% → 12% → 15%); Obstfeld's self-fulfilling attacks; the franc's floor, defended by printing.
* **7. Storage, carry and the convenience yield** (3.3). Cash and carry; the convenience yield (Kaldor, Working);
  backwardation and contango on six days (July 2008, June 2014, March 2022; December 2008, February 2016, 17 April
  2020); the slope since 1986 (contango on 55% of days); Working's curve; Gorton–Hayashi–Rouwenhorst.
* **8. The roll and the commodity premium** (3.1). The roll yield derived; WTI's last-trading-day rule; a rolled
  front-month index 1986–2024 (1.7% a year against the price's 3.2%); 2010–2023 year by year (2020: −41% against −21%);
  Keynes, Gorton–Rouwenhorst and what came after; Optiver (CFTC, 2008; $13 million plus $1 million, 2012).
* **9. Gas and power** (3.2). Henry Hub's seasons (January 1.08, April 0.92 of the year's mean); Amaranth, September
  2006 (front month $7.57 → $4.20; about two thirds of $9.2 billion); Europe at $70 against America's $8.8 in August
  2022; the spark spread; a plant as a strip of spread options (Margrabe: $7.1 independent, $4.5 at ρ = 0.6).
* **10. April 2020: negative oil** (3.4). May WTI to −$37.63 on 20 April (June $20.43); physical delivery and storage;
  the curve on three days (a $58 one-month spread); Black against Bachelier; a put struck at zero; CME's switch
  (advisories 20-152 and 20-171).
* **11. The Treasury basis trade** (4.4). Futures, conversion factors and the cheapest to deliver; the short's delivery
  options; implied repo worked; leverage and margin; leveraged funds' net short in 2-, 5-, 10-year and bond futures
  (−$366 billion in February 2020, −$1.05 trillion at the end of 2025); March 2020 ($173 billion of hedge-fund sales,
  Fed staff); its size since ($260–574 billion in September 2023; about $830 billion in September 2025).
* **12. Inflation: breakevens and the premium** (3.4). TIPS and the breakeven decomposed; 2003–2025 (−2.24% in November
  2008, 3.59% in March 2022; 5y5y average 2.25%); the 5-year breakeven against the CPI that followed (−0.60 ± 1.20
  points); the 2021–22 surge (CPI 9.0%); expected inflation, risk premium and liquidity (D'Amico–Kim–Wei); inflation
  swaps and the swap–TIPS basis.
* **13. Rule 22: the macro desk** (2.5). The desk's first sheet; **lab**: `cip_basis`, `implied_convenience`,
  `implied_repo`; the `macro` module; Rule 22; the rule against the franc, Amaranth, negative oil and the basis trade.
* **For the researcher: the competitive storage model** (5.6). Availability x = I₋₁ + z, price p = P(x − I), storers
  with P(x − I) + k ≥ βE[p′] (equality when I > 0): the price is the fixed point f(x) = max{P(x), βE f(I* + z′) − k}
  (Gustafson 1958; Williams and Wright 1991; Deaton and Laroque 1992), and with risk-neutral storers the one-period
  spread is full carry k + (β⁻¹ − 1)p whenever stocks are positive and backwardation at stock-outs: Working's curve,
  derived. Solved by time iteration (elasticity −0.5, harvest sd 0.1, interest 1%, storage 0.5% a period; 163
  iterations); simulated 200,000 periods: stock-outs 8.8%, price skewness 3.2, autocorrelation 0.46. Data: WTI's
  second over first contract (EIA, monthly average) against US commercial crude stocks relative to the same month's
  5-year average, 372 months 1990–2020: correlation 0.47, 39% of months in backwardation, the scarcest decile
  (−10.3%) −2.6% a month, the most plentiful (+29%) +1.9%. The persistence puzzle: WTI's monthly log price
  autocorrelation is 0.99 (0.87 at twelve months) against the model's 0.46 (Deaton and Laroque 1992, 1996; Cafiero,
  Bobenrieth, Bobenrieth and Wright 2011). Three open problems; pause: at most 70 × 0.004 + 0.30 = $0.58 of contango;
  no arbitrage limit on backwardation.
* **Recap, desk questions, problems** (3.1). Eleven lines; six desk questions; twelve problems (two at
  qualifying-exam level), solutions below.

## Hands-on

* **Lab** (the House's own code on screen): `cip_basis`, `implied_convenience`, `implied_repo` (ch. 13).
* **Computed:** the sterling CIP basis monthly for thirty years; Fama regressions and carry portfolios for nine
  currencies; FX strikes, deltas and a vanna–volga smile; an attack model; a rolled WTI index from the EIA's contract
  series; implied convenience yields; Margrabe spark options; Bachelier puts near zero; the CFTC's positions; breakevens
  against realised CPI.
* **Live constructions:** the CIP square; the carry sort; the shadow exchange rate meeting the peg; futures curves
  flipping between backwardation and contango; the WTI curve on 17, 20 and 21 April 2020.

## Textbook audit

| Textbook | Chapters | Where |
|---|---|---|
| Clark, *Foreign Exchange Option Pricing* | 1–3 (FX markets, Garman–Kohlhagen, conventions), 4 (smile, vanna–volga), 6 (barriers) | ch. 4–5 |
| Wystup, *FX Options and Structured Products* | 1 (deltas, premium adjustment, ATM conventions), 1.5 (vanna–volga) | ch. 4–5 |
| Geman, *Commodities and Commodity Derivatives* | 2 (storage, convenience yield), 3 (the roll, indices), 9–10 (oil, gas), 13 (power) | ch. 7–10 |
| Eydeland and Wolyniec, *Energy and Power Risk Management* | 5 (spread options), 7–8 (power plants as options) | ch. 9 |
| Hull, *Options, Futures, and Other Derivatives* | 5 (forwards, cost of carry), 6 (Treasury futures, CTD), 17 (currency options) | ch. 1, 4, 7, 11 |

## Papers, chapter by chapter

* Hook: SNB press release (15 January 2015); FXCM, 10-K for 2015.
* ch. 1: Du, Tepper and Verdelhan (2018); Borio, McCauley, McGuire and Sushko (2016); the Fed's swap lines (2007–08,
  2020).
* ch. 2–3: Fama (1984); Chinn and Meredith (2004); Brunnermeier, Nagel and Pedersen (2008); Lustig, Roussanov and
  Verdelhan (2011).
* ch. 4–5: Garman and Kohlhagen (1983); Castagna and Mercurio (2007); Reiswich and Wystup (2010) on delta conventions.
* ch. 6: Krugman (1979); Flood and Garber (1984); Obstfeld (1994); HM Treasury papers on Black Wednesday (2005).
* ch. 7–8: Keynes (1930); Kaldor (1939); Working (1949); Gorton and Rouwenhorst (2006); Gorton, Hayashi and Rouwenhorst
  (2013); CFTC releases 5521-08 and 6239-12 (Optiver).
* ch. 9: Margrabe (1978); US Senate PSI, *Excessive Speculation in the Natural Gas Market* (2007).
* ch. 10: Bachelier (1900); CME Clearing advisories 20-152 and 20-171 (April 2020).
* ch. 11: Barth and Kahn (OFR, 2021); Glicoes, Iorio, Monin and Petrasek (FEDS Notes, March 2024); Monin (FEDS Notes,
  June 2026); FOMC statement (23 March 2020); SEC, Treasury clearing rule (2023).
* ch. 12: D'Amico, Kim and Wei (2018); FRED's TIPS breakeven series.

## Build it

```bash
python -m videos.quant.quant22.compute                       # every item (fetches and caches the data)
EXPLAINER_TTS=silent python tools/qa_scene.py quant22 CIP     # one chapter, silent, with a contact sheet
python tools/make.py quant22 --cpu-voice -q m                # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **Dollar rates 5%, yen 0%: is the yen forward at a premium or a discount?** At a premium. Covered parity puts the
   one-year forward, in yen per dollar, at F = S × 1.00/1.05, so a dollar buys about 5% fewer yen for delivery in a
   year. Nothing is left to arbitrage: the forward is set by the two rates. The carry trade is a different bet: that
   the spot will not fall as far as the forward says (ch. 2–3).
2. **Covered parity is an arbitrage. Why did it fail for years after 2008?** The arbitrage borrows dollars and lends
   them through the swap; both legs use balance sheet, and since 2008 balance sheet needs capital even for riskless
   assets. A basis smaller than the capital charge is not worth taking, and the demand to swap into dollars keeps it
   open (ch. 1).
3. **Why does a rolled oil index earn less than the oil price in contango?** Each roll sells the expiring contract and
   buys a dearer one, so the curve's slope is a cost paid every month; in backwardation the roll pays instead (ch. 8).
4. **Why did only the May 2020 contract go negative?** It was about to deliver: holders without storage had to sell
   before 21 April to the few who had space; the June contract still had a month (ch. 10).
5. **A peg has held for years with tiny volatility. What does an option on its end cost?** Less than it should:
   volatility measured in the calm prices a diffusion, but the payoff is a jump whose probability is a political
   judgement (ch. 6, the hook).
6. **What makes the Treasury basis trade risky if it is an arbitrage?** It is an arbitrage only at delivery. Until
   then it is a position levered fifty times, financed overnight, exposed to daily margin, higher haircuts and a wider
   basis exactly when the market is stressed (ch. 11).

## Problems, with solutions

1. **Covered parity.** With S in domestic per foreign: one unit of domestic currency becomes (1 + r_d τ) at home, or
   1/S foreign units that grow to (1 + r_f τ)/S and are sold forward for F(1 + r_f τ)/S. Both are riskless, so
   F = S(1 + r_d τ)/(1 + r_f τ). With continuous rates, F = S e^{(r_d − r_f)τ} and ln(F/S) = (r_d − r_f)τ.
2. **A basis by hand.** y_$ = ln(1.005)/0.25 = 1.995%, y_£ = ln(1.003)/0.25 = 1.198%, ln(F/S)/τ = ln(1.3025/1.30)/0.25
   = 0.769%. So x = 1.995 − 1.198 − 0.769 = +0.028%, about +3 bp: within the cost of trading.
3. **Fama's slope.** Write f − s = E_t[Δs] + p. The regression slope is cov(Δs, f − s)/var(f − s); with Δs = E_t[Δs]
   + ε and ε uncorrelated with time-t information, cov(Δs, f − s) = cov(f − s − p, f − s) = var(f − s) − cov(p, f − s),
   so β = 1 − cov(p, f − s)/var(f − s). β < 0 needs cov(p, f − s) > var(f − s): the premium must move against the
   expected change, and be more variable than it (Fama's two conditions).
4. **FX deltas.** C = e^{−r_d T}[F N(d₁) − K N(d₂)] with F = S e^{(r_d − r_f)T}; dC/dS = e^{−r_f T} N(d₁) (the spot delta),
   and the forward delta, the hedge in forward contracts, is N(d₁). If the premium is paid in foreign units, subtract
   it: Δ_pa = e^{−r_f T}N(d₁) − C/S = (K/S) e^{−r_d T} N(d₂) = e^{−r_f T}(K/F)N(d₂), and in forward terms (K/F)N(d₂).
5. **The straddle strike.** Forward deltas: call N(d₁), put −N(−d₁); their sum is 2N(d₁) − 1 = 0 when d₁ = 0, that is
   ln(F/K) + σ²T/2 = 0, so K = F e^{σ²T/2}.
6. **Pillar vols.** σ_25c = 8 + 0.3 − 0.5 = 7.8%, σ_25p = 8 + 0.3 + 0.5 = 8.8%: euro puts dearer, as the negative
   risk reversal says.
7. **An attack date.** T* = (s̄ − αμ − d₀)/μ = (1 − 0.1 − 0.4)/0.1 = 5; on that day speculators take the remaining
   reserves, αμ = 0.1. Without the attack the reserves would have lasted until (1 − 0.4)/0.1 = 6.
8. **A convenience yield.** y − u = r − ln(F₂/F₁)/Δt = 0.05 − 12 ln(71.5/70) = 0.05 − 0.254 = −20.4% a year: holders
   are paid to store oil; inventories are ample (contango).
9. **Implied repo.** Invoice = 112.0 × 0.89 + 1.1 = 100.78; (100.78/100.2 − 1) × 360/92 = 2.27%. If the note can be
   financed below that, buying it and selling the future earns the difference.
10. **Spread options and correlation.** The exchange option's volatility is √(σ₁² + σ₂² − 2ρσ₁σ₂), which falls as ρ
    rises; an at-the-money option's value is about 0.4 × S × σ√T, so it falls too. Perfectly correlated legs leave
    nothing to exchange.
11. **(qual) Full carry and the threshold.** If I_t > 0 the storer's first-order condition holds with equality:
   P(x − I) + k = βE[p′], and p_t = P(x − I), so βF_t = p_t + k with F_t = E_t[p′] under risk neutrality, i.e.
   F_t − p_t = (β⁻¹ − 1)p_t + β⁻¹k (≈ k + rp). Storage is zero exactly when even the first unit is unprofitable:
   P(x) + k ≥ βE f(z′) (storing nothing, next availability is the harvest alone), so x* solves P(x*) = βE f(z′) − k;
   below x*, f = P, decreasing; above, f is decreasing because both P and the stored amount respond monotonically.
12. **(qual) Monotonicity and skew.** If f is decreasing, E f(I + z′) is decreasing in I, so the root I_f(x) of
   P(x − I) + k = βE f(I + z′) is increasing in x with slope below 1; hence x − I_f(x) increases and Tf(x) = P(x − I_f(x))
   decreases. Skew: when availability is high, storage absorbs the surplus and the price falls only a little; when it
   is low, stocks cannot go below zero, the whole shortfall hits consumption, and P is steep there: high prices are
   reached in a few states with large moves, low prices are compressed, so the distribution is right-skewed.

## For the researcher

* **The theorems.** Gustafson (1958); Williams and Wright, *Storage and Commodity Markets* (1991); Deaton and Laroque
  (1992), "On the behaviour of commodity prices," *Rev. Econ. Studies* 59, and (1996), "Competitive storage and
  commodity price dynamics," *J. Political Economy* 104; Cafiero, Bobenrieth, Bobenrieth and Wright (2011), *J.
  Econometrics* 162; Working (1949); Kaldor (1939).
* **Simplifications.** IID harvests, a constant storage cost, risk-neutral storers, no upper bound on storage; one
  period is not calibrated to a month; the data's inventory deviation uses a 5-year same-month average.
* **Open problems.** Persistence; risk premia in the curve; storage capacity limits.

## Data and reproducibility

* FRED: DEXUSEU, DEXJPUS, DEXUSUK, DEXSZUS, DEXUSAL, DEXCAUS, DEXUSNZ, DEXNOUS, DEXSDUS (noon rates); IR3TIB01xxM156N
  (OECD 3-month rates); TEDRATE and DTB3 (dollar LIBOR, to January 2022); LIOR3MUKM (sterling LIBOR, to 2017); T5YIE,
  T10YIE, T5YIFR, CPIAUCSL; MHHNGSP, PNGASEUUSDM; NIKKEI225. Frozen through 2025 and checksummed.
* Bank of England: XUDLUSS, XUDLDS3 (spot and 3-month forward, to June 2021), XUDLDMS (Deutsche marks per pound).
* EIA: RCLC1–4 and RNGC1–4, daily NYMEX settlements (published to April 2024).
* CFTC: Traders in Financial Futures for contracts 042601, 044601, 043602, 020601.
* Published figures quoted, not computed: the SNB's decision; FXCM's filings; the ERM's band and the Treasury's cost;
  Amaranth's losses (Senate PSI, as summarised by EDHEC); the CME advisories; the Fed's basis-trade estimates; Optiver's
  settlement.
* Illustrative inputs, labelled on screen: the FX option markets (EUR/USD, USD/JPY), the attack model's parameters,
  Working's curve, the spark-spread option, the Treasury trade's prices, the Bachelier put's volatility.
* No hold-out is opened in this part; the trial counter stays at 315.

---

# 量化金融，从零搭建 — 第22部分：外汇、商品与基差

本部分为跨国界转移资金、以及跨时间转移石油和天然气定价，并且在货币、商品和国债中都发现：价格之所以分开，是因为某种稀缺东西的成本。本部分讲：

* 推导抛补利率平价，用三十年的英镑数据度量，以及它在2008年之后的失效（Du、Tepper和Verdelhan）；资产负债表的价格；
* 非抛补平价与Fama的远期溢价之谜（九种货币）；套息交易、其崩盘风险（Brunnermeier、Nagel和Pedersen）及其因子（Lustig、Roussanov和Verdelhan）；2024年8月的日元；
* 外汇期权：Garman–Kohlhagen、四种delta惯例、delta中性跨式、由ATM、风险逆转和蝶式构造微笑、vanna–volga；
* 汇率挂钩与冲击：Krugman的第一代模型、Obstfeld的第二代模型、黑色星期三与瑞士法郎下限；
* 商品：四十年WTI曲线上的持有成本与便利收益、Working曲线、展期与商品溢价（Gorton和Rouwenhorst）；天然气的季节性、Amaranth、欧洲天然气危机、作为价差期权的发电厂；负油价与Bachelier；
* 国债基差交易：期货交割及其期权、隐含回购利率、杠杆、CFTC持仓、2020年3月与美联储的估计；通胀盈亏平衡率、其溢价与通胀互换。

*讲的是方法，不构成投资建议。涉及的公司与事件均依据公开记录，并注明报道来源。*

## 章节（约54分钟）

* **一个崩塌的下限。** 2010–2016年的欧元/瑞郎与1.20的下限（2011年9月6日）；2015年1月15日：纽约中午1.2009 → 1.0357，−13.8%，约为2012–14年日标准差的80倍；FXCM客户2.75亿美元的负余额与Leucadia的3亿美元贷款；Alpari英国；历史条（1983–2024）；本部分安排；宏观交易台开张。
* **1. 抛补利率平价。** 从今天的一美元到三个月后一美元的两条路径；推导远期汇率；基差（Du–Tepper–Verdelhan）；2016年6月的算例（x = −18个基点）；两边都用LIBOR的1986–2016年英镑（2007年年中以前+7 ± 8个基点，2008年11月−147个基点，2010–16年−12 ± 11个基点）；原因：资产负债表的资本成本、季末；谁付钱、谁能套利；美联储的货币互换额度。
* **2. 非抛补平价与远期溢价之谜。** UIP；Fama回归及其分解；九种货币，1999–2025（六个斜率为负；合并为−0.15，比一低三个标准误）；澳元的散点图；风险溢价、比索问题、缓慢的资金（Chinn–Meredith）。
* **3. 套息交易及其崩盘。** 排序（2007年6月）；1999–2025：每年2.9%，波动率7.0%，夏普比率0.41，偏度−0.80；2008年10月−11.2%，2020年3月−5.7%；分布（最差月份−5.7σ）；偏度对利差（相关系数−0.67）；2024年的日元（7月10日161.7 → 8月5日144.0；日经指数−12.4%，随后+10.2%）；HML_FX因子。
* **4. 外汇期权：两个利率与四个delta。** 推导Garman–Kohlhagen；看跌–看涨平价即CIP；看涨–看跌对称性；示意的欧元/美元（平价看涨期权160点）；25-delta看涨期权的四个delta（0.2488、0.2500、0.2433、0.2445）；溢价调整delta的峰值（示意的美元/日元为0.88）；平价delta中性跨式。
* **5. 外汇微笑。** 由RR和BF得到支柱波动率；由delta求行权价（1.0776、1.1071、1.1353）；推导并画出vanna–volga（Castagna–Mercurio）；微笑的期限结构；为什么不用Heston或SABR；障碍期权。
* **6. 汇率挂钩与冲击。** 推导并运行Krugman–Flood–Garber模型（冲击发生在T* = 8，而储备本可维持到10）；1990–93年欧洲汇率机制中的英镑（1992年9月15日2.7812，17日2.6323，六周内下跌13%；10% → 12% → 15%）；Obstfeld的自我实现冲击；靠印钞捍卫的瑞郎下限。
* **7. 储存、持有成本与便利收益。** 现货持有套利；便利收益（Kaldor、Working）；六个交易日的现货升水与期货升水（2008年7月、2014年6月、2022年3月；2008年12月、2016年2月、2020年4月17日）；1986年以来的斜率（55%的交易日为期货升水）；Working曲线；Gorton–Hayashi–Rouwenhorst。
* **8. 展期与商品溢价。** 推导展期收益；WTI的最后交易日规则；1986–2024年的展期近月指数（每年1.7%，对价格的3.2%）；2010–2023年逐年（2020年：−41%对−21%）；Keynes、Gorton–Rouwenhorst以及此后的情况；Optiver（CFTC，2008；2012年1,300万加100万美元）。
* **9. 天然气与电力。** Henry Hub的季节（1月为全年均值的1.08，4月0.92）；Amaranth，2006年9月（近月合约7.57美元 → 4.20美元；92亿美元中约三分之二）；2022年8月欧洲70美元对美国8.8美元；点火价差；作为一串价差期权的发电厂（Margrabe：独立时7.1美元，ρ = 0.6时4.5美元）。
* **10. 2020年4月：负油价。** 4月20日5月WTI跌至−37.63美元（6月合约20.43美元）；实物交割与储存；三天的曲线（一个月价差58美元）；Black对Bachelier；行权价为零的看跌期权；CME的切换（通告20-152和20-171）。
* **11. 国债基差交易。** 期货、转换因子与最便宜可交割券；空头的交割期权；隐含回购利率算例；杠杆与保证金；杠杆基金在2年、5年、10年和长期国债期货上的净空头（2020年2月−3,660亿美元，2025年底−1.05万亿美元）；2020年3月（对冲基金卖出1,730亿美元，美联储工作人员）；此后的规模（2023年9月2,600–5,740亿美元；2025年9月约8,300亿美元）。
* **12. 通胀：盈亏平衡率与溢价。** TIPS与盈亏平衡率的分解；2003–2025（2008年11月−2.24%，2022年3月3.59%；5y5y平均2.25%）；5年期盈亏平衡率对随后的CPI（−0.60 ± 1.20个点）；2021–22年的通胀飙升（CPI 9.0%）；预期通胀、风险溢价与流动性（D'Amico–Kim–Wei）；通胀互换与互换–TIPS基差。
* **13. 第22条规则：宏观交易台。** 交易台的第一张表；**实验**：`cip_basis`、`implied_convenience`、`implied_repo`；`macro`模块；第22条规则；用瑞郎、Amaranth、负油价和基差交易检验这条规则。
* **写给研究者：竞争性储存模型。** 可用量x = I₋₁ + z，价格p = P(x − I)，储存者满足P(x − I) + k ≥ βE[p′]（I > 0时取等号）：价格是不动点f(x) = max{P(x), βE f(I* + z′) − k}（Gustafson 1958；Williams与Wright 1991；迪顿与拉罗克1992），风险中性的储存者下，单期价差在库存为正时为完全持有成本k + (β⁻¹ − 1)p，断货时为现货升水：推导出的沃金曲线。时间迭代求解（弹性−0.5、收成标准差0.1、利率1%、储存每期0.5%；163次迭代）；模拟200,000期：断货8.8%、价格偏度3.2、自相关0.46。数据：WTI第二与第一合约之差（EIA，月均）对美国商业原油库存相对同月五年平均的偏离，1990–2020年372个月：相关0.47，39%的月份为现货升水，最稀缺十分位（−10.3%）每月−2.6%，最充裕（+29%）+1.9%。持续性之谜：WTI月度对数价格自相关0.99（十二个月0.87），模型为0.46（迪顿与拉罗克1992、1996；Cafiero、Bobenrieth、Bobenrieth与Wright 2011）。三个开放问题；暂停题：期货升水至多70 × 0.004 + 0.30 = 0.58美元；现货升水没有套利限制。
* **回顾、交易台问题与习题。** 十一行回顾；六个交易台问题；十二道习题（两道为资格考试水平），解答见下文。

## 交易台问题与解答

1. **美元利率5%，日元0%：日元远期是升水还是贴水？** 升水。抛补平价使一年期远期汇率比即期少约5%的日元，即一美元用于一年后交割时大约少换5%的日元。没有什么可套利的：远期由两个利率决定。套息交易是另一种押注：押即期汇率不会像远期所说的那样下跌那么多（第2–3章）。
2. **抛补平价是套利。为什么它在2008年后多年失效？** 套利要借入美元并通过互换贷出；两条腿都占用资产负债表，而2008年以来即使是无风险资产，资产负债表也需要资本。小于资本成本的基差不值得去做，而换入美元的需求让它一直敞开（第1章）。
3. **为什么在期货升水时，展期的石油指数收益低于油价？** 每次展期都卖出到期的合约、买入更贵的合约，所以曲线的斜率是每个月都要付的成本；在现货升水时，展期反而带来收益（第8章）。
4. **为什么只有2020年5月合约跌成负值？** 它即将交割：没有储存空间的持有者必须在4月21日前把它卖给少数有空间的人；6月合约还有一个月（第10章）。
5. **一个汇率挂钩多年来波动极小。针对它终结的期权值多少？** 比它应有的价值低：在平静中度量的波动率按扩散过程定价，而支付是一次跳跃，其概率是一个政治判断（第6章、开场）。
6. **既然是套利，国债基差交易的风险在哪里？** 它只在交割时才是套利。在那之前，它是一个五十倍杠杆、靠隔夜融资的头寸，恰恰在市场承压时面临每日保证金、更高的折扣率和更宽的基差（第11章）。

## 习题与解答

1. **抛补平价。** 设S为每单位外币的本币价格：一单位本币在本国变成(1 + r_d τ)，或者换成1/S单位外币，增长到(1 + r_f τ)/S并按远期卖出得到F(1 + r_f τ)/S。两者都无风险，所以F = S(1 + r_d τ)/(1 + r_f τ)。用连续复利时F = S e^{(r_d − r_f)τ}，ln(F/S) = (r_d − r_f)τ。
2. **手算基差。** y_$ = ln(1.005)/0.25 = 1.995%，y_£ = ln(1.003)/0.25 = 1.198%，ln(F/S)/τ = ln(1.3025/1.30)/0.25 = 0.769%。所以x = 1.995 − 1.198 − 0.769 = +0.028%，约+3个基点：在交易成本之内。
3. **Fama的斜率。** 记f − s = E_t[Δs] + p。回归斜率为cov(Δs, f − s)/var(f − s)；Δs = E_t[Δs] + ε且ε与t时信息不相关，所以cov(Δs, f − s) = cov(f − s − p, f − s) = var(f − s) − cov(p, f − s)，β = 1 − cov(p, f − s)/var(f − s)。β < 0要求cov(p, f − s) > var(f − s)：溢价必须与预期变化反向变动，且波动更大（Fama的两个条件）。
4. **外汇delta。** C = e^{−r_d T}[F N(d₁) − K N(d₂)]，F = S e^{(r_d − r_f)T}；dC/dS = e^{−r_f T} N(d₁)（即期delta），用远期合约对冲的远期delta为N(d₁)。若权利金以外币支付，要减去它：Δ_pa = e^{−r_f T}N(d₁) − C/S = (K/S) e^{−r_d T} N(d₂) = e^{−r_f T}(K/F)N(d₂)，远期形式为(K/F)N(d₂)。
5. **跨式行权价。** 远期delta：看涨N(d₁)，看跌−N(−d₁)；二者之和为2N(d₁) − 1，当d₁ = 0时为零，即ln(F/K) + σ²T/2 = 0，所以K = F e^{σ²T/2}。
6. **支柱波动率。** σ_25c = 8 + 0.3 − 0.5 = 7.8%，σ_25p = 8 + 0.3 + 0.5 = 8.8%：欧元看跌期权更贵，正如负的风险逆转所说。
7. **冲击日期。** T* = (s̄ − αμ − d₀)/μ = (1 − 0.1 − 0.4)/0.1 = 5；那一天投机者拿走剩余储备αμ = 0.1。没有冲击时，储备本可维持到(1 − 0.4)/0.1 = 6。
8. **便利收益。** y − u = r − ln(F₂/F₁)/Δt = 0.05 − 12 ln(71.5/70) = 0.05 − 0.254 = 每年−20.4%：持有者是被付钱来储存石油的；库存充足（期货升水）。
9. **隐含回购利率。** 发票价格 = 112.0 × 0.89 + 1.1 = 100.78；(100.78/100.2 − 1) × 360/92 = 2.27%。如果这只票据能以低于此的利率融资，买入它并卖出期货就能赚取差额。
10. **价差期权与相关性。** 交换期权的波动率为√(σ₁² + σ₂² − 2ρσ₁σ₂)，随ρ上升而下降；平价期权的价值约为0.4 × S × σ√T，所以也下降。完全相关的两条腿没有什么可交换的。
11. **（资格考试）完全持有成本与阈值。** I_t > 0时储存者的一阶条件取等号：P(x − I) + k = βE[p′]，而p_t = P(x − I)，风险中性下F_t = E_t[p′]，所以F_t − p_t = (β⁻¹ − 1)p_t + β⁻¹k（≈ k + rp）。恰当第一个单位也不赚钱时储存为零：P(x) + k ≥ βE f(z′)，所以x*满足P(x*) = βE f(z′) − k；x*以下f = P递减，以上因P与储存量都单调响应，f仍递减。
12. **（资格考试）单调性与偏度。** 若f递减，则E f(I + z′)对I递减，所以P(x − I) + k = βE f(I + z′)的根I_f(x)对x递增且斜率小于1；于是x − I_f(x)递增，Tf(x) = P(x − I_f(x))递减。偏度：可用量高时，储存吸收过剩，价格只稍降；可用量低时，库存不能低于零，全部短缺落到消费上，而P在那里很陡：高价只在少数状态中以大幅变动出现，低价被压缩，所以分布右偏。

## 数据与复现

* FRED：DEXUSEU、DEXJPUS、DEXUSUK、DEXSZUS、DEXUSAL、DEXCAUS、DEXUSNZ、DEXNOUS、DEXSDUS（中午汇率）；IR3TIB01xxM156N（经合组织3个月利率）；TEDRATE与DTB3（美元LIBOR，至2022年1月）；LIOR3MUKM（英镑LIBOR，至2017年）；T5YIE、T10YIE、T5YIFR、CPIAUCSL；MHHNGSP、PNGASEUUSDM；NIKKEI225。冻结到2025年并校验哈希。
* 英格兰银行：XUDLUSS、XUDLDS3（即期与3个月远期，至2021年6月），XUDLDMS（每英镑的德国马克）。
* 美国能源信息署：RCLC1–4与RNGC1–4，NYMEX每日结算价（公布至2024年4月）。
* CFTC：合约042601、044601、043602、020601的金融期货交易者报告。
* 引用而非计算的公开数字：瑞士央行的决定；FXCM的申报文件；欧洲汇率机制的区间与英国财政部的成本；Amaranth的损失（美国参议院调查小组委员会，据EDHEC的概述）；CME的通告；美联储对基差交易的估计；Optiver的和解。
* 屏幕上标注为示意的输入：外汇期权市场（欧元/美元、美元/日元）、冲击模型的参数、Working曲线、点火价差期权、国债交易的价格、Bachelier看跌期权的波动率。
* 本部分不打开任何样本外数据；试验计数器保持在315。

## 写给研究者

* **定理。** Gustafson（1958）；Williams与Wright，《储存与大宗商品市场》（1991）；迪顿与拉罗克（1992），*Rev. Econ. Studies* 59，以及（1996），*J. Political Economy* 104；Cafiero、Bobenrieth、Bobenrieth与Wright（2011），*J. Econometrics* 162；Working（1949）；Kaldor（1939）。
* **简化。** 独立同分布的收成、固定储存成本、风险中性储存者、无储存上限；一期并未校准为一个月；数据中的库存偏离用五年同月平均。
* **开放问题。** 持续性；曲线中的风险溢价；储存能力上限。
