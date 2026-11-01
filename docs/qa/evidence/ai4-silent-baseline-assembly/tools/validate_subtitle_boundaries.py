from pathlib import Path
import json,re,bisect,hashlib,sys,subprocess,datetime
base=Path(sys.argv[1]);r=json.loads((base/'assembly-receipt.json').read_text());p=base/'validation/final-probe.json';info=json.loads(p.read_text()) if p.exists() else json.loads(subprocess.check_output(['ffprobe','-v','error','-show_chapters','-of','json',r['final']],text=True));chapters=info['chapters'];starts=[float(c['start_time']) for c in chapters]
def secs(x):
 h,m,s=x.replace(',','.').split(':');return int(h)*3600+int(m)*60+float(s)
cues=[]
for block in re.split(r'\n\s*\n',Path(r['subtitle']).read_text().strip()):
 rows=block.splitlines();s,e=rows[1].split(' --> ');s,e=secs(s),secs(e);i=max(0,bisect.bisect_right(starts,s+.001)-1);end=float(chapters[i]['end_time']);assert s>=starts[i]-.0011 and e<=end+.0011,(i,s,e,end);cues.append({'index':int(rows[0]),'chapter_index':i,'start':s,'end':e,'text_sha256':hashlib.sha256('\n'.join(rows[2:]).encode()).hexdigest(),'within_chapter':True})
assert set(c['chapter_index'] for c in cues)==set(range(19));report={'scope':'Independent SRT timestamp parser maps every actualbuilt cue intoembeddedchapterboundaries; no cue crosses chapterboundary beyond1.1ms quantization. Text/timing exact roundtrip throughmov_textvalidatedseparately.','movie_sha256':r['final_sha256'],'cue_count':len(cues),'chapter_count':19,'per_chapter_counts':[sum(x['chapter_index']==i for x in cues) for i in range(19)],'cues':cues,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};(base/'validation/subtitle-boundaries.json').write_text(json.dumps(report,indent=2)+'\n');print(report['cue_count'],'cues allwithin19chapters')
