import pathlib,json,hashlib,sys,datetime
from PIL import Image,ImageDraw
rt=pathlib.Path(__file__).parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();pixel=lambda p:hashlib.sha256(Image.open(p).convert('RGB').tobytes()).hexdigest()
for case in sys.argv[1:]:
 p=rt/case;before=json.loads((p/'before/review.json').read_text());r=json.loads((p/'after/render-result.json').read_text());rows=[]
 for i,f in enumerate(r['frames']):
  q=p/'after'/f['file'];s=sha(q);h=pixel(q);size=list(Image.open(q).size);assert size==[1920,1080];matches=[o for o in before['frames'] if abs(o['time']-f['time'])<1e-9 and o['viewed'] and (s==o['sha256'] or h==o['RGB_pixels_sha256'])];o=matches[0] if matches else None
  rows.append({'index':i,'file':f['file'],'time':f['time'],'reason':f['reason'],'sha256':s,'RGB_pixels_sha256':h,'size':size,'baseline':None if not o else {'file':o['file'],'time':o['time'],'sha256':o['sha256'],'RGB_pixels_sha256':o['RGB_pixels_sha256'],'viewed_page':o['viewed_page'],'viewed_page_sha256':o['viewed_page_sha256']},'byte_equal':bool(o and s==o['sha256']),'pixel_equal':bool(o and h==o['RGB_pixels_sha256']),'viewed':bool(o),'method':'exact timestamp + exact bytes/pixels inherited from actually reviewed original' if o else 'pending direct review'})
 changed=[x for x in rows if not x['viewed']];pages=[]
 for n in range(0,len(changed),4):
  group=changed[n:n+4];canvas=Image.new('RGB',(1920,1160),(24,24,24));draw=ImageDraw.Draw(canvas)
  for j,f in enumerate(group):
   x=(j%2)*960;y=(j//2)*580;draw.text((x+8,y+8),f"{case} #{f['index']} t={f['time']:.6f} {f['file']}",fill='white');canvas.paste(Image.open(p/'after'/f['file']).convert('RGB').resize((960,540)),(x,y+40))
  name=f'changed-page-{n//4+1:03}.png';canvas.save(p/name);pages.append({'file':name,'sha256':sha(p/name),'frame_indices':[f['index'] for f in group],'viewed':False,'scale':[.5,.5]})
 unmatched=[o['file'] for o in before['frames'] if not any(abs(o['time']-f['time'])<1e-9 for f in rows)];d={'case':case,'scope':'Native1080 skipped-animation settled endpoints; exact inherited viewing only; no continuous/motion/audio approval','before_result_sha256':sha(p/'before/render-result.json'),'before_review_sha256':sha(p/'before/review.json'),'after_result_sha256':sha(p/'after/render-result.json'),'after_warnings':r['warnings'],'frames':rows,'changed_pages':pages,'old_timestamps_absent_from_new':unmatched,'native_followups':[],'complete':all(x['viewed'] for x in rows)};(p/'comparison.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(case,'fresh',len(rows),'inherited',len(rows)-len(changed),'changed',len(changed),'oldtimesabsent',len(unmatched),'pages',len(pages))
