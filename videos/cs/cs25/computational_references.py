"""Retained proof objects and separate finite references for Part 25.

These checks establish the reported finite computations. Published theorems,
including full-plane aperiodicity and S(3)=21, remain explicit assumptions where
used. Nothing here upgrades a bounded unsuccessful search to a general decider.
"""
from __future__ import annotations

import collections
import gzip
import hashlib
import json
import math
import platform
import subprocess
from pathlib import Path

import numpy as np

ROOT = Path('.cache/cs25/artifacts')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def artifact(name, data):
    """Atomic replacement also breaks any historical evidence hard link."""
    if not isinstance(data, bytes): data = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode()
    path = ROOT / name; path.parent.mkdir(parents=True, exist_ok=True)
    if name.endswith('.gz'): data = gzip.compress(data, mtime=0)
    temp = path.with_suffix(path.suffix + '.tmp'); temp.write_bytes(data); temp.replace(path)
    return dict(path=str(path), sha256=digest(data), bytes=len(data))


def match(dominoes, seq, first=None):
    assert seq and all(type(i) is int and 0 <= i < len(dominoes) for i in seq)
    assert first is None or seq[0] == first
    top = ''.join(dominoes[i][0] for i in seq)
    bottom = ''.join(dominoes[i][1] for i in seq)
    assert top == bottom
    return dict(length=len(seq), bytes=len(top.encode()), sha256=digest(top.encode()))


def pcp_certificate(dominoes, seq, first=None):
    """Independent distance/closure certificate for a claimed shortest match.

    Residuals are represented as unequal string pairs, one side empty. All
    reachable states through depth L-1 are retained. The checker verifies their
    exact shortest distances and every outgoing edge below that depth; no
    equality may occur before L. A length-L witness supplies the upper bound.
    """
    witness = match(dominoes, seq, first)
    distances = {('', ''): 0}; frontier = {('', '')}
    for depth in range(1, len(seq)):
        new = set()
        for a, b in frontier:
            for i, (t, u) in enumerate(dominoes):
                if depth == 1 and first is not None and i != first: continue
                a1, b1 = a + t, b + u
                j = 0
                while j < min(len(a1), len(b1)) and a1[j] == b1[j]: j += 1
                a1, b1 = a1[j:], b1[j:]
                if a1 and b1: continue
                assert a1 or b1, 'shorter match found'
                if (a1, b1) not in distances: new.add((a1, b1))
        for state in new: distances[state] = depth
        frontier = new
    # Verify the entire finite proof, including completeness of each layer.
    for (a, b), d in list(distances.items()):
        if d >= len(seq) - 1: continue
        for i, (t, u) in enumerate(dominoes):
            if d == 0 and first is not None and i != first: continue
            x, y = a + t, b + u
            if x == y: raise AssertionError('shorter equality in certificate closure')
            if x.startswith(y): state = (x[len(y):], '')
            elif y.startswith(x): state = ('', y[len(x):])
            else: continue
            assert state in distances and distances[state] <= d + 1
    return dict(dominoes=dominoes, match=seq, first=first, witness=witness,
                shortest=len(seq), states=[[a, b, d] for (a, b), d in sorted(distances.items(), key=lambda kv:(kv[1],kv[0]))],
                proof='Every residual reachable at depth < L is present; every edge below L-1 is checked; no shorter equality; full length-L concatenation is equal.')


def grid(tiles, g, periodic=False):
    assert g and g[0] and all(len(r) == len(g[0]) for r in g)
    n, m = len(g), len(g[0])
    for r in range(n):
        for c in range(m):
            i = g[r][c]; assert type(i) is int and 0 <= i < len(tiles)
            if c + 1 < m or periodic: assert tiles[i][1] == tiles[g[r][(c+1)%m]][3]
            if r + 1 < n or periodic: assert tiles[i][2] == tiles[g[(r+1)%n][c]][0]
    return dict(rows=n, columns=m, periodic=periodic, all_edges_checked=True)


