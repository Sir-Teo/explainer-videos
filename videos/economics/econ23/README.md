# Economics, Built: Part 23, Capital and Asset Prices

Part 23 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth of Act V, *The Long Run*. It asks what a claim on the future is worth, and
how that decides what gets built, and answers: the expected value of what it pays, weighted by how much people will
need it when it pays, so that risk is priced by its covariance with bad times. Firms build until the market values
capital at what it costs, slowly, and wait when the future is uncertain. But stocks have paid far more than smooth
consumption can explain, prices swing more than dividends, and bubbles form even in the laboratory.

It opens with Rajnish Mehra and Edward Prescott's two numbers (1985): the standard model allows an equity premium of
at most 0.35% a year with sensible preferences; from 1889 to 1978 the record was 6.18% (stocks 6.98% a year after
inflation, bills 0.80%). From there it covers:

- present value and the Gordon formula; a one-point rise in the discount rate takes a fifth off a long-lived asset;
  Shiller's real price-dividend ratio since 1871;
- investment: Jorgenson's user cost, Tobin's q and Hayashi's adjustment costs, with the Island's firm after a rise in
  productivity;
- the option to wait (McDonald and Siegel 1986; Dixit and Pindyck 1994) and uncertainty shocks (Bloom 2009);
- Modigliani and Miller (1958): the pie and its slices, the cost of levered equity, and what breaks the theorem;
- a game: price a coconut tree that fruits only in good years (8 coconuts, against an average harvest of 10 and an
  insurance tree's 12);
- the Lucas tree (1978) and the stochastic discount factor; the risk-free rate and risk premia as covariance;
- the consumption CAPM on Shiller's century of data: an implied risk aversion of about 12;
- the puzzle computed three ways: Mehra and Prescott's economy solved for every patience and risk aversion, the
  Hansen–Jagannathan bound (risk aversion of at least 8.2), and the risk-free rate puzzle (Weil 1989);
- three repairs: habits (Campbell and Cochrane 1999), simulated; long-run risk (Bansal and Yaron 2004); rare disasters
  (Rietz 1988; Barro 2006), with a 5.1% premium and a 2.3% safe rate at a risk aversion of 3.5;
- an intermission without narration: a real dollar in stocks and in one-year bonds from 1871 to 2013 ($7,972 against
  $34), the stock dollar as a tune;
- excess volatility (Shiller 1981) and the dividend yield's power over 1, 5 and 10 years; efficient markets in one card;
- bubbles: rational bubbles and Tirole's condition; Smith, Suchanek and Williams's laboratory markets, with the
  Island's version; *Called it?* on Irving Fisher's permanently high plateau (wrong);
- housing as an asset: the user cost and the US price-to-rent ratio since 1987;
- two dials (risk aversion, with three rows added; investment's response to the user cost, new), capital budgeting,
  valuation and pension discount rates in practice, and a frontier chapter on the return on everything (Jordà et al.
  2019) and intermediary asset pricing.

## Build it

```bash
python -m videos.economics.econ23.compute              # every number (seconds), into .cache/econ23/
python tools/qa_scene.py econ23 Puzzle                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ23 -q l   # the whole part, silent preview
python tools/build.py econ23                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 23                     # the lab
```

The data are in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): Robert Shiller's annual series (the S&P composite's
price, dividends and real return, one-year interest rates, real consumption per head, and his ex post rational
prices), the S&P CoreLogic Case-Shiller national index and the CPI's rent of primary residence (via FRED), and Mehra and
Prescott's table, transcribed in `tables.py`.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | What is a claim on the future worth, and how does that decide what gets built? | Mehra and Prescott's two numbers: at most 0.35% against 6.18% (1889–1978), a factor of about seventeen; why the price of risk matters; not investment advice; objectives |
| 1 | Present value and the Gordon formula | $P = \sum D_t/(1+r)^t$; $P = D_1/(r-g)$; a dividend of 4 growing 3%: 100 at 7%, 80 at 8%, duration 25 years; Shiller's real price-dividend ratio: 17 in 1871, 27 on average, 42 in 2012; real dividends up 1.3% a year |
| 2 | Investment: the user cost and Tobin's q | Jorgenson's $c = p_K(r + \delta - \pi_K)(1 - \tau z)/(1-\tau)$: 0.13 a year on the Island; $q$; $I/K = (q-1)/\phi$; Hayashi; productivity up 20%: $q$ jumps to 1.48, investment 12% of capital against 8% depreciation, capital from 2.98 to 3.91 |
| 3 | The option to wait | Irreversibility and delay; the threshold $\beta/(\beta-1)$ times cost: 1.42, 2.00, 2.76 and 3.73 at volatilities of 10–40% (interest 4%); Bloom's uncertainty shocks |
| 4 | Modigliani and Miller: the pie and its slices | The pie; $r_E = r_A + \frac{D}{E}(r_A - r_D)$: 8% and 4% give 12% on half-levered equity; taxes, bankruptcy, information (Myers and Majluf), agency |
| 5 | Play it: price a coconut tree | 20 coconuts in good years, 0 in bad; $m$ = 0.8 and 1.2; four answers; the tree 8, the safe coconut 1 per coconut, the insurance tree 12; a 25% expected return against 0 |
| 6 | The Lucas tree and the stochastic discount factor | Lucas (1978); $p = \mathbb{E}[mx]$, $m = \beta u'(c_{t+1})/u'(c_t)$; $R_f = 1/\mathbb{E}[m]$; $\mathbb{E}[R] - R_f = -R_f\operatorname{cov}(m,R)$ |
| 7 | Risk premia and the consumption CAPM | $\mathbb{E}[R] - R_f \approx \gamma\operatorname{cov}(\Delta\ln c, R)$ (Breeden 1979); Shiller's data 1889–1978: stocks 7.4%, bonds 1.7%, premium 5.7%, consumption growth s.d. 4.0%, correlation 0.57, covariance 0.0046, implied $\gamma$ 12 (14 over 1889–2009) |
| 8 | The equity premium puzzle, computed | Mehra and Prescott's two-state economy solved for 3,600 combinations: with a safe rate below 4%, at most 0.36%; the Hansen–Jagannathan bound: Sharpe ratio 0.30, consumption s.d. 3.6%, $\gamma \ge 8.2$; the safe rate it implies, 15%, against 2%; the fact entered |
| 9 | Three repairs: habits, long-run risk, disasters | Campbell and Cochrane's surplus ratio simulated: the price of risk 0.51 at the average, up to 1.14; Bansal and Yaron's persistent component with Epstein–Zin preferences; rare disasters (1.7% a year, falls of 15–65%, average 30%): at $\gamma$ = 3.5, a premium of 5.1% and a safe rate of 2.3%, against 0.16% and 12% without |
| | Intermission: a dollar in stocks, a dollar in bonds | No narration: a real dollar from 1871 to 2013, stocks $7,972, one-year bonds $34; 1929, 1973–74, 2000 and 2008 marked; the stock dollar as a tune |
| 10 | Do prices move too much? | Shiller (1981): the real price against $P^*$, standard deviations 393 and 177; the dividend yield's $R^2$ for returns over 1, 5 and 10 years: 0.03, 0.15, 0.24 (overlapping windows); Samuelson, Fama, Campbell and Shiller; the fact entered |
| 11 | Bubbles | $b_t = \mathbb{E}_t[m_{t+1}b_{t+1}]$; no bubble with a final date; Tirole (1985) and $r < g$; Smith, Suchanek and Williams: 14 of 22 markets bubbled; the Island's market with 7 trend followers among 12; *Called it?*: Fisher (October 1929), wrong |
| 12 | Housing as an asset | Poterba's user cost; price-to-rent as one over it; the US ratio (January 2000 = 1): 1.49 in May 2006, 0.94 in February 2012, 1.36 in August 2026 |
| 13 | The Dials: risk aversion, and investment's response to its cost | Risk aversion with this part's rows (8.2, 12.3, 3.5); the new user-cost dial: Chirinko, Fazzari and Meyer −0.25, Hassett and Hubbard −0.5 to −1, Zwick and Mahon −1.6 |
| 14 | In practice: capital budgeting, valuation, pensions | NPV at the project's risk; terminal values; public pensions discounted at about 8% against Treasury rates, about $3 trillion short (Novy-Marx and Rauh); who uses this |
| 15 | Frontier: the return on everything | Jordà et al. (2019), 16 countries 1870–2015: equities about 7%, housing about 7–8%, bonds 2.5%, bills 1%; intermediary asset pricing (He and Krishnamurthy; Adrian, Etula and Muir); open questions |
| | Recap, problems, and the road ahead | The answer; twelve lines; problems; reading; Diamond's coconut island, and Part 24 |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's asset prices and investment (`explainer.economics.agora.assets`)
with the Island's Part 23 truths, or from the Data Room; the narration states the cached numbers.

