# Economics, Built: Part 56, The Core Exam

Part 56 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the last of Act X, *The Graduate Core*. It asks whether the core can be done with the
book closed. Its answer: yes, for anyone who can do four things without being told how: say who chooses what, given
what; find the condition that pins the answer down (a first-order condition, a Bellman equation, market clearing, a
population moment); solve it with a reason for every step; and check the answer against a special case, its units and
its signs.

The story is the night before the first-year examinations. Twelve questions of the kind every doctoral programme
sets, four each in microeconomics, macroeconomics and econometrics, are solved on screen the way a grader wants to
see them, each after a pause for the viewer, each followed by the mistakes that cost marks. The exam is made up; its
questions are the kind departments set, and every answer is computed twice by Agora's `exam` module, by the formula a
candidate writes and by brute force (a grid, a simulation, an optimizer), and the two are checked against each other.

- Micro: a consumer with a kinked budget (demand 24 on the second segment, at virtual income 120; the income effect
  of the marginal price falls on 4 units, not 24, so dx/dp2 = -8, not -12; a compensating variation of 1.20 against a
  Laspeyres bound of 2.0); an exchange economy with an externality (the equilibrium is the endowment; the Pareto set
  is x_A = 3.57; a Pigouvian tax of 0.5 on A's consumption, returned lump sum, gains 0.37); a first-price auction with
  a reserve of one half (beta(v) = (v^2 + 1/4)/2v; revenue 5/12 against 1/3, with no sale a quarter of the time, and
  0.417 in 400,000 simulated auctions); screening (q_H = 2, q_L = 0.5, a rent of 0.5; with a continuum, q = 2 theta -
  2 and t = theta^2 - 1).
- Macro: the Ramsey model with a 25% tax on the net return to capital, rebated (capital falls from 8.51 to 7.13,
  consumption jumps from 1.616 to 1.690 and ends at 1.568, below where it began, since capital is below the golden
  rule's 17.2); a McCall worker whose benefits expire (the reservation wage falls from 0.809 at the start of a spell
  to 0.740 after exhaustion, so leaving rises from 0.19 to 0.26 a period; Katz and Meyer 1990, Card, Chetty and Weber
  2007); the three-equation model under discretion (an inflation bias of 1.0 point that buys a gap of 0.1, not 0.5;
  inflation 1.83 and the gap -0.73 per unit cost shock; commitment cuts the loss from 4.65 to 3.09); and Aiyagari's
  economy (r = 1.62% below rho = 4.17%, by the supermartingale argument of Chamberlain and Wilson; capital 7.86
  against 5.45 without risk).
- Econometrics: supply and demand on 2,000 simulated days (storms identify demand; least squares gives -0.26, its
  probability limit -0.30; the Wald estimator -0.92, s.e. 0.05, against -1); GMM for the Euler equation (8 moments, 2
  parameters, 6 over-identifying restrictions; beta 0.970 and gamma 3.00, s.e. 0.002 and 0.10; J = 2.77, p = 0.84);
  staggered difference-in-differences with growing effects and no noise (two-way fixed effects 2.00 against an
  average effect of 3.83, with negative weight on the early unit's last four periods, and -0.17, the wrong sign,
  without the never-treated unit; the Goodman-Bacon decomposition; imputation recovers 3.83); and a bivariate VAR
  with Blanchard and Quah's long-run restriction (B recovered exactly in population; in 200 samples of 400 quarters
  the estimates are centred on the truth with standard deviations of a tenth to a fifth of their size).
- How the exam is marked (an illustrative scheme; method marks; two answers to one part, 3 and 12 of 14), what to do
  when stuck, and what a grader looks for.
