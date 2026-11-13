"""Stage II, Bachelor's: Methods (Parts 11-15)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=11, level="U", widget="waldsawtooth", prereq=(8, 10),
        question="What does '95% confident' promise, and which intervals keep it?",
        story="The part opens with the textbook interval for a proportion, the estimate plus or minus 1.96 standard "
              "errors, and computes its coverage exactly: it zigzags below 95% in a sawtooth, and at p = 0.005 one "
              "more observation (592 instead of 591) drops it from 94.5% to 79.2%. Neyman's definition says what "
              "was promised: coverage of at least 1 - alpha for every parameter value, a property of the procedure "
              "and not of the interval in hand. Pivots give exact intervals in the normal and exponential models, "
              "and inverting tests through Neyman's belt gives a confidence set for almost anything, including "
              "Wilson's and Clopper-Pearson's intervals for a proportion. The part then turns to what cannot be "
              "had: discrete data force a choice between a guarantee and an average, and Fieller's set for a ratio "
              "is sometimes two rays or the whole line, as it must be. It ends by separating confidence from "
              "prediction and from Bayesian credibility with Welch's two uniform draws, and by writing down the "
              "Coverage Board's protocol.",
        handoff="Inverted tests give the intervals of regression (Part 12) and of GLMs (Part 14); profile "
                "likelihood returns in Part 22, bootstrap intervals in Part 16, Wilks's order statistics as "
                "conformal prediction in Part 34, credible intervals in Part 15, and Fieller's unbounded sets as "
                "the weak-instrument problem of Part 37. Every later part adds rows to the Coverage Board.",
        outside="Calculus; the binomial, normal, t and chi-squared distributions of Stage I.",
        objectives={
            "U": ["Say what a 95% confidence interval promises and what it does not, and tell a confidence "
                  "interval from a prediction interval.",
                  "Compute Wald and Wilson intervals for a proportion, and apply the rule of three after zero "
                  "events."],
            "M": ["Build an interval from a pivot, and derive Wilson's and Clopper-Pearson's intervals by "
                  "inverting a test.",
                  "Compute an interval's exact binomial coverage, and explain why it jumps as p or n moves."],
            "D": ["Prove the duality between level-alpha tests and confidence sets, and explain why no "
                  "non-randomized interval for a binomial p has coverage exactly 95% at every p.",
                  "State what Gleser and Hwang's theorem requires of any honest confidence set for a ratio, and "
                  "work Welch's example of a relevant subset."],
            "I": ["Choose and report an interval for a rare proportion, a ratio or a new observation, saying "
                  "whether its coverage is guaranteed or approximate.",
                  "Run a coverage check by the Board's protocol, with its Monte Carlo standard error and "
                  "verdict rule."],
        },
        results=[
            ("Neyman's promise", r"P_\theta\bigl(\theta\in C(X)\bigr)\ \ge\ 1-\alpha\quad\text{for every }\theta"),
            ("Duality", r"C(x)=\{\theta_0:\ x\in A(\theta_0)\},\qquad A(\theta_0)\text{ the acceptance region of a "
                        r"level-}\alpha\text{ test of }\theta=\theta_0"),
            ("Wilson's interval", r"\frac{\hat p+\frac{z^2}{2n}}{1+\frac{z^2}{n}}\ \pm\ \frac{z}{1+\frac{z^2}{n}}"
                                  r"\sqrt{\frac{\hat p(1-\hat p)}{n}+\frac{z^2}{4n^2}}"),
            ("Fieller's set", r"\bigl\{\rho:\ (\bar y-\rho\bar x)^2\le z^2\,(v_y-2\rho\,c_{xy}+\rho^2 v_x)\bigr\},"
                              r"\qquad\text{bounded iff } g=\frac{z^2 v_x}{\bar x^2}<1"),
            ("Prediction interval", r"\bar x\ \pm\ t_{n-1,\,1-\alpha/2}\; s\,\sqrt{1+\tfrac{1}{n}}"),
            ("DKW band", r"P\Bigl(\sup_t\bigl|\hat F_n(t)-F(t)\bigr|>\varepsilon\Bigr)\le 2e^{-2n\varepsilon^2}"),
        ],
        U=(0, 1, 2, 4, 9), D=(7, 10), I=(11,),
        also=(("statkit.intervals", "explainer/stats/kit/intervals.py"),),
    ),
    Part(
        n=12, level="U", widget="leastsquares", prereq=(4, 8, 11),
        question="How do you fit a line through noise, and how sure are you of its slope?",
        story="On 1 January 1801 Piazzi finds Ceres and loses it in the Sun's glare; Gauss, twenty-four, says where "
              "it will reappear. The part takes his method apart. Least squares is a projection: the fitted values "
              "are the shadow of the data on the plane the predictors span, and everything else (the normal "
              "equations, R squared, the t and F tests) is Pythagoras in that picture. Gauss-Markov says the "
              "projection is the best linear unbiased guess when the noise is even; when it is not, the slope "
              "stays honest but its classical standard error lies, and White's sandwich repairs it. The part ends "
              "with what a regression cannot do: tell cause from company, or exempt anyone from regression to the "
              "mean.",
        handoff="The projection returns as ANOVA (Part 13), as the working step of every GLM (Parts 14, 24), and "
                "in full matrix generality in Part 23; 'controlling for' becomes a causal question in Parts 35-37.",
        outside="Calculus, and the matrix language of Part 4 (projections, rank, quadratic forms).",
        objectives={
            "U": ["Fit a line by least squares, read the coefficient table, and say in words what a slope and its "
                  "interval claim.",
                  "Read residual, leverage and QQ plots, and tell an outlier from an influential point."],
            "M": ["Derive the normal equations and the hat matrix, and prove Gauss-Markov.",
                  "Use Frisch-Waugh-Lovell to explain what 'controlling for' computes, and compute "
                  "omitted-variable bias."],
            "D": ["State exactly which assumptions each guarantee needs (unbiasedness, BLUE, exact t and F, "
                  "consistency of HC standard errors) and give a counterexample when each is dropped."],
            "I": ["Report a regression a reader can trust: robust standard errors, a prediction band rather "
                  "than a confidence band where one is meant, and no causal verb the design cannot support."],
        },
        results=[
            ("Normal equations", r"X^\top X\hat\beta = X^\top y,\qquad \hat y = Hy,\quad H = X(X^\top X)^{-1}X^\top"),
            ("Gauss-Markov", r"\operatorname{Var}(\tilde\beta)-\operatorname{Var}(\hat\beta)\succeq 0"
                             r"\quad\text{for every linear unbiased }\tilde\beta"),
            ("Frisch-Waugh-Lovell", r"\hat\beta_1=\frac{\tilde x_1^\top \tilde y}{\tilde x_1^\top \tilde x_1},"
                                    r"\qquad \tilde x_1=(I-H_2)x_1,\ \tilde y=(I-H_2)y"),
            ("White's sandwich", r"\widehat{\operatorname{Var}}(\hat\beta)=(X^\top X)^{-1}"
                                 r"\Bigl(\sum_i \hat e_i^2\,x_i x_i^\top\Bigr)(X^\top X)^{-1}"),
        ],
        U=(0, 1, 2, 6, 9, 11), I=(7, 8), D=(3,),
    ),
    Part(
        n=13, level="U", widget="fieldlayout", prereq=(10, 12),
        question="How should data be collected so that the answer is unambiguous?",
        story="In 1919 Fisher arrives at Rothamsted to analyse seventy-six years of Broadbalk wheat records, which "
              "can describe what happened but cannot isolate what a manure does. A simulated uniformity trial "
              "shows why: identically treated plots differ by about 8% of the mean, in patches, with a drift from "
              "west to east. On the field-trial simulator a tidy systematic layout is badly biased, randomization "
              "makes the estimate unbiased and supplies its own test, replication shrinks the error, and blocking "
              "removes the gradient from it. One-way ANOVA is Pythagoras, SST = SSB + SSW; contrasts and Tukey's "
              "HSD handle many comparisons; Latin squares, factorials, fractions of them and response surfaces on "
              "the island bakery spend runs carefully. The part turns on the split plot, where using the wrong "
              "error stratum rejects a true null 25.6% of the time, and ends with power, the minimum detectable "
              "effect, and the same principles in online A/B tests with CUPED and the sample-ratio check.",
        handoff="Permutation tests return in general in Part 16, survey design in Part 18, estimability in the "
                "linear model in Part 23 and split plots as mixed models in Part 25; potential outcomes take over "
                "randomization in Part 35, and sequential experiments come in Part 58.",
        outside="Calculus and the matrix language of Part 4; no agronomy is assumed.",
        objectives={
            "U": ["Explain what replication, randomization and blocking each buy, and lay out a randomized "
                  "complete block design.",
                  "Carry out a randomization test and a one-way ANOVA, and read the F table."],
            "M": ["Derive SST = SSB + SSW as a projection, and compute 2^k effects by Yates's algorithm.",
                  "Work out the aliases and resolution of a fractional factorial from its defining relation.",
                  "Analyse a split plot with the correct error stratum for each factor."],
            "D": ["State the Kiefer-Wolfowitz equivalence theorem for approximate designs and verify it for "
                  "quadratic regression on [-1, 1].",
                  "State exactly what a randomization test assumes (a sharp null, the actual assignment "
                  "mechanism) against what the normal-theory F test assumes."],
            "I": ["Plan a sample size from a minimum detectable effect, and explain why a significant result "
                  "from an underpowered study exaggerates.",
                  "Run an A/B test with CUPED adjustment and a sample-ratio check before reading the result."],
        },
        results=[
            ("The ANOVA identity", r"\sum_{i,j}(y_{ij}-\bar y)^2=\sum_i n_i(\bar y_i-\bar y)^2+\sum_{i,j}"
                                   r"(y_{ij}-\bar y_i)^2,\qquad F=\frac{SSB/(k-1)}{SSW/(N-k)}"),
            ("Replication", r"\operatorname{SE}(\bar y_A-\bar y_B)=\sigma\sqrt{2/n}"),
            ("A two-level effect", r"\widehat{AB}=\bar y_{AB=+}-\bar y_{AB=-},\qquad\text{aliased with }CD"
                                   r"\text{ under } I=ABCD"),
            ("D-optimal quadratic", r"\xi^*=\tfrac13\,\delta_{-1}+\tfrac13\,\delta_{0}+\tfrac13\,\delta_{1},\qquad"
                                    r"\det M(\xi^*)=\tfrac{4}{27},\quad \max_x d(x,\xi^*)=3"),
            ("Minimum detectable effect", r"\delta=(z_{1-\alpha/2}+z_{\text{power}})\,\sigma\sqrt{2/n}"),
            ("CUPED", r"\tilde y=y-\theta(x-\bar x),\quad \theta=\frac{\operatorname{Cov}(y,x)}"
                      r"{\operatorname{Var}(x)},\qquad \operatorname{Var}(\tilde y)=(1-\rho^2)\operatorname{Var}(y)"),
        ],
        U=(0, 1, 2, 3, 5, 7), D=(11,), I=(12, 13),
        also=(("statkit.design", "explainer/stats/kit/design.py"),),
    ),
    Part(
        n=14, level="U", widget="oringlogit", prereq=(10, 12),
        question="How do you regress a yes/no or a count, and read a table?",
        story="On the evening of 27 January 1986 the teleconference before Challenger's launch looks at the seven "
              "flights with O-ring distress, where temperature and damage are uncorrelated. Adding the sixteen "
              "flights with no distress, all launched at 66 F or warmer, shows the effect. A least-squares line "
              "through the 0/1 outcomes predicts a probability of 1.75 at the forecast 31 F, so the part builds "
              "logistic regression: log-odds linear in temperature, fitted by maximum likelihood, with Newton's "
              "method drawn as a sequence of weighted regressions. The Challenger fit puts the probability of "
              "distress at 31 F at 0.9996, with a profile interval of [0.80, 1] and an extrapolation caveat. "
              "Poisson regression does the same for counts, and overdispersion breaks its standard errors. The "
              "part turns to tables at Berkeley in 1973, where the pooled table and the department tables "
              "disagree (Simpson's paradox) and Mantel-Haenszel pools the strata, then to case-control studies "
              "with Doll and Hill, and ends by scoring forecasts with ROC curves, calibration and the Brier score.",
        handoff="The Challenger posterior is computed on a grid in Part 15; exact tests arrive in Part 16; GLMs "
                "get their full theory in Part 24 and clustered counts in Part 25; the causal reading of tables "
                "comes in Parts 35 and 36, and classification and scoring return in Parts 19 and 34.",
        outside="Calculus, logarithms and exponentials; the regression of Part 12.",
        objectives={
            "U": ["Explain why a straight line is the wrong model for a 0/1 outcome, and turn a logistic "
                  "coefficient into an odds ratio.",
                  "Compute an odds ratio, a relative risk and a chi-squared test from a 2 x 2 table, and "
                  "recognise Simpson's paradox in stratified rates."],
            "M": ["Derive the logistic score and Hessian, and carry out one IRLS step as a weighted regression.",
                  "Fit a Poisson regression with an offset, and compare classical, quasi-Poisson and sandwich "
                  "standard errors under overdispersion.",
                  "Pool stratified 2 x 2 tables by Mantel-Haenszel and test with CMH."],
            "D": ["Show why outcome-dependent sampling leaves the logistic slopes unchanged and shifts only the "
                  "intercept, and state what the Prentice-Pyke result adds.",
                  "Explain why the maximum likelihood estimate fails to exist under separation, and what that "
                  "does to Wald and likelihood-ratio inference."],
            "I": ["Report a logistic fit with a profile-likelihood interval, and flag a prediction that "
                  "extrapolates beyond the data.",
                  "Judge a probabilistic forecast by discrimination (AUC), calibration and the Brier score, and "
                  "say which of them a threshold decision needs."],
        },
        results=[
            ("The logistic model", r"\log\frac{p(x)}{1-p(x)}=\beta_0+\beta_1x,\qquad e^{\beta_1}="
                                   r"\text{the odds ratio per unit of }x"),
            ("Score and IRLS", r"X^\top(y-p)=0,\qquad \beta^{\text{new}}=(X^\top WX)^{-1}X^\top Wz,\quad "
                               r"W=\operatorname{diag}\,p_i(1-p_i),\ z=X\beta+W^{-1}(y-p)"),
            ("Odds ratio, Woolf's interval", r"\widehat{OR}=\frac{ad}{bc},\qquad \operatorname{SE}(\log\widehat{OR})"
                                             r"=\sqrt{\tfrac1a+\tfrac1b+\tfrac1c+\tfrac1d}"),
            ("Mantel-Haenszel", r"\widehat{OR}_{MH}=\frac{\sum_k a_kd_k/n_k}{\sum_k b_kc_k/n_k}"),
            ("Case-control sampling", r"\operatorname{logit}P(Y=1\mid x,\text{sampled})=\beta_0+"
                                      r"\log\frac{\pi_1}{\pi_0}+\beta_1x,\qquad \pi_y=P(\text{sampled}\mid Y=y)"),
            ("Brier score", r"\frac1n\sum_{i=1}^n(\hat p_i-y_i)^2"),
        ],
        U=(0, 1, 2, 4, 7, 8), D=(10,), I=(6, 11),
        also=(("statkit.glm", "explainer/stats/kit/glm.py"),),
    ),
    Part(
        n=15, level="U", widget="billiardbeta", prereq=(9, 11),
        question="What should you believe after seeing the data?",
        story="The part opens with Bayes's essay of 1763 and his billiard table: a hidden ball W, twelve more "
              "balls of which 8 stop to its left, and a posterior for W's position that is Beta(9, 5). Laplace "
              "applies the same reasoning to the Paris births and to the sunrise. The machinery is prior times "
              "likelihood, proportional to the posterior, and updating one ball at a time gives the same answer "
              "as updating all at once. Conjugate pairs (beta-binomial, gamma-Poisson, normal-normal) make the "
              "prior read as imaginary data; summaries, predictive distributions and the choice of prior follow, "
              "and the normal model under the reference prior returns Part 8's t interval exactly. When the "
              "algebra gives out, the Challenger posterior is computed on a grid and then by a Metropolis walk. "
              "The part turns when the Coverage Board judges credible intervals by frequency: a confident wrong "
              "prior covers a fixed truth 0% of the time, yet coverage averaged over the prior is exactly 95%. "
              "It ends with Bayes factors, which can favour the null, and Lindley's warning.",
        handoff="Bayesian computation returns in Parts 21 and 27, hierarchical models and shrinkage in Part 25, "
                "the Bayesian workflow and priors for testing in Part 26, model choice in Part 28, decision "
                "theory in Part 45, and the Bernstein-von Mises theorem in Part 53.",
        outside="Calculus (integrals of densities); the beta, gamma and normal distributions of Part 3.",
        objectives={
            "U": ["Update a beta prior with binomial data, and read the prior as imaginary successes and "
                  "failures.",
                  "Compute a posterior mean, a credible interval and the probability that the next trial "
                  "succeeds."],
            "M": ["Derive the gamma-Poisson and normal-normal updates, with precision weighting.",
                  "Compute a posterior on a grid, and by random-walk Metropolis with a sensible step size, and "
                  "check that the two agree.",
                  "Compute a Bayes factor for a point null against a beta alternative."],
            "D": ["Prove that an equal-tailed credible interval has exactly its nominal coverage on average "
                  "over the prior, and show by example that it can have coverage 0 at a fixed truth.",
                  "State Lindley's paradox: at a fixed p-value the Bayes factor moves towards the null as n "
                  "grows."],
            "I": ["Choose a prior and defend it with a prior predictive check and a sensitivity analysis.",
                  "Report a posterior with its interval and predictive distribution, and say what the answer "
                  "owes to the prior."],
        },
        results=[
            ("Bayes's rule for a parameter", r"\pi(\theta\mid y)=\frac{\pi(\theta)\,p(y\mid\theta)}"
                                             r"{\int\pi(t)\,p(y\mid t)\,dt}\ \propto\ \pi(\theta)\,p(y\mid\theta)"),
            ("Beta-binomial", r"p\sim\operatorname{Beta}(a,b),\ s\text{ successes in }n\ \Longrightarrow\ "
                              r"p\mid s\sim\operatorname{Beta}(a+s,\,b+n-s),\quad "
                              r"\mathbb{E}[p\mid s]=\frac{a+s}{a+b+n}"),
            ("Rule of succession", r"P(\text{next success}\mid s\text{ of }n,\ \text{uniform prior})="
                                   r"\frac{s+1}{n+2}"),
            ("Normal-normal", r"\frac{1}{\tau_n^2}=\frac{1}{\tau_0^2}+\frac{n}{\sigma^2},\qquad "
                              r"\mu_n=\tau_n^2\Bigl(\frac{\mu_0}{\tau_0^2}+\frac{n\bar x}{\sigma^2}\Bigr)"),
            ("Calibration over the prior", r"\int P_\theta\bigl(\theta\in C(Y)\bigr)\,\pi(\theta)\,d\theta=0.95"
                                           r"\quad\text{when } P\bigl(\theta\in C(y)\mid y\bigr)=0.95"
                                           r"\text{ for every }y"),
            ("Bayes factor, binomial", r"BF_{10}=\frac{B(a+s,\,b+n-s)/B(a,b)}{p_0^{\,s}(1-p_0)^{n-s}}"),
        ],
        U=(0, 1, 2, 3, 4), D=(9,), I=(5,),
        also=(("statkit.bayes", "explainer/stats/kit/bayes.py"),),
    ),
]
