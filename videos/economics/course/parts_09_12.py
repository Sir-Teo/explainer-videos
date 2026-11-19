"""Act III, Markets (Parts 9-12)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=9, level="U", widget="box", prereq=(5, 8),
        question="Can a whole economy of selfish traders reach a state nobody could improve on, and will it?",
        story="The part opens in R. A. Radford's prisoner-of-war camps (Economica, 1945): equal Red Cross parcels, a "
              "padre who walks round the camp with a tin of cheese and five cigarettes and comes back with a whole "
              "parcel, cigarettes as money, one price where the Exchange and Mart boards were read and two "
              "cigarettes in twenty across one hut where they weren't, then slump and liberation. Nine years later "
              "Arrow and Debreu prove that such an equilibrium can exist in any economy of their kind. The viewer "
              "plays four proposed trades between Ana and Bo; the Edgeworth box shows why two are accepted and one "
              "is efficient (the lens, the contract curve); prices bring offer curves, the competitive equilibrium "
              "at 1.018 baskets a fish, Walras's law and the law of one price as a Fact (Brent against WTI; price "
              "levels across countries; two island villages). The core shrinks to the price outcome as the box "
              "economy is replicated (Edgeworth 1881; Debreu and Scarf 1963; Aumann 1964); the first welfare "
              "theorem is proved in five lines and its assumptions listed; the second reaches an efficient point by "
              "a lump-sum transfer and a separating line. After an intermission of Brent and WTI month by month, "
              "existence by Brouwer and by Sperner's colouring with Scarf's walk, stability (Arrow, Block and "
              "Hurwicz) and Scarf's cycle (also in the laboratory), the whole Island cleared by Newton and by the "
              "auctioneer, Crusoe decentralized, three equilibria and the Sonnenschein-Mantel-Debreu theorem, Arrow "
              "securities against a bond, the calculation debate with Kantorovich's resolving multipliers, a new "
              "dial on misallocation (Hsieh and Klenow; Bils, Klenow and Ruane), CGE models and the 1992 NAFTA "
              "forecasts against what happened (Called it?), and a frontier on PPAD, the housing market's top "
              "trading cycles and Budish's course market.",
        handoff="Part 10 drops price-taking (the price maker), Part 11 brings games, Parts 13-15 the failures the first "
                "theorem's assumptions rule out (information, incentives, spillovers), Parts 16-17 markets by design, "
                "Part 18 fairness and social choice, Part 21 misallocation and growth, Part 23 the prices of risk, "
                "and Parts 35-36 trade models with the new-goods margin.",
        outside="Parts 5-8: indifference curves, demand and the firm. Chapter 7 states Brouwer's fixed-point theorem "
                "without proof; chapter 12 uses expected utility from Part 7; chapter 13 one linear programme.",
        objectives={
            "U": ["Draw an Edgeworth box with indifference curves, the lens of mutual gains and the contract curve, and "
                  "say which trades both traders accept and which are Pareto efficient.",
                  "Find the competitive equilibrium of a two-good exchange economy from offer curves, and use Walras's "
                  "law.",
                  "State the two welfare theorems, the assumptions of the first, and why lump-sum transfers are rare."],
            "M": ["Prove the first welfare theorem; explain the core, its replication and the Debreu-Scarf limit "
                  "theorem.",
                  "Prove existence with a fixed point, and find an approximate equilibrium with Sperner's lemma and "
                  "Scarf's walk; analyze tatonnement stability, gross substitutes and Scarf's example.",
                  "State the Sonnenschein-Mantel-Debreu theorem and what it implies; price Arrow securities and show "
                  "why incomplete markets fail to share risk; read prices off the dual of a linear programme."],
            "D": ["Discuss the complexity of computing equilibria (PPAD), markets with indivisibilities (Shapley and "
                  "Scarf's top trading cycles) and approximate competitive equilibrium from equal incomes (Budish)."],
            "I": ["Describe how computable general equilibrium models are calibrated and used, and judge a forecast "
                  "against outcomes (Kehoe on NAFTA)."],
        },
        results=[
            ("Contract curve", r"MRS_{\text{Ana}} = MRS_{\text{Bo}}"),
            ("Walras's law", r"p \cdot z(p) = 0"),
            ("First welfare theorem", r"\text{equilibrium} \Rightarrow \text{Pareto efficient}"),
            ("Existence", r"f(p)_k = \frac{p_k + \max(z_k, 0)}{1 + \sum_j \max(z_j, 0)},\quad f(p^*) = p^*"),
            ("Tatonnement", r"\dot p = z(p),\qquad \tfrac{d}{dt}\textstyle\sum_k p_k^2 = 2\,p\cdot z = 0"),
            ("Misallocation (lognormal)", r"\log\frac{Y_{\text{eff}}}{Y} = \frac{\sigma}{2}\,\operatorname{var}"
                                          r"(\log \mathit{TFPR})"),
        ],
        U=(0, 1, 2, 3, 5, 6, "s08_intermission", 10, 13, 14), D=(16,), I=(15,),
        also=(("Agora's general equilibrium", "explainer/economics/agora/ge.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
    Part(
        n=10, level="U", widget="ferry", prereq=(6, 8, 9),
        question="What does a seller do when the price is hers to set?",
        story="The part opens with Jules Dupuit, a French engineer of bridges and roads: in 1844 he argues that a "
              "bridge is worth what crossing it is worth to everyone who crosses, so a toll on a crossing that costs "
              "nothing turns value away for no saving; in 1849 he explains third-class carriages without roofs as a "
              "way to keep anyone who could pay for second class from travelling third. The viewer sets one fare "
              "for Bo's ferry against a hundred islanders' values; marginal revenue, the monopoly price, the "
              "missing supply curve and the Lerner index follow, then what monopoly costs (Harberger's triangles, "
              "Posner's and Tullock's rectangles). Price discrimination comes in Pigou's three degrees: a price for "
              "every buyer, a student fare that opens a market (Schmalensee; Varian's output test), and a screening "
              "menu with the bottom made worse on purpose (Mussa and Rosen; Deneckere and McAfee). After an "
              "intermission of green coffee and the shelf price month by month, two-part tariffs (Oi's Disneyland), "
              "bundling (Stigler; Adams and Yellen), the Coase conjecture solved for price changes from once a year "
              "to every day, natural monopoly and Ramsey-Boiteux prices, rate-of-return regulation and gold plating "
              "(Averch and Johnson) against price caps (Littlechild), monopsony with a minimum wage, pass-through "
              "in theory and as a Fact measured on coffee (Nakamura and Zerom), a new dial on markups (De Loecker, "
              "Eeckhout and Unger against Traina), Littlewood's rule for fare classes, and a frontier on "
              "personalized prices learned from an experiment (Dube and Misra) and pricing algorithms.",
        handoff="Part 11 brings games and Part 12 competition among a few sellers; Parts 13-14 screening and "
                "regulation under hidden information; Part 16 auctions; Part 38 monopsony and minimum wages; Part 41 "
                "tax incidence; Parts 43-44 measuring market power and antitrust; Part 60 pricing and revenue "
                "management in practice.",
        outside="Parts 6 and 8: demand, elasticities and costs; Part 9: surplus and efficiency. Chapter 15 uses one "
                "normal quantile; chapter 16 a logistic regression, stated, not derived.",
        objectives={
            "U": ["Find a monopolist's price from marginal revenue and marginal cost, state the Lerner index, and "
                  "measure the deadweight loss.",
                  "Explain first-, second- and third-degree price discrimination, when third-degree discrimination "
                  "raises welfare, and how two-part tariffs and bundling extract surplus.",
                  "Explain natural monopoly, average-cost and Ramsey pricing, and the trade-off between "
                  "rate-of-return regulation and price caps."],
            "M": ["Solve the two-type screening problem: no distortion at the top, the low type's quality cut, the "
                  "information rent.",
                  "Solve a two-period durable-goods monopoly and state the Coase conjecture; derive Ramsey prices "
                  "and the Averch-Johnson distortion.",
                  "Derive pass-through for linear and constant-elasticity demand, estimate it with distributed lags, "
                  "and read Nakamura and Zerom's decomposition."],
            "D": ["Discuss personalized pricing learned from experiments (Dube and Misra), its welfare effects, and "
                  "algorithmic pricing and collusion (Calvano et al.; Assad et al.)."],
            "I": ["Apply Littlewood's rule for two fare classes, and explain fences and revenue management."],
        },
        results=[
            ("Monopoly: MR = MC and the Lerner index", r"\frac{p - c}{p} = -\frac{1}{\varepsilon}"),
            ("Screening, two types", r"q_L = \theta_L - \tfrac{s}{1-s}(\theta_H - \theta_L),\quad q_H = \theta_H"),
            ("Ramsey-Boiteux prices", r"\frac{p_i - c_i}{p_i} = \frac{k}{\varepsilon_i}"),
            ("Pass-through", r"\rho = \frac{dp}{dc} = \frac{1}{2 + q P''(q)/P'(q)}"),
            ("Littlewood's rule", r"p_{\text{hi}}\,P(D_{\text{hi}} \ge y) = p_{\text{lo}}"),
            ("Markups from production", r"\mu = \theta_V \frac{pQ}{P_V V}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, "s08_intermission", 7, 8, 10, 11, 12, 13), D=(16,), I=(15,),
        also=(("Agora's price maker", "explainer/economics/agora/pricing.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
]
