"""Audited Part 60 kernels; numerical demonstrations have explicitly limited scopes."""
from __future__ import annotations
import math
import numpy as np
from scipy import optimize,special,stats
from explainer.stats.kit.shift import *  # noqa: F403


def mcse(values):
    a=np.asarray(values,float)
    return float(a.std(ddof=1)/math.sqrt(len(a)))


def tukey_depth_2d(points,data,n_dirs=None):
    """Closed-halfplane depth by an angular sweep, not a finite direction grid."""
    X=np.asarray(data,float);P=np.atleast_2d(np.asarray(points,float))
    if len(X)==0:raise ValueError("nonempty data required")
    result=[]
    for p in P:
        v=X-p
        nonzero=np.linalg.norm(v,axis=1)>1e-12
        angle=np.sort(np.arctan2(v[nonzero,1],v[nonzero,0]))
        if not len(angle):
            result.append(1.);continue
        doubled=np.r_[angle,angle+2*math.pi]
        ends=np.searchsorted(doubled,angle+math.pi-1e-12,side="left")
        largest=int(np.max(np.minimum(ends-np.arange(len(angle)),len(angle))))
        result.append((len(X)-largest)/len(X))
    return np.array(result)


def tukey_median_2d(data,grid=60):
    """Grid approximation to the global depth maximum; exact depth at candidates."""
    X=np.asarray(data,float);lo,hi=X.min(0),X.max(0)
    G=np.array([[a,b] for a in np.linspace(lo[0],hi[0],grid)
                       for b in np.linspace(lo[1],hi[1],grid)])
    D=tukey_depth_2d(G,X)
    estimate=G[D==D.max()].mean(0)
    return dict(median=estimate,depth=float(tukey_depth_2d(estimate,X)[0]),
                grid=G,depth_grid=D,scope=f"grid-{grid} approximate median; angular-sweep depths")


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


def logistic_density_ratio(Xs,Xt,lam=1e-3,iters=80):
    Xs,Xt=np.atleast_2d(Xs),np.atleast_2d(Xt)
    Z=np.vstack([Xs,Xt]);Z=np.column_stack([np.ones(len(Z)),Z])
    result=_logit(Z,np.r_[np.zeros(len(Xs)),np.ones(len(Xt))],lam,iters)
    return lambda X:len(Xs)/len(Xt)*np.exp(np.column_stack([np.ones(len(np.atleast_2d(X))),np.atleast_2d(X)])@result['beta'])


def ratio_weighted_mean_ci(Xs,y,Xt,alpha=.05,lam=1e-3):
    """Joint fixed-stratum sandwich for estimated logistic ratio and Hajek mean.

    IID source/target draws, correct logistic density-ratio model, overlap and
    regularity are required for the asymptotic normal interval.
    """
    Xs,Xt,y=np.asarray(Xs,float),np.asarray(Xt,float),np.asarray(y,float)
    ns,nt=len(Xs),len(Xt)
    Z=np.column_stack([np.ones(ns+nt),np.vstack([Xs,Xt])])
    labels=np.r_[np.zeros(ns),np.ones(nt)]
    fit=_logit(Z,labels,lam)
    w=(ns/nt)*np.exp(Z[:ns]@fit['beta'])
    total=w.sum();mean=float(w@y/total)
    d=Z.shape[1]
    bread=np.zeros((d+1,d+1));bread[:d,:d]=fit['H']
    bread[d,:d]=-((w*(y-mean))[:,None]*Z[:ns]).sum(0)
    bread[d,d]=total
    score=np.column_stack([Z*(labels-fit['prob'])[:,None],np.r_[w*(y-mean),np.zeros(nt)]])
    influence=np.linalg.solve(bread,score.T).T[:,-1]
    variance=0.
    for values in (influence[:ns],influence[ns:]):
        variance+=np.sum((values-values.mean())**2)*len(values)/(len(values)-1)
    se=math.sqrt(variance);crit=stats.norm.isf(alpha/2)
    naive=weighted_mean_ci(y,w)
    return dict(mean=mean,se=se,lo=mean-crit*se,hi=mean+crit*se,ess=kish_ess(w),
                weights=w,naive_fixed_weight_se=naive['se'],
                logistic_score_residual=fit['score_residual'],
                variance_scope="joint ratio-fit/mean sandwich, centered within fixed source and target strata")


