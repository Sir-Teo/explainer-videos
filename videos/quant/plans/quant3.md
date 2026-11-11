# Part 3 · Value, Accounting and the Firm — expansion plan (29 → ~58.5 min, 12 → 20 chapters)

Planning only; no repository file was edited. Probes and quick computations are in
`/tmp/claude-0/-home-user-explainer-videos/e79d9910-3070-5b5d-804d-ed98af9b99fd/scratchpad/q3scripts/`. Numbers marked
**[run]** come from those probes, run on 2 Nov 2026 on the data the series caches (or on the sources named). The
compute items must reproduce them. Facts marked *(unverified)* could not be checked: the web-search budget ran out
partway through the sweep, so remaining checks used direct page fetches only. They are to be checked before they go on
screen, and dropped if they do not hold up.

## 1. Current state (`python tools/lecture_length.py quant3`: 28.7 min)

| # | Chapter (module) | Min | What it covers, and how deep |
|---|---|---|---|
| 0 | Hook (`s01_hook`) | 2.1 | Shiller (1981) p\* against the real S&P since 1871 (computed, 8× volatility; 40 years with moves above 20%). Objectives; the House chart. **Visual:** two lines drawn. No era/timeline beat. |
| 1 | Time value (`s02`) | 2.1 | PV, annuity, perpetuity, IRR (bond example); Gordon **derived** (3-step ladder); sensitivity curve 5/(r−0.03). Static plot. No computed experiment. |
| 2 | Three statements (`s03`) | 2.9 | Toy firm's year in three linked ledgers with flowing dots (the best visual in the part); accruals identity 200 = 100 + 100; Sloan in one sentence; the XBRL fact card. Schematic only. |
| 3 | DCF (`s04`) | 2.3 | FCF and WACC stated (not derived); five-year DCF bars (76% terminal); **3D value surface over (r, g)** with camera move (computed). |
| 4 | Multiples and CAPE (`s05`) | 2.2 | P/E = b/(r−g) derived (2 lines); EV/EBITDA stated; CAPE series since 1881; CAPE→10-yr return regression (slope −0.074, R² 0.32), overlapping-windows warning; forecast sealed. |
| 5 | MM (`s06`) | 2.4 | Prop I by home-made leverage (arbitrage table); Prop II plot; taxes and trade-off curve (illustrative). No derivation of the tax shield's PV. |
| 6 | Payout + equity as option (`s07`) | 2.7 | Irrelevance by stacked bars; EPS illusion (0.92→1.00); dividend yield since 1871 split at Rule 10b-18 (computed); Merton payoff picture. Three syllabus items squeezed into one chapter. |
| 7 | Signals (`s08`) | 2.9 | Ball–Brown/Bernard–Thomas **as a schematic**; five French decile long-shorts, pre/post publication (computed: 5.6% → 1.5%); McLean–Pontiff quoted; trial counter. |
| 8 | Merger arb (`s09`) | 2.1 | Spread → implied 80% (schematic); Mitchell–Pulvino quoted; AbbVie–Shire narrated. No data. |
| 9 | Crisis (`s10`) | 2.5 | Enron, Wirecard (narrated with dates and amounts); "what a quant takes". No measurement. |
| 10 | House (`s11`) | 1.4 | Bitemporal store on a constructed fact (200 → 150). EDGAR never loaded. |
| 11 | Outro (`s12`) | 3.1 | Recap, 3 desk questions, 5 problems, payoff links. |

Overall: about 4,700 words. Four chapters have a computed experiment: Shiller, DCF, CAPE and the signals. One is
3D (the DCF surface). There are no lab (code) moments and nothing is trained. There is no industry chapter, no frontier chapter and no
era beat, and the fundamentals store has never seen a real filing.

## 2. Audit

### (a) Syllabus items (SYLLABUS §6, Part 3)

| Item | Now | Verdict |
|---|---|---|
| 1 Time value, NPV, IRR, annuities, perpetuities, Gordon | s02 | **thin**: no multiple-IRR or NPV-vs-IRR conflict, no duration of equity, no data |
| 2 Three statements, accruals, what an analyst reads | s03 | covered for the toy year; **thin** on accruals (one sentence), no real statement, no ratio analysis (DuPont) |
| 3 XBRL, point-in-time fundamentals in the House | s03 card + s11 | **thin**: constructed example only; filing lags, restatements never measured |
| 4 DCF: FCF, WACC, terminal value, sensitivity | s04 | **thin**: FCF/WACC stated not derived, no EV→equity bridge, no value-driver formula, no implied cost of capital |
| 5 Multiples, CAPE, Shiller's data | s05 | covered; **missing** the Campbell–Shiller present-value identity and the return/dividend-growth decomposition (CLM ch. 7) |
| 6 MM by arbitrage; taxes, distress, trade-off | s06 | covered; tax shield PV and APV not derived; Miller (1977) absent; no survey evidence |
| 7 Payout; dividend irrelevance proof | s07 (shared) | **thin**: proof by picture; buyback/issuance returns not measured |
| 8 Equity as a call; real options | s07 (shared) | **thin**: payoff picture only; Myers (1977) overhang and risk-shifting absent |
| 9 Earnings announcements, surprises, PEAD | s08 (schematic) | **thin**: no data, no SUE definition, no event study |
| 10 Accruals, F-score, GP → factors | s08 | covered on French sorts; F-score and GP only named; Ohlson/Beneish/Dechow absent |
| 11 Mergers; merger arb as a short put | s09 | **thin**: no spread data, no regression |
| Crisis (Enron, Wirecard; "what the accruals said") | s10 | narrated, **not measured** |
| Firms (quantamental desks, merger-arb funds) | — | **missing** (no industry chapter) |
| Frontier | — | **missing** |

### (b) Textbook audit (TOCs from memory; chapter numbers to be checked against the editions in READING.md)

**Berk–DeMarzo, *Corporate Finance* (5th ed.)**: ch. 2 financial statement analysis → ch. 4–5; ch. 3 law of one price → ch. 2,
11; ch. 4 time value → ch. 2; ch. 5 interest rates, ch. 6 bonds → Part 18 (ch. 2 recalls); ch. 7 decision rules (NPV, IRR
pitfalls) → ch. 2; ch. 8 capital budgeting (FCF) → ch. 7; ch. 9 valuing stocks (DDM, total payout, multiples) → ch. 3, 10,
13; ch. 10–13 risk and return, CAPM, cost of capital, efficiency → ch. 8 (CAPM preview) and Parts 1, 23; ch. 14 MM perfect
markets → ch. 11; ch. 15 debt and taxes (incl. Miller 1977) → ch. 11; ch. 16 distress, agency, information (overhang,
asset substitution, pecking order) → ch. 11, 13; ch. 17 payout → ch. 12; ch. 18 valuation with leverage (WACC, APV, FTE)
→ ch. 8; ch. 19 financial modelling case → ch. 7 (DCF build); ch. 20–21 options → Part 10; ch. 22 real options → ch. 13;
ch. 23–24 raising capital → Part 2 (IPOs: one line in ch. 12, *missing otherwise*); ch. 25 leasing → ch. 18 (ASC 842)
and ch. 6; ch. 26–27 working capital, short-term planning → ch. 7 (ΔNWC) only, otherwise *not covered: a corporate
treasury topic outside a quant syllabus; say so in the README*; ch. 28 M&A → ch. 17; ch. 29 governance → ch. 19
(activism); ch. 30 risk management → Part 40; ch. 31 international → Part 22.

