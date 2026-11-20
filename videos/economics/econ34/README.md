# Economics, Built: Part 34, The Open Economy

Part 34 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first of Act VII, *The World Economy*. It asks what sets the price of one money
in terms of another, and what a country cannot have at once. Its answer: asset markets set it, through interest
rates, expectations and the world's demand for safe assets, far more than trade does; prices pull it back toward
parity only slowly, and month to month no model beats the random walk. And a country cannot have at once a fixed
exchange rate, capital that moves freely and a monetary policy of its own: it chooses two, and markets test the
choice.

It opens on Wednesday 16 September 1992, in four acts: in the morning the Bank of England raises its rate from 10%
to 12%; in the afternoon it announces 15%; all day it buys pounds with its reserves; in the evening the Chancellor
suspends sterling's membership of the European Exchange Rate Mechanism. From there it covers:

- the pound against the mark in the ERM's band, Britain's reserves, and interest rates: sterling fell from 2.81 marks
  in August 1992 to 2.45 in October (13%), and Britain's three-month rate from 10.4% to 6.2% by February 1993;
- the balance of payments as accounts: the current account is saving minus investment; America's deficit reached
  6.2% of GDP in 2006 and its net international investment position went from −12% of GDP to −69%;
- a game: you govern the Island's central bank, its currency pegged, its economy in recession, its reserves draining;
  Obstfeld's model shows why, in a middle zone of slack, the peg falls if traders expect it to;
- purchasing power parity: the Big Mac index (a Big Mac costs $9.04 in Switzerland and $2.45 in India against $6.22
  in America), Balassa and Samuelson's tilt (loose: a correlation of 0.29 across 51 countries), and the half-life of
  real exchange rates over 150 years in 18 countries: 5.2 years, and 2.6 since 1973;
- uncovered interest parity and Fama's puzzle: the slope is negative for six of seven currencies against the dollar;
  the carry trade earned 4.2% a year with a Sharpe ratio of 0.57, and lost 10.9% in October 2008;
- Meese and Rogoff rerun out of sample: interest parity and an AR(1) forecast four currencies no better than "no
  change" at one, three and twelve months;
- Mundell and Fleming, and the trilemma: under a peg fiscal policy moves output and money does not; under a float,
  the reverse;
- Dornbusch's overshooting: with sticky prices, a 10% rise in money makes the currency fall 15% at once;
- an intermission without narration: the pound in dollars, month by month since 1971, as a tune;
- three generations of currency crises: Krugman's predictable attack, which on the Island comes in year 15, five
  years before reserves would have run out; Obstfeld's self-fulfilling crises, and Sweden's 500% overnight rate;
  balance sheets and the Asian crisis;
- the IMF and its critics, from Asia in 1997 to the institutional view of 2012;
- currency areas: Mundell's criteria, the euro's convergence and its crisis (Greek ten-year yields reached 29% in
  2012), and "whatever it takes";
- global imbalances: China's surplus of 9.8% of GDP in 2007, America's deficit of 5.8% in 2006, Germany's surplus of
  8.1% in 2015; the saving glut and the exorbitant privilege;
- the dollar: pass-through into American import prices (0.04 at once, 0.44 after a year), the global financial cycle,
  and the yuan;
- two dials: exchange-rate pass-through (first rows) and the half-life of PPP deviations (new); *Called it?* on Meese
  and Rogoff (right); a frontier chapter on intermediaries, the disconnect and convenience yields.

## Build it

```bash
python -m videos.economics.econ34.compute              # every number (about half a minute), into .cache/econ34/
python tools/qa_scene.py econ34 Dornbusch              # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ34 -q l   # the whole part, silent preview
python tools/build.py econ34                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 34                     # the lab
```

The data are in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): from FRED, the Board of Governors' exchange rates (H.10)
and broad dollar index, the OECD's interest rates and ten-year yields, the BEA's current account and the net
international investment position, the IMF's figures for Britain's reserves, the BLS's import prices excluding fuel,
and the VIX; the World Bank's current accounts; The Economist's Big Mac index (CC BY 4.0); and the
Jordà-Schularick-Taylor Macrohistory Database (release 6, CC BY-NC-SA 4.0) for exchange rates and prices since 1870.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | One day in four acts | 16 September 1992; the band, the reserves, the rates; the question; objectives |
| 1 | The balance of payments | The accounts; saving minus investment; America's deficit and its debts |
| 2 | Play it: the governor | Defend the peg, ask the anchor to cut, or float; Obstfeld's three zones |
| 3 | Purchasing power parity | The Big Mac index; Balassa and Samuelson; the half-life since 1870 |
| 4 | Interest parity and the carry trade | Covered and uncovered parity; Fama's slopes; the carry trade and its crashes |
| 5 | The random walk | Meese and Rogoff, rerun out of sample |
| 6 | Mundell-Fleming and the trilemma | Policy under fixed and floating rates; the impossible trinity |
| 7 | Overshooting | Dornbusch's model; the jump and the slow return |
| — | Intermission | The pound in dollars since 1971, as a tune |
| 8 | Currency crises, three generations | Krugman's attack; self-fulfilling crises; balance sheets |
| 9 | The IMF and its critics | Conditions; Asia in 1997; the Fund's own evaluation; capital controls |
| 10 | Currency areas and the euro | Mundell's criteria; yields before and after the crisis |
| 11 | Global imbalances | Current accounts since 1980; the saving glut; the exorbitant privilege |
| 12 | The dollar | Pass-through; the global financial cycle; the yuan |
| 13 | The Dials | Pass-through (first rows); the half-life of PPP deviations (new) |
| 14 | In practice | Reserve managers, strategists, treasurers, the IMF's desks; *Called it?* on Meese and Rogoff |
| 15 | Frontier | Gabaix and Maggiori; Itskhoki and Mukhin; convenience; open questions |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 35, *Trade I: Comparative Advantage* |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's open economy (`explainer.economics.agora.openecon`) with
the Island's Part 34 truths, or from the Data Room; the narration states the cached numbers.

