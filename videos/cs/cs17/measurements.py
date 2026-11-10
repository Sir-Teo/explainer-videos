"""Fixed-occupancy uniform-permutation insertion illustration, finite model."""
import math,random,statistics

def sample(m,free,rng):
    """Probe a fresh uniform permutation lazily against m-free occupied slots."""
    if not 1<=free<=m:raise ValueError('require 1 <= free <= m')
    occupied=m-free;swapped={}
    for i in range(m):
        j=rng.randrange(i,m);slot=swapped.get(j,j);swapped[j]=swapped.get(i,i)
        if slot>=occupied:return i+1
    raise AssertionError('at least one free slot exists')

def uniform_probe_experiment(m=8192,trials=5000):
    rng=random.Random(17);rows=[]
    for delta in [.5,.25,.1,.05,.02,.01]:
        n=int((1-delta)*m);free=m-n;values=[sample(m,free,rng) for _ in range(trials)]
        expected=(m+1)/(free+1);variance=free*(m+1)*(m-free)/((free+1)**2*(free+2));se=math.sqrt(variance/trials)
        assert max(values)<=n+1 and abs(statistics.mean(values)-expected)<=6*se
        rows.append(dict(requested_delta=delta,delta=free/m,free=free,measured=statistics.mean(values),finite_expectation=expected,yao=m/free,trials=trials,standard_error=se,max_observed=max(values)))
    return dict(rows=rows,m=m,model='fresh pseudorandom uniform permutation per independent insertion trial; fixed occupancy; earlier insertions are not pooled across changing loads',scope='finite illustrative model; no new hashing algorithm implemented')
