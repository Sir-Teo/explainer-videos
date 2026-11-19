# Economics, Built: Part 17, Markets by Design

Part 17 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth of Act IV, *Failure and Design*. It asks whether a market can be engineered
when prices cannot do the work, and answers: yes, within limits. A clearinghouse can make a market thick, uncongested
and safe; deferred acceptance finds a match no pair wants to break and makes the truth safe for the side that asks;
swaps and chains find kidneys no price could. No rule does everything, some trades are always lost to private
information, and a design works only if people trust it and it fits them.

It opens with the American market for medical interns: by 1940 hospitals were hiring students two years before they
graduated; the medical schools stopped releasing grades early in 1945; offers that stayed open ten days, then eight,
became exploding offers by telephone by 1950; and in 1952 the hospitals and students set up a clearinghouse that Alvin
Roth showed in 1984 was Gale and Shapley's algorithm of 1962, found ten years earlier. From there it covers:

- a game: four children, three workshops, and the Boston rule, which punishes the truth;
- mechanisms and the revelation principle (Hurwicz; Myerson 1979), and a designer's checklist;
- Vickrey, Clarke and Groves: Clarke's pivot rule for a footbridge, and why its budget cannot balance (Green and
  Laffont 1977);
- Myerson and Satterthwaite (1983): no voluntary, budget-balanced rule gets every good trade done; the double auction's
  84 percent (Chatterjee and Samuelson 1983);
- stable matching: blocking pairs, deferred acceptance run on a board, and the proof (Gale and Shapley 1962);
- who should propose: the lattice of stable matchings, and truth for the asking side (Dubins and Freedman 1981; Roth
  1982);
- an intermission without narration: marriages per 1,000 people in the United States, 1886-2022;
- the residents' match: Britain's regional clearinghouses as a natural experiment (Roth 1991), with *Called it?*;
  couples and the 1998 redesign (Roth and Peranson 1999);
- school choice: Boston (Abdulkadiroğlu and Sönmez 2003), New York (Abdulkadiroğlu, Pathak and Roth 2005), China's
  parallel mechanism (Chen and Kesten 2017);
- huts and kidneys: top trading cycles (Shapley and Scarf 1974), kidney exchange (Roth, Sönmez and Ünver 2004) and
  chains (Rees et al. 2009);
- why markets fail to form: thickness, congestion, safety; unravelling; repugnance (Roth 2007), with an is/ought card;
- matching with money: the assignment game (Shapley and Shubik 1971);
- what a lottery reveals: Agora's district and Denver's charter schools (Abdulkadiroğlu, Angrist, Narita and Pathak
  2017);
- a new dial (what a sought-after school adds: Boston's exam schools and Denver's charters); clearinghouses and
  platforms; and a frontier chapter on refugees (Bansak et al. 2018) and very large markets (Kojima and Pathak 2009;
  Azevedo and Leshno 2016).

## Build it

```bash
python -m videos.economics.econ17.compute              # every number (seconds), into .cache/econ17/
python tools/qa_scene.py econ17 Stable                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ17 -q l   # the whole part, silent preview
python tools/build.py econ17                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 17                     # the lab
```

