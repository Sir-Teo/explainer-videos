# Economics, Built: Part 31, The Central Bank

Part 31 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the seventh of Act VI, *Money and the Cycle*. It asks what a central bank actually
does, and how we know what it achieves. Its answer: it sets the price of overnight money, by the reserves it supplies
or by the rate it pays on them, and it moves borrowing costs further out by what it promises and what it buys. We know
what it achieves only where we can find the part of its decisions that is its own; where we can, a tightening lowers
output after a year or more and prices later, by amounts still argued, and a central bank that is believed can
sometimes do the most by never having to act.

It opens on 26 July 2012, when Spain was paying 6.8% to borrow for ten years and Italy
6.0%, against Germany's 1.2%, and Mario Draghi told a London audience that the ECB
would do whatever it takes to preserve the euro; two years later Spain paid 2.7%, and the programme
behind the sentence had never been used. From there it covers:

- the central bank's balance sheet as T-accounts; the market for reserves, a corridor (scarce reserves: ten more
  units move the Island's rate) and a floor (abundant reserves: the rate is the rate paid on reserves); America's move
  from one to the other (reserves of $10 billion in August 2008, $4.2 trillion at
  the peak);
- a game: in early 1979 the data of the day put output 1.5% below its trend; where does today's
  estimate put it? (+2.3%: above potential);
- transmission through rates, credit, asset prices, the exchange rate and expectations, and the 2022 tightening, when
  the 2-year yield reached 1.9% before the first rise;
- the identification problem: on the Island a rate rise goes with output +1.37% higher next
  quarter, though the planted effect is negative; the price puzzle in US data (prices +0.34% two years after a
  tightening in a recursive VAR, +0.17% with commodity prices);
- four answers, run on 300 Island histories where the truth is known: the naive regression and recursive VARs
  get it wrong; narrative shocks and clean high-frequency surprises recover it; an information effect halves it;
- the consensus: in this film's VAR, industrial production -1.3% after
  29 months, prices later; published estimates from −0.7% to −4.3%;
- Taylor's rule with the data of the day (Orphanides): through the 1970s the trend of the day put output
  2.4 points further below potential than today's estimates do;
- an intermission without narration: the federal funds rate since 1954, with the Fed's chairs, as a tune;
- the zero bound in practice (Japan from 1999; the Fed for 107 months; the ECB below zero for
  98 months);
- quantitative easing in T-accounts, the Fed's balance sheet ($0.9 trillion in 2008, $9.0 trillion
  in 2022), and the event study of QE1 (-94 basis points on the ten-year yield over
  eight days; +143 on all the others);
- forward guidance, negative rates and yield-curve control, and what each achieved;
- the neutral rate: estimated on the Island by the Kalman filter (a 90% band of ±0.8
  points), and the New York Fed's estimates (3.7% for the US in 2000, 1.0%
  now);
- the euro crisis as self-fulfilling yields (equilibria at 2.5% and
  6%), and the backstop that removes the bad one;
- communication: from secrecy before 1994 to the dots, and the taper tantrum of 2013 (+110 basis
  points);
- three dials (new): the effect of a tightening, of asset purchases, and the neutral rate; *Called it?* on Romer and
  Romer's claim that the Fed's staff forecast inflation better than the private sector (partly right); a frontier
  chapter on the 2021–24 cycle, runoff and the Fed's losses.

## Build it

```bash
python -m videos.economics.econ31.compute              # every number (about a minute), into .cache/econ31/
python tools/qa_scene.py econ31 Methods                # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ31 -q l   # the whole part, silent preview
python tools/build.py econ31                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 31                     # the lab
```

The data are in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): from FRED, the Federal Reserve's assets, reserves and
remittances, the funds rate and its target, the rates on reserves, Treasury yields, industrial production, the CPI and
the PPI, the ECB's deposit rate, Japan's call rate, the FOMC's longer-run projection and the OECD's European bond
yields; from the Philadelphia Fed, real-time GDP vintages, the Greenbook (Tealbook) projections and the SPF's medians;
from the New York Fed, the Holston–Laubach–Williams estimates.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Whatever it takes | Draghi's sentence and the yields; the question; objectives |
| 1 | The balance sheet: reserves, a corridor and a floor | T-accounts; the market for reserves; America's move to a floor |
| 2 | Play it: the chair in 1979 | The data of the day against today's estimate of the gap |
| 3 | Transmission | Five channels; the 2022 tightening and the 2-year yield |
| 4 | The identification problem | The Island's naive regression; the price puzzle in US data |
| 5 | Four answers, scored against the truth | Recursive VARs, narrative shocks, high-frequency surprises and the information effect, on 300 Islands |
| 6 | The consensus response | A US VAR with commodity prices; published sizes |
| 7 | Rules with the data of the day | Real-time output gaps since 1966; Taylor's rule in real time |
| — | Intermission | The federal funds rate since 1954, as a tune |
| 8 | The zero bound in practice | Japan, the United States, the euro area |
| 9 | Quantitative easing | T-accounts; the Fed's balance sheet; the QE1 event study |
| 10 | Forward guidance, negative rates, yield-curve control | Dates and thresholds; the ECB and Japan below zero; Japan's and Australia's yield targets |
| 11 | The neutral rate, estimated | The Island's Kalman filter; Holston, Laubach and Williams; the dots |
| 12 | The euro and the lender of last resort | Self-fulfilling yields; the backstop; Britain against Spain |
| 13 | Communication as policy | From 1994 to the dots; the taper tantrum |
| 14 | The Dials | The effect of a tightening, of asset purchases, and the neutral rate (new) |
| 15 | In practice | Policy staff and rates strategists; *Called it?* on the Greenbook |
| 16 | Frontier | The 2021–24 cycle; losses and runoff; open questions |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 32, *The Treasury* |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's central bank (`explainer.economics.agora.cb`) with the
Island's Part 31 truths, or from the Data Room; the narration states the cached numbers.

