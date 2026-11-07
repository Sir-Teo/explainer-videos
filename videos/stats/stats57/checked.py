"""Part-local audited distribution-free calculations."""
from __future__ import annotations
import math
import numpy as np
from scipy import optimize,stats
from explainer.stats.kit.dfree import *  # noqa: F403
from explainer.stats.kit import conformal as CF


def mcse(values):
    return float(np.std(values,ddof=1)/math.sqrt(len(values)))


def bahadur_savage_coverage(n,eps,shift=3.,alpha=.05):
    """Exact no-atom contribution uses a noncentral t law, not a normal approximation."""
    c=stats.t.isf(alpha/2,n-1);nc=-shift*math.sqrt(n)
    delta=abs(nc)
    cov_none=stats.nct.cdf(c,n-1,delta)-stats.nct.cdf(-c,n-1,delta)
    cov_none=max(0.,float(cov_none));p_none=(1-eps)**n
    return dict(p_none=p_none,no_atom_coverage=cov_none,upper=1-p_none+p_none*cov_none,mean=shift)


def full_conformal_ridge(X,y,x_new,lam,alpha=.1,grid=None):
    """Solve all absolute-affine residual crossings; retain the union, including holes."""
    X,y,x_new=np.asarray(X,float),np.asarray(y,float),np.asarray(x_new,float)
    if lam<=0 or not 0<alpha<1:raise ValueError('positive ridge penalty and valid alpha required')
    Xa=np.vstack([X,x_new]);R=np.eye(len(y)+1)-Xa@np.linalg.solve(Xa.T@Xa+lam*np.eye(X.shape[1]),Xa.T)
    a=R[:,:-1]@y;b=R[:,-1]
    roots=[]
    for sign in [-1,1]:
        numerator=a[:-1]+sign*a[-1];denominator=b[:-1]+sign*b[-1]
        roots.extend((-numerator[denominator!=0]/denominator[denominator!=0]).tolist())
    roots=np.unique(roots)
    def pvalue(t):
        residual=np.abs(a+b*t)
        return float(np.mean(residual>=residual[-1]-1e-11*max(1.,residual[-1])))
    edges=np.r_[-np.inf,roots,np.inf];intervals=[]
    for lo,hi in zip(edges[:-1],edges[1:]):
        t=(lo+hi)/2 if np.isfinite([lo,hi]).all() else (hi-max(1.,abs(hi)) if np.isneginf(lo) else lo+max(1.,abs(lo)))
        if pvalue(t)>alpha:intervals.append((float(lo),float(hi)))
    for t in roots:
        if pvalue(t)>alpha and not any(lo<=t<=hi for lo,hi in intervals):intervals.append((float(t),float(t)))
    merged=[]
    for lo,hi in sorted(intervals):
        if merged and lo<=merged[-1][1]:merged[-1]=(merged[-1][0],max(hi,merged[-1][1]))
        else:merged.append((lo,hi))
    if grid is None:grid=np.linspace(y.min()-3*y.std(),y.max()+3*y.std(),801)
    grid=np.asarray(grid,float)
    return dict(grid=grid,keep=np.array([any(lo<=t<=hi for lo,hi in merged) for t in grid]),intervals=merged,
                lo=min((lo for lo,hi in merged),default=np.nan),hi=max((hi for lo,hi in merged),default=np.nan),
                length=sum(hi-lo for lo,hi in merged),breakpoints=roots)


def conformal_coverage_law(n,alpha):
    k=math.ceil((n+1)*(1-alpha))
    if k>n:return dict(a=k,b=0,mean=1.,q05=1.,q95=1.,degenerate=True)
    return dict(a=k,b=n+1-k,mean=k/(n+1),q05=float(stats.beta.ppf(.05,k,n+1-k)),q95=float(stats.beta.ppf(.95,k,n+1-k)),degenerate=False)


