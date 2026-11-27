# Industry, Built: Part 28, Airlines

Part 28 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second of Act V, *Moving*. It asks: why has an industry that changed the world lost
money over most of its history? It answers with Delta's Form 10-K for 2025 and its results releases of January, April, July
and October 2026; the Forms 10-K for 2025 of Southwest, American and Spirit Aviation Holdings; the SEC company facts of
seventeen airlines, lessors and a booking system; the Airline Deregulation Act of 1978 and the CARES Act of 2020; Ken
Littlewood's rule of 1972; Berkshire Hathaway's letter for 2007; FRED's traffic, fuel, fare and employment series; and the
Works' flight. The answer: an airline sells the most perishable thing there is, a seat on a departing flight, at a cost fixed
in advance, so every airline is tempted to fill the last seat at any price; competition, unleashed in 1978, pushes the
margin on a seat-mile towards zero; its second-largest cost is set by wars and oil markets; and most of the rest cannot be
cut when the passengers stop coming. The airlines that do well have found money outside the seat, above all in the banks
that buy their miles, and the steadiest money is with whoever owns the planes and rents them out.

It opens on Warren Buffett's line about Kitty Hawk, on American airline fares after inflation (down 43% from 2000 to 2025,
by the CPI), and on nine listed American airlines' profits: $78bn over 2009-2025 on $2.46tn of revenue, about three cents
a dollar, with a loss of $35bn in 2020. From there it covers:

- Run it: sell one flight. In the Works a 180-seat flight of 1,000 miles costs $28,800 to fly; about 190 holidaymakers will
  pay at most $129 and book early, about 40 business travellers will pay $429 and book late. Selling to whoever comes first
  fills the plane, turns away 38 business travellers and loses $5,028; one fare of $429 loses $11,633. Holding 44 seats back
  for the late bookers, by Littlewood's rule (hold a seat while the chance it will be wanted at the high fare exceeds
  129/429 = 30%), makes $5,457; overbooking by 14, with 8% no-shows and $900 to each bumped traveller, makes $6,975. With a
  business fare of $600, hold 46 and make $12,119;
- a seat-mile: Delta's 298bn seat-miles, 250bn sold, 84% full; its yield of 20.74 cents, PRASM 17.37, TRASM 21.26, CASM 19.31
  and CASM-ex 13.86; revenue against cost per seat-mile at Delta (+1.95 cents), Southwest (+0.24) and Spirit (-1.92); the
  load each needed to break even at its fares (76%, 76% and 94%, this series' arithmetic) against the load each flew (84%,
  77% and 78%); Southwest's $190 average fare, 780-mile flight, 134m passengers, 803 aircraft and 1.42m trips;
- where the dollar goes: Delta's $57.5bn of costs (30% people, 17% fuel) in thirteen lines; about $170,000 a head of pay and
  benefits and $13,000 of profit-sharing; 91 cents of each dollar in costs, a net income of $5.0bn on $63.4bn; then 2020:
  planes 14% full in April, revenue down by three-fifths at Delta, United, American and Southwest with operating losses of
  $3.8-12.5bn, and up to $25bn of public money for passenger airlines' payrolls;
- fuel and the war: jet fuel from $1.10 a gallon (2020) to $3.37 (2022) and $2.12 (2025); month by month, from $2.26 in
  February 2026 to $3.70 in March and $3.94 in May with Hormuz all but shut; Delta's all-in fuel from $2.30 in 2025 to an
  expected $4.30, $3.15 and $4.25 for the last three quarters of 2026; a $6bn rise in fuel costs against a $4.5bn pre-tax
  profit; American fares 27% higher in May 2026 than a year before; Southwest's seat-miles per gallon from 77.3 to 83.0;
- the bank in the airline: American Express paid Delta $8.2bn in 2025, more than its net income of $5.0bn; American's card
  and partners paid it $6.2bn against a net income of $111m; Delta's $9.3bn of SkyMiles revenue paid for but not yet earned;
  loyalty revenue up 18% in the third quarter of 2026;
- an intermission: the load factor from 72% (2000) to 84% (2019); seat-miles flown and sold; passengers from 669m (2000) to
  927m (2019), 372m (2020) and 972m (2025); air transport jobs from 634k (2001) to 439k (2013) and 574k (2026);
- low cost, and lower: operating margins since 2021 (Delta about 9%, Southwest 1.5%, JetBlue negative every year, Spirit
  -22.5% in 2024); Spirit's two bankruptcies and its fleet from 213 aircraft to 131; Southwest's bag fees and assigned seats,
  its fare from $178 to $190, passengers from 140m to 134m and load from 80.4% to 77.4%;
