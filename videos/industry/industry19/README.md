# Industry, Built: Part 19, Machinery

Part 19 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth of Act III, *Making*. It asks: how do the companies that make the machines earn
more from them after the sale than at it? It answers with the annual reports of Otis, Caterpillar, Deere, United Rentals,
Honeywell and 3M, Caterpillar's and Honeywell's reports for the third quarter of 2026 and GE Aerospace's for 2025; the SEC
company facts of twenty-three machinery, building-equipment, automation and rental companies; the Census Bureau's
machinery orders and shipments, the BEA's equipment investment, the Federal Reserve's machinery output and the BLS's jobs
and farm-machinery prices (via FRED); the International Federation of Robotics' press releases of 2022, 2024 and 2026 and
its installations by country (via the AI Index and Our World in Data); UN Comtrade's exports of excavators and robots; and
the Works' tender and installed base. The answer: every machine sold joins an installed base that needs parts, service and
repairs for decades, at margins the factory never sees, and that base is steadier than new sales, which swing with the
capital-goods cycle; makers know it, so when the servicing is worth enough they fight hard at the sale and machines are
sold near cost; dealers, the makers' own banks and the rental companies stand between the factory and the owner; and the
newest machines, robots and excavators, are increasingly bought and made in China.

It opens on Otis, which in 2025 sold $5.0bn of new elevators at a 4.8% margin and $9.4bn of service at 25.1%, looking
after about 2.5 million lifts and escalators; on Caterpillar's backlog, $30bn at the end of 2024, $51bn a year later and
$78bn in September 2026; and on the 5 million industrial robots now at work. From there it covers:

- Run it: the tender. Two makers bid for a fleet of 100 machines that cost $1.0m each, holding at $1.3m or cutting to
  $0.9m; whoever sells them services them, worth $0.6m a machine today. Both hold: $45m each; you cut and the rival holds:
  $50m and nothing; both cut: $25m each. Cutting is better either way, so both cut. If only 30% of owners buy service from
  the maker, holding pays against a holder ($24m against $8m); the attach rate above which cutting wins is 83%;
- what the makers sell: an excavator's engine, hydraulics, undercarriage and cab; Caterpillar's $67.6bn (Power & Energy
  $32.2bn, construction $25.1bn, mining $12.5bn, Financial Products $3.6bn); Deere's $45.7bn, with $6.3bn from financing;
- the capital-goods cycle: US equipment investment from 7.9% of GDP (1979) to 4.6% (2009) and 5.4% in 2025; machinery
  orders down 29% and shipments 19% in 2009; Caterpillar's sales down 41% from 2012 to 2016 and 22% in 2020;
- the installed base: Otis's two segments, service 65% of sales and 91% of segment profit; the Works' maker, whose new sales
  fall 44% in a crash year while its service revenue falls 2%, ending with service 62% of revenue and 89% of profit;
- dealers, lenders and the rental yard: Caterpillar's 150 dealers serving 190 countries, Deere's 2,050 dealer locations in
  the US and Canada; financing 13.8% of Deere's revenue and 5.3% of Caterpillar's; United Rentals' 1.1 million machines
  costing $22.5bn new, 1,768 locations, about 15% of North American rental, and margins of 10% to 20% since 2015;
- reading the cycle: machinery book-to-bill, 0.90 in 2009; Caterpillar's operating profit from $13.07bn to $11.15bn in
  2025 (volume +$1.22bn, price -$0.82bn, costs, mostly tariffs, -$2.15bn); the Supreme Court's ruling of 20 February 2026
  on the IEEPA tariffs, which had cost Caterpillar about $1.0bn, and $2.2bn of tariff costs still expected in 2026;
- an intermission: since 1990 America's machinery output rose 16% and its machinery jobs fell 23%; farm-machinery prices
  rose 17.8 times since 1947 against 14.4 for consumer prices;
- the robots: installations by country since 2011, China's from 23,000 to 354,000 (59% of the world's 600,000 in 2025),
  Chinese makers 55% of China's market; robot density from South Korea's 1,066 per 10,000 factory workers to America's 323
  and China's 193;
- China's makers: China's excavator exports from $1.2bn (2015) to $10.8bn (2025), passing Japan's $7.7bn; 320,016 machines
  against Japan's 151,321, at about $34,000 each against $51,000;
- the conglomerates come apart: GE HealthCare (January 2023) and GE Vernova (April 2024); Solventum from 3M (April 2024);
  Solstice (October 2025) and Honeywell Aerospace (June 2026) from Honeywell; GE Vernova's $38.1bn of revenue;
