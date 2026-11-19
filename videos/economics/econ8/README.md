# Economics, Built: Part 8, The Firm

Part 8 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the last of Act II, *Choosing*. It asks how a firm decides what to make and how, and
why there is a firm at all, and answers: at the margin. A firm hires each input until the last unit earns what it
costs, builds until price equals marginal cost, and with free entry an industry settles where profits disappear. And
the firm exists because using the market has costs: it draws its boundary where organizing one more transaction
inside costs as much as buying it outside, and ownership goes to whoever's investment matters most.

It opens with Paul Douglas's chart of 1927: capital, labour and output in American manufacturing, 1899–1922, on a log
scale, with output a quarter of the way from labour to capital. His friend Charles Cobb, a mathematician at Amherst,
gave him P′ = 1.01 L^(3/4) C^(1/4), refitted on screen from their own numbers; labour's share of the American economy
stayed near 62% for half a century, then fell. Ten years later Ronald Coase asked why the "islands of conscious power"
exist at all. From there it covers:

- technology: Crusoe's boatyard (boats from slipways and shipwrights), marginal products and diminishing returns,
  isoquants and the technical rate of substitution;
- Cobb and Douglas's regression and its fragility (a time trend turns capital's exponent negative), CES and the
  elasticity of substitution, and why factor shares are the exponents;
- returns to scale, a pipeline's geometry and the engineers' six-tenths rule, and why every industry isn't one firm;
- cost minimization, conditional factor demands, the cost function and Shephard's lemma;
- short-run cost curves, marginal cost through the bottom of average cost, and the long-run envelope;
- a game: the viewer runs the boatyard and hires shipwrights until the last one stops paying;
- profit and supply: price equals marginal cost, shut-down and break-even prices, Le Chatelier's principle and
  Hotelling's lemma;
- an intermission without narration: Douglas's chart redrawn year by year, under the index of output as a tune;
- the industry: free entry and zero profit, a flat long-run supply, and with different firms an upward-sloping one
  and rents;
- whether firms maximize at all: Hall and Hitch's full-cost pricing (1939), Friedman's billiard player (1953), and
  Alchian's survival (1950), run on 200 simulated yards;
