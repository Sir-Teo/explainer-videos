"""Lab 22: analysis computed: a melody reduced level by level, chord progressions parsed by a six-rule grammar (and
their trees counted), the grammar trained on Bach's chorales and scored against chord n-grams, melodies grown from a
skeleton, and skeletons chosen by ear."""

from collections import Counter

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import Clip, concat
from explainer.music.monochord import chorales as BC
from explainer.music.monochord import chords as CH
from explainer.music.monochord import fourpart as F
from explainer.music.monochord import grammar as G
from explainer.music.monochord import melody as M
from explainer.music.monochord.partkit import organ_tone

TITLE = "Analysis, computed"
GOAL = ("Reduce a melody to its skeleton level by level, parse chord progressions with a six-rule grammar of harmony and "
        "count their trees, train the grammar on Bach's chorales and compare it with chord n-grams on held-out phrases, "
        "grow new melodies from a skeleton, and choose skeletons by ear.")
TASKS = [
    "Choose a TUNE from Part 14's corpus. Read its reduction at a note every two, four and eight beats. Does it end on a stepwise descent to the tonic?",
    "Write a PROGRESSION of your own in Roman numerals (I, ii, IV, V, vi, V7). How many trees does the grammar give it? Does it parse at all? Add the plagal rule TR -> SR TR and try again.",
    "Change SEED and grow three melodies from the Tune's skeleton. Which rules did each use, and why does none of them sound like the Tune?",
]
TUNE = "Ode to Joy"
PROGRESSION = "I vi IV ii V I"
SEED = 3
SR = 48_000
HARMONY = ["C", "C", "F", "G", "F", "C", "G", "C"]
PCS = {"C": (0, 4, 7), "F": (5, 9, 0), "G": (7, 11, 2)}


