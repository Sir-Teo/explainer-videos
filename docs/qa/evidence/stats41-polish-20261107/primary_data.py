"""Verify Part 41 teaching data against upstream sources and the original CDC files."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[4]))
from pathlib import Path
import requests,rdata,hashlib,json,pandas as pd,numpy as np,subprocess,sys
from explainer.stats import museum
out=Path('docs/qa/evidence/stats41-polish-20261107');results=[]
url='https://raw.githubusercontent.com/cran/sampleSelection/master/data/Mroz87.txt.gz'
response=requests.get(url,timeout=45);response.raise_for_status();p=Path('/tmp/stats41-mroz.txt.gz');p.write_bytes(response.content)
ref=pd.read_csv(p,sep=r'\s+',index_col=0);actual=museum._table('mroz87.csv');errors={}
for k,a in actual.items():
 rv=np.asarray(ref[k],float);np.testing.assert_array_equal(np.isnan(a),np.isnan(rv));err=float(np.nanmax(np.abs(rv-a)));assert err<5e-6,(k,err);errors[k]=err
results.append(dict(dataset='Mroz87',rows=len(ref),source=url,sha256=hashlib.sha256(response.content).hexdigest(),errors_by_column=errors))
url='https://vincentarelbundock.github.io/Rdatasets/csv/datasets/airquality.csv'
response=requests.get(url,timeout=45);response.raise_for_status();p=Path('/tmp/stats41-airquality.csv');p.write_bytes(response.content);ref=pd.read_csv(p);a=museum.airquality(complete=False);errors={}
for k,rk in [('ozone','Ozone'),('solar','Solar.R'),('wind','Wind'),('temp','Temp'),('month','Month'),('day','Day')]:
 av=np.asarray(a[k],float);rv=np.asarray(ref[rk],float);np.testing.assert_array_equal(np.isnan(av),np.isnan(rv));errors[k]=float(np.nanmax(np.abs(av-rv)));assert errors[k]<1e-10
results.append(dict(dataset='airquality',rows=len(ref),source=url,sha256=hashlib.sha256(response.content).hexdigest(),errors_by_column=errors))
provenance=json.loads(Path('docs/qa/evidence/stats20-polish-20261107/source-provenance.json').read_text())
for name,meta in provenance['sources'].items():
 if name.endswith('.xpt'):
  p=Path('/tmp/stats20-nhanes')/name
  if not p.exists():
   response=requests.get(meta['url'],timeout=90);response.raise_for_status();p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(response.content)
  assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256'],p
subprocess.run([sys.executable,'tools/nhanes_extract.py','/tmp/stats20-nhanes','/tmp/stats41-nhanes-verified.csv'],check=True)
assert Path('/tmp/stats41-nhanes-verified.csv').read_bytes()==Path('explainer/stats/data/nhanes_bp.csv').read_bytes()
results.append(dict(dataset='NHANES 2017-2018 examined adults',rows=5533,columns=29,comparison='Byte-for-byte reconstruction from six independently downloaded, SHA-256 checked CDC XPTs',prior_source_provenance='docs/qa/evidence/stats20-polish-20261107/source-provenance.json',sources=provenance['sources']))
(out/'source-data.json').write_text(json.dumps(results,indent=2)+'\n');print('All three source datasets verified.',flush=True)
