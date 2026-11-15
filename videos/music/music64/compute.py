"""Precompute everything numerical, and every sound, in Part 64 of *Music, Built* ("Source Separation").

    python -m videos.music.music64.compute              # everything missing (a few minutes: the network trains)
    python -m videos.music.music64.compute --force hook

Numbers are cached in ``.cache/music64/<name>.json``, sounds in ``.cache/music64/audio/``.  The tools are Monochord's
separators (``explainer/music/monochord/mir/separate.py``).  The music is Part 56's session, whose every stem Monochord
mixed itself: vocals, bass, drums (kick, snare, hi-hat) and other (piano, guitar), as in the MUSDB18 benchmark.  The
separators learn from the session's later phrases and are tested on its first two.

Items:
    hook        an ear question: a voice and a piano recorded on one track; the voice as recorded alone, and as separated
    pan         stereo: centre cancellation, and the piano and guitar picked out by where they are panned
    ica         independent components: a dry two-channel mixture, then the same in a room
    hpss        harmonic against percussive, by median filtering
    nmf         supervised NMF with templates for each stem, learnt from other phrases
    oracle      the ideal binary and ratio masks, and the true phase: the bounds
    phase       a magnitude with the mixture's phase, with Griffin-Lim's, and with the truth's
    net         a small network that predicts the vocal mask, trained on other phrases
    metrics     two estimates with the same SDR, one leaking another instrument, one full of artifacts
    tune64      Variation 64: an a cappella and a karaoke version, from separated stems and from true ones
    variation   the Variations ledger, row 64
    panmap      every bin's panning index, and the energy at each index
    icascatter  the mixture as a cloud of points before and after unmixing; kurtosis along every direction
    hpsssweep   the median filters' length and the masks' power against the split's SDR
    nmfrank     NMF's templates for voice and drums; vocal SDR against the number of templates
    maskimg     the vocals' ideal binary, ideal ratio and network masks as pictures
    glcurve     Griffin-Lim's inconsistency and SDR, iteration by iteration
    gain        SDR and SI-SDR for a perfect estimate made quieter, inverted, dull or late (three of them heard)
    netleak     the same network trained on stretches that repeat or include the test phrases: what a leak is worth
    meet        the test set heard: each stem alone, then the mixture
    remix       vocals up 6 dB and drums down 6 dB, from separated stems and from the true ones
    hpssknob    the percussive half with short and with long median filters, heard
    truephase   the ideal ratio mask with the mixture's phase and with the vocals' own, heard
"""

from __future__ import annotations

import numpy as np
from scipy.signal import fftconvolve

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat
from explainer.music.monochord import space as SP
from explainer.music.monochord.mir import separate as S
from explainer.music.monochord.partkit import saver
from videos.music.music56 import compute as P56

CACHE = Cache("music64")
CLIPS = ClipStore("music64")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
STEMS = ("vocals", "bass", "drums", "other")


def C(y) -> Clip:
    return Clip(np.asarray(y, float), SR)


def fade(y, a=0.005, r=0.08):
    y = np.array(y, float)
    ka, kr = max(int(a * SR), 1), max(int(r * SR), 1)
    y[:ka] *= np.linspace(0, 1, ka)[:, None] if y.ndim == 2 else np.linspace(0, 1, ka)
    y[len(y) - kr:] *= np.linspace(1, 0, kr)[:, None] if y.ndim == 2 else np.linspace(1, 0, kr)
    return y


_S: dict = {}


def stems(phrases=(0, 1)) -> dict:
    """Part 56's session as four stems (mono), at the session's own levels."""
    key = tuple(phrases)
    if key in _S:
        return _S[key]
    tr = P56.session(key)["tracks"]
    out = {"vocals": tr["vox"], "bass": tr["bass"], "drums": tr["kick"] + tr["snare"] + tr["hat"], "other": tr["piano"] + tr["guitar"]}
    g = 0.9 / np.max(np.abs(sum(out.values())))
    _S[key] = {k: v * g for k, v in out.items()}
    return _S[key]


def stereo(phrases=(0, 1)):
    """The session panned as on Part 56's stage, by a constant-power law."""
    tr = P56.session(tuple(phrases))["tracks"]
    L = np.zeros(len(tr["vox"]))
    R = np.zeros(len(tr["vox"]))
    for k in P56.TRACKS:
        th = (np.pi / 4) * (1 + P56.STAGE[k] / 90)          # 45 degrees: centre; +90: hard left
        L += np.sin(th) * tr[k]
        R += np.cos(th) * tr[k]
    g = 0.9 / max(np.max(np.abs(L)), np.max(np.abs(R)))
    return L * g, R * g, tr, g


