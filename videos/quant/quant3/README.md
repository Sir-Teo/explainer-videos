# Quant, Built — Part 3: Value, Accounting and the Firm

Part 3 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)); the last part of Act I, Markets and Money. It asks what a share is a claim on, values
that claim with the arithmetic of time value, discounted cash flow, implied returns and residual income, and reads it
off the three financial statements, which it runs as one double-entry machine. It then measures what the accounting
has and has not told investors: Shiller's excess volatility, the duration of equity, the CAPE and the
Campbell–Shiller identity, Sloan's accruals, earnings announcements, 208 published predictors before and after
publication, merger arbitrage, and forensic screens. Every number is computed by the series' own code
([`compute.py`](compute.py), the House's [`valuation`](../../../explainer/quant/house/valuation.py) and
[`fundamentals`](../../../explainer/quant/house/fundamentals.py) modules) from public data. Schematics, illustrative
numbers and simulations are labelled on screen. Firms and events are described from the public record; allegations
are labelled as allegations, and settlements without admission are said to be so.

*An education in methods, not investment advice.*

## Chapters (about 55 minutes)

* **What is a share a claim on?** Shiller (1981) rebuilt on screen: p\* by the backward recursion
  p\*ₜ = (p\*ₜ₊₁ + Dₜ)/(1 + r), 1871–2020, at the average real return (8.3%). The price moves 8× as much as p\* from
  year to year (17.5% against 2.1%); 40 years moved more than 20%, p\* never did. How we got here (Pacioli, Graham and
  Dodd, Modigliani–Miller, Ball–Brown, Merton, Sloan, Enron, XBRL). Objectives; the House.
* **1. Time value, IRR and the growing perpetuity.** Twenty-four payments on a receding 3D conveyor as r rises from
  2% to 12%. The annuity as a difference of perpetuities. **Lab:** `valuation.irr_bisect` on a 5% bond (30 halvings:
  5.0000%). A project (−100, +230, −132) with two IRRs, 10% and 20% (a quadratic in 1 + r); NPV at 15% is +0.19.
  Gordon's model derived.
* **2. The duration of equity.** −∂ln P/∂r = 1/(r − g); Macaulay duration (1 + r)/(r − g): 33 and 36 years at r = 8%,
  g = 5%. The PV-weight histogram with its balance point running off as g → r, beside a 30-year bond. Measured on
  French's book-to-market deciles against the monthly change in the 10-year yield, July 1963 – 2020 (690 months):
  growth −2.07% per point (s.e. 0.78), value −1.35% (0.95). The order is duration's; the size is a tenth of Gordon's
  −33%, because g moves with r. Dechow–Sloan–Soliman's implied durations of about 15 years.
* **3. The three statements, running.** The toy firm's year in three linked ledgers; then the House's accounting
  simulator over twenty quarters, the balance sheet balancing to the cent, net income against operating cash flow
  (852 against 1,393 over five years). **Lab:** `fundamentals.step`, the assertion that assets equal claims; sales
  doubled on 90% credit give net income +125 and operating cash flow −300. The indirect cash flow statement and DuPont
  (ROE 18.0% = 14.5% × 1.05 × 1.18) derived.
* **4. Accruals: where earnings and cash part.** Sloan's persistence regression derived; his estimates (1962–1991):
  0.855 for cash, 0.765 for accruals, 0.841 for earnings. The mechanism in 3D on a simulated panel whose accruals carry
  a reversing error (2,000 firms × 9 years, firm-clustered): 0.80 against 0.67. On the seven non-bank firms in the
  EDGAR cache (59 firm-years, FY2009–2019): 1.25 (±0.31) against 0.99 (±1.13), the right order, far too few to separate.
  The accrual long-short (Chen–Zimmermann): 0.44% a month, 1963–2020, t = 6.2.
* **5. XBRL and the point-in-time store.** Release 33-9002's phase-in (2009–2011); 10-K deadlines of 60/75/90 days. The
  bitemporal plane of General Electric's revenue (47 filed values, FY2008–2020) with an as-of line sweeping; the
  history it returns changes as GE's recasts arrive. **Lab:** `Store.history` on Kraft Heinz: FY2016–17 net income
  3,632 and 10,999 ($m) as of mid-2018, 3,596 and 10,941 as of mid-2020 (restated June 2019; SEC 2021-174, $208 m of
  cost savings, $62 m penalty, settled without admitting or denying). The audit of eight firms: GE's revenue changed in
  13 of 14 years (recasts); median 55 days to the 10-K.
