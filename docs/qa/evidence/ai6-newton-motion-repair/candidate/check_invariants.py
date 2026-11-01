import ast,copy,json,hashlib,re,math
from pathlib import Path
import numpy as np
R=Path('/workspace/runtime/ai6-newton-motion-review/candidate');old=ast.parse((R/'s07_newton.before.py').read_text());new=ast.parse((R/'s07_newton.proposed.py').read_text());normalized=copy.deepcopy(new)
def meth(t,name):return next(n for n in ast.walk(t) if isinstance(n,ast.FunctionDef) and n.name==name)
def vo(t,name):return next(n.args[0] for n in ast.walk(meth(t,name)) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='voiceover')
# Revert exactly four approved append switches and the objective-only local changes.
flags=[]
for name in ('derive','digits'):
 for x in ast.walk(meth(normalized,name)):
  if isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='step' and x.keywords:
   assert [(k.arg,ast.literal_eval(k.value)) for k in x.keywords]==[('transform',False)];flags.append((name,ast.literal_eval(x.args[0])));x.keywords=[]
assert flags==[('derive',1),('derive',2),('derive',3),('digits',1)],flags
race=meth(normalized,'race');oldrace=meth(old,'race')
race.body=[n for n in race.body if not(isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ('penalty','system_size') for t in n.targets))]
for i,n in enumerate(race.body):
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='g70n' for t in n.targets):race.body[i]=copy.deepcopy(next(x for x in oldrace.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='g70n' for t in x.targets)))
for n in ast.walk(race):
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='voiceover':n.args[0]=copy.deepcopy(vo(old,'race'))
assert ast.dump(normalized,include_attributes=False)==ast.dump(old,include_attributes=False)
for name in ('construct','derive','digits','runaway'):
 assert ast.dump(vo(old,name),include_attributes=False)==ast.dump(vo(new,name),include_attributes=False) if name!='construct' else True
irpath=Path('/workspace/explainer-videos/.cache/ai6/irls.json');ir=json.loads(irpath.read_text());env={'nn':int(ir['n_newton']),'it6':int(ir['gd_iters_to']),'settle':3,'penalty':float(ir['l2']),'system_size':71};assert env['penalty']==.01
expr=vo(new,'race');en=eval(compile(ast.Expression(expr),'candidate-narration','eval'),{},env);before_en=eval(compile(ast.Expression(vo(old,'race')),'before-narration','eval'),{},env)
assert re.findall(r"<bookmark mark='(.*?)'/>",en)==re.findall(r"<bookmark mark='(.*?)'/>",before_en)==['a','b']
# Exercise actual translator parser/matcher on this private candidate expression and in-memory handoff.
from explainer.zh_templates import Translator,_parts,_NUMBER,numeric
proposal=json.loads((R/'caption-proposal.json').read_text());parts=_parts(expr);rx='';names=[]
for kind,value in parts:
 if kind=='text':rx+=r'\s*'.join(re.escape(w) for w in value.split(' '))
 else:rx+=_NUMBER if numeric(value) else '(.*?)';names.append(value)
t=Translator.__new__(Translator);t.zh={proposal['local_narration_key']:proposal['local_narration_proposal']};t.phrases={};t.tpls={ast.unparse(expr):(re.compile('^'+rx+'$',re.S),names)}
zh=t(en);assert zh is not None and not re.findall(r'\{[^{}]+\}',zh);assert re.findall(r"<bookmark mark='(.*?)'/>",zh)==['a','b'];assert '0.01' in zh and '1000' in zh and '71乘71' in zh
# Validate actual producer's objective expression in isolation, never execute its optimizer/loader.
core=ast.parse(Path('/workspace/explainer-videos/videos/ai/ai6/compute.py').read_text());logloss=next(n for n in core.body if isinstance(n,ast.FunctionDef) and n.name=='logloss');obj=next(n for n in ast.walk(meth(core,'newton_logreg')) if isinstance(n,ast.FunctionDef) and n.name=='obj');e={'np':np,'A':np.array([[1.,2.,1.],[-1.,.5,1.],[.2,-.3,1.]]),'y':np.array([1.,0.,1.]),'pen':np.array([.01,.01,0.])};exec(compile(ast.Module(body=[copy.deepcopy(logloss),copy.deepcopy(obj)],type_ignores=[]),'actual-objective-only','exec'),e)
for b in (-3.,0.,4.):
 theta=np.array([2.,-3.,b]);ce=e['logloss'](e['A']@theta,e['y']);assert math.isclose(e['obj'](theta)-ce,.5*.01*13,rel_tol=0,abs_tol=1e-14)
assert math.isclose(ir['newton_gap'][0]+ir['fstar'],math.log(2),abs_tol=1e-14)
with np.load('/workspace/explainer-videos/.cache/ai6/pages.npz',allow_pickle=False) as pages:
 actual_system_size=int(pages['X'].shape[1])+1
assert actual_system_size==env['system_size']==71
zh_old=ast.parse((R/'zh_lines.before.py').read_text());zh_new=ast.parse((R/'zh_lines.after.py').read_text())
def zdict(tree):return ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='ZH' for t in n.targets)))
a,b=zdict(zh_old),zdict(zh_new);changed=[k for k in a if a[k]!=b[k]];assert set(a)==set(b) and changed==[proposal['local_narration_key']]
assert b[changed[0]]==proposal['local_narration_proposal']
# Confirm actual frozen local table via actual translator; its templates scan AST only.
actual_translator=Translator('ai6');assert actual_translator(en)==zh
result={'status':'passed','actual_system_size_including_intercept':actual_system_size,'local_Chinese_changed_keys':changed,'approved_append_switches':flags,'all_other_AST_exact_after_removing_explicit_objective_caption_VO_and_cached_l2_read':True,'unpenalized_derivation_two_rate_replay_all_arrays_plot_vertices_digits_runaway_unchanged':True,'all_bookmarks_and_requested_play_wait_duration_expressions_unchanged':True,'race_VO_changed':True,'duration_equivalence':'NOT CLAIMED: new speech is longer; fresh EN/ZH captures/sidecars/timings required','synthetic_objective_checks':3,'producer_optimizer_or_default_data_load_executed':False,'cached_l2':ir['l2'],'cached_fstar':ir['fstar'],'cache_json_sha256':hashlib.sha256(irpath.read_bytes()).hexdigest(),'narration_lookup':{'en':en,'zh':zh,'new_source_template':ast.unparse(expr),'placeholders':names,'bookmarks':['a','b']},'before_sha256':hashlib.sha256((R/'s07_newton.before.py').read_bytes()).hexdigest(),'proposed_sha256':hashlib.sha256((R/'s07_newton.proposed.py').read_bytes()).hexdigest()}
(R/'invariants.json').write_text(json.dumps(result,indent=2,ensure_ascii=False));print(json.dumps({k:v for k,v in result.items() if k!='narration_lookup'}))
