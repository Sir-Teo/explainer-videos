# Industry, Built: Part 13, Electricity

Part 13 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the sixth of Act II, *Out of the Ground*. It asks: how is a product that cannot be stored
sold every second, and who pays for the wires? It answers with Samuel Insull's own address of 1910; the EIA's Hourly
Electric Grid Monitor (Form EIA-930), Electric Power Annual, Monthly Energy Review, Annual Energy Outlooks (2005, 2021,
2026 assumptions) and Today in Energy; the FERC-NERC staff report on the February 2021 cold weather outages; the
Independent Market Monitor's State of the Market reports for ERCOT; the 10-Ks of Duke Energy, Vistra and fifteen other
power companies; the National Audit Office on Britain's energy supplier market; the Department of Energy on Lawrence
Berkeley National Laboratory's data centre report; Ember's data via Our World in Data; and the Works' power system. The
answer: electricity is made the instant it is used, so everything is built for the busiest hour and paid for by the
average, the ratio Insull called load factor; the cheapest plants run first and the last one needed sets the price, which
is why power follows gas; the wires are a monopoly whose return a commission sets; markets pay for scarcity, which in a
storm can mean the cap and the dark; and wind, sun, batteries and data centres are now remaking both the day and the demand.

It opens in Boston on 25 February 1910, where Insull described a Chicago block of 193 apartments and 189 customers using
33,000 kWh a year: their own peaks added up to 68.5 kW, a load factor of 5.5% ("only a question of time when you will be
in the hands of a receiver"), but the block's combined peak was 20 kW, 19%. From there it covers:

- Run it: a 500 MW gas plant through a week with a cold snap, selling at spot or forward at $40, running or frozen: about
  +$213m, −$6m, +$4m and −$214m. Vistra's $2.2 billion pre-tax hit from Winter Storm Uri, buying power "at or near the
  price cap";
- a product that cannot be stored: frequency, and the nine minutes ERCOT had on 15 February 2021; ERCOT's peak day (83.6
  GW, 18 August 2025) and a mild day; the 2025 load duration curve, a 67% load factor, and the top tenth of the peak needed
  in 511 hours;
- fixed cost against running cost: EIA's costs for a peaker, a combined cycle, nuclear, wind and solar; the screening
  curve (a new combined cycle at about $40 a MWh, nuclear about $109; nuclear wins only above about $15 gas); capacity
  factors in 2025 (nuclear 91%, combined cycle 59%, coal 49%, wind 34%, solar 24%, peakers 14%);
- the merit order: ERCOT's peak day by source; the Works' stack and price; ERCOT's average price against gas, 2014-2021,
  about $5.8 a MWh for each $1 on gas ("natural gas units are generally on the margin");
- the regulated utility: a kWh in 2020, 5.83 cents of generation, 1.35 of transmission and 3.25 of distribution; the
  Works' revenue requirement; Duke Energy's rate cases (approved returns 9.5%-10.3%; 10.95% asked in North Carolina);
- February 2021: ERCOT's forecast against the load it served, hour by hour; gas down by about 29% and wind to almost
  nothing between Sunday and Monday evening; 1,045 units failed (freezing 44%, fuel 31%); 4.5 million people without
  power, at least 210 deaths, 20,000 MW shed; $9,000 held until 19 February; $59bn of electricity in a week;
- an intermission: US sales since 1950 (9% a year in the 1950s, flat 2007-2021) and the real price of a kWh since 1979;
- wind and sun: California's net load on April days of 2019 and 2026; CAISO's 25 GW of solar, 16 GW of batteries and 29
  GW of gas; why more solar earns less (the Works: $46 to $12 a MWh);
- storing the sun: California's storage charging at noon (about 7 GW) and discharging at night (up to 9 GW) on 15 April
  2026; a battery's arithmetic ($6.6m a year of trading against $20.9m of fixed cost; about 45 bad evenings to break
  even); 23 GW of pumped hydro;
- the retailer's squeeze: Britain's suppliers from 12 (2010) to 70 (2018) to 23 (2022); a supplier with a fixed price
  through 2021's gas prices; 29 failures, Bulb's 1.6 million customers, about £94 on every bill;
- around the world: China's generation up nearly eight-fold since 2000, more than America and the EU together; per
  person; coal against wind and solar by country;
- the new load: US sales growth year by year, 2026 up 2.0% to August; data centres from 58 TWh (2014) to 176 (2023) and
  325-580 projected for 2028; six utilities' capital spending from $39bn (2018) to $69bn (2025);
