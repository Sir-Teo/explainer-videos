"""Precompute everything numerical, and every sound, in Part 58 of *Music, Built* ("Compression for the Ear").

    python -m videos.music.music58.compute              # everything missing (several minutes)
    python -m videos.music.music58.compute --force hook

Numbers are cached in ``.cache/music58/<name>.json``, sounds in ``.cache/music58/audio/``.  The tools are Monochord's
(``explainer/music/monochord/codec.py``, with Part 4's ear).  The music is Part 8's voice, singing the Tune alone, and
Part 56's session; every codec here is Monochord's own, not MP3, AAC or Opus.

Items:
    hook        an ear question: the Tune sung alone, as recorded and through our coder at 64 and 16 kbit/s: which was
                the original?
    lossless    entropy, prediction and Rice codes: a bit-exact round trip
    masking     one frame's spectrum and its mask; noise of the same power, white and shaped to the mask (an ear question)
    mdct        the MDCT's basis, one frame's aliases, their cancellation; a signal rebuilt from every other frame
    preecho     castanet-like hits coded with long and with short blocks
    rates       the voice and the mix at five bit rates: margin to the mask, bands over it, signal-to-noise ratio
    stereo      the session's stereo mix coded left/right and mid/side at one rate
    abx         the power of an ABX test
    transcode   one encoding against five generations
    rvq         residual vector quantization of MDCT vectors: error against stages
    tune58      Variation 58: the Tune at five bit rates, and what the codec discarded, played alone
    variation   the Variations ledger, row 58
"""

from __future__ import annotations

import math

import numpy as np
from scipy.stats import binom

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat
from explainer.music.monochord import codec as K
from explainer.music.monochord import tune as T
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.instruments import drumkit as DK
from explainer.music.monochord.partkit import saver, signoff
from videos.music.music56 import compute as P56

CACHE = Cache("music58")
CLIPS = ClipStore("music58")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
MAJOR = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
RATES = [128, 64, 32, 24, 16]


def C(y) -> Clip:
    return Clip(np.asarray(y, float), SR)


def fade(y, a=0.005, r=0.08):
    y = np.array(y, float)
    ka, kr = max(int(a * SR), 1), max(int(r * SR), 1)
    y[:ka] *= np.linspace(0, 1, ka)
    y[len(y) - kr:] *= np.linspace(1, 0, kr)
    return y


def snr(x, y):
    return float(10 * np.log10(np.sum(x ** 2) / (np.sum((x - y) ** 2) + 1e-20)))


_V: dict = {}


def voice(phrases=(0,)):
    if phrases not in _V:
        notes = [(60 + MAJOR[e["degree"]], e["t"], e["dur"]) for e in T.events(0.5, list(phrases))]
        v = CH.sing(notes, "soprano", "a", seed=1)
        _V[phrases] = 0.3 * v / np.max(np.abs(v))
    return _V[phrases]


def mono_mix(phrases=(0, 1)):
    key = ("mix", phrases)
    if key not in _V:
        s = P56.session(phrases)
        m = P56.mix_dry(s["tracks"], s["n"])["y"]
        _V[key] = 0.5 * m.mean(axis=1) / np.max(np.abs(m.mean(axis=1)))
        _V[("st",) + phrases] = 0.5 * m / np.max(np.abs(m))
    return _V[key]


def stereo_mix(phrases=(0, 1)):
    mono_mix(phrases)
    return _V[("st",) + phrases]


# ---------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    v = voice()
    r64, r16 = K.encode(v, 64), K.encode(v, 16)
    order = ["c64", "orig", "c16"]
    seg = {"orig": v, "c64": r64["y"], "c16": r16["y"]}
    c = concat([C(fade(seg[k])) for k in order], gap=0.9, names=["first", "second", "third"])
    return {"answer": "second", "order": order, "pcm_kbps": SR * 16 / 1000,
            "c64": {"kbps": r64["kbps"], "margin": r64["margin_db"], "over": r64["over"], "snr": snr(v, r64["y"])},
            "c16": {"kbps": r16["kbps"], "margin": r16["margin_db"], "over": r16["over"], "snr": snr(v, r16["y"])},
            "starts": {k: float(c.events[k]) for k in ("first", "second", "third")},
            "clips": {"three": save("hook.three", c, detail="the Tune's first phrase sung by Part 8's voice alone: through Monochord's perceptual coder at 64 kbit/s, as recorded, and through the coder at 16 kbit/s")}}


