# Economics, Built: Part 20, Growth I: Capital

Part 20 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second of Act V, *The Long Run*. It asks whether a country can save its way to being
rich, and answers: richer, yes; growing faster for ever, no. Saving raises the level of income, and East Asia's saving
and schooling were real achievements, but diminishing returns bring growth back to the rate of technology, as the
Soviet Union and, more gently, South Korea found. Across countries, capital and schooling explain well under half of
the gap between rich and poor; the rest is productivity, the residual the Solow model leaves out.

It opens with the two Koreas: in 1940 the north was the richer half; by 2022 the south's income per head was about 26
times the north's (Maddison Project). From there it covers:

- Kaldor's six facts (1961), checked on the Penn World Table 11.0 for the United States since 1950 and for 91 countries;
- Harrod (1939) and Domar (1946): growth from a fixed capital-output ratio, the knife edge, the planners' financing gap,
  and Easterly's (1999) test of it;
- the Solow model derived (Solow 1956; Swan 1956): the per-worker production function, the fundamental equation, the
  diagram, the steady state, the balanced growth path that explains five of Kaldor's facts, and the level effect of
  saving;
- a game: choose the island's saving rate for a century; the golden rule (Phelps 1961); a jump in saving from 15% to 30%;
- the speed of convergence, derived by linearizing, and simulated: 5% a year in the textbook, about 2% with a broad
  capital share;
- convergence in the data: none without controls before 2000 (Pritchett 1997), conditional convergence (Barro 1991),
  Mankiw, Romer and Weil (1992) fitted and refitted, Islam's panels (1995), Quah's clubs (1996);
- an intermission without narration: investment and income for 146 countries, 1960-2023, with South Korea's investment
  share as a tune;
- growth accounting: Solow's residual (1957), redone on the Penn World Table for the United States and eight countries;
- East Asia: Krugman (1994), Young (1995) and Hsieh (2002), with *Called it?* on Samuelson's textbook forecast of Soviet
  overtaking;
- development accounting: Hall and Jones (1999), Caselli (2005), and the same accounting for 134 countries in 2019;
- Lucas's question (1990): why capital does not flow to poor countries, redone on 2019 data;
- Ramsey's problem (1928; Cass 1965; Koopmans 1965): the Hamiltonian, the Euler equation, the phase diagram, and the
  saddle path found by shooting; the modified golden rule;
- China's growth in the model: investment, the capital-output ratio, the return on capital, accounting by period, and
  Song, Storesletten and Zilibotti (2011);
