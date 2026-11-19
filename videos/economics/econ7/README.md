# Economics, Built: Part 7, Time and Risk

Part 7 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third of Act II, *Choosing*. It asks how people choose when the pay-off comes
later, or may not come at all, and answers: by weighing. Later is weighed against now with a discount factor and the
interest rate; chances are weighed against outcomes with a utility function that bends. The theory is coherent and
useful: it prices insurance, pensions and assets. But people break it in systematic ways. They care about what two
options share, about whether the odds are known, about small stakes and about the present moment more than the theory
allows, and the numbers that measure them depend on how they are asked.

It opens with the St Petersburg game: a coin is tossed until it lands heads, and the prize, $1 on the first toss,
doubles with every tail. Its expected prize is infinite; a million simulated games show the average creeping up for
ever. Nicolaus Bernoulli posed it in 1713, Gabriel Cramer answered with the square root of money in 1728, and Daniel
Bernoulli published the logarithm in St Petersburg in 1738: the first utility function. The viewer names a price,
and the part scores Bernoulli's against what people actually pay. From there it covers:

- Fisher's two periods (1930): the interest rate as the price of now, the Euler equation, the elasticity of
  intertemporal substitution, and how saving responds to a higher rate for three choosers;
- discounting: present values, Samuelson's discounted utility (1937) with his own two caveats, Koopmans's axioms,
  and why only exponential discounting is time consistent;
- lotteries and expected utility: the von Neumann–Morgenstern axioms, independence, and the probability triangle with
  its straight, parallel indifference lines;
- a game: Allais's two pairs, chosen by the viewer, then the algebra and the triangle that show why the common answers
  break independence, and the lunch in Paris in 1952 where Savage gave them;
- risk aversion: certainty equivalents and risk premia for a fisher choosing between the reef and the open sea;
  Arrow and Pratt's measures and the premium as half the aversion times the variance; CARA against CRRA;
- insurance and the risky asset: Mossin's full cover at fair odds, partial cover under a loading, the absurd risk
  aversion that cheap deductibles imply, and Merton's share in a risky asset;
- an intermission without narration: Hall's question, ninety-one years of America's real Treasury bill rate against
  the growth of consumption per head, under the real rate as a tune;
- stochastic dominance of first and second order, and Rothschild and Stiglitz's mean-preserving spreads;
- the paradoxes: Machina's fanning out (drawn with Chew's weighted utility), Ellsberg's urn, maxmin expected utility,
  and prospect theory in one card;
- Rabin's calibration theorem, with the power function computed and his tables transcribed;
- time meets risk: one gamma for two attitudes, the plane of estimates, Epstein–Zin preferences and a preference for
  early resolution, the equity premium and risk-free rate puzzles;
- present bias: Thaler's survey, preference reversals, Strotz, beta–delta, a dry-season store eaten faster than
  planned, and the value of commitment;
- measuring it: Holt and Laury's menu and its stakes, the same menu run on 400 simulated islanders with the truth
  planted, the HRS's income gambles, Deal or No Deal; *Called it?*: Bernoulli's price, partly right;
- two new dials (relative risk aversion; the elasticity of intertemporal substitution), insurance pricing and pooling,
  pension defaults and Save More Tomorrow, the discount rate as a value judgment, and a frontier chapter on ambiguity,
  robustness and stated beliefs.

## Build it

```bash
python -m videos.economics.econ7.compute              # every number (seconds), into .cache/econ7/
python tools/qa_scene.py econ7 Rabin                  # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ7 -q l   # the whole part, silent preview
python tools/build.py econ7                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 7                     # the lab
```

