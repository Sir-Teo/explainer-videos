# Industry, Built: Part 35, Travel and Hotels

Part 35 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth and last of Act VI, *Selling*. It asks: why do the biggest hotel companies own
almost no hotels? It answers with the Forms 10-K for 2025 of Marriott International, Hilton, Host Hotels & Resorts, Booking
Holdings, Expedia, Airbnb, Royal Caribbean and Las Vegas Sands, Carnival's for the year to November 2025 and Disney's for
the year to October 2026; Marriott's and Booking's 10-Qs for the third quarter of 2026; Host Marriott's 10-K for 1993 and
Park Hotels' for 2020; Booking's 10-Ks for 2020 and 2023, Carnival's for 2020 and Las Vegas Sands' for 2019 and 2020; the
Nevada Gaming Control Board's revenue report for 2025; the SEC company facts of thirty-two hotel, travel, cruise, casino
and park companies; the BLS's and BTS's series on room prices, airfares, hotel jobs and passengers; and the Works' hotel.
The answer: because what a hotel brand sells is not the building but the guest, a name, a booking system and a loyalty
programme; because owners pay for the buildings, borrow against them and are paid last, while the brand's fees come off the
top of revenue; because fees on profit arrive only when owners have done well; because the online agents in the middle
earn the most of all; and because the businesses that still own their capacity, ships, casinos and parks, live by keeping
it full.

It opens on Marriott's 1,779,936 rooms at the end of 2025, of which it owned or leased 51 hotels, 0.8% of the rooms; on its
rooms by contract (66% franchised, 32% managed for owners); on its $26.2bn of revenue, of which $19.2bn was owners' costs
passed through and $5.4bn fees, with $4.1bn of operating income; on the split of Marriott Corporation on 8 October 1993
into Host Marriott, with the hotels and the debt, and Marriott International; and on the two halves today, Marriott earning
15 cents of operating income on a dollar of assets and Host about 7. From there it covers:

- Run it: fill a hotel for a year. In the Works, a 200-room branded hotel cost $36m, 60% borrowed, pays the brand 10% of
  room revenue and sells a quarter of its rooms through online agents at 17%. One rate all year earns most at $180: 70% of
  rooms sold and $2.81m before interest ($2.54m at $150 and 85% full; $2.63m at $220 and 53%). Rates for each month, from
  $144 to $200, make $2.88m with 75% sold. A dollar of revenue: 51 cents to running costs, 9 to the brand, 6 to agents and
  cards, 4 to a refurbishment reserve, 14 to interest and 11 to the owner, $1.07m, 7.4% on $14.4m. Independent, with 15%
  less demand and half its rooms sold by agents, it makes $2.60m;
- the night that perishes: Marriott's 69.3% occupancy at $185.81, $128.80 a room; Hilton's 71.5% at $159.89; Host's $229
  of room revenue and $383 in all per available room; the Works' hotel half empty in December and turning guests away in
  July; Host's revenue (rooms 60%, food and drink 30%) and costs (wages 58% of the operating departments'); flow-through,
  84 cents of a rate rise against 66 of more rooms sold;
- owner, brand, operator: franchise royalties of 4 to 7% of room revenue, management fees of 2 to 3% of revenue and
  incentive fees of 10 to 20% of profit after a priority return; incentive fees paid by 69% of Marriott's managed hotels,
  32% in the U.S. and Canada; Marriott's $3.3bn of franchise fees, $1.3bn of base and $0.8bn of incentive fees; Hilton's
  $2.8bn and $0.7bn; the Works' hotel paying no incentive fee; reimbursed payroll;
- why the brand owns nothing: operating income on assets of 12 to 22% at the brands against 3 to 8% at the owners; Hilton's
  spin-off of Park in January 2017; pipelines of 610,000 and 520,500 rooms; four reasons and the conflict built in;
- the loyalty machine: members' 75% of Marriott's U.S. room nights and 68% worldwide; Hilton Honors' 243 million members;
  co-branded credit cards; channel costs; a members' discount that pays only if it moves many bookings;
- an intermission: Booking's room nights from 845 million (2019) to 355 million (2020) and 1,235 million (2025); hotel
  rooms, airfares and all prices since 2019; passengers on US airlines; jobs in US hotels, still below 2019;
- the online agents: Booking's $186bn of bookings, 14.5% kept, $8.8bn of operating income; agency against merchant;
  marketing of 30% of revenue at Booking and 50% at Expedia; 4.4 million places on Booking.com, 0.5 million of them hotels;
  Spain's 2024 fine on parity clauses and the EU's gatekeeper designation; Airbnb's $91bn of bookings, 13.4% kept, and New
  York's rules of 2023;
- a hotel that moves: Carnival's 13.6 million passengers at 105% occupancy and 101,000 crew; tickets $17.4bn and on board
  $9.2bn; its dollar; $6.8bn of deposits and $26.6bn of debt; the pandemic's $10.2bn loss; 36% of the world's berths;
