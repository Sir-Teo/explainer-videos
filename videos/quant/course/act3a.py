"""Act III, Derivatives (Q), first half: Parts 9-15."""

from videos.quant.course import Part

PARTS = [
    Part(
        n=9, level="U", widget="tree", prereq=(2, 4),
        question="When two portfolios pay the same thing, they must cost the same. How much of finance follows "
                 "from that alone?",
        story="Put-call parity is assembled from a call, a put, a share and a bond, and then the places where it "
              "visibly fails are measured. The principle behind it is made exact: there is no arbitrage if and "
              "only if positive state prices exist, which is the same as a measure Q under which discounted "
              "prices are martingales. On a tree the option is replicated and the price folds back from "
              "expiry. When there are more states than assets, the price is no longer a number but an interval, "
              "found by a linear program. The density the market implies is read off butterflies.",
        handoff="Replication on the tree becomes Black-Scholes in the limit (Part 10); the implied density and "
                "its arbitrage conditions shape the volatility surface (Part 12).",
        outside="Linear algebra (solving a small linear system).",
        objectives={
            "U": ["Derive put-call parity and the forward price by building two portfolios with equal payoffs.",
                  "Price an option on a one-step and a multi-step binomial tree by replication."],
            "M": ["State and prove the fundamental theorem of asset pricing in one period; compute state "
                  "prices, the stochastic discount factor and Q.",
                  "Bound a price in an incomplete market by super-replication, and change numeraire."],
            "D": ["State the continuous-time theorem (no free lunch with vanishing risk), bubbles as strict "
                  "local martingales, Ross recovery and its critique, and martingale-optimal-transport bounds; "
                  "treat arbitrage under transaction costs through consistent price systems."],
            "I": ["Check a quoted option chain for static arbitrage, and explain why real arbitrage is limited "
                  "by funding and margin."],
        },
        results=[
            ("Put-call parity", r"C-P=S_0\,e^{-qT}-K\,e^{-rT}"),
            ("FTAP", r"\text{no arbitrage}\iff\exists\,\psi\gg0:\ D\psi=p\iff\exists\,\mathbb Q\sim\mathbb P"),
            ("Risk-neutral probability", r"q=\frac{e^{r\Delta t}-d}{u-d}"),
            ("Breeden-Litzenberger", r"\frac{\partial^2 C}{\partial K^2}=e^{-rT}\,f^{\mathbb Q}(K)"),
        ],
        U=(1, 2, 5, 6), I=(17,), D=(10, 14, 15, 16, 18),
    ),
    Part(
        n=10, level="U", widget="hedge", prereq=(5, 9),
        question="Can an option be manufactured from the stock and cash, and what does the manufacturer earn?",
        story="A real month of Bitcoin opens the part: a call sold and left alone loses a quarter of the "
              "notional, the same call hedged every hour makes a little. The hedge is the whole idea. Holding "
              "delta shares cancels the option's exposure to the stock, the drift drops out, and what is left "
              "is an equation whose solution is the Black-Scholes price, derived three ways: as a PDE, as an "
              "expectation under Q, and as the limit of the tree. The hedger's profit is taken apart term by "
              "term (gamma against theta, implied against realized), then stressed: the wrong volatility, "
              "hedging in steps, costs, jumps. October 1987 and LTCM are the two cases where the assumption "
              "that you can always trade was the one that failed.",
        handoff="Implied volatility, the formula turned inside out, becomes the surface of Part 12; the "
                "hedger's ledger becomes the option trader's daily explain in Part 11.",
        outside="Parts 5 and 9. The first seven chapters can be followed with calculus alone.",
        objectives={
            "U": ["Explain delta hedging and why the option's price does not depend on the stock's expected "
                  "return.",
                  "Price a European call and put with the Black-Scholes formula and read its Greeks."],
            "M": ["Derive the Black-Scholes PDE and solve it by the heat equation, by Feynman-Kac and by the "
                  "tree's limit.",
                  "Decompose a hedged option's P&L into gamma, theta and vega terms; account for discrete "
                  "hedging and for costs with Leland's volatility; price American exercise."],
            "D": ["Prove robustness of the hedge under a misspecified volatility (El Karoui, Jeanblanc and "
                  "Shreve), and the optimal rebalancing rule: variance of the error under time- and "
                  "move-based hedging and Fukasawa's lower bound."],
            "I": ["Quote and compare options in implied volatility; explain what portfolio insurance did in "
                  "1987 and what LTCM's short-volatility book assumed."],
        },
        results=[
            ("Black-Scholes PDE", r"V_t+\tfrac12\sigma^2S^2V_{SS}+rSV_S-rV=0"),
            ("The formula", r"C=S\,N(d_1)-K e^{-rT}N(d_2),\qquad d_{1,2}=\frac{\ln(S/K)+(r\pm\tfrac12\sigma^2)T}{\sigma\sqrt T}"),
            ("The hedger's P&L", r"d\Pi=\tfrac12\,\Gamma S^2\bigl(\sigma_{\text{implied}}^2-\sigma_{\text{realized}}^2\bigr)dt"),
            ("Theta and gamma", r"\Theta=-\tfrac12\sigma^2S^2\Gamma\quad(r=0)"),
        ],
        U=(1, 2, 5, 6, 7, 11, 12), I=(15, 16, 17, 18), D=(19,),
        also=(("Stochastic Calculus, Visualized (a gentler first pass)", "videos/math/stochastic/README.md"),),
    ),
    Part(
        n=11, level="U", widget="gamma", prereq=(10,),
        question="An option position earns from movement and pays for time. How is that trade actually run?",
        story="This is the practitioner's part. A book of options is reduced to its Greeks and a day's P&L is "
              "explained term by term. Gamma scalping is replayed on a real path. The standard structures "
              "(straddles, risk reversals, butterflies, calendars) are read as bets on specific things, and "
              "their historical returns show the volatility premium that sellers collect. Then the other "
              "chair: making a market, setting a spread, leaning quotes against inventory, hedging a book "
              "rather than a trade, and surviving expiry. India's expiry-day boom and the short-volatility "
              "blow-ups are the case files.",
        handoff="The volatility premium is measured properly in Part 12; inventory-based quoting becomes "
                "market making in Part 38; the allegations around expiry-day trading reappear as market "
                "structure in Part 35.",
        outside="Part 10.",
        objectives={
            "U": ["Describe an options position by its delta, gamma, theta and vega, and say what each standard "
                  "structure bets on.",
                  "Compute the daily move at which a long-gamma position breaks even."],
            "M": ["Produce a P&L explain including vanna and volga; choose a hedging frequency or a no-trade "
                  "band under costs.",
                  "Quote a two-sided market with a spread and an inventory skew; hedge a book with a small set "
                  "of instruments; price dispersion with implied correlation."],
            "D": ["Derive demand-based option prices (Garleanu, Pedersen and Poteshman): how dealer inventory "
                  "of unhedgeable risk moves the smile."],
            "I": ["Run an options book through expiry: pin risk, early exercise, dividend plays; read a "
                  "regulatory case about expiry-day trading with its allegations labelled as such."],
        },
        results=[
            ("P&L explain", r"\Delta\Pi\approx\Delta\,\delta S+\tfrac12\Gamma\,\delta S^2+\Theta\,\delta t+\mathcal V\,\delta\sigma"
                            r"+\text{vanna}\,\delta S\,\delta\sigma+\tfrac12\text{volga}\,\delta\sigma^2"),
            ("Breakeven move", r"|\delta S|=S\,\sigma\sqrt{\delta t}"),
            ("Implied correlation", r"\bar\rho=\frac{\sigma_I^2-\sum_i w_i^2\sigma_i^2}{\bigl(\sum_i w_i\sigma_i\bigr)^2-\sum_i w_i^2\sigma_i^2}"),
            ("No-trade band (Whalley-Wilmott)", r"\Delta\pm\Bigl(\frac{3\,k\,S\,\Gamma^2}{2\gamma}\Bigr)^{1/3}"),
        ],
        U=(1, 2, 5), I=(14, 15, 16, 17), D=(18,),
    ),
    Part(
        n=12, level="M", widget="svi", prereq=(9, 10),
        question="Black-Scholes says one volatility per stock. The market quotes a different one for every "
                 "strike and expiry. What is that surface, and what shapes can it not take?",
        story="The smile is read as the market's correction to the lognormal density: skew is the price of "
              "crash insurance, the wings are fat tails. Not every surface is possible. Calendar and butterfly "
              "arbitrage rule shapes out, and the SVI and SSVI parameterizations are built to stay inside the "
              "rules. Dupire's local volatility is derived as the one diffusion that reproduces every vanilla "
              "price, and its predictions for how the smile moves are tested and found wanting. Variance swaps "
              "turn the surface into a traded number, the VIX, and the gap between that number and what is "
              "later realized is the variance risk premium. Volmageddon is the day short-volatility products "
              "met their own rebalancing.",
        handoff="Local volatility's wrong dynamics motivate stochastic volatility (Part 13); the surface is the "
                "scoreboard on which every later pricing model is judged.",
        outside="Parts 9 and 10.",
        objectives={
            "U": ["Read a smile: what skew and curvature say about the implied distribution.",
                  "Explain what the VIX measures and why it is not a forecast."],
            "M": ["Fit SVI and SSVI and test a surface for butterfly and calendar arbitrage.",
                  "Derive Dupire's formula; replicate a variance swap with a strip of options and compute its "
                  "fair strike."],
            "D": ["Prove Gyongy's mimicking theorem; analyse estimating the implied density from noisy prices "
                  "(bias, variance, optimal strike spacing); read Lee's moment formula for the wings."],
            "I": ["Explain the roll of VIX futures, leveraged and inverse volatility notes, dealer gamma and "
                  "same-day options."],
        },
        results=[
            ("Raw SVI", r"w(k)=a+b\Bigl(\rho\,(k-m)+\sqrt{(k-m)^2+s^2}\Bigr)"),
            ("Dupire", r"\sigma_{\text{loc}}^2(K,T)=\frac{\partial_T C}{\tfrac12K^2\,\partial_{KK}C}\quad(r=q=0)"),
            ("Variance swap", r"K_{\text{var}}=\frac{2e^{rT}}{T}\Bigl(\int_0^{F}\frac{P(K)}{K^2}dK+\int_F^\infty\frac{C(K)}{K^2}dK\Bigr)"),
            ("No butterfly arbitrage", r"g(k)=\Bigl(1-\frac{k\,w'}{2w}\Bigr)^2-\frac{w'^2}{4}\Bigl(\frac1w+\frac14\Bigr)+\frac{w''}{2}\ \ge 0"),
        ],
        U=(1, 2, 11), I=(14, 15, 16, 18), D=(7, 17, 19),
    ),
    Part(
        n=13, level="M", widget="sabr", prereq=(5, 12),
        question="If volatility itself is random, what smile does that produce, and can one model fit both the "
                 "smile and the way it moves?",
        story="Volatility has its own river (Part 7); give it its own Brownian motion and a smile appears, "
              "tilted by the correlation between the two. Heston's model is solved by its characteristic "
              "function, each parameter's effect on the smile is shown by moving it, and the simulation is done "
              "honestly, since the naive scheme goes negative. SABR does the same job for rates desks in one "
              "formula with known flaws. Jumps fix the short end that diffusions cannot reach. The later "
              "chapters are about practice: mixing local and stochastic volatility, pricing forward-starting "
              "products the vanillas do not pin down, and what makes a calibration unstable.",
        handoff="No one-factor diffusion reproduces the steep short-dated skew: Part 14 asks whether volatility "
                "is rough. Calibration speed is the subject of Parts 16 and 17.",
        outside="Parts 5 and 12; complex exponentials for the Fourier chapters.",
        objectives={
            "U": ["Explain in pictures why random volatility makes a smile and why negative correlation makes "
                  "a skew."],
            "M": ["Price under Heston by its characteristic function and say what each parameter does to the "
                  "surface; use Hagan's SABR formula and know where it breaks.",
                  "Add jumps (Merton, Kou, Bates); simulate Heston with the quadratic-exponential scheme; "
                  "calibrate and diagnose an ill-posed fit."],
            "D": ["Derive moment explosions for affine stochastic volatility (Andersen and Piterbarg) and link "
                  "them to the wings through Lee's formula; set up stochastic-local volatility by the particle "
                  "method and Bergomi's forward-variance models."],
            "I": ["Say which model a desk uses for which product, and how model risk on forward smiles is "
                  "reserved for."],
        },
        results=[
            ("Heston", r"dS=\sqrt v\,S\,dW^S,\quad dv=\kappa(\theta-v)\,dt+\xi\sqrt v\,dW^v,\quad d\langle W^S,W^v\rangle=\rho\,dt"),
            ("Fourier pricing (Lewis, zero rates)", r"C=S_0-\frac{\sqrt{S_0K}}{\pi}\int_0^\infty\operatorname{Re}\Bigl[e^{iuk}\varphi_T\bigl(u-\tfrac i2\bigr)\Bigr]\frac{du}{u^2+\tfrac14}"),
            ("SABR, at the money", r"\sigma_{\text{ATM}}\approx\frac{\alpha}{F^{1-\beta}}\Bigl[1+\Bigl(\tfrac{(1-\beta)^2\alpha^2}{24F^{2-2\beta}}"
                                    r"+\tfrac{\rho\beta\nu\alpha}{4F^{1-\beta}}+\tfrac{(2-3\rho^2)\nu^2}{24}\Bigr)T\Bigr]"),
            ("Feller condition", r"2\kappa\theta\ge\xi^2"),
        ],
        U=(1, 2), I=(17,), D=(9, 11, 13, 18),
    ),
    Part(
        n=14, level="M", widget="rough", prereq=(7, 13),
        question="The skew of short-dated options explodes like a power of maturity. Is volatility rough, and "
                 "does it matter for prices?",
        story="A frontier part. The at-the-money skew grows roughly like maturity to the power minus 0.4, which "
              "no diffusion produces. A volatility driven by a fractional kernel with Hurst exponent near 0.1 "
              "does, and log realized variance scales the same way in the time series. The part builds rough "
              "Bergomi and rough Heston, shows how to simulate and price them, and then gives the other side "
              "equal time: the estimator's bias under measurement noise, what the options data alone say, and "
              "path-dependent volatility, which gets similar fits from the price path with no roughness at "
              "all. Joint calibration to the S&P 500 and the VIX is the open test.",
        handoff="The simulation cost of rough models is what neural calibrators were built for (Part 17); the "
                "roughness estimate returns as a caution about noisy proxies (Part 40).",
        outside="Parts 7 and 13. The later chapters are at research level.",
        objectives={
            "U": ["Say what 'rough' means for a path, and what the skew's term structure is evidence of."],
            "M": ["Estimate a Hurst exponent from realized variance and state the estimator's weaknesses.",
                  "Simulate rough Bergomi with the hybrid scheme and compute its skew; fit a path-dependent "
                  "volatility model."],
            "D": ["Derive the power-law skew from the kernel; solve rough Heston through the fractional Riccati "
                  "equation and its Markovian lift; state strong convergence rates of rough simulation "
                  "schemes; set out the joint SPX-VIX calibration problem."],
            "I": ["Explain what desks actually run (and do not), and why."],
        },
        results=[
            ("Skew term structure", r"\psi(T)=\Bigl|\frac{\partial\sigma_{\text{imp}}}{\partial k}\Bigr|_{k=0}\;\sim\;T^{H-\frac12}"),
            ("Rough Bergomi", r"v_t=\xi_0(t)\exp\Bigl(\eta\sqrt{2H}\int_0^t(t-s)^{H-\frac12}dW_s-\tfrac{\eta^2}{2}t^{2H}\Bigr)"),
            ("Scaling of log-volatility", r"\mathbb E\,\bigl|\ln\sigma_{t+\Delta}-\ln\sigma_t\bigr|^q\;\propto\;\Delta^{qH}"),
            ("Path-dependent volatility", r"\sigma_t=\beta_0+\beta_1\!\int K_1(t-s)\,\frac{dS_s}{S_s}+\beta_2\sqrt{\int K_2(t-s)\Bigl(\frac{dS_s}{S_s}\Bigr)^2}"),
        ],
        U=(), I=(14, 17), D=(6, 7, 8, 10, 15, 16, 18),
    ),
    Part(
        n=15, level="M", widget="snowball", prereq=(10, 12),
        question="A note pays a 15% coupon unless the index falls through a barrier. What has the buyer sold, "
                 "and who is on the other side?",
        story="The snowball, a best-selling structured product in China, is taken apart: the buyer has sold a "
              "down-and-in put and is paid a coupon for it, the issuer hedges by buying the index as it falls "
              "and selling as it rises. To price it the part needs barriers (reflection, the closed form, the "
              "correction for daily monitoring), digitals and their call-spread hedge, and path dependence in "
              "general. Then correlation products, cliquets, and the uncomfortable fact that models agreeing on "
              "every vanilla disagree on exotics. January 2024, when the snowballs knocked in together, and "
              "Korea's ELS losses are the crisis files.",
        handoff="Pricing these by simulation is slow: Part 16 is the engine. The dealers' hedging flows return "
                "as a market-wide force in Part 41.",
        outside="Parts 10 and 12.",
        objectives={
            "U": ["Decompose a structured note into a bond and options, and say who holds which risk."],
            "M": ["Price barrier options by reflection and correct for discrete monitoring; price digitals, "
                  "Asians and lookbacks.",
                  "Price an autocallable by Monte Carlo, compute the issuer's Greeks, and explain their sign "
                  "changes near the barriers."],
            "D": ["Derive uncertain-volatility bounds (Avellaneda, Levy and Paras) and model-free bounds for a "
                  "one-touch from vanilla prices alone."],
            "I": ["Explain how desks mark, reserve and report exotics, and what happened to dealers and buyers "
                  "in January 2024."],
        },
        results=[
            ("Reflection principle", r"\mathbb P\bigl(\min_{s\le T}W_s\le -b,\ W_T>-a\bigr)=\mathbb P(W_T<a-2b),\quad a\le b"),
            ("Discrete monitoring", r"H\;\to\;H\,e^{\mp\,0.5826\,\sigma\sqrt{\Delta t}}"),
            ("Digital as a call spread", r"\mathbf 1_{S_T>K}\approx\frac{C(K-\varepsilon)-C(K+\varepsilon)}{2\varepsilon}"),
            ("Uncertain volatility (BSB)", r"V_t+\tfrac12\,\sigma^2\!\bigl(V_{SS}\bigr)\,S^2V_{SS}=0,\quad"
                                           r"\sigma(\Gamma)=\sigma_{\max}\mathbf 1_{\Gamma>0}+\sigma_{\min}\mathbf 1_{\Gamma\le0}"),
        ],
        U=(1, 2), I=(9, 10, 15, 17), D=(13, 18),
    ),
]
