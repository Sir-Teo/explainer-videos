# Industry, Built: Part 24, Construction

Part 24 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first of Act IV, *Building*. It asks: why has almost everything become cheaper to
make, except a building? It answers with the Empire State Building's fact sheet; the California High-Speed Rail
Authority's business plans of November 2008 and 2026; the National Audit Office's investigation of the collapse of
Carillion (2018); Flyvbjerg's overview of megaprojects (2014); Ferrovial's Form 20-F for 2025; the Forms 10-K of Fluor,
Quanta Services and Martin Marietta for 2025 and Quanta's third-quarter 2026 results; the SEC company facts of
twenty-five contractors, engineers, materials companies, equipment renters and a concession owner; the Census Bureau's
construction spending, the BLS's employment and producer prices (via FRED); BEA's real value added and prices by industry
since 1947; and the Works' contractor. The answer: a building is sold before it is fully designed, by sealed bid, and the
lowest bid is usually the most optimistic estimate, so builders keep a few cents of each dollar; the risk of a wrong
estimate sits with whoever signs a fixed price, and builders have learned to avoid it; the business runs on other people's
cash, which flatters a growing contractor and sinks a shrinking one; every site is a prototype, and construction's real
output per worker has fallen since 1970 while its prices rose nineteen-fold; and the money is with whoever owns the quarry,
the crane or the road, not with whoever does the building.

It opens on the Empire State Building, opened on 1 May 1931, 410 days after ground was broken, its frame rising 4.5 storeys
a week; on California's high-speed railway, about $33bn in 2008 and $126.1bn (by a cheaper route, finished 2039) or
$231.3bn (as first designed) in 2026; and on real output per worker since 1970: manufacturing 5.66 times, the whole
economy 2.02, construction 0.63. From there it covers:

- Run it: five tenders. The Works' job really costs $100m; each of five bidders estimates it with a 5% error and the four
  rivals add 8%; the lowest sealed bid wins. In one tender the rival who estimated $96m wins at $103.7m and makes $3.7m,
  not $8m. Winning estimates are 5.8% too low on average: the winner's curse. Adding 2% wins 2.7 of five jobs and loses
  $2.8m (a margin of -1.1% on work won); adding 8% wins one in five and makes $1.7m (1.7%); adding 15% wins 0.16 jobs
  (3.9%). The best markup is about 8%, winning 19% of tenders; below about 4% every markup loses money. Real general
  contractors' median net margin: 3.1%;
- where a building's dollar goes: $2.24 trillion of American construction in 2025 ($936bn homes, $1,309bn everything
  else, $538bn paid by governments); construction's value added, $1.34 trillion, 63.7% paid to employees against 50.9%
  for the economy; median net margins along the chain (general contractors 3.1%, specialty contractors 3.3%, engineers
  5.0%, concessions 6.6%, equipment rental 13.7%, materials 15.3%); Martin Marietta on why stone travels only so far;
  United Rentals' $16.1bn of revenue at a 17% margin;
- the bid and the contract: fixed price against cost plus a fee; Fluor on lump-sum bids made 'based on incomplete
  information'; its backlog moving to 81% reimbursable ($25.5bn in all); $108m of cost growth on three infrastructure
  projects, $643m of revenue reversed for a judgment on a project finished in 2015, $255m of work on loss-making legacy
  projects; Tutor Perini's net margin from -8.7% (2019) to +1.5% (2025);
- paid first, pay later: one job's cash (about $8m in hand at the peak, $3m profit at the end); an order book of one job a
  month for two years, then none (cash $100m at month 25, $65m eight months later, while profit rises from $61m to $72m);
  Carillion: £5.2bn of revenue in 2016, about 45,000 people, about 420 British public contracts; a £845m provision on
  10 July 2017, £1.05bn in September, a warning on its loans in November, insolvency on 15 January 2018; £655m of cash
  lost from operations in 2017; suppliers paid 45 days after invoice on average; 'large advance payments on new contracts
  at the expense of future profitability'; £2.6bn of pension liabilities;
- why building has not got cheaper: construction jobs from 3.7m (1970) to 8.3m (2025) and manufacturing's from 17.8m to
  12.6m, against real output growth of 1.4 and 4.0 times; prices of construction's output 19 times their 1970 level,
  manufacturing's 3.0, the economy's 6.4; materials prices up 45% from 2019 to 2022 against 14% for consumer prices; four
  explanations, none settled;
- an intermission: homes against everything else since 2002; spending by kind (factories from $82bn in 2021 to $243bn in
  2024); construction's output per worker close up;
- megaprojects: nine in ten over budget; overruns from the Suez Canal's 1,900% to the Great Belt bridge's 50%; rail
  44.7% over with 51.4% fewer passengers, roads 20.4% over; California's railway from 2008 to 2026; optimism bias,
  strategic misrepresentation and lock-in, and Willie Brown's 'the first budget is really just a down payment';
