"""Lab 17: build random structural causal models and check the back-door and front-door formulas against do()."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import causal as Ca

TITLE = "Seeing, adjusting, doing: two formulas against the interventional truth"
GOAL = ("Draw ten confounded models (age affects both drug and recovery) and ten front-door models (a "
        "hidden gene affects smoking and cancer; smoking acts only through tar) with random strengths. In each, "
        "compare the naive difference, the adjustment formula computed from the observational distribution "
        "alone, and the effect of an intervention computed by surgery on the model.")
TASKS = [
    "Give cancer a direct dependence on smoking in front_door_model (add 'S' to C's parents). How far is the "
    "front-door formula from the truth now, and which assumption broke?",
    "Adjust for a collider instead: add a variable caused by both drug and recovery and include it in Z. Check "
    "Ca.backdoor_ok first, then measure the bias.",
    "Sample 2,000 units from one confounded model with model.sample and estimate the adjusted effect from counts. "
    "How large is the sampling error compared with the confounding bias?",
]

GRID = 10  # exogenous noise takes the values 0/10 ... 9/10, so every probability is a multiple of 1/10


def _noise():
    return [(k / GRID, 1 / GRID) for k in range(GRID)]


def confounded_model(rng):
    """Age A -> drug D, A -> recovery R, D -> R, with random conditional probabilities."""
    pd = rng.integers(1, GRID, 2) / GRID            # P(D = 1 | A = a)
    pr = rng.integers(1, GRID, (2, 2)) / GRID           # P(R = 1 | D = d, A = a)
    return Ca.SCM(exo={"A": Ca.bern(0.5), "Ud": _noise(), "Ur": _noise()},
                  eqs={"D": (["A", "Ud"], lambda a, u: int(u < pd[a])),
                       "R": (["D", "A", "Ur"], lambda d, a, u: int(u < pr[d, a]))})


def front_door_model(rng):
    """Hidden gene G -> smoking S, G -> cancer C; S -> tar T -> C; no arrow from S to C."""
    ps = rng.integers(1, GRID, 2) / GRID            # P(S = 1 | G = g)
    pt = rng.integers(1, GRID, 2) / GRID            # P(T = 1 | S = s)
    pc = rng.integers(1, GRID, (2, 2)) / GRID           # P(C = 1 | T = t, G = g)
    return Ca.SCM(exo={"G": Ca.bern(0.4), "Us": _noise(), "Ut": _noise(), "Uc": _noise()},
                  eqs={"S": (["G", "Us"], lambda g, u: int(u < ps[g])),
                       "T": (["S", "Ut"], lambda s, u: int(u < pt[s])),
                       "C": (["T", "G", "Uc"], lambda t, g, u: int(u < pc[t, g]))})


def effects(m, X, Y, adjust):
    naive = m.prob(lambda w: w[Y] == 1, given=lambda w: w[X] == 1) - m.prob(lambda w: w[Y] == 1, given=lambda w: w[X] == 0)
    truth = m.prob(lambda w: w[Y] == 1, do={X: 1}) - m.prob(lambda w: w[Y] == 1, do={X: 0})
    return naive, adjust(m, 1) - adjust(m, 0), truth


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    g = Ca.DAG([("A", "D"), ("A", "R"), ("D", "R")])
    gs = Ca.DAG([("G", "S"), ("G", "C"), ("S", "T"), ("T", "C")])
    assert Ca.backdoor_ok(g, "D", "R", {"A"}) and not Ca.backdoor_ok(g, "D", "R", set())
    assert not Ca.backdoor_ok(gs, "S", "C", {"T"}), "with the gene hidden there is no back door to close"
    film = Ca.adjustment_demo()
    assert abs(film["backdoor"]["adjusted"] - film["backdoor"]["truth"]) < 1e-9
    lab.row("the film's drug: naive, adjusted, do()", "{naive:.2f}   {adjusted:.2f}   {truth:.2f}".format(**film["backdoor"]))
    lab.row("the film's smoking: naive, front door, do()", "{naive:.3f}   {front:.3f}   {truth:.3f}".format(**film["frontdoor"]))

    n = 10
    back = np.array([effects(confounded_model(rng), "D", "R", lambda m, x: Ca.backdoor_adjust(m, "D", x, "R", 1, ["A"]))
                     for _ in range(n)])
    front = np.array([effects(front_door_model(rng), "S", "C", lambda m, x: Ca.frontdoor_adjust(m, "S", x, "T", "C", 1))
                      for _ in range(n)])
    for name, t in (("back door", back), ("front door", front)):
        err_adj, err_naive = np.abs(t[:, 1] - t[:, 2]), np.abs(t[:, 0] - t[:, 2])
        assert err_adj.max() < 1e-9, f"{name}: the formula equals the interventional truth"
        assert err_naive.max() > 0.03, f"{name}: the naive difference is confounded"
        lab.row(f"{name}, {n} random models: largest |formula - do()|", f"{err_adj.max():.1e}   (theory 0)")
        lab.row(f"{name}: largest and mean |naive - do()|", f"{err_naive.max():.3f}   {err_naive.mean():.3f}")
    flips = int(np.sum(np.sign(back[:, 0]) * np.sign(back[:, 2]) < 0) + np.sum(np.sign(front[:, 0]) * np.sign(front[:, 2]) < 0))
    lab.row("models where naive and true effects have opposite signs", f"{flips} of {2 * n}")
    lab.note = ("Conditioning reports what is seen among those who took the drug; the adjustment formulas rebuild, "
                "from the same observational distribution and the graph, what would be seen if everyone were made "
                "to take it. The graph is the extra premise.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    for a, t, title, formula in ((ax[0], back, "Back door: adjust for age", "back-door formula"),
                                 (ax[1], front, "Front door: hidden gene, through tar", "front-door formula")):
        lim = max(0.3, np.abs(t).max() * 1.15)
        a.plot([-lim, lim], [-lim, lim], color=labs.MUTED, ls="--", lw=1, label="estimate = truth")
        a.scatter(t[:, 2], t[:, 0], s=36, color=labs.RED, marker="x", label="naive: P(y | x=1) - P(y | x=0)")
        a.scatter(t[:, 2], t[:, 1], s=30, color=labs.GREEN, label=formula, zorder=3)
        a.set(title=title, xlabel="true effect: P(y | do(x=1)) - P(y | do(x=0))", ylabel="estimate from observation",
              xlim=(-lim, lim), ylim=(-lim, lim))
        a.legend(loc="lower right")
    lab.fig = fig
    return lab
