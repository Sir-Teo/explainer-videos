"""Read-only full-file/PTS/subtitle/chapter QA; optional join frame extraction."""
from pathlib import Path
import argparse,csv,datetime,gzip,hashlib,json,re,subprocess,time
ap=argparse.ArgumentParser();ap.add_argument('base',type=Path);ap.add_argument('--interim',action='store_true');ap.add_argument('--full',action='store_true');args=ap.parse_args();base=args.base;receipt=json.loads((base/'assembly-receipt.json').read_text());movie=Path(receipt['final']);out=base/('interim-validation' if args.interim else 'validation');out.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();commands=[]
def run(cmd):
 start=time.monotonic();p=subprocess.run(cmd,check=True,capture_output=True,text=True);commands.append(dict(command=cmd,seconds=round(time.monotonic()-start,3),exit_code=p.returncode,stderr=p.stderr));return p.stdout
def probe(path):return json.loads(run(['ffprobe','-v','error','-show_streams','-show_chapters','-show_format','-of','json',str(path)]))
def cues(path):
 text=Path(path).read_text();out=[]
 def seconds(s):h,m,x=s.replace(',','.').split(':');return int(h)*3600+int(m)*60+float(x)
 for block in re.split(r'\n\s*\n',text.strip()):
  lines=block.splitlines();m=re.fullmatch(r'(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)',lines[1]);assert m;out.append((seconds(m[1]),seconds(m[2]),'\n'.join(lines[2:])))
 return out
assert sha(movie)==receipt['final_sha256'];info=probe(movie);(out/'final-probe.json').write_text(json.dumps(info,indent=2)+'\n');v=next(s for s in info['streams'] if s['codec_type']=='video');a=next(s for s in info['streams'] if s['codec_type']=='audio');sub=next(s for s in info['streams'] if s['codec_type']=='subtitle');assert (v['codec_name'],v['width'],v['height'],v['r_frame_rate'])==('h264',854,480,'15/1');assert (a['codec_name'],a['sample_rate'],a['channels'])==('aac','48000',2);assert sub['codec_name']=='mov_text';assert sub['tags']['language']==('eng' if receipt['lang']=='en' else 'chi');assert 'SILENT QA PREVIEW' in info['format']['tags']['title'];assert len(info['chapters'])==19
work=base/'private-build-root/media'/('ai4' if receipt['lang']=='en' else 'ai4_zh')/'stitch';chapters=[];offset=0.;expected_frames=0;chapter_lines=Path(receipt['chapter_list']).read_text().splitlines();assert len(chapter_lines)==19
for item,chapter in zip(receipt['inputs'],info['chapters']):
 normalized=work/(item['scene']+'.mp4');p=probe(normalized);vp=next(s for s in p['streams'] if s['codec_type']=='video');source=Path(item['frozen_movie']);assert sha(source)==item['movie_sha256'];source_probe=probe(source);source_v=next(s for s in source_probe['streams'] if s['codec_type']=='video');n=int(vp['nb_frames']);assert n==int(source_v['nb_frames']);assert all(vp[k]==source_v[k] for k in ('codec_name','width','height','r_frame_rate','time_base'));duration=float(p['format']['duration']);assert abs(float(chapter['start_time'])-offset)<.002;assert float(chapter['end_time'])>=float(chapter['start_time']);assert chapter['tags']['title']==chapter_lines[item['index']].split(' ',1)[1];chapters.append(dict(index=item['index'],scene=item['scene'],start=offset,container_duration=duration,video_frames=n,first_frame=expected_frames,metadata_title=chapter['tags']['title'],normalized_sha256=sha(normalized),original_movie_sha256=item['movie_sha256']));expected_frames+=n;offset+=duration
