# Economics, Built: Part 13, Lemons and Signals

Part 13 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first of Act IV, *Failure and Design*. It asks what happens to a market when one
side knows more than the other, and answers: the good is driven out by the bad, and trades that would benefit both
sides don't happen; in the extreme the market vanishes. The informed respond with signals that are cheap only for
the truthful, the uninformed with screens that sort; markets grow guarantees, reputations and inspectors. All of it
costs something, and in the insurance markets where it has been measured the cost is real but modest.

It opens in the late 1960s, when George Akerlof's short paper on used cars was turned down by the *American Economic
Review* and the *Review of Economic Studies* as trivial, and by the *Journal of Political Economy*, whose referees held
that if it were right no goods could be traded. The *Quarterly Journal of Economics* printed it in 1970, thirteen
pages that started the economics of information and won a share of the 2001 Nobel prize. From there it covers:

- a game: buy a boat from Bo that you cannot inspect;
- Akerlof's market: the price at which the average boat offered is worth the price, partial unravelling, Akerlof's
  own example in which nothing trades, Gresham's law, and *Called it?*: the referees;
- guarantees that are cheap only for honest sellers, reputations, brands, chains, inspectors, licences;
- Spence's signals (1973): education that teaches nothing, the separating range, pooling, the intuitive criterion
  (Cho and Kreps 1987; Riley 1979);
- is school a signal? human capital against signalling, sheepskin effects, the GED (Tyler, Murnane and Willett 2000),
  compulsory schooling, and Caplan's case (2018);
- screening (Rothschild and Stiglitz 1976): the separating menu, and why there may be no equilibrium;
- an intermission without narration: the prices of used cars and of new vehicles against all consumer prices,
  1953-2026;
- Harvard's death spiral, 1995-97 (Cutler and Zeckhauser 1998; Cutler and Reber 1998), and Agora's;
- the Einav-Finkelstein diagram, rebuilt from Einav, Finkelstein and Cullen's estimates for Alcoa (2010), and what a
  subsidy would cost;
- testing for private information (Chiappori and Salanié 2000) and advantageous selection (Finkelstein and McGarry
  2006);
- credit rationing (after Stiglitz and Weiss 1981);
- mandates, subsidies and risk adjustment: the Affordable Care Act, Massachusetts (Hackmann, Kolstad and Kowalski
  2015), and inertia (Handel 2013);
- online feedback: Bayes's rule for a new seller, and eBay (Cabral and Hortaçsu 2010);
- a new dial (the welfare cost of adverse selection); underwriting, telematics, annuities (Finkelstein and Poterba
  2004) and *Test-Achats* (2011) in practice; and a frontier chapter on selection on moral hazard (Einav et al. 2013)
  and the end of pooling.

## Build it

```bash
python -m videos.economics.econ13.compute              # every number (seconds), into .cache/econ13/
python tools/qa_scene.py econ13 Diagram                # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ13 -q l   # the whole part, silent preview
python tools/build.py econ13                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 13                     # the lab
```

