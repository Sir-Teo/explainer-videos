"""Precompute everything numerical, and every sound, in Part 66 of *Music, Built* ("Generative Audio").

    python -m videos.music.music66.compute              # everything missing (some tens of minutes: five networks train)
    python -m videos.music.music66.compute --force hook

Numbers are cached in ``.cache/music66/<name>.json``, sounds in ``.cache/music66/audio/``, networks in
``.cache/music66/*.pt``.  The tools are Monochord's generators (``explainer/music/monochord/genaudio.py``); every
training sound was rendered by Monochord itself: Part 9's bowed string, Part 38's piano playing Part 65's chorale tunes,
Part 8's voice.  All generation runs at 16 kHz and is played back at the film's 48 kHz.

Items:
    corpus      the string corpus, the piano-chorale corpus (split by hymn tune, as in Part 65)
    rates       what raw audio asks of a model; mu-law against plain 8-bit, heard
    ar          a network that writes one sample at a time, trained on strings: bits per sample, and what it writes
    vocoder     a mel spectrogram turned back into sound by pseudo-inverse and Griffin-Lim
    codec       residual vector quantization of spectral frames: one, two and four tokens a frame
    tokenlm     the pocket transformer on codec tokens of the piano chorales: continuations, and copying
    diffusion   a diffusion model of a bowed string's harmonic profile: new tones drawn at three pitches
    ddsp        a DDSP string trained on the bowed-string model: resynthesis of a phrase it never heard
    fad         Fréchet distances in Part 63's embedding, generators against real strings
    watermark   a spread-spectrum mark under the music: detection, through a codec and a shift; an ear question
    hook        an ear question: the bowed-string model and the DDSP network's copy of it
    tune66      Variation 66: the Tune sung, re-rendered as a DDSP string, and a piano Tune continued by the token model
    variation   the Variations ledger, row 66
    zoom        a second of sound at three magnifications
    tokpic      a tune's codec tokens as a picture
    vibrato     the DDSP string driven by controls it never learnt from
    voices      one performance sung by three voices
    melbands    a phrase rebuilt from mel spectrograms of 16, 64 and 256 bands
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat
from explainer.music.monochord import codec as K
from explainer.music.monochord import genaudio as G
from explainer.music.monochord import machines as MC
from explainer.music.monochord import tune as T
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.mir import finder as F
from explainer.music.monochord.partkit import saver, signoff
from videos.music.music38 import compute as P38

CACHE = Cache("music66")
CLIPS = ClipStore("music66")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="synthesized")
MAJOR = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
SIX = 0.125                                           # seconds to a sixteenth in the piano corpus (a quarter is 0.5 s)


def C(y16) -> Clip:
    """A 16 kHz signal as a film clip at 48 kHz, faded and normalized."""
    y = G.to48(np.asarray(y16, float))
    k = int(0.005 * SR)
    y[:k] *= np.linspace(0, 1, k)
    r = int(0.08 * SR)
    y[-r:] *= np.linspace(1, 0, r)
    return Clip(y / (np.max(np.abs(y)) + 1e-12) * 0.9, SR)


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


_D: dict = {}


# ---------------------------------------------------------------------------------------------- corpora
def strings_corpus():
    """Bowed-string notes for training (random pitches G3 to A5, lengths and bow pressures) and two phrases held out."""
    if "str" in _D:
        return _D["str"]
    rng = np.random.default_rng(66)
    parts = []
    for _ in range(70):
        m = 55 + int(rng.integers(0, 27))
        d = float(rng.choice([0.35, 0.5, 0.8, 1.2]))
        z = STR.bowed_note(hz(m), d) * float(rng.uniform(0.35, 1.0))
        parts.append(z)
    train = np.concatenate(parts)
    train = G.to16(train / np.max(np.abs(train)) * 0.8)
    ev = T.events(0.5, [0, 1])
    test = np.concatenate([STR.bowed_note(hz(62 + MAJOR[e["degree"]]), e["dur"]) for e in ev])
    test = G.to16(test / np.max(np.abs(test)) * 0.8)
    _D["str"] = (train, test)
    return _D["str"]


def piano_tune(notes) -> np.ndarray:
    """A chorale tune on Part 38's piano at 16 kHz, a quarter note to half a second."""
    t, placed = 0.0, []
    for p, d, f in notes:
        placed.append((P38.arr(P38.piano(p - 12, d * SIX * (1.6 if f else 0.95), 0.8)), t, 0.0))
        t += d * SIX + (0.25 if f else 0.0)
    from explainer.music.monochord import mix
    y = mix(placed, duration=t + 1.0).y
    return G.to16(y / (np.max(np.abs(y)) + 1e-12) * 0.8)


