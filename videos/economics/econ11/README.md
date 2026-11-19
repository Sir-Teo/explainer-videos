# Economics, Built: Part 11, Games

Part 11 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third of Act III, *Markets*. It asks what happens when my best choice depends
on yours, and yours on mine, and answers: each predicts the other, and an equilibrium is where those predictions come
true, so that nobody can do better alone. Selfishness can trap everyone, as in the prisoner's dilemma, but a future
worth protecting, the ability to see each other's moves, and forgiveness can sustain cooperation. Real people reason
only a step or two ahead the first time, and learn their way toward equilibrium.

It opens at the RAND Corporation at the start of 1950, where Merrill Flood and Melvin Dresher had two colleagues,
Armen Alchian and John Williams, play a new game a hundred times in a row. Defecting paid more whatever the other
did, so John Nash's new equilibrium said: defect, every time. Both cooperated in 60 rounds and both defected in only
14 (Poundstone's count from Flood's 1952 report), and Nash replied that the experiment "really amounts to having the
players play one large multimove game". That spring Albert Tucker told the game as a story about two prisoners. From
there it covers:

- a game: guess two-thirds of the average (an Island crowd simulated by Agora; Nagel's students in 1995; the
  Financial Times' readers in 1997);
- the strategic form, dominance in the prisoner's dilemma, iterated elimination (Gibbons's example), and the guessing
  game's descent to 0;
- Nash equilibrium: the definition, best responses crossing three times in the battle of the sexes, and existence by
  a fixed point (Nash 1950, 1951; von Neumann 1928);
- coordination, the battle of the sexes, chicken and the stag hunt;
- mixed strategies and the indifference principle, tested on penalty kicks (Chiappori, Levitt and Groseclose 2002;
  Palacios-Huerta 2003) and Wimbledon serves (Walker and Wooders 2001);
- extensive form, backward induction and subgame perfection: an entry game with an empty threat (Selten 1965), and
  how threats are made credible;
- an intermission without narration: the American and Soviet (later Russian) nuclear stockpiles, 1945-2026, with the
  arms-control treaties;
- the centipede (Rosenthal 1981; McKelvey and Palfrey 1992) and the ultimatum game (Güth, Schmittberger and Schwarze
  1982; Henrich et al. 2001);
- repeated games: grim trigger's threshold, the folk theorem's region (Friedman 1971; Fudenberg and Maskin 1986), and
  the finite horizon (Kreps, Milgrom, Roberts and Wilson 1982; Selten and Stoecker 1986);
- Axelrod's tournaments, Agora's rerun and ecology, and what one mistake does to tit for tat (Nowak and Sigmund 1993);
- focal points (Schelling 1960) and correlated equilibrium as a traffic light (Aumann 1974);
- evolution and learning: hawk and dove (Maynard Smith and Price 1973), rock-paper-scissors cycles (Sinervo and Lively
  1996), fictitious play (Brown, Robinson 1951; Shapley 1964);
- levels of thinking: level-k and the cognitive hierarchy (Stahl and Wilson; Nagel; Camerer, Ho and Chong 2004)
  fitted to the guessing game, and *Called it?*: the Nash prediction of 0;
- a Bayesian game: is Ana tough? (Harsanyi 1967-68);
- a new dial (the depth of strategic reasoning) with Keynes's beauty contest; bargaining (Rubinstein 1982), Sweden's
  switch to driving on the right in 1967 and arms control in practice; and a frontier chapter on regret minimization,
  solved poker and Libratus.

## Build it

```bash
python -m videos.economics.econ11.compute              # every number (seconds), into .cache/econ11/
python tools/qa_scene.py econ11 Axelrod                # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ11 -q l   # the whole part, silent preview
python tools/build.py econ11                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 11                     # the lab
```