* **6. Free cash flow and the DCF surface.** FCFF from the statements; g = reinvestment × RONIC; the value-driver
  formula and ∂TV/∂g > 0 ⇔ RONIC > WACC derived; the bridge to equity. The five-year DCF (1,936, 76% terminal value);
  the (r, g) surface; the (g, RONIC) surface with its flat ridge at RONIC = WACC (1,250 for any g). Monte Carlo, 20,000
  draws: 5–95% from 1,257 to 2,892 (0.65× to 1.49× the base).
* **7. The cost of capital the market implies.** WACC (7.74% for the toy firm), levered betas, the CAPM, APV. The
  balance beam: the S&P 500 at end-2020 against its discounted cash to owners levels at 5.13%, an implied premium of
  4.20%. **Lab:** `valuation.implied_rate` at end-1999 (1.59%), 2008 (8.24%) and 2020 (4.20%). Damodaran's FCFE
  premium rebuilt 1960–2020: within 0.2 pt in 42 of 60 years; the gaps (1995–2009) are where his column used inputs the
  spreadsheet does not carry.
* **8. Residual income and price-to-book.** Ohlson (1995) derived from clean surplus by telescoping;
  P/B = 1 + (ROE − r)/(r − g). The P/B surface over (ROE, g) crossing P/B = 1 along ROE = r. A firm whose ROE fades
  from 15% to 8%: P/B 1.21. RI = DDM on the toy firm's statements to 9 × 10⁻¹³.
* **9. Multiples, the CAPE, and what the dividend yield predicts.** P/E = b/(r − g), PVGO, EV/EBITDA. The CAPE since
  1881 (average 17; 33.8 at end-2020); the ten-year regression (R² 0.32, about 13 independent decades); the sealed
  forecast (0.6% a year). The Campbell–Shiller identity and Cochrane's decomposition derived; on Shiller's annual data,
  1871–2020: long-run return slope 0.60, dividend-growth slope −0.35 (b_r = 0.049, NW t 1.3; φ = 0.956, ρ = 0.961). The
  tug of war: 1871–1945 dividends carry it (0.35 / −0.68); 1946–2020 returns (0.97 / −0.01). Stambaugh bootstrap
  (5,000 samples, no predictability): slopes this large 20% of the time.
* **10. Modigliani and Miller, with taxes and distress.** Proposition I by home-made leverage; Proposition II; the
  tax shield T·D derived; Miller (1977): at US top rates since 2018 (21%, 20%, 37%) the net gain is −0.3%. The fixed
  pie with the government's wedge and a distress ring (illustrative); Graham–Harvey's 392 CFOs: flexibility 59.4%,
  credit rating 57.1%, tax advantage 44.9%, distress costs 21.4%.
* **11. Payout: dividends, buybacks and issuance.** Miller–Modigliani (1961) proved by algebra; the EPS illusion
  (0.92 → 1.00); two simulated firms, one paying dividends and one buying back, whose owners both reach 25.94; the
  dividend yield around Rule 10b-18 (1982); French's net-issuance sorts (repurchasers 13.4% a year, top issuers 7.0%,
  1963–2020); net payout yield 0.88 → 0.81 and share issuance 0.71 → 0.29 % a month after publication.
* **12. Equity as a call.** Merton (1974). The equity and debt surfaces over (assets, volatility), debt 80 due in a
  year: doubling a near-default firm's volatility moves 6.57 from lenders (57.92 → 51.35) to owners (2.08 → 8.65).
  Myers's overhang: a project costing 10 that adds 15 raises equity by only 5.46. Real options (illustrative).
