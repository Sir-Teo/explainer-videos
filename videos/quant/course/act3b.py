"""Act III, Derivatives (Q), second half: Parts 16-22."""

from videos.quant.course import Part

PARTS = [
    Part(
        n=16, level="M", widget="mc", prereq=(10, 13),
        question="The same price can be computed by simulation, by a grid, or by a Fourier integral. Which "
                 "machine, for which product, to what accuracy?",
        story="One option is priced by every method the industry uses, and each method's error is measured "
              "rather than assumed. Monte Carlo gives an answer with an error bar that shrinks like one over "
              "root n; variance reduction changes the constant, low-discrepancy sequences change the rate, and "
              "multilevel changes the cost. American options need regression (Longstaff-Schwartz) and a dual "
              "bound to know how wrong the regression is. Greeks are computed three ways and then by adjoint "
              "differentiation, which prices a thousand sensitivities for the cost of a few valuations. Finite "
              "differences and Fourier methods finish the race.",
        handoff="Adjoint differentiation is backpropagation: Part 17 trains networks with it. The engine prices "
                "every later product of the series.",
        outside="Parts 10 and 13; some numerical linear algebra helps.",
        objectives={
            "U": ["Price an option by Monte Carlo and report a confidence interval.",
                  "Explain why the error falls like one over the square root of the number of paths."],
            "M": ["Apply antithetic, control-variate and importance-sampling estimators; use Sobol points with "
                  "a Brownian bridge.",
                  "Price an American option by least-squares Monte Carlo; compute Greeks by bumping, pathwise "
                  "and likelihood-ratio methods and by AAD; solve the Black-Scholes PDE with a theta scheme; "
                  "price by the COS method."],
            "D": ["Derive the multilevel complexity theorem; the Andersen-Broadie dual bound; convergence of "
                  "least-squares Monte Carlo as paths and basis functions grow together."],
            "I": ["Design an overnight risk run: which method per product, GPU or CPU, and what is validated "
                  "against what."],
        },
        results=[
            ("Monte Carlo error", r"\hat\mu_n\pm1.96\,\frac{\hat\sigma}{\sqrt n}"),
            ("Control variate", r"\hat\mu_{cv}=\bar Y-b^\ast(\bar C-\mathbb E C),\qquad b^\ast=\frac{\operatorname{Cov}(Y,C)}{\operatorname{Var}C}"),
            ("Multilevel cost", r"\text{cost}(\varepsilon)=O\bigl(\varepsilon^{-2}(\log\varepsilon)^2\bigr)\ \text{against}\ O(\varepsilon^{-3})"),
            ("Theta scheme", r"\frac{V^{n+1}-V^{n}}{\Delta t}=\theta\,\mathcal L V^{n+1}+(1-\theta)\,\mathcal L V^{n}"),
        ],
        U=(1, 2), I=(17,), D=(7, 9, 14, 18, 19),
    ),
    Part(
        n=17, level="M", widget="band", prereq=(10, 16),
        question="Can a network learn to price and to hedge, and how would you know whether to trust it?",
        story="A frontier part, and every network in it is trained on screen. A network learns the "
              "Black-Scholes formula and then its Greeks; training on payoffs together with their pathwise "
              "derivatives (differential machine learning) gets there with far fewer samples. A neural "
              "calibrator learns the map from model parameters to a whole surface so that rough volatility "
              "can be calibrated in milliseconds. Deep BSDE solvers price in a hundred dimensions, and the deep "
              "hedger learns a strategy under transaction costs directly, with no model of the Greeks. Each "
              "result is checked against the classical benchmark at the same budget, and the last chapters are "
              "about model risk: where a learned hedger must not be allowed to trade.",
        handoff="The same tools return as learned executors (Part 37), learned risk (Part 40) and learning "
                "agents in markets (Part 42).",
        outside="Parts 10 and 16, and the idea of gradient descent (AI, Built, Part 4, has the full story).",
        objectives={
            "U": ["Explain what it means to train a network on simulated payoffs, and why a benchmark at equal "
                  "budget matters."],
            "M": ["Train a network to approximate a pricing function and its Greeks; explain differential "
                  "labels.",
                  "Set up deep hedging: the objective (a risk measure of the hedged P&L), the network's inputs, "
                  "the cost model; compare with delta hedging and the Whalley-Wilmott band."],
            "D": ["State the deep BSDE method and its a posteriori error bound (Han and Long); deep optimal "
                  "stopping; neural SDEs and signature-based market generators."],
            "I": ["Write a validation plan for a learned pricer or hedger: benchmarks, stress regions, "
                  "monitoring, fallbacks (in the spirit of supervisory model-risk guidance)."],
        },
        results=[
            ("Differential regression", r"\min_\theta\ \sum_i\bigl(f_\theta(x_i)-y_i\bigr)^2+\lambda\sum_i\bigl\|\nabla_xf_\theta(x_i)-\nabla_xy_i\bigr\|^2"),
            ("Deep hedging", r"\min_{\delta_\theta}\ \rho\Bigl(-Z+\sum_k\delta_\theta(I_k)\,(S_{k+1}-S_k)-c\sum_k|\delta_k-\delta_{k-1}|S_k\Bigr)"),
            ("Deep BSDE", r"Y_{t_{k+1}}=Y_{t_k}-f(t_k,X_{t_k},Y_{t_k},Z_{t_k})\Delta t+Z_{t_k}^\top\Delta W_k,\qquad\min\ \mathbb E\,|Y_T-g(X_T)|^2"),
            ("Entropic risk", r"\rho(X)=\frac1\gamma\ln\mathbb E\bigl[e^{-\gamma X}\bigr]"),
        ],
        U=(), I=(17, 19), D=(8, 9, 10, 15, 16, 18),
        also=(("AI, Built (autodiff, optimizers, diffusion, RL)", "videos/ai/README.md"),),
    ),
    Part(
        n=18, level="U", widget="curve", prereq=(2, 3),
        question="Government bonds are called safe, and in 2022 long ones fell further than stocks. What is a "
                 "bond's risk, and what moves the curve?",
        story="The part starts with money itself: reserves, the central bank's floor, quantitative easing and "
              "its reversal, the Taylor rule. Then the arithmetic every rates desk lives by: yields, forwards, "
              "bootstrapping a curve from par bonds, duration and convexity. Five decades of US curves are "
              "replayed and three motions explain almost all of them: level, slope and curvature. Swaps, "
              "Treasury futures and repo are the instruments; the expectations hypothesis and the term premium "
              "are the economics. The gilt crisis of September 2022 and Silicon Valley Bank in March 2023 are "
              "duration risk meeting leverage and deposits.",
        handoff="The curve becomes a stochastic object in Part 19; duration plus leverage plus margin calls is "
                "the spiral of Part 41.",
        outside="Compound interest; Part 3's discounting.",
        objectives={
            "U": ["Compute a bond's price, yield, duration and convexity, and estimate its price change for a "
                  "given move in yield.",
                  "Bootstrap zero rates from par yields and compute forward rates."],
            "M": ["Fit a Nelson-Siegel-Svensson curve; hedge with key-rate durations; extract level, slope and "
                  "curvature by principal components.",
                  "Price a swap, find a Treasury future's cheapest-to-deliver, and separate expected short "
                  "rates from the term premium."],
            "D": ["Explain why the curve's principal components look like level, slope and curvature: total "
                  "positivity and the Gantmacher-Krein oscillation theorem."],
            "I": ["Explain the liability-driven-investment spiral of 2022 and the run on Silicon Valley Bank in "
                  "terms of duration, leverage and funding."],
        },
        results=[
            ("Price and yield", r"P=\sum_{i}\frac{c_i}{(1+y/m)^{m t_i}}"),
            ("Duration and convexity", r"\frac{\Delta P}{P}\approx-D_{\text{mod}}\,\Delta y+\tfrac12\,C\,(\Delta y)^2"),
            ("Forward rate", r"f(t_1,t_2)=\frac{z_2t_2-z_1t_1}{t_2-t_1}"),
            ("Nelson-Siegel", r"y(\tau)=\beta_0+\beta_1\frac{1-e^{-\tau/\lambda}}{\tau/\lambda}+\beta_2\Bigl(\frac{1-e^{-\tau/\lambda}}{\tau/\lambda}-e^{-\tau/\lambda}\Bigr)"),
        ],
        U=(1, 2, 3, 4, 5, 6, 9), I=(16, 17, 18, 19), D=(),
        also=(("Opposing Forces: Earnings vs. the Cost of Money", "videos/markets/opposing_forces/README.md"),),
    ),
    Part(
        n=19, level="M", widget="vasicek", prereq=(5, 18),
        question="How do you price an option on an interest rate when the thing you discount with is the "
                 "thing that is random?",
        story="In 1994 the Federal Reserve raised rates and bond portfolios built on a static curve lost "
              "billions. A model of the curve's motion is needed. The part goes up the ladder: short-rate "
              "models (Vasicek, Cox-Ingersoll-Ross) whose bond prices are exponential-affine, Hull-White "
              "fitted to today's curve, and Heath-Jarrow-Morton, where no arbitrage fixes the drift of every "
              "forward rate. Caps and swaptions are priced by changing numeraire; negative rates forced the "
              "market back to Bachelier's normal model. Bermudan swaptions, the multi-curve world after 2008, "
              "bond risk premia and the negative convexity of mortgages complete the desk.",
        handoff="The same intensity mathematics prices default in Part 20; swap exposures drive XVA in "
                "Part 21.",
        outside="Parts 5 and 18.",
        objectives={
            "U": ["Explain why a model of the whole curve is needed to price an interest-rate option."],
            "M": ["Price zero-coupon bonds under Vasicek, CIR and Hull-White, and calibrate Hull-White to a "
                  "curve.",
                  "Price caps, floors and swaptions with Black's and Bachelier's formulas under the right "
                  "measure; explain the SABR smile for rates and the multi-curve framework."],
            "D": ["Derive the HJM drift condition; set up the LIBOR and SOFR market models; price Bermudan "
                  "swaptions by regression; treat the zero lower bound with a shadow rate."],
            "I": ["Explain mortgage prepayment and negative convexity, and what convexity hedging does to the "
                  "rates market."],
        },
        results=[
            ("Vasicek", r"dr=a(b-r)\,dt+\sigma\,dW,\qquad P(0,T)=e^{A(T)-B(T)r_0},\quad B(T)=\frac{1-e^{-aT}}{a}"),
            ("HJM drift", r"\alpha(t,T)=\sigma(t,T)\int_t^T\sigma(t,u)\,du"),
            ("Bachelier", r"C=A\Bigl[(F-K)\,N(d)+\sigma_n\sqrt T\,\varphi(d)\Bigr],\qquad d=\frac{F-K}{\sigma_n\sqrt T}"),
            ("Swap rate", r"S_{0}=\frac{P(0,T_0)-P(0,T_n)}{\sum_{i=1}^{n}\delta_i\,P(0,T_i)}"),
        ],
        U=(), I=(13,), D=(4, 8, 9),
    ),
    Part(
        n=20, level="U", widget="pool", prereq=(3, 10),
        question="What is a promise to pay worth, and why did so many promises fail together in 2008?",
        story="A credit spread is compensation for default and for the fear of it. Merton's model reads debt as "
              "the firm's assets minus a call option, which turns equity prices into default probabilities. "
              "Reduced-form models treat default as the first tick of a random clock and price the credit "
              "default swap. Then the statistics of who defaults (Altman's Z, logistic regression, trees) and "
              "the question that sank a system: how correlated are defaults? One number, the correlation in a "
              "Gaussian copula, decides whether the senior tranche of a pool is safe. In 2007-08 it was not. "
              "The London Whale, corporate bonds in March 2020 and the marks of private credit are the later "
              "files.",
        handoff="Default probabilities price counterparty risk in Part 21; correlated losses and fire sales "
                "return in Part 41.",
        outside="Parts 3 and 10. The statistical chapters need Part 6.",
        objectives={
            "U": ["Explain what a credit spread compensates for, and compute an implied default probability "
                  "from a spread and a recovery rate.",
                  "Describe a credit default swap and a tranche in words and in cash flows."],
            "M": ["Compute distance to default in Merton's model; bootstrap hazard rates from CDS spreads; fit "
                  "and evaluate a default classifier.",
                  "Derive Vasicek's large-pool loss distribution and price a tranche in the Gaussian copula."],
            "D": ["Derive the granularity adjustment for name concentration and compare it with Monte Carlo."],
            "I": ["Explain how the Basel capital formula uses the one-factor model, and what correlation "
                  "assumptions did to senior tranches in 2007-08."],
        },
        results=[
            ("Credit triangle", r"s\approx\lambda\,(1-R)"),
            ("Merton's distance to default", r"\mathrm{DD}=\frac{\ln(V/D)+(\mu-\tfrac12\sigma_V^2)T}{\sigma_V\sqrt T},\qquad \mathrm{PD}=N(-\mathrm{DD})"),
            ("Large-pool loss", r"\mathbb P(L\le x)=N\!\Bigl(\frac{\sqrt{1-\rho}\,N^{-1}(x)-N^{-1}(p)}{\sqrt\rho}\Bigr)"),
            ("Survival", r"\mathbb Q(\tau>t)=\exp\Bigl(-\int_0^t\lambda_s\,ds\Bigr)"),
        ],
        U=(1, 2, 6, 8), I=(13, 14, 15, 16, 17), D=(),
    ),
    Part(
        n=21, level="M", widget="cva", prereq=(19, 20),
        question="Every derivative is also a loan to whoever owes you. What is that loan worth, and who should "
                 "stand in the middle?",
        story="After 2008 the price of a derivative acquired adjustments: for the counterparty's default (CVA), "
              "for one's own (DVA), for funding, capital and margin. The part computes them from the ground "
              "up. A swap's value is simulated forward, its positive part is the exposure, collateral removes "
              "all but what can happen during the days it takes to close out a defaulter, and what remains is "
              "priced against the counterparty's default curve. Wrong-way risk is exposure that grows as the "
              "counterparty weakens. Initial margin and central clearing move the risk rather than remove it: "
              "the nickel market in March 2022 and Archegos in March 2021 show where it went.",
        handoff="Margin that rises in stress is the procyclical engine of Part 41.",
        outside="Parts 19 and 20.",
        objectives={
            "U": ["Explain counterparty exposure, collateral and what a central counterparty does."],
            "M": ["Compute expected and potential future exposure by simulation, with and without collateral "
                  "and a margin period of risk.",
                  "Compute CVA and DVA from an exposure profile and a hazard curve; describe FVA, KVA, MVA and "
                  "initial-margin models."],
            "D": ["Bound wrong-way risk over all dependence structures by optimal transport; compute XVA "
                  "sensitivities by adjoint differentiation and regress future values with a network."],
            "I": ["Explain margin procyclicality, a clearing house's default waterfall, and what the Archegos "
                  "and nickel episodes revealed."],
        },
        results=[
            ("CVA", r"\mathrm{CVA}=(1-R)\int_0^T\mathrm{EE}(t)\,P(0,t)\,d\,\mathbb Q(\tau\le t)"),
            ("Expected exposure", r"\mathrm{EE}(t)=\mathbb E\bigl[\max(V_t-C_t,0)\bigr]"),
            ("Exposure under margin", r"V_t-C_t\approx V_t-V_{t-\text{MPoR}}"),
            ("FVA", r"\mathrm{FVA}=\int_0^T s_f(t)\,\bigl(\mathrm{EE}(t)+\mathrm{ENE}(t)\bigr)\,P(0,t)\,dt"),
        ],
        U=(10,), I=(11, 12, 13, 14), D=(6, 7),
    ),
    Part(
        n=22, level="U", widget="carry", prereq=(2, 18),
        question="Two currencies, two interest rates, one forward price. Why does the arbitrage that ties them "
                 "together stop working, and what is carry?",
        story="Covered interest parity pins the forward exchange rate to two interest rates; since 2008 it has "
              "failed by a measurable basis, which is the price of a bank's balance sheet. Uncovered parity "
              "fails the other way: high-yield currencies do not depreciate enough, and the carry trade earns "
              "the difference until it crashes. FX options come with two rates and four kinds of delta. In "
              "commodities the forward curve is financing plus storage minus the convenience of having the "
              "barrel; in April 2020 there was nowhere to put the barrel and the price went to minus 37 "
              "dollars. The Treasury basis trade and inflation breakevens complete the macro desk.",
        handoff="Carry is one of the alternative premia of Part 32; the basis trade is the leverage of "
                "Part 41; negative prices bring Bachelier back for the finale.",
        outside="Parts 2 and 18.",
        objectives={
            "U": ["Compute a forward exchange rate from two interest rates, and a commodity forward from "
                  "financing, storage and convenience yield.",
                  "Explain the carry trade and why its returns are negatively skewed."],
            "M": ["Measure the cross-currency basis; run the forward-premium regression.",
                  "Price FX options with Garman-Kohlhagen, convert between delta conventions, and build a "
                  "smile from risk reversals and butterflies."],
            "D": ["Solve the competitive storage model and derive backwardation at stock-outs."],
            "I": ["Explain the roll of commodity futures, the mechanics of negative oil in April 2020, and the "
                  "Treasury cash-futures basis trade."],
        },
        results=[
            ("Covered interest parity", r"F=S\,\frac{1+r_{d}\tau}{1+r_{f}\tau}"),
            ("Cost of carry", r"F=S\,e^{(r+u-y)T}"),
            ("Garman-Kohlhagen", r"C=S e^{-r_fT}N(d_1)-K e^{-r_dT}N(d_2)"),
            ("Fama regression", r"\Delta s_{t+1}=\alpha+\beta\,(f_t-s_t)+\varepsilon_{t+1},\qquad \hat\beta<1"),
        ],
        U=(1, 2, 3, 7), I=(10, 11, 13), D=(),
    ),
]
