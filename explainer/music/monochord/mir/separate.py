"""Monochord's separators (Part 64, *Source Separation*).

The mixing model is x = sum of sources, each perhaps panned; separation runs it backwards.  Monochord owns every stem it
mixed, so every separation can be scored exactly, and against source-informed reference estimates.

    stft, istft                         a Hann STFT with exact overlap-add inverse
    sdr, si_sdr                         signal-to-distortion ratio, and the scale-invariant version (Le Roux et al., 2019)
    centre_cancel, pan_masks            stereo tricks: subtract the channels; select time-frequency bins by panning
    fastica                             independent components of a two-channel instantaneous mixture (Hyvärinen, 1999)
    hpss                                harmonic and percussive by median filtering (FitzGerald, 2010)
    nmf_separate                        templates learnt from each source's own recordings, Wiener masks from the fit
    oracle_masks                        the ideal binary and ratio masks, which need the answer: reference masks, not universal SDR bounds
    griffin_lim                         a phase for a magnitude, by alternating projections (Griffin and Lim, 1984)
    mask_net_train, _mask, _apply       a small network that predicts a source's ratio mask from the mixture's spectrum

No manim; torch only in the network's three functions.  Checked in ``tests/music/test_separate.py``.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.ndimage import median_filter

N_FFT = 2048
HOP = 512


# --------------------------------------------------------------------------------------------- transforms and scores
def stft(x, n: int = N_FFT, hop: int = HOP) -> np.ndarray:
    x = np.asarray(x, float)
    pad = np.r_[np.zeros(n), x, np.zeros(n)]
    count = 1 + (len(pad) - n) // hop
    idx = np.arange(n)[None, :] + hop * np.arange(count)[:, None]
    return np.fft.rfft(pad[idx] * np.hanning(n + 1)[:-1][None, :], axis=1).T          # bins x frames


def istft(X, length: int, n: int = N_FFT, hop: int = HOP) -> np.ndarray:
    w = np.hanning(n + 1)[:-1]
    frames = np.fft.irfft(X.T, n, axis=1) * w[None, :]
    out = np.zeros(hop * (frames.shape[0] - 1) + n)
    norm = np.zeros_like(out)
    for i, f in enumerate(frames):
        out[i * hop:i * hop + n] += f
        norm[i * hop:i * hop + n] += w ** 2
    out /= np.maximum(norm, 1e-8)
    return out[n:n + length]


def sdr(ref, est) -> float:
    ref, est = np.asarray(ref, float), np.asarray(est, float)
    return float(10 * np.log10(np.sum(ref ** 2) / (np.sum((ref - est) ** 2) + 1e-12) + 1e-12))


def si_sdr(ref, est) -> float:
    """Scale-invariant SDR: project the estimate on the reference first, so that a quieter but otherwise perfect
    estimate is not penalized."""
    ref, est = np.asarray(ref, float), np.asarray(est, float)
    a = float(est @ ref) / (float(ref @ ref) + 1e-12)
    t = a * ref
    return float(10 * np.log10(np.sum(t ** 2) / (np.sum((est - t) ** 2) + 1e-12) + 1e-12))


# --------------------------------------------------------------------------------------------- stereo
def centre_cancel(L, R) -> np.ndarray:
    """L - R: whatever is identical in both channels (a centred voice, bass and kick) cancels exactly."""
    return np.asarray(L, float) - np.asarray(R, float)


def pan_masks(L, R, centres, width: float = 0.15) -> list:
    """Per time-frequency bin, the panning index (|L| - |R|) / (|L| + |R|), from -1 (right) to +1 (left); a source
    panned to p gets the bins whose index is within ``width`` of p (after Avendano, 2003).  Returns one mono estimate
    per centre."""
    XL, XR = stft(L), stft(R)
    idx = (np.abs(XL) - np.abs(XR)) / (np.abs(XL) + np.abs(XR) + 1e-12)
    M = (XL + XR) / 2
    out = []
    for c in centres:
        mask = np.abs(idx - c) <= width
        out.append(istft(M * mask, len(L)))
    return out


def fastica(X, iters: int = 200, seed: int = 0) -> dict:
    """FastICA with the log-cosh contrast and symmetric decorrelation, for a (channels x samples) mixture: whiten, then
    find the rotation that makes the outputs as non-Gaussian as possible."""
    X = np.asarray(X, float)
    X = X - X.mean(axis=1, keepdims=True)
    d, E = np.linalg.eigh(np.cov(X))
    Wh = E @ np.diag(1 / np.sqrt(d + 1e-12)) @ E.T
    Z = Wh @ X
    n = Z.shape[0]
    rng = np.random.default_rng(seed)
    W = np.linalg.qr(rng.normal(size=(n, n)))[0]
    for _ in range(iters):
        G = np.tanh(W @ Z)
        W_new = (G @ Z.T) / Z.shape[1] - np.diag((1 - G ** 2).mean(axis=1)) @ W
        U, _, Vt = np.linalg.svd(W_new)
        W_new = U @ Vt
        if np.max(np.abs(np.abs(np.diag(W_new @ W.T)) - 1)) < 1e-9:
            W = W_new
            break
        W = W_new
    S = W @ Z
    return {"S": S, "W": W @ Wh}


# --------------------------------------------------------------------------------------------- single channel
def hpss(x, harm: int = 17, perc: int = 17, power: float = 2.0) -> dict:
    """FitzGerald (2010): in a spectrogram, harmonic sounds are horizontal lines and percussive ones vertical; a median
    filter along time keeps the first, along frequency the second; soft masks share each bin between them."""
    X = stft(x)
    S = np.abs(X)
    H = median_filter(S, size=(1, harm))
    P = median_filter(S, size=(perc, 1))
    Mh = H ** power / (H ** power + P ** power + 1e-12)
    return {"harmonic": istft(X * Mh, len(x)), "percussive": istft(X * (1 - Mh), len(x)), "mask": Mh}


def nmf_separate(x, examples: dict, rank: int = 12, iters: int = 120, seed: int = 0) -> dict:
    """Supervised NMF: for each source, learn ``rank`` spectral templates from an example recording of it; fit the
    mixture's magnitude with all templates fixed; each source is the mixture times its share of the fit (a Wiener-like
    mask)."""
    from .transcribe import nmf
    X = stft(x)
    V = np.abs(X)
    Ws, names = [], []
    for name, ex in examples.items():
        r = nmf(np.abs(stft(ex)), rank=rank, iters=iters, seed=seed)
        Ws.append(r["W"])
        names.append(name)
    W = np.concatenate(Ws, axis=1)
    H = nmf(V, W=W, fix_W=True, iters=iters, seed=seed)["H"]
    total = W @ H + 1e-12
    out, k = {}, 0
    for name, Wk in zip(names, Ws):
        part = Wk @ H[k:k + Wk.shape[1]]
        out[name] = istft(X * part / total, len(x))
        k += Wk.shape[1]
    return out


def oracle_masks(sources: dict, mix=None) -> dict:
    """The ideal binary mask (each bin to the loudest source) and the ideal ratio mask (each bin shared in proportion
    to the sources' magnitudes), applied to the mixture: they need the true sources, they are reference estimates, not universal optima for waveform SDR.
    Phase-sensitive and complex masks use different constraints."""
    names = list(sources)
    length = len(next(iter(sources.values())))
    mix = sum(sources.values()) if mix is None else mix
    X = stft(mix)
    mags = np.array([np.abs(stft(sources[k])) for k in names])
    ibm = (mags == mags.max(axis=0, keepdims=True))
    irm = mags / (mags.sum(axis=0, keepdims=True) + 1e-12)
    out = {"ibm": {}, "irm": {}, "true_phase": {}}
    for i, k in enumerate(names):
        out["ibm"][k] = istft(X * ibm[i], length)
        out["irm"][k] = istft(X * irm[i], length)
        Sk = stft(sources[k])
        out["true_phase"][k] = istft(np.abs(X) * irm[i] * np.exp(1j * np.angle(Sk)), length)
    return out


def griffin_lim(mag, length: int, iters: int = 60, seed: int = 0) -> np.ndarray:
    """A signal whose STFT magnitude is close to ``mag``: start from random phase, and alternate between keeping the
    magnitude and keeping a consistent signal."""
    rng = np.random.default_rng(seed)
    X = mag * np.exp(2j * np.pi * rng.random(mag.shape))
    for _ in range(iters):
        y = istft(X, length)
        X = mag * np.exp(1j * np.angle(stft(y)))
    return istft(X, length)


def log_features(X) -> np.ndarray:
    """Frames of log magnitude for the network, each frame with its neighbours (5 frames), bins x frames -> frames x dims."""
    L = np.log1p(np.abs(X))[:384]                        # up to about 9 kHz at 48 kHz and 2048 points
    pad = np.pad(L, ((0, 0), (2, 2)), mode="edge")
    return np.concatenate([pad[:, k:k + L.shape[1]] for k in range(5)], axis=0).T


def mask_net_train(mixes, targets, epochs: int = 20, hidden: int = 512, seed: int = 0) -> dict:
    """A small network: log-magnitude frames of the mixture in, the clipped source-to-mixture magnitude mask (first 384 bins) out,
    trained by mean squared error on the masks."""
    import torch
    torch.manual_seed(seed)
    torch.set_num_threads(4)
    Xs, Ys = [], []
    for x, s in zip(mixes, targets):
        X, S = stft(x), stft(s)
        Xs.append(log_features(X))
        Ys.append(np.clip(np.abs(S) / (np.abs(X) + 1e-9), 0, 1)[:384].T)
    Xt = torch.tensor(np.concatenate(Xs), dtype=torch.float32)
    Yt = torch.tensor(np.concatenate(Ys), dtype=torch.float32)
    mu, sd = Xt.mean(0), Xt.std(0) + 1e-6
    model = torch.nn.Sequential(torch.nn.Linear(Xt.shape[1], hidden), torch.nn.ReLU(), torch.nn.Linear(hidden, hidden), torch.nn.ReLU(),
                                torch.nn.Linear(hidden, 384), torch.nn.Sigmoid())
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    losses = []
    g = torch.Generator().manual_seed(seed)
    for _ in range(epochs):
        perm = torch.randperm(len(Xt), generator=g)
        tot = 0.0
        for k in range(0, len(Xt), 256):
            i = perm[k:k + 256]
            opt.zero_grad()
            loss = torch.mean((model((Xt[i] - mu) / sd) - Yt[i]) ** 2)
            loss.backward()
            opt.step()
            tot += float(loss.detach()) * len(i)
        losses.append(tot / len(Xt))
    return {"model": model, "mu": mu, "sd": sd, "losses": losses}


def mask_net_mask(fit, X) -> np.ndarray:
    """The network's mask for a mixture's STFT ``X``: its prediction up to about 9 kHz, nothing above (it does not see it)."""
    import torch
    with torch.no_grad():
        M = fit["model"]((torch.tensor(log_features(X), dtype=torch.float32) - fit["mu"]) / fit["sd"]).numpy().T
    full = np.zeros(X.shape)
    full[:384] = M
    return full


def mask_net_apply(fit, x) -> np.ndarray:
    X = stft(x)
    return istft(X * mask_net_mask(fit, X), len(x))