* **13. Earnings announcements and the drift.** Ball–Brown (schematic); SUE and CAR defined. **Lab:**
  `fundamentals.car` on Apple's 8-K 2.02 announcements, October 2015 – 2020 (21 events, SPY-adjusted): correlation of
  SUE and the day-0 move 0.08; drift after day 1 of −1.1% for beats and +8.1% for misses (the wrong way: a lab, not a
  test). At scale (Chen–Zimmermann's EarningsSurprise, Foster–Olsen–Shevlin 1984): 1.13% a month in sample, 0.38 after
  publication (t 4.5), −0.01 since 2006 (t −0.1): Martineau (2022).
* **14. Accounting signals that became factors, and decayed.** Piotroski's nine tests; Novy-Marx's gross
  profitability. Five French long-shorts before and after publication. All 208 OSAP predictors (release 2024.10) with
  two years in sample and after publication: 0.69 → 0.43 (out of sample) → 0.26 % a month (×0.38; bootstrap over
  predictors 0.31–0.45); the 99 accounting ones 0.58 → 0.45 → 0.22. Accruals 0.69 → 0.14; F-score 0.94 → 0.98; GP
  0.30 → 0.62. The trial counter.
* **15. Merger arbitrage.** p = (P e^{rτ} − B)/(O − B) derived. Capri under Tapestry's $57 offer (weekly, 2023–24,
  pre-deal close $35.51): the implied probability through the FTC suit (April 2024), the injunction (24 October 2024)
  and the termination (14 November 2024). The Merger Fund against the S&P 500, 1989–2020 (351 months; 5.7% a year,
  volatility 5.4%): slope 0.12 above a −4% market month, 0.24 below; the extra slope's bootstrap band [−0.04, 0.34]
  includes zero. Mitchell–Pulvino (2001). AbbVie–Shire (2014).
* **16. When the statements lie.** Enron; Wirecard; Luckin Coffee (SEC 2020-319, alleged >$300 m of fabricated sales,
  $180 m penalty, neither admitted nor denied); Kraft Heinz. Beneish's M-score (coefficients and the −1.78 cut-off from
  the 1999 paper): Kraft Heinz FY2017 from its own 10-K, −1.82, not flagged; 1.4% of 69 firm-years flagged. The base
  rate: a screen that flags 15% and catches half of a 1% fraud rate is right 3.3% of the time; Dechow et al. (2011).
* **17. Who values firms for a living.** Graham–Harvey (NPV 74.9%, IRR 75.7%, multiples 38.9%, real options 26.6%);
  AQR's quality-minus-junk and OSAP; *Dell* ($13.75 deal, $17.62 Chancery DCF, $28.61 petitioners' expert; reversed
  December 2017); *Rural/Metro* ($75.8 m against RBC, affirmed 30 November 2015); S&P's financial-risk ratios; 13D
  activism (Brav et al. 2008, about 7%; 5 business days since October 2023); leases (SEC staff 2005, about $1.25 tn
  off balance sheet; ASC 842 from 2019) with the bridge run on an illustrative firm.
* **18. Frontier: machines reading the statements.** van Binsbergen–Han–Lopez-Lira (2023) and the 2025 reply; Cao et
  al. (2024); the two Kim–Muhn–Nikolaev working papers **withdrawn by their authors** (no claims drawn from them);
  FinanceBench (81% wrong or refused); Jensen–Kelly–Pedersen (2023); Gormsen–Lazarus (2023); Eisfeldt–Kim–Papanikolaou
  (2022). **Trained:** an earnings forecaster on a simulated panel (4,000 firms; 28,000 training rows, 8,000 test; 14
  items, 3 pure noise; losses persist 0.4, profits 0.8): test MSE ×10⁻⁴ — random walk 16.23, OLS 13.24, ridge on
  splines 13.18, MLP (2×16, 5 seeds) 13.18 (seed range 13.15–13.22), noise floor 12.50. The MLP does not beat OLS by
  more than its seed spread. Replayed through 22 checkpoints with the seed band.
* **Recap, desk questions, problems,** the House, payoffs, references.

## Build it

```bash
python -m videos.quant.quant3.compute                       # every number (minutes; the forecaster ~3 CPU-min)
EXPLAINER_TTS=silent python tools/qa_scene.py quant3 DCF       # one chapter, silent, with a contact sheet
python tools/make.py quant3 --cpu-voice -q m                # English and Chinese, narrated by Kokoro on the CPU
```

