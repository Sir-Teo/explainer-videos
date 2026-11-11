"""Finite experiments for Part 25: full witnesses, explicit cutoffs and schema-2 provenance.

Run python -m videos.cs.cs25.compute [names] [--force]. Numerical artifacts live
in .cache/cs25/artifacts. Failed bounded searches are not general impossibility
proofs. Host durations describe this retained workload, not benchmark guarantees.
"""
from __future__ import annotations

import argparse
import bz2
import contextlib
import functools
import hashlib
import inspect
import io
import json
import lzma
import math
import platform
import random
import statistics
import sys
import time
import zlib
from pathlib import Path

import numpy as np
from explainer.ai.cache import Cache
from explainer.cache_lock import cache_lock, locked_item
from explainer.cs.algo import computability as C
from . import computational_references as R

SOURCE_FILES = tuple(sorted(set(
    [Path(__file__).resolve(),Path(C.__file__).resolve(),Path(R.__file__).resolve(),
     Path('explainer/cs/algo/paradigms.py').resolve(),Path('explainer/cs/turing.py').resolve(),
     Path('videos/cs/cs16/compute.py').resolve(),Path('videos/cs/cs6/compute.py').resolve(),
     Path('videos/ai/ai1/compute.py').resolve(),Path('explainer/cs/lang/pebble_lang.py').resolve()]
    + [p.resolve() for d in ('explainer/cs/lang/compiler','explainer/cs/pebble') for p in Path(d).rglob('*.py')]
)))


def source_signature():
    return {str(p.relative_to(Path.cwd())):R.digest(p.read_bytes()) for p in SOURCE_FILES}


def cache_current(name, path=None):
    path = CACHE.path(name) if path is None else Path(path)
    try:
        data = json.loads(path.read_text())
        return (data.get('schema') == 2 and data.get('source_sha256') == source_signature()
                and all(Path(a['path']).exists() and R.digest(Path(a['path']).read_bytes()) == a['sha256']
                        for a in data['artifacts']))
    except (OSError,ValueError,KeyError): return False


class ComputabilityCache(Cache):
    @locked_item(lambda self,name:self.path(name))
    def load(self,name):
        if not cache_current(name): self.save(name,ITEMS[name]())
        return super().load(name)

    def main(self,items,doc=None):
        parser=argparse.ArgumentParser(description=doc)
        parser.add_argument('names',nargs='*',default=list(items));parser.add_argument('--force',action='store_true')
        args=parser.parse_args();self.items=items
        if any(n not in items for n in args.names): parser.error('unknown producer')
        for name in args.names:
            with cache_lock(self.path(name)):
                if not args.force and cache_current(name): print('  cached ',name,flush=True);continue
                print('  compute',name,flush=True);self.save(name,items[name]());print('  done   ',name,flush=True)


CACHE=ComputabilityCache('cs25');load=CACHE.load


def _producer(name,fn):
    @functools.wraps(fn)
    def run():
        sources=source_signature();start=time.monotonic_ns();data=fn()
        assert sources == source_signature(),'source changed during compute'
        # Each producer lists its actual raw inputs, complete outputs and references.
        metadata=dict(schema=2,source_sha256=sources,elapsed_ns=time.monotonic_ns()-start,
                      host=platform.platform(),python_version=sys.version,
                      scope='Finite computation; published theorem assumptions stated separately.')
        assert not data.keys() & metadata.keys(), 'producer metadata would overwrite a result field'
        data.update(metadata)
        return data
    return run


