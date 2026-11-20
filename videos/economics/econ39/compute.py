"""Precompute every number in Part 39 of *Economics, Built* ("The Wage Structure").

    python -m videos.economics.econ39.compute            # everything missing (about a minute)
    python -m videos.economics.econ39.compute --force resume

Results are cached in ``.cache/econ39/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: Bertrand and Mullainathan's 4,870 resumes; Autor and Dorn's polarization files; FRED's
median weekly earnings by education and sex, the deciles, employment by education, the labour share and prime-age
employment; Wooldridge's union panel and the 1978/1985 CPS; the tables of Katz and Murphy, Card and Lemieux, Ciccone
and Peri, Autor, Goldin and Katz, Acemoglu and Restrepo, Card, Heining and Kline, Autor et al., the BLS's union
counts, Mas and Pallais, Goldin and Rouse, Quillian et al., Goldin, Kleven et al., Cullen and Pakzad-Hurson and
Leontief).  Models: Agora's labour, part II (``agora.labour``) with the Island's Part 39 truths.

Items:
    resume       the resumes: call-back rates by race, sex, city and quality, the ratio with an interval, names
    wages        the wage distribution: the college premium since 1979, the real median, the deciles since 2000,
                 Autor and Dorn's wage change by percentile, 1980-2005
    race         the canonical model: Katz and Murphy's elasticity, the naive refit on 1992-2025, the demand index
    polar        Autor and Dorn's employment change by percentile and the twelve occupation groups of the game
    tasks        the task model before and after machines take a band of middle tasks
    robots       robots across the Island's commuting zones: exposure, and the effect with and without a control
    firms        the Island's worker-firm economy: AKM against the truth, and the bias as mobility falls
    stars        superstars: earnings against talent at three reaches; the labour share (FRED)
    unions       the union premium, pooled and within workers; the compression of wages
    hedonic      the hedonic wage locus for risk
    theory       Becker's market gap against the share of unprejudiced employers; Phelps's pay lines
    oaxaca       the Oaxaca-Blinder decomposition of the gender gap, 1978 and 1985 (CPS)
    gender       women's to men's median weekly earnings since 1979; the child penalty on the Island
    leontief     Called it?: prime-age employment and the labour share since 1983
    film         the intermission's data film: the college premium, 1979-2025
    melody       its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import labour
from explainer.economics.data import tables

CACHE = Cache("econ39")
load = CACHE.load
TRUTH = island.truths(39)
FILM_SECONDS = 50.0
MELODY_SECONDS = FILM_SECONDS + 8.0
GAME = ("managers", "professionals", "financial sales", "retail sales", "clerical and administrative",
        "food preparation and service", "health service aides", "building and grounds", "child care",
        "precision production", "machine operators and assemblers", "transport and material moving")


def _annual(key: str, min_obs: int = 1) -> dict:
    d = data.fred(key)
    out: dict = {}
    for x, v in zip(d["date"], d["value"]):
        if np.isfinite(v):
            out.setdefault(int(x[:4]), []).append(v)
    return {y: float(np.mean(v)) for y, v in out.items() if len(v) >= min_obs}


def _a(D, k):
    return np.array(D[k], float)


def compute_resume() -> dict:
    R = data.resume()
    cb = _a(R, "received_callback")
    race, sex = np.array(R["race"]), np.array(R["gender"])
    city, qual = np.array(R["job_city"]), np.array(R["resume_quality"])
    W, B = race == "white", race == "black"

    def rate(m):
        return float(cb[m].mean()), int(m.sum()), int(cb[m].sum())
    rw, rb = rate(W), rate(B)
    ratio = rw[0] / rb[0]
    # the ratio's interval by the delta method on log rates (resumes as independent draws)
    se = np.sqrt((1 - rw[0]) / (rw[0] * rw[1]) + (1 - rb[0]) / (rb[0] * rb[1]))
    lo, hi = ratio * np.exp(-1.96 * se), ratio * np.exp(1.96 * se)
    # a two-proportion z test
    p = cb.mean()
    z = (rw[0] - rb[0]) / np.sqrt(p * (1 - p) * (1 / rw[1] + 1 / rb[1]))
    out = {"n": int(cb.size), "ads": int(len(set(R["job_ad_id"]))), "white": rw, "black": rb, "ratio": ratio,
           "lo": float(lo), "hi": float(hi), "z": float(z), "per_white": 1 / rw[0], "per_black": 1 / rb[0]}
    for nm, m in (("chicago", city == "Chicago"), ("boston", city == "Boston"), ("female", sex == "f"),
                  ("male", sex == "m"), ("high", qual == "high"), ("low", qual == "low")):
        out[nm] = {"white": rate(W & m)[0], "black": rate(B & m)[0]}
    # names: callbacks by first name, for the hook's cards
    names = {}
    for nm in sorted(set(R["firstname"])):
        m = np.array(R["firstname"]) == nm
        names[nm] = {"rate": float(cb[m].mean()), "n": int(m.sum()), "race": race[m][0], "sex": sex[m][0]}
    out["names"] = names
    return out


def compute_wages() -> dict:
    c, h, d = _annual("LEU0252918500A"), _annual("LEU0252917300A"), _annual("LEU0252916700A")
    ys = sorted(y for y in c if y in h)
    prem = [float(np.log(c[y] / h[y])) for y in ys]
    dropout = [float(np.log(h[y] / d[y])) for y in ys]
    real = _annual("LEU0252881600A")
    d1, d9, md = _annual("LEU0252911200A"), _annual("LEU0252911500A"), _annual("LEU0252881500A")
    yd = sorted(y for y in d1 if y in d9 and y in md)
    A = data.autor_dorn("pctile")
    prod = _annual("OPHNFB", 4)
    return {"prod_ratio": prod[2025] / prod[1979], "years": ys, "premium": prem,
            "ratio": [float(np.exp(v)) for v in prem], "dropout": dropout,
            "real_years": sorted(real), "real": [real[y] for y in sorted(real)],
            "dec_years": yd, "r9010": [d9[y] / d1[y] for y in yd], "r9050": [d9[y] / md[y] for y in yd],
            "r5010": [md[y] / d1[y] for y in yd],
            "pctile": A["pctile"], "dwage8005": A["dwage8005"], "dwage8090": A["dwage8090"],
            "dwage9000": A["dwage9000"], "dwage0005": A["dwage0005"],
            "prem1979": prem[0], "prem1992": prem[ys.index(1992)], "prem2025": prem[-1],
            "real1979": real[min(real)], "real2025": real[max(real)]}


def compute_race() -> dict:
    c, h = _annual("LEU0252918500A"), _annual("LEU0252917300A")
    nc, nh = _annual("LNU02027662", 11), _annual("LNU02027660", 11)
    ys = [y for y in range(1992, 2026) if y in c and y in nc and y in nh]
    w = np.array([np.log(c[y] / h[y]) for y in ys])
    n = np.array([np.log(nc[y] / nh[y]) for y in ys])
    naive = labour.katz_murphy(w, n, ys)
    K = tables.KM_1992.data
    S = tables.SIGMA_SKILL.data
    out = {"years": ys, "premium": w.tolist(), "supply": n.tolist(), "naive": naive, "km": K, "sigmas": S}
    for nm, sig in (("d141", K["sigma"]), ("d25", S["cl"])):
        D = labour.implied_demand(w, n, sig)
        out[nm] = D.tolist()
        rates = {}
        for a, b in ((1992, 2000), (2000, 2010), (2010, 2025)):
            ia, ib = ys.index(a), ys.index(b)
            rates[f"{a}-{b}"] = float((D[ib] - D[ia]) / (b - a))
        out[nm + "_rates"] = rates
    out["supply_rate"] = float((n[-1] - n[0]) / (ys[-1] - ys[0]))
    # the race, for the diagram: ln(premium) = D - S / sigma, with supply S rising steadily and the demand index D
    # rising fast for twenty years and then slowly
    t = np.arange(0, 41)
    sup = 0.03 * t
    dem = np.where(t < 20, 0.035 * t, 0.035 * 20 + 0.012 * (t - 20))
    out["sim"] = {"t": t.tolist(), "supply": sup.tolist(), "demand": dem.tolist(),
                  "premium": (dem - sup / K["sigma"]).tolist()}
    return out


def _smooth(x, y, bw: float = 9.0):
    x, y = np.asarray(x, float), np.asarray(y, float)
    out = []
    for x0 in x:
        w = np.exp(-0.5 * ((x - x0) / bw) ** 2)
        X = np.column_stack([np.ones_like(x), x - x0])
        b = np.linalg.solve(X.T @ (X * w[:, None]), X.T @ (w * y))
        out.append(b[0])
    return np.array(out)


def compute_polar() -> dict:
    A = data.autor_dorn("pctile")
    p = _a(A, "pctile")
    d = _a(A, "emp2005") - _a(A, "emp1980")
    d90, d00 = _a(A, "emp1990") - _a(A, "emp1980"), _a(A, "emp2000") - _a(A, "emp1990")
    O = data.autor_dorn("occ")
    codes = _a(O, "occ1990dd").astype(int)
    groups = {}
    for g in GAME:
        ix = [k for k, cc in enumerate(codes) if data.occ_group(int(cc)) == g]
        s80 = float(np.nansum(_a(O, "sh_empl1980")[ix]))
        s05 = float(np.nansum(_a(O, "sh_empl2005")[ix]))
        w80 = np.array(O["avg_hrwage1980"], float)[ix]
        wt = _a(O, "sh_empl1980")[ix]
        ok = np.isfinite(w80) & np.isfinite(wt)
        rti = _a(O, "rti1980")[ix]
        okr = np.isfinite(rti) & np.isfinite(wt)
        groups[g] = {"s1980": s80, "s2005": s05, "change": s05 / s80 - 1,
                     "wage1980": float(np.average(w80[ok], weights=wt[ok])),
                     "rti": float(np.average(rti[okr], weights=wt[okr]))}
    order = sorted(GAME, key=lambda g: groups[g]["change"])
    return {"pctile": p.tolist(), "d8005": d.tolist(), "smooth": _smooth(p, d).tolist(),
            "smooth8090": _smooth(p, d90).tolist(), "smooth9000": _smooth(p, d00).tolist(),
            "routine": A["routine_share1980"], "groups": groups, "order": order, "game": list(GAME),
            "dwage8005": A["dwage8005"], "wsmooth": _smooth(p, _a(A, "dwage8005")).tolist(),
            "low": float(np.mean(d[:20])), "mid": float(np.mean(d[30:70])), "high": float(np.mean(d[80:]))}


def compute_tasks() -> dict:
    T = TRUTH["tasks"]
    kw = {k: T[k] for k in ("L", "M", "H", "beta")}
    before, after = labour.task_model(**kw), labour.task_model(**kw, auto=T["auto"])
    return {"before": before, "after": after, **T}


def compute_robots() -> dict:
    R = TRUTH["robots"]
    return {**labour.robot_zones(**R), "ar": tables.AR_2020.data, **{k: v for k, v in R.items() if k != "beta"}}


def compute_firms() -> dict:
    F = TRUTH["firms"]
    E = labour.worker_firm_economy(**F)
    A = labour.akm(E["y"], E["firm"])
    tr = E["truth"]
    sweep = []
    for mv in (0.005, 0.01, 0.02, 0.05, 0.10, 0.20):
        Ei = labour.worker_firm_economy(**{**F, "move": mv})
        Ai = labour.akm(Ei["y"], Ei["firm"])
        sweep.append({"move": mv, "movers": Ei["movers"], "var_psi": Ai["var_psi"], "corr": Ai["corr"],
                      "true_var_psi": Ei["truth"]["var_psi"], "true_corr": Ei["truth"]["corr"]})
    # one worker's wage at two firms, for the picture: the highest-alpha mover
    firm, y = E["firm"], E["y"]
    # a worker who moved exactly once, between firms whose premiums differ most
    once = np.flatnonzero([len(set(r)) == 2 for r in firm])
    i = int(once[np.argmax(np.abs(E["psi"][firm[once, -1]] - E["psi"][firm[once, 0]]))])
    return {"truth": tr, "est": {k: A[k] for k in ("var_alpha", "var_psi", "cov2", "corr", "share_psi",
                                                    "share_alpha", "share_cov")},
            "var_y": float(y.var()), "movers": E["movers"], "sweep": sweep,
            "worker": {"y": y[i].tolist(), "firm": firm[i].tolist(), "psi": E["psi"][firm[i]].tolist(),
                       "alpha": float(E["alpha"][i])},
            "psi_true": E["psi"][:200].tolist(), "psi_hat": (A["psi"][:200] - A["psi"].mean() + E["psi"].mean()
                                                             ).tolist(),
            "chk": tables.CHK_2013.data, **F}


def compute_stars() -> dict:
    S = TRUTH["stars"]
    st = labour.superstars(**S)
    ls = _annual("PRS85006173", 4)
    ys = sorted(ls)
    return {**st, "ls_years": ys, "labour_share": [ls[y] for y in ys], "ls1980": ls[1980], "ls2025": ls[2025],
            "ls1947": ls[1947], **{k: v for k, v in S.items() if k != "reach"}}


def compute_unions() -> dict:
    W = data.wooldridge("wagepan")
    y, u = _a(W, "lwage"), _a(W, "union")
    yr = _a(W, "year")
    ex, ex2, mar = _a(W, "exper"), _a(W, "expersq"), _a(W, "married")
    ed, bl, hi = _a(W, "educ"), _a(W, "black"), _a(W, "hisp")
    yd = [(yr == t).astype(float) for t in range(1981, 1988)]
    one = np.ones_like(y)
    pooled = labour.ols(y, np.column_stack([one, u, ex, ex2, mar, ed, bl, hi, *yd]))
    fe = labour.within(y, np.column_stack([u, ex2, mar, *yd]), _a(W, "nr"))
    C = data.wooldridge("cps78_85")
    cy, cu, cyr = _a(C, "lwage"), _a(C, "union"), _a(C, "year")
    by = {}
    for t in (78, 85):
        m = cyr == t
        X = np.column_stack([np.ones(m.sum()), cu[m], _a(C, "educ")[m], _a(C, "exper")[m], _a(C, "expersq")[m],
                             _a(C, "female")[m], _a(C, "nonwhite")[m], _a(C, "south")[m]])
        r = labour.ols(cy[m], X)
        by[str(t)] = {"premium": r["b"][1], "se": r["se"][1], "share": float(cu[m].mean()),
                      "sd_union": float(cy[m & (cu == 1)].std()), "sd_non": float(cy[m & (cu == 0)].std())}
    raw = float(y[u == 1].mean() - y[u == 0].mean())
    # densities of log wages in 1985, union and non-union (Gaussian kernels, Silverman's bandwidth)
    grid = np.linspace(0.0, 3.6, 121)
    m85 = cyr == 85
    dens = {}
    for nm, mm in (("union", m85 & (cu == 1)), ("non", m85 & (cu == 0))):
        v = cy[mm]
        h = 1.06 * v.std() * v.size ** -0.2
        dens[nm] = (np.exp(-0.5 * ((grid[:, None] - v[None, :]) / h) ** 2).sum(1) / (v.size * h * np.sqrt(2 * np.pi))
                    ).tolist()
    return {"pooled": pooled["b"][1], "pooled_se": pooled["se"][1], "fe": fe["b"][0], "fe_se": fe["se"][0],
            "raw": raw, "n_men": int(len(set(W["nr"]))), "n": int(len(y)), "share": float(u.mean()),
            "cps": by, "bls": tables.UNIONS.data, "grid": grid.tolist(), "dens": dens}


def compute_hedonic() -> dict:
    H = TRUTH["hedonic"]
    return {**labour.hedonic(**H), "mp": tables.MAS_PALLAIS_2017.data}


def compute_theory() -> dict:
    B, P = TRUTH["becker"], TRUTH["phelps"]
    shares = np.linspace(0.0, 0.3, 61)
    gaps = [labour.becker(B["share_minority"], s, d_scale=B["d_scale"])["gap"] for s in shares]
    ex = labour.becker(B["share_minority"], 0.05, d_scale=B["d_scale"])
    s = np.linspace(-3, 3, 61)
    ph = labour.phelps(s, sd_q=P["sd_q"], sd_noise=P["sd_noise"])
    return {"shares": shares.tolist(), "gaps": gaps, "example": ex, "signal": s.tolist(),
            "pay0": ph[0]["pay"], "pay1": ph[1]["pay"], "lam0": ph[0]["lam"], "lam1": ph[1]["lam"], **B, **P}


def compute_oaxaca() -> dict:
    C = data.wooldridge("cps78_85")
    out = {}
    for t in (78, 85):
        m = _a(C, "year") == t
        f = _a(C, "female") == 1

        def X(mm):
            return np.column_stack([np.ones(mm.sum()), *(_a(C, k)[mm] for k in ("educ", "exper", "expersq", "union",
                                                                                  "nonwhite", "married", "south"))])
        r = labour.oaxaca(_a(C, "lwage")[m & ~f], X(m & ~f), _a(C, "lwage")[m & f], X(m & f))
        out[str(t)] = {"gap": r["gap"], "explained": r["explained"], "unexplained": r["unexplained"],
                       "by": r["by_variable"], "n_men": int((m & ~f).sum()), "n_women": int((m & f).sum())}
    out["vars"] = ["constant", "schooling", "experience", "experience squared", "union", "nonwhite", "married",
                   "south"]
    return out


def compute_gender() -> dict:
    m, w = _annual("LEU0252881900A"), _annual("LEU0252882800A")
    ys = sorted(y for y in m if y in w)
    ratio = [w[y] / m[y] for y in ys]
    C = TRUTH["child"]
    cp = labour.child_penalty(**C)
    return {"years": ys, "ratio": ratio, "r1979": ratio[0], "r2025": ratio[-1],
            "r_max": max(ratio), "y_max": ys[int(np.argmax(ratio))], "child": cp, "kls": tables.GENDER.data}


def compute_leontief() -> dict:
    e = _annual("LNS12300060", 12)
    ls = _annual("PRS85006173", 4)
    ys = sorted(y for y in e if y >= 1983)
    return {"epop_years": ys, "epop": [e[y] for y in ys], "epop1983": e[1983], "epop2025": e[2025] if 2025 in e
            else e[max(ys)], "ls1983": ls[1983], "ls2025": ls[2025]}


def film_time(t: float, first: float = 1979.0, last: float = 2025.0) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    W = compute_wages()
    ys, r = W["years"], W["ratio"]
    k = int(np.argmax(r))
    return {"t": ys, "v": r, "times": [film_time(y) for y in ys], "peak": r[k], "peak_y": ys[k], "first": r[0],
            "last": r[-1], "y1992": r[ys.index(1992)]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["v"])
    times = f["times"]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=8, log=False, low=42, high=84)
    events = {"film_end": film_time(2025) + 6.0, "first": times[0], "peak": film_time(f["peak_y"])}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.5, "hz": score.hz(nn), "name": f"{x:.2f}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "the median weekly earnings of full-time college graduates over those of high-school "
                               "graduates, 1979-2025 (BLS, via FRED), as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ39").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "resume": compute_resume,
    "wages": compute_wages,
    "race": compute_race,
    "polar": compute_polar,
    "tasks": compute_tasks,
    "robots": compute_robots,
    "firms": compute_firms,
    "stars": compute_stars,
    "unions": compute_unions,
    "hedonic": compute_hedonic,
    "theory": compute_theory,
    "oaxaca": compute_oaxaca,
    "gender": compute_gender,
    "leontief": compute_leontief,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
