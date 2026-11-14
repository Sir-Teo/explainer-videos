"""Lab 23: chant to polyphony, computed: a chant classified into its mode and solmized, organum and its tritones,
an isorhythmic tenor built from a color and a talea and found again by a scan, a row of note shapes read in perfect
time, a fourteenth-century piece counted, and psalm verses in the eight modes named by ear."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import medieval as MD
from explainer.music.monochord import trecento as T
from explainer.music.monochord.instruments import choir as CH

TITLE = "Chant to polyphony, computed"
GOAL = ("Classify a chant by its final and range, solmize it with the fewest mutations, count the tritones that strict "
        "parallel organum makes, build an isorhythmic tenor and find its talea again, read note shapes by Franco's "
        "rules, count a fourteenth-century piece, and name the modes of psalm verses by ear.")
TASKS = [
    "Write a CHANT of your own (key numbers, white notes and B-flat, ending on D, E, F or G). Which mode does the rule give, and how many mutations does it need?",
    "Change COLOR and TALEA. When do they line up again? Does the scan find the talea in the tenor you built, and at which other lags?",
    "Choose a PIECE from the corpus (part of its title). Is its rhythm repeated at some lag far above chance? How many of its intervals on the beat are perfect?",
]
CHANT = [62, 65, 67, 69, 67, 65, 64, 62, 60, 62, 64, 65, 64, 62]
COLOR = [53, 55, 57, 58, 57, 55, 53, 52, 50]
TALEA = [3, 3, 2, 1, -3]
SHAPES = "BSSBSBSSSSB"
PIECE = "Lugent"


def sing(notes, unit=0.36):
    y = CH.sing([(p, a * unit, d * unit) for p, a, d in notes], "tenor", "a")
    return Clip(y / max(np.abs(y).max(), 1e-9) * 0.4, SR).fade(0.02, 0.2).at_level(-20.0)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. a chant: its mode and its syllables
    m = MD.classify(CHANT)
    syl, mut = MD.solmize(CHANT)
    lab.row("your chant's mode (final and range)", f"{m}, {MD.MODES[m][0]}: final {MD.LETTERS[MD.MODES[m][1] % 12]}, reciting tone {MD.LETTERS[MD.MODES[m][2] % 12]}")
    lab.row("solmized with the fewest mutations", f"{' '.join(syl)}  ({len(mut)} mutation{'s' if len(mut) != 1 else ''})")
    for k in range(1, 9):
        assert MD.classify(MD.psalm_tone(k)) == k

    # 2. organum: strict parallel fifths and fourths below, and their tritones
    for steps, name in ((-4, "fifth"), (-3, "fourth")):
        lo = MD.parallel(CHANT, steps)
        lab.row(f"strict parallel organum a {name} below: tritones", str(MD.tritones(CHANT, lo)))
    ench = MD.enchiriadis(CHANT, floor=57)
    lab.row("by the Enchiriadis rule (never below A): tritones, and the last interval", f"{MD.tritones(CHANT, ench)}, {'unison' if ench[-1] == CHANT[-1] else 'not a unison'}")

    # 3. isorhythm: build a tenor, then find its talea from the rhythm alone
    per = MD.periods(len(COLOR), sum(1 for d in TALEA if d > 0))
    tenor = MD.isorhythm(COLOR, TALEA)
    lab.row("color and talea line up again after", f"{per['lcm']} notes: {per['colors']} colors, {per['taleae']} taleae")
    voice = [(p, int(a * 24), int(d * 24)) for p, a, d in tenor]
    span = sum(abs(d) for d in TALEA)
    bar = 3 * 24 if span % 3 == 0 else 24
    sc = MD.talea_scan(voice, bar, lo=1)
    lab.row("the scan's best lag (bars) and share; the talea's length in bars", f"{sc['lag']}, {sc['share']:.2f}; {span * 24 / bar:g}")
    assert sc["share"] > 0.9

    # 4. Franco's rules
    vals = MD.read_perfect(SHAPES)
    lab.row(f"{SHAPES} in perfect time (semibreves)", f"{' '.join(map(str, vals))} = {sum(vals)} = {sum(vals) / 3:g} perfections")

    # 5. a piece from the corpus
    book = T.load()
    pc = [p for p in book if PIECE.lower() in (p.title + p.name).lower()][0]
    best = max((MD.talea_scan(v, pc.bar) | {"voice": j} for j, v in enumerate(pc.voices)), key=lambda s: s["share"])
    chance = MD.shuffled_share(pc.voices[best["voice"]], pc.bar, rng, trials=5)
    ob = MD.on_off_beat(pc)
    cad = MD.cadences(pc)
    lab.row(f"{pc.title} ({pc.composer}): best talea lag (voice {best['voice'] + 1})", f"{best['lag']} bars, share {best['share']:.2f} (shuffled {chance:.2f})")
    lab.row("intervals on the beat: perfect, imperfect, dissonant", ", ".join(f"{ob['on'][k]:.2f}" for k in ("perfect", "imperfect", "dissonant")))
    lab.row("sixth-to-octave cadences, with a leading tone, with two", f"{cad['sixth_octave']}, {cad['leading_tone']}, {cad['double']}")

    # 6. Problem 3, for the ear: psalm verses in the eight modes, shuffled
    order = rng.permutation(8) + 1
    lab.audio = concat([sing([(p, k, 1.0) for k, p in enumerate(MD.psalm_tone(int(k)))]) for k in order], gap=1.0)
    lab.row("ear problem, the modes in the order sung (listen first)", ", ".join(str(int(k)) for k in order))

    fig, (a, b) = labs.figure(2)
    n_col = len(COLOR)
    for k, (p, on, d) in enumerate(tenor):
        a.plot([on, on + d], [p, p], color=[labs.GOLD, "#7aa6d6", "#d66", "#9c6", "#c9c"][(k // n_col) % 5], lw=5, solid_capstyle="butt")
    for t in range(0, int(max(on + d for _, on, d in tenor)) + 1, span):
        a.axvline(t, color="#888", lw=0.5)
    a.set_title("Isorhythmic tenor: colour by statement of the color, lines at each talea")
    a.set_xlabel("time (breves)")
    a.set_ylabel("key number")
    lags = sorted(best["scan"])
    b.plot(lags, [best["scan"][k] for k in lags], color=labs.GOLD)
    b.axhline(chance, color="#888", ls="--")
    b.set_title(f"{pc.title[:40]}: rhythm repeated at each lag")
    b.set_xlabel("lag (bars)")
    b.set_ylabel("share of bars repeated")
    lab.fig = fig
    lab.note = ("The mode follows from a chant's last note and range; solmization is a shortest path; strict parallel "
                "organum walks into tritones that a boundary rule avoids; an isorhythmic tenor's talea can be found "
                "from its rhythm alone, far above the shuffled chance level; Franco's rules always fill whole "
                "perfections; and a century's style can be counted, with the editors' accidentals counted with it.")
    return lab
