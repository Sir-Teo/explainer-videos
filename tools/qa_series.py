#!/usr/bin/env python
"""Inspect current scenes in manifest order, with one isolated process per chapter.

    python tools/qa_series.py ai1
    python tools/qa_series.py --series ai --cached-only --resume
    python tools/qa_series.py ai1 --lang zh --only Entropy
    python tools/qa_series.py ai1 --motion --cached-only --timeout 1200

Saves narration-beat images, contact sheets, geometry warnings and full tracebacks
under renders/qa/series/. Animation endpoints are evaluated, not intermediate frames:
this is a layout/runtime preflight, not a substitute for watching narrated renders.
Use --motion for real silent 480p15 playback and a dead-air scan, saved separately.
Missing computations can be reported without starting training (--cached-only).
Results are content-keyed; a changed shared helper invalidates --resume results.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import importlib
import json
import os
import re
import signal
import shutil
import subprocess
import sys
import time
import traceback
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
OUT = ROOT / "renders" / "qa" / "series"


class StaleDataError(RuntimeError):
    """A cache exists but cannot satisfy the current scene's data schema."""


def require_part1_cache(compute, name):
    """Cached-only QA must never invoke a schema upgrade's computation."""
    if not compute.path(name).exists():
        raise FileNotFoundError(f"QA needs computed data: ai1/{name}")
    if not compute.cache_current(name):
        raise StaleDataError(f"QA found stale computed data: ai1/{name}; rebuild this item before rendering")


def visible_text_bounds(m, camera=None):
    """Measure visible glyphs in screen space, including 3D camera projection."""
    visible = []
    for glyph in m.get_family():
        if glyph.has_points() and max(glyph.get_fill_opacity(), glyph.get_stroke_opacity()) >= 0.05:
            points = glyph.points
            if camera is not None:
                points = camera.transform_points_pre_display(glyph, points)
                if hasattr(camera, "frame"):  # MovingCamera keeps points in world coordinates.
                    from manim import config

                    points = points.copy()
                    points[:, :2] -= camera.frame_center[:2]
                    points[:, 0] *= config.frame_width / camera.frame_width
                    points[:, 1] *= config.frame_height / camera.frame_height
            visible.append(points)
    if not visible:
        return None
    return [min(float(p[:, 0].min()) for p in visible),
            max(float(p[:, 0].max()) for p in visible),
            min(float(p[:, 1].min()) for p in visible),
            max(float(p[:, 1].max()) for p in visible)]


def fingerprint(video):
    files = sorted((ROOT / "explainer").rglob("*.py"))
    series = ROOT / "videos" / "ai"
    files += sorted(p for p in series.iterdir() if p.suffix in (".py", ".json"))
    # A change in Part 30 should not invalidate Part 1's long motion render.
    # Include the requested part and every part referenced by its Python code,
    # transitively, as well as all shared helpers and language tables.
    pending, seen = [video], set()
    while pending:
        part = pending.pop()
        if part in seen:
            continue
        seen.add(part)
        part_files = sorted(p for p in (series / part).rglob("*") if p.suffix in (".py", ".json"))
        files += part_files
        for p in part_files:
            if p.suffix == ".py":
                src = p.read_text()
                for match in re.findall(r"videos\.ai\.(ai\d+)\b|Cache\([\"'](ai\d+)[\"']\)", src):
                    pending.extend(name for name in match if name)
    files += [Path(__file__), ROOT / "tools" / "dead_air.py", ROOT / "manim.cfg"]
    h = hashlib.sha256()
    for p in files:
        h.update(str(p.relative_to(ROOT)).encode())
        h.update(p.read_bytes())
    return h.hexdigest()


def data_signature(path):
    if not path.exists():
        return None
    stat = path.stat()
    return [stat.st_size, stat.st_mtime_ns]


def inputs_current(result):
    return "inputs" in result and all(data_signature(ROOT / p) == sig for p, sig in result["inputs"].items())


def runtime_completed(result):
    """Warnings require review but do not discard a completed narration capture."""
    return result.get("status") in ("passed", "needs-review")


def preflight_passed(result):
    # Also handles older records whose status was passed despite warnings.
    return result.get("status") == "passed" and not result.get("warnings")


