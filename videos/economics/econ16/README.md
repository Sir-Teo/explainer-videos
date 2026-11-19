# Economics, Built: Part 16, Auctions

Part 16 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth of Act IV, *Failure and Design*. It asks how something should be sold when
nobody knows what it is worth to the buyers, and answers: let the bidders compete, and design the sale around who they
are. When each bidder knows its own value and nothing of the others', any of the standard formats raises the same
money, and a reserve price adds a little. What really matters is getting bidders to come and stopping them from
colluding, protecting winners from the curse of shared values, and choosing rules that bidders can trust and follow.

It opens in London in the spring of 2000, when Britain sold five licences for third-generation mobile spectrum in an
auction designed by game theorists: thirteen bidders, 150 rounds, £22.5 billion. That summer the Netherlands copied the
design with five licences for five incumbents, and raised less than a third of its forecast. From there it covers:

- a game: two sealed bids for Crusoe's canoe, one paying your bid and one paying the next;
- the four standard formats on one draw of values: the English and Dutch clocks, and why the four are two games;
- Vickrey (1961): bidding your value is dominant in a second-price auction, by two cases; Goethe's sealed offer of 1797,
  and why Vickrey's auction is rare (Rothkopf, Teisberg and Kahn 1990);
- shading in a first-price auction, derived: $\tfrac{n-1}{n}v$, and the bid as the expected second value;
- revenue equivalence: five formats on the same 60,000 draws; the spread of the price; the envelope argument (Vickrey
  1961; Myerson 1981; Riley and Samuelson 1981);
- when equivalence fails: risk aversion, the laboratory (Cox, Smith and Walker 1988; Kagel, Harstad and Levin 1987),
  linked values (Milgrom and Weber 1982), asymmetry (Maskin and Riley 2000), collusion and entry;
- an intermission without narration: the 3-month Treasury bill rate, 1934-2025;
- Myerson's reserve price (1981): virtual values, the optimal reserve, Bulow and Klemperer's extra bidder (1996), and
  an is/ought card on reserves for public sales;
- the winner's curse: the Gulf of Mexico's oil leases (Capen, Clapp and Campbell 1971), Agora's estimates, and the jar
  of coins (Bazerman and Samuelson 1983);
- selling the airwaves: the simultaneous ascending auction (Milgrom, Wilson and McAfee, 1994), the exposure problem and
  package bidding, and Britain's design (Binmore and Klemperer 2002);
- what went wrong: trailing digits (Cramton and Schwartz 2000), Germany's two-round auction of 1999, the Dutch and Swiss
  sales of 2000 (Klemperer 2002), with *Called it?* on the Dutch forecast, and the Anglo-Dutch design;
- the auction behind every search: the generalized second price, why it is not Vickrey's, and its equilibrium at
  Vickrey's prices (Edelman, Ostrovsky and Schwarz 2007; Varian 2007);
- many units: the Treasury's move to a single price (Friedman 1960; Garbade and Ingber 2005), demand reduction, and
  electricity markets;
