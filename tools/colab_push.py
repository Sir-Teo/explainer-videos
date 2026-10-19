#!/usr/bin/env python
"""Hand one part to a Colab VM's factory (tools/colab_factory.py), which narrates it and renders its 2160p60 master there.

    python tools/colab_push.py ai3 --lang en --session a100

Uploads the repo's code and the compute caches (.cache/ai*, small), the part's narration lines (with the cache keys
this Mac would use), and starts the factory on the VM if it is not running. Needs the part's compute and a preview
render (like tools/narrate.py). Idempotent: pushing a part again just refreshes its files.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
import colab_narrate as cn  # noqa: E402

REMOTE = cn.REMOTE


def all_jobs(video: str, lg: str) -> list[dict]:
    os.environ.update(EXPLAINER_TTS="server", EXPLAINER_VOICE="qwen3-calm-a", EXPLAINER_LANG=lg)
    from explainer import lang, paths, tts
    from explainer.voiceover import _strip_bookmarks
    from tools.translate_narration import english_lines

    vd = paths.video_dir(video)
    jobs, seen = [], set()
    for cls, raw in english_lines(video):
        clean, _ = _strip_bookmarks(lang.translate(raw, vd, cls))
        text, spoken, key = tts.cache_key(clean)
        if key not in seen:
            seen.add(key)
            jobs.append({"key": key, "text": text, "spoken": spoken})
    return jobs


def pick_box() -> str:
    """The Colab session with the fewest unfinished parts whose toolchain is installed (``--session auto``)."""
    names = [l.split("]")[0].lstrip("[") for l in cn.colab("sessions", check=False).splitlines()
             if l.startswith("[") and not l.startswith("[?]")]
    best = None
    for n in names:
        out = cn.colab("exec", "-s", n, "--timeout", "60", stdin=(
            "import os,glob\n"
            "q='/content/q/'\n"
            "r=len(glob.glob(q+'ready_*'));d=len(glob.glob(q+'render_done_*'))+len(glob.glob(q+'render_fail_*'))\n"
            "print('LOAD', os.path.exists('/content/.toolchain_ok'), r-d)\n"), check=False)
        if "LOAD True" in out:
            load = int(out.split("LOAD True")[1].split()[0])
            if best is None or load < best[0]:
                best = (load, n)
    if not best:
        sys.exit("no Colab session with the toolchain installed")
    return best[1]


def tar(path: Path, args: list[str]):
    subprocess.run(["tar", "czf", str(path), *args], cwd=ROOT, check=True,
                   stderr=subprocess.DEVNULL, env={**os.environ, "COPYFILE_DISABLE": "1"})


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--lang", required=True)
    ap.add_argument("--session", required=True)
    ap.add_argument("--jobs", type=int, default=12, help="scenes rendered at once on the VM")
    args = ap.parse_args()
    s = pick_box() if args.session == "auto" else args.session
    print(f"-> Colab session {s}", flush=True)
    jobs = all_jobs(args.video, args.lang)
    print(f"{args.video} ({args.lang}): {len(jobs)} narration lines", flush=True)
    cn.rexec(s, f"import os;os.makedirs('{REMOTE}',exist_ok=True);os.makedirs('/content/q',exist_ok=True)")
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        files = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], cwd=ROOT, capture_output=True,
                               text=True, check=True).stdout.split("\n")
        (td / "files.txt").write_text("\n".join(f for f in files if f and not f.startswith(("media/", "renders/", "published/"))))
        tar(td / "code.tgz", ["-T", str(td / "files.txt")])
        caches = sorted(p.name for p in (ROOT / ".cache").glob("ai[0-9]*"))
        tar(td / "cache.tgz", ["--exclude=colab_gpu", "--exclude=books", "--exclude=train.txt", "--exclude=valid.txt",
                               *[f".cache/{c}" for c in caches]])
        (td / "jobs.json").write_text(json.dumps(jobs, ensure_ascii=False))
        for name in ("code.tgz", "cache.tgz"):
            cn.colab("upload", "-s", s, str(td / name), f"/content/{name}")
        cn.colab("upload", "-s", s, str(td / "jobs.json"), f"/content/q/jobs_{args.video}_{args.lang}.json")
    out = cn.rexec(s, f"""
import os, subprocess
subprocess.run("cd {REMOTE} && tar xzf /content/code.tgz 2>/dev/null; tar xzf /content/cache.tgz 2>/dev/null", shell=True)
open('/content/q/ready_{args.video}_{args.lang}', 'w').close()
def alive():
    try:
        os.kill(int(open('/content/q/factory.pid').read()), 0)
        return True
    except Exception:
        return False
if not alive():
    p = subprocess.Popen(['python3', '-u', 'tools/colab_factory.py', '--jobs', '{args.jobs}'], cwd='{REMOTE}',
                         stdout=open('/content/q/factory.out', 'a'), stderr=subprocess.STDOUT, start_new_session=True)
    open('/content/q/factory.pid', 'w').write(str(p.pid))
print('PUSHED')
""")
    print(out.strip().splitlines()[-1], flush=True)


if __name__ == "__main__":
    main()
