# Economics, Built: Part 10, The Price Maker

Part 10 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second of Act III, *Markets*. It asks what a seller does when the price is
hers to set, and answers: she raises it above cost until the revenue from one more sale is just its cost, and the
buyers she turns away are the economy's loss. Then, wherever she can tell buyers apart or make them sort
themselves, she charges them differently, and each step takes more of their surplus and wastes less of it. What
limits her is how much she knows, what she can credibly promise, and the regulator.

It opens with Jules Dupuit, an engineer of the French corps of bridges and roads: in 1844 he argued that a bridge
is worth what crossing it is worth to everyone who crosses, and that a toll on a crossing that costs nothing turns
away value for no saving (consumer surplus and deadweight loss in one argument); in 1849 he explained the
third-class carriages without roofs as a way to keep anyone who could pay for second class from travelling third.
From there it covers:

- a game: set one fare for Bo's ferry, against the values of a hundred islanders;
- marginal revenue, the monopoly price, the absence of a supply curve, and the Lerner index;
- what monopoly costs: Harberger's triangles (1954) and Posner's rectangles (1975), with Tullock (1967);
- first-degree discrimination, efficient and all to the seller; Pigou's three degrees (1920);
- third-degree discrimination for students and townsfolk, a market opened, and Schmalensee's and Varian's tests;
- second-degree discrimination: a two-type screening menu (Mussa and Rosen 1978), the quality of the bottom of the
  menu cut on purpose, information rents, and Deneckere and McAfee's damaged goods (1996);
- an intermission without narration: green arabica beans and ground coffee on American shelves, month by month,
  1980-2026;