- a new dial (what a reserve adds: Ostrovsky and Schwarz's field experiment); auction desks, and values read from
  bids (Guerre, Perrigne and Vuong 2000); and a frontier chapter on the incentive auction (Milgrom and Segal 2020),
  credible auctions (Akbarpour and Li 2020) and machines that bid.

## Build it

```bash
python -m videos.economics.econ16.compute              # every number (seconds), into .cache/econ16/
python tools/qa_scene.py econ16 Equivalence            # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ16 -q l   # the whole part, silent preview
python tools/build.py econ16                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 16                     # the lab
```

The data are frozen extracts in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): the 3-month Treasury bill rate from FRED; and transcribed
accounts of Britain's 3G auction (Binmore and Klemperer 2002), the European auctions of 2000 (Klemperer 2002), the jar
of coins (Bazerman and Samuelson 1983), signalling in spectrum auctions (Cramton and Schwartz 2000; Klemperer 2002),
reserve prices at Yahoo! (Ostrovsky and Schwarz 2009), the Treasury's change of format (Garbade and Ingber 2005) and
the FCC's incentive auction (2017), in `explainer/economics/data/tables.py` with where they were read and the date they
were checked.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | How should something be sold when nobody knows what it is worth? | Britain's 3G auction, 6 March to 27 April 2000: 13 bidders, 5 licences (one kept for a newcomer), 150 rounds, £22.5 billion, about 2.5% of national income, five to ten times the newspapers' estimates; euros raised per person across Europe: Britain 650, Germany 615, Italy 240, the Netherlands 170, Austria 100, Switzerland 20; auctions everywhere; the question; objectives |
| 1 | Play it: two sealed bids | You value Crusoe's canoe at 70; three rivals' values uniform on 0-100. Sale A pays your bid, sale B the second bid. Against equilibrium rivals, your expected profit peaks at a bid of 52.5 in A and 70 in B, at 6.0 shells in both, winning 34% of the time; near-misses cost little (45 expects 5.4, 60 expects 5.1); bidding 70 in A expects nothing |
| 2 | Four formats, two games | English, Dutch, first-price and second-price sealed; one sale on each clock (Ana 31, Bo 84, Dara 57, Friday 72): the English clock stops at 72, the second value; the Dutch clock at Bo's planned 63; Dutch = first-price exactly; English ≈ second-price with private values |
| 3 | Vickrey: bid your value | Vickrey (1961) and his Nobel (1996); the proof by two cases on the highest rival bid; Goethe's sealed offer of 1797, met exactly by the publisher's; why Vickrey's auction is rare: trust in the seller, and revealing values (Rothkopf, Teisberg and Kahn 1990) |
| 4 | Shading in a first-price auction | The derivation: $\pi(b) = (v - b)(b/c)^{n-1}$, so $b = \tfrac{n-1}{n}v$ whatever the rivals' slope; bids for 2, 3, 4 and 10 bidders; $\beta(v) = \mathbb{E}[Y \mid Y < v]$: bid what you'd expect to pay in a second-price auction if you won |
| 5 | Revenue equivalence | 60,000 auctions of four bidders through five formats: first-price and Dutch 0.600, second-price and English 0.601, all-pay 0.602, against $\tfrac{n-1}{n+1} = 0.6$; the price's spread, 0.12 against 0.20; the envelope argument: $U' = P$, so $T(v) = vP(v) - \int_0^v P$; Play it's six shells as $v^n/n$ |
| 6 | When equivalence fails | Risk-averse bidders ($u = x^{1/2}$) bid $\tfrac67 v$: first-price revenue 0.686 against 0.600; the laboratory: overbidding in first-price auctions, and above value in sealed second-price ones, but not on the English clock; a table of failures: risk, linked values (Milgrom and Weber), asymmetry (Maskin and Riley), collusion, entry |
| | Intermission: ninety years of the Treasury bill | No narration: the 3-month bill rate, yearly averages 1934-2025: held at 3/8% in 1942-47, 16.3% in May 1981 (14.0% for the year), near zero in 2009-15, five percent again in 2023; the rate as a tune; the story so far |
| 7 | Myerson: the reserve price | Virtual values $\varphi(v) = v - (1 - F)/f = 2v - 1$; revenue is the winner's expected virtual value; the reserve of one half; with two bidders, revenue rises from 1/3 to 5/12 (25%), while a third bidder with no reserve gives 1/2 (Bulow and Klemperer 1996); no sale a quarter of the time; is/ought on reserves in public sales |
| 8 | The winner's curse | Capen, Clapp and Campbell (1971) on the Gulf of Mexico's leases; estimates within 3 of a value of 10: the winner's overestimate 1.0, 1.8, 2.33, 2.65 and 2.82 with 2 to 32 bidders, $3\tfrac{n-1}{n+1}$; the Fact, with the jar of coins: jars of $8, average estimate $5.13, average winning bid $10.01, average loss $2.01 over 48 auctions; the cure, and the linkage principle |
| 9 | Selling the airwaves | Hearings and lotteries; Coase (1959); auctions from 1994; the simultaneous ascending auction and its activity rule (Milgrom, Wilson and McAfee; the 2020 Nobel); the exposure problem with Bo's two fishing rights (pair 10, either alone 1): locals at 4 and 4, bold Bo wins both for 8; at 2 and 9, bold Bo loses 1; package bids; Britain's fifth licence for a newcomer, Vodafone's £6 billion, and sunk prices |
| 10 | What went wrong | US West's bid of $313,378 for Waterloo, pointing at Rochester's licence 378 (Cramton and Schwartz 2000); Germany 1999: 18.18 and 20 million DM per MHz, 18.18 × 1.1 ≈ 20, two rounds (Klemperer 2002); the Dutch auction of July 2000 and the Swiss of November; *Called it?*: the Dutch forecast of almost €10 billion against less than €3 billion: wrong; Klemperer's Anglo-Dutch auction |
| 11 | The auction behind every search | GoTo.com's first-price auctions and their sawtooth (1998); Google's generalized second price (2002); the island's notice board, clicks 200, 120, 60 and values 10, 8, 6, 4: truthful bidding gives Ana 400 in slot 1 but 480 in slot 2; Vickrey's prices 6.2, 5 and 4 a click (1,240, 600, 240); the equilibrium at Vickrey's prices (Edelman, Ostrovsky and Schwarz; Varian 2007); quality scores, reserves, first price for display ads |
| 12 | Many units: bonds and electricity | Pay-as-bid bill auctions from 1929; Friedman (1960); the 1992 experiment and single prices for all from October 1998; demand reduction with two bonds (Bo 10 and 10, Dara 6): one price, bidding for two, profit 8 and revenue 12; bidding for one, profit 10 and revenue 0; Vickrey's rule, profit 14, revenue 6, both bonds to Bo; electricity's single price, Britain's 2001 reform, and 2022 |
| 13 | The Dials: what a reserve adds | The new dial: Ostrovsky and Schwarz's experiment on 438,632 Yahoo! keywords against 23,016 controls: revenue +2.7% overall (t = 4.7), -2.2% on keywords searched under ten times a day, +3.3% on the rest; one fewer ad per page; depends on the setting |
| 14 | In practice: auction desks | Where auction economists work; reading values from bids, $v = b + G(b)/((n-1)g(b))$ (Guerre, Perrigne and Vuong 2000); simulation, laboratory testbeds (Plott 1997), rules, and screens for collusion (Porter and Zona 1993) |
| 15 | Frontier: new auctions, new bidders | The FCC's incentive auction (2017): $10.05 billion to 175 stations, $19.8 billion from carriers, 84 MHz; obviously strategy-proof clocks (Milgrom and Segal 2020); credible auctions (Akbarpour and Li 2020) and display ads' move to first price (2019); bidders that are machines, and a guarantee of half the best value (Aggarwal, Badanidiyuru and Mehta 2019); learning reserves; open questions |
| | Recap, problems, and the road ahead | The answer; twelve lines; problems; reading; hospitals and interns, and Part 17 |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's auction house (`explainer.economics.agora.auctions`), with
the Island's Part 16 truths in `explainer.economics.island`, or from the Data Room or a transcribed table; the narration
states the cached numbers.

