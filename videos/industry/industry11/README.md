# Industry, Built: Part 11, Heavy Materials

Part 11 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth of Act II, *Out of the Ground*. It asks: why do the things everything is
made of earn so little? It answers with the World Steel Association's yearbooks, outlooks and climate paper; the US
Geological Survey's Mineral Commodity Summaries 2026 and its historical statistics since 1900; the International
Aluminium Institute's statistics; the BLS's producer prices and the Federal Reserve's output and capacity figures; the
European Commission's 1994 cement cartel decision and the EU's carbon border regulation; the 10-K accounts of eighteen
steel, cement, stone, aluminium and packaging companies and the 20-F accounts of ArcelorMittal and Cemex; Bessemer's own
account of 1856; and the Works' mills. The answer: steel, cement, aluminium and stone are among the cheapest things the
world buys by weight, and are made in huge plants whose fixed costs make them run in good times and bad, so gluts last
and profits swing. The money stays where something cannot be copied: a scrap-fed mill close to its customers, cheap
power for a smelter, and above all a quarry with a permit near a growing city.

It opens in Cheltenham on 13 August 1856, where a Welsh ironmaster laughed at "a fellow come down from London to read a
paper on the manufacture of malleable iron without fuel": Henry Bessemer, whose converter burned the carbon out of pig
iron with a blast of air. Today the world makes 1,849 million tonnes of steel, about 3.8 billion tonnes of cement and
74 million tonnes of aluminium a year, and a kilogram of steel sheet (94 cents) costs less than a kilogram of bananas
($1.44). From there it covers:

- Run it: an integrated mill (3 million tonnes, $520 a tonne of variable cost, $750 million a year of fixed costs)
  through an eight-quarter glut. Running full loses $308 million, banking the furnace $317 million, cutting output $357
  million; but if every mill runs full the price falls to $482 and banking wins. What Cleveland-Cliffs and US Steel did
  in 2025;
- steel two ways: a blast furnace's recipe (Cliffs: 1.4 tons of pellets, 0.35 of coke, 0.3 of scrap) against a
  minimill's (Nucor: 1.1 tons of scrap); 2.34 against 0.69 tonnes of CO2 a tonne; electric furnaces make 11% of
  China's steel, 30% of the world's and 71% of America's;
- a ton of steel and its dollar: Nucor's $1,008 a ton in 2025, $385 of it scrap, a $623 spread; the spread from $386
  (2020) to $841 (2022) and Nucor's profit from $0.7bn to $7.6bn; Cliffs at the same price with a gross margin of −5%;
  the real price of steel since 1947, about where it was in 1960;
- a plant that must run: the Works' cost curves (fixed costs 32% of an integrated mill's tonne at full output, 15% of a
  minimill's); US iron and steel capacity utilization since 1972 (50% in 1982, 51% in 2009); Nucor's mills since 2003;
  four steelmakers' profits since 2016;
- disruption from below: Christensen's ladder from rebar to sheet; Darlington (1969), Nucor-Yamato (1988), Crawfordsville
  (the end of the 1980s); the US electric-furnace share from 38% (1992) to 71% (2025); Nucor and US Steel, the same size
  in 2010, $30bn and $3bn of profit over 2010-2024, and US Steel sold to Nippon Steel in 2025;
- half the world's steel: China from 13% (1995) to 52% (2025); its steel use down from 954 to 796 million tonnes
  (2021-2025) while its exports doubled from 66 to 134 million tonnes, more than all the steel America makes; tariffs of
  25% and then 50%;
- cement, a circle on the map: the kiln and its chemistry (0.51 t of CO2 from the rock in a tonne of clinker); China's
  1.7 billion tonnes; 97 US plants and $160 a tonne; the Works' two kilns and their market areas; 1989's trucking costs
  (500 km of road added half the price); the four largest firms' 52% of US cement against 15% of ready-mix;
- the home market rule: the European cartel of 1983-1994, 42 companies and associations fined about €250 million, the
  fines cut by almost €140 million in 2000; Amrize's spin-off from Holcim and Martin Marietta's cement sales;
