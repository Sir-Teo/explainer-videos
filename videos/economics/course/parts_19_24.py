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
]
