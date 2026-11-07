"""Audited Part 62 causal demonstration kernels, with explicit identification scopes."""
from __future__ import annotations
import math
from itertools import combinations
import numpy as np
from scipy import special,stats
from explainer.stats.kit.frontier import *  # noqa: F403
from explainer.stats.kit import frontier as _legacy


def mcse(values):
    a=np.asarray(values,float)
    return float(a.std(ddof=1)/np.sqrt(len(a)))


def front_door(y,a,m):
    y,a,m=np.asarray(y,float),np.asarray(a),np.asarray(m)
    if y.shape!=a.shape or y.shape!=m.shape or not np.isfinite(y).all():raise ValueError('finite aligned data required')
    if not np.isin(a,[0,1]).all() or not np.isin(m,[0,1]).all():raise ValueError('binary treatment and mediator required')
    cells=np.array([[np.sum((a==av)&(m==mv)) for mv in (0,1)] for av in (0,1)])
    if np.any(cells==0):raise ValueError('front-door empirical formula requires all four cells')
    return _legacy.front_door(y,a,m)|dict(cells=cells,scope='empirical binary formula; causal interpretation requires front-door graph and positivity')


def msm_bounds(y,t,ps,lam):
    y,t,ps=np.asarray(y,float),np.asarray(t),np.asarray(ps,float)
    if y.shape!=t.shape or y.shape!=ps.shape or not np.isfinite(y).all() or not np.isfinite(ps).all():raise ValueError('finite aligned data required')
    if lam<1 or not np.isfinite(lam) or np.any(ps<=0) or np.any(ps>=1):raise ValueError('Lambda >= 1 and strict propensity overlap required')
    if set(np.unique(t))!={0,1}:raise ValueError('both binary treatment arms required')
    return _legacy.msm_bounds(y,t,ps,lam)|dict(scope='exact finite Hajek weight-box extrema; relaxed bounds, not sharp population Tan identified set')


def _ols(y,X):
    y,X=np.asarray(y,float),np.asarray(X,float);n,p=X.shape
    if n<=p or np.linalg.matrix_rank(X)<p:raise ValueError('full-rank design and positive residual degrees of freedom required')
    bread=np.linalg.inv(X.T@X);b=np.linalg.lstsq(X,y,rcond=None)[0];residual=y-X@b
    V=bread@((X*residual[:,None]**2).T@X)@bread*n/(n-p)
    return dict(b=b,V=V,se=np.sqrt(np.maximum(np.diag(V),0)),residual=residual)


def tsls(y,X,Z):
    """Project on the instrument column space without an n-by-n matrix."""
    y,X,Z=np.asarray(y,float),np.asarray(X,float),np.asarray(Z,float)
    U,s,_=np.linalg.svd(Z,full_matrices=False)
    Q=U[:,s>np.finfo(float).eps*max(Z.shape)*s.max()]
    Xh=Q@(Q.T@X);n,p=X.shape
    if n<=p or np.linalg.matrix_rank(Xh)<p:raise ValueError('projected regressors are not identified')
    bread=np.linalg.inv(Xh.T@Xh);b=bread@(Xh.T@y);e=y-X@b
    V=bread@((Xh*e[:,None]**2).T@Xh)@bread*n/(n-p)
    return dict(b=b,se=np.sqrt(np.maximum(np.diag(V),0)),V=V,
                projected_condition=float(np.linalg.cond(Xh)),instrument_rank=Q.shape[1],covariance='HC1')


def proximal_2sls(y,a,z,w,X=None):
    y,a,z,w=(np.asarray(v,float) for v in (y,a,z,w));n=len(y)
    z=z[:,None] if z.ndim==1 else z;w=w[:,None] if w.ndim==1 else w
    cov=np.empty((n,0)) if X is None else np.asarray(X,float)
    if cov.ndim==1:cov=cov[:,None]
    base=np.column_stack([np.ones(n),a,cov]);Xd=np.column_stack([base,w]);Zd=np.column_stack([base,z])
    result=tsls(y,Xd,Zd)
    diagnostics={}
    if w.shape[1]==z.shape[1]==1:
        first=_ols(w[:,0],Zd);restricted=w[:,0]-base@np.linalg.lstsq(base,w[:,0],rcond=None)[0]
        diagnostics=dict(first_stage_robust_f=float((first['b'][-1]/first['se'][-1])**2),
            first_stage_partial_r2=float(1-np.sum(first['residual']**2)/np.sum(restricted**2)))
    return dict(effect=float(result['b'][1]),se=float(result['se'][1]),**diagnostics,
                projected_condition=result['projected_condition'],scope='correct linear bridge, proxy exclusions/completeness, latent exchangeability and overlap; HC1 asymptotic interval')


