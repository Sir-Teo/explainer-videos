# Industry, Built: Part 14, Water and Waste

Part 14 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the seventh and last of Act II, *Out of the Ground*. It asks: why are the businesses
nobody thinks about among the steadiest there are? It answers with Hansard for July and August 1858 and June 2026; the
BLS's consumer and producer price indexes; the EPA's Solid Waste Dilemma (1989), its MSW Facts and Figures (2009, and the
1960-2018 series), its tipping-fee history and its drinking water and clean watersheds needs surveys; 40 CFR Part 258; the
10-Ks of Waste Management, Republic Services, Clean Harbors, American Water and eight other water and waste companies;
Sabesp's 20-F and Veolia's annual report; Britain's Independent Water Commission (July 2025) and the Competition and
Markets Authority's PR24 redeterminations (March 2026); the WHO/UNICEF Joint Monitoring Programme via the World Bank; and
the Works' route, landfill and water company. The answer: water and waste are networks nobody can duplicate, almost all
fixed cost in things that last for decades; a regulator sets the water company's return on its asset base, and the
scarcity of a landfill permit sets the landfill's; their prices follow their costs up, so the bills only rise; and the
owners who want that steadiness, from pension funds to infrastructure investors, can ruin it by borrowing too much
against it.

It opens in London in July 1858, when Disraeli told the Commons the Thames had "really become a Stygian pool, reeking with
ineffable and intolerable horrors", and the Act "for the Purification of that noble River" received royal assent eighteen
days later, to cost about £3 million, paid by a rate of 3d in the pound for forty years. Then: since 1953 the US price index
for water and sewerage has not fallen in a single year, nor that for rubbish collection since 1984; electricity's fell in
eight years and piped gas's in seventeen. From there it covers:

- Run it: the only landfill in a valley, with 30 million tons of room, priced three ways while a rival waits for a
  permit: filling fast is worth about $397m, charging the valley's ceiling about $590m, and charging the ceiling while
  expanding about $623m; if the rival's permit took five years instead of fifteen, $361m, $425m and $452m. Ten years of a
  rival's permitting are worth about $164m; a ton of airspace about $20, against Waste Management's book depletion of
  $6.96 a ton;
- water as a system: river to tap to sewer to river; a cubic metre weighs a tonne; America's drinking water systems need
  $625bn over twenty years ($423bn of it pipes) and its sewers $630bn; 148,000 public water systems, 17,544 public sewage
  works and four million lead service lines; American Water spent $3.5 for each $1 of depreciation in 2025;
- the regulated water company: the Works' £10bn asset base, a 4% real return, 4% run-off and £600m of running costs give
  a bill of £233 a year; investing £900m a year takes the base to about £18bn and the bill to about £340 in twenty-five
  years; gearing at 55% turns 4% into 6.4% with 2% debt and 2.8% with 5% debt; England's companies went from 4% to 72%
  gearing between 1991 and 2009;
- England's experiment: ten water and sewerage companies listed in 1989, three still listed; Ofwat's allowances up from
  £62bn (2020-25) to £104bn (2025-30); the allowed real return from 2.96% to 4.03% (4.20% from the CMA for five
  companies); an average bill of £603 in 2025/26, £43 of its rise from the higher return; £7-13bn of new equity needed;
  Thames Water's £16.8bn of debt, its lenders' rescue proposal of March 2026 and the Environment Secretary's statement of
  16 June 2026;
- public and private elsewhere: a Kentucky rate case (a 9.70% return on equity on a $667m rate base, 52.26% equity);
  American Water's 14 million people in 24 states and its merger with Essential Utilities; Sabesp's privatization on 22
  July 2024 (the State of São Paulo from 50.26% to 18%), its investment from R$6.3bn (2023) to R$15.2bn (2025) and
  universal service brought forward from 2033 to 2029;
- the route: the Works' truck at about $1.10 a stop with the whole street and $1.24 with half; at $1.37 a stop, one hauler
  makes $275 a day, two make $116 each and three lose money; the CPI for rubbish collection doubled after inflation since
  1984; Waste Management's $25.2bn of revenue by line, and its CPI-linked contracts;
- the hole in the ground: the 1991 rule (a 60-mil membrane over two feet of clay, leachate held under 30 cm, thirty years
  of care after closing); landfills from 7,924 (1988) to 1,908 (2009) while tonnage held near 140 million; Waste
  Management's 257 landfills by remaining life (about 38 years on average); Republic's airspace in 2025 (4,745 to 4,872
  million cubic yards after filling 86); internalization (67%); real tipping fees from $17.75 (1985) to $49.21 (1995);
- an intermission: seventy-two years of American bills after inflation: water and sewerage x3.7, rubbish x2.0 since 1984,
  piped gas x1.5, rent x1.1, electricity x0.9;
- recycling and burning: what America did with its municipal waste, 1960-2018 (in 2018, 50% landfilled, 24% recycled, 9%
  composted, 12% burned for energy); a sorting plant; Republic's $164 and $135 a ton; China's 2018 ban and the 69% fall
  in the recyclable paper index from March 2017 to December 2019;
