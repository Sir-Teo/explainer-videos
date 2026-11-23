# Industry, Built: Part 4, The Cost Curve

Part 4 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth of Act I, *Reading an Industry*. It asks: what does one more cost, and
why does that decide almost everything? It answers with a model factory, then real costs: Delta Air Lines' expense
lines and seat miles, the US Energy Information Administration's costs for new power plants, fifty years of solar
module prices, the whole US power fleet in 2025, Micron's margins through a memory price war and Microsoft's
software segments. The answer: decisions turn on the cost of one more unit, not the average; a business's cost per
unit falls with how full it runs, its size, its second products, its density and its experience; and in a market the
last unit needed sets the price, which is what pays for everything below it, and what turns into a price war when
fixed costs are huge and products alike.

It opens in Buffalo in 1936, where Theodore Wright of the Curtiss-Wright Corporation published his finding that the
labour in an aeroplane fell by about a fifth each time the number built doubled. From there it covers:

- take the order? A factory with $10m of fixed costs sells 200,000 units at $80 (average cost $90) and is offered
  100,000 more at $60: taking it turns a $2m loss into break-even;
- four words for cost: Delta's $57.5bn of 2025 operating costs sorted by how soon cancelling flying avoids them
  (about 31% within days, 95% within a year); fixed, variable, avoidable and sunk as a two-by-two; finishing or
  stopping a plant that is 80% built; the Concorde fallacy (Dawkins and Carlisle, 1976);
- how full? A new reactor's megawatt-hour costs $109 at 95% utilization and $955 at 10%; five kinds of new plant on
  one chart, and where each ran in 2025 (combined-cycle gas $46, wind $58, solar $68, nuclear $113, a peaker $124);
- bigger is cheaper: a tank's steel against its volume; the six-tenths rule; three pairs of real machines from EIA
  (gas turbines 49% cheaper per kilowatt at twice the size, combined-cycle 5%, a small modular reactor 19% dearer than
  a large plant); minimum efficient scale against the size of the market;
- scope and density: Delta's $900m of belly cargo and $8.2bn from American Express against its $5.8bn operating
  profit; a delivery street where a parcel costs $18 to deliver at one house in twenty and $3.34 at one in two;
- learning: solar modules from $132 a watt in 1975 to 12 cents in 2025; on a log scale against capacity built, about
  30% cheaper with each of almost eleven doublings since 2000 (R² 0.94), and what the fit cannot say;
- an intermission: America's plants squeezed from what they could make to what they made in 2025;
- the empty seat: Delta's seat map breaks even at 76% full against 84% flown; one point of load factor is worth about
  $0.75bn a year;
- operating leverage: a hotel and a temp agency with the same sales and profit through a recession and a boom; Delta's
  revenue down 64% in 2020 and its costs down 27%, a $6.6bn profit becoming a $12.5bn loss;
- the Stack: every US power plant lined up by the cost of one more megawatt-hour, then an illustrative summer day on
  it: the marginal plant sets the price for everyone, and the gap pays for the plants below it;
- price wars: the logic of the undercut; Micron's gross margin from 59% (2018) to -9% (2023) to 81% (2026); the four
  ways out (collusion, with the DRAM fines of 2004-2006; mergers, with Micron's purchase of Elpida; discipline;
  differentiation);
- zero marginal cost: software's average cost falls without a floor; Microsoft's Office keeps 60 cents of a dollar
  and its AI-heavy cloud 41;
- *Called it?*: the IEA's 2010 solar roadmap (200 GW by 2020, 2,000 GW by 2040) against 721 GW in 2020 and 2,397 GW
  in 2025; and this series' call that US utility-scale solar will out-generate coal in at least one month of 2027
  (55%).

## Build it

```bash
python -m videos.industry.industry4.compute               # every number, printed (instant)
EXPLAINER_TTS=silent python tools/build.py industry4 -q l  # the whole part, silent preview
python tools/build.py industry4                           # 1080p30 with narration
python -m videos.industry.labs 4                          # the lab
python -m pytest tests/industry                           # the cost functions, the Stack and the Register
```

