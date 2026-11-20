# Economics, Built: Part 22, Consumption and Saving

Part 22 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth of Act V, *The Long Run*. It asks how households decide how much to spend
today, and answers: by looking ahead, but less than the theory says. A household that can borrow and save spreads a
windfall over its life and spends only the interest; prudence keeps a buffer of cash, and below it spending follows
income. Real households spend 10 to 40% of a windfall within a quarter, most when cash is short, whatever they own;
and across generations, how much a nation saves depends on its growth, its pensions and its bequests.

It opens with the 2001 US tax rebates, $300 for a single filer and $600 for a couple, mailed over ten weeks in an order
set by the second-to-last digit of each taxpayer's Social Security number: an experiment no one designed. From there
it covers:

- a game: of each rebate dollar, how much went on nondurables within the quarter? (20 to 40 cents, Johnson, Parker
  and Souleles 2006; 12 to 30 in 2008, 50 to 90 counting cars); and a number the viewer keeps for chapter 9;
- Keynes's consumption function and Kuznets's puzzle, the US ratio of consumption to income since 1959, and Friedman's
  errors-in-variables answer, run on 10,000 of the Island's households;
- permanent income and the life cycle (Friedman 1957; Modigliani and Brumberg 1954) from Part 7's Euler equation;
- Hall's random walk (1978) tested on sixty years of US quarters; Working's (1960) time-averaging effect;
- excess sensitivity (Flavin 1981), Campbell and Mankiw's rule-of-thumb share on the Island and in US data, and
  Deaton's paradox of excess smoothness; the fact that consumption is smoother than income;
- prudence (Kimball 1990), Zeldes (1989), and the buffer-stock household (Deaton 1991; Carroll 1997) solved by the
  endogenous grid method (Carroll 2006), with the propensity to spend of 20,000 such households;
- the rebate experiments of 2001, 2008 and 2020, and Alaska's dividend (Hsieh 2003; Kueng 2018); *Called it?* on Hall;
- an intermission without narration: US income and spending month by month, 1990-2026, the saving rate as a tune;
- the wealthy hand-to-mouth (Kaplan, Violante and Weidner 2014), on the Island, where spending follows liquid wealth;
- what people say and what lottery winners do (Jappelli and Pistaferri 2014; Fuster, Kaplan and Zafar 2021;
  Fagereng, Holm and Natvik 2021);
- Ricardian equivalence (Barro 1974) and why it fails;
- overlapping generations (Samuelson 1958; Diamond 1965), dynamic inefficiency, when a pay-as-you-go pension is a free
  lunch, and the test of Abel, Mankiw, Summers and Zeckhauser (1989);
- the saving of the rich, bequests, and China's household consumption (Penn World Table);
- a new dial (the propensity to spend a windfall), stimulus design and pension defaults in practice (Sahm, Shapiro and
  Slemrod 2012; Madrian and Shea 2001), and a frontier chapter on spending through unemployment (Ganong and Noel 2019)
  and heterogeneous-agent macroeconomics.

## Build it

```bash
python -m videos.economics.econ22.compute              # every number (seconds), into .cache/econ22/
python tools/qa_scene.py econ22 Buffer                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ22 -q l   # the whole part, silent preview
python tools/build.py econ22                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 22                     # the lab
```

