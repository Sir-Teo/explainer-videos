#!/usr/bin/env python
"""Check that this machine can render: each video's first scene, silent, at 480p, in English and in Chinese.

    python tools/smoke.py                       # every video
    python tools/smoke.py ai26 analysis1        # just these
    python tools/smoke.py --series ai --lang zh

Renders go to ``media/smoke/<video>/<lang>/``; one line per render, exit status 1 if any failed (the end of its
log is printed).  Chinese renders narrate any untranslated line in English (``EXPLAINER_COLLECT``), so this checks
the toolchain (LaTeX with CJK, fonts, Pango, ffmpeg) rather than translation coverage, which is
``tools/translate_narration.py --check``.  A first scene that needs computed data computes it (once, into .cache).
"""

from __future__ import annotations

import argparse
import importlib
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from explainer.paths import VIDEOS, video_dir, video_package  # noqa: E402


def all_videos(series: str | None) -> list[str]:
    found = sorted(VIDEOS.glob(f"{series or '*'}/*/manifest.py"))
    return [m.parent.name for m in found]


def render(video: str, lang: str) -> tuple[str, str, bool, str]:
    module, cls, _ = importlib.import_module(f"{video_package(video)}.manifest").SCENES[0]
    media = ROOT / "media" / "smoke" / video / lang
    (media / "Tex").mkdir(parents=True, exist_ok=True)
    cfg = media / "smoke.cfg"
    cfg.write_text(f"[CLI]\ntex_dir = {media / 'Tex'}\ntext_dir = {media / 'texts'}\n")
    env = dict(os.environ, EXPLAINER_TTS="silent", EXPLAINER_LANG=lang, EXPLAINER_VIDEO=video,
               EXPLAINER_COLLECT=str(media / "untranslated.jsonl"), PYTHONWARNINGS="ignore")
    src = video_dir(video) / f"{module}.py"
    cmd = [sys.executable, "-m", "manim", "render", "-ql", "-c", str(cfg), "--media_dir", str(media),
           "--progress_bar", "none", str(src), cls]
    t = time.time()
    p = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True)
    mp4 = media / "videos" / module / "480p15" / f"{cls}.mp4"
    ok = p.returncode == 0 and mp4.exists()
    detail = f"{cls}, {time.time() - t:.0f}s" if ok else "\n".join((p.stdout + p.stderr).strip().splitlines()[-25:])
    return video, lang, ok, detail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("videos", nargs="*")
    ap.add_argument("--series", help="only this series (analysis, ai, ...)")
    ap.add_argument("--lang", nargs="*", default=["en", "zh"])
    ap.add_argument("-j", "--jobs", type=int, default=max(1, (os.cpu_count() or 2) // 2))
    args = ap.parse_args()
    videos = args.videos or all_videos(args.series)
    jobs = [(v, lang) for v in videos for lang in args.lang]
    failed = 0
    with ThreadPoolExecutor(args.jobs) as pool:
        for video, lang, ok, detail in pool.map(lambda j: render(*j), jobs):
            print(f"{'ok  ' if ok else 'FAIL'} {video:<16} {lang}  {detail if ok else ''}", flush=True)
            if not ok:
                failed += 1
                print("     " + detail.replace("\n", "\n     "))
    print(f"{len(jobs) - failed}/{len(jobs)} rendered")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
