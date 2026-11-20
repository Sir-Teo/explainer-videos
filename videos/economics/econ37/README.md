# Economics, Built: Part 37, Cities and Regions

Part 37 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth and last of Act VII, *The World Economy*. It asks why economic activity is
piled up in a few places, and what that does to the people in them. Its answer: because crowding together makes
people more productive, through sharing, matching and learning, and because small advantages compound, activity piles
up; people follow until rents and congestion offset the gains, so in equilibrium places differ more in their prices
than in the welfare of the people who live there. Tight housing turns booms into rents, and where a child grows up
changes the adult.

It opens on Thomas Schelling's checkerboard, played by Agora: coins content with a third of their neighbours alike
end, after seven rounds, with 76% of their neighbours alike. From there it covers:

- a game: guess how mixed the board stays; then the whole curve of final mixing against tolerance, with the region
  where the board never settles, and James Sakoda's earlier model;
- von Thünen's rings around the Island's market town (vegetables and milk to 3 km, firewood to 10, grain to 35,
  cattle to 100), and a railway that halves the freight on grain and cattle (grain to 70 km, cattle to 200);
- the monocentric city of Alonso, Muth and Mills, solved for a closed town of a million households: rent falls 6.7% a
  kilometre near the centre and the edge is at 19 km; the car (commuting half as dear) spreads it to 31 km and cuts
  central density 74%; the lift (height 40% cheaper) builds it up instead;
- why cities exist: Marshall's "in the air" and Duranton and Puga's sharing, matching and learning; agglomeration and
  sorting on the Island (across towns 0.057, from movers 0.029, planted 0.03) and in France (Combes, Duranton,
  Gobillon and Roux: raw 0.05, preferred 0.02);
- Zipf's law for America's 387 metropolitan areas in 2024 (exponent 1.18 for the largest hundred, 0.90 for all), and
  Gibrat's proportional growth with a floor (20,000 towns settle at 0.95; theory 1.05);
- Krugman's core and periphery solved by Agora: the wiggle diagram at three trade costs, and the tomahawk with its
  break point (1.63) and sustain point (1.81);
- an intermission without narration: the share of the world's people living in towns and cities, 1500-2025 (HYDE
  3.5), with America and China, as a tune;
- spatial equilibrium (Rosen, Roback) on the Island's six towns: amenities read back exactly from wages and rents; a
  productivity shock and an amenity shock;
- housing supply: a demand shock against elastic and inelastic supply; Saiz's elasticities (Miami 0.60 to Wichita
  5.45, population-weighted 1.75); house prices since 2000 in the twenty Case-Shiller metros against them (correlation
  −0.42); Hsieh and Moretti's 36% and Greaney's comment;
- rent control in San Francisco after 1994 (Diamond, McQuade and Qian: tenants 20% less mobile, rental supply −15%);
- Moving to Opportunity (Chetty, Hendren and Katz: +$3,477 a year, 31%, for children who moved before 13);
- the Berlin Wall (Ahlfeldt, Redding, Sturm and Wolf), with a line city solved by Agora with their parameters;
- transport: Donaldson's railways of the Raj (+16% real income), Baum-Snow's highways (−18% per highway), and China's
  move to the cities under the hukou;
- place-based policy: Shenzhen, the Tennessee Valley Authority (Kline and Moretti), and the incidence of a subsidy
  where housing is tight and where it is not;
- two dials, agglomeration and housing supply (both new); the Fact of Zipf's law gets Agora's column; *Called it?* on
  Frances Cairncross's *The Death of Distance* (partly right); a frontier chapter on working from home (7% of paid
  days in 2019, 62% in May 2020, about 26% since) and the climate.

## Build it

```bash
python -m videos.economics.econ37.compute              # every number (about half a minute), into .cache/econ37/
python tools/qa_scene.py econ37 Mono                   # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ37 -q l   # the whole part, silent preview
python tools/build.py econ37                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 37                     # the lab
```