- **Private values.** The equilibrium bids in closed form (risk neutral, with a reserve, and with constant relative risk
  aversion); five formats run on the same 60,000 draws of four values (seed 1961), with standard errors; the bidder's
  expected profit against every bid in Play it; one sale on the English and Dutch clocks.
- **Reserves.** Revenue against the reserve by the virtual-value formula, for two and three bidders.
- **Common values.** The winner's overestimate for 2 to 32 bidders, simulated on 40,000 tracts each (seed 1971) and in
  closed form.
- **Design.** The exposure problem's cautious and bold outcomes; Vickrey's prices for slots and the generalized second
  price's deviation payoffs; uniform-price, demand-reduced and Vickrey outcomes for two bonds.
- **Data.** FRED's 3-month bill rate; the transcribed auction accounts, experiment and estimates.

## Problems and solutions

**1.** *Vickrey: show that bidding your value is weakly dominant in a second-price auction, and give a case where it is
not strictly better than some other bid.*

*Solution.* Let $m$ be the highest rival bid. Bidding $v$ wins exactly when $m < v$ and pays $m$, so it earns $\max(v -
m, 0)$, the most any bid can earn against $m$, since the price never depends on your own bid. A bid $b > v$ differs only
when $v < m < b$, where it wins at a loss; a bid $b < v$ differs only when $b < m < v$, where it gives up a profit. So
no bid ever does better than $v$. It is not strictly better: if every rival bids 0, any positive bid wins and pays 0,
exactly as bidding $v$ does.