The data are frozen extracts in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): real personal consumption expenditures, the PCE price
index and the population (BEA), and the 3-month Treasury bill rate (the Federal Reserve Board), all from FRED. The
published results (Bernoulli; Samuelson; Allais and Kahneman and Tversky; Ellsberg; Rabin; Thaler; Holt and Laury;
Hayden and Platt; Madrian and Shea; Thaler and Benartzi; Barsky et al.; Post et al.; Mehra and Prescott) are
transcribed in `explainer/economics/data/tables.py`, each with where it was read and the date it was checked.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | How do people choose when the pay-off comes later, or may not come at all? | The St Petersburg game played: $1, $2, $4, …; each ending worth 50 cents, the expected prize infinite; a pause to name a price; a million simulated games: half pay $1, 87.5% pay $4 or less, the largest $524,288, the average about $11 and still creeping up like ½ log₂ n + 1; Nicolaus Bernoulli (1713), Cramer (1728, about 2.9), Daniel Bernoulli (1738): $4.36 with $100, $5.97 with $1,000, $10.94 with $1 million; the question; the title; objectives; not financial advice |
| 1 | Fisher's two periods | Fisher (1930); Chidi's harvest, $120 now and $40 in the dry season; Dara lends at 10%; the budget line, c₁ + c₂/1.1 = $156.36; β = 0.9, γ = 2: c₁ = 82.1, c₂ = 81.7, lending $37.90; the Euler equation and c₂/c₁ = (β(1 + r))^(1/γ); the EIS = 1/γ; the rate rises to 30%: substitution −3.1, income +3.3, saving barely moves (a magnified view); saving from 0% to 50% for EIS 2 (31.6 → 53.8), ½ (flat), ⅛ (39.5 → 33.3) |
| 2 | Discounting | Σ βᵗ u(cₜ); $100 in 30 years: $41.20 at 3%, $5.73 at 10%; Samuelson (1937): "completely arbitrary" and "disavowed"; Koopmans (1960); exponential, hyperbolic and beta–delta discount functions and the price of a year's wait, D(t+1)/D(t): constant only for the exponential |
| 3 | Lotteries and expected utility | Ana's reef ($60 sure) and open sea ($20 or $140): averages $60 and $80; expected utility with $40 at home; von Neumann and Morgenstern's axioms, independence above all; the theorem and uniqueness up to a + bu; the triangle on $0, $1M, $5M: straight parallel lines, slope (u(1M) − u(0))/(u(5M) − u(1M)), 0.25 for risk neutrality, 9 for a risk averter |
| 4 | Play it: Allais's two pairs | 1A ($1M sure) or 1B (10% $5M, 89% $1M, 1% nothing); 2A (11% $1M) or 2B (10% $5M); countdowns; the common answers 1A and 2B; Kahneman and Tversky (1979): 82% took the sure thing in their first pair; the algebra: the same difference 0.11u(1M) − 0.10u(5M) − 0.01u(0); the triangle: two parallel moves of slope 10 against parallel lines; Allais and Savage at lunch, Paris, May 1952; description or advice? |
| 5 | Risk aversion | u = −1/x: the sea leaves $60 or $180, average $120, certainty equivalent $90, risk premium $30; the reef's $100 wins; certainty equivalents for γ = 0, 1, 2, 4: $120, $103.92, $90, $74.68; the switch at γ = 1.26; Arrow (1965) and Pratt (1964): A = −u″/u′, R = xA; premium ≈ ½Aσ², almost exact for small bets under the logarithm, 13% low at ±$80; CARA's constant premium against CRRA's falling one, for ±$20 as wealth grows |
| 6 | Insurance and the risky asset | Ana's $150 boat out of $300, a storm one year in ten, fair cover $15; her expected utility against cover: 100% at a fair price (Mossin 1968), 81% at a 20% loading, 61% at 50%; the most she pays for full cover, $27.27; deductibles for a $100,000 household with a claim one year in twenty: $500 against $1,000 saves $25 a year on average, and paying $30, $50 or $100 more needs γ ≈ 26, 98, 203 (Sydnor 2010); Dara's venture (+28% or −12%, safe 2%): best shares 82% (γ = 2) and 40% (γ = 4); Merton's (μ − r)/(γσ²): 150%, 75%, 37.5%, 15% for γ = 1, 2, 4, 10 |
| | Intermission: a century of the Euler equation | No narration: one dot a year, 1935–2025, the real 3-month bill rate (bill rate minus PCE inflation) against the growth of real consumption per head, coloured by era; 1942's rationing, 1946's demobilization, 2021's reopening; the fitted slope 0.07, correlation 0.10; instrumented by the rate and growth two years back and the nominal rate a year back, −0.02 (s.e. 0.11, first-stage F 23): the EIS about zero; the real rate as a tune; the story so far |
| 7 | Stochastic dominance | Three nets: old (2, 6, 10 fish), better (4, 6, 10), wide (0, 6, 12), chances ¼, ½, ¼; CDFs: first-order dominance and every increasing utility; integrated CDFs: the wide net is a mean-preserving spread (Rothschild and Stiglitz 1970), second-order dominated; certainty equivalents for γ = 0.5, 2, 5: 5.87, 5.48, 4.73 against 5.71, 4.79, 3.13 |
| 8 | Allais and Ellsberg in the triangle | Machina's fanning out (1982); Chew's weighted utility with illustrative weights: slope 17 at 1A, 0.83 at 2A, so 1A beats 1B and 2B beats 2A; Ellsberg's urn (30 red, 60 black or yellow) and bets I–IV (1961): "a very frequent pattern … I preferred to II, and IV preferred to III"; no single probability can do it; maxmin expected utility (Gilboa and Schmeidler 1989) with p(black) in [0, ⅔]: 0.33, 0.00, 0.33, 0.67; Knight's risk and uncertainty; prospect theory in one card: Tversky and Kahneman's α = 0.88, λ = 2.25, γ = 0.61 |
| 9 | Rabin's calibration | Lose $100 or win $110: a γ = 2 chooser with $100,000 is indifferent at a gain of $100.20; the γ that refuses it: 9, 91, 273, 908 at $10,000, $100,000, $300,000, $1 million; at γ = 91 and $100,000, lose $400 or win up to $634, lose $600 or win up to $1,416, lose $800 or more and win any sum: refused; Rabin's theorem (2000) and his table I (550; 990; 2,090; any sum); table II: lose $1,000 or win $718,190, refused; the moral: loss aversion and narrow framing; Rabin and Thaler's dead parrot (2001) |
| 10 | Time meets risk: substitution against aversion | One γ for risk across states and 1/γ for substitution across time; the (EIS, aversion) plane on log scales: expected utility's line, the dials' estimates on each axis, Bansal and Yaron's (1.5, 10); Barsky et al.: unrelated across people; Epstein–Zin (1989) after Kreps and Porteus (1978); early resolution: Bansal and Yaron's chooser pays 6.0% of today's consumption to learn early, γ = 5 and ψ = ½ pays 4.2%, expected utility nothing, γ = ψ = ½ prefers to learn late; the rule γ > 1/ψ; Mehra and Prescott (1985), Weil (1989); Part 23 |
| 11 | Present bias | Thaler (1981): $15 now against $20 in a month, $50 in a year, $100 in ten years: 345%, 120% and 19% a year; $100 today or $110 tomorrow against the same a month ahead; Strotz (1955–56); beta–delta (Laibson 1997); Chidi's 300 coconuts over six weeks, β = 0.7: planned 66.7 then 46.7 a week, eaten 66.7, 61.4, 55.5, 48.5, 40.0, 28.0; Pollak (1968); a locked box worth 2.8% of the store to week 1's self; Golden Eggs; β ≈ 0.95–0.97 (Imai, Rutter and Camerer 2021) |
| 12 | Measuring it | Holt and Laury's menu (2002) and its CRRA brackets (4 safe choices: −0.14 to 0.15; 5: 0.15–0.41; 6: 0.41–0.68; 7: 0.68–0.97); their table (2005): real 5.2, 6.0, 6.8, 7.2 safe choices at 1, 20, 50, 90 times; hypothetical 4.9, 5.1, 5.3; the 2004 rerun 5.7 → 6.7; 400 islanders with γ ~ N(0.35, 0.35) and noisy choices: 16% switch back, scored mean 0.36 against 0.35, correlation 0.85; the HRS gambles' thresholds γ = 1, 2, 3.76 and mean risk tolerance 0.25; Deal or No Deal; *Called it?*: Bernoulli against Hayden and Platt (2009), median bids $1.75 (real, 20) and $1.50 (hypothetical, 220), flat across truncations whose log prices run $2.50 to $5.95: partly right |
| 13 | The Dials: how risk averse, how willing to wait? | Relative risk aversion (new), on a log scale: Holt and Laury 0.28 and 0.83, Chetty 1.0, Elminejad, Havranek and Irsova 1.0 (economics), 4.5 (2–7, finance), median 3.77, Barsky et al. 4.0, calibrations 6.0 and 10: contested; the EIS (new): Hall 0, Barsky 0.2, Vissing-Jørgensen 0.35 and 0.9, Gruber 2.0, Havranek 0 (macro) and 0.35 (asset holders), Bansal and Yaron 1.5; ours 0.07 and −0.02: contested |
| 14 | In practice: insurance and pensions | Pooling: one boat's claims $15 ± $45, ten thousand boats' $15 ± $0.45; correlated risk, reinsurance and catastrophe bonds; adverse selection (Part 13); Madrian and Shea: 86% enrolled by default against 37%, 76% at the 3% default; Save More Tomorrow: 3.5% → 13.6% in 40 months; Ramsey's r = ρ + ηg; $100 of damage in 2100: $47.41 at 1%, $2.58 at 5%; the is/ought card; Stern and Nordhaus; Part 48 |
| 15 | Frontier: ambiguity, robustness, beliefs | Dara's venture under maxmin (the share falls from 82% to nothing at fifteen points of doubt) and Hansen and Sargent's multiplier preferences (6% to 81% as θ grows); Manski (2004); Hurd and McGarry (2002): survivors' stated chances about 50% higher; the Global Preference Survey (Falk et al. 2018): 80,000 people in 76 countries; open questions |
| | Recap, problems, and the road ahead | The answer; twelve lines; problems; reading; Douglas and Cobb, and Part 8 |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's time and risk (`explainer.economics.agora.risk`), with the
Island's Part 7 truths in `explainer.economics.island`, or from the Data Room or a transcribed table; the narration
states the cached numbers.

