# Economics, Built: Part 50, The Policy Memo

Part 50 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the capstone of Act IX, *The Fields*. It asks what you write when a minister asks
whether to pay a child allowance. Its answer: the decision first, every number with its range, the evidence with its
limits, and the judgment named as the minister's. Here, on the Island: about a fifth fewer poor children for about
$1,500 a child a year; few parents leaving work unless they respond far more than the evidence so far suggests; a
second design that keeps the old credit's work requirement, gives up a little of the poverty reduction and saves a
quarter of the cost; and a case that rests on what the children repay later and on the weight given to their incomes.

It opens on 15 July 2021, when most American families with children received a monthly payment for the first time
($300 a child under six, $250 a child from six to seventeen), and on what followed: child poverty on the Census
Bureau's Supplemental Poverty Measure fell from 9.7% in 2020 to 5.2% in 2021, a record low, and rose to 12.4% in 2022
after the payments stopped; the official measure, which ignores tax credits, barely moved. Then the Island's
finance minister asks for four pages in two weeks. From there it covers:

- the question made answerable: the proposal against the credit it replaces (2,000 a child, refundable only up to
  1,400 and phased in at 15% of earnings, against 3,600 and 3,000 a child paid whatever the family earns, monthly);
  the Island's 40,000 families with children (35% single parents, 74,118 children); the channels and their horizons;
  what counts as an answer;
- the family's budget: for a single parent of two, the allowance adds $6,600 at no earnings, $2,600 in the middle and
  nothing above $127,000; the reward for working at $20,000 falls from $28,504 to $25,759, about a tenth; the income
  effect and the end of the phase-in;
- the dials the memo runs on: the participation elasticity (0.25, run from 0 to 0.5), the elasticity of taxable
  income (which prices a top surtax: $1.11, $1.33 or $1.67 of cost to top earners per dollar raised at 0.1, 0.25 and
  0.4), and the marginal value of public funds;
- Play it: your advice and your forecast of the fall in child poverty, kept;
- the margins the textbook misses: take-up (with 85% claiming, child poverty 12.3% instead of 11.6%, and the cost
  per child $1,248 instead of $1,473: the savings come from missing the families the policy is for), monthly timing,
  labels and conditions;
- the budget and the wider economy: $109 million a year on the Island, of which families' responses add 0.2%; scaled
  to some 70 million American children, about $103 billion, 0.35% of 2024 GDP; three ways to pay; prices, wages,
  births (Quebec's allowance for newborns) and the long run;
- the evidence: America's 2021 payments (Ananat et al.: no detectable effect on parents' work), Canada's Child
  Benefit (Baker, Messacar and Stabile: poverty 11% and 17% lower, no less work), Mothers' Pensions (Aizer et al.: a
  year more life, a third of a year more school), Canadian benefits and children (Milligan and Stabile), the
  simulation of Corinth et al. (1.5 million parents, 2.6%, leaving work; poverty falling by at most 22%), and a
  matrix of how each transfers to the Island;
- the policy run on the Island, a microsimulation: child poverty 14.3% under the old credit, 10.1% with no response,
  11.6% with responses at 0.25 (19% fewer poor children; 633 parents, 1.7%, stop working, 74% of them single
  parents); across the dial from 10.1% to 13.5%; deep poverty rises above the old credit's 7.8% once the elasticity
  exceeds about 0.22;
- the value of public funds: 1.00 with nothing repaid later, 1.33 if a quarter is repaid in children's later taxes,
  1.99 if half; with a top surtax, 0.60 to 0.75 when nothing is repaid; the judgment that remains;
- who gains: the poorest tenth +$5,467 a year, the middle $1,400-1,800, the richest tenth +$452; who loses; the
  *is / ought* card;
- the uncertainty: tornado charts for poverty (the elasticity dominates; every bar stays below the old credit) and
  cost (take-up dominates); what would change the advice;
- the memo, page by page; the two-minute version; the viewer's advice revisited with the second design (12.2% of
  children poor, deep poverty 7.0%, $1,116 a child);
