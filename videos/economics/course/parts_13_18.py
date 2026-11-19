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
]
