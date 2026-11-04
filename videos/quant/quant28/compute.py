"""Every number in Part 28 (Text, LLMs and Alternative Data), computed and cached in .cache/quant28/.

    python -m videos.quant.quant28.compute [items] [--force]

The corpus: every FOMC statement (1997-2025) and set of minutes (1996-2025) the Board's meeting pages link to; the
market's reaction: the 2-year Treasury yield (FRED DGS2) from the close before a statement to the close of its day.
Research uses documents dated to December 2020; 2021-2025 is sealed and read once, in ``envelope``.

* ``corpus``      sizes, Zipf's law, the vocabulary's growth;
* ``hook``        the statement day with the largest 2-year move, and what changed in the words;
* ``tone``        Loughran-McDonald tone of every statement, and the 2-year yield's reaction to it;
* ``form``        length and the fog index of statements over time;
* ``sestm``       Ke, Kelly and Xiu's SESTM on the statements: screened words, topics, out-of-sample scores;
* ``topics``      non-negative matrix factorisation topics of the minutes, and their shares over time;
* ``phrases``     forward guidance: when each phrase entered and left the statement;
* ``embed``       word vectors from the minutes (PPMI and SVD): neighbours and a map;
* ``lm``          pocket language models trained on the minutes through 2007 and through 2020, replayed;
* ``lookahead``   the time-sliced experiment: what each model knows about 2008-2012;
* ``altdata``     a signal's decay as a data set spreads, simulated;
* ``theory``      the research chapter: SESTM's screening, proved, simulated and applied;
* ``envelope``    the statement-score signal, registered and opened on 2021-2025.
"""

from __future__ import annotations

import functools
import json
import math
import warnings

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import pit, text as TX

warnings.filterwarnings("ignore", category=RuntimeWarning)

CACHE = Cache("quant28")
load = pit.counted(CACHE.load, 28)
RESEARCH_END = 20201231
TRAIN_END = 20121231            # SESTM trained on statements to here, tested 2013-2020


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


# ---------------------------------------------------------------------------
# The corpus and the market's reaction
# ---------------------------------------------------------------------------
@functools.lru_cache(maxsize=None)
def _docs(kind: str, through: int = RESEARCH_END):
    rows = [(d, t) for d, t in data.fomc_text(kind) if d <= through]
    return [d for d, _ in rows], [t for _, t in rows], [TX.tokenize(t) for _, t in rows]


@functools.lru_cache(maxsize=None)
def _yields():
    g2 = data.fred("DGS2", start="1996-01-01", through="2025-12-31")
    g10 = data.fred("DGS10", start="1996-01-01", through="2025-12-31")
    return g2, g10


def _reaction(dates, series, horizon: int = 0):
    """Change in a daily yield (basis points) from the close before each date to the close ``horizon`` trading days
    after the first trading day on or after it."""
    d, v = series["date"], series["value"]
    out = []
    for t in dates:
        k = int(np.searchsorted(d, t))            # first trading day >= t
        if k == 0 or k + horizon >= len(d):
            out.append(np.nan)
            continue
        out.append(100 * (v[k + horizon] - v[k - 1]))
    return np.array(out)


def _drift(dates, series, h: int = 5):
    """Change from the statement day's close to ``h`` trading days later (basis points): what is left to trade."""
    d, v = series["date"], series["value"]
    out = []
    for t in dates:
        k = int(np.searchsorted(d, t))
        out.append(100 * (v[k + h] - v[k]) if k + h < len(d) else np.nan)
    return np.array(out)


