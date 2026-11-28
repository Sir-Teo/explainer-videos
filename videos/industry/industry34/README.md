# Industry, Built: Part 34, Restaurants and Franchising

Part 34 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth of Act VI, *Selling*. It asks: who actually owns a fast-food restaurant, and
who is making the money? It answers with the Forms 10-K for 2025 of McDonald's, Chipotle, Wingstop, Domino's, Yum! Brands
and DoorDash and for fiscal 2026 of Darden; McDonald's 10-Q for the third quarter of 2026; Arcos Dorados's annual report on Form 20-F for 2025; DoorDash's 2020
prospectus; the SEC company facts of twenty-eight restaurant companies and DoorDash; the Census Bureau's retail sales at
restaurants and grocery stores, the BLS's food prices, restaurant jobs and leisure wages, and the federal minimum wage;
and the Works' restaurant and franchisor. The answer: usually a local owner, who paid for the kitchen, hires the crew and
keeps a few cents of each dollar; the brand collects about thirteen cents of every franchised dollar, most of it as rent,
and keeps most of that, on restaurants it did not build; the owner carries the risk of wages, bad years and the apps; and
the brand's fee is limited by its need for the next owner. McDonald's is a landlord with a menu.

It opens on McDonald's 45,356 restaurants at the end of 2025, 95% run by franchisees; on franchisees' $129.7bn of sales
against McDonald's own $26.9bn of revenue; on its $10.4bn of rent, $6.0bn of royalties and $9.7bn of company-restaurant
sales, and an operating income of $12.4bn, 46 cents a dollar; and on revenue that was larger in 2013 than in 2025 while its
operating income rose, as it handed restaurants to franchisees. From there it covers:

- Run it: a franchise for a year. In the Works, a restaurant sells $3.99m a year (McDonald's American franchisees' sales
  over their restaurants) on $1.5m of the owner's money. 31 cents of each dollar buy food and paper, 30 pay crew and
  managers, 12.7 go to the franchisor, 4 to the advertising fund, 10 to other costs and 3 to delivery apps, leaving 9.3
  cents, $371k, a payback of about four years. Sales 10% lower leave $262k; wages a fifth higher $132k (payback 11 years);
  twice the delivery orders $252k; a 15% take $279k. As franchisor of a thousand restaurants choosing its fee, with this
  series' assumptions about franchisees' patience, the ten-year profit peaks near 12.5%;
- one restaurant's dollar: McDonald's company restaurants keep 14.7 cents after food (31.0), labour (30.0) and occupancy
  and other costs (24.3), Chipotle 25.4, Darden 21.7 before marketing and its head office; prime cost from 55 to 62
  cents; Darden's sit-down restaurants against a Chipotle's $3.1m and a Wingstop's $2.0m;
- the contract and the land: McDonald's conventional franchise, generally twenty years; rent ($10.4bn) and royalties
  ($6.0bn), 12.7 cents of franchised sales and 63% of it rent; McDonald's owns 56% of the land and 80% of the buildings in
  the markets it runs directly; $88m of initial fees against $16.5bn; Wingstop's 6% royalty and 5.5% advertising; Arcos
  Dorados's royalty from 6%;
- why franchise: McDonald's keeps 84 cents of each franchised dollar against 15 at its own restaurants; franchisors earn
  19 to 46 cents of operating income per dollar against 4 to 16 at chains that run their own; assets turned 0.45 times at
  McDonald's, about once at Yum and Wingstop, 2.9 at Domino's; Chipotle's 4,042 company-run restaurants and its goal of
  7,000 in the U.S. and Canada; capital, effort, local knowledge and the built-in conflict over discounts;
- the system: Domino's $3.0bn of supply-chain sales against $677m of American franchise royalties and fees, and its
  supply business's 11-cent margin; Wingstop's 73.2% digital sales; McDonald's delivery from about 41,000 restaurants and
  its loyalty plans; the rules as the product;
- an intermission: Americans' spending at restaurants and bars from $198bn (1992) to $1.03 trillion (2025), overtaking
  grocery stores in 2016; prices of food away from home up 39% from the end of 2019 against 34% for food at home and 31%
  for all consumer prices; restaurant jobs from 6.3 million in April 2020 to 12.4 million;
- a third of every dollar: the federal minimum wage at $7.25 since 2009 against average pay in leisure and hospitality
  from $11.49 in 2006 to $23.90 in 2026; labour at 30, 25 and 32 cents a dollar; fixed and variable crew hours; a 20% wage
  rise with prices unchanged ($132k) and with prices raised about 6% to cover it ($273k);
- the app in the middle: DoorDash's 3.17 billion orders worth $102bn, 13.4% kept as revenue; one average order; its
  losses from 2018 ($667m in 2019, $1.4bn in 2022) to profits of $123m (2024) and $935m (2025); the Works' $120k of
  commissions;
