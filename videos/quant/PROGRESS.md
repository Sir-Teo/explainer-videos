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

- **Part 10 narrated build** with the CPU voice (Kokoro-82M; `python tools/make.py quant10 --cpu-voice -q m --steps build
  check`, logs `renders/make/quant10_cpu_voice.log`, `quant10.en.log`, `quant10.zh.log`). Rerun the same command after
  an interruption: narration and scenes are cached.
- **Part 1 (The Fair Game)**: compute (13 items), House `stats`, `pit`, `smile` (tested), all 16 scenes written and
  previewed silently, README with solutions, Chinese narration (76 of 76 lines). Remaining: on-screen text table
  (`collect_text.py quant1`, then `--check`), the Chinese dry run, a full silent build and `dead_air.py`, then the
  narrated build (`python tools/make.py quant1 --cpu-voice -q m`).

## Builds queued (CPU voice, 720p)

Part 10 (zh running), then Part 1 and Part 2 (en, zh): `python tools/make.py quantN --cpu-voice -q m --steps build check`
(logs `renders/make/quantN_cpu_voice.log`). Each rerun resumes. Part 1's and Part 2's Chinese text and narration
are complete; Part 1's Chinese dry run passed for all 16 chapters.

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

## Next

1. Narrated masters, on a machine with the TTS server (README, "Narration"; Qwen3-TTS is 10-30x slower than real
   time on CPU, so not in a 4-core cloud container): `python tools/make.py quant10` (English and Chinese, 1080p30),
   or `tools/colab_narrate.py` on a Colab GPU. Then `tools/dead_air.py` on the narrated cut.
2. Act II (Parts 4-8), following SYLLABUS.md section 6; Part 4 next.
3. Phase 0 remainder: `qa_report.py` and `package_uploads.py` still list only the AI series.
