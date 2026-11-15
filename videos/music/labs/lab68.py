"""Lab 68: the round trip.  A tune is played, put in a room, mastered and coded, then transcribed back to a score and
compared with what was written, key by key."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import codec as K
from explainer.music.monochord import melody as ML
from explainer.music.monochord import roundtrip as RT
from explainer.music.monochord import space as SPC
from explainer.music.monochord.mir import transcribe as TR
from explainer.music.monochord.instruments.plucked import plucked

TITLE = "The round trip"
GOAL = ("Send a tune down a chain (Part 1's plucked string, a room, a limiter, a perceptual coder) and back up it (onsets, pitch, "
        "a score with a drifting tempo), and count what comes back wrong at each stage.")
TASKS = [
    "Change KBPS, the coder's bit rate. Where does the line start to come back wrong? Where can you no longer sing it?",
    "Change TUNE (an index into Part 14's melodies). Are repeated notes or leaps harder for the machine?",
    "Change REVERB, the room's level against the direct sound. Which stage of the way back suffers first?",
]
KBPS = 32
TUNE = 4            # Ode to Joy
REVERB = 0.7
CUT = {16: 5500.0}  # Part 58's table has no entry for 16 kbit/s (see Part 68)


def play(keys, beats, beat=0.45):
    """Each note on Part 1's plucked string, retuned to the note, damped 0.15 s after the next would begin."""
    t, y, cache = 0.0, np.zeros(int((sum(beats) * beat + 2.0) * SR)), {}
    for m, b in zip(keys, beats):
        if m not in cache:
            cache[m] = np.asarray(plucked(f1=440 * 2 ** ((m - 69) / 12), seconds=1.2), float)
        z = cache[m][: int(b * beat * SR) + int(0.15 * SR)].copy()
        r = int(0.1 * SR)
        z[-r:] *= np.linspace(1, 0, r) ** 2
        i = int(t * SR)
        y[i:i + len(z)] += z[: len(y) - i]
        t += b * beat
    return y / (np.max(np.abs(y)) + 1e-12) * 0.8


def chain(y, seed=0):
    from scipy.signal import fftconvolve
    ir = SPC.noise_tail(1.4, 1.6, seed=seed, start=0.012)
    wet = fftconvolve(y, ir)[: len(y)]
    room = y + wet * (REVERB * np.sqrt(np.mean(y ** 2)) / (np.sqrt(np.mean(wet ** 2)) + 1e-12))
    room = room / np.max(np.abs(room)) * 0.8
    master = np.tanh(2.2 * room) * 0.9
    coded = K.encode(master, KBPS, cutoff=CUT.get(KBPS))["y"][: len(master)]
    return {"played": y, "room": room, "master": master, "coded": coded}


def run(seed=0):
    lab = labs.Lab()
    m = ML.corpus()[TUNE]
    keys, beats = [72 + p for p in m.pitches], [float(b) for b in m.beats]
    st = chain(play(keys, beats), seed)
    errs = {}
    for k, y in st.items():
        est = RT.monophonic_notes(y, method="onset", compress=10.0, delta=0.2, lag=3)
        b = RT.back_to_score(est)
        e = RT.score_errors(b["keys"], b["values"], keys, beats)
        errs[k] = e["pitch"]
        lab.row(f"{k}: notes found; wrong keys (edit distance); wrong keys and values; tempo", f"{len(est)}; {e['pitch']}; {e['score']}; {b['bpm']:.0f} bpm")
    lab.row("the tune", f"{m.name}, {len(keys)} notes")
    assert errs["played"] <= 2
    lab.row("what the room adds (reverberant energy against the direct sound)", f"{RT.late_to_early_db(st['room'] / 0.8 * np.max(np.abs(st['room'])), st['played']):.1f} dB")
    lab.row("crest factor before and after the limiter", f"{RT.crest_db(st['room']):.1f} dB, {RT.crest_db(st['master']):.1f} dB")
    lab.audio = concat([Clip(st["played"], SR), Clip(st["coded"] / (np.max(np.abs(st["coded"])) + 1e-12) * 0.8, SR)], gap=0.8)
    lab.row("ear problem: the tune played, then after the whole chain; can you still sing it back?", f"coded at {KBPS} kbit/s")
    fig, (ax1, ax2) = labs.figure(2)
    names = list(st)
    ax1.bar(range(len(names)), [errs[k] for k in names], color=labs.GOLD)
    ax1.set_xticks(range(len(names)), names)
    ax1.set_ylabel("wrong keys")
    L = TR.logfreq(st["coded"][: 8 * SR], SR, fmin_midi=48, fmax_midi=120, per_semitone=1, hop=1920)
    ax2.imshow(20 * np.log10(L["S"] + 1e-9), origin="lower", aspect="auto", vmin=-60 + 20 * np.log10(L["S"].max()), cmap="magma")
    ax2.set_xlabel("frame")
    ax2.set_ylabel("semitones above C3")
    lab.fig = fig
    lab.note = ("A chain changes the sound at every link and the notes hardly at all, until the coder runs out of bits: "
                "which is why a score, which keeps only notes and times, travels so well.")
    return lab
