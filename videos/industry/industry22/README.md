# Industry, Built: Part 22, Consumer Goods

Part 22 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the eighth of Act III, *Making*. It asks: why can a company charge double for soap, for a
hundred years? It answers with Procter & Gamble's annual reports for fiscal 2020 to 2026 and its results releases of July
2024, July 2025, July 2026 and October 2026; the 2025 annual reports of Coca-Cola, Altria, Philip Morris International,
Colgate-Palmolive, Church & Dwight, Kimberly-Clark and Hershey, and those of Clorox, General Mills and Costco for fiscal
2026; the SEC company facts of twenty-five household, personal-care, food, drink and tobacco companies; the BLS's consumer
prices of personal care, food at home and tobacco (via FRED); and the Works' brand. The answer: the product is cheap to
make and the name is not, so half the price is the brand; the brand is kept alive by spending on being remembered every
year, and if the spending stops shoppers drift to the cheaper bottle; that spending is a fixed cost, so the biggest brands
pay least per unit for it and stay the biggest; the retailers push back with their size and their own labels; and when
prices rose for everyone in 2021-2023 the brands raised theirs and most shoppers stayed.

It opens on P&G: its segments (fabric and home care 35% of sales, baby, feminine and family care 24%, beauty 19%, health
care 14%, grooming 8%); $87.0bn of sales in fiscal 2026 against $43.4bn of cost of products sold, 2.01 times; $10.2bn of
advertising; Walmart 16% of its sales, its ten largest customers 43%. From there it covers:

- Run it: cut the advertising? The Works' detergent at $10 against a $5 store label, 500 million bottles a year, a 45%
  share and $100m of advertising whose effect wears off 20% a year. Holding earns $1,250m a year; cutting the advertising
  earns $1,263m in year one and falls to $892m by year eight as share slides from 45% to 30%; cutting the price to $8
  wins 67% of the shelf and earns $1,236m a year. Over eight years at 8%: hold $7.18bn, cut the advertising $6.17bn, cut
  the price $7.10bn. The store label ends with 70%, 55% or 33% of the shelf;
- what a brand is worth: a dollar of P&G's sales (making and shipping 50 cents, advertising 12, selling, research and
  running the company 16, operating profit 23, net profit 18); advertising $10.2bn against research $2.1bn; gross margins
  from Philip Morris International's 67% and Coca-Cola's 62% to Mondelez's 28%, with Coca-Cola Consolidated, a bottler,
  at 40%;
- advertising: P&G's from $7.1bn (fiscal 2018) to $10.2bn (fiscal 2026); the Works' memory, from 500 to 84 in eight years
  without spending; advertising from 13.3% of sales (Colgate) to 3.3% (Philip Morris International); P&G's advertising
  larger than all of Clorox's sales ($7.1bn) or Church & Dwight's ($6.2bn); Trademark Coca-Cola 47% of 33.8 billion unit
  cases;
- the shelf and the buyer: Walmart's share of sales (Clorox 26%, Church & Dwight 23%, General Mills 22%, P&G and
  Kimberly-Clark 16%, Colgate 11%); Hershey's 27% to McLane; Church & Dwight's top four customers 44%; General Mills'
  revenue net of trade promotion and coupons, with $493m of promotions owed; Costco's Kirkland Signature, with higher
  margins than national brands;
- concentrate and bottlers: Coca-Cola's concentrate, 85% of cases and 59% of revenue; gross margins of 62% against the
  bottler's 40%, net margins 27% against 8%; about 2.2 billion servings a day, about 1.6 cents of net profit on each;
- pricing power, tested: P&G's sales growth by volume and price, fiscal 2020-2026, with prices up 9% and volume down 3% in
  fiscal 2023; consumer prices from 2020 to 2023 (food at home +21%, all items +18%, personal care +15%); Hershey's gross
  margin from 47.3% to 33.5% in 2025 despite prices up about 6%; General Mills' North America Retail volume down 1%;
- an intermission: personal care and food at home against all consumer prices since 1990 (0.91 and 0.96); P&G's
  advertising as a share of sales, 9.8% in fiscal 2023 and 11.7% in fiscal 2026; tobacco prices 3.7 times all prices;
- tobacco: Altria's cigarettes, 61.8 billion shipped in 2025 (-10%), -$2.43bn from volume and +$1.68bn from price, a 63%
  operating margin, Marlboro 40.5% of the market and the leader for over 50 years, discount brands 31.8%; the State
  Settlement Agreements and the FDA's marketing rule; Philip Morris International's smoke-free revenue from $12.8bn (37%)
  to $16.9bn (41%);
