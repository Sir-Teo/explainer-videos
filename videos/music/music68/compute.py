"""Precompute everything numerical, and every sound, in Part 68 of *Music, Built* ("The Variations").

    python -m videos.music.music68.compute              # everything missing (some minutes: the chain is run end to end)
    python -m videos.music.music68.compute --force suite

Numbers are cached in ``.cache/music68/<name>.json``, sounds in ``.cache/music68/audio/``.  The suite is assembled
from every part's own Variation, as each part stored it (``.cache/musicN/audio/``); the round trip runs the Tune down the
series' chain (Part 43's timing, Part 38's piano, Part 50's room, Part 56's microphones and mix, Part 57's master, Part
58's coder) and back up it (Part 61's transcriber and quantizer, Part 15's key finder).

Items:
    hook        Variation 1 again, as Part 1 made it
    chain       the Tune at each stage down the chain, heard; how far each stage's sound is from the dry score
    roundtrip   the way back: notes transcribed and quantized at each stage and each bit rate, against the score
    order       ways to order 67 Variations into a suite: as built, by nearest sound, at random
    suite       the suite in three movements: an excerpt of every Variation, in the order they were made
    built       Monochord counted: modules, lines, tests, clips and hours of sound
    variation   the Variations ledger, row 68
"""

from __future__ import annotations

import glob
import json
import os

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat
from explainer.music.monochord import codec as K
from explainer.music.monochord import space as SPC
from explainer.music.monochord import roundtrip as RT
from explainer.music.monochord import tune as T
from explainer.music.monochord.mir import finder as F
from explainer.music.monochord.mir import transcribe as TR
from explainer.music.monochord.partkit import saver
from explainer.tts import REPO_ROOT
from videos.music.variations import LEDGER

CACHE = Cache("music68")
CLIPS = ClipStore("music68")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
MAJOR = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
BITRATES = (128, 64, 32, 16)
# Part 58's coder takes its band from a table with no entry for 16 kbit/s, and falls back to the full 18 kHz; between the
# table's 12 (5 kHz) and 24 kbit/s (7 kHz) the chain uses 5.5 kHz.  Item ``wide`` shows what the fallback does.
CUTOFF = {16: 5500.0}
EXCERPT = 8.5


def mono(c: Clip) -> np.ndarray:
    y = np.asarray(c.y, float)
    return y.mean(axis=1) if y.ndim == 2 else y


def C(y) -> Clip:
    y = np.asarray(y, float)
    k = int(0.01 * SR)
    y[:k] *= np.linspace(0, 1, k)
    r = int(0.4 * SR)
    y[-r:] *= np.linspace(1, 0, r)
    return Clip(y / (np.max(np.abs(y)) + 1e-12) * 0.9, SR)


def faded(y) -> Clip:
    """Fades only: the excerpts keep the levels ``excerpt`` gave them."""
    y = np.asarray(y, float).copy()
    k, r = int(0.01 * SR), int(0.5 * SR)
    y[:k] *= np.linspace(0, 1, k)
    y[-r:] *= np.linspace(1, 0, r)
    return Clip(y, SR)


def variation_clip(n: int) -> Clip:
    v = json.load(open(REPO_ROOT / ".cache" / f"music{n}" / "variation.json"))
    return ClipStore(f"music{n}").load(v["clip"])


def excerpt(c: Clip, seconds: float = EXCERPT) -> np.ndarray:
    """``seconds`` of a Variation from its first sound, levelled (``roundtrip.excerpt``)."""
    return RT.excerpt(c.y, c.sr, seconds)


# ---------------------------------------------------------------------------------------------- the chain
def tune_score():
    """The whole Tune as (key, onset s, offset s) at 120 beats a minute, C5 to A5."""
    ev = T.events(0.5, None)
    return [(72 + MAJOR[e["degree"]] - 12 * (MAJOR[e["degree"]] > 9), e["t"], e["t"] + e["dur"] * 0.95) for e in ev], [e["dur"] / 0.5 for e in ev]


