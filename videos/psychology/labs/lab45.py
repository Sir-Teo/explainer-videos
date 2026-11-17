"""Lab 45: item response theory: Rasch and two-parameter fits to the LSAT by marginal ML, conditional ML and the
sufficient sum score, information, an adaptive test against fixed forms, Mantel-Haenszel DIF, and knowledge
tracing."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology import opendata
from explainer.psychology.psyche import irt as I

TITLE = "Item Response Theory"
GOAL = ("Fit the Rasch and two-parameter models to five LSAT items, check that the sum score is sufficient, see where "
        "the test is informative, then build an adaptive test, flag an unfair item and trace a learner.")
TASKS = [
    "Fit the three-parameter idea by hand: add a guessing floor of 0.2 to every item in the adaptive test's bank. How "
    "many more items does it need?",
    "Make the DIF item 0.3 harder for the focal group instead of 0.8. Which ETS category does it fall in?",
    "Give the knowledge-tracing students 5 practices instead of 10. How well are the four parameters recovered?",
]


def run(seed=0):
    out = labs.Lab()
    X = opendata.lsat_1000()["X"]
    r = I.fit_mml(X, "rasch")
    t = I.fit_mml(X, "2pl")
    out.row("LSAT Rasch: common a; b", f"{r['a'][0]:.3f}; " + ", ".join(f"{v:.3f}" for v in r["b"]))
    out.row("LSAT 2PL: a; log-likelihoods (Rasch, 2PL); LR on 4 df",
            ", ".join(f"{v:.2f}" for v in t["a"]) + f"; {r['loglik']:.2f}, {t['loglik']:.2f}; "
            f"{2 * (t['loglik'] - r['loglik']):.2f}")
    assert abs(r["loglik"] + 2466.938) < 0.01
    c = I.fit_cml(X)
    out.row("conditional ML difficulties (centred)", ", ".join(f"{v:.3f}" for v in c["b"]))
    p1 = I.pattern_given_score([1, 1, 0, 0, 0], c["b"])
    out.row("P(1 1 0 0 0 | score 2), free of ability", f"{p1:.3f}")

    th = np.linspace(-6, 4, 201)
    inf = I.info(th, t["a"], t["b"]).sum(1)
    out.row("LSAT test information: peak and where; smallest SE", f"{inf.max():.2f} at {th[inf.argmax()]:.1f}; "
            f"{1 / np.sqrt(inf.max()):.2f}")

    rng = np.random.default_rng(seed + 45)
    a, b = np.exp(rng.normal(0.2, 0.25, 300)), rng.uniform(-3, 3, 300)
    people = rng.normal(size=200)
    runs = [I.cat(float(p), a, b, stop_se=0.3, max_items=60, seed=seed + i) for i, p in enumerate(people)]
    n_items = np.array([len(x["items"]) for x in runs])
    rmse = np.sqrt(np.mean((np.array([x["theta"] for x in runs]) - people) ** 2))
    best = np.argsort(-I.info(0.0, a, b)[0])
    fixed = {}
    for k in (15, 25, 35, 45):
        idx = best[:k]
        e = I.eap(I.simulate(people, a[idx], b[idx], seed=k), a[idx], b[idx])["theta"]
        fixed[k] = float(np.sqrt(np.mean((e - people) ** 2)))
    out.row("adaptive test: mean items; RMSE", f"{n_items.mean():.1f}; {rmse:.3f}")
    out.row("best fixed forms: RMSE at 15, 25, 35, 45 items", ", ".join(f"{fixed[k]:.3f}" for k in fixed))

    g = np.repeat([0, 1], 3000)
    th2 = rng.normal(size=6000) - 0.8 * g
    bb = np.linspace(-1.5, 1.5, 15)
    Xd = I.simulate(th2, 1.0, bb, seed=seed + 7)
    Xd[:, 7] = rng.random(6000) < 1 / (1 + np.exp(-(th2 - np.where(g == 1, bb[7] + 0.8, bb[7]))))
    mh = I.mantel_haenszel(Xd, g, 7)
    mh0 = I.mantel_haenszel(Xd, g, 3)
    out.row("Mantel-Haenszel: fair item 4 (delta, category); item 8 made harder (delta, category)",
            f"{mh0['delta']:.2f}, {mh0['category']}; {mh['delta']:.2f}, {mh['category']}")

    Y, _ = I.bkt_simulate(400, 10, 0.2, 0.15, 0.2, 0.1, seed=seed + 9)
    f = I.bkt_fit(Y)
    out.row("knowledge tracing fit (truth 0.2, 0.15, 0.2, 0.1)", f"L0 {f['L0']:.2f}, T {f['T']:.2f}, G {f['G']:.2f}, "
            f"S {f['S']:.2f}")

    out.note = ("The Rasch model is enough for the LSAT's five easy items, which inform mostly about weak candidates; "
                "an adaptive test matches a fixed form of about twice its length; matching on score separates bias "
                "from impact.")

    fig, ax = labs.figure(2, size=(11, 4.0))
    for j in range(5):
        ax[0].plot(th, I.prob(th, t["a"][j], t["b"][j])[:, 0], label=f"item {j + 1}")
    ax[0].set(title="LSAT item characteristic curves (2PL)", xlabel="ability", ylabel="P(correct)")
    ax[0].legend(fontsize=7)
    ax[1].plot(list(fixed), list(fixed.values()), "o-", color=labs.BLUE, label="best fixed form")
    ax[1].plot([n_items.mean()], [rmse], "s", color=labs.GREEN, ms=9, label="adaptive")
    ax[1].set(title="error against test length", xlabel="items", ylabel="RMSE")
    ax[1].legend(fontsize=8)
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())