The data are in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): FRED's monthly personal consumption expenditures in
total, on nondurables and on services with their price indexes, real disposable income and the saving rate; the Penn
World Table 11.0's household consumption shares; and the windfall studies, transcribed from their abstracts in
`tables.py` (`MPC_STUDIES`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | How do households decide how much to spend today? | The 2001 rebate schedule by Social Security digit; real disposable income jumping in July to September 2001 while spending on nondurables and services barely moves, the saving rate 4.2% in June, 6.9% in September, 2.9% in October; the question; not financial advice; objectives |
| 1 | Play it: what happened to the cheques? | Four answers from 2 to 90 cents; the viewer's own number for a month's income; the answers: permanent income under 1 cent a quarter, 2001 20-40 cents, 2008 12-30 (50-90 with durables) |
| 2 | Keynes's function and Kuznets's puzzle | The fundamental psychological law (1936); Kuznets's long series; US consumption between 0.82 and 0.94 of disposable income since 1959 while income rose 7.5 times; 10,000 Island households: the fitted line $C = 0.31 + 0.62Y$, the share consumed 1.27 for the poorest tenth and 0.72 for the richest; the planted truth $C = 0.9Y^P$; log slope 0.735 in theory, 0.73 measured; $C/Y$ at 0.90 for sixty years |
| 3 | Permanent income and the life cycle | The Euler equation; $c = \frac{r}{1+r}(A_0 + H)$; a windfall: 2.9 cents a year per dollar; a permanent raise: all of it; Modigliani and Brumberg: flat consumption, a hump of wealth peaking at 65 at 14 years of average income; saving with growth and age |
| 4 | Hall's random walk | $c_{t+1} = c_t + \varepsilon_{t+1}$; US nondurables and services, 1960-2019: income growth two to four quarters back, coefficients 0.09, 0.10 and 0.05, $F = 6.8$ ($p = 0.0002$); Working's correlation of 0.21 for three-month averages against 0.47 in the data |
| 5 | Too sensitive, and too smooth | Flavin (1981); Campbell and Mankiw's $\lambda$: 200 Island economies with $\lambda = 0.4$: OLS 0.67, IV median 0.38; US: OLS 0.23, IV 0.65 (s.e. 0.13) with a first-stage F of 4.2; Deaton's paradox: income growth autocorrelated 0.23, so the theory predicts consumption growth with sd 2.0% against income's 1.6%; actual 1.3%; the fact entered (quarterly sd 0.44% against 0.87%) |
| 6 | Precautionary saving and the buffer stock | Prudence with $u'(c) = c^{-2}$ (2.22 against 1); Carroll's household; the endogenous grid method in 133 rounds; $c(m)$ with and without risk; the share of an extra dollar spent: 0.89 at half a year's income, 0.57 at a year's, 0.07 at five; target cash 1.43; 20,000 households: 0.23 of a month's windfall within the year (0.38 for the tenth with least cash, 0.16 for the most) against 0.029 |
| 7 | The rebate experiments | Johnson, Parker and Souleles's design; 2001: 20-40% on nondurables in the quarter, about two-thirds over two quarters, most for low liquidity; 2008: 12-30%, 50-90% with durables; 2020: about 10% (21.7% for low liquid wealth); Alaska: Hsieh (2003), no response in survey data; Kueng (2018), 25% within a quarter in account data, above 50% for high-income liquid households; *Called it?*: Hall (1978), partly right |
| | Intermission: income and spending, month by month | No narration: real disposable income and real spending on nondurables and services, 1990-2026, with the rebate spikes of 2001, 2008 and 2020-21; the saving rate (31.8% in April 2020) as a tune |
| 8 | The wealthy hand-to-mouth | Liquid and illiquid wealth; Kaplan, Violante and Weidner: about a third of US households hand-to-mouth, over two-thirds of them wealthy; the Island's shortcut ($\beta_{\text{cash}} = 0.924$ for owners): owners' median net worth 3.3 years of income against 0.44, share spent 0.36 against 0.23; correlation with net worth +0.48, with liquid wealth −0.98 |
| 9 | Your answer, the surveys and the lottery | The viewer's number against permanent income (3%), the buffer stock (23%) and Italians asked in 2010 (48%, Jappelli and Pistaferri); Fuster, Kaplan and Zafar's gains, losses, news and loans; Norwegian lottery winners (Fagereng, Holm and Natvik): small prizes to the cash-poor spent in full within the year, large prizes to the cash-rich slightly below half |
| 10 | Ricardian equivalence | A month's income cut now, 0.151 years of income repaid in 20 years at 3%; Barro (1974); liquidity, finite lives and bequests, distortions; the Island: none spent by the Ricardian household, 0.23 by renters, 0.31 overall, 0.45 by those short of cash |
| 11 | Overlapping generations | Samuelson's money returning $1 + n = 1.4$ a generation; Diamond's map; patient ($\beta = 0.9$): $R = 1.27 < 1.4$, $k^* = 3.43$ against a golden 2.97, a pension raising welfare up to +0.45% of consumption at $d = 0.4$; impatient ($\beta = 0.3$): $R = 2.6$, every pension lowering welfare (−13.5% at $d = 0.8$); Abel, Mankiw, Summers and Zeckhauser (1989): efficient |
| 12 | The rich, bequests, and China | Dynan, Skinner and Zeldes (2004); Carroll's capitalist spirit; Kotlikoff and Summers (1981) against Modigliani (1988) on inherited wealth; household consumption's share of GDP, PWT: China 0.49 (1990), 0.35 (2010), 0.41 (2019), the United States 0.69; the life cycle (Modigliani and Cao 2004), precaution (Chamon and Prasad 2010), competitive saving (Wei and Zhang 2011) |
| 13 | The Dials: the propensity to spend a windfall | The new dial, percent spent: Johnson et al. 30 (20-40), Parker et al. 2013 21 (12-30), Parker et al. 2022 10, Kueng 25, Jappelli and Pistaferri 48, this film's buffer stock 23; depends on the setting; theory against the dial |
| 14 | In practice: stimulus and pensions | Targeting, speed and form: 25% would mostly spend 2008's payment, 13% 2009's lower withholding (Sahm, Shapiro and Slemrod); pay-as-you-go and funded pensions; automatic enrolment: participation 37% to 86%, 76% at the 3% default (Madrian and Shea); who uses this |
| 15 | Frontier: spending through unemployment | Ganong and Noel: nondurable spending −6% at job loss, under 1% a month while benefits last, −12% when they run out; extending benefits smooths four times as much as raising them; HANK (Kaplan, Moll and Violante 2018); open questions |
| | Recap, problems, and the road ahead | The answer; twelve lines; problems; reading; Mehra and Prescott (1985), and Part 23 |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's households (`explainer.economics.agora.household`) and
overlapping generations (`agora.olg`) with the Island's Part 22 truths, or from the Data Room; the narration states the
cached numbers.

- **US series.** Real spending on nondurables and services is each category's nominal spending divided by its own
  price index, summed; real disposable income is BEA's chained series. Quarterly figures are averages of three months.
- **Hall and Campbell-Mankiw.** OLS of quarterly log consumption growth on income growth at lags two to four, with a
  joint F test; 2SLS of consumption growth on income growth with income and consumption growth at lags two to four as
  instruments, 1960 to 2019.
- **Friedman.** 10,000 households with log permanent income N(0, 0.5²) and a transitory part N(0, 0.3²), each
  consuming 0.9 of permanent income; the cross-section regression and the aggregate ratio over sixty years of 2%
  growth.
- **The buffer stock.** Carroll's normalized problem ($\beta = 0.96$, $R = 1.03$, $\gamma = 2$, $G = 1.02$, shocks with
  10% spreads, a 0.5% chance of no income), seven-point lognormal shocks, solved by the endogenous grid method; 20,000
  households simulated for 400 years.
