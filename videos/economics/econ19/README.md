# Economics, Built: Part 19, The Great Escape

Part 19 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first of Act V, *The Long Run*. It asks why almost everyone was poor for almost all
of history, and what changed, and answers: in a world of fixed land, every gain in technology became more people
rather than more income, Malthus's trap, which England's wages obeyed for five centuries. What changed was that
technology began to improve faster than population could catch it, and then that parents, in a world where skills
paid, chose fewer, better-educated children. Why it began in north-western Europe around 1800 is still argued: prices,
ideas and institutions all played a part.

It opens with the Reverend Thomas Malthus's anonymous *Essay* of 1798 (population grows geometrically, subsistence
arithmetically), and with seven centuries of English real wages that obey him until just after he wrote. From there it
covers:

- a game: on an empty axis from 1270 to 2016, choose when England's income per head began to climb for good;
- the Malthusian model derived (diminishing returns on fixed land; births and deaths that follow income) and run on the
  island, with a plague and a better plough;
- Malthus tested: England's labour demand curve, 1270-1640, and its end after 1600; Ashraf and Galor (2011) across
  countries; Clark's claim;
- the Black Death as a natural experiment: nearly half of England dies in 1348-51, real wages nearly triple by 1450, and
  fall back as the population recovers; the Statute of Labourers; Voigtländer and Voth's three horsemen;
- why Britain, and why the 1760s: prices (Allen 2009), ideas (Mokyr), institutions (North and Weingast 1989), each with
  its critics (Humphries; Kelly, Mokyr and Ó Gráda; Clark 1996);
- why not China: Needham's question, Pomeranz (2000), and Broadberry, Guan and Li (2018), on Maddison's series;
- an intermission without narration: GDP per head, 1820-2022, for seven countries (Maddison), the great divergence and
  the great convergence;
- the Industrial Revolution in numbers: slow growth until 1830 (Crafts and Harley 1992; Crafts 2004) and Engels's pause
  (Allen 2009);
- the demographic transition: life expectancy from 1543, fertility from 1891; quantity against quality (Becker and
  Lewis 1973);
- one model for the whole story: Kremer's scale effect (1993) and Galor and Weil (2000), run in Agora;
- was it good? men's heights by decade of birth, the standard-of-living debate, longer working years (Voth; de Vries);
- a new dial (English living standards, 1300-1700, three reconstructions), *Called it?* on Ehrlich's *Population Bomb*
  and the Simon-Ehrlich wager, the UN's projections, and a frontier chapter on deep roots (Comin, Easterly and Gong;
  Spolaore and Wacziarg; Ashraf and Galor) and spatial noise in persistence studies (Kelly 2019), demonstrated in Agora.

## Build it

```bash
python -m videos.economics.econ19.compute              # every number (seconds), into .cache/econ19/
python tools/qa_scene.py econ19 Plague                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ19 -q l   # the whole part, silent preview
python tools/build.py econ19                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 19                     # the lab
```

