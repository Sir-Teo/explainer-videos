#!/usr/bin/env python
"""Decode a whole video and prepare time-indexed transition frames for review.

    python tools/qa_motion.py chapter.mp4 -o renders/qa/temporal/chapter

Every source frame is decoded, without temporal subsampling. Changes are measured
at a smaller RGB resolution; consecutive changes separated by <= --gap
seconds form one motion interval. Each interval supplies its boundary, midpoint,
and at least one sample per --dense seconds. Static intervals supply a midpoint.
The selected frames are extracted at native resolution into paginated sheets.

This is an automated detection/extraction audit, NOT continuous perceptual
playback or a visual sign-off. At each pixel the largest absolute channel change
is compared with --pixel-delta; its pixel fraction and normalized spatial mean
must meet their thresholds. Small or subtle changes can still escape detection.
JSON records these limits and every selected source time.
Pixel processing streams one frame at a time; timestamp/interval metadata scales
with the number of source frames. FFmpeg uses one decoding/filter/encoding thread.
"""

from __future__ import annotations

import argparse
import bisect
import hashlib
import html
import json
import math
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def probe(path):
    command = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_streams", "-show_frames",
               "-show_entries", "stream=width,height,avg_frame_rate,duration:frame=best_effort_timestamp_time",
               "-of", "json", str(path)]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    data = json.loads(result.stdout)
    stream = data["streams"][0]
    times = [float(frame["best_effort_timestamp_time"]) for frame in data["frames"]]
    if not times or any(b <= a for a, b in zip(times, times[1:])):
        raise ValueError("video needs nonempty, strictly increasing frame timestamps")
    stream["fps"] = float(Fraction(stream["avg_frame_rate"]))
    return stream, times


def read_frame(pipe, size):
    """Pipes may return short reads before EOF."""
    pieces, remaining = [], size
    while remaining:
        chunk = pipe.read(remaining)
        if not chunk:
            break
        pieces.append(chunk)
        remaining -= len(chunk)
    raw = b"".join(pieces)
    if raw and len(raw) != size:
        raise ValueError("FFmpeg returned a truncated raw frame")
    return raw


def detect(path, times, stream, *, width, pixel_delta, changed_fraction, mean_delta, gap):
    height = max(1, round(stream["height"] * width / stream["width"]))
    command = ["ffmpeg", "-v", "error", "-xerror", "-err_detect", "explode", "-threads", "1", "-i", str(path),
               "-map", "0:v:0", "-an", "-sn", "-filter_threads", "1", "-vf",
               f"scale={width}:{height}:flags=area,format=rgb24", "-vsync", "0", "-f", "rawvideo", "-"]
    intervals, first, last, previous, count = [], None, None, None, 0
    peak_fraction = peak_mean = 0.0
    with tempfile.TemporaryFile() as errors:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=errors)
        try:
            while raw := read_frame(process.stdout, width * height * 3):
                if count >= len(times):
                    raise ValueError("decoder emitted more frames than timestamp probe")
                frame = np.frombuffer(raw, np.uint8).reshape(height, width, 3).astype(np.int16)
                changed = False
                if previous is not None:
                    delta = np.abs(frame - previous).max(axis=2)
                    fraction = float((delta >= pixel_delta).mean())
                    mean = float(delta.mean()) / 255
                    peak_fraction, peak_mean = max(peak_fraction, fraction), max(peak_mean, mean)
                    changed = fraction >= changed_fraction and mean >= mean_delta
                if changed:
                    if first is None:
                        first = max(count - 1, 0)
                    last = count
                elif first is not None and times[count] - times[last] > gap:
                    intervals.append((first, last))
                    first = last = None
                previous = frame
                count += 1
            if process.wait() != 0:
                errors.seek(0)
                raise RuntimeError("full-frame decode failed: " + errors.read().decode(errors="replace")[-2000:])
        finally:
            process.stdout.close()
            if process.poll() is None:
                process.kill()
                process.wait()
    if count != len(times):
        raise ValueError(f"full-frame decode count {count} differs from timestamp count {len(times)}")
    if first is not None:
        intervals.append((first, last))
    return intervals, {"decoded_frames": count, "analysis_width": width, "analysis_height": height,
                       "peak_changed_fraction": peak_fraction, "peak_mean_delta": peak_mean}


def select_frames(times, intervals, dense):
    selected = {}

    def add(index, reason):
        selected.setdefault(index, set()).add(reason)

    def at(time):
        return min(bisect.bisect_left(times, time), len(times) - 1)

    add(0, "file-start")
    add(len(times) - 1, "file-last-frame")
    previous_end = 0
    for number, (start, end) in enumerate(intervals):
        prefix = f"motion-{number:03d}"
        if start > previous_end:
            add(at((times[previous_end] + times[start]) / 2), "static-midpoint")
        for index, reason in ((start, "before"), (min(start + 1, end), "onset"),
                              (at((times[start] + times[end]) / 2), "midpoint"),
                              (end, "last-change"), (min(end + 1, len(times) - 1), "after")):
            add(index, prefix + ":" + reason)
        time = times[start] + dense
        while time < times[end]:
            add(at(time), prefix + ":dense")
            time += dense
        previous_end = min(end + 1, len(times) - 1)
    if previous_end < len(times) - 1:
        add(at((times[previous_end] + times[-1]) / 2), "static-midpoint")
    return [{"source_frame": i, "time": times[i], "reasons": sorted(selected[i])} for i in sorted(selected)]


