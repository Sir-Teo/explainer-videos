# Economics, Built: Part 60, The Price

Part 60 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth of Act XI, *Economics at Work*. It asks how firms actually set prices,
and how much of the theory they use. Its answer: most start from cost and a conventional markup, which is less foolish
than it looks, since the profit curve is flat at the top and the elasticity is never known exactly. Firms that can
learn their demand do better, by choices and experiments, by fences, versions and bundles, and, where capacity is fixed
and time runs out, by revenue management. The theory is used most where the stakes are highest and the data richest.

It opens in 1985, when American Airlines answered People Express's low fares with Ultimate Super Saver fares on a
limited number of seats per flight, chosen by software that forecast which seats would otherwise fly empty; People
Express was sold within two years, and American later put the benefit of yield management at $1.4 billion over three
years. The Island has an airline too: one flight, a hundred seats, sixty days of sales, leisure travellers early and
business travellers late. From there it covers:

- what firms say they do: Hall and Hitch's full-cost pricing (1939) and Blinder and coauthors' two hundred firms
  (1998); the markup rule p = c e/(e - 1) and the flat top of the profit curve (with an elasticity of 2.6, every
  price from 1.45 to 1.9 times cost earns more than 95% of the best); with the elasticity estimated, the textbook
  rule earns 90% of the best on average and 74% in the worst tenth, a fixed 50% markup 98.5%;
- willingness to pay: stated values run high (a median ratio of stated to actual of 1.35 in Murphy and coauthors'
  83 comparisons); Becker, DeGroot and Marschak's lottery; an Island conjoint survey of 400 travellers, 3,200 choices
  fitted by a multinomial logit (wifi worth $11.5, legroom $16.3, a free bag $7.1, against $11.25, $17.50 and $7.50
  planted);
- price experiments: an A/B test of a 10% discount in forty cities of 270 rooms and 600 buyers each finds +9.0
  points, the true effect of discounting for everyone is +4.3, and a test randomized by city finds +4.3; Blake and
  Coey's eBay experiment;
- Play it: three weekly rules for the flight, over 2,000 simulated flights each (start high and cut: $10,337; one
  fare of $150: $12,615; start low and raise: $13,396; the optimum: about $14,400);
- revenue management: Littlewood's rule derived (fares of $400 and $150, business demand Poisson with mean 30:
  protect 32 seats, earning $21,662 against $15,000 first-come first-served); EMSR-b's nested protection levels
  (13, 39 and 83 seats for the top one, two and three of four fares); bid prices on networks; overbooking (109 tickets
  for 100 seats, $19,328 against $18,000, about 0.5 passengers bumped a flight);
- dynamic pricing as dynamic programming (Gallego and van Ryzin): the optimal fare for every day and every number of
  seats left, worth $14,359 against $12,575 for the best single fare; Williams (2022) on who gains;
- versions and menus: good, better, best by Mussa and Rosen's rule for three types (profit 0.667 against 0.5625 for
  one version and 0.9875 with full information); damaged goods (IBM's LaserPrinter E; Deneckere and McAfee);
- an intermission: processed food at the factory gate and food at the grocer's, monthly since 1990;
- bundles, subscriptions and free: Bakos and Brynjolfsson's large bundles (revenue per good rising from 0.25 sold
  separately to 0.43 in a bundle of 100, with 98% of buyers subscribing);
- promotions and reference prices: high-low against everyday low prices with shoppers who value a deal (high-low wins
  once the weight on the deal passes about a third; $1.27 million against $1.15 million a year at 0.8); prices ending
  in nines; StubHub's hidden fees; the FTC's fee rule;
- uniform pricing across a chain (DellaVigna and Gentzkow): on the Island, stores' best prices 17% apart between the
  10th and 90th percentiles of elasticity, and one price gives up 0.7% of profit; in the data, the median chain gives
  up about $16 million a year, and poorer shoppers pay more;
- cost pass-through: food at the grocer's on processed food at the factory gate, monthly 2000-2019 (0.58 after a year,
  s.e. 0.05); from December 2020 to December 2023 the factory gate rose 22.2% and the grocer's 20.6%, against 14.1%
  predicted by the quiet years' relation;
- algorithms and personalized prices (a price for each of two groups: 60 and 40 instead of 50 for both; profit 2,000
  against 1,800); Calvano and coauthors' learning algorithms; *United States v. RealPage*;
- business prices: list prices and negotiated discounts, tenders, and the most-favoured-customer clause (the same two
  groups, forced to one price); *United States v. Apple* (2013);
