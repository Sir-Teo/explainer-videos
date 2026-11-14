"""Lab 15: key signatures and relations, a counting proof about rare intervals, a key finder with learnt profiles, and cadences by ear."""

from itertools import combinations

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import Clip, concat
from explainer.music.monochord import chords as CH
from explainer.music.monochord import key as K
from explainer.music.monochord import melody as M
from explainer.music.monochord import scales as S
from explainer.music.monochord.partkit import organ_tone

TITLE = "Keys, found and mapped"
GOAL = ("Work out key signatures and the notes two keys share, count how many major scales contain a pair of notes, find "
        "the key of every tune in the corpus with profiles learnt from the others, and name cadences by ear.")
TASKS = [
    "Set NOTES to 3, 5 and 8. How many notes does the key finder need before it is right four times in five? Which tunes does it still misread with all of their notes?",
    "Set PROFILES to 'ratings'. Which wrong key does it name most often, and where is that key on the circle of fifths?",
    "Set PAIR to (0, 7), (0, 4) and (11, 5). Check the count against the interval vector, and explain the factor of two for the tritone.",
]
NOTES = None                # how many notes of each tune the key finder hears (None: all of them)
PROFILES = "learnt"         # "learnt" (from the other tunes), "counts" (Temperley 2007) or "ratings" (Krumhansl and Kessler 1982)
PAIR = (11, 5)              # two pitch classes: B and F
SR = 48_000
CADENCES = {"authentic": [(5, "major"), (7, "7"), (0, "major")], "half": [(0, "major"), (5, "major"), (7, "major")], "plagal": [(0, "major"), (5, "major"), (0, "major")],
            "deceptive": [(5, "major"), (7, "7"), (9, "minor")]}


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    corpus = M.corpus()

    # 1. Problem 1: signatures and relations
    e, eb = (4, "major"), (3, "major")
    lab.row("four sharps", f"{K.key_name(e)}; relative minor {K.key_name(K.relative(e))}  ({K.shared_notes(e, K.relative(e))} notes shared)")
    lab.row("three flats", f"{K.key_name(eb)}; parallel minor {K.key_name(K.parallel(eb))}  ({K.shared_notes(eb, K.parallel(eb))} notes shared)")
    lab.row("E major and E flat major", f"{K.fifths_apart(e, eb)} steps apart on the circle of fifths; {K.shared_notes(e, eb)} notes shared")
    assert K.signature(e) == 4 and K.signature(eb) == -3

    # 2. Problem 2: a pair of notes lies in as many major scales as its interval class occurs in one
    vec = S.interval_vector(K.MAJOR_SCALE)
    counts = {}
    for a, b in combinations(range(12), 2):
        ic = min((b - a) % 12, (a - b) % 12)
        counts.setdefault(ic, set()).add(len(K.keys_containing([a, b])))
    lab.row("a major scale's interval vector", " ".join(str(v) for v in vec))
    lab.row("major scales containing a pair of notes, by interval class", ";  ".join(f"{ic}: {sorted(c)[0]}" for ic, c in sorted(counts.items())))
    lab.row(f"the pair {K.NAMES_FLAT[PAIR[0]]}, {K.NAMES_FLAT[PAIR[1]]}", ", ".join(K.key_name(k) for k in K.keys_containing(PAIR)))
    assert all(len(c) == 1 for c in counts.values()) and [sorted(counts[ic])[0] for ic in range(1, 7)] == [2, 5, 4, 3, 6, 2]

    # 3. Problem 4: the key of every tune, in every transposition
    wrong, right, total = {}, 0, 0
    for i, m in enumerate(corpus):
        prof = {"learnt": K.learn_profiles(corpus[:i] + corpus[i + 1:]), "counts": (K.TEMPERLEY_MAJOR, K.TEMPERLEY_MINOR), "ratings": (K.KK_MAJOR, K.KK_MINOR)}[PROFILES]
        p, b = (m.pitches, m.beats) if NOTES is None else (m.pitches[:NOTES], m.beats[:NOTES])
        for tr in range(12):
            got = K.find_key(K.distribution([x + tr for x in p], b), prof) if PROFILES == "ratings" else K.bayes_key([x + tr for x in p], b, prof)
            total += 1
            if got == (tr, m.mode):
                right += 1
            elif tr == 0:
                wrong[m.name] = K.key_name(got)
    lab.row(f"keys found ({PROFILES} profiles, {'all' if NOTES is None else NOTES} notes)", f"{right} of {total}  ({100 * right / total:.0f} in a hundred)")
    lab.row("tunes misread (written with C as home)", ";  ".join(f"{n}: {k}" for n, k in wrong.items()) or "none")
    maj, _ = K.learn_profiles(corpus)
    lab.row("profile counted from the corpus against the listeners' ratings", f"r = {np.corrcoef(maj, K.KK_MAJOR)[0, 1]:.2f}")
    lab.row("C major's nearest keys, by profile", ";  ".join(f"{K.key_name(k)} {r:.2f}" for k, r in K.nearest_keys((0, 'major'), top=5)))

    # 4. Problem 3, for the ear: eight cadences
    answers, clips = [], []
    for _ in range(8):
        name = list(CADENCES)[int(rng.integers(0, 4))]
        tonic = int(rng.integers(55, 66))
        y, t, cur = np.zeros(int(4.2 * SR)), 0.0, None
        for off, kind in CADENCES[name]:
            pcs = [(tonic + off + h) % 12 for h in CH.offsets(kind)]
            cur = tuple(sorted(60 + ((p - 60) % 12) for p in pcs[:3])) if cur is None else CH.nearest_voicing(cur, pcs[:3] if len(pcs) == 3 else pcs[1:], low=55, high=74)
            notes = [36 + (tonic + off) % 12 + (12 if (tonic + off) % 12 < 5 else 0)] + list(cur)
            tone = sum(organ_tone(CH.hz(n), 1.5 if t > 1.5 else 0.95, partials=6, rolloff=0.7, decay=1.5) for n in notes)
            i = int(t * SR)
            y[i:i + len(tone)] += tone[: len(y) - i]
            t += 0.95
        clips.append(Clip(y, SR).fade(0.01, 0.2).at_level(-20.0))
        answers.append(name)
    lab.audio = concat(clips, gap=0.9)
    lab.row("ear problem, the eight cadences (listen first)", ";  ".join(answers))

    fig, (a, b) = labs.figure(2)
    x = np.arange(12)
    a.bar(x - 0.2, K.KK_MAJOR / K.KK_MAJOR.sum(), width=0.4, color=labs.GOLD, label="listeners' ratings (1982)")
    a.bar(x + 0.2, maj / maj.sum(), width=0.4, color="#888", label="time on each note, 54 tunes")
    a.set_xticks(x)
    a.set_xticklabels(K.NAMES_FLAT)
    a.set_title("A key's profile, asked and counted")
    a.legend(frameon=False)
    t = K.torus()["angles"]
    for k, (th, ph) in t.items():
        b.text(th, ph, K.key_name(k, short=True), ha="center", va="center", color=labs.GOLD if k[1] == "major" else "#7DD3FC", fontsize=11)
    b.set_xlim(-0.05, 1.05)
    b.set_ylim(-0.05, 1.05)
    b.set_title("The 24 keys on Krumhansl and Kessler's torus, laid flat")
    b.set_xlabel("first angle (the circle of fifths)")
    b.set_ylabel("second angle")
    lab.fig = fig
    lab.note = ("A key is a ranking of the twelve notes that matches how often they occur; a key finder that counts needs about "
                "five notes; the rarest interval of the scale is its best clue; and keys that share notes and chords lie "
                "side by side on a torus.")
    return lab
