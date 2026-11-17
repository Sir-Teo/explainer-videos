"""Precompute everything numerical, and every sound, in Part 63 of *Music, Built* ("Finding Music").

    python -m videos.music.music63.compute              # everything missing (several minutes: every clip is indexed)
    python -m videos.music.music63.compute --force hook

Numbers are cached in ``.cache/music63/<name>.json``, sounds in ``.cache/music63/audio/``.  The tools are Monochord's
finders (``explainer/music/monochord/mir/finder.py``).  The library searched is every sound of Parts 1 to 60, as each
part stored it; the listeners are simulated, with tastes known.

Items:
    library     every clip of Parts 1 to 60: count, length, hashes indexed
    hook        five seconds of a Variation in a noisy bar, named, with the offset
    constellation  one Variation's spectrogram, its peaks and hashes; the peaks alone re-synthesized
    robust      recognition of five-second queries from the Variations against white noise, bar noise and a codec
    falsematch  the arithmetic of chance agreement
    horse       a classifier that learnt a mains hum instead of the music (an ear question)
    recs        simulated listeners: popularity against implicit ALS, recall at 10; cold start from content
    loop        a recommender that recommends what is already played: inequality over rounds, with and without exploring
    playlist    the Variations ordered so that neighbours sound alike (an ear question)
    tune63      Variation 63: three noisy five-second excerpts, each named
    variation   the Variations ledger, row 63
    matches     the hashes a noisy query shares with the true recording and with another: a line, and a scatter
    length      recognition against the query's length, in bar noise
    speed       recognition when the query is played a little fast
    map         every clip's content embedding on its first two principal components; the playlist's path
    matrix      the simulated play matrix as a picture, and ALS's reconstruction of it
    lorenz      Lorenz curves of plays after the feedback loop, with and without exploring, and on users' own
    neighbours  a clip, two nearest neighbours by content and its farthest (an ear question)
    scale       chance matches as the library grows to a hundred million three-minute-and-twenty-second tracks
    sampled     a Variation as a sample under another clip, at several levels: is the sample found, and the track on top?
    hum         query by humming: the Tune sung slower, in another key; the fingerprint against a pitch contour
    lengthpair  one noisy query at one second and at eight, heard
"""

from __future__ import annotations

import glob
import math
import os

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat
from explainer.music.monochord import codec as K
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.mir import finder as F
from explainer.music.monochord.partkit import saver, signoff

CACHE = Cache("music63")
CLIPS = ClipStore("music63")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def C(y) -> Clip:
    return Clip(np.asarray(y, float), SR)


def fade(y, a=0.005, r=0.08):
    y = np.array(y, float)
    ka, kr = max(int(a * SR), 1), max(int(r * SR), 1)
    y[:ka] *= np.linspace(0, 1, ka)
    y[len(y) - kr:] *= np.linspace(1, 0, kr)
    return y


_L: dict = {}


def library():
    """Every clip of Parts 1 to 60: (part, name) -> Clip."""
    if "lib" in _L:
        return _L["lib"]
    out = {}
    for n in range(1, 61):
        d = os.path.join(REPO, ".cache", f"music{n}", "audio")
        if not os.path.isdir(d):
            continue
        store = ClipStore(f"music{n}")
        for j in sorted(glob.glob(os.path.join(d, "*.json"))):
            name = os.path.basename(j)[:-5]
            try:
                out[(f"music{n}", name)] = store.load(name)
            except Exception:
                continue
    _L["lib"] = out
    return out


def mono(c: Clip):
    y = np.asarray(c.y, float)
    return y.mean(axis=1) if y.ndim == 2 else y


def index():
    if "idx" in _L:
        return _L["idx"]
    idx = F.Index()
    for (p, n), c in library().items():
        idx.add(f"{p}/{n}", mono(c), c.sr)
    _L["idx"] = idx
    return idx


def variations():
    return sorted([k for k in library() if k[1].startswith("tune.variation")], key=lambda k: int(k[0][5:]))


def bar_noise(seconds, seed=0):
    """A noisy bar: a dozen people singing and talking on random notes (Part 8's voice, many seeds), pink noise, and
    the odd clink of glass."""
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    y = np.zeros(n)
    for k in range(10):
        notes, t = [], float(rng.uniform(0, 0.5))
        while t < seconds:
            d = float(rng.uniform(0.15, 0.5))
            notes.append((int(rng.integers(48, 70)), t, d))
            t += d + float(rng.uniform(0.0, 0.3))
        v = CH.sing(notes, ("alto", "tenor", "bass", "soprano")[k % 4], ("a", "O", "E", "i")[k % 4], seed=100 + k)
        y += np.r_[v, np.zeros(max(0, n - len(v)))][:n] / (np.max(np.abs(v)) + 1e-9)
    f = np.fft.rfftfreq(n, 1 / SR)
    pink = np.fft.irfft(np.fft.rfft(rng.standard_normal(n)) / np.sqrt(np.maximum(f, 20)), n)
    y = y / np.std(y) + 0.5 * pink / np.std(pink)
    for _ in range(int(seconds * 0.6)):
        i = int(rng.integers(0, n - 4000))
        tt = np.arange(4000) / SR
        y[i:i + 4000] += 2.0 * np.sin(2 * np.pi * rng.uniform(2500, 4500) * tt) * np.exp(-tt / 0.03)
    return y / np.std(y)


def at_snr(sig, noise, snr):
    noise = noise[: len(sig)]
    return sig + noise * np.std(sig) * 10 ** (-snr / 20) / (np.std(noise) + 1e-12)


