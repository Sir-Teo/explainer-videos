"""Reviewed exact narration pairs for tools/zh_lines.py, from the authoritative JSON."""
import json
from pathlib import Path

_table = json.loads(Path(__file__).with_name("narration_zh.json").read_text())
TITLE = _table["title"]
CHAPTERS = _table["chapters"]
ZH = {entry["en"]: entry["zh"] for entry in _table["lines"].values()}
