"""Lab 34: Granovetter's thresholds, DeGroot and bounded-confidence opinions, simple and complex contagion, the wisdom
of crowds under influence, and a cumulative-advantage market."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import social as S

TITLE = "Social Influence"
GOAL = ("Run Granovetter's riot with one threshold changed; watch DeGroot averaging reach consensus and bounded "
        "confidence leave camps; spread a simple and a complex contagion on a clustered and a rewired network; check "
        "the diversity prediction identity and see influence shrink a crowd's diversity without fixing its error; and "
        "build a music market with and without social information.")
TASKS = [
    "In the riot, give the instigator's two followers thresholds 0 and 2 instead of 1 and 2. What happens, and what "
    "would an observer who saw only the outcome conclude about the crowd?",
    "Rewire only 5% of the lattice's ties. Does the complex contagion still spread? Find the fraction at which it stops.",
    "In the music market, set social influence to 0.3 and to 0.95. How do inequality and unpredictability move?",
]


def run(seed=0):
    out = labs.Lab()
    t = np.arange(100)
    t2 = t.copy()
    t2[1] = 2
    out.row("riot: thresholds 0, 1, ..., 99; the same with one threshold 1 -> 2",
            f"{S.cascade_size(t)} join; {S.cascade_size(t2)} joins")

    rng = np.random.default_rng(seed)
    W = rng.random((5, 5)) + np.eye(5)
    W /= W.sum(axis=1, keepdims=True)
    x0 = np.array([0.0, 0.2, 0.5, 0.9, 1.0])
    end = S.degroot(W, x0, steps=200)[-1]
    w = S.influence_weights(W)
    out.row("DeGroot consensus; left-eigenvector average", f"{end[0]:.4f}; {w @ x0:.4f}")
    assert np.isclose(end[0], w @ x0)

    x = np.linspace(0, 1, 101)
    out.row("bounded confidence, clusters at eps = 0.05, 0.10, 0.25",
            ", ".join(str(S.clusters(S.bounded_confidence(x, e, 80)[-1], 1e-2)) for e in (0.05, 0.10, 0.25)))

    L = S.ring_lattice(400, 2)
    R = S.rewire(L, 1.0, seed=seed + 1)
    seeds = [0, 1, 2, 3]
    for need, name in ((1, "simple"), (2, "complex")):
        a, b = S.contagion(L, seeds, need), S.contagion(R, seeds, need)
        out.row(f"{name} contagion: adopters (steps) on the lattice; rewired",
                f"{a[-1]} ({len(a) - 1}); {b[-1]} ({len(b) - 1})")

    c = S.crowd(np.random.default_rng(seed + 2).lognormal(np.log(1200), 0.25, 800), 1198)
    out.row("crowd: collective error = individual - diversity",
            f"{c['collective']:.0f} = {c['individual']:.0f} - {c['diversity']:.0f}")
    r = S.influence_rounds(rounds=5, seed=seed)
    out.row("influence rounds: diversity first and last; collective error first and last",
            f"{r['diversity'][0]:.3f}, {r['diversity'][-1]:.4f}; {r['collective'][0]:.3f}, {r['collective'][-1]:.3f}")

    mk = {s: S.music_market(listeners=1500, worlds=6, social=s, seed=seed + 3) for s in (0.0, 0.8)}
    out.row("music market, independent vs social: mean Gini; unpredictability",
            f"{mk[0.0]['gini'].mean():.2f} vs {mk[0.8]['gini'].mean():.2f}; "
            f"{mk[0.0]['unpredictability']:.4f} vs {mk[0.8]['unpredictability']:.4f}")

    out.note = ("Outcomes of crowds depend on the whole distribution of people, not on the average person; averaging "
                "reaches consensus with weights set by who listens to whom; behaviours that need reinforcement travel "
                "through clustered ties; and social information makes crowds more alike, markets more unequal and "
                "hits less predictable.")

    fig, ax = labs.figure(3, size=(13, 4.0))
    cc = S.cascade_curve()
    ax[0].plot(cc["sd"], cc["size"], color=labs.GOLD)
    ax[0].set(title="Thresholds", xlabel="SD of thresholds (mean 25)", ylabel="final number in")
    path = S.bounded_confidence(x, 0.1, 25)
    ax[1].plot(path, color=labs.BLUE, lw=0.6, alpha=0.6)
    ax[1].set(title="Bounded confidence, eps = 0.1", xlabel="round", ylabel="opinion")
    for s, col in ((0.0, labs.BLUE), (0.8, labs.GOLD)):
        q = mk[s]["quality"]
        o = np.argsort(q)
        ax[2].plot(q[o], mk[s]["shares"][:, o].T, ".", color=col, ms=3, alpha=0.7)
    ax[2].set(title="Market share by quality (blue independent, gold social)", xlabel="quality", ylabel="share")
    out.fig = fig
    return out
