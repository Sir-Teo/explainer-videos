# Economics, Built: Part 12, Competition among the Few

Part 12 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth and last of Act III, *Markets*. It asks how a handful of firms compete,
and when they stop, and answers: somewhere between monopoly and perfect competition, and where depends on what they
commit to. Quantities, capacity and being different keep prices above cost; pure price competition drives them to
cost with only two firms. They stop competing when the future is worth more than one season's cheating, when they
can see each other's prices, and when no newcomer, and no prosecutor, arrives.

It opens in Decatur, Illinois, where in 1989 Archer Daniels Midland committed $150 million to the world's largest
lysine plant. When it opened in 1991 a price war took the American price of lysine, an amino acid added to animal
feed, from $1.30 a pound in 1990 to 64 cents in July 1992, below ADM's own cost of 65 to 70 cents. In June 1992 the
"lysine association" met for the first time in Mexico City; from November 1992 the head of ADM's lysine division,
Mark Whitacre, worked for the FBI, and prices climbed to 98 cents, then $1.08 to $1.13, then about $1.20 (Connor
1998). On a tape played at the trial, ADM's president described a company slogan: "Our competitors are our friends.
Our customers are the enemy." In 1996 ADM was fined $100 million, $70 million of it for lysine, then a record. From
there it covers:

- a game: undercut Crusoe's $40 repair price, then imagine twenty yards;
- Cournot's quantities (1838): best replies, the path to equilibrium, the price with $N$ firms;
- Bertrand's prices (1883): the undercutting spiral, the paradox, unequal costs;
- the escapes: Edgeworth's capacity and his cycles (Maskin and Tirole 1988), Kreps and Scheinkman (1983),
  differentiated prices, and repetition;
- Hotelling's line (1929) and its minimum differentiation, d'Aspremont, Gabszewicz and Thisse (1979), and Salop's
  circle (1979) with excess entry;
- monopolistic competition: Chamberlin and Robinson (1933), Dixit and Stiglitz (1977), and the gains from variety
  that Krugman (1979) used for trade;
- an intermission without narration: crude oil and the pump price of gasoline, 1986-2026, in October 2026 dollars;
- commitment: von Stackelberg (1934), Dixit's capacity (1980) and its three regimes (Bain 1956), and Fudenberg and
  Tirole's animals (1984);
- collusion as a repeated game: grim trigger's thresholds for Cournot and Bertrand with $N$ firms (Friedman 1971),
  Stigler's policing (1964) and *Called it?*: secret price cuts as what breaks cartels;
- cartels in the data: the Joint Executive Committee (Porter 1983), Green and Porter's price wars (1984) simulated,
  the lysine overcharge, and leniency (the US policy of 1993);
- tacit collusion and the law: the Sherman Act, *Twombly* (2007), *Wood Pulp* (1993), price-matching promises, the
  airline fare-database case (1992-94), and rockets and feathers tested on monthly data;
- concentration: the Herfindahl index, Cowling and Waterson's $L = H/\varepsilon$ (1976), and the merger guidelines'
  thresholds (2010, 2023);
- mergers: the merger paradox (Salant, Switzer and Reynolds 1983), Farrell and Shapiro's needed savings (1990),
  Deneckere and Davidson (1985), Williamson's trade-off (1968);
- contestable markets (Baumol, Panzar and Willig 1982), limit pricing (Milgrom and Roberts 1982) and predation (McGee
  1958; Kreps and Wilson 1982; *Brooke Group* 1993);
- a new dial (cartel overcharges) with the sentencing guidelines' 10 percent; antitrust in practice (the hypothetical
  monopolist and critical loss; *FTC v. Staples*, 1997); and a frontier chapter on common ownership and pricing
  algorithms.

## Build it

```bash
python -m videos.economics.econ12.compute              # every number (seconds), into .cache/econ12/
python tools/qa_scene.py econ12 Cournot                # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ12 -q l   # the whole part, silent preview
python tools/build.py econ12                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 12                     # the lab
```

