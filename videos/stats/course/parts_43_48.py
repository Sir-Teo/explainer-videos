"""Stage IV, PhD core: probability, estimation, testing, asymptotics and empirical processes (Parts 43-48)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=43, level="D", widget="kolmogorovgap", prereq=(2, 3, 6),
        question="What exactly is a random variable, and what do the limit theorems really say?",
        story="In Paris in 1900 Hilbert's sixth problem asks for axioms of probability; in 1933 Kolmogorov's "
              "Grundbegriffe supplies them on top of Lebesgue's measure. The part builds the axioms in order: "
              "Vitali's set shows why not every subset can have a length, a random variable becomes a measurable "
              "map and its law a push-forward, and the integral arrives with its convergence theorems and the "
              "counterexamples that mark their edges. Borel-Cantelli, the 0-1 laws and Etemadi's proof give the "
              "strong law. The part then turns from almost-sure limits to laws: the portmanteau theorem, "
              "characteristic functions and Levy's continuity theorem, Lindeberg's condition with Feller's "
              "converse, and Stein's method, which says how fast. The weak-convergence lab measures the rate "
              "exactly: every Kolmogorov distance falls like one over root n, and a fair coin uses 84% of the "
              "Berry-Esseen bound. It ends beyond the normal law, with stable limits and the DAX, Cramer's rate "
              "and Bernoulli's urn, and the extreme-value theorem fitted to Port Pirie's sea levels.",
        handoff="Conditional expectation, martingales and Brownian motion follow in Part 44; sufficiency becomes a "
                "sigma-algebra in Part 45; the delta method and Edgeworth expansions are proved in Part 47; weak "
                "convergence of whole processes (Donsker) is Part 48.",
        outside="Real analysis to the level of Analysis, Built Parts 1-5 (limits, the Lebesgue measure and "
                "Caratheodory's extension), and Stage I's probability (Parts 2, 3 and 6).",
        objectives={
            "U": ["Explain what Hilbert asked for and what Kolmogorov's three objects (outcomes, events, a measure "
                  "of mass one) are.",
                  "Say in words what the Kolmogorov distance between a sum's law and the normal law measures, and "
                  "how it shrinks with n."],
            "M": ["Compute Cramer's rate function as a Legendre transform for the normal, Poisson and Bernoulli "
                  "laws.",
                  "Check Lindeberg's condition for an i.i.d. sum and for an array in which one summand "
                  "dominates."],
            "D": ["Prove that a CDF determines its law by the pi-lambda theorem, and the strong law by Etemadi's "
                  "truncation argument.",
                  "Prove Levy's continuity theorem from the tail bound, and the Lindeberg-Feller theorem by "
                  "replacement.",
                  "Derive the Wasserstein bound rho / sqrt(n) from Stein's equation, and state what the "
                  "Berry-Esseen constant 0.4748 does and does not claim."],
            "I": ["Judge whether a normal approximation is safe at a given n from the summand's skewness, and say "
                  "why a t interval for exponential data still undercovers at n = 30.",
                  "Fit a GEV law to annual maxima and report a return level with the assumptions it rests on."],
        },
        results=[
            ("The portmanteau theorem",
             r"X_n\Rightarrow X\iff \operatorname{E}f(X_n)\to\operatorname{E}f(X)\ \text{for all bounded continuous }f"
             r"\iff \limsup_n P(X_n\in F)\le P(X\in F)\ \text{for all closed }F"),
            ("Lindeberg's condition",
             r"L_n(\varepsilon)=\frac{1}{s_n^2}\sum_{k\le n}\operatorname{E}\bigl[X_k^2\,1(|X_k|>\varepsilon s_n)\bigr]"
             r"\to 0\ \text{for all }\varepsilon>0\ \Longrightarrow\ \frac{S_n}{s_n}\Rightarrow N(0,1)"),
            ("Stein and Berry-Esseen",
             r"d_W(S_n^*,Z)\le\frac{\rho}{\sqrt n},\qquad \sup_z\bigl|P(S_n^*\le z)-\Phi(z)\bigr|\le"
             r"\frac{0.4748\,\rho}{\sqrt n},\qquad \rho=\frac{\operatorname{E}|X-\mu|^3}{\sigma^3}"),
            ("Cramer's theorem",
             r"\tfrac1n\log P(\bar X_n\ge a)\to -I(a),\qquad I(a)=\sup_t\bigl\{ta-\log\operatorname{E}e^{tX}\bigr\}"
             r"\quad (a>\operatorname{E}X)"),
            ("The extreme-value laws",
             r"P\Bigl(\frac{M_n-b_n}{a_n}\le x\Bigr)\to G_\xi(x)=\exp\bigl\{-(1+\xi x)^{-1/\xi}\bigr\},"
             r"\qquad 1+\xi x>0"),
        ],
        U=(0,), I=(11, 13),
        also=(("statkit.limits, the weak-convergence lab", "explainer/stats/kit/limits.py"),),
    ),
    Part(
        n=44, level="D", widget="villewealth", prereq=(17, 27, 43),
        question="What can be proved about randomness that unfolds in time?",
        story="In 1913 Markov counts the vowels and consonants in the first 20,000 letters of Pushkin's Eugene "
              "Onegin to answer Nekrasov, who had claimed that the law of large numbers needs independence: a vowel "
              "follows a vowel with probability 0.128, a consonant with 0.663, and the long-run share still "
              "settles. The part builds the theory of dependence in time. Conditional expectation is defined by "
              "Radon-Nikodym and as a projection, and martingales follow with Doob's theorems: optional stopping "
              "(gambler's ruin, and why doubling fails), the maximal inequalities, and convergence by upcrossings. "
              "Ville's inequality is drawn with the betting paths: a likelihood-ratio wealth under the null reaches "
              "10 with probability at most a tenth, however often one looks. Concentration and the martingale CLT "
              "justify the AR(1) interval; drift and minorization give the CLT behind MCMC standard errors, and "
              "coupling bounds mixing times on the cycle, the hypercube and a deck of cards. The part then "
              "constructs Brownian motion by Levy and Ciesielski, proves Donsker's principle and explains the "
              "Dickey-Fuller law, and ends with the iterated logarithm and the martingales under survival "
              "analysis.",
        handoff="Rao-Blackwell as a conditional expectation and Brown's use of Polya's recurrence come in Part 45; "
                "the score as a martingale in Part 47; Donsker for classes of functions and the Brownian bridge in "
                "Part 48; McDiarmid in Part 54; Ville's inequality becomes e-values and confidence sequences in "
                "Part 58.",
        outside="Part 43's measure theory (sigma-algebras, the integral and its convergence theorems, weak "
                "convergence), and linear algebra for the eigenvalues of a transition matrix.",
        objectives={
            "U": ["Explain what Markov's count of Onegin showed about dependence and the law of large numbers.",
                  "Compute the chance of doubling a stake and the expected length of play in a fair game, and say "
                  "why no stopping rule makes a fair game favourable."],
            "M": ["Compute gambler's ruin probabilities for an unfair game with de Moivre's martingale.",
                  "Compute a finite chain's distance from stationarity, its mixing time and its relaxation time, "
                  "and bound the first by a coupling."],
            "D": ["Prove optional stopping under each of its three conditions and give the doubling strategy as "
                  "the counterexample when they fail.",
                  "Prove Ville's inequality from Doob's maximal inequality, and almost-sure convergence of "
                  "L1-bounded martingales from upcrossings.",
                  "State the drift and minorization conditions under which an MCMC average obeys a CLT with "
                  "variance sigma squared times tau."],
            "I": ["Monitor an experiment with a betting test that stays valid at every look, and say what a "
                  "repeatedly applied z test does instead.",
                  "Report an MCMC mean with a batch-means standard error, and say why the i.i.d. formula "
                  "understates it."],
        },
        results=[
            ("Optional stopping and the fair ruin",
             r"\operatorname{E}M_\tau=\operatorname{E}M_0,\qquad P(\text{reach }b\text{ before }0)=\frac ab,"
             r"\qquad \operatorname{E}\tau=a(b-a)"),
            ("Ville's inequality",
             r"M_n\ge 0\ \text{a supermartingale},\ M_0=1\ \Longrightarrow\ "
             r"P\Bigl(\sup_{n}M_n\ge\frac1\alpha\Bigr)\le\alpha"),
            ("Azuma-Hoeffding",
             r"|M_k-M_{k-1}|\le c_k\ \Longrightarrow\ P\bigl(|M_n-M_0|\ge t\bigr)\le "
             r"2\exp\Bigl\{-\frac{t^2}{2\sum_k c_k^2}\Bigr\}"),
            ("The martingale CLT for AR(1)", r"\sqrt n\,(\hat\varphi-\varphi)\Rightarrow N(0,\,1-\varphi^2)"
                                             r"\qquad (|\varphi|<1)"),
            ("The Markov chain CLT",
             r"\sqrt n\,\bigl(\bar f_n-\pi f\bigr)\Rightarrow N(0,\,\sigma_f^2\,\tau),"
             r"\qquad \tau=1+2\sum_{k\ge1}\rho_k"),
            ("The reflection principle and the iterated logarithm",
             r"P\Bigl(\max_{t\le1}B_t\ge a\Bigr)=2P(B_1\ge a),\qquad "
             r"\limsup_n\frac{S_n}{\sqrt{2n\log\log n}}=1\ \text{a.s.}"),
        ],
        U=(0, 3), I=(4, 8),
        also=(("statkit.chains, the coupling and mixing lab", "explainer/stats/kit/chains.py"),),
    ),
    Part(
        n=45, level="D", widget="riskhull", prereq=(9, 25, 43, 44),
        question="What does 'best' mean for an estimator, and why is the obvious estimator inadmissible in three "
                 "dimensions?",
        story="At the Third Berkeley Symposium, published in 1956, Charles Stein shows that for three or more "
              "normal means the observations themselves are inadmissible: the James-Stein estimator has smaller "
              "expected squared error at every value of the means. The part asks what best can mean. Wald's "
              "decision theory gives the language, and the risk-set explorer draws a whole problem at once: "
              "sixteen rules for calling a coin fair or biased, their convex hull, Bayes rules as supporting lines "
              "and the minimax rule on the diagonal. Exponential families are read as convex duality, and "
              "sufficiency, completeness, Rao-Blackwell, Lehmann-Scheffe and Basu say when a best estimator "
              "exists in a class, with the German tank problem as the example and the absurd unbiased estimator "
              "as the warning. The turn is chapter 10: Stein's lemma gives an unbiased estimate of risk and the "
              "exact risk of James-Stein, and Brown explains the number three by the recurrence of Brownian "
              "motion. The part ends with Strawderman's proper Bayes minimax rules and with Robbins's empirical "
              "Bayes on 9,461 insurance policies.",
        handoff="Risk sets and least favourable priors return for tests in Part 46; the local asymptotic minimax "
                "theorem replaces the Cramer-Rao bound in Part 47; minimax rates come in Part 50, shrinkage in "
                "high dimensions in Part 52, and the frequentist risk of Bayes rules in Part 53.",
        outside="Part 43's measure theory (conditional expectation as in Part 44), convexity and the Legendre "
                "transform, and the estimation theory of Part 9.",
        objectives={
            "U": ["State Stein's paradox in words and say what 'smaller risk for every value of the means' does "
                  "and does not promise about a single coordinate.",
                  "Read a risk set: find the dominated rules, the Bayes rule for a prior, and the minimax rule."],
            "M": ["Compute the risk function of (X + a)/(n + a + b) for a binomial and find the rule with "
                  "constant risk.",
                  "Rao-Blackwellize an unbiased estimator given a sufficient statistic, as for the tanks' "
                  "maximum.",
                  "Apply Robbins's formula and Tweedie's formula to counts and to normal observations."],
            "D": ["Prove Lehmann-Scheffe and Basu's theorem, and give families in which the sufficient "
                  "statistic is not complete.",
                  "Prove Stein's lemma, derive SURE and the exact risk of James-Stein, and state Baranchik's "
                  "condition for minimaxity.",
                  "State Brown's criterion linking admissibility of a generalized Bayes rule to recurrence, and "
                  "apply it to the flat prior in p dimensions."],
            "I": ["Choose between an unconditional and a conditional interval when an ancillary statistic (which "
                  "instrument, the sample range) is observed, and report the conditional one.",
                  "Shrink many noisy estimates with James-Stein or empirical Bayes, and say why an interval of "
                  "the usual width around a shrunken estimate can undercover."],
        },
        results=[
            ("The minimax theorem in a finite problem",
             r"\min_{\delta}\max_{\theta}R(\theta,\delta)=\max_{\pi}\min_{\delta}\int R(\theta,\delta)\,d\pi(\theta)"),
            ("The binomial minimax rule",
             r"\delta(X)=\frac{X+\sqrt n/2}{n+\sqrt n},\qquad R(p,\delta)=\frac{1}{4(1+\sqrt n)^2}\ \text{for every }p"),
            ("Lehmann-Scheffe",
             r"T\ \text{complete sufficient},\ \operatorname{E}_\theta g(T)=\tau(\theta)\ \text{for all }\theta"
             r"\ \Longrightarrow\ g(T)\ \text{is the UMVUE of }\tau(\theta)"),
            ("Stein's unbiased risk estimate",
             r"X\sim N_p(\theta,I):\qquad \operatorname{E}\|X+g(X)-\theta\|^2="
             r"\operatorname{E}\bigl[\,p+\|g(X)\|^2+2\,\nabla\!\cdot g(X)\bigr]"),
            ("The exact risk of James-Stein",
             r"R\Bigl(\theta,\Bigl(1-\frac{p-2}{\|X\|^2}\Bigr)X\Bigr)=p-(p-2)^2\,"
             r"\operatorname{E}\Bigl[\frac{1}{p-2+2K}\Bigr],\qquad K\sim\operatorname{Poisson}\bigl(\|\theta\|^2/2\bigr)"),
            ("Tweedie and Robbins",
             r"\operatorname{E}[\theta\mid x]=x+\nabla\log m(x)\ \ (\text{normal}),\qquad "
             r"\operatorname{E}[\theta\mid x]=\frac{(x+1)\,f(x+1)}{f(x)}\ \ (\text{Poisson})"),
        ],
        U=(0, 2), I=(7, 13),
        also=(("statkit.decision", "explainer/stats/kit/decision.py"),),
    ),
    Part(
        n=46, level="D", widget="similarslices", prereq=(10, 11, 45),
        question="When is a test optimal, and what can an interval honestly promise?",
        story="The part opens with the Behrens-Fisher problem: two normal samples with unequal, unknown variances. "
              "Fisher's fiducial test, Neyman's objection, Welch's approximation and Linnik's negative results "
              "frame the question of whether a test of exact size exists, and a simulation shows the pooled t "
              "test rejecting a true null 30% of the time. The Neyman-Pearson theory is then built in full: the "
              "lemma with randomization, Karlin-Rubin for monotone likelihood ratios, and unbiased tests by "
              "Neyman structure, drawn slice by slice so that each value of the nuisance statistic spends "
              "exactly alpha. Invariance proves the t test optimal, and the likelihood ratio test is taken to a "
              "boundary, where Chernoff's mixture replaces Wilks. The part turns to confidence sets: inversion "
              "gives the Clopper-Pearson belt, Gleser and Hwang show that a ratio needs unbounded sets (Fieller "
              "covers 95% where the delta method covers 78%), and Feldman and Cousins repair limits for a "
              "bounded parameter. It ends with closed testing, recognizable subsets, the Berger-Sellke bounds on "
              "what a p-value of 0.05 can mean, and the Kolmogorov-Smirnov test with estimated parameters.",
        handoff="Wilks's theorem is proved and local power computed in Part 47; the Kolmogorov-Smirnov limit "
                "with estimated parameters is derived in Part 48; conditioning on a selection event is Part 56, "
                "exact distribution-free tests Part 57, and e-values and confidence sequences Part 58.",
        outside="Part 45's decision theory (risk sets, sufficiency, completeness) and exponential families; the "
                "tests and intervals of Parts 10 and 11.",
        objectives={
            "U": ["Explain the Behrens-Fisher problem and why the pooled t test fails when the small sample has "
                  "the large variance.",
                  "Say what a test's size and power are, and why a discrete test needs randomization to spend "
                  "exactly alpha."],
            "M": ["Construct the randomized most powerful test for a binomial and show it is UMP one-sided by "
                  "monotone likelihood ratio.",
                  "Invert a family of tests into a confidence set and compute its exact coverage.",
                  "Apply closed testing with Bonferroni and with Simes local tests to a set of p-values."],
            "D": ["Prove the Neyman-Pearson lemma with its necessity part, and Karlin-Rubin.",
                  "Prove that similar tests have Neyman structure when the nuisance statistic is boundedly "
                  "complete, and derive the UMPU two-sided test from its two side conditions.",
                  "State the Gleser-Hwang theorem and Chernoff's boundary limit, with the conditions each "
                  "needs."],
            "I": ["Report a ratio (an LD50, an instrumental-variable estimate) with Fieller's set, and say what "
                  "an unbounded set means.",
                  "Use Welch's test by default for two means, and Feldman-Cousins rather than flip-flopping for "
                  "a signal above a known background.",
                  "Translate a p-value into a bound on the posterior probability of the null before calling it "
                  "evidence."],
        },
        results=[
            ("The Neyman-Pearson lemma",
             r"\varphi(x)=\begin{cases}1,&f_1(x)>k f_0(x)\\ \gamma,&f_1(x)=k f_0(x)\\ 0,&f_1(x)<k f_0(x)\end{cases}"
             r"\qquad \operatorname{E}_0\varphi=\alpha\ \Longrightarrow\ \varphi\ \text{is most powerful at level }\alpha"),
            ("Neyman structure",
             r"\operatorname{E}_\theta\varphi=\alpha\ \text{on the boundary}\iff "
             r"\operatorname{E}[\varphi\mid T=t]=\alpha\ \text{for almost every }t\quad"
             r"(T\ \text{sufficient and boundedly complete there})"),
            ("The UMPU side conditions",
             r"\operatorname{E}_{\theta_0}\varphi=\alpha,\qquad "
             r"\operatorname{E}_{\theta_0}[T\varphi]=\alpha\,\operatorname{E}_{\theta_0}T"),
            ("Chernoff's boundary limit",
             r"H_0:\mu=0\ \text{vs}\ \mu\ge 0:\qquad 2\log\Lambda_n\Rightarrow\tfrac12\chi^2_0+\tfrac12\chi^2_1"),
            ("Fieller's set",
             r"\Bigl\{\rho:\ (a-\rho b)^2\le z_{\alpha/2}^2\,\bigl(v_a-2\rho\,c_{ab}+\rho^2 v_b\bigr)\Bigr\}"),
            ("The calibration of a p-value",
             r"\mathrm{BF}_{01}\ge -e\,p\log p\quad (p<1/e),\qquad "
             r"P(H_0\mid x)\ge\Bigl(1+\frac{1}{-e\,p\log p}\Bigr)^{-1}\ \text{at equal prior odds}"),
        ],
        U=(0,), I=(8, 9, 11),
        also=(("statkit.testing", "explainer/stats/kit/testing.py"),),
    ),
    Part(
        n=47, level="D", widget="hodgesbump", prereq=(22, 43, 45, 46),
        question="What is the best possible estimator in large samples, and why is 'best' so hard to define?",
        story="In 1951 Hodges builds an estimator that reports the sample mean unless it is within n to the minus "
              "one quarter of zero, and then reports zero: at zero its scaled risk tends to zero, below Fisher's "
              "bound. The exact risks show the price, a bump just beside zero that grows like root n. To say in "
              "what sense the MLE is best, the part first builds the large-sample toolkit: stochastic orders and "
              "the delta method, M-estimators with the sandwich variance (Huber on Newcomb's light), the "
              "Bahadur representation of quantiles, influence functions, U-statistics and rank statistics by "
              "Hajek's projection. Le Cam's local asymptotic normality then shows every regular model looking "
              "locally like one Gaussian observation, contiguity gives local power, and Hajek's convolution and "
              "local asymptotic minimax theorems state the optimality: the risk-bump explorer shows Hodges's "
              "local risk tending to h squared, below one only inside the unit neighbourhood. The theory is then "
              "used on the efficiency of tests, the bootstrap's second-order accuracy, saddlepoints, and the "
              "uniform maximum, where the ordinary bootstrap fails and m-out-of-n repairs it.",
        handoff="The uniform laws, Donsker classes and bootstrap empirical processes this part used are proved in "
                "Part 48; efficient influence functions in semiparametric models come in Part 49, minimax lower "
                "bounds beyond the local scale in Part 50, Bernstein-von Mises in Part 53, and growing dimension "
                "in Part 59.",
        outside="Part 43's weak convergence and Part 45's information bounds; likelihood theory at the level of "
                "Part 22; multivariate calculus for the delta method.",
        objectives={
            "U": ["Describe Hodges's estimator and say what its risk does at zero and just beside zero.",
                  "Explain why 'smaller risk at one parameter value' is not a sensible meaning of best."],
            "M": ["Derive the sandwich variance of an M-estimator and compute it for Huber's location estimate.",
                  "Compute a Pitman efficiency from two efficacies and convert it into a ratio of sample sizes.",
                  "Compute local power at theta = h / sqrt(n) from the information."],
            "D": ["Prove asymptotic normality of a Z-estimator from a uniform law and a Taylor expansion, and "
                  "state what replaces the derivative for a sample quantile.",
                  "State LAN and Le Cam's third lemma, and derive the limit law of a statistic under contiguous "
                  "alternatives.",
                  "State the convolution theorem and the local asymptotic minimax theorem with the order of "
                  "their limits, and show that Hodges's estimator is not regular."],
            "I": ["Choose among the t, sign and Wilcoxon tests from their efficiencies under the error laws you "
                  "consider plausible.",
                  "Choose a bootstrap interval (percentile, BCa, bootstrap-t) knowing which is second-order "
                  "accurate, and use m-out-of-n when the statistic is a maximum."],
        },
        results=[
            ("The sandwich for an M-estimator",
             r"\sqrt n\,(\hat\theta_n-\theta_0)\Rightarrow N\bigl(0,\ V^{-1}BV^{-\top}\bigr),\qquad "
             r"V=\operatorname{E}\,\partial_\theta\psi_{\theta_0}(X),\quad "
             r"B=\operatorname{E}\,\psi_{\theta_0}(X)\psi_{\theta_0}(X)^\top"),
            ("The Bahadur representation",
             r"\hat\xi_p=\xi_p+\frac{p-F_n(\xi_p)}{f(\xi_p)}+R_n,\qquad R_n=O_P\bigl(n^{-3/4}\bigr)"),
            ("Local asymptotic normality",
             r"\log\frac{dP^n_{\theta+h/\sqrt n}}{dP^n_{\theta}}=h\,\Delta_n-\tfrac12h^2I(\theta)+o_P(1),\qquad "
             r"\Delta_n\Rightarrow N\bigl(0,I(\theta)\bigr)"),
            ("Local power (Le Cam's third lemma)",
             r"P_{\theta_0+h/\sqrt n}(\text{reject})\to 1-\Phi\bigl(z_\alpha-h\sqrt{I(\theta_0)}\bigr)"),
            ("Hodges's local risk",
             r"n\operatorname{E}_{h/\sqrt n}\bigl(T_n-h/\sqrt n\bigr)^2\to h^2\ \ (\text{each fixed }h),\qquad "
             r"\sup_{|h|\le c}\to c^2"),
            ("The local asymptotic minimax bound",
             r"\lim_{c\to\infty}\liminf_{n\to\infty}\sup_{|h|\le c}\operatorname{E}_{\theta+h/\sqrt n}\,"
             r"\ell\bigl(\sqrt n\,(T_n-\theta-h/\sqrt n)\bigr)\ \ge\ \operatorname{E}\,\ell(Z),\qquad "
             r"Z\sim N\bigl(0,I(\theta)^{-1}\bigr)"),
        ],
        U=(0,), I=(10, 11),
        also=(("statkit.asymptotics", "explainer/stats/kit/asymptotics.py"),),
    ),
    Part(
        n=48, level="D", widget="bridgesup", prereq=(43, 44, 47),
        question="When does an average converge uniformly over a whole class of functions, and at what rate?",
        story="In 1949 Doob guesses that root n times the gap between the empirical and the true distribution "
              "functions behaves like a Brownian bridge, so that Kolmogorov's 1933 law is the law of the bridge's "
              "largest absolute value; Donsker proves it in 1952. The part turns the guess into a theory. An "
              "empirical distribution function is an average of indicators, so the question becomes for which "
              "classes of functions the law of large numbers and the central limit theorem hold uniformly. "
              "Symmetrization and Rademacher averages give Glivenko-Cantelli classes, VC dimension counts "
              "patterns, covering and bracketing numbers measure a class's size, and Dudley's chaining, drawn as "
              "refining nets on a Brownian path, turns entropy into a uniform CLT. The theory is then put to "
              "work: Talagrand's concentration, the functional delta method for quantiles and Kaplan-Meier, the "
              "footprint an estimated nuisance parameter leaves, cube-root rates and Chernoff's distribution, "
              "and empirical risk minimization. It ends where it began: the bootstrap empirical process, and the "
              "Kolmogorov-Smirnov test with estimated parameters, where Kolmogorov's table gives a 5% test a size "
              "near zero and Durbin's process with a parametric bootstrap repairs it.",
        handoff="Donsker conditions for one-step estimators, and the footprint as Neyman orthogonality, come in "
                "Part 49; entropy becomes minimax rates in Part 50; chaining and suprema in high dimensions are "
                "Part 51; VC, Rademacher and margin bounds for learning are Part 54; multiplier bootstraps "
                "return in Part 56.",
        outside="Part 43's weak convergence, Part 44's Brownian motion and Donsker's principle for random walks, "
                "and Part 47's delta method and bootstrap.",
        objectives={
            "U": ["Explain Doob's heuristic: what the scaled gap between the empirical and true distribution "
                  "functions looks like, and why its largest value has one law for every continuous "
                  "distribution.",
                  "Read a Kolmogorov-Smirnov band around an empirical distribution function."],
            "M": ["Compute growth functions of half-lines, intervals and half-planes and compare them with the "
                  "Sauer-Shelah bound.",
                  "Bound an expected uniform deviation by a Rademacher average and by Massart's finite-class "
                  "lemma.",
                  "Compute a covering number and evaluate Dudley's entropy integral for a simple class."],
            "D": ["Prove the symmetrization inequality and the Glivenko-Cantelli theorem for a VC class.",
                  "Prove Dudley's bound by chaining, and state the uniform-entropy and bracketing conditions "
                  "under which a class is Donsker.",
                  "Derive the limit of a Z-estimator when a nuisance parameter is estimated, and state the "
                  "rate theorem that gives cube-root asymptotics."],
            "I": ["Calibrate a goodness-of-fit test with fitted parameters by a parametric bootstrap, not by "
                  "Kolmogorov's table.",
                  "Choose a confidence band for a distribution function (exact, DKW, bootstrap) knowing which "
                  "undercovers at small n.",
                  "Read a uniform-deviation bound for a classifier and say why the actual excess risk is "
                  "usually far below it."],
        },
        results=[
            ("Symmetrization",
             r"\operatorname{E}\sup_{f\in\mathcal F}\bigl|P_nf-Pf\bigr|\le 2\,\operatorname{E}\sup_{f\in\mathcal F}"
             r"\Bigl|\frac1n\sum_{i=1}^n\varepsilon_if(X_i)\Bigr|"),
            ("Sauer-Shelah",
             r"\Pi_{\mathcal C}(n)\le\sum_{j=0}^{V}\binom nj\le\Bigl(\frac{en}{V}\Bigr)^{V}\qquad (n\ge V)"),
            ("Dudley's entropy integral",
             r"\operatorname{E}\sup_{t\in T}X_t\le K\int_0^{\operatorname{diam}T}\sqrt{\log N(\varepsilon,T,d)}\,"
             r"d\varepsilon"),
            ("Donsker and Kolmogorov",
             r"\sqrt n\,\sup_x|F_n(x)-F(x)|\Rightarrow\sup_{0\le t\le1}|B(t)|,\qquad "
             r"P\bigl(\sup|B|\le t\bigr)=1-2\sum_{k\ge1}(-1)^{k-1}e^{-2k^2t^2}"),
            ("DKW with Massart's constant",
             r"P\bigl(\sqrt n\,\sup_x|F_n(x)-F(x)|>t\bigr)\le 2e^{-2t^2}"),
            ("Durbin's variance with estimated mean and SD",
             r"\operatorname{Var}\to\Phi(z)\bigl(1-\Phi(z)\bigr)-\varphi(z)^2-\tfrac12\bigl(z\varphi(z)\bigr)^2"
             r"\quad\text{in place of}\quad\Phi(z)\bigl(1-\Phi(z)\bigr)"),
        ],
        U=(0,), I=(10, 12),
        also=(("statkit.empirical", "explainer/stats/kit/empirical.py"),),
    ),
]
