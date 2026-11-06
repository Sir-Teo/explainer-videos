"""Text for search (Part 47): the thirty novels split into passages; a tokenizer with case folding; Porter's
stemmer (1980), written out rule by rule; stop words; and Zipf's and Heaps' laws fitted on the corpus."""

from __future__ import annotations

import math
import re
from collections import Counter

STOP = set("a an and are as at be but by for from had has have he her his i in is it its me my not of on or she "
           "so that the their them they this to was we were what which who will with would you your".split())


def corpus(words_per_doc=400):
    """Passages of about words_per_doc words from each novel: (doc id, book title, text)."""
    import videos.ai.ai1.compute as A
    from videos.cs.cs6.compute import novels
    books = novels()
    docs = []
    for bid, title in A.BOOKS.items():
        ws = books[bid].split()
        for k in range(0, len(ws), words_per_doc):
            docs.append((len(docs), title, " ".join(ws[k:k + words_per_doc])))
    return docs


TOKEN = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")


def tokens(text):
    return TOKEN.findall(text.lower())


# ---------------------------------------------------------------- Porter's stemmer

def _cons(w, i):
    c = w[i]
    if c in "aeiou":
        return False
    if c == "y":
        return i == 0 or not _cons(w, i - 1)
    return True


def _m(stem):
    """The measure: the number of vowel-consonant sequences [C](VC)^m[V]."""
    n, i, L = 0, 0, len(stem)
    while i < L and _cons(stem, i):
        i += 1
    while i < L:
        while i < L and not _cons(stem, i):
            i += 1
        if i >= L:
            break
        while i < L and _cons(stem, i):
            i += 1
        n += 1
    return n


def _has_vowel(stem):
    return any(not _cons(stem, i) for i in range(len(stem)))


def _double_c(w):
    return len(w) >= 2 and w[-1] == w[-2] and _cons(w, len(w) - 1)


def _cvc(w):
    return (len(w) >= 3 and _cons(w, len(w) - 1) and not _cons(w, len(w) - 2) and _cons(w, len(w) - 3)
            and w[-1] not in "wxy")


def _rep(w, rules, cond):
    for suf, rep in rules:
        if w.endswith(suf):
            stem = w[:len(w) - len(suf)]
            return stem + rep if cond(stem) else w
    return w


STEP2 = [("ational", "ate"), ("tional", "tion"), ("enci", "ence"), ("anci", "ance"), ("izer", "ize"),
         ("abli", "able"), ("alli", "al"), ("entli", "ent"), ("eli", "e"), ("ousli", "ous"), ("ization", "ize"),
         ("ation", "ate"), ("ator", "ate"), ("alism", "al"), ("iveness", "ive"), ("fulness", "ful"),
         ("ousness", "ous"), ("aliti", "al"), ("iviti", "ive"), ("biliti", "ble")]
STEP3 = [("icate", "ic"), ("ative", ""), ("alize", "al"), ("iciti", "ic"), ("ical", "ic"), ("ful", ""), ("ness", "")]
STEP4 = ["al", "ance", "ence", "er", "ic", "able", "ible", "ant", "ement", "ment", "ent", "ion", "ou", "ism", "ate",
         "iti", "ous", "ive", "ize"]


def porter(w: str) -> str:
    if len(w) <= 2:
        return w
    # step 1a
    if w.endswith("sses"):
        w = w[:-2]
    elif w.endswith("ies"):
        w = w[:-2]
    elif w.endswith("ss"):
        pass
    elif w.endswith("s"):
        w = w[:-1]
    # step 1b
    flag = False
    if w.endswith("eed"):
        if _m(w[:-3]) > 0:
            w = w[:-1]
    elif w.endswith("ed") and _has_vowel(w[:-2]):
        w, flag = w[:-2], True
    elif w.endswith("ing") and _has_vowel(w[:-3]):
        w, flag = w[:-3], True
    if flag:
        if w.endswith(("at", "bl", "iz")):
            w += "e"
        elif _double_c(w) and w[-1] not in "lsz":
            w = w[:-1]
        elif _m(w) == 1 and _cvc(w):
            w += "e"
    # step 1c
    if w.endswith("y") and _has_vowel(w[:-1]):
        w = w[:-1] + "i"
    # steps 2 and 3
    w = _rep(w, STEP2, lambda s: _m(s) > 0)
    w = _rep(w, STEP3, lambda s: _m(s) > 0)
    # step 4
    for suf in STEP4:
        if w.endswith(suf):
            stem = w[:len(w) - len(suf)]
            if _m(stem) > 1 and (suf != "ion" or stem.endswith(("s", "t"))):
                w = stem
            break
    # step 5
    if w.endswith("e"):
        stem = w[:-1]
        if _m(stem) > 1 or (_m(stem) == 1 and not _cvc(stem)):
            w = stem
    if _m(w) > 1 and _double_c(w) and w.endswith("l"):
        w = w[:-1]
    return w


PORTER_EXAMPLES = {"caresses": "caress", "ponies": "poni", "cats": "cat", "feed": "feed", "agreed": "agre",
                   "plastered": "plaster", "motoring": "motor", "sing": "sing", "conflated": "conflat",
                   "hopping": "hop", "filing": "file", "happy": "happi", "relational": "relat",
                   "conditional": "condit", "generalization": "gener", "electrical": "electr", "adjustment": "adjust",
                   "probate": "probat", "controlling": "control", "roll": "roll"}
"""Examples and the outputs given in Porter (1980) and its reference implementation."""


def check_porter():
    return {w: (porter(w), want, porter(w) == want) for w, want in PORTER_EXAMPLES.items()}


# ---------------------------------------------------------------- Zipf and Heaps

def zipf_heaps(words, sample_every=20_000):
    c = Counter(words)
    ranked = c.most_common()
    xs = [math.log10(r + 1) for r in range(len(ranked))]
    ys = [math.log10(f) for _, f in ranked]
    sel = [i for i in range(len(xs)) if 10 <= i + 1 <= 10_000]
    n = len(sel)
    mx = sum(xs[i] for i in sel) / n
    my = sum(ys[i] for i in sel) / n
    slope = sum((xs[i] - mx) * (ys[i] - my) for i in sel) / sum((xs[i] - mx) ** 2 for i in sel)
    seen, growth = set(), []
    for k, w in enumerate(words, 1):
        seen.add(w)
        if k % sample_every == 0:
            growth.append((k, len(seen)))
    lx = [math.log10(a) for a, _ in growth]
    ly = [math.log10(b) for _, b in growth]
    mx2, my2 = sum(lx) / len(lx), sum(ly) / len(ly)
    beta = sum((a - mx2) * (b - my2) for a, b in zip(lx, ly)) / sum((a - mx2) ** 2 for a in lx)
    K = 10 ** (my2 - beta * mx2)
    return {"tokens": len(words), "types": len(c), "top": ranked[:20], "zipf_slope": slope,
            "rank_freq": [(r + 1, ranked[r][1]) for r in (0, 1, 2, 4, 9, 19, 49, 99, 199, 499, 999, 1999, 4999, 9999,
                                                         19999) if r < len(ranked)],
            "heaps": growth[::max(1, len(growth) // 40)], "heaps_beta": beta, "heaps_K": K,
            "hapax": sum(1 for _, f in ranked if f == 1)}
