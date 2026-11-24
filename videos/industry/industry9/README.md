# Industry, Built: Part 9, Mining and Metals

Part 9 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second of Act II, *Out of the Ground*. It asks: why is a mine worth a fortune in
one decade and nothing in the next? It answers with the account of the geologist who found Escondida; BHP's results
for the year to June 2025; Freeport-McMoRan's Form 10-K for 2025; the US Geological Survey's Mineral Commodity
Summaries 2026 and its historical prices since 1900 (Data Series 140); the IMF's monthly metal prices; Vale's
announcement of 1 April 2010; the 20-F and 10-K accounts of BHP, Rio Tinto, Vale, Freeport, Southern Copper, Newmont
and Albemarle; Paul Sabin's history of the Simon-Ehrlich wager; and the Works' model mine. The answer: a mine is
billions spent up front and repaid over decades at prices nobody knows, on rock whose grade only falls. Every miner
takes the exchange's price, so the only thing it controls is its cost. Booms are when mines get built, and the mines
arrive when the boom is over. Over a century, prices swing in long cycles around a level that barely moves, and the
state takes its share throughout.

It opens in the Atacama in March 1981: money for nine holes, five drilled dry, and the sixth finding Escondida, about
300 million tonnes of ore at 1.3-1.5% copper, for a search that had cost $3m. In the year to June 2025 Escondida
produced 1,305 thousand tonnes of copper and $8.6bn of operating profit, but its feed grade falls from 1.02% to about
0.85%. From there it covers:

- Run it: the Works' model deposit (600 Mt at 0.5%, $3bn and three years to build, break-even $3.61 a pound) at
  $4.50 copper. Build now, wait a year or sell, across 400 price paths: building is worth $859m on average but loses in
  32% of futures, so a one-mine company should sell;
- from rock to metal: blast, haul, crush, grind, float, smelt and refine; 353 tonnes of rock moved for a tonne of
  copper at 1%; and leaching, at Freeport's 0.21% ore in Arizona and New Mexico;
- grade is destiny: rock per tonne from 3% to 0.21%; the same mine's cost and break-even at other grades; Escondida's
  grade, output and cost on BHP's guidance (1,150-1,250 kt this year; 900-1,000 kt a year to 2031);
- the mine plan and the option to wait: pushbacks that take the richest rock first, and the value of keeping the right
  to build ($609m at break-even, where building now is worth nothing). Build only when the price is about 35% above
  break-even;
- the cost curve: Grasberg (-$0.55 a pound, net of gold), Escondida ($1.19), Freeport's South American ($2.43) and US
  ($3.05) mines against 2025's $4.51 and September 2026's $6.56; Escondida's block narrowing and rising;
- where metal comes from: Chile 5.3 million tonnes mined, China 14 million refined (8% of the world's mining, 48% of its
  refining); 980 million tonnes of reserves, about 43 years, and why that is not a countdown;
- iron ore: Australia's 980 and Brazil's 420 of 2.6 billion tonnes; one negotiated price a year until Vale's switch in
  April 2010; $14 a tonne in 2003, $216 in June 2021 and about $100 now, quoted for delivery in China;
- how metals are priced: the exchange price, smelters' charges and buyers' premiums; copper's nominal record in
  September 2026 ($14,473 a tonne) against its real peak of February 2011; and 2025's split between New York ($4.80) and
  London ($4.51), as US imports of refined copper nearly doubled;
- an intermission: a century of copper in 1998 dollars, from the First World War to China's boom;
- the supercycle: copper x5.7 and iron ore x13.2 from 2002 to 2011; the bust (Vale -$12.1bn in 2015) and the boom
  of 2021-22 in the three iron ore giants' accounts;
- the state takes its share: 36% of the model mine's profit from a 4% royalty and a 27% tax; Indonesia's 51.24% of
  Grasberg and the mud rush of 8 September 2025; Congo's cobalt ban and quotas (96,600 t a year against 230,000 t
  mined); Indonesia's nickel and Australia's mines shut;
- critical minerals: the largest producer's share of mining (cobalt 73%, rare earths 69%, nickel 67%); copper on the US
  list since 7 November 2025; lithium from $11,700 to $63,700 to $9,000 a tonne, and Albemarle's losses; China's
  rare-earth export controls of April and October 2025;
- gold: 3,300 tonnes mined in 2025, a cube 5.5 metres on a side worth about $350bn at $3,300 an ounce; where it goes
  (central banks 21%); Newmont's record $7.1bn;
- the landscape, November 2026: the miners that file with the SEC by revenue and margin, those that do not, and what
  to watch;