- **The St Petersburg game.** Prizes $2^(k−1)$ with chance $2^{−k}$; a million games from a seeded generator; the
  running average at 240 log-spaced points. Bernoulli's price c at wealth w solves Σ 2^(−k) log(w − c + prize_k) =
  log w (and the square root for Cramer), summed to 200 tosses. The truncated games follow Hayden and Platt: n tosses,
  and the maximum prize if no heads; their expected values ($2.50, $3.50, $5, $6, $8.50) are asserted against the
  transcription.
- **Fisher's chooser.** u(c₁) + βu(c₂) with CRRA utility, maximized on c₁ + c₂/(1 + r) = y₁ + y₂/(1 + r), in closed
  form; Hicks's compensated point on the old curve at the new slope.
- **Lotteries.** Certainty equivalents by inverting CRRA or CARA expected utility; the Arrow–Pratt measures by central
  differences; the triangle's expected-utility lines p₅ = c + slope·p₀; Chew's weighted utility V = Σ pᵢwᵢuᵢ/Σ pᵢwᵢ
  with u = (0, 0.85, 1) and w = (6, 1, 2), whose indifference lines are straight and meet at a point.
- **Insurance and portfolios.** Expected utility over a grid of cover shares and portfolio shares; the deductible's
  risk aversion by root-finding on the CRRA chooser's indifference; Merton's share in closed form.
