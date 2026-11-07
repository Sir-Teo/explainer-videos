"""Part 59 audited numerical kernels, with explicit numerical diagnostics."""
from __future__ import annotations
import math
from functools import lru_cache
import numpy as np
from scipy import optimize, special, stats, integrate
from explainer.stats.kit.amp import *  # noqa: F403
_GH_X, _GH_W = special.roots_hermitenorm(161)
_GH_W /= math.sqrt(2*math.pi)
_sigmoid = special.expit

def mcse(x):
    return float(np.std(x,ddof=1)/math.sqrt(len(x)))

def prox_logistic(z,lam,iters=80):
    """Bracketed Newton: the root lies in [z-lam,z] for lam>=0."""
    z=np.asarray(z,float)
    if lam<0:raise ValueError("nonnegative proximal scale required")
    low,high=z-lam,z.copy()
    t=z-lam*special.expit(z)
    for _ in range(iters):
        sig=special.expit(t)
        residual=t+lam*sig-z
        if np.max(np.abs(residual)/(1+np.abs(z)))<3e-12:return t
        done=np.abs(residual)<3e-12*(1+np.abs(z))
        low=np.where(residual<0,t,low)
        high=np.where(residual>=0,t,high)
        proposal=t-residual/(1+lam*sig*(1-sig))
        t=np.where(done,t,np.where((proposal>low+.1*(high-low))&(proposal<high-.1*(high-low)),proposal,(low+high)/2))
    if np.max(np.abs(t+lam*special.expit(t)-z)/(1+np.abs(z)))>1e-10:
        raise RuntimeError(f"proximal root did not converge: lam={lam}, zmax={np.abs(z).max()}, err={np.max(np.abs(t+lam*special.expit(t)-z)/(1+np.abs(z)))}")
    return t



def mle_exists_boundary(gamma,nodes=161):
    """Deterministic quadrature, integrating Z analytically before optimization."""
    if gamma==0:return .5
    v,w=special.roots_hermitenorm(nodes);w=w/math.sqrt(2*math.pi)
    weights=2*special.expit(gamma*v)*w
    def objective(t):
        a=t*v
        return float(weights @ ((1+a*a)*special.ndtr(-a)-a*stats.norm.pdf(a)))
    result=optimize.minimize_scalar(objective,bounds=(0,20),method="bounded",
                                    options={"xatol":1e-12})
    if not result.success:raise RuntimeError("existence-boundary optimization failed")
    return float(result.fun)

def _bg_mse(tau,thr,eps,n_mc=0,mu=1.):
    """Exact truncated-normal moments; avoids GH errors at soft-threshold kinks."""
    if tau==0:return eps*float(min(abs(mu),thr)**2)
    def component(mean):
        a,b=(thr-mean)/tau,(-thr-mean)/tau
        sf,cdf=stats.norm.sf(a),stats.norm.cdf(b)
        pa,pb=stats.norm.pdf(a),stats.norm.pdf(b)
        right=(tau*tau+thr*thr)*sf+(tau*tau*a-2*tau*thr)*pa
        left=(tau*tau+thr*thr)*cdf+(-tau*tau*b-2*tau*thr)*pb
        middle=mean*mean*(stats.norm.cdf(a)-stats.norm.cdf(b))
        return float(max(0.,right+left+middle))
    return (1-eps)*component(0.)+eps*component(mu)

def bayes_denoiser(r,tau,eps,mu=1.):
    """Posterior weights in log space, including distant observations."""
    if tau<=0 or not 0<eps<1:raise ValueError("tau>0 and 0<eps<1 required")
    r=np.asarray(r,float)
    logw=np.stack((np.log1p(-eps)-.5*(r/tau)**2,
                   np.log(eps/2)-.5*((r-mu)/tau)**2,
                   np.log(eps/2)-.5*((r+mu)/tau)**2))
    weights=np.exp(logw-special.logsumexp(logw,axis=0))
    return mu*(weights[1]-weights[2])

