# Industry, Built: Part 27, Shipping and Ports

Part 27 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first of Act V, *Moving*. It asks: how did moving a tonne across an ocean become
nearly free, and why do the companies that do it swing between fortune and ruin? It answers with ZIM's Forms 20-F for
2020, 2021, 2023 and 2025 and its 2026 results and guidance; Frontline's Form 20-F for 2025 and third-quarter 2026 report;
Matson's Form 10-K for 2025; E2open's Form 10-K of May 2021; Greenwood and Hanson's study of ship prices; the SEC company
facts of twenty-two lines, shipowners, tanker and bulk companies and forwarders, and Maersk's annual reports; IMF
PortWatch's daily transits through six chokepoints since 2019; the World Bank's container port traffic; FRED's deep-sea
freight prices, Brent crude and American imports; and the Works' shipping market. The answer: enormous ships, sailing
slowly and full, and one standard box that every crane, ship, train and lorry takes, made the voyage cost a pair of
trainers pennies; but a full fleet can charge almost anything and a half-empty one almost nothing, everyone orders ships
at the same moment and they arrive years later, together, and the whole system squeezes through a few narrow places, any
of which can close. The cheapness and the violence are the same machine.

It opens on a pair of trainers: at about 5,000 pairs to a forty-foot box (this series' assumption) and ZIM's average
freight of $1,551 a TEU in 2025, the ocean voyage cost about 62 cents a pair; 40 cents in 2019, $1.30 in 2022, 48 cents in
2023. And on the Suez Canal in March 2021: about 55 ships a day, then two on 25 March, when the Ever Given blocked it for
six days. From there it covers:

- Run it: thirty years as a shipowner. In the Works a ship earns $10k a day when the fleet is idle and up to $100k when
  every ship is busy, and needs $25k to pay for itself; the industry orders in proportion to today's profit and the ships
  arrive three years later. Earnings spike at the start and in years 11 and 22 and sit near the floor between. Following
  the market (ordering when earnings top $40k) buys 4 ships at $112m on average, arriving to $18k a day, and returns 8% over
  the thirty years; going against it (ordering below $18k) buys 6 ships at $66m and returns 136%. After Greenwood and
  Hanson: high earnings bring high prices and investment, and low returns after;
- a ship's day: fuel a day rises with the cube of speed, a mile with the square; a voyage of 11,000 miles at 20 knots, 23
  days and $2.29m, at 16 knots, 29 days and $2.03m; the cheapest speed from 17.5 knots (fuel at $300 a tonne) to 12.1 ($900);
  ZIM's fuel 25.7% of its operating costs in 2025;
- the box: world port traffic from 547m TEU (2010) to 913m (2024); China 300m, America 60m, Singapore 41m; ZIM's volume from
  2.82m TEU (2019) to 3.66m (2025); the fleet from 25m TEU (2021) to 33.3m (2025), with 11.3m on order;
- fortune and ruin: ZIM's average freight from $1,009 (2019) to $3,240 (2022) and $1,203 (2023), by quarter from $1,310
  (2026 Q1) to $2,480 (2026 Q3); the BLS's deep-sea freight prices; ZIM's net income of $4.6bn in 2021 and 2022 and a loss
  of $2.7bn in 2023; Maersk's operating profit from $1.7bn (2019) to $30.9bn (2022) and $3.5bn (2025); capacity growth of
  10.3% (2024) and 7.3% (2025) against cargo growth of 3.5%;
- liners and the lessors: MSC, Maersk and CMA CGM with 47.8% of capacity; ZIM's freight by trade ($1,965 Cross-Suez to $960
  within Asia); 16 of ZIM's 128 ships owned; the lessors' steady margins against ZIM's swings; Hapag-Lloyd's agreement to buy
  ZIM for $35 a share;
- an intermission: deep-sea freight prices 3.9 times their 1989 level; Brent at $96 in 2026 so far; American goods imports
  from $2.0tn to $4.7tn; port traffic by country, 2010 against 2024;
- chokepoints: six on a map; Suez from 74 ships a day (2023) to 40 (2024) after the Houthi attacks; the Cape of Good Hope
  from 49 to 87; Panama down to 20 a day in early 2024; Malacca 234 a day in 2025; Hormuz from 85 a day (2025) to 3 from March
  2026;
- tankers and tramps: tankers through Hormuz from 48 a day to under one; Frontline's VLCCs earning $152,700 and $148,500 a
  day in the second and third quarters of 2026 against a cash breakeven of $24,100, and $562,600 booked for the fourth; its
  one-year charters at $76,900; Frontline's and Star Bulk's profits; a tanker orderbook of 27% of the fleet; two 2017 VLCCs
  sold for $270m;
- ports, forwarders and flags: the terminal as a concession; Expeditors' and C.H. Robinson's revenue and steady margins
  against ZIM's; the Jones Act and Matson (51% of its ocean revenue in protected trades, a 13% margin);
