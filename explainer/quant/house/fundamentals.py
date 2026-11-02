"""The House's fundamentals store (Part 3, *Value, Accounting and the Firm*): reported numbers, point in time.

Rule 4: a reported number exists from the day it was filed, as it was first reported; a restatement is a new fact
with its own filing date, never an edit of the past.

Each fact is bitemporal: the **period** it describes (when the quarter or year ended) and the **filing** that made it
public (when the market could know it).  The store is append-only; a query names the day it is asked *as of*, and
sees only facts filed by then, taking for each period the latest such filing:

    store = Store()
    store.add("ACME", "NetIncomeLoss", period_end=20191231, filed=20200220, value=200.0, form="10-K")
    store.add("ACME", "NetIncomeLoss", period_end=20191231, filed=20210315, value=150.0, form="10-K/A")
    store.asof("ACME", "NetIncomeLoss", 20200131)  # None: the year had ended but nothing was filed
    store.asof("ACME", "NetIncomeLoss", 20200630)  # 200.0, as first reported
    store.asof("ACME", "NetIncomeLoss", 20210630)  # 150.0, after the restatement

Facts are the shape of XBRL facts in EDGAR's company-facts files (concept, unit, period end, filing date, form,
accession number), so :meth:`Store.from_companyfacts` loads one directly.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, order=True)
class Fact:
    period_end: int          # YYYYMMDD: the end of the period the number describes
    filed: int               # YYYYMMDD: the day the filing reached the regulator
    value: float
    form: str = ""           # 10-K, 10-Q, 10-K/A ...
    accession: str = ""      # the filing's accession number
    period_start: int = 0    # YYYYMMDD for flows (income, cash flow); 0 for stocks (balance sheet)


@dataclass
class Store:
    facts: dict = field(default_factory=dict)  # (entity, concept) -> list[Fact], kept sorted by (period_end, filed)

    def add(self, entity: str, concept: str, period_end: int, filed: int, value: float, form: str = "",
            accession: str = "", period_start: int = 0) -> Fact:
        if filed < period_end:
            raise ValueError(f"{entity} {concept}: filed {filed} before the period ended {period_end}")
        f = Fact(int(period_end), int(filed), float(value), form, accession, int(period_start))
        lst = self.facts.setdefault((entity, concept), [])
        if f not in lst:
            lst.append(f)
            lst.sort()
        return f

    def known(self, entity: str, concept: str, t: int) -> list:
        """Every fact filed on or before ``t``."""
        return [f for f in self.facts.get((entity, concept), []) if f.filed <= t]

    def history(self, entity: str, concept: str, t: int) -> list:
        """The series as it stood on day ``t``: for each period, the latest value filed by then."""
        last = {}
        for f in self.known(entity, concept, t):
            if f.period_end not in last or f.filed >= last[f.period_end].filed:
                last[f.period_end] = f
        return [last[k] for k in sorted(last)]

    def asof(self, entity: str, concept: str, t: int):
        """The most recent period's value as known on day ``t``, or None if nothing had been filed."""
        h = self.history(entity, concept, t)
        return h[-1].value if h else None

    def first_reported(self, entity: str, concept: str) -> list:
        """For each period, the value as first filed (what the market saw on the day)."""
        first = {}
        for f in self.facts.get((entity, concept), []):
            if f.period_end not in first or f.filed < first[f.period_end].filed:
                first[f.period_end] = f
        return [first[k] for k in sorted(first)]

    def restatements(self, entity: str, concept: str) -> list:
        """(period_end, first value, later value, day of the change) for every value that was later changed."""
        out = []
        by = {}
        for f in self.facts.get((entity, concept), []):
            by.setdefault(f.period_end, []).append(f)
        for p, fs in sorted(by.items()):
            fs = sorted(fs, key=lambda f: f.filed)
            for a, b in zip(fs, fs[1:]):
                if b.value != a.value:
                    out.append((p, a.value, b.value, b.filed))
        return out

    @classmethod
    def from_companyfacts(cls, entity: str, payload: dict, concepts=None, unit: str = "USD") -> "Store":
        """Load EDGAR's ``companyfacts`` JSON (``facts -> us-gaap -> concept -> units -> unit -> [...]``)."""
        s = cls()
        for concept, body in payload.get("facts", {}).get("us-gaap", {}).items():
            if concepts is not None and concept not in concepts:
                continue
            for row in body.get("units", {}).get(unit, []):
                end, filed = int(row["end"].replace("-", "")), int(row["filed"].replace("-", ""))
                start = int(row["start"].replace("-", "")) if "start" in row else 0
                s.add(entity, concept, end, filed, row["val"], row.get("form", ""), row.get("accn", ""), start)
        return s
