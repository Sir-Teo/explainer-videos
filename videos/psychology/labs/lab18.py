"""Lab 18: the attenuator and load; cueing and inhibition of return; guided search with its slopes and misses; a
saliency map; change blindness fitted; the attentional blink and the PRP bottleneck; the Stroop task as a diffusion,
with its delta plot and sequence effect; the normalization model's two kinds of gain; whole report; vigilance; and
the prevalence effect refitted."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology import archive
from explainer.psychology.psyche import attention as A

TITLE = "Attention: filters, search, time, conflict and gain"
GOAL = ("Turn Treisman's attenuator into numbers and see why a filter cannot pass your name; trace Posner's cue "
        "effects; run guided search and read its slopes and misses; compute a saliency map; fit change blindness; "
        "watch the blink and the bottleneck; run the Stroop task as two pathways racing to a bound; derive contrast "
        "and response gain from normalization; and refit the prevalence effect.")
TASKS = [
    "Lower the noise in `attention.dichotic` from 0.25 to 0.1. What attenuation now lets your name through a third of "
    "the time, and how often does an ordinary word get through?",
    "Raise the guided-search noise from 0.6 to 1.2. What happens to the conjunction slopes and to misses? Explain it "
    "with the overlap of the target's and the distractors' priorities.",
    "In `attention.normalization_crf`, give the attention field a width equal to the stimulus's. Is the gain contrast "
    "gain, response gain, or a mixture? Find the width at which c50 and Rmax change by the same factor.",
]


def run(seed=0):
    out = labs.Lab()
    rng = np.random.default_rng(seed)

    # 1. filters and load
    d = A.dichotic()
    out.row("ignored ear at attenuation 0.4: P(heard) for own name, a predicted word, an ordinary word",
            ", ".join(f"{v[1]:.3f}" for v in d.values()))
    out.row("flanker interference (ms) at loads 1 to 6", ", ".join(f"{v:.0f}" for v in A.flanker_interference(range(1, 7))))

    # 2. cueing
    soa = np.array([50, 100, 300, 600, 1000])
    out.row("invalid minus valid (ms), arrow cue, SOA 50 ... 1000", ", ".join(f"{v:.0f}" for v in A.cue_effect(soa)))
    out.row("the same for a flash", ", ".join(f"{v:.0f}" for v in A.cue_effect(soa, "exogenous")))

    # 3. search
    slopes = {}
    for kind in ("feature", "conjunction", "spatial"):
        r = A.search_slopes(kind, n=120, rng=np.random.default_rng(seed + 1))
        slopes[kind] = r
        out.row(f"{kind} search: slopes present, absent (ms an item); misses",
                f"{r['slopes'][0]:.1f}, {r['slopes'][1]:.1f}; {r['present'][1].mean():.0%}")
    rs = slopes["spatial"]["slopes"]
    out.row("unguided search: absent slope over present slope", f"{rs[1] / rs[0]:.2f}")

    # 4. a saliency map: one odd dot in a field
    f = np.zeros((60, 60))
    f[8:56:8, 8:56:8] = 1.0
    g = np.zeros((60, 60))
    g[40, 16] = 1.0
    sal = A.saliency_map({"luminance": f + g, "colour": g})
    out.row("the saliency map's first three fixations (row, column); the odd dot is at (40, 16)",
            "; ".join(str(p) for p in A.scan_path(sal, k=3, ior_radius=5)))

    # 5. change blindness
    w = np.ones(40)
    w[:2] = 4.0
    ci = np.mean([A.flicker(w, 0, 1.2, rng=rng) for _ in range(500)])
    mi = np.mean([A.flicker(w, 20, 1.2, rng=rng) for _ in range(500)])
    rp = archive.RENSINK_1997.data
    out.row("flicker: alternations for a central and a marginal change, Psyche against Rensink",
            f"{ci:.1f} vs {rp['ci_alternations']}; {mi:.1f} vs {rp['mi_alternations']}")

    # 6. time
    blink = A.attentional_blink(np.arange(1, 9), rng=np.random.default_rng(seed + 2))
    out.row("P(T2 | T1) at lags 1 to 8", ", ".join(f"{v:.2f}" for v in blink))
    prp = A.prp(np.array([0, 50, 100, 200, 400, 800]), rng=np.random.default_rng(seed + 3))
    out.row("RT2 (ms) at SOA 0, 50, 100, 200, 400, 800", ", ".join(f"{v:.0f}" for v in prp["rt2"]))
    out.row("its slope between SOA 0 and 50", f"{(prp['rt2'][1] - prp['rt2'][0]) / 50:+.2f}")

    # 7. Stroop
    m = {c: A.stroop(c, rng=np.random.default_rng(seed + 4))[0].mean() for c in ("congruent", "neutral", "incongruent")}
    out.row("Stroop colour naming (ms): congruent, neutral, incongruent; interference, facilitation",
            f"{m['congruent']:.0f}, {m['neutral']:.0f}, {m['incongruent']:.0f}; "
            f"{m['incongruent'] - m['neutral']:.0f}, {m['neutral'] - m['congruent']:.0f}")
    rc, _ = A.stroop("congruent", rng=np.random.default_rng(seed + 5))
    ri, _ = A.stroop("incongruent", rng=np.random.default_rng(seed + 6))
    _, dy = A.delta_plot(rc, ri)
    out.row("delta plot: interference at the 10th ... 90th percentile (ms)", ", ".join(f"{v:.0f}" for v in dy))

    # 8. gain
    c = np.logspace(-2, 0, 20)
    for name, sw, aw in (("small stimulus, broad field", 1, 8), ("large stimulus, narrow field", 8, 1)):
        g_ = A.gain_type(c, A.normalization_crf(c, sw, aw, False), A.normalization_crf(c, sw, aw, True))
        out.row(f"normalization, {name}: c50 and Rmax multiplied by", f"{g_['c50_ratio']:.2f}, {g_['rmax_ratio']:.2f}")
    assert abs(g_["rmax_ratio"] - 1) > 0.3

    # 9. capacity, vigilance, prevalence
    tva = A.tva_whole_report([30, 60, 120, 250], 6, rng=np.random.default_rng(seed + 7))
    out.row("whole report, six letters, at 30, 60, 120, 250 ms", ", ".join(f"{v:.2f}" for v in tva))
    v = A.vigilance(np.array([0, 30, 120]))
    out.row("a watch: hit rate at 0, 30 and 120 minutes", ", ".join(f"{h:.2f}" for h in v["hits"]))
    wd = archive.WOLFE_2005.data
    out.row("prevalence misses at 50%, 10%, 1%: Psyche (d' 2.48, shift 0.69) against Wolfe et al.",
            ", ".join(f"{a:.2f}/{b:.2f}" for a, b in zip(A.prevalence_misses(np.array(wd["prevalence"]), 2.48, 0.69),
                                                       wd["miss"])))
    out.note = ("A filter passes nothing from the ignored ear; an attenuator passes low-threshold words like your name. "
                "Feature search is flat, conjunction search shallow because guided, and unguided search two to one. "
                "The blink spares lag 1; the bottleneck gives a slope of minus one. Interference outweighs "
                "facilitation and grows over the slow tail. A broad attention field gives contrast gain, a narrow "
                "one response gain.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ss = np.array([4, 8, 16, 32])
    for kind, col in (("feature", labs.PINK), ("conjunction", labs.BLUE), ("spatial", labs.GREEN)):
        ax[0].plot(ss, slopes[kind]["present"][0], color=col, lw=1.6, label=f"{kind}, present")
        ax[0].plot(ss, slopes[kind]["absent"][0], color=col, lw=1.2, ls="--")
    ax[0].set(title="Set-size functions (dashed: absent)", xlabel="items", ylabel="RT, ms")
    ax[0].legend(fontsize=8)
    for sw, aw, col, name in ((1, 8, labs.PINK, "small stimulus"), (8, 1, labs.BLUE, "large stimulus")):
        ax[1].semilogx(c, A.normalization_crf(c, sw, aw, False), color=col, lw=1.0, ls="--")
        ax[1].semilogx(c, A.normalization_crf(c, sw, aw, True), color=col, lw=1.8, label=f"{name}, attended")
    ax[1].set(title="Normalization: contrast or response gain", xlabel="contrast", ylabel="response")
    ax[1].legend(fontsize=8)
    out.fig = fig
    return out