- the landscape, November 2026: twenty companies by revenue and median margin, and the map of the business;
- *Called it?*: the IFR's forecasts (570,000 for 2022 against 552,946; 541,000 for 2024 against about 542,000; mid to upper
  single-digit growth to 2025, about 660,000 to 740,000, against a little over 600,000) and this series' call that 2026's
  installations will come in below the IFR's 655,000 (55%);
- after the sale: the five answers.

## Build it

```bash
python -m videos.industry.industry19.compute               # every number, printed
EXPLAINER_TTS=silent python tools/build.py industry19 -q l  # the whole part, silent preview
python tools/build.py industry19                           # 1080p30 with narration
python -m videos.industry.labs 19                          # the lab
python -m pytest tests/industry                            # the Register and the Works (test_machine.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p19.py`) or comes from the Filing Room: the machinery
companies' accounts (`sec_mach.csv`), FRED's orders, shipments, investment, output, jobs and prices (`fred_mach.csv`), robot
installations (`owid_robots.csv`) and UN Comtrade's exports (`comtrade_mach.csv`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The machine and the service | Otis's two businesses; Caterpillar's backlog; the robots; the title |
| 1 | Run it: the tender | The fleet and the bids; the four outcomes; the attach rate flips it |
| 2 | What the machine makers sell | Inside an excavator; Caterpillar's segments; Deere's lines |
| 3 | Capital goods: the cycle | Equipment investment since 1947; machinery orders and shipments; Caterpillar since 2009 |
| 4 | The installed base | Otis's segments; the Works' maker through a cycle; the shares of revenue and profit |
| 5 | Dealers, lenders and the rental yard | The dealer's jobs; the makers' banks; United Rentals |
| 6 | Reading the cycle | Book-to-bill; Caterpillar's profit bridge; the backlog and the tariffs |
| — | Intermission | Machinery output against jobs; farm-machinery prices against all prices |
| 7 | Automation: the robots | Installations by country; robot density |
| 8 | China's makers | Excavator exports by value and by count |
| 9 | The conglomerates come apart | GE, 3M and Honeywell; why |
| 10 | The landscape, November 2026 | Revenue against margin; the map of the business |
| 11 | Called it? | The IFR's forecasts; this series' call |
| — | After the sale | The five answers; Part 20, pharmaceuticals |

## What is computed, and from what

`compute.py` reads the Filing Room and the Register. The tender and the maker are the Works'
(`explainer/industry/works/machine.py`), with illustrative parameters labelled on screen. In the tender the lower bid wins
all 100 machines and a tie splits them; a maker's value is its machines times (price - cost + $0.6m × attach rate). The
maker's new-machine demand follows a trend of 2% a year, an eight-year sine wave of ±45% and one year at half; each
machine sells for 1, at a 5% margin, works 15 years and earns 12% of its price a year in parts and service at a 25%
margin; the shares are over years 15 to 39, after the installed base has filled. Margins are profit attributable to the
parent over revenue from the companies' filings, by fiscal year; the landscape uses the median of 2021-2025, which a
single year's one-off gain or loss (Emerson's 87% margin in 2023, 3M's loss in 2023) cannot move. Machinery
orders and shipments are sums of the Census Bureau's seasonally adjusted monthly values; equipment investment and GDP are
annual averages of quarterly rates; the CPI averages eleven months in 2025 (the BLS published no October 2025 CPI). Robot
installations are the IFR's, via the AI Index Report 2026 and Our World in Data to 2024 and its press release for 2025
(the world's 'more than 600,000', Germany's 'fewer than 25,000'). Average export values divide Comtrade's dollars by its
reported quantities.

## Problems and solutions

**1.** *Two makers bid for 100 machines that cost $1.0m each to build. Each bids $1.3m or $0.9m; the lower bid wins all
100 and a tie splits them. The winner's servicing is worth $0.6m a machine today. Find each maker's value in the four
cases, and what two sensible makers do.*

*Solution.* A machine sold at $1.3m is worth 1.3 - 1.0 + 0.6 = $0.9m; at $0.9m, $0.5m. Both hold: 50 × 0.9 = $45m each.
You cut, the rival holds: 100 × 0.5 = $50m for you, nothing for the rival. Both cut: 50 × 0.5 = $25m each. If the rival
holds, cutting (50) beats holding (45); if the rival cuts, cutting (25) beats holding (0). Both cut, and each has $25m
instead of $45m: the value of the servicing has been handed to the customer in the price.

**2.** *In the same tender, only a share a of owners buys parts and service from the maker. Above what attach rate is
cutting the better reply to a rival who holds?*

*Solution.* Holding against a holder is worth 50 × (0.3 + 0.6a); cutting against a holder, 100 × (-0.1 + 0.6a).
Cutting is better when 100(-0.1 + 0.6a) > 50(0.3 + 0.6a), that is -10 + 60a > 15 + 30a, so a > 25 / 30 = 0.83. A maker
that keeps more than about five-sixths of the servicing will fight for the sale; at a 30% attach rate it will not.