- **Rabin.** The CRRA γ that makes a chooser indifferent to lose l / gain g at wealth w (root-finding on wealth
  relative to w, so no power overflows), and the largest gain still refused for each loss, infinite once
  (1 − L/w)^(1−γ) ≥ 2.
- **Epstein–Zin.** A three-date recursion with consumption 1, 1 and then 0.8 or 1.2; early resolution aggregates the
  certainty equivalent of next season's value, late resolution the certainty equivalent of consumption itself; the
  premium is the share of today's consumption that equates them.
- **Present bias.** Log utility over a cake of 300 coconuts and six weeks, with weights 1, β, β, …; each week's self
  eats the share 1/(1 + β(n − 1)) of what is left; the commitment's worth is the share of the whole store that makes
  week 1's self indifferent between the plan and what happens.
- **The Island's Holt–Laury study.** 400 γs drawn N(0.35, 0.35) (seed 2002); each row chosen with probability
  Λ((CE_A − CE_B)/$0.20); respondents who switch back are set aside, the rest scored by the midpoint of their bracket.
- **Hall's regression.** Annual real consumption per head from PCECCA and the population; PCE inflation from the
  annual PCE price index; the 3-month bill rate averaged over each year; the ex post real rate is the bill rate minus
  inflation. OLS of growth on the rate, and 2SLS with the rate and growth two years back and the nominal rate a year
  back as instruments (as Hall argued, time-averaged data need lags of two years), 1937–2025.
