import json,re,hashlib,sys,datetime
from pathlib import Path
ROOT=Path('/workspace/explainer-videos');OUT=Path('/workspace/runtime/ai4-theory-endpoint-review');sys.path.insert(0,str(ROOT))
from explainer.ai import label,VGroup,DOWN,LEFT,tempconfig
raw=(OUT/'en-HVP/render-result.json').read_bytes();d=json.loads(raw);strings={};checks=[]
for w in d['warnings']:
 if w['kind']!='untranslated-on-screen':continue
 en=w['text'];zh=en.replace('step ','步数 ').replace(': loss ','：损失 ').replace('; training accuracy ','；训练准确率 ').replace('; high-positive ','；高正值 ').replace('; negative ','；负值 ').replace('; near-zero ','；近零 ')
 assert zh!=en
 assert re.findall(r'\\[A-Za-z%]+|\\[,{}]',en)==re.findall(r'\\[A-Za-z%]+|\\[,{}]',zh),(en,zh)
 assert not re.search(r'(?<!\\)\\\\(?:rho|%)',zh),zh
 strings[en]=zh
assert len(strings)==12
payload={'strings':strings,'scope':'Exact 12 missing HVP nested readout captions from actual EN endpoint warning keys; private proposal for root merge','source_render_result_sha256':hashlib.sha256(raw).hexdigest(),'source_module_sha256':hashlib.sha256((ROOT/'videos/ai/ai4/s14_hvp.py').read_bytes()).hexdigest(),'TeX_policy':'Original math substrings and command sequences preserved exactly; no double escaping introduced.'}
p=OUT/'hvp-readout-caption-overlay.json';p.write_text(json.dumps(payload,ensure_ascii=False,indent=2))
(OUT/'readout-Tex').mkdir(exist_ok=True)
with tempconfig({'media_dir':str(OUT),'tex_dir':str(OUT/'readout-Tex')}):
 labels=[]
 for en,zh in strings.items():
  obj=label(zh,font_size=22 if en.startswith('step ') else 20)
  labels.append(obj)
  checks.append({'en':en,'zh':zh,'compiled':True,'math_commands_preserved':True,'width':float(obj.width),'height':float(obj.height)})
 for i in range(0,len(labels),2):
  group=VGroup(*labels[i:i+2]).arrange(DOWN,aligned_edge=LEFT,buff=.12).move_to([2.9,2.6,0])
  if group.width>6.5:group.scale_to_fit_width(6.5)
  bounds=[float(group.get_left()[0]),float(group.get_right()[0]),float(group.get_bottom()[1]),float(group.get_top()[1])]
  assert bounds[0]>=-7.141 and bounds[1]<=7.141 and bounds[2]>=-4.03 and bounds[3]<=4.03,bounds
  checks[i]['paired_readout_bounds']=bounds
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'overlay_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'compiled_labels':12,'construction':'Actual explainer.ai.label -> Tex with CJK compiler, font sizes22/20 and actual source readout grouping/width cap6.5; static objects only, no render','checks':checks,'source_module_sha256':payload['source_module_sha256']}
(OUT/'hvp-readout-caption-compile.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('PASS12labels',report['overlay_sha256'])
