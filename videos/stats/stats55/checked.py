"""Part-local audited numerics for the qualifying exam."""
from __future__ import annotations
import math
import numpy as np
from scipy import stats
from explainer.stats.kit import qual as Q


def mcse(values):
    return float(np.std(values, ddof=1) / np.sqrt(len(values)))


def umpu_binomial(n, p0, alpha=.05):
    """Two-tail binomial UMPU rule with stable tail moments and boundary masses."""
    if n == 0:
        return dict(phi=np.array([alpha]), c1=0, c2=0, g1=alpha, g2=alpha)
    x=np.arange(n+1);f=stats.binom.pmf(x,n,p0);mu=n*p0
    for c1 in range(int(stats.binom.ppf(alpha,n,p0))+1):
        c2=np.arange(c1+1,n+1)
        a0=stats.binom.cdf(c1-1,n,p0)+stats.binom.sf(c2,n,p0)
        centered=mu*(stats.binom.cdf(c1-2,n-1,p0)-stats.binom.cdf(c1-1,n,p0)
                     +stats.binom.sf(c2-1,n-1,p0)-stats.binom.sf(c2,n,p0))
        u1=((c2-mu)*(alpha-a0)+centered)/(c2-c1)
        u2=alpha-a0-u1
        ok=(u1>=-1e-13)&(u2>=-1e-13)&(u1<=f[c1]+1e-13)&(u2<=f[c2]+1e-13)
        indices=np.flatnonzero(ok & (f[c1]>1e-200) & (f[c2]>1e-200))
        if not len(indices):continue
        k=int(indices[0]);upper=int(c2[k])
        phi=((x<c1)|(x>upper)).astype(float)
        g1=float(np.clip(u1[k]/f[c1],0,1));g2=float(np.clip(u2[k]/f[upper],0,1))
        phi[c1],phi[upper]=g1,g2
        if abs(f@phi-alpha)>1e-10 or abs(((x-mu)*f)@phi)>1e-9:
            raise ArithmeticError('binomial size/unbiasedness constraints failed')
        return dict(phi=phi,c1=c1,c2=upper,g1=g1,g2=g2)
    raise ArithmeticError('no UMPU boundaries found')


def sparse_fano(d, s, n, sigma=1.):
    if not 1 <= s <= d // 8 or n < 1 or sigma <= 0:
        raise ValueError('sparse packing requires 1 <= s <= d/8 and positive n, sigma')
    # Either packing may be chosen: disjoint supports give a nontrivial small-s bound.
    logM = max(s / 8 * math.log1p(d / (2*s)), math.log(d // s))
    delta2 = sigma**2 * (logM - math.log(2)) / (2*n*s)
    return dict(logM=logM, delta2=delta2, kl=n*s*delta2/sigma**2,
                lower=sigma**2 * (logM-math.log(2))**2 / (32*n*logM),
                rate=sigma**2 * s * math.log(math.e*d/s) / n)


def soft_risk_coordinate(theta, noise_sd, threshold):
    """Exact Gaussian squared-error risk, from truncated first/second moments."""
    a, b, t = (threshold-theta)/noise_sd, (-threshold-theta)/noise_sd, threshold/noise_sd
    return float(noise_sd**2 * ((1+t*t)*(stats.norm.sf(a)+stats.norm.cdf(b))
                 +(a-2*t)*stats.norm.pdf(a)-(b+2*t)*stats.norm.pdf(b))
                 + theta**2 * (stats.norm.cdf(a)-stats.norm.cdf(b)))


def soft_threshold_risk(d, s, n, signal, sigma=1.):
    sd = sigma/math.sqrt(n)
    threshold = sd*math.sqrt(2*math.log(d/s))
    return s*soft_risk_coordinate(signal, sd, threshold)+(d-s)*soft_risk_coordinate(0., sd, threshold)


def lasso_oracle(n, p, s, rng, reps=30, sigma=1., delta=.05):
    lam = 2*sigma*math.sqrt(2*math.log(2*p/delta)/n)
    pred, l1, events, kkt = [], [], [], []
    for _ in range(reps):
        X = rng.standard_normal((n,p))
        X *= math.sqrt(n)/np.linalg.norm(X,axis=0)
        beta = np.r_[np.ones(s),np.zeros(p-s)]
        noise = sigma*rng.standard_normal(n)
        y = X@beta+noise
        fit = Q.lasso_cd(X,y,lam,iters=20000,tol=1e-11)
        gradient = X.T@(y-X@fit)/n
        active = fit != 0
        error = max(np.max(np.abs(gradient[active]-lam*np.sign(fit[active])),initial=0.),
                    np.max(np.maximum(np.abs(gradient[~active])-lam,0.),initial=0.))
        if error > 1e-8: raise ArithmeticError('lasso KKT tolerance failed')
        pred.append(float(np.mean((X@(fit-beta))**2)));l1.append(float(np.sum(np.abs(fit-beta))))
        events.append(bool(np.max(np.abs(X.T@noise/n))<=lam/2));kkt.append(error)
        if events[-1]:
            # The cone follows directly from the basic inequality; no assumed RE constant.
            assert np.sum(np.abs(fit[s:])) <= 3*np.sum(np.abs(fit[:s]-beta[:s]))+1e-7
    phi2=.5
    return dict(lam=lam,pred=float(np.mean(pred)),l1=float(np.mean(l1)),event=float(np.mean(events)),
                pred_bound=9*s*lam**2/phi2,l1_bound=12*s*lam/phi2,
                pred_mcse=mcse(pred),l1_mcse=mcse(l1),event_mcse=mcse(events),
                pred_samples=pred,l1_samples=l1,event_samples=events,kkt_max=max(kkt),
                max_column_norm=math.sqrt(n),phi2_reference=phi2,
                bound_scope='conditional benchmark if compatibility phi^2 >= .5; not certified for these random designs')


def sequence_contraction(n, alpha, beta, K=100000):
    if n < 1 or alpha <= 0 or beta <= 0 or K < 1: raise ValueError('positive model parameters required')
    out=Q.sequence_contraction(n,alpha,beta,K)
    # Monotone power series integral bounds for omitted coordinates, including shrinkage denominators.
    q=n*(K+1.)**(-1-2*alpha)
    lower=((1/(1+q))**2*(K+1.)**(-2*beta)/(2*beta)
           +n/(1+q)**2*(K+1.)**(-1-4*alpha)/(1+4*alpha)
           +(K+1.)**(-2*alpha)/(2*alpha)/(1+q))
    upper=K**(-2*beta)/(2*beta)+n*K**(-1-4*alpha)/(1+4*alpha)+K**(-2*alpha)/(2*alpha)
    out.update(partial_total=out['total'],tail_lower=lower,tail_upper=upper,
               total_lower=out['total']+lower,total_upper=out['total']+upper,K=K)
    out['total']=(out['total_lower']+out['total_upper'])/2
    return out
