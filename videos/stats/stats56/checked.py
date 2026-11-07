"""Part-local audited selective-inference calculations."""
from __future__ import annotations
import math
from functools import lru_cache
import numpy as np
from scipy import integrate, optimize, special, stats
from explainer.stats.kit import selective as Legacy
from explainer.stats.kit.selective import *  # noqa: F403


def _log_mass(a,b):
    if a>=b:return -np.inf
    if a>0:return _log_mass(-b,-a)
    lb,la=special.log_ndtr(b),special.log_ndtr(a)
    if la == lb:
        mid=a+(b-a)/2
        return float(stats.norm.logpdf(mid)+np.log(b-a))
    return float(lb+np.log(-np.expm1(la-lb)))


def _log_tail_ratio(z,delta):
    """log SF(z+delta)/SF(z), z>=0; delta retained before subtracting huge locations."""
    if np.isinf(delta):return -np.inf
    return float(-z*delta-delta**2/2+np.log(special.erfcx((z+delta)/math.sqrt(2)))-np.log(special.erfcx(z/math.sqrt(2))))


def truncnorm_sf(y,mu,sigma,a,b):
    if sigma<=0 or not a<b:raise ValueError('positive scale and nonempty truncation required')
    if y<a or y>b:raise ValueError('observation is outside selection interval')
    if y==a:return 1.
    if y==b:return 0.
    if mu<=a:
        z=(a-mu)/sigma;d=(y-a)/sigma;B=(b-a)/sigma
        ly=_log_tail_ratio(z,d);lb=_log_tail_ratio(z,B)
        return float(np.exp(ly+np.log(-np.expm1(lb-ly))-np.log(-np.expm1(lb))))
    if mu>=b:
        return float(1-truncnorm_sf(-y,-mu,sigma,-b,-a))
    return float(np.exp(_log_mass((y-mu)/sigma,(b-mu)/sigma)-_log_mass((a-mu)/sigma,(b-mu)/sigma)))


def _solve_increasing(f,centre,scale,limit=None):
    """Expand until a real sign change; numerical failure is never labelled an infinite CI."""
    lo,hi=centre-scale,centre+scale
    width=scale
    for _ in range(1000):
        left,right=f(lo),f(hi)
        if not np.isfinite([left,right]).all():raise ArithmeticError('nonfinite pivot during root expansion')
        if left<=0<=right:
            return float(optimize.brentq(f,lo,hi,xtol=1e-10*scale,rtol=1e-12))
        width*=2
        if not np.isfinite(width):raise ArithmeticError('root bracket exceeded numerical range')
        if left>0:lo=centre-width
        if right<0:hi=centre+width
    raise ArithmeticError('could not bracket finite pivot root')


def truncnorm_interval(y,sigma,a,b,alpha=.05):
    if not a<y<b or not 0<alpha<1:raise ValueError('interior observation and valid alpha required')
    return tuple(_solve_increasing(lambda m:truncnorm_sf(y,m,sigma,a,b)-v,y,sigma) for v in (alpha/2,1-alpha/2))


def polyhedral_limits(A,b,y,eta,Sigma=None):
    A,b,y,eta=(np.asarray(v,float) for v in (A,b,y,eta))
    Sigma=np.eye(len(y)) if Sigma is None else np.asarray(Sigma,float)
    scales=np.max(np.abs(A),axis=1)
    scales=np.where(scales>0,scales,1.)
    A,b=A/scales[:,None],b/scales
    if np.any(A@y>b+1e-8):raise ValueError('observation violates selection event')
    s2=float(eta@Sigma@eta)
    if s2<=0:raise ValueError('contrast must have positive variance')
    c=Sigma@eta/s2;t=float(eta@y);z=y-c*t
    slopes,residual=A@c,b-A@z
    if np.any((slopes==0)&(residual<0)):raise ValueError('zero-slope constraint rules out the nuisance component')
    neg,pos=slopes<0,slopes>0
    lo=float(np.max(residual[neg]/slopes[neg])) if neg.any() else -np.inf
    hi=float(np.min(residual[pos]/slopes[pos])) if pos.any() else np.inf
    if lo>t+1e-8 or hi<t-1e-8:raise ArithmeticError('truncation does not contain observed statistic')
    return dict(stat=t,sd=math.sqrt(s2),lo=lo,hi=hi)