The data are frozen extracts in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): the Federation of American Scientists' estimates of
nuclear warhead stockpiles by country, 1945-2026, via Our World in Data; and transcribed results from Nagel (1995),
Thaler's Financial Times contest (1997), Flood (1952, via Poundstone), Henrich et al. (2001), Camerer, Ho and Chong
(2004) and Axelrod (1980), in `explainer/economics/data/tables.py` with where they were read and the date they were
checked.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | What happens when my best choice depends on yours, and yours on mine? | Flood and Dresher at RAND, 1950: Alchian and Williams, a hundred rounds; 60 both cooperated, 26 split, 14 both defected; Nash's comment; Tucker's prisoners; games everywhere (oligopoly, bidding, arms races, standards, bargaining, climate); the question; objectives |
| 1 | Play it: guess two-thirds of the average | The rules and a countdown; an Island crowd of 67 from the cognitive hierarchy (average 35.8, target 23.8, winner 24); where your number fell (50, 33, 22, 0); Nagel (1995): 67 students, 20 DM a round, mean 36.73, median 33, target about 24.5; the Financial Times (1997): mean 18.9, winner 13; the equilibrium 0 |
| 2 | Strategic form and dominance: how deep did you think? | The prisoner's dilemma (3, 0, 5, 1): defect dominates, both get 1 instead of 3; Gibbons's game: right, then down, then left eliminated, leaving up, middle; each step one more layer of "I know that you know"; the guessing game's bounds 66.7, 44.4, 29.6, 19.8, ... to 0; Nagel: only 6-10% of first choices three steps or more |
| 3 | Nash equilibrium | The definition and its inequality; best responses and correct beliefs; the battle of the sexes: pure equilibria and the mixed one (Ana 2/3, Bo 1/3, each 2/3); Nash (1950), Kakutani then Brouwer; von Neumann (1928); existence is not prediction |
| 4 | Coordination, the battle of the sexes, chicken and the stag hunt | Four 2x2 games with their pure equilibria framed; several equilibria; the stag hunt's trust; chicken's commitment; conventions as equilibria |
| 5 | Mixed strategies: the penalty kick | Exploitable predictability; the indifference principle; scoring chances 58, 95, 93, 70%: the kicker goes left 38%, the keeper 42%, scoring 79.6% either way; Chiappori, Levitt and Groseclose (2002); Palacios-Huerta (2003), 1,417 kicks; Walker and Wooders (2001); laboratory subjects alternate too much |
| 6 | Extensive form and subgame perfection | Dara's yard against Crusoe's: payoffs (0, 4), (1, 1), (-1, -1); backward induction: Crusoe shares, Dara enters; the strategic form's second equilibrium on an empty threat; Selten (1965); capacity, contracts, reputation (the chain store, 1978) |
| | Intermission: two stockpiles | No narration: American and Soviet/Russian warheads, 1945-2026 (peaks 31,255 in 1967 and 40,159 in 1986), with the Partial Test Ban Treaty, SALT I, the INF Treaty, START I and New START marked; their total as a tune; the story so far |
| 7 | The centipede and the ultimatum game | McKelvey and Palfrey's four-move centipede (0.40/0.10 doubling to 6.40/1.60): take at once in theory; hardly anyone took at the first chance; the ultimatum game: offer almost nothing in theory; Güth et al. (1982); Henrich et al.: mean offers 26-58% in fifteen societies, about 44% in industrial ones |
| 8 | Repeated games and the folk theorem | Grim trigger: cooperate forever $R/(1-\delta)$ against deviate $T + \delta P/(1-\delta)$; threshold $\delta \ge 1/2$; the feasible region, the minmax (1, 1) and the folk theorem's region (Friedman 1971; Fudenberg and Maskin 1986); the finite horizon unravels in theory; Selten and Stoecker (1986); Kreps, Milgrom, Roberts and Wilson (1982) |
| 9 | Axelrod's tournaments | Fourteen programs, 200 rounds; tit for tat (Rapoport) wins, and again among more than sixty; nice, retaliatory, forgiving, clear; tit for two tats would have won; Agora's nine strategies: tit for two tats first, tit for tat fifth, the nice ones on top; the ecology; one mistake in round 5: tit for tat echoes it, win-stay lose-shift repairs it in two rounds; with 5% mistakes win-stay lose-shift wins (Nowak and Sigmund 1993) |
| 10 | Focal points and correlated equilibrium | Schelling (1960): noon at Grand Central, heads, one, half; chicken at a crossing: pure 7 and 2, mixed 4.67 each; a light with (0, 1/4, 1/4, 1/2): obedience is an equilibrium worth 5.25 each (Aumann 1974) |
| 11 | Evolution and learning | Hawk and dove (prize 2, cost 4): the replicator settles at half hawks, an ESS (Maynard Smith and Price 1973); rock-paper-scissors orbits; Sinervo and Lively's lizards (1996); fictitious play on matching pennies (Brown 1951; Robinson 1951; Shapley 1964) |
| 12 | Levels of thinking, fitted | Level 0 at random, level 1 at 33, the cognitive hierarchy with Poisson $\tau$; $\tau = 1.5$ gives a mean of 33.5; fits: Nagel's 36.73 needs $\tau = 1.12$, the FT's 18.9 $\tau = 4.07$; Camerer, Ho and Chong: 1 to 2 across nearly 100 games; *Called it?*: everyone chooses 0, wrong the first time, right as the destination of learning |
| 13 | Games of incomplete information | Bo and Ana's fishing grounds: Ana tough with chance 0.3; Harsanyi's types; the Bayesian Nash equilibrium (tough fights, weak shares, Bo enters); Bo enters while the chance is below 0.5; pointers to Parts 13, 16 and 53 |
| 14 | The Dials: how deeply do people think? | Keynes's beauty contest (1936, ch. 12); the new dial: Camerer, Ho and Chong 1.5 (1-2), Nagel's students 1.12, the FT's readers 4.07: depends on the setting |
| 15 | In practice: bargaining, standards and arms control | Rubinstein (1982): the first proposer's share $1/(1+\delta)$, 52.6% at 0.9; Nash's bargaining solution (1950); Sweden's switch to the right, 3 September 1967; arms races as repeated dilemmas, Schelling and Halperin (1961), "trust, but verify" (1987); the stockpiles' total, 63,476 in 1986 and 8,100 in 2026 |
| 16 | Frontier: learning to play at scale | Regret matching (Hart and Mas-Colell 2000) on rock-paper-scissors: a third each, regret 0.009 a round after 20,000 rounds; heads-up limit hold'em essentially solved by CFR+ (Bowling et al. 2015); Libratus (2017): four professionals, 120,000 hands; Pluribus (2019); open questions: Erev and Roth, Camerer and Ho, algorithms in markets, design |
| | Recap, problems, and the road ahead | The answer; twelve lines; problems; reading; the lysine tapes, and Part 12 |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's games (`explainer.economics.agora.games`), with the
Island's Part 11 truths in `explainer.economics.island`, or from the Data Room or a transcribed table; the narration
states the cached numbers.

