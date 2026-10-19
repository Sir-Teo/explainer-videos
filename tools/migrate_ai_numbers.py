#!/usr/bin/env python
"""Rename a checkout's generated AI-series files after the series went from 20 parts to 31 (videos/ai/SYLLABUS.md).

    python tools/migrate_ai_numbers.py          # show what would move
    python tools/migrate_ai_numbers.py --apply  # move it

The parts' computed results (.cache/aiN), rendered scenes (media/aiN) and cuts (renders/aiN*, published/aiN*) are
keyed by video name, so after the renumbering a machine that built the old Part 11 has it under .cache/ai11, where
the new Part 11 (old Part 9) would look.  This moves each to its new name, in two steps so nothing is overwritten.
Run it once, on a checkout that has never built a part under its new number.  The narration cache (.cache/tts) is
keyed by the spoken text, not the video, and needs nothing.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD_TO_NEW = {1: 1, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 11, 10: 12, 11: 13, 12: 15, 13: 16, 14: 21, 15: 22,
              16: 23, 17: 28, 18: 29, 19: 19, 20: 30}
NAME = re.compile(r"^ai(\d{1,2})(?=$|[_.\-])")
ROOTS = [ROOT / ".cache", ROOT / "media", ROOT / "renders", ROOT / "published", ROOT / "renders" / "upload",
         ROOT / "renders" / "qa" / "text"]


def plan() -> list[tuple[Path, Path]]:
    moves = []
    for base in ROOTS:
        if not base.is_dir():
            continue
        for p in sorted(base.iterdir()):
            m = NAME.match(p.name)
            if m and int(m.group(1)) in OLD_TO_NEW and OLD_TO_NEW[int(m.group(1))] != int(m.group(1)):
                new = f"ai{OLD_TO_NEW[int(m.group(1))]}" + p.name[m.end():]
                moves.append((p, p.with_name(new)))
    return moves


def main():
    moves = plan()
    marker = ROOT / ".cache" / "ai_numbers_v31"
    if marker.exists():
        sys.exit("already migrated (.cache/ai_numbers_v31 exists)")
    for a, b in moves:
        print(f"{a.relative_to(ROOT)}  ->  {b.relative_to(ROOT)}")
    if "--apply" not in sys.argv:
        print(f"\n{len(moves)} to move; run with --apply")
        return
    staged = []
    for a, b in moves:
        tmp = a.with_name(a.name + ".migrating")
        a.rename(tmp)
        staged.append((tmp, b))
    for tmp, b in staged:
        if b.exists():
            sys.exit(f"{b} exists; left {tmp} in place")
        tmp.rename(b)
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text("renamed for the 31-part numbering\n")
    print(f"\nmoved {len(moves)}")


if __name__ == "__main__":
    main()
