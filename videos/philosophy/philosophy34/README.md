# Philosophy, Built — Part 34: Games and the Social Contract

Part 34 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)), in Act VII, *Value*: what
happens when choices meet, from Hobbes's state of nature to the design of markets. Hobbes (1651). Nash equilibrium
(1950), defined, found by support enumeration on five games (the prisoner's dilemma, matching pennies, the battle of
the sexes, the stag hunt, chicken), and drawn as best-response correspondences crossing three times (Kakutani 1941);
PPAD-completeness (Daskalakis, Goldberg and Papadimitriou; Chen and Deng 2006). The prisoner's dilemma (Flood and
Dresher 1950; Tucker) and Hobbes's state of nature read as one (Gauthier, Kavka, Hampton); Hardin's commons (1968) as a
Cournot game, where welfare falls to a third of the best with 10 herders and 4% with 100; Ostrom (1990), with a public
goods game in which contributions collapse to 5% without sanctions and hold at 96% with monitored, graduated fines.
Rousseau's stag hunt (1755): basins of 3/4 and 1/4, payoff against risk dominance (Harsanyi and Selten 1988), and
stochastic stability (Kandori, Mailath and Rob 1993): 99% of the time at all-hare. The centipede (Rosenthal 1981):
backward induction takes at once, (3.2, 0.8) when (204.8, 51.2) was on offer; noisy best responses pass early and take
late (McKelvey and Palfrey); the paradox of backward induction (Binmore, Bicchieri, Reny; Aumann 1995; Stalnaker
1998), and **the Wall's thirty-fourth brick**. Correlated equilibrium (Aumann 1974) on chicken: a traffic light gives 5
each, and the best correlated equilibrium, by linear programming, 5.25 against the Nash 4.67; Hart and Mas-Colell
(2000); Hume, Lewis and Gintis on conventions. The shadow of the future: all 32 deterministic memory-one strategies,
played against grim and tit for tat at every discount factor, give the thresholds δ ≥ 1/2 and δ ≥ 2/3, with
alternation the best reply in between; the folk theorem (Friedman 1971; Fudenberg and Maskin 1986), with the least
patience each of 156 cyclic plans needs under grim trigger: mutual cooperation 1/2, taking turns only 1/4, points near
the minmax up to 0.95; and the selection problem. Axelrod's tournaments (1980) rerun with nine strategies: without noise
the nice strategies take the top six places; with 5% noise win-stay lose-shift wins (Nowak and Sigmund 1993); the
ecological tournament as a population river, ending with generous tit for tat 44% and win-stay lose-shift 36%. Press
and Dyson's zero-determinant strategies (2012), derived and checked: the extortioner (11/13, 1/2, 7/26, 0) holds
(s_X − 1)/(s_Y − 1) = 3 against 2000 random opponents and the equalizer fixes the opponent at 2; the extortioner wins
every match and loses the tournament (Stewart and Plotkin 2013; Hilbe et al. 2014). Evolution with rare mutations
(Imhof, Fudenberg and Nowak 2005): 3000 mutation events in a population of 50; generous tit for tat 41.8%, always
defect 30.8%, win-stay lose-shift 21.8%; cooperation 65%; tit for tat as the stepping stone out of defection. Skyrms's
Nash demand game (1996): fair division wins from 1239 of 1711 starting points on the simplex (72%), and from all of
them once encounters are correlated with e = 0.2. Bargaining: Nash's axioms and solution (2/3 against a risk-averse
partner), Kalai–Smorodinsky (0.618), Rubinstein's alternating offers (1/(1 + δ)) and their Nash limit (Binmore,
Rubinstein and Wolinsky 1986). The Shapley value (1953): the axioms, the glove game (2/3, 1/6, 1/6, against the core's
(1, 0, 0)), uniqueness by Harsanyi dividends, and SHAP (Lundberg and Lee 2017) with its limits (Kumar et al. 2020).
Mechanism design: the revelation principle; Vickrey's auction (1961), with truthful bidding optimal; first-price
shading and revenue equivalence; Myerson's optimal reserve (5/12); GSP against VCG (Edelman, Ostrovsky and Schwarz
2007); Gale–Shapley deferred acceptance (1962), run on five students and schools, stable, student-optimal among four
stable matchings, and strategy-proof for students but not schools (Roth 1982); residency, school choice and kidney
exchange. The social contract: a **Price List** for the dilemma (other-regarding preferences; cooperative rationality;
collectively self-defeating rationality), Gauthier (1986), Binmore, Skyrms and Rawls, and four ways out.

