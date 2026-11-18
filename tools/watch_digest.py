#!/usr/bin/env python
"""A compact digest of a part for retrofitting it to the watch standard (videos/cs/SYLLABUS.md 1.2).

    python tools/watch_digest.py cs8            # every chapter: sections, data loaded, narration (f-strings kept)
    python tools/watch_digest.py cs8 --brief    # one line per section: its first sentences

Per section it prints the assignments that read cached data (``load(...)`` and what is derived from them) and the
narration with its ``{...}`` expressions left in place, so a prediction can be written against the same values the
section reveals.
"""

from __future__ import annotations

import argparse
import ast
import importlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from explainer.paths import video_dir, video_package  # noqa: E402


def narration(src: str, call: ast.Call) -> str:
    out = []
    for sub in ast.walk(call.args[0]) if call.args else ():
        if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
            out.append(sub.value)
        elif isinstance(sub, ast.FormattedValue):
            out.append("{" + (ast.get_source_segment(src, sub.value) or "?") + "}")
    text = re.sub(r"<bookmark[^>]*/>", "", "".join(out))
    return " ".join(text.split())


def digest(video: str, brief=False, width=900):
    manifest = importlib.import_module(f"{video_package(video)}.manifest")
    for module, cls, chapter in manifest.SCENES:
        path = video_dir(video) / f"{module}.py"
        src = path.read_text()
        tree = ast.parse(src)
        node = next((n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == cls), None)
        print(f"\n=== {module}.{cls}: {chapter}")
        if node is None:
            continue
        for f in node.body:
            if not isinstance(f, ast.FunctionDef) or f.name in ("construct", "card"):
                continue
            lines = []
            for st in f.body:
                if isinstance(st, ast.Assign) and "load(" in (ast.get_source_segment(src, st) or ""):
                    lines.append("  = " + " ".join((ast.get_source_segment(src, st) or "").split())[:200])
            texts = [narration(src, c) for c in ast.walk(f) if isinstance(c, ast.Call) and
                     isinstance(c.func, ast.Attribute) and c.func.attr == "voiceover"]
            if brief:
                t = " ".join(texts)
                sents = re.split(r"(?<=[.?!])\s+", t)
                head = " ".join(sents[:2])[:260]
                tail = " ".join(sents[-2:])[:200] if len(sents) > 3 else ""
                loads = "; ".join(ln.strip(" =")[:110] for ln in lines[:3])
                print(f"- {f.name}: {head}" + (f" ... {tail}" if tail else "") + (f"  [{loads}]" if loads else ""))
                continue
            print(f"- {f.name}")
            for ln in lines:
                print(ln)
            for t in texts:
                print("  > " + t[:width])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--brief", action="store_true")
    ap.add_argument("--width", type=int, default=900)
    a = ap.parse_args()
    digest(a.video, a.brief, a.width)