**2.** *Shading: with $n$ bidders and values uniform on $[0, 1]$, verify that $b(v) = \tfrac{n-1}{n}v$ is an
equilibrium of the first-price auction, and that revenue is $\tfrac{n-1}{n+1}$.*

*Solution.* If the rivals bid $\tfrac{n-1}{n}w$, a bid $b \le \tfrac{n-1}{n}$ beats one of them with probability $nb/(n
- 1)$, so expected profit is $(v - b)(nb/(n-1))^{n-1}$. Its derivative vanishes where $(n - 1)(v - b) = b$, at $b =
\tfrac{n-1}{n}v$, and no bid above $\tfrac{n-1}{n}$ helps, since it already wins for sure. The winner has the highest
value, whose mean is $\tfrac{n}{n+1}$, so revenue is $\tfrac{n-1}{n}\cdot\tfrac{n}{n+1} = \tfrac{n-1}{n+1}$.

**3.** *All-pay: use the envelope formula to derive the all-pay equilibrium bid $\tfrac{n-1}{n}v^n$, and check its
revenue.*

*Solution.* The highest value wins, so $P(v) = v^{n-1}$, and the lowest type gets $U(0) = 0$. The envelope formula gives
the expected payment $T(v) = vP(v) - \int_0^v s^{n-1}\,ds = v^n - v^n/n = \tfrac{n-1}{n}v^n$. In an all-pay auction every
bidder pays its bid, win or lose, so the bid is $T(v)$. Revenue is $n\,\mathbb{E}[\tfrac{n-1}{n}v^n] = (n - 1)/(n + 1)$,
the same as every other format.

**4.** *Myerson: with two bidders, show revenue with reserve $r$ is $\tfrac13 + r^2 - \tfrac43 r^3$, maximized at $r =
\tfrac12$ with $\tfrac{5}{12}$; compare three bidders with no reserve.*

*Solution.* Revenue is the expected virtual value of the winner, counting only values above $r$:
$2\int_r^1 (2v - 1)\,v\,dv = 2\big[\tfrac23 v^3 - \tfrac12 v^2\big]_r^1 = \tfrac13 + r^2 - \tfrac43 r^3$. Its derivative
$2r - 4r^2$ vanishes at $r = \tfrac12$, where revenue is $\tfrac13 + \tfrac14 - \tfrac16 = \tfrac{5}{12}$, a quarter
more than $\tfrac13$. Three bidders with no reserve give $\tfrac{3-1}{3+1} = \tfrac12 > \tfrac{5}{12}$: an extra bidder
is worth more than the best reserve.

**5.** *The winner's curse: with estimates $V + e$, $e$ uniform on $[-s, s]$, show the highest of $n$ overstates $V$ by
$s\,\tfrac{n-1}{n+1}$ on average.*

*Solution.* Write $e = s(2u - 1)$ with $u$ uniform on $[0, 1]$. The largest of $n$ uniforms has mean $\tfrac{n}{n+1}$,
so the largest error has mean $s(\tfrac{2n}{n+1} - 1) = s\,\tfrac{n-1}{n+1}$. With $s = 3$: 1, 1.8, 2.33, 2.65 and 2.82
for 2, 4, 8, 16 and 32 bidders, which Agora's simulation matches to two decimals.

**6.** *Slots: with values (10, 8, 6, 4) and clicks (200, 120, 60), compute Vickrey's payments, and check that bids of
6.2, 5 and 4 below the top form an equilibrium of the second-price auction for slots.*

*Solution.* The bidder in slot 3 keeps Friday (4) out of 60 clicks: 240. The bidder in slot 2 moves Dara (6) down 60
clicks and keeps Friday out: $60 \times 6 + 240 = 600$. The bidder in slot 1 moves Bo (8) down 80 clicks: $80 \times 8 +
600 = 1{,}240$. Per click: 6.2, 5 and 4. With Bo bidding 6.2, Dara 5 and Friday 4, and Ana anything higher, each pays
the next bid down, which is Vickrey's price. Ana earns $200 \times 3.8 = 760$ in slot 1, against 600 in slot 2 at 5 or
360 in slot 3 at 4; Bo earns $120 \times 3 = 360$, exactly what slot 1 at 6.2 would give and more than slot 3's 240;
Dara earns $60 \times 2 = 120$, exactly what slot 2 at 5 would give; Friday would earn nothing in slot 3 at 4. Nobody
gains by moving: an equilibrium, the lowest in which nobody envies another's slot.