def piano_corpus():
    """Part 65's chorale tunes, each played once on the piano: training tunes (one per hymn tune) and test tunes."""
    if "pno" in _D:
        return _D["pno"]
    ts = MC.tunes()
    train, test = MC.split(ts, 0.2, seed=0)
    seen, tr1 = set(), []
    for t in train:
        if t["group"] not in seen:
            seen.add(t["group"])
            tr1.append(t)
    _D["pno"] = ([(t["name"], piano_tune(t["notes"])) for t in tr1], [(t["name"], piano_tune(t["notes"])) for t in test])
    return _D["pno"]


def rvq():
    if "rvq" in _D:
        return _D["rvq"]
    import pickle
    path = CACHE.dir / "rvq.pkl"
    if path.exists():
        _D["rvq"] = pickle.load(open(path, "rb"))
        return _D["rvq"]
    train, _ = piano_corpus()
    Fr = np.concatenate([G.frames(y) for _, y in train])
    rng = np.random.default_rng(0)
    q = G.RVQ(4, 256, seed=0).fit(Fr[rng.choice(len(Fr), min(len(Fr), 12000), replace=False)])
    path.parent.mkdir(parents=True, exist_ok=True)
    pickle.dump(q, open(path, "wb"))
    _D["rvq"] = q
    return q


def ddsp():
    if "ddsp" in _D:
        return _D["ddsp"]
    import torch
    path = CACHE.dir / "ddsp.pt"
    if path.exists():
        _D["ddsp"] = torch.load(path, weights_only=False)
        return _D["ddsp"]
    train, _ = strings_corpus()
    fit = G.train_ddsp(train, steps=500)
    torch.save(fit, path)
    _D["ddsp"] = fit
    return fit


