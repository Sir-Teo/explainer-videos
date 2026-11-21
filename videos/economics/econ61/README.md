# Economics, Built: Part 61, Economics at the Platforms

Part 61 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth of Act XI, *Economics at Work*. It asks what the economists inside
technology companies do. Its answer: they design markets that a company owns (the commission, the surge, the ranking,
the ratings, the ad auction); they measure what those choices do, mostly by experiment, and catch the ways experiments
mislead (peeking, interference, effects that change with time); and they ask the questions engineers do not: is it
caused, what does the other side do, and whose welfare is it?

It opens on New Year's Eve 2014 in New York, when a fault switched off a ride-hailing app's surge pricing for
twenty-six minutes: about a quarter of requests were completed, against nearly all of them after a sold-out concert at
Madison Square Garden with surge working (a case study by the company's own economists). The Island's app has its own
New Year's Eve. From there it covers:

- the Island's night: requests spike at midnight to more than five times the usual rate; with surge off, about 27% of
  requests are filled at the peak; with it on, the fare rises to 2.8 times normal, fewer riders request, more drivers
  come out a few minutes later, and every request is filled;
- a platform as a designed market (Parts 17 and 44): prices, matching, information and rules; theory, measurement and
  experiments (Athey and Luca 2019);
- Play it: the commission in a two-sided market with a $20 fare (10%: $352 an hour for the platform; 20%: $562;
  30%: $622; 45%: $479); the platform's best is 29%, and moving from 10% to 30% gains it $270 an hour while riders and
  drivers lose $1,270, because each driver who leaves lengthens every rider's wait;
- surge pricing as market clearing (at the peak minute, 340 requests and 70 drivers at the normal fare; the clearing
  fare is 2.1 times normal, with 121 rides a minute); consumer surplus from random surge levels ($1.42 per dollar on
  the Island; about $1.60 for UberX in Cohen, Hahn, Hall, Levitt and Metcalfe 2016, with elasticities mostly between
  -0.4 and -0.6); the 2014 emergency cap agreed with New York's attorney general;
- search and ranking: position alone gives the top slot 3.3 times the fifth's attention; a sponsored listing in the top
  slot cuts clicks per search from 2.05 to 1.84; Ursu's randomized rankings; the Google Shopping decision (2017, upheld
  in 2024);
- reputation: percent positive has a median of 99.1% on the Island (84% of sellers at 98% or more), the effective
  percent positive spreads sellers out and tracks quality better (correlation 0.68 against 0.51); Nosko and Tadelis on
  eBay; Airbnb's simultaneous reviews (Fradkin, Grewal and Holtz);
- ad auctions in practice: quality scores (revenue $1.005 a search against $0.970 by bid alone, with more clicks); a
  reserve; Yahoo!'s reserve-price experiment; the move to first price; auto-bidding;
- does advertising work? On the Island the dashboard reports a return of +1,238%, a regression +2,607%, the truth is
  -64%, and an experiment switching ads off in 30% of 210 regions recovers it (spread about 32 points); eBay's
  experiment (-63%, interval -124% to -3%, against over 1,400% without it); Lewis and Rao's arithmetic (5.7 million
  people an arm to detect a campaign at all, 141 million to tell a 25% return from zero); *Called it?*: Google's advice
  on measuring AdWords returns (wrong);
- an intermission: online sales' share of American retail, quarterly since 1999 (0.6% to 17.9%), as a line and a tune;
- experiments at scale: A/A tests read every day declare a winner 27% of the time against 5% read once; CUPED cuts the
  variance to 0.54 of the plain estimator's (theory 0.51); the habits of an experimentation platform;
- interference: a rider discount with shared drivers; an A/B test by user finds +18.0 rides per 100 riders, the truth is
  +6.7, a switchback +6.7 and a test by city +6.8 (noisier); two-sided randomization;
