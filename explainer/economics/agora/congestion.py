"""Agora's dissertation (Part 68): what New York's congestion charge did, from the MTA's open data, with the series'
methods, and the same study run on the Island where the truth is known.

* **Crossings** (:func:`crossings_panel`, :func:`yoy_did`): weekday traffic on the MTA's bridges and tunnels by week;
  the two tunnels that lead into the charging zone against eight crossings that do not, compared year on year month
  by month, so that seasons cancel; the years before the charge are placebos.
* **Buses and miles** (:func:`bus_speeds`, :func:`vmt`): bus speeds inside and outside the central business district,
  and miles driven in the zone against its excluded highways, year on year.
* **The clock** (:func:`time_rd`): weekday entries by ten-minute block; the toll falls at 9 pm and rises at 5 am, so
  entries jump at both, a regression discontinuity in time that measures retiming.
* **The model** (:func:`bpr_time`, :func:`congestion_model`, :func:`counterfactual`): a speed-flow curve (the Bureau
  of Public Roads form) calibrated to the change in miles and bus speeds, a constant-elasticity demand for trips
  calibrated to the change in miles and the toll, the marginal external cost of a trip and the toll that equals it,
  and the original $15 plan, with uncertainty carried through by simulation.
* **The Island** (:func:`island_study`): the same difference in differences on simulated crossings with a known
  effect, with and without traffic that diverts to the comparison crossings.

numpy only.
"""

from __future__ import annotations

import datetime as dt

import numpy as np

TREATED = (("Queens Midtown Tunnel", "Westbound to Manhattan"), ("Hugh L. Carey Tunnel", "Northbound to Manhattan"))
CONTROLS = (("Bronx - Whitestone Bridge", "Southbound to Queens"), ("Bronx - Whitestone Bridge", "Northbound to Bronx"),
            ("Throgs Neck Bridge", "Southbound to Queens"), ("Throgs Neck Bridge", "Northbound to Bronx"),
            ("Verrazzano - Narrows Bridge", "Westbound to Staten Island"),
            ("Robert F. Kennedy Bridge Bronx", "Southbound to Manhattan or Queens"),
            ("Robert F. Kennedy Bridge Bronx", "Northbound to Manhattan or Bronx"),
            ("Henry Hudson Bridge", "Southbound to Manhattan"), ("Henry Hudson Bridge", "Northbound to Bronx"),
            ("Cross Bay Bridge", "Northbound"), ("Cross Bay Bridge", "Southbound"),
            ("Marine Parkway Bridge", "Northbound to Brooklyn"), ("Marine Parkway Bridge", "Southbound to Queens"))
START = dt.date(2025, 1, 5)          # the charge began on Sunday 5 January 2025


def crossings_panel(D: dict) -> dict:
    """From :func:`explainer.economics.data.mta_crossings`: full weeks only, the average weekday vehicles of each
    facility-direction by week.  Returns ``{"weeks": [...], "series": {(facility, direction): array}}``."""
    weeks = sorted({w for w, n in zip(D["week"], D["days"]) if n == 7})
    idx = {w: k for k, w in enumerate(weeks)}
    series: dict = {}
    for w, f, d, v, n in zip(D["week"], D["facility"], D["direction"], D["weekday_vehicles"], D["days"]):
        if n != 7:
            continue
        series.setdefault((f, d), np.full(len(weeks), np.nan))[idx[w]] = v / 5.0
    return {"weeks": weeks, "series": series}


def _monthly(weeks, x):
    out: dict = {}
    for w, v in zip(weeks, x):
        if np.isfinite(v):
            out.setdefault(w[:7], []).append(v)
    return {m: float(np.mean(v)) for m, v in out.items()}


