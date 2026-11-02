# Quant, Built — Part 2: The Machinery of Markets

Part 2 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)); the second part of Act I, Markets and Money. It follows a trade from the button to
settlement, and measures what the market's plumbing does to anyone who trades: clearing, margin and liquidation on
a real crash, short selling, repo and haircuts, fees, and the rules of markets around the world. Every number is
computed by the series' own code ([`compute.py`](compute.py), the House's funding desk in
[`explainer/quant/house/funding.py`](../../../explainer/quant/house/funding.py)) from public data: Binance's
Bitcoin perpetual futures and funding rates, FRED's money-market rates, and Kenneth French's market returns.
Simulations and schematics are labeled on screen; firms and events are described from the public record, with
allegations labeled as allegations.

*An education in methods, not investment advice.*

## Chapters (about 45 minutes)

* **What happens when you press buy?** The life of a trade: broker, exchange or wholesaler, the clearing house
  (novation), the depository (T+1). The crisis that opens the part: Robinhood on 28 January 2021, when the NSCC asked
  for a deposit of about $3 billion against unsettled trades, later reduced to about $1.4 billion as its chief
  executive described it (accounts differ); objectives; the House's treasury and funding desk.
* **1. The instruments.** Shares, bonds, futures, swaps, options and ETFs, and how each is quoted; notional and
  leverage.
* **2. Orders, books and auctions.** Market, limit and stop orders; the order book and price-time priority; a market
  order walking the book; a closing auction of 300 simulated orders (clears at 100.07, 14,535 shares); exchanges,
  dealer markets, request for quote; wholesalers.
* **3. Clearing and settlement.** Novation and the default waterfall; netting on a simulated day (5,395 trades among
  25 members: $11.0 bn gross, $3.1 bn bilateral, $1.0 bn through a CCP, −91%); US settlement from T+5 to T+1
  (28 May 2024).
* **4. Margin and leverage.** Initial, variation and maintenance margin; the liquidation price
  P₀(1 − 1/L)/(1 − m); three long BTC perpetual positions from 1 March 2020 ($8,555) on Binance's hourly prices: 10×
  liquidated on 9 March, 3× on 12 March, 2× on 13 March at the low ($4,063, −53%), $271 below zero; funding through
  2020 (17.2% a year on average, longs paying 86% of the time; $2,238 to hold one coin long).
* **5. Short selling.** Locate, borrow, fees, recall, dividends; the asymmetric payoff and the squeeze; Volkswagen,
  26–29 October 2008 (Porsche's 74.1%; above €1,000 intraday; the funds' allegations and Porsche's denial).
* **6. Repo, lending and prime brokers.** Repo as a secured loan; SOFR; haircuts as leverage limits (1/h);
  prime brokerage and total return swaps; Archegos (March 2021: about $5.5 bn lost at Credit Suisse, about $2.9 bn at
  Nomura, as the banks reported).
* **7. The day repo broke.** FRED's SOFR, fed funds and interest on reserves, August–October 2019: SOFR 2.20% (13 Sep),
  2.43% (16), 5.25% (17), 2.55% (18); bank reserves at $1.39 tn, down from $2.05 tn at the start of 2018; the crisis
  file.
* **8. Who earns what.** Sell side and buy side; fees compounded: the US market's 94 calendar years as a fund's gross
  returns turn $1 into $7,893; after 2 and 20 with a high-water mark, $360 (the investor keeps 4.5% of the profit);
  after a 1% fee, $3,288; where quants work and the roles.
* **9. Markets around the world.** The US, Europe and the UK (T+1 planned for 2027), Japan, India (SEBI, September
  2024: 93% of individual F&O traders lost money over FY2022–24, about Rs 1.8 lakh crore), China's A-shares (T+1 for
  shares, ±10% and ±20% price limits, Stock Connect); what price limits do to returns.
* **10. The funding desk.** The House's `funding` module and its rule 3: every backtest pays for its funding, margin
  and fees, and is closed out when the exchange would have closed it out.
* **Recap, desk questions, problems.**

## Build it