- in practice: budget offices, ten-year windows, six ways a memo goes wrong; *Called it?* on Corinth et al.'s forecast
  (too early to say); and a frontier led by Baby's First Years (no significant effects at age four).

## Build it

```bash
python -m videos.economics.econ50.compute              # every number (under a minute), into .cache/econ50/
python tools/qa_scene.py econ50 Island                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ50 -q l   # the whole part, silent preview
python tools/build.py econ50                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 50                     # the lab
```

The data are in `explainer/economics/data/`: the Census Bureau's official poverty rates of children and of everyone
(Small Area Income and Poverty Estimates) and BEA's GDP and consumption, via FRED; the tables of Part 50 (the credits'
rules, the 2021 payments and the poverty measures, the studies, the frontier); all registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Six monthly payments | July 2021; the poverty measures; the minister's request; the question; objectives |
| 1 | The question made answerable | The proposal; the Island's families; channels and horizons; what counts as an answer |
| 2 | The family's budget, before and after | The credits; the difference; the budget line; two effects on work |
| 3 | Who responds, and how much | Participation, the elasticity of taxable income, the MVPF |
| 4 | Play it: your advice, before the analysis | Your advice and your forecast, kept |
| 5 | The margins the textbook misses | Take-up; monthly timing; labels and conditions |
| 6 | The budget and the wider economy | The cost; who pays; prices, wages, births, the long run |
| 7 | The evidence | 2021; Canada; Mothers' Pensions; Canadian children; the simulation; does it transfer? |
| — | Intermission | American children below the official line, 1989-2024, as a line and a tune; the story so far |
| 8 | The policy run on the Island | The microsimulation; the results; who stops; the fan; deep poverty |
| 9 | The cost and the value of public funds | The MVPF; the table of repayment and financing; where the numbers stop |
| 10 | Who gains and who loses | Deciles; losers; the *is / ought* card |
| 11 | The uncertainty, stated | Tornado charts for poverty and cost; switching points |
| 12 | The memo | Four pages; the two-minute version; your advice revisited |
| 13 | In practice: how memos are used | Who writes and reads them; six ways they go wrong; *Called it?* (too early to say) |
| 14 | Frontier: what remains unidentified | Baby's First Years; the open questions |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 51, *Computing Economies* |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's policy memo (`explainer.economics.agora.memo`) with the
Island's Part 50 truths, or from the data named above; the narration states the cached numbers.

- **The credits.** The 2021 federal income tax (standard deduction and brackets) for single heads of household and
  couples; the 2021 EITC (34%, 40% or 45% of earnings to 10,640 or 14,950, maxima 3,618, 5,980 and 6,728, phased out
  above 19,520, or 25,470 for a couple, at 15.98% or 21.06%); the credit before 2021 (2,000 a child, refundable at
  15% of earnings above 2,500 up to 1,400 a child, the rest against income tax); the allowance (3,600 and 3,000,
  fully refundable, the extra phased out at 5% above 75,000 or 150,000); the second design (the old credit plus the
  extra, unconditional).
- **The families.** 40,000, 65% couples; one to four children (42%, 37%, 15%, 6%), each under six with probability
  0.35; the main earner's potential earnings log-normal with median 28,000 (single) or 52,000 (couple) and log-sd
  0.75; a second earner in 60% of couples.
- **Work.** The main earner works with probability 1 / (1 + exp(-(a_i + b log g_i))), where g_i is what working adds
  to the family's income per dollar of potential earnings; a_i is set so that 85% of single parents and 95% of
  couples' main earners work under the old credit, and b so that the average participation elasticity is the dial's
  value; the same random draws under every policy.
- **Poverty.** The Island's line, 24,000 for two adults and two children, scaled by the square root of family size;
  deep poverty below half of it; rates are shares of children.
- **The value.** What families would pay is the payment at unchanged behaviour (the envelope theorem); the net cost
  counts credits paid and taxes lost; children's later repayment is a planted range (none, a quarter, half); the
  cost of a top surtax is (1 - tau)/(1 - tau - tau a e) with tau = 0.4 and a = 1.5.

