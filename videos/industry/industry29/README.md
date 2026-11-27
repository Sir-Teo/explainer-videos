# Industry, Built: Part 29, Rail, Trucks and Parcels

Part 29 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third of Act V, *Moving*. It asks: why is one freight industry a set of regional
monopolies, and the next a market of half a million firms? It answers with the Forms 10-K for 2025 of Union Pacific,
UPS, Old Dominion, Knight-Swift, J.B. Hunt and Aurora; Union Pacific's 10-Q for the third quarter of 2026; FedEx's 10-K
for fiscal 2026; Aurora's 10-K for 2021 and its third-quarter 2026 letter; Yellow's last 10-K and its bankruptcy filing;
the Postal Service's report on Form 10-K for fiscal 2025; the Staggers Rail Act of 1980; FMCSA's register of motor
carriers; the SEC company facts of twenty-five railways, parcel, trucking, logistics and driverless-truck companies;
FRED's freight traffic, price, employment and fuel series; and the Works' lane, trucking market, railway and route. The
answer: every freight business is about filling the trip, and the firm with the most freight in the most places fills
it best. A railway owns its track, so the traffic it adds costs little and nobody can lay a second line beside it; a
truck uses the public road, so anyone can enter and a boom fills the road with trucks; buildings, the part-load
carriers' service centers and the parcel hubs, are the trucker's version of track; and at the door, density decides
everything.

It opens on the Staggers Act's finding that railway earnings were 'the lowest of any transportation mode', against the
four big railways' operating ratios falling from about 75% in 2009 to 60-68% in 2025 while Knight-Swift's and Werner's
rose to 97-100%, and on 533,278 active for-hire interstate trucking firms, 272,151 of them with one truck. From there it
covers:

- Run it: price a lane. In the Works a truck costs $2.05 a mile before fuel and 56 cents of diesel ($3.66 a gallon at
  6.5 miles a gallon): $2.61 a mile driven, loaded or empty. A load from Chicago to Atlanta, 720 miles at J.B. Hunt's
  $2.84 a loaded mile, pays $2,048 against $1,882 of cost; driving home empty, the round trip costs $3,763, a loss of
  $1,716, and the load out would have to pay $5.23 a mile. A load home at $1.60 a mile, found six times in ten after a
  day's wait, cuts the loss to $1,474. A network that runs 13.9% of its miles empty, as Knight-Swift's did, needs about
  $3.04; J.B. Hunt's brokerage works with 126,400 other carriers;
- a mile, a hundredweight, a parcel: 5.4 cents a ton-mile by rail; $1.70 a mile for intermodal over 1,643 miles against
  $2.84 for truckload over 596; Old Dominion's 1,477-pound shipment carried 911 miles for $492 ($33.31 a hundredweight);
  $12.49 a FedEx ground parcel, $13.21 a UPS domestic one, $4.77 a Postal Service shipping piece;
- the railway: Union Pacific's 32,889 route miles, 427bn ton-miles and 29,287 employees; the Works' railway, calibrated
  to its accounts with 40% of costs fixed with the track: 3.4 cents a ton-mile at its density of 13m ton-miles a route
  mile against 5.4 cents of revenue, 20 cents on a branch line of 1m, break-even at 5.3m; rail prices after inflation 32%
  below 1981's in 2001 and 13% below in 2025; 2025 operating ratios of 59.8% to 67.9% against Knight-Swift's 97.1%; the
  Surface Transportation Board's remaining powers;
- half a million trucking firms: the census by fleet size; Knight-Swift's truck in a year ($199,897 before fuel
  surcharges, 83,650 miles, 13.9% empty, a 97.0% operating ratio); truckload margins from 16% (2021) to 3% (2025) and
  Heartland's loss; the truckload price index from 138 (2019) to 203 (2022), 179 (2025) and 231 in October 2026 with
  diesel; the Works' market, where a boom pulls in trucks that arrive as it ends;
