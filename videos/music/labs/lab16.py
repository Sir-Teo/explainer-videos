"""Lab 16: count the first-species lines over a cantus, see which rules do the work, check a line of your own,
write in the other species, measure how independent two voices are, and name the motion between them by ear."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import Clip, concat
from explainer.music.monochord import chords as CH
from explainer.music.monochord import counterpoint as K
from explainer.music.monochord.partkit import organ_tone

SHARP = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")


def nm(p: int) -> str:
    return f"{SHARP[p % 12]}{p // 12 - 1}"

TITLE = "Two voices, by rule and by count"
GOAL = ("Count the lines that obey Fux's twelve rules over a cantus firmus, find which rules do the work and which add "
        "nothing, check a line of your own, write the other four species, measure how independent two voices are, and "
        "hear the four kinds of motion.")
TASKS = [
    "Set CANTUS to a cantus of your own: 8 to 12 white keys, mostly steps, ending on its first note (try [60, 62, 65, 64, 62, 67, 65, 64, 62, 60]). How does the number of good lines change with its length and its range?",
    "MY_LINE breaks two rules. Repair it with as few changed notes as you can, then make it score higher than the best sampled line. Which preferences did you trade?",
    "Set SPECIES to 2, 3, 4 and 5. In which species do the voices begin together least often, and why does fourth species never fuse?",
]
CANTUS = K.FUX_DORIAN       # MIDI notes of the cantus firmus (Fux's D F E D G F A G F E D)
MY_LINE = [74, 72, 72, 74, 71, 72, 72, 76, 74, 73, 74]   # a first-species line above it, one note per bar
SPECIES = 3                 # 2, 3, 4 or 5: which species to write above the cantus
SR = 48_000
MOTION = {"parallel": (+2, +2), "similar": (+5, +2), "contrary": (+2, -2), "oblique": (0, -2)}


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    cf = list(CANTUS)

    # 1. Problem 1: the funnel, rule by rule
    f = K.funnel(cf)
    for name, n in f:
        lab.row("any notes at all, from the keys allowed" if name == "no rules" else f"+ {K.NAMES[name]}", f"{n:,}")
    good = f[-1][1]
    lab.row("share of the sequences that obey every rule", f"{good / f[0][1]:.2e}")
    if cf == K.FUX_DORIAN:
        assert good == 152

    # 2. Problem 2: take one rule away at a time
    rows = []
    for r in K.RULES:
        n = K.count(cf, tuple(x for x in K.RULES if x != r))
        rows.append((r, n))
        lab.row(f"without '{K.NAMES[r]}'", f"{n:,}  ({n / good:.1f} times as many)")
    if cf == K.FUX_DORIAN:
        assert dict(rows)["parallel"] == good          # the direct-motion rule already forbids parallel fifths

    # 3. Problem 1 again, by hand: what is wrong with MY_LINE?
    errs = K.check(cf, MY_LINE)
    lab.row("your line", " ".join(nm(p) for p in MY_LINE))
    lab.row("rules it breaks", ";  ".join(f"bar {i + 1}: {K.NAMES[r]}" for i, r in errs) or "none: a good first-species line")
    lab.row("its score by Fux's preferences (higher is better)", f"{K.score(cf, MY_LINE):.1f};  the best of 3000 sampled lines scores {K.score(cf, K.best(cf, tries=3000)):.1f}")

    # 4. Problem 3: the other species
    line = K.species(cf, SPECIES, rng=np.random.default_rng(100 + SPECIES), tries=60)
    cf_ev = [(c, 4.0 * k, 4.0) for k, c in enumerate(cf)]
    diss = [(p, a) for p, a, _ in line if a % 4 and (p - cf[min(int(a // 4), len(cf) - 1)]) % 12 not in K.CONSONANT]
    lab.row(f"species {SPECIES}: notes", " ".join(nm(p) for p, _, _ in line))
    lab.row(f"species {SPECIES}: dissonances off the beat", ";  ".join(f"{nm(p)} (bar {int(a // 4) + 1}, beat {int(a % 4) + 1})" for p, a in diss) or "none")

    # 5. Problem 4: independence, from organum to florid
    table = {"organum": K.independence([(c - 7, 4.0 * k, 4.0) for k, c in enumerate(cf)], cf_ev),
             "first species": K.independence(*K.first_species_events(cf, K.best(cf, tries=1000)))}
    for n in (2, 3, 4, 5):
        table[f"species {n}"] = K.independence(line if n == SPECIES else K.species(cf, n, rng=np.random.default_rng(100 + n), tries=40), cf_ev)
    for name, ind in table.items():
        lab.row(f"{name}: begin together, fused, contrary", f"{100 * ind['together']:.0f}%,  {100 * ind['fused']:.0f}%,  {100 * ind['contrary']:.0f}%")
    assert table["organum"]["fused"] == 1.0
    if cf == K.FUX_DORIAN:
        assert table["species 4"]["fused"] == 0.0 and table["species 4"]["together"] < table["first species"]["together"]

    # 6. Ear problem: eight moves, each one of the four motions
    answers, clips = [], []
    for _ in range(8):
        kind = list(MOTION)[int(rng.integers(0, 4))]
        lo = int(rng.choice([53, 55, 57, 60]))
        hi = lo + int(rng.choice([3, 4, 8, 9]))
        du, dl = MOTION[kind]
        y = np.zeros(int(2.4 * SR))
        for t, (u, l) in enumerate([(hi, lo), (hi + du, lo + dl)]):
            tone = sum(organ_tone(CH.hz(n), 1.1, partials=6, rolloff=0.7, decay=1.2) for n in (u, l))
            i = int(t * 1.1 * SR)
            y[i:i + len(tone)] += tone[: len(y) - i]
        clips.append(Clip(y, SR).fade(0.01, 0.2).at_level(-20.0))
        answers.append(kind)
    lab.audio = concat(clips, gap=0.9)
    lab.row("ear problem, the eight moves (listen first)", ";  ".join(answers))

    fig, (a, b) = labs.figure(2)
    names = ["none"] + [str(i + 1) for i in range(len(f) - 1)]
    a.bar(range(len(f)), [n for _, n in f], color=labs.GOLD)
    a.set_yscale("log")
    a.set_xticks(range(len(f)))
    a.set_xticklabels(names)
    a.set_xlabel("rules added, in Fux's order")
    a.set_title(f"Lines over the cantus: {f[0][1]:,} to {good:,}")
    keys = list(table)
    x = np.arange(len(keys))
    b.bar(x - 0.2, [table[k]["together"] for k in keys], width=0.4, color=labs.GOLD, label="notes begin together")
    b.bar(x + 0.2, [table[k]["fused"] for k in keys], width=0.4, color="#7DD3FC", label="fused moments")
    b.set_xticks(x)
    b.set_xticklabels([k.replace("species ", "sp. ") for k in keys], rotation=20)
    b.set_title("How independent: organum to fifth species")
    b.legend(frameon=False)
    lab.fig = fig
    lab.note = ("Twelve rules leave a few hundred lines out of millions; almost every rule keeps two voices from fusing "
                "into one or keeps one voice from falling apart; and each species after the first adds a way for the "
                "voices to move at different times.")
    return lab
