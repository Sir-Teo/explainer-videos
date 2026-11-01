import ast,copy,gzip,hashlib,json,math,sys,unittest
from pathlib import Path
from types import SimpleNamespace
import numpy as np
R=Path(__file__).resolve().parents[1];D=R/'docs/qa/evidence/ai1-arithmetic-narrated-timing-repair'
sys.path.insert(0,str(R/'tests'))
from test_ai1_entropy_prefix_timing import actual_tracker,compile_nodes,function,Shape,Clock,tag
DIAG=D/'exact-diagnostic.json.gz'
def diagnostic():return json.loads(gzip.decompress(DIAG.read_bytes()))
def tree(before=False):return ast.parse(gzip.decompress((D/'source-before.py.gz').read_bytes()) if before else (R/'videos/ai/ai1/s09_arithmetic.py').read_bytes())
class M(Shape):
 def __init__(self,name):super().__init__(name);self.tex_string=name
 def __getitem__(self,key):return M(self.name+'-'+str(key))
 def shift(self,*a,**kw):return self
 def move_to(self,*a,**kw):return self
 def set_value(self,v):return self
class CClock(Clock):
 def __init__(self,fps,rounded=True):super().__init__(fps,rounded);self.completed={}
def run(fps=60,phase=0.,before=False,rounded=True,defaults=False):
 d=diagnostic();b=d['narration_blocks'][3];occ=d['exact_narration_occurrences'][3];a=d['per_utterance_word_alignment_and_duration'][occ['key']]
 s=CClock(fps,rounded);vo=actual_tracker(b,occ,a,s)
 ns=dict(self=s,vo=vo,config=SimpleNamespace(frame_rate=fps),shown=[],lines=None,y_top=2.35,dy=1.05,ctx_x=-5.95,read_x=3.55,
         steps=[{'context':'context'+str(k),'symbol':'the falcon'[k],'p':.2}for k in range(10)],widths=[2.**(-k-1)for k in range(10)],
         lad=SimpleNamespace(row=lambda k,y:M('row'+str(k)),funnel=lambda k,a,b:M('funnel'+str(k))),
         tot=M('total'),tt=lambda s:s,label=lambda s,**kw:M('label'+s),mtex=lambda s,**kw:M('math'+s),
         bin_lines=lambda k:M('binary'+str(k)),C=SimpleNamespace(CONTEXT='context',INTERVAL='interval'),
         UP=np.array([0.,1.,0.]),LEFT='left',math=math)
 for name in ['FadeOut','FadeIn','Create','Transform']:
  ns[name]=lambda *args,_name=name,**kw:(_name,tag(args),tag(kw))
 tr=tree(before);encode=function(tr,'encode');add=function(encode,'add_row');helpers=[n for n in tr.body if isinstance(n,ast.FunctionDef)and n.name=='_row_run_times']
 factory=ast.FunctionDef(name='_bind_add_row',args=ast.arguments(posonlyargs=[],args=[],kwonlyargs=[],kw_defaults=[],defaults=[]),body=[ast.Assign(targets=[ast.Name(id='lines',ctx=ast.Store())],value=ast.Constant(None)),copy.deepcopy(add),ast.Return(value=ast.Name(id='add_row',ctx=ast.Load()))],decorator_list=[])
 compile_nodes(helpers+[factory],ns,'actual-Arithmetic-nested-add_row')
 actual=ns['_bind_add_row']();actual(0,run_time=1.6)
 initial_requests=[e['requested']for e in s.events]
 s.renderer.time=phase/fps;s.events=[]
 def traced(k,**kw):
  result=actual(k,**kw);s.completed[k]=s.renderer.time;return result
 ns['add_row']=traced
 if defaults:
  for k in range(1,10):traced(k)
  return s,vo,ns,initial_requests
 blocks=[n for n in encode.body if isinstance(n,ast.With)];body=blocks[1].body
 def iswait(n,mark):return isinstance(n,ast.Expr)and isinstance(n.value,ast.Call)and isinstance(n.value.func,ast.Attribute)and n.value.func.attr=='wait_until'and n.value.args[0].value==mark
 ia=next(i for i,n in enumerate(body)if iswait(n,'a'));ib=next(i for i,n in enumerate(body)if iswait(n,'b'))
 compile_nodes(body[:ia],ns,'actual-first-row-loop')
 ns['first_completion']=s.renderer.time;ns['first_event_count']=len(s.events)
 compile_nodes(body[ia:ib],ns,'actual-second-row-loop')
 return s,vo,ns,initial_requests

def holds(scene):
 end=diagnostic()['narration_blocks'][3]['duration'];removed={}
 for e in scene.events:
  for a in e['args']:
   if isinstance(a,tuple)and a[0]=='FadeOut'and a[1]and isinstance(a[1][0],str)and a[1][0].startswith('row')and a[1][0][3:].isdigit():removed[int(a[1][0][3:])]=e['start']
 return {k:removed.get(k,end)-v for k,v in scene.completed.items()}

