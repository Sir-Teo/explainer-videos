# Economics, Built: Part 45, Behavioural Economics

Part 45 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third of Act IX, *The Fields*. It asks what changes in economics when people are
not the agents of Part 5. Its answer: choices become predictable in new ways, because people overweight the present,
judge outcomes as gains and losses from a reference point, attend to little, and care about others; markets cure some
of this, where people learn fast, and feed on the rest; and welfare can only be read where choices made in different
frames agree.

It opens on DellaVigna and Malmendier's gym: 7,752 members of three American health clubs, many on monthly contracts of
over $70, going 4.3 times a month and so paying over $17 a visit, when a ten-visit pass cost $10. On the Island, with
the same prices, naive monthly members forecast 13.9 visits a month, make 4.7, and pay $15.02 a visit; 84% would have
paid less with the pass. From there it covers:

- three departures from Part 5's agent (preferences, beliefs, decision making), drawn as the failure of one term each
  in the standard objective, and four new residents of the Island: the naif, the sophisticate, the loss-averse trader
  and the inattentive buyer;
- a game: the viewer is given a mug and names a selling price; in the Island's mug market (44 people, values lognormal
  around $4) owners who count losses twice ask a median $8.07 against buyers' $4.03, and 24% of the mugs trade instead
  of 50% (averages over 4,000 sessions); Kahneman, Knetsch and Thaler's experiments;
- prospect theory in one card (alpha = beta = 0.88, lambda = 2.25); traders whose loss aversion fades with experience,
  trading 25% of goods as newcomers and 50% as veterans; List's own card-show data (148 traders, Orlando, 1998): 34%
  swapped where about half should have, from none of those who never trade to about half of those trading ten or more
  times a month, and among non-dealers 7% of occasional traders against 47% of regulars; where the reference point
  sits;
- reference points in the field: 400,000 Island marathon runners bunch just under every half hour, with about 1.9
  minutes' worth of excess runners under four hours and as many missing just over it (the planted kink moves 2.5),
  measured with Part 41's bunching estimator; putts for par and birdie, where the raw gap of 21 points is mostly
  distance and putts of the same length differ by 2.2 points (planted 2.5); loss-averse condominium sellers, where a
  regression that misses unseen quality estimates 0.68 and one that controls for the last sale's residual 0.27,
  bracketing the planted 0.3, and owners with losses wait 20 weeks to sell instead of 11;
- present bias: quasi-hyperbolic discounting; a preference reversal ($100 today over $110 tomorrow, $110 in a year and
  a day over $100 in a year); O'Donoghue and Rabin's report (costs 3, 5, 8, 13; beta = 1/2: the time-consistent agent
  writes it in week 1, the naif in week 4, the sophisticate in week 2) and film (week 4, 3, 1); the contract a gym
  designs for present-biased members, with visits priced at m - (1 - beta) b = -$4.20 and a monopoly leaving a naif
  $12.96 a month worse off for joining, while free entry returns the fee to $75.60;
- commitment: Ashraf, Karlan and Yin's SEED accounts; the Island's randomized offer, taken by 30% of those offered,
  raising average savings by 11.0 and by 36.5 for takers (the Wald ratio), takers being the more present-biased
  (beta 0.64 against 0.72) and mostly sophisticates;
- defaults: Madrian and Shea; on the Island, a year after hire 63% of naifs save when they must sign up and 98% when
  enrolled automatically, against 90% either way for time-consistent workers, and 55% of naifs are still at the default
  rate after three years; why defaults stick; Carroll et al.'s active choice; Save More Tomorrow (on the Island 4% would
  save more now and 69% sign up to save more later; Thaler and Benartzi's 3.5% to 13.6% in 40 months);
- an intermission of the American personal saving rate, 1959-2026;
- inattention: shrouded add-ons, with printers priced at $9.50 against a cost of $20 and myopes paying $27.50 in all
  against sophisticates' $15.50; the curse of debiasing; left-digit bias in used-car prices, with steps of $171 at every
  10,000 miles and an estimated theta of 0.29 (planted 0.3);
- social preferences: Fehr and Schmidt's inequity aversion in the ultimatum game (51% would reject a fifth of the pie;
  offers average 44%, and 37% of proposers offer half); gift exchange that fades within hours; List's dictator games
  with a take option; the day-care fine of Part 1 and its record;
