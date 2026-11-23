# Industry, Built: Part 2, The Economy on One Page

Part 2 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second of Act I, *Reading an Industry*. It asks: how big is each industry, and
compared with what? Part 1 followed one phone; this part steps back to the whole American economy and measures it
three ways, by sales, by value added and by jobs, then reads Wassily Leontief's input-output table to see how the
industries feed one another. The answer: it depends on what you count, and each count answers a different question.

It opens in 1936 with Leontief's table of the American economy of 1919: every industry's purchases from every other,
on one page. From there it covers:

- which is the biggest business: by sales Amazon ($716.9bn in 2025) and Walmart; by operating profit Apple, NVIDIA,
  Alphabet and Microsoft (about $130bn each); by employees Walmart (2.1 million) and Amazon (1.6 million), while
  NVIDIA employs 42 thousand;
- why sales mislead: McKesson's sales ($403bn) match Apple's ($416bn), but McKesson keeps $14.6bn after paying for
  the medicines and Apple $195bn after paying for its parts; summed over every firm, what each adds is GDP;
- what an industry is: NAICS's twenty sectors, establishments rather than companies, and Amazon, a retailer by sales
  but a cloud company by profit (AWS: 18% of its sales, $45.6bn of its $80.0bn of operating profit);
- big firms and small: 6.4 million businesses with employees in 2022, almost two in three with fewer than five people;
  2,262 firms with 5,000 or more employees had 36% of the jobs and 46% of the sales; half of all retail jobs are in
  firms of 20,000 or more, three in a hundred in construction;
- the 2025 economy by value added ($30.9 trillion): real estate 13.7% (much of it the rent homeowners are counted as
  paying themselves), government 11.1%, manufacturing 9.5%; and how the shares moved since 1997;
- the economy by jobs (158.4 million): government, health care and business services first; and value added per job,
  from utilities' $845 thousand to restaurants' and hotels' $76 thousand;
- who gets the value added: about half to workers, 7% to taxes on production, 42% to operating surplus; 81 cents of
  each dollar to the people in health care, 85 cents to the owners in real estate;
- Leontief's table as BEA publishes it for 2023, fifteen sectors: manufacturing buys 62 cents of inputs per dollar of
  output; all industries' sales come to $48.4 trillion against $27.7 trillion of value added;
- everything a dollar touches: rounds of buying converge to the Leontief inverse, $2.25 of output for one more dollar
  of manufactured goods; every sector's number, and what multipliers assume;
- upstream and downstream: farms and mines about 2.7 steps from the final buyer, retail, government, education and
  health care close to one; the series follows the same order;
- an intermission: eighty years of the American economy by share of GDP, 1947 to 2025;
- who buys: GDP from the buyers' side, 2023 (households $18.8 trillion, investment $5.0 trillion, government $4.7
  trillion, exports $2.6 trillion, less $3.4 trillion of imports); which buyer each industry sells to;
- a household's dollar, followed back through the table: 24 cents spent on housing and finance becomes 26 cents of
  their value added; business services, two cents of what households buy, end up with 11 cents; about ten cents goes
  abroad; a dollar of investment leaks 16 cents, a government's 9;
