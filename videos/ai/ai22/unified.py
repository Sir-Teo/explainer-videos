"""Part 22, chapter 11: one transformer that reads, draws and edits (Transfusion's recipe, at the size of a letter).

    unified   One transformer (4 layers, width 64) over sequences that mix text tokens and picture patches, trained
              with two losses at once: next-token cross-entropy on the text, and Part 21's flow matching on the
              patches of the picture it is drawing (Zhou et al. 2024). Attention is causal, except inside a
              picture, whose 25 patches all see each other. Three tasks, mixed in every batch:
                draw   "<serif> <R> [image]"                      -> the picture, from noise
                name   "[image] <R> <serif>"                       -> the letter and the family, as text
                edit   "[image] <bold> [image]"                    -> the same letter, in the bold of its font
              Pictures from the 20 training fonts; the edit is learned on 8 pairs of fonts (regular -> bold) and
              tested on the 2 pairs whose regular font is held out. Three seeds.
"""

from __future__ import annotations

import math
import os

import numpy as np

from videos.ai.ai22.base import CACHE, GL, NP, P, dataset, font_files, patches, render, score, steps, threads, unpatch

FAMS = ("sans", "serif", "mono")
BOS, BOI, EOI, BOLD, NULL = 29, 30, 31, 32, 33
V = 34
D, L, H = 64, 4, 4
SEEDS = (0, 1, 2)
N_STEPS, BB = 8000, 24  # steps; pictures per task per batch
GUIDE = 2.0
SHORTCUT = True  # see Unified.forward


def family(path: str) -> int:
    n = os.path.basename(path)
    return 2 if "Mono" in n else (1 if ("Serif" in n or "Math" in n) else 0)


def bold_pairs(files):
    """(regular, bold) pairs of font files among the 24: DejaVuSans -> DejaVuSans-Bold, X-Oblique -> X-BoldOblique,
    X-Italic -> X-BoldItalic."""
    names = {os.path.basename(f)[:-4]: f for f in files}
    out = []
    for n, f in names.items():
        if "Bold" in n or "ExtraLight" in n or "Math" in n:
            continue
        base, _, style = n.partition("-")
        tgt = f"{base}-Bold{style}" if style else f"{base}-Bold"
        if tgt in names:
            out.append((f, names[tgt]))
    return out


