#!/usr/bin/env python
"""Narrate a video on a Colab GPU instead of the local TTS server, filling the local TTS cache (.cache/tts).

    python tools/colab_narrate.py ai1 --lang en [--session tts] [--gpu T4]

Same lines and cache keys as tools/narrate.py (so it is safe to run that afterwards: it finds every line cached and
only synthesizes stragglers locally). Resumable: lines already in the local cache are skipped, the VM keeps what it
finished, and finished lines are copied back every few minutes. Needs the ``colab`` CLI signed in
(~/.local/bin/colab sessions) and a video whose preview render exists (like narrate.py).
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
COLAB = os.environ.get("COLAB_BIN", str(Path.home() / ".local/bin/colab"))
REMOTE = "/content/repo"
FILES = ["tools/tts_server.py", "tools/colab_tts_worker.py", "tools/voices.json", "explainer/lang.py",
         "explainer/paths.py", "tools/voice_refs/kokoro_en.wav", "tools/voice_refs/serenaflat_zh.wav"]


def colab(*a, stdin: str | None = None, check=True) -> str:
    r = subprocess.run([COLAB, *a], input=stdin, capture_output=True, text=True)
    if check and r.returncode:
        sys.exit(f"colab {' '.join(a)} failed:\n{r.stdout[-1500:]}\n{r.stderr[-1500:]}")
    return r.stdout + r.stderr


def rexec(session: str, code: str, timeout=900) -> str:
    return colab("exec", "-s", session, "--timeout", str(timeout), stdin=code)


def lines_to_do(video: str, lg: str) -> list[dict]:
    os.environ.update(EXPLAINER_TTS="server", EXPLAINER_VOICE=os.environ.get("EXPLAINER_VOICE", "qwen3-calm-a"),
                      EXPLAINER_LANG=lg)
    from explainer import lang, paths, tts
    from explainer.voiceover import _strip_bookmarks
    from tools.translate_narration import english_lines

    video_dir = paths.video_dir(video)
    jobs, seen = [], set()
    for cls, raw in english_lines(video):
        clean, _ = _strip_bookmarks(lang.translate(raw, video_dir, cls))
        text, spoken, key = tts.cache_key(clean)
        if key in seen or ((tts.CACHE_DIR / f"{key}.wav").exists() and (tts.CACHE_DIR / f"{key}.json").exists()):
            continue
        seen.add(key)
        jobs.append({"key": key, "text": text, "spoken": spoken})
    return jobs, tts.CACHE_DIR


def ensure_session(session: str, gpu: str):
    if f"[{session}]" not in colab("sessions", check=False):
        print(f"creating Colab session {session!r} ({gpu})", flush=True)
        colab("new", "-s", session, "--gpu", gpu)
    ready = rexec(session, f"import os;print('READY' if os.path.exists('{REMOTE}/.ready') else 'NO')")
    if "READY" in ready:
        return
    print("setting up the VM (packages, models' code, voice references)", flush=True)
    # qwen-tts and qwen-asr pin different transformers versions: one after the other (the later one wins, and both run)
    rexec(session, "import subprocess\nfor c in ('uv pip install --system qwen-tts soundfile pypinyin', 'uv pip install --system qwen-asr'):\n"
                   "    subprocess.run(c, shell=True, check=True)\n", timeout=1500)
    rexec(session, f"import os;[os.makedirs('{REMOTE}/'+d,exist_ok=True) for d in ('tools/voice_refs','explainer')]")
    for f in FILES:
        colab("upload", "-s", session, str(ROOT / f), f"{REMOTE}/{f}")
    rexec(session, f"open('{REMOTE}/.ready','w').write('1')")


def pull(session: str, remote_out: str, cache: Path) -> int:
    """Copy finished lines (not yet in the local cache) from the VM into the local TTS cache."""
    have = sorted(p.stem for p in cache.glob("*.json"))
    code = f"""
import os, tarfile, json
have = set({json.dumps(have)})
done = sorted(f[:-5] for f in os.listdir('{remote_out}') if f.endswith('.json') and f[:-5] not in have and f != 'qa.json')
with tarfile.open('/content/pull.tar', 'w') as tf:
    for k in done:
        tf.add('{remote_out}/'+k+'.wav', arcname=k+'.wav')
        tf.add('{remote_out}/'+k+'.json', arcname=k+'.json')
print('PULL', len(done))
"""
    out = rexec(session, code)
    n = int(out.split("PULL")[-1].split()[0])
    if n:
        with tempfile.TemporaryDirectory() as td:
            colab("download", "-s", session, "/content/pull.tar", f"{td}/pull.tar")
            with tarfile.open(f"{td}/pull.tar") as tf:
                tf.extractall(td + "/x")
            cache.mkdir(parents=True, exist_ok=True)
            for p in sorted(Path(td, "x").iterdir(), key=lambda p: p.suffix != ".wav"):  # .json last, like synthesize()
                shutil.move(str(p), cache / p.name)
    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--session", default="tts")
    ap.add_argument("--gpu", default="T4")
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--poll", type=int, default=240, help="seconds between checks (finished lines are pulled each time)")
    args = ap.parse_args()

    jobs, cache = lines_to_do(args.video, args.lang)
    print(f"{args.video} ({args.lang}): {len(jobs)} lines not yet in the cache", flush=True)
    if not jobs:
        return
    ensure_session(args.session, args.gpu)
    tag = f"{args.video}_{args.lang}"
    remote_out, remote_jobs, remote_log = f"/content/tts_out/{tag}", f"/content/jobs_{tag}.json", f"/content/log_{tag}.txt"
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(jobs, f, ensure_ascii=False)
    colab("upload", "-s", args.session, f.name, remote_jobs)
    os.unlink(f.name)
    launch = f"""
import subprocess, os
alive = subprocess.run("pgrep -f '[c]olab_tts_worker.py {remote_jobs}'", shell=True, capture_output=True).stdout.strip()
if alive:
    print('ALREADY RUNNING')
else:
    subprocess.Popen("cd {REMOTE}/tools && nohup python -u colab_tts_worker.py {remote_jobs} --lang {args.lang} "
                     "--out {remote_out} --batch {args.batch} >> {remote_log} 2>&1", shell=True, start_new_session=True)
    print('LAUNCHED')
"""
    print(rexec(args.session, launch).strip().splitlines()[-1], flush=True)
    while True:
        time.sleep(args.poll)
        tail = rexec(args.session, f"import subprocess;print(subprocess.run('tail -n 3 {remote_log}',shell=True,"
                                   f"capture_output=True,text=True).stdout)")
        n = pull(args.session, remote_out, cache)
        last = [l for l in tail.strip().splitlines() if l.strip()][-1:] or ["(no output yet)"]
        print(f"{time.strftime('%H:%M')} pulled {n} lines; VM: {last[0][:110]}", flush=True)
        if "DONE" in tail:
            pull(args.session, remote_out, cache)
            return
        if "Traceback" in tail or "Error" in tail.split("DONE")[0] and "take" not in tail:
            sys.exit(f"worker failed, see {remote_log} on the VM:\n{tail}")


if __name__ == "__main__":
    main()
