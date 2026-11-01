import pathlib,sys,json,gzip,hashlib,subprocess,shutil,datetime
from PIL import Image,ImageDraw
rt=pathlib.Path(__file__).parent;repo=pathlib.Path('/workspace/explainer-videos');lang,expected=sys.argv[1:];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();pixel=lambda p:hashlib.sha256(Image.open(p).convert('RGB').tobytes()).hexdigest();case=rt/'after'/lang;case.mkdir(parents=True,exist_ok=True);assert not (case/'review.json').exists(),'already prepared; reconcile';source=repo/'videos/ai/ai3/s08_svd.py';assert sha(source)=='291bba0e7c180750274e2117114cc22382f3b9b81880db0a499791b4b2e3e322';canonical=repo/f'renders/qa/series/ai3/{lang}/SVD_motion';record=canonical/'result.json';r=json.loads(record.read_text());assert r['status'] in ['passed','needs-review'] and r['mode']=='motion';movie=pathlib.Path(r['movie']);movie=movie if movie.is_absolute() else repo/movie;assert sha(movie)==expected;shutil.copy2(movie,case/'SVD.mp4');shutil.copy2(record,case/'capture-result.json');shutil.copy2(source,case/'s08_svd.py');before=json.loads((rt/'before'/lang/'capture-result.json').read_text());assert r['narration']==before['narration'],'narration/timing differs; reconcile before inheritance';assert r['inputs']==before['inputs'],'input signatures differ';prior=json.loads(gzip.decompress((rt/'before'/lang/'prior-complete-selected-review.json.gz').read_bytes()));audit=json.loads((rt/'before-audit'/lang/'review.json').read_text());baseline={}
for f in prior['frame_coverage']:
 q=pathlib.Path(f['file']);assert sha(q)==f['sha256'];baseline[f['frame']]={'path':str(q),'sha256':f['sha256'],'RGB_pixels_sha256':pixel(q),'viewing':f['coverage'],'prior_report_sha256':sha(rt/'before'/lang/'prior-complete-selected-review.json.gz')}
for f in audit['frames']:
 q=rt/'before-audit'/lang/f['file'];assert sha(q)==f['sha256'];baseline[f['frame']]={'path':str(q),'sha256':f['sha256'],'RGB_pixels_sha256':f['RGB_pixels_sha256'],'viewing':'direct every encoded frame inspection in preserved before audit','prior_report_sha256':sha(rt/'before-audit'/lang/'review.json')}
selected=sorted(baseline);frames=case/'frames';frames.mkdir(exist_ok=True);assert not list(frames.glob('*.png'))
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',str(movie)]));width,height=probe['streams'][0]['width'],probe['streams'][0]['height'];cmd=['ffmpeg','-v','error','-threads','1','-i',str(movie),'-f','rawvideo','-pix_fmt','rgb24','pipe:1'];proc=subprocess.Popen(cmd,stdout=subprocess.PIPE);frameindex=0;saved=0;chosen=set(selected)
while True:
 raw=proc.stdout.read(width*height*3)
 if not raw:break
 assert len(raw)==width*height*3
 if frameindex in chosen:
  saved+=1;Image.frombytes('RGB',(width,height),raw).save(frames/f'{saved:05d}.png')
 frameindex+=1
assert proc.wait()==0 and saved==len(selected),(saved,len(selected));paths=sorted(frames.glob('*.png'));rows=[]
for frame,p in zip(selected,paths):
 b=baseline[frame];h=pixel(p);equal=h==b['RGB_pixels_sha256'];inwindow=any(w['first_frame']<=frame<=w['last_frame'] for w in audit['windows']);rows.append({'frame':frame,'time':frame/15,'file':str(p.relative_to(case)),'sha256':sha(p),'RGB_pixels_sha256':h,'size':list(Image.open(p).size),'in_reveal_window':inwindow,'baseline':b,'exact_pixel_equal':equal,'viewed':equal,'viewing':'exact RGB inheritance from authenticated actually reviewed baseline' if equal else 'pending direct view'})
# Every changed encoded reveal frame is directly reviewed; exact copies can inherit.
changed=[f for f in rows if not f['viewed']];pages=[]
for n in range(0,len(changed),8):
 group=changed[n:n+8];im=Image.new('RGB',(1280,1576),(18,22,30));draw=ImageDraw.Draw(im)
 for j,f in enumerate(group):
  x=(j%2)*640;y=(j//2)*394;draw.text((x+8,y+7),f"{lang} frame{f['frame']} t={f['time']:.6f}s",fill='white');im.paste(Image.open(case/f['file']).convert('RGB').resize((640,360)),(x,y+34))
 name=f'changed-{n//8+1:03}.png';im.save(case/name);pages.append({'file':name,'sha256':sha(case/name),'frames':[f['frame'] for f in group],'viewed':False,'scale':[640/854,360/480]})
d={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'lang':lang,'scope':'Changed reveal every encoded15fps frame plus prior complete selected-time cohort; exact RGB baseline inheritance only outside changed appearances. No continuous/audio/4K approval.','movie_sha256':expected,'record_sha256':sha(record),'source_sha256':sha(source),'capture_fingerprint':r['fingerprint'],'warnings':r['warnings'],'status':r['status'],'narration_timing_exact_unchanged':True,'input_signatures_exact_unchanged':True,'windows':audit['windows'],'frames':rows,'changed_pages':pages,'native_followups':[],'findings':[],'complete':not changed};(case/'review.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(lang,'cohort',len(rows),'inherited',len(rows)-len(changed),'changed',len(changed),'pages',len(pages),'reveals',sum(f['in_reveal_window'] for f in rows),flush=True)
