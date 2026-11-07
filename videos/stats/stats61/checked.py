"""Audited numerical kernels for Part 61; convergence and empirical targets explicit."""
from __future__ import annotations
import math
import numpy as np
from scipy import optimize,special,sparse
from explainer.stats.kit.ot import *  # noqa: F403


def mcse(values):
    a=np.asarray(values,float)
    return float(a.std(ddof=1)/np.sqrt(len(a)))


def quantile_atoms(samples,weights=None):
    """Exact step-quantile barycenter atoms and masses, not linear interpolation."""
    arrays=[np.sort(np.asarray(x,float)) for x in samples]
    if not arrays or any(x.ndim!=1 or not len(x) or not np.isfinite(x).all() for x in arrays):
        raise ValueError('nonempty finite scalar samples required')
    w=np.full(len(arrays),1/len(arrays)) if weights is None else np.asarray(weights,float)
    if w.shape!=(len(arrays),) or np.any(w<0) or not np.isclose(w.sum(),1):
        raise ValueError('proper barycenter weights required')
    edges=np.unique(np.r_[0.,*[np.arange(1,len(x)+1)/len(x) for x in arrays]])
    mass=np.diff(edges);u=(edges[:-1]+edges[1:])/2
    Q=np.array([x[np.minimum((u*len(x)).astype(int),len(x)-1)] for x in arrays])
    atoms=w@Q;mean=float(mass@atoms)
    return dict(values=atoms,mass=mass,quantiles=Q,mean=mean,
                sd=float(np.sqrt(mass@((atoms-mean)**2))))


def quantile_decomposition(x,y):
    a=quantile_atoms([x,y]);mass=a['mass'];qx,qy=a['quantiles']
    mx,my=mass@qx,mass@qy
    sx,sy=np.sqrt(mass@((qx-mx)**2)),np.sqrt(mass@((qy-my)**2))
    covariance=float(mass@((qx-mx)*(qy-my)))
    location=float((mx-my)**2);spread=float((sx-sy)**2)
    shape=float(2*(sx*sy-covariance));total=float(mass@((qx-qy)**2))
    return dict(location=location,spread=spread,shape=shape,total=total,
                rho=float(covariance/(sx*sy)) if sx*sy else None,
                residual=float(total-location-spread-shape))


def barycenter_1d(samples,weights=None,grid=400):
    a=quantile_atoms(samples,weights)
    u=(np.arange(grid)+.5)/grid
    return a['values'][np.minimum(np.searchsorted(np.cumsum(a['mass']),u,side='right'),len(a['values'])-1)]


def _problem(a,b,C,positive=False):
    a,b,C=np.asarray(a,float),np.asarray(b,float),np.asarray(C,float)
    if (a.ndim!=1 or b.ndim!=1 or C.shape!=(len(a),len(b)) or not len(a) or not len(b)
        or not np.isfinite(C).all() or not np.isfinite(a).all() or not np.isfinite(b).all()
        or np.any(a<0) or np.any(b<0) or not np.isclose(a.sum(),1,atol=1e-12)
        or not np.isclose(b.sum(),1,atol=1e-12)):
        raise ValueError('finite cost and probability marginals required')
    if positive and (np.any(a<=0) or np.any(b<=0)):
        raise ValueError('positive Sinkhorn marginals required')
    return a,b,C


def kantorovich_lp(a,b,C):
    a,b,C=_problem(a,b,C);n,m=C.shape
    A=sparse.vstack([sparse.kron(sparse.eye(n),np.ones((1,m))),
                     sparse.kron(np.ones((1,n)),sparse.eye(m))],format='csr')
    res=optimize.linprog(C.ravel(),A_eq=A[:-1],b_eq=np.r_[a,b][:-1],bounds=(0,None),method='highs')
    if not res.success:raise RuntimeError(f'transport LP failed: {res.message}')
    P=res.x.reshape(n,m);dual=np.r_[res.eqlin.marginals,0.];f,g=dual[:n],dual[n:]
    marginal=max(np.max(np.abs(P.sum(1)-a)),np.max(np.abs(P.sum(0)-b)))
    violation=float(np.max(f[:,None]+g[None,:]-C));gap=float(res.fun-a@f-b@g)
    if marginal>1e-8 or violation>1e-8 or abs(gap)>1e-8*(1+abs(res.fun)):
        raise RuntimeError('transport LP primal/dual residual failed')
    return dict(P=P,cost=float(res.fun),f=f,g=g,
                audit=dict(marginal_residual=float(marginal),dual_violation=violation,duality_gap=gap))