def embed_chunks(y, sec: float = 1.0) -> np.ndarray:
    n = int(sec * G.SR16)
    return np.array([F.embed(y[i:i + n], G.SR16) for i in range(0, len(y) - n + 1, n // 2)])


# ---------------------------------------------------------------------------------------------- items
def compute_corpus() -> dict:
    s_train, s_test = strings_corpus()
    p_train, p_test = piano_corpus()
    return {"string_seconds": len(s_train) / G.SR16, "string_test_seconds": len(s_test) / G.SR16,
            "piano_tunes": len(p_train), "piano_test": len(p_test), "piano_seconds": sum(len(y) for _, y in p_train) / G.SR16}


def compute_rates() -> dict:
    _, test = strings_corpus()
    quiet = test * 0.05
    mu = G.unmulaw(G.mulaw(quiet))
    lin = G.linear8(quiet)
    err = lambda a: float(10 * np.log10(np.sum(quiet ** 2) / np.sum((a - quiet) ** 2)))
    c = concat([C(lin), C(mu)], gap=0.8, names=["linear", "mulaw"])
    return {"samples_per_second": G.SR16, "cd": 44100, "bits_cd": 16, "frames_per_second": G.SR16 / G.HOP, "snr_linear": err(lin), "snr_mulaw": err(mu),
            "starts": {k: float(c.events[k]) for k in ("linear", "mulaw")},
            "clips": {"two": save("rates.two", c, detail="a quiet bowed-string phrase in plain 8-bit samples, then in 8-bit mu-law samples, both turned up to be heard")}}


def compute_ar() -> dict:
    import time
    train, test = strings_corpus()
    fit = G.train_ar(train, context=256, hidden=256, steps=1500)
    bits = G.ar_bits(fit, test)
    prime = test[: int(0.5 * G.SR16)]
    t0 = time.time()
    y = G.sample_ar(fit, prime, int(1.0 * G.SR16), temperature=1.0, seed=1)
    secs = time.time() - t0
    c = concat([C(prime), C(np.r_[prime, y])], gap=0.8, names=["prime", "continued"])
    return {"bits_train_curve": fit["losses"], "bits_test": bits, "seconds_to_sample_1s": secs, "context": fit["context"],
            "starts": {k: float(c.events[k]) for k in ("prime", "continued")},
            "clips": {"two": save("ar.two", c, detail="half a second of a bowed string phrase, then the same half second continued for one second by a network that writes one sample at a time")}}


def compute_vocoder() -> dict:
    _, test = strings_corpus()
    M = G.mel(test, 64)
    y_mel = G.mel_to_audio(M, len(test))
    y_gl = G.griffin_lim(np.abs(G.stft(test)), len(test))
    c = concat([C(test), C(y_mel)], gap=0.8, names=["original", "mel"])
    return {"dist_mel": G.spectral_distance(test, y_mel), "dist_gl": G.spectral_distance(test, y_gl), "mel_shape": list(M.shape),
            "values_per_second_mel": 64 * G.SR16 / G.HOP, "mel": np.log10(M[:, :180] + 1e-4).tolist(),
            "starts": {k: float(c.events[k]) for k in ("original", "mel")},
            "clips": {"two": save("vocoder.two", c, detail="a bowed-string phrase, then the same rebuilt from its 64-band mel spectrogram by a pseudo-inverse and Griffin-Lim's phase")}}


def compute_codec() -> dict:
    q = rvq()
    _, test = piano_corpus()
    name, y = test[0]
    Fr = G.frames(y)
    rows, segs = {}, []
    for st in (1, 2, 4):
        rec = G.from_frames(q.decode(q.encode(Fr, st)), len(y))
        rows[str(st)] = {"dist": G.spectral_distance(y, rec), "kbps": st * 8 * G.SR16 / G.HOP / 1000, "tokens_per_second": st * G.SR16 / G.HOP}
        segs.append(C(rec[: int(8 * G.SR16)]))
    rows["phase only"] = {"dist": G.spectral_distance(y, G.from_frames(Fr, len(y))), "kbps": None, "tokens_per_second": None}
    c = concat([C(y[: int(8 * G.SR16)])] + segs, gap=0.8, names=["original", "s1", "s2", "s4"])
    return {"rows": rows, "tune": name, "codebook": 256, "starts": {k: float(c.events[k]) for k in ("original", "s1", "s2", "s4")},
            "clips": {"four": save("codec.four", c, detail=f"eight seconds of the chorale tune {name} on Part 38's piano, then through a residual vector-quantizing codec with one, two and four tokens a frame")}}


def _tok(y, stages=1):
    return rvq().encode(G.frames(y), stages)[0]


def compute_tokenlm() -> dict:
    import torch
    from dataclasses import asdict
    from explainer.lm import pocket
    train, test = piano_corpus()
    BOS, EOS = 256, 257
    seqs = [[BOS] + _tok(y).tolist() + [EOS] for _, y in train]
    rng = np.random.default_rng(1)
    order = rng.permutation(len(seqs))
    nv = max(4, len(seqs) // 10)
    val = np.array(sum([seqs[i] for i in order[:nv]], []), np.int64)
    trn = np.array(sum([seqs[i] for i in order[nv:]], []), np.int64)
    path = CACHE.dir / "tokenlm.pt"
    if path.exists():
        ck = torch.load(path, weights_only=False)
        model = pocket.PocketGPT(pocket.Config(**ck["config"]))
        model.load_state_dict(ck["state"])
        info = ck["info"]
    else:
        cfg = pocket.Config(vocab=258, d=128, layers=4, heads=4, seq=256)
        runs = {}
        for steps in (1500,):
            run = pocket.Run(model=cfg, lr=2e-3, batch=16, tokens=steps * 16 * 256, seed=0, warmup=80, eval_every=50, eval_batches=4)
            runs[steps] = pocket.train(run, pocket.TokenStream(trn, val, 256, seed=0), threads=2)
        long = runs[1500]
        ev = np.array(long["evals"])
        best = int(ev[int(np.argmin(ev[:, 2])), 0])
        run = pocket.Run(model=cfg, lr=2e-3, batch=16, tokens=best * 16 * 256, seed=0, warmup=80, eval_every=max(1, best // 20), eval_batches=4)
        res = pocket.train(run, pocket.TokenStream(trn, val, 256, seed=0), threads=2)
        model = res["_model"]
        info = {"curve": [[float(a), float(c)] for a, _, c in long["evals"]], "steps": best, "params": int(res["counts"]["total"]),
                "train_tokens": int(len(trn))}
        torch.save({"config": asdict(cfg), "state": model.state_dict(), "info": info}, path)
    # continue a test tune from its first four seconds
    name, y = test[1]
    toks = _tok(y)
    k = int(4 * G.SR16 / G.HOP)
    prompt = [BOS] + toks[:k].tolist()
    g = torch.Generator().manual_seed(66)
    ids = list(prompt)
    model.eval()
    with torch.no_grad():
        for _ in range(int(6 * G.SR16 / G.HOP)):
            logits = model(torch.tensor([ids[-256:]]))[0, -1]
            logits[BOS] = -float("inf")
            logits[EOS] = -float("inf")
            ids.append(int(torch.multinomial(logits.softmax(-1), 1, generator=g)))
    gen = np.array(ids[1:])
    q = rvq()
    y_gen = G.from_frames(q.decode(gen[None, :]), len(gen) * G.HOP)
    y_true = G.from_frames(q.decode(toks[None, :len(gen)]), len(gen) * G.HOP)
    # copying: the longest run of generated tokens (after the prompt) found in the training tokens
    big = trn.tolist()
    s = ",".join(map(str, big))
    cont = gen[k:].tolist()
    longest = 0
    for i in range(len(cont)):
        L = longest + 1
        while i + L <= len(cont) and ("," + ",".join(map(str, cont[i:i + L])) + ",") in ("," + s + ","):
            longest = L
            L += 1
    c = concat([C(y_true), C(y_gen)], gap=0.8, names=["true", "generated"])
    return {**info, "tune": name, "prompt_seconds": 4.0, "continued_seconds": 6.0, "longest_copy_frames": longest,
            "longest_copy_seconds": longest * G.HOP / G.SR16, "starts": {k_: float(c.events[k_]) for k_ in ("true", "generated")},
            "clips": {"two": save("tokenlm.two", c, detail=f"the chorale tune {name} on the piano through the one-token codec, ten seconds; then its first four seconds continued for six by a transformer over the codec's tokens")}}


def compute_diffusion() -> dict:
    """Harmonic profiles of bowed notes (the level of each of 24 harmonics, in dB relative to the strongest), learnt by
    a diffusion model conditioned on pitch; new profiles drawn and played as steady tones."""
    import torch
    rng = np.random.default_rng(3)
    X, P = [], []
    for _ in range(300):
        m = 55 + int(rng.integers(0, 27))
        z = G.to16(STR.bowed_note(hz(m), 0.5) * float(rng.uniform(0.3, 1.0)))
        seg = z[int(0.15 * G.SR16):int(0.4 * G.SR16)]
        S = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
        f = np.fft.rfftfreq(len(seg), 1 / G.SR16)
        amps = np.array([S[np.argmin(np.abs(f - k * hz(m)))] if k * hz(m) < 7800 else 1e-9 for k in range(1, 25)])
        db = 20 * np.log10(amps / amps.max() + 1e-6)
        X.append(np.maximum(db, -80) / 40)
        P.append((m - 68) / 13)
    X, P = np.array(X), np.array(P)
    dm = G.Diffusion(24, cond=1, T=100, seed=0)
    losses = dm.fit(X, P, steps=4000)
    pitches = [57, 69, 79]
    out, snaps = dm.sample(np.array([(m - 68) / 13 for m in pitches]), seed=5, keep=(99, 75, 50, 25, 0))
    real = []
    for m in pitches:
        i = int(np.argmin(np.abs(np.array(P) - (m - 68) / 13)))
        real.append(X[i])

    def tone(m, prof):
        A = 10 ** (np.asarray(prof) * 40 / 20)
        n = int(1.2 * G.SR16 / 64)
        env = np.minimum(1, np.arange(n) / 20) * np.minimum(1, (n - np.arange(n)) / 40)
        return G.harmonic_synth(np.full(n, hz(m)), env[:, None] * A[None, :], hop=64)
    segs = [C(tone(m, real[k])) for k, m in enumerate(pitches)] + [C(tone(m, out[k])) for k, m in enumerate(pitches)]
    names = [f"real{k}" for k in range(3)] + [f"gen{k}" for k in range(3)]
    c = concat(segs, gap=0.5, names=names)
    near = [float(np.min(np.abs(X - out[k]).mean(1)) * 40) for k in range(3)]
    return {"losses": losses, "pitches": pitches, "generated": (out * 40).tolist(), "real": (np.array(real) * 40).tolist(),
            "snapshots": {str(t): (v * 40).tolist() for t, v in snaps.items()}, "nearest_db": near, "n_train": len(X),
            "starts": {k: float(c.events[k]) for k in names},
            "clips": {"six": save("diffusion.six", c, detail="steady tones at A3, A4 and G5 with harmonic profiles measured from the bowed-string model, then with profiles drawn by a diffusion model")}}


def compute_ddsp() -> dict:
    fit = ddsp()
    _, test = strings_corpus()
    f = G.features(test)
    y, amp = G.render_ddsp(fit, f["f0"], f["loud"])
    y = y[:len(test)]
    c = concat([C(test), C(y)], gap=0.8, names=["model", "ddsp"])
    return {"losses": fit["losses"], "dist": G.spectral_distance(test, y), "dist_noise": G.spectral_distance(test, np.random.default_rng(1).standard_normal(len(test)) * np.std(test)),
            "params": int(sum(p.numel() for p in fit["net"].parameters())), "amps": np.log10(amp[::8] + 1e-6).tolist(), "f0": f["f0"][::8].tolist(),
            "loud": f["loud"][::8].tolist(), "starts": {k: float(c.events[k]) for k in ("model", "ddsp")},
            "clips": {"two": save("ddsp.two", c, detail="the Tune's first two phrases on Part 9's bowed-string model, then a DDSP network's resynthesis from their pitch and loudness alone")}}


def compute_fad() -> dict:
    train, test = strings_corpus()
    fit = ddsp()
    real = embed_chunks(train)
    f = G.features(test)
    y_ddsp = G.render_ddsp(fit, f["f0"], f["loud"])[0][:len(test)]
    ar = CLIPS.load("ar.two")
    y_ar = G.to16(ar.y if ar.y.ndim == 1 else ar.y.mean(1))[int(1.3 * G.SR16):]
    y_mel = G.mel_to_audio(G.mel(test, 64), len(test))
    noise = np.random.default_rng(2).standard_normal(len(test)) * np.std(test)
    sets = {"the training notes, replayed": train[: len(test) * 2], "another bowed phrase": test, "DDSP": y_ddsp, "mel and Griffin-Lim": y_mel,
            "sample by sample": y_ar, "white noise": noise}
    allX = np.concatenate([real] + [embed_chunks(v) for v in sets.values()])
    mu, sd = allX.mean(0), allX.std(0) + 1e-9
    R = (real - mu) / sd
    # project to the 8 main directions of the real set, so that the covariances are estimable from few chunks
    U, s_, Vt = np.linalg.svd(R - R.mean(0), full_matrices=False)
    P = Vt[:8].T
    out = {k: G.frechet(R @ P, ((embed_chunks(v) - mu) / sd) @ P) for k, v in sets.items()}
    return {"distances": out, "order": list(sets), "chunks_real": len(real)}


def compute_watermark() -> dict:
    _, test = strings_corpus()
    key = 1966
    rows = {}
    for db in (-25, -35):
        m = G.watermark(test, key, strength_db=db)
        y48 = G.to48(m)
        coded = G.to16(K.encode(y48, 64)["y"])[:len(m)]
        shifted = np.r_[np.zeros(37), m[:-37]]
        from scipy.signal import fftconvolve
        from explainer.music.monochord import space as SPC
        ir = G.to16(SPC.noise_tail(0.6, 0.5, seed=4, stereo=False, start=0.004))
        ir = ir / np.max(np.abs(ir))
        ir[0] = 1.0
        roomed = fftconvolve(m, ir)[: len(m)]
        rows[str(db)] = {"marked": G.detect(m, key), "coded": G.detect(coded, key), "shifted": G.detect(shifted, key), "room": G.detect(roomed, key, max_lag=50),
                         "shifted_search": G.detect(shifted, key, max_lag=50),
                         "other_key": float(max(wrong := [G.detect(m, key + j) for j in range(1, 11)])), "other_key_mean": float(np.mean(wrong))}
    clean = G.detect(test, key)
    m = G.watermark(test, key, strength_db=-35)
    c = concat([C(m), C(test)], gap=0.8, names=["first", "second"])
    return {"rows": rows, "clean": clean, "key": key, "answer": "first", "starts": {k: float(c.events[k]) for k in ("first", "second")},
            "clips": {"two": save("watermark.two", c, detail="a bowed-string phrase twice: once carrying a spread-spectrum watermark 35 dB below it, once not")}}


def compute_hook() -> dict:
    fit = ddsp()
    ev = T.events(0.45, [2, 3])
    y = np.concatenate([STR.bowed_note(hz(67 + MAJOR[e["degree"]]), e["dur"]) for e in ev])
    y = G.to16(y / np.max(np.abs(y)) * 0.8)
    f = G.features(y)
    d = G.render_ddsp(fit, f["f0"], f["loud"])[0][:len(y)]
    c = concat([C(d), C(y)], gap=0.8, names=["first", "second"])
    return {"answer": "first", "dist": G.spectral_distance(y, d), "starts": {k: float(c.events[k]) for k in ("first", "second")},
            "clips": {"two": save("hook.two", c, detail="the Tune's middle phrases twice: a DDSP network's resynthesis, then Part 9's bowed-string model it learnt from")}}


def compute_tune66() -> dict:
    fit = ddsp()
    ev = T.events(0.5, [0, 1])
    notes = [(62 + MAJOR[e["degree"]] - 12, e["t"], e["dur"]) for e in ev]
    sung = G.to16(CH.sing(notes, "alto", "a", seed=2))
    sung = sung / np.max(np.abs(sung)) * 0.8
    f = G.features(sung)
    f0 = f["f0"] * 2                                            # up an octave, into the string's range
    y_str = G.render_ddsp(fit, f0, f["loud"])[0][:len(sung)]
    # the piano Tune, continued by the token model
    import torch
    from explainer.lm import pocket
    ck = torch.load(CACHE.dir / "tokenlm.pt", weights_only=False)
    model = pocket.PocketGPT(pocket.Config(**ck["config"]))
    model.load_state_dict(ck["state"])
    tn = [(72 + MAJOR[e["degree"]] - 12 * (MAJOR[e["degree"]] > 9), int(round(e["dur"] / 0.5 * 4)), i + 1 == len(ev) or ev[i + 1]["phrase"] != e["phrase"]) for i, e in enumerate(ev)]
    yp = piano_tune(tn[: len([e for e in ev if e["phrase"] == 0])])
    toks = _tok(yp)
    g = torch.Generator().manual_seed(6)
    ids = [256] + toks.tolist()
    model.eval()
    with torch.no_grad():
        for _ in range(int(5 * G.SR16 / G.HOP)):
            logits = model(torch.tensor([ids[-256:]]))[0, -1]
            logits[256] = -float("inf")
            logits[257] = -float("inf")
            ids.append(int(torch.multinomial(logits.softmax(-1), 1, generator=g)))
    q = rvq()
    y_cont = G.from_frames(q.decode(np.array(ids[1:])[None, :]), (len(ids) - 1) * G.HOP)
    c = concat([C(sung), C(y_str), C(y_cont)], gap=0.8, names=["sung", "string", "continued"])
    return {"names": ["sung", "string", "continued"], "seconds": c.duration, "starts": {k: float(c.events[k]) for k in ("sung", "string", "continued")},
            "prompt_seconds": len(toks) * G.HOP / G.SR16,
            "clips": {"variation66": save("tune.variation66", c, detail="Variation 66: the Tune's opening sung by Part 8's alto, re-rendered by the DDSP string from its pitch and loudness, then its first phrase on the piano continued by the token model")}}


def compute_variation() -> dict:
    t = load("tune66")
    d = load("ddsp")
    return {"part": 66, "title": "sung, re-rendered as a DDSP string, and continued by a token model", "seconds": round(t["seconds"], 1),
            "measure": f"DDSP {d['dist']:.1f} dB from the string it learnt; {t['prompt_seconds']:.1f} s of piano continued for 5 s",
            "clip": "tune.variation66"}

def compute_zoom() -> dict:
    """A second of the bowed phrase at three magnifications: the phrase, one note's waves, a few samples."""
    _, test = strings_corpus()
    a = int(0.6 * G.SR16)
    return {"second": test[:G.SR16:8].tolist(), "note": test[a:a + 800].tolist(), "samples": test[a + 200:a + 232].tolist()}


def compute_tokpic() -> dict:
    """A tune's tokens as a picture: its log spectrum, the first codebook's entries for its frames, and the token
    numbers themselves."""
    _, test = piano_corpus()
    name, y = test[0]
    Fr = G.frames(y)[:240]
    q = rvq()
    codes = q.encode(Fr, 1)[0]
    rec = q.books[0][codes]
    return {"tune": name, "spectrum": Fr[:, :128].T.tolist(), "codebook": rec[:, :128].T.tolist(), "tokens": codes[:40].tolist(),
            "distinct": int(len(set(codes.tolist()))), "frames": int(len(codes))}


def compute_vibrato() -> dict:
    """The DDSP string driven by controls it never saw: a slow swell with a wide vibrato, and a glide over an octave."""
    fit = ddsp()
    hop = fit["hop"]
    n = int(3.0 * G.SR16 / hop)
    t = np.arange(n) * hop / G.SR16
    f0 = hz(69) * 2 ** (0.5 * np.sin(2 * np.pi * 5.5 * t) / 12)
    loud = -38 + 26 * np.sin(np.pi * t / 3.0)
    a = G.render_ddsp(fit, f0, loud)[0]
    g0 = hz(62) * 2 ** (12 * np.clip(t / 2.5, 0, 1) / 12)
    b = G.render_ddsp(fit, g0, np.full(n, -16.0))[0]
    c = concat([C(a), C(b)], gap=0.8, names=["vibrato", "glide"])
    return {"starts": {k: float(c.events[k]) for k in ("vibrato", "glide")},
            "clips": {"two": save("vibrato.two", c, detail="the DDSP string driven by controls it never learnt from: a swell with a vibrato a semitone wide, then a glide from D4 up an octave")}}


def compute_voices() -> dict:
    """One performance (the same notes, timing and vibrato), sung by three of Part 8's voices: what voice conversion
    keeps and what it changes."""
    ev = T.events(0.5, [0])
    segs = []
    for part, base in (("soprano", 69), ("alto", 62), ("tenor", 57)):
        notes = [(base + MAJOR[e["degree"]], e["t"], e["dur"]) for e in ev]
        y = G.to16(CH.sing(notes, part, "a", seed=4))
        segs.append(C(y / np.max(np.abs(y)) * 0.8))
    c = concat(segs, gap=0.7, names=["soprano", "alto", "tenor"])
    return {"starts": {k: float(c.events[k]) for k in ("soprano", "alto", "tenor")},
            "clips": {"three": save("voices.three", c, detail="the Tune's first phrase, one performance, sung by Part 8's soprano, alto and tenor voices")}}


def compute_melbands() -> dict:
    """The bowed phrase rebuilt from mel spectrograms of 16, 64 and 256 bands."""
    _, test = strings_corpus()
    out, segs = {}, []
    for b in (16, 64, 256):
        y = G.mel_to_audio(G.mel(test, b), len(test))
        out[str(b)] = G.spectral_distance(test, y)
        segs.append(C(y))
    c = concat(segs, gap=0.8, names=["b16", "b64", "b256"])
    return {"dist": out, "starts": {k: float(c.events[k]) for k in ("b16", "b64", "b256")},
            "clips": {"three": save("melbands.three", c, detail="a bowed-string phrase rebuilt from its mel spectrogram with 16, 64 and 256 bands")}}



def compute_signoff() -> dict:
    """The part's last sound: the opening of its Variation, under the next part's title."""
    load("variation")
    return signoff(CLIPS, "tune.variation66", 66)


ITEMS = {"corpus": compute_corpus, "rates": compute_rates, "ar": compute_ar, "vocoder": compute_vocoder, "codec": compute_codec,
         "tokenlm": compute_tokenlm, "diffusion": compute_diffusion, "ddsp": compute_ddsp, "fad": compute_fad,
         "watermark": compute_watermark, "hook": compute_hook, "tune66": compute_tune66, "variation": compute_variation,
         "zoom": compute_zoom, "tokpic": compute_tokpic, "vibrato": compute_vibrato, "voices": compute_voices, "melbands": compute_melbands,
         "signoff": compute_signoff}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
