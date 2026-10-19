#!/usr/bin/env python
"""Keep Colab render boxes busy with a series' missing masters and bring each finished one home.

    python tools/colab_fleet.py ai1 ai3 ... ai30 --boxes l4a l4b

Every (video, lang) whose 2160p master is not yet in renders/ (nor listed in renders/qa/fleet_skip.txt, e.g. masters
already in Drive) is a job. Each box gets up to --depth jobs at a time through tools/colab_push.py; its factory
(tools/colab_factory.py) narrates and renders them, and this loop downloads each finished master (.mp4, .srt,
.chapters.txt) into renders/. A box that comes back as a fresh VM (Colab recycles idle-looking sessions) is set up
again and its jobs handed out anew. Restartable: everything it needs is in renders/ and on the boxes.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import colab_narrate as cn  # noqa: E402

RENDERS = ROOT / "renders"
LOG = RENDERS / "qa" / "fleet.log"
SKIP = RENDERS / "qa" / "fleet_skip.txt"
STATE = RENDERS / "qa" / "state"


def log(msg: str):
    line = time.strftime("%m-%d %H:%M ") + msg
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def master(video: str, lang: str) -> Path:
    return RENDERS / f"{video}_2160p{'_zh' if lang == 'zh' else ''}.mp4"


def box_state(box: str) -> dict | None:
    code = """
import os, glob, json
Q = '/content/q/'
names = lambda p: sorted(os.path.basename(x)[len(p):] for x in glob.glob(Q + p + '*'))
print('STATE' + json.dumps({'toolchain': os.path.exists('/content/.toolchain_ok'),
    'setup_running': os.path.exists('/content/setup.log') and not os.path.exists('/content/.toolchain_ok'),
    'ready': names('ready_'), 'done': names('render_done_'), 'fail': names('render_fail_')}))
"""
    r = subprocess.run([cn.COLAB, "exec", "-s", box, "--timeout", "90"], input=code, capture_output=True, text=True,
                       timeout=240)
    m = re.search(r"STATE(\{.*\})", r.stdout)
    return json.loads(m.group(1)) if m else None


def setup(box: str):
    cn.colab("upload", "-s", box, str(ROOT / "tools" / "colab_setup.sh"), "/content/colab_setup.sh")
    cn.rexec(box, "import subprocess\nsubprocess.Popen('nohup bash /content/colab_setup.sh > /content/setup.log 2>&1',"
                  " shell=True, start_new_session=True)\n", timeout=60)
    log(f"{box}: setting up the toolchain")


def fetch(box: str, video: str, lang: str) -> bool:
    stem = master(video, lang).stem
    for ext in ("srt", "chapters.txt", "mp4"):
        tmp = RENDERS / f".{stem}.{ext}.part"
        r = subprocess.run([cn.COLAB, "download", "-s", box, f"/content/out/{stem}.{ext}", str(tmp)],
                           stdin=subprocess.DEVNULL, capture_output=True, text=True)
        if r.returncode or not tmp.exists():
            log(f"{box}: download of {stem}.{ext} failed: {(r.stdout + r.stderr)[-200:]}")
            return False
        tmp.replace(RENDERS / f"{stem}.{ext}")
    log(f"{box}: brought home {stem}.mp4 ({master(video, lang).stat().st_size / 1e6:.0f} MB)")
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("videos", nargs="+")
    ap.add_argument("--boxes", nargs="+", required=True)
    ap.add_argument("--langs", nargs="+", default=["en", "zh"])
    ap.add_argument("--depth", type=int, default=2, help="jobs queued on a box at once")
    ap.add_argument("--poll", type=int, default=120)
    ap.add_argument("--gpu", default="L4", help="accelerator for a box that has to be recreated")
    args = ap.parse_args()
    skip = set(SKIP.read_text().split()) if SKIP.exists() else set()
    assigned: dict[str, str] = {}  # job tag -> box
    while True:
        todo = [(v, lg) for v in args.videos for lg in args.langs
                if not master(v, lg).exists() and f"{v}_{lg}" not in skip and (STATE / f"preview_{v}.ok").exists()]
        if not todo and not any((STATE / f"preview_{v}.ok").exists() is False for v in args.videos):
            log("all masters are home")
            return
        # first ask every box what it holds, so a job is never handed to a second box
        states = {}
        for box in args.boxes:
            try:
                states[box] = box_state(box)
            except subprocess.TimeoutExpired:
                states[box] = None
            if states[box] is None:
                listed = cn.colab("sessions", check=False)
                if f"[{box}]" not in listed:  # Colab recycled it: get a new VM under the same name
                    for tag in [t for t, b in assigned.items() if b == box]:
                        del assigned[tag]
                    r = subprocess.run([cn.COLAB, "new", "-s", box, "--gpu", args.gpu], stdin=subprocess.DEVNULL,
                                       capture_output=True, text=True)
                    log(f"{box}: gone; new VM: {(r.stdout + r.stderr).strip().splitlines()[-1][:120]}")
                else:
                    log(f"{box}: no answer")
        for box, st in states.items():
            if st and st["toolchain"]:
                for t in st["ready"]:
                    if t not in st["done"] and t not in st["fail"]:
                        assigned.setdefault(t, box)
        for box, st in states.items():
            if st is None:
                continue
            if not st["toolchain"]:
                if not st["setup_running"]:
                    for tag in [t for t, b in assigned.items() if b == box]:
                        del assigned[tag]  # a fresh VM: its jobs are gone
                    setup(box)
                continue
            for tag in st["done"]:
                v, lg = tag.rsplit("_", 1)
                if not master(v, lg).exists() and fetch(box, v, lg):
                    assigned.pop(tag, None)
            for tag in st["fail"]:
                if assigned.pop(tag, None):
                    log(f"{box}: render of {tag} FAILED (see /content/q/render_{tag}.log on the box)")
                    skip.add(tag)
            held = [t for t in st["ready"] if t not in st["done"] and t not in st["fail"]]
            free = args.depth - len(held)
            for v, lg in todo:
                if free <= 0:
                    break
                tag = f"{v}_{lg}"
                if tag in assigned or master(v, lg).exists():  # held elsewhere, or just brought home
                    continue
                r = subprocess.run([sys.executable, "-u", str(ROOT / "tools" / "colab_push.py"), v, "--lang", lg,
                                    "--session", box], capture_output=True, text=True)
                if r.returncode == 0 and "PUSHED" in r.stdout:
                    assigned[tag] = box
                    free -= 1
                    log(f"{box}: pushed {tag}")
                else:
                    log(f"{box}: push of {tag} failed: {(r.stdout + r.stderr)[-300:]}")
                    break
        time.sleep(args.poll)


if __name__ == "__main__":
    main()