def yoy_did(P: dict, treated=TREATED, controls=CONTROLS, years=(2023, 2024, 2025, 2026)) -> dict:
    """Month by month, the year-on-year change in log weekday traffic of the treated crossings minus that of the
    controls (each group's traffic summed).  Months of 2025 compare the charge with the year before it; months of
    2023 and 2024 are placebos; months of 2026 compare two charged years.  Returns the monthly rows, the mean effect
    in 2025, the placebos' spread and a t-ratio against it."""
    def group(keys):
        tot = None
        for k in keys:
            m = _monthly(P["weeks"], P["series"][k])
            tot = m if tot is None else {mm: tot[mm] + m[mm] for mm in tot if mm in m}
        return tot

    T, C = group(treated), group(controls)
    rows = []
    for y in years:
        for mo in range(1, 13):
            a, b = f"{y}-{mo:02d}", f"{y - 1}-{mo:02d}"
            if all(k in T and k in C for k in (a, b)):
                rows.append({"month": a, "year": y, "treated": float(np.log(T[a] / T[b])),
                             "control": float(np.log(C[a] / C[b])),
                             "did": float(np.log(T[a] / T[b]) - np.log(C[a] / C[b]))})
    eff = np.array([r["did"] for r in rows if r["year"] == 2025])
    plc = np.array([r["did"] for r in rows if r["year"] in (2023, 2024)])
    se = float(plc.std(ddof=1) / np.sqrt(len(eff)))
    return {"rows": rows, "effect": float(eff.mean()), "n": len(eff), "placebo_mean": float(plc.mean()),
            "placebo_sd": float(plc.std(ddof=1)), "se": se,
            "t": float(eff.mean() / se) if se > 0 else float("inf"),
            "treated_level_2024": float(np.mean([T[f"2024-{m:02d}"] for m in range(1, 13)])),
            "after_2026": float(np.mean([r["did"] for r in rows if r["year"] == 2026])) if any(
                r["year"] == 2026 for r in rows) else None}


def bus_speeds(B: dict, day_type: str = "Weekday", period: str = "Peak") -> dict:
    """Monthly bus speed (miles over hours) inside and outside the central business district, and the year-on-year
    change in log speed inside minus outside (2024 a placebo, 2025 the charge's first year)."""
    sp: dict = {}
    for m, c, d, p, mi, h in zip(B["month"], B["cbd"], B["day_type"], B["period"], B["miles"], B["hours"]):
        if d == day_type and p == period:
            sp[(c, m)] = mi / h
    months = sorted({m for (_, m) in sp})
    rows = []
    for m in months:
        y, mo = int(m[:4]), m[5:]
        prev = f"{y - 1}-{mo}"
        if ("CBD", prev) in sp and ("Non-CBD", prev) in sp and ("CBD", m) in sp and ("Non-CBD", m) in sp:
            a = np.log(sp[("CBD", m)] / sp[("CBD", prev)])
            b = np.log(sp[("Non-CBD", m)] / sp[("Non-CBD", prev)])
            rows.append({"month": m, "year": y, "cbd": float(a), "non": float(b), "did": float(a - b)})
    eff = [r["did"] for r in rows if r["year"] == 2025]
    plc = [r["did"] for r in rows if r["year"] == 2024]
    return {"months": months, "cbd": [sp.get(("CBD", m)) for m in months],
            "non": [sp.get(("Non-CBD", m)) for m in months], "rows": rows, "effect": float(np.mean(eff)),
            "placebo": float(np.mean(plc)), "placebo_sd": float(np.std(plc, ddof=1)),
            "cbd_2024": float(np.mean([sp[("CBD", f"2024-{k:02d}")] for k in range(1, 13)])),
            "cbd_2025": float(np.mean([sp[("CBD", f"2025-{k:02d}")] for k in range(1, 13)]))}


def vmt(V: dict) -> dict:
    """Miles driven in the zone (CRZ) and on its excluded highways (ER), monthly from January 2024: the
    year-on-year change in 2025 for each, and the difference."""
    s = {(a, m): x for m, a, x in zip(V["month"], V["area"], V["vmt_gps"])}
    rows = []
    for mo in range(1, 13):
        a, b = f"2025-{mo:02d}", f"2024-{mo:02d}"
        if all((ar, mm) in s for ar in ("CRZ", "ER") for mm in (a, b)):
            z, e = np.log(s[("CRZ", a)] / s[("CRZ", b)]), np.log(s[("ER", a)] / s[("ER", b)])
            rows.append({"month": a, "crz": float(z), "er": float(e), "did": float(z - e)})
    months = sorted({m for (_, m) in s})
    return {"months": months, "crz": [s.get(("CRZ", m)) for m in months], "er": [s.get(("ER", m)) for m in months],
            "rows": rows, "crz_change": float(np.mean([r["crz"] for r in rows])),
            "er_change": float(np.mean([r["er"] for r in rows])), "did": float(np.mean([r["did"] for r in rows]))}


