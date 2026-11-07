from pathlib import Path
import requests,hashlib,json,io,re,rdata
import numpy as np,pandas as pd
from scipy import stats
from explainer.stats import museum as M
out=Path('docs/qa/evidence/stats42-polish-20261107');out.mkdir(parents=True,exist_ok=True);results=[]
def get(url,name):
 r=requests.get(url,timeout=60);r.raise_for_status();p=Path('/tmp/stats42-'+name);p.write_bytes(r.content)
 return p,dict(source=url,sha256=hashlib.sha256(r.content).hexdigest())
def csv(package,name):
 p,meta=get(f'https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/{package}/{name}.csv',name+'.csv')
 return pd.read_csv(p,index_col=0),meta
r,meta=csv('datasets','faithful');np.testing.assert_array_equal(r.to_numpy(),np.column_stack(M.faithful()));results.append(dict(dataset='faithful',rows=len(r),exact=True,**meta))
r,meta=csv('datasets','airquality');a=M.airquality(False)
for col,key in [('Ozone','ozone'),('Solar.R','solar'),('Wind','wind'),('Temp','temp'),('Month','month'),('Day','day')]:np.testing.assert_allclose(r[col],a[key],rtol=0,atol=0,equal_nan=True)
results.append(dict(dataset='airquality',rows=len(r),columns=6,exact=True,analysis_scope='111 joint complete cases, not all 116 ozone-observed days',**meta))
r,meta=csv('MASS','newcomb');np.testing.assert_array_equal(np.sort(r.iloc[:,0]),np.sort(M.newcomb()));results.append(dict(dataset='Newcomb',rows=len(r),comparison='Identical multiset, different Museum ordering',**meta))
r,meta=csv('datasets','longley');X,y,names=M.longley();np.testing.assert_allclose(X[:,1:],r[['GNP.deflator','GNP','Unemployed','Armed.Forces','Population','Year']].to_numpy()*[1,1000,10,10,1000,1],rtol=0,atol=1e-8);np.testing.assert_allclose(y,r['Employed']*1000,rtol=0,atol=1e-8);results.append(dict(dataset='Longley',rows=len(r),comparison='Equivalent units to 1e-8 absolute; R columns multiplied by [1,1000,10,10,1000,1], employment by 1000',**meta))
r,meta=csv('MASS','gehan');g=M.gehan();actual=sorted(zip(g['time'],g['event'],g['group']));ref=sorted(zip(r['time'],r['cens'],(r['treat']=='6-MP').astype(int)));assert actual==ref;results.append(dict(dataset='Gehan',rows=len(r),exact_triples=True,scope='ordinary log-rank ignores original matching; no primary age claim',**meta))
p,meta=get('https://hastie.su.domains/ElemStatLearn/datasets/prostate.data','prostate.data');r=pd.read_csv(p,sep=r'\s+',index_col=0);X,y,tr,names=M.prostate();np.testing.assert_allclose(X,r[names],atol=5.1e-8,rtol=0);np.testing.assert_allclose(y,r['lpsa'],atol=5.1e-8,rtol=0);np.testing.assert_array_equal(tr,r['train']=='T');results.append(dict(dataset='Stamey prostate',rows=len(r),max_allowed_rounding_error=5.1e-8,**meta))
p,meta=get('https://raw.githubusercontent.com/stan-dev/example-models/master/misc/eight_schools/eight_schools.data.R','eight-schools.R');s=p.read_text();_,y,sd=M.eight_schools()
for key,expected in [('y',y),('sigma',sd)]:
 match=re.search(key+r'\s*<-\s*c\(([^)]+)\)',s);assert match,(key,s);np.testing.assert_array_equal(np.fromstring(match.group(1),sep=','),expected)
results.append(dict(dataset='eight schools',rows=8,exact=True,**meta))
p,meta=get('https://raw.githubusercontent.com/cran/sda/master/data/singh2002.rda','singh2002.rda');data=rdata.read_rda(p);print({k:getattr(v,'shape',None) for k,v in data.items()},flush=True)
# Re-derive the stored gene scores directly from the independent primary expression matrix.
X=np.asarray(data['singh2002']['x'],float);labels=np.asarray(data['singh2002']['y']);print('labels',np.unique(labels,return_counts=True),flush=True)
classes=np.unique(labels);healthy=X[labels=='healthy'];cancer=X[labels=='cancer']
t=stats.ttest_ind(cancer,healthy,axis=0,equal_var=True).statistic;z=stats.norm.ppf(stats.t.cdf(t,100));mt,mz=M.prostate_z();assert np.max(abs(t-mt))<1e-6;assert np.max(abs(z-mz))<1e-6
results.append(dict(dataset='Singh prostate microarray',samples=len(X),genes=X.shape[1],t_max_error=float(np.max(abs(t-mt))),z_max_error=float(np.max(abs(z-mz))),**meta))
(out/'source-data.json').write_text(json.dumps(dict(independent_datasets=results,not_independently_retrieved=['Bliss beetle observations: Museum and cited 1935 source; IRLS separately checked numerically']),indent=2)+'\n');print('Eight independent source datasets verified.',flush=True)
