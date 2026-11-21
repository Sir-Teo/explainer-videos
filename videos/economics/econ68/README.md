# Economics, Built: Part 68, The Dissertation

Part 68 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the last of Act XII, *The Frontier*, and of the series. It asks how a new piece of
economics is made, and answers by making one: from a question that matters and can be answered, data described
before they are used, a design whose threats are written down first, the smallest model that speaks to the
estimates, a counterfactual with its uncertainty, and the honesty to say what the design cannot show. Then it closes
the series' accounts: the Facts, the Dials, the Calls and the Tableau.

It opens with Bastiat's question of 1845, who feeds Paris, and moves to a new city question: on 5 January 2025 New
York began charging $9 (E-ZPass cars, 5 am to 9 pm on weekdays, 9 am to 9 pm at weekends; $2.25 overnight) to drive
into Manhattan below 60th Street, and a year later the state reported 11% fewer vehicles entering (27 million in the
year) and over $550 million of revenue. From there it covers:

- finding a question: important, answerable, not yet answered, and yours; the literature in one page (Vickrey 1963;
  Singapore 1975; London 2003; Stockholm's trial of 2006 and tax from 2007);
- the data: four public MTA datasets (crossings since 2019, zone entries since 2025, miles driven since 2024, bus
  speeds since 2023), each reduced by a recorded query; about 492,000 entries on an average weekday, 56% of them
  cars, pickups and vans; and a file with no before;
- the design: year-on-year differences in differences for the two tunnels into the zone against thirteen directions
  of crossings elsewhere and for bus routes inside against outside the business district, with 2023 and 2024 as
  placebo years; a regression discontinuity in time at 9 pm and 5 am; five threats listed before any estimate (a
  trend, diversion, a smaller dose for tunnel users, other news, retiming);
- Play it: predict the three headline results;
- the estimates: the tunnels' traffic fell 2.6% relative to the other crossings in 2025, but they were already
  losing 1.4% a year in the placebo years, so the charge's effect is about -1.2% (s.e. 0.6); bus speeds inside the
  district rose 1.9% (9.49 to 9.67 mph at the weekday peak), 1.3% more than outside (the placebo year: 0.1%); miles
  driven in the zone fell 3.9%, on its free highways 2.4%; why these differ from the state's 11% (entries are not
  miles; a projection is a different counterfactual; the free bridges are in neither), and what no design here can say;
- the clock: car entries jump 26% at 9 pm when the toll falls (about 2,400 extra cars in the first hour) and fall 31%
  at 5 am when it rises (about 4,400 fewer): retiming, measured;
- an intermission: daily entries into the zone, as a line and a tune;
- the smallest model: a speed-flow curve whose slope, 0.48, comes from the miles and bus-speed changes; a
  constant-elasticity demand for trips with an elasticity of -0.15 at the central assumptions (3 miles in the zone at
  10 mph, time worth $20 an hour, other costs $25); the marginal external cost of a trip, about $2.90 in drivers' time
  alone, and what that leaves out (bus riders, pedestrians, safety, emissions, the peak);
- the counterfactual: the $15 plan paused in June 2024: traffic 5.9% below its uncharged level (90% range 4.5-7.3%),
  trips 2.6% faster, with both the estimates and the assumptions drawn 2,000 times;
- writing it: the introduction as an argument in five paragraphs; two referees and the replies;
- the same paper on the Island: the method finds -4.0% for a true -4% when trends are parallel, -4.3% when 30% of the
  lost trips divert to the comparison crossings, -5.5% when the tolled crossings drift 1.5% a year, and -4.0% again
  once the placebo year is subtracted;
