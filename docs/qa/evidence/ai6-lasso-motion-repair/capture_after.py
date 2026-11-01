from pathlib import Path
import importlib.util,datetime,json,fcntl
P=Path('/workspace/runtime/ai6-remaining-qa-serial/driver.py');spec=importlib.util.spec_from_file_location('serial_qa_owner_adapter',P);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.HOME=Path('/workspace/runtime/ai6-lasso-after-capture');m.HOME.mkdir(exist_ok=True)
approved='dc8391c0e5be2e50bc0c7a318aedf0e5f16f8c6cd329f18baa78d403ad2d5699';table='20635e737d97cfae5cb70af15ee2b4378637b33e5e17f25c2be5906460fe38e3';source='bff5e9b4c58b1baa11492c217cb281faa1c15f8a421838c43d4d4f4d7b9071c9'
lock=(m.HOME/'focused-driver.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
assert not list((m.HOME/'runs').glob('*/**/receipt.json')),'Reconcile completed/uncertain focused runs before retry'
assert m.sha(m.ROOT/'videos/ai/ai6/s05_lasso.py')==source
assert m.source_snapshot()['qa_fingerprint']==approved
assert m.sha(m.TABLE)==table
item=next(i for i in m.inventory() if i['scene']=='Lasso');run=m.HOME/'runs'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S');run.mkdir(parents=True)
m.write(run/'start-gate.json',{'root_approved_source_fingerprint':approved,'root_approved_global_table':table,'root_approved_direct_source':source,'wrapper':str(Path(__file__)),'wrapper_sha256':m.sha(Path(__file__)),'adapter':str(P),'adapter_sha256':m.sha(P),'scope':'Only four Lasso after captures; independent output storage; cache-only silent numeric1 nice10 768MiB; no producer','preserved_baseline':{l:str(Path('/workspace/runtime/ai6-remaining-qa-serial/runs/20261101T055536/05-Lasso')/l) for l in ['en','zh']}})
receipts=[]
try:
 for lang in ['en','zh']:
  for mode in ['endpoints','motion']:
   assert m.source_snapshot()['qa_fingerprint']==approved
   receipts.append(m.run_one(item,lang,mode,run,table,1200));m.write(run/'progress.json',receipts)
except Exception as exc:
 m.write(run/'stop.json',{'error':repr(exc),'completed_passes':len(receipts),'uncertain_must_reconcile':True});raise
m.write(run/'summary.json',{'all_four_runtime_completed':all(r['runtime_completed'] for r in receipts),'receipts':receipts,'visual_acceptance':'pending'});print('FOUR_RUNTIME_CAPTURES_COMPLETED',run,flush=True)
