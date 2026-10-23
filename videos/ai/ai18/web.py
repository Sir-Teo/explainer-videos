"""Part 18's data pipeline in miniature, on real web pages: a sample of Common Crawl's September 2026 crawl, the
fastText language identifier FineWeb uses, Trafilatura's text extraction, MinHash with locality-sensitive hashing,
and a small quality classifier trained on FineWeb-Edu's own annotations.

Everything downloaded is fixed (Common Crawl's files never change; byte ranges and dataset offsets are fixed), cached
in ``.cache/ai18/crawl/``, and fetched with ``curl`` (as Part 1 fetches its books), so a rerun reads the same pages.
"""

from __future__ import annotations

import io
import json
import re
import subprocess
import time
import zlib
from pathlib import Path

import numpy as np

from explainer.tts import REPO_ROOT

DIR = REPO_ROOT / ".cache" / "ai18" / "crawl"
CC = "https://data.commoncrawl.org/"
CRAWL = "CC-MAIN-2026-39"  # September 2026
WET_FILES = (0, 33_333, 66_666)  # positions in the crawl's list of 100,000 WET files
WET_CHUNKS = 3  # byte ranges per file, spread through it
CHUNK = 3 * 2 ** 20
WARC_CHUNKS = 4
LID_URL = "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz"
EDU = "HuggingFaceFW/fineweb-edu-llama3-annotations"
EDU_ROWS = 467_424
EDU_PAGES = 150  # requests of 100 rows, spread through the dataset

# A small URL keyword filter in the spirit of FineWeb's (which uses the UT1 blocklist); pages that match are dropped
# before anything else, and nothing they contain is ever shown.
BLOCK = ("porn", "xxx", "sex", "nude", "escort", "hentai", "adult", "camgirl", "milf", "fetish", "erotic", "casino",
         "gambl", "betting", "viagra", "onlyfans", "nsfw", "dating", "hookup", "bdsm", "xvideo", "jav")


def curl(url: str, dst: Path, byte_range: str | None = None) -> Path:
    if dst.exists() and dst.stat().st_size > 0:
        return dst
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["curl", "-sS", "-L", "--retry", "5", "--retry-all-errors", "-m", "600", "-o", str(dst) + ".part"]
    if byte_range:
        cmd += ["-r", byte_range]
    for attempt in range(5):
        if subprocess.run(cmd + [url]).returncode == 0:
            break
        time.sleep(2 ** (attempt + 1))
    else:
        raise RuntimeError(f"could not download {url}")
    Path(str(dst) + ".part").replace(dst)
    return dst


def size_of(url: str) -> int:
    out = subprocess.run(["curl", "-sSI", "-L", "-m", "60", url], capture_output=True, text=True).stdout
    sizes = re.findall(r"(?im)^content-length:\s*(\d+)", out)
    return int(sizes[-1])


def wet_paths() -> list[str]:
    import gzip

    p = curl(CC + f"crawl-data/{CRAWL}/wet.paths.gz", DIR / "wet.paths.gz")
    return gzip.decompress(p.read_bytes()).decode().split()


def _records(blob: bytes, kind: str):
    """WARC records of one type from a byte range of a .warc.gz: each record is its own gzip member, so start at
    the first member that decompresses to a WARC header, and stop at the range's truncated last member."""
    from warcio.archiveiterator import ArchiveIterator

    i = 0
    while True:
        i = blob.find(b"\x1f\x8b\x08", i)
        if i < 0:
            return
        try:
            head = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(blob[i:i + 4096])
        except zlib.error:
            head = b""
        if head.startswith(b"WARC/1."):
            break
        i += 1
    try:
        for rec in ArchiveIterator(io.BytesIO(blob[i:])):
            if rec.rec_type == kind:
                yield rec
    except Exception:  # the range ends inside a record
        return


def wet_pages() -> list[dict]:
    """Every page in our byte ranges of three WET files: url, text, and Common Crawl's own language tag."""
    paths = wet_paths()
    pages = []
    for k in WET_FILES:
        url = CC + paths[k]
        n = size_of(url)
        for j in range(WET_CHUNKS):
            a = int(n * (j + 0.5) / (WET_CHUNKS + 0.5))
            f = curl(url, DIR / f"wet{k}_{j}.gz", f"{a}-{a + CHUNK - 1}")
            for rec in _records(f.read_bytes(), "conversion"):
                text = rec.content_stream().read().decode("utf-8", "replace")
                pages.append(dict(url=rec.rec_headers.get_header("WARC-Target-URI") or "", text=text,
                                  cc_lang=rec.rec_headers.get_header("WARC-Identified-Content-Language") or "",
                                  file=k))
    return pages


def warc_pages() -> list[dict]:
    """HTML responses in byte ranges of the first WARC file, with Trafilatura's extraction of each."""
    import logging

    import trafilatura

    logging.getLogger("trafilatura").setLevel(logging.CRITICAL)
    paths = wet_paths()
    url = CC + paths[WET_FILES[0]].replace("/wet/", "/warc/").replace(".warc.wet.gz", ".warc.gz")
    n = size_of(url)
    out = []
    for j in range(WARC_CHUNKS):
        a = int(n * (j + 0.5) / (WARC_CHUNKS + 0.5))
        f = curl(url, DIR / f"warc_{j}.gz", f"{a}-{a + 2 * CHUNK - 1}")
        for rec in _records(f.read_bytes(), "response"):
            ctype = (rec.http_headers.get_header("Content-Type") or "") if rec.http_headers else ""
            if "html" not in ctype.lower():
                continue
            body = rec.content_stream().read()
            u = rec.rec_headers.get_header("WARC-Target-URI") or ""
            try:
                html = body.decode("utf-8", "replace")
                text = trafilatura.extract(html, include_comments=False) or ""
            except Exception:
                text = ""
            out.append(dict(url=u, html_bytes=len(body), text_bytes=len(text.encode()), text=text[:2000]))
    return out


