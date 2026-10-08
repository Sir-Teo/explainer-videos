"""A miniature FineWeb: real Common Crawl files through the real FineWeb filters.

The filters are Hugging Face's own implementations from ``datatrove`` (the
library that built FineWeb), configured as in ``datatrove/examples/fineweb.py``:

    URL blocklist -> Trafilatura text extraction -> fastText language ID (English, > 0.65)
    -> Gopher repetition -> Gopher quality -> C4 line rules -> FineWeb rules -> MinHash dedup

Two inputs:

* ``funnel(warc)``: raw HTML responses from the first part of one WARC file,
  run through the *whole* FineWeb recipe (incl. Trafilatura), keeping per-stage
  counts, bytes, rejection reasons and a few examples for the video.
* ``corpus(wet_files)``: Common Crawl's own text extraction (WET) of whole files,
  filtered from the URL stage onward, to build a training corpus quickly.

MinHash deduplication follows FineWeb's parameters (5-gram word shingles,
14 bands x 8 hashes = 112 hash functions) in a small NumPy implementation that
also exposes signatures and buckets so the video can show them.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from collections import Counter, defaultdict

import numpy as np

STAGES = [  # (key, on-screen name)
    ("url", "URL blocklist"),
    ("extract", "text extraction"),
    ("lang", "English"),
    ("gopher_rep", "repetition"),
    ("gopher_qual", "quality rules"),
    ("c4", "C4 line rules"),
    ("fineweb", "FineWeb rules"),
]


def _filters():
    from datatrove.pipeline.filters import (
        C4QualityFilter,
        FineWebQualityFilter,
        GopherQualityFilter,
        GopherRepetitionFilter,
        LanguageFilter,
        URLFilter,
    )

    return {
        "url": URLFilter(),
        "lang": LanguageFilter(languages=["en"]),
        "gopher_rep": GopherRepetitionFilter(),
        "gopher_qual": GopherQualityFilter(),
        "c4": C4QualityFilter(filter_no_terminal_punct=False),
        "fineweb": FineWebQualityFilter(),
    }


def _apply(f, doc) -> tuple[bool, str]:
    res = f.filter(doc)
    if isinstance(res, tuple):
        return bool(res[0]), res[1]
    return bool(res), "" if res else type(f).__name__


def read_docs(folder: str, pattern: str, limit: int = -1):
    """All records of a WARC/WET file; a file cut short (a byte-range download) ends at its last whole record."""
    return list(_iter_docs(folder, pattern, limit))


def _extract_one(html: str) -> str:
    from datatrove.pipeline.extractors import Trafilatura

    global _EXTRACTOR
    try:
        _EXTRACTOR
    except NameError:
        _EXTRACTOR = Trafilatura(favour_precision=True, timeout=1.0)
    try:
        return _EXTRACTOR.extract(html) or ""
    except Exception:
        return ""


def _iter_docs(folder: str, pattern: str, limit: int = -1):
    from datatrove.pipeline.readers import WarcReader

    it = iter(WarcReader(folder, glob_pattern=pattern, limit=limit).run())
    while True:
        try:
            yield next(it)
        except (StopIteration, EOFError):
            return


def funnel(folder: str, pattern: str, limit: int = -1, workers: int = 4, keep_examples: int = 24,
           keep_html: int = 400, chunk: int = 256) -> dict:
    """Run the full FineWeb recipe on raw-HTML WARC responses, streaming (the HTML of a 400 MB slice is
    several GB as Python strings); return per-stage counts, bytes, reasons and a few examples."""
    from multiprocessing import Pool

    F = _filters()
    keys = [k for k, _ in STAGES]
    counts = {k: 0 for k in ["input"] + keys}  # documents surviving each stage
    nbytes = {k: 0 for k in ["input"] + keys}
    reasons: dict[str, Counter] = {k: Counter() for k in keys}
    langs = Counter()
    examples: dict[str, list] = {k: [] for k in keys}
    seen_removed = Counter()
    rng = np.random.default_rng(0)
    kept = []

    def remove(key, d, why, text=None):
        reasons[key][why] += 1
        seen_removed[key] += 1
        item = dict(url=d.metadata.get("url", ""), text=(text if text is not None else d.text)[:700], reason=why)
        ex = examples[key]
        if len(ex) < keep_examples:  # reservoir sample
            ex.append(item)
        else:
            j = rng.integers(0, seen_removed[key])
            if j < keep_examples:
                ex[j] = item

    def flush(batch, pool):
        texts = pool.map(_extract_one, [d.text for d in batch], chunksize=8)
        for d, t in zip(batch, texts):
            html = d.text
            if not t.strip():
                remove("extract", d, "no_text", html)
                continue
            d.metadata["html_bytes"] = len(html.encode("utf-8", "ignore"))
            d.text = t
            counts["extract"] += 1
            nbytes["extract"] += len(t.encode("utf-8", "ignore"))
            alive = True
            for key in keys[2:]:
                ok, why = _apply(F[key], d)
                if key == "lang":
                    langs[d.metadata.get("language", "?")] += 1
                if not ok:
                    remove(key, d, why)
                    alive = False
                    break
                counts[key] += 1
                nbytes[key] += len(d.text.encode("utf-8", "ignore"))
            if alive:
                item = dict(url=d.metadata.get("url", ""), text=d.text, html_bytes=d.metadata["html_bytes"])
                if len(kept) < keep_html:
                    item["html"] = html
                kept.append(item)

    with Pool(workers) as pool:
        batch = []
        for d in _iter_docs(folder, pattern, limit):
            counts["input"] += 1
            nbytes["input"] += len(d.text.encode("utf-8", "ignore"))
            ok, why = _apply(F["url"], d)
            if not ok:
                remove("url", d, why)
                continue
            counts["url"] += 1
            nbytes["url"] += len(d.text.encode("utf-8", "ignore"))
            batch.append(d)
            if len(batch) >= chunk:
                flush(batch, pool)
                batch = []
        if batch:
            flush(batch, pool)

    stats = {k: dict(docs=counts[k], bytes=nbytes[k]) for k in counts}
    return dict(stats=stats, reasons={k: dict(v) for k, v in reasons.items()},
                languages=dict(langs.most_common(30)), examples=examples, kept=kept)


def filter_wet(folder: str, pattern: str, limit: int = -1) -> tuple[list[dict], dict]:
    """Common Crawl's WET text through the same filters (URL onward, no extraction)."""
    F = _filters()
    counts = Counter()
    out = []
    for d in _iter_docs(folder, pattern, limit):
        counts["input"] += 1
        ok = True
        for key in ["url", "lang", "gopher_rep", "gopher_qual", "c4", "fineweb"]:
            ok, _ = _apply(F[key], d)
            if not ok:
                break
            counts[key] += 1
        if ok:
            out.append(dict(url=d.metadata.get("url", ""), text=d.text))
    return out, dict(counts)


