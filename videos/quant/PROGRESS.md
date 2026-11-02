# Quant, Built: progress log (read this first when resuming)

The plan is [`SYLLABUS.md`](SYLLABUS.md); this file says what exists, what is next, and the exact commands.

## Resume in a fresh container

```bash
bash tools/setup_linux.sh && source .venv/bin/activate     # system packages + .venv (idempotent)
python -m explainer.quant.data                            # market data into .cache/quant_data (checksummed)
python -m pytest -q tests/test_quant_house.py             # the House library
python -m videos.quant.quant10.compute                    # Part 10's numbers into .cache/quant10 (~8 min)
python -m videos.quant.quant1.compute                     # Part 1's numbers into .cache/quant1 (~6 min)
EXPLAINER_TTS=silent python tools/qa_scene.py quant10 Hook   # one chapter, silent, with a contact sheet
```

Videos, audio, `media/`, `renders/` and `.cache/` are never committed (`.gitignore`); everything regenerates.

## Done

- **Phase 0 (partial).** `explainer/quant/` (acts, parts, timeline, cards, House chart; palette `explainer.style.QC`),
  the House library v0 (`explainer/quant/house/`: `bs`, `trees`, `paths`, `hedge`, `surface`), tests, the data
  layer (`explainer/quant/data.py`, manifest `videos/quant/data/manifest.json`), `tools/setup_linux.sh`.
- **The Surface** (Deribit BTC, 10 Dec 2025 08:00 UTC; 11 Dec for out-of-sample): 254 out-of-the-money quotes,
  11 expiries.
- **Part 10 compute** (`videos/quant/quant10/compute.py`): all items.
- **Part 10 English**: all 15 chapters written and reviewed by silent contact sheet (`tools/qa_scene.py`); README
  with desk questions and problems (English and Chinese); lecture_length estimate 55 min.
- **Part 10 Chinese narration**: `videos/quant/quant10/zh_lines.py` covers 70 of 70 source lines (templates for
  the computed ones); glossary and style in `videos/quant/QUANT_ZH_GUIDE.md`; `quant` is in `make.py`'s `BILINGUAL`,
  and `qa_audio.py` / `qa_series.py` resolve the series from the video name.