def lasso(X,y,lam,iters=20000,tol=1e-12):
    if lam<=0:raise ValueError('positive penalty required')
    fit=Legacy.lasso(X,y,lam,iters=iters,tol=tol)
    g=np.asarray(X).T@(np.asarray(y)-np.asarray(X)@fit)
    active=fit!=0
    error=max(np.max(np.abs(g[active]-lam*np.sign(fit[active])),initial=0),
              np.max(np.maximum(np.abs(g[~active])-lam,0),initial=0))
    if error>1e-7:raise ArithmeticError('lasso solution failed KKT check')
    return fit


def lasso_event(X, y, lam: float) -> dict:
    """The lasso's active set E and signs s at lam, with the polyhedron {A y <= b} of all y giving the same (E, s)
    (Lee et al. 2016, Proposition 4.2)."""
    X = np.asarray(X, float)
    bhat = lasso(X, y, lam)
    E = np.flatnonzero(np.abs(bhat) > 1e-10)
    s = np.sign(bhat[E])
    n, p = X.shape
    N = np.setdiff1d(np.arange(p), E)
    XE, XN = X[:, E], X[:, N]
    G = np.linalg.inv(XE.T @ XE)
    P = XE @ G @ XE.T
    pinvT = XE @ G  # (X_E^+)^T
    A0 = np.vstack([XN.T @ (np.eye(n) - P), -XN.T @ (np.eye(n) - P)]) / lam
    b0 = np.concatenate([1 - XN.T @ pinvT @ s, 1 + XN.T @ pinvT @ s])
    A1 = -np.diag(s) @ G @ XE.T
    b1 = -lam * np.diag(s) @ G @ s
    return {"beta": bhat, "E": E, "signs": s, "A": np.vstack([A0, A1]), "b": np.concatenate([b0, b1]), "pinv": G @ XE.T}


def lasso_selective_intervals(X, y, lam: float, sigma: float = 1.0, alpha: float = 0.05) -> dict:
    """Selective intervals for the partial regression coefficients of the selected model, eta_j = (X_E^+)' e_j,
    conditional on the event (E, s): a truncated normal pivot for each.  Also the naive OLS intervals on E."""
    ev = lasso_event(X, y, lam)
    out = []
    for k, j in enumerate(ev["E"]):
        eta = ev["pinv"][k]
        lim = polyhedral_limits(ev["A"], ev["b"], y, eta, sigma ** 2 * np.eye(len(y)))
        lo, hi = truncnorm_interval(lim["stat"], lim["sd"], lim["lo"], lim["hi"], alpha)
        z = stats.norm.ppf(1 - alpha / 2)
        out.append({"j": int(j), "est": lim["stat"], "sd": lim["sd"], "lo": lo, "hi": hi, "naive": (lim["stat"] - z * lim["sd"], lim["stat"] + z * lim["sd"]),
                    "trunc": (lim["lo"], lim["hi"])})
    return {"E": ev["E"], "signs": ev["signs"], "intervals": out}


def winner_conditional(y, sigma: float = 1.0, alpha: float = 0.05) -> dict:
    """Independent Y_k ~ N(mu_k, sigma^2); the winner j = argmax Y_k.  Given the losers, Y_j is N(mu_j, sigma^2)
    truncated to [max_{k != j} Y_k, inf): the conditional interval and median-unbiased estimate (Andrews, Kitagawa &
    McCloskey 2024, in the independent equal-variance case)."""
    y = np.asarray(y, float)
    j = int(np.argmax(y))
    lo_t = float(np.max(np.delete(y, j), initial=-np.inf))
    lo, hi = truncnorm_interval(y[j], sigma, lo_t, np.inf, alpha)
    med = _solve_increasing(lambda m: truncnorm_sf(y[j], m, sigma, lo_t, np.inf) - 0.5, y[j], sigma)
    z = stats.norm.ppf(1 - alpha / 2)
    return {"j": j, "y": float(y[j]), "second": lo_t, "lo": lo, "hi": hi, "median_unbiased": med,
            "naive": (float(y[j] - z * sigma), float(y[j] + z * sigma))}