def time_rd(T: dict, at: float, width: float = 2.0, col: str = "cars") -> dict:
    """A regression discontinuity in time: log entries per weekday in ten-minute blocks, a line on each side of the
    hour ``at`` (21 or 5) within ``width`` hours, and the jump between them at ``at``.  Also the entries the left
    line predicts for the first hour after the cutoff, against those observed (the retimed trips)."""
    t = np.array(T["hour"]) + np.array(T["minute"]) / 60.0
    y = np.array(T[col], float) / T["weekdays"]
    order = np.argsort(t)
    t, y = t[order], y[order]
    left = (t >= at - width) & (t < at)
    right = (t >= at) & (t < at + width)
    bl = np.polyfit(t[left] - at, np.log(y[left]), 1)
    br = np.polyfit(t[right] - at, np.log(y[right]), 1)
    jump = float(br[1] - bl[1])
    hour = right & (t < at + 1)
    pred = np.exp(np.polyval(bl, t[hour] - at))
    return {"t": t.tolist(), "y": y.tolist(), "left": bl.tolist(), "right": br.tolist(), "jump": jump,
            "at": at, "extra_first_hour": float((y[hour] - pred).sum()), "observed_first_hour": float(y[hour].sum())}


def bpr_time(v, a: float = 0.15, b: float = 4.0):
    """Travel time per mile relative to free flow, 1 + a v^b, with v the flow over capacity (the Bureau of Public
    Roads form)."""
    v = np.asarray(v, float)
    return 1 + a * v ** b


def congestion_model(dlnV: float, dlnT: float, toll: float, vot: float, miles: float = 3.0, mph: float = 10.0,
                     other_cost: float = 25.0, b: float = 4.0) -> dict:
    """The smallest model that speaks to the estimates.  Time per trip in the zone T(V) = T0 (1 + a v^b), anchored
    at the observed speed ``mph`` over ``miles`` in the zone.  The observed change in time (dlnT, from bus speeds)
    against the change in traffic (dlnV, from miles driven) gives the elasticity of time with respect to traffic,
    e = dlnT/dlnV = b s, where s = a v^b / (1 + a v^b) is the share of the trip's time due to congestion.  Demand
    for trips has constant elasticity eta in the generalized price P = toll + vot x T + other costs; the observed
    fall in traffic with the toll and the faster trip pins down eta.  The marginal external cost of a trip, the
    delay it adds to every other trip, is V dT/dV x vot = e x T x vot."""
    T_old = miles / mph
    e_tv = dlnT / dlnV
    s_old = float(np.clip(e_tv / b, 1e-4, 0.95))
    av_b = s_old / (1 - s_old)
    T0 = T_old * (1 - s_old)
    T_new = T0 * (1 + av_b * np.exp(b * dlnV))
    P_old = vot * T_old + other_cost
    P_new = toll + vot * T_new + other_cost
    eta = dlnV / np.log(P_new / P_old)
    mec_old = vot * b * av_b * T0
    mec_new = vot * b * av_b * np.exp(b * dlnV) * T0
    return {"T0": T0, "T_old": T_old, "T_new": float(T_new), "s_old": s_old, "e_tv": e_tv, "eta": float(eta),
            "P_old": P_old, "P_new": float(P_new), "mec_old": float(mec_old), "mec_new": float(mec_new),
            "av_b": av_b, "b": b, "vot": vot, "miles": miles, "mph": mph, "other_cost": other_cost, "toll": toll}


def equilibrium(M: dict, toll: float) -> dict:
    """Traffic (relative to the uncharged level, in logs) and time per trip at a toll, from the calibrated model:
    solve ln V = eta ln(P(toll, T(V)) / P_old) by bisection."""
    def P(lnv):
        T = M["T0"] * (1 + M["av_b"] * np.exp(M["b"] * lnv))
        return toll + M["vot"] * T + M["other_cost"], T

    lo, hi = -3.0, 0.5
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        p, _ = P(mid)
        f = mid - M["eta"] * np.log(p / M["P_old"])
        lo, hi = (mid, hi) if f < 0 else (lo, mid)
    p, T = P(lo)
    mec = M["vot"] * M["b"] * M["av_b"] * np.exp(M["b"] * lo) * M["T0"]
    return {"lnV": float(lo), "T": float(T), "P": float(p), "mec": float(mec), "toll": toll}


def optimal_toll(M: dict) -> dict:
    """The toll equal to the marginal external cost of a trip at the traffic it produces (Pigou, Part 15)."""
    lo, hi = 0.0, 60.0
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        e = equilibrium(M, mid)
        lo, hi = (mid, hi) if mid < e["mec"] else (lo, mid)
    return equilibrium(M, lo)