def chord_at(t):
    return set(PCS[HARMONY[min(int(t // 2), len(HARMONY) - 1)]])


def notes_of(tune, base=72):
    out, a = [], 0.0
    for p, d in zip(tune.pitches, tune.beats):
        out.append((base + p, a, float(d)))
        a += d
    return out


def render(notes, beat=0.32):
    T = max(a + d for _, a, d in notes)
    y = np.zeros(int((T * beat + 0.6) * SR))
    for p, a, d in notes:
        tone = organ_tone(CH.hz(p), d * beat, partials=5, rolloff=0.7, decay=1.0)
        i = int(a * beat * SR)
        y[i:i + len(tone)] += tone[: len(y) - i] * 0.3
    return Clip(y, SR).fade(0.01, 0.2).at_level(-20.0)


def chorale_phrases(book):
    out = []
    for c in book:
        if c.mode != "major":
            continue
        cur, prev = [], None
        for x in F.beat_labels(c):
            s = x["label"][:2] if x["label"] else None
            if s is not None:
                r = F.roman((s[0], s[1], 0), "major")
                if r != prev:
                    cur.append(r)
                    prev = r
            if x["fermata"] and cur:
                out.append(cur)
                cur, prev = [], None
        if cur:
            out.append(cur)
    return out


def names(level):
    letters = {0: "C", 2: "D", 4: "E", 5: "F", 7: "G", 9: "A", 11: "B"}
    return " ".join(letters.get(p % 12, "?") for p, _, _ in level)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. a tune, reduced (no harmony given: the most stable note on the strongest beat wins)
    t = [x for x in M.corpus() if x.name == TUNE][0]
    lv = G.reduce_levels(notes_of(t), None, span=1.0)
    for k in (1, 2, 3):
        lab.row(f"{TUNE}: a note every {2 ** k} beats", names(lv[k]))
    assert all(len(lv[k + 1]) <= len(lv[k]) for k in range(len(lv) - 1))

    # 2. parsing: trees for your progression, and the Catalan numbers
    hand = G.PCFG(["I", "vi", "iii", "IV", "ii", "V", "V7", "vii°"], prior=50.0)
    seq = PROGRESSION.split()
    n_trees = hand.count_parses(seq) if all(x in hand.index for x in seq) else 0
    lab.row(f"trees for {PROGRESSION} under the six rules", str(n_trees))
    plagal = G.PCFG(["I", "vi", "iii", "IV", "ii", "V", "V7", "vii°"], rules=G.RULES + [("TR", "SR", "TR")], prior=50.0)
    lab.row(f"... with the plagal rule TR -> SR TR", str(plagal.count_parses(seq) if all(x in plagal.index for x in seq) else 0))
    counts = [hand.count_parses(["I"] + ["IV", "V", "I"] * m) for m in (1, 2, 3)]
    catalan = [2, 14, 132]
    lab.row("trees for I (IV V I) repeated 1, 2, 3 times / Catalan numbers C2, C4, C6", f"{counts} / {catalan}")
    assert counts == catalan

    # 3. the grammar trained on Bach, against chord n-grams, on held-out phrases
    train, test = BC.split(BC.load(), offset=2)
    P, Q = chorale_phrases(train), chorale_phrases(test)
    cnt = Counter(x for p in P for x in p)
    vocab = [v for v, c in cnt.most_common() if c >= 5]
    fix = lambda S: [[x if x in vocab else "?" for x in p] for p in S if 2 <= len(p) <= 14]  # noqa: E731
    P2, Q2 = fix(P), fix(Q)
    vocab = vocab + ["?"]
    g = G.PCFG(vocab, seed=0)
    g.train(P2, iters=15)
    bits = {"no context": G.ngram_bits(P2, Q2, vocab, 1), "chord pairs": G.ngram_bits(P2, Q2, vocab, 2),
            "the six-rule grammar": G.pcfg_bits(g, Q2)}
    for k, v in bits.items():
        lab.row(f"bits per chord on {len(Q2)} held-out phrases: {k}", f"{v:.2f}")
    assert bits["chord pairs"] < bits["no context"]
    short = [p for p in Q if 2 <= len(p) <= 14]
    parsed = sum(1 for p in short if all(x in hand.index for x in p) and hand.viterbi(p) is not None)
    lab.row("held-out phrases the hand-set six rules parse", f"{parsed} of {len(short)}")

    # 4. melodies grown from the Tune's skeleton
    tune = notes_of(M.corpus([M.THE_TUNE])[0])
    first = [n for n in tune if n[1] < 16]
    skel = G.reduce_levels(first, chord_at, span=1.0)[2]
    r = np.random.default_rng(SEED)
    grown = []
    for k in range(3):
        surf, used = G.elaborate(skel, chord_at, r, depth=2, min_dur=1.0)
        grown.append(surf)
        lab.row(f"melody {k + 1} grown from the skeleton {names(skel)}", f"{names(surf)}  (rules: {', '.join(f'{a} {b}' for a, b in sorted(Counter(used).items()))})")

    # 5. Problem 3, for the ear: eight passages, each followed by two skeletons, one right, one wrong
    clips, answers = [], []
    pool = [x for x in M.corpus() if x.mode == "major"]
    for k in rng.permutation(len(pool))[:8]:
        nts = [n for n in notes_of(pool[k], base=72 - 12 * (max(pool[k].pitches) > 14)) if n[1] < 16]
        right = G.reduce_levels(nts, None, span=1.0)[2]
        wrong = [(G.scale_step(p, 1) if j in (1, 2) else p, a, d) for j, (p, a, d) in enumerate(right)]
        pair = [right, wrong] if rng.random() < 0.5 else [wrong, right]
        clips += [render(nts), render(pair[0]), render(pair[1])]
        answers.append(f"{pool[k].name}: {'A' if pair[0] is right else 'B'}")
    lab.audio = concat(clips, gap=0.9)
    lab.row("ear problem, the fitting skeleton for each passage (listen first)", ";  ".join(answers))

    fig, (a, b) = labs.figure(2)
    for k, row in enumerate(lv[:4]):
        for p, on, d in row:
            a.plot([on, on + d], [p - 14 * k] * 2, color=[labs.GOLD, "#7aa6d6", "#d66", "#9c6"][k], lw=4, solid_capstyle="butt")
    a.set_title(f"{TUNE}: the surface and its reductions (each level shifted down)")
    a.set_xlabel("beat")
    a.set_yticks([])
    ks = list(bits)
    b.bar(range(len(ks)), [bits[k] for k in ks], color=labs.GOLD)
    b.set_xticks(range(len(ks)))
    b.set_xticklabels(ks, fontsize=8)
    b.set_ylabel("bits per chord (lower predicts better)")
    b.set_title("Held-out chorale phrases")
    lab.fig = fig
    lab.note = ("A reduction keeps the stable notes on strong beats; a six-rule grammar of tonic, dominant and "
                "subdominant regions gives Catalan numbers of trees for repeated cadences and none at all to a plagal "
                "return; trained on Bach it explains phrases but predicts them no better than chord pairs; and melodies "
                "it grows obey the harmony but never repeat a motive.")
    return lab
