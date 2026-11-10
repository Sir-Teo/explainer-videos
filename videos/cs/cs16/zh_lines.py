"""Reviewed source narration pairs, including data-dependent templates."""
import json
from pathlib import Path

_root = Path(__file__).parent
_table = json.loads((_root / "narration_zh.json").read_text())
TITLE = _table["title"]
CHAPTERS = _table["chapters"]
ZH = json.loads((_root / "narration_source_zh.json").read_text())