- **Shiller's moments.** Annual real returns on the S&P composite (January to January) and on one-year bonds, and the
  growth of real consumption per head over the same year, 1889–1978 and 1889–2009.
- **Mehra and Prescott's economy.** Consumption growth of 1.8% ± 3.6% in a two-state Markov chain with persistence
  0.43; the price-dividend ratio by a linear solve; average returns over the stationary distribution, for 60 × 60
  values of $\beta \in [0.8, 0.999]$ and $\gamma \in [0.05, 10]$.
- **The bound.** $\sqrt{\exp(\gamma^2\sigma_c^2) - 1}$ against the Sharpe ratio; the safe rate from the lognormal
  formula with $\beta = 0.99$.
- **Disasters.** iid lognormal growth (2.5% ± 2%) times $(1-b)$ with probability 1.7%, $b$ from five sizes; closed
  forms for the safe rate and the claim to consumption; $\beta = e^{-0.03}$.
- **Habits.** Campbell and Cochrane's annual calibration ($\gamma = 2$, $\phi = 0.87$, $g = 1.89\%$, $\sigma = 1.5\%$);
  the sensitivity function and the conditional price of risk.
- **Hayashi's firm.** Profits $AK^{0.33}$, $\phi = 4$, $r = 5\%$, $\delta = 8\%$; the saddle path by shooting on the
  initial $q$.
