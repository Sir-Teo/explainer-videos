"""Open trial-level datasets of *Psychology, Built*: fetched from their public home once, cached, checksummed.

Most of the Archive (:mod:`explainer.psychology.archive`) holds published summary numbers.  A few parts fit models
to raw trial-level data that its authors have shared; that data is not copied into the repository.  It is
downloaded on first use into ``.cache/psychology_data/`` (git-ignored) and checked against the SHA-256 recorded
here, so a changed file is noticed rather than silently fitted.  Each dataset also has a row in the Archive's
``SOURCES.md`` saying where it comes from and what was checked.

* :func:`bays_2009`: continuous report of colour, set sizes 1, 2, 4 and 6, sample durations 100, 500 and 2,000 ms,
  12 observers, 7,271 trials (Bays, Catalao and Husain, *Journal of Vision* 9(10):7, 2009); shared by Paul Bays on
  the Open Science Framework (osf.io/c2yx5).  Part 19.
* :func:`peers_free_recall`: immediate free recall of 16-word lists, 126 people and 3,528 lists, from the Penn
  Electrophysiology of Encoding and Retrieval Study (Kahana lab), in the subset packaged with the psifr analysis
  package (a CSV inside its wheel on PyPI; both the wheel and the CSV are checked).  Part 20.
* :func:`murre_2021`: Murre's direct replication of Godden and Baddeley's divers, sixteen divers' words recalled in
  four conditions, from the workbook he shared on the Open Science Framework (osf.io/q2vjk).  Part 20.

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
    "peers_free_recall": {
        # psifr 0.10.1 on PyPI (GPL-3.0-or-later) ships a subset of PEERS immediate free recall as a CSV
        "url": "https://files.pythonhosted.org/packages/d1/d2/f40f44465ef714a70715895cb1ae5ca5c6826133d5cbe091c1bb1ec49a45/"
               "psifr-0.10.1-py3-none-any.whl",
        "page": "https://pypi.org/project/psifr/0.10.1/",
        "file": "psifr-0.10.1-py3-none-any.whl",
        "sha256": "cd22befa61d5d6cbcb3fef970d5c1f7eda5b9acd94618cac08095dc9a271f562",
        "member": "psifr/data/peers_notask.csv",
        "member_sha256": "592f67aae9f8f9bd45a019727c7a498579017d0b7ebdf45666a647a432ce1684",
    },
    "murre_2021": {
        # J. M. J. Murre, Royal Society Open Science 8 (2021) 200724; the workbook at osf.io/q2vjk (component 5xas9)
        "url": "https://osf.io/download/j37sh/",
        "page": "https://osf.io/q2vjk/",
        "file": "murre_2021.xlsx",
        "sha256": "a15c0aaab08d89ad706d692c3201d95c3e24ec6f5afa156b0097c08db5515ce5",
    },
    "overshadowing_rrr1": {
        # V. K. Alogna et al., Perspectives on Psychological Science 9 (2014) 556-578; osf.io/ybeur (component xui4e)
        "url": "https://osf.io/download/dv5ei/",
        "page": "https://osf.io/ybeur/",
        "file": "overshadowing_rrr1.xlsx",
        "sha256": "562b471251e65102694b0449adf71bb8c588deeeb5f09664fb824894c71295db",
    },
    "overshadowing_rrr2": {
        "url": "https://osf.io/download/dy6at/",
        "page": "https://osf.io/ybeur/",
        "file": "overshadowing_rrr2.xlsx",
        "sha256": "81be7ccd1ae7973fb223c745050fc3fc3c551705366d158542067bffde44b775",
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


def member_path(key: str):
    """The local copy of a file inside an archive source, extracted and checked on first use."""
    import zipfile

    src = SOURCES[key]
    out = CACHE / (key + "_" + Path(src["member"]).name)
    if not out.exists():
        with zipfile.ZipFile(path(key)) as z:
            raw = z.read(src["member"])
        tmp = out.with_name(out.name + ".tmp")
        tmp.write_bytes(raw)
        tmp.replace(out)
    h = hashlib.sha256(out.read_bytes()).hexdigest()
    if h != src["member_sha256"]:
        raise RuntimeError(f"{key}: {src['member']} has SHA-256 {h[:12]}, not the recorded {src['member_sha256'][:12]}")
    return out


def peers_free_recall() -> dict:
    """Immediate free recall of 16-word lists from the Penn Electrophysiology of Encoding and Retrieval Study
    (PEERS, Kahana lab), as packaged with psifr: 126 subjects, 3,528 lists.

    ``subject`` and ``session`` per list; ``words`` (lists x 16) in study order; ``recalls`` (lists x 24) of serial
    positions 1..16 in output order, 0 for an intrusion and for padding; ``intrusions`` per list."""
    import csv

    rows = list(csv.DictReader(open(member_path("peers_free_recall"), newline="")))
    study, rec = {}, {}
    for r in rows:
        k = (int(r["subject"]), int(r["session"]), int(r["list"]))
        if r["trial_type"] == "study":
            study.setdefault(k, {})[r["item"]] = int(r["position"])
        else:
            rec.setdefault(k, []).append(r["item"])
    keys = sorted(study)
    n = 16
    words = np.empty((len(keys), n), dtype=object)
    recalls = np.zeros((len(keys), 24), int)
    intr = np.zeros(len(keys), int)
    for i, k in enumerate(keys):
        for w, p in study[k].items():
            words[i, p - 1] = w
        seq = [study[k].get(w, 0) for w in rec.get(k, [])][:24]
        recalls[i, :len(seq)] = seq
        intr[i] = sum(1 for p in seq if p == 0)
    return {"subject": np.array([k[0] for k in keys]), "session": np.array([k[1] for k in keys]), "words": words,
            "recalls": recalls, "intrusions": intr, "list_length": n}


def _xlsx_cells(file, sheet: int = 1) -> dict:
    """The values of one worksheet of an .xlsx file, by cell reference ("B18" -> "10"), read with the standard
    library (an .xlsx file is a zip of XML; nothing in it is executed)."""
    import xml.etree.ElementTree as ET
    import zipfile

    m = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    with zipfile.ZipFile(file) as z:
        shared = [''.join(t.text or "" for t in si.iter(m + "t"))
                  for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(m + "si")]
        root = ET.fromstring(z.read(f"xl/worksheets/sheet{sheet}.xml"))
    out = {}
    for c in root.iter(m + "c"):
        v = c.find(m + "v")
        if v is not None:
            out[c.get("r")] = shared[int(v.text)] if c.get("t") == "s" else v.text
    return out


def murre_2021() -> dict:
    """Murre's replication of Godden and Baddeley: sixteen divers, each learning a list of 36 words on land or
    underwater and recalling it four minutes later on land or underwater (all four combinations, in a Graeco-Latin
    square).  ``scores`` is (16, 4): words recalled in the order DD, DW, WD, WW (learning place first; D = dry,
    W = wet), one row per diver, taken from the 'Analysis' sheet of the published workbook."""
    cells = _xlsx_cells(path("murre_2021"), 1)
    col = lambda c, r0: [float(cells[f"{c}{r}"]) for r in range(r0, r0 + 16)]  # noqa: E731
    dd, wd = col("B", 18), col("C", 18)  # recall on land: learned on land, learned underwater
    dw, ww = col("B", 34), col("C", 34)  # recall underwater
    return {"scores": np.array([dd, dw, wd, ww]).T, "conditions": ("DD", "DW", "WD", "WW"), "words": 36}


def overshadowing_rrr(study: int) -> dict:
    """The verbal-overshadowing Registered Replication Report (Alogna et al. 2014), per lab.  Study 1 had the
    description straight after the film; study 2 had it after a 20-minute filler task, as in the original Study 1.
    ``verbal`` and ``control`` are (labs, 2) arrays of (correct identifications, people included); ``original`` and
    ``online`` are the same pairs for the original study and the online (MTurk) sample, which the report kept out of
    its meta-analysis.  ``labs`` names the first author of each lab."""
    cells = _xlsx_cells(path(f"overshadowing_rrr{study}"), 1)
    rows = sorted({int("".join(ch for ch in ref if ch.isdigit())) for ref in cells})
    out = {"verbal": [], "control": [], "labs": []}
    for r in rows:
        if not str(cells.get(f"H{r}", "")).isdigit():
            continue
        v = (int(cells[f"I{r}"]), int(cells[f"H{r}"]))
        c = (int(cells[f"Q{r}"]), int(cells[f"P{r}"]))
        who = cells[f"A{r}"]
        if who.startswith("ORIGINAL"):
            out["original"] = np.array([v, c])
        elif who.startswith("ONLINE"):
            out["online"] = np.array([v, c])
        else:
            out["verbal"].append(v)
            out["control"].append(c)
            out["labs"].append(who.split(",")[0].strip())
    out["verbal"], out["control"] = np.array(out["verbal"]), np.array(out["control"])
    return out
