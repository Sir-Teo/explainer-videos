"""The Data Room of *Economics, Built* (videos/economics/SYLLABUS.md, section 2.6): real data, with source and vintage.

    from explainer.economics import data
    world = data.maddison_world()                 # {"year": [...], "World": [...], "Western Europe": [...], ...}
    uk = data.maddison_country("GBR")             # {"year": [...], "gdppc": [...], "pop": [...]}
    ip = data.fred("INDPRO")                      # {"date": [...], "value": [...]} as frozen on DATASETS[...]["vintage"]
    data.cite("maddison2023")                     # the line for an on-screen data tag

Every dataset is registered in :data:`DATASETS` with its publisher, URL, licence, the date it was retrieved (its
vintage) and the SHA-256 of the raw download, and described in ``SOURCES.md`` beside this file.  The films read
small frozen extracts committed here (``*.csv``), so a build needs no network and every number on screen can be
traced to a file.  ``python -m explainer.economics.data --refresh NAME`` downloads the source again into
``.cache/economics/raw/``, reports whether it changed since the recorded vintage, and rewrites the extract; a film
that should use the new vintage must then say so (its frozen date moves).

Numbers transcribed from a publication (a table in a paper, a passage in a book) are in :mod:`.tables`, each with
its citation, page and the date it was checked.

This module needs numpy only (openpyxl to refresh the spreadsheets); it imports without manim, so the labs can use
it.
"""

from __future__ import annotations

import argparse
import csv
import functools
import hashlib
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RAW = ROOT / ".cache" / "economics" / "raw"

# ---------------------------------------------------------------------------
# The registry
# ---------------------------------------------------------------------------
FRED_SERIES = {
    # id: (title, units, frequency, source agency)
    "GDPCA": ("Real gross domestic product", "billions of chained 2017 dollars", "annual",
              "U.S. Bureau of Economic Analysis"),
    "GDPC1": ("Real gross domestic product", "billions of chained 2017 dollars, seasonally adjusted annual rate",
              "quarterly", "U.S. Bureau of Economic Analysis"),
    "UNRATE": ("Unemployment rate", "percent, seasonally adjusted", "monthly", "U.S. Bureau of Labor Statistics"),
    "M0892AUSM156SNBR": ("Unemployment rate for the United States, 1929-1942",
                         "percent, seasonally adjusted (National Industrial Conference Board estimates)",
                         "monthly", "NBER Macrohistory Database, series m08292a"),
    "INDPRO": ("Industrial production: total index", "index 2017 = 100, seasonally adjusted", "monthly",
               "Board of Governors of the Federal Reserve System"),
    "CPIAUCNS": ("Consumer price index for all urban consumers: all items", "index 1982-84 = 100, not seasonally "
                 "adjusted", "monthly", "U.S. Bureau of Labor Statistics"),
}

SPF_FILES = ("median_rgdp_level", "median_rgdp_growth", "median_recess_level")
SPF_URL = ("https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/survey-of-professional-forecasters/"
           "data-files/files/{}.xlsx")

DATASETS = {
    "maddison2023": {
        "title": "Maddison Project Database 2023",
        "publisher": "Groningen Growth and Development Centre, University of Groningen",
        "citation": "Bolt, J. and van Zanden, J. L. (2024), Maddison-style estimates of the evolution of the world "
                    "economy: a new 2023 update, Journal of Economic Surveys 1-41",
        "short": "Maddison Project Database 2023 (Bolt and van Zanden 2024)",
        "url": "https://dataverse.nl/api/access/datafile/421302",
        "page": "https://www.rug.nl/ggdc/historicaldevelopment/maddison/releases/maddison-project-database-2023",
        "licence": "CC BY 4.0; the MPD asks that the original country sources be cited when the data are shown "
                   "in a graph (SOURCES.md lists those used)",
        "units": "real GDP per head in 2011 international dollars; population in thousands",
        "vintage": "2026-11-18",
        "sha256": "ecc5916ca12789b983fc4be437f8a354bbf4291323605324ac3e0aea4c57cbb6",
        "files": ("maddison2023_world.csv", "maddison2023_countries.csv"),
    },
    "fred": {
        "title": "FRED, Federal Reserve Bank of St. Louis",
        "publisher": "Federal Reserve Bank of St. Louis (series from the agencies in FRED_SERIES)",
        "citation": "Federal Reserve Bank of St. Louis, FRED; each series retrieved 2026-11-18",
        "short": "FRED, retrieved 18 Nov 2026",
        "url": "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}",
        "licence": "BEA, BLS and Federal Reserve series are in the public domain; the NBER Macrohistory series is "
                   "used with its suggested citation",
        "vintage": "2026-11-18",
        "files": tuple(f"fred_{s}.csv" for s in FRED_SERIES),
    },
    "spf": {
        "title": "Survey of Professional Forecasters, median forecasts",
        "publisher": "Federal Reserve Bank of Philadelphia",
        "citation": "Federal Reserve Bank of Philadelphia, Survey of Professional Forecasters, historical median "
                    "forecasts (files median_rgdp_level, median_rgdp_growth, median_recess_level), retrieved "
                    "2026-11-18",
        "short": "Philadelphia Fed, Survey of Professional Forecasters",
        "url": SPF_URL,
        "licence": "free to use with attribution to the Federal Reserve Bank of Philadelphia",
        "vintage": "2026-11-18",
        "files": ("spf_2006_2011.csv",),
    },
}

