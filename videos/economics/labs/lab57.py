"""Lab 57: reading the economy in real time: revisions, seasonal adjustment, a nowcast on the Island and on American
data, recession signals, and the scoring of forecasts."""

from videos.coursekit import labs
from explainer.economics.agora import nowcast as N

TITLE = "Reading the economy in real time"
GOAL = ("Measure how much first estimates are revised, adjust a series for its seasons, nowcast a quarter as the data "
        "arrive, and score professional forecasts against a benchmark that takes no skill.")
TASKS = [
    "Run x11 on payrolls without the outlier step (robust=False). What happens to April's factor around 2020?",
    "Change the yield-curve probit's lead from 12 to 6 months. Does the fit improve?",
    "Score the professional forecasters with the pandemic quarters left in (score_spf(skip=())). What changes?",
]


def run(seed=0):
    lab = labs.Lab()
    R = N.revisions()
    lab.row("GDP growth, first against latest: mean revision, mean absolute, sign changes",
            f"{R['mean_rev']:+.2f}, {R['mae']:.2f}, {R['sign_flips']} of {R['n']}")
    p8 = R["path_2008q4"]
    lab.row("2008Q4: first estimate, latest", f"{p8[0]['growth']:.1f}, {p8[-1]['growth']:.1f}")
    S = N.seasonal_payrolls()
    lab.row("payrolls: s.d. of monthly changes, unadjusted and adjusted (thousands)",
            f"{S['sd_nsa_change']:.0f}, {S['sd_off_change']:.0f}")
    lab.row("simplified X-11 against the BLS: monthly changes apart before 2020; after, with and without outlier step",
            f"{S['rms_robust_pre']:.0f}; {S['rms_robust_post']:.0f} and {S['rms_raw_post']:.0f}")
    I = N.island_nowcast(quarters=200, seed=57 + seed)
    lab.row("Island nowcast errors by release", ", ".join(f"{x:.2f}" for x in I["rmse"]))
    assert I["rmse"][-1] < I["rmse"][0]
    B = N.bridge_nowcast()
    lab.row("American GDP: bridge-equation errors before, month 1, 2, 3",
            f"{B['rmse_ar']:.2f}, {B['rmse_m1']:.2f}, {B['rmse_m2']:.2f}, {B['rmse_m3']:.2f}")
    P = N.yield_curve_probit()
    lab.row("yield-curve probit: coefficients; area under the ROC curve",
            f"{P['b'][0]:.2f}, {P['b'][1]:.2f}; {P['auc']:.2f}")
    Sa = N.sahm_rule()
    lab.row("Sahm rule in real time: signals, and those with no recession near",
            f"{len(Sa['rt_triggers'])}; {', '.join(t['month'] for t in Sa['rt_triggers'] if t['recession'] is None)}")
    Sc = N.score_spf()
    for r in Sc["rows"]:
        lab.row(f"SPF, {r['h']} quarters ahead: RMSE, the average's, Diebold-Mariano p",
                f"{r['rmse']:.2f}, {r['rmse_mean']:.2f}, {r['dm_p']:.3f}")
    G = N.greenbook_vs_spf()
    lab.row("inflation, 4 quarters ahead: the staff's RMSE, the SPF's", f"{G['rows'][-1]['rmse_gb']:.2f}, "
            f"{G['rows'][-1]['rmse_spf']:.2f}")
    Rg = N.regime_forecasts(seed=57 + seed)
    lab.row("Hamilton's economy: best forecasts a year ahead below zero; quarters below zero",
            f"{100 * Rg['rows'][-1]['share_neg']:.0f}%; {100 * Rg['share_neg_growth']:.0f}%")

    lab.note = ("First estimates are guesses; seasonal factors can invent; nowcasts improve with each release; "
                "signals cry wolf; and a year ahead the best forecasts are close to the average of the past.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    h = [r["h"] for r in Sc["rows"]]
    ax[0].plot(h, [r["rmse"] for r in Sc["rows"]], "o-", color=labs.ORANGE, label="SPF")
    ax[0].plot(h, [r["rmse_mean"] for r in Sc["rows"]], "s--", color=labs.PURPLE, label="ten-year average")
    ax[0].set(title="forecast errors by horizon", xlabel="quarters ahead", ylabel="RMSE, points")
    ax[0].legend()
    ax[1].plot(range(len(I["rmse"])), I["rmse"], "o-", color=labs.GREEN)
    ax[1].set(title="Island nowcast errors by release", xlabel="release", ylabel="RMSE")
    lab.fig = fig
    return lab
