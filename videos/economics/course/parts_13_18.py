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
]