- a new dial (the speed of convergence) and a new row on another (capital's share), potential output and the long-term
  budget in practice, and a frontier chapter on the slowdown since 2005 and convergence since 2000 (Kremer, Willis and
  You 2022, and their critics).

## Build it

```bash
python -m videos.economics.econ20.compute              # every number (seconds), into .cache/econ20/
python tools/qa_scene.py econ20 Solow                  # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ20 -q l   # the whole part, silent preview
python tools/build.py econ20                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 20                     # the lab
```

The data are frozen extracts in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): the Penn World Table 11.0 (Feenstra, Inklaar and Timmer;
output, population, employment, hours, human capital, capital, labour shares, investment shares and the internal rate
of return) and the Maddison Project Database 2023 (the two Koreas and the former Soviet Union).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Can a country save its way to being rich? | The two Koreas (Maddison): north 2,624 and south 1,975 dollars a head in 1940; no estimates for the north from 1944 to 1989; 5.6 to 1 in 1990 and 26 to 1 in 2022; South Korea's investment 11% of GDP in 1960, 41% by 1990 (PWT); the question; Solow (1956); objectives |
| 1 | Kaldor's six facts, checked | United States 1950-2023 (PWT 11.0): output per worker +1.6% a year, capital per worker +1.5%, the internal return on capital 6-10% with no trend, capital 3.2-3.9 years of output, labour's share 63% (1950-79) and 59% (since 2010); growth of GDP per head 1960-2019 across 91 countries, from -1.8% (DR Congo) to 6.2% (China) |
| 2 | Harrod, Domar and the planners | $g = s/v - \delta$; the island (v = 3.5, δ = 3%) grows 2.7% saving a fifth; the knife edge $s^* = v(n+\delta) = 14\%$, with unemployment or idle machines on either side; the financing gap (35% needed for 7% growth); India's Second Plan; Easterly (1999): Zambia's predicted income about 20,000 dollars, actual about 600; predicted and actual growth correlated slightly negatively |
| 3 | The Solow model | $Y = K^{\alpha}(AL)^{1-\alpha}$; $\dot k = s k^{\alpha} - (n+g+\delta)k$; the diagram; the island's steady state ($s$ = 15%, $n$ = 1%, $g$ = 2%, δ = 5%): $k^*$ = 2.57, $y^*$ = 1.37, capital 1.9 years of output; the balanced path explains Kaldor's facts 1-5; doubling saving multiplies capital by 2.83 and output by 1.41 |
| 4 | Play it: how much should the island save? | Five saving rates for a century from 15%: 10% gives 13% less consumption in year 100, 20% 9% more, a third 17% more (overtaking in year 14), half 7% more (year 31), 70% 24% less; the golden rule $f'(k) = n+g+\delta$, $s = \alpha$ (Phelps 1961); dynamic inefficiency; a jump from 15% to 30% in year 10: growth peaks at 4.5%, half the gain in 10 years, then back to 2%, income 41% higher for good |
| 5 | How fast does an economy converge? | $\lambda = (1-\alpha)(n+g+\delta)$ = 5.3% a year, half-life 13 years (10 from a quarter of the steady state's capital, simulated); with a capital share of three quarters, 2% and 35 years (31 simulated); the 2% the regressions found |
| 6 | Do poor countries catch up? | 89 countries (PWT): growth 1960-90 on initial income, slope +0.0030 (s.e. 0.0014), divergence (Pritchett 1997); 1960-2019, -0.0009 (0.0014) without controls, -0.0089 (0.0030) holding investment, population growth and schooling fixed (Barro 1991): λ = 1.3%, half-life 55 years; MRW (1992): $R^2$ 0.59 but $\alpha \approx 0.59$; with human capital α = 0.31, β = 0.28, $R^2$ 0.78; λ = 1.37% (OECD 2.03%); Islam (1995) 5.1% with fixed effects; Nickell's bias; Quah's twin peaks; the fact entered |
| | Intermission: the world saves | No narration: investment share (five-year average) against GDP per head relative to the United States, 1960-2023, 146 countries, with seven named (PWT); South Korea's investment share as a tune, peaking at 50% in 1996 |
| 7 | Growth accounting: Solow's residual | $g_A = g_Y - \alpha g_K - (1-\alpha)(g_L + g_h)$; Solow (1957): output per man-hour doubled 1909-49, seven eighths technical change (Hogan's correction: 90%); Abramovitz's "measure of our ignorance"; the United States 1950-2019: output per hour 1.86% a year = capital deepening 0.61 + schooling 0.33 + residual 0.91 (49%); the residual 1.29% (1950-73), 0.51 (1973-95), 1.53 (1995-2005), 0.52 (2005-19); eight countries (China's residual 3.4% a year 1980-2019; Brazil's and Nigeria's zero or below); Jorgenson and Griliches (1967) |
| 8 | East Asia: perspiration or inspiration? | The Soviet Union (Maddison): 3.3% a year in the 1950s, 0.7% in the 1980s, never above 38% of America's income per head; *Called it?*: Samuelson's textbook (1961: overtaking between 1984 and 1997; 1980: between 2002 and 2012), wrong; Krugman (1994); Young (1995): residuals of 2.3% (Hong Kong), 0.2% (Singapore), 1.7% (Korea) and 2.6% (Taiwan); the same on the PWT (Singapore 0.5%, with capital 6.0 of its 8.7 points); Hsieh (2002): the dual residual more than 2 points higher for Singapore; Korea's growth of GDP per head by decade, 8.2% in the 1980s to 2.0% in the 2010s |
| 9 | Development accounting: why levels differ | $y = (K/Y)^{\alpha/(1-\alpha)} h A^{1/(1-\alpha)}$; Hall and Jones (1999): 31.7 = 1.8 × 2.2 × 8.3; 134 countries in 2019 (PWT): 90/10 ratios of 15.4 (income), 3.1 (factors), 7.1 (productivity); the factors' share of the variance of log income 0.16 (Hall-Jones form) and 0.30 (Caselli's), against 0.26 and 0.40 in Caselli's 1996 data; six countries relative to the United States (India: 0.14 = 1.07 × 0.58 × 0.23) |
| 10 | Why doesn't capital flow to poor countries? | Lucas (1990): a fifteenfold gap and α = 0.4 imply returns 58 times as high; about 5 with Krueger's skill differences; about 1 with spillovers; uphill flows (Prasad, Rajan and Subramanian 2007); 2019: a 7.2-fold gap predicts 19 times (8.5 with schooling); the PWT's internal returns, 12.1% in India and 7.9% in the United States, a ratio of 1.5 |
| 11 | Ramsey's problem: saving chosen | Ramsey (1928) and his refusal to discount; Cass and Koopmans (1965); the Hamiltonian and the Euler equation $\dot c/c = (\alpha k^{\alpha-1} - \delta - \rho - \theta g)/\theta$; the phase diagram; shooting from half the steady state's capital (misses at ±6%, bisection, $c_0$ = 0.951); the modified golden rule ($r$ = ρ + θg = 7%): $k^*$ = 4.63 against the golden rule's 8.51, saving 22% against a third |
| 12 | China's growth in the model | China 1960-2023 (PWT): investment 36% of GDP in 1978, 47% at its peak (2011); capital 3.4 years of output in 1978, 5.5 in 2023; the internal return rising to 1995, then falling; output per hour 7.4% a year 1980-95 (residual 4.1%), 8.3% 1995-2008 (3.7%), 7.4% 2008-19 (2.2%); Song, Storesletten and Zilibotti (2011); what the model says about the next decades |
| 13 | The Dials: how fast, and how much capital? | The new dial: the speed of convergence (MRW 1.37% and 2.03%; Islam 5.07%; this film 1.3%; Kremer, Willis and You 0.7%, unconditional), contested; half-lives; capital's share with MRW's 0.31 added; the United States' one minus labour share since 1950, 0.38 |
| 14 | In practice: potential output and the long-term budget | CBO's potential output built on a Solow model (2001); $g_Y = g_L + g_A/(1-\alpha)$: with hours +0.4% a year, 1.2% (the residual of 2005-19) or 1.9% (that of 1950-2019); debt dynamics $b' = b(1+r)/(1+g) + d$; Blanchard (2019); Ramsey's $r = \rho + \theta g > g$; Abel, Mankiw, Summers and Zeckhauser (1989); who does this work |
| 15 | Frontier: the slowdown, and convergence at last | US output per hour and residual by period; Fernald (2015); Syverson (2017); rolling ten-year convergence slopes, 1960-2009, from +0.005 to -0.0075; Kremer, Willis and You (2022): divergence of about 0.5% a year in 1985-95, convergence of about 0.7% in 2005-15; Acemoglu and Molina's comment; open questions |
| | Recap, problems, and the road ahead | The answer; twelve lines; problems; reading; Romer (1990), and Part 21 |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's growth module (`explainer.economics.agora.growth`), with the
Island's Part 20 truths in `explainer.economics.island`, or from the Data Room; the narration states the cached
numbers.

