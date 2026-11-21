"""Act XII, The Frontier (Parts 63-68)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=63, level="D", widget="network", prereq=(3, 8, 9, 20, 26, 33),
        question="When does a shock to one firm become a shock to everyone?",
        story="On 11 March 2011 an earthquake and tsunami strike north-east Japan; firms far from the coast, "
              "undamaged, stop for want of parts, and the loss travels along supplier-customer links to about half a "
              "point of Japan's growth. The Island's input-output table becomes a network: Domar weights as sums "
              "over supply paths, and Hulten's theorem that a small shock matters by the sector's sales and nothing "
              "else. The viewer picks the sector whose failure would cost most (services, by sales; energy, a third "
              "more than its sales say when inputs are hard to replace). Zipf-sized firms and lopsided networks keep "
              "idiosyncratic shocks from cancelling (Gabaix; Acemoglu et al.), and large shocks to essential inputs "
              "bend Hulten's line (Baqaee and Farhi). The Island's earthquake travels through specific inputs, as in "
              "Japan and America's disasters; Kremer's O-ring. After an intermission of Japan's industrial "
              "production through March 2011, banks' clearing vectors and contagion, robust yet fragile; weak ties "
              "(Called it? right); seeding a village; the key player; network formation, stable against efficient; "
              "two new Dials; and supply networks fragile by design.",
        handoff="Part 64 turns from networks to the machines that learn from data: prediction, selective labels and "
                "machine learning in economics.",
        outside="Part 3: the input-output table; Part 8: technologies and substitution; Part 9: general equilibrium; "
                "Part 20: growth accounting; Part 26: bank runs; Part 33: financial crises; Statistics, Built: "
                "random graphs and peer effects.",
        objectives={
            "U": ["Explain why a sector's sales, not its links, measure its importance for small shocks.",
                  "Explain why firm-level shocks need not cancel out in the aggregate.",
                  "Explain how a disaster travels along supply chains, and what stops it."],
            "M": ["Compute Domar weights from an input-output table and show that they add to more than one.",
                  "Prove Hulten's theorem for Cobb-Douglas economies, and compute the second-order term with CES.",
                  "Find the Eisenberg-Noe clearing vector and compare ring and complete networks."],
            "D": ["Solve a production network with complements and say when second-order terms dominate.",
                  "Characterize efficient and pairwise stable networks in the connections model.",
                  "Explain why supply networks can be fragile in equilibrium, and what it implies for policy."],
            "I": ["Map a supply chain beyond the first tier and identify the inputs that cannot be replaced."],
        },
        results=[
            ("Domar weights", r"\lambda' = \beta'(I - \Omega)^{-1}"),
            ("Hulten's theorem", r"d\log Y = \sum_i \lambda_i \, d\log A_i"),
            ("Granular volatility", r"\sigma_{Y} = \sigma \sqrt{\textstyle\sum_i s_i^2}"),
            ("Clearing vector", r"p_i = \min\!\Big(\bar p_i,\; e_i + \sum_j \pi_{ji} p_j\Big)"),
            ("Key player effort", r"x = (I - \delta G)^{-1} a"),
        ],
        U=(0, 1, 2, 3, 4, 7, "s09_intermission", 9, 10), D=(5, 11, 12, 13, 15), I=(6, 8, 14),
        also=(("Agora's network module", "explainer/economics/agora/network.py"),
              ("The Data Room: Japan's industrial production", "explainer/economics/data")),
    ),
    Part(
        n=64, level="D", widget="bail", prereq=(4, 13, 20, 44, 54, 63),
        question="What does machine learning change in how economics is done?",
        story="Judges decide every day who waits for trial in jail; Kleinberg et al. trained an algorithm on 758,027 "
              "New York City decisions and estimated large gains, but outcomes are seen only for the released. On "
              "the Island's courts, a random forest ranks defendants better than judges who overweight the charge "
              "(18% fewer failures at their detention rate), the viewer detains three of ten, and the contraction "
              "design checks the gain with observed outcomes while filling in hidden ones flatters it; Meehl's 1954 "
              "claim is Called it? (right). Targeting a job programme by risk does worse than at random; double "
              "machine learning recovers an effect that linear controls and a plug-in learner miss; causal forests "
              "allocate places; prediction-powered inference corrects a classifier's measurement. After an "
              "intermission of transistor counts since 1971, a network learns Brock and Mirman's saving rule, "
              "Q-learners learn to price near monopoly, language models serve as pilots and assistants, a calibrated "
              "score makes unequal errors, a new Dial, and the frontier of when to defer.",
        handoff="Part 65 turns from machines that help economists to machines that change the economy: automation, "
                "work and growth.",
        outside="Part 4: instruments and the judge design; Part 13: information; Part 20: the growth model; Part 44: "
                "algorithmic pricing; Part 54: estimation by simulation; Statistics, Built: forests, double ML, "
                "conformal and prediction-powered inference.",
        objectives={
            "U": ["Tell a prediction policy problem from a causal one, with examples.",
                  "Explain why outcomes hidden by a decision make algorithms hard to evaluate.",
                  "Explain why a calibrated score can still make unequal errors across groups."],
            "M": ["Evaluate a decision rule with the contraction design, and say what it can and cannot claim.",
                  "Derive double machine learning's orthogonal score and explain cross-fitting.",
                  "Do inference on a mean measured by a classifier with prediction-powered inference."],
            "D": ["Train a neural network on Euler-equation errors and check it against a known solution.",
                  "Estimate heterogeneous effects with a causal forest and learn a treatment rule.",
                  "Prove Chouldechova's identity and state the impossibility it implies."],
            "I": ["Audit a deployed risk score: its label, its selective labels, and its errors by group."],
        },
        results=[
            ("Orthogonal score", r"\hat\theta = \frac{\sum (d - \hat m)(y - \hat \ell)}{\sum (d - \hat m)^2}"),
            ("Prediction-powered mean", r"\hat\mu = \bar f_N + \overline{(y - f)}_n"),
            ("Chouldechova's identity", r"\text{FPR} = \frac{p}{1-p}\,\frac{1-\text{PPV}}{\text{PPV}}\,(1-\text{FNR})"),
            ("Brock and Mirman", r"k' = \alpha\beta\, k^{\alpha}"),
        ],
        U=(0, 1, 2, 3, 4, "s09_intermission", 10, 12), D=(5, 6, 8, 15), I=(7, 11, 14),
        also=(("Agora's learn module", "explainer/economics/agora/learn.py"),
              ("The Data Room: transistors", "explainer/economics/data")),
    ),
    Part(
        n=65, level="D", widget="automate", prereq=(19, 21, 39, 40, 44, 63, 64),
        question="What happens to work, growth and incomes if machines can do most tasks?",
        story="In 1930 Keynes predicted that in a hundred years the progressive countries would be four to eight times "
              "richer and work fifteen hours a week; they are 4.4 to 7.4 times richer and still work 1,300-1,900 "
              "hours a year. The viewer automates a share of research tasks and watches growth boom and fall back, "
              "or explode when every task is automated. History (the Luddites, Engels's pause, the horse, the ATM) "
              "leads to the task model: displacement against productivity and new tasks, so-so automation, and "
              "labour's share. The dynamo and the J-curve explain why general-purpose technologies take decades; "
              "the experiments with AI assistants find large task gains, most for the least skilled, which "
              "Hulten's arithmetic turns into modest aggregate ones. After an intermission of hours worked since "
              "1950, the race between automation and capital, the research bottleneck and Baumol's disease, "
              "Nordhaus's tests, market structure, policy with Frey and Osborne's Called it?, agents that shop and "
              "price, two new Dials, and Keynes's verdict: partly right.",
        handoff="Part 66 turns from machines that change the economy to states that use trade as a weapon: tariffs, "
                "sanctions and industrial policy.",
        outside="Part 19: Engels's pause; Part 21: ideas and semi-endogenous growth; Part 39: tasks and polarization; "
                "Part 40: the distribution of capital; Part 44: platforms and algorithmic pricing; Part 63: Hulten's "
                "theorem; Part 64: machines that learn.",
        objectives={
            "U": ["Explain displacement, productivity and reinstatement in the task model.",
                  "Explain why general-purpose technologies take decades to raise measured productivity.",
                  "Summarize what the experiments with AI assistants find, and for whom."],
            "M": ["Derive the wage in the task model and decompose its change.",
                  "Compute an aggregate productivity gain from task-level evidence with Hulten's theorem.",
                  "Show why the average price falls towards cost when buyers' agents compare every price."],
            "D": ["Show why automating part of research gives a temporary boom, and automating all of it explosive "
                  "growth.",
                  "Derive Baumol's result that the slow sector sets aggregate growth.",
                  "Explain why wages fall to the cost of a machine when every task can be automated."],
            "I": ["Design a firm's experiment with an AI tool and translate its result into a productivity forecast."],
        },
        results=[
            ("The wage in the task model", r"\ln w = \tfrac{1}{\sigma}\ln Y + \tfrac{1}{\sigma}\ln(N - I) + c"),
            ("Hulten for AI", r"\Delta\ln\text{TFP} \approx s \cdot c"),
            ("Semi-endogenous growth", r"g_A = \frac{\lambda n}{1-\phi}"),
            ("Varian's average price", r"\bar p = c + (1-\mu)(v-c)"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, "s08_intermission", 7, 14), D=(8, 9, 10, 12, 15), I=(11, 13),
        also=(("Agora's automation module", "explainer/economics/agora/automation.py"),
              ("The Data Room: Maddison, the Penn World Table, FRED", "explainer/economics/data")),
    ),
    Part(
        n=66, level="D", widget="tradewar", prereq=(11, 34, 35, 36, 44, 48, 63),
        question="What happens to the gains from trade when trade becomes a weapon?",
        story="On 2 April 2025 the United States set a tariff on almost every country by one formula, the bilateral "
              "deficit over imports, halved; one parameter, the assumed pass-through, multiplied the rates by "
              "nearly four. The 2018-19 tariffs were paid by American buyers; in 2025 the effective rate rose from "
              "2.9% to 11.3% before the Supreme Court struck down the emergency tariffs, and prices rose slowly. The "
              "viewer plays ten rounds of tariff policy against an unknown partner. On CEPII's 2019 flows the "
              "optimal tariff, the Nash war and a 15% tariff with and without retaliation are computed, and "
              "bilateral deficits are put in their place. After an intermission of the trade balance since 1992 "
              "(the rush before the tariffs), weaponized interdependence, dependence as power, resilience, "
              "infant industries and the new evidence (Napoleon's blockade, Korea, shipbuilding), subsidy races, "
              "the dollar as a hub, two Dials, the FOMC's 2025 projection as Called it?, and climate clubs.",
        handoff="Part 67 turns from what economics says to whether it is true: replication, p-hacking and the "
                "credibility revolution.",
        outside="Part 11: games and the folk theorem; Part 34: pass-through and the current account; Parts 35 and 36: "
                "tariffs, gravity and the quantitative trade model; Part 44: platforms and hubs; Part 48: climate "
                "clubs; Part 63: networks.",
        objectives={
            "U": ["Explain who paid for the 2018-19 and 2025 tariffs, and how economists know.",
                  "Explain why a bilateral deficit is not a measure of unfairness, and what sets the overall one.",
                  "Describe how control of a hub, or of a scarce supply, becomes power over others."],
            "M": ["Derive the optimal tariff and show why a tariff war leaves both sides worse off.",
                  "Compute the cost of losing a supplier with the ACR formula.",
                  "Apply Mill's, Bastable's and Baldwin's tests to an infant-industry case."],
            "D": ["Run tariffs with revenue through exact hat algebra, with and without retaliation.",
                  "Derive Brander and Spencer's one-sided and Nash subsidies.",
                  "Separate private from social choices of resilience in a model with spillovers."],
            "I": ["Score a proposed tariff for a ministry: revenue, prices, retaliation and who gains and loses."],
        },
        results=[
            ("The optimal tariff", r"t^\ast = \frac{1}{\varepsilon^\ast}"),
            ("The reciprocal formula", r"\Delta\tau_i = \frac{m_i - x_i}{\varepsilon\,\varphi\,m_i}"),
            ("Losing a supplier", r"\text{loss} = 1 - (1 - s)^{1/\theta}"),
            ("Brander and Spencer", r"s^{\text{Nash}} = \frac{a - c}{5}"),
        ],
        U=(0, 1, 2, 5, "s07_intermission", 6, 11, 13), D=(3, 4, 7, 8, 10, 14), I=(9, 12),
        also=(("Agora's tradewar module", "explainer/economics/agora/tradewar.py"),
              ("The Data Room: FRED and CEPII's Gravity database", "explainer/economics/data")),
    ),
    Part(
        n=67, level="D", widget="field", prereq=(4, 16, 52, 54, 57, 64),
        question="How much of what economics says is true, and how is the field changing the way it finds out?",
        story="Brodeur and coauthors collected 50,000 test statistics from three top journals: a valley just below "
              "the line of significance, a bump just above it. A simulated field with known true effects, "
              "specification search and a publication filter reproduces the camel; the viewer bets on six "
              "published results, and four replicate. Camerer and coauthors' 18 laboratory experiments (11 "
              "replicated, effects two thirds as large) and the prediction markets that priced them; reproducing "
              "papers, and Reinhart and Rogoff's question asked 48 ways; bunching by research design; Andrews and "
              "Kasy's correction on a simulated meta-study. After an intermission of Britain's public debt since "
              "1870, remedies, the empirical turn, the series' own Dials audited, many analysts and a 288-point "
              "specification curve, Brock and Hommes's route to chaos, the profession, AI in the loop, a new "
              "Dial, how to read a paper, and the Dials as a public good.",
        handoff="Part 68, the last, turns from checking economics to making it: one research question carried from "
                "idea to paper, and the series' accounts closed.",
        outside="Part 4: identification and multiple testing; Part 16: the winner's curse; Part 32: Reinhart and "
                "Rogoff; Parts 52 and 63: many agents and networks; Part 54: estimating models; Part 57: scoring "
                "forecasts; Part 64: prediction-powered inference.",
        objectives={
            "U": ["Explain how specification search and publication selection shape a published literature.",
                  "Distinguish reproduction, robustness, replication and generalization, and what each failure means.",
                  "Explain why published effects shrink when studies are repeated."],
            "M": ["Compute a caliper ratio and the false-positive rate of a search over k specifications.",
                  "Write the likelihood of a selected literature and estimate its selection parameter.",
                  "Build a specification curve and report the spread of analysts against the standard error."],
            "D": ["Correct a meta-study for publication bias with study-specific standard errors.",
                  "Size a replication for the true rather than the published effect.",
                  "Derive the loss of stability in Brock and Hommes's switching cobweb."],
            "I": ["Read a new paper with the field's prior: shrink its estimate and say what would change it."],
        },
        results=[
            ("Search over k independent tests", r"P(\text{false positive}) = 1 - 0.95^{k}"),
            ("A selected literature", r"f_{\text{pub}}(z) \propto p(z)\, f(z)"),
            ("The winner's curse", r"E[Z \mid Z > c] = \mu + \frac{\phi(c - \mu)}{1 - \Phi(c - \mu)}"),
            ("Brock and Hommes's flip", r"n^\ast = \frac{b - B}{2b}"),
        ],
        U=(0, 1, 2, 3, "s07_intermission", 7, 11, 13, 14), D=(4, 5, 6, 8, 9, 15), I=(10, 12),
        also=(("Agora's field module", "explainer/economics/agora/field.py"),
              ("The Data Room: Reinhart and Rogoff's panel and the Macrohistory Database",
               "explainer/economics/data")),
    ),
]