def bbse_weights(pred_src,y_src,pred_tgt,K):
    pred_src,y_src,pred_tgt=(np.asarray(v,int) for v in (pred_src,y_src,pred_tgt))
    count=np.bincount(y_src,minlength=K)
    if np.any(count==0):raise ValueError("every source class needs calibration observations")
    C=np.zeros((K,K))
    np.add.at(C,(pred_src,y_src),1)
    conditional=C/count[None,:]
    if np.linalg.matrix_rank(conditional)<K:raise ValueError("singular confusion matrix: prevalence not identified")
    target=np.bincount(pred_tgt,minlength=K)/len(pred_tgt)
    if K==2:
        q1=float(np.clip((target[1]-conditional[1,0])/(conditional[1,1]-conditional[1,0]),0,1))
        q=np.array([1-q1,q1])
    else:
        fit=optimize.minimize(lambda q:np.sum((conditional@q-target)**2),np.full(K,1/K),
            jac=lambda q:2*conditional.T@(conditional@q-target),
            constraints={"type":"eq","fun":lambda q:q.sum()-1,"jac":lambda q:np.ones(K)},
            bounds=[(0,1)]*K,method="SLSQP",options={"ftol":1e-13,"maxiter":1000})
        if not fit.success or abs(fit.x.sum()-1)>1e-8:raise RuntimeError("simplex BBSE solve failed")
        q=fit.x
    p=count/len(y_src)
    return dict(w=q/p,q=q,C=C/len(y_src),mu=target,
                condition_number=float(np.linalg.cond(conditional)),
                moment_residual=float(np.linalg.norm(conditional@q-target)))


def _loss_scale(losses,rho):
    l=np.asarray(losses,float)
    if l.ndim!=1 or not len(l) or not np.isfinite(l).all() or not np.isfinite(rho) or rho<0:
        raise ValueError("finite losses and nonnegative finite radius required")
    center=float(l.min());scale=float(l.max()-center)
    return l,center,scale


def dro_chi2(losses,rho,return_audit=False):
    """Scalar KKT solve, with a feasible primal and a checked dual upper bound."""
    l,center,scale=_loss_scale(losses,rho);n=len(l)
    if scale==0 or rho==0:
        q=np.full(n,1/n);upper=primal=float(q@l);div=0.
    else:
        z=(l-center)/scale;ties=z==1
        if rho>=(n/ties.sum()-1)/2:
            q=ties/ties.sum();upper=primal=float(l.max());div=.5*np.mean((n*q-1)**2)
        else:
            def candidate(eta):
                excess=np.maximum(z-eta,0)
                q=excess/excess.sum()
                return q,.5*np.mean((n*q-1)**2)
            low=-1.
            while candidate(low)[1]>rho:low*=2
            eta=optimize.brentq(lambda e:candidate(e)[1]-rho,low,1-1e-14,xtol=1e-12)
            q,div=candidate(eta)
            upper=center+scale*(eta+math.sqrt((1+2*rho)*np.mean(np.maximum(z-eta,0)**2)))
            primal=float(q@l)
    if div>rho+1e-8 or upper<primal-1e-8*(1+abs(primal)) or upper-primal>1e-7*(1+abs(upper)):
        raise RuntimeError("chi-square primal/dual certificate failed")
    audit=dict(value=float(max(upper,primal)),primal=primal,dual_upper=float(upper),
               divergence=float(div),q=q,gap=float(upper-primal),radius=rho)
    return audit if return_audit else audit['value']


def dro_kl(losses,rho,return_audit=False):
    l,center,scale=_loss_scale(losses,rho);n=len(l)
    if scale==0 or rho==0:
        q=np.full(n,1/n);upper=primal=float(q@l);div=0.
    else:
        z=(l-center)/scale;ties=z==1
        if rho>=math.log(n/ties.sum()):
            q=ties/ties.sum();upper=primal=float(l.max());div=math.log(n/ties.sum())
        else:
            def candidate(beta):
                logw=beta*z-special.logsumexp(beta*z)
                q=np.exp(logw)
                divergence=float(np.sum(special.xlogy(q,q*n)))
                return q,divergence
            high=1.
            while candidate(high)[1]<rho:high*=2
            beta=optimize.brentq(lambda b:candidate(b)[1]-rho,0,high,xtol=1e-12)
            q,div=candidate(beta)
            primal=float(q@l)
            upper=center+scale*(special.logsumexp(beta*z)-math.log(n)+rho)/beta
    if div>rho+1e-8 or upper<primal-1e-8*(1+abs(primal)) or upper-primal>1e-7*(1+abs(upper)):
        raise RuntimeError("KL primal/dual certificate failed")
    audit=dict(value=float(max(upper,primal)),primal=primal,dual_upper=float(upper),
               divergence=float(div),q=q,gap=float(upper-primal),radius=rho)
    return audit if return_audit else audit['value']