- the landscape, November 2026: twenty-two companies by revenue and margin, and the map of the business;
- *Called it?*: ZIM's 2026 forecast raised from $2.0-2.4bn in August to $3.3-3.5bn in November; the market's view at the end
  of 2021 against the fleet growth and rates that followed; and this series' call that Hapag-Lloyd's purchase of ZIM will be
  completed by 30 June 2027 (60%);
- nearly free, and never safe: the five answers.

## Build it

```bash
python -m videos.industry.industry27.compute               # every number, printed
EXPLAINER_TTS=silent python tools/build.py industry27 -q l  # the whole part, silent preview
python tools/build.py industry27                           # 1080p30 with narration
python -m videos.industry.labs 27                          # the lab
python -m pytest tests/industry                            # the Register and the Works (test_ship.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p27.py`) or comes from the Filing Room: the companies'
accounts (`sec_ship.csv`, `esef_maersk.csv`), IMF PortWatch's chokepoint transits (`imf_portwatch.csv`), the World Bank's
port traffic (`wb_ports.csv`) and FRED's freight, oil and import series (`fred_ship.csv`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Less than a dollar a pair | A pair of trainers; the freight a pair by year; Suez in March 2021; the title |
| 1 | Run it: thirty years as a shipowner | The earnings curve; thirty years; the herd; two rules; ship prices; the payoff; why it is hard |
| 2 | A ship's day | The cube law; one voyage at two speeds; the cheapest speed; fuel prices and ZIM's fuel bill |
| 3 | The box | One size, one crane; world port traffic; the countries; ZIM's volume; the fleet and the orderbook |
| 4 | Fortune and ruin | ZIM's freight by year and quarter; the freight index; ZIM's and Maersk's profits; ships against cargo |
| 5 | Liners and the lessors | The top three; ZIM's trades; owned and chartered ships; lessors' margins; Hapag-Lloyd and ZIM |
| — | Intermission | Deep-sea freight prices; oil; imports; port growth by country |
| 6 | Chokepoints | The map; the Red Sea; the Cape; Panama; Malacca; Hormuz |
| 7 | Tankers and tramps | The Gulf's tankers; a VLCC's day; the fourth quarter; charters; profits; the orderbook |
| 8 | Ports, forwarders and flags | The terminal; forwarders' revenue and margins; the Jones Act |
| 9 | The landscape, November 2026 | Revenue against margin; the map |
| 10 | Called it? | ZIM's forecast; the view from 2021; this series' call |
| — | Nearly free, and never safe | The five answers; Part 28, airlines |

## What is computed, and from what

`compute.py` reads the Filing Room and the Register. The market is the Works' (`explainer/industry/works/ship.py`): demand
grows 3% a year with a normal shock of 4.5% (seed 1); a ship earns $10k a day plus $90k times the cube of how far
utilization is above 80%, capped at full use; the industry orders 2% of the fleet a year plus up to 22% in proportion to
earnings above $25k; ships arrive three years later; 2% of the fleet is scrapped a year, 4.5% when earnings are below $15k;
a new ship costs $40m plus $40m times the square root of earnings over $25k. Twelve years are run before the thirty shown.
An owner's ship earns the market rate less $9k a day of running costs from delivery to year thirty, plus what is left of a
25-year life at the last year's price; at most one order every three years. The voyage burns 100 tonnes a day at 20 knots,
scaled by the cube of speed; the ship's other costs are $40,000 a day. The freight on a pair is two TEU's freight over 5,000
pairs. Chokepoint traffic is IMF PortWatch's daily transit calls, estimated from ships' positions, averaged by month and
year. Margins are net income attributable to the parent over revenue, the median of the last five fiscal years; Maersk's
is operating profit over revenue.

## Problems and solutions

**1.** *A forty-foot container holds 5,000 pairs of trainers and ZIM was paid $1,551 per TEU in 2025 and $3,240 in 2022. What
was the ocean freight on one pair in each year? If the pairs sold for $80, what share of the price was freight?*

*Solution.* A forty-foot box is two TEU: 2 × 1,551 / 5,000 = $0.62 in 2025, 2 × 3,240 / 5,000 = $1.30 in 2022. That is 0.8%
and 1.6% of an $80 price. Even at the top of the boom, the voyage was a rounding error in the price of the shoe.

**2.** *A ship burns 100 tonnes of fuel a day at 20 knots, and fuel a day rises with the cube of speed. How much does it burn
a day at 16 knots, and how much fuel does an 11,000-mile voyage use at each speed?*

*Solution.* 100 × (16/20)³ = 51.2 tonnes a day. At 20 knots the voyage takes 11,000 / (20 × 24) = 22.9 days and burns 2,292
tonnes; at 16 knots, 28.6 days and 1,467 tonnes: 36% less fuel for 25% more time.

