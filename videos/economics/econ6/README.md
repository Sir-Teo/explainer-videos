# Economics, Built: Part 6, Demand

Part 6 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second of Act II, *Choosing*. It asks what happens, when a price changes, to what
people buy and to how well off they are, and answers: two things at once. The good becomes cheaper or dearer relative
to everything else, and the buyer richer or poorer. The first always pushes demand the expected way; the second
usually agrees, but for households that live on one staple it can win, and demand slopes up. The change in welfare is
a change in the expenditure function: a number of dollars, different for every household.

It opens in Hunan in 2006, where Robert Jensen and Nolan Miller gave randomly chosen poor households vouchers that cut
the price of rice by up to a quarter, and the households that were poor but not the poorest ate less rice, not more:
the Giffen behaviour Marshall described in 1895 and a century of economists failed to find. The equation that explains
it was written by Eugen Slutsky in Kiev in 1915 and read by almost nobody for twenty years. From there it covers:

- a game: a week's food for one of the Island's poorest households on $21, 14,000 calories needed, coconuts (cheap
  calories) and fish (taste); coconuts go up, and the viewer buys more of them;
- the demand function: the price-consumption curve and Bo's demand curve, the income-consumption curve and his Engel
  curve, homogeneity of degree zero, elasticities and the adding-up rules;
- Slutsky's two effects drawn as two moves, with Hicks's compensation and Slutsky's, the equation, and its elasticity
  form; the recipe for demand that slopes up;
- Giffen behaviour: the rumour (Marshall, Stigler, Rosen), the subsistence model's three zones, Jensen and Miller's
  experiment and table 3, and the same design run on 1,300 simulated island households with the truth planted;
- duality: the four functions, Roy's identity and Shephard's lemma, the concave expenditure function, and the
  identities checked numerically on four demand systems;
- integrability: the Slutsky matrix's symmetry, and a loop of prices that pumps money from a consumer whose demand comes
  from no preference;
- an intermission without narration: a century of relative prices, fifteen kinds of American spending moving through
  price and quantity from 1929 to 2025, under the falling price of recreational goods as a tune;
- Engel curves: Engel's law in 1857, across America's century and across 2024's income quintiles, and Hamilton's use of
  their drift to measure the CPI's bias; Engel's law as *Called it?*;
- welfare in dollars: compensating and equivalent variation, consumer's surplus between them, Willig's bound, and
  Hausman's exact surplus and the deadweight loss it corrects;
- the cost of living: Konüs's index, Laspeyres and Paasche around it, the substitution bias, Hicks's virtual prices and
  Hausman's Apple-Cinnamon Cheerios, and the Boskin Commission's pieces;
- demand systems: the linear expenditure system, the AIDS estimated on a simulated island survey with its tests, and
  Gorman's condition for a representative consumer;
