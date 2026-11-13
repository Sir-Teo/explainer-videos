"""Stage III, Master's: the computational and likelihood core (Parts 21-25)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=21, level="M", widget="condzigzag", prereq=(4, 9, 19),
        question="How are estimators actually computed, and what does the shape of the problem say about them?",
        story="In 1939 George Dantzig arrives late to Neyman's class, copies two problems from the board as homework "
              "and solves them; one becomes, with Wald, the generalized Neyman-Pearson lemma, whose mathematics is "
              "linear-programming duality, and in 1947 he invents the simplex method. The World's bakery, a "
              "two-variable linear program, is walked from corner to corner and priced by its dual. The part then "
              "treats almost every estimator of the course as an optimization problem. Convexity says when a local "
              "answer is the global one, and the condition number says how slowly gradient descent gets there. "
              "Lagrange multipliers, KKT and duality turn constraints into prices and give the lasso a stopping "
              "certificate. Then the algorithms, each on a statistical problem: linear programming for least absolute "
              "deviations and quantile regression, Newton and Fisher scoring for a logistic likelihood, MM, coordinate "
              "descent, ISTA and FISTA, ADMM, and stochastic gradient with Polyak-Ruppert averaging. It ends where "
              "optimization meets inference: the curvature at the optimum is the observed information, and an "
              "optimizer should be run until its error is small beside the standard error.",
        handoff="EM, the likelihood's curvature and the sandwich are taken up in Part 22; IRLS becomes the engine of "
                "every GLM in Part 24; optimizing over variance components is Part 25; the lasso's theory is Part 32, "
                "empirical risk minimization Part 54 and optimal transport as a linear program Part 61.",
        outside="Multivariable calculus (gradients, Hessians) and the matrix language of Part 4; the lasso and "
                "logistic regression as met in Stage II.",
        objectives={
            "U": ["Solve a two-variable linear program by walking its corners, and read the shadow prices as the "
                  "worth of one more unit of each resource.",
                  "Tell a convex objective from one with several peaks, and say why that matters to an optimizer."],
            "M": ["Write the KKT conditions of a constrained likelihood or of the lasso and check them at a "
                  "proposed solution.",
                  "Implement Newton or Fisher scoring, coordinate descent and proximal gradient for a statistical "
                  "objective, and state the rate each one has.",
                  "Compute a duality gap and use it as a stopping certificate."],
            "D": ["Prove the descent property of an MM algorithm and the 1/k bound of proximal gradient, and state "
                  "the class of problems for which Nesterov's 1/k^2 order cannot be improved.",
                  "State the conditions under which the Polyak-Ruppert average is asymptotically efficient, and "
                  "which step exponents they exclude."],
            "I": ["Decide when to stop an optimizer by comparing its error with a tenth of the standard error, and "
                  "read non-convergence warnings from the shape of the likelihood.",
                  "Report standard errors from the curvature at the optimum only after checking that the optimum "
                  "was reached."],
        },
        results=[
            ("KKT conditions", r"\nabla f(x^*)+\sum_i\lambda_i\nabla g_i(x^*)=0,\quad g_i(x^*)\le 0,\quad "
                               r"\lambda_i\ge 0,\quad \lambda_i\,g_i(x^*)=0"),
            ("Weak duality", r"\max_{\lambda\ge 0}\,\min_x L(x,\lambda)\;\le\;\min_x\,\max_{\lambda\ge 0}L(x,\lambda),"
                             r"\qquad L(x,\lambda)=f(x)+\sum_i\lambda_i g_i(x)"),
            ("Fisher scoring for logistic regression", r"\beta^{+}=\beta+(X^\top WX)^{-1}X^\top(y-p),\qquad "
                                                       r"W=\operatorname{diag}\bigl(p_i(1-p_i)\bigr)"),
            ("The MM descent property", r"f(x_{k+1})\le g(x_{k+1}\mid x_k)\le g(x_k\mid x_k)=f(x_k)"),
            ("Soft thresholding", r"\operatorname{prox}_{\lambda|\cdot|}(v)=\arg\min_x\Bigl\{\lambda|x|+"
                                  r"\tfrac12(x-v)^2\Bigr\}=\operatorname{sign}(v)\,(|v|-\lambda)_+"),
            ("ISTA and FISTA", r"F(b_k)-F^*\le\frac{L\,\|b_0-b^*\|^2}{2k}\ \text{(ISTA)},\qquad "
                               r"F(b_k)-F^*\le\frac{2L\,\|b_0-b^*\|^2}{(k+1)^2}\ \text{(FISTA)}"),
        ],
        U=(0, 1), D=(8,), I=(11,),
        also=(("statkit.optim", "explainer/stats/kit/optim.py"),),
    ),
    Part(
        n=22, level="M", widget="trinitycurve", prereq=(9, 10, 21),
        question="Why does maximum likelihood work, and what happens when the model is wrong?",
        story="In Naples in 1893 Weldon measures the foreheads of 1,000 shore crabs, finds the histogram lopsided, "
              "and asks Karl Pearson whether it is two normal curves added together; Pearson matches five moments "
              "and solves a ninth-degree polynomial by hand. EM fits the same mixture by likelihood, and the part "
              "then proves the two promises of Part 9. Consistency comes from a KL divergence: the average log "
              "likelihood converges to a curve whose unique peak is the truth. Normality comes from expanding the "
              "score, and the curvature becomes the standard error, with the observed information tracking the "
              "precision of the sample in hand better than the expected. Wald, score and likelihood-ratio tests are "
              "three readings of one curve. Then each condition is broken in turn: in the Neyman-Scott pairs the "
              "nuisance parameters multiply and the MLE of the variance converges to half the truth, the mixture "
              "likelihood is unbounded, a null sits on a boundary, and the model is simply wrong, where the estimate "
              "converges to the KL projection and its honest standard error is the sandwich. It closes with quasi- "
              "and pseudo-likelihood, the likelihood principle on two stopping rules, and a glimpse of the Fisher "
              "metric.",
        handoff="The sandwich returns clustered in Part 23 and for M-estimators in Part 30; quasi-likelihood and GEE "
                "in Part 24; REML cures Neyman-Scott in Part 25; Jeffreys's prior returns in Part 26, AIC as an "
                "estimate of KL in Part 28, EM for missing data in Part 41, and Hodges and Le Cam in Part 47.",
        outside="Taylor expansion in several variables, the law of large numbers, the central limit theorem and "
                "Slutsky's lemma as used in Stage II.",
        objectives={
            "U": ["Explain what a mixture of two normal curves is and how EM splits each crab between the two "
                  "components.",
                  "State the two promises about maximum likelihood made in Part 9 and name the conditions they "
                  "need."],
            "M": ["Derive the asymptotic normality of the MLE from the expansion of the score, and compute Wald, "
                  "score and likelihood-ratio statistics and the intervals each one inverts to.",
                  "Prove that an EM step never lowers the likelihood, and compute a profile likelihood interval.",
                  "Derive the sandwich covariance under misspecification and estimate it."],
            "D": ["Explain the Efron-Hinkley argument for the observed information by conditioning on an ancillary, "
                  "and where it stops short of a finite-sample guarantee.",
                  "State Birnbaum's theorem, and say which of sufficiency and conditionality a p-value that depends "
                  "on the stopping rule gives up."],
            "I": ["Recognize an unbounded likelihood, label switching and a boundary null in a fitted mixture, and "
                  "calibrate the test by a parametric bootstrap of the same procedure.",
                  "Report sandwich standard errors when the variance model is in doubt, and say that they repair "
                  "the precision claimed and not the model."],
        },
        results=[
            ("Consistency through KL", r"M(\theta)=\mathbb{E}_{\theta_0}\log f(X;\theta),\qquad "
                                       r"M(\theta_0)-M(\theta)=\operatorname{KL}(f_{\theta_0}\,\|\,f_\theta)\ge 0"),
            ("Asymptotic normality", r"\sqrt n\,(\hat\theta-\theta_0)\xrightarrow{d}N\bigl(0,\,I(\theta_0)^{-1}\bigr)"),
            ("The trinity", r"W=(\hat\theta-\theta_0)^2\,nI(\hat\theta),\quad S=\frac{U(\theta_0)^2}{nI(\theta_0)},"
                            r"\quad \Lambda=2\bigl[\ell(\hat\theta)-\ell(\theta_0)\bigr],\quad\text{each}"
                            r"\xrightarrow{d}\chi^2_1\text{ under }H_0"),
            ("Neyman-Scott", r"x_{i1},x_{i2}\sim N(\mu_i,\sigma^2):\qquad \hat\sigma^2=\frac{1}{4n}\sum_{i=1}^n"
                             r"(x_{i1}-x_{i2})^2\xrightarrow{p}\frac{\sigma^2}{2}"),
            ("EM's lower bound", r"\ell(\theta)\ge\ell(\theta_t)+Q(\theta\mid\theta_t)-Q(\theta_t\mid\theta_t)"
                                 r"\ \Longrightarrow\ \ell(\theta_{t+1})\ge\ell(\theta_t)"),
            ("The sandwich", r"\sqrt n\,(\hat\theta-\theta^*)\xrightarrow{d}N\bigl(0,\,A^{-1}BA^{-1}\bigr),\qquad "
                             r"A=-\mathbb{E}_g\nabla^2\log f(X;\theta^*),\ B=\operatorname{Var}_g\nabla\log f(X;\theta^*)"),
        ],
        U=(0, 1), D=(4, 12, 13), I=(9, 10),
        also=(("statkit.mle", "explainer/stats/kit/mle.py"),),
    ),
    Part(
        n=23, level="M", widget="moultonschools", prereq=(12, 21, 22),
        question="What does the linear model really estimate, and how far can its standard errors be trusted?",
        story="In 1967 James Longley runs sixteen years of US employment data through the regression programs of "
              "the day and gets wrong digits: the predictors are nearly collinear, and the normal equations square "
              "the condition number that QR leaves alone. Part 12 derived least squares under four quiet "
              "assumptions, and this part drops each in turn, with one sandwich formula as the frame. The general "
              "linear hypothesis gives every F-test as a quadratic form. Correlated errors lead to Aitken's GLS, "
              "uneven errors to HC0 through HC3 and the wild bootstrap, and pupils grouped in the World's schools to "
              "Moulton's factor, the cluster-robust standard error and its failure with eight clusters. When the "
              "mean is not linear the fit still estimates the best linear predictor, and the sandwich is its correct "
              "standard error. A noisy regressor attenuates the slope, as Hubble's nebulae show. The part then fits "
              "quantiles and spline bases, returns to Householder's reflections and the digits lost to conditioning, "
              "and ends with the deletion formula, DFBETAS and masking.",
        handoff="Working correlations and GEE follow in Part 24; random intercepts model the clusters in Part 25; "
                "penalized splines are Part 29, robust regression and influence functions Part 30, the lasso when "
                "p > n Part 32, few-cluster difference-in-differences Part 37 and measurement error in full Part 41.",
        outside="Linear algebra at the level of Part 4 (projections, QR, quadratic forms) and the regression of "
                "Part 12.",
        objectives={
            "U": ["Explain why two programs can return different coefficients from the same ill-conditioned data, "
                  "and what centring and scaling do to the condition number."],
            "M": ["Test any linear hypothesis C beta = d by its F statistic, in the quadratic-form and the "
                  "two-fits versions, and show they agree.",
                  "Derive GLS by whitening, Moulton's factor for a cluster-level regressor, and the attenuation of a "
                  "slope under classical measurement error.",
                  "Compute HC and cluster-robust covariances and say which small-sample corrections each uses."],
            "D": ["State what least squares estimates when the mean is not linear and the regressors are random, "
                  "and prove that the sandwich, not the classical formula, gives its asymptotic variance.",
                  "Explain why cluster-robust inference fails with few clusters and what the restricted wild "
                  "cluster bootstrap does and does not repair."],
            "I": ["Choose the level to cluster at from the design, and report the number of clusters with the "
                  "standard error.",
                  "Solve least squares by QR, not the normal equations, and check a fit with leverage, DFBETAS "
                  "and deletion of groups of points to catch masking."],
        },
        results=[
            ("The sandwich frame", r"\operatorname{Var}(\hat\beta\mid X)=(X^\top X)^{-1}X^\top"
                                   r"\operatorname{Var}(\varepsilon)\,X\,(X^\top X)^{-1}"),
            ("The general linear hypothesis", r"F=\frac{(C\hat\beta-d)^\top\bigl[C(X^\top X)^{-1}C^\top\bigr]^{-1}"
                                              r"(C\hat\beta-d)}{q\,s^2}=\frac{(\mathrm{RSS}_0-\mathrm{RSS})/q}"
                                              r"{\mathrm{RSS}/(n-p)}\sim F_{q,\,n-p}"),
            ("Aitken's GLS", r"\hat\beta_{\mathrm{GLS}}=(X^\top\Omega^{-1}X)^{-1}X^\top\Omega^{-1}y,\qquad "
                             r"\operatorname{Var}(\varepsilon)=\sigma^2\Omega"),
            ("Moulton's factor", r"\frac{\operatorname{Var}_{\text{true}}(\hat\beta)}"
                                 r"{\operatorname{Var}_{\text{iid}}(\hat\beta)}=1+(m-1)\rho\quad"
                                 r"\text{(clusters of size } m\text{, regressor constant within clusters)}"),
            ("Attenuation", r"w=x+u:\qquad \hat\beta_w\xrightarrow{p}\lambda\beta,\qquad "
                            r"\lambda=\frac{\sigma_x^2}{\sigma_x^2+\sigma_u^2}"),
            ("The deletion formula", r"\hat\beta_{(i)}=\hat\beta-\frac{(X^\top X)^{-1}x_i\,e_i}{1-h_{ii}}"),
        ],
        U=(0,), D=(6,), I=(10, 11),
        also=(("statkit.ols", "explainer/stats/kit/ols.py"),),
    ),
    Part(
        n=24, level="M", widget="beetleirls", prereq=(14, 21, 22),
        question="How does one theory fit binary, count, positive and ordinal outcomes?",
        story="In 1935 Chester Bliss exposes 481 flour beetles to eight doses of carbon disulphide and counts the "
              "dead, from 6 of 59 to 60 of 60; his probit, the logit and the complementary log-log all draw a "
              "dose-response curve through them, and the last fits best. Nelder and Wedderburn's 1972 theory makes "
              "the logistic and Poisson regressions of Part 14 two members of one exponential dispersion family: a "
              "variance function, a link, and one algorithm, Fisher scoring written as weighted least squares on a "
              "working response. The deviance takes the place of the residual sum of squares, with a chi-squared "
              "reference that works for grouped data and is useless for binary data. Then the family is pushed "
              "until it gives: separated data send the slope to infinity, the World's doctor visits are "
              "overdispersed and full of zeros, and quasi-likelihood, the sandwich and the negative binomial "
              "answer in different ways. Tables become log-linear models, ordered categories get proportional odds, "
              "and pupils clustered in schools get GEE with a working correlation. The part ends by grading "
              "probability forecasts with proper scoring rules.",
        handoff="Conditional effects and GLMMs follow in Part 25; Bayesian GLMs and priors against separation in "
                "Part 26; links and terms are chosen by AIC and cross-validation in Part 28; penalized GLMs are "
                "Part 32, calibration and scoring Part 34, propensity scores Part 36, and Cox regression as a "
                "Poisson GLM Part 40.",
        outside="The logistic and Poisson regressions of Part 14, and the score identities of Part 22.",
        objectives={
            "U": ["Read a dose-response curve and its LD50, and say why a straight line is the wrong model for a "
                  "probability.",
                  "Name the three parts of a GLM for a given outcome: the family, the linear predictor and the "
                  "link."],
            "M": ["Put a distribution in exponential dispersion form and read off its mean, variance function and "
                  "canonical link.",
                  "Derive IRLS from Fisher scoring and implement it for any family and link.",
                  "Compare nested GLMs by analysis of deviance, and choose between quasi-Poisson, sandwich and "
                  "negative-binomial answers to overdispersion."],
            "D": ["State when the deviance has a chi-squared limit and prove why it cannot for binary data; give "
                  "the null law of the likelihood-ratio test for overdispersion on the boundary.",
                  "State what GEE estimates when the working correlation is wrong, and what changes when the "
                  "mean model is wrong as well."],
            "I": ["Diagnose separation from an IRLS path and report a Firth estimate in place of a diverging "
                  "one.",
                  "Grade probability forecasts with a proper scoring rule and a calibration plot, not with "
                  "accuracy."],
        },
        results=[
            ("The exponential dispersion family", r"f(y;\theta,\phi)=\exp\Bigl\{\frac{y\theta-b(\theta)}{\phi}"
                                                  r"+c(y,\phi)\Bigr\},\qquad \mathbb{E}\,y=b'(\theta)=\mu,\quad "
                                                  r"\operatorname{Var}y=\phi\,b''(\theta)=\phi V(\mu)"),
            ("IRLS", r"\beta^{+}=(X^\top WX)^{-1}X^\top Wz,\qquad z_i=\eta_i+(y_i-\mu_i)\frac{d\eta_i}{d\mu_i},"
                     r"\quad w_i=\frac{(d\mu_i/d\eta_i)^2}{V(\mu_i)}"),
            ("Deviance", r"D=2\phi\,(\ell_{\text{sat}}-\ell_{\text{fit}}),\qquad D_{\text{Poisson}}=2\sum_i\Bigl\{"
                         r"y_i\log\frac{y_i}{\hat\mu_i}-(y_i-\hat\mu_i)\Bigr\}"),
            ("The negative binomial as a gamma mixture", r"y\mid\lambda\sim\operatorname{Poisson}(\lambda),\ "
                                                         r"\lambda\sim\operatorname{Gamma}(k,\ \text{mean }\mu)"
                                                         r"\ \Longrightarrow\ \operatorname{Var}y=\mu+\frac{\mu^2}{k}"),
            ("Generalized estimating equations", r"\sum_{g}D_g^\top V_g^{-1}(y_g-\mu_g)=0,\qquad "
                                                 r"D_g=\frac{\partial\mu_g}{\partial\beta},\quad "
                                                 r"V_g=\text{the working covariance of cluster }g"),
            ("A proper score: Brier", r"\mathbb{E}_p(q-Y)^2=p(1-q)^2+(1-p)q^2\ \text{ is minimized at } q=p"),
        ],
        U=(0, 1), D=(5,), I=(6, 12),
        also=(("statkit.glm", "explainer/stats/kit/glm.py"),),
    ),
    Part(
        n=25, level="M", widget="steinrails", prereq=(15, 22, 23),
        question="How do you estimate many related things at once?",
        story="After their first 45 at-bats of 1970, eighteen major-league hitters each have a batting average, and "
              "Efron and Morris ask how to predict the rest of the season. Shrinking every average towards the "
              "common mean, by James and Stein's rule, cuts the total squared error by a factor of 3.5. The part "
              "explains why: the squared length of a noisy vector is too large on average, and Stein's lemma turns "
              "that into a risk below the MLE's for every true mean vector once there are three or more. Read as "
              "empirical Bayes, the rule estimates a normal prior from the data, and Tweedie's formula corrects the "
              "winner's curse. The same idea with a model is the random effect: variance components, the linear "
              "mixed model, Henderson's equations and the BLUP, whose shrinkage factor depends on each group's "
              "size, with REML repairing the bias of ML in the variances. The part then applies it to growth "
              "curves, crossed raters, the choice between fixed and random effects, GLMMs and the World's hospital "
              "league table, small areas, meta-analysis and the Rasch model.",
        handoff="The prior becomes explicit in the hierarchical Bayes of Part 26 (the eight schools) and its MCMC in "
                "Part 27; false discovery rates return as empirical Bayes in Part 33, fixed effects for panels in "
                "Part 37, frailty in Part 40, admissibility is proved in Part 45, and item response theory grades AI "
                "benchmarks in Part 64.",
        outside="The multivariate normal and quadratic forms (Part 4), and conjugate normal updating as in Part 15.",
        objectives={
            "U": ["Explain regression to the mean in a table of early-season averages, and why shrinking each "
                  "towards the group mean predicts better in total."],
            "M": ["Derive the James-Stein risk from Stein's lemma and SURE, and show the rule is empirical Bayes "
                  "under a normal prior.",
                  "Write a linear mixed model as V = ZGZ' + R, derive the BLUP of a random intercept and its "
                  "shrinkage factor, and fit it by REML.",
                  "Compute a random-effects meta-analysis with DerSimonian-Laird and Hartung-Knapp intervals."],
            "D": ["Derive the half-and-half chi-squared mixture for a likelihood-ratio test of one variance on "
                  "its boundary, and state the conditions under which it fails.",
                  "State what the James-Stein guarantee covers (total expected squared error, known equal "
                  "variances, p at least 3) and what it does not (any single coordinate)."],
            "I": ["Choose between fixed and random effects with the within and between slopes, Mundlak's model "
                  "and a Hausman test.",
                  "Report shrunk estimates for league tables and small areas with intervals for ranks, and say "
                  "which units gain and which lose from the pooling."],
        },
        results=[
            ("James-Stein", r"\hat\theta_{\mathrm{JS}}=\Bigl(1-\frac{p-2}{\|X\|^2}\Bigr)X,\qquad "
                            r"\mathbb{E}\|\hat\theta_{\mathrm{JS}}-\theta\|^2=p-(p-2)^2\,\mathbb{E}\frac{1}{\|X\|^2}<p"
                            r"\quad(X\sim N_p(\theta,I),\ p\ge 3)"),
            ("Stein's lemma and SURE", r"\mathbb{E}(X-\theta)h(X)=\mathbb{E}h'(X),\qquad "
                                       r"\mathbb{E}\|X+g(X)-\theta\|^2=\mathbb{E}\bigl[p+\|g\|^2+2\,\nabla\!\cdot g\bigr]"),
            ("Tweedie's formula", r"\mathbb{E}(\theta\mid x)=x+\sigma^2\,\frac{d}{dx}\log f(x)"),
            ("The linear mixed model", r"y=X\beta+Zu+e,\qquad V=ZGZ^\top+R,\qquad "
                                       r"\hat\beta=(X^\top V^{-1}X)^{-1}X^\top V^{-1}y"),
            ("The BLUP of a random intercept", r"\hat u_g=\lambda_g\,(\bar y_g-\bar x_g^\top\hat\beta),\qquad "
                                               r"\lambda_g=\frac{\tau^2}{\tau^2+\sigma^2/n_g}"),
            ("A variance on the boundary", r"H_0:\tau^2=0:\qquad \Lambda\xrightarrow{d}\tfrac12\chi^2_0+"
                                           r"\tfrac12\chi^2_1,\qquad P(\Lambda>2.71)\to 0.05"),
        ],
        U=(0,), D=(6,), I=(9, 11, 12),
        also=(("statkit.shrink", "explainer/stats/kit/shrink.py"), ("statkit.mixed", "explainer/stats/kit/mixed.py")),
    ),
]