- who owns the planes: AerCap's and Air Lease's median margins of 26% and 21% against Delta's 5.6%, United's 4.9% and
  Southwest's 1.8%; AerCap's $3.75bn of profit on $8.5bn of revenue against Delta's $5.0bn on $63.4bn;
- the landscape, November 2026: the four largest American airlines with 87% of the revenue of eight; fifteen companies by
  revenue and margin; the map of the business;
- *Called it?*: the Deregulation Act's promise; Delta's 2026 forecast cut from $6.50-7.50 a share in January to $5.10-5.60 in
  October; and this series' call that Gulf Coast jet fuel will average more than $3.00 a gallon over 2027 (40%);
- perishable seats, fixed costs: the six answers.

## Build it

```bash
python -m videos.industry.industry28.compute               # every number, printed
EXPLAINER_TTS=silent python tools/build.py industry28 -q l  # the whole part, silent preview
python tools/build.py industry28                           # 1080p30 with narration
python -m videos.industry.labs 28                          # the lab
python -m pytest tests/industry                            # the Register and the Works (test_airline.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p28.py`) or comes from the Filing Room: the companies'
accounts (`sec_air.csv`) and FRED's traffic, fuel, fare, price and employment series (`fred_air.csv`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Shooting Orville down | Buffett's line; real fares; nine airlines' profits; the title |
| 1 | Run it: sell one flight | The flight; two travellers; first come; one high fare; holding seats back; the result; overbooking; a dearer business fare; the lesson |
| 2 | A seat-mile | The unit; the vocabulary; three airlines' margins; load factors; break-even loads; Southwest in numbers |
| 3 | Where the dollar goes | Delta's costs; in full; per head; the profit; April 2020; revenue and losses in 2020; the rescue |
| 4 | Fuel and the war | Jet fuel since 2000; the last year; Delta's fuel by quarter; the $6bn; fares in 2026; efficiency |
| 5 | The bank in the airline | American Express and Delta; American's cards; the miles owed; how it works |
| — | Intermission | Load factor; seat-miles; passengers; jobs |
| 6 | Low cost, and lower | Margins since 2021; Spirit; Southwest changes course; why the cheapest lost |
| 7 | Who owns the planes | Lessors' margins; the scale; why the lessor keeps more |
| 8 | The landscape, November 2026 | The big four; revenue against margin; the map |
| 9 | Called it? | The 1978 law; Delta's forecast; this series' call; what to watch |
| — | Perishable seats, fixed costs | The six answers; Part 29, rail, trucks and parcels |

## What is computed, and from what

