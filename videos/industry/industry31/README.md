# Industry, Built: Part 31, Grocery and Mass Retail

Part 31 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first of Act VI, *Selling*. It asks: how does a business that keeps two or three cents of
every dollar become one of the largest on earth? It answers with the Forms 10-K of Walmart (fiscal 2026), Costco (fiscal
2026), Kroger (fiscal 2025 and fiscal 2020), Albertsons, Dollar General and Target; Part 22's suppliers' disclosures; the SEC
company facts of nineteen grocers, mass merchants, clubs, dollar and convenience chains and Amazon; FRED's grocery sales,
food prices, retail jobs and e-commerce share; and the Works' store. The answer: by accepting the thin margin that
competition sets and never starting the price war that would wipe it out; by selling goods so fast that the suppliers pay
for the stock; by spreading the same lorries, warehouses and buyers over thousands of stores; sometimes by charging at the
door; and by winning town by town, because that is where shoppers, and courts, look.

It opens on Walmart's $713bn of revenue in its year to January 2026, its 2.1 million people and its $21.9bn of profit,
about three cents a dollar, and on its revenue and profit since 2010; and on Costco, whose $5.9bn of membership fees came to
almost two-thirds of its $9.2bn of net profit. From there it covers:

- Run it: a store for a year. In the Works, a supermarket sells $50m a year at Kroger's 23.3% gross margin and keeps $1.15m
  (2.3 cents) after staff (11 cents), rent (3) and other costs (7). Shoppers have rivals nearby: each 1% dearer loses about
  5.7% of sales, so 3% cheaper keeps $1.04m and 3% dearer $1.07m; a 1% price cut needs 6.1% more sales to stand still, a 2%
  cut 12.9%; 20% fewer staff hours keep $0.78m and 20% more $0.21m; sales 5%, 10% and 15% lower keep $0.74m, $0.34m and a
  loss;
- a dollar at the till: Walmart's 75.8 cents of goods, 20.9 of running costs and 4.2 of operating profit; Walmart U.S.'s
  $483bn at 5.2%; gross against net margins from Costco (13% to 3.0%) to Sprouts (39% to 5.9%); Kroger's dollar in a year of
  $2.5bn of charges; this series' reading of why margins are thin;
- turns and the float: goods on Walmart's shelves for 40 days, paid for after 43; days of stock from Costco's 27 to Dollar
  General's 78; suppliers' money in Walmart's ($4.2bn), Costco's ($3.3bn) and Amazon's ($84bn) stock; margin times turns,
  from Costco's 10.4% return on assets to Kroger's 2.0%;
- big boxes and small ones: 939 Costco warehouses, 4,611 Walmart U.S. stores, 2,697 Kroger supermarkets and 20,959 Dollar
  Generals; sales per store from $317m to $2.0m; per square foot, Costco's $2,139 against Walmart U.S.'s $691; three-quarters
  of Americans within five miles of a Dollar General; its 31% gross and 3.5% net margins;
- paying to shop: Costco's paid members from 76.2m to 84.1m; its operating income split into goods and fees, half each; the
  $65 fee, 42.3m Executive members buying 75% of its goods; renewal of 92.3% in the US and Canada; BJ's against Costco;
- an intermission: grocery-store sales from $397bn (2000) to $912bn (2025); food at home up 30% from 2019 against 26% for all
  prices; 3.24 million grocery jobs and 15.5 million in retail; online sales from 1% of retail to 18%;
- the biggest customer: Walmart's share of its suppliers' sales (Clorox 26%, Church & Dwight 23%, General Mills 22%, P&G 16%);
  everyday low prices; own labels;
- the merger that was stopped: Kroger's 2,697 and Albertsons' 2,244 stores; the court's injunction of 10 December 2024 and
  the lawsuits that followed; a town's two supermarkets; this series' reading of why a court cared;
