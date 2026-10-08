"""Precompute every piece of real footage in the frontier-training video.

    python -m videos.frontier.compute                    # everything missing (a few CPU-hours on 4 cores)
    python -m videos.frontier.compute funnel corpus      # specific items
    python -m videos.frontier.compute --force isoflop    # recompute

Results are cached in ``.cache/frontier/<name>.json`` (+ ``.npz`` for arrays);
scenes call ``load(name)`` and never train or run a model themselves.  Each
stage of the pipeline is run for real, in miniature, on a 4-core CPU:

Data
    funnel      the first 400 MB of one real WARC file from Common Crawl's September 2026
                crawl (CC-MAIN-2026-39) through the full FineWeb recipe (datatrove's filters)
    corpus      8 whole WET files (172K pages) through the same filters -> training text
    dedup       MinHash LSH (FineWeb's 5-grams, 14 bands x 8 hashes) over the corpus
    edu         FineWeb-Edu's educational-quality classifier on the funnel's survivors
    tokenizer   byte-level BPE (2,048 tokens) trained on FineWeb-Edu, which encodes the pretraining text
Pretraining (PocketGPT, explainer/lm/pocket.py)
    isoflop     a Chinchilla-style IsoFLOP sweep: 4 compute budgets x 7 model sizes
    optim       AdamW vs Muon, same model and data
    schedule    cosine vs warmup-stable-decay, plus WSD cooldown branches
    stability   learning-rate sweep with and without QK-norm (after Wortsman et al. 2023)
    moe         mixture of experts: no balancing, auxiliary loss, auxiliary-loss-free bias
    muon_svd    singular values of a real gradient, before and after Newton-Schulz
    precision   FP8 / MXFP8 / NVFP4 quantization of real GPT-2 activations
Post-training
    chat        a real chat template (Qwen3 tokenizer) and its loss mask
    grpo        a real GRPO group: 8 sampled answers from a small open model, verified
    toy_rl      a miniature RLVR run on arithmetic (pass@1 vs pass@k)
Context
    epoch       Epoch AI's database of notable AI models (training compute over time)
"""

from __future__ import annotations

import argparse
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

from explainer.tts import REPO_ROOT

DATA_DIR = REPO_ROOT / ".cache" / "frontier"
CRAWL_DIR = DATA_DIR / "crawl"
RUN_DIR = DATA_DIR / "runs"
CRAWL = "CC-MAIN-2026-39"
CC = "https://data.commoncrawl.org/"
WARC_HEAD_BYTES = 400 * 2**20  # first 400 MiB of the first WARC file of the crawl
N_WET = 8  # WET files 1, 12501, 25001, ... of the crawl's 100,000


# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------
def path(name: str) -> Path:
    return DATA_DIR / f"{name}.json"


_loaded: dict = {}


def load(name: str) -> dict:
    if name not in _loaded:
        p = path(name)
        if not p.exists():
            raise FileNotFoundError(f"{p} missing: run `python -m videos.frontier.compute {name}`")
        _loaded[name] = json.loads(p.read_text())
        npz = p.with_suffix(".npz")
        if npz.exists():
            with np.load(npz) as z:
                _loaded[name].update({k: z[k] for k in z.files})
    return _loaded[name]


def _save(name: str, out: dict) -> None:
    arrays = {k: v for k, v in out.items() if isinstance(v, np.ndarray)}
    rest = {k: v for k, v in out.items() if k not in arrays}
    tmp = path(name).with_suffix(".tmp.json")
    tmp.write_text(json.dumps(rest, ensure_ascii=False, indent=1, default=float))
    tmp.replace(path(name))
    if arrays:
        np.savez_compressed(path(name).with_suffix(".tmp.npz"), **arrays)
        path(name).with_suffix(".tmp.npz").replace(path(name).with_suffix(".npz"))


def _download(url: str, dst: Path, byte_range: str | None = None) -> Path:
    import subprocess

    if dst.exists() and dst.stat().st_size > 0:
        return dst
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["curl", "-sS", "-L", "--retry", "5", "-m", "1800", "-o", str(dst) + ".part", url]
    if byte_range:
        cmd[1:1] = ["-r", byte_range]
    subprocess.run(cmd, check=True)
    Path(str(dst) + ".part").replace(dst)
    return dst


def wet_paths() -> list[str]:
    import gzip

    lst = _download(f"{CC}crawl-data/{CRAWL}/wet.paths.gz", CRAWL_DIR / "wet.paths.gz")
    lines = gzip.open(lst, "rt").read().split()
    return [p for i, p in enumerate(lines) if i % 12_500 == 0][:N_WET]