assert int(v['nb_frames'])==expected_frames;assert abs(float(info['format']['duration'])-offset)<.067;assert abs(float(info['chapters'][-1]['end_time'])-offset)<.002
original=cues(receipt['subtitle']);assert original;assert all(0<=s<=e<=float(info['format']['duration'])+.001 for s,e,_ in original);assert all(x[1]<=y[0]+.001 for x,y in zip(original,original[1:]));soft=out/'extracted-soft-subtitles.srt';run(['ffmpeg','-v','error','-y','-i',str(movie),'-map','0:s:0','-c:s','srt',str(soft)]);extracted=cues(soft);assert len(extracted)==len(original);assert all(x[2]==y[2] and abs(x[0]-y[0])<=.0011 and abs(x[1]-y[1])<=.0011 for x,y in zip(original,extracted))
review=dict(scope='INTERIM mechanism evidence: old GaLore, not current preview' if args.interim else 'Full silent-preview assembly checks, not narrated or1080p approval',started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),language=receipt['lang'],movie=str(movie),movie_sha256=sha(movie),duration=float(info['format']['duration']),video_frames=expected_frames,chapter_count=19,chapter_duration_sum=offset,subtitle_cues=len(original),soft_subtitles_exact_text_and_millisecond_timing=True,chapters=chapters,commands=commands,full_decode=False,join_visual_review='pending',audio_listening=False,continuous_perceptual_playback=False)
if args.full:
 raw=run(['ffprobe','-v','error','-err_detect','explode','-threads','1','-select_streams','v:0','-show_frames','-show_entries','frame=best_effort_timestamp_time,pkt_dts_time,pkt_duration_time,key_frame','-of','json',str(movie)]);(out/'video-frame-times.json.gz').write_bytes(gzip.compress(raw.encode(),mtime=0));frames=json.loads(raw)['frames'];assert len(frames)==expected_frames;pts=[float(f['best_effort_timestamp_time']) for f in frames];assert all(y>x for x,y in zip(pts,pts[1:]));assert not commands[-1]['stderr'];review.update(full_decode=True,decoded_frames=len(frames),first_pts=pts[0],last_pts=pts[-1],minimum_frame_gap=min(y-x for x,y in zip(pts,pts[1:])),maximum_frame_gap=max(y-x for x,y in zip(pts,pts[1:])))
 raw=run(['ffprobe','-v','error','-show_packets','-show_entries','packet=stream_index,pts_time,dts_time,duration_time','-of','json',str(movie)]);(out/'packet-times.json.gz').write_bytes(gzip.compress(raw.encode(),mtime=0));packets=json.loads(raw)['packets'];streams={}
 for p in packets:
  if 'dts_time'in p:streams.setdefault(p['stream_index'],[]).append(float(p['dts_time']))
 assert all(all(y>=x for x,y in zip(ts,ts[1:])) for ts in streams.values());review['packet_dts_monotonic']={k:dict(packets=len(t),first=t[0],last=t[-1]) for k,t in streams.items()}
 joins=[];selection={}
 for chapter in chapters[1:]:
  boundary=chapter['first_frame'];join=dict(index=chapter['index'],incoming_scene=chapter['scene'],outgoing_scene=chapters[chapter['index']-1]['scene'],boundary_frame=boundary,chapter_marker_time=chapter['start'],first_incoming_pts=pts[boundary],marker_vs_frame_delta=pts[boundary]-chapter['start'],frames=[]);assert abs(join['marker_vs_frame_delta'])<=1/15
  for delta in [-15,-12,-9,*range(-6,7),9,12,15]:
   i=boundary+delta;assert 0<=i<len(frames);name=f'frame-{i:07d}.png';selection[i]=name;join['frames'].append(dict(relative_frame=delta,source_frame=i,time=pts[i],relative_time=pts[i]-pts[boundary],file=name,actual_view='pending'))
  joins.append(join)
 folder=out/'join-frames';folder.mkdir(exist_ok=True)
 terms=[f'eq(n\\,{n})' for n in sorted(selection)]
 while len(terms)>1:terms=[f'({terms[i]}+{terms[i+1]})' if i+1<len(terms) else terms[i] for i in range(0,len(terms),2)]
 select=terms[0]
 run(['ffmpeg','-v','error','-xerror','-threads','1','-i',str(movie),'-map','0:v:0','-an','-sn','-filter_threads','1','-vf',f'select={select}','-vsync','0','-threads','1',str(folder/'selected-%05d.png')]);images=sorted(folder.glob('selected-*.png'));assert len(images)==len(selection)
 for (index,name),p in zip(sorted(selection.items()),images):p.rename(folder/name)
 for join in joins:
  for f in join['frames']:p=folder/f['file'];f.update(path=str(p),sha256=sha(p))
 (out/'join-selection.json').write_text(json.dumps({'scope':'All18joins; every frame within±0.4s plus±0.6/0.8/1.0s; not continuous full-part review','joins':joins},indent=2)+'\n');review['join_count']=len(joins);review['join_selected_frames']=len(selection)
review['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();(out/'validation.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in review.items() if k not in ('chapters','commands')},indent=2))
