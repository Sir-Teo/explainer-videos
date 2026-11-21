"""Lab 61: the platform: surge pricing on a busy night, the commission in a two-sided market, ranking and
reputation, quality-scored ad auctions, what search ads return, experiments with peeking, variance reduction and
interference, uplift and the surrogate index, flexible work, and what a free service is worth."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import platform as PL

TITLE = "The platform"
GOAL = ("Run the Island's ride-hailing app and marketplace: set the surge and the commission, sell its ads, test its "
        "changes, and check each answer against the truth the Island knows.")
TASKS = [
    "Make drivers slower to respond to the surge (PL.surge_night(True, {'lag': 15})). What happens to the completion "
    "rate and the peak multiplier?",
    "Raise drivers' outside wage to $25 (PL.commission(params={'w0': 25.0})). How does the platform's best commission "
    "move, and why?",
    "Make regulars a smaller share of searchers (PL.search_ads(frequent=0.1, reps=50)). What happens to the gap "
    "between the dashboard's return and the truth?",
]


def run(seed=0):
    lab = labs.Lab()
    on, off = PL.surge_night(True), PL.surge_night(False)
    lab.row("New Year's Eve: requests completed at the peak, surge off and on; the peak multiplier",
            f"{100 * off['rate_peak']:.0f}%, {100 * on['rate_peak']:.0f}%; {max(on['m']):.2f}x")
    S = PL.surge_surplus(seed=61 + seed)
    lab.row("surge's surplus: consumer surplus per dollar; the elasticity at the normal fare",
            f"${S['cs_per_dollar']:.2f}; {S['elasticity_at_base']:.2f}")
    C = PL.commission()
    i10, i30 = C["c"].index(0.1), C["c"].index(0.3)
    lab.row("the commission: the platform's best; its take at 10% and 30% ($ an hour)",
            f"{100 * C['best_c']:.0f}%; ${C['platform'][i10]:.0f}, ${C['platform'][i30]:.0f}")
    both = [C["rider_cs"][i] + C["driver_surplus"][i] for i in (i10, i30)]
    lab.row("riders' and drivers' surplus at 10% and 30% ($ an hour)", f"${both[0]:,.0f}, ${both[1]:,.0f}")
    Rk = PL.ranking()
    lab.row("ranking: attention, top slot over fifth; clicks per search, organic and with a sponsored top slot",
            f"{Rk['top_vs_fifth']:.2f}; {Rk['total']:.2f}, {Rk['total_sponsored']:.2f}")
    Rp = PL.reputation(seed=61 + seed)
    lab.row("reputation: median percent positive; correlation with quality, percent positive and effective",
            f"{100 * Rp['pp_median']:.1f}%; {Rp['corr_pp']:.2f}, {Rp['corr_epp']:.2f}")
    G = PL.gsp()
    lab.row("ad auction: revenue per search, ranked by bid and by bid x quality",
            f"${G['bid only']['revenue']:.3f}, ${G['quality']['revenue']:.3f}")
    A = PL.search_ads(reps=60, seed=61 + seed)
    assert A["experiment_roi"] - 3 * A["experiment_sd"] / np.sqrt(60) < A["true_roi"]   # the experiment is centred
    lab.row("search ads: the dashboard's return, a regression's, the experiment's, the truth",
            f"{100 * A['attributed_roi']:,.0f}%, {100 * A['ols_roi']:,.0f}%, {100 * A['experiment_roi']:.0f}%, "
            f"{100 * A['true_roi']:.0f}%")
    Pk = PL.peeking(reps=1000, seed=61 + seed)
    lab.row("A/A tests 'significant': read once at the end, read every day", f"{100 * Pk['last']:.1f}%, "
            f"{100 * Pk['ever']:.1f}%")
    Cu = PL.cuped(reps=300, seed=61 + seed)
    lab.row("CUPED: variance ratio, against 1 - rho^2", f"{Cu['ratio']:.2f}, {Cu['predicted']:.2f}")
    Sw = PL.switchback(reps=100, seed=61 + seed)
    lab.row("a rider discount: by user, switchback, by city, the truth (rides per 100 riders)",
            f"{100 * Sw['user']:.1f}, {100 * Sw['switchback']:.1f}, {100 * Sw['city']:.1f}, {100 * Sw['truth']:.1f}")
    U = PL.uplift(seed=61 + seed)
    lab.row("coupons: extra purchases per 100, to the likeliest buyers, at random, by estimated effect",
            ", ".join(f"{100 * U['gains'][k]:+.1f}" for k in ("likeliest buyers", "at random", "estimated effect")))
    L = PL.long_term(seed=61 + seed)
    lab.row("a discount: first month, the surrogate index, the year's truth",
            f"{100 * L['short']:+.0f}%, {100 * L['surrogate']:+.1f}%, {100 * L['truth']:+.1f}%")
    F = PL.flexibility(seed=61 + seed)
    lab.row("drivers' surplus a day: flexible hours, a fixed shift", f"${F['flex']:.0f}, ${F['fixed']:.0f}")
    W = PL.wta_survey(seed=61 + seed)
    lab.row("free search: the median value from a willingness-to-accept survey (planted $15,000)",
            f"${W['median_hat']:,.0f}")
    e = data.fred("ECOMPCTSA")
    lab.row("online sales, share of American retail: first and latest quarters",
            f"{e['value'][0]:.1f}% ({e['date'][0][:7]}), {e['value'][-1]:.1f}% ({e['date'][-1][:7]})")

    lab.note = ("A platform is a market with an owner: every number above is a choice of that owner, and every "
                "measurement of it is only as good as the comparison behind it.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    cs = np.array(C["c"]) * 100
    ax[0].plot(cs, C["platform"], color=labs.ORANGE, label="platform")
    ax[0].plot(cs, C["rider_cs"], color="tab:blue", label="riders")
    ax[0].plot(cs, C["driver_surplus"], color="tab:olive", label="drivers")
    ax[0].axvline(100 * C["best_c"], color="k", lw=1, ls="--")
    ax[0].set(title="the commission", xlabel="commission, %", ylabel="$ an hour")
    ax[0].legend(frameon=False)
    ax[1].plot(on["t"], on["requests"], label="requests, surge on")
    ax[1].plot(off["t"], off["demand"], ls="--", label="requests, surge off")
    ax[1].plot(on["t"], on["drivers"], label="drivers, surge on")
    ax[1].plot(off["t"], off["drivers"], label="drivers, surge off")
    ax[1].set(title="New Year's Eve on the Island", xlabel="minutes after 11 pm", ylabel="a minute")
    ax[1].legend(frameon=False, fontsize=8)
    lab.fig = fig
    return lab
