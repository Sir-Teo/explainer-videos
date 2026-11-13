"""The Ledger gate of *Psychology, Built* (videos/psychology/SYLLABUS.md, §1 "Gates per part" and §2.5).

    python tools/check_ledger.py psych2            # one part
    python tools/check_ledger.py                   # every part that is built

A part passes when every study it shows has a row in the Replication Ledger with its sources and the date they
were checked, or a stated reason for having none.  The gate reads the sources of the part, it renders nothing:

* **the rows the part enters** (``ledger.rows(part=N)``): at least one; each with a date that parses and is not in
  the future, references that carry a year, later studies no earlier than the original, and ``data`` naming
  datasets the Archive holds;
* **what the part shows**: every Archive dataset its scenes and its ``compute.py`` use, and every author-and-year
  written into a ``published_tag`` or ``historical_tag``.  Each has a row entered by this part or an earlier one,
  or a ``ledger.shown(part, name, why)`` declaration.  A declaration that defers the row to a later part fails
  once that part is built, and one that nothing in the part needs any more fails as stale;
* **the Ledger chapter**: a scene that draws ``ledger.rows(part=...)``, and no ``ledger.get`` of a key that is
  not there;
* **the README**: its Ledger table has one line per row, with the original study and the status as the Ledger
  holds them.

Rows checked more than ``--max-age`` days ago (default two years) are listed as a warning, since statuses change.
"""

from __future__ import annotations

import argparse
import ast
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from explainer.paths import VIDEOS, video_dir  # noqa: E402
from explainer.psychology import archive, ledger  # noqa: E402

SERIES = "psychology"
TAGS = {"published_tag", "historical_tag"}
PAIR = re.compile(r"([A-Z][A-Za-z'\-]+)[^()]*?\((\d{4})")


def built_parts() -> dict:
    """Part number -> video name, for every part with a manifest."""
    out = {}
    for m in VIDEOS.glob(f"{SERIES}/psych[0-9]*/manifest.py"):
        out[int(m.parent.name[len("psych"):])] = m.parent.name
    return dict(sorted(out.items()))


def plain(tex: str) -> str:
    """A tag's TeX with its markup taken out, for reading names and years."""
    tex = re.sub(r"\\emph\{([^{}]*)\}", r"\1", tex)
    return tex.replace(r"\&", "&").replace("\\ ", " ").replace("~", " ").replace("\\", "")


def scene_files(folder: Path) -> list:
    return sorted(folder.glob("s[0-9][0-9]_*.py"))


def shown_in(folder: Path) -> tuple:
    """(datasets, tag literals) a part shows: the Archive names its scenes and compute use, and the literal
    strings (those naming an author and a year) written into its source tags."""
    datasets: dict = {}
    literals: dict = {}
    files = scene_files(folder) + [f for f in [folder / "compute.py"] if f.exists()]
    for f in files:
        tree = ast.parse(f.read_text(), filename=str(f))
        for node in ast.walk(tree):
            if (isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "archive"
                    and node.attr.isupper() and node.attr != "ALL"):
                datasets.setdefault(node.attr, f.name)
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in TAGS
                    and node.args):
                for sub in ast.walk(node.args[0]):
                    if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                        text = sub.value.strip().strip(";,").strip()
                        text = re.sub(r"^\\ ", "", text).strip()
                        text = re.sub(r"(; )?\\$", "", text).strip().rstrip(";").strip()
                        if PAIR.search(plain(text)):
                            literals.setdefault(text, f.name)
    return datasets, literals


def cited(surname: str, year: int, rows: list) -> bool:
    """Is this author and year a study, or a reference, of one of these rows?"""
    for f in rows:
        for st in (f.original, *f.record):
            if st.year == year and surname in st.who:
                return True
        if any(surname in src and str(year) in src for src in f.sources):
            return True
    return False


def readme_table(text: str) -> list:
    """The lines of the README's Ledger table: (finding, original, status)."""
    out = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if re.match(r"\|\s*Finding\s*\|\s*Original\s*\|\s*Status\s*\|", line):
            for row in lines[i + 2:]:
                if not row.startswith("|"):
                    break
                cells = [c.strip() for c in row.strip().strip("|").split("|")]
                if len(cells) >= 3:
                    out.append(tuple(cells[:3]))
            break
    return out


def check_rows(n: int) -> tuple:
    problems, warnings = [], []
    rows = ledger.rows(part=n)
    if not rows:
        problems.append(f"Part {n} enters no Ledger row")
    today = dt.date.today()
    for f in rows:
        try:
            when = dt.date.fromisoformat(f.checked)
        except ValueError:
            problems.append(f"{f.key}: the date checked, {f.checked!r}, is not a date")
        else:
            if when > today:
                problems.append(f"{f.key}: checked on {f.checked}, which is in the future")
            warnings.append((f.key, (today - when).days))
        for src in f.sources:
            if len(src) < 30 or not re.search(r"\b(1[5-9]|20)\d\d\b", src):
                problems.append(f"{f.key}: a source should be a full reference with its year: {src!r}")
        if not f.original.who or not f.original.year:
            problems.append(f"{f.key}: the original study needs its authors and year")
        for st in f.record:
            if st.year < f.original.year:
                problems.append(f"{f.key}: {st.who} {st.year} is in the record but earlier than the original")
        for name in f.data:
            if not hasattr(archive, name):
                problems.append(f"{f.key}: the Archive has no dataset {name}")
        if not f.claim.strip().endswith("."):
            problems.append(f"{f.key}: the claim is one sentence, ending with a full stop")
    return problems, warnings


