# Opposing Forces: Booming Earnings vs. the Rising Cost of Money

A 37-minute, 15-chapter explainer of Jurrien Timmer's weekly market note
[*Opposing Forces*](https://www.linkedin.com/pulse/opposing-forces-week-10526-jurrien-timmer-anaac/)
(Fidelity Investments, week of October 5, 2026). The note argues that stock
prices have gone sideways because two forces cancel out: an earnings boom
pushing prices up, and a rising cost of capital pushing the multiple down.
The video builds the arithmetic behind that claim from scratch, walks through
the four forces Timmer says are lifting real yields, and **checks every claim
in the note against public data**. Every chart is drawn from real series,
frozen as of October 6, 2026. Schematics are labeled as schematics. Numbers
quoted only from the note (with no public data to check them) are attributed
to Timmer on screen.

*An explanation of one strategist's view, not investment advice.*

**Watch:** [`published/opposing_forces.mp4`](../../published/opposing_forces.mp4) (1080p, subtitles and chapters embedded).

<details><summary>Chapters</summary>

- `0:00` A boom that goes nowhere
- `2:07` Price = earnings x multiple
- `5:04` What sets the multiple?
- `8:57` Slowly, then all at once
- `12:32` Force 1: the cost of the debt
- `15:11` Force 2: who's left to buy?
- `16:59` Force 3: from savings glut to savings shortage
- `19:00` Force 4: the mortgage market
- `21:23` Is the economy running hot?
- `23:37` The Fed's dilemma
- `24:58` A stealth correction
- `26:55` The other side of the rope: earnings
- `30:16` Is this a bubble?
- `32:37` Where are we on the clock?
- `35:54` Recap

</details>

```bash
python -m videos.opposing_forces.fetch            # optional: re-download sources (~10 min) and rebuild data.json
python -m videos.opposing_forces.fetch --offline  # rebuild data.json from cached raw downloads
python tools/build.py opposing_forces -q l        # preview
python tools/build.py opposing_forces             # final 1080p30 + subtitles + chapters
python tools/export_script.py opposing_forces     # regenerate SCRIPT.md from the code
python tools/check_narration.py opposing_forces   # Whisper listen test of every narration line
python tools/publish.py opposing_forces           # GitHub-sized copy -> published/opposing_forces.mp4
```

`data.json` (about 0.3 MB) is committed, so the video renders offline exactly
as it was published. `fetch.py` needs network access only to refresh it.

## Outline

| # | Scene | What it establishes | Real data on screen |
|---|---|---|---|
| 0 | `Hook` | Earnings estimates up 9%, index flat for four months; only 1 in 4 stocks above its 50-day average while the index sits near a record. The tug of war. Roadmap, disclaimer. | S&P 500 daily (FRED); FactSet forward-EPS change; per-stock 50-day status of 500 members on Oct 2. |
| 1 | `PriceIdentity` | P = E × P/E as a rectangle (area = price). Growth rates multiply. Iso-price hyperbolas in the (E, P/E) plane; the 2023–24 leg was multiple-driven, 2025–26 earnings-driven. | Shiller trailing EPS and P/E, monthly; FactSet Q3 change (price +2.0%, forward EPS +9.3%, P/E 20.4 → 19.0). |
| 2 | `Discounting` | A share as discounted future profits; the geometric series P = D/(r − g); P/E = payout/(r − g); sensitivity of 1/(r − g); far-future dollars are rate-sensitive; the Fed Model; a check of the model against Q3. | 10-year 5.31%, TIPS 2.95% (FRED); forward P/E 19.7 (Timmer). |
| 3 | `BondMarket` | Yields up = prices down. The 40-year bond bull and its end. The 2023–26 triangle and the summer breakout. Nominal = real + breakeven: the whole rise is real. Yield = expected short rates + term premium. The four forces. | DGS10 since 1962 and weekly since 2022 (triangle drawn through the actual pivots); DFII10, T10YIE; NY Fed ACM term premium (0.885%, highest since April 2014). |
| 4 | `Debt` | Debt $23.2T → $40.25T. Interest at 4.0% of GDP, highest since 1998. The rollover conveyor (schematic) and the lagging average rate. The deficit feedback loop. Debt dynamics: Δb ≈ (r − g)b + primary deficit. | GFDEBTN; Debt to the Penny; interest/GDP since 1960; interest/debt vs DGS10; deficit % of GDP. |
| 5 | `Buyers` | Non-economic buyers; the Fed + foreign share of public debt, 69% (2014) → 45% (2026); QT; "not mom and pop". | FDHBFRBN, FDHBFIN, FYGFDPUN. |
| 6 | `Savings` | Loanable funds (schematic); the savings glut (Bernanke); reverse crowding out; the AI build-out. | Information-processing equipment + software investment: 5.05% of GDP vs the dot-com peak of 4.46% (A679RC1Q027SBEA). |
| 7 | `Convexity` | The prepayment option; positive vs negative convexity; duration extension (≈0.9 → 6.2 years in the model); convexity hedging loop; the 2026 mortgage swing. | Price/yield curves from a schematic pool model; MORTGAGE30US 5.98% (Feb) → 7.28% (Oct 1). |
| 8 | `RversusG` | Is growth hot? Real GDP 2.2%, CBO potential 2.2%, consensus 2.1–2.2%. r − g measured: real yield above potential growth for the first time since 2010. France as exhibit A. Timmer's verdict: fiscal risk. | GDPC1, GDPPOT, DFII10; French and German 10-year yields (OECD via FRED). |
| 9 | `FedDilemma` | 2025 cuts, the Sept 2026 hike, the 2-year at 4.84%; one rate, many constituencies (schematic meters). | DFEDTARU/L, DGS2, MORTGAGE30US. |
| 10 | `StealthCorrection` | Cap- vs equal-weighting (schematic weights); since June 30: cap +4.3%, equal −0.2%; breadth 25% / 42% on Oct 2; seasonality. | SPY, RSP (Nasdaq); breadth computed from 500 members; Shiller monthly averages since 1950. |
| 11 | `EarningsBoom` | Quarterly growth and the beats; record margins and guidance; four-year waves; first and second derivatives (schematic); "no top multiples for peak growth" (median P/E change by growth bucket, 1960–2026); the global picture per Timmer. | FactSet Earnings Insight (five issues); Shiller trailing EPS. |
| 12 | `Valuation` | Bubbles are multiple-driven; forward P/E 21.5 → 19.0 (FactSet), 19.7 / 17.3 (Timmer); CAPE 40.7 vs 44.2 in 2000; the Fed Model three ways. | FactSet; Shiller P/E, CAPE, excess CAPE yield; DGS10. |
| 13 | `Clock` | Timmer's clock (schematic), then drawn with real data: clockwise loops in 2016–18 and 2020–22; this cycle moving into 12–3. The two analogs and what followed. Secular bulls since 1900; "harvest those betas". | Shiller EPS growth vs the 12-month change in DFII10; SPY drawdowns (−17.6% in 2018, −24.8% in 2022, weekly closes); Shiller real price since 1900. |
| 14 | `Outro` | The tug of war, annotated; what would break the stalemate; credits. | |

## Color legend (consistent across every scene)

| Concept | Color |
|---|---|
| earnings, EPS, earnings growth, margins | green |
| the multiple (P/E), earnings yield | orange |
| price, the cap-weighted index | blue |
| the equal-weighted index, the average stock, breadth | pale gold |
| nominal yields, the discount rate r, cost of capital | red |
| real (TIPS) yields | pink |
| breakeven inflation | grey |
| term premium | lavender |
| the Fed's policy rate | teal |
| government debt, deficits, interest | brown |
| GDP growth g, potential growth | pale green |
| mortgages, mortgage-backed securities | gold |

## Data (`fetch.py` → `data.json`)

| Source | Series | Used in |
|---|---|---|
| FRED (St. Louis Fed) | DGS10, DFII10, T10YIE, DGS2, DFEDTARU/L, MORTGAGE30US, SP500, GFDEBTN, FYGFDPUN, FDHBFRBN, FDHBFIN, A091RC1Q027SBEA, GDP, GDPC1, GDPPOT, A679RC1Q027SBEA, FYFSGDA188S, IRLTLT01FRM156N, IRLTLT01DEM156N | 0, 2–10, 13 |
| New York Fed | ACM 10-year term premium (`acmPlot_data.csv`), monthly | 3 |
| Robert Shiller ([shillerdata.com](https://shillerdata.com/)) | `ie_data.xls`: monthly S&P 500 price (average of daily closes), trailing 12-month reported earnings (through June 2026), CPI, CAPE, excess CAPE yield | 1, 10–13 |
| U.S. Treasury, Fiscal Data | Debt to the Penny: $23.20T on Dec 31, 2019; $40.25T on Oct 5, 2026 (crossed $40T on Aug 18, 2026) | 4 |
| Nasdaq quote API | daily closes of SPY, RSP, and the 503 current S&P 500 members (500 retrieved; BF.B, PSKY, WBD missing) | 0, 10, 13 |
| FactSet *Earnings Insight* (John Butters) | issues of Nov 21, 2025; Feb 13, May 15, Aug 28 and Oct 2, 2026 (figures typed into `common.FACTSET`) | 1, 2, 11, 12 |

Scenes never download anything. Each number the narration states is asserted
against the data at render time (e.g. `assert abs(share - NOTE["above_50dma"]) < 1.5`
for the breadth grid), so a refreshed dataset that disagrees with the script
fails loudly instead of quietly contradicting the voice-over.

### Method notes

* **Breadth** (Ch. 0, 10): for each current member, today's close against the
  simple average of the last 50 (or 200) closes; the share is taken over members
  with enough history. Using today's members introduces a small survivorship bias.
  Result on Oct 2, 2026: 24.6% above the 50-day, 42.4% above the 200-day. Timmer
  says 25% and 46%. On Oct 6 the figures were 29.4% and 46.6%.
* **Equal vs cap weight** (Ch. 10): RSP and SPY ETF *prices*, not total returns.
* **"If the multiple had held"** (Ch. 0): the June 30 index close × 1.093
  (FactSet's forward-EPS change). FactSet puts the index's Q3 price change at
  +2.0%. FRED's closes give +2.8% for the same dates; FactSet's Sept 30 close
  (7,651.54) matches FRED, so the gap comes from the June 30 baseline.
* **Simple model check** (Ch. 2): P/E = 1/(r − g) with r − g = 5%, raised by the
  Q3 change in the 10-year yield (4.44% → 5.29%), predicts about −14.5%. FactSet's
  forward P/E fell 6.9%.
* **Triangle** (Ch. 3): the upper line runs through the weekly highs of Oct 22,
  2023 (4.93%) and Jan 12, 2025 (4.77%). The lower line runs through the lows of
  Sept 15, 2024 (3.66%) and Mar 1, 2026 (3.97%). The yield closed above the upper
  line in late July 2026.
* **Average rate on the debt** (Ch. 4): NIPA federal interest payments ÷ total
  public debt. It is a smooth proxy, not Treasury's published average interest rate.
* **Mortgage pool** (Ch. 7): 30-year, 6% level-payment loans. Annual prepayment
  speed follows an S-curve in the refinancing incentive, from 5% up to 50% CPR.
  The pool is discounted at the market rate. It is an illustration of the shape,
  not a valuation model.
* **r vs g** (Ch. 8): the 10-year TIPS yield against CBO real potential GDP
  growth (year over year). The real yield was above it in 2006–07 and 2008–10,
  and has been again since 2026. The government's *average* real borrowing cost
  is still lower.
* **Growth → P/E** (Ch. 11): all months since 1960, 12-month change in trailing
  reported EPS vs 12-month change in trailing P/E; medians by bucket (each bucket
  has more than 50 months). Part of the relationship is mechanical (prices lead
  earnings), and the video says so.
* **Fed Model** (Ch. 12): trailing = Shiller E/P − GS10 monthly, with the 2008.5–2010.5
  earnings collapse excluded from the "lowest since" comparison; "now" uses
  FactSet's trailing P/E (25.7) and the Oct 5 10-year yield. CAPE version =
  Shiller's own *excess CAPE yield*: 0.56% in Oct 2026, last lower in Feb 2002.
* **Clock** (Ch. 13): y = 12-month growth of Shiller trailing EPS, x = 12-month
  change in the monthly-average 10-year TIPS yield, both 3-month averages, with y
  clipped at 60% (the 2021 rebound peaked above 100%). The final point combines
  the Oct 2025 → Oct 2026 change in the real yield (+1.2) with Timmer's +30%.
* **Secular bulls** (Ch. 13): real price return, excluding dividends:
  1949.5–1966: 9.8%/yr; 1982.6–2000.7: 11.8%/yr; 2009.2–Oct 2026: 11.2%/yr;
  1900–2026: 2.7%/yr.
* **Seasonality** (Ch. 10): changes in Shiller's *monthly average* prices, so a
  bar labeled "Oct" compares October's average with September's. Measured with
  month-end closes instead, October is usually positive. The weak stretch runs
  from September into mid-October.

## Fact-check notes

Each claim in the note, against the data:

| Claim in the note | Check | Verdict |
|---|---|---|
| Price drifting sideways for 4 months | S&P 500: 7,580 (June 1) → 7,666 (Oct 2); range 7,267–7,819 | ✔ |
| Trailing EPS +30% y/y (later: +28%) | Shiller reported EPS, June 2026: +32.7% | ✔ (different EPS bases) |
| n12m EPS expected +20% | FactSet: CY2027 +15.8%; Q1'27 +19.1% | plausible (not directly checkable) |
| Margins at a new high of 17.4 | FactSet net margin record 17.0% (Q2 2026) | ✔ (different measures) |
| Risk-free 5.3% nominal, 2.9% real; 10-year 5.34%, real 2.91% | FRED Oct 5: 5.31%, 2.95% | ✔ |
| 25% above 50-day, 46% above 200-day | computed: 24.6% / 42.4% (Oct 2); 29.4% / 46.6% (Oct 6) | ✔ |
| Cap- vs equal-weight diverging | since June 30 (to Oct 6): SPY +4.3%, RSP −0.2% | ✔ |
| Real yield above real potential GDP | 2.95% vs CBO 2.2% | ✔ |
| Debt > $40T, up > $16T since COVID | $40.25T; +$17.05T since Dec 31, 2019 | ✔ |
| Debt service doubled to 4.0% of GDP since 2022 | NIPA interest/GDP: 2.5% (2022) → 4.0% (Q4 2025), 2.35% at the 2021 low | level ✔; "doubled" depends on the measure (the video says "about four percent", up from about 2⅓) |
| Term premium at a cycle high of 89 bp | ACM, Sept 2026: 0.885%, highest since April 2014 | ✔ |
| Fed eased in 2025 | cuts on Sept 18, Oct 30, Dec 11, 2025; hike on Sept 17, 2026 | ✔ |
| Bloomberg GDP survey 2026–28: 2.1–2.2% | proprietary; attributed on screen | — |
| Q3 could come in at 30–35% | FactSet estimate 29.5%; Q1 and Q2 beat their start-of-quarter estimates by 15 and 29 points | plausible |
| Trailing P/E down 10% y/y | Shiller trailing P/E June 2026 vs June 2025: −7% | close |
| Forward P/E 19.7 cap / 17.3 equal | FactSet forward P/E 19.0 | ✔ (different source) |
| 2017–18 and 2021–22 playbooks | real-data clock shows clockwise loops in both | ✔ |

The narration states the note's figures as Timmer's, and states the data's
figures as the data's. Where they differ (for example 19.7 vs 19.0 forward
P/E), both are given with their sources.
