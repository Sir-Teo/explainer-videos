"""Lab 47: origins, computed: rhythm priors revealed by tapping back, a melody passed through simulated singers, and
the nPVI of tunes by language."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat, mix
from explainer.music.monochord import origins as O
from videos.music.music47 import compute as C

TITLE = "Origins, computed"
GOAL = ("Reveal a simulated listener's rhythm prior by iterated reproduction; pass a melody through a chain of "
        "simulated singers and watch structure appear; and measure the rhythm of tunes by language.")
TASKS = [
    "Edit PRIOR (integer patterns and weights). Do the chains end in the same proportions as the prior? Why not exactly?",
    "Change SINGER (try novel 0, or category 0.05). Which universals still appear after GENERATIONS singers?",
    "Add tunes to FRENCH or ENGLISH by origin and re-run the permutation test. How many tunes would settle it?",
]
PRIOR = {(1, 1, 2): 2.0, (1, 1, 1): 1.0, (1, 2, 2): 0.6, (1, 2, 3): 0.3}
SINGER = {}
GENERATIONS = 40
FRENCH = {"France", "Canada"}
ENGLISH = {"England", "United States", "Scotland", "Wales", "Britain"}


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    pr = O.RhythmPrior(PRIOR)
    ch = O.rhythm_chains(pr, 300, 5, seed=seed)
    mass = [pr.mass_near(ch[:, i]) for i in range(6)]
    lab.row("share of rhythms near a small-integer ratio, rounds 0 to 5", ", ".join(f"{m:.2f}" for m in mass))
    ends = {}
    for y in ch[:, -1]:
        k = O.nearest_pattern(pr, y)
        if k:
            ends[k] = ends.get(k, 0) + 1
    tot = sum(ends.values())
    share = {k: ends.get(k, 0) / tot for k in PRIOR}
    wsum = sum(PRIOR.values())
    lab.row("where chains ended / the prior's share", "; ".join(f"{':'.join(map(str, k))} {share[k]:.2f} / {PRIOR[k] / wsum:.2f}" for k in PRIOR))
    assert mass[-1] > mass[0]

    mel = O.random_melody(rng)
    chain = O.transmission_chain(mel, GENERATIONS, rng, SINGER)
    s0, s1 = O.structure(chain[0]), O.structure(chain[-1])
    lab.row(f"a random melody before and after {GENERATIONS} singers: pitch levels", f"{s0['levels']} -> {s1['levels']}")
    lab.row("average step (semitones)", f"{s0['step']:.2f} -> {s1['step']:.2f}")
    lab.row("lengths that are simple ratios", f"{s0['simple']:.2f} -> {s1['simple']:.2f}")
    err = [O.align(chain[g], chain[g + 1])["per_note"] for g in range(GENERATIONS)]
    lab.row("copying error per note, first five and last five singers", f"{np.mean(err[:5]):.2f} -> {np.mean(err[-5:]):.2f}")

    fr = [O.npvi(t.beats[:-1]) for t in C.TUNES if t.origin in FRENCH]
    en = [O.npvi(t.beats[:-1]) for t in C.TUNES if t.origin in ENGLISH]
    t = O.bootstrap_diff(fr, en, n=4000, seed=seed)
    lab.row(f"nPVI: French ({len(fr)}) / English ({len(en)}) tunes", f"{np.mean(fr):.1f} / {np.mean(en):.1f}")
    lab.row("English minus French: bootstrap interval; permutation p", f"{t['diff']:.1f} [{t['lo']:.1f}, {t['hi']:.1f}]; p = {t['p']:.3f}")

    # sound: the melody before and after; ear problem: three rhythms, each a random start or a chain's end
    clips = [C.voice_clip(chain[0], seed=1), C.voice_clip(chain[-1], seed=2)]
    answers = []
    for i in range(3):
        c = int(rng.integers(len(ch)))
        if rng.random() < 0.5:
            x, kind = ch[c, 0], "random start"
        else:
            x, kind = ch[c, -1], "after five rounds"
        clips.append(C.rhythm_clip(x[:2], loops=3))
        answers.append(kind)
    lab.audio = concat(clips, gap=0.9)
    lab.row("ear problem: the last three loops are each a random start or a chain's end (listen first)", ", ".join(answers))

    fig, (ax1, ax2) = labs.figure(2)
    ax1.plot(range(6), mass, "o-", color=labs.GOLD)
    ax1.set_xlabel("round of tapping back")
    ax1.set_ylabel("share near a small-integer ratio")
    p0 = [x[0] for x in chain[0]]
    p1 = [x[0] for x in chain[-1]]
    ax2.step(np.cumsum([0] + [x[1] for x in chain[0]])[:-1], p0, where="post", color="C7", label="start")
    ax2.step(np.cumsum([0] + [x[1] for x in chain[-1]])[:-1], p1, where="post", color="C3", label=f"after {GENERATIONS}")
    ax2.set_xlabel("beats")
    ax2.set_ylabel("pitch (semitones)")
    ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("A chain of learners who sample their posterior drifts to their prior (Griffiths and Kalish 2007): that is "
                "why tapping back reveals expectations, and why transmission alone can build musical structure.")
    return lab