- the series' accounts: the Facts (33 of 36 reproduced by Agora; firm sizes' Zipf law, the asymmetry of the cycle and
  the yield curve's inversions left open); the Dials (93, holding 410 estimates: 20 settled within a range, 35
  depending on the setting, 36 contested, 2 not identified), by act; *Called it?* (65 calls: 12 right, 21 partly right,
  28 wrong, 4 too early to say); the Tableau with every pipe open and four boxes still sealed (expectations,
  institutions, the household's inside, the long-run growth rate);
- who feeds Paris now, and the Queen's question of November 2008, answered as well as the series can;
- twelve open problems, one from each act; and the last market.

## Build it

```bash
python -m videos.economics.econ68.compute              # every number (about a minute), into .cache/econ68/
python tools/qa_scene.py econ68 Estimates              # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ68 -q l   # the whole part, silent preview
python tools/build.py econ68                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 68                     # the lab
```

The data are the MTA's open data on data.ny.gov, reduced to five files in the Data Room (`mta_crossings.csv`,
`crz_daily.csv`, `crz_tod.csv`, `cbd_vmt.csv`, `cbd_bus.csv`; the queries are in the registry and
`data.refresh_mta_congestion()` rebuilds them), registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md), and the facts of the charge and the literature's dates
transcribed in `explainer/economics/data/tables.py` (`congestion_68`, `literature_68`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Who feeds Paris, and who drives into Manhattan? | Bastiat's question; the charge of 5 January 2025; objectives |
| 1 | Finding a question | Four tests; the literature in one page |
| 2 | The data | Four datasets; entries since 2025; crossings since 2019 and a drift before the charge |
| 3 | The design, and its threats | Three designs and their placebos; parallel trends drawn; five threats |
| 4 | Play it: predict the result | Three predictions, then the answers |
| 5 | The estimates, and what they cannot say | Tunnels by month with placebo years; buses and miles; the state's figure |
| 6 | The clock | Discontinuities at 9 pm and 5 am; retiming |
| — | Intermission | Daily entries into the zone, as a line and a tune |
| 7 | The smallest model | The speed-flow curve, the demand elasticity, the marginal external cost |
| 8 | The counterfactual | The paused $15 plan, with its uncertainty |
| 9 | Writing it, and the referees | The introduction as an argument; two referee reports and the replies |
| 10 | The same paper on the Island | The method where the truth is known: parallel trends, diversion, a drift |
| 11 | Agora against the Facts | The scorecard; the three Facts left open |
| 12 | The Dials, final | Statuses by act; *Called it?* scored |
| 13 | The Tableau | Every pipe open; the boxes still sealed |
| 14 | Who feeds Paris now, and the Queen's question | Four layers; the British Academy's letter and the series' answer |
| 15 | Frontier | Twelve open problems, one from each act |
| — | Outro | The answer; twelve lines; problems; reading; the last market |

## What is computed, and from what

Everything plotted is computed by `compute.py` with Agora's `congestion` module
(`explainer.economics.agora.congestion`); the narration states the cached numbers.

- **Crossings.** Weekly sums of the hourly crossings by facility and direction; full weeks only; the average weekday
  of each week; months as the mean of their weeks. Treated: the Queens Midtown Tunnel westbound and the Hugh L. Carey
  Tunnel northbound (toward Manhattan). Controls: both directions of the Bronx-Whitestone, Throgs Neck, Henry Hudson,
  Cross Bay and Marine Parkway bridges, the RFK Bridge's Bronx plaza both ways, and the Verrazzano westbound (13
  directions). Each month's log year-on-year change, treated sum minus control sum; the 2025 mean; the 2023-2024
  placebo mean and spread; the effect net of the placebo mean, with a standard error combining both.
- **Buses.** Miles over hours by month, weekday peak, inside against outside the business district; year on year.
- **Miles.** The GPS-based daily vehicle-miles, zone and excluded roadways, 2025 against the same months of 2024.
- **The clock.** Weekday car entries per ten-minute block, summed over 485 weekdays of 2025-2026 and divided by
  them; lines in log entries fitted within two hours on each side of 9 pm and 5 am; the jump between them; the first
  hour's entries against the left line's prediction.
- **The model.** T(V) = T0(1 + a v^4) anchored at 3 miles and 10 mph; e = dlnT/dlnV = 0.0188/0.0389; V = A P^eta with
  P = toll + value of time x T + other costs; eta from the observed change; the marginal external cost e x T x value
  of time; equilibria at other tolls by bisection. The counterfactual draws both estimates from their standard errors
  and the value of time ($14-24), the miles in the zone (2-5) and the other costs ($15-40) uniformly, 2,000 times.
- **The Island.** 400 simulated cities: two tolled and eight comparison crossings, a shared season and random walk,
  crossing-specific trends and noise, a true effect of -4% from week 104; diversion of 30% of the lost trips; a drift
  of -1.5% a year; the same year-on-year estimator with and without subtracting the year before.
