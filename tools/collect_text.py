#!/usr/bin/env python
"""Record every on-screen string of a video's scenes (dry runs, no frames), for translating the Chinese masters.

    python tools/collect_text.py analysis4 [analysis5 ...]    # -> renders/qa/text/<video>.<Scene>.jsonl
    python tools/collect_text.py --check analysis4             # strings the table leaves in English
    python tools/collect_text.py --lang zh analysis4           # dry-run the Chinese build: TeX and layout asserts
"""

import importlib
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from explainer.paths import video_dir, video_package  # noqa: E402


LANG = sys.argv[sys.argv.index("--lang") + 1] if "--lang" in sys.argv else "en"


def run(video, module, cls, out):
    env = dict(os.environ, EXPLAINER_TTS="silent", EXPLAINER_COLLECT_TEXT=str(out), EXPLAINER_LANG=LANG,
               PYTHONWARNINGS="ignore")
    # its own LaTeX and Text caches: sharing a build's would race with a render of the same scene (see build.py)
    media = ROOT / "media" / video / f"dry_{LANG}"
    cfg = media / "cfg" / f"{cls}.cfg"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    (media / "Tex").mkdir(exist_ok=True)
    cfg.write_text(f"[CLI]\ntex_dir = {media / 'Tex' / cls}\ntext_dir = {media / 'texts' / cls}\n")
    cmd = [sys.executable, "-m", "manim", "render", "-ql", "--dry_run", "--progress_bar", "none",
           "--media_dir", str(media), "-c", str(cfg)]
    r = subprocess.run(cmd + [str(video_dir(video) / f"{module}.py"), cls], cwd=ROOT, env=env,
                       capture_output=True, text=True)
    return cls, r.returncode, r.stderr[-400:]


def check(video):
    """Print every collected string that still shows English words once translated."""
    os.environ["EXPLAINER_LANG"] = "zh"
    from explainer.analysis import zh_text
    seen = {}
    for f in sorted((ROOT / "renders" / "qa" / "text").glob(f"{video}.*.jsonl")):
        for line in f.read_text().splitlines():
            d = json.loads(line)
            if d["needs"]:
                seen.setdefault(d["s"], d)
    done = zh_text._table().get("strings", {})
    left = [s for s, d in seen.items() if s not in done and not re.match(r"Part \d+ \\textperiodcentered|Animated with Manim", s)
            and zh_text.needs_translation(zh_text.translate(s), d["kind"] == "MathTex")]
    for s in left:
        print("  " + json.dumps(s, ensure_ascii=False))
    print(f"{video}: {len(seen)} strings to translate, {len(left)} left")


if sys.argv[1] == "--check":
    for video in sys.argv[2:]:
        check(video)
    sys.exit()

for video in [a for a in sys.argv[1:] if a.startswith("analysis")]:
    out_dir = ROOT / "renders" / "qa" / "text"
    out_dir.mkdir(parents=True, exist_ok=True)
    m = importlib.import_module(f"{video_package(video)}.manifest")
    for f in out_dir.glob(f"{video}.*.jsonl"):
        f.unlink()
    with ThreadPoolExecutor(2) as pool:
        for cls, rc, err in pool.map(lambda s: run(video, s[0], s[1], out_dir / f"{video}.{s[1]}.jsonl"), m.SCENES):
            print(f"  {'ok  ' if rc == 0 else 'FAIL'} {video} {cls}" + ("" if rc == 0 else f"\n{err}"), flush=True)
