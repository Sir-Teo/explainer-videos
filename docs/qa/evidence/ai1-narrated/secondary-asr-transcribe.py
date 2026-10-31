"""Local secondary ASR only. Requires explicit root confirmation that TTS is stopped.

No expected text is passed as a decoder prompt. No narration is synthesized/edited,
and no repository QA records or cached audio are modified.
"""
import argparse,datetime,hashlib,json,os,resource,subprocess,sys,time,wave
from pathlib import Path
ROOT=Path('/workspace/explainer-videos');OUT=Path('/workspace/runtime/asr-second');MODEL=OUT/'whisper-base.en'

def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()

def memory():
 current=int(Path('/sys/fs/cgroup/memory.current').read_text());limit=int(Path('/sys/fs/cgroup/memory.max').read_text())
 return {'current_bytes':current,'limit_bytes':limit,'headroom_bytes':limit-current}

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--tts-stopped-confirmed',action='store_true',help='Use only after root explicitly confirms TTS stopped and inference may begin.')
 parser.add_argument('--all-information',action='store_true',help='Decode all six current Information clips in addition to the stress probe.')
 args=parser.parse_args()
 if not args.tts_stopped_confirmed:
  parser.error('Preparation only: wait for explicit root confirmation before model loading/inference.')
 before=memory()
 if before['headroom_bytes']<3*1024**3:
  raise RuntimeError('Require at least3GiB cgroup headroom before loading: '+str(before))
 manifest=json.loads((OUT/'download-manifest.json').read_text())
 for f in manifest['artifacts']:
  if sha(MODEL/f['file'])!=f['sha256']:raise RuntimeError('Artifact hash changed: '+f['file'])
 source=ROOT/'renders/qa/series/ai1/en/Information/audio_result.json';source_raw=source.read_bytes();capture=json.loads(source_raw)
 block=capture['lines'][4]
 inputs=[{'name':'corrected_stress_probe','path':str(ROOT/'.cache/tts/c39672c704c3129b.wav'),'expected':None},
         {'name':'Information_block_5','path':block['audio_path'],'expected':block['spoken']}]
 if args.all_information:
  inputs=inputs[:1]+[{'name':f'Information_block_{i+1}','path':line['audio_path'],'expected':line['spoken']} for i,line in enumerate(capture['lines'])]
 probe_meta=(ROOT/'.cache/tts/c39672c704c3129b.wav').with_suffix('.json')
 if probe_meta.exists():inputs[0]['original_probe_metadata']=json.loads(probe_meta.read_text())
 for x in inputs:
  x['sha256']=sha(x['path'])
  with wave.open(x['path']) as f:x.update(original_sample_rate=f.getframerate(),original_channels=f.getnchannels(),original_frames=f.getnframes(),duration_seconds=f.getnframes()/f.getframerate())
 # Heavy imports and model construction occur only after the two guards above.
 import numpy as np
 import torch
 from transformers import WhisperProcessor,WhisperForConditionalGeneration
 torch.set_num_threads(1)
 start=time.monotonic()
 processor=WhisperProcessor.from_pretrained(str(MODEL),local_files_only=True)
 model=WhisperForConditionalGeneration.from_pretrained(str(MODEL),local_files_only=True,torch_dtype=torch.float32)
 model.eval()
 report={'scope':'Secondary automated speech recognition evidence only; no manual hearing/pronunciation or production QA approval.',
         'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'model_repository':'openai/whisper-base.en','model_revision':manifest['revision'],
         'model_files_manifest':'download-manifest.json','device':'cpu','dtype':'float32','torch_threads':1,'decoding':'greedy, num_beams1, no expected-text prompt',
         'source_audio_record':str(source),'source_audio_record_sha256':hashlib.sha256(source_raw).hexdigest(),'source_audio_record_status_at_read':capture.get('status'),
         'script_sha256':sha(__file__),'all_information_clips_requested':args.all_information,'memory_before_load':before,'load_seconds':round(time.monotonic()-start,3),'inputs':inputs}
 for item in inputs:
  # ffmpeg resampling preserves the cached input; samples are written only beneath OUT.
  resampled=OUT/(item['name']+'_16k.wav')
  subprocess.run(['ffmpeg','-v','error','-nostdin','-y','-i',item['path'],'-ac','1','-ar','16000','-c:a','pcm_s16le',str(resampled)],check=True)
  with wave.open(str(resampled)) as f:
   audio=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(np.float32)/32768
  segments=[]
  # Independent short-form windows avoid a tokenizer or chunker interpreting expected text.
  # Ten-second overlap keeps words at a30s boundary available to another decode.
  for offset in range(0,len(audio),20*16000):
   if offset and len(audio)-offset<5*16000:break
   samples=audio[offset:offset+30*16000]
   features=processor(samples,sampling_rate=16000,return_tensors='pt',return_attention_mask=True)
   began=time.monotonic()
   with torch.inference_mode():
    predicted=model.generate(input_features=features.input_features,attention_mask=features.attention_mask,max_new_tokens=224,num_beams=1,do_sample=False,return_timestamps=False)
   text=processor.batch_decode(predicted,skip_special_tokens=True)[0].strip()
   segments.append({'start_seconds':offset/16000,'end_seconds':min(offset+len(samples),len(audio))/16000,'transcript':text,'elapsed_seconds':round(time.monotonic()-began,3)})
  item['segments']=segments;item['resampled_audio_path']=str(resampled);item['input_unchanged_after_decode']=sha(item['path'])==item['sha256']
  import re
  item['term_flags']=[{'start_seconds':s['start_seconds'],'millionths':bool(re.search(r'\bmillionths?\b',s['transcript'],re.I)),
                      'millions':bool(re.search(r'\bmillions\b',s['transcript'],re.I)),
                      'minus_or_negative':bool(re.search(r'\b(?:minus|negative)\b',s['transcript'],re.I))} for s in segments]
  report['peak_process_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
  report['memory_after_decode']=memory()
  (OUT/'transcripts.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
  print(item['name'],json.dumps(segments,ensure_ascii=False),flush=True)
 report['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
 report['total_elapsed_seconds']=round(time.monotonic()-start,3)
 (OUT/'transcripts.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print('Peak RSS KiB',report['peak_process_rss_kib'],flush=True)

if __name__=='__main__':main()
