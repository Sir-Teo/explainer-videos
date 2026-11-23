# Industry, Built: Part 3, The Accounts

Part 3 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third of Act I, *Reading an Industry*. It asks: what do a company's accounts say
about the business underneath? It answers by keeping a small business's books from nothing, then reading the latest
annual accounts of six very different American companies: Costco, Microsoft, JPMorgan Chase, NextEra Energy, Delta
Air Lines and Eli Lilly. The answer: the accounts measure what a dollar of the owners' money earns, show where each
dollar of sales goes and who funds the business, and the gap between profit and cash is where trouble shows first.

It opens in Venice in November 1494, where Luca Pacioli printed the merchants' method of writing every transaction
twice, and at DuPont in 1914, where Donaldson Brown turned the books into one number, the return on investment, and
split it into profit per dollar of sales times sales per dollar invested. From there it covers:

- six companies with their names removed, five ratios each, to match (answered in chapter 13);
- a model bakery's books, entry by entry: savings, a loan, an oven, flour on credit, sales for cash and on credit,
  wages; the two sides of the book always agree, which is why a balance sheet balances;
- the income statement: the bakery's year ($216,000 of sales, $13,509 of net profit, depreciation explained), then a
  dollar of sales down five real income statements: Costco keeps under 4 cents as operating profit, Microsoft 47,
  Delta 9, Lilly 40 (after 20 cents of research), NextEra 30 (after 24 cents of depreciation);
- the balance sheet: the bakery's, then five companies' as shares: JPMorgan funded 58% by deposits with 8% owners'
  money; NextEra's plants and wires 73% of its assets; Costco's payables larger than its stock; Delta holding $16.4bn
  of customers' money for tickets and miles; Microsoft mostly owners' money, with data centres its largest asset;
- profit is not cash: the bakery's profit of $13,509 against $10,447 of operating cash and a $45,000 oven; the same
  bakery growing 60% a year stays profitable and runs out of cash in its second year; Microsoft's fiscal 2026 net
  income of $133.7bn against free cash of $67.0bn after $115.9bn of capital spending; NextEra's $24.1bn of new plant
  against $12.5bn of operating cash;
- an intermission: Microsoft's capital spending by fiscal year, $2.0bn in 2010 to $115.9bn in 2026;
- paid before it pays: Costco sells its stock in about 27 days and pays suppliers in about 31; its 84.1 million paid
  members each spend about $3,672 a year; membership fees ($5.9bn) are half its operating income;
- the Du Pont identity: return on equity = margin × speed × borrowing; the six on a map of margin against speed;
  JPMorgan's 1.3% on assets becomes 16% on equity through borrowing, and Lilly's 78% is partly buybacks;
- the return on capital against its cost: Lilly, Microsoft and Costco 22-31%, Delta 13%, NextEra 5% (with the reasons
  the measure is unkind to a utility), Enron about 7% in 2000;
- one seat, one member: a Delta seat from New York to Los Angeles brings in about $526 and keeps about $48; the
  seat-mile margin times 298 billion seat miles rebuilds Delta's operating income; American Express paid Delta $8.2bn,
  about $68 a seat;
- the businesses inside: Microsoft's Office and LinkedIn earn a 60% margin, its cloud 41% while growing 30% (its costs
  up 44% on AI infrastructure), Windows and Xbox 27% and shrinking; Mounjaro and Zepbound, one molecule, bring Lilly
  56% of its revenue;
- where the accounts mislead: expensed research, pay in shares, paper gains, goodwill, the company's own measures,
  estimates, each with a figure from the six;
- reading a 10-K, item by item, and where this part found its numbers;
- the six, revealed;
- *Called it?*: Bethany McLean's "How exactly does Enron make its money?" (Fortune, March 2001), Enron's own 2000
  figures, the restatement and the bankruptcy; and this series' call that Microsoft's free cash flow will fall in
  fiscal 2027 while its operating income rises (65%).

## Build it

```bash
python -m videos.industry.industry3.compute               # every number, printed (instant)
EXPLAINER_TTS=silent python tools/build.py industry3 -q l  # the whole part, silent preview
python tools/build.py industry3                           # 1080p30 with narration
python -m videos.industry.labs 3                          # the lab
python -m pytest tests/industry                           # the generic firm's books reconcile; the Register
```

