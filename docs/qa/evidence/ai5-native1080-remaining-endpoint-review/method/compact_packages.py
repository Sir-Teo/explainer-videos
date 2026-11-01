from pathlib import Path
from PIL import Image
import hashlib,json,shutil,datetime
base=Path('/workspace/explainer-videos/docs/qa/evidence');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def manifest(root):
 rows=[{'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':sha(p)}for p in sorted(root.rglob('*'))if p.is_file()and p.name!='manifest.json'];(root/'manifest.json').write_text(json.dumps(rows,indent=2)+'\n');return {'files':len(rows)+1,'bytes':sum(p.stat().st_size for p in root.rglob('*')if p.is_file()),'manifest_sha256':sha(root/'manifest.json')}
r=base/'ai5-silent-candidate-join-review';runtime=Path('/workspace/runtime/ai5-assembly-join-review');oldsha=sha(r/'manifest.json');shutil.copy2(r/'manifest.json',runtime/'package-manifest-before-compaction.json');mapping=[]
for lang in ['en','zh']:
 d=json.loads((runtime/lang/'join-review.json').read_text());keep={3,10,14,25,32}
 for i,pg in enumerate(d['pages'],1):
  original=Path(pg['path']);copy=r/lang/'pages'/pg['file'];assert original.exists()and sha(original)==pg['sha256']==sha(copy)
  joins=sorted({d['selected_frames'][j]['join']for j in pg['actual_selected_indices']})
  mapping.append({'language':lang,'kind':'reviewed-page','page':i,'runtime_original':str(original),'original_png_sha256':pg['sha256'],'joins_represented':joins,'shipped':i in keep,'package_path':str(copy.relative_to(r))if i in keep else None,'tile_width':640,'viewing_scope':'All82pages actually reviewed;10representative actual pages shipped.'})
  if i not in keep:copy.unlink()
 represented=set()
 for x in mapping:
  if x['language']==lang and x['shipped']:represented.update(x['joins_represented'])
 for key,pair in d['native_pairs'].items():
  if pair['actual_view']=='pending':continue
  represented.add(int(key))
  for role in ['before','after']:
   f=pair[role];original=Path(f['path']);copy=r/lang/'native'/f'join-{int(key):02d}-{role}.png';assert sha(original)==f['sha256']==sha(copy)
   mapping.append({'language':lang,'kind':'critical-native-context','join':int(key),'role':role,'runtime_original':str(original),'original_png_sha256':f['sha256'],'shipped':True,'package_path':str(copy.relative_to(r)),'dimensions':[854,480]})
 assert represented==set(range(1,19)),represented
(r/'artifact-map.json').write_text(json.dumps({'created_utc':now,'prior_manifest_sha256':oldsha,'all_runtime_originals_preserved':True,'viewed_pages':82,'shipped_pages':10,'critical_native_images_shipped':44,'all18joins_each_language_represented_by_shipped_page_or_native_context':True,'artifacts':mapping},indent=2)+'\n')
p=r/'README.md';s=p.read_text().replace('All actual reviewed pages and these44native examples are retained, without full movies or data caches.','All82actual reviewed page identities remain in the complete ledgers and all original pages remain in runtime. This bounded package ships10representative actual pages (5per language:3,10,14,25,32) and all44native examples; together these images represent all18joins per language. The artifact map distinguishes viewed versus shipped pages. Redundant package-only page copies were removed only after SHA256 verification against untouched runtime originals. No full movies or data caches are bundled.');s+='\nCompaction preserves the full compressed review/maps/view logs/raw validation/assembly/chapter-warning receipts. All44original native PNG byte streams remain bundled; only redundant page copies were removed. All82runtime pages and every runtime join PNG are untouched.\n';p.write_text(s)
shutil.copy2(Path(__file__),r/'method/compact_packages.py');print('joins',json.dumps(manifest(r)))
r=base/'ai5-native1080-remaining-endpoint-review';runtime=Path('/workspace/runtime/ai5-production1080-remaining-review');oldsha=sha(r/'manifest.json');shutil.copy2(r/'manifest.json',runtime/'package-manifest-before-compaction.json');mapping=[]
for copy in sorted(r.rglob('*.png')):
 rel=copy.relative_to(r);lang,scene=rel.parts[:2];c=runtime/f'{lang}-{scene}'
 if 'native'in rel.parts:original=c/'frames'/copy.name
 elif 'example'in rel.parts:original=c/'pages'/copy.name
 else:original=c/copy.name
 assert original.exists()and sha(original)==sha(copy),(copy,original)
 with Image.open(original)as im:
  assert im.mode in ['RGB','RGBA'];im.load();mode=im.mode;size=im.size;pixels=im.tobytes();pixelsha=hashlib.sha256(pixels).hexdigest();dest=copy.with_suffix('.webp');assert not dest.exists();im.save(dest,format='WEBP',lossless=True,method=3,exact=True)
 with Image.open(dest)as check:
  check=check.convert(mode);assert check.size==size and check.tobytes()==pixels
 mapping.append({'runtime_original':str(original),'original_png_sha256':sha(original),'original_png_bytes':original.stat().st_size,'original_png_package_path_before_compaction':str(rel),'package_encoded_path':str(dest.relative_to(r)),'package_encoded_sha256':sha(dest),'package_encoded_bytes':dest.stat().st_size,'encoding':'lossless-WebP','dimensions':list(size),'decoded_mode':mode,'decoded_pixel_sha256':pixelsha,'decoded_pixel_equality_verified':True,'original_png_bytes_bundled':False})
 copy.unlink()
assert len(mapping)==74,len(mapping)
(r/'artifact-map.json').write_text(json.dumps({'created_utc':now,'prior_manifest_sha256':oldsha,'all_runtime_originals_preserved':True,'critical_original_resolution_images':51,'withdrawal_crops':2,'actual_representative_pages':21,'scope':'Original-resolution content preserved via verified lossless re-encoding; original PNG bytes remain runtime, not this package. Full original timestamps/SHA/viewing ledgers unchanged.','artifacts':mapping},indent=2)+'\n')
p=r/'README.md';s=p.read_text().replace('all51actually inspected original native PNGs, both Brownian crops, one reviewed page per case','all51actually inspected original-resolution native images, both Brownian crops, one reviewed page per case');s+='\n**Lossless package encoding:** the51critical native images,2Brownian crops and21representative pages ship as losslessWebP copies. Each decodedRGB/RGBA pixel buffer and dimensions were checked for exact equality to its unchanged runtime PNG. OriginalPNG bytes are not bundled for these re-encoded assets. `artifact-map.json` records each originalPNG SHA256/runtime path, encodedSHA256/size, dimensions/mode and decodedpixelSHA256. Full original page/frame/viewing ledgers keep their originalPNG identities. All runtime originals are untouched.\n';p.write_text(s)
shutil.copy2(Path(__file__),r/'method/compact_packages.py');print('native21',json.dumps(manifest(r)))