- **Hand-to-mouth.** Owners (60%) solve the same problem with $\beta R/R_h$ in place of $\beta$ ($R_h = 1.07$); illiquid
  wealth lognormal with median three years of income.
- **Diamond.** Log utility, $f(k) = 10k^{0.3}$, $n = 0.4$ a generation; next period's capital by bisection; the steady
  state after 400 periods; welfare as a consumption equivalent.

## Problems and solutions

**1.** *Kuznets and Friedman: with $\ln C = \ln 0.9 + p$ and $\ln Y = p + t$, $p$ and $t$ independent, show that the
slope of $\ln C$ on $\ln Y$ is $\sigma_p^2/(\sigma_p^2 + \sigma_t^2)$.*

*Solution.* The OLS slope is $\operatorname{cov}(\ln C, \ln Y)/\operatorname{var}(\ln Y) = \operatorname{cov}(p, p +
t)/\operatorname{var}(p + t) = \sigma_p^2/(\sigma_p^2 + \sigma_t^2)$. With $\sigma_p = 0.5$ and $\sigma_t = 0.3$ it is
$0.25/0.34 = 0.735$. Measured income is permanent income measured with error, the transitory part, so the slope is
attenuated (Part 4's errors in variables), and households sorted by measured income are partly sorted by luck: the
lucky look rich and seem to save, the unlucky look poor and seem to dissave.

**2.** *Permanent income: with $\beta(1+r) = 1$ and an infinite horizon, show that a windfall $w$ raises consumption by
$\frac{r}{1+r}w$ a year, and a permanent raise of 1 by 1.*

*Solution.* With $\beta(1+r) = 1$ the Euler equation gives a flat plan $c$. The budget is
$\sum_{t\ge0} c/(1+r)^t = c(1+r)/r = A_0 + H$, so $c = \frac{r}{1+r}(A_0 + H)$. A windfall raises $A_0$ by $w$, so $c$
rises by $\frac{r}{1+r}w$: at 3%, 2.9 cents a year per dollar. A raise of 1 every year from now raises $H$ by
$\sum_{t\ge0}(1+r)^{-t} = (1+r)/r$, so $c$ rises by exactly 1.

**3.** *Hall: derive $\mathbb{E}_t c_{t+1} = c_t$ from the Euler equation with quadratic utility, and say why income
growth at $t-1$ is a bad test variable with quarterly averages.*

*Solution.* With $u(c) = ac - \frac{b}{2}c^2$, $u'(c) = a - bc$ is linear, so $a - bc_t = \beta(1+r)\mathbb{E}_t(a -
bc_{t+1})$; with $\beta(1+r) = 1$, $c_t = \mathbb{E}_t c_{t+1}$, and $c_{t+1} - c_t$ is unforecastable from anything
known at $t$. Quarterly data are averages over the quarter: the change in the average from $t-1$ to $t$ shares
within-quarter innovations with the change from $t-2$ to $t-1$, so variables dated $t-1$ are correlated with the
current change even when the theory holds. A clean test uses information dated $t-2$ or earlier.