def mix(st):
    return sum(st.values())


def scores(true: dict, est: dict) -> dict:
    return {k: S.sdr(true[k], est[k]) for k in est}


# ---------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    st = stems((0, 1))
    voice, piano = st["vocals"], 0.8 * P56.session((0, 1))["tracks"]["piano"] * 0.9 / np.max(np.abs(mix(st)))
    x = voice + piano
    train = stems((2, 3))
    tr_piano = 0.8 * P56.session((2, 3))["tracks"]["piano"] * 0.9 / np.max(np.abs(mix(train)))
    est = S.nmf_separate(x, {"voice": train["vocals"], "piano": tr_piano}, rank=16)
    sep = est["voice"]
    c = concat([C(fade(x)), C(fade(sep / np.max(np.abs(sep)) * 0.9)), C(fade(voice / np.max(np.abs(voice)) * 0.9))], gap=0.8, names=["mix", "first", "second"])
    return {"sdr": S.sdr(voice, sep), "answer": "first", "starts": {k: float(c.events[k]) for k in ("mix", "first", "second")},
            "clips": {"three": save("hook.three", c, detail="Part 8's voice and Part 38's piano on one track; then the voice separated from it by NMF; then the voice as recorded alone")}}


def compute_pan() -> dict:
    L, R, tr, gain = stereo((0, 1))
    side = S.centre_cancel(L, R)
    def index(deg):
        th = (np.pi / 4) * (1 + deg / 90)
        return (np.sin(th) - np.cos(th)) / (np.sin(th) + np.cos(th)), (np.sin(th) + np.cos(th)) / 2
    ip, gp = index(P56.STAGE["piano"])
    ig, _ = index(P56.STAGE["guitar"])
    piano_est, guitar_est = S.pan_masks(L, R, centres=[ip, ig], width=0.2)
    sdr_p = S.sdr(gp * gain * tr["piano"], piano_est)
    centre_left = float(np.sqrt(np.mean(side ** 2)) / np.sqrt(np.mean(((L + R) / 2) ** 2)))
    c = concat([C(fade(np.stack([L, R], axis=1))), C(fade(side / np.max(np.abs(side)) * 0.9)), C(fade(piano_est / np.max(np.abs(piano_est)) * 0.9))],
               gap=0.8, names=["stereo", "side", "piano"])
    return {"side_level_db": 20 * np.log10(centre_left), "sdr_piano": sdr_p, "starts": {k: float(c.events[k]) for k in ("stereo", "side", "piano")},
            "clips": {"three": save("pan.three", c, detail="Part 56's session in stereo; then left minus right, where the centred voice, bass and drums cancel; then the bins panned where the piano is", needs="headphones")}}


def compute_ica() -> dict:
    st = stems((0, 1))
    a, b = st["vocals"], st["other"]
    A = np.array([[0.9, 0.35], [0.4, 0.85]])
    X = A @ np.array([a, b])
    r = S.fastica(X)

    def best(sig, S_):
        return max(abs(np.corrcoef(s, sig)[0, 1]) for s in S_)
    dry = {"vocals": best(a, r["S"]), "other": best(b, r["S"])}
    room = SP.noise_tail(1.0, 1.2, seed=3, stereo=True, start=0.01)
    Xr = np.array([fftconvolve(X[0], room[:, 0])[: len(a)] + 0.3 * fftconvolve(X[1], room[:, 1])[: len(a)],
                   fftconvolve(X[1], room[:, 1])[: len(a)] + 0.3 * fftconvolve(X[0], room[:, 0])[: len(a)]])
    rr = S.fastica(Xr)
    wet = {"vocals": best(a, rr["S"]), "other": best(b, rr["S"])}
    k = int(np.argmax([abs(np.corrcoef(s, a)[0, 1]) for s in r["S"]]))
    v = r["S"][k] * np.sign(np.corrcoef(r["S"][k], a)[0, 1])
    k2 = int(np.argmax([abs(np.corrcoef(s, a)[0, 1]) for s in rr["S"]]))
    v2 = rr["S"][k2] * np.sign(np.corrcoef(rr["S"][k2], a)[0, 1])
    c = concat([C(fade(v / np.max(np.abs(v)) * 0.9)), C(fade(v2 / np.max(np.abs(v2)) * 0.9))], gap=0.8, names=["dry", "room"])
    return {"dry": dry, "room": wet, "starts": {k_: float(c.events[k_]) for k_ in ("dry", "room")},
            "clips": {"two": save("ica.two", c, detail="the voice as ICA recovers it from a dry two-channel mixture of voice and piano, then from the same mixture in a room")}}


