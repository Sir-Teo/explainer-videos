# Economics, Built: Part 15, Spillovers

Part 15 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third of Act IV, *Failure and Design*. It asks what happens when my choice lands on
you and nobody pays, and answers: the market makes too much of what harms others and too little of what helps them,
because no price carries the spillover. Where the people involved are few and contracts cheap, they bargain it away,
as the beekeepers did. Where they are many, the remedy is a price on the spillover, a cap with permits to trade, or
rules made by the users; each works only as well as the damage is measured and the rules are kept.

It opens with James Meade's example of 1952: an orchard and a beekeeper, neither paying the other, the textbook's
picture of a benefit no market could price. In 1972 Steven Cheung asked the beekeepers of Washington State what they
were paid, and found that orchards had long paid pollination fees, and that for honey crops the beekeepers paid the
farmers. From there it covers:

- a game: the shared pot, four islanders and twenty shells each;
- the wedge between private and social cost: Bo's kiln and Ana's fish, the market's overproduction and its triangle;
- Pigou's tax (1920): the damage at the margin, the efficient amount of smoke, and subsidies for positive spillovers;
- Coase (1960): his table of the cattle and the corn, bargaining under either liability rule, transaction costs, and
  *Sturges v. Bridgman*;
- the fable of the bees investigated (Cheung 1973): rents per hive in money and in nectar;
- public goods: rival and excludable goods, Samuelson's condition (1954), voluntary provision and Lindahl's prices;
  the lighthouse (Coase 1974) and its critics;
- an intermission without narration: sulphur dioxide emissions in the United States, the United Kingdom, China and
  India, 1900-2022;
- free riding measured: conditional cooperators (Fischbacher, Gächter and Fehr 2001), punishment (Fehr and Gächter
  2000) and antisocial punishment (Herrmann, Thöni and Gächter 2008);
- the commons: Gordon's fishery (1954), Hardin (1968), the northern cod (1992) and Ostrom's design principles (1990);
- permits (Dales 1968; Montgomery 1972) and the acid-rain market (Schmalensee and Stavins 2013), with *Called it?* on
  its forecast benefits;
- prices or quantities (Weitzman 1974), and carbon (Pizer 2002; Roberts and Spence 1976);
- congestion: Vickrey's bottleneck (1969), the toll that halves its cost, and Stockholm's trial (2006);
- networks and lock-in (Rohlfs 1974; Katz and Shapiro 1985; David 1985; Arthur 1989) and knowledge spillovers (Jaffe,
  Trajtenberg and Henderson 1993);
