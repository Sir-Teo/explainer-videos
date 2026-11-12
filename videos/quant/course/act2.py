"""Act II, The Mathematical Toolkit (Parts 4-8)."""

from videos.quant.course import Part

PARTS = [
    Part(
        n=4, level="U", widget="measure", prereq=(1,),
        question="Can any betting system beat a fair game, and what exactly does 'fair' mean once you may stop "
                 "when you like?",
        story="The part builds the language of information (filtrations, conditional expectation as a "
              "projection) in order to state one theorem: a bounded strategy on a martingale is a martingale. "
              "Doubling seems to beat it and does not; Barings in 1995 is doubling with a bank's balance sheet. "
              "Then the idea that carries all of derivatives pricing: a change of measure re-weights the same "
              "paths so that a different process becomes the fair game. The last chapters turn the theorem "
              "around and use betting as a statistical test that can be checked at any time.",
        handoff="The change of measure prices every derivative from Part 9 on; testing by betting returns as the "
                "live monitor of Part 26.",
        outside="A first probability course. Measure theory is introduced as needed, not assumed.",
        objectives={
            "U": ["Explain why no betting system changes the expected value of a fair game, and where doubling "
                  "hides its loss.",
                  "Solve gambler's ruin for a fair and an unfair walk."],
            "M": ["Use conditional expectation, stopping times and the optional stopping theorem, and state "
                  "when it fails.",
                  "Change measure with a likelihood ratio and compute an expectation under either measure."],
            "D": ["Prove Doob's convergence theorem by upcrossings; state Radon-Nikodym and Kakutani's "
                  "dichotomy; derive the law of the iterated logarithm and a time-uniform boundary from "
                  "Ville's inequality."],
            "I": ["Recognize a doubling strategy in a trading record, and build an e-value monitor for a live "
                  "strategy."],
        },
        results=[
            ("Optional stopping", r"\mathbb E[M_\tau]=\mathbb E[M_0]\quad\text{for bounded }\tau"),
            ("Gambler's ruin", r"\mathbb P_a(\text{hit } b \text{ before } 0)=\frac{a}{b}\ \ (p=\tfrac12),\qquad"
                               r"\frac{1-(q/p)^a}{1-(q/p)^b}\ \ (p\ne\tfrac12)"),
            ("Change of measure", r"\mathbb E^{\mathbb Q}[X]=\mathbb E^{\mathbb P}\!\Bigl[\tfrac{d\mathbb Q}{d\mathbb P}X\Bigr]"),
            ("Ville's inequality", r"\mathbb P\bigl(\sup_t M_t\ge 1/\alpha\bigr)\le\alpha\quad(M\ge0,\ M_0=1)"),
        ],
        U=(3, 4, 7, 9), I=(8, 17), D=(10, 13, 14, 18),
    ),
    Part(
        n=5, level="M", widget="ito", prereq=(4,),
        question="Why does calculus need a new rule once the path is Brownian, and why does that rule make "
                 "hedging possible?",
        story="Brownian motion is built from coin flips until its roughness is visible: the squared increments "
              "do not vanish, they add up to elapsed time. That one fact is Ito's correction, and the part "
              "proves the lemma from it. With the lemma come stochastic differential equations and how to "
              "simulate them, the bridge from paths to PDEs (Feynman-Kac), Girsanov's theorem as re-weighted "
              "paths, and the martingale representation theorem, which is the reason a hedge exists at all. "
              "Jumps, self-exciting jumps and rough paths show where the Brownian picture ends.",
        handoff="Ito and Girsanov derive Black-Scholes in Part 10; Hawkes processes return in the order book "
                "(Part 36); fractional Brownian motion returns as rough volatility (Part 14).",
        outside="Multivariable calculus and Part 4's martingales.",
        objectives={
            "U": ["Explain quadratic variation with a picture, and why dW squared behaves like dt.",
                  "Apply Ito's lemma to a function of geometric Brownian motion."],
            "M": ["Solve and simulate the standard SDEs (GBM, Ornstein-Uhlenbeck, CIR), and state the strong "
                  "orders of Euler and Milstein.",
                  "Move between an SDE, its Fokker-Planck equation and a Feynman-Kac expectation, and change "
                  "drift with Girsanov."],
            "D": ["Prove the central limit theorem for realized variance and state what jumps and noise do to "
                  "it; define local time, fractional Brownian motion and the signature of a path."],
            "I": ["Choose a discretization and a variance budget for a production simulator, and test it "
                  "against an exact case."],
        },
        results=[
            ("Quadratic variation", r"\sum_i (W_{t_{i+1}}-W_{t_i})^2\;\longrightarrow\;T"),
            ("Ito's lemma", r"df=\Bigl(f_t+\mu f_x+\tfrac12\sigma^2 f_{xx}\Bigr)dt+\sigma f_x\,dW"),
            ("Girsanov", r"\frac{d\mathbb Q}{d\mathbb P}=\exp\Bigl(-\int_0^T\theta_s\,dW_s-\tfrac12\int_0^T\theta_s^2\,ds\Bigr)"),
            ("Feynman-Kac", r"u(t,x)=\mathbb E\bigl[e^{-\int_t^T r\,ds}\,g(X_T)\mid X_t=x\bigr]"),
        ],
        U=(1, 2, 4), I=(17,), D=(11, 15, 16, 18),
        also=(("Stochastic Calculus, Visualized (a gentler first pass)", "videos/math/stochastic/README.md"),),
    ),
    Part(
        n=6, level="U", widget="hac", prereq=(1,),
        question="One regression of returns on a predictor can be given five different verdicts. Which standard "
                 "error is the right one?",
        story="The same slope is judged with ordinary, Newey-West, clustered, Fama-MacBeth and bootstrap "
              "standard errors, and the verdicts disagree. The part works out why: returns are dependent across "
              "time and across firms, predictors are persistent, and tests are run by the hundred. Each remedy "
              "is derived and then checked on data it was built for. The second half is the toolkit proper: "
              "maximum likelihood, GMM, event studies, shrinkage, multiple testing, and the designs that "
              "separate cause from correlation.",
        handoff="Fama-MacBeth and GRS test the factor models of Part 24; multiple testing is the subject of "
                "Parts 25-26; shrinkage returns in portfolio construction (Part 30).",
        outside="Linear regression at the level of a first statistics course.",
        objectives={
            "U": ["Read a regression table and say what the standard error assumes.",
                  "Compute how many years of data a Sharpe ratio needs before it is distinguishable from zero."],
            "M": ["Choose and compute Newey-West, clustered and Fama-MacBeth standard errors, and a block "
                  "bootstrap.",
                  "Estimate by maximum likelihood and by GMM; correct for multiple tests with Bonferroni, Holm "
                  "and Benjamini-Hochberg."],
            "D": ["Derive the distribution of a predictive regression's slope when the predictor is local to a "
                  "unit root, and the size distortion that follows; set up double machine learning."],
            "I": ["Run a research review: what must be reported with a result before anyone allocates to it."],
        },
        results=[
            ("OLS", r"\hat\beta=(X'X)^{-1}X'y"),
            ("Newey-West", r"\hat S=\hat\Gamma_0+\sum_{j=1}^{L}\Bigl(1-\tfrac{j}{L+1}\Bigr)(\hat\Gamma_j+\hat\Gamma_j')"),
            ("Stambaugh bias", r"\mathbb E[\hat\beta-\beta]\approx-\frac{\sigma_{uv}}{\sigma_v^2}\,\frac{1+3\rho}{T}"),
            ("Years to significance", r"T\approx\Bigl(\frac{t}{\mathrm{SR}}\Bigr)^2"),
        ],
        U=(1, 6, 7, 10, 13, 16), I=(17,), D=(15, 18),
        also=(("Statistics, Built (the full statistics course)", "videos/stats/README.md"),),
    ),
    Part(
        n=7, level="U", widget="garch", prereq=(1, 6),
        question="Returns cannot be forecast. Can their volatility, and by how much does a neural network beat "
                 "a three-line model from 1986?",
        story="Under the noise of returns there is a slow river: volatility is persistent, mean-reverting and "
              "measurable. The part builds the forecasters in historical order (ARMA for the mean, GARCH and "
              "its asymmetric relatives for the variance, realized volatility from intraday data, HAR) and "
              "then trains recurrent and transformer networks on the same data. All of them are scored out of "
              "sample with a loss that cannot be gamed, and the race is shown as it was run, seeds and all.",
        handoff="The volatility forecaster feeds option trading (Part 11), risk measurement (Part 40) and "
                "volatility targeting (Part 32); roughness is taken up in Part 14.",
        outside="Part 6's regression and likelihood.",
        objectives={
            "U": ["Explain stationarity and volatility clustering, and fit a GARCH(1,1) to daily returns.",
                  "Compute realized volatility from intraday returns."],
            "M": ["Test for unit roots and cointegration; fit regime-switching and state-space models.",
                  "Score variance forecasts with QLIKE and compare them with Diebold-Mariano and the model "
                  "confidence set."],
            "D": ["Explain why Diebold-Mariano degenerates for nested models and derive the Clark-West "
                  "correction; weigh the evidence for rough volatility."],
            "I": ["Build a volatility forecast a desk would use: which inputs, which horizon, how it is "
                  "monitored."],
        },
        results=[
            ("GARCH(1,1)", r"\sigma_t^2=\omega+\alpha\,r_{t-1}^2+\beta\,\sigma_{t-1}^2"),
            ("Realized variance", r"\mathrm{RV}_t=\sum_{i=1}^{n} r_{t,i}^2\;\to\;\int_{t-1}^{t}\sigma_s^2\,ds"),
            ("HAR", r"\mathrm{RV}_{t+1}=\beta_0+\beta_d\mathrm{RV}_t+\beta_w\overline{\mathrm{RV}}^{(5)}_t"
                    r"+\beta_m\overline{\mathrm{RV}}^{(22)}_t+\varepsilon"),
            ("QLIKE", r"L(\hat\sigma^2,\sigma^2)=\frac{\sigma^2}{\hat\sigma^2}-\ln\frac{\sigma^2}{\hat\sigma^2}-1"),
        ],
        U=(1, 6, 9, 14), I=(16, 17, 18), D=(11, 15),
    ),
    Part(
        n=8, level="U", widget="kelly", prereq=(4, 5),
        question="You have an edge. How much of your wealth should you bet on it?",
        story="Too little wastes the edge and too much is ruin, and the curve between them has one peak: Kelly's "
              "fraction. The part reaches it from utility theory, then generalizes the question to choosing "
              "through time. Bellman's principle becomes the Hamilton-Jacobi-Bellman equation, Merton's "
              "portfolio problem is solved, transaction costs open a no-trade wedge, and optimal stopping gives "
              "the American option its exercise boundary. LTCM is the case of an edge sized without regard to "
              "the error in its own estimate. At the end a reinforcement-learning agent is trained on Merton's "
              "problem and compared with the closed form.",
        handoff="Control returns as hedging under costs (Parts 10-11), optimal execution (Part 37) and market "
                "making (Part 38); Kelly returns in portfolio construction (Part 30).",
        outside="Parts 4 and 5 for the continuous-time chapters; the Kelly chapters need only logarithms.",
        objectives={
            "U": ["Compute the Kelly fraction of a bet and the growth rate of any other fraction.",
                  "Explain risk aversion with a utility function and a certainty equivalent."],
            "M": ["Solve a finite dynamic program backwards; write and verify the HJB equation for Merton's "
                  "problem.",
                  "Characterize an optimal stopping problem by its Snell envelope and smooth fit."],
            "D": ["Quantify estimation risk in Merton's rule (the expected loss of the plug-in fraction); read "
                  "viscosity solutions, BSDEs and mean-field games as extensions of the same principle."],
            "I": ["Size a position under parameter uncertainty and a drawdown limit; say why practitioners use "
                  "a fraction of Kelly."],
        },
        results=[
            ("Kelly", r"f^\ast=\frac{\mu-r}{\sigma^2}\quad\text{(continuous)},\qquad f^\ast=p-\frac{1-p}{b}\quad\text{(binary)}"),
            ("Merton's fraction", r"\pi^\ast=\frac{\mu-r}{\gamma\,\sigma^2}"),
            ("HJB", r"0=\sup_{\pi}\Bigl\{V_t+\bigl(r+\pi(\mu-r)\bigr)wV_w+\tfrac12\pi^2\sigma^2w^2V_{ww}\Bigr\}"),
            ("Growth rate", r"g(f)=r+f(\mu-r)-\tfrac12 f^2\sigma^2"),
        ],
        U=(1, 2, 8, 9, 13), I=(17, 19), D=(4, 14, 15, 18),
    ),
]