def blocked(url: str) -> bool:
    u = url.lower()
    return any(w in u for w in BLOCK)


# ---------------------------------------------------------------------------
# Language identification
# ---------------------------------------------------------------------------
def lid_model():
    import fasttext

    p = curl(LID_URL, DIR.parent / "lid.176.ftz")
    fasttext.FastText.eprint = lambda *a, **k: None  # silence the deprecation banner
    return fasttext.load_model(str(p))


def identify(model, text: str) -> tuple[str, float]:
    labels, probs = model.predict(" ".join(text.split())[:4000], k=1)
    return labels[0].replace("__label__", ""), float(probs[0])


# ---------------------------------------------------------------------------
# MinHash and locality-sensitive hashing (FineWeb's settings: word 5-grams, 112 hashes, 14 bands of 8)
# ---------------------------------------------------------------------------
P = 4294967311  # a prime just above 2^32: h(x) = (a x + b) mod P fits in 64 bits for 32-bit x, a, b
WORD = re.compile(r"\w+", re.U)


def words(text: str) -> list[str]:
    return WORD.findall(text.lower())


def shingles(ws: list[str], n: int = 5) -> np.ndarray:
    """The set of a document's word n-grams, each as a 32-bit hash (CRC-32 of its text)."""
    if len(ws) < n:
        grams = {" ".join(ws)}
    else:
        grams = {" ".join(ws[i:i + n]) for i in range(len(ws) - n + 1)}
    return np.unique(np.fromiter((zlib.crc32(g.encode()) for g in grams), np.uint64, len(grams)))


def hash_family(k: int = 112, seed: int = 18):
    g = np.random.default_rng(seed)
    return (g.integers(1, 2 ** 32, k, dtype=np.uint64), g.integers(0, 2 ** 32, k, dtype=np.uint64))


def minhash(sh: np.ndarray, fam) -> np.ndarray:
    a, b = fam
    out = np.empty(len(a), np.uint64)
    for s in range(0, len(sh), 4096):
        h = (a[:, None] * sh[None, s:s + 4096] + b[:, None]) % np.uint64(P)
        m = h.min(1)
        out = m if s == 0 else np.minimum(out, m)
    return out


def jaccard(a: np.ndarray, b: np.ndarray) -> float:
    inter = len(np.intersect1d(a, b, assume_unique=True))
    return inter / (len(a) + len(b) - inter) if len(a) + len(b) else 1.0


def lsh_collide(s1: np.ndarray, s2: np.ndarray, bands: int = 14, rows: int = 8) -> bool:
    return bool((s1[:bands * rows].reshape(bands, rows) == s2[:bands * rows].reshape(bands, rows)).all(1).any())


def p_collide(s, bands: int = 14, rows: int = 8):
    return 1 - (1 - np.asarray(s, float) ** rows) ** bands


def lsh_pairs(sigs: list, bands: int = 14, rows: int = 8) -> set:
    """Candidate pairs: documents whose signatures agree on all the rows of at least one band."""
    cand = set()
    for bnd in range(bands):
        buckets = {}
        for i, s in enumerate(sigs):
            buckets.setdefault(s[bnd * rows:(bnd + 1) * rows].tobytes(), []).append(i)
        for ids in buckets.values():
            if 1 < len(ids) < 200:
                for x in range(len(ids)):
                    for y in range(x + 1, len(ids)):
                        cand.add((ids[x], ids[y]))
    return cand


# ---------------------------------------------------------------------------
# FineWeb-Edu's annotations
# ---------------------------------------------------------------------------
def edu_annotations() -> list[dict]:
    """Llama-3-70B-Instruct's 0-5 educational scores for web pages (FineWeb-Edu's training set), 100 rows at a time
    from evenly spaced offsets of the dataset (Hugging Face's dataset viewer API)."""
    path = DIR / "edu_annotations.jsonl"
    if path.exists():
        return [json.loads(x) for x in path.read_text().split("\n")]
    rows = []
    for k in range(EDU_PAGES):
        off = int(k * (EDU_ROWS - 100) / (EDU_PAGES - 1))
        f = DIR / f"edu_{off}.json"
        curl(f"https://datasets-server.huggingface.co/rows?dataset={EDU}&config=default&split=train&offset={off}"
             f"&length=100", f)
        for r in json.loads(f.read_text())["rows"]:
            row = r["row"]
            rows.append(dict(text=row["text"][:6000], score=int(row["score"]), url=row["metadata"]["url"]))
        f.unlink()
    tmp = path.with_suffix(".tmp")
    tmp.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows))
    tmp.replace(path)
    return rows


def ft_line(text: str) -> str:
    return " ".join(words(text)[:1500])
