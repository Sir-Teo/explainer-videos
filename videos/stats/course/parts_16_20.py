"""Stage II, Bachelor's: Methods (Parts 16-20)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=16, level="U", widget="bootspike", prereq=(8, 10, 11),
        question="Can the data stand in for the model when you need a standard error or a p-value?",
        story="In 1979 Efron asks for the standard error of a correlation from 15 law schools, r = 0.776, and answers "
              "by resampling the 15 schools with replacement: 0.135, against 0.115 from the normal formula. The part "
              "first builds the older model-free tools. Permutation tests get exact p-values from exchangeability, "
              "and Darwin's maize and the Challenger temperatures carry the sign test, Wilcoxon's signed ranks and "
              "Mann-Whitney's count of pairs. Then come the jackknife, the bootstrap's two worlds, and four ways "
              "to turn replicates into an interval, each scored on the Coverage Board. The turn is the tank "
              "factory: for the maximum of a uniform sample about 63% of resamples repeat the sample's own maximum, "
              "and the percentile interval covers 0% of the time. The part ends with two more uses of the data on "
              "itself, cross-validation and the kernel density estimate.",
        handoff="Resampling in blocks handles dependent data in Part 17; cross-validation returns in Parts 19 and 28, "
                "kernels in Part 29, Pitman efficiency and influence functions in Part 30, exchangeability as "
                "conformal prediction in Parts 34 and 57, and the bootstrap's consistency is proved in Part 47.",
        outside="Stage I of this series (sampling distributions and tests, Parts 8 and 10) and the intervals of Part 11.",
        objectives={
            "U": ["Carry out a permutation test and a bootstrap by hand on a small sample, and say what each assumes.",
                  "Compute the sign, signed-rank and Mann-Whitney statistics and read U/(mn) as the chance that one "
                  "group's value beats the other's."],
            "M": ["Derive the exact null distribution of the signed-rank statistic from its generating function.",
                  "Compute jackknife and bootstrap standard errors, and percentile, basic and bootstrap-t intervals, "
                  "and explain why they differ on skewed data."],
            "D": ["Show that the bootstrap distribution of a uniform sample's maximum has an atom of mass "
                  "1 - (1 - 1/n)^n at the estimate, and explain why m-out-of-n resampling repairs it."],
            "I": ["Choose between a rank test, a permutation test and a t-test for a given design, and report which "
                  "hypothesis each one tests.",
                  "Recognise the settings where the ordinary bootstrap fails: extremes, boundaries, infinite "
                  "variance, dependence and very small samples."],
        },
        results=[
            ("Permutation p-value", r"p=\frac{\#\{\pi:\ T(\pi)\ge T_{\text{obs}}\}}{\#\{\pi\}}"
                                    r"\quad(\text{exact under exchangeability})"),
            ("Signed-rank null", r"\mathbb{E}\,x^{W^+}=\prod_{k=1}^{n}\frac{1+x^{k}}{2}"),
            ("Mann-Whitney", r"U=R_x-\tfrac{m(m+1)}{2}=\#\{(i,j):x_i>y_j\},\qquad \frac{U}{mn}=\text{AUC}"),
            ("Jackknife", r"\widehat{\text{bias}}=(n-1)\bigl(\bar\theta_{(\cdot)}-\hat\theta\bigr),\qquad "
                          r"\widehat{\text{se}}^2=\frac{n-1}{n}\sum_{i=1}^{n}\bigl(\hat\theta_{(i)}-\bar\theta_{(\cdot)}\bigr)^2"),
            ("Bootstrap standard error", r"\widehat{\text{se}}_{\text{boot}}=\operatorname{sd}^*\bigl(\hat\theta(X_1^*,\dots,X_n^*)\bigr),"
                                         r"\qquad X_i^*\ \text{iid from}\ \hat F_n"),
            ("The failure for a maximum", r"P^*\bigl(\hat\theta^*=\hat\theta\bigr)=1-\Bigl(1-\frac1n\Bigr)^{n}\longrightarrow 1-e^{-1}"),
        ],
        U=(0, 1, 2, 3, 4, 7, 11), I=(8, 10), D=(9,),
        also=(("statkit.bootstrap", "explainer/stats/kit/bootstrap.py"), ("statkit.ranks", "explainer/stats/kit/ranks.py")),
    ),
    Part(
        n=17, level="U", widget="ar2cycle", prereq=(7, 12),
        question="How do you do statistics when each observation remembers the last?",
        story="In 1926 Yule shows that Church of England marriages and mortality in England and Wales correlate at "
              "0.95 over 1866 to 1911, and at 0.02 once each series is differenced; a year later he explains the "
              "sunspot cycle with a pendulum pelted by peas. The part builds the language for such data: "
              "stationarity, the correlogram, and the price of memory, which makes 100 observations of an AR(1) "
              "with correlation 0.7 worth about 18. AR, MA and ARMA models are read from their roots against the "
              "unit circle, and complex roots give the pseudo-cycles of Slutsky and of Yule's sunspot AR(2). "
              "Box and Jenkins's cycle of identification, estimation and checking leads to forecasts whose "
              "intervals widen, to the decomposition of the Mauna Loa record and to Holt-Winters smoothing. The "
              "part returns to Yule: two independent random walks pass a slope test three times in four, and "
              "differencing repairs it. It closes with the M-competitions, where simple methods and combinations "
              "are hard to beat.",
        handoff="Rolling-origin evaluation returns in Part 19; spectra, unit-root tests, cointegration, GARCH and the "
                "Kalman filter are Part 38; dependence in space is Part 39, and martingales and mixing are Part 44.",
        outside="Stage I of this series, and least squares from Part 12; complex numbers for the roots.",
        objectives={
            "U": ["Read a correlogram with its bands, and tell white noise, an autoregression and a random walk apart.",
                  "Explain why the correlation of two trending series says little, and what differencing does."],
            "M": ["Check stationarity and invertibility of an ARMA model from its roots, and compute the period of "
                  "an AR(2) with complex roots.",
                  "Fit an autoregression by Yule-Walker or least squares, check its residuals with Ljung-Box, and "
                  "forecast with intervals."],
            "D": ["Derive the variance of the mean of a stationary series from its autocovariances, and state why the "
                  "t statistic of a regression between independent random walks does not settle as n grows."],
            "I": ["Score forecasts by MASE on a held-out stretch against the naive and seasonal-naive benchmarks.",
                  "Report a mean or a trend from autocorrelated data with a standard error that allows for the "
                  "dependence."],
        },
        results=[
            ("The mean of an AR(1)", r"\operatorname{Var}(\bar X)\approx\frac{\sigma_X^2}{n}\cdot\frac{1+\rho}{1-\rho},"
                                     r"\qquad n_{\text{eff}}=n\,\frac{1-\rho}{1+\rho}"),
            ("Stationarity (causality)", r"\phi(z)=1-\phi_1z-\dots-\phi_pz^p\neq 0\quad\text{for all }|z|\le 1"),
            ("AR(2) pseudo-cycle", r"\phi_1^2+4\phi_2<0:\quad \rho(h)=(-\phi_2)^{h/2}\,\frac{\cos(h\omega-\psi)}{\cos\psi},"
                                   r"\quad \cos\omega=\frac{\phi_1}{2\sqrt{-\phi_2}}"),
            ("Yule-Walker", r"\rho(h)=\phi_1\rho(h-1)+\dots+\phi_p\rho(h-p),\qquad h=1,\dots,p"),
            ("AR(1) forecast", r"\hat X_{n+h}=\mu+\phi^{h}(X_n-\mu),\qquad "
                               r"\operatorname{Var}(X_{n+h}-\hat X_{n+h})=\sigma^2\,\frac{1-\phi^{2h}}{1-\phi^{2}}"),
            ("Exponential smoothing", r"\ell_t=\alpha y_t+(1-\alpha)\ell_{t-1}=\alpha\sum_{j\ge 0}(1-\alpha)^{j}y_{t-j}"
                                      r"\quad(\text{up to the starting value})"),
        ],
        U=(0, 1, 2, 6, 7, 9), I=(8, 10),
        also=(("statkit.ts", "explainer/stats/kit/ts.py"),),
    ),
    Part(
        n=18, level="U", widget="digestpoll", prereq=(8, 11),
        question="How can 1,000 people speak for a nation, and how can 2.4 million fail to?",
        story="In 1936 the Literary Digest counts 2.4 million ballots, gives Landon 57%, and Roosevelt wins in a "
              "landslide. The World reruns it: an election in which Blue has 38.2% of 741,311 adults, a mailing to "
              "the telephone-and-car registers, and 34,588 returns that put Blue at 58.0%, while a random sample "
              "of 1,000 says 38.0%. The part separates the frame's bias from nonresponse, then derives Meng's "
              "identity, in which the error of any sample is a correlation times a size factor times a spread; by "
              "it the returns are worth 6 random voters. Neyman's design-based inference follows: the population "
              "is fixed and only the selection is random. Simple random sampling with its finite-population "
              "correction, stratification with Neyman allocation, clusters with Kish's design effect, and the "
              "Horvitz-Thompson, ratio and regression estimators are each checked on the island. The part ends "
              "with weighting and raking, which pull the Digest back to 49.1% and no further, and with the polls "
              "of 1948, 2016 and 2020.",
        handoff="The survey block's vote is the classification example of Part 19 and design weights carry the "
                "capstone in Part 20; MRP returns in Part 25, inverse probability weighting in Part 35, missing-data "
                "mechanisms in Part 41, and census privacy in Part 63.",
        outside="Stage I of this series: expectation, variance and covariance, and the confidence intervals of Part 8.",
        objectives={
            "U": ["Explain why a random sample of 1,000 beats a self-selected sample of millions, naming frame bias "
                  "and nonresponse bias.",
                  "Compute the standard error of a simple random sample's mean with the finite-population "
                  "correction, and the sample size a margin of error needs."],
            "M": ["Derive Meng's identity and the effective sample size of a biased sample.",
                  "Derive Neyman allocation, and compute Kish's design effect for a cluster sample."],
            "D": ["Prove that the Horvitz-Thompson estimator is unbiased under any design with positive inclusion "
                  "probabilities, and use Basu's elephants to say what unbiasedness does not buy."],
            "I": ["Weight a sample by post-stratification or raking, report Kish's effective sample size, and say "
                  "which kind of nonresponse the weights cannot repair."],
        },
        results=[
            ("Meng's identity", r"\bar y_R-\bar y_N=\rho_{R,Y}\,\sqrt{\frac{1-f}{f}}\;\sigma_Y,\qquad f=\frac nN,"
                                r"\qquad n_{\text{eff}}\approx\frac{f}{1-f}\cdot\frac{1}{\rho_{R,Y}^{2}}"),
            ("Simple random sampling", r"\operatorname{Var}(\bar y)=\Bigl(1-\frac nN\Bigr)\frac{S^2}{n}"),
            ("Neyman allocation", r"n_h=n\,\frac{N_hS_h}{\sum_k N_kS_k}"),
            ("Kish's design effect", r"\text{deff}=1+(m-1)\rho,\qquad n_{\text{eff}}=\frac{n}{\text{deff}}"),
            ("Horvitz-Thompson", r"\hat T=\sum_{i\in s}\frac{y_i}{\pi_i},\qquad \mathbb{E}\,\hat T=\sum_{i=1}^{N}y_i"
                                 r"\quad\text{whenever every }\pi_i>0"),
            ("Ratio estimator", r"\hat{\bar y}_{\text{ratio}}=\frac{\bar y}{\bar x}\,\bar X_N"),
        ],
        U=(0, 1, 3, 4, 5), I=(9, 10), D=(7,),
        also=(("statkit.survey", "explainer/stats/kit/survey.py"), ("The World", "explainer/stats/world.py")),
    ),
    Part(
        n=19, level="U", widget="knntradeoff", prereq=(12, 14, 16),
        question="How do you predict well, and how do you know how well you predict?",
        story="Hamilton and Madison both claimed twelve of the Federalist papers; in 1964 Mosteller and Wallace "
              "settle it from the rates of dull words such as 'upon', which is in every one of Hamilton's 51 papers "
              "and absent from 11 of Madison's 14. The part turns from parameters to prediction. Polynomials "
              "fitted to 30 points show training error falling while test error explodes, and the gap is the "
              "optimism 2σ²p/n. Test error splits into noise, squared bias and variance, simulated for k nearest "
              "neighbours, and cross-validation estimates it from the data in hand. Nearest neighbours, naive "
              "Bayes against logistic regression, trees with pruning, and ridge against the lasso are each tuned "
              "that way, and confusion matrices, ROC curves and calibration say what a classifier's errors cost. "
              "Naive Bayes then gives all twelve disputed papers to Madison; ridge logistic regression agrees on "
              "eleven and leans to Hamilton on No. 55. The part ends with leakage: features selected outside "
              "the cross-validation loop make pure noise look predictable.",
        handoff="The held-out check is used in Part 20; AIC, BIC and cross-validation are compared in Part 28, "
                "smoothers return in Part 29, the lasso in Part 32, conformal prediction in Part 34, and learning "
                "theory bounds test error in Part 54.",
        outside="Least squares (Part 12), logistic regression (Part 14) and cross-validation's first look (Part 16).",
        objectives={
            "U": ["Explain why training error understates test error, and read a curve of both against model "
                  "complexity.",
                  "Run k-fold cross-validation to choose a tuning parameter, and read a confusion matrix and an ROC "
                  "curve."],
            "M": ["Derive the bias-variance decomposition and the optimism of a linear fit.",
                  "Derive the lasso's soft threshold and ridge's proportional shrinkage for an orthonormal design."],
            "D": ["State what k-fold cross-validation estimates, and explain why an interval of CV error plus or "
                  "minus 1.96 fold standard errors undercovers."],
            "I": ["Keep every data-dependent step inside the cross-validation loop, and hold out a test set that is "
                  "used once.",
                  "Choose a classification threshold from the costs of the two errors rather than from accuracy."],
        },
        results=[
            ("Optimism", r"\mathbb{E}\bigl[\text{Err}_{\text{in}}-\overline{\text{err}}\bigr]=\frac{2}{n}\sum_{i=1}^{n}"
                         r"\operatorname{Cov}(\hat y_i,y_i)=\frac{2\sigma^2p}{n}\ \ (\text{least squares})"),
            ("Bias-variance", r"\mathbb{E}\bigl(Y_0-\hat f(x_0)\bigr)^2=\sigma^2+\bigl(\mathbb{E}\hat f(x_0)-f(x_0)\bigr)^2"
                              r"+\operatorname{Var}\hat f(x_0)"),
            ("k nearest neighbours", r"\hat f(x_0)=\frac1k\sum_{i\in N_k(x_0)}y_i,\qquad "
                                     r"\operatorname{Var}\bigl(\hat f(x_0)\mid x_1,\dots,x_n\bigr)=\frac{\sigma^2}{k}"),
            ("Cover-Hart", r"R^*\le R_{1\text{NN}}\le 2R^*(1-R^*)\quad\text{as }n\to\infty\ \text{(two classes)}"),
            ("Shrinkage, orthonormal design", r"\hat\beta^{\text{ridge}}_j=\frac{\hat\beta_j}{1+\lambda},\qquad "
                                              r"\hat\beta^{\text{lasso}}_j=\operatorname{sign}(\hat\beta_j)\bigl(|\hat\beta_j|-\lambda\bigr)_+"),
            ("Threshold from costs", r"\text{predict 1 when }\hat p>t^*=\frac{1}{1+c},\qquad "
                                     r"c=\frac{\text{cost of a miss}}{\text{cost of a false alarm}}"),
        ],
        U=(0, 1, 3, 4, 6, 8), I=(9, 10),
        also=(("statkit.learn", "explainer/stats/kit/learn.py"),),
    ),
    Part(
        n=20, level="U", widget="saltrecall", prereq=(12, 16, 18, 19),
        question="What does a complete, honest statistical analysis look like, from the question to the report?",
        story="The question is how blood pressure depends on salt. Trials find 2 to 3 mm Hg of systolic pressure per "
              "gram of sodium; in NHANES 2017-2018 the crude slope is -0.14. The part introduces no new method and "
              "takes the question through every stage: the estimand, the survey's design and weights, a cleaning "
              "log that runs from 5,533 adults to 3,071, exploration, and a model written down before the results "
              "are seen. The weighted regression gives +0.07 mm Hg per gram with an interval from -0.50 to +0.63 on "
              "15 degrees of freedom. Checks, four standard errors and a specification curve of 64 analyses do not "
              "move it; what matters is that one day's recall is a noisy measure of usual intake. The same code "
              "then runs on the World, where the effect is 1.5: the one-day recall averages 0.23 and covers the "
              "truth 0% of the time, and a randomized trial of 400 recovers it. The part ends with a one-page "
              "report, a reproducible pipeline, six problems across Stages I and II, and the BSc.",
        handoff="The master's stage begins with how estimators are computed (Part 21) and the linear model in depth "
                "(Part 23); causal questions from observational data are Parts 35 to 37, measurement error and "
                "missing data Part 41, and inference after selection Part 56.",
        outside="Stages I and II of this series; this part is their capstone.",
        objectives={
            "U": ["State an estimand: the population, the outcome, the exposure, the contrast and what is held fixed.",
                  "Read a coefficient with its design-based interval, and say what it does and does not show about "
                  "cause."],
            "M": ["Fit a survey-weighted regression with linearized standard errors and the design's degrees of "
                  "freedom.",
                  "Compute the attenuation of a slope from the reliability of its exposure, and correct it by "
                  "regression calibration."],
            "D": ["Explain why a regression on the true exposure can still miss a structural effect when diagnosis "
                  "changes the exposure and the treatment, and name the design that identifies it."],
            "I": ["Keep a decision log of every cleaning step, with its reason and its count.",
                  "Write a one-page report whose every number can be rebuilt from raw data, code and seeds.",
                  "Run a specification curve and report the choices that move the answer."],
        },
        results=[
            ("Design effect", r"\text{deff}=\frac{\operatorname{Var}_{\text{design}}(\hat\theta)}{\operatorname{Var}_{\text{SRS}}(\hat\theta)},"
                              r"\qquad n_{\text{eff}}=\frac{n}{\text{deff}}"),
            ("Design-based interval", r"\hat\beta\pm t_{d,\,0.975}\,\widehat{\text{se}}(\hat\beta),\qquad "
                                      r"d=\#\text{PSUs}-\#\text{strata}=30-15"),
            ("Attenuation (mean of k days)", r"\bar W_k=X+\bar U_k:\qquad \hat\beta_{W}\to\lambda_k\beta,\qquad "
                                             r"\lambda_k=\frac{\operatorname{Var}X}{\operatorname{Var}X+\operatorname{Var}U/k}"),
            ("Regression calibration", r"\text{replace }W_1\text{ by }\hat{\mathbb{E}}[X\mid W_1,Z]=\hat{\mathbb{E}}[W_2\mid W_1,Z]"),
            ("Sizing a two-arm trial", r"n\text{ per arm}=\frac{2\,(z_{1-\alpha/2}+z_{1-\beta})^2\,\sigma^2}{\Delta^2}"),
            ("Sixty-four forks", r"1-0.95^{64}\approx 0.96\ \text{if independent};\qquad "
                                 r"\text{Bonferroni tests each at }0.05/64"),
        ],
        U=(0, 1, 4, 5, 9, 13), I=(3, 11, 12),
        also=(("The capstone pipeline", "videos/stats/stats20/pipeline.py"),
              ("statkit.capstone", "explainer/stats/kit/capstone.py")),
    ),
]