Every company and plant figure is a row of the Register (`explainer/industry/data/rows_p04.py`, with Part 1's Micron
rows and Part 3's Delta and Microsoft rows) with its source, URL and dates. The US fleet is the Filing Room's
`eia_power.csv` (EIA's Electric Power Annual 2025); solar prices and capacity are *Economics, Built*'s Data Room
(`solar_pv`). The cost functions, the merit order and Wright's law are `explainer/industry/works/stack.py`; the
pictures are `explainer/industry/draw.py`.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Wright's aeroplanes | Buffalo, 1936; the 80% curve, doubling by doubling; the title |
| 1 | Take the order? | A half-idle factory, its average-cost curve and an offer below it |
| 2 | Four words for cost | Delta's costs by horizon; fixed, variable, avoidable, sunk; the Concorde fallacy |
| 3 | How full? | A reactor's megawatt-hour against utilization; five kinds of plant and where they ran |
| 4 | Bigger is cheaper | The tank; the six-tenths rule; three pairs of machines; minimum efficient scale |
| 5 | Scope and density | Delta's cargo and miles; a delivery street |
| 6 | Learning | Solar's price tag, 1975-2025; linear, log and Wright's law |
| — | Intermission | America's plants: capacity against output; the story so far |
| 7 | The empty seat | Delta's seat map and break-even load factor |
| 8 | Operating leverage | A hotel against a temp agency; Delta, 2019 and 2020 |
| 9 | The Stack | Every US power plant by the cost of one more; a summer day on it |
| 10 | Price wars | The undercut; Micron's margins; four ways out |
| 11 | Zero marginal cost | Copies of software; Microsoft's two segments |
| 12 | Called it? | The IEA's 2010 roadmap; this series' call on solar and coal |
| — | What one more costs, and what comes next | The answers; Part 5, the moat |

## What is computed, and from what

`compute.py` reads every figure from the Register and the Filing Room. A new plant's yearly fixed cost per kilowatt is
its overnight capital cost from EIA's assumptions for the Annual Energy Outlook 2026 (Table 3, 2025 dollars) times a
capital recovery factor at an assumed 7% over 30 years (0.0806), plus its fixed operating cost; its variable cost per
megawatt-hour is its variable operating cost plus fuel: gas at $3.85 per million Btu (2025, electric power sector)
times its heat rate, and for nuclear EIA's 2025 fuel cost of 6.64 mills per kilowatt-hour. The cost per megawatt-hour
at utilization *u* is the fixed cost times 1,000 over 8,760*u* hours, plus the variable cost. There are no subsidies,
grid connection or financing details: these are illustrations of the arithmetic, not a levelized-cost study.

The Stack's blocks are 2025 net summer capacities and capacity factors from the Electric Power Annual (tables 4.3 and
4.8), with fuel costs from table 7.4 and representative heat rates; wind, solar and hydro are taken to cost nothing (hydro
$1) to run one more hour. The summer day is illustrative: demand is a smooth curve from about 470 GW before dawn to
about 745 GW in the early evening, solar follows the sun, and the other kinds of plant are available at fixed shares
of their capacity. Solar's learning rate is a least-squares fit of log price on log cumulative capacity, 2000-2025.
Delta's revenue per filled seat mile is its total revenue per available seat mile over its load factor, so it counts
cargo and loyalty revenue as if they came from passengers; the break-even load factor is cost per available seat mile
over that. The model factory, the delivery street, the hotel and the agency, and the price-war staircase are models,
labelled as such on screen.

## Problems and solutions

**1.** *A factory has fixed costs of $10m a year and makes each unit for $40. It sells 200,000 units at $80 and is
offered 100,000 more at $60. Should it take the order? What if, once it does, all its regular customers demand $60?*

*Solution.* The order adds 100,000 × (60 - 40) = $2m: the loss of 200,000 × 40 - 10m = -$2m becomes break-even. If
every customer then pays $60, profit is 300,000 × 20 - 10m = -$4m, worse than refusing. The rule is to count what
the decision changes, including what it does to the prices of the units already sold.

**2.** *A plant costs $1,000 per kilowatt to build and $20 per kilowatt a year to keep open; its fuel costs $30 a
megawatt-hour. At 7% over 30 years the capital recovery factor is 0.0806. What does a megawatt-hour cost at 50% and
at 90% utilization?*

*Solution.* The yearly fixed cost is 1,000 × 0.0806 + 20 = $100.6 per kilowatt, or $100,600 per megawatt. At 50% it
runs 4,380 hours: 100,600 / 4,380 + 30 = $52.97. At 90%, 7,884 hours: 100,600 / 7,884 + 30 = $42.76. Running more
spreads the same fixed cost over more hours; the fuel cost per megawatt-hour does not change.

**3.** *A chemical plant of 100,000 tonnes a year costs $50m. Using the six-tenths rule, what would a plant of 400,000
tonnes cost, and how much cheaper is it per tonne of capacity?*

*Solution.* 50 × 4^0.6 = 50 × 2.30 = $114.9m. Per tonne of capacity: $500 against $287, 43% less. Each doubling
multiplies the cost by 2^0.6 = 1.52, so the cost per unit of capacity falls by about a quarter.

**4.** *On an 80% learning curve, the first aircraft takes 100,000 hours. How long does the 64th take? Solar module
prices fall about 30% with each doubling of capacity built; by how much do they fall over three doublings?*

*Solution.* 64 = 2^6, so 100,000 × 0.8^6 = 26,214 hours. Three doublings: 0.7^3 = 0.343, a fall of about two thirds.
The rule works per doubling, so each fall of a given size takes twice as much building as the last.

**5.** *An airline's cost per available seat mile is 15 cents, and it earns 20 cents per filled seat mile. What is its
break-even load factor? At 82% full, what is its margin per available seat mile?*

*Solution.* 15 / 20 = 75%. At 82%: 0.82 × 20 - 15 = 1.4 cents per available seat mile, on revenue of 16.4 cents: an
operating margin of 8.5%. Seven points of load factor separate this airline from break-even.

**6.** *A firm has sales of $100m, fixed costs of $60m and variable costs of 30% of sales. What is its profit and its
degree of operating leverage? What happens to profit if sales fall 10%?*

*Solution.* Profit is 100 - 30 - 60 = $10m. Contribution is $70m, so the degree of operating leverage is 70 / 10 = 7.
A 10% fall in sales cuts contribution by $7m: profit falls to $3m, 70% lower.

**7.** *A power market has four plants: A, 100 MW at $5 a megawatt-hour; B, 200 MW at $25; C, 100 MW at $40; D, 50 MW
at $90. What is the price when demand is 250 MW, 380 MW and 420 MW? At 250 MW, what does A earn above its own cost in
an hour?*

*Solution.* Filling from the cheapest: at 250 MW, B is the last needed: $25. At 380 MW, C: $40. At 420 MW, D: $90.
At 250 MW, A earns (25 - 5) × 100 = $2,000 an hour above its running cost, which is what pays for building it.

## Glossary

- **Marginal cost:** the cost of making one more unit.
- **Average cost:** total cost divided by the number of units.
- **Fixed cost:** a cost that does not change with how much is made, over the horizon of the decision.
- **Variable cost:** a cost that rises with how much is made.
- **Sunk cost:** money spent that cannot be recovered whatever is decided next.
- **Utilization (capacity factor, load factor):** output as a share of what the plant or fleet could produce.
- **Economies of scale:** a lower cost per unit in a larger plant.
- **Minimum efficient scale:** the size beyond which a bigger plant is not much cheaper per unit.
- **Economies of scope:** making two products together for less than making them apart.
- **Economies of density:** a lower cost per customer when customers are closer together.
- **Learning curve (Wright's law, experience curve):** cost falling by a constant share each time cumulative output
  doubles.
- **Operating leverage:** the percentage change in operating profit for a 1% change in sales.
- **Merit order (the Stack):** plants ranked by the cost of one more unit; the last one needed sets the market price.
- **Rent (inframarginal rent):** the gap between the market price and a lower-cost producer's own cost.

## Lab and interactive

- `python -m videos.industry.labs 4`: the order below average cost; new plants' cost per megawatt-hour at 25%, 95%
  and as run; Wright's law fitted to solar; Delta's break-even load factor and the value of a point; operating
  leverage for the hotel, the agency and Delta in 2020; the Stack cleared hour by hour.
- The interactive (course site): the price war. You and a rival each run a plant for 100 units a period; buyers go to
  the cheaper one. Set your opening price, your answer to the rival's cuts, the demand and the fixed cost, and play
  ten rounds.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p04.py`) with its URL. The main ones:

- T. P. Wright, "Factors Affecting the Cost of Airplanes", *Journal of the Aeronautical Sciences* 3(4), 1936.
- U.S. Energy Information Administration: *Assumptions to the Annual Energy Outlook 2026*, Electricity Market Module,
  Table 3 (April 2026); *Electric Power Annual 2025* (tables 2.4, 3.1.A, 4.3, 4.8.A and B, 7.4, 8.2 and 8.4);
  *Short-Term Energy Outlook*, November 2026, Table 7d.
- Solar module prices (IRENA and others, compiled by Our World in Data) and installed capacity (IRENA, via Our World in
  Data); the IEA's *Solar PV Global Supply Chains* (2022).
- Forms 10-K: Delta Air Lines (2019, 2020 and 2025), Micron Technology (fiscal 2016-2026), Microsoft (fiscal 2026);
  Micron's Form 8-K of 31 July 2013.
- US Department of Justice, Antitrust Division, press releases on the DRAM investigation (2005-2006).
- R. Dawkins and T. R. Carlisle, "Parental investment, mate desertion and a fallacy", *Nature* 262 (1976).
- The IEA, *Technology Roadmap: Solar Photovoltaic Energy* (2010).
- *Called it?*: the series' own call is in `explainer/industry/calls.py`.