- the Dials (cost pass-through to retail prices, new; one product's elasticity, revisited), pricing teams,
  *Called it?*: J.C. Penney's fair and square pricing (wrong), and the frontier: Thompson sampling against
  test-then-commit (losses of $12,500 against $19,000 over 20,000 customers), pricing AI services, fairness limits,
  learning algorithms that meet.

## Build it

```bash
python -m videos.economics.econ60.compute              # every number (under a minute), into .cache/econ60/
python tools/qa_scene.py econ60 RM                     # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ60 -q l   # the whole part, silent preview
python tools/build.py econ60                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 60                     # the lab
```

The data are FRED's producer price index for processed foods and feeds (WPU02) and consumer price index for food at
home (CUSR0000SAF11), registered in [`SOURCES.md`](../../../explainer/economics/data/SOURCES.md). Everything else is
computed on the Island, or stated from the papers listed in `dials.SHOWN[60]`.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Ultimate Super Saver | American against People Express; the Island's flight; the question; objectives |
| 1 | What firms say they do | Full cost and fixed markups; the markup rule; the flat top; rules under uncertainty |
| 2 | Measuring willingness to pay | Hypothetical bias; BDM; an Island conjoint survey |
| 3 | Price experiments | A/B tests; interference in a market with scarce rooms; randomizing by market |
| 4 | Play it: a hundred seats, sixty days | Three weekly fare rules, simulated |
| 5 | Revenue management | Littlewood derived; EMSR-b; bid prices; overbooking |
| 6 | Dynamic pricing as dynamic programming | The Bellman equation; the optimal policy; who gains |
| 7 | Versions and menus | Good, better, best; damaged goods |
| — | Intermission | Factory-gate and grocery food prices since 1990, as lines and a tune |
| 8 | Bundles, subscriptions and free | Large bundles; subscriptions; free and freemium |
| 9 | Promotions, reference prices and hidden fees | High-low against everyday low; nines; drip pricing; the fee rule |
| 10 | Why chains charge the same price everywhere | Store-by-store against uniform prices; who pays |
| 11 | Cost pass-through, 2021-22 | A distributed-lag regression; the jump against the old relation |
| 12 | Algorithms and personalized prices | Two groups; learning algorithms; RealPage |
| 13 | Business prices | Negotiation, tenders, most-favoured-customer clauses |
| 14 | The Dials | Cost pass-through (new); one product's elasticity (Part 43's) |
| 15 | In practice: pricing teams | Airlines, retail, software, deal desks; *Called it?*: J.C. Penney, 2012 |
| 16 | Frontier | Thompson sampling; pricing AI services; fairness; algorithms that meet |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 61, *Economics at the Platforms* |

## What is computed, and from what

Everything plotted is computed by `compute.py` with Agora's `revenue` module (`explainer.economics.agora.revenue`);
the narration states the cached numbers.

- **Cost-plus.** Constant-elasticity demand p^(-2.6) and unit cost; the elasticity estimated with log-normal error
  (s.d. 0.35, floored at 1.2), 20,000 draws.
- **Conjoint.** 400 respondents, 8 tasks, 3 fares (price 60 to 180 in steps of 20, three binary features) and none;
  utility -0.08 price + 0.9 wifi + 1.4 legroom + 0.6 bag, none -9, Gumbel errors; multinomial logit by Newton's
  method; willingness to pay by the ratio of coefficients with delta-method errors.
- **Interference.** Forty cities, 270 rooms and 600 buyers each in random order, values log-normal (median 90,
  log-s.d. 0.45), price 100, a 10% discount for a random half; 200 runs.
- **The flight.** 100 seats, 60 days; buyers Poisson, 5 a day in the first 39 days and 4 a day in the last 21, with
  exponential values of mean 90 and 260; daily demand at fare p Poisson with mean lambda exp(-p/mu); the dynamic
  programme on fares from $40 to $500 in steps of $5; the Play-it rules simulated 2,000 times each.
- **Revenue management.** Littlewood with Poisson high-fare demand (mean 30) and plentiful low-fare demand, computed
  exactly; EMSR-b with normal demands (means 15, 25, 40, 60; s.d. 5, 8, 12, 18) for fares 450, 300, 200, 120;
  overbooking with binomial show-ups (0.9), a $200 fare and a $600 bump cost.
- **Menus.** Types 1, 1.5 and 2 with shares 0.5, 0.3 and 0.2; values theta q; cost q^2/2.
- **Bundles.** Values uniform on [0, 1], independent; 20,000 buyers; the best bundle price found by sorting.
- **Reference prices.** 1,000 shoppers with log-normal values (median 42, log-s.d. 0.35); high-low at $50 with a sale
  at $35 every other week; everyday low price $40; 52 weeks.
- **The chain.** 200 stores with elasticities normal around 2.5 (s.d. 0.23) and log-normal sizes; marginal cost 1.
- **Pass-through.** Monthly log changes of CUSR0000SAF11 on the current and twelve lagged log changes of WPU02, by
  least squares with robust errors, 2000-2019; the 2021-23 prediction feeds the actual producer-price changes through
  the fitted coefficients.
- **Bandits.** Six prices from $60 to $160; a customer buys at price p with probability exp(-p/70); Thompson
  sampling with Beta(1, 1) priors; test-then-commit with 1,200 test customers; 40 runs of 20,000 customers.

## Problems and solutions

**1.** *Littlewood: derive the rule P(D_H > y) <= p_L/p_H for the last protected seat, and find y for p_H = 400,
p_L = 150, D_H ~ Poisson(30).*

