"""Lab 22: fill two-dimensional matrices, check Lewis's translation, and sum probabilities over possible worlds."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import worlds as Wd

TITLE = "Worlds twice over, and worlds with weights"
GOAL = ("Classify six identity sentences by the diagonal and the actual row of their two-dimensional matrices, "
        "check that Lewis's first-order translation agrees with counterpart semantics on Humphrey's islands, and "
        "estimate a ProbLog query by sampling worlds against the exact sum over all eight.")
TASKS = [
    "Add Evans's 'Julius invented the zip' in your own copy: a rigid term fixed by the actual world's inventor "
    "against a description. Which box does its matrix land in?",
    "Run Wd.census() (about seven seconds) and list the principles that have countermodels in counterpart theory "
    "but none in Kripke's semantics with constant domains.",
    "Change the sampler so that burglary makes an earthquake report more likely. Is the exact product formula "
    "for P(calls) still right, and what replaces it?",
]

EXPECTED = {
    "water = H2O": "necessary a posteriori", "Hesperus = Phosphorus": "necessary a posteriori",
    "water = the watery stuff": "contingent a priori", "the length of S = one metre": "contingent a priori",
    "the evening star = Venus": "contingent a posteriori", "H2O = H2O": "necessary a priori",
}


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    two = Wd.twod()
    for s in two["sentences"]:
        m = np.array(s["matrix"])
        actual = two["worlds"].index(two["actual"])
        assert s["necessary"] == bool(m[actual].all()) and s["a_priori"] == bool(np.diag(m).all())
        assert s["class"] == EXPECTED[s["sentence"]], s["sentence"]
        lab.row(s["sentence"], s["class"])
    assert len({s["class"] for s in two["sentences"]}) == 4, "all four boxes are occupied"

    rows = Wd.humphrey()["rows"]
    agree = sum(r["direct"] == r["translated"] for r in rows)
    verdict = {r["key"]: r["direct"] for r in rows}
    lab.row("Humphrey's islands: translation agrees", f"{agree} of {len(rows)} sentences")
    lab.row("might have won / necessity of identity", f"{verdict['might']} / {verdict['NI']}")
    assert agree == len(rows) and verdict["might"] and not verdict["NI"] and not verdict["ND"] and verdict["refl"]

    exact = Wd.distribution_semantics()
    p = dict(exact["facts"])
    closed = (1 - (1 - p["burglary"]) * (1 - p["earthquake"])) * p["hears"]
    n = 40000
    b, e, h = (rng.random(n) < p[k] for k in ("burglary", "earthquake", "hears"))
    calls = (b | e) & h
    est = np.cumsum(calls) / np.arange(1, n + 1)
    se = np.sqrt(closed * (1 - closed) / n)
    lab.row("P(calls): sum over 8 worlds", f"{exact['p_calls']:.4f}   (closed form {closed:.4f})")
    lab.row("P(calls): 40,000 sampled worlds", f"{est[-1]:.4f}   (standard error {se:.4f})")
    assert abs(exact["p_calls"] - closed) < 1e-9 and abs(sum(w["p"] for w in exact["worlds"]) - 1) < 1e-9
    assert abs(est[-1] - closed) < 4 * se, "sampling worlds estimates the same sum"
    lab.note = ("The a priori is the diagonal and the necessary is the actual row, so all four combinations occur; "
                "and a probabilistic program's answer is nothing but the total weight of the worlds where the query "
                "holds.")

    fig, ax = labs.figure(3, size=(12, 4.2), gridspec_kw={"width_ratios": [1, 1, 1.5]})
    from matplotlib.patches import Rectangle

    names = ["Earth", "Twin E.", "Dusk"]
    for a, k in zip(ax[:2], (0, 2)):
        s = two["sentences"][k]
        m = np.array(s["matrix"], float)
        a.imshow(m, cmap="RdYlGn", vmin=-0.4, vmax=1.4)
        for i in range(3):
            for j in range(3):
                a.text(j, i, "T" if m[i, j] else "F", ha="center", va="center", color=labs.BG, fontweight="bold")
            a.add_patch(Rectangle((i - 0.5, i - 0.5), 1, 1, fill=False, ec=labs.GOLD, lw=2.5))
        a.add_patch(Rectangle((-0.47, -0.47), 2.94, 0.94, fill=False, ec=labs.BLUE, lw=2.5, ls="--"))
        a.set_xticks(range(3), names)
        a.set_yticks(range(3), names)
        a.grid(False)
        a.set(title=f"{s['sentence']}\n{s['class']}", xlabel="checked at (gold: diagonal)",
              ylabel="considered as actual (blue: actual row)")
    ks = np.arange(1, n + 1)
    ax[2].plot(ks, est, color=labs.BLUE, label="share of sampled worlds where Mary calls")
    ax[2].axhline(closed, color=labs.GOLD, ls="--", label=f"sum over the eight worlds: {closed:.3f}")
    ax[2].fill_between(ks, closed - 2 * np.sqrt(closed * (1 - closed) / ks), closed + 2 * np.sqrt(closed * (1 - closed) / ks),
                       color=labs.GOLD, alpha=0.12)
    ax[2].set(title="A ProbLog query as a sum over worlds", xlabel="worlds sampled", xscale="log",
              ylim=(closed - 0.1, closed + 0.1))
    ax[2].legend(loc="lower right")
    lab.fig = fig
    return lab
