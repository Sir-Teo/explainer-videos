# Industry, Built: Part 10, Farming and Food

Part 10 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third of Act II, *Out of the Ground*. It asks: why do farmers grow ever more, and
keep so little of what we pay? It answers with the US Department of Agriculture's food dollar (the new model released
in November 2026), its costs and returns for corn, soybeans and wheat, and its farm income and wealth statistics since
1910; the Food and Agriculture Organization's yields and food balances (via Our World in Data); the IMF's and the BLS's
food prices; the Nobel Foundation on Borlaug; USDA on farm numbers and beef packers; the ICCO on cocoa; the 10-K
accounts of fifteen companies from CF Industries to Kroger, and Cargill's annual report; and the Works' farm. The
answer: a farmer sells a commodity into a market of millions, so each one takes the price. Every new method raises
output, the price falls, and the gain passes to the people who eat (Cochrane's treadmill). The companies around the farm
keep more where something is hard to copy, a patent, a plant or a brand. Governments pay farmers in bad years. And the
land keeps the good years.

It opens on Norman Borlaug's dwarf wheat. Mexico grew all its own wheat by 1956, the new wheat went to India and
Pakistan from the mid-1960s, Borlaug won the Nobel Peace Prize in 1970, and wheat yields have since multiplied 3.4 to
4.2 times. Yet American farms got 12.6 cents of each food dollar in 2025. From there it covers:

- Run it: a 296-acre corn farm through three real seasons (2012, 2014, 2020), choosing how much to sell ahead at
  planting and whether to store until June. Over the three seasons, selling nothing ahead and storing did best (+$191 an
  acre) and selling everything ahead worst (-$95), but no rule wins every year;
- an acre's arithmetic: in 2025 an acre of corn brought in $782 and cost $901, with fertilizer ($172), land ($190) and
  machinery ($171) the biggest items. It broke even at $2.30 a bushel on cash costs and $4.55 on all costs, against a
  $3.93 price. Corn fell short of all its costs in 19 of 30 years, soybeans in 12 of 29 and wheat in 26 of 28;
- where the food dollar goes: restaurants 35.5 cents, processing 17.2, food shops 14.3, wholesale 6.3; the work done on
  farms about 6. The farm share was 18.9 cents at home and 7.5 away from home. The wheat in a one-pound loaf (Kansas
  Wheat: 70 loaves a bushel) cost 9.6 cents in September 2026, about 5% of the loaf's $1.83;
- the treadmill: Cochrane's model animated, then the record. US corn yields are about seven times their level before
  1935, the real price of corn has not risen, and US farms fell from 6.81 million (1935) to 1.87 million (2025);
- seed, fertilizer and machines: a few sellers on one side and a few buyers on the other. Seed rose from $27 to $113 an
  acre and fertilizer from $51 to $172 (1996-2025), and CF Industries' profit went from $0.32bn in 2020 to $3.35bn in 2022.
  Average margins 2021-2025: CF 21.6%, Deere 13.7%, Mosaic 9.3%, Corteva 6.7%, against 2.6% for growing corn;
- the grain traders: the route from Iowa down the Mississippi and through Panama to Asia. ADM, Bunge, Cargill
  ($154bn) and Louis Dreyfus; ADM's 2.7% average margin; the soybean crush margin, about $30 a tonne on average and $169
  in September 2026;
- selling a crop before it grows: a futures contract (5,000 bushels), a hedge in 2014, and thirty years of the corn
  price;
- meat: four packers buy 85% of fed cattle (36% in 1980); ground beef at a record $6.92 a pound (August 2026); Tyson's
  margins from 6% to a loss and back to 1%;
- an intermission: US net farm income in today's dollars since 1929, from the Depression to 2022's record;
- from a bushel to a box: the margin 'smile' from field to shop; Walmart's thin margin on huge sales; Kraft Heinz's
  2025 loss of $5.8bn;
- the state on the farm: US government payments since 1933 ($57bn in today's dollars in 2020; $47bn forecast for
  2026); India's rice export ban of July 2023 and the world price ($492, then $629, now $466 a tonne);
- land: farm real estate worth $3.7 trillion in 2026 (about $4,100 an acre), half its real value lost from 1980 to
  1991; since 1990, returns on farm assets of 2.5% a year from farming and 4.6% from rising land values; Ricardo's rent
  on the corn acre ($68 left for land that rents for $190);
- cocoa, and the world's plate: Côte d'Ivoire and Ghana's 57% of cocoa, an 11% smaller crop, and a price that went
  from $2,369 (2022) to $10,710 (January 2025); Hershey's and Mondelez's margins squeezed; food supply per person since
  1961 (world 2,184 to 3,013 kilocalories a day);
- the landscape, November 2026: the chain's listed companies by size and margin, the private and foreign giants, and
  what to watch;
- *Called it?*: Ehrlich's *Population Bomb* (1968) against the record, and this series' call that the farm share of
  2026's food dollar will be higher than 2025's in USDA's next release (70%).

## Build it

```bash
python -m videos.industry.industry10.compute               # every number, printed
EXPLAINER_TTS=silent python tools/build.py industry10 -q l  # the whole part, silent preview
python tools/build.py industry10                           # 1080p30 with narration
python -m videos.industry.labs 10                          # the lab
python -m pytest tests/industry                            # the Register and the Works (tests/industry/test_farm.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p10.py`) or comes from the Filing Room: USDA's food
dollar (`ers_food_dollar.csv`), costs and returns (`ers_costs.csv`) and farm income (`ers_farm_income.csv`); FAO's
yields and food supply via Our World in Data (`owid_ag.csv`); food and fertilizer prices via FRED (`fred_food.csv`);
and the companies' 10-Ks (`sec_annual.csv`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The dwarf wheat | Borlaug in Mexico; wheat yields since 1961; the farm's 12.6 cents; the title |
| 1 | Run it: three seasons | A corn farm in 2012, 2014 and 2020; forward sales and storage |
| 2 | An acre's arithmetic | USDA's 2025 corn acre; who is paid last; thirty years of returns |
| 3 | Where the food dollar goes | A dollar in 100 cents; at home and away; a loaf of bread |
| 4 | The treadmill | Cochrane's model; corn yields since 1866; farms in 1935 and 2025 |
| 5 | Seed, fertilizer and machines | Few sellers, few buyers; seed and fertilizer per acre; CF; margins |
| 6 | The grain traders | The route to Asia; the ABCD; ADM's margin; the soybean crush |
| 7 | Selling a crop before it grows | A futures contract and a hedge; thirty years of corn |
| 8 | Meat | From feed to packer; four packers' share; beef prices; Tyson |
| — | Intermission | A century of farm income; the story so far |
| 9 | From a bushel to a box | The margin smile; Walmart; Kraft Heinz |
| 10 | The state on the farm | Government payments since 1933; India's rice ban |
| 11 | Land: who keeps the gain | Land values; returns from farming and from land; Ricardo |
| 12 | Cocoa, and the world's plate | Cocoa's crop and price; the chocolate makers; food per person |
| 13 | The landscape, November 2026 | The companies; what to watch |
| 14 | Called it? | Ehrlich, 1968; this series' call on the farm share |
| — | The harvest, and what comes next | The answers; Part 11, heavy materials |

