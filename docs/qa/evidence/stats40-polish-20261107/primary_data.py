"""Compare Part 40 teaching data with independent upstream R objects."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[4]))
from pathlib import Path
import pickle,json,numpy as np,requests,rdata,hashlib
from explainer.stats import museum
refs={}
for name,url in {
 'gehan':'https://raw.githubusercontent.com/cran/MASS/master/data/gehan.rda',
 'cancer':'https://raw.githubusercontent.com/therneau/survival/master/data/cancer.rda',
 'heart':'https://raw.githubusercontent.com/therneau/survival/master/data/heart.rda',
}.items():
 r=requests.get(url,timeout=45);r.raise_for_status()
 p=Path('/tmp/stats40-primary-'+name+'.rda');p.write_bytes(r.content)
 refs[name]=(url,hashlib.sha256(r.content).hexdigest(),rdata.read_rda(p))
url='https://raw.githubusercontent.com/therneau/survival/master/data/pbc.rda'
r=requests.get(url,timeout=45);r.raise_for_status();p=Path('/tmp/stats40-pbc.rda');p.write_bytes(r.content);refs['pbc']=(url,hashlib.sha256(r.content).hexdigest(),rdata.read_rda(p))
results=[]
for name,container,key,actual in [('pbc','pbc','pbc',museum.pbc()),('stanford','heart','jasa1',museum.stanford_heart()),('mgus2','cancer','mgus2',museum.mgus2()),('veteran','cancer','veteran',museum.veteran()),('kidney','cancer','kidney',museum.kidney())]:
 url,h,data=refs[container];ref=data[key];errors={};cats=[]
 for k,a in actual.items():
  v=np.asarray(ref[k])
  if np.issubdtype(a.dtype,np.number):
   a=np.asarray(a,float);v=np.asarray(v,float);np.testing.assert_array_equal(np.isnan(a),np.isnan(v));diff=float(np.nanmax(np.abs(a-v)));assert diff<=5.00001e-6,(name,k,diff);errors[k]=diff
  else:
   np.testing.assert_array_equal(a.astype(str),v.astype(str));cats.append(k)
 results.append(dict(dataset=name,rows=len(ref),numeric_columns=errors,categorical_columns=cats,source=url,object=key,sha256=h))
url,h,data=refs['gehan'];ref=data['gehan'];a=museum.gehan()
ours=sorted(zip(a['time'],a['event'],a['group']))
theirs=sorted(zip(ref['time'],ref['cens'],(ref['treat']=='6-MP').astype(int)))
assert ours==theirs
results.append(dict(dataset='gehan',rows=42,comparison='All time/event/treatment triples exactly equal after sorting; pair IDs are not retained in the teaching table',source=url,sha256=h))
out=Path('docs/qa/evidence/stats40-polish-20261107');(out/'source-data.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