- Coase's transaction costs, the boundary of the firm, and Williamson's make-or-buy;
- hold-up: a specific investment under ex post bargaining, and the record of Fisher Body and General Motors;
- Grossman, Hart and Moore: residual control rights and who should own the asset;
- two new dials (capital's output elasticity; the elasticity of substitution between capital and labour), cost models
  and capacity in practice, and a frontier chapter on intangible capital, generative AI at work and a Coasean
  singularity.

## Build it

```bash
python -m videos.economics.econ8.compute              # every number (seconds), into .cache/econ8/
python tools/qa_scene.py econ8 HoldUp                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ8 -q l   # the whole part, silent preview
python tools/build.py econ8                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 8                     # the lab
```

The data are frozen extracts in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): the Penn World Table's labour share for the United
States, 1950–2023, via FRED, and Cobb and Douglas's indices for 1899–1922 as reproduced by Felipe and Adams (2005),
transcribed in `explainer/economics/data/tables.py` with where they were read and the date they were checked.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | How does a firm decide what to make and how, and why is there a firm at all? | Douglas's chart (1927): capital ×4.31, labour ×1.61, output ×2.40 by 1922, output on average 0.25 of the way from labour to capital; Charles Cobb; P′ = 1.01 L^(3/4) C^(1/4) refitted (labour 0.746, capital 0.254), the exponents near the income shares; labour's share of US GDP 60–65% in 1950–1999 (62.5% on average), 56.8% in 2023; Coase (1937) and Robertson's islands of conscious power; the question; objectives |
| 1 | Technology: what a firm can make | Crusoe's yard: q = 2K^0.25 L^0.5, slipways $400 a month, shipwrights $1,000; 5.66 boats from four of each; each shipwright adds 2.83, 1.17, 0.90, 0.76, …; isoquants for 4, 5.66 and 8 boats; the technical rate of substitution, 2 at four of each |
| 2 | Cobb and Douglas, and the shape of technology | The 1928 regression refitted: β = 0.254, A = 1.015; unrestricted 0.81 and 0.23; with a time trend 0.91 and −0.53; in growth rates 1.40 and −1.52; 1899–1920 1.09 and 0.08 (Felipe and Adams 2005); CES isoquants for σ = 0, ½, 1, 2, ∞ (Arrow, Chenery, Minhas and Solow 1961); shares as exponents, and how σ moves them |
| 3 | Returns to scale | q(tK, tL) = t^(a+b) q; doubling gives ×1.68, ×2, ×2.30 for returns of 0.75, 1, 1.2; a pipe's steel ∝ d and capacity ∝ d²; the six-tenths rule (Williams 1947); Chenery (1949); why not one firm? |
| 4 | Cost minimization and the cost function | Eight boats: isocosts of slope −2.5, the tangency at 5.89 shipwrights and 7.37 slipways, $8,841.68 a month; MP_L/MP_K = w/r; factor demands against w/r; the cost function, c ∝ q^(4/3); Shephard's lemma checked on three technologies (errors about 10⁻¹⁰) |
| 5 | Cost curves from the technology | Four slipways rented: fixed cost $1,600, variable and total cost; average total, average variable and marginal cost, the bottom of the U at 3.6 boats and $894; the envelope of short-run curves for 1–16 slipways |
| 6 | Play it: run the boatyard | Four slipways, $1,200 a boat, $1,000 a shipwright; values of each shipwright's boats $3,394, $1,406, $1,079, $909, …; a countdown; hire three, where p·MP_L = w; profit $1,279 a month (four: $1,188; two: $1,200); the sunk slipways change the profit, not the decision |
| 7 | Profit and supply | A larger yard (F = $4,000, VC = 200q + 50q²): at $1,500, thirteen boats and $4,450 profit; break-even $1,094 at 8.9 boats, shut-down $200; supply is marginal cost above the shut-down price; Crusoe's first yard: supply elasticity 1 in the short run, 3 in the long; Le Chatelier and Hotelling |
| | Intermission: Douglas's chart, year by year | No narration: capital, labour and output, 1899–1922, drawn year by year with the formula dashed beside output; the output index as a tune; the story so far |
| 8 | The industry: entry, exit and rents | Identical yards and Q = 400 − 0.2p: price $1,094, 8.9 boats each, 181 boats, about 20 yards, zero profit, a flat long-run supply; fixed costs from $2,000 to $8,000: 27 yards at $966, rents of $14,620 a month to the cheaper yards, an upward-sloping long-run supply |
| 9 | Do firms maximize profit? | Hall and Hitch (1939): full-cost pricing; the marginalist controversy; Alchian (1950); Friedman (1953): the billiard player; 200 island yards with habitual markups, demand elasticity −3 (optimum 50%), closure after three losing months and imitation in proportion to profit: the middle half from 22–75% to 46–57% in ten years, 479 closures |
| 10 | Coase: why is there a firm at all? | "The main reason why it is profitable to establish a firm would seem to be that there is a cost of using the price mechanism"; discovering prices, negotiating contracts; the employment relation; the boundary at the margin; Williamson's make-or-buy (illustrative costs, switch at a specificity of 0.4) |
| 11 | Specific assets and hold-up: Fisher Body and General Motors | Value 2V√i, cost i, V = 10: invest 100 together, 25 apart with half the surplus ex post, a quarter of the surplus lost; GM and Fisher Body, 1919 and 1926; Klein, Crawford and Alchian (1978); Coase (2000): "There was no holdup"; Freeland, Casadesus-Masanell and Spulber, Klein's reply |
| 12 | Who should own the asset? | Grossman and Hart (1986), Hart and Moore (1990): incomplete contracts and residual control rights; the yard's investment four times the die maker's: surplus 8.50 first best, 8.29 if the yard owns, 6.50 if the die maker does, 6.38 apart |
| 13 | The Dials: capital's elasticity, and substitution | Capital's output elasticity (new): Cobb and Douglas 0.25, Felipe and Adams 0.233, Gollin 0.20–0.35, the PWT's 0.375 for the US: settled within a range; the elasticity of substitution (new): Chirinko 0.4–0.6, Gechert et al. 0.9 reported and 0.3 corrected, Oberfield and Raval 0.5–0.7, Karabarbounis and Neiman 1.25: contested |
| 14 | In practice: cost models and capacity | The six-tenths rule (twice the capacity, 1.52 times the cost); Wright's learning curve (1936), drawn with a fall of a fifth per doubling; capacity under uncertain orders (mean 100, s.d. 20, cost $250, margin $1,000): 113 boats, where P(orders > K) = 0.25 |
| 15 | Frontier: intangibles, AI and the boundary of the firm | Haskel and Westlake (2018): scalable, sunk, spillovers, synergies; Brynjolfsson, Li and Raymond: 5,172 agents, +14% resolutions an hour, +34% for novices; Shahidi et al. (2025): the Coasean singularity, and which way the boundary moves |
| | Recap, problems, and the road ahead | The answer; twelve lines; problems; reading; Arrow and Debreu (1954), and Part 9 |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's firm (`explainer.economics.agora.firm`), with the Island's
Part 8 truths in `explainer.economics.island`, or from the Data Room or a transcribed table; the narration states the
cached numbers.

