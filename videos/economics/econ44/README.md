# Economics, Built: Part 44, Dynamics, Platforms and Antitrust

Part 44 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second of Act IX, *The Fields*. It asks how firms compete over time, and what is
different when the product is a network. Its answer: over time, firms invest and race, and their choices look ahead in
ways that can be estimated from what they do; with networks, the structure of prices matters as much as their level,
markets can tip and stay tipped, and antitrust must weigh effects that do not show in today's prices.

It opens on Harold Zurcher's ledger: John Rust's data on the Madison (Wisconsin) bus company's engines, drawn as the
sawtooth lines of ten 1975 GMC buses' miles since each rebuild; 162 buses from 1974 to 1985, rebuilt on average at
about 230,000 miles. From there it covers:

- a game: the Island's bus line rebuilds engines for $4,000, upkeep costs $6 a month per 5,000 miles, and buses run
  about 3,280 miles a month (Rust's transitions); rebuilding at 50,000, 150,000, 250,000 or 350,000 miles costs $289,
  $174, $199 and $244 a month; the best rule is 150,000;
- Rust's model written down (values of keeping and rebuilding, logit surprises, the fixed point for expected value)
  and the nested fixed point; estimated on his groups 1 to 4 (104 buses, 8,156 bus-months, 60 rebuilds; monthly steps
  of 0, 1 and 2 bins with chances 35.6%, 63.2% and 1.2%): a rebuild cost of 9.79 (se 0.91) and upkeep of 2.65 (se 0.47)
  per thousand steps, a rebuild worth about 123 months of upkeep at 150,000 miles; myopia rejected (likelihood-ratio
  statistic 12.9), and the likelihood nearly flat for discount factors from 0.99 to 0.9999;
- Hotz and Miller's conditional choice probabilities with Rust's renewal: on Zurcher's buses the rebuild cost moves
  from 7.3 to 17.2 with the first step's polynomial (only 60 rebuilds); on simulated fleets of 104 and 1,000 buses the
  short cut and the nested fixed point agree near the truth;
- a Markov-perfect duopoly in the style of Ericson and Pakes (eight quality steps): investment highest when neck and
  neck (1.13), lower two steps ahead (0.99) or behind (1.08); 202 changes of leader in 4,000 periods; Bajari, Benkard
  and Levin's two-step estimation and Ryan's cement;
- vertical relations: double marginalization (price 8 instead of 6; joint profit 12 instead of 16; buyers' surplus 2
  instead of 8), its fixes (merger, two-part tariffs, resale price maintenance after *Leegin*), and foreclosure with the
  Chicago critique;
- two-sided markets: Rochet and Tirole; Armstrong's linear platform, where side 1's price falls from 0.56 to 0 and
  then below zero (-0.33) as its value to side 2 rises; *Ohio v. American Express*; Rysman's Yellow Pages;
- network effects: QWERTY (David), Arthur's lock-in on the Island (a worse first mover wins 81% of runs at a network
  effect of 0.02, from none at zero to all at 0.04), and Liebowitz and Margolis's reply;
- an intermission: the Madison fleet's average mileage since rebuild, month by month from 1974 to 1985, with each
  month's rebuilds marked, as a tune;
- competition and innovation: Arrow's replacement effect (a cost cut worth 7 to a monopolist, 12 to a competitive
  innovator, 14 to society); Aghion et al.'s step-by-step model solved on the Island, innovation peaking at moderate
  competition (0.99 at a competition parameter of 0.4, against 0.33 and 0.87 at the extremes);
- killer acquisitions in numbers (a project worth 10 to its developer, shelved by an incumbent who would pay up to 70)
  and Cunningham, Ederer and Ma's evidence;
- algorithms that learn to collude: twelve sessions of Q-learning price setters in Calvano et al.'s game (Nash price
  1.47, monopoly 1.92) end with a profit gain of 0.86 on average (0.57 to 0.99), an average price of 1.80, and a
  punishment after a forced deviation in every session; Assad et al.'s German petrol stations;