def sinkhorn(a,b,C,eps,iters=50000,tol=1e-9,accelerate=False):
    """Log scaling for cost + eps KL(P || a tensor b); fail on exhaustion."""
    a,b,C=_problem(a,b,C,True)
    if not np.isfinite(eps) or eps<=0 or iters<1 or tol<=0:raise ValueError('positive epsilon, iterations and tolerance required')
    la,lb=np.log(a),np.log(b);f=np.zeros(len(a));g=np.zeros(len(b));errors=[]
    scaling_budget=min(iters,500) if accelerate else iters
    for _ in range(scaling_budget):
        f=-eps*special.logsumexp((g[None,:]-C)/eps+lb[None,:],axis=1)
        g=-eps*special.logsumexp((f[:,None]-C)/eps+la[:,None],axis=0)
        shift=g[-1];g-=shift;f+=shift
        logP=(f[:,None]+g[None,:]-C)/eps+la[:,None]+lb[None,:]
        P=np.exp(logP)
        err=float(max(np.abs(P.sum(1)-a).sum(),np.abs(P.sum(0)-b).sum()))
        errors.append(err)
        if err<tol:break
    if err>=tol and accelerate:
        # Eliminate the row potential; optimize the remaining convex dual.
        # Its Hessian is a sum of categorical covariances. Fix g[-1]=0.
        def reduced(g):
            lognormal=special.logsumexp((g[None,:]-C)/eps+lb[None,:],axis=1)
            f=-eps*lognormal
            P=a[:,None]*np.exp((g[None,:]-C)/eps+lb[None,:]-lognormal[:,None])
            return float(eps*(a@lognormal)-b@g),f,P
        for _ in range(min(300,iters-scaling_budget)):
            value,f,P=reduced(g);column=P.sum(0);gradient=column-b
            err=float(np.abs(gradient).sum());errors.append(err)
            if err<tol:break
            H=(np.diag(column)-P.T@(P/a[:,None]))/eps
            H=H[:-1,:-1];regularizer=1e-12*max(1.,np.max(np.diag(H)))
            direction=np.r_[np.linalg.solve(H+regularizer*np.eye(len(H)),gradient[:-1]),0.]
            fraction=1.
            for _ in range(45):
                candidate=g-fraction*direction
                new,_,newP=reduced(candidate)
                newerr=float(np.abs(newP.sum(0)-b).sum())
                if (new<=value-1e-4*fraction*(gradient@direction)
                    or (new<=value+1e-12*(1+abs(value)) and newerr<err)):
                    g=candidate;break
                fraction/=2
            else:raise RuntimeError('reduced transport dual Newton line search failed')
        value,f,P=reduced(g)
        err=float(max(np.abs(P.sum(1)-a).sum(),np.abs(P.sum(0)-b).sum()))
    if err>=tol:raise RuntimeError(f'Sinkhorn not converged: epsilon={eps}, residual={err}, budget={iters}')
    cost=float(np.sum(P*C))
    relative_entropy=float(np.sum(special.xlogy(P,P))-np.sum(P*(la[:,None]+lb[None,:])))
    objective=cost+eps*relative_entropy
    dual=float(a@f+b@g-eps*(P.sum()-1))
    return dict(P=P,cost=cost,obj=objective,f=f,g=g,errs=errors,iters=len(errors),
                audit=dict(converged=True,marginal_l1=err,tolerance=tol,
                           algorithm='log scaling with reduced-dual Newton refinement' if accelerate else 'log scaling',
                           relative_entropy=relative_entropy,dual=dual,primal_dual_difference=objective-dual,
                           objective_convention='cost + epsilon KL(P || a tensor b)'))


def sinkhorn_divergence(X,Y,eps,p=2.):
    X,Y=np.asarray(X,float),np.asarray(Y,float)
    a,b=np.full(len(X),1/len(X)),np.full(len(Y),1/len(Y))
    def ot(U,V,u,v):return sinkhorn(u,v,cost_matrix(U,V,p),eps,50000,1e-8)['obj']
    return float(ot(X,Y,a,b)-.5*(ot(X,X,a,a)+ot(Y,Y,b,b)))