def compute_lossless() -> dict:
    v = voice((0, 1))
    m = mono_mix((0, 1))
    out = {"signals": {}}
    for name, x in (("voice", v), ("mix", m)):
        s = np.round(x * 32767).astype(np.int64)
        H = {str(o): K.entropy_bits(K.residual(s, o)) for o in range(5)}
        e = K.lossless_encode(s)
        d = K.lossless_decode(e["data"])
        orders = [o for o, _ in e["chosen"]]
        out["signals"][name] = {"entropy": H, "ratio": e["bits"] / (16 * len(s)), "exact": bool(np.array_equal(d, s)), "bits_per_sample": e["bits"] / len(s),
                                "orders": {str(o): orders.count(o) for o in range(5)}, "seconds": len(s) / SR}
    s = np.round(v * 32767).astype(np.int64)
    k0 = int(1.0 * SR)
    seg = s[k0:k0 + 400]
    out["trace"] = {"x": seg.tolist(), "e2": K.residual(s[k0 - 2:k0 + 400], 2).tolist()}
    hist_x, edges = np.histogram(s, bins=61, range=(-12000, 12000))
    hist_e, _ = np.histogram(K.residual(s, 2), bins=61, range=(-12000, 12000))
    out["hist"] = {"x": hist_x.tolist(), "e": hist_e.tolist(), "edges": edges.tolist()}
    return out


def compute_masking() -> dict:
    m = mono_mix((0, 1))
    N = 1024
    X = K.frames_mdct(m, N)
    i = int(2.4 * SR / N)
    f = X[i]
    mk = K.mask(f, N)
    freqs = (np.arange(N) + 0.5) * SR / (2 * N)
    B = mk["bands"]
    per_bin_allowed = np.zeros(N)
    per_bin_quiet = np.zeros(N)
    for (a, b), Nb, Q in zip(B, mk["allowed"], mk["quiet"]):
        per_bin_allowed[a:b] = Nb / (b - a)
        per_bin_quiet[a:b] = Q / (b - a)
    db = lambda p: (10 * np.log10(np.asarray(p) + 1e-20)).tolist()       # noqa: E731
    # noise of the same power: white, and shaped to the mask, added to the mix (an ear question)
    rng = np.random.default_rng(3)
    Xs = K.frames_mdct(m, N)
    shaped = np.zeros_like(Xs)
    for j, fr in enumerate(Xs):
        mm = K.mask(fr, N)
        for (a, b), Nb in zip(mm["bands"], mm["allowed"]):
            if (a + b) / 2 * SR / (2 * N) < 16000:
                shaped[j, a:b] = rng.standard_normal(b - a) * math.sqrt(Nb / (b - a))
    ns = K.frames_imdct(shaped, N, len(m))
    nw = rng.standard_normal(len(m))
    nw *= np.sqrt(np.mean(ns ** 2) / np.mean(nw ** 2))
    order = ["white", "shaped"]
    c = concat([C(fade(m + nw)), C(fade(m + ns))], gap=0.9, names=["first", "second"])
    return {"f": freqs.tolist(), "power_db": db(f ** 2), "allowed_db": db(per_bin_allowed), "quiet_db": db(per_bin_quiet),
            "band_edges_hz": [a * SR / (2 * N) for a, b in B] + [B[-1][1] * SR / (2 * N)], "alpha": mk["alpha"],
            "noise_snr_db": snr(m, m + ns), "answer": "first", "order": order,
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("masking.two", c, detail="Part 56's mix with noise added at the same power twice: white, then shaped band by band to the masking threshold Monochord's model computes")}}


