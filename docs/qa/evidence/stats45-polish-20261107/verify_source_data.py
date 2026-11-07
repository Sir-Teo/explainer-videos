from pathlib import Path
import requests,pandas as pd,numpy as np,hashlib,json,re,subprocess
from explainer.stats import museum as M
out=Path('docs/qa/evidence/stats45-polish-20261107');out.mkdir(parents=True,exist_ok=True);results=[]
u='https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/pscl/EfronMorris.csv';r=requests.get(u,timeout=60);r.raise_for_status();p=Path('/tmp/stats45-EfronMorris.csv');p.write_bytes(r.content);d=pd.read_csv(p,index_col=0);names,hits,ab,average=M.efron_morris();assert list(d['name'])==names
np.testing.assert_array_equal(hits,d['r']);np.testing.assert_array_equal(ab,d['n']);np.testing.assert_allclose(average,d['p'],atol=0,rtol=0)
results.append(dict(dataset='Efron-Morris hitters',rows=18,comparison='All names, first-45 hits, rest-season at-bats and published three-decimal rest-season averages agree exactly',source=u,sha256=hashlib.sha256(r.content).hexdigest()));print('All 18 hitter records verified.',flush=True)
# The author's current PDF landing page redirects to this public download.
landing='https://hastie.su.domains/CASI_files/PDF/casi.pdf.download.html';r=requests.get(landing,timeout=60);r.raise_for_status();match=re.search(r"url='([^']+)'",r.text);assert match;u=match.group(1);r=requests.get(u,timeout=60);r.raise_for_status();assert r.content.startswith(b'%PDF')
p=Path('/tmp/stats45-casi.pdf');p.write_bytes(r.content);txt=Path('/tmp/stats45-casi.txt');subprocess.run(['pdftotext','-layout',str(p),str(txt)],check=True)
text=txt.read_text();start=text.index('Table 6.1 Counts');section=text[start:start+1800];line=next(line for line in section.splitlines() if 'Counts yx' in line and '7840' in line);counts=[int(x) for x in re.findall(r'\d+',line)];assert counts==M.INSURANCE_CLAIMS
results.append(dict(dataset='Automobile claim frequencies',policies=sum(counts),counts=counts,comparison='All eight frequency cells in Efron and Hastie Table 6.1 match exactly',source=landing,download=u,sha256=hashlib.sha256(r.content).hexdigest()));print('All eight claim-frequency cells verified against Table 6.1.',flush=True)
(out/'source-data.json').write_text(json.dumps(dict(independent_datasets=results,not_independently_retrieved=['Ruggles-Brodie historical production table: cited 1947 article; exact tank sampling formulas separately checked']),indent=2)+'\n')
