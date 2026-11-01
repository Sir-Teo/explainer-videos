from pathlib import Path
import datetime,hashlib,json,os,sys,time,shutil
B=Path('/workspace/explainer-videos');O=Path('/workspace/runtime/ai4-silent-preview-assembly/history-qualified');sys.path.insert(0,str(B));lang=sys.argv[1];assert lang in ['en','zh'];base=O/lang;assert not (base/'assembly-progress.json').exists() and not (base/'assembly-receipt.json').exists(),'Reconcile prior build before retry';assert shutil.disk_usage(B).free>=512*1024**2
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[key]='1'
os.environ.update(EXPLAINER_TTS='silent',EXPLAINER_LANG=lang,EXPLAINER_VIDEO='ai4',EXPLAINER_CACHED_ONLY='1')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();stamp=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();fr=O/'input-freeze.json';freeze=json.loads(fr.read_text());inputs=[x for x in freeze['cases'] if x['lang']==lang];assert len(inputs)==19
for c in inputs:
 assert sha(c['frozen_movie'])==c['movie_sha256'] and sha(c['frozen_record'])==c['record_sha256'];assert sha(Path(c['frozen_movie']).with_suffix('.narration.json'))==c['sidecar_sha256']
for x in freeze['source_observations']:assert sha(B/x['path'])==x['sha256']
for rel,x in freeze['raw_inputs'].items():
 p=B/rel
 if x.get('exists') is False:assert not p.exists()
 else:assert sha(p)==x['sha256'] and [p.stat().st_size,p.stat().st_mtime_ns]==[x['bytes'],x['mtime_ns']]
receipt={'scope':'SILENT854x48015fps manual preview assembly; estimated narration/subtitles only, not narrated/production approval. Canonical38reviewclosures parent-attested; original4warningcases retained.','started_utc':stamp(),'lang':lang,'source_commit_observed_at_freeze':freeze['source_commit_observed_at_freeze'],'source_snapshots_are_observations_not_historical_import_proof':True,'input_freeze':str(fr),'input_freeze_sha256':sha(fr),'inputs':inputs,'commands':[],'disk_before':dict(zip(['total','used','free'],shutil.disk_usage(B)))}
save=lambda:(base/'assembly-progress.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n')
from tools import build
original_run=build.run;original_master=build.master_filter;original_title=build.narration_lang.video_title
paths={x['scene']:Path(x['frozen_movie']) for x in inputs}
def threaded(cmd):return [cmd[0],'-nostdin','-threads','1','-filter_threads','1','-filter_complex_threads','1',*cmd[1:]] if cmd[0]=='ffmpeg' else cmd
def tracked_run(cmd,**kw):
 assert shutil.disk_usage(B).free>=512*1024**2
 command=threaded(cmd);receipt['commands'].append({'command':command,'started_utc':stamp()});save()
 try:r=original_run(command,**kw)
 except Exception as e:receipt['commands'][-1].update(status='failed',error=str(e),completed_utc=stamp());save();raise
 receipt['commands'][-1].update(exit_code=r.returncode,completed_utc=stamp(),stderr=r.stderr);save();return r
def tracked_master(cmd):
 command=threaded(cmd);receipt['commands'].append({'command':command,'started_utc':stamp(),'kind':'master-filter-measurement'});save();r=original_master(command);receipt['commands'][-1].update(exit_code=0,completed_utc=stamp(),selected_filter=r);save();return r
build.ROOT=base/'private-build-root';build.ROOT.mkdir();build.run=tracked_run;build.master_filter=tracked_master;build.scene_output=lambda media,module,scene,quality,fps:paths[scene];build.render_scene=lambda *a,**kw:(_ for _ in ()).throw(RuntimeError('Manualsilentassembly forbids rendering'));build.narration_lang.video_title=lambda video,title,lang=None:original_title(video,title,lang)+' [SILENT QA PREVIEW; estimated narration timing]'
sys.argv=['tools/build.py','ai4','-q','l','--fps','15','--lang',lang,'--stitch-only','-j','1'];receipt.update(build_argv=sys.argv,adapter_changes=['privateoutputroot','frozenQAchapterpathlookup','hardrenderprohibition','singlethreadffmpeg+commandreceipts','explicitsilentcontainertitle']);save();started=time.monotonic();build.main();assert not any(n.startswith('videos.ai.ai4.s') or n=='videos.ai.ai4.compute' for n in sys.modules)
produced=build.ROOT/'renders'/('ai4_480p'+('_zh' if lang=='zh' else ''));dest=base/f'ai4-silent-preview-{lang}-480p15'
for ext in ['.mp4','.srt','.chapters.txt']:shutil.copyfile(Path(str(produced)+ext),Path(str(dest)+ext))
for c in inputs:assert sha(c['original_movie'])==c['movie_sha256'] and sha(c['original_record'])==c['record_sha256']
receipt.update(completed_utc=stamp(),assembly_seconds=round(time.monotonic()-started,3),final=str(dest)+'.mp4',final_sha256=sha(str(dest)+'.mp4'),subtitle=str(dest)+'.srt',subtitle_sha256=sha(str(dest)+'.srt'),chapter_list=str(dest)+'.chapters.txt',chapter_list_sha256=sha(str(dest)+'.chapters.txt'),disk_after=dict(zip(['total','used','free'],shutil.disk_usage(B))),scene_and_producer_modules_imported=False);(base/'assembly-receipt.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n');save();print(json.dumps({'lang':lang,'final':receipt['final'],'sha256':receipt['final_sha256'],'seconds':receipt['assembly_seconds']},indent=2))
