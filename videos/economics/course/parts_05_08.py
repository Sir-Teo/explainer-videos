"""Act II, Choosing (Parts 5-8)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=5, level="U", widget="wants",
        question="Can you tell what someone wants from what they buy, and what does \"rational\" assume?",
        story="The part opens with three weeks of Bo's receipts from the Island market, two of which contradict each "
              "other, and with the road from Jevons's marginal utility (1871) through Edgeworth, Pareto and Hicks and "
              "Allen to Paul Samuelson's note of 1938, which proposed to drop the last vestiges of utility and keep "
              "only what can be observed: choices. The viewer chooses on eleven budget lines of fish and coconuts. "
              "Tastes are built as a ranking (complete, transitive, continuous; the money pump punishes cycles), "
              "utility as a label (Debreu's representation; the lexicographic order no number can represent; the MRS "
              "as what survives relabelling), and the shapes of wanting from complements to substitutes through the "
              "CES family. The best bundle sets the MRS equal to the price ratio, and the multiplier is the value of "
              "a dollar; corners, a bulk price that makes demand jump at $20.49 of income, and the EITC's first kink, "
              "where only the self-employed bunch (Saez 2010), show where tangencies fail. After an intermission on a "
              "century of the American basket, revealed preference takes over: WARP, SARP and GARP; four islanders "
              "tested; Afriat's theorem and the utility his linear programme builds. The viewer's sheet is scored; "
              "random choosers fail on 97.5% of tries on these lines; children, students and 1,182 Dutch adults mostly "
              "pass, and the more consistent hold more wealth; America's spending, 1929-2025, passes a test that has "
              "no power within decades. Varian's bounds and a forecast from consistency alone; what rationality does "
              "not assume (selfishness, calculation, even a human chooser) and Becker's random households; a "
              "consistency dial; McFadden's BART forecast; a logit that recovers the value of time; and a frontier on "
              "random utility, scanner data and the consistency of a language model.",
        handoff="Part 6 follows a price change through to what people buy and how well off they are (Slutsky, Giffen "
                "goods, consumer surplus); Part 7 adds risk and time; the discrete-choice models return in Part 43, "
                "inconsistent choices and welfare in Part 45, taxable income in Part 41, and preference experiments "
                "on platforms in Part 61.",
        outside="School algebra, and calculus from chapter 5 (a derivative and a Lagrange multiplier, explained on "
                "screen). The revealed-preference chapters need only inequalities; chapter 12 uses a logistic curve.",
        objectives={
            "U": ["Find the best bundle on a budget for Cobb-Douglas, perfect substitutes and perfect complements, "
                  "including corner solutions, and explain why the MRS equals the price ratio at an interior optimum.",
                  "Test a short list of purchases for WARP and GARP by hand, and compute Afriat's efficiency index for "
                  "a two-choice contradiction.",
                  "Explain what rationality assumes (consistency) and what it does not (selfishness, calculation)."],
            "M": ["Derive demand and the multiplier with Lagrange's method, show demand is homogeneous of degree zero, "
                  "and find CES demand and its elasticity of substitution.",
                  "State Afriat's theorem, write its inequalities as a linear programme, and construct the "
                  "rationalizing utility; compute Varian's bounds on an indifference curve.",
                  "Compute a test's power against random choice, and explain why aggregate data rarely violate GARP."],
            "D": ["Explain random utility and its revealed-preference test (McFadden and Richter; Kitamura and Stoye), "
                  "and measures of the severity of violations (money pump, minimum cost).",
                  "Design a set of budgets to maximize a test's power, and say what it trades away."],
            "I": ["Estimate a value of time (or willingness to pay) from discrete choices with a logit, with a "
                  "standard error.",
                  "Read bunching at a kink as a measure of response, and say what the bunchers can adjust."],
        },
        results=[
            ("The tangency", r"\frac{\partial u/\partial x}{\partial u/\partial y} = \frac{p_x}{p_y},\qquad "
                             r"\lambda = \frac{\partial u/\partial x}{p_x}"),
            ("Cobb-Douglas demand", r"x = \frac{a\,m}{p_x},\qquad y = \frac{(1-a)\,m}{p_y}"),
            ("CES", r"\frac{x}{y} = \left(\frac{a}{1-a}\cdot\frac{p_y}{p_x}\right)^{\sigma}"),
            ("GARP", r"x_i\,R\,x_j \;\Rightarrow\; p_j\cdot x_j \le p_j\cdot x_i"),
            ("Afriat's inequalities", r"U_j \le U_i + \lambda_i\,p_i\cdot(x_j - x_i),\quad \lambda_i > 0"),
            ("Bunching at a kink", r"z \in \left[\tfrac{K}{(1+s)^{e}},\,K\right] \;\Rightarrow\; z^{*} = K"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, "s08_intermission"), D=(13,), I=(12,),
        also=(("Agora's consumer", "explainer/economics/agora/consumer.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
]
