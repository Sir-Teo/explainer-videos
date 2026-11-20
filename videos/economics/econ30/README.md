# Economics, Built: Part 30, Sticky Prices

Part 30 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the sixth of Act VI, *Money and the Cycle*. It asks why money moves the real economy
and what the best a central bank can do is. Its answer: because many prices are set for months at a time, and leaving
a price alone costs the seller little but the economy a lot, a change in money or interest rates moves spending and
output before it moves prices. The best a central bank can do is move its rate with the natural rate, more than one
for one with inflation, and commit to a path people believe; when its rate hits zero, promises are what it has left,
and they are weaker in reality than in the model.

It opens on the price collectors of the Bureau of Labor Statistics, about 100,000 prices a month from about 23,000
businesses, and on Mark Bils and Peter Klenow, who in 2004 counted how often each price changes. From there it covers:

- a game: how long does the median consumer price last? (4.3 months counting sales; 8–11 months without them);
- the evidence: Cecchetti's magazines, Blinder's survey of 200 firms, the records, and the Atlanta Fed's sticky- and
  flexible-price CPIs (standard deviations of 1.1 and 1.6 points over 1985–2019; in 2022 flexible prices rose 19%,
  sticky ones 6.5%);
- menu costs (Mankiw 1985; Akerlof and Yellen 1985) on the Island's ferry: a fare 1% too high costs 0.14% of profit
  and 5.8% of passengers;
- monopolistic competition and the desired markup (20% with an elasticity of 6), and why a firm sells more at a price
  it did not choose;
- Calvo's fairy (1983), the reset price, and the New Keynesian Phillips curve derived; its slope, 0.13 on the Island,
  0.38 if prices last four months and 0.09 if they last ten;
- the dynamic IS curve from the Euler equation, and the three equations together;
- Taylor's rule (1993) against the federal funds rate: fitted over the Greenspan years, 1.34 on inflation and 0.94 on
  the gap; −1.3% in 2009–15, when the funds rate stopped at zero;
- determinacy and the Taylor principle drawn over every rule; responses to monetary, demand and cost-push shocks;
- an intermission without narration: sticky- and flexible-price inflation since 1968, the flexible series as a tune;
- Wicksell's natural rate and the divine coincidence (Blanchard and Galí 2007);
- optimal policy: the welfare loss from price dispersion, discretion against commitment (loss 0.091 against 0.058),
  and the price level that comes back;
- menu costs with idiosyncratic shocks against Calvo, 20,000 firms on the Island: half of a 5% rise in money passed
  into prices after 1 month against 7 (the selection effect; Golosov and Lucas 2007);
- the zero lower bound (a slump of 5.7% with prices falling 7.9% a year), forward guidance (one extra quarter at zero
  nearly cancels it; three make a boom of 16%), and the forward-guidance puzzle;
- medium-scale models: habits, indexation and a smoothed rule move the trough two quarters out;
- the frequency-of-price-changes dial (new), the sticky-prices and hump Facts, *Called it?* on Bernanke's 2002
  promise that deflation would be mild and brief (right), and a frontier chapter on the model after 2021.

## Build it

```bash
python -m videos.economics.econ30.compute              # every number (half a minute), into .cache/econ30/
python tools/qa_scene.py econ30 Solved                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ30 -q l   # the whole part, silent preview
python tools/build.py econ30                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 30                     # the lab
```