- the world's franchisees: Yum's 63,000 restaurants, 97% franchised; Domino's 22,100; Arcos Dorados's 2,520 in Latin
  America; Yum China's $11.8bn of revenue and its 3% licence fee; who keeps more, the brand or its biggest franchisees;
- the landscape, November 2026: twenty-eight companies by revenue and five-year median net margin; profit in dollars; the
  map of the business;
- *Called it?*: DoorDash's 2020 prospectus and its warning of losses against its later profits; and this series' call
  that McDonald's falls short of 50,000 restaurants at the end of 2027 (25% that it makes it); what to watch;
- a landlord with a menu: the answer, and Part 35, travel and hotels.

## Build it

```bash
python -m videos.industry.industry34.compute               # every number, printed
EXPLAINER_TTS=silent python tools/build.py industry34 -q l  # the whole part, silent preview
python tools/build.py industry34                           # 1080p30 with narration
python -m videos.industry.labs 34                          # the lab
python -m pytest tests/industry                            # the Register and the Works (test_franchise.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p34.py`) or comes from the Filing Room: the companies'
accounts (`sec_rest.csv`) and the Census Bureau's and BLS's series (`fred_rest.csv`, with Part 31's `fred_grocery.csv` for
grocery stores).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Whose burger? | McDonald's restaurants; franchisees' sales against its revenue; rent, royalties and margin; 2013 against 2025; the title |
| 1 | Run it: a franchise for a year | The restaurant; its dollar; payback; the dangers; sales as the lever; the franchisor's fee; the lesson |
| 2 | One restaurant's dollar | Three chains' restaurant costs; prime cost; sit-down restaurants; sales per restaurant |
| 3 | The contract and the land | The conventional franchise; rent and royalties; the property; initial fees; other systems |
| 4 | Why franchise | Franchised against company margins; franchisors against operators; asset turns; Chipotle; the reasons |
| 5 | The system | Domino's supply chain; digital orders; loyalty; the rules |
| — | Intermission | Restaurant sales; restaurants against grocers; prices; jobs |
| 6 | A third of every dollar | Wages and the minimum; labour shares; the rota; a wage rise with and without higher prices |
| 7 | The app in the middle | DoorDash's orders; one order; losses to profit; the restaurant's side |
| 8 | The world's franchisees | The systems abroad; master franchisees; brand against franchisee; the map |
| 9 | The landscape, November 2026 | Revenue against margin; profit in dollars; the map |
| 10 | Called it? | DoorDash's prospectus; this series' call; what to watch |
| — | A landlord with a menu | The answer; Part 35, travel and hotels |

## What is computed, and from what