- **Robustness.** Dara's venture with γ = 2: maxmin over chances 0.5 ± ε, and Hansen and Sargent's multiplier
  criterion −θ log E[exp(−u/θ)], each maximized over a grid of shares.

## Problems and solutions

**1.** *Fisher: incomes $120 and $40, r = 10%, β = 0.9, u = −1/c. Find c₁, c₂ and saving, and check the Euler
equation. How does saving change at r = 30%?*

*Solution.* With γ = 2 the Euler equation c₁^(−2) = β(1 + r)c₂^(−2) gives c₂/c₁ = (0.99)^(1/2) = 0.995. Wealth is
120 + 40/1.1 = 156.36, so c₁(1 + 0.995/1.1) = 156.36: c₁ = 82.10, c₂ = 81.69, and Chidi lends 37.90. At 30%, wealth
falls to 150.77 and c₂/c₁ = 1.17^(1/2) = 1.082, so c₁ = 82.30 and saving is 37.70: the substitution effect (−3.1) and
the lender's income effect (+3.3) almost cancel.

**2.** *Show that only exponential discounting makes D(t + 1)/D(t) the same at every t. What is it for 1/(1 + t)?*

*Solution.* If D(t + 1)/D(t) = k for every t, then D(t) = D(0)kᵗ by induction: exponential. Conversely the
exponential gives the constant e^(−ρ). For D(t) = 1/(1 + t) the ratio is (1 + t)/(2 + t): a half for a wait that
starts now, 0.95 for one that starts in nineteen years, rising toward one. A year's wait looks expensive when it
starts today and cheap when it starts later, which is the preference reversal of chapter 11.

**3.** *Ana: $60 or $180, 50–50, against $100 for sure. Find the certainty equivalent for γ = 1 and 2, and the γ at
which she is indifferent.*

*Solution.* For γ = 1 the certainty equivalent is the geometric mean, √(60·180) = 103.92 > 100: the sea. For γ = 2 it
is the harmonic mean, 2/(1/60 + 1/180) = 90 < 100: the reef. Indifference solves ½(60^(1−γ) + 180^(1−γ)) =
100^(1−γ), which has no closed form; numerically γ = 1.26.

**4.** *Allais: show EU(1A) − EU(1B) = EU(2A) − EU(2B) for every u. Draw the four lotteries in the triangle.*

*Solution.* EU(1A) − EU(1B) = u(1M) − [0.10u(5M) + 0.89u(1M) + 0.01u(0)] = 0.11u(1M) − 0.10u(5M) − 0.01u(0), and
EU(2A) − EU(2B) = [0.11u(1M) + 0.89u(0)] − [0.10u(5M) + 0.90u(0)] = the same. In the triangle (chance of $0 across,
of $5M up) the lotteries are 1A (0, 0), 1B (0.01, 0.10), 2A (0.89, 0) and 2B (0.90, 0.10): the moves from A to B are
parallel, with slope 10, so straight parallel indifference lines rank both pairs the same way.

**5.** *Insurance: wealth $300, a $150 loss with chance 0.1, γ = 2. Find the most Ana pays for full cover, and show
that with a positive loading she buys less than full cover.*

*Solution.* Uninsured, her certainty equivalent solves 1/CE = 0.9/300 + 0.1/150, so CE = 272.73 and she would pay up
to 300 − 272.73 = $27.27 for full cover, against a fair premium of $15. With cover q at price (1 + λ)pLq, the
derivative of expected utility at q = 1, where wealth is the same in both states, is pL u′(w − P)[1 − (1 + λ)] =
−λpL u′ < 0: with any loading λ > 0 she gains by insuring a little less than everything (Mossin 1968).

