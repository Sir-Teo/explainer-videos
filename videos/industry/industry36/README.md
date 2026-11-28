# Industry, Built: Part 36, Software

Part 36 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first of Act VII, *Information*. It asks: what is a business worth when the second
copy costs nothing? It answers with the Forms 10-K of Microsoft and Atlassian (fiscal 2026), Oracle (to May 2026),
Salesforce, Snowflake, CrowdStrike and Workday (to January 2026), Adobe (fiscal 2025), ServiceNow and Datadog (2025);
Microsoft's and Salesforce's latest 10-Qs; Adobe's 10-K for fiscal 2013; Salesforce's investor-day exhibits of 2021 and 2022;
the SEC company facts of thirty-one software companies; the BEA's software investment, the BLS's software prices and
programmers' jobs; and the Works' software company. The answer: a great deal, at scale, because the costs stay put while
revenue grows; but finding each customer is expensive and they are won at a loss; subscriptions turn one sale into a stream
paid in advance; lock-in keeps the stream flowing; and artificial intelligence makes each answer cost something again. A
software company is worth what its customers will keep paying for the next copy.

It opens on the free copy; on Microsoft's $332bn of revenue and $155bn of operating income in the year to June 2026, with
223,000 employees; on where its revenue went ($106bn of cost of revenue, $36bn of engineering, $27bn of selling); and on its
revenue and operating income since 2009. From there it covers:

- Run it: a software company for five years. In the Works, a company with $200m of annual recurring revenue (ARR), a 78%
  gross margin and 100 salespeople each bringing in $450,000 a year; in the first year $45m of new business, $22m from
  customers who stay and $17m lost; selling costs $70m and pays back in about 24 months. With no new hires growth slows from
  25% to 13% while the operating margin climbs from 23% to 44%. An extra $30m a year ends five years with $561m of ARR spent
  on engineers, $588m half and half and $581m on salespeople, and $706m, $596m and $440m of cash. A 10% price rise adds about
  $9m of ARR;
- all fixed, all up front: Salesforce's dollar (22 cents to deliver, 14 to engineering, 35 to selling, 20 of operating
  income); Microsoft's licences and devices at 19 cents to deliver against 35 for services; seven companies' cost
  structures; stock pay from 8 cents a dollar at Salesforce and Adobe to 34 at Snowflake;
- from licence to subscription: the Works' J-curve, with revenue falling 35% in the year of the switch; Adobe's revenue from
  $4.40bn (2012) to $4.06bn (2013) and $23.8bn (2025); licences from 81% of revenue to 61%; 1.4 million paid Creative Cloud
  subscriptions; 96% subscriptions today;
- the layer cake: cohorts; net revenue retention of 125% at Snowflake and about 120% at Datadog; a dollar of new ARR worth
  $5.68 of gross profit over ten years against $1.56 to win; ServiceNow's 603 customers paying over $5m and Snowflake's 733
  over $1m;
- paid in advance: annual invoices and deferred revenue; Salesforce's $8.3bn of operating income against $15.0bn of
  operating cash flow and $24bn of deferred revenue; its $72.4bn of contracted revenue; Microsoft's $678bn and Oracle's
  $638bn backlogs;
- an intermission: business investment in software from almost nothing in 1960 to 2.5% of GDP; software prices flat
  since 1997 while consumer prices doubled; 2.4 million Americans in computer systems design;
- selling it: Salesforce's selling costs of 43 to 53 cents a dollar for fifteen years and its margin near zero, then 35
  cents and 20%; growth against free cash flow and the rule of forty; CrowdStrike's $5.3bn of ARR and $1.0bn net new;
  Atlassian's self-service flywheel against Salesforce's sales teams;
- lock-in and platforms: the system of record; ARR after five years from $530m at 4% churn to $343m at 16%; Microsoft 365
  seats up 6% and revenue up 17%; platforms, open source, the clouds and vertical software;
