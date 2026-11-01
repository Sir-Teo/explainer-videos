import pathlib,json,hashlib,shutil,datetime,sys
from PIL import Image,ImageDraw,ImageFont
rt=pathlib.Path(__file__).parent; repo=pathlib.Path('/workspace/explainer-videos');lang,scene=sys.argv[1:];src=repo/'renders/qa/production-endpoints-1080/ai4'/lang/scene;case=rt/f'{lang}-{scene}'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if (case/'review.json').exists():print('already prepared',case);sys.exit()
d=json.loads((src/'result.json').read_text());assert d['status'] in ['passed','needs-review'] and d['mode']=='endpoints';assert d['manual_capture_configuration']['pixel_width']==1920
case.mkdir(exist_ok=True);shutil.copy2(src/'result.json',case/'render-result.json');frames=[]
for i,row in enumerate(d['frames']):
 f=src/row['file'];dst=case/row['file'];shutil.copy2(f,dst);im=Image.open(dst).convert('RGB');assert im.size==(1920,1080)
 frames.append({**row,'index':i,'sha256':sha(dst),'RGB_pixels_sha256':hashlib.sha256(im.tobytes()).hexdigest(),'size':[1920,1080],'viewed':False})
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',19);pages=[]
for start in range(0,len(frames),4):
 chunk=frames[start:start+4];sheet=Image.new('RGB',(1920,1160),(25,25,25));draw=ImageDraw.Draw(sheet)
 for j,row in enumerate(chunk):
  x=(j%2)*960;y=(j//2)*580;im=Image.open(case/row['file']).convert('RGB').resize((960,540),Image.Resampling.LANCZOS);sheet.paste(im,(x,y+40));draw.text((x+10,y+8),f"{lang}-{scene} #{row['index']:03} t={row['time']:.4f}s {row['file']}",font=font,fill='white')
 f=case/f'page-{len(pages)+1:03}.png';sheet.save(f);pages.append({'file':f.name,'sha256':sha(f),'size':list(sheet.size),'frame_indices':[r['index'] for r in chunk],'frame_cell_size':[960,540],'scale':[.5,.5],'viewed':False})
inputs=[]
for name,sig in d['inputs'].items():
 f=repo/name;st=f.stat() if f.exists() else None; actual=[st.st_size,st.st_mtime_ns] if st else None; inputs.append({'path':name,'render_signature':sig,'review_signature':actual,'signature_matches':sig==actual,'sha256':sha(f) if st else None,'exists':bool(st)})
assert all(i['signature_matches'] for i in inputs)
r={'case':f'{lang}-{scene}','scope':'Native1920x1080 silent cached-only skipped-animation endpoint capture; no production motion or listening approval','prepared_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'capture_status':d['status'],'warnings':d['warnings'],'capture_fingerprint':d['fingerprint'],'result_sha256':sha(case/'render-result.json'),'configuration':d['manual_capture_configuration'],'inputs':inputs,'frames':frames,'pages':pages,'native_followups':[],'findings':[],'complete':False}
(case/'review.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(r['case'],len(frames),'frames',len(pages),'pages','warnings',r['warnings'])