# ---------------------------------------------------------------------------
# MinHash LSH (FineWeb parameters: 5-grams, 14 buckets x 8 hashes)
# ---------------------------------------------------------------------------
N_GRAMS = 5
BANDS, ROWS = 14, 8
_MERSENNE = (1 << 61) - 1


def simplify(text: str) -> str:
    """Lowercase, strip accents and punctuation, collapse whitespace (like datatrove's simplify_text)."""
    text = unicodedata.normalize("NFD", text.lower())
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"[^\w\s]", " ", text)
    return " ".join(text.split())


def shingles(text: str, n: int = N_GRAMS) -> list[str]:
    w = simplify(text).split()
    return [" ".join(w[i:i + n]) for i in range(max(1, len(w) - n + 1))]


def _hash64(s: str) -> int:
    return int.from_bytes(hashlib.sha1(s.encode()).digest()[:8], "little") & _MERSENNE


def hash_params(k: int = BANDS * ROWS, seed: int = 1) -> np.ndarray:
    """One random 64-bit seed per hash function."""
    return np.random.default_rng(seed).integers(0, 2**63, k, dtype=np.uint64)


def _mix(z: np.ndarray) -> np.ndarray:
    """SplitMix64 finalizer: a fast, well-mixing bijection on 64-bit integers (wraps mod 2^64 on purpose)."""
    with np.errstate(over="ignore"):
        z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
        z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
        return z ^ (z >> np.uint64(31))


def signature(text: str, params=None) -> np.ndarray:
    """112 min-hashes: for each hash function h_i(x) = mix(x XOR seed_i), the minimum over the page's shingles.
    Two pages agree on a min-hash with probability equal to their Jaccard similarity."""
    seeds = hash_params() if params is None else params
    hs = np.array(sorted({_hash64(s) for s in shingles(text)}), dtype=np.uint64)
    return _mix(hs[None, :] ^ seeds[:, None]).min(axis=1)


def jaccard(t1: str, t2: str) -> float:
    a, b = set(shingles(t1)), set(shingles(t2))
    return len(a & b) / max(1, len(a | b))


def p_candidate(s, bands: int = BANDS, rows: int = ROWS):
    """Probability two documents with Jaccard similarity s share at least one bucket."""
    s = np.asarray(s, dtype=float)
    return 1 - (1 - s**rows) ** bands


def dedup(docs: list[dict], params=None) -> dict:
    """Cluster near-duplicates (any shared band -> same cluster) and keep one per cluster."""
    params = params or hash_params()
    sigs = np.stack([signature(d["text"], params) for d in docs])
    parent = list(range(len(docs)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for band in range(BANDS):
        buckets = defaultdict(list)
        block = sigs[:, band * ROWS:(band + 1) * ROWS]
        for i, row in enumerate(block):
            buckets[row.tobytes()].append(i)
        for members in buckets.values():
            for j in members[1:]:
                ri, rj = find(members[0]), find(j)
                if ri != rj:
                    parent[rj] = ri
    clusters = defaultdict(list)
    for i in range(len(docs)):
        clusters[find(i)].append(i)
    keep = sorted(min(m) for m in clusters.values())
    sizes = sorted((len(m) for m in clusters.values()), reverse=True)
    big = sorted(clusters.values(), key=len, reverse=True)[:12]
    return dict(keep=keep, sizes=sizes, big=[sorted(m) for m in big], n_in=len(docs), n_out=len(keep))
