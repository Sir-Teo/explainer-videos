"""Freeze one completed silent movie, extract bounded frames, map exact duplicates."""
from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,sys,time
from PIL import Image,ImageDraw

repo=Path('/workspace/explainer-videos');root=Path(__file__).parent
language,scene=sys.argv[1:]
canonical=repo/'renders/qa/series/ai4'/language/(scene+'_motion')/'result.json'
raw=canonical.read_bytes();render=json.loads(raw)
assert render['mode']=='motion' and render['status'] in ['passed','needs-review']
movie=repo/render['movie'];sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
movie_sha=sha(movie);out=root/language/scene/movie_sha;out.mkdir(parents=True,exist_ok=True)
assert not (out/'audit/result.json').exists(),'Reconcile existing audit instead of blindly rerunning.'
(out/'render-result-original.json').write_bytes(raw)
frozen=out/(scene+'.mp4');shutil.copy2(movie,frozen);assert sha(frozen)==movie_sha
assert canonical.read_bytes()==raw and sha(movie)==movie_sha
derived=dict(render);derived['movie']=str(frozen)
derived['_qa_freeze']={'derived_record':'Only movie path rewritten to immutable copy for tool provenance.',
    'original_record':str(canonical.relative_to(repo)),
    'original_record_sha256':hashlib.sha256(raw).hexdigest(),'movie_sha256':movie_sha}
(out/'result.json').write_text(json.dumps(derived,ensure_ascii=False,indent=2)+'\n')
source_paths=[repo/'videos/ai/ai4'/n for n in ['s06_modes.py','s07_backprop.py','s08_library.py','s09_train.py','s10_floats.py','zh_lines.py','common.py']]
source_paths += [repo/'videos/ai/ai_text_zh.json',repo/'tools/qa_motion.py',repo/'tools/qa_scene.py',repo/'tools/qa_series.py',repo/'explainer/ai/autodiff.py']
source_hashes={}
for p in source_paths:
 target=out/'source'/p.relative_to(repo);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
 source_hashes[str(p.relative_to(repo))]=sha(target);assert sha(p)==sha(target)
inputs={}
for name,stats in render['inputs'].items():
 if stats is None:inputs[name]=None;continue
 p=repo/name;assert [p.stat().st_size,p.stat().st_mtime_ns]==stats
 inputs[name]=dict(sha256=sha(p),bytes=stats[0],mtime_ns=stats[1])
command=['python',str(repo/'tools/qa_motion.py'),str(frozen),'-o',str(out/'audit'),'--dense','.5','--max-gap','1']
started=time.monotonic()
with (out/'extract.log').open('w') as log:
 process=subprocess.run(command,cwd=repo,stdout=log,stderr=subprocess.STDOUT)
assert process.returncode==0,'Extraction failed; inspect retained extract.log.'
audit=json.loads((out/'audit/result.json').read_text());assert audit['source_sha256']==movie_sha
assert audit['tool_sha256']==source_hashes['tools/qa_motion.py']
for name,row in inputs.items():
 if row is not None:assert sha(repo/name)==row['sha256']
unique=[];seen={};mapping=[]
for i,row in enumerate(audit['selected_frames']):
 p=out/'audit'/row['file'];assert sha(p)==row['sha256']
 with Image.open(p) as image:
  pixel_sha=hashlib.sha256(image.convert('RGB').tobytes()).hexdigest()
 if pixel_sha not in seen:
  seen[pixel_sha]=len(unique);unique.append(dict(row,pixel_sha256=pixel_sha,selected_index=i))
 mapping.append(dict(row,pixel_sha256=pixel_sha,representative=seen[pixel_sha],
                     representative_selected_index=unique[seen[pixel_sha]]['selected_index']))
views=out/'review';views.mkdir(exist_ok=True);pages=[]
for start in range(0,len(unique),8):
 chunk=unique[start:start+8];w,h=640,round(audit['source_height']*640/audit['source_width']);page=Image.new('RGB',(w*2,(h+30)*((len(chunk)+1)//2)),(20,23,32));draw=ImageDraw.Draw(page)
 for i,row in enumerate(chunk):
  x,y=(i%2)*w,(i//2)*(h+30)
  draw.text((x+6,y+6),f"{language} {scene} t={row['time']:.6f}s src={row['source_frame']} unique={start+i}",fill='white')
  with Image.open(out/'audit'/row['file']) as native:page.paste(native.convert('RGB').resize((w,h)),(x,y+30))
 name=f'page-{len(pages)+1:03d}.png';page.save(views/name)
 pages.append(dict(file=name,sha256=sha(views/name),first_unique=start,unique_count=len(chunk),
                   representatives=[r['selected_index'] for r in chunk],first_time=chunk[0]['time'],last_time=chunk[-1]['time'],tile_width=640,scale=640/audit['source_width']))
receipt=dict(language=language,scene=scene,frozen_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    original_record_sha256=hashlib.sha256(raw).hexdigest(),movie_sha256=movie_sha,movie_bytes=frozen.stat().st_size,
    source_hashes=source_hashes,inputs=inputs,raw_status=render['status'],raw_warnings=render['warnings'],
    original_fingerprint=render['fingerprint'],command=command,exit_code=process.returncode,elapsed=time.monotonic()-started,
    audit_sha256=sha(out/'audit/result.json'),decoded_frames=audit['analysis']['decoded_frames'],
    selected_frames=len(mapping),unique_pixel_frames=len(unique),exact_duplicate_selections=len(mapping)-len(unique),
    frame_mapping=mapping,pages=pages,
    review=dict(viewed_pages=[],native_followups=[],findings=[],continuous_playback='unverified',audio='unverified'),
    limits='All movie frames decoded algorithmically; only selected frames are candidates for actual visual inspection. '
           'Pixel-equal selections may inherit one actually viewed representative; no perceptual-similarity inheritance. '
           'Unselected time/frame intervals remain in audit/result.json. No continuous playback/audio/1080 claim.')
(out/'review-map.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(path=str(out),decoded=receipt['decoded_frames'],selected=receipt['selected_frames'],unique=len(unique),pages=len(pages),movie_sha256=movie_sha),indent=2))
