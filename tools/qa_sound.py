#!/usr/bin/env python
"""The sound gates of *Music, Built* (videos/music/SYLLABUS.md, section 3).

    python tools/qa_sound.py music1                  # every rendered chapter of Part 1
    python tools/qa_sound.py music1 --only Hook Monochord
    python tools/qa_sound.py soundcheck --sync       # also measure picture-to-sound sync on the click test
    python tools/qa_sound.py music1 --lang zh

It reads what each rendered scene left beside its video: ``<Scene>.cues.json`` (the clips it played, when, and how
loud) and ``<Scene>.narration.json`` (what was said, and when).  Gates, each a failure when broken:

* **overlap**: no narration over a listening window, and none over any clip that is not marked ``underscore``;
* **picture**: every listening window moved at least one picture from the clip's own clock;
* **label**: every clip says what it is (``physical model``, ``synthesized``, ``illustrative``, ...);
* **peaks**: the scene's music stem, mixed as the build mixes it, stays under the true-peak ceiling;
* **levels**: no clip's loudest 400 ms is above the maximum, and none is silent;
* **phone**: every clip is auditioned through a small speaker (mono, 300 Hz to 8 kHz).  One that loses more than
  20 dB there must say what it needs (``needs`` in the clip's label: ``bass``, ``headphones``); one that loses its
  stereo image must say ``headphones``.  The table's last column is the verdict the syllabus asks for: ``survives``,
  ``picture carries it`` or ``labelled``.

``--sync`` finds the scene that plays a ``clicks`` clip, decodes the stitched film (``renders/``, where the music
stem has been mixed in) and measures the time between each click and the frame that lights for it.  It must be
under one frame.
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
sys.path.insert(0, str(ROOT))

from explainer.paths import video_package  # noqa: E402

CEILING_DBTP = -1.5      # each scene's music stem
MAX_LEVEL = -9.0         # LUFS, loudest 400 ms of a clip after its gain
MIN_LEVEL = -45.0
PHONE_LOSS_LABEL = 20.0  # dB: beyond this the clip must be labelled
PHONE_LOSS_NOTE = 6.0    # dB: beyond this the picture has to carry the point


def scene_files(video: str, lang: str, module: str, cls: str) -> Path | None:
    """The newest render of a scene (any quality): the path of its .mp4."""
    media = ROOT / "media" / (video if lang == "en" else f"{video}_{lang}")
    found = sorted(media.glob(f"**/videos/{module}/*/{cls}.mp4"), key=lambda p: p.stat().st_mtime)
    return found[-1] if found else None


def phone(clip):
    """The clip as a small speaker plays it: mono, band-limited to 300 Hz - 8 kHz."""
    from scipy.signal import butter, sosfilt

    from explainer.music.monochord.audio import Clip

    sos = butter(4, [300.0, 8000.0], btype="bandpass", fs=clip.sr, output="sos")
    return Clip(sosfilt(sos, clip.mono.astype(np.float64)), clip.sr)


def check_scene(mp4: Path, report: list) -> int:
    from explainer.music.monochord.audio import Clip, mix
    from explainer.music.monochord.loudness import momentary_max, true_peak_db

    sheet = mp4.with_suffix(".cues.json")
    if not sheet.exists():
        return 0
    cues = json.loads(sheet.read_text())["cues"]
    meta = mp4.with_suffix(".narration.json")
    lines = json.loads(meta.read_text())["lines"] if meta.exists() else []
    scene = mp4.stem
    fails = 0

    def fail(msg):
        nonlocal fails
        fails += 1
        report.append(f"  FAIL {scene}: {msg}")

    placed = []
    for c in cues:
        name = c["clip"] or Path(c["path"]).stem
        path = Path(c["path"])
        if not path.exists():
            fail(f"{name}: the clip file is gone ({path})")
            continue
        clip = Clip.read(path)
        side = json.loads(path.with_suffix(".json").read_text())
        label = side.get("meta", {})
        placed.append((Clip(clip.stereo, clip.sr), c["start"], c["gain_db"]))
        a, b = c["start"], c["start"] + c["duration"]
        if not c["underscore"]:
            for ln in lines:
                over = min(b, ln["start"] + ln["duration"]) - max(a, ln["start"])
                if over > 0.08:
                    fail(f"{name} at {a:.1f} s overlaps narration by {over:.1f} s: “{ln['text'][:50]}...”")
                    break
        if c["window"] and not c.get("driven"):
            fail(f"{name} at {a:.1f} s: a listening window with no picture on the clip's clock")
        if not c["label"]:
            fail(f"{name}: no label (physical model, synthesized, illustrative, ...)")
        level = momentary_max(clip) + c["gain_db"]
        if level > MAX_LEVEL:
            fail(f"{name}: loudest 400 ms at {level:.1f} LUFS, above {MAX_LEVEL}")
        if not np.isfinite(level) or level < MIN_LEVEL:
            fail(f"{name}: silent ({level:.1f} LUFS)")
        small = phone(clip)
        loss = momentary_max(clip) - momentary_max(small) if np.isfinite(momentary_max(small)) else 99.0
        needs = label.get("needs", "")
        wide = False
        if clip.channels == 2:
            mid, side_ = clip.y.mean(axis=1), (clip.y[:, 0] - clip.y[:, 1]) / 2
            wide = float(np.mean(side_ ** 2)) > 0.1 * float(np.mean(mid ** 2) + 1e-20)
        if loss > PHONE_LOSS_LABEL and not needs:
            fail(f"{name}: loses {loss:.0f} dB on a small speaker and does not say what it needs")
        if wide and "headphones" not in needs and "stereo" not in needs:
            fail(f"{name}: depends on its stereo image and does not say it needs headphones")
        verdict = "labelled: " + needs if needs else ("picture carries it" if loss > PHONE_LOSS_NOTE else "survives")
        report.append(f"  {scene:<14s} {name:<26s} {a:7.1f}s {c['duration']:5.1f}s  {level:6.1f} LUFS  "
                      f"{true_peak_db(clip) + c['gain_db']:6.1f} dBTP  phone {-loss:+5.1f} dB  {verdict}")
    if placed:
        stem = mix(placed)
        peak = true_peak_db(stem)
        if peak > CEILING_DBTP:
            fail(f"the scene's music peaks at {peak:.1f} dBTP, above {CEILING_DBTP}")
    return fails


def decode_audio(mp4: Path, sr: int = 48_000) -> np.ndarray:
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", str(mp4), "-vn", "-ac", "1", "-ar", str(sr), "-f", "f32le",
                          "-"], capture_output=True, check=True).stdout
    return np.frombuffer(out, dtype="<f4")


def white_fraction(mp4: Path, w: int = 160, h: int = 90) -> tuple[np.ndarray, float]:
    """Per frame, the fraction of pixels that are nearly white; and the frame rate."""
    rate = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate",
                           "-of", "csv=p=0", str(mp4)], capture_output=True, text=True, check=True).stdout.strip()
    num, den = rate.split("/")
    fps = float(num) / float(den)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(mp4), "-an", "-vf", f"scale={w}:{h}:flags=area",
                          "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout
    frames = np.frombuffer(raw, dtype=np.uint8).reshape(-1, h, w)
    return (frames > 235).mean(axis=(1, 2)), fps


def film_of(video: str, lang: str) -> Path | None:
    """The newest stitched film of a video (any quality)."""
    suffix = "" if lang == "en" else f"_{lang}"
    found = [p for p in (ROOT / "renders").glob(f"{video}*.mp4")
             if p.stem.endswith(suffix) and (lang != "en" or not p.stem.endswith("_zh"))]
    return max(found, key=lambda p: p.stat().st_mtime) if found else None


def chapter_starts(film: Path) -> list[float]:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_chapters", "-of", "json", str(film)], capture_output=True,
                         text=True).stdout
    return [float(c["start_time"]) for c in json.loads(out or "{}").get("chapters", [])]


def check_sync(film: Path, offset: float, sheet: Path, report: list) -> int:
    """Each click against the frame that lights for it, measured on the stitched film (where the music stem has
    been mixed in).  The scene must light a white shape on the frame at each click (the sound check does)."""
    cues = json.loads(sheet.read_text())["cues"]
    c = [c for c in cues if c["clip"].startswith("clicks")][0]
    events = json.loads(Path(c["path"]).with_suffix(".json").read_text())["events"]
    y = decode_audio(film)
    white, fps = white_fraction(film)
    base = np.median(white)
    fails = 0
    for name, t in sorted(events.items(), key=lambda kv: kv[1]):
        want = offset + c["start"] + t
        a, b = int((want - 0.2) * 48_000), int((want + 0.2) * 48_000)
        seg = np.abs(y[a:b])
        heard = (a + int(np.argmax(seg > 0.5 * seg.max()))) / 48_000
        fa, fb = int((want - 0.3) * fps), int((want + 0.3) * fps) + 1
        lit = np.flatnonzero(white[fa:fb] > base + 0.003)
        if not lit.size:
            report.append(f"  FAIL sync {name}: no frame lights near {want:.2f} s")
            fails += 1
            continue
        seen = (fa + int(lit[0])) / fps          # the frame is on screen from here for one frame
        off = heard - seen                        # 0 .. 1/fps when the click falls inside its frame; a scene's
        ok = abs(off) <= 1.0 / fps                # events land on frame boundaries, so allow one frame either way
        fails += not ok
        report.append(f"  sync {name}: sound at {heard:8.3f} s, frame from {seen:8.3f} s, offset {off * 1000:+6.1f} ms "
                      f"({'ok' if ok else 'FAIL'}; one frame is {1000 / fps:.0f} ms)")
    return fails


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--only", nargs="*", help="scene classes to check")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--sync", action="store_true")
    args = ap.parse_args()
    manifest = importlib.import_module(f"{video_package(args.video)}.manifest")
    report, fails, seen = [], 0, 0
    film = film_of(args.video, args.lang) if args.sync else None
    starts = chapter_starts(film) if film else []
    chaptered = 0
    for module, cls, chapter in manifest.SCENES:
        offset = starts[chaptered] if chapter and chaptered < len(starts) else None
        chaptered += bool(chapter)
        if args.only and cls not in args.only:
            continue
        mp4 = scene_files(args.video, args.lang, module, cls)
        if mp4 is None:
            report.append(f"  (not rendered: {cls})")
            continue
        seen += 1
        fails += check_scene(mp4, report)
        sheet = mp4.with_suffix(".cues.json")
        if args.sync and sheet.exists() and any(c["clip"].startswith("clicks")
                                                 for c in json.loads(sheet.read_text())["cues"]):
            if film is None or offset is None:
                report.append(f"  FAIL sync: no stitched film of {args.video} in renders/ (run tools/build.py first)")
                fails += 1
            else:
                fails += check_sync(film, offset, sheet, report)
    print("\n".join(report))
    print(f"{args.video}: {seen} scene(s) checked, {fails} failure(s)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
