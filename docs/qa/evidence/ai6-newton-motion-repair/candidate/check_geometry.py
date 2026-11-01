import ast,copy,json,hashlib,os
from pathlib import Path
import numpy as np
from PIL import Image
R=Path('/workspace/runtime/ai6-newton-motion-review/candidate')
qa_lang=os.environ.get('EXPLAINER_LANG','en');proposal=json.loads((R/'caption-proposal.json').read_text())
if qa_lang=='zh':
 import explainer.zh_text as z
 z._TABLE=json.loads(Path('/workspace/explainer-videos/videos/ai/ai_text_zh.json').read_text())
 z._TABLE['strings'].update(proposal['captions']);z._BY_NUMBERS=None
from explainer.ai import *
config.media_dir=str(R/'fixture-media'/qa_lang);config.tex_dir=str(Path(config.media_dir)/'Tex');config.pixel_width=854;config.pixel_height=480
src=ast.parse((R/'s07_newton.proposed.py').read_text());race=next(x for x in ast.walk(src) if isinstance(x,ast.FunctionDef) and x.name=='race')
common=ast.parse(Path('/workspace/explainer-videos/videos/ai/ai6/common.py').read_text())
env=globals().copy();exec(compile(ast.Module(body=[copy.deepcopy(x) for x in common.body if isinstance(x,ast.FunctionDef) and x.name in ('plot','pow10')],type_ignores=[]),'pure-common-geometry','exec'),env)
env['penalty']=float(json.loads(Path('/workspace/explainer-videos/.cache/ai6/irls.json').read_text())['l2'])
selected=[]
for n in race.body:
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ('g70','g70n') for t in n.targets):selected.append(n)
 elif isinstance(n,ast.Expr) and ast.unparse(n).startswith('g70n.next_to'):selected.append(n)
exec(compile(ast.fix_missing_locations(ast.Module(body=copy.deepcopy(selected),type_ignores=[])),'actual-newton-caption-constructors','exec'),env)
g,note=env['g70'],env['g70n']
def box(m):return [float(m.get_left()[0]),float(m.get_right()[0]),float(m.get_bottom()[1]),float(m.get_top()[1])]
b=box(note);assert b[0]>-config.frame_width/2+.1 and b[1]<config.frame_width/2-.1 and b[3]<config.frame_height/2-.1,(b,config.frame_width,config.frame_height)
assert note.get_bottom()[1]>g.get_top()[1]+.07
assert note[1].get_top()[1]<note[0].get_bottom()[1]-.09
scene=Scene();scene.camera.background_color=BG if 'BG' in globals() else '#0b1017';scene.camera.capture_mobjects([g,note]);Image.fromarray(scene.camera.pixel_array).save(R/f'caption-fixture-{qa_lang}.png')
report={'status':'passed','language':qa_lang,'scope':'AST-extracted actual g70 plot and proposed bilingual caption constructors; in-memory proposed translation overlay only. No scene/common producer import or data loading, JSON l2 read directly. Not actual rendered chapter approval.','penalty':env['penalty'],'caption_bounds':b,'plot_bounds':box(g),'line_bounds':[box(x) for x in note],'source_proposed_sha256':hashlib.sha256((R/'s07_newton.proposed.py').read_bytes()).hexdigest(),'image_sha256':hashlib.sha256((R/f'caption-fixture-{qa_lang}.png').read_bytes()).hexdigest()}
(R/f'geometry-{qa_lang}.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
