# Economics, Built: Part 52, Many Agents

Part 52 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second of Act X, *The Graduate Core*. It asks what macroeconomics gets wrong by
treating a country as one household. Its answer: whatever depends on who holds what. How much a nation saves and the
interest rate it needs (households who cannot insure their risks save more, and push the rate below the rate of time
preference); the top of the wealth distribution, which needs more than bad luck to explain; how a rate cut reaches
spending, mostly through incomes when liquid wealth is scarce; how large a deficit-financed multiplier is; and who
gains from inflation. For the path of capital, one household is nearly enough, as Krusell and Smith found; for
spending, which is done disproportionately by those with little, it is not.

It opens on Alan Kirman's 1992 essay asking whom or what the representative individual represents (his answer: the
device deserves "a decent burial"), on Per Krusell and Anthony Smith's 1998 finding that their economy's aggregates
"can be almost perfectly described using only the mean of the wealth distribution", and on Kaplan, Moll and
Violante's 2018 reversal of the textbook account of monetary policy. From there it covers:

- aggregation: three households with straight Engel curves, where a transfer changes nothing when the slopes are equal
  and raises spending by 12 when they are not; Gorman's condition; the share of a windfall spent falling with wealth
  in Aiyagari's economy (76% for a household with nothing and the lowest wage, 6.9% on average, against 4% for a
  representative household);
- incomplete markets after Bewley and Huggett: the Euler inequality, why wealth drifts up without bound when
  beta(1 + r) = 1 (Chamberlain and Wilson), and Huggett's bond market clearing at 3.19% against a rate of time
  preference of 5%, with a crowd of low-income households at the borrowing limit;
- Aiyagari's economy derived and solved: the household's rules by the endogenous grid method, the capital market's
  two curves crossing at 2.12% against 4.17%, with 33% more capital than a representative household would hold and a
  saving rate of 28%;
- the Island's 100,000 households simulated for four centuries, whose Gini (0.481), top 1% share (4.7%) and share at
  the limit (1.6%) match Young's histogram method; Aiyagari's table recomputed (every rate below 4.17%, down to
  0.72% with persistence 0.9, a spread of 0.4 and risk aversion 5);
- Play it: a quarter-point cut in the real rate, fading over a year; which fifth of households by wealth raises its
  spending most? The second fifth (1.18%); the poorest raise theirs by 0.95%, almost all of it through incomes
  (0.04% directly); the richest by 0.76%, mostly through the rate;
- the wealth distribution: the top 1% hold 32.5% of US household wealth in the Federal Reserve's distributional
  accounts (2026 Q2) and the top tenth 68.9%, a Pareto exponent of 1.48; Aiyagari's economy gives 4.7%; three
  degrees of patience, 6.9%; a business state in which 9% of households earn 6 or 8 points more on their wealth,
  7.5% and 23.4% (exponents 2.9 and 1.49), at the same prices;
- Krusell and Smith in the calibration of the 2010 comparison project: 30 rounds of guess, solve, simulate and
  regress; R-squared of 0.99998 in both states; the rule alone, run on the shocks for 1,000 quarters, never more than
  0.59% from the economy; why: the richer half own 74% of the capital and save in nearly straight lines;
- an intermission film of the top 1%'s and the poorer half's shares of US wealth, 1989-2026 (22.8% to 32.5%; 3.5%
  to a low of 0.4% in 2010 and 2.3% now), as lines and a tune;
- continuous time after Achdou, Han, Lasry, Lions and Moll: the HJB and Kolmogorov forward equations, one sparse
  matrix (1,000 unknowns, at most 3,996 non-zeros) and its transpose; one household problem in about 12 milliseconds,
  Huggett's market in 0.2 seconds;
