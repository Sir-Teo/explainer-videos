# Industry, Built: Part 30, Telecoms

Part 30 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth of Act V, *Moving*. It asks: why do the companies that carry everything
capture so little of what it is worth? It answers with the Forms 10-K for 2025 of Verizon, AT&T, T-Mobile, Charter,
Comcast, American Tower, EchoStar and AST SpaceMobile; the 10-Qs for the third quarter of 2026 of AT&T, Charter and Comcast;
Verizon's 10-K for 2020 and AT&T's for 2021 on the C-Band auction; DISH Network's 10-K for 2019; the SEC company facts of
thirty-four carriers, cable, tower, satellite and equipment companies and three companies whose services run over the
networks; FRED's telephone prices and telecom jobs; and the Works' auction, subscriber and tower. The answer: the
carriers pay up front for airwaves sold like land; three networks sell nearly the same thing to customers who leave for a
better price; the network is never finished; the scarce pieces, the airwaves and the tower sites, belong to governments
and landlords; and the value of what travels over the pipe belongs to whoever made it, not to whoever carried it.

It opens on Verizon, AT&T and T-Mobile, whose revenue rose from $311bn in 2015 to $352bn in 2025, against Alphabet, Meta
and Netflix, from $100bn to $649bn; on their operating margins (Meta 41%, Alphabet 32%, Netflix 30% against the carriers'
19-21%); and on telephone service, 7% cheaper in dollars than in 1998 and 53% cheaper after inflation. From there it covers:

- Run it: bid for spectrum. Eight blocks are sold by a rising clock at one price for all. Your blocks are worth $9.5bn,
  $9.0bn, $7.0bn and $6.5bn; three rivals have their own values. Bidding for every block worth the price, demand falls to
  eight only at $6.75bn a block: you win three and keep $5.25bn. Asking for two, the rivals' demand alone falls to six at
  $4.75bn: you win two and keep $9.00bn, every rival is better off, and the auction raises $38bn instead of $54bn. What a
  government auctioneer can do about it;
- a subscriber: Verizon's consumer accounts paid $147.31 a month for 2.95 lines (T-Mobile's $148.97); Verizon sold $25.5bn
  of phones that cost it $29.0bn; churn of 0.92% a month means about nine years' stay and, at a 45% margin and $600 to win
  an account (assumptions), a lifetime worth of about $6,605; lines per account rising from 2.84 to 2.95 as accounts fell;
  the worth by churn rate; AT&T's churn 0.90%, T-Mobile's 0.93%;
- the network: the phone, the tower, the backhaul, the core and the internet; Verizon's dollar (20 cents services and
  network, 21 phones, 24 selling and overheads, 13 depreciation, 21 operating profit); capital spending of 11-17% of the
  carriers' revenue and 21% of Charter's; Verizon's 89,900 staff; the three carriers' $48bn of capital spending against
  Alphabet's $91bn and Meta's $70bn;
- invisible land: low, mid and millimetre-wave bands; Verizon's $45.5bn of C-Band licences in 2021 and AT&T's $25.5bn of
  acquisitions; EchoStar's sales to AT&T ($22.65bn, closed 28 July 2026) and SpaceX (about $20bn); its $15.0bn of revenue
  and $17.7bn operating loss in 2025, after it 'terminated' its 5G network;
- the landlord of the air: American Tower's 149,686 sites, 42,224 in the US and Canada, earning $124k a site a year against
  $20.6k of costs; 80 cents of segment operating profit per dollar; the Works' tower returning 8%, 23% and 38% a year with
  one, two and three tenants; its segments abroad; its operating margin of 46% against T-Mobile's 21%, with T-Mobile, AT&T
  and Verizon 18%, 17% and 14% of its revenue;
- an intermission: telephone prices against all prices since 1997; telecom jobs from 1.46 million (2001) to 559,000 (2026);
  the five largest carriers' revenue; Lumen's from $21.5bn (2019) to $12.4bn (2025);
- three networks: T-Mobile's revenue from $32.5bn (2015) to $88.3bn (2025) after the Sprint merger of 1 April 2020; its
  142.4m customers; churn and revenue per account side by side; three operating margins converging on a fifth;
- the wire to the home: Comcast down 711,000 broadband customers and Charter 403,000 in 2025; Verizon's fixed wireless up
  693,000 and AT&T Internet Air 875,000; the stocks (Comcast 31.3m, Charter 29.7m, AT&T fibre 10.4m); Charter's 11.8m mobile
  lines on Verizon's network; Verizon-Frontier, AT&T-Lumen, Charter-Cox and T-Mobile-UScellular;
