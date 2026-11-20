"""Act IX, The Fields (Parts 43-50), first block (Parts 43-47)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=43, level="U", widget="merger", prereq=(4, 6, 10, 12),
        question="How do you tell whether a market is competitive when you cannot see anyone's costs?",
        story="The part opens on the cereal aisle: around 1980 Kellogg, General Mills and General Foods sold most of "
              "America's cereal, and the FTC's 'shared monopoly' case of 1972 was dismissed in 1981. It shows on 300 "
              "Island industries that concentration and margins correlate (0.78) with no collusion at all, as "
              "Demsetz argued against Bain, and why: a Cournot industry's margin is its Herfindahl index over the "
              "elasticity. The viewer judges two proposed mergers among five cereals in three nests; the one that "
              "barely moves the concentration index raises prices ten times as much, because diversion, not share, "
              "does the work. Bresnahan's rotation identifies conduct. Demand for differentiated products moves "
              "into characteristics space; the logit, Berry's inversion, the red bus and the nested logit lead to "
              "Berry, Levinsohn and Pakes's random coefficients, derived with the contraction and the moments. Their "
              "estimator finds the truth on 40 simulated Islands where OLS and IV logit do not, and plain logit on "
              "their real data leaves 726 impossible inelastic demands even by IV. After an intermission of "
              "corporate profits over GDP since 1947, it runs Nevo's conduct test on the Island's cereal aisle, "
              "simulates a merger with the cost savings that would offset it, values new goods, estimates "
              "production functions by Ackerberg, Caves and Frazer, reads markups from production data and the "
              "debate over their rise, estimates Bresnahan and Reiss's entry thresholds from 400 towns, enters two "
              "dials, reviews mergers in practice with MillerCoors as Called it?, and reaches the frontier.",
        handoff="Part 44 adds time: dynamic decisions, dynamic oligopoly, platforms and antitrust; Part 59 takes the "
                "demand systems into pricing and strategy at firms.",
        outside="Part 4: instrumental variables; Part 6: demand and elasticities; Part 10: the Lerner rule; Part 12: "
                "Cournot and Bertrand. Chapter 6 uses a contraction mapping and the generalized method of moments; "
                "chapter 10 a two-step semiparametric estimator; chapter 12 an ordered probit.",
        objectives={
            "U": ["Explain why concentration alone cannot reveal market power.",
                  "Say why a merger of close substitutes can raise prices more than a merger of large firms.",
                  "State what Nevo's test compares and what it found for cereal."],
            "M": ["Derive logit shares, Berry's inversion and the multi-product Bertrand markups.",
                  "Set out the BLP estimator: simulated shares, the contraction, instruments and moments.",
                  "Explain the simultaneity problem in production functions and the proxy estimators' fix."],
            "D": ["Assess the evidence on rising markups and what the production approach needs.",
                  "Say what instruments and micro data identify in demand estimation."],
            "I": ["Screen a merger by concentration, diversion and upward pricing pressure, and simulate it."],
        },
        results=[
            ("Cournot margins", r"\sum_i s_i\,\frac{p - c_i}{p} = \frac{\mathrm{HHI}}{10{,}000\,\varepsilon}"),
            ("Berry's inversion", r"\ln s_j - \ln s_0 = x_j\beta - \alpha p_j + \xi_j"),
            ("Multi-product markups", r"p - c = -\big(\Omega \circ \tfrac{\partial s}{\partial p}'\big)^{-1} s"),
            ("De Loecker and Warzynski", r"\mu = \theta_V \cdot \frac{P\,Q}{P_V V}"),
            ("Upward pricing pressure", r"\mathrm{UPP}_1 = D_{12}(p_2 - c_2) - E_1 c_1"),
        ],
        U=(0, 1, 2, 4, 5, "s09_intermission", 8, 9, 12), D=(13, 15), I=(14,),
        also=(("Agora's industrial organization", "explainer/economics/agora/io.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
    Part(
        n=44, level="U", widget="rebuild", prereq=(11, 12, 22, 43),
        question="How do firms compete over time, and what is different when the product is a network?",
        story="The part opens on Harold Zurcher's ledger: Rust's data on the Madison bus company's engines, drawn "
              "as sawtooth lines of miles since each rebuild. The viewer picks a rebuild rule for the Island's buses "
              "(150,000 miles is cheapest), then Rust's model is written down and estimated by the nested fixed "
              "point on Zurcher's 104 buses: a rebuild cost of 9.79 and upkeep of 2.65 per thousand steps, with "
              "myopia rejected and the discount factor itself barely identified. Hotz and Miller's conditional choice "
              "probabilities skip the fixed point, and prove fragile with only 60 rebuilds but fine on simulated "
              "fleets. A Markov-perfect duopoly races hardest when neck and neck; double marginalization, the "
              "Chicago critique and resale price maintenance follow; a two-sided platform charges the valuable side "
              "less, below cost if need be; and network effects let a worse first mover win, though the QWERTY "
              "story is disputed. After an intermission of the Madison fleet's mileage, it shows Arrow's "
              "replacement effect and the inverted U, killer acquisitions in numbers, Q-learning price setters that "
              "learn to collude and punish deviations, antitrust's standards from Standard Oil to Google, and Baron "
              "and Myerson's regulator, then two dials, platform strategy, Ballmer's iPhone prediction as Called "
              "it?, and the frontier.",
        handoff="Part 45 turns from firms that look ahead to people who do not always: behavioural economics.",
        outside="Part 11: games and Markov strategies; Part 12: oligopoly and collusion; Part 22: discounting; Part "
                "43: demand and markups. Chapter 2 uses a contraction mapping and maximum likelihood; chapter 4 a "
                "Markov-perfect equilibrium; chapter 10 reinforcement learning; chapter 12 mechanism design.",
        objectives={
            "U": ["Explain the trade-off in replacing a machine, and why choices reveal costs.",
                  "Say why a platform may charge one side below cost, and when markets tip.",
                  "Describe how pricing algorithms can learn to collude without communicating."],
            "M": ["Set out Rust's model, its fixed point and the nested fixed point estimator.",
                  "Derive the CCP inversion with renewal, and say what it trades for speed.",
                  "Solve a two-type regulation problem and explain the virtual cost."],
            "D": ["Assess what dynamic and platform models identify, and what merger retrospectives show.",
                  "State the open questions about data, interoperability and foundation models."],
            "I": ["Apply platform pricing logic and merger screens to a case."],
        },
        results=[
            ("Rust's choice probability", r"P(\text{rebuild}\mid x) = \frac{e^{v_1}}{e^{v_0(x)} + e^{v_1}}"),
            ("The fixed point", r"EV(x) = \sum_j p_j \ln\big(e^{v_0(x+j)} + e^{v_1}\big)"),
            ("Hotz-Miller", r"\ln \frac{P_1(x)}{P_0(x)} = v_1 - v_0(x)"),
            ("Platform prices", r"p_i = c_i + \text{markup}_i - \alpha_j n_j"),
            ("Virtual cost", r"c_H + \tfrac{\nu}{1-\nu}(1-w)(c_H - c_L)"),
        ],
        U=(0, 1, 5, 6, 7, "s09_intermission", 8, 9, 10, 11), D=(13, 15), I=(14,),
        also=(("Agora's industrial organization", "explainer/economics/agora/io.py"),
              ("Rust's data", "explainer/economics/data/rust_buses.csv"),
              ("The Island's planted truths", "explainer/economics/island.py")),
    ),
    Part(
        n=45, level="U", widget="gym", prereq=(5, 7, 22, 42),
        question="What changes in economics when people are not the agents of Part 5?",
        story="The part opens on DellaVigna and Malmendier's gym: members on monthly contracts of over $70 who go "
              "4.3 times a month, paying over $17 a visit when a ten-visit pass cost $10. The Island's gym repeats "
              "it: naive members forecast 13.9 visits, make 4.7, and pay $15 a visit. DellaVigna's three departures "
              "frame the part; the viewer is given a mug and names a selling price, and the Island's mug market "
              "trades a quarter of its mugs instead of half. Prospect theory's kink, experienced traders, marathon "
              "runners bunched under round times (measured with Part 41's bunching estimator), putts for par against "
              "birdie at equal length, and loss-averse condominium sellers bracketed by two regressions follow. "
              "Present bias reverses plans; O'Donoghue and Rabin's naifs and sophisticates act at different times; "
              "a gym designs its contract for them. A randomized commitment account is taken mostly by "
              "sophisticates, and defaults stick for naifs who put off deciding; Save More Tomorrow turns the biases "
              "around. After an intermission of the American saving rate, shrouded add-ons survive competition, "
              "left-digit bias leaves steps in car prices, Fehr-Schmidt players reject low offers, markets cure some "
              "biases and feed on others, welfare is read where choices across frames agree, published nudges look "
              "six times larger than nudges in full, and models of limited minds explain inattention and "
              "forecasters who over-react individually while their average under-reacts. Three dials, practice and "
              "the frontier close it.",
        handoff="Part 46 turns to development: why the poor stay poor, and what actually helps.",
        outside="Part 5: preferences and revealed preference; Part 7: discounting and risk; Part 22: saving; Part 41: "
                "bunching; Part 42: defaults in social insurance; Psychology, Built, Part 26: prospect theory. "
                "Chapter 6 uses the Wald estimator; chapter 12 a selection model fitted by maximum likelihood; "
                "chapter 13 the Blahut-Arimoto iteration.",
        objectives={
            "U": ["Explain present bias, loss aversion and limited attention, each with a field example.",
                  "Say why demand for commitment reveals present bias and knowing it.",
                  "Explain why defaults matter and how Save More Tomorrow works."],
            "M": ["Derive the beta-delta reversal and O'Donoghue and Rabin's naif and sophisticate.",
                  "Estimate loss aversion from bunching and inattention from steps in prices.",
                  "Write the step-function selection model and correct a filtered literature."],
            "D": ["Assess what behavioural parameters are identified in the field, and how welfare can be judged "
                  "when choices conflict.",
                  "State the open questions in structural behavioural economics and behavioural macroeconomics."],
            "I": ["Design a product choice, a disclosure or a default, and say who gains and who loses."],
        },
        results=[
            ("Quasi-hyperbolic discounting", r"U_0 = u_0 + \beta \sum_{t \ge 1} \delta^t u_t"),
            ("Prospect theory's value", r"v(x) = x^{\alpha}\ (x \ge 0),\quad -\lambda(-x)^{\beta}\ (x < 0)"),
            ("The gym's visit price", r"p^{*} = m - (1 - \beta)\, b"),
            ("Left-digit inattention", r"\hat\theta = \frac{\text{jump}}{\text{jump} + \text{slope} \times "
                                       r"10{,}000}"),
            ("Fehr-Schmidt", r"U_i = x_i - \alpha \max(x_j - x_i, 0) - \beta \max(x_i - x_j, 0)"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, "s09_intermission", 8, 9, 10, 11), D=(14, 16), I=(15,),
        also=(("Agora's behavioural economics", "explainer/economics/agora/behave.py"),
              ("Prospect theory's functions", "explainer/psychology/psyche/choice.py"),
              ("The Island's planted truths", "explainer/economics/island.py")),
    ),
]