- causal machine learning: coupons to the likeliest buyers yield -0.7 purchases per 100, at random +6.1, by estimated
  effect +12.2 (truth +12.9); the gains curve; a discount that raises the first month's orders by 41% and lowers the
  year's by 3.1%, which the surrogate index (Athey, Chetty, Imbens and Kang) predicts after eight weeks (-3.4%);
- the gig economy: flexible hours worth 3.3 times a fixed shift's surplus on the Island ($54 against $16 a day); Chen,
  Chevalier, Rossi and Oehlsen; Cook and coauthors' 7% gender gap among a million drivers; AB5, Proposition 22 and
  *Uber v Aslam*;
- data, attention and free goods: a willingness-to-accept survey puts the median value of free search at $14,171 (planted
  $15,000); Brynjolfsson, Collis and Eggers ($17,530 a year for search engines, $8,414 for email, $3,648 for maps);
  the privacy paradox;
- the Dials (the elasticity of rides to the surge price, new; the return on search advertising, new; what a reserve
  price adds, Part 16's), economists in tech, and the frontier: markets of agents, recommendation and welfare.

## Build it

```bash
python -m videos.economics.econ61.compute              # every number (under a minute), into .cache/econ61/
python tools/qa_scene.py econ61 PlayIt                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ61 -q l   # the whole part, silent preview
python tools/build.py econ61                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 61                     # the lab
```

The data are FRED's e-commerce share of retail sales (ECOMPCTSA, from the Census Bureau), registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md). Everything else is computed on the Island, or stated from
the papers listed in `dials.SHOWN[61]`.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Twenty-six minutes | New Year's Eve 2014; the Island's night with surge off and on; the question; objectives |
| 1 | A platform is a designed market | Prices, matching, information, rules; theory, measurement, experiments |
| 2 | Play it: set the commission | Four commissions in a two-sided market; the platform's best against everyone's |
| 3 | Surge pricing | Market clearing at the peak; consumer surplus from random surge levels; the emergency cap |
| 4 | Search and ranking | Position against relevance; a sponsored top slot; self-preferencing |
| 5 | Reputation | Percent positive against effective percent positive; simultaneous reviews |
| 6 | Ad auctions in practice | Quality scores; reserves; first price; auto-bidding |
| 7 | Does advertising work? | Attribution, regression and experiment; eBay; Lewis and Rao; *Called it?* |
| — | Intermission | Online sales' share of American retail since 1999, as a line and a tune |
| 8 | Experiments at scale | Peeking; CUPED; the habits of an experimentation platform |
| 9 | When units interfere | By user, switchback and city designs with shared drivers |
| 10 | Causal machine learning in production | Uplift targeting; the gains curve; the surrogate index |
| 11 | The gig economy | The value of flexible hours; drivers' data; the law |
| 12 | Data, attention and free goods | A willingness-to-accept survey; what free goods are worth; privacy |
| 13 | The Dials | Rides' elasticity to surge (new); the return on search ads (new); reserves (Part 16's) |
| 14 | In practice: economists in tech | The roles; three questions for every number |
| 15 | Frontier: markets of agents | Search by agents; recommendation and welfare; open questions |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 62, *Inside the Firm* |

## What is computed, and from what

Everything plotted is computed by `compute.py` with Agora's `platform` module (`explainer.economics.agora.platform`);
the narration states the cached numbers.

- **The night.** Requests a minute 60, plus 280 decaying from midnight with a 40-minute time constant; requests fall as
  e^(-0.9 (m - 1)) with the multiplier m; drivers 70 + 45 (m - 1), responding with a six-minute lag; with surge, m
  solves requests = drivers each minute (capped at 4).
- **Surge's surplus.** 200,000 sessions at surge levels 1 to 2.5 times a $15 fare; a rider books with probability
  e^(-fare/25); the demand curve fitted by least squares on log booking rates.
