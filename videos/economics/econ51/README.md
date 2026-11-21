# Economics, Built: Part 51, Computing Economies

Part 51 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first of Act X, *The Graduate Core*. It asks how an economy that has no formula
is solved, and how you know the answer is right. Its answer: by turning the economy into a fixed point and iterating
towards it, which Blackwell's conditions guarantee will work, or into equations that hold at well-chosen points, or
into a series around the steady state; each is fast when it fits the problem (grids and endogenous grids where there
are kinks, polynomials where the rule is smooth, perturbation near home). And you know the answer is right only by
measuring it: Euler-equation errors, known answers, fixed seeds, and a report with every result.

It opens on Richard Bellman's own account, in his autobiography, of naming dynamic programming at RAND in 1950 to
avoid the word research, which the Secretary of Defense was said to hate: "programming" for planning, "dynamic"
because, he wrote, it cannot be used as an insult, a name "not even a Congressman could object to" (the date has been
questioned, since the Secretary he named took office in 1953). From there it covers:

- the Bellman operator as a contraction: a cobweb on a line, Banach's theorem, the distances between iterates
  shrinking by 0.96 a round on the growth model of Part 29 (333 rounds to a change below a millionth), and
  Blackwell's two conditions checked numerically;
- value against policy iteration: the policy settles at round 74 of 333; Howard's method gets the same policy, at
  every grid point, in 18 rounds, by solving a sparse linear system for each policy's value;
- Play it: which of three grids (30, 100, 1,000 points) reports the steady-state capital to within 1%? Only the
  finest; the coarse grids put it 8.6% and 2.5% too low, with worst Euler errors of about one dollar in 6, 23 and
  245;
- between the grid points: golden-section search on an interpolated value function (Euler errors of 10^-2.1 with
  straight lines on 40 points, 10^-6.1 with a cubic spline, 10^-6.7 with 12 Chebyshev points); Runge's example (an
  error of 1.9 with evenly spaced points, 0.11 with Chebyshev's); where to put the points;
- the endogenous grid method on Part 22's household: no root finding; against value iteration on 800 points it is
  about 85 times as fast and 40 times as accurate;
- projection: Chebyshev collocation, each extra degree about four times more accurate (10^-2.4 at degree 1 to
  10^-8.1 at degree 10), with Galerkin's method agreeing;
- perturbation to second order (g1 = 0.924, a convergence speed of 7.6% a year), its errors away from the steady
  state, and certainty equivalence: the household with income risk consumes 0.22 less at assets of 2 than one with
  the same income for certain, a precautionary gap a first-order perturbation cannot see;
- an intermission film of transistors per microprocessor, 1971-2021 (2,300 to 58 billion, doubling every two
  years), as a line and a tune;
- accuracy: Judd's Euler-equation errors and Den Haan and Marcet's test; eight methods compared on one model, after
  Aruoba, Fernández-Villaverde and Rubio-Ramírez; why a tighter stopping tolerance does not help a grid;
- expectations: Tauchen's five-state chain at persistence 0.99 never moves and overstates the spread by a third;
  Rouwenhorst's is exact; seven Gauss-Hermite nodes beat 100,000 random draws by a factor of hundreds of millions;
- continuous time: a two-income household's HJB equation by Achdou et al.'s implicit upwind scheme, 9 steps on a
  1,000-unknown sparse system (2,996 non-zeros), and the stationary distribution from the same matrix transposed
  (3.6% at the borrowing limit);
- occasionally binding constraints: the household's kink, and the zero bound solved by guess and verify after
  Guerrieri and Iacoviello (the rate at zero for 3 quarters; the output gap -3.4% against -1.7% if the bound is
  ignored);
- the curse of dimensionality: 5^20 grid points against Smolyak's 841, and sparse-grid interpolation in four
  dimensions;
- reproducibility: the report every solution carries, seeds, a known-answer test on Brock and Mirman's economy
  (collocation within 3 parts in 10 million), and what a replication package contains;
- the Dials: the elasticity of intertemporal substitution (contested, 0 to 2) moves consumption by 2-3%, a hundred
  thousand times a good method's error, while a careless grid errs by as much as the whole dispute;
- in practice (model teams, Dynare, structural estimation) and *Called it?* on Gordon Moore's 1965 forecast (right),
  and a frontier of solvers that return derivatives (the implicit function theorem against finite differences, to six
  digits) and neural-network solvers checked by the same Euler errors.

## Build it

```bash
python -m videos.economics.econ51.compute              # every number (about a minute), into .cache/econ51/
python tools/qa_scene.py econ51 Operator               # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ51 -q l   # the whole part, silent preview
python tools/build.py econ51                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 51                     # the lab
```