def compute_hpss() -> dict:
    st = stems((0, 1))
    x = mix(st)
    r = S.hpss(x)
    tone = st["vocals"] + st["bass"] + st["other"]
    c = concat([C(fade(r["harmonic"] / np.max(np.abs(r["harmonic"])) * 0.9)), C(fade(r["percussive"] / np.max(np.abs(r["percussive"])) * 0.9))], gap=0.8, names=["harmonic", "percussive"])
    M = r["mask"]
    return {"sdr_drums": S.sdr(st["drums"], r["percussive"]), "sdr_tonal": S.sdr(tone, r["harmonic"]), "mask": M[:200:2, ::2].tolist(),
            "starts": {k: float(c.events[k]) for k in ("harmonic", "percussive")},
            "clips": {"two": save("hpss.two", c, detail="Part 56's session split by median filtering: the harmonic part, then the percussive part")}}


def compute_nmf() -> dict:
    st = stems((0, 1))
    x = mix(st)
    train = stems((2, 3))
    est = S.nmf_separate(x, train, rank=12)
    sc = scores(st, est)
    v = est["vocals"]
    c = C(fade(v / np.max(np.abs(v)) * 0.9))
    return {"sdr": sc, "clips": {"vocals": save("nmf.vocals", c, detail="the vocal stem of Part 56's session as supervised NMF separates it, with templates learnt from other phrases")}}


def compute_oracle() -> dict:
    st = stems((0, 1))
    o = S.oracle_masks(st)
    res = {m: scores(st, o[m]) for m in ("ibm", "irm", "true_phase")}
    segs = [C(fade(o["ibm"]["vocals"] / np.max(np.abs(o["ibm"]["vocals"])) * 0.9)), C(fade(o["irm"]["vocals"] / np.max(np.abs(o["irm"]["vocals"])) * 0.9)),
            C(fade(st["vocals"] / np.max(np.abs(st["vocals"])) * 0.9))]
    c = concat(segs, gap=0.8, names=["ibm", "irm", "true"])
    return {"sdr": res, "starts": {k: float(c.events[k]) for k in ("ibm", "irm", "true")},
            "clips": {"three": save("oracle.three", c, detail="the session's vocals through the ideal binary mask, the ideal ratio mask, and as recorded")}}


def compute_phase() -> dict:
    st = stems((0, 1))
    x = mix(st)
    X = S.stft(x)
    V = S.stft(st["vocals"])
    mag = np.abs(V)
    with_mix = S.istft(mag * np.exp(1j * np.angle(X)), len(x))
    gl = S.griffin_lim(mag, len(x), iters=60)
    true = st["vocals"]
    c = concat([C(fade(gl / np.max(np.abs(gl)) * 0.9)), C(fade(with_mix / np.max(np.abs(with_mix)) * 0.9))], gap=0.8, names=["griffin", "mixphase"])
    return {"sdr": {"mixture_phase": S.sdr(true, with_mix), "griffin_lim": S.sdr(true, gl), "si_griffin": S.si_sdr(true, gl), "si_mix": S.si_sdr(true, with_mix)},
            "starts": {k: float(c.events[k]) for k in ("griffin", "mixphase")},
            "clips": {"two": save("phase.two", c, detail="the vocals' true magnitude with a phase invented by Griffin and Lim's method, then with the mixture's phase")}}


_N: dict = {}