def counterfactual(dlnV: float, dlnT: float, se_V: float, se_T: float, toll: float, new_toll: float,
                   vot=(14.0, 24.0), miles=(2.0, 5.0), other=(15.0, 40.0), mph: float = 10.0, draws: int = 2000,
                   seed: int = 68) -> dict:
    """The calibrated model at ``new_toll``, carrying both kinds of uncertainty: the two estimates are drawn from
    normal distributions with their standard errors, and the assumptions (the value of time, the miles driven in
    the zone, the other costs of a trip) uniformly from their ranges; the model is recalibrated each time.  Returns
    the 5th, 50th and 95th percentiles of the change in traffic and in time per trip at ``new_toll``, of the
    marginal external cost of a trip before the charge, and of the toll that would equal it."""
    rng = np.random.default_rng(seed)
    out = {"lnV": [], "dT": [], "mec": [], "opt": [], "eta": []}
    for _ in range(draws):
        dv = dlnV + se_V * rng.normal()
        dtt = dlnT + se_T * rng.normal()
        if dv >= -0.005 or dtt >= -0.001:
            continue
        M = congestion_model(dv, dtt, toll, rng.uniform(*vot), miles=rng.uniform(*miles), mph=mph,
                             other_cost=rng.uniform(*other))
        if not (M["eta"] < 0 and np.isfinite(M["eta"])):
            continue
        e = equilibrium(M, new_toll)
        out["lnV"].append(e["lnV"])
        out["dT"].append(e["T"] / M["T_old"] - 1)
        out["mec"].append(M["mec_old"])
        out["opt"].append(optimal_toll(M)["toll"])
        out["eta"].append(M["eta"])
    q = {k: [float(np.percentile(v, p)) for p in (5, 50, 95)] for k, v in out.items()}
    return {**q, "kept": len(out["lnV"]), "draws": draws}


def island_study(effect: float = -0.04, divert: float = 0.0, pretrend: float = 0.0, weeks: int = 208,
                 start: int = 104, n_ctrl: int = 8, sims: int = 400, seed: int = 680) -> dict:
    """The same year-on-year difference in differences on the Island's crossings, where the truth is known: two
    treated crossings and ``n_ctrl`` controls with a shared season, crossing-specific trends and noise; from week
    ``start`` the treated lose ``effect`` (log) of their traffic and a share ``divert`` of the lost trips shows up on
    the controls; ``pretrend`` is a drift of the treated crossings relative to the others (log points a year) that
    was there before the charge.  Returns the estimates' mean and spread over ``sims`` Islands, against the truth,
    with and without subtracting the year-before placebo."""
    rng = np.random.default_rng(seed)
    est = []
    w = np.arange(weeks)
    season = 0.08 * np.sin(2 * np.pi * w / 52)
    for _ in range(sims):
        base_t = 11 + rng.normal(0, 0.2, 2)
        base_c = 11 + rng.normal(0, 0.3, n_ctrl)
        trend = rng.normal(0.0, 0.0004, 2 + n_ctrl)
        common = np.cumsum(rng.normal(0, 0.004, weeks))
        lt = (base_t[:, None] + season + common + (trend[:2, None] + pretrend / 52) * w
              + rng.normal(0, 0.03, (2, weeks)))
        lc = base_c[:, None] + season + common + trend[2:, None] * w + rng.normal(0, 0.03, (n_ctrl, weeks))
        post = w >= start
        lost = np.exp(lt[:, post]).sum(0) * (1 - np.exp(effect))
        lt[:, post] += effect
        lc[:, post] = np.log(np.exp(lc[:, post]) + divert * lost / n_ctrl)
        T, C = np.exp(lt).sum(0), np.exp(lc).sum(0)
        d = (np.log(T[start:start + 52]) - np.log(T[start - 52:start])) - (
            np.log(C[start:start + 52]) - np.log(C[start - 52:start]))
        p = (np.log(T[start - 52:start]) - np.log(T[start - 104:start - 52])) - (
            np.log(C[start - 52:start]) - np.log(C[start - 104:start - 52]))
        est.append((float(d.mean()), float(d.mean() - p.mean())))
    est = np.array(est)
    return {"truth": effect, "divert": divert, "pretrend": pretrend, "mean": float(est[:, 0].mean()),
            "sd": float(est[:, 0].std(ddof=1)), "bias": float(est[:, 0].mean() - effect),
            "adjusted": float(est[:, 1].mean()), "adjusted_sd": float(est[:, 1].std(ddof=1))}


__all__ = [n for n in dir() if not n.startswith("_") and n not in ("np", "dt", "annotations")]
