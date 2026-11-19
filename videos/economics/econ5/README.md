# Economics, Built: Part 5, What People Want

Part 5 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first of Act II, *Choosing*. It asks whether you can tell what someone wants from
what they buy, and what "rational" assumes, and answers: you can, as far as the choices are consistent. If they satisfy
the generalized axiom of revealed preference, some utility function explains every one of them (Afriat), and the
choices bound how the person trades one thing for another (Varian); they say nothing about why, and only speak where
the budgets crossed.

It opens with three weeks of Bo's receipts from the Island market, two of which contradict each other, and with the
road from Jevons's marginal utility (1871) through Edgeworth, Pareto and Hicks and Allen (1934) to Paul Samuelson's
note of 1938, written at twenty-two, which proposed "dropping off the last vestiges of the utility analysis". From
there it covers:

- a game: eleven budget lines of fish and coconuts, $60 each; the viewer writes down a choice on each, kept for
  chapter 8;
- preferences as a ranking: completeness, transitivity, continuity; better and worse regions; the money pump
  (Davidson, McKinsey and Suppes, 1955);
- utility as a label: Debreu's representation (1954), ordinal utility, the lexicographic order no number can
  represent, and the marginal rate of substitution as what survives relabelling;
- the shapes of wanting: convexity, Cobb–Douglas, perfect substitutes and complements, quasilinear tastes, and the
  CES family between them (Arrow, Chenery, Minhas and Solow, 1961);
- the budget and the best bundle: the tangency, Lagrange's method, and the multiplier as the value of a dollar;
- corners and kinks: a corner solution, a bulk price that makes demand jump, and the earned income tax credit's first
  kink, where (Saez 2010) only the self-employed bunch;
- an intermission without narration: a century of the American basket, fifteen kinds of spending from 1929 to 2025,
  under the falling share of food at home as a tune;
- revealed preference: WARP (Samuelson), SARP (Houthakker), GARP (Afriat, Varian), four islanders tested on the
  Play-it lines, and Afriat's theorem with the utility its linear programme builds;
- the test on data: scoring the viewer's sheet, the power of the test against random choosers (Bronars), children,
  students and Dutch households, and America as one consumer;
- recovering preferences: Varian's bounds on an indifference curve, and a forecast from consistency alone;
- what rationality does not assume (selfishness, calculation, even a human chooser), and Becker's random
  households, whose market demand still slopes down;
- a new dial (consistency with utility maximization), McFadden's BART forecast as *Called it?*, the people who read
  wants from choices for a living and a logit that recovers the value of time, and a frontier chapter on random
  utility, revealed preference in scanner data, and the consistency of a language model.

## Build it

```bash
python -m videos.economics.econ5.compute              # every number (about a minute), into .cache/econ5/
python tools/qa_scene.py econ5 Revealed               # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ5 -q l   # the whole part, silent preview
python tools/build.py econ5                           # 1080p30 with narration and the series' computed score
python -m explainer.economics.data --refresh fred     # the data again, with a report of changes
python -m videos.economics.labs 5                     # the lab
```

