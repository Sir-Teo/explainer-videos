"""Precompute everything numerical, and every sound, in Part 61 of *Music, Built* ("Pitch, Onsets and Transcription").

    python -m videos.music.music61.compute              # everything missing (several minutes: the network trains)
    python -m videos.music.music61.compute --force hook

Numbers are cached in ``.cache/music61/<name>.json``, sounds in ``.cache/music61/audio/``.  The tools are Monochord's
first listeners (``explainer/music/monochord/mir/``).  Every piece is rendered by Monochord, so every answer key is
exact: Part 38's piano for training, and three timbres the transcribers never hear while learning (a plucked harp by
Karplus and Strong, an organ, Part 9's bowed strings).

Items:
    data        training and test pieces: random polyphony on a grid, rendered on four instruments
    pitch       YIN and autocorrelation on Part 8's voice against noise; a tone without its fundamental
    chords      salience and NMF on C-E-G and C-E-G-C (an ear question: the same chord?)
    onsets      spectral flux on piano and on bowed strings
    nmf         note templates from isolated piano notes; NMF transcription of every test piece
    net         a small network trained on piano renders; its transcriptions of every test piece
    timbres     one test piece on four instruments
    hook        an ear question: the Tune with chords on the piano, and the network's transcription of it, re-played
    score       a performance with rubato, quantized to a score, and re-played
    tune61      Variation 61: the Tune performed, transcribed and re-rendered, five times round
    variation   the Variations ledger, row 61
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import tune as T
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.mir import neural as NN
from explainer.music.monochord.mir import transcribe as TR
from explainer.music.monochord.partkit import organ_tone, saver
from videos.music.music38 import compute as P38
from videos.music.music56 import compute as P56

CACHE = Cache("music61")
CLIPS = ClipStore("music61")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
MAJOR = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
LO, HI = 48, 84                                  # the transcribers' range: C3 to C6
PITCHES = list(range(LO, HI + 1))
HOP = 960                                        # 20 ms frames
DURS = (0.25, 0.5, 1.0)
INSTRUMENTS = ("piano", "harp", "organ", "strings")


def C(y) -> Clip:
    return Clip(np.asarray(y, float), SR)


def fade(y, a=0.005, r=0.08):
    y = np.array(y, float)
    ka, kr = max(int(a * SR), 1), max(int(r * SR), 1)
    y[:ka] *= np.linspace(0, 1, ka)
    y[len(y) - kr:] *= np.linspace(1, 0, kr)
    return y


_N: dict = {}


def note(inst, m, dur):
    """One note, cached: ``dur`` seconds of sounding, then a short release."""
    key = (inst, int(m), round(dur, 2))
    if key in _N:
        return _N[key]
    hz = float(TR.midi_hz(m))
    if inst == "piano":
        y = np.asarray(P38.piano(int(m), dur, 0.9), float)
    elif inst == "harp":
        y = STR.karplus_strong(hz, dur + 0.25, seed=int(m))
        y = y * np.r_[np.ones(int(dur * SR)), np.linspace(1, 0, len(y) - int(dur * SR))]
    elif inst == "organ":
        y = organ_tone(hz, dur, partials=6, rolloff=0.7)
        k = int(0.02 * SR)
        y[:k] *= np.linspace(0, 1, k)
        y[-k:] *= np.linspace(1, 0, k)
    elif inst == "strings":
        y = STR.bowed_note(hz, dur)
    else:
        raise ValueError(inst)
    y = np.asarray(y, float)
    y = y / (np.sqrt(np.mean(y[: max(1, int(min(dur, 0.3) * SR))] ** 2)) + 1e-12) * 0.1
    _N[key] = y
    return y


def render(notes, inst, seconds=None, gains=None):
    """[(midi, onset, offset)] on an instrument (durations snapped to the cached lengths)."""
    placed = []
    for i, (m, a, b) in enumerate(notes):
        d = min(DURS, key=lambda z: abs(z - (b - a)))
        placed.append((C(note(inst, m, d)), a, 0.0 if gains is None else gains[i]))
    end = seconds if seconds is not None else max(a + 1.3 for _, a, _ in notes)
    y = mix(placed, duration=end).y
    return y / (np.max(np.abs(y)) + 1e-12) * 0.9


def random_piece(seed, seconds=6.0, grid=0.125, rate=3.0, max_voices=4):
    """Random polyphony: onsets on a grid, at ``rate`` notes a second, pitches in range (no two the same at once),
    durations from DURS, at most ``max_voices`` sounding."""
    rng = np.random.default_rng(seed)
    notes = []
    t = 0.0
    while t < seconds - 1.0:
        k = rng.poisson(rate * grid)
        for _ in range(k):
            d = float(rng.choice(DURS))
            sounding = [n for n in notes if n[1] <= t < n[2]]
            if len(sounding) >= max_voices:
                break
            busy = {n[0] for n in sounding}
            m = int(rng.integers(LO, HI + 1))
            if m in busy:
                continue
            notes.append((m, round(t, 3), round(t + d, 3)))
        t += grid
    return sorted(notes, key=lambda z: (z[1], z[0]))


def spec(y):
    return TR.logfreq(y, SR, hop=HOP)


def gains_for(notes, seed):
    return list(np.random.default_rng(seed + 99).uniform(-6, 0, len(notes)))


_D: dict = {}


def dataset():
    if "d" in _D:
        return _D["d"]
    train = [random_piece(s) for s in range(160)]
    test = [random_piece(10_000 + s) for s in range(12)]
    _D["d"] = (train, test)
    return _D["d"]


def tune_notes(phrases=(0, 1), beat=0.5, base=60):
    """The Tune with its chords (the session's harmony): melody and two chord tones every two beats."""
    out = []
    for m, t, d in P56.tune_notes(phrases, base=base + 12, beat=beat):
        if LO <= m <= HI:
            out.append((m, t, t + d))
    syms = "".join(P56.CHORDS[p] for p in phrases)
    for i, sym in enumerate(syms):
        t0 = 2 * i * beat
        r = P56.ROOT[sym]
        for m in (48 + r, 52 + (r + 4 - 52) % 12):                 # the root, and the third above it
            out.append((m, t0, t0 + 2 * beat * 0.95))
    return sorted(out, key=lambda z: (z[1], z[0]))


# ---------------------------------------------------------------------------------------------- the transcribers
_M: dict = {}


def templates():
    if "W" not in _M:
        sp = {}
        for m in PITCHES:
            S = spec(note("piano", m, 1.0))["S"]
            sp[m] = S[:, 1:int(0.8 / (HOP / SR))]
        _M["W"], _M["keys"] = TR.note_templates(sp)
    return _M["W"], _M["keys"]


def nmf_notes(y, on=0.12):
    W, keys = templates()
    S = spec(y)
    r = TR.nmf(S["S"], W=W, fix_W=True, iters=120, sparsity=0.0)
    H = r["H"]
    return TR.activations_to_notes(H, keys, S["hop_s"], on=on, rel=True, min_dur=0.06), H, S


def network():
    """The network, trained once and kept in the cache (``net.pt``), so that later items need not train it again."""
    if "net" in _M:
        return _M["net"]
    import torch
    path = CACHE.dir / "net.pt" if hasattr(CACHE, "dir") else None
    if path is not None and path.exists():
        saved = torch.load(path, weights_only=False)
        _M["net"] = saved["fit"]
        _M["net_frames"] = saved["frames"]
        return _M["net"]
    train, _ = dataset()
    Xs, Ys = [], []
    for s, nt in enumerate(train):
        y = render(nt, "piano", 6.0, gains_for(nt, s))
        S = spec(y)
        Xs.append(NN.features(S["S"]))
        Ys.append(TR.roll(nt, PITCHES, S["hop_s"], S["S"].shape[1]).T)
    X, Y = np.concatenate(Xs), np.concatenate(Ys)
    fit = NN.train(X, Y, hidden=256, epochs=25, seed=0)
    _M["net"] = fit
    _M["net_frames"] = len(X)
    if path is not None:
        path.parent.mkdir(parents=True, exist_ok=True)
        torch.save({"fit": fit, "frames": len(X)}, path)
    return fit


def net_notes(y, on=0.5):
    fit = network()
    S = spec(y)
    P = NN.predict(fit, NN.features(S["S"]))
    return TR.activations_to_notes(P, PITCHES, S["hop_s"], on=on, off=0.3, min_dur=0.06), P, S


# ---------------------------------------------------------------------------------------------- items
def compute_data() -> dict:
    train, test = dataset()
    return {"train_pieces": len(train), "train_notes": sum(len(n) for n in train), "test_pieces": len(test),
            "test_notes": sum(len(n) for n in test), "example": test[0], "range": [LO, HI], "hop_s": HOP / SR}


def compute_pitch() -> dict:
    ev = T.events(0.5, [0, 1])
    notes = [(57 + MAJOR[e["degree"]], e["t"], e["dur"]) for e in ev]
    v = CH.sing(notes, "soprano", "a", seed=1)
    v = v / np.max(np.abs(v))

    def truth(times):
        out = np.full(len(times), np.nan)
        for m, t0, d in notes:
            k = (times >= t0 + 0.08) & (times < t0 + d - 0.08)
            out[k] = TR.midi_hz(m)
        return out
    snrs = [30, 20, 10, 5, 0, -5, -10]
    rows = []
    tracks = {}
    rng = np.random.default_rng(0)
    noise = rng.standard_normal(len(v))
    for snr in snrs:
        y = v + noise * np.std(v) * 10 ** (-snr / 20)
        a, b = TR.yin(y, SR, fmin=80, fmax=1000), TR.acf_f0(y, SR, fmin=80, fmax=1000)
        ta, tb = truth(a["t"]), truth(b["t"])
        ok_a, ok_b = np.isfinite(ta), np.isfinite(tb)
        fine_a = float(np.median(np.abs(1200 * np.log2(a["f0"][ok_a] / ta[ok_a]))))
        fine_b = float(np.median(np.abs(1200 * np.log2(b["f0"][ok_b] / tb[ok_b]))))
        rows.append({"snr": snr, "yin": TR.gross_error(a["f0"], ta), "acf": TR.gross_error(b["f0"], tb), "yin_cents": fine_a, "acf_cents": fine_b})
        if snr in (20, 0, -10):
            tracks[str(snr)] = {"t": a["t"].tolist(), "f0": a["f0"].tolist(), "truth": ta.tolist(), "acf": b["f0"].tolist(), "acf_t": b["t"].tolist()}
    segs = [C(fade(v + noise * np.std(v) * 10 ** (-s / 20))) for s in (20, 0, -10)]
    c = concat(segs, gap=0.8, names=["s20", "s0", "sm10"])
    # a tone without its fundamental: partials 2..8 of 220 Hz
    t = np.arange(int(1.6 * SR)) / SR
    mf = sum(np.sin(2 * np.pi * 220 * k * t) / k for k in range(2, 9))
    mf *= np.minimum(1, t / 0.02) * np.minimum(1, (t[-1] - t) / 0.1)
    y_mf = TR.yin(mf, SR)
    # a steady tone: the bias of the plain autocorrelation
    st = np.sin(2 * np.pi * 220.3 * t) + 0.5 * np.sin(2 * np.pi * 440.6 * t)
    bias_yin = float(1200 * np.log2(np.median(TR.yin(st, SR)["f0"]) / 220.3))
    bias_acf = float(1200 * np.log2(np.median(TR.acf_f0(st, SR)["f0"]) / 220.3))
    cm = C(mf / np.max(np.abs(mf)) * 0.8)
    return {"rows": rows, "tracks": tracks, "missing_f0": float(np.median(y_mf["f0"][5:-5])), "bias_yin": bias_yin, "bias_acf": bias_acf,
            "starts": {"s20": float(c.events["s20"]), "s0": float(c.events["s0"]), "sm10": float(c.events["sm10"])},
            "clips": {"three": save("pitch.three", c, detail="Part 8's voice singing the Tune's first two phrases with white noise 20, 0 and -10 dB below it"),
                      "missing": save("pitch.missing", cm, kind="synthesized", detail="a tone of partials 2 to 8 of 220 Hz: no energy at 220 Hz itself")}}


def compute_chords() -> dict:
    a = [(60, 0.0, 1.6), (64, 0.0, 1.6), (67, 0.0, 1.6)]
    b = a + [(72, 0.0, 1.6)]
    ya = render(a, "piano", 2.2)
    yb = render(b, "piano", 2.2)
    out = {}
    for name, y, ref in (("triad", ya, a), ("octave", yb, b)):
        S = spec(y)
        k = slice(5, 40)
        cands = np.arange(LO, HI + 1)
        sal = TR.salience(S["S"][:, k], S["midi"], cands).mean(axis=1)
        est, H, _ = nmf_notes(y)
        est_n, _, _ = net_notes(y)
        out[name] = {"salience": (sal / sal.max()).tolist(), "nmf": sorted({n[0] for n in est}), "net": sorted({n[0] for n in est_n}),
                     "truth": [n[0] for n in ref], "nmf_level": (H.mean(axis=1) / H.mean(axis=1).max()).tolist()}
    c = concat([C(fade(ya)), C(fade(yb))], gap=1.0, names=["first", "second"])
    return {"cands": list(range(LO, HI + 1)), **out, "answer": "no",
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("chords.two", c, detail="Part 38's piano: C-E-G, then C-E-G with the C an octave above added")}}