**6.** *A risky asset: premium 6 points, s.d. 20%. Merton's share for γ = 2 and 10. What γ makes a household hold 25%
in it?*

*Solution.* (μ − r)/(γσ²) = 0.06/(0.04γ) = 1.5/γ: 75% at γ = 2 and 15% at γ = 10. A share of 25% needs γ = 6. (The
two-outcome venture of chapter 6 gives 82% and 40% at γ = 2 and 4, close to the formula's 75% and 37.5%.)

**7.** *Rabin: a CRRA chooser with $100,000 rejects lose $100 / win $110. Show γ ≈ 90, and that she rejects lose
$1,000 / win any sum.*

*Solution.* For a small bet, expected utility changes by about u′(w)[½(g − l) − (γ/4w)(g² + l²)], so indifference
needs γ ≈ 2w(g − l)/(g² + l²) = 2·100,000·10/22,100 = 90.5 (exactly 90.8). With γ > 1 utility is bounded above, and a
50–50 bet of losing L is refused for every gain when ½[(1 + G/w)^(1−γ) + (1 − L/w)^(1−γ)] ≥ 1 for all G, that is when
(1 − L/w)^(1−γ) ≥ 2. For L = $1,000, (0.99)^(−89.8) = 2.47 > 2: refused, whatever G.

**8.** ★ *Hall's regression uses instruments lagged two years. Simulate monthly consumption that obeys the Euler
equation exactly, average it to years, and show why one lag is not enough.*

*Solution.* Let log consumption be a monthly random walk, the Euler equation with a constant rate. Annual averages of a
random walk have growth rates that are serially correlated (Working 1960): the change from one year's average to the
next shares the months near the boundary with the change before it, and for a random walk sampled finely the first
autocorrelation of the averaged changes is about 0.25. So this year's growth surprise is correlated with last year's
growth, and any instrument dated last year is correlated with the error; instruments dated two years back are not.
The simulation shows the first-order autocorrelation near 0.25 and the second near zero; a one-lag IV is biased, a
two-lag IV is not. This is the reason for the lags in the intermission's instrumented slope.

## Where it comes back

| Idea | Parts |
|---|---|
| The Euler equation and the EIS | 20 *Growth I: Capital* (Ramsey's problem), 22 *Consumption and Saving*, 30 *Sticky Prices* (the dynamic IS curve) |
| Risk aversion, the equity premium and the risk-free rate puzzle | 23 *Capital and Asset Prices* |
| Insurance, adverse selection and moral hazard | 13 *Lemons and Signals*, 14 *Incentives*, 42 *Social Insurance* |
| Prospect theory, loss aversion, present bias | 45 *Behavioural Economics* |
| The discount rate as a value judgment | 48 *Environment and Climate* |

## Sources

- D. Bernoulli, "Specimen Theoriae Novae de Mensura Sortis", *Commentarii Academiae Scientiarum Imperialis
  Petropolitanae* 5 (1738) 175–192; "Exposition of a New Theory on the Measurement of Risk", trans. L. Sommer,
  *Econometrica* 22(1) (1954) 23–36; the Stanford Encyclopedia of Philosophy, "The St. Petersburg Paradox".
- B. Y. Hayden and M. L. Platt, "The mean, the median, and the St. Petersburg paradox", *Judgment and Decision Making*
  4(4) (2009) 256–272.
- I. Fisher, *The Theory of Interest* (Macmillan, 1930).
- P. A. Samuelson, "A Note on Measurement of Utility", *Review of Economic Studies* 4(2) (1937) 155–161, as quoted by
  S. Frederick, G. Loewenstein and T. O'Donoghue, "Time Discounting and Time Preference: A Critical Review", *Journal
  of Economic Literature* 40(2) (2002) 351–401; T. C. Koopmans, "Stationary Ordinal Utility and Impatience",
  *Econometrica* 28(2) (1960) 287–309.
- J. von Neumann and O. Morgenstern, *Theory of Games and Economic Behavior* (Princeton, 1944; 2nd ed. 1947);
  L. J. Savage, *The Foundations of Statistics* (Wiley, 1954).
- M. Allais, "Le comportement de l'homme rationnel devant le risque", *Econometrica* 21(4) (1953) 503–546;
  D. Kahneman and A. Tversky, "Prospect Theory: An Analysis of Decision under Risk", *Econometrica* 47(2) (1979)
  263–291; A. Tversky and D. Kahneman, "Advances in Prospect Theory", *Journal of Risk and Uncertainty* 5 (1992)
  297–323.
- M. J. Machina, "'Expected Utility' Analysis without the Independence Axiom", *Econometrica* 50(2) (1982) 277–323;
  S. H. Chew, "A Generalization of the Quasilinear Mean", *Econometrica* 51(4) (1983) 1065–1092.
- D. Ellsberg, "Risk, Ambiguity, and the Savage Axioms", *Quarterly Journal of Economics* 75(4) (1961) 643–669;
  F. H. Knight, *Risk, Uncertainty and Profit* (1921); I. Gilboa and D. Schmeidler, "Maxmin Expected Utility with
  Non-Unique Prior", *Journal of Mathematical Economics* 18(2) (1989) 141–153.
- J. W. Pratt, "Risk Aversion in the Small and in the Large", *Econometrica* 32(1/2) (1964) 122–136; K. J. Arrow,
  *Aspects of the Theory of Risk-Bearing* (Helsinki, 1965); J. Mossin, "Aspects of Rational Insurance Purchasing",
  *Journal of Political Economy* 76(4) (1968) 553–568; R. C. Merton, "Lifetime Portfolio Selection under
  Uncertainty", *Review of Economics and Statistics* 51(3) (1969) 247–257; P. A. Samuelson, "Lifetime Portfolio
  Selection by Dynamic Stochastic Programming", same issue, 239–246.
- M. Rothschild and J. E. Stiglitz, "Increasing Risk: I. A Definition", *Journal of Economic Theory* 2(3) (1970)
  225–243.
- J. R. Sydnor, "(Over)insuring Modest Risks", *American Economic Journal: Applied Economics* 2(4) (2010) 177–199.
- M. Rabin, "Risk Aversion and Expected-Utility Theory: A Calibration Theorem", *Econometrica* 68(5) (2000)
  1281–1292; M. Rabin and R. H. Thaler, "Anomalies: Risk Aversion", *Journal of Economic Perspectives* 15(1) (2001)
  219–232, as quoted by A. Rubinstein, *Econometrica* 74(4) (2006), and by J. C. Cox and V. Sadiraj.
- D. M. Kreps and E. L. Porteus, "Temporal Resolution of Uncertainty and Dynamic Choice Theory", *Econometrica* 46(1)
  (1978) 185–200; L. G. Epstein and S. E. Zin, "Substitution, Risk Aversion, and the Temporal Behavior of Consumption
  and Asset Returns: A Theoretical Framework", *Econometrica* 57(4) (1989) 937–969.
- R. Mehra and E. C. Prescott, "The Equity Premium: A Puzzle", *Journal of Monetary Economics* 15(2) (1985) 145–161;
  P. Weil, "The Equity Premium Puzzle and the Risk-Free Rate Puzzle", *Journal of Monetary Economics* 24(3) (1989)
  401–421; R. Bansal and A. Yaron, "Risks for the Long Run", *Journal of Finance* 59(4) (2004) 1481–1509.
- R. E. Hall, "Intertemporal Substitution in Consumption", *Journal of Political Economy* 96(2) (1988) 339–357;
  H. Working, "Note on the Correlation of First Differences of Averages in a Random Chain", *Econometrica* 28(4)
  (1960) 916–918.
- A. Vissing-Jørgensen, "Limited Asset Market Participation and the Elasticity of Intertemporal Substitution",
  *Journal of Political Economy* 110(4) (2002) 825–853; J. Gruber, "A Tax-Based Estimate of the Elasticity of
  Intertemporal Substitution", *Quarterly Journal of Finance* 3(1) (2013); T. Havranek, "Measuring Intertemporal
  Substitution: The Importance of Method Choices and Selective Reporting", *Journal of the European Economic
  Association* 13(6) (2015) 1180–1204.
- R. Chetty, "A New Method of Estimating Risk Aversion", *American Economic Review* 96(5) (2006) 1821–1834;
  A. Elminejad, T. Havranek and Z. Irsova, "Relative Risk Aversion: A Meta-Analysis", *Journal of Economic Surveys*
  39(5) (2025) 2315–2333 (IES Working Paper 2022/14).
- R. H. Strotz, "Myopia and Inconsistency in Dynamic Utility Maximization", *Review of Economic Studies* 23(3)
  (1955–56) 165–180; R. A. Pollak, "Consistent Planning", *Review of Economic Studies* 35(2) (1968) 201–208;
  D. Laibson, "Golden Eggs and Hyperbolic Discounting", *Quarterly Journal of Economics* 112(2) (1997) 443–477;
  R. Thaler, "Some Empirical Evidence on Dynamic Inconsistency", *Economics Letters* 8(3) (1981) 201–207;
  T. Imai, T. A. Rutter and C. F. Camerer, "Meta-Analysis of Present-Bias Estimation Using Convex Time Budgets",
  *Economic Journal* 131 (2021), as reported by Elminejad, Havranek and Irsova.
- C. A. Holt and S. K. Laury, "Risk Aversion and Incentive Effects", *American Economic Review* 92(5) (2002)
  1644–1655; "Risk Aversion and Incentive Effects: New Data without Order Effects", *American Economic Review* 95(3)
  (2005) 902–904.
- R. B. Barsky, F. T. Juster, M. S. Kimball and M. D. Shapiro, "Preference Parameters and Behavioral Heterogeneity",
  *Quarterly Journal of Economics* 112(2) (1997) 537–579.
- T. Post, M. J. van den Assem, G. Baltussen and R. H. Thaler, "Deal or No Deal? Decision Making under Risk in a
  Large-Payoff Game Show", *American Economic Review* 98(1) (2008) 38–71.
- B. C. Madrian and D. F. Shea, "The Power of Suggestion: Inertia in 401(k) Participation and Savings Behavior",
  *Quarterly Journal of Economics* 116(4) (2001) 1149–1187 (NBER Working Paper 7682); R. H. Thaler and S. Benartzi,
  "Save More Tomorrow", *Journal of Political Economy* 112(S1) (2004) S164–S187.
- F. P. Ramsey, "A Mathematical Theory of Saving", *Economic Journal* 38 (1928) 543–559.
- L. P. Hansen and T. J. Sargent, "Robust Control and Model Uncertainty", *American Economic Review* 91(2) (2001)
  60–66; *Robustness* (Princeton, 2008).
- C. F. Manski, "Measuring Expectations", *Econometrica* 72(5) (2004) 1329–1376; M. D. Hurd and K. McGarry, "The
  Predictive Validity of Subjective Probabilities of Survival", *Economic Journal* 112 (2002) 966–985; A. Falk,
  A. Becker, T. Dohmen, B. Enke, D. Huffman and U. Sunde, "Global Evidence on Economic Preferences", *Quarterly Journal
  of Economics* 133(4) (2018) 1645–1692.

**Data.** BEA, real personal consumption expenditures (PCECCA), the PCE price index (DPCERG3A086NBEA) and the
population (B230RC0A052NBEA), annual, 1929–2025; the Federal Reserve Board, the 3-month Treasury bill rate (TB3MS),
monthly, 1934–2026; all via FRED, retrieved 2026-11-19.

**Textbooks.** Varian, *Intermediate Microeconomics*, chs. 10–13; Mas-Colell, Whinston and Green, *Microeconomic
Theory*, ch. 6; Kreps, *Microeconomic Foundations I*, chs. 5–6; Gollier, *The Economics of Risk and Time* (2001);
Eeckhoudt, Gollier and Schlesinger, *Economic and Financial Decisions under Risk* (2005).
