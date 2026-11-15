"""Lab 56: recording and mixing, computed: where a stereo pair puts a source, two microphones' comb, the pan laws in
stereo and in mono, and a masking map of a small mix."""

import math

import numpy as np
from scipy.signal import fftconvolve

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import space as SP
from explainer.music.monochord import studio as S

TITLE = "Recording and mixing, computed"
GOAL = ("Compute where a stereo pair puts a source and its recording angle, the comb two microphones make, the pan laws "
        "in stereo and in mono, and a masking map of a small mix before and after panning.")
TASKS = [
    "Change PAIR, or add your own pair to S.PAIRS. Where does a source at 30 degrees land, and what is the recording angle?",
    "Change NEAR and FAR (the two microphones' distances). How do the delay, the first notch and the comb's depth move?",
    "Change PAN_B. How far apart must the two tones be panned before neither masks the other?",
]
PAIR = "ORTF"
NEAR, FAR = 0.5, 2.0
PAN_B = 0.8


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    c = S.pair_cues(PAIR, 30.0)
    lab.row(f"{PAIR}: a source 30 degrees left: level, time, image", f"{float(c['dL']):.1f} dB, {float(c['dt']):.2f} ms, {float(S.image_position(c['dL'], c['dt'])):.2f} of the way to the loudspeaker")
    lab.row(f"{PAIR}: recording angle", f"{S.recording_angle(PAIR):.0f} degrees")
    tau = (FAR - NEAR) / S.C
    g = NEAR / FAR
    hi, lo = S.comb_extremes(g)
    lab.row(f"microphones at {NEAR:g} m and {FAR:g} m: delay, first notch, comb", f"{1000 * tau:.2f} ms, {1 / (2 * tau):.0f} Hz, +{hi:.1f} / {lo:.1f} dB")
    for law in (-3.0, -4.5, -6.0):
        gL, gR = S.pan_gains(np.array([0.0]), law)
        lab.row(f"pan law {law:g} dB: centre in stereo / in mono (re a hard pan)", f"{10 * math.log10(gL[0] ** 2 + gR[0] ** 2):+.2f} / {20 * math.log10((gL[0] + gR[0])):+.2f} dB")
    t = np.arange(2 * SR) / SR
    a = 0.3 * np.sin(2 * np.pi * 500 * t)
    b = 0.05 * np.sin(2 * np.pi * 530 * t + 1)
    centre = S.masking_map({"a": S.place(a, 0.0), "b": S.place(b, 0.0)})["overall"]
    apart = S.masking_map({"a": S.place(a, -PAN_B), "b": S.place(b, PAN_B)})["overall"]
    lab.row("a quiet tone beside a loud one: masked, both centred / panned apart", f"{100 * centre['b']:.0f} % / {100 * apart['b']:.0f} %")
    assert abs(10 * math.log10(float(sum(x[0] ** 2 for x in S.pan_gains(np.array([0.3]), -3.0))))) < 1e-9

    # sound: the two microphones summed; ear problem: a voice-like tone at random depths (level, treble, reverberation)
    n = int(1.6 * SR)
    tt = np.arange(n) / SR
    tone = sum(np.sin(2 * np.pi * k * 220 * tt) / k for k in range(1, 15)) * np.exp(-tt * 1.5)
    clips = [Clip(0.2 * (tone + g * S.frac_delay(tone, tau * SR)) / 2.5, SR)]
    tail = SP.noise_tail(1.4, 1.8, seed=3)
    answers = []
    for i in range(3):
        k = int(rng.integers(0, 3))
        gain, send = [(1.0, 0.02), (0.5, 0.2), (0.25, 0.6)][k]
        dry = gain * tone
        wet = send * fftconvolve(tone, tail)[: n] * 0.2
        y = dry + wet
        clips.append(Clip(0.15 * y / np.sqrt(np.mean(y ** 2)) * 0.3, SR))
        answers.append(["near", "middle", "far"][k])
    lab.audio = concat(clips, gap=0.6)
    lab.row("ear problem: how far is each of the last three? (listen first)", ", ".join(answers))

    fig, (ax1, ax2) = labs.figure(2)
    th = np.linspace(0, 90, 181)
    for k in S.PAIRS:
        cc = S.pair_cues(k, th)
        ax1.plot(th, S.image_position(cc["dL"], cc["dt"]), label=k)
    ax1.set_xlabel("source angle (degrees)")
    ax1.set_ylabel("image (1 = loudspeaker)")
    ax1.legend(fontsize=7)
    f = np.geomspace(20, 20000, 800)
    ax2.semilogx(f, S.comb_db(f, tau, g), color=labs.GOLD)
    ax2.set_xlabel("Hz")
    ax2.set_ylabel("dB")
    lab.fig = fig
    lab.note = ("A pair turns direction into level and time differences, which listeners trade against each other; two "
                "microphones on one source comb, mildly if the far one is three times as far; no pan law is right in both "
                "stereo and mono; and panning two sounds apart stops one masking the other.")
    return lab
