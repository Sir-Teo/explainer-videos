from pathlib import Path
import ast,datetime,gzip,hashlib,json,re,types,functools
D=Path(__file__).parent; B=Path('/workspace/explainer-videos'); C=Path('/workspace/runtime/ai6-native1080-preparation/run-c80f10b4-remaining34'); reads=[]
def sig(p):
 p=Path(p);s=p.stat();return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=s.st_size,mtime_ns=s.st_mtime_ns)
def read(p):
 a=sig(p);v=Path(p).read_bytes();assert sig(p)==a;reads.append(a);return v

def dicts(src):
 out={}
 for n in ast.parse(src).body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
   try:out[n.targets[0].id]=ast.literal_eval(n.value)
   except (ValueError,TypeError):pass
  if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=='update' and isinstance(n.value.func.value,ast.Name):out[n.value.func.value.id].update(ast.literal_eval(n.value.args[0]))
 return out

def cap(src,table):
 nodes=[n for n in ast.parse(src).body if (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in {'_SPACE','_TEXT_CMD','_NUM'} for t in n.targets)) or (isinstance(n,ast.FunctionDef) and n.name in {'_by_numbers','translate'})]
 ns=dict(re=re,lang=types.SimpleNamespace(LANG='zh'),_TABLE=table,_BY_NUMBERS=None);exec(compile(ast.Module(nodes,type_ignores=[]),'<pure-caption-functions>','exec'),ns);return ns['translate']

def narration_translator(src,scene,table):
 ns=dict(ast=ast,re=re,lru_cache=functools.lru_cache);needed={'_source_body','source_startswith','_parts','_voiceover_args','_branches','numeric','Translator'}
 nodes=[n for n in ast.parse(src).body if (isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in needed) or (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in {'IS_TPL','_NUMBER'} for t in n.targets))]
 exec(compile(ast.Module(nodes,type_ignores=[]),'<pure-narration-functions>','exec'),ns)
 tree=ast.parse(scene);nodes=[n for n in ast.walk(tree) if isinstance(n,ast.JoinedStr)]
 for a in ns['_voiceover_args'](tree):nodes+=ns['_branches'](a)
 tpls={}
 for n in nodes:
  if not isinstance(n,(ast.JoinedStr,ast.BinOp)):continue
  rx='';names=[]
  for kind,v in ns['_parts'](n):
   if kind=='text':rx+=r'\s*'.join(re.escape(w) for w in v.split(' '))
   else:rx+=ns['_NUMBER'] if ns['numeric'](v) else '(.*?)';names.append(v)
  tpls[ast.unparse(n)]=(re.compile('^'+rx+'$',re.S),names)
 obj=ns['Translator'].__new__(ns['Translator']);obj.zh=table['ZH'];obj.phrases=table['PHRASES'];obj.tpls=tpls;return obj
bm=re.compile(r"<bookmark\s+mark\s*=\s*['\"]([^'\"]+)['\"]\s*/>")
def clean(s):
 s=' '.join(bm.sub('',s).split());return re.sub(r'(?<=[㐀-䶿一-鿿豈-﫿，。、；：？！“”（）《》]) | (?=[㐀-䶿一-鿿豈-﫿，。、；：？！“”（）《》])','',s)
