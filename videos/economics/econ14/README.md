# Economics, Built: Part 14, Incentives

Part 14 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second of Act IV, *Failure and Design*. It asks how you get someone to work for
you when you can't see what they do, and answers: pay on what you can see, in proportion to what it tells you about
effort, and only as strongly as the agent's dislike of risk and the narrowness of the measure allow. Where the work is
one person's own and easy to count, a share of the output raises it by a fifth to a half. Where the measure misses
much of the job, pay weakly, design the job, and lean on ownership, promotions, careers and relationships; and beware
of replacing a norm with a price.

It opens in Xiaogang, a poor village in Anhui province, in 1978. Eighteen households share whatever the commune's
fields produce, so a family that works harder keeps about an eighteenth of what it adds. Late in the year the farmers
meet in secret and put their thumbprints on a contract to divide the land, deliver each family's quota and keep the
rest; if the leaders are jailed, the others will raise their children. The next harvest is far larger, and within a few
years the household responsibility system covers rural China. From there it covers:

- a game: write Friday's contract for Crusoe's grove, a fixed pay and a share of the harvest;
- teams and the free rider (Alchian and Demsetz 1972; Holmström 1982): a monitor who keeps the residual, and breaking
  the budget;
- the principal-agent problem with two efforts and two harvests (Ross 1973; Mirrlees 1975; Holmström 1979; Grossman and
  Hart 1983): the participation and incentive constraints, the cheapest contract, and pay as an inference;
- insurance against incentives: the linear contract (Holmström and Milgrom 1987) and the optimal share
  $\beta^* = 1/(1 + rc\sigma^2)$; Prendergast's tenuous trade-off (1999, 2002);
- the informativeness principle (Holmström 1979): filtering out the weather, and chief executives paid for luck
  (Bertrand and Mullainathan 2001);
- piece rates at Safelite (Lazear 2000): incentives and sorting; tree planters (Shearer 2004) and fruit pickers
  (Bandiera, Barankay and Rasul 2005);
- an intermission without narration: GDP per head in China and India, 1950-2022;
- multitasking (Holmström and Milgrom 1991): what you pay for is what you get; Kerr's folly (1975); and *Called it?*:
  cheating teachers in Chicago (Jacob and Levitt 2003);
- tournaments (Lazear and Rosen 1981; Rosen 1986): golf (Ehrenberg and Bognanno 1990), mutual funds (Brown, Harlow and
  Starks 1996) and sabotage (Lazear 1989);
- career concerns (Holmström 1982, published 1999) and explicit pay near retirement (Gibbons and Murphy 1992); the
  ratchet (Weitzman 1980) and commitment;
- efficiency wages: Ford's five-dollar day (Raff and Summers 1987), Shapiro and Stiglitz (1984), gift exchange (Akerlof
  1982; Fehr, Kirchsteiger and Riedl 1993; Gneezy and List 2006);
- sharecropping from Marshall (1890) through Cheung (1969) to Stiglitz (1974); owned against sharecropped plots (Shaban
  1987); Operation Barga (Banerjee, Gertler and Ghatak 2002); China's reform measured (Lin 1992);
- when incentives backfire: the Haifa fine (Gneezy and Rustichini 2000), a Swiss nuclear-waste site (Frey and
  Oberholzer-Gee 1997), token payments, and incentives as messages (Bénabou and Tirole 2003, 2006);
- a new dial (output's response to piece rates); pay, franchises and procurement in practice (Brickley and Dark 1987;
  Jensen and Murphy 1990; Hall and Liebman 1998; Laffont and Tirole 1993); and a frontier chapter on relational
  contracts (Baker, Gibbons and Murphy 2002; Levin 2003) and incentives for machines (Hadfield-Menell and Hadfield 2019;
  Gao, Schulman and Hilton 2023).

## Build it

```bash
python -m videos.economics.econ14.compute              # every number (seconds), into .cache/econ14/
python tools/qa_scene.py econ14 Agency                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ14 -q l   # the whole part, silent preview
python tools/build.py econ14                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 14                     # the lab
```

