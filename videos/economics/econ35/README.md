# Economics, Built: Part 35, Trade I: Comparative Advantage

Part 35 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second of Act VII, *The World Economy*. It asks why countries trade, and who wins
and loses when they do. Its answer: relative costs differ, through technology and through what countries have, so
trade lets each buy what is dear to make at home, and the country as a whole gains. But not everyone in it: the
owners of the factors that imports use intensively, and of those stuck in industries that compete with imports, lose.
Because they are few and concentrated, they often win the politics. The winners could compensate them, and rarely do.

It opens on Stanislaw Ulam's challenge to Paul Samuelson, to name one proposition in the social sciences that is both
true and not trivial, and Samuelson's answer, as he told it in 1969: Ricardo's comparative advantage. From there it
covers:

- trade, exports plus imports, in eighteen rich economies since 1870: 33% of GDP in the median economy in 1870, 42% in
  1913, 25% in 1932 and 60% in 2019;
- a game: the Island needs 3 hours for a fish and 6 for a bolt of cloth, the Archipelago 1 and 4; who should make
  what? The Island weaves, and at 3 fish a bolt both gain (22% and 15%); its wage is half the Archipelago's;
- Ricardo's four numbers (England 100 and 120, Portugal 90 and 80): the world supply staircase, a price of one cloth
  for a wine, gains for both, and Portugal's wage 1.25 times England's, inside the band from 10/9 to 3/2;
- the chain of comparative advantage and the Dornbusch-Fischer-Samuelson continuum: when the Archipelago grows by
  half, the Island's relative wage rises from 0.78 to 0.90 while it gives up industries; shipping costs leave 11% of
  goods untraded;
- Japan's opening in 1859, with Bernhofen and Brown's tables: silk, silkworm eggs and tea were four fifths of its
  exports; its trade valued at the prices of 1851-53 is negative in all eight years from 1868 to 1875, as the theory
  requires; the gains were at most 8 to 9% of GDP, and America's embargo of 1807-09 cost about 5%;
- Heckscher and Ohlin's factor proportions in the Lerner diagram, on the Island (labour-abundant) and the
  Archipelago (capital-abundant): each exports the good that uses its abundant factor, and factor prices equalize;
  Rybczynski's magnification (10% more capital, 13% more machines and 34% less cloth);
- Stolper and Samuelson: a 10% rise in the price of cloth raises the wage 18% and lowers the rent 7%; opening to
  trade, each country's scarce factor loses;
- Leontief's paradox ($13,991 of capital per worker-year in exports against $18,184 in import replacements, 1947),
  four answers including Leamer's, and Trefler's missing trade, recomputed from his data: the measured factor content
  of trade has the predicted sign 50% of the time and about a thirty-eighth of the predicted variance;
- an intermission without narration: America's customs duties as a share of its goods imports since 1929, as a tune;
- specific factors: a 10% rise in the price of food raises land rents 15%, the wage 5% and lowers the return to
  capital 5%; Olson's logic of concentrated losers and diffuse winners;
- a tariff's triangles on the Island's cloth market, a quota and its rent, and the large country's optimal tariff
  (20%, the inverse of the foreign supply elasticity);
- protection for sale: the Corn Laws, Smoot-Hawley (40% to 59% on dutiable imports, much of it from deflation) and
  the collapse of trade; Grossman and Helpman's formula on ten industries, and Goldberg and Maggi's estimate;
- a tariff war as a prisoner's dilemma, with best responses; the GATT, reciprocity, most-favoured-nation treatment and
  the WTO; America's average tariff on goods, 2.6% in 2024 and 8.0% in 2025;
- compensation: when food falls 20%, landowners lose a fifth and factory owners gain a quarter, and the winners could
  pay the losers and still be ahead; the is/ought step; trade adjustment assistance and Hyman's estimate;
- a new dial, the gains from trade; the Fact that rich countries mostly trade similar goods (America's two-way trade
  in capital goods, 0.77 on the Grubel-Lloyd index); *Called it?* on Heckscher and Ohlin's prediction for America
  (partly right); a frontier chapter on Costinot and Donaldson's test and Eaton and Kortum's model.

## Build it

```bash
python -m videos.economics.econ35.compute              # every number (a few seconds), into .cache/econ35/
python tools/qa_scene.py econ35 Tariff                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ35 -q l   # the whole part, silent preview
python tools/build.py econ35                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 35                     # the lab
```