- **The accounts.** `facts.scorecard()`, the Dials by the act of their first part (the plan's acts), the Calls'
  verdicts.
- **The intermission.** Daily entries into the zone (all vehicles), a seven-day average; the melody is one note a
  week.

## Problems and solutions

**1.** *Year-on-year differences: show that comparing each month with the same month a year before removes a seasonal
factor common to both groups, and what it does to a linear trend specific to one group.*

*Solution.* Write log traffic as y = a_g + s_m + b_g t + e for group g, month of year m and time t in years. The
year-on-year change y(t) - y(t - 1) for the same month is b_g + (e_t - e_(t-1)): the season s_m cancels, as does the
level a_g. The difference between groups is b_T - b_C plus noise: a trend specific to one group does not cancel; it
becomes a constant that the placebo years measure.

**2.** *Placebo subtraction: with a group-specific drift delta a year and an effect tau, show that the 2025 comparison
estimates tau + delta and the 2024 placebo delta.*

*Solution.* By problem 1, the treated-minus-control year-on-year change is delta in any year without a charge and
delta + tau in the first year with one. So the 2024 comparison estimates delta, the 2025 comparison tau + delta, and
their difference tau. In New York, -0.026 - (-0.014) = -0.012. The cost is precision: the placebo's noise adds to the
estimate's.

**3.** *The clock: explain why a jump in entries at 9 pm measures retiming, and what extra data would be needed to
count the trips given up.*

*Solution.* Just before and just after 9 pm the same people want to travel, so the jump compares the same demand at
two prices; but someone who would have come at 8:50 can wait ten minutes, so the jump counts trips moved across the
cutoff, not trips lost. To count trips given up one needs total trips over the day against a counterfactual day
without the charge: a before, as the crossings and miles provide, or individual travel diaries.

**4.** *The externality: with T(V) = T0(1 + a v^b), show that V T'(V) = e T with e = b s, and that the marginal
external cost is e x T x the value of time.*

*Solution.* T'(V) V = T0 a b v^b, and T = T0(1 + a v^b), so V T'/T = b a v^b/(1 + a v^b) = b s, where s is the share
of the trip's time due to congestion. One more trip adds T'(V) to the time of each of the V trips, V T'(V) = e T in
all, worth e x T x the value of time. With e = 0.48, T = 18 minutes and $20 an hour, about $2.90.

**5.** *Demand: with V = A P^eta, compute eta from a 3.9% fall in traffic when the full price of a trip rises from
$31 to $39.9.*

*Solution.* eta = dlnV/dlnP = ln(1 - 0.0382)/ln(39.9/31) = -0.0389/0.2523 = -0.154: a 1% rise in the full price of a
trip into the zone cuts trips by about 0.15%.

**6.** *Diversion: if a share d of the trips lost on the tolled crossings appears on the comparison crossings, derive
the bias of the difference in differences, and its sign.*

*Solution.* With treated volume T and an effect tau (in logs), about -tau T trips are lost and -d tau T appear on the
controls, whose volume C rises by a factor 1 - d tau T/C. The comparison's log change rises by about -d tau T/C, so
the difference in differences is tau + d tau T/C = tau(1 + d T/C): biased away from zero, overstating the effect, by a
factor that grows with the share diverted and the tolled crossings' size relative to the controls'.

## Lab and interactive

- `python -m videos.economics.labs 68`: the year-on-year difference in differences with its placebo years; bus speeds
  and miles; the discontinuities at 9 pm and 5 am; the calibrated model and the $15 counterfactual with its
  uncertainty; the Island with diversion and a drift.
- The interactive (course site): congestion. The reader sets the toll, the value of time and the elasticity of time
  with respect to traffic, and sees the traffic, the time per trip, the marginal external cost and the toll that would
  equal it.

## Sources

The studies and records the film states are listed in `dials.SHOWN[68]`; the facts of the charge in
`tables.congestion_68` and `tables.literature_68`. The methods are stated from the works cited in the chapters
(Walters 1961, Vickrey 1963, Small and Verhoef 2007, Angrist and Pischke 2009, Cattaneo, Idrobo and Titiunik 2020,
Thomson 2011, Varian 1997, Cochrane 2005, Shapiro) and computed here.
