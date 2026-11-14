"""Lab 33: the mathematics of rhythm and scale, computed: Euclidean rhythms and their evenness, moments of symmetry
from any generator, oddity and homometry, tiling canons by exact cover, Plain Bob, and a temperament finder."""

from math import log2

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat, mix
from explainer.music.monochord import mathmusic as MM
from explainer.music.monochord.instruments import drumkit as DK

TITLE = "Rhythm and scale, computed"
GOAL = ("Generate Euclidean rhythms and check their evenness; find the scale sizes a generator makes with two step sizes; "
        "test rhythms for oddity and shared intervals; search for tiling canons; and rank equal temperaments.")
TASKS = [
    "Change K and N. Is E(K, N) a rotation of a rhythm you know? Does it have the oddity property?",
    "Change GENERATOR (as a fraction of the octave). At which sizes does a stack of it have exactly two step sizes?",
    "Choose a RHYTHM and a cycle length CYCLE. Does it tile the cycle, and are any of its tilings free of periodicity?",
]
K, N = 5, 12
GENERATOR = log2(1.5)
RHYTHM, CYCLE = (0, 1, 4, 5), 16


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    p = MM.euclid(K, N)
    s = "".join("x" if x else "." for x in p)
    lab.row(f"E({K},{N})", f"{s}; steps {MM.steps(p)}; oddity {MM.oddity(MM.onsets(p), N) if N % 2 == 0 else 'n/a (odd cycle)'}")
    named = [r["name"] for r in MM.named_euclidean() if r["k"] == K and r["n"] == N]
    lab.row("in Toussaint's catalogue here", ", ".join(named) or "(not in the selection)")
    lab.row(f"moments of symmetry of generator {GENERATOR:.5f}", str(MM.mos_sizes(GENERATOR, 60)))
    lab.row("homometric classes, 4 strokes in 8 / 6 in 12", f"{len(MM.homometric_pairs(4, 8))} / {len(MM.homometric_pairs(6, 12))}")
    T = MM.tilings(RHYTHM, CYCLE, limit=5000)
    aper = [B for B in T if not MM.is_periodic(B, CYCLE)]
    lab.row(f"tilings of Z_{CYCLE} by {RHYTHM}; with aperiodic entries", f"{len(T)}; {len(aper)}; rhythm periodic: {MM.is_periodic(RHYTHM, CYCLE)}")
    chk = MM.vuza_check()
    lab.row("the film's Vuza canon at 72: tiles, A periodic, B periodic", f"{chk['tiles']}, {chk['A_periodic']}, {chk['B_periodic']}")
    assert chk["tiles"] and not chk["A_periodic"] and not chk["B_periodic"]
    bob = MM.plain_bob_minimus()
    lab.row("Plain Bob Minimus: distinct rows, back to rounds", f"{len(set(bob[:-1]))}, {bob[-1] == bob[0]}")
    lab.row("record-setting equal divisions up to 60 (worst of 3/2 and 5/4)", str([e["n"] for e in MM.best_edos(60)]))

    # Problem 3: six rhythms of five strokes in twelve pulses, three Euclidean (rotated) and three not
    pool = []
    from itertools import combinations
    for c in combinations(range(12), 5):
        if c[0] == 0:
            pool.append(c)
    euc = [MM.onsets(MM.euclid(5, 12))]
    kinds, clips = [], []
    for i in range(6):
        if i % 2 == 0:
            r = int(rng.integers(12))
            ons = sorted((x + r) % 12 for x in euc[0])
            kinds.append("Euclidean")
        else:
            while True:
                ons = list(pool[int(rng.integers(len(pool)))])
                if not MM.is_rotation(MM.pattern_of(ons, 12), MM.euclid(5, 12)):
                    break
            kinds.append("not")
        parts = []
        for cyc in range(3):
            for o in ons:
                parts.append((Clip(DK.clave(), SR), (cyc * 12 + o) * 0.16, 0.0))
        clips.append(Clip(mix(parts, duration=36 * 0.16 + 0.5).y, SR).at_level(-20.0))
    order = rng.permutation(6)
    lab.audio = concat([clips[i] for i in order], gap=1.0)
    lab.row("ear problem: Euclidean or not, in the order played (listen first)", ", ".join(kinds[i] for i in order))

    fig, (a, b) = labs.figure(2)
    ks = list(range(1, N + 1))
    a.bar(ks, [max(MM.steps(MM.euclid(k, N))) - min(MM.steps(MM.euclid(k, N))) if k < N else 0 for k in ks], color=labs.GOLD)
    a.set_xlabel("strokes k")
    a.set_ylabel("largest minus smallest gap")
    a.set_title(f"E(k, {N}): never more than one pulse of difference")
    e = MM.best_edos(60)
    b.plot([x["n"] for x in e], [x["worst"] for x in e], "o-", color=labs.BLUE)
    b.set_xlabel("steps to the octave")
    b.set_ylabel("worst error, cents")
    b.set_title("record-setting equal temperaments")
    lab.fig = fig
    lab.note = ("Euclid's algorithm never leaves gaps differing by more than one pulse; stacks of a generator have two step "
                "sizes exactly at the denominators of its continued fraction and their sums; and the canon at 72 tiles "
                "with neither part repeating.")
    return lab