The data are frozen extracts in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): BEA's personal consumption expenditures by type of
product (fifteen categories, each a price index and spending, 1929–2025) and the population, from FRED, retrieved on
19 November 2026; `data.pce_by_type()` turns them into quantities per head. The published results (Harbaugh et al.,
Choi et al. 2007 and 2014, Andreoni and Miller, Chen et al., Saez, McFadden's BART forecast) are transcribed in
`explainer/economics/data/tables.py`, each with where it was read and the date it was checked.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Can you tell what someone wants from what they buy? | Bo's receipts: $36 a week at prices (4, 3), (2, 4), (6, 2), bundles (3, 8), (6, 6), (4, 6); Jevons (1871), Edgeworth and Pareto (1881–1906), Hicks and Allen (1934); Samuelson (1938), "dropping off the last vestiges of the utility analysis"; the question; the title; Act II; objectives |
| 1 | Play it: eleven budgets | $60 a trip; the first line, 6 fish or 6 coconuts; the eleven lines (12 or 3, 4 or 9, ... 6 or 7), chosen so that 97.5% of random choosers violate GARP; write down how many fish on each; a countdown |
| 2 | Preferences as a ranking | Completeness, transitivity, continuity; nothing about why; better and worse corners around a bundle; an indifference curve; the money pump: cloth over fish, coconuts over cloth, fish over coconuts, a coin a swap, 30 coins to 18 in four laps (Davidson, McKinsey and Suppes, 1955) |
| 3 | Utility as a label | Debreu (1954); one map labelled xy (4, 16, 36), log x + log y, (xy)³ (64, 4,096, 46,656); ordinal utility; the lexicographic order, complete and transitive, with no utility function; the MRS, y/x under both labels; half a coconut for a fish at (4, 2) |
| 4 | The shapes of wanting | Convexity: (1.8, 8.9) and (8, 2) equally good, their average (4.9, 5.4) better; a falling MRS; Cobb–Douglas, perfect substitutes, perfect complements, quasilinear; the CES family as σ runs from 0.1 to 20 (Arrow, Chenery, Minhas and Solow, 1961) |
| 5 | The budget and the best bundle | Bo's $60, fish $4, coconuts $3; the budget set and line, its slope −4/3; cheaper fish and more money; three indifference curves; sliding along the line; the best bundle, 9 fish and 8 coconuts, where MRS = 4/3; Lagrange: λ = 0.143, the utility of one more dollar |
| 6 | Corners and kinks | Chidi's perfect substitutes: a coconut worth 1.2 fish, costing 1.67: all fish; the bulk price ($2 for the first 6 coconuts, then $1): 4 coconuts at $16, 11 at $28, a jump from 5.1 to 7.3 at $20.49 of income; the EITC (one child, 2008): +34% to $8,580, flat to $15,740, −16% after; 4,000 simulated earners: 0.1%, 4.2% and 14.6% at the kink for elasticities 0, 0.25 and 1; Saez (2010): bunching only among the self-employed, none at the second kink |
| | Intermission: a century of the American basket | No narration: the fifteen shares, 1929 to 2025, in one bar; food at home 21.4% → 7.5%, health care 3.0% → 17.6%; real spending per head ×6.3; food's share as a tune; the story so far |
| 7 | Revealed preference | Weeks 1 and 3: each bundle cost $34 at the other's prices: WARP fails; shrinking week 1's budget to 94.4% removes it; WARP (1938), SARP (Houthakker 1950), GARP (Afriat 1967; Varian 1982); Warshall's algorithm; Bo, Ana and Chidi pass, Dara (random) fails, 8 of 11 choices in cycles, index 0.955; Afriat's inequalities, the LP, the constructed utility and three of its indifference curves |
| 8 | The test on data | Scoring a sheet: the affordability matrix, gold and red; 5,000 random choosers on the eleven lines: 97.5% violate GARP, average index 0.79, 9.5% above 0.95 (Bronars 1987); Harbaugh et al. (2001): 4.3, 2.1 and 2.0 violations at 7, 11 and 21, random about 8.3; none at all: 26%, 62%, 65%, random 2%; Choi et al. (2007): 0.954; Choi et al. (2014): 1,182 Dutch adults, 0.881, gaps by income, education and age, 15–19% more wealth per SD; America 1929–2025: 0 violations; random choosers fail 100%, copied shares 89%, within decades 0% |
| 9 | Recovering preferences | Bo's bundle (3.8, 2.2): revealed-worse budgets and the revealed-better hull; the planted curve between them (Varian 1982; Blundell, Browning and Crawford 2008); a twelfth trip (10 fish or 5 coconuts): only 3.0 to 7.3 fish keep him consistent; he buys 6 |
| 10 | What rationality does not assume | Not selfishness (Andreoni and Miller 2002: 176 people, over 98% consistent, a quarter selfish); not calculation (children; capuchins, Chen et al. 2006); not a human (87% of rats and 81% of pigeons cut back after a compensated price rise); not fixed tastes; Becker (1962): 2,000 random islanders, mean demand 6/p |
| 11 | The Dials: how consistent are people? | The new dial: 0.93, 0.96, 0.94 (Harbaugh et al.), 0.954 (Choi et al. 2007), 0.881 (Choi et al. 2014), 0.963 (Chen et al. 2023, people, food), against random choice at 0.648 and 0.60; settled within a range; *Called it?*: McFadden's BART forecast, 6.3% against the official 15%; actual 6.2% (1975): right |
| 12 | In practice: reading wants from choices | Market researchers (conjoint), recommender teams (the Netflix Prize), demand analysts, transport planners, pricing teams, welfare economists (Bernheim and Rangel 2009); the ferry survey: 2,000 trips, a logit, $4.95 for 20 minutes, the value of time $14.85 an hour (s.e. 0.34) against a planted $15 |
| 13 | Frontier: random utility and machines that choose | Bo on one line forty times: 61% on fish, give or take 7; random utility (Block and Marschak 1960; McFadden 1974; McFadden and Richter 1990; Kitamura and Stoye 2018); the money pump index (Echenique, Lee and Shum 2011), the minimum cost index (Dean and Martin 2016), welfare without consistency (Bernheim and Rangel 2009); GPT's index 0.997–0.999 against people's 0.963–0.985 (Chen et al. 2023), sensitive to the wording; what is not known; the research problem |
| | Recap, problems, and the road ahead | The answer; eleven lines; problems; reading; Jensen and Miller's rice and Part 6 |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's consumer (`explainer.economics.agora.consumer`), with the
Island's Part 5 truths in `explainer.economics.island`, or from the Data Room or a transcribed table; the narration
states the cached numbers.

- **The Play-it lines** (planted): eleven lines of $60, given by the most fish and most coconuts each affords, found by
  a greedy search over integer intercepts from 3 to 12 for the set on which random choosers most often violate GARP.
- **The islanders** (planted): on the eleven lines, Bo is Cobb–Douglas with 60% on fish and a tremble (his share of
  spending on fish moved by a normal shock with s.d. 6 points), Ana buys fish and coconuts one for one, Chidi values a
  coconut at 1.2 fish (perfect substitutes), and Dara picks a uniform random point; seed 1938.
- **Revealed preference** (`consumer`): x_i is directly revealed preferred to x_j when p_i·x_i ≥ p_i·x_j; the closure
  by Warshall's algorithm; GARP violations are pairs with x_i R x_j and p_j·x_j > p_j·x_i; Afriat's index by bisection
  over the ratios p_i·x_j / p_i·x_i (exact); Houtman–Maks by search; Afriat's inequalities by `scipy.optimize.linprog`
  (HiGHS), with the multipliers at least 1, and the utility min_i[U_i + λ_i p_i·(x − x_i)], whose indifference curves
  are found by bisection.
- **Bronars's power**: 5,000 random choosers, each spending a share drawn uniformly from the simplex on every line
  (seed 1987).
- **The bulk price**: Bo, Cobb–Douglas with half on each good, fish at $2, coconuts at $2 for the first 6 and $1
  after; the best point on the bent frontier by search, for incomes from $8 to $40; the tie at 6/(1 − 1/√2) = $20.49.
- **The EITC** (`consumer.eitc`, `consumer.earnings_choice`): the 2008 one-child schedule from Saez (2010), table 1;
  4,000 earners with potential earnings lognormal (median $12,000, σ 0.6, seed 2010), each choosing earnings z to
  maximize z + credit(z) − n/(1 + 1/e)·(z/n)^(1+1/e), so z = n·r^e for a net reward r, on a $10 grid.
- **Becker's households**: 2,000, each spending a uniform random share of $12 on fish at prices from $1 to $6.
- **Varian's bounds**: for Bo's first choice, the union of the budget sets of the choices it is revealed preferred to,
  and the monotone convex hull of the choices revealed preferred to it; the forecast scans the twelfth line on a grid
  of 801 points for choices that keep all twelve consistent with GARP.
- **America as one consumer**: per-head quantities are spending per head divided by each category's price index
  (2017 dollars); random choosers draw shares from the simplex; "copied shares" give each year another year's
  spending shares at its own budget; windows 1929–40, 1970–85 and 2000–25.
- **The ferry survey** (planted): 2,000 trips; the fast ferry saves 10, 20 or 30 minutes for an extra fare uniform on
  $0–15; utility difference 0.5·(15/60·minutes − fare) plus a logistic shock; the binary logit by Newton's method,
  the value of time −a/b·60 with a delta-method standard error.
- **The intermission**: the fifteen shares of PCE, 1929–2025, one year every 0.40 s; the data melody maps the share
  spent on food at home to D dorian, one note a year.
- **The score** (`explainer/economics/score.py`): the scissors theme, chapter stings, beds under the pauses, and the
  close. Synthesized from sines; nothing recorded.

## Problems and solutions

**1.** *Bo's receipts: prices (4, 3), (2, 4), (6, 2); bundles (3, 8), (6, 6), (4, 6); $36 each week. Find every
direct revealed preference, the WARP violation, and Afriat's index.*

*Solution.* The cost of each bundle at each week's prices, rows by prices and columns by bundles: (36, 42, 34),
(38, 36, 32), (34, 48, 36). So week 1's bundle is directly revealed preferred to week 3's (34 ≤ 36), week 2's to week
3's (32 ≤ 36), and week 3's to week 1's (34 ≤ 36). Weeks 1 and 3 each reveal the other worse: WARP fails. Shrinking
week 1's budget to 34/36 = 0.944 of itself (or week 3's to the same share) removes the contradiction, so Afriat's index
is 0.944: at worst, 5.6% of a week's money was wasted.

