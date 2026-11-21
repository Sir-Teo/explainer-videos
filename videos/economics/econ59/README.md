# Economics, Built: Part 59, The Expert Witness

Part 59 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third of Act XI, *Economics at Work*. It asks how economics is used to decide a
merger, and what survives cross-examination. Its answer: economics is used as a prediction, argued before someone who
is not an economist. The law asks whether competition may be substantially lessened; economics answers with a market,
diversion ratios, margins, pass-through and a model. What survives cross-examination is evidence that does not hang on
one specification, one demand curve or one input, and predictions that retrospectives later confirm.

It opens on *FTC v. Staples* (1997): the two biggest office-supply superstore chains said they competed with everyone
who sells a pen, and the Federal Trade Commission answered with their own prices. The Island has its own version: three
superstore chains (Alder in every town, Birch and Cedar in some) and the corner shops, in sixty towns, as a nested
logit with Bertrand pricing, and a proposed merger of Alder and Birch whose true effect is known. From there it covers:

- the price map: Alder's basket costs 94.78 where it is alone and 85.28 where all three chains meet, 11% more; but
  towns with Birch alone are cheaper (83.19) than towns with all three, because the towns with more chains are bigger,
  with dearer rents;
- the law: section 7 of the Clayton Act ("may be substantially to lessen competition"), Hart-Scott-Rodino filings and
  second requests, the burden-shifting of *Baker Hughes*, and *Philadelphia National Bank*'s 30% presumption;
- Play it: three pairs, each with a diversion ratio and a margin (Alder and Birch, 48% and 13%; Alder and the corner
  shops, 7% and 15%; two cement kilns, 20% and 60%); a pair is one market when diversion exceeds the critical value
  X/(X + M) (27%, 25% and 8%), so pairs one and three;
- market definition: the hypothetical-monopolist test in a town with all three chains (Alder alone fails, Alder and
  Birch pass, the three superstores pass easily); critical loss (13.4% margins give a critical loss of 27% against an
  actual loss of 4.9%) and Katz and Shapiro's reply to the defence's reading of it; the cellophane trap (at monopoly
  prices, 100.79 instead of 81.77, a further rise no longer pays);
- concentration: the Herfindahl index and its rise, 2 s_A s_B; the presumptions of 1982, 2010 and 2023 applied to five
  Island industries (the grocers' merger is presumed harmful in 1982 and 2023 but not in 2010); in every Island town
  where Alder and Birch meet the index rises by more than 2,600 points;
- unilateral effects: the diversion matrix (48% of Alder's lost sales go to Birch, 7% to the shops); upward pricing
  pressure derived from the merged firm's first-order condition as an opportunity cost; GUPPIs of 6.3% and 7.5%, a
  simulation of +6.0% and +7.2% (Cedar +1.8%), and compensating cost cuts of 16% and 17%;
- simulation in court: two identical firms with a 30% margin and 30% diversion, and four demand curves fitted to the
  same numbers, predicting rises of 6.4% (linear), 7.4% (logit), 8.0% (linear in log price) and 22.5% (constant
  elasticity), against a GUPPI of 9%; how simulations are attacked; an agency's plain logit, calibrated town by town
  even to Alder's true elasticity, predicts 6.9% on average against a truth of 11.9%;
- efficiencies and entry: a 2% cost saving is passed on at 67% by Alder alone and 53% once merged; Staples' own history
  of 15-17% firm-specific pass-through against the parties' claim of two-thirds; the merger's effect is 5.6% where
  Cedar is present and 18.9% where it is not;
- an intermission: airline fares in the consumer price index, relative to all prices, 1964-2025 (twice their 1978
  level in 2000, 14% above it in 2025), with deregulation and the big mergers marked, and the reminder that an index
  is a method (from late 1998 to mid-2003 the CPI's fares rose 15.4%, the BLS's index of fares actually paid 6.8%);
- vertical mergers: *United States v. AT&T* (2018, affirmed 2019) and the Nash-bargaining model; on the Island a
  channel's fee to a rival distributor rises by $0.90 (45%) while the integrated distributor saves the $2.00 fee, and
  the net effect turns on the share of subscribers who would leave in a blackout (14.8% is the break-even);
- cartels: coordinated effects; a variance screen on fifteen years of the Island's cement prices (margin volatility
  0.051 outside the cartel, 0.009 during it); the before-during-after overcharge (17.7%, s.e. 0.3, against 18%
  planted), damages of $63 million and $190 million trebled; Abrantes-Metz et al.'s frozen perch;
- regression in the witness box: *Daubert*, *Kumho Tire* and Rule 702 as amended in 2023; the Island's price
  regression (7.2% without controls, 10.4% with cost and size, against a true merger effect of 11.9%); sixteen
  specifications (7.2-10.6%), leave-one-out (10.2-10.8%) and the subsamples (3.8% where Cedar is present, 15.4% where
  it is not); Staples' 8.6% against 0.9%;
- labour: two Island hospitals merge and nurses' wages fall 7.7%, the markdown widening from 18% to 24%; Prager and
  Schmitt's hospital mergers; Krueger and Ashenfelter's no-poach clauses (58% of major franchisors in 2016); the 2023
  guidelines' Guideline 10;
- retrospectives: the Island's merger consummated, measured by difference in differences (11.7% against 11.9% true,
  the GUPPI's 9.0 and the plain logit's 6.9); Ashenfelter and Hosken (3-7%), Cooper et al. (about 6% for hospitals
  within five miles), Brot-Goldberg et al. (13 hospital mergers challenged in 2000-2020, about 1%);
