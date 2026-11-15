"""Precompute everything numerical, and every sound, in Part 62 of *Music, Built* ("Beat, Chords and Structure").

    python -m videos.music.music62.compute              # everything missing (a few minutes)
    python -m videos.music.music62.compute --force hook

Numbers are cached in ``.cache/music62/<name>.json``, sounds in ``.cache/music62/audio/``.  The tools are Monochord's
listeners (``explainer/music/monochord/mir/rhythm.py``, on Part 61's spectral flux).  Every performance is rendered by
Monochord with its beats, chords and sections known exactly: Part 56's session at 100 beats a minute, Part 38's piano
played with rubato, Part 8's voice sung freely.

Items:
    hook        an ear question: two click tracks over the session, one on the beat and one 80 ms late
    tempo       novelty, tempogram and the tempo estimate on the session; a slow piece and its double-time reading
    beats       Ellis's dynamic programme on the session and on a rubato piano performance; scores
    downbeat    which beat starts the bar, from the low band (an ear question)
    halfdouble  the slow piece with clicks at the tempo written and at the tempo found
    chords      chroma of the session's Tune; chords frame by frame, by an HMM, and by an HMM with Bach's prior
    cover       a cover in another key and tempo matched by key-invariant DTW (an ear question)
    align       DTW between a deadpan rendering and a rubato performance; online following; errors in ms
    structure   the whole Tune by the session: self-similarity, novelty, boundaries and section labels
    follow      Variation 62: the Tune sung freely, accompanied live by a score follower
    variation   the Variations ledger, row 62
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import chorales as CHO
from explainer.music.monochord import progression as PR
from explainer.music.monochord import tune as T
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.mir import rhythm as RH
from explainer.music.monochord.partkit import saver
from videos.music.music38 import compute as P38
from videos.music.music40 import compute as P40
from videos.music.music56 import compute as P56

CACHE = Cache("music62")
CLIPS = ClipStore("music62")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
BEAT = P56.BEAT                                          # 0.6 s: 100 beats a minute
MAJOR = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
CHORD_INDEX = {"C": 0, "F": 5, "G": 7}


def C(y) -> Clip:
    return Clip(np.asarray(y, float), SR)


def fade(y, a=0.005, r=0.08):
    y = np.array(y, float)
    ka, kr = max(int(a * SR), 1), max(int(r * SR), 1)
    y[:ka] *= np.linspace(0, 1, ka)
    y[len(y) - kr:] *= np.linspace(1, 0, kr)
    return y


_V: dict = {}


def session_mix(phrases=(0, 1)):
    key = ("mix", tuple(phrases))
    if key not in _V:
        s = P56.session(tuple(phrases))
        y = sum(v for k, v in s["tracks"].items() if k in P56.TRACKS)
        _V[key] = y / np.max(np.abs(y)) * 0.9
    return _V[key]


def click(t_list, seconds, hz=2000.0, gain=0.35):
    y = np.zeros(int(seconds * SR))
    n = int(0.02 * SR)
    burst = np.sin(2 * np.pi * hz * np.arange(n) / SR) * np.exp(-np.arange(n) / (0.004 * SR)) * gain
    for t in t_list:
        k = int(t * SR)
        if 0 <= k < len(y) - n:
            y[k:k + n] += burst
    return y


def rubato_times(n_beats, beat=0.5, depth=0.18, seed=0):
    """Beat times of an expressive performance: a slow arch of tempo over each eight-beat phrase, a held phrase end,
    and a little jitter."""
    rng = np.random.default_rng(seed)
    t, out = 0.0, []
    for k in range(n_beats + 1):
        out.append(t)
        phase = (k % 8) / 8
        stretch = 1 + depth * math.cos(2 * math.pi * phase) + (0.25 if k % 8 == 7 else 0.0) + float(rng.normal(0, 0.02))
        t += beat * stretch
    return np.array(out)


def tune_events(phrases):
    return T.events(1.0, list(phrases))                  # times in beats


def piano_tune(beat_times, phrases=(0, 1), chords=True, vel=0.9):
    """The Tune (and its chords) on Part 38's piano, each note placed at the performance's beat times."""
    def at(b):
        k = int(math.floor(b))
        f = b - k
        k = min(k, len(beat_times) - 2)
        return beat_times[k] + f * (beat_times[k + 1] - beat_times[k])
    placed = []
    for e in tune_events(phrases):
        a, b = at(e["t"]), at(e["t"] + e["dur"])
        placed.append((P38.arr(P38.piano(72 + MAJOR[e["degree"]], max(0.2, b - a) * 0.95, vel)), a, 0.0))
    if chords:
        syms = "".join(P56.CHORDS[p] for p in phrases)
        for i, sym in enumerate(syms):
            a, b = at(2 * i), at(2 * i + 2)
            r = CHORD_INDEX[sym]
            for m in (48 + r, 52 + (r + 4 - 52) % 12, 55 + (r + 7 - 55) % 12):
                placed.append((P38.arr(P38.piano(m, max(0.2, b - a) * 0.95, 0.6)), a, -5.0))
    end = beat_times[min(len(beat_times) - 1, 8 * len(phrases))] + 1.2
    y = mix(placed, duration=end).y
    return y / np.max(np.abs(y)) * 0.9


def sung_tune(beat_times, phrases=(0, 1), seed=1):
    def at(b):
        k = min(int(math.floor(b)), len(beat_times) - 2)
        return beat_times[k] + (b - k) * (beat_times[k + 1] - beat_times[k])
    notes = [(72 + MAJOR[e["degree"]] - 12, at(e["t"]), at(e["t"] + e["dur"]) - at(e["t"])) for e in tune_events(phrases)]
    v = CH.sing(notes, "soprano", "a", seed=seed)
    return v / np.max(np.abs(v)) * 0.9


def slow_piece(seconds=14.0, bpm=50.0):
    """A slow piece: a chord every beat at 50 beats a minute, with eighth notes in the melody, which many listeners
    (and machines) hear at double time."""
    beat = 60.0 / bpm
    placed = []
    nb = int(seconds / beat)
    prog = [0, 5, 7, 0] * 8
    for k in range(nb):
        r = prog[k % len(prog)]
        for m in (48 + r, 52 + (r + 4 - 52) % 12, 55 + (r + 7 - 55) % 12):
            placed.append((P38.arr(P38.piano(m, beat * 0.9, 0.65)), k * beat, -4.0))
        for h in range(2):
            m = 72 + [0, 4, 7, 4, 5, 9, 7, 2][(2 * k + h) % 8] + r % 2
            placed.append((P38.arr(P38.piano(m, beat / 2 * 0.9, 0.8 if h == 0 else 0.65)), k * beat + h * beat / 2, 0.0 if h == 0 else -3.0))
    y = mix(placed, duration=nb * beat + 1.0).y
    return y / np.max(np.abs(y)) * 0.9, np.arange(nb) * beat


# ---------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    y = session_mix((0, 1))
    secs = len(y) / SR
    beats = np.arange(0, 16) * BEAT
    on = 0.75 * y + click(beats, secs)
    late = 0.75 * y + click(beats + 0.08, secs)
    c = concat([C(fade(late)), C(fade(on))], gap=1.0, names=["first", "second"])
    return {"answer": "second", "offset_ms": 80, "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("hook.two", c, detail="Part 56's session with a click track: first 80 ms late, then on the beat")}}


def compute_tempo() -> dict:
    y = session_mix((0, 1))
    nv = RH.novelty(y)
    tg = RH.tempogram(nv["nov"], nv["hop_s"], window=6.0, step=0.5)
    tp = RH.tempo(nv["nov"], nv["hop_s"])
    ys, true_slow = slow_piece()
    ns = RH.novelty(ys)
    ts = RH.tempo(ns["nov"], ns["hop_s"])
    ts_flat = RH.tempo(ns["nov"], ns["hop_s"], prior_octaves=10.0)
    return {"nov": nv["nov"][::2].tolist(), "t": nv["t"][::2].tolist(), "A": tg["A"][::3].tolist(), "bpm_axis": tg["bpm"][::3].tolist(),
            "tg_t": tg["t"].tolist(), "bpm": tp["bpm"], "ac_bpm": tp["bpm_axis"].tolist(), "ac": tp["ac"].tolist(), "weighted": tp["weighted"].tolist(),
            "slow_true": 50.0, "slow_found": ts["bpm"], "slow_flat": ts_flat["bpm"]}


def compute_beats() -> dict:
    out = {}
    y = session_mix((0, 1, 2, 3))
    nv = RH.novelty(y)
    tp = RH.tempo(nv["nov"], nv["hop_s"])
    est = RH.track_beats(nv["nov"], nv["hop_s"], tp["bpm"])
    ref = np.arange(0, 32) * BEAT
    out["session"] = {"bpm": tp["bpm"], "est": est.tolist(), "ref": ref.tolist(), **{k: v for k, v in RH.beat_scores(ref, est).items()}}
    bt = rubato_times(16, beat=0.55)
    yr = piano_tune(bt, (0, 1))
    nr = RH.novelty(yr)
    tr = RH.tempo(nr["nov"], nr["hop_s"])
    rows = []
    for tight in (400.0, 100.0, 20.0):
        er = RH.track_beats(nr["nov"], nr["hop_s"], tr["bpm"], tightness=tight)
        rows.append({"tightness": tight, **{k: v for k, v in RH.beat_scores(bt[:16], er).items() if k != "levels"}, "est": er.tolist()})
    out["rubato"] = {"bpm": tr["bpm"], "ref": bt[:16].tolist(), "rows": rows, "ibi": np.diff(bt[:17]).tolist()}
    best = max(rows, key=lambda r: r["f"])
    secs = len(yr) / SR
    a = 0.75 * yr + click(best["est"], secs)
    s = 0.75 * session_mix((0, 1)) + click([b for b in est if b < 16 * BEAT], len(session_mix((0, 1))) / SR)
    out["clips"] = {"session": save("beats.session", C(fade(s)), detail="the beat tracker's clicks over Part 56's session"),
                    "rubato": save("beats.rubato", C(fade(a)), detail="the beat tracker's clicks over the Tune played with rubato on Part 38's piano")}
    return out


def compute_downbeat() -> dict:
    """Which beat starts the bar?  The low band's novelty (the kick drum, the bass) at each beat, folded by the bar's
    phase: the phase with the most low-band energy is called beat one."""
    y = session_mix((0, 1, 2, 3))
    from scipy.signal import butter, sosfilt
    low = sosfilt(butter(4, 150, fs=SR, output="sos"), y)
    nv = RH.novelty(low)
    beats = np.arange(0, 32) * BEAT
    strength = []
    for ph in range(4):
        idx = [int(round(b / nv["hop_s"])) for b in beats[ph::4]]
        strength.append(float(np.mean([nv["nov"][max(0, i - 2):i + 3].max() for i in idx if i < len(nv["nov"])])))
    found = int(np.argmax(strength))
    y2 = session_mix((0, 1))
    secs = len(y2) / SR
    b16 = np.arange(16) * BEAT

    def accented(phase):
        return 0.75 * y2 + click(b16, secs, gain=0.18) + click(b16[phase::4], secs, hz=3000.0, gain=0.45)
    c = concat([C(fade(accented(1))), C(fade(accented(0)))], gap=1.0, names=["first", "second"])
    return {"strength": strength, "found": found, "answer": "second",
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("downbeat.two", c, detail="Part 56's session with clicks on every beat and a high accent every four: first on the second beat of each bar, then on the first")}}


def compute_cover() -> dict:
    """Cover-song matching: chroma sequences compared by DTW under all twelve transpositions (the optimal
    transposition index), so that a version in another key and tempo still matches."""
    from explainer.music.monochord import melody as M
    orig = session_mix((0, 1))
    bt = rubato_times(16, beat=0.5, depth=0.12, seed=2)
    cover = piano_tune(bt, (0, 1))
    cover = np.interp(np.arange(0, len(cover), 2 ** (-5 / 12)), np.arange(len(cover)), cover)       # up a fourth
    other_m = M.corpus(["Frère Jacques"])[0]
    placed, t = [], 0.0
    for p_, b_ in zip(other_m.pitches[:16], other_m.beats[:16]):
        placed.append((P38.arr(P38.piano(72 + p_, b_ * 0.5 * 0.95, 0.9)), t, 0.0))
        t += b_ * 0.5
    other = mix(placed, duration=t + 1.0).y
    other = other / np.max(np.abs(other)) * 0.9
    Co = RH.chroma(orig, hop=4800)["C"]

    def score(y):
        Cy = RH.chroma(y, hop=4800)["C"]
        best = None
        for k in range(12):
            d = RH.dtw(Co, np.roll(Cy, k, axis=0))
            cost = float(d["D"][-1, -1] / len(d["path"]))
            if best is None or cost < best[0]:
                best = (cost, k)
        no_shift = RH.dtw(Co, Cy)
        return {"cost": best[0], "shift": best[1], "cost_no_shift": float(no_shift["D"][-1, -1] / len(no_shift["path"]))}
    sc = {"cover": score(cover), "other": score(other)}
    c = concat([C(fade(orig)), C(fade(cover)), C(fade(other))], gap=0.9, names=["first", "second", "third"])
    return {"scores": sc, "answer": "third", "starts": {k: float(c.events[k]) for k in ("first", "second", "third")},
            "clips": {"three": save("cover.three", c, detail="Part 56's session playing the Tune; Part 38's piano playing it a fourth higher, with rubato; the same piano playing the opening of Frère Jacques")}}


def compute_halfdouble() -> dict:
    ys, true_b = slow_piece()
    ns = RH.novelty(ys)
    ts = RH.tempo(ns["nov"], ns["hop_s"])
    est = RH.track_beats(ns["nov"], ns["hop_s"], ts["bpm"])
    secs = len(ys) / SR
    sc = RH.beat_scores(true_b, est)
    k = int(8.0 * SR)
    written = (0.75 * ys + click(true_b, secs))[:k]
    found = (0.75 * ys + click(est, secs))[:k]
    c = concat([C(fade(written)), C(fade(found))], gap=1.0, names=["written", "found"])
    return {"found_bpm": ts["bpm"], "written_bpm": 50.0, "scores": {kk: v for kk, v in sc.items()},
            "starts": {"written": float(c.events["written"]), "found": float(c.events["found"])},
            "clips": {"two": save("halfdouble.two", c, detail="a slow piano piece at 50 beats a minute: clicks at the tempo written, then at the tempo the tracker found")}}


def bach_prior():
    book = CHO.load()
    seqs = PR.symbols(book, "major")
    return RH.transitions_from_romans(seqs, key=0)


def compute_chords() -> dict:
    phrases = (0, 1, 2, 3)
    s = P56.session(phrases)
    tr = s["tracks"]
    y = tr["vox"] + 0.5 * tr["piano"] + 0.5 * tr["guitar"] + tr["bass"] + tr["kick"] + tr["snare"] + tr["hat"]
    y = y / np.max(np.abs(y)) * 0.9
    ch = RH.chroma(y)
    labels = RH.chord_labels()
    syms = s["syms"]
    t = ch["t"]
    truth = np.array([CHORD_INDEX[syms[min(int(tt // (2 * BEAT)), len(syms) - 1)]] if tt < len(syms) * 2 * BEAT else 24 for tt in t])
    plain = RH.recognize(ch["C"])
    prior = RH.recognize(ch["C"], A=bach_prior())
    acc = lambda p: float(np.mean(p[: len(truth)] == truth))
    k = int(8 * 2 * BEAT / ch["hop_s"])
    c = C(fade(y[: int(16 * BEAT * SR)]))
    return {"labels": labels, "truth": truth.tolist(), "frame": plain["frame"].tolist(), "hmm": plain["hmm"].tolist(), "bach": prior["hmm"].tolist(),
            "acc": {"frame": acc(plain["frame"]), "hmm": acc(plain["hmm"]), "bach": acc(prior["hmm"])},
            "chroma": ch["C"][:, :k].tolist(), "hop_s": ch["hop_s"], "syms": syms,
            "clips": {"tune": save("chords.tune", c, detail="Part 56's session playing the Tune's first two phrases, the voice loud and the chords quiet")}}


def compute_align() -> dict:
    deadpan = np.arange(17) * 0.5
    bt = rubato_times(16, beat=0.55, depth=0.22, seed=4)
    ya = piano_tune(deadpan, (0, 1))
    yb = piano_tune(bt, (0, 1))
    A = RH.chroma(ya, hop=2400)["C"]
    Bc = RH.chroma(yb, hop=2400)
    hop = Bc["hop_s"]
    d = RH.dtw(A, Bc["C"])
    path = d["path"]
    # error: for each beat of the score, the performance time the path gives, against the truth
    errs, on_errs = [], []
    on = RH.oltw(A, Bc["C"])
    for k in range(16):
        fa = int(round(deadpan[k] / hop))
        js = path[path[:, 0] == min(fa, A.shape[1] - 1), 1]
        if len(js):
            errs.append(abs(js.mean() * hop - bt[k]))
        hits = np.where(on >= fa)[0]
        if len(hits):
            on_errs.append(abs(hits[0] * hop - bt[k]))
    c = concat([C(fade(ya)), C(fade(yb))], gap=1.0, names=["deadpan", "rubato"])
    return {"path": path[::2].tolist(), "cost": d["cost"][::2, ::2].tolist(), "hop_s": hop, "deadpan": deadpan.tolist(), "rubato": bt.tolist(),
            "err_ms": float(1000 * np.median(errs)), "err_max_ms": float(1000 * np.max(errs)), "online_ms": float(1000 * np.median(on_errs)),
            "online_max_ms": float(1000 * np.max(on_errs)),
            "starts": {"deadpan": float(c.events["deadpan"]), "rubato": float(c.events["rubato"])},
            "clips": {"two": save("align.two", c, detail="the Tune with chords on Part 38's piano: played strictly, then with rubato")}}


def compute_structure() -> dict:
    y = session_mix((0, 1, 2, 3, 4, 5))
    ch = RH.chroma(y, hop=4800)
    S = RH.ssm(ch["C"])
    nov = RH.checkerboard_novelty(S, half=16)
    b = RH.boundaries(nov, ch["hop_s"], min_gap=3.0, delta=0.15)
    frames = [int(round(x / ch["hop_s"])) for x in b if 1.0 < x < len(y) / SR - 2.0]
    labels = RH.segment_labels(ch["C"], frames, threshold=0.95)
    true_b = [2 * 8 * BEAT, 4 * 8 * BEAT]
    c = C(fade(y))
    return {"S": S[::2, ::2].tolist(), "nov": nov.tolist(), "hop_s": ch["hop_s"], "bounds": [f * ch["hop_s"] for f in frames], "labels": labels,
            "true_bounds": true_b, "seconds": c.duration,
            "clips": {"tune": save("structure.tune", c, detail="the whole Tune by Part 56's session: A, B, A")}}


def compute_follow() -> dict:
    bt = rubato_times(16, beat=0.55, depth=0.2, seed=8)
    voice = sung_tune(bt, (0, 1))
    score = piano_tune(np.arange(17) * 0.5, (0, 1), chords=False)
    A = RH.chroma(score, hop=2400)["C"]
    V = RH.chroma(voice, hop=2400)
    hop = V["hop_s"]
    pos = RH.oltw(A, V["C"])
    # the accompanist plays each chord when the follower believes the score has reached it, 60 ms later (latency)
    syms = "".join(P56.CHORDS[p] for p in (0, 1))
    placed, asyn = [], []
    for i, sym in enumerate(syms):
        target = int(round(2 * i * 0.5 / hop))
        hits = np.where(pos >= target)[0]
        if not len(hits):
            continue
        t_play = hits[0] * hop + 0.06
        asyn.append(t_play - bt[2 * i])
        r = CHORD_INDEX[sym]
        for m in (48 + r, 52 + (r + 4 - 52) % 12, 55 + (r + 7 - 55) % 12):
            placed.append((P38.arr(P38.piano(m, 1.0, 0.6)), t_play, -6.0))
    acc = mix(placed, duration=len(voice) / SR + 1.0).y
    n = max(len(voice), len(acc))
    both = np.r_[voice, np.zeros(n - len(voice))] + 0.6 * np.r_[acc, np.zeros(n - len(acc))] / (np.max(np.abs(acc)) + 1e-9)
    dead = np.zeros(n)
    for i, sym in enumerate(syms):
        r = CHORD_INDEX[sym]
        for m in (48 + r, 52 + (r + 4 - 52) % 12, 55 + (r + 7 - 55) % 12):
            z = P38.piano(m, 1.0, 0.6)
            k = int(2 * i * 0.5 * SR)
            dead[k:k + len(z)] += np.asarray(z)[: max(0, n - k)]
    stiff = np.r_[voice, np.zeros(n - len(voice))] + 0.6 * dead / (np.max(np.abs(dead)) + 1e-9)
    c = concat([C(fade(stiff / np.max(np.abs(stiff)) * 0.9)), C(fade(both / np.max(np.abs(both)) * 0.9))], gap=1.0, names=["stiff", "follow"])
    return {"asynchrony_ms": [1000 * a for a in asyn], "median_ms": float(1000 * np.median(np.abs(asyn))), "seconds": c.duration,
            "names": ["stiff", "follow"], "starts": {"stiff": float(c.events["stiff"]), "follow": float(c.events["follow"])},
            "clips": {"variation62": save("tune.variation62", c, detail="Variation 62: Part 8's voice singing the Tune freely, with piano chords played strictly on the written beats, then placed by a score follower listening to the voice")}}


def compute_variation() -> dict:
    f = load("follow")
    return {"part": 62, "title": "sung freely, and accompanied live by a machine that listens", "seconds": round(f["seconds"], 1),
            "measure": f"the follower's chords land a median {f['median_ms']:.0f} ms from the voice's beats",
            "clip": "tune.variation62"}


ITEMS = {"hook": compute_hook, "tempo": compute_tempo, "beats": compute_beats, "downbeat": compute_downbeat, "halfdouble": compute_halfdouble,
         "chords": compute_chords, "cover": compute_cover,
         "align": compute_align, "structure": compute_structure, "follow": compute_follow, "variation": compute_variation}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