- an intermission: world steel production since 1950, and the story so far;
- electricity in solid form: 13,880 kWh a tonne of aluminium (16,951 in 1980), a 500,000-tonne smelter's 790 MW;
  China's share from 11% (2000) to 60% (2025); US primary output from 4.7 million tonnes (1980) to 0.66 million; the
  Gulf's output halved in April 2026 and the London price to $3,658 in May; a US price of 180 cents a pound behind a 50%
  tariff, against about 119 cents in London;
- boxes, cans and bottles: four firms make 52% of US corrugated boxes, 62% of cans and 88% of glass containers;
  Smurfit Westrock (2024) and International Paper with DS Smith (2025); US paper and board output down 46% since 1995;
- the quarry with a permit: 1.5 billion tonnes of crushed stone from 3,500 quarries; Vulcan's 80% by truck; the real
  price of stone from $10.52 (2000) to $19.39 (2025); Vulcan's $21.98 a ton with $8.66 of gross profit and 73 years of
  reserves;
- the hardest carbon: cement's 1.48 billion tonnes of process CO2 (3.8% of the world's fossil and industrial CO2) and
  steel's 7-8% of greenhouse gases; carbon against hydrogen as the reducer (54 kg of hydrogen per tonne of iron: $108-271
  at $2-5 a kg); 63% of US cement now blended; the EU's border charge from 1 January 2026;
- the landscape, November 2026: the largest steelmakers (China Baowu 124.8 million tonnes; Nucor 16th), the listed
  companies by size and margin, and what to watch;
- *Called it?*: worldsteel's year-ahead forecasts for China (flat, flat, −1%) against the outcomes (−2.3%, −5.4%,
  −7.1%), and this series' call that China's 2026 steel demand will turn out to have fallen by more than the 2.0%
  forecast in October 2026 (70%).

## Build it