The data are frozen extracts in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): the Maddison Project Database 2023's GDP per head for
China and India; Gneezy and Rustichini's Table 1 (transcribed for Part 1); and transcribed passages from Lazear (2000
and the 1996 working paper), Shearer (2004), Bandiera, Barankay and Rasul (2005), Raff and Summers (1987), Lin (1992),
Jacob and Levitt (2003), Banerjee, Gertler and Ghatak (2002), Shaban (1987) and Frey and Oberholzer-Gee (1997), in
`explainer/economics/data/tables.py` with where they were read and the date they were checked.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | How do you get someone to work for you when you can't see what they do? | Xiaogang, 1978: eighteen households, an eighteenth of what each adds; the secret contract with thumbprints; the household responsibility system; the result, not the effort, everywhere (sales, executives, teachers, tenants, contractors, models); the question; objectives |
| 1 | Play it: write Friday's contract | A harvest of effort plus luck (sd 5 baskets); risk aversion $r = 0.2$, effort cost $0.1e^2/2$; shares of none, a third, two-thirds, all, with the fixed pay that keeps Friday on: effort 0, 3.33, 6.67, 10 and profits 0, 2.50, 3.33, 2.50; first best 5.00 |
| 2 | Teams and the free rider | $n$ households sharing equally: effort $1/n$ of the efficient level; at 18, 0.056 and 89% of the surplus lost; Alchian and Demsetz's monitor and residual claimant; Holmström's budget breaker; dividing the team |
| 3 | The principal-agent problem | Hard work makes a good harvest (100) 80% likely against 40% (else 40); log utility, effort costs 0.3, other work 2; the participation and incentive lines in utility space; the cheapest pair 11.59 and 5.47, an expected 10.37 against a flat 9.97 if effort could be seen (a risk premium of 0.39); profit 77.6 against 56.6 for easy work; pay as an inference, the likelihood ratio |
| 4 | Insurance against incentives | Holmström and Milgrom's linear contract: $e = \beta/c$, the risk premium $\tfrac12 r\beta^2\sigma^2$, $\beta^* = 1/(1 + rc\sigma^2)$, 2/3 here; the best share against noise for $r$ = 0.05, 0.2, 0.8; the agency cost, 1.67 of 5; Prendergast's evidence and explanation |
| 5 | The informativeness principle | A common shock (sd 4) and Friday's own luck (sd 3), sixteen simulated seasons against the island's average; the variance from 25 to 9, the share from 0.67 to 0.85, the surplus from 3.33 to 4.24; Holmström (1979); CEOs rewarded for luck, except with a large shareholder on the board (Bertrand and Mullainathan 2001) |
| 6 | Piece rates: Safelite | Hourly pay with a standard to a piece rate with a floor, 1994-95; output per worker up 44%, about half incentives and half sorting; pay up about 10%; the working paper's 20-36%; tree planters (+20%, an experiment) and fruit pickers (at least +50% against relative pay) |
| | Intermission: China and India | No narration: GDP per head, 2011 dollars, log scale, 1950-2022: China 1,744 in 1978 and 19,238 in 2022 (11 times), India 1,540 and 7,766 (5 times); China's line as a tune; the story so far |
| 7 | Multitasking: what you pay for is what you get | A teacher's two tasks sharing hours; Agora's efforts against the bonus: the unmeasured task falls from 0.67 and is dropped at a bonus of 1; weak incentives, job design and asset ownership; Kerr (1975); *Called it?*: Jacob and Levitt's cheating in at least 4-5% of Chicago's elementary classrooms a year, right |
| 8 | Tournaments and promotions | Pay that jumps up the ladder; Lazear and Rosen: effort proportional to the prize gap, $1/(2\sigma\sqrt\pi)$ per unit, halved by twice the noise; Rosen's widening at the top; golf, mutual funds behind at midyear, sabotage |
| 9 | Career concerns and the ratchet | Holmström's market learning over a thirty-year career: the implicit incentive from 0.89 to 0; Gibbons and Murphy's explicit share rising from 0.07 to 0.67; Weitzman's ratchet: effort to a tenth; planning from the achieved level; price caps and commitment |
| 10 | Efficiency wages | Ford's five-dollar day of 1914 and Raff and Summers' queues; Shapiro and Stiglitz's no-shirking wage against demand: 86 of 100 employed at a wage of 2.55, 14% unemployed; turnover, selection, gift exchange in the laboratory and the field |
| 11 | Sharecropping, and China's household responsibility system | Wage, rent and share; Marshall, Cheung, Stiglitz; Agora's best share 0.61 (30.5 against 18 for a rent, 0 for a wage); Shaban's plots; Operation Barga, about 28% of West Bengal's later growth in farm productivity; Lin: about half of China's 1978-84 farm growth from the new contracts |
| 12 | When incentives backfire | The Haifa fine: 8.0 late pick-ups a week before, 16.4 with it, 18.7 after; the Swiss repository: 50.8% accept unpaid, 24.6% when paid $2,175-6,525 a year; pay enough or don't pay at all; Bénabou and Tirole; norms and incomplete contracts |
| 13 | The Dials: how much do piece rates raise output? | The new dial: Lazear 44% (half of it the same workers), Shearer 20%, Bandiera, Barankay and Rasul 50%: a fifth to a half where output is one person's and easy to count |
| 14 | In practice: pay, franchises and procurement | One line from a wage to a rent; franchising far from head office (Brickley and Dark 1987); chief executives: \$3.25 per \$1,000 (Jensen and Murphy 1990) and stock and options (Hall and Liebman 1998); cost-plus, incentive and fixed-price contracts; Laffont and Tirole's menu; ownership (Part 8) |
| 15 | Frontier: relational contracts, and incentives for machines | A bonus no court enforces: the effort it sustains, $\min(1/c, 2\delta/c)$, first best from $\delta = 1/2$; Gibbons and Henderson; specification gaming (the boat race, 2016); rewards as incomplete contracts; reward-model overoptimization (Gao, Schulman and Hilton 2023); Goodhart and Strathern |
| | Recap, problems, and the road ahead | The answer; twelve lines; problems; reading; Cheung's bees, and Part 15 |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's contracts module (`explainer.economics.agora.contracts`),
with the Island's Part 14 truths in `explainer.economics.island`, or from the Data Room or a transcribed table; the
narration states the cached numbers.