- the dials (staples' price elasticities, with Hunan's rows; food's income elasticity, new), the CPI's substitution
  methods, food prices and poor households, Ramsey's rule, and a frontier chapter on inflation inequality, new goods and
  welfare that depends on income.

## Build it

```bash
python -m videos.economics.econ6.compute              # every number (seconds), into .cache/econ6/
python tools/qa_scene.py econ6 Giffen                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ6 -q l   # the whole part, silent preview
python tools/build.py econ6                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 6                     # the lab
```

The data are frozen extracts in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): BEA's personal consumption expenditures by type of
product (fifteen categories, prices and spending, 1929–2025) and the population, from FRED. The published results
(Jensen and Miller; Hausman's cereal; Costa and Hamilton; Engel, Houthakker and Seale and Regmi; the USDA's quintiles;
Jaravel; the BLS's methods; Slutsky's rediscovery) are transcribed in `explainer/economics/data/tables.py`, each with
where it was read and the date it was checked.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | When a price changes, what happens to what people buy? | Hunan and Gansu, 2006: 1,300 urban poor households in 11 county towns, vouchers of 0.10, 0.20 or 0.30 yuan off a 1.20-yuan jin of rice, June to October; those getting under 80% of their calories from rice: a 1% dearer price, 0.45% more rice; Marshall (1895) and Stigler (1987) quoted; Slutsky (1915), Hicks and Allen (1934); the question; the title; objectives |
| 1 | Play it: a week of food on $21 | Coconuts $1.20 (1,400 calories), fish $2 (700 calories, and taste); 14,000 calories; the fed-and-affordable sliver; the best bundle, 6.4 fish and 6.8 coconuts; coconuts go to $1.50; a countdown; 7.6 coconuts and 4.8 fish: the old basket costs $23.04, each fish swapped for half a coconut saves $1.25 |
| 2 | The demand function | Bo (60% of $60 on fish, coconuts $6) as fish fall from $15 to $2.80: the price-consumption curve and x = 36/p; income from $20 to $76: a ray and a straight Engel curve; luxuries and inferior goods; homogeneity, (10, 6, 60) and (20, 12, 120) give (3.6, 4); elasticities, Bo's −1, 0 and 1; homogeneity, Engel and Cournot aggregation |
| 3 | Two effects of one price: the Slutsky equation | Fish $10 → $6: A (3.6, 4) to C (6, 4); Hicks's compensation $15.84, B (4.42, 2.94): substitution +0.82, income +1.58; Slutsky's, $45.60 through A, B′ (4.56, 3.04): +0.96 and +1.44; the equation, −0.360 = −0.144 − 3.6 × 0.06; ε = εʰ − wη: Bo −1 = −0.4 − 0.6, the Play-it household +0.43 = 0 − 0.39 × (−1.11) |
| 4 | When demand slopes up: Giffen behaviour | Marshall (1895), Stigler (1947), Rosen (1999); the household's coconut demand at $21: down to 95 cents, up to $2.10, down again; ε = r/(1 − r) = 0.43; Jensen and Miller's design; table 3: +0.22 (all), +0.45 (≤ 80%), −0.61 (> 80%), +0.64 (60–80%); meat −1.13 for meat-eaters; the inverted U, 0.53–0.84, peak 0.85 at 0.70; Gansu; the Island: 1,300 households, all −0.00, 60–80% +0.34 against a planted +0.43, fish −1.27, the kernel-weighted curve against the planted one |
| 5 | Duality: four functions, one consumer | Bo's problem and the shopkeeper's; a budget shrinking from $110 to $60; the map of x, h, v and e; Roy (1947), Shephard (1953); Bo's expenditure function against the cost of his old bundle, 3.6p + 24: tangent at $10, gaps at $2, $6 ($1.44, Slutsky's $45.60 against Hicks's $44.16), $18 and $27; concavity; identities checked on Cobb–Douglas, CES, the linear expenditure system and the AIDS, errors about 10⁻¹⁰ |
| 6 | Integrability: is there a consumer behind the demand? | Antonelli (1886), Hurwicz and Uzawa (1971); the four conditions; two Slutsky matrices over fish, coconuts and cloth, one symmetric, one circular; a loop of radius 0.4 in log prices: compensated income returns, or ends 3.0% lower; Green's theorem, (0.02 − 0.08) × π 0.4² = −0.030; a test, a licence, and GARP |
| | Intermission: a century of relative prices | No narration: fifteen kinds of spending, relative price and quantity per head (1929 = 1, log scales), 1929–2025; recreational goods to 0.01 of their relative price and 726 times the quantity; health care 3.6 times dearer and 11 times as much; slope −0.84, correlation −0.82; real spending per head ×6.5; not a demand curve; the relative price of recreational goods as a tune; the story so far |
| 7 | Engel curves | Engel (1857) in Zimmerman's translation; Houthakker (1957); America: food at home 21% → 7.5% of spending as real spending per head rose 6.5-fold, food bought ×2.4, food's relative price ×0.96: a century elasticity of 0.47; 2024 quintiles: 33.0%, 12.2%, 6.4% of income, $5,498, $9,097, $16,989; elasticities 0.34 and 0.49; Hamilton's idea; six island surveys with a 1% a year bias planted, 0.97% recovered; Costa and Hamilton's estimates, 1888–1994; Almås; *Called it?*: Engel's law, right |
| 8 | Welfare in dollars | Bo's gain from fish $10 → $6: CV $15.84, EV $21.52; Marshall's and Hicks's demand curves, the areas, CS $18.39 between; Willig (1976): about 15%, exactly 14%; a 60-cent tax on a $1.20 coconut (x = −4p + 0.1m + 6): CS $3.60, CV $3.72; deadweight loss $0.72 by Marshall, $0.61 exact, 17% too big; Hausman (1981)'s closed form |
| 9 | The cost of living as a welfare problem | Konüs (1924); fish $10 → $6: Laspeyres 0.760, true 0.736, Paasche 0.714; $10 → $15: 1.300, 1.275, 1.250; the bias with σ = 0.3, 1, 3: 1.0%, 3.3%, 9.7%; Hicks (1940) and virtual prices; Apple-Cinnamon Cheerios (1989): $7.14 against $3.48, $78.1 million a year, 31 cents a person, the cereal CPI overstated by about 25%; the Boskin Commission's 0.4, 0.1 and 0.6 |
| 10 | Demand systems you can estimate | Stone (1954), Deaton and Muellbauer (1980), Gorman (1953); the AIDS share equation and its restrictions; the Island's survey: 6,000 households, planted and estimated elasticities (coconuts −0.72, cloth's income elasticity 1.48), homogeneity p = 0.41, symmetry p = 0.58; Deaton and Muellbauer's rejection of homogeneity on British data, 1954–74; Gorman's parallel Engel curves: moving $20 from Chidi to Ana changes fish bought by 0 or by −2.4 |
| 11 | The Dials: how much do people respond? | Staples' price elasticities: Part 2's meta-analyses (gasoline −0.09 and −0.31, cigarettes −0.48, alcohol −0.46 to −0.80) and Hunan's rows (+0.22, +0.45, −0.61): status now depends on the setting; a new dial, food's income elasticity: Houthakker 0.6; Seale and Regmi 0.7, 0.6, 0.5, 0.1–0.3; ours, 0.47 and 0.34–0.49 |
| 12 | In practice: price indices, poor households, taxes | The BLS's geometric means (1999) and chained CPI (2002); fifteen kinds of spending, 2000–2025: a fixed 2000 basket 0.18 points a year above the chained Törnqvist; Deaton (1989): net purchases as the first-order welfare effect, three illustrative households; Indonesia 1997–98; Ramsey (1927): $10 from two goods, 5% each costs $0.19, 8% and 2% cost $0.12; equity against efficiency |
| 13 | Frontier: whose inflation, whose welfare? | Jaravel (2019): the poorest fifth's inflation 0.66 points a year above the richest's in retail, 0.88 with new products, 0.37 for the whole basket, 2004–2015; Feenstra (1994)'s variety correction, 1.7% for 5% of spending on new goods at σ = 4; Redding and Weinstein (2020); Jaravel and Lashkari (2024): 1955 understated by 11.5%, growth 18 basis points lower; Atkin, Faber, Fally and Gonzalez-Navarro (2024) |
| | Recap, problems, and the road ahead | The answer; twelve lines; problems; reading; Bernoulli's St Petersburg game and Part 7 |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's demand systems (`explainer.economics.agora.demand`), with
the Island's Part 6 truths in `explainer.economics.island`, or from the Data Room or a transcribed table; the narration
states the cached numbers.

