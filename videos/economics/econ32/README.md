# Economics, Built: Part 32, The Treasury

Part 32 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the eighth of Act VI, *Money and the Cycle*. It asks what a government's budget can
do for the economy, and how much debt is too much. Its answer: a budget can steady an economy, through automatic
stabilizers always, and through deliberate spending or tax cuts whose multipliers are below one in normal times and
larger when the central bank cannot respond. Debt is too much when its interest outruns growth and nobody expects the
surpluses that would pay it; with r below g there is more room than the old rules allowed, but no threshold, and the
room shrinks as rates rise.

It opens on Reinhart and Rogoff's 2010 finding that growth fell to -0.1% a year once public debt
passed 90% of GDP, and on Thomas Herndon, a graduate student who, asked to replicate it for a class, found that a
spreadsheet formula averaged rows 30 to 44 instead of 30 to 49 and left out five countries; with Michael Ash and
Robert Pollin he showed that two other choices mattered more, and the corrected figure was 2.2%.
From there it covers:

- the budget constraint and debt dynamics, with r minus g at the centre, on the Island and in America's record since
  1889 (debt held by the public peaked near 115% of GDP in 1946 and is 97% now);
- a game: the surplus that holds the Island's debt at 100% of GDP (0.98%), and what the
  swing costs with multipliers of 0.5 and 1.5;
- the multiplier in theory: the Keynesian cross, crowding out, Ricardian households, and the New Keynesian model,
  where it is 0.75 under Taylor's rule and 1.13 at the zero
  bound for spending that halves each quarter;
- the multiplier in evidence: Ramey and Zubairy's data since 1889, recomputed here (0.67 after two years
  with military news, 0.41 with Blanchard and Perotti's timing; no larger in slack), and regions with the
  missing intercept (the Island's within-year estimate 1.46 against a national 0.64);
- Romer and Romer's narrative tax changes, and output -2.2% after a tax rise of 1% of GDP;
- automatic stabilizers (the balance worsens 1.2 points per point of unemployment) and the cheques
  of Part 22;
- expansionary austerity and the reply, and the 90% threshold recomputed step by step;
- an intermission without narration: US federal debt to GDP since 1889, as a tune;
- whether debt is a burden (Barro, Diamond, Blanchard), with r below g in 76% of American years
  since 1954;
- tax smoothing through a war (18% less deadweight loss than paying as you go);
- the fiscal theory of the price level and Sargent and Wallace's unpleasant arithmetic;
- sovereign default: Arellano's model solved by value function iteration (defaults at
  2.9% a year, in bad times), Greece in 2012 and Argentina in 2001;
- modern monetary theory, where it agrees with the mainstream and where it does not;
- two dials (new): the spending multiplier and the tax multiplier; *Called it?* on the IMF's 2010 forecasts (wrong:
  slope -1.10); a frontier chapter on interest costs as r rises toward g.

## Build it

```bash
python -m videos.economics.econ32.compute              # every number (about half a minute), into .cache/econ32/
python tools/qa_scene.py econ32 Evidence               # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ32 -q l   # the whole part, silent preview
python tools/build.py econ32                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 32                     # the lab
```