- HANK: the rate cut split into its direct and indirect effects; in the Island's economy (liquid wealth of four
  quarters of output, a quarterly MPC of 22%) 62% of the first quarter's rise and 45% of the first year's is direct,
  against 96% and 94% for a representative household; totals within about a tenth of each other (Werning), the split
  moving with liquidity (47% direct with one quarter of liquid wealth); why one asset cannot match both wealth and
  MPCs (Kaplan and Violante's wealthy hand-to-mouth);
- sequence-space Jacobians: the matrix of intertemporal MPCs, the fake-news algorithm of Auclert, Bardóczy, Rognlie
  and Straub (all 600 columns in under a second against about a minute by brute force, agreeing to 10^-5);
- policy: a balanced-budget multiplier of exactly one whatever the households, a deficit-financed one from 1.04 to
  1.88 as liquid wealth falls from sixteen quarters to one; forward guidance (a promised cut five years out does 14%
  less today than one next quarter with one quarter of liquid wealth, 10% with sixteen, and no less for one
  household); who gains from a surprise 5% inflation (a young family with a 180,000 mortgage gains 8,571, a retired
  teacher with 250,000 in bonds loses 11,905), and Doepke and Schneider's measurement;
- firms: Hopenhayn's industry (6.6% of firms entering and leaving each year; up or out), doubling the entry cost
  (entry to 2.1%, the exit threshold from 0.75 to 0.56, average productivity 7% lower, the price 8% higher), and a
  sketch of lumpy plant investment that vanishes in the sum (73% of plant-years with none), after Khan and Thomas;
- the Dials: the MPC out of a windfall (10 to 40% within a quarter in the studies) against the models' (0.5% for a
  representative household, 6.5% to 49% for the economies of this part, by liquidity);