- **Cobb and Douglas's regression.** OLS on logs of the 24 annual indices: log(Y/L) on log(K/L) with constant returns
  imposed (as in 1928), the unrestricted form, a linear time trend added, first differences, and 1899–1920 only. The
  unrestricted coefficients are asserted against Felipe and Adams's table 2.
- **The yard.** Cobb–Douglas q = 2K^0.25 L^0.5 with closed-form conditional demands and cost; isoquants by bisection
  on log K; Shephard's and Hotelling's lemmas by central differences; the short-run costs with K = 4 in closed form;
  the boatyard game by discrete increments of output.
- **The larger yard and the industry.** Total cost F + cq + dq²; break-even at √(F/d); free entry with identical
  yards; with fixed costs spread evenly from $2,000 to $8,000, yards enter cheapest first until the next one would
  lose money, each producing where price equals marginal cost.
- **Survival.** 200 yards price at cost × (1 + markup) with markups drawn uniform on 0–100% (seed 1950); each month's
  sales are 100 p^(−3) times lognormal noise (s.d. 0.15); a fixed cost of 0.9 times the best variable profit; after
  three losing months a yard is replaced by a copy of a profitable one chosen in proportion to profit, its markup
  perturbed by 0.03.
- **Hold-up and ownership.** Closed forms: first-best investment V², held-up (θV)²; in the ownership model each party
  invests its marginal return, half the value of its investment plus the outside option its ownership gives.

## Problems and solutions

**1.** *The yard: q = 2K^0.25 L^0.5. Find MP_L, MP_K and the technical rate of substitution at K = L = 4, and the
returns to scale.*

*Solution.* q(4, 4) = 2·√2·2 = 5.66. MP_L = 0.5q/L = 0.707 and MP_K = 0.25q/K = 0.354, so the TRS is 0.707/0.354 =
2: one shipwright replaces two slipways at the margin. Returns to scale are 0.25 + 0.5 = 0.75, decreasing: doubling
both inputs multiplies output by 2^0.75 = 1.68.

**2.** *Cost minimization: w = 1000, r = 400, q = 8. Find the least-cost K and L, the cost, and check Shephard's lemma
for L.*

*Solution.* The tangency MP_L/MP_K = (b/a)(K/L) = w/r gives K/L = (a/b)(w/r) = 0.5·2.5 = 1.25. Then 8 =
2(1.25L)^0.25 L^0.5 = 2·1.25^0.25·L^0.75, so L = (4/1.057)^(4/3) = 5.89 and K = 7.37. Cost = 1000·5.89 + 400·7.37 =
$8,841.68. In general c = k(w, r) q^(4/3) with k ∝ w^(2/3) r^(1/3), so ∂c/∂w = (2/3)c/w = 5.89 = L.

**3.** *Show that marginal cost cuts average cost at its minimum. For TC = 4000 + 200q + 50q² find the break-even and
shut-down prices.*

*Solution.* d(TC/q)/dq = (MC − TC/q)/q, which is zero exactly where MC = AC, and negative before. Here ATC =
4000/q + 200 + 50q has its minimum where 4000/q² = 50, q = 8.94, at ATC = 200 + 2√(4000·50) = $1,094.43: the
break-even price. AVC = 200 + 50q is lowest as q → 0, so the shut-down price is $200.

**4.** *Play it: with 4 slipways, a price of $1,200 and a wage of $1,000, how many shipwrights maximize profit? How
does the answer change if the wage falls to $800?*