- regulated prices: a rate case (a revenue requirement of 105, a price of 1.05), *Hope Natural Gas*; Littlechild's
  RPI - X with resets (a real price of 0.54 after fifteen years against 0.86 under cost of service, on assumed
  effort); the efficient component pricing rule for access (8 = 3 + 5);
- the Dials (pass-through of a merger's savings, new; cartel overcharges, revisited), the profession at work,
  *Called it?*: AT&T's bet on Time Warner (wrong), and the frontier: *FTC v. Meta* (2025), zero prices, series of
  acquisitions, data and ecosystems.

## Build it

```bash
python -m videos.economics.econ59.compute              # every number (about four minutes), into .cache/econ59/
python tools/qa_scene.py econ59 Market                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ59 -q l   # the whole part, silent preview
python tools/build.py econ59                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 59                     # the lab
```

The data are FRED's consumer price index for airline fares (CUUR0000SETG01) and for everything (CPIAUCNS),
registered in [`SOURCES.md`](../../../explainer/economics/data/SOURCES.md). Everything else is computed on the Island,
or stated from the cases and papers listed in `dials.SHOWN[59]`.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The price map | *Staples*; the Island's sixty towns and Alder's prices; the question; objectives |
| 1 | What the law asks | Section 7; the review process; who must prove what |
| 2 | Play it: one market or two? | Three pairs; diversion against the critical value X/(X + M) |
| 3 | Market definition | The hypothetical monopolist; critical loss and its misuse; cellophane |
| 4 | Shares and concentration | The HHI and its rise; the presumptions of 1982, 2010 and 2023 |
| 5 | Unilateral effects | Diversion ratios; upward pricing pressure derived; GUPPIs against simulation |
| 6 | Merger simulation in court | Four demand curves, one data set; the attacks; an agency's plain logit |
| 7 | Efficiencies, pass-through and entry | Pass-through merged and alone; Staples' 15-17%; Cedar's discipline |
| — | Intermission | Airline fares in the CPI, 1964-2025, as a line and a tune |
| 8 | Vertical mergers | *AT&T*; Nash bargaining over a fee; the departure rate that decides |
| 9 | Coordinated effects and cartels | Screens; the overcharge regression; damages |
| 10 | Regression in the witness box | *Daubert*; direct examination; the cross-examination |
| 11 | Labour markets | Two hospitals merge; Prager and Schmitt; no-poach clauses |
| 12 | Retrospectives | Difference in differences on the Island; what the real studies found |
| 13 | Regulated prices | A rate case; price caps; access pricing |
| 14 | The Dials | Pass-through of savings (new); cartel overcharges (Part 12's) |
| 15 | In practice | Agencies, consultancies, experts, in-house teams; *Called it?*: AT&T, 2016 |
| 16 | Frontier | *FTC v. Meta*; zero prices; series of acquisitions; data |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 60, *The Price* |

## What is computed, and from what

Everything plotted is computed by `compute.py` with Agora's `merger` module (`explainer.economics.agora.merger`); the
narration states the cached numbers.

- **The market.** Products Alder, Birch, Cedar and the corner shops, and buying nothing; utility 8.6, 8.5, 8.4 and 7.4
  minus 0.08 times the price; a nested logit with the three superstores in one nest (sigma 0.4) and the shops in
  another; marginal costs 70, 71, 72 and 78; Bertrand-Nash prices solved from the first-order conditions by Powell's
  hybrid method.
- **The towns.** Sixty towns with a standardized size; costs shifted by 6% per unit of size plus noise (s.d. 2%);
  Birch present with probability 1/(1 + exp(-(0.2 + 1.2 size))), Cedar with 1/(1 + exp(-(-0.4 + size))); Alder's
  price observed with noise of 0.6%; the true merger effect in each town by solving the market with Alder and Birch
  under one owner.
- **The regression.** Least squares of log price on Birch, Cedar, cost and size with HC1 errors; the sixteen
  specifications toggle cost, size, logs and Cedar; leave-one-out and subsamples as stated.
- **Market definition.** The candidate products' prices raised by X with the others held fixed; profit, actual and
  critical loss; the cellophane test at the prices the three superstores would set as one firm.
- **Unilateral effects.** Diversion from the share Jacobian, D_jk = -(ds_k/dp_j)/(ds_j/dp_j); UPP and GUPPI as
  derived; the simulation and compensating marginal-cost reductions with Agora's `io` module.
- **Functional forms.** Two symmetric firms at price 1 with margin m = 0.3 (own elasticity 1/m) and diversion 0.3;
  linear, logit with an outside good, linear-in-log-price and constant-elasticity demand calibrated to those numbers;
  the merged price from the symmetric joint first-order condition.
- **The agency's model.** In each of the 36 towns where Alder and Birch meet, a plain logit with the observed prices
  and shares and Alder's true own-price elasticity; the merger simulated with it.
- **Pass-through.** A 2% cut in marginal cost for Alder alone, and for Alder and Birch under one owner.
- **Vertical.** Nash bargaining with equal weights; 10% of the rival's subscribers leave in a blackout, 45% of them to
  the integrated distributor, whose margin is $40 a month; a fee of $2; the integrated distributor has 40% of
  subscribers.
- **The cartel.** A cost index following a random walk (s.d. 2% a month) from 50; price 1.25 times cost with noise
  (s.d. 3.5% outside the cartel, 0.8% within), times 1.18 in months 72-131; quantities with elasticity 0.8 (thousands
  of tonnes a month); the screen is the rolling twelve-month standard deviation of the change in the log margin, with
  the calmest quarter flagged.
- **Labour.** Nurses choose two hospitals or other work by logit in the wage (coefficient 0.2); a nurse's hour is
  worth 40; each hospital, or the merged pair, sets wages from its first-order conditions.
- **The retrospective.** Twelve months before and after the merger, with a common random-walk shock and noise of 1%
  in each town; treated towns are those where Birch is present.
- **Regulated prices.** A rate base of 500 at 7%, operating costs 40, depreciation 20, taxes 10, volume 100; inflation
  3%, X = 2%, resets every five years, real cost falling 4% a year under the cap and 1% under cost of service (assumed);
  the access price as the network's cost (3) plus the incumbent's retail margin (5).

## Problems and solutions

**1.** *Critical diversion: for two symmetric firms with linear demand, each pricing to maximize profit, show that a
joint rise of X pays if and only if D > X/(X + M). Evaluate it for M = 0.4 and X = 5%.*

*Solution.* With linear demand and each firm at its optimum, the Lerner condition gives an own elasticity of 1/M, so a
rise of X in one price alone loses a fraction X/M of its sales. When both prices rise, each product keeps the fraction
D of its lost sales that would have gone to the other, so the net loss is (X/M)(1 - D). Profit rises if the loss is
below the critical loss X/(X + M): (X/M)(1 - D) < X/(X + M), that is 1 - D < M/(X + M), or D > X/(X + M). With M =
0.4 and X = 0.05, the critical diversion is 0.05/0.45 = 11.1%.

**2.** *A firm with 30% of a market buys one with 4%. Find the rise in the HHI, and say which of the 1982, 2010 and 2023
presumptions it triggers when the post-merger HHI is 1,600.*

*Solution.* The rise is 2 x 30 x 4 = 240 points. With a post-merger index of 1,600, the market is below the "highly
concentrated" lines of 1982 (1,800) and 2010 (2,500), so neither presumption applies (the 1982 guidelines treated a
moderately concentrated market with a rise above 100 as a likely, but not presumed, concern). The 2023 guidelines add
*Philadelphia National Bank*'s test: a merged share above 30% (here 34%) with a rise above 100 is presumed to lessen
competition. Only 2023's presumption applies.

**3.** *Pricing pressure: from the merged firm's first-order condition, show that the merger acts like a rise of
D_AB (p_B - c_B) in A's marginal cost; find the GUPPI when D_AB = 0.3, p_B - c_B = $20 and p_A = $100.*

*Solution.* After the merger the owner chooses p_A to maximize (p_A - c_A) q_A + (p_B - c_B) q_B, so q_A + (p_A - c_A)
dq_A/dp_A + (p_B - c_B) dq_B/dp_A = 0. Write dq_B/dp_A = -D_AB dq_A/dp_A; then q_A + (p_A - [c_A + D_AB (p_B - c_B)])
dq_A/dp_A = 0, which is the single-product condition with marginal cost raised by D_AB (p_B - c_B). The GUPPI is that
increment over A's price: 0.3 x 20 / 100 = 6%.

**4.** *Pass-through: show that a monopolist with linear demand passes on half of a cost change, and one with constant
elasticity e > 1 passes on e/(e - 1) of it.*

*Solution.* With q = a - b p, profit (p - c)(a - b p) is maximized at p = (a/b + c)/2, so dp/dc = 1/2. With q = A
p^(-e), the Lerner condition (p - c)/p = 1/e gives p = c e/(e - 1), so dp/dc = e/(e - 1) > 1: the curvature of demand,
which no data at one price reveal, decides whether a saving is passed on by less or more than one for one, which is
why chapter six's functional forms matter for efficiencies too.

**5.** *A cartel's price is $120 for 24 months against a but-for price of $100, on sales of 50,000 units a month. Find
the overcharge, the damages and the American treble damages.*

*Solution.* The overcharge is 120/100 - 1 = 20% of the but-for price ($20 a unit). Damages are $20 x 50,000 x 24 =
$24 million, trebled to $72 million under section 4 of the Clayton Act. (If the cartel's higher price also cut sales,
buyers lost the surplus on the units they did not buy too, a triangle the simple calculation leaves out.)

**6.** *The bargaining model: with weight w, show that the fee rises by w x departure x share to the integrated rival x
its margin, and find the departure rate at which the rivals' extra costs equal the integrated distributor's saving.*

*Solution.* In Nash bargaining the fee splits the gains from agreement, so it moves by w times any change in the
channel's payoff if talks fail. Before the merger that payoff does not depend on where departing subscribers go;
after it, a share d of the rival's subscribers leave in a blackout and a share s of those join the integrated
distributor, worth its margin m each, so the channel's disagreement payoff rises by d s m per rival subscriber and the
fee by w d s m. On the Island (w = 1/2, s = 0.45, m = $40, the rival has 60% of subscribers), the rivals' extra cost
per subscriber in the market is 0.5 x d x 0.45 x 40 x 0.6 = 5.4 d, and the saving from removing the $2 fee on the
integrated distributor's 40% is 0.8; they are equal at d = 0.8/5.4 = 14.8%.

## Lab and interactive

- `python -m videos.economics.labs 59`: the Island's market and a town's equilibrium; the critical diversion of the
  three pairs; the hypothetical-monopolist test; the HHI presumptions; diversion, UPP and GUPPI against the
  simulation; the four functional forms; pass-through; the vertical fee and its break-even; the cartel's overcharge
  and damages; the labour merger.
- The interactive (course site): expert. The reader is the agency's economist in one Island town: set the diversion
  ratio and the margins, run the hypothetical-monopolist test and the GUPPI screen, choose a demand curve for the
  simulation, decide whether to challenge, and then see the retrospective's verdict on the decision.

## Sources

The cases and studies the film states are listed with what each shows in `dials.SHOWN[59]`; the new Dial (pass-through
of a merger's cost savings) and the Island's rows for cartel overcharges and merger retrospectives are in
`explainer/economics/dials.py`, and the *Called it?* record of AT&T's purchase of Time Warner in
`explainer/economics/calls.py`. The methods are stated from the works cited in the chapters (Harris and Simons 1989,
Werden 1996, Crooke, Froeb, Tschantz and Werden 1999, Katz and Shapiro 2003, O'Brien and Wickelgren 2003,
Abrantes-Metz, Froeb, Geweke and Taylor 2006, Ashenfelter, Ashmore, Baker, Gleason and Hosken 2006, Farrell and
Shapiro 2010, Ashenfelter and Hosken 2010, Cooper, Craig, Gaynor and Van Reenen 2019, Prager and Schmitt 2021,
Krueger and Ashenfelter 2022, Brot-Goldberg, Cooper, Craig and Klarnet 2024) and computed here.