- antitrust's standards: Standard Oil, the consumer-welfare standard, the neo-Brandeisian critique, *Microsoft* and
  *Google* (liability in August 2024; in September 2025 no sale of Chrome, no exclusive deals, some data shared);
- Baron and Myerson's regulator (high-cost output cut from 6 to 5.2, the low type's rent from 12 to 10.4), and Laffont
  and Tirole;
- two dials (merger price effects measured after the fact, and the discount factor of a dynamic decision maker, both
  new); who does this work, a platform's strategy in four steps; *Called it?* on Steve Ballmer's 2007 dismissal of the
  iPhone (wrong); a frontier chapter on data as a barrier, interoperability, foundation models and algorithms.

## Build it

```bash
python -m videos.economics.econ44.compute              # every number (about four minutes), into .cache/econ44/
python tools/qa_scene.py econ44 RustModel              # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ44 -q l   # the whole part, silent preview
python tools/build.py econ44                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 44                     # the lab
```

The data are in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): Rust's Madison bus panel (162 buses in eight groups, from
the MIT-licensed mirror of his files, checked by SHA-256), and tables from Rust and Hotz and Miller, Ericson and Pakes,
Pakes and McGuire, Bajari, Benkard and Levin and Ryan, Spengler, Bork and *Leegin*, Rochet and Tirole, Armstrong,
Rysman and *Ohio v. American Express*, David, Liebowitz and Margolis and Arthur, Arrow, Aghion et al. and Cunningham,
Ederer and Ma, Calvano et al. and Assad et al., the antitrust cases and Khan, Baron and Myerson and Laffont and Tirole,
Kwoka's retrospectives and their critics, and the 2007 interview and IDC's 2023 shipments.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Harold Zurcher's ledger | The sawtooth lines; what was Zurcher thinking?; the question; objectives |
| 1 | Play it: the odometer climbs | The game; the answer; the cost curve and the surprises it leaves out |
| 2 | Rust's model: when to rebuild | The model; the nested fixed point; the estimates and the fit; myopia rejected |
| 3 | Faster: conditional choice probabilities | The inversion with renewal; on Zurcher's buses; on simulated fleets |
| 4 | Dynamic oligopoly | Ericson and Pakes in miniature; the investment policy; a history; estimation |
| 5 | Vertical relations | Double marginalization; three fixes and a warning; foreclosure |
| 6 | Two-sided markets | Examples; Armstrong's model; prices against value; antitrust |
| 7 | Network effects, tipping and lock-in | QWERTY; lock-in on the Island; the curve; the reply |
| — | Intermission | Madison's buses, 1974-1985, as a tune |
| 8 | Competition and innovation | Schumpeter and Arrow; the replacement effect; step by step; the inverted U |
| 9 | Killer acquisitions | The logic in numbers; the evidence |
| 10 | Algorithms that learn to collude | The set-up; twelve sessions; a punishment; markets and the law |
| 11 | Antitrust's standards | A century in six marks; each side's best case; *Google* |
| 12 | Regulating a firm that knows more | The problem; Baron and Myerson; the trade-off |
| 13 | The Dials | Merger retrospectives; the discount factor |
| 14 | In practice: platform strategy and the agencies | Who does this; four steps; *Called it?* (wrong) |
| 15 | Frontier | Data, interoperability, foundation models, algorithms |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 45, *Behavioural Economics* |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's industrial organization module
(`explainer.economics.agora.io`, part II), with the Island's Part 44 truths, or from Rust's data; the narration states
the cached numbers.

- **Rust's panel.** For groups 1 to 4, each bus-month's mileage since the last rebuild in bins of 5,000 miles (90
  states); a rebuild between two readings is placed halfway; the next month's state counts from zero after a rebuild.
  Transition probabilities are the frequencies of 0, 1 and 2 (or more) bins.