`compute.py` reads the Filing Room and the Register. The Works' restaurant and franchisor are
`explainer/industry/works/franchise.py`. The restaurant sells McDonald's 2025 American franchised sales over its American
franchised restaurants; food and paper and labour are the shares of McDonald's company-operated sales in its 2025 10-K;
the take is franchisees' rent and royalties over franchised sales; the advertising fund (4%), other costs (10%), the
delivery share (15%), the apps' commission (20%), the owner's investment ($1.5m) and the fixed part of labour (60%) are this
series' assumptions, registered with ranges. When sales change, 60% of labour stays where it was. The franchisor starts
with a thousand restaurants; each year four hundred would-be franchisees consider opening one, and each opens if the
payback is within their own patience, lognormal around five years with a log spread of 0.35; the franchisor keeps its fees
less the cost of the property it leases (McDonald's franchised margin against its rent and royalties, 16%) and $60m a year of
overhead. With prices raised to cover a wage rise, revenue rises by the extra labour cost and the fees, advertising and apps
take their shares of it. Margins in the landscape are medians of the last five fiscal years.

## Problems and solutions

**1.** *A franchised restaurant sells $3.0m a year. Food and paper take 31%, labour $900,000, rent and royalties 12.7%,
advertising 4%, other costs 10%, and delivery apps 20% commission on the 15% of sales that come through them. What does the
owner keep, and how long does an investment of $1.5m take to pay back?*

*Solution.* Food $930,000; fees $381,000; advertising $120,000; other $300,000; apps 3.0m x 0.15 x 0.20 = $90,000. Profit:
3,000,000 - 930,000 - 900,000 - 381,000 - 120,000 - 300,000 - 90,000 = $279,000, 9.3 cents a dollar. Payback: 1.5m / 279,000
= 5.4 years.

**2.** *In the same restaurant, 60% of labour is fixed. Sales fall 10%. What happens to the owner's profit?*

*Solution.* Sales are $2.7m. Labour: 540,000 fixed plus 360,000 x 0.9 = 324,000, so $864,000. Every other cost is a share of
sales: 0.31 + 0.127 + 0.04 + 0.10 + 0.03 = 60.7%, $1,638,900. Profit: 2,700,000 - 864,000 - 1,638,900 = $197,100. A 10% fall
in sales cut profit by 29%, because labour hardly fell.

**3.** *McDonald's franchisees paid $10.44bn of rent and $6.02bn of royalties on $129.68bn of sales, and McDonald's
franchised margin was $13.93bn. What share of franchised sales did it collect, how much of it was rent, and what did it keep
of each dollar it collected?*

*Solution.* (10.44 + 6.02) / 129.68 = 12.7 cents of each dollar of sales, of which 10.44 / 16.46 = 63% was rent. It kept
13.93 / 16.46 = 85 cents of each dollar collected (84.2 with the unrounded figures), after the cost of the property it
leases to franchisees.

**4.** *A restaurant pays 30 cents of each dollar in labour. Wages rise 20%. By how much must prices rise to cover the
extra wages, and if the franchisor takes 12.7%, the advertising fund 4% and the apps 3% of every dollar, how much of the
extra revenue is left to pay them?*

*Solution.* The extra labour is 0.30 x 0.20 = 6 cents per dollar of sales, so prices must rise about 6%. Of each extra
dollar, 12.7 + 4 + 3 = 19.7 cents go to the fees and apps, leaving 80.3 cents: a 6% price rise covers only about 80% of the
wage rise, and prices would need to rise about 7.5% to cover it in full (0.06 / 0.803), if customers did not buy less.

**5.** *McDonald's had 43,477 restaurants at the end of 2024 and 45,356 at the end of 2025, and expects to add about 2,100
in 2026. How many must it add in 2027 to reach its target of 50,000? Why does this series give that only a 25% chance?*

*Solution.* 45,356 + 2,100 = 47,456 at the end of 2026, leaving 50,000 - 47,456 = 2,544 to add in 2027: more than the 1,879
it added in 2025 or the 2,100 it expects in 2026. It would need its fastest year yet; the openings depend on franchisees
queuing to build, which depends on how quickly new restaurants pay back.

## Glossary

- **Franchise:** a contract that lets a business owner run a restaurant under a brand's name and system, for fees.
- **Franchisee, franchisor:** the owner who runs the restaurant; the company that owns the brand.
- **Royalty:** a fee charged as a share of a restaurant's sales.
- **Conventional franchise:** McDonald's arrangement in which the company owns or leases the land and building and the
  franchisee pays rent as well as royalties.
- **Master franchisee, developmental licensee:** a company granted the rights to a brand across a whole country or
  region, which may run restaurants itself and sub-franchise others.
- **Average unit volume (AUV):** a restaurant's typical sales in a year.
- **Prime cost:** food and labour, the two largest costs of a restaurant, as a share of sales.
- **Company-operated:** a restaurant run by the brand itself, with its own staff.
- **Delivery app commission:** the share of an order's value a delivery platform charges the restaurant.
- **Payback:** the years of profit needed to recover an investment.

## Lab and interactive

- `python -m videos.industry.labs 34`: the Works' restaurant by sales, wages, delivery and fees; the franchisor's profit by
  its take; McDonald's two margins; franchisors against operators; DoorDash's losses and profits; and this series' call.
- The interactive (course site): run a franchise for a year. Set the restaurant's sales, the franchisor's fee, wages, the
  share of delivery orders and their commission, and the investment; see the restaurant's year, its payback, and the
  franchisor's ten-year profit by its fee.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p34.py`) or the Filing Room
(`explainer/industry/data/SOURCES.md`). The main ones:

- SEC EDGAR: the Forms 10-K for 2025 of McDonald's, Chipotle Mexican Grill, Wingstop, Domino's Pizza, Yum! Brands and
  DoorDash, and for fiscal 2026 of Darden Restaurants; Arcos Dorados's annual report on Form 20-F for 2025; DoorDash's
  prospectus (Form 424B4, December 2020); the company facts of McDonald's, Yum! Brands, Restaurant Brands International,
  Domino's, Chipotle, Starbucks, Darden, Wingstop, Papa John's, Wendy's, Jack in the Box, Shake Shack, Sweetgreen, Cava,
  Texas Roadhouse, Brinker, Dine Brands, Arcos Dorados, Yum China, Dutch Bros, the Cheesecake Factory, Bloomin' Brands,
  Cracker Barrel, Portillo's, El Pollo Loco, First Watch, Krispy Kreme and DoorDash.
- McDonald's Form 10-Q for the third quarter of 2026, for the restaurants it expects to add in 2026 (its 10-K for 2025
  gives the target of 50,000 by the end of 2027 and the loyalty goals).
- FRED: the Census Bureau's retail sales of food services and drinking places and of grocery stores; the BLS's consumer
  prices of food away from home, food at home and all items; employees and average hourly earnings in leisure and
  hospitality and in food services and drinking places; and the federal minimum wage.