- **Contracts.** The team's equilibrium and efficient efforts; the linear contract's effort, risk premium and surplus
  at any share, and the best share; the two-outcome contract with both constraints binding, in closed form; relative
  performance evaluation with the common shock removed; the multitask first-order conditions solved as a linear
  system, with the corner where the unmeasured task is dropped.
- **Careers, tournaments and wages.** Lazear and Rosen's effort from the density of the difference of two normal
  shocks at zero; Holmström's implicit incentive as the discounted sum of the weights later wages put on one year's
  output under normal learning, and Gibbons and Murphy's explicit share on top; Weitzman's ratchet; Shapiro and
  Stiglitz's no-shirking curve against linear labour demand, with the equilibrium by Brent's method; the relational
  contract's self-enforcement condition.
- **Land and machines.** The sharecropping surplus against the tenant's share and its best value; the shape of the
  gold and proxy rewards Gao, Schulman and Hilton fitted for best-of-$n$ sampling, $d(\alpha - \beta d)$, with
  illustrative constants.
- **Data.** The Haifa centres' weekly late pick-ups, fined and not; GDP per head for China and India; the dial's rows.

## Problems and solutions

**1.** *Teams: $n$ members share output $a\sum e_i$ equally, and effort costs $ce^2/2$; show $e = a/(nc)$ and that a
share $(n-1)^2/n^2$ of the surplus is lost; check 89% at $n = 18$.*

