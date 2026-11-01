from pathlib import Path
from contextlib import contextmanager
from types import SimpleNamespace
import ast,json,hashlib,os,sys,math
import numpy as np
R=Path('/workspace/explainer-videos');D=Path('/workspace/runtime/ai6-outro-recap-cue-candidate');sys.path.insert(0,str(R))
from explainer import lang,tts
from explainer.voiceover import _strip_bookmarks,VoiceoverTracker
from explainer.zh_templates import Translator
LANG=os.environ['EXPLAINER_LANG'];assert LANG in ['en','zh'] and tts.BACKEND=='silent'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def forbidden(*args,**kw):raise AssertionError('synthesis forbidden in puretimingpreflight')
tts.synthesize=forbidden
proposal=json.loads((D/'zh-proposal.json').read_text());tr=Translator('ai6');tr.zh.update(proposal['ZH_updates']);lang._templates=lambda root,language:tr if language=='zh' else None
metadata=json.loads((D/'before-witness'/LANG/'Outro.narration.json').read_text());line=metadata['lines'][0];suppliedtext=line['text'];utt=SimpleNamespace(duration=line['duration'],words=[SimpleNamespace(text=w,start=s,end=e) for w,s,e in line['words']]);fps=15.;dt=1/fps
class Box:
 def to_edge(self,*args,**kwargs):return self
class Fade:
 def __init__(self,obj,**kw):self.obj=obj;self.kw=kw
class Lag:
 def __init__(self,*fades,lag_ratio):self.fades=fades;self.lag_ratio=lag_ratio
class Schedule:
 def __init__(self):self.renderer=SimpleNamespace(time=0.);self.events=[];self.cues={};self.identity={}
 def tiles(self):return list(range(12))
 @contextmanager
 def voiceover(self,raw):
  translated=lang.translate(raw,R/'videos/ai/ai6','Outro');clean,marks=_strip_bookmarks(translated);assert clean==suppliedtext
  ck=tts.cache_key(clean);self.identity={'clean':clean,'spoken':ck[1],'silent_cache_key':ck[2],'raw_english':raw,'translated_marked':translated,'marks':marks};self.cues={k:utt.words[i].start if i<len(utt.words) else utt.duration for k,i in marks.items()}
  tracker=VoiceoverTracker(self,utt,marks,self.renderer.time);yield tracker
  left=utt.duration-tracker.elapsed()
  if left>1/60:self.wait(left)
  self.wait(.15)
 def wait(self,duration):self.renderer.time+=int(duration/dt)*dt
 def play(self,*animations,run_time=1.):
  start=self.renderer.time;actual=len(np.arange(0,run_time,dt))*dt
  if len(animations)==1 and isinstance(animations[0],Lag):
   lag=animations[0];total=1+(len(lag.fades)-1)*lag.lag_ratio
   for k,f in enumerate(lag.fades):self.events.append({'tile':f.obj,'start_predicted':start+run_time*k*lag.lag_ratio/total,'settled_predicted':start+run_time*(k*lag.lag_ratio+1)/total,'run_time_requested':run_time,'type':'olduniformLaggedStart'})
  else:
   for f in animations:
    if isinstance(f,Fade) and isinstance(f.obj,int):self.events.append({'tile':f.obj,'start_predicted':start,'settled_predicted':start+actual,'run_time_requested':run_time,'type':'namedgroupFadeIn'})
  self.renderer.time+=actual
 def clear_scene(self):self.play(run_time=1.)
results={}
for phase in ['before','candidate']:
 tree=ast.parse((D/(phase+'.py')).read_text());recap=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='recap');ns={'label':lambda *a,**k:Box(),'PART':6,'UP':np.array([0.,1.,0.]),'FadeIn':Fade,'LaggedStart':Lag,'config':SimpleNamespace(frame_rate=fps)};exec(compile(ast.fix_missing_locations(ast.Module([recap],type_ignores=[])),'actualrecapAST-no-camera','exec'),ns);s=Schedule();ns['recap'](s);assert sorted(e['tile'] for e in s.events)==list(range(12));results[phase]={'identity':s.identity,'cue_times':s.cues,'tile_schedule':s.events,'predicted_next_block_start':s.renderer.time,'actual_supplied_next_block_start':metadata['lines'][1]['start']}