- **Strategic form.** Pure equilibria by checking best responses cell by cell; iterated elimination of strictly
  dominated pure strategies, recording the order; every equilibrium of a bimatrix game by support enumeration (the
  indifference equations solved on each pair of supports, then checked); 2x2 mixed equilibria in closed form.
- **The guessing game.** The cognitive hierarchy with Poisson($\tau$) levels truncated at 30, level 0 uniform (mean
  50), level $k$ choosing two-thirds of the normalized mix of lower levels' choices; $\tau$ fitted to a mean by
  Brent's method; the Island crowd: 67 draws of a level from the fitted $\tau$, level 0 uniform on [0, 100], higher
  levels at the model's choice plus normal noise (sd 6), rounded and clipped.
- **Trees.** Backward induction on explicit trees (the entry game; McKelvey and Palfrey's four-move centipede).
- **Repetition.** Grim trigger's threshold in closed form; the feasible set as the convex hull of the four outcomes,
  clipped at the minmax; Axelrod's payoffs (5, 3, 1, 0); a round robin of nine strategies, each pair (and each with
  itself) five times for 200 rounds, with and without 5% of moves flipped; the ecology as the discrete replicator on
  the score matrix; the single-mistake picture by forcing one move in round 5.
- **The rest.** The best correlated equilibrium of chicken by linear programming over the obedience constraints
  (HiGHS); the replicator by Runge-Kutta; fictitious play on matching pennies for 1,500 rounds; regret matching for
  20,000 rounds; Bayesian equilibria by checking every type-contingent plan; Rubinstein's share in closed form; the
  stockpiles from the Data Room, with the treaties' years.

## Problems and solutions

**1.** *The guessing game: with $n \ge 2$ players choosing from $[0, 100]$ and $p < 1$, show that everyone choosing
0 is the only Nash equilibrium.*

