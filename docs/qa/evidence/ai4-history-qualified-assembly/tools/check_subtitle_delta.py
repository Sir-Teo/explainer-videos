from pathlib import Path
import json,hashlib,re
R=Path('/workspace/runtime/ai4-silent-preview-assembly');rows=[]
for l in ['en','zh']:
 old=json.loads((R/'current-reviewed'/l/'validation/subtitle-boundaries.json').read_text());new=json.loads((R/'history-qualified'/l/'validation/subtitle-boundaries.json').read_text());ov=json.loads((R/'current-reviewed'/l/'validation/validation.json').read_text());nv=json.loads((R/'history-qualified'/l/'validation/validation.json').read_text());chap=[]
 for i in range(19):
  a=[x for x in old['cues'] if x['chapter_index']==i];b=[x for x in new['cues'] if x['chapter_index']==i];os=ov['chapters'][i]['start'];ns=nv['chapters'][i]['start'];assert len(a)==len(b)
  same=all(x['text_sha256']==y['text_sha256'] for x,y in zip(a,b));gap=max(abs((y[k]-ns)-(x[k]-os)) for x,y in zip(a,b) for k in ['start','end'])
  if i!=2:assert same and gap<=.0011
  chap.append({'index':i,'scene':nv['chapters'][i]['scene'],'cues':len(b),'chapter_start_shift':ns-os,'allcue_text_hashes_same':same,'maximum_relative_cue_boundary_shift':gap,'unchanged_clip_localcue_timing_verified':i!=2})
 text=Path(json.loads((R/'history-qualified'/l/'assembly-receipt.json').read_text())['subtitle']).read_text();plain=' '.join(line for line in text.splitlines() if line and not line.isdigit() and ' --> ' not in line);assert 'oldest method' not in plain.lower()
 if l=='en':assert 'standard optimization method' in plain
 rows.append({'lang':l,'all18unchangedchaptercue_text_and_localtimings_preserved':True,'chapters':chap,'oldest_method_phrase_absent_from_current_subtitle':True})
(R/'history-qualified/subtitle-delta-check.json').write_text(json.dumps({'scope':'IndependentactualSRTcuehash/local-boundary comparisonafterallchapteroffsets regenerated; onlyGradientcapturecontent changes. No audioapproval.','cases':rows},indent=2)+'\n');print([(x['lang'],x['chapters'][3]['chapter_start_shift'],max(y['maximum_relative_cue_boundary_shift'] for y in x['chapters'] if y['index']!=2)) for x in rows])
