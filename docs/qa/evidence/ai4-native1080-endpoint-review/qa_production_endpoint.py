"""Private manual 1080p endpoint capture; no CI, no narrated/full-motion claim."""
from pathlib import Path
from types import SimpleNamespace
import hashlib
import json
import shutil
import sys
from PIL import Image
import manim

ROOT = Path("/workspace/explainer-videos")
sys.path.insert(0, str(ROOT))
from tools import qa_series

part, lang, scene = sys.argv[1:]
original_out = qa_series.OUT
qa_series.OUT = ROOT / "renders/qa/production-endpoints-1080"
folder = qa_series.OUT / part / lang / scene
(folder / "Tex").mkdir(parents=True, exist_ok=True)
for source in (original_out / part / lang / scene / "Tex").glob("*.svg"):
    shutil.copy2(source, folder / "Tex" / source.name)
original_config = manim.tempconfig

def production_config(options):
    config = dict(options, quality="high_quality", pixel_width=1920, pixel_height=1080, frame_rate=30)
    return original_config(config)

manim.tempconfig = production_config
status = qa_series.worker(SimpleNamespace(video=part, lang=lang, worker=scene, motion=False, cached_only=True))
record_path = folder / "result.json"
record = json.loads(record_path.read_text())
sizes = {Image.open(folder / frame["file"]).size for frame in record["frames"]}
assert sizes == {(1920, 1080)}, sizes
record["manual_capture_configuration"] = dict(pixel_width=1920, pixel_height=1080, nominal_frame_rate=30,
    animations="skipped endpoint evaluation", audio="silent placeholders", source_inputs="cached-only",
    wrapper_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    interpretation="Native production-resolution endpoint images only; no full production movie or listening approval")
record_path.write_text(json.dumps(record, ensure_ascii=False, indent=1))
print(json.dumps(dict(part=part, lang=lang, scene=scene, status=record["status"], frames=len(record["frames"]),
                      warnings=record["warnings"], pixel_sizes=[list(size) for size in sizes])))
sys.exit(status)
