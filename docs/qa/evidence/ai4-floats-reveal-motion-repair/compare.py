import json,pathlib,hashlib,shutil,sys
from PIL import Image,ImageDraw
lang=sys.argv[1];base=pathlib.Path('/workspace/runtime/ai4-mid-head-motion-review')/lang/'Floats';repo=pathlib.Path('/workspace/explainer-videos');out=pathlib.Path(__file__).parent/lang;out.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
cases=[(p,json.loads(p.read_text())) for p in base.glob('*/review-map.json')]
oldp,old=next((p,d) for p,d in cases if d['source_hashes']['videos/ai/ai4/s10_floats.py'].startswith('929bce'))
newp,new=next((p,d) for p,d in cases if d['source_hashes']['videos/ai/ai4/s10_floats.py'].startswith('98288d'))
assert len(old['review']['viewed_pages'])==len(old['pages']);oldpixels={x['pixel_sha256']:x for x in old['frame_mapping']}
maprows=[];novel=[];seen=set()
for i,x in enumerate(new['frame_mapping']):
 inherited=oldpixels.get(x['pixel_sha256']);row=dict(x,selected_index=i,view='inherited-exact-pixels' if inherited else 'pending-new-view')
 if inherited:row['inherited_from']=dict(movie_sha256=old['movie_sha256'],file=inherited['file'],sha256=inherited['sha256'],pixel_sha256=inherited['pixel_sha256'])
 elif x['pixel_sha256'] not in seen:novel.append(row);seen.add(x['pixel_sha256'])
 maprows.append(row)
pages=[]
for start in range(0,len(novel),8):
 chunk=novel[start:start+8];w,h=640,360;page=Image.new('RGB',(2*w,390*((len(chunk)+1)//2)),(20,23,32));draw=ImageDraw.Draw(page)
 for i,x in enumerate(chunk):
  a,b=(i%2)*w,(i//2)*390;draw.text((a+5,b+5),f"{lang} Floats repaired t={x['time']:.6f} source={x['source_frame']}",fill='white');im=Image.open(newp.parent/'audit'/x['file']);page.paste(im.resize((w,h)),(a,b+30))
 p=out/f'novel-{len(pages)+1:03d}.png';page.save(p);pages.append(dict(file=p.name,sha256=sha(p),selected_indices=[x['selected_index'] for x in chunk],times=[x['time'] for x in chunk]))
canonical=repo/'renders/qa/series/ai4'/lang/'Floats';raw=(canonical/'result.json').read_bytes();rd=json.loads(raw);(out/'endpoint-result.json').write_bytes(raw);endpoint_before={'en':'42dc1179ead28e4bb1a12d3abef9182683502644a693ca892a943ade99385f4b','zh':'9ad96a4fe983c2b8658f9346c30fd03642e63fca1908b6d2d5f47b9a61a05c5a'};oldendpoint=pathlib.Path('/workspace/runtime/ai4-mid-head-endpoint-review')/lang/'Floats'/endpoint_before[lang]/'result.json';od=json.loads(oldendpoint.read_text());assert len(rd['frames'])==len(od['frames']);eps=[]
for i,(a,b) in enumerate(zip(rd['frames'],od['frames'])):
 p=canonical/'frames'/a['file'];p=p if p.exists() else canonical/a['file'];q=oldendpoint.parent/b['file'];assert sha(p)==sha(q),(i,p,q);eps.append(dict(index=i,time=a['time'],file=a['file'],sha256=sha(p),inherited_original_file=str(q)));shutil.copy2(p,out/a['file'])
assert (canonical/'result.json').read_bytes()==raw
receipt=dict(language=lang,old_case=str(oldp.parent),old_review_sha256=sha(oldp),new_case=str(newp.parent),new_review_sha256=sha(newp),old_movie_sha256=old['movie_sha256'],new_movie_sha256=new['movie_sha256'],decoded=new['decoded_frames'],selected=len(maprows),inherited_selected=sum(x['view']=='inherited-exact-pixels' for x in maprows),novel_unique=len(novel),mapping=maprows,pages=pages,viewed_pages=[],native_followups=[],endpoint_raw_status=rd['status'],endpoint_raw_warnings=rd['warnings'],endpoint_result_sha256=hashlib.sha256(raw).hexdigest(),endpoints_inherited=eps,raw_motion_status=new['raw_status'],raw_motion_warnings=new['raw_warnings'],limits=new['limits'])
(out/'regression.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False));print(json.dumps({k:receipt[k] for k in ['language','decoded','selected','inherited_selected','novel_unique','new_movie_sha256']},indent=2));print('pages',len(pages),'endpoints',len(eps))