def extract(path, out, selected):
    out.mkdir(parents=True, exist_ok=True)
    # A long left-associative sum exhausts FFmpeg's expression parser recursion
    # limit even on a modest chapter. A balanced tree has logarithmic depth.
    terms = [f"eq(n\\,{frame['source_frame']})" for frame in selected]
    while len(terms) > 1:
        terms = [f"({terms[i]}+{terms[i + 1]})" if i + 1 < len(terms) else terms[i]
                 for i in range(0, len(terms), 2)]
    expression = terms[0]
    with tempfile.TemporaryDirectory(dir=out) as temporary:
        temp = Path(temporary)
        script = temp / "select.txt"
        script.write_text("select=" + expression)
        result = subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-threads", "1", "-i", str(path), "-map", "0:v:0",
                                 "-an", "-sn", "-filter_threads", "1", "-filter_script:v", str(script), "-vsync", "0",
                                 "-threads", "1", str(temp / "%06d.png")], capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError("native-frame extraction failed: " + result.stderr[:1500] + result.stderr[-500:])
        images = sorted(temp.glob("*.png"))
        if len(images) != len(selected):
            raise ValueError("native-frame extraction count disagrees with selected source frames")
        for image, record in zip(images, selected):
            name = f"{record['source_frame']:07d}_{record['time']:010.3f}s.png"
            image.replace(out / name)
            record["file"] = "frames/" + name
            record["sha256"] = sha256(out / name)


