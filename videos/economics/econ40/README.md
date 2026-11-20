# Economics, Built: Part 40, Inequality and Mobility

Part 40 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third of Act VIII, *Work and the State*. It asks how unequal incomes and wealth
are, why, and whether children escape where they started. Its answer: very unequal at the top, and more so since 1980,
for income and still more for wealth; the long tails come from growth that compounds, and moved fast because a few
incomes grew fast; and children escape less where inequality is high, less than their grandparents did, and much less
in some places than in others.

It opens on Jan Pen's parade of 1971, drawn from data: American families raising children around 2000, one marcher per
percentile of parents' income in Opportunity Insights' tables, each as tall as their income with the mean at 1.7
metres. At minute six the marchers are 29 cm tall; the median family passes at half past, at 1.17 m; average height
arrives only at minute 42; then 2.8 m at minute 54, 8 m in the last minute and 27 m for the top percentile. In
Piketty and Saez's tax records for 2022, the richest 0.01% of tax units had 370 times the average income, about $28
million a year: 629 metres tall. From there it covers:

- a game: four guesses (the top 1% share of income, 19.6% in 2022, 23.6% with capital gains; the top 1% share of
  wealth, 32.5% in 2026; the chance of rising from the bottom fifth to the top fifth, 7.5%; children out-earning their
  parents, 92% for those born in 1940 and 50% for 1984);
- measuring inequality: the Island's 2,000 incomes with bootstrap standard errors (Gini 0.406, s.e. 0.012; top 1%
  share 9.4%, s.e. 1.0 point); the Census Bureau's Gini, 0.397 in 1967 and 0.490 in 2025; Atkinson's equally
  distributed equivalent at aversions 0 to 4 ($60,000 down to $12,212); two societies with the same Gini whose Lorenz
  curves cross, ranked one way by the top 10% share and by Atkinson's index at epsilon 0.5, the other way at 2;
- a century of top incomes (Piketty and Saez, updated to 2022): the top 10% share 46% in 1928, about a third from the
  war to 1980, 50% in 2022; the top 1% share 20%, 8%, 20%; the World Inequality Database's U in America and Britain,
  L in France, Sweden and Germany, and steep rises in China, India and Russia; the measurement dispute (Auten and
  Splinter against Piketty, Saez and Zucman: +10 points of fiscal income, +6 after taxes and transfers by one account,
  +2.6 pre-tax and +1.4 after taxes since 1979 by the other);
- Pareto tails: the top shares on log scales are straight lines, with an exponent of 2.4 in 1970 and 1.6 in 2022
  (from the top 1% and 0.1% shares, year by year since 1913: 1.61 in 1928, 2.63 in 1962, 1.56 in 2022); random growth
  with turnover (Champernowne; Gabaix) on the Island, five careers and then 50,000; the Kolmogorov forward equation, its
  stationary exponential solution and the quadratic for the exponent, zeta = 1.55, matched by the simulation (Hill's
  estimate 1.64; the top 1% share 20%); the Fact;
- why the tail moved so fast (Gabaix, Lasry, Lions and Moll): after a rise in volatility, pure random growth closes
  half the gap in the log top share in 57 years; with a few high-growth types, in 18;
- wealth: the Federal Reserve's shares since 1989 (top 1% 22.8% to 32.5%; bottom half 3.5% to 2.3%), the exponent they
  imply (1.74 to 1.48; the Forbes 400, 1.49), r against g on the Island (the exponent 3.2 at r = g, 1.8 at two points,
  1.3 at three), and the replies to Piketty (housing, depreciation, the elasticity of substitution);
- an intermission without narration: the top 1% share, 1913-2022, as a tune;
- Kuznets's curve: the dual economy (the Gini 0.22 with everyone on the land, 0.44 at the peak, 0.38 with everyone in
  the cities), his own description of the evidence, the downslope he saw and the upslope that followed; *Called it?*
  (partly right);
- the intergenerational elasticity: one year of parents' income estimates 0.24 when the truth is 0.45; averaging 3, 5,
  10 and 15 years gives 0.35, 0.38, 0.41 and 0.42, as the attenuation formula predicts (Solon; Mazumder); the Gatsby
  curve's mechanism (economies differing only in the return to inherited skill) and its American version across 709
  commuting zones (upward mobility against the Gini of the bottom 99%, correlation -0.42); the Fact;
