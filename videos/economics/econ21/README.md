# Economics, Built: Part 21, Growth II: Ideas and Institutions

Part 21 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third of Act V, *The Long Run*. It asks where the growth that capital cannot
explain comes from, and answers: from ideas, which unlike capital can be used by everyone at once and so do not run
into diminishing returns. Markets do too little research, ideas get harder to find, and they spread slowly; across
countries the residual is also how well ideas and resources are used, which institutions, shaped by history, geography
and culture, largely decide.

It opens with William Nordhaus's history of the price of light (1996): about 58 hours of work for 1,000 lumen-hours
from an open fire, 41.5 with a Babylonian lamp, 5.37 with a tallow candle in 1800. From there it covers:

- a game: what did the same light cost in 1992? (0.000119 hours, a third of a second: about 45,000 times cheaper);
  Nordhaus's finding that traditional price indexes overstated the price of light by a factor of 900 to 1,600;
- rival and non-rival goods; the replication argument for increasing returns; Euler's theorem and why ideas need
  monopoly, public money or prizes (Arrow 1962);
- the AK model, learning by doing (Arrow 1962), knowledge spillovers (Romer 1986) and human capital (Lucas 1988), with
  their knife edge and scale problem;
- Romer's (1990) economy derived: research, monopolists and final goods; the balanced growth rate
  $g = (\alpha\delta L - \rho)/(\alpha + \theta)$; too little research; the scale effect;
- creative destruction (Aghion and Howitt 1992): quality ladders sector by sector; the three wedges; the market's and a
  planner's research across step sizes, with too much research for small steps and too little for large;
- *Called it?* on Romer's scale effect; Jones (1995); Bloom, Jones, Van Reenen and Webb (2020): researchers ×23 and
  research productivity ÷41; semi-endogenous growth run in Agora;
- diffusion: adoption 45 years after invention on average (Comin and Hobijn 2010); appropriate technology; TFP levels
  across 113 countries (Penn World Table);
- an intermission without narration: every lamp Nordhaus priced, 1800-1993, with the cheapest light as a falling tune;
- misallocation: Hsieh and Klenow's measure derived and run on 4,000 of the Island's plants; the misallocation dial;
- institutions: settler mortality as an instrument (Acemoglu, Johnson and Robinson 2001), refitted on their 64
  countries; Albouy's critique; the reversal of fortune;
- borders as experiments: the two Koreas, Nogales, and Dell's (2010) mita;
- geography, disease and culture against institutions (Diamond; Gallup, Sachs and Mellinger; Alsan; Nunn and
  Wantchekon; Rodrik, Subramanian and Trebbi);
- directed technical change (Acemoglu 2002) and the college premium (Katz and Murphy 1992), run in Agora;
- patents, prizes and public research (Moser 2005; Williams 2013);
- a new dial (the social return to R&D), R&D tax credits in practice (Dechezleprêtre et al. 2023; Bloom, Van Reenen and
  Williams 2019), and a frontier chapter on growth with a declining population (Jones 2022) and automated research
  (Aghion, Jones and Jones 2019).

## Build it

```bash
python -m videos.economics.econ21.compute              # every number (seconds), into .cache/econ21/
python tools/qa_scene.py econ21 Ladder                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ21 -q l   # the whole part, silent preview
python tools/build.py econ21                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 21                     # the lab
```