def warc_head() -> Path:
    import gzip

    lst = _download(f"{CC}crawl-data/{CRAWL}/warc.paths.gz", CRAWL_DIR / "warc.paths.gz")
    first = gzip.open(lst, "rt").readline().strip()
    return _download(CC + first, CRAWL_DIR / "warc_head.warc.gz", f"0-{WARC_HEAD_BYTES - 1}")


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
def compute_funnel():
    from explainer.data import crawl

    warc_head()
    res = crawl.funnel(str(CRAWL_DIR), "warc_head.warc.gz")
    kept = res.pop("kept")
    with open(DATA_DIR / "funnel_kept.jsonl", "w") as f:
        for d in kept:
            f.write(json.dumps({k: v for k, v in d.items() if k != "html"}, ensure_ascii=False) + "\n")
    with open(DATA_DIR / "funnel_kept_html.jsonl", "w") as f:
        for d in kept:
            if "html" in d:
                f.write(json.dumps(dict(url=d["url"], html=d["html"]), ensure_ascii=False) + "\n")
    res["n_kept"] = len(kept)
    res["kept_urls"] = [d["url"] for d in kept]
    return res


def _filter_one_wet(p: str):
    from explainer.data import crawl

    f = _download(CC + p, CRAWL_DIR / Path(p).name)
    return crawl.filter_wet(str(CRAWL_DIR), f.name)


def compute_corpus():
    paths = wet_paths()
    with ProcessPoolExecutor(4) as pool:
        results = list(pool.map(_filter_one_wet, paths))
    docs, counts = [], {}
    for d, c in results:
        docs += d
        for k, v in c.items():
            counts[k] = counts.get(k, 0) + v
    (DATA_DIR / "corpus_filtered.jsonl").write_text("".join(json.dumps(d, ensure_ascii=False) + "\n" for d in docs))
    return dict(files=[Path(p).name for p in paths], counts=counts, n_docs=len(docs),
                chars=sum(len(d["text"]) for d in docs))


def _read_jsonl(p: Path) -> list[dict]:
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]


def compute_dedup():
    from explainer.data import crawl

    docs = _read_jsonl(DATA_DIR / "corpus_filtered.jsonl")
    res = crawl.dedup(docs)
    keep = set(res["keep"])
    out = [d for i, d in enumerate(docs) if i in keep]
    (DATA_DIR / "corpus_dedup.jsonl").write_text("".join(json.dumps(d, ensure_ascii=False) + "\n" for d in out))
    big = []
    for members in res["big"]:
        big.append([dict(url=docs[i]["url"], text=docs[i]["text"][:600]) for i in members[:6]] + [len(members)])
    # Near-duplicate pairs at a range of similarities (for the MinHash picture): estimated vs true Jaccard.
    params = crawl.hash_params()
    pairs = []
    for members in res["big"][:40]:
        if len(members) < 2:
            continue
        i, j = members[0], members[1]
        si, sj = crawl.signature(docs[i]["text"], params), crawl.signature(docs[j]["text"], params)
        pairs.append(dict(i=i, j=j, true=crawl.jaccard(docs[i]["text"], docs[j]["text"]),
                          est=float((si == sj).mean()), urls=[docs[i]["url"], docs[j]["url"]]))
    return dict(n_in=res["n_in"], n_out=res["n_out"], sizes=res["sizes"][:200],
                n_clusters_multi=sum(1 for s in res["sizes"] if s > 1), big=big, pairs=pairs,
                bands=crawl.BANDS, rows=crawl.ROWS, n_grams=crawl.N_GRAMS)


def compute_edu():
    """FineWeb-Edu's classifier (HuggingFaceFW/fineweb-edu-classifier): an educational score 0-5."""
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    torch.set_num_threads(4)
    name = "HuggingFaceFW/fineweb-edu-classifier"
    tok = AutoTokenizer.from_pretrained(name)
    model = AutoModelForSequenceClassification.from_pretrained(name).eval()
    docs = _read_jsonl(DATA_DIR / "funnel_kept.jsonl")
    scores = []
    with torch.no_grad():
        for k in range(0, len(docs), 16):
            batch = [d["text"] for d in docs[k:k + 16]]
            enc = tok(batch, return_tensors="pt", padding="longest", truncation=True, max_length=512)
            scores += model(**enc).logits.squeeze(-1).float().tolist()
            if k % 320 == 0:
                print(f"    edu {k}/{len(docs)}", flush=True)
    return dict(scores=scores, urls=[d["url"] for d in docs], model=name)


FWEDU_URL = "https://huggingface.co/datasets/karpathy/fineweb-edu-100b-shuffle/resolve/main/shard_{:05d}.parquet"
N_FWEDU = 2  # two ~95 MB shards of FineWeb-Edu (shuffled), ~500M characters


def fineweb_edu_docs() -> list[str]:
    import pyarrow.parquet as pq

    docs = []
    for i in range(N_FWEDU):
        f = _download(FWEDU_URL.format(i), DATA_DIR / "fwedu" / f"shard_{i:05d}.parquet")
        docs += pq.read_table(f, columns=["text"]).column("text").to_pylist()
    return docs


