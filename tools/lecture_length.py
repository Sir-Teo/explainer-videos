#!/usr/bin/env python
"""How long a video runs: estimated from its narration before rendering, measured after.

    python tools/lecture_length.py ai26                 # per chapter and total; exit 1 if under the floor
    python tools/lecture_length.py ai26 --floor 30      # the floor in minutes (default 30; 50 for Computer Science, Built)
    python tools/lecture_length.py music1               # Music, Built: listening counted, and a ceiling of 60
    python tools/lecture_length.py --series ai          # every part of a series, one line each

The estimate counts the words of every ``self.voiceover(...)`` line in the scene source at the series' pace (140
words a minute for the AI series, measured on Part 1; 168 for *Quant, Built*, measured on its rendered Parts 1 and
10, whose CPU voice is faster) and adds the time animations run outside narration (``self.wait`` and the
default 1 s per ``self.play`` outside a voiceover block are ignored: they are small).  Lines built from data
(f-strings) count their literal words plus three per placeholder.  When a render exists, each scene's measured
duration (from its ``.narration.json``) replaces the estimate, unless the scene's source is newer than that render
(a rewritten chapter is estimated again until it is re-rendered).

*Music, Built* has stretches with no narration at all: the listening windows.  A rendered chapter's duration includes
them.  An estimated chapter adds the windows of its last cue sheet (``<Scene>.cues.json``, written by any render, even
a stale one), and a chapter never rendered adds the clips its source names, from the part's clip store.  The series
also has a ceiling (60 minutes): exit 1 above it as well as below the floor.
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
SERIES_WPM = {"quant": 168}
FLOORS = {"cs": 50.0}  # minutes; other series: 30
CEILINGS = {"music": 60.0}  # minutes; other series: none
CLIP_NAME = re.compile(r'clip\(f?"([a-z_0-9]+\.[a-z_0-9]+)"\)')


def wpm(video: str) -> float:
    return SERIES_WPM.get(video_dir(video).parent.name, WPM)

BOOKMARK = re.compile(r"<bookmark[^>]*/>")


def narration_words(path: Path, cls: str) -> int:
    words = 0
    for node in ast.walk(ast.parse(path.read_text())):
        if not (isinstance(node, ast.ClassDef) and node.name == cls):
            continue
        for call in ast.walk(node):
            if not (isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute)
                    and (call.func.attr == "voiceover" or call.func.attr.endswith("_voiceover")) and call.args):
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
    src = video_dir(video) / f"{module}.py"
    if src.exists() and src.stat().st_mtime > metas[-1].stat().st_mtime:
        return None  # the chapter changed since it was rendered
    try:
        return float(json.loads(metas[-1].read_text())["duration"])
    except (KeyError, ValueError):
        return None


def listening(video: str, module: str, cls: str) -> tuple[float, bool]:
    """Seconds of listening windows in a scene, and whether a cue sheet said so (otherwise the clip store did)."""
    sheets = sorted((ROOT / "media" / video / "videos" / module).glob(f"*/{cls}.cues.json"),
                    key=lambda p: p.stat().st_mtime)
    if sheets:
        cues = json.loads(sheets[-1].read_text())["cues"]
        return sum(c["duration"] for c in cues if c.get("window") and not c.get("underscore")), True
    store = ROOT / ".cache" / video / "audio"
    total = 0.0
    for name in set(CLIP_NAME.findall((video_dir(video) / f"{module}.py").read_text())):
        meta = store / f"{name}.json"
        if meta.exists():
            total += float(json.loads(meta.read_text()).get("duration", 0.0))
    return total, False


def report(video: str, verbose=True) -> float:
    manifest = importlib.import_module(f"{video_package(video)}.manifest")
    total = heard_all = 0.0
    rows = []
    for module, cls, chapter in manifest.SCENES:
        src = video_dir(video) / f"{module}.py"
        if not src.exists():  # a chapter still to be written
            rows.append((chapter + "  (not written yet)", 0, 0.0, False))
            continue
        w = narration_words(src, cls)
        m = measured(video, module, cls)
        heard, _ = listening(video, module, cls)
        secs = m if m is not None else 60 * w / wpm(video) + heard
        total += secs
        heard_all += heard
        rows.append((chapter, w, secs, m is not None, heard))
    if verbose:
        for chapter, w, secs, real, heard in rows:
            ear = f"  {heard:4.0f} s listening" if heard_all else ""
            print(f"  {secs / 60:5.1f} min {'(rendered)' if real else '(estimate)':11s} {w:5d} words{ear}  {chapter}")
        ear = f"  ({heard_all / 60:.1f} min of it listening)" if heard_all else ""
        print(f"  {total / 60:5.1f} min total  {video}{ear}")
    return total / 60


def main():
    args = sys.argv[1:]
    floor = None  # per series: the AI series' minimum is 30 minutes, this series' 50
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
            f = floor if floor is not None else FLOORS.get(series, 30.0)
            top = CEILINGS.get(series, float("inf"))
            flag = "  < floor" if mins < f else "  > ceiling" if mins > top else ""
            short += not f <= mins <= top
            print(f"{v:10s} {mins:5.1f} min{flag}")
        sys.exit(1 if short else 0)
    mins = report(args[0])
    series = video_dir(args[0]).parent.name
    f = floor if floor is not None else FLOORS.get(series, 30.0)
    top = CEILINGS.get(series, float("inf"))
    if mins > top:
        print(f"  over the series' ceiling of {top:.0f} minutes")
    sys.exit(0 if f <= mins <= top else 1)


if __name__ == "__main__":
    main()