- **The Solow model.** The annual equation $k' = k + s k^{\alpha} - (n+g+\delta)k$, which shares the continuous model's
  steady state; the golden rule on a grid of saving rates; the speed of convergence linearized and simulated.
- **Harrod-Domar.** Capital and labour in fixed proportions growing at $s/v - \delta$ and $n$; the ratio of machines to
  the workers needed to man them.
- **Convergence.** OLS of average log growth on initial log GDP per head (PWT `rgdpna`/`pop`), countries of a million
  people or more with 80% of investment shares present; the conditional version adds log mean investment share, log
  ($n$ + 0.05) and log human capital at the start; HC1 standard errors; the implied
  $\lambda = -\ln(1 + bT)/T$; Frisch-Waugh partial residuals for the picture; rolling ten-year windows.
- **Accounting.** Growth of real GDP (`rgdpna`), capital (`rnna`), hours (`emp` × `avh`) and human capital (`hc`), with
  α one minus the average labour share (`labsh`); development accounting with α = 1/3 on 2019 levels (`rgdpo`, `emp`,
  `cn`, `hc`).
- **Ramsey.** The two differential equations per effective worker, integrated by Euler's method; the initial
  consumption found by 80 bisections between paths that crash and paths that overaccumulate.

## Problems and solutions

