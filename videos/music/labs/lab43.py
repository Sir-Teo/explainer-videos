"""Lab 43: performing, computed: rules of expression on the Tune, the kinematic ritardando, a duo's phase correction
and its stability, and the timing fingerprint."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat, mix
from explainer.music.monochord import perform as P
from videos.music.music43 import compute as C

TITLE = "Performing, computed"
GOAL = ("Perform the Tune with rules at strengths you choose; set two players' corrections and watch them hold, drift or "
        "shake; and fingerprint model pianists by their timing.")
TASKS = [
    "Edit WEIGHTS and K. Which rule, turned up alone, most changes the total length? Which can you hear most clearly?",
    "Set ALPHAS (each player's correction) and TEMPOS. Find the largest total correction that still holds together.",
    "Change STRETCH and NOISE_MS for the fake release. How much editing noise hides a copy from the correlation test?",
]
WEIGHTS = {"phrase arch": 1.0, "duration contrast": 1.0, "high loud": 1.0, "punctuation": 1.0, "final ritardando": 1.0}
K = 1.0
ALPHAS = [0.3, 0.3]
TEMPOS = [0.5, 0.51]          # each player's own period, seconds
STRETCH = 1.03
NOISE_MS = 2.0


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    sc, ph = P.tune_score()
    pf = P.perform(sc, ph, weights=WEIGHTS, k=K)
    dev, vel = P.deviations(pf, sc)
    lab.row("the Tune: seconds as written / performed", f"{P.deadpan(sc)[-1]['t'] + P.deadpan(sc)[-1]['dur']:.1f} / {pf[-1]['t'] + pf[-1]['dur']:.1f}")
    lab.row("longest note against written; velocity range", f"{max(dev):.2f}; {min(vel):.2f} to {max(vel):.2f}")
    a = sum(ALPHAS)
    r = P.phase_correction(ALPHAS, n=64, period=TEMPOS, rng=np.random.default_rng(seed))
    asy = 1000 * r["asynchrony"][:, 1]
    lab.row("duo: total correction; exact spread if tempos were equal (ms)", f"{a:.2f}; " + ("unstable" if not 0 < a < 2 else f"{np.sqrt(P.asynchrony_variance(a)) * 1000:.1f}"))
    lab.row("duo: asynchrony after 64 beats (ms)", f"{asy[-1]:.0f}")
    sc2, ph2 = sc, ph
    pianists = {i: P.play(P.pianist(i), sc2, ph2) for i in range(8)}
    curves = {f"pianist {chr(65 + i)}": P.tempo_curve(p) for i, p in pianists.items()}
    src = pianists[int(rng.integers(8))]
    fake = [{**p, "t": float(p["t"] * STRETCH + rng.normal(0, NOISE_MS / 1000))} for p in src]
    fake[0]["t"] = 0.0
    rank = P.identify(curves, P.tempo_curve(fake))
    assert rank[0][1] >= rank[-1][1]
    lab.row("the fake release: best match, then the runner-up (correlations)", f"{rank[0][0]} {rank[0][1]:.4f}; {rank[1][0]} {rank[1][1]:.3f}")

    # sound: the performed Tune's first two phrases; ear problem: duos with random corrections
    sub, sph = C.sub([0, 1])
    parts = [C.render(P.perform(sub, sph, weights=WEIGHTS, k=K), sub, sph)]
    kinds = []
    for i, tot in enumerate(rng.permutation([0.0, 0.5, 2.2])):
        tot = float(tot)
        rr = P.phase_correction([tot / 2, tot / 2], n=20, period=[0.5, 0.512], rng=np.random.default_rng(seed + i))
        parts.append(C.duo_clip(rr["onsets"]))
        kinds.append({0.0: "drifts (0)", 0.5: "holds (0.5)", 2.2: "shakes (2.2)"}[tot])
    lab.audio = concat(parts, gap=1.0)
    lab.row("ear problem: each duo, in order (listen first)", ", ".join(kinds))

    fig, (ax1, ax2) = labs.figure(2)
    ax1.bar(range(len(dev)), np.array(dev) - 1, color=labs.GOLD)
    ax1.set_title("each note's length against written (0 = as written)")
    ax1.set_xlabel("note")
    ax2.plot(asy, "o-", color="C0", ms=3)
    ax2.axhline(0, color="#8A93A0", lw=0.8)
    ax2.set_title(f"duo asynchrony, total correction {a:.2f}")
    ax2.set_xlabel("beat")
    ax2.set_ylabel("ms")
    lab.fig = fig
    lab.note = ("Rules stretch and weight notes; a duo's asynchrony shrinks by 1 - (alpha1 + alpha2) a beat, so it holds "
                "only for totals between 0 and 2; and a time-stretched copy keeps its source's tempo curve exactly.")
    return lab