def conformal_risk_control(loss_matrix,lambdas,alpha,B=1.):
    L,grid=np.asarray(loss_matrix,float),np.asarray(lambdas,float)
    if L.ndim!=2 or L.shape[1]!=len(grid) or not len(L):raise ValueError('nonempty loss matrix matching grid required')
    if not np.isfinite(L).all() or np.any(L<0) or np.any(L>B) or np.any(np.diff(L,axis=1)>1e-12):raise ValueError('bounded nonincreasing losses required')
    if np.any(np.diff(grid)<=0):raise ValueError('strictly increasing threshold grid required')
    ok=np.flatnonzero((L.sum(0)+B)/(len(L)+1)<=alpha)
    if not len(ok):raise ValueError('no certified threshold on the grid; a last-grid fallback is not certified')
    return float(grid[ok[0]])


def aci(scores,alpha=.1,gamma=.005,window=300,warm=300):
    """Inflated conformal quantiles; whole/empty sets outside the unit interval."""
    s=np.asarray(scores,float);a=alpha;thresholds=[];errors=[];levels=[]
    if not 0<alpha<1 or gamma<0:raise ValueError('valid alpha and nonnegative step size required')
    for t in range(warm,len(s)):
        q=np.inf if a<=0 else -np.inf if a>=1 else CF.conformal_quantile(s[max(0,t-window):t],a)
        e=float(s[t]>q);thresholds.append(q);errors.append(e);levels.append(a);a+=gamma*(alpha-e)
    return dict(threshold=np.array(thresholds),err=np.array(errors),alpha_t=np.array(levels),alpha_final=a,
                infinite_sets=int(np.isposinf(thresholds).sum()),empty_sets=int(np.isneginf(thresholds).sum()))


def gcc_dual(scores,groups_cal,groups_test_row,S,alpha=.1):
    """Canonical row order and duplicate averaging make the selected dual permutation equivariant."""
    G=np.vstack([groups_cal,groups_test_row]).astype(float);s=np.r_[scores,S].astype(float)
    rows=np.column_stack([G,s]);order=np.lexsort(rows.T[::-1]);ordered=rows[order]
    fit=optimize.linprog(-s[order],A_eq=G[order].T,b_eq=np.zeros(G.shape[1]),bounds=[(-alpha,1-alpha)]*len(s),method='highs')
    if not fit.success:raise ArithmeticError('conditional calibration LP failed: '+fit.message)
    eta=fit.x.copy()
    _,start,counts=np.unique(ordered,axis=0,return_index=True,return_counts=True)
    for i,c in zip(start,counts):
        if c>1:eta[i:i+c]=eta[i:i+c].mean()
    unsorted=np.empty_like(eta);unsorted[order]=eta
    if np.max(np.abs(G.T@unsorted),initial=0)>1e-7:raise ArithmeticError('dual equality residual too large')
    return float(unsorted[-1])


def gcc_group_threshold(scores,groups_cal,groups_test_row,alpha=.1):
    """Monotone dual-score inversion (paper Section 4), with a verified outer bracket."""
    s,G,g=np.asarray(scores,float),np.asarray(groups_cal,float),np.asarray(groups_test_row,float)
    Xa=np.vstack([G,g]);objective=np.r_[np.zeros(len(s)),-1.]
    geometry=optimize.linprog(objective,A_eq=Xa.T,b_eq=np.zeros(Xa.shape[1]),bounds=[(-alpha,1-alpha)]*len(Xa),method='highs')
    if not geometry.success:raise ArithmeticError('dual feasibility check failed')
    if geometry.x[-1]<1-alpha-1e-9:return np.inf
    def accept(S):return gcc_dual(s,G,g,S,alpha)<1-alpha-1e-9
    span=max(1.,float(np.ptp(s)));lo=float(s.min()-span);hi=float(s.max()+span)
    for _ in range(100):
        if accept(lo):break
        lo-=span;span*=2
    else:raise ArithmeticError('could not find accepted score bracket')
    for _ in range(100):
        if not accept(hi):break
        hi+=span;span*=2
    else:raise ArithmeticError('could not find rejected score bracket')
    for _ in range(35):
        mid=(lo+hi)/2
        if accept(mid):lo=mid
        else:hi=mid
    return hi  # outer approximation, error no larger than saved bisection bracket