**1.** *The steady state: with $y = k^{\alpha}$ and $\dot k = s k^{\alpha} - (n+g+\delta)k$, find $k^*$, $y^*$ and
$c^*$, and show that capital is $s/(n+g+\delta)$ years of output.*

*Solution.* Setting $\dot k = 0$ gives $s k^{\alpha} = (n+g+\delta)k$, so $k^* = (s/(n+g+\delta))^{1/(1-\alpha)}$,
$y^* = (k^*)^{\alpha} = (s/(n+g+\delta))^{\alpha/(1-\alpha)}$ and $c^* = (1-s)y^*$. The capital-output ratio is
$k^*/y^* = (k^*)^{1-\alpha} = s/(n+g+\delta)$. On the island, $s = 0.15$ and $n+g+\delta = 0.08$: $k^* = 1.875^{1.5}
\approx 2.57$, $y^* \approx 1.37$, $c^* \approx 1.16$, and capital is 1.875 years of output.

**2.** *The golden rule: show that steady-state consumption is largest when $f'(k) = n+g+\delta$, that this means
$s = \alpha$ for Cobb-Douglas, and find the island's consumption at 15% and at a third.*

*Solution.* In a steady state $c^* = f(k^*) - (n+g+\delta)k^*$. Each saving rate picks a $k^*$, so maximize over $k^*$:
$f'(k) = n+g+\delta$. With $f(k) = k^{\alpha}$, $\alpha k^{\alpha-1} = n+g+\delta$, and since
$s = (n+g+\delta)k^{1-\alpha}$ in a steady state, $s = (n+g+\delta) \cdot \alpha/(n+g+\delta) = \alpha$. At 15%,
$c^* = 0.85 \times 1.875^{0.5} \approx 1.164$; at a third, $c^* = (2/3)(4.17)^{0.5} \approx 1.361$, 17% more.

**3.** *Levels, not growth: show that doubling $s$ multiplies $y^*$ by $2^{\alpha/(1-\alpha)}$, and that output per
worker grows at $g$ in both steady states.*

*Solution.* From problem 1, $y^* \propto s^{\alpha/(1-\alpha)}$, so doubling $s$ multiplies it by $2^{\alpha/(1-\alpha)}$:
with $\alpha = 1/3$, $\sqrt 2 \approx 1.41$. Output per worker is $Y/L = A y$; in any steady state $y$ is constant, so
$Y/L$ grows at the rate of $A$, $g$, whatever $s$ is. During the transition growth is faster (the island's peaks at about
4.5%), and it returns to $g$ as the gap closes.

**4.** *The speed: linearize the Solow equation in $\ln k$, find $\lambda = (1-\alpha)(n+g+\delta)$, and the half-lives
for $\alpha = 1/3$ and $\alpha = 3/4$ when $n+g+\delta = 8\%$.*

*Solution.* Write $x = \ln k$: $\dot x = s e^{(\alpha-1)x} - (n+g+\delta)$. Its derivative with respect to $x$ at the
steady state, where $s e^{(\alpha - 1)x^*} = n+g+\delta$, is $(\alpha - 1)(n+g+\delta)$, so
$\dot x \approx -(1-\alpha)(n+g+\delta)(x - x^*)$. Since $\ln y = \alpha \ln k$, $\ln y$ closes its gap at the same
rate. With $\alpha = 1/3$, $\lambda = 0.0533$ and the half-life $\ln 2/\lambda \approx 13$ years; with $\alpha = 3/4$,
$\lambda = 0.02$ and about 35 years.

**5.** *Growth accounting: output grows 3.1%, capital 2.8%, hours 1.2% and schooling 0.5% a year, with $\alpha = 0.38$:
find the residual and its share of growth per hour.*

