# Industry, Built: Part 15, Semiconductors

Part 15 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first of Act III, *Making*. It asks: why do the most advanced chips come from so few
factories? It answers with Gordon Moore's articles of 1965 and 1975; TSMC's Form 20-F for 2025 and its results for the
third quarter of 2026; the annual reports of ASML, Nvidia, Intel, Micron, the analog makers, the toolmakers and the
design-software companies; General Motors' 10-K for 2021; the Federal Reserve's industrial production of semiconductors
and the BLS's producer prices since 1967; Karl Rupp's microprocessor counts via Our World in Data; the World
Semiconductor Trade Statistics' forecasts and the Semiconductor Industry Association's monthly sales; the Bureau of
Industry and Security's export rules in the Federal Register; and the Works' fab. The answer: Moore's doubling made each
transistor cheaper by making each factory dearer; a fab costs the same full or empty and its newest process yields badly
at first, so only a maker with the whole world's orders can fill one; the foundry model gave TSMC most of those orders;
the machines that print the finest layers come from one company; and governments now pay to have the factories at home
and decide who may buy what they make.

It opens with Moore's four-page article of April 1965: the number of components on the most economical chip had doubled
every year, and by 1975 would be 65,000. Then Hsinchu, 1987: a company that would make other companies' chips and design
none of its own; in 2025 TSMC made 12,682 products for 534 customers and took in about $121 billion. From there it covers:

- Run it: a designer who needs wafers can build its own fab ($20bn, written off over five years, 50,000 wafers a month)
  or book a foundry at $17,000 a wafer. At 5,000 wafers a month a good die costs $29 from the foundry and $183 from its
  own half-empty fab still learning its process (profit $1.07bn against -$3.46bn a year); at 50,000, $29 against $19.
  Owning first pays at about 32,000 wafers a month;
- how a chip is made: one loop repeated on a 300 mm wafer (lay down a film, coat it with resist, print the layer's
  pattern with light through a mask, wash, etch), transistors first and then layer upon layer of wiring;
  about 640 dies of 100 mm2 on one wafer; lines of 25 micrometres in 1961 and 5 in 1975 (Moore); the light from mercury
  lamps (365 nm) to extreme ultraviolet (13.5 nm);
- the node: names that no longer measure anything on the chip; TSMC's wafer revenue by process from 2023 to 2025 (3 nm
  from 6% to 24%) and in the third quarter of 2026 (2 nm 8%, 3 nm 33%, 5 nm 28%);
- yield: defects falling at random, exp(-area x density); a 100 mm2 die yields 90% at 0.1 defects per cm2 and an 800
  mm2 die 45%, so one wafer gives about 20 times as many good small dies as big ones; the learning curve of a new process;
- the fab: TSMC's capital spending, a third to a half of its revenue every year since 2015, $40.9bn in 2025 and
  $52-56bn planned for 2026; $165bn planned in America; about 88% of its capacity used in 2025; revenue per wafer from
  NT$180,000 (2023) to NT$254,000 (2025, about $8,100); gross margin from 54.4% to 59.9%, and 66.4% in the third
  quarter of 2026; 90,557 employees at the end of 2025 (76,478 two years before), about $1.3 million of revenue each;
- fabless and foundry: the split; TSMC's largest customer 19% of revenue, the second 17%, the ten largest 78%; Nvidia,
  which owns no fab, from $6.9bn of revenue in fiscal 2017 to $215.9bn in fiscal 2026, $193.7bn of it for data centres;
  Intel's foundry, which lost $7.1bn, $13.3bn and $10.3bn in 2023-2025 with $307m of outside revenue in 2025, and the US
  government's 275 million Intel shares;
- the tools: ASML, €32.7bn of sales in 2025, 327 lithography systems, 48 of them EUV, 'the world's only manufacturer of
  EUV lithography systems', with one supplier of optics; Applied Materials, Lam Research, KLA, Synopsys and Cadence, each
  keeping at least 19% of revenue as profit; and the money followed upstream: Nvidia's $62bn cost of making $216bn
  of chips and systems (wafers, memory, packaging, assembly), TSMC's $121bn of revenue and $41bn of spending on tools;
