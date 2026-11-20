#!/usr/bin/env python
"""The Dials gate of *Economics, Built*: a part may show a number only with its record.

    python tools/check_dials.py econ1            # exit 1, with the reasons, if the part fails
    python tools/check_dials.py --all

For one part (``videos/economics/econN``) it checks, from the part's own sources:

* every transcribed table the part uses (``tables.NAME`` in its scenes or ``compute.py``) is registered in
  ``explainer.economics.data.tables`` with a citation, where it is in the publication, and the date it was checked;
* every Data Room dataset it loads (``data.maddison_*``, ``data.fred``, ``data.spf``, ``data.pinksheet``,
  ``data.psd_coffee``, ``data.wdi``, ``data.hdr``, ``data.rtdsm``) is registered in
  ``explainer.economics.data.DATASETS`` with a licence and a vintage, and its extracts are listed in ``SOURCES.md``;
* every Called-it card it draws (``call_card(``) comes from a ``explainer.economics.calls`` entry for the part
  (``calls.CALLS["key"]``), and every entry it names exists and belongs to the part;
* every study it draws (``study_card(``, ``published_tag(``) is accounted for: the part either enters a row in
  ``explainer.economics.dials.DIALS`` (a dial whose ``parts`` include it, with estimates) or declares in
  ``dials.SHOWN`` what it shows without one, and why.

The film is the authority for what is shown; this gate is the bookkeeping that keeps a number from appearing without
its source, the way *Psychology, Built*'s Ledger gate does for findings.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from explainer.economics import calls, data, dials  # noqa: E402
from explainer.economics.data import tables  # noqa: E402

LOADERS = {"maddison_world": "maddison2023", "maddison_country": "maddison2023", "maddison_year": "maddison2023",
           "fred": "fred", "spf": "spf", "pinksheet": "pinksheet", "psd_coffee": "psd_coffee", "wdi": "wdi",
           "hdr": "hdr", "rtdsm": "rtdsm", "warheads": "warheads", "so2": "so2", "marriage": "marriage",
           "democracy": "democracy", "millennium": "millennium", "longrun": "longrun", "pwt": "pwt", "ajr": "ajr",
           "shiller": "shiller",
           "rtdsm_q1": "rtdsm", "greenbook": "greenbook", "hlw": "hlw", "wdi_money": "wdi_money",
           "cbsa": "census_cbsa", "urban_share": "urban_share", "njmin": "njmin", "wooldridge": "wooldridge",
           "autor_dorn": "autor_dorn", "resume": "resume", "saez": "saez", "opportunity": "opportunity",
           "wid_top1": "wid_top1", "blp_cars": "blp_cars"}


def check(video: str) -> list[str]:
    m = re.fullmatch(r"econ(\d+)", video)
    if not m:
        return [f"{video}: not a part of Economics, Built"]
    part = int(m.group(1))
    folder = ROOT / "videos" / "economics" / video
    if not folder.exists():
        return [f"{video}: no folder {folder}"]
    src = "\n".join(p.read_text() for p in sorted(folder.glob("*.py")))
    problems = []
    # transcribed tables
    for name in sorted(set(re.findall(r"\btables\.([A-Z][A-Z0-9_]+)\b", src))):
        t = getattr(tables, name, None)
        if t is None:
            problems.append(f"{video}: tables.{name} is not in explainer/economics/data/tables.py")
            continue
        for field in ("cite", "where", "read", "checked"):
            if not getattr(t, field):
                problems.append(f"{video}: tables.{name} has no {field}")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", t.checked or ""):
            problems.append(f"{video}: tables.{name} has no date checked")
    # the Data Room
    sources = (ROOT / "explainer" / "economics" / "data" / "SOURCES.md").read_text()
    for loader in sorted(set(re.findall(r"\bdata\.(" + "|".join(LOADERS) + r")\(", src))):
        d = data.DATASETS[LOADERS[loader]]
        if not d.get("licence") or not d.get("vintage"):
            problems.append(f"{video}: dataset {LOADERS[loader]} has no licence or vintage")
        for f in d["files"]:
            if f"`{f}`" not in sources:
                problems.append(f"{video}: {f} is not listed in SOURCES.md")
    # Called it? (a call may be drawn more than once, e.g. unscored in the hook and scored later)
    n_cards = len(re.findall(r"\bcall_card\(", src))
    keys = set(re.findall(r"calls\.CALLS\[\s*[\"']([A-Za-z0-9_]+)[\"']\s*\]", src))
    mine = {k for k, c in calls.CALLS.items() if c.part == part}
    for k in sorted(keys):
        if k not in calls.CALLS:
            problems.append(f"{video}: calls.CALLS[{k!r}] is not in explainer/economics/calls.py")
        elif k not in mine:
            problems.append(f"{video}: calls.CALLS[{k!r}] belongs to Part {calls.CALLS[k].part}, not Part {part}")
    if n_cards and not (keys & mine):
        problems.append(f"{video}: draws {n_cards} Called-it card(s) but uses no call entered for Part {part} in "
                        f"explainer/economics/calls.py")
    # studies shown
    n_studies = len(re.findall(r"\b(study_card|published_tag)\(", src))
    rows = [d for d in dials.DIALS.values() if part in d.parts and d.estimates]
    if n_studies and not rows and not dials.SHOWN.get(part):
        problems.append(f"{video}: shows {n_studies} studies or published results, but enters no Dial row and "
                        f"declares nothing in dials.SHOWN[{part}]")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("videos", nargs="*")
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()
    videos = args.videos or []
    if args.all:
        videos = sorted((p.parent.name for p in (ROOT / "videos" / "economics").glob("econ[0-9]*/manifest.py")),
                        key=lambda v: int(v[4:]))
    if not videos:
        ap.error("name a part (econ1) or pass --all")
    bad = []
    for v in videos:
        probs = check(v)
        bad += probs
        print(f"{v}: {'ok' if not probs else f'{len(probs)} problem(s)'}")
    for p in bad:
        print("  " + p)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