def perform(score, rng):
    """Part 43's idea of a performance: a tempo that breathes over each two-bar arc, phrase ends held, a little timing
    noise; and dynamics that swell to the middle of each phrase.  Returns the notes and each note's gain in dB."""
    out, gains, t = [], [], 0.0
    for k, (m, a, b) in enumerate(score):
        d = (b - a) / 0.95
        stretch = 1.0 + 0.10 * np.sin(2 * np.pi * k / 14) + float(rng.normal(0, 0.02))
        if k % 7 == 6:
            stretch *= 1.3
        out.append((m, round(t, 3), round(t + d * stretch * 0.92, 3)))
        gains.append(4.0 * np.sin(np.pi * ((k % 7) + 0.5) / 7) - 2.0 + float(rng.normal(0, 0.7)))
        t += d * stretch
    return out, gains


STAGES = ("score", "played", "room", "mic", "master", "codec128", "codec64", "codec32", "codec16")


def run_chain(score, seed: int) -> tuple:
    """A melody's audio at each stage down the chain (48 kHz mono): the score played strictly on Part 38's piano
    (Part 61's renderer); performed (Part 43); in a room, a 1.4 s statistical tail (Part 55); through a microphone's
    band and a noise floor 50 dB down (Part 54); mastered by a soft limiter (Part 57); and through Part 58's coder at
    each bit rate."""
    from videos.music.music61 import compute as P61
    from scipy.signal import fftconvolve, butter, sosfiltfilt
    rng = np.random.default_rng(seed)
    dry = P61.render(score, "piano", score[-1][2] + 1.5)
    perf, gains = perform(score, rng)
    played = P61.render(perf, "piano", perf[-1][2] + 1.5, gains)
    ir = SPC.noise_tail(1.4, 1.6, seed=seed, stereo=False, start=0.012)
    wet = fftconvolve(played, ir)[: len(played)]
    wet *= 0.7 * np.sqrt(np.mean(played ** 2)) / (np.sqrt(np.mean(wet ** 2)) + 1e-12)
    room = played + wet
    g = 0.8 / np.max(np.abs(room))
    room, played_in_room = room * g, played * g
    mic = sosfiltfilt(butter(2, [60, 15000], btype="band", fs=SR, output="sos"), room) + rng.standard_normal(len(room)) * 10 ** (-50 / 20)
    master = np.tanh(2.2 * mic / np.max(np.abs(mic))) * 0.9
    out = {"score": dry, "played": played, "room": room, "mic": mic, "master": master}
    kbps = {}
    for kb in BITRATES:
        e = K.encode(master, kb, cutoff=CUTOFF.get(kb))
        out[f"codec{kb}"] = e["y"][: len(master)]
        kbps[kb] = {"kbps": float(e["kbps"]), "cutoff": float(e["cutoff"]), "nmr_db": float(e["nmr_db"])}
    return perf, gains, out, {"played_in_room": played_in_room, "kbps": kbps}


def melody_score(pitches, beats_, base: int = 72):
    t, score = 0.0, []
    for p, b in zip(pitches, beats_):
        score.append((base + int(p), t, t + b * 0.5 * 0.95))
        t += b * 0.5
    return score


def tune_beats():
    return [float(b) for _, b in T.TUNE]


def calibration_tunes():
    """Not the Tune: four of Part 14's other melodies (Frère Jacques, Mary Had a Little Lamb, London Bridge, Ode to
    Joy), at the same tempo and register, for choosing the transcriber's settings, so that the Tune is a fair test."""
    from explainer.music.monochord import melody as ML
    return [(m.name, melody_score(m.pitches, m.beats), [float(b) for b in m.beats]) for m in ML.corpus()[1:5]]


_S: dict = {}