*Solution.* Member $i$ gets $\frac{a}{n}\sum_j e_j - ce_i^2/2$, so the first-order condition is $a/n = ce_i$, and
$e = a/(nc)$ whatever the others do. Each member's surplus is then $ae - ce^2/2 = \frac{a^2}{2c}\cdot\frac{2n - 1}{n^2}$,
against $\frac{a^2}{2c}$ at the efficient effort $a/c$. The share lost is $1 - \frac{2n-1}{n^2} = \frac{(n-1)^2}{n^2}$;
at $n = 18$ that is $289/324 = 0.892$.

**2.** *Holmström and Milgrom: derive $\beta^* = 1/(1 + rc\sigma^2)$; check 2/3 in the Play it, and profits of 2.50 at
shares of 1/3 and 1.*

*Solution.* Paid $\alpha + \beta y$ with $y = e + \varepsilon$, Friday's certainty equivalent is $\alpha + \beta e -
ce^2/2 - r\beta^2\sigma^2/2$, maximized at $e = \beta/c$. Crusoe sets $\alpha$ so that it is zero, and keeps $e -
\alpha - \beta e = \beta/c - \beta^2/(2c) - r\beta^2\sigma^2/2$. Setting the derivative to zero, $1/c - \beta/c -
r\sigma^2\beta = 0$, so $\beta^* = 1/(1 + rc\sigma^2)$. With $r = 0.2$, $c = 0.1$, $\sigma = 5$, $rc\sigma^2 = 0.5$ and
$\beta^* = 2/3$, with profit $6.667 - 2.222 - 1.111 = 3.33$. At $\beta = 1/3$: $3.333 - 0.556 - 0.278 = 2.50$; at
$\beta = 1$: $10 - 5 - 2.5 = 2.50$.

**3.** *Two outcomes: with log utility, derive the cheapest wages that buy hard work; check 11.59 and 5.47, and the
risk premium of 0.39.*

*Solution.* Both constraints bind at the optimum: if participation were slack, lowering both utilities by the same
amount would keep the incentive constraint and save money; if the incentive constraint were slack, moving the two
utilities closer at the same average would, by Jensen's inequality, cost less. The incentive constraint, $0.4(\ln w_H
- \ln w_L) = 0.3$, gives a gap of 0.75; participation, $0.8\ln w_H + 0.2\ln w_L - 0.3 = 2$, then gives $\ln w_L =
2.3 - 0.8 \times 0.75 = 1.7$ and $\ln w_H = 2.45$: $w_L = e^{1.7} = 5.47$ and $w_H = e^{2.45} = 11.59$. The expected
wage is $0.8 \times 11.59 + 0.2 \times 5.47 = 10.37$, against $e^{2.3} = 9.97$ for a flat wage if effort could be seen:
the premium is 0.39.

**4.** *Informativeness: show that paying on Friday's harvest less the weather cuts the variance from 25 to 9 and
raises the share to 0.85.*

*Solution.* The harvest is $e + m + u$ with $\mathrm{var}\,m = 16$ and $\mathrm{var}\,u = 9$, so its variance is 25
and $\beta^* = 1/(1 + 0.02 \times 25) = 0.667$. Paying on $y - m = e + u$ leaves variance 9 and $\beta^* = 1/(1 + 0.02
\times 9) = 0.847$. At the best share the surplus is $\beta^*/(2c)$, which rises from 3.33 to 4.24. If the measure of
the weather were itself noisy, $z = m + v$, the best contract would pay on $y - kz$ with $k = \mathrm{cov}(y, z)/
\mathrm{var}\,z$, the regression coefficient of the harvest on the signal.

**5.** *Multitasking: solve the two first-order conditions; show the unmeasured task is dropped once the bonus reaches
1.*

*Solution.* The agent gets $(1 + \beta)e_1 + e_2 - \tfrac12(e_1^2 + e_2^2 + 2se_1e_2)$ with $s = 0.5$, so $e_1 + 0.5e_2
= 1 + \beta$ and $e_2 + 0.5e_1 = 1$. Solving, $e_1 = (2 + 4\beta)/3$ and $e_2 = 2(1 - \beta)/3$: at no bonus both are
$2/3$, and $e_2$ reaches zero at $\beta = 1$. Beyond that the agent is at the corner $e_2 = 0$ and $e_1 = 1 + \beta$.

