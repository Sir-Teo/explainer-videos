"""Execute actual AST-selected scene rotations with Manim objects; no scene/producer imports/render."""
import ast,math,json,hashlib
from pathlib import Path
import numpy as np
from manim import VGroup,Circle,Line,Square,Rotate,ApplyMatrix,ORIGIN,PI,Matrix,BackgroundRectangle,UR,DOWN
repo=Path('/workspace/explainer-videos');rt=Path('/workspace/runtime');results={}

def method(file,name):
 t=ast.parse((repo/'videos/ai/ai3'/file).read_text());c=next(n for n in t.body if isinstance(n,ast.ClassDef));return t,next(n for n in c.body if isinstance(n,ast.FunctionDef) and n.name==name)
def execute(nodes,env):exec(compile(ast.Module(body=nodes,type_ignores=[]),'actual-scene-ast','exec'),env)
def shape(pivot):return VGroup(Circle(radius=.7).shift(pivot),Line(pivot,pivot+[.42,0,0]),Line(pivot,pivot+[0,.42,0]))
def animate_checked(anim,g,M,pivot,rigid):
 old=g.get_all_points().copy();oldnorm=np.linalg.norm(old-pivot,axis=1);olddist=np.linalg.norm(old-old[0],axis=1);anim.begin();err=0.
 for alpha in np.linspace(0,1,41):
  anim.interpolate(float(alpha))
  if rigid:
   pts=g.get_all_points();err=max(err,float(np.max(np.abs(np.linalg.norm(pts-pivot,axis=1)-oldnorm))),float(np.max(np.abs(np.linalg.norm(pts-pts[0],axis=1)-olddist))))
   np.testing.assert_allclose(np.linalg.norm(pts-pivot,axis=1),oldnorm,atol=2e-12)
   np.testing.assert_allclose(np.linalg.norm(pts-pts[0],axis=1),olddist,atol=2e-12)
 anim.finish();target=old.copy();target[:,:2]=(old[:,:2]-pivot[:2])@M.T+pivot[:2];np.testing.assert_allclose(g.get_all_points(),target,atol=2e-12)
 return err

# SVD: actual A, svd2, loop branch and angle expression.
t,m=method('s08_svd.py','three_moves');env=dict(np=np,math=math)
execute([n for n in t.body if isinstance(n,ast.Assign) and any(isinstance(a,ast.Name) and a.id=='A' for a in n.targets) or isinstance(n,ast.FunctionDef) and n.name=='svd2'],env)
U,s,Vt=env['svd2'](env['A']);branch=next(n for n in ast.walk(m) if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='move')
g=shape(ORIGIN);orig=g.get_all_points().copy();stages=[]
for k,M in enumerate((Vt,np.diag(s),U)):
 e=dict(np=np,math=math,k=k,M=M,g=g,ORIGIN=ORIGIN,Rotate=Rotate,ApplyMatrix=ApplyMatrix);execute([branch],e);a=e['move'];assert isinstance(a,ApplyMatrix if k==1 else Rotate)
 if k!=1:
  np.testing.assert_allclose(M.T@M,np.eye(2),atol=1e-14);assert np.linalg.det(M)>0
  theta=math.atan2(M[1,0],M[0,0]);np.testing.assert_allclose([[math.cos(theta),-math.sin(theta)],[math.sin(theta),math.cos(theta)]],M,atol=1e-14)
 err=animate_checked(a,g,M,ORIGIN,k!=1);stages.append({'stage':k,'kind':type(a).__name__,'max_rigid_distance_error':err,'angle':float(math.atan2(M[1,0],M[0,0])) if k!=1 else None})
expected=orig.copy();expected[:,:2]=orig[:,:2]@env['A'].T;np.testing.assert_allclose(g.get_all_points(),expected,atol=2e-12);results['svd']={'actual_A':env['A'].tolist(),'stages':stages,'cumulative_endpoint_equals_A':True,'orthogonal_stages_41_actual_Manim_path_samples_each':True}

