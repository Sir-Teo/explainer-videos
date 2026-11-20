# Economics, Built: Part 29, The Cycle as Equilibrium

Part 29 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth of Act VI, *Money and the Cycle*. It asks whether booms and slumps could
be an economy's best response to shocks it cannot avoid. Its answer: in a model with one household, no money and no
frictions, yes. The Island's booms and slumps are its best response to luck, and they look a lot like America's. But
the measured shocks were partly not technology, hours and productivity do not move together the way the model says,
and money and housing lead the cycle. The claim failed. The method won: optimizing households and firms, equilibrium,
computation and an honest comparison with the data became the way macroeconomics is done.

It opens on Finn Kydland and Edward Prescott's *Time to Build and Aggregate Fluctuations* (*Econometrica*, November
1982) and on two cycles side by side, America's and a frictionless model's. From there it covers:

- what a cycle is: Burns and Mitchell (1946); the Hodrick–Prescott trend (a cycle with a standard deviation of 1.6% of
  output) against Hamilton's regression filter (3.2%, correlation 0.73); the end-point problem, which flips the sign
  of 2008's third quarter (−1.8% from trend with the data of the time, +1.3% with today's); the table of volatilities
  and comovements;
- a game: six series around the NBER's peaks, 1953–2007; which turns first? Housing investment, about 7 quarters
  ahead (Leamer 2007);
- dynamic programming from a cake: the Bellman equation, the principle of optimality, the rule $c = (1-\beta)w$ by
  guess and verify; value function iteration on 1,001 cake sizes, the contraction (the gap shrinks by exactly 0.9 a
  step; 238 steps to $10^{-10}$), Blackwell's conditions;
- Brock and Mirman's stochastic growth model (save $\alpha\beta = 0.35$ of output); Markov chains for shocks
  (Tauchen's chain is 24% too volatile at $\rho = 0.95$ and never moves at $\rho = 0.995$; Rouwenhorst's is exact);
  the general model on a grid;
- labour: intertemporal substitution and the Frisch elasticity (with $\varphi = 0.5$ hours move 0.24 times as much as
  output, against 0.90 in the data); Rogerson's lotteries and Hansen's indivisible labour (0.76);
- calibration from the Penn World Table and the argument with estimation (Kydland and Prescott against Hansen and
  Heckman, 1996);
- log-linearization, the roots of the Island's system (0.942, 0.950 and 1.073), Blanchard and Kahn's count, the saddle
  path drawn, and Klein's QZ solution;
- an intermission without narration: America's business cycle quarter by quarter since 1947, as a tune;
- impulse responses to a 1% technology shock (output +1.94%, hours +1.47%, investment +6.2%, consumption +0.47%) and
  the scorecard against the data;
- what fails: hours against productivity (correlation 0.76 in the model, −0.07 in the data; Christiano and Eichenbaum
  1992), the change after 1985, the Solow residual's six years of "technical regress" (1982: −1.6%), labour hoarding
  and utilization (Basu, Fernald and Kimball 2006);
- the critics: Summers (1986); Galí's long-run VAR re-estimated (hours −0.28% on impact with hours in growth rates;
  +0.15% in levels, as Christiano, Eichenbaum and Vigfusson found); money (Friedman and Schwartz; Romer and Romer) and
  *Called it?* on Prescott's 75 percent (partly right);
- what survived: DSGE models, business cycle accounting (the labour wedge, correlation −0.63 with output), news and
  uncertainty shocks;
- the Frisch elasticity dial (new), the volatility and hours Facts, the model in central banks, and a frontier
  chapter on many households and global solutions.

## Build it

```bash
python -m videos.economics.econ29.compute              # every number (twenty seconds), into .cache/econ29/
python tools/qa_scene.py econ29 Linear                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ29 -q l   # the whole part, silent preview
python tools/build.py econ29                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 29                     # the lab
```

