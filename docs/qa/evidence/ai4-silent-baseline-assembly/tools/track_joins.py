from pathlib import Path
import sys,json,hashlib,datetime
language,mode=sys.argv[1:3];base=Path('/workspace/runtime/ai4-silent-preview-assembly/current-reviewed')/language/'validation';p=base/'join-review.json';j=json.loads(p.read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat()
if mode=='pages':
 for index in map(int,sys.argv[3:]):
  page=j['pages'][index-1];assert hashlib.sha256(Path(page['path']).read_bytes()).hexdigest()==page['sha256'];page.update(actual_view='actual-chronological-sheet-view',viewed_utc=now)
  if index not in j['actual_pages_viewed']:j['actual_pages_viewed'].append(index)
  for i in page['actual_selected_indices']:j['selected_frames'][i].update(coverage='actual-image-view',proof={'page':page['path'],'page_sha256':page['sha256'],'viewed_utc':now})
 for f in j['selected_frames']:
  if f['coverage']=='pending-exact-duplicate':
   first=j['selected_frames'][f['first_unique_index']]
   if first['coverage']=='actual-image-view':f.update(coverage='exact-PNG-reuse',proof=first['proof'])
elif mode=='native':
 for index in sys.argv[3:]:
  pair=j['native_pairs'][index]
  for role in ('before','after'):assert hashlib.sha256(Path(pair[role]['path']).read_bytes()).hexdigest()==pair[role]['sha256']
  pair.update(actual_view='actual-native854x480-before-after-view',viewed_utc=now)
else:raise ValueError(mode)
j['accounted_for_selected_times']=sum(not f['coverage'].startswith('pending') for f in j['selected_frames']);j['native_pairs_viewed']=sum(x['actual_view']!='pending' for x in j['native_pairs'].values());p.write_text(json.dumps(j,indent=2)+'\n');print(language,j['accounted_for_selected_times'],'/',j['selected_times'],'times;',j['native_pairs_viewed'],'/18nativepairs')
