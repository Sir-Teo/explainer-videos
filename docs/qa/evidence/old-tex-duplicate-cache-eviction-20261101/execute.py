"""Execute the exact parent-approved duplicate-only SVG cache plan, with restore ledger."""
from pathlib import Path
import os, stat, json, gzip, hashlib, shutil, datetime, re, sys, time
R=Path('/workspace/explainer-videos');B=Path('/workspace/runtime/old-tex-capacity-audit');D=B/'duplicate-only-execution'
PLAN=B/'duplicate-only-plan.json.gz';PIN='10d3c4393bd268426d1355366c9dbba0067df5ddb99cc27d8eb085ef217f9883'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(name,obj):
 p=D/name;p.write_text(json.dumps(obj,indent=2)+'\n')
def save_gz(name,obj):
 p=D/name
 with p.open('wb') as f:
  with gzip.GzipFile(fileobj=f,mode='wb',mtime=0) as z:z.write(json.dumps(obj,indent=2).encode())
def signature(p):
 s=p.stat();return dict(bytes=s.st_size,sha256=sha(p),mode=stat.S_IMODE(s.st_mode),mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns,inode=s.st_ino,device=s.st_dev,allocated_bytes=s.st_blocks*512)
def source_inventory():
 paths=set()
 for root in ['explainer','videos','tools','tests']:
  paths.update(p for p in (R/root).rglob('*') if p.is_file() and p.suffix in ['.py','.json'] and '__pycache__' not in p.parts)
 for n in ['pyproject.toml','uv.lock','requirements.txt','manim.cfg']:
  p=R/n
  if p.is_file():paths.add(p)
 H=R/'docs/qa/evidence/production-handoff-parts1-3';paths.update(p for p in H.glob('*') if p.is_file() and p.suffix in ['.py','.json']);paths.update((H/'overlays').glob('*.json'))
 return {str(p):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(paths)}
def activity():
 counts={};matches=[];jobs=[];prefix=tuple(str(R/f'renders/qa/series/ai{i}')+'/' for i in range(3,6))
 def count(k):counts[k]=counts.get(k,0)+1
 for p in Path('/proc').iterdir():
  if not p.name.isdigit():continue
  count('pids_seen');name='unknown'
  try:name=(p/'comm').read_text().strip()
  except (PermissionError,FileNotFoundError,ProcessLookupError):pass
  try:
   args=(p/'cmdline').read_bytes().decode(errors='replace').split('\0');count('argv_readable')
   renderer=any(Path(a).name in ['manim','qa_series.py','qa_scene.py'] for a in args if a)
   if renderer and any(re.search(r'(?:^|/)ai[3-5](?:/|$)',a) for a in args):jobs.append({'pid':p.name,'comm':name})
  except (PermissionError,FileNotFoundError,ProcessLookupError):count('argv_unreadable_or_raced')
  try:
   fds=list((p/'fd').iterdir());count('fd_dirs_readable')
   for fd in fds:
    try:q=os.readlink(fd);count('fd_links_readable')
    except (PermissionError,FileNotFoundError,ProcessLookupError):count('fd_links_unreadable_or_raced');continue
    if q.startswith(prefix) and '/Tex/' in q:matches.append({'pid':p.name,'kind':'fd','path':q})
  except (PermissionError,FileNotFoundError,ProcessLookupError):count('fd_dirs_unreadable_or_raced')
  try:
   maps=(p/'maps').read_text();count('maps_readable')
   for line in maps.splitlines():
    q=line.split()[-1] if line.split() else ''
    if q.startswith(prefix) and '/Tex/' in q:matches.append({'pid':p.name,'kind':'map','path':q})
  except (PermissionError,FileNotFoundError,ProcessLookupError):count('maps_unreadable_or_raced')
 return {'at':now(),'counts':counts,'visible_open_or_mapped_targets':matches,'visible_explicit_old_part_renderers':jobs,'caveat':'Partial host FD/map visibility. Root reconciled all task-owned runners as Part6 and oldPart3–5 idle; no global absence claim.'}