- when the copy stops being free: Microsoft's additions to property and equipment from $8bn (2016) to $116bn (2026); its
  free cash flow from $74bn to $67bn; its cloud gross margin down to 66%; Oracle's capital spending of $56bn and free cash
  flow of -$24bn; seats against agents;
- the landscape, November 2026: thirty-one companies by revenue and five-year median operating margin; operating income in
  dollars; the map;
- *Called it?*: Salesforce's target of more than $50bn of revenue for fiscal 2026, set in 2021, against $41.5bn; and this
  series' call of 55% that Microsoft Cloud revenue reaches $275bn in fiscal 2027; what to watch;
- paid for the next copy: the answer, and Part 37, cloud and data centres.

## Build it

```bash
python -m videos.industry.industry36.compute               # every number, printed
EXPLAINER_TTS=silent python tools/build.py industry36 -q l  # the whole part, silent preview
python tools/build.py industry36                           # 1080p30 with narration
python -m videos.industry.labs 36                          # the lab
python -m pytest tests/industry                            # the Register and the Works (test_saas.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p36.py`) or comes from the Filing Room: the companies'
accounts (`sec_soft.csv`) and the BEA's, BLS's and Federal Reserve's series (`fred_soft.csv`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The free copy | The first copy and the next; Microsoft's revenue and profit; where its revenue went; its growth; the title |
| 1 | Run it: a software company for five years | The company; the first year; operating leverage; salespeople or engineers; cash; price; the lesson |
| 2 | All fixed, all up front | Salesforce's dollar; a copy against a service; seven companies; stock pay; why |
| 3 | From licence to subscription | The Works' J-curve; Adobe's; 2013 inside the dip; Adobe today |
| 4 | The layer cake | Cohorts; net retention; lifetime value; big customers |
| 5 | Paid in advance | Annual billing; cash against profit; the backlog; the largest backlogs |
| — | Intermission | Software investment; software prices; programmers |
| 6 | Selling it | Salesforce's selling and margin; growth against cash; net new ARR; self-service |
| 7 | Lock-in and platforms | The system of record; what churn is worth; bundles; other ways to stay |
| 8 | When the copy stops being free | Microsoft's capital spending and cash; gross margins; Oracle; seats and agents |
| 9 | The landscape, November 2026 | Revenue against margin; operating income in dollars; the map |
| 10 | Called it? | Salesforce's target; this series' call; what to watch |
| — | Paid for the next copy | The answer; Part 37, cloud and data centres |

## What is computed, and from what

`compute.py` reads the Filing Room and the Register. The Works' software company is `explainer/industry/works/saas.py`,
run a quarter at a time: ARR starts at $200m; customers who stay add 10% a year and others take away 8%; 100 ramped
salespeople each bring in $450,000 of new ARR a year, scaled down as the team grows by (1 + 100/300) / (1 + team/300); a
new salesperson takes two quarters to ramp and costs $700,000 a year with the marketing and engineers around them;
engineering is $40m a year; administration 10% of revenue; the gross margin 78%. Extra engineering builds a product stock
that decays 20% a year; each $150m of it cuts churn by half, raises expansion by 60% and sales productivity by 30%. Revenue
is the quarter's average ARR over four; cash is operating income plus the change in deferred revenue, half of ARR. A price
rise reprices renewals over four quarters, adds three points of churn for a year and cuts new business with a price
elasticity of 1.5. Lifetime value discounts gross profit at 10% a year. The J-curve sells a licence for three years'
subscription plus 20% a year of maintenance; after the switch, new customers subscribe and a third of licence owners convert
each year. Margins in the landscape are medians of the last five fiscal years; SAP's euros are converted at the Federal
Reserve's annual average rate.

## Problems and solutions

**1.** *A company starts the year with $300m of ARR. Customers who stay add 12% and others take away 7%; its sales team
brings in $60m of new ARR. What is ARR at the year's end, and what is net revenue retention?*

*Solution.* 300 + 36 - 21 + 60 = $375m, growth of 25%. Net revenue retention: (300 + 36 - 21) / 300 = 105%.

