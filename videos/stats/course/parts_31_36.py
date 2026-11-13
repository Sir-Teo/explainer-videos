"""Stage III, Master's: many variables, many questions, prediction and causes (Parts 31-36)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=31, level="M", widget="roadmapmds", prereq=(4, 5, 22),
        question="What structure hides in many correlated variables measured at once?",
        story="The part opens with a table and no map: the road distance between every pair of the World's 200 "
              "towns. Torgerson's classical scaling double-centres the squared distances into a Gram matrix, takes "
              "two eigenvectors, and rebuilds the island; the same method on 21 European cities picks out the "
              "table entries worth checking against their sources. From there the classical toolkit is built on "
              "the sample covariance matrix: Mahalanobis distance on Fisher's versicolors, the Wishart law by "
              "Bartlett's decomposition, Hotelling's T-squared as the best single t-test, and MANOVA's four "
              "statistics. Principal components, factor analysis of the 24 tests and canonical correlation look "
              "for low-dimensional structure; discriminant analysis and clustering look for groups, known and "
              "unknown; zeros of the precision matrix draw a graph of conditional independence. The part turns "
              "when the number of variables grows with the sample: the chi-squared calibration of T-squared "
              "rejects 72% of true nulls at p = 40, the exact F holds, and Bai and Saranadasa's test keeps its "
              "power by dropping the inverse covariance. It ends on the promise that Part 52 drops the "
              "assumption of fixed p altogether.",
        handoff="The graphical lasso's penalty returns as sparsity in Part 32, and thousands of correlated tests "
                "in Part 33; Mahalanobis matching returns in Part 36; the Marchenko-Pastur law, the spiked model "
                "and Ledoit-Wolf shrinkage are proved in Part 52, and proportional asymptotics in Part 59.",
        outside="Linear algebra at the level of Part 4 (eigenvectors, the SVD, projections) and the multivariate "
                "normal of Part 5.",
        objectives={
            "U": ["Rebuild a map from a table of distances by classical scaling, and say what the size of the "
                  "negative eigenvalues tells you.",
                  "Read a scree plot and a biplot, and explain why standardizing the variables changes the "
                  "principal components."],
            "M": ["Derive Hotelling's T-squared from the union-intersection principle and convert it to its "
                  "exact F statistic.",
                  "Fit and compare PCA, maximum-likelihood factor analysis with varimax, CCA, LDA and QDA, and a "
                  "Gaussian mixture by EM, and state what each one maximizes.",
                  "Compute partial correlations from the precision matrix and read a graphical lasso path."],
            "D": ["Prove Bartlett's decomposition of the Wishart distribution and the Eckart-Young theorem by "
                  "Weyl's inequality.",
                  "Explain why the chi-squared calibration of T-squared fails when p/n does not vanish, and "
                  "state what the Marchenko-Pastur law says about the sample eigenvalues."],
            "I": ["Report a discriminant or clustering analysis with leave-one-out error or the adjusted Rand "
                  "index, and say why a mixture's BIC is not proof of the number of groups.",
                  "Check p against n before inverting a sample covariance matrix, and switch to the exact F or a "
                  "test without the inverse when they are comparable."],
        },
        results=[
            ("Classical scaling", r"B=-\tfrac12\,J D^{(2)} J = X_0X_0^\top,\qquad J = I-\tfrac1n\mathbf 1\mathbf 1^\top"),
            ("Wishart moments", r"W=\sum_{i=1}^m x_ix_i^\top\sim W_p(m,\Sigma):\quad \mathbb E\,W=m\Sigma,\quad "
                                r"\operatorname{Var}(W_{jk})=m\,(\sigma_{jk}^2+\sigma_{jj}\sigma_{kk})"),
            ("Hotelling's T-squared", r"T^2=\frac{n_1n_2}{n_1+n_2}\,d^\top S^{-1}d=\max_a t^2(a),\qquad "
                                      r"\frac{n_1+n_2-p-1}{p\,(n_1+n_2-2)}\,T^2\sim F_{p,\;n_1+n_2-p-1}"),
            ("Eckart-Young", r"\min_{\operatorname{rank}B\le k}\lVert X_0-B\rVert_F^2=\sum_{j>k}d_j^2"),
            ("Zeros of the precision matrix", r"\rho_{ij\cdot\text{rest}}=-\frac{\theta_{ij}}{\sqrt{\theta_{ii}\theta_{jj}}},"
                                              r"\qquad \theta_{ij}=0\iff x_i\perp x_j\mid x_{\text{rest}}"
                                              r"\quad(\Theta=\Sigma^{-1},\ \text{normal})"),
        ],
        U=(0, 1, 4, 8), D=(2, 10), I=(7,),
        also=(("statkit.multi", "explainer/stats/kit/multi.py"),),
    ),
    Part(
        n=32, level="M", widget="lqcorner", prereq=(19, 21, 23),
        question="How can you solve for a thousand unknowns from a hundred equations?",
        story="In 2004 Candes measures the Shepp-Logan phantom on 22 radial lines of its Fourier transform, a "
              "fifth of the coefficients. The minimum-energy reconstruction is 48% wrong; minimizing total "
              "variation recovers the image to numerical tolerance, because the image is sparse in its jumps. "
              "The part explains why by betting that most unknowns are zero. Ridge shrinks along the singular "
              "directions but leaves every coefficient nonzero; best subset is exact and intractable; the l1 "
              "ball is the smallest convex ball with corners, and the lasso's solution lands on one. The lasso "
              "is then computed (coordinate descent, LARS on the diabetes data), given relatives (elastic net, "
              "group, fused, adaptive, SCAD, MCP), tuned by cross-validation and stability selection, and given "
              "priors (Laplace, the horseshoe). Compressed sensing states when l1 recovery is exact, by the null "
              "space property and the Donoho-Tanner phase transition. The part turns on inference: naive "
              "intervals after selection cover 75%, and the debiased lasso and double selection repair them. It "
              "ends with matrix completion, where rank plays the role of sparsity.",
        handoff="Selecting variables means asking thousands of questions (Part 33); double selection becomes "
                "double machine learning in Part 36; the RIP for random matrices is proved in Part 51, the "
                "lasso's oracle inequality in Part 52, selective inference in Part 56, and the phase transition "
                "is derived by AMP in Part 59.",
        outside="Regression in matrix form (Part 23) and convex optimization at the level of Part 21 "
                "(subgradients, coordinate descent, duality).",
        objectives={
            "U": ["Explain with the picture of a diamond and a disc why an l1 budget sets coefficients exactly "
                  "to zero and an l2 budget does not.",
                  "Apply soft, hard and ridge thresholding to a number and say which rule belongs to which "
                  "penalty."],
            "M": ["Derive the lasso's KKT conditions and lambda_max, and compute a path by coordinate descent "
                  "with warm starts.",
                  "Compute ridge through the SVD and read its shrinkage factors and effective degrees of freedom.",
                  "Construct a debiased lasso interval and a double-selection estimate, and say what each "
                  "assumes."],
            "D": ["Prove that the null space property is necessary and sufficient for exact l1 recovery of "
                  "every s-sparse vector.",
                  "State the conditions (RIP, incoherence, the s log(p/s) sample count) under which the recovery "
                  "theorems hold, and which of them the radial-line phantom does not satisfy."],
            "I": ["Choose lambda by cross-validation with every centring and scaling step refitted inside the "
                  "folds, and report the one-SE model beside the minimum.",
                  "Refuse to report least-squares intervals for variables a lasso selected, and say what to "
                  "report in their place."],
        },
        results=[
            ("Ridge by the SVD", r"\hat\beta_\lambda=V\operatorname{diag}\!\Bigl(\frac{d_j}{d_j^2+\lambda}\Bigr)U^\top y,"
                                 r"\qquad \operatorname{df}(\lambda)=\sum_j\frac{d_j^2}{d_j^2+\lambda}"),
            ("The lasso's KKT conditions", r"\tfrac1n x_j^\top(y-X\hat\beta)=\lambda\operatorname{sign}(\hat\beta_j)"
                                           r"\ \text{ if }\hat\beta_j\ne0,\qquad \bigl|\tfrac1n x_j^\top(y-X\hat\beta)\bigr|"
                                           r"\le\lambda\ \text{ otherwise}"),
            ("Soft thresholding", r"S_\lambda(z)=\operatorname{sign}(z)\,(|z|-\lambda)_+,\qquad "
                                  r"\lambda_{\max}=\tfrac1n\lVert X^\top y\rVert_\infty"),
            ("Null space property", r"\lVert h_S\rVert_1<\lVert h_{S^c}\rVert_1\quad\text{for all }h\in\ker A\setminus\{0\},"
                                    r"\ |S|\le s"),
            ("Debiased lasso", r"\hat b=\hat\beta+\tfrac1n\,\hat\Theta X^\top(y-X\hat\beta)"),
            ("SoftImpute", r"Z\leftarrow S_\lambda^{\text{svd}}\bigl(P_\Omega(M)+P_\Omega^\perp(Z)\bigr),\qquad "
                           r"S_\lambda^{\text{svd}}(UDV^\top)=U\,(D-\lambda I)_+V^\top"),
        ],
        U=(0, 1, 3), D=(9,), I=(7,),
        also=(("statkit.sparse", "explainer/stats/kit/sparse.py"),),
    ),
    Part(
        n=33, level="M", widget="bhsea", prereq=(10, 25),
        question="Ask enough questions and chance will answer some: which answers are real?",
        story="A dead salmon in a scanner appears to respond to photographs: in a toy fish of 9,141 voxels of "
              "pure noise, 446 have p below 0.05, and none survives a correction. The World's gene study makes "
              "the problem a table: 5,000 genes, 250 truly differential, and 430 uncorrected discoveries of "
              "which 214 are false. Bonferroni, Holm and Westfall-Young control the chance of any false "
              "discovery and find about fifty genes. Benjamini and Hochberg change the promise to the expected "
              "share of false discoveries, and the proof that the rate is pi0 times q under independence is "
              "given; Storey's estimate, Efron's local fdr and knockoffs extend it. The part turns from "
              "procedures to practice: the false discovery proportion spreads widely under correlation, and a "
              "p-hacking simulator shows four small analytic freedoms raising the false-positive rate from 5% "
              "to 61%. Ioannidis's calculation, the replication projects and publication bias are measured, "
              "and the remedies are argued. It ends with the false coverage rate: intervals reported only for "
              "selected effects cover 79% until they are widened.",
        handoff="Exchangeability returns as conformal prediction in Part 34; many outcomes in one trial in "
                "Part 35; optimal multiple testing in Part 46; higher criticism in Part 50; selective inference "
                "and PoSI in Part 56; e-values and FDR at any stopping time in Part 58.",
        outside="Testing and p-values from Part 10, and the empirical Bayes of Part 25.",
        objectives={
            "U": ["Compute how many false positives to expect from m tests at level alpha, and apply "
                  "Bonferroni's and Benjamini-Hochberg's rules to a sorted list of p-values.",
                  "Compute the positive predictive value of a significant finding from the prior, the power "
                  "and alpha."],
            "M": ["Prove that Benjamini-Hochberg has FDR equal to pi0 times q for independent uniform nulls, "
                  "and derive Holm's procedure from closed testing.",
                  "Estimate pi0 and q-values, and a local fdr with a theoretical and an empirical null.",
                  "Construct FCR-adjusted intervals for the selected parameters."],
            "D": ["Prove the knockoff filter's FDR bound by the coin-flip argument, stating the exchangeability "
                  "it needs.",
                  "Explain why FDR control says little about the realized FDP under dependence, and state the "
                  "conditions (PRDS, arbitrary dependence) under which BH and BY hold."],
            "I": ["Diagnose a literature with a funnel plot, Egger's test and a p-curve, naming the other "
                  "explanations each pattern admits.",
                  "Write a preregistration that fixes the outcomes, the stopping rule, the covariates and the "
                  "exclusions the p-hacking simulator varies."],
        },
        results=[
            ("Bonferroni", r"\Pr(V\ge1)\le\sum_{i\in\text{nulls}}\Pr\bigl(p_i\le\tfrac{\alpha}{m}\bigr)"
                           r"\le\frac{m_0}{m}\,\alpha\le\alpha"),
            ("Benjamini-Hochberg", r"k=\max\bigl\{i:\ p_{(i)}\le\tfrac{i}{m}q\bigr\},\qquad "
                                   r"\operatorname{FDR}=\mathbb E\Bigl[\frac{V}{\max(R,1)}\Bigr]=\pi_0\,q"
                                   r"\quad\text{(independent uniform nulls)}"),
            ("Local false discovery rate", r"\operatorname{fdr}(z)=\frac{\pi_0f_0(z)}{f(z)},\qquad "
                                           r"f=\pi_0f_0+(1-\pi_0)f_1"),
            ("Knockoff+ threshold", r"T=\min\Bigl\{t>0:\ \frac{1+\#\{j:W_j\le-t\}}{\max(1,\#\{j:W_j\ge t\})}\le q\Bigr\}"),
            ("Positive predictive value", r"\operatorname{PPV}=\frac{\pi\,(1-\beta)}{\pi\,(1-\beta)+(1-\pi)\,\alpha}"),
            ("False coverage rate", r"\text{for }R\text{ selected of }m:\ \text{intervals at level }1-\frac{Rq}{m}"
                                    r"\ \Longrightarrow\ \operatorname{FCR}\le q"),
        ],
        U=(0, 1, 8, 9), D=(7,), I=(10, 11),
        also=(("statkit.multiple", "explainer/stats/kit/multiple.py"),),
    ),
    Part(
        n=34, level="M", widget="scoreladder", prereq=(16, 19, 33),
        question="Can any prediction, from any model, come with an honest guarantee?",
        story="In 2001 Breiman tells statisticians that algorithms have won prediction, and Cox and Efron reply "
              "that prediction is not all of science. The part treats the algorithms as estimators. Fifty "
              "bootstrap trees on the breast cancer data predict equally well and tell different stories; a "
              "forest's variance is rho sigma squared plus what averaging removes; boosting is stagewise "
              "additive modelling; cross-validation estimates the average error over training sets and not the "
              "error of the model in hand; a predicted probability needs calibrating. The part turns at split "
              "conformal prediction: sort the calibration scores on the score ladder, take the rank "
              "ceil((n+1)(1-alpha)), and the interval covers a new exchangeable case with probability at least "
              "1-alpha, whatever the model. Jackknife+, conformalized quantile regression, weighted and "
              "adaptive conformal, and classification sets extend the guarantee and mark where it stops: it is "
              "marginal, and it needs exchangeability. Prediction-powered inference then turns 20,000 biased "
              "smartwatch guesses and 300 clinic visits into a valid interval for the World's mean blood "
              "pressure. It ends with a pneumonia model that predicts well and would advise badly.",
        handoff="Prediction is not intervention: potential outcomes in Part 35. Forests and boosting return as "
                "nuisance fits in Part 36, conformal bands for censored times in Part 40, distribution-free "
                "inference with its impossibility theorems in Part 57, anytime-valid inference in Part 58, shift "
                "in Part 60, and PPI's successors in Part 64.",
        outside="Trees, cross-validation and the bias-variance trade-off from Part 19; the bootstrap of Part 16.",
        objectives={
            "U": ["Compute a split conformal interval from a list of calibration residuals, and say exactly "
                  "what its 90% promises and what it does not.",
                  "Explain why several different models can predict equally well and still disagree about "
                  "which variables matter."],
            "M": ["Derive the variance of an average of B correlated trees and the quantile lemma behind "
                  "split conformal coverage.",
                  "Implement jackknife+, CQR and weighted conformal, and adaptive conformal on a stream.",
                  "Compute a prediction-powered mean with its interval and the tuned PPI++ weight."],
            "D": ["Prove that coverage given the calibration set is Beta(k, n+1-k) for i.i.d. continuous "
                  "scores, and state why exchangeability alone does not give that law.",
                  "State the impossibility of distribution-free conditional coverage and the 1-2 alpha bound "
                  "for jackknife+."],
            "I": ["Check a classifier's reliability diagram and recalibrate it by Platt, isotonic or "
                  "temperature scaling on held-out data.",
                  "Say what a permutation importance, a partial dependence curve, LOCO and a Shapley value each "
                  "estimate before reporting one."],
        },
        results=[
            ("Variance of a forest", r"\operatorname{Var}\Bigl(\tfrac1B\sum_{b=1}^B T_b(x)\Bigr)=\rho\sigma^2+"
                                     r"\frac{1-\rho}{B}\,\sigma^2"),
            ("Split conformal", r"\hat q=S_{(k)},\ k=\lceil(n+1)(1-\alpha)\rceil:\qquad 1-\alpha\le"
                                r"\Pr\bigl(|Y-\hat\mu(X)|\le\hat q\bigr)\le1-\alpha+\frac{1}{n+1}"
                                r"\quad\text{(upper bound: no ties)}"),
            ("Coverage given the calibration set", r"\Pr\bigl(Y\in\hat C(X)\mid\text{calibration}\bigr)\sim"
                                                   r"\operatorname{Beta}(k,\ n+1-k)\quad\text{(i.i.d. continuous scores)}"),
            ("Adaptive conformal inference", r"\alpha_{t+1}=\alpha_t+\gamma\,(\alpha-\operatorname{err}_t),\qquad "
                                             r"\operatorname{err}_t=\mathbf 1\{Y_t\notin\hat C_t\}"),
            ("Prediction-powered mean", r"\hat\theta=\frac1N\sum_{j=1}^Nf(\tilde X_j)-\frac1n\sum_{i=1}^n"
                                        r"\bigl(f(X_i)-Y_i\bigr),\qquad \operatorname{Var}=\frac{\sigma_f^2}{N}"
                                        r"+\frac{\sigma_{Y-f}^2}{n}"),
        ],
        U=(0, 1, 6), D=(8,), I=(5, 11),
        also=(("statkit.conformal", "explainer/stats/kit/conformal.py"), ("statkit.ppi", "explainer/stats/kit/ppi.py")),
    ),
    Part(
        n=35, level="M", widget="sciencecoin", prereq=(13, 23),
        question="What does it mean for one thing to cause another, and why does randomization let us find out?",
        story="The 1954 Salk vaccine trial ran two designs side by side. The randomized, placebo-controlled one "
              "found 28 against 71 cases of paralytic polio per 100,000; the observed-control one found 25 "
              "against 54, because consenting families differed from the rest. Potential outcomes make the "
              "question precise: each unit has an outcome under treatment and one under control, and only one "
              "is ever seen. In the World's clinic both are known, so the science table shows what an "
              "assignment hides, and the naive difference splits into the effect on the treated plus selection "
              "bias. A coin removes the bias. Fisher tests the sharp null by re-randomizing; Neyman gives the "
              "difference in means its variance and a conservative estimate of it. The part then works through "
              "what trials meet in practice: blocking, Lin's adjustment, cluster randomization, noncompliance "
              "and the complier effect, interference in an epidemic, subgroups by star sign in ISIS-2, "
              "boundaries for interim looks, surrogates that failed in CAST, and transport to the island. It "
              "ends by asking what can be learned when no coin is available.",
        handoff="Unconfoundedness replaces the coin in Part 36; instruments and the LATE return in Part 37; "
                "survival endpoints in Part 40; dropout in Part 41; efficient estimation of average effects in "
                "Part 49; anytime-valid monitoring in Part 58; interference and heterogeneity in Part 62.",
        outside="Designed experiments from Part 13 and regression with robust standard errors from Part 23.",
        objectives={
            "U": ["Write a science table for a small study, compute its average effect, and show which half an "
                  "assignment hides.",
                  "Decompose a difference in means into the effect on the treated plus selection bias, and say "
                  "why a coin makes the second term zero on average."],
            "M": ["Carry out Fisher's randomization test of the sharp null and invert it for a constant effect.",
                  "Derive Neyman's variance of the difference in means and explain why its estimator is "
                  "conservative.",
                  "Derive the Wald estimator of the complier average effect under monotonicity and exclusion."],
            "D": ["Define direct, indirect, total and overall effects under partial interference and say which "
                  "of them a two-stage design identifies.",
                  "State what Lin's interacted estimator guarantees asymptotically without a model for the "
                  "outcomes, and Freedman's three critiques of ANCOVA that it answers."],
            "I": ["Analyse a cluster-randomized trial at the level that was randomized, and compute the design "
                  "effect before planning one.",
                  "Plan interim analyses with a Pocock or O'Brien-Fleming boundary instead of repeated tests at "
                  "1.96, and treat an unplanned subgroup finding or a surrogate endpoint with the caution of "
                  "ISIS-2 and CAST."],
        },
        results=[
            ("Selection bias", r"\mathbb E[Y\mid D=1]-\mathbb E[Y\mid D=0]=\underbrace{\mathbb E[Y(1)-Y(0)\mid D=1]}_{\text{ATT}}"
                               r"+\underbrace{\mathbb E[Y(0)\mid D=1]-\mathbb E[Y(0)\mid D=0]}_{\text{selection bias}}"),
            ("Fisher's exact p-value", r"p=\frac{\#\{z:\ |T(z)|\ge|T(z^{\text{obs}})|\}}{\binom{n}{n_1}}"
                                       r"\quad\text{under }Y_i(1)=Y_i(0)\text{ for every }i"),
            ("Neyman's variance", r"\operatorname{Var}(\hat\tau)=\frac{S_1^2}{n_1}+\frac{S_0^2}{n_0}-\frac{S_\tau^2}{n}"
                                  r"\ \le\ \frac{S_1^2}{n_1}+\frac{S_0^2}{n_0}"),
            ("Design effect", r"\operatorname{deff}=1+(\bar m-1)\,\rho_{\text{ICC}}"),
            ("Complier average effect", r"\frac{\mathbb E[Y\mid Z=1]-\mathbb E[Y\mid Z=0]}{\mathbb E[D\mid Z=1]-\mathbb E[D\mid Z=0]}"
                                        r"=\mathbb E\bigl[Y(1)-Y(0)\mid\text{complier}\bigr]"),
        ],
        U=(0, 1, 3, 11), D=(10,), I=(8, 12, 13, 14),
        also=(("statkit.causal", "explainer/stats/kit/causal.py"),),
    ),
    Part(
        n=36, level="M", widget="twochances", prereq=(35,),
        question="When you cannot randomize, what can still be learned, and at what cost in assumptions?",
        story="LaLonde takes a job-training experiment whose answer is known, about $1,794 a year, throws away "
              "its randomized controls, and asks whether survey men can stand in for them: the raw difference "
              "is -$635. The part asks what would have to be true for such a comparison to work. "
              "Unconfoundedness and overlap give the adjustment formula; causal diagrams and d-separation say "
              "which covariates to adjust for, and which (colliders, mediators) to leave alone; the front door "
              "identifies an effect with no adjustment set at all, and Simpson's paradox from Part 1 is "
              "resolved by the graph. Estimation follows on an observational version of the World's clinic, "
              "where the truth is known: g-computation models the outcome, propensity scores model the "
              "treatment, and the augmented estimator combines them so that either model being right is "
              "enough. Double machine learning adds cross-fitting so flexible learners can supply both. The "
              "part turns to what cannot be tested: with an unmeasured frailty every adjusted estimate is "
              "wrong, and Rosenbaum's Gamma, E-values and robustness values say how strong a hidden confounder "
              "would have to be, the argument Cornfield used for smoking. It ends back at LaLonde, where "
              "overlap, placebo outcomes and sensitivity decide how far the estimates can be trusted.",
        handoff="Natural experiments (instruments, discontinuities, difference-in-differences, synthetic control) "
                "follow in Part 37; the same weighting and doubly robust tools handle missing data in Part 41; "
                "efficient influence functions, the theory behind AIPW and DML, are in Part 49; mediation, "
                "heterogeneity and causal discovery in Part 62.",
        outside="Potential outcomes from Part 35; logistic regression (Part 24) and the forests of Part 34 for "
                "the nuisance fits.",
        objectives={
            "U": ["Read a causal diagram: tell a chain, a fork and a collider apart, and say which paths "
                  "conditioning on a variable opens or blocks.",
                  "Explain the argument that made the case for smoking as a cause of lung cancer without an "
                  "experiment."],
            "M": ["Apply the back-door criterion to choose an adjustment set, and compute the adjustment and "
                  "front-door formulas.",
                  "Estimate an average effect by g-computation, matching, subclassification, IPW and AIPW, and "
                  "check balance and effective sample size.",
                  "Fit a marginal structural model with stabilized weights when a confounder is itself affected "
                  "by earlier treatment."],
            "D": ["Show that the AIPW score is Neyman orthogonal, and state the product-rate condition under "
                  "which cross-fitted DML is root-n normal.",
                  "State the three rules of the do-calculus and what their completeness means."],
            "I": ["Inspect overlap before estimating anything, and report the largest weight, the effective "
                  "sample size and a placebo outcome with the estimate.",
                  "Report an E-value or a robustness value with an observational estimate, benchmarked against "
                  "a measured covariate."],
        },
        results=[
            ("Back-door adjustment", r"P\bigl(y\mid\operatorname{do}(t)\bigr)=\sum_zP(y\mid t,z)\,P(z)"),
            ("Front door", r"P\bigl(y\mid\operatorname{do}(t)\bigr)=\sum_mP(m\mid t)\sum_{t'}P(y\mid m,t')\,P(t')"),
            ("Inverse probability weighting", r"\tau=\mathbb E\Bigl[\frac{TY}{e(X)}-\frac{(1-T)Y}{1-e(X)}\Bigr],"
                                              r"\qquad e(X)=\Pr(T=1\mid X)"),
            ("The AIPW score", r"\psi=\mu_1(X)-\mu_0(X)+\frac{T\,(Y-\mu_1(X))}{e(X)}-\frac{(1-T)\,(Y-\mu_0(X))}{1-e(X)}"),
            ("Product rate for DML", r"\lVert\hat e-e\rVert_2\cdot\lVert\hat\mu-\mu\rVert_2=o_P\bigl(n^{-1/2}\bigr)"),
            ("E-value", r"E=\operatorname{RR}+\sqrt{\operatorname{RR}\,(\operatorname{RR}-1)}\qquad(\operatorname{RR}\ge1)"),
        ],
        U=(0, 2, 5, 13), D=(4, 10), I=(12, 15),
        also=(("statkit.causal", "explainer/stats/kit/causal.py"),),
    ),
]
