"""Precompute everything numerical in Part 18 of the AI series ("Pretraining at Scale").

    python tools/make.py ai18                   # everything, in order: Part 1's text, the novels model, Part 14, this
    python -m videos.ai.ai18.compute            # everything missing (about 2-3 CPU-hours on one thread here)
    python -m videos.ai.ai18.compute precision --force

Results are cached in ``.cache/ai18/<name>.json`` (+ ``.npz``); downloads in ``.cache/ai18/crawl/``; trained weights
and checkpoints in ``.cache/ai18/runs/`` (every 100 steps for the long runs), and items made of many runs save each run
as it finishes (``CACHE.partial``), so an interrupted computation resumes.  Every random choice is seeded; processes
are started with ``spawn``; torch uses one thread.  Published numbers are in ``facts.py``, with their sources.

Items:
    published      numbers that follow from published figures: MFU (PaLM, Llama 3), Llama 3's failure statistics,
                   DeepSeek-V3's cost, memory per parameter (ZeRO's 16 bytes), RoPE wavelengths, schedules
    objectives     causal LM, masked LM, span corruption and fill-in-the-middle applied to one sentence
    pipeline       GPipe, 1F1B, interleaved 1F1B and ZB-H1, simulated exactly; the bubble against (p-1)/(m+p-1)
    faults         a 16,384-GPU run with Llama 3's failure rate, simulated for many checkpoint intervals; Young's rule
    collapse       a model trained on its own samples, generation after generation: replace against accumulate
    web            a sample of Common Crawl's September 2026 crawl: URL filter, fastText language ID, extraction
    dedup          MinHash-LSH on those pages: the collision S-curve predicted and measured; real near-duplicates
    quality        a fastText classifier trained on FineWeb-Edu's Llama 3 annotations, applied to the crawl sample
    contamination  13-gram overlap between the scoreboard's passage (and the held-out text) and the training text
    accounting     FLOPs and activation memory of our model, counted by PyTorch, against 6N and the formulas
    collectives    all-reduce, reduce-scatter and all-gather timed on 4 processes (torch.distributed, gloo), against
                   the alpha-beta model
    parallel       data parallel and ZeRO-3 against one process; Megatron tensor parallel on 2 and 4 ranks; ring
                   attention on 4 ranks
    precision      a training run in FP32, BF16, FP16 without and with loss scaling, FP8 per tensor and per tile
    stability      a learning-rate sweep with and without QK-norm and z-loss, pushed to instability
    mtp            multi-token prediction against next-token prediction, at equal tokens; self-speculative acceptance
    mixture        RegMix on four groups of the novels: 32 small runs, a regression, the predicted mixture tested
    recipe_base, recipe_full, recipe_branch
                   our 2020 recipe against our 2026 recipe, same model, data and steps; a warmup-stable-decay
                   cooldown branched from the middle of the run
    recipe         the two models evaluated: held-out loss, bits per character on the scoreboard's passage, samples
    scoreboard     the series' scoreboard (Parts 1 and 14) with our two rows
    mfu            this computer's matrix-multiply peak and our training runs' model-FLOPs utilization
"""

from __future__ import annotations

import math
import re
import time
from pathlib import Path

import numpy as np

from explainer.ai.cache import Cache
from videos.ai.ai18 import facts as F

CACHE = Cache("ai18")
load = CACHE.load
RUNS = CACHE.dir / "runs"


def rng(seed) -> np.random.Generator:
    return np.random.default_rng(seed)


def log(msg: str) -> None:
    print(msg, flush=True)


def loadavg():
    import os

    try:
        return list(os.getloadavg())
    except (OSError, AttributeError):
        return None


# ---------------------------------------------------------------------------
# Published figures, and what follows from them
# ---------------------------------------------------------------------------
def compute_published():
    out = {}
    L = F.LLAMA3
    out["llama_6nd"] = 6 * L["params"] * L["tokens"]
    assert abs(out["llama_6nd"] / L["flops"] - 1) < 0.02
    out["llama_mfu"] = [r[8] * 1e12 / L["peak_bf16"] for r in L["table4"]]
    out["llama_mfu_reported"] = [r[9] for r in L["table4"]]
    hours = L["days"] * 24
    out["llama_mtbf_h"] = hours / L["unexpected"]
    out["llama_gpu_mtbf_years"] = out["llama_mtbf_h"] * L["gpus"] / (24 * 365.25)
    out["llama_ckpt_s"] = L["gpus"] * L["ckpt_per_gpu"][1] / L["tectonic_bw"]  # the largest checkpoint, sustained rate
    out["llama_young_s"] = math.sqrt(2 * out["llama_ckpt_s"] * out["llama_mtbf_h"] * 3600)
    out["llama_causes"] = [dict(name=n, count=c, share=c / L["unexpected"]) for n, c in L["causes"]]
    P = F.PALM
    out["palm_mfu"] = P["tps"] * 6 * P["params"] / (P["peak"] * P["chips"])
    assert abs(100 * out["palm_mfu"] - P["mfu_noattn"]) < 0.1
    D = F.DSV3
    out["dsv3_usd"] = D["hours"] * D["rate"]
    out["dsv3_per_T"] = D["hours_pre"] / (D["tokens"] / 1e12)
    assert abs(out["dsv3_per_T"] / D["hours_per_T"] - 1) < 0.01
    out["dsv3_days_per_T"] = D["hours_per_T"] / D["gpus"] / 24
    out["dsv3_days"] = D["hours_pre"] / D["gpus"] / 24
    out["dsv3_6nd"] = 6 * D["active"] * D["tokens"]
    out["dsv3_mtp_tokens"] = [1 + a / 100 for a in D["mtp_accept"]]  # tokens per forward pass with one draft
    # the DeepSeek-V3 learning-rate schedule, against tokens (Sec. 4.2)
    t = np.linspace(0, D["tokens"], 600)
    c0, c1 = D["lr_const_until"], D["lr_const_until"] + D["lr_decay_tokens"]
    lr = np.where(t < c0, D["lr_peak"], D["lr_end"] + (D["lr_peak"] - D["lr_end"]) * 0.5 *
                  (1 + np.cos(np.pi * np.clip((t - c0) / (c1 - c0), 0, 1))))
    lr = np.where(t >= c1, D["lr_tail"][0], lr)
    lr = np.where(t >= c1 + D["lr_tail"][1], D["lr_tail"][2], lr)
    out["dsv3_lr_t"], out["dsv3_lr"] = t, lr
    # memory: weights (2 bytes), gradients (2), Adam's FP32 master weights and two moments (12): 16 bytes a parameter
    out["mem16"] = {k: 16 * n for k, n in (("llama3", L["params"]), ("dsv3", D["total"]), ("k2", F.KIMIK2["total"]))}
    out["h100_needed"] = math.ceil(out["mem16"]["llama3"] / 80e9)
    Z = F.ZERO
    psi, nd, k = Z["psi"], Z["nd"], Z["k"]
    out["zero_mem"] = [(2 + 2 + k) * psi / 1e9, (2 + 2) * psi / 1e9 + k * psi / nd / 1e9,
                       2 * psi / 1e9 + (2 + k) * psi / nd / 1e9, (2 + 2 + k) * psi / nd / 1e9]
    for a, b in zip(out["zero_mem"], Z["mem"]):
        assert abs(a - b) < 0.06 * b + 0.05, (a, b)
    # RoPE: the slowest-turning pair of dimensions completes one turn every 2 pi base^((d-2)/d) tokens (d = 128)
    out["rope"] = [dict(base=b, longest=2 * math.pi * b ** (126 / 128)) for b in (10_000, 500_000, 1_000_000,
                                                                                    5_000_000)]
    out["rope_wavelengths"] = {str(b): (2 * math.pi * b ** (np.arange(0, 128, 2) / 128)).tolist()
                               for b in (10_000, 500_000)}
    out["ring_lower_bound"] = "2(p-1)/p n / B"
    # activations per layer and sequence (16-bit), Korthikanti et al.'s formula s b h (34 + 5 a s / h), at Llama 3
    # 405B's shape (h = 16,384, 128 heads, 126 layers) and a sequence of 8,192
    s_, h_, a_, L_ = 8192, 16384, 128, 126
    out["act_llama"] = dict(s=s_, h=h_, a=a_, layers=L_, linear=34 * s_ * h_, attn=5 * a_ * s_ * s_,
                            per_seq=34 * s_ * h_ * L_, recompute=2 * s_ * h_ * L_)
    return out


