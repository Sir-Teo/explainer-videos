#!/usr/bin/env python
"""Render a video's scenes in parallel and stitch them into one file.

    python tools/build.py navier_stokes                 # 1080p30 final cut
    python tools/build.py navier_stokes -q l            # fast 480p preview
    python tools/build.py navier_stokes --only Pressure Viscosity
    python tools/build.py navier_stokes --stitch-only   # reuse rendered scenes

Outputs (in ``renders/``):
    <video>.mp4            video + narration + soft subtitles + chapters
    <video>.srt            subtitles
    <video>.chapters.txt   YouTube-style chapter list
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from explainer.voiceover import subtitle_cues, to_srt  # noqa: E402

QUALITY = {"l": "480p", "m": "720p", "h": "1080p", "p": "1440p", "k": "2160p"}


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, text=True, capture_output=True, **kw)


def ffprobe_duration(path: Path) -> float:
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]).stdout
    return float(out.strip())


def has_audio(path: Path) -> bool:
    out = run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", str(path)])
    return bool(out.stdout.strip())


def scene_output(media: Path, module: str, cls: str, quality: str, fps: int) -> Path:
    return media / "videos" / module / f"{QUALITY[quality]}{fps}" / f"{cls}.mp4"


def render_scene(video: str, module: str, cls: str, quality: str, fps: int, media: Path) -> tuple[str, float, str]:
    src = ROOT / "videos" / video / f"{module}.py"
    cmd = [
        sys.executable, "-m", "manim", "render", f"-q{quality}", "--fps", str(fps),
        "--media_dir", str(media), "--progress_bar", "none", str(src), cls,
    ]
    t = time.time()
    env = dict(os.environ, PYTHONWARNINGS="ignore")
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, env=env)
    if proc.returncode != 0:
        return cls, time.time() - t, proc.stdout[-3000:] + proc.stderr[-3000:]
    return cls, time.time() - t, ""


def normalize(src: Path, dst: Path) -> None:
    """Pad/trim audio to exactly the video length so concatenation stays in sync."""
    dur = ffprobe_duration(src)
    if has_audio(src):
        audio_in = ["-i", str(src)]
        amap = "[0:a]aresample=48000,aformat=channel_layouts=stereo,apad[a]"
    else:
        audio_in = ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-i", str(src)]
        amap = "[0:a]apad[a]"
    vin = 0 if has_audio(src) else 1
    cmd = ["ffmpeg", "-y", "-v", "error", *audio_in]
    cmd += ["-filter_complex", amap, "-map", f"{vin}:v", "-map", "[a]", "-t", f"{dur:.3f}"]
    cmd += ["-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(dst)]
    run(cmd)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("-q", "--quality", default="h", choices=list(QUALITY))
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("-j", "--jobs", type=int, default=max(1, (os.cpu_count() or 2) // 2))
    ap.add_argument("--only", nargs="*", help="render only these scene classes (still stitches all)")
    ap.add_argument("--stitch-only", action="store_true")
    args = ap.parse_args()

    manifest = importlib.import_module(f"videos.{args.video}.manifest")
    scenes = manifest.SCENES
    media = ROOT / "media" / args.video

    if not args.stitch_only:
        todo = [s for s in scenes if not args.only or s[1] in args.only]
        print(f"Rendering {len(todo)} scene(s) at {QUALITY[args.quality]}{args.fps} with {args.jobs} job(s)...")
        failed = []
        with ThreadPoolExecutor(args.jobs) as pool:
            futs = [pool.submit(render_scene, args.video, m, c, args.quality, args.fps, media) for m, c, _ in todo]
            for f in futs:
                cls, dt, err = f.result()
                print(f"  {'FAIL' if err else 'ok  '} {cls:<28} {dt:6.0f}s", flush=True)
                if err:
                    failed.append(cls)
                    print(err)
        if failed:
            sys.exit(f"Failed scenes: {failed}")

    # ---- stitch -----------------------------------------------------------
    out_dir = ROOT / "renders"
    work = media / "stitch"
    out_dir.mkdir(exist_ok=True)
    work.mkdir(parents=True, exist_ok=True)
    suffix = "" if args.quality == "h" else f"_{QUALITY[args.quality]}"
    name = f"{args.video}{suffix}"

    parts, cues, chapters, offset = [], [], [], 0.0
    for module, cls, chapter in scenes:
        mp4 = scene_output(media, module, cls, args.quality, args.fps)
        if not mp4.exists():
            sys.exit(f"Missing render for {cls}: {mp4}")
        norm = work / f"{cls}.mp4"
        normalize(mp4, norm)
        dur = ffprobe_duration(norm)
        meta = mp4.with_suffix(".narration.json")
        if meta.exists():
            cues += subtitle_cues(json.loads(meta.read_text())["lines"], offset)
        if chapter:
            chapters.append((offset, chapter))
        parts.append(norm)
        offset += dur

    concat_list = work / "concat.txt"
    concat_list.write_text("".join(f"file '{p}'\n" for p in parts))
    srt = out_dir / f"{name}.srt"
    srt.write_text(to_srt(cues))

    ffmeta = work / "chapters.ffmeta"
    lines = [";FFMETADATA1", f"title={manifest.TITLE}"]
    bounds = [c[0] for c in chapters] + [offset]
    for (start, title), end in zip(chapters, bounds[1:]):
        lines += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={int(start * 1000)}", f"END={int(end * 1000)}", f"title={title}"]
    ffmeta.write_text("\n".join(lines) + "\n")

    final = out_dir / f"{name}.mp4"
    run([
        "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-i", str(srt), "-i", str(ffmeta), "-map", "0", "-map", "1", "-map_metadata", "2",
        "-c:v", "copy", "-c:a", "copy", "-c:s", "mov_text", "-metadata:s:s:0", "language=eng",
        "-movflags", "+faststart", str(final),
    ])
    yt = "\n".join(f"{int(s // 60)}:{int(s % 60):02d} {t}" for s, t in chapters)
    (out_dir / f"{name}.chapters.txt").write_text(yt + "\n")
    print(f"\nWrote {final.relative_to(ROOT)}  ({offset / 60:.1f} min)")
    print(yt)


if __name__ == "__main__":
    main()
