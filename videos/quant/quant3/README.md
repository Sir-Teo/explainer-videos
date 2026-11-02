# Quant, Built — Part 3: Value, Accounting and the Firm

Part 3 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)); the last part of Act I, Markets and Money. It asks what a share is a claim on. It
values that claim with the arithmetic of time value and discounted cash flow, and reads it off the three financial
statements. It then measures what the accounting has and has not told investors: Shiller's excess volatility, the
CAPE, and five accounting signals before and after they were published. Every number is computed by the series' own
code ([`compute.py`](compute.py), the House's
[`valuation`](../../../explainer/quant/house/valuation.py) and
[`fundamentals`](../../../explainer/quant/house/fundamentals.py) modules) from public data: Robert Shiller's monthly
US market data since 1871 and Kenneth French's portfolios sorted on accounting signals. Schematics and
illustrative numbers are labeled on screen. Firms and events are described from the public record.

*An education in methods, not investment advice.*

## Chapters (about 45 minutes)

* **What is a share a claim on?** Shiller (1981) on 150 years of data: the real S&P composite against p\*, the
  present value of the dividends actually paid, discounted at the average real return (8.3%). The standard deviation
  of annual log changes is 17.5% for the price and 2.1% for p\* (8×). 40 years moved by more than 20%; p\* never
  did. Then the objectives, and the House's fundamentals store.
* **1. Time value.** Present value, NPV, annuities, perpetuities, IRR (a 5% ten-year bond is worth 108.11 at 4%, and
  its IRR at 100 is 5.00%). Gordon's growth model derived as a geometric series (Williams 1938; Gordon and Shapiro
  1956), and its sensitivity: a dividend of 5 growing 3% is worth 100 at 8%, 125 at 7% and 250 at 5%.
* **2. The three statements.** A toy firm's year in three linked ledgers. Net income of 200 flows to the cash flow
  statement and, less dividends, to equity, while the change in cash (−100) flows to the balance sheet, which
  balances at 800. Earnings = cash flow + accruals (200 = 100 + 100). Sloan (1996). XBRL, mandated by the SEC from 2009
  to 2011, with filing dates and restatements.
* **3. Discounted cash flow.** Free cash flow and the WACC (7.74% for the toy firm). A five-year DCF at 8% with 2%
  terminal growth: 1,936, of which 76% is the terminal value. The value surface in 3D over r ∈ [6%, 12%] and
  g ∈ [0, 4%]: 1,017 to 5,445. At 7% it is 2,329, at 3% growth 2,249, and at both 2,816 (+45%).
* **4. Multiples and the CAPE.** P/E = b/(r − g); EV/EBITDA. The CAPE since 1881 averages 17. It was 32.6 in
  September 1929, 44.2 in December 1999, 4.8 in December 1920, 6.6 in 1982 and 33.8 in December 2020. Regressing the
  next ten years' real total return on log CAPE gives a slope of −0.074 and R² = 0.32 across 1,560 overlapping
  starts, which are only about 13 independent decades. The end-2020 prediction is 0.6% a year, sealed and registered.
* **5. Modigliani and Miller.** Proposition I by home-made leverage (an arbitrage proof). Proposition II:
  r_E = r_A + (r_A − r_D)D/E, with the WACC flat. Taxes (1963) and the trade-off theory (illustrative distress costs).
* **6. Dividends, buybacks, and equity as an option.** Payout irrelevance (1961): a dividend or a buyback leaves owners
  with 10 a share. A buyback lifts EPS by 9% with the price unchanged. The dividend yield averaged 4.9% from 1871 to
  1982 and 2.5% from 1983 to 2020, after Rule 10b-18 (November 1982). Merton (1974) treats equity as a call on the
  assets and debt as riskless debt minus a put. The chapter ends on asset substitution and real options.
* **7. Accounting signals that became factors.** Ball and Brown (1968) and Bernard and Thomas (1989), as a schematic.
  Five decile long-shorts on French's value-weighted sorts, July 1963 to 2020: accruals, operating profitability,
  investment, book-to-market and earnings yield. Annual means before → after publication: 5.0 → 2.1%, 2.3 → 3.1% (too
  few years after to judge), 6.4 → −1.1%, 6.9 → 1.0% and 7.5 → 2.6%. On average 5.6% → 1.5%, compared with McLean and
  Pontiff (2016). The trial counter is shown.
* **8. Corporate events: merger arbitrage.** The spread as a forecast (an implied 80% chance of closing). Mitchell and
  Pulvino (2001): 4,750 mergers from 1963 to 1998, returns shaped like a short index put, and about 4% a year in
  excess returns after costs. The firm file is AbbVie and Shire (2014).