*Solution.* Output with n shipwrights is 2·4^0.25·√n = 2.83√n, so the nth adds 2.83(√n − √(n − 1)): 2.83, 1.17,
0.90, 0.76, 0.67, … worth $3,394, $1,406, $1,079, $909, $801. At $1,000 the third is worth hiring and the fourth is
not: three. At $800 the fourth ($909) and fifth ($801) are worth it and the sixth ($724) is not: five.

**5.** *Supply: for Cobb–Douglas with a + b < 1, show that the long-run supply elasticity is (a + b)/(1 − a − b)
and the short-run b/(1 − b).*

*Solution.* Long run: c = k q^(1/s) with s = a + b, so p = MC = (k/s) q^((1−s)/s) and q ∝ p^(s/(1−s)). Short run with
K fixed: VC = w L = w (q/(A K^a))^(1/b), so MC ∝ q^((1−b)/b) and q ∝ p^(b/(1−b)). For the yard, 3 and 1: the long run
responds more (Le Chatelier).

**6.** *Free entry: demand Q = 400 − 0.2p and the cost above. Find the long-run price, each yard's output and the
number of yards.*

*Solution.* Price falls to the minimum of ATC, $1,094.43; each yard builds 8.94 boats; the market buys 400 −
0.2·1,094.43 = 181.1 boats, so there is room for 181.1/8.94 = 20.25 yards: about twenty, with the twenty-first
unable to cover its costs.

**7.** *Hold-up: value 2V√i, cost i, the investor gets a share θ ex post. Find its investment and the surplus lost, as
a function of θ.*

*Solution.* The investor maximizes θ·2V√i − i, so θV/√i = 1 and i = (θV)². The first best maximizes 2V√i − i: i = V².
Surplus at i is 2V√i − i, so the first best gives V² and the held-up investment 2θV² − θ²V² = V²θ(2 − θ). The loss is
V²(1 − θ)²: at θ = ½ a quarter of the surplus, at θ = 1 nothing.

**8.** ★ *Refit Cobb and Douglas's 1899–1922 data with a time trend and with growth rates. Why does capital's
coefficient turn negative, and what would you need to estimate it credibly?*

*Solution.* With a trend the fit is labour 0.906, capital −0.526, trend 4.7% a year; in growth rates labour 1.40,
capital −1.52. Capital grows almost linearly in logs over the period, so it is nearly collinear with the trend: once
the trend absorbs steady growth, capital's coefficient is identified only from its small wiggles, which move with
the business cycle (capital in place keeps rising in 1908 and 1921 while output falls), so it comes out negative and
imprecise. Felipe and Adams add that the regression may only be recovering the accounting identity of income shares.
A credible estimate needs variation in capital that is not trend or cycle: firm- or plant-level data with input
choices modelled (Olley–Pakes-style proxies), or exogenous shifts in the cost of capital.

## Where it comes back

| Idea | Parts |
|---|---|
| General equilibrium with firms | 9 *The Invisible Hand, Proved* |
| Market power, markups and the price maker | 10 *The Price Maker*, 43 *Measuring Market Power* |
| The production function and growth | 20 *Growth I: Capital*, 21 *Growth II: Ideas and Institutions* |
| Incentives and contracts inside the firm | 14 *Incentives*, 62 *Inside the Firm* |
| Industrial policy and learning by doing | 66 *Geoeconomics and Industrial Policy* |
| AI and the firm | 65 *The Economics of AI* |

## Sources

- C. W. Cobb and P. H. Douglas, "A Theory of Production", *American Economic Review* 18(1), supplement (1928)
  139–165; P. H. Douglas, "The Cobb-Douglas Production Function Once Again: Its History, Its Testing, and Some New
  Empirical Values", *Journal of Political Economy* 84(5) (1976) 903–915; J. Felipe and F. G. Adams, "'A Theory of
  Production': The Estimation of the Cobb-Douglas Function: A Retrospective View", *Eastern Economic Journal* 31(3)
  (2005) 427–445; S. Smirnov and W. Wang, arXiv 1910.06739 (2019), for the data in logs.
- K. J. Arrow, H. B. Chenery, B. S. Minhas and R. M. Solow, "Capital-Labor Substitution and Economic Efficiency",
  *Review of Economics and Statistics* 43(3) (1961) 225–250; H. B. Chenery, "Engineering Production Functions",
  *Quarterly Journal of Economics* 63(4) (1949) 507–531.
