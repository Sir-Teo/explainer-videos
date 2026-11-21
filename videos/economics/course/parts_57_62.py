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
]
