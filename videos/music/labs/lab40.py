"""Lab 40: the song studio, computed: drum-machine voices, step patterns with swing, the sidechain, chopping, and
the measures of prosody and flow."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat, mix
from explainer.music.monochord import song as S
from videos.music.music40 import compute as C

TITLE = "The song studio, computed"
GOAL = ("Build drum-machine voices and a beat of your own; hear the sidechain at different depths; and score a line's "
        "prosody and a verse's flow.")
TASKS = [
    "Edit PATTERN (sixteen steps a bar) and SWING. What makes it feel like rock, funk or house?",
    "Change DECAY and the kick's pitch. At what decay does the kick become a bass note?",
    "Write your own LINE (syllable, stressed, sixteenth) and VERSE, and score them.",
]
PATTERN = {"kick": [0, 6, 10], "snare": [4, 12], "hat": list(range(0, 16, 2)), "open": [14]}
SWING = 0.55
BPM = 104
DECAY = 0.45
LINE = [("HAP", True, 0), ("py", False, 2), ("BIRTH", True, 4), ("day", False, 6)]
VERSE = [("I", False, 0, None), ("count", True, 2, None), ("the", False, 3, None), ("time", True, 6, "A"), ("in", False, 8, None),
         ("threes", True, 9, None), ("and", False, 11, None), ("rhyme", True, 12, "A")]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    k = S.kick808(52.0, DECAY)
    lab.row(f"kick at decay {DECAY} s: pitch at the strike / settled (Hz)", f"{S.measured_pitch(k, 0.0, 0.01):.0f} / {S.measured_pitch(k):.1f}")
    lab.row("time for the kick to fall 60 dB (s)", f"{DECAY * np.log(1000):.2f}")
    lab.row("hi-hat oscillators (Hz)", ", ".join(f"{f:g}" for f in S.HAT_HZ))
    bb = S.backbeat_share({"snare": PATTERN["snare"]}) if PATTERN["snare"] else 0.0
    lab.row("your pattern: snare hits on 2 and 4", f"{bb:.0%}")
    pr = S.prosody(LINE)
    assert 0.0 <= pr["agree"] <= 1.0
    lab.row("your LINE: syllables whose stress agrees with the beat", f"{pr['agree']:.0%}")
    fl = S.flow(VERSE, 1)
    lab.row("your VERSE: syllables a beat, on the beat, gaps between accents", f"{fl['per_beat']:.2f}, {fl['on_beat']:.0%}, {fl['gaps']}")

    # the pattern, with swing, two bars, drum-machine voices
    step = 60.0 / BPM / 4
    parts = []
    for bar in range(2):
        for kind, ons in PATTERN.items():
            for s in ons:
                pos = (2 * (s // 2) + (0 if s % 2 == 0 else 2 * SWING)) * step
                snd = {"kick": k, "snare": S.clap808(), "hat": S.hat808(), "open": S.hat808(True)}[kind]
                parts.append((Clip(snd, SR), bar * 16 * step + pos, {"kick": -2.0, "snare": -6.0, "hat": -12.0, "open": -12.0}[kind]))
    beat = Clip(mix(parts, duration=32 * step + 0.8).y, SR).at_level(-20.0)

    # ear problem: a pad under a kick, at random sidechain depths
    depths, clips = [], []
    b = 60.0 / 124
    for i in range(4):
        dep = float(rng.choice([0.0, 6.0, 12.0, 18.0]))
        line = np.concatenate([C.pad([9, 0, 4], 4 * b, bright=4000), C.pad([5, 9, 0], 4 * b, bright=4000)])
        hits = [j * b for j in range(8)]
        y, g = S.sidechain(line, hits, depth_db=dep) if dep else (line, None)
        ps = [(Clip(y, SR), 0.0, -6.0)] + [(Clip(S.kick808(52.0, 0.3), SR), h, -4.0) for h in hits]
        clips.append(Clip(mix(ps, duration=8 * b + 0.6).y, SR).at_level(-20.0))
        depths.append(f"{dep:g} dB")
    lab.audio = concat([beat] + clips, gap=1.0)
    lab.row("ear problem: sidechain depth of each pad, in order (listen first)", ", ".join(depths))

    fig, (ax1, ax2) = labs.figure(2)
    t = np.arange(len(k)) / SR
    ax1.plot(t[: int(0.6 * SR)], k[: int(0.6 * SR)], color=labs.GOLD, lw=0.6)
    ax1.set_xlabel("seconds")
    ax1.set_title(f"the kick: a struck resonator, decay {DECAY} s")
    f, spec = S.hat_spectrum()
    ax2.semilogy(f[f < 12000], spec[f < 12000] + 1e-6, color="C0", lw=0.6)
    ax2.set_xlabel("Hz")
    ax2.set_title("six square waves: the hi-hat's raw spectrum")
    lab.fig = fig
    lab.note = ("The kick is one damped mode whose pitch sags after the strike; the hat is six square waves' odd harmonics, "
                "high-passed; a sidechain dips by its depth and recovers in release times ln(depth); prosody and flow are "
                "positions on a sixteenth-note grid.")
    return lab