The data are in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): from FRED, real GDP, consumption and investment (with the
chain-type quantity indexes of residential and nonresidential fixed investment), hours and output per hour in the
nonfarm business sector, and the NBER's recession indicator; and the Penn World Table 11.0 for the United States.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Could booms and slumps be an economy's best response to shocks? | Kydland and Prescott (1982); America's cycle beside the Island's, 200 quarters each; objectives |
| 1 | What a cycle is | Burns and Mitchell; 12 NBER recessions since 1947; the HP trend ($\lambda = 1600$), s.d. 1.6%; Hamilton's filter, s.d. 3.2%, correlation 0.73; the end point; the table of volatilities |
| 2 | Play it: which one turns first? | Six average paths around ten NBER peaks; housing investment peaks about 7 quarters before and is 21% lower a year after; Leamer (2007) |
| 3 | Dynamic programming: the cake | $\max \sum \beta^t \log c_t$; the Bellman equation; the principle of optimality; $c = (1-\beta)w$; the cake over 20 days |
| 4 | Value function iteration | $V_1, V_2, V_5, V_{10}, V_{30}, V_{100}$ on 1,001 sizes against the exact value; the gap falls by 0.900 a step; 238 steps; Blackwell (1965); the grid's policy eats 10.4% |
| 5 | The stochastic growth model | Brock and Mirman: save 0.35; a century on the Island; Tauchen against Rouwenhorst at $\rho = 0.95$ and $0.995$; the grid within 0.44% of the formula; policies with depreciation of 10% |
| 6 | Why work more in a boom? | Lucas and Rapping; the Frisch elasticity; hours' relative volatility 0.14 to 0.59 as $\varphi$ runs from 0.25 to 4; $\varphi \approx 2.1$ for half the data's; Rogerson and Hansen: 0.76 |
| 7 | Calibration | Labour's share 0.62, depreciation 3.6%, 1,884 hours a year; the Island's 0.36, 0.99, 2.5%; the steady state (10.3 quarters of capital, investment 25.6% of output); Kydland and Prescott against Hansen and Heckman |
| 8 | Solving the model: the saddle path | Four conditions; the linear system with its matrices; roots 0.942, 0.950, 1.073; Blanchard and Kahn; five paths from capital 20% low; $\hat c = 0.53\hat k + 0.47\hat z$ |
| — | Intermission | America's cycle since 1947 with the recessions; the story so far |
| 9 | The model beside the data | Impulse responses; why each line looks as it does; the scorecard: output's s.d. 1.79 against 1.58, investment 3.2 against 4.6, hours 0.76 against 0.90, hours with productivity 0.76 against −0.07 |
| 10 | What fits and what does not | The two clouds; 1948–84 against 1985–2019 (productivity's correlation with output 0.64 and −0.10); the Solow residual, correlation 0.80; six negative years; 2009's +0.5%; hoarding and utilization |
| 11 | The critics | Summers (1986); Galí's VAR in two specifications with bootstrap bands; technology's share of output's variance at two years, 9% against 69%; Fernald (2007); money; *Called it?* on Prescott (partly right) |
| 12 | What survived | DSGE; business cycle accounting; the labour wedge (correlation −0.63); news, uncertainty and investment shocks |
| 13 | The Dials | The Frisch elasticity (contested): Chetty, Guren, Manoli and Weber 0.54, 0.28, 0.82 and 2.84; this film 2.14; why micro and macro differ |
| 14 | In practice | The volatility and hours Facts; DSGE models at central banks; Dynare; the modeller's six steps |
| 15 | Frontier | Krusell and Smith (1998); Kaplan, Moll and Violante (2018); global solutions, occasionally binding limits, deep solvers; Parts 51 and 52 |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 30, *Sticky Prices* |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's dynamic programming (`explainer.economics.agora.dp`) and
real business cycle (`explainer.economics.agora.rbc`) with the Island's Part 29 truths, or from the Data Room; the
narration states the cached numbers.

- **Cycles.** Logs of quarterly series, Hodrick–Prescott with $\lambda = 1600$ (annual Penn World Table series:
  $\lambda = 100$); Hamilton's cycle is the residual of $y_{t+8}$ on a constant and $y_t, \dots, y_{t-3}$. Moments use
  1948–2019; hours and output per hour are the nonfarm business sector's, compared with its output (output per hour
  times hours).
- **Play it.** For each NBER peak from 1953 to 2007 (the quarter containing the peak month), log levels from 8
  quarters before to 8 after, relative to the peak quarter, less the series' average quarterly growth over 1950–2019;
  averaged over the ten recessions.
- **The cake.** $\beta = 0.9$, 1,001 sizes from 0.001 to 1, $V_0 = 0$; the smallest cake can only be carried.
- **Growth.** $\alpha = 0.36$, $\beta = 0.96$, TFP with $\rho = 0.9$ and $\sigma = 0.02$ on a five-state Rouwenhorst
  chain; 151 capital points from half to one and a half times the steady state.
- **The Island's RBC.** Quarterly: $\alpha = 0.36$, $\beta = 0.99$, $\delta = 0.025$, $\rho = 0.95$, $\sigma = 0.007$,
  hours of one third; utility $\log c - A n$ (or $- A n^{1+1/\varphi}/(1+1/\varphi)$ for a finite Frisch elasticity).
  The conditions are linearized by central differences and solved by the ordered QZ decomposition; moments are from
  20,000 simulated quarters filtered as the data are.
