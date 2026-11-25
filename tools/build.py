#!/usr/bin/env python
"""Render a video's scenes in parallel and stitch them into one file.

    python tools/build.py navier_stokes                 # 1080p30 final cut
    python tools/build.py navier_stokes -q l            # fast 480p preview
    python tools/build.py navier_stokes --only Pressure Viscosity
    python tools/build.py navier_stokes --stitch-only   # reuse rendered scenes
    python tools/build.py analysis1 --lang zh           # Chinese narration (videos/analysis/analysis1/narration_zh.json)

Outputs (in ``renders/``):
    <video>[_<quality>][_<lang>].mp4   video + narration (loudness-normalized) + soft subtitles + chapters
    <video>.srt            subtitles
    <video>.chapters.txt   YouTube-style chapter list
"""

from __future__ import annotations

import argparse
import importlib
import json
import re
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from fractions import Fraction
from pathlib import Path
from tempfile import NamedTemporaryFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from explainer.paths import video_dir, video_package  # noqa: E402

from explainer import lang as narration_lang  # noqa: E402
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
    if m["input_i"] == "-inf":  # a silent soundtrack (EXPLAINER_TTS=silent): nothing to normalize
        return HIGHPASS
    return (f"{HIGHPASS},{LOUDNORM}:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
            f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
            f":offset={m['target_offset']}:linear=true")


# Music, Built: scenes that play computed clips (explainer/music/sound.py) write a cue sheet beside each render.  The
# master's music is mixed from those cues in float, stereo, 48 kHz, and joins the narration here.  The narration alone
# is high-passed and brought to -16 LUFS by one constant gain; the music stem's gain is fixed, so the levels written
# in a part's compute.py are the levels in the film.  The voice has a few peaks some 20 dB above its loudness, so
# the narration (and only the narration) passes a look-ahead limiter after its gain; on Part 1 that moves its
# loudness by 0.1 LU.  The music is never limited: a mix over the ceiling stops the build.
MUSIC_GAIN_DB = 0.0
NARRATION_LUFS = -16.0
NARRATION_LIMIT = 0.72   # linear, about -2.9 dBFS: true peaks stay under -1.5 dBTP, with room for a sting on top
PEAK_CEILING_DBTP = -1.0


def music_stem(cues: list[dict], seconds: float, out: Path) -> None:
    """The film's music stem: every cue's clip at its start time and gain, as a float WAV."""
    import numpy as np

    from explainer.music.monochord.audio import Clip, SR, float_wav_header

    frames = round(seconds * SR)
    channels = 2 if cues else 1
    header = float_wav_header(frames, channels, SR)
    pending = sorted((round(c["start"] * SR), i, c) for i, c in enumerate(cues))
    active = []
    index = position = 0
    out.parent.mkdir(parents=True, exist_ok=True)
    stream = NamedTemporaryFile(dir=out.parent, delete=False)
    temporary = Path(stream.name)
    try:
        with stream:
            stream.write(header)
            stream.truncate(len(header) + frames * channels * 4)
            while position < frames and (active or index < len(pending)):
                if not active:
                    position = max(position, pending[index][0])
                end = min(frames, position + SR)
                while index < len(pending) and pending[index][0] < end:
                    start, order, cue = pending[index]
                    index += 1
                    clip = Clip.read(Path(cue["path"]))
                    if clip.sr != SR:
                        raise ValueError("clips of different sample rates")
                    if start + clip.n > position:
                        active.append((order, start, clip.stereo, 10 ** (cue["gain_db"] / 20)))
                if position < end and active:
                    # Preserve addition order even for out-of-order, overlapping cues.
                    block = np.zeros((end - position, 2), dtype=np.float64)
                    for _, start, samples, gain in sorted(active):
                        a, b = max(position, start), min(end, start + len(samples))
                        window = samples[a - start:b - start].astype(np.float64)
                        block[a - position:b - position] += window * gain
                    data = block.astype("<f4")
                    if not np.isfinite(data).all():
                        raise ValueError("a clip must be finite")
                    stream.seek(len(header) + position * 8)
                    stream.write(memoryview(data).cast("B"))
                    active = [item for item in active if item[1] + len(item[2]) > end]
                position = end
        temporary.replace(out)
    finally:
        temporary.unlink(missing_ok=True)