Every company figure is a row of the Register (`explainer/industry/data/rows_p03.py`) with its source, URL and dates;
Microsoft's capital spending since 2010 is the Filing Room's `sec_annual.csv`. The model bakery runs on
`explainer/industry/works/firm.py`, the series' generic firm, whose tests prove that its three statements reconcile
for any operations.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Every entry twice | Pacioli, Venice, 1494; Donaldson Brown, DuPont, 1914; the title |
| 1 | Six companies, no names | Five ratios for six anonymous companies; match them |
| 2 | A bakery's books | Eight entries, double entry, the balance sheet balancing |
| 3 | The income statement | The bakery's year as a waterfall; a dollar of sales at five companies |
| 4 | The balance sheet | The bakery's; five companies' as shares: who funds each business |
| 5 | Profit is not cash | From profit to cash; the bakery that grows too fast; Microsoft and NextEra |
| — | Intermission | Microsoft's capital spending, fiscal 2010-2026; the story so far |
| 6 | Paid before it pays | Costco's days of stock and of payables; its fees per member |
| 7 | Margin, speed and borrowing | The Du Pont identity; the six on a map; leverage |
| 8 | The return on capital | Value created and destroyed; five companies against an assumed cost of capital; Enron |
| 9 | One seat, one member | Delta's seat mile and a New York to Los Angeles seat; American Express |
| 10 | The businesses inside | Microsoft's three segments; Lilly's two names |
| 11 | Where the accounts mislead | Six traps, each with a real figure |
| 12 | Reading a 10-K | The items of the annual report; where this part's numbers were found |
| 13 | The six, revealed | The answers to chapter 1, with the reasons |
| 14 | Called it? | McLean and Enron, 2001; this series' call on Microsoft's free cash flow |
| — | What the accounts say, and what comes next | The five answers; Part 4, the cost curve |

## What is computed, and from what

`compute.py` reads each company's latest annual figures from the Register: Costco and Microsoft for their fiscal 2026
(to 30 August and 30 June 2026), JPMorgan Chase, NextEra, Delta and Lilly for calendar 2025. Margins are per dollar
of revenue (for the bank, profit before tax stands in for operating profit); speed is revenue over year-end total
assets; borrowing is year-end assets over year-end equity; return on equity is their product, equal to net income
over year-end equity. Lilly reports income before tax but no operating line, so its operating profit is income before
tax plus its net non-operating expense. The return on capital is operating profit taxed at the statutory 21%, over
year-end equity plus long-term debt; the bank is left out. The 8% cost of capital is an assumption for illustration.

The bakery is a model, not a company: 60,000 loaves at $3.60, flour and fillings at $1.30 a loaf, staff (the owner's
pay included) and rent of $115,000, a $45,000 oven depreciated over ten years, a $20,000 loan at 7%, tax at 21%,
cafes paying in 20 days, flour stocked for 10 and the miller paid in 30. The growing bakery raises volume, staff and
rent 60% a year, buys a new oven each year, and gives its cafes 60 days. Costco's days are year-end inventories and
payables over merchandise costs, times 365; its figures per member divide by the average of the year's opening and
closing paid members. Delta's figures per seat multiply its cost and revenue per available seat mile by 2,475 miles,
about the great-circle distance from New York (JFK) to Los Angeles; fuel, labour and American Express per seat mile
divide those totals by its 298,045 million available seat miles.

## Problems and solutions

**1.** *A shop owner puts in $10,000 and borrows $5,000 from a bank. She buys $8,000 of stock on 30 days' credit and
$6,000 of shelving for cash, then sells half the stock for $7,000 in cash. Draw up her balance sheet.*

*Solution.* Cash: 10,000 + 5,000 - 6,000 + 7,000 = $16,000; stock $4,000; shelving $6,000: assets $26,000. Owed to
the supplier $8,000, the bank $5,000; the owner's $10,000 plus profit of 7,000 - 4,000 = $3,000: claims $26,000. The
two sides agree because each transaction changed both by the same amount, or moved money within one side.

**2.** *A firm reports net income of $50, depreciation of $20, receivables up $15, inventory up $10 and payables up $5.
What is its cash from operations? If it spent $40 on equipment, what is its free cash flow?*

*Solution.* 50 + 20 - 15 - 10 + 5 = $50 of cash from operations: depreciation is added back because it used no cash
this year; the rise in receivables and stock is cash tied up; the rise in payables is cash kept. Free cash flow is 50
- 40 = $10.

**3.** *Costco's fiscal 2026 net income was $9.226bn on revenue of $303.154bn, total assets of $89.045bn and equity of
$35.803bn. Compute its margin, speed, borrowing and return on equity. Which lever does most of the work?*

*Solution.* Margin 9.226 / 303.154 = 3.0%; speed 303.154 / 89.045 = 3.40; borrowing 89.045 / 35.803 = 2.49; return on
equity 3.0% × 3.40 × 2.49 = 25.8% (equal to 9.226 / 35.803). Speed: Costco sells its assets' worth of goods more than
three times a year, which turns a thin margin into a high return.

