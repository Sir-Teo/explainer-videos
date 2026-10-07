#!/usr/bin/env python
"""Tile evenly spaced frames of a video into one image for quick visual QA.

    python tools/contact_sheet.py path/to/Scene.mp4 [-n 16] [-c 4] [-o sheet.png]
    python tools/contact_sheet.py Scene.mp4 --times 3.5 12 40     # specific moments

Catches the classic layout bugs (overlaps, text off-screen, leftovers from a
previous beat) without scrubbing through the video.
"""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw


def duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        check=True, capture_output=True, text=True,
    ).stdout
    return float(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video", type=Path)
    ap.add_argument("-n", type=int, default=16)
    ap.add_argument("-c", "--cols", type=int, default=4)
    ap.add_argument("-w", "--width", type=int, default=480, help="width of each tile")
    ap.add_argument("--times", type=float, nargs="*")
    ap.add_argument("-o", "--out", type=Path)
    args = ap.parse_args()

    total = duration(args.video)
    times = args.times or [total * (i + 0.5) / args.n for i in range(args.n)]
    times = [min(max(t, 0.0), total - 0.1) for t in times]
    tiles = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, t in enumerate(times):
            f = Path(tmp) / f"{i}.png"
            subprocess.run(
                ["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(args.video), "-frames:v", "1",
                 "-vf", f"scale={args.width}:-1", str(f)],
                check=True,
            )
            im = Image.open(f).convert("RGB")
            ImageDraw.Draw(im).text((6, 4), f"{t:6.1f}s", fill=(255, 255, 0))
            tiles.append(im)
    w, h = tiles[0].size
    rows = (len(tiles) + args.cols - 1) // args.cols
    sheet = Image.new("RGB", (args.cols * w + (args.cols - 1) * 4, rows * h + (rows - 1) * 4), (60, 60, 60))
    for i, im in enumerate(tiles):
        sheet.paste(im, ((i % args.cols) * (w + 4), (i // args.cols) * (h + 4)))
    out = args.out or args.video.with_suffix(".sheet.png")
    sheet.save(out)
    print(out)


if __name__ == "__main__":
    main()
