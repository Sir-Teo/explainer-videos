"""The courses beside *Quant, Built* (``videos/coursekit``): every part of AI, Statistics, Computer Science,
Philosophy and Analysis has a course entry, a runnable lab and an interactive, and they agree with the films.

    python -m pytest -q tests/test_courses.py
    python -m pytest -q tests/test_courses.py -k stats

Each lab asserts the theory it illustrates inside ``run()``, so running it is the test.
"""

import os
import re
import subprocess
import sys
import time
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")  # the labs' matrices are small: threaded BLAS only hurts on a busy machine
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import matplotlib  # noqa: E402

matplotlib.use("Agg")

import pytest  # noqa: E402

from videos import coursekit  # noqa: E402
from videos.coursekit import labs  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
PARTS = [(s, n) for s in coursekit.SERIES for n in range(1, coursekit.course(s).n_parts + 1)]
IDS = [f"{s}{n}" for s, n in PARTS]


def check_entry(series: str, n: int) -> None:
    """A part's course entry is complete and agrees with its manifest (also used by tools/check_course.py)."""
    c = coursekit.course(series)
    assert n in c.parts, f"{series}{n} has no course entry"
    p = c.parts[n]
    assert p.level in "UMD" and len(p.level) == 1
    for text, lo in ((p.question, 30), (p.story, 300), (p.handoff, 60)):
        assert len(text) >= lo and "  " not in text and text == text.strip(), text[:60]
    assert p.question.endswith("?")
    assert set(p.objectives) == set("UMDI") and all(1 <= len(v) <= 3 for v in p.objectives.values())
    assert all(len(o) > 30 and o.endswith(".") for v in p.objectives.values() for o in v)
    assert 3 <= len(p.results) <= 6
    for name, tex in p.results:
        assert name and tex.count("{") == tex.count("}"), f"{series}{n}, {name}: unbalanced braces"
        assert len(re.findall(r"\\left(?![a-zA-Z])", tex)) == len(re.findall(r"\\right(?![a-zA-Z])", tex)), (n, name)
        assert tex.count(r"\Bigl") == tex.count(r"\Bigr") and tex.count(r"\bigl") == tex.count(r"\bigr"), (n, name)
        assert "$" not in tex, "results are TeX without dollar signs"
        assert not re.search(r"\\(?:qquad|quad|cdots|ldots)[A-Za-z]", tex), f"{series}{n}, {name}: two strings joined into one command"
    scenes = c.manifest(n)[1]
    numbers = {int(m.group(1)) for _, _, t in scenes if (m := re.match(r"^(\d+)\.\s", t))} | {0}
    modules = {m for m, _, _ in scenes}
    listed = list(p.U) + list(p.D) + list(p.I)
    assert len(listed) == len(set(listed)), f"{series}{n}: a chapter sits in two tiers"
    for k in listed:
        assert k in numbers or k in modules, f"{series}{n}: chapter {k!r} is not in the manifest"
    assert all(1 <= q < n for q in p.prereq), f"{series}{n}: prerequisites are earlier parts"
    tiers = {t for _, _, _, t in c.chapters(n)}
    assert p.level in tiers or p.level == "M", f"{series}{n}: no chapter at the level the part starts at"
    assert "D" in tiers or "I" in tiers, f"{series}{n}: mark the research or the practice chapters"
    for label, path in p.also:
        assert (ROOT / path).exists(), path


def check_widget(series: str, n: int) -> None:
    import series_site

    c = coursekit.course(series)
    name = c.parts[n].widget
    assert re.fullmatch(r"[a-z][a-z0-9]*", name), f"{series}{n}: widget names are lowercase letters and digits"
    assert name in series_site.widgets_defined(series), f"{series}{n}: QB.W.{name} is not defined in site/widgets/"
    assert [p.widget for p in c.parts.values()].count(name) == 1, f"{series}: {name} is used by two parts"


def check_lab(series: str, n: int, tmp_path: Path) -> None:
    assert labs.path(series, n).exists(), f"{series}{n} has no lab"
    module = labs.load(series, n)
    assert module.TITLE and module.GOAL and len(module.TASKS) == 3, "a title, a goal and three things to change"
    assert module.__doc__ and module.__doc__.startswith(f"Lab {n}:")
    source = labs.source(series, n)
    assert not re.search(r"^\s*(from|import) (manim|torch|pandas|sklearn|statsmodels)\b", source, re.M), "numpy and scipy only"
    assert "assert " in source, "a lab checks its own result"
    start = time.time()
    lab = module.run(seed=0)
    assert time.time() - start < 60, "a lab runs in seconds"
    assert len(lab.rows) >= 3 and all(isinstance(a, str) and isinstance(b, str) for a, b in lab.rows)
    assert lab.note, "one line saying what the numbers mean"
    assert lab.fig is not None and len(lab.fig.axes) >= 1
    assert labs.save(lab, tmp_path / f"lab{n:02d}.png").stat().st_size > 10_000