def ols_adjusted(y,a,covs):
    covs=np.asarray(covs,float);covs=covs[:,None] if covs.ndim==1 else covs
    result=_ols(y,np.column_stack([np.ones(len(y)),a,covs]))
    return dict(effect=float(result['b'][1]),se=float(result['se'][1]))


def exposure_probs(adj,p,rng=None,reps=None):
    """Exact probabilities for independent Bernoulli assignment, including zeros."""
    adj=np.asarray(adj)
    if not 0<p<1 or adj.ndim!=2 or adj.shape[0]!=adj.shape[1] or np.any(np.diag(adj)):
        raise ValueError('loop-free adjacency and Bernoulli p in (0,1) required')
    degree=(adj!=0).sum(1);q=(1-p)**degree
    return np.column_stack([(1-p)*q,(1-p)*(1-q),p*q,p*(1-q)])


def exposure_hajek(y,z,adj,pi):
    y,pi=np.asarray(y,float),np.asarray(pi,float);e=exposures(z,adj)
    def contrast(k,j):
        eligible=(pi[:,k]>0)&(pi[:,j]>0)
        if not eligible.any():return math.nan,0
        def mean(exposure):
            selected=eligible&(e==exposure)
            if not selected.any():return math.nan
            w=1/pi[selected,exposure]
            return float(w@y[selected]/w.sum())
        return mean(k)-mean(j),int(eligible.sum())
    direct,nd=contrast(2,0);spill,ns=contrast(1,0);total,nt=contrast(3,0)
    return dict(direct=direct,spill=spill,total=total,eligible=dict(direct=nd,spill=ns,total=nt),
                scope='each Hajek contrast uses its common positive-probability population')


def exposure_ht_contrast(y,e,pi,target,baseline=0):
    y,e,pi,target=np.asarray(y,float),np.asarray(e,int),np.asarray(pi,float),np.asarray(target,int)
    if target.ndim==0:target=np.full(len(y),int(target))
    pt=pi[np.arange(len(y)),target];pb=pi[:,baseline]
    if np.any(pt<=0) or np.any(pb<=0):raise ValueError('target exposures must have positive design probability')
    return float(np.mean((e==target)*y/pt-(e==baseline)*y/pb))


def ewm_threshold(x,gamma,directions=(1,-1)):
    x,g=np.asarray(x,float),np.asarray(gamma,float)
    if x.shape!=g.shape or not len(x) or not np.isfinite([x,g]).all():raise ValueError('finite aligned scores and covariates required')
    order=np.argsort(x);xs,gs=x[order],g[order]
    starts=np.r_[0,np.flatnonzero(np.diff(xs)>0)+1,len(xs)]
    cuts=np.r_[xs[starts[:-1]],np.inf];prefix=np.r_[0,np.cumsum(gs)];best=(-np.inf,None,None)
    for k,cut in zip(starts,cuts):
        for direction in directions:
            if direction not in (-1,1):raise ValueError('threshold directions must be +1 or -1')
            total=prefix[-1]-prefix[k] if direction==1 else prefix[k]
            if total>best[0]:best=(total,float(cut),direction)
    result=dict(value=float(best[0]/len(x)),c=best[1],s=best[2])
    if not np.isclose(policy_value(g,apply_rule(x,result)),result['value'],atol=1e-12):raise RuntimeError('threshold optimizer returned an unrealizable rule')
    return result


def uniform_policy_gain(rule):
    """Exact gain for X~Uniform[-1,1], tau(X)=.25 X-.1."""
    cut=float(np.clip(rule['c'],-1,1));lo,hi=(cut,1.) if rule['s']==1 else (-1.,cut)
    return float(.0625*(hi*hi-lo*lo)-.05*(hi-lo))


def q_learning(X1,A1,X2,A2,Y):
    """Full observed stage-two history; linear working regression at stage one."""
    X1,A1,X2,A2,Y=(np.asarray(v,float) for v in (X1,A1,X2,A2,Y));n=len(Y)
    history=np.column_stack([np.ones(n),X1,A1,A1*X1,X2])
    b2=np.linalg.lstsq(np.column_stack([history,A2,A2*X2]),Y,rcond=None)[0]
    optimum=history@b2[:5]+np.maximum(b2[5]+b2[6]*X2,0)
    b1=np.linalg.lstsq(np.column_stack([np.ones(n),X1,A1,A1*X1]),optimum,rcond=None)[0]
    return dict(b1=b1,b2=b2,rule1=lambda x:b1[2]+b1[3]*np.asarray(x)>0,
                rule2=lambda x:b2[5]+b2[6]*np.asarray(x)>0,
                scope='correct full-history stage-two model; stage-one linear working Q model may be misspecified')