**2.** *u = x^0.6 y^0.4, p_x = 4, p_y = 3, m = 60. Find the best bundle, the MRS there, and λ. Show that doubling every
price and income changes nothing.*

*Solution.* Cobb–Douglas spends the shares 0.6 and 0.4: x = 0.6·60/4 = 9, y = 0.4·60/3 = 8. The MRS is
(0.6/0.4)(y/x) = 1.5·8/9 = 4/3, the price ratio. λ = (∂u/∂x)/p_x = 0.6·u/(x·p_x) with u = 9^0.6·8^0.4 ≈ 8.585, so
λ ≈ 0.143. Doubling p_x, p_y and m leaves m/p_x and m/p_y unchanged, so the demands are unchanged: demand is homogeneous
of degree zero in prices and income (λ halves, since a dollar is worth half as much).

**3.** *CES with weights ½ and σ = 2; p_x = 1, p_y = 4, m = 10. Find the bundle. By how much does x/y change if p_y
doubles?*

*Solution.* The tangency gives x/y = (p_y/p_x)^σ = 4² = 16, and the budget x + 4y = 10, so y = 0.5 and x = 8. If p_y
doubles, x/y = 8² = 64: the ratio rises by 2^σ = 4, which is what an elasticity of substitution of 2 means (a 1%
change in the relative price changes the relative quantity by 2%). The new bundle is x = 80/9 ≈ 8.89, y = 5/36 ≈
0.139.