- waste the law creates: Clean Harbors' ten hazardous waste incinerators and seven landfills, its revenue from $1.1bn
  (2009) to $6.0bn (2025); Waste Management's $2.5bn medical waste arm;
- why the steady money is bought: net margins year by year since 2010, water and waste against oil, steel, chemicals,
  chips, airlines and copper; prices that follow costs, assets nobody can copy, owners who want them; £103bn of regulated
  water assets in England and Wales;
- around the world: safely managed drinking water (74% of the world in 2024, from 61% in 2000) and sanitation (58.5%,
  from 31%), by country;
- the landscape, November 2026: the listed water and waste companies by size and margin, and what to watch;
- *Called it?*: the EPA's 1989 forecast that a third of America's landfills would be full by 1991 (the small ones closed;
  the space did not run out) and this series' call that the US water and sewerage price index will rise more than 4% in
  2027 (70%).

## Build it

```bash
python -m videos.industry.industry14.compute               # every number, printed
EXPLAINER_TTS=silent python tools/build.py industry14 -q l  # the whole part, silent preview
python tools/build.py industry14                           # 1080p30 with narration
python -m videos.industry.labs 14                          # the lab
python -m pytest tests/industry                            # the Register and the Works (test_water_waste.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p14.py`) or comes from the Filing Room: the BLS's
CPI annual averages (`bls_water.csv`), FRED's waste and recyclables prices (`fred_waste.csv`), the EPA's municipal waste
series (`epa_msw.csv`), the World Bank's water and sanitation shares (`wb_water.csv`) and the companies' 10-Ks
(`sec_annual.csv`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | A question of steadiness | The Great Stink, 1858; eighteen days; bills that never fell; the title |
| 1 | Run it: the last landfill in the valley | Three plans; a fifteen-year permit and a five-year one; a ton of airspace |
| 2 | Water as a system | From river to river; America's needs; capital spending against depreciation |
| 3 | The regulated water company | The asset base and the bill; investing; gearing |
| 4 | England's experiment | Owners since 1989; PR24 and the CMA; Thames Water |
| 5 | Public and private elsewhere | A Kentucky rate case; American Water; Sabesp |
| 6 | The route | One truck or two; cost per stop; the price of collection; Waste Management's revenue |
| 7 | The hole in the ground | The 1991 rule; fewer, bigger landfills; airspace; owning the chain |
| — | Intermission | Seventy-two years of American bills after inflation |
| 8 | Recycling and burning | Where the rubbish went; the sorting plant; China's ban |
| 9 | Waste the law creates | Hazardous waste permits; Clean Harbors; medical waste |
| 10 | Why the steady money is bought | Margins year by year; three reasons; the catch |
| 11 | Around the world | Safely managed water and sanitation by country |
| 12 | The landscape, November 2026 | The listed companies; what to watch |
| 13 | Called it? | The EPA's 1989 forecast; this series' call |
| — | The steady business | Bazalgette Tunnel Limited; the answers; Part 15, semiconductors |

## What is computed, and from what

`compute.py` reads the Filing Room and the Register. The years each price index fell compare BLS annual averages
(US city average, not seasonally adjusted) from 1953 (1984 for rubbish collection). Run it, the route and the water
company are the Works' (`explainer/industry/works/route.py`, `utility.py`), with illustrative parameters labelled on
screen; the landfill is valued at 7% a year. The intermission divides each CPI by the all-items CPI. Landfill size per
site divides the EPA's tons landfilled in 1988 and 2009 by its landfill counts. Republic's years of airspace divide its
permitted plus probable airspace by the airspace it consumed in 2025. Margins are net income over revenue from the
companies' 10-Ks, 2010-2025 or as available. The recyclable paper fall compares the index's peak from January 2016 to
June 2018 with its low from January 2018 to December 2020.

## Problems and solutions

**1.** *A refuse truck costs $1,000 a day and works 8 hours of stops. Each stop takes 30 seconds, and between stops it
drives at 12 miles an hour along a street with 100 homes a mile. What does a stop cost with every home on the street, and
with every second home? At $1.30 a stop, what does each hauler make a day?*

*Solution.* With every home, the gap between stops is 1/100 mile, 3 seconds at 12 mph, so a stop takes 33 seconds: 28,800
/ 33 = 873 stops, $1.15 each, and $0.15 × 873 = $134 a day. With every second home the gap is 6 seconds: 800 stops,
$1.25 each, and $0.05 × 800 = $40 a day for each of the two haulers. Splitting the street cuts the haulers' total profit
from $134 to $80: the second truck adds cost without adding a single customer.

**2.** *A landfill has 20 million tons of room and takes 1 million tons a year at $60 a ton; it costs $25 a ton to run.
A rival will open in 10 years, after which the fee falls to $40 and the volume halves. What is the landfill worth at 7%?
What is a ton of its airspace worth?*

*Solution.* For ten years it earns $35 × 1m = $35m a year: 35 × 7.024 = $246m. Then 10 million tons remain, at 0.5
million a year for 20 years, earning $15 × 0.5m = $7.5m a year: 7.5 × 10.594 = $79.5m in year-ten money, or 79.5 /
1.07^10 = $40m today. Total about $286m, or $14 a ton. If the rival never came, the twenty years at $35m would be worth
35 × 10.594 = $371m: the rival's permit costs the owner about $85m.

**3.** *A water company's asset base is £5bn. The regulator allows 3.5% a year after inflation, runs the base off at 5%
a year, and allows £300m of running costs. It has 2.5 million households. What is the bill? If it invests £400m a year,
how does next year's bill change?*

*Solution.* Return 175 + run-off 250 + costs 300 = £725m, or £290 a household. Investing £400m while £250m runs off
grows the base by £150m, to £5.15bn: next year's return rises by £5.25m and its run-off by £7.5m, £12.75m in all, or
about £5.10 on each bill, before inflation. The bill rises because the base does.

**4.** *An asset base earns 4% a year. Its owner has financed 60% of it with debt at 3%. What do the shareholders earn?
What if the debt is refinanced at 6%? And at 80% gearing with debt at 6%?*

*Solution.* r_E = r_A + (r_A − r_D) × D/E. At 60% gearing D/E = 1.5: 4% + 1% × 1.5 = 5.5%. At 6% debt: 4% − 2% × 1.5
= 1%. At 80% gearing D/E = 4: 4% − 2% × 4 = −4%: the shareholders lose money every year, and the company can only pay
its lenders by borrowing more or by asking the owners for new equity.

**5.** *A sorting plant takes 100,000 tons a year of recycling and costs $90 a ton to run. It sells 85% of what it takes
as bales and pays $50 a ton to landfill the other 15%. What does it make on each ton at a bale price of $164, and at
$135? At what bale price does it break even? What if bales fall 55%, as recyclable paper did from 2017 to 2019?*

*Solution.* At $164: 0.85 × 164 − 90 − 0.15 × 50 = $41.90 a ton, $4.2m a year. At $135: $17.25 a ton, $1.7m. Break-even
is 0.85p = 97.5, p = $114.70. At $74 (55% below $164): 62.90 − 97.50 = −$34.60 a ton, a $3.5m loss a year, which the
plant's owner or the towns that send it recycling must cover.

## Glossary

- **Regulatory capital value (RCV) / rate base:** the value of a regulated company's assets on which it may earn a return.
- **Run-off:** the part of the asset base a regulator lets the company recover from customers each year.
- **Allowed return (WACC):** the return a regulator allows on the asset base, a blend of the cost of debt and of equity.
- **Gearing:** the share of the asset base financed with debt.
- **Price review:** the regulator's setting of a company's allowed spending, return and bills, in England every five years.
- **Airspace:** the volume a landfill may still fill under its permits.
- **Tipping fee:** the price a landfill charges per ton to accept waste.
- **Internalization:** the share of the waste a hauler collects that goes to its own landfills.
- **Leachate:** the liquid that drains through buried waste.
- **Materials recovery facility (MRF):** a plant that sorts mixed recycling into bales to sell.

## Lab and interactive

- `python -m videos.industry.labs 14`: the Great Stink; the price indexes; Run it; America's water needs; the Works'
  water company and gearing; England's PR24; the Kentucky rate case and Sabesp; the route; landfills and airspace;
  recycling and China's ban; Clean Harbors; margins; safe water; the 1989 forecast; this series' call.
- The interactive (course site): the last landfill in the valley. Choose a plan, set the years until a rival's permit
  and the valley's ceiling, and see what the landfill is worth and how fast it fills.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p14.py`) or the Filing Room
(`explainer/industry/data/SOURCES.md`). The main ones:

- Hansard: HC Deb 15 July 1858 (Metropolis Local Management Act Amendment Bill); HL Deb 2 August 1858 (the Lords
  Commissioners' speech); HC Deb 16 June 2026 (Thames Water).
- US Environmental Protection Agency: The Solid Waste Dilemma: An Agenda for Action (1989); Municipal Solid Waste in the
  United States: 2009 Facts and Figures; Advancing Sustainable Materials Management: Facts and Figures, 1960-2018; Historic
  Tipping Fees and Commodity Values (2015); 7th Drinking Water Infrastructure Needs Survey and Assessment; Clean
  Watersheds Needs Survey 2022; Information about Public Water Systems.
- 40 CFR Part 258, criteria for municipal solid waste landfills (56 FR 51016, 9 October 1991).
- SEC EDGAR: Forms 10-K of Waste Management (2018, 2025), Republic Services, Clean Harbors and American Water (2025), and
  of Waste Connections, Casella, Essential Utilities, American States Water, California Water Service and H2O America;
  Sabesp's Form 20-F (2025); Veolia's ESEF annual report (2024).
- Independent Water Commission, Final Report (21 July 2025); Competition and Markets Authority, Water PR24 price
  redeterminations: final determinations summary (March 2026); GOV.UK on the Thames Tideway Tunnel.
- Bureau of Labor Statistics: consumer price indexes (CPI-U, US city average) and producer price indexes for solid waste
  collection and recyclable paper (via FRED).
- WHO/UNICEF Joint Monitoring Programme, via the World Bank's World Development Indicators.