- an intermission: America's output of semiconductors about 5,089 times larger in 2025 than in 1972, and their producer
  price down about 98% after inflation since 1967; transistors per microprocessor from 2,308 (1971) to 58 billion (2021),
  doubling about every 2.0 years;
- memory: world memory sales from $129.8bn (2022) to $92.3bn (2023) and up to $230.0bn (2025), forecast at $803.9bn for
  2026; Micron from an operating loss of $2.3bn in a quarter of 2023 to $43.8bn of operating profit on $54.2bn of
  revenue in the quarter to September 2026; Micron's spending on fabs and tools through the cycle, $7.7bn (49% of
  revenue) in the bust of fiscal 2023 and $30.7bn in fiscal 2026;
- the trailing edge: General Motors on the 2021 shortage; 19% of TSMC's wafer revenue from 28 nm and older; the net
  margins of Texas Instruments, Analog Devices, NXP, Microchip, onsemi and STMicroelectronics, 2015-2025, from Texas
  Instruments' 44% in 2022 to three of the six keeping under 3% in 2025;
- where the chips go: $795.6bn of chips in 2025 by product (logic $300bn, memory $230bn, analog $87bn, micro $85bn, the
  rest $95bn); TSMC's revenue by platform, high-performance computing from 43% (2023) to 58% (2025) and 68% in the third
  quarter of 2026; of WSTS's forecast rise of $716bn in 2026, $574bn (80%) is memory;
- geography and the state: TSMC's sixteen fabs, eleven in Taiwan including the three making its 2 and 3 nm chips, and
  Arizona's Fab 21 at 5 nm; CHIPS Act grants of up to $6.6bn and €5bn of German state aid; America's export rules from
  October 2022 to November 2026; WSTS's sales by region, the Americas forecast to rise 112% in 2026;
- the landscape, November 2026: the listed chip companies by revenue and five-year margin, and what to watch;
- *Called it?*: Moore's 1965 forecast (right, then revised); WSTS's December 2025 forecast of $975bn for 2026, passed by
  September at $1.22 trillion; and this series' call that 2026's sales, as WSTS first reports them, will exceed $1.8
  trillion (65%).

## Build it

```bash
python -m videos.industry.industry15.compute               # every number, printed
EXPLAINER_TTS=silent python tools/build.py industry15 -q l  # the whole part, silent preview
python tools/build.py industry15                           # 1080p30 with narration
python -m videos.industry.labs 15                          # the lab
python -m pytest tests/industry                            # the Register and the Works (test_fab.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p15.py`), a transcribed table
(`explainer/industry/data/tables.py`: TSMC's fabs) or comes from the Filing Room: FRED's industrial production, capacity
utilization and producer prices for semiconductors (`fred_chips.csv`), Our World in Data's transistor counts
(`owid_chips.csv`), the foreign filers' accounts (`sec_foreign.csv`: TSMC, UMC, GlobalFoundries, ASML,
STMicroelectronics), the BLS's CPI (`bls_water.csv`) and the companies' 10-Ks (`sec_annual.csv`, `sec_quarterly.csv`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | A question of scale | Moore, 1965; Hsinchu, 1987; the title |
| 1 | Run it: build a fab or book a foundry | Three volumes; the cost of a good die; the break-even |
| 2 | How a chip is made | The loop of layers; the light; dies on a wafer |
| 3 | The node | What a node's name means; TSMC's revenue by process |
| 4 | Yield | Random defects; big dies against small; the learning curve |
| 5 | The fab | TSMC's spending; utilization; revenue per wafer; its people |
| 6 | Fabless and foundry | The split; TSMC's customers; Nvidia; Intel's foundry |
| 7 | The tools | ASML; the other toolmakers and the design software; the money followed upstream |
| — | Intermission | Fifty years of cheaper chips; Moore's law itself |
| 8 | Memory | Micron's quarters; world memory sales; spending through the cycle |
| 9 | Analog, power and the trailing edge | The car and the shortage; the analog makers' margins |
| 10 | Where the chips go | Sales by product; TSMC's revenue by platform; where 2026's growth comes from |
| 11 | Geography and the state | TSMC's fabs on the map; subsidies; export rules; sales by region |
| 12 | The landscape, November 2026 | The listed chip companies; what to watch |
| 13 | Called it? | Moore's forecast; WSTS's forecast for 2026; this series' call |
| — | The factory of factories | The funnel; the answers; Part 16, electronics |

## What is computed, and from what

`compute.py` reads the Filing Room, the Register and the tables. Run it, the dies, the yield and the learning curve are
the Works' (`explainer/industry/works/fab.py`), with illustrative parameters labelled on screen: gross dies are the
wafer's area over the die's less the edge, pi r^2 / A - pi d / sqrt(2A); yield is exp(-A D). TSMC's revenue per wafer
divides its net revenue by its 12-inch-equivalent wafer shipments; its utilization divides shipments by capacity; its
capital spending share divides capital expenditure by revenue, both in NT$. The intermission's real price divides the
BLS's producer price index for semiconductors by the CPI (annual averages; 2025's CPI from the BLS series, since FRED's
October 2025 value is missing); Moore's doubling time fits a line to the logarithm of Rupp's counts. Net margins are net
income (or profit for the year) over revenue; the landscape averages them over each company's last five fiscal years,
and sizes TSMC by its 20-F's dollar translation and UMC at about NT$32 to the dollar. Micron's quarters are revenue and
operating income for three months, the fourth fiscal quarter being the year less the first three. The quarters needed for
the call add WSTS's first-half sales to SIA's third quarter.