- **The commission.** 1,000 riders an hour ride with logit probability in 3.5 - 0.08 fare - 0.8 wait; the wait is
  2 + 3 u/(1 - u) minutes at utilization u = trips/(2 drivers); 2,000 potential drivers drive with logit probability in
  (hourly earnings - 20)/2; each commission's equilibrium by nested root-finding; surplus by logit inclusive values.
- **Ranking.** Ten listings with relevance drawn from a Beta(2, 3); attention k^(-0.75) at position k; clicks are
  attention times relevance; the sponsored listing is the sixth by relevance.
- **Reputation.** 2,000 sellers good 80% to 99% of the time, 200 sales each; happy buyers rate positively 60% of the
  time, unhappy ones negatively 5%.
- **Ad auctions.** Bids 4, 3, 2.5 and 1; qualities 0.5, 1, 0.7 and 0.9; three slots with click rates 30%, 18% and 10%
  times quality; prices are the next score over the winner's quality, and at least the reserve.
- **Search ads.** 210 regions, 16 weeks; 40% of searchers are regulars who buy 30% of the time; the rest buy 2% of the
  time, 2.3% after seeing the ad; half of searchers click an ad when shown, at 50 cents; each searcher spends $50 with
  log-normal noise (s.d. 0.15) by region and week; ads off in a random 30% of regions for the last eight weeks; 200
  runs.
- **Experiments.** A/A tests of a 5% conversion rate, 2,000 users a day an arm for 30 days, 2,000 runs; CUPED with a
  pre-period correlation of 0.7, 20,000 users a test, 1,000 runs.
- **Interference.** 20 cities with sizes and drivers per rider varying by city, 48 hours, 300 riders a city-hour wanting
  a ride with probability 0.5 (0.7 with the discount), drivers Poisson with mean 170 times the city's factors, and
  rides shared at random among those who want one; 400 runs of each design.
- **Uplift and surrogates.** 50,000 customers with effects 0.06 (1 - x), x standard normal, estimated with noise
  (s.d. 0.03); a coupon budget of 30%. The discount: first-month orders and second-month sessions Poisson, with the
  year's orders Poisson in 0.5 + 1.2 orders + 0.6 sessions; the index fitted on 40,000 untreated customers.
- **Flexibility.** 5,000 drivers with reservation wages normal around a personal level (mean $25, s.d. $6) with hourly
  shocks (s.d. $9); pay $20 an hour; the best eight-hour shift or none.
- **Free search.** 4,000 respondents with log-normal values (median $15,000, log-s.d. 1.3) offered sums from $100 to
  $1,000,000 at random on a log scale; a logit of acceptance on the log of the offer.

## Problems and solutions

**1.** *Surge: with requests 340 e^(-0.9 (m - 1)) and drivers 70 + 45 (m - 1) at multiplier m, find the clearing
multiplier, and show that rides rise when the fare does.*

*Solution.* Solve 340 e^(-0.9 (m - 1)) = 70 + 45 (m - 1). The left side falls and the right rises in m, so there is one
root; numerically m is about 2.14, where both sides are about 121. At m = 1 only 70 rides happen (all the drivers there
are), so rides rise from 70 to 121 a minute: the higher fare rations requests and brings out drivers.

**2.** *Surplus: if a rider books with probability e^(-p/mu), show that consumer surplus per trip is mu, and find surplus
per dollar at mu = 25, p = 15.*

*Solution.* Booking with probability e^(-p/mu) means values are exponential with mean mu. Given that a rider books, the
value exceeds the fare by an exponential amount with the same mean (the exponential has no memory), so surplus per
trip is mu = $25. Per dollar of fare it is mu/p = 25/15, about 1.67. The Island's 1.42 averages over sessions at
higher surge, where the fare is larger and the ratio smaller.

**3.** *Quality scores: bids 4, 3, 2.5, 1 and qualities 0.5, 1, 0.7, 0.9 for three slots: rank by bid x quality and find
each winner's price per click.*