- a new dial (traffic's response to roads: Duranton and Turner 2011); the toolkit in use; and a frontier chapter on
  measuring the damage (Chay and Greenstone 2003; Currie and Walker 2011; Deryugina et al. 2019).

## Build it

```bash
python -m videos.economics.econ15.compute              # every number (seconds), into .cache/econ15/
python tools/qa_scene.py econ15 Coase                  # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ15 -q l   # the whole part, silent preview
python tools/build.py econ15                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 15                     # the lab
```

The data are frozen extracts in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): sulphur dioxide emissions from the Community Emissions
Data System (Hoesly et al. 2024) via Our World in Data; and transcribed passages from Coase (1960), Cheung (1973),
Schmalensee and Stavins (2013), Duranton and Turner (2011) with summaries of the Stockholm evaluation, and Currie and
Walker (2011), in `explainer/economics/data/tables.py` with where they were read and the date they were checked.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | What happens when my choice lands on you, and nobody pays? | Meade's apple farmer who "cannot charge the bee-keeper for the bees' food" (1952); Cheung's 1972 survey of nine beekeepers and about 10,000 hives: pollination fees, apiary rents, and apple blossom that yields little honey; spillovers everywhere; the question; objectives |
| 1 | Play it: the shared pot | Four islanders, 20 shells each, the pot multiplied by 1.6 and shared: each shell given costs 1 and returns 0.4; giving nothing is always best for you; all give, 32 each; none give, 20; a four-player prisoner's dilemma; about half given on a first play |
| 2 | The wedge between private and social cost | Bo's kiln and Ana's fish: demand $100 - Q$, Bo's cost $10 + Q$, damage $0.5Q$; the market makes 45 pots, the best is 36; a triangle of 101.25 shells a season; negative and positive spillovers; three remedies |
| 3 | Pigou's tax | Tax the damage at the margin: 18 a pot, and Bo stops at 36 himself; 648 shells of revenue; the damage left, 324 of 506: the right amount of smoke is not zero; Pigouvian subsidies |
| 4 | Coase: the cattle and the corn | Coase's table (1, 3, 6, 10 tons lost with 1 to 4 steers; a $9 fence); Agora's values for the steers (5, 4, 1.50, -1): the best herd is 2; liable or not, the herd is 2, the farmer paying $1.50 to $3 in the second case; a $2 transaction cost leaves 3 when the rancher isn't liable; the problem is reciprocal; *Sturges v. Bridgman* |
| 5 | The fable of the bees, investigated | Cheung's rents per hive: spring pollination $9.65 = $9.02 in money + $0.64 in nectar; summer honey crops $8.07 = $1.30 + $6.77; money and nectar correlated -0.973 across the spring farms; the market priced the spillover; bargaining costs are the lesson |
| 6 | Public goods, and the lighthouse | Rival and excludable: private, common, club and public goods; four ship-owners valuing light at $\theta_i \ln(1 + G)$, $\theta = (4, 3, 2, 1)$: Samuelson's 9 hours against 3 provided voluntarily; Lindahl's shares 40, 30, 20, 10%; Coase's lighthouse (1974) and its critics |
| | Intermission: a century of sulphur | No narration: SO2 emissions, million tonnes a year, 1900-2022: the United States peaks at 31.1 in 1973 and falls to 2.0; China peaks at 38.1 in 2006 and falls to 10.4; India rises to 11.3; the United Kingdom falls to 0.14; the US line as a tune; the story so far |
| 7 | Free riding measured | About half given at first; conditional cooperators and free riders (Fischbacher, Gächter and Fehr 2001); Agora's typed players over ten rounds: decay to about a sixth without punishment, a rise to over half with it; Fehr and Gächter (2000); antisocial punishment in sixteen cities (Herrmann, Thöni and Gächter 2008) |
| 8 | The commons: Gordon, Hardin and Ostrom | Gordon's fishery with Schaefer's growth: open access at 35 boats with no rent, the best at 17.5 with a rent of 6.1 and 65% of the stock left against 30%, the largest catch at 25; Hardin (1968); the northern cod moratorium of 2 July 1992 and about 30,000 jobs in Newfoundland and Labrador; Törbel since 1483 and Ostrom's design principles; the 2009 Nobel |
| 9 | Permits: the acid-rain market | Dales (1968) and Montgomery (1972); the 1990 amendments: power plants' SO2 from 15.9 to 10.2 million tons by 2004 while coal power rose 25%, 5.1 by 2010; the $2,000 fine; savings of 15-90%; low-sulphur coal by rail; prices of $273, $703, over $1,200, $315 to $115 in a day, $70, and $0.56 by 2012; *Called it?*: benefits about equal to costs (Portney 1990) against $59-116 billion a year for $0.5-2 billion: wrong |
| 10 | Prices or quantities? | Weitzman (1974): expected losses with slopes 0.5 and 2: the tax's 0.0125 against the cap's 0.2, and with the slopes reversed the cap's 0.2 against the tax's 3.2; carbon as a stock favours a price (Pizer 2002); hybrids (Roberts and Spence 1976) |
| 11 | Congestion: the bottleneck and the toll | 6,000 commuters, a causeway carrying 4,000 an hour, costs of 20, 10 and 40 shells an hour in the queue, early and late: a queue peaking at 36 minutes for the 9:00 arrival, half the cost in queueing; Vickrey's toll halves the cost (72,000 to 36,000); Stockholm 2006: about a fifth less traffic, 53% of the city voting to keep it, permanent from 2007 |
| 12 | Networks and ideas | Network externalities (Rohlfs 1974; Katz and Shapiro 1985); Arthur's lock-in (1989), run twelve times; QWERTY disputed (David 1985; Liebowitz and Margolis 1990); ideas as non-rival goods; patent citations that stay near home (Jaffe, Trajtenberg and Henderson 1993); a pointer to Parts 21 and 44 |
| 13 | The Dials: do new roads fill? | The new dial: Duranton and Turner's elasticity of driving to lane kilometres, 0.86 by OLS and 1.03 with historical instruments: new lanes fill; transit doesn't reduce driving either |
| 14 | In practice: regulators, markets and charges | Carbon taxes (Sweden 1991, British Columbia 2008), permit markets (1995, the EU 2005), tradable fishing quotas, spectrum auctions (Coase 1959), road charges (Singapore 1975 to New York 2025), user-run commons, standards; cost-benefit analysis; designing markets and charges; politics |
| 15 | Frontier: measuring the damage | The 1981-82 recession and infant mortality (Chay and Greenstone 2003); the wind and older people's deaths (Deryugina et al. 2019); E-ZPass: premature births down 10.8% and low birth weight 11.8% within 2 km of toll plazas (Currie and Walker 2011); open questions |
| | Recap, problems, and the road ahead | The answer; twelve lines; problems; reading; the British spectrum auction of 2000, and Part 16 |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's spillovers module (`explainer.economics.agora.public`),
with the Island's Part 15 truths in `explainer.economics.island`, or from the Data Room or a transcribed table; the
narration states the cached numbers.

