# Economics, Built: Part 9, The Invisible Hand, Proved

Part 9 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first of Act III, *Markets*. It asks whether a whole economy of selfish traders
can reach a state that nobody could improve on, and whether it will, and answers: it can, and it need not. An
equilibrium in which every market clears exists for any economy of the kind Arrow and Debreu described; it is
efficient if every good has a price, nobody sets prices and everyone knows what they are buying; and in a large
economy it is the only outcome no group can undo. But nothing guarantees there is only one, or that a market finds
it, and efficient is not the same as fair.

It opens in R. A. Radford's prisoner-of-war camps (*Economica*, 1945): equal Red Cross parcels; a padre who walked
round a transit camp in Italy with a tin of cheese and five cigarettes and came back with a complete parcel as
well; cigarettes as the standard of value; "cheese for seven" on the Exchange and Mart boards; one price across a
permanent camp and two cigarettes in twenty across a single hut of a transit camp; the halving of August 1944, the
Bully Mark and the blizzard of February 1945; and the arrival of the 30th U.S. Infantry Division on 12 April 1945.
Nine years later Arrow and Debreu proved that order of that kind can exist in any economy that meets their
conditions. From there it covers:

- a game: four proposed trades between Ana (8 fish, 1.5 baskets of coconuts) and Bo (2 fish, 8.5 baskets), to
  accept or refuse;
