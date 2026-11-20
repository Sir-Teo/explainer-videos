"""Precompute every number in Part 22 of *Economics, Built* ("Consumption and Saving").

    python -m videos.economics.econ22.compute            # everything missing (seconds)
    python -m videos.economics.econ22.compute --force buffer

Results are cached in ``.cache/econ22/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: FRED's monthly consumption by type, their price indexes, real disposable income and the
saving rate; the Penn World Table 11.0's consumption shares; the windfall studies, transcribed).  Models: Agora's
households (``agora.household``) and overlapping generations (``agora.olg``), with the Island's Part 22 truths.

Items:
    months       monthly US real consumption (all, and nondurables plus services), real disposable income, saving
    rebate       the summer of 2001: income, spending and saving, month by month; the mailing schedule
    playit       the game's options and its answer
    kuznets      the ratio of consumption to income over sixty years, and the Island's cross-section (Friedman)
    pih          the permanent-income household: a windfall's annuity; the life cycle's hump
    hall         Hall's test on US quarterly data: lagged income, time averaging, Campbell and Mankiw's instrument
    smooth       consumption against income growth; Deaton's paradox of excess smoothness
    rot          Campbell and Mankiw's rule-of-thumb economy on the Island, by OLS and IV
    buffer       the buffer-stock consumption function, with and without income risk; its MPC; its target
    mpc          the Island's 20,000 buffer-stock households: the MPC out of a month's windfall
    htm          the wealthy hand-to-mouth: MPC against net worth and against liquid wealth
    ricardo      a tax cut repaid in twenty years: Ricardian, buffer-stock and hand-to-mouth households
    olg          Diamond's economy: the transition map, steady states, a pay-as-you-go pension's welfare
    samuelson    Samuelson's consumption-loan economy: money as a social contract
    china        household consumption's share of GDP: China against the United States (PWT)
    film         the intermission's data film: income and spending, month by month, 1990-2026
    melody       its data melody: the saving rate
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import household as hh
from explainer.economics.agora import olg
from explainer.economics.data import tables

CACHE = Cache("econ22")
load = CACHE.load
TRUTH = island.truths(22)
STUDIES = tables.MPC_STUDIES.data


def _monthly():
    f = {k: np.array(data.fred(k)["value"], float) for k in ("PCE", "PCEPI", "PCEND", "PCES", "DNDGRG3M086SBEA",
                                                             "DSERRG3M086SBEA", "DSPIC96", "PSAVERT")}
    dates = data.fred("PCE")["date"]
    for k in ("PCEND", "PCES", "DSPIC96", "PSAVERT", "PCEPI"):
        assert data.fred(k)["date"] == dates, k
    C = f["PCE"] / f["PCEPI"] * 100
    CNS = f["PCEND"] / f["DNDGRG3M086SBEA"] * 100 + f["PCES"] / f["DSERRG3M086SBEA"] * 100
    return dates, C, CNS, f["DSPIC96"], f["PSAVERT"]


def compute_months() -> dict:
    dates, C, CNS, Y, s = _monthly()
    t = [int(d[:4]) + (int(d[5:7]) - 1) / 12 for d in dates]
    return {"dates": dates, "t": t, "C": C.tolist(), "CNS": CNS.tolist(), "Y": Y.tolist(), "saving": s.tolist(),
            "last": dates[-1], "retrieved": data.fred("PCE")["retrieved"]}


def _window(m, first, last):
    idx = [i for i, d in enumerate(m["dates"]) if first <= d[:7] <= last]
    return {k: [m[k][i] for i in idx] for k in ("dates", "t", "C", "CNS", "Y", "saving")}


def compute_rebate() -> dict:
    m = compute_months()
    w = _window(m, "2000-07", "2002-06")
    by = dict(zip(w["dates"], range(len(w["dates"]))))
    base_y = np.mean([w["Y"][by[f"2001-0{k}-01"]] for k in (4, 5, 6)])
    base_c = np.mean([w["CNS"][by[f"2001-0{k}-01"]] for k in (4, 5, 6)])
    extra = [w["Y"][by[f"2001-0{k}-01"]] - base_y for k in (7, 8, 9)]
    extra_c = [w["CNS"][by[f"2001-0{k}-01"]] - base_c for k in (7, 8, 9)]
    sav = {d[:7]: v for d, v in zip(w["dates"], w["saving"])}
    return {**w, "extra_income": extra, "extra_cns": extra_c, "extra_total": float(sum(extra) / 12),
            "base_y": float(base_y), "saving_june": sav["2001-06"], "saving_sept": sav["2001-09"],
            "saving_oct": sav["2001-10"], "digits": list(range(10)), "jps": STUDIES["jps"]}


def compute_playit() -> dict:
    opts = list(TRUTH["playit"]["options"])
    j = STUDIES["jps"]
    mid = (j["lo"] + j["hi"]) / 2
    answer = min(range(len(opts)), key=lambda i: abs(opts[i] - mid))
    return {"options": opts, "answer": answer, "jps": [j["lo"], j["hi"]],
            "parker2013": [STUDIES["parker2013"]["lo"], STUDIES["parker2013"]["hi"]],
            "parker2013_total": [STUDIES["parker2013"]["total_lo"], STUDIES["parker2013"]["total_hi"]],
            "pih_quarter": float(hh.pih(1.0, TRUTH["pih"]["r"])["share"] / 4)}


def compute_kuznets() -> dict:
    m = compute_months()
    years, ratio = [], []
    for y in range(1959, 2026):
        idx = [i for i, d in enumerate(m["dates"]) if int(d[:4]) == y]
        if len(idx) == 12:
            years.append(y)
            ratio.append(float(np.sum(np.array(m["C"])[idx]) / np.sum(np.array(m["Y"])[idx])))
    yr = {y: r for y, r in zip(years, ratio)}
    inc = {y: float(np.mean([m["Y"][i] for i, d in enumerate(m["dates"]) if int(d[:4]) == y])) for y in (1960, 2025)}
    pop = TRUTH["population"]
    fx = hh.friedman_cross_section(**pop)
    return {"years": years, "ratio": ratio, "ratio_1960": yr[1960], "ratio_2025": yr[2025],
            "ratio_min": float(min(ratio)), "ratio_max": float(max(ratio)),
            "income_growth": inc[2025] / inc[1960], "island": fx, "truth": pop}


def compute_pih() -> dict:
    p = TRUTH["pih"]
    w = hh.pih(1.0, p["r"])
    lc = hh.life_cycle(work=p["work"], retire=p["retire"], R=p["R"], beta=1 / p["R"], gamma=p["gamma"])
    lc_flat = hh.life_cycle(work=p["work"], retire=p["retire"], R=p["R"], beta=1 / p["R"], gamma=p["gamma"], hump=False)
    return {"r": p["r"], "share_year": w["share"], "share_quarter": w["share"] / 4, "life": lc, "flat": lc_flat}


def _quarterly():
    dates, C, CNS, Y, _ = _monthly()
    q = {}
    for d, c, y in zip(dates, CNS, Y):
        q.setdefault((int(d[:4]), (int(d[5:7]) - 1) // 3), []).append((c, y))
    keys = sorted(k for k in q if len(q[k]) == 3)
    Cq = np.array([np.mean([a for a, _ in q[k]]) for k in keys])
    Yq = np.array([np.mean([b for _, b in q[k]]) for k in keys])
    t = np.array([k[0] + k[1] / 4 for k in keys])
    return t, Cq, Yq


def _ols(y, X):
    X = np.column_stack([np.ones(len(y)), X])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b
    V = e @ e / (len(y) - X.shape[1]) * np.linalg.inv(X.T @ X)
    return b, V


def compute_hall() -> dict:
    """Hall's test on quarterly US nondurables and services, 1960-2019 (before the pandemic's swings).  Consumption
    growth regressed on income growth two to four quarters back (lag one is left out: quarterly averages of a monthly
    random walk have growth correlated with its own lag, Working's (1960) effect); then Campbell and Mankiw's
    instrumental-variable estimate of the share of income going to rule-of-thumb households."""
    t, Cq, Yq = _quarterly()
    dc, dy, tt = np.diff(np.log(Cq)), np.diff(np.log(Yq)), t[1:]
    idx = np.where((tt >= 1960) & (tt < 2020))[0]
    b, V = _ols(dc[idx], np.column_stack([dy[idx - 2], dy[idx - 3], dy[idx - 4]]))
    R = np.eye(4)[1:]
    F = float((R @ b) @ np.linalg.inv(R @ V @ R.T) @ (R @ b) / 3)
    b1, V1 = _ols(dc[idx], dc[idx - 1])
    m = 3
    working = (m * m - 1) / (2 * (2 * m * m + 1))
    # Campbell and Mankiw: dc on dy, instruments dy and dc at lags 2-4
    Z = np.column_stack([np.ones(len(idx)), dy[idx - 2], dy[idx - 3], dy[idx - 4], dc[idx - 2], dc[idx - 3],
                         dc[idx - 4]])
    x, y = dy[idx], dc[idx]
    xh = Z @ np.linalg.lstsq(Z, x, rcond=None)[0]
    X = np.column_stack([np.ones(len(idx)), xh])
    bi = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - np.column_stack([np.ones(len(idx)), x]) @ bi
    se_iv = float(np.sqrt(e @ e / (len(idx) - 2) * np.linalg.inv(X.T @ X)[1, 1]))
    rf = x - Z @ np.linalg.lstsq(Z, x, rcond=None)[0]
    r0 = x - x.mean()
    F1 = float(((r0 @ r0 - rf @ rf) / 6) / (rf @ rf / (len(x) - 7)))
    from scipy.stats import f as fdist

    return {"n": int(len(idx)), "first": float(tt[idx][0]), "last": float(tt[idx][-1]),
            "lags": b[1:].tolist(), "lag_se": np.sqrt(np.diag(V))[1:].tolist(), "F": F,
            "p": float(fdist.sf(F, 3, len(idx) - 4)), "F_crit_1pc": float(fdist.isf(0.01, 3, len(idx) - 4)),
            "own_lag": float(b1[1]), "own_lag_se": float(np.sqrt(V1[1, 1])), "working": working,
            "ols": float(np.polyfit(x, y, 1)[0]), "iv": float(bi[1]), "iv_se": se_iv, "first_F": F1}


def compute_smooth() -> dict:
    t, Cq, Yq = _quarterly()
    dc, dy, tt = np.diff(np.log(Cq)), np.diff(np.log(Yq)), t[1:]
    m = (tt >= 1960) & (tt < 2020)
    dates, C, CNS, Y, _ = _monthly()
    yrs = list(range(1959, 2026))
    Ca = np.array([np.mean([c for d, c in zip(dates, CNS) if int(d[:4]) == y]) for y in yrs])
    Ya = np.array([np.mean([v for d, v in zip(dates, Y) if int(d[:4]) == y]) for y in yrs])
    dca, dya = np.diff(np.log(Ca)), np.diff(np.log(Ya))
    ty = np.array(yrs[1:])
    k = (ty >= 1960) & (ty <= 2019)
    x = dya[k]
    phi, c0 = np.polyfit(x[:-1], x[1:], 1)
    e = x[1:] - (c0 + phi * x[:-1])
    r = TRUTH["pih"]["r"]
    pih_sd = float(e.std() / (1 - phi / (1 + r)))
    return {"t": tt[m].tolist(), "dc": dc[m].tolist(), "dy": dy[m].tolist(), "sd_dc_q": float(dc[m].std()),
            "sd_dy_q": float(dy[m].std()), "ratio_q": float(dc[m].std() / dy[m].std()),
            "years": ty[k].tolist(), "dca": dca[k].tolist(), "dya": dya[k].tolist(),
            "sd_dc_a": float(dca[k].std()), "sd_dy_a": float(dya[k].std()), "phi": float(phi),
            "sd_e": float(e.std()), "pih_sd": pih_sd, "corr_a": float(np.corrcoef(dca[k], dya[k])[0, 1])}


def compute_rot() -> dict:
    p = TRUTH["rule_of_thumb"]
    out = hh.rule_of_thumb(lam=p["lam"], T=p["T"], seed=p["seed"])
    reps = [hh.rule_of_thumb(lam=p["lam"], T=p["T"], seed=p["seed"] + k) for k in range(200)]
    out["ols_mean"] = float(np.mean([r["ols"] for r in reps]))
    out["iv_median"] = float(np.median([r["iv"] for r in reps]))
    out["iv_reps"] = [r["iv"] for r in reps]
    out["ols_reps"] = [r["ols"] for r in reps]
    return out


def compute_buffer() -> dict:
    b = TRUTH["buffer"]
    bs = hh.buffer_stock(**b)
    sure = hh.buffer_stock(**{**b, "perm_sd": 0.0, "tran_sd": 0.0, "p_zero": 0.0})
    m = np.array(bs["m"])
    at = {f"{x:g}": {"c": float(np.interp(x, m, bs["c"])), "mpc": float(np.interp(x, m, bs["mpc"]))}
          for x in (0.5, 1.0, 1.5, 2.0, 3.0, 5.0)}
    einv = 1.0  # E[1/psi] is close to one; the scenes draw the 45-degree target line from the module's own target
    del einv
    return {"m": bs["m"], "c": bs["c"], "mpc": bs["mpc"], "target": bs["target"], "c_target": bs["c_target"],
            "sure_c": sure["c"], "at": at, "impatience": bs["impatience"], "iterations": bs["iterations"],
            "params": bs["params"], "m_grid": bs["m_grid"], "c_grid": bs["c_grid"]}


def compute_mpc() -> dict:
    b = TRUTH["buffer"]
    p = TRUTH["mpc"]
    bs = hh.buffer_stock(**b)
    out = hh.simulate_mpc(bs, n=p["n"], windfall=p["windfall"], seed=p["seed"])
    out["pih_year"] = float(hh.pih(p["windfall"], TRUTH["pih"]["r"])["share"])
    return out


def compute_htm() -> dict:
    b = TRUTH["buffer"]
    i = TRUTH["illiquid"]
    renter = hh.buffer_stock(**b)
    owner = hh.buffer_stock(**{**b, "beta": b["beta"] * b["R"] / i["R_h"]})
    out = hh.hand_to_mouth(renter, owner, n=TRUTH["mpc"]["n"], own=i["own"], median=i["median"], sd=i["sd"],
                           short=i["short"], seed=i["seed"])
    out["beta_owner"] = b["beta"] * b["R"] / i["R_h"]
    out["mpc_curve"] = {"m": renter["m"], "renter": renter["mpc"], "owner": owner["mpc"]}
    out["kvw"] = STUDIES["kvw"]
    return out


def compute_ricardo() -> dict:
    """A tax cut of a month's income now, financed by debt and repaid with interest in twenty years.  A household that
    will pay the later tax (or whose heirs will, and who cares about them) is no richer: it saves the cut.  The Island's
    buffer-stock households spend their MPC of it at once, and owners short of cash more."""
    rc = TRUTH["ricardo"]
    later = rc["cut"] * (1 + rc["r"]) ** rc["years"]
    pv = later / (1 + rc["r"]) ** rc["years"]
    h = compute_htm()
    return {"cut": rc["cut"], "later": later, "pv_later": pv, "years": rc["years"], "r": rc["r"],
            "spent": {"Ricardian": 0.0, "buffer-stock renters": h["mpc_renters"], "the Island, all": h["mpc_all"],
                      "short of cash": h["mpc_short"]}}


def compute_olg() -> dict:
    o = TRUTH["olg"]
    kw = {"alpha": o["alpha"], "n": o["n"], "A": o["A"]}
    out = {"n": o["n"], "alpha": o["alpha"], "A": o["A"], "economies": []}
    for beta in o["betas"]:
        st = olg.diamond_steady(beta=beta, **kw)
        pw = olg.pension_welfare(o["pensions"], beta=beta, **kw)
        ks = np.linspace(0.02, 2.2 * max(st["k"], st["k_gold"]), 120)
        nxt = [olg.diamond_step(k, o["alpha"], beta, o["n"], o["A"]) for k in ks]
        path = olg.diamond_path(0.2 * st["k"], 8, beta=beta, **kw)["k"]
        best = int(np.argmax(pw["utility"]))
        out["economies"].append({"beta": beta, "steady": st, "welfare": pw, "map_k": ks.tolist(), "map_next": nxt,
                                 "path": path, "best_d": pw["d"][best],
                                 "annual_beta": beta ** (1 / 30), "annual_R": st["R"] ** (1 / 30) - 1})
    out["annual_n"] = (1 + o["n"]) ** (1 / 30) - 1
    return out


def compute_samuelson() -> dict:
    o = TRUTH["olg"]
    return olg.samuelson_money(n=o["n"], beta=o["betas"][0])


def compute_china() -> dict:
    rows = {c: {int(r["year"]): r for r in data.pwt(c)} for c in ("CHN", "USA", "JPN", "KOR", "IND", "DEU")}
    years = list(range(1970, 2020))
    out = {"years": years}
    for c, rs in rows.items():
        out[c] = {"csh_c": [float(rs[y]["csh_c"]) for y in years], "csh_i": [float(rs[y]["csh_i"]) for y in years]}
    ch = rows["CHN"]
    out["chn_1990"] = float(ch[1990]["csh_c"])
    out["chn_2010"] = float(ch[2010]["csh_c"])
    out["chn_2019"] = float(ch[2019]["csh_c"])
    out["usa_2019"] = float(rows["USA"][2019]["csh_c"])
    out["chn_min_year"] = int(years[int(np.argmin(out["CHN"]["csh_c"]))])
    out["chn_min"] = float(min(out["CHN"]["csh_c"]))
    return out


FILM_SECONDS = 40.0
MELODY_SECONDS = FILM_SECONDS + 8.0
FILM_FIRST, FILM_LAST = 1990.0, 2026.75


def film_time(t: float) -> float:
    return 1.5 + FILM_SECONDS * (t - FILM_FIRST) / (FILM_LAST - FILM_FIRST)


def compute_film() -> dict:
    m = compute_months()
    idx = [i for i, t in enumerate(m["t"]) if t >= FILM_FIRST]
    t = [m["t"][i] for i in idx]
    base_y, base_c = m["Y"][idx[0]], m["CNS"][idx[0]]
    events = [(2001.5, r"2001: rebate cheques"), (2008.33, r"2008: stimulus payments"),
              (2020.25, r"2020--21: three rounds of payments, \ and lockdown")]
    return {"t": t, "Y": [m["Y"][i] / base_y for i in idx], "C": [m["CNS"][i] / base_c for i in idx],
            "saving": [m["saving"][i] for i in idx], "times": [film_time(x) for x in t],
            "events": [{"t": a, "say": b, "time": film_time(a)} for a, b in events], "last": m["last"],
            "peak_saving": float(max(m["saving"][i] for i in idx)),
            "peak_when": m["dates"][idx[int(np.argmax([m["saving"][i] for i in idx]))]]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    t = np.array(f["t"])
    s = np.array(f["saving"])
    qs = np.arange(FILM_FIRST, t[-1] + 1e-9, 0.25)
    vals = np.interp(qs, t, s)
    times = [film_time(x) for x in qs]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=5, log=False, low=45, high=86)
    events = {"film_end": film_time(FILM_LAST) + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.2, "hz": score.hz(nn), "name": f"{x:.2f}"}
                       for tt, nn, x in zip(times, mel["notes"], qs)],
                meta={"label": "the US personal saving rate, quarter by quarter, 1990-2026 (BEA via FRED), as a tune "
                               "(computed)", "kind": "synthesized"})
    ClipStore("econ22").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "quarters": qs.tolist(), "seconds": MELODY_SECONDS}


ITEMS = {
    "months": compute_months,
    "rebate": compute_rebate,
    "playit": compute_playit,
    "kuznets": compute_kuznets,
    "pih": compute_pih,
    "hall": compute_hall,
    "smooth": compute_smooth,
    "rot": compute_rot,
    "buffer": compute_buffer,
    "mpc": compute_mpc,
    "htm": compute_htm,
    "ricardo": compute_ricardo,
    "olg": compute_olg,
    "samuelson": compute_samuelson,
    "china": compute_china,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