def exact_path(p):
 rel=p.relative_to(R/'renders/qa/series');parts=rel.parts
 assert len(parts)==5 and parts[0] in ['ai3','ai4','ai5'] and parts[1] in ['en','zh'] and parts[3]=='Tex' and p.suffix=='.svg',str(p)
 assert p.resolve()==p and not p.is_symlink() and stat.S_ISREG(p.stat().st_mode),str(p)

assert sha(PLAN)==PIN,'Approved plan hash mismatch'
plan=json.loads(gzip.decompress(PLAN.read_bytes()));rows=plan['candidates'];anchors=plan['anchors'];assert len(rows)==9253 and len(anchors)==6403
remove={r['path'] for r in rows};keep={r['path'] for r in anchors};assert len(remove)==len(rows) and not remove&keep
for row in rows:assert row['retained_byte_exact_svg_anchor'] in keep and row['retained_byte_exact_svg_anchor'] not in remove
act_before=activity();save('activity-before.json',act_before)
assert not act_before['visible_open_or_mapped_targets'] and not act_before['visible_explicit_old_part_renderers'],'Known active oldpart consumer; no deletion begun'
reference=json.loads(Path('/workspace/runtime/capacity-silent-qa-sparse-20261101/receipt.json').read_text())['protected_after'];assert len(reference)==306
protected_before={p:signature(Path(p)) for p in reference};save_gz('protected306-before.json.gz',protected_before)
assert all(protected_before[p]['sha256']==reference[p]['sha256'] and protected_before[p]['bytes']==reference[p]['bytes'] for p in reference),'Protected data differs from historic306 reference; stop'
sources_before=source_inventory();save_gz('source-before.json.gz',sources_before)
inventory=json.loads(gzip.decompress((B/'inventory.json.gz').read_bytes()));tex_paths=[Path(r['path']) for r in inventory['files'] if r['extension']=='.tex'];assert len(tex_paths)==15660
tex_before={str(p):signature(p) for p in tex_paths};save_gz('all-retained-tex-before.json.gz',tex_before)
anchor_before={r['path']:signature(Path(r['path'])) for r in anchors};save_gz('all-anchor-svg-before.json.gz',anchor_before)
for row in anchors:
 exact_path(Path(row['path']));assert anchor_before[row['path']]['sha256']==row['sha256']
restore=[]
for row in rows:
 p=Path(row['path']);a=Path(row['retained_byte_exact_svg_anchor']);t=Path(row['retained_tex_path']);exact_path(p);exact_path(a)
 assert t.suffix=='.tex' and t.parent==p.parent and t.stem==p.stem and not t.is_symlink()
 s=signature(p);assert s['sha256']==row['sha256'] and s['bytes']==row['bytes'] and s['inode']==row['inode'] and s['mtime_ns']==row['mtime_ns'] and s['allocated_bytes']==row['allocated'] and p.stat().st_nlink==1
 assert sha(a)==row['anchor_sha256']==row['sha256'] and sha(t)==row['retained_tex_sha256'] and p.read_bytes()==a.read_bytes()
 restore.append({'path':str(p),'anchor':str(a),'sha256':s['sha256'],'before':s,'atime_ns':p.stat().st_atime_ns,'retained_tex_path':str(t),'retained_tex_sha256':sha(t),'restore':'Copy anchor bytes to missing originalpath; chmod originalmode and utime originalmtime. Recreatedinode/ctime differ. No hardlink.'})
