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
    Part(
        n=54, level="M", widget="estimate", prereq=(4, 5, 7, 22, 44, 51),
        question="How is a model's hidden machinery measured from the choices it predicts?",
        story="The part opens on BART: an official forecast of about 15% of work trips, Daniel McFadden's 6.3% from "
              "a model of commuters' choices, and 6.2% in 1975. On the Island, where the truth is planted: a straight "
              "line through a fuel-price history predicts a negative share of drivers under a congestion charge, a "
              "logit does not; McFadden's logit by maximum likelihood, the value of time, and a railway forecast "
              "undone by the independence of irrelevant alternatives. The viewer asks which of four facts separates "
              "patience from caution (none). Hansen's GMM on the Euler equation with the J-test; simulated moments "
              "and indirect inference; the life-cycle household estimated by simulated moments with the truth "
              "recovered on a narrow ridge. After an intermission of America's vehicle miles since 1971, hidden "
              "types and spurious habit, Andrews, Gentzkow and Shapiro's sensitivity matrix and a 1% error in "
              "wealth worth 38 standard errors, calibration against estimation, Chetty's sufficient statistics, "
              "Todd and Wolpin's validation, Manski's bounds, the risk-aversion dial, estimation at work, Google "
              "Flu Trends as Called it?, and learned estimators.",
        handoff="Part 55 turns from people's choices to an economy's one history: identifying the effects of "
                "monetary and fiscal policy.",
        outside="Part 4: the Lucas critique and instruments; Part 5: random utility; Part 22: the life-cycle "
                "household; Part 42: sufficient statistics; Part 44: Rust's buses; Statistics, Built: likelihood, "
                "GMM, the bootstrap and partial identification.",
        objectives={
            "U": ["Explain why a forecast of a new policy needs a model of why people choose, not a pattern in "
                  "history.",
                  "Read a value of time off a logit's coefficients."],
            "M": ["Estimate a logit by maximum likelihood and a model by GMM, with standard errors and the J-test.",
                  "Estimate a model you can only simulate, by simulated moments or indirect inference.",
                  "Diagnose weak identification and compute the sensitivity of an estimate to its moments."],
            "D": ["Derive the efficient GMM weighting and the (1 + 1/S) correction, and the spurious state "
                  "dependence a hidden type creates.",
                  "Derive Manski's bounds and narrow them with a monotonicity assumption."],
            "I": ["Estimate demand for a new product or service and say which facts in the data the forecast leans "
                  "on, before anyone acts on it."],
        },
        results=[
            ("The logit", r"\Pr(j) = \frac{e^{V_j}}{\sum_k e^{V_k}}"),
            ("Efficient GMM", r"\operatorname{Var}(\hat\theta) \approx \tfrac{1}{n}\left(G' S^{-1} G\right)^{-1}"),
            ("Hansen's J", r"J = n\, \bar g' S^{-1} \bar g \sim \chi^2_{m-k}"),
            ("Sensitivity", r"\Lambda = -\left(G'WG\right)^{-1} G'W"),
            ("Manski's bounds", r"\text{width} = p_1 + p_0"),
        ],
        U=(0, 1, 2, "s08_intermission"), D=(8, 12), I=(14,),
        also=(("Agora's estimation harness", "explainer/economics/agora/estimate.py"),
              ("The Island's planted truths", "explainer/economics/island.py")),
    ),
    Part(
        n=55, level="M", widget="identify", prereq=(28, 29, 30, 31, 32, 54),
        question="With one history and no control group, how can anyone say what a policy did?",
        story="The part opens on Sims's price puzzle, recomputed from FRED data: a monthly VAR of production, prices "
              "and the funds rate, 1965-1995, says prices rise for three years after a hike, until commodity prices "
              "are added. A VAR alone knows six numbers and needs nine; three rotations of one Island history tell "
              "three stories. The viewer picks the monetary tightening from three unlabelled responses. Five schemes "
              "(timing, the long run, signs, an outside instrument, a change in variance) are run on the Island's "
              "structural VAR, where the truth is known, on one history and on 300; local projections against VARs; "
              "narrative and high-frequency instruments cure Part 31's price puzzle. After an intermission of the "
              "yield curve's slope since 1953, Part 30's model is estimated by the Kalman filter and "
              "Metropolis-Hastings, then without the rate observed, its posteriors mostly prior; regions and the "
              "missing intercept; shift-share designs; impulse-response matching; forecasts at the turns and what "
              "macroeconomics knows; the monetary-shock and multiplier dials; research departments and the "
              "frontier.",
        handoff="Part 56 closes the graduate core with the examination: twelve problems in micro, macro and "
                "econometrics, solved the way a grader wants to see them.",
        outside="Part 28: the Lucas critique; Part 29: Gali's long-run VAR; Part 30: the New Keynesian model; Part 31: "
                "narrative and high-frequency shocks; Part 32: local projections and regional multipliers; Part 54: "
                "estimation and identification; Statistics, Built: time series, the Kalman filter and Bayesian "
                "computation.",
        objectives={
            "U": ["Explain why a correlation between interest rates and prices cannot by itself say what policy did.",
                  "Read an impulse response and say what assumption produced it."],
            "M": ["Estimate a VAR and identify a shock by timing, long-run, sign, instrument and variance "
                  "restrictions.",
                  "Estimate impulse responses by local projections and compare them with a VAR's.",
                  "Estimate a small DSGE model by the Kalman filter and Metropolis-Hastings, and check its posteriors "
                  "against its priors."],
            "D": ["Prove that an external instrument and a variance change each identify a column of the impact "
                  "matrix, and that projections and VARs share an estimand.",
                  "Diagnose weak identification by likelihood profiles."],
            "I": ["Brief a policy committee on what the last rate rise did, with the identifying assumption of "
                  "each estimate stated."],
        },
        results=[
            ("Order condition", r"\tfrac{n(n-1)}{2} \text{ restrictions beyond } \Sigma = BB'"),
            ("An external instrument", r"b_m \propto \operatorname{Cov}(u_t, z_t)"),
            ("A change in variance", r"\Sigma_1 - \Sigma_0 = (\sigma_1^2 - \sigma_0^2)\, b_m b_m'"),
            ("Local projection", r"y_{t+h} = \alpha_h + \beta_h z_t + \gamma_h' w_t + e_{t+h}"),
            ("The missing intercept", r"y_{rt} - \bar y_t = m_\ell (g_{rt} - \bar g_t) + \varepsilon_{rt}"),
        ],
        U=(0, 1, 2, "s08_intermission"), D=(3, 8), I=(13,),
        also=(("Agora's macro-econometrics", "explainer/economics/agora/macrometrics.py"),
              ("The Island's planted truths", "explainer/economics/island.py")),
    ),
    Part(
        n=56, level="M", widget="exam", prereq=(6, 15, 16, 14, 20, 24, 30, 52, 4, 54, 55),
        question="Can you do it with the book closed?",
        story="The night before the first-year examinations: an envelope with three papers, and where the core came "
              "from (Samuelson's Foundations, Mas-Colell, Whinston and Green, Ljungqvist and Sargent, Hayashi, "
              "Gali). Twelve questions, each with a pause before its solution and the mistakes that cost marks: a "
              "consumer at an increasing block tariff (demand by segments, Slutsky with virtual income, the "
              "compensating variation), an exchange economy with smoke (the Pareto line and Pigou's tax, with an "
              "is/ought card), a first-price auction with a reserve (the boundary beta(r) = r, revenue 5/12 and a "
              "simulation), screening with two types and a continuum, a capital tax in the Ramsey model (the phase "
              "diagram and the jump), benefits that expire (backward induction and the exit spike's evidence); after "
              "an intermission of the median duration of unemployment since 1967, discretion and commitment, why "
              "r < rho in Aiyagari's economy, storms that identify a demand curve, GMM for the Euler equation with "
              "its J test, staggered timing where two-way fixed effects halves the effect or flips its sign, and "
              "Blanchard and Quah's long-run restriction. Then how answers are marked, what to do when stuck, and "
              "where each question is still open.",
        handoff="Part 57 opens Act XI, Economics at Work: reading the economy in real time, from how a number is made "
                "to nowcasts and the record of forecasters.",
        outside="Parts 5-6: demand and welfare; Part 15: externalities; Part 16: auctions; Parts 10, 13 and 14: "
                "screening; Part 20: the Ramsey model; Parts 24 and 42: search and unemployment insurance; Parts 28 "
                "and 30: discretion and the three-equation model; Part 52: Aiyagari; Part 4: instruments; Part 54: "
                "GMM; Part 55: long-run restrictions; Statistics, Built: difference-in-differences.",
        objectives={
            "U": ["Solve a consumer's problem on a kinked budget and say where the consumer ends up.",
                  "Explain why a market with an externality is inefficient, and what tax fixes it."],
            "M": ["Solve the core's standard problems: an auction with a reserve, a screening menu, a Ramsey "
                  "transition, a search problem with a deadline, discretion against commitment.",
                  "Identify a demand curve with an instrument, estimate an Euler equation by GMM with the J test, and "
                  "identify a VAR by a long-run restriction.",
                  "Read what two-way fixed effects estimates when adoption is staggered."],
            "D": ["Prove that an Aiyagari economy's interest rate lies below the rate of time preference, and that the "
                  "reservation wage falls as benefits run out.",
                  "Derive the screening menu for a continuum of types by the envelope theorem and virtual types."],
            "I": ["Write an answer a grader, a referee or a manager can check: the set-up, the condition, the answer "
                  "in a box, and a test of it."],
        },
        results=[
            ("Slutsky at a kink", r"\frac{dx}{dp_2} = \frac{\partial h}{\partial p_2} - (x - \bar x)\,"
                                  r"\frac{\partial x}{\partial m}"),
            ("A first-price bid with a reserve", r"\beta(v) = v - \frac{v^n - r^n}{n\,v^{n-1}}"),
            ("Screening", r"q(\theta) = \theta - \frac{1 - F(\theta)}{f(\theta)}"),
            ("The inflation bias", r"\bar\pi = \frac{\lambda\kappa x^*}{\lambda(1 - \beta) + \kappa^2}"),
            ("Blanchard and Quah", r"B = C(1)^{-1}\operatorname{chol}\big(C(1)\,\Sigma\,C(1)'\big)"),
        ],
        U=(0, 1, 2, 9, "s08_intermission"), D=(4, 8, 11, 12), I=(13,),
        also=(("Agora's exam solvers", "explainer/economics/agora/exam.py"),
              ("Part 52's Aiyagari economy", "explainer/economics/agora/hetero.py")),
    ),
]
