import ast,copy,json,hashlib,types,os
from pathlib import Path
import numpy as np
from explainer.ai import *
R=Path('/workspace/runtime/ai6-lasso-motion-repair');config.media_dir=str(R/'fixture-media'/os.environ.get('EXPLAINER_LANG','en'));config.tex_dir=str(Path(config.media_dir)/'Tex')
before=ast.parse((R/'before.py').read_text());after=ast.parse((R/'after.py').read_text())
def method(tree,name):return next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name==name)
def compile_block(nodes,env):exec(compile(ast.fix_missing_locations(ast.Module(body=copy.deepcopy(nodes),type_ignores=[])),'isolated-geometry','exec'),env)
def build(tree):
 env=globals().copy()
 nodes=[n for n in tree.body if isinstance(n,(ast.Assign,ast.FunctionDef))]
 compile_block(nodes,env)
 panel=copy.deepcopy(method(tree,'panel'));compile_block([panel],env)
 self=types.SimpleNamespace();self.panel=types.MethodType(env['panel'],self);env['self']=self
 sh=method(tree,'shapes');compile_block(sh.body[:next(i for i,n in enumerate(sh.body) if isinstance(n,ast.With))],env)
 env['R'][3].set_value(.9);env['R'][5].update()
 # AST extract only local plot/annotation constructors; never import scene/common/producer/load.
 common=ast.parse(Path('/workspace/explainer-videos/videos/ai/ai6/common.py').read_text());compile_block([next(n for n in common.body if isinstance(n,ast.FunctionDef) and n.name=='plot')],env)
 soft=method(tree,'soft');names={'g','ax','lam','ident','st','zone','zl'}
 compile_block([n for n in soft.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in names for t in n.targets)],env)
 return env
def box(m):return [float(m.get_left()[0]),float(m.get_right()[0]),float(m.get_bottom()[1]),float(m.get_top()[1])]
def segment_hits_box(a,b,bounds,pad=.025):
 lo=np.array([bounds[0]-pad,bounds[2]-pad]);hi=np.array([bounds[1]+pad,bounds[3]+pad]);a=np.asarray(a)[:2];v=np.asarray(b)[:2]-a;t0,t1=0.,1.
 for j in range(2):
  if abs(v[j])<1e-12:
   if a[j]<lo[j] or a[j]>hi[j]:return False
  else:
   ts=sorted(((lo[j]-a[j])/v[j],(hi[j]-a[j])/v[j]));t0=max(t0,ts[0]);t1=min(t1,ts[1])
 return t0<=t1
old=build(before);new=build(after);report={'language':os.environ.get('EXPLAINER_LANG','en'),'scope':'Isolated actual-Manim label/axes/contour constructors; no scene render/data loads/import of Part6 scene or producer.'}
# Caption entirely below active final contour and above existing footer, within frame.
z=new['zero'];touch=new['R'][5];footer=new['tag'];assert z.get_top()[1]+.10<touch.get_bottom()[1],(box(z),box(touch));assert footer.get_top()[1]+.10<z.get_bottom()[1];assert z.get_left()[0]>-config.frame_width/2+.1 and z.get_right()[0]<config.frame_width/2-.1
# Annotation glyph bounding rectangle clears the identity's full segment and preserves all true plot vertices.
zl=new['zl'];ident=new['ident'];assert not segment_hits_box(ident.get_start(),ident.get_end(),box(zl)),(box(zl),ident.get_start(),ident.get_end());assert segment_hits_box(old['ident'].get_start(),old['ident'].get_end(),box(old['zl']))
assert zl.get_right()[0]<config.frame_width/2-.15 and zl.get_bottom()[1]>new['g'].xlabel.get_top()[1]+.1 if hasattr(new['g'],'xlabel') else True
for name in ['ident','st','zone']:
 np.testing.assert_array_equal(old[name].get_all_points(),new[name].get_all_points())
# Color-only Indicate does not move any measured/illustrative point at any sample.
p0=touch.get_all_points().copy();anim=Indicate(touch,color=new['LASSO'],scale_factor=1.0);anim.begin()
for alpha in np.linspace(0,1,41):anim.interpolate(float(alpha));np.testing.assert_allclose(touch.get_all_points(),p0,atol=1e-12)
anim.finish();report.update(shapes_caption_before=box(old['zero']),shapes_caption_after=box(z),active_contour=box(new['R'][5]),footer=box(footer),threshold_caption_before=box(old['zl']),threshold_caption_after=box(zl),identity_endpoints=[ident.get_start().tolist(),ident.get_end().tolist()],geometry_unchanged=['ident','st','zone'],indicate_samples=41,status='passed')
(R/f"geometry-{report['language']}.json").write_text(json.dumps(report,indent=2));print(json.dumps(report))