- what runs over the pipe: the two sets of revenue as bars and company by company; Verizon's 12 cents of capital spending
  per dollar against Netflix's 1.5; Ericsson and Nokia; AST SpaceMobile ($71m of revenue, $1.06bn of capital spending),
  Iridium and SpaceX; this series' reading of why the pipe captures so little;
- the landscape, November 2026: twenty-three companies by revenue and margin; Vodafone's revenue from EUR 49.8bn to
  EUR 37.4bn; the map of the business;
- *Called it?*: DISH's 2019 commitment to a fourth network against its abandonment in 2025; and this series' call that
  Comcast will report fewer domestic broadband customers at the end of 2027 than at the end of 2026 (80%); what to watch;
- essential, costly, alike: the five answers.

## Build it

```bash
python -m videos.industry.industry30.compute               # every number, printed
EXPLAINER_TTS=silent python tools/build.py industry30 -q l  # the whole part, silent preview
python tools/build.py industry30                           # 1080p30 with narration
python -m videos.industry.labs 30                          # the lab
python -m pytest tests/industry                            # the Register and the Works (test_telco.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p30.py`) or comes from the Filing Room: the companies'
accounts (`sec_tel.csv`) and FRED's price and employment series (`fred_tel.csv`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The pipe and what runs through it | Revenue of the carriers and of Alphabet, Meta and Netflix; margins; phone prices; the title |
| 1 | Run it: bid for spectrum | The rules; the values; where values come from; honest bidding; the rounds; holding back; everyone gains; the seller; the lesson |
| 2 | A subscriber | The bill; the phone; a lifetime; lines per account; churn |
| 3 | The network | The path of a call; Verizon's dollar; capital spending; people; the giants' spending |
| 4 | Invisible land | Bands; C-Band; EchoStar's sales; its loss |
| 5 | The landlord of the air | American Tower's sites; a dollar of rent; tenants; abroad; margins |
| — | Intermission | Phone prices; jobs; revenue; copper |
| 6 | Three networks | T-Mobile's rise; customers; churn and revenue alike; margins |
| 7 | The wire to the home | Flows; stocks; cable's mobile lines; the deals |
| 8 | What runs over the pipe | Revenue as bars; company by company; capital intensity; equipment; space; the reading |
| 9 | The landscape, November 2026 | Revenue against margin; Vodafone; the map |
| 10 | Called it? | DISH's fourth network; this series' call; what to watch |
| — | Essential, costly, alike | The five answers; Part 31, grocery and mass retail |

## What is computed, and from what

