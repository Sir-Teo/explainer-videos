"""Act XII, The Frontier (Parts 63-68)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=63, level="D", widget="network", prereq=(3, 8, 9, 20, 26, 33),
        question="When does a shock to one firm become a shock to everyone?",
        story="On 11 March 2011 an earthquake and tsunami strike north-east Japan; firms far from the coast, "
              "undamaged, stop for want of parts, and the loss travels along supplier-customer links to about half a "
              "point of Japan's growth. The Island's input-output table becomes a network: Domar weights as sums "
              "over supply paths, and Hulten's theorem that a small shock matters by the sector's sales and nothing "
              "else. The viewer picks the sector whose failure would cost most (services, by sales; energy, a third "
              "more than its sales say when inputs are hard to replace). Zipf-sized firms and lopsided networks keep "
              "idiosyncratic shocks from cancelling (Gabaix; Acemoglu et al.), and large shocks to essential inputs "
              "bend Hulten's line (Baqaee and Farhi). The Island's earthquake travels through specific inputs, as in "
              "Japan and America's disasters; Kremer's O-ring. After an intermission of Japan's industrial "
              "production through March 2011, banks' clearing vectors and contagion, robust yet fragile; weak ties "
              "(Called it? right); seeding a village; the key player; network formation, stable against efficient; "
              "two new Dials; and supply networks fragile by design.",
        handoff="Part 64 turns from networks to the machines that learn from data: prediction, selective labels and "
                "machine learning in economics.",
        outside="Part 3: the input-output table; Part 8: technologies and substitution; Part 9: general equilibrium; "
                "Part 20: growth accounting; Part 26: bank runs; Part 33: financial crises; Statistics, Built: "
                "random graphs and peer effects.",
        objectives={
            "U": ["Explain why a sector's sales, not its links, measure its importance for small shocks.",
                  "Explain why firm-level shocks need not cancel out in the aggregate.",
                  "Explain how a disaster travels along supply chains, and what stops it."],
            "M": ["Compute Domar weights from an input-output table and show that they add to more than one.",
                  "Prove Hulten's theorem for Cobb-Douglas economies, and compute the second-order term with CES.",
                  "Find the Eisenberg-Noe clearing vector and compare ring and complete networks."],
            "D": ["Solve a production network with complements and say when second-order terms dominate.",
                  "Characterize efficient and pairwise stable networks in the connections model.",
                  "Explain why supply networks can be fragile in equilibrium, and what it implies for policy."],
            "I": ["Map a supply chain beyond the first tier and identify the inputs that cannot be replaced."],
        },
        results=[
            ("Domar weights", r"\lambda' = \beta'(I - \Omega)^{-1}"),
            ("Hulten's theorem", r"d\log Y = \sum_i \lambda_i \, d\log A_i"),
            ("Granular volatility", r"\sigma_{Y} = \sigma \sqrt{\textstyle\sum_i s_i^2}"),
            ("Clearing vector", r"p_i = \min\!\Big(\bar p_i,\; e_i + \sum_j \pi_{ji} p_j\Big)"),
            ("Key player effort", r"x = (I - \delta G)^{-1} a"),
        ],
        U=(0, 1, 2, 3, 4, 7, "s09_intermission", 9, 10), D=(5, 11, 12, 13, 15), I=(6, 8, 14),
        also=(("Agora's network module", "explainer/economics/agora/network.py"),
              ("The Data Room: Japan's industrial production", "explainer/economics/data")),
    ),
]