- **Part 10 silent build**: `renders/quant10_480p.mp4`, 52.6 min, 15 chapters; `tools/dead_air.py` finds only
  three 1.5–2.2 s transitions. (Implied's 3D surface is the slow chapter: about 29 min at 480p.)
- **Part 10 Chinese**: `narration_zh.json` filled (70 lines, `--verify` clean); on-screen text in
  `videos/quant/quant_text_zh.json` (577 strings; only "Vega" stays Latin); a Chinese Hook preview reviewed.

## In progress

- **Narrated builds** (CPU voice, Kokoro-82M, 720p): Part 10 is finished, English and Chinese
  (`renders/quant10_720p.mp4`, `renders/quant10_720p_zh.mp4`; `dead_air.py` finds 3 s of blank screen in 55 min).
  Parts 1 to 6 are queued, in that order.
- **Part 7** (Time Series and Volatility): every scene, the README, the Chinese narration and the on-screen text are
  done. The Chinese dry run is in progress (`renders/make/quant7_zh_dry.log`); the narrated build goes in the queue
  after Part 6.

## Direction, 2 November 2026 (evening): every part to 50–60 minutes

The owner's instructions: parts must replace college lectures (3Blue1Brown-style visuals, full technical depth),
50–60 minutes each, as complete as possible (every textbook core section, every listed paper, frontier work and how
hedge funds and trading firms actually do it), hands-on like *AI, Built* (models trained and replayed, code labs,
simulations running on screen). Do **not** send rendered files to the owner.

Measured lengths (tools/lecture_length.py): Part 1 44.9, 2 24.6, 3 28.7, 4 23.5, 5 21.4, 6 18.9, 7 19.2, 8 28.2,
9 20.8, 10 45.6, 11 19.4, 12 15.5, 13 26.0, 14 19.9, 15 22.3, 16 19.0, 17 27.0 minutes. The AI series runs 44–64
(17–19 chapters each).

Process per part: (1) a research plan, `scratchpad/plans/quantN.md` (agents audit syllabus items, textbook
sections and papers, and propose 16–20 chapters with signature visuals, labs, replays and compute); (2) revise the
part's SYLLABUS.md entry; (3) write the new chapters and compute; (4) README with a textbook audit; (5) zh narration,
on-screen text, dry run; (6) build. The revised standard is SYLLABUS.md section 1. New instruments in
`explainer/quant/viz.py`: `lab_card`/`lab_run` (code on screen, then run), `TrainingReplay` (checkpoints scrubbed with
the loss curve), `seed_band`.

Builds are paused: narrated builds resume only after a part is expanded (the narration cache keeps finished lines).

## Builds queued (CPU voice, 720p)

Built: Parts 10, 1, 2 (English and Chinese; Part 2's Chinese is rebuilt after a missing string was added). One serial
queue (a lock file, no `pgrep`: the old chained scripts deadlocked because their parent shells' command lines matched
the pattern they waited on) builds, in order: quant3, quant4, quant5, quant6, quant7, quant8, quant9, quant13,
quant11, quant12, quant2, quant14, then quant15 and quant16 once their on-screen text is translated. After a container
restart, rerun for each unbuilt part in that order (each rerun resumes from cached scenes):

    python tools/make.py quantN --cpu-voice -q m --steps build check   # log: renders/make/quantN_cpu_voice.log

## Part 2 plan (The Machinery of Markets), facts checked 2 Nov 2026

Data in hand (`explainer/quant/data.py`): Binance USD-M perpetual BTCUSDT klines (`market="futures/um"`) and funding
(`binance_funding`, from 2020-01; 2020 average about 17% a year); FRED via `data.fred` (SOFR, DFF, IOER to 2021-07,
IORB after, WRESBAL, RRPONTSYD, DTB3). Stooq (single stocks) is blocked here.

Chapters: 0 Hook: the life of a trade (order, broker, exchange, CCP, DTCC, T+1) and Robinhood on 28 January 2021 (the
NSCC asked for about $3bn, cut to $1.4bn, as its CEO described it; accounts differ). 1 Instruments and how each is
quoted. 2 Orders, the book, price-time priority, the closing auction (a toy call auction computed). 3 Clearing:
novation and multilateral netting (simulated: gross vs bilateral vs CCP net), T+1 since 28 May 2024. 4 Margin: a
10x long BTC perpetual from 1 March 2020, hourly variation margin, liquidation on 12 March (real Binance prices), and
funding. 5 Short selling: locate, borrow fee, recall; Volkswagen (26 Oct 2008 Porsche disclosed 74.1% via shares and
cash-settled options; above EUR 1,000 intraday on the 28th, close EUR 945, briefly the world's most valuable company;
hedge funds' fraud claims are allegations). 6 Repo and securities lending: haircut = 1/leverage. 7 Prime brokerage
and total return swaps (Archegos preview, Part 41). 8 Business models and fees (2-and-20 with a high-water mark,
computed; pass-through fees). 9 The quant industry map and roles. 10 Markets around the world (A-shares: T+1, +/-10%,
STAR and ChiNext +/-20%; India: SEBI, Sept 2024: 93% of individual F&O traders lost money FY22-FY24, Rs 1.8 lakh crore).
11 Crisis file: 17 September 2019, SOFR 5.25% from about 2.2% (tax date plus Treasury settlement, reserves at a
multiyear low; FRED). 12 The House: treasury and funding (`house/funding.py`: margin account, financing at SOFR
plus spread, borrow fees, perp funding; tested). Outro: desk "make me a market on the number of trading days in a
year".

Computed (`python -m videos.quant.quant2.compute`, seconds): BTC perp from 1 Mar 2020 ($8,555) to the 13 Mar low
($4,063 hourly close, -52.5%): 10x liquidated 9 Mar 14:00, 3x 12 Mar 20:00, 2x 13 Mar 01:00 ($271 below zero:
the insurance fund's); netting 5,395 trades $11.0bn gross -> $3.1bn bilateral -> $1.03bn via a CCP (-91%); closing
auction clears at 100.07; perp funding 2020 averaged 17.2%/yr, positive 86% of settlements, $2,238 to hold one coin
long; SOFR 2.20 (13 Sep) 2.43 (16) 5.25 (17) 2.55 (18) 1.95 (19 Sep 2019), IOER 2.10, reserves low $1.39tn (18 Sep
2019) from $2.05tn (Jan 2018); fees: $1 in the market 1927-2020 -> $7,893 gross, $360 after 2-and-20 with a
high-water mark (4.5% of the profit kept), $3,288 after a 1% fee. Scenes: all 12 written and previewed silently (`renders/qa/quant2/`); README with solutions. Remaining: Chinese
(zh_lines.py, on-screen text), full build.

## Part 3 plan (Value, Accounting and the Firm)

Data (`explainer/quant/data.py`): `shiller()` (ie_data.xls via xlrd: price, div, earn, cpi, gs10, CAPE, 1871-2020)
and `ken_french_sorts(name)` (monthly value-weighted sorts 1963-2020: AC accruals, OP profitability, INV investment;
E-P from 1951; BE-ME from 1926). SEC EDGAR answers 403 here (it wants a contact e-mail in the User-Agent; the user's
must not be sent), so XBRL point-in-time fundamentals wait for another machine; the chapter on XBRL is described,
not computed.

Chapters: 0 Hook (what is a share a claim on? a dividend stream; Shiller's price vs the present value of dividends,
"Do stock prices move too much?", 1981); 1 time value: NPV, IRR, annuities, perpetuities, Gordon growth derived;
2 the three statements as linked ledgers (a toy firm); 3 DCF and WACC, the value surface over growth and discount
rate in 3D; 4 multiples and CAPE (Shiller): CAPE against the next ten years' real return, with the overlap caveat;
5 Modigliani-Miller by arbitrage, taxes, the trade-off; 6 payout: dividend irrelevance, buybacks (desk question);
7 equity as a call on the firm (Merton, Part 20 preview); 8 earnings and the post-announcement drift (Ball-Brown
1968, Bernard-Thomas 1989; schematic, cited); 9 accounting signals that became factors, computed on French's sorts
(Sloan's accruals, Novy-Marx's profitability, investment): long-short returns, Sharpe, by decade, and their decay
after publication; 10 crisis file: Enron (2001) and Wirecard (2020), public record (verify dates and figures);
11 the House: `house/valuation.py` (npv, irr, annuity, gordon, dcf, wacc, MM levered beta, Merton equity), tested,
and the fundamentals store described; outro (desk: a debt-free firm buys back 10% at market: price and EPS).

Computed (`python -m videos.quant.quant3.compute`, seconds; House `valuation` tested): Shiller 1871-2020 real, constant
discount 8.3%: sd of annual log changes, price 17.5% vs p* 2.1% (8x); 40 years with |change| > 20% vs none for p*.
CAPE vs next-10y real total return: slope -0.074 per log unit, R2 0.32 on 1,560 overlapping monthly starts (~13
independent decades); Dec 2020 CAPE 33.8 -> predicted 0.6%/yr real for 2021-30 (the envelope will tell). Decile
long-shorts 1963-2020 (annual mean, before/after publication): accruals 3.8% (t 2.9; 5.0% -> 2.1%), OP 2.4% (t 1.3),
investment 4.3% (t 2.9; 6.4% -> -1.1%), B/M 4.0% (6.9% -> 1.0%), E/P 3.8% (7.5% -> 2.6%). DCF: FCF 100 growing 5% for
5 years then 2%, at 8%: 1,936, 76% terminal; at 7% and 3%: 2,816.

Status (2 Nov 2026): all 12 scenes written and previewed silently (Hook, TimeValue, Statements, DCF, CAPE, MM, Payout,
Signals, Events, Crisis, House, Outro); README with solutions (EN, ZH); `zh_lines.py` 50 of 50; House
`fundamentals.py` (bitemporal store, EDGAR company-facts loader) tested; `compute.py envelope` sealed Shiller's and
French's hold-outs and registered `cape_forecast_2021_2030` (trials 1) and `accounting_signals_part3` (trials 5):
do not edit `compute_cape` / `compute_factors` (their source hash is registered). Shiller's xls ends Sept 2023, so the
finale scores the CAPE forecast on a second source. Remaining: on-screen text (`collect_text.py quant3`, `--check`,
merge), Chinese dry run, narrated build. Facts verified: Enron (restatement 8 Nov 2001, $586m; bankruptcy 2 Dec; SEC:
>$5bn prepays as operating cash), Wirecard (EUR 1.9bn ~ 1/4 of balance sheet; insolvency 25 Jun 2020; BaFin short ban
18 Feb-18 Apr 2019), Mitchell-Pulvino (4,750 mergers 1963-98, ~4%/yr excess after costs), AbbVie-Shire (withdrew
15 Oct 2014 after Treasury notice of 22 Sep; $1.635bn fee), McLean-Pontiff (97 predictors; 26% / 58% lower).

## Part 4 (Martingales and Measure), 2 Nov 2026

House `martingale.py` (doubling, gamblers_ruin, doob_decomposition, likelihood_ratio, stable_mcculloch validated
against scipy's levy_stable, return_probability, EProcess) tested. `compute.py` items: doob (US log wealth 9.06 =
7.28 drift + 1.78 martingale; EWMA compensator 2.893 vs QV 2.894), measure (median L_300 0.002 = e^{-300 KL}), ruin
(bold 48.6% vs timid 0.45% at 100 units), stable (McCulloch alpha US 1.40, BTC 1.27; Mantegna-Stanley alpha 1.67, 1962-86
1.44, Gaussian 1.99), nikkei (FRED NIKKEI225; 19,331 -> 17,785 -> 16,809), peeking (t-test 50% vs e-process 3.2%),
eprocess (sign continuation: 1926 start passes 20 in Feb 1929, 1975 start in Mar 1976, 2000 start max 6.7, BTC max
1.4), envelope (Nikkei sealed; two tests registered; trials 10). 11 scenes written and previewed; README with
solutions (EN, ZH); zh_lines 44 of 44. Remaining: on-screen text (collect running), Chinese dry run, narrated build.
`data.fred` now fetches a series' whole history on first use (a cached file from a later start is refetched).

## Part 5 (Stochastic Calculus), 2 Nov 2026

House `sim.py` (Euler, Milstein, scheme_orders with exact weak errors, ou_exact, cir_exact, merton_jumps,
hawkes_thinning/fit/intensity, fbm Davies-Harte, hurst_from_increments, signature2) tested. Compute: variation,
signature plot (BTC 1m 2020: 80% at 1 min vs 71% daily), Ito vs true-midpoint Stratonovich, orders (strong 0.50/0.93,
weak 0.99/1.00), rates (DTB3 Vasicek kappa 0.099, theta 4.1%, sigma 1.4%; CIR Feller 0.58; Vasicek 10y 1.38% vs DGS10
0.93%), girsanov (var / 52), stoploss (shortfall 7.94-8.10 at every frequency vs call 7.97; corr with 1/2 L 0.97),
jumps (BTC 1h 2018-20: 204 > 5 bipower sd, 24% of variance), hawkes (229 events, branching 0.36, half-life 7.6 h),
rough (BTC 5-min RV 2019-20: H = 0.15), fbm; registered 2 tests (trials 12). 10 scenes, README (EN, ZH), zh_lines
39/39, on-screen text, Chinese dry run all done; narrated build queued (queue4.sh). The one-minute BTC hold-out is not
sealed (not downloaded); seal it before any later part tests a strategy on it.

## Part 6 (Financial Econometrics), 2 Nov 2026

House `econ.py` (ols with naive/White/NW/HH/cluster/two-way, fama_macbeth, block and stationary bootstrap, sharpe_se,
years_to_significance, Bonferroni/Holm/BH, Stambaugh, gmm, dml_plr with cross-fitted ridge splines, shrink_means)
tested. Data: `ken_french_industries`, `ken_french_factors_monthly`. Compute: overlap (DY 5y: t 15.0 / 2.8 / 2.5; null
size 77% / 17% / 14%), stambaugh (annual DY beta 0.034 -> 0.016), gmm (beta 1.002, gamma 1.1, J 20.0 p 0.0005; HJ gamma
421), event (turn of month: 74% of returns 1926-86, 45% after), panel (t: 1.86, 1.21, 0.27, 0.27, FM 5.08), bootstrap
(SR 0.44, se 0.103 iid / 0.119 block), shrinkage (MSE 8.0 -> 3.8), multiple (5 of 49 raw, 0 after any correction),
ellipse, dml (0.300 vs naive 1.15), snr; envelope sealed industries, monthly factors, PCE; trials 63. 9 scenes, README
(EN, ZH), zh_lines 32/32, on-screen text, Chinese dry run passed (all 9). Narrated build queued (queue5.sh).

## Part 7 (Time Series and Volatility), 2 Nov 2026

House `vol.py` (realized measures, GARCH/GJR/EGARCH by MLE on rescaled returns, HAR/HARQ, QLIKE, Diebold-Mariano,
ADF, Engle-Granger, Hamilton EM, Kalman local level, DCC) tested. The compute items:
- spurious: 89% of levels regressions reject; BTC on the US market gives t 24.
- coint: spot and perp are cointegrated, EG t -7.2, half-life 1.2 days.
- regimes: calm 55 months, turbulent 10, turbulent 14% of the time.
- garch: US alpha .105, beta .884, half-life 63 days; GJR gamma .111.
- dcc: the stock-bond correlation is +0.2 to +0.3 to the 1990s, then -0.33 and -0.46.
- realized: from Binance one-minute data, RV1 106%, RV5 96%, TSRV/RK 93%, BV 92%, jumps 10%.
- har: b_d .41, b_w .03, b_m .43, R2 .38; HARQ b_q -3.0 (t -0.7).
- race: QLIKE on 2020 ranks log-HAR .363, LSTM .371, transformer .410, HARQ .426, HAR .427, GJR .444, GARCH .452 and
  EWMA .512. The LSTM beats HAR (DM t -3.0) but not log-HAR (t +1.5). On MSE, GJR is first.
- scaling: on 13 March 2020, GARCH spot vol is 85% and the one-year average 52%.
- envelope: trials 71. Log-HAR was added after the first look; this is disclosed on screen and counted.

There are 8 scenes, a README (EN, ZH), zh_lines 34/34 and the on-screen text (188 strings).

Notes for whoever picks this up:
- **PyTorch threads.** Train tiny networks with `torch.set_num_threads(1)`. With the renders running, the default
  thread pool made the race about 40x slower (more than an hour, against 25 s).
- **System pip.** An earlier session ran pip against the system Python, which added several GB to its
  site-packages (a CUDA torch, transformers, chronos). With the user's go-ahead those packages were removed on
  2 Nov 2026; the project venv is unaffected.
- **Deferred to production.** The zero-shot foundation models (Chronos, TimesFM, Moirai) need packages outside the
  venv, and installing or importing external code needs approval. The race uses CPU models trained here.

## Part 8 (Decisions and Control), 2 Nov 2026

House `control.py` (tested against closed forms): CRRA/CARA, certainty equivalents, Arrow-Pratt; `bellman_merton`
(backward induction with Gauss-Hermite and certainty-equivalent interpolation; interpolating V itself biased the
policy toward zero at small dt); HARA floor (portfolio insurance); Kelly binary/continuous; `realized_growth`;
`secretary`; `bsde_regression`, with polynomial or hat bases (polynomials can't follow kinks, giving 1.194 against the
PDE's 1.230; hats give 1.225 at 300k paths); `hjb_two_rates`; `ppo_merton`. Getting PPO to converge needed one-step TD
advantages and a fixed exploration of 0.8: learned exploration collapsed and stalled near 1.5. It now reaches 1.84,
matching the discrete optimum of 1.836.

The compute items, with their results:
- coin: Kelly 20%, 93.8% reach the cap, 0% go bust; all-in 87% go bust.
- bellman: Merton 61.7%; the floor matches to 0.005.
- merton_us: excess 8.2% (se 1.9%), sigma 18.5%, fractions 238/119/79/.../24%.
- kelly_us: best 218% (growth 12.6% against 9.7% at 100%); bootstrap 116-302%; the split sample picks 198%, which
  then grows 13.4%; ruin at 348% (Sep 1931).
- fractional, samuelson, ergodic, ltcm (an illustration), secretary (37, 37.1%), american (9.87 against 9.35), bsde,
  ppo.
- envelope: trials 72.

There are 12 scenes, a README (EN, ZH) with solutions, and zh_lines 43/43. Facts checked:
- Haghani-Dewey: about 30% went bust (abstract).
- LTCM: $129bn assets on $4.7bn, $1.3tn notional, under $1bn by mid-September, $3.6bn from 14 banks.
- PNP: about 15% after fees, 1969-88.
- Samuelson 1979: one syllable except the last word.
- 19 Oct 1987: French's market return was -17.4%.

## Part 9 (No Arbitrage), 2 Nov 2026

House `arbitrage.py` (tested):
- `parity_gap`.
- `ftap`: Stiemke/Farkas by LP, returning state prices or an arbitrage portfolio.
- `superhedge`: the upper and lower LPs.
- `static_checks` and `calendar_check`.
- `mot_bounds`: martingale optimal transport by HiGHS, with a sparse constraint matrix.
- `ross_recovery`: Perron-Frobenius.

The compute items:
- parity: 339 call-put pairs on the Surface's trades; median gap 3.4 bp (trades) and 1.5 bp (marks); basis 2.8-4.8%
  a year by expiry.
- density: SVI and BL for 26 Dec 2025 (16 d) and 27 Mar 2026 (107 d); down/up 20%: 2.9/1.9% and 19.1/18.4%; checks
  pass.
- mot: forward-start straddle in [0.137, 0.218], log-normal 0.180. Coarse bins for the first marginal keep convex
  order, and this is checked.
- ross: exact in the CRRA chain; with a martingale tilt, error 0.051 and pessimistic.
- incomplete: binomial is a point; 3+ states give [0, 0.197].
- envelope: trials 72, no test.

There are 10 scenes, a README (EN, ZH), zh_lines 35/35. Remaining: on-screen text, Chinese dry run, narrated build
queued.

Facts checked:
- GameStop: the SEC staff report (Oct 2021) gives +2,700% low to high, -86%; enthusiasm, not covering.
- Melvin: $2.75bn and -53% (Reuters).
- The Robinhood box-spread ban (2019) and its quote. The loss figure is disputed and not used.

## Part 11 (Trading Options): facts checked, 2 Nov 2026, before building

- **SEBI v Jane Street.** An ex-parte interim order dated 3 July 2025 impounded about Rs 4,843.57 crore of alleged
  "unlawful gains". The firm deposited it in escrow and was then allowed to resume. SEBI alleges that on Bank Nifty
  expiry days the firm bought constituents (cash and futures) in the morning to support the index while building
  short exposure in options, then sold futures and stocks after noon to drag the index down. Reports cite various
  counts of expiry days. Jane Street disputes the findings. Describe all of this as *alleged*.
- **SEBI F&O studies.**
  - Sept 2024: 91.1% of individual traders lost money in FY24 (about 7.3 million), with net losses of about Rs
    75,000 crore in FY24 and Rs 1.81 lakh crore over FY22-24.
  - July 2025: FY25 losses were Rs 1,05,603 crore (+41%), and 91% lost money.
- **SEBI circular of 1 Oct 2024**, effective 20 Nov 2024:
  - each exchange may offer weekly expiry on only one benchmark index (NSE keeps the Nifty 50, BSE the Sensex);
  - the minimum contract size rises to Rs 15 lakh;
  - a 2% extreme-loss margin applies to short options on expiry day;
  - intraday position monitoring follows in 2025.
- **Firm founding dates.** SIG 1987 (months before Black Monday); Optiver 1986, Amsterdam; IMC 1989, Amsterdam. Jane
  Street's founding year is reported as 1999 or 2000. The claim that SIG trains traders with poker is not yet sourced.
- **House** `quoting.py` (tested): books, P&L surfaces, implied correlation, quotes, Whalley-Wilmott bands.
- **Built** (compute, 10 scenes, README EN/ZH, zh_lines 36/36). Results:
  - scalp: May 2021 straddle at 74% implied, realized 127%, P&L +1.7 on a premium of 16.9 (gamma +6.4, theta
    -4.6).
  - edge: 1.75 against 0.57 per month on non-overlapping months, t of about 2.4; registered; trials 73.
  - mm: inventory 64 -> 9 with skewed quotes.
  - dispersion: median 0.63; peaks 0.82, 0.79, 0.72; low 0.27 (2001).
  - alleged: a toy only.
  - hedging: deep hedge (move a learned fraction toward delta) lies inside the WW frontier at kappa 1, 4 and 16. A
    first residual-on-delta version, trained 250 steps, was worse than the bands.
  - Remaining: previews QA, on-screen text, dry run, build.

## Part 12 (The Volatility Surface), 2 Nov 2026

- **Data.** The Surface (Deribit trades, 10 and 11 Dec 2025) and 100 weekly surfaces (Wednesdays, 3 Jan 2024 to
  26 Nov 2025, 00:00-12:00 UTC trades), checksummed in `data/manifest.json`. Binance hourly; Deribit DVOL; FRED VIXCLS.
- **Facts checked.** VIX 17.31 -> 37.32 on 5 Feb 2018 (+116%, its largest one-day rise); XIV lost more than 90% and
  Credit Suisse announced its redemption. SSVI calendar condition from Gatheral-Jacquier (2014), Theorem 4.1.
  Baltussen et al. (2021) intraday momentum across about 60 markets since 1974; 0DTE above 40% of SPX option volume.
- **House** `volsurface.py` (tested): SSVI, g-function, Dupire local variance, variance-swap strike, VIX recipe.
- **Built** (compute, 9 scenes, README EN/ZH, zh_lines 33/33). Results:
  - SSVI fits to 0.74 vol points (vega-weighted), rho -0.23; min g 0.075 (SVI) and 0.26 (SSVI).
  - sticky test: sticky moneyness misses next-day quotes by 2.6 vol points, sticky strike by 3.0.
  - local vol: 30-day forward smile 60 days out has skew 3.4 points against 6.5 today.
  - variance swap 48.8% against ATM 43.7%; our VIX recipe 48.8% against DVOL 45.9%.
  - VRP: 54% implied against 47.6% realized, positive 76% of weeks, Newey-West t 3.6; SVIX bound 31% a year.
  - VAE (2-d latent, CPU): rebuilds to 1.9 vol points; corr(z1, ATM) 0.96, corr(z2, skew) -0.39.
  - No strategy tested; trials stay at 73.
  - Remaining: previews QA, on-screen text, dry run, build.

## Part 13 (Stochastic Volatility and Jumps), 2 Nov 2026

- **House** `stochvol.py` (tested): Heston (little trap), Bates, Kou, VG and NIG characteristic functions; COS pricing
  (Fang-Oosterlee Heston benchmark to 1e-8); Hagan's SABR and its density; Andersen's QE; Bates/VG simulators;
  forward-start and cliquet payoffs; the calibrator. `volsurface.theta_at` (SSVI ATM variance linear from zero; the
  old clamp made local vol ~0 before the first expiry) and `local_vol_paths` (4 sub-steps a day), shared with Part 12,
  whose local-vol forward skew is now 3.4 points (was 2.6 with the daily, clamped simulator).
- **Facts checked.** S&P 500 -20.5% / Dow -22.6% on 19 Oct 1987; post-crash skew (Rubinstein 1994; Bates 2000).
  Gatheral (2008, Bachelier Congress, London): a diffusion fits SPX and VIX smiles only approximately. Guyon (2020,
  Risk): an exact joint fit by a discrete-time optimal-transport model.
- **Results.**
  - facts: 30-day RV 17-122%; vol of vol (DVOL) 89%; DVOL +6.4% on days BTC fell >5% and +0.5% on days it rose >5%;
    corr(return, d log DVOL) -0.23, by year -0.42, -0.58, +0.30, +0.04, -0.25 (2021-2025).
  - calibrate (193 quotes): BS 3.89, Heston 1.33 (kappa 14.8, xi 4.6, rho -0.31, Feller ratio 0.37; the 3-day expiry
    is missed by 5.3), Bates 1.31 (jumps go to the bound: 20 a year of -4%), VG 2.89, NIG 2.70, SABR per slice 0.38.
  - SABR's nu falls like T^-0.49; the market's ATM skew grows like T^-0.49 (Heston flat, Levy ~1/T).
  - QE vs Euler, 3-month ATM call: with 2 steps Euler +20%, QE -1.2%; QE inside the noise from 16 steps.
  - SABR's 10-year density (rates-like: F 3%, beta 1/2, nu 0.4, rho -0.3) is negative below 0.7%, mass 0.63.
  - landscape: a curved (kappa, xi) valley (1.30 at kappa 15, 1.43 at kappa 5); 12 random starts reach one minimum.
  - history (100 weeks): kappa moves 25% a week (median), sits at its bound 20% of weeks; Feller fails 91%; rho > 0 in
    54% (call-side smiles: Part 12's 30-day skew was call-side in 67% of 2024 weeks).
  - SLV (particle method, half Heston's vol of vol): reprices to 0.68 (30 d) - 0.44 (120 d) vol points.
  - forward smile (30 d starting in 60): skew today 6.5; LV 3.4, Heston 6.1, Bates 6.3, VG 5.0, SLV 5.1; cliquet
    13.1-14.2% (8% apart); forward-start ATM 11% apart.
  - forward variance: Sat 13 - Sun 14 Dec priced at 32% vol; Saturdays realized 29% vs 54% weekdays (2024-25 hourly).
- **Built** (compute, 11 scenes, README EN/ZH, zh_lines 46/46). Remaining: on-screen text, dry runs, previews, build.

## Part 14 (Rough and Path-Dependent Volatility), 2 Nov 2026

- **House** `rough.py` (tested): rBergomi hybrid scheme (FFT convolution), rough Heston by fractional Adams (reduces
  to Heston at H = 1/2 to 1e-6; frequencies with |phi| < e^-40 are skipped, where explicit Adams is unstable), the
  lifted Heston (Abi Jaber-El Euch weights), the GJR log-RV scaling estimator, Guyon-Lekeufack PDV.
- **Results.**
  - skew: power law T^-0.49 (H ~ 0.01); bounded (T + 21 d)^-0.88 fits better (log error 0.19 vs 0.23).
  - BTC roughness (5-min RV, 700 days): H 0.08; 0.12 without the weekday pattern. Estimator on fBm: 0.1 -> 0.09,
    0.3 -> 0.31, 0.5 -> 0.50, but 0.05 -> 0.015.
  - smooth models through the same lens: 10-day log-OU 0.38; 1 + 60 day 0.42; 5-hour 0.02.
  - rBergomi (175 quotes <= 200 d, 20k paths, CRN, fresh-path repricing): H 0.03, eta 2.0, rho -0.56, error 0.83 vs
    Heston 1.37 on the same quotes; skew tracks the market 4-200 d, misses 3 d.
  - rough Heston free: H 0.45, nu 4.5, lambda 16, error 1.28 (Heston-like). Held: H 0.05 2.25, 0.1 1.49 (nu 1.0,
    lambda 2.0), 0.2 1.41.
  - lift (H 0.1, 30-day smile): N 1 4.7, 10 1.1, 20 0.57, 50 0.26 vol points.
  - PDV on DVOL (fit 2021-23): R^2 0.88 in, 0.42 out; baseline 0.68, -0.27; activity 18.7 vs trend 0.9 vol pts.
- **Built** (compute, 12 scenes, README EN/ZH, zh_lines 40/40). Remaining: on-screen text, dry runs, build.

## Part 15 (Exotics and Structured Products), 2 Nov 2026

- **Data.** `data.yahoo_daily` (Yahoo chart API, checksummed): 510500.SS (CSI 500 ETF), 512100.SS (CSI 1000 ETF),
  ^HSCE. Yahoo has no history for the CSI indices themselves; the ETFs are labelled as such on screen.
- **Facts checked.** Bloomberg 11 Jan 2024 (~$13 bn snowballs near loss triggers); UBS ~$50 bn market; CICC knock-in
  estimates; Risk.net (hedging fuelled futures selling) vs SRP sceptics; April 2024 curbs (Bloomberg). Korea: 19.3 tn won
  HSCEI ELS outstanding (Nov 2023), 15.9 tn via banks; 1.2 tn won lost Jan-Feb 2024; FSS compensation scheme (Mar 2024);
  20-50% repaid. Henderson-Pearson (2011): SPARQS 8.77% (avg) / 7.71% (value-weighted) above model value.
- **House** `exotics.py` (tested): barriers + BGK, digitals, call spreads, geometric Asian, lookback (zero-rate branch
  fixed by continuity), snowball MC + fair coupon, worst-of, UVM (Black-Scholes-Barenblatt).
- **Results.** BGK matches MC at every monitoring frequency (monthly 7.44 vs continuous 7.28). Asian CV: ~21x less
  noise. Snowball fair coupon 13.4% at 20% vol; dealer delta 1.7 above KI, 1.15 below. 2024 book: 11 of 36 knock in
  22 Jan - 5 Feb; dealer hedge 15 -> 25 -> 15 notes' worth. Korea: 6 of 12 2021 notes lost 38-54%. Worst-of vs rho;
  measured rho 0.46. UVM bounds [0.31, 0.62] vs BS 0.45-0.48. Surrogate: 0.017 error, 0.4 us vs 3 s.
- **Built** (compute, 12 scenes, README EN/ZH, zh_lines 42/42). Remaining: on-screen text, dry runs, build.

## Part 16 (Computing Prices), 2 Nov 2026

- **House** `engine.py` (tested): Monte Carlo with antithetics, control variates, importance sampling and Sobol
  (+ Brownian bridge); MLMC; Longstaff-Schwartz and Andersen-Broadie; Greeks (bump, pathwise, likelihood ratio) and
  AAD on the AI series' autodiff; theta-scheme FD with Rannacher; PSOR American put; Heston ADI (Douglas,
  Craig-Sneyd) on in 't Hout-Foulon grids; Carr-Madan.
- **Results.** Sobol 3e-5 vs plain 0.026 at 262k paths; IS 10x less noise at K=160; bridge 31x less spread (Asian,
  64 fixings). MLMC 4/12/26x cheaper at eps 0.04/0.02/0.01. American put (25 dates): LSM 6.061, AB upper 6.075 (1,600
  inner); continuous exercise 6.090 (tree) / 6.085 (PDE). AAD 2.2x a price for 5 Greeks vs 7.4x bumping. Explicit FD
  explodes at 200 steps (von Neumann bound 400; 250 survives). CN error ratio 4.0 per doubling. ADI 0.001-0.002 at
  160x80. COS (L=16) 1.4e-6 at 128 terms, 5e-8 at 256 (L=12 floors at 7e-6 on this fat left tail); Carr-Madan 2.5e-5
  at 16,384. Race: COS beats MC's best (SE 0.016, 3 s) ~14,000x faster.
- **Checked.** Chakrabarti et al. (2021): 7.5k logical qubits, T-depth 54M, 50 MHz for ~1 s. JPMorgan/Maxeler 2011:
  ~8 h to ~4 min (as reported). The QE scheme's 50-step bias on the race call is 0.005 +- 0.006 (not significant).
- **Built** (compute, 12 scenes, README EN/ZH, zh_lines 41/41, silent previews). `why` notes in the quant series now
  wrap instead of shrinking (long notes in Parts 8-16 were unreadable). Remaining: on-screen text, dry run, build.

## Part 17 (Deep Pricing and Hedging), 2 Nov 2026

- **House** `deep.py`: pointwise rough-Bergomi calibrator; deep hedger (plain MLP with log-moneyness in units of total
  vol; Imaki band network anchored at BS delta); HLP regressor; differential ML; deep BSDE; deep stopping; neural SV SDE
  (rho kept off +-1, clamped factor, clipped gradients); signatures (lead-lag), vol x noise LSTM generator, DDPM.
- **Results** (all in the README): HLP net within 4% of BS tracking error; calibrator held-out 1.90 vol pts (label
  noise 2.86), Surface H 0.07, 0.97/1.08 vol pts, 27 s; weekly H at the 0.02 floor in 77% of weeks, near tie with a
  like-for-like Heston (1.19 vs 1.22); DML 256 samples: price 5.03 -> 0.43, delta 31x; deep BSDE 57.37 (0.12%), no
  default 59.57 discounted (paper's 60.781 undiscounted); stopping 13.886 (d=2), 26.107 (d=5, 0.2% under the paper's
  lower bound); hedger: band net beats delta and WW at every cost; plain net with costs: do-nothing zone 0.02 -> 0.10,
  price = WW's; generators: 2024-25 calmer than 2017-23, signature distance alone favours i.i.d. draws, the stylized
  facts favour the signature LSTM; NSDE barrier range 0.0671-0.0703 (lower estimate).
- **Lessons kept on screen**: results reported as measured; earlier claims (band "rediscovered", rough "wins",
  generator "closest") rewritten when the numbers disagreed.
- **Done**: compute, 14 scenes previewed, README EN/ZH, zh_lines 53/53, on-screen text 259 strings. Remaining: zh dry
  run, then queue for build.

## Next

1. Narrated masters, on a machine with the TTS server (README, "Narration"; Qwen3-TTS is 10-30x slower than real
   time on CPU, so not in a 4-core cloud container): `python tools/make.py quant10` (English and Chinese, 1080p30),
   or `tools/colab_narrate.py` on a Colab GPU. Then `tools/dead_air.py` on the narrated cut.
2. Act II: Part 8 (Decisions and Control) next, then Act III from Part 9. Part 8's plan: utility and certainty
   equivalents; Bellman/HJB; Merton by HJB and by simulation; Kelly, fractional Kelly, Thorp, and Samuelson's
   objection; optimal stopping; prospect theory and ambiguity; PPO on Merton against the closed form (CPU).
3. Phase 0 remainder: `qa_report.py` and `package_uploads.py` still list only the AI series.
