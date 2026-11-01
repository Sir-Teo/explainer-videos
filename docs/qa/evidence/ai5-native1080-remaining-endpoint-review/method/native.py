import pathlib,json,sys,datetime,hashlib
c=pathlib.Path(__file__).parent/sys.argv[1];p=json.loads((c/'plan.json').read_text());v=json.loads((c/'views.json').read_text())
for idx in map(int,sys.argv[2].split(',')):
 f=p['frames'][idx];assert not any(x['index']==idx for x in v['native']);fp=c/'frames'/f['file'];assert hashlib.sha256(fp.read_bytes()).hexdigest()==f['sha256']
 v['native'].append({'index':idx,'file':'frames/'+f['file'],'time':f['time'],'sha256':f['sha256'],'size':[1920,1080],'viewed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scale':'original1920x1080','actual_observation':sys.argv[3]})
(c/'views.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');print(c.name,len(v['native']),'natives')
