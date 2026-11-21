# Economics, Built: Part 47, Political Economy

Part 47 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth of Act IX, *The Fields*. It asks why governments so often choose policies
that economists can show are wasteful. Its answer: because small groups with a lot at stake organize and large groups
with a little at stake do not; because chasing a privilege is rewarded, so resources are spent winning it; because
voters cannot watch everything their agents do, and elites cannot credibly promise to give up what they hold. What
helps is whatever makes the hidden visible and the powerful accountable: audits, published accounts, competitive
elections, and rules that take the most tempting decisions out of reach.

It opens on Olken's roads: engineers took core samples from over 600 new village roads in Indonesia and priced what
was really in them; more than a fifth of the money was missing; audits announced in advance cut that by about 8
points, and village meetings did little. The Island's version, 600 projects with the truth planted, finds 28% missing
without an audit, an audit effect of -8.0 points (s.e. 1.5) and a meeting effect of -2.5 (s.e. 1.5) against planted
-8 and -1. From there it covers:

- collective action: Olson's free riding, with a group's total lobbying effort sqrt(B K / n) - K falling from 9 for
  one member to nothing for 100; American sugar at a median of 1.9 times the world price, 1960-2026, from the World
  Bank's Pink Sheet; about 4,000 farms gaining $1.4-2.7 billion a year (hundreds of thousands of dollars a farm)
  against consumers losing $2.5-3.5 billion (about $9 a head), a net loss of about $1 billion (GAO, 2023);
- a game: ten players with a hundred tokens each, who can keep, build (each token returns 0.3 to every player) or
  lobby for a prize of 400; everyone building ends with 340 each, a society of half builders and half lobbyists pays
  the builders 150 and the lobbyists 294, and in equilibrium everyone lobbies 36 and ends with 104;
- rent seeking: the Harberger triangle and the Tullock rectangle; Tullock's contest, where n players spend
  R (n - 1)/n^2 each and together dissipate (n - 1)/n of the prize; Krueger's rents of 7.3% of India's national
  income in 1964 and 15% of Turkey's GNP in 1968 from import licences alone;
- voters: probabilistic voting, where a middle group with twice the swing voters receives a transfer worth 51% of
  average income; Lee, Moretti and Butler's finding that voters elect policies rather than affect them; Cattaneo,
  Frandsen and Titiunik's 1,297 Senate elections with outcomes, 1914-2004, analysed here by local linear regression
  discontinuity: barely winning a seat is worth 7.41 points (s.e. 1.46) at the seat's next election, matching
  rdrobust's documented estimate, and 6.5 to 8.0 across bandwidths from 10 to 50 points;
- lobbying and capture: Stigler's capture; the same voting model with an organized rich group, whose net payment falls
  from 84% to 35% of average income; Grossman and Helpman's protection for sale and Goldberg and Maggi's weight on
  welfare of 50 to 88 times the weight on contributions; Fisman's value of connections to Suharto;
- politicians as agents: Barro and Ferejohn's threshold r* = (1 - delta)(W + R) - W; the Island's mayors, where those
  who can run again take 29% less; Ferraz and Finan's 27% in Brazil's random audits, and a 2025 replication's smaller
  estimates;
- audits: Olken's 27.7% missing without audits and 19.2% with them (J-PAL's summary); why meetings failed (free
  riding, visibility, capture, credibility); perceptions that barely track theft;
- an intermission of the world's electoral democracy index, 1900-2025 (V-Dem): 0.14 to a peak of 0.53 in 2012 and
  0.48 in 2025;
