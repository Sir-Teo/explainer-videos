"""Actual Manim chart objects from consumer AST; no scene or producer import."""
from pathlib import Path
import ast, json, sys, hashlib, os
import numpy as np
R=Path('/workspace/explainer-videos');D=Path('/workspace/runtime/ai6-gauss-hbars-repair');phase=sys.argv[1];case_lang=os.environ['EXPLAINER_LANG']
sys.path.insert(0,str(R))
from explainer.ai import *
from manim import tempconfig

def assigned(n,name):return isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets)
def function(path,name):return next(n for n in ast.walk(ast.parse(path.read_text())) if isinstance(n,ast.FunctionDef) and n.name==name)
def execute(nodes,scope):exec(compile(ast.fix_missing_locations(ast.Module(nodes,type_ignores=[])),str(D/'geometry.py'),'exec'),scope)
files=['videos/ai/ai6/common.py','videos/ai/ai6/s03_gauss.py','videos/ai/ai6/s17_metrics.py']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
paths={f:R/f for f in files}
if phase=='before':paths={f:D/'before'/f for f in files}
scope=dict(globals());scope.update(FIT=C.MODEL_Q,OLS=C.MODEL_Q,TS='#4FD1C5')
execute([function(paths[files[0]],'hbars')],scope)
if phase=='after' and case_lang=='zh':
 import explainer.zh_text as z
 table=json.loads((R/'videos/ai/ai_text_zh.json').read_text())
 overlay=json.loads((D/'caption-overlay.json').read_text())
 table.setdefault('strings',{}).update(overlay['strings']);z._TABLE=table

gm=json.loads((R/'.cache/ai6/gaussmarkov.json').read_text());c=json.loads((R/'.cache/ai6/calibration.json').read_text())
scope.update(G=gm['gauss'],H=gm['t3'],ts_g=gm['gauss']['ts']['var'],ts_h=gm['t3']['ts']['var'],c=c)
with tempconfig({'media_dir':str(D/'manim-geometry-cache'),'verbosity':'ERROR'}):
 sim=function(paths[files[1]],'simulate')
 execute([n for n in sim.body if any(assigned(n,k) for k in ['vb','vbh','vbox'])],scope)
 scores=function(paths[files[2]],'scores')
 for n in scores.body:
  if any(assigned(n,k) for k in ['specs','accs','loss_top','lls','ta','tl','gA','gL']):execute([n],scope)
  elif isinstance(n,ast.For) and isinstance(n.target,ast.Name) and n.target.id=='r_':execute([n],scope)
  elif isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and ast.unparse(n.value).startswith('tl.next_to('):execute([n],scope)
 charts={}
 values={'gauss-vb':[gm['gauss']['ols']['var'],gm['gauss']['ts']['var'],gm['t3']['ols']['var'],gm['t3']['ts']['var']],
  'metrics-accs':[c['acc'][k] for k,_,_ in scope['specs']], 'metrics-lls':[c[k]['logloss'] for k,_,_ in scope['specs']]}
 for key,var,group,width,lo,hi in [('gauss-vb','vb','vbox',3.4,0,.0125),('metrics-accs','accs','gA',3.6,.7,1),('metrics-lls','lls','gL',3.,0,scope['loss_top'])]:
  rows=[];g=scope[var]
  for i,row in enumerate(g):
   nm,b,v=row
   rows.append({'value':values[key][i],'bar_left':float(b.get_left()[0]),'bar_right':float(b.get_right()[0]),'width':float(b.width),'expected_width':max(width*(values[key][i]-lo)/(hi-lo),.02),'y':float(b.get_y()),'name_width':float(nm.width),'name_gap':float(b.get_left()[0]-nm.get_right()[0]),'value_gap':float(v.get_left()[0]-b.get_right()[0]),'name_text':getattr(nm,'tex_string',None),'value_text':getattr(v,'tex_string',None)})
  obj=scope[group];left=min(x['bar_left'] for x in rows);right=max(x['bar_left'] for x in rows)
  charts[key]={'rows':rows,'bar_origin_spread':right-left,'baseline':lo,'range_top':hi,'width':width,'group_bounds':[float(obj.get_left()[0]),float(obj.get_right()[0]),float(obj.get_bottom()[1]),float(obj.get_top()[1])]}
  if key=='metrics-accs':
   t=scope['ta'];charts[key]['heading']={'text':getattr(t,'tex_string',None),'bounds':[float(t.get_left()[0]),float(t.get_right()[0]),float(t.get_bottom()[1]),float(t.get_top()[1])]}
 result={'phase':phase,'lang':case_lang,'source':{f:sha(p) for f,p in paths.items()},'data':{str(p.relative_to(R)):sha(p) for p in [R/'.cache/ai6/gaussmarkov.json',R/'.cache/ai6/calibration.json']},'scope':'actual Manim objects from consumer AST, complete raw cached JSON; no scene import/render/producer','prospective_private_overlay':phase=='after' and case_lang=='zh','charts':charts}
 (D/f'{phase}-geometry-{case_lang}.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
 print(case_lang,phase,{k:round(v['bar_origin_spread'],9) for k,v in charts.items()},flush=True)
