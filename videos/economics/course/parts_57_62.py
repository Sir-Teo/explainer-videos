"""Act XI, Economics at Work (Parts 57-62)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=57, level="U", widget="nowcaster", prereq=(1, 3, 4, 28, 31, 55),
        question="What is the economy doing right now, and how good is anyone's guess about next year?",
        story="Two scorecards open the part: Samuelson's nine alarms for five recessions, and An, Jalles and "
              "Loungani's 5 of 153 recessions foreseen a year ahead. GDP's first estimates against today's since 1965 "
              "(an average revision of about a point and a half, 2008Q4 from -3.8 to -8.5) and payrolls' benchmark "
              "revisions; seasonal adjustment by a simplified X-11 on payrolls, which can invent an April slump out "
              "of 2020 unless extremes are left out. The viewer nowcasts an Island quarter release by release. "
              "Bridge equations on American data and a factor model with the Kalman filter; the yield curve's probit "
              "and the Sahm rule, with their false alarms of 2022-24; the professional forecasters scored by horizon "
              "against the average of the past, and the Federal Reserve staff against them on inflation. After an "
              "intermission of the anxious index since 1968, why the best forecast a year ahead is never a "
              "recession; new data, text as data, combinations and scenarios, fan charts, a new Dial of forecast "
              "errors, the Sahm call of 2024, and the frontier.",
        handoff="Part 58 turns from reading the economy to pricing a policy: cost-benefit analysis and scoring a "
                "bill.",
        outside="Part 1: the 2008 forecast; Part 3: how GDP is measured; Part 4: evidence and the Lucas critique; "
                "Part 28: the 2021 inflation projection; Part 31: real-time output gaps; Part 55: VARs and the "
                "Kalman filter; Statistics, Built: time series, state-space models and forecast evaluation.",
        objectives={
            "U": ["Explain why a first estimate of GDP or payrolls is revised, and what seasonal adjustment does.",
                  "Read a nowcast and a recession probability, and say how often such signals have been wrong."],
            "M": ["Build a bridge-equation nowcast with a ragged edge, and a factor-model nowcast by the Kalman "
                  "filter.",
                  "Score forecasts by horizon against a benchmark with Diebold and Mariano's test, and combine them "
                  "by Bates and Granger's weights.",
                  "Estimate a yield-curve probit and compute the Sahm rule in real time."],
            "D": ["Show why squared-error-optimal forecasts of a rare regime almost never predict it, in Hamilton's "
                  "model.",
                  "Design a fair real-time evaluation: vintages, first releases, overlapping errors."],
            "I": ["Write the weekly note of a forecasting desk: the number, the range, the news in each release, "
                  "and what would change the call."],
        },
        results=[
            ("Forecast error", r"e_t = f_t - a_t, \quad \text{RMSE} = \sqrt{\tfrac1n \textstyle\sum e_t^2}"),
            ("Diebold and Mariano", r"\text{DM} = \bar d / \widehat{\text{se}}_{\text{HAC}}(\bar d), \quad "
                                    r"d_t = e_{A,t}^2 - e_{B,t}^2"),
            ("Bates and Granger", r"w^* = \frac{\sigma_2^2 - \sigma_{12}}{\sigma_1^2 + \sigma_2^2 - 2\sigma_{12}}"),
            ("A dynamic factor model", r"x_{it} = \lambda_i f_t + e_{it}, \quad f_t = \phi f_{t-1} + \eta_t"),
            ("The Sahm rule", r"\bar u_t - \min_{t-12 \le s < t} \bar u_s \ge 0.5"),
        ],
        U=(0, 1, 2, 3, 5, "s09_intermission", 12), D=(8, 15), I=(4, 6, 11, 14),
        also=(("Agora's nowcasting module", "explainer/economics/agora/nowcast.py"),
              ("The Data Room", "explainer/economics/data")),
    ),
    Part(
        n=58, level="U", widget="appraiser", prereq=(3, 15, 18, 23, 41, 42, 48, 50),
        question="How does a government decide whether a project or a law is worth it?",
        story="The Flood Control Act of 1936 tells the Army's engineers to build only where the benefits, 'to "
              "whomsoever they may accrue', exceed the costs, and Dupuit had asked in 1844 what a bridge is worth. The "
              "Island's case: a bridge across the strait, where Bo's ferry runs. Its ledger is built step by step: "
              "the counterfactual and standing; Dupuit's surplus and the rule of a half; fares that net out against "
              "Bo's lost profit; shadow wages and the cost of public funds; time, road noise priced from house sales, "
              "a beach from the trips to it, birds from surveys; a statistical life from the wage premium for risk, "
              "biased by unseen ability. The viewer scores a higher top rate (143 million static, 101 with behaviour). "
              "Discounting decides the bridge (+139 at 3%, -118 at 7%): the Green Book's Ramsey rate and its 2026 cut, "
              "OMB's rates, Weitzman. Budget scoring, the window and its sunsets, a dynamic toy, and CBO's own record "
              "since 1984; after an intermission of forty-two baselines against the deficits that happened, "
              "microsimulation and the distribution table, a small CGE and NAFTA's audited models, megaprojects' "
              "overruns and the outside view (the bridge's forecast +77 becomes a 61% chance of loss), the option to "
              "wait, a regulatory impact analysis, Goodhart's and Campbell's laws, two new Dials, the scorekeepers, "
              "the Sydney Opera House, and weights and wellbeing.",
        handoff="Part 59 takes economics into the courtroom: market definition, diversion ratios and merger "
                "simulation under cross-examination.",
        outside="Part 3: the social accounting matrix; Part 15: externalities and the value of the environment; Part "
                "18: welfare and the value of a statistical life; Part 23: the option to wait; Part 41: taxes and the "
                "elasticity of taxable income; Part 42: the MVPF; Part 48: the social cost of carbon; Part 50: the "
                "policy memo; Statistics, Built: regression and its biases.",
        objectives={
            "U": ["List the steps of a cost-benefit analysis, and say what the counterfactual and standing are.",
                  "Compute consumer surplus with the rule of a half, and explain why transfers net out.",
                  "Explain why the discount rate can decide a long-lived project, and what the agencies use."],
            "M": ["Estimate a hedonic price and a value of a statistical life, and name the biases in each.",
                  "Score a tax change statically and with an elasticity of taxable income, on a weighted survey.",
                  "Build a distribution table from a microsimulation, and a small CGE from a social accounting "
                  "matrix."],
            "D": ["Derive Saez's revenue ratio, Weitzman's declining rate and the value of the option to wait.",
                  "Judge an appraisal's forecasts against a reference class, and the sources of optimism bias."],
            "I": ["Write the break-even sentence and the tornado chart an appraisal or a regulatory analysis needs, "
                  "and read a budget office's score and its record."],
        },
        results=[
            ("Net present value", r"NPV = \sum_{t} \frac{B_t - C_t}{(1 + r)^t}"),
            ("The rule of a half", r"\Delta CS = q_0 (g_0 - g_1) + \tfrac12 (q_1 - q_0)(g_0 - g_1)"),
            ("Ramsey's rate", r"r = \delta + \eta\, g"),
            ("Saez's revenue ratio", r"\frac{dR}{dR_{\text{static}}} = 1 - e\, a\, \frac{\tau}{1 - \tau}"),
            ("Weitzman's rate", r"\bar P_t = \textstyle\sum_i p_i (1 + r_i)^{-t}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, "s09_intermission", 12), D=(9, 15), I=(7, 8, 11, 14),
        also=(("Agora's appraisal module", "explainer/economics/agora/appraisal.py"),
              ("The Data Room: CBO's projections", "explainer/economics/data")),
    ),
    Part(
        n=59, level="M", widget="expert", prereq=(4, 10, 12, 38, 43, 44),
        question="How is economics used to decide a merger, and what survives cross-examination?",
        story="Staples and Office Depot say they compete with everyone who sells a pen; the FTC answers with their "
              "own prices, and in 1997 the court stops the merger. The Island has its own version: Alder in every "
              "town, Birch and Cedar in some, and a proposed merger of Alder and Birch whose true effect is known. "
              "Section 7 and the burden of proof; the viewer decides which of three pairs is one market, by diversion "
              "against the critical value X/(X + M); the hypothetical monopolist, critical loss and the cellophane "
              "trap; the HHI's lines of 1982, 2010 and 2023; upward pricing pressure derived, GUPPIs against a "
              "simulation; four demand curves fitted to the same numbers predicting rises from 6.4% to 22.5%, and an "
              "agency's plain logit that predicts 6.9% against a truth of 11.9%; pass-through, Staples' 15-17% "
              "against a claimed two-thirds, and Cedar's discipline. After an intermission of airline fares since "
              "1964, the AT&T-Time Warner bargaining model and the departure rate that decides it; a cartel's "
              "variance screen, overcharge and damages; the price regression under cross-examination; a hospital "
              "merger that lowers nurses' wages; the retrospective that scores the tools; rate cases, price caps and "
              "access pricing; two Dials, the profession, AT&T's bet, and FTC v. Meta.",
        handoff="Part 60 turns from judging prices in court to setting them: willingness to pay, price experiments, "
                "revenue management and dynamic pricing.",
        outside="Part 4: regression and its biases; Part 10: the price maker and Averch-Johnson; Part 12: oligopoly "
                "and collusion; Part 38: monopsony; Part 43: demand estimation and merger simulation; Part 44: "
                "vertical relations and antitrust's standards; Statistics, Built: difference in differences and "
                "specification curves.",
        objectives={
            "U": ["State what section 7 of the Clayton Act asks, and how the burden of proof moves in a merger case.",
                  "Run the hypothetical-monopolist test with critical loss, and explain the cellophane trap.",
                  "Compute the HHI and its rise, and apply the guidelines' presumptions."],
            "M": ["Derive upward pricing pressure from the merged firm's first-order condition, and compute GUPPIs "
                  "from diversion ratios and margins.",
                  "Explain why merged firms pass on less of a cost saving, and how pass-through is measured.",
                  "Estimate a cartel's overcharge and damages with a before-during-after regression."],
            "D": ["Show how the curvature of demand drives a simulated price effect, and why a misspecified "
                  "substitution pattern biases it.",
                  "Derive the fee change in a Nash-bargaining model of a vertical merger."],
            "I": ["Defend a price regression under cross-examination: specifications, influence, subsamples, and "
                  "what Daubert asks of a method."],
        },
        results=[
            ("Critical loss", r"L^{*} = \frac{X}{X + M}"),
            ("Critical diversion", r"D > \frac{X}{X + M}"),
            ("The rise in the HHI", r"\Delta\text{HHI} = 2\, s_A s_B"),
            ("Upward pricing pressure", r"\text{UPP}_A = D_{AB}(p_B - c_B) - E_A c_A"),
            ("The bargaining fee change", r"\Delta f = w\, d\, s\, m"),
        ],
        U=(0, 1, 2, 3, 4, 5, "s09_intermission", 9, 11, 12), D=(6, 8, 16), I=(10, 13, 15),
        also=(("Agora's merger module", "explainer/economics/agora/merger.py"),
              ("The Data Room: airline fares in the CPI", "explainer/economics/data")),
    ),
]