save_gz('full-restore-map.json.gz',restore)
assert sha(PLAN)==PIN and source_inventory()==sources_before,'Source/plan drift before deletion'
free_before=shutil.disk_usage('/workspace').free;started=now();save('preflight.json',{'at':started,'approved_plan_sha256':PIN,'candidates_verified':len(rows),'anchors_verified':len(anchors),'tex_verified':len(tex_paths),'protected306_reference_bytes_identical':True,'source_files':len(sources_before),'free_before':free_before,'parent_authorization':'Only duplicate-only SVG plan; all unique anchors/tex/media/data/models preserved; task-owned oldPart3–5 inactivity reconciled by root.'})
removed=[];skipped=[];stopped=None
progress=D/'deletion-journal.jsonl'
with progress.open('x') as journal:
 for i,(row,meta) in enumerate(zip(rows,restore)):
  if i%250==0:
   if source_inventory()!=sources_before:stopped='Critical source hash drift; remaining entries preserved';break
  if sha(PLAN)!=PIN:stopped='Approved plan changed; remaining entries preserved';break
  p=Path(row['path']);a=Path(row['retained_byte_exact_svg_anchor']);t=Path(row['retained_tex_path'])
  try:
   exact_path(p);exact_path(a);s=signature(p)
   assert s==meta['before'],'Candidate signature drift'
   assert sha(a)==row['anchor_sha256']==row['sha256'] and sha(t)==row['retained_tex_sha256'],'Anchor/source hash drift'
   assert p.read_bytes()==a.read_bytes(),'Bytes no longer exact anchor duplicate'
  except (AssertionError,FileNotFoundError) as e:
   skipped.append({'path':str(p),'reason':str(e) or type(e).__name__});stopped='Entry drift; stopped before unlink and preserved remaining entries';break
  journal.write(json.dumps({'intent_at':now(),**meta})+'\n');journal.flush();os.fsync(journal.fileno())
  p.unlink()
  assert not p.exists();removed.append({'path':str(p),'anchor':str(a),'sha256':meta['sha256'],'allocated_bytes':meta['before']['allocated_bytes']})
  journal.write(json.dumps({'removed_at':now(),'path':str(p),'status':'removed-exact-duplicate-svg-cache'})+'\n');journal.flush()
  if (i+1)%1000==0:print('removed',i+1,'of',len(rows),flush=True)
free_after=shutil.disk_usage('/workspace').free
protected_after={p:signature(Path(p)) for p in reference};sources_after=source_inventory();tex_after={str(p):signature(p) for p in tex_paths};anchor_after={r['path']:signature(Path(r['path'])) for r in anchors}
save_gz('protected306-after.json.gz',protected_after);save_gz('source-after.json.gz',sources_after);save_gz('all-retained-tex-after.json.gz',tex_after);save_gz('all-anchor-svg-after.json.gz',anchor_after)
act_after=activity();save('activity-after.json',act_after)
receipt={'started':started,'finished':now(),'approved_plan_sha256':PIN,'planned':len(rows),'removed':len(removed),'skipped':skipped,'stopped_reason':stopped,'remaining_preserved':len(rows)-len(removed),'removed_allocated_bytes':sum(r['allocated_bytes'] for r in removed),'removed_logical_bytes':sum(m['before']['bytes'] for m in restore[:len(removed)]),'disk_free_before':free_before,'disk_free_after':free_after,'observed_free_space_delta':free_after-free_before,'free_space_caveat':'Concurrent Part6 writes mean wholefilesystem delta may differ from exact removed fileallocation sum. No globally quiescent space claim.','protected306_exact_signatures_unchanged':protected_before==protected_after,'protected306_count':len(reference),'all_current_source_bytes_unchanged':sources_before==sources_after,'source_files':len(sources_before),'all_tex_exact_signatures_unchanged':tex_before==tex_after,'retained_tex_count':len(tex_paths),'all_anchor_exact_signatures_unchanged':anchor_before==anchor_after,'retained_unique_svg_anchor_count':len(anchors),'all_removed_paths_absent':all(not Path(r['path']).exists() for r in removed),'all_removed_restore_anchors_present_exact':all(sha(Path(r['anchor']))==r['sha256'] for r in removed),'partial_activity_visibility_caveat':act_after['caveat'],'no_png_movie_audio_data_model_or_source_mutations_by_executor':True,'removed_files':removed}
save('receipt.json',receipt)
assert receipt['protected306_exact_signatures_unchanged'] and receipt['all_current_source_bytes_unchanged'] and receipt['all_tex_exact_signatures_unchanged'] and receipt['all_anchor_exact_signatures_unchanged']
print(json.dumps({k:v for k,v in receipt.items() if k!='removed_files'},indent=2),flush=True)