The data are in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): Reinhart and Rogoff's spreadsheet as processed by
Herndon, Ash and Pollin; Ramey and Zubairy's quarterly data since 1889; Ramey's tax data with Romer and Romer's
narrative tax changes; Blanchard and Leigh's forecast-error data; and from FRED the federal deficit, debt and interest
payments, unemployment, Treasury yields, GDP and Greece's and Germany's bond yields.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The missing rows | Reinhart and Rogoff's 90%; Herndon's replication; the question; objectives |
| 1 | The budget constraint and r minus g | The algebra; the Island's three paths; US debt since 1889 |
| 2 | Play it: the minister's budget | The surplus that holds debt steady; what the swing costs |
| 3 | The multiplier in theory | The cross, crowding out, Barro; the New Keynesian multiplier with and without the zero bound |
| 4 | The multiplier in evidence | Four designs; military news and timing since 1889; slack and the zero bound; regions and the missing intercept |
| 5 | Tax changes: the narrative record | Romer and Romer's tax laws; output after a tax increase |
| 6 | Automatic stabilizers | The deficit and unemployment since 1948; the cheques |
| 7 | Austerity, and the 90% threshold recomputed | Alesina and Ardagna and the reply; each correction in turn; the cloud |
| — | Intermission | US federal debt to GDP since 1889, as a tune |
| 8 | Is debt a burden? | Barro, Diamond, Blanchard; r minus g since 1954 |
| 9 | Tax smoothing | Barro's war on the Island; America's wars |
| 10 | Who backs the money? | The fiscal theory; Sargent and Wallace's arithmetic |
| 11 | Sovereign default | Eaton and Gersovitz; Arellano solved and simulated; Greece and Argentina |
| 12 | Modern monetary theory | Its claims; agreements; disagreements |
| 13 | The Dials | The spending and tax multipliers (new) |
| 14 | In practice | Budget offices and debt managers; *Called it?* on the IMF's forecasts |
| 15 | Frontier | Interest costs as r rises toward g; open questions |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 33, *Crises* |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's treasury (`explainer.economics.agora.fiscal`) with the
Island's Part 32 truths, or from the Data Room; the narration states the cached numbers.

- **The 90% recomputation.** Herndon, Ash and Pollin's key columns, 1946-2009, Italy from 1951; the published figure
  as country averages of country-year means with the five countries and the early years left out and New Zealand at
  −7.9; then each correction in turn; finally every country-year counted once.
- **Multipliers.** Ramey and Zubairy's two-step local projections: output and government purchases divided by
  potential output, regressed at each horizon on the shock with four lags of output, purchases and (for news) the
  news; the multiplier is the ratio of cumulative coefficients. States by last quarter's unemployment (6.5% or more)
  or their zero-bound dummy.
- **The New Keynesian multiplier.** Part 30's calibration with spending in the IS curve (sigma_c = 0.8) and in the
  Phillips curve (gamma = 0.5); AR(1) spending; at the zero bound the trap lasts as long as the spending.
- **Taxes.** Local projections of log real GDP on Romer and Romer's exogenous changes (percent of GDP) with four lags
  of the changes and of GDP growth.
- **Default.** Arellano's (2008) calibration: beta 0.953, sigma 2, r 1.7% a quarter, re-entry 0.282, output in
  default min(y, 0.969 E[y]), log output AR(1) with rho 0.945 and s.d. 0.025 on a 21-state Tauchen chain; 200 debt
  points; value function iteration until the values and prices change by less than 10^-7; 20,000 simulated quarters.
- **Called it?** Blanchard and Leigh's baseline: 26 European economies; growth in 2010-11 as reported in fall 2012
  less the spring 2010 forecast, on the change in the structural balance forecast for 2009-11.

## Problems and solutions

**1.** *Debt dynamics: from $B_{t+1} = (1+r)B_t - S_t$ and $Y_{t+1} = (1+g)Y_t$, derive $b_{t+1}$ and the surplus
that holds $b$ steady.*

*Solution.* Dividing by $Y_{t+1}$: $b_{t+1} = \frac{1+r}{1+g} b_t - s_t$ with $s_t = S_t / Y_{t+1}$. Setting
$b_{t+1} = b_t = b$ gives $s = \big(\frac{1+r}{1+g} - 1\big)b = \frac{r-g}{1+g}\,b$: positive when $r > g$,
negative (a deficit is affordable) when $r < g$.

**2.** *The cross with taxes: with consumption $c(1-t)Y$, show the spending multiplier is $1/(1 - c(1-t))$; evaluate
it for $c = 0.8$, $t = 0.25$.*

*Solution.* $Y = c(1-t)Y + I + G$, so $Y = (I + G)/(1 - c(1-t))$ and $dY/dG = 1/(1 - c(1-t))$. With $c = 0.8$ and
$t = 0.25$, $c(1-t) = 0.6$ and the multiplier is $1/0.4 = 2.5$: proportional taxes leak some of each round, which is
one of the automatic stabilizers.

**3.** *Balanced budget: in the simple cross, show that spending paid for by an equal lump-sum tax has a multiplier of
one.*

