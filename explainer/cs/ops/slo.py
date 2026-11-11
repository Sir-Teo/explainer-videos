"""Service-level objectives and error budgets (Part 50): a synthetic month of requests with incidents of four
shapes, the budget draining, and five alerting rules from the SRE Workbook (2018, chapter 5) scored on it:
detection time, reset time, missed incidents and needless pages."""

from __future__ import annotations

import numpy as np

MONTH_MIN = 30 * 24 * 60

INCIDENTS = [  # (name, start minute, duration in minutes, error rate)
    ("blip", 3 * 1440 + 600, 4, 0.05),
    ("second blip", 11 * 1440 + 900, 3, 0.08),
    ("third blip", 26 * 1440 + 100, 8, 0.03),
    ("outage", 8 * 1440 + 200, 25, 0.25),
    ("degradation", 14 * 1440 + 300, 6 * 60, 0.012),
    ("slow leak", 20 * 1440, 3 * 1440, 0.002),
]


def month(rpm: float = 1000.0, base: float = 0.0001, incidents=INCIDENTS, seed: int = 0) -> dict:
    """Requests per minute (Poisson around ``rpm``) and errors (binomial), with background error rate ``base``."""
    rng = np.random.default_rng(seed)
    req = rng.poisson(rpm, MONTH_MIN)
    rate = np.full(MONTH_MIN, base)
    for _, s, d, r in incidents:
        rate[s:s + d] = np.maximum(rate[s:s + d], r)
    err = rng.binomial(req, rate)
    return {"req": req, "err": err, "rate": rate}


def thresholds(slo: float = 0.999) -> list[dict]:
    """Burn rate b consumes the month's budget in 30 days / b.  To page when a share f of the budget has gone in
    a window w, the threshold is b = f * 30 days / w."""
    out = []
    for share, window_h, action in ((0.02, 1, "page"), (0.05, 6, "page"), (0.10, 72, "ticket")):
        b = share * 30 * 24 / window_h
        out.append({"share": share, "window_h": window_h, "burn": b, "error_rate": b * (1 - slo), "action": action,
                    "exhaust_h": 30 * 24 / b})
    return out


def _window(x: np.ndarray, w: int) -> np.ndarray:
    c = np.concatenate([[0], np.cumsum(x)])
    i = np.arange(1, len(x) + 1)
    return c[i] - c[np.maximum(0, i - w)]


def _rate(m, w):
    r = _window(m["req"], w)
    return _window(m["err"], w) / np.maximum(r, 1)


def _burn(m, w, s, b):
    return _rate(m, w) > b * (1 - s)


# each rule: (what pages, what opens a ticket)
RULES = {
    "error rate > 0.1% over 10 minutes": lambda m, s: (_rate(m, 10) > (1 - s), None),
    "error rate > 0.1% over 36 hours": lambda m, s: (_rate(m, 36 * 60) > (1 - s), None),
    "burn > 14.4 over 1 hour": lambda m, s: (_burn(m, 60, s, 14.4), None),
    "multiple burn rates": lambda m, s: (_burn(m, 60, s, 14.4) | _burn(m, 360, s, 6), _burn(m, 4320, s, 1)),
    "multiwindow, multi-burn-rate": lambda m, s: ((_burn(m, 60, s, 14.4) & _burn(m, 5, s, 14.4))
                                                  | (_burn(m, 360, s, 6) & _burn(m, 30, s, 6)),
                                                  _burn(m, 4320, s, 1) & _burn(m, 360, s, 1)),
}


def _episodes(fire: np.ndarray) -> list[tuple[int, int]]:
    d = np.diff(np.concatenate([[0], fire.astype(int), [0]]))
    return list(zip(np.flatnonzero(d == 1), np.flatnonzero(d == -1)))


def budget_used(m, slo: float = 0.999) -> dict:
    """The share of the month's error budget consumed, minute by minute, and by each incident."""
    budget = (1 - slo) * m["req"].sum()
    used = np.cumsum(m["err"]) / budget
    per = {}
    for name, s, d, r in INCIDENTS:
        extra = m["err"][s:s + d].sum() - (m["req"][s:s + d] * 0.0001).sum()
        per[name] = float(extra / budget)
    return {"used": used, "per_incident": per, "budget_errors": float(budget)}


def score(slo: float = 0.999, seed: int = 0, significant: float = 0.02) -> dict:
    """Each rule's alerts on the synthetic month.  An incident is significant if it burns at least
    ``significant`` of the month's budget; paging for anything else is a needless page."""
    m = month(seed=seed)
    b = budget_used(m, slo)
    rows = []
    for name, rule in RULES.items():
        page, ticket = rule(m, slo)
        tiers = {"page": _episodes(page)}
        if ticket is not None:
            tiers["ticket"] = _episodes(ticket & ~page)
        per = {}
        for inc, s, d, r in INCIDENTS:
            per[inc] = {"detected": False}
            for tier, eps in tiers.items():
                hit = [(a, z) for a, z in eps if s - 5 <= a <= s + d + 60]
                if hit:
                    a, z = hit[0][0], max(z for _, z in hit)
                    per[inc] = {"detected": True, "by": tier, "delay_min": int(max(0, a - s)),
                                "reset_min": int(max(0, z - (s + d)))}
                    break
        needless = 0
        for a, z in tiers["page"]:
            owner = [inc for inc, s, d, r in INCIDENTS if s - 5 <= a <= s + d + 60]
            if not owner or all(b["per_incident"][o] < significant for o in owner):
                needless += 1
        missed = [inc for inc, *_ in INCIDENTS if b["per_incident"][inc] >= significant and not per[inc]["detected"]]
        rows.append({"rule": name, "pages": len(tiers["page"]), "tickets": len(tiers.get("ticket", [])),
                     "per_incident": per, "needless": needless, "missed": missed,
                     "minutes_paging": int(page.sum())})
    step = 60
    return {"rules": rows, "budget": {"per_incident": b["per_incident"], "used_hourly": b["used"][::step].tolist(),
                                      "final": float(b["used"][-1])},
            "incidents": [{"name": n, "start_min": s, "minutes": d, "rate": r, "burn": r / (1 - slo)}
                          for n, s, d, r in INCIDENTS],
            "rate_hourly": (np.add.reduceat(m["err"], np.arange(0, MONTH_MIN, step))
                            / np.add.reduceat(m["req"], np.arange(0, MONTH_MIN, step))).tolist(),
            "slo": slo, "thresholds": thresholds(slo)}