*Solution.* Consider the y-th protected seat. Selling it now at the low fare earns p_L for certain. Holding it earns
p_H if high-fare demand reaches y, that is with probability P(D_H >= y), and nothing otherwise. So protect it if
p_H P(D_H >= y) >= p_L, and the last seat worth protecting is the largest y for which this holds; equivalently, stop at
the smallest y with P(D_H > y) <= p_L/p_H. Here the ratio is 0.375, and for a Poisson with mean 30 the survival
function falls through 0.375 at y = 32: protect 32 seats.

**2.** *Markups: show that a profit-maximizing price satisfies (p - c)/p = 1/e; with e = 2.6, what share of the best
profit does a 50% markup earn?*

*Solution.* Profit (p - c) q(p) has derivative q + (p - c) q'(p) = 0, so (p - c)/p = -q/(p q') = 1/e. With constant
elasticity 2.6 the best price is 2.6/1.6 = 1.625 times cost. Profit is proportional to (p - c) p^(-2.6): at 1.625 it
is 0.625 x 1.625^(-2.6) and at 1.5 it is 0.5 x 1.5^(-2.6); the ratio is 0.985. The profit function is flat near its
maximum, so a markup a sixth below the best one loses only 1.5% of profit.

**3.** *Overbooking: with 100 seats, show-up probability 0.9, a $200 fare and a $600 bump cost, write the condition
for selling the b-th ticket and find the best b.*

*Solution.* The b-th ticket-holder shows up with probability 0.9 and then pays $200, but if at least 100 of the other
b - 1 have shown up, someone must be bumped at $600. So sell it if 0.9 x 200 >= 0.9 x 600 x P(S_{b-1} >= 100), where
S_{b-1} is binomial(b - 1, 0.9): that is, if P(S_{b-1} >= 100) <= 1/3. The probability is 0.24 at b = 109 and 0.34 at
b = 110, so sell 109 tickets.

**4.** *Bundles: with N goods valued uniformly on [0, 1], explain why the bundle's revenue per good tends to 1/2, and
what happens to deadweight loss.*

*Solution.* A buyer's value for the bundle is the sum of N independent uniforms, with mean N/2 and standard deviation
the square root of N/12. Per good, the mean is 1/2 and the spread shrinks like one over the square root of N, so almost
every buyer values the bundle at nearly N/2. A price a little below N/2, per good a little below 1/2, sells to almost
everyone and captures almost all of the value; the buyers priced out, and so the deadweight loss, vanish as N grows.
Sold separately, each good earns only 1/4 per buyer, at a price of 1/2.

**5.** *Interference: if rooms sell out under both the old price and the discount, what does an A/B test estimate, and
what is the true effect of discounting for everyone?*

*Solution.* If every room is booked either way, a discount for everyone changes nothing about bookings: the true
effect is zero, and the discount only lowers revenue. In the A/B test, the discounted half books more often than the
other half, because they take rooms the other half would have had; the test reports a positive effect. The difference
is pure displacement between the arms, which is why such tests randomize whole markets.

**6.** *One seat left, at most one buyer a day with probability lambda, values exponential with mean mu: show that the
best fare is mu + V_{t+1}, and find the recursion for V_t.*

*Solution.* With one seat, V_t = max_p [lambda e^(-p/mu) p + (1 - lambda e^(-p/mu)) V_{t+1}] = V_{t+1} + max_p lambda
e^(-p/mu) (p - V_{t+1}). The derivative is lambda e^(-p/mu) [1 - (p - V_{t+1})/mu], which is zero at p = mu + V_{t+1}:
the fare is the seat's value tomorrow plus the buyer's mean value. Then V_t = V_{t+1} + lambda mu e^(-1 - V_{t+1}/mu),
starting from V_T = 0 at departure; the fare falls as departure nears, because the option of selling tomorrow is worth
less.

## Lab and interactive

- `python -m videos.economics.labs 60`: the markup rule and the flat top; the conjoint survey; the interference
  experiment; Littlewood, EMSR-b and overbooking; the dynamic programme and the Play-it rules; versions and bundles;
  high-low against everyday low; the chain's uniform price; food pass-through on FRED data; Thompson sampling.
- The interactive (course site): fares. The reader prices the Island's flight week by week, watching seats sold and
  revenue, then compares the result with the optimal policy on the same simulated buyers.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[60]`; the new Dial (cost pass-through to
retail prices) and DellaVigna and Gentzkow's row in the product elasticity Dial are in `explainer/economics/dials.py`,
and the *Called it?* record of J.C. Penney's fair and square pricing in `explainer/economics/calls.py`. The methods are
stated from the works cited in the chapters (Hall and Hitch 1939, Becker, DeGroot and Marschak 1964, Littlewood 1972,
Mussa and Rosen 1978, Belobaba 1987, Smith, Leimkuhler and Darrow 1992, Gallego and van Ryzin 1994, Deneckere and
McAfee 1996, Blinder et al. 1998, Bakos and Brynjolfsson 1999, Murphy et al. 2005, Blake and Coey 2014, DellaVigna and
Gentzkow 2019, Calvano et al. 2020, Blake et al. 2021, Williams 2022) and computed here.