- the landscape, November 2026: the listed utilities, generators and GE Vernova by size and margin, and what to watch;
- *Called it?*: the EIA's 2005 outlook (5,467 billion kWh in 2025; actual 4,195, 30% lower) and this series' call that
  America's 2027 sales will be more than 1.5% above 2026's (65%).

## Build it

```bash
python -m videos.industry.industry13.compute               # every number, printed
EXPLAINER_TTS=silent python tools/build.py industry13 -q l  # the whole part, silent preview
python tools/build.py industry13                           # 1080p30 with narration
python -m videos.industry.labs 13                          # the lab
python -m pytest tests/industry                            # the Register and the Works (test_power.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p13.py`; the plant costs are Part 4's rows from EIA's
AEO2026 assumptions) or comes from the Filing Room: the EIA-930 extract (`eia_930.csv`), the Monthly Energy Review
(`eia_mer.csv`), the Electric Power Annual (`eia_power.csv`), FRED (`fred_power.csv`), Our World in Data (`owid_elec.csv`)
and the companies' 10-Ks (`sec_annual.csv`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | A question of load | Insull's block, 1910; diversity; the load factor; the title |
| 1 | Run it: a gas plant in a cold snap | Spot or forward, running or frozen; Vistra |
| 2 | A product that cannot be stored | Frequency; ERCOT's days; the load duration curve |
| 3 | Fixed cost against running cost | EIA's costs; the screening curve; capacity factors |
| 4 | The merit order | A day by source; the stack and the price; price against gas |
| 5 | The regulated utility | The kWh in three parts; the revenue requirement; Duke's rate cases |
| 6 | February 2021 | Forecast and served load; the fleet; why plants failed; the cost and the price |
| — | Intermission | US sales since 1950; the real price of a kWh; the story so far |
| 7 | Wind and sun | California's duck; CAISO's capacity; more solar earns less |
| 8 | Storing the sun | California's storage on 15 April 2026; a battery's arithmetic |
| 9 | The retailer's squeeze | Britain's suppliers; a fixed price through 2021; the failures |
| 10 | Around the world | Generation since 2000; per person; coal and wind and sun |
| 11 | The new load | Growth since 2000; data centres; utilities' capital spending |
| 12 | The landscape, November 2026 | The listed companies; what to watch |
| 13 | Called it? | The EIA's 2005 outlook; this series' call |
| — | Power, priced | The answers; Part 14, water and waste |

## What is computed, and from what

`compute.py` reads the Filing Room and the Register. ERCOT's load factor, peak and quiet days, and the hours above 90%
and 95% of the peak use the EIA-930 demand for 2025's 8,736 complete hours. The screening curve uses EIA's AEO2026
overnight costs and fixed and variable O&M (Part 4's rows), 7% capital over 30 years (40 for nuclear), the EIA's 2025
average cost of gas to power plants ($3.85) and its 2025 nuclear fuel expense ($6.64 a MWh). The merit order, the Run it
week, the utility, the solar day, the battery and the retailer are the Works' (`explainer/industry/works/power.py`), with
illustrative parameters labelled on screen. ERCOT's price against gas fits the market monitor's annual averages for
2014-2020 and 2021 without Uri. California's "net load" is EIA-930 demand less solar and wind; the storage pattern is
the operator's "other fuel sources", negative while charging. The real price of a kWh is the BLS's US city average over
the CPI. Utilities' capital spending sums the six whose filings tag it every year from 2018 (Duke, Southern, Exelon,
Xcel, PG&E, Sempra). Company margins are net income over total revenue, averaged over five years.

## Problems and solutions

**1.** *A town uses 87,600 MWh of electricity a year. Its customers' own peaks add up to 40 MW, but the town's combined
peak is 16 MW. What is its load factor, measured on each, and what is its diversity factor?*

*Solution.* Average demand is 87,600 / 8,760 = 10 MW. On the combined peak the load factor is 10 / 16 = 62.5%; on the
customers' own peaks, 10 / 40 = 25%. The diversity factor is 40 / 16 = 2.5: because customers peak at different times,
the plant and wires need be only 40% as large as their peaks added together.

**2.** *A peaker costs $100 a kW-year to own and $40 a MWh to run; a combined-cycle plant costs $130 a kW-year and $28 a
MWh. At what capacity factor do they cost the same? Which should you build for a load needed 1,000 hours a year?*

*Solution.* A kW running at capacity factor f makes 8.76 f MWh a year, so 100 + 40 × 8.76 f = 130 + 28 × 8.76 f, giving
f = 30 / (12 × 8.76) = 28.5%, about 2,500 hours. For 1,000 hours (11%) the peaker costs 100 + 40 × 8.76 × 0.114 = $140 a
kW-year against $158 for the combined cycle: build the peaker.