def entropic_map(X,Y,eps):
    X,Y=np.asarray(X,float),np.asarray(Y,float)
    s=sinkhorn(np.full(len(X),1/len(X)),np.full(len(Y),1/len(Y)),cost_matrix(X,Y,2)/2,eps,50000,1e-10,accelerate=True)
    def T(Z):
        L=(s['g'][None,:]-cost_matrix(np.atleast_2d(Z),Y,2)/2)/eps
        W=np.exp(L-special.logsumexp(L,axis=1,keepdims=True))
        return W@Y
    T.audit=s['audit']
    return T


def empirical_rate(d,ns,reps,rng,p=1.):
    draws=[[assignment(rng.random((n,d)),rng.random((n,d)),p)['W'] for _ in range(reps)] for n in ns]
    means=np.mean(draws,axis=1)
    return dict(ns=list(ns),W=means,slope=float(np.polyfit(np.log(ns),np.log(means),1)[0]),
                draws=draws,mcse=[mcse(v) for v in draws],reps=reps)


def rank_energy_test(X,Y,rng,perms=200,ref=None):
    """Pooled assignment with randomized tie order; cached rank distances."""
    X,Y=np.atleast_2d(X),np.atleast_2d(Y);Z=np.vstack([X,Y]);N,n=len(Z),len(X)
    if ref is None:
        ref=stats.qmc.Halton(d=Z.shape[1],scramble=False).random(N+1)[1:]
    ref=np.asarray(ref,float)
    if ref.shape!=Z.shape or len(np.unique(ref,axis=0))!=N:
        raise ValueError('one distinct fixed reference point per observation required')
    order=rng.permutation(N)
    rows,cols=optimize.linear_sum_assignment(cost_matrix(Z[order],ref,2))
    R=np.empty_like(ref);R[order[rows]]=ref[cols]
    D=cost_matrix(R,R,1)
    def statistic(order):
        left,right=order[:n],order[n:]
        return float(2*D[np.ix_(left,right)].mean()-D[np.ix_(left,left)].mean()-D[np.ix_(right,right)].mean())
    observed=statistic(np.arange(N));null=np.array([statistic(rng.permutation(N)) for _ in range(perms)])
    return dict(stat=observed,p=float((1+np.sum(null>=observed-1e-12))/(1+perms)),
                scope='independent IID null; fixed reference; randomized pooled tie order; plus-one permutations')


def gaussian_ula(m0,S0,mu,Sig,h,steps):
    Sig=np.asarray(Sig,float);mu=np.asarray(mu,float)
    if not 0<h<2*np.linalg.eigvalsh(Sig).min():raise ValueError('stable Gaussian Euler step required')
    M=np.eye(len(mu))-h*np.linalg.inv(Sig);E=np.linalg.matrix_power(M,steps)
    w,V=np.linalg.eigh(Sig);stationary=(V*(w/(1-h/(2*w))))@V.T
    return mu+E@(m0-mu), E@S0@E.T+stationary-E@stationary@E.T


def gaussian_barycenter(covs,weights=None,iters=1000,tol=1e-11):
    covs=[np.atleast_2d(np.asarray(c,float)) for c in covs]
    w=np.full(len(covs),1/len(covs)) if weights is None else np.asarray(weights,float)
    if not np.isclose(w.sum(),1) or np.any(w<0):raise ValueError('proper barycenter weights required')
    if any(not np.allclose(c,c.T) or np.linalg.eigvalsh(c).min()<=0 for c in covs):
        raise ValueError('positive-definite covariances required for this fixed-point algorithm')
    S=sum(v*c for v,c in zip(w,covs))
    for _ in range(iters):
        root=sqrtm_psd(S);inv=np.linalg.inv(root)
        M=sum(v*sqrtm_psd(root@c@root) for v,c in zip(w,covs))
        if np.max(np.abs(S-M))<tol*(1+np.max(np.abs(S))):return (S+S.T)/2
        S=inv@M@M@inv
    raise RuntimeError('Gaussian barycenter fixed point did not converge')