**4.** *Ana: u = min(x, y); Chidi: u = x + 1.2y. Fish $6, coconuts $10, $60. What does each buy? Below what coconut
price does Chidi switch?*

*Solution.* Ana buys equal amounts: x = y = 60/16 = 3.75. Chidi compares utility per dollar: fish 1/6 ≈ 0.167,
coconuts 1.2/10 = 0.12, so he buys only fish, 10 of them. He switches when 1.2/p_y > 1/6, that is when coconuts cost
less than $7.20; at exactly $7.20 any split on the budget line is best.

**5.** *Coconuts: $2 each for the first 6, then $1; fish $2; Bo spends half on each. At what income does he jump past
the sixth coconut, and from how many to how many?*

*Solution.* Below the bend Bo spends m/2 on coconuts at $2: c = m/4 and x = m/4, so u = √(xc) = m/4. Beyond it, s
dollars on coconuts buy c = 6 + (s − 12) = s − 6, and fish x = (m − s)/2; maximizing (m − s)(s − 6) gives s = (m + 6)/2,
c = (m − 6)/2, x = (m − 6)/4 and u = (m − 6)/(2√2). The two are equal when m(4 − 2√2) = 24, at m = 24/(4 − 2√2) ≈ $20.49.
There he jumps from c = m/4 ≈ 5.1 to c = (m − 6)/2 ≈ 7.2 coconuts: no income makes him buy six. A budget set that is not
convex makes demand jump.