def anchor_regression(X,y,A,gamma):
    """Apply the anchor projection without materializing n-by-n matrices."""
    X,y,A=np.asarray(X,float),np.asarray(y,float),np.asarray(A,float)
    if A.ndim==1:A=A[:,None]
    if A.shape[0]!=len(y):A=A.T
    if gamma<0:raise ValueError("nonnegative anchor penalty required")
    U,s,_=np.linalg.svd(A,full_matrices=False)
    Q=U[:,s>np.finfo(float).eps*max(A.shape)*s.max()]
    coefficient=1-math.sqrt(gamma)
    return np.linalg.lstsq(X-coefficient*Q@(Q.T@X),
                          y-coefficient*Q@(Q.T@y),rcond=None)[0]


def icp(X,y,env,alpha=.05):
    """Gaussian linear ICP using coefficient and residual-variance invariance.

    Tests the common conditional linear-Gaussian model at each candidate subset.
    This supplies the parent-subset test needed for the intersection guarantee;
    it is not a distribution-free residual ANOVA/Levene test.
    """
    from itertools import combinations
    X,y,env=np.asarray(X,float),np.asarray(y,float),np.asarray(env)
    accepted=[];pvals={};diagnostics={}
    environments=np.unique(env)
    if len(environments)<2:
        raise ValueError("ICP needs at least two environments")
    for k in range(X.shape[1]+1):
        for subset in combinations(range(X.shape[1]),k):
            Z=np.column_stack([np.ones(len(y)),X[:,subset]]) if subset else np.ones((len(y),1))
            pooled=np.linalg.lstsq(Z,y,rcond=None)[0]
            rss_pool=float(np.sum((y-Z@pooled)**2));rank_pool=np.linalg.matrix_rank(Z)
            rss=[];df=[];ranks=[]
            for e in environments:
                mask=env==e;design=Z[mask];rank=np.linalg.matrix_rank(design)
                residual=y[mask]-design@np.linalg.lstsq(design,y[mask],rcond=None)[0]
                rss.append(float(residual@residual));ranks.append(rank);df.append(int(mask.sum()-rank))
            if min(df)<=0 or min(rss)<=0:
                raise ValueError("each environment needs positive Gaussian residual degrees of freedom")
            full_rss=sum(rss);numerator_df=sum(ranks)-rank_pool;denominator_df=sum(df)
            chow=max(0.,(rss_pool-full_rss)/numerator_df)/(full_rss/denominator_df)
            coefficient_p=float(stats.f.sf(chow,numerator_df,denominator_df))
            variance_p=1.
            pairs=list(combinations(range(len(environments)),2))
            for a,b in pairs:
                ratio=(rss[a]/df[a])/(rss[b]/df[b])
                pv=2*min(stats.f.cdf(ratio,df[a],df[b]),stats.f.sf(ratio,df[a],df[b]))
                variance_p=min(variance_p,len(pairs)*pv)
            pvalue=min(1.,2*min(coefficient_p,variance_p))
            pvals[str(subset)]=pvalue
            diagnostics[str(subset)]=dict(coefficient_p=coefficient_p,variance_p=variance_p,
                coefficient_f=chow,coefficient_df=[numerator_df,denominator_df],
                residual_df=df)
            if pvalue>alpha:accepted.append(set(subset))
    estimate=set.intersection(*accepted) if accepted else set()
    return dict(estimate=sorted(estimate),accepted=[sorted(a) for a in accepted],
                pvals=pvals,diagnostics=diagnostics,
                scope="Gaussian independent homoskedastic parent errors and valid environments; no intervention on outcome mechanism")


