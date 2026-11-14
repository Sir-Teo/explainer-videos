"""Lab 38: blues and swing, computed: the swing model at any tempo, a walking bass and guide tones for any changes,
tritone substitutes, and the syncopations of Joplin's Maple Leaf Rag."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat, mix
from explainer.music.monochord import blues as BL
from videos.music.music38 import compute as C

TITLE = "Blues and swing, computed"
GOAL = ("Swing a line at any tempo; walk a bass and find guide tones through any changes; hear and name tritone "
        "substitutions; and count a rag's syncopations.")
TASKS = [
    "Change TEMPOS. Where does the model's short note stop shrinking? Is that what you hear?",
    "Change KEY and VARIANT (basic, quick, jazz). Do the bass's approaches stay a semitone? How far do the guide tones move?",
    "Write your own CHANGES as bars of chord symbols and find their guide tones.",
]
TEMPOS = [100, 140, 200, 260]
KEY = "F"
VARIANT = "jazz"
CHANGES = [["Cmaj7"], ["A7"], ["Dm7"], ["G7"], ["Em7"], ["A7"], ["Dm7"], ["G7"]]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    lab.row("tempo: long-short ratio, short note (ms)", ", ".join(f"{b}: {BL.swing_ratio(b):.2f}, {BL.short_note_ms(b):.0f}" for b in TEMPOS))
    ch = BL.twelve_bar(KEY, VARIANT)
    wb = BL.walking_bass(ch)
    seq = BL.beats_of(ch)
    firsts = [i for i in range(len(seq)) if i == 0 or seq[i] != seq[i - 1]]
    assert all(wb[i] % 12 == BL.chord(seq[i])["root"] for i in firsts), "every chord starts on its root"
    lab.row(f"walking bass, {VARIANT} blues in {KEY} (first two bars)", str(wb[:8]))
    lab.row("approaches into each chord (semitones)", str([abs(wb[i - 1] - wb[i]) for i in firsts]))
    syms = [s for b in ch for s in b]
    g = BL.guide_tones(syms)
    lab.row("guide tones through it: total motion, biggest step", f"{g['total']} semitones, {g['max_step']}")
    g2 = BL.guide_tones([s for b in CHANGES for s in b])
    lab.row("your CHANGES' guide tones (upper / lower)", f"{g2['upper']} / {g2['lower']}")
    lab.row("tritone substitutes of C7, G7, D7", ", ".join(f"{s} -> {BL.tritone_sub(s)}" for s in ("C7", "G7", "D7")))
    r = C.load("rag")
    lab.row("Maple Leaf Rag, bars 1-16: attacks between the eighths (right / left)",
            f"{r['sync_right']['between']} of {r['sync_right']['onsets']} / {r['sync_left']['between']} of {r['sync_left']['onsets']}")

    # ear problem: ii-V-I's in random keys, some with the tritone substitute
    beat = 60.0 / 90
    kinds, clips = [], []
    for i in range(5):
        k = int(rng.integers(0, 12))
        sub = bool(rng.random() < 0.5)
        prog = [BL.transpose("Dm7", k), BL.transpose("Db7" if sub else "G7", k), BL.transpose("Cmaj7", k)]
        gt = BL.guide_tones(prog)
        parts = []
        for j, s in enumerate(prog):
            for m in (gt["upper"][j], gt["lower"][j]):
                parts.append((Clip(C.piano(m, 2 * beat, 0.7), SR), j * 2 * beat, -3.0))
            root = BL.chord(s)["root"]
            parts.append((Clip(C.bass(root + (36 if root < 6 else 24), 2 * beat), SR), j * 2 * beat, 0.0))
        clips.append(Clip(mix(parts, duration=6 * beat + 1.0).y, SR).at_level(-20.0))
        kinds.append("substitute" if sub else "plain")
    lab.audio = concat(clips, gap=0.8)
    lab.row("ear problem: plain or substitute, in order (listen first)", ", ".join(kinds))

    fig, (ax1, ax2) = labs.figure(2)
    bs = np.arange(80, 321, 5)
    ax1.plot(bs, [BL.swing_ratio(b) for b in bs], color=labs.GOLD, label="long : short")
    ax1b = ax1.twinx()
    ax1b.plot(bs, [BL.short_note_ms(b) for b in bs], color="C0", label="short note (ms)")
    ax1.set_xlabel("tempo (beats a minute)")
    ax1.set_ylabel("ratio")
    ax1b.set_ylabel("short note (ms)")
    ax1.set_title("the swing model")
    ax2.step(range(len(wb)), wb, where="post", color="C0")
    ax2.set_xlabel("beat")
    ax2.set_ylabel("key number")
    ax2.set_title(f"walking bass, {VARIANT} blues in {KEY}")
    lab.fig = fig
    lab.note = ("The model's short note settles near a tenth of a second at fast tempos; the walking bass meets every chord "
                "on its root after a semitone; guide tones through ii-V-I move two semitones in all; and a dominant's "
                "tritone substitute shares its third and seventh.")
    return lab
