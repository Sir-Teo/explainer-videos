"""Lab 49: filters, delay and reverb, computed: a biquad of your choice, a comb, a simulated room and its decay, and
Schroeder's reverberator."""

import numpy as np
from scipy.signal import lfilter

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import effects as F
from videos.music.music49 import compute as C

TITLE = "Filters, delay and reverb, computed"
GOAL = ("Design a biquad and hear it, make a pitch from a delay, simulate a room and measure its reverberation time "
        "against Sabine's, and build Schroeder's reverberator.")
TASKS = [
    "Change KIND, F0, Q and GAIN. Predict the response's shape from the poles and zeros the lab prints.",
    "Change DIMS and ALPHA. How close does the measured RT60 come to Sabine's and Eyring's, and when does it stray?",
    "Change T60 for Schroeder's reverberator and listen for its flutter. Does a longer decay hide it or expose it?",
]
KIND, F0, Q, GAIN = "peak", 1000.0, 1.5, 9.0
DIMS, ALPHA = (4.0, 3.0, 2.6), 0.2
T60 = 1.5


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    b, a = F.biquad(KIND, F0, SR, Q, GAIN)
    r = F.response(b, a, SR, [100.0, F0, 10000.0])
    lab.row(f"{KIND} at {F0:.0f} Hz, Q {Q}, {GAIN} dB: gain at 100 Hz, F0, 10 kHz", ", ".join(f"{v:.1f} dB" for v in r["db"]))
    lab.row("its poles (radius)", ", ".join(f"{np.hypot(*p):.4f}" for p in r["poles"]))
    D = 218
    lab.row(f"a feedback comb {D} samples long rings at", f"{SR / D:.1f} Hz")
    ir = F.room_ir(DIMS, (0.7, 0.8, 1.5), (DIMS[0] - 0.9, DIMS[1] - 0.7, 1.4), ALPHA, SR, 1.0)
    rt = F.rt60(ir, SR)
    lab.row(f"a {DIMS} m room, alpha {ALPHA}: RT60 measured / Sabine / Eyring", f"{rt:.2f} / {F.sabine(DIMS, ALPHA):.2f} / {F.eyring(DIMS, ALPHA):.2f} s")
    imp = np.zeros(int(2.5 * SR))
    imp[0] = 1
    sch = F.schroeder(imp, SR, T60)
    lab.row(f"Schroeder's reverberator set to {T60} s measures", f"{F.rt60(sch, SR):.2f} s")
    assert rt > 0

    # sound: a groove through your filter; the Tune in the room and through Schroeder; ear problem: random filters
    g = C.groove(1)
    x = C.tune_signal()
    clips = [Clip(lfilter(b, a, g), SR), Clip(C.wet(x, ir, 0.6, 1.0), SR), Clip(C.wet(x, sch, 0.6, 1.0), SR)]
    kinds = ["lowpass", "highpass", "peak"]
    answers = []
    for i in range(3):
        k = kinds[int(rng.integers(3))]
        fc = float(rng.choice([400.0, 1000.0, 3000.0]))
        bb, aa = F.biquad(k, fc, SR, 1.0, 12.0 if k == "peak" else 0.0)
        clips.append(Clip(lfilter(bb, aa, g), SR))
        answers.append(f"{k} at {fc:.0f} Hz")
    lab.audio = concat(clips, gap=0.8)
    lab.row("ear problem: the last three are the groove through a random filter (listen first)", "; ".join(answers))

    fig, (ax1, ax2) = labs.figure(2)
    f = np.geomspace(20, 20000, 300)
    ax1.semilogx(f, F.response(b, a, SR, f)["db"], color=labs.GOLD)
    ax1.set_xlabel("Hz")
    ax1.set_ylabel("dB")
    e = F.edc(ir)
    ax2.plot(np.arange(len(e)) / SR, e, color="C0")
    ax2.set_ylim(-80, 0)
    ax2.set_xlabel("s")
    ax2.set_ylabel("energy still to come, dB")
    lab.fig = fig
    lab.note = ("Every effect here is delay and addition: feedback places poles, a room is a sum of delayed images, and "
                "a reverberator is a few delays fed back.")
    return lab