The data are frozen extracts in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): the BLS consumer price indexes for used cars and trucks
(CUSR0000SETA02), new vehicles (CUSR0000SETA01) and all items (CPIAUCSL), via FRED; and transcribed passages from
Akerlof (1970, 2003), Einav, Finkelstein and Cullen (2008, Table 4), Cutler and Zeckhauser (1998), Cutler and Reber
(1998), Tyler, Murnane and Willett (2000), Chiappori and Salanié (2000), Finkelstein and McGarry (2006), Cabral and
Hortaçsu (2010), Hackmann, Kolstad and Kowalski (2015) and Handel (2013), in `explainer/economics/data/tables.py`
with where they were read and the date they were checked.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | What happens to a market when one side knows more than the other? | Akerlof's paper turned down by the AER and the RES as trivial and by the JPE as wrong; the QJE, 1970, pp. 488-500; the 2001 Nobel with Spence and Stiglitz; private information everywhere; the question; objectives |
| 1 | Play it: buy a boat you cannot inspect | Bo's boat worth $0-100 to him, $30 more to you; offers $80, $60, $40, $30, $20: Bo sells 80-20% of the time, the boats you get are worth $70-40 to you, average gains -$8.00, $0, $4.00, $4.50, $4.00; the best blind offer $30; seven boats in ten unsold |
| 2 | Akerlof's market | With many buyers, $p = p/2 + 30$: $60, 60% of boats trade, $12 of gains lost per boat; Akerlof's own example (buyers value 3/2): no price works; unravelling; Gresham's law; his applications; *Called it?*: the referees, wrong |
| 3 | Guarantees, reputations and inspectors | Good boats $90, bad $30, half each, a pooled $60; a guarantee to pay a $100 repair costs a good seller $10 and a bad one $70, against a $30 premium (a bad seller would gain $60): it separates; reputation, brands, chains, inspectors, licences, the law; what they cost |
| 4 | Signalling: education that teaches nothing | Spence (1973): fishers landing 1 or 2 baskets; a season of school costs 1 or 0.5; separating requirements from 1 to 2 seasons; the social waste; pooling at 1.5; the intuitive criterion (Cho and Kreps 1987) and Riley's outcome; with 90% strong, pooling would pay 1.9 against 1.5 |
| 5 | Is school a signal? | Human capital (Becker, Mincer) against signalling; sheepskin effects; the GED: 10-19% for young white dropouts at the margin, no detectable effect for nonwhite dropouts (Tyler, Murnane and Willett 2000); compulsory schooling and Part 4; Caplan (2018) |
| 6 | Screening: contracts that sort | Wealth $100, a $60 storm, risks 0.1 and 0.4, 30% careless: full cover for $24 and $12.57 of cover for $1.26; the careless indifferent between them; the pooled price 0.19; no equilibrium if fewer than about 11% are careless |
| | Intermission: used cars and new | No narration: the CPIs for used cars and trucks and for new vehicles over the CPI, 1953 = 100, to October 2026 (used cars at their low in June 2020, then up 30% by January 2022); the used-car line as a tune; the story so far |
| 7 | The death spiral: Harvard, 1995-97 | About 10,000 employees; the PPO's extra charge $400-500 and about 20% enrolled until 1994; an equal contribution from 1995: about $1,000 and 15% (leavers aged 46 against 51), more than $2,000 and about 9% in 1996 (leavers 20% healthier), disbanded in 1997; Agora's spiral (22.6% to 2.5% in four years); Cutler and Reber: a loss of 2-4% of spending against premiums 5-8% lower |
| 8 | Selection in pictures | Demand, average cost and marginal cost; C and E; Alcoa's prices $384-659; $D = 0.940 - 0.00070p$, $AC = 391.69 + 0.155p$; Agora's rebuild: $464 against $266, 14 points fewer insured, a triangle of $9.46 a head (the paper: $463, $264, $9.55, about 3% of the surplus at stake); a subsidy to reach E would cost about $45, five times the gain |
| 9 | Testing for private information | The positive-correlation test; young French drivers (Chiappori and Salanié 2000): no correlation; Agora's 20,000 drivers: 0.082 with adverse selection, 0.003 with none, -0.027 when caution drives both; long-term care (Finkelstein and McGarry 2006) |
| 10 | Credit rationing | Safe borrowers succeed 90% of the time, risky ones 50%; a $60 cost of chasing a default; the safe leave above $177.78; the bank's best rate $177.78 with $106.42 back per $100, against at most $99.99 from the risky alone; rationing (Stiglitz and Weiss 1981) |
| 11 | Mandates, subsidies and risk adjustment | Six remedies and their costs; the Affordable Care Act and Massachusetts; Hackmann, Kolstad and Kowalski (2015): 4.1% per person, $51.1 million a year; the zero penalty from 2019; Handel (2013): curing inertia would double the loss, to 8.2% of premiums |
| 12 | Online markets: feedback as a fix | A new seller honest with chance 0.6: three good reviews take the price from $76.00 to $91.37, one bad to $65.60, twelve more good to $99.68; eBay (Cabral and Hortaçsu 2010); inflated and fake reviews; escrow and guarantees |
| 13 | The Dials: how much does adverse selection cost? | The new dial: Einav, Finkelstein and Cullen 3%, Cutler and Reber 2-4%, Hackmann, Kolstad and Kowalski 4.1%; Handel's 8.2% if inertia were cured: depends on the setting |
| 14 | In practice: insurance, underwriting and trust | Underwriting, credit scores and telematics; annuitants live longer (Finkelstein and Poterba 2004); *Test-Achats* (2011): one price for men and women; the kit; pointers to Parts 14, 42 and 61 |
| 15 | Frontier: selection on moral hazard, and the end of pooling | Einav, Finkelstein, Ryan, Schrimpf and Cullen (2013): selection on moral hazard as important as on health risk; data, algorithms and genes; the Genetic Information Nondiscrimination Act (2008); open questions |
| | Recap, problems, and the road ahead | The answer; twelve lines; problems; reading; Xiaogang's secret contract, and Part 14 |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's information module (`explainer.economics.agora.info`),
with the Island's Part 13 truths in `explainer.economics.island`, or from the Data Room or a transcribed table; the
narration states the cached numbers.

