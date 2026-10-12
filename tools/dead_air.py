#!/usr/bin/env python
"""Find dead air: stretches where the screen is empty (or nearly) while the video runs.

    python tools/dead_air.py renders/analysis2_2160p.mp4            # report runs of >= 1.5 s
    python tools/dead_air.py renders/analysis2_2160p.mp4 --min 1.0 --sparse 0.004

Every frame is decoded (sampled at --fps, downscaled) and the fraction of pixels that differ from the background is
measured.  A frame is *blank* below --blank (default 0.0005: nothing but the background) and *sparse* below --sparse
(default 0.003: a lone title or a bare axis).  Runs at least --min seconds long are listed with their chapter, so a
scene can be fixed where the narration talks over an empty screen.
"""

from __future__ import annotations

import argparse
import json
import subprocess

import numpy as np

BG = (0x0E, 0x11, 0x17)  # explainer/style.py BACKGROUND


def chapters(path: str) -> list[tuple[float, str]]:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_chapters", "-of", "json", path], capture_output=True,
                         text=True).stdout
    return [(float(c["start_time"]), c["tags"].get("title", "")) for c in json.loads(out or "{}").get("chapters", [])]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--fps", type=float, default=4.0)
    ap.add_argument("--min", type=float, default=1.5, help="shortest run to report, in seconds")
    ap.add_argument("--blank", type=float, default=0.0005)
    ap.add_argument("--sparse", type=float, default=0.003)
    args = ap.parse_args()

    w, h = 320, 180
    cmd = ["ffmpeg", "-v", "error", "-threads", "0", "-i", args.video, "-an", "-sn",
           "-vf", f"fps={args.fps},scale={w}:{h}:flags=area", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    bg = np.array(BG, dtype=np.int16)
    fracs = []
    frame_bytes = w * h * 3
    while True:
        buf = proc.stdout.read(frame_bytes)
        if len(buf) < frame_bytes:
            break
        img = np.frombuffer(buf, dtype=np.uint8).reshape(h, w, 3).astype(np.int16)
        fracs.append(float((np.abs(img - bg).max(axis=2) > 24).mean()))
    proc.wait()
    fracs = np.array(fracs)
    chs = chapters(args.video)

    def chapter_at(t):
        name, start = "", 0.0
        for s, title in chs:
            if s <= t:
                name, start = title, s
        return name, t - start

    def runs(mask):
        out, start = [], None
        for i, m in enumerate(list(mask) + [False]):
            if m and start is None:
                start = i
            elif not m and start is not None:
                if (i - start) / args.fps >= args.min:
                    out.append((start / args.fps, i / args.fps))
                start = None
        return out

    total = len(fracs) / args.fps
    for kind, thr in (("blank", args.blank), ("sparse", args.sparse)):
        rs = runs(fracs < thr)
        print(f"{kind} (< {thr:.2%} of pixels drawn), runs >= {args.min:.1f} s: {len(rs)}, "
              f"{sum(b - a for a, b in rs):.1f} s of {total:.0f} s")
        for a, b in rs:
            name, rel = chapter_at(a)
            print(f"  {int(a // 60):2d}:{a % 60:05.2f}  {b - a:4.1f} s   [{name}  +{rel:.1f} s]")


if __name__ == "__main__":
    main()
