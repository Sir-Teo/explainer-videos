"""Lab 55: identifying macro: the Island's structural VAR identified five ways against the truth, local projections
against VARs, a small New Keynesian model's Kalman likelihood and a short Metropolis-Hastings run, and the regions'
missing intercept."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import fiscal
from explainer.economics.agora import macrometrics as MM
from explainer.economics.island import truths

TITLE = "Identifying macro"
GOAL = ("Identify a monetary shock in a history where the truth is known, five ways, and see which assumptions recover "
        "it; then estimate a small model of the whole economy and find out what its data can and cannot say.")
TASKS = [
    "Make the proxy noisier (proxy_noise 3.0 in svar_simulate). How does the instrument's estimate change?",
    "Let the monetary shock's variance barely change (meeting_sd 1.2). What happens to the variance scheme?",
    "Estimate the New Keynesian model with only inflation observed (obs=(1,)). Which posteriors are still informative?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(55)
    S = T["svar"]
    o = MM.schemes_one(S["T"], S["seed"] + seed, S["p"], S["h"])
    tr = o["truth"]["monetary"]
    lab.row("truth: inflation and output on impact, per point of the rate", f"{tr['pi'][0]:.3f}, {tr['y'][0]:.3f}")
    for m in ("recursive", "proxy", "hetero"):
        lab.row(f"{m}: inflation and output on impact", f"{o[m]['pi'][0]:.3f}, {o[m]['y'][0]:.3f}")
    lab.row("sign restrictions: candidates kept, of tried", f"{o['sign']['accepted']} of {o['sign']['tried']}")
    lab.row("long run: supply's permanent effect on output (truth)",
            f"{o['long_run']['y'][-1]:.3f} ({o['truth']['supply']['y'][-1]:.3f})")
    assert abs(o["recursive"]["pi"][0]) < 1e-9

    mc = MM.schemes_mc(reps=60, seed=2000 + seed)
    for m in ("recursive", "proxy", "hetero"):
        lab.row(f"60 histories, {m}: inflation on impact, mean", f"{mc['methods'][m]['pi']['mean'][0]:.3f}")
    assert abs(mc["methods"]["proxy"]["pi"]["mean"][0] - tr["pi"][0]) < 0.05

    lp = MM.lp_var_mc(reps=80, seed=3000 + seed)
    for m in ("var1", "var4", "lp"):
        d = lp["methods"][m]
        lab.row(f"{m}: output at 16 quarters, mean and s.d. (truth {lp['truth'][-1]:.3f})",
                f"{d['mean'][-1]:.3f}, {d['sd'][-1]:.3f}")

    N = T["nk"]
    D = MM.nk_simulate(T=N["T"], seed=N["seed"])
    ll0 = MM.nk_loglik(MM.NK_DEFAULT, D["Y"])
    ll1 = MM.nk_loglik({**MM.NK_DEFAULT, "kappa": 0.3}, D["Y"])
    lab.row("Kalman log likelihood at the truth, and with kappa 0.3", f"{ll0:.1f}, {ll1:.1f}")
    assert ll0 > ll1
    post = MM.nk_mh(D["Y"], draws=600, burn=200, seed=seed)
    means = [f"{n} {post['chain'][:, j].mean():.2f} ({post['truth'][j]})" for j, n in enumerate(post["names"])]
    lab.row("a short Metropolis-Hastings run: posterior means (truth)", ", ".join(means))

    G = fiscal.regions(**T["regions"])
    lab.row("regions: relative multiplier with year effects; the nation's", f"{G['b_fe']:.2f}; {G['b_nat']:.2f}")

    lab.note = ("Timing is wrong when the bank knows more than the ordering allows; an outside instrument and a change "
                "in variance recover the truth; projections trade bias for noise; a whole model can be estimated, but "
                "only the data that move a parameter can teach anything about it; regions answer a relative question.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    h = np.arange(len(tr["pi"]))
    ax[0].plot(h, tr["pi"], color="white", label="truth")
    for m, c in (("recursive", labs.PURPLE), ("proxy", labs.ORANGE), ("hetero", labs.GREEN)):
        ax[0].plot(h, mc["methods"][m]["pi"]["mean"], color=c, label=m)
    ax[0].set(title="inflation after a one-point rise, 60 histories", xlabel="quarters")
    ax[0].legend()
    for m, c in (("var1", labs.PURPLE), ("var4", labs.GREEN), ("lp", labs.ORANGE)):
        d = lp["methods"][m]
        ax[1].plot(h, d["mean"], color=c, label=m)
        ax[1].fill_between(h, d["lo"], d["hi"], color=c, alpha=0.15)
    ax[1].plot(h, lp["truth"], color="white", label="truth")
    ax[1].set(title="output: projections against VARs", xlabel="quarters")
    ax[1].legend()
    lab.fig = fig
    return lab
