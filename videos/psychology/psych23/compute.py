"""Precompute every number in Part 23 of *Psychology, Built* ("Language").

    python -m videos.psychology.psych23.compute            # everything missing (a few minutes; fetches data once)
    python -m videos.psychology.psych23.compute --force surprisal

Results are cached in ``.cache/psych23/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The models are
Psyche's (``explainer.psychology.psyche.language``).  The text the language model learns from is the reading of *AI,
Built* Part 1 (thirty Project Gutenberg novels, built by ``videos.ai.ai1.compute``); the reading times are the Natural
Stories corpus's (Futrell et al. 2021), fetched by ``explainer.psychology.opendata``.  Simulations use fixed seeds.

Items:
    zipf         Zipf's law in the thirty novels, and in Miller's randomly typing monkey
    lexicon      word frequency and length against reading time in Natural Stories; cohorts of a few words
    ia           the interactive activation model: a letter's activation in a word, alone and in a non-word, and
                 two-alternative accuracy against display time
    garden       a trigram model's surprisal, word by word, for garden-path sentences
    surprisal    surprisal of every word of Natural Stories, and reading time regressed on it
    stream       a syllable stream, its transitional probabilities, segmentation, and learning against exposure
    pasttense    the past-tense learner's U-shaped curve
    readability  Flesch's reading ease for two Natural Stories stories and a chapter of The Maltese Falcon
"""

from __future__ import annotations

import re
from collections import Counter
from functools import lru_cache

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology import opendata
from explainer.psychology.psyche import language as LG

CACHE = Cache("psych23")
load = CACHE.load


@lru_cache(maxsize=None)
def novels_tokens() -> list:
    from explainer.tts import REPO_ROOT

    p = REPO_ROOT / ".cache" / "ai1" / "train.txt"
    if not p.exists():
        from videos.ai.ai1 import compute as ai1

        ai1._save("corpus", ai1.compute_corpus())
    return LG.tokenize(p.read_text())


@lru_cache(maxsize=None)
def lm():
    return LG.KneserNey(novels_tokens(), d=0.75, vocab_size=30000)


def compute_zipf() -> dict:
    C = Counter(novels_tokens())
    z = LG.zipf_fit(C, top=10000)
    m = LG.random_typing(rng=np.random.default_rng(1957))
    zm = LG.zipf_fit(m, top=2000)
    pick = np.unique(np.geomspace(1, 10000, 120).astype(int)) - 1
    pickm = np.unique(np.geomspace(1, 2000, 120).astype(int)) - 1
    return {"s": z["s"], "logC": z["logC"], "r2": z["r2"], "rank": z["rank"][pick], "freq": z["freq"][pick],
            "types": len(C), "tokens": len(novels_tokens()), "top": np.array([w for w, _ in C.most_common(10)]),
            "top_n": np.array([n for _, n in C.most_common(10)]),
            "m_s": zm["s"], "m_logC": zm["logC"], "m_r2": zm["r2"], "m_rank": zm["rank"][pickm],
            "m_freq": zm["freq"][pickm]}


def _ns_words():
    ns = opendata.natural_stories()
    words = [re.sub(r"[^a-z']", "", w.lower()).strip("'") or "x" for w in ns["word"]]
    return ns, words


def compute_surprisal() -> dict:
    ns, words = _ns_words()
    model = lm()
    surp = np.zeros(len(words))
    for st in np.unique(ns["story"]):
        idx = np.where(ns["story"] == st)[0]
        surp[idx] = model.surprisal([words[i] for i in idx])
    C = Counter(novels_tokens())
    logf = np.log10(np.array([C.get(w, 0) + 1 for w in words], float))
    length = np.array([len(w) for w in words], float)
    prev = np.r_[np.nan, surp[:-1]]
    prev[np.r_[True, ns["story"][1:] != ns["story"][:-1]]] = np.nan
    ok = ~np.isnan(prev)
    rt = ns["rt"]
    reg = LG.rt_regression(rt[ok], surp[ok], length[ok], logf[ok], prev[ok])
    edges = np.quantile(surp, np.linspace(0, 1, 11))
    mid, mean_rt, mean_next = [], [], []
    nxt = np.r_[rt[1:], np.nan]
    nxt[np.r_[ns["story"][1:] != ns["story"][:-1], True]] = np.nan
    for a, b in zip(edges[:-1], edges[1:]):
        m = (surp >= a) & (surp <= b)
        mid.append(np.median(surp[m]))
        mean_rt.append(rt[m].mean())
        mean_next.append(np.nanmean(nxt[m]))
    # an example sentence: the first of story 1
    first = np.where(ns["story"] == 1)[0][:14]
    return {"surprisal": surp, "rt": rt, "logf": logf, "length": length, "coef": reg["coef"], "se": reg["se"],
            "names": np.array(reg["names"]), "r2": reg["r2"], "n_words": len(words), "n_stories": len(np.unique(ns["story"])),
            "readers_median": float(np.median(ns["n"])), "bin_mid": np.array(mid), "bin_rt": np.array(mean_rt),
            "bin_next": np.array(mean_next), "mean_surprisal": float(surp.mean()),
            "perplexity": float(2 ** surp.mean()), "ex_words": ns["word"][first], "ex_surprisal": surp[first],
            "ex_rt": rt[first]}