**6.** *Tournaments: show effort is the prize gap times $1/(2\sigma\sqrt\pi)$, over $c$; what does doubling the noise
do?*

*Solution.* Contestant $i$ wins if $e_i - e_j + \varepsilon_i - \varepsilon_j > 0$, where $\varepsilon_i -
\varepsilon_j$ is normal with standard deviation $\sigma\sqrt2$. So the chance of winning rises with $e_i$ at rate
$\phi(0)/(\sigma\sqrt2) = 1/(2\sigma\sqrt\pi)$ when efforts are equal, and with prizes $w_L$ and $w_L + \Delta$ the first-order
condition is $ce = \Delta/(2\sigma\sqrt\pi)$. Effort does not depend on $w_L$. Doubling $\sigma$ halves effort; to keep
it, the gap must double.

**7.** *Shapiro and Stiglitz: show the no-shirking wage rises without bound as unemployment falls; check 14%
unemployed.*

*Solution.* With effort cost 1, a shirker caught with probability 0.5, a discount rate 0.05 and separations at 0.1, the
no-shirking wage is $w = 1 + 2(0.05 + 0.1/u)$, which goes to infinity as $u \to 0$: at full employment a fired worker
is hired at once, and no wage deters shirking. Demand is $w = 6 - 0.04L$ with $L = 100(1 - u)$, that is $w = 2 + 4u$.
Setting $2 + 4u = 1.1 + 0.2/u$ gives $4u^2 + 0.9u - 0.2 = 0$, so $u = (-0.9 + \sqrt{4.01})/8 = 0.138$, and $w = 2.55$.

**8.** ★ *Relational contracts: show the most effort a promise can sustain is $\min(1/c, 2\delta/c)$, first best once
$\delta \ge 1/2$.*

*Solution.* For effort $e$ the agent needs a bonus $b \ge ce^2/2$; the principal then keeps $e - b$ a season. Paying is
worth it only if the bonus is no more than what reneging would throw away: $b \le \frac{\delta}{1 - \delta}(e - b)$.
With $b = ce^2/2$ that is $\frac{ce^2}{2}\cdot\frac{1}{1 - \delta} \le \frac{\delta}{1-\delta}e$, or $e \le 2\delta/c$.
The principal never asks for more than the efficient $1/c$, so the effort sustained is $\min(1/c, 2\delta/c)$, the
efficient level once $\delta \ge 1/2$.

## Where it comes back

| Idea | Parts |
|---|---|
| Externalities and contracts between neighbours | 15 *Spillovers* |
| Auctions and mechanism design | 16 *Auctions*, 17 *Markets by Design* |
| Market power, regulation and antitrust | 43 *Measuring Market Power*, 44 *Dynamics, Platforms and Antitrust* |
| Work, wages and labour markets; unemployment | 24 *Looking for Work*, 38 *Work and Wages* |
| Development: land, credit and the household | 46 *Development* |
| Information design and persuasion | 53 *Information and Persuasion* |
| Personnel economics and organizations; the piece-rate dial | 62 *Inside the Firm* |
| Machines, prediction and AI | 64 *Machines that Learn*, 65 *The Economics of AI* |

## Sources

- Armen A. Alchian and Harold Demsetz, "Production, Information Costs, and Economic Organization", *American Economic
  Review* 62(5) (1972): 777-795; Bengt Holmström, "Moral Hazard in Teams", *Bell Journal of Economics* 13(2) (1982):
  324-340.
- Stephen A. Ross, "The Economic Theory of Agency: The Principal's Problem", *American Economic Review* 63(2) (1973):
  134-139; James A. Mirrlees, "The Theory of Moral Hazard and Unobservable Behaviour: Part I", *Review of Economic
  Studies* 66(1) (1999; written 1975): 3-21; Bengt Holmström, "Moral Hazard and Observability", *Bell Journal of
  Economics* 10(1) (1979): 74-91; Sanford J. Grossman and Oliver D. Hart, "An Analysis of the Principal-Agent
  Problem", *Econometrica* 51(1) (1983): 7-45.