**3.** *A market has 20 GW of wind at $0 a MWh, 5 GW of nuclear at $10, 10 GW of coal at $25, 30 GW of combined-cycle gas
at $30 and 10 GW of peakers at $60. What is the price when demand is 50 GW, and when it is 70 GW? What does the nuclear
plant earn above its running cost in an hour at 70 GW?*

*Solution.* Wind, nuclear and coal cover 35 GW, so at 50 GW the combined cycles are on the margin: $30. At 70 GW the 65
GW up to the combined cycles are not enough, so 5 GW of peakers run and set the price: $60. The nuclear plant earns $60 −
$10 = $50 a MWh, 5,000 MWh in the hour: $250,000, towards its fixed cost.

**4.** *A utility's rate base is $10 billion, financed half with equity allowed 10% and half with debt at 5%. Its O&M is
$400 million a year, depreciation 3.5% of the rate base, and income tax is grossed up at 21% on the equity return. It sells
20 TWh. What is its revenue requirement and price per kWh? What does one more point on the allowed return add?*

*Solution.* Return: 10,000 × (0.5 × 10% + 0.5 × 5%) = $750m. Tax: 10,000 × 0.5 × 10% × 0.21 / 0.79 = $133m.
Depreciation: $350m. Total: 400 + 350 + 133 + 750 = $1,633m, over 20 billion kWh: 8.2 cents. At 11%, the return rises
$50m and the tax $13m: $63m a year more, 0.3 cents a kWh, all from customers.

**5.** *A 400 MW plant sells its output for the next 48 hours forward at $50 a MWh. A storm freezes it, and the spot price
sits at $9,000. What does it lose? What if it had sold only half forward?*

*Solution.* It must buy 400 × 48 = 19,200 MWh at $9,000 to deliver power it sold for $50: a loss of 19,200 × 8,950 =
$172m. Half forward, it buys 9,600 MWh: $86m. Unhedged, it simply earns nothing for two days. A forward sale is a hedge
only if the plant can run; otherwise it is a bet that it will.

## Glossary

- **Load factor:** average demand over peak demand, for a customer, a block or a whole grid.
- **Diversity factor:** the sum of customers' own peaks over the peak of their combined load.
- **Capacity factor:** a plant's output as a share of what it could make running all year.
- **Merit order:** plants ranked from the cheapest to run to the dearest; the last one needed sets the price.
- **Screening curve:** a plant's yearly cost per kW against the hours it runs.
- **Rate base:** a regulated utility's plant and wires, net of depreciation, on which it may earn a return.
- **Revenue requirement:** the yearly revenue a commission lets a utility collect: costs, depreciation, taxes and return.
- **Energy-only market:** a market that pays plants only for energy, so scarce hours' prices must pay for readiness.
- **Load shed:** customers cut off on purpose to keep the grid in balance.
- **Net load:** demand less wind and solar: what every other plant must supply.

## Lab and interactive

- `python -m videos.industry.labs 13`: Insull's load factors; Run it; ERCOT's load duration curve; EIA's costs and the
  screening curve; capacity factors; price against gas; the merit order; the utility; February 2021; growth by decade;
  the solar day and the battery; Britain's suppliers; the world; data centres; the 2005 outlook; this series' call.
- The interactive (course site): the merit order. Set demand, gas, solar and wind and see which plant is on the margin,
  the price and what each plant earns.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p13.py`) or the Filing Room
(`explainer/industry/data/SOURCES.md`). The main ones:

- Samuel Insull, Central-Station Electric Service (1915): address of 25 February 1910.
- US Energy Information Administration: Hourly Electric Grid Monitor (EIA-930); Electric Power Annual 2025; Monthly
  Energy Review, Tables 7.6 and 9.8; Annual Energy Outlook 2005 and 2021 (Table 8); AEO2026 Electricity Market Module
  assumptions; Today in Energy (16 June 2026).
- FERC, NERC and Regional Entity staff, The February 2021 Cold Weather Outages in Texas and the South Central United
  States (November 2021).
- Potomac Economics, 2021 and 2024 State of the Market Reports for the ERCOT Electricity Markets.
- SEC EDGAR: Forms 10-K of Vistra (2021), Duke Energy (2025), NextEra, Southern, AEP, Dominion, Exelon, Xcel, Consolidated
  Edison, PG&E, Sempra, Entergy, Constellation, NRG, AES and GE Vernova.
- National Audit Office, The energy supplier market (June 2022).
- US Department of Energy, on Lawrence Berkeley National Laboratory's 2024 United States Data Center Energy Usage Report.
- BLS average electricity prices and the CPI, via FRED; Ember and the Energy Institute, via Our World in Data.
