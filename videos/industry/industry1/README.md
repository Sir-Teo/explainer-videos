# Industry, Built: Part 1, Where the Money Goes

Part 1 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first of Act I, *Reading an Industry*. It asks: when you pay for something, who
gets the money, and why them? It answers for a single phone, the 256GB iPhone 17 Pro at $1,099, following its price
to the companies that make it and checking each number against their own reports. The answer: the money goes to
whoever is hardest to replace, and that can change in a year. In 2026 it did: memory became the scarce link.

It opens in 2007 with Greg Linden, Kenneth Kraemer and Jason Dedrick's study of a $299 iPod. Of the $299,
assembly in China came to $3.70, of which the assembler kept an estimated 11 cents; the trade statistics booked the
whole factory value as a Chinese export. From there it covers:

- the five questions every part asks (what is sold, how it is made, where the dollar goes, why it stays, what moves
  it), and a guess: split $1,099 into five piles;
- inside the phone: six layers and the companies that make each (Corning, Samsung Display, LG Display, Apple and
  TSMC, Samsung, SK hynix, Micron, Kioxia, Qualcomm, Broadcom, Murata, Sony, Largan, LG Innotek, Foxconn,
  Luxshare, Tata Electronics), in at least six economies;
- what the parts cost: about $520 (published estimates $450 to $570), split the way teardowns split it; what a
  teardown cannot see; what one more phone costs (about $590) against what designing the next one costs (Apple's
  R&D was $45.8bn in fiscal 2026);
- value added: why adding up sales along a chain counts the same dollar again at every link, and why value added sums
  to the price (and, over a country, to GDP);
- the Dollar of one phone: about $66 to the shop or carrier, $520 to the parts, $30 to assembly, $40 to shipping,
  warranty and licences, $154 to Apple's research and selling, $45 to tax, and about $244 of profit to Apple (range
  $148 to $357), checked against Apple's company-wide 28 cents of profit per dollar of sales;
- the carrier's side: in 2025 T-Mobile sold phones for $16.0bn that cost it $21.3bn, and earned $71.3bn on its
  plans; for a carrier the phone is the bait and the monthly bill the business;
- why the profit sits where it does: the margins each link reports, from Foxconn's 6% gross to Apple's services'
  76%; the links that are hardest to replace keep the most; and the customer fights back by making its own chips;
- after the sale: Apple's services were a quarter of its fiscal 2026 sales and 40% of its gross profit ($94bn),
  about $38 of gross profit per active device a year, Google's estimated $20bn in 2022 among it;
- three phones, three businesses: about $859 of revenue and $316 of gross profit per iPhone, against $157 and $17 per
  Xiaomi phone and $72 and $14 per Transsion phone;
- an intermission: iPhone sales by fiscal year, 2008 to 2026;
- made where?: the iPhone 3G's $178.96 booked as a Chinese import, of which $6.50 was Chinese value added; the move of
  assembly to India and the 2025 tariffs; what moves in the statistics (about $590 a phone) against what moves in
  value added (about $30);
- memory's boom and bust: Micron's gross margin from 20% (2016) to 59% (2018) to -9% (2023) to 81% (2026), and
  why a commodity made in a few huge factories cycles;
- the 2026 memory shock: memory prices up five- to sevenfold; memory from a tenth of an iPhone Pro's parts to a third;
  Micron's gross margin from 40% to 81%; the memory makers' gross profit per Pro phone from about $21 to about $197;
  Samsung's chip division earning 106.5 trillion won in a quarter while its phone division lost money; shipments down
  a fifth;
- who pays for the memory: by storage size, Apple's price rises match the memory-cost rises on the 1TB and 2TB models
  and fall short on the smaller ones; Apple's products margin still rose in fiscal 2026;
- the landscape as of November 2026, link by link and region by region;
- *Called it?*: Steve Ballmer's "no chance" (2007), and this series' first call: 2026 shipments below 1.15 billion.

## Build it

```bash
python -m videos.industry.industry1.compute               # every number, printed (instant)
EXPLAINER_TTS=silent python tools/build.py industry1 -q l  # the whole part, silent preview
python tools/build.py industry1                           # 1080p30 with narration
python -m videos.industry.labs 1                          # the lab
python -m pytest tests/industry                           # the chain arithmetic and the Register
```