`compute.py` reads the Filing Room and the Register. The flight is the Works' (`explainer/industry/works/airline.py`): 180
seats, 1,000 miles, a cost of 16 cents a seat-mile; leisure demand is Poisson with mean 190 at $129 and arrives first,
business demand Poisson with mean 40 at $429 and arrives last; 8% of booked travellers do not show, independently; each
bumped traveller is paid $900; every result is the average of 40,000 simulated flights (seed 28). Littlewood's protection
level is the largest y with P(business demand ≥ y) above the fare ratio. Real fares are the CPI for airline fares over the
CPI for all items, annual averages, 2000 = 1. Industry profits are the sum of net income of Delta, United, American,
Southwest, JetBlue, Alaska, Frontier, Allegiant and Hawaiian (Spirit's filed net income is mis-scaled and left out). A
break-even load is cost per seat-mile over revenue per passenger-mile (revenue per seat-mile over the load factor). Margins
are net income over revenue, the median of 2021-2025 or of the last five fiscal years; the cheap carriers' are operating
income over revenue. Passengers a year are twelve times the mean of the monthly enplanements; jet fuel and fares by year are
means of the months.

## Problems and solutions

**1.** *A flight costs $28,800 to fly whether full or empty. Holidaymakers pay $129 and business travellers $429. If 150
holidaymakers and 30 business travellers fly, what does the flight make? If instead 180 holidaymakers fill it, what does it
make?*

*Solution.* 150 × 129 + 30 × 429 = 19,350 + 12,870 = $32,220, a profit of $3,420. All holidaymakers: 180 × 129 = $23,220, a loss
of $5,580. The plane is full both times; thirty seats sold to the right people at the right price make the whole difference.

**2.** *Littlewood's rule: hold the y-th seat for business travellers while the chance that business demand reaches y exceeds
the ratio of the low fare to the high. With fares of $129 and $429, what is the threshold? If business travellers will pay
$600, does the airline hold more seats back or fewer?*

*Solution.* 129 / 429 = 30%. At $600 the ratio falls to 129 / 600 = 21.5%, so a seat is worth holding at a lower chance of being
wanted: the airline holds more back (46 seats instead of 44 in the Works).

**3.** *Delta earned 21.26 cents of revenue per seat-mile in 2025 with planes 84% full, and its costs were 19.31 cents per
seat-mile. How full did its planes need to be to cover costs at those fares? Spirit earned 9.51 cents at 78.4% full and spent
11.43: what load did it need?*

*Solution.* Revenue per passenger-mile is 21.26 / 0.84 = 25.3 cents, so the break-even load is 19.31 / 25.3 = 76%. For Spirit,
9.51 / 0.784 = 12.13 cents, and 11.43 / 12.13 = 94%. Delta had eight points to spare; Spirit would have needed its planes almost
full on every flight, at its fares.

**4.** *Delta burned 4,269 million gallons of fuel in 2025 at $2.30 a gallon. If the 2026 price averaged $3.70 on the same
gallons, how much more would fuel cost? Compare with the $6bn Delta reported.*

*Solution.* 4,269m × (3.70 - 2.30) = $6.0bn: the reported figure is what the gallons of 2025 cost at the dearer price. It is more
than Delta's net income of $5.0bn in 2025.

**5.** *American Express paid Delta $8.2bn in 2025 and Delta's net income was $5.0bn; American's card and partners paid it $6.2bn
and its net income was $111m. Suppose a recession cut both programmes' payments by a fifth and nothing else changed. What
would each airline's net income be, ignoring tax?*

*Solution.* Delta: 5.0 - 0.2 × 8.2 = $3.36bn. American: 0.111 - 0.2 × 6.2 = -$1.13bn, a loss. The card money is the airlines' most
reliable income, but at American it is also most of the margin between profit and loss.

## Glossary

- **Available seat-mile (ASM):** one seat flown one mile, whether or not anyone sits in it.
- **Revenue passenger-mile (RPM):** one paying passenger flown one mile.
- **Load factor:** RPMs over ASMs, the share of seats filled.
- **Yield:** passenger revenue per RPM.
- **PRASM, TRASM:** passenger revenue, or all revenue, per ASM.
- **CASM, CASM-ex:** cost per ASM, with all costs or without fuel and some other items.
- **Revenue management:** setting how many seats to sell at each fare and when, as Littlewood's rule does.
- **Overbooking:** selling more seats than the aircraft has, expecting some travellers not to show.
- **Co-branded card:** a credit card issued by a bank with an airline's name, whose spending earns the airline's miles.
- **Deferred revenue (of a loyalty programme):** money received for miles not yet spent, recognized when the miles are flown.
- **Lessor:** a company that owns aircraft and rents them to airlines.
- **Ultra-low-cost carrier:** an airline that sells the lowest fares and charges separately for bags, seats and everything else.

## Lab and interactive

- `python -m videos.industry.labs 28`: the Works' flight under four ways of selling it; Littlewood's level by fare ratio and
  overbooking against the bump payment; seat-mile arithmetic and break-even loads for three airlines; Delta's costs and fuel;
  2020; the card money; the lessors; and this series' call.
- The interactive (course site): sell a flight. Choose the two fares, how many seats to hold back and how many to oversell,
  and see the passengers, the revenue, the bumped travellers and the profit, with Littlewood's level marked.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p28.py`) or the Filing Room
(`explainer/industry/data/SOURCES.md`). The main ones:

- SEC EDGAR: Delta's Form 10-K for 2025 and its results releases of 13 January, 8 April, 10 July and 9 October 2026 (Forms 8-K);
  the Forms 10-K for 2025 of Southwest Airlines, American Airlines Group and Spirit Aviation Holdings; the company facts of
  American, Delta, United, Southwest, JetBlue, Alaska, Frontier, Spirit, Allegiant, SkyWest, Copa, Ryanair, LATAM, AerCap,
  Air Lease, Sabre and Hawaiian.
- Public Law 95-504, the Airline Deregulation Act of 1978, and Public Law 116-136, the CARES Act of 2020, section 4112
  (govinfo).
- FRED: the Bureau of Transportation Statistics' load factor, seat-miles, passenger-miles and enplanements; the EIA's Gulf
  Coast jet fuel price; the BLS's CPI for airline fares and all items, producer prices for scheduled passenger air
  transportation and employment in air transportation.
- Ken Littlewood, 'Forecasting and control of passenger bookings', AGIFORS Symposium Proceedings 12 (1972), reprinted in the
  Journal of Revenue and Pricing Management 4(2), 2005.
- Berkshire Hathaway, letter to shareholders for 2007.
