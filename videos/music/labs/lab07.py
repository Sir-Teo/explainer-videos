"""Lab 7: a plucked string in three lines, a stiff string's partials, Helmholtz's corner under a bow, and five bow forces to rank by ear."""

import math

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import Clip, concat
from explainer.music.monochord.instruments import strings as S

TITLE = "Strings, computed: a loop, a stiff wire and a bow"
GOAL = ("Write Karplus and Strong's plucked string yourself and find its pitch, compute how far a stiff string's partials "
        "are from whole multiples, bow Monochord's string and check Helmholtz's two rules, and rank five bow forces by ear.")
TASKS = [
    "Set N to 122 and to 488. What happens to the pitch, and to how long the note lasts? Why does the high note die sooner?",
    "Set B to 0.004, the size found in a piano's top octave. How sharp is the 8th partial now? Would you still call the tone harmonic?",
    "Set BETA to 0.05 and to 0.2. Check the slip fraction and the flyback speed against Problem 2 each time.",
]
N = 244          # numbers in Karplus and Strong's loop
B = 0.0004       # the string's stiffness (Problem 1)
F1 = 262.0       # its fundamental, Hz
BETA = 0.1       # where the bow is: fraction of the string from the bridge
SR = 48_000


def pluck(n: int, seconds: float, rng) -> np.ndarray:
    """Karplus and Strong: a loop of n random numbers; each output is read from the loop and replaced by the average of
    itself and the number read just before it."""
    loop = rng.uniform(-1, 1, n)
    out = np.empty(int(seconds * SR))
    before = 0.0
    for i in range(len(out)):
        out[i] = loop[i % n]
        loop[i % n], before = 0.5 * (loop[i % n] + before), loop[i % n]
    return out


def pitch_of(y: np.ndarray, guess: float) -> float:
    """The pitch of a nearly periodic sound, from the peak of its autocorrelation near a guess (parabolic interpolation)."""
    y = y[: int(0.5 * SR)] - np.mean(y[: int(0.5 * SR)])
    lags = np.arange(int(SR / guess * 0.9), int(SR / guess * 1.1) + 1)
    ac = np.array([float(np.dot(y[:-k], y[k:])) for k in lags])
    i = int(np.clip(np.argmax(ac), 1, len(ac) - 2))
    a, b, c = ac[i - 1], ac[i], ac[i + 1]
    return SR / (lags[i] + 0.5 * (a - c) / (a - 2 * b + c))


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. a pluck in three lines
    y = pluck(N, 1.5, rng)
    hz = pitch_of(y, SR / N)
    lab.row(f"a loop of {N} numbers", f"sounds at {hz:.2f} Hz; the loop alone would give {SR / N:.2f}, the loop and its average {SR / (N + 0.5):.2f}")
    early, late = float(np.sqrt(np.mean(y[: SR // 10] ** 2))), float(np.sqrt(np.mean(y[-SR // 10:] ** 2)))
    lab.row("its level after 1.4 seconds", f"{20 * math.log10(late / early):+.1f} dB")
    assert abs(1200 * math.log2(hz / (SR / (N + 0.5)))) < 1.0           # the average is half a sample of extra delay

    # 2. a stiff string (Problem 1)
    def partial(n):
        return n * F1 * math.sqrt((1 + B * n * n) / (1 + B))

    for n in (2, 4, 8):
        lab.row(f"partial {n} of a string with B = {B:g}", f"{partial(n):.1f} Hz, {1200 * math.log2(partial(n) / (n * F1)):.1f} cents sharp of {n * F1:.0f}")
    if B == 0.0004 and F1 == 262.0:
        assert abs(1200 * math.log2(partial(8) / (8 * F1)) - 21.5) < 0.1

    # 3. Helmholtz's corner (Problem 2)
    limit = S.schelleng(BETA, 0.2, 0.25, 0.97)[1]
    bow = S.Bow(speed=0.2, force=0.28 * limit, at=BETA)
    d = S.bowed(196.0, bow, seconds=1.5)
    r = S.bow_regime(d)
    p = int(round(d["period"]))
    v = d["v"][-2 * p:]
    slipping = d["slipping"][-2 * p:] > 0.5
    flyback = float(v[slipping].mean()) / bow.speed
    lab.row(f"bowed at {BETA:g} of its length", f"{r['kind']}: it slips for {100 * r['slip_fraction']:.1f}% of each period (Helmholtz: {100 * d['beta']:.1f}%)")
    lab.row("its speed while slipping", f"{flyback:.1f} times the bow's (Helmholtz: {-(1 - d['beta']) / d['beta']:.1f})")
    if BETA == 0.1:
        assert r["kind"] == "Helmholtz" and abs(r["slip_fraction"] - d["beta"]) < 0.02 and abs(flyback + 9) < 1.0

    # 4. the ear problem (Problem 3): one note at five bow forces
    body = S.violin_body()
    top = S.schelleng(0.1, 0.2, 0.25, 0.97)[1]
    forces = [0.014 * top, 0.25 * top, 0.45 * top, 0.8 * top, 4.0 * top]
    order = rng.permutation(5)
    notes, kinds = [], []
    for f in forces:
        b5 = S.Bow(speed=0.2, force=f, at=0.1)
        kw = dict(press=f) if f < 0.05 * top else {}
        kinds.append(S.bow_regime(S.bowed(196.0, b5, seconds=1.2, **kw))["kind"])
        notes.append(Clip(body.play(S.bowed_note(196.0, 1.2, b5, **kw)), SR).at_level(-20.0))
    lab.audio = concat([notes[j] for j in order], gap=0.35)
    lab.row("ear problem, the order of forces (listen first)", "; ".join(f"{forces[j]:.2f} N" for j in order))
    lab.row("  what each one is", "; ".join(f"{forces[j]:.2f} N: {kinds[j]}" for j in range(5)))
    assert kinds[1:4] == ["Helmholtz"] * 3 and kinds[0] != "Helmholtz" and kinds[4] != "Helmholtz"

    fig, (a, b) = labs.figure(2)
    ns = np.arange(1, 21)
    a.plot(ns, [1200 * math.log2(partial(int(n)) / (n * F1)) for n in ns], "o-", color=labs.GOLD, ms=3, lw=1.2)
    a.axhline(100, color="#888", lw=0.6, ls=":")
    a.set_title(f"A stiff string, B = {B:g}")
    a.set_xlabel("partial")
    a.set_ylabel("cents sharp of a whole multiple")
    t = np.arange(2 * p) / p
    b.plot(t, v, color=labs.RED, lw=1.2, label="the string under the bow")
    b.axhline(bow.speed, color=labs.BLUE, lw=0.8, ls="--", label="the bow")
    b.set_title(f"Stick and slip, bow at {BETA:g} of the length")
    b.set_xlabel("time (periods)")
    b.set_ylabel("speed (m/s)")
    b.legend()
    lab.fig = fig
    lab.note = ("A loop of numbers with an average in it is a string. A real string is stiff, so its partials are sharp; and "
                "under a bow it does one thing, sticking for most of each period and flying back for the fraction of it that "
                "the bow is from the bridge, but only while the bow's force stays between two limits.")
    return lab