The data are frozen extracts in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): the crude marriage rate from the OECD, the US Census
Bureau and CDC via Our World in Data; and transcribed passages from Roth's Nobel lecture (2012) on the medical market,
the clearinghouses, New York's high-school match and kidney chains, and from Abdulkadiroğlu, Angrist and Pathak (2011
working paper of the 2014 article) and Abdulkadiroğlu, Angrist, Narita and Pathak (2016 discussion paper of the 2017
article), in `explainer/economics/data/tables.py` with where they were read and the date they were checked.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Can a market be engineered, when prices cannot do the work? | Interns hired two years early by 1940; grades withheld from 1945; offers open 10 days (1945), 8 (1946), less than twelve hours (by 1950); the 1952 clearinghouse on card-sorting machines; Gale and Shapley (1962) and Roth (1984); markets without prices today; the question; objectives |
| 1 | Play it: rank three workshops | Four children (you, Ana, Bo, Dara), one place at the boatyard, one at the kiln, two at the net loft; lottery Ana, Bo, you, Dara; under the Boston rule the truth gets you the net loft and listing the kiln first gets you the kiln; Dara's kiln is a blocking pair; under deferred acceptance the truth gets you the kiln and nothing does better |
| 2 | Mechanisms, and the revelation principle | Mechanisms as rules played as games (Hurwicz); the revelation principle in one picture; a checklist of efficiency, safe truth, voluntary participation, budget balance and stability against VCG, the double auction, the Boston rule, DA and TTC |
| 3 | Vickrey, Clarke and Groves: pay for the harm you do | A footbridge costing 100, values 60, 10, 10, 40; net values +35, -15, -15, +15 sum to +20; Ana is pivotal and pays 15; truth dominant; the 15 cannot be returned (Green and Laffont 1977); collusion, low revenue, complexity |
| 4 | Myerson and Satterthwaite: no perfect bargain | Values and costs uniform on [0, 1]: every good trade gives 1/6; a posted price of 1/2 gives 1/8 (75%); the double auction's linear equilibrium, trading when v >= c + 1/4, gives 9/64 (84%), the best possible; Vickrey's rule on both sides needs an outside subsidy of the whole surplus |
| 5 | Stable matching: Gale and Shapley | Four apprentices, four workshops; a blocking pair (Dara and the boatyard); deferred acceptance in six rounds, with five rejections; Ana at the net loft, Bo at the grove, Chidi at the kiln, Dara at the boatyard; the proof |
| 6 | Who should propose? | The board's three stable matchings, ordered: the apprentices' best (DA with apprentices asking), the workshops' best (two rounds with workshops asking) and one between; truth dominant for the asking side; no stable rule safe for both; large markets |
| | Intermission: the oldest matching market | No narration: US marriages per 1,000 people, 1886-2022 (7.9 in 1932, 16.4 in 1946, 5.1 in 2020), with Japan, Italy and Sweden from 1960; the US rate as a tune; the story so far |
| 7 | The residents' match | Britain's clearinghouses: stable Edinburgh (1969) and Cardiff still in use; unstable Birmingham, Edinburgh (1967), Newcastle and Sheffield abandoned; Cambridge and the London Hospital the exceptions; *Called it?*: Roth's stability claim: right; the laboratory (Kagel and Roth 2000); couples, women from about 10% of students in the 1970s to about half; Roth and Peranson's redesign of 1998; about 25,000 positions a year by 2012 |
| 8 | School choice | Boston's rule and Abdulkadiroğlu and Sönmez (2003); New York: about 90,000 entering students, about 30,000 placed administratively before, about 3,000 after the 2003-04 clearinghouse; China's parallel mechanism between Boston and DA (Chen and Kesten 2017) |
| 9 | Huts and kidneys | Top trading cycles on four huts (two 2-cycles); kidney exchange, simultaneous surgeries (4 operating rooms for two pairs, 6 for three); Agora's eight pairs: 2 transplants by swaps of two, 6 with cycles of three, all 8 with one altruist's chain; the first long chain (10 transplants, 2009) and one of 30 |
| 10 | Why markets fail to form | Thick, uncongested, safe (Roth 2008); unravelling in judicial clerkships, fellowships, bowl games; repugnance and the kidney market, with an is/ought card (Roth 2007) |
| 11 | Matching with money: the assignment game | Two boats and two buyers, joint surplus (5, 8; 7, 9): the best pairing gives 15; the core runs from Friday's share of 2 (buyers' end) to 8 (sellers' end); core = competitive prices (Shapley and Shubik 1971); the English auction's buyer-optimal end (Demange, Gale and Sotomayor 1986) |
| 12 | What a lottery reveals | Agora's district (20,000 pupils, a true effect of 0.4, siblings first): over 200 lotteries, pupils against everyone 0.80, offered against not ignoring type 0.03, within type 0.40 (spread 0.05); Denver's charters: first stage 0.42, math 0.415 (s.e. 0.052), reading 0.166, writing 0.274, and 0.231 without score controls |
| 13 | The Dials: what a sought-after school adds | Newton and Waltham houses ($412,000 and $316,000); the new dial: Boston exam-school offers, math -0.035 (0.027) and English 0.022 (0.028); Denver charter attendance, math 0.415 (0.052) and reading 0.166 (0.053); depends on the setting |
| 14 | In practice: clearinghouses and platforms | Where matching markets are designed; the economist as engineer (Roth 2002): rules, algorithms, details, simulation, persuasion, evaluation |
| 15 | Frontier: refugees, learning and large markets | Refugee placement by prediction and matching, predicted employment roughly 40-70% higher (Bansak et al. 2018); large markets: little to gain by lying (Kojima and Pathak 2009), cutoffs as prices (Azevedo and Leshno 2016); open questions |
| | Recap, problems, and the road ahead | The answer; twelve lines; problems; reading; Condorcet's paradox, and Part 18 |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's matching module (`explainer.economics.agora.matching`),
with the Island's Part 17 truths in `explainer.economics.island`, or from the Data Room or a transcribed table; the
narration states the cached numbers.

- **Matching.** Deferred acceptance (either side asking, one-to-one or many-to-one) with a round-by-round log; the
  Boston rule; blocking pairs; every stable matching of the board by enumeration of its 24 pairings; the outcome of
  every list the viewer could submit under each rule; top trading cycles; the best set of cycles and chains in the
  kidney pool by exhaustive search.
- **Mechanisms.** Clarke's pivot rule; the gains from trade under three rules in closed form, checked by 200,000
  simulated pairs; the assignment game's efficient pairing and core by linear programming.
- **Evaluation.** A district with one oversubscribed school, sibling priority and always-takers: OLS, IV without type
  controls and IV with them, over 200 lotteries (seeds 2018-2217).
- **Data.** The marriage rate; the transcribed history, clearinghouse table and estimates.

## Problems and solutions

**1.** *The Boston rule: with the four children's lists and the lottery, show that you get the net loft by telling the
truth and the kiln by listing it first; find the blocking pair.*

*Solution.* Truthfully, round one has you and Ana at the boatyard (Ana wins the lottery), Dara at the kiln and Bo at
the loft, all admitted for good. In round two the kiln is full; in round three the loft has a place, so you get the
loft. Listing the kiln first, round one has you and Dara at the kiln, and your lottery number beats Dara's: you get the
kiln, and Dara, rejected at the full boatyard, ends at the loft. In the truthful outcome you prefer the kiln to the
loft and have a better lottery number than Dara, who holds it: (you, kiln) is a blocking pair.

**2.** *Deferred acceptance: run the apprentices' board with workshops asking, and check that every workshop prefers
the result to the apprentices' version.*

*Solution.* Round one: the boatyard and the loft both ask Bo, the grove asks Ana and the kiln asks Chidi. Bo prefers
the boatyard to the loft, so the loft is turned away; the others are held. Round two: the loft asks Dara, its second
choice, who holds it. The result is Bo at the boatyard, Ana at the grove, Chidi at the kiln and Dara at the loft. Each
workshop now has its first choice except the loft, which has its second; with apprentices asking, the boatyard had its
second (Dara), the grove its fourth (Bo), the kiln its first (Chidi) and the loft its third (Ana). No workshop is worse
off.

**3.** *Stability: prove that deferred acceptance ends with a stable matching, and that it is the asking side's best.*

*Solution.* Each proposer asks each receiver at most once, so it ends. Suppose a and b block the final matching: a
prefers b to its partner, so a asked b earlier and was rejected, in favour of someone b preferred; a receiver's
holdings only improve, so b ends with someone it prefers to a, a contradiction. For optimality, call a receiver
possible for a proposer if some stable matching pairs them. Suppose, for a first time in the run, b rejects a, a
possible partner, for a' whom b prefers. Since a' has not yet been rejected by any possible partner and is asking b, a' ranks
b above every possible partner it has not yet asked, and so above its partner in the stable matching where a has b.
Then a' and b block that matching, a contradiction. So no proposer is ever rejected by a possible partner, and each ends with its best one.

**4.** *Clarke's rule: for the footbridge, find who is pivotal and the taxes; show Bo cannot gain by reporting 60
instead of 10.*

*Solution.* Net values are 60 - 25 = +35, -15, -15 and +15, summing to +20: build. Without Ana the others sum to
-15, so Ana is pivotal and pays 15; without Bo or Chidi the others sum to +35, without Dara +5, so no one else is
pivotal. If Bo reports 60, the bridge is still built, and Bo is still not pivotal (the others still sum to +35), so Bo
pays only the share, and gains nothing; reporting falsely could only change the outcome when it flips the decision,
and then the tax equals the net loss imposed, which is at least the gain.

**5.** *Myerson and Satterthwaite: with values and costs uniform on $[0, 1]$, compute the gains from trade under full
efficiency, a posted price of $\tfrac12$ and the rule $v \ge c + \tfrac14$.*

*Solution.* Full efficiency: $\int_0^1\int_c^1 (v - c)\,dv\,dc = \int_0^1 \tfrac12(1 - c)^2\,dc = \tfrac16$. Posted price:
trade when $c \le \tfrac12 \le v$, gains $\tfrac14(\tfrac34 - \tfrac14) = \tfrac18$. The double auction:
$\int_0^{3/4}\int_{c + 1/4}^1 (v - c)\,dv\,dc = \int_0^{3/4} \tfrac12\big[(1 - c)^2 - \tfrac1{16}\big]dc = \tfrac{9}{64}$,
which is $\tfrac{27}{32} \approx 84\%$ of $\tfrac16$.

**6.** *Top trading cycles: run it on the four huts, and show that no coalition can do better by trading among
itself.*

*Solution.* In the first round Ana points at Bo's hut, Bo at Ana's, Chidi at Dara's and Dara at Ana's. The only cycle
is Ana and Bo, who swap and leave. In the second round Dara's favourite remaining hut is Chidi's and Chidi's is
Dara's: a second cycle, and they swap. Ana and Bo each get their favourite hut, so no coalition containing them can make
them better off; Chidi and Dara each get their favourite among the huts left, and a coalition without Ana and Bo can
only trade those huts. By induction, no coalition can make all its members better off: the outcome is in the core.

**7.** *The assignment game: find the core of the two boats and two buyers, and the competitive prices at each end.*

*Solution.* The best pairing is Ana with Friday's boat (8) and Bo with Crusoe's (7). Core payoffs $u_A, u_B, w_C, w_F
\ge 0$ satisfy $u_A + w_F = 8$, $u_B + w_C = 7$, $u_A + w_C \ge 5$ and $u_B + w_F \ge 9$. Writing $w_F = f$: $u_A = 8 -
f$, $u_B + w_C = 7$ and $u_B \ge 9 - f$, $w_C \ge f - 3$. The sellers' end maximizes $w_C + w_F$: $f = 8$, $w_C = 6$,
$u_B = 1$, $u_A = 0$; the buyers' end minimizes it: $w_C = 0$, $u_B = 7$, $f = 2$, $u_A = 6$. So Friday's surplus runs
from 2 to 8, and each end corresponds to competitive prices (the sellers' reservation values plus their $w$).

**8.** *$\bigstar$ What a lottery reveals: with offers random within types, show that 2SLS with type controls recovers a
constant effect, and why the comparison that ignores types does not.*

*Solution.* With $y = a + \tau d + e$ and an offer $z$ independent of $a$ within each type $t$, the type-controlled
reduced form and first stage are $E[y \mid z = 1, t] - E[y \mid z = 0, t] = \tau\,(E[d \mid z = 1, t] - E[d \mid z = 0, t])$,
so their ratio is $\tau$ in every type and in any weighted average. Ignoring $t$, the offered group mixes in the type
that is offered more often (siblings, weaker on average), so $E[a \mid z = 1] \ne E[a \mid z = 0]$ and the difference in
$y$ includes that gap in $a$: in Agora, enough to cancel the effect almost entirely.

## Where it comes back

| Idea | Parts |
|---|---|
| Voting and adding up preferences | 18 *Social Choice and Welfare* |
| Matching workers to firms, wages | 24 *Looking for Work*, 39 *The Wage Structure* |
| Schools, lotteries and school effects | 49 *The Economic Approach* |
| Information design and mechanisms | 53 *Information and Persuasion* |
| Platforms and their matching teams | 44 *Dynamics, Platforms and Antitrust*, 61 *Economics at the Platforms* |
| Algorithms and fairness | 64 *Machines that Learn* |

## Sources

- D. Gale and L. S. Shapley, "College Admissions and the Stability of Marriage", *American Mathematical Monthly* 69(1)
  (1962): 9-15; L. S. Shapley and M. Shubik, "The Assignment Game I: The Core", *International Journal of Game Theory*
  1(1) (1971): 111-130; L. Shapley and H. Scarf, "On Cores and Indivisibility", *Journal of Mathematical Economics* 1(1)
  (1974): 23-37.
- W. Vickrey (1961); E. H. Clarke, "Multipart Pricing of Public Goods", *Public Choice* 11 (1971): 17-33; T. Groves,
  "Incentives in Teams", *Econometrica* 41(4) (1973): 617-631; J. Green and J.-J. Laffont, "Characterization of
  Satisfactory Mechanisms for the Revelation of Preferences for Public Goods", *Econometrica* 45(2) (1977): 427-438;
  L. M. Ausubel and P. Milgrom, "The Lovely but Lonely Vickrey Auction", in *Combinatorial Auctions* (2006).
- R. B. Myerson, "Incentive Compatibility and the Bargaining Problem", *Econometrica* 47(1) (1979): 61-73; R. B.
  Myerson and M. A. Satterthwaite, "Efficient Mechanisms for Bilateral Trading", *Journal of Economic Theory* 29(2)
  (1983): 265-281; K. Chatterjee and W. Samuelson, "Bargaining under Incomplete Information", *Operations Research*
  31(5) (1983): 835-851.
- L. E. Dubins and D. A. Freedman, "Machiavelli and the Gale-Shapley Algorithm", *American Mathematical Monthly* 88(7)
  (1981): 485-494; A. E. Roth, "The Economics of Matching: Stability and Incentives", *Mathematics of Operations
  Research* 7(4) (1982): 617-628.
- A. E. Roth, "The Evolution of the Labor Market for Medical Interns and Residents: A Case Study in Game Theory",
  *Journal of Political Economy* 92(6) (1984): 991-1016; "A Natural Experiment in the Organization of Entry-Level Labor
  Markets", *American Economic Review* 81(3) (1991): 415-440; "The Economist as Engineer", *Econometrica* 70(4) (2002):
  1341-1378; "Repugnance as a Constraint on Markets", *Journal of Economic Perspectives* 21(3) (2007): 37-58; "What Have
  We Learned from Market Design?", *Economic Journal* 118(527) (2008): 285-310; "The Theory and Practice of Market
  Design", Nobel lecture (2012); A. E. Roth and E. Peranson, "The Redesign of the Matching Market for American
  Physicians", *American Economic Review* 89(4) (1999): 748-780; J. H. Kagel and A. E. Roth, "The Dynamics of
  Reorganization in Matching Markets", *Quarterly Journal of Economics* 115(1) (2000): 201-235.
- A. Abdulkadiroğlu and T. Sönmez, "School Choice: A Mechanism Design Approach", *American Economic Review* 93(3)
  (2003): 729-747; A. Abdulkadiroğlu, P. A. Pathak and A. E. Roth, "The New York City High School Match", *American
  Economic Review* 95(2) (2005): 364-367; Y. Chen and O. Kesten, "Chinese College Admissions and School Choice Reforms",
  *Journal of Political Economy* 125(1) (2017): 99-139.
- A. E. Roth, T. Sönmez and M. U. Ünver, "Kidney Exchange", *Quarterly Journal of Economics* 119(2) (2004): 457-488;
  M. A. Rees et al., "A Nonsimultaneous, Extended, Altruistic-Donor Chain", *New England Journal of Medicine* 360 (2009):
  1096-1101.
- C. Avery, C. Jolls, R. A. Posner and A. E. Roth, "The Market for Federal Judicial Law Clerks", *University of Chicago
  Law Review* 68 (2001): 793-902; M. Niederle and A. E. Roth, "Unraveling Reduces Mobility in a Labor Market", *Journal of
  Political Economy* 111(6) (2003): 1342-1352.
- G. Demange, D. Gale and M. Sotomayor, "Multi-Item Auctions", *Journal of Political Economy* 94(4) (1986): 863-872;
  A. S. Kelso and V. P. Crawford, "Job Matching, Coalition Formation, and Gross Substitutes", *Econometrica* 50(6)
  (1982): 1483-1504.
- A. Abdulkadiroğlu, J. Angrist and P. Pathak, "The Elite Illusion: Achievement Effects at Boston and New York Exam
  Schools", *Econometrica* 82(1) (2014): 137-196 (NBER Working Paper 17264, 2011); A. Abdulkadiroğlu, J. D. Angrist,
  Y. Narita and P. A. Pathak, "Research Design Meets Market Design: Using Centralized Assignment for Impact Evaluation",
  *Econometrica* 85(5) (2017): 1373-1432 (IZA Discussion Paper 10429).
- F. Kojima and P. A. Pathak, "Incentives and Stability in Large Two-Sided Matching Markets", *American Economic Review*
  99(3) (2009): 608-627; E. M. Azevedo and J. D. Leshno, "A Supply and Demand Framework for Two-Sided Matching Markets",
  *Journal of Political Economy* 124(5) (2016): 1235-1268; K. Bansak et al., "Improving Refugee Integration through
  Data-Driven Algorithmic Assignment", *Science* 359(6373) (2018): 325-329.
- OECD Family Database, US Census Bureau (1949) and CDC (2020), crude marriage rate, via Our World in Data.
- Textbooks: Alvin E. Roth, *Who Gets What and Why* (2015); Alvin E. Roth and Marilda Sotomayor, *Two-Sided
  Matching* (1990); Tilman Börgers, *An Introduction to the Theory of Mechanism Design* (2015); Noam Nisan, Tim
  Roughgarden, Éva Tardos and Vijay Vazirani (eds), *Algorithmic Game Theory* (2007).
