#!/usr/bin/env python
"""Make a copy of a finished video small enough to commit to GitHub.

    python tools/publish.py llm                 # renders/llm.mp4 -> published/llm.mp4
    python tools/publish.py navier_stokes --max-mb 95

GitHub rejects pushes containing files over 100 MiB, so published copies aim
just under that (95 MB by default).  Narration is re-encoded as mono AAC at
96 kb/s (transparent for speech).  The video stream is copied bit-for-bit when
that already fits; otherwise it is re-encoded with two-pass x264 at exactly
the bitrate that fills the remaining budget.  Soft subtitles and chapter
markers are kept, and the .srt is copied alongside.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GITHUB_HARD_LIMIT = 100 * 1024 * 1024
AUDIO_KBPS = 96
CONTAINER_OVERHEAD = 0.015  # mp4 boxes, subtitles, chapters


def probe(path: Path, entry: str, stream: str | None = None) -> str:
    cmd = ["ffprobe", "-v", "error"]
    if stream:
        cmd += ["-select_streams", stream]
    cmd += ["-show_entries", entry, "-of", "csv=p=0", str(path)]
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout.strip().splitlines()[0]


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--max-mb", type=float, default=95.0, help="size budget in MB (10^6 bytes)")
    ap.add_argument("--force-reencode", action="store_true")
    args = ap.parse_args()

    src = ROOT / "renders" / f"{args.video}.mp4"
    if not src.exists():
        sys.exit(f"Missing {src.relative_to(ROOT)}: run tools/build.py {args.video} first")
    out_dir = ROOT / "published"
    out_dir.mkdir(exist_ok=True)
    dst = out_dir / f"{args.video}.mp4"

    budget = args.max_mb * 1e6
    duration = float(probe(src, "format=duration"))
    video_bits = float(probe(src, "stream=bit_rate", "v:0")) * duration
    audio_bits = AUDIO_KBPS * 1000 * duration
    usable = budget * 8 * (1 - CONTAINER_OVERHEAD)
    common_in = ["-i", str(src)]
    maps = ["-map", "0:v:0", "-map", "0:a:0", "-map", "0:s?", "-map_metadata", "0", "-map_chapters", "0"]
    audio = ["-c:a", "aac", "-b:a", f"{AUDIO_KBPS}k", "-ac", "1", "-ar", "48000"]
    tail = ["-c:s", "mov_text", "-movflags", "+faststart", str(dst)]

    if video_bits + audio_bits <= usable and not args.force_reencode:
        print(f"video stream fits ({video_bits / 8e6:.1f} MB): copying it unchanged")
        run(["ffmpeg", "-y", "-v", "error", *common_in, *maps, "-c:v", "copy", *audio, *tail])
    else:
        kbps = int((usable - audio_bits) / duration / 1000)
        print(f"re-encoding video at {kbps} kb/s (two-pass x264) to fit {args.max_mb:.0f} MB")
        with tempfile.TemporaryDirectory() as tmp:
            log = str(Path(tmp) / "x264")
            x264 = ["-c:v", "libx264", "-preset", "slow", "-tune", "animation", "-b:v", f"{kbps}k",
                    "-pix_fmt", "yuv420p", "-g", "300", "-passlogfile", log]
            run(["ffmpeg", "-y", "-v", "error", *common_in, "-map", "0:v:0", *x264, "-pass", "1", "-an", "-f", "null", "-"])
            run(["ffmpeg", "-y", "-v", "error", *common_in, *maps, *x264, "-pass", "2", *audio, *tail])

    size = dst.stat().st_size
    if size >= GITHUB_HARD_LIMIT:
        sys.exit(f"{dst.name} is {size / 1e6:.1f} MB: still over GitHub's limit, lower --max-mb")
    srt = ROOT / "renders" / f"{args.video}.srt"
    if srt.exists():
        shutil.copy(srt, out_dir / srt.name)
    print(f"Wrote {dst.relative_to(ROOT)}  ({size / 1e6:.1f} MB, {duration / 60:.1f} min)")


if __name__ == "__main__":
    main()
