"""Source-bound native receipts. Timestamp buffering adds one integer store per clock read.

No file I/O occurs between timed clock reads. Full semantic checks run after timers.
Native summaries use the minimum of the recorded repetitions; they are observations
on this shared host, not causal estimates or portable speed guarantees.
"""
from __future__ import annotations
import hashlib,json,os,platform,re,subprocess,time
from pathlib import Path


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),default=int).encode()).hexdigest()


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


CLOCK = r'''
static void cs24_check(int ok,const char *name,unsigned long long count);
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
static uint64_t cs24_stamps[16384];
static unsigned cs24_nstamps;
static double now() {
  struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts);
  uint64_t ns = (uint64_t)ts.tv_sec * 1000000000ULL + (uint64_t)ts.tv_nsec;
  if (cs24_nstamps >= 16384) abort();
  cs24_stamps[cs24_nstamps++] = ns;
  return ts.tv_sec + ts.tv_nsec * 1e-9;
}
static void cs24_check(int ok,const char *name,unsigned long long count) {
  if (!ok) { fprintf(stderr,"CS24 validation failed: %s\n",name); abort(); }
  const char *p=getenv("CS24_VALIDATION_LOG"); if (!p) return;
  FILE *f=fopen(p,"a"); if (!f) abort();
  fprintf(f,"%s %llu\n",name,count); if(fclose(f)) abort();
}
__attribute__((destructor)) static void cs24_write_stamps() {
  const char *p = getenv("CS24_TRIAL_LOG"); if (!p) return;
  FILE *f = fopen(p,"w"); if (!f) abort();
  fprintf(f,"["); for(unsigned i=0;i<cs24_nstamps;i++) fprintf(f,"%s%llu",i?",":"",(unsigned long long)cs24_stamps[i]);
  fprintf(f,"]\n"); if(fclose(f)) abort();
}
'''