- two-part tariffs (Oi's Disneyland, 1971), for identical and for different visitors;
- bundling (Stigler 1963; Adams and Yellen 1976), on two visitors and on four hundred;
- durable goods and the Coase conjecture (1972), solved in Agora for price changes once a year to every day, and
  the ways a durable-goods monopolist ties its own hands;
- natural monopoly, average-cost pricing, and Ramsey-Boiteux prices;
- regulation: rate of return and gold plating (Averch and Johnson 1962), price caps (Littlechild 1983);
- monopsony in one diagram, with a minimum wage that raises both pay and employment;
- pass-through: a half for straight-line demand and one and a half for constant elasticity; incomplete pass-through
  as a Fact, measured on coffee (0.15 in a quarter, 0.55 after six), and Nakamura and Zerom's accounting (2010);
- a new dial (markups over marginal cost: De Loecker, Eeckhout and Unger; Traina), revenue management by
  Littlewood's rule (1972) in practice, and a frontier chapter on personalized prices learned from an experiment
  (Dubé and Misra 2023) and pricing algorithms (Calvano, Calzolari, Denicolò and Pastorello 2020; Assad, Clark,
  Ershov and Xu 2024).

## Build it

```bash
python -m videos.economics.econ10.compute              # every number (seconds), into .cache/econ10/
python tools/qa_scene.py econ10 ThirdDegree            # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ10 -q l   # the whole part, silent preview
python tools/build.py econ10                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 10                     # the lab
```

The data are frozen extracts in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): the average retail price of ground roast coffee in
U.S. cities (BLS, via FRED, series APU0000717311) and the World Bank's Pink Sheet price of arabica coffee, both
monthly; and transcribed passages from De Loecker, Eeckhout and Unger (2020), Traina (2018), Nakamura and Zerom
(2010) and Dubé and Misra (2023), in `explainer/economics/data/tables.py` with where they were read and the date
they were checked.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | What does a seller do when the price is hers to set? | Dupuit (1844): what a bridge is worth, and a toll that turns crossings away; Dupuit (1849): third-class carriages without roofs; the menu everywhere (seats, software, student fares, coupons, joining fees, bundles, personal prices); the question; objectives |
| 1 | Play it: set the fare for Bo's ferry | A hundred islanders' values; fares of $2, $4, $5, $6, $8: 82, 64, 52, 38 and 23 crossings, takings $164, $256, $260, $228, $184; the best fare $5.59 for $268; at $5, 48 stay home and $125 of value is lost |
| 2 | Marginal revenue and the monopoly price | Demand $q = 100 - 10p$; the green and red strips; $MR$ falls twice as fast as demand; 50 crossings at $5 for $250 a day against 100 at cost; with a $2 cost, 40 at $6; no supply curve; $MR = p(1 + 1/\varepsilon)$ and the Lerner index (1934): $4/6 = 1/1.5$ |
| 3 | What monopoly costs: Harberger's triangles and Posner's rectangles | Takings $250, passengers' surplus $125, deadweight loss $125 of the $500; Harberger (1954): under a tenth of one percent of national income; Posner (1975) and Tullock (1967): rent-seeking, a loss of $125 to $375 a day |
| 4 | First-degree discrimination: a price for every buyer | One fare: 52 cross for $260; a price for each: $9.91 down to a few cents, everyone crosses, Bo takes all $514, no deadweight loss; knowledge and no resale; Pigou (1920) |
| 5 | Third-degree discrimination: students and townsfolk | Students $q = 60 - 10p$, townsfolk $q = 100 - 5p$, cost $1; one fare $10.50 serves no student; two fares $3.50 and $10.50; crossings 47.5 to 72.5, profit $451 to $514, surplus $226 to $257, total $677 to $771; Schmalensee (1981), Varian (1985) |
| 6 | Second-degree discrimination: menus that sort | Seven in ten value comfort at $1 a unit, three in ten at $2; cost $q^2/2$; with types seen: deck 1 unit for $1, cabin 2 for $4; the menu: deck 0.57 for $0.57, cabin 2 for $3.43, rent $0.57, profit $0.71 against $0.95; Mussa and Rosen (1978); Deneckere and McAfee (1996) |
| | Intermission: from bean to shelf | No narration: green arabica and ground coffee on the shelf, in dollars a pound, monthly, 1980-2026; the shelf price year by year as a tune; the story so far |
| 7 | Two-part tariffs: Oi's Disneyland | Demand $10 - p$, cost $2$: one price $6$ for $16$; rides at cost and a $32$ fee for $32$; two ordinary visitors to one keen one ($16 - p$): rides at cost and a $32 fee bring $96, rides at $4 and an $18 fee $102, and the keen visitor alone at a fee of $98 less |
| 8 | Bundling | Ana ($8, $2) and Chidi ($2, $8): $16 separately, $20 for a $10 bundle; 400 visitors: negatively correlated values $2,040 separately and $3,245 bundled, positively correlated slightly less bundled; mixed bundling; Stigler (1963), Adams and Yellen (1976) |
| 9 | Durable goods and the Coase conjecture | Boats valued uniformly to $1,000; $500 once; buyers wait; Agora's equilibrium at 10% a year over thirty years: first prices $239, $139, $88, $49, $30 for one, four, twelve, 52 and 365 price changes a year; Coase (1972), Stokey (1981), Bulow (1982), Gul, Sonnenschein and Wilson (1986); renting, commitment, planned obsolescence (Bulow 1986), reputation |
| 10 | Natural monopoly and Ramsey prices | Pipes at $200 a day and $1 a unit; marginal-cost pricing leaves the pipes unpaid, average cost $3.81; households ($\varepsilon = 1.5$) and boatyards ($\varepsilon = 4$) covering a fixed cost of 40: Ramsey markups 40% and 15% of the price, a loss of 17.5 a day against 33 with one markup; Ramsey (1927), Boiteux (1956) |
| 11 | Regulating a monopoly | Rate-of-return regulation with an allowed return 1.4 above the cost of capital 1.0: capital per worker 0.75 (least cost) becomes 1.07, 43% more; Averch and Johnson (1962); RPI $-$ X price caps (Littlechild 1983), the ratchet, Part 14 |
| 12 | Monopsony: one employer | Labour supply $w = 5 + 0.1L$, a shipwright adds $25: 100 hired at $15 against 200 at $25; a $18 minimum wage: 130 hired; Robinson (1933); Part 38 |
| 13 | Pass-through: who pays when costs rise? | $\rho = dp/dc$: 0.5 for straight-line demand, 1.5 for constant elasticity 3; the Fact: incomplete pass-through, with coffee (522 months, the bean price swinging by a factor of almost eight); quarterly distributed lags: 0.15 at once, 0.55 after six quarters; in dollars $1.64 per $1 a pound of beans, against 1.19 pounds of beans in a pound of roast coffee; Nakamura and Zerom: local costs cut long-run pass-through by 59%, markups by a further 33% |
| 14 | The Dials: how large are markups? | $\mu = \theta_V\,pQ/(P_V V)$, checked on an Agora firm (1.25); De Loecker and Warzynski (2012), Hall (1988); De Loecker, Eeckhout and Unger: 1.21 in 1980, 1.61 in 2016, average profits 1% to 8%, the median unchanged; Traina: flat or falling with SG&A and reweighting: contested |
| 15 | In practice: fare classes and revenue management | Fences: advance purchase, Saturday stays, refunds; Littlewood (1972): 40 seats, $4 and $10, late demand $12 \pm 5$; protect 13 seats, expected takings $160 to $213; Part 60 |
| 16 | Frontier: prices set by machine learning | Dubé and Misra (2023): randomized prices, a model of demand, personal prices: profit +19% against the best single price and +86% against the old price, consumer surplus down, more than 60% better off; Agora's experiment: 8,000 buyers shown random prices, a logit, profit +23%, buyers served 49% to 65%, 66% pay less, consumer surplus $-6$%; Calvano et al. (2020); Assad et al. (2024) |
| | Recap, problems, and the road ahead | The answer; twelve lines; problems; reading; Flood and Dresher's game at RAND, and Part 11 |

