"""Full finite evidence for Part 27; independent checks run after timed calls.

The teaching RNG is seeded random.Random. Logged transcripts, not security
claims about that generator, are the reproducible outputs. A marginal colour
histogram is not a verification of full zero knowledge.
"""
from __future__ import annotations
import functools
import gzip
import hashlib
import json
import math
import random
import time
from pathlib import Path

ROOT=Path('.cache/cs27/artifacts')
def digest(data): return hashlib.sha256(data).hexdigest()
def artifact(name,value):
    raw=json.dumps(value,ensure_ascii=False,separators=(',',':')).encode()
    raw=gzip.compress(raw,mtime=0);path=ROOT/name;path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix(path.suffix+'.tmp');temp.write_bytes(raw);temp.replace(path)
    return dict(path=str(path),sha256=digest(raw),bytes=len(raw))

def plain(value):
    if value is None or isinstance(value,(str,int,float,bool)): return value
    if isinstance(value,random.Random): return {'random_source':'seeded random.Random; actual outputs retained'}
    if isinstance(value,bytes): return {'hex':value.hex()}
    if isinstance(value,(list,tuple)): return [plain(x) for x in value]
    if isinstance(value,(set,frozenset)): return sorted((plain(x) for x in value),key=repr)
    if isinstance(value,dict): return {str(k):plain(v) for k,v in value.items()}
    if callable(value): return {'callable':value.__name__}
    raise TypeError(f'cannot preserve {type(value).__name__}')

P_CALLS=('binom_tail','next_prime','fingerprint_eq','dnf_random','random_restriction','restrict','truth_table',
         'dt_depth','gni_round','count_sat','sumcheck','zk_colouring','zk_simulate','distance_to_linear','blr_rejection',
         'walksat','vc_branch','buss_kernel','permanent_ryser','det_bareiss','ov_brute','three_sum','planted_clique',
         'degree_recover','pollard_rho','ug_instance','ug_propagate','ug_value','sat_to_ov','vandermonde_test')
class Recorder:
    def __init__(self,P,X): self.P=P;self.X=X;self.calls=[];self.pool={};self.originals=[]
    def intern(self,value):
        value=plain(value);key=digest(json.dumps(value,sort_keys=True,separators=(',',':')).encode())
        if key not in self.pool: self.pool[key]=value
        return key
    def wrap(self,module,name,prefix):
        fn=getattr(module,name);self.originals.append((module,name,fn))
        @functools.wraps(fn)
        def call(*args,**kwargs):
            argkey=self.intern(dict(args=args,kwargs=kwargs))
            trace=[]
            if name in ('fingerprint_eq','gni_round','zk_colouring') and 'trace' not in kwargs: kwargs={**kwargs,'trace':trace}
            start=time.perf_counter_ns();result=fn(*args,**kwargs);elapsed=time.perf_counter_ns()-start
            row=dict(fn=prefix+'.'+name,input=argkey,output=self.intern(result),elapsed_ns=elapsed)
            if trace: row['trace']=self.intern(trace)
            self.calls.append(row)
            return result
        setattr(module,name,call)
    def __enter__(self):
        for name in P_CALLS:self.wrap(self.P,name,'P')
        for name in ('cdcl','random_ksat'):self.wrap(self.X,name,'X')
        return self
    def __exit__(self,*_):
        for module,name,fn in reversed(self.originals):setattr(module,name,fn)
    def times(self,name):return [r['elapsed_ns']/1e9 for r in self.calls if r['fn']==name]
    def evidence(self):return dict(objects=self.pool,calls=self.calls,timing_scope='Only the teaching function call; input/output serialization and all independent checks are outside these recorded timers.')

# The references below do not import the teaching instrument.
import os
import subprocess
from fractions import Fraction
from collections import Counter

NATIVE_SOURCE=Path(__file__).with_name('reference_native.cpp')
NATIVE_FLAGS=['-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=all']

