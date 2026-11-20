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
]