The data are in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): from FRED, the federal funds rate, the GDP deflator, real
GDP and the CBO's potential, the core PCE price index, the CPI, and the Atlanta Fed's sticky- and flexible-price CPIs
less food and energy.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Why does money move the real economy? | The price collectors; Bils and Klenow; sticky and flexible inflation since 1968; objectives |
| 1 | Play it: how long does a price last? | A month, four months or a year? 4.3 months (Bils and Klenow); 8–11 without sales (Nakamura and Steinsson) |
| 2 | The evidence on price setting | Cecchetti; Blinder and coauthors (once a year; coordination); the Atlanta Fed's indexes, 1985–2019; the sticky-prices Fact |
| 3 | Why prices stick: menu costs | Bo's fare: profit and passengers against the fare; the table (40, 20, 8 and 4 to 1); Mankiw; Akerlof and Yellen |
| 4 | Monopolistic competition | Demand $y_i = (P_i/P)^{-\varepsilon}Y$; the markup $\varepsilon/(\varepsilon-1) = 1.2$; a stuck price and a shrinking markup |
| 5 | Calvo's fairy | A third reset each quarter; the reset price; the NKPC and its forward solution; $\kappa$ against $\theta$ |
| 6 | The dynamic IS curve | The Euler equation; the natural rate; the three equations and three shocks |
| 7 | A rule for the central bank | Taylor's rule; 1985–2007 (correlation 0.69); the fit; 2009–15 and 2021–22 |
| 8 | Three equations, solved | Determinacy over $(\phi_\pi, \phi_x)$; the Taylor principle; Clarida, Galí and Gertler; three impulse responses |
| — | Intermission | Sticky- and flexible-price inflation since 1968; the story so far |
| 9 | The natural rate and the divine coincidence | Wicksell; strict inflation targeting after a demand shock (gap 0) and a cost-push shock (gap −1.96%) |
| 10 | Optimal policy | Price dispersion and Woodford's loss (weight 0.021); discretion against commitment; the price level |
| 11 | Menu costs and the selection effect | Golosov and Lucas; 20,000 firms: half passed through after 1 month against 7; 5.6 against 42 percent-months of output |
| 12 | The zero lower bound and forward guidance | The trap; promises of 1, 2 and 3 extra quarters; the puzzle (+0.28% at one quarter, +10% at twelve); the repairs |
| 13 | Medium-scale models | The hump; Christiano, Eichenbaum and Evans; Smets and Wouters; what each friction buys |
| 14 | The Dials | The frequency of price changes (settled within a range): 0.21, 0.195, 0.105 and the Island's 0.126 |
| 15 | In practice | The hump Fact; what central bank staff do with the model; *Called it?* on Bernanke (2002) |
| 16 | Frontier | The surge of 2021–23 and what the model had to learn; open questions |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 31, *The Central Bank* |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's sticky prices (`explainer.economics.agora.nk`) with the
Island's Part 30 truths, or from the Data Room; the narration states the cached numbers.

- **The Island's economy.** Galí's (2015, ch. 3) quarterly baseline: $\beta = 0.99$, $\sigma = \varphi = 1$,
  $\alpha = 1/3$, $\varepsilon = 6$, $\theta = 2/3$, so $\kappa = 0.1275$; the rule $\phi_\pi = 1.5$, $\phi_x = 0.125$.
  Shocks are AR(1) with persistence 0.5 and size one point at an annual rate; responses by undetermined coefficients.
- **Determinacy.** Both roots of the two-variable system outside the unit circle, on a grid of rules.
- **Optimal policy.** A cost-push shock; discretion $x = -\varepsilon\pi$; commitment in the timeless form, with the
  price level following $\hat p_t = \delta \hat p_{t-1} + \frac{\delta}{1-\delta\beta\rho}u_t$; losses discounted
  over twelve quarters with weight $\kappa/\varepsilon$ on the gap.
- **Hybrid model.** Habits $h = 0.9$, indexation $\gamma = 0.9$ and smoothing 0.8, solved by the ordered QZ
  decomposition (Klein 2000).
- **The zero bound.** Perfect foresight: the natural rate at −2% (annualized) for six quarters, then normal; the
  policy rate at zero through the shock plus any promised quarters, the economy at steady state after; solved
  backwards. The puzzle: a one-point cut for one quarter, $h$ quarters ahead.
- **Price setters.** 20,000 firms whose best prices drift as random walks (4% a month); Calvo with 10% resetting each
  month against an (S,s) band calibrated so that 10% reset each month; money rises 5% after 120 months.