- **Lemons.** Uniform quality with an additive or proportional premium: the value of the average boat offered at
  each price, the highest price at which it covers the price (refined by Brent's method), the share traded and the
  gains lost; a single buyer's offers in closed form.
- **Signals and screens.** The guarantee's two separation conditions; Spence's separating range, the least-cost
  equilibrium and the pooling wage; Rothschild and Stiglitz with log utility: full cover for the high risks, the
  largest cover at the low risks' fair price that the high risks do not prefer (on a grid of 4,001 covers), the best
  pooled contract for the low risks, existence, and the share of high risks at which it fails (Brent); the
  indifference curves through both contracts (Brent at each cover).
- **Selection.** Einav, Finkelstein and Cullen's two published lines turned into demand, average and marginal cost
  in the share insured; the competitive price ($p = AC$), the efficient one ($P = MC$, Brent), the triangle by the
  trapezoid rule, and the subsidy's social cost at a marginal cost of public funds of 0.3. Agora's death spiral: 20,000
  employees with lognormal expected extra costs (sd 1.4), valuations 1.5 times that plus a normal taste, a $450 charge
  in year 0, then the previous year's average extra cost (seed 1995).
- **The rest.** The positive-correlation test on 20,000 simulated drivers with Beta(2, 18) risks, under adverse,
  advantageous and no selection (seed 2000); the two-type credit market's expected repayment on a grid of rates;
  Bayes's rule for a seller's reputation; the vehicle CPIs divided by the CPI for all items.

## Problems and solutions

**1.** *Lemons: quality uniform on $[0, H]$, worth $q$ to sellers and $q + a$ to buyers; show the price is $2a$ (if
$2a \le H$) and the share traded $2a/H$; check $60 and 60%.*

*Solution.* At a price $p \le H$ every boat with $q \le p$ is offered, so the average quality offered is $p/2$ and a
buyer values the average boat at $p/2 + a$. Competing buyers bid the price up to that value, and no higher: $p = p/2
+ a$, so $p = 2a$. The boats offered are those with $q \le 2a$, a share $2a/H$. With $a = 30$ and $H = 100$: $60, and
60% of boats. (If $2a > H$, every boat is offered at $p = H/2 + a$ and all trade.)

**2.** *Akerlof's example: buyers value a car at $m$ times its worth to the seller; show nothing trades if $m < 2$ and
everything if $m \ge 2$.*

*Solution.* With quality uniform on $[0, H]$, at a price $p \le H$ the cars offered are worth $p/2$ to their owners on
average and $mp/2$ to a buyer. If $m < 2$ then $mp/2 < p$ for every $p > 0$, so buyers will not pay any positive
price for what is offered, and only $p = 0$ (no trade) is consistent. If $m \ge 2$ then at $p = H$ every car is
offered, worth $mH/2 \ge H$ to a buyer on average, so the price can be $H$ or more and everything trades.

**3.** *Play it: show a single buyer's best offer is $p = a$, with expected gain $a^2/2H$; check $30 and $4.50.*

*Solution.* An offer $p$ is accepted with chance $p/H$ and buys a boat worth $p/2 + a$ to the buyer on average, so the
expected gain is $\frac{p}{H}(p/2 + a - p) = \frac{p}{H}(a - p/2)$. Its derivative, $(a - p)/H$, is zero at $p = a$,
where the gain is $\frac{a}{H} \cdot \frac{a}{2} = \frac{a^2}{2H}$. With $a = 30$ and $H = 100$: $30 and $4.50.

**4.** *The guarantee: with chapter 3's numbers, check that good sellers gain by offering it and bad sellers don't gain
by copying.*

*Solution.* Without guarantees every boat sells at $0.5 \times 90 + 0.5 \times 30 = 60$. If buyers believe that
guaranteed boats are good, a guaranteed boat sells at $90$. A good seller gains $90 - 60 = 30$ and expects to pay
$0.1 \times 100 = 10$ in repairs: net $+20$. A bad seller who copied would gain $90 - 30 = 60$ over being known as bad
and expect to pay $0.7 \times 100 = 70$: net $-10$. So only good sellers offer the guarantee, and the buyers' belief
is correct.

**5.** *Spence: derive the separating range $[1, 2]$ for chapter 4's fishers, and show the strong prefer pooling when
90% are strong.*

*Solution.* In a separating equilibrium the strong take $e^*$ seasons and earn 2, the weak take none and earn 1. The
weak must not copy: $2 - 1 \cdot e^* \le 1$, so $e^* \ge 1$. The strong must prefer to study: $2 - 0.5\,e^* \ge 1$, so
$e^* \le 2$. Least-cost separation ($e^* = 1$) leaves the strong $2 - 0.5 = 1.5$. If 90% are strong, pooling at no
school pays everyone $0.9 \times 2 + 0.1 \times 1 = 1.9 > 1.5$, so the strong would be better off pooling; the
intuitive criterion still rules pooling out, because a fisher who studied one season could only be strong.

**6.** *Rothschild and Stiglitz: verify that the careless are indifferent between full cover at 0.4 and $12.57 of
cover at 0.1.*

*Solution.* With wealth 100 and a loss of 60, full cover at the careless price costs $0.4 \times 60 = 24$, leaving 76
in both states: utility $\ln 76 = 4.3307$. Cover of 12.57 at the careful price costs 1.257, leaving 98.743 without a
storm and $100 - 60 + 12.57 - 1.257 = 51.313$ with one; to the careless that is worth $0.6 \ln 98.743 + 0.4 \ln
51.313 = 0.6 \times 4.5925 + 0.4 \times 3.9380 = 4.3307$. Equal, to the precision shown; any more cover at that price
would attract them.

**7.** *Einav, Finkelstein and Cullen: from $D = 0.94 - 0.0007p$ and $AC = 391.69 + 0.155p$, derive the competitive
and efficient prices.*

*Solution.* Competition sets $p = AC(p)$: $p = 391.69 + 0.15524p$, so $p = 391.69/0.84476 = 463.67$, where $D =
0.615$. In the share insured, $p(D) = (0.94 - D)/0.0007$ and $AC(D) = 391.69 + 0.15524\,p(D) = 600.15 - 221.77D$, so
total cost $D \cdot AC(D)$ has marginal cost $MC(D) = 600.15 - 443.54D$. Efficiency sets $p(D) = MC(D)$: $1342.86 -
1428.57D = 600.15 - 443.54D$, so $D = 0.754$ and $p = 265.7$. The triangle between demand and marginal cost over $D
\in [0.615, 0.754]$ is $\tfrac12 \times 0.139 \times (463.67 - 327.2) \approx 9.5$ dollars a head.

**8.** ★ *Stiglitz and Weiss: show the bank's expected repayment falls when the safe borrowers leave at $177.78, and
find its maximum.*

*Solution.* A borrower applies while the project's expected profit $y - sR$ is positive: the safe ($s = 0.9$, $y =
160$) up to $R = 160/0.9 = 177.78$, the risky ($s = 0.5$, $y = 130$) up to $R = 260$. With both applying, half each,
the bank expects $\bar s R - (1 - \bar s) \times 60$ with $\bar s = 0.7$: $0.7R - 18$, which reaches $106.44$ at
$R = 177.78$. Just above, only the risky apply: $0.5R - 30 = 58.9$. That rises with $R$ but only to $0.5 \times 260 -
30 = 100$ at the risky borrowers' limit. So the bank's best rate is just under $177.78$, and at that rate it turns
away applicants rather than raise the rate.

