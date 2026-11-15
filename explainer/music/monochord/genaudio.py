"""Monochord's generative audio (Part 66 of *Music, Built*): the smallest honest version of each idea that took
machines from noodling one sample at a time to finished songs.  Everything runs at 16 kHz.

    mulaw, unmulaw                 WaveNet's 8-bit companding: 256 levels, fine near silence and coarse when loud
    ARNet, train_ar, sample_ar     a network that predicts the next sample's level from the last few hundred
    melbank, mel, mel_to_audio     a mel spectrogram, and back to sound by a pseudo-inverse and Griffin-Lim's phase
    kmeans, RVQ                    residual vector quantization of spectral frames: a codec's tokens, stage on stage
    harmonic_synth                 a bank of harmonics plus filtered noise, frame by frame (numpy and torch)
    features                       pitch (Part 61's YIN) and loudness per frame
    DDSP, train_ddsp, render_ddsp  Engel et al.'s idea: a small network sets a synthesizer's controls, learnt by
                                   comparing spectra at several resolutions
    Diffusion                      a denoising diffusion model over vectors (here, a tone's harmonic profile)
    frechet                        the Fréchet distance between two sets of embeddings (as in FAD)
    watermark, detect              a spread-spectrum mark under the music, and its detection by correlation

No manim; torch for the networks.  Checked in ``tests/music/test_genaudio.py``.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.signal import resample_poly

SR16 = 16_000
N_FFT, HOP = 512, 256                                     # 32 ms frames, 16 ms hop at 16 kHz


def to16(y, sr: int = 48_000) -> np.ndarray:
    return resample_poly(np.asarray(y, float), 1, sr // SR16) if sr != SR16 else np.asarray(y, float)


def to48(y) -> np.ndarray:
    return resample_poly(np.asarray(y, float), 3, 1)


# --------------------------------------------------------------------------------------------- samples
def mulaw(y, mu: int = 255) -> np.ndarray:
    """Samples in [-1, 1] to integer levels 0..mu by mu-law companding."""
    y = np.clip(np.asarray(y, float), -1, 1)
    c = np.sign(y) * np.log1p(mu * np.abs(y)) / np.log1p(mu)
    return np.round((c + 1) / 2 * mu).astype(int)


def unmulaw(q, mu: int = 255) -> np.ndarray:
    c = 2 * np.asarray(q, float) / mu - 1
    return np.sign(c) * ((1 + mu) ** np.abs(c) - 1) / mu


def linear8(y) -> np.ndarray:
    """Plain 8-bit quantization, for comparison: 256 equal steps."""
    return np.round((np.clip(y, -1, 1) + 1) / 2 * 255) / 255 * 2 - 1


def train_ar(y, context: int = 256, hidden: int = 256, steps: int = 3000, batch: int = 128, seed: int = 0) -> dict:
    """A network that reads the last ``context`` samples (mu-law, scaled) and outputs a distribution over the next
    sample's 256 levels; trained by cross-entropy on random positions of ``y``."""
    import torch
    torch.manual_seed(seed)
    q = mulaw(y)
    x = torch.tensor(q / 127.5 - 1, dtype=torch.float32)
    t = torch.tensor(q, dtype=torch.long)
    net = torch.nn.Sequential(torch.nn.Linear(context, hidden), torch.nn.ReLU(), torch.nn.Linear(hidden, hidden), torch.nn.ReLU(),
                              torch.nn.Linear(hidden, 256))
    opt = torch.optim.Adam(net.parameters(), lr=1e-3)
    g = torch.Generator().manual_seed(seed)
    win = x.unfold(0, context, 1)                          # every window of `context` samples, as a view
    losses = []
    for s in range(steps):
        ix = torch.randint(context, len(q), (batch,), generator=g)
        xb = win[ix - context]
        loss = torch.nn.functional.cross_entropy(net(xb), t[ix])
        opt.zero_grad()
        loss.backward()
        opt.step()
        if s % 50 == 0:
            losses.append(float(loss.detach()) / math.log(2))
    return {"net": net, "context": context, "losses": losses}


