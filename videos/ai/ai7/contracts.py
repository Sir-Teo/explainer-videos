"""Bounded Part7 data contracts. No loaders, network, models or producers."""
from __future__ import annotations

import importlib.metadata
import math
import os
import platform
import re
import sys
import unicodedata

import numpy as np

BOOK_IDS = (1342,98,2701,1661,1400,84,345,174,1260,145,158,768,2852,1184,2600,
            120,43,36,35,219,76,74,2554,28054,64317,1952,160,514,46,4300)
ITEM_DEPENDENCIES = {
    'gmm': ('pca',), 'embound': ('gmm',), 'kmeans': ('gmm',), 'forward': ('hmm',),
    'infini': ('kn',), 'scoreboard': ('kn','infini'), 'gpland': ('gp',), 'occam': ('gp',),
}
PAGES_ITEMS = frozenset(('pca','gmm','gp','pca2','cavi'))
TEXT_INPUTS = {
    'hmm': ('train',), 'kn': ('train','valid','passage'), 'goodturing': ('train',),
    'infini': ('train','valid','passage'), 'bayesopt': ('train','valid','passage'),
}
PART1_ITEMS = {'kn': ('raw',), 'scoreboard': ('scoreboard',)}
BAYESOPT = dict(order=5, valid=200_000, initial=2, steps=12, seed=1975,
                grid=[.05,.95,31], candidates=[.02,.98,400],
                length_scales=[.05,1.,25], noise=1e-6, near_duplicate=.005)
REQUIRED = {
    'pca':'share proj y top split n d',
    'gmm':'P y means covs w ll r agree covariance_floor',
    'hmm':'A B pi Bs lls vowel_side sentence states n post',
    'gp':'x y xs mean sd ell s2 noise prior post mean20 sd20 m20 mu0 n_pages',
    'vi':'path t_qp t_pq mean_p cov_p kl_qp kl_final kl_pq_final initial_forward_kl objective_scope reverse_optimizer forward_optimizer',
    'kn':'K rows best best_bits comparison_best_bits comparison_start valid_count test_count selected_same_order part1_best part1_rows',
    'pca2':'vals kept err sv n d theta along lost total2 th_best Z2 ll_tr ll_te sig2 best_k full_te n_train n_test share5 share_best training_share_best',
    'ica':'t S X Xw Y A theta kurt ang iters r_ica r_pca r_mic kurt_src kurt_mix',
    'embound':'ts i0 i1 rounds ll bound',
    'kmeans':'centres z J iters agree same_as_em agree_em sigma hard',
    'lda':'K V D seg alpha n_names words_total bounds bound_rounds monotone snaps top topw size main main_share ex_title ex_theta ex_words ex_topic book_titles share',
    'forward':'letters alpha brute delta back vpath T n logp_bits bits_per_letter A B_letters',
    'ibm1':'F E t lls align example best test hyp_gloss hyp_rule bleu_gloss bleu_rule n_train show show_best',
    'goodturing':'rows discount V tokens types_a bigram_trials_a bigram_trials_b singleton_types p_unseen example word word_count word_prev word_top_prev word_top_share other other_count other_prev',
    'infini':'K n M types discounts edges lam mix_bits kn_bits L hist mean_L median_L max_L acc zero sparse acc_long long_count share_long grow_context grow_next grow_counts demo demo_sa valid_positions example_start example example_L gain',
    'scoreboard':'rows new passage', 'dsep':'N collider fork',
    'bp':'n edges exact belief order msgs loopy_err loopy_final states bp_ops',
    'causal':'stones total pz adjusted naive adjusted_sim experiment truth strata treated_severe untreated_severe p_y_x p_y_nx N',
    'gpland':'order ns means sds mean_sd s noise_sd',
    'occam':'ells fit comp total best_ell gp_ell xp yp degs evidence rmse best_deg xg fits true_deg',
    'bayesopt':'order valid_chars grid truth cand xs ys best_D best_bits grid_best_D grid_best_bits gt_D gt_bits evals grid_evals steps_x steps_y steps_mean steps_sd steps_ei steps_next',
    'cavi':'x N xbar prior post logp elbo kl gap q sd_mu_true sd_mu_q iters mu_range tau_range',
    'reparam':'m true score_mean rep_mean score_sd rep_sd ratio R bins h_score h_rep',
}
REQUIRED_ARRAYS = {
    'pca':'share proj y', 'gmm':'P y means covs w ll r', 'hmm':'A B pi Bs lls post',
    'gp':'x y xs mean sd prior post mean20 sd20', 'vi':'path t_qp t_pq mean_p cov_p',
    'pca2':'vals kept err sv theta along lost Z2 ll_tr ll_te sig2',
    'ica':'t S X Xw Y A theta kurt ang r_ica r_pca r_mic kurt_src kurt_mix',
    'embound':'ts ll bound', 'kmeans':'centres z J sigma hard',
    'lda':'size ex_theta share', 'forward':'alpha delta back A B_letters',
    'ibm1':'t lls align', 'infini':'lam L hist example_L', 'bp':'exact belief',
    'gpland':'order means sds mean_sd', 'occam':'ells fit comp total xp yp evidence rmse xg fits',
    'bayesopt':'grid truth cand xs ys steps_mean steps_sd steps_ei',
    'cavi':'x', 'reparam':'bins h_score h_rep',
}