def native_build():
    root=Path('.cache/cs27/reference-native');root.mkdir(parents=True,exist_ok=True)
    version=subprocess.run(['g++','--version'],capture_output=True,text=True,check=True).stdout
    key=digest(NATIVE_SOURCE.read_bytes()+json.dumps(NATIVE_FLAGS).encode()+version.encode())
    binary=root/('reference-'+key[:20]);manifest=binary.with_suffix('.json')
    if not binary.exists():
        temp=binary.with_suffix('.tmp')
        command=['g++',*NATIVE_FLAGS,str(NATIVE_SOURCE),'-lgmpxx','-lgmp','-o',str(temp)]
        result=subprocess.run(command,capture_output=True,text=True)
        record=dict(command=command,returncode=result.returncode,stdout=result.stdout,stderr=result.stderr,
                    compiler=version,source_sha256=digest(NATIVE_SOURCE.read_bytes()))
        manifest.write_text(json.dumps(record,indent=2)+'\n')
        if result.returncode:raise RuntimeError('native reference build failed; actual log retained '+str(manifest))
        os.replace(temp,binary);record['binary_sha256']=digest(binary.read_bytes());manifest.write_text(json.dumps(record,indent=2)+'\n')
    record=json.loads(manifest.read_text())
    assert record['source_sha256']==digest(NATIVE_SOURCE.read_bytes()) and record['binary_sha256']==digest(binary.read_bytes())
    return binary,record

def native_query(text,evidence):
    binary,build=native_build()
    run=subprocess.run([str(binary)],input=text,capture_output=True,text=True,timeout=180)
    evidence.setdefault('native_build',build)
    row=dict(command=[str(binary)],stdin=text,stdout=run.stdout,stderr=run.stderr,returncode=run.returncode)
    evidence.setdefault('native_queries',[]).append(row)
    assert run.returncode==0 and not run.stderr,row
    return run.stdout.strip()

def sat_reference(n,clauses,evidence):
    from pysat.solvers import Glucose42
    with Glucose42(bootstrap_with=clauses) as solver:
        answer=solver.solve();raw=solver.get_model() if answer else None
    model=None if raw is None else [False]+[v in set(raw) for v in range(1,n+1)]
    if answer:assert all(any(model[abs(l)]==(l>0) for l in c) for c in clauses)
    evidence.setdefault('native_sat_queries',[]).append(dict(n=n,clauses=clauses,status='sat' if answer else 'unsat',model=model,
        scope='Independent native Glucose 4.2 implementation cross-check; UNSAT agreement is not a retained proof trace.'))
    return answer

def matrix_query(op,A,evidence):
    text=op+' '+str(len(A))+' '+' '.join(str(v) for row in A for v in row)+'\n'
    return native_query(text,evidence).split()

def dnf_value(f,assignment):
    if isinstance(f,bool):return f
    return any(all(assignment[int(v)]==bool(b) for v,b in term) for term in f)

def direct_depth(table,n):
    """Minimum depth by partial-assignment states, not tuple reindexing."""
    @functools.lru_cache(None)
    def solve(mask,values):
        entries=[bool(table[x]) for x in range(1<<n) if x&mask==values]
        if all(entries) or not any(entries):return 0
        return 1+min(max(solve(mask|1<<v,values),solve(mask|1<<v,values|1<<v))
                     for v in range(n) if not mask>>v&1)
    return solve(0,0)

def fourier(table,n):
    coefficients=[1-2*int(v) for v in table];step=1
    while step<len(coefficients):
        for base in range(0,len(coefficients),2*step):
            for i in range(step):
                x,y=coefficients[base+i],coefficients[base+i+step]
                coefficients[base+i]=x+y;coefficients[base+i+step]=x-y
        step*=2
    return coefficients

def eval_interpolant(values,r,p):
    # Newton forward differences on consecutive nodes; independent of the
    # teaching Lagrange formula and its denominator implementation.
    differences=list(values);factor=1;out=0
    for degree in range(len(values)):
        out=(out+factor*differences[0])%p
        differences=[(b-a)%p for a,b in zip(differences,differences[1:])]
        factor=factor*(r-degree)*pow(degree+1,-1,p)%p
    return out

def direct_polynomial(clauses,point,p):
    result=1
    for clause in clauses:
        false=1
        for literal in clause:
            value=point[abs(literal)-1]
            false=false*((1-value) if literal>0 else value)%p
        result=result*(1-false)%p
    return result

