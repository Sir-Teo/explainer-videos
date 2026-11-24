# Industry, Built: Part 7, Sizing a Market

Part 7 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the last of Act I, *Reading an Industry*. It asks: how big is a market, and how would
anyone know? It answers with Uber's and WeWork's prospectuses; three published sizes of American bottled water (the
Census Bureau's survey of manufacturers, Primo Brands' annual report, the Beverage Marketing Corporation's volumes);
the 2022 Economic Census's home centers and nail salons, against Home Depot's and Lowe's accounts; the Bureau of
Labor Statistics' price indexes; the Census Bureau's count of e-commerce and of households; and a century of
American adoption curves. The answer: a market size is a definition plus a count. Two honest numbers for the same
market can differ by a factor of three because they stand at different points of the chain, count different plants
and products, and use different years and money. Count it top-down from what governments count and bottom-up from
units times a price you choose; let the market's structure pick the method; compare only on one definition, and
report a range with the input that decides it. Split every growth rate into price and quantity. Read an addressable
market as ambition, not a forecast. An S-curve's early years cannot tell you its ceiling, and once the curve is full,
the market is what wears out.

It opens on Uber's prospectus of April 2019, which put its market at $12.3 trillion when its revenue was $10.4bn
(0.08% of it; $52.0bn and 0.42% in 2025). From there it covers:

- Run it: size American bottled water from the shelf, from people, gallons each and two shelf prices (about $28bn);
- definition is most of it: the Census's $7.2bn of shipments in 2023 against Primo Brands' $25bn of retail sales,
  3.5 times as much, and the four questions every market size answers (level, plants, products, buyers and year);
- top-down: the Economic Census and the annual survey between, shipments from $5.7bn (2012) to $7.5bn (2024), the
  same deflated by the producer price index, the three-year wait for the concentration tables; and how plants are
  filed by what they mainly make;
- bottom-up: units times price, and what a gallon is worth at the plant door ($0.46) and at the till ($1.60);
- when adding up companies works: the 2022 census's 776 home centers ($258bn, the largest four 98%) against Home
  Depot and Lowe's ($254bn together, within 1.4%), and its 33,066 nail salons, where the largest four made 0.4%;
- three answers, one market: triangulation's three rules, and a sensitivity chart in which the pack price you
  choose decides most of the range ($19bn to $39bn);
- surveys and panels: scanner, household, card and app data, and company surveys, each a window; and e-commerce's
  share of US retail sales, from 0.9% (2000) to 17% (2025), moving the windows;
- price and quantity: dollars as an area; computers' quality-adjusted prices down 92% since 2000 and new vehicles'
  up 25%; bottled water's 30% growth in dollars, 2012-2024, split into 20% price and 8% water;
- addressable markets: Uber's $5.7tn for 'getting around' (every car, bus and train mile in 175 countries), Uber
  Eats' $2.8tn (every restaurant meal, eat-in included, against a $795bn SAM and $7.9bn of orders in 2018), and the
  three rings;
- an intermission: a century of S-curves in American homes;
- how new things spread: Bass's model (1969) on a hundred households, the peak at ln(q/p)/(p+q), and fits to
  microwaves, the internet and smartphones;
- calling the curve early: colour TV fitted on its first quarter tops out at 31% (it reached 96%); curves with
  ceilings of 40%, 60%, 80% and 100% all fit its first four years within a third of a point; across 25 technologies
  the median miss is 12 points;
- when everyone has one: a model of microwave ovens in American homes, first purchases peaking in the mid-1980s and
  replacements 84% of sales by the 2020s, and the rule that a full market sells its number in use divided by its life;
- the Register: what every entry records, and what the Register holds after seven parts;
- *Called it?*: WeWork's $3.0tn and its Chapter 11; the Beverage Marketing Corporation's forecast; and this series'
  call that the Census will report more than $7.5bn of bottled-water shipments for 2026 (65%).

## Build it

```bash
python -m videos.industry.industry7.compute               # every number, printed (instant)
EXPLAINER_TTS=silent python tools/build.py industry7 -q l  # the whole part, silent preview
python tools/build.py industry7                           # 1080p30 with narration
python -m videos.industry.labs 7                          # the lab
python -m pytest tests/industry                           # the Register and the Works (tests/industry/test_diffusion.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p07.py`) or comes from the Filing Room: company
revenue (`sec_annual.csv`), the 2022 Economic Census's concentration tables (`census_conc_2022.csv`), FRED's bottled
water, population, e-commerce and household series (`fred_market.csv`) and price indexes (`fred_prices.csv`), and the
adoption curves (`owid_tech.csv`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Twelve trillion dollars | Uber's TAM against its revenue; WeWork; the title |
| 1 | Run it: size a market | Six facts and your estimate of American bottled water |
| 2 | Definition is most of it | Two published numbers, 3.5 times apart; the four questions |
| 3 | Top-down: the census | Shipments 2012-2024, deflated; the wait; plants filed by what they mainly make |
| 4 | Bottom-up: units times price | Gallons and prices; a gallon at the plant door and at the till |
| 5 | When adding up companies works | Home centers against Home Depot and Lowe's; nail salons |
| 6 | Three answers, one market | Triangulation; the sensitivity of your sum |
| 7 | Surveys and panels | Four windows; e-commerce moves them |
| 8 | Price and quantity | Dollars as an area; computers and cars; bottled water split |
| 9 | Addressable markets | Uber's TAM built up; Uber Eats; the three rings |
| — | Intermission | A century of S-curves; the story so far |
| 10 | How new things spread | Bass's model on a hundred households; the peak; three fits |
| 11 | Calling the curve early | Colour TV; four ceilings through the same dots; 25 technologies |
| 12 | When everyone has one | First purchases and replacements; the rule for a full market |
| 13 | The Register | One entry, field by field; what the Register holds |
| 14 | Called it? | WeWork; a tracker's forecast; this series' call on the Census |
| — | The market, and what comes next | The rules; Act I in seven parts; Act II, oil and gas |

## What is computed, and from what

`compute.py` multiplies the Census Bureau's US population for 2023 by the Beverage Marketing Corporation's gallons a
person, and divides the Census's shipments and Primo Brands' retail figure by the result. It deflates the Census's
shipments by the producer price index for bottled water (2012 = 1) and splits their growth into price and quantity.
It adds Home Depot's and Lowe's revenue for the fiscal years ending early in 2023 and compares the sum with the 2022
Economic Census's home centers. Bass curves are fitted by least squares to each technology in Our World in Data's
table, with the ceiling free, then on the years up to the first at 25% only (the early forecasts), then with the
ceiling held at 40%, 60%, 80% and 100% for colour TV's first years (the fan). The replacement model multiplies the
microwave's fitted curve by the Census's count of US households, counts first purchases as the growth of that stock
and replacements as last year's stock divided by an assumed life of ten years. The sensitivity chart moves each input
of the viewer's sum across the range shown on screen. The models, the life and the ranges are labelled as such.

## Problems and solutions

**1.** *A city has 2 million people. Each buys 60 litres of bottled water a year, two thirds in 24-packs of half-litre
bottles at $6 a pack and the rest at $0.40 a litre. Size the market.*

*Solution.* 2m × 60 = 120m litres. Packs: 80m litres, at $6 for 12 litres = $0.50 a litre, so $40m. The rest: 40m
litres at $0.40 = $16m. The market is about $56m a year at retail. The pack price decides most of it: $5 or $7 a pack
moves the answer by $6.7m either way.

**2.** *A market's sales rose from $100m to $130m over ten years, while its price index rose from 100 to 125. How much
did the quantity sold grow?*

*Solution.* 1.30 / 1.25 = 1.04: the quantity grew 4%. Almost all of the 30% growth in dollars was price. Adding the
two growth rates (30% - 25% = 5%) gives nearly the same answer because the rates are small enough.

**3.** *A product has p = 0.02 and q = 0.38 in Bass's model. In what year after launch do new adopters peak? What if
q is 0.19?*

*Solution.* t* = ln(q/p) / (p + q) = ln(19) / 0.40 = 2.944 / 0.40 = 7.4 years. With q = 0.19: ln(9.5) / 0.21 =
2.251 / 0.21 = 10.7 years. Less copying makes the peak later and flatter.

**4.** *Ninety million homes each have one washing machine, and a machine lasts eleven years. The number of homes grows
by one million a year. About how many machines are sold a year? And if machines lasted nine years?*

*Solution.* 90 / 11 + 1 = 8.2 + 1 = 9.2 million a year. With a nine-year life, 10 + 1 = 11 million: two years less of
life adds about a fifth to the market, with no more homes.

**5.** *A start-up says its addressable market is $400bn: every dollar spent on dry cleaning and laundry in the world.
Its revenue last year was $40m. What two questions would you ask before using the $400bn?*

*Solution.* First, what is the serviceable part: the countries and services it actually offers, and the customers
who could switch to it at its price (most laundry is done at home, unpaid, and much dry cleaning is local and
loyal)? Second, what share of that serviceable market does $40m represent, and how fast has the share grown? A TAM
says how big the prize would be if everyone did it the company's way; the revenue against the serviceable market
says how much of it is being won.

## Glossary

- **Market size:** what buyers pay for a defined product, in a defined place and year, at a defined point of the chain.
- **Top-down:** a size taken from official statistics, then narrowed to the definition.
- **Bottom-up:** a size built from units and prices.
- **Triangulation:** comparing estimates made in different ways, on one definition.
- **Price index:** what a fixed basket costs over time; dividing dollars by it gives quantities.
- **Panel:** a fixed group of shops, households or cardholders whose purchases are recorded.
- **TAM, SAM:** total addressable market (everything that could be done the company's way) and serviceable market (the
  part it actually serves).
- **Bass model:** adoption driven by innovators (p) and imitators (q), up to a ceiling (m).
- **Replacement demand:** sales to people who already own the product, as theirs wear out.

## Lab and interactive

- `python -m videos.industry.labs 7`: Uber's revenue as a share of its TAM; the three bottled-water answers; home
  centers added up; bottled water split into price and quantity; Bass fits and their peaks; the colour TV fan and
  the early forecasts; the replacement model with lives of 8, 10 and 12 years.
- The interactive (course site): size a market. Set the gallons a person, the share in single-serve bottles and two
  shelf prices; compare your sum with the Census's and Primo's figures, and see which input moves it most.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p07.py`) or the Filing Room
(`explainer/industry/data/SOURCES.md`). The main ones:

- Uber Technologies, Form S-1, 11 April 2019 (its market figures cite Euromonitor International and Armstrong &
  Associates), and Forms 10-K.
- The We Company, Form S-1, 14 August 2019, and Form RW, 30 September 2019; WeWork Inc., Form 8-K, 7 November 2023.
- Primo Brands, Form 10-K for 2024.
- Beverage Marketing Corporation, news release on US bottled water, May 2025.
- US Census Bureau: Annual Integrated Economic Survey (bottled water manufacturing, via FRED); 2022 Economic Census,
  concentration of largest firms (released April 2025); Quarterly Retail E-Commerce Sales; Current Population Survey
  households (via FRED).
- US Bureau of Labor Statistics: producer price index for bottled water; consumer price indexes for computers and
  for new vehicles (via FRED).
- Home Depot and Lowe's: Forms 10-K (SEC company facts).
- Our World in Data, technology adoption by US households (Comin and Hobijn, 2004, and others).
- F. M. Bass, 'A New Product Growth for Model Consumer Durables', *Management Science* 15(5), 1969.