nt=read(B/'videos/ai/ai_text_zh.json');nz=read(B/'videos/ai/ai6/zh_lines.py');cases=[]
for lang in ['en','zh']:
 c=C/(lang+'-GradientBoosting');receipt=json.loads(read(c/'receipt.json'));plan=json.loads(read(c/'plan.json'));scope=json.loads(read(c/'used-caption-narration-scope.json'));oldroot=c/'source-before'
 source=[]
 for row in receipt['source_before']:
  raw=read(row['copy']);assert hashlib.sha256(raw).hexdigest()==row['sha256'];now=read(row['source']);source.append(dict(path=str(Path(row['source']).relative_to(B)),captured_sha256=row['sha256'],current_sha256=hashlib.sha256(now).hexdigest(),exact=raw==now))
 scene=read(oldroot/'videos/ai/ai6/s16_gboost.py').decode();zt=read(oldroot/'explainer/zh_text.py').decode();zts=read(oldroot/'explainer/zh_templates.py').decode();ot=read(oldroot/'videos/ai/ai_text_zh.json');oz=read(oldroot/'videos/ai/ai6/zh_lines.py');on=json.loads(read(oldroot/'videos/ai/ai6/narration_zh.json'));nn=json.loads(read(B/'videos/ai/ai6/narration_zh.json'))
 tr0=cap(zt,json.loads(ot));tr1=cap(zt,json.loads(nt));rows=[json.loads(l) for l in read(c/'standard480-witness/text.jsonl').decode().splitlines() if l];strings=sorted({x['s'] for x in rows});outputs=[dict(input=s,historical=tr0(s),current=tr1(s),equal=tr0(s)==tr1(s)) for s in strings]
 otn=narration_translator(zts,scene,dicts(oz.decode()));ntn=narration_translator(zts,scene,dicts(nz.decode()));narr=[]
 for line in scope['actual_captured_narration']:
  raw=line['raw'];normalized=' '.join(raw.split());key=hashlib.sha1(normalized.encode()).hexdigest()[:12];a=on['lines'].get(key,{}).get('zh') or otn(normalized);b=nn['lines'].get(key,{}).get('zh') or ntn(normalized);assert a is not None and b is not None
  expected=clean(a) if lang=='zh' else ' '.join(bm.sub('',raw).split());narr.append(dict(key=key,raw=raw,captured_text=line['text'],historical_zh=a,current_zh=b,equal=a==b,captured_output_matches=expected==line['text']))
 inputs=[]
 for row in receipt['inputs']:
  now=sig(B/row['path']);inputs.append(dict(**row,actual_current=now,equal=now['sha256']==row['sha256'] and [now['bytes'],now['mtime_ns']]==row['captured_signature']))
 originals=[]
 for f in plan['frames']:
  a=sig(c/'native'/f['file']);assert a['sha256']==f['sha256'];originals.append(a)
 pages=[]
 for f in plan['pages']:
  a=sig(c/f['file']);assert a['sha256']==f['sha256'];pages.append(a)
 rawresult=json.loads(read(c/'native/result.json'));prior=json.loads(read(c/'standard480-witness/result.json'))
 cases.append(dict(case=lang+'/GradientBoosting',direct_source_and_helper_scope=source,captured_table_sha256=hashlib.sha256(ot).hexdigest(),current_table_sha256=hashlib.sha256(nt).hexdigest(),captured_local_zh_sha256=hashlib.sha256(oz).hexdigest(),current_local_zh_sha256=hashlib.sha256(nz).hexdigest(),caption_input_rows=len(rows),unique_inputs=len(strings),caption_outputs=outputs,caption_differences=[x for x in outputs if not x['equal']],narration=narr,narration_differences=[x for x in narr if not x['equal'] or not x['captured_output_matches']],inputs=inputs,originals=originals,pages=pages,native_raw_status=rawresult.get('status'),native_raw_warnings=rawresult.get('warnings'),native_raw_fingerprint=rawresult.get('fingerprint'),standard480_raw_status=prior.get('status'),standard480_raw_warnings=prior.get('warnings'),standard480_raw_fingerprint=prior.get('fingerprint'),native_caption_input_log_bytes=(c/'native/text.jsonl').stat().st_size,scope='Native caption input logs empty. Inputs are actual collected480witness strings under exact current scene/helper/data, with captured native displayed-text records and matching native/480 narration. Caption output comparison is scoped to those actual constructor inputs; not a fabricated native call log.'))
for row in reads:assert sig(row['path'])==row
out=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),no_scene_or_producer_or_model_import=True,pure_AST_translation_functions_only=True,cases=cases,reads_before_after=reads,scope='Current used-input caption/narration equivalence and exact direct source/helper/data checks. Raw warnings/fingerprints preserved; aggregate changed peer modules receive no blanket waiver. No render/decode/data recomputation.')
(D/'equivalence.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps([dict(case=c['case'],caption_rows=c['caption_input_rows'],unique=c['unique_inputs'],caption_differences=len(c['caption_differences']),narration_rows=len(c['narration']),narration_differences=len(c['narration_differences']),changed_sources=[x['path'] for x in c['direct_source_and_helper_scope'] if not x['exact']],data_exact=all(x['equal'] for x in c['inputs']),native_raw_warnings=c['native_raw_warnings'],standard480_raw_warnings=c['standard480_raw_warnings']) for c in cases],indent=2))
assert all(not c['caption_differences'] and not c['narration_differences'] and all(x['equal'] for x in c['inputs']) for c in cases)
