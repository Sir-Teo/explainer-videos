"""Independent finite references and explicit measurement protocol for Part22."""
from __future__ import annotations
import hashlib,itertools,json,math,platform
from collections import Counter
from fractions import Fraction
import numpy as np


def protocol():
    return dict(timer='time.perf_counter',python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),scope='shared-host observations; construction, query work and model bounds are separate; no causal timing guarantee')


def digest(value):
    def normalize(v):
        if isinstance(v,np.ndarray):return dict(dtype=str(v.dtype),shape=list(v.shape),sha256=hashlib.sha256(v.tobytes()).hexdigest())
        if isinstance(v,np.generic):return v.item()
        if isinstance(v,dict):return {str(k):normalize(x)for k,x in sorted(v.items(),key=lambda kv:str(kv[0]))}
        if isinstance(v,(list,tuple)):return [normalize(x)for x in v]
        if isinstance(v,set):return sorted((normalize(x)for x in v),key=str)
        if hasattr(v,'__dict__'):return normalize(vars(v))
        return v
    return hashlib.sha256(json.dumps(normalize(value),sort_keys=True,ensure_ascii=False,allow_nan=False).encode()).hexdigest()


def hull_reference(points):
    P=sorted(set(tuple(int(x)if isinstance(x,(int,np.integer))else float(x)for x in p)for p in points))
    def turn(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    def chain(data):
        h=[]
        for p in data:
            while len(h)>1 and turn(h[-2],h[-1],p)<=0:h.pop()
            h.append(p)
        return h
    return P if len(P)<3 else chain(P)[:-1]+chain(P[::-1])[:-1]


def crossing_pairs(segments):
    """All strict crossings using four oriented sides, independently of the instrument's t/u divisions."""
    S=np.asarray(segments,dtype=float);n=len(S);result=[]
    if not n:return result
    c,d=S[:,0],S[:,1];edge=d-c
    cross=lambda x,y:x[...,0]*y[...,1]-x[...,1]*y[...,0]
    for i,(a,b)in enumerate(S):
        ab=b-a
        left=cross(ab,c-a);right=cross(ab,d-a)
        side_a=cross(edge,a-c);side_b=cross(edge,b-c)
        mask=(((left<0)&(right>0))|((left>0)&(right<0)))&(((side_a<0)&(side_b>0))|((side_a>0)&(side_b<0)))
        result.extend((i,int(j))for j in np.flatnonzero(mask)if j>i)
    return result


def triangulation_certificate(points,triangles,colours=None):
    """Integer area/edge/Euler certificate plus exact local empty-circle checks when appropriate."""
    P=[tuple(int(x)for x in p)for p in points];T=[tuple(map(int,t))for t in triangles];edges=Counter();total=0
    def area(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    for t in T:
        assert len(set(t))==3 and all(0<=i<len(P)for i in t)
        a,b,c=(P[i]for i in t);ar=area(a,b,c);assert ar!=0;total+=abs(ar)
        if colours is not None:assert len({colours[i]for i in t})==3
        for i,j in zip(t,t[1:]+t[:1]):edges[tuple(sorted((i,j)))]+=1
    assert all(v in (1,2)for v in edges.values())
    boundary=sum(v==1 for v in edges.values())
    return dict(area2=total,triangles=len(T),edges=len(edges),boundary=boundary)


def delaunay_certificate(points,triangles):
    P=[tuple(map(int,p))for p in points];cert=triangulation_certificate(P,triangles);h=hull_reference(P)
    area=abs(sum(a[0]*b[1]-a[1]*b[0]for a,b in zip(h,h[1:]+h[:1])))
    assert cert['area2']==area
    if not area:assert not triangles;return cert
    assert cert['triangles']==2*len(P)-2-cert['boundary']
    opposite={}
    for t in triangles:
        a,b,c=t
        for i,j,k in ((a,b,c),(b,c,a),(c,a,b)):opposite.setdefault(tuple(sorted((i,j))),[]).append(k)
    for (i,j),adj in opposite.items():
        if len(adj)!=2:continue
        k,l=adj;a,b,c,d=P[i],P[j],P[k],P[l]
        adx,ady=a[0]-d[0],a[1]-d[1];bdx,bdy=b[0]-d[0],b[1]-d[1];cdx,cdy=c[0]-d[0],c[1]-d[1]
        ar=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
        det=(adx*adx+ady*ady)*(bdx*cdy-bdy*cdx)-(bdx*bdx+bdy*bdy)*(adx*cdy-ady*cdx)+(cdx*cdx+cdy*cdy)*(adx*bdy-ady*bdx)
        assert det*ar<=0
    return cert


def circle_certificate(points,center,radius):
    """Numerical minimality certificate: containment and center in the hull of boundary support."""
    X=np.asarray(points,float);c=np.asarray(center,float);r=float(radius)
    if not len(X):assert r==0;return dict(points=0,support=0)
    distances=np.linalg.norm(X-c,axis=1);tol=1e-8*max(1.,r)
    assert np.all(distances<=r+tol)
    support=X[np.abs(distances-r)<=tol]
    if r<=tol:return dict(points=len(X),support=1)
    assert 2<=len(support)<=10
    for a,b in itertools.combinations(support,2):
        if np.linalg.norm((a+b)/2-c)<=tol:return dict(points=len(X),support=2)
    for a,b,d in itertools.combinations(support,3):
        A=np.vstack((np.array([a,b,d]).T,np.ones(3)));target=np.r_[c,1.]
        try:w=np.linalg.solve(A,target)
        except np.linalg.LinAlgError:continue
        if np.min(w)>=-1e-8 and np.linalg.norm(A@w-target)<=tol:return dict(points=len(X),support=3)
    raise AssertionError('center is outside the convex hull of boundary support')


def segment_interior_reference(a,b,polygon):
    """Exact binary64 rational half-plane intervals; boundary contact is allowed."""
    a=tuple(map(Fraction,a));b=tuple(map(Fraction,b));P=[tuple(map(Fraction,q))for q in polygon];low,high=Fraction(0),Fraction(1)
    for u,v in zip(P,P[1:]+P[:1]):
        edge=(v[0]-u[0],v[1]-u[1]);f=lambda q:edge[0]*(q[1]-u[1])-edge[1]*(q[0]-u[0]);s,t=f(a),f(b);delta=t-s
        if not delta:
            if s<=0:return False
        elif delta>0:low=max(low,-s/delta)
        else:high=min(high,-s/delta)
        if low>=high:return False
    return low<high


def path_certificate(path,polygons):
    assert path
    for a,b in zip(path,path[1:]):assert not any(segment_interior_reference(a,b,P)for P in polygons)
    return sum(math.dist(a,b)for a,b in zip(path,path[1:]))
