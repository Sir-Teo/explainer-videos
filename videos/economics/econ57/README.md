# Economics, Built: Part 57, Reading the Economy in Real Time

Part 57 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first of Act XI, *Economics at Work*. It asks what the economy is doing right
now, and how good anyone's guess about next year is. Its answer: the present can be read fairly well, and better
each week, if the data are read as they arrive and their revisions expected; a year ahead, forecasts are hardly
better than the average of the past, and almost never predict a recession, because the best guess of a rare and
randomly timed event is never the event. So read the present carefully, say how uncertain the future is, and keep
score.

It opens on two scorecards: Paul Samuelson's quip (1966) that the stock market had predicted nine of the last five
recessions, and An, Jalles and Loungani's (2018) count of 153 recessions in 63 countries between 1992 and 2014, of
which forecasters expected a fall in output in only five by April of the year before, and in 118 by October of the
year itself. From there it covers:

- how numbers are made: GDP's advance, second, third, annual and comprehensive estimates, and payrolls' survey,
  revisions and annual benchmark (in August 2024 the BLS announced about 818,000 fewer jobs in the year to March,
  settled at 598,000; 911,000 in 2025; 79,000 in 2026); 244 quarters of first-published against latest real GDP
  growth since 1965Q4 (an average revision of 1.48 points either way, +0.44 on average, 17 quarters whose sign
  changed); 2008Q4 vintage by vintage, from -3.8% a year in January 2009 to -8.5% today;
- seasonal adjustment: unadjusted payrolls fall by two to three million every January (monthly changes with a
  standard deviation of 861,000 before 2020, against 208,000 adjusted); a simplified X-11 (a centred 2x12 trend,
  seasonal-irregular values, 3x3 seasonal averages) tracks the official monthly changes within 85,000 jobs before
  2020; without its step that leaves extreme values out, the collapse of April 2020 becomes a seasonal April slump of
  3.4%, and April 2021's adjusted figure moves by 3.3 million jobs;
- Play it: an Island quarter release by release (a survey, then hard data for each month); the nowcast goes from
  +1.1% before the quarter to -0.3% after the survey and -4.5% after the second month; the quarter fell at 3.9%;
- nowcasting: bridge equations on American GDP, 1985-2026, pseudo real time (errors of 2.24 points before the
  quarter, 2.01, 1.88 and 1.71 after one, two and three months of payrolls and industrial production); a dynamic
  factor model through the Kalman filter on the Island (errors from 3.04 to 1.06 across five releases, with honest
  bands), the news decomposition, GDPNow and the New York Fed's nowcast;
- recession signals: Estrella and Mishkin's yield-curve probit on every month since 1959 (an area under the ROC curve
  of 0.82); nine inversions of three months or more, seven followed by a recession within two years, the exceptions
  1966 and 2022-24; the Sahm rule in real time, eleven signals since 1960, two with no recession near (1976 and
  2024); 2022-24's alarms (a 25-month inversion, a probit peak of 58%, the forecasters' 50% for 2023Q3, the Sahm
  rule) and no recession;
- scoring forecasts: bias, root mean squared error, Diebold and Mariano's test; the Survey of Professional
  Forecasters' growth forecasts since 1968 against first estimates (1.86 points for the current quarter, 2.47, 2.78,
  2.98 and 2.97 up to a year ahead, against 3.04-3.10 for the past ten years' average: better for the current
  quarter and the next two, not beyond; biased up by 0.72 a year ahead);
- the record: Romer and Romer's comparison redone, 1968-2020, the Federal Reserve staff's inflation forecasts better
  at every horizon, significantly from three quarters ahead; the forecasters' probability of a fall the quarter
  before each recession since 1970 (mostly 10-40%); 2008 and 2021 from Parts 1 and 28;
- why recessions are hard: Hamilton's two regimes, where even a forecaster who knows today's state never forecasts a
  fall a year ahead, though 22% of quarters fall; the real forecasters' year-ahead forecasts were below zero in 0% of
  surveys, against 13% of quarters; forecasts that change the outcome;
- new data (Cavallo and Rigobon's online prices, Chetty and coauthors' card-payment tracker, Henderson, Storeygard and
  Weil's night lights, job postings) and text as data (Baker, Bloom and Davis's policy-uncertainty index, highest in
  April 2025; Hansen, McMahon and Prat on FOMC transcripts; Gentzkow, Kelly and Taddy);
