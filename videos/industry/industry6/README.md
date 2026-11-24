# Industry, Built: Part 6, The Cycle

Part 6 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the sixth of Act I, *Reading an Industry*. It asks: why do industries keep building
too much at the top? It answers with Micron's accounts, quarter by quarter since 2009; Maersk's results from its
annual reports; UNCTAD's count of ships on order; the NBER's hog prices and slaughter, 1880-1940; the Census Bureau's
housing starts; retail sales and factory orders; West Texas crude and Exxon Mobil's spending; Intel's 2021 plan; and
the Works' model of a shipping market. The answer: when capacity takes years to build and firms order it by looking at
today's price, it arrives together and prices swing, even when demand grows smoothly; the longer the wait, the bigger
the swing; the swings grow up a supply chain and in the makers of machines; fixed costs and debt turn a fall in sales
into a collapse in profit; and the low-cost producer with little debt is the one still standing at the bottom.

It opens three years apart: Micron lost $5.7bn on its operations on $15.5bn of sales in fiscal 2023, and made $99.3bn
on $133.2bn in fiscal 2026; Maersk's operating profit went from $1.7bn in 2019 to $30.9bn in 2022 and $3.9bn in 2023.
From there it covers:

- Run it: a shipowner offered a ship in three years at a record rate, then a market of such owners in the Works'
  model, making a cycle out of demand that grows 3% every year;
- the cobweb (Ezekiel, 1938), drawn with hogs: converging when farmers respond less than buyers, exploding when they
  respond more, and a predicted cycle of two years;