- less than a truckload: the service-center network; Old Dominion's 260 centers and 43,762 shipments a day; its tons down
  9.1% and revenue per hundredweight up 3.9% in 2025; its operating ratio against Yellow's before Yellow's Chapter 11
  filing of 6 August 2023; part-load margins of 8-25% against truckload's 0-3%;
- an intermission: rail carloads down and intermodal up; the truck tonnage index; jobs in trucking, couriers and rail;
  e-commerce from $4bn a quarter (1999) to $347bn (2026);
- the parcel networks: 90 lanes or 18 through a hub; UPS's 20.8m parcels a day at $14.50 and FedEx's 17.6m at $16.80;
  their margins; UPS's 385,000 hourly employees and unions; Amazon at 10.6% of UPS's revenue and the planned halving; 93
  buildings closed and 48,000 positions cut; FedEx Freight spun off on 1 June 2026;
- the last mile: the Works' route ($65 an hour, 1.5 minutes a stop, 20 miles an hour, 1.4 parcels a stop): $1.28 a parcel
  in the city, $1.86 in a suburb, $5.80 in the countryside; the Postal Service's 2.4 pieces an address a day against 5.5
  in 2007, 1.8m new addresses, $80.5bn of revenue and a $9.0bn loss;
- the truck without a driver: Aurora's promise of late 2023 and launch in April 2025; 500,000 driverless miles, 20+
  trucks, $3m of revenue and a $901m operating loss; its aim of 1,000 trucks by the end of 2027;
- the landscape, November 2026: twenty-three companies by revenue and margin, and the map of the business;
- *Called it?*: the Staggers Act's purpose; Aurora's dates; and this series' call that Union Pacific completes its purchase
  of Norfolk Southern by 31 December 2027 (40%);
- who owns the road: the five answers.

## Build it