def check_shown(n: int, folder: Path, parts: dict) -> tuple:
    """Every study the part shows against the rows entered so far and the part's ``shown`` declarations."""
    problems, report = [], []
    datasets, literals = shown_in(folder)
    rows = ledger.rows(upto=n)
    declared = {s.name: s for s in ledger.SHOWN if s.part == n}
    used = set()
    for name, where in sorted(datasets.items()):
        if not hasattr(archive, name):
            problems.append(f"{where}: archive.{name} is not in the Archive")
            continue
        holders = [f.key for f in rows if name in f.data]
        if holders:
            report.append(f"{name}: row {', '.join(holders)}")
        elif name in declared:
            used.add(name)
        else:
            problems.append(f"{where} shows archive.{name}, which no Ledger row rests on: give a row `data`, or "
                            f"declare ledger.shown({n}, {name!r}, why)")
    for text, where in sorted(literals.items()):
        if text in declared:
            used.add(text)
            continue
        missing = [(who, year) for who, year in PAIR.findall(plain(text)) if not cited(who, int(year), rows)]
        if missing:
            names = ", ".join(f"{w} ({y})" for w, y in missing)
            problems.append(f"{where}: the tag {text!r} cites {names}, in no Ledger row so far: enter a row, or "
                            f"declare ledger.shown({n}, {text!r}, why)")
        else:
            report.append(f"{plain(text)}: cited in the Ledger")
    for name, s in declared.items():
        if name not in used:
            problems.append(f"ledger.shown({n}, {name!r}) is stale: the part no longer shows it, or it has a row")
            continue
        later = f"; its row is due in Part {s.row_in}" if s.row_in else ""
        report.append(f"{plain(name)}: no row ({s.why}{later})")
        if s.row_in in parts:
            problems.append(f"{name}: its row was deferred to Part {s.row_in}, which is built: enter the row there "
                            f"and remove the declaration")
    return problems, report


def check_scenes(n: int, folder: Path) -> list:
    problems = []
    board = False
    for f in scene_files(folder):
        text = f.read_text()
        if re.search(r"ledger\.rows\(\s*part\s*=\s*(PART|%d)\s*\)" % n, text):
            board = True
        for key in re.findall(r"ledger\.get\(\s*[\"']([^\"']+)[\"']\s*\)", text):
            if key not in ledger.LEDGER:
                problems.append(f"{f.name}: ledger.get({key!r}) is not a row")
            elif ledger.get(key).part > n:
                problems.append(f"{f.name}: the row {key!r} is entered by Part {ledger.get(key).part}, later than "
                                f"this part")
    if not board:
        problems.append("no scene draws the part's rows (ledger.rows(part=PART)): the Ledger chapter is missing")
    return problems


def check_readme(n: int, folder: Path) -> list:
    problems = []
    readme = folder / "README.md"
    table = readme_table(readme.read_text()) if readme.exists() else []
    rows = ledger.rows(part=n)
    if not table:
        return [f"{folder.name}/README.md has no Ledger table (| Finding | Original | Status |)"]
    if len(table) != len(rows):
        problems.append(f"README.md lists {len(table)} Ledger rows; the Ledger holds {len(rows)} for Part {n}")
    left = list(table)
    for f in rows:
        surname = re.split(r"[ ,]", f.original.who)[0]
        hit = [t for t in left if surname in t[1] and str(f.original.year) in t[1] and t[2].startswith(f.status)]
        if not hit:
            problems.append(f"README.md has no line for {f.key} ({f.original.who} {f.original.year}: {f.status})")
        else:
            left.remove(hit[0])
    return problems


def check(video: str, max_age: int = 730) -> tuple:
    """(problems, notes) for one part."""
    folder = video_dir(video)
    if folder.parent.name != SERIES:
        raise SystemExit(f"{video} is not a part of Psychology, Built")
    n = int(video[len("psych"):])
    parts = built_parts()
    problems, ages = check_rows(n)
    shown_problems, report = check_shown(n, folder, parts)
    problems += shown_problems + check_scenes(n, folder) + check_readme(n, folder)
    notes = [f"{len(ledger.rows(part=n))} rows entered"] + report
    old = [f"{key} ({days} days)" for key, days in ages if days > max_age]
    if old:
        notes.append("checked long ago, look again: " + ", ".join(old))
    return problems, notes


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("videos", nargs="*", help="psychN; default: every built part")
    ap.add_argument("--max-age", type=int, default=730, help="days after which a row's check is called old")
    args = ap.parse_args()
    videos = args.videos or list(built_parts().values())
    bad = 0
    for v in videos:
        problems, notes = check(v, args.max_age)
        print(f"{v}:")
        for line in notes:
            print(f"    {line}")
        for line in problems:
            print(f"  ! {line}")
        bad += len(problems)
    print(f"Ledger gate: {'OK' if not bad else f'{bad} problem(s)'} ({', '.join(videos)})")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