**EDGAR.** The fundamentals store reads the SEC's XBRL company facts and submissions (data.sec.gov). The SEC asks
every client to identify itself with a contact, so the loaders take it from the environment: set
`SEC_USER_AGENT="Your Name your.address@example.org"` before the first run on a new machine. This build used eight
companies' files already in `.cache/quant_data/edgar/` (Boeing, Exxon Mobil, GE, Wells Fargo, Apple, Microsoft, Capri,
Kraft Heinz; facts filed through 31 October 2026, checksummed in `videos/quant/data/manifest.json`). With a contact set,
the same code can load any CIK; the full-panel versions of chapters 4, 13 and 16 (thousands of firms) are the natural
extension.

## Textbook audit

| Textbook section | Where |
|---|---|
| Berk–DeMarzo ch. 2 (financial statement analysis) | ch. 3–5 |
| ch. 3–4 (law of one price, time value) | ch. 1, 10 |
| ch. 5–6 (interest rates, bonds) | ch. 1 (recall); Part 18 |
| ch. 7 (investment decision rules, IRR pitfalls) | ch. 1 |
| ch. 8 (capital budgeting, FCF) | ch. 6 |
| ch. 9 (valuing stocks: DDM, total payout, multiples) | ch. 1, 9, 11 |
| ch. 10–13 (risk and return, CAPM, cost of capital, efficiency) | ch. 7; Parts 1, 23 |
| ch. 14–16 (MM, debt and taxes, distress and agency) | ch. 10, 12 |
| ch. 17 (payout) | ch. 11 |
| ch. 18 (valuation with leverage: WACC, APV, FTE) | ch. 7 |
| ch. 19 (financial modelling) | ch. 6 |
| ch. 20–21 (options) | Part 10 |
| ch. 22 (real options) | ch. 12 |
| ch. 23–24 (raising capital, IPOs) | Part 2; not otherwise covered |
| ch. 25 (leasing) | ch. 17 (ASC 842) |
| ch. 26–27 (working capital, short-term planning) | ch. 3 (ΔNWC) only: corporate treasury, outside a quant syllabus |
| ch. 28 (M&A) | ch. 15 |
| ch. 29 (governance) | ch. 17 (activism) |
| ch. 30 (risk management) | Part 40 |
| ch. 31 (international) | Part 22 |
| Brealey–Myers–Allen ch. 2–6 (PV, bonds, stocks, NPV rules) | ch. 1, 6 |
| ch. 7–9 (risk, CAPM, cost of capital) | ch. 7; Part 23 |
| ch. 10–12 (project analysis, rents, agency) | ch. 6 (RONIC > WACC), 12 |
| ch. 14–16 (financing, issuing, payout) | ch. 11 |
| ch. 17–19 (debt policy, APV) | ch. 7, 10 |
| ch. 20–22 (options, real options) | ch. 12; Part 10 |
| ch. 23 (credit risk) | Part 20 |
| ch. 28 (financial analysis, ratios, DuPont) | ch. 3 |
| ch. 29–30 (planning, working capital) | not covered (corporate treasury) |
| ch. 31–32 (mergers, restructuring) | ch. 15 |
| Damodaran ch. 2–3 (approaches, statements) | ch. 3, 6 |
| ch. 7 (riskless rate, ERP, implied ERP) | ch. 7 |
| ch. 9–12 (earnings to cash flows, growth, terminal value) | ch. 6 |
| ch. 13–16 (DDM, FCFE, firm valuation, equity per share) | ch. 1, 6, 7 |
| ch. 17–20 (relative valuation) | ch. 9 |
| ch. 21–24 (financial, negative-earnings, young, private firms) | not covered: firm-specific valuation practice |
| ch. 25 (acquisitions) | ch. 15 |
| ch. 28–30 (real options, distressed equity) | ch. 12; Part 20 |
| ch. 31–32 (value enhancement, EVA) | ch. 8 (residual income) |
| Koller–Goedhart–Wessels ch. 2–3 (value creation, conservation of value) | ch. 6, 11 |
| ch. 6–7 (ROIC, growth) | ch. 6 |
| ch. 8–9 (frameworks; reorganising statements) | ch. 6–8 |
| ch. 10–12 (performance, forecasting, continuing value) | ch. 3, 6, 18 |
| ch. 13–14 (cost of capital; EV to equity) | ch. 6, 7 |
| ch. 15–16 (results, multiples) | ch. 9 |
| ch. 18–21 (taxes, provisions, leases, pensions) | ch. 6 (debt-like items), 17 (leases) |
| ch. 30, 32 (M&A; capital structure and payout) | ch. 10, 11, 15 |
| ch. 34–38 (emerging markets, high growth, cyclical, banks, flexibility) | flexibility in ch. 12; the rest not covered |
| Bodie–Kane–Marcus ch. 18 (DDM, PVGO, P/E) | ch. 1, 9 |
| ch. 19 (financial statement analysis, quality of earnings) | ch. 3–5, 16 |
| Campbell–Lo–MacKinlay ch. 7 (present-value relations) | ch. 9 |
| Luenberger ch. 2–3 (cash-flow streams, IRR) | ch. 1 |
| Penman, *Financial Statement Analysis and Security Valuation* (residual income) | ch. 8 |