def net():
    import torch
    import torch.nn as nn

    class Block(nn.Module):
        """A transformer block with adaLN-Zero (chapter 6): each position's own condition sets its scales, shifts and
        gates, which start at zero."""

        def __init__(self):
            super().__init__()
            self.n1 = nn.LayerNorm(D, elementwise_affine=False)
            self.n2 = nn.LayerNorm(D, elementwise_affine=False)
            self.att = nn.MultiheadAttention(D, H, batch_first=True)
            self.mlp = nn.Sequential(nn.Linear(D, 4 * D), nn.GELU(), nn.Linear(4 * D, D))
            self.ada = nn.Linear(D, 6 * D)
            nn.init.zeros_(self.ada.weight)
            nn.init.zeros_(self.ada.bias)

        def forward(self, h, c, mask):
            s1, b1, g1, s2, b2, g2 = self.ada(c).chunk(6, -1)
            a = self.n1(h) * (1 + s1) + b1
            h = h + g1 * self.att(a, a, a, attn_mask=mask, need_weights=False)[0]
            return h + g2 * self.mlp(self.n2(h) * (1 + s2) + b2)

    class Unified(nn.Module):
        def __init__(self):
            super().__init__()
            self.tok = nn.Embedding(V, D)
            self.patch = nn.Linear(P * P, D)
            self.freq = nn.Parameter(torch.randn(D // 2) * 4.0, requires_grad=False)
            self.tmlp = nn.Sequential(nn.Linear(D, D), nn.SiLU(), nn.Linear(D, D))
            self.pos = nn.Parameter(torch.randn(1, 64, D) * 0.02)
            self.ppos = nn.Parameter(torch.randn(1, NP, D) * 0.02)  # where a patch is in its picture
            self.layers = nn.ModuleList([Block() for _ in range(L)])
            self.ctext = nn.Parameter(torch.zeros(D))  # the condition of a text position
            self.nf = nn.LayerNorm(D)
            self.lm = nn.Linear(D, V)
            self.vel = nn.Linear(D, P * P)

        def temb(self, t):
            a = t[..., None] * self.freq * 2 * math.pi
            return self.tmlp(torch.cat([torch.sin(a), torch.cos(a)], -1))

        def forward(self, layout, text, imgs, ts):
            """layout: a list of ('t', n) and ('i', k) items; text (B, n_text) token ids in order; imgs: list of
            (B, 20, 20) pictures in [-1, 1]; ts: list of (B,) noise levels (1 = clean). Returns per-position hidden
            states and the position ranges of each picture."""
            B = text.shape[0]
            parts, spans, ti, pos = [], [], 0, 0
            block, said, conds = [], [], []
            for kind, n in layout:
                if kind == "t":
                    e = self.tok(text[:, ti:ti + n])
                    parts.append(e)
                    said.append(e)
                    conds.append(self.ctext.expand(B, n, D))
                    block += list(range(pos, pos + n))
                    ti += n
                    pos += n
                else:
                    x = imgs[n]
                    c = self.temb(ts[n])
                    if SHORTCUT:  # the text so far, averaged, joins the noise level in every patch's condition
                        c = c + torch.cat(said, 1).mean(1)
                    parts.append(self.patch(patches(x)) + self.ppos + c[:, None])
                    conds.append(c[:, None].expand(B, NP, D))
                    spans.append((pos, pos + NP))
                    block += [pos] * NP  # one block: the picture's patches see each other
                    pos += NP
            h = torch.cat(parts, 1) + self.pos[:, :pos]
            blk = torch.tensor(block)
            idx = torch.arange(pos)
            allow = (idx[None, :] <= idx[:, None]) | (blk[None, :] == blk[:, None])
            cond = torch.cat(conds, 1)
            for lyr in self.layers:
                h = lyr(h, cond, ~allow)
            return self.nf(h), spans

    return Unified()


def layouts():
    return {"draw": [("t", 4), ("i", 0)],                       # BOS FAM LET BOI | picture
            "name": [("t", 2), ("i", 0), ("t", 3)],             # BOS BOI | picture | EOI LET FAM
            "edit": [("t", 2), ("i", 0), ("t", 3), ("i", 1)]}   # BOS BOI | source | EOI BOLD BOI | target


def edit_data(seed=2025):
    """For each (regular, bold) pair and letter, three small shifts, the same for both pictures."""
    files = font_files()
    pairs = bold_pairs(files)
    held = [k for k, (a, b) in enumerate(pairs) if files.index(a) >= len(files) - 4]
    g = np.random.default_rng(seed)
    src, tgt, lab, pair = [], [], [], []
    for k, (a, b) in enumerate(pairs):
        for j, ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            for _ in range(3):
                dx, dy = g.uniform(-1.5, 1.5, 2)
                src.append(render(a, ch, GL, dx, dy))
                tgt.append(render(b, ch, GL, dx, dy))
                lab.append(j)
                pair.append(k)
    return (np.array(src), np.array(tgt), np.array(lab), np.array(pair), held,
            [(os.path.basename(a)[:-4], os.path.basename(b)[:-4]) for a, b in pairs])


def train(seed, data, n_steps):
    import torch
    import torch.nn.functional as F

    X, Y, Fm, S, T, Tl = data
    torch.manual_seed(2024 + seed)  # Zhou et al., Transfusion (2024)
    m = net()
    opt = torch.optim.AdamW(m.parameters(), lr=1e-3, weight_decay=0.0)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=1e-3, total_steps=n_steps, pct_start=0.05)
    g = torch.Generator().manual_seed(seed)
    lay = layouts()
    curve, run = [], []
    for st in range(1, n_steps + 1):
        # draw: the prompt (dropped to NULL a tenth of the time, for guidance), then the noisy picture
        i = torch.randint(0, len(X), (BB,), generator=g)
        drop = torch.rand(BB, generator=g) < 0.1
        fam = torch.where(drop, torch.full_like(Fm[i], NULL), Fm[i] + 26)
        let = torch.where(drop, torch.full_like(Y[i], NULL), Y[i])
        text = torch.stack([torch.full_like(let, BOS), fam, let, torch.full_like(let, BOI)], 1)
        x1, x0, t = X[i], torch.randn(BB, GL, GL, generator=g), torch.rand(BB, generator=g)
        xt = (1 - t[:, None, None]) * x0 + t[:, None, None] * x1
        h, sp = m(lay["draw"], text, [xt], [t])
        flow_draw = ((unpatch(m.vel(h[:, sp[0][0]:sp[0][1]])) - (x1 - x0)) ** 2).mean()
        lm_draw = F.cross_entropy(m.lm(h[~drop, 0:2]).reshape(-1, V), text[~drop, 1:3].reshape(-1))
        # name: a clean picture, then its letter and its family
        i = torch.randint(0, len(X), (BB,), generator=g)
        text = torch.stack([torch.full_like(Y[i], BOS), torch.full_like(Y[i], BOI), torch.full_like(Y[i], EOI), Y[i],
                            Fm[i] + 26], 1)
        h, sp = m(lay["name"], text, [X[i]], [torch.ones(BB)])
        e = sp[0][1]  # the EOI position: it predicts the letter, the letter predicts the family
        lm_name = F.cross_entropy(m.lm(h[:, e:e + 2]).reshape(-1, V), text[:, 3:5].reshape(-1))
        # edit: a clean source picture, the instruction, the noisy target
        i = torch.randint(0, len(S), (BB,), generator=g)
        text = torch.tensor([[BOS, BOI, EOI, BOLD, BOI]] * BB)
        x1, x0, t = T[i], torch.randn(BB, GL, GL, generator=g), torch.rand(BB, generator=g)
        xt = (1 - t[:, None, None]) * x0 + t[:, None, None] * x1
        h, sp = m(lay["edit"], text, [S[i], xt], [torch.ones(BB), t])
        flow_edit = ((unpatch(m.vel(h[:, sp[1][0]:sp[1][1]])) - (x1 - x0)) ** 2).mean()
        loss = lm_draw + lm_name + flow_draw + flow_edit
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step()
        sched.step()
        run.append([float(lm_draw), float(lm_name), float(flow_draw), float(flow_edit)])
        if st % 50 == 0:
            curve.append([st] + np.mean(run, 0).tolist())
            run = []
    m.eval()
    return m, curve


def draw(m, fams, letters, seed, n_steps=20, w=GUIDE):
    import torch

    lay = layouts()["draw"]
    y = torch.tensor(np.asarray(letters))
    f = torch.tensor(np.asarray(fams)) + 26
    B = len(y)
    tc = torch.stack([torch.full_like(y, BOS), f, y, torch.full_like(y, BOI)], 1)
    tu = torch.stack([torch.full_like(y, BOS), torch.full_like(y, NULL), torch.full_like(y, NULL),
                      torch.full_like(y, BOI)], 1)
    x = torch.randn(B, GL, GL, generator=torch.Generator().manual_seed(seed))
    with torch.no_grad():
        for k in range(n_steps):
            t = torch.full((B,), k / n_steps)
            hc, sp = m(lay, tc, [x], [t])
            hu, _ = m(lay, tu, [x], [t])
            vc, vu = unpatch(m.vel(hc[:, sp[0][0]:sp[0][1]])), unpatch(m.vel(hu[:, sp[0][0]:sp[0][1]]))
            x = x + (vu + w * (vc - vu)) / n_steps
    return ((x.numpy() + 1) / 2).clip(0, 1)


def name(m, imgs):
    import torch

    lay = layouts()["name"]
    x = torch.tensor(np.asarray(imgs) * 2 - 1, dtype=torch.float32)
    B = len(x)
    with torch.no_grad():
        text = torch.tensor([[BOS, BOI, EOI, 0, 0]] * B)
        h, sp = m(lay, text, [x], [torch.ones(B)])
        let = m.lm(h[:, sp[0][1]])[:, :26].argmax(1)
        text[:, 3] = let
        h, sp = m(lay, text, [x], [torch.ones(B)])
        fam = m.lm(h[:, sp[0][1] + 1])[:, 26:29].argmax(1)
    return let.numpy(), fam.numpy()


def edit(m, src, seed, n_steps=20):
    import torch

    lay = layouts()["edit"]
    s = torch.tensor(np.asarray(src) * 2 - 1, dtype=torch.float32)
    B = len(s)
    text = torch.tensor([[BOS, BOI, EOI, BOLD, BOI]] * B)
    x = torch.randn(B, GL, GL, generator=torch.Generator().manual_seed(seed))
    with torch.no_grad():
        for k in range(n_steps):
            t = torch.full((B,), k / n_steps)
            h, sp = m(lay, text, [s, x], [torch.ones(B), t])
            x = x + unpatch(m.vel(h[:, sp[1][0]:sp[1][1]])) / n_steps
    return ((x.numpy() + 1) / 2).clip(0, 1)


def compute_unified():
    import time

    import torch

    threads()
    imgs, labels, test, _, font = dataset()
    files = font_files()
    fam = np.array([family(files[k]) for k in font])
    src, tgt, elab, epair, held, pair_names = edit_data()
    tr_e = ~np.isin(epair, held)
    data = (torch.tensor(imgs[~test] * 2 - 1, dtype=torch.float32), torch.tensor(labels[~test]),
            torch.tensor(fam[~test]), torch.tensor(src[tr_e] * 2 - 1, dtype=torch.float32),
            torch.tensor(tgt[tr_e] * 2 - 1, dtype=torch.float32), torch.tensor(elab[tr_e]))
    n = steps(N_STEPS)
    want = np.repeat(np.arange(26), 10)
    fams = np.tile(np.arange(3), 87)[:len(want)]
    he = np.where(~tr_e)[0]
    # one resumable file per seed, so seeds can train in separate processes (AI22_UNI_SEEDS=1 python -m ...)
    parts = {s_: CACHE.partial(f"unified_s{s_}", dict(steps=n, D=D, L=L, bb=BB, held=held, guide=GUIDE,
                                                      shortcut=SHORTCUT, blocks="adaLN-Zero")) for s_ in SEEDS}
    only = [int(x) for x in os.environ.get("AI22_UNI_SEEDS", "").split(",") if x]
    for seed in SEEDS:
        key = f"s{seed}"
        part = parts[seed]
        if key in part or (only and seed not in only):
            continue
        t0 = time.time()
        m, curve = train(seed, data, n)
        let, fm = name(m, imgs[test])
        q = score(draw(m, fams, want, seed=80 + seed), want)
        out_e = edit(m, src[he], seed=90 + seed)
        ink = lambda a: np.asarray(a).reshape(len(a), -1).sum(1)  # noqa: E731
        r = dict(curve=curve, name_acc=float((let == labels[test]).mean()), fam_acc=float((fm == fam[test]).mean()),
                 draw_acc=q["acc"], draw_fd=q["fd"],
                 edit_rmse=float(np.sqrt(((out_e - tgt[he]) ** 2).mean())),
                 copy_rmse=float(np.sqrt(((src[he] - tgt[he]) ** 2).mean())),
                 edit_ink=float(np.median(ink(out_e) / ink(src[he]))), true_ink=float(np.median(ink(tgt[he]) / ink(src[he]))),
                 edit_letter=score(out_e, elab[he])["acc"], secs=time.time() - t0,
                 params=int(sum(p.numel() for p in m.parameters() if p.requires_grad)))
        if seed == 0:
            pick = he[[0, 3 * 4, 3 * 17, 3 * 6, 3 * 26 + 3 * 1, 3 * 26 + 3 * 12, 3 * 26 + 3 * 22, 3 * 26 + 3 * 18]]
            pk = np.searchsorted(he, pick)
            r["edit_src"], r["edit_out"], r["edit_true"] = src[pick].tolist(), out_e[pk].tolist(), tgt[pick].tolist()
            r["draw_samples"] = draw(m, [1] * 10 + [0] * 10 + [2] * 10, list(range(10)) * 3, seed=5).tolist()
            ex = np.where(test)[0][[0, 3 * 7, 3 * 13 + 1, 3 * 25]]
            r["name_imgs"] = imgs[ex].tolist()
            l_, f_ = name(m, imgs[ex])
            r["name_pred"], r["name_fam"] = l_.tolist(), f_.tolist()
        part[key] = r
        print(f"    unified s{seed}: names {r['name_acc']:.3f} (family {r['fam_acc']:.3f}); draws right letter "
              f"{r['draw_acc']:.3f}, FD {r['draw_fd']:.1f}; held-out edit RMSE {r['edit_rmse']:.3f} (copying "
              f"{r['copy_rmse']:.3f}), ink x{r['edit_ink']:.2f} (true x{r['true_ink']:.2f}); {r['secs']:.0f}s", flush=True)
    missing = [s_ for s_ in SEEDS if f"s{s_}" not in parts[s_]]
    if missing:
        raise SystemExit(f"unified: seeds {missing} still to train")
    part = {f"s{s_}": parts[s_][f"s{s_}"] for s_ in SEEDS}
    out = dict(seeds=list(SEEDS), steps=n, D=D, L=L, bb=BB, held=[pair_names[k] for k in held],
               pairs=[list(p_) for p_ in pair_names], params=part["s0"]["params"], guide=GUIDE)
    for f_ in ("name_acc", "fam_acc", "draw_acc", "draw_fd", "edit_rmse", "copy_rmse", "edit_ink", "true_ink", "edit_letter"):
        out[f_] = [part[f"s{s}"][f_] for s in SEEDS]
    for f_ in ("edit_src", "edit_out", "edit_true", "draw_samples", "name_imgs"):
        out[f_] = np.array(part["s0"][f_])
    out["name_pred"], out["name_fam"] = part["s0"]["name_pred"], part["s0"]["name_fam"]
    out["curve"] = np.array([np.array(part[f"s{s}"]["curve"]) for s in SEEDS])
    return out