def compute_tokenizer():
    """Byte-level BPE with 2,048 tokens, trained on FineWeb-Edu (the FineWeb recipe at full scale, plus the
    educational classifier); the whole text is encoded to uint16 for the pretraining experiments."""
    from tokenizers import Tokenizer, decoders, models, pre_tokenizers, trainers

    docs = fineweb_edu_docs()
    n_val = 2000
    val_docs, train_docs = docs[:n_val], docs[n_val:]
    tok = Tokenizer(models.BPE())
    tok.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
    tok.decoder = decoders.ByteLevel()
    trainer = trainers.BpeTrainer(vocab_size=2048, special_tokens=["<|doc|>"],
                                  initial_alphabet=pre_tokenizers.ByteLevel.alphabet(), show_progress=False)
    tok.train_from_iterator(train_docs[:60_000], trainer=trainer)
    tok.save(str(DATA_DIR / "bpe.json"))
    sep = tok.token_to_id("<|doc|>")

    def encode(ds):
        out = []
        for k in range(0, len(ds), 5000):
            for enc in tok.encode_batch(ds[k:k + 5000]):
                out.append(np.array([sep] + enc.ids, dtype=np.uint16))
        return np.concatenate(out)

    train, val = encode(train_docs), encode(val_docs)
    np.save(DATA_DIR / "tokens_train.npy", train)
    np.save(DATA_DIR / "tokens_val.npy", val)
    train_bytes = sum(len(d.encode()) for d in train_docs)
    example = "The mitochondria is the powerhouse of the cell, converting nutrients into energy."
    enc = tok.encode(example)
    return dict(vocab=tok.get_vocab_size(), train_tokens=int(len(train)), val_tokens=int(len(val)),
                train_docs=len(train_docs), val_docs=len(val_docs), bytes_per_token=train_bytes / len(train),
                example=example, example_tokens=[tok.decode([i]) for i in enc.ids], example_ids=enc.ids)


def bpe():
    from tokenizers import Tokenizer

    return Tokenizer.from_file(str(DATA_DIR / "bpe.json"))


def corpus_tokens():
    return np.load(DATA_DIR / "tokens_train.npy", mmap_mode="r"), np.load(DATA_DIR / "tokens_val.npy")


# ---------------------------------------------------------------------------
# Pretraining experiments (PocketGPT).  Every run trains single-threaded so four run side by side,
# and is cached on its own in .cache/frontier/runs/<name>.json, so a sweep resumes where it stopped.
# ---------------------------------------------------------------------------
SEQ = 256
ISO_SIZES = [(1, 32), (2, 48), (2, 64), (3, 96), (4, 128), (5, 160), (6, 192), (8, 256)]  # (layers, width)
ISO_BUDGETS = {1e12: ISO_SIZES[0:4], 3e12: ISO_SIZES[0:5], 1e13: ISO_SIZES[0:6], 3e13: ISO_SIZES[1:7]}