def check_status(result):
    """Normalize older records that labelled warning-bearing runs as passed."""
    return "needs-review" if result.get("status") == "passed" and result.get("warnings") else result.get("status")


def sheet(paths, out, cols=4, width=427):
    from PIL import Image, ImageDraw

    if not paths:
        return
    height = round(width * 9 / 16)
    tile_h = height + 24
    im = Image.new("RGB", (cols * width, ((len(paths) + cols - 1) // cols) * tile_h), "#30343b")
    draw = ImageDraw.Draw(im)
    for i, p in enumerate(paths):
        x, y = i % cols * width, i // cols * tile_h
        with Image.open(p) as frame:
            im.paste(frame.convert("RGB").resize((width, height)), (x, y + 24))
        draw.text((x + 6, y + 4), p.stem, fill="white")
    im.save(out)


def worker(args):
    folder = OUT / args.video / args.lang / (args.worker + ("_motion" if args.motion else ""))
    folder.mkdir(parents=True, exist_ok=True)
    # A focused recheck can overlap a queued run. Serialize the same chapter's
    # TeX cache and evidence writes; different chapters/languages stay independent.
    chapter_lock = (folder / ".lock").open("a")
    fcntl.flock(chapter_lock, fcntl.LOCK_EX)
    if args.motion:
        # TeX SVGs are content-addressed and independent of output resolution.
        # Reuse a successful endpoint run instead of compiling every equation
        # again. Never read its cache while another endpoint worker writes it.
        endpoint = folder.with_name(args.worker)
        endpoint_result = endpoint / "result.json"
        if endpoint_result.exists():
            with (endpoint / ".lock").open("a") as source_lock:
                try:
                    fcntl.flock(source_lock, fcntl.LOCK_SH | fcntl.LOCK_NB)
                except BlockingIOError:
                    pass
                else:
                    if runtime_completed(json.loads(endpoint_result.read_text())):
                        (folder / "Tex").mkdir(exist_ok=True)
                        for svg in (endpoint / "Tex").glob("*.svg"):
                            target = folder / "Tex" / svg.name
                            if not target.exists():
                                shutil.copyfile(svg, target)
    text_record = folder / "text.jsonl"
    text_record.write_text("")
    os.environ.update(EXPLAINER_TTS="silent", EXPLAINER_LANG=args.lang, EXPLAINER_VIDEO=args.video,
                      EXPLAINER_COLLECT_TEXT="" if args.motion else str(text_record),
                      PYTHONWARNINGS="ignore", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1")
    from manim import MathTex, Tex, Text, config, tempconfig
    from explainer.paths import video_package
    from explainer.voiceover import VoiceoverScene

    result = {"video": args.video, "scene": args.worker, "lang": args.lang, "status": "running",
              "mode": "motion" if args.motion else "endpoints",
              "fingerprint": fingerprint(args.video), "inputs": {}, "frames": [], "warnings": [],
              "visual_review": "pending", "full_playback_review": "pending",
              "narrated_playback_review": "pending"}
    original_vo, original_wait = VoiceoverScene.voiceover, VoiceoverScene.wait
    active = []
    last_image = None

    def capture(scene, reason):
        nonlocal last_image
        scene.renderer.static_image = None
        scene.renderer.update_frame(scene)
        pixels = scene.renderer.get_frame()
        digest = hashlib.sha256(pixels.tobytes()).hexdigest()
        if digest == last_image:
            return
        last_image = digest
        from PIL import Image
        import numpy as np

        i = len(result["frames"])
        name = f"{i:03d}_{scene.renderer.time:07.1f}s.png"
        Image.fromarray(pixels).save(folder / name)
        bg = np.array(config.background_color.to_rgb()) * 255
        coverage = float((np.abs(pixels[:, :, :3].astype(float) - bg).max(axis=2) > 24).mean())
        texts, visited = [], set()
        for root in scene.mobjects:
            for m in root.get_family():
                if id(m) in visited or not isinstance(m, (Tex, MathTex, Text)):
                    continue
                visited.update(id(c) for c in m.get_family())
                if not m.has_points() and not m.submobjects:
                    continue
                bounds = visible_text_bounds(m, scene.camera)
                if bounds is None:
                    continue
                s = getattr(m, "tex_string", getattr(m, "text", ""))
                texts.append({"text": s, "bounds": bounds})
                if (bounds[0] < -config.frame_width / 2 - 0.03 or
                        bounds[1] > config.frame_width / 2 + 0.03 or
                        bounds[2] < -config.frame_height / 2 - 0.03 or
                        bounds[3] > config.frame_height / 2 + 0.03):
                    result["warnings"].append({"kind": "text-outside-frame", "frame": name,
                                               "text": s, "bounds": bounds})
        result["frames"].append({"file": name, "time": scene.renderer.time, "reason": reason,
                                 "coverage": coverage, "texts": texts})
        if coverage < 0.0005:
            result["warnings"].append({"kind": "blank-narration-beat", "frame": name, "reason": reason})

    @contextmanager
    def voiceover(self, text, *a, **kw):
        with original_vo(self, text, *a, **kw) as tracker:
            active.append(text)
            try:
                yield tracker
                capture(self, "narration-end")
            finally:
                active.pop()

    def wait(self, duration=1, *a, **kw):
        if active and duration >= 1.5:
            capture(self, f"narrated-hold-{duration:.1f}s")
        return original_wait(self, duration, *a, **kw)

    VoiceoverScene.voiceover, VoiceoverScene.wait = voiceover, wait
    from explainer.ai.cache import Cache
    from explainer.cache_lock import cache_lock
    from videos.ai.ai1 import compute as c1
    original_load, original_c1 = Cache.load, c1.load

    def record_data(path):
        for p in (path, path.with_suffix(".npz")):
            key, signature = str(p.relative_to(ROOT)), data_signature(p)
            if key in result["inputs"] and result["inputs"][key] != signature:
                warning = {"kind": "input-changed-during-render", "path": key}
                if warning not in result["warnings"]:
                    result["warnings"].append(warning)
            else:
                result["inputs"][key] = signature

    def load(cache, name):
        if args.cached_only and not cache.path(name).exists():
            raise FileNotFoundError(f"QA needs computed data: {cache.part}/{name}")
        with cache_lock(cache.path(name)):
            value = original_load(cache, name)
            record_data(cache.path(name))
        return value

    def load1(name):
        with cache_lock(c1.path(name)):
            if args.cached_only:
                require_part1_cache(c1, name)
            value = original_c1(name)
            record_data(c1.path(name))
        return value

    Cache.load, c1.load = load, load1

    start = time.monotonic()
    try:
        manifest = importlib.import_module(f"{video_package(args.video)}.manifest")
        module = next(m for m, cls, _ in manifest.SCENES if cls == args.worker)
        with tempconfig({"dry_run": not args.motion, "quality": "low_quality", "verbosity": "ERROR",
                         "media_dir": str(folder / "media"), "tex_dir": str(folder / "Tex"),
                         "text_dir": str(folder / "texts"), "disable_caching": True,
                         "progress_bar": "none"}):
            cls = getattr(importlib.import_module(f"{video_package(args.video)}.{module}"), args.worker)
            scene = cls(skip_animations=not args.motion)
            scene.render()
            result.update(status="passed", duration=scene.renderer.time, narration=scene._narration)
            if args.motion:
                movie = Path(scene.renderer.file_writer.movie_file_path)
                if not movie.exists():
                    raise RuntimeError("motion render did not produce a video")
                result["movie"] = str(movie.relative_to(ROOT))
                scan = subprocess.run([sys.executable, str(ROOT / "tools" / "dead_air.py"), str(movie)],
                                      capture_output=True, text=True, check=True)
                result["dead_air"] = scan.stdout
                (folder / "dead_air.log").write_text(scan.stdout)
                if re.search(r"runs >= [\d.]+ s: [1-9]", scan.stdout):
                    result["warnings"].append({"kind": "dead-air-review", "report": scan.stdout})
                subprocess.run([sys.executable, str(ROOT / "tools" / "contact_sheet.py"), str(movie),
                                "-n", "40", "-c", "4", "-o", str(folder / "motion_sheet.png")],
                               capture_output=True, text=True, check=True)
            if args.lang == "en":
                from explainer import lang
                from explainer.paths import video_dir
                from tools.translate_narration import problems

                lang.LANG = "zh"
                try:
                    for line in scene._narration:
                        try:
                            translated = lang.translate(line["raw"], video_dir(args.video), args.worker)
                            errors = [p for p in problems(line["raw"], translated, "zh")
                                      if not p.startswith("Latin words left")]
                        except (KeyError, ValueError) as exc:
                            errors = [str(exc)]
                        if errors:
                            result["warnings"].append({"kind": "narration-translation", "text": line["raw"],
                                                       "errors": errors})
                finally:
                    lang.LANG = "en"
            # Collect the original strings even in a Chinese run. Verbatim model
            # input/output is excluded by data_text's existing collection guard.
            from explainer import lang, zh_text

            lang.LANG = "zh"
            try:
                table = zh_text._table().get("strings", {})
                translated_targets = {zh_text._NUM.sub("\0", zh_text.translate(s)) for s in table}
                # Technical names explicitly retained by approved translations
                # are also valid in numeric/regex caption variants.
                names = {name for value in table.values() if zh_text.CJK.search(value)
                         for name in re.findall(r"(?<![A-Za-z0-9_])(?:[A-Z]{2,}[A-Za-z0-9]*|[A-Za-z]+[A-Z][A-Za-z0-9]*)(?![A-Za-z0-9_])", value)}
                names_pattern = re.compile(r"(?<![A-Za-z0-9_])(?:" + "|".join(re.escape(n) for n in sorted(names, key=len, reverse=True)) + r")(?![A-Za-z0-9_])")
                seen = set()
                for line in text_record.read_text().splitlines():
                    entry = json.loads(line)
                    text = entry["s"]
                    if text in seen or not entry["needs"] or text in table:
                        continue
                    # TeX can construct subobjects from an already translated
                    # string. Bibliographic titles and model names stay Latin.
                    if zh_text._NUM.sub("\0", text) in translated_targets:
                        continue
                    # chapter_card and narration_credit select their Chinese
                    # wording in code, rather than through the text table.
                    if re.match(r"Part \d+ \\textperiodcentered|Animated with Manim", text):
                        continue
                    seen.add(text)
                    translated = zh_text.translate(text)
                    if translated != text and zh_text.CJK.search(translated):
                        translated = names_pattern.sub("", translated)
                    if zh_text.needs_translation(translated, entry["kind"] == "MathTex"):
                        result["warnings"].append({"kind": "untranslated-on-screen", "text": text})
            finally:
                lang.LANG = args.lang
    except Exception as exc:
        result.update(status=("stale-data" if isinstance(exc, StaleDataError) else
                              "missing-data" if "QA needs computed data:" in str(exc) else "failed"),
                      error=f"{type(exc).__name__}: {exc}", traceback=traceback.format_exc())
        traceback.print_exc()
    result["elapsed"] = round(time.monotonic() - start, 2)
    if runtime_completed(result) and result["fingerprint"] != fingerprint(args.video):
        result["warnings"].append({"kind": "source-changed-during-render"})
    if runtime_completed(result) and not inputs_current(result):
        result["warnings"].append({"kind": "input-changed-during-render"})
    if result["status"] == "passed" and result["warnings"]:
        result["status"] = "needs-review"
    (folder / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=1))
    sheet([folder / f["file"] for f in result["frames"]], folder / "sheet.png")
    return 0 if preflight_passed(result) else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", nargs="?")
    ap.add_argument("--series")
    ap.add_argument("--start-at", help="start the series at this part (inclusive)")
    ap.add_argument("--lang", default="en", choices=["en", "zh"])
    ap.add_argument("--only", nargs="+")
    ap.add_argument("--cached-only", action="store_true")
    ap.add_argument("--motion", action="store_true", help="render real silent playback and scan for dead air")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--timeout", type=int, default=240)
    ap.add_argument("--worker", help=argparse.SUPPRESS)
    args = ap.parse_args()
    if args.worker:
        return worker(args)
    from tools.make import all_videos
    from explainer.paths import video_package

    videos = [args.video] if args.video else all_videos(args.series or "ai")
    if args.start_at:
        videos = videos[videos.index(args.start_at):]
    if args.only:
        known = {cls for video in videos
                 for _, cls, _ in importlib.import_module(f"{video_package(video)}.manifest").SCENES}
        unknown = set(args.only) - known
        if unknown:
            ap.error(f"--only contains unknown chapters: {', '.join(sorted(unknown))}")
    summary = []
    for video in videos:
        key = fingerprint(video)
        manifest = importlib.import_module(f"{video_package(video)}.manifest")
        overview = []
        for _, cls, _ in manifest.SCENES:
            if args.only and cls not in args.only:
                continue
            folder = OUT / video / args.lang / (cls + ("_motion" if args.motion else ""))
            folder.mkdir(parents=True, exist_ok=True)
            path = folder / "result.json"
            old = json.loads(path.read_text()) if path.exists() else {}
            if not (args.resume and old.get("fingerprint") == key and runtime_completed(old)
                    and inputs_current(old)):
                cmd = [sys.executable, str(Path(__file__)), video, "--worker", cls, "--lang", args.lang]
                if args.cached_only:
                    cmd.append("--cached-only")
                if args.motion:
                    cmd.append("--motion")
                with (folder / "render.log").open("w") as log:
                    try:
                        proc = subprocess.Popen(cmd, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                                                start_new_session=True)
                        rc = proc.wait(timeout=args.timeout)
                    except subprocess.TimeoutExpired:
                        os.killpg(proc.pid, signal.SIGTERM)
                        try:
                            proc.wait(timeout=5)
                        except subprocess.TimeoutExpired:
                            os.killpg(proc.pid, signal.SIGKILL)
                            proc.wait()
                        rc = -1
                if rc and (not path.exists() or json.loads(path.read_text()) == old):
                    path.write_text(json.dumps({"video": video, "scene": cls, "lang": args.lang,
                                                "status": "timeout" if rc == -1 else "crashed",
                                                "mode": "motion" if args.motion else "endpoints",
                                                "error": f"worker exit code {rc}",
                                                "fingerprint": key, "frames": [], "warnings": []}))
            r = json.loads(path.read_text())
            r["status"] = check_status(r)
            frames = r.get("frames", [])
            if frames:
                best = max(frames, key=lambda f: f["coverage"])
                overview.append(folder / best["file"])
            summary.append({k: r.get(k) for k in ("video", "scene", "lang", "status", "error", "elapsed")}
                           | {"warnings": len(r.get("warnings", [])), "frames": len(frames)})
            print(f"{video:5} {cls:20} {r['status']:12} {len(frames):3} frames  "
                  f"{len(r.get('warnings', [])):3} warnings  {r.get('error', '')}", flush=True)
            (OUT / video / args.lang / ("summary_motion.json" if args.motion else "summary.json")).write_text(json.dumps(
                [row for row in summary if row["video"] == video], ensure_ascii=False, indent=1))
        # Copy a representative frame per chapter with the chapter name as its tile label.
        thumbs = []
        import shutil
        for p in overview:
            dst = p.parents[1] / f"{p.parent.name}.png"
            shutil.copyfile(p, dst)
            thumbs.append(dst)
        sheet(thumbs, OUT / video / args.lang / ("overview_motion.png" if args.motion else "overview.png"))
    # Separate runs (for example English and Chinese, or adjacent parts) keep
    # independent chapter records. Aggregate those instead of dropping earlier runs.
    records = [r for p in sorted(OUT.glob(f"*/{args.lang}/*/result.json"))
               if (r := json.loads(p.read_text())).get("mode", "endpoints") == ("motion" if args.motion else "endpoints")]
    compact = [{k: r.get(k) for k in ("video", "scene", "lang", "status", "error", "elapsed")}
               | {"status": check_status(r)}
               | {"warnings": len(r.get("warnings", [])), "frames": len(r.get("frames", []))} for r in records]
    suffix = f"{args.lang}" + ("_motion" if args.motion else "")
    tmp = OUT / f"summary_{suffix}.{os.getpid()}.tmp"
    tmp.write_text(json.dumps(compact, ensure_ascii=False, indent=1))
    tmp.replace(OUT / f"summary_{suffix}.json")
    return int(any(not preflight_passed(r) for r in summary))


if __name__ == "__main__":
    sys.exit(main())
