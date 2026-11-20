# Economics, Built: Part 28, Inflation and Expectations

Part 28 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth of Act VI, *Money and the Cycle*. It asks whether a country can buy lower
unemployment with higher inflation, and answers: only for a while, and only by surprise. Unemployment falls below its
natural rate only while inflation runs ahead of what people expect, and expectations catch up, so a lasting gain
would take ever faster inflation. Bringing inflation down costs output unless the central bank is believed, which is
why central banks are now independent, with targets, and judged by whether expectations stay anchored.

It opens on Milton Friedman's presidential address to the American Economic Association, on 29 December 1967: there is
always a temporary trade-off between inflation and unemployment, but no permanent one. Within a decade America had
both more inflation and more unemployment than at any time since the war: 3.5% unemployment with 5.4% inflation in
1969, 8.5% with 9.1% in 1975, 7.2% with 13.5% in 1980. From there it covers:

- Phillips's curve (1958), $\dot w + 0.900 = 9.638\,u^{-1.394}$, and Samuelson and Solow's menu (1960), which the
  1960s marched up;
- a game: it is the end of 1972; forecast 1973's inflation (it was 6.3%, and 11.0% in 1974);
- Friedman (1968) and Phelps (1967): the natural rate; on the Island, holding unemployment a point below it raises
  inflation half a point every year;
- the Great Inflation's loops, two oil shocks, controls, and Romer and Romer's account of the ideas behind it;
- adaptive expectations scored against American inflation since 1960 (errors too low through 1980, too high after);
- rational expectations (Muth 1961): what it claims and what it does not;
- Lucas's islands (1972): output's response to money falls from 0.79 when money is calm to 0.10 when it is wild;
  Sargent and Wallace's policy ineffectiveness;
- the Lucas critique (1976) on the Island: a fitted slope of 1.9 predicts output of 107.6 under a 6% rule; it stays
  at 100;
- an intermission without narration: American inflation and unemployment month by month since 1948, inflation as a
  tune;
- time inconsistency (Kydland and Prescott 1977; Barro and Gordon 1983): inflation of 2% for nothing;
- Volcker, 1979–82: the federal funds rate at 19.1%, unemployment at 10.8%, and a sacrifice ratio of about 2;
- the fixes: Rogoff's conservative banker (the best weight on output, 0.31 of society's), independence (Alesina and
  Summers 1993), and inflation targets (New Zealand, 1990);
- the flat Phillips curve: slopes of $-0.65$ (1960–83), $-0.18$ (1984–99), $-0.07$ (2000–19); Hazell, Herreño,
  Nakamura and Steinsson (2022);
- 2021–23: inflation at 9.0%, the anchor that held, openings per unemployed and the bent curve, three accounts, and
  *Called it?* on "team transitory" (wrong);
- two dials (the slope of the Phillips curve and the sacrifice ratio, both new), the persistence Fact and *Called
  it?* on Friedman's forecast (right), and a frontier chapter on how households and firms actually form
  expectations.

## Build it

```bash
python -m videos.economics.econ28.compute              # every number (half a minute), into .cache/econ28/
python tools/qa_scene.py econ28 Islands                # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ28 -q l   # the whole part, silent preview
python tools/build.py econ28                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 28                     # the lab
```