*Solution.* $g_A = 3.1 - 0.38 \times 2.8 - 0.62 \times (1.2 + 0.5) = 3.1 - 1.064 - 1.054 = 0.98\%$ a year. Output per
hour grows $3.1 - 1.2 = 1.9\%$, so the residual is about 52% of it; the rest is capital deepening,
$0.38 \times (2.8 - 1.2) = 0.61$, and schooling, $0.62 \times 0.5 = 0.31$. These are close to the United States'
numbers for 1950-2019 on the Penn World Table.

**6.** *Development accounting: derive $y = (K/Y)^{\alpha/(1-\alpha)}\,h\,A^{1/(1-\alpha)}$, and explain why capital
intensity is measured by $K/Y$ rather than $K/L$.*

*Solution.* Per worker, $y = A k^{\alpha} h^{1-\alpha}$. Divide both sides by $y^{\alpha}$:
$y^{1-\alpha} = A (k/y)^{\alpha} h^{1-\alpha}$, and raise to $1/(1-\alpha)$:
$y = A^{1/(1-\alpha)} (K/Y)^{\alpha/(1-\alpha)} h$. In the Solow model a country with higher $A$ accumulates more
capital per worker, in proportion to its output, so $K/L$ is partly a consequence of $A$; the steady-state $K/Y$,
$s/(n+g+\delta)$, does not depend on $A$. Writing the decomposition with $K/Y$ credits that induced capital to
productivity, which is where it comes from.

**7.** *Lucas: with $y = A k^{\alpha}$, the same $A$ and $\alpha = 0.4$, show that a fifteenfold income gap implies
returns 58 times as high, and about 5 when workers differ fivefold in skill.*

*Solution.* $r = \alpha A k^{\alpha - 1}$ and $k = (y/A)^{1/\alpha}$, so $r = \alpha A^{1/\alpha} y^{(\alpha-1)/\alpha}$.
With the same $A$, $r_{\text{poor}}/r_{\text{rich}} = (y_{\text{rich}}/y_{\text{poor}})^{(1-\alpha)/\alpha} = 15^{1.5}
\approx 58$. If an American worker supplies five times the effective labour, output per effective worker differs only
$15/5 = 3$ times, and the ratio is $3^{1.5} \approx 5.2$. On 2019 data the income gap is about 7.2 and the predicted
ratio about 19, or 8.5 with measured schooling; the Penn World Table's internal returns differ by a factor of about 1.5.

**8.** *$\bigstar$ Ramsey: derive the Euler equation from the Hamiltonian, the modified golden rule, and show that an
optimizing economy never saves beyond the golden rule.*

*Solution.* Per effective worker, the objective is $\int_0^\infty e^{-\beta t} c^{1-\theta}/(1-\theta)\,dt$ with
$\beta = \rho - n - (1-\theta)g$ (population growth and technology folded into the discount rate). With
$H = c^{1-\theta}/(1-\theta) + \mu[k^{\alpha} - c - (n+g+\delta)k]$, the conditions are $c^{-\theta} = \mu$ and
$\dot\mu = \beta\mu - \partial H/\partial k = \mu[\beta + n + g + \delta - \alpha k^{\alpha-1}]$. Differentiating the first,
$-\theta \dot c/c = \dot\mu/\mu = \rho + \theta g + \delta - \alpha k^{\alpha-1}$, so
$\dot c/c = (\alpha k^{\alpha-1} - \delta - \rho - \theta g)/\theta$. In the steady state $\dot c = 0$, so
$f'(k^*) - \delta = \rho + \theta g$: the modified golden rule. The golden rule has $f'(k_{\text{gold}}) - \delta = n + g$.
The objective is finite only if $\beta > 0$, that is $\rho + \theta g > n + g$, so $f'(k^*) > f'(k_{\text{gold}})$ and,
since $f'$ falls, $k^* < k_{\text{gold}}$. On the island, $r = 0.03 + 2 \times 0.02 = 7\%$, $k^* = 4.63$ against 8.51, and the
saving rate is 22% against a third.

## Where it comes back