- Bengt Holmström and Paul Milgrom, "Aggregation and Linearity in the Provision of Intertemporal Incentives",
  *Econometrica* 55(2) (1987): 303-328; "Multitask Principal-Agent Analyses: Incentive Contracts, Asset Ownership, and
  Job Design", *Journal of Law, Economics and Organization* 7 (1991): 24-52; Canice Prendergast, "The Provision of
  Incentives in Firms", *Journal of Economic Literature* 37(1) (1999): 7-63; "The Tenuous Trade-off between Risk and
  Incentives", *Journal of Political Economy* 110(5) (2002): 1071-1102.
- Marianne Bertrand and Sendhil Mullainathan, "Are CEOs Rewarded for Luck? The Ones without Principals Are", *Quarterly
  Journal of Economics* 116(3) (2001): 901-932; Michael C. Jensen and Kevin J. Murphy, "Performance Pay and
  Top-Management Incentives", *Journal of Political Economy* 98(2) (1990): 225-264; Brian J. Hall and Jeffrey B.
  Liebman, "Are CEOs Really Paid Like Bureaucrats?", *Quarterly Journal of Economics* 113(3) (1998): 653-691.
- Edward P. Lazear, "Performance Pay and Productivity", *American Economic Review* 90(5) (2000): 1346-1361 (NBER Working
  Paper 5672, 1996); Bruce Shearer, "Piece Rates, Fixed Wages and Incentives: Evidence from a Field Experiment",
  *Review of Economic Studies* 71(2) (2004): 513-534; Oriana Bandiera, Iwan Barankay and Imran Rasul, "Social
  Preferences and the Response to Incentives: Evidence from Personnel Data", *Quarterly Journal of Economics* 120(3)
  (2005): 917-962.
- Steven Kerr, "On the Folly of Rewarding A, While Hoping for B", *Academy of Management Journal* 18(4) (1975):
  769-783; Brian A. Jacob and Steven D. Levitt, "Rotten Apples: An Investigation of the Prevalence and Predictors of
  Teacher Cheating", *Quarterly Journal of Economics* 118(3) (2003): 843-877.
- Edward P. Lazear and Sherwin Rosen, "Rank-Order Tournaments as Optimum Labor Contracts", *Journal of Political
  Economy* 89(5) (1981): 841-864; Sherwin Rosen, "Prizes and Incentives in Elimination Tournaments", *American Economic
  Review* 76(4) (1986): 701-715; Ronald G. Ehrenberg and Michael L. Bognanno, "Do Tournaments Have Incentive Effects?",
  *Journal of Political Economy* 98(6) (1990): 1307-1324; Keith C. Brown, W. V. Harlow and Laura T. Starks, "Of
  Tournaments and Temptations", *Journal of Finance* 51(1) (1996): 85-110; Edward P. Lazear, "Pay Equality and
  Industrial Politics", *Journal of Political Economy* 97(3) (1989): 561-580.
- Bengt Holmström, "Managerial Incentive Problems: A Dynamic Perspective", *Review of Economic Studies* 66(1) (1999;
  written 1982): 169-182; Robert Gibbons and Kevin J. Murphy, "Optimal Incentive Contracts in the Presence of Career
  Concerns", *Journal of Political Economy* 100(3) (1992): 468-505; Martin L. Weitzman, "The 'Ratchet Principle' and
  Performance Incentives", *Bell Journal of Economics* 11(1) (1980): 302-308.