```bash
python -m videos.quant.quant2.compute                     # every number, cached in .cache/quant2/ (seconds)
EXPLAINER_TTS=silent python tools/qa_scene.py quant2 Margin  # one chapter, silent, with a contact sheet
python tools/make.py quant2 --cpu-voice -q m              # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **Make me a market on the number of trading days in a US year.** 365 days less 104 weekend days is 261 weekdays;
   the NYSE closes for 9 or 10 holidays (and occasionally for a day of national mourning), so a year has about
   250–252 trading days. A tight market, say 249 bid at 252 offered, shows you know the answer; the point of the
   game is how you widen or move the quote when you are hit.
2. **10× long, three daily falls of 4%, then +20%.** The cumulative fall after three days is 1 − 0.96³ = 11.5%. With a
   maintenance margin of 0.5%, a 10× long is liquidated after a fall of 1 − 0.9/0.995 = 9.5%, so the position was
   closed on day three; the rally comes too late, and the profit is the loss of the whole margin.
3. **2 and 20, −20% then +25% before fees.** After year one the fund is at 0.80 less the 2% management fee, about 0.78,
   below its high-water mark of 1. A 25% gain takes it to about 0.98, still below the mark: no performance fee, only
   the management fee. The investor is down about 4% over two years in which the gross return was zero.

## Problems, with solutions

1. **Liquidation prices.** Long one unit at P₀ with margin P₀/L: equity at price P is P₀/L + (P − P₀); liquidation when
   it equals mP, so P = P₀(1 − 1/L)/(1 − m). Short: equity P₀/L − (P − P₀) = mP gives P = P₀(1 + 1/L)/(1 + m). With
   m = 0.5%, the fall a long survives is 1 − (1 − 1/L)/0.995: 9.5% at 10×, 33.0% at 3×, 49.7% at 2×. A 33% fall
   liquidates a 3× long at the margin; 2× survives it.
2. **Netting.** Gross: 10 + 10 + 10 + 5 = 35. Bilateral: A–B 10, B–C 10, and C–A nets 10 against 5, leaving 5: 25 in
   all. Multilateral: A pays 15 and receives 10 (net −5), B pays 10 and receives 10 (0), C pays 10 and receives 15
   (+5): the CCP moves 5.
3. **Haircuts.** Each dollar of collateral borrows 1 − h, which buys 1 − h of collateral, which borrows (1 − h)², and
   so on: 1 + (1 − h) + (1 − h)² + … = 1/h. At 2% the most leverage is 50×; at 4%, 25×. A fund at the limit with
   equity E holds 50E of assets and may hold only 25E: it must sell half its assets, into a market where others are
   doing the same.
4. **Funding.** 0.016% per 8 hours is 0.016% × 3 × 365 ≈ 17.5% a year paid by longs. A cash-and-carry trade earns it:
   buy the coin, short the perpetual, collect the funding. Its risks: funding can turn negative; the short leg needs
   margin, and a sharp rally can liquidate it even though the hedge has gained (the margin sits on a different
   account, or exchange); and the exchange itself can fail (Part 39).
5. **Fees.** Gross: 1.10³⁰ = 17.4. A 1% fee on assets makes each year ×1.09: 1.09³⁰ = 13.3. Two and twenty with no
   losses: each year the fund grows to 1.08 after the 2%, and pays 20% of the 0.08 gain: ×1.064, and 1.064³⁰ = 6.4.
   The investor ends with 37% of the gross wealth, and keeps 33% of the gross profit.

## Data and reproducibility

* Binance's public archive (data.binance.vision): USD-M BTCUSDT perpetual hourly and daily candles; funding-rate
  history from January 2020; each file checked against Binance's published SHA-256 and the series' manifest.
* FRED (Federal Reserve Bank of St. Louis): SOFR, DFF, IOER, WRESBAL; frozen through 31 December 2025.
* Kenneth French's daily US market returns (the fees chapter), research window to 2020.
* The netting day and the auction are simulations with fixed seeds; Volkswagen's prices are reported figures shown as
  a four-point schematic, not a series.

---

# 量化金融，从零搭建 — 第2部分：市场的机器

本部分跟随一笔交易从按下按钮直到结算，并测量市场的“管道”对每个交易者做了什么：清算、真实崩盘中的保证金与强平、卖空、回购与折扣率、
费用，以及世界各地市场的规则。所有数字都由本系列自己的代码根据公开数据算出。

*讲的是方法，不构成投资建议。*

## 交易台问题与解答

1. **给美国一年的交易日数报个价。** 365天减去104个周末日是261个工作日；纽交所每年休市9到10个节假日（偶尔还有国丧日），所以一年
   大约250到252个交易日。报一个窄的价差，比如249买、252卖，说明你知道答案；这个游戏真正考的是被成交之后你如何调整报价。
2. **10倍做多，连续三天各跌4%，然后涨20%。** 三天累计下跌1 − 0.96³ = 11.5%。维持保证金0.5%时，10倍多头在下跌
   1 − 0.9/0.995 = 9.5%时被强平，所以第三天就已被平仓；反弹来得太晚，盈利等于损失全部保证金。
3. **2加20，扣费前先跌20%再涨25%。** 第一年后基金为0.80，再扣2%管理费，约0.78，低于高水位线1。上涨25%后约0.98，仍低于高水位线：
   没有业绩报酬，只有管理费。两年的毛收益为零，投资者却亏了约4%。

## 习题与解答

1. **强平价格。** 在P₀做多一单位、保证金P₀/L：价格为P时权益为P₀/L + (P − P₀)；当它等于mP时强平，P = P₀(1 − 1/L)/(1 − m)。
   空头：P₀/L − (P − P₀) = mP，得P = P₀(1 + 1/L)/(1 + m)。m = 0.5%时，多头能承受的跌幅为1 − (1 − 1/L)/0.995：10倍9.5%，
   3倍33.0%，2倍49.7%。下跌33%恰好让3倍多头被强平；2倍能挺过去。
2. **净额结算。** 总额：10 + 10 + 10 + 5 = 35。双边：A–B 10，B–C 10，C–A 10与5相抵剩5，合计25。多边：A付15收10（净−5），
   B付10收10（0），C付10收15（+5）：中央对手方只需转移5。
3. **折扣率。** 每1美元抵押品可借1 − h，再买1 − h的抵押品，又可借(1 − h)²……总和为1/h。2%时最多50倍；4%时25倍。
   处于上限的基金，权益为E时持有50E资产，现在只能持有25E：必须卖掉一半资产，而市场上的其他人也在同时卖。
4. **资金费率。** 每8小时0.016%，即0.016% × 3 × 365 ≈ 每年17.5%，由多头支付。期现套利可以赚取它：买入现货，做空永续合约，收取资金费。
   风险：资金费率可能转负；空头需要保证金，急涨时即使对冲整体赚钱也可能被强平；交易所本身可能倒闭（第39部分）。
5. **费用。** 毛收益：1.10³⁰ = 17.4。1%管理费使每年乘以1.09：1.09³⁰ = 13.3。2加20且从不亏损：每年扣2%后为1.08，
   再付0.08收益的20%：每年乘以1.064，1.064³⁰ = 6.4。投资者最终只得到毛财富的37%，毛利润的33%。
