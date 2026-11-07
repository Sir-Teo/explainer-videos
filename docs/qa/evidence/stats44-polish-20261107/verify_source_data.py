from pathlib import Path
import requests,hashlib,json,re,pandas as pd,numpy as np
from explainer.stats import museum as M
out=Path('docs/qa/evidence/stats44-polish-20261107');out.mkdir(parents=True,exist_ok=True);results=[]
url='https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/MASS/gehan.csv'
r=requests.get(url,timeout=60);r.raise_for_status();p=Path('/tmp/stats44-gehan.csv');p.write_bytes(r.content);ref=pd.read_csv(p,index_col=0);a=M.gehan()
assert sorted(zip(a['time'],a['event'],a['group']))==sorted(zip(ref['time'],ref['cens'],(ref['treat']=='6-MP').astype(int)))
results.append(dict(dataset='Gehan',rows=42,comparison='Exact event time, censoring and treatment triples; no age claim',source=url,sha256=hashlib.sha256(r.content).hexdigest()));print('Gehan all 42 triples verified.',flush=True)
url='https://lib.ru/LITRA/PUSHKIN/p4.txt'
r=requests.get(url,timeout=60);r.raise_for_status();r.encoding='cp1251';text=r.text;Path('/tmp/stats44-onegin-source.txt').write_text(text)
start=re.search(r'Мой\s+дядя\s+самых\s+честных\s+правил',text,re.I);assert start,'opening not found'
text=text[start.start():];letters=re.findall('[А-ЯЁа-яё]',text);letters=[x.upper() for x in letters if x.upper() not in 'ЬЪ'][:20000]
bits=np.array([int(x in 'АЕЁИОУЫЭЮЯЙ') for x in letters]);actual=M.onegin()
np.testing.assert_array_equal(bits,actual)
results.append(dict(dataset='Onegin vowel/consonant sequence',rows=20000,comparison='All first 20,000 bits agree after Cyrillic-only extraction, excluding hard/soft signs and counting short i as a vowel',source=url,sha256=hashlib.sha256(r.content).hexdigest()));print('Onegin all 20,000 bits verified.',flush=True)
(out/'source-data.json').write_text(json.dumps(results,indent=2)+'\n')