**4.** *Working's effect: for a random walk averaged over $m$ points, show that successive changes of the averages have
correlation $(m^2-1)/(2(2m^2+1))$.*

*Solution.* Write the walk as $x_s = \sum_{j\le s} e_j$ with unit-variance innovations, and let block $k$ hold dates
$km+1, \dots, km+m$. Then $\Delta\bar x_k = \frac1m\sum_{i=1}^m (x_{km+i} - x_{(k-1)m+i})$, and each bracket is the sum
of the $m$ innovations after date $(k-1)m+i$. Counting how often each innovation appears: the one at position $p$ of
block $k-1$ enters with weight $(p-1)/m$, and the one at position $p$ of block $k$ with weight $(m-p+1)/m$. So
$\operatorname{var}\Delta\bar x = \frac{1}{m^2}\big[\sum_{q=0}^{m-1}q^2 + \sum_{q=1}^{m}q^2\big] = \frac{2m^2+1}{3m}$.
Successive changes share only block $k-1$'s innovations, with weights $(p-1)/m$ in $\Delta\bar x_k$ and $(m-p+1)/m$ in
$\Delta\bar x_{k-1}$, so the covariance is $\frac{1}{m^2}\sum_{q=0}^{m-1}q(m-q) = \frac{m^2-1}{6m}$. The ratio is
$(m^2-1)/(2(2m^2+1))$: for three months a quarter, $8/38 = 0.21$; as $m\to\infty$, $1/4$ (Working 1960).

**5.** *Campbell and Mankiw: with $\Delta c = \lambda\Delta y + (1-\lambda)\varepsilon$, show that OLS of $\Delta c$ on
$\Delta y$ is biased when $\operatorname{cov}(\Delta y, \varepsilon) > 0$, and that a lagged instrument removes the
bias.*