* **9. When the statements lie.** Enron: the restatement of 8 November 2001 removed $586 m; bankruptcy followed on
  2 December; the SEC found more than $5 bn of prepays booked as operating cash. Wirecard: €1.9 bn of trust cash,
  about a quarter of the balance sheet, most likely did not exist; insolvency on 25 June 2020; BaFin's short ban of
  February 2019. Then what a quant takes from both.
* **10. The fundamentals store.** The House's bitemporal store and its as-of query on one restated fact. Rule 4: a
  reported number exists from the day it was filed, as first reported, and a restatement is a new fact.
* **Recap, desk questions, problems.**

## Build it

```bash
python -m videos.quant.quant3.compute                       # every number, cached in .cache/quant3/ (seconds)
EXPLAINER_TTS=silent python tools/qa_scene.py quant3 DCF       # one chapter, silent, with a contact sheet
python tools/make.py quant3 --cpu-voice -q m                # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **A debt-free firm buys back 10% of its shares at market.** Without taxes or information effects the price does
   not move: the firm gives up cash worth exactly what it pays, and each remaining share keeps the same claim
   (Modigliani–Miller, 1961). Earnings per share rise if the earnings yield E/P exceeds the after-tax return the cash
   was earning. In the chapter's example the operations earn 10% of their value and the cash earned 2%, so EPS goes
   from 0.92 to 1.00 (+9%) and the P/E falls from 10.9 to 10. Higher EPS is not higher value. In practice, a buyback
   can also signal that managers think the shares are cheap, and it changes the tax paid by the owners.
2. **$2 next year, 4% growth, price $50.** Rearrange Gordon: r = D₁/P + g = 2/50 + 4% = 8%. The market's expected
   return is the dividend yield plus the growth rate.
3. **47 under a cash offer of 50, 35 if it breaks, six months, 4% a year.** Under the risk-neutral measure the
   expected payoff, discounted, equals the price: p·50 + (1 − p)·35 = 47 × 1.02 = 47.94, so p = 12.94/15 ≈ 86%.
   Ignoring the interest gives 80%. A risk-neutral probability is not a forecast, though: arbitrageurs demand a
   premium for the crash risk of chapter 8, so the real chance of closing is higher still.

## Problems, with solutions

1. **P/E from Gordon.** P = D₁/(r − g), and D₁ = bE₁, so P/E₁ = b/(r − g). A P/E of 30 with b = 0.5 needs
   r − g = 0.5/30 = 1.67%, so at r = 8% the market must expect g ≈ 6.3% forever, faster than nominal GDP has grown in
   most decades.
2. **The DCF.** The five forecasts are 105, 110.25, 115.76, 121.55 and 127.63, with present values at 8% of 97.2, 94.5,
   91.9, 89.3 and 86.9 (459.8 in all). The terminal value at year 5 is 127.63 × 1.02/0.06 = 2,169.7, worth 1,476.6
   today. Total 1,936.5, of which the terminal share is 76%. At 7% and 3% the total is 2,816 (+45%).
3. **Modigliani–Miller.** Without taxes, r_E = 8% + (8% − 4%) × 1 = 12% and the WACC is ½·12% + ½·4% = 8%, the same as
   r_A. With a 21% tax rate the cost of equity becomes r_E = r_A + (r_A − r_D)(1 − t)D/E = 11.16%, and the WACC is
   ½·11.16% + ½·4%·0.79 = 7.16%. Without taxes, cheaper debt is exactly offset by dearer equity. With taxes, the
   government pays part of the interest, so the firm's after-tax cost of capital falls, and the value rises by the tax
   shield.
4. **Merton.** Black–Scholes with S = A = 100, K = F = 80, T = 5, σ = 25% and r = 2% gives equity E = 35.75. The
   debt is A − E = 64.25. Its yield is −ln(64.25/80)/5 = 4.39%, a spread of 2.39% over the 2% riskless rate. The
   risk-neutral chance of default, N(−d₂), is 38%.
5. **Overlapping windows.** Each ten-year window shares all but one month with its neighbour, so the 1,560 windows
   contain about 1,560/120 = 13 independent decades. When the predictor barely changes within a decade, as the CAPE
   does, the regression's errors are almost perfectly correlated across neighbouring windows. Treating them as
   independent overstates the t-statistic by roughly √120 ≈ 11. Part 6 derives the corrections (Hansen–Hodrick,
   Newey–West) and Stambaugh's bias for persistent predictors.

## Data and reproducibility

* Robert Shiller's `ie_data.xls` (monthly S&P composite price, dividends, earnings, CPI, the 10-year yield and the
  CAPE), read with `xlrd`. The research window ends in December 2020, and the hold-out from 2021 is sealed in
  [`../data/envelope.json`](../data/envelope.json). The file stops in September 2023, so the CAPE forecast for
  2021–30 will be scored on a second source in the finale.
* Kenneth French's `Portfolios_Formed_on_{AC,OP,INV,BE-ME,E-P}`, value-weighted monthly returns, July 1963 to
  December 2020. The hold-out from 2021 is sealed. The long-shorts use deciles 10 and 1, before costs.
* The SEC's XBRL company facts (EDGAR) are the intended source of the fundamentals store. EDGAR asks for a contact
  e-mail in every request, so this part builds and tests the store on a constructed example and leaves loading real
  filings to a machine set up with one.
* The toy firm, the DCF, the trade-off curve, the post-earnings drift and the merger-arbitrage payoff are illustrative
  or schematic, and labeled so.

---

# 量化金融，从零搭建 — 第3部分：价值、会计与企业

本部分追问一股股票究竟是对什么的索取权：用货币时间价值和现金流折现为这项索取权估值，从三张财务报表中读出它，再测量会计究竟告诉了
投资者什么、没告诉什么：Shiller的“过度波动”、CAPE，以及五个会计信号在论文发表前后的表现。所有数字都由本系列自己的代码根据公开数据算出。

*讲的是方法，不构成投资建议。*

## 交易台问题与解答

1. **一家无负债公司以市价回购10%的股份。** 在没有税收和信息效应时，股价不变：公司付出的现金恰好等于它换回的价值，剩余每股的索取权不变
   （莫迪利亚尼–米勒，1961）。只要盈利收益率E/P高于这笔现金原本的税后收益，每股收益就会上升。本章例子中经营资产的收益率为10%，现金只赚2%，
   所以每股收益从0.92升到1.00（+9%），市盈率从10.9降到10。每股收益提高并不等于价值提高。现实中回购还可能传递“管理层认为股价便宜”的信号，
   并改变股东的税负。
2. **明年分红2美元、永续增长4%、股价50美元。** 把戈登公式反过来：r = D₁/P + g = 2/50 + 4% = 8%。市场的预期收益等于股息率加增长率。
3. **现金要约50，现价47，失败则跌到35，六个月后完成，年利率4%。** 在风险中性测度下，折现后的期望收益等于价格：
   p·50 + (1 − p)·35 = 47 × 1.02 = 47.94，所以p = 12.94/15 ≈ 86%；忽略利息则为80%。风险中性概率不是预测：套利者因第8章的崩盘风险
   要求溢价，所以真实的成交概率还要更高。

## 习题与解答

1. **由戈登模型得市盈率。** P = D₁/(r − g)，D₁ = bE₁，所以P/E₁ = b/(r − g)。b = 0.5、市盈率30时需要r − g = 0.5/30 = 1.67%，
   因此r = 8%时市场必须预期g ≈ 6.3%永续增长，比大多数年代的名义GDP增速还快。
2. **现金流折现。** 五年预测为105、110.25、115.76、121.55、127.63，按8%折现的现值为97.2、94.5、91.9、89.3、86.9（合计459.8）。
   第5年的终值为127.63 × 1.02/0.06 = 2,169.7，现值1,476.6。合计1,936.5，终值占76%。在7%与3%下合计为2,816（+45%）。
3. **莫迪利亚尼–米勒。** 无税时r_E = 8% + (8% − 4%) × 1 = 12%，加权平均资本成本为½·12% + ½·4% = 8%，等于r_A。税率21%时
   r_E = r_A + (r_A − r_D)(1 − t)D/E = 11.16%，加权平均资本成本为½·11.16% + ½·4%·0.79 = 7.16%。无税时，便宜的债务恰好被更贵的股权抵消；
   有税时，政府替企业付了一部分利息，所以税后资本成本下降，价值增加了税盾。
4. **默顿模型。** 用布莱克–斯科尔斯公式，S = A = 100，K = F = 80，T = 5，σ = 25%，r = 2%：股权E = 35.75，债务A − E = 64.25。
   债务收益率为−ln(64.25/80)/5 = 4.39%，比无风险利率2%高出2.39%。风险中性违约概率N(−d₂)为38%。
5. **重叠窗口。** 每个十年窗口与相邻窗口只差一个月，所以1,560个窗口大约只有1,560/120 = 13个独立的十年。当预测变量在十年内几乎不变时
   （CAPE正是如此），回归误差在相邻窗口间几乎完全相关，把它们当成独立样本会把t统计量高估约√120 ≈ 11倍。第6部分推导修正方法
   （Hansen–Hodrick、Newey–West）以及持续性预测变量的Stambaugh偏差。
