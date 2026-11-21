"""Lab 67: the next economics: a simulated research field with specification search and a publication filter, the
caliper ratio and Andrews and Kasy's selection model, replication and the winner's curse, forking paths, a
meta-study corrected for selection, many analysts and the specification curve, and the loss of stability in Brock
and Hommes's switching cobweb."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import field as F

TITLE = "The next economics"
GOAL = ("Build a research field in which the truth is known, see what search and selection do to what gets "
        "published, and test the tools that detect and correct them.")
TASKS = [
    "Switch off the publication filter (F.literature(publish_ns=1.0)). What happens to the caliper ratio, and to the "
    "replication rate?",
    "Let every researcher search (F.literature(search=1.0, tries=20)). How far can search alone push the caliper "
    "ratio, and what does the selection model's beta report?",
    "Make specifications nearly identical (F.false_positive([1, 5, 20], 0.95)). Why does searching them barely raise "
    "the false-positive rate?",
]


def run(seed=0):
    lab = labs.Lab()
    L = F.literature(n=40000, search=0.3, seed=67 + seed)
    clean = F.literature(n=40000, search=0.0, publish_ns=1.0, seed=67 + seed)
    c, c0 = F.caliper(L["z"], width=0.2), F.caliper(clean["z"], width=0.2)
    assert c["ratio"] > 2.0 > 1.2 > c0["ratio"]                       # selection leaves a bump at 1.96
    lab.row("caliper ratio at 1.96: the selected field, and with no search or filter",
            f"{c['ratio']:.2f} and {c0['ratio']:.2f}")
    sel = F.selection_mle(L["z"])
    assert sel["beta"] < 0.6 and F.selection_mle(clean["z"])["beta"] > 0.9
    lab.row("Andrews and Kasy's beta (relative publication of insignificant results)", f"{sel['beta']:.2f}")
    R = F.replicate(L, seed=seed)
    assert 0.4 < R["rate"] < 0.8 and R["ratio"] < 0.85
    lab.row("replication at 90% planned power: success rate, effect over the original",
            f"{100 * R['rate']:.0f}%, {100 * R['ratio']:.0f}%")
    fp = F.false_positive([1, 5, 20], 0.6, sims=10000, seed=seed + 1)
    assert abs(fp[0] - 0.05) < 0.01 and fp[0] < fp[1] < fp[2]
    lab.row("false positives with 1, 5 and 20 specifications (correlation 0.6)",
            ", ".join(f"{100 * x:.0f}%" for x in fp))
    M = F.meta_literature(theta=-0.01, tau=0.005, seed=676 + seed)
    A = F.ak_meta(M["est"], M["se"])
    naive = float(np.mean(M["est"]))
    assert abs(A["theta"] - M["theta"]) < abs(naive - M["theta"])          # the correction moves towards the truth
    lab.row("the meta-study: truth, published average, Andrews and Kasy", f"{M['theta']:.3f}, {naive:.3f}, "
            f"{A['theta']:.3f}")
    An = F.many_analysts()
    S = F.specification_curve()
    assert An["ratio"] > 1.5 and S["n_specs"] == 288
    lab.row("seven analysts: spread over the mean standard error; 288 specifications: range",
            f"{An['ratio']:.1f}; {S['lo']:.3f} to {S['hi']:.3f}")
    b, B = 1.35, 1.0
    n_star = (b - B) / (2 * b)
    beta_flip = np.log(1 / n_star - 1)
    lo, hi = F.brock_hommes([beta_flip - 0.3], T=2000, keep=50), F.brock_hommes([beta_flip + 0.5], T=2000, keep=50)
    assert np.ptp(lo["x"]) < 1e-6 < np.ptp(hi["x"])                     # stable below the flip, a cycle above
    lab.row("Brock and Hommes: the beta at which the steady state loses stability", f"{beta_flip:.2f}")

    lab.note = ("Search and selection leave fingerprints, a bump at the threshold and shrinking replications; the "
                "same models that make them can measure and partly undo them.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    bins = np.arange(0, 5.01, 0.1)
    ax[0].hist(L["z"], bins=bins, color=labs.ORANGE, alpha=0.8, label="published")
    ax[0].hist(L["first"], bins=bins, histtype="step", color="tab:blue",
               weights=np.full(len(L["first"]), len(L["z"]) / len(L["first"])), label="first tries (rescaled)")
    ax[0].axvline(1.96, color="tab:red", lw=1)
    ax[0].set(title="the camel", xlabel="|z|", ylabel="results")
    ax[0].legend(fontsize=8)
    est = np.array([r["est"] for r in S["rows"]])
    se = np.array([r["se"] for r in S["rows"]])
    k = np.arange(len(est))
    ax[1].fill_between(k, est - 1.96 * se, est + 1.96 * se, color="0.85")
    ax[1].plot(k, est, color="tab:blue")
    ax[1].axhline(An["ate"], color="tab:green", ls="--", label="effect among finishers")
    ax[1].set(title="the specification curve", xlabel="specification (sorted)", ylabel="estimate")
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab
