"""Act VIII, Work and the State (Parts 38-42)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=38, level="U", widget="minimum", prereq=(4, 8, 9, 10),
        question="What sets a wage, and what happens when the law sets it instead?",
        story="The part opens on Card and Krueger's telephone survey of 410 fast-food restaurants either side of the "
              "Delaware in 1992, and asks the viewer to predict what New Jersey's higher minimum did; the answer is "
              "recomputed from their published data. It builds labour supply with income effects and three "
              "elasticities, tests it on cab drivers and Uber, derives the competitive prediction for a wage floor, "
              "reads the border design and its critics, counts missing and excess jobs with the bunching estimator, "
              "and explains the puzzle with monopsony, then runs the same design on the Island under both theories. "
              "After an intermission of the real federal minimum since 1938, it fits Mincer's equation, measures the "
              "return to schooling by ability controls and natural experiments with Card's college-distance "
              "instrument recomputed, builds Roy's model with Heckman's correction, reads the Mariel boatlift three "
              "ways, enters three dials, and takes the 1979 survey of economists as Called it?.",
        handoff="Part 39 turns to why wages differ: skill, technology, discrimination; Part 41 uses the labour supply "
                "elasticities for taxes; Part 42 asks what insurance against job loss does.",
        outside="Part 4: difference in differences and instrumental variables; Part 8: the firm's demand for "
                "inputs; Part 9: competitive equilibrium; Part 10: market power, here on the buying side. Chapter 2 "
                "uses Slutsky's equation; chapter 7 a firm's first-order condition with an upward-sloping supply; "
                "chapter 10 two-stage least squares; chapter 11 a probit and the inverse Mills ratio.",
        objectives={
            "U": ["Read a difference-in-differences design and say what its comparison group assumes.",
                  "Explain the competitive and monopsony predictions for a minimum wage, and why studies disagree.",
                  "State what a year of school is worth and why a regression may overstate or understate it."],
            "M": ["Derive Marshallian, Hicksian and Frisch elasticities and relate them by Slutsky's equation.",
                  "Solve a monopsonist's hiring with and without a minimum wage, and the markdown 1/(1 + eta).",
                  "Estimate the return to schooling by least squares and two-stage least squares, and correct a "
                  "selected sample by Heckman's two steps."],
            "D": ["Explain why one well-designed study can mislead, and what accumulating designs buys.",
                  "Say what remains open about high minimums, employer concentration and non-competes."],
            "I": ["Advise on a minimum wage, a pay band or a training programme with the evidence and its limits."],
        },
        results=[
            ("Difference in differences", r"\hat\delta = (\bar y_{T,1} - \bar y_{T,0}) - (\bar y_{C,1} - "
                                          r"\bar y_{C,0})"),
            ("Slutsky", r"\varepsilon^{H} = \varepsilon^{M} - w\,\frac{\partial h}{\partial y}"),
            ("The monopsony markdown", r"\frac{\text{MRPL} - w}{\text{MRPL}} = \frac{1}{1 + \eta}"),
            ("Mincer", r"\ln w = \alpha + \rho S + \beta_1 X + \beta_2 X^2"),
            ("The Wald estimator", r"\hat\rho = \frac{\bar y_1 - \bar y_0}{\bar S_1 - \bar S_0}"),
            ("Heckman", r"E[\ln w \mid \text{selected}] = X\beta + \sigma_{\varepsilon v}\,\lambda(Z\gamma)"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, "s10_intermission", 9, 12, 13), D=(8, 15), I=(14,),
        also=(("Agora's labour", "explainer/economics/agora/labour.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
]
