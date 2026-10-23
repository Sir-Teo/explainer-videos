#!/usr/bin/env python
"""Rebuild videos from the repo, end to end: the computations, then the narrated final cut in each language.

    python tools/make.py ai26                                # English and Chinese, 1080p30, narrated
    python tools/make.py ai26 ai27 -q k --fps 60 --crf 16    # 4K60 upload masters
    python tools/make.py --series ai                         # every part of a series, in order
    python tools/make.py ai26 --lang en --silent -q l        # a quick silent preview
    python tools/make.py ai26 --steps compute                # only the numbers

Every step picks up where it stopped, so after an interruption (a closed laptop, a crash) rerun the same command:

  compute  first the videos this one draws on (found from its imports: Part 30 reuses Part 13's transformer, Part 27
           the novels model), then its own compute module.  Each item is cached in .cache/<video>/ the moment it is
           done (and only then), and the long jobs checkpoint as they go: AlphaZero after every generation, the
           language models every 100 steps.  Everything is seeded: the same machine gives the same numbers; another
           machine's floating point can move the last digits, and the narration, written over the data, follows.
  build    tools/build.py in each language.  Narration and animations are cached by content, so a rerun redoes only
           what's missing.  Before a Chinese build every narrated line is checked to translate
           (tools/zh_lines.py --verify), so a long build can't fail halfway.
  check    the on-screen text of the Chinese edition (tools/collect_text.py), reported, not fatal.

Narration comes from the TTS server (README: "Narration"); --silent builds without it.  Logs: renders/make/.
"""

from __future__ import annotations

import argparse
import os
import re
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from explainer.paths import video_dir, video_package  # noqa: E402

VIDEOS = ROOT / "videos"
LOGS = ROOT / "renders" / "make"
BILINGUAL = {"ai", "analysis"}  # series with a Chinese edition (and Qwen3-TTS narration)