The data are frozen extracts in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): the BLS average price of regular unleaded gasoline
(APU000074714), the EIA's West Texas Intermediate crude price (MCOILWTICO) and the CPI-U (CPIAUCNS), all via FRED;
and transcribed passages from Connor (1998) on lysine, Connor (2014) and Boyer and Kotchoni (2015) on overcharges, and
the 2010 and 2023 merger guidelines, in `explainer/economics/data/tables.py` with where they were read and the date
they were checked.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | How do a handful of firms compete, and when do they stop? | ADM's lysine plant (1989, $150 million); the price war, $1.30 (1990) to 64 cents (July 1992), below ADM's cost of 65-70 cents; Mexico City, June 1992; Whitacre and the FBI, November 1992 to June 1995; prices of 98 cents, $1.08-1.13, about $1.20; the raid; the slogan; the $100 million fine; Connor's 12-28%; markets of a few (airlines, phones, chips, cloud, groceries, fuel); the question; objectives |
| 1 | Play it: name your price | Repairs cost $10; demand $100 - p$; Crusoe posts $40; your choices $45, $40, $39, $25, $10 earn 0, 900, 1,769, 1,125 and 0; one dollar under nearly doubles the split; with twenty yards at $40 matching earns about $86 and undercutting still $1,769 |
| 2 | Cournot: competing in quantities | Cournot (1838), the mineral springs; best replies $q_C = (90 - q_D)/2$; from Crusoe alone at 45 the replies close in on 30 each, price $40, $900 each; the monopoly's 45 boats at $55 ($2,025, or $1,012.50 each): a prisoner's dilemma; $P = (a + Nc)/(N + 1)$: $55, $40, $32.50 ... $14.29 with twenty |
| 3 | Bertrand's reply: competing in prices | Bertrand (1883); the spiral from $40 down to the $10 cost; the paradox; with costs $10 and $20 the efficient yard prices at $19.99 and earns about $799; Cournot or Bertrand: what firms can't easily change |
| 4 | Resolving the paradox: capacity, difference, repetition | Edgeworth (1897) and cycles in some cities' petrol prices (Maskin and Tirole 1988); Kreps and Scheinkman (1983): 30 slips each, price $40, Agora checks every higher price; differentiated boats $q_C = 90 - 2p_C + p_D$: equilibrium $36.67 and $1,422 each against the joint $50; repetition |
| 5 | Hotelling's line and Salop's circle | Ana and Bo on a beach at fixed prices drift to the middle (a quarter of the beach walked on average, against an eighth); Hotelling's "excessive sameness" and his two parties; Downs (1957); with prices, d'Aspremont, Gabszewicz and Thisse (1979): to the ends, price $c + t$; Salop (1979): free entry 10 stalls, the planner 5 |
| 6 | Monopolistic competition | Chamberlin and Robinson (1933): the tangency, zero profit with price above marginal cost, excess capacity; Dixit and Stiglitz (1977): markup $\sigma/(\sigma - 1)$, size $(\sigma - 1)f/c$, varieties $L/(\sigma f)$: 4/3, 3 and 25 on the Island; doubling the economy raises well-being by $2^{1/3} = 1.26$; Krugman (1979) |
| | Intermission: crude and the pump | No narration: WTI crude per gallon and the BLS pump price of regular gasoline, January 1986 to October 2026, in October 2026 dollars (the pump peaked at $6.28 in July 2008); the pump price year by year as a tune; the story so far |
| 7 | Commitment and entry deterrence | Stackelberg (1934): Crusoe leads with 45, Dara follows with 22.5, $1,012.50 and $506.25, price $32.50; Dixit (1980): slips at $30, use at $10, Dara's setup cost $144: credible capacities 20 to 40, deterrence at 36 slips ($864) against accommodation ($450) and the unthreatened monopoly ($900); regimes by setup cost (Bain 1956); Fudenberg and Tirole's top dog, puppy dog, fat cat and lean and hungry look (1984) |
| 8 | Collusion as a repeated game | The yards' deal at 22.5 boats each: $1,012.50 a season against cheating's $1,139.06 once then $900; $\delta \ge 9/17 = 0.529$ (Friedman 1971); with $N$ firms: $1 - 1/N$ for prices, 0.529 to 0.752 for quantities; Stigler (1964) and what helps a cartel; Bernheim and Whinston (1990); *Called it?*: partly right (Levenstein and Suslow 2006) |
| 9 | Cartels in the data | The Joint Executive Committee, 1880-86 (Porter 1983); Green and Porter (1984) in Agora: 10 wars in 300 seasons, a fifth of the time at war, each started by a bad demand season; the lysine overcharge: $65-140 million on $495-550 million of sales; leniency: forgive more than 80% and confessing dominates; the US policy of August 1993 |
| 10 | Tacit collusion and the law | The Sherman Act and Article 101; *Bell Atlantic v. Twombly* (2007); *Wood Pulp* (1993); price-matching promises make $55 an equilibrium ($1,012.50 each, a cut to $54 earns $1,012); the airline fare-database case (1992-94); rockets and feathers (Borenstein, Cameron and Gilbert 1997) and Agora's monthly test: 77 cents after a rise, 75 after a fall, a difference of 1 cent with a standard error of 11 |
| 11 | Concentration: the Herfindahl index | $H = \sum s_i^2$: 10,000, 5,000, 2,500, 5,200 and 1,000 for five markets; Cowling and Waterson (1976): $\sum s_i (P - c_i)/P = H/\varepsilon$, six Island markets on the line; the 2023 guidelines (1,800 and 100; 30%) and 2010's (2,500 and 200); two of five merging: 2,000 to 2,800 |
| 12 | Mergers | Two of three Cournot yards merge and lose $112.50 (Salant, Switzer and Reynolds 1983); four of five break even; Farrell and Shapiro (1990): the price stays put only if cost falls by $22.50, more than the whole $10, and even at zero cost it rises from $32.50 to $36.67; Deneckere and Davidson (1985); Williamson (1968): with elasticity 2, a 10% price rise costs a triangle of about 1% of sales |
| 13 | Contestable markets, limit pricing and predation | Baumol, Panzar and Willig (1982): a ferry with a $1,000 fixed cost prices at average cost, $22.98, not $55; airlines; limit pricing and Milgrom and Roberts (1982); McGee on Standard Oil (1958), reputation (Kreps and Wilson 1982), *Brooke Group* (1993) |
| 14 | The Dials: how much do cartels overcharge? | The sentencing guidelines' 10% and the 20% base fine; the new dial: Connor (2014) median 23%, Boyer and Kotchoni (2015) 16.01%, lysine 12-28%: contested |
| 15 | In practice: the economics of antitrust | The hypothetical monopolist and critical loss: 6.25% against an actual 3.3% at $40; Katz and Shapiro (2003); *FTC v. Staples* (1997); the economist's kit; pointers to Parts 43, 44 and 59 |
| 16 | Frontier: common owners and pricing algorithms | Azar, Schmalz and Tecu (2018) and Dennis, Gerardi and Schenone (2022); O'Brien and Salop's modified HHI: four funds with 7% of each of two airlines give 5,182 if the rest has one owner and 9,871 if it is dispersed; Calvano et al. (2020); Assad et al. (2024); the RealPage case (2024-25) |
| | Recap, problems, and the road ahead | The answer; twelve lines; problems; reading; Akerlof's lemons, and Part 13 |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's oligopoly module (`explainer.economics.agora.oligopoly`),
with the Island's Part 12 truths in `explainer.economics.island`, or from the Data Room or a transcribed table; the
narration states the cached numbers.