*Solution.* Everyone at 0 is an equilibrium: a player who moves to $x > 0$ moves the target to $px/n$, and is
then $x - px/n$ from it while the others are only $px/n$ away, so the deviator loses. Now take any equilibrium. A player who
is not among the winners gets nothing, but can always move exactly onto the target the move creates: choosing $x' =
p(S - x)/(n - p)$, where $S$ is the old sum and $x$ the old number, makes $x'$ equal to $p$ times the new mean, which
wins or ties and gets something. So in an equilibrium everyone is a winner, all equally close to the target $t$, so
every choice is $t - d$ or $t + d$. If $d > 0$, a player at $t + d$ can do the same trick and win alone; so $d = 0$
and everyone chooses the same $x$. If $x > 0$ the target is $px < x$, and a player who moves slightly down is closest
alone and takes the whole prize. Hence $x = 0$.

**2.** *The penalty: for scoring chances $\begin{pmatrix} a & b \\ c & d \end{pmatrix}$ (rows: kick left, right;
columns: dive left, right), find both mixtures by indifference, and check 0.383, 0.417 and 0.796.*

*Solution.* The keeper dives left with probability $q$ that makes the kicker indifferent: $aq + b(1 - q) = cq + d(1 -
q)$, so $q = \frac{d - b}{a - b - c + d}$. The kicker kicks left with probability $p$ that makes the keeper
indifferent: $ap + c(1 - p) = bp + d(1 - p)$, so $p = \frac{d - c}{a - b - c + d}$. With $a, b, c, d = 0.58, 0.95,
0.93, 0.70$: the denominator is $-0.60$, so $q = -0.25/-0.60 = 0.417$ and $p = -0.23/-0.60 = 0.383$, and the scoring
rate is $0.58 \times 0.417 + 0.95 \times 0.583 = 0.796$.

**3.** *The battle of the sexes: find all three equilibria, and show the mixed one gives each player less than
either pure one.*

*Solution.* With payoffs (2, 1) at the regatta, (1, 2) at the market and (0, 0) apart, both pure profiles where they
meet are equilibria. In the mixed one, Bo goes to the regatta with $q$ that makes Ana indifferent: $2q = 1 - q$, $q =
1/3$; Ana with $p$ that makes Bo indifferent: $p = 2(1 - p)$, $p = 2/3$. Ana then expects $2q = 2/3$ and Bo $p =
2/3$, less than the 1 each gets in the pure equilibrium they like less.

**4.** *Entry: find every Nash equilibrium of chapter 6's game in strategic form, and show that only one is subgame
perfect.*

*Solution.* Dara chooses enter or stay out; Crusoe chooses a plan, share or fight if Dara enters. The payoffs are
(enter, share) = (1, 1), (enter, fight) = (-1, -1), and (stay out, either) = (0, 4). (Enter, share) is an
equilibrium: Dara gets 1 > 0, and Crusoe 1 > -1. (Stay out, fight) is too: Dara gets 0 > -1, and Crusoe's plan is
never tested, so he is indifferent. The remaining profiles fail: against share, staying out gives Dara 0 < 1; against
fight, entering gives her -1 < 0. In the subgame after entry, Crusoe's only best move is to share, so only (enter,
share) is subgame perfect.

**5.** *Tit for tat: with Axelrod's payoffs, show that tit for tat against itself is an equilibrium only if $\delta
\ge \tfrac{T-R}{R-S} = \tfrac23$.*

*Solution.* Against tit for tat, a player's future depends only on their last move, so two deviations need checking.
Defecting for ever gives $T + \delta P/(1 - \delta)$ against $R/(1 - \delta)$ for cooperating: it does not pay if
$\delta \ge (T - R)/(T - P) = 1/2$. Alternating defect, cooperate, defect, ... gets $T, S, T, S, \dots$, worth $(T +
\delta S)/(1 - \delta^2)$; this does not pay if $T + \delta S \le R(1 + \delta)$, that is $\delta \ge (T - R)/(R - S)
= 2/3$. Both conditions hold, and so tit for tat is an equilibrium, only for $\delta \ge 2/3$.

**6.** *The traffic light: check that the distribution $(0, \tfrac14, \tfrac14, \tfrac12)$ on (go, go), (go, stop),
(stop, go), (stop, stop) in chicken satisfies every obedience constraint, and gives each driver 5.25.*

*Solution.* With payoffs go/go 0, go/stop 7, stop/go 2, stop/stop 6 to the row driver: told go (probability 1/4), the
other has been told stop, so going gives 7 and stopping 6: obey. Told stop (probability 3/4), the other was told go
with chance $\tfrac{1/4}{3/4} = 1/3$ and stop with chance $2/3$: stopping gives $\tfrac13 \cdot 2 + \tfrac23 \cdot 6 =
14/3$ and going $\tfrac13 \cdot 0 + \tfrac23 \cdot 7 = 14/3$, so obeying is (weakly) best. Each expects $\tfrac14
\cdot 7 + \tfrac14 \cdot 2 + \tfrac12 \cdot 6 = 5.25$.

