#!/usr/bin/env python
"""Find dead air: stretches where the screen is empty (or nearly) while the video runs.

    python tools/dead_air.py renders/analysis2_2160p.mp4            # report runs of >= 1.5 s
    python tools/dead_air.py renders/analysis2_2160p.mp4 --min 1.0 --sparse 0.004
    python tools/dead_air.py renders/music1_480p.mp4 --sound music1  # and the converse: sound over a still screen

Every frame is decoded (sampled at --fps, downscaled) and the fraction of pixels that differ from the background is
measured.  A frame is *blank* below --blank (default 0.0005: nothing but the background) and *sparse* below --sparse
(default 0.003: a lone title or a bare axis).  Runs at least --min seconds long are listed with their chapter, so a
scene can be fixed where the narration talks over an empty screen.

With ``--sound <video>`` (the series with a soundtrack of their own: *Music, Built*) the converse is checked as well:
"everything you hear, you see".  The cue sheets each scene wrote (``<Scene>.cues.json``) say when a clip sounds; inside
those windows the picture must be neither empty nor still for --still seconds or longer (default 2.5), and the exit
code is 1 if it is.  Clips played as an underscore (under narration) are left out.
"""

from __future__ import annotations

import argparse
import importlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

BG = (0x0E, 0x11, 0x17)  # explainer/style.py BACKGROUND


def chapters(path: str) -> list[tuple[float, str]]:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_chapters", "-of", "json", path], capture_output=True,
                         text=True).stdout
    return [(float(c["start_time"]), c["tags"].get("title", "")) for c in json.loads(out or "{}").get("chapters", [])]


def sound_windows(video: str, starts: list[float]) -> list[tuple[float, float, str]]:
    """(start, end, clip) on the film's clock of every clip that is listened to, from the newest cue sheets."""
    sys.path.insert(0, str(ROOT))
    from explainer.paths import video_package

    manifest = importlib.import_module(f"{video_package(video)}.manifest")
    out, k = [], 0
    for module, cls, chapter in manifest.SCENES:
        offset = starts[k] if chapter and k < len(starts) else None
        k += bool(chapter)
        sheets = sorted((ROOT / "media" / video / "videos" / module).glob(f"*/{cls}.cues.json"),
                        key=lambda q: q.stat().st_mtime)
        if offset is None or not sheets:
            continue
        for c in json.loads(sheets[-1].read_text())["cues"]:
            if not c.get("underscore"):
                out.append((offset + c["start"], offset + c["start"] + c["duration"], c["clip"]))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--fps", type=float, default=4.0)
    ap.add_argument("--min", type=float, default=1.5, help="shortest run to report, in seconds")
    ap.add_argument("--blank", type=float, default=0.0005)
    ap.add_argument("--sparse", type=float, default=0.003)
    ap.add_argument("--sound", metavar="VIDEO", help="also check that the picture moves while this video's clips sound")
    ap.add_argument("--still", type=float, default=2.5, help="longest still or empty picture allowed under a sound")
    ap.add_argument("--moving", type=float, default=0.0002, help="fraction of pixels that must change between frames")
    args = ap.parse_args()

    w, h = 320, 180
    cmd = ["ffmpeg", "-v", "error", "-threads", "0", "-i", args.video, "-an", "-sn",
           "-vf", f"fps={args.fps},scale={w}:{h}:flags=area", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    bg = np.array(BG, dtype=np.int16)
    fracs, moved, last = [], [], None
    frame_bytes = w * h * 3
    while True:
        buf = proc.stdout.read(frame_bytes)
        if len(buf) < frame_bytes:
            break
        img = np.frombuffer(buf, dtype=np.uint8).reshape(h, w, 3).astype(np.int16)
        fracs.append(float((np.abs(img - bg).max(axis=2) > 24).mean()))
        moved.append(1.0 if last is None else float((np.abs(img - last).max(axis=2) > 10).mean()))
        last = img
    if proc.wait() != 0:
        sys.exit(f"ffmpeg could not decode {args.video}; dead-air QA did not run")
    if not fracs:
        sys.exit(f"no video frames decoded from {args.video}; dead-air QA did not run")
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

    if not args.sound:
        return
    moved = np.array(moved)
    windows = sound_windows(args.sound, [s for s, _ in chs])
    if not windows:
        sys.exit(f"no cue sheets for {args.sound} match this film's chapters; the sound check did not run")
    bad, heard = [], 0.0
    for a, b, clip in windows:
        i, j = int(np.ceil(a * args.fps)), min(int(b * args.fps), len(fracs) - 1)
        heard += b - a
        if j <= i:
            continue
        unseen = (fracs[i:j + 1] < args.blank) | (moved[i:j + 1] < args.moving)
        run = best = 0
        for u in unseen:
            run = run + 1 if u else 0
            best = max(best, run)
        if best / args.fps >= args.still:
            bad.append((a, b, clip, best / args.fps))
    print(f"sound over a still or empty screen (>= {args.still:.1f} s): {len(bad)} of {len(windows)} windows, "
          f"{heard:.0f} s of listening")
    for a, b, clip, secs in bad:
        name, rel = chapter_at(a)
        print(f"  {int(a // 60):2d}:{a % 60:05.2f}  {secs:4.1f} s still in a {b - a:.1f} s clip   {clip}   [{name}  +{rel:.1f} s]")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