The data are in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): the Census Bureau's Vintage 2024 population of every
metropolitan area; HYDE 3.5's urban shares since 1500, via Our World in Data (CC BY 4.0); from FRED, the twenty
S&P CoreLogic Case-Shiller metropolitan indices and Barrero, Bloom and Davis's work-from-home rate (CC BY 4.0); and
tables transcribed from Saiz, Combes et al., Ahlfeldt et al., Ciccone and Hall, Diamond et al., Chetty et al., Hsieh
and Moretti with Greaney's comment, Donaldson, Baum-Snow, Kline and Moretti, Shenzhen's census and Schelling's history.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | A board of coins | Schelling's checkerboard, played; America's largest metros; the question; objectives |
| 1 | Play it: Schelling's rule | Guess the final mixing; the board by rounds; the whole tolerance curve |
| 2 | Von Thünen's rings | Bid rents, the upper envelope, the rings; a railway |
| 3 | The monocentric city | The rent gradient derived; height and density; the car and the lift |
| 4 | Why cities exist | Sharing, matching, learning; sorting on the Island; movers; France |
| 5 | Zipf's law | America's rank-size plot; Gibrat with a floor; the Fact |
| 6 | Core and periphery | Krugman's loop; the wiggle diagram; the tomahawk |
| — | Intermission | Five centuries of moving to town, as a tune |
| 7 | Spatial equilibrium | Six towns; quality of life read from prices; two shocks |
| 8 | Housing supply | Elastic and inelastic supply; Saiz; prices since 2000; the aggregate cost, contested |
| 9 | Rent control | San Francisco's 1994 expansion and what it did |
| 10 | Neighbourhoods and children | Moving to Opportunity's lottery and the children's earnings |
| 11 | The Berlin Wall as an experiment | Division and reunion; a line city with the paper's parameters |
| 12 | Transport | Railways of the Raj; highways and suburbs; China and the hukou |
| 13 | Place-based policy | Shenzhen; the TVA; who gains from a subsidy to a place |
| 14 | The Dials | Agglomeration; housing supply |
| 15 | In practice | Planning, property, transport appraisal; *Called it?* on Cairncross (1997) |
| 16 | Frontier | Working from home; the climate; density and emissions; sorting; housing |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 38, *Work and Wages* |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's city (`explainer.economics.agora.city`) with the Island's
Part 37 truths, or from the Data Room; the narration states the cached numbers.

- **Schelling.** A 40 by 40 board whose edges wrap, a tenth empty, two kinds in equal numbers; a coin is content if at
  least a third of its occupied neighbours (of eight) are its own kind; discontented coins move, in random order, to a
  random empty square where they would be content. The tolerance curve averages three boards of 30 by 30 at each
  threshold.
- **Von Thünen.** Four crops with yields, prices, costs and freight rates chosen so the rings fall at 3, 10, 35 and
  100 km; the railway halves the freight on grain and cattle.
- **The monocentric city.** A closed city of a million households with income $60,000 and commuting at $1,000 a
  kilometre a year; Cobb-Douglas utility over goods and floor space (housing share 0.25); floor space built from land
  and capital (land share 0.25, capital costing 0.06 a year); farming pays $0.10 a square metre a year at the edge.
  Common utility is solved so that the population adds up. The car halves the commuting cost; the lift cuts the cost
  of capital by 40%.
- **Agglomeration.** 60 towns, 60,000 workers; productivity rises with density at elasticity 0.03; abler workers prefer
  denser towns (a logit taste of 0.3 times ability times log density); a fifth move to a random town in a second year.
- **Zipf.** The Gabaix-Ibragimov rank − ½ regression; Gibrat's growth for 20,000 towns over 3,000 periods with shocks
  of standard deviation 0.2 and a floor at 5% of the mean, fitted on the largest tenth.
- **Core and periphery.** Fujita, Krugman and Venables's two-region model with μ = 0.4 and σ = 5, solved by damped
  iteration; the break point by their closed form (checked against the slope of the wage gap), the sustain point by
  root-finding.
- **The six towns.** Log-linear labour demand (slope 0.3), housing supply through the average town's size with each
  town's elasticity, housing share 0.3, common utility solved so that populations add up.
- **Prices since 2000.** The average of each Case-Shiller index over 2025 divided by its average over 2000, against
  Saiz's Table VI; consumer prices from the CPI.
- **The line city.** 61 blocks from −6 to 6 km; Fréchet commuting (ε = 6.83) with commuting costs exp(−0.25 km) in
  probability; production externalities 0.07 decaying at 0.36 a kilometre; fundamental productivity peaked 1.5 km
  east of the wall, with a smaller western centre at −3.5 km. Division solves the western blocks alone with the same
  residents; price changes are relative to the western average.

## Problems and solutions

**1.** *Rent gradient: commuting costs $1,000 a kilometre a year and a household near the centre has 150 m². How fast
must floor rent fall with distance?*