- building the road, or owning it: Ferrovial's construction arm at 4.7% of €7.65bn against its toll roads at 52% of
  €1.37bn; the 407 ETR (C$2,009m of revenue, C$811m of net profit, 48.3% Ferrovial's); C$1.99bn for 5.06% more, valuing
  the road at about C$39bn; the owner's traffic risk; a €17.4bn order book, 84% public;
- the new boom: factories ($81bn to $214bn, 2019-2025) and power ($118bn to $172bn); Quanta's quarterly revenue from
  $7.63bn to $12.01bn and its backlog from $44.0bn to $63.7bn, 44% under master service agreements; margins at Comfort
  Systems, EMCOR and Sterling;
- the landscape, November 2026: twenty-five companies by revenue and margin; and the map of the business;
- *Called it?*: the railway's forecasts of 2008 and 2026, the reference class (about one large project in ten on
  schedule) and this series' call that its trains will not carry fare-paying passengers between Merced and Bakersfield
  before 1 January 2034 (70%);
- every building a prototype: the five answers.

## Build it

```bash
python -m videos.industry.industry24.compute               # every number, printed
EXPLAINER_TTS=silent python tools/build.py industry24 -q l  # the whole part, silent preview
python tools/build.py industry24                           # 1080p30 with narration
python -m videos.industry.labs 24                          # the lab
python -m pytest tests/industry                            # the Register and the Works (test_contractor.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p24.py`) or comes from the Filing Room: the companies'
accounts (`sec_construction.csv`, with United Rentals from `sec_mach.csv`), FRED's construction spending, jobs and prices
(`fred_construction.csv`) and BEA's long series of real value added and prices (`bea_long.csv`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Faster in 1930 | The Empire State Building; California's railway; output per worker since 1970; the title |
| 1 | Run it: five tenders | The tender; one example; the winner's curse; three markups; the curve; real margins |
| 2 | Where a building's dollar goes | Spending by kind; pay's share; margins along the chain; quarries; rental |
| 3 | The bid and the contract | Fixed price and cost plus; Fluor's lump-sum risk and contract mix; charges; Tutor Perini |
| 4 | Paid first, pay later | One job's cash; an order book that stops; Carillion; its warnings; the mechanism |
| 5 | Why building has not got cheaper | Workers and output; prices; materials; the explanations |
| — | Intermission | Homes against the rest; spending by kind; output per worker close up |
| 6 | Megaprojects | The iron law; famous overruns; rail and roads; California's railway; why |
| 7 | Building the road, or owning it | Ferrovial's two margins; the 407 ETR; what it is worth; traffic risk; the order book |
| 8 | The new boom: power and factories | Factories and power; Quanta's revenue and backlog; specialty contractors' margins |
| 9 | The landscape, November 2026 | Revenue against margin; the map |
| 10 | Called it? | The railway's forecasts; the reference class; this series' call |
| — | Every building a prototype | The five answers; Part 25, homes |

## What is computed, and from what

`compute.py` reads the Filing Room and the Register. The tender is the Works' (`explainer/industry/works/contractor.py`):
the true cost is $100m; each bidder's estimate is the cost times one plus a normal error with a 5% standard deviation;
four rivals add 8%; the lowest bid wins and is paid its bid. Your chance of winning at a given estimate is the chance all
four rivals bid higher; expectations integrate over your own error on a 4,001-point grid; the best markup is searched on a
0.1% grid. Five tenders multiply one tender's expectations by five. The cash model bills each month's work and is paid two
months later, less 5% retention released six months after completion; it pays its costs three months after the work; the
order book starts one $100m, twelve-month, 3%-margin job a month for two years. Real output per worker is BEA's real value
added (chain-type quantity index, its 1947-1997 table linked at 1997 to the current release) over the BLS's annual average
employment (construction, manufacturing; for the whole economy, real GDP over total nonfarm employment), 1970 = 1; prices
are BEA's chain-type price indexes for value added. Margins are profit attributable to the parent over revenue, the median
of the last five fiscal years; Ferrovial's revenue is converted at 2025's average dollar-euro rate. Spending is the annual
average of the Census Bureau's seasonally adjusted annual rates. The 407 ETR's implied value is C$1.99bn / 0.0506.

## Problems and solutions

**1.** *Five bidders estimate a job that really costs $100m; their estimates are 96, 99, 101, 103 and 106, and all add 8%.
Who wins, at what price, and what does it make?*

*Solution.* Bids are 103.68, 106.92, 109.08, 111.24 and 114.48: the bidder who estimated 96 wins at $103.68m. It meant to
add $7.68m; it makes 103.68 - 100 = $3.68m, because its estimate was $4m too low. The lowest bid comes from the lowest
estimate, which is usually too low.

**2.** *A contractor bills $100m of work evenly over twelve months, is paid two months after each month's work less 5%
retention, and pays its costs (97% of the work) three months after the work. Roughly how much cash does the job hand it
at its peak?*

