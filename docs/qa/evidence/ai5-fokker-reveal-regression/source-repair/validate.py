from pathlib import Path
import ast,json,hashlib,difflib
from manim import Succession,FadeOut,FadeIn,Dot,ValueTracker,AnimationGroup,linear
import numpy as np
O=Path(__file__).parent;before=ast.parse((O/'before.py').read_text());after=ast.parse((O/'after.py').read_text());dump=lambda x:ast.dump(x,include_attributes=False)
# Normalize only the six authorized kwargs and the one authorized caption grouping.
class Normalize(ast.NodeTransformer):
 def __init__(self):self.step_count=0;self.caption_count=0
 def visit_Call(self,node):
  node=self.generic_visit(node)
  if isinstance(node.func,ast.Name) and node.func.id=='step':
   kk=[k for k in node.keywords if k.arg=='transform'];
   if kk:assert len(kk)==1 and isinstance(kk[0].value,ast.Constant) and kk[0].value.value is False;node.keywords=[k for k in node.keywords if k.arg!='transform'];self.step_count+=1
  if isinstance(node.func,ast.Attribute) and node.func.attr=='play':
   result=[]
   for a in node.args:
    if isinstance(a,ast.Call) and isinstance(a.func,ast.Name) and a.func.id=='Succession':
     assert len(a.args)==2 and [x.func.id for x in a.args]==['FadeOut','FadeIn'];assert [x.args[0].id for x in a.args]==['cap','nxt'];assert all(len(x.keywords)==1 and x.keywords[0].arg=='run_time' and ast.literal_eval(x.keywords[0].value)==2.5 for x in a.args);assert len(a.keywords)==1 and a.keywords[0].arg=='run_time' and ast.literal_eval(a.keywords[0].value)==5.0
     for x in a.args:x.keywords=[]
     result.extend(a.args);self.caption_count+=1
    else:result.append(a)
   node.args=result
  return node
n=Normalize();normalized=n.visit(after);assert n.step_count==6 and n.caption_count==1;assert dump(before)==dump(normalized)
oldvo=[dump(x) for x in ast.walk(before) if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr=='voiceover'];newvo=[dump(x) for x in ast.walk(ast.parse((O/'after.py').read_text())) if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr=='voiceover'];assert oldvo==newvo
cap,nxt=Dot(),Dot();t=ValueTracker(0);field=Dot();fade=Succession(FadeOut(cap,run_time=2.5),FadeIn(nxt,run_time=2.5),run_time=5.0)
assert fade.run_time==5.0
schedule=[(float(r['start']),float(r['end'])) for r in fade.anims_with_timings];assert schedule==[(0.0,2.5),(2.5,5.0)]
# Exact scheduling and disjoint support under the preserved nonlinear outer progress.
alphas=np.linspace(0,1,1001);warped=1-(1-alphas)**2.2;simultaneous_visible=[]
for a in warped:
 clock=5*a;out=max(0,1-clock/2.5);incoming=max(0,min(1,(clock-2.5)/2.5));assert not(out>1e-12 and incoming>1e-12)
# Parent5s wrapper keeps tracker, field, and caption succession in one animated group.
g=AnimationGroup(t.animate.set_value(50).build(),field.animate.set_opacity(.15).build(),fade,run_time=5,rate_func=lambda a:1-(1-a)**2.2);assert g.run_time==5
result={'normalized_whole_ast_equal':True,'authorized_step_calls':n.step_count,'voiceover_expressions_identical':len(oldvo),'caption_group_run_time':fade.run_time,'actual_manim_caption_schedule':schedule,'outer_run_time':g.run_time,'nonoverlapping_caption_support_samples':len(alphas),'source_after_sha256':hashlib.sha256((O/'after.py').read_bytes()).hexdigest(),'limits':'Actual Manim constructors and schedule plus AST invariants; no fresh production visual approval, producer imports or data computation.'}
(O/'validation.json').write_text(json.dumps(result,indent=2)+'\n');(O/'source.patch').write_text(''.join(difflib.unified_diff((O/'before.py').read_text().splitlines(keepends=True),(O/'after.py').read_text().splitlines(keepends=True),fromfile='before/s19_fokker.py',tofile='after/s19_fokker.py')));print(json.dumps(result))
