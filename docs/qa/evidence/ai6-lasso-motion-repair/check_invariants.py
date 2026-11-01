import ast,copy,hashlib,json
from pathlib import Path
R=Path('/workspace/runtime/ai6-lasso-motion-repair');a=ast.parse((R/'before.py').read_text());b=ast.parse((R/'after.py').read_text());n=copy.deepcopy(b)
def meth(t,name):return next(x for x in ast.walk(t) if isinstance(x,ast.FunctionDef) and x.name==name)
old_assign={x.targets[0].id:x for name in ['shapes','soft'] for x in meth(a,name).body if isinstance(x,ast.Assign) and isinstance(x.targets[0],ast.Name) and x.targets[0].id in ['zero','zl']}
counts={'caption_positions':0,'append_flags':0,'indicate_scale':0}
for name in ['shapes','soft']:
 f=meth(n,name)
 for i,x in enumerate(f.body):
  if isinstance(x,ast.Assign) and isinstance(x.targets[0],ast.Name) and x.targets[0].id in old_assign:
   f.body[i]=copy.deepcopy(old_assign[x.targets[0].id]);counts['caption_positions']+=1
 for x in ast.walk(f):
  if isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='step' and x.args and ast.literal_eval(x.args[0]) in [1,2]:
   assert [(k.arg,ast.literal_eval(k.value)) for k in x.keywords]==[('transform',False)];x.keywords=[];counts['append_flags']+=1
  if isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='Indicate':
   flags=[k for k in x.keywords if k.arg=='scale_factor'];assert len(flags)==1 and ast.literal_eval(flags[0].value)==1.;x.keywords=[k for k in x.keywords if k.arg!='scale_factor'];counts['indicate_scale']+=1
assert counts=={'caption_positions':2,'append_flags':2,'indicate_scale':1};assert ast.dump(n,include_attributes=False)==ast.dump(a,include_attributes=False)
strings=lambda t:[x.value for x in sorted((x for x in ast.walk(t) if isinstance(x,ast.Constant) and isinstance(x.value,str)),key=lambda x:(x.lineno,x.col_offset))]
assert strings(a)==strings(b)
laddertree=ast.parse(Path('/workspace/explainer-videos/explainer/analysis/__init__.py').read_text());ld=next(x for x in laddertree.body if isinstance(x,ast.FunctionDef) and x.name=='ladder');step=next(x for x in ast.walk(ld) if isinstance(x,ast.FunctionDef) and x.name=='step');assert ast.literal_eval(step.args.defaults[0])==1.2
branch=next(x for x in ast.walk(step) if isinstance(x,ast.If) and 'not transform' in ast.unparse(x.test));assert any(isinstance(x,ast.Call) and ast.unparse(x.func)=='Write' for x in ast.walk(branch));assert any(isinstance(x,ast.Call) and ast.unparse(x.func)=='scene.play' and 'run_time=run_time' in ast.unparse(x) for x in ast.walk(branch))
result={'status':'passed','allowed_five_changes':counts,'all_other_ast_exact':True,'all_strings_including_VO_bookmarks_and_caption_words_exact':True,'all_play_wait_duration_expressions_exact_except_approved_Indicate_keyword':True,'ladder_requested_duration':1.2,'ladder_write_branch_preserves_duration':True,'data_model_shared_changes':False,'before_sha256':hashlib.sha256((R/'before.py').read_bytes()).hexdigest(),'after_sha256':hashlib.sha256((R/'after.py').read_bytes()).hexdigest()};(R/'invariants.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