def network():
    """The vocal-mask network, trained once and kept in ``.cache/music64/net.pt``."""
    if "net" in _N:
        return _N["net"]
    import torch
    path = CACHE.dir / "net.pt"
    if path.exists():
        _N["net"] = torch.load(path, weights_only=False)
        return _N["net"]
    # the middle phrases only: the Tune's last two phrases repeat its first two, which are the test, so training on
    # them would be training on the test.  Five transpositions (by resampling, tempo with pitch) give some variety.
    mixes, targets = [], []
    st = stems((2, 3))
    for semis in (-2, -1, 0, 1, 2):
        f = 2 ** (semis / 12)
        n = len(st["vocals"])
        grid = np.arange(0, n - 1, f)
        sh = {k: np.interp(grid, np.arange(n), v) for k, v in st.items()}
        mixes.append(mix(sh))
        targets.append(sh["vocals"])
    _N["net"] = S.mask_net_train(mixes, targets, epochs=20)
    torch.save(_N["net"], path)
    return _N["net"]


def compute_net() -> dict:
    fit = network()
    st = stems((0, 1))
    x = mix(st)
    v = S.mask_net_apply(fit, x)
    c = concat([C(fade(v / np.max(np.abs(v)) * 0.9)), C(fade(st["vocals"] / np.max(np.abs(st["vocals"])) * 0.9))], gap=0.8, names=["net", "true"])
    return {"sdr": S.sdr(st["vocals"], v), "si_sdr": S.si_sdr(st["vocals"], v), "losses": fit["losses"],
            "starts": {k: float(c.events[k]) for k in ("net", "true")},
            "clips": {"two": save("net.two", c, detail="the session's vocals as a small network separates them, trained on other phrases; then as recorded")}}


def compute_metrics() -> dict:
    st = stems((0, 1))
    v = st["vocals"]
    target = 8.0
    leak = st["other"] * np.sqrt(np.sum(v ** 2) / np.sum(st["other"] ** 2)) * 10 ** (-target / 20)
    est_leak = v + leak
    X = S.stft(v)
    rng = np.random.default_rng(2)
    keep = rng.random(X.shape) > 0.35                       # musical noise: random bins switched off
    est_art = S.istft(X * keep, len(v))
    # scale the artifact estimate's error to the same SDR
    err = est_art - v
    est_art = v + err * np.sqrt(np.sum(leak ** 2) / np.sum(err ** 2))
    c = concat([C(fade(est_leak / np.max(np.abs(est_leak)) * 0.9)), C(fade(est_art / np.max(np.abs(est_art)) * 0.9))], gap=0.8, names=["leak", "artifacts"])
    return {"sdr_leak": S.sdr(v, est_leak), "sdr_artifacts": S.sdr(v, est_art), "starts": {k: float(c.events[k]) for k in ("leak", "artifacts")},
            "clips": {"two": save("metrics.two", c, detail="two estimates of the session's vocals with the same SDR: one with the piano and guitar leaking in, one with random bins switched off")}}


def compute_tune64() -> dict:
    st = stems((0, 1))
    x = mix(st)
    fit = network()
    v_est = S.mask_net_apply(fit, x)
    karaoke_est = x - v_est
    karaoke_true = st["bass"] + st["drums"] + st["other"]
    acap_true = st["vocals"]
    n = lambda y: y / np.max(np.abs(y)) * 0.9
    c = concat([C(fade(n(v_est))), C(fade(n(karaoke_est))), C(fade(n(acap_true))), C(fade(n(karaoke_true)))], gap=0.8,
               names=["acap_sep", "kara_sep", "acap_true", "kara_true"])
    return {"names": ["acap_sep", "kara_sep", "acap_true", "kara_true"], "sdr_voice": S.sdr(acap_true, v_est), "sdr_karaoke": S.sdr(karaoke_true, karaoke_est),
            "seconds": c.duration, "starts": {k: float(c.events[k]) for k in ("acap_sep", "kara_sep", "acap_true", "kara_true")},
            "clips": {"variation64": save("tune.variation64", c, detail="Variation 64: the session's Tune a cappella and as karaoke, first from the network's separation, then from the true stems")}}


def compute_variation() -> dict:
    t = load("tune64")
    return {"part": 64, "title": "a cappella and karaoke, separated, beside the true stems", "seconds": round(t["seconds"], 1),
            "measure": f"the separated voice {t['sdr_voice']:.1f} dB SDR, the karaoke {t['sdr_karaoke']:.1f} dB",
            "clip": "tune.variation64"}


# ---------------------------------------------------------------------------------------------- pictures and sweeps
def _band(M, top_hz=4700.0, step=2):
    k = int(top_hz / (SR / S.N_FFT))
    return np.asarray(M)[:k:step, ::step]