assert results['before']['identity']['clean']==results['candidate']['identity']['clean'];assert results['before']['identity']['spoken']==results['candidate']['identity']['spoken'];assert results['before']['identity']['silent_cache_key']==results['candidate']['identity']['silent_cache_key']
assert abs(results['before']['predicted_next_block_start']-metadata['lines'][1]['start'])<=dt+1e-8
cachekey=results['candidate']['identity']['silent_cache_key'];wav=R/'.cache/tts'/(cachekey+'.wav');meta=wav.with_suffix('.json');assert wav.exists() and meta.exists();cacheidentity={'key':cachekey,'existing_wav_sha256':sha(wav),'existing_wav_bytes':wav.stat().st_size,'existing_metadata_sha256':sha(meta),'backend':tts.BACKEND,'voice':tts.VOICE,'speed':tts.SPEED,'no_synthesize_call':True}
groups=proposal['cue_groups'];groupstates=[]
for k,g in enumerate(groups):
 cue=results['candidate']['cue_times'][g['name']]
 nextcue=results['candidate']['cue_times'][groups[k+1]['name']] if k+1<len(groups) else utt.duration
 events=[e for e in results['candidate']['tile_schedule'] if e['tile'] in g['tile_indices']]
 settled=max(e['settled_predicted'] for e in events);assert settled<nextcue
 groupstates.append({'name':g['name'],'tile_indices':g['tile_indices'],'cue_word_start':cue,'next_group_or_line_end':nextcue,'start_predicted':min(e['start_predicted'] for e in events),'fully_settled_predicted':settled,'settled_hold_before_next_group':nextcue-settled})
# The Newton picture arrives with the logistic/Newton clause, before Newton is actually named.
newton_token=next(i for i,w in enumerate(utt.words) if (w.text.startswith("Newton") if LANG=='en' else w.text=='牛'))
newton_mention=utt.words[newton_token].start;newton_new=next(e for e in results['candidate']['tile_schedule'] if e['tile']==4);newton_old=next(e for e in results['before']['tile_schedule'] if e['tile']==4);assert newton_new['settled_predicted']<newton_mention
result={'lang':LANG,'source_before_sha256':sha(D/'before.py'),'candidate_sha256':sha(D/'candidate.py'),'local_zh_base_sha256':sha(D/'zh_lines.base.py'),'private_zh_proposal_sha256':sha(D/'zh-proposal.json'),'cleaned_spoken_cache_identity_verified':True,'existing_cache_identity':cacheidentity,'group_schedule':groupstates,'newton':{'spoken_name_start':newton_mention,'old_schedule':newton_old,'candidate_schedule':newton_new,'predicted_settled_lead_before_named_word':newton_mention-newton_new['settled_predicted']},'complete_source_call_runs':results,'model':'Exact recap method AST executed with no-camera scheduling stubs, real lang.translate/privateTranslator, realbookmarkstrip andVoiceoverTracker. FreshCairo15fpsmodel: dynamicplay=len(np.arange(0,run_time,1/fps))/fps; frozenwait=int(duration*fps)/fps; wait_until usesactual1/60threshold. Baseline nextblock reproducedwithinoneframe.','limits':['Pure source/actualsilentwordtimestamp prediction, not newrender/pixel/listening approval.','Silentwordtimings are estimated uniformtoken timing; realspokenvoice alignment still needs actualspeech review.','Cleanedtext/spoken/cachekeys are exact; animation scheduling intentionallychanges. Predicted blockduration agreement does not prove actualtotalduration/audioequivalence.','When futurecuegap falls belowoneframe, a oneframefade can overrun; actualsupplied9group budgets all leavepositiveheldtime.']}
(D/f'preflight-{LANG}.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'lang':LANG,'cachekey':cachekey,'spoken_identity':True,'Newton_name':newton_mention,'old_Newton_settled':newton_old['settled_predicted'],'candidate_Newton_settled':newton_new['settled_predicted'],'minimum_group_hold':min(g['settled_hold_before_next_group'] for g in groupstates),'next_block_model':results['candidate']['predicted_next_block_start'],'actual_old_next_block':metadata['lines'][1]['start']},indent=2),flush=True)