- **The model.** Upkeep 0.001 theta x per month, rebuild cost RC, logit surprises with unit scale, discount factor
  0.9999; the expected value function is solved by 50 contraction steps and Newton-Kantorovich steps to 1e-12; the
  likelihood is maximized by Nelder-Mead, with standard errors from a numerical Hessian. The profile over the discount
  factor re-estimates RC and theta at each of seven values.
- **CCP.** A logit in a polynomial of mileage (degree 1 to 3) for the first step; then a logit for (RC, theta) with the
  offset beta times the sum over j of p_j (ln P1(x + j) - ln P1(j)). The simulated fleets run ten years of monthly
  decisions under the NFXP estimates.
- **The game.** The deterministic rule 'rebuild at T bins' with RC = $4,000 and upkeep $6 per bin per month; the
  average monthly cost from the stationary distribution of the chain it induces.
- **The duopoly.** Pakes and McGuire's symmetric game: profit 5 exp(w_i) / (1 + exp(w_i) + exp(w_j)), success
  probability 1.5 x / (1 + 1.5 x), depreciation 0.3, discount factor 0.925; best responses in closed form from the
  first-order condition; Gauss-Jacobi iteration with damping 0.5 to 1e-9; 4,000 simulated periods.
- **The platform.** n1 = 1 + 0.2 n2 - p1, n2 = 1 + alpha2 n1 - p2, zero costs; prices from the linear first-order
  conditions.
- **Lock-in.** 600 adopters with B's advantage normal(0.3, 1); A starts with 20; 300 runs at each network strength.
- **Innovation.** Quadratic research costs, leader profit 1, neck-and-neck profit (1 - Delta) each, interest 5%,
  imitation 0.1; values by solving the three Bellman equations; the steady-state shares from the flows.
- **Q-learning.** Calvano et al.'s logit duopoly (a = 2, a0 = 0, mu = 0.25, cost 1), 15 prices from the Nash price
  less 10% of the Nash-monopoly gap to the monopoly price plus 10%, one-period memory, alpha 0.15, exploration
  exp(-4e-6 t), delta 0.95; each session stops when both greedy strategies are unchanged for 100,000 periods.
- **Regulation.** Demand P = 10 - q, costs 2 or 4 with equal probability, profits weighted 0.6.

## Problems and solutions

**1.** *Zurcher's game: a rebuild costs $4,000, upkeep is $6 a month per 5,000 miles, and a bus covers 3,300 miles a
month. Using the rule that the best mileage is about sqrt(2 RC v / c), find it.*

*Solution.* In bins, v = 3,300 / 5,000 = 0.66 a month, so sqrt(2 x 4,000 x 0.66 / 6) = sqrt(880) = 29.7 bins, about
148,000 miles: the chapter's 150,000. (The rule comes from minimizing (RC + c v t^2 / 2) / t over the time t between
rebuilds.)

**2.** *Rust: with RC = 9.79 and theta = 2.65 (per 1,000 steps), how many months of upkeep at 150,000 miles is a
rebuild worth? At 250,000?*

*Solution.* At 150,000 miles (30 bins) a month's upkeep is 0.001 x 2.65 x 30 = 0.0795, so 9.79 / 0.0795 = 123 months.
At 250,000 (50 bins), 0.1325, so 74 months.

**3.** *Myopia: the log likelihood is -299.2 at beta = 0.9999 and -305.7 at beta = 0. Compute the likelihood-ratio
statistic and test at 5%.*

*Solution.* 2 x (305.7 - 299.2) = 12.9 (13.0 with the rounded numbers), above the 5% critical value of 3.84 for one
restriction: myopia is rejected.

**4.** *Double marginalization: demand P = 10 - Q, cost 2. Find the integrated price, the wholesale and retail prices of
separate firms, and the fixed fee a two-part tariff could charge.*

