"""Act VI, Market Microstructure: Parts 35-39."""

from videos.quant.course import Part

PARTS = [
    Part(
        n=35, level="U", widget="gm", prereq=(2, 4),
        question="Why is there a spread between the price to buy and the price to sell, and what do an "
                 "insider's orders reveal?",
        story="A dealer who quotes two prices has two problems. Inventory: every trade leaves a position that "
              "must be carried. Information: some of the people trading know more. Glosten and Milgrom show "
              "the spread is insurance against the informed, paid by everyone else; Kyle shows how an insider "
              "hides in the noise and how prices absorb the information anyway. The part then measures these "
              "things from data alone: the spread implied by price reversals, the price impact per unit of "
              "order flow, the share of trading that is toxic, and where price discovery happens when the "
              "same asset trades in two places. The flash crash is the day liquidity left.",
        handoff="The next part opens the book itself: queues, order flow and the microprice.",
        outside="Parts 2 and 4 (Bayes' rule is enough for most of it).",
        objectives={
            "U": ["Explain the bid-ask spread as compensation for inventory risk and adverse selection.",
                  "Update a dealer's belief after a buy or a sell with Bayes' rule."],
            "M": ["Derive Glosten-Milgrom quotes and Kyle's one-period equilibrium with its lambda.",
                  "Estimate the effective spread (Roll), price impact (Kyle's lambda, Amihud) and information "
                  "shares (Hasbrouck) from data."],
            "D": ["Solve Kyle's model in continuous time: the insider's bridge strategy, constant depth, and "
                  "the verification argument (Kyle; Back)."],
            "I": ["Describe market structure: lit and dark venues, wholesalers, maker-taker fees, circuit "
                  "breakers; explain what happened on 6 May 2010."],
        },
        results=[
            ("Glosten-Milgrom quotes", r"\text{ask}=\mathbb E[V\mid\text{buy}],\qquad\text{bid}=\mathbb E[V\mid\text{sell}]"),
            ("Kyle's lambda", r"p=p_0+\lambda\,(x+u),\qquad\lambda=\frac{\sigma_v}{2\sigma_u}"),
            ("Roll's spread", r"s=2\sqrt{-\operatorname{Cov}(\Delta p_t,\Delta p_{t-1})}"),
            ("Amihud illiquidity", r"\mathrm{ILLIQ}=\frac1D\sum_{d}\frac{|r_d|}{\text{dollar volume}_d}"),
        ],
        U=(1, 2), I=(8, 9, 10, 11), D=(),
        also=(("Building a Real-Time Trading System (the engineering)", "videos/markets/trading/README.md"),),
    ),
    Part(
        n=36, level="M", widget="lob", prereq=(5, 35),
        question="With a bid at 100.00 for five hundred and an offer at 100.01 for one hundred, where is fair "
                 "value?",
        story="Not at the midpoint. The thin side is more likely to be consumed first, so the next move is "
              "probably up, and the part turns that into numbers on a real order book. Queues are modelled as "
              "they are: orders arrive, cancel and trade at rates that depend on the state of the book, and "
              "events cause further events, a self-exciting process with most of its activity endogenous. "
              "Order-flow imbalance explains short-horizon price changes almost linearly. The microprice "
              "corrects the midpoint for the state of the queues. A network is trained on the book and "
              "compared with the linear model, a simulator of the book is fitted, and an order is placed in "
              "its queue to see what a place in line is worth.",
        handoff="A model of the book prices a large order: Part 37. A place in the queue is the market maker's "
                "asset: Part 38.",
        outside="Parts 5 and 35.",
        objectives={
            "U": ["Read a limit order book: levels, queues, market and limit orders, price-time priority."],
            "M": ["Compute order-flow imbalance and regress price changes on it; estimate the probability the "
                  "next move is up from queue sizes.",
                  "Fit a Hawkes process to order arrivals and interpret its branching ratio; fit and simulate "
                  "a queue-reactive model."],
            "D": ["Prove the microprice theorem for a finite-state Markov book (the adjustment as the solution "
                  "of a Poisson equation) and test its Markov assumption on data."],
            "I": ["Score a short-horizon signal against the spread and fees it must pay; value queue "
                  "position."],
        },
        results=[
            ("Queue imbalance", r"I=\frac{Q^b}{Q^b+Q^a}"),
            ("Next move up (diffusive queues)", r"\mathbb P(\text{up})=1-\frac{2}{\pi}\arctan\frac{Q^a}{Q^b}"),
            ("Order-flow imbalance", r"\Delta m_t\approx\beta\,\mathrm{OFI}_t,\qquad\beta\propto\frac{1}{\text{depth}}"),
            ("Hawkes intensity", r"\lambda_t=\mu+\sum_{t_i<t}\alpha\,e^{-\beta(t-t_i)},\qquad n=\frac{\alpha}{\beta}<1"),
        ],
        U=(1,), I=(9,), D=(6,),
    ),
    Part(
        n=37, level="U", widget="ac", prereq=(8, 36),
        question="Trading ten percent of a day's volume costs thirty basis points. What does forty percent "
                 "cost, and how should the order be split?",
        story="Not four times as much: about twice. The cost of a large order grows like the square root of "
              "its size, in every market where it has been measured, and the part asks what kind of book "
              "produces that law. Impact is partly permanent and partly transient; a propagator model "
              "describes how each trade's effect decays, and the decay cannot be arbitrary or a round trip "
              "would make money. Almgren and Chriss trade the cost of going fast against the risk of going "
              "slow. When impact decays, the best schedule is a block, a trickle and another block. A "
              "reinforcement-learning executor is trained and compared with both.",
        handoff="The other side of the execution algorithm is the market maker: Part 38.",
        outside="Part 36; Part 8 for the control chapters.",
        objectives={
            "U": ["State the square-root law of market impact and use it to estimate the cost of an order.",
                  "Explain TWAP, VWAP and implementation shortfall."],
            "M": ["Derive Almgren-Chriss optimal schedules and their efficient frontier.",
                  "Fit a propagator model to trade data and compute the cost of a schedule under transient "
                  "impact."],
            "D": ["State the no-dynamic-arbitrage conditions on impact kernels (Gatheral) and derive the "
                  "optimal schedule under transient impact, including Obizhaeva and Wang's solution."],
            "I": ["Read a transaction-cost report; choose an algorithm and a participation rate for a given "
                  "order and urgency."],
        },
        results=[
            ("Square-root law", r"\text{cost}\approx Y\,\sigma\sqrt{\frac{Q}{V}}"),
            ("Almgren-Chriss", r"x(t)=X\,\frac{\sinh\kappa(T-t)}{\sinh\kappa T},\qquad\kappa=\sqrt{\frac{\lambda\sigma^2}{\eta}}"),
            ("Propagator", r"p_t=p_0+\sum_{s<t}G(t-s)\,\varepsilon_s\,v_s+\text{noise}"),
            ("Obizhaeva-Wang", r"\text{blocks }\frac{X}{2+\rho T}\text{ at each end, rate }\frac{\rho X}{2+\rho T}\text{ between}"),
        ],
        U=(1, 2), I=(8, 9), D=(4,),
    ),
    Part(
        n=38, level="U", widget="mm", prereq=(35, 36),
        question="A market maker buys at the bid and sells at the offer all day. Where does the money come "
                 "from, and who takes it away?",
        story="The spread earned on each round trip is the income; the losses come from quotes that are stale "
              "when the price moves. The part replays a maker on real trade data, slow and fast, and the "
              "difference between them is the business. Optimal quotes lean against inventory "
              "(Avellaneda-Stoikov and its closed-form approximation). Tick size and queue position decide who "
              "earns the spread. Exchange-traded funds are market making across two markets, held together "
              "by creation and redemption. The speed race is given its economics: when everyone is equally "
              "fast, the spread is the price of being picked off, and a batch auction would remove it.",
        handoff="Crypto rebuilds all of this with a formula in place of a dealer: Part 39. Learning market "
                "makers that find each other's prices are Part 42.",
        outside="Parts 35 and 36.",
        objectives={
            "U": ["Explain a market maker's P&L: spread earned, adverse selection, inventory risk.",
                  "Explain how ETF arbitrage keeps a fund's price near its holdings' value."],
            "M": ["Fit fill intensities and compute optimal quotes with an inventory skew.",
                  "Evaluate a quoting rule by replay on trade data, including markouts and queue position."],
            "D": ["Derive the sniping equilibrium of Budish, Cramton and Shim for a general jump distribution "
                  "and show what frequent batch auctions change."],
            "I": ["Explain the economics of speed, co-location, and what public filings show about a market "
                  "maker's daily P&L."],
        },
        results=[
            ("Reservation price", r"r=s-q\,\gamma\,\sigma^2(T-t)"),
            ("Optimal spread (Avellaneda-Stoikov)", r"\delta^a+\delta^b=\gamma\sigma^2(T-t)+\frac{2}{\gamma}\ln\Bigl(1+\frac{\gamma}{k}\Bigr)"),
            ("Sniping spread", r"\frac{s}{2}=\frac{\lambda_{\text{jump}}\,J}{\lambda_{\text{invest}}+\lambda_{\text{jump}}}"),
            ("Fill intensity", r"\Lambda(\delta)=A\,e^{-k\delta}"),
        ],
        U=(1, 5, 6), I=(7, 8), D=(),
    ),
    Part(
        n=39, level="U", widget="amm", prereq=(22, 38),
        question="A liquidity pool has no dealer, only a formula. When the price doubles, what has the person "
                 "who funded it lost?",
        story="Crypto is the series' natural experiment in market design: every structure of the previous "
              "four parts rebuilt in public, with the data free. A constant-product pool quotes any size from "
              "one equation, and the provider's loss against simply rebalancing is derived exactly: it "
              "accrues at a rate of volatility squared over eight, and it is paid to arbitrageurs. "
              "Concentrated liquidity multiplies both the fee and the loss. The order of transactions in a "
              "block is itself worth money. Perpetual futures hold their price to the spot with a funding "
              "payment, which creates a carry trade with collateral risk. Stablecoins are money-market funds "
              "and run like them.",
        handoff="Runs, leverage and liquidations are the general subject of Part 41.",
        outside="Parts 22 and 38.",
        objectives={
            "U": ["Explain how a constant-product market maker sets prices and what impermanent loss is.",
                  "Explain a perpetual future's funding rate, and why a stablecoin can run."],
            "M": ["Derive impermanent loss and loss-versus-rebalancing; value a concentrated position.",
                  "Compute the cash-and-carry return on a perpetual net of funding and collateral costs; "
                  "solve for the profit of a sandwich attack."],
            "D": ["Prove the loss-versus-rebalancing formula (Milionis, Moallemi, Roughgarden and Zhang), its "
                  "exact discrete form, and its version with fees and discrete blocks."],
            "I": ["Assess a crypto strategy for the risks its return series does not show: venue, custody, "
                  "collateral, liquidation, legal."],
        },
        results=[
            ("Constant product", r"x\,y=k,\qquad P=\frac{y}{x}"),
            ("Impermanent loss", r"\mathrm{IL}(r)=\frac{2\sqrt r}{1+r}-1"),
            ("Loss versus rebalancing", r"\frac{d\,\mathrm{LVR}}{dt}=\frac{\sigma^2}{8}\,V"),
            ("Perpetual funding", r"\text{funding}\approx\text{premium}+\operatorname{clamp}(\text{interest}-\text{premium})"),
        ],
        U=(1, 2, 8), I=(9, 10), D=(),
    ),
]
