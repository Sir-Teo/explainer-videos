"""Reviewed exact narration pairs for tools/zh_lines.py, from the authoritative JSON."""
import json
from pathlib import Path

_table = json.loads(Path(__file__).with_name("narration_zh.json").read_text())
TITLE = _table["title"]
CHAPTERS = _table["chapters"]
ZH = {entry["en"]: entry["zh"] for entry in _table["lines"].values()}

import json as _json  # noqa: E402
from pathlib import Path as _Path  # noqa: E402

_watch = _Path(__file__).with_name("zh_watch.json")
if _watch.exists():  # the watch retrofit's lines (tools/zh_watch.py)
    ZH.update(_json.loads(_watch.read_text()))