- Frontier: where each question's idea is still open, from bunching (Saez 2010; Kleven 2016) and multidimensional
  screening (Rochet and Chone 1998) to the zero capital tax revisited (Straub and Werning 2020), the path of
  benefits (Kolsrud, Landais, Nilsson and Spinnewijn 2018), HANK (Kaplan, Moll and Violante 2018), weak instruments
  (Andrews, Stock and Sun 2019), staggered timing (Roth, Sant'Anna, Bilinski and Poe 2023) and hours after technology
  shocks (Gali 1999; Christiano, Eichenbaum and Vigfusson 2004).

The intermission plays the median duration of unemployment in the United States, 1967-2026 (BLS via FRED), with the
NBER's recessions: a line and a tune. There is no *Called it?* and no Dial in this part: an examination has answers,
not estimates.

## Build it

```bash
python -m videos.economics.econ56.compute              # every number (under a minute), into .cache/econ56/
python tools/qa_scene.py econ56 Micro1                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ56 -q l   # the whole part, silent preview
python tools/build.py econ56                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 56                     # the lab
```

The data are FRED's median duration of unemployment and the NBER's recession months (the intermission), registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md); every other number is computed.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The night before | The envelope; where the core came from; how to read a problem; the question; objectives |
| 1 | Micro: a kinked budget | Demand by segments; Slutsky with virtual income; the compensating variation (Play it) |
| 2 | Micro: an externality in an exchange economy | Equilibrium, the Pareto set, Pigou's tax; the box; is and ought |
| 3 | Micro: a first-price auction with a reserve | The bid function and its boundary; revenue by formula and simulation |
| 4 | Micro: screening | Two types; a continuum by virtual types; quality and rents |
| 5 | Macro: the Ramsey model with a tax on capital | The steady state; the phase diagram and the saddle path |
| 6 | Macro: a McCall worker whose benefits expire | Bellman equations by backward induction; the exit rate; the evidence |
| — | Intermission | The median duration of unemployment, 1967-2026, as a line and a tune; the story so far |
| 7 | Macro: the three-equation model under discretion | The inflation bias; a cost shock; commitment |
| 8 | Macro: why r lies below the rate of time preference | The supermartingale argument; Aiyagari's diagram |
| 9 | Econometrics: identifying a demand curve | Order and rank; least squares' bias; the Wald estimator |
| 10 | Econometrics: GMM for an Euler equation | Moments, two steps, the J test; the objective's ridge |
| 11 | Econometrics: staggered difference-in-differences | TWFE against the truth; Goodman-Bacon; weights; imputation |
| 12 | Econometrics: a VAR with a long-run restriction | Counting; C(1)B and Cholesky; precision in samples |
| 13 | How the exam is marked, and what to do when stuck | A mark scheme; two answers; five habits; a grader's eye |
| 14 | Frontier: where each problem is still open | Twelve open questions, one for each problem |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 57, *Reading the Economy in Real Time* |

## What is computed, and from what

Everything plotted is computed by `compute.py` with Agora's `exam` module (`explainer.economics.agora.exam`), which
calls Part 52's Aiyagari economy (`agora.hetero`), Part 54's GMM (`agora.estimate`) and statkit's
difference-in-differences (`explainer.stats.kit.quasi`); the narration states the cached numbers. Each solver asserts
that its formula agrees with a brute-force check:

- **Kinked budget.** Demand by segments against a search over 400,001 points of the kinked budget; the Slutsky total
  against a numerical derivative; the compensating variation by root-finding against its closed form.
- **Externality.** The Pareto condition by root-finding against a numerical maximization of the sum of utilities.
- **Auction.** Revenue by formula against 400,000 simulated first-price and second-price auctions; the bid function
  against a grid of deviations for a bidder with value 0.8.
- **Screening.** The two-type menu against a numerical maximization with the binding constraints substituted; the slack
  constraints checked; the continuum menu checked for incentive compatibility on a grid.
- **Ramsey.** The saddle path by shooting (bisection on c0), Euler steps of 0.02 years.
- **McCall.** Value functions on 501 wage points; the expired state's reservation wage against its closed form.
- **Discretion.** The undetermined coefficients checked in the Phillips curve; commitment solved for its stable root.
- **Aiyagari.** Part 52's economy (beta 0.96, gamma 3, a seven-state Rouwenhorst chain with persistence 0.9 and
  shocks of s.d. 0.2, alpha 0.36, delta 0.08), with its capital supply at twelve interest rates.
- **Supply and demand.** a = 10, b = 1, c = 2, d = 1, e = -2, shocks of s.d. 1, storms on 30% of days; the
  probability limit of least squares in closed form.
- **GMM.** Part 54's `euler_data` (two assets, beta 0.97, gamma 3), 2,000 periods; two-step GMM with sandwich
  standard errors; the second-step objective on a 61 x 61 grid.
- **Staggered timing.** Unit effects 0, 0.5, 1 and a period trend of 0.3; the effect is e + 1 in event time e.
- **Long run.** A = [[0.2, 1/3], [-0.1, 0.8]], B = [[0.8, 0.5], [-0.1, -0.3]], chosen so that demand's long-run
  effect on output's level is zero; 200 samples of 400 quarters, VAR(1) by least squares.

## Exam problems and solutions