def sound_master(concat_list: Path, voice_input: int, music_input: int) -> str:
    """Measure post-highpass narration loudness and split the final mix for encoding and metering."""
    cmd = ["ffmpeg", "-nostats", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-vn",
           "-af", f"{HIGHPASS},ebur128=framelog=verbose", "-f", "null", "-"]
    levels = run(cmd).stderr.rsplit("Summary:", 1)[-1]
    loudness = float(re.search(r"I:\s+(-?[\d.]+|-inf) LUFS", levels)[1])
    # EBU R128 has an absolute gate at -70 LUFS. A silent narration needs no gain.
    gain = max(-20.0, min(20.0, NARRATION_LUFS - loudness)) if loudness > -70 else 0.0
    print(f"narration gain: {gain:+.1f} dB")
    limiter = f"alimiter=level_in=1:level_out=1:limit={NARRATION_LIMIT}:attack=5:release=80:level=disabled"
    return (f"[{voice_input}:a]{HIGHPASS},volume={gain:.2f}dB,{limiter},aresample=48000[n];"
            f"[{music_input}:a]volume={MUSIC_GAIN_DB:.2f}dB[m];"
            "[n][m]amix=inputs=2:duration=longest:normalize=0,asplit[a][meter];"
            "[meter]ebur128=peak=true:framelog=verbose[levels]")


def check_mix_levels(log: str) -> None:
    summary = log.rsplit("Summary:", 1)[-1]
    peak = float(re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", summary)[1])
    loud = re.search(r"I:\s+(-?[\d.]+) LUFS", summary)[1]
    print(f"soundtrack: mix {loud} LUFS integrated, true peak {peak:.1f} dBTP")
    if peak > PEAK_CEILING_DBTP:
        sys.exit(f"the mixed soundtrack peaks at {peak:.1f} dBTP, above the ceiling of {PEAK_CEILING_DBTP} dBTP: "
                 "lower the clip at its source (python tools/qa_sound.py <video> names it)")


def series_score(video: str):
    """The series' computed score (``explainer/<series>/score.py`` with a ``cues(timeline, cache)``), or None."""
    series = video_dir(video).parent.name
    try:
        mod = importlib.import_module(f"explainer.{series}.score")
    except ModuleNotFoundError:
        return None
    return mod if hasattr(mod, "cues") else None


def scene_output(media: Path, module: str, cls: str, quality: str, fps: int) -> Path:
    return media / "videos" / module / f"{QUALITY[quality]}{fps}" / f"{cls}.mp4"


def repair_segment_cache(scene: Path) -> None:
    """Quarantine incomplete MP4s left by a stopped render before Manim reuses them."""
    import av

    for segment in (scene.parent / "partial_movie_files" / scene.stem).glob("*.mp4"):
        try:
            with av.open(str(segment)) as container:
                if not container.streams.video[0].frames:
                    raise ValueError("Empty segment")
        except (av.error.FFmpegError, IndexError, ValueError):
            segment.replace(segment.with_suffix(".incomplete"))
            print(f"Quarantined incomplete animation {segment.name}", flush=True)


def render_scene(video: str, module: str, cls: str, quality: str, fps: int, media: Path,
                 crf: int | None = None) -> tuple[str, float, str]:
    src = video_dir(video) / f"{module}.py"
    if crf is not None and src.parent.parent.name == "music":
        repair_segment_cache(scene_output(media, module, cls, quality, fps))
    # Each scene gets its own LaTeX and Text caches: parallel manim processes sharing one
    # Tex dir race on the .dvi files (one cleans up what another converts), and sharing one
    # texts dir race on the .svg files of identical Text strings (one unlinks what another reads).
    cfg = media / "cfg" / f"{cls}.cfg"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    # The typeset SVGs depend on neither the resolution nor the narration language, so every build of a video
    # (previews, masters, translations) shares one cache: a 4K or Chinese master reuses the preview's LaTeX.
    cache = ROOT / "media" / video
    (cache / "Tex").mkdir(parents=True, exist_ok=True)  # manim creates tex_dir without parents=True
    (cache / "texts").mkdir(exist_ok=True)
    cfg.write_text(f"[CLI]\ntex_dir = {cache / 'Tex' / cls}\ntext_dir = {cache / 'texts' / cls}\n")
    launcher = "manim" if os.environ.get("EXPLAINER_LOCAL_RENDER") == "0" else "tools.manim_local"
    cmd = [
        sys.executable, "-m", launcher, "render", f"-q{quality}", "--fps", str(fps), "-c", str(cfg),
        "--media_dir", str(media), "--progress_bar", "none", str(src), cls,
    ]
    if crf is not None:  # part of manim's segment-cache fingerprint, so masters never reuse preview segments
        cmd[-2:-2] = ["--encoder-option", f"crf={crf}", "--encoder-option", "preset=slow"]
    t = time.time()
    env = dict(os.environ, PYTHONWARNINGS="ignore")
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
    """Pad/trim audio to exactly the video length so concatenation stays in sync.

    ``lossless``: take the scene's PCM soundtrack (manim keeps ``<Scene>.wav`` next to the video) into an ALAC
    intermediate, so the only lossy audio encode is the final master's."""
    dur = ffprobe_duration(src)
    wav = src.with_suffix(".wav")
    if lossless and wav.exists():
        audio_in, vin = ["-i", str(wav), "-i", str(src)], 1
        amap = "[0:a]aresample=48000,aformat=channel_layouts=stereo,apad[a]"
    elif has_audio(src):
        audio_in, vin = ["-i", str(src)], 0
        amap = "[0:a]aresample=48000,aformat=channel_layouts=stereo,apad[a]"
    else:
        audio_in, vin = ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-i", str(src)], 1
        amap = "[0:a]apad[a]"
    acodec = ["-c:a", "alac"] if lossless else ["-c:a", "aac", "-b:a", "192k"]
    cmd = ["ffmpeg", "-y", "-v", "error", *audio_in]
    cmd += ["-filter_complex", amap, "-map", f"{vin}:v", "-map", "[a]", "-t", f"{dur:.3f}"]
    cmd += ["-c:v", "copy", *acodec, str(dst.with_suffix(".mov" if lossless else ".mp4"))]
    run(cmd)


def picture_duration(src: Path) -> Fraction:
    """Read the picture clock independently of the scene AAC stream and MP4 rounding."""
    result = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                  "stream=nb_frames,r_frame_rate", "-of", "json", str(src)])
    video, = json.loads(result.stdout)["streams"]
    return int(video["nb_frames"]) / Fraction(video["r_frame_rate"])


