import pathlib,json,subprocess,hashlib,sys
from PIL import Image,ImageDraw
lang=sys.argv[1];out=pathlib.Path(__file__).parent/lang;d=json.loads((out/'regression.json').read_text());case=pathlib.Path(d['new_case']);movie=case/'Backprop.mp4';frames=out/'dense-frames';frames.mkdir(exist_ok=True);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ranges={'en':[(111.9,113.4),(124.3,125.8),(136.3,137.8)],'zh':[(118.1,119.6),(131.6,133.1),(141.6,143.1)]}[lang]
probe=['ffprobe','-v','error','-select_streams','v:0','-show_entries','frame=best_effort_timestamp_time','-of','json',str(movie)];pd=json.loads(subprocess.check_output(probe));times=[float(x['best_effort_timestamp_time']) for x in pd['frames']];ids=[i for i,t in enumerate(times) if any(a<=t<=b for a,b in ranges)];expr='+'.join(f'eq(n,{i})' for i in ids);cmd=['ffmpeg','-nostdin','-v','error','-threads','1','-i',str(movie),'-vf',f"select='{expr}'",'-vsync','0','-threads','1',str(frames/'%04d.png')];r=subprocess.run(cmd);assert r.returncode==0
pngs=sorted(frames.glob('*.png'));assert len(pngs)==len(ids);rows=[dict(file=str(p.relative_to(out)),source_frame=i,time=times[i],sha256=sha(p)) for p,i in zip(pngs,ids)];pages=[]
for start in range(0,len(rows),8):
 chunk=rows[start:start+8];page=Image.new('RGB',(1280,390*((len(chunk)+1)//2)),(20,23,32));draw=ImageDraw.Draw(page)
 for j,x in enumerate(chunk):
  a,b=j%2*640,j//2*390;draw.text((a+5,b+5),f"{lang} repaired frame{x['source_frame']} t={x['time']:.6f}",fill='white');page.paste(Image.open(out/x['file']).resize((640,360)),(a,b+30))
 p=out/f'dense-{len(pages)+1:03d}.png';page.save(p);pages.append(dict(file=p.name,sha256=sha(p),frames=chunk))
d['dense_reveal_spans']=dict(ranges=ranges,probe_command=probe,probe_sha256=hashlib.sha256(json.dumps(pd,sort_keys=True).encode()).hexdigest(),command=cmd,exit_code=r.returncode,selected_all_frames_in_ranges=rows,pages=pages,viewed_pages=[],limits='Every encoded source frame in these three bounded spans selected; still frame inspection, not continuous perceptual playback.');(out/'regression.json').write_text(json.dumps(d,indent=2,ensure_ascii=False));print(lang,len(rows),len(pages))