def compute_quines():
    from explainer.cs.lang.compiler import driver as Dr
    q=C.python_quine();buf=io.StringIO()
    with contextlib.redirect_stdout(buf):exec(q,{})
    assert buf.getvalue()==q
    artifacts=[R.artifact('quines/python.py',q.encode()),R.artifact('quines/python-output.txt',buf.getvalue().encode())]
    receipts={}
    for name,src in [('forward',C.pebble_quine()),('backward',C.pebble_backward_quine())]:
        comp=Dr.compile_program(src,2);r=Dr.run(comp,b'');actual=bytes(r.output)
        expected=src.encode() if name=='forward' else src.encode()[::-1]
        assert actual==expected
        artifacts.extend([R.artifact(f'quines/{name}.pebble',src.encode()),R.artifact(f'quines/{name}.image',bytes(comp.program.image)),
                          R.artifact(f'quines/{name}.asm',comp.asm.encode()),R.artifact(f'quines/{name}-output.txt',actual)])
        receipts[name]=dict(source_bytes=len(src.encode()),output_sha256=R.digest(actual),steps=r.steps,stats=comp.stats,byte_exact=True)
        if name=='forward':forward=src;steps=r.steps
    lines=forward.splitlines()
    return dict(python=q,python_ok=True,pebble_len=len(forward),pebble_lines=len(lines),pebble_ok=True,pebble_steps=steps,
                pebble_head=lines[:14],pebble_data=lines[14:18],pebble_tail=lines[-16:],
                data_lines=sum(ln.strip().startswith('d[') for ln in lines),receipts=receipts,artifacts=artifacts)


def compute_pcp():
    sip=[('b','ca'),('a','ab'),('ca','a'),('abc','c')];s=C.pcp_search(sip,10)
    rules={('q','1'):('p','1','R'),('p','0'):('a','0','R'),('q','0'):('r','0','R'),
           ('p','1'):('r','1','R'),('q','_'):('r','_','R'),('p','_'):('r','_','R')}
    D=C.tm_to_mpcp(rules,'q','a','10','01');t=C.pcp_search(D,60,first=0)
    trace=C.run_tm_trace(rules,'q','a','10');assert trace['status']=='accepted'
    R.match(D,t['match'],first=0);top=''.join(D[i][0] for i in t['match']);assert top.startswith(trace['history'])
    artifacts=[]
    for name,dominoes,result,first in [('sipser',sip,s,None),('mpcp',D,t,0)]:
        artifacts.append(R.artifact(f'pcp/{name}-shortest.json.gz',R.pcp_certificate(dominoes,result['match'],first)))
    rng=random.Random(25);words=[format(i,f'0{n}b') for n in (1,2,3) for i in range(2**n)]
    samples=[];best=[];statuses={}
    for j in range(20_000):
        inst=[(rng.choice(words),rng.choice(words)) for _ in range(3)]
        r=C.pcp_search(inst,60,max_nodes=20_000)
        statuses[r['status']]=statuses.get(r['status'],0)+1
        if r['match'] is not None:
            R.match(inst,r['match']);best.append((len(r['match']),inst,r['match'],r['nodes']))
        samples.append(dict(index=j,dominoes=inst,**r))
    best.sort(key=lambda x:-x[0]);lens=[b[0] for b in best]
    artifacts.append(R.artifact('pcp/all-20000-samples.json.gz',dict(seed=25,max_len=60,max_nodes=20000,samples=samples)))
    hard=[dict(len=b[0],dominoes=b[1],match=b[2],nodes=b[3]) for b in best[:5]]
    for i,row in enumerate(hard):artifacts.append(R.artifact(f'pcp/hard-{i}-shortest.json.gz',R.pcp_certificate(row['dominoes'],row['match'])))
    four=[('1000','0'),('01','0'),('1','101'),('00','001')];f=C.pcp_search(four,300)
    assert len(f['match'])==206
    cert=R.pcp_certificate(four,f['match']);artifacts.append(R.artifact('pcp/four-206-shortest.json.gz',cert))
    artifacts.append(R.artifact('pcp/tm-trace.json',dict(rules=[[list(k),v] for k,v in rules.items()],**trace)))
    return dict(sipser=sip,sipser_match=s['match'],sipser_nodes=s['nodes'],tm_dominoes=D,tm_match=t['match'],tm_nodes=t['nodes'],
                history=trace['history'],tm_top=top,hard=hard,tried=len(samples),solved=len(best),statuses=statuses,
                len_hist={str(k):lens.count(k) for k in sorted(set(lens))},four=dict(dominoes=four,**f,certificate_states=len(cert['states'])),
                artifacts=artifacts,node_convention='Dequeued residual states, including root; old 73134 excludes the root.')