## Problems and solutions

**1.** *The credits: a single parent of two, one under six, with no other income. Find the old credit and the
allowance at earnings of 0, 10,000 and 30,000 (the old credit: 2,000 a child, refundable up to 1,400 a child at 15%
of earnings above 2,500; tax 10% above 18,800), and the gain at each.*

*Solution.* At 0 the old credit is 0 (nothing earned, nothing refundable) and the allowance 3,600 + 3,000 = 6,600: a
gain of 6,600. At 10,000 the refundable part is min(2,800, 0.15 x 7,500) = 1,125, and there is no tax to offset, so
the old credit is 1,125; the gain is 5,475. At 30,000 the tax is 0.10 x 11,200 = 1,120 and the refundable part
min(2,800, 0.15 x 27,500) = 2,800; the credit is the smaller of 4,000 and 1,120 + 2,800 = 3,920; the gain is 2,680.

**2.** *The reward for work: at 20,000 the parent pays 120 in tax and receives 5,879 of EITC. Find what working adds
under each system, the percentage fall, and the fall in the share working if the participation elasticity is 0.44
and 85% worked.*

*Solution.* The old credit at 20,000 is 120 + min(2,800, 0.15 x 17,500) = 2,745, so working adds 20,000 - 120 +
5,879 + 2,745 = 28,504 under the old system. Under the allowance the 6,600 comes whether or not the parent works, so
working adds 20,000 - 120 + 5,879 = 25,759: 9.6% less. The share working changes by about 0.44 x ln(25,759/28,504) =
0.44 x (-0.101) = -4.5%, from 85% to about 81.3%, a fall of about 3.7 points. (On the Island single parents' work
falls from 85.7% to 82.4%.)

**3.** *Deep poverty: the line for three is 24,000 sqrt(3/4). Show that the parent working at 15,000 is above it under
the old credit, and that stopping work under the allowance leaves the family below half of it.*

*Solution.* The line is 20,785 and half of it 10,392. Working at 15,000: no tax, an EITC of min(0.40 x 15,000, 5,980)
= 5,980 (the phase-out starts at 19,520), and an old credit of 0.15 x 12,500 = 1,875: 22,855, above the line.
Stopping under the allowance leaves 6,600, below half the line. The allowance raises the income of a family whose
parent does not work, from 0 to 6,600, but a parent who would otherwise have worked and now stops loses 16,255.

**4.** *The MVPF: families would pay 108.9 million; the net cost is 109.2 million. Find the MVPF if children later
repay nothing, a quarter or half of 108.9 million, and divide each by a cost of funds of 1.33.*

*Solution.* 108.9/109.2 = 1.00; 108.9/(109.2 - 27.2) = 1.33; 108.9/(109.2 - 54.5) = 1.99. Divided by 1.33: 0.75,
1.00 and 1.49. With a surtax and nothing repaid, families receive 75 cents of value for each dollar top earners give
up; whether that is worth it is the weight on poor families' incomes.

**5.** *The cost of funds: show that a dollar of net revenue from a top rate tau costs top earners
(1 - tau)/(1 - tau - tau a e). With tau = 0.4 and a = 1.5, find it for e = 0.25, and the e at which it is 2.*

*Solution.* Income above the threshold is a Pareto tail whose size scales like (1 - tau)^(a e) (Part 41), so
revenue is proportional to tau (1 - tau)^(a e). Raising tau by d tau costs top earners the base, (1 - tau)^(a e) d tau
(the envelope theorem), and raises revenue by (1 - tau)^(a e - 1) (1 - tau - a e tau) d tau. The ratio is
(1 - tau)/(1 - tau - tau a e). At tau = 0.4, a e = 0.375: 0.6/0.45 = 1.33. It equals 2 when 0.6 = 2(0.6 - 0.6 e),
so at e = 0.5.

**6.** *The second design: the old credit plus 1,600 for the young child and 1,000 for the older, unconditional. For
the parent of problem 2, find the payment at 0 and at 20,000, and what working adds.*