def compute_mdct() -> dict:
    N = 16
    Cm, w = K.mdct_matrix(N)
    basis = {str(k): (w * Cm[k]).tolist() for k in (0, 1, 3)}
    # one frame's aliases: a ramp inside one frame, through MDCT and IMDCT
    n = np.arange(2 * N)
    x = np.where(n < N, n / N, 1.0) * np.sin(np.pi * n / (2 * N) * 3) + 0.2
    single = K.imdct(K.mdct(x, N), N)
    # a longer signal: frames and their overlap-add
    rng = np.random.default_rng(0)
    sig = np.cumsum(rng.standard_normal(6 * N)) / 6
    X = K.frames_mdct(sig, N)
    y = K.frames_imdct(X, N, len(sig))
    m = mono_mix((0,))
    Nl = 1024
    Xl = K.frames_mdct(m, Nl)
    full = K.frames_imdct(Xl, Nl, len(m))
    half = Xl.copy()
    half[1::2] = 0.0                                                   # every other frame dropped: aliases left uncancelled
    alias = K.frames_imdct(half, Nl, len(m)) * 2.0
    err = float(np.max(np.abs(full - m)))
    c = concat([C(fade(m)), C(fade(alias))], gap=0.9, names=["whole", "alternate"])
    return {"N": N, "basis": basis, "x": x.tolist(), "single": single.tolist(), "w": w.tolist(),
            "sig": sig.tolist(), "rebuilt": y.tolist(), "max_err_small": float(np.max(np.abs(y - sig))), "max_err_mix": err,
            "starts": {"whole": float(c.events["whole"]), "alternate": float(c.events["alternate"])},
            "clips": {"two": save("mdct.two", c, detail="Part 56's mix rebuilt from all of its MDCT frames, then from every other frame only (doubled), so that each frame's time-domain aliases are left uncancelled")}}


def castanets(seconds=3.0):
    y = np.zeros(int(seconds * SR))
    hit = np.asarray(DK.clave(), float)
    for t0 in (0.31, 0.71, 1.02, 1.52, 1.83, 2.23, 2.48):
        i = int(t0 * SR)
        y[i:i + len(hit)] += hit[: len(y) - i]
    return 0.5 * y / np.max(np.abs(y))


def pre_echo_db(x, y, onsets, ms=15.0):
    """Coding noise in the ms before each hit, against the hit's own level, dB."""
    out = []
    for t0 in onsets:
        i = int(t0 * SR)
        a = i - int(ms * SR / 1000)
        pre = np.mean((y[a:i] - x[a:i]) ** 2) + 1e-20
        hit = np.mean(x[i:i + int(ms * SR / 1000)] ** 2) + 1e-20
        out.append(10 * math.log10(pre / hit))
    return float(np.mean(out))


def compute_preecho() -> dict:
    x = castanets()
    onsets = [0.31, 0.71, 1.02, 1.52, 1.83, 2.23, 2.48]
    long_ = K.encode_at(x, 0.0, N=1024)
    short = K.encode_at(x, 0.0, N=128)
    i = int(1.02 * SR)
    a, b = i - int(0.03 * SR), i + int(0.02 * SR)
    step = 8
    c = concat([C(fade(long_["y"])), C(fade(short["y"]))], gap=0.9, names=["long", "short"])
    return {"pre_long": pre_echo_db(x, long_["y"], onsets), "pre_short": pre_echo_db(x, short["y"], onsets),
            "kbps": {"long": long_["kbps"], "short": short["kbps"]},
            "zoom": {"t": ((np.arange(a, b, step) - i) / SR * 1000).tolist(), "x": x[a:b:step].tolist(), "long": long_["y"][a:b:step].tolist(), "short": short["y"][a:b:step].tolist()},
            "block_ms": {"long": 2 * 1024 / SR * 1000, "short": 2 * 128 / SR * 1000},
            "starts": {"long": float(c.events["long"]), "short": float(c.events["short"])},
            "clips": {"two": save("preecho.two", c, detail="castanet-like hits (Part 40's clave) through Monochord's coder with its noise at the masking threshold, with long blocks (43 ms) and with short ones (5 ms)")}}


def compute_rates() -> dict:
    out = {}
    segs = []
    for name, x in (("voice", voice()), ("mix", mono_mix((0, 1)))):
        rows = []
        for kb in RATES:
            r = K.encode(x, kb)
            rows.append({"kbps": r["kbps"], "target": kb, "margin": r["margin_db"], "over": r["over"], "snr": snr(x, r["y"]), "cutoff": r["cutoff"]})
            if name == "voice":
                segs.append(C(fade(r["y"])))
        out[name] = rows
    out["pcm_kbps"] = SR * 16 / 1000
    names = [f"k{kb}" for kb in RATES]
    c = concat(segs, gap=0.7, names=names)
    out["starts"] = {k: float(c.events[k]) for k in names}
    out["clips"] = {"voice": save("rates.voice", c, detail="the Tune's first phrase sung by Part 8's voice alone, through Monochord's coder at 128, 64, 32, 24 and 16 kbit/s")}
    return out