The worked model results are computed by the Reasoner's new module `explainer/philosophy/reasoner/games.py` (with `prop`
for the Price List), tested in `tests/philosophy/test_games.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy34.compute       # every computed item (seconds; .cache/philosophy34)
python tools/build.py philosophy34 -q l                # 480p preview
python tools/build.py philosophy34                     # 1080p30 -> renders/philosophy34.mp4
python tools/qa_scene.py philosophy34 ZD               # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Hobbes (1651); four questions; the plan. | — |
| 1 | `Nash` | Nash (1950); Kakutani (1941); PPAD (2006). | support enumeration on five games; best responses crossing |
| 2 | `Commons` | Flood and Dresher (1950); Hobbes; Hardin (1968); Ostrom (1990). | the commons for 1 to 100 herders; a public goods game with sanctions |
| 3 | `StagHunt` | Rousseau (1755); Harsanyi and Selten (1988); Skyrms (2004); Kandori, Mailath and Rob (1993). | basins; stochastic stability |
| 4 | `Centipede` | Rosenthal (1981); McKelvey and Palfrey; Aumann (1995); Stalnaker (1998); **the Wall's thirty-fourth brick**. | backward induction; noisy best responses |
| 5 | `Correlated` | Aumann (1974); Hart and Mas-Colell (2000); Hume (1739); Lewis (1969); Gintis. | the best correlated equilibrium, by linear programming |
| 6 | `Axelrod` | Friedman (1971); Fudenberg and Maskin (1986); Axelrod (1980, 1984); Nowak and Sigmund (1993). | 32 memory-one strategies against grim and tit for tat; the folk theorem's patience map; nine strategies with and without noise; the ecological river |
| 7 | `ZD` | Press and Dyson (2012); Stewart and Plotkin (2013); Hilbe et al. (2014). | extortion and equalizers against 2000 opponents |
| 8 | `Evolution` | Imhof, Fudenberg and Nowak (2005); the Moran process. | fixation probabilities; a sampled history; the stationary distribution |
| 9 | `Skyrms` | Skyrms (1996). | 1711 populations run to their ends; correlated encounters |
| 10 | `Bargaining` | Nash (1950); Kalai and Smorodinsky (1975); Rubinstein (1982); Binmore, Rubinstein and Wolinsky (1986). | the two solutions; alternating offers |
| 11 | `Shapley` | Shapley (1953); Gillies (1959); Harsanyi; Lundberg and Lee (2017); Kumar et al. (2020). | the glove game and its core; SHAP on a tiny model |
| 12 | `Auctions` | Gibbard (1973); Myerson (1979, 1981); Vickrey (1961). | second and first price; revenue equivalence; the optimal reserve |
| 13 | `Markets` | Edelman, Ostrovsky and Schwarz (2007); Gale and Shapley (1962); Roth (1982, 2007). | GSP against VCG; deferred acceptance, its stability and incentives |
| 14 | `Contract` | Sen (1977); Gauthier (1986); Parfit (1984); Binmore; Rawls; **the Price List**. | the dilemma's minimal conflicts |
| 15 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Notes

The folk-theorem plans are cycles of up to seven outcomes, each deviation punished by mutual defection for ever (Nash
reversion); the patience shown for a payoff point is the least over all plans reaching it, on a grid of 0.001. The
centipede's noisy best response is a logit rule on relative gains, in the spirit of McKelvey and Palfrey's quantal
response equilibrium rather than their exact model. The public goods dynamics are imitation with mutation inside
groups of four. The Skyrms basin is computed on an interior grid of the simplex (step 1/60; 1/40 for the correlated
runs).

## Problems (solutions in the notes)

1. Find every Nash equilibrium of rock–paper–scissors, and prove there are no others.
2. In the commons, show that total grazing tends to a − c as n → ∞.
3. For what discount factor does grim trigger sustain cooperation in the repeated dilemma? (δ ≥ 1/2.)
4. Derive the extortionate strategy for χ = 2 with (T, R, P, S) = (5, 3, 1, 0).
5. Show that the Shapley value of a unanimity game on T gives 1/|T| to each member.
6. Prove that no student can gain by misreporting in deferred acceptance with two schools.