`compute.py` reads the Filing Room and the Register. The Works' telecoms are `explainer/industry/works/telco.py`. The
auction sells eight blocks by a clock rising $0.25bn a round; each bidder wants the blocks it values at or above the price,
up to its cap, and every winner pays the price at which the blocks wanted first fall to eight or fewer; the four bidders'
values are this series' illustration. A subscriber's worth is ARPA times a margin of 45% over the monthly churn, less $600
to win the account (assumptions; ARPA and churn are Verizon's 2025 Consumer figures), without discounting. A tower costs
$300k, earns $45k a year a tenant (assumptions) and costs American Tower's 2025 U.S. & Canada segment operating expenses per
site to run. Operating margins are operating income over revenue; landscape margins are net income over revenue, the median
of the last five fiscal years, for companies reporting in dollars, euros and Canadian dollars. Real telephone prices are the
CPI for telephone services over the CPI for all items, annual averages, 1998 = 1.

## Problems and solutions

**1.** *In the Works' auction, your values are $9.5bn, $9.0bn, $7.0bn and $6.5bn. With honest bidding the clock stops at
$6.75bn and you win three blocks; asking for two, it stops at $4.75bn. What do you keep in each case, and what did the
government lose?*

*Solution.* Three blocks: 9.5 + 9.0 + 7.0 - 3 × 6.75 = 25.5 - 20.25 = $5.25bn. Two blocks: 9.5 + 9.0 - 2 × 4.75 = $9.0bn. The
government sold eight blocks at $6.75bn ($54bn) in the first case and at $4.75bn ($38bn) in the second: $16bn less.

**2.** *An account pays $147.31 a month, 45% of which is left after serving it, and 0.92% of accounts leave each month. How
long does an account stay on average, and what is it worth if winning it cost $600? What if churn rises to 1.5%?*

*Solution.* 1 / 0.0092 = 109 months, about nine years. Worth: 147.31 × 0.45 / 0.0092 - 600 = 7,205 - 600 = $6,605. At 1.5%,
147.31 × 0.45 / 0.015 - 600 = 4,419 - 600 = $3,819: churn up by three-fifths cuts the worth by more than two-fifths.

**3.** *A tower costs $300,000 to build and $20,600 a year to run; each tenant pays $45,000 a year. What does it return a
year with one, two and three tenants? Why does a tower company want more tenants on old towers rather than new towers?*

*Solution.* One: (45,000 - 20,600) / 300,000 = 8.1%. Two: (90,000 - 20,600) / 300,000 = 23.1%. Three: 38.1%. Each extra tenant
adds $45,000 of rent and almost no cost to a tower already built, while a new tower starts again at 8%.

**4.** *Verizon took in $138.2bn in 2025 and spent $17.0bn on capital projects; Netflix took in $45.2bn and spent $0.69bn.
What is each one's capital spending per dollar of revenue? Verizon sold phones for $25.5bn that cost it $29.0bn: what was the
subsidy per dollar of its service revenue of $112.7bn?*

*Solution.* Verizon 17.0 / 138.2 = 12.3 cents; Netflix 0.69 / 45.2 = 1.5 cents. The subsidy was 29.0 - 25.5 = $3.5bn, about 3.1
cents per dollar of service revenue: a cost of keeping customers, paid every year.

**5.** *Comcast had 31.84m domestic broadband customers at the end of 2024 and 31.26m at the end of 2025. If it lost the same
number each year, how many would it have at the end of 2027? If it lost 2.3% a year instead, how many?*

*Solution.* By these totals it lost 587,000 (its reported net loss was 711,000; the two need not match exactly). At 587,000 a year: 31.26 - 2 × 0.587 = 30.08m. At 2.3% a year: 31.26 × 0.977² = 29.84m. Either way, the call that it
ends 2027 with fewer than it ends 2026 with needs only that the loss continue.

## Glossary

- **Spectrum:** a band of radio frequencies; a licence gives the right to use one across a territory.
- **Clock auction:** an auction in which the price rises round by round and bidders say how much they want at each price.
- **Demand reduction:** bidding for fewer units than you value, to stop the price rising.
- **ARPA, ARPU:** average revenue per account, or per user, a month.
- **Churn:** the share of customers who leave in a month.
- **Postpaid, prepaid:** billed after the month on a plan, or paid in advance.
- **Backhaul:** the link from a tower to the rest of the network, usually fibre.
- **Fixed wireless access (FWA):** home internet delivered over a mobile network to a receiver in the house.
- **MVNO:** a mobile virtual network operator, which sells service on another company's network.
- **Tower company:** a company that owns towers and rents space on them to carriers.
- **Co-location:** more than one carrier's antennas on the same tower.

## Lab and interactive

- `python -m videos.industry.labs 30`: the Works' auction under each cap; a subscriber's worth by churn; a tower by tenants;
  the carriers' and the over-the-top companies' revenue and margins; capital spending; spectrum deals; American Tower;
  broadband flows; and this series' call.
- The interactive (course site): bid for spectrum. Set your values for four blocks, how many you will ask for and how many
  are on offer, and see the clock, the price, what each bidder wins and what you keep by the number you ask for.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p30.py`) or the Filing Room
(`explainer/industry/data/SOURCES.md`). The main ones:

- SEC EDGAR: the Forms 10-K for 2025 of Verizon, AT&T, T-Mobile, Charter, Comcast, American Tower, EchoStar and AST
  SpaceMobile; the Forms 10-Q for the third quarter of 2026 of AT&T, Charter and Comcast; Verizon's Form 10-K for 2020 and
  AT&T's for 2021; DISH Network's Form 10-K for 2019; the company facts of Verizon, AT&T, T-Mobile, Comcast, Charter, Cable
  One, Lumen, Frontier, TDS, EchoStar, American Tower, Crown Castle, SBA, Vodafone, Telefónica, BCE, Rogers, Telus,
  Millicom, Nokia, Ericsson, Iridium, Viasat, AST SpaceMobile, Alphabet, Meta and Netflix.
- FRED: the BLS's CPI for telephone services and all items, employment in telecommunications, and PPIs for wired and
  wireless carriers.