- the Edgeworth box: indifference maps, the lens of mutual gains, Pareto efficiency and the contract curve
  (Edgeworth's name, 1881);
- prices: budget lines, offer curves, the competitive equilibrium at 1.018 baskets a fish, Walras's law, and the
  law of one price as a Fact;
- the core of the replicated economy, shrinking to the competitive allocation (Edgeworth's conjecture; Debreu and
  Scarf 1963; Aumann 1964);
- the first welfare theorem proved in five lines, and the assumptions that Act IV relaxes;
- the second welfare theorem: a target allocation, its supporting price, the lump-sum transfer, the separating
  hyperplane, and why such transfers are rare;
- an intermission without narration: Brent and West Texas Intermediate crude, month by month, 1987-2026;
- existence: the price simplex, Brouwer's theorem, Sperner's colouring and Scarf's door-to-door walk;
- stability: the auctioneer, gross substitutes (Arrow, Block and Hurwicz), Scarf's economy that circles for ever,
  and its laboratory test (Anderson, Plott, Shimomura and Granat 2004);
- the whole Island cleared at once, by Newton's method and by the auctioneer;
- production: Crusoe decentralized into a firm and a household;
- anything goes: an economy with three equilibria, and the Sonnenschein-Mantel-Debreu theorem;
- time and uncertainty: Arrow securities share the islanders' weather risk, and a bond alone cannot;
- the calculation debate (Mises, Lange, Hayek) and Kantorovich's linear programme with its resolving multipliers;
- a new dial (the TFP gain from equalizing marginal products: Hsieh and Klenow; Bils, Klenow and Ruane),
  computable general equilibrium models in practice and the 1992 NAFTA forecasts against what happened, and a
  frontier chapter on PPAD, Shapley and Scarf's housing market and Budish's course market.

## Build it

```bash
python -m videos.economics.econ9.compute              # every number (seconds), into .cache/econ9/
python tools/qa_scene.py econ9 Core                   # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ9 -q l   # the whole part, silent preview
python tools/build.py econ9                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 9                     # the lab
```

The data are frozen extracts in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): Brent and West Texas Intermediate crude oil prices,
monthly, via FRED (from the U.S. Energy Information Administration); GDP per head at market prices and at
purchasing-power parity from the World Bank's WDI (2023); and transcribed passages and tables from Radford (1945),
Edgeworth (1881), Hsieh and Klenow (2009), Bils, Klenow and Ruane (2021) and Kehoe (2014), in
`explainer/economics/data/tables.py` with where they were read and the date they were checked.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Can a whole economy of selfish traders reach a state nobody could improve on, and will it? | Radford's camps: Oflags of 1,200 to 2,500 prisoners; the parcel; "Everyone receives a roughly equal share of essentials; it is by trade that individual preferences are given expression and comfort increased"; the padre; "cheese for seven"; the Exchange and Mart board (drawn with Radford's prices); the salmon; August 1944, the Bully Mark at four-fifths of a cigarette, February 1945, 12 April 1945; Arrow and Debreu (1954); the question; objectives |
| 1 | Play it: trade in the box | Ana and Bo; four trades: 2 fish for 1 basket (both gain, more to gain), 4.2 for 4.3 (both gain, efficient, the market's trade to the first decimal), 2 for 6 (Bo refuses), 6 for 1.5 (Ana refuses) |
| 2 | The Edgeworth box | The box (Edgeworth's idea; drawn in this form by Pareto and Bowley); indifference maps; the lens; the trades of Play it inside and outside it; tangency, Pareto efficiency, MRS equal; the contract curve, "which locus it is here proposed to call the contract-curve"; efficient is not fair |
| 3 | Prices: offer curves, equilibrium, Walras's law | At 1.5 baskets a fish Ana sells 4.4 fish and Bo buys 2.6: excess supply 1.8; offer curves cross at 1.018: Ana sells 4.21 fish for 4.29 baskets; Walras (1874); $p_{\text{fish}}z_{\text{fish}} + p_{\text{coco}}z_{\text{coco}} = 0$; the Fact: one price (Brent minus WTI averaged $-1.37$ a barrel in 1987-2010; the 20 poorest countries' price level 0.33 of America's; Agora's villages: fish carried at $1 cost $5.50 and $6.50, haircuts $8 and $4) |
| 4 | The core, and Edgeworth's conjecture | The core of the box: 2.07 to 5.59 fish for Ana; two Anas and one Bo block a deal good for Bo; with 2, 3, 5, 10, 20 copies: 3.27-4.32, 3.48-4.11, 3.62-3.96, 3.71-3.87, 3.75-3.83, around the competitive 3.79; Edgeworth (1881, p. 20); Debreu and Scarf (1963); Aumann (1964) |
| 5 | The first welfare theorem | Both MRS equal the price, 1.018; the five-line proof; what it assumes: a price for everything (Part 15), price-taking (Parts 10, 12), information (Part 13), complete markets (chapter 12, Part 23), and efficient is not fair (Parts 18, 41) |
| 6 | The second welfare theorem | The efficient point with 5 fish and 6.92 baskets for Ana, supported by a price of 0.923; a transfer of 2.65 baskets from Bo; the separating hyperplane between the two better-than sets; convexity; why lump-sum transfers are rare |
| | Intermission: one price for oil? | No narration: Brent and WTI, monthly, May 1987 to October 2026, with the gap below; three notes (usually within a dollar or two for 24 years; 2011-13 and Cushing; new pipelines and exports from December 2015) and a fourth that 2026's spike is too recent to explain; Brent's premium year by year as a tune; the story so far |
| 7 | Existence: Sperner's lemma and Scarf's walk | Three goods and three islanders on the price simplex; excess-demand arrows; the map $f(p)_k = (p_k + \max(z_k,0))/(1 + \sum_j \max(z_j,0))$ and Brouwer (1912); Arrow and Debreu, and McKenzie (1954); Sperner's lemma (1928) as a colouring; the door-to-door walk: 7, 11 and 38 rooms on grids of 6, 12 and 48, errors 0.12, 0.064, 0.007; Scarf (1967) |
| 8 | Does it get there? The auctioneer and Scarf's cycle | Tatonnement $\dot p = z(p)$ converges on the island (Arrow, Block and Hurwicz 1959: gross substitutes); Scarf's three traders who want goods $i$ and $i+1$ together: the prices circle the equal-price equilibrium, with $\sum p^2$ and $p_1p_2p_3$ conserved; Anderson, Plott, Shimomura and Granat (2004) |
| 9 | Computing an equilibrium: the Island cleared at once | Five goods, twelve islanders with CES tastes (elasticities 0.6 to 1.7); prices with fish = 1: coconuts 0.48, timber 0.71, cloth 0.43, salt 0.85; the auctioneer takes 238 steps to a millionth, Newton 6 to $10^{-13}$ |
| 10 | Production: Crusoe decentralized | 12 hours, $c = 2\sqrt{L}$, $0.6\log c + 0.4\log(\text{leisure})$: the plan works 5.14 hours for 4.54 coconuts; the market's wage 0.441, profit 2.27, the same plan; convexity, and increasing returns as the way to market power |
| 11 | Anything goes: Sonnenschein, Mantel and Debreu | Two traders whose excess demand crosses zero at relative prices 1/2, 1 and 2, the middle one unstable; the theorem (Sonnenschein 1973; Mantel 1974; Debreu 1974); no general uniqueness, stability or comparative statics; Kirman (1992); Brown and Matzkin (1996) |
| 12 | Time and uncertainty: Arrow's securities | Ana's fishing (80 calm, 20 storm) and Chidi's coconuts (20, 80); contingent goods (Arrow 1953, Debreu 1959); two Arrow securities at 0.475; Ana sells 30 calm claims and buys 30 storm claims; both eat 50 in either weather, as good as 50 a year for sure against 39.25 without trade; a bond alone is not traded, and shares nothing |
| 13 | The calculation debate: Mises, Lange, Hayek and Kantorovich | Mises (1920), Lange (1936-37), Hayek (1945): "a system of telecommunications"; Kantorovich's programme for the yard's four machines: 5 sets a day against 2.85; the dual's values (saw 2.00, adze 1.33, lathe 0.67, press 1.00; a plank and a mast a third of a set each); 1975, with Koopmans; information and incentives |
| 14 | The Dials: what misallocation costs | Equal marginal products as the first theorem for firms; $\log(Y_{\text{eff}}/Y) = \tfrac{\sigma}{2}s^2$; 100,000 simulated plants: 43% with America's 1997 spread, 83% with China's 2005; Hsieh and Klenow: China 30.5% and India 59.2% to US efficiency, full equalization 42.9%, 86.6%, 127.5%; Bils, Klenow and Ruane: measurement error a fifth of India's gap and three fifths of America's: contested |
| 15 | In practice: general equilibrium models, and NAFTA | CGE models: built on input-output tables, calibrated, used for trade, taxes and carbon; Called it?: Sobarzo's 1992 forecasts against 1989-2009 (median +95%, tobacco +576%; weighted correlation $-0.12$, unweighted $-0.39$ from the table); the new-goods margin (Kehoe and Ruhl), whose rule correlates 0.47 |
| 16 | Frontier: hard equilibria, and markets without money | PPAD (Papadimitriou 1994); Nash equilibrium PPAD-complete (Daskalakis, Goldberg and Papadimitriou; Chen and Deng); markets as hard (Chen, Dai, Du and Teng 2009); Shapley and Scarf's housing market with Gale's top trading cycles on six huts, in three rounds; Roth (1982); Budish's approximate competitive equilibrium from equal incomes and Course Match |
| | Recap, problems, and the road ahead | The answer; twelve lines; problems; reading; Dupuit's roofless carriages, and Part 10 |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's general equilibrium (`explainer.economics.agora.ge`),
with the Island's Part 9 truths in `explainer.economics.island`, or from the Data Room or a transcribed table; the
narration states the cached numbers.

- **The box.** Cobb-Douglas traders; the contract curve in closed form; the lens's ends by root-finding along it;
  the equilibrium price in closed form; offer curves by demand at 300 prices.
- **The core.** For $r$ copies of each trader, a contract-curve allocation is blocked if some coalition of $s$ Anas
  and $t$ Bos ($s, t \le r$, $s \ne t$), treating members of a type alike, can give its Bos what the allocation gave
  them and leave its Anas better off; the best such deal for the Anas is found on a grid of 2,001 points along the
  Bos' indifference curve and refined; the core's two ends by bisection.
- **Existence.** Grid points of the simplex labelled by the first good with a positive price that is not in excess
  demand (a Sperner labelling, checked); Scarf's walk from the first door on the face where timber is free; the
  exact equilibrium by Newton's method.
- **Dynamics.** Tatonnement $\dot p = z(p)$ by an adaptive Runge-Kutta solver (relative tolerance $10^{-9}$);
  Scarf's economy with Leontief traders; the island's auctioneer by Euler steps of 0.1 $z(p)$.
- **The rest.** Crusoe's wage by root-finding on the labour market; the three-equilibrium economy in closed form
  (endowments $(2, r)$ and $(r, 2)$ with $r = 2^{8/9} - 2^{1/9}$, utilities $x - y^{-8}/8$ and $y - x^{-8}/8$);
  Arrow-Debreu state prices by solving the clearing conditions, the bond economy by its first-order conditions;
  Kantorovich's programme by HiGHS with its duals; the misallocation simulation with labour only and $\sigma = 3$;
  top trading cycles by the algorithm; the villages of the Fact with demand $12 - p$ and a carrying cost of $1.

## Problems and solutions

**1.** *The box: Ana spends a share $a$ of her wealth on fish, Bo a share $b$, and there are $X$ fish and $Y$
baskets. Show that the contract curve is $y = \frac{k_B x Y}{k_A (X - x) + k_B x}$ with $k = \tfrac{a}{1-a}$, and
find it for Ana and Bo.*

*Solution.* Ana's marginal rate of substitution at $(x, y)$ is $k_A\,y/x$; Bo holds $(X - x, Y - y)$, so his is
$k_B (Y - y)/(X - x)$. Setting them equal, $k_A y (X - x) = k_B x (Y - y)$, so $y\,[k_A (X - x) + k_B x] = k_B x Y$.
For Ana and Bo, $k_A = 2/3$ and $k_B = 3/2$, so $y = 15x/(\tfrac{20}{3} + \tfrac{5}{6}x)$: it runs from Ana's corner
to Bo's, bowing above the diagonal because Bo cares more for fish.

**2.** *Equilibrium: derive the competitive price $p = \frac{a\,e_{A2} + b\,e_{B2}}{(1-a)\,e_{A1} + (1-b)\,e_{B1}}$
(fish in baskets) and check it for Ana and Bo.*

*Solution.* With coconuts as numeraire, Ana's wealth is $p e_{A1} + e_{A2}$ and she demands $a(p e_{A1} + e_{A2})/p$
fish; Bo likewise. The fish market clears when $a(p e_{A1} + e_{A2}) + b(p e_{B1} + e_{B2}) = p(e_{A1} + e_{B1})$,
that is $p[(1-a) e_{A1} + (1-b) e_{B1}] = a e_{A2} + b e_{B2}$. For Ana and Bo: $p = (0.4 \cdot 1.5 + 0.6 \cdot 8.5)
/(0.6 \cdot 8 + 0.4 \cdot 2) = 5.7/5.6 = 1.018$. Ana then holds $0.4 \cdot 9.643/1.018 = 3.79$ fish and $0.6 \cdot
9.643 = 5.79$ baskets.

**3.** *Walras's law: show that $p \cdot z(p) = 0$ for any prices, and that only relative prices matter.*

*Solution.* Each trader's demand satisfies the budget, $p \cdot x_i(p) = p \cdot e_i$ (with more always better, the
whole budget is spent). Summing, $p \cdot \sum_i (x_i(p) - e_i) = p \cdot z(p) = 0$. Multiplying every price by
$\lambda > 0$ multiplies every budget by $\lambda$ and leaves the budget sets, and so the demands, unchanged:
$z(\lambda p) = z(p)$. So prices can be scaled to add to one, and $n$ goods have $n - 1$ relative prices.

