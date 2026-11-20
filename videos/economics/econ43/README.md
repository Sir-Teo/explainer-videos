# Economics, Built: Part 43, Measuring Market Power

Part 43 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first of Act IX, *The Fields*, which takes the fields of economics one by one,
beginning with industrial organization. It asks how you can tell whether a market is competitive when you cannot see
anyone's costs. Its answer: not from concentration alone. Estimate how buyers substitute between products, from
prices, shares and characteristics, with instruments that move prices but not unseen quality; the markups, and the
conduct that fits them, follow. Or read markups from production data with a carefully estimated production function,
or from how many firms towns of different sizes can support.

It opens on the cereal aisle, drawn as three shelves of ninety boxes coloured by maker: around 1980 Kellogg sold about
42% of America's cereal, General Mills about 20% and General Foods (Post) about 16%; the Federal Trade Commission's
"shared monopoly" case of 1972 was dismissed by an administrative law judge in 1981, collusion unproved. In 2001 Aviv
Nevo found the margins explained by differentiation and portfolios of brands, using the method of a 1995 paper on
cars. From there it covers:

- structure, conduct, performance: Bain's 42 industries of 1936-40 (profit rates of about 11.8% where the eight
  largest firms made at least 70% of output, 7.5% elsewhere); Demsetz's objection, computed: 300 Island industries
  that all play Cournot, differing only in how unequal their firms' costs are, with a correlation of 0.78 between the
  Herfindahl index and the margin, and 0.93 within industries between a firm's share and its margin; the identity
  behind it, a Cournot industry's margin equals HHI / (10,000 epsilon);
- a game: two mergers among five cereals in three nests (nested logit, sigma 0.6): the bran twins, with 26% of sales
  and a rise of 344 in the Herfindahl index, raise their prices 30.3% and cut shoppers' surplus 8.3%; the two
  largest brands, with 59% and a rise of 1,736, raise theirs 3.0% (3.5% of surplus); diversion ratios of 47% and 8%;
- conduct as a parameter: with parallel shifts of demand a competitive industry with rising marginal cost and a
  monopoly with flat cost give identical prices and quantities; a rotation separates them (6.00 against 5.33),
  Bresnahan and Lau's identification;
- demand for differentiated products: 144 cross-price elasticities for 12 products, 40,000 for 200; Lancaster's
  characteristics space, drawn with the 131 cars of 1990 from Berry, Levinsohn and Pakes's data; utility with
  unseen quality xi and why price is endogenous;
- the logit, Berry's inversion and its elasticities; the red bus (a half becomes a third for each option under logit,
  against 49% and 25% each under a tight nest); diversion from Bran Buds: 5% to its twin under plain logit, 47% under
  the game's nested logit; the nested logit and its limits;
- random coefficients derived (Berry, Levinsohn and Pakes): buyers' price sensitivity varying around 0.6 with spread
  0.15 on the Island; shares as integrals, simulated; Berry's contraction, which shrinks the error by a constant
  factor each step until it is below 10^-14; the estimator's loop; instruments from rivals' and the firm's own
  characteristics, cost shifters and Gandhi and Houde's crowding measures;
- the estimator on 40 simulated Islands (40 years of 24 models from six firms): price sensitivity 0.22 by OLS logit,
  0.42 by IV logit, 0.60 by BLP (standard deviation 0.14 across Islands), against 0.6; median own-price elasticities
  -1.87, -3.56, -3.80 against -3.87; then plain logit on the real 2,217 cars of 1971-1990: 1,491 models with
  inelastic demand by OLS (alpha 0.0895), 726 by IV (alpha 0.138, first-stage F 56), and an almost constant dollar
  markup of about $7,300 (1983 dollars) on every car;
- an intermission: corporate profits after tax over GDP, 1947-2026 (4.1% in 1947, about 6% in 1980-2000, about 10%
  since 2010, 11.9% in 2026), as a tune;
- from elasticities to markups, and Nevo's test on the Island's aisle (twelve brands, four firms, random-coefficient
  logit): the margins implied by today's prices are 38% if every brand had its own owner, 42% with the real owners
  and 92% for a cartel, against 42% earned; Nevo's finding for American cereal;
- merger simulation: the two smaller firms (43% of sales, Herfindahl +899 to 3,463) raise their prices 5.8% and
  rivals follow by 0.4%; Werden's compensating cost reductions, about 12%; new goods: an identical copy of a cereal
  is worth $0.092 to every shopper under plain logit, $0.035 with the game's nests and nothing as the nest tightens;
  Petrin's minivan;