- forty million tax records (Chetty, Hendren, Kline and Saez): the rank-rank slope 0.341; the transition matrix by
  fifths (7.5% from the bottom to the top, 33.7% staying at the bottom, 36.5% staying at the top); absolute mobility
  by birth year and parents' percentile; why it fell (62% with the old growth rates, 80% with the old sharing);
- places: upward mobility across commuting zones (37 at the tenth percentile of places, 52 at the ninetieth); the
  extremes among the fifty largest (Charlotte 4.4%, San Jose 12.9%); twelve correlates; movers (about 4% a year of
  exposure) and Moving to Opportunity (+$3,477, 31%, for children who moved before 13);
- the world: the Gini between 158 countries' GDP per person, weighted by population, 0.64 in 1980 and 0.47 in 2023,
  almost all of the fall due to China and India; the elephant curve (Lakner and Milanovic); the world's top 1% share;
- does inequality matter: life expectancy at 40 for the richest and poorest 1% (14.6 years apart for men, 10.1 for
  women); what can and cannot be identified;
- redistribution and pre-distribution, with a flat tax and equal transfer on the Island (Gini 0.41 to 0.32);
- two dials, both new (the intergenerational elasticity; the Pareto exponent of top wealth); a distributional table
  and the four choices behind every one; a frontier chapter on distributional national accounts, Denmark's wealth
  taxes, and Swedish adoptees' wealth.

## Build it

```bash
python -m videos.economics.econ40.compute              # every number (about ten seconds), into .cache/econ40/
python tools/qa_scene.py econ40 Pareto                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ40 -q l   # the whole part, silent preview
python tools/build.py econ40                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 40                     # the lab
```

