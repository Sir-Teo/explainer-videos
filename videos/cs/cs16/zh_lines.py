"""Reviewed source narration pairs, including data-dependent templates."""
import json
from pathlib import Path

_root = Path(__file__).parent
_table = json.loads((_root / "narration_zh.json").read_text())
TITLE = _table["title"]
CHAPTERS = _table["chapters"]
ZH = json.loads((_root / "narration_source_zh.json").read_text())

import json as _json  # noqa: E402
from pathlib import Path as _Path  # noqa: E402

_watch = _Path(__file__).with_name("zh_watch.json")
if _watch.exists():  # the watch retrofit's lines (tools/zh_watch.py)
    ZH.update(_json.loads(_watch.read_text()))
