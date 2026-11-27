# Industry, Built: Part 12, Chemicals

Part 12 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth of Act II, *Out of the Ground*. It asks: how does a molecule of gas become a
thousand products, and where in the chain is the money? It answers with the Nobel Foundation's records of Haber and
Bosch; the US Geological Survey's Mineral Commodity Summaries 2026 and its historical statistics for nitrogen; the EIA's
cracker yields, its natural gas liquids series, its Today in Energy reports and its Annual Energy Outlook of 2005; the
IMF's gas and oil prices, the BLS's producer prices and the Federal Reserve's capacity figures; Eurostat's industrial
production; the OECD's plastics figures via Our World in Data; the 10-K accounts of seventeen American chemical, gas,
fertilizer and paint companies and ICL's 20-F; the 8-Ks of 3M and Chemours; the EPA's PFAS rule; the Supreme Court of
India's Bhopal judgment of 1989; and the Works' cracker and gas plant. The answer: at the root of the tree the
feedstock is most of the cost, so the cheapest molecules win, and shale gave America the cheapest in the rich world while
Europe's dear gas closes its plants; everyone builds in the good years, so commodity profits swing; further along the
tree, contracts (industrial gases) and service and brands (paint) steady the money; and the bill for harm arrives decades
after the profit.

It opens with Fritz Haber's patent of 13 October 1908 on the synthesis of ammonia from its elements, and Carl Bosch's
plant around 1913. The world made 4.8 million tonnes of nitrogen as ammonia in 1950 and about 160 million in 2025, while
the number of people rose from about 1.7 billion to more than 8 billion and the nitrogen spread on a hectare of cropland
from 9 kg (1961) to 71 kg (2024). From there it covers:

- Run it: a $6bn, 1.5-million-tonne cracker built in 2012, in Texas on ethane or in Europe on naphtha, played through
  2013-2026 with the IMF's gas and oil prices and a world price set by the dearest crackers. Texas's margin: $939 a
  tonne in 2013, $418 in 2016, $788 in 2026; cash of about $12.3bn by 2026, paid back by 2020. Europe's: $0-252, $0.6bn
  in all. What happened: US ethylene capacity from about 27 to almost 40 million tonnes (2013-2020); Dow's Böhlen
  cracker to close by the end of 2027; INEOS's Antwerp cracker built for about 80,000 barrels a day of American ethane;
- three raw materials, a thousand products: gas, oil and salt; the building blocks; American chemical sales of about
  $901bn in 2022 (Economic Census);
- the cracker: inside the furnace; EIA's yields (a tonne of ethane gives 81% ethylene, of naphtha 39%); the cash cost
  of a tonne of ethylene at 2026 prices, $360 in Texas and $1,097 in Europe, piece by piece;
- the shale advantage: wet gas and the gas plant; American ethane from 314 thousand barrels a day (1981) to 3,361
  (August 2026) and exports from 14 (2014) to 794; gas in three markets since 2000; the cost gap, within $29 a tonne in
  2001-2005 and about $608 from 2010;
- the commodity cycle: why everyone builds at once; US chemical capacity utilization since 1948 (67% in 2009, 80% in
  2021); resin prices (+33% in 2021); Dow, LyondellBasell, Westlake and Olin: $15.2bn of profit in 2021, a loss of
  $5.0bn in 2025;
- fertilizer: nitrogen, phosphorus and potassium; Haber's chemistry; CF Industries' 34.6 million Btu of gas in a ton of
  ammonia; the gas in a ton in 2022, $1,298 in Europe against a Gulf price of $1,070 and $225 in America; CF's British
  closures; the producers (China 49, India 15, Russia 15, the US 14 million tonnes of N; potash: Canada 15, Russia 10,
  China 6.3, Belarus 6 million tonnes of K2O); CF's $3.3bn in 2022 and its 22% five-year margin;
- an intermission: the world's ammonia since 1946; America's, which fell by almost half when its gas got dear in the
  2000s and came back with shale; and the story so far;