- **Spillovers.** The linear market with a rising marginal damage: market and efficient outputs, the triangle and the
  tax; Coase's table with Agora's values for the steers, the herd under each liability rule, the bargaining range and
  the effect of a transaction cost.
- **Public goods and the pot.** Samuelson's condition, voluntary provision and Lindahl's shares in closed form; the
  shared pot's payoffs; four hundred groups of Agora's typed players (half conditional cooperators, three tenths free
  riders, the rest random), ten rounds, with and without punishment (seed 2000).
- **Commons, caps and queues.** Gordon's fishery with Schaefer's logistic growth; Weitzman's expected losses in closed
  form, checked against 20,000 simulated cost shocks; Vickrey's bottleneck in the form of Arnott, de Palma and Lindsey
  (the queue, its cost and the toll that replaces it); Arthur's lock-in, twelve runs of 800 adopters (seed 1989).
- **Data.** CEDS sulphur dioxide for four countries; the transcribed rents, emissions, prices and estimates.

## Problems and solutions

**1.** *The kiln: with demand $a - bQ$, private cost $c + eQ$ and damage $dQ$, derive the market and efficient
outputs, Pigou's tax and the triangle; check 45, 36, 18 and 101.25.*

*Solution.* The market sets $a - bQ = c + eQ$, so $Q_m = (a - c)/(b + e) = 90/2 = 45$. Counting the damage, $a - bQ = c
+ (e + d)Q$, so $Q^* = (a - c)/(b + e + d) = 90/2.5 = 36$. Pigou's tax is the marginal damage there, $dQ^* = 18$: with
it the market sets $a - bQ = c + eQ + 18$, and $Q = 72/2 = 36$. The triangle runs from $Q^*$ to $Q_m$ between social
cost and demand; at $Q_m$ the gap is $(10 + 1.5 \times 45) - 55 = 22.5$, so its area is $\tfrac12 \times 9 \times 22.5 =
101.25$.

**2.** *Coase: with his table and Agora's values for the steers, show the herd is 2 under either rule, and the farmer
pays between $1.50 and $3.*