def sheets(out, selected, *, tile_width=640, cols=2, rows=4):
    pages = []
    for page, offset in enumerate(range(0, len(selected), cols * rows)):
        chunk = selected[offset:offset + cols * rows]
        tiles = []
        for record in chunk:
            with Image.open(out / record["file"]) as native:
                tile_height = round(native.height * tile_width / native.width)
                tile = Image.new("RGB", (tile_width, tile_height + 34), "#202732")
                tile.paste(native.convert("RGB").resize((tile_width, tile_height)), (0, 34))
            draw = ImageDraw.Draw(tile)
            draw.text((8, 3), f"{record['time']:.3f}s / source frame {record['source_frame']}", fill="white")
            draw.text((8, 18), ", ".join(record["reasons"]), fill="#c6d6e9")
            tiles.append(tile)
        width, height = tiles[0].size
        image = Image.new("RGB", (cols * width, math.ceil(len(tiles) / cols) * height), "#0e1117")
        for i, tile in enumerate(tiles):
            image.paste(tile, ((i % cols) * width, (i // cols) * height))
        name = f"sheet-{page + 1:03d}.png"
        image.save(out / name)
        pages.append({"file": name, "first_selected_frame": offset, "frames": len(chunk), "sha256": sha256(out / name)})
    return pages


def provenance(path):
    for folder in path.parents:
        candidate = folder / "result.json"
        if not candidate.is_file():
            continue
        record = json.loads(candidate.read_text())
        root = Path(__file__).resolve().parents[1]
        if record.get("movie") and (root / record["movie"]).resolve() == path:
            from tools.qa_series import fingerprint, inputs_current

            return {"record": str(candidate), "sha256": sha256(candidate),
                    "fingerprint": record.get("fingerprint"), "status": record.get("status"),
                    "current_source_and_inputs": record.get("fingerprint") == fingerprint(record["video"])
                                                 and inputs_current(record)}
    return None


def _audit(path, out, *, width=320, pixel_delta=8, changed_fraction=0.0005, mean_delta=0.0001, gap=0.2, dense=1.0):
    path, out = Path(path).resolve(), Path(out).resolve()
    if (width < 1 or dense <= 0 or gap < 0 or not (1 <= pixel_delta <= 255)
            or not (0 < changed_fraction <= 1) or not (0 <= mean_delta <= 1)):
        raise ValueError("invalid temporal audit settings")
    original_hash = sha256(path)
    tool_hash = sha256(Path(__file__))
    stream, times = probe(path)
    intervals, analysis = detect(path, times, stream, width=width, pixel_delta=pixel_delta,
                                 changed_fraction=changed_fraction, mean_delta=mean_delta, gap=gap)
    selected = select_frames(times, intervals, dense)
    out.mkdir(parents=True, exist_ok=True)
    extract(path, out / "frames", selected)
    pages = sheets(out, selected)
    if sha256(path) != original_hash:
        raise ValueError("source video changed during the audit; output is not stable evidence")
    if sha256(Path(__file__)) != tool_hash:
        raise ValueError("audit tool changed during the audit; rerun with a stable algorithm")
    duration = float(stream.get("duration", times[-1] + 1 / stream["fps"]))
    report = {"status": "automated-temporal-audit-completed", "source": str(path), "source_sha256": original_hash,
              "tool_sha256": tool_hash, "algorithm": "rgb-max-channel-v1", "color_space": "RGB24",
              "source_width": stream["width"], "source_height": stream["height"], "average_fps": stream["fps"],
              "duration": duration, "first_decoded_time": times[0], "last_decoded_time": times[-1],
              "settings": {"pixel_delta": pixel_delta, "changed_fraction": changed_fraction,
                           "mean_delta": mean_delta, "mean_delta_definition": "spatial mean of max-channel absolute RGB delta / 255",
                           "static_gap_seconds": gap, "dense_motion_seconds": dense},
              "analysis": analysis, "provenance": provenance(path),
              "motion_intervals": [{"first_frame": a, "last_frame": b, "start": times[a], "end": times[b]}
                                   for a, b in intervals],
              "selected_frames": selected, "pages": pages,
              "unextracted_frame_gaps": [{"after_frame": a["source_frame"], "before_frame": b["source_frame"],
                                           "start": a["time"], "end": b["time"],
                                           "unextracted_frames": b["source_frame"] - a["source_frame"] - 1}
                                          for a, b in zip(selected, selected[1:])
                                          if b["source_frame"] - a["source_frame"] > 1],
              "largest_selected_time_gap": max((b["time"] - a["time"] for a, b in zip(selected, selected[1:])), default=0),
              "manual_frame_review": "pending", "continuous_perceptual_playback": "unverified",
              "narration_listening_and_synchronization": "unverified",
              "coverage_limits": ["Every source frame was decoded and analyzed, not visually inspected.",
                                  "Only listed native-resolution times were extracted; review of those images is pending.",
                                  "Low-resolution RGB thresholds can miss small or subtle spatial/channel changes.",
                                  "Static interval midpoints are samples, not proof that their full intervals are unchanged.",
                                  "Full perceptual playback and listening remain unverified."]}
    (out / "result.json").write_text(json.dumps(report, indent=2) + "\n")
    links = "".join(f'<li><a href="{p["file"]}">{p["file"]}</a> ({p["frames"]} frames)</li>' for p in pages)
    frame_links = "".join(f'<li><a href="{f["file"]}">{f["time"]:.3f}s — frame {f["source_frame"]}</a></li>' for f in selected)
    (out / "index.html").write_text('<!doctype html><meta charset="utf-8"><title>Temporal frame evidence</title>'
        '<style>body{font:17px/1.5 system-ui;max-width:900px;margin:40px auto;background:#0e1117;color:#ddd}a{color:#8ecaff}</style>'
        f'<h1>Time-indexed frame evidence</h1><p>{html.escape(path.name)}: {analysis["decoded_frames"]} source frames decoded; '
        f'{len(intervals)} detected motion intervals; {len(selected)} selected images.</p>'
        '<p>Automated detection/extraction only. Image review is pending. Continuous perceptual playback, listening '
        'and synchronization remain unverified. See <a href="result.json">exact coverage and limits</a>.</p>'
        f'<h2>Contact sheets</h2><ul>{links}</ul><h2>Native frames</h2><ul>{frame_links}</ul>')
    return report


def audit(path, out, **settings):
    """An interrupted/failed refresh must not leave an earlier completed verdict."""
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    result = out / "result.json"
    result.write_text(json.dumps({"status": "running", "source": str(Path(path).resolve())}) + "\n")
    try:
        return _audit(path, out, **settings)
    except Exception as error:
        result.write_text(json.dumps({"status": "failed", "source": str(Path(path).resolve()),
                                      "error": f"{type(error).__name__}: {error}",
                                      "manual_frame_review": "pending"}, indent=2) + "\n")
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("video", type=Path)
    parser.add_argument("-o", "--out", required=True, type=Path)
    parser.add_argument("--width", type=int, default=320)
    parser.add_argument("--pixel-delta", type=int, default=8)
    parser.add_argument("--changed-fraction", type=float, default=0.0005)
    parser.add_argument("--mean-delta", type=float, default=0.0001)
    parser.add_argument("--gap", type=float, default=0.2)
    parser.add_argument("--dense", type=float, default=1.0)
    args = parser.parse_args()
    report = audit(args.video, args.out, width=args.width, pixel_delta=args.pixel_delta,
                   changed_fraction=args.changed_fraction, mean_delta=args.mean_delta, gap=args.gap, dense=args.dense)
    print(f'{report["analysis"]["decoded_frames"]} frames decoded; {len(report["motion_intervals"])} motion intervals; '
          f'{len(report["selected_frames"])} selected frames; {len(report["pages"])} sheets; visual review pending')


if __name__ == "__main__":
    main()
