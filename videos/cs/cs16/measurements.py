"""Checked, bounded measurements used by Counting Steps (CS16)."""
from __future__ import annotations
import json
import math
import platform
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def positive_seconds(value):
    value=float(value)
    if not math.isfinite(value) or value<=0:
        raise ValueError(f"Expected positive finite elapsed time, got {value!r}")
    return value


def uneven_recurrence(n):
    """Integer recurrence: T(n)=n for n<=2; otherwise split floor(n/3), n-floor(n/3)."""
    from functools import lru_cache
    @lru_cache(None)
    def cost(m):
        if m<=2:return m
        left=m//3
        return cost(left)+cost(m-left)+m
    if not isinstance(n,int) or n<0:raise ValueError('n must be a nonnegative integer')
    return cost(n)


def squaring_measurements():
    rows=[];x=3
    for k in range(1,22):
        samples=[]
        for _ in range(3):
            start=time.perf_counter_ns();y=x*x;samples.append(positive_seconds((time.perf_counter_ns()-start)/1e9))
        assert y==pow(3,1<<k)
        x=y;rows.append(dict(step=k,bits=x.bit_length(),seconds=min(samples),samples=samples))
    return dict(rows=rows,python=sys.version,executable=sys.executable,implementation=platform.python_implementation(),
                protocol='Minimum of three same-operand squarings at each step; positive perf_counter_ns elapsed times. Small operands are timer/interpreter-overhead dominated. Result exponent checked outside timed region.')


LINEAR_C=r'''
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>
#include <string.h>
#include <time.h>
static double now(void){struct timespec t;if(clock_gettime(CLOCK_MONOTONIC,&t))exit(3);return t.tv_sec+t.tv_nsec/1e9;}
static int cmp(const void*a,const void*b){uint32_t x=*(const uint32_t*)a,y=*(const uint32_t*)b;return(x>y)-(x<y);}
static uint64_t digest(const uint32_t*a,size_t n){uint64_t h=1469598103934665603ULL;for(size_t i=0;i<n;i++){h^=a[i];h*=1099511628211ULL;}return h;}
static int ordered(const uint32_t*a,size_t n){for(size_t i=1;i<n;i++)if(a[i-1]>a[i])return 0;return 1;}
static void radix(uint32_t*a,uint32_t*t,size_t n){
 for(int s=0;s<32;s+=8){size_t c[257]={0};
  for(size_t i=0;i<n;i++)c[((a[i]>>s)&255)+1]++;
  for(int k=0;k<256;k++)c[k+1]+=c[k];
  for(size_t i=0;i<n;i++)t[c[(a[i]>>s)&255]++]=a[i];
  memcpy(a,t,n*sizeof*a);
 }
}
static void counting(uint32_t*a,size_t n){
 size_t*c=calloc(65536,sizeof*c);if(!c)exit(3);
 for(size_t i=0;i<n;i++)c[a[i]]++;
 size_t o=0;for(uint32_t v=0;v<65536;v++)for(size_t j=0;j<c[v];j++)a[o++]=v;
 free(c);
}
int main(int argc,char**argv){
 if(argc!=2)return 2;char*end;unsigned long long arg=strtoull(argv[1],&end,10);
 if(*end||!arg||arg>10000000)return 2;size_t n=(size_t)arg,bytes=n*sizeof(uint32_t);
 uint32_t*a=malloc(bytes),*b=malloc(bytes),*t=malloc(bytes),*ref=malloc(bytes);if(!a||!b||!t||!ref)return 3;
 uint64_t s=88172645463325252ULL;
 for(size_t i=0;i<n;i++){s^=s<<13;s^=s>>7;s^=s<<17;a[i]=(uint32_t)s;}
 memcpy(ref,a,bytes);double t0=now();qsort(ref,n,sizeof*ref,cmp);double tq=now()-t0;
 if(!ordered(ref,n))return 4;uint64_t h32=digest(ref,n);
 memcpy(b,a,bytes);t0=now();radix(b,t,n);double tr=now()-t0;
 if(memcmp(ref,b,bytes)||!ordered(b,n))return 5;
 for(size_t i=0;i<n;i++)ref[i]=a[i]&65535;
 memcpy(b,ref,bytes);qsort(ref,n,sizeof*ref,cmp);
 t0=now();counting(b,n);double tc=now()-t0;
 if(memcmp(ref,b,bytes)||!ordered(b,n))return 6;
 printf("{\"qsort\":%.9g,\"radix\":%.9g,\"counting\":%.9g,\"hash32\":\"%016" PRIx64 "\",\"hash16\":\"%016" PRIx64 "\",\"exact_reference_matches\":true}\n",tq,tr,tc,h32,digest(b,n));
 free(a);free(b);free(t);free(ref);return 0;
}
'''