**6.** *The EITC subsidizes earnings at 34% up to $8,580. Earners have z = n r^e for a net reward r. With potential
earnings n uniform on $4,000–$14,000, what share bunch at the kink when e = 0.25, and when e = 1?*

*Solution.* Below the kink the reward is 1.34, above it 1. Anyone with n·1.34^e > 8,580 but n < 8,580 would like to
be above the kink at the subsidy's rate and below it without: they stop at the kink. The window is
[8,580/1.34^e, 8,580]: for e = 0.25, [7,975, 8,580], 605/10,000 ≈ 6.1% of earners; for e = 1, [6,403, 8,580], about
21.8%. The share at the kink, divided by the density there, measures the elasticity: that is the logic of Saez's
estimate.

**7.** *Becker: each household spends a uniform random share of m on x. Show that market demand is m/(2p) per household,
with price elasticity −1, although no household obeys WARP.*

*Solution.* Each household's demand is x = s·m/p with s uniform on [0, 1] drawn afresh on every budget. Averaging over
households (or over many budgets), E[x] = E[s]·m/p = m/(2p), so log demand falls one for one with log price:
elasticity −1. A single household's choices are random, so on two crossing budgets it chooses each bundle when the
other was affordable with positive probability: WARP fails, yet the market demand slopes down. Budgets alone produce
the law of demand on average.

**8.** ★ *Design eleven budgets that catch as many random choosers as possible, and also catch Cobb–Douglas choosers
with a 5% tremble. Are the two goals in conflict?* (Research problem.)