**1.** *A consumer has u = 0.4 ln x + 0.6 ln y and income 100; y costs 1; x costs 1 for the first 20 units and 2
beyond. Find demand; decompose the effect of a small rise in the second price; find the compensating variation of a
rise to 2.5.*

*Solution.* On the first segment demand would be 0.4 x 100 = 40 > 20, off the segment. The second segment lies on the
line with price 2 and virtual income 100 + (2 - 1) x 20 = 120, so x = 0.4 x 120 / 2 = 24 > 20, on the segment, with
y = 72 (check: 20 + 8 + 72 = 100). Since virtual income rises by 20 per unit rise in p2, dx/dp2 = dh/dp2 - (x - 20)
dx/dm = -7.2 - 4 x 0.2 = -8, where dh/dp2 = -0.4 x 120/4 + 24 x 0.2 = -7.2; directly, x = 0.4(80/p2 + 20) has slope
-32/p2^2 = -8. At p2 = 2.5, virtual income is 130 and x = 20.8; indirect utility on the segment is ln m' - 0.4 ln p2
+ const, so the compensating variation is 120 x 1.25^0.4 - 130 = 1.20, below the Laspeyres bound (x - 20) x 0.5 = 2.0.

**2.** *u_A = 4 ln x_A + y_A, u_B = 4 ln x_B + y_B - 0.5 x_A; 10 units of x and 20 of y, split equally. Find the
equilibrium, the Pareto set, and a decentralizing tax.*

*Solution.* Each sets 4/x_i = p; with x_A + x_B = 10, x_A = x_B = 5 and p = 0.8: the endowment is the equilibrium. With
quasilinear utility, efficiency maximizes u_A + u_B: 4/x_A - 0.5 = 4/(10 - x_A), so x_A = 3.57, with any feasible split
of y (a vertical line in the box). A tax t = 0.5 on A's consumption with the revenue returned to A gives 4/x_A = p +
0.5 and 4/x_B = p, so p = 0.62 and A pays 1.12; surplus rises by 0.37. Where on the Pareto line to stop is a judgment
about distribution, not a theorem.

**3.** *Two bidders, values uniform on [0, 1], a first-price auction with reserve 0.5. Find the bid function, the
revenue, and why the seller sets the reserve.*

*Solution.* A bidder of value v bidding b wins with probability beta^{-1}(b); the first-order condition at b = beta(v)
is v beta' + beta = v, so v beta(v) = v^2/2 + C, and the boundary beta(r) = r gives C = r^2/2: beta(v) = (v^2 +
0.25)/2v for v >= 0.5, no bid below. Revenue is the expected virtual value 2v - 1 of the winner when the object sells:
2 integral_{0.5}^1 (2v - 1) v dv = 5/12, against 1/3 with no reserve; nothing sells with probability 1/4. Selling to a
type whose virtual value is negative lowers revenue, so the best reserve sets 2v - 1 = 0 (Myerson 1981).

**4.** *Quality q at cost q^2/2; a buyer of type theta gets theta q - t. Two types, 1 (probability 2/3) and 2; then
theta uniform on [1, 2]. Find the menus.*

*Solution.* The low type's participation and the high type's incentive constraint bind: t_L = q_L, t_H = 2 q_H - q_L.
Profit (2/3)(q_L - q_L^2/2) + (1/3)(2 q_H - q_L - q_H^2/2) gives q_H = 2 and (2/3)(1 - q_L) = 1/3, so q_L = 1/2; t_L =
0.5, t_H = 3.5, a rent of 0.5, profit 0.75 against 1.00. With a continuum, the envelope condition U' = q and U(1) = 0
turn profit into virtual surplus, maximized by q = theta - (2 - theta) = 2 theta - 2, with t = theta q - integral q =
theta^2 - 1; profit 2/3 against 7/6. Quality increases with type, so the menu is incentive compatible.

**5.** *Ramsey with f = k^{1/3}, delta 0.05, rho 0.03, theta 2: a permanent 25% tax on the net return to capital,
rebated. The new steady state, the transition, and consumption.*

*Solution.* The rebate keeps the tax out of the resource constraint; the Euler equation becomes c'/c = ((1 - tau)(f'
- delta) - rho)/theta, so f'(k*) = 0.05 + 0.03/0.75 = 0.09 and k* = (1/3 / 0.09)^{3/2} = 7.13 (from 8.51), c* = 1.568
(from 1.616). Capital cannot jump; consumption jumps up onto the new saddle path, to 1.690, then both fall to the new
steady state, half the fall in capital taking about 13 years. Long-run consumption is lower because both steady states
lie below the golden rule (17.2).

