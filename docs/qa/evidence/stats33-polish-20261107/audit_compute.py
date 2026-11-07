"""Verified compiled coordinate descent for the Part 33 knockoff/CV audit.

The scene computation retains its teaching solver. This audit substitute uses
the same objective, path grid and preprocessing and checks every lasso KKT
condition. It replaces lasso_path and lasso_cd; the Board samplers remain unchanged.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
import numpy as np
from sklearn.linear_model import Lasso
from videos.stats.stats33 import compute as C
def compiled_path(X,y,lams=None,nlam=100,eps=1e-3,alpha=1.,weights=None):
    assert alpha==1 and weights is None
    if lams is None:lams=C.SP.lam_max(X,y)*np.logspace(0,np.log10(eps),nlam)
    fit=Lasso(fit_intercept=False,warm_start=True,tol=1e-12,max_iter=100000,selection='cyclic')
    coefs=[]
    for lam in lams:
        fit.set_params(alpha=float(lam));fit.fit(X,y);b=fit.coef_.copy()
        k=C.SP.kkt(X,y,b,lam)
        error=max(k['on_err'],k['off_max']-lam,0)
        if error>2e-7:raise RuntimeError(f"compiled path KKT residual {error}")
        coefs.append(b)
    B=np.array(coefs)
    return dict(lams=np.asarray(lams),coefs=B,df=(B!=0).sum(1))
def compiled_cd(X,y,lam,alpha=1.,weights=None,**kwargs):
    return compiled_path(X,y,[lam],alpha=alpha,weights=weights)["coefs"][0]
C.SP.lasso_path=compiled_path
C.SP.lasso_cd=compiled_cd
sys.argv=[__file__,'--force','knock','fcr','board']
C.CACHE.main(C.ITEMS,C.__doc__)