The data are frozen extracts in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): the Bank of England's *A Millennium of Macroeconomic Data*
(version 3.1) for England's population, real wages (from daily wage rates, and adjusted for days worked) and real GDP
per head; the Maddison Project Database 2023; and Our World in Data's long-run population, life expectancy, fertility
and men's heights. Malthus's passage is transcribed from the first edition in `explainer/economics/data/tables.py`.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Why was almost everyone poor for almost all of history, and what changed? | Malthus's *Essay* (1798) and its two ratios; English real wages, 1209-1798, going nowhere, then about seventeenfold by 2016; the question; objectives |
| 1 | Play it: when did the climb begin? | Five candidate years (1350, 1500, 1650, 1800, 1900); England's real GDP per head (Broadberry et al.; Bank of England), 806 pounds in 1270, 978 in 1650, 2,332 in 1800, 28,982 in 2016 (×12 since 1800); on a log scale, growth of 0.05% a year to 1650, 0.58% to 1800, 1.17% since; real wages not above their 1450 level for good until 1874 |
| 2 | The Malthusian model | Income per head $A(X/L)^{\beta}$ with $\beta = 0.6$; births and deaths crossing at subsistence; the stable trap; a better plough ($A$ +50%) leaves income at subsistence with 1.97 times the people; Agora's island: a plague kills 45%, income jumps 43% and returns with a half-life of about 58 years |
| 3 | Malthus tested | England's decades, 1270-1859: log wages on log population, slope -0.90 (Newey-West s.e. 0.05), $R^2$ 0.82, for 1270-1640; +0.59 for 1600-1800; the residuals' first-order correlation (0.64) and the slope's standard error by lag window (0.022 with none, 0.050 with ten years, 0.071 with forty: still 13 standard errors from zero); Ashraf and Galor (2011); Clark's claim, disputed in detail |
| 4 | The Black Death as an experiment | England's population 4.8 million (1348) to 2.6 million (1351), 46% dead; real wages ×2.2 by 1400, ×2.7 by 1450; 5.3 million and wages back to 29 by 1650; the Statute of Labourers (1351) and the Peasants' Revolt (1381); Voigtländer and Voth (2013) |
| 5 | Why 1760, and why Britain? | Prices: dear labour and cheap coal (Allen 2009) against Humphries (2013) and Kelly, Mokyr and Ó Gráda (2014); ideas: the industrial Enlightenment (Mokyr); institutions: 1688 (North and Weingast 1989) against Clark (1996) |
| 6 | Why not China? | Needham's question; Maddison's GDP per head 1000-1850 for Britain, the Netherlands, Italy, China, Japan and India (Britain 1,151 and China 1,225 dollars in 1000; 2,412 and 1,543 in 1700; 4,332 and 858 in 1850); the little divergence; Pomeranz (2000) against Broadberry, Guan and Li (2018): the Yangzi delta behind Europe's richest region around 1700 |
| | Intermission: the great divergence, and the great convergence | No narration: GDP per head, 1820-2022, for Britain, the United States, Japan, South Korea, China, India and Nigeria (Maddison); the world's GDP per head as a tune; the story so far |
| 7 | The Industrial Revolution in numbers | English GDP per head growth: 0.33% (1700-60), 0.34% (1760-1800), 0.19% (1800-30), 1.17% (1830-70), 0.76% (1870-1913); Crafts and Harley (1992), Crafts on steam (2004); Engels's pause: from 1780 to 1840 output per head +31%, real wages +12% (Allen 2009) |
| 8 | The demographic transition | Life expectancy: England 34 (1543), 43 (1850); Sweden 32 (1800), 52 (1900); the world 28.5 (1800), 73 (2023); fertility: Sweden 4.1 (1891) to 1.7 (1935); the world 4.9 (1950) to 2.3 (2023); South Korea 6.1 to 0.72; Nigeria 4.5; Becker and Lewis (1973) in Galor and Weil's form |
| 9 | One model for the whole story | Kremer (1993): more people, faster technology; Galor and Weil's household solved on screen, schooling zero until technology's growth passes $\rho^2\tau/(1-\rho) = 0.075$ a generation, then rising; Agora's unified economy from the year 1000: Malthusian, then a take-off around 1600, fertility peaking around 1875, then modern growth |
| 10 | Was it good? | Men's heights by decade of birth: Britain 169.8 cm (1760s), 165.6 (1850s), 176.9 (1960s), with the Netherlands, the United States and Sweden; optimists, pessimists, longer working years (Voth 2000; de Vries 1994) |
| 11 | The Dials: growth before the escape | The new dial, % a year 1300-1700: GDP per head 0.189 (Broadberry et al. 2015), day wages 0.072, days-adjusted earnings 0.104 (Humphries and Weisdorf); compounded over four centuries, ×2.13, ×1.33 and ×1.52, against a doubling every sixty years or so since 1800; contested; why the reconstructions disagree |
| 12 | In practice: forecasting the long run | *Called it?*: Ehrlich (1968), wrong; the Simon-Ehrlich wager ($576.07); the UN's 2024 projection (a peak near 10.3 billion in the mid-2080s; 63 countries past their peak) |
| 13 | Frontier: deep roots and persistence | Comin, Easterly and Gong (2010); Spolaore and Wacziarg (2009); Ashraf and Galor (2013) and its critics; Kelly (2019): in Agora, two unrelated smooth maps over 300 places look significantly related 55% of the time (5% without spatial pattern); open questions |
| | Recap, problems, and the road ahead | The answer; twelve lines; problems; reading; Solow (1956), and Part 20 |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's long-run module (`explainer.economics.agora.malthus`), with
the Island's Part 19 truths in `explainer.economics.island`, or from the Data Room; the narration states the cached
numbers.

