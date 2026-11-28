# Industry, Built: Part 33, The Middlemen

Part 33 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third of Act VI, *Selling*. It asks: if the internet removes the middleman, why are the
middlemen among the largest companies in every country? It answers with the Forms 10-K of McKesson, Cencora, Cardinal Health
and Sysco for fiscal 2026 and of US Foods, W.W. Grainger and Bunge for 2025; Mitsui & Co.'s results for the year to March
2026 and the half-year to September 2026; Chemdex's 1999 prospectus and Ventro's 10-K for 2000; the SEC company facts of
twenty-nine distributors and traders; the Census Bureau's wholesale trade survey and the BLS's wholesale jobs and margin
prices; and the Works' distributor. The answer: because connecting many makers to many buyers costs less through one
middle; because a penny on a dollar is a good business when suppliers' credit pays for the stock; because density lets the
biggest local player deliver for less, so a few firms win each market; because the service is the stock and the truck, not
the order form; and because, where the margin is too thin, the middleman can become an owner.

It opens on McKesson's $403bn, Cencora's $337bn and Cardinal Health's $254bn of revenue in their latest years, $995bn in all
with about $10bn of profit, a cent a dollar; on McKesson's revenue against Johnson & Johnson's $94bn; on McKesson's revenue
and profit since 2010; and on Mitsui & Co.'s ¥14.0 trillion of revenue and ¥834bn of profit, 54% of it from companies it
partly owns. From there it covers:

- Run it: a distributor for a year. In the Works, a drug wholesaler with McKesson's margins sells $5bn when every order is
  filled; 96.4 cents of each dollar go to the makers, 2.1 cents to warehouses, vans and people, 1.5 cents are operating
  profit. It holds 18 days of stock ($226m), is paid in 25 days ($338m) and pays the makers in 56 ($724m): the business needs
  -$160m. Filling 97.7% of order lines it makes $85m after an 8% cost of capital; at 99% (19 days of stock) $88m; filling
  every line (26 days) $82m. Drop-shipping instead keeps 55% of the sales and makes $33m;
- what a wholesaler does: breaks bulk, holds stock, gives credit and delivers; five makers and six shops need 30 accounts
  directly and 11 through a middleman, a thousand makers and ten thousand pharmacies ten million or eleven thousand;
  McKesson's $28bn owed by customers, 21% of it by CVS; Sysco's 333 distribution facilities, US Foods' 250,000 customer
  locations and 6,500 trucks, Grainger's 1.5 million products in stock, McKesson's 27 distribution centers;
- thin margin, fast money: net margins from 0.7 cents (Cardinal) to 15.3 (Fastenal); McKesson's 23 days of stock, 25 of
  receivables and 56 of payables, -8 days of money tied up, against Fastenal's +171; margin times turns from Arrow's 2.0% to
  Fastenal's 24.9%;
- four kinds of middlemen: McKesson keeps 3.6 cents after the goods, Sysco 18, Arrow 11, Grainger 39, Fastenal 45; what the
  customer pays for in each; Avnet's 90 days of stock; Sysco's own brands at 35.4% of its U.S. broadline sales;
- why three: delivery density in a town; the Works' cost of a stop, $41 at a tenth of the pharmacies and $33 at two-fifths;
  the three wholesalers' $995bn against $1,305bn sold by all American drug wholesalers in 2025; CVS's 24% of McKesson's sales
  and Walgreens' 23% of Cencora's;
- an intermission: American merchant wholesalers' sales from $1.8 trillion (1992) to $8.4 trillion (2025); their stocks from
  1.32 months of sales to 1.21; 5.9 million wholesale jobs in 2000 and 6.1 million in 2026; their margin prices against the
  CPI since 2005;
- between giants: Cencora's GLP-1 sales up $8.0bn, which at Cardinal 'did not meaningfully contribute to segment profit';
  McKesson's top ten customers at 73% of revenue, Cencora's top five suppliers at 36% of purchases, Cardinal and CVS's Red Oak
  Sourcing; the national opioid settlement of April 2022, Cardinal's sixth annual payment of $374m and McKesson's $5.7bn still
  owed;
- the trading house: Mitsui's gross profit of ¥1,328bn, equity-method profit of ¥447bn, dividends of ¥179bn and profit of
  ¥834bn; its core operating cash flow by business (metals and mines ¥330bn, energy ¥262bn, lifestyle ¥8bn); energy's cash
  falling from ¥363bn and profit from ¥900bn; Bunge and ADM at a cent or so a dollar;