**7.** *Rubinstein: with patience $\delta$ for both, derive the first proposer's share $\frac{1}{1+\delta}$.*

*Solution.* Look for a stationary equilibrium in which each proposer offers the other just what they would get by
waiting to propose next round, and the offer is accepted. If a proposer keeps $x$, the responder, who would keep $x$
next round, accepts any share of at least $\delta x$ now. So the proposer keeps $x = 1 - \delta x$, giving $x = 1/(1 +
\delta)$. (Rubinstein shows this is the only subgame-perfect equilibrium.) At $\delta = 0.9$, $x = 0.526$.

**8.** ★ *The cognitive hierarchy: find level 2's choice for $\tau = 1.5$, and show that the population's mean falls
as $\tau$ rises.*

*Solution.* With $f_k = e^{-\tau}\tau^k/k!$, level 2 believes the others are level 0 or 1 in proportions $f_0 : f_1 =
1 : \tau$, so it chooses $\tfrac23 \cdot \frac{50 + 1.5 \times 33.3}{2.5} = 26.67$. Level 1 chooses 33.3, and every
level $k \ge 1$ chooses two-thirds of a mixture of lower levels' choices, so the choices fall with $k$ (each is
two-thirds of an average of larger numbers). Raising $\tau$ moves weight from lower levels to higher ones (the
Poisson family is ordered by stochastic dominance), and the choices of the levels themselves fall as more weight on
higher levels enters each level's beliefs; both effects lower the mean. Agora finds 33.5 at $\tau = 1.5$, and the
fits of chapter 12 invert this falling curve.

## Where it comes back

| Idea | Parts |
|---|---|
| Oligopoly, cartels and collusion | 12 *Competition among the Few* |
| Signals, reputation, screening | 13 *Lemons and Signals*, 14 *Incentives* |
| Public goods and climate | 15 *Spillovers*, 48 *Environment and Climate* |
| Auctions and markets by design | 16 *Auctions*, 17 *Markets by Design* |
| Beauty contests and asset prices | 23 *Capital and Asset Prices*, 33 *Crises* |
| Networks and platforms | 44 *Dynamics, Platforms and Antitrust* |
| Fairness, anger and limited thinking | 45 *Behavioural Economics* |
| Information design | 53 *Information and Persuasion* |

## Sources

- M. M. Flood, "Some Experimental Games", RAND RM-789-1 (1952), and *Management Science* 5(1) (1958); W. Poundstone,
  *Prisoner's Dilemma* (1992); the Stanford Encyclopedia of Philosophy, "Prisoner's Dilemma".
- J. von Neumann, "Zur Theorie der Gesellschaftsspiele", *Mathematische Annalen* 100 (1928); J. F. Nash, "Equilibrium
  Points in n-Person Games", *PNAS* 36(1) (1950) 48-49; "Non-Cooperative Games", *Annals of Mathematics* 54(2) (1951);
  "The Bargaining Problem", *Econometrica* 18(2) (1950).
- R. Nagel, "Unraveling in Guessing Games: An Experimental Study", *American Economic Review* 85(5) (1995) 1313-1326;
  R. Thaler's Financial Times contest (1997), as reported in *Chicago Booth Review* (2015).
- R. Gibbons, *A Primer in Game Theory* (1992); M. Osborne, *An Introduction to Game Theory* (2004); M. Osborne and A.
  Rubinstein, *A Course in Game Theory* (1994); D. Fudenberg and J. Tirole, *Game Theory* (1991).
- P.-A. Chiappori, S. Levitt and T. Groseclose, "Testing Mixed-Strategy Equilibria When Players Are Heterogeneous:
  The Case of Penalty Kicks in Soccer", *American Economic Review* 92(4) (2002); I. Palacios-Huerta, "Professionals
  Play Minimax", *Review of Economic Studies* 70(2) (2003); M. Walker and J. Wooders, "Minimax Play at Wimbledon",
  *American Economic Review* 91(5) (2001).
