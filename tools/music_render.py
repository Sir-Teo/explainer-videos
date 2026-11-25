#!/usr/bin/env python
"""Render Music, Built in order and verify each English 4K60 master."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import fcntl
from fractions import Fraction
import importlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

STATE = ROOT / ".cache" / "music-render"
OUTPUT = ROOT / "renders"


def available_parts() -> list[int]:
    manifests = (ROOT / "videos" / "music").glob("music*/manifest.py")
    return sorted(int(path.parent.name[5:]) for path in manifests if path.parent.name[5:].isdigit())


def run_step(log, *command, capture=None):
    with log.open("a") as output:
        print(f"\n$ {' '.join(map(str, command))}", file=output, flush=True)
        result = subprocess.run(command, cwd=ROOT, stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE if capture == "stdout" else output,
                                stderr=subprocess.PIPE if capture == "stderr" else output, text=True)
        if capture:
            output.write(getattr(result, capture))
        result.check_returncode()
    return getattr(result, capture) if capture else None


def check_picture_clock(master, stream, log):
    """Every frame has exactly one slot on the 60 Hz presentation clock, including B-frames."""
    count = int(stream["nb_frames"])
    ticks = Fraction(1, 60) / Fraction(stream["time_base"])
    if count < 1 or ticks.denominator != 1:
        raise ValueError("The master has no exact 60 Hz frame grid")
    step = int(ticks)
    seen = bytearray(count)
    with log.open("a") as output:
        packets = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                  "packet=pts", "-of", "csv=p=0", str(master)],
                                 stdout=subprocess.PIPE, stderr=output, text=True, check=True)
    for pts in packets.stdout.splitlines():
        index, remainder = divmod(int(pts), step)
        if remainder or not 0 <= index < count or seen[index]:
            raise ValueError(f"Unexpected or duplicate video timestamp {pts}")
        seen[index] = 1
    if not all(seen):
        raise ValueError("A video presentation timestamp is missing")


def verify_master(master, scenes, log):
    probe = json.loads(run_step(log, "ffprobe", "-v", "error", "-show_streams", "-show_chapters",
                                "-show_format", "-of", "json", master, capture="stdout"))
    streams = {stream["codec_type"]: stream for stream in probe["streams"]}
    picture, audio, subtitles = (streams[key] for key in ("video", "audio", "subtitle"))
    if (picture["codec_name"], picture["width"], picture["height"], picture["r_frame_rate"],
            picture["avg_frame_rate"], picture["pix_fmt"]) != ("h264", 3840, 2160, "60/1", "60/1", "yuv420p"):
        raise ValueError("Expected a constant-rate 4K60 H.264 picture")
    check_picture_clock(master, picture, log)
    if (audio["codec_name"], audio["sample_rate"], audio["channels"]) != ("aac", "48000", 2):
        raise ValueError("Expected 48 kHz stereo AAC")
    if any(stream.get("tags", {}).get("language") != "eng" for stream in (audio, subtitles)):
        raise ValueError("Expected English audio and subtitles")
    if abs(float(audio["duration"]) - float(picture["duration"])) > 0.05:
        raise ValueError("Master audio and picture durations differ by more than 50 ms")
    chapter_count = sum(bool(title) for _, _, title in scenes)
    if (len(probe["chapters"]) != chapter_count
            or len(master.with_suffix(".chapters.txt").read_text().splitlines()) != chapter_count
            or not master.with_suffix(".srt").read_text().strip()):
        raise ValueError("Chapter or subtitle sidecars are incomplete")

    # Decode several picture/audio windows, including both ends. Measure the
    # entire encoded soundtrack separately without decoding the 4K picture.
    seconds = float(picture["duration"])
    for point in (0, seconds * 0.25, seconds * 0.5, seconds * 0.75, max(0, seconds - 2)):
        run_step(log, "ffmpeg", "-v", "error", "-xerror", "-ss", str(point), "-i", master,
                 "-map", "0:v:0", "-map", "0:a:0", "-t", "1", "-f", "null", "-")
    levels = run_step(log, "ffmpeg", "-nostats", "-xerror", "-i", master, "-vn", "-af", "ebur128=peak=true:framelog=verbose",
                      "-f", "null", "-", capture="stderr").rsplit("Summary:", 1)[-1]
    loudness = float(re.search(r"I:\s+(-?[\d.]+) LUFS", levels)[1])
    peak = float(re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", levels)[1])
    if peak > -1.0 or loudness <= -60:
        raise ValueError(f"Encoded soundtrack is {loudness:.1f} LUFS with {peak:.1f} dBTP peak")
    return {"probe": probe, "loudness_lufs": loudness, "true_peak_dbtp": peak}


def file_state(master):
    files = (master, master.with_suffix(".srt"), master.with_suffix(".chapters.txt"))
    return {path.name: [path.stat().st_size, path.stat().st_mtime_ns] for path in files}


def complete(master, receipt):
    try:
        return json.loads(receipt.read_text())["files"] == file_state(master)
    except (OSError, ValueError, KeyError):
        return False


def save_receipt(receipt, master, report):
    receipt.parent.mkdir(parents=True, exist_ok=True)
    temporary = receipt.with_suffix(".tmp")
    temporary.write_text(json.dumps({"files": file_state(master), **report}, indent=2) + "\n")
    temporary.replace(receipt)


def clear_intermediates(video, receipt):
    media = ROOT / "media" / video / "crf16"
    for source in media.glob("videos/*/2160p60/*.json"):
        destination = receipt.with_suffix("") / source.relative_to(media / "videos")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    if media.exists():
        shutil.rmtree(media)


def finish_part(video, build, clean):
    log = STATE / "logs" / f"{video}.log"
    master = OUTPUT / f"{video}_2160p.mp4"
    receipt = OUTPUT / "qa" / "music-master" / f"{video}.json"
    print(f"{video}: mastering and verifying", flush=True)
    try:
        run_step(log, *build, "--stitch-only")
        run_step(log, sys.executable, "tools/qa_sound.py", video)
        manifest = importlib.import_module(f"videos.music.{video}.manifest")
        report = verify_master(master, manifest.SCENES, log)
        save_receipt(receipt, master, report)
        if clean:
            clear_intermediates(video, receipt)
        print(f"{video}: verified at {report['loudness_lufs']:.1f} LUFS, "
              f"{report['true_peak_dbtp']:.1f} dBTP", flush=True)
    except (subprocess.CalledProcessError, OSError, ValueError, KeyError, TypeError) as error:
        print(f"{video}: deferred ({error}); see {log}", flush=True)
        return False
    return True


def free_space():
    return min(shutil.disk_usage(ROOT).free, shutil.disk_usage(OUTPUT.resolve().parent).free)


def main() -> int:
    parts = available_parts()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parts", type=int, choices=parts, nargs="+", metavar="PART",
                        help="part numbers to render (default: every numbered part)")
    parser.add_argument("-j", "--jobs", type=int, default=3, help="parallel scene renders per part")
    parser.add_argument("--min-free-gib", type=float, default=6, help="free space needed to start a part")
    parser.add_argument("--clean", action="store_true", help="keep cue sheets and discard verified scene intermediates")
    parser.add_argument("--force", action="store_true", help="rebuild masters with existing receipts")
    args = parser.parse_args()
    if args.jobs < 1 or not args.min_free_gib > 0:
        parser.error("jobs and minimum free space must be positive")
    if os.environ.get("EXPLAINER_TTS") != "server":
        parser.error("start the narration server and set EXPLAINER_TTS=server")

    os.environ.setdefault("EXPLAINER_VOICE", "qwen3-calm-a")
    (STATE / "logs").mkdir(parents=True, exist_ok=True)
    with (STATE / "run.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            parser.error("another Music render queue is already running in this checkout")
        failed = []
        # The next part can use the narration GPU while the previous part's
        # picture is stream-copied and its soundtrack encoded and measured.
        with ThreadPoolExecutor(max_workers=1) as pool:
            pending = None

            def wait_for_master():
                nonlocal pending
                if pending is not None:
                    name, future = pending
                    if not future.result():
                        failed.append(name)
                    pending = None

            for part in sorted(set(args.parts or parts)):
                video = f"music{part}"
                master = OUTPUT / f"{video}_2160p.mp4"
                receipt = OUTPUT / "qa" / "music-master" / f"{video}.json"
                log = STATE / "logs" / f"{video}.log"
                if not args.force and complete(master, receipt):
                    print(f"{video}: verified master already exists", flush=True)
                    continue
                if free_space() < args.min_free_gib * 1024**3:
                    wait_for_master()
                    if free_space() < args.min_free_gib * 1024**3:
                        print(f"{video}: paused for space (needs {args.min_free_gib:g} GiB free)", flush=True)
                        return 1
                print(f"{video}: rendering with {args.jobs} scene workers ({log})", flush=True)
                build = [sys.executable, "tools/build.py", video, "--lang", "en", "-q", "k", "--fps", "60",
                         "--crf", "16", "-j", str(args.jobs)]
                try:
                    run_step(log, sys.executable, "tools/make.py", video, "--steps", "compute")
                    run_step(log, *build, "--scenes-only")
                except (subprocess.CalledProcessError, OSError) as error:
                    failed.append(video)
                    print(f"{video}: deferred ({error}); see {log}", flush=True)
                    continue
                wait_for_master()
                pending = video, pool.submit(finish_part, video, build, args.clean)
            wait_for_master()
        if failed:
            print(f"Deferred parts: {', '.join(failed)}", flush=True)
        return int(bool(failed))


if __name__ == "__main__":
    sys.exit(main())