def validate_recording(name,evidence):
    from sympy import isprime,nextprime
    import itertools
    pool=evidence['objects'];counts=Counter();validated={};pit=[]
    def obj(key):return pool[key]
    for row in evidence['calls']:
        assert row['elapsed_ns']>=0
        for key in ('input','output','trace'):
            if key in row:assert digest(json.dumps(obj(row[key]),sort_keys=True,separators=(',',':')).encode())==row[key]
        fn=row['fn'];call=obj(row['input']);args=call['args'];kw=call['kwargs'];out=obj(row['output']);counts[fn]+=1
        identity=(fn,row['input'],row['output'],row.get('trace'))
        if identity in validated:continue
        validated[identity]=True
        if fn=='P.binom_tail':
            k,probability,threshold=args;q=Fraction(probability).limit_denominator(1000)
            assert float(q)==probability
            a,b=q.numerator,q.denominator
            numerator=sum(math.comb(k,i)*a**i*(b-a)**(k-i) for i in range(max(0,threshold),k+1))
            reference=float(Fraction(numerator,b**k))
            assert math.isclose(out,reference,rel_tol=2e-9,abs_tol=1e-300)
        elif fn=='P.next_prime':
            assert out==int(nextprime(max(1,args[0]-1))) and isprime(out)
        elif fn=='P.fingerprint_eq':
            x,y,p=args[:3];trace=obj(row['trace']);assert len(trace)==1
            t=trace[0];r=t['r'];values=[]
            for bits in (x,y):
                power=1;value=0
                for bit in bits:value=(value+int(bit)*power)%p;power=power*r%p
                values.append(value)
            assert values==[t['left'],t['right']] and out==[values[0]==values[1],2*(p-1).bit_length()]
        elif fn=='P.dnf_random':
            n,terms,width=args[:3];assert len(out)==terms
            assert all(len(t)==width and len({v for v,b in t})==width and all(0<=v<n for v,b in t) for t in out)
        elif fn=='P.random_restriction':
            n=args[0];assert all(0<=int(v)<n and isinstance(b,bool) for v,b in out.items())
        elif fn=='P.restrict':
            f,rho=args;rho={int(v):bool(b) for v,b in rho.items()}
            variables={int(v) for term in f for v,b in term};free=sorted(variables-set(rho))
            for bits in itertools.product((False,True),repeat=len(free)):
                assignment={**rho,**dict(zip(free,bits))}
                assert dnf_value(f,assignment)==dnf_value(out,assignment)
        elif fn=='P.truth_table':
            f,free=args;assert len(out)==1<<len(free)
            assert out==[dnf_value(f,{v:bool(mask>>i&1) for i,v in enumerate(free)}) for mask in range(len(out))]
        elif fn=='P.dt_depth':
            table,n=args;assert out==direct_depth(table,n)
        elif fn=='P.gni_round':
            G0,G1,n=args[:3];t=obj(row['trace'])[0];b,answer=out
            chosen=G1 if b else G0;perm=t['permutation'];H={tuple(sorted((perm[u],perm[v]))) for u,v in chosen}
            assert sorted(H)==[tuple(e) for e in t['challenge_edges']] and sorted(perm)==list(range(n))
            expected=[]
            for graph in (G0,G1):
                possible=any({tuple(sorted((pi[u],pi[v]))) for u,v in graph}==H for pi in itertools.permutations(range(n)))
                expected.append(possible)
            assert expected==t['matches'] and (b,answer)==(t['bit'],t['answer'])
            if expected[0]!=expected[1]:assert answer==int(expected[1])
        elif fn=='P.count_sat':
            clauses,n=args;reference=sum(all(any(bits[abs(l)-1]==(l>0) for l in c) for c in clauses)
                                        for bits in itertools.product((False,True),repeat=n))
            assert out==reference
        elif fn=='P.sumcheck':
            clauses,n,p,claim=args[:4];accepted,rounds,log=out;current=claim%p;prefix=[]
            for stage in log[:-1]:
                values=stage['g'];assert len(values)==stage['degree_bound']+1
                assert (values[0]+values[1])%p==current==stage['previous']
                r=stage['r'];assert 0<=r<p;current=eval_interpolant(values,r,p);prefix.append(r)
                assert current==stage['next']
            assert len(prefix)==n==rounds
            final=direct_polynomial(clauses,prefix,p)
            assert log[-1]==dict(final=final,claim=current,ok=final==current) and accepted==(final==current)
            if not kw.get('cheat',False):
                # Every honest message is checked against a direct suffix sum.
                prefix=[]
                for stage in log[:-1]:
                    expected=[sum(direct_polynomial(clauses,prefix+[x]+list(suffix),p)
                                  for suffix in itertools.product((0,1),repeat=n-len(prefix)-1))%p
                              for x in range(len(stage['g']))]
                    assert expected==stage['g'];prefix.append(stage['r'])
        elif fn=='P.zk_colouring':
            n,edges,col,rounds=args[:4];caught,pairs=out;trace=obj(row['trace']) if 'trace'in row else []
            assert len(trace)==len(pairs)
            valid_edges={tuple(sorted(e)) for e in edges}
            for i,t in enumerate(trace):
                assert len(t['commitments'])==n and tuple(sorted(t['edge'])) in valid_edges
                assert t['edge']==[o['vertex'] for o in t['openings']]
                assert pairs[i]==[o['colour'] for o in t['openings']]
                for opening in t['openings']:
                    h=hashlib.sha256(bytes.fromhex(opening['nonce'])+bytes([opening['colour']])).hexdigest()
                    assert h==t['commitments'][opening['vertex']]
                u,v=t['edge'];good=col[u]!=col[v]
                assert t['accepted']==good==(pairs[i][0]!=pairs[i][1])
                if not good:assert caught==i+1==len(trace)
            assert (caught is None and (len(trace)==rounds or not edges)) or (caught==len(trace) and not trace[-1]['accepted'])
        elif fn=='P.zk_simulate':
            assert len(out)==args[0] and all(0<=a<3 and 0<=b<3 and a!=b for a,b in out)
        elif fn in ('P.distance_to_linear','P.blr_rejection'):
            table,n=args;N=1<<n;coefficients=fourier(table,n)
            reference=Fraction(N-max(coefficients),2*N) if fn.endswith('distance_to_linear') else Fraction(1,2)-Fraction(sum(c**3 for c in coefficients),2*N**3)
            assert out==float(reference)
        elif fn=='P.walksat':
            n,clauses=args[:2];best,model=out;assert len(model)==n+1
            assert best==sum(any(model[abs(l)]==(l>0) for l in c) for c in clauses)
        elif fn=='P.vc_branch':
            edges,k=args;cover,nodes=out;assert 0<nodes<=2**(k+1)-1
            if cover is not None:assert len(set(cover))==len(cover)<=k and all(u in cover or v in cover for u,v in edges)
            else:
                from pysat.card import CardEnc
                n=max((max(e) for e in edges),default=-1)+1
                clauses=[[u+1,v+1] for u,v in edges]+(CardEnc.atmost(list(range(1,n+1)),bound=k,encoding=1).clauses if k<n else [])
                assert not sat_reference(max(n,max((abs(l) for c in clauses for l in c),default=0)),clauses,evidence)
        elif fn=='P.buss_kernel':
            edges,k=args;remaining={tuple(sorted(e)) for e in edges};budget=k
            if out is not None:
                forced,residual,new_k=out
                for v in forced:
                    assert sum(v in e for e in remaining)>budget
                    remaining={e for e in remaining if v not in e};budget-=1
                assert budget==new_k>=0 and remaining=={tuple(sorted(e)) for e in residual} and len(remaining)<=budget**2
            else:
                from pysat.card import CardEnc
                n=max((max(e) for e in edges),default=-1)+1
                clauses=[[u+1,v+1] for u,v in remaining]+(CardEnc.atmost(list(range(1,n+1)),bound=k,encoding=1).clauses if k<n else [])
                assert not sat_reference(max(n,max((abs(l) for c in clauses for l in c),default=0)),clauses,evidence)
        elif fn in ('P.permanent_ryser','P.det_bareiss'):
            values=matrix_query('permanent' if fn.endswith('permanent_ryser') else 'determinant',args[0],evidence)
            assert int(values[0])==out
        elif fn=='P.ov_brute':
            A,B=args;assert all(0<=v<1<<128 for v in A+B)
            text='ov '+str(len(A))+' '+str(len(B))+' '+' '.join(map(str,A+B))+'\n'
            answer,i,j,checked=map(int,native_query(text,evidence).split());assert bool(answer)==out
            if answer:assert A[i]&B[j]==0
            else:assert checked==len(A)*len(B)
        elif fn=='P.three_sum':
            xs=args[0]
            if out is None:assert all(v&1 for v in xs),'unreturned general negative 3SUM needs a reference beyond the odd-input certificate'
            else:
                assert sum(out)==0 and not Counter(out)-Counter(xs)
        elif fn=='P.planted_clique':
            n,k=args[:2];adj,planted=out;assert len(adj)==n and len(planted)==k
            assert all(not adj[v]>>v&1 for v in range(n))
            assert all((adj[u]>>v&1)==(adj[v]>>u&1) for u in range(n) for v in range(u))
            assert all(adj[u]>>v&1 for u in planted for v in planted if u!=v)
        elif fn=='P.degree_recover':
            adj,k=args;top=sorted(range(len(adj)),key=lambda v:(-adj[v].bit_count(),v))[:k];mask=sum(1<<v for v in top)
            scores=[(adj[v]&mask).bit_count()+int(v in top) for v in range(len(adj))]
            expected=sorted(sorted(range(len(adj)),key=lambda v:(-scores[v],v))[:k]);assert sorted(out)==expected
        elif fn=='P.pollard_rho':
            n=args[0];factor,steps=out;budget=kw.get('max_steps',10**7)
            assert 0<=steps<=budget
            assert factor is None and steps==budget or factor is not None and 1<factor<n and n%factor==0
        elif fn=='P.ug_instance':
            n,m,k,eps=args[:4];edges,labels=out
            assert len(edges)==m and len(labels)==n and len({tuple(sorted((a,b))) for a,b,c in edges})==m
            assert all(0<=a<n and 0<=b<n and a!=b and 0<=c<k for a,b,c in edges)
            assert sum((labels[b]-labels[a]-c)%k!=0 for a,b,c in edges)==round(eps*m)
            reached={0}
            while True:
                new=reached|{v for a,b,c in edges if a in reached or b in reached for v in(a,b)}
                if new==reached:break
                reached=new
            assert len(reached)==n
        elif fn=='P.ug_propagate':
            n,edges,k,root=args;assert len(out)==n and out[root]==0 and all(0<=v<k for v in out)
            adjacency=[[] for _ in range(n)]
            for a,b,c in edges:adjacency[a].append((b,c));adjacency[b].append((a,-c))
            visited={root};queue=[root]
            for a in queue:
                for b,c in adjacency[a]:
                    if b not in visited:assert out[b]==(out[a]+c)%k;visited.add(b);queue.append(b)
        elif fn=='P.ug_value':
            edges,labels,k=args;reference=Fraction(sum((labels[b]-labels[a]-c)%k==0 for a,b,c in edges),len(edges)) if edges else 1
            assert out==float(reference)
        elif fn=='P.sat_to_ov':
            clauses,n=args;A,B=out;h=n//2;assert(len(A),len(B))==(1<<h,1<<(n-h))
            for vectors,offset,width in ((A,0,h),(B,h,n-h)):
                for bits,mask in enumerate(vectors):
                    reference=0
                    for j,clause in enumerate(clauses):
                        satisfied=False
                        for literal in clause:
                            v=abs(literal)-1
                            if offset<=v<offset+width:satisfied|=bool(bits>>(v-offset)&1)==(literal>0)
                        if not satisfied:reference+=1<<j
                    assert mask==reference
        elif fn=='P.vandermonde_test':
            xs,p=args[:2];pit.append((xs,p,bool(kw.get('wrong',False)),out))
        elif fn=='X.random_ksat':
            n,m,k=args[:3];assert len(out)==m and all(len(c)==k and len({abs(l) for l in c})==k and all(1<=abs(l)<=n for l in c) for c in out)
        elif fn=='X.cdcl':
            n,clauses=args[:2];model,stats=out
            if stats['status']=='unknown':assert model is None
            else:
                reference=sat_reference(n,clauses,evidence);assert reference==(stats['status']=='sat')==(model is not None)
                if model is not None:assert all(any(model[abs(l)]==(l>0) for l in c) for c in clauses)
        else:raise AssertionError('unhandled retained call '+fn)
    if pit:
        text='pit_batch '+str(len(pit))+'\n'+''.join(str(len(xs))+' '+str(p)+' '+str(int(wrong))+' '+' '.join(map(str,xs))+'\n' for xs,p,wrong,_ in pit)
        values=native_query(text,evidence).splitlines();assert len(values)==len(pit)
        for result,(_,_,_,expected) in zip(values,pit):
            left,right,accepted=map(int,result.split());assert (left==right)==bool(accepted)==expected
    if name=='maxsat':
        for row in evidence['producer_witnesses']:
            clauses=row['clauses']
            for trial in row['random_assignments']:
                assert trial['satisfied']==sum(any(trial['model'][abs(l)]==(l>0) for l in c) for c in clauses)
            assert row['walksat_satisfied']==sum(any(row['walksat_model'][abs(l)]==(l>0) for l in c) for c in clauses)
    if name=='vc':
        for row in evidence['producer_witnesses']:assert all(u in row['planted_cover'] or v in row['planted_cover'] for u,v in row['edges'])
    if name=='oneway':
        for row in evidence['producer_witnesses']:
            assert isprime(row['p']) and isprime(row['q']) and row['N']==row['p']*row['q'] and row['actual_bits']==row['N'].bit_length()
            assert row['N']%row['factor']==0 and row['batch_operations']==1000
    return dict(passed=True,call_counts=dict(counts),unique_calls_checked=len(validated),
                native_queries=len(evidence.get('native_queries',[])),native_sat_queries=len(evidence.get('native_sat_queries',[])),
                scope='Complete retained actual inputs, outputs and sampled protocol transcripts. Independent exact rational/Fourier/partial-state references, native GMP/CRT/subset-DP checks, full models and explicit finite negative certificates. No asymptotic or cryptographic security theorem is inferred.')

