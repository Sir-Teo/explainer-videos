from pathlib import Path
import os,json,hashlib,wave,array,sys
os.environ['EXPLAINER_TTS']='server';os.environ['EXPLAINER_VOICE']='qwen3-calm-a';os.environ['EXPLAINER_LANG']='en'
B=Path('/workspace/explainer-videos');sys.path.insert(0,str(B))
from explainer import tts
x=json.loads((B/'renders/qa/narrated/ai1/en/Information_result.json').read_text())
rows=[]
for n,line in enumerate(x['narration'],1):
 clean,spoken,key=tts.cache_key(line['text']);p=B/'.cache/tts'/f'{key}.json';w=p.with_suffix('.wav')
 assert p.exists() and w.exists(),key
 meta=json.loads(p.read_text());assert meta['text']==clean and meta['spoken']==spoken
 with wave.open(str(w),'rb') as f:
  sr=f.getframerate();frames=f.getnframes();channels=f.getnchannels();width=f.getsampwidth();pcm=f.readframes(frames)
 assert width==2
 samples=array.array('h');samples.frombytes(pcm)
 if sys.byteorder!='little':samples.byteswap()
 nonzero=sum(v!=0 for v in samples);peak=max(abs(v) for v in samples)
 assert nonzero>0
 rows.append({'block':n,'cache_key':key,'text':clean,'spoken':spoken,'duration':meta['duration'],'tokens':len(meta['tokens']),'wav_sample_rate':sr,'wav_frames':frames,'channels':channels,'sample_width':width,'nonzero_samples':nonzero,'peak_integer':peak,'files':[{'path':str(q.relative_to(B)),'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()} for q in [p,w]]})
report={'scope':'Six existing real InformationEN speech blocks and alignment metadata. Actualcache_key evaluated with backendserver,voiceqwen3-calm-a,speed1.0 and currentprofile matching927. No synthesis/network/model load. Nonzero PCM confirms speech-bearing signal, not pronunciation/listening approval.','source_result':'renders/qa/narrated/ai1/en/Information_result.json','source_result_sha256':hashlib.sha256((B/'renders/qa/narrated/ai1/en/Information_result.json').read_bytes()).hexdigest(),'backend':tts.BACKEND,'voice':tts.VOICE,'speed':tts.SPEED,'profile':tts._profile_settings(),'blocks':rows,'total_transfer_bytes':sum(f['bytes'] for r in rows for f in r['files'])}
p=Path('/workspace/runtime/production-handoff-parts1-3/real-information-audio.json');p.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'blocks':len(rows),'transfer_bytes':report['total_transfer_bytes'],'keys':[r['cache_key'] for r in rows],'durations':[r['duration'] for r in rows]},indent=2))
