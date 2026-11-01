from pathlib import Path
import sys,shutil,subprocess
sys.path.insert(0,'/workspace/explainer-videos')
from tools.qa_motion import audit
O=Path(__file__).parent
for l in ['en','zh']:
 assert shutil.disk_usage(O).free>768*1024**2
 d=O/l;out=d/'audit';assert not(out/'result.json').exists()
 a=audit(d/'FokkerPlanck.mp4',out,width=320,pixel_delta=8,changed_fraction=.0005,mean_delta=.0001,gap=.2,dense=.25,max_gap=1.)
 print(l,a['analysis']['decoded_frames'],len(a['selected_frames']),flush=True)
subprocess.run([sys.executable,str(O/'compare_decode.py')],check=True)
