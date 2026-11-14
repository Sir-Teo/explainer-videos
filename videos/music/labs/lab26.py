"""Lab 26: the Classical style, computed: a quartet movement's tonal plan read by a key tracker, its cadences and phrase
gaps, who leads bar by bar, a fair attribution test of Haydn, Mozart and Beethoven with its permutation null, and eight
phrases on the Tune sorted by ear into half and authentic cadences."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import baroque as B
from explainer.music.monochord import classical as CL
from explainer.music.monochord import palestrina as PS
from explainer.music.monochord.partkit import organ_tone

TITLE = "The Classical style, computed"
GOAL = ("Read a quartet movement's keys window by window and find its second key, count its cadences and phrase lengths "
        "and who leads each bar, run a fair attribution test with a permutation null, and hear the difference between a "
        "half cadence and an authentic one.")
TASKS = [
    "Choose a MOVEMENT (try 'opus59no2/movement4' or 'k458/movement1'). Where does the tracker find its second key, and does it agree with the score?",
    "Change WINDOW, the tracker's window in bars. With 4 bars, what happens to Op. 59 No. 2's finale? With 16, what is lost?",
    "Choose FEATURES, a subset of the eight. Which subset scores best, and is it better than the shuffled names?",
]
MOVEMENT = "opus74no1/movement1"
WINDOW = 8
FEATURES = list(CL.FEATURES)
KN = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]


def key_name(k) -> str:
    return f"{KN[k[0]]} {k[1]}"


def tone(m: float, seconds: float, gain: float) -> np.ndarray:
    return organ_tone(440 * 2 ** ((m - 69) / 12), seconds, partials=6, rolloff=0.7, decay=2.5) * gain


def phrase(kind: str) -> Clip:
    """Four bars of the Tune's opening over I, IV, I, then V (a half cadence) or V-I (an authentic cadence)."""
    mel = [72, 72, 79, 79, 81, 81, 79, None, 77, 77, 76, 76]
    mel += [74, 74, 79, None] if kind == "half" else [74, 74, 72, None]
    bass = [48, 53, 48, 43] if kind == "half" else [48, 53, 43, 48]
    beat = 0.36
    y = np.zeros(int(len(mel) * beat * SR + 1.0 * SR))
    for i, p in enumerate(mel):
        if p is not None:
            seg = tone(p, beat * (2 if i + 1 < len(mel) and mel[i + 1] is None else 1), 0.3)
            j = int(i * beat * SR)
            y[j:j + len(seg)] += seg[: len(y) - j]
    for b, p in enumerate(bass):
        for x in (p, p + 16, p + 19):        # the bass, its third and its fifth, above
            seg = tone(x, 4 * beat, 0.12)
            j = int(4 * b * beat * SR)
            y[j:j + len(seg)] += seg[: len(y) - j]
    return Clip(y, SR).fade(0.01, 0.2).at_level(-20.0)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    ms = [CL.Movement(r) for r in B.load_quartets() if "movement" in r["name"]]
    m = [x for x in ms if x.name == MOVEMENT][0]

    # 1. the tonal plan and the second key
    plan = CL.tonal_plan(m, window_bars=WINDOW, hop_bars=2)
    lab.row(f"{m.name} ({m.composer}, {m.bars} bars): keys every {WINDOW} bars, hop 2",
            ", ".join(f"{t['bar']:.0f} {key_name(t['key'])}" for t in plan[:: max(1, len(plan) // 14)]))
    sk = CL.second_key(plan)
    lab.row("home (first window) and the first new key that holds", f"{key_name(plan[0]['key'])}; " +
            ("none" if sk is None else f"{key_name(((plan[0]['key'][0] + sk[0]) % 12, sk[1]))} from bar {sk[2]:.0f}"))

    # 2. cadences, phrase gaps, who leads
    cad = CL.cadences(m)
    gaps = CL.phrase_gaps(m)
    lab.row("authentic cadences (bars) and the gaps between them", f"{cad[:12]}{' ...' if len(cad) > 12 else ''}; gaps {gaps[:12]}")
    lead = CL.lead_voices(m)
    shares = np.bincount(lead, minlength=4) / max(len(lead), 1)
    lab.row("who leads (most onsets): 1st violin, 2nd violin, viola, cello, in 100 bars", ", ".join(f"{100 * s:.0f}" for s in shares))

    # 3. the attribution test and its null
    idx = [CL.FEATURES.index(f) for f in FEATURES]
    X = np.array([CL.features(x) for x in ms])[:, idx]
    y = [x.composer for x in ms]
    acc = PS.loo_centroid(X, y)["accuracy"]
    null = np.array([PS.loo_centroid(X, list(rng.permutation(y)))["accuracy"] for _ in range(300)])
    p = (1 + np.sum(null >= acc - 1e-12)) / (1 + len(null))
    lab.row(f"leave-one-out accuracy with {len(idx)} features / shuffled names (mean) / p",
            f"{acc:.2f} / {null.mean():.2f} / {p:.3f}")
    assert 0.0 <= acc <= 1.0 and 0.0 < p <= 1.0

    # 4. Problem 3: eight phrases, half or authentic
    kinds = list(rng.permutation(["half"] * 4 + ["authentic"] * 4))
    lab.audio = concat([phrase(k) for k in kinds], gap=0.9)
    lab.row("ear problem: the eight phrases in the order played (listen first)", ", ".join(kinds))

    fig, (a, b) = labs.figure(2)
    names = sorted({tuple(t["key"]) for t in plan}, key=lambda k: (k[1], k[0]))
    row = {k: i for i, k in enumerate(names)}
    for t in plan:
        a.barh(row[tuple(t["key"])], 2, left=t["bar"], color=labs.GOLD if tuple(t["key"]) == tuple(plan[0]["key"]) else labs.BLUE)
    a.set_yticks(range(len(names)))
    a.set_yticklabels([key_name(k) for k in names], fontsize=8)
    a.set_xlabel("bar")
    a.set_title(f"{m.name}: the key of each window")
    b.hist(null * len(y), bins=np.arange(0, len(y) + 2) - 0.5, color="#888")
    b.axvline(acc * len(y), color=labs.GOLD, lw=3)
    b.set_xlabel("movements attributed correctly")
    b.set_title("shuffled names (grey) and the real names (gold)")
    lab.fig = fig
    lab.note = ("A key tracker that knows no themes still sees the plan of a sonata movement; cadences fall at four and eight "
                "bars less often than the textbook says; and a fair attribution test can carry real information about the "
                "composer while still losing to a trivial rule.")
    return lab
