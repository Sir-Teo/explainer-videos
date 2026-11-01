import ast,copy,difflib,hashlib,json
from pathlib import Path
import manim as m
R=Path('/workspace/explainer-videos');O=Path(__file__).parent;P=R/'videos/ai/ai5/s17_ito.py'
before=(O/'before.py').read_text();after=P.read_text();a,b=ast.parse(before),ast.parse(after)
changes=[]
for method in ast.walk(b):
 if isinstance(method,ast.FunctionDef) and method.name in ['integral','lemma']:
  calls=[n for n in ast.walk(method) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='step' and n.args and isinstance(n.args[0],ast.Constant) and n.args[0].value in [1,2]]
  assert len(calls)==2
  for n in calls:
   assert len(n.keywords)==1 and n.keywords[0].arg=='transform' and isinstance(n.keywords[0].value,ast.Constant) and n.keywords[0].value.value is False
   changes.append([method.name,n.args[0].value,n.lineno]);n.keywords=[]
assert len(changes)==4 and ast.dump(a)==ast.dump(b)
expr=lambda t,name:[ast.dump(n) for n in ast.walk(t) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr==name]
b2=ast.parse(after);assert expr(a,'voiceover')==expr(b2,'voiceover');assert expr(a,'play')==expr(b2,'play')
# Exercise the actual shared ladder AST and real Manim animation constructors,
# without any production scene, data loader, renderer or model import.
tree=ast.parse((R/'explainer/analysis/__init__.py').read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='ladder');namespace=vars(m).copy();namespace['changed_parts']=lambda *args:[]
exec(compile(ast.Module(body=[fn],type_ignores=[]),'actual-ladder-AST','exec'),namespace)
class Recorder:
 def __init__(self):self.calls=[]
 def play(self,*animations,run_time=1):self.calls.append({'types':[type(x).__name__ for x in animations],'run_time':run_time})
fixtures=[]
with m.tempconfig({'media_dir':str(O/'geometry-media'),'verbosity':'ERROR'}):
 for transform in [True,False]:
  rows=[m.MathTex('a','=','b'),m.MathTex('a','=','c')];whys=[m.Text('first'),m.Text('next')];s=Recorder();step=namespace['ladder'](s,rows,whys,highlight=False);step(0);step(1,transform=transform)
  fixtures.append({'transform':transform,'calls':s.calls,'sum_scheduled_seconds':sum(c['run_time'] for c in s.calls),'row_centers':[r.get_center().tolist() for r in rows]})
assert fixtures[0]['sum_scheduled_seconds']==fixtures[1]['sum_scheduled_seconds']
assert fixtures[0]['row_centers']==fixtures[1]['row_centers']
assert any('TransformMatchingTex' in x['types'] for x in fixtures[0]['calls'])
assert not any('TransformMatchingTex' in x['types'] for x in fixtures[1]['calls'])
assert sum('Write' in x['types'] for x in fixtures[1]['calls'])==2
sh=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(O/'after.py').write_text(after);(O/'source.patch').write_text(''.join(difflib.unified_diff(before.splitlines(keepends=True),after.splitlines(keepends=True),fromfile='before/s17_ito.py',tofile='after/s17_ito.py')))
receipt={'before_sha256':sh(O/'before.py'),'after_sha256':sh(P),'changes':changes,'whole_AST_identical_after_removing_four_transform_False_keywords':True,'all_voiceover_expressions_identical':True,'voiceover_expressions':len(expr(a,'voiceover')),'all_self_play_calls_and_arguments_identical':True,'self_play_calls':len(expr(a,'play')),'actual_shared_ladder_animation_constructor_fixture':fixtures,'same_scheduled_animation_time_and_final_row_centers_in_fixture':True,'limits':'AST/real-animation-constructor checks only; no production scene import/render/data load/producer. Fresh bilingual image/motion regression remains pending parent.'}
(O/'freeze.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
