"""Act V, The Long Run (Parts 19-24)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=19, level="U", widget="malthus", prereq=(3, 4, 8),
        question="Why was almost everyone poor for almost all of history, and what changed?",
        story="The part opens with the Reverend Thomas Malthus's anonymous Essay of 1798 and seven centuries of English "
              "real wages that obey it until just after he wrote. The viewer guesses when England's income per head "
              "began to climb, then derives the Malthusian model and runs it on the island with a plague and a better "
              "plough, tests it on England's labour demand curve, and watches the Black Death run the mechanism "
              "backwards. After the arguments over why Britain and why not China, and an intermission of two "
              "centuries of divergence and convergence, the part measures the Industrial Revolution and Engels's "
              "pause, follows the demographic transition, runs a unified growth model from the year 1000, asks whether "
              "the escape was good by way of heights and hours, opens a dial on growth before the escape, scores "
              "Ehrlich's Population Bomb, and ends with deep roots and the spatial noise that can fake them.",
        handoff="Part 20 asks what capital can do for growth; Part 21 what ideas can; Part 46 returns to development and "
                "the dial; Part 47 to institutions; Part 48 to population and the climate.",
        outside="Part 3: GDP per head and real wages; Part 4: regression and standard errors; Part 8: diminishing "
                "returns. Chapter 2 uses a first-order difference equation and its steady state; chapter 3 a log-log "
                "regression with Newey-West errors; chapter 9 a household's optimum found numerically.",
        objectives={
            "U": ["Explain the Malthusian trap with diminishing returns and a population that follows income, and why "
                  "better technology raised population rather than income.",
                  "Read England's wages, population and income from 1270 to today, and describe the Black Death, the "
                  "Industrial Revolution and the demographic transition with their numbers.",
                  "State the main explanations of why the escape began in Britain, with their critics."],
            "M": ["Derive the Malthusian steady state and the speed of convergence; estimate a labour demand curve "
                  "from historical data with standard errors that allow for serial correlation.",
                  "Solve the Galor-Weil household's education choice and its threshold, and show Kremer's scale "
                  "effect."],
            "D": ["Weigh historical reconstructions of living standards against each other, and recognize spatial "
                  "noise in persistence regressions."],
            "I": ["Read and use long-run population and income projections, and the record of past forecasts."],
        },
        results=[
            ("The Malthusian steady state", r"y^* = \bar y,\quad L^* = X\,(A/\bar y)^{1/\beta}"),
            ("Convergence after a shock", r"\dot\ell = -\lambda\beta\,\ell,\ \ t_{1/2} = \ln 2/(\lambda\beta)"),
            ("England's labour demand curve, 1270-1640", r"\partial \ln w / \partial \ln L \approx -0.9"),
            ("Galor and Weil's threshold", r"e > 0 \iff g > \rho^2\tau/(1-\rho)"),
            ("Kremer's scale effect", r"\dot L / L = (\phi/\beta)\, L"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, "s08_intermission", 7, 8, 9, 10), D=(11, 13), I=(12,),
        also=(("Agora's long-run module", "explainer/economics/agora/malthus.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
    Part(
        n=20, level="U", widget="solow", prereq=(3, 7, 8, 19),
        question="Can a country save its way to being rich?",
        story="The part opens with the two Koreas, the richer north of 1940 and the south twenty-six times richer by "
              "2022, and asks what saving can do. It checks Kaldor's six facts on the Penn World Table, runs Harrod "
              "and Domar's knife edge and Easterly's test of the financing gap, derives Solow's model and lets the "
              "viewer choose the island's saving rate for a century, finding the golden rule. It works out the speed "
              "of convergence and tests it across countries, absolute and conditional, with Mankiw, Romer and Weil's "
              "regression refitted; then an intermission of investment and income for 146 countries. Growth and "
              "development accounting find the residual large in time and larger across countries; East Asia, "
              "Samuelson's Soviet forecast and Lucas's puzzle follow. Ramsey's problem is solved by shooting, China "
              "is put in the model, a dial on the speed of convergence opens, and the part ends with potential "
              "output, the slowdown since 2005 and convergence since 2000.",
        handoff="Part 21 explains the residual with ideas and institutions; Part 22 builds the Euler equation into a "
                "theory of consumption; Part 30 uses the neutral rate; Part 46 returns to convergence and its dial; "
                "Part 48 puts Ramsey's machinery to work on the climate.",
        outside="Part 3: national accounts and the Penn World Table; Part 7: the Euler equation; Part 8: the "
                "Cobb-Douglas production function and capital's share; Part 19: the long run before 1800. Chapter 5 "
                "linearizes a differential equation; chapter 6 runs cross-country regressions with robust standard "
                "errors; chapter 11 uses a Hamiltonian and solves a boundary-value problem by shooting.",
        objectives={
            "U": ["Derive the Solow model's steady state and show that saving raises the level of income, not its "
                  "long-run growth rate; find the golden rule.",
                  "Read Kaldor's facts, growth accounting and development accounting on the Penn World Table, and "
                  "explain what the residual is and is not.",
                  "State the evidence on convergence, absolute and conditional, and the argument over East Asia."],
            "M": ["Linearize the Solow model to find the speed of convergence, and estimate it by cross-country "
                  "regression with and without controls.",
                  "Set up the Ramsey-Cass-Koopmans problem with a Hamiltonian, derive the Euler equation and the "
                  "modified golden rule, and find the saddle path by shooting."],
            "D": ["Weigh cross-section against panel estimates of convergence, and the quantity-based against the "
                  "price-based residual."],
            "I": ["Build a potential-output projection from growth accounting, and read debt dynamics with r and g."],
        },
        results=[
            ("The Solow steady state", r"k^* = \big(s/(n+g+\delta)\big)^{1/(1-\alpha)},\quad K/Y = s/(n+g+\delta)"),
            ("The golden rule", r"f'(k_{\text{gold}}) = n+g+\delta \iff s = \alpha"),
            ("The speed of convergence", r"\lambda = (1-\alpha)(n+g+\delta)"),
            ("Growth accounting", r"g_A = g_Y - \alpha g_K - (1-\alpha)(g_L + g_h)"),
            ("Development accounting", r"y = (K/Y)^{\alpha/(1-\alpha)}\, h\, A^{1/(1-\alpha)}"),
            ("The modified golden rule", r"f'(k^*) - \delta = \rho + \theta g"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, "s08_intermission", 7, 8, 9, 10, 12), D=(11, 13, 15), I=(14,),
        also=(("Agora's growth module", "explainer/economics/agora/growth.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
    Part(
        n=21, level="U", widget="misallocation", prereq=(4, 9, 15, 20),
        question="Where does the growth that capital cannot explain come from?",
        story="The part opens with William Nordhaus's history of the price of light and asks the viewer what an hour "
              "of light cost in 1992. It explains why ideas, being non-rival, bring increasing returns and need "
              "monopoly or public money; runs the AK model and learning by doing; derives Romer's economy and its "
              "scale effect; builds Aghion and Howitt's quality ladder and finds when the market does too much "
              "research or too little; scores Romer's scale effect against Bloom, Jones, Van Reenen and Webb's "
              "evidence that ideas are getting harder to find; and measures slow diffusion. After an intermission "
              "of two centuries of light, it measures misallocation on the Island's plants, refits Acemoglu, Johnson "
              "and Robinson's settler-mortality instrument with its critics, reads borders as experiments, weighs "
              "geography, disease and culture, models directed technical change, reviews the evidence on patents, "
              "opens a dial on the social return to R&D, and ends with growth when populations shrink.",
        handoff="Part 22 turns to consumption and saving; Parts 43 and 44 return to market power and the spread of "
                "productivity; Part 46 to development; Part 47 to institutions; Part 65 to the economics of AI.",
        outside="Part 4: instrumental variables and regression discontinuity; Part 9: the efficiency of competitive "
                "allocations; Part 15: public goods; Part 20: the Solow model and the residual. Chapter 4 solves a "
                "balanced growth path; chapter 5 uses Poisson arrivals; chapter 8 a lognormal moment.",
        objectives={
            "U": ["Explain why non-rival ideas bring increasing returns and why they need monopoly, public money or "
                  "prizes; read the price of light.",
                  "Describe Romer's and Aghion and Howitt's models and what they say about whether markets do enough "
                  "research.",
                  "State the evidence on ideas getting harder to find, diffusion, misallocation and institutions, "
                  "with its critics."],
            "M": ["Derive Romer's balanced growth rate and the semi-endogenous growth rate; solve the market's and a "
                  "planner's research in a quality-ladder model.",
                  "Derive Hsieh and Klenow's misallocation formula, and estimate an instrumental-variables regression "
                  "of income on institutions."],
            "D": ["Weigh the identification of institutional effects (settler mortality, borders, discontinuities) "
                  "against their critiques."],
            "I": ["Read evaluations of R&D tax credits, and the evidence on the social return to research."],
        },
        results=[
            ("Romer's balanced growth", r"g = \frac{\alpha\delta L - \rho}{\alpha + \theta}"),
            ("Semi-endogenous growth", r"g_A = \frac{\lambda n}{1-\phi}"),
            ("The quality ladder", r"E\,\dot{\ln A} = \lambda n \ln\gamma"),
            ("Misallocation", r"\ln\frac{Y_{\text{eff}}}{Y} = \frac{\sigma}{2}\operatorname{var}(\ln \text{TFPR})"),
            ("Directed technical change", r"\frac{w_H}{w_L} \propto (H/L)^{\sigma - 2}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, "s09_intermission", 8, 9, 10, 11, 12, 13), D=(14, 16), I=(15,),
        also=(("Agora's ideas module", "explainer/economics/agora/ideas.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
    Part(
        n=22, level="U", widget="bufferstock", prereq=(4, 7, 20),
        question="How do households decide how much to spend today?",
        story="The part opens with the 2001 US tax rebates, mailed in an order set by a digit of each taxpayer's "
              "Social Security number, and asks the viewer how much of each dollar went on nondurables within the "
              "quarter. It sets Keynes's consumption function against Kuznets's long series and runs Friedman's "
              "answer on the Island's 10,000 households; derives permanent income and the life cycle from the Euler "
              "equation; tests Hall's random walk on sixty years of US data; estimates the share of rule-of-thumb "
              "households; solves the buffer-stock household by the endogenous grid method; and reads the rebate "
              "experiments and Alaska's dividend, scoring Hall's prediction. After an intermission of income and "
              "spending month by month, it shows the wealthy hand-to-mouth, sets the viewer's own answer against "
              "surveys and lottery winners, tests Ricardian equivalence, builds overlapping generations and asks "
              "when a pension is a free lunch, takes up the saving of the rich and of China, opens a dial on the "
              "propensity to spend a windfall, and ends with spending through unemployment in bank-account data.",
        handoff="Part 23 prices the claims that savings buy; Part 27 builds the multiplier; Part 32 designs fiscal "
                "stimulus; Part 42 returns to pensions; Part 45 to present bias; Part 52 builds economies of "
                "buffer-stock households.",
        outside="Part 4: instrumental variables and errors in variables; Part 7: the Euler equation and prudence; "
                "Part 20: the golden rule. Chapter 4 uses an F test; chapter 6 iterates on a grid; chapter 11 solves "
                "a difference equation.",
        objectives={
            "U": ["State Keynes's consumption function, Kuznets's puzzle and Friedman's answer; explain why a "
                  "forward-looking household spends only the annuity value of a windfall.",
                  "Describe the rebate experiments and what they show about the propensity to spend, and who spends "
                  "most.",
                  "Explain Ricardian equivalence and why it fails; explain when a pay-as-you-go pension raises "
                  "welfare."],
            "M": ["Derive permanent income from the Euler equation and the budget; derive Hall's random walk and "
                  "test it, allowing for time averaging.",
                  "Solve a buffer-stock household by the endogenous grid method and compute its marginal propensity "
                  "to consume; estimate Campbell and Mankiw's share by instrumental variables."],
            "D": ["Weigh the evidence on the marginal propensity to consume from experiments, account data and "
                  "surveys, and what two-asset models add."],
            "I": ["Design a stimulus payment and a pension default from the evidence on who spends and who saves."],
        },
        results=[
            ("Permanent income", r"c = \frac{r}{1+r}\Big(A_0 + \sum_{t\ge0}\frac{\mathbb{E}\,y_t}{(1+r)^t}\Big)"),
            ("Hall's random walk", r"c_{t+1} = c_t + \varepsilon_{t+1}"),
            ("Friedman's slope", r"\frac{\sigma_p^2}{\sigma_p^2 + \sigma_t^2}"),
            ("The buffer stock", r"c(m)^{-\gamma} = \beta R\,\mathbb{E}\big[(G\psi' c(m'))^{-\gamma}\big]"),
            ("Dynamic inefficiency", r"R < 1 + n"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, "s09_intermission", 8, 9, 10, 11, 12), D=(13, 15), I=(14,),
        also=(("Agora's household module", "explainer/economics/agora/household.py"),
              ("Agora's overlapping generations", "explainer/economics/agora/olg.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
    Part(
        n=23, level="U", widget="tree", prereq=(7, 20, 22),
        question="What is a claim on the future worth, and how does that decide what gets built?",
        story="The part opens with Mehra and Prescott's two numbers: a model premium of a third of a point against "
              "six in the record. It values a growing stream of dividends and shows how sensitive long-lived assets "
              "are to the discount rate; builds investment from the user cost, Tobin's q and adjustment costs, run on "
              "the Island's firm; prices the option to wait; and slices Modigliani and Miller's pie. The viewer then "
              "prices a coconut tree, and the part derives the stochastic discount factor from the Lucas tree, "
              "measures the consumption CAPM on Shiller's century of data, computes the equity premium puzzle three "
              "ways and tries three repairs. After an intermission following a dollar in stocks and in bonds since "
              "1871, it tests excess volatility and predictability, shows bubbles in theory and in the laboratory, "
              "scores Irving Fisher's 1929 forecast, treats housing as an asset, reads two dials, and ends with the "
              "return on everything.",
        handoff="Part 24 turns to the labour market; Parts 26 and 33 to banks and crises; Part 31 to low interest "
                "rates; Part 32 to public debt; Part 40 to the return on wealth and inequality; Part 45 to behavioural "
                "finance; Quant, Built treats the evidence on asset pricing in depth.",
        outside="Part 7: expected utility, risk aversion and the Euler equation; Part 20: the golden rule; Part 22: "
                "dynamic inefficiency. Chapter 3 uses a geometric Brownian motion; chapter 8 a two-state Markov chain.",
        objectives={
            "U": ["Value a growing stream with the Gordon formula and explain why long-lived assets are sensitive to "
                  "the discount rate.",
                  "Explain the user cost of capital, Tobin's q, the option to wait and the Modigliani-Miller theorem.",
                  "State the equity premium puzzle and the three leading repairs."],
            "M": ["Derive asset prices from the stochastic discount factor: the risk-free rate, risk premia as "
                  "covariance, and the Hansen-Jagannathan bound.",
                  "Solve Mehra and Prescott's economy and a rare-disaster economy, and compute their premia."],
            "D": ["Weigh the evidence on excess volatility, predictability and bubbles, and on the response of "
                  "investment to its cost."],
            "I": ["Apply the NPV rule, terminal values and pension discount rates, and say which discount rate each "
                  "needs."],
        },
        results=[
            ("The Gordon formula", r"P = \frac{D_1}{r - g}"),
            ("Investment and q", r"\frac{I}{K} = \frac{q - 1}{\phi}"),
            ("The pricing equation", r"p = \mathbb{E}[m x], \quad m = \beta \frac{u'(c_{t+1})}{u'(c_t)}"),
            ("Risk premia", r"\mathbb{E}[R] - R_f = -R_f \operatorname{cov}(m, R)"),
            ("Hansen-Jagannathan", r"\frac{\sigma(m)}{\mathbb{E}(m)} \ge \frac{|\mathbb{E}[R - R_f]|}{\sigma(R - R_f)}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "s11_intermission", 10, 11, 12), D=(13, 15), I=(14,),
        also=(("Agora's asset prices and investment", "explainer/economics/agora/assets.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
    Part(
        n=24, level="U", widget="labour", prereq=(2, 11, 22),
        question="Why are there unemployed workers and unfilled jobs at the same time?",
        story="The part opens on Peter Diamond's coconut island, where climbing a palm pays only if others climb too, "
              "and then puts the two numbers side by side: millions of openings and millions of unemployed people in "
              "the same month. It shows the gross flows behind the small net change, lets the viewer choose a "
              "stopping rule for job offers, and derives McCall's reservation wage; draws the American Beveridge "
              "curve from JOLTS and the soft-landing debate of 2022; animates the matching function with urns and "
              "balls and estimates it; derives the Diamond-Mortensen-Pissarides model, Nash bargaining and the "
              "Hosios condition on the Island. After an intermission tracing the Beveridge curve month by month, it "
              "meets the volatility puzzle and its repairs, scores Mortensen and Pissarides's 1994 claim, splits "
              "unemployment's swings into ins and outs, climbs job ladders, measures the natural rate and the scars "
              "of job loss, reads two dials, and ends with online vacancies and remote work.",
        handoff="Part 25 opens Act VI with money, itself a search problem; Part 28 returns to the natural rate and the "
                "Phillips curve; Part 29 puts search into the business cycle; Part 38 measures monopsony and the "
                "minimum wage; Part 42 designs unemployment insurance.",
        outside="Part 2: supply and demand; Part 7: discounting and expected values; Part 11: Nash's bargaining "
                "solution and Rubinstein's game; Part 22: liquidity and spending. Chapter 10 uses the HP filter.",
        objectives={
            "U": ["Explain unemployment as a stock with flows in and out, and compute the steady-state rate from the "
                  "two flows.",
                  "Derive the reservation wage and explain how benefits and patience move it.",
                  "Read the Beveridge curve: movements along it and shifts of it."],
            "M": ["Derive the DMP model: job creation, the Nash wage, tightness, and unemployment and vacancies in a "
                  "steady state; derive its comparative statics.",
                  "State and prove the Hosios condition, and estimate the matching elasticity from data."],
            "D": ["Explain the volatility puzzle, its repairs and the fundamental surplus, and weigh the evidence on "
                  "the matching elasticity and the worker's bargaining share."],
            "I": ["Read a labour-market dashboard (flows, quits, tightness) and explain how job platforms change "
                  "matching efficiency."],
        },
        results=[
            ("Steady-state unemployment", r"u^* = \frac{s}{s + f}"),
            ("The reservation wage", r"w^* - b = \frac{\beta}{1-\beta} \int_{w^*} (w - w^*)\, dF(w)"),
            ("The matching function", r"M = A U^{\eta} V^{1-\eta}, \quad f = A\theta^{1-\eta}"),
            ("Job creation and the wage", r"\frac{c}{q(\theta)} = \frac{p - w}{r + s}, \quad w = (1-\beta) b + "
                                           r"\beta (p + c\theta)"),
            ("The fundamental surplus", r"\frac{d\ln\theta}{d\ln p} = \frac{r + s + \beta f}{\eta(r+s) + \beta f}"
                                        r"\cdot\frac{p}{p - b}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, "s10_intermission", 9, 10, 11, 12), D=(13, 15), I=(14,),
        also=(("Agora's labour market with frictions", "explainer/economics/agora/search.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
]
