"""Precompute everything numerical in Part 16 of the AI series ("Every Sense Is a Token").

    python -m videos.ai.ai16.compute              # everything missing (Part 1's books)
    python -m videos.ai.ai16.compute --force clip

Results are cached in ``.cache/ai16/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.

Items:
    bpe        byte-pair encoding learned on Part 1's books: the first merges, and for vocabularies of 500, 2,000 and
               8,000 merges, how many characters a token covers on held-out text and on the scoreboard's passage, and
               how one sentence is cut
    vq         4 x 4 patches of Part 14's letter pictures as vectors: a codebook (k-means) of 16, 64 and 256 codes;
               residual quantization, 1 to 4 stages of 16 codes; finite scalar quantization; the errors, and one
               letter rebuilt from its codes
    sound      a synthesized voice saying five vowels (a pulse train through formant resonances): its spectrogram,
               frame by frame, and the same frames as residual-quantized codes, stage by stage
    clip       a contrastive model pairing letter pictures with captions ("bold serif A"), trained with CLIP's softmax
               loss and with SigLIP's sigmoid loss: the similarity table of a batch, and how often each picks the
               right caption
"""

from __future__ import annotations

import collections
import math

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai16")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


# ---------------------------------------------------------------------------
def learn_bpe(text: str, merges: int):
    """Sennrich et al.'s byte-pair encoding over words (a word carries its leading space): the merges, in order."""
    words = collections.Counter()
    for w in text.replace("\n", " ").split(" "):
        if w:
            words[" " + w] += 1
    vocab = {tuple(w): c for w, c in words.items()}
    seqs = list(vocab.keys())
    counts = [vocab[s] for s in seqs]
    seqs = [list(s) for s in seqs]
    pairs = collections.Counter()
    where = collections.defaultdict(set)
    for i, s in enumerate(seqs):
        for a, b in zip(s, s[1:]):
            pairs[(a, b)] += counts[i]
            where[(a, b)].add(i)
    out = []
    for _ in range(merges):
        if not pairs:
            break
        (a, b), n = pairs.most_common(1)[0]
        if n < 2:
            break
        out.append((a, b))
        ab = a + b
        for i in list(where[(a, b)]):
            s, c = seqs[i], counts[i]
            for x, y in zip(s, s[1:]):  # remove this word's old pairs
                pairs[(x, y)] -= c
                if pairs[(x, y)] <= 0:
                    del pairs[(x, y)]
                where[(x, y)].discard(i)
            j, new = 0, []
            while j < len(s):
                if j + 1 < len(s) and s[j] == a and s[j + 1] == b:
                    new.append(ab)
                    j += 2
                else:
                    new.append(s[j])
                    j += 1
            seqs[i] = new
            for x, y in zip(new, new[1:]):
                pairs[(x, y)] += c
                where[(x, y)].add(i)
    return out


def apply_bpe(word: str, ranks: dict) -> list[str]:
    s = list(word)
    while len(s) > 1:
        best = min(((ranks.get((x, y), 1e9), k) for k, (x, y) in enumerate(zip(s, s[1:]))), default=(1e9, -1))
        if best[0] == 1e9:
            break
        k = best[1]
        s = s[:k] + [s[k] + s[k + 1]] + s[k + 2:]
    return s


def tokenize(text: str, ranks: dict) -> list[str]:
    toks, cache = [], {}
    for w in text.replace("\n", " ").split(" "):
        if not w:
            continue
        w = " " + w
        if w not in cache:
            cache[w] = apply_bpe(w, ranks)
        toks += cache[w]
    return toks