```bash
python -m videos.industry.industry11.compute               # every number, printed
EXPLAINER_TTS=silent python tools/build.py industry11 -q l  # the whole part, silent preview
python tools/build.py industry11                           # 1080p30 with narration
python -m videos.industry.labs 11                          # the lab
python -m pytest tests/industry                            # the Register, the tables and the Works (test_mill.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p11.py`), a transcribed table
(`explainer/industry/data/tables.py`: worldsteel's yearbooks, Nucor's 10-Ks year by year, the International Aluminium
Institute) or comes from the Filing Room: USGS history (`usgs_heavy.csv`), producer prices and output via FRED
(`fred_heavy.csv`, `fred_metals.csv`), the Global Carbon Budget via Our World in Data (`owid_co2.csv`), the companies'
10-Ks and 20-Fs (`sec_annual.csv`, `sec_ifrs.csv`) and the Economic Census (`census_conc_2022.csv`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Iron without fuel | Bessemer at Cheltenham, 1856; the world's tonnages; a kilogram's price; the title |
| 1 | Run it: a mill in a glut | A blast furnace through eight quarters; if every mill runs full; 2025's idlings |
| 2 | Steel two ways | The blast furnace and converter; the minimill; who uses which |
| 3 | A ton of steel and its dollar | Nucor's ton and its spread; Cliffs; the real price since 1947 |
| 4 | A plant that must run | Cost curves; capacity utilization since 1972; profits |
| 5 | Disruption from below | Christensen's ladder; the electric share; Nucor and US Steel |
| 6 | Half the world's steel | China's rise; the ten producers; exports; tariffs |
| 7 | Cement: a circle on the map | The kiln; the world's cement; two kilns and their market areas |
| 8 | The home market rule | Europe's cement cartel; the fines; trading the circles |
| — | Intermission | World steel since 1950; the story so far |
| 9 | Electricity in solid form | The potline; China's share; the Gulf's shock and the tariff premium |
| 10 | Boxes, cans and bottles | Concentration; the mergers; paper's decline |
| 11 | The quarry with a permit | Trucking; the real price of stone since 1900; Vulcan's ton |
| 12 | The hardest carbon | Emissions; carbon against hydrogen; the EU's border charge |
| 13 | The landscape, November 2026 | The steelmakers; the listed companies; what to watch |
| 14 | Called it? | worldsteel's China forecasts; this series' call |
| — | Heavy, cheap and everywhere | The answers; Part 12, chemicals |

## What is computed, and from what

`compute.py` reads worldsteel's figures (transcribed into `tables.py` and the Register), USGS's Data Series 140 and
Mineral Commodity Summaries, the IAI's statistics, FRED's producer prices and Federal Reserve series, and the SEC's
company facts. A kilogram's price divides USGS's 2025 unit values for stone and cement, Cliffs' 2025 hot-rolled coil
index (a US short ton of 907 kg) and the IMF's latest aluminium price by 1,000, and converts the BLS's banana price per
pound. Nucor's metal per ton is 1.1 gross tons of scrap at its reported cost, converted from gross (2,240 lb) to short
(2,000 lb) tons. The real price of steel is the PPI for steel mill products over the CPI (both from 1947), set to 1 in
2025. The real price of stone uses USGS's own 1998-dollar series (1900-2021), carried to today's dollars with the CPI,
and the Mineral Commodity Summaries' nominal values for 2022-2025. China's share of world steel uses each year from
the latest worldsteel publication that gives it. Company margins are net income over revenue, averaged over five years;
Ball's and Martin Marietta's 2024, dominated by one sale each, are left out. The glut game, the cost curves, the two kilns
and the hydrogen arithmetic are the Works' (`explainer/industry/works/mill.py`), labelled as models on screen.

## Problems and solutions

**1.** *A mill can make 2 million tonnes a year. Its variable cost is $550 a tonne and its fixed costs $500 million a
year. (a) What is its break-even price at full output, and at 70%? (b) The price is $700. Should it keep running at
70%, or shut down entirely if half its fixed costs continue while it is shut?*

*Solution.* (a) At full output the fixed cost per tonne is 500 / 2 = $250, so it breaks even at 550 + 250 = $800. At 70%
it makes 1.4 million tonnes, fixed cost per tonne 500 / 1.4 = $357, break-even $907. (b) Running at 70%: (700 − 550) ×
1.4 − 500 = −$290 million. Shut: −$250 million (half the fixed costs). Shutting loses less here, but only just; add a
restart cost of $40 million and the two are equal. That is why mills hesitate.

**2.** *A minimill sells steel for $1,000 a short ton and uses 1.1 gross tons of scrap per ton of steel, at $400 a gross
ton. What is its metal cost per short ton, and its metal spread? If steel falls to $800 and scrap to $320, what happens
to the spread?*

*Solution.* A gross ton is 2,240 lb and a short ton 2,000 lb, so 1.1 gross tons cost 1.1 × 400 × 2,000 / 2,240 = $393 per
short ton of steel; the spread is 1,000 − 393 = $607. At $800 and $320 the metal costs 1.1 × 320 × 0.893 = $314, and the
spread is $486: it falls by $121, much less than the $200 fall in price, because scrap moves with steel.

**3.** *Two cement plants are 300 km apart, each with a cash cost of $95 a tonne at the gate. Trucking costs 12 cents a
tonne-kilometre. (a) Where is the border between their markets? (b) What is the most plant A can charge a customer at
its own gate, and one 100 km away towards B, if B will deliver at cost?*

*Solution.* (a) Halfway, 150 km from each, where both deliver at 95 + 0.12 × 150 = $113. (b) At A's gate, B delivers at
95 + 0.12 × 300 = $131, so A can charge up to $131 (a margin of $36). At 100 km towards B, B's delivered cost is 95 +
0.12 × 200 = $119 and A's own cost there is 95 + 12 = $107, so A can charge up to $119, a margin of $12. Margins are
fattest at home.

**4.** *How much CO2 comes from the chemistry alone when (a) a tonne of clinker that is 65% lime (CaO) is made from
limestone, and (b) a tonne of iron is reduced from haematite with carbon monoxide? (CaCO3 → CaO + CO2; Fe2O3 + 3CO →
2Fe + 3CO2; molar masses: CaO 56.08, CO2 44.01, Fe 55.85.)*

*Solution.* (a) 0.65 × 44.01 / 56.08 = 0.51 t of CO2 per tonne of clinker. (b) Two moles of iron need three of CO and
release three of CO2: 1.5 × 44.01 / 55.85 = 1.18 t of CO2 per tonne of iron, before any fuel is burned. Hydrogen instead
needs 1.5 × 2.016 / 55.85 = 0.054 t, 54 kg of hydrogen per tonne of iron.

**5.** *A quarry sells stone at $22 a ton at its gate; trucking costs 20 cents a ton-mile. At what distance has the
delivered price doubled? A rival quarry 60 miles away has the same costs. At the halfway point, how much does each pay
in trucking, as a share of the delivered price?*

*Solution.* Doubling: 22 / 0.20 = 110 miles. At the halfway point, 30 miles from each, trucking costs 30 × 0.20 = $6, and
the delivered price is $28, so trucking is 6 / 28 = 21% of it. Close to its quarry, a producer faces no rival who can
match it without paying the trucking.

## Glossary

- **Pig iron:** the iron that runs out of a blast furnace, with 4-5% carbon; hard and brittle.
- **Integrated mill:** a steelworks that makes iron from ore in a blast furnace and turns it into steel in a converter.
- **Basic oxygen furnace (converter):** the vessel where oxygen is blown through molten iron to burn off its carbon.
- **Minimill, electric arc furnace:** a steelworks that melts scrap (or directly reduced iron) with electricity.
- **Metal spread:** a steelmaker's selling price less the cost of the metal in each ton.
- **Capacity utilization:** output as a share of what the plants could make.
- **Banking a furnace:** stopping a blast furnace while keeping it ready to restart.
- **Clinker:** the nodules that come out of a cement kiln, ground with gypsum into cement.
- **Calcination:** heating limestone so that it gives off carbon dioxide and leaves lime.
- **Aggregates:** crushed stone, sand and gravel used in concrete, asphalt and road beds.
- **Concentration (CR4):** the share of a market held by its four largest firms.
- **Carbon border adjustment:** a charge on imports for the carbon emitted in making them.

## Lab and interactive

- `python -m videos.industry.labs 11`: a kilogram's price; the glut game and what happens if every mill runs full; the
  two routes' recipes and CO2; Nucor's spread and the real price of steel; China's share and exports; cement's market
  areas; aluminium's energy and China's share; the real price of stone and Vulcan's ton; the chemistry of the carbon
  chapter; worldsteel's forecasts; this series' call.
- The interactive (course site): the mill in a glut. Set the depth and length of the glut, the share of other mills
  that run full and the restart cost, and watch the three strategies' losses quarter by quarter.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p11.py`), the transcribed tables
(`explainer/industry/data/tables.py`) or the Filing Room (`explainer/industry/data/SOURCES.md`). The main ones:

- World Steel Association: World Steel in Figures 2022, 2024 and 2026; Steel Statistical Yearbooks 2002, 2011 and 2020;
  Short Range Outlooks (October 2022-2026, April 2026); 'October 2026 crude steel production' (24 November 2026);
  'Climate change and the production of iron and steel' (October 2025).
- US Geological Survey: Mineral Commodity Summaries 2026 (iron and steel, iron and steel scrap, cement, aluminum, stone
  (crushed)); Data Series 140.
- International Aluminium Institute, statistics: primary aluminium production; smelting energy intensity.
- BLS producer price indexes, the CPI and average prices; Federal Reserve G.17; Census construction spending; via FRED.
- US Census Bureau, 2022 Economic Census, concentration of largest firms.
- Global Carbon Budget (2025), via Our World in Data.
- European Commission Decision 94/815/EC (Cement), 30 November 1994; Court of First Instance, Press Release 16/00 (15
  March 2000); Regulation (EU) 2023/956.
- SEC EDGAR: Forms 10-K of Nucor (2003-2025), Steel Dynamics, Cleveland-Cliffs, US Steel, Commercial Metals, CRH, Amrize,
  Vulcan, Martin Marietta, Eagle Materials, Alcoa, Century Aluminum, International Paper, Smurfit Westrock, Packaging
  Corporation of America, Ball, Crown and O-I Glass; Forms 20-F of ArcelorMittal and Cemex.
- Nucor Corporation, 'History'.
- Sir Henry Bessemer, F.R.S.: An Autobiography (1905); Clayton Christensen, *The Innovator's Dilemma* (1997).