Every figure is a row of the Register (`explainer/industry/data/rows_p01.py`), with its definition, its source, the
date it describes and the date it was checked; `compute.py` does arithmetic on those rows and nothing else.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | A $299 question | The iPod study, 2007; the title; the five questions |
| 1 | Guess the split | The iPhone 17 Pro at $1,099; five piles to guess |
| 2 | Inside the phone | Six layers, their makers, six economies |
| 3 | What the parts cost | The bill of materials; one more phone against the next design; what a teardown misses |
| 4 | Counting the money once | Sales double-count; value added sums to the price |
| 5 | Follow the dollar | The Dollar of one phone; the guess checked |
| 6 | The carrier's side of the deal | T-Mobile sells phones below cost and earns on the plan; what that means for the shop's slice |
| 7 | Why the profit sits where it does | Margins from filings; the hard-to-replace links; designing a link away |
| 8 | After the sale | Apple's services: a quarter of its sales, 40% of its gross profit; the App Store, Google's payment |
| 9 | Three phones, three businesses | 2025 shares; revenue and gross profit per phone: Apple, Xiaomi, Transsion |
| — | Intermission | iPhone sales by fiscal year, 2008-2026; the story so far |
| 10 | Made where? | Gross trade against value added; India and the tariffs |
| 11 | Memory's boom and bust | Micron's gross margin, fiscal 2016-2026; why commodity memory cycles |
| 12 | 2026: the memory shock | AI memory; the bill of a Pro; the memory makers' margins; Samsung's two halves; the market |
| 13 | Who pays for the memory? | Price rises against memory-cost rises by storage size; Apple's margin |
| 14 | The landscape, November 2026 | The companies in each link, by region |
| 15 | Called it? | Ballmer, 2007; this series' call for 2026 |
| — | The five questions, answered | The answers for the phone; next, Part 2 |

## What is computed, and from what

`compute.py` builds the Dollar with `explainer.industry.works.chain.dollar`: the retail price, Apple's share of sales
through indirect channels (60%, its 10-K) at an assumed channel margin (10%, range 3% to 15%), the parts (central
$520, range $450 to $570), assembly ($30, range $20 to $45) and other costs of sales ($40, range $25 to $60), Apple's
operating expenses as a share of revenue (14.9%, fiscal 2025) and its tax rate (15.6%). The profit range takes all
the favourable ends together and all the unfavourable ends together. The split of the parts by category is this
series' estimate from teardown houses' published shares, with memory pinned to TrendForce's 10% and the WSJ's $52.

The 2026 phone takes TrendForce's +38% on the parts and 34% memory share (memory $244); the WSJ's DRAM and flash
estimates give a second case ($196). The tier analysis takes DRAM at $39 then $145 per phone (WSJ) and flash per
gigabyte from the WSJ's 256GB figures ($13 then $51) for the low case and from Counterpoint's 1TB figure ($250) for the
high case. Per-phone revenue divides segment revenue by units: Apple's iPhone sales for fiscal 2025 by IDC's calendar
units shifted one quarter (244 million), Xiaomi's and Transsion's at FRED's 2025 average yuan rate (7.188); Transsion's
phone share of revenue (84%) is an assumption. The memory makers' gross profit per phone is the memory cost times
Micron's gross margin for the year.

## Problems and solutions

**1.** *The iPod's $299 split into retail ($45), distribution ($30), Apple ($80) and inputs ($144.40). What was Apple's
gross margin on its wholesale price, and why is the $80 more than any single part?*

*Solution.* Apple's wholesale price was 75% of $299, about $224.25; less inputs of $144.40 leaves about $79.85, a gross
margin of 35.6%. The most expensive part, the hard drive, was $73.39, so Apple's gross profit exceeded it. That is the
study's point: the design, the brand and the software that made a box of commodity parts into an iPod captured more
than any physical component.

**2.** *A chain has four firms with sales of $10, $83, $1,033 and $1,099, each buying only from the one before. What
is the total of sales, the total of value added, and why do they differ?*

*Solution.* Sales total $2,225. Value added is each firm's sales minus its purchases: 10, 73, 950 and 66, which sum to
$1,099, the final price. Sales count the $10 of wafers four times, TSMC's $73 three times and so on, because each sale
includes everything bought before it.

**3.** *Using this part's model, how does Apple's profit on the $1,099 phone change if the channel margin is 15%
instead of 10%? If the parts cost $570 instead of $520?*

*Solution.* The channel's take is price × 60% × margin: $66 at 10%, $99 at 15%, so Apple's revenue falls by $33. Its
operating costs (14.9% of revenue) fall by about $5, so pre-tax profit falls by about $28 and after-tax profit (tax
15.6%) by about $24, to about $220. Parts at $570 cut gross profit by $50; operating costs do not change, so after-tax
profit falls by about $42, to about $202.

**4.** *Xiaomi's 2025 smartphone revenue was CNY 186.44bn from 165.2m phones at a 10.9% gross margin. At 7.188 yuan to
the dollar, what are revenue and gross profit per phone? How many Xiaomi phones does it take to earn the gross profit
of one iPhone ($316)?*

