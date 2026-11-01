import pathlib,json,sys,datetime,hashlib
rt=pathlib.Path(__file__).parent;case=rt/sys.argv[1];p=case/'review.json';d=json.loads(p.read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat();sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for name in sys.argv[2:]:
 if name.startswith('page-'):
  row=next(r for r in d['pages'] if r['file']==name);assert sha(case/name)==row['sha256'];row.update(viewed=True,viewed_utc=now,method='direct declared sheet via view_image original; every populated960x540cell inspected')
  for i in row['frame_indices']:d['frames'][i].update(viewed=True,viewed_page=name,viewed_page_sha256=row['sha256'],scale=[.5,.5])
 else:
  row=next(r for r in d['frames'] if r['file']==name);assert sha(case/name)==row['sha256'];d['native_followups']=[r for r in d['native_followups'] if r['file']!=name]+[{'file':name,'sha256':row['sha256'],'size':[1920,1080],'scale':[1,1],'viewed_utc':now,'method':'direct native1920x1080PNG via view_image original'}]
d['complete']=all(r['viewed'] for r in d['frames']);d['actual_coverage']={'endpoint_frames_viewed':sum(r['viewed'] for r in d['frames']),'pages_viewed':sum(r['viewed'] for r in d['pages']),'native_followups_viewed':len(d['native_followups'])};p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(d['case'],d['actual_coverage'],'complete',d['complete'])