*Solution.* $Y = c(Y - T) + I + G$. With $dG = dT$: $dY = c\,dY - c\,dG + dG$, so $(1-c)\,dY = (1-c)\,dG$ and
$dY = dG$. The spending adds a full round; the tax subtracts all rounds but the first.

**4.** *The zero bound: in the model of chapter 3 with $i = 0$ and $\gamma = 0$, solve for the multiplier and show it
exceeds one.*

*Solution.* With $y = m g$, $\pi = q g$ and expectations $\rho$ times today's values, the IS curve gives
$(m-1)(1-\rho) = \sigma_c \rho q$ and the Phillips curve $q(1 - \beta\rho) = \kappa m$. Substituting,
$m = \frac{(1-\rho)(1-\beta\rho)}{(1-\rho)(1-\beta\rho) - \sigma_c\kappa\rho}$, which exceeds one whenever
the denominator is positive, the condition for a bounded solution: spending raises expected inflation, which lowers
the real rate when the nominal rate cannot move.

**5.** *The missing intercept: with $y_{rt} = m_L(g_{rt} - \bar g_t) + m_A \bar g_t + u_t + e_{rt}$, show that year
fixed effects estimate $m_L$, not $m_A$.*

*Solution.* Subtracting each year's average across regions removes $m_A \bar g_t + u_t$ and leaves
$y_{rt} - \bar y_t = m_L(g_{rt} - \bar g_t) + (e_{rt} - \bar e_t)$, so least squares on the demeaned data
estimates $m_L$. The national multiplier $m_A$ lives only in the year averages, which the fixed effects absorb.

**6.** *Tax smoothing: minimize $\sum \beta^t \tau_t^2$ subject to $\sum \beta^t \tau_t = \sum \beta^t g_t$; show
the best $\tau_t$ is constant.*

*Solution.* The Lagrangian's first-order condition is $2\beta^t\tau_t = \lambda\beta^t$, so $\tau_t = \lambda/2$
for every $t$; the budget fixes $\tau = \sum\beta^t g_t / \sum \beta^t$, the annuity value of spending, and debt
absorbs the gap in each year.

**7.** *The fiscal theory: with $B/P = s/r$, find $P$ for $B = 100$, $s = 2$, $r = 0.02$, and after $s$ falls to
1.5.*

*Solution.* $P = Br/s = 100 \times 0.02 / 2 = 1$. With $s = 1.5$, $P = 2/1.5 = 1.33$: the price level rises a third,
since the nominal debt is now backed by smaller surpluses.

**8.** *$\bigstar$ Default: a country owing $b$ defaults if a random cost $\kappa \sim F$ is below $b$; derive the
bond price $q(b) = (1 - F(b))/(1+r)$ and the most it can raise.*

*Solution.* The country repays when $\kappa \ge b$, with probability $1 - F(b)$; risk-neutral lenders who recover
nothing pay $q(b) = (1-F(b))/(1+r)$ per unit promised. It raises $b\,q(b)$, which is maximized where
$1 - F(b) - b f(b) = 0$: past that point promising more raises less, the debt Laffer curve, and a country there is
rationed out of the market.

## Lab and interactive

- `python -m videos.economics.labs 32`: debt dynamics, the 90% recomputation, the Ramey-Zubairy multipliers, the
  missing intercept, the narrative tax response, the New Keynesian multiplier at the zero bound, tax smoothing, and
  Arellano's model.
- The interactive (course site): the minister's budget. The reader sets the interest rate, growth, the starting debt
  and a fiscal plan, and the multiplier, and watches the debt ratio and output over twenty years: with a large
  multiplier, sharp austerity raises the debt ratio before it lowers it.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[32]`; the spending and tax multipliers are
dials (`explainer/economics/dials.py`); the IMF's 2010 forecasts are a *Called it?* entry
(`explainer/economics/calls.py`). The replication data (Herndon, Ash and Pollin; Ramey and Zubairy; Ramey's Handbook
tax files; Blanchard and Leigh) were retrieved on 2026-11-20 from the authors' pages, and FRED's series on 2026-11-19
and 2026-11-20. The spreadsheet range is from Herndon, Ash and Pollin's paper; Greece's 53.5% nominal haircut is the
ESM's figure.