- the plant at the fence: air separation; cylinders, trucks and pipes; Linde's 10-20 and Air Products' 15-20 year
  contracts; the Works' take-or-pay plant; Linde's profit rising every year from 2019 to 2025; Air Products' $3.0bn of
  charges in fiscal 2025; prices of industrial gases against petrochemicals;
- sold by performance: what is in a can of paint; Sherwin-Williams' 4,853 stores; 49 cents of each dollar of sales left
  after the cost of goods against Dow's 6; paint prices against petrochemicals; IFF's $6.0bn of goodwill write-downs;
- Europe's energy shock: European gas at $70 in August 2022 against America's $9, and still about eight times
  America's in September 2026; Germany's chemical output 23% below 2021, its lowest since January 2009; the EU's 21%;
  the map of closures and imports;
- plastics, and where they go: polymerization; production from 2 to 460 million tonnes (1950-2019), about 59 kg a
  person; the fate of 353 million tonnes of waste in 2019 (49% landfilled, 22% mismanaged, 19% burned, 9% recycled);
- the state and harm: Bhopal, 2 December 1984 (2,660 killed at once by the count before the Supreme Court; $470 million);
  PFAS, the EPA's 4 parts per trillion (about four drops in twenty Olympic pools); 3M's $10.5-12.5bn and Chemours, DuPont
  and Corteva's $1.185bn;
- the landscape, November 2026: the listed companies by revenue and five-year margin, and what to watch;
- *Called it?*: the EIA's outlook of February 2005 (net LNG imports of 6.4 trillion cubic feet in 2025; America
  exported 5.5) and this series' call that Germany's chemical output will average below 79.8 in 2027 (75%).

## Build it