- **The Solow residual.** Penn World Table: $\Delta\log A = \Delta\log Y - (1-\bar s_L)\Delta\log K - \bar s_L\Delta\log L$
  with $Y$ = real GDP at national prices, $K$ = the capital stock, $L$ = employment times average hours, $\bar s_L$ the
  two-year average labour share.
- **Galí's VAR.** Output per hour's growth and hours (growth, or the log level less a linear trend), four lags, 1948–2019;
  the technology shock is the only one with a long-run effect on productivity (Blanchard–Quah); bands are the 16th and
  84th percentiles of 500 residual-bootstrap replications.
- **The labour wedge.** With $u = \log c - An$, $1 - \tau = A c n/((1-\alpha)y)$; its cycle is minus the HP cycle of
  $\log(c\,n/y)$ from real consumption, the hours index and real GDP.

## Problems and solutions

**1.** *The finite cake: with $T$ days left and $u = \log c$, show $c_t = w_t / (1 + \beta + \dots + \beta^{T-t})$; let
$T \to \infty$.*

*Solution.* Giving up a little cake today to eat it tomorrow must not help, so $1/c_t = \beta / c_{t+1}$, that is,
$c_{t+1} = \beta c_t$, and $c_s = \beta^{s-t} c_t$. All the cake is eaten by the last day, so
$\sum_{s=t}^{T} c_s = c_t(1 + \beta + \dots + \beta^{T-t}) = w_t$. As $T \to \infty$ the sum tends to $1/(1-\beta)$
and $c_t = (1-\beta)w_t$: the infinite-horizon rule is the limit of the finite ones, which is what value function
iteration computes, one more day at a time.

**2.** *Guess and verify with $u = c^{1-\sigma}/(1-\sigma)$: show $c = (1 - \beta^{1/\sigma})\, w$.*

*Solution.* Guess that a constant share $s$ is eaten, $c_t = s w_t$, so $w_{t+1} = (1-s) w_t$ and
$c_{t+1}/c_t = 1 - s$. The Euler equation $c_t^{-\sigma} = \beta c_{t+1}^{-\sigma}$ gives
$c_{t+1}/c_t = \beta^{1/\sigma}$, so $s = 1 - \beta^{1/\sigma}$. With $\sigma = 1$ (log utility) this is $1 - \beta$.
A larger $\sigma$, a stronger wish for smooth consumption, makes $\beta^{1/\sigma}$ closer to 1 and the share smaller:
the cake is stretched more evenly.

**3.** *Blackwell: show that the cake's Bellman operator $T$ satisfies $\|TV - TW\| \le \beta \|V - W\|$.*

*Solution.* $T$ is monotone: if $V \le W$ everywhere, then $\log c + \beta V(w-c) \le \log c + \beta W(w-c)$ for every
$c$, so $TV \le TW$. It discounts: $T(V + a) = TV + \beta a$ for any constant $a$. Let $d = \|V - W\|$; then
$V \le W + d$, so $TV \le T(W + d) = TW + \beta d$, and by symmetry $TW \le TV + \beta d$. Hence
$|TV - TW| \le \beta d$ everywhere. By the contraction mapping theorem $T$ has one fixed point, and iterating from any
start converges to it, with the error shrinking by $\beta$ each step.

**4.** *Brock–Mirman: verify $V = a + \frac{\alpha}{1-\alpha\beta}\log k + \frac{1}{(1-\alpha\beta)(1-\beta\rho)}\log z$ and
$k' = \alpha\beta z k^\alpha$.*