def compute_stereo() -> dict:
    st = stereo_mix((0, 1))
    L, R = st[:, 0], st[:, 1]
    M, S = (L + R) / 2, (L - R) / 2
    total = 64
    rl, rr = K.encode(L, total / 2), K.encode(R, total / 2)
    # mid/side: the side is quieter, so it gets fewer bits
    share = np.sum(S ** 2) / (np.sum(M ** 2) + np.sum(S ** 2))
    side_kb = max(8.0, total * min(0.35, 0.5 * share + 0.08))
    rm, rs = K.encode(M, total - side_kb), K.encode(S, side_kb, cutoff=9000.0)
    lr = np.stack([rl["y"], rr["y"]], axis=1)
    ms = np.stack([rm["y"] + rs["y"], rm["y"] - rs["y"]], axis=1)
    c = concat([Clip(np.stack([fade(lr[:, 0]), fade(lr[:, 1])], axis=1), SR), Clip(np.stack([fade(ms[:, 0]), fade(ms[:, 1])], axis=1), SR)],
               gap=0.9, names=["lr", "ms"])
    return {"total": total, "side_kbps": side_kb, "side_share_db": float(10 * math.log10(share + 1e-20)),
            "lr": {"snr_l": snr(L, lr[:, 0]), "snr_r": snr(R, lr[:, 1]), "margin": (rl["margin_db"] + rr["margin_db"]) / 2},
            "ms": {"snr_l": snr(L, ms[:, 0]), "snr_r": snr(R, ms[:, 1]), "margin_m": rm["margin_db"], "margin_s": rs["margin_db"]},
            "starts": {"lr": float(c.events["lr"]), "ms": float(c.events["ms"])},
            "clips": {"two": save("stereo.two", c, detail="headphones: Part 56's stereo mix through Monochord's coder at 64 kbit/s in all, left and right coded apart, then mid and side", needs="headphones")}}


def compute_abx() -> dict:
    v = voice()
    b = K.encode(v, 32)["y"]
    trial = concat([C(fade(v)), C(fade(b)), C(fade(b))], gap=0.8, names=["A", "B", "X"])
    ns = [8, 10, 12, 16, 20, 30, 50, 100]
    ps = [0.6, 0.7, 0.8, 0.9]
    return {"n": ns, "p": ps, "threshold": {str(n): K.abx_threshold(n) for n in ns},
            "power": {str(p): [K.abx_power(n, p) for n in ns] for p in ps},
            "guess_pass": {str(n): float(binom.sf(K.abx_threshold(n) - 1, n, 0.5)) for n in ns}, "answer": "B",
            "starts": {k: float(trial.events[k]) for k in ("A", "B", "X")},
            "clips": {"trial": save("abx.trial", trial, detail="one ABX trial: A, the Tune's first phrase as sung; B, the same through Monochord's coder at 32 kbit/s; X, one of the two")}}


def compute_transcode() -> dict:
    x = mono_mix((0, 1))
    y = x.copy()
    gens = []
    once = None
    for g in range(5):
        r = K.encode(y, 48)
        y = r["y"]
        if g == 0:
            once = y.copy()
        gens.append({"generation": g + 1, "snr": snr(x, y), "margin": r["margin_db"]})
    c = concat([C(fade(once)), C(fade(y))], gap=0.9, names=["once", "five"])
    return {"kbps": 48, "gens": gens, "starts": {"once": float(c.events["once"]), "five": float(c.events["five"])},
            "clips": {"two": save("transcode.two", c, detail="Part 56's mix through Monochord's coder at 48 kbit/s once, then decoded and re-encoded five times")}}


def mdct_vectors(x, N=1024, dim=8, top=640):
    """MDCT coefficients cut into vectors of ``dim`` neighbouring bins, each vector divided by its band's RMS (sent as
    a scale factor), up to bin ``top`` (15 kHz)."""
    X = K.frames_mdct(x, N)[:, :top]
    V = X.reshape(X.shape[0], -1, dim)
    g = np.sqrt(np.mean(V ** 2, axis=2, keepdims=True)) + 1e-9
    return (V / g).reshape(-1, dim), g, X.shape


