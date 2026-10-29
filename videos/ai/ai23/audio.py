"""Part 23's sound experiments, on speech synthesized here by Kokoro-82M (the repo's local TTS, a hard dependency).

* ``speech``: twelve Kokoro voices (ten to learn from, two held out) say digit words, four-digit strings and sentences
  from the scoreboard's passage; 16 kHz, saved voice by voice under ``.cache/ai23/speech/`` (so a killed run resumes);
* sampling and aliasing, the STFT and the mel scale, and Whisper's log-mel front end, checked against the
  ``transformers`` feature extractor;
* a 1952-style recognizer (one speaker's templates; then dynamic time warping), the speaker problem measured;
* a small neural codec with residual vector quantization and quantizer dropout, at 0.4 to 3.2 kbps, graded by
  Whisper's word error rate on its output;
* a CTC recognizer for digit strings, its training replayed and its forward-algorithm lattice drawn;
* Whisper (base.en, from the Hugging Face cache) on the held-out voices: its input, its tokens, its transcripts.
"""

from __future__ import annotations

import json
import math
import os
import re
import time
from pathlib import Path

import numpy as np

SCALE = float(os.environ.get("AI23_SCALE", "1"))
SR = 16_000
DIGITS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
VOICES_TRAIN = ["af_heart", "af_bella", "af_nicole", "af_sarah", "am_adam", "am_michael", "am_eric", "bf_emma",
                "bm_george", "bm_lewis"]
VOICES_TEST = ["am_liam", "bf_isabella"]
TEMPLATE_VOICE = "af_heart"


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def threads() -> int:
    import torch

    n = int(os.environ.get("AI23_THREADS", "1"))
    torch.set_num_threads(n)
    return n


# ---------------------------------------------------------------------------
# Speech, synthesized by Kokoro
# ---------------------------------------------------------------------------
_pipes: dict = {}


def kokoro(text: str, voice: str, speed: float = 1.0) -> np.ndarray:
    """``text`` in Kokoro's ``voice``, at 16 kHz, silence trimmed."""
    import warnings

    import torch
    from scipy.signal import resample_poly

    warnings.filterwarnings("ignore")
    from kokoro import KPipeline

    code = voice[0]
    if code not in _pipes:
        _pipes[code] = KPipeline(lang_code=code, repo_id="hexgrad/Kokoro-82M")
    torch.manual_seed(0)
    parts = [r.audio.numpy() for r in _pipes[code](text, voice=voice, speed=speed) if r.audio is not None]
    a = resample_poly(np.concatenate(parts).astype(np.float64), 2, 3)  # 24 kHz -> 16 kHz
    return trim(a).astype(np.float32)


def trim(a: np.ndarray, pad=0.04) -> np.ndarray:
    on = np.nonzero(np.abs(a) > 0.02 * np.abs(a).max())[0]
    if len(on) == 0:
        return a
    p = int(pad * SR)
    return a[max(0, on[0] - p):on[-1] + p]


def passage_sentences(n: int, seed: int = 23) -> list[str]:
    from videos.ai.ai1 import compute as c1

    t = " ".join(c1.text("passage").split())
    sents = re.split(r'(?<=[.!?])"?\s+', t)
    ok = [s.strip('"') for s in sents if 6 <= len(s.split()) <= 14 and re.fullmatch(r"[A-Za-z ,.'?!;-]+", s.strip('"'))]
    g = rng(seed)
    idx = g.permutation(len(ok))[:n]
    return [ok[i] for i in sorted(idx)]


def speech_plan():
    """What each voice says: (kind, text, speed).  Train voices: digit words at two speeds, four-digit strings and
    sentences; held-out voices: digit words, more strings, sentences."""
    g = rng(1952)  # Davis, Biddulph & Balashek's Audrey, 1952
    k = max(1, int(round(SCALE * 10)))
    sents = passage_sentences(10 * len(VOICES_TRAIN) + 12 * len(VOICES_TEST))
    plan, si = {}, 0
    for v in VOICES_TRAIN + VOICES_TEST:
        test = v in VOICES_TEST
        items = [("word", d, s) for s in ((1.0,) if test else (0.9, 1.1)) for d in DIGITS[: max(3, k)]]
        n_str = 20 if test else 6
        for _ in range(max(2, int(n_str * min(1, SCALE * 4)))):
            items.append(("string", " ".join(DIGITS[i] for i in g.integers(0, 10, 4)), 1.0))
        n_s = 12 if test else 10
        for s in sents[si:si + n_s][: max(1, int(n_s * min(1, SCALE * 4)))]:
            items.append(("sentence", s, 1.0))
        si += n_s
        plan[v] = items
    return plan


def speech_dir(cache) -> Path:
    return cache.dir / "speech"


def synthesize_all(cache, log=print):
    """Every voice's clips, saved voice by voice (a killed run resumes at the next voice)."""
    plan = speech_plan()
    d = speech_dir(cache)
    d.mkdir(parents=True, exist_ok=True)
    for v, items in plan.items():
        meta = d / f"{v}.json"
        if meta.exists() and json.loads(meta.read_text()).get("items") == [list(x) for x in items]:
            continue
        t0 = time.time()
        clips = [kokoro(text, v, speed) for _, text, speed in items]
        lens = np.cumsum([0] + [len(c) for c in clips])
        audio = np.concatenate(clips)
        np.savez_compressed(d / f"{v}.tmp.npz", audio=(np.clip(audio, -1, 1) * 32767).astype(np.int16), offsets=lens)
        (d / f"{v}.tmp.npz").replace(d / f"{v}.npz")
        meta.write_text(json.dumps({"items": [list(x) for x in items]}))
        log(f"    {v}: {len(items)} clips, {lens[-1] / SR:.0f} s of speech in {time.time() - t0:.0f} s")
    return plan