def compute_bpe():
    from videos.ai.ai1 import compute as c1

    train = c1.text("train")
    g = rng(2016)  # Sennrich, Haddow & Birch, 2016
    starts = g.integers(0, len(train) - 20_000, 100)
    sample = " ".join(train[s:s + 20_000] for s in starts)  # two million characters from across the books
    merges = learn_bpe(sample, 8000)
    valid, passage = c1.text("valid")[:200_000], c1.text("passage")
    sentence = "Spade sat down in the armchair and rolled a cigarette."
    out = dict(first=[a + b for a, b in merges[:40]], sizes=[500, 2000, 8000], sentence=sentence, n_merges=len(merges))
    for n in out["sizes"]:
        ranks = {p: i for i, p in enumerate(merges[:n])}
        for name, t in (("valid", valid), ("passage", passage)):
            toks = tokenize(t, ranks)
            out[f"cpt_{name}{n}"] = len(t.replace("\n", " ").replace("  ", " ")) / len(toks)
        out[f"cut{n}"] = tokenize(sentence, ranks)
    out["cut0"] = tokenize(sentence, {})
    print("    chars per token on the passage: " + ", ".join(f"{n}: {out[f'cpt_passage{n}']:.2f}" for n in out["sizes"]),
          flush=True)
    assert out["cpt_passage8000"] > out["cpt_passage500"] > 1.5
    return out


# ---------------------------------------------------------------------------
def nearest(X, C):
    """The index of each row of X's nearest code in C (squared distances by |x|^2 - 2 x.c + |c|^2)."""
    return ((C * C).sum(1)[None] - 2 * X @ C.T).argmin(1)


def kmeans(X, k, seed=0, iters=30):
    g = rng(seed)
    C = X[g.choice(len(X), k, replace=False)].copy()
    for _ in range(iters):
        a = nearest(X, C)
        for j in range(k):
            m = a == j
            C[j] = X[m].mean(0) if m.any() else X[g.integers(len(X))]
    return C, nearest(X, C)


def compute_vq():
    from videos.ai.ai14.compute import glyph_images

    imgs, labels, _ = glyph_images()
    P, n = 4, imgs.shape[1] // 4
    patches = imgs.reshape(len(imgs), n, P, n, P).transpose(0, 1, 3, 2, 4).reshape(-1, P * P)
    g = rng(2017)  # van den Oord et al., VQ-VAE
    fit = patches[g.choice(len(patches), 12_000, replace=False)]
    test_img = imgs[labels == 0][7]  # an A
    tp = test_img.reshape(n, P, n, P).transpose(0, 2, 1, 3).reshape(-1, P * P)

    def rebuild(codes_patches):
        return codes_patches.reshape(n, n, P, P).transpose(0, 2, 1, 3).reshape(n * P, n * P)

    out = dict(image=test_img, sizes=[16, 64, 256])
    evalp = patches[g.choice(len(patches), 6_000, replace=False)]
    for k in out["sizes"]:
        C, _ = kmeans(fit, k, seed=k)
        q = C[nearest(evalp, C)]
        out[f"err_vq{k}"] = float(np.sqrt(((q - evalp) ** 2).mean()))
        out[f"img_vq{k}"] = rebuild(C[nearest(tp, C)])
        if k == 16:
            out["codebook16"] = C.reshape(-1, P, P)
    # residual: quantize, then quantize what's left, with a fresh codebook of 16 each time
    res_fit, res_eval, res_t, rec_eval, rec_t = fit.copy(), evalp.copy(), tp.copy(), 0 * evalp, 0 * tp
    out["rvq_errs"] = []
    for stage in range(4):
        C, _ = kmeans(res_fit, 16, seed=100 + stage)
        res_fit = res_fit - C[nearest(res_fit, C)]
        qe = C[nearest(res_eval, C)]
        qt = C[nearest(res_t, C)]
        rec_eval, rec_t = rec_eval + qe, rec_t + qt
        res_eval, res_t = res_eval - qe, res_t - qt
        out["rvq_errs"].append(float(np.sqrt(((rec_eval - evalp) ** 2).mean())))
        out[f"img_rvq{stage + 1}"] = rebuild(rec_t)
    # finite scalar quantization: project to 4 numbers, round each to one of 5 levels (625 codes, no codebook)
    mu = fit.mean(0)
    u, s, vt = np.linalg.svd(fit - mu, full_matrices=False)
    W = vt[:4]
    z = (evalp - mu) @ W.T
    lo, hi = np.percentile((fit - mu) @ W.T, [2, 98], axis=0)
    levels = np.linspace(lo, hi, 5)
    zq = np.stack([levels[np.abs(z[:, j:j + 1] - levels[:, j][None]).argmin(1), j] for j in range(4)], 1)
    out["err_fsq"] = float(np.sqrt(((zq @ W + mu - evalp) ** 2).mean()))
    out["err_none"] = float(np.sqrt(((evalp - evalp.mean(0)) ** 2).mean()))
    print("    vq {}; rvq {}; fsq {:.3f}".format([round(out[f'err_vq{k}'], 3) for k in out["sizes"]],
                                                 np.round(out["rvq_errs"], 3), out["err_fsq"]), flush=True)
    assert out["rvq_errs"][-1] < out["rvq_errs"][0] and out["err_vq256"] < out["err_vq16"]
    return out