def compute_rvq() -> dict:
    train = np.concatenate([mono_mix((2,)), mono_mix((3,))])
    test = mono_mix((0, 1))
    Vt, _, _ = mdct_vectors(train)
    rng = np.random.default_rng(0)
    Vt = Vt[rng.choice(len(Vt), size=min(30000, len(Vt)), replace=False)]
    stages, k, dim = 8, 256, 8
    books = K.rvq_train(Vt, stages, k)
    V, g, shape = mdct_vectors(test)
    rows, recon = [], {}
    frames_per_s = SR / 1024
    vectors_per_frame = shape[1] // dim
    for s_ in range(1, stages + 1):
        Y, _ = K.rvq_encode(V, books, s_)
        X = (Y.reshape(shape[0], -1, dim) * g).reshape(shape[0], -1)
        Xf = np.zeros((shape[0], 1024))
        Xf[:, :shape[1]] = X
        y = K.frames_imdct(Xf, 1024, len(test))
        kbps = (s_ * 8 * vectors_per_frame + 6 * vectors_per_frame) * frames_per_s / 1000
        rows.append({"stages": s_, "vec_err_db": float(10 * np.log10(np.mean((V - Y) ** 2) / np.mean(V ** 2))), "snr": snr(test, y), "kbps": kbps})
        if s_ in (1, 3, 8):
            recon[s_] = y
    c = concat([C(fade(recon[1])), C(fade(recon[3])), C(fade(recon[8]))], gap=0.9, names=["s1", "s3", "s8"])
    return {"rows": rows, "k": k, "dim": dim, "stages": stages, "starts": {k_: float(c.events[k_]) for k_ in ("s1", "s3", "s8")},
            "clips": {"three": save("rvq.three", c, detail="Part 56's mix coded by residual vector quantization of its MDCT (codebooks of 256 eight-dimensional vectors, trained on other phrases), with 1, 3 and 8 stages")}}


def compute_tune58() -> dict:
    x = mono_mix((0, 1))
    segs, names, rows = [], [], []
    r32 = None
    for kb in RATES:
        r = K.encode(x, kb)
        rows.append({"kbps": kb, "margin": r["margin_db"], "snr": snr(x, r["y"])})
        segs.append(C(fade(r["y"][: int(6.0 * SR)])))
        names.append(f"k{kb}")
        if kb == 32:
            r32 = r["y"]
    residue = x - r32
    segs.append(C(fade(residue[: int(6.0 * SR)] * 3.0)))
    names.append("residue")
    c = concat(segs, gap=0.7, names=names)
    return {"rows": rows, "names": names, "seconds": c.duration, "residue_db": float(10 * np.log10(np.mean(residue ** 2) / np.mean(x ** 2))),
            "starts": {k: float(c.events[k]) for k in names},
            "clips": {"variation58": save("tune.variation58", c, detail="Part 56's session playing the Tune, through Monochord's coder at 128, 64, 32, 24 and 16 kbit/s; then what the 32 kbit/s version discarded, played alone and turned up 10 dB")}}


def compute_variation() -> dict:
    t = load("tune58")
    r = {row["kbps"]: row for row in t["rows"]}
    return {"part": 58, "title": "at five bit rates, and the residue alone", "seconds": round(t["seconds"], 1),
            "measure": f"128 to 16 kbit/s: noise {r[128]['margin']:.0f} dB under the mask at 128, {-r[16]['margin']:.0f} dB over it at 16",
            "clip": "tune.variation58"}


def compute_signoff() -> dict:
    """The part's last sound: the opening of its Variation, under the next part's title."""
    load("variation")
    return signoff(CLIPS, "tune.variation58", 58)


ITEMS = {"hook": compute_hook, "lossless": compute_lossless, "masking": compute_masking, "mdct": compute_mdct, "preecho": compute_preecho,
         "rates": compute_rates, "stereo": compute_stereo, "abx": compute_abx, "transcode": compute_transcode, "rvq": compute_rvq,
         "tune58": compute_tune58, "variation": compute_variation,
         "signoff": compute_signoff}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