def compute_tiles():
    T=C.JEANDEL_RAO;rects=[];checks=[];artifacts=[]
    for n in (4,8,12,16,20):
        start=time.monotonic_ns();g,nodes,done=C.wang_tile(T,n,n,limit=50_000_000)
        rects.append(dict(n=n,found=g is not None,complete=done,nodes=nodes,seconds=(time.monotonic_ns()-start)/1e9,grid=g))
        assert g is not None;checks.append(R.grid(T,g))
    tori=[]
    for n in range(1,9):
        for m in range(1,9):
            g,nodes,done=C.wang_tile(T,n,m,limit=3_000_000,periodic=True)
            tori.append(dict(n=n,m=m,found=g is not None,complete=done,nodes=nodes,grid=g,
                             status='found' if g else ('refuted' if done else 'node-limit')))
            if g is not None:checks.append(R.grid(T,g,True))
    for width in range(1,9):artifacts.append(R.artifact(f'tiles/row-dag-{width}.json.gz',R.tile_row_certificate(T,width)))
    P=[(0,1,1,0),(1,0,0,1)];gp,_,_=C.wang_tile(P,4,4,periodic=True);checks.append(R.grid(P,gp,True))
    return dict(tiles=T,rects=rects,tori=tori,refuted=sum(not t['found'] and t['complete'] for t in tori),
                periodic_example=P,periodic_grid=gp,grid_checks=checks,row_dag_widths=list(range(1,9)),artifacts=artifacts)


def compute_hilbert():
    rows=[];certs=[]
    for D in (2,3,5,7,13,29,61,109,181,991):
        cert={};x,y=C.pell(D,certificate=cert);check=R.pell_certificate(D,x,y,cert);clocks=[]
        for _ in range(9):
            start=time.monotonic_ns();assert C.pell(D)==(x,y);end=time.monotonic_ns();clocks.append([start,end])
        median=statistics.median(b-a for a,b in clocks)/1e9
        rows.append(dict(D=D,x=str(x),y=str(y),digits=len(str(x)),cf_seconds=median,clock_pairs_ns=clocks))
        certs.append(dict(**cert,check=check))
    brute=[]
    for D in (13,29,61):
        start=time.monotonic_ns();found=None;tried=0;cap=1_000_000
        for y in range(1,cap+1):
            v=D*y*y+1;r=math.isqrt(v);tried+=1
            if r*r==v:found=(r,y);break
        brute.append(dict(D=D,found=found is not None,solution=found,tried=tried,seconds=(time.monotonic_ns()-start)/1e9,
                          cap=cap,status='found' if found else 'attempt-limit'))
    return dict(rows=rows,brute=brute,artifacts=[R.artifact('pell/convergents.json',certs)],
                timing_scope='Nine monotonic repetitions; displayed median is descriptive. Brute uses a deterministic million-attempt cap.')


def compute_fractran():
    trace=bytearray();start=time.monotonic_ns();r=C.fractran_run(C.PRIMEGAME,2,3_000_000,trace=trace);seconds=(time.monotonic_ns()-start)/1e9
    output,native=R.native('fractran',bytes(trace));lines=output.decode().splitlines();pairs=[tuple(map(int,s.split())) for s in lines[:-1]]
    assert pairs==r['outputs']
    exponents=list(map(int,lines[-1].split()[1:]));primes=[2,3,5,7,11,13,17,19,23,29]
    assert math.prod(p**e for p,e in zip(primes,exponents))==r['final']
    expected=[p for p in range(2,128) if all(p%d for d in range(2,math.isqrt(p)+1))]
    assert [p for _,p in pairs]==expected
    return dict(primes=expected,steps=[s for s,_ in pairs],seconds=seconds,status=r['status'],executed=r['steps'],final=str(r['final']),
                artifacts=[R.artifact('fractran/instruction-trace.gz',bytes(trace)),R.artifact('fractran/run.json',(r | {'final':str(r['final'])})),
                           R.artifact('fractran/native-receipt.json',native),*[v for v in native.values() if isinstance(v,dict) and 'path' in v]],
                timing_scope='Three million Python first-applicable steps including instruction trace recording; reference replay excluded.')