**Brealey–Myers–Allen (13th ed.)**: ch. 2–5 PV, bonds, stocks, NPV rules → ch. 2–3; ch. 6 NPV decisions → ch. 7; ch. 7–9
risk, CAPM, cost of capital → ch. 8, Part 23; ch. 10–12 project analysis, rents, agency → ch. 7 (value driver RONIC>WACC),
ch. 13; ch. 13 efficient markets → Part 1; ch. 14–15 financing overview, issuing → ch. 12; ch. 16 payout → ch. 12; ch. 17–18
debt policy → ch. 11; ch. 19 financing and valuation (APV) → ch. 8; ch. 20–22 options, real options → ch. 13, Part 10;
ch. 23 credit risk → Part 20; ch. 25 leasing → ch. 6/18; ch. 28 financial analysis (ratios, DuPont) → ch. 4; ch. 29–30
planning, working capital → *not covered (README)*; ch. 31–32 mergers, restructuring → ch. 17; ch. 33 governance → ch. 19.

**Damodaran, *Investment Valuation* (3rd ed.)**: ch. 2 approaches → ch. 7; ch. 3 statements → ch. 4; ch. 7 riskless rate and ERP
(implied ERP) → ch. 8; ch. 8 risk parameters → ch. 8, Part 23; ch. 9–10 earnings to cash flows → ch. 5, 7; ch. 11 growth
(g = reinvestment × ROC) → ch. 7; ch. 12 terminal value → ch. 7; ch. 13 DDM → ch. 2–3; ch. 14 FCFE → ch. 7; ch. 15 firm
valuation, WACC and APV → ch. 7–8; ch. 16 equity per share (bridge) → ch. 7; ch. 17–20 relative valuation (P/E, P/B,
EV multiples, sector multiples) → ch. 9–10; ch. 21 financial firms → *mention only*; ch. 22–24 negative earnings,
young, private firms → *not covered (README)*; ch. 25 acquisitions → ch. 17; ch. 28–30 real options, distressed equity
→ ch. 13, Part 20; ch. 31–32 value enhancement, EVA → ch. 9 (residual income); ch. 33–34 bonds, futures → Parts 18, 2.

**Koller–Goedhart–Wessels, *Valuation* (7th ed.)**: ch. 2–3 value creation, conservation of value → ch. 7 (RONIC), ch. 12
(buybacks); ch. 4–5 stock market performance, "the market is smarter" → ch. 10, 16; ch. 6–7 ROIC, growth → ch. 7;
ch. 8 frameworks (enterprise DCF, economic profit, APV) → ch. 7–9; ch. 9 reorganising statements (NOPAT, invested capital)
→ ch. 7; ch. 10 analysing performance → ch. 4; ch. 11 forecasting → ch. 7, 19 (frontier forecaster); ch. 12 continuing
value (value-driver formula) → ch. 7; ch. 13 cost of capital → ch. 8; ch. 14 EV to equity → ch. 7; ch. 15–16 results,
multiples → ch. 10; ch. 18–21 taxes, provisions, leases, pensions → ch. 7 (one card: "debt-like items"), *otherwise
README*; ch. 24 inflation → ch. 3 (duration pause question); ch. 30 M&A → ch. 17; ch. 32 capital structure and payout →
ch. 11–12; ch. 34–38 emerging markets, high-growth, cyclical, banks, flexibility → *README; flexibility → ch. 13*.

**Also on the spine for Part 3:** Bodie–Kane–Marcus ch. 18 (equity valuation: DDM, PVGO, P/E) → ch. 3, 10; ch. 19
(financial statement analysis, DuPont, quality of earnings) → ch. 4–5; CLM ch. 7 (present-value relations, Campbell–Shiller)
→ ch. 10 (**now missing**, the biggest textbook gap); Luenberger ch. 2–3 (cash-flow streams, IRR, annuities) → ch. 2.

### (c) Papers on READING.md's Part 3 list

| Paper | Now | Plan |
|---|---|---|
| Modigliani–Miller (1958) | on screen | ch. 11, derivation kept |
| Miller–Modigliani (1961) | on screen | ch. 12, proof by algebra added |
| Gordon–Shapiro (1956) | on screen (credit) | ch. 2 |
| Myers (1977) | **absent** | ch. 13: overhang worked example on screen |
| Ball–Brown (1968) | on screen (schematic) | ch. 14: their figure recreated, then our event study |
| Bernard–Thomas (1989) | on screen (schematic) | ch. 14: SUE deciles and the 60-day drift measured |
| Ohlson (1995) | **absent** | ch. 9: clean surplus → residual income derived |
| Sloan (1996) | on screen | ch. 5: persistence regression rerun on EDGAR |
| Piotroski (2000) | mentioned | ch. 15: the nine signals as a card, OSAP `PS` pre/post |
| Beneish (1999) | **absent** | ch. 18: M-score derived and run on the panel |
| Dechow–Ge–Larson–Sloan (2011) | **absent** | ch. 18: F-score (misstatement) named, with what it adds |
| Novy-Marx (2013) | mentioned | ch. 15: GP/A beside B/M, OSAP `GP` pre/post |
| Mitchell–Pulvino (2001) | on screen | ch. 17: their kink re-estimated on The Merger Fund |