## What is computed, and from what

`compute.py` reads USDA's food dollar (the Ag-FEDS model, 2007-2025) for the farm share and the thirteen industry groups;
its costs and returns for corn, soybeans and wheat (US totals, 1996-2025); and its farm income statistics, deflated with
ERS's GDP deflator (2026 = 100), from 1929. The Run it seasons take each year's yield, cost and harvest price from USDA.
The expected yield is the trend of the ten years before, and the planting and June prices are the harvest price scaled
by the IMF's monthly maize price. Storage costs 4 cents a bushel a month, an assumption. The real price of corn is the
IMF's maize price, converted at 39.37 bushels a tonne and deflated by the CPI; the CPI has no October 2025, so that
year averages the months published. The crush margin uses the IMF's world prices of soybeans, meal and oil with CME's
standard yields (44 lb of meal and 11 lb of oil a bushel). The wheat in a loaf divides the IMF's wheat price per bushel
by Kansas Wheat's 70 loaves. Company margins are net income over revenue from the 10-Ks, averaged over 2021-2025.

## Problems and solutions

**1.** *An acre of corn yields 200 bushels, sold at $4.20. Operating costs are $460; machinery, labour and overheads $260;
and the land rents for $200. What is the acre's profit, its break-even price on cash costs and on all costs, and the
most the farmer could have paid in rent and broken even?*

*Solution.* Revenue is 200 × 4.20 = $840. All costs are 460 + 260 + 200 = $920, so the acre loses $80. Break-even on cash
costs: 460 / 200 = $2.30; on all costs: 920 / 200 = $4.60. The most the land could earn is 840 − 460 − 260 = $120, so a
rent of $200 is $80 too high this year. The farmer still plants, because the price covers the cash costs.

**2.** *A farmer expects 180 bushels an acre and sells it all forward in spring at $4.80. (a) The crop is normal and the
harvest price $3.90. (b) A drought cuts the crop to 120 bushels and the harvest price rises to $6.00. What does the acre
bring in each case, with and without the forward sale?*