- production functions: on 1,500 Island plants, labour's and capital's elasticities by OLS (1.00, 0.14), within a
  plant (0.89, 0.16) and by Ackerberg, Caves and Frazer (0.60, 0.30), against (0.6, 0.3); Olley and Pakes and
  Levinsohn and Petrin; Syverson's 90/10 productivity ratio of 1.92 as a Fact, with 1.87 on the Island;
- markups from production data: De Loecker and Warzynski's ratio recovers the Island's planted median of 1.30 with
  ACF's elasticity and gives 2.17 with OLS's; De Loecker, Eeckhout and Unger's rise from 1.21 to 1.61, 1980-2016, and
  its critics (Traina, Bond et al., Basu);
- entry: Bresnahan and Reiss's thresholds, estimated by an ordered probit from 400 Island towns: per-firm threshold
  ratios 1.77, 1.22, 0.99 and 1.02 against the planted 1.67, 1.25, 1.04 and 1.02; Cournot with straight-line demand
  would give 1.1 to 1.2, a cartel one; Axtell's Zipf law for firm sizes as a Fact;
- two dials (markups, updated; the own-price elasticity of one product, new); merger review in practice (the 2023
  Guidelines' 1,800 and 100, upward pricing pressure of +0.177 for the bran twins and -0.060 for the two largest with a
  10% cost credit, who does the work); *Called it?* on the 2008 MillerCoors clearance (partly right); a frontier
  chapter on micro data, learned characteristics, instruments and identification.

## Build it

```bash
python -m videos.economics.econ43.compute              # every number (about two minutes), into .cache/econ43/
python tools/qa_scene.py econ43 Cars                   # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ43 -q l   # the whole part, silent preview
python tools/build.py econ43                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 43                     # the lab
```

The data are in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): Berry, Levinsohn and Pakes's 2,217 cars (from the R
package BLPestimatoR, read without evaluating anything); from FRED, corporate profits after tax with and without the
inventory valuation and capital consumption adjustments, and GDP; and tables from the FTC's cereal case, Nevo, Bain
and Demsetz, Bresnahan and Lau, Lancaster, McFadden and Berry, Berry, Levinsohn and Pakes, Petrin, Olley and Pakes,
Levinsohn and Petrin, Ackerberg, Caves and Frazer, Syverson, De Loecker and Warzynski, De Loecker, Eeckhout and Unger,
Traina, Basu, Bond et al., Bresnahan and Reiss, the Merger Guidelines, the MillerCoors studies and Axtell.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The cereal aisle | The shelves and the FTC's case; the puzzle with no costs in sight; the question; objectives |
| 1 | Structure, conduct, performance | Bain; Demsetz on the Island; within industries; HHI over the elasticity |
| 2 | Play it: two mergers among five brands | The game; the answer; diversion |
| 3 | Conduct as a parameter | Parallel shifts; a rotation; the conduct parameter |
| 4 | Demand for differentiated products | 40,000 elasticities; characteristics space; utility and endogeneity |
| 5 | The logit, the red bus and the nest | Shares, inversion, elasticities; IIA; diversion; nested logit |
| 6 | Random coefficients, derived | Tastes that differ; shares as integrals; the contraction; the loop; instruments |
| 7 | BLP on the Island, then on real cars | 40 Islands; elasticities against price; real cars; constant dollar markups |
| — | Intermission | Corporate profits over GDP since 1947, as a tune |
| 8 | From elasticities to markups: Nevo's cereals | Multi-product markups; the conduct test on the aisle; the split; caveats |
| 9 | Merger simulation and new goods | The recipe; the aisle's merger; offsetting savings; a clone's value |
| 10 | The supply side: production functions | Simultaneity; the proxy estimators; OLS, within, ACF; the dispersion Fact |
| 11 | Markups from production data | The ratio derived; the Island; the rise; the critics |
| 12 | How many dentists does a town need? | Thresholds; the Island's towns; the ordered probit; Zipf's Fact |
| 13 | The Dials | Markups; one product's own-price elasticity |
| 14 | In practice: merger review | The screens; upward pricing pressure; *Called it?* (partly right); who does this |
| 15 | Frontier | Micro data, learned characteristics, instruments, identification; the chain |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 44, *Dynamics, Platforms and Antitrust* |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's industrial organization module
(`explainer.economics.agora.io`), with the Island's Part 43 truths, or from the Data Room; the narration states the
cached numbers.