@pytest.mark.parametrize("series,n", PARTS, ids=IDS)
def test_course_entry(series, n):
    check_entry(series, n)
    check_widget(series, n)


@pytest.mark.parametrize("series,n", PARTS, ids=IDS)
def test_lab_runs_and_checks_itself(series, n, tmp_path):
    check_lab(series, n, tmp_path)


@pytest.mark.parametrize("series", coursekit.SERIES)
def test_tracks_and_nothing_extra(series):
    c = coursekit.course(series)
    assert set(c.tracks) == set(c.track_intro) == set("UMDI")
    assert sorted(c.parts) == list(range(1, c.n_parts + 1))
    assert labs.available(series) == list(range(1, c.n_parts + 1))
    assert len(c.track_parts("M")) == c.n_parts and 1 in c.track_parts("U")
    assert len(c.track_parts("D")) >= c.n_parts // 2 and len(c.track_parts("I")) >= c.n_parts // 3
    source = "\n".join(f.read_text() for f in sorted((ROOT / "videos" / series / "course" / "site" / "widgets").glob("*.js")))
    assert "document.write" not in source and "innerHTML =" not in source.replace('el.innerHTML = ""', "")
    assert not re.search(r"\b(fetch|XMLHttpRequest|import)\s*\(", source), "the interactives load nothing"


def test_labs_are_seeded():
    a, b = labs.run("stats", 12, seed=0), labs.run("stats", 12, seed=0)
    assert a.rows == b.rows


def test_libraries_import_without_manim(tmp_path):
    """The labs promise numpy, scipy and matplotlib: hide manim and run one of each series from a clean process."""
    code = ("import importlib.util as u, sys\n"
            "find = u.find_spec\n"
            "u.find_spec = lambda name, *a, **k: None if name == 'manim' else find(name, *a, **k)\n"
            "from videos.coursekit import labs\n"
            "for s in ('ai', 'stats', 'cs', 'philosophy', 'analysis'):\n"
            "    assert len(labs.run(s, 1).rows) >= 3\n"
            "assert 'manim' not in sys.modules and not hasattr(sys.modules['explainer'], 'VoiceoverScene')\n")
    env = dict(os.environ, PYTHONPATH=str(ROOT), MPLBACKEND="Agg")
    out = subprocess.run([sys.executable, "-c", code], cwd=ROOT, env=env, capture_output=True, text=True)
    assert out.returncode == 0, out.stderr[-2000:]


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    out = tmp_path_factory.mktemp("site")
    run = subprocess.run([sys.executable, "tools/series_site.py", "--out", str(out), "--series", "analysis"],
                         cwd=ROOT, capture_output=True, text=True)
    assert run.returncode == 0, run.stderr[-3000:]
    return out


def test_part_page_carries_the_course(built):
    c = coursekit.course("analysis")
    page = (built / "analysis" / "part03.html").read_text()
    for needle in (f'data-widget="{c.parts[3].widget}"', 'id="objectives"', 'id="results"', 'id="lab"',
                   'class="track-buttons"', "Undergraduate track", "python -m videos.analysis.labs 3", "labs/lab03.png",
                   "widgets-analysis.js", "Where it goes next", 'href="tracks.html"'):
        assert needle in page, needle
    assert page.count("<li data-tier=") == len(c.chapters(3))
    assert (built / "analysis" / "labs" / "lab03.png").stat().st_size > 10_000
    assert (built / "analysis" / "labs" / "lab03.py").read_text() == labs.source("analysis", 3)
    bundle = (built / "assets" / "widgets-analysis.js").read_text()
    assert bundle.startswith("// Quant, Built") and bundle.rstrip().endswith("QB.mount();")
    assert all(f"W.{p.widget} = function" in bundle for p in c.parts.values())
    index = (built / "analysis" / "index.html").read_text()
    assert 'id="tracks"' in index and index.count('class="tcard') == 4 and "runnable labs" in index
    assert (built / "analysis" / "labs.html").read_text().count('class="lcard"') == 10
    tracks = (built / "analysis" / "tracks.html").read_text()
    assert all(f'id="{k}"' in tracks for k in "UMDI")
