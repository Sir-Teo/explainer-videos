"""Independent checks for causal sensitivity and the corrected data targets."""
import itertools,json
from pathlib import Path
import numpy as np
import pytest
from scipy import stats
from explainer.stats.kit import causal as CA
from videos.stats.stats36 import compute as C


@pytest.mark.parametrize('gamma',[1.,1.7,3.])
def test_exact_signed_rank_tail_matches_independent_sign_enumeration(gamma):
    # Includes zero differences and equal absolute ranks.
    d=np.array([0.,-1,1,2,-3,5]);nz=d[d!=0]
    rank=stats.rankdata(abs(nz));obs=rank[nz>0].sum();p=gamma/(1+gamma)
    ref=0.
    for signs in itertools.product([0,1],repeat=len(nz)):
        s=np.array(signs)
        if s@rank >= obs-1e-12:ref+=p**s.sum()*(1-p)**(len(s)-s.sum())
    assert C.signed_rank_bound(d,gamma)==pytest.approx(ref,abs=1e-14)
    if gamma==1:
        assert C.signed_rank_bound([1,2,3,4],1)==pytest.approx(1/16)


def test_disjoint_pairs_preserve_pair_independence_and_caliper():
    treated=np.array([1,1,1,1,0,0,0,0],bool)
    ps=np.array([.1,.11,.8,.9,.105,.79,.91,.99])
    i,j=C.disjoint_ps_pairs(treated,ps)
    assert len(i)>0 and len(set(i))==len(i) and len(set(j))==len(j)
    assert treated[i].all() and not treated[j].any()
    logit=stats.logistic.ppf(ps)
    assert np.all(abs(logit[i]-logit[j])<=.2*logit.std(ddof=1)+1e-14)


def test_sensitivity_cache_uses_disjoint_pairs_and_exact_tails():
    d=C.load('sens')
    assert d['reused_controls']==0 and d['world_pairs']>0 and d['nsw_pairs']>0
    assert d['rosen_world']['1.0'] < d['rosen_world']['2.0'] < d['rosen_world']['3.0']
    assert d['gamma_star']<4  # Reused controls previously gave a misleading ~7.


def test_cate_grading_has_no_training_patients_and_names_latent_target():
    d=C.load('cate')
    assert d['test_training_overlap']==0
    assert 'latent' in d['benchmark'] and 'noisy' in d['benchmark']


def test_evalue_is_equal_strength_threshold_not_two_separate_lower_bounds():
    rr=2.;e=CA.e_value(rr)
    assert e*e/(2*e-1)==pytest.approx(rr)
    # A confounder with unequal strengths can explain the association even
    # when one strength is smaller than E.
    a,b=10.,3.
    assert b<e and a*b/(a+b-1)>rr


def test_nsw_primary_package_tables_agree_to_disclosed_cent_precision():
    rows=json.loads(Path('docs/qa/evidence/stats36-polish-20261107/source-data.json').read_text())
    assert [r['rows'] for r in rows]==[445,429]
    for r in rows:
        assert np.max(r['maximum_absolute_errors'][:7])==0
        assert np.max(r['maximum_absolute_errors'][7:])<.00500000001


def test_dml_coverage_matches_population_target_and_stored_replicates():
    d=C.load('dml');r=d['replicates'];q=stats.norm.ppf(.95)
    assert d['ate']==3.0 and len(r)==d['reps']==150
    for key in ['dml','nocf']:
        est=np.array([v[key+'_est'] for v in r]);se=np.array([v[key+'_se'] for v in r])
        hits=abs(est-3.)<=q*se
        assert hits.tolist()==[v[key+'_hit'] for v in r]
        assert hits.mean()==pytest.approx(d[key]['cover'])
        assert est.mean()-3.==pytest.approx(d[key]['bias'])
    # 88% is within one nominal Monte Carlo SE of 90%, not an exact guarantee.
    assert abs(d['dml']['cover']-.9)<(.9*.1/d['reps'])**.5


def test_reusing_world_pool_preserves_seeded_study_draws(monkeypatch):
    cached=C.observational_pool()
    before={k:np.asarray(cached[k]).copy() for k in ['base_pool','tau_pool','y0_pool']}
    actual=C.obs_sample(C.rng(636),120,frailty=1.)
    with monkeypatch.context() as m:
        m.setattr(C,'observational_pool',lambda:C.World().trial)
        fresh=C.obs_sample(C.rng(636),120,frailty=1.)
    for k in actual:np.testing.assert_array_equal(actual[k],fresh[k])
    for k in before:np.testing.assert_array_equal(cached[k],before[k])
