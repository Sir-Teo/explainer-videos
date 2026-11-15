"""Lab 44: music for picture and play, computed: a tempo finder for your own hit points, click arithmetic, an
adaptive score's transition delays, and the chip's pulse spectra."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat, mix
from explainer.music.monochord import screen as S
from videos.music.music44 import compute as C

TITLE = "Music for picture and play, computed"
GOAL = ("Spot a scene of your own and find the tempos that hit it; see what rounding a click costs; and measure how long "
        "an adaptive score keeps the wrong music.")
TASKS = [
    "Edit HITS and START. How many tempos between LO and HI hit all of them within TOL frames? Allow half-beats (SUB = 2).",
    "Change QUANTISE ('now', 'beat', 'bar', 'phrase') and BPM. Check that the mean delay is half the boundary's length.",
    "Change DUTY. Which harmonics vanish, and why?",
]
HITS = [3.2, 7.95, 11.4]
START = 0.5
LO, HI, TOL, SUB = 70.0, 160.0, 1.0, 1
QUANTISE = "bar"
BPM = 120.0
DUTY = 0.25


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    r = S.find_tempo(HITS, start=START, lo=LO, hi=HI, tol_frames=TOL, subdivision=SUB)
    sols = r["solutions"]
    lab.row("tempos that hit every point within TOL frames", "; ".join(f"{s['bpm']:.2f} (click {s['click'][0]}-{s['click'][1]}, beats {s['beats']})" for s in sols) or "none")
    if sols:
        b = min(sols, key=lambda s: s["worst_frames"])
        w, e = b["click"]
        cb = S.click_bpm(w, e)
        err = [abs(((h - START) / (60 / cb)) - round((h - START) / (60 / cb))) * (60 / cb) * 24 for h in HITS]
        lab.row(f"the nearest written click {w}-{e} ({cb:.2f} bpm): misses in frames", ", ".join(f"{x:.2f}" for x in err))
    sc = S.Score(BPM)
    d = [s["delay"] for seed_ in range(100) for s in S.adapt(S.simulate(seed_, 120.0), sc, QUANTISE)["switches"][1:]]
    unit = {"now": 0.0, "beat": sc.beat, "bar": sc.bar, "phrase": sc.bar * sc.segment_bars}[QUANTISE]
    assert abs(np.mean(d) - unit / 2) < 0.15
    lab.row(f"adaptive score, switching at '{QUANTISE}': mean / worst delay (s); theory", f"{np.mean(d):.2f} / {np.max(d):.2f}; {unit / 2:.2f}")
    h = S.pulse_harmonics(DUTY, 16)
    lab.row(f"pulse at duty {DUTY}: missing harmonics (of 16)", ", ".join(str(i + 1) for i, a in enumerate(h) if a < 1e-9) or "none")

    # sound: a click track over the hits; ear problem: door slams at random offsets
    beat = 60.0 / (min(sols, key=lambda s: s["worst_frames"])["bpm"] if sols else 120.0)
    parts, t = [], START
    while t < max(HITS) + 0.5:
        parts.append((Clip(C.piano(84, 0.08, 0.6), SR), t, -10.0))
        t += beat
    for hh in HITS:
        parts.append((Clip(C.P40.kick(), SR), hh, 0.0))
    clicks = Clip(mix(parts, duration=max(HITS) + 1.5).y, SR)
    slams, offs = [], []
    for i in range(3):
        off = float(rng.choice([-0.12, 0.0, 0.12]))
        ref = [(Clip(C.piano(84, 0.08, 0.6), SR), t0, -8.0) for t0 in (0.0, 0.5)]        # two clicks set the pulse
        slams.append(Clip(mix(ref + [(Clip(C.P40.kick(), SR), 1.0 + off, 0.0)], duration=2.0).y, SR))
        offs.append({-0.12: "early", 0.0: "in sync", 0.12: "late"}[off])
    lab.audio = concat([clicks] + slams, gap=1.0)
    lab.row("ear problem: two clicks, then a slam meant for the third click; early, in sync or late?", ", ".join(offs))

    fig, (ax1, ax2) = labs.figure(2)
    ax1.plot(r["bpm"], r["worst"], color="C0", lw=0.6)
    ax1.axhline(TOL, color=labs.GOLD, lw=1)
    ax1.set_ylim(0, 12)
    ax1.set_xlabel("tempo (bpm)")
    ax1.set_ylabel("worst miss (frames)")
    ax1.set_title("the tempo finder")
    ax2.bar(range(1, 17), h, color=labs.GOLD)
    ax2.set_xlabel("harmonic")
    ax2.set_title(f"pulse wave, duty {DUTY}")
    lab.fig = fig
    lab.note = ("A hit t seconds after the downbeat falls on beat t x bpm / 60; the finder scans tempos for the ones that make "
                "every such number nearly whole. Waiting for a boundary of length u costs u/2 on average. A pulse of duty d "
                "loses every harmonic k with k d whole.")
    return lab
