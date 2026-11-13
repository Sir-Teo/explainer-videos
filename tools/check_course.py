#!/usr/bin/env python
"""Check the course material of some parts of a series: the entry, the lab, the interactive, and the built page.

    python tools/check_course.py stats 11 12 13        # these parts
    python tools/check_course.py analysis              # every part that has an entry

For each part it runs the checks of ``tests/test_courses.py`` (the entry against the manifest, the lab, the
interactive's name), builds the part's page into a scratch folder, and (where Node and Playwright are installed)
opens the page at desktop and phone width, drags every slider to both ends and presses every button, and fails on
any script error, a blank canvas or a page wider than the screen.  Exit status 0 means every part passed.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("OMP_NUM_THREADS", "1")  # small matrices: threaded BLAS only hurts on a busy machine
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(ROOT / "tools"))


def main() -> int:
    import matplotlib

    matplotlib.use("Agg")
    import series_site
    import test_courses as t
    from videos import coursekit

    coursekit.TOLERANT = True  # other ranges may be half written while this one is checked
    if len(sys.argv) < 2 or sys.argv[1] not in coursekit.SERIES:
        print(__doc__)
        return 0 if "--help" in sys.argv or "-h" in sys.argv else 2
    series, parts = sys.argv[1], [int(x) for x in sys.argv[2:]]
    parts = parts or sorted(coursekit.course(series).parts)
    out = Path(tempfile.mkdtemp(prefix=f"course-{series}-"))
    failed, pages = [], []
    for n in parts:
        try:
            t.check_entry(series, n)
            t.check_widget(series, n)
            t.check_lab(series, n, out / "figs")
            print(f"{series}{n}: entry, interactive name and lab ok", flush=True)
        except Exception:  # noqa: BLE001  (report every part, then fail)
            failed.append(n)
            print(f"{series}{n}: FAILED\n{traceback.format_exc(limit=6)}", flush=True)
    try:
        series_site.build(out, [series], parts, log=lambda *a, **k: None, run_labs=True, pages_only=True)
        pages = [str(out / series / f"part{n:02d}.html") for n in parts if n not in failed]
    except Exception:  # noqa: BLE001
        failed.append("site")
        print(f"site build FAILED\n{traceback.format_exc(limit=8)}")
    if pages:
        run = subprocess.run(["node", str(ROOT / "tools" / "check_widgets.js"), *pages], capture_output=True, text=True)
        print(run.stdout.strip() or run.stderr.strip()[-2000:])
        if run.returncode not in (0, 3):  # 3: Playwright is not installed here; the Python checks still ran
            failed.append("widgets")
    print(f"pages: {out}/{series}/" + ("" if failed else "   ALL OK"))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