LINEAR_CPP=r'''
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cinttypes>
#include <cstdio>
#include <cstdlib>
#include <vector>
static int cmp(const void*a,const void*b){uint32_t x=*(const uint32_t*)a,y=*(const uint32_t*)b;return(x>y)-(x<y);}
int main(int argc,char**argv){
 if(argc!=2)return 2;char*end;unsigned long long arg=strtoull(argv[1],&end,10);
 if(*end||!arg||arg>10000000)return 2;size_t n=(size_t)arg;
 std::vector<uint32_t>a(n);uint64_t s=88172645463325252ULL;
 for(auto&x:a){s^=s<<13;s^=s>>7;s^=s<<17;x=(uint32_t)s;}
 auto ref=a;std::qsort(ref.data(),n,sizeof(uint32_t),cmp);
 auto t0=std::chrono::steady_clock::now();std::sort(a.begin(),a.end());
 double t=std::chrono::duration<double>(std::chrono::steady_clock::now()-t0).count();
 if(a!=ref||!std::is_sorted(a.begin(),a.end()))return 4;
 uint64_t h=1469598103934665603ULL;for(auto x:a){h^=x;h*=1099511628211ULL;}
 printf("{\"std_sort\":%.9g,\"hash32\":\"%016" PRIx64 "\",\"exact_reference_matches\":true}\n",t,h);
}
'''


def native_sort_measurements(sizes=(10**5,10**6,10**7),repeats=3,extra_flags=()):
    rows=[];runs=[]
    with tempfile.TemporaryDirectory() as directory:
        Path(directory,'l.c').write_text(LINEAR_C);Path(directory,'l.cpp').write_text(LINEAR_CPP)
        commands=[['gcc','-std=c11','-O2',*extra_flags,'-o','l','l.c'],['g++','-std=c++17','-O2',*extra_flags,'-o','lp','l.cpp']]
        for command in commands:subprocess.run(command,cwd=directory,check=True,capture_output=True,text=True)
        for n in sizes:
            best={}
            for repeat in range(repeats):
                c=json.loads(subprocess.run(['./l',str(n)],cwd=directory,capture_output=True,text=True,check=True).stdout)
                cpp=json.loads(subprocess.run(['./lp',str(n)],cwd=directory,capture_output=True,text=True,check=True).stdout)
                assert c['exact_reference_matches'] and cpp['exact_reference_matches'] and c['hash32']==cpp['hash32']
                cur={k:positive_seconds((cpp if k=='std_sort' else c)[k]) for k in ['qsort','radix','counting','std_sort']}
                best={k:min(best.get(k,float('inf')),v) for k,v in cur.items()}
                runs.append(dict(n=n,repeat=repeat,c=c,cpp=cpp))
            rows.append(dict(n=n,**best));print(rows[-1],flush=True)
    version=lambda cmd:subprocess.run([cmd,'--version'],capture_output=True,text=True,check=True).stdout.splitlines()[0]
    return dict(rows=rows,runs=runs,gcc=version('gcc'),gxx=version('g++'),commands=commands,
                protocol='Minimum of three runs per size; identical seeded uint32 source for qsort/std::sort/radix. Counting uses the source masked to 16 bits, a different domain. Input copies/reference checks excluded; counting allocates its count array inside the timed region. Every radix/counting/std::sort result matches an independently sorted full reference element-for-element; emitted hashes bind comparable 32-bit results. Single-host cache state and allocation effects remain.')