# ---------------------------------------------------------------------------
def compute_sound():
    sr = 16_000
    # formant frequencies (Hz) of five vowels, from Peterson & Barney's classic measurements (adult male, rounded)
    vowels = {"a": (730, 1090, 2440), "e": (530, 1840, 2480), "i": (270, 2290, 3010), "o": (570, 840, 2410),
              "u": (300, 870, 2240)}
    seg = int(0.35 * sr)
    f0 = 120.0
    sig = []
    g = rng(1952)  # Peterson & Barney, 1952
    for name, F in vowels.items():
        t = np.arange(seg) / sr
        pulses = (np.sin(2 * np.pi * f0 * (1 + 0.03 * np.sin(2 * np.pi * 3 * t)) * t) > 0.97).astype(float)
        x = pulses + 0.01 * g.normal(size=seg)
        for fc in F:  # a resonance at each formant: a two-pole filter
            r = math.exp(-math.pi * 90 / sr)
            a1, a2 = -2 * r * math.cos(2 * math.pi * fc / sr), r * r
            y = np.zeros_like(x)
            for i in range(len(x)):
                y[i] = x[i] - a1 * (y[i - 1] if i else 0) - a2 * (y[i - 2] if i > 1 else 0)
            x = y / np.abs(y).max()
        env = np.minimum(1, np.minimum(t / 0.03, (t[-1] - t) / 0.03))
        sig.append(x * env)
    sig = np.concatenate(sig)
    n_fft, hop = 512, 160  # 10 ms frames
    win = np.hanning(n_fft)
    frames = np.stack([sig[i:i + n_fft] * win for i in range(0, len(sig) - n_fft, hop)])
    spec = np.abs(np.fft.rfft(frames, axis=1))[:, :200]  # up to 6.25 kHz
    logspec = np.log(spec + 1e-3)
    logspec = (logspec - logspec.mean()) / logspec.std()
    # frames as tokens: residual quantization, 4 stages of 32 codes
    res, rec, errs = logspec.copy(), 0 * logspec, []
    for stage in range(4):
        C, a = kmeans(res, 32, seed=stage)
        q = C[a]
        rec, res = rec + q, res - q
        errs.append(float(np.sqrt(((rec - logspec) ** 2).mean())))
        if stage == 0:
            codes1 = a
    out = dict(sr=sr, wave=sig[::8], spec=logspec.T, rec_errs=errs, rec4=rec.T, codes1=codes1, vowels=list(vowels),
               frame_ms=1000 * hop / sr, n_frames=len(frames))
    assert errs[-1] < errs[0]
    return out


# ---------------------------------------------------------------------------
STYLES = ["sans", "serif", "mono"]


def styled_glyphs(seed=0):
    import glob

    from PIL import Image, ImageDraw, ImageFont

    files = sorted(glob.glob("/usr/share/fonts/truetype/dejavu/DejaVu*.ttf"))
    files = [f for f in files if "Math" not in f and "ExtraLight" not in f]
    g = rng(seed)
    imgs, caps = [], []
    for f in files:
        name = f.rsplit("/", 1)[-1].lower()
        fam = "mono" if "mono" in name else "serif" if "serif" in name else "sans"
        words = (["bold"] if "bold" in name else []) + (["italic"] if ("oblique" in name or "italic" in name) else []) + \
                (["narrow"] if "condensed" in name else []) + [fam]
        try:
            font = ImageFont.truetype(f, 15)
        except Exception:
            continue
        for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            for _ in range(2):
                im = Image.new("L", (20, 20), 0)
                dx, dy = g.uniform(-1.5, 1.5, 2)
                ImageDraw.Draw(im).text((10 + dx, 10 + dy), ch, fill=255, font=font, anchor="mm")
                imgs.append(np.asarray(im, float) / 255.0)
                caps.append(words + [ch])
    return np.array(imgs), caps