- **Bo** (planted in Part 5): Cobb–Douglas with 60% of $60 on fish, coconuts at $6. Demand, compensated demand,
  indirect utility and expenditure in closed form; the Hicks decomposition from h(p₁, u₀), Slutsky's from x(p₁, p₁·A).
- **The subsistence diet** (`demand.Diet`): a household maximizes β log(s − s₀) + (1 − β) log f with s₀ = 3 coconuts
  and β = 1/6, subject to its budget and to eating 14,000 calories (coconuts 1,400 each, fish 700); the Island's
  version spends 12% of its budget on oil and greens at 600 calories a dollar. The zones: deprived when the budget
  cannot buy the calories even as coconuts; subsistence when the taste optimum falls short of the calories, so the
  bundle is where the budget and calorie lines cross; standard otherwise. In the subsistence zone the coconut's price
  elasticity is r/(1 − r), r the fish's calories per dollar over the coconut's.
- **The voucher experiment** (`demand.voucher_experiment`; planted): 1,300 households in 11 villages, a control group
  and vouchers of 10, 20 or 30 cents off $1.20 assigned at random within villages; weekly food money lognormal (median
  $17, σ 0.3), calorie needs ±10%, income moving 5% between rounds, consumption reported with 12% multiplicative error;
  three rounds; the regression of the arc percent change in coconuts on the arc percent change in the price, with
  village-by-round fixed effects and household-clustered standard errors; the kernel-weighted curve uses a biweight
  window of ±0.10 in the initial calorie share; seed 2006.
- **Duality checks** (`demand.duality_errors`): three goods at prices (2, 3, 1.5) and income 100; derivatives by
  central differences with a relative step of 10⁻⁶.
