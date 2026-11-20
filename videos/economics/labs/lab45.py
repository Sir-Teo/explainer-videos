"""Lab 45: behavioural economics on the Island: the gym and the contract designed for present-biased members, the
mug market and loss aversion, bunching at round finishing times, present bias with naifs and sophisticates, a
randomized commitment account, defaults, left-digit bias, Fehr-Schmidt players, a literature filtered by
significance and its correction, and forecasters who over- and under-react."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import behave
from explainer.economics.island import truths

TITLE = "Behavioural economics"
GOAL = ("Measure what present bias costs gym members and how a gym prices for it; see loss aversion halve trade and "
        "bunch runners under round times; tell naifs from sophisticates; estimate the effect of a commitment account "
        "on those who take it; recover inattention from steps in prices; and undo a literature's publication filter.")
TASKS = [
    "The gym: make every member sophisticated (naive_share = 0). How do the share on monthly contracts and the price "
    "paid per visit change, and why?",
    "Bunching: raise loss aversion from 2.25 to 3. How does the excess mass under four hours change, and how would you "
    "turn it back into lambda?",
    "Nudges: let journals publish insignificant trials half the time (gamma = 0.5). How far is the published mean from "
    "the truth now, and does the selection model still recover it?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(45)

    G = T["gym"]
    g = behave.island_gym(n=2000, fee=G["fee"], per_visit=G["per_visit"], N=G["N"], C=G["C"], b_mean=G["b_mean"],
                          b_sd=G["b_sd"], beta_lo=G["beta_lo"], beta_hi=G["beta_hi"], naive_share=G["naive_share"],
                          busy=G["busy"], seed=G["seed"] + seed)
    lab.row("gym: share monthly; visits forecast and made; price per visit",
            f"{100 * g['share']['monthly']:.0f}%; {g['monthly_forecast']:.1f} and {g['monthly_visits']:.1f}; "
            f"${g['price_per_visit']:.2f}")
    assert g["price_per_visit"] > G["per_visit"]
    c = behave.gym_contract(0.7, 1.0, G["b_mean"], G["C"], G["N"], G["m"])
    lab.row("the gym's contract for a naif (beta 0.7): price of a visit, fee, member's real gain",
            f"${c['p']:.2f}, ${c['F']:.2f}, ${c['realized_surplus']:.2f}")

    M = T["mugs"]
    m0 = behave.mug_market(M["n"], 1.0, 1.0, M["mu"], M["sigma"], 1000, M["seed"] + seed)
    m1 = behave.mug_market(M["n"], M["lam_goods"], 1.0, M["mu"], M["sigma"], 1000, M["seed"] + seed)
    lab.row("mugs: share traded without and with loss aversion; ask/bid ratio",
            f"{100 * m0['share_traded']:.0f}%, {100 * m1['share_traded']:.0f}%; {m1['ratio']:.2f}")

    R = T["marathon"]
    mr = behave.marathon(n=200_000, k=R["k"], eta=R["eta"], lam=R["lam"], base=R["base"], friction=R["friction"],
                         seed=R["seed"] + seed)
    b240 = behave.bunching_at(mr["T"], 240.0)
    lab.row("marathon: excess and missing mass at 4:00 (minutes); planted", f"{b240['excess']:.2f}, "
            f"{b240['missing']:.2f}; {mr['extra_minutes']:.2f}")

    O = T["odr"]
    oc, orw = behave.odr(O["values"], O["beta"], "cost"), behave.odr(O["values"], O["beta"], "reward")
    lab.row("O'Donoghue-Rabin weeks (time-consistent, naif, sophisticate): report; film",
            f"{oc['tc']}, {oc['naif']}, {oc['soph']}; {orw['tc']}, {orw['naif']}, {orw['soph']}")

    S = T["seed"]
    st = behave.commitment_trial(n=S["n"], soph_share=S["soph_share"], flex_mean=S["flex_mean"],
                                 flex_sd=S["flex_sd"], seed=S["seed"] + seed)
    lab.row("commitment: take-up; effect of the offer; effect on takers", f"{100 * st['take_up']:.0f}%; "
            f"{st['itt']:.1f}; {st['tot']:.1f}")

    C = T["cars"]
    u = behave.used_cars(n=200_000, theta=C["theta"], seed=C["seed"] + seed)
    lab.row("left digits: theta planted and estimated", f"{C['theta']:.2f}, {u['theta_hat']:.2f}")

    N = T["nudges"]
    lit = behave.nudge_literature(N["k"], N["mu"], N["tau"], N["control"], *N["journal_n"], N["gamma"],
                                  N["seed"] + seed)
    pub = np.array(lit["published"])
    fit = behave.selection_mle(np.array(lit["x"])[pub], np.array(lit["se"])[pub])
    lab.row("nudges: truth; published mean; selection-model estimate", f"{N['mu']:.2f}; "
            f"{lit['mean_published']:.2f}; {fit['mu']:.2f}")
    assert lit["mean_published"] > N["mu"]

    F = T["forecast"]
    fr = behave.forecasters(T=F["T"], n=F["n"], rho=F["rho"], sd_signal=F["sd_signal"], theta=0.0, seed=F["seed"])
    fd = behave.forecasters(T=F["T"], n=F["n"], rho=F["rho"], sd_signal=F["sd_signal"], theta=F["theta"],
                            seed=F["seed"])
    lab.row("forecasters: individual and consensus slopes, rational; diagnostic",
            f"{fr['individual']:+.2f}, {fr['consensus']:+.2f}; {fd['individual']:+.2f}, {fd['consensus']:+.2f}")
    assert fd["individual"] < fr["individual"]

    lab.note = ("Members who forecast like Part 5's agents pay for being someone else; loss aversion halves trade and "
                "bunches runners at round times; commitment is taken by those who know their bias; inattention "
                "leaves steps in prices; and a literature filtered by significance overstates, by a margin a model of "
                "the filter can largely undo.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    e = np.array(mr["edges"])
    ax[0].bar((e[:-1] + e[1:]) / 2, mr["h"], width=1.0, color=labs.ORANGE)
    ax[0].set(title="finishing times on the Island", xlabel="minutes", xlim=(180, 330))
    ax[1].scatter(np.array(lit["x"])[pub], np.array(lit["se"])[pub], s=6, color=labs.BLUE)
    se = np.linspace(0, 3.5, 50)
    ax[1].plot(1.96 * se, se, color="red")
    ax[1].axvline(N["mu"], color="black", lw=1)
    ax[1].set(title="a filtered literature", xlabel="estimate (points)", ylabel="standard error")
    lab.fig = fig
    return lab