# Eigen: source S and diagonalization rotation helper, actual new branch.
t,m=method('s06_eigen.py','symmetric');common=ast.parse((repo/'videos/ai/ai3/common.py').read_text());e=dict(np=np,math=math,PI=PI);execute([next(n for n in common.body if isinstance(n,ast.FunctionDef) and n.name=='rot')],e)
for name in ('S','lam','Lm','Qr'):
 n=next(n for n in m.body if isinstance(n,ast.Assign) and (isinstance(n.targets[0],ast.Name) and n.targets[0].id==name or isinstance(n.targets[0],ast.Tuple) and name in [x.id for x in n.targets[0].elts]))
 execute([n],e)
branch=next(n for n in ast.walk(m) if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='move');g=shape(ORIGIN);orig=g.get_all_points().copy();stages=[]
for k,M in enumerate((e['Qr'],e['Lm'],e['Qr'].T)):
 q=dict(e,k=k,M=M,g=g,ORIGIN=ORIGIN,Rotate=Rotate,ApplyMatrix=ApplyMatrix);execute([branch],q);a=q['move'];assert isinstance(a,ApplyMatrix if k==1 else Rotate);stages.append({'stage':k,'kind':type(a).__name__,'max_rigid_distance_error':animate_checked(a,g,M,ORIGIN,k!=1)})
expected=orig.copy();expected[:,:2]=orig[:,:2]@e['S'].T;np.testing.assert_allclose(g.get_all_points(),expected,atol=2e-12);results['eigen']={'stages':stages,'cumulative_endpoint_equals_source_S':True}

# Matrices: both panels, actual branch on source quarter-turn identity and pivot.
t,m=method('s04_matrices.py','composition');e=dict(np=np);execute([n for n in m.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('R','S')],e);branch=next(n for n in ast.walk(m) if isinstance(n,ast.If) and ast.unparse(n.test)=='M is R');panels=[]
for j,(first,second) in enumerate(((e['R'],e['S']),(e['S'],e['R']))):
 c=np.array([-3.5+7*j,-.4,0]);g=VGroup(Square(side_length=2).move_to(c),*shape(c));old=g.get_all_points().copy();stages=[]
 for M in (first,second):
  q=dict(e,M=M,g=g,c=c,PI=PI,Rotate=Rotate,ApplyMatrix=ApplyMatrix,anims=[]);execute([branch],q);assert len(q['anims'])==2
  errs=[animate_checked(a,target,M,c,M is e['R']) for a,target in zip(q['anims'],(g[1:],g[0]))];stages.append({'kind':type(q['anims'][0]).__name__,'max_rigid_distance_error':max(errs)})
 expected=old.copy();expected[:,:2]=(old[:,:2]-c[:2])@(second@first).T+c[:2];np.testing.assert_allclose(g.get_all_points(),expected,atol=2e-12);panels.append({'pivot':c.tolist(),'stages':stages,'endpoint_equals_source_composition':True})
results['matrices']={'panels':panels,'determinant_formatter_unchanged':True,'negative_zero_observed_claim_retracted':True}

# Vectors: actual Matrix construction and local clamp only; never hit load().
t,m=method('s02_vectors.py','arrows');e=dict(np=np,v=np.array([3.,2.,0]),Matrix=Matrix,BackgroundRectangle=BackgroundRectangle,UR=UR,DOWN=DOWN,I_COLOR='#7CE38B',J_COLOR='#FF6B8B',BACKGROUND='#0B0F15');picked=[]
for n in m.body:
 if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='g':break
 if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('col','bg','three'):picked.append(n)
 elif isinstance(n,ast.Expr) and ast.unparse(n).startswith('col.get_entries'):picked.append(n)
 elif isinstance(n,ast.If):picked.append(n)
execute(picked,e);assert e['three'].get_top()[1]<=3.7+1e-12
results['vectors']={'three_column_top':float(e['three'].get_top()[1]),'minimum_top_margin':float(4-e['three'].get_top()[1]),'actual_AST_Matrix_and_clamp_executed':True}
results['source_hashes']={f:hashlib.sha256((repo/'videos/ai/ai3'/f).read_bytes()).hexdigest() for f in ('s02_vectors.py','s04_matrices.py','s06_eigen.py','s07_power.py','s08_svd.py')};results['limits']=['No production scene or producer imports/loaders/rendering/model/data computation.','Fixtures establish geometric path/endpoints, not actual repaired movie appearance.']
(rt/'ai3-head-motion-invariants.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
