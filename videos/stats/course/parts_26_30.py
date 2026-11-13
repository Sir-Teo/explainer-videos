"""Stage III, Master's: Bayes, computation, model choice, smoothing and robustness (Parts 26-30)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=26, level="M", widget="schoolstau", prereq=(15, 25),
        question="How do you build, fit and check a Bayesian model with many parameters, honestly?",
        story="Rubin's eight schools open the part: eight SAT coaching experiments with estimated effects from -3 to "
              "28 points and standard errors of 9 to 18. No pooling believes each estimate, complete pooling gives "
              "one effect of 7.7, and Part 25's empirical Bayes estimates a spread of zero and collapses to the "
              "second. The hierarchical model, justified by exchangeability and de Finetti's theorem, averages over "
              "the spread tau instead: its posterior is computed on a grid, and the tau explorer shows every "
              "school's estimate fanning out as tau grows. The part then asks what the prior on tau does (four "
              "priors, eight schools and three), states Bernstein-von Mises and where it fails, and computes Bayes "
              "factors until Lindley's paradox appears in the PEAR data: p = 0.0003 and a posterior probability of "
              "0.92 for the null. It turns to practice with decisions and the value of information, posterior and "
              "prior predictive checks, and simulation-based calibration, which catches a halved variance. It ends "
              "with the argument between the schools of inference stated honestly, and a first look at the "
              "Dirichlet process.",
        handoff="The posteriors that no grid can reach are computed in Part 27 (MCMC, HMC, Neal's funnel on these "
                "same schools); LOO, WAIC, BIC and stacking return in Part 28, shrinkage priors in Part 32, "
                "decision theory in Part 45, and Bernstein-von Mises is proved, with Bayesian nonparametrics, in "
                "Part 53.",
        outside="Part 15's one-parameter Bayes (conjugate updates, credible intervals) and Part 25's empirical "
                "Bayes; multivariate calculus for the Gaussian integrals.",
        objectives={
            "U": ["Explain no pooling, complete pooling and partial pooling on the eight schools, and say why "
                  "school A's 28 becomes about 10.",
                  "Read a posterior for tau and a posterior predictive check, and say what each does and does not "
                  "show."],
            "M": ["Derive the marginal posterior of tau in the hierarchical normal model and draw from the joint "
                  "posterior by tau, then mu, then the effects.",
                  "Compute the normal point-null Bayes factor, show Bartlett's and Lindley's paradoxes with it, "
                  "and state the Sellke-Bayarri-Berger bound.",
                  "Derive Jeffreys's prior and prove its invariance under reparametrization."],
            "D": ["State the conditions of Bernstein-von Mises and explain each of the part's failures (a mode on "
                  "the boundary, Neyman-Scott, nonparametric priors) as a condition dropped.",
                  "State what de Finetti's theorem gives and what it does not: infinite extendibility, and no "
                  "normal population."],
            "I": ["Run a Bayesian workflow: a prior predictive check, a fit, a posterior predictive check on a "
                  "feature the model was not built to match, and a sensitivity analysis over the prior on tau.",
                  "Validate posterior code by simulation-based calibration and say what uniform ranks cannot "
                  "detect."],
        },
        results=[
            ("The marginal posterior of tau",
             r"p(\tau\mid y)\propto p(\tau)\,V_\mu^{1/2}\prod_j(\sigma_j^2+\tau^2)^{-1/2}"
             r"\exp\Bigl\{-\frac{(y_j-\hat\mu)^2}{2(\sigma_j^2+\tau^2)}\Bigr\},"
             r"\qquad \hat\mu=\frac{\sum_j w_jy_j}{\sum_j w_j},\ V_\mu=\frac{1}{\sum_j w_j},\ "
             r"w_j=\frac{1}{\sigma_j^2+\tau^2}"),
            ("Partial pooling",
             r"\operatorname{E}(\theta_j\mid\mu,\tau,y)=\frac{\tau^2}{\sigma_j^2+\tau^2}\,y_j"
             r"+\frac{\sigma_j^2}{\sigma_j^2+\tau^2}\,\mu"),
            ("Jeffreys's prior", r"p(\theta)\propto\sqrt{\det I(\theta)},\qquad "
                                 r"\sqrt{I(\eta)}=\sqrt{I(\theta)}\,\Bigl|\frac{d\theta}{d\eta}\Bigr|"),
            ("The normal point-null Bayes factor",
             r"\mathrm{BF}_{01}=\sqrt{1+\frac{n\tau^2}{\sigma^2}}\;"
             r"\exp\Bigl\{-\frac{z^2}{2}\,\frac{n\tau^2}{\sigma^2+n\tau^2}\Bigr\}"),
            ("Sellke-Bayarri-Berger", r"\mathrm{BF}_{01}\ \ge\ -e\,p\log p\qquad (p<1/e)"),
            ("Tables in the Chinese restaurant",
             r"\operatorname{E}K_n=\sum_{i=0}^{n-1}\frac{\alpha}{\alpha+i}\approx\alpha\log\Bigl(1+\frac{n}{\alpha}\Bigr)"),
        ],
        U=(0, 1, 12), I=(10, 11), D=(13,),
        also=(("statkit.bayes", "explainer/stats/kit/bayes.py"),),
    ),
    Part(
        n=27, level="M", widget="funnelneck", prereq=(7, 26),
        question="How do you compute an integral you cannot do, in a hundred dimensions?",
        story="Los Alamos, 1953: Metropolis, the Rosenbluths and the Tellers move forty hard disks at random, reject "
              "the moves that overlap, and the lattice melts. The part builds the samplers that grew from that walk. "
              "Importance sampling reweights draws and fails quietly when the proposal's tails are too light; "
              "Metropolis-Hastings and Gibbs are exact in the limit but crawl, the Gibbs zigzag at correlation 0.95 "
              "earning 33 effective draws from 2,000 sweeps. Hamiltonian Monte Carlo sends a puck across the "
              "surface of minus the log posterior by leapfrog steps, and NUTS chooses the path length itself. The "
              "turn is Neal's funnel: the centred sampler never enters the neck, on the eight schools it reports "
              "47 divergences, and writing each effect as mu plus tau times a standard normal fixes it. The samplers "
              "are assembled into statkit.ppl, a small probabilistic programming language on AI, Built's "
              "autodiff, checked against closed forms. The part ends with the approximations and what each "
              "gives up: particle filters and tempering, variational inference, Laplace and INLA, ABC, and "
              "coupling from the past, which is exact.",
        handoff="PSIS becomes leave-one-out cross-validation in Part 28; NUTS fits the shrinkage priors of Part 32; "
                "the particle and Kalman filters return with state-space models in Part 38, INLA with Gaussian "
                "processes in Part 39, and the chains' mixing times are studied in Part 44.",
        outside="Part 7's Markov chains (stationary laws, detailed balance) and Part 26's posteriors; gradients "
                "and a little classical mechanics for the Hamiltonian chapters.",
        objectives={
            "U": ["Explain why accepting uphill moves always and downhill moves sometimes makes a random walk "
                  "visit each region in proportion to its probability.",
                  "Read a trace plot and an acceptance rate, and say what a step that is too small or too large "
                  "does to both."],
            "M": ["Prove detailed balance for Metropolis-Hastings and show that a leapfrog step preserves volume "
                  "and is reversible.",
                  "Derive the effective sample size of Gibbs sampling on a correlated normal, and the ELBO "
                  "identity.",
                  "Implement random-walk Metropolis and HMC for a log density, with the Jacobian of a log "
                  "transform."],
            "D": ["State the assumptions behind the 0.234 and 0.574 acceptance guidelines and why they are not "
                  "universal.",
                  "Explain why coupling from the past returns an exact draw and why monotonicity is needed to "
                  "run it."],
            "I": ["Diagnose a fit from rank-normalized split R-hat, bulk and tail ESS and divergences, knowing "
                  "that they detect failures and prove nothing.",
                  "Recognise a funnel in a hierarchical model and remove it by a non-centred parametrization.",
                  "Check an importance-sampling or variational approximation with the Pareto k-hat diagnostic."],
        },
        results=[
            ("Self-normalized importance sampling",
             r"\hat{\operatorname{E}}_\pi f=\frac{\sum_s w_sf(x_s)}{\sum_s w_s},\quad w_s=\frac{\pi(x_s)}{q(x_s)},"
             r"\qquad \mathrm{ESS}=\frac{(\sum_s w_s)^2}{\sum_s w_s^2}"),
            ("The Hastings ratio", r"\alpha(x,x')=\min\Bigl\{1,\ \frac{\pi(x')\,q(x\mid x')}{\pi(x)\,q(x'\mid x)}\Bigr\}"
                                   r"\ \Longrightarrow\ \pi(x)K(x\to x')=\pi(x')K(x'\to x)"),
            ("Gibbs on a correlated normal",
             r"x_1^{(t+1)}=\rho^2x_1^{(t)}+\text{noise},\qquad \frac{\mathrm{ESS}}{n}=\frac{1-\rho^2}{1+\rho^2}"),
            ("Leapfrog", r"p\leftarrow p-\tfrac{\varepsilon}{2}\nabla U(q),\quad q\leftarrow q+\varepsilon M^{-1}p,"
                         r"\quad p\leftarrow p-\tfrac{\varepsilon}{2}\nabla U(q),\qquad U=-\log\pi"),
            ("Non-centring", r"\theta_j=\mu+\tau z_j,\qquad z_j\sim N(0,1)"),
            ("The ELBO", r"\log p(y)=\operatorname{E}_q\log\frac{p(y,\theta)}{q(\theta)}"
                         r"+\operatorname{KL}\bigl(q\,\|\,p(\theta\mid y)\bigr)"),
        ],
        U=(0, 2), I=(4, 7, 8), D=(13,),
        also=(("statkit.ppl", "explainer/stats/kit/ppl.py"), ("AI, Built's autodiff", "explainer/ai/autodiff.py")),
    ),
    Part(
        n=28, level="M", widget="penaltybench", prereq=(19, 22, 26),
        question="How do you choose a model without fooling yourself?",
        story="In 1983 David Freedman regresses a hundred observations of noise on fifty columns of noise, keeps "
              "the columns that look promising and runs the regression again: the second round is significant "
              "95% of the time. The gap between how a chosen model fits and how it predicts is optimism, and the "
              "part measures it: 2 sigma squared d over n for least squares, and a covariance that defines degrees "
              "of freedom for any procedure. Cp and AIC estimate prediction error and are derived by two Taylor "
              "expansions; BIC comes from Laplace's method and answers a different question. On the model-selection "
              "bench, with Stamey's prostate data, AIC chooses seven predictors and BIC two, and two simulations "
              "show the trade: BIC finds a true quadratic 99% of the time at large n where AIC stays near 75%, "
              "and AIC predicts better at n = 1,000 when every candidate is wrong. "
              "Cross-validation, PSIS-LOO and WAIC do the same job by prediction, singular models break BIC's "
              "count of parameters, and stacking beats Bayesian model averaging when no candidate is true. The "
              "part ends with the cost of choosing (the naive interval after AIC covers 75%) and with forecasts "
              "judged by calibration and proper scores.",
        handoff="GCV and degrees of freedom choose the smoothing parameter in Part 29; the lasso's degrees of "
                "freedom and selection in high dimensions return in Part 32, conformal prediction in Part 34, "
                "oracle inequalities in Part 50, and inference after selection is done properly in Part 56.",
        outside="Part 19's cross-validation, Part 22's likelihood asymptotics (Taylor expansions around the MLE, "
                "Wilks's theorem) and Part 26's marginal likelihood.",
        objectives={
            "U": ["Explain Freedman's paradox: why a regression on screened noise looks significant, and what "
                  "splitting the data would have shown.",
                  "Read a curve of training error and test error against model size and say where optimism "
                  "comes from."],
            "M": ["Derive the optimism of a linear smoother from Efron's covariance formula, and the "
                  "leave-one-out shortcut from Sherman-Morrison.",
                  "Derive AIC as an estimate of expected Kullback-Leibler loss and BIC from Laplace's method, and "
                  "say which goal each serves.",
                  "Compute PSIS-LOO and WAIC from posterior draws and read the Pareto k-hat warnings."],
            "D": ["Compute the real log canonical threshold of a singular model by hand and state Watanabe's "
                  "free-energy expansion that replaces BIC's d/2.",
                  "State the conflict between consistency and minimax-rate efficiency (Yang 2005) and what it "
                  "does not rule out."],
            "I": ["Choose a model size by cross-validation with the search redone inside every fold, and apply "
                  "the one-standard-error rule.",
                  "Report inference after selection honestly: split the sample, or say that the naive interval "
                  "undercovers.",
                  "Judge a probabilistic forecast by its PIT histogram, log score and CRPS."],
        },
        results=[
            ("Optimism", r"\operatorname{E}(\mathrm{Err}_{\text{in}})-\operatorname{E}(\overline{\mathrm{err}})"
                         r"=\frac{2}{n}\sum_i\operatorname{Cov}(\hat y_i,y_i)=\frac{2\sigma^2\operatorname{tr}S}{n}"
                         r"\quad(\hat y=Sy)"),
            ("AIC and BIC", r"\mathrm{AIC}=-2\ell(\hat\theta)+2k,\qquad \mathrm{BIC}=-2\ell(\hat\theta)+k\log n"
                            r"\approx-2\log p(y\mid M)"),
            ("AIC overfits by one parameter", r"P\bigl(2(\ell_{k+1}-\ell_k)>2\bigr)\to P(\chi^2_1>2)=0.157"),
            ("The leave-one-out shortcut", r"y_i-x_i^\top\hat\beta_{-i}=\frac{y_i-\hat y_i}{1-h_{ii}},\qquad "
                                           r"\mathrm{GCV}=\frac{\mathrm{RSS}/n}{(1-\operatorname{tr}S/n)^2}"),
            ("Watanabe's free energy", r"-\log p(y\mid M)=-\ell(\theta_0)+\lambda\log n-(m-1)\log\log n+O_p(1)"),
            ("The log score is strictly proper", r"\operatorname{E}_g[-\log f(Y)]-\operatorname{E}_g[-\log g(Y)]"
                                                 r"=\operatorname{KL}(g\,\|\,f)\ \ge\ 0"),
        ],
        U=(0, 1), I=(9, 10, 11), D=(6,),
        also=(("statkit.select", "explainer/stats/kit/select.py"),),
    ),
    Part(
        n=29, level="M", widget="humpsbandwidth", prereq=(16, 23, 25),
        question="How do you estimate a whole curve, and how much data does it take?",
        story="Old Faithful's 272 eruption lengths have two humps, or twelve, or one, depending on the bandwidth; "
              "Silverman's critical bandwidths and his smoothed bootstrap reject one mode and do not reject two. "
              "The part then treats the picture as an estimator. A histogram's bias and variance balance at a bin "
              "width of order n to the minus one third; a kernel estimate does better, with squared error of "
              "order n to the minus four fifths, and Marron and Wand's exact MISE on a two-humped stand-in shows "
              "both rates arriving. Bandwidth selectors are raced, and the curse of dimensionality prices the same "
              "accuracy at 4 points in one dimension and 841,616 in ten. For regression the part builds local "
              "polynomials, proves that the penalized criterion is minimized by a natural cubic spline, turns the "
              "dial on the spline spectrum, and chooses lambda by GCV and REML on the motorcycle crash data. "
              "Reproducing kernels, wavelets and additive models follow. It ends with what smoothing costs "
              "inference: at the optimal bandwidth the conventional interval covers 91%, and robust bias correction "
              "restores 95%; and with shape constraints, where Grenander's estimator converges at the cube-root "
              "rate.",
        handoff="Robust smoothing follows in Part 30; local linear fits at a cutoff with robust bias correction "
                "become regression discontinuity in Part 37, kernels become Gaussian processes and kriging in "
                "Part 39, and Part 50 proves that the rates derived here cannot be beaten.",
        outside="Taylor expansions and integration by parts; Part 16's cross-validation, Part 23's linear model "
                "(hat matrices, ridge) and Part 25's mixed models and REML.",
        objectives={
            "U": ["Explain why a histogram or a kernel estimate changes with the bin or the bandwidth, and what "
                  "is traded when the bandwidth grows.",
                  "Explain the curse of dimensionality with the ball in the cube and the distance to the nearest "
                  "neighbour."],
            "M": ["Derive the bias and variance of a kernel density estimate, its AMISE, the optimal bandwidth "
                  "and the rate.",
                  "Prove the Reinsch-Schoenberg theorem and write a smoothing spline as ridge regression in the "
                  "Demmler-Reinsch basis.",
                  "Implement a kernel density estimate with a bandwidth selector and a local linear smoother."],
            "D": ["Prove the representer theorem and identify kernel ridge regression with a Gaussian process's "
                  "posterior mean.",
                  "Explain why Grenander's estimator has a cube-root rate and Chernoff's limit, and state the "
                  "smoothness classes under which each rate of the part holds."],
            "I": ["Choose a bandwidth or a smoothing parameter by Sheather-Jones, GCV or REML, and say why the "
                  "normal-reference rule oversmooths two humps.",
                  "Report a pointwise interval for a curve that covers: undersmooth or use robust bias "
                  "correction, and say that the band is pointwise."],
        },
        results=[
            ("The histogram", r"\mathrm{AMISE}=\frac{1}{nh}+\frac{h^2R(f')}{12},\qquad "
                              r"h^*=\Bigl(\frac{6}{nR(f')}\Bigr)^{1/3}"),
            ("The kernel estimate", r"\operatorname{bias}\approx\tfrac12h^2\mu_2f''(x),\qquad "
                                    r"\operatorname{Var}\approx\frac{f(x)R(K)}{nh}"),
            ("Its optimal bandwidth and rate",
             r"h^*=\Bigl(\frac{R(K)}{\mu_2^2R(f'')\,n}\Bigr)^{1/5},\qquad "
             r"\mathrm{AMISE}(h^*)=\tfrac54\bigl(\mu_2R(K)^2\bigr)^{2/5}R(f'')^{1/5}n^{-4/5}"),
            ("The curse of dimensionality", r"\mathrm{MISE}\asymp n^{-4/(4+d)}"),
            ("The smoothing spline", r"\hat g=\arg\min_g\sum_i\bigl(y_i-g(x_i)\bigr)^2+\lambda\int g''(x)^2\,dx"
                                     r"\ \Longrightarrow\ \hat g=(I+\lambda K)^{-1}y,\ \text{a natural cubic spline}"),
            ("The representer theorem", r"\hat f=\sum_j\alpha_jk(x_j,\cdot),\qquad \alpha=(K+\lambda I)^{-1}y"),
        ],
        U=(0, 4), I=(3, 7, 11), D=(8, 12),
        also=(("statkit.smooth", "explainer/stats/kit/smooth.py"),),
    ),
    Part(
        n=30, level="M", widget="strayrail", prereq=(16, 22, 23),
        question="What survives when a few observations are wrong, or the tails are heavier than the model admits?",
        story="In 1960 Tukey sets the standard deviation against the mean absolute deviation under a normal "
              "contaminated by a few observations with three times the spread: the textbook winner loses once "
              "one observation in 570 is a gross error. Newcomb's 66 passage times of light, with strays at -44 "
              "and -2, show the same thing on real data: the mean moves by a point and a half, the robust "
              "estimates barely at all, and none comes near the modern value. The part measures robustness three "
              "ways. Pitman efficiency: the Wilcoxon test never loses more than 13.6% against t, and the "
              "Hodges-Lehmann estimator inherits that. Influence: on the estimator rail one dragged point pulls "
              "the mean without limit and the median hardly at all. Breakdown: the share of bad points an "
              "estimate can absorb, from none for the mean to half for the median. Huber's minimax problem then "
              "produces the clipped psi, and the same ideas are carried to scale (MAD, Qn, Sn), regression (LTS "
              "and MM on the CYG OB1 stars, where least squares gets the slope's sign wrong), covariance (MCD) and "
              "heavy-tailed means (median of means, Catoni). It ends on the World, where 10% of heights recorded "
              "in inches break the t interval and the Hodges-Lehmann interval alike.",
        handoff="Robust covariance returns in Part 31 and heavy-tailed losses in Part 32; influence functions "
                "become the central tool of semiparametric theory in Part 49, the heavy-tailed bounds are proved "
                "by concentration in Part 51, and robustness in high dimensions, with Tukey depth, is Part 60.",
        outside="Part 16's rank tests and Walsh averages, Part 22's M-estimation asymptotics and Part 23's "
                "least squares with leverage; the calculus of variations is introduced where it is used.",
        objectives={
            "U": ["Explain on Newcomb's data why one stray observation moves the mean and the standard "
                  "deviation but not the median or the MAD.",
                  "Find the breakdown point of the mean, a trimmed mean and the median by replacing points "
                  "one at a time."],
            "M": ["Derive the Wilcoxon test's efficacy and its efficiency 3/pi at the normal, and the bound "
                  "108/125 by the calculus of variations.",
                  "Compute influence functions of the mean, median, trimmed mean and Huber's estimator, and the "
                  "Hodges-Lehmann breakdown point.",
                  "Derive Huber's least favourable distribution and implement his estimator by iteratively "
                  "reweighted least squares."],
            "D": ["Prove the median-of-means deviation bound from Chebyshev and Hoeffding, and say what Catoni's "
                  "estimator needs to know.",
                  "State the neighbourhood in which Huber's estimator is minimax and why a bounded influence "
                  "function does not imply a high breakdown point in regression."],
            "I": ["Flag outliers with a median and MAD rule and explain masking under the three-SD rule.",
                  "Fit a regression with a high-breakdown start (LTS or MM) and use its residuals and MCD "
                  "distances to find leverage points that least squares hides.",
                  "Say what robustness does not protect against: a systematic error common to the whole "
                  "sample."],
        },
        results=[
            ("Wilcoxon against t", r"\mathrm{ARE}(W,t)=12\,\sigma^2\Bigl(\int f^2\Bigr)^2:\quad "
                                   r"\frac{3}{\pi}\text{ at the normal},\qquad \ge\frac{108}{125}=0.864\text{ always}"),
            ("Influence functions at the normal",
             r"\mathrm{IF}_{\text{mean}}(z)=z,\qquad \mathrm{IF}_{\text{median}}(z)=\frac{\operatorname{sign}(z)}{2f(0)}"
             r"=\pm1.253,\qquad \mathrm{IF}_{\text{Huber}}(z)=\frac{\psi_k(z)}{2\Phi(k)-1}"),
            ("Breakdown points", r"\varepsilon^*_{\text{mean}}=0,\qquad \varepsilon^*_{\alpha\text{-trimmed}}=\alpha,"
                                 r"\qquad \varepsilon^*_{\text{HL}}=1-\tfrac{1}{\sqrt2}\approx0.293,"
                                 r"\qquad \varepsilon^*_{\text{median}}=\tfrac12"),
            ("Huber's minimax estimator",
             r"\psi_k(u)=\max(-k,\min(k,u)),\qquad \frac{2\varphi(k)}{k}-2\Phi(-k)=\frac{\varepsilon}{1-\varepsilon}"),
            ("Median of means", r"P\Bigl(|\hat\mu_{\text{MoM}}-\mu|>2\sigma\sqrt{k/n}\Bigr)\le e^{-k/8},"
                                r"\qquad k=\lceil 8\log(1/\delta)\rceil"),
        ],
        U=(0, 4), I=(6, 10), D=(9,),
        also=(("statkit.robust", "explainer/stats/kit/robust.py"),),
    ),
]