**4.** *The first welfare theorem: where does the proof use local nonsatiation? Give an economy where the theorem
fails without it.*

*Solution.* In step 2: a trader who is indifferent between $x'_i$ and her equilibrium bundle cannot find $x'_i$
cheaper than her wealth, because if she could, local nonsatiation would put something slightly better within her
budget, contradicting her choice. Without it, take two traders, each with 5 of each good; Ana's utility is
$\min(x, 3) + \min(y, 3)$, so she is satiated at $(3, 3)$, and Bo's is $\log x + \log y$. At equal prices both may
keep their endowments (Ana is indifferent among all her affordable bundles that include $(3, 3)$), so no trade is an
equilibrium; but moving $(2, 2)$ from Ana to Bo makes Bo better off and Ana no worse: the equilibrium is not
Pareto efficient.

**5.** *The second theorem: find the transfer that makes the efficient point with 5 fish for Ana an equilibrium.*

*Solution.* On the contract curve at $x = 5$, $y = 15 \cdot 5/(\tfrac{20}{3} + \tfrac{25}{6}) = 6.923$. The common
MRS there is $k_A y/x = \tfrac{2}{3} \cdot 6.923/5 = 0.923$ baskets a fish, the supporting price. Ana's budget line
must pass through the target, so her wealth at that price must be $0.923 \cdot 5 + 6.923 = 11.54$ baskets; she has
$0.923 \cdot 8 + 1.5 = 8.88$. A transfer of $2.65$ baskets from Bo to Ana, before trade, does it, and at that price
each then demands exactly the target.

