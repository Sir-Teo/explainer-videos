# Industry, Built: Part 5, The Moat

Part 5 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth of Act I, *Reading an Industry*. It asks: why do some industries earn
high returns for decades while others never do? It answers with Aswath Damodaran's returns on capital for 90 US
industries, the Census Bureau's 2022 concentration ratios for 897 industries, McGahan and Porter's split of profit
differences, Berkshire Hathaway's letter for 2007, and the accounts of Visa, Costco, Delta, Kodak and the newspaper
industry. The answer: returns differ widely between industries and fade only slowly; a few firms earn high returns
only if something keeps newcomers out and the few do not fight; the walls are made of cost, habit, networks and law;
five forces can drain what they protect; and no wall survives customers who stop wanting what is inside.

It opens with Warren Buffett's letter of February 2008: "A truly great business must have an enduring 'moat' that
protects excellent returns on invested capital." From there it covers:

- three businesses from the letter: See's Candies, bought in 1972 for $25m, earning $82m before tax on $40m of
  capital in 2007 ($2.41 a year for each extra dollar put in); FlightSafety, about 31 cents; airlines, little or
  nothing;
- Run it: an incumbent earning $100m a year against an entrant whose set-up costs $30m; an empty threat, a bigger
  plant, advertising and lock-in, and why only moves paid for in advance deter;
- the facts: return on capital for 90 US industries in 2025, from tobacco's 63% to consumer electronics' loss; 83%
  above their cost of capital; a rank correlation of 0.57 between 2015-2019 and 2022-2025; the top quarter from 30% to
  27%, the bottom from 5% to 10%;
- why high returns fade when money can flow in, and how a moat bends the curve (a model);
- where the excess profit is: $1.47 trillion above the cost of capital in 2025, 39% of it in five industries
  (two kinds of software, computers, chips and health care support);
- industry or company: McGahan and Porter (1997) find the industry explains 19% of the variance in business units'
  profitability and the business itself 32%;
- counting the castles: 33,066 firms run nail salons and the four largest have 0.4% of sales; under 800 run home
  centers and the four largest have 98%; the distribution across 897 industries (median 31%); the HHI and the 2023
  merger guidelines' threshold of 1,800;
- concentration against returns for eight matched industries: tobacco and home centers high on both, airlines (73%)
  and carmakers (58%) concentrated but earning less than 10%;
- walls of cost (warehouse clubs, 96% for the four largest) and of habit (switching costs, brands);
- a moat that held: smokers fell from about 42 in 100 adults (1965) to under 12 (2022), and tobacco had the
  highest return on capital in seven of eleven years and the second highest in the other four, 45% to 96%;
- walls of networks (n users, n(n-1)/2 links; Visa keeping 61 cents of each dollar in fiscal 2026) and of law
  (a patent's 20 years; licences and scarce rights);
- Porter's five forces (1979), applied to airlines and to tobacco;
- buyers and suppliers: in the phone's chain from Part 1, TSMC keeps 62% and Qualcomm's licensing 72%, Foxconn 6%;
- a moat in the accounts: operating margins since fiscal 2009, Visa about 50-66% (apart from a legal charge in 2012), Costco 2.5-3.9% with a standard
  deviation of 0.4 points, Delta from 19% to -73%;
- good for whom? a high return as a reward or as a toll;
- an intermission: eight industries' returns, 2015 to 2025, ranked year by year;
- moats that drained: newspapers' advertising from $49.4bn (2005) to $9.6bn (2020, Pew's estimate), below
  circulation; Kodak's sales from $9.4bn (2008) to $1.5bn (2017) and its chapter 11 in January 2012;
- *Called it?*: Buffett's airline forecast against airlines' 6.5% average return on capital, 2015-2025, against a
  6.0% cost; and this series' call that at least seven of 2025's top ten industries will be in the top twenty in 2028
  (75%).

## Build it

