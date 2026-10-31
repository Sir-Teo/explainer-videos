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


def validate_input(value):
    """Normalize only the documented shapes, before opening any output file."""
    if not isinstance(value, dict):
        raise ValueError("input must be an object containing string translations")
    if any(not isinstance(key, str) for key in value):
        raise ValueError("input keys must be strings")
    # A bare mapping may itself translate the English words 'strings'/'patterns'.
    if all(isinstance(text, str) for text in value.values()):
        return {"strings": value, "patterns": []}
    if "strings" not in value:
        bad = next(key for key, text in value.items() if not isinstance(text, str))
        raise ValueError(f"bare translation value for {bad!r} must be a string; "
                         "wrapped input requires a 'strings' mapping")
    unknown = set(value) - {"strings", "patterns"}
    if unknown:
        raise ValueError(f"unsupported wrapped input fields: {', '.join(sorted(unknown))}")
    strings = value["strings"]
    if not isinstance(strings, dict):
        raise ValueError("'strings' must be an object mapping English strings to Chinese strings")
    for key, text in strings.items():
        if not isinstance(key, str) or not isinstance(text, str):
            raise ValueError(f"'strings' entry {key!r} must have a string key and string value")
    patterns = value.get("patterns", [])
    if not isinstance(patterns, list):
        raise ValueError("'patterns' must be a list of [regex, replacement] string pairs")
    for index, pair in enumerate(patterns):
        if not isinstance(pair, list) or len(pair) != 2 or not all(isinstance(text, str) for text in pair):
            raise ValueError(f"'patterns' entry {index} must be a [regex, replacement] string pair")
    return {"strings": strings, "patterns": patterns}


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    series, src = sys.argv[1], Path(sys.argv[2])
    path = ROOT / "videos" / series / f"{series}_text_zh.json"
    try:
        new = validate_input(json.loads(src.read_text()))
    except (json.JSONDecodeError, ValueError) as exc:
        sys.exit(f"invalid translation input: {exc}")
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