def clips(cache, voice: str, kind: str | None = None):
    """[(kind, text, speed, audio float32)] for one voice."""
    d = speech_dir(cache)
    items = json.loads((d / f"{voice}.json").read_text())["items"]
    with np.load(d / f"{voice}.npz") as z:
        a, off = z["audio"].astype(np.float32) / 32767, z["offsets"]
    out = [(k, t, s, a[off[i]:off[i + 1]]) for i, (k, t, s) in enumerate(items)]
    return [c for c in out if kind is None or c[0] == kind]


# ---------------------------------------------------------------------------
# Spectra: the STFT, the mel scale, Whisper's log-mel front end
# ---------------------------------------------------------------------------
def hz_to_mel(f):
    """Slaney's mel scale (librosa's default, which Whisper uses): linear to 1 kHz, logarithmic above."""
    f = np.asarray(f, float)
    lin = f / (200.0 / 3)
    logstep = math.log(6.4) / 27.0
    return np.where(f >= 1000.0, 15.0 + np.log(np.maximum(f, 1e-9) / 1000.0) / logstep, lin)


def mel_to_hz(m):
    m = np.asarray(m, float)
    logstep = math.log(6.4) / 27.0
    return np.where(m >= 15.0, 1000.0 * np.exp(logstep * (m - 15.0)), m * 200.0 / 3)