- *Called it?*: Simon and Ehrlich's wager (the basket fell to about $625 of $1,000; the cheque was $576.07), re-run for
  all 110 ten-year windows from 1900 (Ehrlich would have won 61% of them); and this series' call that Escondida will
  produce less than 1,100 kt in BHP's year to June 2027 (75%).

## Build it

```bash
python -m videos.industry.industry9.compute               # every number, printed
EXPLAINER_TTS=silent python tools/build.py industry9 -q l  # the whole part, silent preview
python tools/build.py industry9                           # 1080p30 with narration
python -m videos.industry.labs 9                          # the lab
python -m pytest tests/industry                           # the Register and the Works (tests/industry/test_mine.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p09.py`) or comes from the Filing Room: the USGS's
historical unit values (`usgs_ds140.csv`), the IMF's monthly metal prices via FRED (`fred_metals.csv`), the CPI
(`fred_energy.csv`), the miners' 20-F accounts (`sec_ifrs.csv`) and 10-K accounts (`sec_annual.csv`). The world map
is Natural Earth's (`world_land.json`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The sixth hole | Escondida's discovery, 1981; the mine today and its falling grade; the title |
| 1 | Run it: build, wait or sell | The model deposit; a mine's cash; 400 price paths |
| 2 | From rock to metal | Pit to cathode; the tonnage funnel; leaching |
| 3 | Grade is destiny | 400 tonnes of ore; rock per tonne; cost against grade; Escondida |
| 4 | The mine plan and the option to wait | Pushbacks; the value of waiting against the price |
| 5 | The cost curve | Four real operations against the price; Escondida's block moving |
| 6 | Where metal comes from | Mining and refining by country; reserves |
| 7 | Iron ore: three companies, one customer | Producers; the end of the benchmark; the price since 1992 |
| 8 | How metals are priced | The exchange price; the nominal and real record; the 2025 tariff gap |
| — | Intermission | A century of copper; the story so far |
| 9 | The supercycle | Prices from 2002; the iron ore giants' profits |
| 10 | The state takes its share | The model mine's cash; Grasberg; Congo, Indonesia and Australia |
| 11 | Critical minerals | Concentration; lithium's boom and bust; rare earths |
| 12 | Gold | The year's gold as a cube; where it goes; Newmont |
| 13 | The landscape, November 2026 | The miners by revenue and margin; what to watch |
| 14 | Called it? | Simon and Ehrlich, every decade since 1900; this series' call on Escondida |
| — | The ore, and what comes next | The answers; Part 10, farming and food |

## What is computed, and from what