def normalize_master_audio(src: Path, dst: Path, duration: Fraction) -> None:
    """Pad the narration to the picture's duration using exactly counted 48 kHz samples."""
    wav = src.with_suffix(".wav")
    if wav.exists() or has_audio(src):
        audio_in = ["-i", str(wav if wav.exists() else src)]
    else:
        audio_in = ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
    run(["ffmpeg", "-y", "-v", "error", *audio_in, "-map", "0:a:0",
         "-af", f"aresample=48000,aformat=channel_layouts=stereo,apad,atrim=end_sample={round(duration * 48000)}",
         "-c:a", "alac", str(dst)])


def concat_file(path: Path, entries) -> Path:
    """Write explicit picture durations when concatenating scene MP4s that also contain AAC."""
    with path.open("w") as stream:
        for media, duration in entries:
            escaped = str(media).replace("'", "'\\''")
            stream.write(f"file '{escaped}'\n")
            if duration is not None:
                stream.write(f"duration {float(duration):.9f}\n")
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("-q", "--quality", default="h", choices=list(QUALITY))
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--crf", type=int, choices=range(52), metavar="0-51",
                    help="master quality: H.264 CRF (lower is better; 16-18 for upload masters), lossless audio "
                         "intermediates and a 384 kb/s AAC soundtrack")
    ap.add_argument("-j", "--jobs", type=int, default=max(1, (os.cpu_count() or 2) // 2))
    ap.add_argument("--only", nargs="*", help="render only these scene classes (still stitches all)")
    stages = ap.add_mutually_exclusive_group()
    stages.add_argument("--stitch-only", action="store_true")
    stages.add_argument("--scenes-only", action="store_true", help="render the scenes and defer mastering")
    ap.add_argument("--lang", default="en", help="narration language (en, or zh from narration_zh.json)")
    ap.add_argument("--no-score", action="store_true",
                    help="leave out the series' computed score (explainer/<series>/score.py), if it has one")
    args = ap.parse_args()
    os.environ["EXPLAINER_LANG"] = args.lang  # the scene renders inherit it
    os.environ["EXPLAINER_VIDEO"] = args.video  # and the video's name (explainer/zh_text.py finds its series' table)
    os.environ["EXPLAINER_SOUND_STEMS"] = "1"  # scenes with computed sound leave it to the cue sheet (music_stem)

    manifest = importlib.import_module(f"{video_package(args.video)}.manifest")
    scenes = manifest.SCENES
    media = ROOT / "media" / (args.video if args.lang == "en" else f"{args.video}_{args.lang}")
    if args.crf is not None:
        media = media / f"crf{args.crf}"

    if not args.stitch_only:
        todo = [s for s in scenes if not args.only or s[1] in args.only]
        # longest first (by any earlier render of the scene), so the last job running alone is a short one
        def est(s):
            done = [p for d in (args.video, f"{args.video}_*")
                    for p in (ROOT / "media").glob(f"{d}/**/videos/{s[0]}/*/{s[1]}.mp4")]
            durations = []
            for old in done:
                try:
                    durations.append(ffprobe_duration(old))
                except (subprocess.CalledProcessError, ValueError):
                    continue
            fallback = (video_dir(args.video) / f"{s[0]}.py").stat().st_size / 100
            return max(durations, default=fallback)
        todo.sort(key=est, reverse=True)
        print(f"Rendering {len(todo)} scene(s) at {QUALITY[args.quality]}{args.fps} with {args.jobs} job(s)...")
        failed = []
        with ThreadPoolExecutor(args.jobs) as pool:
            futs = [pool.submit(render_scene, args.video, m, c, args.quality, args.fps, media, args.crf)
                    for m, c, _ in todo]
            for f in as_completed(futs):
                cls, dt, err = f.result()
                print(f"  {'FAIL' if err else 'ok  '} {cls:<28} {dt:6.0f}s", flush=True)
                if err:
                    failed.append(cls)
                    print(err)
        if failed:
            sys.exit(f"Failed scenes: {failed}")

    if args.scenes_only:
        return

    # ---- stitch -----------------------------------------------------------
    out_dir = ROOT / "renders"
    work = media / "stitch"
    out_dir.mkdir(exist_ok=True)
    work.mkdir(parents=True, exist_ok=True)
    suffix = "" if args.quality == "h" else f"_{QUALITY[args.quality]}"
    suffix += "" if args.lang == "en" else f"_{args.lang}"
    name = f"{args.video}{suffix}"

    split_tracks = args.crf is not None and video_dir(args.video).parent.name == "music"
    pictures = []
    parts, cues, chapters, offset, sound_cues, timeline = [], [], [], 0.0, [], []
    for module, cls, chapter in scenes:
        mp4 = scene_output(media, module, cls, args.quality, args.fps)
        if not mp4.exists():
            sys.exit(f"Missing render for {cls}: {mp4}")
        meta = mp4.with_suffix(".narration.json")
        meta_json = json.loads(meta.read_text()) if meta.exists() else {}
        lines = meta_json.get("lines", [])
        check_narration_audio(mp4, lines)
        if split_tracks:
            duration = picture_duration(mp4)
            norm = work / f"{cls}.m4a"
            normalize_master_audio(mp4, norm, duration)
            pictures.append((mp4, duration))
            dur = float(duration)
        else:
            norm = work / f"{cls}.{'mov' if args.crf is not None else 'mp4'}"
            normalize(mp4, norm, lossless=args.crf is not None)
            dur = ffprobe_duration(norm)
        sheet = mp4.with_suffix(".cues.json")
        if sheet.exists():
            heard = json.loads(sheet.read_text())["cues"]
            sound_cues += [{**c, "start": c["start"] + offset} for c in heard]
            # a viewer with the sound off reads what each example is: "[sound: lower, upper, both (physical model)]"
            for c in heard:
                if c.get("window") and not c.get("underscore"):
                    what = ", ".join(x for x in (c.get("caption"), c.get("label")) if x) or "an example"
                    cues.append((offset + c["start"], offset + c["start"] + min(c["duration"], 6.0),
                                 f"[{'声音' if args.lang == 'zh' else 'sound'}: {what}]"))
        cues += subtitle_cues(lines, offset, args.lang,
                              preserve_terms=getattr(manifest, "SUBTITLE_TERM_BOUNDARIES", False) is True)
        if chapter:
            chapters.append((offset, narration_lang.chapter_title(args.video, cls, chapter, args.lang)))
        parts.append(norm)
        timeline.append({"video": args.video, "cls": cls, "chapter": chapter, "start": offset, "duration": dur,
                         "lines": [{"start": x["start"], "duration": x["duration"]} for x in lines],
                         "marks": meta_json.get("marks", [])})
        offset += dur

    score = series_score(args.video) if not args.no_score else None
    if score is not None:  # a series with a computed score: its cues join the music stem
        scored = score.cues(timeline, ROOT / ".cache")
        print(f"score: {len(scored)} cue(s) from {score.__name__}")
        sound_cues += scored

    durations = (duration for _, duration in pictures) if split_tracks else (None for _ in parts)
    concat_list = concat_file(work / "concat.txt", zip(parts, durations, strict=True))
    audio_in = ["-f", "concat", "-safe", "0", "-i", str(concat_list)]
    inputs = audio_in
    if split_tracks:
        picture_list = concat_file(work / "picture.txt", pictures)
        # Ignore AAC priming in the unused scene audio track. FFmpeg would
        # otherwise shift the picture input forward to offset a negative audio timestamp.
        inputs = ["-copyts", "-f", "concat", "-safe", "0", "-i", str(picture_list), *audio_in]
    voice_input = int(split_tracks)
    subtitles, chapters_input, music_input = range(voice_input + 1, voice_input + 4)
    srt = out_dir / f"{name}.srt"
    srt.write_text(to_srt(sorted(cues, key=lambda c: c[0])))

    ffmeta = work / "chapters.ffmeta"
    lines = [";FFMETADATA1", f"title={narration_lang.video_title(args.video, manifest.TITLE, args.lang)}"]
    bounds = [c[0] for c in chapters] + [offset]
    for (start, title), end in zip(chapters, bounds[1:]):
        lines += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={int(start * 1000)}", f"END={int(end * 1000)}", f"title={title}"]
    ffmeta.write_text("\n".join(lines) + "\n")

    final = out_dir / f"{name}.mp4"
    temporary = out_dir / f".{name}.{os.getpid()}.tmp.mp4"
    tail = ["-ar", "48000", "-c:a", "aac", "-b:a", "384k" if args.crf is not None else "192k",
            "-c:s", "mov_text", "-metadata:s:s:0", f"language={ {'en': 'eng', 'zh': 'chi'}[args.lang] }",
            "-metadata:s:a:0", f"language={ {'en': 'eng', 'zh': 'chi'}[args.lang] }", "-movflags", "+faststart",
            str(temporary)]
    # Manim scene edit lists can end a fraction of a frame early. Rescale copied
    # packet timestamps onto the frame grid, including B-frame decode timestamps.
    video_clock = ["-video_track_timescale", str(args.fps), "-movie_timescale", "1000"] if split_tracks else []
    tracks = [*video_clock, "-map", f"{subtitles}:s:0", "-map_metadata", str(chapters_input),
              "-map_chapters", str(chapters_input), "-c:v", "copy", *tail]
    if sound_cues:  # Music, Built (or a series' score): narration and music stem are mastered apart, then joined
        music = work / "music.wav"
        music_stem(sound_cues, offset, music)
        graph = sound_master(concat_list, voice_input, music_input)
        try:
            result = run(["ffmpeg", "-y", "-nostats", *inputs, "-i", str(srt), "-i", str(ffmeta), "-i", str(music),
                          "-filter_complex", graph, "-map", "0:v:0", "-map", "[a]", *tracks,
                          "-map", "[levels]", "-f", "null", "-"])
            check_mix_levels(result.stderr)
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise
    else:
        audio_filter = master_filter([
            "ffmpeg", "-v", "info", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-vn",
            "-af", f"{HIGHPASS},{LOUDNORM}:print_format=json", "-f", "null", "-",
        ])
        run([
            "ffmpeg", "-y", "-v", "error", *inputs, "-i", str(srt), "-i", str(ffmeta),
            "-map", "0:v:0", "-map", f"{voice_input}:a:0", "-af", audio_filter, *tracks,
        ])
    temporary.replace(final)
    yt = "\n".join(f"{int(s // 60)}:{int(s % 60):02d} {t}" for s, t in chapters)
    (out_dir / f"{name}.chapters.txt").write_text(yt + "\n")
    print(f"\nWrote {final.relative_to(ROOT)}  ({offset / 60:.1f} min)")
    print(yt)


if __name__ == "__main__":
    main()