- from factories to services: manufacturing from almost two payroll jobs in five (1943) to one in twelve (2025), while
  its real output rose 57% since 1987; prices from 2000 to 2025 (hourly pay +124%, school fees and childcare +175%,
  doctors' and hospitals' services +138%, new cars +25%, toys -74%, computers -92%); the four forces (productivity,
  demand, Baumol's cost disease, trade);
- who is growing: real output from 2015 to 2025 against the economy's 27%: internet services about four times as big,
  computer systems design and software nearly tripled, manufacturing +17%, printing -28%;
- around the world: manufacturing a quarter of GDP in Korea, China and Vietnam, under a tenth in the United States,
  France and Britain; China adds 27% of the world's $17.6 trillion of manufacturing value added;
- where the profit is: six technology companies, and operating profit per employee of $3.1 million at NVIDIA against
  $14 thousand at Walmart; operating margins from NVIDIA's 60 cents per dollar of sales to McKesson's one and a half;
- the Board: the ten numbers every later part fills in for its industry;
- *Called it?*: Leontief's 1983 forecast that people would go the way of horses, and this series' call that in 2030
  health care will employ more Americans than manufacturing and retail combined (probability 40%).

## Build it

```bash
python -m videos.industry.industry2.compute               # every number, printed (instant)
EXPLAINER_TTS=silent python tools/build.py industry2 -q l  # the whole part, silent preview
python tools/build.py industry2                           # 1080p30 with narration
python -m videos.industry.labs 2                          # the lab
python -m explainer.industry.data.fetch --all             # refresh the BEA, BLS and World Bank extracts
```

Company figures are rows of the Register (`explainer/industry/data/rows_p02.py`); the economy's are small committed
extracts of BEA's, the BLS's and the World Bank's public tables in `explainer/industry/data/` (listed in
`SOURCES.md`, each with its URL and retrieval date). `compute.py` reads both and does arithmetic, nothing else.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | A table of everything | Leontief's 1936 table; the title; the question |
| 1 | Which is the biggest business? | The largest US-listed companies by sales, by operating profit, by employees |
| 2 | Sales count the same dollar again | McKesson against Apple; the pill's chain; value added and GDP |
| 3 | What is an industry? | NAICS; establishments; Amazon's segments against its profit |
| 4 | Big firms and small | Firms, jobs and sales by firm size, 2022; the giants' share of jobs by industry |
| 5 | The economy by value added | Twenty sectors, 2025; the shares since 1997 |
| 6 | The economy by jobs | Payroll jobs by sector, 2025; value added per job |
| 7 | Who gets the value added | Wages, taxes and operating surplus, by sector |
| 8 | Leontief's table, 2023 | BEA's direct requirements, fifteen sectors; a column, a row, the totals |
| 9 | Everything a dollar touches | Rounds of buying; the Leontief inverse; every sector's total requirement |
| 10 | Upstream and downstream | Upstreamness by sector; the series' order |
| — | Intermission | Shares of GDP, 1947-2025; the story so far |
| 11 | Who buys | GDP from the buyers' side; each industry's buyers |
| 12 | A household's dollar, followed back | What a household's dollar buys against who earns it; three buyers' dollars |
| 13 | From factories to services | Manufacturing's share of jobs since 1939; jobs against output; prices since 2000; four forces |
| 14 | Who is growing | Real value added by industry, 2015-2025, against the economy's 27% |
| 15 | Around the world | Manufacturing and farming shares by country; shares of the world's manufacturing |
| 16 | Where the profit is | The six largest operating profits; profit per employee; operating margins |
| 17 | The Board | The ten rows every part fills in |
| 18 | Called it? | Leontief, 1983; this series' call for 2030 |
| — | Three maps, and what comes next | The answers; Part 3, the accounts |

## What is computed, and from what

`compute.py` reads value added by sector for 2025 and its split into compensation, taxes on production and imports
less subsidies, and gross operating surplus from BEA's GDP-by-industry tables (TVA105, TVA110, TVA112, published 30
September 2026), and shares of GDP since 1947 from BEA's historical tables. Jobs are the BLS's annual averages of
payroll employment (Current Employment Statistics, via FRED); private education and health care are separate series,
and the sectors are matched to BEA's as `JOB_MAP` lists. Value added per job divides the two; it mixes BEA's
industry definitions with the BLS's, and real estate's value added includes owner-occupiers' imputed rent, which has
no jobs behind it.

The input-output table is BEA's 2023 use table after redefinitions at the sector level, at producers' prices. Industry
output is each column's total (intermediate inputs plus value added); the direct requirements are A = Z / x, the
Leontief inverse (I - A)^-1, and a sector's total requirement is its column sum. Upstreamness follows Antràs, Chor,
Fally and Hillberry (2012): each commodity's use by each industry as a share of its domestic absorption (output less
exports plus imports less inventory change), and U = (I - Δ)^-1 · 1. The world's figures are the World Bank's World
Development Indicators (manufacturing and agriculture as shares of GDP; manufacturing value added in current dollars),
with the United States' 2025 shares from BEA.

Who buys is the table's final-use columns (personal consumption, private fixed investment with the change in
inventories, government, exports, imports). A buyer's dollar is followed back the way BEA computes domestic
requirements: each commodity's imports are taken as the same share of its domestic supply (output plus imports less
exports) for every user; the domestic part of each purchase sets off rounds of domestic buying, x = (I - diag(1 - m)
A)^-1 diag(1 - m) c, and each industry earns its value-added coefficient times its output. What is not value added is
imports (and about one cent of scrap, second-hand goods and noncomparable imports, shown with them). The purchases
are at producers' prices, so the shops' and wholesalers' margins appear as purchases of their services.

Growth is BEA's chain-type quantity index of each industry's value added (2017 = 100), 2025 against 2015.

Firms by size are the Census Bureau's Statistics of US Businesses for 2022 (released April 2025), which cover private
employers and leave out farms' crop and livestock production, railroads, private households and government. Prices
are the BLS's consumer price indexes (US city average, annual averages) and the average hourly earnings of production
and nonsupervisory employees, 2000 against 2025.