*Solution.* At 0 the family receives the extra only, 2,600; at 20,000, the old credit 2,745 plus 2,600 = 5,345.
Working adds 20,000 - 120 + 5,879 + 5,345 - 2,600 = 28,504, exactly as under the old credit: the reward for work is
untouched, so no parent stops for that reason. The price is that a family with no earnings gets 2,600 instead of
6,600, which is why the second design leaves more children poor (12.2% against 11.6% at the central elasticity) but
fewer in deep poverty (7.0% against 8.0%).

**7.** *The tornado: poverty ranges 10.1-13.5 for the elasticity, 11.6-12.5 for the income effect, 11.6-12.3 for
take-up. Which study would you fund first, and what would it have to find to change the advice?*

*Solution.* The elasticity's range (3.4 points) is larger than the other two together (0.9 and 0.7), so a study of
how parents' employment responds to a permanent allowance, for instance a staggered start across regions, has the
highest value of information. It would change the advice if it found a participation elasticity well above 0.22,
where deep poverty starts to rise and the second design becomes the better choice; a finding near zero, like the
2021 and Canadian results, would strengthen the case for the full allowance.

**8.** *The envelope theorem: a parent chooses work h in {0, 1} to maximize u(y(h) + T) - theta h. Show that the
value of a small allowance dT is u' dT whether or not the parent switches, so that what families would pay equals the
payment at unchanged behaviour.*

*Solution.* Let V(T) = max over h of u(y(h) + T) - theta h. Where the choice does not change, dV = u'(y(h*) + T) dT.
Where a small dT makes the parent switch, the parent was indifferent between the two choices before, so the switch
itself gains nothing to first order: V is the upper envelope of two smooth functions, continuous at the switch, with
derivative u' at the chosen option. In money, each family values dT at dT, so the sum of what families would pay is
the mechanical cost at unchanged behaviour; changed behaviour shows up only in the government's cost (the fiscal
externality).

## Lab and interactive

- `python -m videos.economics.labs 50`: the credits for one family and the reward for work; the Island's
  microsimulation at the central dials; the fan across the elasticity and the deep-poverty crossing; take-up; the
  value of public funds by repayment and financing; the second design.
- The interactive (course site): memo. The reader sets the participation elasticity, take-up, the share of the cost
  children repay later and how the money is raised, and chooses the design, and reads child poverty, deep poverty,
  how many parents stop working, the cost per child and the value per dollar.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[50]`; the three dials it uses
(`labour_supply`, `eti`, `mvpf`) are in `explainer/economics/dials.py`; Corinth et al.'s forecast is a *Called it?*
entry (`explainer/economics/calls.py`); the tables are `PART50` in `explainer/economics/data/tables.py`. The data were
retrieved on 2026-11-21 and are registered with their licences in the Data Room. The statements were checked on
2026-11-21: the American Rescue Plan's credit (amounts, monthly payments July-December 2021, expiry); the Census
Bureau's SPM and official child poverty rates for 2020-2022 (as published at the time; BLS later re-released the SPM
thresholds for 2019-24); Ananat et al. (very small, inconsistently signed, insignificant employment effects); Baker,
Messacar and Stabile (11% and 17%, no labour supply reduction); Milligan and Stabile (test scores, maternal health and
mental health); Aizer et al. (16,000 boys; a year of life, a third of a year of schooling, higher income); Corinth et
al. (1.5 million, 2.6%, at most 22%); the 2021 EITC parameters and the pre-2021 credit (statute and CRS tables);
Milligan (2005) (up to 25% for families eligible for the full amount of up to C$8,000); the Census Household Pulse
(food the most common use); Baby's First Years (1,000 mothers, $333 or $20 a month, no significant effects at age
four, NBER WP 33844); the IRS's repayment protection for 2021 (up to $2,000 for each child no longer qualifying, in
full at modified incomes up to $40,000, $50,000 or $60,000). Not verified, so not stated: the Joint Committee on
Taxation's cost estimate for the 2021 expansion; the number of American children receiving the payments.