- corruption measured four ways (core samples, share prices, diplomats' parking tickets, surveys) and a fifth
  (following the money: Uganda's school grants, a fifth of which arrived in the mid-1990s); the World Bank's control
  of corruption for 195 countries, correlated 0.72 with log income;
- why bad institutions persist: Acemoglu and Robinson's franchise as commitment, with the Island's elite (the richest
  10% earning 70%) extending the vote when crises are rare and relying on promises when they are frequent, and a map
  of revolution, democratization and promises over the frequency of crises and the cost of revolution;
- state capacity: Besley and Persson; central government tax revenue of 13% of GDP in the median poorest-quarter
  country and 22% in the richest quarter, for 150 countries; seven democratizations in V-Dem's index; Acemoglu, Naidu,
  Restrepo and Robinson's 20% higher GDP per head 25 years after democratizing;
- conflict: Miguel, Satyanath and Sergenti's rainfall instrument; on the Island, with growth measured with error, least
  squares gives -1.51 and two-stage least squares -1.97 (s.e. 0.47) against a planted -2; the resource curse;
- media: DellaVigna and Kaplan's Fox News effect and persuasion rate (an Island example gives 8%); Autor, Dorn, Hanson
  and Majlesi's trade shocks and polarization;
- political business cycles: Nordhaus's cycle on the Island, with unemployment pushed down before each election and
  inflation ratcheting up; delegation to central banks, fiscal councils and rules;
- two dials (the share of spending lost to corruption; the incumbency advantage); practice (governance teams,
  regulators, political-risk analysts); *Called it?* on the Treasury's May 2016 forecast of a year-long recession
  after a vote to leave the EU (wrong); and a frontier chapter on democratic backsliding, the economics of populism
  (10% lower GDP per head 15 years on) and the digital state (biometric payments in Andhra Pradesh).

## Build it

```bash
python -m videos.economics.econ47.compute              # every number (under a minute), into .cache/econ47/
python tools/qa_scene.py econ47 Voters                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ47 -q l   # the whole part, silent preview
python tools/build.py econ47                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 47                     # the lab
```

The data are in `explainer/economics/data/`: Cattaneo, Frandsen and Titiunik's Senate elections as distributed in the
R package rdrobust 4.1.2; the World Bank's Pink Sheet sugar prices (world and US); V-Dem's electoral democracy index
via Our World in Data; and the World Bank's tax revenue, control of corruption and GDP per head, all registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Core samples from a road | Olken's design; the Island's road audit; the question; objectives |
| 1 | The logic of collective action | Free riding and group size; sugar's two prices; stakes per head |
| 2 | Play it: build or lobby? | A hundred tokens; the choice; what each society ends with |
| 3 | Rent seeking | The triangle and the rectangle; Tullock's contest; Krueger's estimates |
| 4 | Voters | Probabilistic voting; affect or elect; the Senate's discontinuity; bandwidths |
| 5 | Lobbying and capture | Stigler; an organized group; protection for sale; Fisman's connections |
| 6 | Politicians as agents | The threshold; what it depends on; lame-duck mayors |
| 7 | Audits from above, meetings from below | Olken's results; why meetings failed; perceptions |
| — | Intermission | The world's democracy index, 1900-2025, as a tune |
| 8 | Corruption measured four ways | Audits, prices, behaviour, surveys; Uganda's grants; the WGI |
| 9 | Why bad institutions persist | The commitment problem; the Island's elite; the map of outcomes |
| 10 | State capacity and democracy | Besley and Persson; taxes and income; transitions; democracy and growth |
| 11 | Conflict | Rain, growth and civil war; the Island's instrument; the resource curse |
| 12 | Media and persuasion | Fox News; the persuasion rate; trade shocks and polarization |
| 13 | Political business cycles | Nordhaus's cycle; delegation |
| 14 | The Dials | Corruption's share; the incumbency advantage |
| 15 | In practice: governance, regulation, political risk | Who uses this; design rules; *Called it?* (wrong) |
| 16 | Frontier | Backsliding; populism; the digital state |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 48, *Environment and Climate* |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's political economy (`explainer.economics.agora.politics`)
with the Island's Part 47 truths, or from the data named above; the narration states the cached numbers.

- **Roads.** 600 projects with missing shares normal around 28% (s.d. 18 points), audits and meetings each assigned
  to half at random, measurement error of 6 points; effects by least squares with robust standard errors.
- **Collective action.** Each member of an n-member group chooses effort to maximize (B/n) E/(E + K) minus their own
  effort; the symmetric equilibrium's total is sqrt(B K / n) - K. The sugar contest treats each group as a Tullock
  contestant with its stake per head.
- **Tokens and Tullock.** Payoffs as stated in the chapter; the symmetric Nash equilibrium of the lottery contest.
- **Voting.** Both parties maximize expected votes; with log utility the equilibrium maximizes
  sum alpha_g w_g log c_g subject to the budget, where w_g is a group's density of swing voters plus its lobbying
  weight.
- **The Senate.** Local linear regressions on each side of a zero margin, triangular kernel, bandwidth 17.754 points
  (rdrobust's MSE-optimal choice for these data), with heteroskedasticity-robust standard errors; bins of 2.5 points.
- **Mayors.** What office is worth, W, normal(0.1, 0.3) and at least 0; honesty uniform on [0.3, 1]; delta = 0.43.
- **The franchise.** The poor's values of revolution, of promises honoured only in crises (a two-state Bellman
  system) and of democracy (the poor's ideal tax forever), with tax costs tau^2/2 and a discount of 0.95.
- **Conflict.** Rainfall and other shocks to growth, conflict drawn with probability 0.25 - 2 x growth, growth measured
  with normal error of 4 points; the Wald/2SLS estimate with a robust standard error.
- **The cycle.** Unemployment chosen over sixteen years to maximize voters' myopically weighted judgement at each
  election, with an accelerationist Phillips curve, by BFGS.

## Problems and solutions

**1.** *Olson: a policy worth B = 100 to a group, won with probability E/(E + 1). Find each member's effort and the
group's total for n = 4 and n = 25. At what size does the group give up?*

*Solution.* Each member maximizes (100/n) E/(E + 1) minus their own effort; the first-order condition is
(100/n)/(E + 1)^2 = 1, so the group's total is E = sqrt(100/n) - 1. For n = 4, E = 5 - 1 = 4, or 1 each; for n = 25,
E = 2 - 1 = 1, or 0.04 each. The total reaches zero when sqrt(100/n) = 1, at n = 100: a group of a hundred or more does
nothing, though the policy is still worth 100 to it.

**2.** *Tullock: five players compete for a prize of 100. Find each one's spending in equilibrium and the share of the
prize dissipated. What if one player's spending counts double?*

*Solution.* Each spends R (n - 1)/n^2 = 100 x 4/25 = 16, so the five spend 80: 80% of the prize is dissipated. If
player 1's spending counts double, solving the first-order conditions gives player 1 spending about 24.7 and each of
the others about 9.9; player 1 wins with probability 5/9 and the others 1/9 each, and total spending falls to about
64. An uneven contest wastes less, because the weaker players give up some of the fight.

**3.** *Rent seeking: a quota raises a price from 2 to 6 on demand q = 10 - p. Find the triangle and the rectangle, and
the social cost if the rectangle is competed away.*

*Solution.* At p = 2, q = 8; at p = 6, q = 4. The triangle is (8 - 4)(6 - 2)/2 = 8; the rectangle is (6 - 2) x 4 =
16. If firms spend the whole rectangle competing for the quota, the social cost is 8 + 16 = 24, three times the
triangle.

**4.** *Agency: office is worth W = 0.2 a term, rents up to 1, delta = 0.6. Find the rents voters must tolerate. How
high must W be for them to tolerate none?*

*Solution.* r* = (1 - delta)(W + R) - W = 0.4 x 1.2 - 0.2 = 0.28. Voters tolerate none when 0.4 (W + 1) <= W, that is
W >= 2/3: when a term is worth two-thirds of the maximum grab, compliance needs no rents.

**5.** *Close elections: explain why a regression discontinuity needs the density of the margin to be smooth at zero,
and what bunching just above zero would mean.*

*Solution.* The design treats who barely wins as if by chance, so the elections just above and just below zero must be
alike. If one party could influence the outcome in very close races (by recounts, fraud or better information), more
of its races would land just above zero than just below, the density would jump at zero, and bare winners would
differ from bare losers before the election. McCrary's test checks the density; balance tests on earlier outcomes
check the rest (as Caughey and Sekhon did for the House).

**6.** *Persuasion: a channel reaches 40% of homes against 10%, and a party's share is 52% against 51%. Find the
persuasion rate.*

*Solution.* f = ((0.52 - 0.51)/(0.40 - 0.10)) / (1 - 0.51) = (0.01/0.30)/0.49 = 0.068: about 7% of the viewers who would
not otherwise have voted for the party were persuaded.

**7.** *The franchise: explain why the elite democratizes when crises are rare but not when they are frequent.*

*Solution.* Without the vote, the elite can redistribute only while a crisis lasts, because once it passes the elite
can reverse itself. The poor value promises by how often they will be renewed. When crises are frequent, promises
recur and are worth nearly as much as permanent redistribution, so they can be enough to forestall revolution. When
crises are rare, a promise made today is worth little, the poor would revolt, and the elite's best option is to
extend the vote, which commits it to redistribution in every period.

**8.** *Two groups lobby with stakes per head v_s and v_l in a Tullock contest. Derive the efforts and the probability
the small group wins.*

*Solution.* With free riding each member's first-order condition uses the stake per head, and only the group's total
matters, so each group behaves like a single contestant with valuation v. Then v_s E_l/(E_s + E_l)^2 = 1 and
v_l E_s/(E_s + E_l)^2 = 1. Dividing, E_s/E_l = v_s/v_l; substituting, E_s + E_l = v_s v_l/(v_s + v_l), so
E_s = v_s^2 v_l/(v_s + v_l)^2 and E_l = v_s v_l^2/(v_s + v_l)^2, and the small group wins with probability
E_s/(E_s + E_l) = v_s/(v_s + v_l). With sugar's stakes, about $500,000 a farm against $9 a head, that is almost one.

## Lab and interactive

- `python -m videos.economics.labs 47`: Olson's effort by group size; the sugar contest; the tokens game; Tullock's
  dissipation; probabilistic voting with and without a lobby; the Senate's discontinuity at several bandwidths; the
  agency threshold and the mayors; the franchise map; the rainfall instrument; the election cycle.
- The interactive (course site): build or lobby. The reader chooses how many of a hundred tokens to keep, build with
  and lobby with, while nine other players follow a rule the reader sets, and sees what everyone ends with.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[47]`; the two dials
(`corruption_share`, `incumbency`) are in `explainer/economics/dials.py`; the Treasury's forecast is a *Called it?* entry
(`explainer/economics/calls.py`). rdrobust 4.1.2 was retrieved from CRAN and checked by SHA-256; the Senate estimates
are computed here. The World Bank's tax and governance series were retrieved through its API on 2026-11-20; the US and
EU sugar columns were added from the same Pink Sheet workbook already in the Data Room; more countries were added to
the V-Dem extract from the same file. The studies' statements were checked on 2026-11-21 against their abstracts and
the authors', J-PAL's or GAO's summaries: Olken (over 600 projects, 4% to 100%, about 8 points, 27.7% to 19.2% in
J-PAL's summary; perceptions 0.8%; rice at least 18%); GAO-24-106144 ($2.5-3.5 billion, $1.4-2.7 billion, about $1
billion, twice the world price) and the 2022 farm counts (3,257 and 745); Krueger (7.3%, 5.1%, 15%); Lee, Moretti and
Butler; Lee (7.7, as reported by reanalyses); Caughey and Sekhon; Goldberg and Maggi (50 to 88 times); Fisman; Ferraz
and Finan (27%) and the 2025 replication; Fisman and Miguel; Reinikka and Svensson (a fifth; 13% in 1991-95); Acemoglu
et al. (20%, 25 years); Besley and Persson; Miguel, Satyanath and Sergenti (41 countries, 5% and up to 10 points);
Sachs and Warner (1971-89); DellaVigna and Kaplan (0.4-0.7 points; 3-28%); Autor et al.; the Treasury's analysis (3.6%,
6%, 500,000) and the IFS and OBR assessments (about 2% growth in 2016); Funke, Schularick and Trebesch (51 leaders,
10%, 15 years); Muralidharan, Niehaus and Sukhtankar (157 sub-districts, 19 million people). Not verified, so not
stated: Olken's exact control mean in the paper itself (J-PAL's figure is stated as J-PAL's), and Lee's probability
of winning.