The data are in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): the Jordà-Schularick-Taylor Macrohistory Database
(release 6, CC BY-NC-SA 4.0) for exports, imports and GDP since 1870; from FRED, the BEA's customs duties, imports of
goods, imports and GDP, and exports and imports by end use; Trefler's 1983 factor-content data (NBER); and the tables
transcribed in `tables.py` from Ricardo, Bernhofen and Brown, Irwin, Leontief, Trefler, Goldberg and Maggi,
Arkolakis, Costinot and Rodríguez-Clare, Costinot and Donaldson, and the record of trade adjustment assistance.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | True and not trivial | Ulam's challenge and Samuelson's answer; trade since 1870; the question; objectives |
| 1 | Play it: four numbers | The Island and the Archipelago; opportunity costs; frontiers and the gains; wages |
| 2 | Ricardo's four numbers | England and Portugal; the world supply staircase; the gains; the wage band |
| 3 | Many goods | The chain; the continuum; growth abroad; shipping costs and non-traded goods |
| 4 | A test: Japan opens | The treaty ports; the composition of trade; the inner product; the size of the gains |
| 5 | Factor proportions | Heckscher and Ohlin; the Lerner diagram; trade and factor price equalization; four theorems |
| 6 | Stolper and Samuelson | Factor prices against goods prices; the magnification effect; who gains from opening |
| 7 | Leontief's paradox and the missing trade | Leontief's table; four answers; Trefler's test recomputed |
| — | Intermission | America's average tariff on goods since 1929, as a tune |
| 8 | Specific factors | The labour diagram; who loses first; concentrated losers and diffuse winners |
| 9 | Tariffs and quotas | The triangles; a quota's rent; the large country's optimal tariff |
| 10 | Protection for sale | The Corn Laws and Smoot-Hawley; the collapse of trade; Grossman and Helpman |
| 11 | Trade agreements | The tariff war as a dilemma; best responses; the GATT and the WTO |
| 12 | Compensation | Winners and losers when the Island opens; is and ought; trade adjustment assistance |
| 13 | The Dials | The gains-from-trade formula; the new dial; the Fact of two-way trade |
| 14 | In practice | Trade ministries, customs, trade remedies; *Called it?* on Heckscher and Ohlin |
| 15 | Frontier | Costinot and Donaldson; Eaton and Kortum; open questions |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 36, *Trade II: Scale, Firms and Gravity* |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's trade (`explainer.economics.agora.trade`) with the
Island's Part 35 truths, or from the Data Room; the narration states the cached numbers.

- **Openness.** (exports + imports) / GDP from the Macrohistory Database, each in national currency; the median of
  the economies with data in each year (at least ten), and the United States.
- **Ricardo.** Two goods, labour only, Cobb-Douglas demand with half of spending on each good. The world relative
  supply is a step function; with full specialization the price is (1 − β)/β times the ratio of world outputs,
  clamped to the two autarky prices (and a country whose autarky price it is makes both goods).
- **The continuum.** 200 goods with the Island's productivity edge A(z) = 0.4 exp(1.5(1 − 2z)), equal spending
  shares, the Archipelago's labour twice the Island's; the relative wage balances trade. With iceberg costs (85% of a
  cargo arrives) the Island exports z with ω ≤ 0.85 A(z), the Archipelago z with ω ≥ A(z)/0.85.
- **Japan.** Bernhofen and Brown's table 2, rows summed; their table 1 for the composition.
- **Heckscher-Ohlin.** Cobb-Douglas technologies with labour shares 0.7 (cloth) and 0.3 (machines); zero profits give
  log-linear equations for the wage and the rent; outputs from full employment; the world price by root-finding on
  world relative demand. The Island has 120 workers and 50 units of capital, the Archipelago 80 and 130.
- **Trefler.** For each factor f and country c, the predicted factor content is V_fc − s_c V_fw, with s_c = (Y − B)/
  (Y_w − B_w); both measured and predicted are divided by σ_f √s_c, as in the paper, and pooled.
- **Specific factors.** 100 workers; capital 100 in manufacturing and land 100 in farming; Cobb-Douglas with labour
  share 0.5 in both; the wage equalizes the values of the marginal products.
- **Tariffs.** The Island's cloth market D = 100 − 10p, S = 10p − 20 at a world price of 4; as a large country, the
  Archipelago's export supply X* = 40p* − 120.
- **Protection for sale.** Ten industries with output/imports drawn between 0.5 and 6 and import elasticities between
  1 and 3 (seed 35), four organized, 5% of the population organized, weights on welfare of 50 and 5.
- **The tariff war.** Two mirror-image economies, each importing one good: demand 10 − p in both, supply 0.5p at the
  importer and 2p at the exporter; best responses by bounded optimization, the Nash tariff by iteration.
- **The dial.** 1 − λ^{1/ε} with λ = 1 − (imports of goods and services)/GDP for 2025 and ε = 5 and 10.
- **The Fact.** The Grubel-Lloyd index 1 − |X − M|/(X + M) for three end-use categories (NIPA table 4.2.5).
- **The intermission.** Customs duties (NIPA) over imports of goods, annual, 1929-2025.

## Problems and solutions

**1.** *Ricardo: Home needs 1 hour for a fish and 2 for a bolt of cloth; Foreign 3 and 4. Who has the comparative
advantage in cloth, and between which prices can they trade?*

*Solution.* A bolt costs Home 2 fish (2 hours could land 2 fish) and Foreign 4/3 of a fish. Foreign has the
comparative advantage in cloth though it is worse at both; Home in fish. Trade can happen at any price between 4/3
and 2 fish a bolt; outside that range one country would want to make both goods.

**2.** *The same, with 1,200 hours each and half of spending on each good: find the world price, and show that Home
gains nothing.*

