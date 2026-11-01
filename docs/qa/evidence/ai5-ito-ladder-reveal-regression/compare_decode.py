from pathlib import Path
import hashlib,json,subprocess,datetime
O=Path(__file__).parent;B=Path('/workspace/runtime/ai5-ito-sde-fokker-motion-review')
old={'en':B/'en-Ito/959961e957831004e962bd0841e5fa978a350a91ece728f508cb2cf0bfcefa99/Ito.mp4','zh':B/'zh-Ito/74d8917be2b3c0f1c55d69a2438aaa7bfc4de0eec6e728aa975c587d4318c1d3/Ito.mp4'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def hashes(movie,log):
 count=854*480*3;out=[]
 with log.open('wb') as err:
  p=subprocess.Popen(['ffmpeg','-v','error','-xerror','-err_detect','explode','-threads','1','-i',str(movie),'-map','0:v:0','-an','-sn','-filter_threads','1','-pix_fmt','rgb24','-threads','1','-f','rawvideo','pipe:1'],stdout=subprocess.PIPE,stderr=err)
  while True:
   chunk=p.stdout.read(count)
   if not chunk:break
   while len(chunk)<count:
    add=p.stdout.read(count-len(chunk))
    if not add:raise RuntimeError('partial nativeRGB frame')
    chunk+=add
   out.append(hashlib.sha256(chunk).hexdigest())
  assert p.wait()==0,log
 return out
rows=[]
for l in ['en','zh']:
 p=O/l/'decoded-comparison.json';assert not p.exists();a=hashes(old[l],O/l/'before-native-decode.log');b=hashes(O/l/'Ito.mp4',O/l/'after-native-decode.log');assert len(a)==len(b)
 diff=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y];runs=[]
 for i in diff:
  if runs and i==runs[-1][-1]+1:runs[-1].append(i)
  else:runs.append([i])
 row={'lang':l,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'before_movie_sha256':sha(old[l]),'after_movie_sha256':sha(O/l/'Ito.mp4'),'frame_size':[854,480],'pixel_format':'RGB24','fps':15,'decoded_frame_count':len(a),'before_all_frame_rgb_sha256':a,'after_all_frame_rgb_sha256':b,'different_rgb_frames':diff,'different_runs':[{'first':r[0],'last':r[-1],'start':r[0]/15,'end':r[-1]/15,'count':len(r)} for r in runs],'limits':'Full native video decoding and exact pixel comparison only, not visual review. Exact old actually viewed PNG inheritance is evaluated separately.'};p.write_text(json.dumps(row,indent=2)+'\n');print(l,'different',len(diff),'runs',row['different_runs'],flush=True)