# Countries kept at full (annual) resolution in the Maddison extract; every other country is kept at the
# benchmark years in MADDISON_YEARS (enough for the data films).
MADDISON_FULL = ("GBR", "NLD", "ITA", "FRA", "ESP", "SWE", "DEU", "USA", "JPN", "CHN", "IND", "KOR", "PRK", "NGA",
                 "BRA", "MEX", "ARG", "EGY", "TUR", "ZAF", "IDN", "ETH", "AUS", "CAN", "BWA", "VNM", "RUS", "SUN",
                 "POL", "BGD", "PAK", "GHA", "KEN", "CHL", "IRN", "SGP", "TWN")
MADDISON_YEARS = (1820, 1850, 1870, 1880, 1890, 1900, 1913, 1929, 1938, *range(1950, 2023, 2), 2022)


def cite(name: str) -> str:
    """The short source line for an on-screen data tag."""
    d = DATASETS[name]
    return d["short"]


def vintage(name: str) -> str:
    return DATASETS[name]["vintage"]


# ---------------------------------------------------------------------------
# Loaders (the committed extracts)
# ---------------------------------------------------------------------------
def _read(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _num(x: str):
    if x is None or x == "":
        return float("nan")
    return float(x)


@functools.lru_cache(maxsize=None)
def maddison_world() -> dict:
    """World and regional GDP per head, 1820-2022, from the MPD's regional sheet: ``{"year": [...], name: [...]}``.
    Missing values are NaN (several regions start after 1820)."""
    rows = _read(HERE / "maddison2023_world.csv")
    cols = [c for c in rows[0] if c != "year"]
    out = {"year": [int(r["year"]) for r in rows]}
    for c in cols:
        out[c] = [_num(r[c]) for r in rows]
    return out


@functools.lru_cache(maxsize=None)
def _maddison_rows() -> list[dict]:
    return _read(HERE / "maddison2023_countries.csv")


def maddison_country(code: str) -> dict:
    """One country's series from the extract: ``{"code", "name", "region", "year", "gdppc", "pop"}``.  Only years
    with a GDP-per-head estimate are kept.  Full annual series for :data:`MADDISON_FULL`, benchmark years for the
    rest."""
    rows = [r for r in _maddison_rows() if r["code"] == code]
    if not rows:
        raise KeyError(f"no Maddison series for {code!r} in the extract")
    return {"code": code, "name": rows[0]["country"], "region": rows[0]["region"],
            "year": [int(r["year"]) for r in rows], "gdppc": [_num(r["gdppc"]) for r in rows],
            "pop": [_num(r["pop"]) for r in rows]}


def maddison_year(year: int) -> list[dict]:
    """Every country with an estimate in ``year``: ``[{"code", "country", "region", "gdppc", "pop"}]``."""
    return [{"code": r["code"], "country": r["country"], "region": r["region"], "gdppc": _num(r["gdppc"]),
             "pop": _num(r["pop"])} for r in _maddison_rows() if int(r["year"]) == year]


@functools.lru_cache(maxsize=None)
def fred(series: str) -> dict:
    """A FRED series as frozen on the vintage date: ``{"date": ["YYYY-MM-DD", ...], "value": [...], "title",
    "units", "frequency", "source"}`` (missing observations are NaN)."""
    rows = _read(HERE / f"fred_{series}.csv")
    title, units, freq, source = FRED_SERIES[series]
    return {"date": [r["date"] for r in rows], "value": [_num(r["value"]) for r in rows], "title": title,
            "units": units, "frequency": freq, "source": source, "series": series}


@functools.lru_cache(maxsize=None)
def spf() -> list[dict]:
    """Median forecasts from each survey of 2006-2011: ``[{"year", "quarter", "rgdp_a", "rgdp_b", "growth_q": [...],
    "recess": [...]}]``.  ``rgdp_a``, ``rgdp_b``: the median forecast of the annual-average level of real GDP in the
    survey's year and the next; ``growth_q``: annualized quarterly growth for the survey quarter and the four after
    (DRGDP2-6); ``recess``: the probability (percent) of a decline in real GDP in the survey quarter and the four
    after (RECESS1-5)."""
    out = []
    for r in _read(HERE / "spf_2006_2011.csv"):
        out.append({"year": int(r["year"]), "quarter": int(r["quarter"]), "rgdp_a": _num(r["rgdp_a"]),
                    "rgdp_b": _num(r["rgdp_b"]),
                    "growth_q": [_num(r[f"drgdp{k}"]) for k in range(2, 7)],
                    "recess": [_num(r[f"recess{k}"]) for k in range(1, 6)]})
    return out


# ---------------------------------------------------------------------------
# Refreshing from the sources
# ---------------------------------------------------------------------------
def _download(url: str, dest: Path) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "explainer-videos-data-room/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        blob = r.read()
    dest.write_bytes(blob)
    return hashlib.sha256(blob).hexdigest()


def refresh_maddison() -> None:
    import openpyxl  # noqa: PLC0415  (only needed to refresh)

    d = DATASETS["maddison2023"]
    raw = RAW / "mpd2023.xlsx"
    sha = _download(d["url"], raw)
    if sha != d["sha256"]:
        print(f"maddison2023: the download differs from the recorded vintage ({sha[:12]} vs {d['sha256'][:12]})")
    wb = openpyxl.load_workbook(raw, read_only=True, data_only=True)
    rows = list(wb["Regional data"].iter_rows(values_only=True))
    names = [n for n in rows[1][1:9]]
    with open(HERE / "maddison2023_world.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "World", *names])
        for r in rows[2:]:
            if not isinstance(r[0], (int, float)):
                continue
            w.writerow([int(r[0]), _fmt(r[9]), *[_fmt(x) for x in r[1:9]]])
    keep = set(MADDISON_YEARS)
    with open(HERE / "maddison2023_countries.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["code", "country", "region", "year", "gdppc", "pop"])
        for r in wb["Full data"].iter_rows(min_row=2, values_only=True):
            cc, name, region, year, g, p = r[:6]
            if g is None or year is None:
                continue
            if cc in MADDISON_FULL or int(year) in keep:
                w.writerow([cc, name, region, int(year), _fmt(g), _fmt(p)])


def _fmt(x) -> str:
    if x is None or x == "":
        return ""
    return f"{float(x):.4f}".rstrip("0").rstrip(".")


def refresh_fred() -> None:
    for s in FRED_SERIES:
        raw = RAW / f"fred_{s}.csv"
        _download(DATASETS["fred"]["url"].format(s), raw)
        with open(raw, newline="") as f:
            rows = list(csv.reader(f))
        with open(HERE / f"fred_{s}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["date", "value"])
            for r in rows[1:]:
                w.writerow([r[0], "" if r[1] in (".", "") else r[1]])


def refresh_spf() -> None:
    import openpyxl  # noqa: PLC0415

    tabs = {}
    for name in SPF_FILES:
        raw = RAW / f"spf_{name}.xlsx"
        _download(SPF_URL.format(name), raw)
        ws = openpyxl.load_workbook(raw, read_only=True, data_only=True).worksheets[0]
        rows = list(ws.iter_rows(values_only=True))
        head = [str(h).lower() for h in rows[0]]
        tabs[name] = {(int(r[0]), int(r[1])): dict(zip(head, r)) for r in rows[1:] if isinstance(r[0], (int, float))}
    with open(HERE / "spf_2006_2011.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        cols = ["rgdp_a", "rgdp_b", *[f"drgdp{k}" for k in range(2, 7)], *[f"recess{k}" for k in range(1, 6)]]
        w.writerow(["year", "quarter", *cols])
        for (y, q) in sorted(tabs["median_rgdp_level"]):
            if not 2006 <= y <= 2011:
                continue
            lv, gr, rc = (tabs[n].get((y, q), {}) for n in SPF_FILES)
            vals = [lv.get("rgdpa"), lv.get("rgdpb"), *[gr.get(f"drgdp{k}") for k in range(2, 7)],
                    *[rc.get(f"recess{k}") for k in range(1, 6)]]
            w.writerow([y, q, *[_fmt(v) if isinstance(v, (int, float)) else "" for v in vals]])


REFRESH = {"maddison2023": refresh_maddison, "fred": refresh_fred, "spf": refresh_spf}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--refresh", nargs="*", choices=list(REFRESH), help="download again and rewrite the extract")
    args = ap.parse_args()
    for name in args.refresh or []:
        print(f"refreshing {name} ...")
        REFRESH[name]()
    if not args.refresh:
        for name, d in DATASETS.items():
            print(f"{name:14s} {d['vintage']}  {d['title']}  ({', '.join(d['files'])})")


if __name__ == "__main__":
    main()