There is no *Called it?* in this part: the theory of a single seller makes no dated public forecast that can be
checked against what followed. The Fact (incomplete pass-through) and the dial (markups) carry its contact with
data.

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's price maker (`explainer.economics.agora.pricing`),
with the Island's Part 10 truths in `explainer.economics.island`, or from the Data Room or a transcribed table; the
narration states the cached numbers.

- **The ferry.** A hundred values drawn from the Island's seed and sorted; crossings and takings at each fare, and the
  revenue curve on a grid of fares.
- **One price.** The monopoly price, quantity, profit, consumer surplus and deadweight loss in closed form for
  straight-line demand, and numerically for constant elasticity; the Lerner index checked against $-1/\varepsilon$
  at the optimum; pass-through by a central difference in the cost.
- **Discrimination.** Third degree by each group's own monopoly problem, and the single price by the better of
  serving one group or both; the two-type screening menu in closed form; two-part tariffs by maximizing over the
  ride price with the fee set to the smaller visitor's surplus; bundling by searching separate prices, bundle
  prices and mixed menus on a grid of 121 prices for 400 visitors with correlated values.
- **Time.** The Coase equilibrium by backward induction over the skimming path for each number of price changes a
  year, with thirty years of selling.
- **Natural monopoly and regulation.** Ramsey prices by root-finding on the common factor $k$ that just covers the
  fixed cost, against the uniform markup that does; the Averch-Johnson firm by maximizing profit subject to the
  allowed return; monopsony in closed form.
- **Coffee.** BLS's ground coffee price and the Pink Sheet's arabica price (converted from dollars a kilogram to
  dollars a pound) matched by month, averaged by quarter; the change in the log shelf price regressed on the current
  and six lagged changes in the log bean price (and the same in dollars), by least squares.
- **Markups and revenue management.** The production-approach formula checked on a firm with output $K^{0.3}M^{0.5}$,
  capital fixed, and demand of elasticity 5; Littlewood's rule from the normal quantile, and expected takings for
  every protection level from 200,000 simulated evenings.
- **Personal prices.** Six standard normal features, three of which shift a log-logistic willingness to pay; 8,000
  buyers shown prices drawn from 116 prices between $0.50 and $12; a logit of purchase on the features and the log
  price by Newton's method; each of 200,000 new buyers priced at the fitted model's best price, against the best
  single price, with profit and surplus realized on their simulated values.

