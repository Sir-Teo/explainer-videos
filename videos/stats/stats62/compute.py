"""Precompute every number in Part 62 of *Statistics, Built* ("Frontiers of Causal Inference").

    OMP_NUM_THREADS=1 python -m videos.stats.stats62.compute            # everything missing (a few minutes)
    python -m videos.stats.stats62.compute --force board

Results are cached in ``.cache/stats62/<name>.json``.  The NSW job-training data are the Museum's; everything else is a
seeded simulation.

Items:
    frontdoor    a hidden confounder of A and Y, a mediator M: naive, back-door-impossible, front-door estimates
    msm          NSW against PSID: the IPW estimate and its marginal-sensitivity bounds against the experiment
    proximal     two proxies of a hidden confounder: naive adjustment against proximal 2SLS (coverage)
    interference a random geometric network: exposure-based Hajek contrasts against the naive difference
    policy       empirical welfare maximization with AIPW scores: in-sample against cross-fitted policy values
    dtr          a two-stage SMART: Q-learning's regime against static regimes, valued from the true model
    discovery    random linear SEMs: the PC skeleton, varsortability, and what standardizing does to it
    fusion       a trial younger than its target: the trial ATE, the transported ATE, the target's truth
    surrogate    the surrogate index under its assumption and when the treatment bypasses the surrogates
    board        Coverage Board rows
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import causal as C
from . import checked as F

CACHE = Cache("stats62")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def nest(obj):
    if isinstance(obj, np.ndarray):
        return nest(obj.tolist())
    if isinstance(obj, dict):
        return {str(k): nest(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [nest(v) for v in obj]
    if isinstance(obj, (np.floating, float)):
        v = float(obj)
        return v if math.isfinite(v) else None
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    return obj


def compute_frontdoor():
    r = rng(6201)
    n = 20000
    U = r.random(n) < 0.5
    A = r.random(n) < np.where(U, 0.8, 0.2)
    M = r.random(n) < np.where(A, 0.75, 0.25)
    Y = 2.0 * M + 3.0 * U + r.standard_normal(n)
    # truth: E[Y | do(a)] = 2 P(M = 1 | a) + 3 P(U = 1) -> ATE = 2 (0.75 - 0.25) = 1
    naive = float(Y[A].mean() - Y[~A].mean())
    fd = F.front_door(Y, A, M)
    g = C.DAG([("U", "A"), ("U", "Y"), ("A", "M"), ("M", "Y")])
    return {"n": n, "truth": 1.0, "naive": naive, "fd": fd["ate"], "frontdoor_ok": F.frontdoor_ok(g, "A", "Y", ["M"]),
            "backdoor_empty": g.backdoor_ok("A", "Y", [])}


def _nsw_psid():
    d = museum.nsw()
    m = (d["sample"] == "psid") | ((d["sample"] == "experiment") & (d["treat"] == 1))
    X = np.column_stack([d[k][m] for k in ("age", "educ", "black", "hisp", "married", "nodegree")] + [d["re74"][m] / 1e4, d["re75"][m] / 1e4])
    e = d["sample"] == "experiment"
    exp = float(d["re78"][e & (d["treat"] == 1)].mean() - d["re78"][e & (d["treat"] == 0)].mean())
    return X, d["treat"][m], d["re78"][m], exp


def compute_msm():
    from scipy import optimize
    X,t,y,experiment=_nsw_psid()
    def design(X):
        Z=(X-X.mean(0))/X.std(0)
        return np.column_stack([Z,Z[:,6]**2,Z[:,7]**2,Z[:,0]**2])
    def fit(X,t):
        raw,residual=F.propensity(design(X),t)
        return np.clip(raw,.01,.99),residual,float(np.mean((raw<.01)|(raw>.99)))
    ps,residual,clipped=fit(X,t);lams=[1.,1.25,1.5,1.75,2.,2.5,3.]
    rows=[]
    for lam in lams:
        bound=F.msm_bounds(y,t,ps,lam)
        rows.append(dict(lam=lam,lo=bound['ate_lo'],hi=bound['ate_hi']))
    r=rng(6209);arms=[np.flatnonzero(t==a) for a in (0,1)];bootstrap=[];bootstrap_residual=[]
    for _ in range(200):
        idx=np.r_[*[r.choice(group,len(group),replace=True) for group in arms]]
        e,res,_=fit(X[idx],t[idx]);bootstrap_residual.append(res)
        bounds=[F.msm_bounds(y[idx],t[idx],e,lam) for lam in lams]
        bootstrap.append([[b['ate_lo'],b['ate_hi']] for b in bounds])
    bootstrap=np.asarray(bootstrap)
    for k,row in enumerate(rows):
        row['bootstrap_outer_95']=[float(np.quantile(bootstrap[:,k,0],.025)),float(np.quantile(bootstrap[:,k,1],.975))]
    def tipping(target):
        function=lambda lam:F.msm_bounds(y,t,ps,lam)['ate_hi']-target
        return float(optimize.brentq(function,1,3)) if function(1)*function(3)<=0 else None
    return dict(n1=int((t==1).sum()),n0=int((t==0).sum()),naive=float(y[t==1].mean()-y[t==0].mean()),
        ipw=rows[0]['lo'],exp=experiment,rows=rows,ps_t=ps[t==1],ps_c=ps[t==0],
        propensity_score_residual=residual,propensity_clipped_fraction=clipped,
        tipping_zero=tipping(0),tipping_experimental_estimate=tipping(experiment),
        bootstrap_draws=bootstrap,bootstrap_reps=200,bootstrap_score_residual_max=max(bootstrap_residual),
        scope='exact relaxed finite Hajek weight-box bounds; 200 treatment-stratified bootstrap resamples refit feature scaling and logistic propensity; not sharp population Tan bounds or a finite-sample causal ATE certificate')


def compute_proximal():
    r=rng(6202);reps,n=600,1000
    en,ep,sn,sp,hn,hp,first,partial,condition=[],[],[],[],[],[],[],[],[]
    for _ in range(reps):
        U=r.standard_normal(n);Z=U+r.standard_normal(n);W=U+r.standard_normal(n)
        A=(.8*U+r.standard_normal(n)>0).astype(float);Y=A+2*U+r.standard_normal(n)
        naive=F.ols_adjusted(Y,A,np.c_[Z,W]);prox=F.proximal_2sls(Y,A,Z,W)
        en.append(naive['effect']);ep.append(prox['effect']);sn.append(naive['se']);sp.append(prox['se'])
        hn.append(abs(naive['effect']-1)<=1.96*naive['se']);hp.append(abs(prox['effect']-1)<=1.96*prox['se'])
        first.append(prox['first_stage_robust_f']);partial.append(prox['first_stage_partial_r2']);condition.append(prox['projected_condition'])
    return dict(reps=reps,n=n,truth=1.,cov_naive=float(np.mean(hn)),cov_prox=float(np.mean(hp)),
        est_naive=en,est_prox=ep,se_naive=sn,se_prox=sp,mean_naive=float(np.mean(en)),mean_prox=float(np.mean(ep)),
        sd_naive=float(np.std(en,ddof=1)),sd_prox=float(np.std(ep,ddof=1)),
        mcse_cov_naive=F.mcse(hn),mcse_cov_prox=F.mcse(hp),mcse_mean_naive=F.mcse(en),mcse_mean_prox=F.mcse(ep),
        first_stage_robust_f=first,first_stage_partial_r2=partial,projected_condition=condition,
        scope='correct linear bridge, independent measurement noises and outcome error; asymptotic HC1 normal intervals')


def compute_interference():
    r=rng(6203);n,p=400,.3;pos=r.random((n,2))
    D=np.sqrt(((pos[:,None]-pos[None])**2).sum(-1));adj=((D<.06)&(D>0)).astype(int)
    pi=F.exposure_probs(adj,p);isolated=adj.sum(1)==0
    y0=r.standard_normal(n);reps=300;out={k:[] for k in ['direct','spill','total','naive']}
    target=np.where(isolated,2,3)
    for _ in range(reps):
        z=(r.random(n)<p).astype(int);e=F.exposures(z,adj)
        y=y0+2*z+((adj@z)>0)+.5*r.standard_normal(n)
        contrasts=F.exposure_hajek(y,z,adj,pi)
        for k in ['direct','spill']:out[k].append(contrasts[k])
        out['total'].append(F.exposure_ht_contrast(y,e,pi,target))
        out['naive'].append(float(y[z==1].mean()-y[z==0].mean()))
    z=(r.random(n)<p).astype(int)
    return dict(n=n,p=p,pos=pos,edges=np.argwhere(np.triu(adj)),z=z,exposure=F.exposures(z,adj),
        deg=float(adj.sum(1).mean()),frac_isolated=float(isolated.mean()),reps=reps,pi=pi,
        direct_eligible=n,spill_eligible=int((~isolated).sum()),truth_total=float(3-isolated.mean()),
        **out,mean={k:float(np.mean(v)) for k,v in out.items()},sd={k:float(np.std(v,ddof=1)) for k,v in out.items()},
        mcse={k:F.mcse(v) for k,v in out.items()},
        scope='exact Bernoulli probabilities; direct common support all units, spillover nonisolates; global all-treated versus none HT; variation over assignment and fresh outcome noise')


def _policy_once(r,n):
    # Fit nuisances on independent auxiliary outcomes, so learning cannot see evaluation outcomes.
    xa=r.uniform(-1,1,n);ta=(r.random(n)<.5).astype(float)
    ya=xa+ta*(.25*xa-.1)+r.standard_normal(n)
    models={a:np.polyfit(xa[ta==a],ya[ta==a],1) for a in (0,1)}
    x=r.uniform(-1,1,n);t=(r.random(n)<.5).astype(float)
    y=x+t*(.25*x-.1)+r.standard_normal(n)
    G=F.aipw_scores(y,t,np.polyval(models[0],x),np.polyval(models[1],x),.5)
    idx=r.permutation(n)
    return x,G,idx[:n//2],idx[n//2:]


def _true_value(rule):
    return F.uniform_policy_gain(rule)


def compute_policy():
    r=rng(6204);reps,n=800,400
    hn,hs,gn,gs,en,es,vn,vs,sn,ss=[],[],[],[],[],[],[],[],[],[]
    for _ in range(reps):
        x,G,A,B=_policy_once(r,n);rule=F.ewm_threshold(x,G)
        values=G*F.apply_rule(x,rule);estimate=values.mean();se=values.std(ddof=1)/np.sqrt(n);truth=_true_value(rule)
        hn.append(abs(estimate-truth)<=1.96*se);gn.append(estimate-truth);en.append(estimate);vn.append(truth);sn.append(se)
        ru=F.ewm_threshold(x[A],G[A]);values=G[B]*F.apply_rule(x[B],ru)
        estimate=values.mean();se=values.std(ddof=1)/np.sqrt(len(B));truth=_true_value(ru)
        hs.append(abs(estimate-truth)<=1.96*se);gs.append(estimate-truth);es.append(estimate);vs.append(truth);ss.append(se)
    x,G,A,B=_policy_once(r,n);rule=F.ewm_threshold(x,G,directions=(1,))
    return dict(reps=reps,n=n,auxiliary_n=n,cov_naive=float(np.mean(hn)),cov_split=float(np.mean(hs)),
        gap_naive=float(np.mean(gn)),gap_split=float(np.mean(gs)),rule_c=rule['c'],rule_s=rule['s'],best=.0225,x=x,G=G,
        true_cut=.4,value_est=rule['value'],value_true=_true_value(rule),
        mcse_cov_naive=F.mcse(hn),mcse_cov_split=F.mcse(hs),mcse_gap_naive=F.mcse(gn),mcse_gap_split=F.mcse(gs),
        estimate_naive=en,estimate_split=es,truth_naive=vn,truth_split=vs,se_naive=sn,se_split=ss,
        scope='400 policy observations plus independent 400-outcome nuisance-training sample per run; known propensity .5; upper/lower threshold class for coverage; upper-only representative chart; random learned-policy gain target')


def compute_dtr():
    r=rng(6205);n=1000;X1=r.standard_normal(n);A1=(r.random(n)<.5).astype(float)
    X2=.5*X1+.8*A1*(X1>0)-.4*A1+r.standard_normal(n);A2=(r.random(n)<.5).astype(float)
    Y=X2+A2*(X2-.2)+.5*A1*X1+r.standard_normal(n)
    q=F.q_learning(X1,A1,X2,A2,Y)
    pol={'Q-learning':(q['rule1'],q['rule2']),
         'always treat':(lambda x:np.ones_like(x,bool),lambda x:np.ones_like(x,bool)),
         'never treat':(lambda x:np.zeros_like(x,bool),lambda x:np.zeros_like(x,bool)),
         'stage 2 only':(lambda x:np.zeros_like(x,bool),lambda x:x>.2),
         'oracle':(lambda x:x>0,lambda x:x>.2)}
    evaluation_n=200000;x=r.standard_normal(evaluation_n);noise=r.standard_normal(evaluation_n)
    draws={}
    for key,(first,second) in pol.items():
        a=first(x).astype(float);state=.5*x+.8*a*(x>0)-.4*a+noise
        draws[key]=state+second(state)*(state-.2)+.5*a*x
    return dict(n=n,b1=q['b1'],b2=q['b2'],values={k:float(v.mean()) for k,v in draws.items()},
        value_mcse={k:F.mcse(v) for k,v in draws.items()},evaluation_n=evaluation_n,
        oracle_difference_mcse={k:F.mcse(v-draws['oracle']) for k,v in draws.items()},
        scope='one fitted regime; full-history stage-two Q; linear working stage-one Q; common fresh simulation states with conditional-mean outcomes for value integration')


def compute_discovery():
    r = rng(6206)
    rows = []
    for _ in range(30):
        s = F.random_linear_sem(10, 0.3, r, 2000)
        if not np.any(s["B"]):
            continue
        pc = F.pc_skeleton(s["X"], 0.01, None)
        true = (s["B"] != 0) | (s["B"].T != 0)
        tp = int(np.sum(pc["adj"] & true) // 2)
        fp = int(np.sum(pc["adj"] & ~true) // 2)
        fn = int(np.sum(~pc["adj"] & true) // 2)
        Xs = (s["X"] - s["X"].mean(0)) / s["X"].std(0)
        rows.append({"edges": int(true.sum() // 2), "tp": tp, "fp": fp, "fn": fn, "vs": F.varsortability(s["X"], s["B"]),
                     "vs_std": F.varsortability(Xs, s["B"])})
    # faithfulness: a cancelling pair of paths X -> Y directly and X -> M -> Y
    n = 5000
    Xc = r.standard_normal(n)
    Mc = 1.0 * Xc + r.standard_normal(n)
    Yc = 1.0 * Xc - 1.0 * Mc + r.standard_normal(n)
    corr = float(np.corrcoef(Xc, Yc)[0, 1])
    return {"rows": rows, "vs": float(np.mean([q["vs"] for q in rows])), "vs_std": float(np.mean([q["vs_std"] for q in rows])),
            "recall": float(np.sum([q["tp"] for q in rows]) / np.sum([q["edges"] for q in rows])),
            "precision": float(np.sum([q["tp"] for q in rows]) / max(1, np.sum([q["tp"] + q["fp"] for q in rows]))), "cancel_corr": corr}


def compute_fusion():
    r=rng(6207);N=20000;age=r.uniform(20,80,N);tau=.05*(age-20)
    selection=.15*np.exp(-(age-20)/15);reps=200
    tr_est,tp_est,ess,truths,target_age,trial_age,trial_n=[],[],[],[],[],[],[]
    for _ in range(reps):
        selected=r.random(N)<selection;tr=np.flatnonzero(selected)
        z=r.random(len(tr))<.5;y=1+.02*age[tr]+z*tau[tr]+r.standard_normal(len(tr))
        weight=(1-selection[tr])/selection[tr]
        tr_est.append(float(y[z].mean()-y[~z].mean()))
        tp_est.append(float(np.average(y[z],weights=weight[z])-np.average(y[~z],weights=weight[~z])))
        ess.append(float(weight.sum()**2/(weight@weight)))
        truths.append(float(tau[~selected].mean()));target_age.append(float(age[~selected].mean()))
        trial_age.append(float(age[tr].mean()));trial_n.append(len(tr))
    errors=np.asarray(tp_est)-truths
    return dict(n_trial=int(round(np.mean(trial_n))),mean_age_trial=float(np.mean(trial_age)),
        mean_age_target=float(np.mean(target_age)),reps=reps,trial=float(np.mean(tr_est)),trial_sd=float(np.std(tr_est,ddof=1)),
        transported=float(np.mean(tp_est)),transported_sd=float(np.std(tp_est,ddof=1)),ess=float(np.mean(ess)),
        truth=float(np.mean(truths)),target_truth_draws=truths,tr_est=tr_est,tp_est=tp_est,
        transport_error_mean=float(errors.mean()),transport_error_mcse=F.mcse(errors),mcse_trial=F.mcse(tr_est),mcse_transport=F.mcse(tp_est),
        scope='oracle known selection odds; target is the finite nonparticipant population in that run, not entire baseline pool; target and trial randomization/outcome draws recorded')


def compute_surrogate():
    r = rng(6208)

    def world(n, t, bypass):
        S1 = 0.5 * t + r.standard_normal(n)
        S2 = 0.3 * t + 0.5 * S1 + r.standard_normal(n)
        Y = 2 * S1 + 1 * S2 + bypass * t + r.standard_normal(n)
        return np.column_stack([S1, S2]), Y
    out = {}
    for name, bypass in (("valid", 0.0), ("bypass", -1.0)):
        to = (r.random(5000) < 0.5).astype(float)  # observational sample with long-term outcomes (no treatment info used)
        So, Yo = world(5000, np.zeros(5000), bypass)
        te = (r.random(2000) < 0.5).astype(float)
        Se, Ye = world(2000, te, bypass)
        si = F.surrogate_index(So, Yo, Se, te)
        truth = 2 * 0.5 + 1 * (0.3 + 0.5 * 0.5) + bypass
        out[name] = {"est": si["effect"], "se": si["se"], "truth": truth,"index_fit_variance":si["index_fit_variance"],"trial_variance":si["trial_variance"],"scope":si["scope"]}
        del to
    return out


def compute_board():
    p = load("proximal")
    q = load("policy")
    rows = [Row(62, r"OLS adjusting for both proxies", r"hidden confounder, \ $n = 1{,}000$", "coverage", 0.95, p["cov_naive"], p["reps"],mc_se=p["mcse_cov_naive"]),
            Row(62, r"proximal 2SLS", r"hidden confounder, \ $n = 1{,}000$", "coverage", 0.95, p["cov_prox"], p["reps"],mc_se=p["mcse_cov_prox"]),
            Row(62, r"policy value, \ learned and evaluated in-sample", r"EWM, \ AIPW scores, \ $n = 400$", "coverage", 0.95, q["cov_naive"], q["reps"],mc_se=q["mcse_cov_naive"]),
            Row(62, r"policy value, \ learned on one half, \ evaluated on the other", r"EWM, \ AIPW scores, \ $n = 400$", "coverage", 0.95, q["cov_split"], q["reps"],mc_se=q["mcse_cov_split"])]
    save_rows(62, rows)
    return {"rows": [asdict(x) | {"verdict": x.verdict, "se": x.se} for x in rows]}


ITEMS = {
    "frontdoor": compute_frontdoor, "msm": compute_msm, "proximal": compute_proximal, "interference": compute_interference,
    "policy": compute_policy, "dtr": compute_dtr, "discovery": compute_discovery, "fusion": compute_fusion,
    "surrogate": compute_surrogate, "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