def tile_row_certificate(tiles, width):
    # Independent transcription: Jeandel/Rao Figure3 five-color T, N,E,S,W.
    published = [(1,1,1,3),(2,1,2,3),(1,3,3,3),(4,2,1,2),(2,2,0,2),
                 (0,0,1,0),(1,3,2,0),(2,0,2,1),(2,1,4,1),(3,3,2,1),(1,0,1,3)]
    assert set(published) == set(map(tuple, tiles))
    rows = []
    def visit(seq):
        if len(seq) == width:
            if published[seq[-1]][1] == published[seq[0]][3]: rows.append(tuple(seq))
            return
        for i, t in enumerate(published):
            if not seq or published[seq[-1]][1] == t[3]: visit(seq + [i])
    visit([])
    colors = sorted({t[j] for t in published for j in (1,3)})
    matrix = [[sum(t[3] == i and t[1] == j for t in published) for j in colors] for i in colors]
    power = [[int(i == j) for j in colors] for i in colors]
    for _ in range(width):
        power = [[sum(power[i][k]*matrix[k][j] for k in range(len(colors))) for j in range(len(colors))] for i in range(len(colors))]
    assert len(rows) == len(set(rows)) == sum(power[i][i] for i in range(len(colors)))
    edges = [(tuple(published[i][0] for i in row), tuple(published[i][2] for i in row)) for row in rows]
    vertices = {v for edge in edges for v in edge}
    succ = {v:set() for v in vertices}; indeg = {v:0 for v in vertices}
    for a, b in edges: succ[a].add(b)
    for bs in succ.values():
        for b in bs: indeg[b] += 1
    queue = collections.deque(sorted(v for v in vertices if not indeg[v])); order = []
    while queue:
        a = queue.popleft(); order.append(a)
        for b in sorted(succ[a]):
            indeg[b] -= 1
            if not indeg[b]: queue.append(b)
    assert len(order) == len(vertices)
    rank = {v:i for i, v in enumerate(order)}
    assert all(rank[a] < rank[b] for a, b in edges)
    return dict(width=width, tiles=published, rows=rows, row_count=len(rows), topological_order=order,
                matrix=matrix, excludes_all_positive_heights=True,
                scope='Finite widths only; not a computational proof of full-plane aperiodicity.')


def pell_certificate(D, x, y, certificate):
    assert type(D) is int and D > 0 and math.isqrt(D)**2 != D and x > 0 and y > 0
    m, d, a = 0, 1, math.isqrt(D)
    oldp, oldq, p, q = 1, 0, a, 1
    rows = certificate['convergents']
    for i, row in enumerate(rows):
        assert tuple(row) == (m,d,a,p,q)
        assert p*p-D*q*q != 1 or i == len(rows)-1
        if i + 1 < len(rows):
            m = d*a-m; assert (D-m*m) % d == 0
            d = (D-m*m)//d; a = (math.isqrt(D)+m)//d
            oldp,p = p,a*p+oldp; oldq,q = q,a*q+oldq
    assert (p,q) == (x,y) and x*x-D*y*y == 1
    return dict(convergents=len(rows), exact_identity=True,
                minimality='Least positive Pell solution is a sqrt(D) convergent; all earlier convergents checked.')