- **Quantities and prices.** Cournot with linear demand and any costs in closed form, dropping firms whose output
  would be negative; alternating best replies from the monopoly output; homogeneous Bertrand with a one-cent tick;
  differentiated Bertrand's best replies and equilibrium in closed form; Kreps and Scheinkman's capacities with every
  higher price checked against the residual demand.
- **Space and variety.** Hotelling's drift as alternating best moves at fixed prices; Salop's free-entry and
  cost-minimizing numbers of sellers with the total of entry and walking costs; Dixit and Stiglitz's markup, firm size
  and number of varieties, and well-being per worker as $L^{1/(\sigma - 1)}$.
- **Commitment.** Stackelberg in closed form; Dixit's game solved for every capacity on a grid by iterating the two
  replies (the incumbent's reply at cost $c$, capped at its capacity, never below its reply at $c + r$), the
  deterring capacity from the entrant's zero-profit output $\sqrt{F/b}$, and the regime for each setup cost.
- **Collusion.** Grim-trigger thresholds from the cartel, deviation and Nash profits; Green and Porter's model with
  normal demand shocks (sd 1, seed 1984), a trigger price of 3.5 and wars of six periods; the leniency game's
  expected fines.
- **Concentration and mergers.** HHIs and share-weighted Lerner indexes for six Cournot markets; the merger paradox
  for two of $N$ and $k$ of five; the cost that keeps the price unchanged; Williamson's triangle $\tfrac12 \varepsilon
  \Delta p^2$; a contestable ferry's average-cost price; O'Brien and Salop's MHHI with control proportional to
  holdings.
- **Data.** Rockets and feathers: monthly changes in the pump price regressed on the current and two lagged rises and
  falls of WTI per gallon, with one lag of the dependent variable (1986-2026, 486 months); the intermission's prices
  deflated to October 2026 by the CPI-U.

## Problems and solutions

**1.** *Cournot with $N$ firms: for $P = a - bQ$ and cost $c$, show $P = \frac{a + Nc}{N + 1}$ and each profit
$\frac{(a - c)^2}{b(N + 1)^2}$; check $40 and $14.29.*

*Solution.* Firm $i$ maximizes $(a - bQ - c)q_i$, so $a - bQ - bq_i - c = 0$. In a symmetric equilibrium $Q = Nq$,
so $a - c = b(N + 1)q$ and $q = \frac{a - c}{b(N + 1)}$. Then $P = a - bNq = \frac{a + Nc}{N + 1}$ and profit $(P -
c)q = \frac{a - c}{N + 1} \cdot \frac{a - c}{b(N + 1)}$. With $a = 100$, $b = 1$, $c = 10$: two firms give $120/3 =
40$, twenty give $300/21 = 14.29$.

**2.** *Bertrand with costs $10 and $20: show there is no equilibrium in which the low-cost firm prices above $20,
and find its profit when it prices a cent below.*

*Solution.* If the low-cost firm charged $p > 20$, the high-cost firm could charge just below $p$, still above its
own cost, and take the market at a profit; so the low-cost firm would lose everything, and would rather undercut. The
equilibrium (with prices in cents) has the low-cost firm at $19.99 and the high-cost firm at $20, selling nothing; the
low-cost firm earns $(19.99 - 10)(100 - 19.99) = 9.99 \times 80.01 = 799.30$.

**3.** *Differentiated prices: for $q_i = \alpha - \beta p_i + \gamma p_j$, derive $p = \frac{\alpha + \beta
c}{2\beta - \gamma}$ and check $36.67; find the joint-profit price.*

*Solution.* Firm $i$ maximizes $(p_i - c)(\alpha - \beta p_i + \gamma p_j)$: $\alpha - 2\beta p_i + \gamma p_j +
\beta c = 0$, so $p_i = \frac{\alpha + \beta c + \gamma p_j}{2\beta}$, rising in $p_j$. Setting $p_i = p_j = p$ gives
$p = \frac{\alpha + \beta c}{2\beta - \gamma} = \frac{90 + 20}{3} = 36.67$. Jointly, with a common price, each sells
$\alpha - (\beta - \gamma)p$, so they maximize $(p - c)(\alpha - (\beta - \gamma)p)$: $p = \tfrac12\big(\frac{\alpha}
{\beta - \gamma} + c\big) = \tfrac12(90 + 10) = 50$, earning $40 \times 40 = 1{,}600$ each, against $26.67 \times 53.33
= 1{,}422$.

**4.** *Stackelberg: derive the leader's 45 and the follower's 22.5, and show the leader earns more than in
Cournot.*

*Solution.* The follower replies $q_F = \frac{a - c - bq_L}{2b}$. Substituting, the leader's price is $a - b(q_L +
q_F) = c + \frac{a - c - bq_L}{2}$, so it maximizes $\frac{a - c - bq_L}{2} q_L$: $q_L = \frac{a - c}{2b} = 45$, $q_F
= 22.5$, $P = 32.5$. The leader earns $22.5 \times 45 = 1{,}012.50$, more than Cournot's $900$, because it could
have chosen 30 and did better; the follower earns $22.5^2 = 506.25$.