**6.** *Scarf's economy: show that $\sum_k p_k^2$ and $p_1 p_2 p_3$ are constant along the auctioneer's path.*

*Solution.* Along $\dot p = z(p)$, $\tfrac{d}{dt}\sum_k p_k^2 = 2\,p \cdot z(p) = 0$ by Walras's law. For the product,
$\tfrac{d}{dt}\log(p_1p_2p_3) = \sum_j z_j/p_j$. Trader $j$ demands $p_j/(p_j + p_{j+1})$ of goods $j$ and $j+1$, so
$z_j = \frac{p_j}{p_j + p_{j+1}} + \frac{p_{j-1}}{p_{j-1} + p_j} - 1$ and $z_j/p_j = \frac{1}{p_j + p_{j+1}} -
\frac{1}{p_{j-1} + p_j}$; summed round the cycle of three goods, the terms cancel. Two conserved quantities pin the
path to a closed curve around equal prices.

**7.** *Arrow securities: with no aggregate risk and equal patience and risk aversion, show that complete markets give
full insurance, and find the securities' prices.*

*Solution.* Trader $i$'s first-order conditions are $\beta \pi_s u'(c_{is}) = \lambda_i q_s$ and $u'(c_{i0}) =
\lambda_i$. If every trader consumes the same in every state and the total in each state is the same, then
$c_{is} = c_{i0}$ is consistent with clearing and $q_s = \beta \pi_s$. For Ana and Chidi, with 50 today and 100 in
total in each state, both consume 50 everywhere and $q_s = 0.95 \cdot 0.5 = 0.475$; Ana sells 30 calm-state claims
and buys 30 storm-state claims, which cost the same, so her trade is self-financing.

