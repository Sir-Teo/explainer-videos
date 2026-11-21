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
]