**5.** *Grim trigger: show the Cournot duopoly needs $\delta \ge \tfrac{9}{17}$, and that Bertrand with $N$ firms
needs $\delta \ge 1 - \tfrac1N$.*

*Solution.* Cooperation is worth $\frac{\pi_c}{1 - \delta}$ and cheating $\pi_d + \frac{\delta \pi_n}{1 - \delta}$,
so cartels hold when $\delta \ge \frac{\pi_d - \pi_c}{\pi_d - \pi_n}$. For the duopoly, with $A = a - c$ and $b = 1$:
$\pi_c = A^2/8$; the best reply to $A/4$ is $3A/8$, at a price $3A/8$ above cost, so $\pi_d = 9A^2/64$; $\pi_n =
A^2/9$. Then $\delta^* = \frac{9/64 - 8/64}{9/64 - 1/9} = \frac{1/64}{17/576} = \frac{9}{17}$. Under Bertrand, $\pi_c
= \pi_m/N$, a cheater undercutting by a cent takes $\pi_m$, and $\pi_n = 0$, so $\delta^* = 1 - \frac1N$.

**6.** *The merger paradox: show that two of three Cournot firms lose $112.50 by merging, and that four of five
exactly break even.*

*Solution.* With $N$ firms each earns $\frac{8{,}100}{(N + 1)^2}$. Three firms earn $506.25$ each; after two merge,
two firms earn $900$ each, so the pair goes from $1{,}012.50$ to $900$: a loss of $112.50$. Five firms earn $225$
each; if four merge, two firms remain at $900$ each, exactly the four's $4 \times 225$.

