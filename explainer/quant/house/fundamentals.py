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

Also here: :func:`filing_lags` (how long the market waited for each number); the toy firm (:class:`Firm`,
:func:`step`, :func:`simulate`), whose three statements are one double-entry machine; :func:`earnings_panel`, a
simulated panel whose accruals carry a reversing error; and the earnings-event tools :func:`sue` and :func:`car`.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


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


# ---------------------------------------------------------------------------
# Part 3, expanded: filing lags; the three statements as one double-entry machine; accruals; earnings events
# ---------------------------------------------------------------------------
def _days(a: int, b: int) -> int:
    from datetime import date

    da = date(a // 10000, a // 100 % 100, a % 100)
    db = date(b // 10000, b // 100 % 100, b % 100)
    return (db - da).days


def filing_lags(store: Store, entity: str, concept: str, forms=("10-K",)) -> list:
    """For each period, the days from its end to the first filing of a form in ``forms`` that reported it: how long
    the market waited for the number."""
    first = {}
    for f in store.facts.get((entity, concept), []):
        if forms and f.form not in forms:
            continue
        if f.period_end not in first or f.filed < first[f.period_end]:
            first[f.period_end] = f.filed
    return [(p, _days(p, d)) for p, d in sorted(first.items())]


@dataclass
class Firm:
    """A toy firm's balance sheet: what it owns (cash, receivables, plant) and who has a claim on it (debt, equity)."""
    cash: float = 150.0
    receivables: float = 0.0
    plant: float = 500.0
    debt: float = 200.0
    equity: float = 450.0

    def assets(self) -> float:
        return self.cash + self.receivables + self.plant

    def claims(self) -> float:
        return self.debt + self.equity


def step(firm: Firm, sales: float, cost_ratio=0.7, credit=0.2, dep_rate=0.05, capex=0.0, payout=0.25,
         rate_debt=0.0, tax=0.0, write_off=0.0) -> dict:
    """One period's journal entries, posted to ``firm`` in place.  A share ``credit`` of sales is unpaid (a
    receivable); last period's receivables are collected, less ``write_off`` of them that never pay.  Every entry
    touches both sides, so assets = claims after each period (asserted).  Returns the period's three statements."""
    collected = (1 - write_off) * firm.receivables
    lost = write_off * firm.receivables
    firm.receivables = credit * sales                       # new credit sales replace the collected ones
    firm.cash += (1 - credit) * sales + collected
    costs = cost_ratio * sales
    firm.cash -= costs
    dep = dep_rate * firm.plant
    firm.plant += capex - dep
    firm.cash -= capex
    interest = rate_debt * firm.debt
    ebt = sales - costs - dep - interest - lost
    taxes = tax * max(ebt, 0.0)
    firm.cash -= interest + taxes
    ni = ebt - taxes
    div = payout * max(ni, 0.0)
    firm.cash -= div
    firm.equity += ni - div                                 # clean surplus: equity moves by earnings less payout
    assert abs(firm.assets() - firm.claims()) < 1e-9, "the books do not balance"
    d_ar = credit * sales - (collected + lost)
    cfo = ni + dep - d_ar                                   # the indirect method
    return {"sales": sales, "costs": costs, "depreciation": dep, "interest": interest, "taxes": taxes,
            "net_income": ni, "cfo": cfo, "accruals": ni - cfo, "capex": capex, "dividends": div,
            "collected": collected, "written_off": lost, "cash": firm.cash, "receivables": firm.receivables,
            "plant": firm.plant, "debt": firm.debt, "equity": firm.equity, "assets": firm.assets()}


def simulate(firm: Firm, periods: int, sales0=250.0, growth=0.02, vol=0.08, seed=0, **kw) -> list:
    """Run :func:`step` for ``periods`` periods with sales growing at ``growth`` per period with lognormal noise,
    and capital spending that keeps plant in line with sales.  Returns the list of statements."""
    rng = np.random.default_rng(seed)
    out = []
    s = sales0
    dep_rate = kw.get("dep_rate", 0.05)
    for _ in range(periods):
        s *= (1 + growth) * np.exp(vol * rng.standard_normal() - vol ** 2 / 2)
        capex = max(dep_rate * firm.plant + growth * firm.plant, 0.0)
        out.append(step(firm, s, capex=capex, **kw))
    return out


def earnings_panel(n_firms: int, years: int, seed=0, mu=0.06, phi=0.8, phi_loss=None, sd_roa=0.03, sd_err=0.005,
                   accrual_share=(-0.2, 0.6), growth_sd=0.08) -> dict:
    """A simulated panel whose truth is known, for accrual and forecasting experiments.  True return on assets
    follows an AR(1) around ``mu`` with persistence ``phi`` (``phi_loss`` when the firm is losing money, if given).
    Reported earnings add a booked estimation error e_t (receivables that will not pay, provisions too small) that
    reverses next year: E_t = ROA_t + e_t - e_{t-1}.  A random share of true profit, drawn from ``accrual_share``, is
    not yet cash (a true accrual, as persistent as profit); the error lives only in accruals, so cash flow is clean.
    All items are scaled by assets; ``growth`` is a sales-growth item unrelated to the truth."""
    rng = np.random.default_rng(seed)
    burn = 20
    T = years + burn
    roa = np.empty((n_firms, T))
    roa[:, 0] = mu + sd_roa * rng.standard_normal(n_firms) / np.sqrt(1 - phi ** 2)
    for t in range(1, T):
        p = phi if phi_loss is None else np.where(roa[:, t - 1] < 0, phi_loss, phi)
        roa[:, t] = mu + p * (roa[:, t - 1] - mu) + sd_roa * rng.standard_normal(n_firms)
    err = sd_err * rng.standard_normal((n_firms, T))
    g = growth_sd * rng.standard_normal((n_firms, T)) + 0.04
    true_acc = rng.uniform(*accrual_share, (n_firms, T)) * roa   # profit booked but not yet collected
    E = roa + err - np.roll(err, 1, axis=1)
    ACC = true_acc + err - np.roll(err, 1, axis=1)
    CFO = E - ACC
    sl = slice(burn, T)
    return {"E": E[:, sl], "CFO": CFO[:, sl], "ACC": ACC[:, sl], "ROA": roa[:, sl], "err": err[:, sl],
            "growth": g[:, sl], "params": {"mu": mu, "phi": phi, "phi_loss": phi_loss, "sd_roa": sd_roa,
                                           "sd_err": sd_err}}


def sue(x, lookback: int = 8) -> np.ndarray:
    """Standardized unexpected earnings under a seasonal random walk: (x_q - x_{q-4}) divided by the standard
    deviation of the previous ``lookback`` seasonal differences.  NaN until enough history."""
    x = np.asarray(x, float)
    d = np.full(len(x), np.nan)
    d[4:] = x[4:] - x[:-4]
    out = np.full(len(x), np.nan)
    for q in range(4 + lookback, len(x)):
        past = d[q - lookback:q]
        sd = np.nanstd(past, ddof=1)
        if np.isfinite(d[q]) and sd > 0:
            out[q] = d[q] / sd
    return out


def car(returns, market, day0: int, window=(-5, 60)) -> np.ndarray:
    """Cumulative abnormal return in event time: r_i - r_m summed from ``window[0]`` to each day up to
    ``window[1]``, around the index ``day0`` (the first trading day the news could be traded on)."""
    r = np.asarray(returns, float)
    m = np.asarray(market, float)
    a, b = window
    lo, hi = day0 + a, day0 + b + 1
    if lo < 0 or hi > len(r):
        return np.full(b - a + 1, np.nan)
    return np.cumsum(r[lo:hi] - m[lo:hi])