- **Structure and performance.** 300 industries with demand P = 10 - Q and five Cournot firms whose costs are 4 exp(s
  z), z standard normal and s uniform on [0, 0.6]; firms that would produce nothing drop out.
- **The game.** Five brands with qualities 0.8, 0, 1.0, -0.5, -0.5 and costs 1.5, 1.2, 1.6, 1.0, 1.0 in nests sweet
  (1, 2), nutty (3) and bran (4, 5); nested logit with price coefficient 1 and sigma 0.6; Bertrand-Nash prices by
  damped iteration on the first-order conditions; a merger recovers costs from the pre-merger prices and solves
  again with the new owners; shoppers' surplus is ln(1 + sum of D_g^(1 - sigma)).
- **Conduct.** Demand Q = 10 + y - (1 + z) P; story A is competitive with marginal cost 2 + Q, story B a monopoly with
  marginal cost 2.
- **The Island's cars.** 40 years of 24 models (six firms of four) with size and power uniform on [0.5, 2], unseen
  quality xi normal with sd 0.8, utility -4 + 1.5 size + power + xi - alpha_i p with alpha_i = 0.6 - 0.15 nu_i (300
  simulated buyers), marginal cost exp(1.2 + 0.3 size + 0.2 power + 0.5 w + omega) with omega = 0.15 e + 0.3 xi;
  Bertrand-Nash prices by Morrow and Skerlos's zeta iteration. Instruments: the cost shifter w, Gandhi and Houde's
  sums of squared differences in characteristics, their squares and w squared. BLP minimizes the GMM objective over
  sigma by a bounded scalar search, inverting shares by Berry's contraction for each trial. The Monte Carlo repeats
  this on 40 Islands (seeds 0 to 39).
- **BLP's data.** Plain logit on (horsepower over weight, air conditioning, miles per gallon, space, price), by OLS and
  by two-stage least squares with BLP's instruments (sums of the characteristics over the firm's other models and
  over rivals' models in the same year); markups for multi-product firms from the logit derivatives.
- **The aisle.** Twelve brands (owners 4, 4, 2, 2), mean utilities normal(1, 0.5), costs lognormal around 1.2 (sd
  0.15), price sensitivity 1.6 - 0.4 nu over 500 simulated shoppers; implied margins from the observed prices under
  each ownership; Werden's reductions from the costs that make today's prices optimal after the merger.
- **Plants.** 1,500 plants for 10 years: y = 0.6 l + 0.3 k + omega + eps, omega an AR(1) with persistence 0.8 and
  innovations 0.15, labour chosen with omega in view plus a shock of sd 0.3, materials omega + 0.5 k + 0.5 l as the
  proxy; ACF by a grid search then bounded least squares on the moments in k_t, l_(t-1) and k_(t-1).
- **Markups from production.** 2,000 plants with markups lognormal around 1.3 (sd 0.15) whose labour share of revenue
  is 0.6 / mu.