def compute_onsets() -> dict:
    mel = [(60 + MAJOR[e["degree"]] + 12, e["t"], e["t"] + e["dur"] * 0.95) for e in T.events(0.45, [0, 1])]
    out = {}
    clips = []
    for inst in ("piano", "strings"):
        y = render(mel, inst, mel[-1][2] + 1.2)
        o = TR.onset_strength(y, SR)
        est = TR.pick_onsets(o["odf"], o["hop_s"])
        ref = sorted({round(n[1], 3) for n in mel})
        sc = TR.onset_scores(ref, est.tolist())
        sweep = []
        for delta in (0.01, 0.02, 0.04, 0.07, 0.1, 0.15, 0.2, 0.3, 0.4):
            e2 = TR.pick_onsets(o["odf"], o["hop_s"], delta=delta)
            z = TR.onset_scores(ref, e2.tolist())
            sweep.append({"delta": delta, "precision": z["precision"], "recall": z["recall"], "f": z["f"]})
        out[inst] = {"odf": o["odf"].tolist(), "t": o["t"].tolist(), "est": est.tolist(), "ref": ref, **sc, "sweep": sweep}
        clips.append(C(fade(y)))
    c = concat(clips, gap=1.0, names=["piano", "strings"])
    out["starts"] = {"piano": float(c.events["piano"]), "strings": float(c.events["strings"])}
    out["clips"] = {"two": save("onsets.two", c, detail="the Tune's first two phrases (repeated notes included) on Part 38's piano, then on Part 9's bowed strings")}
    return out