*Solution.* Each month brings in 100 / 12 × 0.95 = $7.92m and pays out 100 × 0.97 / 12 = $8.08m a month later. In the
month the first payment arrives, nothing has yet been paid out, so cash peaks at about $7.9m; after that each month's
inflow roughly matches the previous month's outflow and the balance drifts down until the last payments to suppliers
and the release of the $5m retention leave the $3m profit.

**3.** *Ferrovial's construction arm had €7,653m of revenue and €357m of operating profit in 2025; its toll roads had
€1,374m and €719m. What are the two margins, and what share of the group's operating profit from the two came from roads?*

*Solution.* Construction: 357 / 7,653 = 4.7%. Toll roads: 719 / 1,374 = 52.3%. Roads earned 719 / (719 + 357) = 67% of
the two segments' operating profit on 15% of their revenue.

**4.** *Since 1970 construction's real value added rose 1.42 times while its employment rose from 3.65 million to 8.26
million. What happened to real output per worker?*

*Solution.* 1.42 / (8.26 / 3.65) = 1.42 / 2.26 = 0.63: each worker produced about 37% less, in real terms, in 2025 than in
1970. Manufacturing: 4.00 / (12.63 / 17.85) = 5.66 times more.

**5.** *California's 2008 plan put the line from Los Angeles and Anaheim to San Francisco at $33bn in 2008 dollars. Its
2026 plan puts Phase 1 at $126.1bn by a cheaper route. If prices rose about 55% between 2008 and 2026, how much of the
increase is inflation?*

*Solution.* $33bn × 1.55 = about $51bn in 2026 dollars. The 2026 estimate is about 126.1 / 51 = 2.5 times that, even by
the cheaper route, and 231.3 / 51 = 4.5 times as first designed: most of the increase is not inflation. (The 55% is an
assumption for the exercise; the plan's own figures are in dollars of different years.)

## Glossary

- **Tender:** a competition in which contractors submit sealed prices for a job.
- **Winner's curse:** the tendency of the winner of a sealed-bid contest for something of uncertain value to be the bidder
  who misjudged it most.
- **Lump-sum (fixed-price) contract:** the contractor agrees a price and bears any cost above it.
- **Cost-reimbursable (cost-plus) contract:** the owner pays the actual cost plus an agreed fee.
- **Guaranteed maximum price:** cost plus a fee, up to a ceiling.
- **Backlog (order book):** work won and not yet done.
- **Retention:** a share of each payment held back until a job is finished, as security for defects.
- **Working capital:** money tied up in a business's day-to-day trade; negative when it is paid before it pays.
- **Megaproject:** a project costing a billion dollars or more.
- **Reference class:** the record of past projects like the one being planned.
- **Concession:** the right to build or run an asset, such as a toll road, and collect its revenue for a period.

## Lab and interactive

- `python -m videos.industry.labs 24`: the Works' tender at every markup and the winner's curse; five tenders; one job's
  cash and an order book that stops; construction spending; output per worker and prices since 1970; margins along the
  chain; Fluor's contract mix; Carillion; megaprojects and California's railway; Ferrovial's two margins; Quanta; the
  landscape; and this series' call.
- The interactive (course site): bid for five tenders. Choose your markup, how far off estimates are, how much the rivals
  add and how many there are, and see your chance of winning, the margin on work you win and your expected profit.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p24.py`) or the Filing Room
(`explainer/industry/data/SOURCES.md`). The main ones:

- The Empire State Building's fact sheet (esbnyc.com).
- The California High-Speed Rail Authority's Business Plans of November 2008 and 2026 (hsr.ca.gov).
- The National Audit Office, *Investigation into the government's handling of the collapse of Carillion* (HC 1002, June
  2018).
- Bent Flyvbjerg, 'What You Should Know about Megaprojects and Why: An Overview', *Project Management Journal* 45(2), 2014
  (arXiv:1409.0003).
- SEC EDGAR: Ferrovial's Form 20-F for 2025; the Forms 10-K of Fluor, Quanta Services and Martin Marietta for 2025;
  Quanta's Form 8-K of 29 October 2026; the company facts of Fluor, Jacobs, AECOM, Quanta, EMCOR, MasTec, Granite, Tutor
  Perini, Dycom, Comfort Systems, Sterling, KBR, Primoris, MYR Group, Argan, APi Group, Tetra Tech, Construction Partners,
  Vulcan Materials, Martin Marietta, CRH, Eagle Materials, Herc, United Rentals and Ferrovial.
- FRED: the Census Bureau's construction spending by type; the BLS's employment in construction and manufacturing and
  total nonfarm, average weekly hours in construction, producer prices for construction materials, new warehouse
  construction and lumber, and the CPI.
- BEA: value added by industry and its components (2025); real value added and price indexes by industry, 1947-2025.