- groceries online: who does the work; the online share's jump in spring 2020 and fall back; Kroger's automated warehouses,
  three closed and one cancelled with $2.5bn of charges; Amazon's revenue passing Walmart's in 2025;
- the landscape, November 2026: nineteen companies by revenue and margin; the map of the business;
- *Called it?*: Kroger's 2021 bet on Ocado's warehouses against its 2026 closures; and this series' call that Costco reports
  more than 87 million paid members at the end of fiscal 2027 (55%); what to watch;
- pennies, turned fast: the five answers.

## Build it

```bash
python -m videos.industry.industry31.compute               # every number, printed
EXPLAINER_TTS=silent python tools/build.py industry31 -q l  # the whole part, silent preview
python tools/build.py industry31                           # 1080p30 with narration
python -m videos.industry.labs 31                          # the lab
python -m pytest tests/industry                            # the Register and the Works (test_store.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p31.py`, with suppliers' rows from `rows_p22.py`) or
comes from the Filing Room: the companies' accounts (`sec_grocery.csv`) and FRED's grocery, price, job and e-commerce
series (`fred_grocery.csv`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Three cents on the dollar | Walmart's size and profit; its revenue since 2010; Costco's fees; the title |
| 1 | Run it: a store for a year | The store; its dollar; price; a price cut; staff; a bad year; the lesson |
| 2 | A dollar at the till | Walmart; Walmart U.S.; gross against net; Kroger; the reading |
| 3 | Turns and the float | Shelf days and payment days; days of stock; the float; margin times turns |
| 4 | Big boxes and small ones | The formats; sales per store; per square foot; Dollar General's reach and money |
| 5 | Paying to shop | Members; goods and fees; Executive members; renewals; other clubs |
| — | Intermission | Grocery sales; food prices; grocery and retail jobs; online's share |
| 6 | The biggest customer | Suppliers' dependence; everyday low prices; own labels |
| 7 | The merger that was stopped | Two chains; the court; a town; the reading |
| 8 | Groceries online | Who does the work; 2020; Kroger's warehouses; Amazon and Walmart |
| 9 | The landscape, November 2026 | Revenue against margin; the map |
| 10 | Called it? | Kroger's bet; this series' call; what to watch |
| — | Pennies, turned fast | The five answers; Part 32, e-commerce |

## What is computed, and from what

`compute.py` reads the Filing Room and the Register. The Works' store is `explainer/industry/works/store.py`: $50m of sales
at price level 1 with Kroger's 2025 gross margin (one minus cost of sales over revenue); volume moves with the price level
to the power -5.7 and with staff hours by 1 - 0.6(1 - s) - 1.5(1 - s)² below normal and 1 + 0.3(s - 1) - (s - 1)² above;
staff cost 11% of base sales times the hours, rent 3% of base sales, other costs 7% of revenue (assumptions). The break-even
volume for a price cut keeps staff and rent fixed. Days of stock and of payables are inventory and accounts payable over a
365th of cost of sales at the latest year-end; return on assets is net income over revenue times revenue over total assets.
Margins are from the latest fiscal year, or the median of the last five for the landscape; fiscal years ending in January
to March are labelled by the previous calendar year. Sales per store and per square foot are company sales over stores and
over square feet (Costco's: warehouses times their average size).

## Problems and solutions

**1.** *A store sells $50m a year at a 23.3% gross margin; staff cost $5.5m, rent $1.5m, and other costs are 7% of sales. What
does it keep? If it cuts prices 1% and staff and rent do not change, how much must volume rise to keep the same profit?*

*Solution.* 50 × (0.233 - 0.07) - 5.5 - 1.5 = 8.15 - 7.0 = $1.15m. After the cut, each dollar of base volume brings 0.99 ×
0.93 - 0.767 = 0.1537 of contribution, so volume must reach (1.15 + 7.0) / (50 × 0.1537) = 1.0605: 6.1% more.

**2.** *Walmart's inventory was $58.9bn, its accounts payable $63.1bn and its cost of sales $535.4bn. How many days of goods did
it hold, how many days did it take to pay, and how much of its stock did suppliers fund?*

*Solution.* A day of cost is 535.4 / 365 = $1.467bn. Inventory: 58.9 / 1.467 = 40 days; payables: 63.1 / 1.467 = 43 days.
Suppliers funded all the stock and $4.2bn more.

**3.** *Costco kept 3.0 cents per dollar and turned its assets 3.4 times; Kroger kept 0.7 cents and turned them 2.96 times. What
return on assets did each earn? What margin would Kroger need to match Costco at its own turns?*

*Solution.* Costco 3.0 × 3.4 = 10.2% (10.4% unrounded); Kroger 0.7 × 2.96 = 2.0%. Kroger would need 10.4 / 2.96 = 3.5 cents per
dollar.

**4.** *Costco's operating income was $11.7bn and its membership fees $5.9bn. If the fees cost almost nothing to collect, what
share of the operating income do they make up? If renewals fell from 90% to 85% of 84 million members, at $65 a year, how
much fee income would be lost?*

*Solution.* 5.9 / 11.7 = 50%. Five points of 84 million is 4.2 million members; at $65, about $0.27bn a year, roughly 2% of
operating income, before counting what those members would have bought.

**5.** *Walmart U.S. sold $483bn from 699 million square feet; Costco sold $297bn from 939 warehouses of about 148,000 square
feet. What does each sell per square foot? Why can Costco sell so much more?*

*Solution.* Walmart U.S.: 483 / 0.699 = $691 per square foot. Costco: 297 / (939 × 0.148) = 297 / 139 = $2,139. Costco sells far
fewer items in bulk on pallets, to members who come to fill a trolley, so each foot of floor turns over much more money.

## Glossary

- **Gross margin:** sales less the cost of the goods sold, as a share of sales.
- **Operating margin, net margin:** what is left after running costs, or after everything, as a share of sales.
- **Days of inventory (stock):** how long goods sit, on average, before they are sold.
- **Days payable:** how long, on average, a retailer takes to pay its suppliers.
- **Float:** cash a business holds because it is paid before it pays.
- **Return on assets:** profit over assets; net margin times asset turnover.
- **Everyday low prices (EDLP):** steady low prices with few promotions; high-low pricing is the opposite.
- **Own label (private label):** goods made for a retailer and sold under its own name.
- **Warehouse club:** a retailer that charges a membership fee and sells a narrow range in bulk.
- **Shrink:** goods lost to theft, damage and spoilage.

## Lab and interactive

- `python -m videos.industry.labs 31`: the Works' store by price, staff and sales; the break-even volume for a price cut;
  margins across the retailers; days of stock, payables and the float; margin times turns; formats; Costco's members and
  fees; and this series' call.
- The interactive (course site): run a store for a year. Set its sales, gross margin, staff costs and its shoppers' price
  sensitivity, then choose its prices and staff hours, and see the year's profit and the most profitable price.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p31.py`; suppliers' Walmart shares in `rows_p22.py`) or the
Filing Room (`explainer/industry/data/SOURCES.md`). The main ones:

- SEC EDGAR: the Forms 10-K of Walmart for fiscal 2026, Costco for fiscal 2026, Kroger for fiscal 2025 and fiscal 2020,
  Albertsons for fiscal 2025, Dollar General for fiscal 2025 and Target; the company facts of Walmart, Costco, Kroger,
  Albertsons, Target, Dollar General, Dollar Tree, BJ's, Sprouts, Weis, Ingles, Grocery Outlet, Casey's, Five Below,
  Ollie's, PriceSmart, Village, Natural Grocers and Amazon.
- FRED: the Census Bureau's retail sales of grocery stores and e-commerce share; the BLS's CPI for food at home and all
  items, and employment in food and beverage stores and in retail trade.