The data are in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): Piketty and Saez's top shares (Saez's TabFig2022.xlsx,
Tables A0, A1 and A3); Opportunity Insights' tables (by parent percentile, with the child's quintile summed from the
100 x 100 transition matrix; absolute mobility by cohort and percentile; Online Data Tables V and VIII by commuting
zone); the World Inequality Database's top 1% shares via Our World in Data (CC BY 4.0); from FRED, the Federal
Reserve's Distributional Financial Accounts and the Census Bureau's Gini; the Penn World Table; and tables from Pen,
Atkinson, Auten and Splinter, Pareto, Champernowne and Gabaix, Gabaix, Lasry, Lions and Moll, Piketty, Rognlie,
Krusell and Smith, Kuznets, Solon, Mazumder, Corak, Chetty and coauthors, Lakner and Milanovic, Klass et al., Piketty,
Saez and Zucman, Jakobsen et al. and Black et al.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Pen's parade | The parade, minute by minute; the giants of the tax records; the question; objectives |
| 1 | Play it: four numbers | Four guesses; the answers |
| 2 | Measuring inequality | Lorenz and Gini with standard errors; the Census Gini; Atkinson's ethics; crossing curves |
| 3 | A century of top incomes | The U; eight countries; the measurement dispute |
| 4 | Pareto tails and random growth | The law; its exponent since 1913; careers; the Kolmogorov equation; the Fact |
| 5 | Why the tail moved so fast | Pure random growth against high-growth types; scale and type dependence |
| 6 | Wealth, and r against g | The Fed's shares; the exponent of wealth; r - g and the tail; the replies |
| — | Intermission | The top 1% share since 1913, as a tune |
| 7 | Kuznets's curve | The dual economy; the data; *Called it?* (partly right) |
| 8 | Like parent, like child? | The elasticity; attenuation; the Gatsby curve's mechanism; American places; the Fact |
| 9 | Forty million tax records | Rank-rank; the transition matrix; absolute mobility; growth against sharing |
| 10 | Places | The spread of upward mobility; the largest places; correlates; movers and MTO |
| 11 | The world's distribution | Between countries; the elephant curve; the world's top 1% |
| 12 | Does inequality matter? | Life expectancy by income; what can be identified |
| 13 | Redistribution and pre-distribution | From market to disposable income; changing market incomes |
| 14 | The Dials | The intergenerational elasticity; the Pareto exponent of top wealth |
| 15 | In practice | A distributional table; the four choices; precision |
| 16 | Frontier | Distributional national accounts; wealth taxes; genes, family and luck |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 41, *Taxes* |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's distribution module (`explainer.economics.agora.
distribution`), with the Island's Part 40 truths, or from the Data Room; the narration states the cached numbers.

- **The parade.** Heights are each parent percentile's mean family income (1996-2000, 2012 dollars) over the mean of
  the hundred percentiles, times 1.7 m; the giants use the 2022 shares of the top 1%, 0.1% and 0.01% of tax units
  over their population shares (income excluding capital gains).
- **The measures.** The Island's 2,000 incomes are careers under random growth (no drift, volatility 0.12, careers
  ending at rate 0.025) after 400 years, scaled to a mean of 60,000; standard errors from 400 bootstrap resamples.
  The two invented societies are A = (0.2 four times, 1 six times) and B = (0.8 nine times, 4.46), whose Ginis are
  equal (0.282).
- **Pareto exponents.** From two top shares p > q, alpha = 1 / (1 - ln(S_q/S_p) / ln(q/p)); the straight lines fit the
  log shares of the top 1% to 0.01%.
- **Random growth.** Log income drifts at nu with volatility sigma; careers end at rate delta and restart at 1; a
  reflecting floor at a third of the starting income. The Kolmogorov forward equation is solved on 1,000 points of log
  income from -1 to 16 as a continuous-time Markov chain (so that probability is conserved), its stationary state by
  a sparse linear solve and its transitions by implicit Euler steps of half a year. Volatility rises from 0.0894 to
  0.144 with delta 0.025 (the top 1% share from 6.6% to 20%). The type-dependent economy: ordinary careers drift at
  -3% with volatility 0.10; 15% of newcomers are high-growth types who turn ordinary at rate 0.2, and their growth
  rises from 8.5% to 16% a year. Half-lives are measured on the log of the top 1% share against its new stationary
  value.
- **Wealth.** Relative wealth grows at r - g - c with c = 0.03, volatility 0.15, and dynasties end or split at rate
  0.02; the exponent follows the same quadratic. The Fed's shares give the exponent from the top 1% and top 10%.
- **Kuznets.** 40,000 people whose log incomes are normal with standard deviation 0.4 on the land and 0.7 in the
  cities, where the mean is one log point higher.
- **Generations.** 6,000 families; parents' permanent log incomes with standard deviation 0.6; children's with the
  same spread and an elasticity of 0.45; yearly incomes add a transitory shock with standard deviation 0.55. The
  Gatsby mechanism: log income p h + u with skill h inherited at 0.5 and luck u with standard deviation 0.5, for
  returns p from 0.2 to 1.1. The binned elasticity regresses the log of children's mean income on the log of parents'
  mean income across parents' percentiles 10 to 90.
- **Mobility.** The rank-rank slope fits the mean child rank on the parent percentile's midpoint; the quintile matrix
  averages the percentiles' quintile shares within each fifth; upward mobility and correlations are weighted by each
  commuting zone's 2000 population.
- **The world.** Expenditure-side real GDP per person (PWT 11.0) for the 158 countries observed every year from 1980
  to 2023 (95% of the world's people in 2023), as a population-weighted Gini.
- **The distributional table.** A 20% flat tax on the Island's incomes, paid back as $12,000 a head; deciles of
  pre-tax income.

## Problems and solutions

**1.** *Lorenz: five people earn 1, 2, 3, 4 and 10. Draw the Lorenz curve and find the Gini, the top 20% share and
Atkinson's index with epsilon = 1.*

*Solution.* Total 20, so the curve passes through (0.2, 0.05), (0.4, 0.15), (0.6, 0.30), (0.8, 0.50) and (1, 1). The
area under it by trapezoids is 0.1 x (0.05 + 0.20 + 0.45 + 0.80 + 1.50) = 0.30, so the Gini is 1 - 2 x 0.30 = 0.40.
The top 20% (one person) hold 10/20 = 50%. With epsilon = 1 the equally distributed equivalent is the geometric mean,
240^(1/5) = 2.99, so Atkinson's index is 1 - 2.99/4 = 0.25.

**2.** *Pareto: the top 1% hold 20% of income and the top 0.1% hold 9%. What is alpha? What share do the top 0.01%
hold?*

*Solution.* The ratio 9/20 = 0.45 equals 0.1^(1 - 1/alpha), so 1 - 1/alpha = ln 0.45 / ln 0.1 = 0.347 and alpha = 1.53.
Under the same tail each tenfold step up multiplies the share by 0.45: the top 0.01% hold 9% x 0.45 = 4.1%.

**3.** *Random growth: with nu = 0, sigma = 0.1 and delta = 0.02, find zeta. What happens to zeta if careers last
twice as long?*

*Solution.* With no drift, zeta = sqrt(2 delta) / sigma = sqrt(0.04) / 0.1 = 2.0. Careers twice as long halve delta:
zeta = sqrt(0.02) / 0.1 = 1.41, a fatter tail, because luck has longer to compound before a career ends.

**4.** *Wealth: with r - g - c = 0.01, sigma = 0.15 and delta = 0.02, find the tail exponent. Is the mean finite?*

*Solution.* zeta = (-0.01 + sqrt(0.0001 + 2 x 0.0225 x 0.02)) / 0.0225 = (-0.01 + 0.0316) / 0.0225 = 0.96. A Pareto
tail with exponent at or below one has no finite mean: wealth would keep concentrating, with no stable distribution
of relative wealth. A point less of r - g gives 1.33.

**5.** *Kuznets: sigma_a = 0.4, sigma_m = 0.7, Delta = 1. At what modern share is the variance of log income
largest?*

*Solution.* V(s) = 0.49 s + 0.16 (1 - s) + s (1 - s), so V'(s) = 0.33 + 1 - 2s = 0 at s = 0.665, where V = 0.60
(against 0.16 with no one in the cities and 0.49 with everyone). Because the cities are more unequal, the variance
peaks after half have moved; the Gini, more sensitive to the gap between the sectors, peaks near half (chapter 7).

**6.** *Attenuation: sigma_perm = 0.6, sigma_trans = 0.55, beta = 0.45. What does one year of parents' income
estimate? Five years?*

*Solution.* With T years the estimate converges to beta x 0.36 / (0.36 + 0.3025 / T). For T = 1 the factor is
0.36 / 0.6625 = 0.54, so 0.245; for T = 5 it is 0.36 / 0.4205 = 0.86, so 0.385. The Island's estimates were 0.24 and
0.38.

**7.** *Ranks: with a rank-rank slope of 0.34 and a mean rank of 50 at the 50th percentile, what is the expected rank
of a child from the 25th percentile? From the 75th?*

*Solution.* The line is E[R] = 50 + 0.34 (P - 50): 41.5 at the 25th percentile and 58.5 at the 75th. Children from
families fifty percentiles apart end up seventeen percentiles apart on average.

**8.** *Derive zeta: substitute f(y) = e^(-zeta y) into the stationary Kolmogorov equation above the entry point, and
show that the positive root is the Pareto exponent of x = e^y.*

*Solution.* Above the entry point the stationary equation is 0 = -nu f' + (sigma²/2) f'' - delta f. With
f = e^(-zeta y), f' = -zeta f and f'' = zeta² f, so (sigma²/2) zeta² + nu zeta - delta = 0, whose roots have product
-2 delta / sigma² < 0: one positive, one negative. Above the entry point the density must be integrable, which rules
out the negative root, so zeta = (-nu + sqrt(nu² + 2 sigma² delta)) / sigma². Then P(Y > y) is proportional to
e^(-zeta y), and P(X > x) = P(Y > ln x) is proportional to x^(-zeta): a Pareto tail with exponent zeta.

## Lab and interactive

- `python -m videos.economics.labs 40`: the measures with standard errors; the Pareto exponent from the tax data;
  random growth's tail by theory, simulation and the Kolmogorov equation; the speed of transitions; wealth's tail
  against r - g; Kuznets's curve; attenuation; the Gatsby mechanism; the rank-rank slope, the transition matrix and
  absolute mobility.
- The interactive (course site): where long tails come from. The reader sets the volatility of income growth, the
  length of careers and the drift, and watches 4,000 simulated careers settle into a Pareto tail, with the theory's
  exponent, the top 1% share and the Lorenz curve.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[40]`; the two dials are in
`explainer/economics/dials.py`; Kuznets's prediction is a *Called it?* entry (`explainer/economics/calls.py`); Pareto
tails and the Gatsby curve are Facts (`explainer/economics/facts.py`). FRED's series were retrieved on 2026-11-20.
Auten and Splinter's figures were read from their paper's abstract and introduction as quoted, with Piketty, Saez and
Zucman's after-tax shares from the Brookings primer; Chetty et al.'s 0.341, 0.344, 4.4% and 12.9% from the published
paper; the 62% and 80% counterfactuals from the authors' VoxEU column and NBER abstract; the exposure effect and MTO
from the NBER abstracts; the life-expectancy gaps from the JAMA abstract; Klass et al.'s exponent from their abstract;
Corak's range from his 2012 Senate testimony, which uses the same 22-country estimates. The elephant curve is
described, not drawn: its percentile-by-percentile values were not transcribed, and the film states only the shape the
authors report. Kuznets's own description of his evidence is quoted from the article.