*Solution.* The steers are worth 5, 4, 1.50 and -1 to the rancher, and destroy 1, 2, 3 and 4 tons more crop at $1 a
ton (or $9 a year for a fence). The joint value with $k$ steers is the steers' value less the cheaper of the damage
and the fence: 0, 4, 6, 4.50 and 0.50 for $k = 0, \dots, 4$, so the best herd is 2. If the rancher is liable, the
rancher's own profit is that joint value, and the rancher keeps 2. If not, the rancher alone would keep 3 (the value is
largest there, 10.50); the farmer gains $3 by losing the third steer and the rancher loses $1.50, so any payment between
them strikes the bargain, and the herd is 2.

**3.** *The shared pot: show that giving nothing is best for each player when the return per shell $m < 1$, and giving
everything best for the group when $nm > 1$.*

*Solution.* Player $i$ ends with $w - g_i + m\sum_j g_j$; one more shell changes this by $-1 + m < 0$, whatever the
others give, so giving nothing is a dominant strategy. The group ends with $\sum_i (w - g_i) + nm\sum_j g_j$; one more
shell from anyone changes this by $-1 + nm$, positive when $nm > 1$. Here $m = 0.4$ and $n = 4$: each shell costs its
giver 0.6 and is worth 0.6 to the group.

**4.** *Samuelson and Lindahl: for values $\theta_i \ln(1 + G)$ with $\theta = (4, 3, 2, 1)$ and cost 1, find the efficient
$G$, voluntary provision, and Lindahl's prices.*

*Solution.* Samuelson's condition sets the sum of marginal values to the cost: $\sum\theta_i/(1 + G) = 10/(1 + G) = 1$,
so $G^* = 9$. Voluntarily, each gives until their own marginal value $\theta_i/(1 + G)$ falls to 1; the keenest stops at
$G = 3$, where the others' values ($3/4$, $2/4$, $1/4$) are already below the cost, so they give nothing. Lindahl's price
for each is their marginal value at $G^*$: $\theta_i/10 = 0.4, 0.3, 0.2, 0.1$, which sum to the cost, and at those
prices each asks for exactly 9.

**5.** *Gordon's fishery: with Schaefer's growth, derive open-access effort, maximum economic yield and maximum
sustainable yield; check 35, 17.5 and 25.*

*Solution.* With growth $rX(1 - X/K)$ and catch $qEX$, the steady state has $X = K(1 - qE/r)$ and yield $Y = qEK(1 -
qE/r)$. Open access drives the rent $pY - cE$ to zero: $pqK(1 - qE/r) = c$, so $E = (r/q)(1 - c/(pqK)) = 50 \times 0.7
= 35$. The rent is largest where $pqK(1 - 2qE/r) = c$, at half that, $17.5$. The yield is largest where $1 - 2qE/r =
0$, at $E = r/(2q) = 25$.

**6.** *Weitzman: derive the expected losses of a tax and a quota, and show their difference is
$\sigma^2(C'' - B'')/(2C''^2)$.*

*Solution.* Let marginal benefit be $b_0 - B''Q$ and marginal cost $c_0 + \theta + C''Q$. The best $Q$ for each $\theta$
is $Q^*(\theta) = (b_0 - c_0 - \theta)/(B'' + C'')$, and missing it by $\Delta$ costs $\tfrac12(B'' + C'')\Delta^2$. A
quota at the expected optimum misses by $\theta/(B'' + C'')$, an expected loss of $\sigma^2/(2(B'' + C''))$. A tax at the
expected optimum's marginal cost leads firms to $Q = Q^*(0) - \theta/C''$, missing by $\theta B''/(C''(B'' + C''))$: an
expected loss of $\sigma^2B''^2/(2C''^2(B'' + C''))$. Subtracting, the quota's loss less the tax's is
$\sigma^2(C''^2 - B''^2)/(2C''^2(B'' + C'')) = \sigma^2(C'' - B'')/(2C''^2)$.

**7.** *Vickrey's bottleneck: show the equilibrium cost per commuter is $\delta N/s$ with $\delta = \beta\gamma/(\beta +
\gamma)$, and that half of the total is time in the queue.*

