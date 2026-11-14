"""Lab 25: the Baroque, computed: Galilei's weights, Corelli's bass figured from his violins and realized again, a
ritornello finder, the colours of keys in a temperament you choose, ornaments and inequality, and twelve cadences in
Werckmeister III ranked by ear."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import baroque as B
from explainer.music.monochord import tuning as TU
from explainer.music.monochord.partkit import organ_tone
from explainer.music.monochord.score import Pitch
from explainer.music.monochord.score import figured as FIG

TITLE = "The Baroque, computed"
GOAL = ("Find the weights that make musical intervals on a string, figure Corelli's bass from his violins and realize it "
        "again, find a ritornello's returns at any transposition, measure the colour of every key in a temperament, "
        "apply ornaments and inequality, and rank twelve keys of Werckmeister III by ear.")
TASKS = [
    "Change RATIO. What weight ratio does it need on equal strings? What would the Pythagorean legend have predicted, and what interval would that make?",
    "Change TOP, where the realizer starts its top voice. How much do the realizations of Corelli's bass differ, and how close does any come to his first violin?",
    "Choose a TEMPERAMENT: 'meantone', 'werckmeister', 'equal' or a number of equal steps. Which keys have the purest and roughest major thirds?",
]
RATIO = 1.5
TOP = 77
TEMPERAMENT = "werckmeister"


def tuning():
    if TEMPERAMENT == "meantone":
        return TU.meantone()
    if TEMPERAMENT == "werckmeister":
        return TU.werckmeister3()
    if TEMPERAMENT == "equal":
        return TU.equal(12)
    return TU.equal(int(TEMPERAMENT))


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. Galilei
    w = B.weights_for(RATIO)
    legend = 1200 * np.log2(np.sqrt(RATIO))
    lab.row(f"frequency ratio {RATIO}: weights needed / the legend's weights", f"{w:.3f} / {RATIO} (which makes {legend:.0f} cents)")

    # 2. Corelli figured and realized
    d = B.load()["corelli"]
    v1, v2, bass = d["Violino I."], d["Violino II."], d["Violone e Organo"]
    fl = B.figured_line(bass, [v1, v2])
    basses = [Pitch.from_midi(p, flats=True) for p, _, _, _ in fl]
    r = FIG.realize(basses, [f for *_, f in fl], key=-1, voices=3, low=55, high=84, top=TOP)
    ag = B.agreement(r["chords"], bass, [v1, v2])
    lab.row("Corelli's Grave: bass notes, figures used", f"{len(fl)}: " + ", ".join(f"{f or '5/3'} {n}" for f, n in sorted(__import__('collections').Counter(f for *_, f in fl).items(), key=lambda x: -x[1])))
    lab.row(f"realized with the top voice near {TOP}: Corelli's notes held, top voice = first violin, parallels",
            f"{ag['pitch_classes']:.2f}, {ag['top']:.2f}, {r['parallels']}")
    assert r["parallels"] == 0

    # 3. ritornello returns in a built line
    head = [(72, 0, 0.5), (76, 0.5, 0.5), (79, 1, 0.5), (76, 1.5, 0.5), (84, 2, 1), (83, 3, 0.5), (81, 3.5, 0.5)]
    line = head + [(74 + k % 3, 4 + 0.5 * k, 0.5) for k in range(8)] + [(p + 5, o + 8, d_) for p, o, d_ in head]
    found = B.ritornello_returns(line, head=6)
    lab.row("a theme, an episode, the theme a fourth higher: returns found (onset, transposition)", "; ".join(f"{f['onset']:g}, {f['transpose']:+d}" for f in found))

    # 4. keys in a temperament
    t = tuning()
    kc = B.key_colours(t)
    best = min(kc, key=lambda x: abs(x["third_error"]))
    worst = max(kc, key=lambda x: abs(x["third_error"]))
    lab.row(f"{t.name}: purest and roughest major thirds (cents from 5:4)", f"{best['key']} {best['third_error']:+.1f}, {worst['key']} {worst['third_error']:+.1f}")

    # 5. ornaments
    tr = B.trill(72, 0, 1, n=8, turn=True)
    lab.row("a trill on C over one beat: notes", " ".join(str(p) for p, _, _ in tr))

    # 6. Problem 3: twelve cadences in Werckmeister III, shuffled
    wm = TU.werckmeister3()
    order = rng.permutation(12)
    clips = []
    for k in order:
        chords = [(0, 4, 7), (5, 9, 0), (7, 11, 2), (0, 4, 7)]
        y = np.zeros(int(4.8 * SR))
        for j, ch in enumerate(chords):
            for x in ch:
                pc = (k + x) % 12
                m = 60 + wm.cents[pc] / 100.0 + (12 if pc < k else 0)
                tone = organ_tone(440 * 2 ** ((m - 69) / 12), 1.1, partials=6, rolloff=0.75)
                i = int(j * 1.1 * SR)
                y[i:i + len(tone)] += tone[: len(y) - i] * 0.2
        clips.append(Clip(y, SR).fade(0.02, 0.2).at_level(-20.0))
    lab.audio = concat(clips, gap=0.8)
    errs = {r_["key"]: r_["third_error"] for r_ in B.key_colours(wm)}
    lab.row("ear problem: the keys in the order played, with their thirds' error (listen first)",
            ", ".join(f"{B.KEY_NAMES[k]} {errs[B.KEY_NAMES[k]]:+.1f}" for k in order))

    fig, (a, b) = labs.figure(2)
    keys = [x["key"] for x in kc]
    a.bar(range(12), [x["third_error"] for x in kc], color=labs.GOLD)
    a.set_xticks(range(12))
    a.set_xticklabels(keys, fontsize=8)
    a.set_ylabel("major third, cents from 5:4")
    a.set_title(f"{t.name}: the colour of each key")
    for p, o, d_ in v1[:60]:
        b.plot([o / 24, (o + d_) / 24], [p, p], color=labs.GOLD, lw=3)
    for ch, (p, o, d_) in zip(r["chords"][:40], bass[:40]):
        b.plot([o / 24, (o + d_) / 24], [max(ch), max(ch)], color="#d66", lw=2)
    b.set_title("Corelli's first violin (gold) and the realizer's top voice (red)")
    b.set_xlabel("quarter notes")
    lab.fig = fig
    lab.note = ("An octave needs four times the weight, as Galilei found; a figured bass carries most of the harmony and none "
                "of the melody; returns can be found at any transposition by matching intervals; and in a well "
                "temperament every key has its own colour, from nearly pure to Pythagorean.")
    return lab