- **The integrability loop** (`demand.loop_income`): shares w = α + γ log p over fish, coconuts and cloth with cloth's
  price fixed; compensated log income integrated by the midpoint rule over 720 steps round a circle of radius 0.4.
- **Engel curves**: America's real spending per head is nominal spending per head deflated by a chained Fisher index
  of the fifteen categories (2017 = 1); the century elasticity is log(food quantity ratio) / log(real spending ratio).
  The quintile elasticities are log ratios of food spending over log ratios of the income implied by each quintile's
  food spending and share.
- **Hamilton's method** (`demand.hamilton_drift`; planted): six surveys four years apart, 1,500 households each; food's
  share 0.60 − 0.10 log(real income / 300) + 0.05 log(food's relative price, varying across 10 regions) + noise (s.d.
  0.04); real income grows 1.5% a year; the official index overstates the cost of living by 1% a year; food shares on
  log measured income, the log relative price and year dummies; each dummy over the income slope is the cumulative
  bias; seed 2001.
- **Welfare**: CV, EV and Marshall's surplus for Bo by the expenditure function and by integrating demand; the coconut
  tax with `demand.LinearDemand`, whose expenditure function e(p, k) = k e^{δp} − (αp + α/δ + c)/δ is Hausman's
  closed form; deadweight loss exact as CV − t·h(p₁, u₀), Marshall's as CS − t·x(p₁, m).
- **The cost of living**: Laspeyres, Paasche and Konüs's index for Bo and for CES tastes with σ = 0.3 and 3 (weights
  0.6 and 0.4); the Cheerios picture is schematic (a straight line through the observed price with Hausman's virtual
  price as its intercept); the numbers are his.
- **The survey** (`demand.Survey`, `demand.aids_fit`; planted): an AIDS over fish, coconuts and cloth with α = (0.35,
  0.40, 0.25), β = (−0.04, −0.08, 0.12) and a symmetric, homogeneous γ; α₀ = log 300; 20 villages × 12 months of log
  prices (village, month and cell shocks with s.d. 0.15, 0.15 and 0.075), 25 households a cell with log spending of
  s.d. 0.5 around log 300, shares with noise of s.d. 0.03 (summing to zero); estimated by iterated least squares
  (log a(p) from the current estimates, then a stacked GLS of two equations), with Wald tests from the unrestricted
  system; seed 1980.
- **The CPI computation**: a fixed-base Laspeyres index (2000 weights) and a chained Törnqvist index of the fifteen
  PCE categories, 2000–2025.
- **Ramsey**: two goods with $100 of spending each and elasticities −0.3 and −1.2; deadweight loss approximated by
  ½|ε|t²·px; $10 of revenue.
- **The intermission**: relative prices are each category's price index over the chained Fisher index of all fifteen;
  quantities are per head; one year every 0.42 s; the data melody maps the relative price of recreational goods (log
  scale) to D dorian.
- **The score** (`explainer/economics/score.py`): the scissors theme, chapter stings, beds under the pauses, and the
  close. Synthesized from sines; nothing recorded.

## Problems and solutions

**1.** *Bo: u = x^0.6 y^0.4, $60, coconuts $6; fish fall from $10 to $6. Find the bundles A, C, Hicks's B and
Slutsky's B′, and both splits into substitution and income effects.*

*Solution.* Cobb–Douglas spends 60% on fish: A = (0.6·60/10, 0.4·60/6) = (3.6, 4) and C = (36/6, 4) = (6, 4).
Utility at A is u₀ = 3.6^0.6·4^0.4 ≈ 3.755. Hicks: the income that reaches u₀ at the new prices is e = u₀·(6/0.6)^0.6·
(6/0.4)^0.4 ≈ $44.16, so B = (0.6·44.16/6, 0.4·44.16/6) ≈ (4.42, 2.94): substitution +0.82 fish, income +1.58.
Slutsky: the income that buys A at the new prices is 6·3.6 + 6·4 = $45.60, so B′ = (4.56, 3.04): substitution +0.96,
income +1.44. Slutsky's compensation is $1.44 more generous, so more of the move counts as substitution.

**2.** *A good takes 30% of a budget, with compensated elasticity −0.5 and income elasticity 0.8. Find its price
elasticity. How negative must the income elasticity be for demand to slope up?*

