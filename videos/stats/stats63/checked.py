"""Audited kernels for Part 63. Privacy uses fixed-size replace-one adjacency."""
from explainer.stats.kit.privacy import *  # noqa: F401,F403
import numpy as np
from scipy import special, stats
import math


def gaussian_delta(sigma, sensitivity, eps):
    if sigma <= 0 or sensitivity < 0 or eps < 0: raise ValueError("invalid Gaussian parameters")
    if sensitivity == 0: return 0.0
    a=sensitivity/(2*sigma); b=eps*sigma/sensitivity
    log1=special.log_ndtr(a-b); log2=eps+special.log_ndtr(-a-b)
    return float(np.exp(log1)*(-np.expm1(min(0.,log2-log1))))


def rdp_gaussian_eps(sensitivity,sigma,k,delta,alphas=None):
    rho=k*sensitivity**2/(2*sigma**2)
    if alphas is None: return zcdp_to_dp(rho,delta)
    a=np.asarray(alphas); return float(np.min(rho*a+np.log(1/delta)/(a-1)))


def private_proportion(x,eps,rng,alpha=.05):
    x=np.asarray(x)
    if not len(x) or not np.isin(x,[0,1]).all() or eps<=0:raise ValueError("binary data and positive budget required")
    n=len(x); raw=(x.sum()+rng.laplace(0,1/eps))/n
    plug=np.clip(raw,0,1); z=stats.norm.ppf(1-alpha/2)
    vn=max(plug*(1-plug),1e-12)/n
    a=z*np.sqrt(vn); b=z*np.sqrt(vn+2/(n*eps)**2)
    return dict(p=raw,naive=(raw-a,raw+a),aware=(raw-b,raw+b))


def mean_mse_central_local(n,eps,reps,rng,p=.3):
    # Binomial sufficient statistics give exactly the original marginal experiments.
    c=rng.binomial(n,p,reps); ec=(c+rng.laplace(0,1/eps,reps))/n-p
    keep=special.expit(eps); q=(1-keep)+(2*keep-1)*p
    el=(rng.binomial(n,q,reps)/n-(1-keep))/(2*keep-1)-p
    out={}
    for name,error in [('central',ec),('local',el)]:
        sq=error**2;out[name]=float(sq.mean());out[name+'_mcse']=float(sq.std(ddof=1)/np.sqrt(reps))
    out['local_exact']=p*(1-p)/n+np.exp(eps)/(n*np.expm1(eps)**2)
    return out


def integer_total_projection(noisy,total):
    if total<0 or int(total)!=total: raise ValueError('integer nonnegative total required')
    c=nonneg_total_projection(noisy,total); out=np.floor(c).astype(int)
    k=int(total-out.sum())
    if k:out[np.argsort(-(c-out),kind='stable')[:k]]+=1
    assert out.sum()==total and (out>=0).all()
    return out


def fixed_features(X):
    # Fixed feature units, chosen without inspecting any training or test observations.
    scale=np.array([20,30,150,1500,.2,.2,.2,.1,.3,.1]*3)
    return np.column_stack([np.ones(len(X)),np.clip(2*np.asarray(X)/scale-1,-1,1)])


def dp_logistic_gd(X,y,rho,steps,clip,lr,rng,ridge=1e-3):
    X,y=np.asarray(X,float),np.asarray(y,float)
    if rho<=0 or clip<=0 or steps<1 or len(X)!=len(y):raise ValueError('invalid gradient mechanism')
    n,d=X.shape;w=np.zeros(d)
    # A replacement changes two clipped vectors: global l2 sensitivity 2C.
    sensitivity=2*clip; sigma=0 if np.isinf(rho) else sensitivity*np.sqrt(steps/(2*rho))
    for _ in range(steps):
        G=(special.expit(X@w)-y)[:,None]*X
        G/=np.maximum(1,np.linalg.norm(G,axis=1)/clip)[:,None]
        w-=lr*((G.sum(0)+sigma*rng.standard_normal(d))/n+ridge*w)
    return dict(w=w,sigma=float(sigma),sensitivity=sensitivity,rho=rho,adjacency='fixed-size replace-one')