- the house and the kingdom: the Strip's $8.8bn of gaming win; 2,000 invented roulette players and a house that keeps 14.5%
  of chips bought from a 2.7% edge, against the Strip's 14.9%; Macao's gaming revenue from 293bn patacas (2019) to 60bn
  (2020) and 247bn (2025) and its 35% tax; Marina Bay Sands against Sands' Macao resorts; Disney's parks with $39.6bn of
  revenue and $11.2bn of operating income, 57% of Disney's segments;
- the landscape, November 2026: thirty-two companies by revenue and five-year median net margin; profit in dollars; the
  map;
- *Called it?*: Booking's warning of February 2021 against its room nights, back above 2019 in 2022; and this series' call
  of 35% that Booking reports at least 1.4 billion room nights for 2027; what to watch;
- a brand on someone else's building: the answer, and Part 36, software.

## Build it

```bash
python -m videos.industry.industry35.compute               # every number, printed
EXPLAINER_TTS=silent python tools/build.py industry35 -q l  # the whole part, silent preview
python tools/build.py industry35                           # 1080p30 with narration
python -m videos.industry.labs 35                          # the lab
python -m pytest tests/industry                            # the Register and the Works (test_hotel.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p35.py`) or comes from the Filing Room: the companies'
accounts (`sec_travel.csv`) and the BLS's, BTS's and Federal Reserve's series (`fred_travel.csv`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Whose hotel? | Marriott's rooms and the few it owns; rooms by contract; revenue by kind; the 1993 split; the two halves today; the title |
| 1 | Run it: fill a hotel for a year | The hotel; one rate; a rate a month; the dollar; the owner; branded or not; the lesson |
| 2 | The night that perishes | RevPAR; the perishing night; revenue mix; costs; flow-through |
| 3 | Owner, brand, operator | Three jobs; the franchise; the management contract; incentive fees; the fee lines; the Works under contract; reimbursements |
| 4 | Why the brand owns nothing | Returns on assets; Hilton's spin-off; pipelines; the reasons |
| 5 | The loyalty machine | Members' share; credit cards; channel costs; members' discounts |
| — | Intermission | Room nights; prices; flying; hotel jobs |
| 6 | The online agents | Booking; agency and merchant; marketing; supply; parity rules; Airbnb |
| 7 | A hotel that moves | Carnival's scale; tickets and on board; its dollar; deposits and debt; the pandemic; capacity |
| 8 | The house and the kingdom | The Strip; roulette; hold; Macao; Sands' Singapore; Disney's parks |
| 9 | The landscape, November 2026 | Revenue against margin; profit in dollars; the map |
| 10 | Called it? | Booking's warning; this series' call; what to watch |
| — | A brand on someone else's building | The answer; Part 36, software |

## What is computed, and from what

`compute.py` reads the Filing Room and the Register. The Works' hotel is `explainer/industry/works/hotel.py`: 200 rooms;
demand in an average month is 75% of the rooms at $180 and falls with the rate at an elasticity of 1.5; a seasonal index
from 0.66 (December) to 1.24 (July) scales it; nights within a month scatter around it lognormally (log standard deviation
0.22), and rooms sold on a night are the smaller of demand and the rooms; each room sold costs $35 and each room available
$45 a night; breakfast, parking and the rest add 8% of room revenue at a 30% margin; the brand takes 5.5% royalty and 4.5%
programme fees on room revenue; online agents sell 25% of rooms (50% for an independent, which has 15% less demand) at a
17% commission, and a direct booking costs 3%; a members' discount applies to the 60% of direct bookings made by members and
moves four times its size of the agents' share to direct; the owner reserves 4% of revenue and pays 6.5% on 60% of $180,000
a room. Rates are chosen on a $2 grid, month by month for revenue management. A management contract's base fee is 2.5% of
revenue and its incentive fee 15% of profit after fees and a 10% priority return on the hotel's cost. The roulette table is
single-zero, red winning 18 of 37 spins at even money; 2,000 players each buy $500 of chips and bet $25 a spin for up to 100
spins or until their chips run out. Margins in the landscape are medians of the last five fiscal years; yuan are converted
at the Federal Reserve's annual average rate.

## Problems and solutions

**1.** *A 300-room hotel sold 76,650 room nights last year for $14.6m. What were its occupancy, average daily rate and
RevPAR?*

*Solution.* Rooms available: 300 x 365 = 109,500. Occupancy 76,650 / 109,500 = 70%; ADR 14.6m / 76,650 = $190.48; RevPAR
14.6m / 109,500 = $133.33, which is also 0.70 x 190.48.

**2.** *A franchised hotel's room revenue is $9.4m. It pays a 5.5% royalty and 4.5% programme fees; 25% of rooms are sold by
agents at 17% and the rest direct at 3%. What do the brand and the channels cost it?*