- **Towns.** 400 towns with populations log-uniform on 500 to 40,000; the market's profit per resident is 1, 0.6, 0.48,
  0.46 and 0.45 with one to five firms; fixed cost 1 (thousand residents' worth) times a lognormal shock with sd
  0.25; the ordered probit is fitted by BFGS on increasing cut-offs.

## Problems and solutions

**1.** *Cournot: three firms with shares 50%, 30% and 20%; market demand has elasticity 2. Find each firm's margin,
the Herfindahl index and the industry's margin.*

*Solution.* Each margin is the share over the elasticity: 25%, 15% and 10%. The Herfindahl index is 2,500 + 900 +
400 = 3,800, and the share-weighted margin is 0.38 / 2 = 19% (check: 0.5 x 0.25 + 0.3 x 0.15 + 0.2 x 0.10 = 0.19).

**2.** *Logit: two products with shares 0.2 and 0.3 (outside good 0.5), alpha = 0.5, p1 = 4. Find product 1's
own-price elasticity and product 2's elasticity with respect to p1.*

*Solution.* Own: -alpha p1 (1 - s1) = -0.5 x 4 x 0.8 = -1.6. Cross: alpha p1 s1 = 0.5 x 4 x 0.2 = 0.4, the same for
every other product, whatever it is like.

**3.** *The red bus: a car and a blue bus each take half. A red bus identical to the blue appears. Find the shares
under plain logit, and under nested logit with the buses in one nest as sigma tends to one.*

*Solution.* Plain logit gives each of three equal options a third. With the buses nested and sigma tending to one,
the nest behaves as one option: the car keeps a half and each bus takes a quarter.

**4.** *Upward pricing pressure: diversion from product 1 to product 2 is 0.4, product 2's margin is $3, product 1's
cost is $10. With a 5% cost credit, is there upward pressure?*

*Solution.* UPP = 0.4 x 3 - 0.05 x 10 = 1.2 - 0.5 = 0.7 > 0: yes. Savings would have to exceed 12% of cost to
offset it.

**5.** *Berry's inversion: with plain logit, a product's share is 0.2 and the outside share 0.5. Find its mean
utility, and show that, started there, the contraction does not move when sigma = 0.*

*Solution.* delta = ln 0.2 - ln 0.5 = -0.916. With sigma = 0 the predicted share at that delta is
e^delta / (1 + sum of e^delta) = 0.2 exactly, because the denominator is 1 / 0.5; so ln s - ln s_hat = 0 and the
update leaves delta where it is.

**6.** *De Loecker and Warzynski: materials' output elasticity is 0.6 and materials are 40% of revenue. Find the
markup. What if the elasticity were mis-estimated as 0.7?*

*Solution.* mu = 0.6 / 0.4 = 1.5. With 0.7 it would be 1.75: every markup inflated by the same 17%, which is why the
level of markups hinges on the production function.

**7.** *Entry: a town needs 1,000 people for one dentist and 3,333 for two. Find the ratio of per-firm thresholds, and
what it says about the duopoly's margin per resident.*

*Solution.* Per firm, 1,000 and 3,333 / 2 = 1,667: a ratio of 1.67. Since S_N = N F / v_N, the ratio is v_1 / v_2,
so the market's profit per resident with two firms is 1 / 1.67 = 60% of the monopolist's: the second firm brings
real competition.

**8.** *Derive the multi-product first-order conditions and show that p - c = -(Omega o ds/dp')^-1 s; for
single-product logit firms, show p_j - c_j = 1/(alpha (1 - s_j)).*

*Solution.* Firm f maximizes the sum over its products k of (p_k - c_k) M s_k(p). Differentiating with respect to p_j,
for j owned by f: s_j + sum over k owned by f of (p_k - c_k) ds_k/dp_j = 0. Stacking all products with J[j, k] =
ds_k/dp_j and Omega[j, k] = 1 when j and k share an owner gives s + (Omega o J)(p - c) = 0, so p - c = -(Omega o
J)^-1 s. For a single-product logit firm, Omega o J is diagonal with ds_j/dp_j = -alpha s_j (1 - s_j), so p_j - c_j =
s_j / (alpha s_j (1 - s_j)) = 1/(alpha (1 - s_j)): almost the same dollar markup for every small product, as the
film shows on the real cars.

## Lab and interactive

- `python -m videos.economics.labs 43`: concentration and margins under Cournot; the two mergers; OLS, IV logit and
  BLP on a simulated car market; plain logit on Berry, Levinsohn and Pakes's cars; Nevo's test; production functions
  by OLS and ACF and the markups they imply; entry thresholds.
- The interactive (course site): simulate a merger. The reader picks any two of the game's five cereals, the nesting
  parameter and a cost saving, and sees every brand's price change, the merging brands' price rise against the nesting
  parameter beside the game's two mergers, the Herfindahl index, the diversion ratio, upward pricing pressure and
  shoppers' surplus.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[43]`; the two dials are in
`explainer/economics/dials.py`; the MillerCoors clearance is a *Called it?* entry (`explainer/economics/calls.py`).
FRED's series were retrieved on 2026-11-20; BLP's data are BLPestimatoR 0.3.4's copy, checked by SHA-256. The FTC's
case is from the Commission's decision volume and contemporary reports; Bain's profit rates are as later summaries
report his table; Nevo, Berry, Levinsohn and Pakes, Petrin, Olley and Pakes, Levinsohn and Petrin, Ackerberg, Caves
and Frazer, De Loecker and Warzynski, De Loecker, Eeckhout and Unger, Traina, Basu, Bond et al., Bresnahan and Reiss
and Axtell from their abstracts; Syverson's 1.92 from his survey; the Merger Guidelines' thresholds from Guideline 1
and law-firm summaries; the MillerCoors facts from the Department of Justice's statement and the two papers' abstracts.
Where a published number could not be checked (BLP's own elasticities, Nevo's margins), the film states the finding in
words and computes the method on the Island instead.
