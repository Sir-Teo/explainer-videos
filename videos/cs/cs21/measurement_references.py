"""Independent string references and explicit benchmark models for Part 21."""
from __future__ import annotations
import hashlib,platform,subprocess
from collections import Counter
from pathlib import Path
import numpy as np


def protocol():
    return dict(timer='time.perf_counter',python=platform.python_version(),platform=platform.platform(),numpy=np.__version__,scope='shared-host observations; timing minima and single observations are labeled; index build and query costs remain separate',validation='timed outputs checked after stopping the timer; expected references prepared outside timing')


def digest_bytes(data):
    return hashlib.sha256(data).hexdigest()


def find_all(text,pattern):
    if not pattern:
        return list(range(len(text)+1))
    result=[];start=0
    while True:
        at=text.find(pattern,start)
        if at < 0:return result
        result.append(at);start=at+1


def naive_comparisons_reference(text,pattern):
    alignments=max(0,len(text)-len(pattern)+1)
    if not pattern or not alignments:return 0
    return alignments+sum(len(find_all(text[:alignments+j-1],pattern[:j])) for j in range(1,len(pattern)))


def check_suffix_order(text,sa):
    """Complete O(n) certificate: permutation, ordered first bytes and ordered suffix tails."""
    sa=np.asarray(sa);n=len(text)
    assert sa.ndim==1 and len(sa)==n and sa.dtype.kind in 'iu'
    if not n:return
    assert sa.min()==0 and sa.max()==n-1
    inverse=np.full(n+1,-1,dtype=np.int64);inverse[sa]=np.arange(n);assert np.all(inverse[:n]>=0)
    a=np.frombuffer(text,dtype=np.uint8)[sa];tails=inverse[sa.astype(np.int64)+1]
    assert np.all((a[1:]>a[:-1])|((a[1:]==a[:-1])&(tails[1:]>tails[:-1])))


def longest_repeat_reference(text,sa):
    """Exact extension of all adjacent suffixes, one byte at a time; no residual is discarded."""
    t=np.frombuffer(text,dtype=np.uint8);sa=np.asarray(sa);alive=np.arange(1,len(sa),dtype=np.int64);length=0;last=np.empty(0,dtype=np.int64)
    while len(alive):
        x=sa[alive-1].astype(np.int64)+length;y=sa[alive].astype(np.int64)+length
        valid=(x<len(t))&(y<len(t));same=np.zeros(len(alive),dtype=bool);ix=np.flatnonzero(valid);same[ix]=t[x[ix]]==t[y[ix]];alive=alive[same]
        if len(alive):length+=1;last=alive
    at=[int(sa[last[0]-1]),int(sa[last[0]])] if len(last) else []
    return length,at


def lzw_decode_reference(codes):
    """Independent decoder including the special previous-phrase-plus-first-byte case."""
    if not codes:return b''
    dictionary={i:bytes([i]) for i in range(256)};assert codes[0] in dictionary
    previous=dictionary[codes[0]];out=bytearray(previous)
    for code in codes[1:]:
        assert code in dictionary or code==len(dictionary)
        value=dictionary[code] if code in dictionary else previous+previous[:1]
        out.extend(value);dictionary[len(dictionary)]=previous+value[:1];previous=value
    return bytes(out)


def history_snapshot(root,path):
    """Pin full object IDs and actual content; retain both chronological and reverse orders explicitly."""
    root=Path(root);revs=subprocess.check_output(['git','log','--format=%H','--',path],cwd=root,text=True).split()[::-1];rows=[]
    for rev in revs:
        raw=subprocess.check_output(['git','show',f'{rev}:{path}'],cwd=root)
        rows.append(dict(commit=rev,sha256=digest_bytes(raw),bytes=len(raw),raw=raw))
    return rows


def border_reference(pattern):
    return [max((k for k in range(j+1) if pattern[:k]==pattern[j+1-k:j+1]),default=0) for j in range(len(pattern))]


def alignment_reference(a,b,local=False):
    score=[[0]*(len(b)+1) for _ in range(len(a)+1)]
    gap=-2 if local else -1
    if not local:
        for i in range(len(a)+1):score[i][0]=-i
        score[0]=[-j for j in range(len(b)+1)]
    for i,x in enumerate(a,1):
        for j,y in enumerate(b,1):
            candidates=[score[i-1][j-1]+((2 if local else 1) if x==y else -1),score[i-1][j]+gap,score[i][j-1]+gap]
            score[i][j]=max([0]+candidates) if local else max(candidates)
    return score


def exact_chunk_reuse(old,old_cuts,new,new_cuts):
    def chunks(text,cuts):
        assert (not text and not cuts) or (cuts and cuts[-1]==len(text))
        return [text[a:b] for a,b in zip([0]+cuts,cuts)]
    originals=set(chunks(old,old_cuts))
    return [i for i,value in enumerate(chunks(new,new_cuts)) if value not in originals]


def huffman_cost_reference(frequencies):
    """Merge weights only; weighted external path length is the sum of merged weights."""
    import heapq
    heap=list(frequencies.values());heapq.heapify(heap)
    if len(heap)==1:return heap[0]
    total=0
    while len(heap)>1:
        merged=heapq.heappop(heap)+heapq.heappop(heap);total+=merged;heapq.heappush(heap,merged)
    return total
