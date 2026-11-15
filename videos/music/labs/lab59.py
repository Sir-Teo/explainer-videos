"""Lab 59: live sound, computed: the gain before feedback by Nyquist's criterion and by ringing out, a point source
against a line array, a cardioid subwoofer pair, a delay tower, a wireless frequency plan, the speech transmission
index and a night's noise dose."""

import numpy as np
from scipy.signal import butter, sosfilt

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import live as LV

TITLE = "Live sound, computed"
GOAL = ("Find the gain at which a microphone and loudspeaker in a room will howl and the note they will howl at, buy "
        "gain back with notches, compare how a point source and a line array fall off with distance, cancel a "
        "subwoofer's sound behind the stage, time a delay tower, plan radio frequencies free of intermodulation, and "
        "predict how much of an announcement survives a reverberant, noisy hall.")
TASKS = [
    "Change ECHOES (the room between loudspeaker and microphone). Does the howl frequency move? Does ringing out still help?",
    "Change N_BOXES and SPACING. At what distance does the line array start falling 6 dB per doubling, like a point?",
    "Change T and SNR. Which matters more for speech in a station: halving the reverberation, or 10 dB less noise?",
]
ECHOES = [(0.006, 0.45), (0.0137, 0.3), (0.021, 0.25), (0.034, 0.2)]     # (delay s, gain) of the room's paths
N_BOXES, SPACING = 16, 0.35
T, SNR = 2.5, 10.0


def room_ir(seed=0):
    rng = np.random.default_rng(seed)
    h = np.zeros(int(0.5 * SR))
    for d, g in ECHOES:
        h[int(d * SR)] += g
    tail = rng.standard_normal(len(h)) * np.exp(-np.arange(len(h)) / (0.12 * SR)) * 0.02
    tail[: int(0.04 * SR)] = 0
    band = butter(2, [150, 5000], btype="band", fs=SR, output="sos")        # the loudspeaker and the microphone
    return sosfilt(band, h + tail)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    ir = room_ir(seed)
    fb = LV.feedback(ir)
    lab.row("gain before feedback (Nyquist), and the note it howls at", f"{fb['max_gain_db']:+.1f} dB, {fb['howl_hz']:.0f} Hz")
    lab.row("the quick estimate from |H| alone (ignores phase)", f"{fb['peak_gain_db']:+.1f} dB, {fb['peak_hz']:.0f} Hz")
    ro = LV.ring_out(ir, 6)
    lab.row("after six notches: gain before feedback", f"{ro[-1]['max_gain_db']:+.1f} dB ({ro[-1]['max_gain_db'] - ro[0]['max_gain_db']:+.1f})")
    assert ro[-1]["max_gain_db"] > ro[0]["max_gain_db"]

    clap = np.zeros(int(2.0 * SR))
    clap[:2880] = rng.standard_normal(2880) * np.hanning(2880) * 0.3
    rings = {}
    for m in (-6.0, -0.5):
        y = LV.closed_loop(clap, ir, fb["max_gain_db"] + m, 2.0)
        rings[m] = y / np.max(np.abs(y))
    late = {m: 10 * np.log10(np.mean(y[SR:] ** 2) / np.mean(y[: SR // 5] ** 2)) for m, y in rings.items()}
    lab.row("a clap: its ring one second on, 6 dB and 0.5 dB under the edge", f"{late[-6.0]:.0f} dB, {late[-0.5]:.0f} dB")
    assert late[-0.5] > late[-6.0]

    dists = np.array([5.0, 10.0, 20.0, 40.0, 80.0, 160.0])
    pos, _ = LV.line_array(N_BOXES, SPACING, top=(0.0, 1.5 + (N_BOXES - 1) * SPACING / 2))
    line = LV.field(pos, 1000.0, dists, [1.5], air=False)[0]
    point = LV.field([(0.0, 1.5)], 1000.0, dists, [1.5], air=False)[0]
    lab.row("per doubling 5 to 160 m at 1 kHz: point source", " ".join(f"{a - b:.1f}" for a, b in zip(point, point[1:])))
    lab.row(f"the same: a line of {N_BOXES} boxes {SPACING} m apart", " ".join(f"{a - b:.1f}" for a, b in zip(line, line[1:])))

    f = np.array([40.0, 63.0, 100.0])
    cs = LV.cardioid_sub(f)
    lab.row("cardioid pair at 40, 63, 100 Hz: in front, behind (dB)", ", ".join(f"{a:.1f}/{b:.0f}" for a, b in zip(cs["front_db"], np.maximum(cs["back_db"], -99))))
    lab.row("a delay tower 30 m from you, the stage 90 m: delay at 20 and 5 C",
            f"{1000 * LV.delay_time(90, 30, 20):.1f} ms, {1000 * LV.delay_time(90, 30, 5):.1f} ms")

    plan = LV.plan_channels(470.0, 500.0, 16, exclude=[(482.0, 488.0)])
    prods = LV.imd3(plan)
    worst = min(min(abs(p - c) for p in prods) for c in plan)
    lab.row("wireless: carriers planned in 470-500 MHz, closest product to any carrier", f"{len(plan)}, {1000 * worst:.0f} kHz")
    assert worst >= 0.1 - 1e-9

    lab.row(f"STI at T = {T} s, SNR = {SNR} dB; halve T; 10 dB less noise",
            f"{LV.sti(T, SNR):.2f}, {LV.sti(T / 2, SNR):.2f}, {LV.sti(T, SNR + 10):.2f}")
    lab.row("dose: 2 h at 104 dBA; with 15 dB earplugs", f"{LV.dose([104], [2]):.0f} %, {LV.dose([89], [2]):.0f} %")

    order = [-6.0, -0.5]
    lab.audio = concat([Clip(0.5 * rings[m], SR) for m in order], gap=0.6)
    lab.row("ear problem: two claps; which was nearer the edge? (listen first)", "the second")

    fig, (ax1, ax2) = labs.figure(2)
    ax1.plot(fb["f"], fb["mag_db"], color="0.6", lw=0.6, label="|H|")
    ax1.axhline(-fb["max_gain_db"], color=labs.GOLD, lw=1, label="the edge")
    ax1.set_xscale("log")
    ax1.set_xlabel("Hz")
    ax1.set_ylabel("dB")
    ax1.legend(fontsize=7)
    ax2.semilogx(dists, point - point[0], "o-", color="0.5", label="point")
    ax2.semilogx(dists, line - line[0], "o-", color=labs.GOLD, label="line")
    ax2.set_xlabel("m")
    ax2.set_ylabel("dB")
    ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("A loop howls where its gain first reaches one in phase; notches buy a few decibels; a line source holds "
                "its level near it and falls like a point far away; and delays and polarity aim sound that is too long to "
                "aim with a box.")
    return lab