*Solution.* The brand: 10% of $9.4m = $940,000. The channels: 9.4m x (0.25 x 0.17 + 0.75 x 0.03) = 9.4m x 0.065 = $611,000.
In all $1.55m, 16.5 cents of each room dollar.

**3.** *A managed hotel has $10m of revenue and $2.9m of profit before management fees. Its owner paid $36m for it and gets
a 10% priority return. The base fee is 2.5% of revenue and the incentive fee 15% of profit above the base fee and the priority
return. What are the fees?*

*Solution.* Base fee: $250,000. Profit after the base fee: $2.65m, below the $3.6m priority return, so the incentive fee is
zero. To earn any incentive fee the hotel would need more than $3.85m of profit before fees.

**4.** *At single-zero roulette a player bets $25 on red 100 times. What is the expected loss, and what share of a $500
buy-in is it? Why do casinos report a much higher 'win percent' on tables than their edge?*

*Solution.* Each bet loses 1/37 on average: 25 / 37 = $0.68 a spin, $67.57 over 100 spins, 13.5% of the $500 of chips. The
casino's win percent is measured against the chips bought (the drop), and chips are bet again and again, so a 2.7% edge on
each bet becomes a much larger share of the drop.

**5.** *Booking reported 1,235 million room nights for 2025 and 1,007 million for the first nine months of 2026, against 951
million a year earlier. If the fourth quarter grows at the same rate, what is 2026's total, and what growth does 2027 need to
reach 1,400 million?*

*Solution.* Growth so far: 1,007 / 951 = 5.9%. The fourth quarter of 2025 was 1,235 - 951 = 284 million, growing to about 301;
2026 then ends near 1,308 million. Reaching 1,400 needs 1,400 / 1,308 - 1 = 7.0% in 2027.

## Glossary

- **Occupancy:** the share of available rooms sold.
- **Average daily rate (ADR):** room revenue over rooms sold.
- **RevPAR:** room revenue per available room; occupancy times ADR.
- **Franchise:** a contract letting an owner use a brand's name and systems for royalties and fees, and run the hotel.
- **Management contract:** a contract under which a hotel company runs an owner's hotel for a base and an incentive fee.
- **Priority return:** a return an owner receives on its investment before the manager earns an incentive fee.
- **Cost reimbursement revenue:** costs a hotel company pays on owners' behalf, chiefly payroll, and is repaid at cost.
- **Online travel agent (OTA):** a website that sells hotel rooms and other travel for a commission or a margin.
- **Agency and merchant models:** the hotel takes the guest's payment and pays a commission; or the agent takes it and
  pays the hotel.
- **Parity clause:** a contract term by which a hotel promises an agent rates no worse than it offers elsewhere.
- **Drop, win and hold:** chips bought at a table; what the casino keeps; the win as a share of the drop or of what was played.
- **Lower berth:** a cruise cabin's two standard beds, the industry's measure of capacity.

## Lab and interactive

- `python -m videos.industry.labs 35`: the Works' hotel by rate, season, brand and channel; the owner's return; a management
  contract's fees; returns on assets; the agents' take; Carnival's dollar; a night at roulette; and this series' call.
- The interactive (course site): fill a hotel for a year. Set its rate and how far it follows the season, fly a brand's flag
  or go independent, set the agents' share and commission and a members' discount, and see the rooms sold by month, the
  profit by rate, and what the owner keeps.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p35.py`) or the Filing Room
(`explainer/industry/data/SOURCES.md`). The main ones:

- SEC EDGAR: the Forms 10-K for 2025 of Marriott International, Hilton, Host Hotels & Resorts, Booking Holdings, Expedia,
  Airbnb, Royal Caribbean and Las Vegas Sands; Carnival's for the year to 30 November 2025; Disney's for the year to 3
  October 2026; the 10-Qs for the third quarter of 2026 of Marriott and Booking; Host Marriott's 10-K for 1993; Park Hotels'
  10-K for 2020; Booking's 10-Ks for 2020 and 2023; Carnival's for 2020; Las Vegas Sands' for 2019 and 2020; the company facts
  of Marriott, Hilton, Hyatt, IHG, Wyndham, Choice, H World, Atour, Host, Park, Apple Hospitality, Ryman, Booking, Expedia,
  Airbnb, Tripadvisor, Trip.com, MakeMyTrip, Carnival, Royal Caribbean, Norwegian, Las Vegas Sands, Wynn, MGM, Caesars,
  DraftKings, Flutter, United Parks, Six Flags, Marriott Vacations, Hilton Grand Vacations and Sabre.
- Nevada Gaming Control Board: gaming revenue report for December 2025, twelve months, the Las Vegas Strip and statewide.
- FRED: the BLS's consumer prices of lodging away from home, airline fares and all items, its producer price index for hotels
  and employment in accommodation and in amusements, gambling and recreation; the BTS's enplanements and load factor; the
  Federal Reserve's yuan exchange rate.