**Add to READING.md Part 3** (each appears in the plan): Williams (1938) *The Theory of Investment Value*; Shiller (1981)
*AER*; Campbell–Shiller (1988) "The dividend-price ratio and expectations of future dividends and discount factors" *RFS*;
Cochrane (2008) "The dog that did not bark" *RFS*; Modigliani–Miller (1963) *AER*; Miller (1977) "Debt and taxes" *JF*;
Jensen–Meckling (1976) *JFE*; Merton (1974) *JF*; Foster–Olsen–Shevlin (1984) *TAR*; Ikenberry–Lakonishok–Vermaelen
(1995) *JFE*; Pontiff–Woodgate (2008) *JF*; Boudoukh–Michaely–Richardson–Roberts (2007) *JF*; Dechow–Sloan–Soliman (2004)
"Implied equity duration" *RAS*; Graham–Harvey (2001) *JFE*; Brav–Jiang–Partnoy–Thomas (2008) *JF*; Asness–Frazzini–Pedersen
(2019) *RAS*; McLean–Pontiff (2016) *JF*; Chen–Zimmermann (2022) *CFR*; Hou–van Dijk–Zhang (2012) *JAE* (cross-sectional
earnings model) *(verify)*; plus the frontier list in §4. Penman, *Financial Statement Analysis and Security Valuation*,
should join the spine as the residual-income textbook *(owner's call)*.

## 3. The proposed chapters (20 chapters, ~58.5 min)

Keys: **K** keep, **D** deepen, **N** new. *Lab* means a `code_block` (≤12 lines) of the House function, then run, with
output appearing live. *Sim* means a simulation that runs on screen. *Replay* means a ValueTracker scrub of checkpoints
beside the loss curve (pattern: `videos/ai/ai21/s12_reflow.py` `replay`/`measure`). The data functions to add to
`explainer/quant/data.py` are listed in §3.21. Research window: to Dec 2020. Hold-outs from 2021 are sealed, as now. The
2023–24 case files (Capri) are not backtests and do not touch the envelope.

**Note on the arithmetic.** The SYLLABUS standard says chapters of 4–6 min. The new 16–20-chapter rule at 50–60 min
implies about 3 min. The plan follows the newer rule: content chapters run 2.5–3.5 min, and each syllabus item gets one
or two of them.

### Ch. 0 · Hook: what is a share a claim on? (D, 2.5)
Goal: the puzzle (prices move too much) and the era. Beats: Shiller p\* (keep, but **sim**: p\* is built on screen by the
backward recursion $p^*_t=(p^*_{t+1}+D_t)/(1+r)$. A gold cursor walks from 2020 back to 1871, and each year's
dividend bar drops into the line). Then the timeline strip lights Pacioli 1494, Graham–Dodd 1934, Williams 1938,
MM 1958, Ball–Brown 1968, Ohlson 1995, XBRL 2009 and Shiller's Nobel 2013. Then the objectives and the House.
P&P: "If price is the best forecast of p\*, which line must be smoother?"

### Ch. 1 · Time value, IRR and the growing perpetuity (D, 3.0)
Goal: discounting as one operation; when IRR lies. Beats: PV, then annuity as a difference of two perpetuities, then IRR,
then a project whose cash flows (−100, +230, −132) have two IRRs (10% and 20%), then Gordon (keep the ladder).
Derivations: $\text{annuity}=\frac{C}{r}-\frac{C}{r}(1+r)^{-n}$ (a perpetuity now minus one starting at $n$);
$\text{NPV}(r)=-100+\frac{230}{1+r}-\frac{132}{(1+r)^2}=0\iff 100x^2-230x+132=0,\ x=1+r\in\{1.1,1.2\}$ (a quadratic in the
discount factor, so two roots); the Gordon ladder (keep). **Signature:** a conveyor of cash-flow bars recedes into
depth (a `ThreeDScene` with the camera low). Each bar shrinks by $(1+r)^{-t}$ as it moves back, and a `ValueTracker` on $r$
makes the far bars collapse while the near ones barely move. The stacked tower of PVs on the left is the NPV, live.
**Lab 1:** `valuation.irr` (bisection, ~8 lines). Run it on the bond, and the bracket [lo, hi] shrinks on a number line, one step a beat.
Then on the two-root project, where it returns one root and the NPV(r) curve beside it shows the second. Experiment: none (arithmetic). P&P: "NPV(r) for this project
crosses zero twice. At 15%, is it worth doing?" (yes: NPV > 0 between the roots).

### Ch. 2 · The duration of equity (N, 2.5)
Goal: a growing perpetuity is a long bond, and why stocks are not as rate-sensitive as Gordon says.
Derivation: $P=\frac{D_1}{r-g}\Rightarrow -\frac{\partial\ln P}{\partial r}=\frac{1}{r-g}$ (log-differentiate; modified duration);
Macaulay $D=\sum_t t\,w_t=\frac{1+r}{r-g}$ ($w_t$ the PV weights; differentiate the geometric series); at $r-g=3\%$:
33 years modified (Macaulay 36 at $r=8\%$). **Signature:** the PV-weight histogram over $t$ with a balance fulcrum at its mean (the duration). As $g\to r$ the
mass slides right and the fulcrum runs off toward infinity. Beside it, a 30-year bond's weights for scale.
**Experiment [run]:** monthly return of French's B/M deciles on the monthly change in the 10-year yield (Shiller `gs10`),
1963-07–2020-12: growth decile (Lo 10) −2.07% per point, value (Hi 10) −1.35% per point. Gordon at r−g = 3% predicts
−33%. Narration branches: the sign and ordering hold (growth is longer), the size is off by >10× because $g$ and the risk
premium move with the yield (inflation pass-through). Dechow–Sloan–Soliman's implied duration is about 15 years
*(verify)*. P&P: "Gordon says a one-point rise in yields should cut a growth stock by a third. The data say 2%. Why?"

### Ch. 3 · The three statements, running (D, 3.5)
Goal: the three statements are one double-entry machine, run over time. Beats: keep the toy year, then **sim**
`house.accounting.simulate(firm, years=5, seed)` drives the three ledgers quarter by quarter. Sales arrive as tokens. A
credit sale splits into revenue (income statement) and receivables (balance sheet). Collections move receivables to cash.
Capex moves cash to plant, depreciation moves plant to expense, and a green "assets = claims" check stays lit every
quarter. Then DuPont: $\frac{NI}{E}=\frac{NI}{S}\cdot\frac{S}{A}\cdot\frac{A}{E}$ (multiply and divide). Then what an
analyst reads (margins, turnover, leverage, cash conversion).
Derivation: $\Delta\text{Cash}=NI+\text{Dep}-\Delta AR-\text{Capex}-\text{Div}$ (indirect method), from
$A=L+E$ and clean surplus $\Delta E=NI-\text{Div}$ (differences of the identity).
**Lab 2:** `accounting.step(firm, q)` (≤12 lines: post the journal entries, then `assert assets == claims`). Run it on screen
for one quarter. The ledgers tick and the assert line flashes green.
Experiment: the simulator's 5 years. P&P: "Sales double on 90-day credit. Does cash go up or down this quarter?" (down).

### Ch. 4 · Accruals: where earnings and cash part (N, 2.5)
Goal: Sloan's mechanism, measured. Definition: balance-sheet accruals
$\text{ACC}=(\Delta CA-\Delta\text{Cash})-(\Delta CL-\Delta STD-\Delta TP)-\text{Dep}$, or from cash flows $NI-\text{CFO}$.
Derivation of the persistence test: $E_{t+1}=\alpha+\gamma_1 \text{CFO}_t+\gamma_2 \text{ACC}_t+\varepsilon$ and $\gamma_2<\gamma_1$
(accruals reverse, because a receivable either becomes cash or is written off). Sloan (1996) reports γ ≈ 0.77 for accruals
and 0.86 for cash *(verify Table 3)*. **Signature:** a cloud of firm-years as dots on the plane (CFO/A, ACC/A). The camera
tilts into 3D, $z=E_{t+1}/A$. Two regression planes appear, and the plane's slope is visibly flatter along the accrual axis.
Rotating so the viewer looks straight along the CFO axis shows it.
**Experiment:** EDGAR frames panel (`edgar_frames`, NetIncomeLoss, NetCashProvidedByUsedInOperatingActivities, Assets,
FY 2009–2020, all filers with both, about 3–4k firms a year). Pooled OLS with year effects and firm-clustered SE
(`econ.ols(se="cluster")`). Expected: γ₂ < γ₁ by about 0.05–0.15; narration branches on the gap and its t-stat. Then the accrual
decile spread from OSAP `Accruals` (in-sample 0.69%/month [run]; pre/post in ch. 15). P&P: "Two firms earn 10% of assets.
One collected it in cash, one booked it as receivables. Whose earnings will be higher next year?"

### Ch. 5 · XBRL and the point-in-time store (N, merges s11; 3.0)
Goal: a reported number has two dates. Beats: the XBRL fact card (keep). SEC phase-in: periods ending after 15 June 2009
for large accelerated filers with float above $5 bn, June 2010 for other large accelerated filers, June 2011 for the rest
(Release 33-9002). Then the 10-K deadline of 60/75/90 days by filer size. Then the restatement map, then the House rule.
**Signature:** the bitemporal plane. x is the fiscal period, y the filing date, and every filed value of one concept is a
dot above the diagonal $y=x$. A horizontal "as-of" line sweeps upward. For each column the store's answer is the highest
dot below the line, lit. Where a later dot exists (a restatement), the lit value jumps as the line passes it. The 3D
version, z = value, makes a restatement a visible step in a staircase.
**Lab 3:** `fundamentals.Store.asof` (keep the code, ≤12 lines) run live on **Kraft Heinz** NetIncomeLoss from companyfacts:
asked as of mid-2018 vs mid-2020, the 2016–17 values differ. The SEC found an expense-management scheme with
$208 m of improperly recognised cost savings restated in June 2019 and a $62 m penalty
(https://www.sec.gov/news/press-release/2021-174).
**Experiment [run, 8-firm probe]:** of annual 10-K values later shown differently in a later 10-K (restatements *and*
recasts): GE Revenues 16/19 periods and Assets 14/18; Exxon Revenues 5/17; Kraft Heinz NetIncomeLoss 2/12; Apple and
Microsoft NetIncomeLoss 3/19 and 2/19. Median filing lags: Microsoft 30 days, Apple 34, Exxon 56, Capri 60. The full item uses
about 100 large firms (`edgar_companyfacts`) and reports the share of facts changed by concept and the lag distribution
against the 60/75/90-day rules. P&P: "A backtest uses December's earnings on 1 January. How many days of the future has it
read?" (the median lag).

### Ch. 6 · Free cash flow and the DCF surface (D, 3.5)
Goal: build the firm-value machine from the statements; where value comes from. Derivations:
$\text{FCFF}=\text{EBIT}(1-t)+\text{Dep}-\text{Capex}-\Delta\text{NWC}$ (cash from ops before financing, read off ch. 3's
ledgers); $\text{FCFF}=\text{NOPAT}(1-\text{IR})$ with reinvestment rate IR; $g=\text{IR}\cdot\text{RONIC}$ (growth must be
paid for); hence the value-driver formula $\text{TV}=\frac{\text{NOPAT}_{T+1}(1-g/\text{RONIC})}{\text{WACC}-g}$ (substitute
IR = g/RONIC into Gordon); $\partial \text{TV}/\partial g>0\iff \text{RONIC}>\text{WACC}$ (differentiate). The bridge: equity = EV − net debt −
minorities − preferred − debt-like items (leases, pensions) + non-operating assets.
**Signature:** keep the (r, g) surface, then the camera swings to a **second 3D surface over (g, RONIC)** at fixed WACC 8%.
A ridge line at RONIC = WACC is the hinge. On one side the surface rises with g, on the other it falls, and a ball rolled
along g goes uphill or downhill depending on its side. "Growth is worth something only above the cost of capital."
**Sim:** Monte Carlo DCF. 20,000 draws of (r ~ U[6,10]%, g ~ U[0,3]%, margin) fall as dots onto the surface and pile into
a histogram of firm values on the side wall; the 5–95% band is printed. Experiment (`dcf_mc`): expected band roughly 0.6–2.0× the base value.
P&P: "A firm earns exactly its cost of capital on new investment. What does faster growth add?" (nothing).

### Ch. 7 · The cost of capital the market implies (N, 2.5)
Goal: WACC, APV, and turning a price into a discount rate. Derivations: WACC (keep); levering beta
$\beta_E=\beta_A+(\beta_A-\beta_D)\frac{D}{E}$ (MM II applied to betas, ch. 11 forward link); implied cost of capital: solve
$P_0=\sum_{t=1}^{5}\frac{CF_0(1+g)^t}{(1+r)^t}+\frac{CF_5(1+g_L)}{(r-g_L)(1+r)^5}$ for $r$, ERP = r − y₁₀ (Damodaran's two-stage
model; the root is unique because the right side is monotone in $r$).
**Lab 4:** `valuation.implied_rate(price, cf0, g, g_long)` (bisection reusing `irr`). Run it live on the S&P 500 at end-2008 and
end-2020 using Damodaran's inputs. The bracket shrinks and the ERP appears.
**Experiment** (`erp`, `damodaran("histimpl")`): rebuild Damodaran's FCFE implied ERP 1960–2020 and plot it against his
published column. His values [read from histimpl.xls, 2 Nov 2026]: 1974 5.59%, 1981 5.73%, 1999 2.05%, 2008 6.43%,
2020 4.72% (2022 5.94%, 2025 4.23%: post-window, shown as published, not used). Expected: our rebuild within about 0.2 pt of his.
**Signature:** a balance beam. Left pan: the index level as a gold block. Right pan: the stack of discounted cash-flow
bars. A dial on r turns until the beam levels, and the dial's reading is the market's implied return, redone for each
year as the 1960–2020 line draws itself. P&P: "In December 1999 the implied premium was about 2%. What did that
forecast for the next decade?"

### Ch. 8 · Residual income and price-to-book (N, 3.0)
Goal: Ohlson (1995). Value = book plus the PV of abnormal earnings. Derivation (each step on screen):
$P_0=\sum_{t\ge1}\frac{D_t}{(1+r)^t}$ (DDM); clean surplus $D_t=E_t-(B_t-B_{t-1})$ (all equity changes pass through earnings
or payout); substitute and telescope: $\sum\frac{E_t-B_t+B_{t-1}}{(1+r)^t}=B_0+\sum\frac{E_t-rB_{t-1}}{(1+r)^t}-\lim\frac{B_T}{(1+r)^T}$
(add and subtract $rB_{t-1}$; the book terms cancel pairwise); transversality kills the limit; so
$P_0=B_0+\sum_t\frac{(\text{ROE}_t-r)B_{t-1}}{(1+r)^t}$. Steady state: $\frac{P}{B}=1+\frac{\text{ROE}-r}{r-g}$, and with payout
$\frac{P}{B}=\frac{\text{ROE}\cdot(1-g/\text{ROE})}{r-g}$ (Gordon on dividends = ROE·B·payout), the formula AQR's QMJ starts from.
**Signature:** a 3D surface of P/B over (ROE, g) at r = 8%. The plane P/B = 1 is drawn in grey, and the surface crosses
it exactly along the line ROE = r for every g (the camera flies along that seam). Then a firm's own bars: book as a
base block, residual-income bars above it (negative when ROE < r) shrinking with discounting. Experiment
(`ri`): the identity checked numerically on the ch. 3 simulator (DDM value = RI value to 1e-9: an `assert`). The EDGAR panel
then supplies the cross-section of P/B vs ROE for FY2019. **This needs market caps:** `dei:EntityPublicFloat` from
companyfacts as a proxy, labelled. Expected: positive slope, wide dispersion. P&P: "A firm's ROE equals its cost of
equity. What is its P/B, whatever its growth?" (1).

### Ch. 9 · Multiples, the CAPE, and what the dividend yield predicts (D, 3.5)
Goal: multiples are compressed DCFs, and the CLM ch. 7 identity. Beats: P/E = b/(r−g) (keep). PVGO:
$P=\frac{E_1}{r}+\text{PVGO}$ (value of no-growth earnings plus growth options). EV/EBITDA (keep). The CAPE series and the
regression (keep, trimmed). Then Campbell–Shiller.
Derivation: $r_{t+1}=\ln\frac{P_{t+1}+D_{t+1}}{P_t}\approx\kappa+\rho\,pd_{t+1}+\Delta d_{t+1}-pd_t$ (first-order Taylor in
$pd$ around its mean, $\rho=1/(1+e^{\overline{dp}})$); iterate forward: $pd_t=\text{const}+\sum_j\rho^{j-1}(\Delta
d_{t+j}-r_{t+j})$ (no bubbles); multiply by $dp_t$ and take expectations:
$\text{var}(dp)=\text{cov}(dp,\sum\rho^{j-1}r_{t+j})-\text{cov}(dp,\sum\rho^{j-1}\Delta d_{t+j})$; with AR(1) $dp$:
$b_r^{lr}-b_d^{lr}=1$ where $b^{lr}=b/(1-\rho\phi)$ (Cochrane 2008).
**Signature:** a tug-of-war. The dividend yield is a bar whose movements must be "paid for" by future returns (red rope) or by
future dividend growth (green rope). Each rope's pull is its long-run coefficient, and the two always sum to 1. The
sample slider moves from 1871–1945 to 1946–2020 and the weight shifts from green to red.
**Experiment [run]** (`campbell_shiller`, Shiller annual, real, Jan-to-Jan): full 1871–2020, $b_r=0.049$ (NW t 1.3),
$b_d=-0.029$, $\phi=0.956$, $\rho=0.961$; identity check $b_r-b_d=0.078$ vs $1-\rho\phi=0.081$. Long-run shares: returns
0.60, dividends −0.36. 1871–1945: returns 0.36, dividend growth −0.70 (dividends did the work). 1946–2020: returns 0.88,
dividends 0.00 (the dog that did not bark). Add the Stambaugh-bias bootstrap (`econ.simulate_predictive`) for the short-horizon
t. P&P: "After 1945, when the dividend yield was high, which came next: higher returns or slower dividend growth?"

### Ch. 10 · Modigliani–Miller, with taxes and distress (D, 3.5)
Goal: the arbitrage proof (keep), then what breaks it. Derivations: Prop I table (keep); Prop II (keep);
tax shield: $\text{PV}=\sum_t\frac{T_c r_D D}{(1+r_D)^t}=T_cD$ (permanent debt, shield as risky as the debt), so $V_L=V_U+T_cD$;
$r_E=r_A+(r_A-r_D)(1-T_c)\frac{D}{E}$ (value balance with the shield); APV $=V_U+\text{PV(shield)}-\text{PV(distress)}$;
Miller (1977): $T^*=1-\frac{(1-T_c)(1-T_E)}{1-T_D}$ (the personal taxes on interest and on equity income).
**Signature:** the pie that cannot grow. A circle of fixed area X is cut into debt and equity wedges, and re-slicing
never changes the area (Prop I). Then a grey "government" wedge appears. Debt shrinks it, which enlarges the investors'
part, and a red "distress" ring grows around the rim as D rises. The investors' area peaks and then falls: the trade-off
curve is read off the animation. Experiment: Graham–Harvey survey card (JACF 2002 / JFE 2001, 392 CFOs). 44.9% call the
tax advantage of debt important, 21.4% distress costs, 57.1% credit ratings, 59.4% financial flexibility
(https://people.duke.edu/~charvey/Teaching/CDROM_BA453_2003/Other_Harvey_Papers/W62_How_do_CFOs.pdf). Narration: CFOs act
more on flexibility and ratings than on the trade-off's two forces. P&P: "With 21% tax and permanent debt of 100, how
much value does the debt add, and who loses it?" (21, from the government).

### Ch. 11 · Payout: dividends, buybacks and issuance (D, split from s07; 2.5)
Goal: MM (1961) proved, then what payout signals in data. Derivation: $V_t=\frac{1}{1+r}\left[n_tD_{t+1}+n_{t+1}P_{t+1}-m_{t+1}P_{t+1}\right]$
(new shares $m$ sold at $P_{t+1}$); funds identity $n_tD_{t+1}=X_{t+1}-I_{t+1}+m_{t+1}P_{t+1}$; substitute: $D$ cancels,
$V_t=\frac{X_{t+1}-I_{t+1}+V_{t+1}}{1+r}$ (value depends on investment, not payout). Keep the stacked bars and the EPS illusion.
Keep the dividend yield since 1871 split at Rule 10b-18.
**Signature:** two firms run side by side by the simulator, one paying dividends and one buying back. A shareholder's
wealth (shares × price + cash received) is drawn as one gold bar per firm, and the bars stay equal while price, EPS and
share count diverge on the ledgers.
**Experiment [run]** (`issuance`, French `Portfolios_Formed_on_NI`, value-weighted, 1963-07–2020): net repurchasers
(NI < 0) 13.35%/yr vs top-decile issuers 6.99%/yr. Then OSAP `NetPayoutYield` (Boudoukh et al. 2007) and `ShareIss1Y`
(Pontiff–Woodgate 2008) long-shorts [run, monthly in-sample 0.88% and 0.71%]. Narration: irrelevance holds for the
mechanics, but managers time issues; the signal is information, not the payout. P&P: the existing buyback desk question.

### Ch. 12 · Equity as a call: overhang, risk-shifting, real options (D, split from s07; 3.0)
Goal: Merton (1974) and the agency costs it predicts. Derivations: $E=A\,N(d_1)-Fe^{-rT}N(d_2)$ (a call on assets; priced in
Part 10); $D=Fe^{-rT}-\text{Put}(A,F)$ (put–call parity); $\partial E/\partial\sigma=\text{vega}>0$ (risk-shifting); Myers
overhang worked example: assets 100 (or 0), debt F = 80, project costs 10 paid by equity and returns 15. Equity gains only the
part not captured by the lenders, so a positive-NPV project is refused (numbers from `valuation.merton_equity`).
**Signature (3D, two inputs):** the equity-value surface over (A, σ). A firm sits as a ball on the surface. "Gamble"
moves it along σ and the ball rises (owners gain) while the debt surface, drawn below in DEBT colour, sinks by the same
amount: the total is conserved. The camera orbits to show the two surfaces as mirror images about the plane $A$.
Real option: the option to delay an investment drawn as the call's hockey stick over project value, so NPV < option value.
Experiment: `merton` grid (no data); one real-firm illustration is deferred to Part 20. P&P: "Near default, the owners can
double the firm's volatility at no cost. Do they? Who pays?"

### Ch. 13 · Earnings announcements and the drift (N, from the s08 schematic; 3.5)
Goal: Ball–Brown, then Bernard–Thomas measured from public filings. Definitions: seasonal random walk
$\text{SUE}_{iq}=\frac{\text{EPS}_{iq}-\text{EPS}_{i,q-4}}{\sigma_{i}(\text{EPS}_{q-j}-\text{EPS}_{q-4-j})_{j=1..8}}$;
$\text{CAR}_i(0,\tau)=\sum_{s=0}^{\tau}(r_{i,s}-r_{m,s})$ (event time; day 0 = 8-K item 2.02 acceptance, +1 if after 16:00).
**Sim:** the event-study clock. Each announcement drops a short path, aligned on day 0, into one of five SUE-quintile lanes.
The lane means draw themselves as the paths pile up (thousands of thin strokes, then the five fat means). After day 0
the top and bottom lanes keep diverging.
**Lab 5:** `events.car(returns, market, day0, window)` (≤10 lines), run on one Apple announcement (curve appears), then on all.
**Experiment** (`pead`): 8-K 2.02 dates from `edgar_submissions`, quarterly diluted EPS first-reported from companyfacts,
Yahoo daily closes (`yahoo_daily`) minus SPY, 2010–2020, about 100 current large caps (**survivorship labelled on screen**).
Expected: day-0 jump ordered by SUE; post-day-1 to +60 drift Q5−Q1 about 0–2% (small for large caps, after 2010). The
narration branches: if the drift is near zero, say so and cite Martineau (2022) "Rest in peace post-earnings announcement
drift" *CFR* *(unverified)*. Then the long history: OSAP `EarningsSurprise` [run]: 1.13%/month in-sample (1974–81),
0.38% after 1984, through 2020. P&P: "A firm beats by 3σ and the stock jumps 5%. Buy at the next open?"

### Ch. 14 · Accounting signals that became factors, and decayed (D, 3.5)
Goal: from Sloan, Piotroski and Novy-Marx to McLean–Pontiff, at scale. Beats: the F-score card (nine binary tests:
ROA > 0, CFO > 0, ΔROA > 0, CFO > ROA, Δleverage < 0, Δcurrent ratio > 0, no issuance, Δmargin > 0, Δturnover > 0; Piotroski:
within high-B/M stocks high-minus-low F-score about 23%/yr *(verify)*). GP/A beside B/M (Novy-Marx). Then the keep chart (five French
sorts, pre/post). Then all of them.
**Signature:** 99 accounting predictors as 99 small bars arranged on a timeline by publication year, each split into
in-sample / out-of-sample-before-publication / after-publication segments. The camera pulls back, the bars collapse
into three averages, and the post-publication bar settles at about 40% of the in-sample one.
**Experiment [run]** (`osap`, Chen–Zimmermann release 2024.10 `PredictorLSretWide`, original-paper portfolios, through
2020): all 208 predictors with ≥24 months each way: 0.69 → 0.43 (OOS pre-publication) → 0.26 %/month after publication
(×0.61, ×0.38). The 99 accounting ones: 0.58 → 0.45 → 0.22 (×0.78, ×0.38). McLean–Pontiff (2016): about −26% and −58%
(their 97). Examples: Accruals 0.69 → 0.14; PS (F-score) 0.94 → 0.98 after 2000; GP 0.30 → 0.62 after 2013. Block-bootstrap the decay
ratio (2,000 draws) for its band. Seal OSAP months from 2021. Trial counter: +208 looked at, registered as one meta-test.
P&P: "Which would you rather trade: a signal with a t of 6 published in 1990, or a t of 3 published last year?"

### Ch. 15 · Merger arbitrage (D, 3.5)
Goal: the spread is a probability, and the strategy is a short put, from data. Derivation: under Q,
$P_t=e^{-r\tau}[pO+(1-p)B]\Rightarrow p=\frac{P_te^{r\tau}-B}{O-B}$ (the price is the discounted expected payoff), with
the caveat that p is a risk-neutral, premium-laden probability.
**Signature (case file):** Capri Holdings (CPRI) under Tapestry's $57 cash offer. The price path draws itself week by week
from Yahoo; a dashed line at 57; the fallback B = $35.51 (last pre-deal weekly close [run]); a second panel draws the
implied p live. The deal was announced 10 Aug 2023 (EV about $8.5 bn, 59% premium to the 30-day VWAP:
https://www.businesswire.com/news/home/20230809944810/en/). The FTC sued in April 2024
(https://www.cnbc.com/2024/04/22/ftc-sues-to-block-tapestry-acquisition-of-capri-holdings.html). SDNY granted the
preliminary injunction on 24 Oct 2024 (Judge Rochon), and the merger agreement was terminated on 13–14 Nov 2024, per
Capri's 10-K (https://www.sec.gov/Archives/edgar/data/1530721/000153072125000052/cpri-20250329.htm). The weekly close
went 52.0 (Aug 2023) → 45.3 (Mar 2024) → 35.5 (after the suit) → 42.98 (mid-Oct 2024) → 21.26 (week of the ruling)
[run], *below* the pre-deal price.
**Experiment [run]** (`merger`, Yahoo monthly adjusted MERFX vs ^GSPC, 1989-01–2020-12, 383 months): piecewise OLS with a kink at a
−4% market month. β = 0.11 above the kink and 0.26 below (+0.14). Mean 5.2%/yr, vol 5.1%. Worst month −7.6% (S&P −5.1%).
Bootstrap the kink coefficient's band. Replay: none (OLS), but the fitted hinge line pivots into place over the scatter.
Keep the Mitchell–Pulvino card (4,750 deals 1963–98, about 4%/yr excess after costs). P&P: the existing desk question (86%).

### Ch. 16 · When the statements lie (D, 3.0, the crisis file)
Goal: the crisis measured where it can be, and the forensic models. Keep the Enron and Wirecard beats (facts already checked in
PROGRESS.md), shortened. Add Luckin Coffee: more than $300 m of retail sales fabricated from April 2019 to January 2020, and a $180 m penalty
(SEC 16 Dec 2020, https://www.sec.gov/news/press-release/2020-319). Add Kraft Heinz from ch. 5.
Derivation: Beneish (1999) $M=-4.84+0.920\,\text{DSRI}+0.528\,\text{GMI}+0.404\,\text{AQI}+0.892\,\text{SGI}+0.115\,\text{DEPI}-0.172\,\text{SGAI}+4.679\,\text{TATA}-0.327\,\text{LVGI}$
(a probit on 74 manipulators vs controls), with each ratio defined on a card and threshold −1.78 *(verify coefficients and
threshold against the paper)*. Dechow et al. (2011) F-score as the AAER-trained logistic successor (named only).
**Signature:** a "lie detector" dial for each firm-year. The eight ratio needles swing in from the XBRL values and the M-score
needle sums them. The panel's distribution is a histogram, with Kraft Heinz FY2016–17 *as first reported* dropped onto it as a
marked dot. Then the *restated* values move the dot. **Experiment** (`mscore`, EDGAR frames panel FY2010–2020): the
distribution, with the share above −1.78 (expected 10–20%: the score's false-positive problem, said plainly) and where the
named cases sit. Labelled "a screen, not a test: no fraud labels". P&P: "The screen flags 15% of firms. If 1% commit fraud
and it catches half, what share of flags are frauds?" (about 3%: base rates).

### Ch. 17 · Industry: who values firms for a living (N, 3.5)
Each beat is a `firm_card` with its source line on screen.
1. **Corporate finance practice.** 392 CFOs: 74.9% always or almost always use NPV and 75.7% IRR. Earnings multiples are used by 38.9%
   and real options by 26.6% (Graham–Harvey, JFE 2001; JACF 2002, URL above). CAPM use is about 73.5% *(unverified: JFE table)*.
2. **Banks' valuation groups in court.** *Dell* appraisal: the MBO paid $13.75. The Court of Chancery ran its own DCF and found
   $17.62 (31 May 2016); the petitioners' expert had said $28.61, and the experts' DCFs differed by 126%
   (https://www.potteranderson.com/insights/cases/In-re-Appraisal-of-Dell-May-31-2016). The Delaware Supreme Court
   reversed on 14 Dec 2017 and told the court to weigh market price and deal price
   (https://www.ropesgray.com/newsroom/alerts/2017/12/Delaware-Supreme-Court-Reverses-Court-of-Chancerys-Dell-Appraisal-Decision).
   *Rural/Metro*: RBC Capital Markets was held liable for aiding and abetting the board's breach. The court found
   conflicts (it sought buy-side financing roles) and a "flawed valuation analysis" delivered just before the board's vote.
   $75.8 m, affirmed on 30 Nov 2015 (https://corpgov.law.harvard.edu/2015/12/04/ruralmetro-decision-aiding-and-abetting-liability/).
   The lesson for the DCF surface of ch. 6: whoever picks (r, g) picks the answer.
3. **Rating agencies.** S&P's six financial-risk categories, from minimal to highly leveraged, are driven by cash-flow and
   leverage ratios. The 2009 criteria table puts "minimal" at FFO/debt > 60% and debt/EBITDA < 1.5×
   (https://www.maalot.co.il/Publications/MT20240214173645.PDF for the category names). The other cut-offs are *(unverified)*. The
   Merton-based EDF (Moody's KMV) is deferred to Part 20.
4. **Activists.** A 13D filing earns about 7–8% abnormal return in (−20, +20) days with no reversal (Brav–Jiang–Partnoy–Thomas, JF 2008,
   https://law.duke.edu/sites/default/files/centers/gfmc/session_3/2_brav_et_al-hedge_fund_activism-2008.pdf). The SEC
   cut the 13D deadline from 10 days to 5 business days on 10 Oct 2023
   (https://corpgov.law.harvard.edu/2023/10/24/sec-adopts-updates-to-schedule-13d-and-13g-reporting).
5. **Quant equity on fundamentals.** AQR's Quality-minus-Junk (Asness–Frazzini–Pedersen, RAS 24(1) 2019) starts from ch. 8's
   P/B formula and buys profitable, growing, safe firms. Open Source Asset Pricing publishes 200+ predictors' code and data
   (releases 2024.10–2026.10 on Hugging Face: https://huggingface.co/datasets/OpenSourceAP/CrossSection). Merger-arb
   funds: The Merger Fund's record is ch. 15's data.
6. **Standard setters and regulators.** Leases: the SEC staff's 2005 report estimated about $1.25 tn of off-balance-sheet
   operating-lease commitments (https://www.cooley.com/news/insight/2005/sec-report-on-offbalance-sheet-arrangements).
   ASU 2016-02 put them on the balance sheet for public companies from fiscal years starting after 15 Dec 2018
   (https://dart.deloitte.com/USDART/home/codification/broad-transactions/asc842-10/roadmap-leasing/chapter-1-overview/1-2-overview).
   XBRL (33-9002) and the 60/75/90-day deadlines are in ch. 5. Enforcement: Luckin and Kraft Heinz (ch. 16).
Hands-on: the lease beat runs the bridge from ch. 6 live, moving a lease liability from the footnote to net debt to show EV/EBITDA
and leverage change while equity value does not.

### Ch. 18 · Frontier: machines reading the statements (N, 3.0)
1. **Man vs machine earnings forecasts.** van Binsbergen, Han, Lopez-Lira (2023) "Man versus machine learning: the term
   structure of earnings expectations and conditional biases", *RFS* 36(6) 2361–96
   (https://www.nber.org/papers/w27843). Their findings: an ML benchmark beats linear models out of sample, analysts are biased
   upward, and the bias predicts returns. Cao, Jiang, Wang, Yang (2024) *JFE* "From man vs. machine to man + machine" *(verify;
   listed in READING Part 28)*.
2. **LLMs on statements, and a cautionary tale.** Kim, Muhn, Nikolaev (2024) "Financial statement analysis with large
   language models", arXiv 2407.17866, reported that GPT-4 beat analysts at predicting the direction of earnings. On 20 Feb 2025 the authors **withdrew**
   it after "a co-author identified inconsistencies in the data and analyses"
   (https://arxiv.org/abs/2407.17866v3). The same authors' "Bloated disclosures" (arXiv 2306.10224) is also withdrawn;
   a co-author's replication did not support it (https://arxiv.org/abs/2306.10224). FinanceBench (Islam et al. 2023,
   arXiv 2311.11944, https://arxiv.org/abs/2311.11944): GPT-4-Turbo with retrieval answered 81% of 150 questions about filings
   wrongly or not at all.
3. **Replication at scale.** Jensen, Kelly, Pedersen (2023) "Is there a replication crisis in finance?" *JF* 78(5)
   (https://www.nber.org/papers/w28432): most factors replicate, in 13 themes across 93 countries, the counterweight to ch. 14.
   Chen–Zimmermann's open data (above).
4. **Duration and intangibles.** Gormsen–Lazarus (2023) "Duration-driven returns" *JF* *(verify)*; Eisfeldt–Kim–Papanikolaou
   (2022) "Intangible value" *CFR* *(verify)*: capitalising SG&A changes what "book" means in ch. 8.
**Replay (the trained model of the part):** `forecaster` predicts next-year earnings/assets from 20 XBRL items (frames
panel, train FY2010–2016, validate 2017–2018, test 2019–2020). Models at equal budget: a random walk ($E_{t+1}=E_t$),
pooled OLS (Hou–van Dijk–Zhang style), ridge on splines (`econ.ridge_fit_predict`), and a 2-layer MLP (torch, 5 seeds). The
replay scrubs 30 checkpoints: the validation loss curve, beside a scatter of predicted vs realised test values
that tightens, with spread bands across seeds and the baselines drawn as flat lines. The narration branches on the result: if the MLP does not beat
OLS by more than the seed spread, say so (the random walk is famously hard to beat for levels; the gain, if any, is in
changes and direction). P&P: "Which will be hardest to beat: the random walk, the analyst, or the linear model?"

### Ch. 19 · Recap, the House, desk questions, problems (D, 2.0)
Keep, rewritten: the recap in 10 lines. The House card: the data desk now has `fundamentals` (real EDGAR, bitemporal),
`accounting` (simulator), `valuation` (+RI, implied rate, APV, value driver) and `events` (CAR). Rule 4 is unchanged. Desk
questions: keep the three and add "A firm's ROE = 12%, r = 8%, g = 4%. P/B?" (2). Problems: keep 5, add (6) the two-IRR
project and (7) the Campbell–Shiller identity with $\rho = 0.96$. Payoff links: Part 6 (Stambaugh, overlapping), Part 10
(the call), Part 20 (default), Parts 23–25, 28.

### 3.20 Minutes

| Ch | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | **Total** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| min | 2.5 | 3.0 | 2.5 | 3.5 | 2.5 | 3.0 | 3.5 | 2.5 | 3.0 | 3.5 | 3.5 | 2.5 | 3.0 | 3.5 | 3.5 | 3.5 | 3.0 | 3.5 | 3.0 | 2.0 | **58.5** |

At the current ~170 words/min this is about 9,500 words of narration (now about 4,700). Labs: 5 (ch. 1, 3, 5, 7, 13). Sims: 6
(ch. 0, 1, 3, 6, 11, 13). Replays: 1 trained model (ch. 18), plus the bootstrap bands of ch. 9, 14 and 15. 3D: ch. 1, 4, 5, 6, 8,
12. Manifest titles follow the chapter names above. Keep the existing module names where the chapter is kept, because
renaming a module invalidates the narration cache (CLAUDE.md).

### 3.21 Data, House code, compute budget

**`explainer/quant/data.py` additions** (cached and checksummed like the rest):
- `edgar_companyfacts(cik, concepts)`: data.sec.gov, keeps only the listed concepts (a 4–8 MB file becomes about 100 kB). The
  User-Agent comes from env `SEC_USER_AGENT` (SEC fair-access policy asks for a contact; the README tells the owner to set
  it). Probed working on 2 Nov 2026 (www.sec.gov, unlike data.sec.gov, returned 403 to a generic agent).
- `edgar_frames(concept, unit, period)`: e.g. `CY2019`, about 6,000 filers a request. The value is *as last reported*, so
  label it and use companyfacts for anything point-in-time.
- `edgar_submissions(cik)`: forms, filingDate, acceptanceDateTime, items (8-K "2.02" verified on Apple).
- `damodaran(name)`: `histimpl.xls` (and `wacc.xls`), via xlrd (verified to load).
- `osap_ls(release="2024.10")`: Hugging Face `PredictorLSretWide.parquet` plus `SignalDoc.csv`. pyarrow is in the venv;
  pandas is not needed.
- `ken_french_sorts("NI")` works already (new file only). `yahoo_daily` for CPRI, MERFX, ^GSPC and SPY works already. Delisted
  tickers (ATVI, TWTR, SHPG) return 404 on Yahoo, hence Capri.

**House** (`explainer/quant/house/`, tests in `tests/test_quant_house.py`): `accounting.py` (toy-firm simulator and
`step`, asserting the identity), `events.py` (`car`, `sue`), `valuation.residual_income`, `.implied_rate`, `.apv`,
`.value_driver_tv`, `.campbell_shiller`, `.beneish_m`, `fundamentals.Store.from_frames` and `.filing_lags`. Tests: RI =
DDM on the simulator; `implied_rate` inverts `dcf`; the identity of ch. 9 to 1e-12 on synthetic data.

**`compute.py` items** (4-core CPU, seeded, resumable; network time excluded):

| Item | What | CPU min |
|---|---|---|
| shiller, cape, factors, dcf, envelope | existing (envelope extended to OSAP and NI months from 2021) | 1 |
| pstar_sim, duration, issuance | recursion frames; rate betas; NI sorts | 1 |
| dcf_mc | 20k draws, value-driver surface | 1 |
| erp | implied rate 1960–2020 vs Damodaran | 1 |
| campbell_shiller | VAR, subsamples, Stambaugh bootstrap 5k | 3 |
| edgar_panel | parse frames (≈15 concepts × 12 FY) and 100 companyfacts | 4 |
| pit_audit, sloan, ri, mscore | restatement map; persistence regressions; P/B cross-section; M-score | 5 |
| pead | 100 firms × ~44 quarters, CARs, quintiles, bootstrap | 6 |
| osap | 208 predictors pre/post; block bootstrap 2k | 8 |
| merger | CPRI implied p; MERFX kink; bootstrap 5k | 2 |
| simulator | 1,000 toy firms for the accrual reversal and RI = DDM checks | 2 |
| forecaster | 4 models; MLP 5 seeds × 300 epochs, 30 checkpoints; 8-config sweep (logged in the trial counter) | 75 |
| **total** | | **≈ 110** |

## 4. Industry and frontier: the full source list

The industry chapter (ch. 17) and the frontier chapter (ch. 18) give each source's URL inline. All were checked on 2 Nov 2026
by search or by fetching the page, except where marked *(unverified)*/*(verify)*. **Allegations:** the SEC's Luckin and Kraft Heinz matters were
settled without admitting or denying (say so on screen). Rural/Metro and Dell are court findings. The FTC's case
against Tapestry–Capri was the agency's claim; the court granted an injunction and there was no final merits ruling.

## 5. Revised SYLLABUS.md §6 entry (ready to paste)

```markdown
### Part 3 · Value, Accounting and the Firm (~58)
1. Time value: NPV, IRR (and when it has two roots), annuities and perpetuities; Gordon growth, and the duration of
   equity, (1 + r)/(r − g), against growth and value stocks' measured rate sensitivity.
2. The three statements as one double-entry machine, run on screen; DuPont; accruals, and Sloan's persistence test
   rerun on EDGAR.
3. XBRL and the point-in-time fundamentals store, on real filings: filing lags against the 60/75/90-day rules, and
   restatements and recasts measured (Kraft Heinz, GE).
4. DCF: free cash flow from the statements, the value-driver formula (growth adds value only when RONIC > WACC), the
   enterprise-to-equity bridge, the (r, g) surface, and a Monte Carlo of the value.
5. The cost of capital: WACC, APV, levered betas, and the market's implied return (Damodaran's ERP rebuilt, 1960–2020).
6. Residual income (Ohlson 1995) derived from clean surplus; P/B = 1 + (ROE − r)/(r − g).
7. Multiples (P/E, PVGO, EV/EBITDA) and the CAPE; the Campbell–Shiller identity and Cochrane's decomposition on 150
   years of Shiller's data.
8. Modigliani–Miller (1958) by arbitrage; the tax shield, Miller (1977), distress and the trade-off; what CFOs say
   (Graham–Harvey).
9. Payout: the dividend-irrelevance proof; buybacks, Rule 10b-18, the EPS illusion; issuers against repurchasers.
10. Equity as a call (Merton 1974): risk-shifting, debt overhang (Myers 1977), real options.
11. Earnings announcements: SUE, an event study from 8-K dates, the drift (Ball–Brown 1968; Bernard–Thomas 1989), then
    and now.
12. Accounting signals that became factors (accruals, F-score, gross profitability) and their decay after
    publication, across 200 predictors (McLean–Pontiff; Chen–Zimmermann).
13. Merger arbitrage: the spread as a risk-neutral probability, Capri–Tapestry (2023–24), and the short put (Mitchell–Pulvino),
    re-estimated on The Merger Fund.
14. Forensic accounting: the Beneish M-score and its base-rate problem; Dechow et al.'s F-score.

*Textbooks:* Berk–DeMarzo ch. 2–4, 7–9, 14–19, 22, 28; Brealey–Myers–Allen ch. 2–6, 16–19, 22, 28, 31; Damodaran ch.
2–3, 7, 9–20, 28–32; Koller et al. ch. 2–16, 20, 32; Bodie–Kane–Marcus ch. 18–19; CLM ch. 7; Luenberger ch. 2–3.
*Computed/Trained:* p* recursion; rate betas of B/M deciles; DCF Monte Carlo; implied ERP; Campbell–Shiller VAR with
Stambaugh bootstrap; EDGAR panel (frames, companyfacts, submissions): restatement map, Sloan regressions, P/B vs ROE,
M-score; PEAD event study; 208 OSAP predictors before and after publication; NI sorts; Capri implied probability;
MERFX kink regression; an earnings forecaster (random walk, OLS, ridge, MLP; 5 seeds) replayed.
*Visuals:* the receding cash-flow conveyor; the duration fulcrum; three ledgers running with the identity lit; the 3D
accrual-persistence planes; the bitemporal plane with the as-of line sweeping; the (r, g) and (g, RONIC) surfaces; the
P/B surface crossing 1 along ROE = r; the return/dividend tug-of-war; the fixed pie with the government wedge; the
equity and debt surfaces over (A, σ); event-time paths piling into SUE lanes; 99 predictors collapsing to three bars.
*Crisis:* Enron (2001), Wirecard (2020), Luckin Coffee (2020) and Kraft Heinz (restated 2019): what the statements, the
accruals and the M-score showed at the time.
*Firms:* corporate finance practice (Graham–Harvey); banks' valuation groups in court (Dell, Rural/Metro); rating
agencies; activists (13D); quant equity on fundamentals (AQR, OSAP); merger-arbitrage funds; the SEC, the FASB.
*Desk:* the buyback question; Gordon's implied return; the merger-arb probability; "ROE 12%, r 8%, g 4%: P/B?"
*House:* the fundamentals store on real EDGAR filings; the accounting simulator; valuation (RI, implied rate, APV);
event studies.
```

## 6. Estimated minutes

Per chapter, see §3.20: **58.5 min in 20 chapters** (floor 50 cleared by 8.5 min; if the render runs long, ch. 16's
M-score and ch. 18's papers 3–4 are the first cuts, about 2 min). Compute about 110 CPU-min (≤ 2 h).

## 7. Open points for the implementer
- EDGAR needs `SEC_USER_AGENT` set by the owner (a real contact). No e-mail is hard-coded.
- The OSAP release must be pinned (2024.10 used here). Newer releases change the numbers slightly; checksum the parquet.
- Every *(verify)* / *(unverified)* item above is checked or dropped before render. Check especially the Sloan coefficients,
  the Beneish coefficients and threshold, Piotroski's 23%, Graham–Harvey's CAPM share, the S&P ratio cut-offs, Gormsen–Lazarus,
  Eisfeldt–Kim–Papanikolaou, Cao et al. and Martineau.
- Chinese: new terms for the QUANT_ZH_GUIDE: 剩余收益模型, 干净盈余, 应计项目, 盈余公告后漂移, 标准化未预期盈余, 隐含资本成本,
  债务悬置, 资产替代, 并购套利, 时点数据库.
