"""Part 23's picture-and-word experiments: a small contrastive model pairing letter pictures with captions ("bold serif
A"), trained with CLIP's softmax loss and with SigLIP's sigmoid loss, at three batch sizes, three seeds each, on the
same budget of pairs.  Measured: zero-shot retrieval of captions never seen in training, the InfoNCE estimate of the
mutual information against its log N ceiling, and how the letters survive being shrunk (the VLM chapter's question
of resolution).  Also the vision-language model arithmetic the VLM chapter shows: Qwen2-VL's dynamic-resolution token
counts and M-RoPE position ids, from the published code.
"""

from __future__ import annotations

import math
import os

import numpy as np

SCALE = float(os.environ.get("AI23_SCALE", "1"))
LOSSES = ["clip", "siglip"]
BATCHES = [16, 64, 256]
SEEDS = [0, 1, 2]
PAIRS = 384_000  # every run sees this many picture-caption pairs
HOLDOUT = 0.15
RES = [3, 4, 5, 7, 10, 20]


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def styled_glyphs(seed=0):
    from PIL import Image, ImageDraw, ImageFont

    from explainer.ai.fonts import font_files

    files = font_files("**/DejaVu*.ttf")  # /usr/share/fonts/truetype/dejavu on Linux; fetched on macOS
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


def shrink(imgs, r):
    """Pictures reduced to r x r (area averaging) and blown back up to 20 x 20: what a low input resolution keeps."""
    from PIL import Image

    out = []
    for a in imgs:
        im = Image.fromarray((a * 255).astype(np.uint8))
        small = im.resize((r, r), Image.BOX)
        out.append(np.asarray(small.resize((20, 20), Image.NEAREST), float) / 255.0)
    return np.array(out)


def data():
    imgs, caps = styled_glyphs(0)
    timgs, tcaps = styled_glyphs(1)  # the same pictures, jittered differently: a test set
    uniq = sorted({" ".join(c) for c in caps})
    vocab = sorted({w for c in caps for w in c})
    g = rng(2021)
    held = set(g.choice(uniq, int(round(HOLDOUT * len(uniq))), replace=False).tolist())
    return imgs, caps, timgs, tcaps, uniq, vocab, held


def bow(caps, vocab):
    T = np.zeros((len(caps), len(vocab)), np.float32)
    for i, c in enumerate(caps):
        for w in (c.split() if isinstance(c, str) else c):
            T[i, vocab.index(w)] = 1.0
    return T


