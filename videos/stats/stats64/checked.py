"""Audited evaluation kernels for Part 64; independent of earlier part sources."""
from explainer.stats.kit.evals import *  # noqa: F401,F403
import numpy as np
from scipy import stats,special,optimize,integrate
import math


def clustered_truth(acc,tau,m,G):
    f=lambda z:special.expit(special.logit(acc)+tau*z)
    mean=integrate.quad(lambda z:f(z)*stats.norm.pdf(z),-12,12,epsabs=1e-12)[0]
    second=integrate.quad(lambda z:f(z)**2*stats.norm.pdf(z),-12,12,epsabs=1e-12)[0]
    icc=(second-mean**2)/(mean*(1-mean))
    return dict(mean=mean,icc=icc,deff=1+(m-1)*icc,sd=np.sqrt(mean*(1-mean)*(1+(m-1)*icc)/(G*m)))


def rank_one_set(fit,cov,alpha=.05):
    fit=np.asarray(fit);K=len(fit);z=stats.norm.ppf(1-alpha/(K*(K-1)))
    pairvar=np.diag(cov)[:,None]+np.diag(cov)[None,:]-2*cov
    upper=fit[:,None]-fit[None,:]+z*np.sqrt(np.maximum(0,pairvar))
    # Candidate i remains if no j has a strictly positive lower bound for theta_j-theta_i.
    return [i for i in range(K) if np.all(upper[i]>=-1e-12)]


def logistic_checked(X,y):
    X,y=np.asarray(X,float),np.asarray(y,float)
    if np.linalg.matrix_rank(X)<X.shape[1]:raise ValueError('comparison design is rank deficient')
    w=np.zeros(X.shape[1]);objective=lambda b:np.sum(np.logaddexp(0,X@b)-y*(X@b))
    for it in range(100):
        p=special.expit(X@w);g=X.T@(p-y);H=(X*(p*(1-p))[:,None]).T@X
        if np.max(abs(g))<1e-7:break
        if np.linalg.eigvalsh(H)[0]<1e-10:raise ValueError('separation or singular information')
        step=np.linalg.solve(H,g);scale=1.;old=objective(w)
        while objective(w-scale*step)>old-1e-4*scale*(g@step)+1e-10:
            scale/=2
            if scale<1e-10:raise RuntimeError('logistic line search failed')
        w-=scale*step
    else:raise RuntimeError('logistic score failed to converge')
    p=special.expit(X@w);H=(X*(p*(1-p))[:,None]).T@X;Hi=np.linalg.inv(H);S=X*(y-p)[:,None]
    return w,Hi,Hi@(S.T@S)@Hi,float(np.max(abs(X.T@(p-y))))


def bt_fit(i,j,y,K,ref=0,iters=100):
    i,j,y=np.asarray(i,int),np.asarray(j,int),np.asarray(y,float);n=len(y)
    from scipy.sparse.csgraph import connected_components
    wins=np.zeros((K,K));wins[np.where(y==1,i,j),np.where(y==1,j,i)]=1
    if connected_components(wins,directed=True,connection="strong")[0]!=1:raise ValueError("finite Bradley-Terry MLE needs a strongly connected win graph")
    X=np.zeros((n,K));X[np.arange(n),i]+=1;X[np.arange(n),j]-=1;keep=[k for k in range(K) if k!=ref]
    w,V,W,score=logistic_checked(X[:,keep],y);theta=np.zeros(K);theta[keep]=w
    cov=np.zeros((K,K));sw=np.zeros((K,K));cov[np.ix_(keep,keep)]=V;sw[np.ix_(keep,keep)]=W
    return dict(theta=theta,se=np.sqrt(np.diag(cov)),se_sandwich=np.sqrt(np.diag(sw)),cov=cov,cov_sandwich=sw,score_max=score)


def bt_bootstrap(i,j,y,K,B,rng,ref=0):
    i,j,y=map(np.asarray,(i,j,y));out=[]
    for _ in range(B):
        ix=rng.integers(0,len(y),len(y));out.append(bt_fit(i[ix],j[ix],y[ix],K,ref)['theta'])
    return np.array(out)


def bt_style_fit(i,j,y,K,style,ref=0):
    n=len(y);X=np.zeros((n,K));X[np.arange(n),i]+=1;X[np.arange(n),j]-=1;keep=[k for k in range(K) if k!=ref]
    Z=np.column_stack([X[:,keep],np.asarray(style).reshape(n,-1)]);w,V,W,score=logistic_checked(Z,y);theta=np.zeros(K);theta[keep]=w[:K-1]
    return dict(theta=theta,gamma=w[K-1:],score_max=score)