## Problems and solutions

**1.** *One price: with demand $q = a - b\,p$ and marginal cost $c$, show that $p^* = \tfrac{1}{2}(a/b + c)$, that
$(p^* - c)/p^* = 1/\varepsilon$ there, and that the deadweight loss is a quarter of the competitive surplus.*

*Solution.* Inverse demand is $p = (a - q)/b$, so revenue is $q(a - q)/b$ and $MR = (a - 2q)/b$. Setting
$MR = c$ gives $q^* = (a - bc)/2$ and $p^* = (a - q^*)/b = \tfrac{1}{2}(a/b + c)$. The elasticity's size there is
$b\,p^*/q^*$, and $1/\varepsilon = q^*/(b p^*) = \tfrac{1}{2}(a/b - c)/p^* = (p^* - c)/p^*$. The competitive quantity is
$a - bc = 2q^*$, so the deadweight loss is $\tfrac{1}{2}(p^* - c)(q^*) = \tfrac{1}{2}\cdot\tfrac{a - bc}{2b}\cdot
\tfrac{a - bc}{2} = \tfrac{(a - bc)^2}{8b}$, and the competitive surplus is $\tfrac{(a - bc)^2}{2b}$: a quarter. For
the ferry ($a = 100$, $b = 10$, $c = 0$): $p^* = 5$, a loss of 125 of 500.

**2.** *Third degree: students $q = 60 - 10p$, townsfolk $q = 100 - 5p$, $c = 1$. Show that one price serves only the
townsfolk, and that two prices raise welfare.*

*Solution.* Separately, each group's price is halfway between its choke price and cost: students $(6 + 1)/2 = 3.50$
(25 crossings, profit 62.5), townsfolk $(20 + 1)/2 = 10.50$ (47.5 crossings, profit 451.25). With one price, serving
both means $p < 6$ and demand $160 - 15p$, whose best price is $(160/15 + 1)/2 = 5.83$, for a profit of
$4.83 \times 72.5 = 350.4$; serving only the townsfolk at 10.50 earns 451.25, so the single price is 10.50 and no student
crosses. Welfare with one price is $451.25 + 225.6 = 676.9$; with two it adds the students' market, $62.5 + 31.25$,
for 770.6. Output rises from 47.5 to 72.5, as Varian's condition requires.

**3.** *Screening: types $\theta_L < \theta_H$, a share $s$ high. Show $q_L = \theta_L - \tfrac{s}{1-s}(\theta_H -
\theta_L)$ and that the high type's rent is $(\theta_H - \theta_L)\,q_L$.*

*Solution.* A type-$\theta$ buyer values quality $q$ at $\theta q$; it costs $q^2/2$. At the optimum the low type's
participation binds, $t_L = \theta_L q_L$, and the high type's incentive constraint binds, $t_H = \theta_H q_H -
(\theta_H - \theta_L) q_L$: the high type must get at least what it would from the low option. Profit per buyer is
$(1 - s)(\theta_L q_L - q_L^2/2) + s(\theta_H q_H - (\theta_H - \theta_L) q_L - q_H^2/2)$. Its derivative in $q_H$
gives $q_H = \theta_H$ (no distortion at the top), and in $q_L$ gives $(1 - s)(\theta_L - q_L) = s(\theta_H -
\theta_L)$, the stated $q_L$. The rent is the high type's surplus, $\theta_H q_H - t_H = (\theta_H - \theta_L) q_L$.
For $\theta = 1, 2$ and $s = 0.3$: $q_L = 1 - \tfrac{3}{7} = 0.571$, rent 0.571.

**4.** *Oi: two buyers with $q = 10 - p$ and one with $q = 16 - p$, cost 2. Show that the best tariff that keeps all
three is a price of 4 and a fee of 18, and that it beats shutting the two out.*

