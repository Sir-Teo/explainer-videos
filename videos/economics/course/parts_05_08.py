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
    Part(
        n=6, level="U", widget="demand", prereq=(5,),
        question="When a price changes, what happens to what people buy, and to how well off they are?",
        story="The part opens in Hunan in 2006, where Robert Jensen and Nolan Miller gave randomly chosen poor "
              "households vouchers that cut the price of rice by up to a quarter, and the households that were poor "
              "but not the poorest ate less rice: the Giffen behaviour Marshall described in 1895 and Stigler said would "
              "make its discoverer immortal. The viewer runs one of the Island's poorest households for a week on $21 "
              "and buys more coconuts when they get dearer. Demand is traced from the tangency (price- and "
              "income-consumption curves, homogeneity, elasticities and the adding-up rules); Slutsky's equation of "
              "1915, unread for twenty years, splits a price change into substitution and income effects, drawn as two "
              "moves with Hicks's and Slutsky's compensations; its elasticity form gives the recipe for Giffen "
              "behaviour, and the subsistence model's three zones, Jensen and Miller's table 3 and the same design run "
              "on 1,300 simulated households with the truth planted show where to look and how an average hides it. "
              "Duality gives four functions for one consumer (Roy, Shephard, a concave expenditure function), and "
              "integrability a loop of prices that pumps money from demand that comes from no preference. After an "
              "intermission on a century of relative prices, Engel curves (America's century, 2024's quintiles, "
              "Hamilton's use of their drift to measure CPI bias, Engel's law as a call that came true), welfare in "
              "dollars (CV, EV, consumer's surplus, Willig, Hausman's exact deadweight loss), the cost of living "
              "(Konus, the substitution bias, Hicks's virtual prices and Apple-Cinnamon Cheerios), demand systems (the "
              "linear expenditure system, the AIDS estimated and tested on an island survey, Gorman's aggregation), the "
              "dials, the CPI's methods, food prices and poor households, Ramsey taxes, and a frontier on inflation "
              "inequality and welfare that depends on income.",
        handoff="Part 7 adds time and risk; CV and EV return in cost-benefit analysis (Part 18), the CPI and inflation "
                "by income group in Part 28, Ramsey and optimal taxation in Part 41, demand estimation with product "
                "characteristics in Part 43, and food prices and poverty in Part 46.",
        outside="School algebra and the calculus of Part 5 (derivatives, a Lagrange multiplier); logarithms for the "
                "elasticities. Chapters 5 and 6 use partial derivatives and, once, Green's theorem, explained on screen.",
        objectives={
            "U": ["Derive a demand curve and an Engel curve from a utility function, and compute own-price, cross-price "
                  "and income elasticities.",
                  "Split a price change into substitution and income effects with Hicks's and with Slutsky's "
                  "compensation, and use the Slutsky equation to say when demand can slope up.",
                  "Compute compensating and equivalent variation and consumer's surplus for a price change, and say "
                  "which is larger and why."],
            "M": ["State and use the duality identities (Roy's identity, Shephard's lemma, e(p, v(p, m)) = m), and "
                  "show that compensated demand slopes down because the expenditure function is concave.",
                  "Check a demand system for integrability (symmetry and negative semidefiniteness of the Slutsky "
                  "matrix), and estimate and test an almost ideal demand system.",
                  "Relate Laspeyres, Paasche and the true cost-of-living index, and value a new good by its virtual "
                  "price."],
            "D": ["Explain how scanner data, variety corrections and income-dependent preferences change the "
                  "measurement of inflation and welfare (Jaravel; Feenstra; Redding and Weinstein; Jaravel and "
                  "Lashkari; Atkin et al.)."],
            "I": ["Use budget shares to estimate the first-order welfare effect of a price change on different "
                  "households, and explain how the official CPI allows for substitution.",
                  "Apply Ramsey's inverse-elasticity rule and state the equity objection."],
        },
        results=[
            ("The Slutsky equation", r"\frac{\partial x_i}{\partial p_j} = \frac{\partial h_i}{\partial p_j} - "
                                     r"x_j\,\frac{\partial x_i}{\partial m}"),
            ("In elasticities", r"\varepsilon_{ii} = \varepsilon^{h}_{ii} - w_i\,\eta_i"),
            ("Duality", r"e(p, v(p,m)) = m,\qquad h_i = \frac{\partial e}{\partial p_i},\qquad "
                        r"x_i = -\frac{\partial v/\partial p_i}{\partial v/\partial m}"),
            ("Welfare", r"CV = e(p_1, u_0) - m,\qquad EV = m - e(p_0, u_1)"),
            ("Cost of living", r"\frac{e(p_1,u_0)}{e(p_0,u_0)} \le \frac{p_1\cdot x_0}{p_0\cdot x_0},\qquad "
                               r"\frac{e(p_1,u_1)}{e(p_0,u_1)} \ge \frac{p_1\cdot x_1}{p_0\cdot x_1}"),
            ("AIDS", r"w_i = \alpha_i + \sum_j \gamma_{ij}\log p_j + \beta_i \log\frac{m}{P(p)}"),
        ],
        U=(0, 1, 2, 3, 4, 7, 8, 11, "s08_intermission"), D=(13,), I=(12,),
        also=(("Agora's demand systems", "explainer/economics/agora/demand.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
]
