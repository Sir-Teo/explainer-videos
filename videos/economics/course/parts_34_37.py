"""Act VII, The World Economy (Parts 34-37)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=34, level="U", widget="peg", prereq=(3, 23, 27, 28, 30, 31),
        question="What sets the price of one money in terms of another, and what can a country not have at once?",
        story="The part opens on Wednesday 16 September 1992 in four acts, as the Bank of England raises its rate, "
              "announces another rise, spends its reserves and leaves the Exchange Rate Mechanism by evening. It "
              "reads the balance of payments as accounts, puts the viewer in the governor's chair with reserves "
              "draining, and shows with Obstfeld's model why a peg in a middle zone falls if traders expect it to. "
              "It tests purchasing power parity with the Big Mac index and 150 years of real exchange rates, "
              "uncovered parity with Fama's regression and the carry trade, and every model against the random walk "
              "with Meese and Rogoff's horse race rerun; derives Mundell-Fleming's trilemma and Dornbusch's "
              "overshooting; and after an intermission of the pound since 1971 turns to three generations of "
              "currency crises, the IMF and its critics, the euro, global imbalances and the dollar's dominance; two "
              "dials, Meese and Rogoff as Called it?, and a frontier where finance, not trade, moves currencies.",
        handoff="Part 35 turns from money to goods with comparative advantage; Part 36 measures the pass-through of "
                "tariffs; Part 66 returns to the dollar's power, sanctions and trade wars.",
        outside="Part 3: the national accounts; Part 23: asset prices and no arbitrage; Part 27: IS-LM; Part 28: "
                "expectations; Part 30: sticky prices; Part 31: the central bank. Chapter 4 uses Newey-West standard "
                "errors for overlapping horizons; chapter 7 a first-order differential equation; chapter 12 a "
                "distributed-lag regression.",
        objectives={
            "U": ["Read the balance of payments, and explain the current account as saving minus investment.",
                  "Explain purchasing power parity, the Big Mac index and the Balassa-Samuelson effect, and why real "
                  "exchange rates return to parity only slowly.",
                  "State the trilemma, and describe the three generations of currency crises with an example of "
                  "each."],
            "M": ["Derive the effects of fiscal and monetary policy under fixed and floating rates in "
                  "Mundell-Fleming.",
                  "Derive Dornbusch's overshooting and its impact factor.",
                  "Estimate a PPP half-life, Fama's regression with overlapping-horizon standard errors, and an "
                  "out-of-sample horse race against the random walk."],
            "D": ["Solve the timing of a first-generation attack and the band of self-fulfilling crises.",
                  "Explain the exchange-rate disconnect and the financial explanations at the frontier: limited "
                  "intermediaries and financial shocks."],
            "I": ["Read a reserve-adequacy or currency-strategy note: carry, parity, pass-through and the dollar's "
                  "role."],
        },
        results=[
            ("The current account", r"CA = S - I = (S_p - I) + (T - G)"),
            ("Uncovered interest parity", r"E_t[s_{t+h}] - s_t = i_t - i^*_t"),
            ("Fama's regression", r"s_{t+h} - s_t = \alpha + \beta\,(i_t - i^*_t) + \varepsilon_{t+h}, \quad "
                                  r"\hat\beta < 1"),
            ("The PPP half-life", r"q_t = \rho\, q_{t-1} + \varepsilon_t, \qquad t_{1/2} = \ln 0.5 / \ln \rho"),
            ("Overshooting", r"s_0 - \bar s = \frac{\Delta m}{\lambda\theta}"),
            ("Krugman's attack", r"T = (\bar s - \alpha\mu - d_0)/\mu"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, "s09_intermission", 8, 9, 10, 11, 12, 13), D=(15,), I=(14,),
        also=(("Agora's open economy", "explainer/economics/agora/openecon.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
    Part(
        n=35, level="U", widget="fournumbers", prereq=(2, 8, 9, 11, 18),
        question="Why do countries trade, and who wins and loses when they do?",
        story="The part opens on Stanislaw Ulam's challenge to Paul Samuelson, to name one proposition in the social "
              "sciences that is both true and not trivial, and Samuelson's answer: comparative advantage. The viewer "
              "decides who should make what when one island is worse at everything; then Ricardo's four numbers with "
              "the world price and the wage band, the chain of goods and the Dornbusch-Fischer-Samuelson continuum, "
              "and a test: Japan's opening in 1859, with Bernhofen and Brown's tables. Heckscher and Ohlin's factor "
              "proportions are drawn in the Lerner diagram with their four theorems, Stolper and Samuelson's losers "
              "inside each country, and Leontief's paradox and Trefler's missing trade, recomputed from his data. "
              "After an intermission of America's tariff since 1929 come specific factors, a tariff's triangles and "
              "the optimal tariff, protection for sale, the tariff war and the trade agreements that escape it, and "
              "compensation, with its is/ought step; a new dial, the Fact of two-way trade, Heckscher and Ohlin's "
              "prediction for America as Called it?, and a frontier of Ricardo tested in the fields.",
        handoff="Part 36 explains two-way trade with scale and firms, measures the trade elasticity with gravity, and "
                "follows the China shock's losers; Part 37 asks where economic activity locates; Part 66 returns to "
                "tariffs, trade wars and industrial policy.",
        outside="Part 2: supply, demand and surplus; Part 8: production and cost functions, Shephard's lemma; Part 9: "
                "general equilibrium; Part 11: the prisoner's dilemma and best responses; Part 18: compensation tests "
                "and welfare. Chapter 5 uses Cobb-Douglas unit costs and a linear system in logs; chapter 7 a "
                "factor-content regression; chapter 11 best responses found numerically.",
        objectives={
            "U": ["Find comparative advantage from four numbers, the range of trade prices, and the gains for both "
                  "countries.",
                  "State the Heckscher-Ohlin and Stolper-Samuelson theorems, and say who gains and loses from trade "
                  "inside a country.",
                  "Measure a tariff's effects on consumers, producers and revenue, and explain why protection is "
                  "common."],
            "M": ["Solve the Dornbusch-Fischer-Samuelson continuum and its comparative statics.",
                  "Derive factor price equalization and the magnification effect from zero-profit conditions.",
                  "Compute the optimal tariff and the Nash tariffs of a tariff war."],
            "D": ["Run and interpret tests of comparative advantage: Bernhofen and Brown's inner product and "
                  "Trefler's factor-content statistics.",
                  "Explain the Arkolakis-Costinot-Rodriguez-Clare formula and how Costinot and Donaldson test "
                  "Ricardo."],
            "I": ["Read a tariff schedule, a trade-remedy case and an estimate of the gains from a trade agreement."],
        },
        results=[
            ("Comparative advantage", r"\frac{a_{1}}{a_{2}} < \frac{a^*_{1}}{a^*_{2}} \;\Rightarrow\; \text{Home "
                                      r"exports good 1}"),
            ("The DFS equilibrium", r"A(\bar z) = \omega = \frac{\bar z}{1 - \bar z}\,\frac{L^*}{L}"),
            ("Stolper-Samuelson", r"\hat w = \frac{\hat p_1 (1-\alpha_2) - \hat p_2 (1-\alpha_1)}{\alpha_1 - "
                                  r"\alpha_2}"),
            ("HOV", r"F_c = V_c - s_c V_w"),
            ("The optimal tariff", r"t^{\text{opt}} = 1/\varepsilon^*"),
            ("The gains from trade", r"1 - \lambda^{1/\varepsilon}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, "s09_intermission", 8, 9, 10, 11, 12, 13), D=(7, 15), I=(14,),
        also=(("Agora's trade", "explainer/economics/agora/trade.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
    Part(
        n=36, level="U", widget="gravity", prereq=(10, 12, 24, 35),
        question="Why is most trade between similar countries, and what did a generation of imports from China do?",
        story="The part opens on the Ideal X leaving Newark in April 1956 with fifty-eight trailers on deck, and on "
              "the trade web of 2019. It measures two-way trade with the Grubel-Lloyd index, explains it with "
              "Krugman's variety and scale and the home-market effect, and asks the viewer where Spain sells the "
              "most. Gravity is estimated on every pair of countries by least squares and PPML, with McCallum's "
              "border puzzle; then firms: Bernard and Jensen's rare exporters, Melitz's selection, and Eaton and "
              "Kortum's Ricardo with a distribution. After an intermission of America's imports from China, one "
              "formula gives the gains from trade and exact hat algebra a counterfactual on real 2019 data; then the "
              "China shock with Autor, Dorn and Hanson's design reproduced on the Island, the tariffs of 2018 and "
              "2025, value chains, three dials, Krugman's 1995 estimate as Called it?, and a frontier.",
        handoff="Part 37 turns to why activity clusters in a few places; Part 63 to fragile networks; Part 66 to "
                "tariffs, industrial policy and the 2025 tariffs on the quantitative model.",
        outside="Part 10: monopolistic pricing and markups; Part 12: firms and market structure; Part 24: local "
                "labour markets; Part 35: comparative advantage and the gains formula. Chapter 4 uses Poisson "
                "pseudo-maximum likelihood with two sets of fixed effects; chapter 7 the Frechet distribution; "
                "chapter 8 a fixed-point solution for wages; chapter 9 instrumental variables.",
        objectives={
            "U": ["Measure two-way trade with the Grubel-Lloyd index and explain it with variety and scale.",
                  "State the gravity equation and interpret its distance and border effects.",
                  "Describe the China shock's design and findings, and who paid the 2018-19 tariffs."],
            "M": ["Solve Krugman's model and the home-market effect; solve Melitz's cutoffs and the gain from "
                  "opening.",
                  "Estimate gravity by least squares and by PPML with fixed effects, and explain why they differ.",
                  "Compute the gains from trade by the ACR formula and a counterfactual by exact hat algebra."],
            "D": ["Derive Eaton and Kortum's trade shares from Frechet draws, and connect theta to the trade "
                  "elasticity.",
                  "Explain what shift-share designs assume, and why the short- and long-run trade elasticities "
                  "differ."],
            "I": ["Run a trade-policy counterfactual from a matrix of trade flows, and read a tariff pass-through "
                  "study."],
        },
        results=[
            ("Grubel-Lloyd", r"GL = 1 - \frac{|X - M|}{X + M}"),
            ("Gravity", r"X_{od} = \exp(a_o + b_d - \delta \ln D_{od} + \dots)"),
            ("Melitz's export cutoff", r"\varphi_x^* = \tau \left(\frac{f_x}{f}\right)^{1/(\sigma-1)} \varphi^*"),
            ("Eaton-Kortum", r"\pi_{ni} = \frac{T_i (w_i d_{ni})^{-\theta}}{\sum_k T_k (w_k d_{nk})^{-\theta}}"),
            ("Hat algebra", r"\hat W_n = \hat E_n / \hat P_n, \quad \hat P_n = \Big(\sum_i \pi_{ni} (\hat w_i "
                            r"\hat d_{ni})^{-\theta}\Big)^{-1/\theta}"),
            ("The China shock", r"\Delta L^m_{z} = \beta \sum_k \frac{L_{zk}}{L_z} \frac{\Delta M_k}{L_k} + "
                                r"\varepsilon_z"),
        ],
        U=(0, 1, 2, 3, 4, 5, "s09_intermission", 9, 10, 11, 12), D=(7, 14), I=(13,),
        also=(("Agora's trade", "explainer/economics/agora/trade.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
    Part(
        n=37, level="U", widget="schelling", prereq=(8, 9, 15, 20, 36),
        question="Why is economic activity piled up in a few places, and what does that do to the people in them?",
        story="The part opens on Thomas Schelling's checkerboard, played by Agora: coins content with a third of their "
              "neighbours alike end with three quarters alike. The viewer guesses the outcome, then sees the whole "
              "tolerance curve. Von Thuenen's rings and the monocentric city derive rents from transport costs, with "
              "the car spreading the town and the lift building it up. Why cities exist: sharing, matching and "
              "learning, with sorting separated from agglomeration by movers on the Island and in France; Zipf's law "
              "on America's metropolitan areas, grown from Gibrat's law; Krugman's core and periphery and its "
              "tomahawk. After an intermission of five centuries of urbanization, spatial equilibrium reads "
              "amenities from wages and rents; then housing supply with Saiz's elasticities and twenty cities' "
              "prices, rent control in San Francisco, Moving to Opportunity, the Berlin Wall, railways and highways, "
              "place-based policy, two dials, Cairncross's Death of Distance as Called it?, and a frontier on remote "
              "work and the climate.",
        handoff="Part 38 opens Act VIII with wages and the minimum wage; Part 40 maps mobility and neighbourhoods "
                "county by county; Part 48 values clean air with the same spatial logic.",
        outside="Part 8: production with land and capital; Part 9: equilibrium; Part 15: externalities; Part 20: "
                "growth; Part 36: variety, scale and the gains-from-trade formula. Chapter 3 solves a differential "
                "equation for the rent gradient and integrates a density; chapter 5 uses a rank-size regression and a "
                "stationary distribution; chapter 6 a fixed point and bifurcation; chapter 11 a quantitative model "
                "with Frechet commuting.",
        objectives={
            "U": ["Explain how mild preferences can produce strong segregation, and what Schelling's model does not "
                  "show.",
                  "State the forces for and against agglomeration, and why the raw big-city premium overstates it.",
                  "Describe spatial equilibrium: why wages, rents and amenities move together, and who gains from a "
                  "local boom."],
            "M": ["Derive the rent gradient of the monocentric city from Muth's condition, and solve a closed city.",
                  "Fit Zipf's law by the rank minus one half regression, and explain it with Gibrat's growth and a "
                  "floor."],
            "D": ["Solve Krugman's core and periphery and find its break and sustain points.",
                  "Explain how a quantitative spatial model identifies agglomeration from the Berlin Wall."],
            "I": ["Read a housing supply elasticity, a rent-control study and a transport appraisal, and say what "
                  "each means for a city's policy."],
        },
        results=[
            ("Muth's condition", r"p'(x)\,h(x) = -t"),
            ("Bid rent", r"R_i(x) = Y_i\,(p_i - c_i - f_i x)"),
            ("Zipf's law", r"\ln(\text{rank} - \tfrac12) = c - \zeta \ln S, \quad \zeta \approx 1"),
            ("The break point", r"T_B^{\sigma-1} = \frac{(\rho+\mu)(1+\mu)}{(\rho-\mu)(1-\mu)}"),
            ("Spatial equilibrium", r"\ln w_j - \alpha \ln r_j + q_j = \bar v"),
            ("Quality of life", r"\hat q_j = \alpha \ln r_j - \ln w_j"),
        ],
        U=(0, 1, 2, 4, "s08_intermission", 7, 8, 9, 10, 12, 13, 14), D=(6, 11, 16), I=(15,),
        also=(("Agora's city", "explainer/economics/agora/city.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
]