- the internet and the middleman: Grainger's high-touch business ($14.0bn, 41.7 cents kept, 16.8 cents operating profit)
  against its online endless assortment ($3.6bn, 29.9 and 9.5 cents), with 13 and 29 million products; what the internet
  changed and what it did not;
- the landscape, November 2026: thirty companies by revenue and margin; profit in dollars; the map of the business;
- *Called it?*: Chemdex's 1999 prospectus against Ventro's decision in December 2000 to close the marketplace; and this
  series' call that Mitsui reports at least ¥1,050bn of profit for the year to March 2027 (55%); what to watch;
- still in the middle: the five answers.

## Build it

```bash
python -m videos.industry.industry33.compute               # every number, printed
EXPLAINER_TTS=silent python tools/build.py industry33 -q l  # the whole part, silent preview
python tools/build.py industry33                           # 1080p30 with narration
python -m videos.industry.labs 33                          # the lab
python -m pytest tests/industry                            # the Register and the Works (test_distributor.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p33.py`) or comes from the Filing Room: the companies'
accounts (`sec_middle.csv`, with Part 20's `sec_pharma.csv` for Johnson & Johnson) and the Census Bureau's and BLS's series
(`fred_middle.csv`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | A trillion dollars, a penny at a time | The three drug wholesalers; against a drug maker; McKesson since 2010; Mitsui; the title |
| 1 | Run it: a distributor for a year | The business; its dollar; the money it needs; stock and service; drop-shipping; the lesson |
| 2 | What a wholesaler does | Four jobs; counting links; credit; the networks |
| 3 | Thin margin, fast money | Net margins; days of stock, receivables and payables; margin times turns |
| 4 | Four kinds of middlemen | A dollar at five distributors; why they differ; electronics stock; own brands |
| 5 | Why three | A town's deliveries; the cost of a stop; the market; concentrated customers |
| — | Intermission | Wholesale sales; stocks against sales; jobs; margin prices |
| 6 | Between giants | Pass-through drugs; buying power both ways; the opioid settlements |
| 7 | The trading house | Mitsui's income; its cash by business; an owner's year; the crop traders |
| 8 | The internet and the middleman | Grainger's two businesses; their margins; the reading |
| 9 | The landscape, November 2026 | Revenue against margin; profit in dollars; the map |
| 10 | Called it? | Chemdex; this series' call; what to watch |
| — | Still in the middle | The five answers; Part 34, restaurants and franchising |

## What is computed, and from what

`compute.py` reads the Filing Room and the Register. The Works' distributor is `explainer/industry/works/distributor.py`:
$5bn of sales when every order is filled, with McKesson's fiscal 2026 gross margin (one minus cost of sales over revenue,
3.61%) and costs (gross margin less operating margin, 2.07% of base sales, which do not shrink with sales); it reorders every
14 days with a 14-day lead time, holds half a review period of cycle stock plus z standard deviations of demand over lead
time and review (a line's daily demand varies with a coefficient of 1.0), fills a share Φ(z) of order lines and loses 2% of
sales for each point below 99%; its receivables and payables days are McKesson's (receivables over revenue, payables over
cost of sales, times 365); money tied up is charged, or credited, at 8% a year. Drop-shipping keeps 55% of sales at a 2.0%
margin with costs of 0.8% of base sales. The route has a ten-hour shift, an hour to and from the area, a quarter of an hour a
stop and 20 miles an hour between stops spaced one over the square root of customers served per square mile; a truck and
driver cost $900 a day and a stop delivers $5,000 of goods. Days of stock and payables use cost of sales; receivables use
revenue. Margins in the landscape are medians of the last five fiscal years; Mitsui's yen are at its average rate for the
year, ¥151.09 to the dollar.

## Problems and solutions

**1.** *A distributor's cost of sales is $3.65bn a year and its revenue $3.80bn. It holds $200m of stock, is owed $260m by
customers and owes $560m to suppliers. Find its days of stock, receivables and payables, and the money it needs.*

*Solution.* A day of cost is $10m, a day of revenue $10.4m. Stock: 200 / 10 = 20 days; receivables: 260 / 10.4 = 25 days;
payables: 560 / 10 = 56 days. Money needed: 200 + 260 - 560 = -$100m: suppliers fund the stock, the customers' debts and
$100m more.

**2.** *Five makers sell to six shops. How many accounts are needed if every maker sells to every shop directly, and how many
through one wholesaler? What about 1,000 makers and 10,000 pharmacies?*

*Solution.* Directly: 5 x 6 = 30; through a wholesaler: 5 + 6 = 11. With 1,000 and 10,000: 10,000,000 against 11,000.

**3.** *McKesson kept 1.18 cents of each dollar and turned its assets 4.9 times a year; Fastenal kept 15.35 cents and turned
them 1.62 times. What return on assets did each earn? What margin would McKesson need to match Fastenal at its own turns?*

*Solution.* McKesson: 1.18 x 4.9 = 5.8%; Fastenal: 15.35 x 1.62 = 24.9%. McKesson would need 24.9 / 4.9 = 5.1 cents per
dollar, more than four times what it keeps.

**4.** *A distributor's daily demand for a line has a standard deviation equal to its mean; it reviews every 14 days and the
maker takes 14 days. How many days of stock does it hold with z = 2, and with z = 3? What share of lines does each fill?*

*Solution.* Cycle stock is 14 / 2 = 7 days; safety stock is z x 1.0 x √28 = 5.29z days. With z = 2: 7 + 10.6 = 17.6 days,
filling Φ(2) = 97.7%; with z = 3: 7 + 15.9 = 22.9 days, filling 99.9%. The last 2.2 points of fill cost 5.3 more days of
stock.

**5.** *Mitsui earned ¥574.9bn in the first half of its year to March 2027 and forecasts ¥1,050bn for the year. How much must
it earn in the second half? If more than half its cash comes from mines and energy, why might the second half fall short?*

*Solution.* 1,050 - 574.9 = ¥475.1bn, about 83% of the first half. Its profit now moves with iron ore, coal, oil and gas prices
as well as with the volume it trades, so a fall in commodity prices in the second half would cut it even if its trading
business held steady.

## Glossary

- **Wholesaler, distributor:** a firm that buys from makers in bulk and resells to businesses, holding stock and delivering.
- **Breaking bulk:** selling in small quantities what was bought in large ones.
- **Days of stock, receivables, payables:** inventory over a day's cost of sales; money owed by customers over a day's
  revenue; money owed to suppliers over a day's cost of sales.
- **Negative working capital:** a business whose suppliers' credit exceeds its stock and customers' debts.
- **Fill rate:** the share of order lines delivered from stock.
- **Safety stock:** stock held beyond expected demand, against surprises.
- **Drop-shipping:** having the maker send an order straight to the customer.
- **Group purchasing organization:** a buying group that negotiates for many hospitals or pharmacies together.
- **Trading house (sōgō shōsha):** a Japanese general trading company that trades and invests across many industries.
- **Equity method:** a way of accounting for a part-owned company by taking a share of its profit.

## Lab and interactive

- `python -m videos.industry.labs 33`: the Works' distributor by safety stock, payment terms and drop-shipping; delivery cost
  by local share; distributors' margins, payment days and returns; Mitsui's income; and this series' call.
- The interactive (course site): run a distributor for a year. Choose the safety stock, the maker's lead time, how fast
  customers pay and how slowly you pay the makers, and see the order lines filled, the money tied up and the profit.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p33.py`) or the Filing Room
(`explainer/industry/data/SOURCES.md`). The main ones:

- SEC EDGAR: the Forms 10-K for fiscal 2026 of McKesson, Cencora, Cardinal Health and Sysco and for 2025 of US Foods,
  W.W. Grainger and Bunge Global; Chemdex's prospectus (Form 424B4, July 1999) and Ventro's Form 10-K for 2000; the company
  facts of McKesson, Cencora, Cardinal Health, Henry Schein, Owens & Minor, Sysco, US Foods, Performance Food Group, UNFI,
  Chefs' Warehouse, Arrow, Avnet, TD Synnex, ScanSource, CDW, WESCO, Grainger, Fastenal, MSC Industrial, Applied Industrial,
  Global Industrial, Genuine Parts, Core & Main, Watsco, Pool, SiteOne, Bunge, ADM and the Andersons.
- Mitsui & Co.: consolidated financial results for the year ended 31 March 2026 (1 May 2026) and for the six months ended
  30 September 2026 (4 November 2026).
- FRED: the Census Bureau's monthly wholesale trade (sales, inventories, the inventories-to-sales ratio, drug wholesalers'
  sales); the BLS's employment in wholesale trade, producer price indexes for merchant wholesalers' margins and the CPI.
