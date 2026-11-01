from pathlib import Path
import json,re,hashlib,math
from explainer import lang as L
R=Path('/workspace/runtime/ai6-newton-after-review');oldroot=Path('/workspace/runtime/ai6-remaining-qa-serial/runs/20261101T055536/07-Newton');newroot=Path('/workspace/runtime/ai6-newton-after-capture/runs/20261101T075505/07-Newton')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();out={}
for lang in ('en','zh'):
 L.LANG=lang;oldp=oldroot/lang/'motion/completed/media/videos/480p15/Newton.narration.json';newp=newroot/lang/'motion/completed/media/videos/480p15/Newton.narration.json';a=json.loads(oldp.read_text());b=json.loads(newp.read_text());assert len(a['lines'])==len(b['lines'])==5;rows=[]
 for i,(x,y) in enumerate(zip(a['lines'],b['lines'])):
  assert all(math.isfinite(float(y[k])) for k in ('start','duration')) and y['start']>=0 and y['duration']>0
  oldmarks=re.findall(r"<bookmark\s+mark=['\"]([^'\"]+)['\"]\s*/>",x['raw']);newmarks=re.findall(r"<bookmark\s+mark=['\"]([^'\"]+)['\"]\s*/>",y['raw']);assert oldmarks==newmarks
  assert (x['raw']==y['raw'])==(i!=2)
  words=y['words'];assert all(0<=float(w[1])<=float(w[2])<=b['duration']+1/15 for w in words);assert all(float(u[2])<=float(v[1])+1e-9 for u,v in zip(words,words[1:]));assert y['start']+y['duration']<=b['duration']+1/15
  translated=L.translate(y['raw'],Path('/workspace/explainer-videos/videos/ai/ai6'),'Newton'); assert L.clean(re.sub(r"<bookmark\s+mark=['\"]([^'\"]+)['\"]\s*/>",'',translated))==y['text']; marks={};parts=[];pos=0
  for m in re.finditer(r"<bookmark\s+mark=['\"]([^'\"]+)['\"]\s*/>",translated):
   parts.append(translated[pos:m.start()]);idx=len(L.tokens(L.clean(''.join(parts))));marks[m[1]]=words[idx][1] if idx<len(words) else y['start']+y['duration'];pos=m.end()
  assert list(marks.values())==sorted(marks.values())
  rows.append({'line':i,'raw_unchanged':x['raw']==y['raw'],'old_start':x['start'],'new_start':y['start'],'old_duration':x['duration'],'new_duration':y['duration'],'bookmarks':newmarks,'fresh_absolute_bookmark_times_from_actual_tokens_words':marks,'fresh_raw':y['raw'] if i==2 else None,'fresh_words':len(words)})
 race=b['lines'][2]['text'];assert '0.01' in race and ('71 by 71' in race if lang=='en' else '71乘71' in race);assert 'penalized objective' in race if lang=='en' else '带惩罚目标' in race
 out[lang]={'status':'passed silent-sidecar structural/content checks; no listening or real narration sync approval','old_sidecar':str(oldp),'old_sha256':sha(oldp),'new_sidecar':str(newp),'new_sha256':sha(newp),'old_movie_duration':a['duration'],'new_movie_duration':b['duration'],'duration_delta':b['duration']-a['duration'],'old_race_VO_duration':a['lines'][2]['duration'],'new_race_VO_duration':b['lines'][2]['duration'],'lines':rows}
(R/'sidecar-review.json').write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({k:{'old':v['old_movie_duration'],'new':v['new_movie_duration'],'delta':v['duration_delta'],'bookmarks':[r['fresh_absolute_bookmark_times_from_actual_tokens_words'] for r in v['lines']]} for k,v in out.items()}))
