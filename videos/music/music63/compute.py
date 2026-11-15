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
from explainer.music.monochord.partkit import saver

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
    kq, segq = queries[3]
    nz = noise[: len(segq)]
    named = []
    for snr in (10, 0, -5):
        r = idx.query(at_snr(segq, nz, snr), SR)
        named.append({"snr": snr, "found": r[0]["track"] if r else None, "votes": r[0]["votes"] if r else 0, "ok": bool(r and r[0]["track"] in alias[kq])})
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
    mu, sd = X.mean(axis=0), X.std(axis=0) + 1e-9
    Z, Zc = (X - mu) / sd, (Xc - mu) / sd
    perm = rng.permutation(len(y))
    tr, te = perm[: int(0.7 * len(y))], perm[int(0.7 * len(y)):]
    w = F.logistic(Z[tr], y[tr], l2=1e-3, iters=800)
    acc_hum = float(np.mean(F.logistic_predict(w, Z[te]) == y[te]))
    acc_clean = float(np.mean(F.logistic_predict(w, Zc[te]) == y[te]))
    w_clean = F.logistic(Zc[tr], y[tr], l2=1e-3, iters=800)
    acc_fair = float(np.mean(F.logistic_predict(w_clean, Zc[te]) == y[te]))
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
    return {"acc_hum": acc_hum, "acc_clean": acc_clean, "acc_fair": acc_fair, "top_features": names, "n": len(y), "answer": "second",
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


def compute_recs() -> dict:
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


ITEMS = {"library": compute_library, "hook": compute_hook, "constellation": compute_constellation, "robust": compute_robust,
         "falsematch": compute_falsematch, "horse": compute_horse, "recs": compute_recs, "loop": compute_loop,
         "playlist": compute_playlist, "tune63": compute_tune63, "variation": compute_variation}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
