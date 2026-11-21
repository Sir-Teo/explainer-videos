# Economics, Built: Part 58, Scoring the Bill

Part 58 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second of Act XI, *Economics at Work*. It asks how a government decides whether a
project or a law is worth it. Its answer: by adding up, in money, what the change does to everyone it touches,
against what would have happened anyway, with the future discounted and people's responses allowed for. The method is
old and sound; its inputs are forecasts, prices for things no market sells, and a discount rate that is partly ethics.
So show the ranges, take the outside view, and score the forecasts afterwards.

It opens on the sentence of the Flood Control Act of 1936 that made the Army's engineers build only where "the
benefits to whomsoever they may accrue are in excess of the estimated costs", and on Jules Dupuit's question of 1844,
what a bridge is worth. The Island has a case: a bridge across the strait, where Bo's ferry runs now. From there it
covers:

- the steps of an appraisal: options and the counterfactual (the ferry keeps running), standing (Bo counts), impacts,
  values, discounting, sensitivity; the bridge's ledger for a year (millions of Island dollars: time on today's 0.84
  million crossings 5.4, fares no longer paid 3.4, new crossings 4.3, Bo's lost profit -1.5, 0.12 fewer deaths a year
  1.1; 300 to build over three years, 1.2 a year to keep, noise for 200 homes);
