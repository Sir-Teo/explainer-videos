import subprocess,pathlib,sys,ast
p=pathlib.Path('/workspace/explainer-videos/videos/ai/ai4/manifest.py');m=ast.parse(p.read_text());rows=ast.literal_eval(next(n.value for n in m.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SCENES' for t in n.targets)))
for _,scene,_ in rows[6:]:
 cp=subprocess.run([sys.executable,'/workspace/runtime/ai4-production1080-review/capture_pair.py',scene],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 log=pathlib.Path('/workspace/runtime/ai4-production1080-review')/(scene+'-pair.log');log.write_text(cp.stdout);print(scene,cp.returncode,flush=True)
 if cp.returncode:sys.exit(cp.returncode)