The fifteen-sector table is a coarse one: a sector such as manufacturing buys from itself (factories from other
factories), which the detailed tables would spread across steel, chips and car parts. The totals and the inverse do
not depend much on that; the diagonal does.

## Problems and solutions

**1.** *McKesson's sales in fiscal 2026 were $403.4bn and its gross profit $14.55bn; Apple's sales in fiscal 2025 were
$416.2bn and its gross profit $195.2bn. What share of each dollar of sales does each keep after paying for what it
sells, and how many times bigger is Apple by that measure?*

*Solution.* McKesson keeps 14.55 / 403.4 = 3.6 cents of each dollar; Apple 195.2 / 416.2 = 46.9 cents. By gross
profit Apple is 195.2 / 14.55 = 13.4 times bigger, though their sales are within 3% of each other. Gross profit is not
quite value added (Apple's own wages are inside it, and some of McKesson's costs of sales are services bought from
others), but it shows the same thing: a distributor's sales are mostly other firms' goods passing through.

**2.** *A drug maker buys $20 of chemicals and sells a pack of pills to a wholesaler for $80; the wholesaler sells it to
a pharmacy for $83; the pharmacy sells it for $100. Add up the sales along the chain, and the value added. Which sum is
the pack's contribution to GDP?*

*Solution.* Sales: 20 + 80 + 83 + 100 = $283. Value added: the chemical maker 20, the drug maker 80 - 20 = 60, the
wholesaler 3, the pharmacy 17: $100, the price paid at the counter. GDP counts the $100. The $283 counts the
chemicals four times, the drug maker's work three times and so on.

**3.** *A two-sector economy has direct requirements A = [[0.2, 0.1], [0.3, 0.1]] (column 1: per dollar of sector 1's
output it buys 20 cents from itself and 30 cents from sector 2). Compute the output of both sectors for one more dollar
of sector 1's goods bought by final users, by rounds and by the inverse.*

*Solution.* Round 0: (1, 0). Round 1: A(1, 0) = (0.2, 0.3), total 0.5. Round 2: A(0.2, 0.3) = (0.07, 0.09), total 0.16.
The rounds shrink by roughly a third each time. The inverse: I - A = [[0.8, -0.1], [-0.3, 0.9]], determinant 0.69, so
(I - A)^-1 = [[1.304, 0.145], [0.435, 1.159]]. Its first column, (1.304, 0.435), sums to $1.74 of output: 1 + 0.5 +
0.16 + ... converges there.

**4.** *A farm sells half its output to households and half to a mill; the mill sells all of its flour to households.
What are the upstreamness of the farm and of the mill?*

*Solution.* The mill sells only to final users, so its upstreamness is 1. Half the farm's output is one step from a
final user and half is two steps (farm to mill to household): 0.5 × 1 + 0.5 × 2 = 1.5. With the formula, U_farm = 1 +
0.5 × U_mill = 1.5.

**5.** *In 2025 utilities added $507.7bn with 0.60 million payroll jobs, and health care and social assistance added
$2,327bn with 23.3 million. Compute value added per job in each. Does the difference mean a utility worker works eight
times harder?*

*Solution.* Utilities: 507.7bn / 0.601m = about $845 thousand per job; health care: 2,327bn / 23.29m = about $100
thousand. No: value added per job measures the capital behind each worker (power plants, pipes, grids) and the prices
the industry charges, much of which is paid to the owners of that capital. In utilities 60% of value added is
operating surplus; in health care 81% is pay.

**6.** *NVIDIA earned $130.4bn of operating profit in fiscal 2026 with 42 thousand employees; Walmart $29.8bn with 2.1
million. Compute operating profit per employee. What would Walmart's operating profit have to be to match NVIDIA's per
employee?*

*Solution.* NVIDIA: 130.4bn / 42,000 = about $3.1 million. Walmart: 29.8bn / 2.1m = about $14 thousand, some 220 times
less. To match NVIDIA per employee Walmart would need 2.1m × $3.1m = about $6.5 trillion of operating profit, nine
times its sales. The comparison says less about the two companies' managers than about their products: chips designed
once and sold many times against goods moved and sold by people.

**7.** *A household spends $100. Using this part's estimates, about how much ends up as value added in American
business services, and how much abroad? Why is the first so much larger than the $2 households spend on business
services directly?*

*Solution.* About $11 in business services and about $10 abroad. Every other industry buys business services as
inputs: the landlord's lawyer, the hospital's billing contractor, the shop's advertising, the factory's software. The
rounds of buying carry part of every purchase to them, so their share of value added is five times their share of
households' purchases.

