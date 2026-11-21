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
    Part(
        n=52, level="M", widget="households", prereq=(22, 26, 30, 40, 51),
        question="What does macroeconomics get wrong by treating a country as one household?",
        story="The part opens on Alan Kirman's 1992 essay asking whom or what the representative individual "
              "represents (it 'deserves a decent burial'), on Krusell and Smith's 1998 finding that their economy's "
              "aggregates are almost perfectly described by the mean of the wealth distribution, and on Kaplan, Moll "
              "and Violante's reversal of the textbook account of monetary policy. Gorman's condition and MPCs that "
              "fall with wealth; Bewley's and Huggett's households, whose uninsured risk pushes the interest rate "
              "below time preference; Aiyagari's economy derived and solved, with 33% more capital than one "
              "household would hold; the Island's 100,000 households against Young's histogram and Aiyagari's table "
              "recomputed. The viewer guesses which fifth of households spends most after a rate cut (the second; "
              "the poorest almost entirely through incomes). The wealth distribution's top, missed by the simple "
              "model and reached by lucky returns; Krusell and Smith's algorithm, fit and Den Haan's test. After an "
              "intermission of the top 1%'s and poorer half's shares of US wealth since 1989, continuous time as one "
              "sparse matrix and its transpose; HANK's direct and indirect effects against a representative "
              "household; sequence-space Jacobians by fake news, against brute force; multipliers, forward guidance "
              "and who gains from inflation; Hopenhayn's industry and lumpy plants; the MPC dial against the models; "
              "distributions at the central bank, Krusell and Smith as Called it?, and micro data in macro models.",
        handoff="Part 53 turns from what households have to what they know: games of incomplete information, cheap "
                "talk, and the design of information itself.",
        outside="Part 22: consumption and the MPC; Part 26: banks and liquidity; Part 30: the New Keynesian model; "
                "Part 40: the wealth distribution; Part 51: the methods; Statistics, Built: Markov chains and "
                "stationary distributions.",
        objectives={
            "U": ["Explain when a representative household is exact (Gorman) and why differing MPCs break it.",
                  "Explain why uninsurable risk lowers the interest rate and raises saving."],
            "M": ["Solve Aiyagari's and Huggett's economies, with the stationary distribution by Young's method or the "
                  "Kolmogorov forward equation, and simulate a population.",
                  "Run Krusell and Smith's algorithm and judge its rule by R-squared and Den Haan's test.",
                  "Compute sequence-space Jacobians by the fake-news algorithm and use them to split a rate cut into "
                  "direct and indirect effects and to compute multipliers."],
            "D": ["Prove the fake-news recursion and the balanced-budget multiplier of the intertemporal Keynesian "
                  "cross; derive Hopenhayn's stationary industry.",
                  "State what remains open: estimation with micro data, heterogeneous beliefs, nonlinear aggregate "
                  "risk."],
            "I": ["Write a distributional analysis of a policy: equilibrium paths, every household's response, and "
                  "the change by group, reported beside its assumptions."],
        },
        results=[
            ("Gorman", r"c_i = a_i(p) + b(p)\, m_i \Rightarrow \textstyle\sum_i c_i = \sum_i a_i(p) + b(p)\sum_i m_i"),
            ("Aiyagari's market", r"K(r) = \int a\, d\lambda_r(a, e),\quad r = \alpha K^{\alpha - 1} - \delta"),
            ("The forward equation", r"\mathbf{A}^{\top}\mathbf{g} = 0"),
            ("Direct and indirect", r"dC = \mathbf{M}_r\, dr + \mathbf{M}_Z\, dZ"),
            ("Fake news", r"\mathbf{J}_{t,s} = \mathbf{F}_{t,s} + \mathbf{J}_{t-1,s-1}"),
        ],
        U=(0, 1, 2, 5, "s09_intermission"), D=(10, 12), I=(14,),
        also=(("Agora's many agents", "explainer/economics/agora/hetero.py"),
              ("The Island's planted truths", "explainer/economics/island.py")),
    ),
    Part(
        n=53, level="M", widget="persuade", prereq=(11, 13, 26, 34, 51),
        question="How does someone who controls only what others learn get them to do what she wants?",
        story="The part opens on Kamenica and Gentzkow's prosecutor: 30% of defendants guilty, a judge who convicts "
              "only if guilt is more likely than not, and an investigation that flags every guilty defendant and 3 "
              "in 7 of the innocent, convicting 60% with nobody deceived. The viewer designs the investigation. "
              "Harsanyi's Bayesian games on a Cournot duopoly with an unknown rival; perfect Bayesian equilibrium "
              "and Cho and Kreps's beer and quiche; Crawford and Sobel's cheap talk; Bayesian persuasion as "
              "concavification; Bergemann and Morris's information design for two investors; Blackwell's order. "
              "After an intermission of Michigan households' expected inflation against the actual since 1978, "
              "Aumann's agreement theorem, Geanakoplos and Polemarchakis's dialogue and Rubinstein's email game; "
              "global games; cascades; Kreps and Wilson's chain store; Nash, Rubinstein and Coase on bargaining; "
              "Levin's relational contracts; the reasoning-depth dial and DellaVigna and Kaplan's persuasion rate; "
              "information designers in practice, the 2006 triple-A ratings as Called it?, and robust design.",
        handoff="Part 54 turns from what people know to what economists can measure: estimating models from the "
                "choices they predict.",
        outside="Part 11: games and correlated equilibrium; Part 13: signalling; Part 26: bank runs; Part 34: "
                "currency attacks; Statistics, Built: Bayes's rule and the value of information.",
        objectives={
            "U": ["Explain how an investigation that cannot lie can still shift decisions, using Bayes's rule.",
                  "Explain why talk is informative only when interests are close enough."],
            "M": ["Solve Bayesian games and find perfect Bayesian equilibria, applying the intuitive criterion.",
                  "Compute a sender's optimal signal by concavification, and Bayes correlated equilibria by linear "
                  "programming.",
                  "Derive Crawford and Sobel's partitions, a global game's threshold and a cascade's odds."],
            "D": ["Prove Blackwell's theorem in the binary case, the uniform belief of the global game's marginal "
                  "player, and Rubinstein's bargaining solution.",
                  "State the open problems of robust and algorithmic information design."],
            "I": ["Design a disclosure policy (a rating, an alert, a stress test) and test it against receivers who "
                  "reason less deeply than the theory assumes."],
        },
        results=[
            ("Bayes plausibility", r"\sum_k \tau_k \mu_k = \mu_0"),
            ("The value of persuasion", r"V(\mu_0) = \operatorname{cav}\, v(\mu_0)"),
            ("Cheap talk", r"a_i = \tfrac{i}{N} + 2 b\, i\, (i - N)"),
            ("Global games", r"\theta^* = 1 - c"),
            ("Rubinstein", r"x^* = \frac{1 - \delta_2}{1 - \delta_1 \delta_2}"),
        ],
        U=(0, 1, 5, "s09_intermission"), D=(7, 9), I=(15,),
        also=(("Agora's information and persuasion", "explainer/economics/agora/persuade.py"),
              ("The Island's planted truths", "explainer/economics/island.py")),
    ),
]