```bash
python -m videos.industry.industry12.compute               # every number, printed
EXPLAINER_TTS=silent python tools/build.py industry12 -q l  # the whole part, silent preview
python tools/build.py industry12                           # 1080p30 with narration
python -m videos.industry.labs 12                          # the lab
python -m pytest tests/industry                            # the Register, the tables and the Works (test_cracker.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p12.py`) or comes from the Filing Room: the IMF's
prices and the BLS's and the Federal Reserve's series via FRED (`fred_chem.csv`), the EIA's natural gas liquids and gas
series (`eia_ngl.csv`, `eia_gas.csv`), USGS history (`usgs_heavy.csv`), Eurostat (`eurostat_chem.csv`), Our World in
Data (`owid_chem.csv`), the companies' 10-Ks and 20-Fs (`sec_annual.csv`, `sec_ifrs.csv`) and the Economic Census
(`census_conc_2022.csv`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Bread from air | Haber's patent; the chemistry; ammonia and people since 1950; the tree; the title |
| 1 | Run it: a cracker for forty years | Texas on ethane or Europe on naphtha, 2013-2026; what the industry did |
| 2 | Three raw materials, a thousand products | The tree; America's chemical sales by group |
| 3 | The cracker | Inside the furnace; yields; a tonne of ethylene's cost, piece by piece |
| 4 | The shale advantage | Wet gas; American ethane and its exports; gas in three markets; the gap |
| 5 | The commodity cycle | The building wave; capacity in use since 1948; resin prices; four makers' profits |
| 6 | Fertilizer: gas into food | N, P and K; Haber's chemistry and CF's gas; Europe's costs; producers; profits |
| — | Intermission | The world's ammonia since 1946; America's twist; the story so far |
| 7 | The plant at the fence | Air separation; delivery; the take-or-pay contract; Linde against Dow; prices |
| 8 | Sold by performance | A can of paint; the dollar of sales; paint prices; margins and IFF |
| 9 | Europe's energy shock | Gas since 2019; Germany's and the EU's output; the map |
| 10 | Plastics, and where they go | Polymerization; production since 1950; the fate of waste |
| 11 | The state and harm | Bhopal; PFAS; four parts per trillion; the settlements |
| 12 | The landscape, November 2026 | The listed companies; what to watch |
| 13 | Called it? | The EIA's 2005 outlook; this series' call |
| — | From molecules to money | The answers; Part 13, electricity |

## What is computed, and from what

`compute.py` reads the Filing Room's extracts and the Register. Annual gas and oil prices average the IMF's monthly
prices (a year needs nine months). The cracker is the Works' (`explainer/industry/works/cracker.py`): EIA's yields
(AEO2026 Industrial Demand Module, Table 6); ethane priced as gas plus a $60 fee, naphtha at 90% of Brent per barrel and
9 barrels a tonne; hydrogen and methane credited at the local gas price, other by-products at 1.1 times naphtha's price;
17 (ethane) and 25 (naphtha) million Btu of fuel a tonne of ethylene; $150 of other cash costs. The world price is the
dearest of a Texas, a European and an Asian cracker plus a markup of $25 a tonne for each point by which US chemical
capacity utilization exceeds 70%: all assumptions, labelled on screen. The gas in a ton of ammonia is CF's 2025 gas use
over its gross ammonia output, times the IMF's gas prices. Company margins are net income over revenue, averaged over five
years; DuPont, whose accounts are dominated by businesses sold or spun off, is left off the landscape. Germany's and the
EU's output are Eurostat's seasonally and calendar adjusted index (2021 = 100). The drops-in-pools picture assumes a drop
of 0.05 ml and an Olympic pool of 2,500 cubic metres.

## Problems and solutions

**1.** *A naphtha cracker pays $600 a tonne for naphtha; 39% of it becomes ethylene, and the by-products from a tonne of
feed sell for $430. The furnace burns 25 million Btu of gas per tonne of ethylene at $12, and other cash costs are $150
a tonne. An ethane cracker pays $200 a tonne for ethane, gets 80% ethylene and $40 of by-products per tonne of feed, and
burns 17 million Btu at $3. What does a tonne of ethylene cost each?*

*Solution.* Naphtha: (600 − 430) / 0.39 = $436 of net feed, plus 25 × 12 = $300 of fuel and $150: $886. Ethane: (200 −
40) / 0.80 = $200, plus 17 × 3 = $51 and $150: $401. The naphtha cracker depends on its by-products (they recover most of
its feed cost) and on the price of gas for its furnace; the ethane cracker depends on almost nothing but cheap ethane.

**2.** *A ton of ammonia takes 34.6 million Btu of gas. Ammonia sells for $500 a ton. What is the margin over gas for a
plant paying $4 per million Btu, and for one paying $14? Above what gas price does the gas alone cost more than the
ammonia sells for?*

*Solution.* At $4: 34.6 × 4 = $138, a margin of $362. At $14: $484, a margin of $16, before any other cost. The break-even
is 500 / 34.6 = $14.45 per million Btu. European gas was above that for most of 2022, which is why European plants
stopped.

**3.** *A gas company builds an oxygen plant at a steel mill's fence. The mill pays a fixed fee of $75 million a year and
$40 a tonne for at least 80% of the plant's 1 million tonnes, whether it takes it or not; making a tonne costs $25,
mostly power. What is the gas company's cash in a year when the mill takes 100%, 60% and nothing? Who carries the risk of
a recession?*

*Solution.* 100%: 75 + 40 − 25 = $90 million. 60%: 75 + 0.8 × 40 − 0.6 × 25 = 75 + 32 − 15 = $92 million. Nothing: 75 +
32 = $107 million. The gas company's cash barely moves (it even rises, because it saves the power); the mill pays for gas
it does not use. The contract hands the cycle to the customer.

**4.** *A market for ethylene has 10 million tonnes of capacity running at 92%, and demand grows 4% a year. Seeing fat
margins, three companies each start a 1.5-million-tonne cracker; all three start up four years later. What share of
capacity is in use then? If nobody builds again, how long until plants are 92% full?*

*Solution.* Demand now is 9.2 Mt; in four years, 9.2 × 1.04⁴ = 10.76 Mt, against 14.5 Mt of capacity: 74%. To reach 92%
demand must be 0.92 × 14.5 = 13.34 Mt, which takes ln(13.34 / 10.76) / ln(1.04) = 5.5 more years. A good year, a four-year
build and five and a half lean years: the commodity cycle.

**5.** *A city supplies 400 million litres of drinking water a day. If its water held PFOA at exactly the EPA's limit of 4
parts per trillion, how many grams would pass through the system in a day, and in a year? (A litre of water weighs a
kilogram.)*

*Solution.* 400 million litres weigh 4 × 10⁸ kg; 4 parts per trillion of that is 4 × 10⁸ × 4 × 10⁻¹² = 1.6 × 10⁻³ kg, 1.6
grams a day, about 580 grams a year. Finding and removing so little from so much water is what makes the limit
expensive.

## Glossary

- **Steam cracker:** a furnace that breaks ethane or naphtha into ethylene, propylene and other building blocks.
- **Ethane, naphtha:** a gas separated from natural gas; a light liquid distilled from crude oil.
- **Ethylene:** the two-carbon molecule with a double bond from which polyethylene, PVC and much else are made.
- **Polymer:** a long chain of repeated units, such as polyethylene made of linked ethylene molecules.
- **Haber-Bosch process:** making ammonia from nitrogen in the air and hydrogen, over an iron catalyst at high pressure.
- **Potash:** potassium salts mined from ancient sea beds, the K of fertilizer.
- **Air separation unit:** a plant that liquefies air and distils it into nitrogen, oxygen and argon.
- **Take-or-pay:** a contract in which the customer pays for a minimum amount whether it takes it or not.
- **Gross margin:** sales less the cost of making what was sold, as a share of sales.
- **Goodwill impairment:** writing down the premium a company paid for businesses it bought.
- **PFAS:** per- and polyfluoroalkyl substances, chemicals of carbon and fluorine that barely break down.
- **LNG:** liquefied natural gas, chilled for shipping by sea.

## Lab and interactive

- `python -m videos.industry.labs 12`: Haber's arithmetic; Run it; a tonne of ethylene from ethane and naphtha; American
  ethane and its exports; the shale gap; capacity in use and four makers' profits; the gas in a ton of ammonia; the
  producers; the gas plant's cash; margins by group; Europe's output; plastics; the EIA's 2005 outlook; this series'
  call.
- The interactive (course site): where would you build a cracker? Set American and European gas, Brent and how full the
  plants are, and see each plant's cost, the world price and each plant's cash.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p12.py`) or the Filing Room
(`explainer/industry/data/SOURCES.md`). The main ones:

- The Nobel Foundation: Fritz Haber (1918) and Carl Bosch (1931); Erisman et al., Nature Geoscience (2008), on Haber's
  patent.
- US Geological Survey: Mineral Commodity Summaries 2026 (nitrogen, potash); Data Series 140 (nitrogen).
- US Energy Information Administration: AEO2026 Industrial Demand Module assumptions (cracker yields); natural gas plant
  liquids and LNG series; Today in Energy (21 May 2021; 30 March 2026); Annual Energy Outlook 2005.
- The IMF's primary commodity prices; BLS producer price indexes; Federal Reserve G.17; via FRED.
- Eurostat, industrial production index (sts_inpr_m), manufacture of chemicals.
- Our World in Data: plastics production (Geyer, Jambeck and Law, 2017, and the OECD); the fate of plastic waste (OECD
  Global Plastics Outlook, 2022); nitrogen per hectare (FAO); population (UN).
- US Census Bureau, 2022 Economic Census.
- SEC EDGAR: Forms 10-K of Dow, LyondellBasell, Westlake, Olin, Huntsman, Eastman, Celanese, Linde, Air Products, CF
  Industries, Mosaic, Sherwin-Williams, PPG, Ecolab, IFF, DuPont and Chemours; ICL's Form 20-F; Forms 8-K of 3M (22 June
  2023) and Chemours (2 June 2023).
- US EPA, PFAS National Primary Drinking Water Regulation, Federal Register, 26 April 2024.
- Supreme Court of India, Union Carbide Corporation v. Union of India, 4 May 1989.