def _cfg(layers: int, d: int, **kw):
    from explainer.lm.pocket import Config

    heads = max(1, d // 32) if d % 32 == 0 else 2
    return Config(d=d, layers=layers, heads=heads, seq=SEQ, **kw)


def _tokens_for(cfg, flops: float) -> int:
    from explainer.lm.pocket import PocketGPT, flops_per_token

    return int(flops / flops_per_token(PocketGPT(cfg).count(), cfg))


def iso_lr(d: int) -> float:
    """Peak AdamW learning rate by width (from a small sweep at 1e13 FLOPs: the optimum sat near 3-4e-3 for
    widths 64 and 160, with a weak width dependence)."""
    return 3.5e-3 * (128 / d) ** 0.25


MUON_LR = 6e-3  # Muon beat 2e-3 clearly at this scale; AdamW was flat between 2e-3 and 6e-3


def iso_runs() -> dict:
    from dataclasses import asdict

    from explainer.lm.pocket import Run

    runs = {}
    for C, sizes in ISO_BUDGETS.items():
        for L, d in sizes:
            cfg = _cfg(L, d)
            tokens = _tokens_for(cfg, C)
            steps = tokens // (16 * SEQ)
            runs[f"iso_{C:.0e}_L{L}_d{d}"] = asdict(Run(model=cfg, lr=iso_lr(d), batch=16, tokens=tokens,
                                                         warmup=max(10, steps // 20), schedule="cosine"))
    return runs


def _run_one(item):
    name, rd = item
    out = RUN_DIR / f"{name}.json"
    if out.exists():
        return name, json.loads(out.read_text())
    import torch

    from explainer.lm.pocket import Config, Run, TokenStream, train

    torch.set_num_threads(1)
    rd = dict(rd)
    rd["model"] = Config(**rd["model"])
    run = Run(**rd)
    tr, va = corpus_tokens()
    res = train(run, TokenStream(tr, va, run.model.seq, seed=run.seed))
    res.pop("_model")
    res.pop("_opts")
    res["name"] = name
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".tmp")
    tmp.write_text(json.dumps(res))
    tmp.replace(out)
    print(f"    run {name}: val {res['final_val']:.3f} in {res['seconds'] / 60:.1f} min", flush=True)
    return name, res


def run_all(runs: dict, workers: int = 4) -> dict:
    """Train every run (longest first, to finish the sweep sooner) and return {name: result}."""
    from explainer.lm.pocket import Config, PocketGPT, flops_per_token

    def cost(rd):
        cfg = Config(**rd["model"])
        return flops_per_token(PocketGPT(cfg).count(), cfg) * rd["tokens"]

    order = sorted(runs.items(), key=lambda kv: -cost(kv[1]))
    with ProcessPoolExecutor(workers) as pool:
        return dict(pool.map(_run_one, order))


def _slim(res: dict) -> dict:
    keep = ["run", "counts", "steps", "tokens_per_step", "curve", "evals", "final_val", "diverged", "seconds",
            "probes", "loads", "bias", "name"]
    return {k: res[k] for k in keep if k in res}


def compute_isoflop():
    from explainer.lm.pocket import Config, PocketGPT, flops_per_token

    results = run_all(iso_runs())
    rows = []
    for name, r in results.items():
        cfg = Config(**r["run"]["model"])
        counts = PocketGPT(cfg).count()
        rows.append(dict(name=name, budget=float(name.split("_")[1]), layers=cfg.layers, d=cfg.d,
                         params=counts["compute"], tokens=r["run"]["tokens"],
                         flops=flops_per_token(counts, cfg) * r["run"]["tokens"], val=r["final_val"],
                         evals=r["evals"]))
    return dict(rows=sorted(rows, key=lambda x: (x["budget"], x["params"])), seq=SEQ)


OPT_TOKENS = 12_000_000  # AdamW vs Muon: L4 d128 (~1M params), ~12 tokens per parameter
SCHED_TOKENS = 8_000_000  # schedules: L3 d96 (~0.5M params)
STAB_TOKENS = 2_000_000
STAB_LRS = [3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1]
MOE_TOKENS = 4_000_000


def opt_runs() -> dict:
    from dataclasses import asdict

    from explainer.lm.pocket import Run

    cfg = _cfg(4, 128)
    lrs = {"adamw": iso_lr(128), "muon": MUON_LR}
    return {f"opt_{o}": asdict(Run(model=cfg, optimizer=o, lr=lrs[o], batch=16, tokens=OPT_TOKENS, warmup=50,
                                   schedule="wsd", decay_frac=0.3, final_lr=0.05)) for o in ["adamw", "muon"]}


def sched_runs() -> dict:
    """WSD's cooldown branches share their prefix with the main run exactly (same seed, same batches, same
    learning rate until the branch point), so each branch is just a shorter WSD run."""
    from dataclasses import asdict

    from explainer.lm.pocket import Run

    cfg = _cfg(3, 96)
    base = dict(model=cfg, lr=iso_lr(96), batch=16, warmup=50, final_lr=0.05)
    out = {}
    for frac in [0.5, 0.75, 1.0]:
        tag = f"{int(frac * 100):03d}"
        out[f"sched_wsd_{tag}"] = asdict(Run(**base, schedule="wsd", decay_frac=0.2, tokens=int(SCHED_TOKENS * frac)))
        if frac != 0.75:
            out[f"sched_cos_{tag}"] = asdict(Run(**base, schedule="cosine", tokens=int(SCHED_TOKENS * frac)))
    return out


def stab_runs() -> dict:
    from dataclasses import asdict

    from explainer.lm.pocket import Run

    out = {}
    for qk in [False, True]:
        for lr in STAB_LRS:
            cfg = _cfg(4, 128, qk_norm=qk)
            out[f"stab_{'qk' if qk else 'base'}_{lr:.0e}"] = asdict(Run(model=cfg, lr=lr, batch=16, tokens=STAB_TOKENS,
                                                                        warmup=20, schedule="cosine", probe_every=10))
    return out


def moe_runs() -> dict:
    from dataclasses import asdict

    from explainer.lm.pocket import Run

    out = {}
    for bal in ["none", "aux", "bias"]:
        cfg = _cfg(4, 128, experts=8, top_k=2, balance=bal)
        out[f"moe_{bal}"] = asdict(Run(model=cfg, lr=iso_lr(128), batch=16, tokens=MOE_TOKENS, warmup=50,
                                       schedule="cosine", log_every=5))
    return out


def compute_optim():
    return {k: _slim(v) for k, v in run_all(opt_runs()).items()}


def compute_schedule():
    return {k: _slim(v) for k, v in run_all(sched_runs()).items()}


def compute_stability():
    return {k: _slim(v) for k, v in run_all(stab_runs()).items()}


def compute_moe():
    return {k: _slim(v) for k, v in run_all(moe_runs()).items()}


def compute_sweeps():
    """Every pretraining run in one pool (longest first), so the four cores stay busy."""
    runs = {**iso_runs(), **opt_runs(), **sched_runs(), **stab_runs(), **moe_runs()}
    res = run_all(runs)
    return dict(n=len(res), minutes=sum(r["seconds"] for r in res.values()) / 60)


def compute_muon_svd():
    """A real gradient (one MLP matrix of a briefly trained L4 d128 PocketGPT): its singular values, the
    AdamW update's, and the singular values after each Newton-Schulz iteration."""
    import torch
    import torch.nn.functional as F

    from explainer.lm.pocket import NS_COEFFS, Run, TokenStream, newton_schulz, train

    torch.set_num_threads(4)
    run = Run(model=_cfg(4, 128), lr=iso_lr(128), batch=16, tokens=400 * 16 * SEQ, warmup=40, schedule="constant")
    tr, va = corpus_tokens()
    data = TokenStream(tr, va, SEQ, seed=7)
    res = train(run, data, threads=4)
    model, opts = res["_model"], res["_opts"]
    W = model.blocks[2].mlp.up.weight
    adam_state = opts[0].state[W]
    x, y = data.batch(16)
    model.zero_grad()
    F.cross_entropy(model(x).flatten(0, 1), y.flatten()).backward()
    G = W.grad.detach().clone()
    hist = []
    newton_schulz(G, 5, history=hist)
    sv = lambda M: torch.linalg.svdvals(M.float()).numpy()  # noqa: E731
    adam_upd = adam_state["exp_avg"] / (adam_state["exp_avg_sq"].sqrt() + 1e-8)
    return dict(shape=list(G.shape), coeffs=list(NS_COEFFS), grad_sv=sv(G), adam_sv=sv(adam_upd),
                ns_sv=np.stack([sv(h) for h in hist]), param="blocks.2.mlp.up.weight", train_steps=res["steps"],
                grad_frob=float(G.norm()))


# ---------------------------------------------------------------------------
# Number formats: exact rounding to FP8 / FP4 grids
# ---------------------------------------------------------------------------
def float_grid(exp_bits: int, man_bits: int, bias: int, max_val: float | None = None) -> np.ndarray:
    """All non-negative finite values of a small float format (with subnormals)."""
    vals = {0.0}
    for e in range(0, 2**exp_bits):
        for m in range(2**man_bits):
            v = (m / 2**man_bits) * 2.0 ** (1 - bias) if e == 0 else (1 + m / 2**man_bits) * 2.0 ** (e - bias)
            vals.add(v)
    g = np.array(sorted(vals))
    return g[g <= max_val] if max_val is not None else g


E4M3 = float_grid(4, 3, 7, 448.0)  # no infinities; 0 1111 111 is NaN, so the max is 448
E5M2 = float_grid(5, 2, 15, 57344.0)  # IEEE-like: the top exponent is inf/NaN
E2M1 = float_grid(2, 1, 1, 6.0)  # {0, .5, 1, 1.5, 2, 3, 4, 6}


def round_to(x: np.ndarray, grid: np.ndarray) -> np.ndarray:
    """Round to the nearest representable value (saturating at the grid's max)."""
    a = np.clip(np.abs(x), 0, grid[-1])
    i = np.clip(np.searchsorted(grid, a), 1, len(grid) - 1)
    lo, hi = grid[i - 1], grid[i]
    return np.sign(x) * np.where(a - lo <= hi - a, lo, hi)


def quantize(x: np.ndarray, scheme: str) -> np.ndarray:
    """Fake-quantize a 2-D activation matrix (tokens x channels) under one scaling scheme."""
    x = np.asarray(x, dtype=np.float64)
    T, C = x.shape
    if scheme == "bf16":
        return (x.astype(np.float32).view(np.uint32) & 0xFFFF0000).view(np.float32).astype(np.float64)
    if scheme == "fp8_tensor":  # one scale for the whole tensor
        s = np.abs(x).max() / 448.0
        return round_to(x / s, E4M3) * s
    if scheme == "fp4_tensor":  # FP4 (E2M1) with one scale for the whole tensor
        s = np.abs(x).max() / 6.0
        return round_to(x / s, E2M1) * s
    if scheme == "fp8_tile128":  # DeepSeek-V3: 1 x 128 tiles
        out = np.empty_like(x)
        for j in range(0, C, 128):
            blk = x[:, j:j + 128]
            s = np.maximum(np.abs(blk).max(axis=1, keepdims=True), 1e-12) / 448.0
            out[:, j:j + 128] = round_to(blk / s, E4M3) * s
        return out
    if scheme in ("mxfp8", "mxfp4"):  # OCP MX: 32-element blocks, power-of-two (E8M0) scale
        grid, emax = (E4M3, 8) if scheme == "mxfp8" else (E2M1, 2)
        out = np.empty_like(x)
        for j in range(0, C, 32):
            blk = x[:, j:j + 32]
            amax = np.maximum(np.abs(blk).max(axis=1, keepdims=True), 1e-30)
            s = 2.0 ** (np.floor(np.log2(amax)) - emax)
            out[:, j:j + 32] = round_to(blk / s, grid) * s
        return out
    if scheme == "nvfp4":  # 16-element blocks, E4M3 block scale, FP32 per-tensor scale
        st = np.abs(x).max() / (448.0 * 6.0)
        out = np.empty_like(x)
        for j in range(0, C, 16):
            blk = x[:, j:j + 16]
            sb = round_to(np.abs(blk).max(axis=1, keepdims=True) / 6.0 / st, E4M3)
            sb = np.maximum(sb, E4M3[1])
            out[:, j:j + 16] = round_to(blk / (sb * st), E2M1) * sb * st
        return out
    raise ValueError(scheme)


SCHEMES = ["bf16", "fp8_tensor", "fp8_tile128", "mxfp8", "fp4_tensor", "mxfp4", "nvfp4"]


def compute_precision():
    """GPT-2 small's residual stream entering block 7 (it has "massive activations": channel 447 reaches
    ~2,900 at the first token while a typical entry is ~1), quantized under each format and scaling scheme."""
    import torch
    from transformers import GPT2LMHeadModel, GPT2TokenizerFast

    torch.set_num_threads(4)
    tok = GPT2TokenizerFast.from_pretrained("openai-community/gpt2")
    model = GPT2LMHeadModel.from_pretrained("openai-community/gpt2").eval()
    text = ("The Eiffel Tower is located in the city of Paris. It was built for the 1889 World's Fair, and for "
            "four decades it was the tallest structure in the world. Today millions of visitors climb it every year.")
    ids = tok(text, return_tensors="pt").input_ids
    with torch.no_grad():
        out = model(ids, output_hidden_states=True)
    X = out.hidden_states[6][0].numpy().astype(np.float64)  # residual stream after 6 blocks
    col_amax = np.abs(X).max(axis=0)
    typical = np.argsort(-col_amax)[8:]  # every channel except the 8 largest
    errs, Q = {}, {}
    for sc in SCHEMES:
        q = quantize(X, sc)
        Q[sc] = q
        nz = X != 0
        Xt, qt = X[:, typical], q[:, typical]
        errs[sc] = dict(rel_rmse=float(np.sqrt(((q - X) ** 2).sum() / (X**2).sum())),
                        rel_rmse_typical=float(np.sqrt(((qt - Xt) ** 2).sum() / (Xt**2).sum())),
                        flushed=float(((q == 0) & nz).sum() / nz.sum()),
                        snr_db=float(10 * np.log10((X**2).sum() / max(((q - X) ** 2).sum(), 1e-30))))
    tokens = [tok.decode([i]) for i in ids[0]]
    return dict(text=text, tokens=tokens, X=X.astype(np.float32), errors=errs, e4m3=E4M3, e5m2=E5M2, e2m1=E2M1,
                outlier_channels=[int(c) for c in np.argsort(-col_amax)[:8]], median_abs=float(np.median(np.abs(X))),
                amax=float(np.abs(X).max()), **{f"q_{k}": v.astype(np.float32) for k, v in Q.items()})


# ---------------------------------------------------------------------------
# Post-training
# ---------------------------------------------------------------------------
CHAT = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Where is the Eiffel Tower?"},
    {"role": "assistant", "content": "The Eiffel Tower is in Paris, France."},
]


def compute_chat():
    """How a conversation becomes one token sequence (Qwen3's chat template), and which tokens are trained."""
    from transformers import AutoTokenizer

    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3-0.6B")
    text = tok.apply_chat_template(CHAT, tokenize=False)
    prefix = tok.apply_chat_template(CHAT[:-1], tokenize=False, add_generation_prompt=True)
    ids = tok(text).input_ids
    n_prefix = len(tok(prefix).input_ids)
    pieces = [tok.decode([i]) for i in ids]
    assert "".join(pieces) == text
    gens = _base_vs_chat(CHAT[1]["content"])
    return dict(text=text, pieces=pieces, ids=ids, n_prompt=n_prefix, vocab=len(tok), model="Qwen/Qwen3-0.6B", **gens)


def _base_vs_chat(question: str, n_new: int = 48) -> dict:
    """Greedy continuations of the same question by Qwen3-0.6B-Base (a document completer) and by Qwen3-0.6B
    after post-training (asked through its chat template, thinking off)."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    torch.set_num_threads(4)
    out = {}
    for key, name in [("base", "Qwen/Qwen3-0.6B-Base"), ("chat", "Qwen/Qwen3-0.6B")]:
        tok = AutoTokenizer.from_pretrained(name)
        model = AutoModelForCausalLM.from_pretrained(name, torch_dtype=torch.float32).eval()
        if key == "base":
            prompt = question + "\n"
        else:
            prompt = tok.apply_chat_template([{"role": "user", "content": question}], tokenize=False,
                                             add_generation_prompt=True, enable_thinking=False)
        ids = tok(prompt, return_tensors="pt").input_ids
        with torch.no_grad():
            gen = model.generate(ids, max_new_tokens=n_new, do_sample=False)
        out[f"{key}_prompt"] = prompt
        out[f"{key}_output"] = tok.decode(gen[0, ids.shape[1]:], skip_special_tokens=True)
        out[f"{key}_model"] = name
    return out


# ---------------------------------------------------------------------------
# A miniature RLVR run: a pocket model that learned "noisy internet arithmetic"
# ---------------------------------------------------------------------------
RL_VOCAB = "0123456789+=\n"
RL_LEN = 13  # "347+285=0632\n"
CARRY_DROP = 0.4  # fraction of pretraining examples written by someone who forgets to carry


def _no_carry_sum(a: int, b: int) -> int:
    return int("".join(str((int(x) + int(y)) % 10) for x, y in zip(f"{a:04d}", f"{b:04d}")))


def _rl_example(a: int, b: int, ans: int) -> list[int]:
    s = f"{a:03d}+{b:03d}={ans:04d}\n"
    return [RL_VOCAB.index(c) for c in s]


def compute_toy_rl():
    """Pretrain a 2-layer PocketGPT on 3-digit additions where 40% of the answers forget every carry,
    then run GRPO-style RL with a verifiable reward (exact answer).  Tracks pass@1 and pass@8."""
    import torch
    import torch.nn.functional as F

    from explainer.lm.pocket import Config, PocketGPT

    torch.set_num_threads(1)  # tiny matrices: more threads only add synchronization overhead
    torch.manual_seed(0)
    rng = np.random.default_rng(0)
    cfg = Config(vocab=len(RL_VOCAB), d=96, layers=3, heads=3, seq=RL_LEN)
    model = PocketGPT(cfg)
    # ---- "pretraining" on noisy arithmetic
    def batch(n):
        a, b = rng.integers(0, 1000, n), rng.integers(0, 1000, n)
        drop = rng.random(n) < CARRY_DROP
        ans = [(_no_carry_sum(x, y) if d else x + y) for x, y, d in zip(a, b, drop)]
        return torch.tensor([_rl_example(x, y, z) for x, y, z in zip(a, b, ans)])

    opt = torch.optim.AdamW(model.parameters(), lr=2e-3, weight_decay=0.0, betas=(0.9, 0.98))
    pre_curve = []
    for step in range(3000):
        x = batch(128)
        logits = model(x[:, :-1])
        loss = F.cross_entropy(logits[:, 7:].flatten(0, 1), x[:, 8:].flatten())  # answer tokens only
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step % 50 == 0:
            pre_curve.append([step, loss.item()])

    test_a, test_b = rng.integers(0, 1000, 400), rng.integers(0, 1000, 400)
    has_carry = np.array([_no_carry_sum(a, b) != a + b for a, b in zip(test_a, test_b)])

    @torch.no_grad()
    def sample(prompts, n, greedy=False):
        model.eval()
        x = prompts.repeat_interleave(n, 0)
        for _ in range(5):
            logits = model(x)[:, -1]
            nxt = logits.argmax(-1) if greedy else torch.multinomial(logits.softmax(-1), 1)[:, 0]
            x = torch.cat([x, nxt[:, None]], 1)
        model.train()
        return x

    def decode_answer(seq):
        s = "".join(RL_VOCAB[i] for i in seq[8:12].tolist())
        return int(s) if s.isdigit() else -1

    def prompts_for(a, b):
        return torch.tensor([_rl_example(x, y, 0)[:8] for x, y in zip(a, b)])

    def evaluate(k=8):
        P = prompts_for(test_a, test_b)
        seqs = sample(P, k)
        correct = np.array([decode_answer(s) for s in seqs]).reshape(len(P), k) == (test_a + test_b)[:, None]
        greedy = np.array([decode_answer(s) for s in sample(P, 1, greedy=True)]) == test_a + test_b
        return dict(pass1=float(correct.mean()), pass8=float(correct.any(1).mean()),
                    pass1_carry=float(correct[has_carry].mean()), greedy=float(greedy.mean()))

    # ---- RL: GRPO with a verifiable reward
    G, P_PER_STEP, STEPS = 8, 32, 120
    opt = torch.optim.AdamW(model.parameters(), lr=1e-4, weight_decay=0.0, betas=(0.9, 0.98))
    show_a, show_b = 478, 356
    groups, curve, zero_var, mean_r = [], [], [], []
    for step in range(STEPS + 1):
        if step % 10 == 0:
            curve.append(dict(step=step, **evaluate()))
        if step in (0, STEPS):
            seqs = sample(prompts_for([show_a], [show_b]), G)
            groups.append(dict(step=step, answers=[decode_answer(s) for s in seqs]))
        if step == STEPS:
            break
        a, b = rng.integers(0, 1000, P_PER_STEP), rng.integers(0, 1000, P_PER_STEP)
        seqs = sample(prompts_for(a, b), G)
        r = (np.array([decode_answer(s) for s in seqs]) == np.repeat(a + b, G)).astype(np.float32)
        r = torch.tensor(r).view(P_PER_STEP, G)
        zero_var.append(float((r.std(1) == 0).float().mean()))
        mean_r.append(float(r.mean()))
        adv = ((r - r.mean(1, keepdim=True)) / (r.std(1, keepdim=True) + 1e-4)).flatten()
        logp = F.log_softmax(model(seqs[:, :-1])[:, 7:12], -1).gather(2, seqs[:, 8:13, None])[..., 0]
        loss = -(adv[:, None] * logp).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    return dict(pre_curve=pre_curve, curve=curve, groups=groups, show=[show_a, show_b], carry_drop=CARRY_DROP,
                zero_var=zero_var, mean_reward=mean_r,
                G=G, prompts_per_step=P_PER_STEP, params=sum(p.numel() for p in model.parameters()),
                no_carry_answer=_no_carry_sum(show_a, show_b))


def compute_goodhart():
    """Best-of-n against a proxy reward: each candidate has a true quality g ~ N(0, 1); the reward model sees
    g + e with heavy-tailed error e ~ 0.6 * Student-t(3).  Choosing the proxy's favourite of n candidates moves
    the policy by KL = log n - (n - 1)/n from the original (Gao, Schulman & Hilton 2022 use the same measure)."""
    rng = np.random.default_rng(0)
    ns = np.unique(np.round(np.logspace(0, 4.3, 26)).astype(int))
    gold, proxy = [], []
    for n in ns:
        T = max(400, int(8e6 // n))
        g = rng.normal(size=(T, n))
        e = rng.standard_t(3, size=(T, n)) * 0.6
        i = np.argmax(g + e, axis=1)
        gold.append(float(g[np.arange(T), i].mean()))
        proxy.append(float((g + e)[np.arange(T), i].mean()))
    kl = np.log(ns) - (ns - 1) / ns
    return dict(n=ns.astype(float), kl=kl, gold=np.array(gold), proxy=np.array(proxy))


def compute_epoch():
    """Epoch AI, 'Data on AI models' (CC BY 4.0): notable models with a training-compute estimate."""
    import csv
    import io

    f = _download("https://epoch.ai/data/notable_ai_models.csv", DATA_DIR / "epoch_notable.csv")
    rows = []
    for r in csv.DictReader(io.StringIO(f.read_text(encoding="utf-8"))):
        try:
            c = float(r["Training compute (FLOP)"])
        except (ValueError, KeyError):
            continue
        date = r.get("Publication date", "")
        if len(date) < 4:
            continue
        y, m, d = (date.split("-") + ["1", "1"])[:3]
        t = int(y) + (int(m or 1) - 1) / 12 + (int(d or 1) - 1) / 365
        rows.append(dict(model=r["Model"], org=r.get("Organization", ""), date=date, t=t, flop=c,
                         frontier=r.get("Frontier model", ""), confidence=r.get("Confidence", ""),
                         domain=r.get("Domain", "")))
    return dict(rows=sorted(rows, key=lambda x: x["t"]), source="https://epoch.ai/data/ai-models",
                retrieved=time.strftime("%Y-%m-%d"))


# ---------------------------------------------------------------------------
# Item registry
# ---------------------------------------------------------------------------
ITEMS = {
    "funnel": compute_funnel,
    "corpus": compute_corpus,
    "dedup": compute_dedup,
    "edu": compute_edu,
    "tokenizer": compute_tokenizer,
    "sweeps": compute_sweeps,
    "isoflop": compute_isoflop,
    "optim": compute_optim,
    "schedule": compute_schedule,
    "stability": compute_stability,
    "moe": compute_moe,
    "muon_svd": compute_muon_svd,
    "precision": compute_precision,
    "chat": compute_chat,
    "toy_rl": compute_toy_rl,
    "goodhart": compute_goodhart,
    "epoch": compute_epoch,
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="*", default=list(ITEMS))
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "true")
    for name in args.names:
        if path(name).exists() and not args.force:
            print(f"  cached  {name}")
            continue
        t = time.time()
        print(f"  compute {name} ...", flush=True)
        _save(name, ITEMS[name]())
        _loaded.pop(name, None)
        print(f"  done    {name} in {time.time() - t:.0f}s", flush=True)


if __name__ == "__main__":
    main()