- **The Island's monetary history.** Output and inflation respond to policy with a lag; the bank sets its rate after
  seeing this quarter's output and inflation and two pieces of private news about next quarter's cost and demand
  shocks; a true policy shock (s.d. 0.25 points) is added. 300 histories of 240 quarters each.
- **The methods.** Naive: local projections on the change in the rate. Recursive VAR: output, inflation and the rate,
  four lags, the rate ordered last; again with a noisy commodity-price proxy for the cost news. Narrative: the residual
  of the rate on the bank's information (its news included), then local projections. High-frequency: the true shock
  plus noise, with or without 60% of the rate's reaction to the demand news, as an instrument in local projections.
- **The US VAR.** Monthly, 1965–2007: log industrial production, log CPI, (log PPI), the funds rate ordered last; 12
  lags; responses to a one-point shock; 5–95% bands from 200 residual bootstraps.
- **Real time.** Each first-quarter vintage of real GDP (real GNP before 1992) from the Philadelphia Fed, 1966–2008; a
  log-linear trend fitted to everything the vintage holds; the gap at its last quarter, against the CBO's potential
  with today's data. Taylor's rule is $i = 2 + \pi + 0.5(\pi - 2) + 0.5x$ with CPI inflation over the year before.
- **The natural rate.** A random-walk $r^*$ (s.d. 0.12 a quarter) in the Island's IS curve, estimated by a scalar
  Kalman filter from output and the real rate.
- **Self-fulfilling yields.** Debt of 120% of GDP; default when the interest bill exceeds a normal fiscal capacity
  whose mean and spread put the equilibria at 2.5% and 6%; risk-neutral lenders with nothing recovered; a backstop
  at 3.5%.
- **QE1.** The ten-year Treasury yield (DGS10), close to close, on Gagnon, Raskin, Remache and Sack's eight baseline
  days.
- **Called it?** For each quarter, the Greenbook nearest mid-quarter and the SPF's median, each forecasting GDP-price
  inflation over the next four quarters, against today's GDP price index.

## Problems and solutions

**1.** *The corridor: with reserve demand $i = f + (c - f)\,\bar\Phi((R - n)/s)$, find the reserves that put the rate
mid-corridor, and the rate's slope there.*

*Solution.* Mid-corridor means $\bar\Phi((R-n)/s) = 1/2$, so $R = n$. The slope is
$di/dR = -(c-f)\,\phi(0)/s$; with $f = 1$, $c = 3$, $n = 50$, $s = 15$, that is $-2 \times 0.399/15 = -0.053$
points per unit of reserves: ten units lower the rate about half a point.

**2.** *The floor: show that in a floor system the rate does not change when reserves fall by a small amount, and that
raising the rate on reserves raises it one for one.*

*Solution.* With $R \gg n$, $\bar\Phi((R-n)/s) \approx 0$, so $i \approx f$ and $di/dR \approx 0$: a small change in
reserves leaves the rate where it is. No bank lends reserves for less than $f$, which it can earn at the central bank,
and with reserves abundant none needs to borrow for more, so $i = f$; raising $f$ raises $i$ by the same amount.

**3.** *QE in T-accounts: the central bank buys 100 of bonds from a household; write every balance sheet that
changes.*

*Solution.* The central bank: bonds $+100$ (assets), reserves $+100$ (liabilities). The household's bank: reserves
$+100$ (assets), deposits $+100$ (liabilities). The household: bonds $-100$, deposits $+100$ (both assets). The
public's holdings of money rise, and of long bonds fall, by the same amount.

**4.** *Recursive identification: in a two-variable VAR with the rate ordered last, show that the shock is the
residual of the rate on the other variable's innovation.*

