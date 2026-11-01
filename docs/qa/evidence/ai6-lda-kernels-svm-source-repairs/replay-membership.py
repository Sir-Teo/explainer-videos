"""Replay pinned LDA draw-membership AST with fake objects; no renderer/data."""
from pathlib import Path
import ast,copy,gzip,hashlib,json
D=Path(__file__).resolve().parent
rows=json.loads((D/'codec-map.json').read_text())
def source(name):
 r=next(r for r in rows if r['owner']=='LDA' and r['path']==name)
 b=gzip.decompress((D/r['object']).read_bytes())
 assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
 return ast.parse(gzip.decompress(b))
def wait(n,m):
 return isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=='wait_until' and n.value.args and isinstance(n.value.args[0],ast.Constant) and n.value.args[0].value==m
class State:
 def __init__(self):self.visible={'pl','pile_l','dl','sp1'};self.events=[];self.underlay=[]
 def record(self,kind):
  self.events.append(dict(event=kind,visible=sorted(self.visible)))
  if self.visible & {'swc','back'} and self.visible & {'pl','pile_l'}:self.underlay.append(len(self.events)-1)
 def remove(self,*xs):self.visible.difference_update(xs);self.record('remove')
 def add(self,*xs):self.visible.update(xs);self.record('add')
 def play(self,*actions,**kwargs):
  for kind,a,b in actions:
   if kind=='in':self.visible.add(a)
   if kind=='out':self.visible.discard(a)
   if kind=='replacement':self.visible.discard(a);self.visible.add(b)
  self.record('play')
def replay(tree):
 block=next(n for n in ast.walk(tree) if isinstance(n,ast.With) and any(wait(x,'w') for x in n.body))
 start=next(i for i,n in enumerate(block.body) if wait(n,'w'))
 end=next(i for i,n in enumerate(block.body[start:],start) if wait(n,'b'))
 s=State();vo=type('VO',(),{'wait_until':lambda self,m:s.record('cue:'+m)})()
 scope=dict(self=s,vo=vo,pl='pl',pile_l='pile_l',dl='dl',swc='swc',back='back',sp=[None,'sp1'],after='after',C=type('C',(),{'BITS':'bits'}),FadeIn=lambda a:('in',a,None),FadeOut=lambda a:('out',a,None),Transform=lambda a,b:('transform',a,b),ReplacementTransform=lambda a,b:('replacement',a,b),Indicate=lambda a,**kw:('indicate',a,None))
 exec(compile(ast.fix_missing_locations(ast.Module(body=copy.deepcopy(block.body[start:end]),type_ignores=[])),'pinned-LDA-inset-sequence','exec'),scope)
 assert s.visible=={'pl','pile_l','dl','sp1'}
 return s
old,new=replay(source('before.py.gz')),replay(source('after.py.gz'))
assert old.underlay and not new.underlay
print(json.dumps(dict(scope='Pinned source AST/fake draw-membership only; not a render/opacity/always_redraw simulation',before_underlay_events=old.underlay,after_underlay_events=new.underlay,restored_after_exit=True,after=new.events),indent=2))
