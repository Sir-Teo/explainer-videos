"""Lab 57: mastering and loudness, computed: a gated loudness meter and a true-peak meter, a limiter pushed to
several targets, a streaming service's normalization, and dither."""

import math

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import master as M

TITLE = "Mastering and loudness, computed"
GOAL = ("Measure loudness by BS.1770 and true peak by oversampling, master a small groove at several loudness targets "
        "with a look-ahead limiter, see what normalization does to each master, and hear dither.")
TASKS = [
    "Change TARGETS. Where does the limiter start working, and what does each extra decibel of loudness cost in PLR?",
    "Change SERVICE (a streaming service's target). Which masters are turned down, which up, and how loud are their peaks then?",
    "Change BITS. At how many bits does the rounded fade stop sounding gritty without dither?",
]
TARGETS = [-18.0, -14.0, -10.0, -8.0]
SERVICE = -14.0
BITS = 8


def groove(seconds=4.0, seed=0):
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for k in range(int(seconds * 4)):
        i = int(k * 0.25 * SR)
        L = int(0.2 * SR)
        tt = np.arange(L) / SR
        if k % 2 == 0:
            hit = np.sin(2 * np.pi * (60 + 80 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 12)
        else:
            hit = rng.standard_normal(L) * np.exp(-tt * 25) * 0.6
        y[i:i + L] += hit[: n - i]
    y += 0.15 * np.sin(2 * np.pi * 110 * t) * (1 + 0.5 * np.sin(2 * np.pi * 0.5 * t))
    return np.stack([y, y], axis=1) * 0.1


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    g = groove(seed=seed)
    lab.row("the groove as made: integrated loudness, true peak", f"{M.lufs(g):.1f} LUFS, {M.true_peak_db(g):.1f} dBTP")
    masters = {}
    for tg in TARGETS:
        r = M.master(g, tg)
        masters[tg] = r["y"]
        lab.row(f"mastered to {tg:g} LUFS: reached, true peak, PLR, most limiting",
                f"{r['lufs']:.1f} LUFS, {r['true_peak']:.1f} dBTP, {M.plr(r['y']):.1f} dB, {-r['gain_db'].min():.1f} dB")
        assert r["true_peak"] <= -0.95
    for tg, y in masters.items():
        n = M.normalize(y, SERVICE, allow_up=True)
        lab.row(f"the {tg:g} LUFS master on a {SERVICE:g} LUFS service: gain, then peaks at", f"{n['gain_db']:+.1f} dB, {M.true_peak_db(n['y']):.1f} dBTP")

    # sound: the masters matched in loudness, in a random order; ear problem: order them by how hard they were limited
    order = list(rng.permutation(len(TARGETS)))
    clips = []
    for i in order:
        y = masters[TARGETS[i]]
        clips.append(Clip(y * 10 ** ((-20 - M.lufs(y)) / 20), SR))
    tt = np.arange(int(1.5 * SR)) / SR
    fade = 0.5 * np.sin(2 * np.pi * 440 * tt) * np.exp(-tt * 3)
    clips.append(Clip(M.quantize(fade, BITS) * 4, SR))
    clips.append(Clip(M.tpdf_dither(fade, BITS, rng) * 4, SR))
    lab.audio = concat(clips, gap=0.6)
    lab.row("ear problem: the first four, matched in loudness: which was limited hardest? (listen first)",
            ", ".join(f"{TARGETS[i]:g} LUFS" for i in order))
    lab.row(f"then a fading tone at {BITS} bits: rounded, then dithered", f"16 bits would give {6.02 * 16 + 1.76:.0f} dB of range")

    fig, (ax1, ax2) = labs.figure(2)
    L = [M.lufs(masters[t]) for t in TARGETS]
    ax1.plot(L, [M.plr(masters[t]) for t in TARGETS], "o-", color=labs.GOLD)
    ax1.set_xlabel("master's loudness (LUFS)")
    ax1.set_ylabel("PLR (dB)")
    f = np.geomspace(20, 20000, 400)
    ax2.semilogx(f, M.k_response(f), color="C0", label="K-weighting")
    ax2.semilogx(f, M.riaa_db(f), color="C3", label="RIAA playback")
    ax2.set_xlabel("Hz")
    ax2.set_ylabel("dB")
    ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("A loudness meter weights the spectrum like the ear and ignores the silences; a true-peak meter looks between "
                "the samples; a limiter buys loudness with the peaks; a streaming service gives the loudness back and keeps "
                "the damage; dither turns rounding's distortion into hiss.")
    return lab
