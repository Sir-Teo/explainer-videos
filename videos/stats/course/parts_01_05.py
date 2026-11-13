"""Stage I, Bachelor's: Foundations (Parts 1-5)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=1, level="U", widget="lpcentre", prereq=(),
        question="What can you know about what you cannot see, from what you can?",
        story="In 1662 John Graunt reads London's Bills of Mortality and estimates what nobody had counted: the "
              "city's growth by migration, the surplus of boys, a table of how long Londoners lived. The part then "
              "builds the series' laboratory, the World, a simulated population of one million whose truth is "
              "known, and looks at samples from it before any probability. Histograms come first; the mean and "
              "the median turn out to be the minimizers of squared and absolute loss, and squares win because of "
              "Pythagoras. Quantiles, heavy tails, QQ plots and the Box-Cox family describe shape, and correlation "
              "is the cosine of an angle between centred vectors. Then the summaries fail: Anscombe's quartet and "
              "an annealed cloud share their statistics, the World's clinic reverses under aggregation, and a "
              "chart can lie by its axis. The part ends with twenty samples of a hundred heights whose averages "
              "all differ: every statistic is random.",
        handoff="The sampling distribution is the subject of Parts 6, 8 and 11; estimators as minimizers of a loss "
                "return in Parts 9 and 21; Pythagoras returns as least squares in Part 12 and ANOVA in Part 13; "
                "the ECDF becomes the bootstrap in Part 16; heavy tails return in the robust statistics of Part 30; "
                "Simpson's paradox is resolved in Part 36; the Coverage Board is filled by every part that makes "
                "a promise.",
        outside="School algebra and a first look at derivatives. Nothing from the series.",
        objectives={
            "U": ["Compute the mean, median, SD, MAD, IQR and five-number summary of a sample, and say which of "
                  "them one extreme value can move.",
                  "Read a histogram, a box plot and a QQ plot, and say what a bend in a QQ plot means.",
                  "Explain why two samples from the same population give different averages."],
            "M": ["Derive the mean and the median as minimizers of squared and absolute loss, and prove the "
                  "Pythagorean decomposition of a sum of squares.",
                  "Derive the Box-Cox family's limit at lambda = 0 and choose lambda by its profile "
                  "log-likelihood."],
            "D": ["State which moments a Pareto tail of exponent alpha has, and explain why the sample skewness "
                  "of the World's incomes cannot settle as n grows."],
            "I": ["Diagnose a misleading chart by its lie factor, its axis and its encoding, and redraw it "
                  "honestly.",
                  "Report group and aggregate rates together, and say which comparison the question needs when "
                  "they disagree."],
        },
        results=[
            ("Centres as minimizers", r"\bar x=\arg\min_c\sum_{i}(x_i-c)^2,\qquad "
                                      r"\operatorname{med}(x)\in\arg\min_c\sum_{i}|x_i-c|"),
            ("Pythagoras for sums of squares", r"\sum_{i}(x_i-c)^2=\sum_{i}(x_i-\bar x)^2+n(\bar x-c)^2"),
            ("Why a QQ plot is straight", r"X=\mu+\sigma Z\ \Longrightarrow\ Q_X(p)=\mu+\sigma\,Q_Z(p)"
                                          r"\quad\text{for every }p\in(0,1)"),
            ("Box-Cox family", r"x^{(\lambda)}=\frac{x^{\lambda}-1}{\lambda}\ \longrightarrow\ \log x"
                               r"\quad\text{as }\lambda\to 0"),
            ("Correlation as a cosine", r"r=\frac{\langle x-\bar x\mathbf 1,\ y-\bar y\mathbf 1\rangle}"
                                        r"{\lVert x-\bar x\mathbf 1\rVert\,\lVert y-\bar y\mathbf 1\rVert}"
                                        r"=\cos\theta,\qquad |r|\le 1"),
            ("Standard error of a mean", r"\operatorname{SD}(\bar X)=\frac{\sigma}{\sqrt n}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 14), I=(13,),
        also=(("The World", "explainer/stats/world.py"), ("The Museum", "explainer/stats/museum.py")),
    ),
    Part(
        n=2, level="U", widget="screenposterior", prereq=(1,),
        question="How do you reason exactly about what might happen?",
        story="In 1654 a game to three points is interrupted at two to one, and Pascal and Fermat divide the pot: "
              "Fermat completes the future and counts four equally likely continuations, Pascal averages backwards "
              "from the end, and expectation is born. Galileo's dice and de Mere's bets show how easily the wrong "
              "cases are called equally likely, and Bertrand's three random chords show that 'at random' means "
              "nothing until a measure is chosen. Kolmogorov's axioms make the measure the foundation. "
              "Conditioning renormalizes a slice, and Bayes' theorem in odds form turns a ninety percent "
              "sensitive screening test into a fifteen percent chance of having the condition. The transposed "
              "conditional then sends Sally Clark to prison, and Monty Hall shows that the host's protocol is "
              "part of the data. Random variables, expectation, variance, the St. Petersburg game and generating "
              "functions follow, and the part ends with the old argument about what a probability is.",
        handoff="Expectation and its linearity drive the laws of averages in Part 6 and estimation in Parts 9 and "
                "22; Bayes' theorem becomes Bayesian statistics in Parts 15 and 26 and the false discovery rate in "
                "Part 33; conditional independence returns in Part 5 and in the causal graphs of Part 36; "
                "generating functions name the distributions of Part 3; measure theory returns in Part 43.",
        outside="School algebra, and sums of series for the 1/e and coupon-collector limits.",
        objectives={
            "U": ["Compute a probability by counting equally likely cases, and say which cases are equally likely "
                  "and why.",
                  "Compute the chance of a condition given a positive test from the prevalence, sensitivity and "
                  "specificity, in natural frequencies and in odds form.",
                  "Compute expectations by linearity and indicators: matches in a shuffle, birthdays, the coupon "
                  "collector."],
            "M": ["Derive inclusion-exclusion and the union bound from the axioms, and the derangement "
                  "probability's limit 1/e.",
                  "Compute Monty Hall under each host protocol and explain why the likelihood depends on how the "
                  "evidence was produced."],
            "D": ["Prove that betting prices immune to a finite Dutch book are finitely additive, and state what "
                  "countable additivity needs beyond that.",
                  "Explain why the Cantor distribution is continuous yet has no density."],
            "I": ["Diagnose a transposed conditional in a report or a courtroom, and restate the evidence as a "
                  "likelihood ratio.",
                  "Check an exact answer against a seeded simulation and say how large a gap is noise."],
        },
        results=[
            ("The problem of points: A needs a points, B needs b (Pascal)", r"v(a,b)=\tfrac12\,v(a-1,b)+\tfrac12\,v(a,b-1),\quad v(0,b)=1,\ "
                                               r"v(a,0)=0,\qquad v(1,2)=\tfrac34"),
            ("Hat-check problem", r"P(\text{no match among }n)=\sum_{k=0}^{n}\frac{(-1)^k}{k!}"
                                  r"\ \longrightarrow\ \frac1e"),
            ("Bayes in odds form", r"\frac{P(A\mid B)}{P(A^c\mid B)}=\frac{P(A)}{P(A^c)}\cdot"
                                   r"\frac{P(B\mid A)}{P(B\mid A^c)}"),
            ("Linearity, with no independence", r"\mathbb E\Bigl[\sum_i X_i\Bigr]=\sum_i\mathbb E[X_i],"
                                                r"\qquad \mathbb E[T_{\text{coupons}}]=n\,H_n"),
            ("Variance", r"\operatorname{Var}X=\mathbb E[X^2]-(\mathbb E X)^2,\qquad "
                         r"\operatorname{Var}(X+Y)=\operatorname{Var}X+\operatorname{Var}Y"
                         r"\ \text{ if }X,Y\text{ are independent}"),
            ("Generating functions", r"G_X(s)=\mathbb E[s^X],\qquad G_{X+Y}(s)=G_X(s)\,G_Y(s)"
                                     r"\ \text{ for independent }X,Y,\qquad G_X'(1)=\mathbb E X"),
        ],
        U=(0, 1, 2, 3, 5, 6, 8, 9, 11, 12), I=(7,), D=(14,),
        also=(("The exact probability engine", "explainer/stats/prob.py"),),
    ),
    Part(
        n=3, level="U", widget="rareevents", prereq=(2,),
        question="Why do the same few shapes keep appearing?",
        story="Bortkiewicz's 200 corps-years of deaths by horse kick (109, 65, 22, 3, 1) follow Poisson's formula "
              "with mean 0.61. The part explains why, and assembles the family tree of distributions arrow by "
              "arrow. The binomial counts lattice paths; many rare chances make a Poisson, and Le Cam's inequality "
              "says how closely, even when the chances are unequal. The geometric and the exponential forget the "
              "past, sampling without replacement counts the fish in the World's lake, and the Poisson process "
              "produces the inspection paradox. The normal is derived three ways (de Moivre, Gauss, "
              "Herschel-Maxwell), and chi-squared, t and F arrive as statistics' own distributions, beside a "
              "lighthouse whose Cauchy beam has no mean. Order statistics count German tanks, power laws are "
              "fitted by likelihood rather than by a straight line, and mixtures and exponential families tie "
              "the relatives together before all 24 arrows of the tree are walked.",
        handoff="The normal and sums return in the laws of averages of Part 6 and the sampling theory of Part 8; "
                "chi-squared, t and F in every interval and test from Part 8 on; the tank problem in the "
                "estimation of Part 9; exponential families in Parts 9, 15, 22 and 24; the full limit proofs come "
                "in Parts 6 and 43.",
        outside="Calculus: series, the exponential limit, integration by substitution and polar coordinates.",
        objectives={
            "U": ["Compute binomial, Poisson, geometric, hypergeometric and exponential probabilities, and say "
                  "which story (trials, rare events, waiting, sampling without replacement) calls for which.",
                  "Explain the law of rare events and check a table of counts against a Poisson by its mean and "
                  "variance.",
                  "Explain memorylessness and the inspection paradox."],
            "M": ["Derive the Poisson limit of the binomial, the Gaussian integral, and the density of the k-th "
                  "order statistic.",
                  "Derive the gamma-Poisson and beta-binomial mixtures and their overdispersion from the law of "
                  "total variance.",
                  "Write a distribution in exponential-family form and read its mean and variance from A."],
            "D": ["State Le Cam's inequality for unequal success probabilities and say what it gives that the "
                  "pointwise limit does not.",
                  "State which arrows of the family tree are limits whose proofs need the tools of Parts 6 "
                  "and 43."],
            "I": ["Estimate a population size by capture-recapture, and explain why Chapman's version is "
                  "preferred to the Lincoln-Petersen ratio.",
                  "Fit a power-law exponent by maximum likelihood, and explain what goes wrong with least "
                  "squares on a log-log plot."],
        },
        results=[
            ("Law of rare events (Le Cam)", r"d_{\mathrm{TV}}\Bigl(\sum_{i=1}^n \operatorname{Bern}(p_i),\ "
                                            r"\operatorname{Poisson}\bigl(\textstyle\sum_i p_i\bigr)\Bigr)"
                                            r"\le\sum_{i=1}^n p_i^2\ \Bigl(=\tfrac{\lambda^2}{n}"
                                            r"\text{ when }p_i=\tfrac{\lambda}{n}\Bigr)"),
            ("Memorylessness", r"P(T>s+t\mid T>s)=P(T>t)\quad\text{for geometric and exponential }T"),
            ("The Gaussian integral", r"\int_{-\infty}^{\infty}e^{-x^2/2}\,dx=\sqrt{2\pi}"),
            ("Order statistics of n uniforms", r"U_{(k)}\sim\operatorname{Beta}(k,\ n-k+1),\qquad "
                                         r"\mathbb E\,U_{(k)}=\frac{k}{n+1}"),
            ("Mixtures overdisperse", r"X\mid\Lambda\sim\operatorname{Poisson}(\Lambda)\ \Longrightarrow\ "
                                      r"\operatorname{Var}X=\mathbb E\Lambda+\operatorname{Var}\Lambda"
                                      r"\ \ge\ \mathbb E X"),
            ("Exponential family", r"f(x\mid\eta)=h(x)\exp\{\eta\,T(x)-A(\eta)\},\qquad "
                                   r"A'(\eta)=\mathbb E\,T(X),\quad A''(\eta)=\operatorname{Var}T(X)"),
        ],
        U=(0, 1, 2, 3, 5, 6, 8, 9), I=(4, 10),
    ),
    Part(
        n=4, level="U", widget="hatdof", prereq=(),
        question="What matrix facts does statistics run on?",
        story="The part opens with the hat matrix of a line fitted to forty of the World's families. It is "
              "symmetric and idempotent, so its eigenvalues can only be zero and one: two ones, thirty-eight "
              "zeros, and a residual sum of squares that averages n minus p times the noise variance, not n. "
              "From that fact the toolkit is laid out. A sample is a vector and centring is a projection; the "
              "trace gives the expectation of any quadratic form; the spectral theorem draws the ellipses of a "
              "covariance matrix and the SVD gives the best low-rank approximation. Pseudoinverses, Schur "
              "complements, Woodbury, Kronecker products and matrix calculus follow, each checked numerically. "
              "Quadratic forms in projections of normal vectors are chi-squared, which is where t and F come "
              "from. The part ends in floating point: the condition number of X'X is the square of X's, so the "
              "normal equations lose the digits that QR keeps.",
        handoff="Projections and n minus p return in the sampling theory of Part 8, regression in Part 12 and "
                "ANOVA in Part 13; Schur complements give Part 5's conditional Gaussians and Part 25's mixed "
                "models; the SVD returns as principal components in Part 31; Cochran's theorem is used in Part 8; "
                "the linear model in full matrix generality is Part 23.",
        outside="A first course in linear algebra (vectors, matrices, rank, eigenvalues), or AI, Built Part 3.",
        objectives={
            "U": ["Compute a projection matrix, check that it is symmetric and idempotent, and read degrees of "
                  "freedom as its trace.",
                  "Explain why dividing a residual sum of squares by n underestimates the noise variance.",
                  "Read a covariance matrix as an ellipse: its axes are eigenvectors, its squared half-lengths "
                  "eigenvalues."],
            "M": ["Derive P = A(A'A)^-1 A', the expectation of a quadratic form, and the leave-one-out residual "
                  "e_i / (1 - h_ii).",
                  "Use the Schur complement and Woodbury to invert in blocks, and matrix calculus to derive "
                  "least squares and the Gaussian MLE of a covariance.",
                  "Prove that z'Pz is chi-squared with rank(P) degrees of freedom for standard normal z."],
            "D": ["Prove Eckart-Young for the Frobenius norm and state Cochran's theorem with its rank "
                  "condition."],
            "I": ["Solve least squares by QR after centring and scaling, and never by inverting X'X.",
                  "Diagnose a loss of digits from a condition number, and compute a variance in two passes."],
        },
        results=[
            ("The hat matrix", r"H=X(X^\top X)^{-1}X^\top,\quad H^2=H=H^\top\ \Longrightarrow\ "
                               r"\lambda_i(H)\in\{0,1\},\quad \operatorname{tr}H=p,\quad "
                               r"\mathbb E\,\mathrm{RSS}=(n-p)\sigma^2"),
            ("Expectation of a quadratic form", r"\mathbb E[x^\top A x]=\operatorname{tr}(A\Sigma)+\mu^\top A\mu"
                                                r"\quad\text{for }\mathbb E x=\mu,\ \operatorname{Var}x=\Sigma"),
            ("Eckart-Young", r"\min_{\operatorname{rank}B\le r}\lVert A-B\rVert_F="
                             r"\Bigl(\sum_{k>r}\sigma_k^2\Bigr)^{1/2},\quad\text{attained by the truncated SVD}"),
            ("Woodbury", r"(A+UCV)^{-1}=A^{-1}-A^{-1}U\,(C^{-1}+VA^{-1}U)^{-1}\,VA^{-1}"),
            ("Quadratic forms in normal vectors", r"z\sim N(0,I_n),\ P\text{ a projection of rank }r"
                                                  r"\ \Longrightarrow\ z^\top P z\sim\chi^2_r"),
            ("Conditioning", r"\kappa(X)=\frac{\sigma_{\max}(X)}{\sigma_{\min}(X)},\qquad "
                             r"\kappa(X^\top X)=\kappa(X)^2"),
        ],
        U=(0, 1, 2, 3, 4, 6), I=(12,),
        also=(("statkit.ols: least squares by QR", "explainer/stats/kit/ols.py"),),
    ),
    Part(
        n=5, level="U", widget="galtonslice", prereq=(3, 4),
        question="What does knowing one thing tell you about another?",
        story="In 1886 Francis Galton tabulates 928 adult children of 205 families against their mid-parents, "
              "smooths the counts and sees nested ellipses; the children's averages lie on a line of slope about "
              "two-thirds, which he calls regression towards mediocrity. The part reads a joint distribution "
              "three ways and builds a Gaussian slicer that cuts a density and renormalizes the slice. "
              "Uncorrelated is shown not to be independent. The conditional mean is proved to be the best "
              "predictor, a projection, and Eve's law splits variance into within and between. The multivariate "
              "normal is an affine image of independent normals, and its conditionals have linear means and "
              "Schur-complement variances: regression is born. Regression to the mean then turns out to be no "
              "force at all, since it runs backwards and leaves the population's spread unchanged. Three lines "
              "pass through one ellipse; copulas, Polya's urn, de Finetti's theorem, measures of dependence and "
              "the simplex close the part.",
        handoff="Conditional expectation is the backbone of regression in Part 12, causal inference in Parts "
                "35-37 and the martingales of Part 44; within and between returns as ANOVA in Part 13 and random "
                "effects in Part 25; Gaussian conditioning returns as the Kalman filter in Part 38 and kriging in "
                "Part 39; exchangeability as Bayes in Parts 15 and 26 and as conformal prediction in Part 34.",
        outside="Multivariable calculus (double integrals, Jacobians) and the matrix language of Part 4.",
        objectives={
            "U": ["Compute marginal and conditional distributions from a joint table, and say why a zero "
                  "correlation does not prove independence.",
                  "Compute the regression line from two means, two SDs and r, and predict how far an extreme "
                  "group will fall back on a second measurement.",
                  "Explain why regression to the mean is not a force, using the fact that it runs in both "
                  "directions."],
            "M": ["Prove that E[Y | X] minimizes mean squared error, and derive Eve's law from the tower "
                  "property.",
                  "Derive the conditional distribution of a multivariate normal by decorrelation, and read "
                  "conditional independence from a zero of the precision matrix.",
                  "Compute the density of a transformed vector with its Jacobian."],
            "D": ["State de Finetti's theorem for infinite exchangeable 0-1 sequences, and give the finite "
                  "urn that shows why the sequence must be infinite.",
                  "Explain what the L2 projection picture of E[Y | X] still needs to be rigorous (Part 44)."],
            "I": ["Diagnose regression to the mean in a before-and-after comparison of a group selected for "
                  "being extreme.",
                  "Choose a copula by its tail dependence, not only by its correlation, and say what the "
                  "Gaussian copula assumed in 2008."],
        },
        results=[
            ("Best predictor", r"\mathbb E\bigl[(Y-g(X))^2\bigr]\ \ge\ \mathbb E\bigl[(Y-\mathbb E[Y\mid X])^2\bigr]"
                               r"\quad\text{for every }g,\qquad \mathbb E\bigl[\mathbb E[Y\mid X]\bigr]=\mathbb E Y"),
            ("Eve's law", r"\operatorname{Var}Y=\mathbb E\bigl[\operatorname{Var}(Y\mid X)\bigr]"
                          r"+\operatorname{Var}\bigl(\mathbb E[Y\mid X]\bigr)"),
            ("Conditioning a Gaussian", r"X_1\mid X_2=x_2\ \sim\ N\bigl(\mu_1+\Sigma_{12}\Sigma_{22}^{-1}"
                                        r"(x_2-\mu_2),\ \ \Sigma_{11}-\Sigma_{12}\Sigma_{22}^{-1}\Sigma_{21}\bigr)"),
            ("Regression to the mean", r"\mathbb E[Y\mid X=x]=\mu_y+\rho\,\frac{\sigma_y}{\sigma_x}(x-\mu_x),"
                                       r"\qquad \operatorname{Var}(Y\mid X=x)=(1-\rho^2)\,\sigma_y^2"),
            ("Sklar's theorem", r"F(x,y)=C\bigl(F_X(x),\,F_Y(y)\bigr),\quad C\text{ a copula, unique when the "
                                r"margins are continuous}"),
            ("de Finetti, for an infinite exchangeable 0-1 sequence", r"P(X_1=x_1,\dots,X_n=x_n)=\int_0^1\theta^{s}(1-\theta)^{n-s}\,d\mu(\theta),"
                           r"\qquad s=\sum_{i} x_i"),
        ],
        U=(0, 1, 2, 3, 4, 7, 8), I=(11,), D=(12,),
        also=(("Galton's table and family notebook (the Museum)", "explainer/stats/museum.py"),),
    ),
]