def compute_nmf() -> dict:
    W, keys = templates()
    _, test = dataset()
    res = {}
    for inst in INSTRUMENTS:
        f = []
        for s, nt in enumerate(test):
            y = render(nt, inst, 6.0, gains_for(nt, 500 + s))
            est, _, _ = nmf_notes(y)
            f.append(TR.note_scores(nt, est))
        res[inst] = {"f": float(np.mean([z["f"] for z in f])), "precision": float(np.mean([z["precision"] for z in f])),
                     "recall": float(np.mean([z["recall"] for z in f]))}
    nt = test[0]
    y = render(nt, "piano", 6.0, gains_for(nt, 500))
    est, H, S = nmf_notes(y)
    # NMF without templates: rank 12, learnt from the piece alone
    blind = TR.nmf(S["S"], rank=12, iters=200, seed=1)
    # each blind component: the pitch whose template it most resembles, and how much
    Wn = W / np.linalg.norm(W, axis=0, keepdims=True)
    Bn = blind["W"] / (np.linalg.norm(blind["W"], axis=0, keepdims=True) + 1e-12)
    sim = Bn.T @ Wn
    blind_match = [{"pitch": int(keys[int(np.argmax(r))]), "cos": float(np.max(r))} for r in sim]
    order = np.argsort([m["pitch"] for m in blind_match])
    c = C(fade(y))
    return {"scores": res, "templates": W[::2].tolist(), "keys": keys, "bins": S["midi"][::2].tolist(),
            "H": (H / H.max())[:, ::2].tolist(), "truth": nt, "est": est, "piece": nt,
            "cost": TR.nmf(S["S"], W=W, fix_W=True, iters=120)["cost"], "blind_cost": blind["cost"],
            "blind_W": (blind["W"][:, order][::2] / blind["W"].max()).tolist(), "blind_match": [blind_match[i] for i in order],
            "piece_pitches": sorted({int(n[0]) for n in nt}),
            "piece_scores": TR.note_scores(nt, est),
            "clips": {"piece": save("nmf.piece", c, detail="a test piece of random polyphony on Part 38's piano (never used to learn the templates)")}}


