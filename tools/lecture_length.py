#!/usr/bin/env python
"""How long a video runs: estimated from its narration before rendering, measured after.

    python tools/lecture_length.py ai26                 # per chapter and total; exit 1 if under the floor
    python tools/lecture_length.py ai26 --floor 30      # the floor in minutes (default 30, the AI series' minimum)
    python tools/lecture_length.py --series ai          # every part of a series, one line each

The estimate counts the words of every ``self.voiceover(...)`` line in the scene source at 140 words a minute (the
narrator's pace, measured on Part 1) and adds the time animations run outside narration (``self.wait`` and the
default 1 s per ``self.play`` outside a voiceover block are ignored: they are small).  Lines built from data
(f-strings) count their literal words plus three per placeholder.  When a render exists, each scene's measured
duration (from its ``.narration.json``) replaces the estimate.
"""

from __future__ import annotations

import ast
import importlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from explainer.paths import VIDEOS, video_dir, video_package  # noqa: E402

WPM = 140
BOOKMARK = re.compile(r"<bookmark[^>]*/>")


def narration_words(path: Path, cls: str) -> int:
    words = 0
    for node in ast.walk(ast.parse(path.read_text())):
        if not (isinstance(node, ast.ClassDef) and node.name == cls):
            continue
        for call in ast.walk(node):
            if not (isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute)
                    and call.func.attr == "voiceover" and call.args):
                continue
            arg = call.args[0]
            for sub in ast.walk(arg):
                if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                    words += len(BOOKMARK.sub(" ", sub.value).split())
                elif isinstance(sub, ast.FormattedValue):
                    words += 3
    return words


def measured(video: str, module: str, cls: str) -> float | None:
    metas = sorted((ROOT / "media" / video / "videos" / module).glob(f"*/{cls}.narration.json"),
                   key=lambda p: p.stat().st_mtime)
    if not metas:
        return None
    try:
        return float(json.loads(metas[-1].read_text())["duration"])
    except (KeyError, ValueError):
        return None


def report(video: str, verbose=True) -> float:
    manifest = importlib.import_module(f"{video_package(video)}.manifest")
    total = 0.0
    rows = []
    for module, cls, chapter in manifest.SCENES:
        src = video_dir(video) / f"{module}.py"
        if not src.exists():  # a chapter still to be written
            rows.append((chapter + "  (not written yet)", 0, 0.0, False))
            continue
        w = narration_words(src, cls)
        m = measured(video, module, cls)
        secs = m if m is not None else 60 * w / WPM
        total += secs
        rows.append((chapter, w, secs, m is not None))
    if verbose:
        for chapter, w, secs, real in rows:
            print(f"  {secs / 60:5.1f} min {'(rendered)' if real else '(estimate)':11s} {w:5d} words  {chapter}")
        print(f"  {total / 60:5.1f} min total  {video}")
    return total / 60


def main():
    args = sys.argv[1:]
    floor = 30.0
    if "--floor" in args:
        i = args.index("--floor")
        floor = float(args[i + 1])
        del args[i:i + 2]
    if "--series" in args:
        series = args[args.index("--series") + 1]
        videos = sorted((p.parent.name for p in (VIDEOS / series).glob("*/manifest.py")),
                        key=lambda n: int(re.sub(r"\D", "", n) or 0))
        short = 0
        for v in videos:
            mins = report(v, verbose=False)
            flag = "" if mins >= floor else "  < floor"
            short += mins < floor
            print(f"{v:10s} {mins:5.1f} min{flag}")
        sys.exit(1 if short else 0)
    mins = report(args[0])
    sys.exit(0 if mins >= floor else 1)


if __name__ == "__main__":
    main()
