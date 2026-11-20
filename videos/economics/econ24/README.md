# Economics, Built: Part 24, Looking for Work

Part 24 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the last of Act V, *The Long Run*. It asks why there are unemployed workers and unfilled
jobs at the same time, and answers: because finding each other takes time. Workers and firms meet through a matching
process with roughly constant returns; firms open vacancies until hiring costs what a worker is worth; wages split each
match's surplus. Together these fix the market's tightness, and the flows fix unemployment and vacancies, both positive
in a steady state. But with ordinary numbers the model's unemployment barely moves in a recession, while the real one
moves more than ten times as much.

It opens with Peter Diamond's coconut island (1982), where a taboo forbids eating the coconuts you pick, so climbing a
palm pays only if others climb too; the island has three equilibria (nobody climbs, 58% climb, unstable, and almost
everyone), and a slump or a boom with the same people and the same trees. From there it covers:

- stocks and flows: JOLTS since December 2000, about 5.0 million hires and 4.9 million separations a month before 2020
  (2.6 million quits), a net change of 84 thousand, and 11.5 million separations in April 2020; the bathtub and
  $u^* = s/(s+f)$;
- a game: offers between 50 and 150 arrive one a month, with a benefit of 40 while looking and patience 0.95; four
  stopping rules (80, 100, 120, 140) against the best, a reservation wage of 120.9;
- search (Stigler 1961; McCall 1970): the reservation wage derived and drawn; its response to the benefit and to
  patience; the evidence on benefits and spells (Katz and Meyer 1990; Card, Chetty and Weber 2007);
- the Beveridge curve from JOLTS by period, its outward shift after 2009, two openings per searcher in March 2022, and
  the 2022 soft-landing debate (Blanchard, Domash and Summers; Figura and Waller); the model's curve and its shift;
- the matching function: urns and balls (Butters 1977; Hall 1979), animated; constant returns; estimated on the CPS
  job-finding rate against JOLTS openings ($\eta \approx 0.58$, 2001–2019);
- the Diamond–Mortensen–Pissarides model derived: job creation, the wage curve, tightness, the model's Beveridge
  curve, and the path after a 3% fall in productivity;
- Nash bargaining and the wage $w = (1-\beta)b + \beta(p + c\theta)$; comparative statics of benefits, productivity,
  separations and bargaining power;
- efficiency: congestion and the Hosios condition (1990), computed; coordination failure on Diamond's island;
- an intermission without narration: the American Beveridge curve month by month, 2000–2026, with openings per
  unemployed worker as a tune;
- the volatility puzzle (Shimer 2005): tightness about 25 times as volatile as productivity in 2001–2019, against 1.7
  in the calibrated model; *Called it?* on Mortensen and Pissarides's 1994 claim (partly right); the repairs (Hall
  2005; Hall and Milgrom 2008; Hagedorn and Manovskii 2008; Pissarides 2009) and the fundamental surplus (Ljungqvist
  and Sargent 2017);
- ins against outs: Shimer's job-finding and separation rates since 1948, computed from the CPS; job finding accounts
  for about 72% of unemployment's swings (Shimer 2012; Elsby, Michaels and Solon 2009);
- job ladders: careers (Topel and Ward 1992), Burdett and Mortensen's equilibrium wage dispersion (1998), and
  monopsony from frictions (Manning 2003);