def pc_skeleton(X,alpha=.01,max_cond=None):
    """PC-stable skeleton, considering neighbors from either endpoint."""
    X=np.asarray(X,float);n,p=X.shape;C=np.corrcoef(X.T)
    if n<=p+3 or not np.isfinite(C).all():raise ValueError('nondegenerate covariates and sufficient Gaussian sample required')
    adj=np.ones((p,p),bool);np.fill_diagonal(adj,False);sep={};tested=0
    maximum=p-2 if max_cond is None else min(max_cond,p-2)
    for k in range(maximum+1):
        snapshot=adj.copy();removals=[];eligible=False
        for i in range(p):
            for j in range(i+1,p):
                if not snapshot[i,j]:continue
                seen=set()
                for endpoint,other in [(i,j),(j,i)]:
                    nb=[v for v in range(p) if snapshot[endpoint,v] and v!=other]
                    if len(nb)>=k:eligible=True
                    for S in combinations(nb,k):
                        if S in seen:continue
                        seen.add(S);tested+=1
                        if fisher_z_indep(C,i,j,S,n)>alpha:
                            removals.append((i,j,S));break
                    else:continue
                    break
        for i,j,S in removals:adj[i,j]=adj[j,i]=False;sep[(i,j)]=S
        if not eligible:break
    return dict(adj=adj,sep=sep,conditional_tests=tested,max_conditioning=maximum,
                truncated=max_cond is not None and max_cond<p-2,
                scope='skeleton only; Gaussian Fisher-z approximations, causal sufficiency/Markov/faithfulness required')


def varsortability(X,B,tol=1e-9):
    """Match the cited paper's Boolean reachability-by-length implementation."""
    v=np.var(X,axis=0);E=np.asarray(B)!=0;Ek=E.copy()
    if np.any(v<=0):raise ValueError('positive marginal variances required')
    ratio=v[None,:]/v[:,None];total=correct=0.
    for _ in range(len(v)-1):
        total+=Ek.sum()
        correct+=np.sum(Ek&(ratio>1+tol))+.5*np.sum(Ek&(np.abs(ratio-1)<=tol))
        Ek=Ek@E  # Boolean matrix multiplication, as in the published implementation.
    return float(correct/total) if total else math.nan


def surrogate_index(S_obs,Y_obs,S_exp,t_exp):
    """Two-independent-sample delta SE, including fitted-index uncertainty."""
    So,Se=np.asarray(S_obs,float),np.asarray(S_exp,float)
    So=So[:,None] if So.ndim==1 else So;Se=Se[:,None] if Se.ndim==1 else Se
    t=np.asarray(t_exp,int)
    if set(np.unique(t))!={0,1} or min(np.sum(t==0),np.sum(t==1))<2:
        raise ValueError('two experiment observations per treatment arm required')
    fit=_ols(Y_obs,np.column_stack([np.ones(len(So)),So]));beta=fit['b'];slope=beta[1:]
    delta=Se[t==1].mean(0)-Se[t==0].mean(0)
    covariance=np.atleast_2d(np.cov(Se[t==1].T,ddof=1))/np.sum(t==1)+np.atleast_2d(np.cov(Se[t==0].T,ddof=1))/np.sum(t==0)
    trial_variance=float(slope@covariance@slope)
    index_variance=float(delta@fit['V'][1:,1:]@delta)
    return dict(effect=float(delta@slope),se=math.sqrt(max(0.,trial_variance+index_variance)),b=beta,
                trial_variance=trial_variance,index_fit_variance=index_variance,
                scope='independent training/experiment samples; linear-index HC1 two-sample delta approximation; surrogate/comparability assumptions required')


def _logit(X,y,lam=1e-3,iters=80):
    """Penalized logistic fit with backtracking and a checked score residual."""
    X,y=np.asarray(X,float),np.asarray(y,float)
    penalty=np.r_[0.,np.ones(X.shape[1]-1)]*lam
    b=np.zeros(X.shape[1])
    objective=lambda b:float(np.logaddexp(0,X@b).sum()-y@(X@b)+.5*np.sum(penalty*b*b))
    value=objective(b)
    for _ in range(iters):
        p=special.expit(X@b)
        gradient=X.T@(p-y)+penalty*b
        H=(X*(p*(1-p))[:,None]).T@X+np.diag(penalty)
        step=np.linalg.solve(H,gradient)
        if np.max(np.abs(gradient))<1e-8:
            return dict(beta=b,H=H,prob=p,score_residual=float(np.max(np.abs(gradient))))
        fraction=1.
        while fraction>2**-30:
            candidate=b-fraction*step;new=objective(candidate)
            if new<=value-1e-4*fraction*float(gradient@step)+1e-12:break
            fraction/=2
        if fraction<=2**-30:raise RuntimeError("logistic line search failed")
        b,value=candidate,new
    raise RuntimeError("logistic fit did not converge")


def propensity(X,t,lam=1e-6):
    X=np.asarray(X,float);fit=_logit(np.column_stack([np.ones(len(X)),X]),t,lam)
    return fit["prob"],fit["score_residual"]