**3.** *In 2025 Otis's New Equipment segment had sales of $4,989m and operating profit of $240m; Service had $9,442m and
$2,374m. Find each margin, Service's share of sales and of profit, and how much more profit a dollar of service sales
brought than a dollar of new equipment.*

*Solution.* New Equipment: 240 / 4,989 = 4.8%; Service: 2,374 / 9,442 = 25.1%. Service is 9,442 / 14,431 = 65% of sales
and 2,374 / 2,614 = 91% of segment profit. A dollar of service brought 25.1 / 4.8 = 5.2 times the profit of a dollar of
new equipment.

**4.** *Caterpillar's sales and revenues were $20.7bn in the third quarter of 2026, and its order backlog rose by $6.0bn
in the quarter. Ignoring cancellations and other adjustments, what orders did it take, and what was its book-to-bill?
What does it mean?*

*Solution.* Orders ≈ sales + the rise in backlog = 20.7 + 6.0 = $26.7bn, so book-to-bill ≈ 26.7 / 20.7 = 1.29. It took
29% more orders than it shipped; the backlog is growing, and at that pace the factories will be busy for longer than a year
ahead (the backlog, $78.1bn, is almost four quarters of sales).

**5.** *China installed 23,000 industrial robots in 2011 and 354,000 in 2025. What was the average annual growth rate? The
IFR forecasts 655,000 installations worldwide in 2026, a 9% rise; what does that say 2025's total was?*

*Solution.* (354,000 / 23,000)^(1/14) = 15.4^(0.0714) = 1.216: about 22% a year for fourteen years. A 9% rise to 655,000
means 2025 was about 655,000 / 1.09 = 601,000, consistent with the IFR's 'more than 600,000'.

## Glossary

- **Capital goods:** machines and equipment bought by businesses to produce other things.
- **Installed base:** all the machines a maker has sold that are still in use.
- **Aftermarket:** parts, service, repairs and upgrades sold for machines already in use.
- **Attach rate:** the share of a maker's installed base whose owners buy parts and service from the maker.
- **Dealer:** an independent company licensed to sell and service a maker's machines in a territory.
- **Captive finance arm:** a maker's own lender, financing its machines for owners and dealers.
- **Rental fleet:** machines owned by a rental company and hired out by the day, week or month.
- **Backlog:** firm orders not yet delivered.
- **Book-to-bill:** new orders divided by shipments; above one, the backlog grows.
- **Price realization:** the part of a change in sales or profit due to prices rather than volumes.
- **Industrial robot:** an automatically controlled, reprogrammable, multipurpose machine that moves in three or more axes.
- **Robot density:** industrial robots in use per 10,000 manufacturing employees.
- **Conglomerate:** a company that owns businesses in several unrelated industries.
- **Spin-off:** a company separating a business by giving its shareholders shares in the new company.

## Lab and interactive

- `python -m videos.industry.labs 19`: Otis's segments; the tender and its attach threshold; Caterpillar's segments and
  Deere's lines; equipment investment, orders and shipments; the installed base through a cycle; dealers, lenders and
  United Rentals; book-to-bill and the profit bridge; output and jobs; robots and density; excavator exports; the
  separations; and the forecasts, with this series' call.
- The interactive (course site): the tender. Set the bids, the value of servicing and the attach rate, and see the four
  outcomes, the equilibrium and the attach rate above which the makers fight for the sale.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p19.py`) or the Filing Room
(`explainer/industry/data/SOURCES.md`). The main ones:

- SEC EDGAR: Forms 10-K of Otis, Caterpillar, United Rentals, Honeywell and 3M (2025) and Deere (fiscal 2025); Forms 10-Q
  of Caterpillar and Honeywell for the third quarter of 2026; GE Aerospace's Form 10-K 2025; the company facts of
  Caterpillar, Deere, CNH, AGCO, Cummins, Otis, Carrier, Trane, Johnson Controls, Rockwell, Emerson, Honeywell, Illinois
  Tool Works, Parker Hannifin, Eaton, Dover, United Rentals, Terex, Oshkosh, 3M, GE Vernova, Ingersoll Rand and Xylem.
- FRED: the Census Bureau's machinery orders and shipments and core capital goods orders; the BEA's equipment investment
  and GDP; the Federal Reserve's machinery output and capacity use; the BLS's machinery jobs, producer prices of farm and
  construction machinery, and the CPI-U.
- International Federation of Robotics: press releases of 13 October 2022, 24 September 2024, 24 September 2026 and 12
  November 2026; installations by country via the AI Index Report 2026 and Our World in Data.
- UN Comtrade: exports of HS 842952 and 847950 by China, Japan, Germany, South Korea and the United States.
