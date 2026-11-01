from pathlib import Path
import ast,json,sys,os,hashlib,math
import numpy as np
R=Path('/workspace/explainer-videos');D=Path('/workspace/runtime/ai6-lda-repair-candidate');sys.path.insert(0,str(R))
from explainer.ai import *
from manim import tempconfig
lang=os.environ.get('EXPLAINER_LANG','en')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def assignments(n,name):return isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets)
def execute(nodes,ns):exec(compile(ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[])),'bounded-extracted-geometry','exec'),ns)
results={}
with tempconfig({'media_dir':str(D/'object-cache'),'verbosity':'ERROR'}):
 for phase,src in [('before',D/'before.py'),('candidate',D/'candidate.py')]:
  tree=ast.parse(src.read_text());f=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='fisher');ns=dict(globals());ns['th']=ValueTracker(.15)
  nodes=[next(n for n in tree.body if assignments(n,'U'))]
  for n in f.body:
   if assignments(n,'C0') or assignments(n,'names') or isinstance(n,ast.FunctionDef) and n.name in ['S','direction']:nodes.append(n)
   if isinstance(n,ast.For) and isinstance(n.target,ast.Name) and n.target.id=='name' and isinstance(n.iter,ast.Name) and n.iter.id=='names':nodes.append(n)
  execute(nodes,ns);names=ns['names'];rows=[]
  for i,n in enumerate(names):
   glyph=n if phase=='before' else VGroup(*n.submobjects[1:]);pts=glyph.get_all_points();row={'index':i,'glyph_bounds':[float(glyph.get_left()[0]),float(glyph.get_right()[0]),float(glyph.get_bottom()[1]),float(glyph.get_top()[1])],'glyph_point_sha256':hashlib.sha256(pts.tobytes()).hexdigest(),'glyph_point_count':len(pts)}
   if phase=='candidate':
    bg=n.submobjects[0];row['background']={'bounds':[float(bg.get_left()[0]),float(bg.get_right()[0]),float(bg.get_bottom()[1]),float(bg.get_top()[1])],'opacity':float(bg.get_fill_opacity()),'color':bg.get_fill_color().to_hex(),'z_index':n.z_index,'background_z_index':bg.z_index,'glyph_min_z_index':min(x.z_index for x in glyph.family_members_with_points())}
    assert row['background']['opacity']==1 and row['background']['background_z_index']==5 and row['background']['glyph_min_z_index']==5
    assert abs(bg.width-glyph.width-.08)<1e-12 and abs(bg.height-glyph.height-.08)<1e-12
   rows.append(row)
  bounds=[];max_drift=0.
  for theta in np.linspace(.15,math.pi*.97,181):
   ns['th'].set_value(float(theta));g=ns['direction']();bounds.append([float(g.get_bottom()[1]),float(g.get_top()[1])]);start=g.get_all_points().copy();an=Indicate(g,color=C.BITS,scale_factor=1.0);an.begin()
   for alpha in np.linspace(0,1,61):an.interpolate(float(alpha));max_drift=max(max_drift,float(np.abs(g.get_all_points()-start).max()))
   an.finish()
  assert max_drift<1e-12
  results[phase]={'source_sha256':sha(src),'labels':rows,'sweep_y_min':min(x[0] for x in bounds),'sweep_y_max':max(x[1] for x in bounds),'frame_half_height':float(config.frame_height/2),'color_only_Indicate_181angles_x61phases_max_point_drift':max_drift}
 for i in range(2):assert results['before']['labels'][i]['glyph_point_sha256']==results['candidate']['labels'][i]['glyph_point_sha256'];assert results['before']['labels'][i]['glyph_bounds']==results['candidate']['labels'][i]['glyph_bounds']
 results['scope']='Actual Manim objects from exact source AST fragments; no scene imports/data/model/producers/renders.181directionangles×61color-onlyanimationphases. Names glyph points/positions byteexact; onlyindividual opaque.04masks+z5 added.'
 results['language']=lang
 (D/f'geometry-{lang}.json').write_text(json.dumps(results,indent=2)+'\n');print(lang,'geometryPASS',max(x['color_only_Indicate_181angles_x61phases_max_point_drift'] for x in [results['before'],results['candidate']]),flush=True)