*Solution.* (a) Hedged: 180 × 4.80 = $864; unhedged: 180 × 3.90 = $702. (b) Hedged: the farmer must buy 60 bushels to
fill the contract, so 180 × 4.80 − 60 × 6.00 = $504; unhedged: 120 × 6.00 = $720. The hedge protects against the price,
not the weather, which is why revenue insurance exists.

**3.** *A new seed raises a crop's total output by 12%. Demand has an elasticity of −0.4. By how much does the price fall,
and what happens to farmers' total revenue?*

*Solution.* The price multiple is 1.12^(1 / −0.4) = 1.12^−2.5 = 0.753, a fall of about 25%. Revenue is 1.12 × 0.753 =
0.843 of what it was: farmers as a whole earn 16% less from a larger crop. The gain goes to consumers.

**4.** *Wheat sells for $7.00 a bushel and a bushel makes about 70 one-pound loaves. A loaf costs $1.90. What share of
the price is the wheat, and how much would the loaf rise if wheat doubled with nothing else changing?*

*Solution.* The wheat in a loaf is 7.00 / 70 = 10 cents, about 5% of $1.90. Doubling wheat adds 10 cents, to $2.00, a
rise of about 5%.

**5.** *Soybeans cost $430 a tonne, soybean meal $300 and soybean oil $1,200. A tonne of beans gives 44/60 of a tonne of
meal and 11/60 of a tonne of oil. What is the crusher's margin a tonne?*

*Solution.* Meal: 0.733 × 300 = $220. Oil: 0.183 × 1,200 = $220. Together $440, less $430 of beans: a margin of about
$10 a tonne, a little over 2% of the price. A crusher cares about the gap, not the level, of the prices.

## Glossary

- **Price taker:** a seller too small to change the market price by selling more or less.
- **Food dollar:** USDA's breakdown of a dollar spent on food into the industries whose work it pays for.
- **Farm share:** the part of the food dollar paid to farms for their products.
- **Break-even price:** the price at which revenue just covers a set of costs.
- **Forward sale, hedge:** selling a crop before harvest at a price agreed today.
- **Futures contract:** an exchange-traded promise to deliver a standard amount at a set price and date.
- **Basis:** the difference between the local cash price and the futures price.
- **Crush margin:** the value of soybean meal and oil from a tonne of beans, less the beans.
- **Treadmill:** Cochrane's name for the way new farm methods lower prices and push farmers to keep adopting.
- **Rent (Ricardian):** what is left for land after every other cost.
- **Concentration (CR4):** the share of a market held by its four largest firms.

## Lab and interactive

- `python -m videos.industry.labs 10`: the food dollar; the corn acre and its break-evens; the three seasons; the
  treadmill; the loaf; the crush; the companies' margins; farm income, government payments and the returns from land;
  this series' call.
- The interactive (course site): Cochrane's treadmill. Set the extra output from a new method, the demand elasticity and
  the speed of adoption, and see the price and the margins of early adopters and laggards over thirty years.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p10.py`) or the Filing Room
(`explainer/industry/data/SOURCES.md`). The main ones:

- USDA Economic Research Service: Food Dollar Series (November 2026); Commodity Costs and Returns; Farm Income and Wealth
  Statistics (3 September 2026); Amber Waves (January 2024) on meatpacking; Ag and Food Statistics: Charting the
  Essentials.
- USDA National Agricultural Statistics Service, Farms and Land in Farms 2025 Summary (February 2026).
- FAO food balances and yields via Our World in Data.
- IMF primary commodity prices and BLS average prices via FRED.
- The Nobel Foundation, 'Norman Borlaug - Facts'.
- International Cocoa Organization, Quarterly Bulletin of Cocoa Statistics, Vol. LI No. 1 (February 2025).
- CME Group, corn futures specifications and the Soybean Crush Reference Guide.
- Kansas Wheat, 'What does a bushel of wheat mean to me?'.
- SEC EDGAR: Forms 10-K of CF Industries, Deere, Mosaic, Corteva, ADM, Bunge, Tyson Foods, Pilgrim's Pride, Hormel,
  PepsiCo, Mondelez, General Mills, Kraft Heinz, Hershey, Kroger, Walmart and Costco; Cargill, 2025 Annual Report.
- Willard W. Cochrane, *Farm Prices: Myth and Reality* (1958); David Ricardo, *On the Principles of Political Economy
  and Taxation* (1817); Paul R. Ehrlich, *The Population Bomb* (1968).
