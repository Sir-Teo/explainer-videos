"""The Dials gate (tools/check_dials.py) passes on every built part."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import check_dials  # noqa: E402


def test_every_built_part_passes():
    parts = sorted(p.parent.name for p in (ROOT / "videos" / "economics").glob("econ[0-9]*/manifest.py"))
    assert parts
    for v in parts:
        assert check_dials.check(v) == [], v