- **Taylor's rule.** $i = 2 + \pi + 0.5(\pi - 2) + 0.5x$ with four-quarter GDP-deflator inflation and the CBO gap, as
  the data stand today; the federal funds rate as a quarterly average; the fit by least squares over 1987Q3–2005Q4.

## Problems and solutions

**1.** *Calvo: if a price survives each quarter with probability $\theta$, show its mean life is $1/(1-\theta)$
quarters; find $\theta$ for 9 months.*

*Solution.* A price set now lasts exactly $k$ quarters with probability $(1-\theta)\theta^{k-1}$, so its mean life is
$\sum_k k(1-\theta)\theta^{k-1} = 1/(1-\theta)$. Nine months is three quarters, so $1/(1-\theta) = 3$ and
$\theta = 2/3$: a third of prices are reset each quarter, about 13% a month.

**2.** *Bo's fare: with demand $p^{-\varepsilon}$ and cost 1, show a fare $g$ too high costs about
$\varepsilon(\varepsilon-1)g^2/2$ of profit and $\varepsilon g$ of sales.*

*Solution.* Profit is $(p-1)p^{-\varepsilon}$, best at $p^* = \varepsilon/(\varepsilon-1)$. With $p = p^*e^{g}$,
$\Pi/\Pi^* = \frac{p^*e^g - 1}{p^* - 1}\,e^{-\varepsilon g}$. Expanding to second order, the first factor is
$1 + \varepsilon g + \varepsilon g^2/2$ (using $p^*/(p^*-1) = \varepsilon$) and the second
$1 - \varepsilon g + \varepsilon^2 g^2/2$; their product is $1 - \varepsilon(\varepsilon-1)g^2/2$. Sales are
$e^{-\varepsilon g} \approx 1 - \varepsilon g$. With $\varepsilon = 6$ and $g = 1\%$: 0.15% of profit (exactly 0.14%)
and 6% of sales (exactly 5.8%), forty to one.

**3.** *Forward: solve $\pi_t = \beta \mathbb{E}_t \pi_{t+1} + \kappa x_t$ forward; with $x_t$ an AR(1) with persistence
$\rho$, show $\pi_t = \kappa x_t/(1-\beta\rho)$.*

*Solution.* Substitute for $\mathbb{E}_t\pi_{t+1}$ repeatedly, using the law of iterated expectations:
$\pi_t = \kappa\sum_{k=0}^{K}\beta^k\mathbb{E}_t x_{t+k} + \beta^{K+1}\mathbb{E}_t\pi_{t+K+1}$, and the last term
vanishes for a bounded solution. With $\mathbb{E}_t x_{t+k} = \rho^k x_t$ the sum is $\kappa x_t/(1-\beta\rho)$:
inflation reacts more to a gap expected to last.

**4.** *Determinacy: with $\phi_x = 0$, show the three-equation model has a unique bounded solution iff $\phi_\pi > 1$.*

*Solution.* Without shocks, $\mathbb{E}_t z_{t+1} = Mz_t$ for $z = (x, \pi)$ with
$M = \begin{pmatrix} 1 + \kappa/(\sigma\beta) & (\phi_\pi - 1/\beta)/\sigma \\ -\kappa/\beta & 1/\beta \end{pmatrix}$.
Both variables can jump, so uniqueness needs both roots outside the unit circle: $\det M > 1$ and
$|\mathrm{tr}\,M| < 1 + \det M$. Here $\det M = (1 + \kappa\phi_\pi/\sigma)/\beta > 1$, and
$1 + \det M - \mathrm{tr}\,M = \kappa(\phi_\pi - 1)/(\sigma\beta)$, positive exactly when $\phi_\pi > 1$.

**5.** *A monetary shock: with $v_t$ an AR(1), find $x_t$ and $\pi_t$ by undetermined coefficients.*

