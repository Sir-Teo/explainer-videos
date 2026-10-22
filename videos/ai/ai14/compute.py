"""Precompute everything numerical in Part 14 of the AI series ("The Language-Model Lineage").

    python -m explainer.ai.novels               # first: the novels tokenizer and the series' base model
    python -m videos.ai.ai14.compute            # everything missing (training: about 3 CPU-hours on 2 threads)
    python -m videos.ai.ai14.compute gpt_m --force

Results are cached in ``.cache/ai14/<name>.json`` (+ ``.npz``); trained weights in ``.cache/ai14/<name>.pt``, with
resumable checkpoints ``<name>.ckpt.pt`` while a run trains.  Published numbers live in ``facts.py`` (with their
sources); Epoch AI's database of language models, trimmed, in ``epoch_lm.json``.

Items:
    published  numbers derived from published configurations: the Transformer's training FLOPs from GPU-days, the
               parameter count of a decoder from its shape (12 L d^2 + vocabulary), GPT-3's 6ND, LLaMA's SwiGLU
               width, the KV cache per token under MHA, GQA and MLA, tokens per parameter, 6ND of the open models
    family     our models' shapes and parameter counts, before training
    aa         open against closed on Artificial Analysis's index (as fetched on 8 October 2026): the running best of
               each, and how many months behind each new open record was
    epoch      growth of training compute: a least-squares fit of log10(FLOP) against the date for Epoch AI's
               frontier language models (and for all its notable language models), and the compute tower
    gpt_xs, gpt_s, gpt_m, gpt_l
               our GPT-style family on the thirty novels: four shapes, the same 6 million tokens each; curves and
               snapshots (held-out loss, loss at each position, a repeated-list test, a sample)
    bert_m     a BERT-style masked model with gpt_m's shape, initial weights, data, steps and schedule: equal compute
    lineage    gpt_m against bert_m on tasks both can do: filling a blank among eight candidates, and naming the book
               a held-out sentence comes from with a linear probe on frozen features; plus bits per character
    icl        in-context learning as the family grows (and the series' base model): the loss at each position of
               the context, the repeated-list test, and few-shot "which book?" prompts with 0-8 examples
    scoreboard bits per character on the scoreboard's passage (The Maltese Falcon, ch. 2) for our models
"""

from __future__ import annotations

import math
import re
from datetime import date

import numpy as np

from explainer.ai.cache import Cache
from videos.ai.ai14 import facts as F

CACHE = Cache("ai14")
load = CACHE.load

FAMILY = {  # name: (shape, label)
    "gpt_xs": dict(d=32, layers=1, heads=2),
    "gpt_s": dict(d=64, layers=2, heads=2),
    "gpt_m": dict(d=128, layers=4, heads=4),
    "gpt_l": dict(d=192, layers=6, heads=6),
}
TOKENS = 3_000_000  # per model: equal data for every member of the family, and for the masked model
FEW_SHOT_BOOKS = ["Emma", "Dracula", "Frankenstein", "Middlemarch", "Jane Eyre", "Moby Dick", "Little Women",
                  "Ulysses"]
SHOTS = [0, 1, 2, 4, 8]


def rng(seed) -> np.random.Generator:
    return np.random.default_rng(seed)


def year(d: str) -> float:
    y, m, dd = (int(x) for x in d.split("-"))
    return y + (date(y, m, dd).timetuple().tm_yday - 1) / 365.25