## Problems and solutions

**1.** *A 300 mm wafer carries dies of 150 mm2. How many gross dies fit (use pi r^2 / A - pi d / sqrt(2A))? At 0.2 defects
per cm2, how many are good, and what does a good die cost at $17,000 a wafer? What if the process matures to 0.1?*

*Solution.* Gross: pi x 150^2 / 150 = 471.2, less pi x 300 / sqrt(300) = 54.4: about 417 dies. Yield at 0.2: exp(-1.5 x
0.2) = 0.741, so about 309 good dies and $17,000 / 309 = $55 each. At 0.1: exp(-0.15) = 0.861, about 359 good dies, $47
each. Halving the defect density cuts the cost of a good die by 14% without touching the price of the wafer, which is why
a maker's first months on a new process are its dearest.

**2.** *The Works' fab costs $20bn, written off over five years, plus $1bn a year to run and $2,500 a wafer in materials
and power. It can start 50,000 wafers a month. What does a wafer cost full, and half full? At what loading does it match a
foundry's price of $17,000 a wafer?*

*Solution.* The fixed cost is $4bn + $1bn = $5bn a year. Full, 600,000 wafers: $8,333 + $2,500 = $10,833 a wafer. Half
full: $16,667 + $2,500 = $19,167, dearer than the foundry. It matches $17,000 when 5e9 / (12v) = 14,500, v = 28,700
wafers a month, 57% full. The film's break-even is higher, about 32,000, because a new fab also yields fewer good dies
while it learns its process.

**3.** *A foundry spends $40bn a year on tools written off over five years. Once it has spent that for five years, what
is its yearly depreciation? With revenue of $120bn and other costs of $30bn, what is its operating margin? If revenue falls
20% and the other costs stay, what then?*

*Solution.* Five vintages of $40bn, each written off at $8bn a year: $40bn a year. The margin is (120 - 40 - 30) / 120 =
41.7%. At $96bn of revenue: (96 - 40 - 30) / 96 = 27.1%. A fifth less revenue takes away two-fifths of the profit,
because the machines cost the same whether the wafers come or not: the fab's cost is mostly fixed.

**4.** *A memory maker sells 20% more bits each year. Its fixed costs are $60bn a year and its variable costs 20% of
revenue; revenue is $100bn. Next year the price per bit falls 30%; the year after it rises 50%. What happens to revenue
and to profit?*

