"""Act X, The Graduate Core (Parts 51-56)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=51, level="M", widget="solver", prereq=(22, 29, 30, 44),
        question="How is an economy that has no formula solved, and how do you know the answer is right?",
        story="The part opens on Richard Bellman's account of naming dynamic programming at RAND, a name 'not even a "
              "Congressman could object to', and on value iteration settling on the growth model of Part 29. The "
              "Bellman operator is a contraction (a cobweb, Banach's theorem, distances shrinking by beta, "
              "Blackwell's two conditions checked); Howard's policy iteration reaches the same policy in a handful "
              "of rounds by a sparse solve. The viewer chooses which of three grids reports the steady state to "
              "within 1%; interpolation, Runge's warning and Chebyshev's nodes; Carroll's endogenous grid method on "
              "Part 22's household, far faster and more accurate than value iteration; Judd's projection with its "
              "spectral convergence; perturbation to second order, and the precautionary saving that certainty "
              "equivalence cannot see. After an intermission of transistors per microprocessor since 1971, "
              "Euler-equation errors and eight methods compared; Tauchen against Rouwenhorst and quadrature against "
              "simulation; the HJB equation by Achdou et al.'s upwind scheme with its stationary distribution; the "
              "household's kink and the zero bound by guess and verify; Smolyak's sparse grids; the report, seeds "
              "and known answers of a reproducible computation; the EIS dial against method error; model teams, "
              "estimation loops, Moore's 1965 forecast as Called it?, and solvers that differentiate.",
        handoff="Part 52 puts these methods to work on a whole population of households: what macroeconomics gets "
                "wrong by treating a country as one household.",
        outside="Part 22: the household's saving; Part 29: the growth model; Part 30: the zero bound; Part 44: the "
                "nested fixed point; Statistics, Built: optimization, Monte Carlo and reproducible computation.",
        objectives={
            "U": ["Explain why repeating Bellman's equation converges, and why a coarse grid can bias an answer.",
                  "Read an Euler-equation error as a mistake in dollars."],
            "M": ["Solve a dynamic model by value and policy iteration, with interpolation, by the endogenous grid "
                  "method, by collocation and by perturbation, and compare them by Euler errors.",
                  "Discretize a persistent process, compute expectations by quadrature, and solve an HJB equation by "
                  "upwind finite differences.",
                  "Handle an occasionally binding constraint by guess and verify."],
            "D": ["Prove Blackwell's sufficient conditions, and derive the implicit derivative of a solution with "
                  "respect to a parameter.",
                  "State the open problems of high-dimensional solution methods: certified accuracy, sequence-space "
                  "methods, neural-network solvers."],
            "I": ["Write a solution report and a replication package another team can run."],
        },
        results=[
            ("The Bellman operator", r"(TV)(k) = \max_{k'}\, u(f(k) - k') + \beta V(k')"),
            ("Contraction", r"\lVert TV - TW \rVert \le \beta\, \lVert V - W \rVert"),
            ("The endogenous grid", r"c = \big(\beta R\, \mathbb{E}[u'(c')]\big)^{-1/\gamma},\ a = (c + a' - y)/R"),
            ("Euler-equation error", r"\log_{10}\Big|1 - \frac{u'^{-1}(\beta\,\mathbb{E}[u'(c')R'])}{c}\Big|"),
            ("Smolyak, level 2", r"1 + 4d + 2d(d-1)\ \text{points}"),
        ],
        U=(0, 1, 3, 8, "s09_intermission"), D=(12, 16), I=(13, 15),
        also=(("Agora's solver harness", "explainer/economics/agora/solve.py"),
              ("The Island's planted truths", "explainer/economics/island.py")),
    ),
]