```bash
python -m videos.industry.industry5.compute               # every number, printed (instant)
EXPLAINER_TTS=silent python tools/build.py industry5 -q l  # the whole part, silent preview
python tools/build.py industry5                           # 1080p30 with narration
python -m videos.industry.labs 5                          # the lab
python -m pytest tests/industry                           # the Register and the Works
```

Every figure is a row of the Register (`explainer/industry/data/rows_p05.py`, with Part 1's margins in the phone's
chain) or comes from the Filing Room: Damodaran's tables (`damodaran_roc.csv`), the Census's concentration ratios
(`census_conc_2022.csv`) and the SEC extract (`sec_annual.csv`, now with Visa).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Three businesses | Buffett's moat; See's, FlightSafety and airlines; the title |
| 1 | Run it: the entrant | Four moves against an entrant, and why only commitments deter |
| 2 | The facts first | 90 industries' returns against their cost; persistence, 2015-2019 to 2022-2025 |
| 3 | Why high returns fade | Entry pulls returns down to the cost of capital; a moat bends the curve |
| 4 | Where the excess profit is | Economic profit by industry, 2025 |
| 5 | Industry or company? | McGahan and Porter's decomposition |
| 6 | Counting the castles | Nail salons and home centers; 897 industries; the HHI |
| 7 | Few castles, high walls? | Concentration against returns; airlines and carmakers |
| 8 | Walls of cost and habit | Scale and sunk costs; switching costs and brands |
| 9 | A moat that held | Tobacco: fewer smokers, the highest returns |
| 10 | Walls of networks and law | Links among users; Visa; patents and licences |
| 11 | Five forces | Porter, 1979; airlines against tobacco |
| 12 | Buyers and suppliers | TSMC, Foxconn, Apple and Qualcomm's margins |
| 13 | A moat in the accounts | Visa, Costco and Delta's margins since 2009 |
| 14 | Good for whom? | Reward or toll |
| — | Intermission | Eight industries' returns, 2015-2025; the story so far |
| 15 | Moats that drained | Newspapers and Kodak |
| 16 | Called it? | Buffett on airlines; this series' call on the top ten |
| — | The moat, and what comes next | The answers; Part 6, the cycle |

## What is computed, and from what

`compute.py` reads Damodaran's tables for 2015-2025 (each published the following January) and takes his return on
capital and cost of capital as published; banks, whose return on capital he does not compute, drop out, leaving 90
industries for 2025. Persistence compares each industry's average return over 2015-2019 with its average over
2022-2025 (88 industries present throughout), by Spearman's rank correlation and quartile means. Profit above the cost
of capital is (return - cost) × book capital, in Damodaran's dollars. The Census figures are the 2022 Economic
Census's share of sales of the four largest firms, for every six-digit industry with a published ratio. The eight
industries in chapter 7 are matched by hand between Damodaran's names and Census codes; the match is this film's and
approximate. The entrant game and the fading curve are models. Margins are operating income over revenue from each
company's Forms 10-K (SEC company facts).

## Problems and solutions

**1.** *A business needs $8m of capital and earns $5m before tax. Twenty years later it needs $40m and earns $82m.
What did each extra dollar of capital add to yearly profit? Compare a business that adds $159m of profit on $509m of
extra capital.*

*Solution.* (82 - 5) / (40 - 8) = $2.41 a year per extra dollar, against 159 / 509 = $0.31. The first business can
grow while sending almost all its profit to its owners; the second must keep reinvesting to grow.

**2.** *An incumbent earns $100m a year alone. A rival would pay $30m a year to enter, after which each earns $40m.
The incumbent can build capacity for $20m a year that cuts the rival's post-entry profit to $25m. Does the rival
enter, and is the capacity worth building?*

*Solution.* Without the move the rival enters (40 > 30) and the incumbent earns 40. With it the rival would earn 25 <
30, so it stays out, and the incumbent earns 100 - 20 = 80. The capacity is worth building because it is paid for
before the rival decides; a mere threat to cut prices would not change the rival's sums.

**3.** *An industry earns 15% on $200bn of capital, against a cost of capital of 8%. What is its profit above the
cost of capital?*

