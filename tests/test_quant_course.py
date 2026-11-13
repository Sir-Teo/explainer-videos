"""Quant, Built: the course table matches the films, and the course site builds from it.

    python -m pytest -q tests/test_quant_course.py

The table (``videos/quant/course``) names chapters by the numbers in the films' chapter titles, so a renumbered
manifest must fail here rather than mislabel a track on the site.
"""

import re
import subprocess
import sys
from pathlib import Path

import pytest

from videos.quant import course, labs

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "videos" / "quant" / "course" / "site"
PARTS = range(1, course.N_PARTS + 1)


def test_every_part_has_an_entry():
    assert sorted(course.PARTS) == list(PARTS)
    assert sum(b - a + 1 for _, _, (a, b), _ in course.ACTS) == course.N_PARTS


@pytest.mark.parametrize("n", PARTS)
def test_entry_matches_the_film(n):
    p = course.PARTS[n]
    chapters = course.chapters(n)
    numbers = {c[1] for c in chapters if c[1] is not None}
    for tier in "UDI":
        listed = getattr(p, tier)
        assert set(listed) <= numbers, f"Part {n}: {tier} lists chapters {set(listed) - numbers} the film does not have"
    assert not (set(p.U) & set(p.D)) and not (set(p.U) & set(p.I)) and not (set(p.D) & set(p.I)), "one home tier each"
    assert chapters[0][3] == "U", "the cold open is for everyone"
    assert chapters[-1][3] == "*" and "ecap" in chapters[-1][2], "the last chapter is the recap"
    assert p.level in ("U", "M"), "a part starts at undergraduate or master's level"
    if p.level == "U":
        assert p.U, "a part that opens at undergraduate level has undergraduate chapters"
    assert all(q < n for q in p.prereq), "prerequisites come earlier"
    assert set(p.objectives) == set("UMDI") and all(p.objectives[k] for k in "UMDI")
    assert 3 <= len(p.results) <= 5 and all(name and tex for name, tex in p.results)
    for text in (p.question, p.story, p.handoff, p.outside):
        assert text and "  " not in text and not text.endswith(" ")
    assert p.question.endswith("?")
    for _, path in p.also:
        assert (ROOT / path).exists(), path


def test_every_part_has_doctoral_and_industry_material():
    for n in PARTS:
        tiers = {c[3] for c in course.chapters(n)}
        assert "D" in tiers or n == 34, f"Part {n} has no doctoral chapter"  # Part 34 is the industry part
        assert "I" in tiers, f"Part {n} has no industry chapter"


def test_tracks():
    assert set(course.TRACKS) == set(course.TRACK_TIERS) == set("UMDI")
    assert len(course.track_parts("M")) == course.N_PARTS
    undergraduate = course.track_parts("U")
    assert 1 in undergraduate and 10 in undergraduate and 43 in undergraduate and 14 not in undergraduate


def test_tex_is_balanced():
    for n in PARTS:
        for name, tex in course.PARTS[n].results:
            assert tex.count("{") == tex.count("}"), f"Part {n}, {name}"
            assert len(re.findall(r"\\left(?![a-zA-Z])", tex)) == len(re.findall(r"\\right(?![a-zA-Z])", tex)), (n, name)
            assert tex.count(r"\Bigl") == tex.count(r"\Bigr") and tex.count(r"\bigl") == tex.count(r"\bigr"), (n, name)


def test_every_widget_exists():
    source = "\n".join(f.read_text() for f in sorted((SITE / "widgets").glob("*.js")))
    defined = set(re.findall(r"\bW\.([a-z]+) = function", source))
    wanted = {course.PARTS[n].widget for n in PARTS}
    assert wanted <= defined, f"missing interactives: {sorted(wanted - defined)}"
    assert len(wanted) == course.N_PARTS, "one interactive per part, none shared"
    assert "hero" in defined
    assert source.rstrip().endswith("QB.mount();"), "the boot file must come last"


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    out = tmp_path_factory.mktemp("site")
    run = subprocess.run([sys.executable, "tools/course_site.py", "--out", str(out), "--parts", "5", "10", "36", "43", "--quant-only"],
                         cwd=ROOT, capture_output=True, text=True)
    assert run.returncode == 0, run.stderr[-3000:]
    return out


def test_site_builds(site):
    for name in ("index.html", "tracks.html", "labs.html", "reading.html", "syllabus.html", "part10.html"):
        assert (site / "quant" / name).stat().st_size > 5000, name
    assert (site / ".nojekyll").exists() and (site / "assets" / "widgets.js").stat().st_size > 50_000
    index = (site / "quant" / "index.html").read_text()
    assert index.count('class="pcard"') == course.N_PARTS and 'data-widget="hero"' in index


def test_part_page_has_the_course_material(site):
    page = (site / "quant" / "part10.html").read_text()
    for needle in ('data-widget="hedge"', 'id="objectives"', 'id="results"', 'id="chapters"', 'id="lab"', 'id="notes"',
                   'id="reading"', 'id="zh"', "Manufacture an option by delta hedging", "Black-Scholes premium",
                   "Desk questions, with solutions", "Problems, with worked solutions", "For the researcher",
                   "python -m videos.quant.labs 10", "labs/lab10.png"):
        assert needle in page, needle
    assert page.count('<li data-tier=') == len(course.chapters(10))
    assert (site / "quant" / "labs" / "lab10.png").stat().st_size > 10_000
    assert (site / "quant" / "labs" / "lab10.py").read_text() == labs.source(10)


def test_readme_math_survives_markdown(site):
    page = (site / "quant" / "part05.html").read_text()
    assert r"\(\sigma\)" in page, "inline LaTeX from the README reaches the page for KaTeX"
    for name in ("part05.html", "part10.html", "part36.html", "part43.html", "reading.html", "syllabus.html"):
        text = (site / "quant" / name).read_text()
        assert not re.search(r"zzMATH\d|\bMATH\d+\b", text), f"{name}: a math placeholder leaked"
    assert "$1.75 million" in page, "dollar amounts are not mistaken for math"


def test_review_logs_stay_out_of_the_course(site):
    """Earlier QA passes left review logs in some READMEs; they are not course material."""
    for name in ("part36.html", "part43.html"):
        text = (site / "quant" / name).read_text()
        assert "Current visual review" not in text and "当前视觉审阅" not in text
    assert "Worked problems: six basic" in (site / "quant" / "part36.html").read_text()