- judgment, combinations (Bates and Granger's weights: about 0.55 on the staff for the current quarter, all of it a
  year ahead; Stock and Watson's combination puzzle) and scenarios (the Bernanke review of 2024);
- telling uncertainty: a fan chart from the forecasters' own record around their latest forecast; calibrated
  language; the Dial of forecast errors by horizon (new); *Called it?*: Claudia Sahm in August 2024 (right); and the
  frontier: language models as forecasters, real-time distributional accounts.

## Build it

```bash
python -m videos.economics.econ57.compute              # every number (under a minute), into .cache/econ57/
python tools/qa_scene.py econ57 Nowcast                # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ57 -q l   # the whole part, silent preview
python tools/build.py econ57                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 57                     # the lab
```

The data are the Philadelphia Fed's Real-Time Data Set for Macroeconomists (real GDP, first and latest estimates and
every vintage of 2006-2010), its Survey of Professional Forecasters (every median growth forecast and probability of
decline since 1968) and its Greenbook data set; and FRED's PAYEMS, PAYNSA, GDPC1, INDPRO, GDPDEF, GS10, TB3MS, USREC,
UNRATE, SAHMREALTIME and USEPUINDXM, all registered in [`SOURCES.md`](../../../explainer/economics/data/SOURCES.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Nine of the last five recessions | Two scorecards; the question; objectives |
| 1 | How a number is made | Estimates and benchmarks; first against latest since 1965; 2008Q4 by vintage |
| 2 | Seasonal adjustment | Unadjusted payrolls; a simplified X-11; what it can invent, and the fix |
| 3 | Play it: nowcast the quarter | An Island quarter release by release |
| 4 | Nowcasting | Bridge equations on American data; a factor model and the Kalman filter; news |
| 5 | The yield curve and the Sahm rule | The probit since 1959; inversions; Sahm in real time; 2022-24 |
| 6 | Scoring forecasts | Bias, RMSE, Diebold-Mariano; the SPF by horizon against two benchmarks |
| 7 | The record | The staff against the market on inflation; the forecasters before recessions; 2008 and 2021 |
| — | Intermission | The anxious index, 1968-2026, as a line and a tune; the story so far |
| 8 | Why recessions are hard to forecast | Hamilton's regimes; the best forecast never says recession; reflexivity |
| 9 | New data | Delays by source; online prices, card payments, night lights, job postings |
| 10 | Text as data | The policy-uncertainty index; FOMC transcripts; from counts to embeddings |
| 11 | Judgment, models and combinations | Bates and Granger on the staff and the market; scenarios; the Bernanke review |
| 12 | Telling people about uncertainty | A fan chart from the record; words and numbers |
| 13 | The Dials | Forecast errors by horizon (new) |
| 14 | In practice: this is the job | A forecasting desk's week; *Called it?*: Sahm, 2024 |
| 15 | Frontier | Language models as forecasters; real-time distributions; official statistics rebuilt |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 58, *Scoring the Bill* |

## What is computed, and from what

Everything plotted is computed by `compute.py` with Agora's `nowcast` module (`explainer.economics.agora.nowcast`);
the narration states the cached numbers.

- **Revisions.** Annualized growth of real GDP (GNP before 1992) in the first vintage that reported each quarter and
  in the latest (2026Q4), 1965Q4-2026Q3.
- **Seasonal adjustment.** Logs of unadjusted payrolls; trend by a centred 2x12 moving average; seasonal factors by
  3x3 averages of each calendar month's seasonal-irregular values, centred; the outlier step leaves out values more
  than 2.5 robust standard deviations (1.4826 times the median absolute deviation) from the seasonal, three times.
- **The Island.** f_t = 0.6 f_{t-1} + eta_t; indicators x_it = lam_i f_t + e_it with loadings 1.0, 0.8, 0.7, 0.5 and
  noise s.d. 0.6, 0.7, 0.8, 1.0; GDP growth 2 + 3 x (the quarter's average factor) + noise of s.d. 0.8; 400 quarters,
  scored from the twentieth; the Play-it quarter is the first after the fortieth to fall while the nowcast before it
  was above 1%.
- **Bridge equations.** GDP growth on the quarterly averages of annualized monthly log growth of payrolls and
  industrial production, refitted each quarter on the past; months not yet out filled by each indicator's AR(1);
  1985Q1-2026Q3, 2020Q2-Q3 left out of the averages.
- **Signals.** A probit of the NBER recession indicator twelve months ahead on the 10-year minus 3-month spread,
  1959-2026, by Newton's method; the Sahm rule as FRED computes it in real time (SAHMREALTIME) and on today's
  unemployment rates, with a signal when it first reaches 0.5 and re-arms below 0.1.
- **Scoring.** SPF median forecasts (DRGDP2-6) against first estimates; benchmarks: the average of the previous 40
  quarters' first estimates and the previous quarter's first estimate, both known at the survey; Diebold-Mariano with
  Newey-West standard errors (h + 1 lags); 2020Q2-Q3 left out unless stated.
- **The staff against the market.** For each quarter, the Greenbook closest to the middle of its second month,
  against the SPF's GDP-price inflation forecasts, scored against today's GDP deflator, 1968-2020.
- **Regimes.** Growth mu_s + 2 eps with mu = 3 in expansion and -3 in recession, staying probabilities 0.95 and 0.75;
  4,000 quarters; Hamilton's filter on growth alone.

## Problems and solutions

**1.** *Diebold and Mariano: why does the test for forecasts h quarters ahead need a standard error that allows for
h - 1 lags of autocorrelation?*

*Solution.* A forecast made at t for t + h and the one made at t + 1 for t + h + 1 share the shocks of quarters t + 2
to t + h, so even optimal h-step errors follow an MA(h - 1). The loss differential inherits that dependence, and its
mean's variance is the long-run variance, not the variance over n; Newey and West's estimator with at least h - 1
lags (here h + 1) provides it. Ignoring it overstates the test's significance.

**2.** *Bates and Granger: derive the weight that minimizes the variance of w e_1 + (1 - w) e_2, and evaluate it for
errors of s.d. 0.99 and 1.02 with correlation 0.73.*

*Solution.* The variance is w^2 s_1^2 + (1 - w)^2 s_2^2 + 2 w (1 - w) s_12; setting its derivative to zero gives w* =
(s_2^2 - s_12)/(s_1^2 + s_2^2 - 2 s_12). With s_12 = 0.73 x 0.99 x 1.02 = 0.737: w* = (1.040 - 0.737)/(0.980 + 1.040 -
1.474) = 0.55, and the combined error's root mean square is 0.93, below both: the film's current-quarter inflation
forecasts.

**3.** *Pseudo real time: why is a nowcast scored on today's revised data, with the release calendar imposed, likely
to look better than it was?*

*Solution.* The indicators it uses have since been revised toward the truth, and the GDP it is scored against is the
latest estimate, with which today's indicators are more consistent than the first releases were. The model's
specification and coefficients may also have been chosen knowing how the history turned out. A real-time evaluation
uses each vintage as it was, and scores against the first or a fixed later release.

**4.** *The Sahm rule on today's data fired in 2003; in real time it did not. Give two reasons the two can differ.*

*Solution.* The unemployment rate is revised, mostly through new seasonal factors each January and population
controls, so the three-month averages and their twelve-month low change. And today's series has had its seasonal
factors re-estimated with data after the date, which shifts small movements around the 0.5 threshold.

**5.** *A minister asks: 'will there be a recession next year?' Write the three-sentence answer this part's Dial
allows.*

*Solution.* For example: 'Our central forecast is growth of about two percent, but a year ahead our forecasts have
missed by about three points on average, so a fall cannot be ruled out; in the past a little over one quarter in ten
has seen output fall. No reliable signal is warning of one now, and the signals that exist have given false alarms.
We will know much more within each quarter, as the monthly data arrive, and we will tell you as soon as they move.'

**6.** *Hamilton: with expansions that persist with probability 0.95 a quarter and recessions with 0.75, find the share
of time in recession and the average length of each regime.*

*Solution.* The stationary probability of recession is (1 - 0.95)/((1 - 0.95) + (1 - 0.75)) = 0.05/0.30 = 1/6. A
regime that persists with probability p lasts 1/(1 - p) quarters on average: expansions 20 quarters (five years),
recessions 4 quarters (a year). The simulation's share, 18%, is close.

## Lab and interactive

- `python -m videos.economics.labs 57`: revisions and the 2008Q4 path; payrolls adjusted by the simplified X-11, with
  and without the outlier step; Island nowcast errors by release; American bridge equations; the yield-curve probit;
  the Sahm rule in real time; the SPF scored by horizon; the staff against the market; Hamilton's economy.
- The interactive (course site): nowcaster. The reader sets a nowcast of an Island quarter's growth after each of
  five releases, sees the indicators fill in, can compare with the model's Kalman-filter nowcast, and is scored
  against the truth when the quarter ends.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[57]`; the new Dial of forecast errors
by horizon is in `explainer/economics/dials.py`, and the *Called it?* record of Claudia Sahm's 2024 call in
`explainer/economics/calls.py`. The models are stated from the papers cited in the chapters (Bates and Granger 1969,
Shiskin, Young and Musgrave 1967, Lucas 1976, Mankiw and Shapiro 1986, Hamilton 1989, Diebold and Mariano 1995,
Estrella and Mishkin 1998, Romer and Romer 2000, Stock and Watson 2002 and 2004, Giannone, Reichlin and Small 2008,
Henderson, Storeygard and Weil 2012, Baker, Bloom and Davis 2016, Cavallo and Rigobon 2016, An, Jalles and Loungani
2018, Hansen, McMahon and Prat 2018, Gentzkow, Kelly and Taddy 2019, Sahm 2019, Blanchet, Saez and Zucman 2022,
Bernanke 2024, Chetty et al. 2024, Halawi et al. 2024) and computed here.