Times quoted in the film are measured when the cache is built, so they differ from machine to machine; the ratios
between methods are what the film relies on. The only data are Karl Rupp's microprocessor trend data via Our World in
Data, registered in [`SOURCES.md`](../../../explainer/economics/data/SOURCES.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | A name nobody could object to | Bellman at RAND; value iteration settling; the question; objectives |
| 1 | The Bellman operator as a contraction | The operator; a cobweb; distances shrinking by beta; Blackwell's conditions |
| 2 | Value and policy iteration, timed | The policy settles first; Howard's method; why it is Newton's method |
| 3 | Play it: which grid is fine enough? | Three grids; their steady states; Euler errors |
| 4 | Between the grid points | Golden-section search; linear, spline and Chebyshev; Runge; where to put points |
| 5 | The endogenous grid method | The household; Carroll's trick; the rules; the race against value iteration |
| 6 | Projection: the rule as a polynomial | Collocation and Galerkin; the residual; spectral convergence |
| 7 | Perturbation, and when certainty equivalence misleads | g1 and g2; errors away from home; precautionary saving |
| — | Intermission | Transistors per microprocessor, 1971-2021, as a line and a tune; the story so far |
| 8 | Accuracy: Euler-equation errors | The definition; eight methods compared; tolerance against accuracy |
| 9 | Expectations: chains and quadrature | Tauchen and Rouwenhorst; Gauss-Hermite against Monte Carlo |
| 10 | Continuous time | The HJB equation; upwind and implicit; saving and the distribution |
| 11 | Occasionally binding constraints | The household's kink; the zero bound by guess and verify |
| 12 | The curse of dimensionality | Grid sizes; Smolyak's sparse grid; accuracy per point |
| 13 | Reproducibility | The report; seeds; a known answer; the replication package |
| 14 | The Dials: parameters against method error | The EIS dial; parameter uncertainty against method error |
| 15 | In practice: model teams and estimation | Who solves economies; estimation loops; *Called it?* (right) |
| 16 | Frontier: solvers that differentiate | Implicit derivatives; neural-network solvers; open questions |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 52, *Many Agents* |

## What is computed, and from what

Everything plotted is computed by `compute.py` with Agora's solver harness (`explainer.economics.agora.solve`) and the
Island's Part 51 truths; the narration states the cached numbers.

- **The growth model.** u = c^(1-gamma)/(1-gamma) with gamma = 2, output k^0.36, depreciation 8%, beta = 0.96;
  capital grids from half to one and a half times the steady state.
- **Value and policy iteration.** The Bellman operator with next period's capital on the grid (a payoff matrix);
  Howard's evaluation step by a sparse solve of (I - beta P)V = u; Blackwell's conditions on random value functions.
- **Interpolation.** Golden-section search (60 steps) on linear, cubic-spline or Chebyshev interpolants of the value
  function; Runge's function through 11 points.
- **The household.** log income a five-state Rouwenhorst chain (persistence 0.9, innovation s.d. 0.2), normalized to
  mean one; R = 1.03, beta = 0.95, gamma = 2, no borrowing; 200 asset points crowded near the limit; the endogenous
  grid method to a change below 10^-9; value iteration with savings on grids of 100 to 800 points.
- **Projection.** Chebyshev collocation on [0.5, 1.5] times the steady state, degree by degree, each started from the
  degree below, by Powell's hybrid method; Galerkin by Gauss-Chebyshev quadrature with 60 points.
- **Perturbation.** g1 from the quadratic of the once-differentiated Euler equation; g2 from the second derivative
  of the Euler residual along the quadratic policy (a linear equation, solved numerically).
- **Euler errors.** log10 |1 - u'^-1(beta u'(c') R')/c| on 241 points between 0.6 and 1.4 times the steady state.
- **Continuous time.** Incomes 0.1 and 0.2 switching at rate 1.2, r = 0.03, rho = 0.05, borrowing to -0.15, 500 asset
  points; implicit steps of size 1,000 until the change is below 10^-8; the distribution from A' g = 0.
- **The zero bound.** The three-equation model (beta = 0.99, sigma = 1, kappa = 0.1275, Taylor coefficients 1.5 and
  0.5), the natural rate at -2% for four quarters, perfect foresight over 40 quarters, solved as a linear system for
  each guessed set of bound quarters.
- **Sparse grids.** Smolyak's combination technique on nested Clenshaw-Curtis nodes with barycentric polynomial
  interpolation; the test function exp(-|x|^2/2) on [-1, 1]^4 at 300 random points.

## Problems and solutions

**1.** *The contraction: with beta = 0.96 and a first change of 10, how many rounds of value iteration bring the
change below 10^-6? With beta = 0.99?*

*Solution.* The change after n rounds is about 10 x beta^n, so n must exceed log(10^-7)/log(beta). For beta = 0.96
that is 16.12/0.0408 = 395 rounds; for beta = 0.99, 16.12/0.01005 = 1,604 rounds. Patience is expensive for value
iteration, which is why quarterly models use policy iteration or other methods.

**2.** *Blackwell: show that the growth model's Bellman operator satisfies discounting, T(V + a) = TV + beta a, and
monotonicity.*

*Solution.* (T(V + a))(k) = max over k' of u(f(k) - k') + beta (V(k') + a). The constant beta a is the same for every
choice, so it comes out of the max: (TV)(k) + beta a. For monotonicity, if V <= W everywhere then for every choice
u + beta V(k') <= u + beta W(k') <= (TW)(k); taking the max over k' on the left gives (TV)(k) <= (TW)(k). By
Blackwell's theorem, T is then a contraction with modulus beta.

**3.** *Policy evaluation: a policy sends state 1 to state 2 and keeps state 2 where it is; utilities are 1 and 2,
beta = 0.9. Solve V = u + beta P V.*

*Solution.* State 2 stays put: V2 = 2 + 0.9 V2, so V2 = 20. State 1 moves to state 2: V1 = 1 + 0.9 x 20 = 19. One
linear solve gives the value of following the policy forever, which is the evaluation step of Howard's method.

**4.** *The endogenous grid by hand: u = log c, beta R = 1, R = 1.05, y = 1, and tomorrow's rule c(a') = 0.05 a' + 1.
For a' = 2, find today's c and the assets a that choose it.*

*Solution.* The Euler equation 1/c = beta R E[1/c'] = 1/c' gives c = c' = 0.05 x 2 + 1 = 1.1, with no search. The
budget a' = R a + y - c gives a = (c + a' - y)/R = (1.1 + 2 - 1)/1.05 = 2.0. So the household with assets 2 consumes
1.1 and keeps its assets at 2.

**5.** *Collocation: fit c0 + c1 x to e^x at the Chebyshev nodes +-1/sqrt(2). Find the coefficients and the error at
x = 0.*

*Solution.* At x = 0.7071, e^x = 2.0281; at -0.7071, 0.4931. So c1 = (2.0281 - 0.4931)/1.4142 = 1.0854 and c0 =
(2.0281 + 0.4931)/2 = 1.2606. At x = 0 the fit gives 1.2606 against 1: an error of 0.26. More nodes, and a higher
degree, shrink it quickly, as in the film's chapter on projection.

**6.** *Perturbation: for Brock and Mirman's economy, k' = alpha beta k^alpha. Show that g1 = alpha, and find the
speed of convergence for alpha = 0.36.*

*Solution.* The derivative is alpha^2 beta k^(alpha - 1). At the steady state k* = alpha beta k*^alpha, so
alpha beta k*^(alpha - 1) = 1 and g1 = alpha. With alpha = 0.36 the gap to the steady state shrinks to 36% of itself
each year: a speed of convergence of 64% a year, far faster than with partial depreciation (7.6% in the film).

**7.** *Euler errors: a rule's error is 10^-3 for a household that consumes 50,000 a year. What is the mistake in
money, and is it worth a better method?*

*Solution.* About 50 a year. That is small beside the uncertainty about the parameters (the film's dial chapter shows
consumption moving by 2-3%, over 1,000, across the range of the EIS), so for many questions it is good enough; for
welfare comparisons of small policies, whose effects may be a few dollars, it is not, and a method with errors near
10^-6 should be used.

**8.** *Smolyak: show that the level-2 sparse grid in d dimensions has 1 + 4d + 2d(d - 1) points.*

*Solution.* With nested Clenshaw-Curtis nodes, level 1 in a direction adds 1 point, level 2 adds 2 new points and
level 3 adds 2 more. The level-2 grid takes multi-indices whose levels exceed one by at most 2 in total: all at level
1 (one point, the centre); one direction at level 2 (2 new points, d ways: 2d); one direction at level 3 (2 new
points, d ways: 2d); two directions at level 2 (2 x 2 new points, d(d - 1)/2 ways: 2d(d - 1)). The total is
1 + 4d + 2d(d - 1): 13 in two dimensions, 221 in ten, 841 in twenty.

## Lab and interactive

- `python -m videos.economics.labs 51`: value iteration and Howard's method with their rounds; grids and their steady
  states; the endogenous grid method against value iteration; collocation by degree; perturbation; the zero bound by
  guess and verify; Smolyak's counts.
- The interactive (course site): solver. The reader picks a grid size and a method for the growth model and watches
  the policy, the steady state and the Euler errors change.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[51]`; the EIS dial is in
`explainer/economics/dials.py`; Moore's forecast is a *Called it?* entry (`explainer/economics/calls.py`); the
microprocessor data are in the Data Room. Checked on 2026-11-21: Bellman's account of the name (his autobiography,
as excerpted by Dreyfus in Operations Research, 2002; the conflict with Wilson's dates); Moore (1965: 65,000
components by 1975, doubling yearly; 1975: realized, revised to two years); Maliar, Maliar and Winant (JME 2021) and
Azinovic, Gaegauf and Scheidegger (IER 2022). The methods are stated from the papers cited in the chapters (Howard
1960, Blackwell 1965, Tauchen 1986, Judd 1992, Den Haan and Marcet 1994, Rouwenhorst 1995, Krueger and Kubler 2004,
Schmitt-Grohé and Uribe 2004, Carroll 2006, Aruoba et al. 2006, Kopecky and Suen 2010, Guerrieri and Iacoviello 2015,
Achdou et al. 2022) and computed here. Not stated, because not checked: how many times a typical estimation solves its
model; the AEA's exact procedures beyond its data editor's pre-publication checks.