- where growth comes from: P&G's segments (beauty +7%, fabric and home care +2%); Colgate's emerging markets, 45% of
  sales; Monster from $2.1bn (2012) to $8.3bn (2025); P&G's first quarter of fiscal 2027, +4% with volume +2;
- the landscape, November 2026: twenty-one companies by revenue and median margin; advertising against gross margin;
  and the map of the business;
- *Called it?*: P&G's organic sales guidance (fiscal 2025: 3-5% against 2%; fiscal 2026: 0-4% against 1%; fiscal 2027:
  1-3%, first quarter 4%), what the year needs (about 2.7% a quarter for 3%) and this series' call that fiscal 2027 will
  reach 3% or more (40%);
- double, for a hundred years: the five answers.

## Build it

```bash
python -m videos.industry.industry22.compute               # every number, printed
EXPLAINER_TTS=silent python tools/build.py industry22 -q l  # the whole part, silent preview
python tools/build.py industry22                           # 1080p30 with narration
python -m videos.industry.labs 22                          # the lab
python -m pytest tests/industry                            # the Register and the Works (test_brand.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p22.py`) or comes from the Filing Room: the companies'
accounts (`sec_consumer.csv`) and FRED's consumer and producer prices (`fred_consumer.csv`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Double | P&G's segments; sales against the cost of products; advertising and Walmart; the title |
| 1 | Run it: cut the advertising? | The shelf; profits and shares under three choices; the retailer's side; eight years |
| 2 | What a brand is worth | P&G's dollar; advertising against research; gross margins |
| 3 | Advertising | P&G's advertising; the Works' memory; advertising across the makers; scale; Trademark Coca-Cola |
| 4 | The shelf and the buyer | Walmart's shares; McLane and the top customers; trade promotion; own labels |
| 5 | Concentrate and bottlers | The system; volume against revenue; the two halves' margins; servings a day |
| 6 | Pricing power, tested | P&G's volume and price; consumer prices 2020-2023; Hershey and General Mills |
| — | Intermission | Shelf prices against all prices; P&G's advertising share; tobacco prices |
| 7 | Tobacco: price against volume | Altria's bridge; the margin and the law; Marlboro; PMI's smoke-free products |
| 8 | Where growth comes from | P&G's segments; Colgate's emerging markets; Monster; P&G's latest quarter |
| 9 | The landscape, November 2026 | Revenue against margin; advertising against gross margin; the map |
| 10 | Called it? | P&G's guidance, three years; what the year needs; this series' call |
| — | Double, for a hundred years | The five answers; Part 23, fashion and luxury |

## What is computed, and from what

`compute.py` reads the Filing Room and the Register. The brand is the Works' (`explainer/industry/works/brand.py`):
shoppers choose by a logit in which the brand's utility is 0.05 × sqrt(advertising stock) - 0.45 × price + c and the store
label's -0.45 × its price, with c set so the brand has 45% at the steady stock ($100m a year over a 20% yearly decay, a
stock of 500) and its own price; 500 million units a year; the brand costs $4 a unit; eight years at 8%, starting from the
steady stock. P&G's dollar takes gross margin, advertising and operating margin from the 10-K and puts the rest of the gap
between gross and operating profit under selling, research and running the company. Gross margins are 1 - cost of sales /
revenue in the latest fiscal year; margins in the landscape are profit attributable to the parent over revenue, the median of
2021-2025, by fiscal year (P&G and Clorox end in June, General Mills and Conagra in May, Constellation in February,
Brown-Forman and Smucker in April, Campbell's in August). Revenues below the cost of sales are dropped as narrower tags
(General Mills tags only part of its sales as Revenues in 2019-2024); Kraft Heinz and Smucker tag no total revenue in recent
years and are left out. Consumer prices are annual averages of the BLS's not-seasonally-adjusted indexes (eleven months in
2025: the BLS published no October 2025 CPI). Servings a day are 33.8 billion unit cases × 24 / 365; net profit per serving
divides Coca-Cola's 2025 net income by those servings for the year. What a later quarter needs treats the four quarters of
fiscal 2027 as equal in size.

## Problems and solutions

**1.** *P&G's net sales in fiscal 2026 were $87.0bn and its cost of products sold $43.4bn; advertising was $10.2bn and its
operating margin 22.7%. Split a dollar of sales into making, advertising, operating profit and everything else.*

*Solution.* Making: 43.4 / 87.0 = 49.8 cents; advertising: 10.2 / 87.0 = 11.7 cents; operating profit: 22.7 cents; the
rest, 100 - 49.8 - 11.7 - 22.7 = 15.8 cents, is selling, research and running the company. The products sold for 87.0 /
43.4 = 2.0 times what they cost to make and ship.

**2.** *A brand advertises $100m a year and its advertising stock decays 20% a year. What is its steady stock? If it stops
advertising, what is the stock after one, two and eight years?*

