# Industry, Built: Part 25, Homes

Part 25 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second of Act IV, *Building*. It asks: where does the price of a house come from:
the house, the land or the loan? It answers with D.R. Horton's Forms 8-K of 28 October 2025 and 29 October 2026 and its
Form 10-K for fiscal 2026; the Forms 10-K of Lennar (fiscal 2025), NVR, Fannie Mae and Compass (2025); Invitation Homes'
annual report; the SEC company facts of twenty-five builders, factory builders, suppliers, lenders, brokers and a landlord;
the Census Bureau's starts, sales, months' supply, prices and homeownership, Freddie Mac's mortgage rates, S&P
CoreLogic Case-Shiller's national index, the BLS's materials prices and rents, the Federal Reserve's mortgage debt and
delinquencies (all via FRED); and the Works' builder. The answer: what a buyer can pay is what a buyer can borrow, so the
thirty-year rate moves the monthly cost more than the price does; house prices have outrun the cost of building, and the
difference is land near jobs and the permission to build on it; builders bet on both years ahead, which is why the largest
of them now control most of their land by option rather than own it; when rates rise, builders pay down the buyer's rate
and their margins pay for it; and the brokers, portals and lenders in between keep little.

It opens on one house: the median new American house cost $354.8k in January 2021, when the thirty-year rate was 2.74%,
and $391.3k in October 2026, at 7.33%; with 10% down the monthly payment went from $1,301 to $2,421. Real house prices
(Case-Shiller over the CPI, 1987 = 1) were 1.56 at the 2006 peak and 1.75 in 2025. From there it covers:

- Run it: buy land for 2029. A home sells for $400k today: $100k for a finished lot, $220k to build, 8% to sell it and run
  the company, 12% profit. It will be sold in three years, for $432k if rates hold (60%) or $340k if they rise (40%). Own
  the lot (carried at 7% a year) and make $54.9k or lose $29.7k a home, $21.1k on average, 21% on the $100k tied up; option
  it (a $10k deposit, the lot bought later at a price rising 12% a year) and make $36.9k or lose the deposit, $18.2k on
  average, 182% on the $10k. Above a 48% chance of a bust the option earns more even per home;
- a builder's arithmetic: D.R. Horton's fiscal 2026, $33.0bn of revenue from 84,202 homes at $363.6k on average, a gross
  margin of 20.2% (21.5% a year before) and 11.2% before tax; Lennar's 82,583 deliveries at $391k (from $445k in 2023), a
  gross margin of 17.7% (22.3%) and incentives of $62.7k a home (from $48.8k), 13.8% of the price before them; 17,700
  unsold homes at D.R. Horton; the subcontractors who do the building;
- own the land, or control it: D.R. Horton's 570,600 lots, 23% owned and 77% controlled through purchase contracts, about
  1.5 years of closings owned and 6.8 years in all; Lennar's homesites 98% controlled by option (82% a year before),
  through land banks and its spin-off Millrose; Forestar's 38,400 lots and the 68% of D.R. Horton's homes built on lots
  others developed; NVR's 169,250 lots under purchase agreements backed by $920.1m of deposits, about $5.4k a lot; Lennar
  walking away from 15,500 homesites and writing off $23.1m of deposits, Run it's bust case in an annual report;
- why prices outran costs: starts from 2.36m (1972) to 554k (2009) and 1.36m (2025); months' supply 9.0 in 2009, 4.6 in
  2020 and 8.8 in 2025; new single-family sales 1.28m (2005), 0.31m (2011), 0.68m (2025); since 2000, consumer prices 1.87
  times, materials 2.27 and house prices 3.14; the median price over median household income 3.6 (1984), 5.8 (2022) and
  4.7 (2025); land near jobs, zoning and approvals;
- the thirty-year loan: rates from 16.6% (1981) to 2.96% (2021) and 6.60% (2025); the payment on the median new house as
  a share of median income, 45% (1984), 22% (2020) and 33% (2025); how a loan is paid down; Fannie Mae's $4.1tn book,
  about a quarter of American mortgage debt; the lock-in of owners with cheap loans; delinquencies from 10.9% (2010) to
  1.8% (2025); $14.0tn of household mortgage debt;
- an intermission: rents 2.4 times their 2000 level; homeownership from 69.0% (2004) to 65.3% (2025); rental vacancy
  from 10.6% (2009) to 5.8% (2022) and 7.1% (2025); Invitation Homes' 86,192 rented houses;
- between the buyer and the house: the National Association of Realtors' settlement and the practice changes of August
  2024, with Anywhere's $83.5m; Zillow's and Compass's margins (losses in most years); Opendoor's revenue from $15.6bn
  (2022) to $4.4bn (2025) with a loss in every year; UWM's margin from 3.3% (2021) to a loss in 2023;
- after the sale: Home Depot's $165bn and Lowe's $86bn of revenue, at margins of 8.6% and 7.7%, against D.R. Horton's
  $33bn; Builders FirstSource's lumber boom and bust; factory-built homes at Cavco and Champion;
