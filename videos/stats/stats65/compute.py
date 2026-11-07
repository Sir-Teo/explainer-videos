"""Precompute every number in Part 65 of *Statistics, Built* ("The Dissertation").

    OMP_NUM_THREADS=1 python -m videos.stats.stats65.compute            # everything missing (several minutes)
    python -m videos.stats.stats65.compute --force board

Results are cached in ``.cache/stats65/<name>.json``. This is a post hoc corrected rerun of the historical
protocol, with a separately committed QA amendment. The NHANES application is independent IID resampling
from fixed empirical source/target laws, not national survey inference.

Items:
    bound      the theorem's lower bound for tempered Gaussian-tilt weights, against the temper lambda
    pilot      a small pilot run, used only to check the code and the Monte Carlo error (not the results)
    study      the protocol-guided corrected study: 3 shifts x 3 heteroscedasticities x 5 methods, 1,000 replicates per cell
    nhanes     the application: blood pressure intervals under designed empirical covariate shift
    fullboard  every Coverage Board row of the degree, summarized
    board      Coverage Board rows
"""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import asdict

import numpy as np

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, load_all, save_rows
from . import checked as T
from pathlib import Path
import hashlib

CACHE = Cache("stats65")


def _board_parts():
    return {n for n in range(1, 66)
            if 'save_rows(' in Path(f'videos/stats/stats{n}/compute.py').read_text()}


def _historical_inputs():
    return [p for p in sorted(Path(".cache").glob("stats*/board.json"))
            if int(p.parent.name[5:]) <= 65] + [Path(".cache/stats64/holdout.json")]


def load(name):
    data = CACHE.load(name)
    if name == "fullboard":
        records = data.get("input_hashes", [])
        stale = not records or {r["file"] for r in records} != {str(p) for p in _historical_inputs()}
        stale |= bool(_board_parts() - {r["part"] for r in data.get("rows", [])})
        for record in records:
            path = Path(record["file"])
            stale |= not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != record["sha256"]
        if stale:
            raise RuntimeError("Cached full Board is stale or incomplete; run "
                               "python -m videos.stats.stats65.compute --force fullboard")
    return data

MUS = [0.5, 1.0, 1.5]
GAMMAS = [0.0, 0.5, 1.0]
METHODS = ["none", "oracle", "estimated", "tempered", "misspecified"]
ALPHA = 0.1


def rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def nest(obj):
    if isinstance(obj, dict):
        return {k: nest(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [nest(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return nest(obj.tolist())
    if isinstance(obj, (np.floating,)):
        return float(obj) if math.isfinite(float(obj)) else None
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, float) and not math.isfinite(obj):
        return None
    return obj


def compute_bound():
    lam = np.linspace(0, 1.2, 121)
    return {"lam": lam, "alpha": ALPHA, "curves": {str(mu): [T.coverage_bound(ALPHA, mu, l) for l in lam] for mu in MUS}}


def compute_pilot():
    r = rng(6501)
    res = T.study([1.0], [0.5], METHODS, 50, 500, 500, ALPHA, r)
    return {"rows": res, "reps": 50}


def compute_study():
    r = rng(6502)
    res = T.study(MUS, GAMMAS, METHODS, 1000, 500, 500, ALPHA, r)
    return {"rows": res, "reps": 1000, "n_cal": 500, "n_tgt": 500, "n_test": 200, "alpha": ALPHA}


def _fit(X, y):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    return b


def _design(age, bmi):
    a, m = (age - 50) / 15, (bmi - 28) / 6
    return np.column_stack([np.ones(len(a)), a, a * a, m, a * m])


def compute_nhanes():
    d=museum.nhanes();raw=np.column_stack([d['sbp1'],d['sbp2'],d['sbp3']]);counts=np.isfinite(raw).sum(1)
    sbp=np.divide(np.nansum(raw,axis=1),counts,out=np.full(len(counts),np.nan),where=counts>0)
    ok=np.isfinite(sbp)&np.isfinite(d['bmi'])&np.isfinite(d['age']);age,bmi,y=d['age'][ok].astype(float),d['bmi'][ok].astype(float),sbp[ok]
    N=len(y);pi=T.selection_probs(age);ps=pi/pi.sum();pt=(1-pi)/(1-pi).sum();n_selected=int(round(pi.sum()));ntr=n_selected//2;nca=n_selected-ntr
    r=rng(6503);methods=['none','oracle','estimated'];out={m:[] for m in methods};widths={m:[] for m in methods};inf={m:[] for m in methods};by_age={m:{'lo':[],'hi':[]} for m in methods}
    ess,wmax={m:[] for m in methods[1:]},{m:[] for m in methods[1:]};corr=[];tv=[];scores=[]
    F=np.column_stack([np.ones(N),(age-50)/15,((age-50)/15)**2,(bmi-28)/6])
    for _ in range(200):
        tr=r.choice(N,ntr,replace=True,p=ps);ca=r.choice(N,nca,replace=True,p=ps)
        auxs=r.choice(N,1000,replace=True,p=ps);auxt=r.choice(N,1000,replace=True,p=pt)
        test=r.choice(N,3000,replace=True,p=pt)
        pred=_design(age,bmi)@_fit(_design(age[tr],bmi[tr]),y[tr]);res=abs(y[ca]-pred[ca])
        fit=T._logit(np.vstack([F[auxs],F[auxt]]),np.r_[np.zeros(1000),np.ones(1000)],lam=1e-6)
        wts={'none':None,'oracle':(1-pi)/pi,'estimated':np.exp(F@fit['beta'])}
        normalized=wts['estimated']*ps;normalized/=normalized.sum();tv.append(.5*sum(abs(normalized-pt)));scores.append(fit['score_residual'])
        corr.append(np.corrcoef(np.log(wts['oracle']),np.log(wts['estimated']))[0,1]);old=age[test]>=65
        for method,w in wts.items():
            if w is None:h=T.halfwidths(res,np.ones(nca),np.ones(len(test)),ALPHA)
            else:
                h=T.halfwidths(res,w[ca],w[test],ALPHA);wc=w[ca];ess[method].append(wc.sum()**2/(wc@wc));wmax[method].append(wc.max()/wc.sum())
            covered=abs(y[test]-pred[test])<=h;out[method].append(covered.mean());finite=np.isfinite(h);widths[method].append(np.median(2*h[finite]) if finite.any() else np.inf);inf[method].append(np.mean(~finite))
            by_age[method]['hi'].append(covered[old].mean());by_age[method]['lo'].append(covered[~old].mean())
    return dict(N=N,reps=200,mean_selected=n_selected,frac_old_pop=float(np.mean(age>=65)),frac_old_sel=float(ps@(age>=65)),frac_old_target=float(pt@(age>=65)),coverage={m:float(np.mean(v)) for m,v in out.items()},mcse={m:float(np.std(v,ddof=1)/np.sqrt(200)) for m,v in out.items()},width={m:float(np.mean(v)) for m,v in widths.items()},inf={m:float(np.mean(v)) for m,v in inf.items()},old={m:float(np.mean(v['hi'])) for m,v in by_age.items()},young={m:float(np.mean(v['lo'])) for m,v in by_age.items()},ess={m:float(np.mean(v)) for m,v in ess.items()},wmax={m:float(np.mean(v)) for m,v in wmax.items()},corr_logw=float(np.mean(corr)),n_cal=nca,n_train=ntr,n_aux_each=1000,n_test=3000,mean_tv=float(np.mean(tv)),bound=.9-float(np.mean(tv)),max_logistic_score=max(scores),scope='Fixed unweighted empirical NHANES population; source mass proportional to pi(age), target to 1-pi; independent IID draws with replacement for all five samples, conditional on the empirical table. Not national or without-replacement design coverage.')



def compute_fullboard():
    expected = _board_parts()
    rows = load_all(upto=65)
    missing=expected-{r.part for r in rows}
    if missing:raise RuntimeError(f'Cannot publish full Board: missing parts {sorted(missing)}')
    stage = lambda p: 1 if p <= 10 else 2 if p <= 20 else 3 if p <= 42 else 4 if p <= 55 else 5  # noqa: E731
    historical_inputs = _historical_inputs()
    out = {"n": len(rows), "parts": len({r.part for r in rows}), "verdict": Counter(r.verdict for r in rows),
           "kind": Counter(r.kind for r in rows),
           "holdout_reuse_accuracy": Cache("stats64").load("holdout")["reuse"]["holdout"][-1],
           "by_stage": {s: Counter(r.verdict for r in rows if stage(r.part) == s) for s in range(1, 6)},
           "input_hashes": [{"file":str(p),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in historical_inputs],
           "rows": [{"part": r.part, "method": r.method, "kind": r.kind, "nominal": r.nominal, "achieved": r.achieved,
                     "verdict": r.verdict, "reps": r.reps, "mc_se": r.se, "setting": r.setting} for r in rows]}
    return {k: (dict(v) if isinstance(v, Counter) else ({s: dict(c) for s, c in v.items()} if k == "by_stage" else v)) for k, v in out.items()}


def compute_board():
    st = {(x["mu"], x["gamma"], x["method"]): x for x in load("study")["rows"]}
    nh = load("nhanes")
    a, b = st[(1.0, 1.0, "none")], st[(1.0, 1.0, "estimated")]
    rows = [Row(65, r"split conformal, \ no weights, \ under shift", r"$\mu = 1$, \ $\gamma = 1$, \ $n = 500$", "coverage", 0.9, a["coverage"], 1000, mc_se=a["mcse"]),
            Row(65, r"weighted conformal, \ estimated weights", r"$\mu = 1$, \ $\gamma = 1$, \ $n = 500$", "coverage", 0.9, b["coverage"], 1000, mc_se=b["mcse"]),
            Row(65, r"NHANES blood pressure, \ no weights", r"a sample short of the old", "coverage", 0.9, nh["coverage"]["none"], nh["reps"], mc_se=nh["mcse"]["none"]),
            Row(65, r"NHANES blood pressure, \ estimated weights", r"a sample short of the old", "coverage", 0.9, nh["coverage"]["estimated"], nh["reps"], mc_se=nh["mcse"]["estimated"])]
    save_rows(65, rows)
    return {"rows": [asdict(x) | {"verdict": x.verdict, "se": x.se} for x in rows]}


ITEMS = {"bound": compute_bound, "pilot": compute_pilot, "study": compute_study, "nhanes": compute_nhanes,
         "board": compute_board, "fullboard": compute_fullboard}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