**6.** *Offers uniform on [0, 1], beta 0.95; benefits 0.5 for 8 periods, then 0.1. Bellman equations; the reservation
wage; the exit rate.*

*Solution.* W(w) = w/(1 - beta); after exhaustion U_0 = z + beta E max(W, U_0), stationary, with w*_0 = z + beta/(2(1
- beta))(1 - w*_0)^2 = 0.740; then U_d = b + beta E max(W, U_{d-1}). Since b > z and the operator is monotone, U_d
rises with d, so the reservation wage (1 - beta) U_d falls as benefits run out, from 0.809 to 0.740, and the chance of
accepting rises from 0.19 to 0.26 a period.

**7.** *Loss pi^2 + 0.25(x - 0.5)^2, pi = beta E pi' + 0.1 x + u, beta 0.99, u AR(1) with rho 0.5, discretion.*

*Solution.* The first-order condition is kappa pi + lambda (x - x*) = 0. In a steady state with the Phillips curve,
pi = lambda kappa x* / (lambda(1 - beta) + kappa^2) = 1.0 and x = (1 - beta) pi / kappa = 0.1. With pi = a u, x = b u
and E pi' = rho a u: a = lambda / (kappa^2 + lambda(1 - beta rho)) = 1.83, b = -kappa / (...) = -0.73. Under
commitment pi_t = (lambda/kappa)(x_{t-1} - x_t), x_t = 0.82 x_{t-1} + c u_t: inflation rises less, the gap stays low
longer, and the loss from one shock falls from 4.65 to 3.09.

**8.** *Aiyagari: show r < 1/beta - 1, and compute the equilibrium.*

*Solution.* u'(c_t) >= beta(1 + r) E_t u'(c_{t+1}), with equality off the borrowing limit. If beta(1 + r) >= 1,
marginal utility is a nonnegative supermartingale and converges; with income that keeps moving, that requires assets
to grow without bound (Chamberlain and Wilson 2000), so capital supply is infinite at r = rho while firms' demand is
finite; the curves cross below rho. Computed: r = 1.62% against rho = 4.17%, capital 7.86 against 5.45 at r = rho.

**9.** *Demand q = a - bp + u_d, supply q = c + dp + ew + u_s, w a storm dummy. Identification; least squares; a
consistent estimator.*

*Solution.* Demand excludes w, one instrument for one endogenous regressor (order), and e != 0 (rank): exactly
identified; supply excludes nothing. Least squares converges to -b + sigma_d^2 / ((b + d) Var p) = -0.30 (sample
-0.26). The Wald estimator, (mean q on storm days - on calm days)/(the same for p), is -0.92 (s.e. 0.05); the truth is
-1.

**10.** *Euler equation for two assets; instruments 1, lagged consumption growth and lagged returns. Moments; over-
identifying restrictions; two-step GMM and J.*