def compute_panmap() -> dict:
    """Every bin's panning index, and the energy at each index: peaks where the sources are panned."""
    L, R, tr, gain = stereo((0, 1))
    XL, XR = np.abs(S.stft(L)), np.abs(S.stft(R))
    idx = (XL - XR) / (XL + XR + 1e-12)
    w = (XL + XR) ** 2
    edges = np.linspace(-1, 1, 81)
    hist, _ = np.histogram(idx.ravel(), bins=edges, weights=w.ravel())
    def index(deg):
        th = (np.pi / 4) * (1 + deg / 90)
        return float((np.sin(th) - np.cos(th)) / (np.sin(th) + np.cos(th)))
    return {"centres": ((edges[:-1] + edges[1:]) / 2).tolist(), "energy": (hist / hist.max()).tolist(),
            "where": {k: index(P56.STAGE[k]) for k in P56.TRACKS}, "image": _band(idx).tolist(),
            "loud": _band(np.log10(w + 1e-9) > np.log10(w.max()) - 4).astype(float).tolist()}


def _kurt(y):
    y = np.asarray(y, float) - np.mean(y)
    return float(np.mean(y ** 4) / np.mean(y ** 2) ** 2 - 3)


def compute_icascatter() -> dict:
    """The two-channel mixture as a cloud of points, before and after unmixing; and the kurtosis that ICA climbs."""
    st = stems((0, 1))
    a, b = st["vocals"], st["other"]
    A = np.array([[0.9, 0.35], [0.4, 0.85]])
    X = A @ np.array([a, b])
    r = S.fastica(X)
    rng = np.random.default_rng(4)
    loud = np.flatnonzero(np.abs(X).sum(0) > 0.02)
    pick = rng.choice(loud, 1500, replace=False)
    nx = lambda Z: (Z / np.max(np.abs(Z[:, pick]), axis=1, keepdims=True))[:, pick]
    Sx = r["S"]
    order = np.argsort([-abs(np.corrcoef(Sx[i], a)[0, 1]) for i in range(2)])
    Sx = Sx[order] * np.sign([np.corrcoef(Sx[order[0]], a)[0, 1], np.corrcoef(Sx[order[1]], b)[0, 1]])[:, None]
    # kurtosis along every direction of the whitened mixture: ICA picks the most non-Gaussian
    Xc = X - X.mean(1, keepdims=True)
    d, E = np.linalg.eigh(np.cov(Xc))
    Z = (E / np.sqrt(d)) .T @ Xc
    ang = np.linspace(0, np.pi, 91)
    kurt = [_kurt(np.cos(t) * Z[0] + np.sin(t) * Z[1]) for t in ang]
    return {"mixed": nx(X).T.tolist(), "unmixed": nx(Sx).T.tolist(), "angles": np.degrees(ang).tolist(), "kurtosis": kurt,
            "kurt_sources": {"vocals": _kurt(a), "other": _kurt(b)}, "kurt_mixes": [_kurt(X[0]), _kurt(X[1])],
            "kurt_gauss": _kurt(rng.standard_normal(len(a)))}


def compute_hpsssweep() -> dict:
    """How the median filters' length and the masks' power change the split."""
    st = stems((0, 1))
    x = mix(st)
    tone = st["vocals"] + st["bass"] + st["other"]
    sizes = [3, 5, 9, 17, 31, 63]
    out = {}
    for p in (1.0, 2.0):
        dr, tn = [], []
        for n in sizes:
            r = S.hpss(x, harm=n, perc=n, power=p)
            dr.append(S.sdr(st["drums"], r["percussive"]))
            tn.append(S.sdr(tone, r["harmonic"]))
        out[str(int(p))] = {"drums": dr, "tonal": tn}
    return {"sizes": sizes, "power": out}


def compute_nmfrank() -> dict:
    """NMF's templates for the voice and the drums, and the vocal SDR as the number of templates per source grows."""
    from explainer.music.monochord.mir.transcribe import nmf
    train = stems((2, 3))
    Wv = nmf(np.abs(S.stft(train["vocals"])), rank=12, iters=120, seed=0)["W"]
    Wd = nmf(np.abs(S.stft(train["drums"])), rank=12, iters=120, seed=0)["W"]
    k = int(4700 / (SR / S.N_FFT))
    def norm(W):
        W = W[:k] / (W[:k].max(axis=0, keepdims=True) + 1e-12)
        return W[:, np.argsort(np.argmax(W, axis=0))]
    st = stems((0, 1))
    x = mix(st)
    ranks = [1, 3, 6, 12, 24]
    voc, oth = [], []
    for rk in ranks:
        est = S.nmf_separate(x, train, rank=rk, iters=80)
        voc.append(S.sdr(st["vocals"], est["vocals"]))
        oth.append(S.sdr(st["other"], est["other"]))
    return {"W_vocals": np.log10(norm(Wv) + 1e-3).tolist(), "W_drums": np.log10(norm(Wd) + 1e-3).tolist(), "ranks": ranks, "vocals": voc, "other": oth}


