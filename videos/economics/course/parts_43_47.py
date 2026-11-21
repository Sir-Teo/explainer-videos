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
    Part(
        n=46, level="U", widget="aidbudget", prereq=(4, 20, 22, 45),
        question="Why do the poor stay poor, and what actually helps?",
        story="The part opens on Cohen and Dupas's bed nets: a price of about 60 cents, drawn at random at Kenyan "
              "clinics, cut demand by about 60%, and those who paid used their nets no more than those who did not. "
              "The Island's clinic repeats it. The World Bank's count of the poor, from a dollar a day to $3.00 at "
              "2021 prices, falls from 47% of the world in 1981 to 10% in 2024, mostly in East and South Asia; the "
              "viewer spends a ten-million-dollar aid budget across six programmes and learns to spend at the "
              "margin. A technology with a fixed cost gives the Island's households an S-shaped capital map, a "
              "threshold and a trap that only a large enough transfer breaks; Lewis's dual economy and the "
              "agricultural productivity gap, recomputed for 172 countries, follow. The moneylender's rate is mostly "
              "cost; a randomized microlender raises profits modestly, with the gains in the top tail. Cash: "
              "PROGRESA's randomized roll-out, GiveDirectly, a village multiplier of 2.5, and Uruguay's PANES "
              "households analysed here by regression discontinuity. The graduation programme in six countries and "
              "the threshold in the Island's data come before an intermission of world poverty. Then schools "
              "(Duflo's difference in differences and Wald ratio, learning poverty, Teaching at the Right Level), "
              "health (deworming's spillovers, the worm wars, Thornton's incentives analysed from her data), risk "
              "(Townsend's test, index insurance, a default in China's data), fertilizer and present bias, mobile "
              "money, management, the mita's boundary and the slave trades, and the debate over what experiments "
              "can teach, with twelve heterogeneous sites and China's growth. Three dials, practice and the "
              "frontier close it.",
        handoff="Part 47 turns from programmes that work to the governments that choose them: political economy.",
        outside="Part 4: difference in differences, instruments and regression discontinuity; Part 20: the Solow "
                "model; Part 22: saving and insurance; Part 27: the multiplier; Part 45: present bias and defaults; "
                "Statistics, Built: quantile treatment effects, the bootstrap and partial pooling.",
        objectives={
            "U": ["Explain how the world's poor are counted, and why prices change the count.",
                  "Say what makes a poverty trap, and why the size of a transfer matters in one.",
                  "Explain why the moneylender charges so much and why microcredit's average effect is small."],
            "M": ["Find the steady states of an S-shaped capital map and say which are stable.",
                  "Run Townsend's test and say why village-year effects are needed.",
                  "Compute a Wald estimate from a difference in differences, and a regression discontinuity."],
            "D": ["Assess the external validity of randomized trials with heterogeneous sites, and what scaling "
                  "changes.",
                  "State the open questions in measuring and targeting poverty with satellites and phones."],
            "I": ["Allocate a budget across programmes at the margin, and read a cost-effectiveness estimate."],
        },
        results=[
            ("The trap's dynamics", r"k_{t+1} = s\, f(k_t) + (1-\delta)\, k_t"),
            ("The lender's break-even rate", r"(1+i)(1-p) = 1 + r + m"),
            ("The village multiplier", r"1 + a + a^2 + \cdots = \tfrac{1}{1-a}"),
            ("Townsend's test", r"\Delta \log c_{ivt} = \beta\, \Delta \log y_{ivt} + \gamma_{vt} + e_{ivt}"),
            ("The best split", r"a_i\, e^{-x_i/s_i} = \lambda \ \text{for every funded programme}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, "s09_intermission", 8, 9, 10, 11, 12), D=(13, 16), I=(15,),
        also=(("Agora's village", "explainer/economics/agora/village.py"),
              ("The Island's planted truths", "explainer/economics/island.py")),
    ),
    Part(
        n=47, level="U", widget="buildlobby", prereq=(4, 11, 15, 18),
        question="Why do governments so often choose policies that economists can show are wasteful?",
        story="The part opens on Olken's roads: engineers took core samples from over 600 new village roads in "
              "Indonesia, and more than a fifth of the money was missing; announced audits cut that by about 8 "
              "points and village meetings did little, and the Island's 600 projects with the truth planted give "
              "the same answer. Olson's free riding follows, with a group's lobbying falling to nothing as it grows "
              "and America's sugar at twice the world price, about $500,000 a year for each of 4,000 farms against "
              "$9 for each consumer. The viewer plays build or lobby with a hundred tokens and finds that everyone "
              "ends with 104 instead of 340; Tullock's contest, Harberger's triangle and Krueger's rents in India and "
              "Turkey measure the waste. Voters come next: probabilistic voting, Lee, Moretti and Butler's affect or "
              "elect, and 1,297 Senate elections analysed here by regression discontinuity, where barely winning is "
              "worth 7.4 points next time. Capture (Stigler, Grossman and Helpman, Fisman's connections), the agency "
              "model with the Island's lame-duck mayors and Brazil's random audits, and Olken's results with why "
              "meetings failed lead to an intermission of the world's democracy index since 1900. Then corruption "
              "measured four ways and the World Bank's governance scores; Acemoglu and Robinson's franchise as a "
              "commitment, with the Island's elite and a map of revolution, democratization and promises; state "
              "capacity in taxes and democracy and growth; conflict with a rainfall instrument; media and "
              "persuasion; Nordhaus's political business cycle. Two dials, practice, the Treasury's 2016 forecast "
              "and a frontier of backsliding, populism and the digital state close it.",
        handoff="Part 48 turns from failures of government to a market failure the size of the planet: the climate.",
        outside="Part 4: regression discontinuity and instruments; Part 11: games and equilibrium; Part 14: agency and "
                "efficiency wages; Part 15: public goods and free riding; Part 18: voting and social choice; "
                "Statistics, Built: local linear regression and two-stage least squares.",
        objectives={
            "U": ["Explain why small groups with large stakes win against large groups with small ones.",
                  "Distinguish the Harberger triangle from the Tullock rectangle, and say why rents are competed "
                  "away.",
                  "Say what a close-election regression discontinuity identifies, and what it assumes."],
            "M": ["Solve a Tullock contest for equilibrium spending and dissipation, with equal or unequal players.",
                  "Derive the threshold of the Barro-Ferejohn agency model and say what lowers it.",
                  "Estimate a regression discontinuity by local linear regression and check it across bandwidths."],
            "D": ["Explain the commitment problem in Acemoglu and Robinson's model of the franchise, and when an "
                  "elite democratizes.",
                  "State the open questions about backsliding, populism and the digital state."],
            "I": ["Design an anti-corruption or anti-capture rule (publication, random audits, cooling-off, rules "
                  "over discretion) and say what it costs."],
        },
        results=[
            ("A group's lobbying", r"E^{*} = \sqrt{B K / n} - K"),
            ("Tullock's contest", r"x^{*} = R\, \tfrac{n-1}{n^2}, \quad n x^{*} = \tfrac{n-1}{n} R"),
            ("The agency threshold", r"r^{*} = (1-\delta)(W + R) - W"),
            ("The persuasion rate", r"f = \frac{y_T - y_C}{e_T - e_C} \cdot \frac{1}{1 - y_C}"),
            ("The close-election jump", r"\tau = \lim_{m \downarrow 0} E[y \mid m] - \lim_{m \uparrow 0} E[y \mid m]"),
        ],
        U=(0, 1, 2, 3, 4, 6, 7, "s09_intermission", 8, 12, 13), D=(9, 16), I=(15,),
        also=(("Agora's political economy", "explainer/economics/agora/politics.py"),
              ("The Island's planted truths", "explainer/economics/island.py")),
    ),
]