def compute_collatz():
    N=1_000_000;lengths=np.zeros(N,dtype=np.uint32);peaks=np.zeros(N,dtype=np.uint64);peaks[1]=1
    best,best_n,peak_best,peak_n=0,1,1,1;records=[]
    for n in range(2,N):
        m,s,pk=n,0,n
        while m>=n:
            m=m//2 if m%2==0 else 3*m+1;pk=max(pk,m);s+=1
            if s==10_000_000:raise TimeoutError('prefix reference budget')
        lengths[n]=s+int(lengths[m]);peaks[n]=max(pk,int(peaks[m]))
        if lengths[n]>best:best,best_n=int(lengths[n]),n;records.append((n,best))
        if peaks[n]>peak_best:peak_best,peak_n=int(peaks[n]),n
    output,native=R.native('collatz',f'{N}\n'.encode())
    independent=np.frombuffer(output,dtype=np.dtype([('steps','<u4'),('peak','<u8')]))
    assert len(independent)==N-1 and np.array_equal(independent['steps'],lengths[1:]) and np.array_equal(independent['peak'],peaks[1:])
    traj=[27]
    while traj[-1]!=1:traj.append(traj[-1]//2 if traj[-1]%2==0 else 3*traj[-1]+1)
    return dict(N=N,longest_n=best_n,longest=best,records=records,peak_n=peak_n,peak=peak_best,traj27=traj,
                verified_to='This run: every positive start below one million; no general Collatz conclusion.',
                artifacts=[R.artifact('collatz/all-lengths.u32.gz',lengths.astype('<u4').tobytes()),R.artifact('collatz/all-peaks.u64.gz',peaks.astype('<u8').tobytes()),
                           R.artifact('collatz/native-receipt.json',native),*[v for v in native.values() if isinstance(v,dict) and 'path' in v]])


def compute_kolmo():
    from videos.cs.cs16.compute import _full_text
    from explainer.cs.algo.paradigms import chudnovsky
    n=100_000;rng=random.Random(5);pi=C.pi_digits(n);certificate={}
    certified=chudnovsky(n-1,certificate=certificate);old=sys.get_int_max_str_digits();sys.set_int_max_str_digits(0)
    try:assert str(certified)==pi
    finally:sys.set_int_max_str_digits(old)
    full=_full_text();samples={'random bytes':bytes(rng.getrandbits(8) for _ in range(n)),
        'English text':full[1_000_000:1_000_000+n],'digits of pi':pi.encode(),'Thue-Morse':C.thue_morse(n).encode(),
        '0101...':('01'*(n//2)).encode(),'all zeros':b'0'*n}
    rows=[];artifacts=[]
    for i,(name,data) in enumerate(samples.items()):
        assert len(data)==n
        enc={'zlib':zlib.compress(data,9),'bz2':bz2.compress(data,9),'lzma':lzma.compress(data,preset=9|lzma.PRESET_EXTREME)}
        for key,decode in [('zlib',zlib.decompress),('bz2',bz2.decompress),('lzma',lzma.decompress)]:
            assert decode(enc[key])==data;artifacts.append(R.artifact(f'compression/{i}-{key}.bin',enc[key]))
        r=C.complexity_proxies(data);assert all(r[k]==len(v) for k,v in enc.items())
        rows.append(dict(name=name,**r,best=min(len(v) for v in enc.values()),input_sha256=R.digest(data)))
        artifacts.append(R.artifact(f'compression/{i}-input.gz',data))
    src=inspect.getsource(C.pi_digits)
    # Avoid a giant integer JSON conversion while retaining its exact digest.
    cert=dict(terms=certificate['terms'],guard_digits=certificate['guard_digits'],
              lower_equals_upper=certificate['lower_floor']==certificate['upper_floor'],prefix_sha256=R.digest(pi.encode()),
              decimal_places=n-1,digits_including_leading_three=n)
    artifacts.append(R.artifact('compression/pi-certificate.json',cert))
    return dict(rows=rows,n=n,pi_program_bytes=len(src.encode()),pi_program_lines=len(src.splitlines()),artifacts=artifacts,
                corpus_sha256=R.digest(full),zlib_version=zlib.ZLIB_RUNTIME_VERSION,
                libraries='Python bz2/lzma containers and zlib; exact compressed bytes retained.',
                complexity_scope='Bytes times eight plus fixed decoder/interpreter/framing cost bounds plain C, not prefix-free K. Printer size excludes n, caller and dependencies.')


def compute_godel():
    codes={'0':1,'S':2,'=':3,'+':4,'(':5,')':6,'¬':7,'∀':8,'x':9,'→':10};primes=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53];out=[]
    for f in ['0=0','S0=S0','∀x(x+0=x)']:
        assert len(f)<=len(primes) and all(all(p%d for d in range(2,math.isqrt(p)+1)) for p in primes)
        g=math.prod(primes[i]**codes[ch] for i,ch in enumerate(f));dec=[];h=g
        for p in primes:
            e=0
            while h%p==0:h//=p;e+=1
            if not e:break
            dec.append(e)
        inv={v:k for k,v in codes.items()};decoded=''.join(inv[e] for e in dec)
        assert h==1 and decoded==f and len(dec)==len(f)
        out.append(dict(formula=f,codes=[codes[c] for c in f],number=str(g),digits=len(str(g)),decoded=decoded,remaining_factor=h))
    return dict(codes=codes,rows=out,primes=primes,artifacts=[R.artifact('godel/full-encode-decode.json',out)])


def compute_omega():
    from explainer.cs import turing as T
    rng=random.Random(3);N=5000;budgets=[1,2,4,8,16,32,64,128,512,2000];halt_at=[];texts=[]
    for _ in range(N):
        rules=[rng.choice('01')+rng.choice('LR')+rng.choice('ABCZ') for _ in range(6)]
        text='_'.join(''.join(rules[2*i:2*i+2]) for i in range(3));texts.append(text)
        r=T.run(T.TM.parse(text),max_steps=2000);halt_at.append(r.steps if r.halted else None)
    output,native=R.native('omega',('\n'.join(texts)+'\n').encode());reference=[int(s) or None for s in output.splitlines()]
    assert reference==halt_at
    k=sum(h is not None for h in halt_at);rows=[dict(t=t,fraction=sum(h is not None and h<=t for h in halt_at)/N) for t in budgets]
    return dict(N=N,rows=rows,longest=max(h for h in halt_at if h is not None),halted=k,wilson95=R.wilson(k,N),population_size=16**6,
                classification_assumption='Standard blank-tape 3-state 2-symbol machines: S(3)=21, including the final halting transition.',
                probability_scope='Exact sample fraction, not exact population probability. Wilson interval assumes iid uniform sampling with replacement.',
                artifacts=[R.artifact('omega/all-machines.json.gz',dict(seed=3,machines=texts,halt_at=halt_at,source_budget=2000,reference_budget=21)),R.artifact('omega/native-receipt.json',native),*[v for v in native.values() if isinstance(v,dict) and 'path' in v]])


def compute_hat():
    lattice=[(0,0),(-1,-1),(0,-2),(2,-2),(2,-1),(4,-2),(5,-1),(4,0),(3,0),(2,2),(0,3),(0,2),(-1,2)]
    cross=sum(x*v-u*y for (x,y),(u,v) in zip(lattice,lattice[1:]+lattice[:1]));P=C.hat_polygon()
    assert abs(cross)==32
    for (x,y),point in zip(lattice,P):assert np.allclose(point,[x+y/2,math.sqrt(3)*y/2],rtol=0,atol=1e-15)
    assert abs(C.shoelace(P)-8*math.sqrt(3))<1e-12
    cert=dict(lattice=lattice,integer_cross_sum=cross,area='abs(cross)*sqrt(3)/4 = 8*sqrt(3)',all_vertices_checked=True)
    return dict(P=P.tolist(),area=C.shoelace(P),kites=8,exact_area='8*sqrt(3)',artifacts=[R.artifact('hat/exact-lattice-area.json',cert)])


ITEMS={k[8:]:_producer(k[8:],v) for k,v in list(globals().items()) if k.startswith('compute_')}
if __name__=='__main__':CACHE.main(ITEMS,__doc__)