**7.** *Exposure: with Bo's pair worth 10 and either right 1, find for which local values a bold Bo loses money.*

*Solution.* Let the locals' values be $a \le b$. Bold Bo stays in until the two prices together reach 10. The weaker
local quits at $a$; the other price can rise to $10 - a$. If $b \le 10 - a$, Bo wins both, earning $10 - a - b \ge 0$.
If $a + b > 10$, Bo stops, holding the right bought at $a$, worth 1 alone: a loss of $a - 1$ whenever $a > 1$. So bold
Bo loses money exactly when $a + b > 10$ and $a > 1$; with $(2, 9)$ the loss is 1.

**8.** *$\bigstar$ Demand reduction: two units, values (10, 10) and 6; show that under one price the big bidder bids for
one unit, and find Vickrey's payments.*

*Solution.* With one price set by the highest losing bid, bidding for both units at 10 leaves Dara's 6 as the losing
bid: Bo pays 6 for each, earning $20 - 12 = 8$. Bidding for one unit leaves no losing bid: Bo and Dara each win one at
a price of 0, and Bo earns 10. So Bo bids for one; the seller gets nothing, and a unit goes to Dara, who values it at 6
rather than 10 (surplus 16 instead of 20). Under Vickrey's rule each winner pays the bids its wins displace: Bo wins
both and displaces Dara's 6, so pays 6 in all and earns 14; bidding for one would earn only 10, so Bo bids for both, and
the units go where they are worth most.

## Where it comes back

| Idea | Parts |
|---|---|
| Mechanism design, matching and bargaining with private information | 17 *Markets by Design*, 53 *Information and Persuasion* |
| Common values and adverse selection | 13 *Lemons and Signals* (back) |
| The reserve as a monopoly price | 10 *The Price Maker* (back) |
| Treasury auctions and the government's debt | 32 *The Treasury* |
| Estimating values from bids | 54 *Estimating Models* |
| Electricity markets and carbon permits | 48 *Environment and Climate* |
| Ad auctions, platforms and auto-bidding | 44 *Dynamics, Platforms and Antitrust*, 61 *Economics at the Platforms* |

## Sources

- William Vickrey, "Counterspeculation, Auctions, and Competitive Sealed Tenders", *Journal of Finance* 16(1) (1961):
  8-37; Roger B. Myerson, "Optimal Auction Design", *Mathematics of Operations Research* 6(1) (1981): 58-73; John G.
  Riley and William F. Samuelson, "Optimal Auctions", *American Economic Review* 71(3) (1981): 381-392; Paul R. Milgrom
  and Robert J. Weber, "A Theory of Auctions and Competitive Bidding", *Econometrica* 50(5) (1982): 1089-1122.
- Benny Moldovanu and Manfred Tietzel, "Goethe's Second-Price Auction", *Journal of Political Economy* 106(4) (1998):
  854-859; Michael H. Rothkopf, Thomas J. Teisberg and Edward P. Kahn, "Why Are Vickrey Auctions Rare?", *Journal of
  Political Economy* 98(1) (1990): 94-109.
- James C. Cox, Vernon L. Smith and James M. Walker, "Theory and Individual Behavior of First-Price Auctions", *Journal
  of Risk and Uncertainty* 1(1) (1988): 61-99; John H. Kagel, Ronald M. Harstad and Dan Levin, "Information Impact and
  Allocation Rules in Auctions with Affiliated Private Values: A Laboratory Study", *Econometrica* 55(6) (1987):
  1275-1304; John H. Kagel and Dan Levin, "Independent Private Value Auctions: Bidder Behaviour in First-, Second- and
  Third-Price Auctions with Varying Numbers of Bidders", *Economic Journal* 103(419) (1993): 868-879; John H. Kagel and
  Dan Levin, *Common Value Auctions and the Winner's Curse* (2002).
- Eric Maskin and John Riley, "Asymmetric Auctions", *Review of Economic Studies* 67(3) (2000): 413-438; Jeremy Bulow
  and Paul Klemperer, "Auctions versus Negotiations", *American Economic Review* 86(1) (1996): 180-194.
