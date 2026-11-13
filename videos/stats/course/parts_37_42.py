"""Stage III, Master's: natural experiments, dependence in time and space, lifetimes, missing data, the exam (Parts 37-42)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=37, level="M", widget="forbiddentwfe", prereq=(35, 36),
        question="When the world runs an experiment by accident, how do you read it?",
        story="In 1854 two water companies ran their pipes down the same London streets, and Snow counted 315 "
              "cholera deaths per 10,000 houses for one against 37 for the other. The part collects the designs "
              "that borrow a piece of randomization in the same way. An instrument identifies an effect by a Wald "
              "ratio, and a weak one breaks the usual interval while the Anderson-Rubin set survives. A cutoff "
              "gives a regression discontinuity, read with the cutoff lens and checked for sorting. "
              "Difference-in-differences needs parallel trends and standard errors clustered by town, and here the "
              "part turns: on the World's staggered rollout the standard two-way fixed-effects regression says "
              "minus 0.49 when the true effect is 3.96, because it uses already-treated towns as controls. "
              "Callaway and Sant'Anna's estimator, synthetic control on Prop 99 and Nickell's bias in panels "
              "follow. The part ends with Manski's and Lee's bounds: what the data say before any design is "
              "assumed.",
        handoff="The serial correlation behind the placebo laws becomes the subject of Part 38; selection and "
                "measurement error return in Part 41; weak-instrument asymptotics are derived in Part 47, the "
                "influence functions of these estimators in Part 49, and partial identification goes to the "
                "frontier in Part 62.",
        outside="Potential outcomes and the adjustment methods of Parts 35 and 36; regression in matrix form "
                "(Part 23).",
        objectives={
            "U": ["Explain Snow's comparison of the two water companies and why it is as good as an experiment.",
                  "Compute a two-by-two difference-in-differences from four means and say what parallel trends "
                  "assumes."],
            "M": ["Compute a Wald ratio and a 2SLS estimate, and invert the Anderson-Rubin test when the first-stage "
                  "F is small.",
                  "Estimate a sharp and a fuzzy regression discontinuity by local linear fits and test the running "
                  "variable for sorting.",
                  "Decompose a two-way fixed-effects coefficient into its two-by-two comparisons and replace it "
                  "with an estimator that never uses treated units as controls."],
            "D": ["Derive the bias of a later-versus-earlier comparison when effects grow, and state the "
                  "restriction under which an honest parallel-trends interval is valid.",
                  "Explain what synthetic difference-in-differences adds to synthetic control and what its placebo "
                  "standard errors assume."],
            "I": ["Diagnose a design before trusting its estimate: the first-stage F, the density at the cutoff, "
                  "the pre-period event-study coefficients, the pre-treatment fit.",
                  "Report a difference-in-differences with standard errors clustered at the unit of treatment, and "
                  "check the test's size with placebo laws."],
        },
        results=[
            ("The Wald ratio", r"\beta_{\text{IV}}=\frac{\operatorname{Cov}(Y,Z)}{\operatorname{Cov}(D,Z)}"
                               r"=\frac{E[Y\mid Z=1]-E[Y\mid Z=0]}{E[D\mid Z=1]-E[D\mid Z=0]}"),
            ("Sharp regression discontinuity", r"\tau_{\text{RD}}=\lim_{x\downarrow c}E[Y\mid X=x]-"
                                               r"\lim_{x\uparrow c}E[Y\mid X=x],\qquad h_{\text{MSE}}\propto n^{-1/5}"),
            ("Difference-in-differences", r"\hat\tau=(\bar Y_{1,\text{post}}-\bar Y_{1,\text{pre}})-"
                                          r"(\bar Y_{0,\text{post}}-\bar Y_{0,\text{pre}})"),
            ("Goodman-Bacon decomposition", r"\hat\beta_{\text{TWFE}}=\sum_k w_k\,\hat\beta_k^{2\times 2},\qquad "
                                            r"w_k\ge 0,\ \sum_k w_k=1"),
            ("Nickell's bias with two periods", r"\operatorname{plim}_{N\to\infty}\hat\rho_{\text{FE}}-\rho="
                                                r"-\tfrac{1+\rho}{2}"),
            ("Manski's bounds, outcomes in [0, 1]", r"\text{width}=(1-r_1)+(1-r_0),\qquad r_a=\text{response rate in arm }a"),
        ],
        U=(0, 1, 7), D=(10, 12), I=(6, 8),
        also=(("statkit.quasi", "explainer/stats/kit/quasi.py"),),
    ),
    Part(
        n=38, level="M", widget="kalmangain", prereq=(17, 22),
        question="What changes when memory is long, the variance moves, or the state is hidden?",
        story="Hurst measures the Nile for a dam and finds that the rescaled range of its yearly minima grows like "
              "n to the 0.85, where white noise gives about a half. Part 17 assumed stationary series with short "
              "memory and constant variance, fully observed, and this part drops each assumption in turn. The "
              "periodogram is inconsistent until it is smoothed. A unit root gives the Dickey-Fuller statistic a "
              "Brownian limit, so the normal critical value rejects 45.6% of true random walks, and two independent "
              "walks regress on each other with a significant slope 77% of the time. GARCH lets the variance "
              "cluster on the DAX, and fractional differencing gives the Nile's long memory a model in which 663 "
              "years are worth about 3.5. Then the state is hidden: the Kalman filter tracks the Nile's level at "
              "Aswan and finds its fall into 1899, with smoothing, EM, particle filters and Hamilton's regimes "
              "after it. The part ends with VARs, the block bootstrap and how forecasters are evaluated without "
              "leakage.",
        handoff="Dependence in every direction, with kriging as its filter, is Part 39; EM returns for missing "
                "data in Part 41; Part 44 proves Donsker's theorem behind the Dickey-Fuller limit, Part 53 treats "
                "Gaussian processes, and Part 64 evaluates pretrained forecasters.",
        outside="The ACF, ARMA models and forecasting of Part 17, and likelihood (Part 22).",
        objectives={
            "U": ["Explain Hurst's rescaled range and what an exponent well above one half says about a series.",
                  "Name the four things Part 17 assumed and recognize a path that breaks each."],
            "M": ["Test for a unit root with the Dickey-Fuller statistic and its own critical values, and for "
                  "cointegration with Engle-Granger.",
                  "Fit a GARCH(1,1) and forecast its variance h steps ahead.",
                  "Run the Kalman filter and the RTS smoother for a local-level model and estimate its two variances "
                  "by the prediction-error likelihood."],
            "D": ["Derive the hyperbolic decay of an ARFIMA's autocorrelations and the rate at which the variance "
                  "of the mean falls under long memory.",
                  "Compare the EKF, the UKF and the bootstrap particle filter on a nonlinear state equation and "
                  "say what each approximates."],
            "I": ["Evaluate a forecaster by rolling origin with MASE against naive benchmarks, and recognize "
                  "selection on the test outcomes as leakage."],
        },
        results=[
            ("Herglotz", r"\gamma(h)=\int_{-\pi}^{\pi}e^{ih\omega}\,dF(\omega)"),
            ("Dickey-Fuller limit (with a constant)", r"t_{\hat\gamma}\Rightarrow\frac{\int_0^1\bar W\,dW}"
                                                      r"{\bigl(\int_0^1\bar W^2\,dr\bigr)^{1/2}},\qquad "
                                                      r"\bar W(r)=W(r)-\int_0^1 W(s)\,ds"),
            ("GARCH(1,1) and its forecast", r"\sigma_t^2=\omega+\alpha\varepsilon_{t-1}^2+\beta\sigma_{t-1}^2,\qquad "
                                            r"E_t\sigma_{t+h}^2-\bar\sigma^2=(\alpha+\beta)^{h-1}"
                                            r"(\sigma_{t+1}^2-\bar\sigma^2)"),
            ("Long memory", r"\rho(h)\sim c\,h^{2d-1},\qquad \operatorname{Var}(\bar X_n)\asymp n^{2d-1},\qquad "
                            r"H=d+\tfrac12"),
            ("Kalman filter, local level", r"K_t=\frac{P_{t\mid t-1}}{P_{t\mid t-1}+\sigma_v^2},\quad "
                                           r"m_t=m_{t-1}+K_t(y_t-m_{t-1}),\quad "
                                           r"P_{t+1\mid t}=(1-K_t)P_{t\mid t-1}+\sigma_w^2"),
            ("Steady-state gain", r"K=\tfrac12\bigl(\sqrt{q^2+4q}-q\bigr),\qquad q=\sigma_w^2/\sigma_v^2"),
        ],
        U=(0, 1), D=(6, 9), I=(12,),
        also=(("statkit.ts", "explainer/stats/kit/ts.py"),),
    ),
    Part(
        n=39, level="M", widget="krigeline", prereq=(25, 29),
        question="How do you predict where nobody measured?",
        story="In 1951 Krige values blocks of ore from boreholes with weights that account for how grades covary "
              "with each other and with the block. The part builds that predictor on the World's pollution field, "
              "hidden but for 300 stations, and on the Meuse flood plain's zinc. A random field has a covariance, "
              "Bochner says which functions qualify, and the variogram estimates it. Kriging is the best linear "
              "unbiased predictor, derived with a Lagrange multiplier, and it is the posterior mean of a Gaussian "
              "process. The Matérn family sets the smoothness, and here the part turns: under infill the variance "
              "and the range cannot both be learned, only a ridge of them, though predictions along the ridge "
              "barely change. Likelihood costs n cubed, so Vecchia's approximation and sparse precision matrices "
              "from the SPDE carry it to 100,000 locations. Areal data, point patterns on Snow's map, spatial "
              "confounding and Bayesian optimization follow, and the part ends by cross-validating in spatial "
              "blocks, where the error is honest.",
        handoff="Shared frailties are random effects for lifetimes in Part 40; prediction at unmeasured places "
                "is imputation in Part 41; Brownian motion, the first Gaussian process, is built in Part 44, "
                "Gaussian-process priors and their contraction rates are Part 53, and predicting in a new region "
                "is distribution shift in Part 60.",
        outside="Mixed models and REML (Part 25), smoothing (Part 29), and the multivariate normal's conditioning "
                "formula.",
        objectives={
            "U": ["Explain Tobler's first law and why 300 correlated stations carry far fewer than 300 "
                  "observations' worth of information about a mean.",
                  "Read a kriged map together with its standard-error map."],
            "M": ["Estimate and fit a variogram, and read its nugget, sill and range.",
                  "Derive the kriging weights and show that simple kriging is Gaussian conditioning.",
                  "Fit a Matérn covariance by REML and approximate the likelihood by Vecchia's method."],
            "D": ["State Zhang's result on what is identifiable under infill asymptotics and explain why "
                  "predictions are nearly constant along the ridge.",
                  "Explain how the SPDE turns a Matérn field into a Gaussian Markov random field with a sparse "
                  "precision matrix."],
            "I": ["Validate a spatial predictor with blocked cross-validation and standardized errors, not random "
                  "folds alone.",
                  "Recognize spatial confounding: a spatial random effect does not remove bias from an unmeasured "
                  "confounder that varies at the exposure's scale."],
        },
        results=[
            ("The variogram", r"\gamma(h)=\tfrac12\operatorname{Var}\bigl(Z(s+h)-Z(s)\bigr)=C(0)-C(h)"),
            ("Simple kriging", r"\hat Z(s_0)=\mu+k_0^\top K^{-1}(z-\mu\mathbf 1),\qquad "
                               r"\operatorname{Var}=C(0)-k_0^\top K^{-1}k_0"),
            ("The Matérn covariance", r"C(d)=\sigma^2\,\frac{2^{1-\nu}}{\Gamma(\nu)}"
                                      r"\Bigl(\frac{\sqrt{2\nu}\,d}{\rho}\Bigr)^{\nu}"
                                      r"K_\nu\Bigl(\frac{\sqrt{2\nu}\,d}{\rho}\Bigr)"),
            ("Zhang (2004)", r"\text{under infill, } d\le 3:\ \text{only }\sigma^2/\rho^{2\nu}"
                             r"\text{ is consistently estimable}"),
            ("Vecchia's approximation", r"p(z)\approx\prod_{i=1}^{n}p\bigl(z_i\mid z_{N(i)}\bigr),\qquad "
                                        r"N(i)\subseteq\{1,\dots,i-1\},\ |N(i)|\le m"),
            ("Moran's I", r"I=\frac{n}{\sum_{i,j}w_{ij}}\,\frac{\sum_{i,j}w_{ij}(z_i-\bar z)(z_j-\bar z)}"
                          r"{\sum_i(z_i-\bar z)^2}"),
        ],
        U=(0, 1), D=(5, 8), I=(11, 14),
        also=(("statkit.spatial", "explainer/stats/kit/spatial.py"),),
    ),
    Part(
        n=40, level="M", widget="censorstairs", prereq=(22, 24),
        question="How do you average lifetimes you have not finished watching?",
        story="Freireich's leukaemia trial ends with twelve of twenty-one patients on 6-MP still in remission: "
              "averaging their times as if they had relapsed gives 17.1 weeks, and averaging only the relapses "
              "gives 12.1, and both are wrong. The part builds the answer from the risk set. The hazard and the "
              "survival function determine each other, and under independent censoring Kaplan and Meier's product "
              "over the shrinking risk set estimates survival, drawn as the staircase with Greenwood's variance "
              "around it. Aalen's counting processes make every estimator an integral against a martingale. The "
              "log-rank test compares observed and expected relapses over risk sets, and Cox's partial likelihood "
              "estimates a hazard ratio without the baseline. Then the traps: a hazard ratio drifts when frailty "
              "selects the survivors, and counting the wait for a heart transplant as treated time gives Stanford's "
              "programme a hazard ratio of 0.27 where the time-varying analysis gives 1.13. Competing risks, "
              "frailty models and prediction under censoring close the part.",
        handoff="Censoring is one kind of missing data, and its weights return in Part 41; Part 44 builds the "
                "martingales and Rebolledo's central limit theorem, Part 48 treats the Kaplan-Meier curve as an "
                "empirical process, Part 49 shows Cox's estimator is semiparametrically efficient, and Part 58 "
                "monitors survival trials as they accumulate.",
        outside="Likelihood and its asymptotics (Part 22) and generalized linear models (Part 24).",
        objectives={
            "U": ["Compute a Kaplan-Meier curve by hand from a risk table and read a median from it.",
                  "Explain why dropping the censored, or counting them as events, biases a survival estimate."],
            "M": ["Derive Greenwood's variance and compute a log-log interval for S(t).",
                  "Compute the log-rank statistic from observed and expected events over risk sets.",
                  "Write Cox's partial likelihood, fit it, and check proportional hazards with Schoenfeld "
                  "residuals."],
            "D": ["Show that the counting process minus its compensator is a martingale and write the "
                  "Nelson-Aalen estimator as a stochastic integral against it."],
            "I": ["Report a restricted mean survival time beside a hazard ratio, and say why a period-specific "
                  "hazard ratio is not a causal effect.",
                  "Recognize immortal time and remove it by coding treatment as time-varying."],
        },
        results=[
            ("Hazard and survival", r"S(t)=\exp\Bigl(-\int_0^t h(u)\,du\Bigr)=e^{-H(t)}"),
            ("Kaplan-Meier", r"\hat S(t)=\prod_{t_k\le t}\Bigl(1-\frac{d_k}{n_k}\Bigr)"),
            ("Greenwood's variance", r"\widehat{\operatorname{Var}}\,\hat S(t)=\hat S(t)^2"
                                     r"\sum_{t_k\le t}\frac{d_k}{n_k(n_k-d_k)}"),
            ("The counting-process martingale", r"M(t)=N(t)-\int_0^t Y(u)\,h(u)\,du"),
            ("The log-rank statistic", r"\frac{\bigl(\sum_k (d_{1k}-n_{1k}d_k/n_k)\bigr)^2}"
                                       r"{\sum_k \frac{n_{1k}n_{0k}\,d_k(n_k-d_k)}{n_k^2(n_k-1)}}"
                                       r"\ \approx\ \chi^2_1"),
            ("Cox's partial likelihood", r"L(\beta)=\prod_{i:\,\delta_i=1}\frac{e^{x_i^\top\beta}}"
                                         r"{\sum_{j\in R(t_i)}e^{x_j^\top\beta}}"),
        ],
        U=(0, 1, 3), D=(6,), I=(10, 11),
        also=(("statkit.survival", "explainer/stats/kit/survival.py"),),
    ),
    Part(
        n=41, level="M", widget="maskmean", prereq=(18, 22, 36),
        question="Data are missing or mismeasured: when does it matter, and what can be done?",
        story="In 1943 Wald is shown where returning bombers were hit and says to armour where they were not: the "
              "planes hit there are the ones that did not return. The part gives the idea its definitions. Rubin's "
              "three mechanisms say whether missingness depends on nothing, on what was seen, or on the missing "
              "value itself, and the World's income survey is masked under each. Complete cases, mean imputation "
              "and last observation carried forward each fail in a way that can be computed. Under missing at "
              "random the likelihood ignores the mechanism, so EM fits a normal with holes, and multiple "
              "imputation with Rubin's rules carries the uncertainty that a single imputation hides. Weighting "
              "respondents by the inverse of their response probability is the causal inference of Part 36 under "
              "another name. When the value itself drives the missingness nothing in the data can show it: "
              "Heckman's model, pattern mixtures and tipping points are assumptions made explicit. The part ends "
              "with MRP for a self-selected poll, and with measurement error, which attenuates a slope by the "
              "reliability.",
        handoff="The comprehensive exam's second case starts with a missing confounder (Part 42); Part 45 proves "
                "EM's convergence and measures the information lost, Part 49 derives AIPW's efficiency, Part 62 "
                "uses proxies for unmeasured confounders, and Part 63 treats privacy noise as deliberate "
                "measurement error.",
        outside="Survey weighting (Part 18), likelihood (Part 22), and propensity scores and AIPW from Part 36.",
        objectives={
            "U": ["Explain Wald's argument about the bombers as a statement about which data are missing.",
                  "Show by example what complete cases, mean imputation and LOCF each do to a mean, a spread "
                  "and a correlation."],
            "M": ["Classify a missingness mechanism as MCAR, MAR or MNAR and derive ignorability under MAR.",
                  "Combine m completed-data analyses by Rubin's rules and compute the fraction of missing "
                  "information.",
                  "Estimate a mean with missing outcomes by IPW and AIPW, and correct a slope for classical "
                  "measurement error by regression calibration."],
            "D": ["Explain why MAR cannot be tested against MNAR from the observed data, and what Heckman's "
                  "exclusion restriction and normality buy.",
                  "State the congeniality condition under which Rubin's variance is valid."],
            "I": ["Report an analysis with missing data: the mechanism assumed, the imputation model, and a "
                  "tipping-point sensitivity analysis.",
                  "Adjust a self-selected poll by MRP and say what residual selection the cells cannot remove."],
        },
        results=[
            ("Ignorability under MAR", r"p(y_{\text{obs}},r\mid\theta,\psi)=p(r\mid y_{\text{obs}},\psi)\,"
                                       r"p(y_{\text{obs}}\mid\theta)"),
            ("Rubin's rules", r"\bar Q=\frac1m\sum_{j=1}^m\hat Q_j,\qquad T=\bar W+\Bigl(1+\frac1m\Bigr)B,\qquad "
                              r"B=\frac{1}{m-1}\sum_j(\hat Q_j-\bar Q)^2"),
            ("IPW and AIPW means", r"\hat\mu_{\text{IPW}}=\frac1n\sum_i\frac{R_iY_i}{\pi(X_i)},\qquad "
                                   r"\hat\mu_{\text{AIPW}}=\frac1n\sum_i\Bigl[m(X_i)+\frac{R_i}{\pi(X_i)}"
                                   r"\bigl(Y_i-m(X_i)\bigr)\Bigr]"),
            ("Heckman's correction", r"E[Y\mid X,Z,S=1]=X^\top\beta+\rho\sigma\,\lambda(Z^\top\gamma),\qquad "
                                     r"\lambda(u)=\frac{\phi(u)}{\Phi(u)}"),
            ("Attenuation", r"\operatorname{plim}\hat\beta_{\text{naive}}=\lambda\beta,\qquad "
                            r"\lambda=\frac{\sigma_x^2}{\sigma_x^2+\sigma_u^2}"),
        ],
        U=(0, 2), D=(6,), I=(7, 9),
        also=(("statkit.mi", "explainer/stats/kit/mi.py"),),
    ),
    Part(
        n=42, level="M", widget="clustertowns", prereq=(22, 35, 36, 41),
        question="A client writes with two questions and a deadline: can you do the master's?",
        story="The World's ministry of health writes with two questions and six weeks. The first is a trial to "
              "design: would community health workers lower blood pressure by 4 mm Hg? Households in a town "
              "contaminate one another, so towns are randomized, the pilot gives an intraclass correlation of "
              "0.034, and a design effect of 3.70 turns 267 adults per arm into 21 towns per arm; simulation shows "
              "the individual-level analysis rejecting a true null 30% of the time. The second is a survey to "
              "analyse: users of a salt substitute have pressure 6.7 mm Hg higher, because the people told their "
              "pressure was high are the ones who bought it. A causal graph picks the adjustment set and rules out "
              "the mediator and the collider, multiple imputation fills the withheld incomes, AIPW gives minus "
              "2.22, and a robustness value says how strong a hidden confounder would have to be. Then the "
              "comprehensive exam: twelve problems from Stage III, each posed, paused and solved, from a Poisson "
              "sandwich to a Kaplan-Meier curve. The MSc goes on the Transcript.",
        handoff="Stage IV begins: Part 43 rebuilds probability on measure theory, and the PhD core (Parts 43-55) "
                "proves what the exam's problems only used, ending in the qualifying exam of Part 55.",
        outside="All of Stage III (Parts 21-41); the two cases draw on Parts 13, 35, 36 and 41.",
        objectives={
            "U": ["Explain why a trial of a community programme randomizes towns rather than households.",
                  "State an estimand in words before choosing a design."],
            "M": ["Estimate an intraclass correlation from a one-way ANOVA and size a cluster-randomized trial "
                  "with its design effect.",
                  "Choose an adjustment set from a causal graph, impute a missing confounder and estimate an "
                  "effect by AIPW with Rubin's rules.",
                  "Solve the twelve exam problems, from a sandwich standard error to a Greenwood interval, "
                  "without notes."],
            "D": ["Derive REML's variance estimate from the likelihood of error contrasts, and explain why AIC is "
                  "not consistent for a nested true model while BIC is."],
            "I": ["Test an analysis plan by simulation before the data arrive: its type I error and its power.",
                  "Write a one-page report with the estimate, its interval, a robustness value with a benchmark, "
                  "and what the design cannot support."],
        },
        results=[
            ("ICC from a one-way ANOVA", r"\hat\sigma_b^2=\frac{\text{MSB}-\text{MSW}}{m},\qquad "
                                         r"\hat\rho=\frac{\hat\sigma_b^2}{\hat\sigma_b^2+\text{MSW}}"),
            ("Towns per arm", r"k=\frac{2(z_{1-\alpha/2}+z_{1-\beta})^2\sigma^2}{\delta^2}\cdot"
                              r"\frac{1+(m-1)\rho}{m}\ \ge\ \frac{2(z_{1-\alpha/2}+z_{1-\beta})^2\rho\,\sigma^2}"
                              r"{\delta^2}"),
            ("AIPW for an average effect", r"\hat\tau=\frac1n\sum_i\Bigl[m_1(X_i)-m_0(X_i)+"
                                           r"\frac{T_i\,(Y_i-m_1(X_i))}{e(X_i)}-"
                                           r"\frac{(1-T_i)(Y_i-m_0(X_i))}{1-e(X_i)}\Bigr]"),
            ("Robustness value", r"\text{RV}=\tfrac12\bigl(\sqrt{f^4+4f^2}-f^2\bigr),\qquad "
                                 r"f=\frac{|t|}{\sqrt{\text{df}}}"),
            ("Poisson MLE: two standard errors", r"\text{SE}_{\text{model}}=\sqrt{\bar y/n},\qquad "
                                                 r"\text{SE}_{\text{sandwich}}=\frac1n\sqrt{\sum_i(y_i-\bar y)^2}"),
            ("Benjamini-Hochberg", r"\text{reject }p_{(1)},\dots,p_{(k)},\qquad "
                                   r"k=\max\{i:\ p_{(i)}\le iq/m\}"),
        ],
        U=(0, 1), I=(2, 3, 6),
        also=(("The World's ministry block", "explainer/stats/world.py"),),
    ),
]