def gaussian_collapse(n,T,reps,rng,accumulate=False):
    # Both experiments start from fitted moments mu0=0, variance0=1.
    paths=np.ones((reps,T+1))
    for k in range(reps):
        pool=rng.standard_normal(n);pool=(pool-pool.mean())/pool.std();mu,s2=0.,1.
        for t in range(1,T+1):
            new=mu+np.sqrt(s2)*rng.standard_normal(n)
            if accumulate:pool=np.concatenate([pool,new]);mu,s2=pool.mean(),pool.var()
            else:mu,s2=new.mean(),new.var()
            paths[k,t]=s2
    return dict(paths=paths,expected=((n-1)/n)**np.arange(T+1),drift=float(special.digamma((n-1)/2)+np.log(2/n)))


def watermark_power(T,gamma,delta,z_thr,entropy_frac=1.,edit_frac=0.):
    q=(1-edit_frac)*(entropy_frac*green_prob(gamma,delta)+(1-entropy_frac)*gamma)+edit_frac*gamma
    need=math.floor(gamma*T+z_thr*np.sqrt(T*gamma*(1-gamma)))+1
    return float(stats.binom.sf(need-1,T,q))


def probability_flow(score_fn,sigmas,n,rng,initial=None):
    sigmas=np.asarray(sigmas)
    if not np.all(np.diff(sigmas)<0) or sigmas[-1]<=0:raise ValueError('strictly descending positive noise grid required')
    x=sigmas[0]*rng.standard_normal(n) if initial is None else np.asarray(initial,float).copy()
    for s0,s1 in zip(sigmas[:-1],sigmas[1:]):
        d0=-s0*score_fn(x,s0);xe=x+(s1-s0)*d0;d1=-s1*score_fn(xe,s1);x+=(s1-s0)*.5*(d0+d1)
    if not np.isfinite(x).all():raise RuntimeError('nonfinite probability flow')
    return x


def sbi_comparison(n_sim,p_feat,level,reps,rng,n_obs=10):
    def feats(x):return np.column_stack([x**k for k in range(p_feat+1)])
    th=rng.standard_normal(n_sim);xb=th+rng.standard_normal(n_sim)/np.sqrt(n_obs);F=feats(xb/2)
    beta=np.linalg.lstsq(F,th,rcond=None)[0];s_train=np.mean((th-F@beta)**2)
    tc=rng.standard_normal(n_sim);xc=tc+rng.standard_normal(n_sim)/np.sqrt(n_obs);s_cal=np.mean((tc-feats(xc/2)@beta)**2)
    tt=rng.standard_normal(reps);xt=tt+rng.standard_normal(reps)/np.sqrt(n_obs);err=tt-feats(xt/2)@beta
    z=stats.norm.ppf((1+level)/2)
    exact_mean=n_obs/(n_obs+1)*xt;exact_sd=1/np.sqrt(n_obs+1)
    return dict(insample=float(np.mean(abs(err)<=z*np.sqrt(s_train))),heldout=float(np.mean(abs(err)<=z*np.sqrt(s_cal))),exact=float(np.mean(abs(tt-exact_mean)<=z*exact_sd)))


def fit_2pl(R,iters=25,ridge=.01):
    """Bounded penalized joint 2PL fit; checked optimizer, no global-optimum claim."""
    from explainer.stats.kit.evals import fit_2pl as initialize
    R=np.asarray(R,float);M,J=R.shape;f=initialize(R,iters=iters,ridge=ridge)
    start=np.r_[np.clip(f['theta'],-8,8),np.clip(f['a'],.05,6),np.clip(f['b'],-6,6)]
    def objective(v):
        th,a,b=v[:M],v[M:M+J],v[M+J:];diff=th[:,None]-b;z=a*diff;r=special.expit(z)-R
        loss=np.sum(np.logaddexp(0,z)-R*z)+ridge/2*(th@th+(a-1)@(a-1)+b@b)
        grad=np.r_[(r*a).sum(1)+ridge*th,(r*diff).sum(0)+ridge*(a-1),-(r*a).sum(0)+ridge*b]
        return loss,grad
    bounds=[(-8,8)]*M+[(.05,6)]*J+[(-6,6)]*J
    out=optimize.minimize(objective,start,jac=True,method='L-BFGS-B',bounds=bounds,options=dict(maxiter=4000,ftol=1e-15,gtol=2e-6,maxcor=20))
    loss,grad=objective(out.x);projected=out.x-np.array([np.clip(v-g,lo,hi) for v,g,(lo,hi) in zip(out.x,grad,bounds)])
    if not out.success or np.max(abs(projected))>2e-3:raise RuntimeError(f'2PL optimizer: {out.message}, projected score {np.max(abs(projected))}')
    th,a,b=out.x[:M],out.x[M:M+J],out.x[M+J:];mu,sd=th.mean(),th.std()
    return dict(theta=(th-mu)/sd,a=a*sd,b=(b-mu)/sd,objective=float(loss),projected_score=float(np.max(abs(projected))),iterations=out.nit,scope='bounded penalized local optimum; final affine standardization preserves all logits')
