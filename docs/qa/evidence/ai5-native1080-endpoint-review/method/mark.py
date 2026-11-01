import pathlib,json,sys,datetime,hashlib
b=pathlib.Path(__file__).parent;c=b/sys.argv[1];lo=int(sys.argv[2]);hi=int(sys.argv[3]);note=sys.argv[4]
p=json.loads((c/'plan.json').read_text());v=json.loads((c/'views.json').read_text())
for pg in p['pages']:
 if lo<=pg['page']<=hi:
  assert not any(x['page']==pg['page'] for x in v['pages'])
  assert hashlib.sha256((c/pg['file']).read_bytes()).hexdigest()==pg['sha256']
  v['pages'].append({**pg,'viewed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_observation':note,'review_scale':'960x540 per native1920x1080 endpoint'})
(c/'views.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
print(c.name,len(v['pages']),'pages viewed')
