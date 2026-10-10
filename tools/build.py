#!/usr/bin/env python
"""Render a video's scenes in parallel and stitch them into one file.

    python tools/build.py navier_stokes                 # 1080p30 final cut
    python tools/build.py navier_stokes -q l            # fast 480p preview
    python tools/build.py navier_stokes --only Pressure Viscosity
    python tools/build.py navier_stokes --stitch-only   # reuse rendered scenes

Outputs (in ``renders/``):
    <video>.mp4            video + narration (loudness-normalized) + soft subtitles + chapters
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


# Audio mastering for the stitched soundtrack: remove sub-bass rumble, then two-pass EBU R128
# loudness normalization to -16 LUFS integrated (the usual target for online video) with a
# -1.5 dBTP true-peak ceiling, so every video plays at the same, comfortable level.
HIGHPASS = "highpass=f=60"
LOUDNORM = "loudnorm=I=-16:TP=-1.5:LRA=11"


def master_filter(measure_cmd: list[str]) -> str:
    """Run the first loudnorm pass and return the filter for the second (linear) pass."""
    err = subprocess.run(measure_cmd, text=True, capture_output=True, check=True).stderr
    m = json.loads(err[err.rindex("{"): err.rindex("}") + 1])
    return (f"{HIGHPASS},{LOUDNORM}:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
            f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
            f":offset={m['target_offset']}:linear=true")


def scene_output(media: Path, module: str, cls: str, quality: str, fps: int) -> Path:
    return media / "videos" / module / f"{QUALITY[quality]}{fps}" / f"{cls}.mp4"


def render_scene(video: str, module: str, cls: str, quality: str, fps: int, media: Path, crf: int | None = None) -> tuple[str, float, str]:
    src = ROOT / "videos" / video / f"{module}.py"
    # Each scene gets its own LaTeX cache: parallel manim processes sharing one
    # Tex dir race on the .dvi files (one cleans up what another converts).
    cfg = media / "cfg" / f"{cls}.cfg"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    tex_dir = media / "Tex" / cls
    tex_dir.mkdir(parents=True, exist_ok=True)
    cfg.write_text(f"[CLI]\ntex_dir = {tex_dir}\n")
    cmd = [
        sys.executable, "-m", "manim", "render", f"-q{quality}", "--fps", str(fps), "-c", str(cfg),
        "--media_dir", str(media), "--progress_bar", "none", str(src), cls,
    ]
    t = time.time()
    env = dict(os.environ, PYTHONWARNINGS="ignore")
    if crf is not None:
        env["EXPLAINER_RENDER_CRF"] = str(crf)
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, env=env)
    if proc.returncode != 0:
        return cls, time.time() - t, proc.stdout[-3000:] + proc.stderr[-3000:]
    return cls, time.time() - t, ""


def check_narration_audio(mp4: Path, lines: list[dict]) -> None:
    """Fail if a scene's soundtrack stops before its last narration line ends (sound dropped while rendering)."""
    if not lines:
        return
    end = max(ln["start"] + ln["duration"] for ln in lines)
    out = run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=duration", "-of", "csv=p=0", str(mp4)])
    audio = float(out.stdout.strip() or 0)
    if audio < end - 0.5:
        sys.exit(f"{mp4.name}: the soundtrack ends at {audio:.1f} s but the narration runs to {end:.1f} s")


def normalize(src: Path, dst: Path, lossless: bool = False) -> None:
    """Pad/trim audio to exactly the video length so concatenation stays in sync."""
    dur = ffprobe_duration(src)
    wav = src.with_suffix(".wav")
    source_has_audio = has_audio(src)
    if lossless and wav.exists():
        # Manim retains its PCM soundtrack next to the scene. Use it rather
        # than repeatedly encoding its AAC preview soundtrack.
        audio_in = ["-i", str(src), "-i", str(wav)]
        amap = "[1:a]aresample=48000,aformat=channel_layouts=stereo,apad[a]"
    elif source_has_audio:
        audio_in = ["-i", str(src)]
        amap = "[0:a]aresample=48000,aformat=channel_layouts=stereo,apad[a]"
    else:
        audio_in = ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-i", str(src)]
        amap = "[0:a]apad[a]"
    vin = 0 if source_has_audio or (lossless and wav.exists()) else 1
    cmd = ["ffmpeg", "-y", "-v", "error", *audio_in]
    cmd += ["-filter_complex", amap, "-map", f"{vin}:v", "-map", "[a]", "-t", f"{dur:.3f}"]
    audio_codec = ["-c:a", "alac", "-sample_fmt", "s32p"] if lossless else ["-c:a", "aac", "-b:a", "192k"]
    cmd += ["-c:v", "copy", *audio_codec, str(dst)]
    run(cmd)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("-q", "--quality", default="h", choices=list(QUALITY))
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--crf", type=int, choices=range(52), metavar="0-51",
                    help="H.264 encoding quality (lower is better; 18 for YouTube masters)")
    ap.add_argument("-j", "--jobs", type=int, default=max(1, (os.cpu_count() or 2) // 2))
    ap.add_argument("--only", nargs="*", help="render only these scene classes (still stitches all)")
    ap.add_argument("--stitch-only", action="store_true")
    args = ap.parse_args()

    manifest = importlib.import_module(f"videos.{args.video}.manifest")
    scenes = manifest.SCENES
    media = ROOT / "media" / args.video
    if args.crf is not None:
        # Manim's animation hashes do not include our encoder override.
        media = media / f"crf{args.crf}"

    if not args.stitch_only:
        todo = [s for s in scenes if not args.only or s[1] in args.only]
        print(f"Rendering {len(todo)} scene(s) at {QUALITY[args.quality]}{args.fps} with {args.jobs} job(s)...")
        failed = []
        with ThreadPoolExecutor(args.jobs) as pool:
            futs = [pool.submit(render_scene, args.video, m, c, args.quality, args.fps, media, args.crf) for m, c, _ in todo]
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
        meta = mp4.with_suffix(".narration.json")
        lines = json.loads(meta.read_text())["lines"] if meta.exists() else []
        check_narration_audio(mp4, lines)
        normalize(mp4, norm, lossless=args.crf is not None)
        dur = ffprobe_duration(norm)
        cues += subtitle_cues(lines, offset)
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
    audio_filter = master_filter([
        "ffmpeg", "-v", "info", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-vn",
        "-af", f"{HIGHPASS},{LOUDNORM}:print_format=json", "-f", "null", "-",
    ])
    run([
        "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-i", str(srt), "-i", str(ffmeta), "-map", "0", "-map", "1", "-map_metadata", "2",
        "-c:v", "copy", "-af", audio_filter, "-ar", "48000", "-c:a", "aac", "-b:a", "384k" if args.crf is not None else "192k",
        "-c:s", "mov_text", "-metadata:s:s:0", "language=eng", "-movflags", "+faststart", str(final),
    ])
    yt = "\n".join(f"{int(s // 60)}:{int(s % 60):02d} {t}" for s, t in chapters)
    (out_dir / f"{name}.chapters.txt").write_text(yt + "\n")
    print(f"\nWrote {final.relative_to(ROOT)}  ({offset / 60:.1f} min)")
    print(yt)


if __name__ == "__main__":
    main()
