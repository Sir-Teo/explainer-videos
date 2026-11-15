"""Lab 54: microphones and loudspeakers, computed: patterns, proximity, a woofer in boxes, and a noise canceller."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import transducer as T

TITLE = "Microphones and loudspeakers, computed"
GOAL = ("Compute a pattern's directivity and a gradient microphone's proximity effect, put a woofer in sealed and vented "
        "boxes and check the simulator against Small's and Thiele's formulas, and cancel a hum adaptively.")
TASKS = [
    "Change A (the pattern). Where is the null, how directional is it, and how much bass does it gain at 5 cm?",
    "Change FS, QES, VAS and VB. Does the simulated -3 dB point still match Small's formula? Then try a vented box.",
    "Change MU and TAPS in the canceller. What makes it converge faster, and what makes it unstable?",
]
A = 0.5
FS, QES, VAS, VB = 40.0, 0.40, 0.050, 0.030
MU, TAPS = 0.01, 64


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    dv = T.directivity(A)
    lab.row(f"pattern A = {A:g}: directivity index, distance factor, null", f"{dv['DI']:.2f} dB, {dv['distance']:.2f}, {dv['null_deg'] if dv['null_deg'] else 'none'}")
    lab.row("bass gain at 100 Hz at 1 m, 15 cm, 5 cm (dB)", ", ".join(f"{20 * np.log10(abs(T.proximity(np.array([100.0]), r, A)[0])):.1f}" for r in (1.0, 0.15, 0.05)))
    d = T.Driver(fs=FS, Qes=QES, Vas=VAS)
    f = np.geomspace(10, 4000, 4000)
    r = T.response(d, f, {"kind": "sealed", "Vb": VB})
    al = T.sealed_alignment(d, VB)
    lab.row(f"sealed {1000 * VB:.0f} L: -3 dB simulated / Small's formula", f"{T.f_minus(f, r['spl']):.2f} / {al['f3']:.2f} Hz (Qtc {al['Qtc']:.2f})")
    rv = T.response(d, f, {"kind": "vented", "Vb": VB, "fb": FS})
    lab.row(f"vented {1000 * VB:.0f} L tuned to {FS:g} Hz: -3 dB simulated", f"{T.f_minus(f, rv['spl']):.2f} Hz")
    t = np.arange(4 * SR) / SR
    x = np.sin(2 * np.pi * 100 * t) + 0.5 * np.sin(2 * np.pi * 200 * t + 1) + 0.05 * rng.standard_normal(len(t))
    prim = np.zeros(60)
    prim[40] = 1.0
    dn = np.convolve(x, prim)[: len(x)]
    sec = np.zeros(24)
    sec[6] = 0.7
    sec[7] = 0.2
    out = T.fxlms(dn, x, sec, taps=TAPS, mu=MU)
    e = out["e"]
    att = 10 * np.log10(np.mean(e[-SR:] ** 2) / np.mean(dn[-SR:] ** 2))
    lab.row("canceller: attenuation in the last second", f"{att:.1f} dB")
    assert abs(T.f_minus(f, r["spl"]) - al["f3"]) < 0.01 * al["f3"]

    # sound: the hum before and after cancelling; ear problem: a voice-like tone at random distances from a figure-8
    clips = [Clip(0.3 * dn[: 2 * SR] / np.max(np.abs(dn)), SR), Clip(0.3 * e[-2 * SR:] / np.max(np.abs(dn)), SR)]
    tone = sum(np.sin(2 * np.pi * k * 110 * t[: int(1.5 * SR)]) / k for k in range(1, 12))
    answers = []
    for i in range(3):
        rr = [1.0, 0.15, 0.05][int(rng.integers(0, 3))]
        y = T.apply_response(tone, lambda ff, rr=rr: T.proximity(ff, rr, 0.0))
        clips.append(Clip(0.3 * y / np.sqrt(np.mean(y ** 2)) * 0.1, SR))
        answers.append({1.0: "1 m", 0.15: "15 cm", 0.05: "5 cm"}[rr])
    lab.audio = concat(clips, gap=0.6)
    lab.row("ear problem: how far is each of the last three from the figure-8? (listen first)", ", ".join(answers))

    fig, (ax1, ax2) = labs.figure(2)
    ax1.semilogx(f, r["spl"] - r["spl"][-1], color=labs.GOLD, label="sealed")
    ax1.semilogx(f, rv["spl"] - rv["spl"][-1], color="C3", label="vented")
    ax1.set_xlim(10, 1000)
    ax1.set_ylim(-30, 5)
    ax1.set_xlabel("Hz")
    ax1.set_ylabel("dB")
    ax1.legend(fontsize=7)
    ax2.plot(np.arange(len(e)) / SR, e, lw=0.5, color="C0")
    ax2.set_xlabel("s")
    ax2.set_ylabel("error at the ear")
    lab.fig = fig
    lab.note = ("A pattern is a mix of pressure and its gradient; the gradient part gains bass near the source. A woofer in "
                "a box is a high-pass filter whose corner the box sets, as Small's closed form predicts. An adaptive filter "
                "can learn the anti-noise for a periodic hum.")
    return lab