class NativeAudit:
    def __init__(self, root):
        self.root=Path(root).resolve()/str(time.time_ns());self.root.mkdir(parents=True,exist_ok=False)
        self.builds=[];self.executions=[]

    def build(self,d,name,code,cc='gcc',flags=('-O2',),libs=()):
        ext='.cpp' if cc=='g++' else '.c'
        original=code
        pattern=r'static double now\((?:void)?\)\s*\{[^\n]*\}'
        code,n=re.subn(pattern,lambda _:CLOCK,code)
        assert n==1,(name,n)
        key=digest(dict(original=original,cc=cc,flags=flags,libs=libs,instrumentation=CLOCK))[:20]
        dest=self.root/(name+'-'+key);dest.mkdir(exist_ok=True)
        (dest/('original'+ext)).write_text(original);(dest/('timed'+ext)).write_text(code)
        path=Path(d,name+ext);path.write_text(code)
        argv=[cc,*flags,'-o',name,name+ext,*libs]
        result=subprocess.run(argv,cwd=d,capture_output=True,text=True)
        (dest/'compiler.stdout').write_text(result.stdout);(dest/'compiler.stderr').write_text(result.stderr)
        result.check_returncode()
        binary=Path(d,name);(dest/'program').write_bytes(binary.read_bytes())
        asm=subprocess.run(['objdump','-d',str(binary)],capture_output=True,text=True,check=True)
        (dest/'disassembly.txt').write_text(asm.stdout)
        rec=dict(name=name,compiler=subprocess.check_output([cc,'--version'],text=True).splitlines()[0],argv=argv,
                 original_sha256=file_hash(dest/('original'+ext)),timed_sha256=file_hash(path),binary_sha256=file_hash(binary),
                 assembly_sha256=file_hash(dest/'disassembly.txt'),path=str(dest),flags=list(flags),libs=list(libs))
        self.builds.append(rec)
        return './'+name

    def run(self,d,exe,*args,env=None,text=True):
        index=len(self.executions);stamp=self.root/f'timestamps-{index:04d}.json'
        validation=self.root/f'validation-{index:04d}.txt'
        validation.unlink(missing_ok=True)
        run_env=dict(os.environ if env is None else env,CS24_TRIAL_LOG=str(stamp),CS24_VALIDATION_LOG=str(validation))
        result=subprocess.run([exe,*map(str,args)],cwd=d,capture_output=True,text=text,check=True,env=run_env)
        raw=json.loads(stamp.read_text());assert raw and all(b>=a for a,b in zip(raw,raw[1:]))
        stdout=result.stdout if text else result.stdout.decode();stderr=result.stderr if text else result.stderr.decode()
        rec=dict(executable=exe,args=list(map(str,args)),clock='CLOCK_MONOTONIC',timestamps_ns=raw,
                 stdout=stdout,stderr=stderr,semantic_checks=validation.read_text().splitlines() if validation.exists() else [],pad_bytes=len(run_env.get('PAD','')),
                 threads={k:run_env[k] for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS') if k in run_env})
        self.executions.append(rec)
        return result

    def receipt(self):
        return dict(builds=self.builds,executions=self.executions,host=platform.platform(),
                    clock_instrumentation='uint64 nanoseconds buffered after every clock_gettime; written at exit; one store per read',
                    timing_statistic='minimum of fixed repetitions unless explicitly labeled otherwise',
                    limitation='shared host; algorithm order fixed inside native runs; no causal hardware counter attribution')


def mo_reference(a, queries):
    """Offline last-occurrence sweep; a separate iterative sum tree, no Mo moves."""
    size=1
    while size<len(a):size*=2
    tree=[0]*(2*size);last={};out=[0]*len(queries);at=0
    def put(i,value):
        i+=size;tree[i]=value
        while i>1:i//=2;tree[i]=tree[i*2]+tree[i*2+1]
    for qi,(l,r) in sorted(enumerate(queries),key=lambda row:row[1][1]):
        while at<=r:
            if a[at] in last:put(last[a[at]],0)
            put(at,1);last[a[at]]=at;at+=1
        lo,hi=l+size,r+1+size;s=0
        while lo<hi:
            if lo&1:s+=tree[lo];lo+=1
            if hi&1:hi-=1;s+=tree[hi]
            lo//=2;hi//=2
        out[qi]=s
    return out


def ski_parameters(B,lam):
    from fractions import Fraction
    import operator
    if isinstance(B,bool):raise TypeError('B must be an integer')
    B=operator.index(B)
    if B<=0:raise ValueError('B must be positive')
    if isinstance(lam,bool):raise TypeError('lambda must be a finite real in (0,1]')
    try:lam=Fraction(str(lam))
    except (ValueError,ZeroDivisionError):raise ValueError('lambda must be finite') from None
    if not 0<lam<=1:raise ValueError('lambda must be in (0,1]')
    ceil=lambda x:-(-x.numerator//x.denominator)
    early,late=ceil(lam*B),ceil(Fraction(B)/lam)
    consistency=Fraction(B+early-1,B)
    worst=max(Fraction(B+early-1,early),Fraction(B+late-1,B))
    return B,lam,early,late,consistency,worst


def ski_ratio(B,days,forecast,lam):
    import math,operator
    B,lam,early,late,_,_=ski_parameters(B,lam)
    if isinstance(days,bool):raise TypeError('days must be an integer')
    days=operator.index(days)
    if days<=0:raise ValueError('days must be positive')
    if not math.isfinite(forecast):raise ValueError('forecast must be finite')
    buy=early if forecast>=B else late
    return (days if days<buy else B+buy-1)/min(days,B)


def verify_illustrations(name,d,P):
    """Independent complete illustrated outputs, checked after timing intervals."""
    checks=[]
    def check(label,got,expected):
        assert got==expected,(name,label,got,expected)
        checks.append(dict(label=label,output_sha256=digest(got),reference_sha256=digest(expected)))
    if name=='prefix':
        a=d['a'];check('all_prefixes',d['S'],[sum(a[:i]) for i in range(len(a)+1)])
        ref=[sum(v for l,r,v in d['updates'] if l<=i<=r) for i in range(len(a))]
        check('all_difference_updates',d['after'],ref)
        image=d['img'];integral=[[sum(image[y][x] for y in range(r) for x in range(c)) for c in range(len(image[0])+1)] for r in range(len(image)+1)]
        check('every_integral_cell',d['I'],integral);l,r=d['query'];check('range',d['query_sum'],sum(a[l:r+1]))
        r0,c0,r1,c1=d['box'];check('box',d['box_sum'],sum(image[y][x] for y in range(r0,r1+1) for x in range(c0,c1+1)))
    elif name=='fenwick':
        check('update_path',d['update_path'],[i for i in range(1,d['n']+1) if i-(i&-i)<5<=i])
        check('query_cover',sorted(j for i in d['query_path'] for j in range(i-(i&-i)+1,i+1)),list(range(1,14)))
    elif name=='segtree':
        a=d['a'];l,r=d['query'];check('range_min',d['min'],min(a[l:r+1]))
        check('cover_partition',sorted(i for _,lo,hi in d['cover'] for i in range(lo,hi+1)),list(range(l,r+1)))
    elif name=='rmq':
        a=d['a'];st=P.SparseTable(a)
        for l in range(len(a)):
            for r in range(l,len(a)):
                check(f'argmin_{l}_{r}',st.argmin(l,r),min(range(l,r+1),key=lambda i:(a[i],i)))
        parent=d['parent'];kids={}
        for v,p in enumerate(parent):
            if p>=0:kids.setdefault(p,[]).append(v)
        e=P.EulerLCA(kids,0);b=P.BinaryLift([0]+parent[1:],0)
        def ancestors(v):
            out=[]
            while v>=0:out.append(v);v=parent[v]
            return out
        for u in range(len(parent)):
            for v in range(len(parent)):
                ref=next(w for w in ancestors(v) if w in ancestors(u));check(f'lca_{u}_{v}',[e.lca(u,v),b.lca(u,v)],[ref,ref])
        # Recursive interval minimum defines the Cartesian parent relation independently.
        ref=[-1]*len(a)
        def visit(lo,hi,p):
            if lo>=hi:return
            m=min(range(lo,hi),key=lambda i:(a[i],i));ref[m]=p;visit(lo,m,m);visit(m+1,hi,m)
        visit(0,len(a),-1);check('cartesian_leftmost',d['cartesian'],ref)
    elif name=='monotone':
        a=d['a'];k=d['k'];check('every_window',d['max'],[max(a[i:i+k]) for i in range(len(a)-k+1)])
        check('every_next_greater',d['next_greater'],[next((j for j in range(i+1,len(a)) if a[j]>v),-1) for i,v in enumerate(a)])
        h=d['h'];best=max([0]+[(r-l+1)*min(h[l:r+1]) for l in range(len(h)) for r in range(l,len(h))]);check('all_histogram_rectangles',d['rect'][0],best)
        # A surviving index is larger than every later value in the active window.
        # This suffix-record characterization independently checks every deque state.
        for i,state in enumerate(d['trace']):
            candidates=range(max(0,i-k+1),i+1)
            expected=[j for j in candidates if all(a[j]>a[t] for t in range(j+1,i+1))]
            check('deque_state_'+str(i),state,expected)
        check('total_deque_removals',d['pops'],len(a)-len(d['trace'][-1]))
        import random
        rng=random.Random(6)
        for row in d['scale']:
            values=[rng.randint(0,10**6) for _ in range(row['n'])]
            final=values[-64:]
            survivors=sum(all(v>later for later in final[j+1:]) for j,v in enumerate(final))
            check('scaled_removals_'+str(row['n']),row['pops'],row['n']-survivors)
    elif name=='search':
        w=d['w'];days=d['days']
        def feasible(cap):
            used=1;load=0
            for x in w:
                if load+x>cap:used+=1;load=0
                load+=x
            return used<=days
        check('every_answer_predicate',d['pred'],[dict(cap=c,ok=feasible(c)) for c in range(max(w),sum(w)+1)])
        check('minimum_feasible',d['cap'],next(c for c in range(max(w),sum(w)+1) if feasible(c)))
    elif name=='bits':
        check('all_popcounts',[r['pop'] for r in d['table']],[bin(i).count('1') for i in range(16)])
        for row in d['submasks']:check('submask_pairs_'+str(row['n']),row['pairs'],row['three'])
    elif name=='pairs':check('stress_failures',d['fails'],0)
    return checks



def job_code(name,code):
    """Dump every final count after the timing endpoint, retaining exact top20 output."""
    if name=='textbook':
        marker=' double elapsed=now()-begin;'
        addition=r'''
 const char *counts_path=getenv("CS24_COUNTS_FILE");
 if(counts_path){FILE *cf=fopen(counts_path,"wb");if(!cf)abort();
  for(size_t k=0;k<shown;k++)entries[selected[k]].count=counts[k];
  for(size_t e=0;e<ne;e++){fwrite(pool+entries[e].start,1,entries[e].len,cf);fprintf(cf," %llu\n",(unsigned long long)entries[e].count);}
  if(fclose(cf))abort();}
'''
    else:
        marker='  double s = now() - t0;'
        addition=r'''
 const char *counts_path=getenv("CS24_COUNTS_FILE");
 if(counts_path){FILE *cf=fopen(counts_path,"wb");if(!cf)abort();
  for(int k=0;k<shown;k++)cnt[top[k]]=topc[k];
  for(long e=0;e<ne;e++){fwrite(pool+es[e],1,el[e],cf);fprintf(cf," %u\n",cnt[e]);}
  if(fclose(cf))abort();}
'''
    assert code.count(marker)==1
    return code.replace(marker,marker+addition)


def decode_timings(receipt):
    """Decode complete raw clock sequences, not the rounded stdout summaries."""
    groups=[]
    for execution in receipt['executions']:
        exe=Path(execution['executable']).name;t=execution['timestamps_ns']
        def pairs(labels,blocks,repeats):
            width=2*len(labels);assert len(t)==blocks*repeats*width,(exe,len(t))
            for block in range(blocks):
                for rep in range(repeats):
                    base=(block*repeats+rep)*width
                    for j,label in enumerate(labels):
                        groups.append(dict(executable=exe,args=execution['args'],block=block,repetition=rep,operation=label,seconds=(t[base+2*j+1]-t[base+2*j])*1e-9))
        def phases(labels,blocks,repeats,width):
            assert len(t)==blocks*repeats*width,(exe,len(t))
            for block in range(blocks):
                for rep in range(repeats):
                    base=(block*repeats+rep)*width
                    for label,start,end in labels:
                        groups.append(dict(executable=exe,args=execution['args'],block=block,repetition=rep,operation=label,seconds=(t[base+end]-t[base+start])*1e-9))
        if exe=='hook':pairs(['array_sum','linked_sum'],1,5)
        elif exe=='ranges':pairs(['plain_1024_operations','prefix_1024_operations','fenwick_1048576_operations','segtree_1048576_operations'],1,1)
        elif exe=='layouts':pairs(['sorted_branchy','sorted_branchless','eytzinger','avx512_btree'],9,3)
        elif exe=='maps':phases([(f'{a}_{p}',3*j+k,3*j+k+1) for j,a in enumerate(('unordered_map','linear','swiss_sse2')) for k,p in enumerate(('construction_insert','lookup'))],8,3,9)
        elif exe=='sorts':phases([('copy_sort',0,1),('copy_radix',1,2)],11,3,3)
        elif exe=='bits':pairs(['closure_byte','closure_uint64','lcs_dp','lcs_uint64'],1,1)
        elif exe=='tok':pairs(['scalar_tokenize','avx2_tokenize'],1,5)
        elif exe=='bench':
            if execution['args'][0]=='0':pairs(['fixed_loop'],1,6)
            else:phases([('unused_loop',0,1),('kept_loop',1,2)],1,1,3)
        elif exe in ('textbook','engineered'):pairs(['whole_job_without_input_read_or_output'],1,1)
        elif exe=='learned':pairs(['binary_lookup','model_bracket_lookup'],1,3)
        elif exe=='branches':pairs(['random_branchy','sorted_branchy','random_branchless','sorted_branchless'],1,5)
        elif exe.startswith('vec_'):pairs(['saxpy_4000_loops','integer_sum_4000_loops','copy_prefix_400_loops'],1,1)
        elif exe=='topk':pairs(['full_sort_extract','partial_sort_extract','nth_element_sort_extract','heap_build_extract'],1,3)
        else:raise AssertionError(('unrecognized timed executable',exe))
    assert all(g['seconds']>=0 for g in groups)
    return groups
