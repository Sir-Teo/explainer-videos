"""Lab 42: composing as search, computed: operations on a motive, the constraint funnel, a dice game's count, and a
generate-and-test searcher whose critics you can change."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat, mix
from explainer.music.monochord import composer as K
from explainer.music.monochord import melody as M
from videos.music.music42 import compute as C

TITLE = "Composing as search, computed"
GOAL = ("Write a motive and let the searcher develop it over your chords; count what your rules leave; and hear how "
        "much a Markov chain copies as its memory grows.")
TASKS = [
    "Edit MOTIVE (key number, onset in beats, length) and CHORDS. Does the searcher keep more drafts or fewer?",
    "Change PLAN (the tension curve, one number a bar). Does the kept melody's peak move with it?",
    "Change RULES (a subset of composer.FUNNEL_RULES) and LENGTH. Which rule cuts the most?",
]
MOTIVE = [(64, 0.0, 0.5), (62, 0.5, 0.5), (60, 1.0, 1.0), (67, 2.0, 2.0)]
CHORDS = ["I", "IV", "V", "I", "vi", "ii", "V", "I"]
PLAN = [1.0, 1.5, 2.0, 1.5, 2.5, 3.0, 2.5, 0.5]
DRAFTS = 1500
RULES = K.FUNNEL_RULES
LENGTH = 8


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    bass = K.bass_line(CHORDS)
    r = K.compose(MOTIVE, CHORDS, bass, np.random.default_rng(seed), drafts=DRAFTS, plan=PLAN)
    assert sum(r["rejected"].values()) + r["survivors"] == DRAFTS
    lab.row("drafts; rejected, by the first critic that refused", f"{DRAFTS}; " + ", ".join(f"{k} {v}" for k, v in sorted(r["rejected"].items(), key=lambda kv: -kv[1])))
    if r["best"] is None:
        lab.row("kept", "nothing survived: loosen a rule or change the motive")
        best = None
    else:
        v = r["best"]["verdict"]
        best = r["best"]["melody"]
        lab.row("kept draft; its score", f"{r['best']['draft'] + 1}; {v['score']:.3f}")
        lab.row("unity, variety, tension fit, chord tones", f"{v['unity']:.2f}, {v['variety']:.2f}, {v['tension_fit']:.2f}, {v['harmony']:.2f}")
        lab.row("how each bar derives from the motive", "; ".join("motive" if d == () else ("-" if d is None else "+".join(d)) for d in (K.derivation(f, MOTIVE) for f in K.bar_figures(best))))
    counts = [K.count_funnel(LENGTH, rules=tuple(RULES[:k])) for k in range(len(RULES) + 1)]
    lab.row(f"{LENGTH}-note melodies on 15 white keys, adding RULES one at a time", " -> ".join(f"{c:,}" for c in counts))
    dc = K.dice_count(K.dice_table(seed + 42))
    lab.row("our dice game: distinct minuets; entropy (bits)", f"{dc['distinct']:,}; {dc['entropy_bits']:.1f}")

    # sound: the kept melody; ear problem: chains of random order
    parts = []
    if best is not None:
        parts.append(C.render(best, bass))
    seqs = {t.name: t.pitches for t in M.corpus() if t.mode == "major"}
    orders = []
    for i in range(3):
        o = int(rng.choice([1, 2, 4]))
        g = K.generate(K.markov(list(seqs.values()), o), 20, np.random.default_rng(seed * 10 + i))
        mel = [(72 + x, float(j), 1.0) for j, x in enumerate(g)]
        parts.append(C.render(mel, beat=0.3, tail=0.6))
        orders.append(f"{o} (copies {K.longest_copy(g, seqs)['run']} notes)")
    lab.audio = concat(parts, gap=1.0)
    lab.row("ear problem: the order of each chain melody, in order (listen first)", ", ".join(orders))

    fig, (ax1, ax2) = labs.figure(2)
    if best is not None:
        for m, a, d in best:
            ax1.plot([a, a + d * 0.95], [m, m], color=labs.GOLD, lw=5, solid_capstyle="butt")
        for b in range(len(CHORDS) + 1):
            ax1.axvline(4 * b, color="#3A4250", lw=0.8)
        ax1.set_title("the kept melody (bars of four beats)")
        ax1.set_xlabel("beat")
        ax2.plot(range(1, len(PLAN) + 1), PLAN, "--", color="#8A93A0", label="plan")
        ax2.plot(range(1, len(CHORDS) + 1), K.tension(best, CHORDS), "o-", color=labs.GOLD, label="kept melody")
        ax2.set_xlabel("bar")
        ax2.set_title("tension: the plan and the result")
        ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("The generator only proposes; the critics decide. Hard critics refuse, soft critics rank, and the best "
                "survivor is kept; the funnel shows how fast rules shrink the space a generator has to search.")
    return lab
