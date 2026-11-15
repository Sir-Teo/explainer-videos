"""Lab 66: generative audio's representations, computed: mu-law against plain 8-bit samples, a residual vector-quantizing
codec at one to four tokens a frame, a Fréchet distance between sets of sounds, and a spread-spectrum watermark with its
detector."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import Clip, concat
from explainer.music.monochord import genaudio as G

TITLE = "Generative audio's representations, computed"
GOAL = ("Compand samples with mu-law, quantize spectral frames into codec tokens stage on stage, compare sets of sounds "
        "by a Fréchet distance, and hide and find a watermark under music.")
TASKS = [
    "Change STAGES. How much does each extra codebook buy, in dB of spectral distance and in bits a second?",
    "Change STRENGTH, the watermark's level. How quiet can it be and still be found through a time shift?",
    "Change K, the codebook size. Is a bigger codebook or another stage the better use of eight more bits?",
]
STAGES = [1, 2, 3, 4]
STRENGTH = -35.0
K = 64
SR = G.SR16


def note(f, seconds, bright, rng):
    t = np.arange(int(seconds * SR)) / SR
    env = np.minimum(1, t / 0.03) * np.exp(-t * 2.5)
    y = sum((bright ** (k - 1)) * np.sin(2 * np.pi * f * k * t + rng.uniform(0, 6.28)) for k in range(1, 12) if f * k < 7500)
    return env * y


def melody(seed, n=16):
    rng = np.random.default_rng(seed)
    scale = [0, 2, 4, 5, 7, 9, 11, 12]
    out = []
    for _ in range(n):
        m = 60 + scale[int(rng.integers(len(scale)))]
        out.append(note(440 * 2 ** ((m - 69) / 12), float(rng.choice([0.25, 0.5])), float(rng.uniform(0.4, 0.8)), rng))
    y = np.concatenate(out)
    return y / np.max(np.abs(y)) * 0.8


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    y = melody(seed + 100)
    quiet = y * 0.05
    snr = lambda a: 10 * np.log10(np.sum(quiet ** 2) / np.sum((a - quiet) ** 2))
    s_mu, s_lin = snr(G.unmulaw(G.mulaw(quiet))), snr(G.linear8(quiet))
    lab.row("a quiet melody in 8 bits: equal steps, mu-law (signal to noise)", f"{s_lin:.0f} dB, {s_mu:.0f} dB")
    assert s_mu > s_lin + 10
    train = np.concatenate([melody(seed + k) for k in range(12)])
    F = G.frames(train)
    q = G.RVQ(max(STAGES), K, seed=seed).fit(F[rng.choice(len(F), min(len(F), 4000), replace=False)])
    Ft = G.frames(y)
    dists, clips = {}, [Clip(G.to48(y), 48000)]
    for st in STAGES:
        rec = G.from_frames(q.decode(q.encode(Ft, st)), len(y), iters=40)
        dists[st] = G.spectral_distance(y, rec)
        bits = st * np.log2(K) * SR / G.HOP / 1000
        lab.row(f"codec, {st} token(s) a frame of {K} codewords: kbit/s, spectral distance", f"{bits:.2f}, {dists[st]:.1f} dB")
        clips.append(Clip(G.to48(rec / (np.max(np.abs(rec)) + 1e-12) * 0.8), 48000))
    assert dists[max(STAGES)] < dists[min(STAGES)]
    gl = G.spectral_distance(y, G.from_frames(Ft, len(y), iters=40))
    lab.row("no quantization at all (the phase alone invented)", f"{gl:.1f} dB")
    def emb(ys):
        """Half-second chunks as 9 log band energies."""
        rows = [np.log(np.mean(np.abs(G.stft(z[i:i + SR // 2])) ** 2, axis=1)[::32] + 1e-9)
                for z in ys for i in range(0, len(z) - SR // 2, SR // 4)]
        return np.vstack(rows)
    real = emb([melody(seed + 200 + k) for k in range(4)])
    other = emb([melody(seed + 300 + k) for k in range(4)])
    noise = emb([rng.standard_normal(len(y)) * 0.2 for _ in range(4)])
    d_same, d_noise = G.frechet(real, other), G.frechet(real, noise)
    lab.row("Fréchet distance: two sets of melodies; melodies against noise", f"{d_same:.1f}; {d_noise:.1f}")
    assert d_same < d_noise
    key = 4321
    m = G.watermark(y, key, strength_db=STRENGTH)
    z = G.detect(m, key)
    zs = G.detect(np.r_[np.zeros(25), m[:-25]], key, max_lag=40)
    lab.row(f"watermark {STRENGTH:.0f} dB down: score marked; shifted (searched); unmarked; wrong key",
            f"{z:.1f}; {zs:.1f}; {G.detect(y, key):.1f}; {G.detect(m, key + 1):.1f}")
    if STRENGTH >= -40:
        assert z > 5
    order = list(rng.permutation(len(STAGES)))
    marked_first = bool(rng.integers(2))
    pair = [m, y] if marked_first else [y, m]
    lab.audio = concat([clips[0]] + [clips[1 + i] for i in order] + [Clip(G.to48(p), 48000) for p in pair], gap=0.6)
    lab.row("ear problem: the melody, then the codec at shuffled stages, then two phrases (one marked); which is which? (listen first)",
            f"stages {', '.join(str(STAGES[i]) for i in order)}; marked: {'first' if marked_first else 'second'}")
    fig, (ax1, ax2) = labs.figure(2)
    ax1.plot(STAGES, [dists[s] for s in STAGES], "o-", color=labs.GOLD)
    ax1.axhline(gl, color="0.6", ls="--")
    ax1.set_xlabel("tokens a frame")
    ax1.set_ylabel("spectral distance (dB)")
    ax2.imshow(np.log(np.abs(G.stft(y)) + 1e-4), origin="lower", aspect="auto", cmap="magma")
    ax2.set_xlabel("frame")
    ax2.set_ylabel("bin")
    lab.fig = fig
    lab.note = ("Every generator needs a representation: mu-law makes a sample one of 256 classes; a codec makes a frame a few "
                "tokens, each stage cleaning up the last; a Fréchet distance compares whole sets of sounds; and a watermark "
                "rides under the music, found only with its key.")
    return lab