*Solution.* In equilibrium every commuter bears the same cost, and the first and last to arrive don't queue. The first
arrives early by $\tau_1$ at cost $\beta\tau_1$, the last late by $\tau_2$ at cost $\gamma\tau_2$; arrivals run at capacity
for $\tau_1 + \tau_2 = N/s$. Equal costs give $\tau_1 = \gamma N/((\beta + \gamma)s)$ and a cost of $\beta\gamma N/((\beta +
\gamma)s) = \delta N/s$, 12 here. The schedule costs of all commuters sum to $s\int(\beta\text{ or }\gamma)u\,du = \delta
N^2/(2s)$, half the total $\delta N^2/s$; the other half is queueing.

**8.** ★ *Arthur's lock-in: show that once one technology leads by more than taste/network adopters, every later adopter
chooses it.*

*Solution.* An adopter who prefers B gains $\text{taste} + \text{network}\cdot n_B$ from B and $\text{network}\cdot n_A$
from A. If $n_A - n_B > \text{taste}/\text{network}$, A is better even for them; an adopter who prefers A chooses it
anyway. So every adopter chooses A, the lead grows, and the condition holds for ever after.

## Where it comes back

| Idea | Parts |
|---|---|
| Auctions and markets designed on purpose | 16 *Auctions*, 17 *Markets by Design* |
| Ideas, growth and knowledge spillovers | 21 *Growth II: Ideas and Institutions* |
| Cities, agglomeration and roads | 37 *Cities and Regions* |
| Taxes and public goods | 41 *Taxes*, 42 *Social Insurance* |
| Platforms and network effects | 44 *Dynamics, Platforms and Antitrust*, 61 *Economics at the Platforms* |
| Collective action and political economy | 47 *Political Economy* |
| Climate, carbon and resources | 48 *Environment and Climate* |
| Cost-benefit analysis | 58 *Scoring the Bill* |

## Sources

- A. C. Pigou, *The Economics of Welfare* (1920); J. E. Meade, "External Economies and Diseconomies in a Competitive
  Situation", *Economic Journal* 62(245) (1952): 54-67.
- R. H. Coase, "The Federal Communications Commission", *Journal of Law and Economics* 2 (1959): 1-40; "The Problem of
  Social Cost", *Journal of Law and Economics* 3 (1960): 1-44; "The Lighthouse in Economics", *Journal of Law and
  Economics* 17(2) (1974): 357-376; David E. Van Zandt, "The Lessons of the Lighthouse", *Journal of Legal Studies*
  22(1) (1993): 47-72; Elodie Bertrand, "The Coasean Analysis of Lighthouse Financing", *Cambridge Journal of Economics*
  30(3) (2006): 389-402.
- Steven N. S. Cheung, "The Fable of the Bees: An Economic Investigation", *Journal of Law and Economics* 16(1) (1973):
  11-33.
- Paul A. Samuelson, "The Pure Theory of Public Expenditure", *Review of Economics and Statistics* 36(4) (1954):
  387-389; Erik Lindahl, *Die Gerechtigkeit der Besteuerung* (1919).
- Gerald Marwell and Ruth Ames, "Experiments on the Provision of Public Goods I", *American Journal of Sociology* 84(6)
  (1979): 1335-1360; John O. Ledyard, "Public Goods: A Survey of Experimental Research", in *The Handbook of
  Experimental Economics* (1995); Ernst Fehr and Simon Gächter, "Cooperation and Punishment in Public Goods
  Experiments", *American Economic Review* 90(4) (2000): 980-994; Urs Fischbacher, Simon Gächter and Ernst Fehr, "Are
  People Conditionally Cooperative?", *Economics Letters* 71(3) (2001): 397-404; Benedikt Herrmann, Christian Thöni and
  Simon Gächter, "Antisocial Punishment across Societies", *Science* 319 (2008): 1362-1367.