*Solution.* With innovations $u = (u_x, u_i)$ and $\Sigma = LL'$, $L$ lower triangular, $u = L\varepsilon$ gives
$u_x = L_{11}\varepsilon_x$ and $u_i = L_{21}\varepsilon_x + L_{22}\varepsilon_i$. So $u_i = (L_{21}/L_{11})u_x +
L_{22}\varepsilon_i$, with $L_{21}/L_{11} = \mathrm{cov}(u_i,u_x)/\mathrm{var}(u_x)$: the shock (scaled) is the
residual of the rate's innovation on output's. The ordering assumes output does not respond to the shock within the
period.

**5.** *The price puzzle: if the bank raises $i_t$ on news $n_t$ that raises $\pi_{t+1}$, and $n_t$ is left out, sign
the bias in the estimated response of $\pi$.*

*Solution.* Let $\pi_{t+1} = \beta i_t + c\,n_t + e$ with $\beta \le 0$ and $i_t = \phi n_t + v_t$ with $\phi, c > 0$.
Regressing $\pi_{t+1}$ on $i_t$ alone gives
$\beta + c\,\phi\,\mathrm{var}(n)/(\phi^2\mathrm{var}(n) + \mathrm{var}(v))$: the bias is positive, and when the
bank's news is large relative to its shocks it can make the estimated effect of a tightening on prices positive.

**6.** *Real time: fit a log-linear trend to output that grew 4% a year for 20 years and 2.5% for the next 6; find the
end-point gap.*

*Solution.* Over the 27 annual points the fitted slope is 3.8% a year, and the trend at the last point lies 5.0%
above output: a gap of $-5.0\%$, all of it an artefact of the slowdown, which the trend has not yet absorbed. That is
the 1970s' error in miniature.

**7.** *Self-fulfilling yields: with default when $r\,b > F$, $F \sim N(\mu, \sigma^2)$, derive
$R(r) = (1 + r_f)/(1 - p(r)) - 1$ and count its fixed points.*

*Solution.* Lenders are paid $1 + r$ with probability $1 - p(r)$, $p(r) = \Phi((rb - \mu)/\sigma)$, and nothing
otherwise; indifference with the safe rate gives $(1+r)(1-p(r)) = 1 + r_f$. Near $r_f$, $p$ is tiny, so $R(r) < r$
just above $r_f$ only if $p$ is small enough: then $R$ crosses the diagonal once from above (a stable, low equilibrium)
and, since $p$ rises steeply, once more from below (an unstable one), beyond which $R(r) > r$ always. With the
Island's numbers, $2.5\%$ and $6\%$. If $\mu$ is small, $R(r) > r$ everywhere: no equilibrium, and no one lends.

**8.** *$\bigstar$ The information effect: if a surprise is $s = v + \lambda n$, find the bias of the instrumented
response of output when $n$ raises it.*

*Solution.* Let output $h$ periods on respond $\beta_h$ to $v$ and $\gamma_h$ to the news $n$, and the rate respond 1 to
$v$ and $\delta$ to $n$. The IV estimate is $\mathrm{cov}(y_{t+h}, s)/\mathrm{cov}(i_t, s) = (\beta_h\sigma_v^2 +
\lambda\gamma_h\sigma_n^2)/(\sigma_v^2 + \lambda\delta\sigma_n^2)$. Its bias is
$\lambda\sigma_n^2(\gamma_h - \delta\beta_h)/(\sigma_v^2 + \lambda\delta\sigma_n^2)$, positive when good news about
demand raises output: a tightening that reveals good news looks less contractionary than it is, as on the Island.

## Lab and interactive

- `python -m videos.economics.labs 31`: the corridor and the floor, the Island's methods against the truth, the US VAR
  with and without commodity prices, real-time output gaps and Taylor's rule, the QE1 event study, the Kalman filter
  for $r^*$, self-fulfilling yields, and the Greenbook against the SPF.
- The interactive (course site): the chair, 1966–1990. Each year the reader sees inflation and the gap as they were
  published then and sets the funds rate; the page shows what the rule said with the data of the day and with today's,
  and what the Federal Reserve did.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[31]`; the effect of a tightening, of asset
purchases and the neutral rate are dials (`explainer/economics/dials.py`); Romer and Romer's claim about the Greenbook
is a *Called it?* entry (`explainer/economics/calls.py`). FRED's series and the Philadelphia and New York Fed files
were retrieved on 2026-11-19 and 2026-11-20. Draghi's sentence is quoted from the speech; the communication dates are
the Federal Reserve's; the QE1 days and figures are from Gagnon, Raskin, Remache and Sack's *Economic Policy Review*
article; Eurostat's 2011 debt ratios (Spain 69.3%, the United Kingdom 85.0%) are from its April 2012 release.
