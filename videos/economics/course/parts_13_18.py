"""Act IV, Failure and Design (Parts 13-18)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=13, level="U", widget="lemons", prereq=(7, 10, 11),
        question="What happens to a market when one side knows more than the other?",
        story="The part opens with George Akerlof's paper on used cars, turned down by the American Economic Review "
              "and the Review of Economic Studies as trivial and by the Journal of Political Economy as wrong, then "
              "printed by the Quarterly Journal of Economics in 1970. The viewer makes a blind offer for Bo's used "
              "boat, then builds Akerlof's market (partial unravelling, and his own example in which nothing trades), "
              "with Called it? on the referees; meets guarantees that are cheap only for honest sellers, reputations "
              "and inspectors; Spence's signals and the intuitive criterion; whether school is a signal (the GED); and "
              "Rothschild and Stiglitz's screening, which may have no equilibrium. After an intermission of used and "
              "new car prices, the death of Harvard's generous health plan in 1995-97, the Einav-Finkelstein diagram "
              "rebuilt from Alcoa's estimates, the positive-correlation test and advantageous selection, credit "
              "rationing, mandates and risk adjustment (the Affordable Care Act, Massachusetts, inertia), online "
              "feedback, a new dial on the welfare cost of adverse selection, underwriting and Test-Achats in practice, "
              "and a frontier on selection on moral hazard and the end of pooling.",
        handoff="Part 14 turns from hidden information to hidden action; Parts 16-17 to auctions with private values; "
                "Part 26 to banks; Part 42 to social insurance; Part 45 to inertia and choice; Part 46 to group lending; "
                "Part 53 to information design; Part 61 to reputation on platforms.",
        outside="Part 7: expected utility and risk aversion; Part 10: monopoly pricing; Part 11: Nash, Bayesian and "
                "signalling-game equilibria. Chapter 6 uses log utility; chapter 8 the marginal cost of a pool, "
                "derived from its average cost.",
        objectives={
            "U": ["Explain adverse selection with Akerlof's market, and solve for the price and the share traded with "
                  "uniform quality.",
                  "Explain how guarantees, reputations and certification counter asymmetric information, and what "
                  "makes a signal credible.",
                  "Describe a death spiral, and the trade-offs of mandates, subsidies and risk adjustment."],
            "M": ["Solve Spence's signalling game for its separating and pooling equilibria, and apply the intuitive "
                  "criterion.",
                  "Solve the Rothschild-Stiglitz insurance market and its existence condition.",
                  "Measure the welfare cost of adverse selection with the Einav-Finkelstein diagram, from demand and "
                  "cost curves."],
            "D": ["Design and interpret positive-correlation tests, distinguishing adverse selection, moral hazard and "
                  "advantageous selection, and explain selection on moral hazard."],
            "I": ["Apply underwriting, risk adjustment and platform trust tools, and judge rating restrictions."],
        },
        results=[
            ("Lemons price, uniform quality", r"p^* = \mathbb{E}[q \mid q \le p^*] + a"),
            ("Spence separation", r"\tfrac{\theta_H - \theta_L}{c_L} \le e^* \le \tfrac{\theta_H - \theta_L}{c_H}"),
            ("Competitive insurance price", r"p = AC(p)"),
            ("Efficient insurance price", r"P(D) = MC(D)"),
            ("Positive correlation test", r"\operatorname{corr}(\text{cover}, \text{claim} \mid X) > 0"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, "s08_intermission", 7, 11, 12), D=(9, 15), I=(14,),
        also=(("Agora's information module", "explainer/economics/agora/info.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
    Part(
        n=14, level="U", widget="contract", prereq=(7, 8, 11, 13),
        question="How do you get someone to work for you when you can't see what they do?",
        story="The part opens in Xiaogang, Anhui, in 1978, where eighteen households sharing a commune's harvest each "
              "kept about an eighteenth of what their extra work added, until the farmers put their thumbprints on a "
              "secret contract to divide the land and keep what each family grew above the quota. The viewer writes "
              "Friday's contract for Crusoe's grove, then meets the free rider in teams (Alchian and Demsetz; "
              "Holmström's budget breaker), the principal-agent problem with its two constraints and pay as an "
              "inference, Holmström and Milgrom's optimal share and Prendergast's puzzle, the informativeness "
              "principle and chief executives paid for luck, and Safelite's piece rates (incentives and sorting). "
              "After an intermission of China's and India's incomes, multitasking and teaching to the test, with "
              "Called it? on cheating teachers in Chicago; tournaments in golf and mutual funds; career concerns and "
              "the ratchet; Ford's five-dollar day and Shapiro and Stiglitz's unemployment as discipline; "
              "sharecropping, Operation Barga and China's reform measured; incentives that backfire (Haifa, a Swiss "
              "nuclear-waste site, token pay); a new dial on piece rates; pay, franchises and procurement in practice; "
              "and a frontier on relational contracts and incentives for machines.",
        handoff="Part 15 turns from two people and a contract to costs that fall on third parties; Parts 16-17 to "
                "mechanism design; Part 24 to unemployment; Part 38 to wages; Part 46 to land and credit in "
                "development; Part 62 to personnel economics and management; Parts 64-65 to machines.",
        outside="Part 7: expected utility, CARA and certainty equivalents; Part 8: the firm and ownership (Grossman, "
                "Hart and Moore); Part 11: repeated games and the folk theorem; Part 13: hidden information. Chapter 3 "
                "uses log utility; chapter 4 the mean-variance certainty equivalent of a normal shock under CARA; "
                "chapter 8 the normal density; chapter 9 normal learning.",
        objectives={
            "U": ["Explain moral hazard and the free-rider problem in teams, and why a residual claimant or a budget "
                  "breaker helps.",
                  "Set up a principal-agent problem with participation and incentive constraints, and explain why the "
                  "best contract exposes the agent to risk.",
                  "Explain piece rates, tournaments and efficiency wages, and separate incentive effects from sorting."],
            "M": ["Derive the optimal linear share beta* = 1/(1 + r c sigma^2) and the agency cost.",
                  "Solve the two-outcome agency problem with both constraints binding, and state the informativeness "
                  "principle.",
                  "Solve multitask, tournament, career-concerns and no-shirking models, and the relational contract's "
                  "self-enforcement condition."],
            "D": ["Read the evidence on piece rates, executive pay, tournaments and crowding out, and judge what each "
                  "design identifies; connect reward misspecification in machine learning to multitasking."],
            "I": ["Design pay, franchise and procurement contracts on the line from a wage to a rent, and spot "
                  "ratchets, gaming and crowding out."],
        },
        results=[
            ("Team effort with equal sharing", r"e = a/(nc)"),
            ("Optimal linear share", r"\beta^* = \dfrac{1}{1 + r c \sigma^2}"),
            ("Incentive compatibility, two outcomes", r"(p_H - p_L)\,(u(w_H) - u(w_L)) \ge c"),
            ("Tournament effort", r"c\,e = \Delta \cdot \tfrac{1}{2\sigma\sqrt{\pi}}"),
            ("No-shirking wage", r"w = e + \tfrac{e}{q}\left(r + \tfrac{b}{u}\right)"),
            ("Relational effort", r"e \le \min(1/c,\ 2\delta/c)"),
        ],
        U=(0, 1, 2, 3, 6, "s08_intermission", 7, 8, 10, 11, 12), D=(15,), I=(14,),
        also=(("Agora's contracts module", "explainer/economics/agora/contracts.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
    Part(
        n=15, level="U", widget="pot", prereq=(2, 9, 11, 14),
        question="What happens when my choice lands on you, and nobody pays?",
        story="The part opens with James Meade's orchard and beekeeper of 1952, the textbook's example of a benefit no "
              "market could price, and Steven Cheung's 1972 survey of Washington's beekeepers, who had been paid "
              "pollination fees, or paid apiary rents, for decades. The viewer plays the shared pot, then meets the "
              "wedge between private and social cost (Bo's kiln and Ana's fish), Pigou's tax and the efficient amount "
              "of smoke, Coase's cattle and corn from his own table, with bargaining and transaction costs, Cheung's "
              "rents per hive, and public goods with Samuelson's condition, Lindahl's prices and the lighthouse. After "
              "an intermission of a century of sulphur dioxide, free riding measured (conditional cooperators, "
              "punishment and antisocial punishment), the commons from Gordon and Hardin to the cod collapse and "
              "Ostrom's design principles, permits and the acid-rain market with Called it? on its forecast benefits, "
              "prices against quantities, Vickrey's bottleneck and Stockholm's charge, networks, lock-in and ideas, a "
              "new dial on whether new roads fill, the toolkit in use, and a frontier on measuring the damage.",
        handoff="Parts 16-17 turn to markets designed on purpose; Part 21 to ideas and growth; Part 37 to cities; Parts "
                "41-42 to taxes and public goods; Part 44 to platforms; Part 47 to collective action; Part 48 to climate; "
                "Part 58 to cost-benefit analysis.",
        outside="Part 2: supply, demand and surplus; Part 9: the first welfare theorem; Part 11: the prisoner's dilemma "
                "and repeated games; Part 14: contracts. Chapter 8 uses logistic growth; chapter 10 expected values of "
                "squared normal shocks; chapter 11 piecewise-linear costs over the rush hour.",
        objectives={
            "U": ["Explain externalities as a wedge between private and social cost, and find the market and efficient "
                  "outputs and the deadweight loss.",
                  "Explain Pigou's tax, the Coase theorem and its dependence on transaction costs, and why the efficient "
                  "amount of pollution is not zero.",
                  "Classify goods by rivalry and excludability, and explain free riding, the commons and Ostrom's "
                  "design principles."],
            "M": ["Derive Samuelson's condition, voluntary provision and Lindahl prices for a public good.",
                  "Solve Gordon's fishery for open-access, maximum-economic and maximum-sustainable effort.",
                  "Derive Weitzman's comparison of prices and quantities, and Vickrey's bottleneck equilibrium and "
                  "toll."],
            "D": ["Read the evidence on permit markets, congestion charges and induced traffic, and design studies that "
                  "measure damages (natural experiments, instruments)."],
            "I": ["Design a tax, a cap-and-trade market or a road charge, and judge its distributional and political "
                  "costs."],
        },
        results=[
            ("Market and efficient output", r"P(Q) = MC_{\text{private}}(Q) \quad\text{vs}\quad P(Q) = MC(Q) + MD(Q)"),
            ("Pigou's tax", r"t^* = MD(Q^*)"),
            ("Samuelson's condition", r"\textstyle\sum_i MB_i(G) = MC(G)"),
            ("Open-access fishing effort", r"E_{oa} = \tfrac{r}{q}\left(1 - \tfrac{c}{pqK}\right)"),
            ("Prices against quantities", r"\Delta = \tfrac{\sigma^2 (C'' - B'')}{2 C''^2}"),
            ("Bottleneck cost per commuter", r"\delta N / s,\ \ \delta = \tfrac{\beta\gamma}{\beta + \gamma}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, "s08_intermission", 7, 8, 9, 11, 12), D=(13, 15), I=(14,),
        also=(("Agora's spillovers module", "explainer/economics/agora/public.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
    Part(
        n=16, level="U", widget="auction", prereq=(2, 7, 10, 11, 13),
        question="How should something be sold when nobody knows what it is worth to the buyers?",
        story="The part opens with Britain's 3G auction of 2000, designed by game theorists: thirteen bidders, 150 "
              "rounds, 22.5 billion pounds; that summer the Netherlands copied the design with as many licences as "
              "incumbents and raised less than a third of its forecast. The viewer bids twice for Crusoe's canoe, "
              "once paying the bid and once the next bid, then meets the four formats on the English and Dutch "
              "clocks, Vickrey's proof (and Goethe's sealed offer), shading derived, revenue equivalence on 60,000 "
              "simulated auctions and by the envelope argument, and the ways it fails: risk, the laboratory, linked "
              "values, asymmetry, collusion and entry. After an intermission of ninety years of the Treasury bill, "
              "Myerson's reserve and Bulow and Klemperer's extra bidder, the winner's curse from the Gulf of Mexico's "
              "oil leases to a jar of coins, the simultaneous ascending auction and the exposure problem, signals in "
              "the digits and the Dutch sale with Called it?, the auction behind every search, demand reduction in "
              "bond auctions and electricity, a new dial on what a reserve adds, auction desks, and a frontier on the "
              "incentive auction, credible auctions and machines that bid.",
        handoff="Part 17 designs markets without prices; Part 32 returns to the Treasury's debt; Part 48 to electricity "
                "and permits; Part 53 to information design; Part 54 to estimating values from bids; Parts 44 and 61 to "
                "the platforms.",
        outside="Part 7: risk aversion and expected utility; Part 10: the monopoly price; Part 11: Nash equilibrium and "
                "dominant strategies; Part 13: private information. Chapters 4-5 use order statistics of uniform "
                "variables and the envelope theorem; chapter 7 a hazard rate.",
        objectives={
            "U": ["Describe the English, Dutch, first-price and second-price auctions, and explain which are "
                  "strategically equivalent.",
                  "Prove that bidding one's value is dominant in a second-price auction, and derive equilibrium bid "
                  "shading in a first-price auction.",
                  "Explain the winner's curse, and why it grows with the number of bidders."],
            "M": ["State and prove revenue equivalence with the envelope formula, and use it to solve the all-pay "
                  "auction.",
                  "Derive Myerson's optimal reserve from virtual values, and compare it with one more bidder.",
                  "Compute Vickrey's prices for position auctions and the equilibrium of the generalized second price, "
                  "and explain demand reduction under a uniform price."],
            "D": ["Read the evidence on reserves, overbidding and collusion, and recover values from first-price bids "
                  "(Guerre, Perrigne and Vuong)."],
            "I": ["Design an auction for a given set of bidders, weighing entry, collusion, exposure and the seller's "
                  "risk."],
        },
        results=[
            ("First-price equilibrium bid", r"\beta(v) = \mathbb{E}[Y_1 \mid Y_1 < v] = \tfrac{n-1}{n}v"),
            ("Revenue equivalence", r"T(v) = vP(v) - \int_0^v P(s)\,ds - U(0)"),
            ("Virtual value", r"\varphi(v) = v - \tfrac{1 - F(v)}{f(v)}"),
            ("The winner's expected overestimate", r"s\,\tfrac{n-1}{n+1}"),
            ("Vickrey's price for slot i", r"\textstyle\sum_{j \ge i} (c_j - c_{j+1})\, v_{j+1}"),
            ("Values from first-price bids", r"v = b + \tfrac{G(b)}{(n-1)\,g(b)}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, "s08_intermission", 7, 8, 9, 10, 11, 12), D=(13, 15), I=(14,),
        also=(("Agora's auction house", "explainer/economics/agora/auctions.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),    Part(
        n=17, level="U", widget="match", prereq=(2, 9, 11, 16),
        question="Can a market be engineered, when prices cannot do the work?",
        story="The part opens with the American market for medical interns, which unravelled until hospitals hired "
              "students two years before graduation, then congested into exploding offers, until in 1952 the "
              "hospitals and students built a clearinghouse that Alvin Roth later showed was Gale and Shapley's "
              "algorithm. The viewer ranks three workshops under the Boston rule and finds the truth punished, then "
              "meets mechanisms and the revelation principle, Clarke's pivot rule for a footbridge, Myerson and "
              "Satterthwaite's impossible bargain, stable matching run on a board, and who should propose. After an "
              "intermission of a century and a half of American marriages, Britain's clearinghouses with Called it? on "
              "Roth's stability claim, couples and the 1998 redesign, school choice in Boston, New York and China, "
              "huts and kidney exchange with chains, why markets fail to form and repugnance, the assignment game, "
              "what a school lottery reveals, a new dial on what a sought-after school adds, clearinghouses and "
              "platforms, and a frontier on refugee placement and very large markets.",
        handoff="Part 18 adds up preferences by voting; Parts 24 and 39 match workers to jobs; Part 49 returns to "
                "schools; Part 53 to information design; Parts 44 and 61 to platforms; Part 64 to algorithms and "
                "fairness.",
        outside="Part 9: efficiency; Part 11: dominant strategies and Nash equilibrium; Part 16: Vickrey and the "
                "envelope argument. Chapter 4 uses double integrals over the unit square; chapter 11 a small linear "
                "programme; chapter 12 two-stage least squares (Part 4).",
        objectives={
            "U": ["Explain unravelling, congestion and safety as reasons markets fail to form, with the interns' "
                  "market and school choice as examples.",
                  "Run deferred acceptance and the Boston rule by hand, find blocking pairs, and explain why the "
                  "Boston rule rewards strategic lists.",
                  "Explain kidney exchange, cycles and chains, and the role of repugnance."],
            "M": ["Prove that deferred acceptance yields a stable matching that is optimal for the asking side, and "
                  "that truth is dominant for that side.",
                  "State the revelation principle; derive Clarke's pivot rule and explain why its budget cannot "
                  "balance; compute gains from trade under Myerson and Satterthwaite.",
                  "Run top trading cycles and find the core of an assignment game."],
            "D": ["Use the lotteries inside a centralized match to estimate school effects, controlling for each "
                  "applicant's chance of an offer, and read the evidence on sought-after schools."],
            "I": ["Design a clearinghouse for a real market, from its rules and details to its simulation and its "
                  "evaluation."],
        },
        results=[
            ("Blocking pair", r"a \succ_b \mu(b)\ \text{and}\ b \succ_a \mu(a)"),
            ("Clarke's pivot tax", r"t_i = \big|\textstyle\sum_{j \ne i} u_j\big|\ \text{if } i \text{ is pivotal}"),
            ("Gains from trade, uniform values", r"\tfrac16\ \text{(efficient)},\ \tfrac{9}{64}\ \text{(the "
                                                 r"best feasible)}"),
            ("Assignment-game core", r"u_i + w_j \ge a_{ij},\ \textstyle\sum u + \sum w = \max \sum a"),
            ("2SLS within types", r"\tau = \frac{E[y \mid z = 1, t] - E[y \mid z = 0, t]}{E[d \mid z = 1, t] - "
                                  r"E[d \mid z = 0, t]}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, "s08_intermission", 7, 8, 9, 10, 11, 12), D=(13, 15), I=(14,),
        also=(("Agora's matching module", "explainer/economics/agora/matching.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
    Part(
        n=18, level="U", widget="vote", prereq=(5, 9, 11, 17),
        question="Can the wants of many people be added up into what society wants?",
        story="The part opens with Condorcet's discovery in 1785 that a majority can prefer A to B, B to C and C to "
              "A, and Kenneth Arrow's proof in 1950 that the trouble is not majority rule: every rule fails. The "
              "viewer sees thirty-eight islanders' ballots give five winners under five rules, then follows Borda "
              "against Condorcet and the agenda setter, Arrow's theorem proved by the pivotal voter, the ways out "
              "through single peaks and May's theorem, strategic voting with Called it? on Duverger's law, and Sen's "
              "case for comparing people. After an intermission of two centuries of democracy in V-Dem's data, the "
              "part builds welfare functions from Bentham to Rawls through Atkinson's epsilon and Okun's leaky "
              "bucket, Harsanyi's veil against Rawls's, Scitovsky's reversal and the Paretian liberal, cost-benefit "
              "analysis with distributional weights and the discount rate, the value of a statistical life and a new "
              "dial on it, capabilities and the Human Development Index, the rules regulators and voters actually "
              "use, and a frontier on behavioural welfare, quadratic voting and preference aggregation for AI.",
        handoff="Part 19 opens Act V on growth; Part 45 returns to behavioural welfare; Part 47 to voting and "
                "parties; Part 48 to discounting the climate; Part 58 to scoring a bill with a value of a statistical "
                "life.",
        outside="Part 5: preferences and utility; Part 7: risk aversion and discounting; Part 9: Pareto efficiency; "
                "Part 17: mechanisms and Gibbard-Satterthwaite's cousin, safe truth. Chapter 7 uses power means; "
                "chapter 10 the present value of a stream.",
        objectives={
            "U": ["Compute the winner of one profile under plurality, the runoff, instant runoff, Borda's count and "
                  "Condorcet's rule, and show how the agenda decides a majority cycle.",
                  "State Arrow's conditions and theorem, Black's median voter theorem and May's theorem, and explain "
                  "what each way out gives up.",
                  "Explain the value of a statistical life, where its estimates come from and what it is not."],
            "M": ["Prove Arrow's theorem by the pivotal voter and the median voter theorem.",
                  "Compute Atkinson's equally distributed equivalent and index for any epsilon, and the switch between "
                  "Harsanyi's and Rawls's choices behind the veil.",
                  "Check Kaldor and Hicks's compensation test both ways, and show Scitovsky's reversal and Sen's "
                  "liberal paradox."],
            "D": ["Read the evidence on the value of a statistical life by design, and the case for and against "
                  "distributional weights and a low discount rate."],
            "I": ["Explain the parameters a regulatory analysis sets (the discount rate, distributional weights, the "
                  "value of a statistical life) and who sets them."],
        },
        results=[
            ("Borda's count", r"s(c) = \textstyle\sum_i \big(m - \text{rank}_i(c)\big)"),
            ("Atkinson's equivalent", r"y_\varepsilon = \Big(\tfrac1n \textstyle\sum_i "
                                      r"y_i^{\,1-\varepsilon}\Big)^{1/(1-\varepsilon)},"
                                      r"\ A_\varepsilon = 1 - y_\varepsilon / \bar y"),
            ("Okun's leaky bucket", r"\text{leak} \le 1 - (y_{\text{poor}} / y_{\text{rich}})^{\varepsilon}"),
            ("Ramsey's rule", r"r = \delta + \eta\, g"),
            ("Value of a statistical life", r"\text{VSL} = \Delta w / \Delta p"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, "s08_intermission", 7, 8, 9, 10, 11, 12), D=(13, 15), I=(14,),
        also=(("Agora's social choice module", "explainer/economics/agora/choice.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
]