def compute_corpus() -> dict:
    ds, ts, toks = _docs("statement")
    dm, tm, tokm = _docs("minutes")
    alltok = [w for t in toks for w in t] + [w for t in tokm for w in t]
    z = TX.zipf(alltok)
    # vocabulary growth: distinct words seen by each year (minutes), the Heaps curve
    years = sorted(set(d // 10000 for d in dm))
    seen, growth = set(), []
    for y in years:
        for d, t in zip(dm, tokm):
            if d // 10000 == y:
                seen.update(t)
        growth.append(len(seen))
    top = sorted(((c, w) for w, c in __import__("collections").Counter(alltok).items()), reverse=True)[:30]
    ranks = np.unique(np.round(np.logspace(0, math.log10(len(z["freq"])), 80)).astype(int))
    return _json({"n_statements": len(ds), "n_minutes": len(dm), "first_statement": ds[0], "last_statement": ds[-1],
                  "first_minutes": dm[0], "last_minutes": dm[-1],
                  "words_statements": int(sum(map(len, toks))), "words_minutes": int(sum(map(len, tokm))),
                  "zipf_slope": z["slope"], "zipf_intercept": z["intercept"], "n_types": z["n_types"],
                  "n_tokens": z["n_tokens"], "zipf_rank": ranks, "zipf_freq": z["freq"][ranks - 1],
                  "top": [[w, int(c)] for c, w in top], "years": years, "growth": growth,
                  "median_statement_words": float(np.median([len(t) for t in toks])),
                  "median_minutes_words": float(np.median([len(t) for t in tokm]))})


def compute_hook() -> dict:
    ds, ts, toks = _docs("statement")
    g2, _ = _yields()
    dy = _reaction(ds, g2)
    ok = np.isfinite(dy)
    i = int(np.nanargmax(np.where(ok, np.abs(dy), -1)))
    diff = TX.word_diff(ts[i - 1], ts[i]) if i > 0 else []
    ranked = np.argsort(-np.where(ok, np.abs(dy), -1))[:8]
    return _json({"date": ds[i], "prev": ds[i - 1], "dy": float(dy[i]), "text": ts[i], "prev_text": ts[i - 1],
                  "diff": diff, "top": [[ds[k], float(dy[k])] for k in ranked],
                  "sd": float(np.nanstd(dy)), "n": int(ok.sum()), "mean_abs": float(np.nanmean(np.abs(dy)))})


def _tone_rows(toks, lm):
    return [TX.tone(t, lm) for t in toks]


def compute_tone() -> dict:
    lm = TX.lm_sets(data.lm_dictionary())
    ds, ts, toks = _docs("statement")
    g2, g10 = _yields()
    dy2, dy10 = _reaction(ds, g2), _reaction(ds, g10)
    T = _tone_rows(toks, lm)
    neg = np.array([r["negative"] for r in T])
    pos = np.array([r["positive"] for r in T])
    unc = np.array([r["uncertainty"] for r in T])
    net = pos - neg
    dnet = np.r_[np.nan, np.diff(net)]
    out = {"dates": ds, "neg": neg, "pos": pos, "unc": unc, "net": net, "dy2": dy2, "dy10": dy10}
    regs = {}
    for name, x in (("net", net), ("dnet", dnet), ("neg", neg), ("unc", unc)):
        m = np.isfinite(x) & np.isfinite(dy2)
        r = stats.linregress(100 * x[m], dy2[m])
        regs[name] = {"slope": r.slope, "t": r.slope / r.stderr if r.stderr > 0 else 0.0, "r2": r.rvalue ** 2,
                      "n": int(m.sum())}
    out["regs"] = regs
    # the words doing the work: LM words in the statements, by count
    from collections import Counter
    c_neg, c_pos, c_unc = Counter(), Counter(), Counter()
    for t in toks:
        for w in t:
            u = w.upper()
            if u in lm["_Negative_set"]:
                c_neg[w] += 1
            if u in lm["_Positive_set"]:
                c_pos[w] += 1
            if u in lm["_Uncertainty_set"]:
                c_unc[w] += 1
    out["top_neg"] = c_neg.most_common(12)
    out["top_pos"] = c_pos.most_common(12)
    out["top_unc"] = c_unc.most_common(12)
    out["n_lm"] = {"negative": len(data.lm_dictionary()["Negative"]), "positive": len(data.lm_dictionary()["Positive"]),
                   "uncertainty": len(data.lm_dictionary()["Uncertainty"])}
    return _json(out)


def compute_form() -> dict:
    ds, ts, toks = _docs("statement")
    F = [TX.fog(t) for t in ts]
    dm, tm, tokm = _docs("minutes")
    return _json({"dates": ds, "words": [f["words"] for f in F], "fog": [f["fog"] for f in F],
                  "wps": [f["words_per_sentence"] for f in F], "complex": [f["complex"] for f in F],
                  "min_dates": dm, "min_words": [len(t) for t in tokm],
                  "first5": float(np.median([f["words"] for d, f in zip(ds, F) if d < 20020101])),
                  "last5": float(np.median([f["words"] for d, f in zip(ds, F) if d >= 20160101])),
                  "fog_first": float(np.median([f["fog"] for d, f in zip(ds, F) if d < 20020101])),
                  "fog_last": float(np.median([f["fog"] for d, f in zip(ds, F) if d >= 20160101]))})


# ---------------------------------------------------------------------------
# SESTM on the statements
# ---------------------------------------------------------------------------
STOP = set("the of and to in a that for its at on be by with as is are has have was were it this from which an or "
           "will would been their than also over such these other committee federal open market".split())


def _sestm_fit(toks_tr, y_tr, vocab, alpha, kappa):
    D = TX.dtm(toks_tr, vocab)
    s = TX.sestm_screen(D, y_tr, alpha=alpha, kappa=kappa)
    if len(s["pos"]) == 0 or len(s["neg"]) == 0:
        return None
    tp = TX.sestm_topics(D[:, s["S"]], y_tr)
    return s, tp


def compute_sestm() -> dict:
    ds, ts, toks = _docs("statement")
    g2, _ = _yields()
    y = _reaction(ds, g2)
    ds = np.array(ds)
    ok = np.isfinite(y) & (y != 0)
    tr = ok & (ds <= TRAIN_END)
    te = ok & (ds > TRAIN_END)
    toks_tr = [toks[i] for i in np.flatnonzero(tr)]
    vocab = TX.vocabulary(toks_tr, min_df=3, stop=STOP)
    # choose (alpha, kappa) by a time-ordered split inside the training years: fit to 2006, validate 2007-2012
    grid = [(a, k) for a in (0.05, 0.1, 0.15, 0.2) for k in (5, 10, 20)]
    fit_m = tr & (ds <= 20061231)
    val_m = tr & (ds > 20061231)
    cv = []
    for a, k in grid:
        f = _sestm_fit([toks[i] for i in np.flatnonzero(fit_m)], y[fit_m], vocab, a, k)
        if f is None:
            cv.append({"alpha": a, "kappa": k, "corr": np.nan, "n_words": 0})
            continue
        s, tp = f
        Dv = TX.dtm([toks[i] for i in np.flatnonzero(val_m)], vocab)[:, s["S"]]
        sc = np.array([TX.sestm_score(d_, tp["O_pos"], tp["O_neg"]) for d_ in Dv])
        cv.append({"alpha": a, "kappa": k, "corr": float(stats.spearmanr(sc, y[val_m])[0]), "n_words": int(len(s["S"]))})
    best = max((c for c in cv if np.isfinite(c["corr"])), key=lambda c: c["corr"])
    s, tp = _sestm_fit(toks_tr, y[tr], vocab, best["alpha"], best["kappa"])
    Dte = TX.dtm([toks[i] for i in np.flatnonzero(te)], vocab)[:, s["S"]]
    Dtr = TX.dtm(toks_tr, vocab)[:, s["S"]]
    sc_te = np.array([TX.sestm_score(d_, tp["O_pos"], tp["O_neg"]) for d_ in Dte])
    sc_tr = np.array([TX.sestm_score(d_, tp["O_pos"], tp["O_neg"]) for d_ in Dtr])
    words = [vocab[j] for j in s["S"]]
    pos_w = sorted(((s["f"][j], vocab[j], int(s["k"][j])) for j in s["pos"]), reverse=True)
    neg_w = sorted(((s["f"][j], vocab[j], int(s["k"][j])) for j in s["neg"]))
    yte = y[te]
    hit = float(np.mean(np.sign(sc_te - 0.5) == np.sign(yte)))
    rho, p_rho = stats.spearmanr(sc_te, yte)
    return _json({"alpha": best["alpha"], "kappa": best["kappa"], "cv": cv, "pi": s["pi"], "n_vocab": len(vocab),
                  "n_train": int(tr.sum()), "n_test": int(te.sum()), "words": words,
                  "pos": [[w, float(f), k] for f, w, k in pos_w[:15]], "neg": [[w, float(f), k] for f, w, k in neg_w[:15]],
                  "n_pos": int(len(s["pos"])), "n_neg": int(len(s["neg"])),
                  "O_pos": tp["O_pos"], "O_neg": tp["O_neg"],
                  "train_dates": ds[tr], "train_score": sc_tr, "train_y": y[tr],
                  "test_dates": ds[te], "test_score": sc_te, "test_y": yte, "hit": hit, "rho": float(rho),
                  "p_rho": float(p_rho), "rho_train": float(stats.spearmanr(sc_tr, y[tr])[0]),
                  "f_all": s["f"], "k_all": s["k"], "vocab": vocab})


# ---------------------------------------------------------------------------
# Topics, phrases, embeddings
# ---------------------------------------------------------------------------
MIN_STOP = STOP | set("participants members staff noted said percent rate rates period recent quarter year months "
                      "month first second third fourth half january february march april may june july august "
                      "september october november december meeting also could might many some while messrs mr ms "
                      "shall chairman chair president vice subcommittee paragraph division director al b c d e "
                      "authorization authorizes authorized arrangements accounts secretary deputy associate assistant "
                      "economist economists governors board bank reserve new york".split())


def compute_topics(k: int = 8) -> dict:
    dm, tm, tokm = _docs("minutes")
    vocab = TX.vocabulary(tokm, min_df=10, max_df=0.6, stop=MIN_STOP)
    X = TX.tfidf(TX.dtm(tokm, vocab))
    r = TX.nmf_topics(X, k=k, iters=500, seed=28)
    tops = [[vocab[j] for j in np.argsort(-r["H"][t])[:10]] for t in range(k)]
    return _json({"dates": dm, "share": r["share"], "top_words": tops, "err": r["err"], "n_vocab": len(vocab), "k": k})


PHRASES = ["considerable period", "likely to be measured", "extended period", "exceptionally low levels", "patient",
           "some time", "gradual", "accommodative", "ongoing increases", "highly accommodative", "transitory",
           "balance of risks", "pandemic"]


def compute_phrases() -> dict:
    ds, ts, toks = _docs("statement", through=20251231)
    rows = {}
    for p in PHRASES:
        hits = [int(p in t.lower()) for t in ts]
        on = [d for d, h in zip(ds, hits) if h]
        rows[p] = {"hits": hits, "first": on[0] if on else None, "last": on[-1] if on else None, "n": len(on)}
    return _json({"dates": ds, "rows": rows, "research_end": RESEARCH_END})


EMBED_WORDS = ["inflation", "unemployment", "accommodation", "purchases", "housing", "uncertainty", "tightening",
               "liquidity"]


def compute_embed(V: int = 3000, dim: int = 50) -> dict:
    dm, tm, tokm = _docs("minutes")
    from collections import Counter
    c = Counter(w for t in tokm for w in t if w not in STOP)
    vocab = sorted(w for w, _ in c.most_common(V))
    C = TX.cooccurrence(tokm, vocab, window=5)
    E = TX.ppmi_svd(C, dim=dim)
    nb = {w: TX.neighbours(E, vocab, w, k=8) for w in EMBED_WORDS if w in vocab}
    # a 2-D map of a few hundred common words: PCA of their vectors
    show = [w for w, _ in c.most_common(400) if w in vocab][:250]
    idx = [vocab.index(w) for w in show]
    Y = E[idx] - E[idx].mean(0)
    U, s_, Vt = np.linalg.svd(Y, full_matrices=False)
    xy = Y @ Vt[:2].T
    # an analogy, by vector arithmetic
    def vec(w):
        return E[vocab.index(w)]
    analog = []
    for a, b, c_ in (("tightening", "raise", "lower"), ("inflation", "prices", "employment")):
        if all(x in vocab for x in (a, b, c_)):
            q = vec(a) - vec(b) + vec(c_)
            q = q / np.linalg.norm(q)
            sims = E @ q
            best = [vocab[j] for j in np.argsort(-sims) if vocab[j] not in (a, b, c_)][:3]
            analog.append({"a": a, "b": b, "c": c_, "best": best})
    return _json({"V": V, "dim": dim, "neighbours": nb, "map_words": show, "map_xy": xy, "analogies": analog,
                  "n_tokens": int(sum(map(len, tokm)))})


# ---------------------------------------------------------------------------
# Pocket language models: the time-sliced experiment
# ---------------------------------------------------------------------------
SLICES = {"A": "minutes 1996-2007 (point in time for 2008)",
          "B": "minutes 1996-2020 (the test years included)",
          "C": "minutes 1996-2007 and 2013-2020 (the future, but not the test years)"}
TEST = (20080101, 20121231)
LM_CFG = dict(vocab=2048, d=160, layers=4, heads=4, seq=256)
LM_TOKENS = 4_000_000


def _slice_docs(name):
    dm, tm, _ = _docs("minutes")
    held = set(dm[i] for i in range(len(dm)) if dm[i] < TEST[0] and i % 10 == 5)   # in-period validation, all models
    keep = []
    for d, t in zip(dm, tm):
        if d in held:
            continue
        if name == "A" and d < TEST[0]:
            keep.append(t)
        elif name == "B":
            keep.append(t)
        elif name == "C" and (d < TEST[0] or d > TEST[1]):
            keep.append(t)
    test = [t for d, t in zip(dm, tm) if TEST[0] <= d <= TEST[1]]
    val = [t for d, t in zip(dm, tm) if d in held]
    return keep, test, val


def _tokenizer(texts, vocab):
    from tokenizers import Tokenizer, decoders, models, pre_tokenizers, trainers
    tk = Tokenizer(models.BPE())
    tk.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
    tk.decoder = decoders.ByteLevel()
    tk.train_from_iterator(texts, trainers.BpeTrainer(vocab_size=vocab, initial_alphabet=pre_tokenizers.ByteLevel.alphabet(),
                                                       show_progress=False))
    return tk


def _ids(tk, texts):
    return np.concatenate([np.array(tk.encode(t + "\n").ids, np.int32) for t in texts])


def _train_slice(name: str) -> dict:
    import torch
    from explainer.lm import pocket as PK
    keep, test, val = _slice_docs(name)
    tk = _tokenizer(keep, LM_CFG["vocab"])
    tr, te = _ids(tk, keep), _ids(tk, test)
    run = PK.Run(model=PK.Config(**LM_CFG), lr=3e-3, batch=16, tokens=LM_TOKENS, seed=28, eval_every=40,
                 eval_batches=6)
    stream = PK.TokenStream(tr, te, LM_CFG["seq"], seed=28)
    path = CACHE.dir / f"lm_{name}"
    path.mkdir(parents=True, exist_ok=True)
    out = PK.train(run, stream, threads=1, ckpt=path / "ckpt.pt", ckpt_every=100)
    torch.save(out["_model"].state_dict(), path / "model.pt")
    tk.save(str(path / "tokenizer.json"))
    chars_te = sum(len(t) + 1 for t in test)
    return {"name": name, "desc": SLICES[name], "train_tokens": int(len(tr)), "train_chars": int(sum(len(t) + 1 for t in keep)),
            "test_tokens": int(len(te)), "test_chars": int(chars_te), "curve": out["curve"], "evals": out["evals"],
            "bpc_scale": float(len(te) / chars_te / math.log(2)), "seconds": out["seconds"], "params": out["counts"]}


def compute_lm() -> dict:
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=3) as ex:
        res = list(ex.map(_train_slice, ["A", "B", "C"]))
    return _json({"slices": {r["name"]: r for r in res}, "cfg": LM_CFG, "tokens": LM_TOKENS, "test": TEST})


PROBES = [("The Committee decided to keep the target range for the federal funds rate at 0 to", " 1/4 percent"),
          ("the Federal Reserve would purchase large quantities of agency mortgage-backed", " securities"),
          ("with the federal funds rate at its effective lower", " bound"),
          ("the Committee's forward", " guidance"),
          ("the Committee decided to increase its holdings of Treasury", " securities"),
          ("The Committee decided to lower its target for the federal funds rate", " by 25 basis points")]
PROMPTS = ["In light of the deterioration in financial conditions, the Committee",
           "Participants discussed the balance sheet and"]


def _load_lm(name):
    import torch
    from tokenizers import Tokenizer
    from explainer.lm import pocket as PK
    path = CACHE.dir / f"lm_{name}"
    m = PK.PocketGPT(PK.Config(**LM_CFG))
    m.load_state_dict(torch.load(path / "model.pt", weights_only=True))
    m.eval()
    return m, Tokenizer.from_file(str(path / "tokenizer.json"))


def _nll(model, ids, seq):
    """Total negative log-likelihood (nats) of a token sequence, in windows of ``seq`` with ``seq//2`` context."""
    import torch
    import torch.nn.functional as F
    ids = list(ids)
    tot, n = 0.0, 0
    with torch.no_grad():
        start = 0
        while start < len(ids) - 1:
            lo = max(0, start - seq // 2)
            chunk = ids[lo:start + seq // 2 + 1]
            x = torch.tensor([chunk[:-1]])
            y = torch.tensor([chunk[1:]])
            lp = F.log_softmax(model(x)[0], -1)
            nl = -lp[torch.arange(len(chunk) - 1), y[0]]
            k0 = start - lo
            tot += float(nl[k0:].sum())
            n += len(chunk) - 1 - k0
            start += seq // 2
    return tot, n


def _bpc(model, tk, texts):
    tot, chars = 0.0, 0
    for t in texts:
        ids = tk.encode(t).ids
        nl, _ = _nll(model, ids, LM_CFG["seq"])
        tot += nl
        chars += len(t)
    return tot / max(chars, 1) / math.log(2)


def _continuation(model, tk, prefix, cont):
    import torch
    import torch.nn.functional as F
    a = tk.encode(prefix).ids
    b = tk.encode(prefix + cont).ids
    if b[:len(a)] != a:
        a = b[:len(a)]
    with torch.no_grad():
        lp = F.log_softmax(model(torch.tensor([b[:-1]]))[0], -1)
    nl = -sum(float(lp[k - 1, b[k]]) for k in range(len(a), len(b)))
    top = torch.topk(lp[len(a) - 1], 5)
    return {"nats": nl, "prob": math.exp(-nl), "top": [[tk.decode([int(i)]), float(math.exp(v))] for v, i in zip(top.values, top.indices)]}


def _sample(model, tk, prompt, n=40, seed=0):
    import torch
    from explainer.lm import pocket as PK
    torch.manual_seed(seed)
    ids = PK.sample(model, tk.encode(prompt).ids, n, temperature=0.7, seed=seed, top_k=40)
    return tk.decode(list(ids))


def compute_lookahead() -> dict:
    import torch
    torch.set_num_threads(2)
    dm, tm, _ = _docs("minutes")
    ds, ts, _ = _docs("statement")
    _, test, val = _slice_docs("A")
    out = {"slices": SLICES, "test": TEST}
    for name in ("A", "B", "C"):
        m, tk = _load_lm(name)
        years = sorted(set(d // 10000 for d in ds))
        by_year = [_bpc(m, tk, [t for d, t in zip(ds, ts) if d // 10000 == y]) for y in years]
        out[name] = {"bpc_test": _bpc(m, tk, test), "bpc_val": _bpc(m, tk, val), "years": years,
                     "bpc_statements": by_year,
                     "probes": [dict(prefix=a, cont=b, **_continuation(m, tk, a, b)) for a, b in PROBES],
                     "samples": [_sample(m, tk, p_, 40, seed=k) for k, p_ in enumerate(PROMPTS)]}
    return _json(out)


# ---------------------------------------------------------------------------
# Research: SESTM's screening
# ---------------------------------------------------------------------------
def _sestm_world(rng, n, theta, s_len, V=1000, n_s=20, s_neutral=60):
    """Ke, Kelly and Xiu's model: n articles; 20 positive and 20 negative charged words; p ~ U(0,1); P(y > 0) =
    1/2 + theta (p - 1/2); s_len charged words per article, s_neutral neutral ones."""
    Op, On = np.zeros(V), np.zeros(V)
    Op[:n_s] = 1.0 / n_s                                # positive words: all of O+
    On[n_s:2 * n_s] = 1.0 / n_s                         # negative words: all of O-
    neutral = np.full(V, 1.0 / (V - 2 * n_s))
    neutral[:2 * n_s] = 0
    p = rng.random(n)
    y = np.where(rng.random(n) < 0.5 + theta * (p - 0.5), 1.0, -1.0)
    D = np.empty((n, V), np.int32)
    for i in range(n):
        D[i] = rng.multinomial(s_len, p[i] * Op + (1 - p[i]) * On) + rng.multinomial(s_neutral, neutral)
    return D, y, p, Op, On


def _f_limit(theta, s_len, O_j_pos, O_j_neg, grid=20001):
    """The population limit of f_j: E[g(p) q_j(p)] / E[q_j(p)], q_j(p) = P(word j appears | p)."""
    p = np.linspace(0, 1, grid)
    q = 1 - (1 - (p * O_j_pos + (1 - p) * O_j_neg)) ** s_len
    g = 0.5 + theta * (p - 0.5)
    return float(np.trapezoid(g * q, p) / np.trapezoid(q, p))


def compute_theory() -> dict:
    rng = np.random.default_rng(2828)
    n_s, V = 20, 1000
    out = {"V": V, "n_s": n_s}
    # population limits (theorem) for a positive, a negative and a neutral word
    lim = {}
    for theta in (0.2, 0.5, 1.0):
        for s_len in (5, 20):
            lim[f"{theta}_{s_len}"] = {"pos": _f_limit(theta, s_len, 1 / n_s, 0), "neg": _f_limit(theta, s_len, 0, 1 / n_s),
                                       "neutral": 0.5}
    out["limits"] = lim
    # simulated recovery by n
    ns = [100, 200, 500, 1000, 2000, 5000]
    rec = {}
    for theta in (0.2, 0.5, 1.0):
        for s_len in (5, 20):
            rows = []
            for n in ns:
                tp_, fd_, corr_ = [], [], []
                for rep in range(8):
                    D, y, p, Op, On = _sestm_world(rng, n, theta, s_len)
                    a = 1.0 * math.sqrt(math.log(V) / n)            # alpha shrinking like sqrt(log m / n)
                    sc = TX.sestm_screen(D, y, alpha=a, kappa=max(3, int(0.01 * n)))
                    S = set(sc["S"].tolist())
                    true = set(range(2 * n_s))
                    tp_.append(len(S & true) / len(true))
                    fd_.append(len(S - true) / max(len(S), 1))
                    if len(sc["pos"]) and len(sc["neg"]):
                        tpc = TX.sestm_topics(D[:, sc["S"]], y)
                        D2, y2, p2, _, _ = _sestm_world(rng, 400, theta, s_len)
                        s2 = [TX.sestm_score(d_, tpc["O_pos"], tpc["O_neg"]) for d_ in D2[:, sc["S"]]]
                        corr_.append(float(np.corrcoef(s2, p2)[0, 1]))
                rows.append({"n": n, "tpr": float(np.mean(tp_)), "fdr": float(np.mean(fd_)),
                             "corr": float(np.mean(corr_)) if corr_ else float("nan")})
            rec[f"{theta}_{s_len}"] = rows
    out["recovery"] = rec
    out["ns"] = ns
    # f_j at large n against the limits
    D, y, p, Op, On = _sestm_world(rng, 20000, 0.5, 5)
    sc = TX.sestm_screen(D, y, alpha=0.0, kappa=1)
    out["f_big"] = {"pos": float(np.mean(sc["f"][:n_s])), "neg": float(np.mean(sc["f"][n_s:2 * n_s])),
                    "neutral": float(np.mean(sc["f"][2 * n_s:])), "neutral_sd": float(np.std(sc["f"][2 * n_s:])),
                    "f_pos": sc["f"][:n_s], "f_neg": sc["f"][n_s:2 * n_s], "f_neutral": sc["f"][2 * n_s:2 * n_s + 200],
                    "limit": lim["0.5_5"], "pi": sc["pi"]}
    # the statements: does screening find more words than it would on shuffled labels?
    sm = load("sestm")
    ds, ts, toks = _docs("statement")
    g2, _ = _yields()
    yv = _reaction(ds, g2)
    dsa = np.array(ds)
    ok = np.isfinite(yv) & (yv != 0) & (dsa <= TRAIN_END)
    toks_tr = [toks[i] for i in np.flatnonzero(ok)]
    vocab = TX.vocabulary(toks_tr, min_df=3, stop=STOP)
    Dtr = TX.dtm(toks_tr, vocab)
    real = TX.sestm_screen(Dtr, yv[ok], alpha=sm["alpha"], kappa=sm["kappa"])
    null = []
    for r in range(500):
        yy = rng.permutation(yv[ok])
        null.append(len(TX.sestm_screen(Dtr, yy, alpha=sm["alpha"], kappa=sm["kappa"])["S"]))
    null = np.array(null)
    out["data"] = {"n": int(ok.sum()), "alpha": sm["alpha"], "kappa": sm["kappa"], "n_real": int(len(real["S"])),
                   "null_mean": float(null.mean()), "null_q95": float(np.quantile(null, 0.95)),
                   "p_perm": float(np.mean(null >= len(real["S"]))), "null_hist": np.bincount(null, minlength=60)[:60],
                   "n_needed": None, "rho_test": sm["rho"], "p_rho": sm["p_rho"], "n_test": sm["n_test"]}
    return _json(out)


# ---------------------------------------------------------------------------
# Alternative data: what happens to a signal as the data spreads (a model)
# ---------------------------------------------------------------------------
def compute_altdata() -> dict:
    """Kyle (1985) with N informed traders who share the same signal (Admati and Pfleiderer 1988's symmetric case):
    price impact lambda = sigma_v sqrt(N) / ((N + 1) sigma_u); total informed profit sqrt(N) sigma_u sigma_v / (N + 1);
    each trader's share 1/N of it; the price reveals N/(N + 1) of the signal's variance.  Checked by simulation, then
    run along a logistic adoption curve (a stylised data set bought by more funds each year)."""
    rng = np.random.default_rng(2814)
    sv, su = 1.0, 1.0
    Ns = np.arange(1, 41)
    lam = sv * np.sqrt(Ns) / ((Ns + 1) * su)
    total = np.sqrt(Ns) * su * sv / (Ns + 1)
    each = total / Ns
    reveal = Ns / (Ns + 1)
    sim = []
    for N in (1, 2, 5, 10, 20):
        v = rng.standard_normal(200000) * sv
        u = rng.standard_normal(200000) * su
        beta = su / (sv * math.sqrt(N))
        x = N * beta * v + u
        l_ = sv * math.sqrt(N) / ((N + 1) * su)
        p = l_ * x
        prof = (v - p) * beta * v
        sim.append({"N": N, "each": float(prof.mean()), "theory": float(su * sv / ((N + 1) * math.sqrt(N))),
                    "reveal": float(1 - np.var(v - p) / np.var(v)), "reveal_theory": N / (N + 1)})
    years = np.arange(2010, 2026)
    adopters = 1 + np.round(39 / (1 + np.exp(-(years - 2017) / 1.5))).astype(int)
    path = {"years": years, "N": adopters, "each": su * sv / ((adopters + 1) * np.sqrt(adopters)),
            "total": np.sqrt(adopters) * su * sv / (adopters + 1)}
    return _json({"Ns": Ns, "lam": lam, "total": total, "each": each, "reveal": reveal, "sim": sim, "path": path})


# ---------------------------------------------------------------------------
# The envelope: the statement score, registered and opened on 2021-2025
# ---------------------------------------------------------------------------
STRATEGY = "sestm_fomc_drift_part28"
DURATION = 1.9            # a 2-year note's modified duration, roughly: return = -1.9 x yield change


def compute_envelope() -> dict:
    import inspect
    from explainer.quant.house import track
    sm = load("sestm")
    ds_all, ts_all, toks_all = _docs("statement", through=20251231)
    g2, _ = _yields()
    dsa = np.array(ds_all)
    dy = _reaction(ds_all, g2)
    drift = _drift(ds_all, g2, h=5)
    code = inspect.getsource(_sestm_fit) + inspect.getsource(TX.sestm_screen) + inspect.getsource(TX.sestm_topics) + \
        inspect.getsource(TX.sestm_score) + inspect.getsource(_drift)
    n_trials = len(sm["cv"]) + 1
    pit.register(STRATEGY, code, {"train": "statements 1997-2020, statement-day 2-year change as the label",
                                  "alpha": sm["alpha"], "kappa": sm["kappa"], "trade": "after the statement-day close, "
                                  "short the 2-year note when the score is above 1/2 (yields expected to keep rising), "
                                  "long below; hold five trading days", "duration": DURATION}, trials=n_trials)
    # refit on everything to 2020, the registered rule
    ok = np.isfinite(dy) & (dy != 0) & (dsa <= RESEARCH_END)
    toks_tr = [toks_all[i] for i in np.flatnonzero(ok)]
    vocab = TX.vocabulary(toks_tr, min_df=3, stop=STOP)
    s, tp = _sestm_fit(toks_tr, dy[ok], vocab, sm["alpha"], sm["kappa"])
    D = TX.dtm(toks_all, vocab)[:, s["S"]]
    score = np.array([TX.sestm_score(d_, tp["O_pos"], tp["O_neg"]) for d_ in D])
    bond = np.where(score > 0.5, -1.0, 1.0)                # short the note when the statement reads hawkish
    pnl = bond * (-DURATION * drift / 10000)              # decimal return of the position over the five days
    # the hold-out: the 5-day drifts after the 2021-2025 statements
    fin = np.isfinite(drift)
    hd, hv = pit.open_envelope(STRATEGY, "fred/dgs2_fomc_5day_drift", dsa[fin], np.round(drift[fin], 6))
    res_m = fin & (dsa <= RESEARCH_END)
    hold_m = fin & (dsa > RESEARCH_END)

    def monthly(mask):
        ym = dsa[mask] // 100
        keys = np.unique(ym)
        return keys, np.array([pnl[mask][ym == k].sum() for k in keys])
    kr, mr = monthly(res_m)
    kh, mh = monthly(hold_m)
    cost = 8 * DURATION * 1.0 / 10000                     # about 1 bp of yield a round trip, eight statements a year
    row = track.record(STRATEGY, 28, mr, mh, cost, note="statement months only; flat in other months")
    hit_h = float(np.mean(pnl[hold_m] > 0)) if hold_m.any() else np.nan
    hit_r = float(np.mean(pnl[res_m] > 0))
    return _json({"trials": pit.trials_so_far(), "n_trials": n_trials, "row": row, "words": [vocab[j] for j in s["S"]],
                  "dates": dsa, "score": score, "drift": drift, "pnl": pnl, "dy": dy,
                  "n_research": int(res_m.sum()), "n_hold": int(hold_m.sum()),
                  "mean_hold_bp": float(np.mean(pnl[hold_m]) * 1e4) if hold_m.any() else np.nan,
                  "mean_research_bp": float(np.mean(pnl[res_m]) * 1e4),
                  "cum_hold": np.cumsum(pnl[hold_m]), "hold_dates": dsa[hold_m], "cum_research": np.cumsum(pnl[res_m]),
                  "research_dates": dsa[res_m], "first": int(dsa[hold_m][0]) if hold_m.any() else None,
                  "last": int(dsa[hold_m][-1]) if hold_m.any() else None, "hit_hold": hit_h,
                  "hit_research": hit_r, "cost": cost, "duration": DURATION})


ITEMS = {"corpus": compute_corpus, "hook": compute_hook, "tone": compute_tone, "form": compute_form,
         "sestm": compute_sestm, "topics": compute_topics, "phrases": compute_phrases, "embed": compute_embed,
         "lm": compute_lm, "lookahead": compute_lookahead, "theory": compute_theory,
         "altdata": compute_altdata, "envelope": compute_envelope}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
