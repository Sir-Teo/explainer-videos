"""Check a part of *Industry, Built* against the Register (videos/industry/SYLLABUS.md §2.7).

    python tools/check_register.py industry1          # one part
    python tools/check_register.py --all              # every built part
    python tools/check_register.py --stale            # every row past its stale-after date

A part passes when every key its scenes, compute module and lab ask for (``get("...")``, ``row("...")``,
``span("...")``) has a Register row, and every row entered for the part has a source, a URL (unless it is an
assumption), an ISO checked date and a range that holds its value.  Prints ALL OK or the problems, and exits 1 on any.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from explainer.industry import register  # noqa: E402

KEY = re.compile(r"""(?<![.\w])(?:get|row|span)\(\s*["']([a-z0-9_.]+)["']""")  # register.get, not obj.get


def keys_used(part: int) -> set[str]:
    files = sorted((ROOT / "videos" / "industry" / f"industry{part}").glob("*.py"))
    lab = ROOT / "videos" / "industry" / "labs" / f"lab{part:02d}.py"
    files += [lab] if lab.exists() else []
    used = set()
    for f in files:
        used.update(KEY.findall(f.read_text()))
    return used


def check(part: int) -> list[str]:
    known = {r.key for r in register.rows()}
    out = [f"industry{part}: no Register row for {k!r}" for k in sorted(keys_used(part) - known)]
    out += [f"industry{part}: {p}" for p in register.problems(part)]
    if not register.rows(part):
        out.append(f"industry{part}: no rows entered for this part")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("video", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--stale", action="store_true")
    a = ap.parse_args()
    if a.stale:
        stale = [r for r in register.rows() if r.stale()]
        for r in stale:
            print(f"stale: {r.key} (checked {r.checked}): {r.source}")
        print("ALL OK" if not stale else f"{len(stale)} stale rows")
        return 1 if stale else 0
    if a.all:
        parts = sorted(int(p.parent.name[len("industry"):])
                       for p in (ROOT / "videos" / "industry").glob("industry[0-9]*/manifest.py"))
    elif a.video and re.fullmatch(r"industry\d+", a.video):
        parts = [int(a.video[len("industry"):])]
    else:
        ap.error("name a part (industry1) or pass --all or --stale")
    problems = [p for n in parts for p in check(n)]
    for p in problems:
        print(p)
    if not problems:
        print(f"ALL OK ({', '.join(f'industry{n}: {len(keys_used(n))} keys' for n in parts)})")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