- **The laboratory market.** Fifteen periods, dividends of 0, 8, 28 or 60 cents with equal chances; 12 traders, each a
  fundamental trader or a trend follower; the price the median bid.

## Problems and solutions

**1.** *Gordon: derive $P = D_1/(r-g)$ from $\sum_t D_1(1+g)^{t-1}/(1+r)^t$, and show that
$-\frac{dP/P}{dr} = \frac{1}{r-g}$.*

*Solution.* The sum is geometric with first term $D_1/(1+r)$ and ratio $(1+g)/(1+r) < 1$, so
$P = \frac{D_1/(1+r)}{1 - (1+g)/(1+r)} = \frac{D_1}{r-g}$. Then $\ln P = \ln D_1 - \ln(r-g)$ and
$d\ln P/dr = -1/(r-g)$: with $r - g = 4\%$, a price falls about 25% per point, or exactly 20% for a full point (100 to
80) because the derivative changes as $r$ rises.

**2.** *Hayashi: with cost $I + \frac{\phi}{2}I^2/K$ and shadow value $q$, show that $I/K = (q-1)/\phi$, and find $q$ in
a steady state.*

*Solution.* The firm chooses $I$ to maximize $qI - I - \frac{\phi}{2}I^2/K$; the first-order condition is
$q = 1 + \phi I/K$. In a steady state capital is constant, so $I/K = \delta$ and $q = 1 + \phi\delta$: with $\phi = 4$
and $\delta = 8\%$, $q = 1.32$. Above that, the firm invests more than depreciation and capital grows.

**3.** *The option to wait: with $dV = \mu V dt + \sigma V dW$, show that waiting's value $AV^\beta$ solves
$\frac12\sigma^2\beta(\beta-1) + \mu\beta - r = 0$, and derive the threshold $\frac{\beta}{\beta-1}I$.*

*Solution.* While waiting, the option $F(V)$ earns only capital gains, so $rF = \mu VF' + \frac12\sigma^2V^2F''$. Trying
$F = AV^\beta$ gives the quadratic; take the root above one. At the threshold $V^*$, value matching
$AV^{*\beta} = V^* - I$ and smooth pasting $\beta AV^{*\beta-1} = 1$ give $V^* = \frac{\beta}{\beta-1}I$. With $\mu = 0$,
$r = 4\%$ and $\sigma = 20\%$: $0.02\beta(\beta-1) = 0.04$, so $\beta = 2$ and $V^* = 2I$.

**4.** *Modigliani–Miller: show that $r_E = r_A + \frac{D}{E}(r_A - r_D)$ leaves the weighted average cost of capital
equal to $r_A$.*