@lru_cache(maxsize=30000)
def bayes_mmse(tau,eps,mu=1.):
    """Adaptive scalar integration, partitioned at posterior transition points."""
    if tau==0:return 0.
    # Integrate errors against each true mixture component on standardized Z.
    # Extra transition points prevent narrow posterior changes being missed.
    transitions=np.array([-mu/2,mu/2])
    values=[]
    for truth in (0.,mu):
        points=sorted(set([-12.,12.,0.]+[float((q-truth)/tau) for q in transitions
                                      if -12<(q-truth)/tau<12]))
        value=0.
        for a,b in zip(points[:-1],points[1:]):
            value+=integrate.quad(lambda z: float((bayes_denoiser(truth+tau*z,tau,eps,mu)-truth)**2)
                                 *stats.norm.pdf(z),a,b,epsabs=2e-12,epsrel=2e-9,limit=100)[0]
        values.append(value)
    return (1-eps)*values[0]+eps*values[1]

def state_evolution(delta: float, eps: float, sigma2: float, theta: float, iters: int = 30, mu: float = 1.0) -> np.ndarray:
    """tau_{t+1}^2 = sigma2 + (1/delta) E[(eta(X + tau_t Z; theta tau_t) - X)^2], tau_0^2 = sigma2 + E X^2 / delta."""
    tau2 = sigma2 + eps * mu * mu / delta
    out = [tau2]
    for _ in range(iters):
        tau = math.sqrt(tau2)
        tau2 = sigma2 + _bg_mse(tau, theta * tau, eps, mu=mu) / delta
        out.append(tau2)
    return np.asarray(out)

def bayes_state_evolution(delta: float, eps: float, sigma2: float, iters: int = 200, mu: float = 1.0, start=None) -> np.ndarray:
    """State evolution of Bayes-optimal AMP: tau^2 <- sigma2 + mmse(tau)/delta, from an uninformative start; its fixed
    point gives AMP's MSE, which equals the replica (Bayes-optimal) MMSE outside the hard phase (Barbier et al. 2019)."""
    tau2 = sigma2 + eps * mu * mu / delta if start is None else start
    out = [tau2]
    for _ in range(iters):
        tau2 = sigma2 + bayes_mmse(math.sqrt(tau2), eps, mu) / delta
        out.append(tau2)
    return np.asarray(out)

def lasso_se_mse(delta,eps,sigma2,thetas=None,mu=1.):
    """Best positive lasso penalty on the stated threshold grid, converged SE only."""
    thetas=np.linspace(.5,3.,26) if thetas is None else thetas
    best=None
    for th in thetas:
        if 2*((1+th*th)*stats.norm.sf(th)-th*stats.norm.pdf(th)) >= delta:
            continue  # below the standard positive-penalty AMP threshold domain
        sequence=state_evolution(delta,eps,sigma2,th,1000,mu)
        t2=sequence[-1]
        if not np.isfinite(t2) or abs(t2-sequence[-2])>1e-8*(1+t2):continue
        tau=math.sqrt(t2)
        active=(1-eps)*2*stats.norm.sf(th)+eps*(stats.norm.sf(th-mu/tau)+stats.norm.cdf(-th-mu/tau))
        penalty=th*tau*(1-active/delta)
        if penalty<=0:continue
        mse=_bg_mse(tau,th*tau,eps,mu=mu)
        if best is None or mse<best["mse"]:
            best=dict(theta=float(th),mse=float(mse),penalty=float(penalty),
                      fixed_point_residual=abs(float(t2-sequence[-2])))
    if best is None:raise RuntimeError("no converged positive-penalty lasso candidate")
    return best


def lad_fit(X,y):
    X,y=np.asarray(X,float),np.asarray(y,float);n,p=X.shape
    A=np.hstack([X,np.eye(n),-np.eye(n)])
    fit=optimize.linprog(np.r_[np.zeros(p),np.ones(2*n)],A_eq=A,b_eq=y,
                        bounds=[(None,None)]*p+[(0,None)]*(2*n),method="highs")
    if not fit.success or np.max(np.abs(A@fit.x-y))>2e-7:
        raise RuntimeError("LAD linear program failed")
    return fit.x[:p]