_validate_teaching_calls=validate_recording

def validate_recording(name,evidence):
    result=_validate_teaching_calls(name,evidence)
    if name=='blr_minima':
        reference=[list(map(int,line.split())) for line in native_query('blr4\n',evidence).splitlines()]
        witness=evidence['producer_witnesses'];assert witness['records']==reference and len(reference)==65536
        for row in witness['rows']:
            group=[r for r in reference if r[1]==row['distance_numerator']]
            assert row['bad_pairs']==min(r[2] for r in group) and reference[row['witness']][1:]==[row['distance_numerator'],row['bad_pairs']]
        result.update(exhaustive_functions=65536,independent_native_direct_queries=65536*256)
    if name=='fiat_shamir':
        witness=evidence['producer_witnesses'];st=witness['statement'];n=st['n'];clauses=st['clauses'];p=st['p']
        text='satcount '+str(n)+' '+str(len(clauses))+' '+' '.join(str(len(c))+' '+' '.join(map(str,c)) for c in clauses)+'\n'
        count=int(native_query(text,evidence));assert count==st['claim']==59049
        def independent_verify(statement,proof):
            try:
                n=statement['n'];p=statement['p'];current=statement['claim']%p;prefix=[];history=[]
                if n!=20 or statement['degree_bound']!=1 or len(proof)!=n:return False
                for values in proof:
                    if len(values)!=2 or sum(values)%p!=current:return False
                    history.append(dict(message=values))
                    raw=b'CS27-SUMCHECK-FS-TEACHING-v1\0'+json.dumps(dict(statement=statement,history=history),sort_keys=True,separators=(',',':')).encode()
                    counter=0
                    while True:
                        h=hashlib.sha256(raw+counter.to_bytes(8,'big')).digest();integer=int.from_bytes(h,'big')
                        if integer<(1<<256)//p*p:break
                        counter+=1
                    r=integer%p;history[-1]['challenge']=r;prefix.append(r);current=eval_interpolant(values,r,p)
                return current==direct_polynomial(statement['clauses'],prefix,p)
            except (ValueError,TypeError,KeyError,IndexError):return False
        assert independent_verify(st,witness['proof'])
        for case in witness['cases']:assert case['accepted']==independent_verify(case['statement'],case['proof'])
        result.update(actual_full_assignments=1<<n,mutation_cases=len(witness['cases']),scope='Structured finite hash-challenge demonstration, independent exhaustive count and actual mutation checks. This does not establish generic Fiat-Shamir security.')
    result['native_queries']=len(evidence.get('native_queries',[]))
    return result