*Solution.* The firm's assets are owned by its lenders and shareholders, so
$r_A = \frac{D}{D+E}r_D + \frac{E}{D+E}r_E$. Solving for $r_E$ gives the formula; the weighted average is $r_A$ by
construction, whatever $D/E$ is. With $r_A = 8\%$, $r_D = 4\%$ and $D = E$: $r_E = 12\%$.

**5.** *The discount factor: from $p = \mathbb{E}[mx]$, derive $R_f = 1/\mathbb{E}[m]$ and
$\mathbb{E}[R] - R_f = -R_f\operatorname{cov}(m, R)$.*

*Solution.* A safe bond pays $R_f$ for a price of 1: $1 = \mathbb{E}[m]R_f$. For any return $R = x/p$,
$1 = \mathbb{E}[mR] = \mathbb{E}[m]\mathbb{E}[R] + \operatorname{cov}(m, R)$; divide by $\mathbb{E}[m] = 1/R_f$:
$\mathbb{E}[R] = R_f - R_f\operatorname{cov}(m, R)$. On the Island, $m$ is 0.8 or 1.2, so $R_f = 1$; the tree returns
2.5 or 0, so $\operatorname{cov}(m,R) = -0.25$ and $\mathbb{E}[R] - R_f = 0.25$.

**6.** *Hansen–Jagannathan: from the last result and $|\operatorname{corr}| \le 1$, derive
$\sigma(m)/\mathbb{E}(m) \ge |\mathbb{E}[R - R_f]|/\sigma(R - R_f)$.*

*Solution.* For an excess return $Z = R - R_f$ (a payoff with price zero), $0 = \mathbb{E}[mZ] = \mathbb{E}[m]\mathbb{E}[Z]
+ \rho\,\sigma(m)\sigma(Z)$, so $|\mathbb{E}[Z]|/\sigma(Z) = |\rho|\sigma(m)/\mathbb{E}[m] \le \sigma(m)/\mathbb{E}[m]$.
With Shiller's stocks, the right side is 0.30, and power utility gives $\sigma(m)/\mathbb{E}(m) \approx \gamma\sigma_c$,
so $\gamma \ge 0.30/0.036 \approx 8$.

**7.** *Rational bubbles: show that $b_t = \mathbb{E}_t[m_{t+1}b_{t+1}]$ rules out a bubble on an asset with a final
date $T$.*

*Solution.* After the final payment the asset is worth nothing, so $b_T = 0$. Then
$b_{T-1} = \mathbb{E}_{T-1}[m_Tb_T] = 0$, and by induction $b_t = 0$ for every $t$. A bubble needs an infinite horizon,
and a bubble that grows at the rate of interest can last only if it does not outgrow the economy: $r < g$.

**8.** ★ *Disasters: with growth $e^{g + \sigma z}(1-b)^{\mathbb{1}[\text{disaster}]}$ and probability $p$, derive
$R_f$ and the price of a claim to consumption under power utility.*

*Solution.* $\mathbb{E}[G^{k}] = e^{kg + k^2\sigma^2/2}\big(1 - p + p\,\mathbb{E}[(1-b)^{k}]\big)$. Then
$R_f = 1/(\beta\mathbb{E}[G^{-\gamma}])$, and the claim's price-dividend ratio $w$ solves
$w = \beta\mathbb{E}[G^{1-\gamma}](1 + w)$, so $w = x/(1-x)$ with $x = \beta\mathbb{E}[G^{1-\gamma}] < 1$, and its expected
return is $\mathbb{E}[G](1+w)/w$. Disasters raise $\mathbb{E}[G^{-\gamma}]$ sharply, because $(1-b)^{-\gamma}$ is large:
the safe rate falls and the premium rises. On the Island, $\gamma = 3.5$ gives 5.1% and 2.3%.

## Lab and interactive

- `python -m videos.economics.labs 23`: price the Island's trees, solve Mehra and Prescott's economy, compute the
  Hansen–Jagannathan bound on Shiller's data, and add disasters.
- The interactive (course site): a tree economy where the reader sets risk aversion, patience and the chance of a
  disaster, and sees the premium and the safe rate against the record.

## Sources

Mehra and Prescott's moments are transcribed in `tables.MEHRA_PRESCOTT_1985`; the studies the films state are listed
with what each shows in `dials.SHOWN[23]`, and the user-cost and risk-aversion estimates are in the dials
(`explainer/economics/dials.py`). Shiller's data were retrieved on 2026-11-20 (they end in 2012–2016 by series);
FRED's housing series on the same day.
