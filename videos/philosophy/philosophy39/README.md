# Philosophy, Built — Part 39: The Arithmetic of Democracy

Part 39 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)), in Act VII, *Value*: social
choice. Rousseau's general will (1762) and a teaser: one 55-voter election, five standard rules, five winners.
**Condorcet's paradox** (1785) as a cycle; Llull (1299), Cusanus (1433), Borda (1770), Dodgson (1876); **the
probability of no Condorcet winner under impartial culture**, exact for 3 to 31 voters (1/18 at 3) with Guilbaud's
limit (1952, 8.77%), and simulated for 3 to 7 candidates (8.5% to 37%); Riker's claimed cycles, Mackie (2003),
Regenwetter et al. (2006). **Five rules, five winners** (plurality A, runoff B, instant runoff C, Borda D, Condorcet
E), instant runoff round by round, the head-to-head matrix (Copeland, Kemeny, Schulze), agenda control (McKelvey 1976;
Riker 1982), **instant runoff's non-monotonicity found by search** (smallest tie-free case: 21 voters), Young's
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

Every number on screen is computed by the Reasoner's new module `explainer/philosophy/reasoner/vote.py` (with
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

Ties are broken alphabetically throughout (the manipulation counts depend on this). The impartial-culture simulation
uses 20,000 elections of 101 voters for each number of candidates (seeds 1785 + m). The SAT encoding uses strict
social rankings; unrestricted domain is built in. The Hong–Page model is a rebuilt toy, not their exact code: 2,000
points, 1,320 agents of three step sizes from 1 to 12, teams of ten in relay; "smooth" is a 25-point moving average.
The opinion-leader jury model conditions on the leader: voters are independent given the leader's answer. The
Bradley–Terry fit uses the infinite-data comparison probabilities and gradient ascent.

## Problems (solutions in the notes)

1. Show that with an odd number of voters, pairwise majority on two alternatives is never tied.
2. Find a profile of 3 voters on which the Borda winner is not the Condorcet winner.
3. Show that if preferences are single-peaked, the majority relation among 3 options has no cycle.
4. Show that a dictatorship is strategy-proof.
5. With p = 0.6, compute the probability that a majority of 3 independent voters is right.
6. Find quotas where Hamilton's method and Webster's method disagree.