- sixty years of hogs (NBER, Chicago prices and US slaughter, 1880-1940): a same-month correlation of -0.61, a high
  price followed by more hogs about two and a half years later, and a swing of about 3.6 years, not two (Coase and
  Fowler's objection, 1935);
- the capital cycle as a loop: high returns, orders, the wait, capacity arrives, losses, exit;
- why the wait makes it worse: the same market with lead times of one to four years swings by 3%, 11%, 81% and 130%;
  and why knowing about the cycle does not stop it (lumpy plants, hidden orders, lenders at the top, career risk);
- ships: the world's orderbook at 52% of the fleet in 2009 (bulk carriers 78%), 19% in 2014, 11% in 2023 and 15% in
  early 2025, with container ships at a quarter of their fleet and 41% of 2024's deliveries, and LNG carriers at
  half; Maersk, 2019-2025;
- memory chips: Micron's quarterly sales fell 21%, 37%, 43% and 57% after its peaks of 2010, 2014, 2018 and 2022;
  $54.2bn in the quarter to September 2026 at an 81% operating margin; spending 3.2 times depreciation;
- houses: starts at a pace of 2.27 million a year in January 2006, down 79% by April 2009; completions kept coming
  for a year; unsold new homes peaked at 12.2 months' supply in January 2009; D.R. Horton, a builder that came
  through the bust ($3.7bn of sales and a loss in fiscal 2009, $36.8bn and a $4.8bn profit in fiscal 2024);
- an intermission: four cycles, a century apart;
- the bullwhip (Lee, Padmanabhan and Whang, 1997): a chain of three tiers, and America's factory orders 1.6 times
  as volatile as its retail sales, 1993-2026; its cures; and the 2021 car-chip shortage (car output to a fifth of
  February's in April 2020, down a sixth again in 2021; buyers' median chip stock from 40 days to under 5; used-car
  prices up 53%);
- the accelerator (Clark, 1917): a bakery chain's ovens, where bread up 10% doubles the oven maker's orders;
- leverage: a model business, then Micron's fiscal 2023 (sales -49%, an operating loss) and Maersk's 2023 (sales
  -37%, operating profit -87%);
- oil: West Texas crude from about $100 to $30 between 2014 and 2016 and $17 in April 2020, US output from 5.5 to 9.4 million barrels a
  day (2010-2015), Exxon Mobil's spending from $34bn (2012) to $12bn (2021) and back to $28bn (2025);
- reading where you are: ships on order, spending against wear, unsold stock (Micron: 6.5 months of sales in 2023,
  0.9 in 2026) and houses for sale;
- a boom you can watch: Microsoft, Alphabet, Amazon and Meta spent $23bn on buildings and equipment in 2015 and
  $357bn in 2025, 2.8 times their depreciation and 64% of their operating cash;
- who wins a cycle: the low-cost producer on the supply curve, the buyer at the bottom, the company that owes
  little, the supplier paid in advance;
- *Called it?*: Intel's 2021 plan for two Arizona fabs against its loss of $11.7bn in 2024; and this series' call that
  Micron will report a quarter at least 25% below its best before the end of 2028 (55%).

## Build it

```bash
python -m videos.industry.industry6.compute               # every number, printed (instant)
EXPLAINER_TTS=silent python tools/build.py industry6 -q l  # the whole part, silent preview
python tools/build.py industry6                           # 1080p30 with narration
python -m videos.industry.labs 6                          # the lab
python -m pytest tests/industry                           # the Register and the Works (tests/industry/test_cycle.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p06.py`) or comes from the Filing Room:
Micron's, Intel's and Exxon's filings (`sec_annual.csv`, `sec_quarterly.csv`), Maersk's (`esef_maersk.csv`) and FRED's
monthly series (`fred_cycle.csv`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Three years apart | Micron in fiscal 2023 and 2026; Maersk, 2019-2025; the title |
| 1 | Run it: the shipowner | The choice at a record rate; a market of owners makes a cycle |
| 2 | The cobweb | Ezekiel's model, converging and exploding; the two-year prediction |
| 3 | Sixty years of hogs | NBER prices and slaughter, 1880-1940; correlations and the cycle's length |
| 4 | The capital cycle | The loop, and where it turns |
| 5 | Why the wait makes it worse | Lead times of one to four years; four reasons the cycle survives |
| 6 | Ships | UNCTAD's orderbook; container ships and Maersk |
| 7 | Memory chips | Micron's quarters since 2009; spending against depreciation |
| 8 | Houses | Starts, completions and months' supply, 2000-2026; D.R. Horton through the bust |
| — | Intermission | Four cycles; the story so far |
| 9 | The bullwhip | A chain of tiers; retail sales against factory orders; the cures; cars in 2021 |
| 10 | The accelerator | Ovens and bread: orders follow growth, not level |
| 11 | Leverage | Operating and financial leverage; Micron and Maersk in 2023 |
| 12 | Oil | West Texas crude, US output and Exxon's spending |
| 13 | Reading where you are | Four gauges |
| 14 | A boom you can watch | Microsoft, Alphabet, Amazon and Meta's capital spending against wear and cash |
| 15 | Who wins a cycle | The supply curve in a trough; four other ways to come out ahead |
| 16 | Called it? | Intel's 2021 plan; this series' call on Micron |
| — | The cycle, and what comes next | The answers; Part 7, sizing a market |

## What is computed, and from what

`compute.py` reads Micron's and Intel's quarterly revenue from their Forms 10-Q and 10-K (a fiscal fourth quarter is
the year less its first three) and finds every quarter higher than the four on each side, with the lowest quarter in
the eight that followed. The hog analysis takes the NBER's monthly Chicago price and US slaughter, 1880-1940, averages
each over twelve months, takes logs and subtracts a 61-month moving average, then computes correlations at lags of
six months and the spectral peak of each series. The bullwhip's national figures are the standard deviations of the
monthly log changes of retail sales (excluding food services) and manufacturers' new orders, 1993-2026. Capital
spending against depreciation and inventory in months of sales are from each company's annual filings. The fleet,
cobweb, bullwhip chain, accelerator, leverage and supply-curve examples are models (the Works' `cycle.py`), labelled
as such on screen.

## Problems and solutions

**1.** *Demand is p = 10 - q and farmers plan q = 0.8 p from last year's price. Starting at p = 8, trace two years.
Does the cobweb converge?*

*Solution.* Year 1: q = 6.4, so p = 3.6. Year 2: q = 2.88, so p = 7.12. The equilibrium is p = 10 / 1.8 = 5.56. The
gaps are 2.44, -1.96, 1.56: each is 0.8 times the last in size, with the sign flipping, so it converges. It converges
because b × d = 1 × 0.8 < 1.

**2.** *A business has sales of $200m, variable costs of 60% of sales and fixed costs of $50m. Sales fall 10%. By how
much does operating profit fall? It also pays $10m of interest; by how much does profit after interest fall?*

*Solution.* Before: 200 × 0.4 - 50 = $30m. After: 180 × 0.4 - 50 = $22m, down 27%. After interest: 20 to 12, down
40%. A 10% fall in sales becomes a 27% fall in operating profit and a 40% fall after interest.

**3.** *A chain needs one oven per thousand loaves a day and replaces a tenth of its ovens each year. It sells 200,000
loaves a day. What does it order if sales are flat, if they grow 5%, and if they fall 5%?*

*Solution.* It has 200 ovens and replaces 20 a year. Flat: 20. Up 5% (210,000): 20 + 10 = 30, up 50%. Down 5%:
20 - 10 = 10, down 50%. A 5% swing in bread becomes a 50% swing in ovens.

**4.** *The world fleet is 100 ships and 15 are on order. Ships take three years to build and demand grows 3% a year.
If 2 ships a year are scrapped, how much does the fleet grow when the ships on order arrive, compared with demand?*

*Solution.* Over three years demand grows about 9.3%. The fleet grows by 15 - 6 = 9 ships: about 9%. The orders match
demand only if nothing more is ordered in the meantime; every extra ship ordered at today's high rate is surplus
when it arrives.

**5.** *A company spends $30m a year on new plant against depreciation of $10m. What does the ratio of 3 tell you,
and why is it a warning sign in a cyclical industry?*

*Solution.* It is adding capacity three times as fast as its plant is wearing out: growing it fast, at today's high
prices. In a cyclical industry, spending far above depreciation across the industry is how a boom builds the surplus
that ends it.

## Glossary

- **Cycle:** a rise and fall in prices and profits that repeats, driven by the industry's own investment.
- **Lead time:** the time from ordering capacity to using it.
- **Cobweb:** a model in which this period's output is planned from last period's price.
- **Capital cycle:** high returns draw investment, which arrives as surplus capacity, which brings losses and exit.
- **Orderbook:** capacity ordered but not yet delivered; in shipping, as a share of the fleet.
- **Bullwhip effect:** orders that swing more than sales, more at each step up a supply chain.
- **Accelerator:** demand for machines follows the growth of demand for what they make, not its level.
- **Operating leverage:** the change in operating profit for a change in sales, larger when more costs are fixed.
- **Depreciation:** the cost of plant wearing out, spread over its life.

## Lab and interactive

- `python -m videos.industry.labs 6`: the swing of the freight rate for lead times of one to four years; the cobweb
  converging and exploding; the hog cycle's correlations and length; the bullwhip in a model chain and in America's
  statistics; Micron's peaks and falls; spending against depreciation.
- The interactive (course site): the shipowners. Set the time from order to delivery, how eagerly owners order,
  the growth of demand and how far the rate moves when ships are short, and watch the freight rate and the ships on
  order over forty years.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p06.py`) or the Filing Room
(`explainer/industry/data/SOURCES.md`). The main ones:

- Micron Technology, Intel and Exxon Mobil: Forms 10-K and 10-Q (SEC company facts).
- A.P. Moller-Maersk: annual reports 2020-2025 (ESEF filings, via filings.xbrl.org).
- UNCTAD, Review of Maritime Transport 2024 and 2025, chapter II (from Clarksons Research).
- NBER Macrohistory Database via FRED: wholesale price of hogs and live hog receipts at Chicago; hogs slaughtered.
- US Census Bureau via FRED: housing starts, completions, months' supply; retail sales; manufacturers' new orders.
- US Energy Information Administration: West Texas Intermediate (via FRED) and US field production of crude oil.
- Intel, press release 'Intel CEO Pat Gelsinger Announces IDM 2.0 Strategy', 23 March 2021.
- M. Ezekiel, 'The Cobweb Theorem', *Quarterly Journal of Economics* 52(2), 1938.
- R. H. Coase and R. F. Fowler, 'Bacon Production and the Pig-Cycle in Great Britain', *Economica* 2, 1935.
- J. M. Clark, 'Business Acceleration and the Law of Demand', *Journal of Political Economy* 25(3), 1917.
- H. L. Lee, V. Padmanabhan and S. Whang, 'The Bullwhip Effect in Supply Chains', *Sloan Management Review*, 1997.
- *Called it?*: the series' own call is in `explainer/industry/calls.py`.