NATIVE_SOURCE = r'''
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
int main(int argc,char**argv){
 if(argc!=4) return 2;
 string mode=argv[1]; ifstream input(argv[2],ios::binary); ofstream output(argv[3],ios::binary);
 if(!input||!output)return 3;
 if(mode=="collatz"){
   uint32_t N;input>>N;
   for(uint32_t n=1;n<N;n++){
     uint64_t v=n,peak=n;uint32_t steps=0;
     while(v!=1){
       if(steps==10000000)throw runtime_error("budget");
       if(v&1){if(v>(UINT64_MAX-1)/3)throw runtime_error("overflow");v=3*v+1;}else v/=2;
       peak=max(peak,v);steps++;
     }
     output.write(reinterpret_cast<char*>(&steps),4);output.write(reinterpret_cast<char*>(&peak),8);
   }
   input>>ws;
   cout<<"all positive starts checked independently; uint64 overflow guarded\n";
 }else if(mode=="omega"){
   string s;int count=0;
   while(input>>s){
     string flat;for(char c:s)if(c!='_')flat+=c;
     if(flat.size()!=18)return 4;
     map<int,int> tape;int h=0,q=0,halt=0;
     for(int step=1;step<=21;step++){
       int k=6*q+3*tape[h];tape[h]=flat[k]-'0';h+=flat[k+1]=='R'?1:-1;
       if(flat[k+2]=='Z'){halt=step;break;}q=flat[k+2]-'A';
     }
     output<<halt<<'\n';count++;
   }
   cout<<count<<" independent two-sided tape simulations through S(3)=21\n";
 }else if(mode=="fractran"){
   const int primes[10]={2,3,5,7,11,13,17,19,23,29};
   const int num[14]={17,78,19,23,29,77,95,77,1,11,13,15,1,55};
   const int den[14]={91,85,51,38,33,29,23,19,17,13,11,2,7,1};
   int delta[14][10]={},need[14][10]={};
   for(int i=0;i<14;i++){
     int a=num[i],b=den[i];for(int j=0;j<10;j++){
       while(a%primes[j]==0){a/=primes[j];delta[i][j]++;}
       while(b%primes[j]==0){b/=primes[j];delta[i][j]--;need[i][j]++;}
     }if(a!=1||b!=1)return 5;
   }
   int e[10]={1};char recorded;uint64_t steps=0;
   while(input.get(recorded)){
     int chosen=-1;
     for(int i=0;i<14;i++){
       bool ok=true;for(int j=0;j<10;j++)if(e[j]<need[i][j])ok=false;
       if(ok){chosen=i;break;}
     }
     if(chosen<0||chosen!=static_cast<unsigned char>(recorded))return 6;
     for(int j=0;j<10;j++){e[j]+=delta[chosen][j];if(e[j]<0)return 7;}
     steps++;bool power=true;for(int j=1;j<10;j++)if(e[j])power=false;
     if(power)output<<steps<<' '<<e[0]<<'\n';
   }
   output<<"final";for(int j=0;j<10;j++)output<<' '<<e[j];output<<'\n';
   cout<<steps<<" first-applicable instructions checked by prime-exponent replay\n";
 }else return 8;
 if(!input.eof()||!output)return 9;
}
'''


def native(mode, data):
    """Retain exact compiler, source, image, full inputs/outputs and exit status."""
    ROOT.mkdir(parents=True, exist_ok=True)
    source = ROOT/'reference.cpp'; binary = ROOT/'reference'
    version = subprocess.run(['g++','--version'], check=True, capture_output=True, text=True).stdout
    flags = ['-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=all']
    source.write_text(NATIVE_SOURCE)
    build = subprocess.run(['g++',*flags,str(source),'-o',str(binary)], capture_output=True)
    assert build.returncode == 0, build.stderr
    inp = ROOT/f'{mode}.input'; inp.write_bytes(data)
    out = ROOT/f'{mode}.output'
    run = subprocess.run([str(binary),mode,str(inp),str(out)], capture_output=True)
    assert run.returncode == 0, (run.returncode,run.stderr)
    result = out.read_bytes()
    receipt = dict(mode=mode,compiler=version,flags=flags,host=platform.platform(),
                   build_exit=build.returncode,run_exit=run.returncode,stdout=run.stdout.decode(),stderr=run.stderr.decode(),
                   source=artifact('reference-source.cpp',NATIVE_SOURCE.encode()),
                   binary=artifact(f'{mode}-reference-image',binary.read_bytes()),input=artifact(f'{mode}-input.gz',data),
                   output=artifact(f'{mode}-output.gz',result))
    artifact(f'{mode}-native-receipt.json',receipt)
    return result, receipt


def wilson(k, n, z=1.959963984540054):
    p=k/n; denominator=1+z*z/n
    center=(p+z*z/(2*n))/denominator
    radius=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/denominator
    return [center-radius,center+radius]