**8.** ★ *Kantorovich: write the dual of the boatyard's programme, and show that a machine works on a part only if its
day's value there equals the machine's price.*

*Solution.* The primal: maximize $z$ subject to $\sum_j t_{ij} \le 1$ for each machine (multiplier $\lambda_i$),
$k_j z \le \sum_i r_{ij} t_{ij}$ for each part ($\mu_j$), $t, z \ge 0$. The dual: minimize $\sum_i \lambda_i$
subject to $\lambda_i \ge r_{ij}\mu_j$ for every machine and part, $\sum_j k_j \mu_j \ge 1$, $\lambda, \mu \ge 0$.
Complementary slackness: $t_{ij} > 0$ only if $\lambda_i = r_{ij}\mu_j$, and since $\lambda_i \ge r_{ij}\mu_j$ for
every $j$, a machine works only where its day is worth the most. For the yard, $\mu = (\tfrac13, \tfrac13)$ and
$\lambda = (2, \tfrac43, \tfrac23, 1)$: the saw's day is worth 2 on planks and $\tfrac13$ on masts, the press's
$\tfrac13$ and 1, and the lathe's $\tfrac23$ either way; $\sum_i \lambda_i = 5$, the number of sets, as strong
duality requires.

## Where it comes back

| Idea | Parts |
|---|---|
| Market power and the price maker | 10 *The Price Maker*, 12 *Competition among the Few* |
| Games and Nash equilibrium | 11 *Games* |
| The failures of the first theorem | 13 *Lemons and Signals*, 14 *Incentives*, 15 *Spillovers* |
| Markets by design | 16 *Auctions*, 17 *Markets by Design* |
| Fairness and social choice | 18 *Social Choice and Welfare*, 41 *Taxes* |
| Misallocation and growth | 21 *Growth II: Ideas and Institutions* |
| The prices of risk | 23 *Capital and Asset Prices*, 33 *Crises* |
| Trade and the new-goods margin | 35 *Trade I*, 36 *Trade II* |

## Sources

- R. A. Radford, "The Economic Organisation of a P.O.W. Camp", *Economica*, New Series 12(48) (1945) 189-201.
- F. Y. Edgeworth, *Mathematical Psychics* (London, 1881), pp. 20-21; L. Walras, *Éléments d'économie politique
  pure* (Lausanne, 1874).
- K. J. Arrow and G. Debreu, "Existence of an Equilibrium for a Competitive Economy", *Econometrica* 22(3) (1954)
  265-290; L. W. McKenzie, "On Equilibrium in Graham's Model of World Trade and Other Competitive Systems",
  *Econometrica* 22(2) (1954); G. Debreu, *Theory of Value* (1959).