```bash
python -m videos.industry.industry29.compute               # every number, printed
EXPLAINER_TTS=silent python tools/build.py industry29 -q l  # the whole part, silent preview
python tools/build.py industry29                           # 1080p30 with narration
python -m videos.industry.labs 29                          # the lab
python -m pytest tests/industry                            # the Register and the Works (test_freight.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p29.py`) or comes from the Filing Room: the
companies' accounts (`sec_freight.csv`) and FRED's traffic, price, employment, fuel and e-commerce series
(`fred_freight.csv`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The lowest earnings of any mode | The Staggers Act's finding; railways' and truckers' operating ratios; the firms; the title |
| 1 | Run it: price a lane | The truck's cost; the load out; the trip home; a load home; the network; the lesson |
| 2 | A mile, a hundredweight, a parcel | Four units; intermodal against truckload; a part load; a parcel |
| 3 | The railway: a road you own | Union Pacific; density; rail prices since 1981; the four; captive shippers |
| 4 | Half a million trucking firms | The census; a truck's year; margins; prices; the Works' market |
| 5 | Less than a truckload | The network; prices in a bad year; Old Dominion against Yellow; margins |
| — | Intermission | Carloads and containers; truck tonnage; jobs; e-commerce |
| 6 | The parcel networks | Hubs; scale; margins; people; Amazon and FedEx Freight |
| 7 | The last mile | The Works' route; the cost by density; the Postal Service |
| 8 | The truck without a driver | Aurora's promise and launch; where it stands; what it would change |
| 9 | The landscape, November 2026 | Revenue against margin; the map |
| 10 | Called it? | The Staggers Act; Aurora's dates; this series' call |
| — | Who owns the road | The five answers; Part 30, telecoms |

## What is computed, and from what

`compute.py` reads the Filing Room and the Register. The Works' freight is `explainer/industry/works/freight.py`. The
truck costs $2.05 a mile before fuel (this series' assumption, set against Knight-Swift's truckload segment, which earned
$2.71 a mile at a 97.0% operating ratio) plus the EIA's 2025 average retail diesel price over 6.5 miles a gallon. The lane
is 720 miles each way; the rate out is J.B. Hunt's truckload revenue per load over its length of haul; a load home pays
$1.60 a mile with probability 0.6 after a day's wait at $450. The rate a loaded mile needed at an empty share e is the
cost a mile over 1 - e. The market is monthly: demand grows 0.2% a month and runs 15% above trend for twenty months; the
spot rate is $2.40 times (demand over trucks) squared; trucks are added six months after a positive margin (5% of it
times the fleet) and removed at 3% of a negative margin a month. The railway takes Union Pacific's 2025 operating
expenses (revenue times its operating ratio), route miles and revenue ton-miles, with 40% of costs fixed per route mile.
The route costs $65 an hour for eight hours; each stop takes 1.5 minutes plus the drive from the last at 20 miles an
hour, and takes 1.4 parcels. Operating ratios are operating expenses over revenue (one minus operating income over
revenue); BNSF's revenue is its operating expenses plus operating income. Landscape margins are net income over revenue,
the median of the last five fiscal years. Real rail prices are the PPI for line-haul railroads over the CPI, annual
averages, 1981 = 1. The carrier census counts FMCSA's active, interstate, authorized-for-hire records by power units, as
queried on 27 November 2026.

## Problems and solutions

**1.** *A truck costs $2.05 a mile before fuel, gets 6.5 miles a gallon and diesel costs $3.66. What does a mile cost? If
diesel rises to $5.21, as it averaged in 2026, what does it cost, and by how much must the rate a loaded mile rise to keep
a carrier with 13.9% empty miles whole?*

*Solution.* 2.05 + 3.66 / 6.5 = $2.61 a mile. At $5.21, 2.05 + 0.80 = $2.85, 24 cents more. With 13.9% of miles empty the
rate a loaded mile must cover 1 / 0.861 = 1.16 miles driven, so it must rise by 0.24 / 0.861 = 28 cents. A fuel surcharge
tied to the price of diesel does this automatically.

**2.** *A load out pays $2.84 a mile for 720 miles. Driving home empty, what must the load out pay to cover a $2.61 truck?
If a load home paying $1.60 a mile is found with probability p (and a day's wait costs $450 when one is sought), for what p
does seeking it beat driving home empty?*

*Solution.* Empty: 2 × 2.61 = $5.22 a loaded mile out. Seeking a load home adds p × 1.60 × 720 = 1,152p and costs $450, so it
pays when p > 450 / 1,152 = 0.39. The rate home is below the truck's cost, but the truck is driving home anyway.

**3.** *Union Pacific's operating expenses were about $14.7bn in 2025 on 32,889 route miles and 426.9bn ton-miles. If 40% of
costs are fixed with the track, what is the fixed cost a route mile, the variable cost a ton-mile, and the average cost of a
ton-mile at its density and on a branch with 1m ton-miles a mile? At 5.43 cents of revenue a ton-mile, what density breaks
even?*

*Solution.* F = 0.4 × 14.66bn / 32,889 = $178,000 a route mile; v = 0.6 × 14.66bn / 426.9bn = 2.06 cents. Density is 426.9bn /
32,889 = 13.0m, so the average cost is 178,000 / 13.0m + 2.06 = 1.37 + 2.06 = 3.43 cents. At 1m it is 17.8 + 2.06 = 19.9 cents.
Break-even: 178,000 / (5.43 - 2.06 cents) = 5.3m ton-miles a route mile.

**4.** *A driver and van cost $65 an hour for eight hours; each stop takes 1.5 minutes plus the drive from the last at 20
miles an hour, and takes 1.4 parcels. What does a parcel cost to deliver with stops 0.05 miles apart, and 2 miles apart?*

*Solution.* Close: each stop takes 1.5 + 60 × 0.05 / 20 = 1.65 minutes, so 480 / 1.65 = 291 stops and 407 parcels; $520 / 407 =
$1.28. Far: 1.5 + 6 = 7.5 minutes, 64 stops, 90 parcels, $5.80. The cost a parcel rises in proportion to the time between
doors, which is why density decides the last mile.

**5.** *In 2025 Old Dominion's LTL tons fell 9.1% and its revenue per hundredweight rose 3.9%. Roughly what happened to its
LTL revenue? Its total revenue fell from $5.81bn to $5.50bn and its operating ratio rose from 73.4% to 75.2%: what happened
to its operating income, and what share of the lost revenue came out of operating income?*

*Solution.* Revenue ≈ tons × revenue per hundredweight: 0.909 × 1.039 = 0.944, about 5.6% lower. Operating income went from
5.81 × 0.266 = $1.55bn to 5.50 × 0.248 = $1.36bn, $0.18bn lower on $0.32bn less revenue: about three-fifths of the lost revenue.
A network with fixed buildings and pricing power still loses most of its lost revenue as profit when volume falls.

## Glossary

- **Ton-mile:** one ton of freight carried one mile; railways' revenue ton-miles count paying freight.
- **Operating ratio:** operating expenses as a share of revenue; lower is better.
- **Intermodal:** a container or trailer carried partly by train and partly by truck.
- **Truckload, less than truckload (LTL):** a whole trailer for one shipper, or part loads for many, sorted through
  service centers.
- **Hundredweight:** a hundred pounds; LTL carriers quote revenue per hundredweight.
- **Deadhead, empty miles:** miles a truck drives with no paying load.
- **Backhaul:** a load carried on the way home, often at a low rate.
- **Broker:** a firm that finds trucks for shippers' loads without owning the trucks.
- **Fuel surcharge:** an addition to a freight rate that rises and falls with the price of diesel.
- **Captive shipper:** a shipper served by only one railway.
- **Surface Transportation Board (STB):** the federal regulator of railway rates, services, abandonments and mergers.
- **Last mile:** the final leg of a delivery, from a local depot to the door.
- **Universal service:** the Postal Service's duty to serve every address.

## Lab and interactive

- `python -m videos.industry.labs 29`: the Works' lane, the needed rate by empty share and the trucking market; the units;
  the railway's cost by density and the four railways' operating ratios; the census of carriers; truckload and LTL
  margins; Old Dominion against Yellow; the parcel networks; the route and the Postal Service; Aurora; and this series'
  call.
- The interactive (course site): price a lane. Choose the truck's costs, the price of diesel, the distance, the rate out,
  the rate and chance of a load home and a network's share of empty miles, and see the round trip's result and the rate
  a loaded mile needs.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p29.py`) or the Filing Room
(`explainer/industry/data/SOURCES.md`). The main ones:

- SEC EDGAR: the Forms 10-K for 2025 of Union Pacific, United Parcel Service, Old Dominion Freight Line, Knight-Swift, J.B.
  Hunt and Aurora Innovation; Union Pacific's Form 10-Q for the third quarter of 2026; FedEx's Form 10-K for fiscal 2026;
  Aurora's Form 10-K for 2021 and third-quarter 2026 shareholder letter; Yellow Corporation's Form 10-K for 2022 and Form
  8-K of 7 August 2023; the company facts of Union Pacific, BNSF, CSX, Norfolk Southern, CPKC, UPS, FedEx, ZTO Express, J.B.
  Hunt, Hub Group, Knight-Swift, Schneider, Werner, Heartland, Marten, Old Dominion, Saia, XPO, ArcBest, TFI International,
  RXO, Landstar, GXO, Yellow and Aurora.
- The United States Postal Service, report on Form 10-K for fiscal 2025.
- Public Law 96-448, the Staggers Rail Act of 1980 (govinfo).
- FMCSA's Company Census File (data.transportation.gov), counted by this series on 27 November 2026.
- FRED: the BTS's rail carloads and intermodal traffic, the ATA's truck tonnage index and the Transportation Services
  Index; Cass's freight index; the BLS's PPIs for truckload, LTL, line-haul railroads and couriers, employment in truck and
  rail transportation and couriers, and the CPI; the EIA's diesel price; the Census Bureau's e-commerce sales.