**3.** *With fuel at $600 a tonne and the ship's other costs at $40,000 a day, which is cheaper for that voyage, 20 knots or 16?*

*Solution.* 20 knots: 2,292 × 600 + 22.9 × 40,000 = 1.375m + 0.917m = $2.29m. 16 knots: 1,467 × 600 + 28.6 × 40,000 = 0.880m
+ 1.146m = $2.03m. Sixteen knots saves about $0.27m a voyage; the cheapest speed, found by trying every speed, is about 13.9
knots.

**4.** *Frontline's VLCCs needed $24,100 a day to break even in cash. They earned $148,500 a day in the spot market in the third
quarter of 2026, and seven had been let for a year from January at $76,900. What did each earn above breakeven in a 92-day
quarter, spot and on charter?*

*Solution.* Spot: (148,500 - 24,100) × 92 = $11.4m a ship. Charter: (76,900 - 24,100) × 92 = $4.9m. The charter gave up about
$6.6m a ship in that quarter for the certainty agreed in January.

**5.** *In 2025 the container fleet grew 7.3% and cargo 3.5%. For 2026 the forecast was 3.7% and 2.5%. If utilization was 90% at
the start of 2025, what would it be at the end of 2026, all else equal? What does Run it's curve say that does to earnings?*

*Solution.* 0.90 × 1.035 × 1.025 / (1.073 × 1.037) = 0.90 × 1.0609 / 1.1127 = 0.858. In the Works, earnings at 90% busy are
about $21k a day and at 86% about $12k: a fall of more than 40%, below breakeven. (In fact the detours round Africa and the
Gulf's closure absorbed ships and pushed rates up instead: utilization depends on how far each box travels, not only on
how many there are.)

## Glossary

- **TEU:** twenty-foot equivalent unit, the size of a small container; a forty-foot box is two TEU.
- **Liner:** a ship, or a company, running fixed routes on a timetable, as container lines do.
- **Tramp:** a ship hired for a voyage or a period, wherever the cargo is, as most tankers and bulk carriers are.
- **Spot market, time charter:** hiring a ship for one voyage at today's rate, or for months or years at a fixed daily rate.
- **Time charter equivalent (TCE):** a ship's voyage revenue less voyage costs (fuel, port and canal fees), per day.
- **VLCC:** very large crude carrier, the largest common class of oil tanker.
- **Orderbook:** ships ordered from shipyards and not yet delivered.
- **Slow steaming:** sailing well below a ship's design speed to save fuel.
- **Chokepoint:** a canal or strait through which a large share of shipping must pass.
- **Freight forwarder:** a company that books transport and handles the paperwork for shippers, usually without owning
  ships.
- **Jones Act:** the American law (the Merchant Marine Act of 1920) reserving cargo between American ports to
  American-built, American-flagged, mostly American-crewed and American-owned ships.

## Lab and interactive

- `python -m videos.industry.labs 27`: the Works' market and the owner's two rules; a voyage at different speeds and fuel
  prices; ZIM's freight by year and quarter; the fleet and the orderbook; chokepoint traffic; Frontline's earnings against
  breakeven; the forwarders' margins; the landscape; and this series' call.
- The interactive (course site): sail a voyage. Choose the speed, the price of fuel and the ship's daily cost, and see the
  days, the fuel and the cost of the voyage, and the cheapest speed; then choose a rule for ordering ships and watch thirty
  years of the Works' market.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p27.py`) or the Filing Room
(`explainer/industry/data/SOURCES.md`). The main ones:

- SEC EDGAR: ZIM's Forms 20-F for 2020, 2021, 2023 and 2025 and its Forms 6-K of 9 March, 20 May, 19 August, 6 October and
  18 November 2026 (with Alphaliner's fleet statistics as ZIM quotes them); Frontline's Form 20-F for 2025 and Form 6-K of
  20 November 2026; Matson's Form 10-K for 2025; E2open's Form 10-K of May 2021; the company facts of ZIM, Matson, Kirby,
  Frontline, Star Bulk, Danaos, Global Ship Lease, Costamare, Scorpio Tankers, International Seaways, Genco, Teekay Tankers,
  DHT, Flex LNG, Expeditors, C.H. Robinson, CMB.Tech, Nordic American Tankers, TORM, SFL, Diana Shipping and Navios Maritime
  Partners.
- A.P. Moller - Maersk's annual reports (ESEF filings).
- IMF PortWatch: daily chokepoint transit calls.
- The World Bank: container port traffic (World Development Indicators).
- FRED: the BLS's producer prices for deep sea freight and water transportation; Brent crude (EIA); American imports of goods
  (Census Bureau and BEA); the CPI.
- Robin Greenwood and Samuel Hanson, 'Waves in Ship Prices and Investment', NBER Working Paper 19246.