def excerpt(y, sr, seconds=5.0, rng=None, loud=True):
    rng = rng or np.random.default_rng(0)
    n = int(seconds * sr)
    if len(y) <= n:
        return 0, y
    e = np.array([np.sqrt(np.mean(y[i:i + sr // 2] ** 2)) for i in range(0, len(y) - n, sr // 2)])
    ok = np.flatnonzero(e > 0.4 * e.max()) if loud else np.arange(len(e))
    a = int(rng.choice(ok)) * (sr // 2)
    return a, y[a:a + n]


# ---------------------------------------------------------------------------------------------- items
def compute_library() -> dict:
    lib = library()
    idx = index()
    secs = sum(c.duration for c in lib.values())
    return {"clips": len(lib), "hours": secs / 3600, "hashes": idx.size, "variations": len(variations()),
            "parts": len({p for p, _ in lib})}


def compute_hook() -> dict:
    lib = library()
    idx = index()
    k = ("music40", "tune.variation40") if ("music40", "tune.variation40") in lib else variations()[len(variations()) // 2]
    c = lib[k]
    y = mono(c)
    a, seg = excerpt(y, c.sr, 5.0, np.random.default_rng(4))
    noise = bar_noise(5.0, seed=1)
    q = at_snr(seg, noise, 0.0)
    r = idx.query(q, c.sr)
    clip = C(fade(q / np.max(np.abs(q)) * 0.9))
    return {"truth": f"{k[0]}/{k[1]}", "offset_s": a / c.sr, "result": r, "snr": 0.0,
            "clips": {"bar": save("hook.bar", clip, detail=f"five seconds of {k[1]} (from {k[0]}) in a simulated noisy bar, music and noise equally loud")}}


def compute_constellation() -> dict:
    lib = library()
    k = variations()[0]
    c = lib[k]
    y = F.to_8k(mono(c), c.sr)[: 8 * F.SR_FP]
    S = F.spectrogram(y)
    pts = F.peaks(S)
    hs = F.hashes(pts)
    # the peaks alone, re-synthesized: a short sine at each peak's frequency and time
    out = np.zeros(int(8 * SR))
    for t, b in pts:
        f = b * F.SR_FP / 1024
        i = int(t * 256 / F.SR_FP * SR)
        nn = int(0.06 * SR)
        tt = np.arange(nn) / SR
        if i + nn < len(out):
            out[i:i + nn] += np.sin(2 * np.pi * f * tt) * np.hanning(nn)
    orig = np.asarray(c.y if c.y.ndim == 1 else c.y.mean(axis=1), float)[: int(8 * c.sr)]
    if c.sr != SR:
        orig = np.interp(np.arange(0, len(orig), c.sr / SR), np.arange(len(orig)), orig)
    cl = concat([C(fade(orig / np.max(np.abs(orig)) * 0.9)), C(fade(out / np.max(np.abs(out)) * 0.9))], gap=0.8, names=["full", "peaks"])
    return {"name": f"{k[0]}/{k[1]}", "S": S[:256:2, ::2].tolist(), "peaks": pts.tolist(), "n_hashes": len(hs), "per_second": len(pts) / 8.0,
            "starts": {"full": float(cl.events["full"]), "peaks": float(cl.events["peaks"])},
            "clips": {"two": save("constellation.two", cl, kind="synthesized", detail=f"eight seconds of {k[1]}, then only its fingerprint's peaks, each a short sine at its frequency")}}


def compute_robust() -> dict:
    lib = library()
    idx = index()
    var = variations()
    rng = np.random.default_rng(7)
    noise = bar_noise(6.0, seed=3)
    rows = {"white": [], "bar": []}
    snrs = [20, 10, 5, 0, -5, -10]
    queries = []
    for k in var:
        c = lib[k]
        y = mono(c)
        if len(y) < 6 * c.sr:
            continue
        a, seg = excerpt(y, c.sr, 5.0, rng)
        if c.sr != SR:
            seg = np.interp(np.arange(0, len(seg), c.sr / SR), np.arange(len(seg)), seg)
        queries.append((k, seg))
    # aliases: clips that contain the same audio as a query (some parts reuse a Variation's sound in another clip);
    # found from the clean query, any clip with at least 40% of the best vote count
    alias = {}
    for k, seg in queries:
        r = idx.query(seg, SR, top=5)
        best = r[0]["votes"] if r else 0
        alias[k] = {x["track"] for x in r if x["votes"] >= 0.4 * best} | {f"{k[0]}/{k[1]}"}
    for kind in rows:
        for snr in snrs:
            ok = 0
            for k, seg in queries:
                nz = rng.standard_normal(len(seg)) if kind == "white" else np.roll(noise, int(rng.integers(len(noise))))[: len(seg)]
                r = idx.query(at_snr(seg, nz, snr), SR)
                ok += bool(r and r[0]["track"] in alias[k])
            rows[kind].append(ok / len(queries))
    codec = []
    for kb in (64, 32, 16):
        ok = 0
        for k, seg in queries[::3]:
            r = idx.query(K.encode(seg, kb)["y"], SR)
            ok += bool(r and r[0]["track"] in alias[k])
        codec.append({"kbps": kb, "rate": ok / len(queries[::3])})
    # the demo: a query that behaves as the averages do (named at +10 and 0 dB, lost at -5), else the fourth
    def attempt(kq, segq):
        nz = noise[: len(segq)]
        out = []
        for snr in (10, 0, -5):
            r = idx.query(at_snr(segq, nz, snr), SR)
            out.append({"snr": snr, "found": r[0]["track"] if r else None, "votes": r[0]["votes"] if r else 0, "ok": bool(r and r[0]["track"] in alias[kq])})
        return out
    kq, segq = queries[3]
    named = attempt(kq, segq)
    for kk, sg in queries:
        trial = attempt(kk, sg)
        if [t["ok"] for t in trial] == [True, True, False]:
            kq, segq, named = kk, sg, trial
            break
    nz = noise[: len(segq)]
    three = concat([C(fade(at_snr(segq, nz, s_) / np.max(np.abs(at_snr(segq, nz, s_))) * 0.9)) for s_ in (10, 0, -5)], gap=0.7, names=["s10", "s0", "sm5"])
    k, seg = queries[5]
    coded = K.encode(seg, 16)["y"]
    cl = concat([C(fade(coded)), C(fade(seg))], gap=0.8, names=["first", "second"])
    n_alias = sum(1 for k in alias if len(alias[k]) > 1)
    return {"n_alias": n_alias, "snrs": snrs, "rates": rows, "codec": codec, "n": len(queries), "answer": "first", "named": named, "noise_truth": f"{kq[0]}/{kq[1]}",
            "starts": {"first": float(cl.events["first"]), "second": float(cl.events["second"])},
            "starts3": {k_: float(three.events[k_]) for k_ in ("s10", "s0", "sm5")},
            "clips": {"two": save("codec.two", cl, detail=f"five seconds of {k[1]} through Part 58's coder at 16 kbit/s, then as stored"),
                      "three": save("noise.three", three, detail=f"five seconds of {kq[1]} in a simulated noisy bar, the music 10 dB above the noise, level with it, and 5 dB below")}}


def compute_falsematch() -> dict:
    idx = index()
    lib = library()
    secs = sum(c.duration for c in lib.values())
    qh = int(len(F.fingerprint(np.random.default_rng(0).standard_normal(5 * F.SR_FP), F.SR_FP)))
    fm = F.false_match_rate(bits=24, query_hashes=400, db_hashes=idx.size, tracks=len(lib), offsets=int(secs / len(lib) * F.SR_FP / 256))
    # an empirical check: queries of pure noise, and of music the library does not contain
    rng = np.random.default_rng(11)
    top = []
    for s in range(20):
        r = idx.query(rng.standard_normal(5 * F.SR_FP) * 0.1, F.SR_FP)
        top.append(r[0]["votes"] if r else 0)
    true_votes = []
    for k in variations()[::6]:
        c = lib[k]
        _, seg = excerpt(mono(c), c.sr, 5.0, rng)
        r = idx.query(seg, c.sr)
        true_votes.append(r[0]["votes"] if r else 0)
    from videos.music.music38 import compute as P38
    from explainer.music.monochord import mix as MIX
    from explainer.music.monochord import tune as T
    MAJOR = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
    placed = [(P38.arr(P38.piano(74 + MAJOR[e["degree"]], e["dur"] * 0.95, 0.85)), e["t"], 0.0) for e in T.events(0.47, [0, 1])]
    fresh = MIX(placed).y
    fresh = fresh / np.max(np.abs(fresh)) * 0.9
    r_new = idx.query(fresh, SR)
    unk = C(fade(fresh))
    return {"fresh_top": r_new[:3], "model": {"chance_hits": fm["chance_hits"], "per_bin": fm["per_bin"], "tail": {str(k): v for k, v in fm["p_some_bin_at_least"].items()}},
            "noise_top_votes": top, "true_votes": true_votes, "db_hashes": idx.size, "noise_query_hashes": qh,
            "clips": {"one": save("unknown.one", unk, detail="a new rendering of the Tune's first two phrases on Part 38's piano, in D and at a tempo no earlier part used: the same song, a recording the library has never held")}}


def compute_horse() -> dict:
    """Two classes: Variations from Parts 1 to 30 and from Parts 31 to 60.  In the training set (and in the test set
    the builders checked against) every clip of the second class carries a faint 50 Hz mains hum with harmonics, as if
    recorded in another studio.  A classifier on the content embedding learns the hum."""
    lib = library()
    var = variations()
    rng = np.random.default_rng(5)
    X, y, Xc = [], [], []
    for k in var:
        c = lib[k]
        s = mono(c)
        if c.sr != SR:
            s = np.interp(np.arange(0, len(s), c.sr / SR), np.arange(len(s)), s)
        lab = int(int(k[0][5:]) > 30)
        for j in range(3):
            _, seg = excerpt(s, SR, 4.0, rng, loud=False)
            t = np.arange(len(seg)) / SR
            hum = sum(np.sin(2 * np.pi * 50 * h * t) / h for h in (1, 2, 3)) * np.std(seg) * 10 ** (-30 / 20)
            X.append(F.embed(seg + (hum if lab else 0), SR))
            Xc.append(F.embed(seg, SR))
            y.append(lab)
    X, Xc, y = np.array(X), np.array(Xc), np.array(y)
        # split by clip, not by excerpt: three excerpts of one clip are near neighbours, and must not sit on both sides
    clip_of = np.repeat(np.arange(len(y) // 3), 3)
    cperm = rng.permutation(len(y) // 3)
    test_clips = set(cperm[int(0.7 * len(cperm)):].tolist())
    te = np.array([i for i in range(len(y)) if clip_of[i] in test_clips])
    tr = np.array([i for i in range(len(y)) if clip_of[i] not in test_clips])
    mu, sd = X[tr].mean(axis=0), X[tr].std(axis=0) + 1e-9
    Z, Zc = (X - mu) / sd, (Xc - mu) / sd
    w = F.logistic(Z[tr], y[tr], l2=1e-3, iters=800)
    acc_hum = float(np.mean(F.logistic_predict(w, Z[te]) == y[te]))
    acc_clean = float(np.mean(F.logistic_predict(w, Zc[te]) == y[te]))
    clean_mu, clean_sd = Xc[tr].mean(axis=0), Xc[tr].std(axis=0) + 1e-9
    Zc = (Xc - clean_mu) / clean_sd
    w_clean = F.logistic(Zc[tr], y[tr], l2=1e-3, iters=800)
    acc_fair = float(np.mean(F.logistic_predict(w_clean, Zc[te]) == y[te]))
    # the same honest classifier, but split by excerpt, so that excerpts of one clip sit on both sides: a second leak
    ep = np.random.default_rng(55).permutation(len(y))
    etr, ete = ep[: int(0.7 * len(y))], ep[int(0.7 * len(y)):]
    leak_mu, leak_sd = Xc[etr].mean(axis=0), Xc[etr].std(axis=0) + 1e-9
    Zleak = (Xc - leak_mu) / leak_sd
    w_leak = F.logistic(Zleak[etr], y[etr], l2=1e-3, iters=800)
    acc_leaky = float(np.mean(F.logistic_predict(w_leak, Zleak[ete]) == y[ete]))
    base = float(max(np.mean(y[te]), 1 - np.mean(y[te])))
    blocks = {"band energies": slice(0, 24), "band spreads": slice(24, 48), "chroma": slice(48, 60), "flux": slice(60, 62)}
    def share(wv):
        a = np.abs(wv[1:])
        return {b: float(a[sl].sum() / a.sum()) for b, sl in blocks.items()}
    lowband = {"hum": float(np.abs(w[1:4]).sum() / np.abs(w[1:]).sum()), "fair": float(np.abs(w_clean[1:4]).sum() / np.abs(w_clean[1:]).sum())}
    top = np.argsort(-np.abs(w[1:]))[:3]
    names = [f"band {i}" if i < 24 else (f"band spread {i - 24}" if i < 48 else ("chroma" if i < 60 else "flux")) for i in top]
    k = var[-1]
    c = lib[k]
    s = mono(c)
    if c.sr != SR:
        s = np.interp(np.arange(0, len(s), c.sr / SR), np.arange(len(s)), s)
    _, seg = excerpt(s, SR, 5.0, np.random.default_rng(2))
    t = np.arange(len(seg)) / SR
    hum = sum(np.sin(2 * np.pi * 50 * h * t) / h for h in (1, 2, 3)) * np.std(seg) * 10 ** (-24 / 20)
    cl = concat([C(fade(seg)), C(fade(seg + hum))], gap=0.8, names=["first", "second"])
    return {"acc_hum": acc_hum, "acc_clean": acc_clean, "acc_fair": acc_fair, "top_features": names, "share_hum": share(w), "share_fair": share(w_clean), "acc_leaky": acc_leaky, "majority": base,
            "lowest_three_bands": lowband, "n": len(y), "answer": "second",
            "starts": {"first": float(cl.events["first"]), "second": float(cl.events["second"])},
            "clips": {"two": save("horse.two", cl, detail=f"five seconds of {k[1]}, then the same with a mains hum at 50, 100 and 150 Hz 24 dB down", needs="bass")}}


def embeddings():
    if "emb" in _L:
        return _L["emb"]
    lib = library()
    keys = sorted(lib)
    E = np.array([F.embed(mono(lib[k]), lib[k].sr) for k in keys])
    _L["emb"] = (keys, F.standardize(E))
    return _L["emb"]


def _world():
    """The simulated listeners: 500 users, 300 clips, tastes partly predictable from content; returns the generator too,
    so that what follows draws the same numbers whoever calls it."""
    keys, E = embeddings()
    rng = np.random.default_rng(0)
    n_items = 300
    items = rng.choice(len(keys), n_items, replace=False)
    Ei = E[items]
    # item tastes: partly predictable from content (a projection of the embedding), partly not
    k = 6
    W = rng.normal(0, 1, (E.shape[1], k)) / math.sqrt(E.shape[1])
    V = 0.9 * Ei @ W / (np.std(Ei @ W) + 1e-9) + 0.5 * rng.normal(0, 1, (n_items, k))
    n_users = 500
    U = rng.normal(0, 1, (n_users, k))
    pop = 0.4 * rng.normal(0, 1, n_items)
    A = U @ V.T / math.sqrt(k) + pop[None, :]
    P = np.exp(A - A.max(axis=1, keepdims=True))
    P /= P.sum(axis=1, keepdims=True)
    R = rng.poisson(40 * P)
    return keys, E, rng, n_items, items, Ei, n_users, R


def compute_recs() -> dict:
    keys, E, rng, n_items, items, Ei, n_users, R = _world()
    train, held = F.split(R, 0.2, seed=1)
    popularity = np.tile(train.sum(axis=0), (n_users, 1)).astype(float)
    fit = F.implicit_als(train, k=8, iters=8)
    S = fit["X"] @ fit["Y"].T
    rand = rng.random(R.shape)
    out = {"recall": {"random": F.recall_at_k(rand, held, train), "popular": F.recall_at_k(popularity, held, train), "als": F.recall_at_k(S, held, train)}}
    # cold start: 30 items nobody has played; score them from content, via a regression from embedding to learnt factors
    cold = rng.choice(n_items, 30, replace=False)
    warm = np.setdiff1d(np.arange(n_items), cold)
    tr2 = train.copy()
    tr2[:, cold] = 0
    fit2 = F.implicit_als(tr2, k=8, iters=8)
    B, *_ = np.linalg.lstsq(np.c_[np.ones(len(warm)), Ei[warm]], fit2["Y"][warm], rcond=None)
    Yc = fit2["Y"].copy()
    Yc[cold] = np.c_[np.ones(len(cold)), Ei[cold]] @ B
    S2 = fit2["X"] @ Yc.T
    heldc = np.zeros_like(R)
    heldc[:, cold] = R[:, cold]
    only_cold = np.full(R.shape, -np.inf)
    only_cold[:, cold] = S2[:, cold]
    rand_c = np.full(R.shape, -np.inf)
    rand_c[:, cold] = rng.random((n_users, len(cold)))
    out["cold"] = {"content": F.recall_at_k(only_cold, heldc, np.zeros_like(R), k=5), "random": F.recall_at_k(rand_c, heldc, np.zeros_like(R), k=5), "n": len(cold)}
    out["users"], out["items"], out["plays"] = n_users, n_items, int(R.sum())
    # a listener's top three, heard
    u = int(np.argmax(R.sum(axis=1)))
    top3 = [int(i) for i in np.argsort(-np.where(train[u] > 0, -np.inf, S[u]))[:3]]
    lib = library()
    segs, names = [], []
    for j, i in enumerate(top3):
        kk = keys[items[i]]
        c = lib[kk]
        s = mono(c)
        if c.sr != SR:
            s = np.interp(np.arange(0, len(s), c.sr / SR), np.arange(len(s)), s)
        _, seg = excerpt(s, SR, 4.0, np.random.default_rng(j))
        segs.append(C(fade(seg / (np.max(np.abs(seg)) + 1e-9) * 0.9)))
        names.append(f"{kk[0]}/{kk[1]}")
    cl = concat(segs, gap=0.6, names=["one", "two", "three"])
    ci = int(cold[0])
    dist = np.linalg.norm(Ei[warm] - Ei[ci], axis=1)
    near = int(warm[int(np.argmin(dist))])
    pair = []
    for j, i in enumerate((ci, near)):
        kk = keys[items[i]]
        c = lib[kk]
        s = mono(c)
        if c.sr != SR:
            s = np.interp(np.arange(0, len(s), c.sr / SR), np.arange(len(s)), s)
        _, seg = excerpt(s, SR, 4.0, np.random.default_rng(20 + j))
        pair.append(C(fade(seg / (np.max(np.abs(seg)) + 1e-9) * 0.9)))
    cold_clip = concat(pair, gap=0.8, names=["cold", "near"])
    out["cold_pair"] = [f"{keys[items[ci]][0]}/{keys[items[ci]][1]}", f"{keys[items[near]][0]}/{keys[items[near]][1]}"]
    out["cold_starts"] = {k_: float(cold_clip.events[k_]) for k_ in ("cold", "near")}
    out["top3"] = names
    out["starts"] = {k_: float(cl.events[k_]) for k_ in ("one", "two", "three")}
    out["clips"] = {"three": save("recs.three", cl, detail="four seconds each of the three clips the recommender suggests to one simulated listener"),
                    "cold": save("cold.two", cold_clip, detail="a clip no simulated listener has played, then the played clip whose content it most resembles")}
    return out


def compute_loop() -> dict:
    a = F.feedback_loop(explore=0.0, seed=1)
    b = F.feedback_loop(explore=0.3, seed=1)
    return {"gini": a["gini"], "gini_explore": b["gini"], "gini_own": a["gini_own"], "top1": a["top1"], "top1_explore": b["top1"], "top1_own": a["top1_own"]}


def compute_playlist() -> dict:
    lib = library()
    var = variations()
    keys, E = embeddings()
    pos = {k: i for i, k in enumerate(keys)}
    X = E[[pos[k] for k in var]]
    order = F.playlist(X, start=0)
    rng = np.random.default_rng(3)
    rand = [0] + list(rng.permutation(np.arange(1, len(var))))
    L_smooth, L_rand = F.path_length(X, order), F.path_length(X, rand)

    def snippets(seq, n=6):
        out = []
        for j, i in enumerate(seq[:n]):
            c = lib[var[i]]
            s = mono(c)
            if c.sr != SR:
                s = np.interp(np.arange(0, len(s), c.sr / SR), np.arange(len(s)), s)
            _, seg = excerpt(s, SR, 2.5, np.random.default_rng(10 + j))
            out.append(seg / (np.max(np.abs(seg)) + 1e-9) * 0.9)
        y = np.concatenate([fade(z, 0.01, 0.15) for z in out])
        return y
    cl = concat([C(fade(snippets(rand))), C(fade(snippets(order)))], gap=1.0, names=["first", "second"])
    return {"order": [f"{var[i][1][14:]}" for i in order], "random": [f"{var[i][1][14:]}" for i in rand], "length_smooth": L_smooth,
            "length_random": L_rand, "answer": "second", "starts": {"first": float(cl.events["first"]), "second": float(cl.events["second"])},
            "clips": {"two": save("playlist.two", cl, detail="six Variations, two and a half seconds each, in a random order, then in the order a playlist builder chose so that neighbours sound alike")}}


def compute_tune63() -> dict:
    lib = library()
    idx = index()
    var = variations()
    rng = np.random.default_rng(63)
    picks = [var[int(i)] for i in rng.choice(len(var), 3, replace=False)]
    segs, found = [], []
    for j, k in enumerate(picks):
        c = lib[k]
        s = mono(c)
        if c.sr != SR:
            s = np.interp(np.arange(0, len(s), c.sr / SR), np.arange(len(s)), s)
        a, seg = excerpt(s, SR, 5.0, rng)
        q = at_snr(seg, bar_noise(5.0, seed=20 + j), 3.0)
        r = idx.query(q, SR)
        found.append({"truth": f"{k[0]}/{k[1]}", "found": r[0]["track"] if r else None, "votes": r[0]["votes"] if r else 0,
                      "offset_s": r[0]["offset_s"] if r else None, "true_offset_s": a / SR})
        segs.append(C(fade(q / np.max(np.abs(q)) * 0.9)))
    cl = concat(segs, gap=0.8, names=["one", "two", "three"])
    return {"found": found, "names": ["one", "two", "three"], "seconds": cl.duration, "starts": {k: float(cl.events[k]) for k in ("one", "two", "three")},
            "clips": {"variation63": save("tune.variation63", cl, detail="Variation 63: five seconds each of three earlier Variations in a simulated noisy bar, music 3 dB above the noise, each to be named by the fingerprinter")}}


def compute_variation() -> dict:
    t = load("tune63")
    ok = sum(1 for f in t["found"] if f["found"] == f["truth"])
    return {"part": 63, "title": "three earlier Variations, five noisy seconds each, named", "seconds": round(t["seconds"], 1),
            "measure": f"{ok} of 3 named, against every clip of Parts 1 to 60",
            "clip": "tune.variation63"}

# ---------------------------------------------------------------------------------------------- pictures and sweeps
def _queries(seconds=5.0, seed=7):
    lib = library()
    rng = np.random.default_rng(seed)
    out = []
    for k in variations():
        c = lib[k]
        y = mono(c)
        if len(y) < (seconds + 1) * c.sr:
            continue
        a, seg = excerpt(y, c.sr, seconds, rng)
        if c.sr != SR:
            seg = np.interp(np.arange(0, len(seg), c.sr / SR), np.arange(len(seg)), seg)
        out.append((k, seg))
    return out


def _aliases(idx, queries):
    al = {}
    for k, seg in queries:
        r = idx.query(seg, SR, top=5)
        best = r[0]["votes"] if r else 0
        al[k] = {x["track"] for x in r if x["votes"] >= 0.4 * best} | {f"{k[0]}/{k[1]}"}
    return al


def compute_matches() -> dict:
    """Wang's picture: the hashes a noisy query shares with the true recording fall on a line; with another, they scatter."""
    lib = library()
    idx = index()
    k = variations()[10]
    c = lib[k]
    y = mono(c)
    a, seg = excerpt(y, c.sr, 5.0, np.random.default_rng(9))
    q = at_snr(seg, bar_noise(5.0, seed=5), 0.0)
    r = idx.query(q, c.sr, top=3)
    true = f"{k[0]}/{k[1]}"
    other = next(x["track"] for x in r if x["track"] != true) if len(r) > 1 else variations()[11]
    m_true = idx.matches(q, c.sr, true)
    m_other = idx.matches(q, c.sr, other)
    hop = 256 / F.SR_FP
    d_true = (m_true[:, 1] - m_true[:, 0]) * hop
    d_other = (m_other[:, 1] - m_other[:, 0]) * hop
    return {"truth": true, "other": other, "offset_s": a / c.sr, "true": (m_true * hop).tolist(), "wrong": (m_other * hop).tolist(),
            "diff_true": d_true.tolist(), "diff_other": d_other.tolist(), "track_seconds": c.duration, "result": r}


def compute_length() -> dict:
    """How long must a query be?  Recognition against the length of the excerpt, in bar noise level with the music."""
    idx = index()
    qs = _queries(10.0, seed=13)
    al = _aliases(idx, qs)
    rng = np.random.default_rng(3)
    noise = bar_noise(11.0, seed=8)
    lens = [1.0, 2.0, 3.0, 5.0, 8.0]
    out = {"0": [], "-5": []}
    for snr in (0, -5):
        for L in lens:
            ok = 0
            for k, seg in qs:
                n = int(L * SR)
                st = int(rng.integers(0, len(seg) - n))
                nz = np.roll(noise, int(rng.integers(len(noise))))[:n]
                r = idx.query(at_snr(seg[st:st + n], nz, snr), SR)
                ok += bool(r and r[0]["track"] in al[k])
            out[str(snr)].append(ok / len(qs))
    return {"lengths": lens, "rates": out, "n": len(qs)}


def compute_speed() -> dict:
    """Played a little fast (pitch and tempo together, as a sped-up tape or radio edit): every peak moves, so do the hashes."""
    idx = index()
    qs = _queries(6.0, seed=17)
    al = _aliases(idx, qs)
    pct = [0.0, 0.5, 1.0, 2.0, 4.0, 8.0]
    rates = []
    for p_ in pct:
        f = 1 + p_ / 100
        ok = 0
        for k, seg in qs:
            y = np.interp(np.arange(0, len(seg) - 1, f), np.arange(len(seg)), seg)[: int(5 * SR)]
            r = idx.query(y, SR)
            ok += bool(r and r[0]["track"] in al[k])
        rates.append(ok / len(qs))
    k, seg = qs[4]
    y4 = np.interp(np.arange(0, len(seg) - 1, 1.04), np.arange(len(seg)), seg)[: int(5 * SR)]
    r4 = idx.query(y4, SR)
    r0 = idx.query(seg[: int(5 * SR)], SR)
    cl = concat([C(fade(seg[: int(5 * SR)])), C(fade(y4))], gap=0.8, names=["as stored", "fast"])
    return {"percent": pct, "rates": rates, "n": len(qs), "truth": f"{k[0]}/{k[1]}", "votes_fast": r4[0]["votes"] if r4 else 0,
            "found_fast": r4[0]["track"] if r4 else None, "votes_stored": r0[0]["votes"] if r0 else 0,
            "starts": {"stored": float(cl.events["as stored"]), "fast": float(cl.events["fast"])},
            "clips": {"two": save("speed.two", cl, detail=f"five seconds of {k[1]} as stored, then played 4 per cent fast, pitch and tempo together")}}


def compute_map() -> dict:
    """Every clip's content embedding, projected onto its two principal components, coloured by act; the playlist's path."""
    keys, E = embeddings()
    Ec = E - E.mean(axis=0)
    U, s_, Vt = np.linalg.svd(Ec, full_matrices=False)
    P = Ec @ Vt[:2].T
    P = P / np.abs(P).max(axis=0)
    part = np.array([int(k[0][5:]) for k in keys])
    var = variations()
    pos = {k: i for i, k in enumerate(keys)}
    vi = [pos[k] for k in var]
    order = F.playlist(E[vi], start=0)
    explained = (s_[:2] ** 2 / np.sum(s_ ** 2)).tolist()
    return {"xy": P.tolist(), "part": part.tolist(), "explained": explained, "var_xy": P[vi].tolist(),
            "order": [int(i) for i in order]}


def compute_matrix() -> dict:
    """The listeners' play matrix as a picture: users by clips, both sorted by total plays; and how sparse it is."""
    keys, E, rng, n_items, items, Ei, n_users, R = _world()
    ru = np.argsort(-R.sum(axis=1))
    ri = np.argsort(-R.sum(axis=0))
    M = R[ru][:, ri]
    fit = F.implicit_als(R, k=8, iters=8)
    S = fit["X"] @ fit["Y"].T
    return {"R": np.log1p(M[::2, :]).tolist(), "S": S[ru][:, ri][::2, :].tolist(), "nonzero": float(np.mean(R > 0)),
            "plays": int(R.sum()), "users": n_users, "items": n_items, "max": int(R.max())}


def compute_lorenz() -> dict:
    """Who gets the plays: Lorenz curves after thirty rounds, with the popularity recommender, with exploring, and on
    their own."""
    a = F.feedback_loop(explore=0.0, seed=1)
    b = F.feedback_loop(explore=0.3, seed=1)
    def lor(x):
        x = np.sort(np.asarray(x, float))
        c = np.r_[0, np.cumsum(x)] / x.sum()
        return c[:: max(1, len(c) // 100)].tolist() + [1.0]
    top10 = lambda x: float(np.sort(x)[::-1][: max(1, len(x) // 10)].sum() / np.sum(x))
    return {"rec": lor(a["plays"]), "explore": lor(b["plays"]), "own": lor(a["own"]),
            "top10": {"rec": top10(a["plays"]), "explore": top10(b["plays"]), "own": top10(a["own"])}}


def compute_neighbours() -> dict:
    """One clip, its two nearest neighbours in the content embedding and its farthest, three seconds each (an ear question)."""
    lib = library()
    keys, E = embeddings()
    var = variations()
    pos = {k: i for i, k in enumerate(keys)}
    i0 = pos[var[20]]
    dist = np.linalg.norm(E - E[i0], axis=1)
    order = np.argsort(dist)
    near = [int(j) for j in order[1:] if keys[j][0] != keys[i0][0]][:2]          # from other parts
    far = int(order[-1])
    seq = [i0, near[0], far, near[1]]
    segs = []
    for j, i in enumerate(seq):
        c = lib[keys[i]]
        s = mono(c)
        if c.sr != SR:
            s = np.interp(np.arange(0, len(s), c.sr / SR), np.arange(len(s)), s)
        _, seg = excerpt(s, SR, 3.0, np.random.default_rng(30 + j))
        segs.append(C(fade(seg / (np.max(np.abs(seg)) + 1e-9) * 0.9)))
    cl = concat(segs, gap=0.8, names=["start", "a", "b", "c"])
    return {"names": [f"{keys[i][0]}/{keys[i][1]}" for i in seq], "dist": [float(dist[i]) for i in seq], "answer": "b",
            "median_dist": float(np.median(dist)), "starts": {k: float(cl.events[k]) for k in ("start", "a", "b", "c")},
            "clips": {"four": save("neighbours.four", cl, detail="three seconds of a Variation, then its two nearest neighbours in the content embedding from other parts and, between them, its farthest, in the order near, far, near")}}


def compute_scale() -> dict:
    """The chance of a false match as the library grows from this series to a hundred million tracks."""
    lib = library()
    idx = index()
    per_track = idx.size / len(lib)
    secs = sum(c.duration for c in lib.values()) / len(lib)
    rows = []
    for tracks in (908, 10_000, 1_000_000, 100_000_000):
        tr = len(lib) if tracks == 908 else tracks
        fm = F.false_match_rate(bits=24, query_hashes=400, db_hashes=int(per_track * tr * 200 / secs), tracks=tr, offsets=int(200 * F.SR_FP / 256))
        rows.append({"tracks": tr, "hashes": per_track * tr * 200 / secs, "chance_hits": fm["chance_hits"],
                     "tail": {str(k): v for k, v in fm["p_some_bin_at_least"].items()}})
    return {"rows": rows, "per_second": per_track / secs, "bytes_per_hash": 8}


def compute_sampled() -> dict:
    """A Variation used as a sample: five seconds of it under five seconds of another clip, at several levels.  Does the
    fingerprinter find the sample, and the track on top?  (What Content ID and sample-spotting must do.)"""
    idx = index()
    lib = library()
    qs = _queries(6.0, seed=23)
    al = _aliases(idx, qs)
    rng = np.random.default_rng(29)
    levels = [0, -6, -12, -18]
    found_s, found_both = [], []
    for lv in levels:
        ok_s = ok_b = 0
        for j, (k, seg) in enumerate(qs):
            k2, top = qs[(j + 7) % len(qs)]
            n = int(5 * SR)
            a_, b_ = seg[:n], top[:n]
            q = b_ / np.std(b_) + a_ / np.std(a_) * 10 ** (lv / 20)
            r = idx.query(q, SR, top=10)
            names = [x["track"] for x in r if x["votes"] >= 8]
            hit_s = any(t in al[k] for t in names)
            ok_s += hit_s
            ok_b += hit_s and any(t in al[k2] for t in names)
        found_s.append(ok_s / len(qs))
        found_both.append(ok_b / len(qs))
    k, seg = qs[2]
    k2, top = qs[9]
    n = int(5 * SR)
    q = top[:n] / np.std(top[:n]) + seg[:n] / np.std(seg[:n]) * 10 ** (-12 / 20)
    r = idx.query(q, SR, top=5)
    cl = concat([C(fade(seg[:n] / np.max(np.abs(seg[:n])) * 0.9)), C(fade(q / np.max(np.abs(q)) * 0.9))], gap=0.8, names=["sample", "track"])
    return {"levels": levels, "sample_found": found_s, "both_found": found_both, "n": len(qs), "demo": r,
            "demo_truth": [f"{k[0]}/{k[1]}", f"{k2[0]}/{k2[1]}"], "starts": {"sample": float(cl.events["sample"]), "track": float(cl.events["track"])},
            "clips": {"two": save("sampled.two", cl, detail=f"five seconds of {k[1]}, then the same five seconds 12 dB under {k2[1]}, as a sample inside another track")}}


def compute_hum() -> dict:
    """Query by humming: the Tune's opening sung slower, in another key and a little out of tune.  The fingerprint finds
    nothing; a pitch contour, matched by time warping, picks the Tune out of thirty melodies."""
    from explainer.music.monochord import tune as T
    from explainer.music.monochord.mir import transcribe as TR
    MAJOR = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
    rng = np.random.default_rng(61)
    ev = T.events(0.62, [0, 1])
    notes = [(63 + MAJOR[e["degree"]] + float(rng.normal(0, 0.25)), e["t"], e["dur"] * 0.92) for e in ev]
    y = CH.sing(notes, "alto", "u", seed=3)
    y = y / np.max(np.abs(y)) * 0.9
    p = TR.yin(y, SR, fmin=100, fmax=800)
    voiced = (np.asarray(p["aperiodicity"]) < 0.2) & (np.asarray(p["f0"]) > 0)
    q = F.contour(p["f0"], voiced)

    def ref(degrees_durs, fps=25):
        out = []
        for d, du in degrees_durs:
            out += [d] * max(1, int(round(du * fps)))
        return np.array(out, float)
    cands = {"the Tune": ref([(MAJOR[e["degree"]], e["dur"]) for e in T.events(0.5, [0, 1])]),
             "the Tune's middle": ref([(MAJOR[e["degree"]], e["dur"]) for e in T.events(0.5, [2, 3])])}
    durs = [e["dur"] for e in T.events(0.5, [0, 1])]
    scale = [0, 2, 4, 5, 7, 9, 11, 12, 14]
    for k in range(28):
        i, seq = 4, []
        for du in rng.permutation(durs):
            i = int(np.clip(i + rng.choice([-2, -1, -1, 0, 1, 1, 2]), 0, len(scale) - 1))
            seq.append((scale[i], du))
        cands[f"melody {k + 1}"] = ref(seq)
    dist = {k: F.melody_distance(q, v) for k, v in cands.items()}
    ranked = sorted(dist, key=dist.get)
    idx = index()
    r = idx.query(y, SR)
    c = C(fade(y))
    return {"dist": dist, "ranked": ranked[:5], "rank_of_tune": ranked.index("the Tune") + 1, "n": len(cands),
            "fingerprint": r[:2], "contour": q.tolist(), "tune_ref": cands["the Tune"].tolist(),
            "clips": {"one": save("hum.one", c, kind="synthesized", detail="the Tune's first two phrases sung on 'oo' by Part 8's alto voice, slower, three semitones up and a little out of tune: a hummed query")}}


def compute_lengthpair() -> dict:
    """One noisy query at one second and at eight, heard, each sent to the index."""
    idx = index()
    k, seg = _queries(10.0, seed=13)[6]
    al = _aliases(idx, [(k, seg)])[k]
    noise = bar_noise(9.0, seed=8)
    out, segs = {}, []
    for name, L in (("one", 1.0), ("eight", 8.0)):
        n = int(L * SR)
        q = at_snr(seg[:n], noise[:n], 0.0)
        r = idx.query(q, SR)
        out[name] = {"found": r[0]["track"] if r else None, "votes": r[0]["votes"] if r else 0, "ok": bool(r and r[0]["track"] in al)}
        segs.append(C(fade(q / np.max(np.abs(q)) * 0.9)))
    cl = concat(segs, gap=0.8, names=["one", "eight"])
    return {"truth": f"{k[0]}/{k[1]}", **out, "starts": {x: float(cl.events[x]) for x in ("one", "eight")},
            "clips": {"two": save("length.two", cl, detail=f"one second, then eight seconds, of {k[1]} level with a simulated bar's noise")}}



def compute_signoff() -> dict:
    """The part's last sound: the opening of its Variation, under the next part's title."""
    load("variation")
    return signoff(CLIPS, "tune.variation63", 63)


ITEMS = {"library": compute_library, "hook": compute_hook, "constellation": compute_constellation, "robust": compute_robust,
         "falsematch": compute_falsematch, "horse": compute_horse, "recs": compute_recs, "loop": compute_loop,
         "playlist": compute_playlist, "tune63": compute_tune63, "variation": compute_variation,
         "matches": compute_matches, "length": compute_length, "speed": compute_speed, "map": compute_map, "matrix": compute_matrix,
         "lorenz": compute_lorenz, "neighbours": compute_neighbours, "scale": compute_scale,
         "sampled": compute_sampled, "hum": compute_hum, "lengthpair": compute_lengthpair,
         "signoff": compute_signoff}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
