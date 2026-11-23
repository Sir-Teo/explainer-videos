"""The Register: every figure an *Industry, Built* film shows, with its definition, source and dates (SYLLABUS §2.7).

    from explainer.industry.register import get, row
    get("apple.iphone_sales.fy2026")      # 254.098 (the value, in the row's unit)
    row("apple.iphone_sales.fy2026")      # the whole Row: unit, definition, source, url, dates, note

A row is either a single ``value`` or a range (``lo``, ``hi``; ``value`` is then the central figure the film uses).
``kind`` says what sort of figure it is:

* ``filing``    a company's own audited or reported number (10-K, 20-F, 6-K, annual results);
* ``official``  a statistical office, regulator or court;
* ``tracker``   a market tracker's published estimate (IDC, Counterpoint, TrendForce, Omdia): estimates, not counts;
* ``study``     a published paper;
* ``press``     a figure known only through press reporting of a source we could not read (used sparingly, flagged);
* ``assumption``  this series' own assumption, stated and bounded.

``tools/check_register.py industryN`` fails a part whose scenes ask for a key with no row, or a row without a source.
Rows live in ``explainer/industry/data/rows_pNN.py`` (one module per part); a later part may reuse earlier rows.
"""

from __future__ import annotations

import datetime as dt
import importlib
import pkgutil
from dataclasses import dataclass, field

KINDS = ("filing", "official", "tracker", "study", "press", "assumption")


@dataclass(frozen=True)
class Row:
    key: str
    value: float
    unit: str
    definition: str
    source: str
    url: str
    fact: str            # the date (or period) the figure describes, e.g. "FY2026 (to 2026-09-26)"
    checked: str         # ISO date the figure was read from its source
    kind: str = "filing"
    lo: float | None = None
    hi: float | None = None
    note: str = ""
    stale_after: str = ""  # ISO date; empty = one year after ``checked``
    parts: tuple = field(default=(1,))

    def stale(self, today: dt.date | None = None) -> bool:
        today = today or dt.date.today()
        limit = (dt.date.fromisoformat(self.stale_after) if self.stale_after
                 else dt.date.fromisoformat(self.checked) + dt.timedelta(days=365))
        return today > limit


_ROWS: dict[str, Row] = {}
_LOADED = False


def add(*rows: Row) -> None:
    for r in rows:
        if r.key in _ROWS and _ROWS[r.key] != r:
            raise ValueError(f"register: {r.key} entered twice with different contents")
        if r.kind not in KINDS:
            raise ValueError(f"register: {r.key} has unknown kind {r.kind!r}")
        _ROWS[r.key] = r


def _load() -> None:
    global _LOADED
    if _LOADED:
        return
    from explainer.industry import data

    for m in sorted(pkgutil.iter_modules(data.__path__), key=lambda m: m.name):
        if m.name.startswith("rows_"):
            importlib.import_module(f"explainer.industry.data.{m.name}")
    _LOADED = True


USED: set[str] = set()  # keys asked for in this process (tools/check_register.py reads it after a dry run)


def row(key: str) -> Row:
    _load()
    if key not in _ROWS:
        raise KeyError(f"register: no row {key!r}; enter it in explainer/industry/data/rows_pNN.py with its source")
    USED.add(key)
    return _ROWS[key]


def get(key: str) -> float:
    return row(key).value


def span(key: str) -> tuple[float, float]:
    r = row(key)
    return (r.lo if r.lo is not None else r.value, r.hi if r.hi is not None else r.value)


def rows(part: int | None = None) -> list[Row]:
    _load()
    return [r for r in _ROWS.values() if part is None or part in r.parts]


def problems(part: int | None = None) -> list[str]:
    """What is wrong with the rows of ``part``: missing sources, URLs, dates, ranges that do not hold the value."""
    out = []
    for r in rows(part):
        if not r.source.strip():
            out.append(f"{r.key}: no source")
        if r.kind != "assumption" and not r.url.startswith(("http://", "https://")):
            out.append(f"{r.key}: no URL")
        try:
            dt.date.fromisoformat(r.checked)
        except ValueError:
            out.append(f"{r.key}: checked date {r.checked!r} is not ISO")
        if r.lo is not None and r.hi is not None and not (r.lo <= r.value <= r.hi):
            out.append(f"{r.key}: value {r.value} outside its range [{r.lo}, {r.hi}]")
        if r.kind == "press" and not r.note:
            out.append(f"{r.key}: a press-reported figure needs a note saying whose estimate it is")
    return out