- **Black Wednesday.** Marks per pound as the product of monthly dollars per pound and marks per dollar; the ERM band
  as 2.95 marks ± 6%.
- **Real exchange rates.** From the Macrohistory Database, the log of local currency per dollar plus the log of
  America's price level minus the local one; each country's series demeaned over the sample; a pooled AR(1) on annual
  data, and the half-life $\ln 0.5/\ln\rho$.
- **Balassa-Samuelson.** The Big Mac index's latest survey: the raw valuation against the dollar on the log of GDP per
  head, by least squares, across the countries with both.
- **Fama's regression.** For each currency from 1979, the change in the log dollar price of the currency over three
  months on the three-month interest differential (America's minus the other's) for those months, with Newey-West
  standard errors. Uncovered parity predicts a slope of one. The mark is spliced to the euro at 1.95583.
- **The carry trade.** From 1985, monthly: hold the two highest-yielding of eight currencies (the dollar included),
  funded by the two lowest-yielding; the return is the rate gap plus the change in the currencies' values.
- **Meese and Rogoff.** End-of-month rates from daily data (monthly averages would make changes falsely predictable),
  from 1980, for the pound, yen, Canadian dollar and Swiss franc. For each month after a ten-year window, the change
  one, three and twelve months ahead forecast by no change, by the interest gap, and by an AR(1) in monthly changes
  fitted on the window; root mean squared errors pooled over currencies.
- **Mundell-Fleming.** A small open economy in deviations with $r = r^*$: IS $y = 0.5y + g - 0.6r + 0.4e$, LM
  $m = 0.5y - 0.8r$; a unit rise in $g$ or $m$ under each regime.
- **Dornbusch.** Money up 10%; money demand's interest semi-elasticity $\lambda = 4$; prices close half the gap a year
  ($\theta = 0.5$). The currency jumps by $(1 + 1/(\lambda\theta))$ times the money shock and converges at rate $\theta$.
- **Krugman.** Peg 100, domestic credit 60 growing by 2 a year, money demand's semi-elasticity $\alpha = 5$; the attack
  when the shadow rate $d + \alpha\mu$ reaches the peg.
- **Pass-through.** Monthly changes in the log of the BLS import price index excluding fuel on the current and twelve
  lagged changes in the log of the Fed's broad dollar index, December 2001 to December 2019; cumulative coefficients.
  (Over all imports the estimate is contaminated by oil, whose dollar price moves against the dollar.)

## Problems and solutions

**1.** *Accounts: national saving is 18% of GDP and investment 22%. Find the current account; then cut the budget
deficit by 2 points with private saving fixed.*

*Solution.* The current account is saving minus investment: $18 - 22 = -4\%$ of GDP, borrowed from abroad. Cutting the
deficit by 2 points raises national saving to 20%, so with investment unchanged the deficit halves to 2%. If private
saving fell to offset it, as Ricardian equivalence would have it, nothing would change; the evidence of the twin
deficits is that it offsets only part.

**2.** *Big Mac: it costs $6.22 in America and 6.50 francs in Switzerland, at 0.80 francs per dollar. Find the implied
PPP rate and the franc's valuation.*

*Solution.* The rate that would equalize the price is $6.50/6.22 = 1.045$ francs per dollar. At the market rate of
0.80 the Swiss burger costs $6.50/0.80 = \$8.13$, so the franc is $8.13/6.22 - 1 = 31\%$ overvalued: it buys fewer
burgers in Switzerland than its dollars would buy in America.

**3.** *Half-life: show that an AR(1) with coefficient $\rho$ has half-life $\ln 0.5/\ln\rho$; evaluate at
$\rho = 0.87$ a year and $0.98$ a month.*

*Solution.* A deviation $q_0$ is expected to be $\rho^t q_0$ after $t$ periods; setting $\rho^t = 1/2$ gives
$t = \ln 0.5/\ln\rho$. At 0.87 a year, $0.693/0.139 = 5.0$ years, close to this part's estimate since 1870. At 0.98 a
month, $0.693/0.0202 = 34$ months, or 2.9 years.

