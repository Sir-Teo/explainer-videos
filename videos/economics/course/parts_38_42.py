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
    Part(
        n=39, level="U", widget="race", prereq=(4, 9, 38),
        question="Why are some people paid so much more than others, and how much of the gap is unfair?",
        story="The part opens on Bertrand and Mullainathan's 4,870 invented resumes, sent to 1,323 advertisements in "
              "Boston and Chicago, and recomputes their result: 9.65% of White-sounding names called back against "
              "6.45% of African-American ones. It then reads the wage distribution since 1979 from the BLS, explains "
              "the college premium with the race between education and technology (and shows why the regression "
              "fails on recent data), plays a game with Autor and Dorn's occupations, builds the task model of "
              "polarization, runs the robots design on the Island, fits the two-way fixed-effects model to a "
              "worker-firm economy with its truth known, and computes Rosen's superstars against the falling labour "
              "share. After an intermission of the college premium, it measures the union premium within workers, "
              "draws Rosen's hedonic wage locus, solves Becker's and Phelps's models of discrimination, measures "
              "discrimination by experiments and by decomposition, and finds the gender gap opening at the first "
              "child; three dials, pay audits, Leontief's horses as Called it?, and pay transparency.",
        handoff="Part 40 widens from wages to incomes, wealth and mobility across generations; Part 41 taxes them; "
                "Part 65 returns to automation with artificial intelligence.",
        outside="Part 4: randomized experiments and regression; Part 9: competitive equilibrium; Part 38: labour "
                "supply, monopsony and selection. Chapter 2 uses a CES production function; chapter 6 two-way fixed "
                "effects; chapter 10 a normal signal-extraction formula; chapter 11 the omitted-variable logic of "
                "Part 38.",
        objectives={
            "U": ["Describe how the US wage distribution changed since 1979 and what polarization means.",
                  "Explain why a randomized correspondence study measures discrimination and a decomposition does not.",
                  "Say what part of the gender gap the child penalty explains."],
            "M": ["Derive the college premium in the canonical model and back out relative demand for a given sigma.",
                  "Solve a three-skill task-assignment model and show what automating middle tasks does to wages.",
                  "Fit a two-way fixed-effects model and explain limited-mobility bias; solve Becker's and Phelps's "
                  "models of discrimination."],
            "D": ["Explain why trend and supply cannot be separated on recent national data, and which designs can.",
                  "Assess bias-corrected estimates of firm effects and sorting."],
            "I": ["Design a pay-equity audit and explain which controls can hide discrimination."],
        },
        results=[
            ("The canonical model", r"\ln\frac{w_H}{w_L} = \Big(1-\frac{1}{\sigma}\Big)\ln\frac{A_H}{A_L} - "
                                    r"\frac{1}{\sigma}\ln\frac{H}{L}"),
            ("AKM", r"\ln w_{it} = \alpha_i + \psi_{J(i,t)} + \varepsilon_{it}"),
            ("Statistical discrimination", r"E[q \mid s] = (1-\lambda)\mu_g + \lambda s, \; "
                                           r"\lambda = \frac{\sigma_q^2}{\sigma_q^2+\sigma_{e,g}^2}"),
            ("Oaxaca-Blinder", r"\bar y_a - \bar y_b = (\bar x_a - \bar x_b)\hat\beta_b + \bar x_a(\hat\beta_a - "
                               r"\hat\beta_b)"),
            ("Becker's market gap", r"\frac{w_{maj}}{w_{min}} - 1 = d^{*}, \text{ the taste of the marginal employer}"),
        ],
        U=(0, 1, 3, 4, "s09_intermission", 8, 9, 11, 12), D=(6, 13, 15), I=(14,),
        also=(("Agora's labour (part II)", "explainer/economics/agora/labour.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
    Part(
        n=40, level="U", widget="tail", prereq=(3, 4, 22, 39),
        question="How unequal are incomes and wealth, why, and do children escape where they started?",
        story="The part opens on Jan Pen's parade of 1971, drawn from Opportunity Insights' family incomes and "
              "Piketty and Saez's tax records: average height arrives at minute 42, and the richest one in ten "
              "thousand are over 600 metres tall. After a game of four numbers it weighs the measures and the ethics "
              "inside Atkinson's index, reads a century of top shares and their U, sets out the dispute over how "
              "much the top pulled away after taxes, derives Pareto tails from random growth with the Kolmogorov "
              "forward equation, shows with Gabaix, Lasry, Lions and Moll why pure random growth is too slow, and "
              "turns to wealth, r against g, and the replies. After an intermission of the top 1% share since 1913, "
              "it builds Kuznets's dual economy and takes his inverted U as Called it?, measures the "
              "intergenerational elasticity with and without averaging, computes the Gatsby curve's mechanism and "
              "its American version across commuting zones, reads rank-rank slopes, the transition matrix and the "
              "fading of absolute mobility, finds the places where poor children rise and the designs that show "
              "places matter, and steps back to the world; two dials, a distributional table and the frontier.",
        handoff="Part 41 asks what taxes do and cost; Part 42 the transfers and insurance of the welfare state; Part "
                "65 returns to wealth taxes and inequality at the frontier.",
        outside="Part 3: Lorenz curves and the Gini; Part 4: regression and natural experiments; Part 22: saving and "
                "wealth; Part 39: the wage structure. Chapter 4 uses a stochastic differential equation and its "
                "Kolmogorov forward equation; chapter 8 the errors-in-variables formula; chapter 11 a "
                "population-weighted Gini.",
        objectives={
            "U": ["Draw a Lorenz curve, compute the Gini and top shares, and say what each measure hides.",
                  "Describe a century of top income shares and why their measurement is disputed.",
                  "Explain rank-rank mobility, absolute mobility and what the Gatsby curve shows."],
            "M": ["Derive the Pareto exponent of random growth with turnover from the Kolmogorov forward equation.",
                  "Show how transitory income attenuates the intergenerational elasticity, and correct it.",
                  "Compute Atkinson's index and the Pareto exponent implied by two top shares."],
            "D": ["Explain why pure random growth is too slow to explain the rise of top incomes, and the repairs.",
                  "Assess what r - g can and cannot explain about the tail of wealth."],
            "I": ["Build a distributional table for a policy and state the four choices behind it."],
        },
        results=[
            ("Atkinson's index", r"A_\varepsilon = 1 - \frac{1}{\bar x}\Big(\frac{1}{n}\sum_i "
                                 r"x_i^{1-\varepsilon}\Big)^{1/(1-\varepsilon)}"),
            ("Pareto from two shares", r"\frac{S(q)}{S(p)} = \Big(\frac{q}{p}\Big)^{1-1/\alpha}"),
            ("Random growth's tail", r"\zeta = \frac{-\nu + \sqrt{\nu^2 + 2\sigma^2\delta}}{\sigma^2}"),
            ("Attenuation", r"\operatorname{plim}\hat\beta_T = \beta\,\frac{\sigma^2_{p}}{\sigma^2_{p} + "
                            r"\sigma^2_{t}/T}"),
            ("Rank-rank", r"E[R_{child} \mid R_{parent}] = \alpha + 0.341\, R_{parent}"),
        ],
        U=(0, 1, 2, 3, "s08_intermission", 7, 9, 10, 11, 12, 13), D=(5, 14, 16), I=(15,),
        also=(("Agora's distribution", "explainer/economics/agora/distribution.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
    Part(
        n=41, level="U", widget="toprate", prereq=(2, 10, 18, 40),
        question="Who really pays a tax, and how high should the top rate be?",
        story="The part opens on Arthur Laffer's napkin of 1974 and the dispute about it, and shows that the top of "
              "his curve depends on one elasticity. It computes who bears a tax on capital as capital becomes "
              "mobile (none to all of it), measures the Harberger triangle as it grows with the square of the rate, "
              "and asks the viewer to set the top rate from three numbers, the Pareto parameter read from the 2022 "
              "tax data. It derives Ramsey's rule on three goods, sets out Mirrlees's information problem and "
              "Diamond's formula, derives the top rate from one small reform, and computes the U-shaped schedule. "
              "After an intermission of the top statutory rate since 1913, it measures the elasticity from a century "
              "of rates and top shares and the 1986 reform, runs Saez's bunching estimator on the Island's taxpayers, "
              "reads Chetty, Looney and Kroft's shelf tags, the case against taxing capital and its unravelling, "
              "profit shifting and the global minimum tax, Allingham and Sandmo's model against Denmark's audit "
              "experiment; three dials, a static and a behavioural score, Mnuchin's 2017 promise as Called it?, and "
              "the frontier.",
        handoff="Part 42 turns to what the state pays out: social insurance, the EITC and cash transfers; Part 58 "
                "returns to tax policy in practice.",
        outside="Part 2: incidence in one market; Part 10: elasticities and pricing; Part 18: welfare weights; Part "
                "40: Pareto tails and top shares. Chapter 1 uses a Cobb-Douglas production function; chapter 4 a "
                "Lagrangian; chapter 6 a first-order condition on a small reform; chapter 9 a polynomial fit.",
        objectives={
            "U": ["Explain why a tax's burden does not depend on who pays it, and who bears the corporate tax.",
                  "Show why deadweight loss grows with the square of the rate.",
                  "State what the elasticity of taxable income measures and why it is partly a policy choice."],
            "M": ["Derive the optimal top rate (1 - g)/(1 - g + a e) from a small reform.",
                  "Derive Ramsey's inverse-elasticity rule for independent goods.",
                  "Compute Diamond's optimal marginal rates and explain the U-shape."],
            "D": ["Estimate an elasticity from bunching at a kink and explain the role of frictions.",
                  "Assess the Chamley-Judd result and Straub and Werning's revision."],
            "I": ["Score a change in the top rate with and without behavioural responses."],
        },
        results=[
            ("The Laffer peak", r"R(t) = t(1-t)^{e} \;\Rightarrow\; t^{*} = \frac{1}{1+e}"),
            ("Harberger's triangle", r"\mathrm{DWL} \approx \tfrac12 t^2 \frac{\varepsilon_d \varepsilon_s}"
                                     r"{\varepsilon_d+\varepsilon_s} pq"),
            ("Ramsey's rule", r"\frac{t_i}{1+t_i} = \frac{k}{\varepsilon_i}"),
            ("The top rate", r"\tau^{*} = \frac{1-g}{1-g+a e}"),
            ("Bunching", r"\hat e = \frac{b}{z^{*}\ln\frac{1-t_0}{1-t_1}}"),
        ],
        U=(0, 1, 2, 3, "s09_intermission", 8, 10, 12, 13), D=(9, 11, 14, 16), I=(15,),
        also=(("Agora's tax", "explainer/economics/agora/tax.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
    Part(
        n=42, level="U", widget="ui", prereq=(7, 13, 22, 24, 41),
        question="What should the state insure, and how generously?",
        story="The part opens on Oregon's 2008 lottery for Medicaid places, drawn as dots: about 90,000 names, "
              "30,000 drawn, 10,000 places. It shows why recessions put a floor under the risk any private pool can "
              "remove, and how much of American unemployment the state's insurance reaches (35% on average since "
              "1967). The viewer sets the Island's unemployment benefit (a third of the wage is best), and the "
              "Baily-Chetty formula is derived and checked exactly at that optimum. A weekly search model shows "
              "the hazard rising as benefits run out; the published durations and consumption drops are put into "
              "the formula, which needs high risk aversion to justify today's benefits, while Chetty's liquidity "
              "share of 60% says they are too low. RAND's experiment and the Island's coinsurance trade-off "
              "(the best plan pays 28% of each bill) lead to Oregon's results and to 200 simulated lotteries that "
              "show why a small effect on blood pressure could not be detected. After an intermission of weekly "
              "claims since 1967, it covers pay-as-you-go arithmetic and the implicit debt, defaults against "
              "subsidies, the examiner design for disability insurance, the negative income tax trials, the 2025 "
              "EITC and tagging, a basic income financed by a flat tax and its trials, the MVPF of the Island's "
              "programmes, three dials, an actuary's arithmetic, the 1983 Social Security reform as Called it?, "
              "and the frontier.",
        handoff="Part 43 opens Act IX, the fields, with industrial organization: measuring market power without "
                "seeing costs.",
        outside="Part 7: risk aversion and defaults; Part 13: adverse selection; Part 22: pay-as-you-go pensions; "
                "Part 24: search and unemployment; Part 41: taxes and the cost of public funds. Chapter 3 uses a "
                "first-order condition with an envelope argument; chapter 7 an instrumental variable.",
        objectives={
            "U": ["Explain why private markets underinsure some risks and what the state can pool.",
                  "State the Baily-Chetty formula and what each side measures.",
                  "Describe what the RAND and Oregon experiments found, and what they could not detect."],
            "M": ["Derive the Baily-Chetty formula from a static model of search with a balanced budget.",
                  "Split the response of search to benefits into liquidity and moral hazard.",
                  "Find the optimal coinsurance rate when insurance raises spending."],
            "D": ["Estimate the effect of coverage from a lottery with incomplete take-up, with its power.",
                  "Use examiner leniency as an instrument and explain why the naive comparison is biased."],
            "I": ["Compute pay-as-you-go replacement rates and the MVPF of a programme."],
        },
        results=[
            ("Baily-Chetty", r"\frac{u'(c_u)-u'(c_e)}{u'(c_e)} = \frac{\varepsilon_{1-e,b}}{e}"),
            ("Its measurable form", r"\gamma\,\frac{\Delta c}{c} \approx \varepsilon"),
            ("Liquidity and moral hazard", r"\frac{de}{db} = \frac{de}{dA} - \frac{de}{dw}"),
            ("Pay-as-you-go", r"\frac{b}{w} = \tau \cdot \frac{\text{workers}}{\text{retirees}}"),
            ("The MVPF", r"\text{MVPF} = \frac{\text{WTP}}{\text{net cost}}"),
        ],
        U=(0, 1, 2, 3, 4, 6, 7, "s09_intermission", 8, 9, 11, 12), D=(5, 10, 13, 14, 16), I=(15,),
        also=(("Agora's insurance", "explainer/economics/agora/insurance.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
]