*Solution.* In the steady state the stock S satisfies S = 0.8 S + 100, so S = 100 / 0.2 = 500. Without advertising it
falls by a fifth a year: 400, 320, and after eight years 500 × 0.8^8 = 84. The share follows the memory down, slowly at
first, which is why cutting looks good for a year.

**3.** *In fiscal 2023 P&G's prices rose 9% and its volume fell 3%. Roughly how much did sales from those two alone change,
and what is the implied elasticity of volume to price?*

*Solution.* 1.09 × 0.97 = 1.057: about 5.7% more sales from price and volume (P&G reported net sales up 2%, after a
5-point drag from currency and a 1-point gain from mix). The implied elasticity is about -3 / 9 = -0.33: a 1% price rise
lost about a third of a percent of volume, a sign that most shoppers stayed.

**4.** *Coca-Cola's concentrate operations were 85% of its unit cases and 59% of its revenue; finished-product operations 15%
and 41%. How much more revenue does a case of finished drinks bring Coca-Cola than a case of concentrate?*

*Solution.* Revenue per case is proportional to revenue share over volume share: concentrate 59 / 85 = 0.69, finished 41 /
15 = 2.73. A case Coca-Cola bottles itself brings about 2.73 / 0.69 = 3.9 times the revenue of a case of concentrate, at a
lower gross margin, which is why it leaves most bottling to others.

**5.** *In 2025 Altria's cigarette revenue lost $2,426m to lower volume and gained $1,680m from higher prices; revenue was
$21,204m in 2024. What was the net change, and by how much would prices have had to rise to hold revenue level?*

*Solution.* Net change: -2,426 + 1,680 = -$746m, about -3.5% of $21,204m (Altria reports -3.4%, other items included).
To hold revenue level the price effect would have had to equal $2,426m, about 1.44 times what it was: price is still doing
most of the work against a market shrinking by a tenth a year.

## Glossary

- **Brand:** a name that tells a shopper what to expect, so the shopper need not check.
- **Gross margin:** what is left of a dollar of sales after the cost of making and shipping the product.
- **Advertising stock:** the effect of past advertising still in shoppers' minds, which wears off unless topped up.
- **Store label (own label, private label):** a retailer's own brand, sold beside the makers' brands.
- **Trade promotion:** money a maker gives retailers to promote its products, taken off its revenue.
- **Concentrate:** the syrup base a soft-drinks company sells to bottlers.
- **Bottler:** a company that makes, packages and delivers finished drinks from a brand owner's concentrate.
- **Unit case:** 192 US fluid ounces of finished drink, twenty-four eight-ounce servings.
- **Organic sales:** sales growth leaving out currency and acquisitions and sales of businesses.
- **Volume and price:** the parts of sales growth from selling more units and from charging more for each.
- **Excise tax:** a tax on a particular product, such as cigarettes or alcohol, charged per unit.
- **Smoke-free products:** heated tobacco, e-vapour and nicotine pouches.

## Lab and interactive

- `python -m videos.industry.labs 22`: P&G's double and its dollar; the Run it brand under the three choices and the
  store label; gross margins and advertising across the makers; Walmart's shares; Coca-Cola's two halves; P&G's volume and
  price; consumer prices; Hershey; Altria's bridge and PMI's smoke-free revenue; the landscape; and P&G's forecasts, with
  this series' call.
- The interactive (course site): run a brand. Set the advertising, the price, the store label's price and how fast
  advertising wears off, and see the brand's share and profit year by year and over eight years.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p22.py`) or the Filing Room
(`explainer/industry/data/SOURCES.md`). The main ones:

- SEC EDGAR: Procter & Gamble's Forms 10-K for fiscal 2020 to 2026 and Forms 8-K of 30 July 2024, 29 July 2025, 29 July
  2026 and 22 October 2026; the Forms 10-K 2025 of Coca-Cola, Altria, Philip Morris International, Colgate-Palmolive,
  Church & Dwight, Kimberly-Clark and Hershey; the Forms 10-K for fiscal 2026 of Clorox, General Mills and Costco; the
  company facts of P&G, Unilever, Colgate-Palmolive, Kimberly-Clark, Clorox, Church & Dwight, Estee Lauder, Coca-Cola,
  PepsiCo, Mondelez, Kraft Heinz, General Mills, Hershey, Altria, Philip Morris International, Constellation, Brown-Forman,
  Diageo, AB InBev, Keurig Dr Pepper, Conagra, Smucker, Campbell's, Monster and Coca-Cola Consolidated.
- FRED: the BLS's CPI-U for personal care, tobacco and smoking products, food at home and all items, and its producer price
  index for soap, cleaning compounds and toilet preparations.