def chain_data():
    """The Tune down the chain (computed once, then kept in ``.cache/music68/stages.npz``)."""
    if "s" in _S:
        return _S["s"]
    path = CACHE.dir / "stages.npz"
    score, beats = tune_score()
    if path.exists():
        z = np.load(path, allow_pickle=True)
        out = {k: z[k] for k in STAGES}
        extra = {"played_in_room": z["played_in_room"], "kbps": z["kbps"].item()}
        perf, gains = [tuple(r) for r in z["perf"].tolist()], z["gains"].tolist()
    else:
        perf, gains, out, extra = run_chain(score, 68)
        path.parent.mkdir(parents=True, exist_ok=True)
        np.savez(path, perf=np.array(perf), gains=np.array(gains), played_in_room=extra["played_in_room"], kbps=np.array(extra["kbps"], dtype=object), **out)
    perf = [(int(m), float(a), float(b)) for m, a, b in perf]
    _S["s"] = (score, perf, beats, gains, out, extra)
    return _S["s"]


# ---------------------------------------------------------------------------------------------- items
NAMES = {"score": "as written", "played": "performed", "room": "in a room", "mic": "through a microphone", "master": "mastered",
         "codec128": "128 kbit/s", "codec64": "64 kbit/s", "codec32": "32 kbit/s", "codec16": "16 kbit/s"}


def compute_hook() -> dict:
    c = variation_clip(1)
    v = json.load(open(REPO_ROOT / ".cache" / "music1" / "variation.json"))
    return {"title": v.get("title", ""), "seconds": c.duration, "measure": v.get("measure", ""),
            "clips": {"one": save("hook.one", c, kind=c.meta.get("label", "physical model"), level=None, ceiling=float("inf"), detail="Variation 1, as Part 1 made it: the Tune on one simulated string, its bridge moved for each note")}}


def compute_chain() -> dict:
    """The Tune down the chain, heard at five stages; and each stage measured by what it changes."""
    score, perf, beats, gains, st, ex = chain_data()
    m = {"timing_ms": RT.timing_rms_ms(perf, score, 0.5), "gain_range_db": float(max(gains) - min(gains)),
         "reverb_db": RT.late_to_early_db(st["room"], ex["played_in_room"]),
         "snr_db": float(20 * np.log10(np.sqrt(np.mean(st["room"] ** 2)) / 10 ** (-50 / 20))),
         "crest_before": RT.crest_db(st["mic"]), "crest_after": RT.crest_db(st["master"]), "codec": ex["kbps"],
         "seconds": {k: len(v) / SR for k, v in st.items()}}
    names = ["score", "played", "room", "master", "codec16"]
    n = int(10.0 * SR)
    c = concat([C(st[k][:n]) for k in names], gap=0.8, names=names)
    low = C(st["codec16"][: int(14.5 * SR)])
    return {**m, "names": names, "starts": {k: float(c.events[k]) for k in names},
            "clips": {"five": save("chain.five", c, detail="the Tune's opening at five stages of the chain on Part 38's piano: as written, performed, in a room, mastered, and through Part 58's coder at 16 kbit/s"),
                      "low": save("chain.low", low, detail="the Tune's first two phrases after the whole chain, ending in Part 58's coder at 16 kbit/s")}}


def compute_pictures() -> dict:
    """Log-frequency spectrograms (dB) of the Tune's first eight seconds at four stages, for the film."""
    score, perf, beats, gains, st, ex = chain_data()
    out = {}
    for k in ("played", "room", "master", "codec16"):
        L = TR.logfreq(st[k][: int(8 * SR)], SR, fmin_midi=48, fmax_midi=120, per_semitone=1, n_fft=4096, hop=1920)
        D = 20 * np.log10(L["S"] + 1e-9)
        out[k] = np.round(D - D.max(), 1).tolist()
    return {"stages": out, "lo_midi": 48, "hi_midi": 120, "seconds": 8.0}