def sample_ar(fit, prime, n: int, temperature: float = 1.0, seed: int = 0) -> np.ndarray:
    """Draw ``n`` samples one at a time after ``prime`` (audio at 16 kHz): sixteen thousand decisions a second."""
    import torch
    g = torch.Generator().manual_seed(seed)
    c = fit["context"]
    buf = list(mulaw(prime)[-c:] / 127.5 - 1)
    out = []
    net = fit["net"]
    with torch.no_grad():
        for _ in range(n):
            logits = net(torch.tensor([buf[-c:]], dtype=torch.float32))[0] / max(temperature, 1e-3)
            k = int(torch.multinomial(logits.softmax(-1), 1, generator=g))
            out.append(k)
            buf.append(k / 127.5 - 1)
    return unmulaw(np.array(out))


def ar_bits(fit, y) -> float:
    """Bits per sample of the network on audio it was not trained on (teacher forcing)."""
    import torch
    q = mulaw(y)
    c = fit["context"]
    x = torch.tensor(q / 127.5 - 1, dtype=torch.float32)
    idx = np.arange(c, len(q), 7)
    with torch.no_grad():
        xb = torch.stack([x[i - c:i] for i in idx])
        lp = torch.log_softmax(fit["net"](xb), -1)
        return float(-lp[torch.arange(len(idx)), torch.tensor(q[idx])].mean()) / math.log(2)


