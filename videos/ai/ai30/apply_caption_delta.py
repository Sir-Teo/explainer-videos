"""Merge only the owned delta into a newer table; dry-run unless --write is given."""
from pathlib import Path
import argparse,copy,fcntl,json,os,tempfile

def merge(table, delta):
 result=copy.deepcopy(table);conflicts=[];changed=0
 for op in delta['strings']:
  key=op['key'];present=key in result['strings'];value=result['strings'].get(key)
  candidate_ok=present==op['candidate_present'] and (not present or value==op['candidate_value'])
  baseline_ok=present==op['baseline_present'] and (not present or value==op['baseline_value'])
  if candidate_ok:continue
  if not baseline_ok:conflicts.append({'kind':'string','key':key});continue
  if op['candidate_present']:result['strings'][key]=op['candidate_value']
  else:result['strings'].pop(key,None)
  changed+=1
 for entry in delta.get('patterns_remove',[]):
  same=[p for p in result['patterns'] if p[0]==entry[0]]
  if not same:continue
  if same!=[entry]:conflicts.append({'kind':'pattern-remove','key':entry[0]});continue
  result['patterns'].remove(entry);changed+=1
 for entry in delta.get('patterns_add',[]):
  same=[p for p in result['patterns'] if p[0]==entry[0]]
  if same==[entry]:continue
  if same:conflicts.append({'kind':'pattern-add','key':entry[0]});continue
  result['patterns'].append(entry);changed+=1
 if conflicts:raise ValueError(json.dumps({'conflicts':conflicts},ensure_ascii=False))
 return result,changed

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('delta',type=Path);p.add_argument('table',type=Path);p.add_argument('--write',action='store_true');a=p.parse_args();delta=json.loads(a.delta.read_text())
 if not a.write:
  _,changed=merge(json.loads(a.table.read_text()),delta);print(json.dumps({'mode':'dry-run','changes':changed,'unrelated_entries':'preserved'}));return
 # Same lock as repository tools/text_zh_add.py; resolve every conflict before writing.
 with a.table.with_suffix('.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX);result,changed=merge(json.loads(a.table.read_text()),delta)
  with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=a.table.parent,prefix='ai30-caption-',suffix='.tmp',delete=False) as out:
   json.dump(result,out,ensure_ascii=False,indent=2);out.write('\n');temporary=Path(out.name)
  os.chmod(temporary,a.table.stat().st_mode & 0o777)
  try:os.replace(temporary,a.table)
  finally:temporary.unlink(missing_ok=True)
 print(json.dumps({'mode':'written','changes':changed,'unrelated_entries':'preserved'}))

if __name__=='__main__':main()