*Solution.* Scores are 2.0, 3.0, 1.75 and 0.9, so the order is B, A, C, and D gets nothing. Each pays the least bid that
keeps its rank: the next score over its own quality. B pays 2.0/1 = $2.00; A pays 1.75/0.5 = $3.50; C pays
0.9/0.7, about $1.29. A, the highest bidder with the worst ad, ranks second and pays the most per click.

**4.** *Interference: 300 riders, 170 drivers; riders want a ride with probability 0.5, 0.7 with a discount. Half get it:
what does the A/B test estimate, and what is the true effect?*

*Solution.* With half discounted, about 105 + 75 = 180 riders want a ride and 170 drivers serve a random 170/180 of
them, so the treated ride at 0.7 x 0.944 = 0.661 and the controls at 0.5 x 0.944 = 0.472: the test estimates about
+0.19 rides per rider. The true effect compares everyone discounted (210 want, 170 ride: 0.567 per rider) with nobody
(150 want, all ride: 0.5): about +0.067. The test is nearly three times the truth, because the treated riders' extra
rides come mostly from the controls.

**5.** *CUPED: show that subtracting theta (X_B - X_A) with theta = Cov(X, Y)/Var(X) cuts the variance of the
difference by the factor 1 - rho^2.*

*Solution.* Work with Y - theta X for each user. Its variance is Var(Y) - 2 theta Cov(X, Y) + theta^2 Var(X), which is
smallest at theta = Cov(X, Y)/Var(X), where it equals Var(Y) (1 - rho^2). The difference in means of the adjusted
outcome has the same factor, and since X is measured before randomization, the mean of X_B - X_A is zero: the
adjustment removes noise without moving the estimate's centre.

**6.** *The commission: the platform maximizes c F T(c) for fare F and trips T(c). Show that at its best commission
d ln T/d ln c = -1, and explain why drivers' waits enter T'(c).*

*Solution.* The first-order condition is F T(c) + c F T'(c) = 0, that is c T'(c)/T(c) = -1: the elasticity of trips with
respect to the commission is -1 at the optimum, the monopolist's rule with the commission as the price. T'(c) is the
full equilibrium response: a higher commission lowers pay per trip, fewer drivers drive, utilization and waits rise,
and fewer riders ride, which lowers trips per driver again. The feedback through waits makes trips more responsive than
the drivers' decision alone, and it is why the platform's best commission (29% on the Island) costs riders and drivers
far more than it earns.

## Lab and interactive

- `python -m videos.economics.labs 61`: the night with surge off and on; surge's surplus; the commission; ranking and
  reputation; the ad auction; search ads by attribution, regression and experiment; peeking and CUPED; interference;
  uplift and the surrogate index; flexibility; free search; online sales on FRED data.
- The interactive (course site): platform. The reader sets the commission, the fare and drivers' outside wage, and
  watches trips, waits, the platform's take and both sides' surplus move.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[61]`; the new Dials (the elasticity of rides
to the surge price, and the return on search advertising) and the returning reserve-price Dial are in
`explainer/economics/dials.py`, and the *Called it?* record of Google's advice on measuring AdWords returns in
`explainer/economics/calls.py`. The methods are stated from the works cited in the chapters (Rochet and Tirole 2003,
Edelman, Ostrovsky and Schwarz 2007, Varian 2007, Ostrovsky and Schwarz 2009, Deng, Xu, Kohavi and Walker 2013, Blake,
Nosko and Tadelis 2015, Hall, Kendrick and Nosko 2015, Lewis and Rao 2015, Nosko and Tadelis 2015, Cohen et al. 2016,
Einav, Farronato and Levin 2016, Tadelis 2016, Athey, Catalini and Tucker 2017, Ursu 2018, Athey and Luca 2019, Athey,
Chetty, Imbens and Kang 2019, Brynjolfsson, Collis and Eggers 2019, Chen et al. 2019, Allcott et al. 2020, Kohavi, Tang
and Xu 2020, Cook et al. 2021, Fradkin, Grewal and Holtz 2021, Bajari et al. 2023) and computed here.