- **The Malthusian economy.** Income per head on fixed land, population growth $\lambda \ln(y/\bar y)$, a plague and an
  invention scheduled; the steady state in closed form; births and deaths for the diagram.
- **England's curve.** OLS of log real wages on log population for 1270-1640 and 1600-1800 on annual data, with HC1 and
  Newey-West (ten lags) standard errors; decade means for the scatter.
- **Unified growth.** Galor and Weil's household (education chosen to maximize $h(e, g)/(\tau + e)$), fertility
  $\min(y^{\kappa}, \gamma/(\tau + e))$, technology growth $\phi(e + a)L$; regimes labelled by rule.
- **Spatial noise.** Two independent Gaussian fields with exponential covariance on 300 random places, 400 times; the
  share of OLS slopes called significant at 5%.
- **Data.** Growth rates and indexes from the Bank of England's series; Maddison's GDP per head, interpolated in logs for
  the film; Our World in Data's long-run series; the dial's three rows, checked against the data when computed.

## Problems and solutions

**1.** *The steady state: with $y = A (X/L)^{\beta}$ and population growth $\lambda \ln(y/\bar y)$, find $L^*$, and show
that raising $A$ by half multiplies $L^*$ by $1.5^{1/\beta}$ and leaves $y^*$ unchanged.*

*Solution.* Population is constant when $y = \bar y$, so $A (X/L^*)^{\beta} = \bar y$ and $L^* = X (A/\bar y)^{1/\beta}$.
Income at the steady state is $\bar y$ whatever $A$ is. Replacing $A$ by $1.5A$ multiplies $L^*$ by $1.5^{1/\beta}$; with
$\beta = 0.6$ that is $1.5^{5/3} \approx 1.97$. The model's dynamics are stable: above $L^*$, $y < \bar y$ and the
population shrinks; below it, the population grows.

**2.** *The plague: if 45% die and $\beta = 0.6$, by how much does income per head jump? Linearize the recovery and find
its half-life when $\lambda = 0.02$.*

*Solution.* Income per head scales as $L^{-\beta}$, so it jumps by $0.55^{-0.6} = e^{0.6 \times 0.598} \approx 1.43$:
43%. Let $\ell = \ln L - \ln L^*$. Then $\ln y - \ln \bar y = -\beta \ell$ and $\dot \ell = \lambda(\ln y - \ln \bar y)
= -\lambda \beta \ell$, so the gap decays at rate $\lambda\beta = 0.012$ a year, with a half-life of
$\ln 2 / 0.012 \approx 58$ years.

**3.** *England's curve: with the decade averages, estimate the elasticity of real wages to population for 1270-1640, and
explain why ordinary standard errors overstate its precision.*

*Solution.* Agora's OLS on the annual series gives a slope of $-0.90$ with $R^2 = 0.82$. Its heteroskedasticity-robust
standard error is 0.022, but the Newey-West error, which allows each year's residual to be correlated with the next ten,
is 0.050. Population and wages move slowly, so successive years are not independent observations: the effective sample
is far smaller than 371 years, and ignoring that understates the uncertainty by more than half. The slope is still far
from zero.

**4.** *Growth rates: from the Bank of England's series, compute England's growth of GDP per head for 1270-1650,
1650-1800 and 1800-2016, and the doubling time of each.*

*Solution.* GDP per head was 806 pounds (2013 prices) in 1270, 978 in 1650, 2,332 in 1800 and 28,982 in 2016. Growth is
$(978/806)^{1/380} - 1 = 0.051\%$, $(2332/978)^{1/150} - 1 = 0.58\%$ and $(28982/2332)^{1/216} - 1 = 1.17\%$ a year.
Doubling times, $\ln 2 / \ln(1 + g)$: about 1,360, 120 and 59 years.

