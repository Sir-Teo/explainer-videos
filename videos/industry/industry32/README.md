# Industry, Built: Part 32, E-commerce

Part 32 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second of Act VI, *Selling*. It asks: is selling online a shop, a toll road or an
advertising business? It answers with Amazon's letters to shareholders of 1997 and 2000, its Forms 10-K for 2015 to 2025 and
its 10-Qs for 2025 and 2026; the Forms 10-K for 2025 of eBay, Etsy, Shopify, MercadoLibre, Coupang, Wayfair and Chewy; the
20-Fs of PDD, JD.com, Alibaba and Sea; Wish's prospectus of 2020 and its later 10-Ks; the FTC's release of September 2023;
Amazon's published seller fees; the SEC company facts of twenty-five online companies; the Census Bureau's e-commerce series
and the BLS's warehouse and courier jobs; and the Works' marketplace. The answer: all three. It is a shop, with a shop's thin
margin, when the platform owns the stock; a marketplace when it does not, with a fee bounded by what buyers and sellers can do
instead; a toll road for the firms that sell the tools; and for the biggest, above all an advertising business, held together
by a network of sheds and vans that only scale can pay for.

It opens on Amazon's 1997 letter ('Day 1'; 1.5 million customers; $147.8m of revenue) and its 2000 letter ('Ouch'; shares down
more than 80%), and on its $717bn of revenue in 2025: 41% its own shop, 24% fees from other sellers, then advertising,
subscriptions and AWS, which was 18% of the revenue and 57% of the operating income. From there it covers:

- Run it: a marketplace for a year. In the Works, buyers come for selection, price, speed and uncluttered results, and sellers
  come if what they keep covers their own fixed costs; each side's size depends on the other's. At a 30% take rate, ads of 6% of
  sales and two-day delivery, 60 million buyers and 258,000 sellers spend $37.3bn and the platform keeps $3.9bn of profit.
  Revenue peaks at a take rate near 25% and profit near 30%; at 15% the platform loses $1.0bn, at 40% only 105,000 sellers
  stay. Profit peaks with ads near 4% of sales; at 12% only 27 million buyers remain. One-day delivery costs $9.94 an order
  against $8.14 for two days, but $7.50 at four times the size;
- shop or marketplace: the same $40 order as $40 of a shop's revenue or $12 of a marketplace's fees; Amazon's online stores
  ($77bn to $269bn, 2015-2025) against its third-party seller services ($16bn to $172bn); take rates from Shopify's 3.1% to
  Shopee's 11.4%, eBay's 13.9% and Etsy's 24.2%; JD.com's 78% of revenue from its own stock; Alibaba's RMB344bn of customer
  management revenue; Shopify's $378bn of merchants' sales and $11.6bn of revenue;
- a seller's dollar: a $40 order as $18 of goods, a $6 referral fee (15% on Amazon's list for many categories), $6 of
  fulfilment and other fees, $2.40 of ads and $7.60 left for the seller; Amazon's fee schedule; the FTC's allegation that many
  sellers pay close to 50%, its 2023 suit and Amazon's $2.5bn settlement of a different FTC case in 2025; Amazon's $172bn of
  seller fees and $69bn of ads against $103bn of shipping and $109bn of fulfilment costs;
- getting it there: the path of a parcel; the cost of an order as a fixed network spread over volume; Amazon's shipping costs
  from $11.5bn (2015) to $102.7bn (2025); American warehouse jobs from 0.51 million (2000) to a peak of 1.93 million (2022);
  couriers to 1.1 million; Coupang's 78 million square feet and JD.com's RMB88bn of fulfilment;
- the shop that sells ads: a results page; Amazon's advertising from $12.6bn (2019) to $68.6bn (2025) and up 20% in 2026,
  larger every year than its shops' entire operating income (a loss of $10.6bn in 2022); eBay's $2.0bn, Etsy's $0.88bn of
  services, PDD's 50%; the FTC's and 22 states' August 2026 complaint over reserve prices in Amazon's ad auctions;
- an intermission: e-commerce's share of American retail from 0.6% (1999) to 16.0% in spring 2020 and 17.9% in 2026; its
  sales from $27bn (2000) to $1.25 trillion (2025); the 82% still bought in person;
- the subscription and the cloud: Amazon's subscriptions from $4.5bn to $49.6bn; Chewy's 83.3% of sales from Autoship
  customers and Wayfair's 80.3% of orders from repeat customers; AWS's operating income against the shops' since 2015;