*Solution.* E[(beta exp(-gamma dc') R'_j - 1) z] = 0 with z = (1, dc, R_1, R_2): 8 moments, 2 parameters, 6 over-
identifying restrictions. First step with identity weights; second with the inverse of the moments' covariance at the
first-step estimate. Here beta = 0.970 (0.002), gamma = 3.00 (0.10); J = T g' S^{-1} g = 2.77 on 6 degrees of freedom,
p = 0.84.

**11.** *E adopts in period 3, L in period 7, N never; effects 1, 2, 3, ... with exposure; no noise. TWFE; its
decomposition; a correct estimator.*

*Solution.* The average effect on the 12 treated cells is (36 + 10)/12 = 3.83. TWFE gives 2.00: Goodman-Bacon's
comparisons are E vs N, 4.5 (weight 0.25), L vs N, 2.5 (0.375), E vs L before L starts, 2.5 (0.125), and L vs E after
E started, -1.5 (0.25), where E's growing effect is used as a control. Imputing Y(0) from unit and period effects
fitted on untreated cells recovers 3.83.

**12.** *A VAR(1) in output growth and unemployment, two shocks, demand with no long-run effect on output. Count;
identify; compute.*

*Solution.* B has 4 unknowns and Sigma = BB' gives 3 equations. The long-run effect on output's level is the first
row of C(1)B, C(1) = (I - A)^{-1}, and [C(1)B]_{12} = 0. Then C(1) Sigma C(1)' = (C(1)B)(C(1)B)', so C(1)B is its
Cholesky factor, unique up to column signs, and B = C(1)^{-1} chol(C(1) Sigma C(1)'), with signs set so supply raises
output and demand lowers unemployment. In population B = [[0.80, 0.50], [-0.10, -0.30]] exactly; in 200 samples of
400 quarters, b11 averages 0.79 (s.d. 0.08) and b12 0.50 (s.d. 0.10).

## Problems and solutions

**1.** *Question 1 again: for which values of alpha does the consumer buy exactly 20 units?*

*Solution.* The first segment fails when alpha x 100 > 20, that is alpha > 0.2; the second fails when alpha x 120 / 2
< 20, that is alpha < 1/3. For 0.2 <= alpha <= 1/3 the consumer is at the kink; at alpha = 0.3 the marginal rate of
substitution there is (0.3/0.7)(80/20) = 1.71, between the prices.

**2.** *Question 3 with n bidders: show that the best reserve is 1/2 for every n, and find the revenue with and without
it for n = 3.*

*Solution.* Revenue is n integral_r^1 (2v - 1) v^{n-1} dv; its derivative in r is -n(2r - 1) r^{n-1}, zero at r = 1/2
whatever n. For n = 3: 6(1 - 1/16)/4 - (1 - 1/8) = 0.531 with the reserve, against (n - 1)/(n + 1) = 0.5 without.

**3.** *Question 5 again, but the revenue pays for useless government spending instead of a rebate: what changes in the
steady state?*

*Solution.* The Euler equation is unchanged, so k* = 7.13 as before. The resource constraint loses g = tau (f' -
delta) k = 0.25 x 0.04 x 7.13 = 0.071, so c* = 1.568 - 0.071 = 1.497. The saddle path shifts down with it, so the
transition has to be solved again; whether consumption still jumps up on impact depends on the numbers.

**4.** *Question 9: suppose storms also keep shoppers at home. What does the Wald estimator estimate now?*

*Solution.* If demand is q = a - bp + delta w + u_d, then the storm moves price by (delta - e)/(b + d) and quantity by
-b times that plus delta, so the Wald ratio is -b + delta (b + d)/(delta - e): biased unless delta = 0. The exclusion
restriction has to be argued from what storms do, not assumed.

**5.** *Question 11 without unit N: compute the two-way fixed-effects coefficient, and explain its sign.*

*Solution.* Only two comparisons remain: E against L before L starts (2.5, weight 1/3) and L against E after E started
(-1.5, weight 2/3), so the coefficient is (2.5 - 3)/3 = -0.17, the wrong sign for a policy that helps every adopter.
The forbidden comparison gets two thirds of the weight, and E's growing effect is subtracted.

**6.** *Question 8: what happens to r\* as the variance of income shocks goes to zero? Why?*

*Solution.* r* rises toward rho and capital falls toward its level at r = rho. The gap is the price of the
precautionary motive: with less risk, households need less buffer stock, supply shifts left, and with no risk the
household's Euler equation holds with beta(1 + r) = 1 in a steady state. Aiyagari's own table shows the gap shrinking
as the variance falls.

## Lab and interactive

- `python -m videos.economics.labs 56`: all twelve questions, each solved by its formula and checked by brute force,
  printed as a marked answer sheet.
- The interactive (course site): the exam. The reader picks one of the twelve questions, reveals the hints one step at
  a time, enters an answer, and sees it marked against the computed solution.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[56]`; the intermission's FRED series is
in the Data Room. The models are stated from the textbooks and papers cited in the chapters (Slutsky 1915, Ramsey
1928, Pigou 1920, Coase 1960, Vickrey 1961, Cass 1965 and Koopmans 1965, McCall 1970, Kydland and Prescott 1977,
Burtless and Hausman 1978, Mussa and Rosen 1978, Shavell and Weiss 1979, Myerson 1981, Riley and Samuelson 1981,
Hansen 1982, Hansen and Singleton 1982, Barro and Gordon 1983, Maskin and Riley 1984, Chamley 1986, Blanchard and Quah
1989, Katz and Meyer 1990, Huggett 1993, Aiyagari 1994, Mas-Colell, Whinston and Green 1995, Faust and Leeper 1997,
Clarida, Gali and Gertler 1999, Chamberlain and Wilson 2000, Hayashi 2000, Ljungqvist and Sargent 2000, Card, Chetty
and Weber 2007, Gali 2008, de Chaisemartin and D'Haultfoeuille 2020, Goodman-Bacon 2021, Callaway and Sant'Anna 2021,
Borusyak, Jaravel and Spiess 2024) and computed here.