*Solution.* ε = εʰ − wη = −0.5 − 0.3·0.8 = −0.74. Demand slopes up when −0.5 − 0.3η > 0, that is η < −0.5/0.3 ≈
−1.67: the good must be strongly inferior, because it takes less than a third of the budget and has real room to
substitute. With a share of 0.39 and εʰ = 0, as in Play it, any negative η is enough.

**3.** *Play it: $21, 14,000 calories; coconuts 1,400 calories, fish 700 at $2. Find the bundle at coconut prices
$1.20 and $1.50, and show the elasticity in the subsistence zone is r/(1 − r).*

*Solution.* In the subsistence zone both constraints bind: p s + 2f = 21 and 1,400s + 700f = 14,000, so f = 20 − 2s
and s = (21 − 40)/(p − 4) = 19/(4 − p). At $1.20, s = 6.79 and f = 6.43; at $1.50, s = 7.60 and f = 4.80. Generally,
s = (K p_f − m c_f)/(p_f c_s − p c_f), so ds/dp = s·c_f/(p_f c_s − p c_f) and ε = p c_f/(p_f c_s − p c_f) =
r/(1 − r) with r = (c_f/p_f)/(c_s/p). At $1.20, r = 350/1,167 = 0.3 and ε = 0.43. (Check the zone: at $1.20 the taste
optimum would buy 3 + (21 − 3.6)/(6·1.2) = 5.42 coconuts and 7.25 fish, 12,658 calories, too few.)

**4.** *Derive the expenditure function and Hicksian demand for u = x^a y^(1−a), and check Shephard's lemma and Roy's
identity.*

*Solution.* Demand is x = am/p_x, y = (1 − a)m/p_y, so v(p, m) = m (a/p_x)^a ((1 − a)/p_y)^(1−a). Inverting at
v = u, e(p, u) = u (p_x/a)^a (p_y/(1 − a))^(1−a), and h_x(p, u) = x(p, e(p, u)) = a·e/p_x. Shephard: ∂e/∂p_x =
a·e/p_x = h_x. Roy: ∂v/∂p_x = −a v/p_x and ∂v/∂m = v/m, so −(∂v/∂p_x)/(∂v/∂m) = a m/p_x = x.

**5.** *Shares w_i = α_i + Σ_j γ_ij log p_j with γ₁₂ = 0.08, γ₂₁ = 0.02. Compensated income goes counter-clockwise
round a square of side 0.2 in (log p₁, log p₂). By how much does it change, and in which direction?*

*Solution.* Along the loop d log m = w₁ d log p₁ + w₂ d log p₂, and by Green's theorem the integral round a closed
counter-clockwise loop is ∬ (∂w₂/∂log p₁ − ∂w₁/∂log p₂) dA = (γ₂₁ − γ₁₂)·area = (0.02 − 0.08)·0.04 = −0.0024. Log
income ends 0.24% lower at the same prices; clockwise it would end 0.24% higher. A symmetric γ gives zero for every
loop, which is the integrability condition.

**6.** *2024: the poorest fifth spent $5,498 on food (33.0% of income), the middle fifth $9,097 (12.2%). Find the
incomes and the arc income elasticity of food.*

*Solution.* Incomes are 5,498/0.330 ≈ $16,661 and 9,097/0.122 ≈ $74,566. The log-arc elasticity is
ln(9,097/5,498)/ln(74,566/16,661) = 0.504/1.499 ≈ 0.34: food spending rises by about a third of a percent for each
percent of income, a necessity. (The midpoint-percent version gives 0.39.)

**7.** *Coconuts: x = −4p + 0.1m + 6, m = 60, p = 1.20. A 60-cent tax: find Marshall's loss, Willig's approximation to
CV, and Hausman's exact CV and deadweight loss.*

*Solution.* At m = 60 demand is 12 − 4p: 7.2 coconuts at $1.20 and 4.8 at $1.80. Marshall's loss is ∫ from 1.2 to 1.8
of (12 − 4p) dp = $3.60, and revenue is 0.6·4.8 = $2.88, so Marshall's deadweight loss is $0.72. The income
elasticity is 0.1·60/7.2 = 0.83, so Willig's CV ≈ 3.60·(1 + 0.83·3.60/120) ≈ $3.69. Exactly, e(p, k) = k e^{0.1p} +
(4p + 40 − 6)/0.1 with k fixed by e(1.2, k) = 60, so e(1.8, k) ≈ $63.72 and CV = $3.72. The compensated demand at
$1.80 is x(1.8, 63.72) ≈ 5.17, so the exact deadweight loss is 3.72 − 0.6·5.17 ≈ $0.61: Marshall's is 17% too big,
though his loss of surplus was only 3% off.