| Idea | Parts |
|---|---|
| Ideas, the residual and endogenous growth | 21 *Growth II: Ideas and Institutions* |
| The Euler equation and consumption | 22 *Consumption and Saving* |
| The neutral rate and the output gap | 30 *Sticky Prices* |
| Labour's share | 39 *The Wage Structure* |
| Development and the dial on convergence | 46 *Development* |
| Ramsey's machinery and the price of carbon | 48 *Environment and Climate* |

## Sources

- R. F. Harrod, "An Essay in Dynamic Theory", *Economic Journal* 49(193) (1939); E. D. Domar, "Capital Expansion, Rate
  of Growth, and Employment", *Econometrica* 14(2) (1946); W. Easterly, "The ghost of financing gap", *Journal of
  Development Economics* 60(2) (1999): 423-438; W. Easterly, *The Elusive Quest for Growth* (2001).
- R. M. Solow, "A Contribution to the Theory of Economic Growth", *QJE* 70(1) (1956); T. W. Swan, "Economic Growth and
  Capital Accumulation", *Economic Record* 32 (1956); R. M. Solow, "Technical Change and the Aggregate Production
  Function", *REStat* 39(3) (1957): 312-320; M. Abramovitz, *AER* 46(2) (1956); N. Kaldor, "Capital Accumulation and
  Economic Growth", in Lutz and Hague (eds), *The Theory of Capital* (1961); E. S. Phelps, "The Golden Rule of
  Accumulation", *AER* 51(4) (1961): 638-643; D. W. Jorgenson and Z. Griliches, *REStud* 34(3) (1967).
- F. P. Ramsey, "A Mathematical Theory of Saving", *Economic Journal* 38(152) (1928); D. Cass, *REStud* 32(3) (1965);
  T. C. Koopmans, "On the Concept of Optimal Economic Growth" (1965).
- R. J. Barro, *QJE* 106(2) (1991); N. G. Mankiw, D. Romer and D. N. Weil, *QJE* 107(2) (1992): 407-437; N. Islam,
  *QJE* 110(4) (1995): 1127-1170; S. Nickell, *Econometrica* 49(6) (1981); D. Quah, *EJ* 106(437) (1996); L. Pritchett,
  "Divergence, Big Time", *JEP* 11(3) (1997).
- P. Krugman, "The Myth of Asia's Miracle", *Foreign Affairs* 73(6) (1994); A. Young, "The Tyranny of Numbers", *QJE*
  110(3) (1995): 641-680; C.-T. Hsieh, *AER* 92(3) (2002): 502-526; D. M. Levy and S. J. Peart, "Soviet growth and
  American textbooks", *Journal of Economic Behavior & Organization* 78(1-2) (2011): 110-125.
- R. E. Hall and C. I. Jones, *QJE* 114(1) (1999): 83-116; F. Caselli, "Accounting for Cross-Country Income
  Differences", *Handbook of Economic Growth* 1A (2005); R. E. Lucas, "Why Doesn't Capital Flow from Rich to Poor
  Countries?", *AER* 80(2) (1990): 92-96; E. Prasad, R. Rajan and A. Subramanian, *Brookings Papers* (2007).
- Z. Song, K. Storesletten and F. Zilibotti, "Growing Like China", *AER* 101(1) (2011): 196-233.
- CBO, *CBO's Method for Estimating Potential Output: An Update* (2001); O. Blanchard, "Public Debt and Low Interest
  Rates", *AER* 109(4) (2019); A. B. Abel, N. G. Mankiw, L. H. Summers and R. J. Zeckhauser, "Assessing Dynamic
  Efficiency", *REStud* 56(1) (1989).
- J. Fernald, *NBER Macroeconomics Annual* 29 (2015); C. Syverson, *JEP* 31(2) (2017); M. Kremer, J. Willis and Y. You,
  "Converging to Convergence", *NBER Macroeconomics Annual* 36 (2022): 337-412; D. Acemoglu and C. Molina, "Converging
  to Converge? A Comment", same volume.
- R. C. Feenstra, R. Inklaar and M. P. Timmer, "The Next Generation of the Penn World Table", *AER* 105(10) (2015),
  Penn World Table 11.0; J. Bolt and J. L. van Zanden, Maddison Project Database 2023.
