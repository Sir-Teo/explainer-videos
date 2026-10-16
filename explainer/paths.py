"""Where a video lives: ``videos/<series>/<video>/``.  Callers name only the video (``analysis1``, ``quantum``)."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIDEOS = ROOT / "videos"
ANALYSIS_DATA = VIDEOS / "analysis"  # analysis_text_zh.json, analysis_upload.json, ANALYSIS_ZH_GUIDE.md


@lru_cache(maxsize=None)
def video_dir(video: str) -> Path:
    for manifest in VIDEOS.glob(f"*/{video}/manifest.py"):
        return manifest.parent
    raise SystemExit(f"No video named {video!r}: expected videos/<series>/{video}/manifest.py")


def video_package(video: str) -> str:
    """Dotted module path, e.g. ``videos.analysis.analysis1``."""
    return f"videos.{video_dir(video).parent.name}.{video}"