*Solution.* If all three are to come, the fee can be at most an ordinary buyer's surplus at the ride price $p$,
$(10 - p)^2/2$. Profit is $3 \cdot (10 - p)^2/2 + (p - 2)\,[2(10 - p) + (16 - p)] = \tfrac{3}{2}(10 - p)^2 + (p - 2)(36 -
3p)$. Its derivative is $-3(10 - p) + (36 - 3p) - 3(p - 2) = 12 - 3p$, zero at $p = 4$. The fee is $36/2 = 18$, and
profit is $54 + 2 \times 24 = 102$, against 96 with rides at cost. Shutting the ordinary buyers out, the keen one is
charged at cost with a fee equal to their whole surplus, $14^2/2 = 98$: less than 102. (With one ordinary buyer to
one keen one, the comparison reverses: 73 against 98, and the park would rather lose the ordinary visitor.)

**5.** *Coase in two periods: values uniform on $[0, 1]$, discount $\delta$. Show that the first price is
$\frac{(2-\delta)^2}{2(4 - 3\delta)}$, below $\tfrac{1}{2}$.*

*Solution.* Suppose buyers above $v_1$ buy in period 1. In period 2 the seller faces values uniform on $[0, v_1]$
and charges $p_2 = v_1/2$. The marginal buyer $v_1$ is indifferent: $v_1 - p_1 = \delta(v_1 - v_1/2)$, so
$p_1 = v_1(1 - \delta/2)$. The seller maximizes $p_1(1 - v_1) + \delta\,p_2(v_1 - p_2) = v_1(1 - \delta/2)(1 - v_1) +
\delta v_1^2/4$, whose first-order condition is $(1 - \delta/2)(1 - 2v_1) + \delta v_1/2 = 0$, so $v_1 = \frac{2 -
\delta}{4 - 3\delta}$ and $p_1 = \frac{(2 - \delta)^2}{2(4 - 3\delta)}$. At $\delta = 0$ it is $\tfrac12$; its
derivative in $\delta$ is negative on $(0, 1)$, so it is below $\tfrac12$ there ($0.465$ at $\delta = 0.9$).

**6.** *Ramsey: minimize the deadweight loss of two prices subject to covering a fixed cost, and derive
$\frac{p_i - c_i}{p_i} = \frac{k}{\varepsilon_i}$.*

