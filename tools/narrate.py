#!/usr/bin/env python
"""Synthesize a video's narration into the TTS cache before rendering it (speech on the GPU, renders on the CPU).

    EXPLAINER_TTS=server EXPLAINER_VOICE=qwen3-calm-a python tools/narrate.py analysis1 [--lang zh]
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--only", nargs="*", help="only these scene classes")
    args = ap.parse_args()
    os.environ["EXPLAINER_LANG"] = args.lang  # read when explainer.lang is imported

    from explainer import lang, tts
    from explainer.voiceover import _strip_bookmarks
    from tools.translate_narration import english_lines

    video_dir = ROOT / "videos" / args.video
    lines = [(cls, raw) for cls, raw in english_lines(args.video) if not args.only or cls in args.only]
    t0, made, audio = time.time(), 0, 0.0
    for i, (cls, raw) in enumerate(lines, 1):
        clean, _ = _strip_bookmarks(lang.translate(raw, video_dir, cls))
        t = time.time()
        utt = tts.synthesize(clean)
        fresh = time.time() - t > 1.0
        made += fresh
        audio += utt.duration
        print(f"[{i:3d}/{len(lines)}] {cls:<22} {utt.duration:6.1f}s {'new' if fresh else 'cached':6} "
              f"{time.time() - t:6.0f}s  {clean[:50]}", flush=True)
    print(f"{args.video} ({args.lang}): {len(lines)} lines, {made} synthesized, {audio / 60:.1f} min of narration "
          f"in {(time.time() - t0) / 60:.1f} min")


if __name__ == "__main__":
    main()
