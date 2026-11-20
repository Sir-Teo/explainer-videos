"""Act VI, Money and the Cycle (Parts 25-33)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=25, level="U", widget="inflationtax", prereq=(3, 11, 24),
        question="What is money, and what happens when there is too much of it?",
        story="The part opens on Yap, where the money was limestone wheels and a stone lost at the bottom of the sea "
              "still made its owners rich, and with Milton Friedman's comparison to the Bank of France's gold in a "
              "New York basement. It shows why barter fails and why money is a kind of memory; the viewer chooses "
              "which of the Island's goods becomes money, and Kiyotaki and Wright's search economy decides, with fresh "
              "fish and then smoked. It traces money from Lydia's coins to 1971, tests the quantity theory on 146 "
              "countries, measures the hyperinflations, derives Cagan's money demand and the inflation tax's Laffer "
              "curve, scores Cagan's revenue ceiling, and shows how four big inflations ended, then Zimbabwe's and "
              "Venezuela's. After an intermission of American base money, M2 and prices since 1959, it derives "
              "Baumol and Tobin's square-root rule and watches money demand break in the 1980s, shows how a bank "
              "creates a deposit by lending and why the multiplier collapsed after 2008, tests Fisher's equation, "
              "computes the cost of inflation and the Friedman rule, reads one dial, and ends with payments, "
              "stablecoins and central bank digital money.",
        handoff="Part 26 turns to the banks that create most money and why they run; Part 28 to inflation and "
                "expectations; Part 30 to sticky prices; Part 31 to the central bank and its operating framework; "
                "Part 33 to crises; Quant, Built Part 39 to crypto and decentralized finance.",
        outside="Part 3: price indexes and inflation; Part 11: equilibrium and expectations; Part 24: search and "
                "matching. Chapter 3 uses a two-state Bellman equation solved by value iteration; chapter 7 a "
                "first-order difference equation with adaptive expectations.",
        objectives={
            "U": ["Explain the double coincidence of wants, money's three jobs, and why money can be thought of as "
                  "memory.",
                  "State the quantity equation, read it in growth rates, and describe the cross-country evidence and "
                  "its short-run failure.",
                  "Explain how hyperinflations start and end, and how a bank creates a deposit by lending."],
            "M": ["Solve a Kiyotaki-Wright economy and check which trading strategies are equilibria.",
                  "Derive Cagan's inflation-tax Laffer curve, its two steady states with a deficit, Baumol and Tobin's "
                  "rule, and the cost of inflation in a cash-in-advance economy."],
            "D": ["Weigh the evidence on the stability of money demand and its interest semi-elasticity, and the open "
                  "questions about stablecoins and central bank digital money."],
            "I": ["Explain an ample-reserves operating framework and how payment systems settle in central bank "
                  "money."],
        },
        results=[
            ("The quantity equation", r"MV = PY, \quad \pi \approx \mu + \Delta\ln V - g"),
            ("Cagan's money demand", r"\ln \frac{M}{P} = -\alpha\,\pi^e + \gamma"),
            ("The inflation tax's peak", r"\max_\mu \mu e^{-\alpha\mu} \text{ at } \mu = 1/\alpha"),
            ("Baumol and Tobin", r"M^* = \sqrt{\frac{bY}{2i}}"),
            ("Fisher and Friedman", r"i \approx r + \pi^e, \quad i = 0 \Rightarrow \pi = -r"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, "s10_intermission", 9, 10, 11, 12), D=(13, 15), I=(14,),
        also=(("Agora's money", "explainer/economics/agora/money.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
    Part(
        n=26, level="U", widget="bankrun", prereq=(7, 11, 25),
        question="Why are banks fragile, and can they be made safe?",
        story="The part opens on thirty-six hours in March 2023, when the customers of Silicon Valley Bank withdrew 42 "
              "billion dollars in a day, mostly from their phones, and the bank was closed the next morning. It draws "
              "a bank's balance sheet, asks the viewer to stay or withdraw on a rumour, derives Diamond and Dybvig's "
              "deposit contract and its second equilibrium, the run, and runs a bank with sequential service. It "
              "shows the cures, suspension and deposit insurance, against America's bank suspensions before and after "
              "1934; Bagehot's rule after Overend, Gurney, with a fire sale computed against a lender; deposit "
              "insurance as Merton's put and the moral hazard it brings; and capital, with the interest-rate risk "
              "that risk weights miss. After an intermission of small and large banks' deposits through 2023, it "
              "follows runs outside the banks, in repo and money funds, solves the global game that makes runs "
              "predictable, tests panics against fundamentals in the Depression and in 2023, explains banks as "
              "delegated monitors, reads two dials, scores the 2022 stress scenario, and ends with digital runs, the "
              "weekend of 12 March 2023, narrow banking and stablecoins.",
        handoff="Part 27 turns to the Keynesian revolution and a whole economy short of buyers; Part 31 to the central "
                "bank as lender of last resort and its operating framework; Part 33 to financial crises, credit booms "
                "and too big to fail; Quant, Built to bank stocks and credit.",
        outside="Part 7: risk aversion and expected utility; Part 11: games and equilibria; Part 23: Modigliani and "
                "Miller and option pricing; Part 25: what money is. Chapter 3 is a constrained maximization with CRRA "
                "utility; chapter 7 uses Black and Scholes; chapter 10 a Bayesian game with private signals; chapter "
                "12 a binomial tail.",
        objectives={
            "U": ["Draw a bank's balance sheet and explain maturity transformation and why a bank cannot pay everyone "
                  "at once.",
                  "Explain the two equilibria of Diamond and Dybvig's model and how suspension, deposit insurance and a "
                  "lender of last resort remove the run.",
                  "Explain moral hazard from deposit insurance, and how capital and interest-rate risk interact."],
            "M": ["Derive the optimal deposit contract and the share of withdrawals at which waiting stops paying.",
                  "Price deposit insurance as a put, compute a repo squeeze, and solve the global game's threshold "
                  "theta* = c/R."],
            "D": ["Weigh the evidence on panics against fundamentals in the Depression and in 2023, and on deposit "
                  "betas and the output cost of banking crises."],
            "I": ["Explain stress tests, duration and liquidity management at a bank's treasury desk, and deposit "
                  "pricing."],
        },
        results=[
            ("The Diamond-Dybvig contract", r"c_1 = \frac{1}{t + (1-t)R^{1/\gamma - 1}}, \quad c_2 = R^{1/\gamma} c_1"),
            ("The run threshold", r"f^* = \frac{R - c_1}{c_1 (R - 1)}"),
            ("Deposit insurance as a put", r"E = P + V - D \quad (r = 0)"),
            ("Repo", r"\text{assets} \le \text{equity} / h"),
            ("The global game", r"\theta^* = c / R"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, "s10_intermission", 9, 10, 11, 12), D=(13, 15), I=(14,),
        also=(("Agora's banks", "explainer/economics/agora/bank.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
    Part(
        n=27, level="U", widget="coop", prereq=(2, 22, 25),
        question="How can a whole economy be short of buyers?",
        story="The part opens on Capitol Hill, where a babysitting co-operative of about 150 couples fell into "
              "recession because everyone wanted to save coupons and nobody went out, and on the Island's own "
              "co-op, cured when the board prints coupons. It shows the Great Depression in the data against Say's "
              "law, asks the viewer to hoard or spend, and runs the co-op over every quantity of money. It derives "
              "Keynes's effective demand, the cross and Kahn's multiplier as a geometric series, computes the paradox "
              "of thrift, derives Hicks's IS-LM and its fiscal and monetary policy, and follows the economy into the "
              "liquidity trap, with Japan's and America's zero rates and Krugman's promise. Phillips's water machine "
              "runs the multiplier in time. After an intermission of industrial production from 1919 to 1945, it "
              "explains sticky wages with Bewley's interviews and the spike at zero, builds aggregate demand and "
              "supply and the neoclassical synthesis, asks what ended the Depression (gold, money, war), hears the "
              "critics, scores Keynes's forecast of 1919, reads two dials, measures Okun's law and the length of "
              "expansions, and ends with supply shocks that cut demand.",
        handoff="Part 28 turns to inflation, expectations and the Phillips curve; Part 29 to the cycle as an "
                "equilibrium; Part 30 to sticky prices; Part 31 to the central bank; Part 32 to fiscal policy and "
                "multipliers; Part 33 to crises.",
        outside="Part 2: supply and demand; Part 22: the propensity to consume; Part 25: what money is. Chapter 4 "
                "sums a geometric series; chapter 6 solves two linear equations; chapter 8 is a first-order "
                "difference equation.",
        objectives={
            "U": ["Explain effective demand, the Keynesian cross and the multiplier, and why trying to save more can "
                  "lower saving.",
                  "Use IS-LM to show the effects of fiscal and monetary policy, and explain the liquidity trap.",
                  "Explain why money wages are sticky and how aggregate demand and supply combine the short and the "
                  "long run."],
            "M": ["Derive equilibrium income and the multipliers in the cross and in IS-LM, with and without the zero "
                  "bound.",
                  "Solve aggregate demand and supply for demand and supply shocks, and estimate Okun's law."],
            "D": ["Weigh the evidence on what ended the Great Depression and on the size of the propensity to spend "
                  "and Okun's coefficient."],
            "I": ["Build a demand-side forecast from its components and read the output gap."],
        },
        results=[
            ("The cross", r"Y = \frac{a - bT + I + G}{1 - b}"),
            ("Kahn's multiplier", r"\Delta G\,(1 + b + b^2 + \cdots) = \frac{\Delta G}{1 - b}"),
            ("IS and LM", r"Y = \frac{A - d\,r}{1 - b}, \quad \frac{M}{P} = kY - h\,i, \quad i \ge 0"),
            ("Okun's law", r"u - u^* = \beta\,\frac{Y - Y^*}{Y^*}, \quad \beta \approx -0.5"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, "s10_intermission", 9, 10, 11, 12), D=(13, 15), I=(14,),
        also=(("Agora's Keynesian economy", "explainer/economics/agora/keynes.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
]