def mel_filters(n_mels=80, n_fft=400, sr=SR, fmin=0.0, fmax=None):
    """Triangles evenly spaced on the mel scale, each normalized to unit area (Slaney)."""
    fmax = fmax or sr / 2
    freqs = np.linspace(0, sr / 2, n_fft // 2 + 1)
    hz = mel_to_hz(np.linspace(hz_to_mel(fmin), hz_to_mel(fmax), n_mels + 2))
    W = np.zeros((n_mels, len(freqs)))
    for m in range(n_mels):
        lo = (freqs - hz[m]) / (hz[m + 1] - hz[m])
        hi = (hz[m + 2] - freqs) / (hz[m + 2] - hz[m + 1])
        W[m] = np.maximum(0, np.minimum(lo, hi)) * 2.0 / (hz[m + 2] - hz[m])
    return W


def stft_power(x, n_fft=400, hop=160):
    """|STFT|^2 with a periodic Hann window and reflect padding (centred frames), the last frame dropped."""
    win = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(n_fft) / n_fft)
    xp = np.pad(x, n_fft // 2, mode="reflect")
    n = 1 + (len(xp) - n_fft) // hop
    idx = np.arange(n_fft)[None] + hop * np.arange(n)[:, None]
    S = np.abs(np.fft.rfft(xp[idx] * win, axis=1)) ** 2
    return S[:-1].T  # (freq, frames)


def whisper_logmel(x, n_mels=80, pad_to=30 * SR):
    """Whisper's input: 30 s of audio, 25 ms windows every 10 ms, 80 mel bands, log10, the top 8 decades kept,
    scaled to about [-1, 1]."""
    x = np.asarray(x, np.float64)
    x = np.pad(x, (0, max(0, pad_to - len(x))))[:pad_to] if pad_to else x
    M = mel_filters(n_mels) @ stft_power(x)
    L = np.log10(np.maximum(M, 1e-10))
    L = np.maximum(L, L.max() - 8.0)
    return (L + 4.0) / 4.0


def logmel(x, n_mels=40):
    """The CTC model's features: log mel energies, 10 ms frames, normalized per utterance."""
    M = mel_filters(n_mels) @ stft_power(np.asarray(x, np.float64))
    L = np.log(M + 1e-6)
    return ((L - L.mean()) / (L.std() + 1e-6)).astype(np.float32)


def compute_mel(cache):
    v = VOICES_TEST[0]
    kind, text, _, a = clips(cache, v, "sentence")[0]
    from transformers import WhisperFeatureExtractor

    ours = whisper_logmel(a)
    fe = WhisperFeatureExtractor.from_pretrained("openai/whisper-base.en")
    hf = fe(a, sampling_rate=SR, return_tensors="np").input_features[0]
    diff = float(np.abs(ours - hf).max())
    n = int(math.ceil(len(a) / 160)) + 2
    P = stft_power(a.astype(np.float64))
    W = mel_filters(80)
    out = dict(text=text, voice=v, seconds=len(a) / SR, wave=a[::4], power_db=10 * np.log10(P + 1e-10),
               mel=ours[:, :n], filters=W, max_diff_hf=diff, n_frames=n, hf_frames=int(hf.shape[1]),
               mel_edges=mel_to_hz(np.linspace(0, hz_to_mel(8000), 82)).tolist())
    print(f"    our log-mel against transformers' WhisperFeatureExtractor: max difference {diff:.2e}", flush=True)
    assert diff < 1e-3
    return out


def compute_nyquist(cache):
    """Sampling and aliasing, measured: tones sampled at 8 kHz, and speech decimated with and without a filter."""
    from scipy.signal import resample_poly

    fs = 8000
    tones = {}
    n = 4096
    t = np.arange(n) / fs
    for f in (1000, 3000, 5000, 7000):
        x = np.sin(2 * np.pi * f * t)
        spec = np.abs(np.fft.rfft(x * np.hanning(n)))
        tones[str(f)] = float(np.fft.rfftfreq(n, 1 / fs)[spec.argmax()])
    true = np.linspace(0, 16000, 321)
    seen = np.abs(true - fs * np.round(true / fs))
    # the two sinusoids that agree at every sample: 7 kHz and 1 kHz, on 2 ms
    tt = np.linspace(0, 0.002, 400)
    ts = np.arange(0, 0.002 + 1e-12, 1 / fs)
    a = clips(cache, VOICES_TEST[1], "sentence")[0][3].astype(np.float64)
    naive = a[::4]  # every fourth sample: 4 kHz, no filter
    proper = resample_poly(a, 1, 4)  # low-pass first, then keep every fourth
    E = np.abs(np.fft.rfft(a)) ** 2
    fr = np.fft.rfftfreq(len(a), 1 / SR)
    above = float(E[fr > 2000].sum() / E.sum())

    def spec_db(x, sr, n_fft):
        P = stft_power(x, n_fft=n_fft, hop=n_fft // 4)
        return 10 * np.log10(P + 1e-10)

    out = dict(fs=fs, tones=tones, true=true, seen=seen, tt=tt, ts=ts, above2k=above,
               spec_full=spec_db(a, SR, 512)[:65], spec_naive=spec_db(naive, 4000, 128),
               spec_proper=spec_db(proper, 4000, 128))
    # how much of the decimated signal's band (0-2 kHz) is folded-in energy: the naive minus the proper spectrum
    Pn, Pp = 10 ** (out["spec_naive"] / 10), 10 ** (out["spec_proper"] / 10)
    m = min(Pn.shape[1], Pp.shape[1])
    out["folded_share"] = float(np.clip((Pn[:, :m] - Pp[:, :m]).sum() / Pn[:, :m].sum(), 0, 1))
    print(f"    tones at 8 kHz appear at {tones}; {100 * above:.1f}% of the sentence's energy is above 2 kHz", flush=True)
    assert abs(tones["7000"] - 1000) < 10 and abs(tones["5000"] - 3000) < 10
    return out


# ---------------------------------------------------------------------------
# 1952: templates; the 1970s: dynamic time warping
# ---------------------------------------------------------------------------
def dtw(A, B):
    """Dynamic time warping distance between two feature sequences (frames x dims), steps (1,0), (0,1), (1,1)."""
    n, m = len(A), len(B)
    d = ((A[:, None] - B[None]) ** 2).sum(-1)
    D = np.full((n + 1, m + 1), np.inf)
    D[0, 0] = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i, j] = d[i - 1, j - 1] + min(D[i - 1, j], D[i, j - 1], D[i - 1, j - 1])
    return D[n, m] / (n + m)


def stretch(F, n=24):
    """A feature sequence resampled to ``n`` frames: Audrey-style, every word squeezed to the same length."""
    idx = np.linspace(0, len(F) - 1, n)
    return np.stack([F[int(round(i))] for i in idx])


def compute_audrey(cache):
    feats = {}
    for v in VOICES_TRAIN + VOICES_TEST:
        for k, text, s, a in clips(cache, v, "word"):
            feats[(v, text, s)] = logmel(a, 20).T  # frames x 20
    words = sorted({t for (_, t, _) in feats}, key=DIGITS.index)
    tmpl = {w: feats[(TEMPLATE_VOICE, w, 0.9)] for w in words}  # the templates: one voice, one take
    rows = []
    for (v, w, s), F in feats.items():
        if v == TEMPLATE_VOICE and s == 0.9:
            continue
        lin = min(words, key=lambda u: ((stretch(F) - stretch(tmpl[u])) ** 2).mean())
        warp = min(words, key=lambda u: dtw(F, tmpl[u]))
        rows.append(dict(voice=v, word=w, speed=s, same=v == TEMPLATE_VOICE, lin=lin == w, dtw=warp == w))
    # templates from all ten training voices (nearest of all), tested on the two held-out voices
    many = [(w, F) for (v, w, s), F in feats.items() if v in VOICES_TRAIN]
    held = [(w, F) for (v, w, s), F in feats.items() if v in VOICES_TEST]
    multi = np.mean([min(many, key=lambda t: dtw(F, t[1]))[0] == w for w, F in held])

    def acc(sel, key):
        r = [x[key] for x in rows if sel(x)]
        return float(np.mean(r)) if r else float("nan")

    out = dict(words=words, template_voice=TEMPLATE_VOICE,
               same_lin=acc(lambda x: x["same"], "lin"), same_dtw=acc(lambda x: x["same"], "dtw"),
               other_lin=acc(lambda x: not x["same"], "lin"), other_dtw=acc(lambda x: not x["same"], "dtw"),
               multi_dtw=float(multi), n_other=sum(not x["same"] for x in rows), n_same=sum(x["same"] for x in rows),
               n_templates=len(many),
               per_voice={v: acc(lambda x, v=v: x["voice"] == v, "dtw") for v in VOICES_TRAIN + VOICES_TEST})
    w_ex = "seven" if "seven" in words else words[-1]
    ex = feats[(TEMPLATE_VOICE, w_ex, 1.1)], tmpl[w_ex]
    out["example_a"], out["example_b"] = ex[0], ex[1]
    n, m = len(ex[0]), len(ex[1])
    d = ((ex[0][:, None] - ex[1][None]) ** 2).sum(-1)
    D = np.full((n + 1, m + 1), np.inf)
    D[0, 0] = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i, j] = d[i - 1, j - 1] + min(D[i - 1, j], D[i, j - 1], D[i - 1, j - 1])
    i, j, path = n, m, []
    while i > 0 and j > 0:
        path.append((i - 1, j - 1))
        k = int(np.argmin([D[i - 1, j - 1], D[i - 1, j], D[i, j - 1]]))
        i, j = (i - 1, j - 1) if k == 0 else (i - 1, j) if k == 1 else (i, j - 1)
    out["example_cost"], out["example_path"] = d, np.array(path[::-1])
    print("    templates from {}: same voice {:.0%} (stretched) / {:.0%} (DTW); other voices {:.0%} / {:.0%}; "
          "ten voices' templates on held-out voices {:.0%}".format(TEMPLATE_VOICE, out["same_lin"], out["same_dtw"],
                                                                    out["other_lin"], out["other_dtw"], multi),
          flush=True)
    return out