- the landscape, November 2026: twenty companies by revenue and median five-year margin; and the map of the business;
- *Called it?*: D.R. Horton's October 2025 guidance (86,000-88,000 homes, $33.5-35.0bn) against its fiscal 2026 (84,202,
  $33.0bn); Fannie Mae's February 2026 forecast of $2.41tn of originations; and this series' call that D.R. Horton will
  close fewer than 81,500 homes in fiscal 2027 (60%);
- the house, the land and the loan: the five answers.

## Build it

```bash
python -m videos.industry.industry25.compute               # every number, printed
EXPLAINER_TTS=silent python tools/build.py industry25 -q l  # the whole part, silent preview
python tools/build.py industry25                           # 1080p30 with narration
python -m videos.industry.labs 25                          # the lab
python -m pytest tests/industry                            # the Register and the Works (test_builder.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p25.py`) or comes from the Filing Room: the companies'
accounts (`sec_homes.csv`) and FRED's housing, mortgage and price series (`fred_homes.csv`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The house, the land or the loan | One house's payment in 2021 and 2026; real prices; the median new house; the title |
| 1 | Run it: buy land for 2029 | The deal; the dollar; two futures; own against option; the capital; the crossing point |
| 2 | A builder's arithmetic | D.R. Horton's year and margin; Lennar's prices and incentives; unsold homes; subcontractors |
| 3 | Own the land, or control it | D.R. Horton's lots; Lennar's options; lots in years; Forestar; NVR; walking away |
| 4 | Why prices outran costs | Starts; months' supply; sales; prices against costs; price over income; land |
| 5 | The thirty-year loan | Rates; the payment's share of income; paying down; Fannie Mae; lock-in; delinquencies; debt |
| — | Intermission | Rents; owners; vacancy; a landlord of houses |
| 6 | Between the buyer and the house | The commission rules; the portals; the lender; the iBuyer |
| 7 | After the sale | The stores; the distributor; Home Depot's cycle; factory-built homes |
| 8 | The landscape, November 2026 | Revenue against margin; the map |
| 9 | Called it? | D.R. Horton's guidance; Fannie Mae's forecast; this series' call |
| — | The house, the land and the loan | The five answers; Part 26, property |

## What is computed, and from what

`compute.py` reads the Filing Room and the Register. The land deal is the Works' (`explainer/industry/works/builder.py`):
a home sells for $400k today on a $100k lot with $220k of building cost and overhead of 8% of the sale price; it is sold
in three years at 8% above today's price or 15% below, with a 40% chance of the fall. An owned lot is carried at 7% a
year, compounded; an optioned lot costs a $10k deposit now and is bought at the end at today's price compounded at 12% a
year (the deposit is part of that price); in the bust the optioned lot is abandoned if building would lose more than the
deposit. The return is the expected profit over the capital tied up (the lot, or the deposit). Mortgage payments are
level payments on a thirty-year fixed loan of 90% of the price at the monthly or annual average of Freddie Mac's
thirty-year rate; the payment's share of income is twelve payments on the year's median new house over the Census
Bureau's median household income. Real house prices are the Case-Shiller national index over the CPI-U, both annual
averages. Annual values are averages of monthly or quarterly observations (weekly rates are averaged within each month
first). Margins are profit attributable to the parent over revenue, the median of the last five fiscal years. Lots in
years are lots over the homes closed in fiscal 2026.

## Problems and solutions

**1.** *In Run it, the home sells in three years for $432k (boom) or $340k (bust). The owned lot costs $100k carried at 7%
a year; the optioned lot costs $100k × 1.12³ at the end. Building costs $220k and overhead is 8% of the sale. Compute the
profit per home in each case, and the expected profit with a 40% chance of the bust.*

*Solution.* Owned lot: 100 × 1.07³ = $122.5k. Boom: 432 - 122.5 - 220 - 34.6 = $54.9k; bust: 340 - 122.5 - 220 - 27.2 =
-$29.7k; expected 0.6 × 54.9 - 0.4 × 29.7 = $21.1k. Optioned lot: 100 × 1.12³ = $140.5k. Boom: 432 - 140.5 - 220 - 34.6 =
$36.9k; bust: building would lose 340 - 140.5 - 220 - 27.2 = -$47.7k, so the builder walks away and loses the $10k deposit;
expected 0.6 × 36.9 - 0.4 × 10 = $18.2k.

**2.** *At what chance of a bust do owning and optioning earn the same per home?*

*Solution.* Owning earns 54.9 - p(54.9 + 29.7) = 54.9 - 84.6p; optioning earns 36.9 - p(36.9 + 10) = 36.9 - 46.9p. They
are equal when 18.0 = 37.7p, p = 0.48. Below that owning earns more per home; above it optioning does. Per dollar tied up
optioning wins at every p here, because it ties up a tenth of the money.