*Solution.* Year 0: profit 100 - 60 - 20 = $20bn. Year 1: revenue 100 x 1.2 x 0.7 = $84bn, profit 84 - 60 - 16.8 =
$7.2bn, a 64% fall on a 16% fall in revenue. Year 2: revenue 84 x 1.2 x 1.5 = $151.2bn, profit 151.2 - 60 - 30.2 = $61bn,
more than eight times year 1's. Prices that swing by a third, on top of large fixed costs, make memory's profits swing by
multiples, as Micron's did from 2023 to 2026.

**5.** *Rupp's data put 2,308 transistors on a microprocessor in 1971 and 58.2 billion in 2021. If they had doubled
every two years, how many would there have been in 2021? What doubling time do the two numbers imply?*

*Solution.* Fifty years is 25 doublings: 2,308 x 2^25 = 77.4 billion, a third more than the actual count. The ratio is
58.2e9 / 2,308 = 2.52e7, or log2(2.52e7) = 24.6 doublings in fifty years: one every 2.03 years. Moore's revised law held
to within a few weeks a doubling for half a century.

## Glossary

- **Wafer:** a polished disc of silicon, 300 mm across for most new fabs, on which hundreds of chips are made at once.
- **Die:** one chip's rectangle on the wafer, cut out and packaged.
- **Yield:** the share of dies that work; defects falling at random kill big dies more often than small ones.
- **Defect density:** killer defects per square centimetre; it falls as a process matures.
- **Node:** a generation of manufacturing process, named in nanometres that no longer measure any feature.
- **Lithography:** printing a layer's pattern onto the wafer with light through a mask; EUV uses 13.5 nm light.
- **Fab:** a chip factory, a cleanroom full of machines.
- **Foundry:** a company that makes chips designed by others; **fabless:** a designer that owns no fab; **integrated
  device maker (IDM):** a company that designs and makes its own.
- **DRAM and NAND flash:** the two main kinds of memory, for working data and for storage.
- **Trailing edge:** older, written-off processes making chips that do not need the smallest features: analog, power,
  microcontrollers.
- **WSTS:** World Semiconductor Trade Statistics, the industry's own count of chip sales, by product and region.

## Lab and interactive

- `python -m videos.industry.labs 15`: Moore's forecast; Run it; dies and yield; TSMC's utilization, revenue per wafer
  and spending; ASML and the toolmakers; fifty years of cheaper chips; memory; the trailing edge; sales by product and
  platform; TSMC's fabs and sales by region; WSTS's forecasts and this series' call.
- The interactive (course site): build a fab or book a foundry. Set the volume, the fab's cost, the foundry's price and
  the chip's size, and see the profit of each, the cost of a good chip and the volume at which owning first pays.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p15.py`), the tables (`explainer/industry/data/tables.py`)
or the Filing Room (`explainer/industry/data/SOURCES.md`). The main ones:

- G. E. Moore, 'Cramming more components onto integrated circuits', Electronics 38 (8), 19 April 1965; 'Progress in
  Digital Integrated Electronics', IEDM Technical Digest 1975.
- SEC EDGAR: TSMC's Form 20-F 2025 and Forms 6-K of 4 March 2025 and 15 October 2026 (with the third quarter 2026
  presentation); ASML's Form 20-F 2025; the Forms 10-K of Nvidia, Intel, Micron, Texas Instruments, Analog Devices, NXP,
  Microchip, onsemi, Applied Materials, Lam Research, KLA, Synopsys, Cadence, Broadcom, Qualcomm, AMD, Marvell and Amkor;
  the Forms 20-F of UMC, GlobalFoundries and STMicroelectronics; General Motors' Form 10-K 2021.
- World Semiconductor Trade Statistics: forecasts of Fall 2023, Autumn 2025 and Spring 2026; releases for Q4 2025 and Q2
  2026. Semiconductor Industry Association, press release of 3 November 2026.
- Federal Register: Bureau of Industry and Security rules 87 FR 62186 (2022), 88 FR 73458 (2023), 89 FR 96790 (2024),
  90 FR 4544 (2025), 91 FR 1684 and 91 FR 74970 (2026).
- Federal Reserve, industrial production and capacity utilization (G.17); Bureau of Labor Statistics, producer and
  consumer price indexes (via FRED and the BLS).
- Karl Rupp, Microprocessor Trend Data, via Our World in Data.