- whether markets cure biases: learning, arbitrage and selection, and the Island's mixed ledger;
- behavioural welfare: Bernheim and Rangel's welfare range across frames; libertarian paternalism and its critics; a
  disclosure rule at the Island's gym that raises members' average real gain from $14.32 a month to $26.25 if every
  naif believes it;
- nudges at scale: DellaVigna and Linos (8.7 points in the journals, 1.4 points in two nudge units' full records); the
  Island's filtered literature (a published mean of 2.67 against a truth of 1.4) and the step-function selection model
  (1.19);
- models of limits: rational inattention by the Blahut-Arimoto iteration, sparse attention by soft thresholding, and
  forecasters who are rational (individual slope -0.04, consensus +1.17) or diagnostic (-0.36 and +0.37);
- three dials (loss aversion: 2.25, 1.955, 1.31 and 1.13; present bias: about 0.5 structurally, 0.70-0.79 over effort,
  about 1 over money; the effect of a default: 49 points for Madrian and Shea's new hires); practice (click to cancel,
  vacated in July 2025; SECURE 2.0's automatic enrollment); *Called it?* on experts who expected a token piece rate to
  crowd out effort (it raised effort 24%: wrong); and a frontier chapter on structural behavioural economics, behavioural macro,
  theories learned from data (prospect theory refitted to choices13k gives lambda = 1.13) and robustness.

## Build it

```bash
python -m videos.economics.econ45.compute              # every number (about a minute), into .cache/econ45/
python tools/qa_scene.py econ45 Present                # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ45 -q l   # the whole part, silent preview
python tools/build.py econ45                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 45                     # the lab
```

The data are in `explainer/economics/data/` and *Psychology, Built*'s Archive: FRED's personal saving rate (PSAVERT),
choices13k (Peterson et al. 2021, fetched on first use and checked by SHA-256), and the tables registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Paying not to go to the gym | DellaVigna and Malmendier; the Island's gym; the question; objectives |
| 1 | Three departures | The standard objective, term by term; three classes; the Island's new residents |
| 2 | Play it: your mug | Name a price; one session's asks and bids; 4,000 sessions |
| 3 | Reference dependence | Prospect theory's value function; experienced traders; List's card-show data; where the reference point sits |
| 4 | In the field: runners, golfers, sellers | Bunching under round times; the kink; par against birdie; condominium sellers |
| 5 | Present bias | Discount curves; a preference reversal; naifs and sophisticates; the gym's contract |
| 6 | Commitment, demanded | Why pay for fewer options; SEED; the Island's trial |
| 7 | Defaults and inertia | Madrian and Shea; the Island's new hires; why defaults stick; Save More Tomorrow |
| — | Intermission | The American saving rate, 1959-2026, as a tune |
| 8 | Inattention | Shrouded add-ons; the curse of debiasing; left digits |
| 9 | Social preferences | The ultimatum game; gift exchange; dictator games and the take option |
| 10 | Do markets cure it? | Three reasons to hope; the Island's ledger; the general pattern |
| 11 | Behavioural welfare | Frames and the welfare range; nudges and their critics; disclosure at the gym |
| 12 | Nudges at scale | Journals against nudge units; a filtered literature; the selection model |
| 13 | Models of limits | Rational inattention; sparsity; forecasts that over- and under-react |
| 14 | The Dials | Loss aversion; present bias; the effect of a default |
| 15 | In practice: products, protection, pensions | Who uses this; click to cancel; SECURE 2.0; *Called it?* (wrong) |
| 16 | Frontier | Structural behavioural economics, behavioural macro, theories from data, robustness |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 46, *Development* |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's behavioural economics module
(`explainer.economics.agora.behave`) with the Island's Part 45 truths, or from the data named above; the narration
states the cached numbers.

- **The gym.** Thirty days a month; on 55% of them a member cannot go; on the others today's cost of going is uniform on
  [0, 60] and the member goes if it is below beta times the later benefit b (less the price of a visit). Benefits are
  lognormal around 24, beta uniform on [0.5, 0.95]; 85% of members are naive (beta_hat = 1, forgetting the busy days).
  Contracts are chosen by the forecast surplus, the long-run value of the visits forecast less the price.
- **The contract.** A firm with cost m = 3 a visit chooses a fee F and a visit price p for a member with beta = 0.7 and
  b = 24; a monopolist sets F to the perceived surplus, free entry sets profit to zero; both choose p by the same first
  order condition, p = m - (1 - beta) b with uniform costs.
- **The mug market.** 44 people, 22 given a mug; values lognormal (median $4, sigma 0.5); asks lambda v, bids v; the
  trades are the crossings of the ordered asks and bids; 4,000 sessions.
- **The marathon.** Natural times lognormal around 270 minutes (sigma 0.17); effort e costs e^2/2; a minute is worth 1
  plus gain-loss utility 2 per minute around the goal, losses times 2.25; the goal is the fastest half-hour mark
  reachable with the effort a loss calls for, and making it means finishing a quarter-minute under; finishing noise 0.3
  minutes. Bunching by a degree-5 polynomial fitted outside the window from 4 minutes under to 8 over.
- **Golf, condos, cars.** Putt lengths gamma-distributed (birdie putts longer), success a logit in log feet, par putts
  2.5 points likelier. Condos: eight purchase years with an index that peaks in year 4; asking price = value + 0.3 x
  the nominal loss; unseen quality sd 0.15, purchase luck sd 0.12; weekly sale hazard 0.1 exp(-8 x markup). Cars:
  mileage uniform from 5,000 to 120,000, perceived L + 0.7 (m - L), price 12,000 - 0.06 x perceived + noise; band fixed
  effects and a common within-band slope.
- **Commitment, defaults.** The trial: beta uniform on [0.4, 1], 35% sophisticated, savings beta x 100 without the lock
  and 100 with it, the value of flexibility normal(16, 12). Enrolment: ideal rates zero for 10%, otherwise uniform from
  2% to 15%; the effort of changing exponential with mean 300 each month; the gain 2,500 (s* - d)^2 a month; a naif acts
  when k (1 - beta delta) <= beta g, with beta = 0.7 and delta = 0.995.
- **Inattention, social preferences, welfare.** Shrouding as in Gabaix and Laibson's competitive equilibrium. Envy
  alpha exponential with mean 0.5 and guilt beta uniform on [0, 0.8] for 2,000 players. The disclosure rule turns a
  share of naifs' forecasts into the truth.
- **The literature.** 600 journal trials with 300 to 8,000 people an arm, true effects normal(1.4, 1) on a 17.2% base,
  published if significant (one-sided) and otherwise with probability 0.1; a unit's 150 trials of 2,000 to 100,000 an
  arm, all reported. The step-function selection model by maximum likelihood (Nelder-Mead from three starts).
- **Forecasts.** An AR(1) with persistence 0.8, forty forecasters with private noise 1.5 and the steady-state Kalman
  gain; diagnostic forecasters add 0.6 of the news to their forecast; 600 periods.
- **choices13k.** Prospect theory fitted by least squares to the choice rates of the 1,928 problems described without
  feedback, as in *Psychology, Built*, Part 26.

## Problems and solutions

**1.** *The gym: a monthly fee of $70 and 4.3 visits a month. What does a visit cost? How many visits a month would
make the fee cheaper than a pass at $10 a visit?*

*Solution.* $70 / 4.3 = $16.28 a visit. The fee is cheaper than the pass once 10 x visits > 70, that is from the
eighth visit a month: a member must go more than 7 times a month for the contract to pay.

**2.** *Present bias: with beta = 0.7 and delta = 1, compare $100 today with $110 tomorrow, and the same pair a year
away. Below what beta does today's $100 win?*

*Solution.* Today: 100 against 0.7 x 110 = 77, so the $100. A year away both are multiplied by 0.7: 70 against 77, so
the $110. Today's $100 wins when 110 beta < 100, that is for beta below 0.909; for any such beta the plan made a year
ahead reverses when the day comes.

**3.** *O'Donoghue and Rabin: costs 3, 5, 8, 13 over four weeks. Find when the naif and the sophisticate act with beta
= 1/2, then with beta = 0.7.*

*Solution.* With beta = 1/2 the naif compares each week's cost with half the cheapest later one: 3 > 2.5, 5 > 4, 8 >
6.5, so it waits to week 4. The sophisticate reasons backward: week 3 would wait (8 > 6.5) for week 4's 13, so in week
2 the comparison is 5 against 6.5, and it acts in week 2. With beta = 0.7, 3 <= 0.7 x 5 = 3.5, so both act in week 1:
mild present bias does not distort this choice at all.

**4.** *The mug: owner and buyer both value a mug at $4; losses over goods count twice, over money once. Find the ask
and the bid. Can they trade?*

*Solution.* The owner asks 2 x $4 = $8; the buyer bids $4. No price lies between, so they do not trade, although the
mug is worth the same to both and trade would cost nothing.

**5.** *Left digits: within a band, price falls $40 per 1,000 miles; at each 10,000 it drops a further $170. Estimate
theta.*

*Solution.* Ten thousand miles of within-band slope are worth $400. Then theta = 170 / (170 + 400) = 0.30: buyers
ignore about 30% of the information in the digits after the first.

**6.** *Commitment: 30% of those offered take the account, and the offer raises average savings by 11. What is the
effect on a taker, and what does it assume?*

*Solution.* 11 / 0.30 = 36.7. It assumes that the offer changes savings only through the account (being offered and
declining has no effect); with one-sided take-up (nobody not offered can open one) nothing more is needed, and the
answer is the effect on those who take it, not on everyone.

**7.** *Fehr and Schmidt: a responder with alpha = 1 and a proposer with beta = 0.6. Find the smallest acceptable share
and the proposer's offer.*

*Solution.* Accepting s gives s - alpha (1 - 2s) for s < 1/2, which is positive when s > alpha / (1 + 2 alpha) = 1/3.
The proposer's utility from an accepted offer s < 1/2 is (1 - s) - beta (1 - 2s), whose slope in s is 2 beta - 1 =
0.2 > 0, so the proposer offers half.

**8.** *Selection: estimates are published with probability 1 if z >= 1.96, gamma otherwise. Write the density of a
published estimate, and show the published mean exceeds mu when gamma < 1.*

*Solution.* With x ~ normal(mu, sigma^2) and a = 1.96 se, a published estimate has density p(x) f(x) / P, where p(x)
= 1 for x >= a and gamma below, and P = Pr(x >= a) + gamma Pr(x < a). Its mean is a weighted average of E[x | x >= a]
and E[x | x < a] with weights Pr(x >= a) and gamma Pr(x < a). With gamma = 1 the weights give mu; lowering gamma moves
weight from the lower conditional mean, which is below mu, to the upper one, which is above it, so the published mean
exceeds mu.

## Lab and interactive

- `python -m videos.economics.labs 45`: the Island's gym and the contract for a naif; the mug market with and without
  loss aversion; bunching at four hours; O'Donoghue and Rabin's weeks; the commitment trial; left-digit bias; a filtered
  literature and its correction; forecasters' slopes.
- The interactive (course site): join the gym. The reader sets their present bias, what they believe about it, the busy
  days they expect and what a workout is worth, and sees which contract they choose, what each visit costs and what the
  choice costs them in hindsight.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[45]`; the three dials (loss aversion,
present bias, the effect of a default) are in `explainer/economics/dials.py`; the experts' forecast of crowding out is a
*Called it?* entry (`explainer/economics/calls.py`). List's card-show data are AER 1.2-17's `SportsCards` (from Stock
and Watson's online complements), retrieved 2026-11-21 and checked by SHA-256; the shares are computed here. The
studies' statements were checked on 2026-11-21 against their abstracts and the authors' summaries: DellaVigna and
Malmendier (7,752 members, over $70 a month, 4.3 visits, more than $17 a visit against $10); Ashraf, Karlan and Yin
(202 of 710 offered took the account; savings up 81 percentage points); Madrian and Shea (37% to 86%, as the authors
summarized it in 2024); Thaler and Benartzi (78% joined; 3.5% to 13.6% in 40 months); Lacetera, Pope and Sydnor (22
million sales; steps of roughly $150-200); Pope and Schweitzer (about two points); Genesove and Mayer (25-35% of the
gap); Allen et al. (9,789,093 finishing times); DellaVigna and Linos; Gneezy and List; List (2007); Metcalf et al.
(2020); DellaVigna and Pope (2018); the FTC ruling of 8 July 2025 and SECURE 2.0. Not verified, so stated in words:
Kahneman, Knetsch and Thaler's exact medians (stated as about two to one) and Augenblick, Niederle and Sprenger's beta
values (stated as little present bias over money and more over effort).
