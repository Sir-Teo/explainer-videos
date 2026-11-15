"""Open trial-level datasets of *Psychology, Built*: fetched from their public home once, cached, checksummed.

Most of the Archive (:mod:`explainer.psychology.archive`) holds published summary numbers.  A few parts fit models
to raw trial-level data that its authors have shared; that data is not copied into the repository.  It is
downloaded on first use into ``.cache/psychology_data/`` (git-ignored) and checked against the SHA-256 recorded
here, so a changed file is noticed rather than silently fitted.  Each dataset also has a row in the Archive's
``SOURCES.md`` saying where it comes from and what was checked.

* :func:`bays_2009`: continuous report of colour, set sizes 1, 2, 4 and 6, sample durations 100, 500 and 2,000 ms,
  12 observers, 7,271 trials (Bays, Catalao and Husain, *Journal of Vision* 9(10):7, 2009); shared by Paul Bays on
  the Open Science Framework (osf.io/c2yx5).  Part 19.

Nothing here imports manim.
"""

from __future__ import annotations

import hashlib
import time
import urllib.request
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / ".cache" / "psychology_data"
UA = {"User-Agent": "explainer-videos/psychology (education)"}

SOURCES = {
    "bays_2009": {
        "url": "https://osf.io/download/dfhys/",
        "page": "https://osf.io/c2yx5/",
        "file": "bays_2009_Exp_data.mat",
        "sha256": "467d479936f8a06f6fe2a5ca54d51a1907df00fc66169b8e4a21121d91e6dd9e",
    },
}


def _get(url: str, retries: int = 4, timeout: int = 90) -> bytes:
    err = None
    for k in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                return r.read()
        except Exception as e:  # network errors and rate limits: back off and retry
            err = e
            time.sleep(min(2 ** k, 20))
    raise RuntimeError(f"failed to fetch {url}: {err}")


def path(key: str) -> Path:
    """The local copy of dataset ``key``, downloaded and checked on first use."""
    src = SOURCES[key]
    p = CACHE / src["file"]
    if not p.exists():
        raw = _get(src["url"])
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_name(p.name + ".tmp")
        tmp.write_bytes(raw)
        tmp.replace(p)
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    if h != src["sha256"]:
        raise RuntimeError(f"{key}: the downloaded file's SHA-256 {h[:12]} is not the recorded "
                           f"{src['sha256'][:12]}; the source changed, so check it at {src['page']}")
    return p


def available(key: str) -> bool:
    """Whether dataset ``key`` is cached or can be fetched now."""
    try:
        path(key)
        return True
    except Exception:
        return False


def bays_2009() -> dict:
    """Bays, Catalao and Husain (2009), one entry per trial.

    ``subject`` (1-12), ``set_size`` (1, 2, 4, 6), ``duration`` (sample display, ms: 100, 500, 2000), ``target`` and
    ``response`` (colour angles, radians), ``error`` (response minus target, wrapped to [-pi, pi)), ``nontarget``
    (trials x 5, the other items' colours, NaN where the display had fewer) and ``nontarget_error`` (response minus
    each non-target, wrapped)."""
    from scipy.io import loadmat

    m = loadmat(path("bays_2009"))
    nt = np.asarray(m["nontarget"], float)
    resp = m["response"].ravel().astype(float)
    return {
        "subject": m["subject"].ravel().astype(int),
        "set_size": m["n_items"].ravel().astype(int),
        "duration": m["delay"].ravel().astype(int),
        "target": m["target"].ravel().astype(float),
        "response": resp,
        "error": m["error"].ravel().astype(float),
        "nontarget": nt,
        "nontarget_error": (resp[:, None] - nt + np.pi) % (2 * np.pi) - np.pi,
    }