def build_dependencies(items=None):
    """Explicit upstream preparation for full and selected-item make commands.

    The guarded readers deliberately never launch earlier parts. Walk local
    item prerequisites here so, for example, requesting only KN does not build
    the unrelated pages experiment or the model-backed final scoreboard.
    """
    needed = set(REQUIRED) if items is None else set(items)
    if not needed <= REQUIRED.keys():
        raise KeyError("Unknown Part7 computation")
    pending = list(needed)
    while pending:
        for dependency in ITEM_DEPENDENCIES.get(pending.pop(), ()):
            if dependency not in needed:
                needed.add(dependency)
                pending.append(dependency)
    dependencies = {}
    if needed & PAGES_ITEMS:
        dependencies['ai6'] = {'pages'}
    part1 = set()
    if needed & TEXT_INPUTS.keys() or 'lda' in needed:
        part1.add('corpus')
    for name in needed:
        part1.update(PART1_ITEMS.get(name, ()))
    if part1:
        dependencies['ai1'] = part1
    return dependencies


def runtime_identity():
    return dict(python=platform.python_version(),implementation=platform.python_implementation(),
                numpy=np.__version__,scipy=importlib.metadata.version('scipy'),
                machine=platform.machine(),byteorder=sys.byteorder,
                numeric_thread_environment={k:os.environ.get(k) for k in
                    ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS')})


def to27(text):
    text=unicodedata.normalize('NFKD',text).encode('ascii','ignore').decode().lower()
    return ' '.join(re.sub(r'[^a-z]+',' ',text).split())


def integer(x,low=0,high=None):
    return isinstance(x,(int,np.integer)) and not isinstance(x,(bool,np.bool_)) and x>=low and (high is None or x<=high)


def array(x,shape=None,*,ndim=None,low=-math.inf,high=math.inf):
    try:
        a=np.asarray(x)
        return bool(a.dtype.kind in 'biuf' and (shape is None or a.shape==shape)
                    and (ndim is None or a.ndim==ndim) and np.isfinite(a).all()
                    and (a>=low).all() and (a<=high).all())
    except (TypeError,ValueError,OverflowError):
        return False


def scalar(x,low=-math.inf,high=math.inf):
    return not isinstance(x,(bool,np.bool_)) and array(x,(),low=low,high=high)


def finite_tree(x):
    if isinstance(x,dict):return all(isinstance(k,(str,int)) and finite_tree(v) for k,v in x.items())
    if isinstance(x,(list,tuple)):return all(finite_tree(v) for v in x)
    if isinstance(x,np.ndarray):return array(x)
    if isinstance(x,(float,np.floating)):return math.isfinite(float(x))
    return x is None or isinstance(x,(str,bool,int,np.integer,np.bool_))


def simplex(x,axis=-1):
    return array(x,low=0,high=1) and bool(np.allclose(np.sum(x,axis=axis),1.,rtol=1e-9,atol=1e-10))


def strings(x):
    return isinstance(x,(list,tuple)) and all(isinstance(v,str) and v for v in x)


def required_arrays(name,data=None):
    return set(REQUIRED_ARRAYS.get(name,'').split())


def board_rows(rows):
    if not isinstance(rows,list) or not rows:return False
    keys=[]
    for r in rows:
        if not isinstance(r,dict) or not isinstance(r.get('key'),str) or not isinstance(r.get('label'),str):return False
        keys.append(r['key'])
        if 'bits' in r:
            if not scalar(r['bits'],0):return False
        elif not (scalar(r.get('lo'),0) and scalar(r.get('hi'),r['lo'])):return False
    return len(keys)==len(set(keys))


def bayesopt_piece(key,value):
    if not isinstance(key,str) or not scalar(value,0):return False
    if key.startswith('grid_'):
        return key in {f'grid_{x:.4f}' for x in np.linspace(.05,.95,31)}
    if re.fullmatch(r'x_\d\.\d{6}',key):return .02<=float(key[2:])<=.98
    return False


def valid_structure(name,d,cohort=None):
    """Integrity/reporting contract, not a preferred scientific outcome test."""
    try:
        return _valid(name,d,cohort)
    except (ValueError,TypeError,KeyError,IndexError,AttributeError,OverflowError,np.linalg.LinAlgError):
        return False


def _valid(name,d,cohort):
    if name not in REQUIRED or not isinstance(d,dict) or not set(REQUIRED[name].split())<=d.keys():return False
    ordinary={k:v for k,v in d.items() if not(name=='embound' and k in ('ll','bound'))}
    if not finite_tree(ordinary):return False
    a=lambda k,shape=None,**kw:array(d[k],shape,**kw)
    s=lambda k,lo=-math.inf,hi=math.inf:scalar(d[k],lo,hi)
    if name=='pca':
        n,z=d['n'],d['d']
        return (integer(n,3) and integer(z,3) and a('share',(z,),low=-1e-10,high=1)
                and np.isclose(np.sum(d['share']),1) and a('proj',(n,3)) and a('y',(n,),low=0,high=1)
                and np.isin(d['y'],[0,1]).all() and s('split',0,1)
                and (cohort is None or n==cohort['n_pages'])
                and isinstance(d['top'],dict) and {'0','1'}<={str(k)for k in d['top']})
    if name=='gmm':
        p=np.asarray(d['P']);t=len(d['ll']);n=len(p)
        return (a('P',(n,2)) and a('y',(n,),low=0,high=1) and a('means',(t,2,2))
                and a('covs',(t,2,2,2)) and np.allclose(d['covs'],np.swapaxes(d['covs'],-1,-2))
                and s('covariance_floor',1e-300)
                and (np.linalg.eigvalsh(d['covs'])>=d['covariance_floor']-1e-10).all() and a('ll',(t,)) and t==40
                and a('r',(t,n),low=0,high=1) and a('w',(t,2)) and simplex(d['w']) and s('agree',.5,1))
    if name=='hmm':
        return (a('A',(2,2)) and simplex(d['A']) and a('B',(2,27)) and simplex(d['B'])
                and a('pi',(2,)) and simplex(d['pi']) and a('Bs',(61,2,27)) and simplex(d['Bs'])
                and np.allclose(np.asarray(d['Bs'])[-1],d['B']) and a('lls',(61,))
                and a('post',(2,27)) and simplex(d['post'],axis=0) and isinstance(d['sentence'],str)
                and a('states',(len(d['sentence']),),low=0,high=1) and np.isin(d['states'],[0,1]).all()
                and integer(d['n'],1) and strings(d['vowel_side']))
    if name=='gp':
        n=d['n_pages'];q=300
        return (integer(n,20) and a('x',(n,)) and np.all(np.diff(d['x'])>0) and a('y',(n,),low=0)
                and all(a(k,(q,)) for k in ('xs','mean','mean20'))
                and all(a(k,(q,),low=0) for k in ('sd','sd20')) and a('prior',(5,q)) and a('post',(5,q))
                and all(s(k,1e-300) for k in ('ell','s2','noise')) and integer(d['m20'],1,n))
    if name=='vi':
        return (a('path',(40,5)) and a('t_qp',(5,)) and a('t_pq',(5,)) and a('mean_p',(2,))
                and a('cov_p',(2,2)) and np.all(np.linalg.eigvalsh(d['cov_p'])>0)
                and a('kl_qp',(40,),low=-1e-9) and s('kl_final',-1e-9) and s('kl_pq_final',-1e-9)
                and s('initial_forward_kl',-1e-9) and isinstance(d['objective_scope'],str) and d['objective_scope']
                and all(isinstance(d[k],dict) and type(d[k].get('success')) is bool
                        and isinstance(d[k].get('message'),str) for k in ('reverse_optimizer','forward_optimizer')))
    if name=='kn':
        rows=d['rows'];best=d['best'];start=d['comparison_start'];selected=d['selected_same_order']
        return (integer(d['K'],2) and isinstance(rows,list) and rows and integer(best,0,len(rows)-1)
                and integer(start,0) and start==len(rows)-1
                and integer(d['valid_count'],1) and integer(d['test_count'],1)
                and all(isinstance(r,dict) and r.get('order')==i and scalar(r.get('valid'),0)
                        and scalar(r.get('test'),0) and integer(r.get('start'),0) and r.get('start')==start
                        and integer(r.get('valid_count'),1) and r.get('valid_count')==d['valid_count']
                        and integer(r.get('test_count'),1) and r.get('test_count')==d['test_count']
                        for i,r in enumerate(rows))
                and int(np.argmin([r['valid']for r in rows]))==best and s('part1_best',0)
                and s('comparison_best_bits',0) and np.isclose(d['comparison_best_bits'],rows[best]['test'])
                and isinstance(selected,dict) and integer(selected.get('order'),0)
                and integer(selected.get('start'),0) and selected.get('order')==selected.get('start')==best
                and integer(selected.get('valid_count'),1) and integer(selected.get('test_count'),1)
                and selected.get('valid_count')==d['valid_count']+start-best
                and selected.get('test_count')==d['test_count']+start-best
                and scalar(selected.get('valid'),0) and scalar(selected.get('test'),0)
                and s('best_bits',0) and np.isclose(d['best_bits'],selected['test'])
                and array(d['part1_rows'],ndim=1,low=0))
    if name=='pca2':
        n,z=d['n'],d['d']
        return (integer(n,3) and integer(z,3) and all(a(k,(z,)) for k in ('vals','sv','ll_tr','ll_te','sig2'))
                and all(a(k,(z+1,),low=-1e-8) for k in ('kept','err')) and a('Z2',(n,2))
                and all(a(k,(181,))for k in ('theta','along','lost')) and integer(d['best_k'],0,z-1)
                and integer(d['n_train'],1) and integer(d['n_test'],1) and d['n_train']+d['n_test']==n
                and s('training_share_best',0,1)
                and np.allclose(np.asarray(d['kept'])+d['err'],z,atol=1e-7)
                and np.allclose(np.asarray(d['sv'])**2/n,d['vals'],atol=1e-7))
    if name=='ica':
        return (a('t',(800,)) and all(a(k,(2,800))for k in ('S','X','Xw','Y')) and a('A',(2,2))
                and a('theta',(361,)) and a('kurt',(361,)) and integer(d['iters'],0,40)
                and a('ang',(d['iters']+1,)) and all(a(k,(2,),low=0,high=1+1e-10)for k in ('r_ica','r_pca','r_mic')))
    if name=='embound':
        ll,bd=np.asarray(d['ll']),np.asarray(d['bound'])
        return (a('ts',(85,)) and ll.dtype.kind=='f' and bd.dtype.kind=='f' and ll.shape==bd.shape==(4,85)
                and not np.isinf(ll).any() and not np.isinf(bd).any()
                and np.array_equal(np.isnan(ll),np.isnan(bd)) and list(d['rounds'])==[0,1,2,4]
                and integer(d['i0'],0,84) and integer(d['i1'],0,84)
                and np.isfinite(ll[:,[d['i0'],d['i1']]]).all())
    if name=='kmeans':
        i=d['iters'];n=np.asarray(d['z']).shape[-1]
        return (integer(i,1,50) and a('centres',(i,2,2)) and a('z',(i,n),low=0,high=1)
                and np.isin(d['z'],[0,1]).all() and a('J',(i,),low=0) and a('sigma',(10,),low=1e-300)
                and a('hard',(10,),low=0,high=1) and all(s(k,.5,1)for k in ('agree','same_as_em','agree_em')))
    if name=='lda':
        k=d['K'];v=d['V'];n=d['D']
        return (k==12 and integer(v,10,3000) and integer(n,3) and d['seg']==2000
                and array(d['bounds'],(41,)) and list(d['bound_rounds'])==list(range(41))
                and isinstance(d['monotone'],(bool,np.bool_))
                and np.asarray(d['top']).shape==(k,10) and a('topw',(k,10),low=0,high=1)
                and a('size',(k,)) and simplex(d['size']) and a('share',(k,30)) and simplex(d['share'])
                and a('ex_theta',(k,)) and simplex(d['ex_theta']) and strings(d['book_titles']) and len(d['book_titles'])==30
                and strings(d['ex_words']) and a('ex_topic',(len(d['ex_words']),),low=-1,high=k-1)
                and isinstance(d['snaps'],dict) and {'0','1','2','3','5','8','13','20','30','40'}<=d['snaps'].keys())
    if name=='forward':
        return (d['T']==6 and all(a(k,(6,2),low=0)for k in ('alpha','delta')) and a('back',(6,2),low=0,high=1)
                and a('vpath',(6,),low=0,high=1) and a('A',(2,2)) and simplex(d['A']) and a('B_letters',(2,6),low=0,high=1)
                and np.isclose(np.asarray(d['alpha'])[-1].sum(),d['brute'],rtol=1e-9,atol=1e-20) and s('bits_per_letter',0))
    if name=='ibm1':
        f,e=len(d['F']),len(d['E']);example=d['example'];align=np.asarray(d['align'])
        ok=(strings(d['F']) and strings(d['E']) and f>0 and e>0 and a('t',(31,f+1,e),low=0,high=1)
            and simplex(d['t']) and a('lls',(31,)) and isinstance(example,(list,tuple)) and len(example)==2
            and all(isinstance(t,str)for t in example)
            and align.shape==(31,len(example[1].split()),len(example[0].split())+1) and simplex(align)
            and integer(d['n_train'],1))
        for key in ('bleu_gloss','bleu_rule'):
            b=d[key];ok=ok and isinstance(b,dict) and scalar(b.get('bleu'),0,1) and array(b.get('p'),(4,),low=0,high=1)
        return ok
    if name=='goodturing':
        return (integer(d['V'],2) and integer(d['tokens'],1) and len(d['rows'])==9
                and integer(d['bigram_trials_a'],1) and integer(d['bigram_trials_b'],1)
                and d['tokens']==d['bigram_trials_a']+d['bigram_trials_b']+2
                and integer(d['singleton_types'],0,d['bigram_trials_a'])
                and all(isinstance(r,dict) and r.get('r')==i and all(scalar(r.get(k),0)for k in ('Nr','gt','held'))for i,r in enumerate(d['rows']))
                and all(d['rows'][i]['Nr']>0 for i in range(9))
                and d['singleton_types']==d['rows'][1]['Nr']
                and a('discount',(7,)) and s('p_unseen',0,1)
                and np.isclose(d['p_unseen'],d['singleton_types']/d['bigram_trials_a'],rtol=1e-12,atol=0)
                and isinstance(d['word'],str) and isinstance(d['other'],str) and d['word']!=d['other']
                and s('word_top_share',0,1))
    if name=='infini':
        l=np.asarray(d['L']);m=d['M'];n=len(l)
        long=l>=10
        return (integer(d['K'],2,255) and integer(d['n'],1,2**31-1) and integer(m,0)
                and a('L',(n,),low=0,high=500) and np.equal(l,np.floor(l)).all()
                and a('hist',(41,),low=0) and np.sum(d['hist'])==n
                and np.array_equal(d['hist'],np.bincount(np.minimum(l.astype(int),40),minlength=41))
                and a('lam',(7,2),low=0,high=.995) and len(d['types'])==len(d['discounts'])==m+1
                and all(s(k,0,1)for k in ('acc','zero','sparse','share_long'))
                and integer(d['long_count'],0,n) and d['long_count']==int(long.sum())
                and ((d['acc_long'] is None and d['long_count']==0)
                     or (d['long_count']>0 and scalar(d['acc_long'],0,1)))
                and s('mix_bits',0) and s('kn_bits',0) and np.isclose(d['gain'],d['kn_bits']-d['mix_bits']))
    if name=='scoreboard':
        return (board_rows(d['rows']) and len(d['new'])==2 and all(integer(i,0,len(d['rows'])-1)for i in d['new'])
                and [d['rows'][i]['key']for i in d['new']]==['kn','infini'] and isinstance(d['passage'],str))
    if name=='dsep':
        return integer(d['N'],1) and all(isinstance(d[k],dict) and d[k] and all(scalar(x,0,1)for x in d[k].values())for k in ('collider','fork'))
    if name=='bp':
        return (d['n']==7 and len(d['edges'])==6 and len(d['order'])==12 and a('msgs',(12,1),low=0,high=1)
                and a('exact',(7,),low=0,high=1) and a('belief',(7,),low=0,high=1)
                and np.allclose(d['exact'],d['belief'],atol=1e-10) and a('loopy_err',(30,),low=0,high=1)
                and np.isclose(d['loopy_final'],d['loopy_err'][-1]) and d['states']==128 and d['bp_ops']==48)
    if name=='causal':
        return (integer(d['N'],1) and a('strata',(2,2),low=0,high=1)
                and all(s(k,-1,1)for k in ('naive','adjusted_sim','experiment','truth'))
                and all(s(k,0,1)for k in ('treated_severe','untreated_severe','p_y_x','p_y_nx'))
                and all(integer(v[0],0) and integer(v[1],1) and v[0]<=v[1]for group in d['stones'].values()for v in group.values()))
    if name=='gpland':
        ns=d['ns'];q=np.asarray(d['means']).shape[-1];order=np.asarray(d['order'])
        return (len(ns)==16 and a('means',(16,q)) and a('sds',(16,q),low=0) and a('mean_sd',(16,),low=0)
                and np.allclose(np.mean(d['sds'],axis=1),d['mean_sd']) and np.array_equal(np.sort(order),np.arange(len(order)))
                and max(ns)<=len(order))
    if name=='occam':
        t=len(d['ells'])
        return (70<=t<=71 and a('ells',(t,),low=1e-300) and all(a(k,(t,))for k in ('fit','comp','total'))
                and a('xp',(30,)) and a('yp',(30,)) and a('xg',(200,)) and a('fits',(13,200))
                and a('evidence',(13,)) and a('rmse',(13,),low=0) and list(d['degs'])==list(range(13)) and integer(d['best_deg'],0,12))
    if name=='bayesopt':
        e=d['evals'];s_=e-1
        return (d['order']==5 and integer(d['valid_chars'],6,200000) and integer(e,2,14) and d['grid_evals']==31
                and a('grid',(31,),low=.05,high=.95) and a('truth',(31,),low=0) and a('cand',(400,),low=.02,high=.98)
                and a('xs',(e,),low=.02,high=.98) and a('ys',(e,),low=0) and len(d['gt_D'])==6
                and all(a(k,(s_,400),low=0)for k in ('steps_sd','steps_ei')) and a('steps_mean',(s_,400))
                and len(d['steps_x'])==len(d['steps_y'])==len(d['steps_next'])==s_
                and all(np.array_equal(x,np.asarray(d['xs'])[:i+2]) and np.array_equal(y,np.asarray(d['ys'])[:i+2])for i,(x,y)in enumerate(zip(d['steps_x'],d['steps_y'])))
                and np.isclose(d['best_bits'],min(d['ys'])) and np.isclose(d['best_D'],np.asarray(d['xs'])[np.argmin(d['ys'])]))
    if name=='cavi':
        i=d['iters']
        return (d['N']==25 and a('x',(25,)) and a('prior',(4,)) and a('post',(4,)) and integer(i,1,12)
                and a('elbo',(i,)) and a('kl',(i,),low=-1e-6) and a('q',(i,4))
                and np.all(np.asarray(d['q'])[:,1:]>0) and s('gap',0) and s('sd_mu_true',1e-300) and s('sd_mu_q',1e-300))
    if name=='reparam':
        return (integer(d['R'],1) and a('bins',(81,)) and np.all(np.diff(d['bins'])>0)
                and all(a(k,(80,),low=0) and np.sum(d[k])==d['R'] for k in ('h_score','h_rep'))
                and s('ratio',0) and s('score_sd',0) and s('rep_sd',0))
    return False