class Timing(unittest.TestCase):
 def test_exact_diagnostic_and_all_actual_tracker_targets(self):
  raw=gzip.decompress(DIAG.read_bytes());self.assertEqual((len(raw),hashlib.sha256(raw).hexdigest()),(152277,'ffbf5a0de4593a85c2ea734d62b69cf1de835a33acce1d4b5291dce62762fec5'))
  d=json.loads(raw);self.assertEqual(hashlib.sha256(gzip.decompress((D/'source-before.py.gz').read_bytes())).hexdigest(),d['source_sha256'])
  by={}
  for b,o in zip(d['narration_blocks'],d['exact_narration_occurrences']):
   a=d['per_utterance_word_alignment_and_duration'][o['key']];v=actual_tracker(b,o,a,CClock(60));by[round(b['start'],8)]=(b,v)
  self.assertEqual(len(by),10);self.assertEqual(len(d['all_bookmark_requests']),24)
  for q in d['all_bookmark_requests']:
   b,v=by[round(q['block_start'],8)];self.assertAlmostEqual(b['start']+v.mark_time(q['mark']),q['target_seconds'])
  self.assertEqual([x['key']for x in d['speech_masters']],[x['key']for x in d['exact_narration_occurrences']])
 def test_actual_original_nested_function_reproduces_point17_overrun(self):
  s,v,n,_=run(100,before=True,rounded=False);self.assertAlmostEqual(n['first_completion'],7.)
  self.assertAlmostEqual(s.renderer.time-v.mark_time('b'),.17,places=10)
  self.assertEqual([e['requested']for e in s.events[n['first_event_count']:]],([.5,.6,.6]*4))
 def test_both_real_loops_frame_reserved_and_same_animation_arguments(self):
  for fps in [15,30,60]:
   for phase in [0.,.49,1.]:
    with self.subTest(fps=fps,phase=phase):
     s,v,n,_=run(fps,phase);old,_,_,_=run(fps,phase,before=True)
     self.assertLessEqual(n['first_completion'],v.mark_time('a')-1/fps+1e-10)
     self.assertLessEqual(s.renderer.time,v.mark_time('b')-1/fps+1e-10)
     self.assertEqual(len(s.completed),9)
     self.assertEqual([e['args']for e in s.events],[e['args']for e in old.events])
     self.assertEqual([e['kwargs']for e in s.events],[e['kwargs']for e in old.events])
     self.assertTrue(all(e['requested']>=1/fps for e in s.events))
 def test_every_revealed_row_has_settled_source_clock_reading_hold(self):
  for fps in [15,30,60]:
   for phase in [0.,.49,1.]:
    s,v,n,_=run(fps,phase);h=holds(s)
    self.assertEqual(set(h),set(range(1,10)));self.assertGreaterEqual(min(h.values()),1.5)
    self.assertGreaterEqual(diagnostic()['narration_blocks'][3]['duration']-s.renderer.time,1.5)
 def test_other_add_row_calls_and_impossible_budgets_keep_honest_contract(self):
  for fps in [15,30,60]:
   a,_,_,init=run(fps,defaults=True);b,_,_,oldinit=run(fps,before=True,defaults=True)
   self.assertEqual(init,oldinit);self.assertEqual([e['requested']for e in a.events],[e['requested']for e in b.events])
   helper=function(tree(),'_row_run_times');ns=compile_nodes([helper],dict(config=SimpleNamespace(frame_rate=fps)),'actual-cue-row-budget')
   good=SimpleNamespace(mark_time=lambda _:100.,elapsed=lambda:0.);miss=SimpleNamespace(mark_time=lambda _:0.,elapsed=lambda:1.)
   self.assertEqual(ns['_row_run_times'](good,'a',5,1),(1.,.5))
   row,scroll=ns['_row_run_times'](miss,'a',5,1);self.assertAlmostEqual(.6*row,1/fps);self.assertAlmostEqual(scroll,1/fps)
 def test_entire_module_AST_is_exact_except_local_timing(self):
  class Reverse(ast.NodeTransformer):
   def visit_FunctionDef(self,n):
    if n.name=='_row_run_times':return None
    if n.name=='add_row':n.args.args.pop();n.args.defaults.pop()
    return self.generic_visit(n)
   def visit_Assign(self,n):return None if any(isinstance(t,ast.Name)and t.id=='row_times'for t in n.targets)else self.generic_visit(n)
   def visit_Call(self,n):
    if isinstance(n.func,ast.Attribute)and n.func.attr=='play':
     for k in n.keywords:
      if k.arg=='run_time'and isinstance(k.value,ast.Name)and k.value.id=='scroll_time':k.value=ast.Constant(.5)
    if isinstance(n.func,ast.Name)and n.func.id=='add_row':
     n.keywords=[k for k in n.keywords if k.arg!='scroll_time']
     for k in n.keywords:
      if k.arg=='run_time'and isinstance(k.value,ast.Subscript):k.value=ast.Constant(1.)
    return self.generic_visit(n)
  self.assertEqual(ast.dump(Reverse().visit(copy.deepcopy(tree())),include_attributes=False),ast.dump(tree(True),include_attributes=False))

if __name__=='__main__':unittest.main()