def winner_hybrid(y, sigma: float = 1.0, alpha: float = 0.05, beta: float = 0.005) -> dict:
    """The hybrid interval: condition on the winner and also on |Y_j - mu_j| <= c_beta sigma (c_beta the 1 - beta
    simultaneous constant), at level (alpha - beta)/(1 - beta); then intersect with the projection interval.  It is never
    longer than the projection interval and close to the conditional one when the win is clear."""
    y = np.asarray(y, float)
    K = len(y)
    j = int(np.argmax(y))
    lo_t = float(np.max(np.delete(y, j), initial=-np.inf))
    c = max_z_quantile(K, 1 - beta)
    a2 = (alpha - beta) / (1 - beta)
    proj = (float(y[j] - c * sigma), float(y[j] + c * sigma))

    def sf(m):
        if m <= proj[0]: return 0.
        if m >= proj[1]: return 1.
        return truncnorm_sf(y[j], m, sigma, max(lo_t, m - c * sigma), m + c * sigma)

    def root(level):
        g = lambda m: sf(m) - level  # noqa: E731
        lo, hi = proj
        if g(lo) > 0:
            return lo
        if g(hi) < 0:
            return hi
        return optimize.brentq(g, lo, hi, xtol=1e-9)

    return {"lo": root(a2 / 2), "hi": root(1 - a2 / 2), "projection": proj}


def two_means_1d(x):
    x=np.asarray(x,float)
    if len(x)<2 or not np.isfinite(x).all():raise ValueError('at least two finite observations required')
    return Legacy.two_means_1d(x-x.mean())


def clustering_region(x):
    """Exact 1-D global two-means selection region along its observed contrast.

    Same groups must remain separated, so their within-group sorted order is fixed.
    All alternative split costs are quadratics. Remove their negative intervals.
    """
    x=np.asarray(x,float);labels=two_means_1d(x)
    n=len(x);n1=int(np.sum(labels==0));n2=n-n1
    nu=np.where(labels==1,1/n2,-1/n1);nn=float(nu@nu);d=float(nu@x)
    lower=max(0.,d+float(x[labels==0].max()-x[labels==1].min()))
    order=np.argsort(x,kind='stable');slope=(nu/nn)[order]
    z=(x-nu*d/nn)[order];z-=z.mean()
    own=float(np.sum((x[labels==0]-x[labels==0].mean())**2)+np.sum((x[labels==1]-x[labels==1].mean())**2))
    forbidden=[]
    for k in range(1,n):
        if k==n1:continue
        rz=z.copy();rc=slope.copy()
        rz[:k]-=rz[:k].mean();rz[k:]-=rz[k:].mean()
        rc[:k]-=rc[:k].mean();rc[k:]-=rc[k:].mean()
        a=float(rc@rc);b=float(2*rc@rz);c=float(rz@rz-own)
        disc=b*b-4*a*c
        if disc<=0:continue
        q=-.5*(b+math.copysign(math.sqrt(disc),b))
        roots=sorted((q/a,c/q)) if q!=0 else [0.,0.]
        lo,hi=max(lower,roots[0]),roots[1]
        if hi>lo:forbidden.append((lo,hi))
    merged=[]
    for lo,hi in sorted(forbidden):
        if merged and lo<=merged[-1][1]:merged[-1]=(merged[-1][0],max(hi,merged[-1][1]))
        else:merged.append((lo,hi))
    intervals=[];start=lower
    for lo,hi in merged:
        if lo>start:intervals.append((start,lo))
        start=max(start,hi)
    intervals.append((start,np.inf))
    if not any(a-1e-8<=d<=b+1e-8 for a,b in intervals):raise ArithmeticError('analytic clustering region excludes observation')
    return dict(labels=labels,nu=nu,d=d,nn=nn,intervals=intervals,n=(n1,n2))


def clustering_pvalues(x,sigma=1.,grid=None):
    if sigma<=0:raise ValueError('known positive Gaussian scale required')
    region=clustering_region(x);d=region['d'];sd=sigma*math.sqrt(region['nn'])
    masses=[_log_mass(a/sd,b/sd) for a,b in region['intervals']]
    tails=[_log_mass(max(a,d)/sd,b/sd) for a,b in region['intervals'] if b>d]
    selective=float(np.exp(special.logsumexp(tails)-special.logsumexp(masses)))
    return dict(**region,sd=sd,naive=float(2*stats.norm.sf(abs(d)/sd)),selective=selective)


@lru_cache(None)
def _legendre(n):
    nodes,weights=special.roots_legendre(n)
    return (nodes+1)/2,weights/2


