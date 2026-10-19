#!/usr/bin/env python3
"""Runs on a Colab VM, detached (started by tools/colab_push.py): narrates and renders the parts the Mac pushes.

    python3 /content/repo/tools/colab_factory.py [--jobs 12]

Queue directory /content/q holds one trio per (video, lang), written by colab_push.py:
    jobs_<video>_<lang>.json   narration lines [{key, text, spoken}]
    ready_<video>_<lang>       the part's caches are uploaded: narrate it
and this script adds narr_done_*, render_done_* (or render_fail_*). Narration (GPU) and rendering (CPU) run side by side,
parts in numeric order. A 2160p60 CRF 16 master lands in /content/out (and, when Drive is mounted, in
/content/drive/MyDrive/explainer-videos). Restartable: finished markers are skipped, and narration and the render
cache (media/) keep what was done.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

Q = Path("/content/q")
REPO = Path("/content/repo")
OUT = Path("/content/out")
DRIVE = Path("/content/drive/MyDrive/explainer-videos")


def part_key(name: str):
    m = re.match(r"ready_([a-z]+)(\d+)_(\w+)$", name)
    return (int(m.group(2)), m.group(3)) if m else (999, "")


def pending(prefix_in: str, prefix_out: str, skip_failed=True):
    names = sorted((p.name[len(prefix_in):] for p in Q.glob(prefix_in + "*")), key=lambda n: part_key("ready_" + n))
    return [n for n in names if not (Q / (prefix_out + n)).exists()
            and not (skip_failed and (Q / ("render_fail_" + n)).exists())]


def log(msg: str):
    with open(Q / "factory.log", "a") as f:
        f.write(time.strftime("%H:%M ") + msg + "\n")


def narrate_loop():
    while True:
        todo = pending("ready_", "narr_done_")
        if not todo:
            time.sleep(15)
            continue
        tag = todo[0]  # <video>_<lang>
        video, lang = tag.rsplit("_", 1)
        log(f"narrate {tag}")
        r = subprocess.run(
            f"cd {REPO}/tools && python3 -u colab_tts_worker.py {Q}/jobs_{tag}.json --lang {lang} "
            f"--out {REPO}/.cache/tts --batch 24 >> {Q}/narr_{tag}.log 2>&1", shell=True)
        if r.returncode == 0:
            (Q / f"narr_done_{tag}").touch()
            log(f"narrated {tag}")
        else:
            log(f"narration FAILED {tag}; retrying in 60 s")
            time.sleep(60)


def render_loop(jobs: int):
    OUT.mkdir(exist_ok=True)
    while True:
        todo = [t for t in pending("narr_done_", "render_done_") if not (Q / f"render_fail_{t}").exists()]
        if not todo:
            time.sleep(15)
            continue
        tag = todo[0]
        video, lang = tag.rsplit("_", 1)
        log(f"render {tag}")
        t0 = time.time()
        cmd = (f"cd {REPO} && EXPLAINER_TTS=server EXPLAINER_VOICE=qwen3-calm-a EXPLAINER_TTS_SERVER=http://127.0.0.1:9 "
               f"python3 -u tools/build.py {video} -q k --fps 60 --crf 16 -j {jobs}"
               f"{' --lang zh' if lang == 'zh' else ''} >> {Q}/render_{tag}.log 2>&1")
        r = subprocess.run(cmd, shell=True)
        if r.returncode:
            # one retry reuses the cached scene segments
            r = subprocess.run(cmd, shell=True)
        if r.returncode:
            (Q / f"render_fail_{tag}").touch()
            log(f"render FAILED {tag} (see {Q}/render_{tag}.log)")
            continue
        suffix = "_zh" if lang == "zh" else ""
        files = [p for p in (REPO / "renders").glob(f"{video}_2160p{suffix}.*")]
        dests = [OUT] + ([DRIVE] if DRIVE.parent.exists() else [])
        for d in dests:
            d.mkdir(parents=True, exist_ok=True)
            for p in files:
                shutil.copy2(p, d / p.name)
        (Q / f"render_done_{tag}").touch()
        log(f"rendered {tag} in {(time.time() - t0) / 60:.0f} min -> {', '.join(str(d) for d in dests)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=12)
    args = ap.parse_args()
    Q.mkdir(exist_ok=True)
    threading.Thread(target=narrate_loop, daemon=True).start()
    render_loop(args.jobs)


if __name__ == "__main__":
    sys.exit(main())