def compute_wide() -> dict:
    """The coder at 16 kbit/s with its fallback band (18 kHz) beside the chain's (5.5 kHz): band levels, what the
    transcriber recovers, and both heard."""
    score, perf, beats, gains, st, ex = chain_data()
    e = K.encode(st["master"], 16)
    wide = e["y"][: len(st["master"])]
    bands = [(0, 300), (300, 700), (700, 1500), (1500, 3000), (3000, 6000), (6000, 12000)]

    def levels(y):
        P = np.abs(np.fft.rfft(y)) ** 2
        f = np.fft.rfftfreq(len(y), 1 / SR)
        ref = np.abs(np.fft.rfft(st["master"])) ** 2
        return [float(10 * np.log10((P[(f >= a) & (f < b)].sum() + 1e-12) / (ref[(f >= a) & (f < b)].sum() + 1e-12))) for a, b in bands]

    est = RT.monophonic_notes(wide, **settings())
    want = [int(m) for m, _, _ in score]
    n = int(9.0 * SR)
    c = concat([C(st["codec16"][:n]), C(wide[:n])], gap=0.8, names=["cut", "wide"])
    return {"bands": bands, "cut": levels(st["codec16"]), "wide": levels(wide), "wide_kbps": float(e["kbps"]), "wide_nmr": float(e["nmr_db"]),
            "wide_pitch_errors": RT.edit_distance([m for m, _, _ in est], want), "starts": {k: float(c.events[k]) for k in ("cut", "wide")},
            "clips": {"two": save("coder.two", c, detail="the Tune's opening after the chain, through Part 58's coder at 16 kbit/s: with its band cut to 5.5 kHz, then with the full band it falls back to")}}


def calibrate() -> dict:
    """The transcriber's settings, chosen on four other melodies sent down the same chain (seeds 101 to 104): the
    setting with the fewest wrong keys (edit distance per note), averaged over every stage and melody.  Both ways of
    reading a note's pitch are in the grid: YIN over the note, and the harmonics that gained energy at its onset."""
    grid = [(mth, d, c, r, g) for mth in ("yin", "onset") for d in (0.07, 0.12, 0.2) for c in (10.0, 1000.0) for r in (0.0, 1.0)
            for g in (1, 3)]
    chains = []
    for i, (name, score, beats) in enumerate(calibration_tunes()):
        perf, gains, out, _ = run_chain(score, 101 + i)
        chains.append((name, score, out, {k: RT.analyse(y) for k, y in out.items()}))
    table = {}
    for mth, d, c, r, g in grid:
        per = {k: 0.0 for k in STAGES}
        for name, score, out, an in chains:
            want = [n[0] for n in score]
            for k, y in out.items():
                est = RT.monophonic_notes(y, delta=d, compress=c, rise_db=r, method=mth, analysis=an[k], lag=g)
                per[k] += RT.edit_distance([n[0] for n in est], want) / len(want) / len(chains)
        table[f"{mth}/{d}/{c:g}/{r:g}/{g}"] = per
    mean = {k: float(np.mean(list(v.values()))) for k, v in table.items()}
    best = min(mean, key=mean.get)
    best_yin = min((k for k in mean if k.startswith("yin/")), key=mean.get)
    best_flux = min((k for k in mean if k.startswith("onset/") and k.endswith("/1")), key=mean.get)
    mth, d, c, r, g = best.split("/")
    return {"tunes": [n for n, _, _ in calibration_tunes()], "table": table, "mean": mean, "best": best, "best_yin": best_yin,
            "best_flux": best_flux, "notes": int(sum(len(sc) for _, sc, _ in calibration_tunes())),
            "settings": {"method": mth, "delta": float(d), "compress": float(c), "rise_db": float(r), "lag": int(g)}}


def settings() -> dict:
    return load("calibrate")["settings"]


def compute_calibrate() -> dict:
    return calibrate()