# ---------------------------------------------------------------------------
# A small neural codec: convolutions, residual vector quantization, quantizer dropout
# ---------------------------------------------------------------------------
CODEC_STAGES = 8
CODEC_K = 256
CODEC_D = 64
CODEC_STEPS = 3000
CODEC_SEEDS = [0, 1]
CODEC_CROP = 8000
CODEC_HZ = SR // 320  # 50 frames a second


def codec_nets(C=8, D=CODEC_D):
    import torch.nn as nn

    class Res(nn.Module):
        def __init__(s, c, dil):
            super().__init__()
            s.b = nn.Sequential(nn.ELU(), nn.Conv1d(c, c, 7, padding=3 * dil, dilation=dil), nn.ELU(), nn.Conv1d(c, c, 1))

        def forward(s, x):
            return x + s.b(x)

    enc, c = [nn.Conv1d(1, C, 7, padding=3)], C
    for st in (2, 4, 5, 8):
        enc += [Res(c, 1), Res(c, 3), nn.ELU(), nn.Conv1d(c, 2 * c, 2 * st, stride=st, padding=st // 2 + st % 2)]
        c *= 2
    enc += [nn.ELU(), nn.Conv1d(c, D, 3, padding=1)]
    dec = [nn.Conv1d(D, c, 7, padding=3)]
    for st in (8, 5, 4, 2):
        dec += [nn.ELU(), nn.ConvTranspose1d(c, c // 2, 2 * st, stride=st, padding=st // 2 + st % 2,
                                             output_padding=st % 2), Res(c // 2, 1), Res(c // 2, 3)]
        c //= 2
    dec += [nn.ELU(), nn.Conv1d(c, 1, 7, padding=3), nn.Tanh()]
    return nn.Sequential(*enc), nn.Sequential(*dec)


class RVQ:
    """Residual vector quantization: stage s quantizes what stages 1..s-1 left over.  Codebooks learn by EMA, and a
    code unused for 100 steps restarts at a random residual (SoundStream and EnCodec do both)."""

    def __init__(self, seed, n=CODEC_STAGES, K=CODEC_K, D=CODEC_D):
        import torch

        self.g = torch.Generator().manual_seed(seed)
        self.C = [torch.randn(K, D, generator=self.g) * 0.1 for _ in range(n)]
        self.n_ = [torch.ones(K) for _ in range(n)]
        self.sum_ = [c.clone() for c in self.C]
        self.idle = [torch.zeros(K) for _ in range(n)]
        self.K = K

    def __call__(self, z, n_q, train=True):
        """z: (N, D).  Returns the quantized sum (straight-through), the codes (N, n_q) and the commitment loss."""
        import torch
        import torch.nn.functional as F

        res, total, codes, commit = z, torch.zeros_like(z), [], 0.0
        for s in range(n_q):
            C = self.C[s]
            d = (res * res).sum(1, keepdim=True) - 2 * res @ C.T + (C * C).sum(1)[None]
            k = d.argmin(1)
            e = C[k]
            commit = commit + F.mse_loss(res, e.detach())
            if train:
                with torch.no_grad():
                    oh = F.one_hot(k, self.K).float()
                    cnt = oh.sum(0)
                    self.n_[s].mul_(0.99).add_(cnt, alpha=0.01)
                    self.sum_[s].mul_(0.99).add_(oh.T @ res.detach(), alpha=0.01)
                    self.C[s] = self.sum_[s] / self.n_[s].clamp_min(1e-5)[:, None]
                    self.idle[s] = torch.where(cnt > 0, torch.zeros_like(self.idle[s]), self.idle[s] + 1)
                    dead = (self.idle[s] >= 100).nonzero()[:, 0]
                    if len(dead):
                        pick = torch.randint(0, len(res), (len(dead),), generator=self.g)
                        self.C[s][dead] = res.detach()[pick]
                        self.sum_[s][dead] = res.detach()[pick]
                        self.n_[s][dead] = 1.0
                        self.idle[s][dead] = 0
            total = total + e
            res = res - e.detach()
            codes.append(k)
        return z + (total - z).detach(), torch.stack(codes, 1), commit

    def state(self):
        return dict(C=self.C, n=self.n_, sum=self.sum_, idle=self.idle, g=self.g.get_state())

    def load(self, st):
        self.C, self.n_, self.sum_, self.idle = st["C"], st["n"], st["sum"], st["idle"]
        self.g.set_state(st["g"])


def spec_loss(x, y):
    import torch

    tot = 0.0
    for n in (128, 256, 512, 1024):
        w = torch.hann_window(n)
        X = torch.stft(x, n, n // 4, window=w, return_complex=True).abs()
        Y = torch.stft(y, n, n // 4, window=w, return_complex=True).abs()
        tot = tot + (torch.log(X + 1e-5) - torch.log(Y + 1e-5)).abs().mean() + \
            torch.linalg.norm(X - Y) / (torch.linalg.norm(X) + 1e-7)
    return tot / 4


def codec_data(cache):
    tr = [a for v in VOICES_TRAIN for k, t, s, a in clips(cache, v) if k in ("sentence", "string")]
    te = [(t, a) for v in VOICES_TEST for k, t, s, a in clips(cache, v, "sentence")]
    return tr, te


def encode_decode(enc, dec, rvq, a, n_q):
    import torch

    with torch.no_grad():
        n = int(math.ceil(len(a) / 320) * 320)
        x = torch.tensor(np.pad(a, (0, n - len(a))), dtype=torch.float32)[None, None]
        z = enc(x)
        zf = z.permute(0, 2, 1).reshape(-1, CODEC_D)
        q, codes, _ = rvq(zf, n_q, train=False)
        y = dec(q.reshape(1, -1, CODEC_D).permute(0, 2, 1))[0, 0, :len(a)].numpy()
    return y, codes.numpy()


def train_codec(cache, seed, log=print):
    import torch

    threads()
    tr, te = codec_data(cache)
    torch.manual_seed(seed)
    enc, dec = codec_nets()
    rvq = RVQ(seed)
    opt = torch.optim.Adam([*enc.parameters(), *dec.parameters()], lr=1e-3)
    g = rng(500 + seed)
    steps = max(30, int(CODEC_STEPS * SCALE))
    checks = sorted({min(c, steps) for c in (0, 100, 300, 800, 1600, 3000)})
    ex_text, ex = te[0]
    ckpt = cache.dir / "models" / f"codec_s{seed}.ckpt"
    ckpt.parent.mkdir(parents=True, exist_ok=True)
    start, curve, snaps = 0, [], []
    if ckpt.exists():
        ck = torch.load(ckpt, weights_only=False)
        if ck["steps"] == steps:
            enc.load_state_dict(ck["enc"])
            dec.load_state_dict(ck["dec"])
            opt.load_state_dict(ck["opt"])
            rvq.load(ck["rvq"])
            g.bit_generator.state = ck["g"]
            torch.set_rng_state(ck["torch"])
            start, curve, snaps = ck["step"], ck["curve"], ck["snaps"]
            log(f"    codec seed {seed}: resuming at step {start}")
    t0 = time.time()
    for step in range(start, steps + 1):
        if step % 250 == 0 and step > start:
            tmp = ckpt.with_suffix(".tmp")
            torch.save(dict(enc=enc.state_dict(), dec=dec.state_dict(), opt=opt.state_dict(), rvq=rvq.state(),
                            g=g.bit_generator.state, torch=torch.get_rng_state(), step=step, curve=curve, snaps=snaps,
                            steps=steps), tmp)
            tmp.replace(ckpt)
        if step in checks and not any(s_[0] == step for s_ in snaps):
            y, _ = encode_decode(enc, dec, rvq, ex, CODEC_STAGES)
            snaps.append((step, whisper_logmel(y, pad_to=0)[:, :400].astype(np.float32)))
        if step == steps:
            break
        xs = []
        for _ in range(8):
            a = tr[int(g.integers(len(tr)))]
            if len(a) <= CODEC_CROP:
                a = np.pad(a, (0, CODEC_CROP + 1 - len(a)))
            s0 = int(g.integers(0, len(a) - CODEC_CROP))
            xs.append(a[s0:s0 + CODEC_CROP] * g.uniform(0.6, 1.0))
        x = torch.tensor(np.stack(xs), dtype=torch.float32)[:, None]
        n_q = int(g.integers(1, CODEC_STAGES + 1))  # quantizer dropout: one model for every bitrate
        z = enc(x)
        zf = z.permute(0, 2, 1).reshape(-1, CODEC_D)
        q, _, commit = rvq(zf, n_q)
        y = dec(q.reshape(len(x), -1, CODEC_D).permute(0, 2, 1))[..., :CODEC_CROP]
        sl = spec_loss(x[:, 0], y[:, 0])
        loss = sl + 0.1 * (x - y).abs().mean() + 0.25 * commit
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step % 25 == 0:
            curve.append([step, float(sl), n_q])
        if step % 500 == 0:
            log(f"    codec seed {seed}: step {step}/{steps}, spectral loss {float(sl):.3f}, "
                f"{(time.time() - t0) / max(1, step - start + 1):.2f} s/step")
    return enc, dec, rvq, curve, snaps, (ckpt, steps)


def mel_distance(a, b):
    A, B = whisper_logmel(a, pad_to=0), whisper_logmel(b, pad_to=0)
    m = min(A.shape[1], B.shape[1])
    return float(np.abs(A[:, :m] - B[:, :m]).mean())


def compute_codec(cache):
    tr, te = codec_data(cache)
    stages = [1, 2, 4, 8]
    part = cache.partial("codec", dict(steps=int(CODEC_STEPS * SCALE), seeds=CODEC_SEEDS, stages=stages, v=2))
    n_wer = min(len(te), max(2, int(12 * min(1, SCALE * 4))))
    refs = [t for t, _ in te[:n_wer]]
    for seed in CODEC_SEEDS:
        key = f"s{seed}"
        if key in part:
            continue
        enc, dec, rvq, curve, snaps, (ckpt, steps) = train_codec(cache, seed)
        rows = {}
        for nq in stages:
            outs = [encode_decode(enc, dec, rvq, a, nq) for _, a in te]
            rows[str(nq)] = dict(mel=float(np.mean([mel_distance(a, y) for (_, a), (y, _) in zip(te, outs)])),
                                 hyps=transcribe([y for y, _ in outs[:n_wer]]))
        piece = dict(curve=curve, rows=rows, snaps=[[s_, m.tolist()] for s_, m in snaps])
        if seed == CODEC_SEEDS[0]:
            ex_t, ex = te[0]
            piece["example"] = dict(text=ex_t, orig=whisper_logmel(ex, pad_to=0)[:, :400].tolist(),
                                    rec={str(nq): whisper_logmel(encode_decode(enc, dec, rvq, ex, nq)[0], pad_to=0)[:, :400].tolist()
                                         for nq in stages},
                                    codes=encode_decode(enc, dec, rvq, ex, CODEC_STAGES)[1].tolist())
            usage = []
            import torch

            with torch.no_grad():
                allc = np.concatenate([encode_decode(enc, dec, rvq, a, CODEC_STAGES)[1] for _, a in te])
            for s in range(CODEC_STAGES):
                cnt = np.bincount(allc[:, s], minlength=CODEC_K)
                p = cnt / cnt.sum()
                usage.append(float(np.exp(-(p[p > 0] * np.log(p[p > 0])).sum())))
            piece["perplexity"] = usage
            piece["params"] = int(sum(p.numel() for p in enc.parameters()) + sum(p.numel() for p in dec.parameters()))
        part[key] = piece
        ckpt.unlink(missing_ok=True)
    orig_hyps = transcribe([a for _, a in te[:n_wer]])
    out = dict(stages=stages, hz=CODEC_HZ, bits=int(math.log2(CODEC_K)), seeds=CODEC_SEEDS, refs=refs,
               orig_hyps=orig_hyps, orig_wer=wer_many(refs, orig_hyps), n_test=len(te), n_wer=n_wer,
               train_seconds=float(sum(len(a) for a in tr) / SR), pcm_bps=16 * SR, steps=int(CODEC_STEPS * SCALE))
    for seed in CODEC_SEEDS:
        p = part[f"s{seed}"]
        out[f"curve_s{seed}"] = np.array(p["curve"])
        for nq in stages:
            r = p["rows"][str(nq)]
            out[f"mel_s{seed}_{nq}"] = r["mel"]
            out[f"wer_s{seed}_{nq}"] = wer_many(refs, r["hyps"])
            out[f"hyps_s{seed}_{nq}"] = r["hyps"]
    p0 = part[f"s{CODEC_SEEDS[0]}"]
    out["snap_steps"] = [s_ for s_, _ in p0["snaps"]]
    out["snaps"] = np.array([m for _, m in p0["snaps"]], np.float32)
    out["ex_text"] = p0["example"]["text"]
    out["ex_orig"] = np.array(p0["example"]["orig"], np.float32)
    for nq in stages:
        out[f"ex_rec{nq}"] = np.array(p0["example"]["rec"][str(nq)], np.float32)
    out["ex_codes"] = np.array(p0["example"]["codes"])
    out["perplexity"], out["params"] = p0["perplexity"], p0["params"]
    print("    codec: " + "; ".join(f"{nq} stages ({nq * 8 * CODEC_HZ} bps): mel {np.mean([out[f'mel_s{s}_{nq}'] for s in CODEC_SEEDS]):.3f}, "
                                      f"WER {np.mean([out[f'wer_s{s}_{nq}'] for s in CODEC_SEEDS]):.0%}" for nq in stages)
          + f"; original WER {out['orig_wer']:.0%}", flush=True)
    return out


# ---------------------------------------------------------------------------
# Whisper
# ---------------------------------------------------------------------------
_whisper: dict = {}


def whisper_model():
    if not _whisper:
        import torch
        from transformers import WhisperForConditionalGeneration, WhisperProcessor

        threads()
        _whisper["proc"] = WhisperProcessor.from_pretrained("openai/whisper-base.en")
        _whisper["model"] = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base.en").eval()
        torch.manual_seed(0)
    return _whisper["proc"], _whisper["model"]


def transcribe(audios, batch=4, ids=False):
    import torch

    proc, model = whisper_model()
    out, tok = [], []
    for i in range(0, len(audios), batch):
        f = proc([np.asarray(a, np.float32) for a in audios[i:i + batch]], sampling_rate=SR, return_tensors="pt")
        with torch.no_grad():
            seq = model.generate(f.input_features, max_new_tokens=96)
        out += [s.strip() for s in proc.batch_decode(seq, skip_special_tokens=True)]
        tok += [s.tolist() for s in seq]
    return (out, tok) if ids else out


NUMWORDS = {str(i): w for i, w in enumerate(DIGITS)}


def words(s: str) -> list[str]:
    s = s.lower().replace("-", " ")
    s = re.sub(r"\d", lambda m: f" {NUMWORDS[m.group(0)]} ", s)
    return re.sub(r"[^a-z' ]", " ", s).split()


def edits(a, b) -> int:
    d = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        prev, d[0] = d[0], i
        for j, y in enumerate(b, 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (x != y))
    return d[len(b)]


def wer_many(refs, hyps) -> float:
    e = sum(edits(words(r), words(h)) for r, h in zip(refs, hyps))
    return e / max(1, sum(len(words(r)) for r in refs))


def compute_whisper(cache):
    proc, model = whisper_model()
    sents = [(t, a) for v in VOICES_TEST for k, t, s, a in clips(cache, v, "sentence")]
    strs = [(t, a) for v in VOICES_TEST for k, t, s, a in clips(cache, v, "string")]
    hyp_s, ids_s = transcribe([a for _, a in sents], ids=True)
    hyp_d = transcribe([a for _, a in strs])
    errs = [(r, h) for (r, _), h in zip(sents, hyp_s) if words(r) != words(h)]
    t0, a0 = sents[0]
    toks = [proc.tokenizer.convert_ids_to_tokens(int(i)) for i in ids_s[0]]
    n_par = sum(p.numel() for p in model.parameters())
    secs = sum(len(a) for _, a in sents) / SR
    n_tok = sum(len([i for i in s if i < 50257]) for s in ids_s)
    cfg = model.config
    out = dict(refs=[t for t, _ in sents], hyps=hyp_s, wer=wer_many([t for t, _ in sents], hyp_s),
               digit_refs=[t for t, _ in strs], digit_hyps=hyp_d, digit_wer=wer_many([t for t, _ in strs], hyp_d),
               errors=errs, example_text=t0, example_ids=ids_s[0], example_tokens=toks,
               example_mel=whisper_logmel(a0)[:, :int(len(a0) / 160) + 30], example_seconds=len(a0) / SR,
               params=int(n_par), enc_layers=int(cfg.encoder_layers), dec_layers=int(cfg.decoder_layers),
               d_model=int(cfg.d_model), vocab=int(cfg.vocab_size), tokens_per_second=n_tok / secs,
               n_sents=len(sents), n_strings=len(strs), seconds=secs)
    print(f"    whisper base.en: WER {out['wer']:.1%} on {len(sents)} held-out sentences, {out['digit_wer']:.1%} "
          f"on {len(strs)} digit strings; {n_par / 1e6:.1f}M parameters", flush=True)
    return out


# ---------------------------------------------------------------------------
# CTC: a small recognizer for digit strings
# ---------------------------------------------------------------------------
ALPHA = "_ abcdefghijklmnopqrstuvwxyz"  # 0 is CTC's blank
CTC_STEPS = 2000
CTC_SEEDS = [0, 1, 2]
CTC_CHECKS = [0, 50, 150, 400, 900, 2000]


def ctc_net(width=96):
    """A small convolutional recognizer: a strided convolution to 20 ms frames, then five residual convolutions with
    growing dilation (each frame sees about 1.3 s of context, both ways), then a letter per frame."""
    import torch.nn as nn

    class Res(nn.Module):
        def __init__(s, c, dil):
            super().__init__()
            s.conv = nn.Conv1d(c, c, 3, padding=dil, dilation=dil)
            s.norm = nn.GroupNorm(1, c)

        def forward(s, x):
            return x + nn.functional.gelu(s.norm(s.conv(x)))

    class Net(nn.Module):
        def __init__(s):
            super().__init__()
            s.inp = nn.Sequential(nn.Conv1d(40, width, 5, stride=2, padding=2), nn.GELU())
            s.body = nn.Sequential(*[Res(width, d) for d in (1, 2, 4, 8, 16)])
            s.out = nn.Conv1d(width, len(ALPHA), 1)

        def forward(s, x):  # x: (B, 40, T) -> log-probabilities (B, T/2, labels)
            return s.out(s.body(s.inp(x))).transpose(1, 2).log_softmax(-1)

    return Net()


def labels_of(text: str) -> list[int]:
    return [ALPHA.index(c) for c in text]


def greedy(lp) -> str:
    best = lp.argmax(-1)
    out, prev = [], 0
    for b in best:
        if b != prev and b != 0:
            out.append(ALPHA[b])
        prev = b
    return "".join(out).strip()


def ctc_lattice(lp: np.ndarray, text: str):
    """The forward algorithm on CTC's lattice: blanks between and around the letters, and the rule that a path may
    skip a blank only between two different letters.  Returns log alpha, the posterior occupancy of each node (from
    alpha and beta), the best path (Viterbi) and the total log-probability of the transcript."""
    lab = labels_of(text)
    ext = [0]
    for c in lab:
        ext += [c, 0]
    T, S = len(lp), len(ext)
    la = np.full((T, S), -np.inf)
    lv = np.full((T, S), -np.inf)
    bp = np.zeros((T, S), np.int64)
    la[0, 0], la[0, 1] = lp[0, ext[0]], lp[0, ext[1]]
    lv[0, :2] = la[0, :2]
    for t in range(1, T):
        for s in range(S):
            cands = [s, s - 1] + ([s - 2] if s >= 2 and ext[s] != 0 and ext[s] != ext[s - 2] else [])
            cands = [c for c in cands if c >= 0]
            vals = [la[t - 1, c] for c in cands]
            m = max(vals)
            la[t, s] = (m + math.log(sum(math.exp(v - m) for v in vals)) if m > -np.inf else -np.inf) + lp[t, ext[s]]
            vv = [lv[t - 1, c] for c in cands]
            k = int(np.argmax(vv))
            lv[t, s], bp[t, s] = vv[k] + lp[t, ext[s]], cands[k]
    lb = np.full((T, S), -np.inf)
    lb[T - 1, S - 1], lb[T - 1, S - 2] = lp[T - 1, ext[S - 1]], lp[T - 1, ext[S - 2]]
    for t in range(T - 2, -1, -1):
        for s in range(S):
            cands = [s, s + 1] + ([s + 2] if s + 2 < S and ext[s] != 0 and ext[s] != ext[s + 2] else [])
            cands = [c for c in cands if c < S]
            vals = [lb[t + 1, c] for c in cands]
            m = max(vals)
            lb[t, s] = (m + math.log(sum(math.exp(v - m) for v in vals)) if m > -np.inf else -np.inf) + lp[t, ext[s]]
    total = np.logaddexp(la[T - 1, S - 1], la[T - 1, S - 2])
    gamma = np.exp(la + lb - lp[:, ext] - total)  # alpha_t(s) beta_t(s) / y_t(s) / P
    s = S - 1 if lv[T - 1, S - 1] >= lv[T - 1, S - 2] else S - 2
    path = [s]
    for t in range(T - 1, 0, -1):
        s = bp[t, s]
        path.append(s)
    return la, gamma, np.array(path[::-1]), float(total), ext


def ctc_utterance(g, words_by_voice, strings, voices):
    """A training utterance: three to five digit words from one voice, joined by short gaps; or a whole string."""
    v = voices[int(g.integers(len(voices)))]
    if g.uniform() < 0.3 and strings[v]:
        text, a = strings[v][int(g.integers(len(strings[v])))]
    else:
        n = int(g.integers(3, 6))
        ws = [words_by_voice[v][int(g.integers(len(words_by_voice[v])))] for _ in range(n)]
        parts = []
        for w, clip in ws:
            parts += [np.zeros(int(g.uniform(0.02, 0.15) * SR), np.float32), clip]
        parts.append(np.zeros(int(0.05 * SR), np.float32))
        text, a = " ".join(w for w, _ in ws), np.concatenate(parts)
    a = a * g.uniform(0.5, 1.0) + g.normal(0, 10 ** g.uniform(-3.5, -2.5), len(a)).astype(np.float32)
    return text, a


def spec_augment(F_, g, n_freq=2, max_f=6, n_time=2, max_t=12):
    """SpecAugment (Park et al., 2019), lightly: blank out a few bands of frequency and stretches of time."""
    F_ = F_.copy()
    for _ in range(n_freq):
        w = int(g.integers(0, max_f + 1))
        f0 = int(g.integers(0, F_.shape[0] - w + 1))
        F_[f0:f0 + w] = 0.0
    for _ in range(n_time):
        w = int(g.integers(0, min(max_t, F_.shape[1] // 5) + 1))
        t0 = int(g.integers(0, F_.shape[1] - w + 1))
        F_[:, t0:t0 + w] = 0.0
    return F_


def run_ctc(cache, seed, log=print):
    import torch
    import torch.nn.functional as F

    threads()
    wv = {v: [(t, a) for k, t, s, a in clips(cache, v, "word")] for v in VOICES_TRAIN}
    sv = {v: [(t, a) for k, t, s, a in clips(cache, v, "string")] for v in VOICES_TRAIN}
    test = [(t, a) for v in VOICES_TEST for k, t, s, a in clips(cache, v, "string")]
    seen = [(t, a) for v in VOICES_TRAIN for t, a in sv[v]]
    torch.manual_seed(seed)
    net = ctc_net()
    opt = torch.optim.Adam(net.parameters(), lr=1e-3)
    g = rng(300 + seed)
    steps = max(30, int(CTC_STEPS * SCALE))
    checks = sorted({min(c, steps) for c in CTC_CHECKS})
    ex_t, ex_a = test[0]
    ex_x = torch.tensor(logmel(ex_a))[None]
    curve, snaps = [], []

    def evaluate(data):
        net.eval()
        with torch.no_grad():
            hyps = [greedy(net(torch.tensor(logmel(a))[None])[0].numpy()) for _, a in data]
        net.train()
        return hyps

    for step in range(steps + 1):
        if step in checks:
            net.eval()
            with torch.no_grad():
                lp = net(ex_x)[0].numpy()
            net.train()
            snaps.append(dict(step=step, lp=lp, text=greedy(lp)))
        if step == steps:
            break
        batch = [ctc_utterance(g, wv, sv, VOICES_TRAIN) for _ in range(16)]
        feats = [spec_augment(logmel(a), g) for _, a in batch]
        for gr in opt.param_groups:  # warm up for 100 steps, then a cosine down to a tenth
            gr["lr"] = 1e-3 * (min(1.0, (step + 1) / 100) * (0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * step / steps))))
        T = max(f.shape[1] for f in feats)
        x = torch.tensor(np.stack([np.pad(f, ((0, 0), (0, T - f.shape[1]))) for f in feats]))
        lens = torch.tensor([(f.shape[1] + 1) // 2 for f in feats])
        tg = [torch.tensor(labels_of(t)) for t, _ in batch]
        lp = net(x)
        loss = F.ctc_loss(lp.transpose(0, 1), torch.cat(tg), lens, torch.tensor([len(t_) for t_ in tg]), blank=0,
                          zero_infinity=True)
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(net.parameters(), 5.0)
        opt.step()
        if step % 10 == 0:
            curve.append([step, float(loss.detach())])
    hyps = evaluate(test)
    hyps_seen = evaluate(seen)
    net.eval()
    with torch.no_grad():
        lp = net(ex_x)[0].numpy()
        # the lattice's total agrees with torch's own CTC loss (an invariant of the forward algorithm)
        la, gamma, path, total, ext = ctc_lattice(lp, ex_t)
        ref = -F.ctc_loss(torch.tensor(lp)[:, None], torch.tensor([labels_of(ex_t)]), torch.tensor([len(lp)]),
                          torch.tensor([len(ex_t)]), blank=0, reduction="sum").item()
    assert abs(total - ref) < 1e-3 * max(1, abs(ref)), (total, ref)
    n_par = sum(p.numel() for p in net.parameters())
    return dict(seed=seed, curve=curve, hyps=hyps, hyps_seen=hyps_seen,
                wer=wer_many([t for t, _ in test], hyps), wer_seen=wer_many([t for t, _ in seen], hyps_seen),
                snaps=[dict(step=s["step"], lp=s["lp"].tolist(), text=s["text"]) for s in snaps],
                lattice=dict(log_alpha=la.tolist(), gamma=gamma.tolist(), path=path.tolist(), total=total, ext=ext,
                             text=ex_t, lp=lp.tolist()), params=int(n_par), steps=steps)