*Solution.* Guess $x_t = \psi_x v_t$, $\pi_t = \psi_\pi v_t$, so expectations are $\rho$ times today's values. The
Phillips curve gives $\psi_\pi = \kappa\psi_x/(1-\beta\rho)$; the IS curve with the rule gives
$\sigma(1-\rho)\psi_x = -(\phi_\pi\psi_\pi + \phi_x\psi_x + 1 - \rho\psi_\pi)$. Solving,
$\psi_x = -(1-\beta\rho)\Lambda$ and $\psi_\pi = -\kappa\Lambda$ with
$\Lambda = 1/[(1-\beta\rho)(\sigma(1-\rho) + \phi_x) + \kappa(\phi_\pi - \rho)]$. On the Island
($\rho = 0.5$) $\Lambda = 2.26$: a shock of 0.25 a quarter lowers the gap 0.285% and annual inflation 0.29 points.

**6.** *The divine coincidence: with $u_t = 0$, show $i_t = r^n_t + \phi_\pi \pi_t$ with $\phi_\pi > 1$ gives
$\pi_t = x_t = 0$.*

*Solution.* Try $\pi_t = x_t = 0$ for all $t$. The Phillips curve holds, $0 = 0$. The IS curve requires
$i_t = \mathbb{E}_t\pi_{t+1} + r^n_t = r^n_t$, which is what the rule delivers when $\pi_t = 0$. So it is an
equilibrium, and by problem 4 the only bounded one. Stabilizing inflation stabilizes the gap too, as long as nothing
shifts the Phillips curve on its own.

**7.** *Discretion: minimize $\pi_t^2 + \vartheta x_t^2$ subject to $\pi_t = \kappa x_t + v_t$; show
$x_t = -(\kappa/\vartheta)\pi_t$.*

*Solution.* Under discretion the bank takes expectations, folded into $v_t$, as given, and chooses $x_t$.
Substituting the constraint, the derivative is $2\pi_t\kappa + 2\vartheta x_t = 0$, so
$x_t = -(\kappa/\vartheta)\pi_t$: lean against inflation by giving up output in proportion. With
$\vartheta = \kappa/\varepsilon$ this is $x_t = -\varepsilon\pi_t$, the Island's discretionary rule.

**8.** $\bigstar$ *Forward guidance: with $\kappa = 0$, show a one-quarter cut promised $h$ quarters ahead moves $x_0$
by the same for every $h$; why does $\kappa > 0$ make it grow?*

*Solution.* With $\kappa = 0$ inflation is always zero, and the IS curve is $x_t = x_{t+1} - (i_t - r^n_t)/\sigma$.
After the cut nothing happens, so $x_{h+1} = 0$ and $x_h = c/\sigma$ for a cut of $c$; before it, $x_t = x_{t+1}$, so
$x_0 = c/\sigma$ whatever $h$. With $\kappa > 0$, each quarter of higher output before the cut raises inflation, and
expected inflation lowers the real rate in the quarter before, which raises output there, and so on: the further away
the cut, the more quarters there are to compound, and the effect grows with $h$, the forward-guidance puzzle.

## Lab and interactive

- `python -m videos.economics.labs 30`: Mankiw's arithmetic, Calvo's slope, the Taylor rule on FRED's data,
  determinacy, impulse responses, discretion against commitment, the selection effect with simulated firms, the zero
  bound and forward guidance, and the hump with habits and indexation.
- The interactive (course site): run the three equations. The reader sets the response to inflation, how sticky
  prices are, and the shock, and watches output, inflation and the policy rate; a response below one makes the model
  lose its anchor.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[30]`; the frequency of price changes is a
dial (`explainer/economics/dials.py`); Bernanke's 2002 promise is a *Called it?* entry (`explainer/economics/calls.py`).
FRED's series were retrieved on 2026-11-20. The BLS's collection figures are from its *Handbook of Methods*.
Cecchetti's and Blinder's findings are stated qualitatively; Bils and Klenow's and Nakamura and Steinsson's figures are
from their published abstracts and tables. The model results are the Island's, with Galí's textbook calibration; the
Taylor-rule fit uses today's vintage of the data, not what the Federal Reserve saw at the time.