- Daniel M. G. Raff and Lawrence H. Summers, "Did Henry Ford Pay Efficiency Wages?", *Journal of Labor Economics* 5(4)
  (1987): S57-S86; Carl Shapiro and Joseph E. Stiglitz, "Equilibrium Unemployment as a Worker Discipline Device",
  *American Economic Review* 74(3) (1984): 433-444; George A. Akerlof, "Labor Contracts as Partial Gift Exchange",
  *Quarterly Journal of Economics* 97(4) (1982): 543-569; Ernst Fehr, Georg Kirchsteiger and Arno Riedl, "Does Fairness
  Prevent Market Clearing?", *Quarterly Journal of Economics* 108(2) (1993): 437-459; Uri Gneezy and John A. List,
  "Putting Behavioral Economics to Work", *Econometrica* 74(5) (2006): 1365-1384.
- Alfred Marshall, *Principles of Economics* (1890); Steven N. S. Cheung, *The Theory of Share Tenancy* (1969); Joseph
  E. Stiglitz, "Incentives and Risk Sharing in Sharecropping", *Review of Economic Studies* 41(2) (1974): 219-255;
  Radwan Ali Shaban, "Testing between Competing Models of Sharecropping", *Journal of Political Economy* 95(5) (1987):
  893-920; Abhijit V. Banerjee, Paul J. Gertler and Maitreesh Ghatak, "Empowerment and Efficiency: Tenancy Reform in
  West Bengal", *Journal of Political Economy* 110(2) (2002): 239-280; Justin Yifu Lin, "Rural Reforms and
  Agricultural Growth in China", *American Economic Review* 82(1) (1992): 34-51.
- Uri Gneezy and Aldo Rustichini, "A Fine Is a Price", *Journal of Legal Studies* 29(1) (2000): 1-17; "Pay Enough or
  Don't Pay at All", *Quarterly Journal of Economics* 115(3) (2000): 791-810; Bruno S. Frey and Felix Oberholzer-Gee,
  "The Cost of Price Incentives: An Empirical Analysis of Motivation Crowding-Out", *American Economic Review* 87(4)
  (1997): 746-755; Roland Bénabou and Jean Tirole, "Intrinsic and Extrinsic Motivation", *Review of Economic Studies*
  70(3) (2003): 489-520; "Incentives and Prosocial Behavior", *American Economic Review* 96(5) (2006): 1652-1678.
- James A. Brickley and Frederick H. Dark, "The Choice of Organizational Form: The Case of Franchising", *Journal of
  Financial Economics* 18(2) (1987): 401-420; Jean-Jacques Laffont and Jean Tirole, *A Theory of Incentives in
  Procurement and Regulation* (1993).
- George Baker, Robert Gibbons and Kevin J. Murphy, "Relational Contracts and the Theory of the Firm", *Quarterly
  Journal of Economics* 117(1) (2002): 39-84; Jonathan Levin, "Relational Incentive Contracts", *American Economic
  Review* 93(3) (2003): 835-857; Robert Gibbons and Rebecca Henderson, "What Do Managers Do?", in *The Handbook of
  Organizational Economics* (2013).
- Dario Amodei and Jack Clark, "Faulty Reward Functions in the Wild", OpenAI (2016); Victoria Krakovna et al.,
  "Specification Gaming: The Flip Side of AI Ingenuity", DeepMind (2020); Dylan Hadfield-Menell and Gillian K.
  Hadfield, "Incomplete Contracting and AI Alignment", *AIES* (2019); Leo Gao, John Schulman and Jacob Hilton, "Scaling
  Laws for Reward Model Overoptimization", *ICML* (2023); Marilyn Strathern, "'Improving Ratings': Audit in the
  British University System", *European Review* 5(3) (1997): 305-321.
- The Maddison Project Database 2023 (Jutta Bolt and Jan Luiten van Zanden, Groningen Growth and Development Centre).
- Textbooks: Patrick Bolton and Mathias Dewatripont, *Contract Theory* (2005), chs. 4, 6, 8, 11; Jean-Jacques Laffont
  and David Martimort, *The Theory of Incentives* (2002); Bernard Salanié, *The Economics of Contracts*; Paul Milgrom
  and John Roberts, *Economics, Organization and Management* (1992); Robert Gibbons and John Roberts, eds., *The
  Handbook of Organizational Economics* (2013); Edward P. Lazear and Michael Gibbs, *Personnel Economics in Practice*.