*Solution.* Revenue per phone is 186.44bn / 165.2m = CNY 1,129, or $157. Gross profit is 10.9% of that, about $17.
One iPhone's gross profit equals that of about 18 Xiaomi phones.

**5.** *The 2TB iPhone Pro Max rose from $1,999 to $2,499. DRAM rose from $39 to $145 per phone and flash from $13 to
$51 per 256GB. By how much did the memory in the 2TB phone rise, and how does it compare with the price rise?*

*Solution.* The 2TB phone has eight times 256GB of flash, so flash rose by 8 × (51 - 13) = $304; with DRAM's $106, the
memory rose by $410. The price rose by $500. On Counterpoint's higher flash cost (about $250 per terabyte) the memory
rise is about $502. Either way, the buyer of the biggest phone pays for the extra memory almost dollar for dollar.

**6.** *Why can a market tracker say Apple sold one smartphone in five in 2025 while Counterpoint says it took about
half the industry's revenue?*

*Solution.* Shares by units weight a $100 phone and a $1,199 phone equally; shares by revenue weight them by price.
Apple's revenue per phone (about $859) is several times the industry's average, so its share of revenue is several
times its share of units, and its share of profit (85% of operating profit in Q2 2023, by Counterpoint's estimate) is
higher still, because its margin per phone is higher too.

**7.** *In 2025 T-Mobile's equipment revenues were $15.972bn and its cost of equipment sales $21.277bn; its service
revenues were $71.306bn and its cost of services $11.497bn. What did it lose on equipment, and what share of service
revenue was left after the direct cost of the network? Why does a carrier accept the first to get the second?*

*Solution.* Equipment lost $21.277bn - $15.972bn = $5.305bn. Service kept ($71.306bn - $11.497bn) / $71.306bn, about
84% before depreciation, selling and overheads. A discounted phone wins or keeps a customer who pays every month for
years; the carrier treats the discount as the cost of acquiring that stream, as a razor maker treats a cheap razor.

## Glossary

- **Bill of materials (BOM):** the cost of all the parts in a product, as estimated by a teardown.
- **Value added:** a firm's sales minus what it bought from other firms; summed over every firm, it is GDP.
- **Gross margin:** the share of each dollar of sales left after the direct cost of making the product.
- **Operating margin:** the share left after research, selling and overheads as well.
- **Channel:** the shops, carriers and resellers between the maker and the buyer.
- **DRAM and NAND:** working memory and storage memory.
- **Contract manufacturer:** a company that assembles products designed and sold by others (Foxconn, Luxshare, Tata).

## Lab and interactive

- `python -m videos.industry.labs 1`: the Dollar of the $1,099 phone with its ranges; the same phone in 2026; value
  added along a chain; revenue and gross profit per phone for three brands; price rises against memory-cost rises by
  storage size.
- The interactive (course site): split the price. The reader divides $1,099 into five piles with sliders, then sees
  this part's model beside the guess, and can move the model's assumptions (the channel margin, the parts, memory) to
  see what happens to Apple's profit.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p01.py`) with its URL. The main ones:

- Apple Form 10-K, fiscal 2010 to 2026 (net sales by category, units to fiscal 2018, margins, operating expenses, tax,
  channels, manufacturing locations, tariffs, supply constraints); Qualcomm, Micron, Skyworks, Broadcom and Corning
  Forms 10-K; TSMC Form 6-K (Q3 2026) and Q4 2025 release; T-Mobile US and AT&T Forms 10-K (2025); Apple's
  results release of 29 January 2026 (installed base).
- Samsung Electronics results (FY2025, Q3 2026); SK hynix 3Q26 results; Xiaomi 2025 annual results (HKEX); Hon Hai,
  Sony and Transsion results as reported.
- IDC Worldwide Quarterly Mobile Phone Tracker releases (13 January 2026; 28 August 2026); Counterpoint Research
  (Q3 2026 shipments; Q2 2023 profit share; Q2 2026 revenue share; the iPhone 18 Pro Max bill); TrendForce (the iPhone
  18 Pro bill); the Wall Street Journal's memory-cost estimates; Omdia (Africa).
- Linden, Kraemer and Dedrick (2007), *Who Captures Value in a Global Innovation System? The case of Apple's iPod*;
  Xing and Detert (2010), ADBI Working Paper 257.
- FRED: average exchange rates (DEXCHUS, DEXKOUS).
- *United States v. Google LLC*, memorandum opinion (D.D.C., 5 August 2024), as reported by NPR; Apple's App Store
  guidelines and Small Business Program.
- *Called it?*: Steve Ballmer at the USA Today CEO Forum, April 2007; this series' own call is in
  `explainer/industry/calls.py`.