## Where it comes back

| Idea | Parts |
|---|---|
| Hidden action, contracts and incentives | 14 *Incentives* |
| Auctions with private values | 16 *Auctions*, 17 *Markets by Design* |
| Banks, runs and credit | 26 *Banks and Runs* |
| Social insurance and its design | 42 *Social Insurance* |
| Behaviour: inertia, overconfidence, signalling as waste | 45 *Behavioural Economics* |
| Microcredit and group lending | 46 *Development* |
| Information design | 53 *Information and Persuasion* |
| Reputation and trust on platforms | 61 *Economics at the Platforms* |

## Sources

- George A. Akerlof, "The Market for 'Lemons': Quality Uncertainty and the Market Mechanism", *Quarterly Journal of
  Economics* 84(3) (1970): 488-500; "Writing 'The Market for Lemons': A Personal and Interpretive Essay" (Nobel
  Foundation, 2003), as excerpted.
- Michael Spence, "Job Market Signaling", *Quarterly Journal of Economics* 87(3) (1973): 355-374; John G. Riley,
  "Informational Equilibrium", *Econometrica* 47(2) (1979): 331-359; In-Koo Cho and David M. Kreps, "Signaling Games
  and Stable Equilibria", *Quarterly Journal of Economics* 102(2) (1987): 179-221.
