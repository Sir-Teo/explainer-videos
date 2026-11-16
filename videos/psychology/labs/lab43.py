"""Lab 43: the capstone pipeline: a frozen plan, power and d33, a dry run on simulated labs, the confirmatory
analysis of two registered multi-lab replications, the verdict, and a labelled multiverse."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology import capstone as C
from explainer.psychology import opendata

TITLE = "The Replication"
GOAL = ("Freeze a plan, check its power and the small-telescopes benchmark, run it on simulated labs, then apply it "
        "once to the open data of the verbal-overshadowing and ego-depletion replications, judge the results by the "
        "registered criteria, and explore a labelled multiverse.")
TASKS = [
    "Raise the smallest effect of interest for ego depletion to 0.2. How does the dry run's power change, and would "
    "the verdict change?",
    "Run the verbal-overshadowing plan on the first study (description straight after the film). Which criteria does "
    "it meet?",
    "Add a third estimator to the multiverse (pool only labs with at least 100 people). Does it move the estimate?",
]


def run(seed=0):
    out = labs.Lab()

    e = opendata.ego_depletion_rrr()
    orig = e["original"]
    data = {k: e[kk][~orig] for k, kk in (("m1", "m_dep"), ("s1", "sd_dep"), ("n1", "n_dep"), ("m2", "m_ctl"),
                                           ("s2", "sd_ctl"), ("n2", "n_ctl"))}
    g, v = C.hedges_g(e["m_dep"][orig], e["sd_dep"][orig], e["n_dep"][orig], e["m_ctl"][orig], e["sd_ctl"][orig],
                      e["n_ctl"][orig])
    plan = C.Plan("ego depletion", "g", 1, float(g[0]), float(np.sqrt(v[0])), 0.1)
    d33 = C.d33(int(e["n_dep"][orig][0]), int(e["n_ctl"][orig][0]))
    out.row("ego depletion: original g (SE); d33; n per group for 95% power at 0.1",
            f"{plan.original:.2f} ({plan.original_se:.2f}); {d33:.2f}; {C.n_per_group(0.1, 0.95)}")
    dry = C.dry_run(plan, 23, 46, effects=(0.0, 0.1), reps=100, seed=seed)
    out.row("dry run, 23 labs of 46: share significant with no effect; at 0.1", f"{dry[0.0]:.2f}; {dry[0.1]:.2f}")
    assert dry[0.0] < 0.12
    r = C.analyse(data, plan)
    vd = C.verdict(r, plan, d33)
    out.row("ego depletion, 23 labs: g; 95% interval; one-sided p", f"{r['est']:.3f}; {r['lo']:.3f} to {r['hi']:.3f}; "
            f"{r['p_one']:.3f}")
    out.row("criteria met; replication Bayes factor", f"{vd['n_met']} of 3; {vd['bf_r0']:.3f}")

    d = opendata.overshadowing_rrr(2)
    vdat = {"k1": d["verbal"][:, 0], "n1": d["verbal"][:, 1], "k2": d["control"][:, 0], "n2": d["control"][:, 1]}
    o = d["original"]
    rd, rv = C.risk_difference(o[0, 0], o[0, 1], o[1, 0], o[1, 1])
    vplan = C.Plan("verbal overshadowing", "rd", -1, float(rd), float(np.sqrt(rv)), 0.05)
    vr = C.analyse(vdat, vplan)
    vv = C.verdict(vr, vplan, C.d33_rd(o[1, 0] / o[1, 1], int(o[0, 1]), int(o[1, 1])))
    out.row("verbal overshadowing, 22 labs: difference per 100; interval; criteria met",
            f"{100 * vr['est']:.1f}; {100 * vr['lo']:.1f} to {100 * vr['hi']:.1f}; {vv['n_met']} of 3")
    assert vv["significant"] and not vd["significant"]

    mv = C.multiverse(data, plan, {"all": np.ones(len(data["n1"]), bool),
                                   "English": e["language"][~orig] == "English"})
    out.row("multiverse (exploratory): range of ego-depletion estimates",
            f"{min(m['est'] for m in mv):.3f} to {max(m['est'] for m in mv):.3f} over {len(mv)} analyses")

    out.note = ("A plan frozen as code, checked on simulated data, applied once: verbal overshadowing replicates "
                "with a smaller effect than reported; ego depletion does not; the multiverse is a source of new "
                "hypotheses, labelled as such.")

    fig, ax = labs.figure(2, size=(11, 4.0))
    for a_, (res, scale, name, col) in zip(ax, ((vr, 100, "verbal overshadowing (per 100)", labs.GREEN),
                                                 (r, 1, "ego depletion (g)", labs.RED))):
        y, se = res["y"] * scale, np.sqrt(res["v"]) * scale
        order = np.argsort(y)
        a_.errorbar(y[order], np.arange(len(y)), xerr=1.96 * se[order], fmt="o", color=col, ms=3)
        a_.axvline(0, color="grey", ls=":")
        a_.axvline(res["est"] * scale, color=col)
        a_.set(title=name, xlabel="effect", yticks=[])
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())