def run(loss_name: str, B: int, seed: int, snaps_wanted=False, threads=1):
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

    torch.set_num_threads(threads)
    imgs, caps, timgs, tcaps, uniq, vocab, held = data()
    train_idx = np.array([i for i, c in enumerate(caps) if " ".join(c) not in held])
    X = torch.tensor(imgs.reshape(len(imgs), -1), dtype=torch.float32)
    T = torch.tensor(bow(caps, vocab))
    U = torch.tensor(bow(uniq, vocab))
    cap_id = torch.tensor([uniq.index(" ".join(c)) for c in caps])
    torch.manual_seed(seed)
    img_enc = nn.Sequential(nn.Linear(400, 256), nn.GELU(), nn.Linear(256, 64))
    txt_enc = nn.Sequential(nn.Linear(len(vocab), 128), nn.GELU(), nn.Linear(128, 64))
    t_ = nn.Parameter(torch.tensor(math.log(10.0)))
    b_ = nn.Parameter(torch.tensor(-10.0))
    opt = torch.optim.Adam([*img_enc.parameters(), *txt_enc.parameters(), t_, b_], lr=2e-3)
    g = torch.Generator().manual_seed(100 + seed)
    steps = max(20, int(PAIRS * SCALE) // B)
    tr = torch.tensor(train_idx)
    sel = torch.tensor(rng(3).choice(train_idx, 12, replace=False))
    checks = sorted({int(round(f * steps)) for f in (0, 0.01, 0.03, 0.08, 0.2, 0.5, 1.0)})
    snaps, losses = [], []

    def snap():
        with torch.no_grad():
            return (F.normalize(img_enc(X[sel]), dim=-1) @ F.normalize(txt_enc(T[sel]), dim=-1).T).numpy()

    for step in range(steps + 1):
        if snaps_wanted and step in checks:
            snaps.append(snap())
        if step == steps:
            break
        i = tr[torch.randint(0, len(tr), (B,), generator=g)]
        zi = F.normalize(img_enc(X[i] + 0.05 * torch.randn(B, 400, generator=g)), dim=-1)
        zt = F.normalize(txt_enc(T[i]), dim=-1)
        logits = zi @ zt.T * t_.exp()
        same = (cap_id[i][:, None] == cap_id[i][None]).float()  # copies of a caption in the batch match too
        if loss_name == "clip":  # softmax over the batch, both ways
            tgt = same / same.sum(1, keepdim=True)
            loss = -(tgt * F.log_softmax(logits, 1)).sum(1).mean() - (tgt.T * F.log_softmax(logits.T, 1)).sum(1).mean()
            loss = loss / 2
        else:  # every pair on its own: a yes-or-no question
            loss = F.binary_cross_entropy_with_logits(logits + b_, same, reduction="sum") / B
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step % max(1, steps // 150) == 0:
            losses.append((step * B, float(loss)))
    out = dict(loss=loss_name, B=B, seed=seed, steps=steps, losses=losses, temp=float(t_.exp()), bias=float(b_))
    with torch.no_grad():
        zu = F.normalize(txt_enc(U), dim=-1)
        tX = torch.tensor(timgs.reshape(len(timgs), -1), dtype=torch.float32)
        tid = np.array([uniq.index(" ".join(c)) for c in tcaps])
        is_held = np.array([" ".join(c) in held for c in tcaps])
        letters = np.array([u.split()[-1] for u in uniq])

        def accs(Ximg):
            pick = (F.normalize(img_enc(Ximg), dim=-1) @ zu.T).argmax(1).numpy()
            right = pick == tid
            let = letters[pick] == letters[tid]
            return right, let

        right, let = accs(tX)
        out.update(seen=float(right[~is_held].mean()), unseen=float(right[is_held].mean()),
                   letter_seen=float(let[~is_held].mean()), letter_unseen=float(let[is_held].mean()))
        out["res"] = {str(r): float(accs(torch.tensor(shrink(timgs, r).reshape(len(timgs), -1), dtype=torch.float32))[1].mean())
                      for r in RES}
        # the InfoNCE bound, measured on batches of N different captions (one picture each, seen captions only)
        gg = rng(900 + seed)
        seen_ids = np.unique(tid[~is_held])
        by_cap = {c: np.nonzero((tid == c) & ~is_held)[0] for c in seen_ids}
        zi_all = F.normalize(img_enc(tX), dim=-1)
        scale = float(t_.exp())
        mi = {}
        for N in BATCHES:
            vals = []
            for _ in range(30):
                cs = gg.choice(seen_ids, N, replace=False)
                ii = np.array([gg.choice(by_cap[c]) for c in cs])
                lg = (zi_all[ii] @ zu[cs].T * scale).numpy()
                lg = lg - lg.max(1, keepdims=True)
                lsm = lg - np.log(np.exp(lg).sum(1, keepdims=True))
                vals.append(math.log(N) + float(np.mean(np.diag(lsm))))
            mi[str(N)] = float(np.mean(vals))
        out["mi"] = mi
        if snaps_wanted:
            out["snaps"] = np.array(snaps).tolist()
            out["checks"] = [c * B for c in checks]
            out["batch_imgs"] = imgs[sel.numpy()].tolist()
            out["batch_caps"] = [" ".join(caps[k]) for k in sel.tolist()]
            out["sim"] = snap().tolist()
    return out


def smart_resize(height: int, width: int, factor: int = 28, min_pixels: int = 56 * 56, max_pixels: int = 28 * 28 * 1280):
    """Qwen2-VL's dynamic resolution (transformers' ``image_processing_qwen2_vl.smart_resize``, copied): each side to a
    multiple of 28 pixels (14-pixel patches, merged 2 x 2), the area kept between the bounds, the shape kept."""
    h_bar = round(height / factor) * factor
    w_bar = round(width / factor) * factor
    if h_bar * w_bar > max_pixels:
        beta = math.sqrt((height * width) / max_pixels)
        h_bar = max(factor, math.floor(height / beta / factor) * factor)
        w_bar = max(factor, math.floor(width / beta / factor) * factor)
    elif h_bar * w_bar < min_pixels:
        beta = math.sqrt(min_pixels / (height * width))
        h_bar = math.ceil(height * beta / factor) * factor
        w_bar = math.ceil(width * beta / factor) * factor
    return h_bar, w_bar


def compute_vlm_arith():
    sizes = [(224, 224), (448, 448), (720, 1280), (1080, 1920), (1600, 1200), (3000, 4000)]
    rows = []
    for h, w in sizes:
        H, W = smart_resize(h, w)
        rows.append(dict(h=h, w=w, H=H, W=W, tokens=(H // 28) * (W // 28), fixed=(336 // 14) ** 2))
    # M-RoPE (Qwen2-VL): every token gets (time, row, column); text tokens use the same number three times; an
    # image's tokens share one time and take their row and column; the text after it starts past the largest id
    seq, ids = [], []
    for k in range(3):
        seq.append(("text", k))
        ids.append((k, k, k))
    base = 3
    gh, gw = 2, 3
    for r in range(gh):
        for c in range(gw):
            seq.append(("image", r * gw + c))
            ids.append((base, base + r, base + c))
    nxt = max(max(t) for t in ids) + 1
    for k in range(3):
        seq.append(("text", 3 + k))
        ids.append((nxt + k,) * 3)
    return dict(rows=rows, mrope_kind=[s[0] for s in seq], mrope_ids=ids, grid=[gh, gw])