*Solution.* With independent demands, maximize total surplus $\sum_i [CS_i(p_i) + (p_i - c_i) q_i(p_i)]$ subject
to $\sum_i (p_i - c_i) q_i(p_i) = F$. With multiplier $\lambda$ and $CS_i' = -q_i$, the first-order condition for
$p_i$ is $-q_i + (1 + \lambda)[q_i + (p_i - c_i) q_i'] = 0$, so $(p_i - c_i) q_i' = -\tfrac{\lambda}{1 + \lambda}
q_i$. Dividing by $p_i q_i$ and writing $\varepsilon_i = -p_i q_i'/q_i$: $\frac{p_i - c_i}{p_i} = \frac{k}{\varepsilon_i}$
with $k = \tfrac{\lambda}{1 + \lambda}$, the same for every product; $k = 0$ when $F = 0$ (marginal-cost prices),
and $k = 1$ gives the monopoly prices.

**7.** *Littlewood: derive the rule from the last seat kept back, and find it for $4 and $10 fares and late demand
$N(12, 5^2)$.*

*Solution.* With $y$ seats protected, the $y$-th protected seat earns $p_{\text{hi}}$ if late demand reaches $y$,
and nothing otherwise, so its expected value is $p_{\text{hi}} P(D \ge y)$; selling it now to an early buyer earns
$p_{\text{lo}}$ for sure. Keep protecting while $p_{\text{hi}} P(D \ge y) \ge p_{\text{lo}}$, that is, while $P(D \ge
y) \ge p_{\text{lo}}/p_{\text{hi}}$. Since $P(D \ge y)$ falls with $y$, the rule is $y^* = F^{-1}(1 -
p_{\text{lo}}/p_{\text{hi}})$. Here $1 - 0.4 = 0.6$, $z_{0.6} = 0.253$, so $y^* = 12 + 5 \times 0.253 = 13.3$: protect 13
seats, as Agora's simulation finds.

**8.** ★ *Personal prices: if $\log v = a + s\,e$ with $e$ logistic, show that at its best personal price every buyer
buys with probability $1 - s$, and compare with Agora's 65%.*

*Solution.* A buyer buys at $p$ if $v \ge p$, that is $e \ge (\log p - a)/s$, which has probability $\sigma(z)$ with
$z = (a - \log p)/s$ and $\sigma$ the logistic function: a logit in the log price, the model Agora fits. Expected
revenue is $p\,\sigma(z)$, and since $dz/dp = -1/(s p)$, its derivative is $\sigma - p\,\sigma(1 - \sigma)/(s p) =
\sigma[1 - (1 - \sigma)/s]$, zero where $\sigma = 1 - s$ (for $s < 1$). So the best price is
$p^* = e^{a}\,(s/(1 - s))^{s}$, different for every buyer, but each buys with the same probability $1 - s$, whatever
their features. With $s = 0.35$, that is 65%, and Agora's buyers bought 65.3% of the time at their personal prices
(the prices lie on a grid, and the model is estimated). With a single price, high-$a$ buyers buy more often than
low-$a$ ones; personal prices equalize the chance of a sale and move the price instead.

## Where it comes back

| Idea | Parts |
|---|---|
| Games, and competition among a few sellers | 11 *Games*, 12 *Competition among the Few* |
| Screening and hidden types | 13 *Lemons and Signals*, 14 *Incentives* |
| Regulation and the incentive-rent trade-off | 14 *Incentives* |
| Auctions as discrimination | 16 *Auctions* |
| Monopsony and minimum wages | 38 *Work and Wages* |
| Pass-through and tax incidence | 2 *The Scissors*, 41 *Taxes* |
| Measuring market power | 43 *Measuring Market Power*, 44 *Dynamics, Platforms and Antitrust* |
| Revenue management and pricing in practice | 60 *The Price*, 61 *Economics at the Platforms* |

## Sources

- J. Dupuit, "De la mesure de l'utilité des travaux publics", *Annales des ponts et chaussées* (1844); "De
  l'influence des péages sur l'utilité des voies de communication", *Annales des ponts et chaussées* (1849).
- A. C. Pigou, *The Economics of Welfare* (1920); J. Robinson, *The Economics of Imperfect Competition* (1933); A. P.
  Lerner, "The Concept of Monopoly and the Measurement of Monopoly Power", *Review of Economic Studies* 1(3) (1934).
- A. C. Harberger, "Monopoly and Resource Allocation", *American Economic Review* 44(2) (1954); G. Tullock, "The
  Welfare Costs of Tariffs, Monopolies, and Theft", *Western Economic Journal* 5(3) (1967); R. A. Posner, "The Social
  Costs of Monopoly and Regulation", *Journal of Political Economy* 83(4) (1975).
- R. Schmalensee, "Output and Welfare Implications of Monopolistic Third-Degree Price Discrimination", *American
  Economic Review* 71(1) (1981); H. R. Varian, "Price Discrimination and Social Welfare", *American Economic Review*
  75(4) (1985).
- M. Mussa and S. Rosen, "Monopoly and Product Quality", *Journal of Economic Theory* 18(2) (1978); E. Maskin and J.
  Riley, "Monopoly with Incomplete Information", *RAND Journal of Economics* 15(2) (1984); R. J. Deneckere and R. P.
  McAfee, "Damaged Goods", *Journal of Economics and Management Strategy* 5(2) (1996).
- W. Y. Oi, "A Disneyland Dilemma: Two-Part Tariffs for a Mickey Mouse Monopoly", *Quarterly Journal of Economics*
  85(1) (1971); G. J. Stigler, "United States v. Loew's Inc.: A Note on Block-Booking", *Supreme Court Review* (1963);
  W. J. Adams and J. L. Yellen, "Commodity Bundling and the Burden of Monopoly", *Quarterly Journal of Economics* 90(3)
  (1976); R. P. McAfee, J. McMillan and M. D. Whinston, "Multiproduct Monopoly, Commodity Bundling, and Correlation of
  Values", *Quarterly Journal of Economics* 104(2) (1989).
- R. H. Coase, "Durability and Monopoly", *Journal of Law and Economics* 15(1) (1972); N. L. Stokey, "Rational
  Expectations and Durable Goods Pricing", *Bell Journal of Economics* 12(1) (1981); J. I. Bulow, "Durable-Goods
  Monopolists", *Journal of Political Economy* 90(2) (1982), and "An Economic Theory of Planned Obsolescence",
  *Quarterly Journal of Economics* 101(4) (1986); F. Gul, H. Sonnenschein and R. Wilson, "Foundations of Dynamic
  Monopoly and the Coase Conjecture", *Journal of Economic Theory* 39(1) (1986).
- F. P. Ramsey, "A Contribution to the Theory of Taxation", *Economic Journal* 37(145) (1927); M. Boiteux, "Sur la
  gestion des monopoles publics astreints à l'équilibre budgétaire", *Econometrica* 24(1) (1956); H. Averch and L. L.
  Johnson, "Behavior of the Firm Under Regulatory Constraint", *American Economic Review* 52(5) (1962); S. C.
  Littlechild, *Regulation of British Telecommunications' Profitability* (Department of Industry, 1983).
- K. Littlewood, "Forecasting and Control of Passenger Bookings", *AGIFORS Symposium Proceedings* 12 (1972),
  reprinted in *Journal of Revenue and Pricing Management* 4(2) (2005); K. Talluri and G. van Ryzin, *The Theory and
  Practice of Revenue Management* (2004).
- E. Nakamura and D. Zerom, "Accounting for Incomplete Pass-Through", *Review of Economic Studies* 77(3) (2010)
  1192-1230 (read in NBER Working Paper 15255, 2009); E. G. Weyl and M. Fabinger, "Pass-Through as an Economic Tool",
  *Journal of Political Economy* 121(3) (2013).
- R. E. Hall, "The Relation between Price and Marginal Cost in U.S. Industry", *Journal of Political Economy* 96(5)
  (1988); J. De Loecker and F. Warzynski, "Markups and Firm-Level Export Status", *American Economic Review* 102(6)
  (2012); J. De Loecker, J. Eeckhout and G. Unger, "The Rise of Market Power and the Macroeconomic Implications",
  *Quarterly Journal of Economics* 135(2) (2020) 561-644; J. Traina, "Is Aggregate Market Power Increasing?
  Production Trends Using Financial Statements", Stigler Center Working Paper 272 (2018).
- J.-P. Dubé and S. Misra, "Personalized Pricing and Consumer Welfare", *Journal of Political Economy* 131(1)
  (2023) 131-189; E. Calvano, G. Calzolari, V. Denicolò and S. Pastorello, "Artificial Intelligence, Algorithmic
  Pricing, and Collusion", *American Economic Review* 110(10) (2020); S. Assad, R. Clark, D. Ershov and L. Xu,
  "Algorithmic Pricing and Competition: Empirical Evidence from the German Retail Gasoline Market", *Journal of
  Political Economy* 132(3) (2024) 723-771.
- U.S. Bureau of Labor Statistics, average price of coffee, 100%, ground roast, all sizes, per pound, U.S. city
  average (APU0000717311), via FRED; the World Bank, Commodity Price Data (the Pink Sheet), arabica coffee.
- Textbooks: J. Tirole, *The Theory of Industrial Organization* (1988), chs. 1-4; P. Belleflamme and M. Peitz,
  *Industrial Organization: Markets and Strategies* (2nd ed., 2015); H. R. Varian, *Intermediate Microeconomics*, the
  chapters on monopoly, monopoly behaviour and factor markets; A. Mas-Colell, M. D. Whinston and J. R. Green,
  *Microeconomic Theory* (1995), ch. 12.