def all_videos(series: str) -> list[str]:
    names = [p.parent.name for p in (VIDEOS / series).glob("*/manifest.py")]
    return sorted(names, key=lambda n: [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", n)])


def series_of(video: str) -> str:
    return video_dir(video).parent.name


_ALIAS = re.compile(r"from videos\.\w+\.(\w+) import compute as (\w+)")
_LOAD_ALIAS = re.compile(r"from videos\.\w+\.(\w+)\.compute import (?:[^\n]*\b)?load as (\w+)")
_COMMON_LOAD = re.compile(r"from videos\.\w+\.(\w+)\.common import [^\n]*\bload\b")


def depends_on(video: str) -> dict[str, set | None]:
    """The videos whose computed results this one reads, each with the items it reads, and "novels" if it uses the
    series' base model.  Results are read as ``cN.load("item")`` (``from videos.ai.aiN import compute as cN``) or
    through ``load as ...`` from another video's compute; a ``load`` imported from another video's common, or its
    Cache opened directly, means all of its items (None).  Borrowed code (Part 2 uses Part 26's Connect Four rules,
    Part 10 Part 1's text helpers) is no dependency: every cache and helper computes what it lacks on first use, so
    Part 10, which shows Part 7's Kneser-Ney row, needn't compute the rest of Part 7."""
    me = video_dir(video)
    found: dict[str, set | None] = {}

    def add(name, items):
        if name == video or not list(VIDEOS.glob(f"*/{name}/manifest.py")):
            return
        if name in found and found[name] is None:
            return
        found[name] = None if items is None else (found.get(name) or set()) | items

    for f in me.rglob("*.py"):
        src = f.read_text()
        for name, alias in _ALIAS.findall(src):
            add(name, set(re.findall(rf"\b{alias}\.load\(\s*\"(\w+)\"", src)))
        for name, alias in _LOAD_ALIAS.findall(src):
            add(name, set(re.findall(rf"\b{alias}\(\s*\"(\w+)\"", src)))
        for name in _COMMON_LOAD.findall(src):
            add(name, None)
        for name in re.findall(r"Cache\(\"(\w+)\"\)", src):
            add(name, None)
        if re.search(r"explainer\.ai\.novels|from explainer\.ai import novels|explainer\.ai import .*\bnovels\b", src):
            found["novels"] = None
    return {k: v for k, v in sorted(found.items()) if v is None or v}


def compute_modules(video: str) -> list[str]:
    """The video's precompute entry points, in the order its README gives them."""
    d = video_dir(video)
    return [f"{video_package(video)}.{m}" for m in ("simulate", "analyze", "compute") if (d / f"{m}.py").exists()]


def run(cmd: list[str], log: Path, env: dict | None = None) -> None:
    log.parent.mkdir(parents=True, exist_ok=True)
    print(f"  $ {' '.join(cmd)}   (log: {log.relative_to(ROOT)})", flush=True)
    t = time.time()
    with open(log, "a") as f:
        f.write(f"\n=== {time.strftime('%Y-%m-%d %H:%M:%S')}  {' '.join(cmd)}\n")
        f.flush()
        # unbuffered, so progress shows as it happens rather than when a pipe's buffer fills
        p = subprocess.Popen(cmd, cwd=ROOT, env={**(env or os.environ), "PYTHONUNBUFFERED": "1"},
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in p.stdout:
            f.write(line)
            if re.match(r"\s*(compute|done|cached|step|gen |resuming|  AlphaZero|Render|ok  |FAIL|Wrote|stitch|\[)", line):
                print("    " + line.rstrip()[:150], flush=True)
        rc = p.wait()
    if rc:
        tail = log.read_text().splitlines()[-25:]
        sys.exit(f"failed ({rc}) after {time.time() - t:.0f}s: {' '.join(cmd)}\n" + "\n".join(tail) +
                 "\nFix the cause and rerun the same command: finished work is kept.")
    print(f"    ok in {time.time() - t:.0f}s", flush=True)


def compute(video: str, done: set, items: set | None = None) -> None:
    """Compute a video's results (all of them, or just ``items`` when another video needs only those), the videos it
    draws on first."""
    if video in done:
        return
    if items is None:
        done.add(video)
        for dep, its in depends_on(video).items():
            if dep == "novels":
                if "novels" not in done:
                    done.add("novels")
                    print("== the series' novels model (Parts 14, 27, 31 build on it)")
                    run([sys.executable, "-m", "explainer.ai.novels"], LOGS / "novels.log")
            else:
                compute(dep, done, its)
        mods = compute_modules(video)
        if mods:
            print(f"== {video}: computations")
        for m in mods:
            run([sys.executable, "-m", m], LOGS / f"{video}.compute.log")
    else:
        # only what was asked for; each item computes whatever it loads on first use
        key = f"{video}:" + ",".join(sorted(items))
        if key in done:
            return
        done.add(key)
        mod = f"{video_package(video)}.compute"
        print(f"== {video}: {', '.join(sorted(items))} (for another part)")
        run([sys.executable, "-m", mod, *sorted(items)], LOGS / f"{video}.compute.log")


def tts_ready() -> str | None:
    """None if the narration server answers, else what to do about it."""
    url = urlparse(os.environ.get("EXPLAINER_TTS_SERVER", "http://127.0.0.1:8765"))
    try:
        socket.create_connection((url.hostname, url.port or 80), timeout=3).close()
        return None
    except OSError:
        return (f"the narration server isn't answering at {url.geturl()}: start it in another terminal "
                "(README, \"Narration\"), e.g.\n  .venv-tts/bin/python tools/tts_server.py --voice qwen3-calm-a\n"
                "or build without narration: --silent")


def build(video: str, lang: str, args) -> None:
    env = os.environ.copy()
    if args.silent:
        env["EXPLAINER_TTS"] = "silent"
    elif series_of(video) in BILINGUAL:
        env.setdefault("EXPLAINER_TTS", "server")
        env.setdefault("EXPLAINER_VOICE", "qwen3-calm-a")
    if lang != "en":
        # the lines come from the English render: it runs first
        run([sys.executable, "tools/zh_lines.py", video, "--verify", "--lang", lang], LOGS / f"{video}.{lang}.log",
            env)
    cmd = [sys.executable, "tools/build.py", video, "-q", args.quality, "--fps", str(args.fps), "--lang", lang]
    if args.crf is not None:
        cmd += ["--crf", str(args.crf)]
    if args.jobs:
        cmd += ["-j", str(args.jobs)]
    print(f"== {video}: build ({lang}, -q {args.quality}, {args.fps} fps)")
    run(cmd, LOGS / f"{video}.{lang}.log", env)


def check_text(video: str) -> None:
    print(f"== {video}: on-screen text of the Chinese edition")
    for cmd in ([sys.executable, "tools/collect_text.py", video], [sys.executable, "tools/collect_text.py", "--check",
                                                                     video]):
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        (LOGS / f"{video}.text.log").write_text(r.stdout + r.stderr)
    last = (LOGS / f"{video}.text.log").read_text().strip().splitlines()[-1:] or ["?"]
    print("    " + last[0])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("videos", nargs="*")
    ap.add_argument("--series", help="every video of this series (ai, analysis, physics, ...), in order")
    ap.add_argument("--steps", nargs="+", default=["compute", "build", "check"], choices=["compute", "build", "check"])
    ap.add_argument("--lang", nargs="+", help="default: en, and zh for the bilingual series")
    ap.add_argument("-q", "--quality", default="h", choices=list("lmhpk"), help="l 480p, m 720p, h 1080p, k 2160p")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--crf", type=int, help="H.264 quality of the master (16-18 for uploads)")
    ap.add_argument("-j", "--jobs", type=int, help="scenes rendered in parallel (default: half the cores)")
    ap.add_argument("--silent", action="store_true", help="no narration (timed by an estimate): a preview")
    args = ap.parse_args()
    videos = list(args.videos) + (all_videos(args.series) if args.series else [])
    if not videos:
        ap.error("name a video, or --series")
    if "build" in args.steps and not args.silent and any(series_of(v) in BILINGUAL for v in videos):
        problem = tts_ready()
        if problem:
            sys.exit(problem)
    done: set = set()
    t0 = time.time()
    for v in videos:
        langs = args.lang or (["en", "zh"] if series_of(v) in BILINGUAL else ["en"])
        if "compute" in args.steps:
            compute(v, done)
        if "build" in args.steps:
            for lang in (["en"] + [x for x in langs if x != "en"]) if "en" in langs else langs:
                build(v, lang, args)
        if "check" in args.steps and "zh" in langs:
            check_text(v)
        print(f"== {v}: finished ({(time.time() - t0) / 60:.0f} min so far); renders/ has the results")


if __name__ == "__main__":
    main()
