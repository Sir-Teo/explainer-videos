#!/usr/bin/env python
"""Merge translated on-screen strings into a series' text table, safely while other jobs do the same.

    python tools/text_zh_add.py ai new_strings.json

The file holds {"strings": {english: chinese}, "patterns": [[regex, replacement], ...]} (or just the strings
mapping). Existing entries are kept, and a differing translation is reported, not overwritten. The table is
videos/<series>/<series>_text_zh.json; an exclusive lock serializes concurrent merges.
"""

import fcntl
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    series, src = sys.argv[1], Path(sys.argv[2])
    path = ROOT / "videos" / series / f"{series}_text_zh.json"
    new = json.loads(src.read_text())
    if "strings" not in new:
        new = {"strings": new}
    with open(path.with_suffix(".lock"), "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        table = json.loads(path.read_text())
        added = 0
        for k, v in new["strings"].items():
            if k not in table["strings"]:
                table["strings"][k] = v
                added += 1
            elif table["strings"][k] != v:
                print(f"kept existing: {k!r} -> {table['strings'][k]!r} (not {v!r})")
        have = {a for a, _ in table["patterns"]}
        for a, b in new.get("patterns", []):
            if a not in have:
                table["patterns"].append([a, b])
                added += 1
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(table, ensure_ascii=False, indent=2) + "\n")
        tmp.replace(path)
    print(f"{path.relative_to(ROOT)}: {added} added")


if __name__ == "__main__":
    main()