- R. L. Hall and C. J. Hitch, "Price Theory and Business Behaviour", *Oxford Economic Papers* 2 (1939) 12–45;
  A. A. Alchian, "Uncertainty, Evolution, and Economic Theory", *Journal of Political Economy* 58(3) (1950) 211–221;
  M. Friedman, "The Methodology of Positive Economics", in *Essays in Positive Economics* (Chicago, 1953), p. 21.
- R. H. Coase, "The Nature of the Firm", *Economica* 4(16) (1937) 386–405; O. E. Williamson, *Markets and
  Hierarchies* (1975) and *The Economic Institutions of Capitalism* (1985).
- B. Klein, R. G. Crawford and A. A. Alchian, "Vertical Integration, Appropriable Rents, and the Competitive
  Contracting Process", *Journal of Law and Economics* 21(2) (1978) 297–326; R. H. Coase, "The Acquisition of Fisher
  Body by General Motors", *Journal of Law and Economics* 43(1) (2000) 15–31; B. Klein, "Fisher-General Motors and the
  Nature of the Firm", same issue, 105–141; R. F. Freeland, "Creating Holdup through Vertical Integration: Fisher Body
  Revisited", same issue; R. Casadesus-Masanell and D. F. Spulber, "The Fable of Fisher Body", same issue.
- S. J. Grossman and O. D. Hart, "The Costs and Benefits of Ownership: A Theory of Vertical and Lateral
  Integration", *Journal of Political Economy* 94(4) (1986) 691–719; O. Hart and J. Moore, "Property Rights and the
  Nature of the Firm", *Journal of Political Economy* 98(6) (1990) 1119–1158; O. Hart, *Firms, Contracts, and
  Financial Structure* (Oxford, 1995).
- D. Gollin, "Getting Income Shares Right", *Journal of Political Economy* 110(2) (2002) 458–474; R. C. Feenstra,
  R. Inklaar and M. P. Timmer, "The Next Generation of the Penn World Table", *American Economic Review* 105(10)
  (2015) 3150–3182; L. Karabarbounis and B. Neiman, "The Global Decline of the Labor Share", *Quarterly Journal of
  Economics* 129(1) (2014) 61–103.
- R. S. Chirinko, "σ: The Long and Short of It", *Journal of Macroeconomics* 30(2) (2008) 671–686; S. Gechert,
  T. Havranek, Z. Irsova and D. Kolcunova, "Measuring Capital-Labor Substitution: The Importance of Method Choices and
  Publication Bias", *Review of Economic Dynamics* 45 (2022) 55–82; E. Oberfield and D. Raval, "Micro Data and Macro
  Technology", *Econometrica* 89(2) (2021) 703–732.
- T. P. Wright, "Factors Affecting the Cost of Airplanes", *Journal of the Aeronautical Sciences* 3(4) (1936)
  122–128; R. Williams Jr., *Chemical Engineering* (December 1947), the first statement of the six-tenths rule as the
  cost-estimation literature cites it.
- J. Haskel and S. Westlake, *Capitalism without Capital* (Princeton, 2018); C. Corrado, C. Hulten and D. Sichel,
  "Intangible Capital and U.S. Economic Growth", *Review of Income and Wealth* 55(3) (2009) 661–685; E. Brynjolfsson,
  D. Li and L. Raymond, "Generative AI at Work", *Quarterly Journal of Economics* 140(2) (2025) 889–942 (NBER Working
  Paper 31161); P. Shahidi, G. Rusak, B. S. Manning, A. Fradkin and J. J. Horton, "The Coasean Singularity? Demand,
  Supply, and Market Design with AI Agents", NBER Working Paper 34468 (2025).

**Data.** The Penn World Table's share of labour compensation in GDP for the United States (LABSHPUSA156NRUG), via
FRED; Cobb and Douglas's indices of output, labour and capital, 1899–1922, as reproduced by Felipe and Adams (2005).

**Textbooks.** Varian, *Intermediate Microeconomics*, chs. 19–24; Mas-Colell, Whinston and Green, *Microeconomic
Theory*, ch. 5; Nicholson and Snyder, *Microeconomic Theory*, chs. 9–11; Hart, *Firms, Contracts, and Financial
Structure*; Williamson, *The Economic Institutions of Capitalism*.