- Michael Rothschild and Joseph Stiglitz, "Equilibrium in Competitive Insurance Markets", *Quarterly Journal of
  Economics* 90(4) (1976): 629-649; Joseph Stiglitz and Andrew Weiss, "Credit Rationing in Markets with Imperfect
  Information", *American Economic Review* 71(3) (1981): 393-410.
- Gary Becker, *Human Capital* (1964); Jacob Mincer, *Schooling, Experience, and Earnings* (1974); Thomas Hungerford
  and Gary Solon, "Sheepskin Effects in the Returns to Education", *Review of Economics and Statistics* 69(1) (1987):
  175-177; John H. Tyler, Richard J. Murnane and John B. Willett, "Estimating the Labor Market Signaling Value of the
  GED", *Quarterly Journal of Economics* 115(2) (2000): 431-468; Joshua Angrist and Alan Krueger, *Quarterly Journal
  of Economics* 106(4) (1991): 979-1014; Bryan Caplan, *The Case against Education* (2018).
- David M. Cutler and Richard J. Zeckhauser, "Adverse Selection in Health Insurance", *Frontiers in Health Policy
  Research* 1 (1998): 1-31; David M. Cutler and Sarah J. Reber, "Paying for Health Insurance: The Trade-Off between
  Competition and Adverse Selection", *Quarterly Journal of Economics* 113(2) (1998): 433-466.
- Liran Einav, Amy Finkelstein and Mark R. Cullen, "Estimating Welfare in Insurance Markets Using Variation in
  Prices", *Quarterly Journal of Economics* 125(3) (2010): 877-921 (NBER Working Paper 14414, 2008, read for the
  numbers); Liran Einav and Amy Finkelstein, "Selection in Insurance Markets: Theory and Empirics in Pictures",
  *Journal of Economic Perspectives* 25(1) (2011): 115-138.
- Pierre-André Chiappori and Bernard Salanié, "Testing for Asymmetric Information in Insurance Markets", *Journal of
  Political Economy* 108(1) (2000): 56-78; Amy Finkelstein and Kathleen McGarry, "Multiple Dimensions of Private
  Information: Evidence from the Long-Term Care Insurance Market", *American Economic Review* 96(4) (2006): 938-958;
  Amy Finkelstein and James Poterba, "Adverse Selection in Insurance Markets: Policyholder Evidence from the U.K.
  Annuity Market", *Journal of Political Economy* 112(1) (2004): 183-208.
- Martin B. Hackmann, Jonathan T. Kolstad and Amanda E. Kowalski, "Adverse Selection and an Individual Mandate: When
  Theory Meets Practice", *American Economic Review* 105(3) (2015): 1030-1066; Benjamin R. Handel, "Adverse Selection
  and Inertia in Health Insurance Markets: When Nudging Hurts", *American Economic Review* 103(7) (2013): 2643-2682;
  Liran Einav, Amy Finkelstein, Stephen Ryan, Paul Schrimpf and Mark R. Cullen, "Selection on Moral Hazard in Health
  Insurance", *American Economic Review* 103(1) (2013): 178-219.
- Luís Cabral and Ali Hortaçsu, "The Dynamics of Seller Reputation: Evidence from eBay", *Journal of Industrial
  Economics* 58(1) (2010): 54-78.
- *Association Belge des Consommateurs Test-Achats*, C-236/09, Court of Justice of the European Union (1 March 2011);
  the Genetic Information Nondiscrimination Act, Pub. L. 110-233 (2008).
- Textbooks: Patrick Bolton and Mathias Dewatripont, *Contract Theory* (2005); Andreu Mas-Colell, Michael Whinston
  and Jerry Green, *Microeconomic Theory* (1995), ch. 13; Jean-Jacques Laffont and David Martimort, *The Theory of
  Incentives* (2002); Bernard Salanié, *The Economics of Contracts*; Liran Einav, Amy Finkelstein and Ray Fisman,
  *Risky Business* (2023).