The data are in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): from FRED, the CPI and core CPI, the PCE price index,
the unemployment rate and the CBO's natural rate, real GDP and the CBO's potential, the federal funds rate, job
openings and unemployment, the University of Michigan's expected inflation and the 5-year breakeven rate.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Can a country buy lower unemployment with higher inflation? | Friedman's address, 29 December 1967; America 1960–1982 as a tidy curve and then loops: 1969 (3.5%, 5.4%), 1975 (8.5%, 9.1%), 1980 (7.2%, 13.5%); objectives |
| 1 | Phillips's curve | Britain 1861–1913: wages stable at about 5½% unemployment, 1.8% a year at 2½%; Samuelson and Solow's menu; the 1960s march up it |
| 2 | Play it: forecast inflation | 1960–1972, then 1973: 6.3%, and 1974: 11.0% |
| 3 | The natural rate | $\pi = \pi^e - \beta(u - u^*)$; the Island holds $u$ at 4% against $u^* = 5\%$: 2.5, 3.0, 3.5, ... 9.5% after fifteen years; slower learning, 4.6%; the NAIRU |
| 4 | The Great Inflation | 1966–1983 joined in order; oil in 1973–74 and 1979–80; controls; Romer and Romer |
| 5 | Adaptive expectations | $\lambda = 1$: RMSE 1.75 points; $\lambda = 0.2$: 2.21; errors $+0.8$ a year in 1966–80, $-1.9$ in 1981–86 |
| 6 | Rational expectations | Muth (1961); unpredictable errors; what it claims and does not |
| 7 | Lucas's islands | $\theta = \sigma_z^2/(\sigma_z^2 + \sigma_m^2)$; output's response 0.79 (calm) and 0.10 (wild); Lucas (1973) across countries; Sargent and Wallace (1975) |
| 8 | The Lucas critique | Fitted slope 1.94 under a 2% rule; predicted 107.6 at 6%; actual 100.0 |
| — | Intermission | Inflation and unemployment monthly since 1948; the story so far |
| 9 | Time inconsistency | Barro and Gordon on the Island ($\lambda = 1$, $k = 2$): the rule's loss 2, cheating's 1, discretion's 4 with 2% inflation |
| 10 | Volcker | 6 October 1979; inflation 14.6% (March 1980), the federal funds rate 19.1% (June 1981), unemployment 10.8% (November 1982); 16.4 point-years of output for 8.0 points of core disinflation: a ratio of 2.0; Ball (1994) |
| 11 | The fixes | Rogoff: society's loss 5.0 with its own weight, 4.0 with a pure hawk, 3.47 at $w = 0.31$; Alesina and Summers; New Zealand's target (1990); the Fed's 2% (2012) |
| 12 | The flat curve | Slopes $-0.65$, $-0.18$, $-0.07$; anchored expectations, hidden curves, flatter curves; Hazell, Herreño, Nakamura and Steinsson |
| 13 | 2021–23 | Headline CPI 9.0% (June 2022), core 6.6%, the 5-year breakeven never above 3.4%; openings per unemployed to 2.0; Bernanke and Blanchard, Benigno and Eggertsson; *Called it?*: PCE inflation 5.7% (2021) and 6.1% (2022) against a projected 3.4% and 2.1% |
| 14 | The Dials | The slope of the Phillips curve (contested) and the sacrifice ratio (contested): Ball 1.8, Mankiw 2.8, this film 2.0 |
| 15 | In practice | Persistence: this year's inflation and last year's, correlation 0.73 (0.81 before 1984, 0.52 after); *Called it?* on Friedman (right); the forecaster's toolkit and indexation |
| 16 | Frontier | Michigan's households: 2.9% expected in the 2010s against 1.8% realized; Weber and coauthors; Coibion, Gorodnichenko and Kumar's New Zealand firms; rational inattention; four open questions |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 29, *The Cycle as Equilibrium* |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's expectations (`explainer.economics.agora.expectations`)
with the Island's Part 28 truths, or from the Data Room; the narration states the cached numbers.

- **Inflation.** Annual inflation is the change in the annual average index (CPI, core CPI); monthly charts use the
  change over twelve months; PCE inflation for the *Called it?* card is fourth quarter on fourth quarter, current
  vintage.
- **Acceleration.** $\pi_t = \pi^e_t - 0.5(u_t - 5)$ with $u_t = 4$, $\pi^e$ adaptive with $\lambda = 1$ or 0.3.
- **Lucas's islands.** 200 islands, 60 years, $\sigma_z = 1$, $\sigma_m = 0.5$ or 3; aggregate output on money.
- **The critique.** Output $100 + 2(\pi - \pi^e) + u$, 40 years under each rule, $\pi = \bar\pi + N(0, 1.5^2)$.
- **Barro–Gordon and Rogoff.** $\lambda = 1$, $k = 2$, $b = 1$, supply shocks with $\sigma = 2$; society's loss over
  the banker's weight on a grid of 301 points.
- **Slopes and sacrifice.** Annual changes in core inflation on unemployment less the CBO's natural rate, by period;
  the 1980–85 sacrifice ratio sums quarterly gaps below the CBO's potential (divided by four) over the fall in
  annual core inflation from 1980 to 1985.

## Problems and solutions

**1.** *Phillips: from $\dot w + 0.900 = 9.638\,u^{-1.394}$, find the unemployment rate at which wages are stable, and
the slope there.*

*Solution.* Stable wages need $9.638\,u^{-1.394} = 0.900$, so $u^{-1.394} = 0.0934$ and
$u = e^{\ln(0.0934)/(-1.394)} = e^{1.70} = 5.5\%$. The slope is $d\dot w/du = -1.394 \times 9.638\,u^{-2.394} =
-13.4 \times 5.5^{-2.394} \approx -0.23$: near the natural rate, a point of unemployment moves wage growth by only a
quarter of a point; at 2.5% it moves it by 1.5.

**2.** *Acceleration: with $\pi_t = \pi_{t-1} - \beta(u_t - u^*)$, show that holding $u$ one point below $u^*$ raises
inflation by $\beta$ every year.*

*Solution.* With $\pi^e_t = \pi_{t-1}$, $\pi_t - \pi_{t-1} = -\beta(u_t - u^*) = \beta$ whenever $u_t = u^* - 1$.
Inflation rises by $\beta$ each year, without limit, for as long as unemployment is held there: the Island's
$\beta = 0.5$ takes it from 2% to 9.5% in fifteen years.

**3.** *Adaptive expectations: show that $\pi^e_{t+1} = \lambda \sum_k (1-\lambda)^k \pi_{t-k}$; what is the mean lag?*

*Solution.* Rewrite the rule as $\pi^e_{t+1} = \lambda \pi_t + (1-\lambda)\pi^e_t$ and substitute for $\pi^e_t$
repeatedly: $\pi^e_{t+1} = \lambda\pi_t + \lambda(1-\lambda)\pi_{t-1} + \lambda(1-\lambda)^2\pi_{t-2} + \cdots$. The
weights sum to one. The mean lag is $\sum_k k\lambda(1-\lambda)^k = (1-\lambda)/\lambda$: zero for $\lambda = 1$, four
years for $\lambda = 0.2$, which is why the slow average was always late.