# ---------------------------------------------------------------------------
# Published configurations, and what follows from them
# ---------------------------------------------------------------------------
def decoder_params(L, d, V, ctx=0, d_ff=None, kv=None, heads=None, swiglu=False, tied=True):
    """Parameters of a decoder from its shape: attention (Q, O: d x d each; K, V: d x kv_dim each), the MLP (two
    matrices of d x d_ff, or three for SwiGLU), and the token (and learned position) embeddings."""
    d_ff = d_ff or 4 * d
    kv_dim = d if kv is None else kv * (d // heads)
    attn = 2 * d * d + 2 * d * kv_dim
    mlp = (3 if swiglu else 2) * d * d_ff
    emb = V * d * (1 if tied else 2) + ctx * d
    return dict(attn=attn * L, mlp=mlp * L, emb=emb, total=(attn + mlp) * L + emb)


def compute_published():
    T = F.TRANSFORMER
    out = {}
    # the Transformer's training cost, the paper's way: time x GPUs x sustained FLOP/s of a P100
    out["tf_big_flops"] = T["big"]["hours"] * 3600 * T["gpus"] * T["tflops"] * 1e12
    out["tf_base_flops"] = T["base"]["hours"] * 3600 * T["gpus"] * T["tflops"] * 1e12
    assert abs(out["tf_big_flops"] / 2.3e19 - 1) < 0.02 and abs(out["tf_base_flops"] / 3.3e18 - 1) < 0.02
    # decoders from their shapes: 12 L d^2 plus the embeddings (GPT-1/2/3 tie input and output embeddings)
    rows = {}
    for key in ("gpt1", "gpt2", "gpt3"):
        c = F.CFG[key]
        p = decoder_params(c["layers"], c["d"], c["vocab"], c["ctx"])
        rows[key] = dict(L=c["layers"], d=c["d"], vocab=c["vocab"], ctx=c["ctx"], body=p["attn"] + p["mlp"],
                         emb=p["emb"], total=p["total"], published=c["params"])
    out["shape_params"] = rows
    assert abs(rows["gpt3"]["total"] / (F.GPT3["params_m"] * 1e6) - 1) < 0.002  # Table D.1: 174,600M
    assert abs(rows["gpt2"]["total"] / 1.558e9 - 1) < 0.01  # the corrected count of the released model
    # GPT-3's training compute: 6ND
    n, d_ = F.GPT3["params_m"] * 1e6, F.CFG["gpt3"]["tokens"]
    out["gpt3_6nd"] = 6 * n * d_
    out["gpt3_pfdays"] = out["gpt3_6nd"] / (1e15 * 86400)
    assert abs(out["gpt3_6nd"] / F.GPT3["flops"] - 1) < 0.01
    # SwiGLU's width: 2/3 of 4d keeps the MLP's parameters (LLaMA rounds up to a multiple of 256)
    d = F.CFG["llama"]["d"]
    out["swiglu_exact"] = 8 * d / 3
    out["swiglu_llama"] = int(math.ceil(8 * d / 3 / 256) * 256)
    assert out["swiglu_llama"] == F.CFG["llama"]["d_ff"]
    lp = decoder_params(80, d, 32000, 0, d_ff=22016, swiglu=True, tied=False)
    out["llama65_params"] = lp["total"]
    assert abs(lp["total"] / 65.2e9 - 1) < 0.01
    c = F.CFG["llama3"]
    l3 = decoder_params(c["layers"], c["d"], c["vocab"], 0, d_ff=c["d_ff"], kv=c["kv_heads"], heads=c["heads"],
                        swiglu=True, tied=False)
    out["llama3_params"] = l3["total"]
    assert abs(l3["total"] / 405e9 - 1) < 0.01
    # the KV cache per token (16-bit numbers): K and V for every layer and KV head
    hd = c["d"] // c["heads"]
    out["kv_llama3_gqa"] = 2 * c["layers"] * c["kv_heads"] * hd * 2
    out["kv_llama3_mha"] = 2 * c["layers"] * c["heads"] * hd * 2
    out["kv_llama3_ctx"] = c["ctx"]
    out["kv_dsv3_mla"] = (512 + 64) * F.CFG["dsv3"]["layers"] * 2  # the latent and the shared RoPE key
    g3 = F.CFG["gpt3"]
    out["kv_gpt3"] = 2 * g3["layers"] * g3["d"] * 2
    # tokens per parameter (active parameters for mixtures of experts)
    tpp = [("GPT-3", 2020.41, 174.6e9, 300e9), ("Gopher", 2021.94, 280e9, 300e9), ("Chinchilla", 2022.24, 70e9, 1.4e12),
           ("PaLM", 2022.26, 540.35e9, 780e9), ("LLaMA-7B", 2023.15, 6.7e9, 1.0e12), ("LLaMA-65B", 2023.15, 65.2e9, 1.4e12),
           ("Llama 2 70B", 2023.54, 70e9, 2e12), ("Llama 3.1 405B", 2024.56, 405e9, 15.6e12),
           ("DeepSeek-V3", 2024.98, 37e9, 14.8e12), ("Qwen3-0.6B", 2025.32, 0.6e9, 36e12),
           ("Kimi K2", 2025.52, 32.6e9, 15.5e12), ("GLM-5", 2026.11, 40e9, 28.5e12)]
    out["tpp"] = [dict(name=a, year=y, n=nn, d=dd, ratio=dd / nn) for a, y, nn, dd in tpp]
    # 6ND of open models (active parameters) against what was reported
    six = []
    for key in ("llama", "llama2", "llama3", "dsv3", "qwen3", "kimik2", "glm45"):
        c = F.CFG[key]
        nn = c["active"] or c["params"]
        six.append(dict(key=key, name=c["name"], date=c["date"], n=nn, d=c["tokens"], flops=6 * nn * c["tokens"]))
    out["six_nd"] = six
    assert abs(six[2]["flops"] / F.LLAMA3["flops"] - 1) < 0.02  # Llama 3's reported 3.8e25
    out["dsv3_usd"] = F.DSV3["gpu_hours"] * F.DSV3["rate"]
    out["dsv3_6nd"] = 6 * 37e9 * 14.8e12
    out["glm5_6nd"] = 6 * F.GLM5["active"] * F.GLM5["tokens"]
    out["dsv4_6nd"] = 6 * F.DSV4["active"] * F.DSV4["tokens"]
    # sparsity of the open frontier: the share of parameters a token uses
    out["active_share"] = {c["key"]: c["active"] / c["params"] for c in F.CONFIGS if c.get("active")}
    return out


# ---------------------------------------------------------------------------
# Compute trends, from Epoch AI's data
# ---------------------------------------------------------------------------
TOWER = [  # (label, date, FLOP, how we know)
    ("Transformer", "2017-06-12", 2.3e19, "paper"),
    ("GPT-1", "2018-06-11", 1.76e19, "Epoch"),
    ("BERT-Large", "2018-10-11", 5.33e20, "GPT-3 paper"),
    ("GPT-2", "2019-02-14", 1.92e21, "Epoch"),
    ("T5-11B", "2019-10-23", 3.30e22, "GPT-3 paper"),
    ("GPT-3", "2020-05-28", 3.14e23, "paper"),
    ("PaLM", "2022-04-04", 2.53e24, "Epoch"),
    ("GPT-4", "2023-03-14", 2.1e25, "Epoch"),
    ("Llama 3.1 405B", "2024-07-23", 3.8e25, "paper"),
    ("Grok 3", "2025-02-17", 3.5e26, "Epoch"),
]


def compute_epoch():
    import json
    from pathlib import Path

    data = json.loads((Path(__file__).parent / "epoch_lm.json").read_text())
    ms = data["models"]

    def fit(sel, start=None):
        x = np.array([year(m["date"]) for m in sel if not start or m["date"] >= start])
        y = np.log10([m["flop"] for m in sel if not start or m["date"] >= start])
        A = np.vstack([x - 2020, np.ones_like(x)]).T
        coef, res, *_ = np.linalg.lstsq(A, y, rcond=None)
        resid = y - A @ coef
        s2 = float(resid @ resid) / max(1, len(x) - 2)
        se = math.sqrt(s2 / float(((x - x.mean()) ** 2).sum()))
        return dict(slope=float(coef[0]), icept=float(coef[1]), per_year=float(10 ** coef[0]),
                    lo=float(10 ** (coef[0] - 1.645 * se)), hi=float(10 ** (coef[0] + 1.645 * se)), n=len(x),
                    doubling_months=float(12 * math.log10(2) / coef[0]), x=x.tolist(), y=y.tolist())

    front = [m for m in ms if m["frontier"]]
    f_all = fit(front)
    f_recent = fit(front, "2020-06-01")
    f_lm = fit(ms)
    out = dict(meta=data["meta"], frontier=f_all, frontier_recent=f_recent, all_lm=f_lm,
               names=[m["model"] for m in front], dates=[m["date"] for m in front],
               conf=[m["confidence"] for m in front], open=[m["open"] for m in front])
    out["tower"] = [dict(label=a, date=d, year=year(d), flop=c, src=s) for a, d, c, s in TOWER]
    span = year(TOWER[-1][1]) - year(TOWER[0][1])
    out["tower_span_years"] = span
    out["tower_ratio"] = TOWER[-1][2] / TOWER[0][2]
    out["tower_per_year"] = out["tower_ratio"] ** (1 / span)
    # what F.EPOCH's 4-5x a year compounds to
    out["x45_doubling_months"] = [12 * math.log(2) / math.log(g) for g in (4.0, 5.0)]
    out["x45_decade"] = [g ** 10 for g in (4.0, 5.0)]
    return out


def compute_aa():
    """Open against closed on one independent index (Artificial Analysis): the running best of each, and for every new
    open record, how many months earlier a closed model had first scored as high."""
    import json
    from pathlib import Path

    d = json.loads((Path(__file__).parent / "aa_progress.json").read_text())
    rows = sorted(d["progress"], key=lambda r: r["release"])
    best = {True: [], False: []}
    lag = []
    for r in rows:
        y = year(r["release"])
        prev = best[r["open"]][-1][1] if best[r["open"]] else -1
        if r["score"] > prev:
            best[r["open"]].append((y, r["score"], r["name"]))
            if r["open"]:
                closed_first = next((year(c["release"]) for c in rows if not c["open"] and c["score"] >= r["score"]),
                                    None)
                lag.append(dict(name=r["name"], year=y, score=r["score"],
                                months=None if closed_first is None else 12 * (y - closed_first)))
    return dict(meta=d["meta"], open=best[True], closed=best[False], lag=lag, rows=rows)


# ---------------------------------------------------------------------------
# Our own lineage: training
# ---------------------------------------------------------------------------
def _train(name, kind, shape):
    from videos.ai.ai14 import lm

    CACHE.dir.mkdir(parents=True, exist_ok=True)
    return lm.train(name, kind, shape, TOKENS, CACHE.dir)


def _trained(name):
    """One of our trained models, training it (or resuming its checkpoint) first if it isn't cached yet, so that
    `python -m videos.ai.ai14.compute` alone rebuilds everything."""
    from videos.ai.ai14 import lm

    if not CACHE.path(name).exists() or not (CACHE.dir / f"{name}.pt").exists():
        CACHE.save(name, ITEMS[name]())
    return lm.load_trained(name, CACHE.dir)


def compute_family():
    """Our models' shapes and parameter counts (no training needed)."""
    from videos.ai.ai14 import lm

    rows = []
    for nm, shape in FAMILY.items():
        p = lm.n_params(lm.build(shape, "gpt"))
        rows.append(dict(name=nm, **shape, **p, tokens=TOKENS, flops=6.0 * p["compute"] * TOKENS))
    return dict(rows=rows, tokens=TOKENS, seq=lm.SEQ, batch=lm.BATCH, vocab=lm.VOCAB,
                bert=lm.n_params(lm.build(FAMILY["gpt_m"], "bert")))


def compute_gpt_xs():
    return _train("gpt_xs", "gpt", FAMILY["gpt_xs"])


def compute_gpt_s():
    return _train("gpt_s", "gpt", FAMILY["gpt_s"])


def compute_gpt_m():
    return _train("gpt_m", "gpt", FAMILY["gpt_m"])


def compute_gpt_l():
    return _train("gpt_l", "gpt", FAMILY["gpt_l"])


def compute_bert_m():
    return _train("bert_m", "bert", FAMILY["gpt_m"])


# ---------------------------------------------------------------------------
# Sentences from the novels (Part 1's split: every 20th block of 40 paragraphs is held out)
# ---------------------------------------------------------------------------
SPLIT = re.compile(r'(?<=[.!?])\s+(?=[A-Z"])')
PLAIN = re.compile(r"^[A-Za-z0-9 ,.;:!?'-]+$")


def _paragraphs():
    from videos.ai.ai1 import compute as ai1

    out = {}
    for n, title in ai1.BOOKS.items():
        raw = (ai1.BOOK_DIR / f"{n}.txt").read_text(encoding="utf-8", errors="replace")
        paras = ai1.clean(ai1.strip_gutenberg(raw)).split("\n")
        train, valid = [], []
        for k in range(0, len(paras), 40):
            (valid if (k // 40) % 20 == 7 else train).extend(paras[k:k + 40])
        out[title] = (train, valid)
    return out


def _sentences(paras, lo=8, hi=26):
    for p in paras:
        for s in SPLIT.split(p):
            s = s.strip()
            if lo <= len(s.split()) <= hi and PLAIN.match(s) and s[0].isupper():
                yield s


# ---------------------------------------------------------------------------
# GPT against BERT, on tasks both can do
# ---------------------------------------------------------------------------
def _cloze_items(n=600, k=8, seed=0):
    """Held-out sentences with one whole-word token blanked, and k-1 distractors of similar frequency."""
    from explainer.ai import novels as N
    from videos.ai.ai14 import lm

    g = rng(seed)
    train, _ = N.token_arrays()
    counts = np.bincount(train.astype(np.int64), minlength=4096)
    words = lm.word_tokens(train, top=3000)
    wset = set(words)
    by_freq = np.array(sorted(words, key=lambda t: -counts[t]))
    rank = {int(t): i for i, t in enumerate(by_freq)}
    sents = []
    for title, (_, valid) in _paragraphs().items():
        sents += list(_sentences(valid, 8, 24))
    g.shuffle(sents)
    items = []
    for s in sents:
        ids = N.encode(s)
        if len(ids) > 40:
            continue
        cand = [i for i in range(2, len(ids) - 1) if ids[i] in wset]
        if not cand:
            continue
        pos = int(g.choice(cand))
        true = ids[pos]
        r = rank[true]
        pool = [int(t) for t in by_freq[max(0, r - 60): r + 60] if t != true]
        distract = [int(t) for t in g.choice(pool, k - 1, replace=False)]
        opts = [true] + distract
        g.shuffle(opts)
        items.append(dict(text=s, ids=ids, pos=pos, opts=[int(o) for o in opts], answer=opts.index(true)))
        if len(items) >= n:
            break
    return items


def _cloze_scores(model, kind, items):
    import torch
    import torch.nn.functional as Fn

    from videos.ai.ai14 import lm

    right = {"full": 0, "left": 0}
    model.eval()
    with torch.no_grad():
        for it in items:
            ids, pos, opts = it["ids"], it["pos"], it["opts"]
            if kind == "bert":
                x = list(ids)
                x[pos] = lm.MASK
                lp = model(torch.tensor([x]))[0, pos].float().log_softmax(-1)
                right["full"] += int(int(torch.tensor([lp[o] for o in opts]).argmax()) == it["answer"])
                continue
            rows = []
            for o in opts:
                x = list(ids)
                x[pos] = o
                rows.append(x)
            x = torch.tensor(rows)
            logp = model(x[:, :-1]).float().log_softmax(-1).gather(-1, x[:, 1:, None]).squeeze(-1)
            full = logp.sum(-1)  # the whole sentence's log-probability with each candidate in the blank
            left = logp[:, pos - 1]  # only p(candidate | the words before it)
            right["full"] += int(int(full.argmax()) == it["answer"])
            right["left"] += int(int(left.argmax()) == it["answer"])
    return {k: v / len(items) for k, v in right.items()}


def _features(model, sents, B=32):
    """Mean of the final (normalized) hidden states over a sentence's tokens."""
    import torch

    from explainer.ai import novels as N

    feats = []
    model.eval()
    with torch.no_grad():
        for i in range(0, len(sents), B):
            chunk = [N.encode(s)[:64] for s in sents[i:i + B]]
            T = max(len(c) for c in chunk)
            x = torch.zeros(len(chunk), T, dtype=torch.long)
            m = torch.zeros(len(chunk), T)
            for j, c in enumerate(chunk):
                x[j, :len(c)] = torch.tensor(c)
                m[j, :len(c)] = 1
            h = model.emb(x)
            for b in model.blocks:
                h = b(h)
            h = model.norm(h)
            feats.append(((h * m[..., None]).sum(1) / m.sum(1, keepdim=True)).numpy())
    return np.concatenate(feats)


def _probe(Xtr, ytr, Xte, yte, classes, wd=1e-3, iters=300):
    """Multinomial logistic regression on standardized features (full-batch L-BFGS)."""
    import torch

    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-6
    A = torch.tensor((Xtr - mu) / sd, dtype=torch.float32)
    Bt = torch.tensor((Xte - mu) / sd, dtype=torch.float32)
    y = torch.tensor(ytr)
    torch.manual_seed(0)
    W = torch.zeros(A.shape[1], classes, requires_grad=True)
    b = torch.zeros(classes, requires_grad=True)
    opt = torch.optim.LBFGS([W, b], max_iter=iters, line_search_fn="strong_wolfe")

    def closure():
        opt.zero_grad()
        loss = torch.nn.functional.cross_entropy(A @ W + b, y) + wd * (W ** 2).sum()
        loss.backward()
        return loss

    opt.step(closure)
    with torch.no_grad():
        pred = (Bt @ W + b).argmax(-1).numpy()
        tr = float(((A @ W + b).argmax(-1).numpy() == ytr).mean())
    return float((pred == yte).mean()), tr


def _probe_data(per_train=200, per_test=40, seed=1):
    g = rng(seed)
    tr, te = [], []
    books = _paragraphs()
    for k, (title, (train, valid)) in enumerate(books.items()):
        a, b = list(_sentences(train)), list(_sentences(valid))
        tr += [(str(s), k) for s in g.choice(a, min(per_train, len(a)), replace=False)]
        te += [(str(s), k) for s in g.choice(b, min(per_test, len(b)), replace=False)]
    return tr, te, list(books)


def compute_lineage():
    import torch

    from videos.ai.ai14 import lm

    torch.set_num_threads(2)
    gpt, bert = _trained("gpt_m"), _trained("bert_m")
    rg, rb = load("gpt_m"), load("bert_m")
    out = dict(params=rg["params"], flops_gpt=rg["flops"], flops_bert=rb["flops"], tokens=rg["tokens"],
               steps=rg["steps"], seconds_gpt=rg["seconds"], seconds_bert=rb["seconds"])
    items = _cloze_items()
    cg, cb = _cloze_scores(gpt, "gpt", items), _cloze_scores(bert, "bert", items)
    out.update(cloze_n=len(items), cloze_k=len(items[0]["opts"]), cloze_gpt=cg["full"], cloze_gpt_left=cg["left"],
               cloze_bert=cb["full"])
    from explainer.ai import novels as N

    ex = items[3]
    out["cloze_example"] = dict(text=ex["text"], blank=N.decode([ex["ids"][ex["pos"]]]).strip(),
                                left=N.decode(ex["ids"][:ex["pos"]]), right=N.decode(ex["ids"][ex["pos"] + 1:]),
                                opts=[N.decode([o]).strip() for o in ex["opts"]], answer=ex["answer"])
    tr, te, titles = _probe_data()
    ytr, yte = np.array([k for _, k in tr]), np.array([k for _, k in te])
    for nm, m in (("gpt", gpt), ("bert", bert)):
        Xtr, Xte = _features(m, [s for s, _ in tr]), _features(m, [s for s, _ in te])
        out[f"probe_{nm}"], out[f"probe_{nm}_train"] = _probe(Xtr, ytr, Xte, yte, len(titles))
    out["probe_n_train"], out["probe_n_test"], out["probe_classes"] = len(tr), len(te), len(titles)
    # the masked model writing: fill [MASK]s at the end one at a time (left to right), against the GPT's sample
    out["gpt_sample"] = lm.sample(gpt, lm.PROMPT, 24, seed=1)
    out["bert_sample"] = _bert_generate(bert, lm.PROMPT, 12)
    return out


def _bert_generate(model, prompt, n):
    """A masked model asked to continue text: append a [MASK], take its best guess, repeat."""
    import torch

    from explainer.ai import novels as N
    from videos.ai.ai14 import lm

    ids = N.encode(prompt)
    start = len(ids)
    with torch.no_grad():
        for _ in range(n):
            x = torch.tensor([ids + [lm.MASK]])
            lp = model(x)[0, -1, :4096].float()
            lp[:4] = -float("inf")
            ids.append(int(lp.argmax()))
    return N.decode(ids[start:])


# ---------------------------------------------------------------------------
# In-context learning as the family grows
# ---------------------------------------------------------------------------
def _fewshot_items(n_pairs=10, per_pair=30, seed=2):
    """Two-way 'which book?' prompts: k labelled sentences from two books, then a held-out sentence."""
    g = rng(seed)
    books = _paragraphs()
    pool = {}
    for b in FEW_SHOT_BOOKS:
        train, valid = books[b]
        pool[b] = (list(_sentences(train, 6, 16)), list(_sentences(valid, 6, 16)))
    pairs = []
    while len(pairs) < n_pairs:
        a, b = (str(x) for x in g.choice(FEW_SHOT_BOOKS, 2, replace=False))
        if (a, b) not in pairs and (b, a) not in pairs:
            pairs.append((a, b))
    items = []
    for a, b in pairs:
        for j in range(per_pair):
            book = a if j % 2 == 0 else b
            q = str(g.choice(pool[book][1]))
            demos = []
            for i in range(max(SHOTS)):
                lab = a if i % 2 == 0 else b
                demos.append((str(g.choice(pool[lab][0])), lab))
            order = g.permutation(len(demos))
            items.append(dict(pair=(a, b), query=q, answer=book, demos=[demos[i] for i in order]))
    return items


def _fewshot_prompt(demos, query):
    lines = [f'"{s}" is from {lab}.\n' for s, lab in demos]
    return "".join(lines) + f'"{query}" is from'


def _fewshot_scores(model, items, shots=SHOTS):
    """Accuracy at each k: does the model give the right title the higher log-probability?  All the prompts of an
    item (every k, both titles) go through the model as one right-padded batch; padding after a sequence can't
    change a causal model's outputs before it."""
    import torch

    from explainer.ai import novels as N

    acc = {k: 0 for k in shots}
    model.eval()
    T = model.cfg.seq
    titles = {}
    with torch.no_grad():
        for it in items:
            a, b = it["pair"]
            seqs, ns = [], []
            for k in shots:
                demos = it["demos"][:k] if k else []  # balanced: the first k of a list that alternates labels
                p = N.encode(_fewshot_prompt(demos, it["query"]))
                for lab in (a, b):
                    c = titles.setdefault(lab, N.encode(" " + lab))
                    seqs.append((p + c)[-(T + 1):])
                    ns.append(len(c))
            t = torch.zeros(len(seqs), max(len(x) for x in seqs), dtype=torch.long)
            for i, x in enumerate(seqs):
                t[i, :len(x)] = torch.tensor(x)
            lp = model(t[:, :-1]).float().log_softmax(-1)
            sc = []
            for i, (x, n) in enumerate(zip(seqs, ns)):
                m = len(x)
                sc.append(float(lp[i, m - 1 - n:m - 1].gather(-1, t[i, m - n:m, None]).sum()))
            for j, k in enumerate(shots):
                acc[k] += int((sc[2 * j] > sc[2 * j + 1]) == (it["answer"] == a))
    return [acc[k] / len(items) for k in shots]


def compute_icl():
    import torch

    from explainer.ai import novels as N
    from videos.ai.ai14 import lm

    torch.set_num_threads(2)
    train, valid = N.token_arrays()
    win = lm.val_windows(valid, 128)
    rep = lm.repeat_batch(lm.word_tokens(train))
    items = _fewshot_items()
    out = dict(shots=SHOTS, books=FEW_SHOT_BOOKS, n_items=len(items), example=_fewshot_prompt(items[0]["demos"][:2],
                                                                                              items[0]["query"]),
               example_answer=items[0]["answer"], example_pair=list(items[0]["pair"]))
    models = [(nm, _trained(nm)) for nm in FAMILY]
    models.append(("base", N.load_base()))  # the series' own model (explainer.ai.novels; make.py trains it first)
    rows = []
    for nm, m in models:
        pp = lm.per_position(m, win)
        r = lm.repeat_test(m, rep)
        fs = _fewshot_scores(m, items)
        c = m.count()
        rows.append(dict(name=nm, params=int(c["total"]), body=int(c["body"]), pos=pp.tolist(), early=float(pp[8:24].mean()),
                         late=float(pp[192:].mean()), icl=float(pp[192:].mean() - pp[8:24].mean()), fewshot=fs, **r))
        print(f"  {nm}: early {rows[-1]['early']:.3f} late {rows[-1]['late']:.3f} rep {r['acc1']:.2f}->{r['acc2']:.2f}"
              f" few-shot {[round(x, 3) for x in fs]}", flush=True)
    out["rows"] = rows
    out["base_tokens"] = base_tokens()
    return out


def base_tokens():
    """Tokens the series' base model trained on, from its configuration (explainer.ai.novels.BASE_RUN)."""
    from explainer.ai import novels as N

    per_step = N.BASE_RUN["batch"] * N.BASE["seq"]
    return N.BASE_RUN["tokens"] // per_step * per_step


# ---------------------------------------------------------------------------
# The scoreboard
# ---------------------------------------------------------------------------
def compute_scoreboard():
    import json

    import torch

    from explainer.ai import novels as N
    from explainer.tts import REPO_ROOT
    from videos.ai.ai14 import lm

    torch.set_num_threads(2)
    passage = (REPO_ROOT / ".cache" / "ai1" / "passage.txt").read_text()
    rows = []
    raw = REPO_ROOT / ".cache" / "ai1" / "raw.json"
    if raw.exists():
        r = json.loads(raw.read_text())
        rows += [dict(label="gzip", bits=r["compressors"]["gzip"], kind="compressor", part=1),
                 dict(label="bzip2", bits=r["compressors"]["bzip2"], kind="compressor", part=1),
                 dict(label=f"the previous {r['best']} characters", bits=r["best_bits"], kind="count", part=1)]
    ours = []
    for nm in FAMILY:
        m = _trained(nm)
        b = lm.bits_per_char(m, passage)
        ours.append(dict(name=nm, params=int(m.count()["total"]), bits=b["bits"], tokens=b["tokens"]))
    out = dict(rows=rows, ours=ours, chars=len(passage))
    if (N.OUT / "base.pt").exists():  # never train it from here
        base = N.load_base()
        b = lm.bits_per_char(base, passage)
        out["base"] = dict(bits=b["bits"], params=int(base.count()["total"]))
    return out


ITEMS = {
    "published": compute_published,
    "epoch": compute_epoch,
    "family": compute_family,
    "aa": compute_aa,
    "gpt_xs": compute_gpt_xs,
    "gpt_s": compute_gpt_s,
    "gpt_m": compute_gpt_m,
    "bert_m": compute_bert_m,
    "gpt_l": compute_gpt_l,
    "lineage": compute_lineage,
    "icl": compute_icl,
    "scoreboard": compute_scoreboard,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