The data are in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): Nordhaus's table 1.6 and Bloom, Jones, Van Reenen and
Webb's aggregate numbers, transcribed in `tables.py`; Acemoglu, Johnson and Robinson's base sample of 64 former
colonies, read from the R package hdm; and the Penn World Table 11.0.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Where does the growth that capital cannot explain come from? | Nordhaus's labour price of light: open fire 58 hours per 1,000 lumen-hours, Neolithic lamp 50, Babylonian lamp 41.5, tallow candle 5.37 (1800); traditional indexes overstated the price by 900 to 1,600 times (3.6% a year); the question; Romer (1990); objectives |
| 1 | Play it: how much work buys an hour of light? | Five answers from an hour to a third of a second; 1992's compact fluorescent bulb: 0.000119 hours (0.43 seconds), about 45,000 times cheaper than 1800, 5.4% a year; every lamp from 1800 on a log scale; the fact entered |
| 2 | Ideas are not like lamps | Rival and excludable goods; replication: doubling K and L doubles output, doubling A too quadruples it; Euler's theorem leaves nothing for ideas (Arrow 1962) |
| 3 | Growth without end: AK and learning by doing | $Y = AK$: 3% a year for ever, against Solow's fading path; Arrow's learning by doing and the Horndal works; Romer (1986); Lucas (1988); the knife edge and the scale problem |
| 4 | Romer's economy | Three sectors; $\pi = \alpha(1-\alpha)Y/A$, $V = \pi/r$, the researcher's arbitrage $L_Y = r/(\alpha\delta)$; $g = (\alpha\delta L - \rho)/(\alpha+\theta)$: 2% a year with a fifth of the island in research, $r$ = 4%; too little research; the scale effect (5.3% with twice the people) |
| 5 | Creative destruction | Aghion and Howitt (1992): 200 sectors, steps of 1.5 at rate $\lambda n$ (about 3 jumps each in 120 years), the average growing at $\lambda n \ln\gamma$ = 1.0%; appropriability, spillover and business stealing; the market's and a planner's research for steps from 1.005 to 3: at 1.2, 0.17 against 0; at 2.5, 0.44 against 0.67; crossing near 1.49 |
| 6 | Are ideas getting harder to find? | *Called it?*: Romer (1990), "the stock of human capital determines the rate of growth", wrong; Jones (1995); Bloom et al. (2020): effective researchers ×23 since the 1930s, research productivity ÷41 (−5.1% a year), Moore's law ×18, research productivity halving every 13 years; semi-endogenous growth with researchers growing 4.3% and $1 - \phi = 3$: idea growth tends to 1.4% |
| 7 | Diffusion: ideas cross borders slowly | Comin and Hobijn (2010): 15 technologies, 166 countries, adoption 45 years after invention, lags explaining at least a quarter of income differences; Basu and Weil (1998); PWT TFP levels 2019, 113 countries: 10th percentile 0.37, 90th 0.94 |
| | Intermission: two centuries of light | No narration: every lamp Nordhaus priced, 1800-1993, by device; the cheapest light at each date as a falling line and a falling tune |
| 8 | Misallocation: the same inputs, less output | TFPR and the Hsieh-Klenow formula $(\sigma/2)\operatorname{var}(\ln \text{TFPR})$; 4,000 of the Island's plants with wedges of sd 0.35 and 0.65: output lost 19% and 88% (formula 20% and 87%); the misallocation dial (China 30.5%, India 59.2% at America's dispersion; Bils, Klenow and Ruane's correction) |
| 9 | Institutions and settler mortality | North's rules of the game; reverse causation and omitted variables; Acemoglu, Johnson and Robinson (2001) on their 64 countries: first stage −0.61 (s.e. 0.13), F about 23, OLS 0.52, 2SLS 0.92 (published 0.94); Albouy (2012): 28 of 64 rates measured on own soil; the reply; the reversal of fortune (2002) and its fragility |
| 10 | Borders as experiments | The two Koreas; Nogales (about \$30,000 against a third of that, *Why Nations Fail*); Dell (2010): the mita, 1573-1812, consumption about 25% lower and stunting about 6 points higher today; land tenure and roads (illustrative regression discontinuity) |
| 11 | Geography, disease and culture | Diamond; Gallup, Sachs and Mellinger; Alsan's tsetse fly; Nunn and Wantchekon's slave trades and trust; Rodrik, Subramanian and Trebbi's "institutions rule"; entanglement |
| 12 | Directed technical change | The college premium rose as supply rose (Katz and Murphy 1992); Acemoglu (2002): price and market-size effects; long-run slope $\sigma - 2$; curves for $\sigma$ = 1.4 (slopes −0.71 and −0.6) and 3 (+1) |
| 13 | Patents, prizes and public research | Patents, prizes (Longitude, 1714), public research, secrecy; Moser (2005): patents shifted direction more than rate; Williams (2013): Celera's IP, 20-30% less follow-on research |
| 14 | The Dials: the return to research, and misallocation | The new dial, % a year: Jones and Williams (1998) 30 (optimal R&D two to four times actual), Bloom, Schankerman and Van Reenen (2013) 55 (private 21), Lucking, Bloom and Van Reenen (2019) 58 (private 14); settled within a range; the two dials together |
| 15 | In practice: R&D policy and productivity analysis | The UK's 2008 threshold as a regression discontinuity (Dechezleprêtre et al. 2023): more R&D and patents for up to seven years, larger for constrained firms, spillovers; Bloom, Van Reenen and Williams (2019); who does this work |
| 16 | Frontier: growth with fewer people | $g_A = \lambda n/(1-\phi)$ with $n < 0$; Jones (2022): an empty planet; automated research (Aghion, Jones and Jones 2019) and Baumol's cost disease; open questions |
| | Recap, problems, and the road ahead | The answer; twelve lines; problems; reading; Friedman (1957), and Part 22 |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's ideas module (`explainer.economics.agora.ideas`),
misallocation measure (`agora.ge.misallocation`) and 2SLS (`agora.econometrician.iv`, over statkit's `quasi`), with the
Island's Part 21 truths, or from the Data Room; the narration states the cached numbers.

- **Romer.** The balanced path from the researcher's arbitrage and the Euler equation; the stock of designs on it; the
  growth rate across labour-force sizes.
- **Aghion and Howitt.** The market's research from $\alpha(\rho + \lambda n) = \lambda\gamma(1-\alpha)(L - n)$
  (risk-neutral households, as in the paper) and a log-utility planner's $n^* = L - \alpha\rho/(\lambda\ln\gamma)$,
  across 120 step sizes; 200 simulated sectors.
- **Semi-endogenous growth.** $\dot A = \theta S^{\lambda}A^{\phi}$ year by year with $S$ growing 4.3% a year.
- **Misallocation.** 4,000 plants with lognormal physical productivity and wedges; output under the distorted and
  the efficient allocation of labour, computed directly, against the lognormal formula.
- **Institutions.** OLS, first stage, reduced form and 2SLS of log GDP per head on expropriation risk, instrumented by
  log settler mortality, on AJR's 64 countries.

## Problems and solutions

**1.** *Replication: with $Y = A K^{\alpha} L^{1-\alpha}$, show that doubling $K$ and $L$ doubles $Y$, that doubling $A$
too quadruples it, and that paying $K$ and $L$ their marginal products uses up all of $Y$.*

*Solution.* $A(2K)^{\alpha}(2L)^{1-\alpha} = 2^{\alpha + 1 - \alpha} Y = 2Y$, and with $2A$ as well, $4Y$. The marginal
products are $\alpha Y/K$ and $(1-\alpha)Y/L$, so $rK + wL = \alpha Y + (1-\alpha)Y = Y$ (Euler's theorem for a
function homogeneous of degree one in $K$ and $L$). Nothing is left to pay for $A$: ideas must be financed by
monopoly rents, public money, prizes, or come as a by-product.

**2.** *AK: with $Y = AK$ and $\dot K = sY - \delta K$, find the growth rate, and show that a permanent rise in $s$
raises growth for ever.*

*Solution.* $\dot K/K = sA - \delta$, and $Y$ grows at the same rate. It does not depend on $K$, so there is no steady
state for the level and no convergence: with $s = 0.2$, $A = 0.4$ and $\delta = 0.05$, growth is 3% a year from the
first year. Raising $s$ to 0.25 raises it to 5% permanently, unlike the Solow model, where the effect on growth fades.

**3.** *Romer: derive $L_Y = r/(\alpha\delta)$ from the researcher's arbitrage, and the balanced growth rate
$g = (\alpha\delta L - \rho)/(\alpha + \theta)$.*

*Solution.* Each design's monopolist earns $\pi = \alpha(1-\alpha)Y/A$; on the balanced path $Y/A$ is constant, so a
patent is worth $V = \pi/r$. A researcher finds $\delta A$ designs a year, earning $\delta A V = \delta\alpha(1-\alpha)Y/r$.
A production worker earns $(1-\alpha)Y/L_Y$. Equal pay gives $L_Y = r/(\alpha\delta)$. Then
$g = \delta(L - L_Y) = \delta L - r/\alpha$ and, with $r = \rho + \theta g$,
$g(1 + \theta/\alpha) = \delta L - \rho/\alpha$, so $g = (\alpha\delta L - \rho)/(\alpha + \theta)$. With
$\alpha = 0.5$, $\delta = 0.1$, $L = 1$, $\rho = 0.02$ and $\theta = 1$: $g = 2\%$, $L_Y = 0.8$, $r = 4\%$.

**4.** *The ladder: with research $n$, arrival rate $\lambda n$ and steps $\gamma$, show that expected log productivity
grows at $\lambda n \ln\gamma$, and solve for the market's $n$.*

*Solution.* In time $t$ the number of innovations $N_t$ is Poisson with mean $\lambda n t$, and $\ln A_t = \ln A_0 +
N_t \ln\gamma$, so $E\ln A_t = \ln A_0 + \lambda n t\ln\gamma$. A researcher earns $\lambda$ times the value of the next
patent, $\gamma\pi/(r + \lambda n)$, where the patent's profit is $\gamma$ times today's $\pi = (1-\alpha)wx/\alpha$
and lasts until the next innovation. Setting this equal to $w$, with $x = L - n$ and $r = \rho$:
$\alpha(\rho + \lambda n) = \lambda\gamma(1-\alpha)(L - n)$, so
$n = [\lambda\gamma(1-\alpha)L - \alpha\rho]/[\lambda(\alpha + \gamma(1-\alpha))]$.

**5.** *Semi-endogenous growth: with $\dot A = \theta S^{\lambda}A^{\phi}$ and $S$ growing at $n$, show that on a
balanced path $g_A = \lambda n/(1 - \phi)$.*

*Solution.* $g_A = \dot A/A = \theta S^{\lambda}A^{\phi-1}$. On a balanced path $g_A$ is constant, so its growth rate
is zero: $\lambda n + (\phi - 1)g_A = 0$, giving $g_A = \lambda n/(1-\phi)$. With $\lambda = 1$, $n = 4.3\%$ and
$\phi = -2$, $g_A = 1.43\%$. Research productivity, $g_A/S$, falls at rate $n$ along the path.

**6.** *Misallocation: with $\ln$ TFPR normal with variance $v$, independent of $\ln A$, show that
$\ln(Y_{\text{eff}}/Y) = \sigma v/2$ in the one-factor model.*

*Solution.* With $Y = (\sum_i (A_iL_i)^{e})^{1/e}$, $e = (\sigma-1)/\sigma$, a plant facing wedge $\tau_i$ hires
$L_i \propto A_i^{\sigma-1}\tau_i^{-\sigma}$. Substituting, $Y \propto (\sum A^{\sigma-1}\tau^{1-\sigma})^{1/e} /
\sum A^{\sigma-1}\tau^{-\sigma}$, and the efficient allocation sets $\tau_i = 1$. With $\ln\tau \sim N(0, v)$ independent
of $A$ and many plants, $E\tau^{1-\sigma} = e^{(\sigma-1)^2v/2}$ and $E\tau^{-\sigma} = e^{\sigma^2 v/2}$, so
$Y/Y_{\text{eff}} = e^{[\sigma(\sigma-1) - \sigma^2]v/2} = e^{-\sigma v/2}$. With $\sigma = 3$ and sd 0.65, the loss is
$e^{1.5 \times 0.42} - 1 \approx 88\%$, as Agora finds on 4,000 plants (with 400 plants the sample misses the tails).

**7.** *Settler mortality: with the first stage $-0.61$ and the reduced form $-0.57$, compute the 2SLS estimate, and
state the exclusion restriction it needs.*

*Solution.* With one instrument, 2SLS is the ratio of the reduced form (log GDP on log mortality) to the first stage
(expropriation risk on log mortality): $-0.566/-0.613 \approx 0.92$. It needs settler mortality to affect income today
only through institutions: not through today's disease burden, the settlers' human capital, or anything else
correlated with it. Albouy's critique adds a measurement problem: most of the mortality rates were assigned from other
places.

**8.** *$\bigstar$ Directed technical change: with $N_H/N_L \propto (H/L)^{\sigma-1}$, derive the long-run response of
the skill premium to $H/L$, and the condition for it to slope up.*

*Solution.* The premium is $w_H/w_L = (N_H/N_L)^{(\sigma-1)/\sigma}(H/L)^{-1/\sigma}$. Substituting,
$(H/L)^{(\sigma-1)^2/\sigma - 1/\sigma} = (H/L)^{(\sigma^2 - 2\sigma)/\sigma} = (H/L)^{\sigma - 2}$. It slopes up when
$\sigma > 2$: then a rise in the supply of skill induces enough skill-biased invention to raise the premium. With
$\sigma \approx 1.4$, as Katz and Murphy estimate, the long-run slope is $-0.6$, flatter than the short-run $-0.71$ but
still negative; Acemoglu's richer models, with state dependence in invention, lower the threshold.

## Where it comes back

| Idea | Parts |
|---|---|
| Consumption, saving and the Euler equation | 22 *Consumption and Saving* |
| Market power, markups and the spread of productivity | 43 *Measuring Market Power*; 44 *Dynamics, Platforms and Antitrust* |
| Development and poverty | 46 *Development* |
| Institutions and how they change | 47 *Political Economy* |
| The economics of AI | 65 *The Economics of AI* |
| Industrial policy | 66 *Geoeconomics and Industrial Policy* |

## Sources

- W. D. Nordhaus, "Do Real-Output and Real-Wage Measures Capture Reality? The History of Lighting Suggests Not", in
  T. F. Bresnahan and R. J. Gordon (eds), *The Economics of New Goods* (NBER, 1996), table 1.6.
- K. J. Arrow, "The Economic Implications of Learning by Doing", *REStud* 29(3) (1962), and "Economic Welfare and the
  Allocation of Resources for Invention" (NBER, 1962); P. M. Romer, *JPE* 94(5) (1986) and "Endogenous Technological
  Change", *JPE* 98(5) (1990): S71-S102; R. E. Lucas, *JME* 22(1) (1988); P. Aghion and P. Howitt, *Econometrica*
  60(2) (1992): 323-351.
- C. I. Jones, *QJE* 110(2) (1995): 495-525, and "The End of Economic Growth?", *AER* 112(11) (2022): 3489-3527; N.
  Bloom, C. I. Jones, J. Van Reenen and M. Webb, "Are Ideas Getting Harder to Find?", *AER* 110(4) (2020): 1104-1144.
- D. Comin and B. Hobijn, *AER* 100(5) (2010): 2031-2059; S. Basu and D. N. Weil, *QJE* 113(4) (1998).
- C.-T. Hsieh and P. J. Klenow, *QJE* 124(4) (2009): 1403-1448; M. Bils, P. J. Klenow and C. Ruane (2021).
- D. Acemoglu, S. Johnson and J. A. Robinson, *AER* 91(5) (2001): 1369-1401, and *QJE* 117(4) (2002); D. Albouy, *AER*
  102(6) (2012): 3059-3076; M. Dell, *Econometrica* 78(6) (2010): 1863-1903; D. Acemoglu and J. A. Robinson, *Why
  Nations Fail* (2012); D. Rodrik, A. Subramanian and F. Trebbi, *Journal of Economic Growth* 9(2) (2004).
- J. Diamond, *Guns, Germs, and Steel* (1997); J. L. Gallup, J. D. Sachs and A. D. Mellinger (1999); M. Alsan, *AER*
  105(1) (2015); N. Nunn and L. Wantchekon, *AER* 101(7) (2011).
- D. Acemoglu, "Directed Technical Change", *REStud* 69(4) (2002); L. F. Katz and K. M. Murphy, *QJE* 107(1) (1992).
- P. Moser, *AER* 95(4) (2005); H. L. Williams, *JPE* 121(1) (2013): 1-27.
- C. I. Jones and J. C. Williams, *QJE* 113(4) (1998): 1119-1135; N. Bloom, M. Schankerman and J. Van Reenen,
  *Econometrica* 81(4) (2013): 1347-1393; B. Lucking, N. Bloom and J. Van Reenen, *Fiscal Studies* 40(4) (2019):
  561-590.
- A. Dechezleprêtre, E. Einiö, R. Martin, K.-T. Nguyen and J. Van Reenen, *AEJ: Economic Policy* 15(4) (2023):
  486-521; N. Bloom, J. Van Reenen and H. Williams, "A Toolkit of Policies to Promote Innovation", *JEP* 33(3) (2019);
  P. Aghion, B. F. Jones and C. I. Jones, "Artificial Intelligence and Economic Growth" (2019).
- Acemoglu, Johnson and Robinson's data via the R package hdm (Chernozhukov, Hansen and Spindler); the Penn World Table
  11.0.