**8.** *In 2025 health care and social assistance employed 23.29 million people and manufacturing plus retail 28.07
million. Health care added 0.78 million jobs in 2025, after 0.96 and 0.97 million in 2023 and 2024. If manufacturing and
retail stay flat, in which year does health care pass them at each pace? Why does the series put the chance of it
happening by 2030 at 40%?*

*Solution.* The gap is 4.78 million. At 0.78 million a year it closes in 6.1 years, in 2031; at the three-year average
of about 0.90 million, in 5.3 years, during 2030. The 2030 annual average needs the crossing early in the year or
before, so on the recent pace it is just short; a dip in manufacturing or retail, or a faster health-care pace, would
bring it inside 2030, and a slowdown in health-care hiring would push it out. Close, but more likely than not to miss:
hence 40%.

## Glossary

- **Value added:** an industry's output minus what it bought from other industries; summed over every industry, it is
  GDP.
- **Gross domestic product (GDP):** the value added of every producer in a country in a year; equally, what final
  users spend on its goods and services, less imports.
- **NAICS:** the North American Industry Classification System, which sorts establishments (factories, offices, stores)
  into twenty sectors and about a thousand industries.
- **Compensation:** wages, salaries and benefits paid to employees.
- **Gross operating surplus:** value added left after pay and taxes on production: profit, interest, rent and
  depreciation.
- **Imputed rent:** the rent homeowners are counted as paying themselves, so that owning and renting add the same to
  GDP.
- **Input-output table (use table):** what each industry buys from every other, and what final users buy.
- **Direct requirements:** what an industry buys from each other industry per dollar of its own output.
- **Leontief inverse (total requirements):** the output every industry must produce for one more dollar of an
  industry's goods bought by final users, counting every round of buying.
- **Upstreamness:** the average number of steps an industry's output passes through before it reaches a final user.
- **Cost disease:** William Baumol's name for the rising relative price of services whose productivity cannot grow as
  fast as goods'.

## Lab and interactive

- `python -m videos.industry.labs 2`: McKesson against Apple; the 2023 table's direct requirements and inverse, with the
  rounds of buying checked against the inverse; upstreamness; value added per job; a household's dollar followed back
  to value added and imports; the series' 2030 call projected from the BLS's series.
- The interactive (course site): everything a dollar touches. The reader picks a sector, steps through the rounds of
  buying and watches the total converge to the Leontief inverse, and can make every industry buy more or less from the
  others to see the multiplier move.

## Sources

Company figures are in the Register (`explainer/industry/data/rows_p02.py`) with their URLs; the economy's extracts
are listed in `explainer/industry/data/SOURCES.md`. The main ones:

- Bureau of Economic Analysis: GDP by industry, value added and its components, 2025 (ValueAdded.xlsx, tables TVA105,
  TVA110, TVA112, released 30 September 2026); value added as a share of GDP, 1947-1997 (historical tables); the 2023
  use table after redefinitions, sector level (AllTablesIO.zip).
- Bureau of Labor Statistics, Current Employment Statistics, annual averages of payroll jobs by industry, 1939-2025, and
  the Federal Reserve's manufacturing output index, via FRED.
- The World Bank, World Development Indicators: manufacturing, agriculture and services as shares of GDP and
  manufacturing value added in current dollars, by country.
- Forms 10-K of Amazon, Walmart, UnitedHealth Group, McKesson, Apple, NVIDIA, Alphabet, Microsoft and Meta (fiscal
  years ending June 2025 to March 2026: revenue, operating income, employees, segment results).
- US Census Bureau, North American Industry Classification System, 2022; Statistics of US Businesses, 2022 (firms,
  establishments, employment and receipts by enterprise size).
- BLS consumer price indexes (all items, services, durables, medical care services, tuition and childcare, food away
  from home, rent, new vehicles, apparel, toys, computers) and average hourly earnings, via FRED.
- Leontief (1936), "Quantitative Input and Output Relations in the Economic System of the United States", *Review of
  Economic Statistics* 18(3); the Nobel prize in economic sciences, 1973; Leontief (1983), in *The Long-Term
  Impact of Technology on Employment and Unemployment*, National Academy of Engineering.
- Antràs, Chor, Fally and Hillberry (2012), "Measuring the Upstreamness of Production and Trade Flows", *American
  Economic Review: Papers and Proceedings* 102(3).
- Baumol (1967), "Macroeconomics of Unbalanced Growth", *American Economic Review* 57(3); Autor, Dorn and Hanson (2013),
  "The China Syndrome", *American Economic Review* 103(6), on imports and manufacturing jobs.
- *Called it?*: the series' own call is in `explainer/industry/calls.py`.