*Solution.* Integrated: (10 + 2)/2 = 6. Separate: the maker charges w = 6, the retailer (10 + 6)/2 = 8. With a two-part
tariff the maker sells at w = 2, the retailer charges 6 and earns (6 - 2) x 4 = 16, all of which the maker can take as
the fee.

**5.** *Platforms: with n1 = 1 + 0.2 n2 - p1 and n2 = 1 + alpha2 n1 - p2 at zero cost, show that p1 = p2 = 0.5 when
alpha2 = 0.2.*

*Solution.* By symmetry p1 = p2 = p and n1 = n2 = n, so n = 1 + 0.2n - p, n = (1 - p)/0.8. Profit 2pn = 2p(1 -
p)/0.8 is largest at p = 0.5, where n = 0.625. (The general first-order conditions, which also allow the two prices to
differ, give the same answer, as the film's computation confirms.)

**6.** *Arrow: demand P = 10 - Q; a new process cuts cost from 4 to 2. Find the gain to a monopolist and to an
innovator in a competitive industry. Is the innovation drastic?*

*Solution.* Monopoly profit (10 - c)^2 / 4: 9 at c = 4, 16 at c = 2, a gain of 7. The monopoly price at the new cost,
(10 + 2)/2 = 6, is above the old cost 4, so the innovation is not drastic: the competitive innovator prices just below
4 and earns (4 - 2) x 6 = 12.

**7.** *Killer acquisitions: with the chapter's numbers, for which development costs does the start-up develop the drug
but the incumbent shelve it?*

*Solution.* The start-up develops if the cost is below its duopoly profit, 40; the incumbent develops only if the cost
is below the drug's addition to its profit, 110 - 100 = 10. So for costs between 10 and 40 the project is killed after
an acquisition.

**8.** *Baron and Myerson with two types: derive the virtual cost and show the high-cost output is a minus it.*

*Solution.* The regulator maximizes expected consumer surplus less transfers plus w times profits, where the low type
must get at least the profit it would earn by mimicking the high type, (c_H - c_L) q_H. Substituting the binding
constraints, the high-cost output appears in expected welfare as (1 - nu)[S(q_H) - c_H q_H] - nu (1 - w)(c_H - c_L)
q_H. The first-order condition is P(q_H) = c_H + nu/(1 - nu) (1 - w)(c_H - c_L), so with P = a - q, q_H = a minus that
virtual cost: 10 - 4.8 = 5.2 with the chapter's numbers.

## Lab and interactive

- `python -m videos.economics.labs 44`: Rust's model by NFXP on his data, the myopic fit and the likelihood-ratio
  test, the CCP short cut; the duopoly's policy; double marginalization; the platform's prices; lock-in; the inverted
  U; a Q-learning session; Baron and Myerson.
- The interactive (course site): rebuild the engine. The reader sets the rebuild cost, the upkeep and a rebuild rule,
  and sees the average monthly cost of every rule, the best one, and how much their own rule wastes.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[44]`; the two dials are in
`explainer/economics/dials.py`; Ballmer's 2007 remark is a *Called it?* entry (`explainer/economics/calls.py`). Rust's
data are his files as mirrored by OpenSourceEconomics (zurcher-data), retrieved 2026-11-20 and checked by SHA-256; his
results are replicated here, not transcribed. Hotz and Miller, Ericson and Pakes, Pakes and McGuire, Bajari, Benkard
and Levin, Ryan, Rochet and Tirole, Armstrong, Rysman, David, Liebowitz and Margolis, Aghion et al., Cunningham, Ederer
and Ma, Calvano et al., Assad et al., Khan and Baron and Myerson from their abstracts; the cases from their decisions'
summaries and, for Google's remedies, press reports of 2 September 2025; Kwoka's numbers from Northeastern's summary
of the 2013 article and reviews of the 2015 book; IDC's from its release of 15 January 2024. Not verified, so stated in
words or computed on the Island instead: Rust's own published estimates, Calvano et al.'s profit gains, the size of
killer acquisitions, Assad et al.'s margin effects, network-effect elasticities.