def compute_clip():
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

    torch.set_num_threads(2)
    imgs, caps = styled_glyphs()
    vocab = sorted({w for c in caps for w in c})
    X = torch.tensor(imgs.reshape(len(imgs), -1), dtype=torch.float32)
    T = torch.zeros(len(caps), len(vocab))
    for i, c in enumerate(caps):
        for w in c:
            T[i, vocab.index(w)] = 1.0
    uniq = sorted({" ".join(c) for c in caps})
    U = torch.zeros(len(uniq), len(vocab))
    for i, c in enumerate(uniq):
        for w in c.split():
            U[i, vocab.index(w)] = 1.0
    cap_id = torch.tensor([uniq.index(" ".join(c)) for c in caps])
    out = dict(vocab=vocab, n_images=len(imgs), n_captions=len(uniq))
    for loss_name in ("clip", "siglip"):
        torch.manual_seed(2021)  # Radford et al., CLIP (2021); Zhai et al., SigLIP (2023)
        img_enc = nn.Sequential(nn.Linear(400, 256), nn.GELU(), nn.Linear(256, 64))
        txt_enc = nn.Sequential(nn.Linear(len(vocab), 128), nn.GELU(), nn.Linear(128, 64))
        t_ = nn.Parameter(torch.tensor(math.log(10.0)))
        b_ = nn.Parameter(torch.tensor(-10.0))
        opt = torch.optim.Adam([*img_enc.parameters(), *txt_enc.parameters(), t_, b_], lr=2e-3)
        g = torch.Generator().manual_seed(0)
        for step in range(3000):
            i = torch.randint(0, len(X), (128,), generator=g)
            zi = F.normalize(img_enc(X[i] + 0.05 * torch.randn(128, 400, generator=g)), dim=-1)
            zt = F.normalize(txt_enc(T[i]), dim=-1)
            logits = zi @ zt.T * t_.exp()
            same = (cap_id[i][:, None] == cap_id[i][None]).float()  # duplicates of a caption in the batch are matches too
            if loss_name == "clip":  # softmax over the batch, both ways
                tgt = same / same.sum(1, keepdim=True)
                loss = -(tgt * F.log_softmax(logits, 1)).sum(1).mean() - (tgt.T * F.log_softmax(logits.T, 1)).sum(1).mean()
            else:  # every pair on its own: a yes/no question
                loss = F.binary_cross_entropy_with_logits(logits + b_, same, reduction="sum") / 128
            opt.zero_grad()
            loss.backward()
            opt.step()
        with torch.no_grad():
            zi = F.normalize(img_enc(X), dim=-1)
            zu = F.normalize(txt_enc(U), dim=-1)
            pick = (zi @ zu.T).argmax(1)
            right = pick == cap_id
            letter_right = torch.tensor([uniq[p].split()[-1] == caps[k][-1] for k, p in enumerate(pick.tolist())])
            out[f"acc_{loss_name}"] = float(right.float().mean())
            out[f"letter_{loss_name}"] = float(letter_right.float().mean())
            sel = torch.tensor(rng(3).choice(len(X), 12, replace=False))
            out[f"sim_{loss_name}"] = (zi[sel] @ F.normalize(txt_enc(T[sel]), dim=-1).T).numpy()
            if loss_name == "clip":
                out["batch_imgs"] = imgs[sel.numpy()]
                out["batch_caps"] = [" ".join(caps[k]) for k in sel.tolist()]
        print(f"    {loss_name}: right caption {out[f'acc_{loss_name}']:.1%}, right letter {out[f'letter_{loss_name}']:.1%}",
              flush=True)
    assert out["letter_clip"] > 0.8 and out["letter_siglip"] > 0.8
    return out


ITEMS = {
    "bpe": compute_bpe,
    "vq": compute_vq,
    "sound": compute_sound,
    "clip": compute_clip,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
