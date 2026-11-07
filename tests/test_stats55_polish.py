"""Independent numerical and proof-condition checks for the qualifying exam."""
import math
import numpy as np
import pytest
from scipy import integrate, optimize, stats
from videos.stats.stats55 import checked as C
from explainer.stats.kit import qual as Q


@pytest.mark.parametrize('theta', [0., .03, .3, 3.])
def test_gaussian_soft_risk_matches_independent_quadrature(theta):
    sd, threshold=.1,.22
    exact=C.soft_risk_coordinate(theta,sd,threshold)
    def loss(z):
        y=theta+sd*z
        fit=np.sign(y)*max(abs(y)-threshold,0)
        return (fit-theta)**2*stats.norm.pdf(z)
    breaks=[-np.inf,(-threshold-theta)/sd,(threshold-theta)/sd,np.inf]
    numeric=sum(integrate.quad(loss,a,b,epsabs=1e-12)[0] for a,b in zip(breaks[:-1],breaks[1:]))
    assert exact==pytest.approx(numeric,abs=1e-11)


@pytest.mark.parametrize('n,p0', [(0,.5),(1,.3),(20,.3),(1361,40046/(40046+26107))])
def test_umpu_size_centered_moment_and_two_tail_shape(n,p0):
    rule=C.umpu_binomial(n,p0)
    phi=rule['phi'];x=np.arange(n+1);f=stats.binom.pmf(x,n,p0)
    assert f@phi==pytest.approx(.05,abs=1e-10)
    assert ((x-n*p0)*f)@phi==pytest.approx(0,abs=1e-9)
    assert np.all((phi>=0)&(phi<=1))
    if n>1:
        assert np.all(phi[:rule['c1']]==1) and np.all(phi[rule['c2']+1:]==1)
        assert np.all(phi[rule['c1']+1:rule['c2']]==0)
    if n==1361:assert phi[1263]==1


@pytest.mark.parametrize('alternative', [.1,.65])
def test_umpu_agrees_with_independent_constrained_lp(alternative):
    n,p0=20,.3;x=np.arange(n+1);f=stats.binom.pmf(x,n,p0)
    target=stats.binom.pmf(x,n,alternative)
    lp=optimize.linprog(-target,A_eq=[f,(x-n*p0)*f],b_eq=[.05,0],bounds=[(0,1)]*(n+1),method='highs')
    assert lp.success
    assert target@C.umpu_binomial(n,p0)['phi']==pytest.approx(-lp.fun,abs=1e-9)


def test_sparse_packing_remains_nontrivial_for_one_nonzero():
    f=C.sparse_fano(8,1,100)
    assert f['logM']==pytest.approx(math.log(8))
    assert f['lower']>0
    assert f['kl']+math.log(2)<f['logM']
    # Eight singletons explicitly give the fallback packing.
    points=np.eye(8)
    assert min(np.sum((a-b)**2) for i,a in enumerate(points) for b in points[i+1:])>=.5
    with pytest.raises(ValueError):C.sparse_fano(8,2,100)


@pytest.mark.parametrize('alpha', [.5,1.,2.])
def test_certified_sequence_tails_contain_longer_evaluation(alpha):
    short=C.sequence_contraction(10000,alpha,1.,K=1000)
    longer=C.sequence_contraction(10000,alpha,1.,K=100000)
    assert short['total_lower']<=longer['total_upper']
    assert longer['total_lower']<=short['total_upper']
    assert short['partial_total']<longer['total_upper']
    assert short['tail_lower']<=short['tail_upper']


def test_lasso_column_scaling_cone_and_kkt():
    result=C.lasso_oracle(60,100,4,np.random.default_rng(5),reps=8)
    assert result['kkt_max']<1e-8
    assert result['max_column_norm']==pytest.approx(math.sqrt(60))
    assert result['phi2_reference']==.5
    assert 'not certified' in result['bound_scope']
    assert result['pred_mcse']==pytest.approx(C.mcse(result['pred_samples']))
    assert result['event_mcse']==pytest.approx(C.mcse(result['event_samples']))


def test_stopped_walk_matches_enumerated_paths_without_integrable_time_assumption():
    import itertools
    N=8;times=[];positions=[]
    for steps in itertools.product([-1,1],repeat=N):
        position=0;time=N
        for i,step in enumerate(steps,1):
            position+=step
            if position==1:
                time=i;break
        times.append(time);positions.append(position)
    fp=Q.first_passage(N)
    assert fp['e_min'][-1]==pytest.approx(np.mean(times))
    assert np.mean(positions)==0


def test_uniform_halfline_ceiling_integral_and_relaxed_bound_are_different():
    ceiling=Q.bracketing_integral(lambda e:np.log(np.ceil(1/e**2)),grid=100000)
    relaxed=integrate.quad(lambda e:math.sqrt(math.log(2/e**2)),0,1)[0]
    assert math.sqrt(math.pi/2)<ceiling<relaxed
