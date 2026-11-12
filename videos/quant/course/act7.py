"""Act VII, The System (Parts 40-42), and the Finale (Part 43)."""

from videos.quant.course import Part

PARTS = [
    Part(
        n=40, level="U", widget="var", prereq=(7, 20),
        question="A bank reports that it will lose more than ten million dollars on one day in a hundred. How "
                 "would you check a number like that?",
        story="A risk measure is a forecast, and forecasts can be scored. Value at risk is computed three ways "
              "(a normal assumption, history, a volatility-filtered history) and each is backtested: do "
              "exceptions happen as often as promised, and do they come alone or in clusters? Expected "
              "shortfall is what you lose when the bad day comes; it is coherent where VaR is not, and harder "
              "to backtest. Extreme value theory fits the tail beyond the data, copulas describe losses that "
              "arrive together, stress tests ask the question history has not asked yet. The regulatory "
              "chapter follows these ideas into the Basel rules.",
        handoff="Risk limits that tighten together are the mechanism of Part 41.",
        outside="Parts 7 and 20.",
        objectives={
            "U": ["Define value at risk and expected shortfall and compute both from a sample of returns.",
                  "Explain why diversification can fail to reduce VaR, and what a stress test is for."],
            "M": ["Forecast VaR by historical, filtered-historical and parametric methods and backtest with "
                  "Kupiec's and Christoffersen's tests.",
                  "Fit a generalized Pareto tail; measure tail dependence; fit a quantile model by pinball "
                  "loss."],
            "D": ["Explain elicitability: why VaR has a consistent scoring function, expected shortfall alone "
                  "has none, and the pair has one (Fissler and Ziegel); bound VaR under dependence "
                  "uncertainty."],
            "I": ["Explain the Basel traffic light, the move from VaR to expected shortfall, and liquidity "
                  "horizons."],
        },
        results=[
            ("Value at risk", r"\mathrm{VaR}_\alpha=\inf\{x:\ \mathbb P(L\le x)\ge\alpha\}"),
            ("Expected shortfall", r"\mathrm{ES}_\alpha=\frac{1}{1-\alpha}\int_\alpha^1\mathrm{VaR}_u\,du"),
            ("Kupiec's test", r"\mathrm{LR}=-2\ln\frac{(1-p)^{T-x}p^{x}}{(1-\hat p)^{T-x}\hat p^{x}}\ \sim\ \chi^2_1"),
            ("Generalized Pareto tail", r"\mathbb P(L-u>y\mid L>u)\approx\Bigl(1+\frac{\xi y}{\beta}\Bigr)^{-1/\xi}"),
        ],
        U=(1, 2, 6), I=(9, 10), D=(7,),
    ),
    Part(
        n=41, level="U", widget="firesale", prereq=(2, 21, 40),
        question="A levered fund loses five percent. What must it sell, to whom, and what does that sale do to "
                 "everyone holding the same thing?",
        story="This is the part where the series' crisis files meet. Leverage turns a price fall into a forced "
              "sale; the sale moves the price; lenders raise margins because volatility rose; the fund sells "
              "again. The loss spiral and the margin spiral are iterated on screen. Fire sales spread losses "
              "to institutions with similar holdings, and a network of mutual debts spreads default, with the "
              "striking result that the network safest against small shocks is the most dangerous against "
              "large ones. Then five crises told with their numbers: LTCM in 1998, the run on the shadow banks "
              "in 2007-08, the dash for cash in March 2020, Shanghai in 2015, and the rate shock and bank runs "
              "of 2022-23.",
        handoff="If the participants are machines trained on the same data, do they make this worse? Part 42.",
        outside="Parts 2, 21 and 40.",
        objectives={
            "U": ["Explain how leverage, margin calls and falling prices reinforce each other.",
                  "Tell the story of one of the five crises with its mechanism and its numbers."],
            "M": ["Iterate a deleveraging spiral and compute its amplification; compute fire-sale spillovers "
                  "across institutions.",
                  "Solve for the clearing payments of a network of debts; compute CoVaR, MES and SRISK; find "
                  "a bank's run threshold."],
            "D": ["Prove existence and uniqueness of the clearing vector (Eisenberg and Noe), the fictitious "
                  "default algorithm, and the phase transition in contagion between the ring and the complete "
                  "network."],
            "I": ["Run a liquidity stress test on a levered book: which positions are sold first, at what "
                  "haircut, and who else is selling."],
        },
        results=[
            ("Leverage and forced sales", r"\text{sell}=\Bigl(\frac{1}{m}-1\Bigr)\times\text{loss}\quad\text{to restore leverage }1/m"),
            ("Clearing vector", r"p^\ast=\min\bigl(\bar p,\ \Pi^\top p^\ast+e\bigr)"),
            ("Contagion threshold", r"\varepsilon^\ast=n\,(a-v)"),
            ("SRISK", r"\mathrm{SRISK}=k\,\text{Debt}-(1-k)\,(1-\mathrm{LRMES})\,\text{Equity}"),
        ],
        U=(1, 2), I=(6, 7, 8, 9, 10, 11), D=(),
    ),
    Part(
        n=42, level="M", widget="kirman", prereq=(8, 38),
        question="Two pricing algorithms that have never communicated settle on prices above the competitive "
                 "level. Is that collusion?",
        story="Markets are increasingly populated by programs that learn. The part starts with artificial "
              "markets, where simple rules of imitation are enough to produce fat tails and volatility "
              "clusters with no news at all. Herding has an exact theory in Kirman's ants. Then learning "
              "agents: a market maker that learns to quote by trial and error, language models placed in a "
              "simulated market, and the experiment the title refers to, in which independent reinforcement "
              "learners arrive at supra-competitive prices and punish deviations. The part works out when "
              "such outcomes can persist and when they are an artefact of the learning rule. The last "
              "chapters ask what happens when everyone trains the same model.",
        handoff="The finale asks what, after all of this, is left to earn.",
        outside="Parts 8 and 38; AI, Built, Part 26, for reinforcement learning.",
        objectives={
            "U": ["Explain how imitation among traders can produce fat tails and volatility clusters.",
                  "Explain what algorithmic collusion means and why intent is hard to define."],
            "M": ["Simulate a fundamentalist-chartist market and test it against the stylized facts of "
                  "Part 1.",
                  "Train tabular Q-learners in a repeated pricing game and measure how far prices sit above "
                  "the competitive level."],
            "D": ["Derive the stationary law of Kirman's herding chain and its two regimes; prove when grim "
                  "trigger sustains collusion and compare the bound with what the learners do."],
            "I": ["Design a test for a trading agent that includes the market's reaction to it; state the "
                  "regulatory questions about shared models."],
        },
        results=[
            ("Herding: stationary law", r"\pi(x)\propto x^{\frac{\varepsilon N}{1-\delta}-1}(1-x)^{\frac{\varepsilon N}{1-\delta}-1}\quad(\text{large }N)"),
            ("Grim trigger", r"\delta\ \ge\ \frac{\pi^D-\pi^C}{\pi^D-\pi^N}"),
            ("Q-learning", r"Q(s,a)\leftarrow(1-\alpha)\,Q(s,a)+\alpha\bigl[r+\delta\max_{a'}Q(s',a')\bigr]"),
            ("Collusion index", r"\Delta=\frac{\bar\pi-\pi^N}{\pi^M-\pi^N}"),
        ],
        U=(1, 2), I=(8, 9), D=(5,),
        also=(("AI, Built, Part 26 (reinforcement learning)", "videos/ai/README.md"),),
    ),
    Part(
        n=43, level="U", widget="skill", prereq=(26,),
        question="After forty-two parts: can you beat the market, and how would anyone know?",
        story="Before costs the average active investor earns the market's return; after costs, less. That is "
              "arithmetic, not a theory. So the question is who is on the winning side of the average, and "
              "whether it can be known in advance. Thousands of funds are sorted into the skilled, the "
              "unskilled and the lucky, with the statistics of Part 25. Skill that exists attracts money until "
              "it no longer shows up in returns. The series then turns the question on itself: what record "
              "would a strategy have to keep (registered before its test, every trial counted, costs stated, "
              "reported whatever the result) for a claim of skill to mean anything? It ends where it began, with "
              "Bachelier, whose model the oil market went back to in April 2020 because a price had gone below "
              "zero.",
        handoff="The House: forty-three parts of tested code, and the question the series started with.",
        outside="The series. The first chapters need only Part 1.",
        objectives={
            "U": ["State Sharpe's arithmetic of active management and what it does and does not imply.",
                  "Explain why a fund's past performance says little about its future."],
            "M": ["Estimate the share of funds with no skill from the distribution of p-values, and split the "
                  "significant ones into skilled and lucky.",
                  "Explain why skill and scale together produce no persistence (Berk and Green)."],
            "D": ["Prove that Storey's estimator of the null share is conservative under arbitrary dependence, "
                  "and the Berk-Green no-persistence result."],
            "I": ["Design an evidence record for a strategy or a manager: what is registered, what is "
                  "counted, what is reported whatever the result."],
        },
        results=[
            ("Sharpe's arithmetic", r"\bar R_{\text{active}}=\bar R_{\text{market}}\ \text{before costs},\qquad\bar R_{\text{active}}<\bar R_{\text{passive}}\ \text{after}"),
            ("Share with no skill (Storey)", r"\hat\pi_0(\lambda)=\frac{\#\{p_i>\lambda\}}{M(1-\lambda)}"),
            ("Chance of beating the index by luck", r"\mathbb P=N\!\Bigl(-\frac{c\sqrt T}{\mathrm{TE}}\Bigr)"),
            ("Bachelier", r"C=(F-K)\,N(d)+\sigma_n\sqrt T\,\varphi(d),\qquad d=\frac{F-K}{\sigma_n\sqrt T}"),
        ],
        U=(1, 2, 4, 8), I=(5, 9, 10), D=(7,),
    ),
]
