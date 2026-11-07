"""Audited Part 65 kernels; the rerun is a post hoc QA correction."""
from explainer.stats.kit.thesis import *  # noqa: F401,F403
import numpy as np
from scipy import special,stats
import math
def _logit(X, y, lam=0.001, iters=80):
    """Penalized logistic fit with backtracking and a checked score residual."""
    X, y = (np.asarray(X, float), np.asarray(y, float))
    penalty = np.r_[0.0, np.ones(X.shape[1] - 1)] * lam
    b = np.zeros(X.shape[1])
    objective = lambda b: float(np.logaddexp(0, X @ b).sum() - y @ (X @ b) + 0.5 * np.sum(penalty * b * b))
    value = objective(b)
    for _ in range(iters):
        p = special.expit(X @ b)
        gradient = X.T @ (p - y) + penalty * b
        H = (X * (p * (1 - p))[:, None]).T @ X + np.diag(penalty)
        step = np.linalg.solve(H, gradient)
        if np.max(np.abs(gradient)) < 1e-08:
            return dict(beta=b, H=H, prob=p, score_residual=float(np.max(np.abs(gradient))))
        fraction = 1.0
        while fraction > 2 ** (-30):
            candidate = b - fraction * step
            new = objective(candidate)
            if new <= value - 0.0001 * fraction * float(gradient @ step) + 1e-12:
                break
            fraction /= 2
        if fraction <= 2 ** (-30):
            raise RuntimeError('logistic line search failed')
        b, value = (candidate, new)
    raise RuntimeError('logistic fit did not converge')


def logistic_weights(x_src,x_tgt,ridge=0.,degree=1):
    xs,xt=np.asarray(x_src,float),np.asarray(x_tgt,float)
    x=np.r_[xs,xt];F=np.column_stack([x**k for k in range(degree+1)])
    fit=_logit(F,np.r_[np.zeros(len(xs)),np.ones(len(xt))],lam=ridge)
    beta=fit['beta'];ratio=len(xs)/len(xt)
    def w(z):
        z=np.atleast_1d(z);return ratio*np.exp(np.column_stack([z**k for k in range(degree+1)])@beta)
    w.coef=beta;w.score_residual=fit['score_residual'];return w


def halfwidths(scores,w_cal,w_test,alpha):
    scores,w_cal,w_test=map(lambda x:np.asarray(x,float),(scores,w_cal,w_test))
    if not 0<alpha<1 or len(scores)!=len(w_cal) or not np.isfinite(scores).all() or not np.isfinite(w_cal).all() or not np.isfinite(w_test).all() or np.any(w_cal<=0) or np.any(w_test<=0):raise ValueError('positive finite weights and finite scores required')
    # Scale all weights together to preserve ratios and avoid overflow in sums.
    scale=max(w_cal.max(),w_test.max());wc=w_cal/scale;wt=w_test/scale
    order=np.argsort(scores);s=scores[order];c=np.cumsum(wc[order]);target=(1-alpha)*(c[-1]+wt)
    indices=np.searchsorted(c,target,side='left');return np.r_[s,np.inf][indices]


def weighted_interval(x_cal,y_cal,w_fn,x_test,alpha):
    scores=np.abs(np.asarray(y_cal)-mean_fn(x_cal))
    if w_fn is None:return halfwidths(scores,np.ones(len(scores)),np.ones(len(x_test)),alpha)
    return halfwidths(scores,w_fn(x_cal),w_fn(x_test),alpha)


def tv_abs_tilt(b,mu):
    """TV(exp(b|x|)phi(x)/Z, phi(x-mu)), by its piecewise affine log-density ratio."""
    logPhi=special.log_ndtr(b);constant=-.5*b*b-np.log(2)-logPhi+.5*mu*mu
    def cdf(x):
        if x<0:return .5*np.exp(special.log_ndtr(x+b)-logPhi)
        return 1-.5*np.exp(special.log_ndtr(b-x)-logPhi)
    cuts=[-np.inf,0.,np.inf]
    for slope,side in [(-b-mu,-1),(b-mu,1)]:
        if abs(slope)>1e-14:
            root=-constant/slope
            if root*side>0:cuts.append(root)
    cuts=sorted(cuts);out=0.
    for lo,hi in zip(cuts,cuts[1:]):out+=abs((cdf(hi)-cdf(lo))-(stats.norm.cdf(hi-mu)-stats.norm.cdf(lo-mu)))
    return float(out/2)


def one_run(n_cal,n_tgt,mu,gamma,alpha,method,rng,n_test=200,lam=.5):
    xc,yc=draw(n_cal,0.,gamma,rng);xt,yt=draw(n_test,mu,gamma,rng)
    score_residual=0.
    if method=='none':w=None;tv=tv_gauss_shift(0,mu)
    elif method=='oracle':w=lambda x:np.exp(mu*np.asarray(x)-mu*mu/2);tv=0.
    elif method=='tempered':w=lambda x:np.exp(lam*(mu*np.asarray(x)-mu*mu/2));tv=tv_gauss_shift(lam*mu,mu)
    elif method in ('estimated','misspecified'):
        xs=rng.standard_normal(n_tgt);xu=mu+rng.standard_normal(n_tgt)
        w0=logistic_weights(abs(xs),abs(xu)) if method=='misspecified' else logistic_weights(xs,xu)
        score_residual=w0.score_residual
        if method=='estimated':w=w0;tv=tv_gauss_shift(w0.coef[1],mu)
        else:w=lambda x:w0(abs(np.asarray(x)));tv=tv_abs_tilt(w0.coef[1],mu)
    else:raise ValueError(method)
    h=weighted_interval(xc,yc,w,xt,alpha);cov=abs(yt-mean_fn(xt))<=h;finite=np.isfinite(h)
    return dict(coverage=float(cov.mean()),width=float(np.median(2*h[finite])) if finite.any() else np.inf,inf=float(np.mean(~finite)),bound=1-alpha-tv,finite_coverage=float(cov[finite].mean()) if finite.any() else None,finite_covered_mass=float(np.mean(cov&finite)),score_residual=score_residual)


def study(mus,gammas,methods,reps,n_cal,n_tgt,alpha,rng):
    out=[]
    for mu in mus:
      for gamma in gammas:
       for method in methods:
        rows=[one_run(n_cal,n_tgt,mu,gamma,alpha,method,rng) for _ in range(reps)]
        c=np.array([x['coverage'] for x in rows]);b=np.array([x['bound'] for x in rows]);w=np.array([x['width'] for x in rows])
        out.append(dict(mu=mu,gamma=gamma,method=method,coverage=float(c.mean()),mcse=float(c.std(ddof=1)/np.sqrt(reps)),bound=float(b.mean()),gap_mcse=float((c-b).std(ddof=1)/np.sqrt(reps)),width=float(np.median(w[np.isfinite(w)])) if np.isfinite(w).any() else None,inf=float(np.mean([x['inf'] for x in rows])),finite_covered_mass=float(np.mean([x['finite_covered_mass'] for x in rows])),max_logistic_score=max(x['score_residual'] for x in rows)))
    return out