*Solution.* $\hat b_{OLS} \to \lambda + (1-\lambda)\operatorname{cov}(\Delta y, \varepsilon)/\operatorname{var}(\Delta
y) > \lambda$: news about permanent income moves both the forward-looking households' consumption and current income.
An instrument $z$ dated $t-2$ is in the information set at $t-1$, so $\operatorname{cov}(z, \varepsilon_t) = 0$ by
Hall's argument, and if it forecasts $\Delta y_t$, then $\operatorname{cov}(z, \Delta c)/\operatorname{cov}(z, \Delta y) =
\lambda$. On the Island ($\lambda = 0.4$) OLS averages 0.67 and IV is centred near 0.38; a weak first stage, as in the
US data (F = 4.2), leaves IV biased toward OLS.

**6.** *Prudence: show that with $u'(c) = c^{-\gamma}$, a mean-preserving spread in $c_{t+1}$ raises
$\mathbb{E}u'(c_{t+1})$, and so raises saving.*

*Solution.* $u'''(c) = \gamma(\gamma+1)c^{-\gamma-2} > 0$, so $u'$ is convex, and by Jensen's inequality a
mean-preserving spread raises $\mathbb{E}u'(c_{t+1})$: with $\gamma = 2$, $c = 0.5$ or $1.5$ gives $(4 + 0.444)/2 = 2.22$
against $u'(1) = 1$. The Euler equation $u'(c_t) = \beta R\,\mathbb{E}u'(c_{t+1})$ then requires a higher $u'(c_t)$,
that is, lower consumption today and more saving: precautionary saving. With quadratic utility $u''' = 0$ and the
motive disappears.

**7.** *Ricardian equivalence: a tax cut $T$ today is repaid as $T(1+r)^n$ in $n$ years; show the household's lifetime
budget is unchanged, and name two reasons it may still spend.*

*Solution.* The later tax's present value is $T(1+r)^n/(1+r)^n = T$, so the present value of after-tax income, and
with it the budget constraint, is unchanged; a household that will pay the tax saves the cut. It may still spend if
it is short of cash and would have borrowed (its marginal propensity to spend the cut is then that of a windfall), or
if the tax will fall after its death on people whose welfare it does not weigh (no operative bequest). Distorting
taxes, uncertainty about who pays, and inattention are further reasons.

**8.** ★ *Diamond: with log utility and $f(k) = Ak^\alpha$, derive the steady state $k^*$, and show that a
pay-as-you-go pension raises steady-state welfare if and only if $R < 1 + n$.*

*Solution.* With log utility the young save $s = \frac{\beta}{1+\beta}w$ whatever the interest rate, and
$w = (1-\alpha)Ak^\alpha$, so $(1+n)k' = \frac{\beta}{1+\beta}(1-\alpha)Ak^\alpha$ and
$k^* = \left[\frac{\beta(1-\alpha)A}{(1+\beta)(1+n)}\right]^{1/(1-\alpha)}$. A small pension $d$ paid by each young
worker and received as $(1+n)d$ when old has two effects, and both have the sign of $1 + n - R$. At given prices, it
changes the present value of lifetime resources by $-d + (1+n)d/R$, positive exactly when $R < 1+n$: the pension pays
the growth rate, saving pays $R$. And it lowers saving and so steady-state capital, which raises consumption per head
exactly when capital is above the golden rule, where the marginal product of capital falls short of growth, again
$R < 1 + n$. So a small pension raises steady-state welfare if and only if the economy is dynamically inefficient.
On the Island, $\beta = 0.9$ gives $R = 1.27 < 1.4$ and a gain of 0.45% of consumption at $d = 0.4$;
$\beta = 0.3$ gives $R = 2.6$ and a loss at every $d$.

## Lab and interactive

- `python -m videos.economics.labs 22`: solve the buffer-stock household, simulate its propensity to spend, run
  Friedman's cross-section and Hall's test, and find when a pension raises welfare.
- The interactive (course site): a buffer-stock household's consumption function as income risk and patience change,
  with its target and the share of a windfall it spends.

## Sources

The rebate studies and the windfall evidence are read from their abstracts and NBER summaries, recorded with the date
checked in `tables.MPC_STUDIES` and in the dial `mpc_windfall` (`explainer/economics/dials.py`); Madrian and Shea's
numbers are from their working paper (`tables.MADRIAN_SHEA_2001`). The US series are FRED's, retrieved 2026-11-20.