- valuing what has a price: Dupuit's surplus on the demand for crossings (a generalized cost of 12 on the ferry, 4 of
  fare and 8 of time, against 1.6 on a free bridge), the rule of a half for new trips, transfers that net out (fares
  saved and Bo's lost profit leave the ferry's running costs, 1.86 a year); the shadow wage (if half the labour would
  be idle, the cost falls by 30 and the net present value rises from 77 to 106) and the marginal cost of public funds
  (Norway's 20%: the NPV falls to 13);
- valuing what has none: time at half the hourly wage (the US Department of Transportation's rule for personal
  travel); road noise priced from 3,000 Island house sales (on noise alone, +0.28% a decibel; with the harbour and
  rooms held fixed, -0.75%, against -0.7% planted); a beach valued by the trips to it from ten villages (about 760,000
  a year beyond their cost); stated preference: the Exxon Valdez survey (about $3 billion), willingness to pay of $80,
  $78 and $88 for 2,000, 20,000 and 200,000 birds, the NOAA panel and Diamond and Hausman;
- a statistical life: Schelling's arithmetic; the wage premium for risk on 100,000 Island jobs (3.5 million on risk
  alone, 9.2 with ability held fixed, against 9 planted, 6.5 with risk mismeasured); Part 18's Dial; the life-year
  (0.59 million at the Department of Transportation's 13.7) and the "senior discount" of 2003;
- Play it: a top rate raised from 40% to 45% above 150,000, scored on a weighted survey of 44,154 records for
  400,000 taxpayers: 143 million statically, 101 million with an elasticity of taxable income of 0.25 (71%, against
  Saez's 1 - e a t/(1 - t) = 0.69); 60 million would need an elasticity of 0.5, and nothing one of 0.89;
- discounting: a dollar in thirty years at 2%, 3.5% and 7% (55, 36 and 13 cents); the bridge's NPV against the rate
  (+139 at 3%, +77 at 3.5%, -118 at 7%; an internal rate of return of 4.4%); the Green Book's Ramsey rate, 0.5% +
  1.0% + 1.0 x 2.0% = 3.5%, its declining schedule, and the 3.00% for years 1 to 30 the Treasury accepted in October
  2026; OMB's 7% and 3% (2003), 2.0% (2023), and the 2003 rates reinstated in 2025; Weitzman's declining rate; the
  market's real rate (10-year TIPS, 0.97% on average, 2003-2025);
- scoring a bill: the baseline; static, conventional and dynamic scores; the ten-year window and sunsets (the 2017
  individual tax cuts, made permanent in 2025); an Island toy in which a tax cut of 1% of GDP a year costs 10.0% over
  the window, growth pays back 0.86 and higher interest rates on all debt add 1.22 (a dynamic score of 10.36); CBO
  on the 2017 act and on the House's 2025 bill; CBO's own record since 1984 (errors of 0.5% of GDP in the first year,
  2.0% by the sixth, 2.3% by the eleventh, once laws passed later are taken out), and May 2001's projected surplus of
  5.7% of GDP for 2011, a deficit of 5.0% with the laws passed later, and 8.4% in fact;
- microsimulation: a survey of 6,000 households grossed up to 176,920 households and 424,505 people; a tax and
  benefit calculator; a higher allowance (cost 114 million; the poorest tenth gains nothing, the middle about 2%);
  paid for by 45% above 80,000 (net cost 17 million; the richest tenth loses 2.8% of net income, three in four of its
  households worse off); TAXSIM, EUROMOD, TAXBEN and the distribution tables;
- general equilibrium: the Island's social accounting matrix; a 10% tax on manufactures moves labour into food,
  raises the wage 1.9% against the return to capital, and costs 0.20 of 11.2 raised (Harberger's triangle, 0.23);
  Kehoe's audit of the NAFTA models;
- risk and the record: Flyvbjerg, Holm and Buhl's 258 projects (rail 44.7% over budget, bridges and tunnels 33.8%,
  roads 20.4%; rail passengers overestimated by 106%); the Island's reference class (70% over budget, a median overrun
  of 14% and an 80th percentile of 53%); with that uplift the bridge's NPV is -76, and drawn from the record its
  forecast +77 becomes a mean of -40 with a 61% chance of losing money; the option to wait (16, or 58 with the usual
  overrun); Hendren and Sprung-Keyser's after-the-fact scores;
- regulatory impact analysis: Executive Orders 12291 (1981) and 12866 (1993), Circular A-4; an Island rule for
  scrubbers (net +71, +59, +25 at 2%, 3% and 7% with a value of a statistical life of 9 million; negative at 5
  million; break-even at 3.6 deaths a year avoided);
- what targets do to numbers: Goodhart and Campbell; a four-hour target on an Island emergency department (within
  target 79% to 91%, a spike in the last quarter-hour from 4% to 16%, the median wait unchanged); England's 2002-2004
  numbers;
- two new Dials (the social discount rate; cost overruns), the scorekeepers at work, *Called it?*: the Sydney Opera
  House estimate of 1957 (wrong), and the frontier: distributional weights and the WELLBY.

## Build it

```bash
python -m videos.economics.econ58.compute              # every number (under a minute), into .cache/econ58/
python tools/qa_scene.py econ58 Priced                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ58 -q l   # the whole part, silent preview
python tools/build.py econ58                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 58                     # the lab
```

The data are the Congressional Budget Office's evaluation files (github.com/US-CBO/eval-projections: every deficit
projection since 1984 with its outcome and legislation-adjusted error, and CBO's summary statistics) and FRED's DFII10,
registered in [`SOURCES.md`](../../../explainer/economics/data/SOURCES.md); the transcribed passages and numbers are in
`explainer/economics/data/tables.py` (`FLOOD_1936`, `VALUES_58`, `STATED_58`, `DISCOUNT_58`, `MEGAPROJECTS`,
`SCORING_58`, `TARGETS_58`, `FRONTIER58`, and Parts 41 and 42's `TCJA_2017` and `MVPF_2020`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | To whomsoever they may accrue | The Flood Control Act; Dupuit; the strait; the question; objectives |
| 1 | The steps of an appraisal | Six steps; the counterfactual and standing; the bridge's ledger |
| 2 | Valuing what has a price | Dupuit's surplus and the rule of a half; transfers; shadow wages; the cost of public funds |
| 3 | Valuing what has none | The value of time; hedonic noise; the travel-cost beach; stated preference and the birds |
| 4 | A statistical life | Schelling's arithmetic; the wage-risk regression and its biases; the Dial; the age question |
| 5 | Play it: the minister's budget | A higher top rate, static and with behaviour, on a weighted survey |
| 6 | Discounting | Discount factors; the bridge against the rate; the Green Book and OMB; Weitzman |
| 7 | Scoring a bill | Baselines and three kinds of score; the window; a dynamic toy; CBO's record |
| — | Intermission | Forty-two CBO baselines against the deficits that happened, as lines and a tune |
| 8 | Microsimulation | A tax and benefit calculator; the distribution table of an allowance and its financing |
| 9 | General equilibrium | A social accounting matrix; a tax on manufactures; Harberger; NAFTA's models audited |
| 10 | Risk, optimism and the record | Megaprojects; the outside view; Monte Carlo; the option to wait; evaluation after |
| 11 | Regulatory impact analysis | Executive orders; an Island rule by discount rate; break-even |
| 12 | What targets do to numbers | Goodhart and Campbell; a four-hour target, gamed |
| 13 | The Dials | The social discount rate (new); cost overruns (new) |
| 14 | In practice: the scorekeepers | Budget offices, ministries, regulators, banks, think tanks; *Called it?*: Sydney, 1957 |
| 15 | Frontier | Distributional weights; the WELLBY; open models; evaluation joined to appraisal |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 59, *The Expert Witness* |

## What is computed, and from what

Everything plotted is computed by `compute.py` with Agora's `appraisal` module
(`explainer.economics.agora.appraisal`); the narration states the cached numbers.

- **The bridge.** Crossings q = 1.8 - 0.08 g (millions a year) at generalized cost g = fare + 12 x minutes/60; the
  ferry 4 and 40 minutes, the bridge free and 8; travellers' gain q0 (g0 - g1) + (q1 - q0)(g0 - g1)/2, split into time,
  fares and new trips; Bo's profit (4 - 1.5) q0 - 0.6 lost; deaths 0.24 and 0.05 per million crossings at a value of
  a statistical life of 9; noise 0.7% a decibel on 200 homes of 0.2 million for 10 decibels, once; construction
  100 a year for three years, upkeep 1.2, a hundred years of use, traffic growing 1% a year for forty years. NPV,
  benefit-cost ratio (Bo's loss and the noise count as costs) and internal rate of return by Brent's method.
- **Hedonic prices.** 3,000 houses: distance to the harbour uniform on 0-5 km; the coast road follows the harbour, so
  noise = 48 + 22 exp(-distance to road/0.5) + noise; log price = log 200,000 + 0.10 (rooms - 4) - 0.06 x harbour km
  - 0.007 (dB - 50) + e (s.d. 0.12); least squares with HC1 errors, with and without the harbour and rooms.
- **Travel cost.** Ten villages 1 to 16 km away; a trip costs 2 x km x (0.3 + 12/30); visits per resident 6 - 0.25 x
  cost + noise; the fitted line is the demand curve; each resident's surplus is the triangle above their cost.
- **Wage and risk.** 100,000 workers; ability N(0, 1); risk (deaths per 10,000 a year) max(0, 1 - 0.015 x ability +
  0.5 x noise); pay 30 + 8 x ability + 0.9 x risk + N(0, 3), in thousands; risk mismeasured with noise of s.d. 0.3.
- **The Play it.** 400,000 incomes, log-normal (median 38,000, log-s.d. 0.7) with a Pareto tail of exponent 1.5 above
  150,000; a survey of one in ten below and one in two above, weights 10 and 2; incomes above the threshold move as
  z ((1 - 0.45)/(1 - 0.40))^e, no lower than 150,000.
- **Discounting.** Constant rates; the Green Book's 2003 schedule (3.5% to year 30, then 3.0, 2.5, 2.0, 1.5, 1.0%);
  Weitzman's certainty-equivalent factor (1.01^-t + 1.07^-t)/2.
- **Scoring.** The dynamic toy: a cut of 1% of GDP a year; output rising towards 0.4% at a quarter of the gap a year,
  taxed at 30%; interest rates rising 0.025 points for each point of debt to GDP added, on a debt of 100% of GDP. CBO's
  errors are its own (outcome minus the projection adjusted for later laws, in percent of GDP), averaged by year of the
  projection; the averages reproduce CBO's published summary.
- **Microsimulation.** 6,000 households, one or two adults (each earning log-normally around 32,000, one in six not
  working), up to three children; weights 25 and 35; individual income tax (15,000 free, 20% to 50,000, 35% to
  150,000, 40% above); 1,000 a child; a credit of 3,000 for families, withdrawn at 30% above 20,000; deciles of net
  income over the square root of household size.
- **General equilibrium.** Labour 100 and capital 100; Cobb-Douglas technologies with labour shares 0.6 (food) and 0.4
  (manufactures); a household spending 40% on food; capital's price the numeraire; the wage found by Brent's method;
  the loss is the equivalent variation at untaxed prices; Harberger's triangle uses the compensated elasticity 0.4.
- **Risk.** Sixty past projects, outturn over forecast log-normal with means 1.28 (costs, s.d. 0.39) and 0.90
  (traffic, s.d. 0.25); 4,000 Monte Carlo draws; the option to wait between traffic 30% above and 30% below.
- **The rule.** 60 up front, 40 a year for 20 years; 4 deaths a year avoided; 0.1 million tonnes of CO2 at 120 a tonne.
- **The target.** 20,000 patients, minutes log-normal (median 160, log-s.d. 0.5); under the target, those who would
  breach it by under two hours are moved, with probability 0.8, into the last fifteen minutes.

## Problems and solutions

**1.** *The rule of a half: with linear demand, show that the gain on new trips is exactly ½(q1 - q0)(g0 - g1), and
that it is an approximation otherwise.*

*Solution.* Travellers' gain is the area under the demand curve between the two costs, the integral of q(g) from g1 to
g0. With linear demand that area is a trapezoid, (g0 - g1)(q0 + q1)/2 = q0 (g0 - g1) + ½(q1 - q0)(g0 - g1): the
rectangle on existing trips plus a triangle on the new ones. With a curved demand the area between the curve and the
chord differs from zero, so the rule of a half over- or understates the gain on new trips, by more the larger the
change in cost.

**2.** *Bo's fares: show that counting travellers' fare savings and Bo's lost profit nets to the ferry's operating cost.
When would it not net out?*

*Solution.* Travellers save the fare f on each of the q0 crossings; Bo loses his profit (f - c) q0 - F. The sum is
f q0 - (f - c) q0 + F = c q0 + F, the variable and fixed costs of running the ferry, which the bridge frees for other
uses: 1.5 x 0.84 + 0.6 = 1.86 a year. It does not net out if Bo has no standing (say, a foreign operator), if part of
the fare is a tax (then the tax is a transfer to the government, which also has standing, and still nets), or if the
ferry's resources have no other use, when their shadow price is below their cost.

**3.** *Saez's ratio: derive 1 - e a t/(1 - t) for a small rise in a top rate on a Pareto tail with exponent a.*

*Solution.* Raising the top rate by dt raises, mechanically, dt times the income above the threshold: N (z_m - z̄) dt,
where z_m is the mean top income. Each top taxpayer's income responds by dz = -e z dt/(1 - t), and each dollar lost
costs the government t: a behavioural loss of t N z_m e dt/(1 - t). Their ratio is e (t/(1 - t)) z_m/(z_m - z̄), and
for a Pareto tail z_m/(z_m - z̄) = a. Revenue with behaviour over the static score is therefore 1 - e a t/(1 - t);
with e = 0.25, a = 1.5 and t = 0.45, 0.69.

**4.** *Weitzman: with rates of 1% and 7% equally likely, find the certainty-equivalent rate at 50 and 200 years.*

*Solution.* The certainty-equivalent factor is the average, (1.01^-t + 1.07^-t)/2: at 50 years (0.608 + 0.034)/2 =
0.321, a constant rate of 0.321^(-1/50) - 1 = 2.30%; at 200 years (0.137 + 0.0000013)/2 = 0.068, a rate of 1.35%. The
rate from year 200 to 201 is already 1.00%: far out, only the low-rate world still counts.

**5.** *A regulation prevents an unknown number of deaths. Write the break-even sentence its analysis should contain,
and say why it is more honest than a point estimate.*

*Solution.* For the Island's rule: "The rule costs 655 million in present value, less 179 million of carbon benefits;
at a value of a statistical life of 9 million and a 3% discount rate, it is worth its cost if it prevents more than
3.6 deaths a year. Our best estimate is 4." A point estimate of net benefits buries the most uncertain input, the
deaths avoided, inside a precise-looking total; the break-even puts it in front of the reader, who can judge it
against the epidemiology.

**6.** *Option value: with traffic 30% above or below the forecast next year, find the cost overrun at which waiting
becomes worth more than building now.*

*Solution.* Building now is worth the average of the two outcomes, (N_H + N_L)/2; waiting a year and building only if
traffic is high is worth (N_H/2)/(1 + r) when N_L < 0. Waiting wins once N_L < -N_H r/(1 + r). Both values fall with
the cost ratio c at the present value of construction, 290 million per unit of c; solving at 3.5% gives c = 0.89.
So at the forecast cost (c = 1) waiting is already better, by 16 million, and any overrun widens the gap: the
bridge's low-traffic case loses money, and the year of information is worth more than the year of crossings.

## Lab and interactive

- `python -m videos.economics.labs 58`: the bridge's ledger, NPV by rate and IRR; the tornado; the hedonic and
  travel-cost estimates; the wage-risk regressions; the Play-it score and its elasticity curve; Weitzman's rates;
  the dynamic toy; the distribution tables; the CGE's loss against Harberger's triangle; the reference class and
  the Monte Carlo NPV; CBO's errors by horizon.
- The interactive (course site): appraiser. The reader sets the discount rate, the value of time, the cost overrun
  and the traffic, watches the bridge's NPV, benefit-cost ratio and ledger move, decides whether to build, and then
  draws an outturn from the Island's reference class to see how the decision would have turned out.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[58]`; the new Dials (the social discount
rate; cost overruns) are in `explainer/economics/dials.py`, and the *Called it?* record of the Sydney Opera House
estimate in `explainer/economics/calls.py`. The methods are stated from the works cited in the chapters (Dupuit 1844,
Hotelling 1947, Orcutt 1957, Harberger 1962, Schelling 1968, Rosen 1974, Goodhart 1975, Thaler and Rosen 1976,
Campbell 1979, Kahneman and Lovallo 1993, Diamond and Hausman 1994, Weitzman 1998 and 2001, Saez 2001, Flyvbjerg,
Holm and Buhl 2002 and 2005, Viscusi and Aldy 2003, Auerbach 2005, Kehoe 2005, Bevan and Hood 2006, Boardman et al.
2018, Drupp et al. 2018, Hendren and Sprung-Keyser 2020) and computed here.