def compute_net() -> dict:
    fit = network()
    _, test = dataset()
    res = {}
    for inst in INSTRUMENTS:
        f, fr = [], []
        for s, nt in enumerate(test):
            y = render(nt, inst, 6.0, gains_for(nt, 500 + s))
            est, P, S = net_notes(y)
            f.append(TR.note_scores(nt, est))
            fr.append(TR.frame_scores(TR.roll(nt, PITCHES, S["hop_s"], P.shape[1]), P > 0.5))
        res[inst] = {"f": float(np.mean([z["f"] for z in f])), "precision": float(np.mean([z["precision"] for z in f])),
                     "recall": float(np.mean([z["recall"] for z in f])), "frame_f": float(np.mean([z["f"] for z in fr]))}
    nt0 = test[0]
    y0 = render(nt0, "piano", 6.0, gains_for(nt0, 500))
    est0, P0, _ = net_notes(y0)
    nt = test[1]
    y = render(nt, "organ", 6.0, gains_for(nt, 501))
    est, P, S = net_notes(y)
    re = render(est, "organ", 6.0) if est else np.zeros(int(6 * SR))
    c = concat([C(fade(y)), C(fade(re))], gap=1.0, names=["first", "second"])
    c0 = C(fade(y0))
    W1 = fit["model"][0].weight.detach().numpy()                     # 256 units x (5 frames x 217 bins)
    nb = W1.shape[1] // 5
    units = []
    for u in np.argsort(-np.linalg.norm(W1, axis=1))[:6]:
        w = W1[u].reshape(5, nb).T                                   # bins x frames
        units.append({"w": (w / np.abs(w).max()).tolist(), "peak_midi": float(36 + np.argmax(w[:, 2]) / 3)})
    return {"units": units, "scores": res, "losses": fit["losses"], "frames": _M["net_frames"], "P": P[:, ::1].tolist(), "truth": nt, "est": est,
            "piano_P": P0[:, ::2].tolist(), "piano_truth": nt0, "piano_scores": TR.note_scores(nt0, est0),
            "piece_scores": TR.note_scores(nt, est), "answer": "first",
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"piano": save("net.piano", c0, detail="the first test piece on Part 38's piano, as the network transcribes it"),
                      "two": save("net.two", c, kind="synthesized", detail="a test piece on the organ (a timbre the network never heard), then the network's transcription of it played back on the same organ")}}