def compute_lexicon() -> dict:
    d = load("surprisal")
    out = {}
    edges = np.quantile(d["logf"], np.linspace(0, 1, 9))
    mid, rt = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        m = (d["logf"] >= a) & (d["logf"] <= b)
        mid.append(np.median(d["logf"][m]))
        rt.append(d["rt"][m].mean())
    out["freq_mid"], out["freq_rt"] = np.array(mid), np.array(rt)
    lens = np.arange(1, 13)
    out["len"] = lens
    out["len_rt"] = np.array([d["rt"][d["length"] == L].mean() if (d["length"] == L).sum() > 20 else np.nan
                              for L in lens])
    C = Counter(novels_tokens())
    lex = [w for w, n in C.items() if n >= 3]
    for w in ("elephant", "candle", "trespass"):
        out["cohort_" + w] = np.array(LG.cohort(w, lex))
    out["lexicon_size"] = len(lex)
    return out


def _ia_model():
    C = Counter(novels_tokens())
    four = [w for w, _ in C.most_common(30000) if len(w) == 4 and w.isalpha()][:1500]
    return LG.InteractiveActivation(four, [C[w] for w in four]), four


def compute_ia() -> dict:
    m, four = _ia_model()
    K = LG.LETTERS.index("K")
    out = {"lexicon": len(four)}
    for name, disp in (("word", list("WORK")), ("alone", [None, None, None, "K"]), ("nonword", list("OWRK"))):
        L, W = m.run(disp, 40, mask_at=12)
        out[name + "_K"] = L[:, 3, K]
        out[name + "_D"] = L[:, 3, LG.LETTERS.index("D")]
        if name == "word":
            out["word_WORK"] = W[:, m.words.index("WORK")]
            out["word_WORD"] = W[:, m.words.index("WORD")]
    durs = np.arange(4, 17)
    for name, disp in (("word", list("WORK")), ("alone", [None, None, None, "K"]), ("nonword", list("OWRK"))):
        out["acc_" + name] = np.array([m.forced_choice(disp, 3, "K", "D", mask_at=int(t)) for t in durs])
    out["durations"] = durs
    return out


GARDEN = ("the horse raced past the barn fell", "the horse that was raced past the barn fell",
          "the old man the boats")


def compute_garden() -> dict:
    model = lm()
    out = {}
    for k, s in enumerate(GARDEN):
        out[f"words_{k}"] = np.array(s.split())
        out[f"surp_{k}"] = model.surprisal(s.split())
    return out


def compute_stream() -> dict:
    st = LG.syllable_stream(n=180, rng=np.random.default_rng(1996))
    tp = LG.transitional_probabilities(st)
    p = np.array([tp[(a, b)] for a, b in zip(st[:-1], st[1:])])
    words = set(LG.SAFFRAN_WORDS)
    exposure = np.array([4, 8, 12, 20, 30, 45, 60, 90, 180])
    correct = []
    for n in exposure:
        sub = st[:3 * n]
        seg = LG.segment(sub, LG.transitional_probabilities(sub))
        correct.append(np.mean([w in words for w in seg]))
    tests = {"words": ["tupiro", "golabu"], "partwords": ["pirogo", "labubi"]}
    return {"syllables": np.array(st[:36]), "tp": p[:35], "segments": np.array(LG.segment(st)[:12]),
            "word_scores": np.array([LG.word_score(w, tp) for w in tests["words"]]),
            "part_scores": np.array([LG.word_score(w, tp) for w in tests["partwords"]]),
            "exposure": exposure, "correct": np.array(correct), "n_syllables": len(st)}


def compute_pasttense() -> dict:
    irr = list(LG.IRREGULAR)
    reg = list(LG.REGULAR)
    early = irr[:10] + reg[:2]
    flood = irr[:10] + reg
    r = LG.past_tense_learner([early, flood], epochs_per_stage=20, lr=0.3, l2=1e-3, rng=np.random.default_rng(1986))
    return {"over": r["over"], "right": r["right"], "stage": r["stage"], "early": np.array(irr[:10]),
            "n_regular": len(reg), "n_irregular": len(irr)}


def compute_readability() -> dict:
    ns = opendata.natural_stories()
    out = {}
    for st in (1, 5):
        text = " ".join(str(w) for w, s_ in zip(ns["word"], ns["story"]) if s_ == st)
        f = LG.flesch(text)
        out[f"story{st}"] = f["score"]
        out[f"story{st}_wps"] = f["words_per_sentence"]
        out[f"story{st}_spw"] = f["syllables_per_word"]
    from explainer.tts import REPO_ROOT

    passage = (REPO_ROOT / ".cache" / "ai1" / "passage.txt").read_text()[:6000]
    f = LG.flesch(passage)
    out["falcon"], out["falcon_wps"], out["falcon_spw"] = f["score"], f["words_per_sentence"], f["syllables_per_word"]
    return out


ITEMS = {
    "zipf": compute_zipf,
    "surprisal": compute_surprisal,
    "lexicon": compute_lexicon,
    "ia": compute_ia,
    "garden": compute_garden,
    "stream": compute_stream,
    "pasttense": compute_pasttense,
    "readability": compute_readability,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
