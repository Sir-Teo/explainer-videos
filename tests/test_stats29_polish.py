"""Independent references for the Part 29 smoothing corrections."""
import math

import numpy as np
import pytest
from scipy import integrate, interpolate, optimize, stats

from explainer.stats.kit import smooth as Sm
from videos.stats.stats29 import compute as C


def test_histogram_minimum_constant_against_scalar_optimization():
    roughness=C.GEYSER.R(1)
    for n in (100,1000,10000):
        result=optimize.minimize_scalar(lambda logh: 1/(n*np.exp(logh))+np.exp(2*logh)*roughness/12,bounds=(-12,2),method='bounded')
        expected=1.5*(roughness/6)**(1/3)*n**(-2/3)
        assert result.fun==pytest.approx(expected,rel=1e-9)
        assert np.exp(result.x)==pytest.approx(Sm.histogram_amise_h(n,roughness),rel=1e-5)


def test_tied_weighted_spline_reml_against_full_gaussian_projection():
    g=np.random.default_rng(2908)
    knots=np.linspace(0,1,12)
    x=np.repeat(knots,[2,1,3,1,2,1,3,1,2,1,2,2])
    y=np.sin(5*x)+.2*g.normal(size=len(x))
    w=g.uniform(.5,2,len(x)); sp=Sm.SmoothingSpline(x,y,w)
    d,U=np.linalg.eigh(sp.K)
    Z=(U[:,2:]/np.sqrt(d[2:]))[sp.inv]
    X=np.column_stack((np.ones(len(x)),x))
    reference=[]; actual=[]
    for lam in (.001,.01,.1):
        V=np.diag(1/w)+Z@Z.T/lam
        Vi=np.linalg.solve(V,np.eye(len(x)))
        XtViX=X.T@Vi@X
        P=Vi-Vi@X@np.linalg.solve(XtViX,X.T@Vi)
        m=len(x)-2
        reference.append(.5*(np.linalg.slogdet(V)[1]+np.linalg.slogdet(XtViX)[1]+m*np.log(y@P@y/m)+m))
        actual.append(C.spline_reml(sp,lam))
    np.testing.assert_allclose(np.diff(actual),np.diff(reference),atol=2e-8,rtol=2e-8)


def test_reml_retains_within_tie_noise_information():
    x=np.repeat(np.linspace(0,1,10),2)
    mean=np.sin(5*x)
    low=Sm.SmoothingSpline(x,mean+np.tile([-.02,.02],10))
    high=Sm.SmoothingSpline(x,mean+np.tile([-.8,.8],10))
    np.testing.assert_allclose(low.ybar,high.ybar,atol=1e-15)
    assert abs((C.spline_reml(low,.001)-C.spline_reml(low,.1))-(C.spline_reml(high,.001)-C.spline_reml(high,.1)))>1


def test_distinct_unit_weight_reml_matches_kit_reference():
    x=np.linspace(0,1,20);y=np.sin(7*x)+np.random.default_rng(2).normal(0,.2,len(x))
    sp=Sm.SmoothingSpline(x,y)
    for lam in (.0001,.01,.5):assert C.spline_reml(sp,lam)==pytest.approx(sp.reml(lam),abs=1e-9)


def test_additive_prediction_natural_extension_against_scipy_cubic_spline():
    g=np.random.default_rng(2911);X=g.uniform(-1,1,(50,2));y=np.sin(X[:,0]*3)+X[:,1]**2+.1*g.normal(size=50)
    result=Sm.backfit(X,y,[.001,.002],iters=200)
    assert result['iterations']<200
    for j in range(2):
        order=np.argsort(X[:,j]);knots=X[order,j];values=result['f'][order,j]
        Q,R=Sm._QR(knots);gamma=np.linalg.solve(R,Q.T@values)
        probe=np.linspace(knots[0],knots[-1],55)
        reference=interpolate.CubicSpline(knots,values,bc_type='natural')
        np.testing.assert_allclose(Sm.natural_spline_eval(knots,values,gamma,probe),reference(probe),atol=1e-10)
        outside=np.array([knots[0]-.2,knots[-1]+.2])
        expected=[values[0]-.2*reference(knots[0],1),values[-1]+.2*reference(knots[-1],1)]
        np.testing.assert_allclose(Sm.natural_spline_eval(knots,values,gamma,outside),expected,atol=1e-10)


def test_neighbour_summary_excludes_infinite_self_distance():
    result=C.compute_curse()
    for row in result['nn'].values():
        assert np.isfinite(row['farthest'])
        assert 0<row['nearest']<=row['farthest']
        assert 0<row['ratio']<1


def test_zero_exceedance_bootstrap_retains_positive_probability_and_uncertainty(monkeypatch):
    monkeypatch.setattr(Sm,'silverman_test',lambda *args:dict(h=.8,p=0.,B=500))
    result=C.silverman_bootstrap([0,1],1,500,np.random.default_rng(1))
    assert result['p']==pytest.approx(1/501)
    assert result['exceedances']==0 and result['mc_se']>0
    assert 'no Hall-York' in result['calibration']


def test_corrected_gaussian_kernel_moments_and_fourth_order_bias():
    M=lambda u:float(stats.norm.pdf(u)*(1.5-.5*u*u))
    assert integrate.quad(M,-np.inf,np.inf)[0]==pytest.approx(1,abs=1e-10)
    assert integrate.quad(lambda u:u*u*M(u),-np.inf,np.inf)[0]==pytest.approx(0,abs=1e-10)
    assert integrate.quad(lambda u:u**4*M(u),-np.inf,np.inf)[0]==pytest.approx(-3,abs=1e-10)
    biases=[]
    for h in (.04,.02):
        mean=integrate.quad(lambda u:M(u)*float(C.GEYSER.pdf(4.3-h*u)),-10,10,epsabs=1e-12)[0]
        biases.append(abs(mean-float(C.GEYSER.pdf(4.3))))
    assert biases[0]/biases[1]==pytest.approx(16,rel=.02)