- R. Selten, "Spieltheoretische Behandlung eines Oligopolmodells mit Nachfrageträgheit", *Zeitschrift für die gesamte
  Staatswissenschaft* 121 (1965), and "The Chain Store Paradox", *Theory and Decision* 9 (1978); R. Rosenthal, "Games
  of Perfect Information, Predatory Pricing and the Chain-Store Paradox", *Journal of Economic Theory* 25 (1981); R.
  McKelvey and T. Palfrey, "An Experimental Study of the Centipede Game", *Econometrica* 60(4) (1992).
- W. Güth, R. Schmittberger and B. Schwarze, "An Experimental Analysis of Ultimatum Bargaining", *Journal of Economic
  Behavior and Organization* 3(4) (1982); J. Henrich et al., "In Search of Homo Economicus", *American Economic
  Review* 91(2) (2001).
- J. Friedman, "A Non-cooperative Equilibrium for Supergames", *Review of Economic Studies* 38(1) (1971); D. Fudenberg
  and E. Maskin, "The Folk Theorem in Repeated Games with Discounting or with Incomplete Information", *Econometrica*
  54(3) (1986); D. Kreps, P. Milgrom, J. Roberts and R. Wilson, "Rational Cooperation in the Finitely Repeated
  Prisoners' Dilemma", *Journal of Economic Theory* 27(2) (1982); R. Selten and R. Stoecker, "End Behavior in
  Sequences of Finite Prisoner's Dilemma Supergames", *Journal of Economic Behavior and Organization* 7(1) (1986).
- R. Axelrod, "Effective Choice in the Prisoner's Dilemma" and "More Effective Choice in the Prisoner's Dilemma",
  *Journal of Conflict Resolution* 24 (1980), and *The Evolution of Cooperation* (1984); M. Nowak and K. Sigmund, "A
  Strategy of Win-Stay, Lose-Shift that Outperforms Tit-for-Tat", *Nature* 364 (1993).
- T. Schelling, *The Strategy of Conflict* (1960); T. Schelling and M. Halperin, *Strategy and Arms Control* (1961);
  R. Aumann, "Subjectivity and Correlation in Randomized Strategies", *Journal of Mathematical Economics* 1(1) (1974).
- J. Maynard Smith and G. Price, "The Logic of Animal Conflict", *Nature* 246 (1973); B. Sinervo and C. Lively, "The
  Rock-Paper-Scissors Game and the Evolution of Alternative Male Strategies", *Nature* 380 (1996); G. Brown,
  "Iterative Solution of Games by Fictitious Play" (1951); J. Robinson, "An Iterative Method of Solving a Game",
  *Annals of Mathematics* 54(2) (1951); L. Shapley, "Some Topics in Two-Person Games" (1964).
- D. Stahl and P. Wilson, "Experimental Evidence on Players' Models of Other Players", *Journal of Economic Behavior
  and Organization* 25(3) (1994); C. Camerer, T.-H. Ho and J.-K. Chong, "A Cognitive Hierarchy Model of Games",
  *Quarterly Journal of Economics* 119(3) (2004); C. Camerer, *Behavioral Game Theory* (2003); J. M. Keynes, *The
  General Theory of Employment, Interest and Money* (1936), ch. 12.
- J. Harsanyi, "Games with Incomplete Information Played by 'Bayesian' Players", *Management Science* 14 (1967-68);
  A. Rubinstein, "Perfect Equilibrium in a Bargaining Model", *Econometrica* 50(1) (1982).
- S. Hart and A. Mas-Colell, "A Simple Adaptive Procedure Leading to Correlated Equilibrium", *Econometrica* 68(5)
  (2000); M. Bowling, N. Burch, M. Johanson and O. Tammelin, "Heads-up Limit Hold'em Poker Is Solved", *Science* 347
  (2015); N. Brown and T. Sandholm, "Superhuman AI for Heads-up No-limit Poker: Libratus Beats Top Professionals",
  *Science* 359 (2018), and "Superhuman AI for Multiplayer Poker", *Science* 365 (2019); I. Erev and A. Roth,
  "Predicting How People Play Games", *American Economic Review* 88(4) (1998); C. Camerer and T.-H. Ho,
  "Experience-Weighted Attraction Learning in Normal Form Games", *Econometrica* 67(4) (1999).
- Federation of American Scientists, "Estimated Global Nuclear Warhead Inventories" (2026), via Our World in Data.
