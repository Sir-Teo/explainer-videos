"""Lab 46: development on the Island: a poverty trap and the transfers that break it, Lewis's turning point, the
moneylender's rate and a randomized microlender, the village multiplier, Townsend's test, deworming's spillover,
Duflo's Wald ratio, fertilizer offers for present-biased farmers, heterogeneous sites, and the aid budget."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import village
from explainer.economics.island import truths

TITLE = "Development"
GOAL = ("Find a poverty trap's threshold and see which transfers break it; read a lender's rate as cost; see where a "
        "microlender's gains fall; test village insurance; measure a spillover; turn a difference in differences into "
        "a return to schooling; time an offer to present-biased farmers; and spend an aid budget at the margin.")
TASKS = [
    "The trap: lower the fixed cost from 11 to 9. Where do the steady states and the threshold move, and how many "
    "households escape with no transfer at all?",
    "Credit: let 30% of businesses have high returns instead of 15%. How do the average effect, the effect per "
    "borrower and the top quantile effect change?",
    "Sites: raise the trials' standard error from 0.05 to 0.15. How does the shrinkage change, and the interval for "
    "the next site?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(46)
    tech = {k: T["trap"][k] for k in ("a_low", "a_high", "alpha", "fixed")}
    Tr = T["trap"]

    ss = village.trap_steady_states(s=Tr["s"], delta=Tr["delta"], **tech)
    lab.row("the trap: low steady state, threshold, high steady state",
            f"{ss['low']:.1f}, {ss['threshold']:.1f}, {ss['high']:.1f}")
    shares = []
    for tr in (0.0, 5.0, 10.0, 20.0):
        h = village.trap_households(n=2000, T=Tr["T"], transfer=tr, k_mu=Tr["k_mu"], k_sd=Tr["k_sd"],
                                    shock_sd=Tr["shock_sd"], s=Tr["s"], delta=Tr["delta"], seed=Tr["seed"] + seed,
                                    **tech)
        shares.append(h["share_above_end"])
    lab.row("share above the threshold after 12 years, transfers 0, 5, 10, 20",
            ", ".join(f"{100 * x:.0f}%" for x in shares))
    assert shares[-1] > shares[0]

    L = village.lewis(**T["lewis"])
    lab.row("Lewis: the turning point (year); the wage in year 60", f"{L['turn']}; {L['wage'][-1]:.2f}")

    m = village.moneylender(**T["lender"])
    lab.row("the lender's rate: total; from defaults; from screening", f"{100 * m['rate']:.0f}%; "
            f"{100 * m['from_default']:.0f} points; {100 * m['from_monitoring']:.0f} points")
    C = village.microcredit_trial(**{**T["credit"], "n": 20000, "seed": T["credit"]["seed"] + seed})
    lab.row("microcredit: take-up; ITT on profits; per borrower; effect at the 95th percentile",
            f"{100 * C['take_up']:.0f}%; {C['itt']:.1f}; {C['tot']:.1f}; {C['qte'][-1]:.1f}")

    M = village.local_multiplier(**T["cash"])
    lab.row("the village multiplier: nominal, real", f"{M['multiplier']:.2f}, {M['real_multiplier']:.2f}")

    R = T["risk"]
    tw = village.townsend(pooled=R["pooled"], villages=R["villages"], households=R["households"], T=R["T"],
                          seed=R["seed"] + seed)
    lab.row("Townsend's slope with and without village-year effects (truth 0.15)",
            f"{tw['within']:.2f}, {tw['raw']:.2f}")

    w = village.deworming(**{**T["worms"], "seed": T["worms"]["seed"] + seed})
    lab.row("deworming: within-school; spillover; whole schools (points of absence)",
            f"{100 * w['within']:+.1f}; {100 * w['spillover']:+.1f}; {100 * w['between_schools']:+.1f}")

    d = village.inpres(**{**T["inpres"], "per_cell": 300, "seed": T["inpres"]["seed"] + seed})
    lab.row("schools: years per school; log wage per school; Wald (planted 0.08)",
            f"{d['school_per_school']:.3f}; {d['wage_per_school']:.4f}; {d['wald']:.3f}")

    f = village.fertilizer(**{**T["fert"], "seed": T["fert"]["seed"] + seed})
    lab.row("fertilizer: no offer; harvest offer; same offer later; half price later",
            f"{100 * f['base']:.0f}%; {100 * f['harvest_offer']:.0f}%; {100 * f['late_offer']:.0f}%; "
            f"{100 * f['planting_subsidy']:.0f}%")

    s = village.sites(**{**T["sites"], "seed": T["sites"]["seed"] + seed})
    lab.row("sites: mean; spread of true effects; interval for the next site",
            f"{s['mean']:.2f}; {s['tau_hat']:.2f}; {s['next_lo']:+.2f} to {s['next_hi']:+.2f}")

    P = {k: tuple(v) for k, v in T["aid"].items()}
    a = village.aid_allocate(P, budget=10.0, step=0.05)
    lab.row("the aid budget: best total; allocation (millions)", f"{a['total']:.2f}; " +
            ", ".join(f"{k} {v:.2f}" for k, v in a["alloc"].items()))

    lab.note = ("A fixed cost makes a threshold, and only transfers that push households across it last; the "
                "lender's high rate is mostly the cost of defaults and information; a microlender's gains sit in the "
                "top tail; a comparison within schools misses a spillover; timing does for fertilizer what a large "
                "subsidy does; and what one site's trial says about the next is limited by how much sites differ.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    k = np.linspace(0.5, 70, 400)
    ax[0].plot(k, village.trap_next(k, s=Tr["s"], delta=Tr["delta"], **tech), color=labs.ORANGE)
    ax[0].plot(k, k, color="black", lw=1, ls="--")
    ax[0].set(title="the trap: next year's capital", xlabel="capital this year", ylabel="capital next year")
    ax[1].plot(np.array(C["qs"]) * 100, C["qte"], color=labs.BLUE)
    ax[1].axhline(0, color="black", lw=1)
    ax[1].set(title="microcredit: quantile effects on profits", xlabel="percentile", ylabel="treated - control")
    lab.fig = fig
    return lab
