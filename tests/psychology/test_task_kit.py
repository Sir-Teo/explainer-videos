"""The browser task kit (``videos/psychology/course/site/widgets/00_tasks.js``) and the rule that an experiment
on the course site stores and sends nothing.  The experiments themselves are driven in a browser by
``tools/check_course.py psychology N`` (a scripted participant in ``tools/check_widgets.js``)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import series_site as site  # noqa: E402

WIDGETS = ROOT / "videos" / "psychology" / "course" / "site" / "widgets"
DEFINES = re.compile(r"\bW\.([A-Za-z0-9_]+) = function")
# anything that would keep a reader's data, or send it anywhere
FORBIDDEN = ("localStorage", "sessionStorage", "indexedDB", "document.cookie", "fetch(", "XMLHttpRequest",
             "sendBeacon", "WebSocket", "EventSource", "postMessage", "navigator.clipboard")


def test_experiments_store_and_send_nothing():
    files = sorted(WIDGETS.glob("*.js"))
    assert files
    for f in files:
        text = f.read_text()
        for word in FORBIDDEN:
            assert word not in text, f"{f.name} uses {word}: an experiment's data stay in the page's memory"


def test_the_kit_comes_first_and_defines_no_interactive():
    files = sorted(WIDGETS.glob("*.js"))
    assert files[0].name == "00_tasks.js"
    kit = files[0].read_text()
    assert not DEFINES.findall(kit) and "QB.task = T" in kit
    for name in ("T.create", "T.timed", "T.stage", "T.message", "T.now", "T.wrap"):
        assert f"{name} = function" in kit


def test_every_interactive_is_an_experiment_on_the_kit():
    for f in sorted(WIDGETS.glob("parts_*.js")):
        text = f.read_text()
        bodies = re.split(r"\n  W\.[A-Za-z0-9_]+ = function", text)[1:]
        assert len(bodies) == len(DEFINES.findall(text))
        for name, body in zip(DEFINES.findall(text), bodies):
            assert re.search(r"\bT\.(create|timed)\(el,", body), f"{name} does not register a task with the kit"


def test_a_check_of_one_part_still_gets_the_kit(tmp_path):
    (tmp_path / "assets").mkdir()
    site.write_widgets(tmp_path, "psychology", {"berandom"})
    bundle = (tmp_path / "assets" / "widgets-psychology.js").read_text()
    assert 0 < bundle.index("QB.task = T") < bundle.index("W.berandom = function")