def compute_maskimg() -> dict:
    """The vocals' ideal binary and ratio masks, and the network's, as pictures (0 to 4.7 kHz)."""
    st = stems((0, 1))
    X = S.stft(mix(st))
    mags = np.array([np.abs(S.stft(st[k])) for k in STEMS])
    irm = mags[0] / (mags.sum(0) + 1e-12)
    ibm = (mags[0] == mags.max(0)).astype(float)
    net = S.mask_net_mask(network(), X)
    frames = slice(0, min(X.shape[1], 400))
    return {"ibm": _band(ibm[:, frames]).tolist(), "irm": _band(irm[:, frames]).tolist(), "net": _band(net[:, frames]).tolist(),
            "mix": _band(np.log10(np.abs(X[:, frames]) + 1e-4)).tolist(), "seconds": float((frames.stop) * S.HOP / SR),
            "net_vs_irm": float(np.mean(np.abs(net[:384] - irm[:384])))}


def compute_glcurve() -> dict:
    """Griffin-Lim's inconsistency, iteration by iteration, and its SDR: consistent is not correct."""
    st = stems((0, 1))
    v = st["vocals"]
    mag = np.abs(S.stft(v))
    rng = np.random.default_rng(0)
    X = mag * np.exp(2j * np.pi * rng.random(mag.shape))
    inc, sd, its = [], [], []
    for i in range(101):
        y = S.istft(X, len(v))
        Y = S.stft(y)
        if i in (0, 1, 2, 3, 5, 8, 12, 20, 30, 45, 60, 80, 100):
            its.append(i)
            inc.append(float(20 * np.log10(np.linalg.norm(np.abs(Y) - mag) / np.linalg.norm(mag))))
            sd.append(S.sdr(v, y))
        X = mag * np.exp(1j * np.angle(Y))
    return {"iters": its, "inconsistency_db": inc, "sdr": sd}


def compute_gain() -> dict:
    """What SDR and SI-SDR say about simple changes to a perfect estimate; and three of them heard."""
    st = stems((0, 1))
    v = st["vocals"]
    from scipy.signal import butter, sosfiltfilt
    lp = sosfiltfilt(butter(6, 2000, fs=SR, output="sos"), v)
    late = np.concatenate([np.zeros(48), v[:-48]])
    rows = {"half as loud": 0.5 * v, "upside down": -v, "dull (2 kHz low-pass)": lp, "1 ms late": late}
    g = 0.9 / np.max(np.abs(v))
    c = concat([C(fade(v * g)), C(fade(lp * g)), C(fade(late * g))], gap=0.8, names=["true", "dull", "late"])
    return {"rows": {k: {"sdr": S.sdr(v, e), "si_sdr": S.si_sdr(v, e)} for k, e in rows.items()},
            "starts": {k: float(c.events[k]) for k in ("true", "dull", "late")},
            "clips": {"three": save("gain.three", c, detail="the session's vocals as recorded; low-passed at 2 kHz; and a millisecond late")}}

def compute_netleak() -> dict:
    """The same network trained the wrong way: on stretches that include the Tune's last two phrases, which repeat the
    first two (the test), and one that includes the second test phrase itself.  What a leak is worth."""
    mixes, targets = [], []
    for ph in ((2, 3), (4, 5), (1, 2), (3, 4)):
        st = stems(ph)
        mixes.append(mix(st))
        targets.append(st["vocals"])
    fit = S.mask_net_train(mixes, targets, epochs=20)
    st = stems((0, 1))
    v = S.mask_net_apply(fit, mix(st))
    return {"sdr": S.sdr(st["vocals"], v), "honest": load("net")["sdr"]}


