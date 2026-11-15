"""Precompute everything numerical, and every sound, in Part 53 of *Music, Built* ("MIDI, Sequencers and the DAW").

    python -m videos.music.music53.compute              # everything missing (about a minute)
    python -m videos.music.music53.compute --force hook

Numbers are cached in ``.cache/music53/<name>.json``, sounds in ``.cache/music53/audio/``.  The tools are Monochord's
(``explainer/music/monochord/daw.py``); the voices are the engine's own sawtooth voice, Part 51's ladder and drum
circuits, Part 52's Karplus-Strong strings, Part 7's piano and Part 9's modal bars.

Items:
    hook        an ear question: a twelve-note chord struck four times, all at once and as MIDI 1.0 sends it, one byte
                after another down the cable; which was the cable?
    musicbox    the Tune on a computed music box (clamped-free tines)
    pianola     a passage no pianist could play, on Part 7's piano: forty notes a second
    musicn      the Tune's first phrase from three unit generators, MUSIC-style
    bytes       the Tune's first phrase as MIDI messages: bytes with and without running status, and their times on
                the wire; chord smear against chord size
    zipper      a resonant filter swept by a 7-bit controller and by a smooth one
    smf         the whole Tune as a Standard MIDI File, written and read back
    steps       a sixteen-step bass line with accents and slides
    pattern     two lines in the pattern language, four cycles
    callback    the engine in blocks of 32 to 2048 samples: identical output, cost per block, latency; dropouts
                simulated when a block misses its deadline
    timing      hi-hats placed to the sample, and snapped to 1024-sample blocks
    pdc         parallel compression with a look-ahead limiter: the paths misaligned, then compensated
    tune53      Variation 53: the Tune as a four-channel tracker module, then as a tempo canon at 3 : 4 : 5 : 6
    variation   the Variations ledger, row 53
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import daw as W
from explainer.music.monochord import song as SONG
from explainer.music.monochord import synth as S1
from explainer.music.monochord import synth2 as F
from explainer.music.monochord import tune as T
from explainer.music.monochord.instruments import percussion as PC
from explainer.music.monochord.partkit import saver
from videos.music.music38 import compute as P38

CACHE = Cache("music53")
CLIPS = ClipStore("music53")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="synthesized")
save_pm = saver(CLIPS, LEVEL, kind="physical model")
MAJOR = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
BEAT = 0.5


def C(y) -> Clip:
    return Clip(np.asarray(y, float), SR)


def hz(m: float) -> float:
    return 440.0 * 2 ** ((m - 69) / 12)


def tune_notes(phrases=(0,), base=60, beat=BEAT):
    return [(base + MAJOR[e["degree"]], e["t"], e["dur"]) for e in T.events(beat, list(phrases))]


def norm(y, peak=0.5):
    y = np.asarray(y, float)
    return peak * y / (np.max(np.abs(y)) + 1e-12)


def norm_rms(y, target=0.1):
    return y * target / (np.sqrt(np.mean(np.asarray(y) ** 2)) + 1e-12)


def fade(y, a=0.003, r=0.03):
    y = np.array(y, float)
    ka, kr = max(int(a * SR), 1), max(int(r * SR), 1)
    y[:ka] *= np.linspace(0, 1, ka)
    y[len(y) - kr:] *= np.linspace(1, 0, kr)
    return y


def pluck(m, seconds=1.2, seed=0):
    return F.ks_tuned(hz(m), seconds, seed=seed, rho=0.997)


# ---------------------------------------------------------------------------------------------------------- items
CHORD = [36, 43, 48, 52, 55, 60, 64, 67, 72, 76, 79, 84]


def chord_arrivals(keys, running=True):
    """When each note-on of a chord has arrived, sent as one burst of messages."""
    stream = W.encode([W.note_on(0, k, 100) for k in keys], running=running)
    ends = W.wire_times(stream)
    out, i = [], 0
    for j in range(len(keys)):
        n = 3 if (j == 0 or not running) else 2
        i += n
        out.append(float(ends[i - 1]))
    return out


def compute_hook() -> dict:
    arr = chord_arrivals(CHORD)
    strikes = []
    for serial in (True, False):
        parts = []
        for c in range(4):
            t0 = c * 1.2
            for j, k in enumerate(CHORD):
                parts.append((C(pluck(k, 1.1, seed=j)), t0 + (arr[j] if serial else 0.0), -6.0))
        strikes.append(mix(parts, duration=4 * 1.2 + 0.8).y)
    c = concat([C(norm_rms(strikes[0])), C(norm_rms(strikes[1]))], gap=1.0, names=["first", "second"])
    return {"answer": "first", "arrivals_ms": [1000 * a for a in arr], "keys": CHORD, "spread_ms": 1000 * (arr[-1] - arr[0]),
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save_pm("hook.two", c, detail="a twelve-note chord of Karplus-Strong strings struck four times as MIDI 1.0 sends it, one note-on after another at 31,250 bits a second, then four times all at once")}}


TINE = (1.0, 6.267, 17.55)


def tine(f, seconds=1.6):
    return PC.modal([f * r for r in TINE], [1.0, 0.25, 0.08], [1.0 / 1.2, 1.0 / 0.25, 1.0 / 0.08], seconds, SR, attack=0.0008)


def compute_musicbox() -> dict:
    notes = tune_notes(phrases=(0, 1), base=84, beat=0.32)
    parts = [(C(tine(hz(m))), a, 0.0) for m, a, d in notes]
    y = mix(parts, duration=notes[-1][1] + 2.0).y
    c = concat([C(norm_rms(y))], names=["box"])
    return {"notes": [list(n) for n in notes], "tine": list(TINE),
            "clips": {"one": save_pm("musicbox.one", c, detail="the Tune's first two phrases two octaves above middle C on a computed music box: steel tines clamped at one end, struck by the pins of a turning cylinder")}}


def compute_pianola() -> dict:
    rate = 40.0
    seq = []
    pat = [0, 4, 7, 12, 16, 19, 24, 19, 16, 12, 7, 4]
    t = 0.0
    for rep in range(6):
        for j, iv in enumerate(pat):
            seq.append((48 + iv + 2 * (rep % 3), t))
            t += 1 / rate
    # and a chord of 15 notes spread over five octaves, struck at once
    cl = [36, 40, 43, 48, 52, 55, 60, 64, 67, 72, 76, 79, 84, 88, 91]
    parts = [(C(np.asarray(P38.piano(m, 0.5), float)), a, -4.0) for m, a in seq]
    parts += [(C(np.asarray(P38.piano(m, 1.5), float)), t + 0.2, -9.0) for m in cl]
    y = mix(parts, duration=t + 2.2).y
    c = concat([C(norm_rms(y))], names=["roll"])
    return {"rate": rate, "notes": len(seq) + len(cl), "chord": cl, "seconds": t,
            "clips": {"one": save_pm("pianola.one", c, detail="Part 7's computed piano played by a roll: arpeggios at forty notes a second, then a fifteen-note chord over five octaves")}}


def ugen_note(f, seconds):
    """MUSIC-style: an envelope generator (linear attack, exponential decay) driving an oscillator's amplitude, the
    oscillator reading a stored table (a sine and two harmonics), the output summed into the score."""
    n = int(seconds * SR)
    t = np.arange(n) / SR
    table = np.sin(2 * np.pi * np.arange(512) / 512) + 0.4 * np.sin(4 * np.pi * np.arange(512) / 512) + 0.2 * np.sin(6 * np.pi * np.arange(512) / 512)
    idx = (np.cumsum(np.full(n, f * 512 / SR)) % 512).astype(int)
    env = np.minimum(t / 0.02, 1.0) * np.exp(-t / 0.6)
    return table[idx] * env


def compute_musicn() -> dict:
    notes = tune_notes(beat=0.45)
    parts = [(C(ugen_note(hz(m), d + 0.4)), a, 0.0) for m, a, d in notes]
    y = mix(parts, duration=notes[-1][1] + 1.2).y
    c = concat([C(norm_rms(y))], names=["score"])
    score = [f"i1 {a:.2f} {d:.2f} {hz(m):.1f}" for m, a, d in notes]
    return {"score": score, "clips": {"one": save("musicn.one", c, detail="the Tune's first phrase from a MUSIC-style orchestra: a table-lookup oscillator, its amplitude from an envelope generator, one line of score per note")}}


def compute_bytes() -> dict:
    notes = tune_notes(beat=0.5)
    msgs, times = [], []
    for m, a, d in notes:
        msgs.append(W.note_on(0, m, 100))
        times.append(a)
        msgs.append(W.note_off(0, m))
        times.append(a + d * 0.9)
    order = np.argsort(times, kind="stable")
    msgs = [msgs[i] for i in order]
    plain = W.encode(msgs, running=False)
    run = W.encode(msgs)
    sizes = list(range(1, 17))
    spread = {"plain": [], "running": []}
    for n in sizes:
        keys = list(range(48, 48 + n))
        spread["plain"].append(1000 * chord_arrivals(keys, False)[-1])
        spread["running"].append(1000 * chord_arrivals(keys, True)[-1])
    first = [list(m) for m in msgs[:6]]
    return {"plain_bytes": len(plain), "running_bytes": len(run), "messages": len(msgs), "first": first,
            "plain_hex": plain[:18].hex(" "), "running_hex": run[:14].hex(" "), "decoded": [list(x) for x in W.decode(run)[:6]],
            "byte_us": W.BYTE_S * 1e6, "sizes": sizes, "spread": spread,
            "bend_cents": {"2": 400 / 16384, "48": 9600 / 16384}, "bend_example": list(W.bend(0, 8192 + 2048))}


def compute_zipper() -> dict:
    secs = 4.0
    n = int(secs * SR)
    t = np.arange(n) / SR
    u = t / secs
    lo, hi = 200.0, 2000.0
    smooth = lo * (hi / lo) ** u
    cc = np.floor(u * 127 + 0.5)
    # a controller sent every 10 ms, its value one of 128
    held = np.repeat(cc[:: int(0.01 * SR)], int(0.01 * SR))[:n]
    stepped = lo * (hi / lo) ** (held / 127)
    x = 0.5 * S1.saw_polyblep(hz(36), n)
    a = S1.ladder(x, stepped, 3.6)
    b = S1.ladder(x, smooth, 3.6)
    c = concat([C(fade(norm_rms(a))), C(fade(norm_rms(b)))], gap=0.8, names=["stepped", "smooth"])
    step_cents = 1200 * np.log2(hi / lo) / 127
    return {"answer": "first", "step_cents": float(step_cents), "lo": lo, "hi": hi, "steps": 128,
            "curve_t": t[::480].tolist(), "stepped": stepped[::480].tolist(), "smooth": smooth[::480].tolist(),
            "starts": {"stepped": float(c.events["stepped"]), "smooth": float(c.events["smooth"])},
            "clips": {"two": save("zipper.two", c, detail="a resonant ladder filter swept from 200 Hz to 2 kHz over four seconds, first by a MIDI controller (128 values, sent every 10 ms), then smoothly")}}


def compute_smf() -> dict:
    notes = tune_notes(phrases=range(6), base=60, beat=0.5)
    div = 480
    tr = []
    for m, a, d in notes:
        on = int(round(a / 0.5 * div))
        off = int(round((a + 0.9 * d) / 0.5 * div))
        tr.append((on, W.note_on(0, m, 90)))
        tr.append((off, W.note_off(0, m)))
    data = W.write_smf([tr], division=div, tempo_us=500000)
    back = W.read_smf(data)
    ons = [(t_s, m[1]) for _, m, t_s in back["events"] if m[0] & 0xF0 == 0x90 and m[2] > 0]
    ok = all(abs(t_s - a) < 1e-9 and k == m for (t_s, k), (m, a, d) in zip(ons, notes))
    seconds = notes[-1][1] + notes[-1][2]
    wav = seconds * SR * 2 * 3
    return {"bytes": len(data), "head_hex": data[:22].hex(" "), "events": len(back["events"]), "notes": len(notes), "roundtrip": bool(ok),
            "wav_bytes": wav, "seconds": seconds, "vlq": {str(v): W.vlq(v).hex(" ") for v in (0, 127, 128, 480, 16383, 16384)}}


def bassline():
    """A sixteen-step line: (step, key, accent, slide); None for a rest."""
    return [(0, 36, 1, 0), (1, 36, 0, 0), (2, 48, 0, 1), (3, 36, 0, 0), (5, 39, 1, 0), (6, 36, 0, 0), (7, 46, 0, 1), (8, 48, 1, 0),
            (10, 36, 0, 0), (11, 43, 0, 1), (12, 41, 1, 0), (13, 36, 0, 0), (14, 39, 0, 0), (15, 46, 1, 1)]


def compute_steps() -> dict:
    bpm = 126
    step = 60 / bpm / 4
    line = bassline()
    bars = 4
    n = int((bars * 16 * step + 0.5) * SR)
    f = np.zeros(n)
    gate = np.zeros(n)
    acc = np.zeros(n)
    events = []
    for b in range(bars):
        for j, (s, k, a, sl) in enumerate(line):
            t0 = (16 * b + s) * step
            nxt = line[j + 1][0] if j + 1 < len(line) else 16
            length = (nxt - s) * step if sl else 0.55 * step
            events.append([t0, k, a, sl, length])
    events.sort()
    cur = hz(36)
    for t0, k, a, sl, length in events:
        i0, i1 = int(t0 * SR), int((t0 + length) * SR)
        gate[i0:i1] = 1.0
        acc[i0:i1] = a
    # pitch: jumps on each note, glides (60 ms) into a note after a slide
    target = np.zeros(n)
    for j, (t0, k, a, sl, length) in enumerate(events):
        i0 = int(t0 * SR)
        target[i0:] = hz(k)
    glide = np.ones(n) * 0.0
    for j, (t0, k, a, sl, length) in enumerate(events[1:], start=1):
        if events[j - 1][3]:
            i0 = int(t0 * SR)
            glide[i0:i0 + int(0.06 * SR)] = 1.0
    f[0] = target[0]
    g = 1 - np.exp(-1 / (0.02 * SR))
    for i in range(1, n):
        f[i] = f[i - 1] + g * (target[i] - f[i - 1]) if glide[i] else target[i]
    t = np.arange(n) / SR
    env = np.zeros(n)
    last_on = 0.0
    for t0, k, a, sl, length in events:
        pass
    # a filter envelope restarted on every non-slid note
    starts = [e[0] for j, e in enumerate(events) if j == 0 or not events[j - 1][3]]
    since = np.full(n, 10.0)
    for s0 in starts:
        i0 = int(s0 * SR)
        since[i0:] = t[i0:] - s0
    fenv = np.exp(-since / 0.12)
    cutoff = 300 * 2 ** ((2.0 + 1.5 * acc) * fenv)
    x = 0.6 * S1.saw_polyblep(f, n) * np.convolve(gate * (0.7 + 0.3 * acc), np.ones(96) / 96, mode="same")
    y = S1.ladder(x, cutoff, 3.3)
    c = concat([C(fade(norm_rms(y)))], names=["line"])
    return {"bpm": bpm, "line": [list(e) for e in line], "clips": {"one": save("steps.one", c, detail="a sixteen-step bass line at 126 beats a minute, played four times: a sawtooth through Part 51's ladder, accented steps opening the filter further, slid steps gliding into the next")}}


DRUM = {"bd": lambda: S1.kick_circuit(seconds=0.6), "sn": lambda: S1.snare_circuit(), "cp": lambda: S1.clap_circuit(), "hh": lambda: SONG.hat808(False)}


def compute_pattern() -> dict:
    cyc = 2.0
    mel = "c4 e4 [g4 g4] <a4 c5 b4 e5>"
    drm = "bd [~ bd] sn [bd hh]"
    me = W.pattern_events(mel, 4, cyc)
    de = W.pattern_events(drm, 4, cyc)
    ev = [(int(a * SR), W.note_number(sym), 0.8, int(0.85 * d * SR), "lead") for a, d, sym in me]
    eng = W.Engine(ev, tracks={"lead": {"cut": 2600.0, "d": 0.3, "s": 0.4}})
    n = int((4 * cyc + 0.6) * SR)
    lead = eng.render(n, 256)
    parts = [(C(DRUM[sym]()), a, {"bd": 0.0, "sn": -4.0, "cp": -5.0, "hh": -10.0}[sym]) for a, d, sym in de]
    dr = mix(parts, duration=n / SR).y[:n]
    y = norm_rms(lead) + 0.8 * norm_rms(dr)
    c = concat([C(fade(norm_rms(y)))], names=["loop"])
    return {"mel": mel, "drums": drm, "mel_events": [[a, d, s] for a, d, s in me], "drum_events": [[a, d, s] for a, d, s in de], "cycle": cyc,
            "clips": {"one": save("pattern.one", c, detail="two lines of the pattern language, four cycles: a melody on the engine's sawtooth voice, and drums from Part 51's circuits")}}


def busy_engine(seconds):
    rng = np.random.default_rng(7)
    ev = []
    for i in range(int(seconds * 8)):
        for j in range(3):
            ev.append((int((i * 0.125 + 0.0001 * j) * SR) + int(rng.integers(0, 50)), int(rng.choice([48, 52, 55, 60, 64, 67, 72])) + 12 * (j - 1), 0.6, int(0.3 * SR),
                       ["pad", "lead", "bass"][j]))
    tracks = {"pad": {"cut": 1500.0, "a": 0.05, "r": 0.4}, "lead": {"cut": 3500.0, "chain": [W.Limiter(96, 0.2)]}, "bass": {"cut": 600.0}}
    return ev, tracks


def compute_callback() -> dict:
    secs = 4.0
    n = int(secs * SR)
    ev, tracks = busy_engine(secs)

    def fresh():
        tr = {k: ({kk: vv for kk, vv in v.items() if kk != "chain"} | ({"chain": [W.Limiter(96, 0.2)]} if "chain" in v else {})) for k, v in tracks.items()}
        return W.Engine(ev, tracks=tr)
    ref = fresh().render(n)
    blocks = [32, 64, 128, 256, 512, 1024, 2048]
    same, cost = [], []
    for B in blocks:
        tm = []
        y = fresh().render(n, B, tm)
        same.append(bool(np.array_equal(y, ref)))
        cost.append(float(np.median(tm[3:])) * 1000)
    latency = [1000 * B / SR for B in blocks]
    load_ = [c / l for c, l in zip(cost, latency)]
    # dropouts: a block that misses its deadline plays silence; simulated with the measured cost at 128 samples,
    # scaled to a heavy session (60 per cent load), plus rare stalls from the operating system
    rng = np.random.default_rng(3)
    B = 128
    nb = n // B
    budget = B / SR
    t_need = 0.6 * budget * (1 + 0.15 * rng.standard_normal(nb))
    stalls = rng.random(nb) < 0.004
    t_need[stalls] += rng.exponential(3 * budget, stalls.sum())
    miss = t_need > budget
    dropped = ref.copy()
    for i in np.where(miss)[0]:
        dropped[i * B:(i + 1) * B] = 0.0
    c = concat([C(norm_rms(ref)), C(norm_rms(dropped))], gap=0.8, names=["clean", "dropouts"])
    return {"blocks": blocks, "identical": same, "cost_ms": cost, "latency_ms": latency, "load": load_, "missed": int(miss.sum()),
            "blocks_total": int(nb), "voices": len(ev),
            "starts": {"clean": float(c.events["clean"]), "dropouts": float(c.events["dropouts"])},
            "clips": {"two": save("callback.two", c, detail="a busy passage from the engine, first clean, then with every block that missed its 2.7 ms deadline played as silence (deadlines simulated)")}}


def compute_timing() -> dict:
    bpm = 120
    step = 60 / bpm / 4
    hits = [i * step + 0.0137 for i in range(32)]
    B = 1024
    snapped = [np.floor(t * SR / B) * B / SR for t in hits]
    err = [1000 * (a - b) for a, b in zip(hits, snapped)]

    def render(times):
        parts = [(C(SONG.hat808(False)), t, -6.0 if i % 2 else 0.0) for i, t in enumerate(times)]
        parts += [(C(S1.kick_circuit(seconds=0.5)), times[i], 0.0) for i in range(0, 32, 4)]
        return mix(parts, duration=32 * step + 0.6).y
    a = render(snapped)
    b = render(hits)
    c = concat([C(norm_rms(b)), C(norm_rms(a))], gap=0.8, names=["exact", "snapped"])
    return {"answer": "second", "block": B, "block_ms": 1000 * B / SR, "err_ms": err, "max_ms": float(max(err)), "sd_ms": float(np.std(err)),
            "starts": {"snapped": float(c.events["snapped"]), "exact": float(c.events["exact"])},
            "clips": {"two": save("timing.two", c, detail="sixteenth-note hi-hats over a kick at 120 beats a minute: every hit placed to the sample, then every hit moved to the start of its 1024-sample block")}}


def drum_loop(bars=2, bpm=100):
    step = 60 / bpm / 4
    pat = {"bd": [0, 7, 10], "sn": [4, 12], "hh": [0, 2, 4, 6, 8, 10, 12, 14]}
    parts = []
    for b in range(bars):
        for k, steps in pat.items():
            for s in steps:
                parts.append((C(DRUM[k]()), (16 * b + s) * step, {"bd": 0.0, "sn": -3.0, "hh": -12.0}[k]))
    return mix(parts, duration=bars * 16 * step + 0.5).y


def compute_pdc() -> dict:
    x = drum_loop()
    x = 0.5 * x / np.max(np.abs(x))
    D = int(0.005 * SR)
    lim = W.Limiter(D, ceiling=0.06, release_s=0.06)
    wet = lim.process(x.copy())
    g = 1.2
    raw = x + g * wet                                    # the dry path not delayed: the paths are 5 ms apart
    dly = W.Delay(D)
    dd = dly.process(x.copy())
    fixed = dd + g * wet
    f = np.geomspace(20, 20000, 400)
    H = np.abs(1 + g * 0.6 * np.exp(-2j * np.pi * f * D / SR))
    c = concat([C(norm_rms(raw)), C(norm_rms(fixed))], gap=0.8, names=["late", "aligned"])
    return {"latency_samples": D, "latency_ms": 1000 * D / SR, "notch_hz": SR / (2 * D), "f": f.tolist(), "H_db": (20 * np.log10(H + 1e-9)).tolist(),
            "starts": {"late": float(c.events["late"]), "aligned": float(c.events["aligned"])},
            "clips": {"two": save("pdc.two", c, detail="a drum loop from Part 51's circuits, mixed with a copy through a look-ahead limiter 5 ms late: first with the dry path not delayed, then delayed to match")}}


# ---------------------------------------------------------------------------------------------------------- Variation 53
CHORDS = {0: ["I", "I", "IV", "I"], 1: ["IV", "I", "V", "I"], 2: ["I", "IV", "I", "V"], 3: ["I", "IV", "I", "V"], 4: ["I", "I", "IV", "I"], 5: ["IV", "I", "V", "I"]}
ROOTS = {"I": 0, "IV": 5, "V": 7}
TRIAD = {"I": (0, 4, 7), "IV": (5, 9, 12), "V": (7, 11, 14)}


def tracker_rows(phrases=(0, 1)):
    """Four channels, one row a quaver (two rows a beat): lead, bass, arpeggio, drums (instrument names)."""
    rows = []
    for p in phrases:
        mel = [(1, 1), (1, 1), (5, 1), (5, 1), (6, 1), (6, 1), (5, 2)] if p in (0, 4) else ([(4, 1), (4, 1), (3, 1), (3, 1), (2, 1), (2, 1), (1, 2)] if p in (1, 5) else [(5, 1), (5, 1), (4, 1), (4, 1), (3, 1), (3, 1), (2, 2)])
        lead = []
        for deg, beats in mel:
            lead += [(72 + MAJOR[deg], "lead")] + [None] * (2 * beats - 1)
        for r in range(16):
            ch = CHORDS[p][r // 4]
            bass = (36 + ROOTS[ch] + (12 if r % 4 == 2 else 0), "bass") if r % 2 == 0 else None
            arp = (60 + TRIAD[ch][r % 3], "arp")
            dr = ("bd" if r % 4 == 0 else ("sn" if r % 8 == 4 else "hh"), "drum")
            rows.append([lead[r], bass, arp, dr])
    return rows


INS = {"lead": {"cut": 2800.0, "d": 0.4, "s": 0.6, "gain": 0.3}, "bass": {"cut": 500.0, "d": 0.2, "s": 0.3, "gain": 0.35},
       "arp": {"cut": 1800.0, "d": 0.08, "s": 0.0, "r": 0.05, "gain": 0.12}}


def render_tracker(rows, row_s):
    ev = W.tracker_events(rows, row_s, 4)
    syn = [(int(a * SR), k, 0.8, int(0.9 * d * SR), ins) for a, d, k, ins, ch in ev if ins != "drum"]
    eng = W.Engine(syn, tracks={k: dict(v) for k, v in INS.items()})
    n = int((len(rows) * row_s + 1.0) * SR)
    y = eng.render(n, 128)
    dp = [(C(DRUM[k]()), a, {"bd": -2.0, "sn": -6.0, "hh": -14.0}[k]) for a, d, k, ins, ch in ev if ins == "drum"]
    dr = mix(dp, duration=n / SR).y[:n]
    return norm_rms(y) + 0.7 * norm_rms(dr), ev


def compute_tune53() -> dict:
    row_s = 0.18
    rows = tracker_rows((0, 1))
    trk, ev = render_tracker(rows, row_s)
    # a tempo canon: the whole Tune in four voices at 3 : 4 : 5 : 6, meeting on the last note
    notes = [(60 + MAJOR[e["degree"]], e["t"], e["dur"]) for e in T.events(1.0, None)]
    ratios = [3.0, 4.0, 5.0, 6.0]
    canon, t_conv = W.tempo_canon(notes, [r / 2.0 for r in ratios], len(notes) - 1)
    offs = [0, 12, 7, -12]
    evc = []
    for v, k, a, d in canon:
        evc.append((int(a * SR), k + offs[v], 0.7, int(0.85 * d * SR), f"v{v}"))
    cuts = {"v0": 1200.0, "v1": 2400.0, "v2": 3200.0, "v3": 800.0}
    eng = W.Engine(evc, tracks={k: {"cut": c, "d": 0.25, "s": 0.35, "gain": 0.22} for k, c in cuts.items()})
    n = int((t_conv + 2.5) * SR)
    can = eng.render(n, 256)
    same = bool(np.array_equal(can, W.Engine(evc, tracks={k: {"cut": c, "d": 0.25, "s": 0.35, "gain": 0.22} for k, c in cuts.items()}).render(n)))
    full = np.concatenate([fade(norm_rms(trk)), np.zeros(int(0.8 * SR)), fade(norm_rms(can))])
    c = Clip(full, SR)
    c.events["tracker"] = 0.0
    c.events["canon"] = len(trk) / SR + 0.8
    rows_show = [[None if x is None else [x[0], x[1]] for x in r] for r in rows]
    return {"rows": rows_show, "row_s": row_s, "ratios": ratios, "t_conv": float(t_conv), "canon": [[v, k, a, d] for v, k, a, d in canon],
            "identical": same, "seconds": c.duration, "starts": {"tracker": 0.0, "canon": float(c.events["canon"])}, "notes_canon": len(canon),
            "clips": {"variation53": save("tune.variation53", c, detail="the Tune's first two phrases as a four-channel tracker module (lead, bass, arpeggio, drum circuits); then the whole Tune as a tempo canon in four voices at speeds 3 : 4 : 5 : 6, all arriving together on the last note")}}


def compute_variation() -> dict:
    t = load("tune53")
    return {"part": 53, "title": "as a tracker module and a tempo canon at 3 : 4 : 5 : 6", "seconds": round(t["seconds"], 1),
            "measure": f"{len(t['rows'])} tracker rows; four voices meeting on the last note after {t['t_conv']:.1f} s; block and offline renders identical",
            "clip": "tune.variation53"}


ITEMS = {"hook": compute_hook, "musicbox": compute_musicbox, "pianola": compute_pianola, "musicn": compute_musicn, "bytes": compute_bytes,
         "zipper": compute_zipper, "smf": compute_smf, "steps": compute_steps, "pattern": compute_pattern, "callback": compute_callback,
         "timing": compute_timing, "pdc": compute_pdc, "tune53": compute_tune53, "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