def em_label_shift(probs_tgt,p_src,iters=500):
    P,p=np.asarray(probs_tgt,float),np.asarray(p_src,float)
    if np.any(p<=0) or np.any(P<0) or not np.allclose(P.sum(1),1):
        raise ValueError("proper source posteriors and positive source priors required")
    q=p.copy();converged=False
    for iteration in range(iters):
        R=P*(q/p)[None,:];R/=R.sum(1,keepdims=True)
        qn=R.mean(0)
        difference=float(np.max(np.abs(qn-q)))
        q=qn
        if difference<1e-12:
            converged=True;break
    R=P*(q/p)[None,:];R/=R.sum(1,keepdims=True)
    return dict(q=q,posterior=R,converged=converged,iterations=iteration+1,
                residual=float(np.max(np.abs(R.mean(0)-q))))


def _mmd_kernel(X,Y,bw=None):
    X,Y=np.atleast_2d(X),np.atleast_2d(Y)
    if min(len(X),len(Y))<2:raise ValueError("two observations per sample required")
    Z=np.vstack([X,Y]);D=((Z[:,None,:]-Z[None,:,:])**2).sum(2)
    if bw is None:
        off=D[np.triu_indices(len(Z),1)]
        positive=off[off>0]
        bw=math.sqrt(np.median(positive)/2) if len(positive) else 1.
    if bw<=0:raise ValueError("positive bandwidth required")
    return np.exp(-D/(2*bw*bw)),float(bw)


def _mmd_from_kernel(K,left,right):
    xx=K[np.ix_(left,left)];yy=K[np.ix_(right,right)];xy=K[np.ix_(left,right)]
    n,m=len(left),len(right)
    return float((xx.sum()-np.trace(xx))/(n*(n-1))
                +(yy.sum()-np.trace(yy))/(m*(m-1))-2*xy.mean())


def mmd2(X,Y,bw=None):
    K,_=_mmd_kernel(X,Y,bw)
    n=len(X);return _mmd_from_kernel(K,np.arange(n),np.arange(n,len(K)))


def mmd_test(X,Y,rng,perms=300):
    K,bw=_mmd_kernel(X,Y)
    n=len(X);obs=_mmd_from_kernel(K,np.arange(n),np.arange(n,len(K)))
    null=[]
    for _ in range(perms):
        order=rng.permutation(len(K))
        null.append(_mmd_from_kernel(K,order[:n],order[n:]))
    null=np.array(null)
    return dict(mmd2=obs,p=float((1+np.sum(null>=obs-1e-14))/(perms+1)),
                null=null,bandwidth=bw,scope="pooled label-invariant bandwidth; independent IID samples under null")


def classifier_holdout_test(source_prediction,target_prediction):
    """Exact balanced-label randomization test, classifier fixed before holdout."""
    left,right=np.asarray(source_prediction,int),np.asarray(target_prediction,int)
    if len(left)!=len(right):raise ValueError("this display uses equal test-group sizes")
    n=len(left);total_positive=int(left.sum()+right.sum());source_positive=int(left.sum())
    correct=source_positive+int((right==0).sum())
    return dict(acc=correct/(2*n),p_acc=float(stats.hypergeom.sf(source_positive-1,2*n,total_positive,n)),
                correct=correct,pooled_positive=total_positive,source_positive=source_positive,
                scope="conditional hypergeometric test on independent held-out IID samples")


def quantile_interval(values,q,alpha=.05):
    a=np.sort(values);n=len(a)
    k=int(stats.binom.ppf(alpha/2,n,q));l=int(stats.binom.ppf(1-alpha/2,n,q))+1
    return [float(a[k-1]) if k else -math.inf,float(a[l-1]) if l<=n else math.inf]

def weighted_mean_ci(y,w,alpha=.05):
    y,w=np.asarray(y,float),np.asarray(w,float)
    if len(y)<2 or y.shape!=w.shape or np.any(w<0) or w.sum()<=0 or not np.isfinite([y,w]).all():
        raise ValueError("finite equal-length observations and nonnegative weights required")
    W=w/w.sum();m=float(W@y)
    se=math.sqrt(float(np.sum(W*W*(y-m)**2))*len(y)/(len(y)-1))
    crit=stats.norm.isf(alpha/2)
    return dict(mean=m,se=se,lo=m-crit*se,hi=m+crit*se,ess=kish_ess(w))