- the natural rate (CBO's estimate, 6.2% in 1979, 4.4% in 2025), long-term unemployment (46% in 2010), duration
  dependence (Kroft, Lange and Notowidigdo 2013) and the cost of job loss (Davis and von Wachter 2011);
- two dials (the matching elasticity, new; the worker's bargaining share, new), labour-market desks and job platforms
  in practice (Horton 2017; Belot, Kircher and Muller 2019), and a frontier chapter on online vacancies (Hershbein and
  Kahn 2018), the geography of search (Marinescu and Rathelot 2018) and remote work (Hansen et al. 2023).

## Build it

```bash
python -m videos.economics.econ24.compute              # every number (seconds), into .cache/econ24/
python tools/qa_scene.py econ24 DMP                    # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ24 -q l   # the whole part, silent preview
python tools/build.py econ24                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 24                     # the lab
```

The data are in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): from FRED, the BLS's JOLTS (openings, hires, total
separations, quits), the Current Population Survey (the unemployed, the unemployed for under five weeks and for 27
weeks and more, the labour force, the unemployment rate), output per hour in the nonfarm business sector, and the
CBO's noncyclical rate of unemployment.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Why are there unemployed workers and unfilled jobs at the same time? | Diamond's coconut island: equilibria at 0, 0.58 (unstable) and 1.00; the latest JOLTS openings against the unemployed; the 2010 Nobel prize; objectives |
| 1 | Stocks and flows | JOLTS hires and separations, 2001–2026: 4.97 and 4.89 million a month before 2020, 2.63 million quits, a net 84 thousand; 11.5 million separations in April 2020; the tub; $u^* = s/(s+f) \approx 5.4\%$ on the CPS averages; Davis and Haltiwanger's gross flows |
| 2 | Play it: take it or keep looking? | Ten offers (88, 71, 104, 63, 97, 121, 79, 135, 92, 110); rule A takes 88, B 104, C 121 in month 6, D is still looking; their values as wages for ever: 109.8, 116.9, 120.8 and 109.0, against the best rule's 120.9 |
| 3 | Search: the reservation wage | Stigler and McCall; $W = w/(1-\beta)$, $U = b + \beta\mathbb{E}\max(W, U)$; $w^* - b = \frac{\beta}{1-\beta}\int_{w^*}(w-w^*)dF$, drawn: 120.9, 29% of offers accepted, 3.4 months; $b$ from 0 to 120 moves $w^*$ from 115 to 137 and search from 2.9 to 7.5 months; Katz and Meyer (0.16–0.20 weeks per week of benefits); Card, Chetty and Weber |
| 4 | The Beveridge curve | JOLTS openings rate against the unemployment rate in four periods; the model's curve with productivity from 0.8 to 1.2 and its shift when matching is 20% less efficient; 1.96 openings per unemployed worker in March 2022; the soft-landing debate; the fact card |
| 5 | The matching function | Twelve applicants, twelve openings, eight hires; $V(1 - e^{-U/V})$; $M = AU^\eta V^{1-\eta}$, $f = A\theta^{1-\eta}$, $q = A\theta^{-\eta}$; 76 quarters: slope 0.42, $\eta \approx 0.58$; JOLTS hires give 0.69, since they include job-to-job moves; Petrongolo and Pissarides's 0.5–0.7 |
| 6 | The Diamond–Mortensen–Pissarides model | The values of a vacancy and a job; free entry; job creation and the wage curve crossing at $\theta^* = 1.85$, $w^* = 0.977$; $u = 3.5\%$, $v = 6.6\%$, $f = 82\%$ a month; a 3% fall in productivity: $\theta$ jumps to 1.75, unemployment rises from 3.55% to 3.64% with a half-life of 0.8 months |
| 7 | Nash bargaining and the split of the surplus | The surplus and Nash's solution; $w = (1-\beta)b + \beta(p + c\theta)$; the equation for $\theta$; unemployment with a higher benefit 3.9%, 5% higher productivity 3.4%, 50% more separations 5.3%, a larger worker share 4.3%; the shifted wage curve |
| 8 | Efficiency: the Hosios condition | Congestion both ways; net output $(1-u)p + ub - cv$ against $\beta$, highest at 0.50 $= \eta$; Diamond's increasing returns and coordination failure (Cooper and John 1988) |
| — | Intermission | The Beveridge curve month by month, December 2000 to the latest month, with openings per unemployed worker as a tune; the story so far |
| 9 | The volatility puzzle | HP-filtered log tightness against output per hour, 2001–2019: s.d. 0.39 against 0.016, a ratio of about 25 (Shimer's 1951–2003: 0.382 against 0.020); the model's elasticity 1.7 with Shimer's calibration and 34 with Hagedorn and Manovskii's; *Called it?* (partly right); the repairs; $\frac{d\ln\theta}{d\ln p} = \frac{r+s+\beta f}{\eta(r+s)+\beta f}\cdot\frac{p}{p-b}$ |
| 10 | Ins against outs | Shimer's method from unemployment by duration, with the 1994 correction; job finding averages 55% a month, separation 3.2%; the steady state and its two counterfactuals; job finding 72% of the variance since 1948 (74% since 1987), separation 28% |
| 11 | Job ladders and wage dispersion | Topel and Ward's seven jobs in ten years; a simulated career; Burdett and Mortensen's offer and earnings distributions (offers from 0.40 to 0.98, mean 0.76; earnings mean 0.90); monopsony from frictions |
| 12 | The natural rate, duration and scarring | CBO's natural rate against unemployment since 1949 (6.2% in 1979, 4.4% in 2025); the long-term share, 46% in 2010; callbacks falling from about 7% to 4% with a spell's length; 1.4 against 2.8 years of earnings lost |
| 13 | The Dials | The matching elasticity (settled within a range: 0.5–0.7, Shimer's 0.72, this film's 0.58 and 0.31); the worker's bargaining share (contested: 0.72, 0.052, and none for low- and intermediate-skill French workers) |
| 14 | In practice: labour-market desks, job platforms | The latest month's dashboard; quits and tightness; Horton's recommendations (fill rate up about 20%); Belot, Kircher and Muller's search advice; who uses this |
| 15 | Frontier | Hershbein and Kahn's upskilling in vacancy postings; Marinescu and Rathelot's 35% fall in applications ten miles away and 5.3% gain from relocation; remote-work postings more than tripled in the US (Hansen et al.); four open questions |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 25, *Money* |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's labour market with frictions
(`explainer.economics.agora.search`) with the Island's Part 24 truths, or from the Data Room; the narration states the
cached numbers.

- **Diamond's island.** Climbing costs spread logistically around 0.6; an islander climbs if the cost is below
  $0.9 \times 1.2 \times e$, where $e$ is the share expected to climb; equilibria are the fixed points.
- **The game.** Offers uniform on $[50, 150]$ (1,001 points), $b = 40$, $\beta = 0.95$; a rule's value before the draw is
  $(b + \beta P\,\mathbb{E}[w\,|\,w \ge R]/(1-\beta))/(1 - \beta(1-P))$, shown times $1-\beta$.
- **The DMP Island.** Monthly: $p = 1$, $b = 0.4$, $\beta = \eta = 0.5$, $A = 0.6$, $s = 0.03$, $r = 0.004$, $c = 0.3$;
  $\theta$ by bisection on $(r+s)c/q(\theta) + \beta c\theta = (1-\beta)(p-b)$.
- **The calibrations.** Quarterly, $s = 0.10$, $r = 0.012$, $f = 1.355$ at $\theta = 1$ (the vacancy cost chosen so):
  Shimer's $b = 0.4$, $\beta = \eta = 0.72$; Hagedorn and Manovskii's $b = 0.955$, $\beta = 0.052$ (with $\eta = 0.45$
  here). The elasticity by central differences.
- **The data's volatility.** Quarterly means of JOLTS openings over CPS unemployment and of output per hour,
  2001–2019, in logs, minus an HP trend with $\lambda = 10^5$.
- **Flows.** $F = 1 - (u_{t+1} - u^s_{t+1})/u_t$, $f = -\ln(1-F)$, $s$ solving the continuous-time stock equation; short-term
  unemployment scaled by 1.1 from February 1994; quarterly means; the decomposition is Shimer's covariance shares of
  the HP-detrended log steady state.
- **The ladder.** Offers at rate 0.1 a month, separations at 0.02, $b = 0.4$, $p = 1$:
  $F(w) = \frac{1+k}{k}\big(1 - \sqrt{(p-w)/(p-b)}\big)$, $G = F/(1 + k(1-F))$, $k = 5$.

## Problems and solutions

**1.** *The tub: from $u_{t+1} = u_t + s(1-u_t) - fu_t$, derive $u^* = s/(s+f)$, and show that a gap from $u^*$ shrinks by
the factor $1 - s - f$ each month.*

*Solution.* In a steady state $u_{t+1} = u_t = u^*$, so $s(1-u^*) = fu^*$ and $u^* = s/(s+f)$. Subtracting the steady
state from the law of motion, $u_{t+1} - u^* = (1 - s - f)(u_t - u^*)$, so the gap shrinks geometrically. With
$s = 0.03$ and $f = 0.82$ (the Island) it falls by 85% a month; the continuous-time half-life is $\ln 2/(s+f) \approx 0.8$
months.

**2.** *McCall: derive $w^* - b = \frac{\beta}{1-\beta}\int_{w^*}(w - w^*)\,dF(w)$, and solve it when offers are uniform on
$[\ell, h]$.*

*Solution.* $W(w) = w/(1-\beta)$ and $U = b + \beta\mathbb{E}\max\{W(w'), U\}$. At the reservation wage $W(w^*) = U$, so
$U = w^*/(1-\beta)$. Then $\frac{w^*}{1-\beta} = b + \frac{\beta}{1-\beta}\mathbb{E}\max\{w', w^*\}$; subtract
$\frac{\beta w^*}{1-\beta}$ from both sides: $w^* = b + \frac{\beta}{1-\beta}\mathbb{E}[(w' - w^*)^+]$. For a uniform,
$\mathbb{E}[(w'-w^*)^+] = (h - w^*)^2/(2(h-\ell))$, so $w^* - b = \frac{\beta}{1-\beta}\frac{(h-w^*)^2}{2(h-\ell)}$, a
quadratic. With $\ell = 50$, $h = 150$, $b = 40$, $\beta = 0.95$: $w^* - 40 = 0.095(150 - w^*)^2$, whose root below 150 is
$w^* \approx 120.8$ (120.9 on the film's grid of 1,001 offers).

**3.** *Urns and balls: show that $U$ applicants choosing among $V$ openings at random fill $V\big(1-(1-\frac1V)^U\big)$ on
average, and that the limit $V(1 - e^{-U/V})$ has constant returns.*

*Solution.* A given opening receives no application with probability $(1 - 1/V)^U$, so the expected number with at least
one is $V(1 - (1-1/V)^U)$. As $U, V \to \infty$ with $U/V$ fixed, $(1 - 1/V)^U = \big((1-1/V)^V\big)^{U/V} \to
e^{-U/V}$. Then $M(\lambda U, \lambda V) = \lambda V(1 - e^{-U/V}) = \lambda M(U, V)$. With twelve and twelve,
$12(1 - (11/12)^{12}) \approx 7.8$.

**4.** *Matching: with $M = A U^\eta V^{1-\eta}$, find $f(\theta)$ and $q(\theta)$ and their elasticities with respect to
$\theta$.*

*Solution.* $f = M/U = A(V/U)^{1-\eta} = A\theta^{1-\eta}$, with elasticity $1-\eta$; $q = M/V = A\theta^{-\eta}$, with
elasticity $-\eta$; and $f = \theta q$. A regression of $\ln f$ on $\ln\theta$ estimates $1-\eta$: 0.42 on the American
quarters of 2001–2019, so $\eta \approx 0.58$.

**5.** *Job creation: from $r\mathcal{V} = -c + q(\theta)(\mathcal{J} - \mathcal{V})$, $r\mathcal{J} = p - w - s\mathcal{J}$
and free entry, derive $c/q(\theta) = (p - w)/(r + s)$.*

*Solution.* Free entry sets $\mathcal{V} = 0$, so $0 = -c + q(\theta)\mathcal{J}$, that is $\mathcal{J} = c/q(\theta)$. The
second equation gives $\mathcal{J} = (p - w)/(r + s)$. Equate them. The left side is the expected cost of filling a
vacancy (the cost per month times the expected $1/q$ months); the right is the present value of a filled job's profits.

**6.** *The wage: with $r\mathcal{W} = w + s(\mathcal{U} - \mathcal{W})$, $r\mathcal{U} = b + f(\theta)(\mathcal{W} -
\mathcal{U})$ and $\mathcal{W} - \mathcal{U} = \beta S$, derive $w = (1-\beta)b + \beta(p + c\theta)$.*

*Solution.* With $\mathcal{V} = 0$, $S = \mathcal{W} - \mathcal{U} + \mathcal{J}$, so the sharing rule is
$(1-\beta)(\mathcal{W} - \mathcal{U}) = \beta\mathcal{J}$. Subtracting the two value equations,
$(r + s)(\mathcal{W} - \mathcal{U}) = w - r\mathcal{U}$; and $(r + s)\mathcal{J} = p - w$. So
$(1-\beta)(w - r\mathcal{U}) = \beta(p - w)$, that is $w = r\mathcal{U} + \beta(p - r\mathcal{U})$. Finally
$r\mathcal{U} = b + f\frac{\beta}{1-\beta}\mathcal{J} = b + \frac{\beta}{1-\beta}\theta c$ (using $f\mathcal{J} =
\theta q\mathcal{J} = \theta c$), and substituting gives $w = (1-\beta)b + \beta(p + c\theta)$.

**7.** *Hosios: as $r \to 0$, show that $(1-u)p + ub - cv$ is maximized over $\theta$ where $\beta = \eta$.*

*Solution.* With $u = s/(s + f(\theta))$ and $v = \theta u$, net output is $p - u(\theta)(p - b + c\theta)$. The first-order
condition is $-u'(\theta)(p - b + c\theta) = u c$. Since $u' = -uf'/(s+f)$ and $f' = (1-\eta)f/\theta$, it becomes
$(1-\eta)\frac{f}{\theta(s+f)}(p - b + c\theta) = c$, or $\frac{(1-\eta)(p-b)}{c} = \frac{s}{q} + \eta\theta$ (multiply out
and use $f = \theta q$). The market's equation with $r = 0$ is $\frac{(1-\beta)(p-b)}{c} = \frac{s}{q} + \beta\theta$. The
two coincide for every parameter value exactly when $\beta = \eta$. On the Island net output peaks at $\beta = 0.50$.

**8.** *★ The fundamental surplus: from the equation for $\theta$, derive
$\frac{d\ln\theta}{d\ln p} = \frac{r + s + \beta f}{\eta(r+s) + \beta f}\cdot\frac{p}{p - b}$.*

*Solution.* Differentiate $(r+s)c/q(\theta) + \beta c\theta = (1-\beta)(p - b)$. Since $d(1/q)/d\theta = \eta/(\theta q)$,
the left side's derivative is $\frac{1}{\theta}\big(\eta(r+s)c/q + \beta c\theta\big)$, so
$\frac{d\theta}{\theta} = \frac{(1-\beta)\,dp}{\eta(r+s)c/q + \beta c\theta}$. Replace $(1-\beta)$ using the equation itself,
$(1-\beta) = \frac{(r+s)c/q + \beta c\theta}{p - b}$, and multiply through by $q/c$ (with $\theta q = f$):
$\frac{d\ln\theta}{d\ln p} = \frac{r + s + \beta f}{\eta(r+s) + \beta f}\cdot\frac{p}{p-b}$. The first factor lies between
1 and $1/\eta$; the second is one over Ljungqvist and Sargent's fundamental surplus fraction. With Shimer's numbers it
is about $1.03 \times 1.67 \approx 1.7$; with $b = 0.955$ the second factor alone is 22.

## Lab and interactive

- `python -m videos.economics.labs 24`: solve McCall's problem, measure the matching function and Shimer's flows on the
  American data, solve the DMP model and its comparative statics, check Hosios's condition, and reproduce the
  volatility puzzle.
- The interactive (course site): a labour market where the reader sets the benefit, the worker's share, separations
  and matching efficiency, and watches the two curves, the Beveridge curve and unemployment move; with a switch to the
  small-surplus calibration.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[24]`; the matching elasticity and the
bargaining share are dials (`explainer/economics/dials.py`), and Mortensen and Pissarides's 1994 claim is a
*Called it?* entry (`explainer/economics/calls.py`). FRED's labour-market series were retrieved on 2026-11-20 (JOLTS
to September 2026; the CPS to its latest month). Shimer's own series (1948–2003, with help-wanted data) are not
reproduced: this film recomputes the flows from the CPS and uses JOLTS for openings, so its volatility ratio is for
2001–2019.