def compute_timbres() -> dict:
    _, test = dataset()
    nt = test[2]
    segs = [C(fade(render(nt, inst, 6.0, gains_for(nt, 502))[: int(4.0 * SR)])) for inst in INSTRUMENTS]
    c = concat(segs, gap=0.6, names=list(INSTRUMENTS))
    return {"starts": {k: float(c.events[k]) for k in INSTRUMENTS},
            "clips": {"four": save("timbres.four", c, detail="one test piece's first four seconds on Part 38's piano, a Karplus-Strong harp, an organ and Part 9's bowed strings")}}


def compute_hook() -> dict:
    ref = tune_notes((0, 1))
    rng = np.random.default_rng(3)
    perf = [(m, a + float(rng.normal(0, 0.012)), b) for m, a, b in ref]
    y = render(perf, "piano", ref[-1][2] + 1.2)
    est, P, S = net_notes(y)
    re = render(est, "piano", ref[-1][2] + 1.2)
    sc = TR.note_scores(ref, est)
    c = concat([C(fade(re)), C(fade(y))], gap=1.0, names=["first", "second"])
    return {"ref": ref, "est": est, "scores": sc, "answer": "second",
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("hook.two", c, detail="the Tune with chords on Part 38's piano, and a small network's transcription of that performance, played back on the same piano; the transcription first")}}


