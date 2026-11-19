# Economics, Built: Part 18, Social Choice and Welfare

Part 18 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the last of Act IV, *Failure and Design*. It asks whether the wants of many people can
be added up into what society wants, and answers: not without a choice. Between two options, or along a single line,
majority rule works; beyond that, every rule breaks a reasonable condition, and every rule can be gamed. To add people
up we must compare them: welfare functions, cost-benefit analysis and indices do, but each carries an ethical number
(how much we care about equality, about the future, about a risk to life) that economics can make visible and measure
the effects of, but cannot choose.

It opens with the Marquis de Condorcet's essay of 1785, in which three voters' majorities go round in a circle, and
with Kenneth Arrow's discovery in 1950 that the trouble is not majority rule: every rule for turning rankings into a
social ranking fails a reasonable condition unless one person decides. From there it covers:

- a game: thirty-eight islanders, four kinds of ballot, five plans, and five rules that pick five different winners;
- Borda against Condorcet; Borda's failure of independence, found on the same ballots; the agenda setter (Black 1958;
  McKelvey 1976);
- Arrow's conditions and theorem, proved by the pivotal voter (Geanakoplos 2005), step by step;
- the ways out: single peaks and the median voter (Black 1948; Downs 1957); May's theorem (1952);
- strategic voting: Gibbard (1973) and Satterthwaite (1975), with the island's blocs who gain by lying, and *Called
  it?* on Duverger's law;
- comparing people: Robbins (1932) against Sen (1970), and what each kind of comparison allows (Hammond 1976;
  d'Aspremont and Gevers 1977);
- an intermission without narration: V-Dem's electoral democracy index, 1789-2025, for the world, the United States,
  the United Kingdom, France and India;
- welfare functions from Bentham to Rawls through Atkinson's epsilon (1970), and Okun's leaky bucket (1975);
- Harsanyi's veil (1953, 1955) against Rawls's (1971), on two societies, and the laboratory's answer (Frohlich and
  Oppenheimer 1992);
- Pareto and its limits: Kaldor and Hicks (1939), Scitovsky's reversal (1941), Sen's Paretian liberal (1970);
- cost-benefit analysis with and without distributional weights (Kaplow and Shavell 1994), an is/ought card, and the
  discount rate (Ramsey 1928; Stern 2006);
- the value of a statistical life (Schelling 1968; Thaler and Rosen 1976; Ashenfelter and Greenstone 2004) and what it
  is not;
- capabilities and the Human Development Index (Sen; ul Haq; Ravallion 2012);
- a new dial (the value of a statistical life), the rules regulators and voters actually use, and a frontier chapter
  on behavioural welfare (Bernheim and Rangel 2009), quadratic voting (Lalley and Weyl 2018) and preference
  aggregation for AI (Siththaranjan, Laidlaw and Hadfield-Menell 2024; Conitzer et al. 2024).

## Build it

```bash
python -m videos.economics.econ18.compute              # every number (seconds), into .cache/econ18/
python tools/qa_scene.py econ18 ArrowTheorem           # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ18 -q l   # the whole part, silent preview
python tools/build.py econ18                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 18                     # the lab
```

