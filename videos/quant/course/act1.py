"""Act I, Markets and Money (Parts 1-3)."""

from videos.quant.course import Part

PARTS = [
    Part(
        n=1, level="U", widget="walk",
        question="If prices are a fair game, as Bachelier said in 1900, why does anyone trade, and who is on the "
                 "other side?",
        story="A real price chart is shown beside a coin-flip walk, and you cannot tell them apart: the direction "
              "of returns is close to unpredictable. Then the differences appear. Real returns have heavy tails, "
              "their volatility comes in clusters, and both fade at slower clocks. The part separates the two "
              "worlds the series lives in: Q, where a price is a discounted expectation, and P, where someone is "
              "paid to hold risk. It ends with Thorp, who beat a game that was not quite fair by knowing exactly "
              "how unfair it was.",
        handoff="The stylized facts become the tests every later model must pass; P and Q become the series' two "
                "halves; 'who is on the other side?' is asked in every part.",
        outside="Calculus, and a first course in probability (expectation, variance, the normal distribution).",
        objectives={
            "U": ["Compute simple and log returns, and explain the volatility drag between the average and the "
                  "compounded return.",
                  "State the stylized facts of returns (no linear memory, heavy tails, volatility clusters) and "
                  "show each in data."],
            "M": ["Run and read a variance-ratio test, including its heteroskedasticity-robust form.",
                  "Estimate a tail exponent with Hill's estimator and say what it implies for which moments "
                  "exist."],
            "D": ["Derive the limiting law of the variance ratio and explain why it fails when the fourth "
                  "moment's structure is that of a GARCH process."],
            "I": ["Explain how tail assumptions enter margin and capital rules, and what March 2020 did to them."],
        },
        results=[
            ("Volatility drag", r"g \;\approx\; \mu - \tfrac12\sigma^2"),
            ("Variance ratio", r"\mathrm{VR}(q)=\frac{\operatorname{Var}(r_t+\dots+r_{t+q-1})}{q\operatorname{Var}(r_t)}"
                               r"\;\approx\;1+2\sum_{k=1}^{q-1}\Bigl(1-\tfrac{k}{q}\Bigr)\rho_k"),
            ("Power-law tail", r"\mathbb P(|r|>x)\sim C\,x^{-\alpha},\qquad \alpha\approx 3"),
            ("Martingale", r"\mathbb E[P_{t+1}\mid\mathcal F_t]=P_t"),
        ],
        U=(1, 2, 3, 5, 6, 9, 10, 11, 12), I=(13, 14, 16), D=(15,),
        also=(("Stochastic Calculus, Visualized (a gentler first pass)", "videos/math/stochastic/README.md"),),
    ),
    Part(
        n=2, level="U", widget="margin", prereq=(1,),
        question="What actually happens between pressing 'buy' and owning the share, and where can it break?",
        story="One order is followed through the machine: the book or the auction that matches it, the clearing "
              "house that steps between buyer and seller, the two days (now one) before it settles, and the "
              "margin that makes the promise credible. Leverage, short selling, repo and prime brokerage are the "
              "same idea seen from different desks: someone lends, someone posts collateral, and a rule says when "
              "the position is closed for you. The crisis file is the day in September 2019 when the repo rate "
              "more than doubled.",
        handoff="Margin and funding return in every crisis of the series (Parts 21, 41); the auction and the "
                "book return as microstructure (Parts 35-38).",
        outside="Nothing beyond Part 1.",
        objectives={
            "U": ["Describe the life of a trade: order, match, clearing, settlement, and who bears the risk at "
                  "each step.",
                  "Compute a liquidation price from leverage and a maintenance margin, for a long and for a "
                  "short."],
            "M": ["Price a future by cost of carry and compute a minimum-variance hedge ratio.",
                  "Size initial margin from a volatility forecast and a confidence level, and net exposures "
                  "bilaterally and through a central counterparty."],
            "D": ["Backtest a margin model: derive Kupiec's likelihood-ratio test and its exact size, and add "
                  "Christoffersen's test of independence."],
            "I": ["Explain repo, haircuts, specials, securities lending and what a prime broker does when a "
                  "client cannot meet a call."],
        },
        results=[
            ("Cost of carry", r"F_0 = S_0\,e^{(r-q)T}"),
            ("Liquidation price of a long", r"P_{\text{liq}} = P_0\,\frac{1-1/L}{1-m}"),
            ("Leverage and haircut", r"L_{\max}=\frac1h"),
            ("Minimum-variance hedge", r"h^\ast=\rho\,\frac{\sigma_S}{\sigma_F}"),
        ],
        U=(1, 2, 3, 4, 6, 8, 10), I=(12, 13, 14, 16, 17), D=(18,),
        also=(("Building a Real-Time Trading System (the engineering)", "videos/markets/trading/README.md"),),
    ),
    Part(
        n=3, level="U", widget="dcf", prereq=(1,),
        question="What is a share a claim on, and how far can accounting numbers be trusted to say what it is "
                 "worth?",
        story="A share is a claim on cash flows that mostly arrive decades from now, which makes it a very long "
              "bond: the part computes its duration and shows why growth stocks fall hardest when rates rise. "
              "The three financial statements are run forward for a model firm, accruals are separated from "
              "cash, and the discounted cash flow is drawn as a surface over the two numbers nobody knows, "
              "growth and the discount rate. Then the market's side: multiples, the CAPE, Modigliani and Miller, "
              "equity as a call on the firm's assets, and what happens around earnings announcements.",
        handoff="Value becomes a factor in Part 24; equity as a call becomes the credit model of Part 20; the "
                "point-in-time store is the discipline behind every backtest (Part 26).",
        outside="Compound interest. No accounting is assumed.",
        objectives={
            "U": ["Discount cash flows: NPV, IRR, annuities and the growing perpetuity.",
                  "Read an income statement, balance sheet and cash-flow statement, and reconcile earnings with "
                  "cash."],
            "M": ["Build a DCF with a terminal value, find its sensitivity to growth and the discount rate, and "
                  "back out the rate a price implies.",
                  "Use residual income and Modigliani-Miller (with taxes and distress) to connect book value, "
                  "leverage and price."],
            "D": ["Derive Ohlson's valuation from linear information dynamics and estimate the persistence of "
                  "abnormal earnings from filings."],
            "I": ["Explain point-in-time data, restatements and look-ahead, and how accounting signals decayed "
                  "once published."],
        },
        results=[
            ("Gordon growth", r"P_0=\frac{D_1}{r-g}"),
            ("Duration of equity", r"-\frac{\partial\ln P}{\partial r}=\frac{1}{r-g}"),
            ("Modigliani-Miller II", r"r_E = r_A + (r_A-r_D)\,\frac{D}{E}"),
            ("Residual income", r"P_0 = B_0+\sum_{t\ge1}\frac{\mathbb E[x_t - r\,B_{t-1}]}{(1+r)^t}"),
        ],
        U=(1, 3, 4, 6, 9, 10), I=(5, 15, 16, 17), D=(18,),
        also=(("Opposing Forces: Earnings vs. the Cost of Money", "videos/markets/opposing_forces/README.md"),),
    ),
]