- H. Scott Gordon, "The Economic Theory of a Common-Property Resource: The Fishery", *Journal of Political Economy*
  62(2) (1954): 124-142; Garrett Hardin, "The Tragedy of the Commons", *Science* 162 (1968): 1243-1248; Elinor Ostrom,
  *Governing the Commons* (1990); Christopher Costello, Steven D. Gaines and John Lynham, "Can Catch Shares Prevent
  Fisheries Collapse?", *Science* 321 (2008): 1678-1681.
- J. H. Dales, *Pollution, Property and Prices* (1968); W. David Montgomery, "Markets in Licenses and Efficient
  Pollution Control Programs", *Journal of Economic Theory* 5(3) (1972): 395-418; Paul R. Portney, "Economics and the
  Clean Air Act", *Journal of Economic Perspectives* 4(4) (1990): 173-181; Richard Schmalensee and Robert N. Stavins,
  "The SO2 Allowance Trading System: The Ironic History of a Grand Policy Experiment", *Journal of Economic
  Perspectives* 27(1) (2013): 103-122.
- Martin L. Weitzman, "Prices vs. Quantities", *Review of Economic Studies* 41(4) (1974): 477-491; Marc J. Roberts and
  Michael Spence, "Effluent Charges and Licenses under Uncertainty", *Journal of Public Economics* 5 (1976): 193-208;
  William A. Pizer, "Combining Price and Quantity Controls to Mitigate Global Climate Change", *Journal of Public
  Economics* 85(3) (2002): 409-434.
- William S. Vickrey, "Congestion Theory and Transport Investment", *American Economic Review* 59(2) (1969): 251-260;
  Richard Arnott, André de Palma and Robin Lindsey, "Economics of a Bottleneck", *Journal of Urban Economics* 27(1)
  (1990): 111-130; Gilles Duranton and Matthew A. Turner, "The Fundamental Law of Road Congestion", *American Economic
  Review* 101(6) (2011): 2616-2652; Jonas Eliasson et al., "The Stockholm Congestion-Charging Trial 2006: Overview of
  Effects", *Transportation Research Part A* 43(3) (2009): 240-250.
- Jeffrey Rohlfs, "A Theory of Interdependent Demand for a Communications Service", *Bell Journal of Economics* 5(1)
  (1974): 16-37; Michael L. Katz and Carl Shapiro, "Network Externalities, Competition, and Compatibility", *American
  Economic Review* 75(3) (1985): 424-440; Paul A. David, "Clio and the Economics of QWERTY", *American Economic Review*
  75(2) (1985): 332-337; S. J. Liebowitz and Stephen E. Margolis, "The Fable of the Keys", *Journal of Law and
  Economics* 33(1) (1990): 1-25; W. Brian Arthur, "Competing Technologies, Increasing Returns, and Lock-In by Historical
  Events", *Economic Journal* 99(394) (1989): 116-131; Adam B. Jaffe, Manuel Trajtenberg and Rebecca Henderson,
  "Geographic Localization of Knowledge Spillovers as Evidenced by Patent Citations", *Quarterly Journal of Economics*
  108(3) (1993): 577-598.
- Kenneth Y. Chay and Michael Greenstone, "The Impact of Air Pollution on Infant Mortality", *Quarterly Journal of
  Economics* 118(3) (2003): 1121-1167; Janet Currie and Reed Walker, "Traffic Congestion and Infant Health: Evidence
  from E-ZPass", *American Economic Journal: Applied Economics* 3(1) (2011): 65-90; Tatyana Deryugina, Garth Heutel,
  Nolan H. Miller, David Molitor and Julian Reif, "The Mortality and Medical Costs of Air Pollution: Evidence from
  Changes in Wind Direction", *American Economic Review* 109(12) (2019): 4178-4219.
- R. M. Hoesly et al., Community Emissions Data System (CEDS) v_2024_07_08, via Our World in Data.
- Textbooks: Jonathan Gruber, *Public Finance and Public Policy*, chs. 5-9; Andreu Mas-Colell, Michael Whinston and
  Jerry Green, *Microeconomic Theory* (1995), ch. 11; Tom Tietenberg and Lynne Lewis, *Environmental and Natural
  Resource Economics*.