*Solution.* Write $V = a + b\log k + d\log z$ with $\log z' = \rho\log z + \varepsilon$. The choice of $k'$ solves
$\max \log(zk^\alpha - k') + \beta b\log k'$, so $1/(zk^\alpha - k') = \beta b/k'$ and $k' = \frac{\beta b}{1+\beta b}
zk^\alpha$. Substituting, the coefficient on $\log k$ is $\alpha(1 + \beta b)$, which must equal $b$, so
$b = \alpha/(1-\alpha\beta)$ and $\beta b/(1+\beta b) = \alpha\beta$. The coefficient on $\log z$ is
$1 + \beta b + \beta\rho d = d$, so $d = (1+\beta b)/(1-\beta\rho) = 1/((1-\alpha\beta)(1-\beta\rho))$.

**5.** *The steady state: with $\alpha = 0.36$, $\beta = 0.99$, $\delta = 0.025$, find $\bar k/\bar y$ and
$\bar\imath/\bar y$.*

*Solution.* The steady-state Euler equation $1 = \beta(\alpha\bar y/\bar k + 1 - \delta)$ gives
$\bar k/\bar y = \alpha/(1/\beta - 1 + \delta) = 0.36/(0.0101 + 0.025) = 10.26$ quarters, about 2.6 years of output.
Investment replaces depreciation, $\bar\imath = \delta\bar k$, so $\bar\imath/\bar y = 0.025 \times 10.26 = 0.256$, and
consumption is the remaining 74.4% of output.

**6.** *Hansen: with $u = \log c - A n$, show the wage is $A c$ and $\hat n = (\hat z + \alpha \hat k - \hat c)/\alpha$.*

*Solution.* The household's conditions are $1/c = \lambda$ for consumption and $A = \lambda w$ for hours, so
$w = A c$. Firms pay the marginal product, $w = (1-\alpha)y/n = (1-\alpha) z k^\alpha n^{-\alpha}$. Setting the two
equal and taking logs, $\log A + \log c = \log(1-\alpha) + \log z + \alpha\log k - \alpha\log n$; in deviations from
the steady state, $\hat c = \hat z + \alpha\hat k - \alpha\hat n$, which rearranges to the result. Hours rise with
technology and capital and fall with consumption: the wealth effect.

**7.** *The saddle: $x_{t+1} = M x_t$ with roots $0.9$ and $1.1$, $k$ predetermined, $c$ free; find the unique stable
path.*

*Solution.* Diagonalize $M = Q\Lambda Q^{-1}$ and let $q_t = Q^{-1}x_t$, so $q_{1,t+1} = 0.9\,q_{1,t}$ and
$q_{2,t+1} = 1.1\,q_{2,t}$. Any $q_2 \ne 0$ explodes, so the path is stable only if $q_{2,t} = 0$, that is, if
$(Q^{-1})_{21}k_t + (Q^{-1})_{22}c_t = 0$: $c_t = -\big((Q^{-1})_{21}/(Q^{-1})_{22}\big)k_t$. This line is the saddle
path, the eigenvector of the stable root; along it $k$ converges at the rate 0.9. One unstable root and one free
variable give exactly one solution (Blanchard and Kahn).

**8.** $\bigstar$ *Rouwenhorst: for two states $\pm\psi$ and $p = (1+\rho)/2$, show the autocorrelation is $\rho$; choose
$\psi$.*

*Solution.* With $P = \begin{pmatrix} p & 1-p \\ 1-p & p \end{pmatrix}$ the stationary distribution is
$(\tfrac12, \tfrac12)$, so the mean is 0 and the variance $\psi^2$. Then $\mathbb{E}[z_t z_{t+1}] = \psi^2\big(p -
(1-p)\big) = \psi^2(2p - 1) = \psi^2\rho$, and the autocorrelation is $\rho$ exactly. To match the variance of
$z' = \rho z + \varepsilon$, choose $\psi = \sigma/\sqrt{1-\rho^2}$. The method builds $n$ states from this two-state
chain recursively, and the first two moments stay exact for any $\rho$, which is why it survives persistence that
breaks Tauchen's grid.

## Lab and interactive

- `python -m videos.economics.labs 29`: measure the American cycle with two filters, solve the cake and watch the
  contraction, compare Tauchen's and Rouwenhorst's chains, check the growth model's grid against Brock and Mirman,
  solve and simulate the Island's RBC beside FRED's data, vary the Frisch elasticity, and re-estimate Galí's VAR in
  both specifications.
- The interactive (course site): eat the cake by iteration. The reader sets patience, the grid and the number of
  iterations, and watches the value function approach the exact answer and the change between iterations shrink by
  a factor of beta.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[29]`; the Frisch elasticity is a dial
(`explainer/economics/dials.py`); Prescott's estimate is a *Called it?* entry (`explainer/economics/calls.py`). FRED's
series were retrieved on 2026-11-20; residential and nonresidential investment are BEA's chain-type quantity indexes,
because FRED's chained-dollar series for them begin only in 2007. The Penn World Table is version 11.0. Galí's,
Christiano, Eichenbaum and Vigfusson's, and Basu, Fernald and Kimball's findings are stated from their papers; the VAR
responses shown are the film's own estimates on the data above, not their published figures. The Island's parameters
are the standard quarterly calibration of the 1980s textbooks.