## Desk questions, with solutions

1. **A debt-free firm buys back 10% of its shares at market.** Without taxes or information effects the price does
   not move: the firm gives up cash worth exactly what it pays, and each remaining share keeps the same claim
   (Miller–Modigliani, 1961). Earnings per share rise if the earnings yield E/P exceeds the after-tax return the cash
   was earning. In the chapter's example the operations earn 10% of their value and the cash earned 2%, so EPS goes
   from 0.92 to 1.00 (+9%) and the P/E falls from 10.9 to 10. Higher EPS is not higher value. In practice, a buyback
   can also signal that managers think the shares are cheap (chapter 11's sorts), and it changes owners' taxes.
2. **$2 next year, 4% growth, price $50.** Rearrange Gordon: r = D₁/P + g = 2/50 + 4% = 8%.
3. **47 under a cash offer of 50, 35 if it breaks, six months, 4% a year.** Under the risk-neutral measure:
   p·50 + (1 − p)·35 = 47 × 1.02 = 47.94, so p = 12.94/15 ≈ 86%; ignoring the interest gives 80%. A risk-neutral
   probability carries a premium for deal risk (chapter 15's short put), so the real chance is higher still.
4. **ROE 12%, cost of equity 8%, book growing 4% forever: P/B?** Residual income in steady state:
   P/B = 1 + (0.12 − 0.08)/(0.08 − 0.04) = 2. Check by Gordon on dividends: payout = 1 − g/ROE = 2/3, so
   P/B = ROE × payout/(r − g) = 0.08/0.04 = 2.

## Problems, with solutions

1. **P/E from Gordon.** P = D₁/(r − g) and D₁ = bE₁, so P/E₁ = b/(r − g). A P/E of 30 with b = 0.5 needs
   r − g = 1.67%: at r = 8%, g ≈ 6.3% forever.
2. **The DCF.** Forecasts 105, 110.25, 115.76, 121.55, 127.63; present values at 8%: 97.2, 94.5, 91.9, 89.3, 86.9
   (459.8). Terminal value at year 5: 127.63 × 1.02/0.06 = 2,169.7, worth 1,476.6 today. Total 1,936.5, 76% of it
   terminal. At 7% and 3%: 2,816 (+45%).
3. **Modigliani–Miller.** Without taxes r_E = 8% + 4% × 1 = 12% and the WACC is 8% = r_A. With a 21% tax rate
   r_E = r_A + (r_A − r_D)(1 − t)D/E = 11.16% and the WACC is ½·11.16% + ½·4%·0.79 = 7.16%. Without taxes cheap debt
   is offset by dearer equity; with taxes the government pays part of the interest, so the after-tax cost falls and
   value rises by the shield.
4. **Merton.** Black–Scholes with A = 100, F = 80, T = 5, σ = 25%, r = 2%: E = 35.75, D = 64.25, yield
   −ln(64.25/80)/5 = 4.39%, a spread of 2.39%; risk-neutral default probability N(−d₂) = 38%.
5. **Overlapping windows.** 1,560/120 ≈ 13 independent decades. With a predictor that barely changes within a decade,
   neighbouring windows' errors are almost perfectly correlated, and treating them as independent overstates t by
   roughly √120 ≈ 11. Part 6 derives the corrections (Hansen–Hodrick, Newey–West) and Stambaugh's bias.
6. **Two IRRs.** −100 + 230/x − 132/x² = 0 with x = 1 + r gives 100x² − 230x + 132 = 0, so x = 1.1 or 1.2: IRRs of
   10% and 20%. NPV(15%) = −100 + 200 − 99.81 = +0.19 > 0: accept at 15%, reject below 10% or above 20%.
7. **Campbell–Shiller.** The identity b_r − b_d + ρφ ≈ 1: 0.05 + 0.03 + 0.96 × 0.95 = 0.992, within the
   linearisation's error. Long-run slopes: b_r/(1 − ρφ) = 0.05/0.088 = 0.57 and b_d/(1 − ρφ) = −0.34; their difference,
   0.91, is the share of the yield's variance explained, with returns carrying about 0.57/0.91 ≈ 63% of it.

## Reading guide (beyond what is on screen)

Every paper in [`READING.md`](../READING.md)'s Part 3 list appears on screen. Penman's textbook is the residual-income
reference behind chapter 8. Hou–van Dijk–Zhang (2012), the cross-sectional earnings model, is the natural benchmark for
chapter 18's forecaster on a real panel. The two withdrawn Kim–Muhn–Nikolaev papers are shown only as withdrawn; nothing
is drawn from their results.

## Data and reproducibility

* Robert Shiller's `ie_data.xls` (monthly S&P composite since 1871, dividends, earnings, CPI, GS10, CAPE); research
  window to December 2020, hold-out from 2021 sealed in [`../data/envelope.json`](../data/envelope.json).
* Kenneth French's `Portfolios_Formed_on_{AC,OP,INV,BE-ME,E-P,NI}`, value-weighted, July 1963 – December 2020; NI's
  hold-out sealed too.
* Chen and Zimmermann's Open Source Asset Pricing, release 2024.10 (`PredictorLSretWide.parquet`, `SignalDoc.csv`,
  pinned to the Hugging Face branch `2024.10`, checksummed); months from 2021 sealed.
* Aswath Damodaran's `histimpl.xls` (implied ERP by year).
* Yahoo Finance: AAPL and SPY daily closes (2013–2021), MERFX and ^GSPC monthly adjusted closes (1989–2020), CPRI
  weekly closes (2023–24, a case file).
* SEC EDGAR company facts and submissions for eight firms (see **Build it**).
* Simulated, with the generating model stated: the toy firm and its simulator; the accrual panel of chapter 4; the
  forecaster's panel of chapter 18. Illustrative: the trade-off pie, the real option, the lease bridge.
* Trials registered this part: the five French signals, the CAPE forecast, the 208 OSAP predictors (as one
  meta-test with 208 trials), and the forecaster's 8 configurations.

---

# 量化金融，从零搭建 — 第3部分：价值、会计与公司

本部分追问一股股票究竟是对什么的索取权：用货币时间价值、现金流折现、隐含收益率和剩余收益为这项索取权估值，从三张财务报表中读出它，
并把三张报表当作一台复式记账的机器运转起来。然后测量会计究竟告诉了投资者什么、没告诉什么：席勒的过度波动、股权久期、CAPE与
坎贝尔–席勒恒等式、斯隆的应计项目、盈利公告、208个已发表预测变量在发表前后的表现、并购套利，以及财务造假筛查。所有数字都由本系列
自己的代码根据公开数据算出；示意图、示例数字和模拟都在画面上标明。公司与事件均取自公开记录；指控标注为指控，未承认也未否认的和解如实说明。

*讲的是方法，不构成投资建议。*

## 各章（约55分钟）

开场：席勒p星的逆向递推（价格的逐年波动是p星的8倍）；历史；本部分目标。第1章：货币时间价值、二分法求内部收益率（实验）、
有两个内部收益率的项目、戈登模型。第2章：股权久期(1+r)/(r−g)，以及成长股与价值股实测的利率敏感度（每个百分点−2.07%与−1.35%）。
第3章：运转起来的三张报表（会计模拟器与实验）、间接法现金流量表与杜邦分解。第4章：应计项目与斯隆的持续性检验（模拟面板、EDGAR、
多空组合）。第5章：XBRL与时点数据库（通用电气的双时间平面、卡夫亨氏的重述查询实验、申报滞后）。第6章：自由现金流、价值驱动公式、
两个三维曲面与蒙特卡洛。第7章：资本成本与市场隐含收益率（天平、实验、达摩达兰隐含风险溢价的重建）。第8章：剩余收益与市净率曲面。
第9章：估值倍数、CAPE、坎贝尔–席勒恒等式与拔河图。第10章：莫迪利亚尼–米勒、税盾、米勒1977、权衡理论与CFO调查。第11章：派息无关性的
证明、两家公司的模拟、净发行排序。第12章：作为看涨期权的股权、风险转移、债务悬置、实物期权。第13章：盈利公告与公告后漂移（事件研究实验；
大样本上2006年以后漂移消失）。第14章：会计信号与208个预测变量的衰减。第15章：并购套利（Capri案例与The Merger Fund的拐点回归）。
第16章：当报表说谎（安然、Wirecard、瑞幸、卡夫亨氏、贝尼什M分数与基础比率）。第17章：以估值为业的人。第18章：前沿与训练回放。
回顾、交易台问题与习题。

## 构建

见英文部分的命令。EDGAR要求每个客户端提供联系方式：首次在新机器上运行前，请设置环境变量`SEC_USER_AGENT`（姓名与邮箱）。
本次构建使用了缓存中八家公司的申报数据。

## 交易台问题与解答

1. **一家无负债公司以市价回购10%的股份。** 在没有税收和信息效应时，股价不变；只要盈利收益率E/P高于这笔现金原本的税后收益，
   每股收益就会上升。本章例子中每股收益从0.92升到1.00（+9%），市盈率从10.9降到10。每股收益提高并不等于价值提高；现实中回购还可能传递
   “股价便宜”的信号，并改变股东的税负。
2. **明年分红2美元、永续增长4%、股价50美元。** r = D₁/P + g = 2/50 + 4% = 8%。
3. **现金要约50，现价47，失败则跌到35，六个月，年利率4%。** p·50 + (1 − p)·35 = 47 × 1.02 = 47.94，所以p ≈ 86%；忽略利息为80%。
   风险中性概率包含交易风险溢价，真实的成交概率更高。
4. **净资产收益率12%、股权成本8%、账面价值永续增长4%：市净率？** P/B = 1 + (0.12 − 0.08)/(0.08 − 0.04) = 2。用股息的戈登公式验证：
   派息率 = 1 − g/ROE = 2/3，P/B = ROE × 派息率/(r − g) = 0.08/0.04 = 2。

## 习题与解答

1. **由戈登模型得市盈率。** P/E₁ = b/(r − g)。b = 0.5、市盈率30时r − g = 1.67%，r = 8%时g ≈ 6.3%。
2. **现金流折现。** 五年预测的现值合计459.8；终值2,169.7，现值1,476.6；合计1,936.5，终值占76%。在7%与3%下为2,816（+45%）。
3. **莫迪利亚尼–米勒。** 无税时r_E = 12%，加权平均资本成本8% = r_A；税率21%时r_E = 11.16%，加权平均资本成本7.16%。
   有税时政府替企业付了一部分利息，价值增加了税盾。
4. **默顿模型。** 股权35.75，债务64.25，债务收益率4.39%，信用利差2.39%，风险中性违约概率38%。
5. **重叠窗口。** 约13个独立的十年；把它们当作独立样本会把t统计量高估约√120 ≈ 11倍。第6部分推导修正方法与斯坦博偏差。
6. **两个内部收益率。** 100x² − 230x + 132 = 0，x = 1.1或1.2：内部收益率10%和20%。15%时净现值为+0.19 > 0，应当接受。
7. **坎贝尔–席勒。** b_r − b_d + ρφ = 0.05 + 0.03 + 0.912 = 0.992 ≈ 1（线性化误差）。长期斜率0.57与−0.34，差为0.91，其中收益率约占63%。