**4.** *Investors in a business could earn 8% elsewhere at the same risk. It earns $12 a year on $100 put in, forever.
What is it worth? What if it earned $6? What happens to value if the second business doubles in size on the same
terms?*

*Solution.* 12 / 0.08 = $150, so $50 of value was created. 6 / 0.08 = $75: $25 destroyed. Doubling the second
business puts in another $100 to create another $75: it destroys another $25. Growth adds value only when the return
on capital exceeds its cost.

**5.** *Delta's revenue per available seat mile was 21.26 cents and its cost 19.31 cents, of which fuel was 3.29 cents
at an average of $2.30 a gallon. Holding everything else fixed, at what fuel price would its operating margin
vanish?*

*Solution.* The margin is 1.95 cents, so fuel per seat mile could rise to 3.29 + 1.95 = 5.24 cents before the margin
is gone: 59% more, or about $3.66 a gallon. Airlines' profits swing with fuel because their margin per seat mile is a
small difference between two large numbers.

**6.** *Costco holds about 27 days of merchandise and pays suppliers in about 31; members pay at the till. What is its
cash conversion cycle, and why does fast growth give it cash rather than consume it?*

*Solution.* 27 + 0 - 31 = -4 days: it is paid about four days before it pays. As sales grow, the payables owed to
suppliers grow faster than the stock it must hold, so growth releases cash. The growing bakery had the opposite cycle
(10 + 60 - 30 = 40 days) and ran out of cash.

**7.** *Microsoft's fiscal 2026 net income was $133.7bn, including $6.5bn of net gains on OpenAI; its operating cash
flow was $182.9bn and its additions to property and equipment $115.9bn. What was its free cash flow, and what share
of net income was it? Name two reasons operating cash exceeded net income.*

*Solution.* 182.9 - 115.9 = $67.0bn, half of net income. Operating cash exceeded net income because depreciation of
its existing equipment ($34.3bn) used no cash this year and customers pay for subscriptions in advance; the paper
gain on OpenAI works the other way, raising net income without cash.

## Glossary

- **Double entry:** recording every transaction twice, once on each side of the books, so that they always balance.
- **Assets, liabilities, equity:** what a business has; what it owes; what belongs to its owners. Assets = liabilities
  + equity.
- **Income statement:** a year's sales less its costs, down to profit.
- **Depreciation:** the cost of equipment spread over the years it is used.
- **Balance sheet:** what a business has and who paid for it, on one day.
- **Cash-flow statement:** the cash that came in and went out, from operations, investment and financing.
- **Free cash flow:** cash from operations less spending on equipment.
- **Working capital:** money tied up in stock and in what customers owe, less what is owed to suppliers.
- **Return on equity (ROE):** a year's profit per dollar of the owners' money.
- **Du Pont identity:** ROE = profit margin × asset turnover (speed) × leverage (borrowing).
- **Return on invested capital (ROIC):** after-tax operating profit per dollar of capital invested by owners and
  lenders.
- **Cost of capital:** the return investors could expect elsewhere at the same risk.
- **Goodwill:** the amount paid for a company above the value of its separately identifiable assets.
- **Non-GAAP measure:** a figure a company defines itself, such as an adjusted cost, which must be reconciled to the
  official one.

## Lab and interactive

- `python -m videos.industry.labs 3`: the bakery's entries checked for balance; its year from operations; the growing
  bakery running out of cash; return on equity as margin × speed × borrowing for four of the six; Costco's days;
  Delta's operating income rebuilt from its seat miles; Microsoft's profit against free cash.
- The interactive (course site): grow the bakery. Set its growth, the days its cafes take to pay, the days the miller
  gives and the price of a loaf, and see its profit against its cash for six years and its balance sheet at the end.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p03.py`) with its URL. The main ones:

- Forms 10-K: Costco (fiscal 2026), Microsoft (fiscal 2026, with its 10-Q for the quarter to September 2026),
  JPMorgan Chase, NextEra Energy, Delta Air Lines and Eli Lilly (2025), from SEC EDGAR's company facts and the filed
  documents.
- Microsoft's fiscal 2027 capital-spending guidance (earnings call, 29 July 2026), as reported by Investing Live and
  Nasdaq.
- National Library of Scotland, on Pacioli's *Summa de arithmetica* (Venice, 1494); Hagley Museum and Library, *The
  Father of ROI: Donaldson Brown*.
- Bethany McLean, "Is Enron Overpriced?", *Fortune*, 5 March 2001; Enron's Form 10-K for 2000 and Forms 8-K of 8
  November and 17 December 2001; Senator Carl Levin's statement on the role of the financial institutions in Enron's
  collapse, Permanent Subcommittee on Investigations, 23 July 2002.
- *Called it?*: the series' own call is in `explainer/industry/calls.py`.