The data are frozen extracts in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): V-Dem's electoral democracy index (version 16, 2026) via
Our World in Data; the UNDP's Human Development Report 2025 data; and transcribed values of a statistical life (the
Department of Transportation's guidance, the EPA's central value, Ashenfelter and Greenstone's estimate) and of
Duverger's law, in `explainer/economics/data/tables.py` with where they were read and the date they were checked.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Can the wants of many people be added up into what society wants? | Condorcet's three voters (1785): A beats B, B beats C, C beats A, each 2 to 1; Arrow (1950): every rule breaks a reasonable condition unless one person decides; where people are added up (elections, committees, appraisal, inequality, lives, machines); the question; objectives |
| 1 | Play it: one island, five rules, five winners | 38 islanders: 12 A E D B C, 11 B D E C A, 8 C E D B A, 7 D C B E A (A fish, B fruit, C dance, D boat race, E market fair); plurality A (12), runoff B (26 to 12), instant runoff C (26 to 12), Borda D (101, E 89, B 78), Condorcet E (beats A 26-12, B 20-18, C 23-15, D 20-18) |
| 2 | Borda against Condorcet, and the agenda | Borda (1770) and Condorcet (1785) disagree; the 12 fish-first voters move the fruit above the boat race and Borda's order of B and E flips (D 101, E 89, B 78 to B 90, D 89, E 89) though no one's B-against-E ranking changed; with Condorcet's three voters, whichever plan is voted on last wins |
| 3 | Arrow's theorem | Four conditions; Geanakoplos's proof animated with five voters: b moved to the top voter by voter jumps from bottom to top for society at voter 3, who is pivotal and then a dictator; something must give |
| 4 | Ways out: single peaks and May's theorem | Five ideal granary sizes 1, 2, 3, 7, 9 (hundreds of baskets): the median, 3, beats every other size, not the mean 4.4 (Black 1948); Downs (1957); two dimensions and McKelvey's chaos; May (1952): only simple majority rule is anonymous, neutral and positively responsive |
| 5 | Strategic voting | Gibbard and Satterthwaite; on the island, the 11 fruit-first voters make the boat race win under plurality, the 12 fish-first voters make the market fair win under Borda (burying the boat race) and under instant runoff (compromising early); only the Condorcet winner is safe; *Called it?*: Duverger (1951), partly right |
| 6 | Comparing people: Sen's enlargement | Robbins (1932); Sen (1970): the impossibility comes from too little information; rankings only (a dictator), levels (Rawls), units (Bentham), both (a family between) |
| | Intermission: two centuries of democracy | No narration: V-Dem's electoral democracy index, 1789-2025, for the world (0.05 in 1789, a peak of 0.53 in 2012, 0.48 in 2025) and four countries; the world's index as a tune; the story so far |
| 7 | Welfare functions: Bentham, Rawls and Atkinson | Incomes 5, 10, 20, 40, 80; Atkinson's equally distributed equivalent 31 (epsilon 0), 25.3 (0.5), 20 (1), 12.9 (2), 7.4 (5), index 0.35 at epsilon 1; Okun's leaky bucket from 80 to 5: up to 75% may leak at epsilon 0.5, 94% at 1, 99.6% at 2 |
| 8 | Two veils: Harsanyi and Rawls | Society A (20 each) against B (8, 30, 30, 30, 30; mean 25.6): Rawls chooses A; Harsanyi chooses B below epsilon 1.9 and A above; Harsanyi's critique (1975) and Rawls's answer; groups in the laboratory choose an average with a floor |
| 9 | Pareto and its limits | Kaldor and Hicks (1939); Scitovsky's reversal rebuilt with Ana and Bo: state 1 (6, 1) and (1, 6), state 2 (1, 4) and (7, 3), utility fish times fruit; the compensation test approves the move and its reverse; Sen's prude and lewd: liberty and Pareto make a cycle |
| 10 | Cost-benefit analysis as applied social choice | A jetty worth 30 to Ana (income 80) and costing Friday (income 5) 10: +20 unweighted, -6.2 at epsilon 0.5, -50.4 at epsilon 1; Kaplow and Shavell's case for no weights; an is/ought card; Ramsey's rule and Stern's 1.4%: a million dollars in 100 years is worth $249,003, $52,033 or $12,257 today at 1.4%, 3% or 4.5% |
| 11 | The value of a statistical life | $1,000 a year for a 1-in-10,000 risk: $10 million (Schelling 1968); wages, surveys, behaviour; 65 mph limits from 1987: speeds up 2.5 mph, fatality rates up 35%, about 125,000 hours saved per extra death, about $1.54 million (1997 dollars) as an upper bound; what it is not; the EPA's age adjustment dropped in 2003 |
| 12 | Capabilities: what to measure | Sen's capabilities; income against life expectancy for 193 countries in 2023: Sri Lanka ($12,616, 77.5 years) and Equatorial Guinea ($12,762, 63.7); Cuba, the United States, Costa Rica, Qatar; the HDI (1990; geometric mean since 2010): Qatar 4th by income, 43rd by HDI; Cuba 127th and 97th; the United States 10th and 18th; Ravallion's critique |
| 13 | The Dials: the value of a statistical life | The new dial in 2024 dollars: Ashenfelter and Greenstone 3.0 (1.0 to 5.0), the EPA 11.5, the Department of Transportation 13.7; contested; why the methods disagree |
| 14 | In practice: rules for regulators and voters | Regulatory review since 1981; Circular A-4 (3% and 7% in 2003, 2% and distributional weights in 2023, the 2003 version restored in 2025); the Green Book's 3.5%; *Whitman v. American Trucking* (2001) and *Michigan v. EPA* (2015); Australia's instant runoff (1918), Maine (2018), Alaska (2022; kept in 2024 and 2026), Fargo's approval voting (2020) and North Dakota's ban (2025); the first bans on ranked voting (2022) |
| 15 | Frontier: new votes, and choosing for machines | Bernheim and Rangel's welfare from choices (2009); quadratic voting, votes in proportion to intensity, collusion, Colorado's House Democrats (2019); RLHF as Borda's count (Siththaranjan, Laidlaw and Hadfield-Menell 2024), social choice for alignment (Conitzer et al. 2024), Collective Constitutional AI (2023) |
| | Recap, problems, and the road ahead | The answer; twelve lines; problems; reading; Malthus (1798), and Part 19 |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's social choice module (`explainer.economics.agora.choice`),
with the Island's Part 18 truths in `explainer.economics.island`, or from the Data Room or a transcribed table; the
narration states the cached numbers.