def sur_candes(kappa,gamma,x0=None,nodes=161):
    """Positive, bounded least-squares solve of the published scalar system.

    Solver failure is reported as numerical failure, never nonexistence.
    A separate phase boundary determines which regime is admissible.
    """
    if not 0<kappa<.5 or gamma<0:raise ValueError("need 0<kappa<.5 and gamma>=0")
    boundary=mle_exists_boundary(gamma,nodes=max(nodes,161))
    if kappa>=boundary:
        return dict(alpha=np.nan,sigma=np.nan,lam=np.nan,factor=np.nan,ok=False,
                    residual=np.nan,status="above asymptotic existence boundary",
                    kappa_boundary=boundary)
    z,w=special.roots_hermitenorm(nodes);w=w/math.sqrt(2*math.pi)
    z1,z2=np.meshgrid(z,z,indexing="ij")
    w2=np.outer(w,w);q1=gamma*z1;r1=special.expit(q1)
    def system(v):
        a=math.exp(v[0]) if gamma else 1.
        sig,lam=math.exp(v[-2]),math.exp(v[-1])
        q2=-a*q1+math.sqrt(kappa)*sig*z2
        prox=prox_logistic(q2,lam)
        rp=special.expit(prox)
        e1=np.sum(w2*2*r1*(lam*rp)**2)/(kappa*sig)**2-1
        e3=np.sum(w2*2*r1/(1+lam*rp*(1-rp)))-(1-kappa)
        if gamma:
            e2=np.sum(w2*r1*q1*rp)/(gamma*gamma)
            return np.array([e1,e2,e3])
        return np.array([e1,e3])
    starts=[x0] if x0 is not None else [(1.2,3.,1.),(2.,7.,6.)]
    best=None
    for a,sig,lam in starts:
        start=np.log([a,sig,lam] if gamma else [sig,lam])
        fit=optimize.least_squares(system,start,bounds=(-8,12),xtol=1e-12,
                                  ftol=1e-12,gtol=1e-12,max_nfev=500)
        res=float(np.max(np.abs(system(fit.x))))
        if best is None or res<best[0]:best=res,fit
        if res<1e-10:break
    res,fit=best;values=np.exp(fit.x)
    a,sig,lam=values if gamma else (1.,*values)
    return dict(alpha=float(a),sigma=float(sig),lam=float(lam),
                factor=float(kappa*sig*sig/lam),ok=res<1e-8,
                residual=res,nodes=nodes,kappa_boundary=boundary,
                status="converged" if res<1e-8 else "numerical solve failed")

def logistic_mle(X,y,iters=80,tol=1e-9,check_separation=True):
    """No-intercept MLE; certify no weak separator before reporting a finite fit."""
    X,y=np.asarray(X,float),np.asarray(y,float)
    p=X.shape[1];b=np.zeros(p)
    if check_separation:
        signed=X*np.where(y>0,1.,-1.)[:,None]
        fit=optimize.linprog(-signed.sum(0),A_ub=-signed,b_ub=np.zeros(len(y)),
                            bounds=[(-1,1)]*p,method="highs")
        if not fit.success:raise RuntimeError("separation LP failed")
        if -fit.fun>1e-7:
            return b,np.nan,False
    ll=float(-len(y)*math.log(2))
    for _ in range(iters):
        eta=X@b;pr=special.expit(eta)
        gradient=X.T@(y-pr)
        hessian=(X*(pr*(1-pr))[:,None]).T@X
        try:step=np.linalg.solve(hessian,gradient)
        except np.linalg.LinAlgError:return b,ll,False
        decrement=float(gradient@step)
        if decrement<tol and np.max(np.abs(gradient))<1e-7:
            return b,ll,True
        fraction=1.
        while fraction>2**-30:
            trial=b+fraction*step
            value=float(np.sum(y*(X@trial)-np.logaddexp(0,X@trial)))
            if value>=ll+1e-4*fraction*decrement-1e-12:break
            fraction/=2
        if fraction<=2**-30:return b,ll,False
        b,ll=trial,value
    return b,ll,False

def lrt_one(X,y,j=0):
    X=np.asarray(X,float)
    b,ll1,ok1=logistic_mle(X,y)
    if not ok1:return dict(llr2=np.nan,beta=b,ok=False)
    keep=np.arange(X.shape[1])!=j
    _,ll0,ok0=logistic_mle(X[:,keep],y,check_separation=False)
    stat=2*(ll1-ll0)
    if stat < -1e-7:raise RuntimeError("full likelihood below restricted likelihood")
    return dict(llr2=max(0.,stat),beta=b,ok=ok0)

