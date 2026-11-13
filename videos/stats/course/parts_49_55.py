"""Stage IV, PhD core: efficiency, minimax theory, high dimensions, Bayes, learning theory, the exam (Parts 49-55)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=49, level="D", widget="tangentgain", prereq=(36, 47, 48),
        question="How well can you estimate one number when the rest of the model is infinite dimensional?",
        story="In 1956 Stein asks whether the centre of a symmetric distribution can be estimated as well without "
              "knowing its shape; Stone (1975) and Bickel (1982) answer yes, and a simulation over five symmetric "
              "laws shows a density-score estimator, never told the law, near the bound 1/I_f in every row. The "
              "part builds the theory that explains it. A model's tangent space is the set of directions it can "
              "move, drawn to scale for a 2 x 2 table under independence; a functional's pathwise derivative is "
              "an inner product with a gradient, and the efficient influence function is that gradient projected "
              "onto the tangent space, whose variance is the bound. The mean, quantiles, the ATE and ATT, "
              "Robinson's partially linear model and Cox's partial likelihood are worked, and projecting the "
              "score off the nuisance tangent space gives the efficient score and explains adaptation. The part "
              "then turns to estimators: the one-step, estimating equations and TMLE remove the plug-in's "
              "first-order bias, double robustness is the product form of the second-order remainder, and "
              "cross-fitting with the product rate is what double machine learning needs. It ends with missing "
              "data under MAR, higher-order influence functions for the integrated squared density, and the "
              "World test, where the plug-in's 90% interval covers 3% of the time and the cross-fitted one-step "
              "and TMLE keep their level.",
        handoff="Part 50 asks for the rate when root-n is impossible; the same one-step correction returns as the "
                "debiased lasso in Part 52 and as the semiparametric Bernstein-von Mises theorem in Part 53; "
                "double robustness returns under distribution shift in Part 60 and in proximal causal inference "
                "and policy learning in Part 62; Problem 8 of the qualifying exam (Part 55) is an efficient "
                "influence function.",
        outside="Hilbert-space geometry (L2 projections), Part 47's LAN and convolution theorem, Part 48's "
                "empirical processes, and the causal estimators of Part 36.",
        objectives={
            "U": ["Explain Stein's question and read the table of five symmetric laws: which estimator is near "
                  "the bound in every row, and what it was never told."],
            "M": ["Compute an efficient influence function on a finite sample space by projecting a gradient onto "
                  "the tangent space, and read its variance as the bound.",
                  "Derive the influence functions of the mean, a quantile and the ATE, and show that the one-step "
                  "estimator's bias is a product of two nuisance errors."],
            "D": ["State the semiparametric convolution theorem and prove that the efficient influence function "
                  "is the unique gradient lying in the tangent space.",
                  "Prove that a cross-fitted one-step estimator is root-n and efficient when the product of the "
                  "nuisance rates is of smaller order than n to the minus one half, and say what fails at "
                  "equality."],
            "I": ["Estimate an ATE by one-step and TMLE with cross-fitted nuisances and influence-function "
                  "standard errors, and report which nuisance models the interval relies on.",
                  "Diagnose a plug-in estimator with machine-learned nuisances: explain why its interval "
                  "undercovers and what the correction term adds."],
        },
        results=[
            ("Pathwise derivative and the efficient influence function",
             r"\frac{d}{dt}\psi(P_t)\Big|_{t=0}=\operatorname{E}[\varphi(X)\,s(X)],\qquad "
             r"\varphi^*=\Pi(\varphi\mid\dot{\mathcal P}),\qquad "
             r"\operatorname{avar}(\hat\psi)\ \ge\ \operatorname{E}[\varphi^{*2}]"),
            ("The ATE's efficient influence function (Hahn 1998)",
             r"\varphi^*=\mu_1(X)-\mu_0(X)-\psi+\frac{T\,(Y-\mu_1(X))}{e(X)}-\frac{(1-T)(Y-\mu_0(X))}{1-e(X)},"
             r"\qquad \operatorname{E}[\varphi^{*2}]=\operatorname{Var}\tau(X)+\operatorname{E}\Bigl[\frac{\sigma_1^2(X)}{e(X)}"
             r"+\frac{\sigma_0^2(X)}{1-e(X)}\Bigr]"),
            ("The efficient score",
             r"\ell^*=\dot\ell_\theta-\Pi(\dot\ell_\theta\mid\Lambda_{\text{nuisance}}),\qquad "
             r"I^*=\operatorname{E}[\ell^{*2}]\ \le\ I_\theta"),
            ("The one-step estimator", r"\hat\psi=\psi(\hat P)+\frac1n\sum_{i=1}^n\varphi^*_{\hat P}(X_i)"),
            ("Double robustness: the one-step's bias",
             r"\operatorname{E}\Bigl[\frac{(e-\hat e)(\mu_1-\hat\mu_1)}{\hat e}\Bigr]"
             r"-\operatorname{E}\Bigl[\frac{(\hat e-e)(\mu_0-\hat\mu_0)}{1-\hat e}\Bigr]"),
            ("The product rate",
             r"\|\hat e-e\|\,\|\hat\mu-\mu\|=o_P(n^{-1/2})\quad\text{(for rates } n^{-a},\,n^{-b}:\ a+b>\tfrac12)"),
        ],
        U=(0,), I=(6, 9, 11),
    ),
    Part(
        n=50, level="D", widget="pinskertaper", prereq=(29, 45, 47),
        question="How well can anyone estimate a function, with any method at all?",
        story="The part opens with Farrell (1972) and Stone (1980): with s derivatives in d dimensions no method "
              "of any kind estimates a function faster than n to the power -2s/(2s+d), which is the promise Part "
              "29 took on trust when it found n^(-4/5). The Gaussian sequence model is set up and shown to stand "
              "for regression and density estimation (Brown and Low, Nussbaum). Over a Sobolev ellipsoid Pinsker "
              "finds the exact linear minimax risk, its tapered rule and its least favourable Gaussian prior, and "
              "a hard cut-off is shown to lose the factor 3^(2/3). Lower bounds are then built on a workbench of "
              "hypotheses: Le Cam's two points for a density at a point, Fano's packings with Varshamov-Gilbert "
              "for sparse vectors, Assouad's hypercube of bumps for Holder regression. Blockwise James-Stein and "
              "thresholding give upper bounds that match, and Lepski's method adapts to unknown smoothness at a "
              "price for pointwise loss. The part turns to testing, with Ingster's separation rates, the "
              "sparse-mixture detection boundary and higher criticism, and to planted clique and sparse PCA, where "
              "rates achievable in principle seem out of reach of efficient algorithms. It ends on the Board: "
              "an interval at Lepski's bandwidth covers 44% of the time at a peak, and only the bias-aware "
              "interval has a guarantee over the whole class.",
        handoff="Part 51 supplies the concentration and chaining the bounds rest on; the lasso attains Fano's "
                "s log(p/s) in Part 52; posterior contraction rates match these minimax rates in Part 53; "
                "learning-theory lower bounds use VC dimension and Fano in Part 54; Problem 9 of the qualifying "
                "exam (Part 55) is a Fano bound; the minimax price of differential privacy is Part 63.",
        outside="Part 29's smoothing (bias, variance, bandwidths), Part 45's decision theory (Bayes and minimax "
                "risk), Part 47's local asymptotics, and Fourier series.",
        objectives={
            "U": ["Explain what a minimax rate claims: a speed limit for every method over a class of functions, "
                  "and why Part 29's rate n^(-4/5) is such a limit."],
            "M": ["Compute Pinsker's taper, its risk and its least favourable prior over a Sobolev ellipsoid, and "
                  "compare them with the best projection estimator.",
                  "Compute total variation, Hellinger and KL between two normals and use Le Cam's two-point "
                  "bound on a pair of hypotheses."],
            "D": ["Prove a lower bound three ways (Le Cam's two points, Fano with a Varshamov-Gilbert packing, "
                  "Assouad's hypercube) and say which loss and which class each suits.",
                  "State the price of adaptation for pointwise loss and why no confidence interval can be both "
                  "adaptive and honest over a union of smoothness classes.",
                  "State the planted-clique conjecture and what low-degree evidence does and does not prove about "
                  "statistical-computational gaps."],
            "I": ["Choose between an undersmoothed, a Lepski and a bias-aware interval for a curve at a point, "
                  "and report which class of functions the stated coverage holds over.",
                  "Calibrate higher criticism by simulation rather than by its leading null scale, and report its "
                  "size."],
        },
        results=[
            ("The Gaussian sequence model on an ellipsoid",
             r"y_k=\theta_k+\varepsilon z_k,\quad z_k\overset{\text{iid}}{\sim}N(0,1),\qquad "
             r"\Theta=\Bigl\{\theta:\ \sum_k a_k^2\theta_k^2\le C^2\Bigr\},\ a_k=k^\alpha"),
            ("Pinsker's theorem",
             r"\hat\theta_k=\Bigl(1-\frac{a_k}{\mu}\Bigr)_+y_k,\quad "
             r"\varepsilon^2\sum_k a_k(\mu-a_k)_+=C^2,\quad "
             r"R_L=\varepsilon^2\sum_k\Bigl(1-\frac{a_k}{\mu}\Bigr)_+\sim "
             r"P(\alpha)\,C^{\frac{2}{2\alpha+1}}\varepsilon^{\frac{4\alpha}{2\alpha+1}},\quad "
             r"P(\alpha)=(2\alpha+1)^{\frac{1}{2\alpha+1}}\Bigl(\frac{\alpha}{\alpha+1}\Bigr)^{\frac{2\alpha}{2\alpha+1}}"),
            ("Le Cam's two-point bound",
             r"|\theta_1-\theta_0|=2\delta\ \Longrightarrow\ \max_{j\in\{0,1\}}\operatorname{E}_j(\hat\theta-\theta_j)^2"
             r"\ \ge\ \frac{\delta^2}{2}\,\bigl(1-\operatorname{TV}(P_0,P_1)\bigr)"),
            ("Fano's bound",
             r"\inf_{\psi}\max_{j\le M}P_j(\psi\ne j)\ \ge\ 1-\frac{\max_{j,k}\operatorname{KL}(P_j\,\|\,P_k)+\log 2}{\log M}"),
            ("Stone's rate", r"\inf_{\hat f}\sup_{f\in\mathcal F_s}\operatorname{E}\|\hat f-f\|_2^2\ \asymp\ n^{-2s/(2s+d)}"),
            ("The detection boundary (Ingster; Donoho and Jin)",
             r"\varepsilon=n^{-\beta},\ \mu=\sqrt{2r\log n}:\qquad \rho^*(\beta)=\begin{cases}\beta-\tfrac12,&\tfrac12<\beta\le\tfrac34\\"
             r"(1-\sqrt{1-\beta})^2,&\tfrac34<\beta<1\end{cases}"),
        ],
        U=(0,), I=(10,),
    ),
    Part(
        n=51, level="D", widget="equatorband", prereq=(43, 48),
        question="What does randomness look like in a thousand dimensions?",
        story="The part opens with Levy's equator: a point drawn uniformly from the sphere in a thousand dimensions "
              "has its first coordinate within 0.062 of zero with probability 95%, for any coordinate fixed in "
              "advance. From that picture it builds the non-asymptotic toolkit. Sub-Gaussian and sub-exponential "
              "variables and their Orlicz norms give Hoeffding, Bernstein and Chernoff bounds, set against exact "
              "binomial tails; thin shells, near-orthogonality and Johnson-Lindenstrauss follow. Lipschitz functions "
              "of Gaussians concentrate (Tsirelson, Ibragimov and Sudakov, by Herbst's argument), which gives the "
              "singular values of an n by p Gaussian matrix as root n plus or minus root p, covariance estimation "
              "at the rate of the square root of p/n, and a real correlation spectrum read against Marchenko-Pastur. Matrix "
              "Bernstein, Dudley's integral with Sudakov's minoration, and the comparison inequalities of Slepian, "
              "Sudakov-Fernique and Gordon lead to Gaussian widths and the escape through the mesh. The part turns "
              "there to Part 32's experiment: the statistical dimension of the l1 descent cone computes the "
              "Donoho-Tanner curve. It ends on the Board, where a Wald interval for a rare proportion covers 90.9% "
              "and the Hoeffding interval is valid and five times wider.",
        handoff="These are the proofs of Part 52: the maximum of p Gaussians sets the lasso's penalty, Gordon's "
                "inequality gives restricted eigenvalues, matrix Bernstein drives matrix completion. Rademacher "
                "complexity and contraction return in Part 54, confidence sequences in Part 58, Marchenko-Pastur "
                "and the convex Gaussian min-max theorem in Part 59; Problem 10 of the qualifying exam (Part 55) is "
                "a matrix Bernstein bound.",
        outside="Part 43's measure-theoretic probability (moment generating functions, the CLT, large deviations), "
                "Part 48's chaining, and linear algebra (singular values, operator norm).",
        objectives={
            "U": ["Explain the equator picture: why one coordinate of a random point on a high-dimensional sphere "
                  "is about normal with variance 1/n, and why that does not hold for all equators at once."],
            "M": ["Compute Hoeffding, Bernstein and Chernoff bounds for a binomial mean and compare them with the "
                  "exact tail.",
                  "Predict the largest and smallest singular values of a Gaussian matrix and the operator-norm "
                  "error of a sample covariance from n and p."],
            "D": ["Prove Gaussian concentration for Lipschitz functions by Herbst's argument and derive from it "
                  "the bound on a Gaussian matrix's extreme singular values.",
                  "Prove Dudley's bound and Sudakov's minoration, and state Slepian's, Sudakov-Fernique's and "
                  "Gordon's inequalities with what each compares.",
                  "Derive the phase transition of basis pursuit from Gordon's escape through the mesh and the "
                  "statistical dimension of the descent cone."],
            "I": ["Choose between a Wald, a Hoeffding and an empirical Bernstein interval for a bounded mean, and "
                  "report what each assumes and what it costs in width.",
                  "Read a sample correlation spectrum against the Marchenko-Pastur edge and a permutation null "
                  "without mistaking the count of large eigenvalues for a number of factors."],
        },
        results=[
            ("One coordinate on the sphere",
             r"x\sim\operatorname{Unif}(S^{n-1}):\quad f_{x_1}(u)=c_n(1-u^2)^{\frac{n-3}{2}},\qquad "
             r"P(|x_1|\ge t)\le 2e^{-nt^2/2}"),
            ("Hoeffding and Bernstein",
             r"P(\bar X-\mu\ge t)\le\exp\Bigl(-\frac{2nt^2}{(b-a)^2}\Bigr),\qquad "
             r"P(\bar X-\mu\ge t)\le\exp\Bigl(-\frac{nt^2}{2(\sigma^2+bt/3)}\Bigr)"),
            ("Gaussian concentration",
             r"f\ L\text{-Lipschitz},\ g\sim N(0,I_n):\qquad P\bigl(f(g)-\operatorname{E}f(g)\ge t\bigr)\le e^{-t^2/(2L^2)}"),
            ("Extreme singular values of a Gaussian matrix",
             r"\sqrt n-\sqrt p\ \le\ \operatorname{E}s_{\min}(X)\ \le\ \operatorname{E}s_{\max}(X)\ \le\ \sqrt n+\sqrt p"),
            ("Matrix Bernstein (Tropp 2012)",
             r"\operatorname{E}\Bigl\|\sum_i X_i\Bigr\|\le\sqrt{2v\log(2p)}+\tfrac13L\log(2p),\qquad "
             r"v=\Bigl\|\sum_i\operatorname{E}X_i^2\Bigr\|,\ \|X_i\|\le L"),
            ("The statistical dimension of the l1 descent cone",
             r"\delta\ \le\ \inf_{\tau\ge0}\Bigl\{s(1+\tau^2)+(p-s)\operatorname{E}\bigl(|g|-\tau\bigr)_+^2\Bigr\},"
             r"\qquad \text{basis pursuit succeeds when } m\gtrsim\delta"),
        ],
        U=(0,), I=(10,),
    ),
    Part(
        n=52, level="D", widget="bbpspike", prereq=(31, 32, 51),
        question="What can be estimated, and how fast, when parameters outnumber observations?",
        story="The part opens with principal components on pure noise: a thousand observations of five hundred "
              "independent variables have sample eigenvalues from 0.085 to 2.92 where every true eigenvalue is 1. "
              "It first proves what Part 32 showed by experiment. The lasso's oracle inequality follows from the "
              "basic inequality, the cone and a restricted eigenvalue; the primal-dual witness says when the "
              "signed support is recovered; decomposable regularizers give one theorem for sparse, group and "
              "low-rank problems, and matrix completion is worked on a rank-3 matrix. The part then turns to "
              "covariance. Banding, thresholding and Ledoit-Wolf beat the sample covariance, Davis-Kahan bounds an "
              "eigenvector's rotation by the perturbation over the gap, and the Stieltjes transform gives the "
              "Marchenko-Pastur and semicircle laws. In the spiked model a signal below the square root of p/n is "
              "invisible to PCA and above it the top eigenvalue is biased by a known map (BBP), read on Harman's "
              "24 tests; the edge fluctuates on the Tracy-Widom scale, which calibrates Roy's test. It ends with "
              "sparse PCA and its computational barrier, neighbourhood selection, and the debiased lasso on the "
              "diabetes data with its caveats stated.",
        handoff="Posterior contraction for sparse priors at these rates is in Part 53, learning bounds in high "
                "dimensions in Part 54, selective inference after the lasso in Part 56, the lasso's exact risk "
                "when p/n tends to a constant in Part 59, and causal adjustment for many confounders in Part 62; "
                "Problem 11 of the qualifying exam (Part 55) is the oracle inequality.",
        outside="Part 31's PCA and Part 32's lasso as methods, Part 51's concentration and Gaussian comparison, "
                "and complex analysis at the level of a contour and an imaginary part (the Stieltjes transform).",
        objectives={
            "U": ["Explain why PCA on pure noise shows large and small eigenvalues when p is comparable to n, and "
                  "what the Marchenko-Pastur edges say about them."],
            "M": ["Compute the Marchenko-Pastur edges, the BBP limit of a spiked eigenvalue and the eigenvector "
                  "overlap, and invert the map to correct a sample eigenvalue.",
                  "Apply Davis-Kahan to bound an eigenvector's error from an operator-norm error and an "
                  "eigengap."],
            "D": ["Prove the lasso's oracle inequality from the basic inequality, the cone condition and a "
                  "restricted eigenvalue, and state what it does not give.",
                  "Construct the primal-dual witness and derive the sample-size threshold for signed support "
                  "recovery.",
                  "Derive the Marchenko-Pastur law from the fixed-point equation of its Stieltjes transform, and "
                  "state the BBP transition and the Tracy-Widom limit."],
            "I": ["Report a debiased-lasso interval with its target, its sparsity condition and its unvalidated "
                  "finite-sample coverage stated.",
                  "Test for a spike with Roy's largest root on the Tracy-Widom scale rather than a normal test, "
                  "and correct a spiked eigenvalue before interpreting it."],
        },
        results=[
            ("The lasso's oracle inequality",
             r"\lambda\ge2\|X^\top\varepsilon/n\|_\infty\ \Longrightarrow\ \|\hat\beta-\beta^*\|_2\le"
             r"\frac{3\sqrt s\,\lambda}{\kappa}\asymp\frac{\sigma}{\kappa}\sqrt{\frac{s\log p}{n}}"),
            ("Davis-Kahan", r"\sin\angle(\hat v_1,v_1)\ \le\ \frac{2\,\|\hat\Sigma-\Sigma\|_{\mathrm{op}}}{\lambda_1(\Sigma)-\lambda_2(\Sigma)}"),
            ("Marchenko-Pastur", r"f_\gamma(x)=\frac{\sqrt{(b-x)(x-a)}}{2\pi\gamma x},\qquad a,b=(1\mp\sqrt\gamma)^2,\quad \gamma=p/n\le1"),
            ("The BBP transition",
             r"\Sigma=I+\ell vv^\top:\quad \hat\lambda_1\to\begin{cases}(1+\ell)(1+\gamma/\ell),&\ell>\sqrt\gamma\\"
             r"(1+\sqrt\gamma)^2,&\ell\le\sqrt\gamma\end{cases}\qquad "
             r"\langle\hat v_1,v\rangle^2\to\Bigl(\frac{1-\gamma/\ell^2}{1+\gamma/\ell}\Bigr)_+"),
            ("Tracy-Widom at the edge", r"\frac{\hat\lambda_1-\mu_{np}}{\sigma_{np}}\ \Rightarrow\ TW_1\qquad(\Sigma=I,\ \text{Johnstone's centring and scaling})"),
            ("The debiased lasso",
             r"\hat b_j=\hat\beta_j+\frac{\theta_j^\top X^\top(y-X\hat\beta)}{n},\qquad "
             r"\hat b_j\pm1.96\,\hat\sigma\sqrt{\theta_j^\top\hat\Sigma\,\theta_j/n}"),
        ],
        U=(0,), I=(5, 11),
    ),
    Part(
        n=53, level="D", widget="credibleball", prereq=(26, 47, 50),
        question="When does the posterior find the truth, and are its credible sets honest?",
        story="The part opens with Diaconis and Freedman (1986): in a symmetric location problem a reasonable "
              "prior, a symmetrized Dirichlet process with a Cauchy base, has a posterior that never settles at "
              "the true centre. Doob's theorem is proved by martingales and shown to promise consistency only "
              "for truths the prior itself would draw; Schwartz's theorem replaces it with Kullback-Leibler "
              "support plus tests. Contraction rates (Ghosal, Ghosh and van der Vaart) are made exact in the "
              "Gaussian sequence model, where a prior of smoothness alpha meets a truth of smoothness beta. "
              "Bernstein-von Mises follows from Part 47's LAN, and then fails in infinite dimensions: with an "
              "oversmoothing prior the credible ball's coverage falls from 100% to about zero. The part builds "
              "the nonparametric priors themselves, Dirichlet processes with the Chinese restaurant and a mixture "
              "fitted to Old Faithful, Polya trees, and Gaussian processes through small-ball probabilities, and "
              "shows empirical Bayes adapting to the smoothness. It ends on the Board with three honest answers: "
              "adaptive credible sets cover polished-tail truths and not all truths, spike-and-slab and horseshoe "
              "intervals undercover intermediate signals, and a tempered posterior repairs a Poisson interval "
              "that covers 62% on overdispersed counts.",
        handoff="PAC-Bayes bounds for Gibbs posteriors follow in Part 54, credible sets after selection in Part "
                "56, anytime-valid tests from Bayesian mixtures in Part 58, Bayesian causal inference in Part 62 "
                "and the calibration of Bayesian deep learning in Part 64; Problem 12 of the qualifying exam "
                "(Part 55) is a contraction rate.",
        outside="Part 26's Bayesian modelling, Part 47's LAN, Part 50's minimax rates and sequence model, and "
                "martingale convergence from Part 44.",
        objectives={
            "U": ["Explain what it means for a posterior to be consistent, and what Diaconis and Freedman's "
                  "example shows a reasonable prior can do."],
            "M": ["Compute the posterior, its exact risk and its credible ball in the Gaussian sequence model, and "
                  "read the contraction rate off the prior's and the truth's smoothness.",
                  "Simulate a Dirichlet process by the Polya urn and by stick-breaking, and compute its posterior "
                  "given data."],
            "D": ["Prove Doob's theorem and state Schwartz's theorem and the prior-mass, entropy and sieve "
                  "conditions of the contraction-rate theorem.",
                  "Prove the parametric Bernstein-von Mises theorem from LAN and explain why it fails for "
                  "infinite-dimensional parameters but can hold for smooth functionals.",
                  "State why no credible set can be both adaptive and honest over all truths, and what the "
                  "polished-tail condition restores."],
            "I": ["Check the frequentist coverage of a credible interval by simulation before reporting it, for "
                  "sparse signals of intermediate size in particular.",
                  "Detect an overdispersed count model's overconfident posterior and calibrate a tempered "
                  "posterior's learning rate."],
        },
        results=[
            ("Schwartz's theorem",
             r"\Pi\bigl(p:\operatorname{KL}(p_0\,\|\,p)<\varepsilon\bigr)>0\ \ \forall\varepsilon>0\ \text{ and exponentially "
             r"powerful tests of } p_0 \text{ against } U^c\ \Longrightarrow\ \Pi(U^c\mid X_1,\dots,X_n)\to0\ \text{a.s.}"),
            ("The posterior in the sequence model",
             r"Y_k=\theta_k+\frac{Z_k}{\sqrt n},\ \theta_k\sim N(0,\lambda_k):\qquad "
             r"\theta_k\mid Y\sim N\Bigl(\frac{n\lambda_k}{1+n\lambda_k}Y_k,\ \frac{\lambda_k}{1+n\lambda_k}\Bigr)"),
            ("Its contraction rate",
             r"\lambda_k=k^{-1-2\alpha},\ \theta_0\ \text{of regularity }\beta:\qquad "
             r"\varepsilon_n=n^{-\frac{\min(\alpha,\beta)}{1+2\alpha}},\quad\text{minimax } n^{-\frac{\beta}{1+2\beta}} \text{ iff } \alpha=\beta"),
            ("Bernstein-von Mises",
             r"\Bigl\|\Pi(\cdot\mid X_1,\dots,X_n)-N\bigl(\hat\theta_n,\ (nI_{\theta_0})^{-1}\bigr)\Bigr\|_{\mathrm{TV}}"
             r"\ \xrightarrow{\ P_{\theta_0}\ }\ 0"),
            ("The Dirichlet process is conjugate",
             r"P\sim\operatorname{DP}(\alpha,G_0),\ X_i\mid P\overset{\text{iid}}{\sim}P:\qquad "
             r"P\mid X\sim\operatorname{DP}\Bigl(\alpha+n,\ \frac{\alpha G_0+\sum_i\delta_{X_i}}{\alpha+n}\Bigr)"),
            ("The tempered posterior", r"\pi_\eta(\theta\mid x)\ \propto\ \pi(\theta)\,p(x\mid\theta)^\eta,\qquad 0<\eta\le1"),
        ],
        U=(0,), I=(11,),
    ),
    Part(
        n=54, level="D", widget="bestofk", prereq=(34, 48, 51),
        question="Why does fitting data generalize at all, and why do interpolating models seem to break the theory?",
        story="In Moscow in 1971 Vapnik and Chervonenkis ask when the empirical risk converges to the true risk "
              "uniformly over a class of rules, and answer with shattering: half-planes realize 14 of the 16 "
              "labellings of four points in a square. The part turns Part 48's uniform laws into the risk of the "
              "rule that was chosen. Empirical risk minimization, PAC learning and the no-free-lunch theorem set "
              "the problem; VC bounds are proved by symmetrization and Sauer-Shelah, and Rademacher complexity "
              "with the contraction lemma sharpens them for linear and kernel classes. Localization explains why "
              "the excess risk falls like 1/n while the deviation falls like one over root n. Margins account for "
              "AdaBoost improving on the breast cancer data after its training error reaches zero; PAC-Bayes "
              "bounds a Gibbs posterior, stability bounds ridge and SGD, and Hedge and the bandit algorithms give "
              "regret bounds that convert to batch guarantees. Calibrated surrogates justify minimizing a convex "
              "loss. The part ends where the theory strains: min-norm interpolators show double descent and "
              "benign overfitting, and Nagarajan and Kolter show that uniform convergence cannot explain it.",
        handoff="The qualifying exam follows (Part 55). Distribution-free conformal guarantees are Part 57, online "
                "learning becomes betting and e-values in Part 58, the exact risks of interpolators in "
                "proportional asymptotics are Part 59, and the generalization of foundation models is Part 64.",
        outside="Part 48's empirical processes (symmetrization, VC classes, chaining), Part 51's concentration, "
                "and Part 34's predictive methods as things to be explained.",
        objectives={
            "U": ["Explain shattering by counting the labellings a class of rules can produce on a few points, "
                  "and why a class that can produce all of them learns nothing from them."],
            "M": ["Compute VC, Rademacher and finite-class bounds for a given class and sample size, and compare "
                  "them with a simulated uniform deviation.",
                  "Run Hedge and UCB1 and compare their regret with the bounds."],
            "D": ["Prove the VC bound by symmetrization and the Sauer-Shelah lemma, and the Rademacher bound with "
                  "the contraction lemma.",
                  "Prove a PAC-Bayes bound and a uniform-stability bound, and say which property of the algorithm "
                  "each uses in place of the size of the class.",
                  "State the benign-overfitting conditions and why a uniform-convergence bound can be vacuous for "
                  "an interpolator that generalizes."],
            "I": ["Report the error of a model chosen among many with a holdout or a bound uniform over the "
                  "candidates, never a Wald interval on its training error.",
                  "Read a boosting run by its margin distribution as well as its training error."],
        },
        results=[
            ("ERM and uniform convergence",
             r"R(\hat h)-\inf_{h\in\mathcal H}R(h)\ \le\ 2\sup_{h\in\mathcal H}|R_n(h)-R(h)|"),
            ("Sauer-Shelah", r"\Pi_{\mathcal H}(n)\ \le\ \sum_{i=0}^{d}\binom ni\ \le\ \Bigl(\frac{en}{d}\Bigr)^d\qquad(n\ge d=\operatorname{VC}(\mathcal H))"),
            ("The Rademacher bound",
             r"\sup_{f\in\mathcal F}\bigl(\operatorname{E}f-\operatorname{E}_nf\bigr)\le2\mathfrak R_n(\mathcal F)+\sqrt{\frac{\log(1/\delta)}{2n}},"
             r"\qquad \hat{\mathfrak R}_n\bigl(\{x\mapsto\langle w,x\rangle:\|w\|\le B\}\bigr)\le\frac{B}{n}\sqrt{\sum_i\|x_i\|^2}"),
            ("PAC-Bayes (the kl form)",
             r"\operatorname{kl}\bigl(R_n(\rho)\,\|\,R(\rho)\bigr)\ \le\ \frac{\operatorname{KL}(\rho\,\|\,\pi)+\log(2\sqrt n/\delta)}{n}"
             r"\quad\text{for all }\rho\text{, with probability }1-\delta"),
            ("Hedge", r"\text{regret}_T\ \le\ \sqrt{\tfrac12T\log K}\qquad(K\text{ experts, losses in }[0,1],\ \text{tuned learning rate})"),
            ("Calibrated surrogates (Bartlett, Jordan and McAuliffe)",
             r"\psi\bigl(R(f)-R^*\bigr)\ \le\ R_\phi(f)-R_\phi^*,\qquad \psi(\theta)=|\theta|\ \text{(hinge)},\ \ \theta^2\ \text{(squared)}"),
        ],
        U=(0,), I=(5,),
    ),
    Part(
        n=55, level="D", widget="stoppedwalk", prereq=(49, 52, 53, 54),
        question="Can you prove the core of a statistics PhD, twelve problems in six hours?",
        story="The part adds no new method. It opens with Hilbert's twenty-three problems in Paris in 1900, and "
              "then the letter on the desk the night before the qualifying exam: twelve problems drawing on Parts "
              "43 to 54, and a correct answer without its proof earns nothing. The problems are set in six "
              "sittings, each posed on an exam card, paused, proved on screen and drawn as a proof map whose boxes "
              "name the part each move borrows from. Probability gives a Borel-Cantelli argument for exponential "
              "maxima and the walk stopped at +1, whose mean is 1 because the stopped walk is not uniformly "
              "integrable. Estimation gives a UMVUE strictly above the Cramer-Rao bound, a parameter with no "
              "unbiased estimator, and Blyth's method, which works in one dimension and fails in two. Testing "
              "gives the UMPU test of equal Poisson rates on Snow's Table IX and local power in the logistic "
              "model. The last three sittings prove a bracketing bound, the median's influence function on "
              "Newcomb's passage times, Fano's sparse rate, a matrix Bernstein ball for a covariance, the lasso's "
              "oracle inequality and a posterior contraction rate. Candidacy goes on the Transcript.",
        handoff="Stage V, PhD research, begins: inference after selection in Part 56, where the lasso's chosen "
                "variables need honest intervals, distribution-free inference in Part 57, optional stopping made "
                "safe by test martingales and e-values in Part 58, the lasso and the posterior when p and n grow "
                "together in Part 59, and the dissertation in Part 65.",
        outside="The whole PhD core, Parts 43 to 54; each problem names the part it draws on.",
        objectives={
            "U": ["State in words what each of the twelve problems claims and which part of the core it comes "
                  "from."],
            "M": ["Check a proof's conclusion by computation: the stopped walk's mean at bounded times, the "
                  "UMVUE's exact variance against the Cramer-Rao bound, the median's sampling variance against "
                  "its influence function."],
            "D": ["Prove each of the twelve problems unaided, showing every step, and draw its proof map.",
                  "Say for each proof where it stops working: optional stopping without uniform integrability, "
                  "Blyth's method in two dimensions, bracketing for classes that are not Donsker."],
            "I": ["Compute the exact conditional test and interval for a ratio of two Poisson rates and report "
                  "its size, as on Snow's Table IX.",
                  "Report a median with a Wald interval from its influence function and say what the density "
                  "plug-in assumes."],
        },
        results=[
            ("Problem 1: exponential maxima",
             r"X_i\overset{\text{iid}}{\sim}\operatorname{Exp}(1),\ M_n=\max_{i\le n}X_i:\qquad \frac{M_n}{\log n}\to1\ \text{a.s.}"),
            ("Problem 2: the walk stopped at +1",
             r"T=\inf\{n:S_n=1\}:\qquad \operatorname{E}S_{T\wedge m}=0\ \ \forall m,\qquad \operatorname{E}S_T=1,\qquad \operatorname{E}T=\infty"),
            ("Problem 3: a UMVUE above the Cramer-Rao bound",
             r"T=\sum_{i\le n}X_i,\ X_i\sim\operatorname{Poisson}(\lambda):\quad \operatorname{E}\bigl(1-\tfrac1n\bigr)^T=e^{-\lambda},\quad "
             r"\operatorname{Var}=e^{-2\lambda}\bigl(e^{\lambda/n}-1\bigr)>\frac{\lambda e^{-2\lambda}}{n}"),
            ("Problem 8: the median's influence function",
             r"\varphi(x)=\frac{\tfrac12-\mathbf 1\{x\le m\}}{f(m)},\qquad \sqrt n\,(\hat m-m)\Rightarrow N\Bigl(0,\frac{1}{4f(m)^2}\Bigr)"),
            ("Problem 9: the sparse minimax rate",
             r"\inf_{\hat\theta}\sup_{\|\theta\|_0\le s}\operatorname{E}\|\hat\theta-\theta\|_2^2\ \asymp\ \frac{\sigma^2s\log(d/s)}{n}"),
            ("Problem 12: a contraction rate",
             r"\theta_k\sim N(0,k^{-1-2\alpha}),\ \theta_0\ \text{of regularity }\beta:\qquad \varepsilon_n=n^{-\frac{\min(\alpha,\beta)}{1+2\alpha}}"),
        ],
        U=(0,),
    ),
]
