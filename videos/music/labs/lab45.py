"""Lab 45: the auditory scene, computed: the streaming model against van Noorden's boundary, interleaved melodies,
a mistuned harmonic, and a timbre space you can extend."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat, mix
from explainer.music.monochord import scene as S
from videos.music.music45 import compute as C

TITLE = "The auditory scene, computed"
GOAL = ("Fit the competition model to the streaming boundary and use it to predict your own ABA- sequences; hide a "
        "melody in another and release it; and map timbre from measurements.")
TASKS = [
    "Change POINTS (the boundary data) or F_A. How does the fitted constant change? Predict a sequence, then listen.",
    "Edit HIDDEN and the distractor rule. How few crossings are enough to hide a tune?",
    "Add a feature to FEATURES (scene.features returns more than the map uses) and redraw the timbre space.",
]
POINTS = S.VAN_NOORDEN_TCB
F_A = 1000.0
HIDDEN = [67, 67, 74, 74, 76, 76, 74, 72, 72, 71, 71, 69, 69, 67]     # the Tune's first two phrases, in G
FEATURES = S.FEATURE_KEYS


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    fit = S.fit_boundary(POINTS, F_A)
    lab.row("fitted w / tau (ERB-numbers a second); rms miss (semitones)", f"{fit['k']:.1f}; {fit['rms_st']:.2f}")
    trts = [0.06, 0.09, 0.12, 0.15]
    lab.row("model boundary at 60, 90, 120, 150 ms (semitones)", ", ".join(f"{float(S.boundary(t, F_A, 1.0, fit['k'])):.1f}" for t in trts))
    scale = [x for x in range(min(HIDDEN) - 6, max(HIDDEN) + 7) if x % 12 in (0, 2, 4, 5, 7, 9, 11)]
    distr = [scale[scale.index(m) + (2 if i % 2 == 0 else -2)] if m in scale else m + 3 for i, m in enumerate(HIDDEN)]
    lab.row("HIDDEN against the distractor: crossings", f"{S.crossings(HIDDEN, distr)} in {len(HIDDEN)} notes")
    feats = {k: S.features(np.asarray(y, float), float(f0)) for k, (y, f0) in list(C.instruments().items())}
    sp = S.timbre_space(feats, keys=FEATURES)
    assert len(sp["coords"]) == len(feats)
    lab.row("timbre space: share of variation on two axes", f"{sp['share'][0]:.2f}, {sp['share'][1]:.2f}")

    # sound: the interleaved tune, then released; ear problem: ABA- at random settings
    ioi = 0.12
    def line(shift):
        p = []
        for i, (x, y) in enumerate(zip(HIDDEN, distr)):
            p.append((Clip(C.piano(x, 0.22, 0.7), SR), 2 * i * ioi, 0.0))
            p.append((Clip(C.piano(y + shift, 0.22, 0.7), SR), (2 * i + 1) * ioi, 0.0))
        return Clip(mix(p, duration=2 * len(HIDDEN) * ioi + 0.5).y, SR)
    clips = [line(0), line(-19)]
    answers = []
    for i in range(3):
        st = float(rng.choice([2.0, 5.0, 9.0, 13.0]))
        trt = float(rng.choice([0.06, 0.1, 0.15]))
        clips.append(Clip(S.aba(st, trt, max(6, int(2.4 / (4 * trt))), f_a=F_A), SR))
        answers.append(f"{st:.0f} st at {1000 * trt:.0f} ms: model says {'two' if S.streams(st, trt, F_A, 1.0, fit['k']) else 'one'}")
    lab.audio = concat(clips, gap=0.9)
    lab.row("ear problem: one stream or two? (listen first)", "; ".join(answers))

    fig, (ax1, ax2) = labs.figure(2)
    t = np.linspace(0.04, 0.17, 50)
    ax1.plot(1000 * t, S.boundary(t, F_A, 1.0, fit["k"]), color=labs.GOLD, label="model")
    ax1.plot([1000 * p[0] for p in POINTS], [p[1] for p in POINTS], "o", color="C3", label="van Noorden (read from figure)")
    ax1.axhline(S.VAN_NOORDEN_FB, color="C0", ls="--", lw=1, label="fission boundary")
    ax1.set_xlabel("tone repetition time (ms)")
    ax1.set_ylabel("semitones")
    ax1.legend(fontsize=7)
    xy = np.array(sp["coords"])
    ax2.plot(xy[:, 0], xy[:, 1], "o", color=labs.GOLD)
    for n, (x, y) in zip(sp["names"], xy):
        ax2.annotate(n, (x, y), fontsize=6)
    ax2.set_title("timbre space of the series' instruments")
    lab.fig = fig
    lab.note = ("Two streams form when A captures the next A more strongly than it captures B; with exponential fall-offs "
                "in time and on the ERB scale, the boundary is a straight line in the repetition time.")
    return lab
