"""Lab 46: scaling and choice: Thurstone's Case V and Bradley-Terry on Guilford's vegetables, the logit from Gumbel
noise, the red bus, a comparing chooser's decoy and compromise effects, a conjoint study, and acquiescence."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology import opendata
from explainer.psychology.psyche import scaling as Sc

TITLE = "Scaling, Surveys and Choice"
GOAL = ("Scale nine vegetables two ways, derive the logit by simulation and watch it fail for similar options, "
        "produce context effects from a comparing chooser, price attributes with a conjoint study, and see a response "
        "style create a correlation.")
TASKS = [
    "Give the comparing chooser no loss aversion (loss = 1). Do the decoy and compromise effects survive?",
    "Make the buses less alike (correlation 0.5). Where do the shares fall between the logit and the identical case?",
    "Reverse three of the six items in only one of the two scales. What happens to the spurious correlation?",
]


def run(seed=0):
    out = labs.Lab()
    d = opendata.vegetables_guilford()
    th = Sc.thurstone_scale(d["P"] * 100)
    bt = Sc.btl_fit(d["P"] * 100)
    order = np.argsort(th)
    out.row("Case V order, lowest to highest", ", ".join(d["names"][i] for i in order))
    out.row("Case V scale; Bradley-Terry log strengths (centred)",
            ", ".join(f"{v:.2f}" for v in th[order]) + "; " + ", ".join(f"{v:.2f}" for v in (bt["log"] - bt["log"].mean())[order]))
    assert np.corrcoef(th, bt["log"])[0, 1] > 0.99
    out.row("correlation of the two scales; MM updates", f"{np.corrcoef(th, bt['log'])[0, 1]:.4f}; {bt['iters']}")

    V = np.array([0.0, 0.5, 1.0])
    out.row("Gumbel simulation against the logit", ", ".join(f"{a:.3f}/{b:.3f}" for a, b in
                                                            zip(Sc.gumbel_choice_shares(V, seed=seed), Sc.logit_probs(V))))
    rb = Sc.normal_choice_shares([0.0, 0.0, 0.0], [[1, 0, 0], [0, 1, 0.999], [0, 0.999, 1]], seed=seed)
    out.row("car, red bus, blue bus: logit; nearly identical buses", "0.333 each; " + ", ".join(f"{v:.3f}" for v in rb))

    A, B = [6, 4], [4, 6]
    for name, opts in (("A, B", [A, B]), ("+ decoy below A", [A, B, [5.5, 3.5]]), ("+ extreme beyond A", [A, B, [8, 2]])):
        sh = Sc.pairwise_sampler(opts, steps=40, n=30_000, noise=0.1, seed=seed)
        out.row(f"comparing chooser, 40 comparisons: {name}", ", ".join(f"{v:.2f}" for v in sh))

    levels = [3, 2, 2, 3]
    design = Sc.conjoint_design(levels, 300, 3, seed=seed + 46)
    X = Sc.dummy_code(design, levels, numeric={0: [4.0, 6.0, 8.0]})
    beta = np.array([-0.6, 0.9, 0.5, 0.3, -0.2])
    Xs, ys = Sc.simulate_conjoint(X, beta, np.array([0.2, 0.5, 0.4, 0.4, 0.4]), 600, seed=seed + 47)
    f = Sc.fit_clogit(Xs, ys)
    out.row("conjoint estimates (truth -0.6, 0.9, 0.5, 0.3, -0.2)", ", ".join(f"{v:.2f}" for v in f["b"]))
    out.row("willingness to pay: battery, camera ($)", f"{-100 * f['b'][1] / f['b'][0]:.0f}, {-100 * f['b'][2] / f['b'][0]:.0f}")

    rng = np.random.default_rng(seed + 48)
    t1, t2, style = rng.standard_normal((3, 20000))
    r = {}
    for name, keys in (("one-way", [1] * 6), ("balanced", [1, -1] * 3)):
        a = Sc.styled_answers(t1, style, keys, seed=1).sum(1)
        b = Sc.styled_answers(t2, style, keys, seed=2).sum(1)
        r[name] = np.corrcoef(a, b)[0, 1]
    assert r["one-way"] > 0.15 and abs(r["balanced"]) < 0.05
    out.row("unrelated scales with acquiescence: one-way keys; balanced", f"{r['one-way']:.2f}; {r['balanced']:.2f}")

    out.note = ("Two scaling models agree on the vegetables; the logit holds for distinct options and fails for similar "
                "ones; a chooser who compares bends with the menu; and a response style can manufacture a correlation.")

    fig, ax = labs.figure(2, size=(11, 4.0))
    ax[0].scatter(th, bt["log"] - bt["log"].mean(), color=labs.BLUE)
    for i, n in enumerate(d["names"]):
        ax[0].annotate(n, (th[i], bt["log"][i] - bt["log"].mean()), fontsize=7)
    ax[0].set(title="Guilford's vegetables: two scales", xlabel="Case V", ylabel="Bradley-Terry log strength")
    steps = [2, 5, 10, 20, 40, 80]
    ax[1].plot(steps, [Sc.pairwise_sampler([A, B, [5.5, 3.5]], steps=s, n=20_000, noise=0.1, seed=seed)[0] for s in steps],
               "o-", color=labs.GREEN, label="decoy below A")
    ax[1].plot(steps, [Sc.pairwise_sampler([A, B, [8, 2]], steps=s, n=20_000, noise=0.1, seed=seed)[0] for s in steps],
               "o-", color=labs.BLUE, label="A in the middle")
    ax[1].set(title="context effects grow with deliberation", xlabel="comparisons", ylabel="share choosing A")
    ax[1].legend(fontsize=8)
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())
