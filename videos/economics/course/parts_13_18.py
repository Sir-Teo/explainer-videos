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
    ),
]