- made in China, sold everywhere: PDD's revenue from $1.9bn (2018) to $62bn (2025) after Temu's launch in September 2022;
  transaction services from 38% to 50% of its revenue; the end of America's de minimis exemption for China (2 May 2025) and
  everywhere (29 August 2025); MercadoLibre's $65bn of goods and $278bn of payments, Shopee's $127bn, Coupang's 24.6 million
  customers, Alibaba's quick commerce up 47%;
- buying customers: the Works' direct brand, whose customers are worth $42, $12 or -$18 when ads cost $30, $60 or $90 a
  customer; marketing from 6.5% of revenue at Chewy to 32% at Etsy; Allbirds' revenue falling from $298m (2022) to $152m
  (2025) against Warby Parker's and FIGS's growth;
- the landscape, November 2026: twenty-three companies by revenue and margin; the map of the business;
- *Called it?*: Wish's prospectus of 2020 against its 68% fall in users and its sale for $162m; and this series' call that
  the Census Bureau's first estimate of e-commerce's share for 2027 Q4 is 19.0% or more (45%); what to watch;
- a shop, a toll road and an ad business: the five answers.

## Build it

```bash
python -m videos.industry.industry32.compute               # every number, printed
EXPLAINER_TTS=silent python tools/build.py industry32 -q l  # the whole part, silent preview
python tools/build.py industry32                           # 1080p30 with narration
python -m videos.industry.labs 32                          # the lab
python -m pytest tests/industry                            # the Register and the Works (test_marketplace.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p32.py`), a table (`explainer/industry/data/tables.py`:
Amazon's revenue by kind, its segment operating income and its shipping costs, 2015-2025) or comes from the Filing Room:
the companies' accounts (`sec_ecom.csv`) and the Census Bureau's and BLS's series (`fred_ecom.csv`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Day 1 | Amazon's 1997 and 2000 letters; its revenue since 2009; its mix; its profit by segment; the title |
| 1 | Run it: a marketplace for a year | The two sides; the settled market; the take rate; who stays; ads; speed; the lesson |
| 2 | Shop or marketplace | One order two ways; Amazon's shop and its sellers; take rates; China and Shopify; three businesses |
| 3 | A seller's dollar | A $40 order; Amazon's fees; the FTC; what the platform pays to deliver |
| 4 | Getting it there | The parcel's path; the cost curve; Amazon's shipping costs; jobs; Coupang and JD.com |
| 5 | The shop that sells ads | A results page; Amazon's ads; ads against the shops' profit; others; the auction case |
| — | Intermission | E-commerce's share; its sales; the rest of retail |
| 6 | The subscription and the cloud | Prime; Autoship and repeat buyers; AWS against the shops; the reading |
| 7 | Made in China, sold everywhere | PDD and Temu; its revenue by kind; the de minimis rule; the world |
| 8 | Buying customers | A direct brand's arithmetic; its payback; marketing shares; three brands; the lesson |
| 9 | The landscape, November 2026 | Revenue against margin; the map |
| 10 | Called it? | Wish; this series' call; what to watch |
| — | A shop, a toll road and an ad business | The five answers; Part 33, the middlemen |

## What is computed, and from what

`compute.py` reads the Filing Room, the Register and the tables. The Works' marketplace is
`explainer/industry/works/marketplace.py`: up to 100 million buyers and a million sellers; a buyer joins with logistic
probability rising with the log of the number of sellers and falling with prices (sellers pass half of any fee above 36% into
them), with each day of delivery beyond two and with ad clutter; orders a buyer rise with selection and speed; a seller joins
if its sales times its margin less fees and ads (55% - 30% - 6%) covers its own fixed costs, lognormal with a median of
$60,000; both sides are solved together by damped iteration. The platform earns its take rate and ads on every dollar, pays
$5 an order plus $2 divided by the promise in days, a $4bn network divided by the promise, 2.5% for payments and $1bn of
overhead. The direct brand earns 45% of a first order of $80 and of $120 a year from the 40% of customers who return, falling
40% a year, less the cost of acquiring them. Take rates are revenue over GMV (Shopify) or as reported. Yuan are converted at
the 20-Fs' convenience rates. Margins in the landscape are medians of the last five fiscal years.

## Problems and solutions

**1.** *eBay's buyers spent $79.6bn in 2025 and its revenue was $11.1bn. What was its take rate? Shopify's merchants sold
$378.4bn through it and its revenue was $11.6bn: what was Shopify's? Why can the two be so different?*

*Solution.* eBay: 11.1 / 79.6 = 13.9%. Shopify: 11.6 / 378.4 = 3.1%. eBay runs the market where buyers find the goods and
charges the sellers for those buyers; Shopify sells software and payments to shops that find their own buyers, so it can
charge only for the tools.

**2.** *A seller lists a $40 item. The goods cost $18; the referral fee is 15%; fulfilment and other fees are another 15%;
it spends 6% of the price on ads. What does it keep? If the referral fee rose to 17%, how much more must it charge to keep the
same amount, assuming the other fees stay proportional to the price?*

*Solution.* 40 - 18 - 6 - 6 - 2.40 = $7.60. With fees and ads at 38% of the price, the seller keeps 0.62 p - 18 = 7.60, so
p = 25.6 / 0.62 = $41.29: about 3% more.

**3.** *A delivery network costs $4bn a year divided by the promised days, plus $5 and $2 divided by the days for each
order. What does an order cost with a one-day promise at 1 billion orders a year, and at 4 billion? At what volume does
one-day delivery cost the same as two-day delivery does at 1 billion orders?*

*Solution.* At 1bn: 5 + 2 + 4 = $11. At 4bn: 5 + 2 + 1 = $8. Two days at 1bn: 5 + 1 + 2 = $8. One day costs $8 when
5 + 2 + 4 / n = 8, n = 4 billion orders: four times the volume.

**4.** *A direct brand pays $60 in ads for a customer whose first order is $80; it keeps 45% of sales; 40% of customers buy
again each year, spending $120, and the number still buying falls by 60% a year. What is a customer worth over a lifetime?
What is the most it can pay for a customer and still break even?*

*Solution.* First order: 0.45 x 80 = $36. Later years: 0.45 x 120 x (0.4 + 0.16 + 0.064 + ...) = 54 x 0.4 / 0.6 = $36. Total
$72, less $60: $12. It can pay up to $72 a customer and break even.

**5.** *Amazon's advertising revenue was $68.6bn in 2025 and the operating income of its North America and International
segments together $34.4bn. If Amazon's ads cost 20 cents a dollar to deliver, and nothing else changed, what would its shops
have earned without them? Why is this only a reading, not a fact?*

*Solution.* 34.4 - 0.8 x 68.6 = 34.4 - 54.9 = -$20.5bn: a loss. It is only a reading because Amazon does not report what its
advertising costs or earns, some of its ads run on Prime Video and other services, and without ads sellers' prices and
Amazon's other choices would change.

## Glossary

- **GMV (gross merchandise value):** what buyers spend on a platform, before returns, fees or costs.
- **Take rate:** a platform's revenue as a share of GMV.
- **First party, third party:** goods a platform buys and sells itself, against goods other sellers sell on its site.
- **Fulfilment:** storing, picking, packing and shipping orders; a fulfilment centre is the warehouse that does it.
- **The last mile:** the final delivery from a local depot to the door.
- **Sponsored product:** a listing a seller pays to place in search results, usually priced by the click in an auction.
- **Reserve price:** the lowest bid an auction will accept.
- **De minimis:** the exemption from duty for low-value imports.
- **Customer acquisition cost (CAC):** what it costs, mostly in advertising, to win a customer.
- **Lifetime value:** a customer's contribution over all their purchases, less what it cost to win them.

## Lab and interactive

- `python -m videos.industry.labs 32`: the Works' marketplace by take rate, ads and delivery; the cost of an order; take
  rates; a seller's dollar; Amazon's advertising against its shops' profit; e-commerce's share; a direct brand's customers;
  and this series' call.
- The interactive (course site): run a marketplace for a year. Set the take rate, the ads sold to sellers, the delivery
  promise and the size of the market, and see buyers, sellers, GMV and profit answer.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p32.py`), the tables (`explainer/industry/data/tables.py`) or
the Filing Room (`explainer/industry/data/SOURCES.md`). The main ones:

- SEC EDGAR: Amazon's letters to shareholders for 1997 (reprinted with the 2008 letter) and 2000, its Forms 10-K for 2017,
  2019, 2020, 2021, 2023 and 2025 and its 10-Qs for the third quarters of 2025 and 2026; the Forms 10-K for 2025 of eBay,
  Etsy, Shopify, MercadoLibre, Coupang and Wayfair and Chewy's for fiscal 2025; the Forms 20-F for 2025 of PDD Holdings,
  JD.com and Sea and Alibaba's for fiscal 2026; ContextLogic's (Wish's) Form S-1 of November 2020 and Forms 10-K for 2022 and
  2024; the company facts of twenty-five online retailers, marketplaces, tools, delivery platforms and direct brands.
- The Federal Trade Commission's press release of 26 September 2023; Amazon's 'Pricing' page for sellers in its US store.
- FRED: the Census Bureau's quarterly e-commerce sales and share of retail; the BLS's employment in warehousing and storage
  and in couriers and messengers.
