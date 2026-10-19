#!/usr/bin/env python
"""Carry a Chinese narration line over when only the numbers in its English line changed (data-driven lines).

    python tools/zh_follow_numbers.py ai9

A line computed from a part's results ("it reaches 2.51 bits, ahead of AdamW's 2.61") gets a new hash when a re-run
of compute.py moves a number in the last digit, and then has no translation. For each such line this finds the stored
English line that is identical except for its numbers, adds an entry for the new one, and substitutes the numbers in
the Chinese. Lines that differ in anything but numbers, or whose numbers cannot be matched one to one, are listed.
"""

from __future__ import annotations

import difflib
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ["EXPLAINER_LANG"] = "zh"
NUM = re.compile(r"\d+(?:\.\d+)?")


def main():
    from explainer import lang as L
    from explainer.paths import video_dir
    from tools.translate_narration import english_lines

    video = sys.argv[1]
    vd = video_dir(video)
    path = vd / "narration_zh.json"
    table = json.loads(path.read_text())
    lines = table["lines"]
    fixed, manual = 0, []
    for cls, raw in english_lines(video):
        k = L.key(raw)
        if lines.get(k, {}).get("zh"):
            continue
        shape = NUM.sub("#", raw)
        best = None
        for h, e in lines.items():
            if e.get("zh") and NUM.sub("#", e["en"]) == shape:
                best = (h, e)
                break
        if not best:
            manual.append((cls, raw))
            continue
        old_nums, new_nums = NUM.findall(best[1]["en"]), NUM.findall(raw)
        zh = best[1]["zh"]
        ok = True
        for o, n in zip(old_nums, new_nums):
            if o == n:
                continue
            if len(re.findall(rf"(?<![\d.]){re.escape(o)}(?![\d])", zh)) != 1:
                ok = False
                break
            zh = re.sub(rf"(?<![\d.]){re.escape(o)}(?![\d])", n, zh)
        if not ok:
            manual.append((cls, raw))
            continue
        lines[k] = {"scene": cls, "en": " ".join(raw.split()), "zh": zh}
        fixed += 1
        print(f"  {cls}: {', '.join(f'{a}->{b}' for a, b in zip(old_nums, new_nums) if a != b)}")
    if fixed:
        path.write_text(json.dumps(table, ensure_ascii=False, indent=1) + "\n")
    print(f"{video}: {fixed} line(s) carried over, {len(manual)} need a translation")
    for cls, raw in manual:
        print(f"  MANUAL {cls}: {raw[:150]}")


if __name__ == "__main__":
    main()