**7.** *Cowling and Waterson: prove that in Cournot equilibrium the share-weighted Lerner index equals $H /
\varepsilon$.*

*Solution.* Firm $i$'s first-order condition is $P + P'(Q)q_i - c_i = 0$, so $\frac{P - c_i}{P} = -\frac{P'(Q)Q}{P}
\cdot \frac{q_i}{Q} = \frac{s_i}{\varepsilon}$, where $\varepsilon = -\frac{P}{P'(Q)Q}$ is the elasticity of market
demand. Weighting by $s_i$ and summing, $\sum_i s_i \frac{P - c_i}{P} = \frac{\sum_i s_i^2}{\varepsilon} =
\frac{H}{\varepsilon}$. For two equal firms at $P = 40$, $Q = 60$: $\varepsilon = 2/3$ and $H = 0.5$, so the markup
is $0.75 = (40 - 10)/40$.

**8.** ★ *Dixit: with slips at $30 and use at $10, show credible capacities run from 20 to 40, and that 36 deters an
entrant with setup cost $144.*

*Solution.* After entry the entrant's cost is $40$, so its reply is $q_E = \frac{60 - q_I}{2}$. The incumbent's
reply is $\frac{90 - q_E}{2}$ for output it has capacity for, and $\frac{60 - q_E}{2}$ beyond it. With no capacity
the two meet at 20 each (both at cost 40): the point $S$. With unlimited capacity the incumbent's low-cost reply meets
the entrant's at $q_I = 40$, $q_E = 10$: the point $T$. Capacity below 20 is never used to fight, and capacity above
40 would be left idle, so only $k \in [20, 40]$ changes what happens. Against $q_I$ the entrant earns $q_E^2 - F$, so
it stays out once $q_E \le \sqrt{144} = 12$, that is $q_I \ge 60 - 24 = 36$, within the credible range. The
incumbent then earns $(100 - 36 - 40) \times 36 = 864$, against $450$ as a Stackelberg leader at cost 40 (30 and 15
at a price of 55), so deterrence pays; it costs $36$ against the unthreatened monopoly's $(70 - 40) \times 30 = 900$.

## Where it comes back

| Idea | Parts |
|---|---|
| Asymmetric information, signals and screening | 13 *Lemons and Signals*, 14 *Incentives* |
| Auctions, bidding rings and market design | 16 *Auctions*, 17 *Markets by Design* |
| Monopolistic competition in growth, sticky prices and trade | 21 *Growth II*, 30 *Sticky Prices*, 36 *Trade II* |
| Measuring markups and conduct | 43 *Measuring Market Power* |
| Platforms, dynamic competition and antitrust | 44 *Dynamics, Platforms and Antitrust* |
| Party competition | 47 *Political Economy* |
| Damages and the expert witness | 59 *The Expert Witness* |

## Sources

- John M. Connor, "Lysine: A Case Study in International Price-Fixing", *Choices* 13(3) (1998): 13-19; *Global
  Price Fixing* (2nd ed., 2008); "Price-Fixing Overcharges: Revised 3rd Edition" (2014), in *Research in Law and
  Economics* 26: 249-387.
- U.S. Department of Justice, press release on ADM's plea (15 October 1996); "Caught in the Act: Inside an
  International Cartel" (2005); Corporate Leniency Policy (10 August 1993); *U.S. v. Airline Tariff Publishing Co.*,
  Civ. No. 92-2854 (D.D.C.), final judgment (1994); *U.S. v. RealPage* (M.D.N.C., 2024) and the proposed settlement
  (24 November 2025).
- Antoine Augustin Cournot, *Recherches sur les principes mathématiques de la théorie des richesses* (1838), ch. 7;
  Joseph Bertrand, review in the *Journal des Savants* (1883); F. Y. Edgeworth, "La teoria pura del monopolio",
  *Giornale degli Economisti* (1897).
- Harold Hotelling, "Stability in Competition", *Economic Journal* 39(153) (1929): 41-57; C. d'Aspremont, J. J.
  Gabszewicz and J.-F. Thisse, *Econometrica* 47(5) (1979): 1145-1150; Steven Salop, *Bell Journal of Economics*
  10(1) (1979): 141-156; Anthony Downs, *An Economic Theory of Democracy* (1957).
- Edward Chamberlin, *The Theory of Monopolistic Competition* (1933); Joan Robinson, *The Economics of Imperfect
  Competition* (1933); Avinash Dixit and Joseph Stiglitz, *American Economic Review* 67(3) (1977): 297-308; Paul
  Krugman, *Journal of International Economics* 9(4) (1979): 469-479.
- Heinrich von Stackelberg, *Marktform und Gleichgewicht* (1934); Joe Bain, *Barriers to New Competition* (1956);
  Avinash Dixit, *Economic Journal* 90(357) (1980): 95-106; Drew Fudenberg and Jean Tirole, *American Economic
  Review* 74(2) (1984): 361-366; David Kreps and José Scheinkman, *Bell Journal of Economics* 14(2) (1983): 326-337;
  Eric Maskin and Jean Tirole, *Econometrica* 56(3) (1988): 571-599.
- James Friedman, *Review of Economic Studies* 38(1) (1971): 1-12; George Stigler, *Journal of Political Economy*
  72(1) (1964): 44-61; B. Douglas Bernheim and Michael Whinston, *RAND Journal of Economics* 21(1) (1990): 1-26;
  Robert Porter, *Bell Journal of Economics* 14(2) (1983): 301-314; Edward Green and Robert Porter, *Econometrica*
  52(1) (1984): 87-100; Margaret Levenstein and Valerie Suslow, *Journal of Economic Literature* 44(1) (2006): 43-95.
- *Bell Atlantic Corp. v. Twombly*, 550 U.S. 544 (2007); *Ahlström Osakeyhtiö v. Commission* (Wood Pulp), Court of
  Justice (1993); Severin Borenstein, A. Colin Cameron and Richard Gilbert, *Quarterly Journal of Economics* 112(1)
  (1997): 305-339.
- Orris Herfindahl, *Concentration in the Steel Industry* (Columbia dissertation, 1950); Albert Hirschman, *National
  Power and the Structure of Foreign Trade* (1945); Keith Cowling and Michael Waterson, *Economica* 43(171) (1976):
  267-274; U.S. Department of Justice and Federal Trade Commission, *Horizontal Merger Guidelines* (2010) and
  *Merger Guidelines* (2023).
- Stephen Salant, Sheldon Switzer and Robert Reynolds, *Quarterly Journal of Economics* 98(2) (1983): 185-199;
  Joseph Farrell and Carl Shapiro, *American Economic Review* 80(1) (1990): 107-126; Raymond Deneckere and Carl
  Davidson, *RAND Journal of Economics* 16(4) (1985): 473-486; Oliver Williamson, *American Economic Review* 58(1)
  (1968): 18-36.
- William Baumol, John Panzar and Robert Willig, *Contestable Markets and the Theory of Industry Structure* (1982);
  Paul Milgrom and John Roberts, *Econometrica* 50(2) (1982): 443-459 and *Journal of Economic Theory* 27(2) (1982):
  280-312; David Kreps and Robert Wilson, *Journal of Economic Theory* 27(2) (1982): 253-279; John McGee, *Journal of
  Law and Economics* 1 (1958): 137-169; *Brooke Group v. Brown & Williamson*, 509 U.S. 209 (1993).
- U.S. Sentencing Commission, *Guidelines Manual*, §2R1.1 and its commentary; Marcel Boyer and Rachidi Kotchoni,
  *Review of Industrial Organization* 47(2) (2015): 119-153; Michael Katz and Carl Shapiro, "Critical Loss: Let's
  Tell the Whole Story", *Antitrust* 17(2) (2003); *FTC v. Staples*, 970 F. Supp. 1066 (D.D.C. 1997).
- José Azar, Martin Schmalz and Isabel Tecu, *Journal of Finance* 73(4) (2018): 1513-1565; Patrick Dennis,
  Kristopher Gerardi and Carola Schenone, *Journal of Finance* 77(5) (2022): 2765-2798; Daniel O'Brien and Steven
  Salop, *Antitrust Law Journal* 67 (2000); Emilio Calvano, Giacomo Calzolari, Vincenzo Denicolò and Sergio
  Pastorello, *American Economic Review* 110(10) (2020): 3267-3297; Stephanie Assad, Robert Clark, Daniel Ershov and
  Lei Xu, *Journal of Political Economy* 132(3) (2024): 723-771.
- Textbooks: Jean Tirole, *The Theory of Industrial Organization* (1988); Luís Cabral, *Introduction to Industrial
  Organization* (2nd ed., 2017); Dennis Carlton and Jeffrey Perloff, *Modern Industrial Organization*; Paul
  Belleflamme and Martin Peitz, *Industrial Organization: Markets and Strategies*; Massimo Motta, *Competition
  Policy* (2004); Michael Whinston, *Lectures on Antitrust Economics* (2006); Kurt Eichenwald, *The Informant*
  (2000).
