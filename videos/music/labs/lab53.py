"""Lab 53: MIDI and the engine, computed: bytes on the wire, a file written and read, an engine in blocks, a tempo canon."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import daw as W

TITLE = "MIDI and the engine, computed"
GOAL = ("Send a chord down a simulated MIDI cable, write and read a MIDI file, render a pattern in blocks of any size and "
        "check that nothing changes, and build a tempo canon.")
TASKS = [
    "Change CHORD (how many notes) and RUNNING. How long does the chord take on the wire, and how many bytes does it cost?",
    "Change PATTERN and BLOCK. Does any block size change the sound? Now set QUANTIZE = True: what moves, and by how much?",
    "Change RATIOS. When do the canon's voices meet, and which voice starts first?",
]
CHORD, RUNNING = 12, True
PATTERN = "c4 e4 [g4 g4] <a4 c5>"
BLOCK, QUANTIZE = 256, False
RATIOS = (2.0, 3.0, 4.0)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    keys = list(range(48, 48 + CHORD))
    stream = W.encode([W.note_on(0, k, 100) for k in keys], running=RUNNING)
    lab.row(f"a {CHORD}-note chord, running status {'on' if RUNNING else 'off'}", f"{len(stream)} bytes, {1000 * W.wire_times(stream)[-1]:.2f} ms on the wire")
    tr = [(0, W.note_on(0, 60, 90)), (480, W.note_off(0, 60)), (480, W.note_on(0, 64, 90)), (960, W.note_off(0, 64))]
    data = W.write_smf([tr])
    back = W.read_smf(data)
    lab.row("a two-note MIDI file", f"{len(data)} bytes; read back {len(back['events'])} events; first bytes {data[:8].hex(' ')}")
    ev = [(int(a * SR), W.note_number(s), 0.8, int(0.9 * d * SR), "main") for a, d, s in W.pattern_events(PATTERN, 2, 2.0)]
    n = int(4.5 * SR)
    ref = W.Engine(ev).render(n)
    y = W.Engine(ev, quantize=QUANTIZE).render(n, BLOCK)
    same = bool(np.array_equal(y, ref))
    lab.row(f"pattern in blocks of {BLOCK}{' (snapped)' if QUANTIZE else ''}: identical to one block?", "yes" if same else f"no: largest difference {np.max(np.abs(y - ref)):.3g}")
    notes = [(60, 0.0, 1.0), (62, 1.0, 1.0), (64, 2.0, 1.0), (65, 3.0, 1.0), (67, 4.0, 2.0)]
    canon, T = W.tempo_canon(notes, list(RATIOS), len(notes) - 1)
    starts = sorted({round(a, 3) for v, k, a, d in canon if k == 60})
    lab.row("tempo canon: voices start at (s)", ", ".join(f"{s:.2f}" for s in starts) + f"; they meet at {T:.2f} s")
    assert (not QUANTIZE and same) or QUANTIZE

    # sound: the pattern and the canon; ear problem: snapped or exact, at random
    cev = [(int(a * SR), k + 12 * (v - 1), 0.7, int(0.85 * d * SR), "main") for v, k, a, d in canon]
    can = W.Engine(cev).render(int((T + 2.0) * SR), 512)
    clips = [Clip(0.5 * ref / np.max(np.abs(ref)), SR), Clip(0.5 * can / np.max(np.abs(can)), SR)]
    answers = []
    hats = [(int((i * 0.125 + 0.013) * SR), 84, 0.6, int(0.05 * SR), "main") for i in range(24)]
    for i in range(3):
        q = bool(rng.random() < 0.5)
        h = W.Engine(hats, quantize=q).render(int(3.4 * SR), 1024)
        clips.append(Clip(0.5 * h / np.max(np.abs(h)), SR))
        answers.append("snapped" if q else "exact")
    lab.audio = concat(clips, gap=0.6)
    lab.row("ear problem: the last three are snapped to blocks or exact (listen first)", ", ".join(answers))

    fig, (ax1, ax2) = labs.figure(2)
    nn = list(range(1, 17))
    for run_, col, name in ((False, "C3", "plain"), (True, labs.GOLD, "running status")):
        ax1.plot(nn, [1000 * W.wire_times(W.encode([W.note_on(0, 48 + j, 100) for j in range(k)], running=run_))[-1] for k in nn], "o-", color=col, label=name)
    ax1.set_xlabel("notes in the chord")
    ax1.set_ylabel("ms on the wire")
    ax1.legend(fontsize=7)
    for v, k, a, d in canon:
        ax2.plot([a, a + d], [v + 0.05 * (k - 60)] * 2, color=f"C{v}", lw=3)
    ax2.axvline(T, color="k", lw=1)
    ax2.set_xlabel("s")
    ax2.set_ylabel("voice")
    lab.fig = fig
    lab.note = ("MIDI 1.0 sends a byte every 320 microseconds; running status saves the repeated status byte. A MIDI file "
                "counts in ticks. An engine that keeps its state between blocks and places notes to the sample gives the same "
                "music in any block size. A tempo canon starts each voice so that all meet on one note.")
    return lab