def ridge_risk(lam,gamma,snr,sigma2=1.):
    """Positive-axis analytic derivative, avoiding finite-difference cancellation."""
    lam=np.asarray(lam,float)
    if np.any(lam<=0) or gamma<=0:raise ValueError("positive lambda and ratio required")
    a=1-gamma+lam
    disc=np.sqrt(a*a+4*gamma*lam)
    m=np.where(a>=0,2/(a+disc),(disc-a)/(2*gamma*lam))
    derivative=m*(gamma*m+1)/disc
    bias=snr*sigma2*lam*lam*derivative
    var=sigma2*gamma*(1-lam*m)/disc
    return dict(bias=bias,var=var,risk=bias+var)

def optimal_ridge_risk(gamma,snr,sigma2=1.):
    return float(ridge_risk(gamma/snr,gamma,snr,sigma2)["risk"])

def ridge_sim(n,gamma,snr,lams,reps,rng,sigma2=1.,return_draws=False):
    p=max(1,int(round(gamma*n)))
    draws=np.zeros((reps,len(lams)))
    for rep in range(reps):
        X=rng.standard_normal((n,p));beta=rng.standard_normal(p)
        beta*=math.sqrt(snr*sigma2)/np.linalg.norm(beta)
        y=X@beta+math.sqrt(sigma2)*rng.standard_normal(n)
        U,s,Vt=np.linalg.svd(X,full_matrices=False);uy=U.T@y
        for k,lam in enumerate(lams):
            shrink=1/s if lam==0 else s/(s*s+n*lam)
            fitted=Vt.T@(shrink*uy)
            draws[rep,k]=np.sum((fitted-beta)**2)
    summary=dict(mean=draws.mean(0),mcse=draws.std(0,ddof=1)/math.sqrt(reps),draws=draws)
    return summary if return_draws else summary["mean"]

def free_semicircle_plus_pm1(xs,s2,eta=1e-3,iters=4000,return_audit=False):
    values=[];errors=[]
    for x in np.atleast_1d(xs):
        z=x+1j*eta
        roots=np.roots([s2*s2,2*z*s2,z*z-1+s2,z])
        candidates=[r for r in roots if r.imag>0]
        if len(candidates)!=1:raise RuntimeError("ambiguous Stieltjes branch")
        m=candidates[0]
        residual=abs(m-.5*(1/(1-z-s2*m)+1/(-1-z-s2*m)))
        if residual>1e-9:raise RuntimeError("Pastur residual too large")
        values.append(m.imag/math.pi);errors.append(residual)
    audit=dict(density=np.array(values),eta=eta,max_residual=max(errors))
    return audit if return_audit else audit["density"]

def random_features_experiment(n,d,Ns,lams,reps,rng,sigma2=.25):
    """Paired penalties, nested features, 1/sqrt(N) kernel normalization."""
    draws=np.zeros((reps,len(lams),len(Ns)))
    for rep in range(reps):
        beta=rng.standard_normal(d);beta/=np.linalg.norm(beta)
        X=rng.standard_normal((n,d))/math.sqrt(d)
        Xt=rng.standard_normal((2000,d))/math.sqrt(d)
        y=X@beta+math.sqrt(sigma2)*rng.standard_normal(n);truth=Xt@beta
        W=rng.standard_normal((max(Ns),d))
        features=np.maximum(X@W.T,0)
        test=np.maximum(Xt@W.T,0)
        for j,N in enumerate(Ns):
            F=features[:,:N]/math.sqrt(N);Ft=test[:,:N]/math.sqrt(N)
            U,s,Vt=np.linalg.svd(F,full_matrices=False);uy=U.T@y
            for k,lam in enumerate(lams):
                shrink=np.divide(1,s,out=np.zeros_like(s),where=s>1e-12*s.max()) if lam==0 else s/(s*s+n*lam)
                fit=Vt.T@(shrink*uy)
                draws[rep,k,j]=np.mean((Ft@fit-truth)**2)
    return dict(mean=draws.mean(0),mcse=draws.std(0,ddof=1)/math.sqrt(reps),draws=draws,
                target_variance=1/d,noise_variance=sigma2,feature_normalization="1/sqrt(N)",
                risk_scope="squared error against noiseless target; excludes irreducible test noise",
                design_scope="paired penalties; same nested random feature draws across N")