**4.** *Lucas's islands: with $p_i = m + z_i$, derive $\mathbb{E}[z_i \mid p_i] = \theta p_i$ with
$\theta = \sigma_z^2/(\sigma_z^2 + \sigma_m^2)$.*

*Solution.* With $m$ and $z_i$ independent normal with mean zero, $(z_i, p_i)$ is jointly normal, and
$\mathbb{E}[z_i \mid p_i] = \frac{\mathrm{Cov}(z_i, p_i)}{\mathrm{Var}(p_i)}\,p_i = \frac{\sigma_z^2}{\sigma_z^2 +
\sigma_m^2}\,p_i$. A producer supplying $b$ times its expected relative price produces $b\theta p_i$; averaging over
islands, output is $b\theta m$, so the response to money falls as $\sigma_m$ rises: 0.8 at $\sigma_m = 0.5$, 0.1 at 3.

**5.** *The critique: fit $y = a + c\pi$ under a 2% rule; why does it fail at 6%? What is stable?*

*Solution.* Under the old rule $\pi^e = 2$, so $y = y^* + b(\pi - 2) + u$: the fit finds $c \approx b$ and
$a \approx y^* - 2b$. The intercept contains the old rule's expected inflation. Under a 6% rule $\pi^e = 6$, so output
is $y^* + b(\pi - 6)$ and averages $y^*$, not $a + 6c = y^* + 4b$. What is stable is the relation between output and
the *surprise*, $\pi - \pi^e$; the fitted line mixes it with the policy rule.

**6.** *Barro–Gordon: derive discretionary inflation $\lambda b k$, and show society's loss is higher than under the rule
$\pi = 0$.*

*Solution.* Taking $\pi^e$ as given, the bank minimizes $\pi^2/2 + (\lambda/2)(b(\pi - \pi^e) - k)^2$; the first-order
condition is $\pi + \lambda b\,(b(\pi - \pi^e) - k) = 0$. In equilibrium the public is not fooled, $\pi^e = \pi$, so
$\pi = \lambda b k$. Output is at $y^*$ either way, so the loss is $(\lambda b k)^2/2 + \lambda k^2/2$ under
discretion and $\lambda k^2/2$ under the rule: on the Island, 4 against 2.

**7.** *Sacrifice: output is 2%, 4%, 3%, 1% below potential over four years while inflation falls from 9% to 4%; find
the ratio.*

*Solution.* The output lost is $2 + 4 + 3 + 1 = 10$ point-years; inflation fell 5 points; the ratio is $10/5 = 2$,
about America's in 1980–85.

**8.** $\bigstar$ *Rogoff: with supply shocks of variance $\sigma^2$, find the banker's weight $w$ that minimizes
society's loss, and show $0 < w < \lambda$.*

*Solution.* A banker with weight $w$ sets $\pi = wbk - \frac{wb}{1+wb^2}e$, so the output gap is $e/(1+wb^2)$, and
society's expected loss is $L(w) = \tfrac12\big[(wbk)^2 + \big(\tfrac{wb}{d}\big)^2\sigma^2\big] +
\tfrac{\lambda}{2}\big[k^2 + \tfrac{\sigma^2}{d^2}\big]$ with $d = 1 + wb^2$. Differentiating,
$L'(w) = wb^2k^2 + \sigma^2 b^2 (w - \lambda)/d^3$. At $w = \lambda$ the second term vanishes and $L'(\lambda) =
\lambda b^2 k^2 > 0$; at $w = 0$, $L'(0) = -\lambda\sigma^2 b^2 < 0$. So the minimum lies strictly between: a banker
more conservative than society, but not indifferent to output. On the Island ($\lambda = 1$, $k = 2$, $\sigma = 2$) it
is at $w = 0.31$, with a loss of 3.47 against 5.0 and 4.0 at the ends.

## Lab and interactive

- `python -m videos.economics.labs 28`: draw Phillips's curve, accelerate inflation on the Island, score adaptive
  forecasts of American inflation, solve Lucas's islands and the critique, find the inflation bias and Rogoff's best
  banker, and measure the sacrifice ratio and the Phillips curve's slope on FRED's data.
- The interactive (course site): hold unemployment down. The reader runs the central bank, chooses the unemployment
  rate to hold and how fast people learn, and watches inflation and the short-run curves shift.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[28]`; the slope and the sacrifice ratio are
dials (`explainer/economics/dials.py`); Friedman's forecast and the Fed's projection of June 2021 are *Called it?*
entries (`explainer/economics/calls.py`). FRED's series were retrieved on 2026-11-20; the University of Michigan's
survey data are its own, used as a cited extract. Ball's US estimate is as cited by Federal Reserve staff (other
citations give 2.4); Mankiw's is his textbook calculation. Hazell, Herreño, Nakamura and Steinsson's estimates are
described, not quoted; the slopes shown are the film's own regressions on aggregate data.