- G. Debreu and H. Scarf, "A Limit Theorem on the Core of an Economy", *International Economic Review* 4(3) (1963); R. J. Aumann, "Markets with a Continuum of Traders", *Econometrica* 32(1/2) (1964).
- K. J. Arrow, H. D. Block and L. Hurwicz, "On the Stability of the Competitive Equilibrium, II", *Econometrica*
  27(1) (1959); H. Scarf, "Some Examples of Global Instability of the Competitive Equilibrium",
  *International Economic Review* 1(3) (1960); H. Scarf, "The Approximation of Fixed Points of a Continuous
  Mapping", *SIAM Journal on Applied Mathematics* 15(5) (1967), and *The Computation of Economic Equilibria*
  (1973); C. M. Anderson, C. R. Plott, K.-I. Shimomura and S. Granat, "Global Instability in Experimental General
  Equilibrium: The Scarf Example", *Journal of Economic Theory* 115(2) (2004) 209-249.
- H. Sonnenschein, "Do Walras' Identity and Continuity Characterize the Class of Community Excess Demand
  Functions?", *Journal of Economic Theory* 6(4) (1973); R. Mantel, "On the Characterization of Aggregate
  Excess Demand", *Journal of Economic Theory* 7(3) (1974); G. Debreu, "Excess Demand Functions", *Journal of
  Mathematical Economics* 1(1) (1974); A. Kirman, "Whom or What Does the Representative Individual Represent?",
  *Journal of Economic Perspectives* 6(2) (1992); D. J. Brown and R. L. Matzkin, "Testable Restrictions on the
  Equilibrium Manifold", *Econometrica* 64(6) (1996).
- K. J. Arrow, "Le rôle des valeurs boursières pour la répartition la meilleure des risques" (1953), translated as
  "The Role of Securities in the Optimal Allocation of Risk-bearing", *Review of Economic Studies* 31(2) (1964).
- L. von Mises, "Die Wirtschaftsrechnung im sozialistischen Gemeinwesen" (1920); O. Lange, "On the Economic Theory of
  Socialism", *Review of Economic Studies* 4(1) and 4(2) (1936-37); F. A. Hayek, "The Use of Knowledge in Society",
  *American Economic Review* 35(4) (1945) 519-530; L. V. Kantorovich, *Mathematical Methods of Organizing and
  Planning Production* (Leningrad, 1939), translated in *Management Science* 6(4) (1960).
- C.-T. Hsieh and P. J. Klenow, "Misallocation and Manufacturing TFP in China and India", *Quarterly Journal of
  Economics* 124(4) (2009) 1403-1448 (read in the December 2008 accepted version); M. Bils, P. J. Klenow and C.
  Ruane, "Misallocation or Mismeasurement?", *Journal of Monetary Economics* 124(S) (2021) S39-S56 (NBER Working Paper
  26711, 2020).
- T. J. Kehoe, "An Evaluation of the Performance of Applied General Equilibrium Models of the Impact of NAFTA", in
  *Frontiers in Applied General Equilibrium Modeling* (Cambridge, 2005); T. J. Kehoe, "The Challenges of Predicting
  the Impact of Trade Reforms", in *NAFTA at 20* (Federal Reserve Bank of Dallas, 2014), table 1; USITC publication
  2516 (1992).
- C. H. Papadimitriou, "On the Complexity of the Parity Argument and Other Inefficient Proofs of Existence", *Journal
  of Computer and System Sciences* 48(3) (1994); C. Daskalakis, P. W. Goldberg and C. H. Papadimitriou, "The
  Complexity of Computing a Nash Equilibrium", *SIAM Journal on Computing* 39(1) (2009); X. Chen, D. Dai, Y.
  Du and S.-H. Teng, "Settling the Complexity of Arrow-Debreu Equilibria in Markets with Additively Separable
  Utilities", FOCS (2009); L. Shapley and H. Scarf, "On Cores and Indivisibility", *Journal of Mathematical
  Economics* 1(1) (1974); A. E. Roth, "Incentive Compatibility in a Market with Indivisible Goods", *Economics
  Letters* 9(2) (1982); E. Budish, "The Combinatorial Assignment Problem: Approximate Competitive Equilibrium
  from Equal Incomes", *Journal of Political Economy* 119(6) (2011); E. Budish, G. P. Cachon, J. B. Kessler
  and A. Othman, "Course Match", *Operations Research* 65(2) (2017).
- U.S. Energy Information Administration, crude oil prices (Brent, WTI), via FRED; the World Bank, World
  Development Indicators (GDP per head at market prices and at PPP, 2023).
