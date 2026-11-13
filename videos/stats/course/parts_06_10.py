"""Stage I, Bachelor's: Foundations (Parts 6-10)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=6, level="U", widget="thirtyenough", prereq=(5,),
        question="Why does averaging work, how fast, and when does it fail?",
        story="At a Plymouth livestock fair, 787 legible guesses at the dressed weight of an ox have a median of "
              "1,207 lb against a true 1,198. The part proves why a crowd can do that: Markov, Chebyshev and Jensen, "
              "then the weak law in three lines, with Bernoulli's 1713 urn and his 25,550 trials set against modern "
              "bounds. The central limit theorem is seen by exact convolution and on a Galton board, then proved by "
              "expanding the log-MGF. The part turns when the folklore 'n at least 30' is tested: for the World's "
              "Pareto-tailed incomes the usual 95% interval still falls short at a thousand observations, and "
              "Berry-Esseen says how slowly the bell may arrive. The delta method and Slutsky's theorem make the "
              "normal approximation usable for every later part; Cauchy running means, which never settle, show "
              "where it stops. It ends with Hoeffding's inequality, the three laws of maxima, Port Pirie's 65 "
              "annual sea-level maxima, and van Dantzig's dike height after the 1953 North Sea flood.",
        handoff="Consistency is asked of every estimator from Part 9 on; the central limit theorem stands behind the "
                "intervals and tests of Parts 8, 10 and 11 and is proved in full in Part 43; its speed returns with "
                "the bootstrap in Part 16; the delta method gives the standard errors of Parts 9, 14, 18 and 22; "
                "concentration returns in Parts 51, 54 and 58, heavy tails in Parts 30 and 60, extremes in Parts 39 "
                "and 40.",
        outside="Calculus (limits, Taylor expansions), and the expectations, moment generating functions and joint "
                "laws of Parts 3 to 5.",
        objectives={
            "U": ["Compute a sample size three ways (Chebyshev, Hoeffding, the normal approximation) and say which "
                  "answers are guarantees.",
                  "Explain what the weak law and the central limit theorem each claim, and use the continuity "
                  "correction for a binomial count."],
            "M": ["Prove the weak law from Chebyshev's inequality and the central limit theorem by expanding the "
                  "log-MGF, and state what that proof assumed.",
                  "Derive the delta method, and use it with Slutsky's theorem to show that the t statistic is "
                  "asymptotically normal without normal data."],
            "D": ["Prove Hoeffding's inequality by Chernoff's trick and Hoeffding's lemma, and state what the "
                  "Lindeberg-Feller, stable and extreme-value limit theorems each require."],
            "I": ["Judge from the skewness over root n, not from n = 30, whether a normal interval for a mean can be "
                  "trusted, and say on which side it will miss.",
                  "Report a return level from annual maxima with a profile-likelihood interval, and name the "
                  "stationarity assumption it rests on."],
        },
        results=[
            ("Chebyshev and the weak law", r"P\bigl(|\bar X_n-\mu|\ge\varepsilon\bigr)\le"
                                           r"\frac{\sigma^2}{n\varepsilon^2}\;\longrightarrow\;0"),
            ("Central limit theorem", r"\frac{\sqrt n\,(\bar X_n-\mu)}{\sigma}\;\xrightarrow{d}\;N(0,1)"
                                      r"\qquad\text{(i.i.d., } 0<\sigma^2<\infty\text{)}"),
            ("Berry-Esseen", r"\sup_z\Bigl|P\Bigl(\tfrac{\sqrt n(\bar X_n-\mu)}{\sigma}\le z\Bigr)-\Phi(z)\Bigr|"
                             r"\le\frac{C\rho}{\sqrt n},\quad \rho=\tfrac{E|X-\mu|^3}{\sigma^3},\ C\le 0.4748"),
            ("Delta method", r"\sqrt n\,\bigl(g(\bar X_n)-g(\mu)\bigr)\;\xrightarrow{d}\;"
                             r"N\bigl(0,\;g'(\mu)^2\sigma^2\bigr)"),
            ("Hoeffding", r"P\bigl(|\bar X_n-\mu|\ge t\bigr)\le 2\exp\Bigl(-\frac{2nt^2}{(b-a)^2}\Bigr)"
                          r"\qquad\text{for } a\le X_i\le b"),
            ("Maxima of exponentials", r"P\bigl(\max_{i\le n}X_i-\log n\le x\bigr)=\bigl(1-e^{-x}/n\bigr)^n"
                                       r"\;\longrightarrow\;\exp\bigl(-e^{-x}\bigr)"),
        ],
        U=(0, 1, 2, 4, 6, 7, 10), I=(13,), D=(11,),
    ),
    Part(
        n=7, level="U", widget="randuplanes", prereq=(3, 6),
        question="How does a deterministic machine make randomness, and how do you run an honest simulation?",
        story="Von Neumann warned in 1951 that arithmetic randomness is a state of sin, and IBM's RANDU proved him "
              "right: turn its consecutive triples in a cube and every point falls on one of fifteen planes. The "
              "part builds a generator (Lehmer's congruences, then PCG32) and the tests that catch a bad one, then "
              "shapes uniforms into any law by the inverse CDF, rejection, Box-Muller, Marsaglia-Tsang and Walker's "
              "alias table. Monte Carlo integration has error sigma over root n in any dimension, from Buffon's "
              "needle to Lazzarini's suspicious 355/113. The part turns from making randomness to using it "
              "honestly: a simulation study is an experiment with a protocol (ADEMP), seeds, streams and a Monte "
              "Carlo standard error on every number, and the textbook interval for a proportion fails it. It ends "
              "with Markov chains: Markov's count of vowels in Onegin, stationary laws and PageRank, the riffle "
              "shuffle's cutoff near seven, and the Metropolis algorithm on a two-humped target.",
        handoff="statkit.random and the simulation harness run the sampling distributions of Part 8, the coverage "
                "of Part 11, the bootstrap of Part 16 and the thousands of tests of Part 33; importance sampling "
                "and Metropolis grow into Bayesian computation in Parts 15, 26 and 27; Markov chains return in "
                "time series (Part 17) and with full rigour in Part 44.",
        outside="Modular arithmetic and a little programming; the CDFs and densities of Part 3 and the laws of "
                "large numbers of Part 6. Chapters 8 to 10 use matrix multiplication and eigenvectors.",
        objectives={
            "U": ["Compute the period of a small congruential generator by hand, and explain why passing a "
                  "one-dimensional test did not save RANDU.",
                  "Derive an inverse-CDF sampler for the exponential, Pareto or logistic law, and the acceptance "
                  "rate 1/M of a rejection sampler."],
            "M": ["Prove that rejection sampling and Box-Muller give the laws they claim, and that a chain in "
                  "detailed balance with a law has it as a stationary law.",
                  "Compute the variance saved by antithetic pairs, a control variate and importance sampling on a "
                  "stated integral."],
            "D": ["Compute the total-variation distance of k riffle shuffles from uniform by the Bayer-Diaconis "
                  "formula, and state what the cutoff phenomenon claims about how the distance falls."],
            "I": ["Plan and report a simulation study by ADEMP: one recorded seed, a stream per scenario, the same "
                  "data sets for every method, and a Monte Carlo standard error beside every number.",
                  "Choose the number of replicates needed to resolve a stated difference in coverage."],
        },
        results=[
            ("RANDU's planes", r"x_{k+1}=65539\,x_k \bmod 2^{31}\ \Longrightarrow\ "
                               r"x_{k+2}\equiv 6x_{k+1}-9x_k \pmod{2^{31}}"),
            ("Inverse CDF", r"U\sim\operatorname{Unif}(0,1)\ \Longrightarrow\ P\bigl(F^{-1}(U)\le x\bigr)=F(x)"),
            ("Rejection sampling", r"X\sim g,\ \text{keep } X \text{ when } U\le\frac{f(X)}{M g(X)}:\qquad "
                                   r"X\mid\text{kept}\sim f,\quad P(\text{kept})=\frac1M"),
            ("Monte Carlo error", r"\operatorname{SE}\Bigl(\frac1n\sum_{i=1}^n g(X_i)\Bigr)=\frac{\sigma_g}{\sqrt n}"
                                  r"\ \text{ in any dimension};\qquad \operatorname{MCSE}(\hat c)="
                                  r"\sqrt{\frac{\hat c(1-\hat c)}{R}}"),
            ("Detailed balance", r"\pi_i P_{ij}=\pi_j P_{ji}\ \text{ for all } i,j\ \Longrightarrow\ \pi P=\pi"),
            ("Metropolis", r"y\sim q(\cdot\mid x)\ \text{symmetric};\quad \text{accept } y \text{ with probability } "
                           r"\min\Bigl(1,\frac{f(y)}{f(x)}\Bigr)"),
        ],
        U=(0, 1, 2, 3, 5, 8), I=(6,), D=(10,),
    ),
    Part(
        n=8, level="U", widget="studentcards", prereq=(4, 6, 7),
        question="How much does an estimate wobble from sample to sample, and how can one sample tell you?",
        story="In 1908 a Guinness brewer with four barley plots finds that the normal table lies for small samples. "
              "Gosset checks it by hand: 3,000 cards bearing the heights of Macdonell's prisoners, dealt into 750 "
              "samples of four. Redone in the film with one seeded shuffle, the interval with 1.96 covers 87.1% of "
              "the time and Student's multiplier 3.18 covers 96.7%. The part builds the sampling machine and the "
              "standard error, explains the n - 1 as an expectation and as a dimension, and follows Fisher's "
              "rotation of the sample, from "
              "which the independence of mean and variance, chi-squared, Cochran's theorem, Student's t and the F "
              "distribution all fall out. It then weighs bias against variance (the divisor n + 1 beats n - 1 in "
              "mean squared error), builds plug-in estimators and Laplace's ratio estimate of the population of "
              "France, and corrects for finite populations. It ends by opening the Coverage Board with seven rows, "
              "some kept and some broken, and with Box's 1953 warning that the t-test is fairly robust to "
              "non-normality while the F-test for variances is not.",
        handoff="Sampling distributions and standard errors carry Parts 9, 11 and 16; t, chi-squared, F and "
                "Cochran's theorem return in the tests of Part 10, in regression (Part 12), ANOVA (Part 13) and "
                "the linear model of Part 23; the bias-variance trade-off returns as shrinkage in Parts 25 and 29; "
                "ratio estimators and finite populations in Part 18; the Coverage Board in every part.",
        outside="Calculus, and from earlier parts: projections and orthogonal matrices (Part 4), the central limit "
                "theorem and the delta method (Part 6), simulation (Part 7).",
        objectives={
            "U": ["Compute a standard error and a Student's t interval for a mean, and explain why 1.96 is the "
                  "wrong multiplier when sigma is estimated from a few observations.",
                  "Explain the divisor n - 1 two ways: as what makes the sample variance unbiased, and as the "
                  "dimension of the space the residuals live in."],
            "M": ["Derive from Fisher's rotation that for normal samples the mean and variance are independent, "
                  "with a normal and a scaled chi-squared law, and obtain t and F from them.",
                  "Derive the delta-method standard error of a ratio of means, and the divisor that minimizes the "
                  "mean squared error of a variance estimate."],
            "D": ["State which normal-theory results survive without normality (the unbiasedness of the sample "
                  "variance, the asymptotic t) and which do not (independence of mean and variance, the "
                  "chi-squared law of the variance), with the role of kurtosis."],
            "I": ["Read a Coverage Board row: the method, the setting, the achieved coverage with its Monte Carlo "
                  "error, and the verdict.",
                  "Plan a sample size with the finite-population correction, and avoid testing variances by an "
                  "F-test on data that may not be normal."],
        },
        results=[
            ("Standard error and the n - 1", r"\operatorname{Var}(\bar x)=\frac{\sigma^2}{n},\qquad "
                                             r"E\,s^2=E\Bigl[\frac{1}{n-1}\sum_{i=1}^n (x_i-\bar x)^2\Bigr]=\sigma^2"),
            ("Fisher's geometry", r"x_i\overset{\text{iid}}{\sim}N(\mu,\sigma^2):\qquad \bar x\sim N\bigl(\mu,\tfrac{\sigma^2}{n}\bigr)"
                                  r"\ \perp\ \frac{(n-1)s^2}{\sigma^2}\sim\chi^2_{n-1}"),
            ("Student's t", r"\frac{\bar x-\mu}{s/\sqrt n}\sim t_{n-1},\qquad "
                            r"\bar x\pm t_{n-1,\,0.975}\,\frac{s}{\sqrt n}\ \text{ covers } \mu \text{ with probability } 0.95"),
            ("Mean squared error (normal samples)", r"\operatorname{MSE}=\operatorname{Var}+\operatorname{bias}^2;\qquad "
                                                    r"\operatorname{MSE}\bigl(\tfrac1c{\textstyle\sum}(x_i-\bar x)^2\bigr)"
                                                    r"\ \text{is least at } c=n+1"),
            ("Standard error of a ratio", r"\operatorname{SE}\Bigl(\frac{\bar y}{\bar x}\Bigr)\approx\frac{1}{|\mu_x|}"
                                          r"\sqrt{\frac{\sigma_y^2-2R\,\sigma_{xy}+R^2\sigma_x^2}{n}},\qquad R=\frac{\mu_y}{\mu_x}"),
            ("Finite-population correction", r"\operatorname{Var}(\bar x)=\frac{\sigma^2}{n}\cdot\frac{N-n}{N-1}"
                                             r"\qquad\text{(} n \text{ of } N \text{ drawn without replacement)}"),
        ],
        U=(0, 1, 2, 5, 7, 11), I=(10, 12),
    ),
    Part(
        n=9, level="U", widget="tankserials", prereq=(8,),
        question="How do you build a good estimator, and how good can any estimator be?",
        story="In the Second World War, serial numbers on captured tanks gave 169 for June 1940 where intelligence "
              "said 1,000 and the German records later showed 122 (Ruggles and Brodie 1947). The part plays that "
              "problem in miniature throughout: a factory of N tanks, a handful captured. Estimators are recipes "
              "judged by their sampling distributions; the method of moments and maximum likelihood produce them, "
              "with the score, invariance, the boundary MLE and Newton's method. Sufficiency says which part of "
              "the data matters, Rao-Blackwell turns the moment estimator 2 x-bar - 1 into the scaled maximum, and "
              "completeness makes that the best unbiased estimator: the maximum plus the average gap. Fisher "
              "information and the Cramer-Rao bound, proved by Cauchy-Schwarz, set a 1/sqrt(n) speed limit for "
              "regular unbiased estimation, and the tanks break it at rate 1/k because the support moves with N. "
              "It ends on an MSE board under three worlds, where the best estimator of the textbook model is off "
              "by a thousand once the serials do not start at 1.",
        handoff="Likelihood, the MLE and Fisher information carry Parts 10, 14, 22 and 24; Newton's method grows "
                "into Fisher scoring and EM in Parts 21 and 24; sufficiency, completeness and the UMVUE are proved "
                "in general in Part 45; Cramer-Rao and irregular rates return in Parts 47 and 50; misspecification "
                "and robustness in Parts 22 and 30; the tank factory game grades estimators in later parts.",
        outside="Calculus (maximizing a function, Taylor's theorem), and the sampling distributions, bias and mean "
                "squared error of Part 8.",
        objectives={
            "U": ["Compute the moment estimate, the maximum likelihood estimate and the unbiased estimate of N "
                  "from a handful of serial numbers, and say what each one's sampling distribution looks like.",
                  "Write down a likelihood, maximize it for the normal, Poisson, exponential and uniform models, "
                  "and read a standard error off its curvature."],
            "M": ["Prove the factorization theorem in the discrete case and the Rao-Blackwell theorem, and "
                  "Rao-Blackwellize a given unbiased estimator.",
                  "Derive the Cramer-Rao bound by Cauchy-Schwarz, compute Fisher information for standard "
                  "models, and say when the bound is attained."],
            "D": ["Prove that the tank maximum is complete, apply Lehmann-Scheffe, and explain which regularity "
                  "condition fails when an estimator converges at rate 1/n and beats the Cramer-Rao rate."],
            "I": ["Grade an estimator by simulation on the model it assumed and on models it did not, reporting "
                  "bias, standard deviation and RMSE with Monte Carlo errors.",
                  "Choose between an efficient estimator and a robust one by naming the assumption each depends on."],
        },
        results=[
            ("The tank UMVUE (m the largest of k serials)", r"\hat N=m\bigl(1+\tfrac1k\bigr)-1:\qquad E\,\hat N=N,\quad "
                                                            r"\operatorname{Var}(\hat N)=\tfrac{(N-k)(N+1)}{k(k+2)}"),
            ("Maximum likelihood, large n", r"\sqrt n\,(\hat\theta-\theta)\xrightarrow{d}N\bigl(0,I(\theta)^{-1}\bigr),\qquad "
                                            r"\operatorname{SE}(\hat\theta)\approx\bigl(-\ell''(\hat\theta)\bigr)^{-1/2}"),
            ("Factorization", r"T \text{ is sufficient}\iff p_\theta(x)=g_\theta\bigl(T(x)\bigr)\,h(x)"),
            ("Rao-Blackwell", r"\tilde\delta=E(\delta\mid T),\ T \text{ sufficient}:\qquad E\,\tilde\delta=E\,\delta,\quad "
                              r"\operatorname{Var}(\tilde\delta)\le\operatorname{Var}(\delta)"),
            ("Fisher information", r"u(\theta)=\frac{\partial}{\partial\theta}\log p_\theta(X):\qquad E\,u=0,\qquad "
                                   r"I(\theta)=\operatorname{Var}(u)=-E\,\frac{\partial u}{\partial\theta}"),
            ("Cramer-Rao", r"E_\theta T=\psi(\theta)\ \Longrightarrow\ \operatorname{Var}_\theta(T)\ge"
                           r"\frac{\psi'(\theta)^2}{n\,I(\theta)}\qquad\text{(regular models)}"),
        ],
        U=(0, 1, 3, 4), I=(11,), D=(8,),
    ),
    Part(
        n=10, level="U", widget="peekpaths", prereq=(8, 9),
        question="When is a pattern too strong to be chance?",
        story="In 1710 Arbuthnot finds more boys than girls christened in London in each of 82 years, a (1/2)^82 "
              "event if every year were a fair coin; in 1935 Fisher's lady has 1 chance in 70 of picking out four "
              "milk-first cups by guessing. The part builds Fisher's logic (a null, a statistic, a tail "
              "probability) and the exact tests that randomization itself supplies, from the tea to Darwin's maize "
              "and the permutation machine, and proves the p-value uniform under the null. Neyman and Pearson add "
              "the alternative: two kinds of error, power, and the lemma that the likelihood ratio gives the most "
              "powerful test, found here as a knapsack over all 2,048 rejection regions of a dice problem. The "
              "likelihood ratio test with Wilks' theorem, the everyday z and t tests, Welch's repair and Pearson's "
              "chi-squared follow, with Mendel's peas fitting too well. Then the part turns to how tests go wrong: "
              "too little power, peeking after every observation (29% false alarms by n = 100), reading p as the "
              "probability of the null, and testing many things at once.",
        handoff="Tests are inverted into confidence intervals in Part 11 and again in Part 46; permutation "
                "inference returns in Parts 13, 16 and 35; the likelihood ratio, Wald and score tests in Parts 14, "
                "22 and 24; power and design in Parts 13 and 35; sequential and anytime-valid testing in Parts 35 "
                "and 58; multiple testing and the false discovery rate in Parts 33 and 56.",
        outside="Counting (binomial coefficients), and from earlier parts: the t, chi-squared and F distributions "
                "of Part 8 and the likelihood of Part 9.",
        objectives={
            "U": ["Carry out a sign test, Fisher's exact test and a t-test, and state the null hypothesis each "
                  "one tests.",
                  "Say what a p-value is, and explain why it is not the probability that the null is true."],
            "M": ["Prove that a p-value is uniform under a continuous null, and prove the Neyman-Pearson lemma "
                  "for simple hypotheses.",
                  "Derive the likelihood ratio statistic for a one-parameter model and compare it with the Wald "
                  "and score tests on the same data."],
            "D": ["State when a uniformly most powerful test exists (a monotone likelihood ratio, a one-sided "
                  "alternative), and what a randomization test needs from the design to be valid without a model."],
            "I": ["Compute the sample size for a stated power, and the type S and type M errors of an "
                  "underpowered study.",
                  "Recognize what breaks a test's size (peeking, a pooled variance with unequal spreads, many "
                  "tests) and name the repair for each."],
        },
        results=[
            ("The tea, and Arbuthnot's 82 years", r"\binom{8}{4}^{-1}=\frac{1}{70},\qquad "
                                                  r"\bigl(\tfrac12\bigr)^{82}\approx 2.1\times10^{-25}"),
            ("The p-value is uniform", r"P_{H_0}(p\le u)=u\ \text{(continuous null)},\qquad "
                                       r"P_{H_0}(p\le u)\le u\ \text{(discrete)}"),
            ("Neyman-Pearson lemma", r"\text{reject when }\frac{p_1(x)}{p_0(x)}>c:\ \text{no test of the same size "
                                     r"has more power against } p_1"),
            ("Wilks' theorem", r"W=2\bigl[\ell(\hat\theta)-\ell(\theta_0)\bigr]\;\xrightarrow{d}\;\chi^2_r"
                               r"\quad\text{under } H_0\ \text{(} r \text{ parameters fixed by } H_0\text{)}"),
            ("Welch's t", r"t=\frac{\bar x-\bar y}{\sqrt{s_1^2/n_1+s_2^2/n_2}},\qquad "
                          r"\nu=\frac{\bigl(s_1^2/n_1+s_2^2/n_2\bigr)^2}"
                          r"{\frac{(s_1^2/n_1)^2}{n_1-1}+\frac{(s_2^2/n_2)^2}{n_2-1}}"),
            ("Sample size for power", r"n=\Bigl(\frac{(z_{1-\alpha/2}+z_{1-\beta})\,\sigma}{\delta}\Bigr)^2"
                                      r"\qquad\text{(one mean, two-sided level } \alpha\text{, power } 1-\beta\text{)}"),
        ],
        U=(0, 1, 2, 3, 4, 7, 11), I=(9, 10, 12),
    ),
]
