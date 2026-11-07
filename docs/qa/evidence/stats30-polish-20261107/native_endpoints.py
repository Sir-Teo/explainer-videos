"""Reproduce selected Part 30 endpoint captures at native 1920x1080 resolution.

Run from the repository root with the rendering environment active:
    python docs/qa/evidence/stats30-polish-20261107/native_endpoints.py

Uses the normal QA worker and its provenance/warning checks. This only evaluates
animation endpoints, with silent timing; it does not establish playback approval.
"""

import os
os.environ.update(EXPLAINER_TTS="silent", EXPLAINER_LANG="en")

from contextlib import contextmanager
from pathlib import Path
import shutil
import subprocess
import sys
from types import SimpleNamespace

ROOT = Path("/workspace/explainer-videos")
sys.path.insert(0, str(ROOT))
SCENES = ('Hook', 'Pitman', 'HodgesLehmann', 'Influence', 'Breakdown', 'Huber', 'Scale', 'Regression', 'Multivariate', 'Heavy', 'World')


def capture(scene):
    import manim
    from tools import qa_series

    original = manim.tempconfig

    @contextmanager
    def native(config):
        with original(dict(config, quality="high_quality")):
            yield

    manim.tempconfig = native
    source = qa_series.OUT / "stats30/en" / scene / "Tex"
    qa_series.OUT = ROOT / "renders/qa/native1080"
    target = qa_series.OUT / "stats30/en" / scene / "Tex"
    target.mkdir(parents=True, exist_ok=True)
    if source.exists():
        shutil.copytree(source, target, dirs_exist_ok=True)
    return qa_series.worker(SimpleNamespace(video="stats30", lang="en", worker=scene,
                                           motion=False, cached_only=True))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        sys.exit(capture(sys.argv[1]))
    for scene in SCENES:
        # Isolate Manim/language/cache state just as the normal QA runner does.
        result = subprocess.run([sys.executable, __file__, scene], cwd=ROOT)
        print(f"1080p endpoint capture {scene}: exit {result.returncode}", flush=True)
        if result.returncode not in (0, 1):
            sys.exit(result.returncode)
