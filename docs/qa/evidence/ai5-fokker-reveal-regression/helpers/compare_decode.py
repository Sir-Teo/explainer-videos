from pathlib import Path
import hashlib,json,subprocess,datetime
O=Path('/workspace/runtime/ai5-fokker-reveal-regression');B=Path('/workspace/runtime/ai5-ito-sde-fokker-motion-review')
old={'en':B/'en-FokkerPlanck/842896444f939e53af0608f2e0c212527abd73a090b707cad2303b589783cc3b/FokkerPlanck.mp4','zh':B/'zh-FokkerPlanck/3e293d7b94b9ef8c28fc83fc90cd2b8c554acc79e88481ed21402270e993b43b/FokkerPlanck.mp4'}
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
 p=O/l/'decoded-comparison.json';assert not p.exists();a=hashes(old[l],O/l/'before-native-decode.log');b=hashes(O/l/'FokkerPlanck.mp4',O/l/'after-native-decode.log');assert len(a)==len(b)
 diff=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y];runs=[]
 for i in diff:
  if runs and i==runs[-1][-1]+1:runs[-1].append(i)
  else:runs.append([i])
 row={'lang':l,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'before_movie_sha256':sha(old[l]),'after_movie_sha256':sha(O/l/'FokkerPlanck.mp4'),'frame_size':[854,480],'pixel_format':'RGB24','fps':15,'decoded_frame_count':len(a),'before_all_frame_rgb_sha256':a,'after_all_frame_rgb_sha256':b,'different_rgb_frames':diff,'different_runs':[{'first':r[0],'last':r[-1],'start':r[0]/15,'end':r[-1]/15,'count':len(r)} for r in runs],'limits':'Full native video decoding and exact pixel comparison only, not visual review. Exact old actually viewed PNG inheritance is evaluated separately.'};p.write_text(json.dumps(row,indent=2)+'\n');print(l,'different',len(diff),'runs',row['different_runs'],flush=True)