*Solution.* Fully specialized, Home lands 1,200 fish and Foreign weaves 300 bolts; with equal spending shares the
price would be 1,200/300 = 4 fish a bolt, above Home's own cost of 2. So Home also weaves, and the price is Home's
autarky price, 2: Home's options are unchanged and it gains nothing, while Foreign, trading at a price far from its
own, takes all the gain (22.5% here). A large country trading with a small one may gain little.

**3.** *Wages: with Ricardo's numbers, show that Portugal's wage relative to England's lies between 10/9 and 3/2.*

*Solution.* With wages w_P and w_E, cloth costs 100 w_E in England and 90 w_P in Portugal; England makes cloth only
if 100 w_E ≤ 90 w_P, so w_P/w_E ≥ 10/9. Wine costs 120 w_E and 80 w_P; Portugal makes wine only if 80 w_P ≤
120 w_E, so w_P/w_E ≤ 3/2. Demand picks the point in between: 1.25 in this part's world.

**4.** *Continuum: with equal spending shares, show that ω = z̄/(1 − z̄) · L*/L, and that a larger L* raises ω and
lowers z̄.*

*Solution.* Home makes goods [0, z̄], so the world spends a share z̄ of its income on them: wL = z̄(wL + w*L*).
Rearranged, w/w* = z̄/(1 − z̄) · L*/L, the rising B curve. A larger L* shifts B up; since A(z) falls, they now cross at
a higher ω and a lower z̄: Home's wage rises and it makes fewer goods.

**5.** *Stolper-Samuelson: with labour shares 0.7 and 0.3, show that a 10% rise in cloth's price raises the wage
17.5% and lowers the rent 7.5%, to first order.*

*Solution.* Zero profits in proportional changes: p̂₁ = 0.7ŵ + 0.3r̂ and p̂₂ = 0.3ŵ + 0.7r̂. With p̂₂ = 0,
r̂ = −(3/7)ŵ, so p̂₁ = (0.7 − 0.9/7)ŵ = (4/7)ŵ and ŵ = 1.75 p̂₁ = 17.5%, r̂ = −0.75 p̂₁ = −7.5%. (Exactly, in logs,
the wage rises 18.2% and the rent falls 6.9%, as the chapter shows.)

**6.** *Tariff: D = 100 − 10p, S = 10p − 20, world price 4, tariff 1. Find the consumers' loss, the producers' gain,
the revenue and the deadweight loss.*

*Solution.* At 4: demand 60, supply 20, imports 40. At 5: demand 50, supply 30, imports 20. Consumers lose the area
between the prices under demand, (60 + 50)/2 = 55; producers gain (20 + 30)/2 = 25; revenue is 1 × 20 = 20; the
deadweight loss is 55 − 25 − 20 = 10, two triangles of 5.

**7.** *Optimal tariff: import demand M = 120 − 20p, foreign supply X\* = 40p\* − 120. Find the best tariff, and check
that t/p\* = 1/ε\*.*

*Solution.* With p = p* + t, clearing gives 120 − 20(p* + t) = 40p* − 120, so p* = 4 − t/3 and imports
M = 40 − 40t/3. Welfare relative to free trade, measuring the home market's surplus loss and the revenue, is
maximized at t = 0.75: then p* = 3.75, imports 30, and the foreign supply elasticity is ε* = 40 × 3.75/30 = 5, so
t/p* = 0.2 = 1/ε*.

**8.** *$\bigstar$ Show that identical technologies, equal factor prices and identical homothetic tastes imply
F_c = V_c − s_c V_w.*

*Solution.* With identical technologies and equal factor prices, every country uses the same matrix A of factor
requirements per unit of output. Full employment gives A Q_c = V_c. Identical homothetic tastes at common prices make
every country's consumption a fraction of world consumption, C_c = s_c C_w, where s_c is its share of world spending,
and the world consumes what it produces, C_w = Q_w. The factor content of net exports is then
F_c = A(Q_c − C_c) = V_c − s_c A Q_w = V_c − s_c V_w. Trefler's test compares both sides.

## Lab and interactive

- `python -m videos.economics.labs 35`: Ricardo's world and the Island's, the continuum with growth and shipping
  costs, Bernhofen and Brown's test, the Heckscher-Ohlin world with Stolper-Samuelson and Rybczynski, Trefler's
  statistics from his data, specific factors, tariffs and the optimal tariff, protection for sale, the tariff war, and
  the gains-from-trade formula.
- The interactive (course site): four numbers. The reader sets the hours each island needs for each good and the
  size of each, and sees who makes what, the world price, and each island's gain.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[35]`; the gains from trade are a dial
(`explainer/economics/dials.py`); Heckscher and Ohlin's prediction for America is a *Called it?* entry
(`explainer/economics/calls.py`). The Macrohistory Database (release 6) and FRED's series were retrieved on
2026-11-20, and Trefler's data file from NBER on the same day. Bernhofen and Brown's tables were transcribed from the
published article; Samuelson's words are given as several sources reproduce them, since his 1969 lecture itself was
not read; Japan's opening (Perry's arrival in 1853, the treaty ports in July 1859) is as the article describes it; the
*Ideal X*'s voyage of 26 April 1956 with fifty-eight trailers was checked against several accounts, which agree.
