"""Stage V, PhD: the research frontier, from selection to shift (Parts 56-60)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=56, level="D", widget="truncpivot", prereq=(33, 46, 52),
        question="How do you give honest uncertainty about a question chosen by looking at the data?",
        story="Ioannidis's 2008 paper on inflated associations opens the part, with the World's gene study: the "
              "twenty genes with the largest statistics out of 5,000 have estimated effects of 1.84 standard "
              "deviations against true effects of 1.23, and a replication lands at 1.22. The part states the "
              "problem (the winner's curse by the number of questions, conditional against simultaneous coverage, "
              "the false coverage rate) and then builds four families of answer, each with its price. PoSI covers "
              "every submodel at once with a constant between root 2 log p and root p. Conditional selective "
              "inference proves the polyhedral lemma, turns the lasso's selection event into a truncated normal "
              "in the selection window, and gives selective intervals on Stamey's prostate data, where they "
              "restore 95% coverage at about twice the length. Randomization, carving, data fission and thinning "
              "buy shorter intervals with added noise or split information. Knockoffs and conformal selection "
              "control an error rate over the selected set and give no intervals. The part ends with inference "
              "on winners for the prostate microarray's top gene, the test of clusters found in Old Faithful and "
              "Newcomb's data, and the open problems.",
        handoff="Conformal methods are taken to their limits in Part 57; e-values, which derandomize knockoffs, "
                "come in Part 58; the lasso when p and n grow together in Part 59; subgroups selected in causal "
                "analyses in Part 62; the dissertation's analysis plan in Part 65.",
        outside="Stages I to IV of the series: the multivariate normal and its conditionals, the lasso and its KKT "
                "conditions (Parts 32, 52), FDR control (Part 33), martingales and optional stopping (Part 44), "
                "and testing theory (Part 46).",
        objectives={
            "U": ["Explain the winner's curse on the gene study: why the top twenty estimates shrink on "
                  "replication although every one of the effects is real.",
                  "Compute the coverage of the usual 95% interval for the largest of K null estimates, "
                  "0.975^K - 0.025^K, and say what it is at K = 10 and K = 100."],
            "M": ["Compute a truncated-normal pivot and invert it into a selective interval for an estimate "
                  "reported because it crossed a threshold.",
                  "Split a normal observation by data fission, show the two pieces are independent, and "
                  "choose tau for a given budget of selection noise."],
            "D": ["Prove the polyhedral lemma and derive the lasso's selection polyhedron from its KKT conditions "
                  "at a fixed lambda.",
                  "Prove FDR control for knockoff+ by the supermartingale argument, stating the sign-flip "
                  "property it needs.",
                  "State what conditional, simultaneous and false-coverage-rate guarantees each promise, and "
                  "why conditional and simultaneous coverage do not imply one another."],
            "I": ["Diagnose selection in an analysis (stepwise P-values, OLS after the lasso, tests of clusters "
                  "found in the same data) and choose a correction: splitting, fission, a selective interval "
                  "or a simultaneous one.",
                  "Report a selected finding with the selection rule, an interval valid after it, and no "
                  "interval where the method (knockoffs, conformal selection) controls only an error rate."],
        },
        results=[
            ("The winner's curse", r"\operatorname{E}\max_{k\le K}Z_k\le\sqrt{2\log K},\qquad "
                                   r"P\bigl(|\max_k Z_k|\le z_{0.975}\bigr)=0.975^K-0.025^K"
                                   r"\quad (Z_k\ \text{iid}\ N(0,1))"),
            ("The polyhedral lemma",
             r"\{AY\le b\}=\{\mathcal V^-(Z)\le\eta^\top Y\le\mathcal V^+(Z),\ \mathcal V^0(Z)\ge 0\},\qquad "
             r"c=\frac{\Sigma\eta}{\eta^\top\Sigma\eta},\ Z=Y-c\,\eta^\top Y,\ "
             r"\mathcal V^-=\max_{j:(Ac)_j<0}\frac{b_j-(AZ)_j}{(Ac)_j},\ "
             r"\mathcal V^+=\min_{j:(Ac)_j>0}\frac{b_j-(AZ)_j}{(Ac)_j}"),
            ("The truncated-normal pivot",
             r"\frac{\Phi\bigl(\tfrac{b-\mu}{\sigma}\bigr)-\Phi\bigl(\tfrac{y-\mu}{\sigma}\bigr)}"
             r"{\Phi\bigl(\tfrac{b-\mu}{\sigma}\bigr)-\Phi\bigl(\tfrac{a-\mu}{\sigma}\bigr)}"
             r"\ \sim\ \operatorname{Unif}(0,1)\quad\text{for } y=\eta^\top Y\ \text{given}\ "
             r"\eta^\top Y\in[a,b],\ \mu=\eta^\top\operatorname{E}Y,\ \sigma^2=\eta^\top\Sigma\eta"),
            ("The false coverage rate (Benjamini-Yekutieli)",
             r"\text{report the } R \text{ selected of } K \text{ independent estimates at level } "
             r"1-\frac{\alpha R}{K}\ \Longrightarrow\ \mathrm{FCR}\le\alpha"),
            ("Data fission", r"Z\sim N(0,\sigma^2)\ \text{independent of}\ X\sim N(\mu,\sigma^2):\quad "
                             r"X+\tau Z\sim N\bigl(\mu,(1+\tau^2)\sigma^2\bigr)\ \perp\ "
                             r"X-\frac{Z}{\tau}\sim N\bigl(\mu,(1+\tau^{-2})\sigma^2\bigr)"),
            ("Knockoff+", r"T=\min\Bigl\{t>0:\ \frac{1+\#\{j:W_j\le -t\}}{\max(1,\#\{j:W_j\ge t\})}\le q\Bigr\},"
                          r"\qquad \mathrm{FDR}\bigl(\{j:W_j\ge T\}\bigr)\le q"),
        ],
        U=(0, 1), I=(5, 9),
        also=(("statkit.selective", "explainer/stats/kit/selective.py"),),
    ),
    Part(
        n=57, level="D", widget="quantilelemma", prereq=(34, 46, 47),
        question="What can be guaranteed with no assumptions about the distribution, and what is impossible?",
        story="Bahadur and Savage's 1956 paper opens the part: over all distributions with a finite mean, no "
              "interval of bounded length covers the mean with probability bounded away from zero. A mixture of "
              "a standard normal with a rare value at 3 over epsilon has mean exactly 3, and at n = 50 it drives "
              "the 95% t-interval's coverage to 14%, while split conformal covers the next draw from the same "
              "mixture 95.8% of the time. The difference is the functional: the next observation is exchangeable "
              "with the ones in hand, so its rank is uniform. The rank strip proves the quantile lemma, coverage "
              "exactly k/(n + 1), with the Beta law of coverage given the calibration set; full conformal, split "
              "conformal and the jackknife+ follow, with the proof of 1 - 2 alpha. Then the part turns to what "
              "cannot be had: coverage conditional on x forces infinite length, and no distribution-free "
              "interval exists for a regression function. Between the two lie the relaxations: conditional "
              "guarantees over function classes, weighted and nonexchangeable conformal with a total-variation "
              "bound, adaptive conformal inference on a drifting series, conformal p-values for outliers on the "
              "Wisconsin biopsies, and risk control. It ends on NHANES blood pressures, where marginal "
              "calibration covers 78.3% of adults over seventy and group-conditional calibration 90.7%.",
        handoff="ACI's online-learning idea becomes anytime-valid testing with e-values in Part 58; conformal "
                "inference when p and n grow together is in Part 59; prediction intervals for individual causal "
                "effects in Part 62; uncertainty for foundation models in Part 64; the dissertation's predictive "
                "claims in Part 65.",
        outside="Stages I to IV of the series: Part 34's conformal methods as algorithms, order statistics and "
                "the Beta law, total variation, linear programming for quantile regression, and Part 46's "
                "testing theory.",
        objectives={
            "U": ["Explain with the mixture of the cold open why no sample of fifty can pin down a mean, and why "
                  "the median and the next observation are different.",
                  "Compute split conformal's threshold from n calibration scores, k = ceil((n + 1)(1 - alpha)), "
                  "and its exact coverage k/(n + 1)."],
            "M": ["Prove the quantile lemma from exchangeability, and derive the Beta(k, n + 1 - k) law of "
                  "coverage given the calibration set.",
                  "Derive the long-run coverage bound of adaptive conformal inference from its update rule."],
            "D": ["Prove the jackknife+ guarantee of 1 - 2 alpha by the tournament argument, and give the "
                  "unstable fit on which the plain jackknife fails.",
                  "State and prove the impossibility of distribution-free conditional coverage, and state the "
                  "guarantee of Gibbs, Cherian and Candes over a finite-dimensional function class with its slack.",
                  "State the nonexchangeable conformal bound and compute its total-variation term for a "
                  "changepoint."],
            "I": ["Check a deployed conformal method by group: report coverage in each subgroup, not only "
                  "overall, and recalibrate by Mondrian or group-conditional thresholds where it fails.",
                  "State with every conformal interval the sampling assumption it rests on (exchangeability, "
                  "a known shift, or none with an online update), the calibration size, and that the guarantee "
                  "is marginal."],
        },
        results=[
            ("Bahadur-Savage, on the mixture",
             r"P_\varepsilon=(1-\varepsilon)N(0,1)+\varepsilon\,\delta_{M/\varepsilon}:\quad "
             r"\operatorname{E}X=M,\qquad P(\text{t-interval covers } M)\le 1-(1-\varepsilon)^n+(1-\varepsilon)^n c_n(M)"),
            ("The quantile lemma",
             r"P\bigl(S_{n+1}\le S_{(k)}\bigr)=\frac{k}{n+1},\quad k=\lceil(n+1)(1-\alpha)\rceil\le n:"
             r"\qquad 1-\alpha\le\frac{k}{n+1}<1-\alpha+\frac{1}{n+1}"),
            ("Coverage given the calibration set",
             r"P\bigl(S_{n+1}\le S_{(k)}\mid S_1,\dots,S_n\bigr)=F(S_{(k)})\sim\operatorname{Beta}(k,\,n+1-k)"),
            ("Jackknife+", r"P\bigl(Y_{n+1}\in\hat C^{\,\mathrm{jack+}}_{\alpha}(X_{n+1})\bigr)\ge 1-2\alpha"),
            ("Nonexchangeable conformal",
             r"P\bigl(Y_{n+1}\in\hat C(X_{n+1})\bigr)\ge 1-\alpha-\sum_{i=1}^n\tilde w_i\,d_{\mathrm{TV}}(Z,Z^{i}),"
             r"\qquad \tilde w_i=\frac{w_i}{1+\sum_j w_j}"),
            ("Adaptive conformal inference",
             r"\alpha_{t+1}=\alpha_t+\gamma(\alpha-\mathrm{err}_t)\ \Longrightarrow\ "
             r"\Bigl|\frac1T\sum_{t=1}^T\mathrm{err}_t-\alpha\Bigr|\le\frac{\max(\alpha_1,1-\alpha_1)+\gamma}{\gamma T}"),
        ],
        U=(0, 1), I=(7, 9),
        also=(("statkit.dfree", "explainer/stats/kit/dfree.py"),),
    ),
    Part(
        n=58, level="D", widget="peekville", prereq=(35, 44, 46),
        question="What if you look at the data every day, and choose what to collect as you go?",
        story="At the Statistical Research Group at Columbia in 1943 a Navy officer complains that a test runs its "
              "full length long after the answer is clear, and Abraham Wald answers with the sequential "
              "probability ratio test. For a defective rate of 10% against 20% the SPRT, computed exactly on its "
              "lattice, needs 57 and 59 shells on average where the fixed test needs 109; the unplanned way to "
              "look early, a 5% z-test checked after every observation, rejects a true null 38% of the time "
              "within 100 looks. The part rebuilds testing so that looking is free. Group-sequential boundaries "
              "are placed in the Brownian picture; Ville's inequality, proved by optional stopping, turns any "
              "nonnegative martingale into a test valid at every look; betting gives e-values, calibrators and "
              "merging, universal inference handles composite nulls, and inverting the tests gives the "
              "confidence sequences of the confidence funnel. CAST's deaths are replayed as a betting test, "
              "e-BH controls the FDR under any dependence, and CUSUM finds the Nile's change. The part then "
              "turns to data collected adaptively: Thompson sampling and the Lai-Robbins bound, the bias of "
              "sample means after a bandit, adaptively weighted estimates, and off-policy evaluation, and it "
              "ends with five open problems.",
        handoff="The proportional regime follows in Part 59 and shift in Part 60; adaptive and sequential causal "
                "designs and dynamic treatment regimes are in Part 62, privacy budgets spent over time in Part 63, "
                "the evaluation of deployed AI systems in Part 64, and the dissertation's monitoring plan in "
                "Part 65.",
        outside="Stages I to IV of the series: likelihood ratios and Neyman-Pearson (Part 46), martingales, "
                "optional stopping and Brownian motion (Part 44), group-sequential trials as a recipe (Part 35), "
                "and Part 33's Benjamini-Hochberg procedure.",
        objectives={
            "U": ["Explain why checking a 5% test after every observation is not a 5% test, and read the "
                  "peeking curve.",
                  "Follow a bettor's wealth through the CAST deaths and say what a wealth of 20 licenses."],
            "M": ["Derive Wald's thresholds and error bounds for the SPRT, and compute its expected sample size "
                  "by Wald's identity.",
                  "Prove Ville's inequality by optional stopping and turn a likelihood-ratio martingale into an "
                  "anytime-valid p-value.",
                  "Derive Robbins's normal-mixture confidence sequence."],
            "D": ["Prove that e-BH controls the FDR under arbitrary dependence, and state why the average of "
                  "e-values is an e-value while the product needs sequential validity.",
                  "State the GROW criterion and the reverse information projection for a composite null, and "
                  "the cost of universal inference against the t-test.",
                  "State the Lai-Robbins lower bound and explain why sample means after adaptive allocation "
                  "are biased and not asymptotically normal without reweighting."],
            "I": ["Monitor an experiment that will be looked at daily with a confidence sequence or a "
                  "group-sequential boundary, and report an estimate corrected for the stop.",
                  "Set a CUSUM threshold from a target false-alarm run length and state the detection delay "
                  "it buys.",
                  "Record the assignment propensities of an adaptive experiment so that weighted and "
                  "off-policy estimates can be computed afterwards."],
        },
        results=[
            ("Wald's SPRT", r"\text{stop when } \Lambda_n\ge A=\frac{1-\beta}{\alpha}\ \text{or}\ "
                            r"\Lambda_n\le B=\frac{\beta}{1-\alpha}:\qquad "
                            r"\alpha'\le\frac{\alpha}{1-\beta},\quad \beta'\le\frac{\beta}{1-\alpha},\quad "
                            r"\alpha'+\beta'\le\alpha+\beta"),
            ("Wald's identity", r"\operatorname{E}S_N=\operatorname{E}N\cdot\operatorname{E}X_1"
                                r"\qquad (N \text{ a stopping time},\ \operatorname{E}N<\infty)"),
            ("Ville's inequality", r"M_t\ge 0 \text{ a supermartingale},\ M_0=1:\qquad "
                                   r"P\bigl(\exists\,t:\ M_t\ge 1/\alpha\bigr)\le\alpha"),
            ("e-values and calibrators", r"\operatorname{E}_{H_0}E\le 1\ \Rightarrow\ P_{H_0}(E\ge 1/\alpha)\le\alpha;"
                                         r"\qquad e=\kappa\,p^{\kappa-1}\ (0<\kappa<1)\ \text{is an e-value}"),
            ("Robbins's mixture confidence sequence",
             r"P\Bigl(\forall t:\ |\bar X_t-\mu|\le\sigma\,\frac{\sqrt{(1+t\tau^2)\bigl(\log(1+t\tau^2)+2\log(1/\alpha)\bigr)}}"
             r"{t\,\tau}\Bigr)\ge 1-\alpha"),
            ("e-BH", r"k^*=\max\Bigl\{k:\ e_{(k)}\ge\frac{m}{\alpha k}\Bigr\},\ \text{reject the } k^* "
                     r"\text{ largest}:\qquad \mathrm{FDR}\le\frac{m_0}{m}\,\alpha\ \text{ under any dependence}"),
        ],
        U=(0, 7), I=(2, 10, 11),
        also=(("statkit.sequential", "explainer/stats/kit/sequential.py"),),
    ),
    Part(
        n=59, level="D", widget="stateevolution", prereq=(32, 51, 52),
        question="What happens to classical statistics when p and n grow together?",
        story="Sur and Candes's 2019 logistic regression opens the part: with one variable for every five "
              "observations and signal strength 5, the maximum likelihood estimate is inflated by a factor of "
              "1.499, its spread is 4.74 where the textbook says 3.88, and twice the log likelihood ratio is "
              "1.487 times a chi-squared, so the usual 5% test rejects 8.6% of true nulls. The part derives what "
              "replaces the fixed-p theory when p/n tends to a constant. It starts with least squares and the "
              "Marchenko-Pastur law, solves the Sur-Candes system by root finding and quadrature, and finds the "
              "boundary beyond which the MLE does not exist. Stieltjes transforms and free convolution give the "
              "exact risk of ridge and of minimum-norm least squares, with double descent derived and simulated. "
              "M-estimation shows least absolute deviations losing to least squares at large p/n even for Laplace "
              "errors. Approximate message passing is tracked step by step by the state-evolution cobweb, which "
              "also yields the Donoho-Tanner curve; Gordon's comparison and the replica method reach the same "
              "equations by other routes, and random features show double descent in a two-layer network. The "
              "part ends with corrected inference, the rescaled likelihood-ratio test and the debiased MLE on the "
              "Wisconsin biopsies' design, and five open problems.",
        handoff="Robust estimation in high dimensions and distribution shift follow in Part 60; the sample "
                "complexity of optimal transport in Part 61; high-dimensional causal adjustment in Part 62; the "
                "theory of large models beyond the lazy regime in Part 64; the dissertation's simulation study in "
                "Part 65.",
        outside="Stages I to IV of the series: likelihood theory and Wilks's theorem (Part 22), ridge and the lasso "
                "(Part 32), random matrices and Gaussian comparison inequalities (Part 51), high-dimensional rates "
                "(Part 52), and complex analysis at the level of a contour and a branch of a square root.",
        objectives={
            "U": ["Explain the cold open's experiment: what goes wrong with a logistic regression's estimates and "
                  "tests when there is one variable for every five observations."],
            "M": ["Compute the limiting risk of least squares, ridge and minimum-norm least squares from the "
                  "Marchenko-Pastur Stieltjes transform, and explain the peak at p = n.",
                  "Run AMP for the lasso and its state evolution, and check one against the other iteration by "
                  "iteration."],
            "D": ["Derive the Marchenko-Pastur equation by leaving one column out, and the ridge risk of Dobriban "
                  "and Wager from it.",
                  "Derive state evolution for AMP, explain the Onsager term, and obtain the Donoho-Tanner curve "
                  "from the fixed-point condition.",
                  "State the convex Gaussian min-max theorem and recover the least-squares risk from its "
                  "auxiliary problem; state which replica predictions are proved and which are open."],
            "I": ["Diagnose when a fitted logistic regression is in the proportional regime (p/n not small, "
                  "estimates and z-statistics too large) and apply the rescaled test and debiased estimate, "
                  "with the signal strength estimated.",
                  "Choose a ridge penalty knowing that interpolation without one is worst near p = n."],
        },
        results=[
            ("Least squares when p/n tends to kappa < 1",
             r"\operatorname{E}\lVert\hat\beta-\beta\rVert^2\to\sigma^2\,\frac{\kappa}{1-\kappa}"
             r"\qquad (x_i\sim N(0,I_p),\ p/n\to\kappa)"),
            ("The Marchenko-Pastur law",
             r"f_\kappa(x)=\frac{\sqrt{(b-x)(x-a)}}{2\pi\kappa x}\ \text{ on } [a,b],\qquad "
             r"a,b=(1\mp\sqrt\kappa)^2\quad(\kappa\le 1)"),
            ("Ridgeless risk (Hastie, Montanari, Rosset and Tibshirani)",
             r"R(\gamma)=\sigma^2\frac{\gamma}{1-\gamma}\ (\gamma<1),\qquad "
             r"R(\gamma)=r^2\Bigl(1-\frac1\gamma\Bigr)+\frac{\sigma^2}{\gamma-1}\ (\gamma>1),"
             r"\qquad \gamma=p/n,\ r^2=\lVert\beta\rVert^2"),
            ("Optimal ridge (Dobriban and Wager)",
             r"\lambda^\star=\frac{\gamma\sigma^2}{r^2},\qquad R(\lambda^\star)=\sigma^2\gamma\,m(-\lambda^\star),"
             r"\quad m(z)=\int\frac{f_\gamma(x)}{x-z}\,dx"),
            ("AMP and state evolution",
             r"x^{t+1}=\eta\bigl(x^t+A^\top z^t;\theta\tau_t\bigr),\ "
             r"z^t=y-Ax^t+\tfrac1\delta z^{t-1}\bigl\langle\eta'\bigr\rangle;\qquad "
             r"\tau_{t+1}^2=\sigma^2+\frac1\delta\operatorname{E}\bigl[\eta(X+\tau_tZ;\theta\tau_t)-X\bigr]^2"),
            ("The rescaled likelihood-ratio test (Sur and Candes)",
             r"2\log\mathrm{LR}_j\ \xrightarrow{d}\ \frac{\kappa\,\sigma_\star^2}{\lambda_\star}\,\chi^2_1"
             r"\quad\text{under } \beta_j=0;\qquad \kappa=0.2,\ \gamma^2=5:\ \text{factor } 1.487"),
        ],
        U=(0,), I=(9,),
        also=(("statkit.amp", "explainer/stats/kit/amp.py"),),
    ),
    Part(
        n=60, level="D", widget="shiftweights", prereq=(30, 51, 57),
        question="What can be guaranteed when the data are corrupted, or the future differs from the past?",
        story="In 2019 Recht, Roelofs, Schmidt and Shankar rebuilt ImageNet's test set, and on their "
              "MatchedFrequency collection the evaluated classifiers lost eleven to fourteen points of accuracy: "
              "a test set samples one collection process, and deployment may use another. The first half of the "
              "part is about corrupted data. Tukey's depth finds the centre of a cloud whatever a minority of "
              "the points do, shown in the depth map on Old Faithful with thirty planted eruptions; in high "
              "dimensions the mean and the medians are pulled by a planted cluster by an amount that grows like "
              "root d, and the spectral filter, list decoding and median-of-means estimators are the computable "
              "answers. The second half is about shift. On an NHANES extract the unweighted source mean of "
              "blood pressure is 118.5 against a target of 126.2 and its interval never covers, while the "
              "weighted mean with a logistic density ratio covers 95% at an effective sample size of 268 out of "
              "600; on the breast cancer biopsies, black-box shift estimation recovers a target prevalence of "
              "0.70 that classify-and-count puts at 0.64. Distributionally robust optimization, invariant "
              "causal prediction and anchor regression, transfer learning and tests that detect shift follow, "
              "each with the scope of its guarantee stated, and the part ends with open problems.",
        handoff="Optimal transport, the geometry behind Wasserstein balls, is Part 61; Part 62 transports causal "
                "effects between populations; Part 63 relates robustness to privacy; Part 64 examines the "
                "behaviour of large models under shift; Part 65 revisits robustness in the dissertation.",
        outside="Stages I to IV of the series: Part 30's one-dimensional robust estimators and breakdown, "
                "concentration and random matrices (Part 51), convex duality, instrumental variables (Part 37), "
                "and Part 57's weighted conformal inference.",
        objectives={
            "U": ["Explain the ImageNetV2 result: what a test set measures, and why a new sample collected the "
                  "same way can score lower.",
                  "Compute the Tukey depth of a point in a small planar data set and say why the deepest point "
                  "resists a planted cluster that moves the mean."],
            "M": ["Estimate a density ratio with a classifier, form the importance-weighted mean, and compute "
                  "Kish's effective sample size.",
                  "Estimate target class proportions under label shift from a confusion matrix (BBSE), and say "
                  "when the matrix does not identify them.",
                  "Compute the chi-square robust risk of a loss sample and verify it against mean plus root of "
                  "2 rho times the variance."],
            "D": ["State the minimax rate of robust mean estimation under contamination, why coordinatewise "
                  "and geometric medians miss it by root d, and what a certified filter must control beyond "
                  "the top eigenvalue.",
                  "State the list-decoding guarantee when the clean points are a minority, and the "
                  "sub-Gaussian rate of median-of-means tournaments under two moments.",
                  "Derive the anchor regression estimator and its limits (OLS at gamma = 1, two-stage least "
                  "squares as gamma grows, when identified), and state what invariant causal prediction "
                  "guarantees."],
            "I": ["Diagnose a shift before correcting it: compare covariates with a two-sample test, report the "
                  "effective sample size of the weights, and refuse to extrapolate without overlap.",
                  "Report a transported estimate with the assumption that licenses it (covariate shift, label "
                  "shift, or a robustness ball) and an interval that includes the estimation of the weights."],
        },
        results=[
            ("Tukey depth", r"D(x;P)=\inf_{\lVert u\rVert=1}P\bigl(u^\top X\ge u^\top x\bigr),\qquad "
                            r"\text{Tukey median}=\arg\max_x D(x;P_n)"),
            ("A planted cluster in d dimensions",
             r"\text{coordinatewise median: } \lVert\hat\mu-\mu\rVert\approx\Phi^{-1}\Bigl(\frac{1}{2(1-\varepsilon)}\Bigr)\sqrt d"
             r"\approx 1.25\,\varepsilon\sqrt d;\qquad \text{minimax: } \varepsilon+\sqrt{d/n}"),
            ("Importance weighting", r"\operatorname{E}_P\bigl[w(X)f(X,Y)\bigr]=\operatorname{E}_Q f(X,Y),\quad "
                                     r"w=\frac{dQ_X}{dP_X};\qquad n_{\mathrm{eff}}=\frac{(\sum_i w_i)^2}{\sum_i w_i^2}"),
            ("Black-box shift estimation", r"Cw=\mu,\qquad C_{ij}=P_{\text{source}}(\hat y=i,\,y=j),\quad "
                                           r"\mu_i=P_{\text{target}}(\hat y=i),\quad w_j=\frac{q(j)}{p(j)}"),
            ("Chi-square DRO", r"\sup\Bigl\{\sum_i q_i\ell_i:\ \tfrac n2\sum_i\bigl(q_i-\tfrac1n\bigr)^2\le\rho\Bigr\}"
                               r"=\bar\ell+\sqrt{2\rho\operatorname{Var}_n(\ell)}"
                               r"\quad\text{while every } q_i\ge 0"),
            ("Anchor regression", r"\hat b_\gamma=\arg\min_b\ \lVert(I-P_A)(y-Xb)\rVert^2+\gamma\,\lVert P_A(y-Xb)\rVert^2"),
        ],
        U=(0, 1), I=(5, 6, 10),
        also=(("statkit.shift", "explainer/stats/kit/shift.py"),),
    ),
]