# --------------------------------------------------------------------------------------------- spectra
def stft(y, n: int = N_FFT, hop: int = HOP) -> np.ndarray:
    y = np.asarray(y, float)
    w = np.hanning(n + 1)[:-1]
    pad = np.pad(y, (n // 2, n // 2))
    k = 1 + (len(pad) - n) // hop
    fr = np.stack([pad[i * hop:i * hop + n] * w for i in range(k)])
    return np.fft.rfft(fr, axis=1).T


def istft(X, length: int, n: int = N_FFT, hop: int = HOP) -> np.ndarray:
    w = np.hanning(n + 1)[:-1]
    fr = np.fft.irfft(X.T, n=n, axis=1) * w
    out = np.zeros(n + hop * (fr.shape[0] - 1))
    norm = np.zeros_like(out)
    for i, f in enumerate(fr):
        out[i * hop:i * hop + n] += f
        norm[i * hop:i * hop + n] += w ** 2
    out = out / np.maximum(norm, 1e-8)
    return out[n // 2:n // 2 + length]


def griffin_lim(mag, length: int, iters: int = 60, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    X = mag * np.exp(2j * np.pi * rng.random(mag.shape))
    for _ in range(iters):
        Y = stft(istft(X, length))
        if Y.shape[1] != mag.shape[1]:                     # a length that does not fill the last frame exactly
            Y = Y[:, :mag.shape[1]] if Y.shape[1] > mag.shape[1] else np.pad(Y, ((0, 0), (0, mag.shape[1] - Y.shape[1])))
        X = mag * np.exp(1j * np.angle(Y))
    return istft(X, length)


def melbank(n_mels: int = 64, n: int = N_FFT, sr: int = SR16, fmin: float = 40.0, fmax: float = 7600.0) -> np.ndarray:
    hz = lambda m: 700 * (10 ** (m / 2595) - 1)
    mm = lambda f: 2595 * np.log10(1 + f / 700)
    pts = hz(np.linspace(mm(fmin), mm(fmax), n_mels + 2))
    f = np.fft.rfftfreq(n, 1 / sr)
    B = np.zeros((n_mels, len(f)))
    for i in range(n_mels):
        a, b, c = pts[i], pts[i + 1], pts[i + 2]
        B[i] = np.clip(np.minimum((f - a) / (b - a), (c - f) / (c - b)), 0, None)
    return B


def mel(y, n_mels: int = 64) -> np.ndarray:
    return melbank(n_mels) @ np.abs(stft(y))


def mel_to_audio(M, length: int, iters: int = 60) -> np.ndarray:
    """Back from a mel spectrogram: the least-squares (non-negative) magnitude, then Griffin-Lim's phase."""
    B = melbank(M.shape[0])
    mag = np.maximum(np.linalg.pinv(B) @ M, 0)
    return griffin_lim(mag, length, iters)


# --------------------------------------------------------------------------------------------- tokens
def kmeans(X, k: int, iters: int = 25, seed: int = 0) -> np.ndarray:
    """Lloyd's algorithm with k-means++ starts; returns the k centres."""
    rng = np.random.default_rng(seed)
    X = np.asarray(X, float)
    C = [X[rng.integers(len(X))]]
    d2 = ((X - C[0]) ** 2).sum(1)
    for _ in range(1, k):
        p = d2 / d2.sum() if d2.sum() > 0 else None
        C.append(X[rng.choice(len(X), p=p)])
        d2 = np.minimum(d2, ((X - C[-1]) ** 2).sum(1))
    C = np.array(C)
    for _ in range(iters):
        lab = assign(X, C)
        for j in range(k):
            m = lab == j
            if m.any():
                C[j] = X[m].mean(0)
    return C


def assign(X, C) -> np.ndarray:
    d = (X ** 2).sum(1)[:, None] - 2 * X @ C.T + (C ** 2).sum(1)[None, :]
    return np.argmin(d, axis=1)


class RVQ:
    """Residual vector quantization: the first codebook quantizes a frame, the next quantizes what is left, and so on;
    each frame becomes one token per stage (log2 k bits each)."""

    def __init__(self, stages: int = 4, k: int = 256, seed: int = 0):
        self.stages, self.k, self.seed = stages, k, seed
        self.books = []

    def fit(self, X) -> "RVQ":
        R = np.asarray(X, float).copy()
        for s in range(self.stages):
            C = kmeans(R, self.k, seed=self.seed + s)
            self.books.append(C)
            R = R - C[assign(R, C)]
        return self

    def encode(self, X, stages=None) -> np.ndarray:
        R = np.asarray(X, float).copy()
        codes = []
        for C in self.books[:stages or self.stages]:
            c = assign(R, C)
            codes.append(c)
            R = R - C[c]
        return np.array(codes)

    def decode(self, codes) -> np.ndarray:
        return sum(self.books[s][c] for s, c in enumerate(codes))


def frames(y) -> np.ndarray:
    """A codec's input: each frame's log magnitude spectrum (frames x bins)."""
    return np.log(np.abs(stft(y)).T + 1e-4)


def from_frames(F, length: int, iters: int = 60) -> np.ndarray:
    return griffin_lim(np.exp(F).T, length, iters)


def spectral_distance(a, b) -> float:
    """Mean absolute difference of log magnitude spectra, in dB."""
    A, B = frames(a), frames(b)
    n = min(len(A), len(B))
    return float(np.mean(np.abs(A[:n] - B[:n])) * 20 / math.log(10))


# --------------------------------------------------------------------------------------------- DDSP
def features(y, sr: int = SR16, hop: int = 64) -> dict:
    """Pitch by YIN (Part 61) and loudness (dB RMS) every ``hop`` samples (4 ms at 16 kHz)."""
    from .mir import transcribe as TR
    p = TR.yin(np.asarray(y, float), sr, fmin=60, fmax=1000, hop=hop)
    t = np.arange(0, len(y), hop) / sr
    f0 = np.interp(t, p["t"], np.nan_to_num(p["f0"], nan=0.0))
    ok = np.interp(t, p["t"], (np.asarray(p["aperiodicity"]) < 0.25).astype(float)) > 0.5
    # hold the last good pitch through unvoiced frames, so the synthesizer never jumps
    last = 220.0
    for i in range(len(f0)):
        if ok[i] and f0[i] > 0:
            last = f0[i]
        else:
            f0[i] = last
    pad = np.pad(np.asarray(y, float), (hop, hop))
    rms = np.array([np.sqrt(np.mean(pad[i:i + 2 * hop] ** 2)) for i in range(0, len(y), hop)])
    return {"f0": f0[:len(rms)], "loud": 20 * np.log10(rms + 1e-5), "hop": hop}


def harmonic_synth(f0, amps, noise=None, hop: int = 64, sr: int = SR16, seed: int = 0):
    """Harmonics k f0 (k = 1..H) with amplitudes ``amps`` (frames x H), upsampled to samples; plus white noise shaped
    by ``noise`` (frames x bands) if given.  Harmonics above Nyquist are silenced.  Works on numpy arrays."""
    f0 = np.asarray(f0, float)
    A = np.asarray(amps, float)
    n = len(f0) * hop
    t = (np.arange(n) + 0.5) / hop - 0.5
    fs = np.interp(t, np.arange(len(f0)), f0)
    phase = 2 * np.pi * np.cumsum(fs) / sr
    H = A.shape[1]
    y = np.zeros(n)
    for k in range(1, H + 1):
        a = np.interp(t, np.arange(len(f0)), A[:, k - 1]) * (fs * k < sr / 2 - 200)
        y += a * np.sin(k * phase)
    if noise is not None:
        y += _noise(np.asarray(noise, float), n, hop, sr, seed)
    return y


def _noise(G, n, hop, sr, seed):
    rng = np.random.default_rng(seed)
    w = rng.standard_normal(n)
    W = stft(w)
    bands = np.linspace(0, W.shape[0], G.shape[1] + 1).astype(int)
    gain = np.zeros(W.shape)
    tf = np.linspace(0, G.shape[0] - 1, W.shape[1])
    for b in range(G.shape[1]):
        gain[bands[b]:bands[b + 1]] = np.interp(tf, np.arange(G.shape[0]), G[:, b])[None, :]
    return istft(W * gain, n)


def _torch_synth(f0, amps, noise_gain, hop, sr, noise_basis):
    import torch
    n = f0.shape[0] * hop
    up = torch.nn.functional.interpolate(f0[None, None, :], size=n, mode="linear", align_corners=False)[0, 0]
    phase = 2 * math.pi * torch.cumsum(up, 0) / sr
    H = amps.shape[1]
    A = torch.nn.functional.interpolate(amps.T[None], size=n, mode="linear", align_corners=False)[0]
    k = torch.arange(1, H + 1, dtype=torch.float32)[:, None]
    alias = (up[None, :] * k < sr / 2 - 200).float()
    y = (A * alias * torch.sin(k * phase[None, :])).sum(0)
    g = torch.nn.functional.interpolate(noise_gain.T[None], size=n, mode="linear", align_corners=False)[0]
    y = y + (g * noise_basis[:, :n]).sum(0)
    return y


def _spec_loss(a, b, sizes=(2048, 1024, 512, 256, 128)):
    import torch
    loss = 0.0
    for s in sizes:
        w = torch.hann_window(s)
        A = torch.stft(a, s, s // 4, window=w, return_complex=True).abs()
        B = torch.stft(b, s, s // 4, window=w, return_complex=True).abs()
        loss = loss + (A - B).abs().mean() + (torch.log(A + 1e-5) - torch.log(B + 1e-5)).abs().mean()
    return loss


def _noise_basis(n, bands, seed=0):
    """White noise split into ``bands`` equal-width frequency bands (bands x samples), fixed for training."""
    rng = np.random.default_rng(seed)
    w = rng.standard_normal(n)
    W = np.fft.rfft(w)
    edges = np.linspace(0, len(W), bands + 1).astype(int)
    out = np.zeros((bands, n))
    for b in range(bands):
        M = np.zeros_like(W)
        M[edges[b]:edges[b + 1]] = W[edges[b]:edges[b + 1]]
        out[b] = np.fft.irfft(M, n)
    return out


def train_ddsp(y, H: int = 40, bands: int = 16, hidden: int = 128, steps: int = 600, chunk: float = 1.0, seed: int = 0) -> dict:
    """A small network maps (pitch, loudness) per frame to H harmonic amplitudes and ``bands`` noise gains, which drive
    the synthesizer; it learns by comparing the synthesized and the real spectra at five resolutions, on random
    one-second chunks of ``y`` (16 kHz)."""
    import torch
    torch.manual_seed(seed)
    feat = features(y)
    hop = feat["hop"]
    f0, loud = feat["f0"], feat["loud"]
    n = len(f0) * hop
    y = np.pad(np.asarray(y, float), (0, max(0, n - len(y))))[:n]
    X = np.stack([np.log2(f0 / 440.0), (loud + 40) / 20], axis=1)
    net = torch.nn.Sequential(torch.nn.Linear(2, hidden), torch.nn.LeakyReLU(), torch.nn.Linear(hidden, hidden), torch.nn.LeakyReLU(),
                              torch.nn.Linear(hidden, H + bands + 1))
    opt = torch.optim.Adam(net.parameters(), lr=2e-3)
    L = int(chunk * SR16 / hop)
    basis = torch.tensor(_noise_basis(L * hop, bands, seed), dtype=torch.float32)
    rng = np.random.default_rng(seed)
    losses = []
    for s in range(steps):
        i = int(rng.integers(0, len(f0) - L))
        xb = torch.tensor(X[i:i + L], dtype=torch.float32)
        out = net(xb)
        amp = torch.nn.functional.softplus(out[:, :1]) * torch.softmax(out[:, 1:H + 1], -1)
        ng = torch.nn.functional.softplus(out[:, H + 1:]) * 0.05
        pred = _torch_synth(torch.tensor(f0[i:i + L], dtype=torch.float32), amp, ng, hop, SR16, basis)
        real = torch.tensor(y[i * hop:(i + L) * hop], dtype=torch.float32)
        loss = _spec_loss(pred, real)
        opt.zero_grad()
        loss.backward()
        opt.step()
        if s % 10 == 0:
            losses.append(float(loss.detach()))
    return {"net": net, "H": H, "bands": bands, "hop": hop, "losses": losses}


def render_ddsp(fit, f0, loud, seed: int = 0) -> np.ndarray:
    """Drive the trained synthesizer with any pitch and loudness curves (frames of ``fit['hop']`` samples)."""
    import torch
    H, bands, hop = fit["H"], fit["bands"], fit["hop"]
    X = torch.tensor(np.stack([np.log2(np.asarray(f0) / 440.0), (np.asarray(loud) + 40) / 20], axis=1), dtype=torch.float32)
    with torch.no_grad():
        out = fit["net"](X)
        amp = (torch.nn.functional.softplus(out[:, :1]) * torch.softmax(out[:, 1:H + 1], -1)).numpy()
        ng = (torch.nn.functional.softplus(out[:, H + 1:]) * 0.05).numpy()
    basis = _noise_basis(len(f0) * hop, bands, seed)
    y = harmonic_synth(f0, amp, hop=hop, sr=SR16)
    gain = np.stack([np.interp(np.arange(len(f0) * hop) / hop, np.arange(len(f0)), ng[:, b]) for b in range(bands)])
    return y + (gain * basis).sum(0), amp


# --------------------------------------------------------------------------------------------- diffusion
class Diffusion:
    """A denoising diffusion model over vectors (Ho et al., 2020), with a small conditioning input: noise is added in
    ``T`` steps; a network learns to predict the noise; sampling runs the steps backwards from pure noise."""

    def __init__(self, dim: int, cond: int = 1, T: int = 100, hidden: int = 256, seed: int = 0):
        import torch
        torch.manual_seed(seed)
        self.T, self.dim, self.cond = T, dim, cond
        self.beta = np.linspace(1e-4, 0.05, T)
        self.abar = np.cumprod(1 - self.beta)
        self.net = torch.nn.Sequential(torch.nn.Linear(dim + cond + 1, hidden), torch.nn.SiLU(), torch.nn.Linear(hidden, hidden), torch.nn.SiLU(),
                                       torch.nn.Linear(hidden, dim))
        self.seed = seed

    def fit(self, X, C, steps: int = 4000, batch: int = 128) -> list:
        import torch
        X = torch.tensor(X, dtype=torch.float32)
        C = torch.tensor(C, dtype=torch.float32).reshape(len(X), -1)
        ab = torch.tensor(self.abar, dtype=torch.float32)
        opt = torch.optim.Adam(self.net.parameters(), lr=1e-3)
        g = torch.Generator().manual_seed(self.seed)
        losses = []
        for s in range(steps):
            i = torch.randint(0, len(X), (batch,), generator=g)
            t = torch.randint(0, self.T, (batch,), generator=g)
            e = torch.randn(batch, self.dim, generator=g)
            a = ab[t][:, None]
            xt = a.sqrt() * X[i] + (1 - a).sqrt() * e
            pred = self.net(torch.cat([xt, C[i], (t[:, None].float() / self.T)], 1))
            loss = ((pred - e) ** 2).mean()
            opt.zero_grad()
            loss.backward()
            opt.step()
            if s % 50 == 0:
                losses.append(float(loss.detach()))
        return losses

    def sample(self, C, seed: int = 0, keep=()) -> tuple:
        """Draw one vector per row of ``C``; also the intermediate states at the steps in ``keep``."""
        import torch
        g = torch.Generator().manual_seed(seed)
        C = torch.tensor(C, dtype=torch.float32).reshape(-1, self.cond)
        x = torch.randn(len(C), self.dim, generator=g)
        snaps = {}
        with torch.no_grad():
            for t in range(self.T - 1, -1, -1):
                if t in keep:
                    snaps[t] = x.numpy().copy()
                e = self.net(torch.cat([x, C, torch.full((len(C), 1), t / self.T)], 1))
                b, ab = self.beta[t], self.abar[t]
                x = (x - b / math.sqrt(1 - ab) * e) / math.sqrt(1 - b)
                if t > 0:
                    x = x + math.sqrt(b) * torch.randn(x.shape, generator=g)
        return x.numpy(), snaps


# --------------------------------------------------------------------------------------------- judging and marking
def frechet(X, Y) -> float:
    """The Fréchet distance between Gaussians fitted to two sets of embeddings (the formula behind FAD)."""
    from scipy.linalg import sqrtm
    X, Y = np.asarray(X, float), np.asarray(Y, float)
    mx, my = X.mean(0), Y.mean(0)
    Sx, Sy = np.cov(X, rowvar=False), np.cov(Y, rowvar=False)
    cs = sqrtm(Sx @ Sy)
    cs = cs.real if np.iscomplexobj(cs) else cs
    return float(((mx - my) ** 2).sum() + np.trace(Sx + Sy - 2 * cs))


def watermark(y, key: int, strength_db: float = -30.0, sr: int = SR16, band=(1000, 6000)) -> np.ndarray:
    """Add a key-seeded pseudo-random +-1 sequence, band-limited, ``strength_db`` below the music's RMS."""
    from scipy.signal import butter, sosfiltfilt
    rng = np.random.default_rng(key)
    pn = rng.choice([-1.0, 1.0], len(y))
    pn = sosfiltfilt(butter(4, band, btype="band", fs=sr, output="sos"), pn)
    pn = pn / np.std(pn) * np.std(y) * 10 ** (strength_db / 20)
    return np.asarray(y, float) + pn


def _score(yb, pn, max_lag):
    best = -np.inf
    for lag in range(-max_lag, max_lag + 1):
        a, b = (yb[lag:], pn[:len(pn) - lag]) if lag >= 0 else (yb[:lag], pn[-lag:])
        best = max(best, float(np.sum(np.sign(a) * b) / np.sqrt(np.sum(b ** 2))))
    return best


def detect(y, key: int, sr: int = SR16, band=(1000, 6000), max_lag: int = 0, null_keys: int = 30) -> float:
    """A z-score: the audio's correlation with the key's sequence (signs of the band-limited audio against the
    sequence; with ``max_lag``, the best over small shifts), standardized by the same score for ``null_keys`` keys that
    were never used, so that chance gives about 0 +- 1 whatever the music."""
    from scipy.signal import butter, sosfiltfilt
    sos = butter(4, band, btype="band", fs=sr, output="sos")
    yb = sosfiltfilt(sos, np.asarray(y, float))
    seq = lambda k: sosfiltfilt(sos, np.random.default_rng(k).choice([-1.0, 1.0], len(y)))
    s = _score(yb, seq(key), max_lag)
    null = np.array([_score(yb, seq(10_000_019 + 7919 * j + key), max_lag) for j in range(null_keys)])
    return float((s - null.mean()) / (null.std() + 1e-12))
