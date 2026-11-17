# Philosophy, Built — Part 39: The Arithmetic of Democracy

Part 39 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)), in Act VII, *Value*: social
choice. Rousseau's general will (1762) and a teaser: one 55-voter election, five standard rules, five winners.
**Condorcet's paradox** (1785) as a cycle; Llull (1299), Cusanus (1433), Borda (1770), Dodgson (1876); **the
probability of no Condorcet winner under impartial culture**, exact for 3 to 31 voters (1/18 at 3) with Guilbaud's
limit (1952, 8.77%), and simulated for 3 to 7 candidates (8.5% to 37%); Riker's claimed cycles, Mackie (2003),
Regenwetter et al. (2006). **Five rules, five winners** (plurality A, runoff B, instant runoff C, Borda D, Condorcet
E), instant runoff round by round, the head-to-head matrix (Copeland, Kemeny, Schulze), agenda control (McKelvey 1976;
Riker 1982), **instant runoff's non-monotonicity found by search** (a 21-voter witness in the restricted search), Young's
consistency (1975), Saari, Young's Kemeny (1988), STV, Droop and list systems. **May's theorem** (1952) by exhaustive
search (59,049 rules, 1 survivor) and its proof; Dasgupta–Maskin (2008). **Arrow's theorem** (1951): the conditions,
**the Borda count breaking IIA** (withdraw C and D and E swap), Geanakoplos's pivotal voter (2005) drawn,
Wilson (1972), Kirman–Sondermann (1972), Sen (1970) — **the Wall's thirty-ninth brick**. **Arrow by SAT** (Tang and
Lin 2009): 108 variables, 992 clauses, unsatisfiable; ORDER, PARETO and IIA have exactly two models, both
dictatorships; all 32 subsets checked; a **Price List** of Arrow's conditions; Nipkow (2009), Geist–Endriss (2011),
Brandt–Geist (2016), verified STV counting (2018). **Gibbard–Satterthwaite** (1973, 1975) and **every profile of 3
voters and 3 candidates searched for manipulations** (plurality 36, Borda 51, IRV 24, Copeland 24, dictator 0,
two-winner majority 0); Bartholdi–Tovey–Trick (1989), Friedgut–Kalai–Nisan (2008), Duverger, Cox, VCG and Gibbard
(1977). **Black's median voter** (1948) checked on all 4,096 single-peaked profiles; Hotelling, Downs, Plott,
NOMINATE, Sen's value restriction, Moulin (1980), List et al. (2013). Range, approval and majority judgment;
**quadratic voting computed** against one person, one vote; participatory budgeting and the method of equal shares;
interpersonal comparisons (d'Aspremont–Gevers 1977). **The Condorcet jury theorem computed** (0.998 at 201 voters with
p = 0.6) and with an opinion leader (stuck near 0.60); Lorenz et al. (2011); prediction markets; epistemic democracy;
**Hong and Page rebuilt** (random team beats the ten best on a rugged landscape in 5 runs out of 5; the advantage
vanishes on a smooth one) and Thompson (2014). **The doctrinal paradox** and **List and Pettit's impossibility by
enumeration** (all four systematic anonymous rules fail); linear and geometric pooling; **the Alabama paradox**
(Hamilton against Webster) and **a Jefferson quota violation found by search**; Balinski–Young (1982);
gerrymandering ensembles. Deliberation (Habermas, Fishkin, Ireland's assembly, Polis), liquid democracy, sortition,
and social choice for AI: **Bradley–Terry fitted to hidden-group comparisons ranks like Borda, not Condorcet**
(Siththaranjan, Laidlaw and Hadfield-Menell 2023), Conitzer et al. (2024), Ge et al. (2024), collective
constitutions (2023), generative social choice and AI mediation (2024).

The worked model results are computed by the Reasoner's new module `explainer/philosophy/reasoner/vote.py` (with
`prop.cdcl` for the SAT proofs), tested in `tests/philosophy/test_vote.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy39.compute       # every computed item (about a minute; .cache/philosophy39)
python tools/build.py philosophy39 -q l                # 480p preview
python tools/build.py philosophy39                     # 1080p30 -> renders/philosophy39.mp4
python tools/qa_scene.py philosophy39 Machine          # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Rousseau (1762); one election, five winners; four questions; the plan. | the 55-voter teaser |
| 1 | `Condorcet` | Condorcet (1785); Llull; Cusanus; Borda; Dodgson; Guilbaud (1952); Riker; Mackie; Regenwetter et al. | the cycle; P(no winner), exact and simulated |
| 2 | `Rules` | plurality, runoff, IRV, Borda, Condorcet, Copeland, Kemeny, Schulze; McKelvey; Riker; Young; Saari; Hare; Droop. | five winners; IRV rounds; pairwise matrix; agendas; IRV non-monotonicity |
| 3 | `May` | May (1952); Dasgupta and Maskin (2008). | 59,049 rules searched |
| 4 | `Arrow` | Arrow (1951); Geanakoplos (2005); Wilson; Kirman–Sondermann; Sen; Riker; G. Mackie; Dryzek; **the Wall's thirty-ninth brick**. | Borda breaks IIA |
| 5 | `Machine` | Tang and Lin (2009); Nipkow; Geist and Endriss; Brandt and Geist; Ghale et al. (2018); **the Price List**. | the SAT encoding, solve, model counts, correction sets |
| 6 | `Strategy` | Gibbard (1973); Satterthwaite (1975); Bartholdi, Tovey, Trick; Conitzer et al.; Friedgut, Kalai, Nisan; Faliszewski–Procaccia; Duverger; Cox; Moulin; Vickrey–Clarke–Groves; Gibbard (1977). | 216 profiles × 6 rules |
| 7 | `Peaks` | Black (1948); Hotelling; Downs; Plott; Poole–Rosenthal; Sen (1966); Moulin; List et al. (2013). | 4,096 single-peaked profiles |
| 8 | `Cardinal` | range; approval (Brams–Fishburn); majority judgment (Balinski–Laraki); Lalley–Weyl; Aziz et al.; Peters–Skowron; d'Aspremont–Gevers. | quadratic voting |
| 9 | `Jury` | Condorcet; Ladha; Dietrich–Spiekermann; Lorenz et al.; Hayek; Wolfers–Zitzewitz; Galton; Estlund; Landemore; Brennan; Hong–Page; Thompson. | jury curves; Hong–Page in ten runs |
| 10 | `Judgment` | Kornhauser–Sager (1986); Pettit; List–Pettit (2002, 2011); McConway; Dietrich–List; Hamilton; Webster; Jefferson; Balinski–Young; Stephanopoulos–McGhee; Duchin. | the doctrinal paradox; four rules fail; Alabama; a quota violation |
| 11 | `Machines` | Habermas (1992); Fishkin; Ireland; Polis; Ford; Kahng et al.; Guerrero; Landemore; Flanigan et al.; Siththaranjan et al.; Conitzer et al.; Ge et al.; Argyle et al.; Fish et al.; Tessler et al. | Bradley–Terry against Borda and Condorcet |
| 12 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Notes

The monotonicity search uses three candidates, odd electorates, distinct totals in every round, and promotes the
winner to the top on one ballot type at a time. Its first witness has 21 voters; the minimum applies to these search restrictions.

Ties are broken alphabetically throughout (the manipulation counts depend on this). The impartial-culture simulation
uses 20,000 elections of 101 voters for each number of candidates (seeds 1785 + m). The SAT encoding uses strict
social rankings; unrestricted domain is built in. The Hong–Page model is a rebuilt toy, not their exact code: 2,000
points, 1,320 agents of three step sizes from 1 to 12, teams of ten in relay; "smooth" is a 25-point moving average.
The opinion-leader jury model conditions on the leader: voters are independent given the leader's answer. The
Bradley–Terry fit uses the infinite-data comparison probabilities and gradient ascent.

## Problems and solutions

1. Show that with an odd number of voters, pairwise majority on two alternatives is never tied.

   *Solution.* With two alternatives and strict preferences, every voter votes for exactly one of them, so the two tallies add to the number of voters, $n$. A tie would mean each tally is $n/2$, which is not a whole number when $n$ is odd. So one alternative always has a strict majority. (Abstention or indifference would bring ties back.)

2. Find a profile of 3 voters on which the Borda winner is not the Condorcet winner.

   *Solution.* With three voters and three alternatives no profile does it, but four alternatives suffice. Voters 1 and 2 rank $a \succ b \succ c \succ d$; voter 3 ranks $b \succ c \succ d \succ a$. Borda scores (3, 2, 1, 0 points): $a$ gets $3 + 3 + 0 = 6$, $b$ gets $2 + 2 + 3 = 7$, $c$ gets 4, $d$ gets 1, so $b$ wins. But $a$ beats every rival by two votes to one, so $a$ is the Condorcet winner. Borda rewards $b$ for voter 3's strong dislike of $a$, which pairwise majority ignores.

3. Show that if preferences are single-peaked, the majority relation among 3 options has no cycle.

   *Solution.* Order the options $a < b < c$ on the line. Single-peakedness rules out ranking the middle option $b$ last, so each voter ranks $abc$, $bac$, $bca$ or $cba$. A cycle $a \succ b \succ c \succ a$ needs a majority with $a$ over $b$ (only $abc$ voters) and a majority with $c$ over $a$ ($bca$ and $cba$ voters); these groups are disjoint, so both cannot be majorities. The reverse cycle $a \succ c \succ b \succ a$ needs majorities with $c$ over $b$ (only $cba$) and with $a$ over $c$ ($abc$ and $bac$), again disjoint. So no cycle: Black's median-voter theorem in miniature.

4. Show that a dictatorship is strategy-proof.

   *Solution.* A dictatorship picks the dictator's reported top choice. Reporting truthfully already gets the dictator her favourite, so no misreport can do better for her. Every other voter's report is ignored, so no one else can change the outcome at all, and in particular cannot improve it by lying. So no one ever gains by misreporting: strategy-proof, which is why the Gibbard–Satterthwaite theorem must exclude dictatorship by assumption.

5. With p = 0.6, compute the probability that a majority of 3 independent voters is right.

   *Solution.* A majority of three is right when at least two are right: $p^3 + 3p^2(1 - p) = 0.216 + 3 \times 0.36 \times 0.4 = 0.216 + 0.432 = 0.648$. The group (64.8%) beats each voter (60%), and by Condorcet's jury theorem the margin grows with the number of independent voters.

6. Find quotas where Hamilton's method and Webster's method disagree.

   *Solution.* The film's states, populations 20, 16 and 7 (43 in all), with 10 seats. Quotas: $10 \times 20/43 = 4.65$, $3.72$ and $1.63$. Hamilton gives the floors 4, 3, 1, then the two remaining seats to the largest remainders, 0.72 and 0.65: $(5, 4, 1)$. Webster's divisor method rounds each population divided by a common divisor to the nearest whole number, with the divisor chosen so the seats add to 10; with divisor 4.5: $4.44 \to 4$, $3.56 \to 4$, $1.56 \to 2$, giving $(4, 4, 2)$. The two methods disagree about whether the smallest state gets one seat or two.