- in practice (the Fed's distributional accounts, HANK models at central banks, open-source toolkits) and *Called
  it?* on Krusell and Smith's approximate aggregation (partly right); a frontier of intertemporal MPCs as targets
  (Fagereng, Holm and Natvik's lottery winners) and the open problems.

## Build it

```bash
python -m videos.economics.econ52.compute              # every number (about five minutes), into .cache/econ52/
python tools/qa_scene.py econ52 Aiyagari               # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ52 -q l   # the whole part, silent preview
python tools/build.py econ52                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 52                     # the lab
```

Times quoted in the film are measured when the cache is built, so they differ from machine to machine; the ratios
between methods are what the film relies on. The only data are the Federal Reserve's Distributional Financial
Accounts (shares of the top 1%, the next 9% and the bottom half, via FRED), registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | A decent burial, and a reprieve | Kirman; Krusell and Smith; Kaplan, Moll and Violante; the question; objectives |
| 1 | Aggregation: when one household is exact | Three households; Gorman's condition; MPCs that fall with wealth |
| 2 | Incomplete markets | The setting; the Euler inequality; Huggett's market; the distribution |
| 3 | The Aiyagari economy | The model; the household's rules; the capital market |
| 4 | The Island's 100,000 households | Five lives; the crowd against the histogram; Aiyagari's table recomputed |
| 5 | Play it: rates fall | Which fifth spends most; direct and indirect by fifth |
| 6 | The wealth distribution | The gap at the top; why; patience and returns; Pareto tails |
| 7 | Aggregate shocks: Krusell and Smith | The problem; the algorithm; the fit and Den Haan's test; why it works |
| — | Intermission | The top 1%'s and the poorer half's shares of wealth, 1989-2026; the story so far |
| 8 | Continuous time: two equations, one matrix | HJB and Kolmogorov; the sparse matrix and its transpose; timings |
| 9 | HANK: monetary policy with many households | Direct and indirect; against one household; liquidity |
| 10 | Sequence-space Jacobians | Paths in, paths out; the matrix; fake news; against brute force |
| 11 | What changes for policy | Multipliers; forward guidance; who gains from inflation |
| 12 | Many firms: entry, exit and lumps | Hopenhayn's industry; cohorts; an entry barrier; lumpy plants |
| 13 | The Dials: the propensity to spend | The MPC dial; the models' MPCs |
| 14 | In practice: distributions at the central bank | Who uses the models; a distributional analysis; *Called it?* (partly right) |
| 15 | Frontier: micro data in macro models | Intertemporal MPCs as targets; open questions |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 53, *Information and Persuasion* |

## What is computed, and from what

Everything plotted is computed by `compute.py` with Agora's many agents (`explainer.economics.agora.hetero`), the
continuous-time household of Agora's solver (`agora.solve`) and the Island's Part 52 truths; the narration states the
cached numbers.

- **Aiyagari's economy.** Annual periods; u = c^(1-gamma)/(1-gamma) with gamma = 3, beta = 0.96; log wage draws a
  seven-state Rouwenhorst chain with persistence 0.9 and unconditional s.d. 0.4, normalized to mean one; no
  borrowing; 300 asset points up to 250, crowded near zero; output K^0.36 with labour 1 and depreciation 8%. The
  household by the endogenous grid method, the distribution by Young's (2010) lottery, the interest rate by
  bisection on the capital market. MPCs out of a windfall of 5% of the wage, arriving as cash.
- **The Island.** 100,000 households from equal wealth for 400 years with seed 52, following the equilibrium rules.
- **The table.** Spreads 0.2 and 0.4, persistence 0 to 0.9, risk aversion 1, 3 and 5, as in Aiyagari's Table II;
  each cell a full equilibrium.
- **The top.** Three permanent types with beta 0.94, 0.96 and 0.98, a common interest rate; a business state entered
  with probability 2% a year and left with 20%, earning 6 or 8 points more, at the base economy's interest rate and
  wage (not re-cleared), on 600 points up to 20,000. Pareto exponents from the top 1% and 10% shares,
  S(p) = p^(1 - 1/alpha), for the data and the models alike.
- **Huggett.** Incomes 0.1 and 0.2 switching at rate 1.2, rho = 0.05, gamma = 2, borrowing to -0.15, 500 points; the
  rate that makes bonds sum to zero, by bisection.
- **Krusell and Smith.** The calibration of Den Haan, Judd and Juillard (2010): beta = 0.99, log utility, alpha =
  0.36, quarterly depreciation 2.5%, productivity 0.99 or 1.01, unemployment 10% or 4%, unemployment benefits of 15%
  of the wage financed by a tax on the employed, labour endowment 1/0.9; Krusell and Smith's transition matrices
  (eight-quarter spells, unemployment spells of 2.5 and 1.5 quarters); 100 asset points and six values of capital;
  1,100 quarters (the first 100 dropped) with the distribution moved by Young's method; the rule updated with
  damping 0.3 until it changes by less than 10^-6.
- **HANK.** Quarterly; output 1; the real rate 0.5%; government bonds of 1 to 16 quarters of output are all the
  households hold; taxes r B; log income a seven-state chain with persistence 0.966 and s.d. 0.5; log utility; the
  discount factor set to clear the bond market. Jacobians over 300 quarters by the fake-news algorithm with a step of
  10^-4. The rate cut: -0.25 points from quarter 1, decaying by 30% a quarter; debt constant (taxes fall by B dr);
  after-tax income from asset-market clearing. Spending by fifth from the date-0 rules on the equilibrium paths.
  Government purchases of 1% of output decaying by 20% a quarter; deficit-financed with taxes of 10% of last
  quarter's debt. The representative household's responses in closed form.
- **Firms.** Productivity a 41-state Rouwenhorst chain (persistence 0.9, innovation s.d. 0.2); output phi n^0.64;
  fixed cost 15; beta = 0.95; entrants drawn half a standard deviation below incumbents; entry costs 40 and 80;
  expenditure 100. Plants: 20,000, depreciation 10%, adjusting when the log gap exceeds 0.3, a common shock of 10% at
  year 80.

## Problems and solutions

**1.** *Gorman: three households spend c_i = 5 + b_i m_i with b = (0.9, 0.6, 0.3). A transfer of 10 goes from the
third to the first. By how much does total spending change? With equal slopes?*

*Solution.* The first spends 0.9 x 10 = 9 more, the third 0.3 x 10 = 3 less: total spending rises by 6. With equal
slopes b the two changes are b x 10 and -b x 10, and total spending does not move: that is Gorman's condition.

**2.** *The supermartingale: with beta(1 + r) = 1 and income risk, show that u'(c_t) is a nonnegative
supermartingale, and explain why consumption cannot settle down.*

*Solution.* The Euler inequality u'(c_t) >= beta(1 + r) E_t u'(c_{t+1}) becomes u'(c_t) >= E_t u'(c_{t+1}), the
definition of a supermartingale, and marginal utility is positive. By the martingale convergence theorem it converges
almost surely. If it converged to a positive number, consumption would settle at a finite level, but a household
with finite wealth and random income cannot keep consumption constant: a run of bad draws would force it to change.
So marginal utility must go to zero: consumption, and wealth, grow without bound. At that interest rate everyone
wants to save, so the market can only clear at a lower rate.

**3.** *Aiyagari's market: with alpha = 0.36 and delta = 0.08, find capital per worker at r = 4.17% and at r =
2.12%. By what percentage does capital rise?*

*Solution.* From r = alpha K^(alpha - 1) - delta, K = (alpha/(r + delta))^(1/(1 - alpha)). At 4.17%:
(0.36/0.1217)^1.5625 = 5.45. At 2.12%: (0.36/0.1012)^1.5625 = 7.26. Capital is 33% higher: the precautionary
saving of households who cannot insure their wages.

**4.** *Huggett: explain why bonds held must sum to zero, and why the interest rate that clears the market falls as
the borrowing limit tightens.*

*Solution.* The bonds are IOUs among households: every bond one holds is another's debt, so in total they sum to zero.
A tighter limit means borrowers can absorb fewer bonds, while savers still want a buffer; to clear the market the
interest rate must fall until savers want to hold fewer. In the limit of no borrowing at all, nobody can hold a bond,
and the rate falls until no household wants to save.

**5.** *Krusell and Smith: a rule log K' = 0.13 + 0.964 log K. Find its fixed point. What does R-squared miss that
Den Haan's test catches?*

*Solution.* log K = 0.13/(1 - 0.964) = 3.61, so K = 37.0. R-squared measures one-step-ahead fit when the true capital
is fed in every quarter, so small, persistent biases never accumulate. Den Haan's test feeds the rule only the shocks
and lets it use its own forecasts; a rule that is slightly off in a consistent direction drifts away from the
economy, and the test shows how far (0.59% at most in the film).

**6.** *Werning's benchmark: with debt fixed and output set by demand, show that a balanced-budget increase in
purchases raises output one for one, whatever the MPCs.*

*Solution.* With the real rate fixed, spending responds only to after-tax income: dC = M dZ, with dZ = dY - dT.
Balanced budget means dT = dG, and the goods market says dY = dC + dG. Try dY = dG: then dZ = 0, so dC = 0, and
dY = dG holds. As long as I - M is invertible this is the only solution, whatever the matrix of MPCs M. (The film
attributes the general framework to Auclert, Rognlie and Straub.)

**7.** *Fake news: show that J_{t,s} = F_{t,s} + J_{t-1,s-1} when the economy is the same at every date.*

*Solution.* J_{t,s} is the effect on C_t of a change in the input at s, announced at 0. Split it into the part that
works through date-0 decisions and the date-1 distribution they produce (the fake-news entry F_{t,s}) and the rest,
which works through decisions from date 1 on. From date 1, the economy faces news about an input s - 1 periods ahead
and is asked about an outcome t - 1 periods ahead: because the economy is the same at every date, that is exactly
J_{t-1,s-1}.

**8.** *Hopenhayn: derive the stationary mass of firms mu = M (I - P' X)^(-1) nu, and show that a higher entry cost
lowers the exit threshold.*

*Solution.* Next year's firms are this year's stayers, moved by the productivity chain, plus the entrants:
mu' = P' X mu + M nu, with X the diagonal matrix of decisions to stay. In a steady state mu' = mu, so
mu = M (I - P' X)^(-1) nu. Free entry says the expected value of entering equals c_e; a higher c_e therefore needs a
higher value of being in the industry, which needs a higher price. A higher price raises every firm's profits, so a
less productive firm now finds staying worth its fixed cost: the threshold falls, from 0.75 to 0.56 in the film.

## Lab and interactive

- `python -m videos.economics.labs 52`: Gorman's transfer; Aiyagari's equilibrium and its supply curve; Huggett's
  market; the wealth shares by model; a small Krusell and Smith; the fake-news Jacobians against brute force; the rate
  cut split by fifth; multipliers; Hopenhayn at two entry costs.
- The interactive (course site): households. The reader sets how much liquid wealth households hold and how the
  government pays, and watches a rate cut split into direct and indirect effects and the multiplier change.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[52]`; the MPC dial is in
`explainer/economics/dials.py`; Krusell and Smith's finding is a *Called it?* entry (`explainer/economics/calls.py`);
the wealth shares are in the Data Room. Checked on 2026-11-21: Kirman's essay (JEP 6(2), 1992) and its "decent
burial"; Krusell and Smith's abstract (JPE 106(5), 1998: "almost perfectly described using only the mean of the
wealth distribution"); Kaplan, Moll and Violante (AER 108(3), 2018: direct effects small, indirect effects dominant);
Doepke and Schneider (JPE 114(6), 2006: rich, old households lose; young, middle-class households with fixed-rate
mortgages and the government gain); Fagereng, Holm and Natvik (AEJ: Macroeconomics 13(4), 2021: low-liquidity
winners of small prizes spend all within the year; spending reverts within five years). The models are stated from
the papers cited in the chapters (Gorman 1953, Bewley 1977, Hopenhayn 1992, Huggett 1993, Aiyagari 1994, Chamberlain
and Wilson 2000, Khan and Thomas 2008, Den Haan 2010, Young 2010, Benhabib, Bisin and Zhu 2011 and 2015, Kaplan and
Violante 2014, Werning 2015, McKay, Nakamura and Steinsson 2016, Auclert et al. 2021, Achdou et al. 2022) and computed
here. Not stated, because not checked: Krusell and Smith's own R-squared and rule coefficients; Aiyagari's own table
entries; Kaplan, Moll and Violante's exact direct share.
