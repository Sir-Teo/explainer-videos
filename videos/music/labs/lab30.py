"""Lab 30: sound itself, computed: tape operations on a bell, a phasing engine for any figure, a Poisson cloud checked
against its law, a sieve of your own, a cluster's beats, and six clouds, random or even, sorted by ear."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import soundmass as S
from explainer.music.monochord.instruments import percussion as PC
from explainer.music.monochord.partkit import organ_tone

TITLE = "Sound itself, computed"
GOAL = ("Speed, reverse and cut a recorded sound; find the alignments two loops of a figure pass through; check a random "
        "cloud against Poisson's law; build scales from sieves; and hear random and even timing apart.")
TASKS = [
    "Choose a FIGURE of pitch classes. Through how many different alignments does it pass when phased against itself, and which are richest?",
    "Choose a SIEVE as (modulus, residue) terms. What scale does it make, and after how many semitones does it repeat?",
    "Change RATE, the cloud's notes per second. How does the spread of the per-second counts grow with the rate?",
]
FIGURE = (0, 2, 4, 0, 2, 4, 7, 4, 2, 0, 2, 4)
SIEVE = [[(5, 0)], [(7, 2)]]
RATE = 5.0


def tick(m, seconds=0.25):
    return organ_tone(440 * 2 ** ((m - 69) / 12), seconds, partials=5, rolloff=0.6, decay=10.0) * 0.3


def cloud(times, pitches, seconds=6.0):
    y = np.zeros(int((seconds + 0.6) * SR))
    for t, p in zip(times, pitches):
        s = tick(p)
        i = int(t * SR)
        y[i:i + len(s)] += s[: len(y) - i]
    return Clip(y, SR).fade(0.01, 0.2).at_level(-20.0)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. tape operations on a bell
    bell = np.asarray(PC.bell(392.0, seconds=2.0), float)
    lab.row("a bell's attack time: as struck / reversed / attack cut (s)",
            f"{S.attack_time(bell):.3f} / {S.attack_time(S.reverse(bell)):.3f} / {S.attack_time(S.cut_attack(bell, 0.25)):.3f}")

    # 2. phasing
    pats = S.phase_patterns(FIGURE)
    lab.row(f"figure {FIGURE}: unisons at each shift", " ".join(str(p["unisons"]) for p in pats))
    lab.row("distinct pairs at each shift (richness)", " ".join(str(p["distinct"]) for p in pats))

    # 3. sieves
    sv = S.sieve(SIEVE, 72)
    period = next((p for p in range(1, 72) if all((x + p in sv) for x in sv if x + p < 72)), None)
    lab.row(f"sieve {SIEVE}: first notes, and its period in semitones", f"{sv[:12]} ..., {period}")

    # 4. a Poisson cloud
    on = S.poisson_onsets(RATE, 600.0, rng)
    counts = S.counts_per_cell(on, 600.0, 1.0)
    lab.row(f"cloud at {RATE:g} a second for ten minutes: mean and variance of per-second counts",
            f"{counts.mean():.2f}, {counts.var():.2f} (Poisson: both {RATE:g})")
    assert abs(counts.mean() - RATE) < 0.5

    # 5. a cluster
    lab.row("beat rates in a quarter-tone cluster of five around A4 (Hz)", ", ".join(f"{b:.1f}" for b in S.beat_rates(S.cluster(69, 2.0, 5))))

    # 6. Problem 3: six clouds, random or even
    kinds = list(rng.permutation(["random"] * 3 + ["even"] * 3))
    clips = []
    for k in kinds:
        t = S.poisson_onsets(4.0, 6.0, rng)
        if k == "even":
            t = np.linspace(0, 6.0, len(t), endpoint=False)
        clips.append(cloud(t, rng.uniform(60, 84, len(t))))
    lab.audio = concat(clips, gap=1.0)
    lab.row("ear problem: the six clouds in the order played (listen first)", ", ".join(kinds))

    fig, (a, b) = labs.figure(2)
    hist = np.bincount(counts, minlength=20)[:20]
    from math import exp, factorial
    a.bar(range(20), hist, color=labs.GOLD, label="counted")
    a.plot(range(20), [600 * exp(-RATE) * RATE ** k / factorial(k) for k in range(20)], "o", color=labs.RED, label="Poisson")
    a.set_xlabel("notes in a second")
    a.legend(frameon=False)
    a.set_title(f"a cloud at {RATE:g} notes a second")
    b.plot([p["shift"] for p in pats], [p["unisons"] for p in pats], "o-", color=labs.GOLD, label="unisons")
    b.plot([p["shift"] for p in pats], [p["distinct"] for p in pats], "s-", color=labs.BLUE, label="distinct pairs")
    b.set_xlabel("notes ahead")
    b.legend(frameon=False)
    b.set_title("a figure phased against itself")
    lab.fig = fig
    lab.note = ("A tape machine changes pitch and time together; a phased figure walks through a fixed set of alignments, "
                "symmetric about the middle; and a random cloud's counts have a variance equal to their mean.")
    return lab