- E. C. Capen, R. V. Clapp and W. M. Campbell, "Competitive Bidding in High-Risk Situations", *Journal of Petroleum
  Technology* 23 (1971): 641-653; Max H. Bazerman and William F. Samuelson, "I Won the Auction But Don't Want the
  Prize", *Journal of Conflict Resolution* 27(4) (1983): 618-634.
- R. H. Coase, "The Federal Communications Commission", *Journal of Law and Economics* 2 (1959): 1-40; John McMillan,
  "Selling Spectrum Rights", *Journal of Economic Perspectives* 8(3) (1994): 145-162; Paul Milgrom, *Putting Auction
  Theory to Work* (2004); Ken Binmore and Paul Klemperer, "The Biggest Auction Ever: the Sale of the British 3G Telecom
  Licences", *Economic Journal* 112(478) (2002): C74-C96.
- Peter Cramton and Jesse A. Schwartz, "Collusive Bidding: Lessons from the FCC Spectrum Auctions", *Journal of
  Regulatory Economics* 17(3) (2000): 229-252; Paul Klemperer, "What Really Matters in Auction Design", *Journal of
  Economic Perspectives* 16(1) (2002): 169-189; Paul Klemperer, "How (Not) to Run Auctions: the European 3G Telecom
  Auctions", *European Economic Review* 46(4-5) (2002): 829-845; Paul Klemperer, "Auctions with Almost Common Values",
  *European Economic Review* 42 (1998): 757-769.
- Benjamin Edelman, Michael Ostrovsky and Michael Schwarz, "Internet Advertising and the Generalized Second-Price
  Auction", *American Economic Review* 97(1) (2007): 242-259; Hal R. Varian, "Position Auctions", *International
  Journal of Industrial Organization* 25(6) (2007): 1163-1178; Michael Ostrovsky and Michael Schwarz, "Reserve Prices
  in Internet Advertising Auctions: A Field Experiment", working paper (2009).
- Milton Friedman, *A Program for Monetary Stability* (1960); Kenneth D. Garbade and Jeffrey F. Ingber, "The Treasury
  Auction Process: Objectives, Structure, and Recent Adaptations", Federal Reserve Bank of New York, *Current Issues in
  Economics and Finance* 11(2) (2005); Lawrence M. Ausubel and Peter Cramton, "Demand Reduction and Inefficiency in
  Multi-Unit Auctions", working paper (2002).
- Emmanuel Guerre, Isabelle Perrigne and Quang Vuong, "Optimal Nonparametric Estimation of First-Price Auctions",
  *Econometrica* 68(3) (2000): 525-574; Robert H. Porter and J. Douglas Zona, "Detection of Bid Rigging in Procurement
  Auctions", *Journal of Political Economy* 101(3) (1993): 518-538; Charles R. Plott, "Laboratory Experimental
  Testbeds: Application to the PCS Auction", *Journal of Economics and Management Strategy* 6(3) (1997): 605-638.
- Paul Milgrom and Ilya Segal, "Clock Auctions and Radio Spectrum Reallocation", *Journal of Political Economy* 128(1)
  (2020): 1-31; Mohammad Akbarpour and Shengwu Li, "Credible Auctions: A Trilemma", *Econometrica* 88(2) (2020):
  425-467; Gagan Aggarwal, Ashwinkumar Badanidiyuru and Aranyak Mehta, "Autobidding with Constraints", *Web and Internet
  Economics* (WINE 2019); Kareem Amin, Afshin Rostamizadeh and Umar Syed, "Learning Prices for Repeated Auctions with
  Strategic Buyers", *NeurIPS* (2013); Federal Communications Commission, Auction 1000 (2017).
- Board of Governors of the Federal Reserve System, 3-Month Treasury Bill Secondary Market Rate (TB3MS), via FRED.
- Textbooks: Vijay Krishna, *Auction Theory* (2nd ed., 2010); Paul Klemperer, *Auctions: Theory and Practice* (2004);
  Paul Milgrom, *Putting Auction Theory to Work* (2004); Andreu Mas-Colell, Michael Whinston and Jerry Green,
  *Microeconomic Theory* (1995), ch. 23.
