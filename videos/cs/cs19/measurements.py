"""Independent certificates and explicit benchmark scope for Part 19."""
from __future__ import annotations
import hashlib,math,os,platform,struct,subprocess,tempfile
from pathlib import Path
import numpy as np


def protocol():
    import ctypes
    pools=[]
    for path in (Path(np.__file__).parent.parent/'numpy.libs').glob('*blas*.so'):
        library=ctypes.CDLL(str(path))
        for symbol in ('scipy_openblas_get_num_threads64_','openblas_get_num_threads64_','openblas_get_num_threads'):
            try:
                function=getattr(library,symbol);function.restype=ctypes.c_int
                pools.append(dict(library=path.name,query=symbol,configured_threads=function()));break
            except AttributeError:
                continue
    return dict(timer='time.perf_counter',statistic='minimum of recorded complete trials',
                validation='each timed output checked after stopping timer; reference preparation excluded',
                python=platform.python_version(),platform=platform.platform(),numpy=np.__version__,
                native_threadpools=pools,numpy_build=getattr(np.__config__,'CONFIG',{}),scope='one shared host; no causal hardware attribution')


def integer_digest(value):
    return hashlib.sha256(value.to_bytes(max(1,(value.bit_length()+7)//8),'big')).hexdigest()


def check_digits(coefficients,expected):
    from explainer.cs.algo import paradigms as P
    assert P.from_digits(P._carry(coefficients))==expected


def edit_reference(a,b):
    """Independent rolling-row Levenshtein reference, without traceback storage."""
    row=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        new=[i]
        for j,y in enumerate(b,1):new.append(min(new[-1]+1,row[j]+1,row[j-1]+(x!=y)))
        row=new
    return row[-1]


def check_edit(a,b,result,expected):
    table,ops,path=result;assert table[-1][-1]==expected
    assert len(table)==len(a)+1 and all(len(row)==len(b)+1 for row in table)
    assert table[0]==list(range(len(b)+1)) and [row[0] for row in table]==list(range(len(a)+1))
    assert path[0]==(0,0) and path[-1]==(len(a),len(b)) and len(path)==len(ops)+1
    edits=0
    for (i,j),(ii,jj),op in zip(path,path[1:],ops):
        assert (ii-i,jj-j) in [(1,0),(0,1),(1,1)]
        cost=(a[i]!=b[j]) if (ii-i,jj-j)==(1,1) else 1
        assert table[ii][jj]==table[i][j]+cost
        assert (op=='=')==(cost==0);edits+=cost
    assert edits==expected


def knapsack_reference(items,capacity):
    """Sparse weight/value frontier, distinct from the full dense row table."""
    frontier={0:0}
    for w,v in items:
        nxt=dict(frontier)
        for old,value in frontier.items():
            if old+w<=capacity:nxt[old+w]=max(nxt.get(old+w,-math.inf),value+v)
        high=-math.inf;frontier={}
        for weight,value in sorted(nxt.items()):
            if value>high:frontier[weight]=value;high=value
    return max(frontier.values())


def check_knapsack(items,capacity,result,expected):
    value,chosen,cells=result;assert value==expected and len(chosen)==len(set(chosen))
    assert sum(items[i][0] for i in chosen)<=capacity and sum(items[i][1] for i in chosen)==value
    assert cells==(len(items)+1)*(capacity+1)


def check_sudoku(givens,solution):
    assert solution is not None and len(solution)==81
    digits=set('123456789')
    assert all(g in '.0' or g==s for g,s in zip(givens,solution))
    rows=[solution[i:i+9] for i in range(0,81,9)]
    assert all(set(row)==digits for row in rows)
    assert all({rows[r][c] for r in range(9)}==digits for c in range(9))
    assert all({rows[r+i][c+j] for i in range(3) for j in range(3)}==digits for r in (0,3,6) for c in (0,3,6))


def prefix_maxsub(a):
    prefix=small=0;best=-math.inf
    for x in a:
        prefix+=x;best=max(best,prefix-small);small=min(small,prefix)
    return best


def convolution_checker(a,b):
    """Certify every coefficient via two exact NTTs and a strict integer uniqueness bound.

    Inputs and rounded candidates are nonnegative integers. The product of the two primes exceeds
    the common coefficient bound, so matching both residues certifies equality over the integers.
    This native reference and all validation run outside the reported NumPy stopwatch.
    """
    a=np.asarray(a);b=np.asarray(b)
    assert a.ndim==b.ndim==1 and len(a) and len(b)
    assert np.all(np.isfinite(a)) and np.all(np.isfinite(b))
    assert np.all(a==np.rint(a)) and np.all(b==np.rint(b)) and np.all(a>=0) and np.all(b>=0)
    n=1
    while n<len(a)+len(b)-1:n*=2
    bound=min(len(a),len(b))*int(a.max())*int(b.max());primes=[998244353,469762049]
    assert n<=2**23 and bound<math.prod(primes) and bound<2**53
    from .fft_certificate_source import SOURCE
    source_hash=hashlib.sha256(SOURCE.encode()).hexdigest()
    compiler=os.environ.get('CXX','c++');version=subprocess.check_output([compiler,'--version'],text=True).splitlines()[0]
    with tempfile.TemporaryDirectory(prefix='cs19-ntt-') as directory:
        directory=Path(directory);binary=directory/'reference';input_path=directory/'input.bin';output=directory/'output.bin'
        source=directory/'reference.cpp';source.write_text(SOURCE)
        subprocess.run([compiler,'-std=c++17','-O2',str(source),'-o',str(binary)],check=True,capture_output=True)
        with input_path.open('wb') as f:
            f.write(struct.pack('<QQQ',len(a),len(b),n));a.astype('<u4').tofile(f);b.astype('<u4').tofile(f)
        subprocess.run([str(binary),str(input_path),str(output)],check=True,capture_output=True)
        residues=np.fromfile(output,dtype='<u4');assert residues.size==2*n;residues=residues.reshape(2,n)
        reference_hash=hashlib.sha256(output.read_bytes()).hexdigest()
    def check(candidate):
        candidate=np.asarray(candidate);assert candidate.shape==(n,) and np.all(np.isfinite(candidate))
        assert np.all(candidate==np.rint(candidate)) and np.all(candidate>=0) and np.all(candidate<=bound)
        ints=candidate.astype(np.int64)
        for p,ref in zip(primes,residues):assert np.array_equal(ints%p,ref)
        assert np.all(ints[len(a)+len(b)-1:]==0)
    certificate=dict(coefficients=len(a)+len(b)-1,padded_length=n,primes=primes,coefficient_bound=bound,
                     modulus_product=math.prod(primes),source_sha256=source_hash,compiler=version,
                     residue_sha256=reference_hash,input_sha256=hashlib.sha256(a.astype('<u4').tobytes()+b.astype('<u4').tobytes()).hexdigest(),
                     method='all coefficients: exact independent two-prime NTT residues plus strict nonnegative uniqueness bound',
                     excluded_from_timing='native compilation/reference construction and complete candidate validation')
    return check,certificate
