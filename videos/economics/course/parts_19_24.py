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
]