**2.** *A company spends $90m a year on sales and marketing and wins $50m of new ARR at an 80% gross margin. How many months
does the selling take to pay back, and what is the 'magic number' if ARR rose $65m in all?*

*Solution.* Payback: 12 x 90 / (50 x 0.8) = 27 months. Magic number: 65 / 90 = 0.72.

**3.** *A licence costs $3,000 plus $600 a year of maintenance; a subscription costs $1,000 a year. A company switches and its
new customers subscribe. How much less does it collect from a new customer in the first year, and in which year does the
subscription bring in more in total?*

*Solution.* First year: $1,000 against $3,000, $2,000 less. Totals: licence 3,000 + 600(n - 1); subscription 1,000n. They are
equal when 1,000n = 2,400 + 600n, n = 6: from the seventh year the subscriber has paid more.

**4.** *Salesforce's operating income was $8.3bn and its deferred revenue rose by about $3.6bn during the year; it paid $3.5bn
of its staff's pay in shares. Roughly what was its operating cash flow, before tax, interest and other items?*

*Solution.* 8.3 + 3.6 + 3.5 = $15.4bn, close to the $15.0bn reported: customers paying ahead and stock pay explain most
of the gap between cash and profit.

**5.** *Microsoft Cloud revenue was $214.4bn in fiscal 2026. What growth does fiscal 2027 need to reach $275bn, and if the
first quarter grew 30% to $63.9bn, what must the other three quarters bring in?*

*Solution.* 275 / 214.4 - 1 = 28.3%. The other three quarters must bring in 275 - 63.9 = $211.1bn. In fiscal 2026 those
quarters brought about 214.4 - 63.9 / 1.30 = $165.3bn, so they need 27.7% growth.

## Glossary

- **Annual recurring revenue (ARR):** the yearly value of subscriptions in force.
- **Churn:** revenue lost as customers leave or cut back.
- **Expansion:** extra revenue from customers who stay.
- **Net revenue retention:** this year's revenue from last year's customers, against last year's.
- **Cohort:** the customers who signed up in the same period.
- **Payback:** months of gross profit needed to recover the cost of winning a customer.
- **Deferred revenue:** money received for service not yet delivered.
- **Remaining performance obligation (RPO):** all revenue under contract not yet recognized.
- **Perpetual licence:** a one-time purchase of the right to use a version of software for ever.
- **Stock-based compensation:** pay in shares, an expense that uses no cash but dilutes owners.
- **System of record:** the software that holds a company's authoritative data for some function.
- **Rule of forty:** the rule of thumb that revenue growth plus profit margin should be at least 40%.

## Lab and interactive

- `python -m videos.industry.labs 36`: the Works' company by churn, budget split and price; unit economics and lifetime
  value; cohorts; the J-curve against Adobe's; costs, stock pay and growth against cash; capital spending; and this
  series' call.
- The interactive (course site): run a software company. Set churn, expansion and the gross margin, an extra budget and its
  split between salespeople and engineers, and a price rise, and see five years of ARR, the trade between ARR and cash, and
  the margin.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p36.py`) or the Filing Room
(`explainer/industry/data/SOURCES.md`). The main ones:

- SEC EDGAR: the Forms 10-K of Microsoft and Atlassian for fiscal 2026, Oracle for fiscal 2026, Salesforce, Snowflake,
  CrowdStrike and Workday for fiscal 2026, Adobe for fiscal 2025 and fiscal 2013, ServiceNow and Datadog for 2025;
  Microsoft's 10-Q for the first quarter of fiscal 2027 and Salesforce's for the second; Salesforce's Forms 8-K of
  September 2021 and 2022; the company facts of thirty software companies and SAP's Form 20-F.
- FRED: the BEA's private fixed investment in software and in information processing equipment and software, and GDP; the
  BLS's producer price index for software publishers, the CPI, and employment in computer systems design and in
  information; the Federal Reserve's dollar-euro rate.