*Solution.* (0.15 - 0.08) × 200 = $14bn a year: the amount its capital earns beyond what the same money could have
earned elsewhere at the same risk.

**4.** *A market has firms with shares of 40%, 30%, 20% and 10%. Compute the four-firm ratio and the HHI. If the two
smallest merge, what happens to each, and would the 2023 guidelines presume harm?*

*Solution.* CR4 = 100%; HHI = 1,600 + 900 + 400 + 100 = 3,000. After the merger: CR4 still 100% (now three firms);
HHI = 1,600 + 900 + 900 = 3,400, up 400. The market is above 1,800 and the increase is above 100, so the merger is
presumed to lessen competition. The four-firm ratio missed the change entirely.

**5.** *A network has 10 users. How many possible links? If it grows to 20, by how much do users and links grow?*

*Solution.* 10 × 9 / 2 = 45 links; 20 × 19 / 2 = 190. Users double; links multiply by 4.2. Each new user joins a
network that is worth more to join, which is why networks tend to tip to one winner.

**6.** *Three companies' operating margins have standard deviations of 0.4, 10 and 20 points over 17 years. Which
pattern best indicates a moat, and why is the height of the margin not enough?*

*Solution.* The steadiest. A moat protects a return from rivals and from bad years; a high but volatile margin may
reflect a boom rather than a barrier. Costco's thin margin is steady because no rival can undercut its prices; an
airline's can be high in a good year and deeply negative in a bad one.

## Glossary

- **Moat:** whatever stops rivals from competing away a business's high returns.
- **Return on capital:** operating profit after tax divided by the money owners and lenders have put in.
- **Cost of capital:** the return investors could expect elsewhere at the same risk.
- **Economic profit (EVA):** profit above the cost of capital: (return - cost) × capital.
- **Entry barrier:** a cost or condition a newcomer faces that the incumbent does not.
- **Credible commitment:** a move paid for in advance that changes what a rival can expect.
- **Four-firm concentration ratio (CR4):** the four largest firms' share of an industry's sales.
- **HHI:** the sum of the squared market shares of all firms, from near 0 to 10,000.
- **Switching cost:** what a customer loses by moving to a rival.
- **Network effect:** each user makes a product more valuable to the others.
- **Five forces:** rivalry, entrants, substitutes, buyers and suppliers (Porter, 1979).

## Lab and interactive

- `python -m videos.industry.labs 5`: See's and FlightSafety's returns on extra capital; the persistence of
  industry returns; the spread of concentration; profit above the cost of capital; HHI examples; the steadiness of
  three companies' margins; the base rate behind the series' call.
- The interactive (course site): the entrant. Set your monopoly profit, the rival's set-up cost, the shared profit
  after entry, and what your move costs and how much it cuts the rival's profit, and see whether it keeps the rival
  out and whether it pays.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p05.py`) or the Filing Room
(`explainer/industry/data/SOURCES.md`). The main ones:

- Berkshire Hathaway, letter to shareholders for 2007 (February 2008), pp. 6-8.
- Aswath Damodaran, NYU Stern, "Excess Returns (EVA) by industry, US companies", 2015-2025.
- US Census Bureau, 2022 Economic Census, Concentration of Largest Firms for the U.S. (April 2025).
- A. McGahan and M. Porter, "How much does industry matter, really?", *Strategic Management Journal* 18 (1997).
- M. Porter, "How Competitive Forces Shape Strategy", *Harvard Business Review*, March 1979.
- US Department of Justice and Federal Trade Commission, Merger Guidelines (2023), Guideline 1.
- CDC: adult smoking in 1965 (press release, March 2022) and 2022 (*MMWR* 73(29), 2024).
- Forms 10-K of Visa, Costco and Delta (SEC company facts); Eastman Kodak's Forms 10-K and Form 8-K of 19 January 2012.
- Pew Research Center, estimated advertising and circulation revenue of the newspaper industry (2021).
- 35 U.S.C. 154 (patent term).
- *Called it?*: the series' own call is in `explainer/industry/calls.py`.