- **Voting.** Plurality, the two-round runoff, instant runoff, Borda's count, Condorcet's and Copeland's rules on the
  island's 38 ballots; every agenda of Condorcet's three voters; a search for Borda's failure of independence; the
  first step of Geanakoplos's proof on five voters; the single-peaked line; for each rule and each kind of ballot, the
  lie by the whole group that gives it the winner it most prefers, counted only when that winner wins outright (the
  rules break ties by letter, so each result is checked with the letters' order reversed).
- **Welfare.** Atkinson's equally distributed equivalent and index for epsilon from 0 to 8; Okun's leaky bucket;
  Harsanyi's and Rawls's choices behind the veil and the epsilon at which Harsanyi's changes; Kaldor's test both ways
  for Scitovsky's two states, by a grid over the ways to share the goods; Sen's liberal paradox; the jetty with and
  without weights; present values over a century.
- **Data.** V-Dem's index; the Human Development Report's income, life expectancy and HDI ranks for 2023; the
  transcribed values of a statistical life, converted to 2024 dollars with the CPI-U.

## Problems and solutions

**1.** *Five rules: with the island's 38 ballots, find the winner under plurality, the runoff, instant runoff, Borda's
count and Condorcet's head-to-head rule.*

*Solution.* The ballots are 12 A E D B C, 11 B D E C A, 8 C E D B A and 7 D C B E A. Plurality counts first places: A
12, B 11, C 8, D 7, E 0, so A wins. The runoff puts A against B: only the 12 rank A above B, so B wins 26 to 12.
Instant runoff drops E (no first places), then D (7), whose ballots pass to C (15); then B (11), whose ballots pass to C
(their next choice among A and C), and C beats A 26 to 12. Borda's count (4, 3, 2, 1, 0) gives A 48, B 78, C 64,
D 101, E 89: D wins. Head to head, E beats A 26 to 12, B 20 to 18, C 23 to 15 and D 20 to 18: E is the Condorcet
winner.

**2.** *The agenda: with Condorcet's three voters, show that whichever plan is voted on last wins.*

*Solution.* The voters rank A B C, B C A and C A B, so A beats B, B beats C and C beats A, each 2 to 1. If C comes last,
A meets B first and wins, then loses to C. If A comes last, B meets C and wins, then loses to A. If B comes last, C
meets A and wins, then loses to B. In each case the plan held back to the end wins, because the plan that beats it has
already been eliminated.

**3.** *Arrow, step one: prove that if every voter puts $b$ at the very top or the very bottom, so does society.*

*Solution.* Suppose not: for some $a, c$ other than $b$, society ranks $a \succsim b$ and $b \succsim c$. Change every
voter's ranking so that $c$ moves just above $a$, leaving $b$ where it is. Since $b$ is at an extreme for every voter,
nobody's ranking of $a$ against $b$ or of $b$ against $c$ changes, so by independence society still has
$a \succsim b \succsim c$, and by transitivity $a \succsim c$. But every voter now prefers $c$ to $a$, so by Pareto
society has $c \succ a$: a contradiction.

**4.** *Black's theorem: with single-peaked preferences on a line, prove that the median peak beats every other
option.*

*Solution.* Let $n$ be odd and $m$ the median peak. Take any option $x < m$. Every voter whose peak is $m$ or more has
$x < m \le$ peak, so $m$ lies between $x$ and the peak, and single-peakedness means the voter prefers $m$ to $x$. At
least $(n + 1)/2$ voters have peaks of $m$ or more, a majority. The case $x > m$ is the same with the voters whose peaks
are $m$ or less. So $m$ beats every other option: it is the Condorcet winner.

**5.** *Strategy: find a lie by the 12 fish-first islanders that changes Borda's winner to one they prefer.*

*Solution.* Honestly, D has 101 points and E 89, and the 12 rank A E D B C, preferring E to D. Putting E first would
lift it by 12, only to a tie with D at 101; lowering D works better. Voting A E C B D moves D from third place to last,
taking 2 points from each of 12 ballots: D falls to 77. C rises by 2 per ballot to 88, B stays at 78, and E, with
89, wins outright. (Voting A E C D B instead takes only 12 from D and leaves D and E tied at 89.)

**6.** *Atkinson: for incomes 5, 10, 20, 40, 80, find the equally distributed equivalent at $\varepsilon = 0, 1, 2$,
and its limit as $\varepsilon \to \infty$.*

*Solution.* $y_\varepsilon = \big(\tfrac15 \sum y_i^{1 - \varepsilon}\big)^{1/(1 - \varepsilon)}$. At 0 it is the
mean, 31. At 1 it is the geometric mean, $(5 \cdot 10 \cdot 20 \cdot 40 \cdot 80)^{1/5} = 20$. At 2 it is the
harmonic mean, $5 / (\tfrac15 + \tfrac1{10} + \tfrac1{20} + \tfrac1{40} + \tfrac1{80}) = 5 / 0.3875 \approx 12.9$. As
$\varepsilon \to \infty$ the smallest income dominates the sum of $y_i^{1 - \varepsilon}$, so $y_\varepsilon \to 5$,
the minimum: Rawls's rule.

**7.** *The veil: find the $\varepsilon$ at which Harsanyi's chooser switches from society B to society A.*

*Solution.* Society A gives 20 for sure; B gives 8 with probability $\tfrac15$ and 30 with probability $\tfrac45$.
Harsanyi's chooser prefers B while B's equally distributed equivalent,
$\big(\tfrac15 8^{1 - \varepsilon} + \tfrac45 30^{1 - \varepsilon}\big)^{1/(1 - \varepsilon)}$, exceeds 20. At
$\varepsilon = 1$ it is $8^{0.2}\, 30^{0.8} \approx 23.1$; at $\varepsilon = 2$ it is $1 / (0.2/8 + 0.8/30) \approx 19.4$.
Solving numerically, the two are equal near $\varepsilon \approx 1.9$; above that, Harsanyi joins Rawls in choosing A.

**8.** *$\bigstar$ Scitovsky: verify that the compensation test approves the move from state 1 to state 2 and the move
back.*

*Solution.* Utility is fish times fruit. In state 1, Ana (6, 1) and Bo (1, 6) each have 6; the totals are (7, 7). In
state 2, Ana (1, 4) has 4 and Bo (7, 3) has 21; the totals are (8, 7). From 1 to 2: share state 2's totals as Ana
(0.98, 6.125), utility about 6.00, and Bo (7.02, 0.875), utility about 6.14, so nobody is worse off than in state 1 and
Bo is better off: the test approves. From 2 back to 1: share state 1's totals as Ana (1.19, 3.38), utility about 4.02,
and Bo (5.81, 3.62), utility about 21.05, so nobody is worse off than in state 2: the test approves again. The test
compares states at different prices, because which goods are scarce depends on who holds them.

## Where it comes back

| Idea | Parts |
|---|---|
| Growth and living standards over centuries | 19 *The Great Escape* |
| Behavioural welfare and nudges | 45 *Behavioural Economics* |
| Voting, parties and the median voter | 47 *Political Economy* |
| Discounting the climate | 48 *Environment and Climate* |
| Scoring a bill, the value of a statistical life | 58 *Scoring the Bill* |
| Capabilities and justice | *Philosophy, Built*, Part 38 |

## Sources

- Marquis de Condorcet, *Essai sur l'application de l'analyse à la probabilité des décisions rendues à la pluralité
  des voix* (1785); J.-C. de Borda, "Mémoire sur les élections au scrutin" (1781, read 1770); D. Black, "On the
  Rationale of Group Decision-making", *Journal of Political Economy* 56(1) (1948): 23-34, and *The Theory of
  Committees and Elections* (1958); K. O. May, "A Set of Independent Necessary and Sufficient Conditions for Simple
  Majority Decision", *Econometrica* 20(4) (1952): 680-684; A. Downs, *An Economic Theory of Democracy* (1957);
  R. D. McKelvey, "Intransitivities in Multidimensional Voting Models", *Journal of Economic Theory* 12(3) (1976):
  472-482.
- K. J. Arrow, "A Difficulty in the Concept of Social Welfare", *Journal of Political Economy* 58(4) (1950): 328-346,
  and *Social Choice and Individual Values* (1951; 3rd ed. 2012); J. Geanakoplos, "Three Brief Proofs of Arrow's
  Impossibility Theorem", *Economic Theory* 26(1) (2005): 211-215.
- A. Gibbard, "Manipulation of Voting Schemes: A General Result", *Econometrica* 41(4) (1973): 587-601; M. A.
  Satterthwaite, "Strategy-proofness and Arrow's Conditions", *Journal of Economic Theory* 10(2) (1975): 187-217;
  M. Duverger, *Les partis politiques* (1951); W. H. Riker, "The Two-Party System and Duverger's Law", *American
  Political Science Review* 76(4) (1982): 753-766.
- L. Robbins, *An Essay on the Nature and Significance of Economic Science* (1932); A. Sen, *Collective Choice and
  Social Welfare* (1970; expanded ed. 2017); P. J. Hammond, "Equity, Arrow's Conditions, and Rawls' Difference
  Principle", *Econometrica* 44(4) (1976): 793-804; C. d'Aspremont and L. Gevers, "Equity and the Informational Basis
  of Collective Choice", *Review of Economic Studies* 44(2) (1977): 199-209.
- A. B. Atkinson, "On the Measurement of Inequality", *Journal of Economic Theory* 2(3) (1970): 244-263; A. M. Okun,
  *Equality and Efficiency: The Big Tradeoff* (1975).
- J. C. Harsanyi, "Cardinal Utility in Welfare Economics and in the Theory of Risk-taking", *Journal of Political
  Economy* 61(5) (1953): 434-435; "Cardinal Welfare, Individualistic Ethics, and Interpersonal Comparisons of
  Utility", *Journal of Political Economy* 63(4) (1955): 309-321; "Can the Maximin Principle Serve as a Basis for
  Morality?", *American Political Science Review* 69(2) (1975): 594-606; J. Rawls, *A Theory of Justice* (1971);
  N. Frohlich and J. A. Oppenheimer, *Choosing Justice* (1992).
- N. Kaldor, "Welfare Propositions of Economics and Interpersonal Comparisons of Utility", *Economic Journal* 49(195)
  (1939): 549-552; J. R. Hicks, "The Foundations of Welfare Economics", *Economic Journal* 49(196) (1939): 696-712;
  T. de Scitovszky, "A Note on Welfare Propositions in Economics", *Review of Economic Studies* 9(1) (1941): 77-88;
  A. Sen, "The Impossibility of a Paretian Liberal", *Journal of Political Economy* 78(1) (1970): 152-157.
- L. Kaplow and S. Shavell, "Why the Legal System Is Less Efficient than the Income Tax in Redistributing Income",
  *Journal of Legal Studies* 23(2) (1994): 667-681; F. P. Ramsey, "A Mathematical Theory of Saving", *Economic
  Journal* 38(152) (1928): 543-559; N. Stern, *The Economics of Climate Change: The Stern Review* (2007).
- T. C. Schelling, "The Life You Save May Be Your Own", in S. B. Chase (ed.), *Problems in Public Expenditure Analysis*
  (1968); R. Thaler and S. Rosen, "The Value of Saving a Life: Evidence from the Labor Market", in N. Terleckyj (ed.),
  *Household Production and Consumption* (1976); O. Ashenfelter and M. Greenstone, "Using Mandated Speed Limits to
  Measure the Value of a Statistical Life", *Journal of Political Economy* 112(S1) (2004): S226-S267; U.S. EPA,
  *Mortality Risk Valuation*; U.S. Department of Transportation, guidance on the value of a statistical life.
- A. Sen, *Commodities and Capabilities* (1985) and *Development as Freedom* (1999); UNDP, *Human Development Report*
  (1990; 2025 data); M. Ravallion, "Troubling Tradeoffs in the Human Development Index", *Journal of Development
  Economics* 99(2) (2012): 201-209.
- Executive Orders 12291 (1981), 12866 (1993) and 14192 (2025); OMB Circular A-4 (2003; 2023); HM Treasury, *The Green
  Book*; *Whitman v. American Trucking Associations*, 531 U.S. 457 (2001); *Michigan v. EPA*, 576 U.S. 743 (2015).
- B. D. Bernheim and A. Rangel, "Beyond Revealed Preference: Choice-Theoretic Foundations for Behavioral Welfare
  Economics", *Quarterly Journal of Economics* 124(1) (2009): 51-104; S. P. Lalley and E. G. Weyl, "Quadratic Voting:
  How Mechanism Design Can Radicalize Democracy", *AEA Papers and Proceedings* 108 (2018): 33-37; E. A. Posner and
  E. G. Weyl, *Radical Markets* (2018).
- A. Siththaranjan, C. Laidlaw and D. Hadfield-Menell, "Distributional Preference Learning: Understanding and
  Accounting for Hidden Context in RLHF", ICLR 2024 (arXiv 2312.08358); V. Conitzer et al., "Position: Social Choice
  Should Guide AI Alignment in Dealing with Diverse Human Feedback", ICML 2024, PMLR 235: 9346-9360; S. Huang et al.,
  "Collective Constitutional AI: Aligning a Language Model with Public Input", FAccT 2024.
- V-Dem Institute, *V-Dem dataset* version 16 (2026), electoral democracy index, via Our World in Data.
- Textbooks: Kenneth J. Arrow, *Social Choice and Individual Values*; Amartya Sen, *Collective Choice and Social
  Welfare*; Andreu Mas-Colell, Michael D. Whinston and Jerry R. Green, *Microeconomic Theory* (1995), chs. 21-22;
  Matthew D. Adler, *Measuring Social Welfare: An Introduction* (2019).