**8.** ★ *Hamilton's method assumes the food Engel curve's shape is stable. Let tastes drift away from food by 0.2
points of share a year. What does the method report, and how could you tell drift from CPI bias?*

*Solution.* With w = a + b log(true income) + drift·t and log(true income) = log(measured income) + bias·t, the year
dummies estimate (b·bias + drift)·t, and the method reports (b·bias + drift)/b = bias + drift/b a year. With b = −0.10
and drift = −0.002, that is bias + 0.02: a planted 1% a year is reported as 3%. Ways to tell them apart: use several
indicator goods (a genuine price-index error shifts every good's Engel curve by the same income distance, a taste
drift need not); use regions with different measured inflation in the same year (only the bias varies with the
regional index); and compare with independent evidence on quality and new goods. Open questions: how much of the
measured drift in food's share since the 1970s is eating out rather than CPI bias, and whether the method can be made
robust to Engel curves that change slope as well as level (Almås and coauthors' and Logan's critiques).

## Where it comes back

| Idea | Where |
|---|---|
| choice over time and under risk; the expected-utility consumer | Part 7, *Time and Risk* |
| welfare measures, CV and EV in cost–benefit analysis | Part 18, *Social Choice and Welfare* |
| the CPI, its biases, and inflation by income group | Part 28, *Inflation and Expectations* |
| Ramsey taxes, optimal commodity and income taxation | Part 41, *Taxes* |
| demand estimation with product characteristics (BLP), new goods | Part 43, *Measuring Market Power* |
| welfare when choices are inconsistent | Part 45, *Behavioural Economics* |
| food prices, poverty and nutrition; Engel curves for welfare | Part 46, *Development* |

## Sources

**Primary texts.**
- E. Slutsky, "Sulla teoria del bilancio del consumatore", *Giornale degli Economisti e Rivista di Statistica* 51
  (July 1915); J. S. Chipman and J.-S. Lenfant, "Slutsky's 1915 Article: How It Came to Be Found and Interpreted",
  *History of Political Economy* 34(3) (2002) 553–597.
- J. R. Hicks and R. G. D. Allen, "A Reconsideration of the Theory of Value", *Economica* NS 1 (1934); J. R. Hicks,
  *Value and Capital* (Oxford, 1939); "The Valuation of the Social Income", *Economica* NS 7 (1940).
- A. Marshall, *Principles of Economics*, 3rd edition (Macmillan, 1895), p. 208.
- E. Engel, "Die Productions- und Consumtionsverhältnisse des Königreichs Sachsen" (1857), as translated in C. C.
  Zimmerman, "Ernst Engel's Law of Expenditures for Food", *Quarterly Journal of Economics* 47(1) (1932) 78–101.
- A. A. Konüs, "The Problem of the True Index of the Cost of Living" (1924; English translation in *Econometrica* 7,
  1939).
- R. Roy, "La distribution du revenu entre les divers biens", *Econometrica* 15 (1947); R. W. Shephard, *Cost and
  Production Functions* (Princeton, 1953).
- G. B. Antonelli, *Sulla teoria matematica della economia politica* (1886); L. Hurwicz and H. Uzawa, "On the
  Integrability of Demand Functions", in J. S. Chipman et al., eds., *Preferences, Utility, and Demand* (1971).
- F. P. Ramsey, "A Contribution to the Theory of Taxation", *Economic Journal* 37 (1927) 47–61.