def compute_roundtrip() -> dict:
    """Back up the chain.  The line transcriber (onsets and YIN, Part 61; settings from ``calibrate``) and, for
    comparison, Part 61's network read each stage; the line is quantized with a drifting tempo (Part 61) and scored
    against what was written: notes found (pitch, and onset within 50 ms of the performance), and edit distances of the
    keys alone and of (key, note value) pairs."""
    from videos.music.music61 import compute as P61
    from explainer.music.monochord import key as KY
    score, perf, beats, gains, st, ex = chain_data()
    want_k = [int(m) for m, _, _ in score]
    rows = {}
    for k in STAGES:
        y = st[k]
        est = RT.monophonic_notes(y, **settings())
        net, _, _ = P61.net_notes(y)
        ref = score if k == "score" else perf
        sc, scn = TR.note_scores(ref, est), TR.note_scores(ref, net)
        b = RT.back_to_score(est)
        e = RT.score_errors(b["keys"], b["values"], want_k, beats)
        dist = KY.distribution(b["keys"], b["values"]) if b["keys"] else np.ones(12) / 12
        on = np.array([n[1] for n in est])
        found = [bool(len(on)) and float(np.min(np.abs(on - ref[i][1]))) < 0.08 for i in range(len(ref))]
        rep = [i for i in range(1, len(score)) if score[i][0] == score[i - 1][0]]          # re-strikes of the same key
        moves = [i for i in range(len(score)) if i not in rep]
        extra = int(sum(1 for o in on if np.min(np.abs(np.array([x[1] for x in ref]) - o)) > 0.08))
        rows[k] = {"note_f": float(sc["f"]), "net_f": float(scn["f"]), "notes": len(est), "pitch_errors": e["pitch"], "score_errors": e["score"],
                   "key": KY.key_name(KY.ranking(dist)[0][0]), "key_by_count": KY.key_name(KY.ranking(KY.distribution(b["keys"]))[0][0]) if b["keys"] else "",
                   "bpm": b["bpm"], "keys": b["keys"], "values": b["values"], "onsets": [float(x) for x in on],
                   "restrikes_found": int(sum(found[i] for i in rep)), "restrikes": len(rep),
                   "moves_found": int(sum(found[i] for i in moves)), "moves": len(moves), "extra": extra}
    return {"rows": rows, "n": len(score), "want_keys": want_k, "want_values": beats, "settings": settings()}


def replay(keys, values, beat: float = 0.5):
    """A recovered score played strictly on Part 38's piano."""
    from videos.music.music61 import compute as P61
    t, notes = 0.0, []
    for m, v in zip(keys, values):
        if 48 <= m <= 84:
            notes.append((int(m), t, t + v * beat * 0.95))
        t += v * beat
    return P61.render(notes, "piano", t + 1.2)


def compute_back() -> dict:
    """An ear question: the score recovered from three stages (mastered, 32 and 16 kbit/s), replayed strictly, in a
    shuffled order: which came back from where?"""
    r = load("roundtrip")["rows"]
    order = ["codec32", "master", "codec16"]               # shuffled once, by hand, and kept: the answer is said aloud
    n = 14
    segs = [C(replay(r[k]["keys"][:n], r[k]["values"][:n])) for k in order]
    c = concat(segs, gap=1.0, names=["A", "B", "C"])
    return {"order": order, "starts": {k: float(c.events[k]) for k in "ABC"}, "errors": {k: r[k]["pitch_errors"] for k in order},
            "clips": {"three": save("back.three", c, detail="the scores a machine wrote down from three stages of the chain, replayed strictly on Part 38's piano: from the master, and from Part 58's coder at 32 and 16 kbit/s, in a shuffled order")}}


def compute_identify() -> dict:
    """Does each stage still sound like itself?  Part 63's fingerprinter, indexed on the 67 Variations and the Tune as
    performed, is queried with six seconds from each stage; Part 62's tempo estimate; the key of the recovered score."""
    from explainer.music.monochord.mir import rhythm as RH
    score, perf, beats, gains, st, ex = chain_data()
    idx = F.Index()
    for n in range(1, 68):
        c = variation_clip(n)
        idx.add(f"Variation {n}", mono(c), c.sr)
    idx.add("the Tune, performed", st["played"], SR)
    rows = {}
    r = load("roundtrip")["rows"]
    for k in STAGES:
        q = st[k][int(4.0 * SR): int(10.0 * SR)]
        top = idx.query(q, SR, top=2)
        nov = RH.novelty(st[k])
        tp = RH.tempo(nov["nov"] if "nov" in nov else nov["odf"], nov["hop_s"], prior_bpm=120.0)
        rows[k] = {"found": top[0]["track"], "votes": int(top[0]["votes"]), "runner_up": int(top[1]["votes"]) if len(top) > 1 else 0,
                   "bpm": float(tp["bpm"]), "key": r[k]["key"]}
    return {"rows": rows}


