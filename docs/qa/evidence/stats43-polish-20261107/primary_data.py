from pathlib import Path
import requests,hashlib,json,pandas as pd,numpy as np
from explainer.stats import museum as M
out=Path('docs/qa/evidence/stats43-polish-20261107');out.mkdir(parents=True,exist_ok=True);results=[]
for package,name in [('datasets','EuStockMarkets'),('texmex','portpirie'),('vcd','HorseKicks')]:
 url=f'https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/{package}/{name}.csv';r=requests.get(url,timeout=60);r.raise_for_status();p=Path('/tmp/stats43-'+name+'.csv');p.write_bytes(r.content);ref=pd.read_csv(p,index_col=0);print(name,ref.shape,ref.columns.tolist(),flush=True)
 if name=='EuStockMarkets':
  a=M.eustock()
  for c in ['DAX','SMI','CAC','FTSE']:np.testing.assert_allclose(a[c],ref[c],atol=1e-12,rtol=0)
 if name=='portpirie':
  np.testing.assert_array_equal(np.asarray(M.PORTPIRIE_YEARS),ref.iloc[:,0]);np.testing.assert_allclose(M.PORTPIRIE,ref.iloc[:,1],atol=1e-12,rtol=0)
 if name=='HorseKicks':
  np.testing.assert_array_equal(M.HORSEKICK_K,ref.iloc[:,0]);np.testing.assert_array_equal(M.HORSEKICK_N,ref.iloc[:,1])
 results.append(dict(dataset=name,rows=len(ref),columns=len(ref.columns),comparison='All displayed data values agree to 1e-12 absolute or exactly for counts/years',source=url,sha256=hashlib.sha256(r.content).hexdigest()))
(out/'source-data.json').write_text(json.dumps(results,indent=2)+'\n');print('All three independent datasets verified.',flush=True)