# ---------------------------------------------------------------------------
# Objectives
# ---------------------------------------------------------------------------
SENTENCE = ("It is a truth universally acknowledged, that a single man in possession of a good fortune must be in "
            "want of a wife.")


def compute_objectives():
    from explainer.ai import novels as N

    g = rng(2018)
    ids = N.encode(SENTENCE)
    toks = [N.decode([i]) for i in ids]
    n = len(ids)
    assert SENTENCE in (N.OUT.parent / "ai1" / "train.txt").read_text()  # Pride and Prejudice's first sentence
    # BERT: 15% of positions; of those 80% [MASK], 10% a random token, 10% unchanged
    pick = sorted(g.choice(n, max(1, round(0.15 * n)), replace=False).tolist())
    mlm = []
    for i in range(n):
        if i in pick:
            r = g.random()
            mlm.append(("[MASK]" if r < 0.8 else N.decode([int(g.integers(4, 4096))]) if r < 0.9 else toks[i], True))
        else:
            mlm.append((toks[i], False))
    # T5 span corruption: 15% of tokens in spans of mean length 3, each replaced by one sentinel
    noise = max(1, round(0.15 * n))
    spans = max(1, round(noise / 3))
    starts = sorted(g.choice(np.arange(1, n - 3), spans, replace=False).tolist())
    lens = [noise // spans + (1 if k < noise % spans else 0) for k in range(spans)]
    masked = set()
    for s, ln in zip(starts, lens):
        masked.update(range(s, min(n, s + ln)))
    sent = ["<X>", "<Y>", "<Z>"]
    inp, tgt, k, i = [], [], 0, 0
    while i < n:
        if i in masked:
            inp.append(sent[k])
            tgt.append(sent[k])
            while i < n and i in masked:
                tgt.append(toks[i])
                i += 1
            k += 1
        else:
            inp.append(toks[i])
            i += 1
    # fill in the middle (Bavarian et al.): cut the document at two random points; prefix, suffix, then middle
    a, b = sorted(g.choice(np.arange(2, n - 2), 2, replace=False).tolist())
    fim = dict(prefix=toks[:a], middle=toks[a:b], suffix=toks[b:])
    # prediction targets in a 256-token sequence, by objective
    T = 256
    targets = dict(causal=T - 1, mlm=round(0.15 * T), span=round(0.15 * T) + round(0.15 * T / 3), fim=T - 1)
    return dict(sentence=SENTENCE, tokens=toks, n=n, mlm=mlm, mlm_picked=pick, span_input=inp, span_target=tgt,
                fim=fim, targets=targets, T=T)


# ---------------------------------------------------------------------------
# Pipeline schedules
# ---------------------------------------------------------------------------
def compute_pipeline(p=4, m=8):
    from videos.ai.ai18 import sched as S

    out = {}
    runs = {"gpipe": (S.gpipe(p, m), 1, {"F": 1, "B": 2}), "1f1b": (S.one_f_one_b(p, m), 1, {"F": 1, "B": 2}),
            "interleaved": (S.interleaved(p, m, 2), 2, {"F": 1, "B": 2}),
            "zb": (S.zb_h1(p, m), 1, {"F": 1, "B": 1, "W": 1})}
    for name, (orders, v, dur) in runs.items():
        st, en = S.simulate_fixed(orders, p, v, dur)
        r = S.stats(st, en, p, v)
        r["ops"] = S.ops_list(st, en, p)
        r["v"] = v
        out[name] = r
    out["p"], out["m"] = p, m
    out["formula"] = dict(gpipe=(p - 1) / (m + p - 1), interleaved=(p - 1) / (2 * m + p - 1),
                          zb=(p - 1) / (3 * m + p - 1))
    for k in ("gpipe", "1f1b"):
        assert abs(out[k]["bubble"] - out["formula"]["gpipe"]) < 1e-9
    assert abs(out["interleaved"]["bubble"] - out["formula"]["interleaved"]) < 1e-9
    assert abs(out["zb"]["bubble"] - out["formula"]["zb"]) < 1e-9
    sweep = []
    for pp in (4, 8, 16):
        for mm in (4, 8, 16, 32, 64, 128):
            st, en = S.simulate_fixed(S.one_f_one_b(pp, mm), pp, 1, {"F": 1, "B": 2})
            sweep.append(dict(p=pp, m=mm, bubble=S.stats(st, en, pp)["bubble"], formula=(pp - 1) / (mm + pp - 1)))
    out["sweep"] = sweep
    return out


# ---------------------------------------------------------------------------
# Fault tolerance
# ---------------------------------------------------------------------------
def compute_faults(seed=54, runs=200):
    P = load("published")
    M = P["llama_mtbf_h"] * 3600  # seconds between unexpected interruptions, 16,384 GPUs
    delta = P["llama_ckpt_s"]  # seconds to write a checkpoint (the largest, at Tectonic's sustained rate)
    R = 600.0  # seconds to restart and reload (illustrative)
    H = F.LLAMA3["days"] * 86400.0
    g = rng(seed)
    taus = np.geomspace(60, 6 * 3600, 28)
    good = np.zeros((len(taus), runs))
    for i, tau in enumerate(taus):
        for r in range(runs):
            t = done = 0.0
            nxt = g.exponential(M)
            while t < H:
                seg = tau + delta
                if t + seg <= nxt:  # the segment and its checkpoint complete
                    t += seg
                    done += tau
                else:  # a failure: the work since the last checkpoint is lost, then a restart
                    t = nxt + R
                    nxt = t + g.exponential(M)
            good[i, r] = done / t
    mean = good.mean(1)
    best = int(mean.argmax())
    young = math.sqrt(2 * delta * M)
    first = 1 - (delta / taus + taus / (2 * M) + R / M)  # Young's first-order model
    return dict(M=M, delta=delta, R=R, H=H, taus=taus, goodput=mean, lo=np.percentile(good, 10, 1),
                hi=np.percentile(good, 90, 1), best_tau=float(taus[best]), best=float(mean[best]), young=young,
                first_order=first, young_goodput=float(np.interp(young, taus, mean)), runs=runs,
                interruptions_per_day=86400 / M)


# ---------------------------------------------------------------------------
# Model collapse
# ---------------------------------------------------------------------------
def compute_collapse(n=50_000, gens=30, seeds=5):
    """A unigram model of the novels' tokens fitted to n samples, then refitted, generation after generation, to n
    samples drawn from itself (replace), or to everything so far, real and synthetic (accumulate)."""
    from explainer.ai import novels as N

    tr, va = N.token_arrays()
    V = 4096
    p_true = np.bincount(va.astype(np.int64), minlength=V).astype(float)
    p_true /= p_true.sum()
    res = {"replace": [], "accumulate": []}
    for s in range(seeds):
        g = rng([77, s])
        start = int(g.integers(0, len(tr) - n))
        real = np.bincount(tr[start:start + n].astype(np.int64), minlength=V).astype(float)
        for mode in res:
            counts, total = real.copy(), real.copy()
            rows = []
            for k in range(gens + 1):
                q = (counts + 0.5) / (counts.sum() + 0.5 * V)  # what the next generation is scored with
                rows.append([int((counts > 0).sum()), float(-(p_true * np.log2(q)).sum()),
                             float(p_true[counts == 0].sum())])
                pk = counts / counts.sum()
                sample = np.bincount(g.choice(V, n, p=pk), minlength=V).astype(float)
                if mode == "replace":
                    counts = sample
                else:
                    total = total + sample
                    counts = total
            res[mode].append(rows)
    out = {m: np.asarray(v) for m, v in res.items()}  # seed, generation, (support, cross-entropy, lost mass)
    out["n"], out["gens"], out["seeds"] = n, gens, seeds
    return out


# ---------------------------------------------------------------------------
# The web: Common Crawl, language ID, extraction
# ---------------------------------------------------------------------------
SAFE = re.compile(r"(?i)\b(sex|porn|nude|naked|xxx|escort|casino|viagra|bet|gambl|adult|erotic|fuck|shit|kill|"
                  r"murder|drug|weed|cbd|loan|crypto|bitcoin|forex)")


def safe(text: str) -> bool:
    return not SAFE.search(text)


def compute_web():
    import json

    from videos.ai.ai18 import web as W

    pages = W.wet_pages()
    lid = W.lid_model()
    langs, english, blocked, ft_vs_cc = {}, [], 0, [0, 0]
    for pg in pages:
        if W.blocked(pg["url"]):
            blocked += 1
            continue
        lab, pr = W.identify(lid, pg["text"])
        pg["lang"], pg["prob"] = lab, pr
        langs[lab] = langs.get(lab, 0) + 1
        if pg["cc_lang"]:
            ft_vs_cc[0] += 1
            cc3 = pg["cc_lang"].split(",")[0]
            ft_vs_cc[1] += int({"eng": "en", "zho": "zh", "spa": "es", "deu": "de", "fra": "fr", "jpn": "ja",
                                "rus": "ru", "por": "pt", "ita": "it"}.get(cc3, cc3) == lab)
        nw = len(W.words(pg["text"]))
        if lab == "en" and pr >= F.FINEWEB["lid"] and nw >= 50:
            english.append(dict(url=pg["url"], text=pg["text"], prob=pr, words=nw))
    probs_en = [pg["prob"] for pg in pages if pg.get("lang") == "en"]
    (W.DIR / "english.jsonl").write_text("\n".join(json.dumps(e, ensure_ascii=False) for e in english))
    top = sorted(langs.items(), key=lambda kv: -kv[1])
    warc = W.warc_pages()
    hb = np.array([w["html_bytes"] for w in warc], float)
    tb = np.array([w["text_bytes"] for w in warc], float)
    ex = next((w for w in warc if 1000 < w["text_bytes"] < 8000 and 30_000 < w["html_bytes"] < 300_000
               and not W.blocked(w["url"]) and safe(w["text"]) and w["text"].isascii()), None)
    return dict(crawl=W.CRAWL, files=list(W.WET_FILES), chunks=W.WET_CHUNKS, chunk_bytes=W.CHUNK, n_pages=len(pages),
                blocked=blocked, langs=top[:12], n_langs=len(langs), english=len(english),
                english_any=len(probs_en), english_below=int(sum(p < F.FINEWEB["lid"] for p in probs_en)),
                text_bytes=int(sum(len(pg["text"].encode()) for pg in pages)), ft_vs_cc=ft_vs_cc,
                warc_pages=len(warc), html_bytes=float(hb.sum()), extracted_bytes=float(tb.sum()),
                extracted_share=float(tb.sum() / hb.sum()), empty=int((tb == 0).sum()),
                median_ratio=float(np.median(tb[tb > 0] / hb[tb > 0])),
                example=None if ex is None else dict(url=ex["url"], html_bytes=ex["html_bytes"],
                                                    text_bytes=ex["text_bytes"], text=ex["text"][:600]),
                loadavg=loadavg())


def _english():
    import json

    from videos.ai.ai18 import web as W

    if not (W.DIR / "english.jsonl").exists():
        CACHE.save("web", compute_web())
    return [json.loads(x) for x in (W.DIR / "english.jsonl").read_text().split("\n")]


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------
def compute_dedup(n_pairs=3000, seed=5):
    from videos.ai.ai18 import web as W

    docs = _english()
    fam = W.hash_family(F.FINEWEB["hashes"])
    B, R = F.FINEWEB["bands"], F.FINEWEB["rows"]
    wds = [W.words(d["text"]) for d in docs]
    sh = [W.shingles(w) for w in wds]
    sigs = [W.minhash(s, fam) for s in sh]
    # exact duplicates (the same normalized text), then near-duplicates: LSH candidates checked by their Jaccard
    seen, exact = {}, 0
    for i, w in enumerate(wds):
        key = hash(" ".join(w))
        if key in seen:
            exact += 1
        else:
            seen[key] = i
    cand = W.lsh_pairs(sigs, B, R)
    verified = [(i, j, W.jaccard(sh[i], sh[j])) for i, j in sorted(cand)]
    near = [(i, j, s) for i, j, s in verified if s >= F.FINEWEB["target"]]
    parent = list(range(len(docs)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i, j, _ in near:
        parent[find(i)] = find(j)
    clusters = {}
    for i in range(len(docs)):
        clusters.setdefault(find(i), []).append(i)
    dup_clusters = [c for c in clusters.values() if len(c) > 1]
    removed = sum(len(c) - 1 for c in dup_clusters)
    big = sorted(dup_clusters, key=len, reverse=True)[:6]
    examples = []
    for c in big:
        i, j = c[0], c[1]
        examples.append(dict(size=len(c), url_a=docs[i]["url"], url_b=docs[j]["url"],
                             jaccard=W.jaccard(sh[i], sh[j]), words=len(wds[i])))
    # the S-curve: pairs of known similarity (a page, and a copy with a fraction of its words replaced)
    g = rng(seed)
    vocab = sorted({w for ws in wds[:400] for w in ws})
    pool = [w for w in wds if len(w) >= 200]
    S_, A_, C_ = [], [], []
    for k in range(n_pairs):
        base = pool[int(g.integers(len(pool)))][:400]
        q = float(g.uniform(0.0, 0.45))
        mut = [vocab[int(g.integers(len(vocab)))] if g.random() < q else w for w in base]
        s1, s2 = W.shingles(base), W.shingles(mut)
        m1, m2 = W.minhash(s1, fam), W.minhash(s2, fam)
        S_.append(W.jaccard(s1, s2))
        A_.append(float((m1 == m2).mean()))
        C_.append(W.lsh_collide(m1, m2, B, R))
    S_, A_, C_ = np.array(S_), np.array(A_), np.array(C_, float)
    edges = np.linspace(0, 1, 21)
    bins = []
    for a, b in zip(edges, edges[1:]):
        sel = (S_ >= a) & (S_ < b if b < 1 else S_ <= b)
        if sel.sum() >= 5:
            bins.append(dict(lo=float(a), hi=float(b), n=int(sel.sum()), measured=float(C_[sel].mean()),
                             predicted=float(W.p_collide(S_[sel], B, R).mean()), agree=float(A_[sel].mean()),
                             s=float(S_[sel].mean())))
    # the thirty Gutenberg files: the same licence at the end of each, with the title changed
    from videos.ai.ai1 import compute as P1

    foot, body = [], []
    for n_ in P1.BOOKS:
        raw = (P1.BOOK_DIR / f"{n_}.txt").read_text(encoding="utf-8", errors="replace").replace("\r", "")
        mt = re.search(r"\*\*\* ?END OF (THE|THIS) PROJECT GUTENBERG EBOOK", raw)
        foot.append(W.shingles(W.words(raw[mt.start():])))
        body.append(W.shingles(W.words(P1.strip_gutenberg(raw))))
    fs = [W.minhash(s, fam) for s in foot]
    bs = [W.minhash(s, fam) for s in body]
    fj, fc = [], 0
    for i in range(len(foot)):
        for j in range(i + 1, len(foot)):
            fj.append(W.jaccard(foot[i], foot[j]))
            fc += W.lsh_collide(fs[i], fs[j], B, R)
    bc = sum(W.lsh_collide(bs[i], bs[j], B, R) for i in range(len(bs)) for j in range(i + 1, len(bs)))
    s_half = (1 - 0.5 ** (1 / B)) ** (1 / R)
    return dict(n=len(docs), exact=exact, candidates=len(cand), near_pairs=len(near), clusters=len(dup_clusters),
                removed=removed, removed_share=(removed + exact) / len(docs), examples=examples,
                pair_s=S_, pair_agree=A_, pair_collide=C_, bins=bins, bands=B, rows=R, hashes=F.FINEWEB["hashes"],
                agree_err=float(np.mean(np.abs(A_ - S_))), s_half=s_half,
                foot_pairs=len(fj), foot_caught=int(fc), foot_jaccard=[float(min(fj)), float(np.median(fj))],
                body_pairs=len(bs) * (len(bs) - 1) // 2, body_caught=int(bc),
                foot_words=int(np.median([len(s) for s in foot])))


# ---------------------------------------------------------------------------
# Quality: a classifier trained on FineWeb-Edu's annotations
# ---------------------------------------------------------------------------
def compute_quality(seed=3):
    """FineWeb-Edu's recipe, small: Llama-3-70B's 0-5 scores for web pages as labels, a cheap classifier (fastText on
    word bigrams, where FineWeb-Edu fitted a linear head on an embedding model) trained to reproduce them, and a
    threshold at 3: P(score >= 3) above a cut chosen on a validation split; then applied to our crawl sample."""
    import fasttext

    from videos.ai.ai18 import web as W

    rows = W.edu_annotations()
    g = rng(seed)
    order = g.permutation(len(rows))
    n_test = n_val = 1000
    test = [rows[i] for i in order[:n_test]]
    val = [rows[i] for i in order[n_test:n_test + n_val]]
    train = [rows[i] for i in order[n_test + n_val:]]
    path = CACHE.dir / "edu_train.txt"
    path.write_text("\n".join(f"__label__{r['score']} {W.ft_line(r['text'])}" for r in train))
    clf = fasttext.train_supervised(str(path), epoch=25, lr=0.3, wordNgrams=2, dim=64, minCount=3, thread=1,
                                    seed=0, verbose=0)
    path.unlink()

    def probs(text):
        labs, ps = clf.predict(W.ft_line(text), k=-1)
        d = {int(lab.replace("__label__", "")): float(p_) for lab, p_ in zip(labs, ps)}
        return np.array([d.get(k, 0.0) for k in range(6)])

    def f1(pred, truth):
        tp = int((pred & truth).sum())
        pr, rc = tp / max(1, int(pred.sum())), tp / max(1, int(truth.sum()))
        return 2 * pr * rc / max(1e-9, pr + rc), pr, rc

    pv = np.stack([probs(r["text"]) for r in val])
    tv = np.array([r["score"] >= 3 for r in val])
    cuts = np.linspace(0.02, 0.9, 89)
    cut = float(max(cuts, key=lambda c: f1(pv[:, 3:].sum(1) >= c, tv)[0]))
    pt = np.stack([probs(r["text"]) for r in test])
    truth = np.array([r["score"] for r in test])
    hi = pt[:, 3:].sum(1) >= cut
    f, prec, rec = f1(hi, truth >= 3)
    expect = pt @ np.arange(6)
    docs = _english()
    pc = np.stack([probs(d["text"]) for d in docs])
    kept = pc[:, 3:].sum(1) >= cut
    ec = pc @ np.arange(6)
    order_ = np.argsort(-pc[:, 3:].sum(1))
    good = [i for i in order_ if safe(docs[i]["text"]) and docs[i]["text"].isascii()][:3]
    bad = [i for i in order_[::-1] if safe(docs[i]["text"]) and docs[i]["text"].isascii()][:3]

    def ex(i):
        t = " ".join(docs[i]["text"].split())
        return dict(url=docs[i]["url"], p=float(pc[i, 3:].sum()), score=float(ec[i]), text=t[:220])

    return dict(n=len(rows), n_train=len(train), n_val=n_val, n_test=n_test,
                labels=np.bincount(truth, minlength=6).tolist(),
                all_labels=np.bincount([r["score"] for r in rows], minlength=6).tolist(), cut=cut, f1=f, precision=prec,
                recall=rec, test_pos=int((truth >= 3).sum()), corr=float(np.corrcoef(expect, truth)[0, 1]),
                cc_n=len(docs), cc_kept=float(kept.mean()), cc_kept_n=int(kept.sum()),
                cc_hist=np.histogram(ec, bins=np.arange(0, 5.5, 0.5))[0].tolist(),
                test_hist=np.histogram(expect, bins=np.arange(0, 5.5, 0.5))[0].tolist(),
                best=[ex(i) for i in good], worst=[ex(i) for i in bad])


# ---------------------------------------------------------------------------
# Contamination
# ---------------------------------------------------------------------------
def compute_contamination(n=13):
    from videos.ai.ai1 import compute as P1
    from videos.ai.ai18 import web as W

    train = W.words(P1.text("train"))

    def table(k):
        return np.unique(np.fromiter((hash(tuple(train[i:i + k])) for i in range(len(train) - k + 1)), np.int64))

    grams, g8 = table(n), table(8)

    def hits(ws, k=n, tab=grams):
        h = np.fromiter((hash(tuple(ws[i:i + k])) for i in range(len(ws) - k + 1)), np.int64)
        j = np.minimum(np.searchsorted(tab, h), len(tab) - 1)  # tab is sorted (np.unique)
        return np.nonzero(tab[j] == h)[0].tolist()

    pw = W.words(P1.text("passage"))
    ph, ph8 = hits(pw), hits(pw, 8, g8)
    paras = [p for p in P1.text("valid").split("\n") if len(p.split()) >= 20]
    flagged, example = 0, None
    for p in paras:
        ws = W.words(p)
        h = hits(ws)
        if h:
            flagged += 1
            if example is None and len(ws) > 30:
                example = " ".join(ws[h[0]:h[0] + n])
    return dict(n=n, train_grams=len(grams), passage_grams=len(pw) - n + 1, passage_hits=len(ph),
                passage_hits8=len(ph8), passage_grams8=len(pw) - 7, valid_paras=len(paras), valid_flagged=flagged,
                example=example)


# ---------------------------------------------------------------------------
# Accounting: FLOPs and activation memory, counted
# ---------------------------------------------------------------------------
RECIPE_SHAPE = dict(d=128, layers=4, heads=4, seq=256)


def _saved_bytes(fn):
    import torch

    seen = {}

    def pack(t):
        try:
            key = (t.untyped_storage().data_ptr(), t.untyped_storage().nbytes())
        except Exception:
            key = (id(t), t.numel() * t.element_size())
        seen[key] = key[1]
        return t

    with torch.autograd.graph.saved_tensors_hooks(pack, lambda t: t):
        out = fn()
    return out, sum(seen.values())


def compute_accounting():
    import torch
    import torch.nn.functional as Fn
    from torch.utils.checkpoint import checkpoint
    from torch.utils.flop_counter import FlopCounterMode

    from explainer.lm import pocket

    torch.set_num_threads(1)
    torch.manual_seed(0)
    cfg = pocket.Config(vocab=4096, d=RECIPE_SHAPE["d"], layers=RECIPE_SHAPE["layers"], heads=RECIPE_SHAPE["heads"],
                        seq=1024)
    m = pocket.PocketGPT(cfg)
    c = m.count()
    T = 256
    x = torch.randint(0, 4096, (1, T + 1))

    def loss():
        return Fn.cross_entropy(m(x[:, :-1]).flatten(0, 1), x[0, 1:])

    with FlopCounterMode(display=False) as fc:
        lv = loss()
    fwd = fc.get_total_flops()
    with FlopCounterMode(display=False) as fc:
        lv = loss()
        lv.backward()
    both = fc.get_total_flops()
    m.zero_grad()
    # with each block recomputed in the backward pass (activation checkpointing)
    def loss_ckpt():
        h = m.emb(x[:, :-1])
        for b in m.blocks:
            h = checkpoint(b, h, use_reentrant=False)
        return Fn.cross_entropy(m.head(m.norm(h)).flatten(0, 1), x[0, 1:])

    with FlopCounterMode(display=False) as fc:
        lc = loss_ckpt()
        lc.backward()
    both_ckpt = fc.get_total_flops()
    m.zero_grad()
    attn = 4 * T * T * cfg.d * cfg.layers  # QK^T and AV, forward, the full square
    six = 6 * c["compute"] * T
    import explainer.lm.pocket as PK

    def unfused(q, k, v, is_causal=True):
        s_ = (q @ k.transpose(-2, -1)) / math.sqrt(q.shape[-1])
        s_ = s_.masked_fill(~torch.ones(s_.shape[-2], s_.shape[-1], dtype=torch.bool).tril(), -float("inf"))
        return s_.softmax(-1) @ v

    sdpa = PK.F.scaled_dot_product_attention
    PK.F.scaled_dot_product_attention = unfused
    try:
        with FlopCounterMode(display=False) as fc:
            lu = loss()
            lu.backward()
        both_attn = fc.get_total_flops()
    finally:
        PK.F.scaled_dot_product_attention = sdpa
    m.zero_grad()
    # activation memory of the blocks against sequence length: attention fused (as PyTorch runs it), unfused (its
    # probabilities stored), and every block recomputed in the backward pass
    def blocks_saved(Tm, mode):
        h0 = torch.randn(1, Tm, cfg.d, requires_grad=True)

        def f():
            h = h0
            for b in m.blocks:
                h = checkpoint(b, h, use_reentrant=False) if mode == "recompute" else b(h)
            return h.sum()

        if mode == "unfused":
            PK.F.scaled_dot_product_attention = unfused
        try:
            return _saved_bytes(f)[1]
        finally:
            PK.F.scaled_dot_product_attention = sdpa

    mem = [dict(T=Tm, **{k: blocks_saved(Tm, k) for k in ("fused", "unfused", "recompute")})
           for Tm in (64, 128, 256, 512, 1024)]
    Ts = np.array([r["T"] for r in mem], float)
    A = np.stack([np.ones_like(Ts), Ts, Ts ** 2], 1)
    fit = {k: np.linalg.lstsq(A, np.array([r[k] for r in mem], float), rcond=None)[0].tolist()
           for k in ("fused", "unfused", "recompute")}
    per = lambda k: fit[k][1] / 4 / cfg.layers / cfg.d  # noqa: E731  (FP32 numbers per token per layer, units of d)
    return dict(params=int(c["total"]), compute_params=int(c["compute"]), d=cfg.d, layers=cfg.layers,
                heads=cfg.heads, hidden=cfg.hidden, T=T, fwd=fwd, both=both, bwd=both - fwd, ratio=(both - fwd) / fwd,
                both_ckpt=both_ckpt, ckpt_ratio=both_ckpt / both, six=six, attn=attn, both_attn=both_attn,
                attn_share=(both_attn - both) / both_attn, mem=mem, fit=fit, per_fused=per("fused"),
                per_unfused=per("unfused"), per_recompute=per("recompute"),
                quad_per_head=fit["unfused"][2] / 4 / cfg.layers / cfg.heads,
                body_share=c["body"] / c["compute"])


# ---------------------------------------------------------------------------
# Collectives, timed with torch.distributed
# ---------------------------------------------------------------------------
def compute_collectives(p=4, reps=5):
    from videos.ai.ai18 import dist as D

    sizes = [int(4 ** e) for e in range(5, 13)] + [2 ** 25]  # 1 KiB ... 16 MiB, 32 MiB
    la = loadavg()
    res = D.run(D.w_collectives, p, sizes, reps)
    ns = np.asarray(sizes, float)
    pp = np.asarray(res[0]["pingpong"])
    Am = np.stack([np.ones_like(ns), ns], 1) / pp[:, None]
    coef, *_ = np.linalg.lstsq(Am, np.ones_like(ns), rcond=None)
    alpha, B = float(coef[0]), float(1 / coef[1])
    meas = {}
    for k in ("all_reduce", "reduce_scatter", "all_gather"):
        T = np.array([[res[r][k][i] for r in range(p)] for i in range(len(sizes))])  # size, rank, rep
        meas[k] = T.max(1).min(1)
    nn_ = (ns // 4 // p * p) * 4
    pred = dict(all_reduce=2 * (p - 1) * alpha + 2 * (p - 1) / p * nn_ / B,
                reduce_scatter=(p - 1) * alpha + (p - 1) / p * nn_ / B,
                all_gather=(p - 1) * alpha + (p - 1) / p * nn_ / B)
    big = ns >= 2 ** 18
    ratio = {k: float(np.median(meas[k][big] / pred[k][big])) for k in meas}
    return dict(p=p, sizes=ns, bytes=nn_, pingpong=pp, alpha=alpha, B=B, ok=all(r["ok"] for r in res),
                **{f"m_{k}": v for k, v in meas.items()}, **{f"p_{k}": v for k, v in pred.items()}, ratio=ratio,
                loadavg_before=la, loadavg_after=loadavg())


# ---------------------------------------------------------------------------
# Data, ZeRO-3, tensor and context parallelism, on spawned processes
# ---------------------------------------------------------------------------
def compute_parallel(p=4):
    import torch

    from videos.ai.ai18 import dist as D

    torch.set_num_threads(1)
    ref = D.reference_run()
    dp = D.run(D.w_dp, p, "dp")
    z3 = D.run(D.w_dp, p, "zero3")
    x = ref["x"]
    err = {k: float((torch.tensor(r[0]["params"]) - x).abs().max()) for k, r in (("dp", dp), ("zero3", z3))}
    losses = dict(ref=ref["losses"], dp=dp[0]["losses"], zero3=z3[0]["losses"])
    tp = {str(q): D.run(D.w_tp, q)[0] for q in (2, 4)}
    ra = D.run(D.w_ring_attention, p)
    # causal work per rank (key blocks each query block attends to): contiguous blocks against 2p "zigzag" chunks
    contiguous = [r + 1 for r in range(p)]
    zigzag = [(r + 1) + (2 * p - r) for r in range(p)]  # chunks r and 2p-1-r: (r + 1) + (2p - r) half-blocks
    return dict(p=p, n_params=ref["n"], steps=D.DP_STEPS, batch=D.DP_BATCH, err=err, losses=losses,
                sent_dp=dp[0]["sent_per_step"], sent_z3=z3[0]["sent_per_step"],
                persistent_dp=dp[0]["persistent_elems"], persistent_z3=z3[0]["persistent_elems"],
                transient_z3=z3[0]["transient_elems"], comm_dp=dp[0]["comm_seconds"], comm_z3=z3[0]["comm_seconds"],
                tp=tp, ring=dict(err=max(r["err"] for r in ra), blocks=[r["blocks"] for r in ra],
                                 sent=ra[0]["sent_elems"], T=D.RA["T"], heads=D.RA["heads"], hd=D.RA["hd"]),
                contiguous=contiguous, zigzag=zigzag, tiny=D.TINY)


# ---------------------------------------------------------------------------
# Training runs on the novels
# ---------------------------------------------------------------------------
def _run_piece(spec, name, keep_model=False, **kw):
    """One training run, as plain data (curves thinned), resumable from its checkpoint."""
    from videos.ai.ai18 import lm

    RUNS.mkdir(parents=True, exist_ok=True)
    t = time.time()
    r = lm.train(spec, ckpt=RUNS / f"{name}.ckpt.pt", log=log, **kw)
    model = r.pop("_model")
    r.pop("_opts")
    if keep_model:
        import torch

        tmp = RUNS / f"{name}.pt.tmp"
        torch.save({"spec": r["spec"], "model": model.state_dict()}, tmp)
        tmp.replace(RUNS / f"{name}.pt")
    (RUNS / f"{name}.ckpt.pt").unlink(missing_ok=True)
    log(f"  {name}: val {r['final_val']:.3f} in {time.time() - t:.0f}s")
    r["_model"] = model
    return r


def _thin(r, every=1):
    out = {k: v for k, v in r.items() if k != "_model"}
    out["curve"] = out["curve"][::every]
    return out


SMALL = dict(d=64, layers=2, heads=2, seq=128, batch=16)
PRECISIONS = ["fp32", "bf16", "fp16", "fp16_scaled", "fp8_tensor", "fp8_tile"]


def _grad_histogram(steps=60):
    """log2 |dL/dy| at the outputs of the block's matrix products, FP32, after a few steps of training."""
    import torch
    import torch.nn.functional as Fn

    from videos.ai.ai18 import lm

    torch.set_num_threads(1)
    spec = lm.Spec(**SMALL, steps=steps, seed=0)
    model = lm.build(spec)
    from explainer.lm import pocket

    opts = pocket.make_optimizers(model, "adamw", spec.lr, spec.wd)
    from explainer.ai import novels as N

    tr, _ = N.token_arrays()
    grabbed = []
    hooks = [mod.register_full_backward_hook(lambda mod, gi, go: grabbed.append(go[0].detach().flatten()))
             for n, mod in model.named_modules() if isinstance(mod, torch.nn.Linear) and n.startswith("blocks")]
    for step in range(steps + 1):
        f = pocket.lr_factor(step, steps, "cosine", spec.warmup)
        for o in opts:
            for g in o.param_groups:
                g["lr"] = spec.lr * f
        x = lm.batch_at([tr], None, 0, step, spec.batch, spec.seq)
        grabbed.clear()
        loss = Fn.cross_entropy(model(x[:, :-1]).flatten(0, 1), x[:, 1:].flatten())
        for o in opts:
            o.zero_grad()
        loss.backward()
        for o in opts:
            o.step()
    for h in hooks:
        h.remove()
    g = torch.cat(grabbed).abs().numpy().astype(np.float64)
    nz = g[g > 0]
    edges = np.arange(-40, 1, 1.0)
    hist, _ = np.histogram(np.log2(nz), bins=edges)
    return dict(edges=edges, hist=hist / len(g), zero=float((g == 0).mean()), n=len(g),
                below_sub=float((g < 2.0 ** -25).mean()), below_normal=float((g < 2.0 ** -14).mean()),
                median_log2=float(np.median(np.log2(nz))), tokens=spec.batch * spec.seq)


def _quant_error():
    """Rounding error of E4M3 with one scale per tensor against one per 1 x 128 tile, on the real activations and
    weights of the series' base model (the inputs of its blocks' matrix products)."""
    import torch

    from explainer.ai import novels as N
    from videos.ai.ai18 import lm

    torch.set_num_threads(1)
    m = N.load_base()
    _, va = N.token_arrays()
    acts = []
    hooks = [mod.register_forward_hook(lambda mod, inp, out: acts.append(inp[0].detach().reshape(-1, inp[0].shape[-1])))
             for n, mod in m.named_modules() if isinstance(mod, torch.nn.Linear) and n.startswith("blocks")
             and n.endswith(("qkv", "gate"))]
    with torch.no_grad():
        m(torch.from_numpy(va[:257].astype(np.int64))[None, :-1])
    for h in hooks:
        h.remove()

    def rel(x, q):
        return float(((q - x).pow(2).mean() / x.pow(2).mean()).sqrt())

    rows = []
    for a in acts:
        rows.append(dict(tensor=rel(a, lm._f8(a, lm.E4M3, 448.0)), tile=rel(a, lm._f8_rows(a, lm.E4M3, 448.0, 128)),
                         ratio=float(a.abs().max() / a.abs().median())))
    W = [p_ for n, p_ in m.named_parameters() if n.startswith("blocks") and p_.dim() == 2]
    wt = [rel(w.detach(), lm._f8(w.detach(), lm.E4M3, 448.0)) for w in W]
    wb = [rel(w.detach(), lm._f8_blocks(w.detach(), lm.E4M3, 448.0, 128)) for w in W]
    a0 = acts[0]
    return dict(act_tensor=float(np.mean([r["tensor"] for r in rows])), act_tile=float(np.mean([r["tile"] for r in rows])),
                w_tensor=float(np.mean(wt)), w_block=float(np.mean(wb)), outlier=float(np.max([r["ratio"] for r in rows])),
                act_sample=a0[0, :128].numpy())


def compute_precision(steps=250, seeds=(0, 1)):
    from videos.ai.ai18 import lm

    part = CACHE.partial("precision", dict(steps=steps, seeds=list(seeds), v=2))
    runs = {}
    for v in PRECISIONS:
        for s in seeds:
            key = f"{v}_{s}"
            if key not in part:
                r = _run_piece(lm.Spec(**SMALL, steps=steps, seed=s, precision=v, eval_windows=16), f"prec_{key}")
                part[key] = _thin(r, 2)
            runs[key] = part[key]
    if "hist" not in part:
        part["hist"] = _grad_histogram()
    if "qerr" not in part:
        part["qerr"] = _quant_error()
    out = dict(runs=runs, precisions=PRECISIONS, seeds=list(seeds), steps=steps, hist=part["hist"], qerr=part["qerr"])
    out["final"] = {v: [runs[f"{v}_{s}"]["final_val"] for s in seeds] for v in PRECISIONS}
    return out


ACCUM = 64  # micro-batches a step's gradient is accumulated over, in the second precision experiment


def compute_precision_acc(steps=250, seeds=(0, 1)):
    """FP16 without and with loss scaling again, when each step's gradient is accumulated over 64 micro-batches (each
    micro-batch's loss divided by 64, as gradient accumulation and large data-parallel batches do): the gradients are
    64 times smaller while they are rounded."""
    from videos.ai.ai18 import lm

    part = CACHE.partial("precision_acc", dict(steps=steps, seeds=list(seeds), accum=ACCUM, v=1))
    runs = {}
    for v in ("fp16", "fp16_scaled"):
        for s in seeds:
            key = f"{v}_{s}"
            if key not in part:
                r = _run_piece(lm.Spec(**SMALL, steps=steps, seed=s, precision=v, eval_windows=16, grad_div=ACCUM),
                               f"precacc_{key}")
                part[key] = _thin(r, 2)
            runs[key] = part[key]
    return dict(runs=runs, accum=ACCUM, seeds=list(seeds), steps=steps,
                final={v: [runs[f"{v}_{s}"]["final_val"] for s in seeds] for v in ("fp16", "fp16_scaled")})


LRS = [3e-3, 1e-2, 3e-2, 1e-1]
STAB = {"plain": dict(), "qk": dict(qk_norm=True), "qkz": dict(qk_norm=True, z_loss=1e-4)}


def compute_stability(steps=150, seeds=(0, 1)):
    from videos.ai.ai18 import lm

    part = CACHE.partial("stability", dict(steps=steps, seeds=list(seeds), lrs=LRS, v=1))
    runs = {}
    for cfg, extra in STAB.items():
        for lr in LRS:
            for s in seeds:
                key = f"{cfg}_{lr:g}_{s}"
                if key not in part:
                    spec = lm.Spec(**SMALL, steps=steps, lr=lr, warmup=15, seed=s, probe_every=5, eval_windows=16,
                                   **extra)
                    part[key] = _thin(_run_piece(spec, f"stab_{key}"), 1)
                runs[key] = part[key]
    out = dict(runs=runs, lrs=LRS, configs=list(STAB), seeds=list(seeds), steps=steps)
    out["final"] = {c: [[runs[f"{c}_{lr:g}_{s}"]["final_val"] for s in seeds] for lr in LRS] for c in STAB}
    out["maxlogit"] = {c: [[max(p[1] for p in runs[f"{c}_{lr:g}_{s}"]["probes"]) for s in seeds] for lr in LRS]
                       for c in STAB}
    return out


def compute_mtp(steps=500, seeds=(0, 1)):
    from explainer.ai import novels as N
    from videos.ai.ai18 import lm

    part = CACHE.partial("mtp", dict(steps=steps, seeds=list(seeds), v=1))
    _, va = N.token_arrays()
    starts = np.linspace(0, len(va) - 200, 24).astype(int)
    prompts = [va[s:s + 32].astype(int).tolist() for s in starts]
    runs = {}
    for lam in (0.0, 0.3):
        for s in seeds:
            key = f"{lam:g}_{s}"
            if key not in part:
                spec = lm.Spec(**SMALL, steps=steps, warmup=30, seed=s, mtp=lam, mtp_late=0.1 if lam else None,
                               eval_windows=32)
                r = _run_piece(spec, f"mtp_{key}")
                model = r.pop("_model")
                piece = _thin(r, 2)
                if lam:
                    piece["accept"] = lm.mtp_acceptance(model, prompts, 40)
                    c = model.count()
                    extra = sum(p_.numel() for p_ in model.mtp.parameters()) + c["head"]
                    piece["extra_share"] = extra / (c["compute"] - extra)
                part[key] = piece
            runs[key] = part[key]
    out = dict(runs=runs, seeds=list(seeds), steps=steps)
    out["final"] = {lam: [runs[f"{lam}_{s}"]["final_val"] for s in seeds] for lam in ("0", "0.3")}
    out["accept"] = [runs[f"0.3_{s}"]["accept"]["rate"] for s in seeds]
    out["extra_share"] = runs[f"0.3_{seeds[0]}"]["extra_share"]
    return out


# ---------------------------------------------------------------------------
# Mixtures: RegMix on groups of the novels
# ---------------------------------------------------------------------------
GROUPS = {
    "American": [2701, 76, 74, 64317, 1952, 160, 514],
    "English society": [1342, 158, 1260, 145, 768, 1400, 98, 46],
    "Adventure and mystery": [1661, 2852, 120, 43, 345, 84, 174, 36, 35, 219],
    "Translations and Ulysses": [1184, 2600, 2554, 28054, 4300],
}


def group_arrays():
    """The training paragraphs of each group of books (Part 1's split), as token arrays; cached."""
    from explainer.ai import novels as N
    from videos.ai.ai1 import compute as P1

    path = CACHE.dir / "groups.npz"
    if path.exists():
        with np.load(path) as z:
            return [z[k] for k in GROUPS]
    arrs = {}
    for gname, books in GROUPS.items():
        ids = []
        for n_ in books:
            raw = (P1.BOOK_DIR / f"{n_}.txt").read_text(encoding="utf-8", errors="replace")
            paras = P1.clean(P1.strip_gutenberg(raw)).split("\n")
            for k in range(0, len(paras), 40):
                if (k // 40) % 20 != 7:
                    for p_ in paras[k:k + 40]:
                        ids.extend(N.encode(p_ + "\n"))
        arrs[gname] = np.asarray(ids, np.uint16)
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    np.savez(CACHE.dir / "groups.tmp.npz", **arrs)
    (CACHE.dir / "groups.tmp.npz").replace(path)
    return [arrs[k] for k in GROUPS]


def falcon_ids(n: int):
    """Chapter n of The Maltese Falcon, as tokens (chapter 2 is the scoreboard's passage)."""
    from explainer.ai import novels as N
    from videos.ai.ai1 import compute as P1

    raw = (P1.BOOK_DIR / f"{P1.FALCON}.txt").read_text(encoding="utf-8")
    return N.encode(P1.falcon_chapter(P1.strip_gutenberg(raw), n))


def _features(w):
    w = np.asarray(w, float)
    q = [w[i] * w[j] for i in range(len(w)) for j in range(i, len(w))]
    return np.concatenate([w, q])


def compute_mixture(n_proxy=32, seed=11):
    import torch

    from explainer.ai import novels as N
    from videos.ai.ai18 import lm

    torch.set_num_threads(1)
    arrays = group_arrays()
    sizes = np.array([len(a) for a in arrays], float)
    natural = (sizes / sizes.sum()).tolist()
    _, va = N.token_arrays()
    target = falcon_ids(1) + falcon_ids(3)  # chosen on chapters 1 and 3; tested on chapter 2, the scoreboard's
    test = falcon_ids(2)
    g = rng(seed)
    mixes = [g.dirichlet(np.ones(len(arrays))).tolist() for _ in range(n_proxy)]
    part = CACHE.partial("mixture", dict(n=n_proxy, seed=seed, v=1))
    proxy = []
    for k, w in enumerate(mixes):
        key = f"proxy_{k}"
        if key not in part:
            spec = lm.Spec(d=48, layers=2, heads=2, seq=128, batch=16, steps=120, warmup=12, mix=w, seed=0,
                           eval_windows=16)
            r = _run_piece(spec, f"mix_{key}", arrays=arrays, valid=va)
            m = r.pop("_model")
            part[key] = dict(w=w, target=lm.text_nats(m, target), test=lm.text_nats(m, test), val=r["final_val"])
        proxy.append(part[key])
    X = np.stack([_features(p_["w"]) for p_ in proxy])
    y = np.array([p_["target"] for p_ in proxy])
    lam = 1e-3

    def fit(Xa, ya):
        A = np.hstack([Xa, np.ones((len(Xa), 1))])
        return np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1]), A.T @ ya)

    coef = fit(X, y)
    loo = []
    for i in range(len(y)):
        c_ = fit(np.delete(X, i, 0), np.delete(y, i))
        loo.append(float(np.append(X[i], 1) @ c_))
    cand = g.dirichlet(np.ones(len(arrays)), 100_000)
    pred = np.hstack([np.stack([_features(c) for c in cand]), np.ones((len(cand), 1))]) @ coef
    best = cand[np.argsort(pred)[:100]].mean(0)  # RegMix: the average of the top 100 predicted mixtures
    pred_best = float(np.append(_features(best), 1) @ coef)
    pred_nat = float(np.append(_features(natural), 1) @ coef)
    tests = {}
    for name, w in (("natural", natural), ("uniform", [0.25] * 4), ("regmix", best.tolist())):
        for s in (0, 1):
            key = f"test_{name}_{s}"
            if key not in part:
                spec = lm.Spec(d=64, layers=2, heads=2, seq=128, batch=16, steps=300, warmup=20, mix=w, seed=s,
                               eval_windows=16)
                r = _run_piece(spec, f"mix_{key}", arrays=arrays, valid=va)
                m = r.pop("_model")
                part[key] = dict(w=w, target=lm.text_nats(m, target), test=lm.text_nats(m, test), val=r["final_val"])
            tests[key] = part[key]
    corr = float(np.corrcoef(loo, y)[0, 1])
    return dict(groups=list(GROUPS), books={k: len(v) for k, v in GROUPS.items()}, sizes=sizes.tolist(),
                natural=natural, proxy=proxy, coef=coef.tolist(), loo=loo, loo_corr=corr, best=best.tolist(),
                pred_best=pred_best, pred_natural=pred_nat, tests=tests, target_tokens=len(target),
                test_tokens=len(test), proxy_spec=dict(d=48, layers=2, steps=120), test_spec=dict(d=64, layers=2,
                                                                                                  steps=300))


# ---------------------------------------------------------------------------
# Our full-recipe model against the 2020 recipe
# ---------------------------------------------------------------------------
RECIPE_STEPS = 732  # 3.0 million tokens at 16 x 256 a step: Part 14's budget
SNAPS = [0, 10, 25, 50, 100, 200, 366, 550, 732]
BRANCH = 366  # a cooldown branched from the middle of the stable phase
RECIPES = {
    "base": dict(optimizer="adamw", schedule="cosine", final=0.1),
    "full": dict(optimizer="muon", schedule="wsd", decay_frac=0.2, final=0.0, qk_norm=True, z_loss=1e-4),
}


def _recipe_spec(name, **kw):
    from videos.ai.ai18 import lm

    return lm.Spec(**RECIPE_SHAPE, batch=16, steps=RECIPE_STEPS, lr=3e-3, warmup=100, seed=0, eval_windows=48,
                   eval_every=24, snaps=SNAPS, keep=[BRANCH] if name == "full" else [], probe_every=12,
                   **{**RECIPES[name], **kw})


def _recipe(name):
    r = _run_piece(_recipe_spec(name), f"recipe_{name}", keep_model=True)
    return _thin(r, 2)


def compute_recipe_base():
    return _recipe("base")


def compute_recipe_full():
    return _recipe("full")


def compute_recipe_branch():
    """The 2026 recipe's run, from its state at step 366 of the stable phase, decayed over the next 92 steps (a
    budget of 458 steps, 20% of it cooling down): an answer at 1.9M tokens without starting again."""
    import torch

    if not CACHE.path("recipe_full").exists() or not (RUNS / f"recipe_full.step{BRANCH}.pt").exists():
        CACHE.save("recipe_full", compute_recipe_full())
    state = torch.load(RUNS / f"recipe_full.step{BRANCH}.pt", weights_only=False)
    total = int(round(BRANCH / 0.8))
    spec = _recipe_spec("full", steps=total, decay_start=BRANCH, keep=[], snaps=[])
    r = _run_piece(spec, "recipe_branch", init_state=state)
    return _thin(r, 2)


def _trained(name):
    import torch

    from videos.ai.ai18 import lm

    if not CACHE.path(f"recipe_{name}").exists() or not (RUNS / f"recipe_{name}.pt").exists():
        CACHE.save(f"recipe_{name}", ITEMS[f"recipe_{name}"]())
    ck = torch.load(RUNS / f"recipe_{name}.pt", weights_only=False)
    m = lm.build(lm.Spec(**{k: v for k, v in ck["spec"].items()}))
    m.load_state_dict(ck["model"])
    return m.eval()


def compute_recipe():
    import torch

    from videos.ai.ai1 import compute as P1
    from videos.ai.ai14 import lm as lm14

    torch.set_num_threads(1)
    passage = P1.text("passage")
    out = {}
    for name in RECIPES:
        m = _trained(name)
        b = lm14.bits_per_char(m, passage)
        r = load(f"recipe_{name}")
        out[name] = dict(bits=b["bits"], params=int(m.count()["total"]), val=r["final_val"], seconds=r["seconds"],
                         tokens=r["tokens"], max_logit=max(p_[1] for p_ in r["probes"]))
    br = load("recipe_branch")
    full = load("recipe_full")
    stable_at = [e for e in full["evals"] if e[0] <= br["spec"]["steps"]][-1]
    out["branch"] = dict(steps=br["spec"]["steps"], val=br["final_val"], stable_val=stable_at[2],
                         stable_step=stable_at[0], tokens=br["tokens"])
    return out


def compute_scoreboard():
    """The series' scoreboard, as Part 14 left it (Part 1's baselines, Part 14's family, the series' base model),
    with our two models."""
    from videos.ai.ai14.compute import load as load14

    S14 = load14("scoreboard")
    rows = [dict(label=r["label"], bits=r["bits"], kind=r["kind"], part=r["part"]) for r in S14["rows"]]
    names = {"gpt_xs": "XS", "gpt_s": "S", "gpt_m": "M", "gpt_l": "L"}
    for r in S14["ours"]:
        rows.append(dict(label=f"Part 14, model {names[r['name']]}", bits=r["bits"], kind="lm", part=14,
                         params=r["params"], name=r["name"]))
    B = load14("scoreboard_base")
    rows.append(dict(label="the series' model", bits=B["bits"], kind="lm", part=14, params=B["params"], name="base"))
    R = load("recipe")
    for k in RECIPES:
        rows.append(dict(label=k, bits=R[k]["bits"], kind="lm", part=18, params=R[k]["params"], name=f"recipe_{k}"))
    return dict(rows=rows, chars=S14["chars"])


def compute_mfu():
    import torch

    from explainer.lm import pocket

    torch.set_num_threads(1)
    best = 0.0
    a, b = torch.randn(1024, 1024), torch.randn(1024, 1024)
    for _ in range(8):
        t = time.perf_counter()
        a @ b
        best = max(best, 2 * 1024 ** 3 / (time.perf_counter() - t))
    out = dict(peak=best, loadavg=loadavg())
    for name in RECIPES:
        r = load(f"recipe_{name}")
        cfg = pocket.Config(vocab=4096, **RECIPE_SHAPE)
        fpt = pocket.flops_per_token(r["counts"], cfg)
        tps = r["tokens"] / r["seconds"]
        out[name] = dict(tokens_per_s=tps, flops_per_token=fpt, achieved=tps * fpt, mfu=tps * fpt / best)
    return out


ITEMS = {
    "published": compute_published,
    "objectives": compute_objectives,
    "pipeline": compute_pipeline,
    "faults": compute_faults,
    "collapse": compute_collapse,
    "web": compute_web,
    "dedup": compute_dedup,
    "quality": compute_quality,
    "contamination": compute_contamination,
    "accounting": compute_accounting,
    "collectives": compute_collectives,
    "parallel": compute_parallel,
    "precision": compute_precision,
    "precision_acc": compute_precision_acc,
    "stability": compute_stability,
    "mtp": compute_mtp,
    "mixture": compute_mixture,
    "recipe_base": compute_recipe_base,
    "recipe_full": compute_recipe_full,
    "recipe_branch": compute_recipe_branch,
    "recipe": compute_recipe,
    "scoreboard": compute_scoreboard,
    "mfu": compute_mfu,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    import os

    os.environ.setdefault("OMP_NUM_THREADS", "1")
    CACHE.main(ITEMS, __doc__)
