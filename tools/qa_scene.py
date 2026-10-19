#!/usr/bin/env python
"""Render one chapter silently at 480p15 and make its contact sheet: the quick look while writing a scene.

    python tools/qa_scene.py ai27 SFT                   # -> renders/qa/ai27/SFT_en.png (and the .mp4 path)
    python tools/qa_scene.py ai27 SFT --lang zh -n 32

The render goes to media/<video>/qa_<lang>/ with its own TeX and text caches, so it never races a build.
"""

import argparse
import importlib
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from explainer.paths import video_dir, video_package  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("scene", help="scene class, as in the manifest")
    ap.add_argument("--lang", default="en")
    ap.add_argument("-n", type=int, default=24, help="frames on the contact sheet")
    ap.add_argument("-c", "--cols", type=int, default=4)
    ap.add_argument("-o", help="contact sheet path (default renders/qa/<video>/<scene>_<lang>.png)")
    args = ap.parse_args()
    manifest = importlib.import_module(f"{video_package(args.video)}.manifest")
    module = next((m for m, cls, _ in manifest.SCENES if cls == args.scene), None)
    if module is None:
        sys.exit(f"{args.scene} is not in {args.video}'s manifest")
    media = ROOT / "media" / args.video / f"qa_{args.lang}"
    cfg = media / "cfg" / f"{args.scene}.cfg"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(f"[CLI]\ntex_dir = {media / 'Tex' / args.scene}\ntext_dir = {media / 'texts' / args.scene}\n")
    log = ROOT / "renders" / "qa" / args.video / f"{args.scene}_{args.lang}.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, EXPLAINER_TTS="silent", EXPLAINER_LANG=args.lang, EXPLAINER_VIDEO=args.video,
               PYTHONWARNINGS="ignore")
    cmd = [sys.executable, "-m", "manim", "render", "-ql", "-c", str(cfg), "--media_dir", str(media),
           "--progress_bar", "none", str(video_dir(args.video) / f"{module}.py"), args.scene]
    with open(log, "w") as f:
        rc = subprocess.run(cmd, cwd=ROOT, env=env, stdout=f, stderr=subprocess.STDOUT).returncode
    if rc:
        lines = [x for x in log.read_text().splitlines() if x.strip()]
        print("\n".join(lines[-30:]))
        sys.exit(f"render failed (log: {log.relative_to(ROOT)})")
    mp4 = media / "videos" / module / "480p15" / f"{args.scene}.mp4"
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)],
                         capture_output=True, text=True).stdout.strip()
    out = Path(args.o) if args.o else log.with_suffix(".png")
    subprocess.run([sys.executable, str(ROOT / "tools" / "contact_sheet.py"), str(mp4), "-n", str(args.n), "-c",
                    str(args.cols), "-o", str(out)], cwd=ROOT, check=True, capture_output=True)
    print(f"{args.scene} ({args.lang}): {float(dur):.0f} s\n  video {mp4.relative_to(ROOT)}\n  sheet {out}")


if __name__ == "__main__":
    main()