`compute.py` reads the IMF's monthly copper, iron ore, nickel, aluminium, zinc and tin prices since 1992 and deflates
them by the CPI to October 2026 dollars; the iron ore series' distinct prices a year date the end of the benchmark. The
supercycle multiples divide 2011's yearly averages by 2002's. The Simon-Ehrlich basket holds $200 of each metal at the
USGS's 1980 unit values in 1998 dollars and revalues it at 1990's; the same basket is revalued for every ten-year
window with all five prices from 1900 (the Works' `mine.bet_windows`). The cost curve sorts the four operations by
their published net cash costs and widths of copper produced (Freeport's million pounds converted at 2,204.62 a tonne).
The model deposit, its cash flows, break-even, price paths (mean-reverting towards $3.80 with 25% volatility),
option to wait, grade curves and the state's share are the Works' `mine.py`, labelled as models on screen.

## Problems and solutions

**1.** *Ore holds 0.6% copper, the mill recovers 90% of it, and the mine strips three tonnes of waste for every tonne of
ore. How many tonnes of rock does it move for one tonne of copper?*

*Solution.* Each tonne of ore yields 0.006 × 0.9 = 0.0054 tonnes of copper, so a tonne of copper needs 1 / 0.0054 = 185
tonnes of ore. With three tonnes of waste for each, the mine moves 4 × 185 = 741 tonnes of rock.

**2.** *A mill grinds 40 million tonnes of ore a year and recovers 87% of the copper. Its site costs are fixed at $500m a
year. The grade falls from 1.0% to 0.8%. What happens to its output and to its site cost per pound?*

*Solution.* At 1.0%: 40m × 0.01 × 0.87 = 348,000 tonnes, or 767m pounds, so $500m costs 65 cents a pound. At 0.8%:
278,400 tonnes (−20%), 614m pounds, and 81 cents a pound (+25%). A fall in grade cuts output and raises the cost of
every pound together.

**3.** *Building a mine now is worth −$100m at today's price. In a year the price will be either high, making the mine
worth $1,200m, or low, making it worth −$1,400m, each with probability one half. At 8% a year, what is the right to wait a
year worth, and should the company build now?*

*Solution.* Waiting, it builds only if the price is high: 0.5 × 1,200 / 1.08 = $556m. Building now is worth −$100m
(the average of the two outcomes, about what today's price implies). Waiting is worth $656m more, so it should wait.
Building destroys the choice, which here is worth more than the mine.

**4.** *A basket holds $200 each of five metals. After inflation, their prices change by −12%, −24%, −10%, −71% and −71%.
What is the basket worth, and who wins a bet that it will be worth more than $1,000?*

*Solution.* 200 × (0.88 + 0.76 + 0.90 + 0.29 + 0.29) = 200 × 3.12 = $624. It lost $376, so the bettor on scarcity loses.
These are the USGS's yearly values for 1980-1990; on the exact dates of the wager, Ehrlich's cheque was $576.07.

**5.** *A mine sells $10bn of copper in a year. Its operating costs are $5bn and its depreciation $1bn. The state takes a 5%
royalty on revenue and a 30% income tax on profit after the royalty and depreciation. What share of the $5bn cash margin
does the state take?*

*Solution.* Royalty: $0.5bn. Taxable profit: 10 − 5 − 0.5 − 1 = $3.5bn, so tax is $1.05bn. The state takes $1.55bn,
31% of the cash margin. In a bad year with no taxable profit, it still takes the royalty.

## Glossary

- **Grade:** the share of a metal in ore; copper ores today mostly hold well under 1%.
- **Strip ratio:** tonnes of waste rock removed for each tonne of ore.
- **Recovery:** the share of the metal in the ore that the plant actually captures.
- **Flotation:** separating mineral grains from ground rock by making them cling to air bubbles.
- **Concentrate:** the product of flotation, about a quarter to a third copper, sold to smelters.
- **Cathode:** refined copper plate, 99.99% pure, the form in which copper is traded.
- **Leaching (SX-EW):** dissolving copper from heaped ore with acid and plating it out by electricity, without a smelter.
- **Net cash cost (C1):** the cash cost of a pound of copper, less the value of by-products such as gold.
- **Reserves:** metal known and worth mining at today's prices and methods.
- **Block caving:** underground mining by undercutting a column of ore so that it collapses under its own weight.
- **Benchmark pricing:** a price negotiated once a year between the biggest sellers and buyers.
- **Royalty:** the state's share of revenue for the right to extract its minerals.
- **Critical mineral:** one that is essential, hard to replace and produced in few places.

## Lab and interactive

- `python -m videos.industry.labs 9`: Escondida's discovery and decline; rock per tonne by grade; the model mine's
  costs, break-even, price paths and the option to wait; the state's share; the cost curve; mining against
  refining; the end of iron ore's benchmark; the supercycle and the bust; lithium and gold; the wager over every
  decade; this series' call.
- The interactive (course site): a copper mine. Set the grade, the strip ratio, the recovery and the copper price, and
  see the rock a tonne of copper takes, the cost of a pound, the break-even price and what the mine is worth today.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p09.py`) or the Filing Room
(`explainer/industry/data/SOURCES.md`). The main ones:

- Francisco Ortiz, 'El descubrimiento del yacimiento Escondida', CESCO, December 2024.
- BHP, results for the year ended 30 June 2025 (ASX release, 19 August 2025).
- Freeport-McMoRan Inc., Form 10-K for 2025.
- US Geological Survey, Mineral Commodity Summaries 2026 (copper, iron ore, gold, lithium, cobalt, nickel, rare
  earths) and Data Series 140, historical statistics for mineral and material commodities.
- IMF primary commodity prices via FRED (PCOPPUSDM, PIORECRUSDM, PNICKUSDM, PALUMUSDM, PZINCUSDM, PTINUSDM); the
  consumer price index (BLS).
- Vale S.A., 'Vale on iron ore pricing', 1 April 2010.
- SEC EDGAR: BHP, Rio Tinto and Vale, Forms 20-F; Freeport-McMoRan, Southern Copper, Newmont and Albemarle, Forms
  10-K (company facts).
- Paul Sabin, *The Bet: Paul Ehrlich, Julian Simon, and Our Gamble over Earth's Future* (Yale University Press, 2013).
- Avinash Dixit and Robert Pindyck, *Investment under Uncertainty* (Princeton University Press, 1994).
- Natural Earth, 1:110m land (public domain), for the maps.