def randomized_sf(y,mu,c,sigma,gamma,quadrature=False):
    """Condition on S=Y+W>c, then integrate the conditional Gaussian Y|S."""
    if gamma<=0:return truncnorm_sf(y,mu,sigma,c,np.inf)
    v=math.hypot(sigma,gamma);conditional_sd=sigma*gamma/v
    logp=special.log_ndtr((mu-c)/v)
    def integrand(u):
        z=-special.ndtri_exp(logp+np.log(u))
        return special.ndtr((mu+sigma*sigma/v*z-y)/conditional_sd)
    if quadrature:
        value,error=integrate.quad(integrand,0,1,epsabs=2e-10,epsrel=2e-9,limit=150)
        if error>1e-7:raise ArithmeticError('randomization quadrature error too large')
        return value
    u,weights=_legendre(256)
    return float(weights@integrand(u))


def threshold_selective(y,c,sigma=1.,gamma=0.,alpha=.05,grid=None):
    if sigma<=0 or gamma<0:raise ValueError('positive sigma and nonnegative gamma required')
    if gamma==0:
        lo,hi=truncnorm_interval(y,sigma,c,np.inf,alpha)
        return dict(lo=lo,hi=hi,pivot_residual=0.)
    ends=[];residuals=[]
    for level in (alpha/2,1-alpha/2):
        approximate=_solve_increasing(lambda mu:randomized_sf(y,mu,c,sigma,gamma)-level,y,sigma)
        residual=randomized_sf(y,approximate,c,sigma,gamma,True)-level
        if abs(residual)>2e-8:
            approximate=_solve_increasing(lambda mu:randomized_sf(y,mu,c,sigma,gamma,True)-level,approximate,.1*sigma)
        ends.append(approximate)
        residuals.append(abs(randomized_sf(y,approximate,c,sigma,gamma,True)-level))
    if max(residuals)>1e-7:raise ArithmeticError('selective interval failed independent quadrature residual')
    return dict(lo=ends[0],hi=ends[1],pivot_residual=max(residuals))


def mcse(values):
    return float(np.std(values,ddof=1)/math.sqrt(len(values)))


def ratio_mcse(hits,counts):
    hits,counts=np.asarray(hits,float),np.asarray(counts,float)
    ratio=float(hits.sum()/counts.sum())
    return mcse((hits-ratio*counts)/counts.mean())


def posi_constant(X,rng,alpha=.05,reps=4000):
    L=Legacy._contrasts(X)
    def maxima():
        return np.concatenate([np.max(np.abs(rng.standard_normal((min(256,reps-start),L.shape[1]))@L.T),axis=1)
                               for start in range(0,reps,256)])
    values=maxima();validation=maxima();ordered=np.sort(values)
    K=float(np.quantile(values,1-alpha));lo=max(0,int(stats.binom.ppf(.025,reps,1-alpha))-1)
    hi=min(reps-1,int(stats.binom.ppf(.975,reps,1-alpha)))
    p=X.shape[1];nc=len(L)
    return dict(K=K,n_contrasts=nc,z=float(stats.norm.isf(alpha/2)),
                bonferroni=float(stats.norm.isf(alpha/(2*nc))),scheffe=float(np.sqrt(stats.chi2.isf(alpha,p))),
                quantile_ci=[float(ordered[lo]),float(ordered[hi])],quantile_ci_scope='pointwise binomial order-statistic 95% interval',
                maxima=values,validation=validation,validation_coverage=float(np.mean(validation<=K)),
                validation_mcse=mcse(validation<=K),reps=reps)


def gaussian_knockoffs(X,Sigma,rng):
    s=min(1.,2*np.linalg.eigvalsh(Sigma).min())*.999
    D=s*np.eye(Sigma.shape[0]);inverse=np.linalg.inv(Sigma)
    covariance=2*D-D@inverse@D
    # The strictly shrunken equicorrelated parameter makes C positive definite already.
    factor=np.linalg.cholesky(covariance)
    return X-X@inverse@D+rng.standard_normal(X.shape)@factor.T


def lasso_W(X,Xk,y,lam):
    design=np.column_stack([X,Xk]);design-=design.mean(0)
    coefficients=lasso(design,y-y.mean(),len(y)*lam)
    p=X.shape[1]
    return np.abs(coefficients[:p])-np.abs(coefficients[p:])


def truncnorm_pvalue(y,mu0,sigma,a,b,two_sided=True):
    tail=truncnorm_sf(y,mu0,sigma,a,b)
    return min(1.,2*min(tail,1-tail)) if two_sided else tail
