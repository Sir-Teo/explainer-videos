"""Reproducible worked witnesses; these do not execute a Pebble-language port."""
from __future__ import annotations
import hashlib,json
import numpy as np
from explainer.cs.algo import practice as P


def witnesses():
    counts=[3,1,4,1,5,9,2,6];tree=P.Fenwick(len(counts));updates=[]
    for i,v in enumerate(counts,1):updates.append(dict(index=i,delta=v,path=tree.add(i,v)))
    before=tree.prefix(5);before_path=tree.last_path.copy();path=tree.add(2,5)
    counts[1]+=5;after=tree.prefix(5);after_path=tree.last_path.copy()
    assert before==14 and after==sum(counts[:5])==19
    assert [tree.prefix(i) for i in range(9)]==[sum(counts[:i]) for i in range(9)]
    a=[2,2,1,3];maxima,trace,pops=P.sliding_max(a,2,trace=True)
    assert maxima==[max(a[i:i+2]) for i in range(3)]
    cartesian=P.cartesian_tree([2,1,1,3]);assert cartesian==[1,-1,1,2]
    submasks=[dict(n=n,actual=sum(1 for m in range(1<<n) for _ in P.submasks(m)),expected=3**n) for n in range(9)]
    assert all(r['actual']==r['expected'] for r in submasks)
    class Reads:
        def __init__(self):self.n=0
        def __len__(self):return 1000
        def __getitem__(self,i):self.n+=1;return 2*i
    values=Reads();answer,reported=P.galloping(values,500);assert answer==250 and reported==values.n==16
    return dict(fenwick=dict(initial=[3,1,4,1,5,9,2,6],initial_updates=updates,query=5,before=before,before_path=before_path,update=[2,5],update_path=path,after=after,after_path=after_path,all_prefixes=[tree.prefix(i) for i in range(9)],scope='Python arithmetic trace; fixed8-ID Pebble design guidance only'),deque=dict(input=a,k=2,outputs=maxima,trace=trace,pops=pops),cartesian=dict(input=[2,1,1,3],parents=cartesian),submasks=submasks,galloping=dict(length=1000,target=500,answer=answer,actual_reads=values.n,reported_reads=reported))


def iid_mean_exit(seed=2406,replicates=1000,epsilons=(4,8,16,32)):
    """Fixed slope1 for positive IID exponential gaps with population mean/variance1.

    Each walk stops at its first strict exit from [-epsilon,+epsilon]. The
    epsilon-squared formula is an asymptotic baseline, not an exact finite mean.
    Sample means and standard errors describe these independent simulated walks.
    """
    rng=np.random.default_rng(seed);rows=[]
    for eps in epsilons:
        errors=np.zeros(replicates);lengths=np.zeros(replicates,dtype=np.int64)
        previous=np.zeros(replicates);exited=np.zeros(replicates,dtype=bool);draw_hash=hashlib.sha256()
        while not exited.all():
            active=np.flatnonzero(~exited);gaps=rng.exponential(1,len(active));draw_hash.update(gaps.tobytes())
            previous[active]=errors[active];errors[active]+=gaps-1;lengths[active]+=1
            exited[active]=np.abs(errors[active])>eps
        assert (np.abs(previous)<=eps).all() and (np.abs(errors)>eps).all()
        mean=float(lengths.mean());se=float(lengths.std(ddof=1)/np.sqrt(replicates))
        rows.append(dict(epsilon=eps,replicates=replicates,lengths=lengths.tolist(),previous_errors=previous.tolist(),exit_errors=errors.tolist(),mean=mean,standard_error=se,asymptotic_baseline=eps**2,mean_over_epsilon_squared=mean/eps**2,generated_gaps_sha256=draw_hash.hexdigest()))
    return dict(seed=seed,generator='NumPy default_rng PCG64, exponential mean1',population_mean=1,population_variance=1,fixed_slope=1,rows=rows,scope='Finite IID fixed-slope first-exit reproduction; not the anchored greedy corpus fit, optimal PLA or a new theorem')


if __name__=='__main__':
    print(json.dumps(dict(witnesses=witnesses(),iid_mean_exit=iid_mean_exit()),indent=2))
