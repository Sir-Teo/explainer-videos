"""Stage V, PhD: the research frontier, from optimal transport to the dissertation (Parts 61-65)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=61, level="D", widget="quantiletransport", prereq=(43, 48, 51),
        question="How far apart are two distributions, when moving mass has a cost?",
        story="In 1781 Monge asks the Paris Academy which shovelful of earth should fill which hole so that the "
              "total carrying is least. On a line the monotone plan, leftmost earth to leftmost hole, is optimal "
              "for any convex cost, and in 1942 Kantorovich lets mass split, which makes the problem a linear "
              "program with a dual of shipping prices. The optimal cost is the Wasserstein distance: on a line "
              "the distance between two quantile functions, computed for the BMI of men and women in NHANES and "
              "split exactly into location, spread and shape. The part then asks how well it can be estimated: "
              "the empirical rate n^(-1/d) is the curse of dimensionality, entropic smoothing and Sinkhorn's "
              "scaling buy speed and a dimension-free rate at fixed regularization, and transport maps have "
              "minimax rates of their own. Averaging quantile functions gives barycenters of blood pressure by "
              "age, and optimal maps to a reference grid give center-outward ranks and a test that keeps its "
              "power on Cauchy data where Hotelling's has almost none. It ends with Langevin dynamics as the gradient "
              "flow of relative entropy, flow matching as transport, and the open problems.",
        handoff="Transport returns as carrying a causal effect to a new population in Part 62, as barycenter "
                "score adjustment in Part 63, as the generalization of generative models in Part 64, and as a "
                "way of comparing distributions in the dissertation of Part 65.",
        outside="Stage IV's measure-theoretic probability and empirical process theory; linear programming "
                "duality as in Part 21; the Wasserstein balls of Part 60.",
        objectives={
            "U": ["Explain Monge's problem on a line and why the plan that keeps the order is optimal for a "
                  "convex cost.",
                  "Compute the Wasserstein distance between two samples of equal size by sorting them."],
            "M": ["Write the Kantorovich linear program and its dual, and check strong duality and "
                  "complementary slackness on a small example.",
                  "Derive the log-domain Sinkhorn updates as block maximization of the entropic dual."],
            "D": ["State the n^(-1/d) rate for empirical Wasserstein distances with its assumptions, and say "
                  "what entropic regularization changes and what it does not.",
                  "Explain in what sense Langevin dynamics is the Wasserstein gradient flow of relative "
                  "entropy, and prove the exponential rate for a Gaussian target."],
            "I": ["Compare two empirical distributions by W1 and W2, split W2 squared into location, spread "
                  "and shape, and report which empirical laws were compared.",
                  "Run Sinkhorn with a convergence check on both marginals, and distinguish the raw plan cost "
                  "from the regularized objective."],
        },
        results=[
            ("Kantorovich duality",
             r"\min_{P\ge 0,\ P\mathbf 1=a,\ P^\top\mathbf 1=b}\ \sum_{i,j}P_{ij}C_{ij}"
             r"\;=\;\max_{f_i+g_j\le C_{ij}}\ a^\top f+b^\top g"),
            ("Transport on a line",
             r"W_p^p(\mu,\nu)=\int_0^1\bigl|F^{-1}(u)-G^{-1}(u)\bigr|^p\,du,\qquad "
             r"W_1(\mu,\nu)=\int_{-\infty}^{\infty}|F(x)-G(x)|\,dx"),
            ("Normal laws on a line",
             r"W_2^2\bigl(N(m_1,\sigma_1^2),N(m_2,\sigma_2^2)\bigr)=(m_1-m_2)^2+(\sigma_1-\sigma_2)^2"),
            ("The empirical rate",
             r"\operatorname{E}W_1(\hat\mu_n,\mu)\asymp n^{-1/d}\qquad(d\ge 3,\ \mu\text{ uniform on the cube})"),
            ("Sinkhorn's update",
             r"f_i\leftarrow-\varepsilon\log\sum_j b_j\,e^{(g_j-C_{ij})/\varepsilon},\qquad "
             r"g_j\leftarrow-\varepsilon\log\sum_i a_i\,e^{(f_i-C_{ij})/\varepsilon}"),
            ("Langevin's rate for a Gaussian target",
             r"\operatorname{KL}(\rho_t\,\Vert\,N(0,\Sigma))\le e^{-2t/\lambda_{\max}(\Sigma)}\,"
             r"\operatorname{KL}(\rho_0\,\Vert\,N(0,\Sigma))\qquad(\rho_0=N(m_0,\Sigma))"),
        ],
        U=(0,), I=(4, 6, 9),
        also=(("statkit.ot", "explainer/stats/kit/ot.py"),),
    ),
    Part(
        n=62, level="D", widget="proxybridge", prereq=(36, 37, 49),
        question="What can be identified, and estimated, when the textbook assumptions fail?",
        story="In 2011 the HIV-CAUSAL Collaboration emulates a trial of when to start therapy, comparing "
              "strategies indexed by CD4 thresholds, and START later randomizes the question. That is a dynamic "
              "regime, and the part asks what remains when randomization, measured confounders and natural "
              "experiments all fail. The front-door formula identifies an effect through a mediator, and "
              "the ID algorithm decides which effects a graph identifies. When it identifies none, the marginal sensitivity "
              "model bounds the effect on the National Supported Work data, and proximal inference replaces the "
              "hidden confounder by two proxies and a two-stage least squares fit. The questions then grow: "
              "spillovers on a network by exposure mappings, treatment rules learned and then evaluated on "
              "independent data, Q-learning for two-stage regimes, and what causal discovery can and cannot "
              "recover. It ends by transporting a trial to its nonparticipants, with a surrogate index that "
              "works and one that a bypass breaks, and the open problems. Each method replaces one assumption "
              "with other explicit assumptions.",
        handoff="Fair decisions and causal fairness follow in Part 63, causal questions about deployed AI "
                "systems (interference, surrogate indices) in Part 64, and learned adjustment sets are one of "
                "the candidate questions of Part 65.",
        outside="The potential-outcomes and graphical causal inference of Parts 35 to 37; semiparametric "
                "efficiency as in Part 49; instrumental variables.",
        objectives={
            "U": ["Explain what a dynamic treatment regime is, and how the question 'when to start' differs "
                  "from 'treat or not'."],
            "M": ["Evaluate the front-door formula from a table of treatment, mediator and outcome, and state "
                  "the graph it needs.",
                  "Derive the inverse-odds weights that carry a trial's effect to its nonparticipants."],
            "D": ["State the marginal sensitivity model and explain why optimizing over the weight box is a "
                  "relaxation of the identified set.",
                  "State the assumptions of proximal identification (proxy exclusions, a bridge function, "
                  "completeness) and show which one each counterexample drops.",
                  "Prove that the in-sample value of a learned policy is optimistic, and say what an "
                  "independent evaluation sample repairs."],
            "I": ["Report an observational effect with the value of Lambda at which its bounds reach zero, "
                  "beside a benchmark.",
                  "Estimate direct and spillover effects on a network from exposure probabilities, and say "
                  "which units have no support for a contrast."],
        },
        results=[
            ("The front-door formula",
             r"P(y\mid\operatorname{do}(a))=\sum_m P(m\mid a)\sum_{a'}P(a')\,P(y\mid m,a')"),
            ("The marginal sensitivity model's weight box",
             r"1+\frac{1}{\Lambda}\cdot\frac{1-e(x)}{e(x)}\ \le\ w\ \le\ 1+\Lambda\cdot\frac{1-e(x)}{e(x)}"),
            ("The linear proximal moment",
             r"\operatorname{E}\bigl[(Y-b_0-b_AA-b_WW)\,(1,A,Z)^\top\bigr]=0"),
            ("The winner's curse of a learned policy",
             r"\operatorname{E}\sup_{\pi\in\Pi}\hat V(\pi)\ \ge\ \sup_{\pi\in\Pi}V(\pi)\ \ge\ "
             r"\operatorname{E}V(\hat\pi)"),
            ("Inverse-odds transport weights",
             r"\frac{dP_{X\mid\text{nonparticipant}}}{dP_{X\mid\text{trial}}}(x)\ \propto\ \frac{1-p(x)}{p(x)},"
             r"\qquad p(x)=P(\text{trial}\mid x)"),
        ],
        U=(0,), I=(2, 8, 9),
        also=(("statkit.frontier", "explainer/stats/kit/frontier.py"),),
    ),
    Part(
        n=63, level="D", widget="privacytradeoff", prereq=(41, 46, 50),
        question="How much does protecting individuals cost the statistics, and what does fairness require?",
        story="In the mid-1990s Massachusetts releases state employees' hospital records without names, and "
              "Latanya Sweeney finds Governor Weld's by joining ZIP code, birth date and sex to a twenty-dollar "
              "voter roll. Anonymity is not a property of a dataset, so privacy becomes a property of the "
              "release: differential privacy, whose price is noise. The part reads the definition as a "
              "hypothesis test between two neighbouring databases, with trade-off curves and Gaussian "
              "differential privacy, and adds up losses with Renyi and zero-concentrated accountants. It then "
              "prices privacy in mean squared error under the central and local models, repairs a confidence "
              "interval that ignored the noise (85.4% against 95.2% coverage), and follows the 2020 Census and "
              "noisy gradient descent. The second half turns to ProPublica's COMPAS data: independence, "
              "separation and sufficiency, Chouldechova's identity and the theorem that they cannot all hold "
              "when base rates differ, multicalibration by patching, and counterfactual fairness.",
        handoff="Part 64 answers repeated queries to a holdout through noise and reads watermark detection and "
                "judged labels as tests with the same error rates; private inference beyond the mean is one of the candidate questions of Part 65.",
        outside="Neyman-Pearson testing as in Part 46; minimax lower bounds as in Part 50; measurement error "
                "and survey practice as in Part 41.",
        objectives={
            "U": ["Explain how a join on ZIP code, birth date and sex re-identifies a record with no name on "
                  "it.",
                  "Compute false positive rates, false negative rates and predictive values by group, and say "
                  "which fairness criterion each belongs to."],
            "M": ["Prove that the Laplace mechanism and randomized response are epsilon-differentially "
                  "private, and debias a randomized-response proportion.",
                  "Derive Chouldechova's identity and the impossibility that follows from unequal base rates."],
            "D": ["State differential privacy as a bound on every test's trade-off curve, and prove that "
                  "independent Gaussian mechanisms compose to a Gaussian curve with the root sum of squares.",
                  "State the central and local minimax costs of privacy and the assumptions behind each."],
            "I": ["Build a confidence interval from a privatized count that adds the mechanism's variance, "
                  "and publish the mechanism and its parameters with it.",
                  "Audit a score by group: error rates, calibration within score cells, and which gaps a "
                  "change of threshold can and cannot remove."],
        },
        results=[
            ("Differential privacy",
             r"P\bigl(M(D)\in S\bigr)\le e^{\varepsilon}P\bigl(M(D')\in S\bigr)+\delta"
             r"\qquad\text{for all neighbours }D,D'\text{ and all }S"),
            ("The trade-off curve of (epsilon, delta)-DP",
             r"\beta(\alpha)\ \ge\ \max\bigl\{0,\ 1-\delta-e^{\varepsilon}\alpha,\ "
             r"e^{-\varepsilon}(1-\delta-\alpha)\bigr\}"),
            ("Gaussian differential privacy",
             r"G_\mu(\alpha)=\Phi\bigl(\Phi^{-1}(1-\alpha)-\mu\bigr),\qquad "
             r"G_{\mu_1}\otimes G_{\mu_2}=G_{\sqrt{\mu_1^2+\mu_2^2}}"),
            ("A private proportion's mean squared error",
             r"\text{central: }\frac{p(1-p)}{n}+\frac{2}{n^2\varepsilon^2},\qquad "
             r"\text{local: }\frac{q(1-q)}{n(2\pi-1)^2},\quad \pi=\frac{e^\varepsilon}{1+e^\varepsilon},\ "
             r"q=(2\pi-1)p+1-\pi"),
            ("Chouldechova's identity",
             r"\mathrm{FPR}=\frac{p}{1-p}\cdot\frac{1-\mathrm{PPV}}{\mathrm{PPV}}\cdot(1-\mathrm{FNR})"),
        ],
        U=(0, 8), I=(5, 6, 7),
        also=(("statkit.privacy", "explainer/stats/kit/privacy.py"),),
    ),
    Part(
        n=64, level="D", widget="leaderboardgap", prereq=(34, 57, 58),
        question="When machines make the predictions, generate the data and grade each other, what does honest "
                 "uncertainty look like?",
        story="A new model scores 85.2% on a thousand questions against 84.7% for the previous best. On a "
              "constructed table the paired 95% interval for the half point runs from -1.88 to 2.88 points, and "
              "in fresh benchmarks written under the same model the order reverses a third of the time. The "
              "part treats evaluation as estimation: questions that cluster need cluster-robust errors, two "
              "models on the same questions need a paired analysis and McNemar's test, an arena is a "
              "Bradley-Terry logistic regression, and item response theory picks anchor questions. Reusing a "
              "test set adaptively overfits it, and a noisy threshold limits the damage. Then the machines move "
              "into the data: labels from a judge are corrected by prediction-powered inference, and a Gaussian "
              "refitted to its own samples loses variance by a factor (n-1)/n each generation. It ends with "
              "conformal factuality, watermarks as hypothesis tests, simulation-based inference, Tweedie's "
              "formula inside diffusion models, experiments in a market with interference, and open problems. "
              "Every example is constructed arithmetic or seeded simulation; no real model is evaluated.",
        handoff="The weighted conformal intervals and the open problem of conditional guarantees pass to the "
                "dissertation of Part 65, and the benchmark rows join its full Coverage Board.",
        outside="Prediction-powered inference from Part 34, conformal prediction from Part 57, sequential and "
                "adaptive analysis from Part 58; logistic regression and cluster-robust variances.",
        objectives={
            "U": ["Compute a benchmark score's standard error and say why two overlapping intervals do not "
                  "answer which model is better.",
                  "Compare two models on the same questions with a paired interval and McNemar's test, using "
                  "only the questions on which they disagree."],
            "M": ["Fit a Bradley-Terry model as a logistic regression and say why only differences of "
                  "strengths are identified.",
                  "Derive the expected variance ((n-1)/n)^t of a Gaussian refitted to its own samples, and "
                  "show that it tends to zero almost surely."],
            "D": ["State what prediction-powered inference assumes about the predictor and the two samples, "
                  "and derive its variance.",
                  "Derive Tweedie's formula for a noised density and explain how an exact empirical score "
                  "memorizes the training points."],
            "I": ["Report a benchmark comparison with cluster-robust and paired standard errors, and count "
                  "ties and reversals rather than announcing an order.",
                  "Recognize adaptive reuse of a test set, and interference between arms of an experiment on "
                  "a deployed system."],
        },
        results=[
            ("The cluster-robust standard error (CR1)",
             r"\widehat{\mathrm{SE}}^2=\frac{G}{G-1}\cdot\frac{1}{n^2}\sum_{c=1}^{G}"
             r"\Bigl(\sum_{i\in c}(x_i-\bar x)\Bigr)^2"),
            ("The paired variance",
             r"\operatorname{Var}(\bar a-\bar b)=\frac{\sigma_a^2+\sigma_b^2-2\sigma_{ab}}{n},\qquad "
             r"\bar a-\bar b=\frac{n_{10}-n_{01}}{n}"),
            ("Bradley-Terry", r"P(i\text{ beats }j)=\frac{1}{1+e^{-(\theta_i-\theta_j)}}"),
            ("Prediction-powered inference for a mean",
             r"\hat\theta=\frac1N\sum_{i=1}^{N}f(\tilde x_i)+\frac1n\sum_{i=1}^{n}\bigl(y_i-f(x_i)\bigr),"
             r"\qquad \operatorname{Var}\hat\theta=\frac{\operatorname{Var}f}{N}+"
             r"\frac{\operatorname{Var}(y-f)}{n}"),
            ("The Gaussian's collapse",
             r"\operatorname{E}\hat\sigma_t^2=\Bigl(\frac{n-1}{n}\Bigr)^{t},\qquad "
             r"\hat\sigma_t^2\to 0\ \text{almost surely}"),
            ("Tweedie's formula",
             r"\operatorname{E}[x\mid y]=y+\sigma^2\,\nabla\log p_\sigma(y),\qquad y=x+N(0,\sigma^2)"),
        ],
        U=(0, 1, 2), I=(3, 5, 6, 12),
        also=(("statkit.evals", "explainer/stats/kit/evals.py"),),
    ),
    Part(
        n=65, level="D", widget="tiltedconformal", prereq=(57, 60, 64),
        question="How is new statistical knowledge made, and what has the whole degree shown?",
        story="The degree began in 1662 with John Graunt reading the Bills of Mortality, and it ends by "
              "carrying out one small piece of research on screen. The question is cut from Stage V's open "
              "problems: weighted conformal prediction keeps its coverage under covariate shift when the "
              "likelihood ratio is known, so what does estimating it cost? After reading the literature, the "
              "part states a conjecture precisely enough to be wrong and proves it: coverage is at least "
              "nominal minus the total variation distance between the reweighted source and the target. A "
              "simulation study of 45 cells with 1,000 replicates each tests the bound and five predictions, "
              "one of which fails, and the NHANES extract gives 73.4% coverage without weights and 90.5% with "
              "estimated ones. The original protocol is kept beside a post hoc amendment, and the rerun is "
              "reported as that. Then the full Coverage Board, every promise of the degree with its verdict, "
              "the completed transcript, and a reading list.",
        handoff="Nothing follows in the series. The part hands on a reading list, the open problems of Parts "
                "56 to 64, and the habit of replicating a paper's main table before changing one assumption.",
        outside="The whole series, and in particular weighted conformal prediction (Part 57), density-ratio "
                "weights under shift (Part 60) and simulation studies (Part 7).",
        objectives={
            "U": ["Read the Coverage Board: say what a row promises, what kept, conservative and broken mean, "
                  "and what the Board cannot show.",
                  "Name the four habits the degree ends on, and give one part where each was learned."],
            "M": ["Compute the total variation between two unit-variance normal laws, and the reweighted law "
                  "that an exponential tilt of a standard normal produces.",
                  "Run weighted split conformal with the test point's atom at infinity, and report finite "
                  "widths and infinite intervals separately."],
            "D": ["Prove the coverage bound for weights fixed independently of calibration and test data, and "
                  "say where the proof uses the common conditional law of the outcome.",
                  "State what the bound does not give: equality, conditional coverage, or a result for "
                  "weights fitted on the calibration data."],
            "I": ["Write a simulation protocol with predictions before running it, and report the failed "
                  "predictions and any post hoc amendment as such.",
                  "Diagnose weighted conformal intervals in an application: effective sample size, largest "
                  "weight share, and coverage by subgroup."],
        },
        results=[
            ("The teaching theorem",
             r"Q\bigl\{Y\in\hat C_{\hat w}(X)\bigr\}\ \ge\ 1-\alpha-\operatorname{TV}(P_{\hat w},Q_X),\qquad "
             r"P_{\hat w}(dx)=\frac{\hat w(x)\,P_X(dx)}{\operatorname{E}_P\hat w(X)}"),
            ("Total variation between shifted normal laws",
             r"\operatorname{TV}\bigl(N(a,1),N(b,1)\bigr)=2\Phi\bigl(|a-b|/2\bigr)-1"),
            ("Tempered weights tilt the source",
             r"e^{\lambda\mu x}\,N(0,1)\ \propto\ N(\lambda\mu,1),\qquad "
             r"\operatorname{TV}=2\Phi\bigl(|1-\lambda|\,|\mu|/2\bigr)-1"),
            ("Pinsker's inequality in the tempered case",
             r"\operatorname{TV}\le\sqrt{\operatorname{KL}/2},\qquad \operatorname{KL}=(1-\lambda)^2\mu^2/2"),
        ],
        U=(0, 8, 9, 10), I=(2, 6, 7),
        also=(("statkit.thesis", "explainer/stats/kit/thesis.py"),
              ("The original protocol", "videos/stats/stats65/PROTOCOL.md")),
    ),
]