*Solution sketch.* Power against random choice grows with the number of budgets and with how often they cross; a
greedy search over integer intercepts (this part's lines) reaches about 97.5%. Catching nearly rational choosers is a
different goal: their trembles produce violations only where two budgets cross close to their chosen bundles, so the
design should place crossings near where such a chooser buys (here, near 60% of spending on fish), which may cost power
against random choice spread over the whole line. Start from `consumer.bronars` and the choosers in
`videos/economics/econ5/compute.py`; score a design by both powers, and search (greedy, simulated annealing, or an
integer programme over a grid of lines). Open questions: optimal designs for the CCEI rather than for pass/fail;
adaptive designs that choose the next budget from the choices so far (as in Choi et al.'s later work); and designs for
random-utility tests.

## Where it comes back

| Idea | Where |
|---|---|
| price changes, Slutsky, Giffen goods, consumer surplus | Part 6, *Demand* |
| choice over risk and time | Part 7, *Time and Risk* |
| demand estimation with discrete choice (BLP) | Part 43, *Measuring Market Power* |
| reference dependence, present bias, welfare with inconsistent choices | Part 45, *Behavioural Economics* |
| the EITC and taxable income | Part 41, *Taxes* |
| the value of time and of a statistical life | Part 18, *Social Choice and Welfare*; Part 58, *Scoring the Bill* |
| experiments on platforms, prices and preferences | Part 61, *Economics at the Platforms* |

## Sources

**Primary texts.**
- P. A. Samuelson, "A Note on the Pure Theory of Consumer's Behaviour", *Economica* NS 5(17) (1938) 61–71; I. Moscati,
  "Not a behaviorist: Samuelson's contributions to utility theory in the Harvard years, 1936–1940" (2019).
- H. S. Houthakker, "Revealed Preference and the Utility Function", *Economica* NS 17(66) (1950) 159–174.
- G. Debreu, "Representation of a Preference Ordering by a Numerical Function", in R. M. Thrall, C. H. Coombs and
  R. L. Davis, eds., *Decision Processes* (Wiley, 1954).
- S. N. Afriat, "The Construction of Utility Functions from Expenditure Data", *International Economic Review* 8(1)
  (1967) 67–77.
- H. R. Varian, "The Nonparametric Approach to Demand Analysis", *Econometrica* 50(4) (1982) 945–973.
- J. R. Hicks and R. G. D. Allen, "A Reconsideration of the Theory of Value", *Economica* NS 1 (1934) 52–76 and
  196–219.
- D. Davidson, J. C. C. McKinsey and P. Suppes, "Outlines of a Formal Theory of Value, I", *Philosophy of Science* 22
  (1955) 140–160.

**Papers.**
- G. S. Becker, "Irrational Behavior and Economic Theory", *Journal of Political Economy* 70(1) (1962) 1–13.
- K. J. Arrow, H. B. Chenery, B. S. Minhas and R. M. Solow, "Capital-Labor Substitution and Economic Efficiency",
  *Review of Economics and Statistics* 43(3) (1961) 225–250.
- S. G. Bronars, "The Power of Nonparametric Tests of Preference Maximization", *Econometrica* 55(3) (1987) 693–698.
- W. T. Harbaugh, K. Krause and T. R. Berry, "GARP for Kids", *American Economic Review* 91(5) (2001) 1539–1545,
  tables 1–2.
- J. Andreoni and J. Miller, "Giving According to GARP", *Econometrica* 70(2) (2002) 737–753.
- S. Choi, R. Fisman, D. Gale and S. Kariv, "Consistency and Heterogeneity of Individual Behavior under
  Uncertainty", *American Economic Review* 97(5) (2007) 1921–1938.
- S. Choi, S. Kariv, W. Müller and D. Silverman, "Who Is (More) Rational?", *American Economic Review* 104(6) (2014)
  1518–1550.
- M. K. Chen, V. Lakshminarayanan and L. R. Santos, "How Basic Are Behavioral Biases? Evidence from Capuchin Monkey
  Trading Behavior", *Journal of Political Economy* 114(3) (2006) 517–537.
- J. H. Kagel, R. C. Battalio and L. Green, *Economic Choice Theory: An Experimental Analysis of Animal Behavior*
  (Cambridge, 1995), as summarized by Harbaugh et al.
- E. Saez, "Do Taxpayers Bunch at Kink Points?", *American Economic Journal: Economic Policy* 2(3) (2010) 180–212.
- R. Blundell, M. Browning and I. Crawford, "Best Nonparametric Bounds on Demand Responses", *Econometrica* 76(6)
  (2008) 1227–1262.
- D. McFadden, "Conditional Logit Analysis of Qualitative Choice Behavior", in P. Zarembka, ed., *Frontiers in
  Econometrics* (1974); "The Path to Discrete-Choice Models", *Access* 20 (2002); "Economic Choices", *American
  Economic Review* 91(3) (2001); D. McFadden and M. K. Richter, "Stochastic Rationality and Revealed Stochastic
  Preference" (1990).
- H. D. Block and J. Marschak, "Random Orderings and Stochastic Theories of Responses" (1960).
- Y. Kitamura and J. Stoye, "Nonparametric Analysis of Random Utility Models", *Econometrica* 86(6) (2018).
- F. Echenique, S. Lee and M. Shum, "The Money Pump as a Measure of Revealed Preference Violations", *Journal of
  Political Economy* 119(6) (2011); M. Dean and D. Martin, "Measuring Rationality with the Minimum Cost of Revealed
  Preference Violations", *Review of Economics and Statistics* 98(3) (2016) 524–534.
- B. D. Bernheim and A. Rangel, "Beyond Revealed Preference", *Quarterly Journal of Economics* 124(1) (2009) 51–104.
- Y. Chen, T. X. Liu, Y. Shan and S. Zhong, "The Emergence of Economic Rationality of GPT", *Proceedings of the
  National Academy of Sciences* 120(51) (2023); arXiv 2305.12763.
- R. Jensen and N. Miller, "Giffen Behavior and Subsistence Consumption", *American Economic Review* 98(4) (2008)
  1553–1577 (for the road ahead).

**Textbooks.** Varian, *Intermediate Microeconomics*, chs. 2–7; Mas-Colell, Whinston and Green, *Microeconomic
Theory*, chs. 1–3; Kreps, *Microeconomic Foundations I*, chs. 1–4; Jehle and Reny, *Advanced Microeconomic Theory*,
ch. 1; Nicholson and Snyder, *Microeconomic Theory*, chs. 2–4; Chambers and Echenique, *Revealed Preference Theory*
(Econometric Society Monographs, 2016).