**4.** *Parity: spot $1.25 per pound, dollar rate 4%, sterling rate 5%. Find the one-year forward rate; and the carry
return if the pound then rises 3%.*

*Solution.* Covered parity: $F = S(1 + i_\$)/(1 + i_\pounds) = 1.25 \times 1.04/1.05 = \$1.238$, a forward discount on
the pound equal to the rate gap. The carry trade borrows dollars at 4% and holds pounds at 5%: if the pound rises 3%,
it earns $1.05 \times 1.03/1.04 - 1 = 4.0\%$, the rate gap plus the appreciation. Uncovered parity would have predicted
a 1% fall in the pound and a return of zero.

**5.** *Mundell-Fleming: with $y = ay + g - br + ce$, $m = ky - hr$ and $r = r^*$, derive the effects of $g$ and $m$
under each regime.*

*Solution.* With $r$ fixed at $r^*$, the LM curve alone gives $y = (m + hr^*)/k$. Floating: $m$ is set, so
$dy = dm/k$; fiscal policy cannot move output, and the IS curve gives the currency's appreciation
$de = -dg/c$ (with $dm = 0$), which crowds out net exports one for one. Monetary policy: $dy = dm/k$, with
$de = (1-a)dm/(kc)$, a depreciation. Fixed: $e$ is set and the money stock must adjust, so the IS curve alone gives
$dy = dg/(1-a)$, the full closed-economy multiplier, with $dm = k\,dy$ supplied by the central bank buying foreign
currency; an attempt to change $m$ is reversed at once, $dy = 0$.

**6.** *Overshooting: derive the impact factor $1 + 1/(\lambda\theta)$; evaluate at $\lambda = 4$ with $\theta = 0.5$ and
$\theta = 2$.*

*Solution.* After a permanent rise $dm$, the long-run currency and prices rise by $dm$. At impact prices are fixed,
so money-market equilibrium $m - p = -\lambda i$ needs $i$ to fall by $dm/\lambda$. Interest parity then needs the
currency expected to appreciate at $dm/\lambda$; with regressive expectations $\dot s = -\theta(s - \bar s)$, that
requires $s - \bar s = dm/(\lambda\theta)$ at impact, so $s$ jumps by $dm(1 + 1/(\lambda\theta))$. At $\lambda = 4$,
$\theta = 0.5$: 1.5 times the shock. At $\theta = 2$, prices adjust faster and the overshoot shrinks: 1.125.

**7.** *Krugman: reserves 40, credit 60 growing 2 a year, peg 100, $\alpha = 5$. When do reserves run out unaided, and
when does the attack come?*

*Solution.* Money is credit plus reserves and equals 100 under the peg, so reserves fall by 2 a year and would run out
at $(100 - 60)/2 = 20$ years. Once the currency floats, prices rise with credit at 2 a year, money demand falls by
$\alpha\mu = 10$, and the floating rate is $d + 10$. The attack comes when that shadow rate reaches the peg:
$60 + 2T + 10 = 100$, $T = 15$, when the last 10 of reserves are taken in a single day. Any later, and speculators
holding the currency would take a predictable loss.

**8.** *$\bigstar$ Obstfeld: with loss $(u + \gamma x)^2$ and cost $C$, find the band of $u$ with two equilibria; show
that it widens with $\gamma\delta$.*

*Solution.* With no devaluation expected ($x = 0$) the government defends while $u^2 < C$, that is $u < \sqrt C$.
With a devaluation of $\delta$ expected it gives up once $(u + \gamma\delta)^2 > C$, that is $u > \sqrt C - \gamma\delta$.
For $\sqrt C - \gamma\delta < u < \sqrt C$ both are self-confirming: the band has width $\gamma\delta$, wider when an
expected devaluation raises the interest rate a defence needs by more ($\gamma$) or when the expected devaluation is
larger ($\delta$). With $C = 1$, $\gamma = 1$ and $\delta = 0.5$ it is $(0.5, 1)$, and the Island, at 0.75, is inside it.

## Lab and interactive

- `python -m videos.economics.labs 34`: real exchange rates and their half-lives, the Big Mac index and
  Balassa-Samuelson, Fama's regressions, the carry trade, the Meese-Rogoff horse race, Mundell-Fleming, overshooting,
  Krugman's attack, Obstfeld's regions, and pass-through.
- The interactive (course site): the governor's dilemma. The reader sets the depth of the recession and how much
  traders expect a devaluation, and sees when the peg holds, falls, or depends on what traders believe.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[34]`; exchange-rate pass-through and the
half-life of PPP deviations are dials (`explainer/economics/dials.py`); Meese and Rogoff's 1983 paper is a *Called it?*
entry (`explainer/economics/calls.py`). FRED's series were retrieved on 2026-11-20, the Big Mac index on 2026-11-20
from The Economist's public repository, and the World Bank's current accounts on 2026-11-20. The events of 16
September 1992, the Treasury's 2005 estimate of the cost (about £3.3 billion) and Sweden's 500% overnight rate are as
reported at the time and since; Gopinath, Itskhoki and Rigobon's pass-through estimates are from their paper's
abstract.