**Papers.**
- R. T. Jensen and N. H. Miller, "Giffen Behavior and Subsistence Consumption", *American Economic Review* 98(4)
  (2008) 1553–1577, tables 1–3 and 6, figure 2 (read in the authors' manuscript of January 2008).
- G. J. Stigler, "Notes on the History of the Giffen Paradox", *Journal of Political Economy* 55(2) (1947) 152–156;
  *The Theory of Price*, 4th edition (1987); S. Rosen, "Potato Paradoxes", *Journal of Political Economy* 107(6)
  (1999) S294–S313; R. Koenker, "Was Bread Giffen?", *Review of Economics and Statistics* 59(2) (1977).
- R. D. Willig, "Consumer's Surplus without Apology", *American Economic Review* 66(4) (1976) 589–597.
- J. A. Hausman, "Exact Consumer's Surplus and Deadweight Loss", *American Economic Review* 71(4) (1981) 662–676;
  "Valuation of New Goods under Perfect and Imperfect Competition", in T. F. Bresnahan and R. J. Gordon, eds., *The
  Economics of New Goods* (Chicago, 1997), ch. 5.
- R. Stone, "Linear Expenditure Systems and Demand Analysis", *Economic Journal* 64 (1954) 511–527.
- A. Deaton and J. Muellbauer, "An Almost Ideal Demand System", *American Economic Review* 70(3) (1980) 312–326;
  *Economics and Consumer Behavior* (Cambridge, 1980); R. Blundell and J.-M. Robin, "Estimation in Large and
  Disaggregated Demand Systems", *Journal of Applied Econometrics* 14 (1999).
- W. M. Gorman, "Community Preference Fields", *Econometrica* 21 (1953) 63–80.
- H. S. Houthakker, "An International Comparison of Household Expenditure Patterns, Commemorating the Centenary of
  Engel's Law", *Econometrica* 25(4) (1957) 532–551; J. L. Seale and A. Regmi, "Modeling International Consumption
  Patterns", *Review of Income and Wealth* 52(4) (2006); both as summarized by R. Anker, "Engel's Law Around the World
  150 Years Later", PERI Working Paper 247 (2011).
- B. W. Hamilton, "Using Engel's Law to Estimate CPI Bias", *American Economic Review* 91(3) (2001) 619–630; D. L.
  Costa, "Estimating Real Income in the United States from 1888 to 1994: Correcting CPI Bias Using Engel Curves",
  *Journal of Political Economy* 109(6) (2001) 1288–1310; I. Almås, "International Income Inequality: Measuring PPP
  Bias by Estimating Engel Curves for Food", *American Economic Review* 102(2) (2012) 1093–1117.
- M. J. Boskin, E. R. Dulberger, R. J. Gordon, Z. Griliches and D. W. Jorgenson, *Toward a More Accurate Measure of
  the Cost of Living* (1996); B. R. Moulton, "The Measurement of Output, Prices, and Productivity" (Brookings, 2018).
- A. Deaton, "Rice Prices and Income Distribution in Thailand: A Non-parametric Analysis", *Economic Journal* 99
  (1989) 1–37; J. Friedman and J. Levinsohn, "The Distributional Impacts of Indonesia's Financial Crisis on Household
  Welfare", *World Bank Economic Review* 16(3) (2002), as cited by Jensen and Miller.
- R. C. Feenstra, "New Product Varieties and the Measurement of International Prices", *American Economic Review*
  84(1) (1994) 157–177.
- X. Jaravel, "The Unequal Gains from Product Innovations: Evidence from the U.S. Retail Sector", *Quarterly Journal
  of Economics* 134(2) (2019) 715–783; X. Jaravel and D. Lashkari, "Measuring Growth in Consumer Welfare with
  Income-Dependent Preferences", *Quarterly Journal of Economics* 139(1) (2024) 477–532.
- S. J. Redding and D. E. Weinstein, "Measuring Aggregate Price Indices with Taste Shocks: Theory and Evidence for CES
  Preferences", *Quarterly Journal of Economics* 135(1) (2020) 503–560.
- D. Atkin, B. Faber, T. Fally and M. Gonzalez-Navarro, "Measuring Welfare and Inequality with Incomplete Price
  Information", *Quarterly Journal of Economics* 139(1) (2024) 419–475.

**Data.** BEA, personal consumption expenditures by type of product, 1929–2025, via FRED; USDA ERS, *Ag and Food
Statistics: Charting the Essentials*, Food Prices and Spending (2026), from the BLS Consumer Expenditure Survey, 2024;
the BLS *Handbook of Methods*, the Consumer Price Index.

**Textbooks.** Varian, *Intermediate Microeconomics*, chs. 6–10 and 14; Mas-Colell, Whinston and Green, *Microeconomic
Theory*, chs. 2–3; Deaton and Muellbauer, *Economics and Consumer Behavior*; Nicholson and Snyder, *Microeconomic
Theory*, chs. 5–6; Jehle and Reny, *Advanced Microeconomic Theory*, ch. 1.
