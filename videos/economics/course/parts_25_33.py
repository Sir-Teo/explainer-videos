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
    Part(
        n=28, level="U", widget="natural", prereq=(4, 11, 27),
        question="Can a country buy lower unemployment with higher inflation?",
        story="The part opens on Milton Friedman's presidential address of December 1967, which said the menu of "
              "inflation against unemployment would vanish once people came to expect the inflation, and on the "
              "decade that proved it. It draws Phillips's curve and Samuelson and Solow's menu, asks the viewer to "
              "forecast 1973's inflation, derives the natural rate and shows acceleration on the Island, follows the "
              "Great Inflation's loops, scores adaptive forecasts against the data, explains rational expectations, "
              "solves Lucas's islands and shows the Lucas critique. After an intermission of inflation and "
              "unemployment since 1948, it turns inflation into Barro and Gordon's game, measures the cost of "
              "Volcker's disinflation, builds the fixes (a conservative banker, independence, targets), shows the "
              "flat curve of 2000-19 and the surge of 2021-23 with its three accounts, scores two forecasts, reads "
              "two dials, and ends with what surveys say about how households and firms form expectations.",
        handoff="Part 29 builds the business cycle as an equilibrium; Part 30 gives prices that are set in advance "
                "and the New Keynesian Phillips curve; Part 31 the central bank's rules and targets.",
        outside="Part 4: the Lucas critique on the Island; Part 11: games; Part 27: aggregate demand and supply. "
                "Chapter 7 is a normal signal-extraction problem; chapter 9 a two-stage game solved backwards; "
                "chapter 11 a one-dimensional minimization.",
        objectives={
            "U": ["Explain the expectations-augmented Phillips curve, the natural rate and why holding unemployment "
                  "below it makes inflation accelerate.",
                  "Contrast adaptive and rational expectations and explain the Lucas critique.",
                  "Explain the inflation bias of discretion and the case for independent central banks with targets."],
            "M": ["Solve Lucas's signal-extraction problem and Barro and Gordon's game, and find Rogoff's best "
                  "central banker.",
                  "Estimate a Phillips curve's slope and a sacrifice ratio from data."],
            "D": ["Weigh the accounts of the flat Phillips curve and of the 2021-23 surge, and the evidence on how "
                  "expectations are formed."],
            "I": ["Build an inflation forecast from trend, shocks, expectations and slack, and explain indexation in "
                  "wage bargaining."],
        },
        results=[
            ("The expectations-augmented curve", r"\pi = \pi^e - \beta\,(u - u^*)"),
            ("Adaptive expectations", r"\pi^e_{t+1} = \pi^e_t + \lambda\,(\pi_t - \pi^e_t)"),
            ("Lucas's signal extraction", r"\theta = \frac{\sigma_z^2}{\sigma_z^2 + \sigma_m^2}"),
            ("The inflation bias", r"\pi^{\text{discretion}} = \lambda b k"),
            ("The sacrifice ratio", r"\frac{\text{point-years of output lost}}{\text{points of disinflation}}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, "s10_intermission", 9, 10, 11), D=(12, 13, 14, 16), I=(15,),
        also=(("Agora's expectations", "explainer/economics/agora/expectations.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
    Part(
        n=29, level="U", widget="cake", prereq=(7, 20, 22, 28),
        question="Could booms and slumps be an economy's best response to shocks it cannot avoid?",
        story="The part opens on Kydland and Prescott's paper of 1982 and on two cycles side by side, America's and "
              "a frictionless model's. It defines the cycle by filters (Hodrick and Prescott against Hamilton, and "
              "the end-point problem), asks the viewer which of six series turns first before a recession (housing), "
              "and builds dynamic programming from a cake: the Bellman equation solved by hand, then by value "
              "function iteration, with the contraction drawn. It solves Brock and Mirman's stochastic growth model, "
              "builds shocks as Markov chains (Tauchen against Rouwenhorst), adds labour supply and Hansen and "
              "Rogerson's indivisible labour, calibrates the model, and solves it by counting the roots of the "
              "linearized system. After an intermission of America's cycle since 1947, it puts the model's impulse "
              "responses and moments beside the data's, shows what fails (hours against productivity, the Solow "
              "residual's recessions), re-estimates Gali's VAR in both specifications, scores Prescott's estimate, "
              "measures the labour wedge, and reads the Frisch elasticity dial.",
        handoff="Part 30 puts money and sticky prices into this framework; Part 31 the central bank; Part 51 solves "
                "economies without formulas; Part 52 gives them many households; Part 55 estimates them.",
        outside="Part 7: discounting; Part 20: the Solow model and the residual; Part 22: consumption smoothing; "
                "Part 28: rational expectations. Chapter 3 needs a derivative and a geometric series; chapter 4 the "
                "idea of a fixed point; chapter 8 eigenvalues of a 3-by-3 matrix; chapter 11 a vector "
                "autoregression.",
        objectives={
            "U": ["Explain how a business cycle is measured against a trend, and why the filter matters.",
                  "Write a Bellman equation for the cake problem and solve it, and explain intertemporal "
                  "substitution and indivisible labour.",
                  "Explain what the real business cycle model gets right and wrong about the US cycle."],
            "M": ["Solve a dynamic program by value function iteration and explain why it converges.",
                  "Discretize an AR(1) by Tauchen's and Rouwenhorst's methods, and log-linearize and solve a model "
                  "with the Blanchard-Kahn conditions."],
            "D": ["Weigh the evidence on technology shocks and hours (long-run VARs, purified technology) and on "
                  "the Frisch elasticity, micro against macro."],
            "I": ["Lay out the workflow of a structural model in a policy institution, from steady state to "
                  "scenario."],
        },
        results=[
            ("The Bellman equation", r"V(w) = \max_{c} \{\log c + \beta V(w - c)\} \Rightarrow c = (1-\beta)\,w"),
            ("The contraction", r"\| TV - TW \| \le \beta\, \| V - W \|"),
            ("Brock and Mirman", r"k' = \alpha\beta\, z k^{\alpha}"),
            ("The steady state", r"\frac{\bar k}{\bar y} = \frac{\alpha}{1/\beta - 1 + \delta}"),
            ("Blanchard and Kahn", r"\#\{|\lambda| > 1\} = \#\{\text{jump variables}\}"),
        ],
        U=(0, 1, 2, 3, 6, 7, "s10_intermission", 9, 10, 12), D=(11, 13, 15), I=(14,),
        also=(("Agora's dynamic programming", "explainer/economics/agora/dp.py"),
              ("Agora's real business cycle", "explainer/economics/agora/rbc.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
    Part(
        n=30, level="U", widget="nk", prereq=(10, 12, 22, 28, 29),
        question="Why does money move the real economy, and what is the best a central bank can do?",
        story="The part opens on the price collectors behind America's consumer price index and on Bils and "
              "Klenow, who counted how often each price changes. It asks the viewer how long the median price "
              "lasts, reviews the evidence (magazines, a survey of firms, the records, sticky and flexible inflation), "
              "computes Mankiw's menu-cost argument on the Island's ferry, and derives the New Keynesian Phillips "
              "curve from Calvo pricing and the dynamic IS curve from the Euler equation. It fits Taylor's rule to "
              "the Greenspan years, draws the Taylor principle, and solves the three equations for three shocks. "
              "After an intermission of sticky and flexible inflation since 1968, it shows the divine coincidence, "
              "optimal policy under discretion and commitment, the selection effect with 20,000 simulated firms, the "
              "zero lower bound and the forward-guidance puzzle, and the frictions of medium-scale models, reads the "
              "frequency-of-price-changes dial, and scores Bernanke's 2002 promise on deflation.",
        handoff="Part 31 turns to what central banks actually do and how their effects are measured; Part 52 gives "
                "the model many households; Part 55 estimates it.",
        outside="Part 10: monopoly pricing; Part 12: monopolistic competition; Part 22: the Euler equation; Part 28: "
                "the Phillips curve; Part 29: the saddle path. Chapter 5 sums a geometric series of expectations; "
                "chapter 8 checks the roots of a 2-by-2 matrix; chapter 10 is a constrained minimization.",
        objectives={
            "U": ["Explain why prices are sticky, with the evidence on how often they change and Mankiw's menu-cost "
                  "argument.",
                  "Explain the three equations of the New Keynesian model and what each says about firms, "
                  "households and the central bank.",
                  "Explain the Taylor principle, the divine coincidence and why the zero lower bound matters."],
            "M": ["Derive the New Keynesian Phillips curve from Calvo pricing and solve the model for AR(1) shocks.",
                  "Compare discretion and commitment after a cost-push shock, and compute policy at the zero bound."],
            "D": ["Weigh the evidence on price stickiness (sales, selection) and the forward-guidance puzzle and its "
                  "repairs."],
            "I": ["Use a New Keynesian model for scenarios and alternative policy paths, alongside judgement."],
        },
        results=[
            ("The New Keynesian Phillips curve", r"\pi_t = \beta\,\mathbb{E}_t\pi_{t+1} + \kappa x_t"),
            ("The dynamic IS curve", r"x_t = \mathbb{E}_t x_{t+1} - \tfrac{1}{\sigma}(i_t - \mathbb{E}_t\pi_{t+1} - "
                                     r"r^n_t)"),
            ("Taylor's rule", r"i = 2 + \pi + 0.5(\pi - 2) + 0.5x"),
            ("The Taylor principle", r"\kappa(\phi_\pi - 1) + (1 - \beta)\phi_x > 0"),
            ("Mankiw's menu cost", r"\Delta\Pi/\Pi \approx \varepsilon(\varepsilon - 1)g^2/2"),
        ],
        U=(0, 1, 2, 3, 4, 6, 7, "s10_intermission", 9), D=(11, 12, 13, 14, 16), I=(15,),
        also=(("Agora's sticky prices", "explainer/economics/agora/nk.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
]
