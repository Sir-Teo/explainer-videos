"""Act V, Portfolios, Strategies and the Firm: Parts 30-34."""

from videos.quant.course import Part

PARTS = [
    Part(
        n=30, level="U", widget="shrink", prereq=(23, 25),
        question="The optimizer promises the best portfolio. Why does the one it builds from data do worse "
                 "than splitting your money equally?",
        story="Mean-variance optimization takes estimates as truth and puts the most weight where the "
              "estimates are most wrong: it maximizes error. With as many assets as observations the sample "
              "covariance matrix is nearly singular and the optimizer reports almost no risk at all. The part "
              "measures the promise against the delivery, then repairs the inputs: shrinkage of the "
              "covariance (Ledoit and Wolf), constraints that act as shrinkage, Black-Litterman's blend of "
              "views with the market, risk parity and hierarchical methods that avoid inverting the matrix. "
              "Kelly returns as the growth-optimal portfolio, and a network is trained to go from features to "
              "weights in one step.",
        handoff="The portfolio needs a risk model and a cost model before it can trade: Part 31.",
        outside="Parts 23 and 25; linear algebra (eigenvalues).",
        objectives={
            "U": ["Explain why an optimizer amplifies estimation error and why 1/N is hard to beat.",
                  "Compute a minimum-variance portfolio of a few assets."],
            "M": ["Shrink a covariance matrix and show the effect on out-of-sample risk; clean eigenvalues "
                  "with the Marchenko-Pastur edge.",
                  "Build Black-Litterman, risk-parity, hierarchical-risk-parity and minimum-CVaR portfolios."],
            "D": ["Derive the exact in- and out-of-sample variance of the sample minimum-variance portfolio "
                  "for Gaussian returns, and its limit as K/T tends to a constant."],
            "I": ["Specify an optimizer for production: constraints, turnover control, and how its output is "
                  "evaluated."],
        },
        results=[
            ("Minimum variance", r"w=\frac{\Sigma^{-1}\mathbf 1}{\mathbf 1'\Sigma^{-1}\mathbf 1}"),
            ("Promise and delivery", r"\frac{\mathbb E[\hat\sigma^2_{\text{in}}]}{\sigma^2_{\min}}\to1-\frac KT,\qquad"
                                     r"\frac{\mathbb E[\sigma^2_{\text{out}}]}{\sigma^2_{\min}}\to\frac{1}{1-K/T}"),
            ("Linear shrinkage", r"\hat\Sigma_{\text{LW}}=\delta\,\bar\sigma^2 I+(1-\delta)\,S"),
            ("Black-Litterman", r"\mu_{\text{BL}}=\bigl[(\tau\Sigma)^{-1}+P'\Omega^{-1}P\bigr]^{-1}\bigl[(\tau\Sigma)^{-1}\pi+P'\Omega^{-1}q\bigr]"),
        ],
        U=(1, 2), I=(12, 13), D=(9, 11),
    ),
    Part(
        n=31, level="M", widget="law", prereq=(24, 30),
        question="A backtest shows a Sharpe ratio of 3.9 before costs and 1.6 after. Which number is the "
                 "strategy?",
        story="Between a forecast and a profit sit a risk model, a cost model and time. The fundamental law "
              "says skill times the square root of breadth, and the part shows how quickly that overstates "
              "things once the information coefficient varies. A factor risk model splits a portfolio's "
              "variance into what is shared and what is specific. Costs grow like the square root of size, "
              "which gives every strategy a capacity. With costs, the optimal portfolio moves only part of "
              "the way toward its target each day (Garleanu and Pedersen). August 2007, when crowded "
              "long-short books were unwound together, is the crisis file.",
        handoff="Costs are derived from the order book in Parts 36-37; crowding returns as fire sales in "
                "Part 41.",
        outside="Parts 24 and 30.",
        objectives={
            "U": ["State the fundamental law of active management and compute an information ratio from an IC "
                  "and a breadth.",
                  "Explain why trading costs grow with size and what capacity means."],
            "M": ["Estimate a cross-sectional factor risk model and decompose a portfolio's risk and P&L.",
                  "Apply the square-root impact law; solve for the partial-adjustment trading rule under "
                  "quadratic costs; combine alphas."],
            "D": ["Derive the information ratio when the IC is random (Qian and Hua; Ding) and its limit "
                  "E[IC]/sd(IC); solve Garleanu-Pedersen's dynamic problem."],
            "I": ["Read a P&L attribution, and explain what crowding did in August 2007."],
        },
        results=[
            ("Fundamental law", r"\mathrm{IR}=\mathrm{TC}\cdot\mathrm{IC}\cdot\sqrt{\mathrm{BR}}"),
            ("When the IC varies", r"\mathrm{IR}=\frac{\mathbb E[\mathrm{IC}]}{\sqrt{\sigma^2_{\mathrm{IC}}+(1-\mathbb E[\mathrm{IC}]^2)/N}}"),
            ("Factor risk model", r"\Sigma=XFX'+D"),
            ("Square-root impact", r"\frac{\Delta P}{P}\approx Y\,\sigma\sqrt{\frac{Q}{\mathrm{ADV}}}"),
        ],
        U=(1, 4), I=(9, 10, 11, 12), D=(5,),
    ),
    Part(
        n=32, level="U", widget="trend", prereq=(7, 24),
        question="Trend followers made money in 2008 and again in 2022 while almost everything else lost. Is "
                 "that insurance, a premium, or luck?",
        story="A trend rule buys what has risen and sells what has fallen, across dozens of futures markets. "
              "Its returns plotted against the market's draw a smile: it does best in the largest moves either "
              "way, like an option bought with no premium. The part derives that shape exactly and shows the "
              "small losses that pay for it. Volatility targeting, risk parity and its dependence on the "
              "stock-bond correlation, value, momentum, carry and defensive premia across asset classes, and "
              "the strategies that sell insurance for a living follow, each with its payoff profile and its "
              "worst year.",
        handoff="Mean reversion, the mirror image of trend, is Part 33; what these books look like inside a "
                "firm is Part 34.",
        outside="Parts 7 and 24.",
        objectives={
            "U": ["Explain a time-series momentum rule and why its payoff is convex in the market's move.",
                  "Explain volatility targeting and risk parity."],
            "M": ["Build a diversified trend book with volatility-scaled positions and measure its skew and "
                  "its behaviour in crises.",
                  "Construct carry, value and defensive portfolios in several asset classes and compare their "
                  "tails."],
            "D": ["Prove the identity between a linear trend rule's P&L and realized variance minus its "
                  "expectation; derive its mean and skewness from the autocovariances."],
            "I": ["Explain how alternative risk premia are packaged, and what the stock-bond correlation did "
                  "to risk parity in 2022."],
        },
        results=[
            ("Trend identity", r"\sum_{t}\Bigl(\sum_{s<t}r_s\Bigr)r_t=\tfrac12\Bigl[\Bigl(\sum_t r_t\Bigr)^2-\sum_t r_t^2\Bigr]"),
            ("Expected trend profit", r"\mathbb E[P]=\sum_{k=1}^{n-1}(n-k)\,\gamma_k"),
            ("Volatility targeting", r"w_t=\frac{\sigma^\ast}{\hat\sigma_t}"),
            ("Skewness of the rule", r"\operatorname{skew}(P)=\frac{2^{3/2}(n-2)}{\sqrt{n(n-1)}}\ \to\ 2\sqrt2"),
        ],
        U=(1, 2), I=(9, 10), D=(),
    ),
    Part(
        n=33, level="M", widget="ou", prereq=(7, 31),
        question="Two prices are tied by an elastic band. When is trading the stretch a strategy, and when is "
                 "it a way to find out the band was never there?",
        story="Statistical arbitrage began in a bank's back office in the 1980s with pairs of similar stocks. "
              "The part rebuilds it in stages: pairs chosen by distance, the cointegration test and the "
              "screening problem it creates (test enough pairs and noise passes), the Ornstein-Uhlenbeck "
              "spread and its half-life, residuals from a factor model in place of pairs, and hedge ratios "
              "that drift, tracked with a Kalman filter. The research chapter answers the practical question: "
              "given a cost, how far should the spread stretch before you trade? Crowding and decay close the "
              "part.",
        handoff="The costs that set the band are measured in Parts 36-37; who provides the liquidity a "
                "stat-arb book consumes is Part 38.",
        outside="Parts 7 and 31.",
        objectives={
            "U": ["Explain a pairs trade and what could make the spread not come back."],
            "M": ["Test for cointegration and correct for the number of pairs screened; fit an "
                  "Ornstein-Uhlenbeck process and compute its half-life.",
                  "Build residual (eigenportfolio) signals and trade them with an s-score rule, net of costs."],
            "D": ["Derive the optimal entry band for an OU spread by renewal-reward and first-passage times, "
                  "and the small-cost law in which the band scales with the cube root of the cost."],
            "I": ["Explain capacity and crowding in stat arb, and how a desk decides a spread has broken."],
        },
        results=[
            ("Ornstein-Uhlenbeck", r"dX=\kappa(\theta-X)\,dt+\sigma\,dW,\qquad t_{1/2}=\frac{\ln2}{\kappa}"),
            ("s-score", r"s_t=\frac{X_t-\theta}{\sigma/\sqrt{2\kappa}}"),
            ("Profit rate of a band", r"R(m)=\frac{m-c}{\mathbb E_{m}[T_0]+\mathbb E_0[\tau_m]}"),
            ("Small-cost law", r"\frac{m^\ast}{s_{\text{eq}}}\sim\Bigl(\frac{3c}{s_{\text{eq}}}\Bigr)^{1/3}"),
        ],
        U=(2,), I=(1, 9, 10, 11), D=(8,),
    ),
    Part(
        n=34, level="U", widget="pods", prereq=(26, 31),
        question="How long does a portfolio manager's seat last, and what does the answer say about how quant "
                 "firms are built?",
        story="The industry part. Six ways to be a quant firm are laid out from the public record: the "
              "multi-manager platform, the single research engine, the market maker, the systematic asset "
              "manager, the bank desk, the proprietary shop. What they have disclosed about themselves is "
              "collected and read carefully. The pod model is examined as a mechanism: capital, a risk limit, "
              "a drawdown stop, a payout. The stop turns out to have an exact theory (how long a manager of a "
              "given skill survives), and the part derives it and asks what the stop actually selects for. "
              "Technology, surveillance, the interview and founding stories complete the picture.",
        handoff="The other side of these firms' trades is the subject of Act VI.",
        outside="Parts 26 and 31 for the research chapter; most chapters need nothing.",
        objectives={
            "U": ["Describe the main business models of quant firms and how each earns its money.",
                  "Explain how a pod is allocated capital and stopped."],
            "M": ["Compute the expected time to a drawdown stop for a given Sharpe ratio, and the P&L "
                  "distribution at the stop.",
                  "Model a platform of pods: netting, pass-through costs, the effect of correlation between "
                  "managers."],
            "D": ["Derive the law of the drawdown stopping time for Brownian motion with drift (Taylor; "
                  "Lehoczky) and the exponential law of the peak at the stop."],
            "I": ["Prepare for the interview: probability, market-making games, mental arithmetic, a research "
                  "discussion; read a regulatory case with its allegations labelled as such."],
        },
        results=[
            ("Expected time to the stop", r"\mathbb E[\tau_d]=\frac{\sigma^2}{2\mu^2}\Bigl(e^{2\mu d/\sigma^2}-1-\frac{2\mu d}{\sigma^2}\Bigr)"),
            ("In Sharpe units", r"\mathbb E[\tau]=\frac{e^{2S\delta}-1-2S\delta}{2S^2}\ \text{years}"),
            ("Peak at the stop", r"M_\tau\sim\operatorname{Exp},\qquad\mathbb E[M_\tau]=\frac{\sigma^2}{2\mu}\bigl(e^{2\mu d/\sigma^2}-1\bigr)"),
            ("Zero skill", r"\mathbb E[\tau_d]=\frac{d^2}{\sigma^2}"),
        ],
        U=(1, 3, 8), I=(2, 4, 5, 6, 7, 9, 11), D=(),
    ),
]