def compute_score() -> dict:
    ev = T.events(0.5, [0, 1])
    rng = np.random.default_rng(5)
    t, perf, beats = 0.0, [], []
    for k, e in enumerate(ev):
        stretch = 1.0 + 0.12 * math.sin(2 * math.pi * k / len(ev)) + float(rng.normal(0, 0.03))
        d = e["dur"] * stretch * (1.25 if k in (6, 13) else 1.0)        # rubato, and a held phrase end
        perf.append((72 + MAJOR[e["degree"]], round(t, 3), round(t + d * 0.92, 3)))
        beats.append(e["dur"] / 0.5)
        t += d
    y = render(perf, "piano", t + 1.0)
    est, _, _ = net_notes(y)
    mel = sorted([n for n in est if n[0] >= 69], key=lambda z: z[1])
    q = TR.quantize(mel, divisions=2)
    on_q = q["beats"]
    re = []
    for (m, _, _), b, d in zip(mel, on_q, q["durations"]):
        re.append((m, b * 0.5, b * 0.5 + d * 0.5 * 0.92))
    yq = render(re, "piano", re[-1][2] + 1.0) if re else np.zeros(SR)
    true_on = np.r_[0, np.cumsum(beats)[:-1]].tolist()
    from explainer.music.monochord import key as K
    dist = K.distribution([n[0] for n in mel], q["durations"][:len(mel)])
    ranking = K.ranking(dist)[:3]
    c = concat([C(fade(y)), C(fade(yq))], gap=1.0, names=["performance", "score"])
    return {"key": [K.key_name(k) for k, _ in ranking], "key_r": [float(r) for _, r in ranking], "perf": perf, "est": mel, "beats": on_q, "durations": q["durations"], "bps": q["bps"], "true_beats": true_on,
            "true_durations": beats, "pitches_ok": [n[0] for n in mel] == [p[0] for p in perf],
            "starts": {"performance": float(c.events["performance"]), "score": float(c.events["score"])},
            "clips": {"two": save("score.two", c, detail="the Tune's first two phrases played with rubato on Part 38's piano, then the score quantized from its transcription, played strictly")}}


def compute_tune61() -> dict:
    ref = tune_notes((0, 1))
    cur = ref
    rounds, segs, names = [], [], []
    for k in range(6):
        y = render(cur, "piano", ref[-1][2] + 1.2)
        if k in (0, 1, 3, 5):
            segs.append(C(fade(y)))
            names.append(f"r{k}")
        est, _, _ = net_notes(y)
        rounds.append({"round": k, "notes": len(cur), "vs_original": TR.note_scores(ref, cur)["f"]})
        cur = [(m, a, b) for m, a, b in est]
    c = concat(segs, gap=0.8, names=names)
    return {"rounds": rounds, "names": names, "seconds": c.duration, "starts": {n: float(c.events[n]) for n in names},
            "clips": {"variation61": save("tune.variation61", c, detail="Variation 61: the Tune with chords on Part 38's piano; then after one, three and five rounds of transcription by a small network and re-rendering")}}


def compute_variation() -> dict:
    t = load("tune61")
    r = t["rounds"]
    return {"part": 61, "title": "performed, transcribed and re-rendered, five times round", "seconds": round(t["seconds"], 1),
            "measure": f"note F against the original: {r[1]['vs_original']:.2f} after one round, {r[5]['vs_original']:.2f} after five",
            "clip": "tune.variation61"}


ITEMS = {"data": compute_data, "pitch": compute_pitch, "chords": compute_chords, "onsets": compute_onsets, "nmf": compute_nmf,
         "net": compute_net, "timbres": compute_timbres, "hook": compute_hook, "score": compute_score, "tune61": compute_tune61,
         "variation": compute_variation}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