**5.** *Engels's pause: index output per head and real wages to 1780, and find each one's growth to 1840; what happened
to the share of income going to labour?*

*Solution.* By 1840 output per head had reached 131 and real wages 112: growth of 0.45% and 0.18% a year. If employment
per head did not change much, and the price indexes for output and for workers' consumption moved alike, labour's share
fell by about $1 - 112/131 \approx 15\%$ of its level: the gains went to profits, rents and capital. (The two price
indexes are not the same, so this is an approximation; Allen's argument rests on factor shares estimated directly.)

**6.** *Quantity and quality: maximize $h(e,g)/(\tau + e)$ with $h = (e + \rho\tau)/(e + \rho\tau + g)$, and find the
threshold $g$ above which parents educate.*

*Solution.* Maximize $\ln(e + \rho\tau) - \ln(e + \rho\tau + g) - \ln(\tau + e)$. Its derivative at $e = 0$ is
$1/(\rho\tau) - 1/(\rho\tau + g) - 1/\tau$, positive when $g/(\rho\tau(\rho\tau + g)) > 1/\tau$, that is
$g(1 - \rho) > \rho^2 \tau$. So parents educate only when $g > \rho^2\tau/(1 - \rho)$; with $\rho = 0.5$ and
$\tau = 0.15$, $g > 0.075$, as Agora finds numerically. Above it, $e$ rises with $g$, and fertility
$\gamma/(\tau + e)$ falls.

**7.** *Kremer: if $\dot A / A = \phi L$ and population is always at its Malthusian level $L \propto A^{1/\beta}$, show
that population growth rises with population.*

*Solution.* Taking logs and differentiating, $\dot L / L = (1/\beta)\,\dot A / A = (\phi/\beta) L$. The growth rate is
proportional to the level, so population grows faster as it grows: hyperbolically rather than exponentially, as world
population did from prehistory until the 1960s.

**8.** *$\bigstar$ Spatial noise: two independent fields with covariance $e^{-d/\ell}$ on $n$ sites; explain why the OLS
$t$-statistic's variance exceeds one, and how a spatial HAC correction fixes it.*

*Solution.* With $x$ and $y$ independent and demeaned, the slope is $\hat b = \sum_i x_i y_i / \sum_i x_i^2$. Conditional
on $x$, $\operatorname{Var}(\sum_i x_i y_i) = \sum_i \sum_j x_i x_j C_y(d_{ij})$, which includes every pair of nearby
sites; OLS keeps only the $i = j$ terms. When both fields are smooth, $x_i x_j$ tends to be positive for nearby pairs, so
the true variance is larger than OLS assumes, and $t$ has a variance well above one: in Agora, 55% of slopes are
"significant" at 5%. A spatial HAC estimator (Conley 1999) keeps the cross terms for pairs within a cutoff distance,
weighted by a kernel, and restores roughly correct coverage.

## Where it comes back

| Idea | Parts |
|---|---|
| Capital, saving and the Solow model | 20 *Growth I: Capital* |
| Ideas, scale effects and endogenous growth | 21 *Growth II: Ideas* |
| Institutions and political economy | 47 *Political Economy* |
| Development, poverty traps and what poor countries can do | 46 *Development* |
| Population, climate and the long run | 48 *Environment and Climate* |

## Sources

- T. R. Malthus, *An Essay on the Principle of Population* (1798); D. Ricardo, *On the Principles of Political Economy
  and Taxation* (1817).
- R. Thomas and N. Dimsdale, *A Millennium of UK Data*, Bank of England OBRA dataset, version 3.1 (2017); S. Broadberry,
  B. M. S. Campbell, A. Klein, M. Overton and B. van Leeuwen, *British Economic Growth, 1270-1870* (2015); J. Humphries
  and J. Weisdorf, "Unreal Wages? Real Income and Economic Growth in England, 1260-1850", *Economic Journal* 129(623)
  (2019).
- J. Bolt and J. L. van Zanden, Maddison Project Database 2023; S. Broadberry, H. Guan and D. D. Li, "China, Europe, and
  the Great Divergence: A Study in Historical National Accounting, 980-1850", *Journal of Economic History* 78(4)
  (2018): 955-1000; K. Pomeranz, *The Great Divergence* (2000); J. Needham, *Science and Civilisation in China* (from
  1954).
- Q. Ashraf and O. Galor, "Dynamics and Stagnation in the Malthusian Epoch", *American Economic Review* 101(5) (2011):
  2003-2041; "The 'Out of Africa' Hypothesis, Human Genetic Diversity, and Comparative Economic Development", *American
  Economic Review* 103(1) (2013): 1-46; G. Clark, *A Farewell to Alms* (2007); "The Political Foundations of Modern
  Economic Growth: England, 1540-1800", *Journal of Interdisciplinary History* 26(4) (1996): 563-588.
- N. Voigtländer and H.-J. Voth, "The Three Horsemen of Riches: Plague, War, and Urbanization in Early Modern Europe",
  *Review of Economic Studies* 80(2) (2013): 774-811.
- R. C. Allen, *The British Industrial Revolution in Global Perspective* (2009); "Engels' Pause: Technical Change,
  Capital Accumulation, and Inequality in the British Industrial Revolution", *Explorations in Economic History* 46(4)
  (2009): 418-435; J. Humphries, "The Lure of Aggregates and the Pitfalls of the Patriarchal Perspective", *Economic
  History Review* 66(3) (2013): 693-714; M. Kelly, J. Mokyr and C. Ó Gráda, "Precocious Albion: A New Interpretation of
  the British Industrial Revolution", *Annual Review of Economics* 6 (2014): 363-389.
- J. Mokyr, *The Enlightened Economy* (2009) and *A Culture of Growth* (2016); D. C. North and B. R. Weingast,
  "Constitutions and Commitment", *Journal of Economic History* 49(4) (1989): 803-832.
- N. F. R. Crafts and C. K. Harley, "Output Growth and the British Industrial Revolution: A Restatement of the
  Crafts-Harley View", *Economic History Review* 45(4) (1992): 703-730; N. Crafts, "Steam as a General Purpose
  Technology: A Growth Accounting Perspective", *Economic Journal* 114(495) (2004): 338-351; F. Engels, *The Condition of
  the Working Class in England* (1845).
- G. S. Becker and H. G. Lewis, "On the Interaction between the Quantity and Quality of Children", *Journal of Political
  Economy* 81(2) (1973): S279-S288; M. Kremer, "Population Growth and Technological Change: One Million B.C. to 1990",
  *Quarterly Journal of Economics* 108(3) (1993): 681-716; O. Galor and D. N. Weil, "Population, Technology, and Growth",
  *American Economic Review* 90(4) (2000): 806-828; O. Galor, *Unified Growth Theory* (2011).
- H.-J. Voth, *Time and Work in England 1750-1830* (2000); J. de Vries, "The Industrial Revolution and the Industrious
  Revolution", *Journal of Economic History* 54(2) (1994): 249-270.
- P. R. Ehrlich, *The Population Bomb* (1968); J. Tierney, "Betting on the Planet", *New York Times Magazine*,
  2 December 1990; United Nations, *World Population Prospects 2024*.
- D. Comin, W. Easterly and E. Gong, "Was the Wealth of Nations Determined in 1000 BC?", *American Economic Journal:
  Macroeconomics* 2(3) (2010): 65-97; E. Spolaore and R. Wacziarg, "The Diffusion of Development", *Quarterly Journal of
  Economics* 124(2) (2009): 469-529; M. Kelly, "The Standard Errors of Persistence" (2019 working paper); T. G. Conley,
  "GMM Estimation with Cross Sectional Dependence", *Journal of Econometrics* 92(1) (1999): 1-45.
- Our World in Data: population (HYDE, Gapminder, UN WPP), life expectancy (Riley; Zijdeman and Ribeira da Silva; HMD;
  UN WPP), children per woman (HFD; UN WPP), men's heights (Baten and Blum; NCD-RisC).
- Textbooks: David N. Weil, *Economic Growth*, chs. 4-5; Mark Koyama and Jared Rubin, *How the World Became Rich*
  (2022); Oded Galor, *The Journey of Humanity* (2022).