def compute_survive() -> dict:
    """What survives the chain and what it changes: pitch errors of the recovered line beside two measures of the
    sound itself, its brightness (spectral centroid) and its space (reverberant energy)."""
    score, perf, beats, gains, st, ex = chain_data()
    r = load("roundtrip")["rows"]

    def centroid(y):
        n = 4096
        fr = np.lib.stride_tricks.sliding_window_view(np.asarray(y, float), n)[:: n // 2]
        P = np.abs(np.fft.rfft(fr * np.hanning(n), axis=1)) ** 2
        f = np.fft.rfftfreq(n, 1 / SR)
        w = P.sum(axis=1)
        keep = w > 1e-4 * w.max()
        return float(np.sum((P[keep] * f).sum(axis=1)) / np.sum(w[keep]))

    def quiet(y):
        """The share of a spectrogram's cells within 40 dB of its loudest: low for a dry sound, high once a room and
        noise fill the gaps, low again when a coder drops what is quiet."""
        D = 20 * np.log10(TR.logfreq(y, SR, fmin_midi=36, fmax_midi=120, per_semitone=1, n_fft=4096, hop=960)["S"] + 1e-9)
        return float(np.mean(D > D.max() - 40))

    base = centroid(st["played"])
    rows = {k: {"pitch_errors": r[k]["pitch_errors"], "brightness": centroid(st[k]) / base, "filled": quiet(st[k]),
                "moves_found": r[k]["moves_found"], "restrikes_found": r[k]["restrikes_found"]} for k in STAGES}
    wet = st["room"] - ex["played_in_room"]
    room = C(np.r_[ex["played_in_room"][: int(9 * SR)], np.zeros(int(0.8 * SR)), wet[: int(9 * SR)] / (np.max(np.abs(wet)) + 1e-12) * np.max(np.abs(ex["played_in_room"]))])
    return {"rows": rows, "split": 9.8,
            "clips": {"room": save("survive.room", room, detail="the Tune's opening performed on Part 38's piano, then the room alone: what the room added, with the direct sound taken away")}}


def compute_pairs() -> dict:
    """The suite's largest and smallest steps as built, heard as pairs of excerpts."""
    o = load("order")
    big, small = o["far_after"][0], o["close_after"][0]
    seg = lambda n: faded(excerpt(variation_clip(n), 5.0))
    c = concat([seg(big), seg(big + 1), seg(small), seg(small + 1)], gap=0.5, names=["a1", "a2", "b1", "b2"])
    return {"big": big, "small": small, "starts": {k: float(c.events[k]) for k in ("a1", "a2", "b1", "b2")},
            "clips": {"two": save("order.pairs", c, kind="synthesized", detail=f"five seconds each of Variations {big} and {big + 1}, then of {small} and {small + 1}, as their parts made them (physical models and synthesis)")}}


def compute_nearest() -> dict:
    """The first eight steps of the nearest-neighbour order, four seconds each."""
    o = load("order")
    first = o["nearest_order"][:8]
    c = concat([faded(excerpt(variation_clip(n), 4.0)) for n in first], gap=0.35, names=[f"v{n}" for n in first])
    return {"parts": first, "starts": {str(n): float(c.events[f"v{n}"]) for n in first},
            "clips": {"eight": save("order.nearest", c, kind="synthesized", detail="four seconds each of eight Variations in the order a nearest-neighbour rule picks: " + ", ".join(map(str, first)))}}


def compute_fifths() -> dict:
    """Part 1's question once more: a fifth on the simulated string at 3:2, then mistuned by 1 % (Part 5's beats)."""
    from explainer.music.monochord.partkit import string_note
    from explainer.music.monochord import mix
    lo = string_note(1.0, 3.0)
    pure = string_note(2 / 3, 3.0)
    off = string_note(2 / 3 / 1.01, 3.0)
    a = mix([(lo, 0.0), (pure, 0.0)])
    b = mix([(lo, 0.0), (off, 0.0)])
    c = concat([a, b], gap=0.8, names=["pure", "off"])
    from explainer.music.monochord.instruments.plucked import C3
    stars = json.load(open(REPO_ROOT / ".cache" / "music67" / "stars.json"))
    return {"starts": {k: float(c.events[k]) for k in ("pure", "off")}, "f0": float(C3),
            "beat_hz": float(3 * C3 - 2 * 1.5 * C3 / 1.01), "open_problems": int(stars["count"]),
            "clips": {"two": save("unknown.fifths", c, detail="Part 1's simulated string with its bridge at 2/3 of its length, sounding with the open string: a fifth at 3:2, then with the bridge moved 1 %")}}


def compute_order() -> dict:
    """Three orders for the suite, by how far apart neighbours sound (Part 63's embedding, standardized)."""
    E = F.standardize(np.array([F.embed(excerpt(variation_clip(n)), SR) for n in range(1, 68)]))
    built = list(range(67))
    near = RT.nearest_order(E, 0)
    rng = np.random.default_rng(68)
    rand = np.array([RT.path_length(E, [0] + list(rng.permutation(np.arange(1, 67)))) for _ in range(2000)])
    step = np.linalg.norm(np.diff(E[built], axis=0), axis=1)
    L = RT.path_length(E, built)
    return {"built": L, "nearest": RT.path_length(E, near), "random_mean": float(rand.mean()),
            "random_lo": float(np.quantile(rand, 0.025)), "random_hi": float(np.quantile(rand, 0.975)),
            "random_hist": np.histogram(rand, bins=30)[0].tolist(), "random_edges": np.histogram(rand, bins=30)[1].tolist(),
            "built_below_random": float(np.mean(rand <= L)), "steps": step.tolist(),
            "far_after": [int(i) + 1 for i in np.argsort(-step)[:3]], "close_after": [int(i) + 1 for i in np.argsort(step)[:3]],
            "nearest_order": [int(i) + 1 for i in near], "xy": RT.mds2(E).tolist()}


def compute_suite() -> dict:
    """An excerpt of every Variation, in the order they were made, in three movements: Acts I to III, IV to VII, VIII
    to XII."""
    moves = {"one": range(1, 23), "two": range(23, 45), "three": range(45, 68)}
    out, clips = {}, {}
    for name, parts in moves.items():
        vc = [variation_clip(n) for n in parts]
        kind = "physical model" if all(c.meta.get("label") == "physical model" for c in vc) else "synthesized"
        segs = [faded(excerpt(c)) for c in vc]
        c = concat(segs, gap=0.6, names=[f"v{n}" for n in parts])
        out[name] = {"parts": list(parts), "starts": {str(n): float(c.events[f"v{n}"]) for n in parts}, "seconds": c.duration,
                     "kinds": {str(n): v.meta.get("label") for n, v in zip(parts, vc)}}
        clips[name] = save(f"suite.{name}", c, kind=kind, detail=f"the suite, movement {name}: {EXCERPT:g} s of each of Variations {parts[0]} to {parts[-1]}, as each part made it (physical models and synthesis), in the order they were made")
    titles = {r["part"]: r["title"] for r in LEDGER}
    return {"moves": out, "titles": {str(k): v for k, v in titles.items()}, "excerpt": EXCERPT, "clips": clips}


LAYERS = {
    "the physics": ("physics", "instruments", "ear", "consonance", "tuning"),
    "the theory": ("pitch", "scales", "chords", "key", "melody", "rhythm", "counterpoint", "fourpart", "progression", "chromatic",
                   "canon", "form", "grammar", "neoriemann", "geometry", "mathmusic", "atonal", "score"),
    "the styles": ("medieval", "trecento", "renaissance", "palestrina", "baroque", "classical", "romantic", "modern", "soundmass",
                   "raga", "maqam", "bronze", "timelines", "blues", "changes", "song"),
    "the craft and the mind": ("orchestra", "composer", "perform", "screen", "scene", "listener", "origins"),
    "the electronics": ("digital", "dsp", "effects", "dynamics", "synth", "synth2", "daw"),
    "the studio": ("transducer", "space", "studio", "master", "loudness", "codec", "live", "business"),
    "the listeners and makers": ("mir", "machines", "genaudio", "research", "roundtrip"),
}


def compute_built() -> dict:
    """Monochord and the series counted from the repository."""
    root = REPO_ROOT
    mods = [p for p in glob.glob(str(root / "explainer" / "music" / "monochord" / "**" / "*.py"), recursive=True) if "__pycache__" not in p]
    lines = sum(sum(1 for _ in open(p)) for p in mods)
    tests = glob.glob(str(root / "tests" / "music" / "test_*.py"))
    n_tests = sum(open(p).read().count("\ndef test_") for p in tests)
    clips, secs = 0, 0.0
    for n in range(1, 68):
        for j in glob.glob(str(root / ".cache" / f"music{n}" / "audio" / "*.json")):
            m = json.load(open(j))
            secs += float(m.get("duration", 0.0) or 0.0)
            clips += 1
    labs_ = glob.glob(str(root / "videos" / "music" / "labs" / "lab[0-9]*.py"))
    scenes = sum(len(glob.glob(str(root / "videos" / "music" / f"music{n}" / "s[0-9][0-9]_*.py"))) for n in range(1, 68))
    groups = {}
    for p in mods:
        rel = os.path.relpath(p, root / "explainer" / "music" / "monochord")
        g = rel.split(os.sep)[0] if os.sep in rel else "core"
        groups[g] = groups.get(g, 0) + 1
    layer_of = {m: name for name, ms in LAYERS.items() for m in ms}
    layers = {name: {"modules": 0, "lines": 0} for name in LAYERS}
    layers["the core"] = {"modules": 0, "lines": 0}
    for p in mods:
        rel = os.path.relpath(p, root / "explainer" / "music" / "monochord")
        top = rel.split(os.sep)[0].removesuffix(".py")
        name = layer_of.get(top, "the core")
        layers[name]["modules"] += 1
        layers[name]["lines"] += sum(1 for _ in open(p))
    return {"modules": len(mods), "lines": lines, "test_files": len(tests), "tests": n_tests, "clips": clips, "hours": secs / 3600,
            "labs": len(labs_), "scenes": scenes, "groups": groups, "layers": layers}


def compute_variation() -> dict:
    s = load("suite")
    r = load("roundtrip")["rows"]
    total = sum(m["seconds"] for m in s["moves"].values())
    return {"part": 68, "title": "the suite: every Variation, in the order they were made", "seconds": round(total, 1),
            "measure": f"the Tune down the whole chain and back: {r['score']['pitch_errors']} of 42 keys wrong as written, {r['master']['pitch_errors']} after the master, {r['codec16']['pitch_errors']} at 16 kbit/s",
            "clip": "suite.one"}


ITEMS = {"hook": compute_hook, "chain": compute_chain, "pictures": compute_pictures, "wide": compute_wide, "calibrate": compute_calibrate, "roundtrip": compute_roundtrip, "back": compute_back,
         "identify": compute_identify, "survive": compute_survive, "order": compute_order, "pairs": compute_pairs, "nearest": compute_nearest,
         "fifths": compute_fifths, "suite": compute_suite, "built": compute_built, "variation": compute_variation}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