*Solution.* Muth's condition p′(x) h(x) = −t: the rent saved on the household's floor space must equal the extra
commuting cost. So p′ = −1,000/150 ≈ −$6.67 per square metre per year for each kilometre.

**2.** *Von Thünen: grain yields 2.6 tons a hectare, sells for $150 a ton, costs $90 to grow and $1 a ton-kilometre to
cart. Find its bid rent at the market and where it reaches zero.*

*Solution.* Bid rent = 2.6 × (150 − 90 − x) = 2.6 (60 − x) dollars a hectare: $156 at the market, falling to zero at
60 km. (In the film cattle outbid grain beyond 35 km.)

**3.** *Zipf: with an exponent of one and a largest city of 20 million, how large are the 10th and the 100th?*

*Solution.* With exponent one, size is proportional to one over rank: the 10th has 2 million people, the 100th
200,000.

**4.** *Agglomeration: with an elasticity of 0.03, how much more productive is a worker in a city twice as dense? Ten
times?*

*Solution.* 2^0.03 − 1 ≈ 2.1%; 10^0.03 − 1 ≈ 7.2%.

**5.** *Quality of life: with α = 0.3, town A's log wage is 0.10 above B's and its log rent 0.40 above. Which is
nicer, and by how much?*

*Solution.* Quality of life read from prices is α log r − log w: 0.3 × 0.40 − 0.10 = 0.02. A's rent premium is more
than its wage premium pays for, so people value A more: by about 2% of income.

**6.** *Housing: demand rises 20%, demand elasticity 1. Find the change in price and quantity with supply elasticities
0.6 and 3.*

*Solution.* In logs, Δp = 0.2/(ε_s + 1) and Δq = ε_s Δp. With 0.6: prices +12.5%, the stock +7.5%. With 3: prices +5%,
the stock +15%.

**7.** *Core and periphery: compute the break point for μ = 0.4 and σ = 5.*

*Solution.* With ρ = (σ − 1)/σ = 0.8, T^{σ−1} = (ρ + μ)(1 + μ)/((ρ − μ)(1 − μ)) = (1.2 × 1.4)/(0.4 × 0.6) = 7, so
T = 7^{1/4} ≈ 1.63: shipping must cost less than 63% of a good's value for the even spread to break.

**8.** ★ *Gibrat with a floor: show that a stationary power law has exponent 1/(1 − s_min/s̄).*

*Solution.* Measure sizes relative to the mean, so s̄ = 1. Above the floor, growth is multiplicative with mean one, so
a density proportional to s^{−ζ−1} is carried into itself (Champernowne and Kesten): sizes above any level shrink and
grow in the same proportions everywhere. The floor makes the distribution Pareto with minimum s_min, whose mean is
ζ s_min/(ζ − 1). Setting the mean to one gives ζ = 1/(1 − s_min); as the floor goes to zero, ζ goes to one, Zipf's
law.

## Lab and interactive

- `python -m videos.economics.labs 37`: Schelling's board and its tolerance curve, von Thünen's rings, the monocentric
  city with the car and the lift, sorting and movers, Zipf's law on the Census data and Gibrat's towns, the core and
  periphery with its break point checked, the Island's towns with quality of life read from prices, and the line city
  divided.
- The interactive (course site): Schelling's board. The reader sets how many like neighbours each coin wants and how
  many squares are empty, runs the board, and watches the share of like neighbours climb.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[37]`; the agglomeration elasticity and
the housing supply elasticity are dials (`explainer/economics/dials.py`); Cairncross's 1997 book is a *Called it?*
entry (`explainer/economics/calls.py`). The Census Bureau's estimates, HYDE's urban shares via Our World in Data and
FRED's series were retrieved on 2026-11-20. Saiz's elasticities were read from Table VI of the published article;
Combes et al.'s estimates from the NBER chapter; Ahlfeldt et al.'s from NBER Working Paper 20354; Diamond et al.'s,
Chetty et al.'s, Hsieh and Moretti's, Greaney's and Donaldson's from the AEA's abstracts (Donaldson's 16% from the
NBER working paper and MIT's summary); Baum-Snow's and Kline and Moretti's from their abstracts. Ciccone and Hall's 5-6%
is from secondary summaries; the working paper's abstract gives no number. Schelling's story is told from
Hegselmann's history: the model first appeared in a 1969 RAND memorandum; the plan's tale of a plane journey was not
found in a source. Shenzhen's 1979 population (314,100) is the statistical bureau's figure as tabulated; the often
quoted "fishing village of 30,000" appears to count workers, not residents.