def compute_meet() -> dict:
    """The test set heard: each stem of the session's first two phrases alone, then the mixture."""
    st = stems((0, 1))
    n = int(4.0 * SR)
    segs = [C(fade(st[k][:n] / np.max(np.abs(st[k][:n])) * 0.9)) for k in STEMS] + [C(fade(mix(st)[:n] / np.max(np.abs(mix(st)[:n])) * 0.9))]
    c = concat(segs, gap=0.5, names=list(STEMS) + ["mix"])
    share = {k: float(np.sum(st[k] ** 2) / np.sum(mix(st) ** 2)) for k in STEMS}
    return {"starts": {k: float(c.events[k]) for k in list(STEMS) + ["mix"]}, "energy_share": share,
            "clips": {"five": save("meet.five", c, detail="Part 56's session, four seconds of each stem alone (vocals, bass, drums, other), then all four mixed")}}


def compute_remix() -> dict:
    """A remix from separated stems: the vocals turned up 6 dB and the drums down 6 dB, from the network's vocal and the
    median filter's drums, against the same remix from the true stems."""
    st = stems((0, 1))
    x = mix(st)
    v = S.mask_net_apply(network(), x)
    r = S.hpss(x - v, harm=63, perc=63)
    up, down = 10 ** (6 / 20), 10 ** (-6 / 20)
    est = x + (up - 1) * v + (down - 1) * r["percussive"]
    true = x + (up - 1) * st["vocals"] + (down - 1) * st["drums"]
    g = 0.9 / max(np.max(np.abs(est)), np.max(np.abs(true)))
    c = concat([C(fade(x * 0.9 / np.max(np.abs(x)))), C(fade(est * g)), C(fade(true * g))], gap=0.8, names=["mix", "separated", "true"])
    return {"sdr_remix": S.sdr(true, est), "sdr_mix": S.sdr(true, x), "starts": {k: float(c.events[k]) for k in ("mix", "separated", "true")},
            "clips": {"three": save("remix.three", c, detail="the session as mixed; then remixed with the vocals 6 dB up and the drums 6 dB down from separated stems; then the same remix from the true stems")}}


def compute_hpssknob() -> dict:
    """The percussive half with short and with long median filters, heard."""
    st = stems((0, 1))
    x = mix(st)
    a, b = S.hpss(x, harm=5, perc=5), S.hpss(x, harm=63, perc=63)
    n = lambda y: y / np.max(np.abs(y)) * 0.9
    c = concat([C(fade(n(a["percussive"]))), C(fade(n(b["percussive"])))], gap=0.8, names=["short", "long"])
    return {"sdr_short": S.sdr(st["drums"], a["percussive"]), "sdr_long": S.sdr(st["drums"], b["percussive"]),
            "starts": {k: float(c.events[k]) for k in ("short", "long")},
            "clips": {"two": save("hpssknob.two", c, detail="the session's percussive half by median filtering with 5-point filters, then with 63-point filters")}}


def compute_truephase() -> dict:
    """The vocals' ideal ratio mask with the mixture's phase, then with the vocals' own: the phase gap, heard."""
    st = stems((0, 1))
    o = S.oracle_masks(st)
    n = lambda y: y / np.max(np.abs(y)) * 0.9
    c = concat([C(fade(n(o["irm"]["vocals"]))), C(fade(n(o["true_phase"]["vocals"])))], gap=0.8, names=["mixphase", "truephase"])
    return {"sdr_mix": S.sdr(st["vocals"], o["irm"]["vocals"]), "sdr_true": S.sdr(st["vocals"], o["true_phase"]["vocals"]),
            "starts": {k: float(c.events[k]) for k in ("mixphase", "truephase")},
            "clips": {"two": save("truephase.two", c, detail="the session's vocals through the ideal ratio mask with the mixture's phase, then with the vocals' own phase")}}



ITEMS = {"hook": compute_hook, "pan": compute_pan, "ica": compute_ica, "hpss": compute_hpss, "nmf": compute_nmf, "oracle": compute_oracle,
         "phase": compute_phase, "net": compute_net, "metrics": compute_metrics, "tune64": compute_tune64, "variation": compute_variation,
         "panmap": compute_panmap, "icascatter": compute_icascatter, "hpsssweep": compute_hpsssweep, "nmfrank": compute_nmfrank,
         "maskimg": compute_maskimg, "glcurve": compute_glcurve, "gain": compute_gain, "netleak": compute_netleak,
         "meet": compute_meet, "remix": compute_remix, "hpssknob": compute_hpssknob, "truephase": compute_truephase}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
