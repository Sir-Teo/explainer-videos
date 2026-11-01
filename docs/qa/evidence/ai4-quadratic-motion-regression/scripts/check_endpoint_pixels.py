from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
R=Path(__file__).parent;reports=json.loads((R/'endpoint-comparison.json').read_text());anchors=[[-1,0],[1,0],[-2,0],[2,0],[-4,0],[4,0],[-3.2,-.48],[-3.2,.48]];pixels=np.array([[427+66*x,276-110*y] for x,y in anchors]);rows=[]
for case in reports:
 for row in case['rows']:
  old=np.asarray(Image.open(row['old_file']).convert('RGB'));new=np.asarray(Image.open(row['new_file']).convert('RGB'));ys,xs=np.nonzero(np.any(old!=new,axis=2));points=np.column_stack([xs,ys]);dist=np.linalg.norm(points[:,None,:]-pixels[None,:,:],axis=2) if len(points) else np.empty((0,8));nearest=dist.argmin(axis=1) if len(points) else []
  if len(points):
   assert row['index'] in [5,6,7,8]
   near=dist.min(axis=1)<8
   other=points[~near]
   if len(other):
    assert row['index'] in [6,7,8]
    assert np.all((other[:,0]>=410)&(other[:,0]<=437)&(other[:,1]>=267)&(other[:,1]<=285))
    delta=np.abs(old.astype(int)-new.astype(int));assert max(delta[y,x].max() for x,y in other)==1
  rows.append({'lang':case['lang'],'endpoint_index':row['index'],'different_pixels':len(points),'all_differences_within8px_of8_repaired_contour_vertices':bool(not len(points) or np.all(dist.min(axis=1)<8)),'final_dot_only_one_channel_unit_exception_pixels':int(sum(dist.min(axis=1)>=8)) if len(points) else 0,'per_vertex_pixel_counts':[int(sum(nearest==i)) for i in range(8)] if len(points) else [0]*8,'max_contour_local_distance_px':float(dist.min(axis=1)[dist.min(axis=1)<8].max()) if len(points) else 0})
d={'scope':'Exact native854x480 RGB comparison, no image rescaling/threshold/perceptual equivalence. Source-matched axes map8 repaired interior vertices to pixel centers;16 restored incident segments (two per vertex). The bare-contour capture changes144pixels only at these8vertices. Later held valley captures also have2/10/8pixels near finaldots, eachmax8-bit channel delta1; separately qualified as raster rounding, never exactpixelidentity. Allother pixels exact. This is pixel localization, not a new numerical contour producer run.','anchors_data':anchors,'anchors_pixels':pixels.tolist(),'source_plot_mapping':'native854x480; axes at worldcenter(0,-.6),xlength11/range10,y_length4.4/range2.4;60pixels/worldunit','rows':rows,'unchanged_endpoints':sum(x['different_pixels']==0 for x in rows),'valley_changed_endpoints':sum(x['different_pixels']>0 for x in rows)};(R/'endpoint-pixel-localization.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps({k:v for k,v in d.items() if k!='rows'},indent=2))
B=Path('/workspace/explainer-videos');data=B/'.cache/ai4/valley.npz';before=hashlib.sha256(data.read_bytes()).hexdigest();out=[]
with np.load(data,allow_pickle=False) as z:
 for name,duration in [('gd',3.5),('momentum',3.0),('newton',1.0)]:
  q=z[name]*np.array([1.1,4.4/2.4]);lengths=np.linalg.norm(np.diff(q,axis=0),axis=1);cum=np.cumsum(lengths);total=float(cum[-1]);n=len(lengths);out.append({'name':name,'vertices':len(q),'original_duration':duration,'rate_function':'smooth' if name=='newton' else 'linear','old_visible_prefix_progress':'uniform curve-index, equal animationtime per measuredsegment','new_progress':'uniform on-screen arc length after unchanged external ratefunction','first_corner_old_linear_time':duration/n,'first_corner_new_linear_time':duration*float(cum[0])/total,'all_corner_old_linear_times':(duration*np.arange(1,n+1)/n).tolist(),'all_corner_new_linear_times':(duration*cum/total).tolist(),'note':'Newton has one segment; unchanged smoothexternalrate. GD/momentum spend proportionally more time on long earlysegments and less on tiny finalsegments; iteration-time pacing is deliberately not preserved.'})
assert hashlib.sha256(data.read_bytes()).hexdigest()==before;(R/'pacing-choice.json').write_text(json.dumps({'cache_sha256':before,'rows':out,'scope':'Raw immutablecachedvertices with source-matched linearaxis scaling; no scene/producer/model imports or data mutation.'},indent=2)+'\n');print('pacing',[(x['name'],x['first_corner_old_linear_time'],x['first_corner_new_linear_time']) for x in out])