**3.** *The median new house cost $354.8k in January 2021 at a rate of 2.735% and $391.3k in October 2026 at 7.328%. With
10% down on a thirty-year fixed loan, the payments are $1,301 and $2,421. How much of the $1,120 rise came from the price
and how much from the rate?*

*Solution.* The monthly payment per dollar borrowed is r / (1 - (1 + r)^-360), with r the monthly rate: 0.004075 at 2.735%
and 0.006875 at 7.328%. At the 2021 rate the 2026 loan of $352.2k would cost 352.2 × 4.075 = $1,435 a month: the price
added $134, the rate the other $986. (Taking the rate first gives $2,195 for the 2021 loan at the 2026 rate, $894 from the
rate and $226 from the price; either way, the rate did most of it.)

**4.** *D.R. Horton owned 130,500 lots and controlled 440,100 more in September 2026, and closed 84,202 homes in fiscal
2026. How many years of building do the owned lots, and all the lots, represent? What share was owned, and what was it a
year before (147,000 owned, 444,900 controlled)?*

*Solution.* Owned: 130,500 / 84,202 = 1.5 years. All: 570,600 / 84,202 = 6.8 years. Owned share: 130,500 / 570,600 = 23%,
against 147,000 / 591,900 = 25% a year before.

**5.** *Lennar's average sale price in fiscal 2025 was $391k after incentives of $62.7k a home ($48.8k a year before), and
its gross margin was 17.7%. What share of the price before incentives did the incentive take? If the incentive had stayed
at $48.8k and costs had not changed, what would the margin have been?*

*Solution.* 62.7 / (391 + 62.7) = 13.8%. Cost per home: 391 × (1 - 0.177) = $321.8k. With $13.9k less incentive the price
would have been $404.9k and the margin (404.9 - 321.8) / 404.9 = 20.5%: the extra incentives explain about 2.8 of the 4.6
points by which the margin fell from 22.3%. (This holds the home's cost fixed, which is this exercise's assumption.)

## Glossary

- **Finished lot:** a plot with roads, water, sewers and power, ready for a house.
- **Lot option (lot purchase agreement):** a contract to buy a lot later at an agreed price, secured by a deposit that is
  lost if the builder walks away.
- **Land bank:** an investor that buys land and sells it to a builder lot by lot under such contracts.
- **Closing (settlement, delivery):** the day a home's sale completes and the builder books the revenue.
- **Gross margin:** revenue less the cost of the homes sold, as a share of revenue.
- **Incentive (buydown):** a payment by the builder, often to lower the buyer's mortgage rate, that reduces the price
  received.
- **Months' supply:** the homes for sale divided by the monthly pace of sales.
- **Thirty-year fixed-rate mortgage:** a loan repaid in equal monthly payments over thirty years at a rate fixed at the
  start.
- **Government-sponsored enterprise:** Fannie Mae or Freddie Mac, which buy and guarantee mortgages and sell them on as
  bonds.
- **Lock-in:** owners staying put because moving would replace a cheap loan with a dear one.
- **Buyer's agent:** the broker who represents the buyer, paid a commission.
- **iBuyer:** a company that buys homes directly from sellers to resell them.

## Lab and interactive

- `python -m videos.industry.labs 25`: the Works' land deal, owned against optioned, and the chance of a bust at which
  they cross; one house's payment in 2021 and 2026; D.R. Horton's, Lennar's and NVR's years and lots; starts, months' supply
  and sales; prices against costs and incomes; the payment's share of income; rents, owners and vacancy; the brokers, the
  stores and the lender; the landscape; and this series' call.
- The interactive (course site): bet on land. Choose the chance of a bust, how far prices fall, the land banker's return
  and the deposit, and see the profit per home and per dollar of owning and of optioning; then set a price and a rate and
  see the monthly payment.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p25.py`) or the Filing Room
(`explainer/industry/data/SOURCES.md`). The main ones:

- SEC EDGAR: D.R. Horton's Forms 8-K of 28 October 2025 and 29 October 2026 and Form 10-K for fiscal 2026; the Forms 10-K
  of Lennar (fiscal 2025), NVR, Fannie Mae and Compass (2025); Invitation Homes' Form 10-K for 2025; the company facts of
  D.R. Horton, Lennar, PulteGroup, NVR, Toll Brothers, KB Home, Meritage, Century Communities, M/I Homes, Dream Finders,
  LGI Homes, Cavco, Champion Homes, Builders FirstSource, Home Depot, Lowe's, Rocket, UWM, Fannie Mae, Freddie Mac,
  Zillow, Compass, Opendoor, Invitation Homes and American Homes 4 Rent.
- FRED: S&P CoreLogic Case-Shiller's national home price index; the Census Bureau's starts, permits, new houses sold, months'
  supply, median sales prices, homeownership and rental vacancy rates and median household income; Freddie Mac's
  thirty-year mortgage rate; the BLS's rent of primary residence, producer prices for inputs to residential construction
  and the CPI; the Federal Reserve's household mortgage debt and delinquency rate on single-family mortgages.
