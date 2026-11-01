from pathlib import Path
import os,sys,ast,json,hashlib
import numpy as np
R=Path('/workspace/explainer-videos');D=Path('/workspace/runtime/ai6-trees-margin-candidate');sys.path.insert(0,str(R))
from explainer.ai import *
from manim import tempconfig
LANG=os.environ['EXPLAINER_LANG'];assert LANG in ['en','zh'];assert os.environ['EXPLAINER_VIDEO']=='ai6'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def fn(t,n):return next(x for x in ast.walk(t) if isinstance(x,ast.FunctionDef) and x.name==n)
def execute(nodes,scope):exec(compile(ast.fix_missing_locations(ast.Module(nodes,type_ignores=[])),'exact-source-tree-margin-object-fixture','exec'),scope)
class SettledObjects:
 def play(self,*args,**kw):
  for a in args:
   if hasattr(a,'build'):a=a.build()
   a.begin();a.interpolate(1);a.finish()
def bounds(o):return [float(o.get_left()[0]),float(o.get_right()[0]),float(o.get_bottom()[1]),float(o.get_top()[1])]
def separated(a,b):return a[1]<b[0] or b[1]<a[0] or a[3]<b[2] or b[3]<a[2]
def coords(o):return o.get_all_points().copy()
raw=json.loads((D/'actual-trees.json').read_text());raw.update({k:v for k,v in np.load(D/'actual-trees.npz',allow_pickle=False).items()});common=ast.parse((D/'source-at-check/videos/ai/ai6/common.py').read_text());results={};objects={};px=854/float(config.frame_width);py=480/float(config.frame_height)
with tempconfig({'media_dir':str(D/'object-cache'),'verbosity':'ERROR'}):
 for phase in ['before','candidate']:
  src=D/(phase+'.py');tree=ast.parse(src.read_text());base=dict(globals(),t=raw,GINI=C.BITS,ENT=C.TRUE_P,ERRC=C.PENALTY,self=SettledObjects());execute([fn(common,'plot'),fn(common,'side_ladder')],base)
  # Actual fragile() construction through the first voiceover; t supplied raw, never load().
  frag=base.copy();nodes=[]
  for n in fn(tree,'fragile').body:
   if isinstance(n,ast.With):break
   if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='t' for x in n.targets):continue
   nodes.append(n)
  execute(nodes,frag)
  imp=base.copy();nodes=[]
  for n in fn(tree,'impurity').body:
   if isinstance(n,ast.With):break
   if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='t' for x in n.targets):continue
   nodes.append(n)
  execute(nodes,imp)
  for k in [0,1,2]:imp['step'](k)
  ib={k:bounds(imp[k]) for k in ['g','key','sc','scans','bl','res','flat']};ib['xlabel']=bounds(imp['sc'].xlabel);ib['ylabel']=bounds(imp['sc'].ylabel);ib['rows_whys']=bounds(VGroup(*imp['rows'],*imp['whys']))
  fb={k:bounds(frag[k]) for k in ['icons','counts','accl','head']}
  right=(config.frame_width/2-fb['accl'][1])*px;bottom=(ib['xlabel'][2]+config.frame_height/2)*py
  record={'source_sha256':sha(src),'fragile_bounds':fb,'impurity_bounds':ib,'accl_right_margin_854px':right,'gain_xlabel_bottom_margin_480px':bottom,'fragile_horizontal_icon_to_counts_gap_854px':(fb['counts'][0]-fb['icons'][1])*px,'fragile_horizontal_icon_to_accl_gap_854px':(fb['accl'][0]-fb['icons'][1])*px,'gain_to_upper_group_gap_480px':(min(ib['g'][2],ib['key'][2])-ib['sc'][3])*py,'gain_group_vs_readouts_separate':separated(ib['sc'],ib['res']) and separated(ib['sc'],ib['flat']),'gain_vs_upper_separate':separated(ib['sc'],ib['g']) and separated(ib['sc'],ib['key']),'accl_vs_icons_separate':separated(fb['accl'],fb['icons']),'counts_vs_icons_separate':separated(fb['counts'],fb['icons']),'actual_values':{'root_word_counts':{w:sum(r[0]==w for r in raw['boot_roots']) for w in frag['words']},'boot_count':len(raw['boot_roots']),'accuracy_min':float(np.min(raw['boot_acc'])),'accuracy_max':float(np.max(raw['boot_acc'])),'threshold_argmax':imp['best']}}
  if phase=='candidate':
   assert right>=15 and bottom>=15
   assert record['gain_group_vs_readouts_separate'] and record['gain_vs_upper_separate'] and record['accl_vs_icons_separate'] and record['counts_vs_icons_separate']
   assert min(fb['counts'][0],fb['accl'][0])>-config.frame_width/2 and max(fb['counts'][1],fb['accl'][1])<config.frame_width/2
  results[phase]=record;objects[phase]={'fragile':{k:coords(frag[k]) for k in ['icons','counts','accl','head']},'impurity':{k:coords(imp[k]) for k in ['g','key','sc','scans','bl','res','flat']} }
 for section in ['fragile','impurity']:
  for k,before in objects['before'][section].items():
   expected=np.array([-.3,0,0]) if k in ['counts','accl'] else np.array([0,.25,0]) if k in ['sc','scans','bl'] else np.zeros(3)
   delta=objects['candidate'][section][k]-before;assert delta.shape==before.shape and np.max(np.abs(delta-expected))<1e-12,(section,k)
 results['invariants']='Exact actual source AST-built Manim objects; onlycounts/accl translatedleft.3 and gainplot/scans/cut translatedup.25. Allotherfigurepoints/labels/data unchanged to1e−12; no source/producer/model imports/renders. Separate fresh interpreter language initialization.'
 results['lang']=LANG;results['raw_trees_json_sha256']=sha(D/'actual-trees.json');results['raw_trees_npz_sha256']=sha(D/'actual-trees.npz');results['global_caption_sha256']=sha(R/'videos/ai/ai_text_zh.json');results['pixels_per_world']={'x':px,'y':py}
 (D/f'geometry-{LANG}.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n');print(LANG,json.dumps({p:{k:r[k] for k in ['accl_right_margin_854px','gain_xlabel_bottom_margin_480px','fragile_horizontal_icon_to_counts_gap_854px','gain_to_upper_group_gap_480px']} for p,r in results.items() if p in ['before','candidate']}),flush=True)
