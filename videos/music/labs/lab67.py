"""Lab 67: research methods, computed: a manuscript tradition copied and recovered by neighbour joining; the power of
ABX listening tests; and a literature with selective publication, its funnel and Egger's test."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import melody as ML
from explainer.music.monochord import research as R
from explainer.music.monochord.partkit import organ_tone
from explainer.stats.kit import multiple as MT

TITLE = "Research methods, computed"
GOAL = ("Copy the Tune through a simulated tradition of scribes and recover its family tree and original; work out how "
        "many listening trials a test needs; and watch selective publication bend a literature.")
TASKS = [
    "Change ERROR, the scribes' error rate. When does the majority reconstruction start to fail?",
    "Change HIT, the listener's true hit rate. How many ABX trials give 80% power?",
    "Change PUBLISH_NULL, the chance that a non-significant study is published. How much does the pooled estimate improve?",
]
ERROR = 0.05
HIT = 0.7
PUBLISH_NULL = 0.15


def play(keys, beats, beat=0.4):
    t, y = 0.0, np.zeros(int((sum(beats) * beat + 1) * SR))
    for m, b in zip(keys, beats):
        z = organ_tone(440 * 2 ** ((m - 69) / 12), b * beat * 0.95, partials=6, rolloff=0.7)
        i = int(t * SR)
        y[i:i + len(z)] += z[: len(y) - i]
        t += b * beat
    return Clip(y / (np.max(np.abs(y)) + 1e-12) * 0.8, SR)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    m = ML.corpus()[0]
    keys, beats = [60 + p for p in m.pitches], list(m.beats)
    t = R.copy_tradition(keys, rng, generations=4, error_rate=ERROR)
    sv = t["survive"]
    W = [t["mss"][i]["notes"] for i in sv]
    errs = [R.hamming(w, keys) for w in W]
    D = np.array([[R.hamming(a, b) for b in W] for a in W])
    rf = R.rf_distance(R.true_adjacency(t["mss"], sv), R.neighbor_joining(D, [str(i) for i in sv]), sv)
    rec = R.reconstruct(W)
    lab.row("manuscripts; surviving; errors per surviving copy (least to most)", f"{len(t['mss'])}; {len(sv)}; {min(errs)} to {max(errs)}")
    lab.row("true groupings of the copies; recovered by neighbour joining", f"{rf['true_splits']}; {rf['recovered']}")
    lab.row("the original rebuilt by majority: notes wrong", str(R.hamming(rec, keys)))
    assert R.hamming(rec, keys) <= np.median(errs)
    n80 = R.abx_trials_needed(HIT)
    p20 = R.abx_power(HIT, 20)
    lab.row(f"ABX at a true hit rate of {HIT:.0%}: power of 20 trials; trials for 80% power", f"{p20['power']:.2f}; {n80}")
    assert R.abx_power(HIT, n80)["power"] >= 0.8
    sim = MT.publication_sim(150, 0.1, rng, n_range=(12, 120), publish_null=PUBLISH_NULL)
    est, se, pub = sim["est"], sim["se"], sim["published"]
    fe = lambda e, s: float(np.sum(e / s ** 2) / np.sum(1 / s ** 2))
    eg = MT.egger(est[pub], se[pub])
    lab.row("a true effect of 0.1: pooled over all studies; over the published", f"{fe(est, se):.2f}; {fe(est[pub], se[pub]):.2f}")
    lab.row("Egger's test on the published: intercept, p", f"{eg['intercept']:.2f}, {eg['p']:.3f}")
    if PUBLISH_NULL < 0.5:
        assert fe(est[pub], se[pub]) > fe(est, se)
    worst = int(np.argmax(errs))
    lab.audio = concat([play(keys, beats), play(W[worst], beats), play(rec, beats)], gap=0.8)
    lab.row("ear problem: the Tune, the worst copy and the rebuilt original; where are the wrong notes? (listen first)",
            ", ".join(str(i + 1) for i, (a, b) in enumerate(zip(W[worst], keys)) if a != b))
    fig, (ax1, ax2) = labs.figure(2)
    ax1.scatter(est[~pub], 1 / se[~pub], s=8, color="0.75", label="unpublished")
    ax1.scatter(est[pub], 1 / se[pub], s=10, color=labs.GOLD, label="published")
    ax1.axvline(0.1, color="0.3", lw=1)
    ax1.set_xlabel("estimate")
    ax1.set_ylabel("precision (1/se)")
    ax1.legend(fontsize=7)
    ns = np.arange(8, 200, 4)
    ax2.plot(ns, [R.abx_power(HIT, n)["power"] for n in ns], color=labs.GOLD)
    ax2.axhline(0.8, color="0.6", ls="--")
    ax2.set_xlabel("ABX trials")
    ax2.set_ylabel("power")
    lab.fig = fig
    lab.note = ("Shared errors reveal who copied from whom; small listening tests miss real differences; and a literature "
                "that publishes its lucky studies overstates its effects in a way its funnel plot can show.")
    return lab
