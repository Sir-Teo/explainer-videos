"""The course sites of every series but Quant, Built (``tools/series_site.py``): generated from the manifests,
the READMEs and the syllabi, so these tests check that the sources still have the shape the builder reads."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import series_site as site  # noqa: E402

PARTS = {"ai": 31, "stats": 65, "cs": 61, "philosophy": 42, "analysis": 10, "films": 13}


def test_every_part_is_found_and_sits_in_one_act():
    for key, count in PARTS.items():
        entries = site.entries(key)
        assert len(entries) == count, key
        covered = [n for _, _, (a, b), _ in site.acts(key) for n in range(a, b + 1)]
        assert covered == list(range(1, count + 1)), f"{key}: the acts must cover every part once"
        assert len({e.slug for e in entries}) == count
        for e in entries:
            assert e.title and "Part" not in e.title.split()[0], e.video
            assert site.card_line(e), f"{e.video} has no line for the course map"


def test_the_readme_tables_and_syllabi_are_read():
    assert [a[1] for a in site.acts("ai")][:2] == ["Foundations", "Learning from Data"]
    assert site.acts("stats")[0][0] == "Stage I" and site.acts("cs")[-1][2] == (56, 61)
    for key in ("ai", "stats", "cs", "philosophy"):
        rows = site.parts_table(key)[1]
        assert sorted(rows) == list(range(1, PARTS[key] + 1)), f"{key}: a part is missing from the README's table"
        for e in site.entries(key):
            assert site.syllabus_entry(key, e.n)["plan"], f"{e.video} has no entry in SYLLABUS.md"
    twelve = site.syllabus_entry("stats", 12)
    assert twelve["question"].startswith("How do you fit a line") and twelve["prereq"] == "4, 11"
    assert twelve["story"].startswith("Gauss finds a lost asteroid") and "*Story:*" not in twelve["plan"]
    assert all(site.syllabus_entry("stats", n)["question"] for n in range(1, 66))
    assert all(site.syllabus_entry("cs", n)["story"] for n in range(1, 62))


def test_a_series_in_progress_is_read_too():
    """*Music, Built* has its whole plan and its first parts: the acts cover the plan, the entries are what is built."""
    entries = site.entries("music")
    assert [e.video for e in entries][:1] == ["music1"] and entries[0].title == "One String"
    covered = [n for _, _, (a, b), _ in site.acts("music") for n in range(a, b + 1)]
    assert covered == list(range(1, 69))
    assert sorted(site.parts_table("music")[1]) == list(range(1, 69))
    for e in entries:
        assert site.card_line(e) and site.syllabus_entry("music", e.n)["plan"], e.video
        assert sum(site.chapter_minutes(e)) > 30, e.video
        kinds = {k for k, *_ in site.split_readme(e.dir / "README.md")["en"]}
        assert {"problems", "sources", "build"} <= kinds, (e.video, kinds)


def test_lengths_come_from_the_narration():
    for key in PARTS:
        for e in site.entries(key):
            minutes = site.chapter_minutes(e)
            assert len(minutes) == len(site.manifest(e.dir)[1])
            assert sum(minutes) > 15, f"{e.video}: {sum(minutes):.0f} minutes of narration found"


def test_readmes_split_into_course_material():
    r = site.split_readme(ROOT / "videos/cs/cs7/README.md")
    assert {"problems", "glossary", "sources", "build"} <= {k for k, *_ in r["en"]}
    assert [k for k, *_ in r["zh"]] == ["problems"] and "Pebble" in r["intro"]
    for key in ("ai", "stats", "cs"):
        for e in site.entries(key):
            kinds = {k for k, *_ in site.split_readme(e.dir / "README.md")["en"]}
            assert "problems" in kinds, f"{e.video}: no problem set found in its README"
    # QA logs of review passes are not course material
    for e in site.entries("ai") + site.entries("stats"):
        r = site.split_readme(e.dir / "README.md")
        for _, _, heading, _ in r["en"] + r["zh"]:
            assert not re.search(r"\bQA\b|Review|Reviewed|checkpoint", heading), (e.video, heading)
        assert "docs/qa/" not in r["intro"], e.video


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    out = tmp_path_factory.mktemp("site")
    run = subprocess.run([sys.executable, "tools/series_site.py", "--out", str(out), "--parts", "5", "7", "9", "12", "--skip-labs"],
                         cwd=ROOT, capture_output=True, text=True)
    assert run.returncode == 0, run.stderr[-3000:]
    return out


def test_site_builds(built):
    landing = (built / "index.html").read_text()
    for key, count in PARTS.items():
        assert f'href="{key}/index.html"' in landing
        index = (built / key / "index.html").read_text()
        assert index.count('class="pcard"') == count and 'id="map"' in index
        for e in site.entries(key):  # every card points at a page the full build writes
            assert f'href="{e.slug}.html"' in index
    assert 'href="quant/index.html"' in landing
    for key in ("ai", "stats", "cs", "philosophy"):
        assert (built / key / "syllabus.html").stat().st_size > 30_000
    assert not (built / "analysis" / "syllabus.html").exists()
    assert len(list((built / "films").glob("*.html"))) == 14
    assert (built / "assets" / "course.css").exists() and (built / ".nojekyll").exists()


def test_part_page_has_the_course_material(built):
    page = (built / "stats" / "part12.html").read_text()
    for needle in ("<h1>Least Squares</h1>", "Stage II", 'class="question"', 'class="glance"', 'id="chapters"',
                   "Gauss-Markov", "Problems, with solutions", "Where it comes back", "Sources",
                   "The syllabus's plan for this part", "python -m videos.stats.stats12.compute",
                   "python tools/build.py stats12", 'href="part11.html"', 'href="part13.html"'):
        assert needle in page, needle
    assert page.count('<span class="num">') == len(site.manifest(ROOT / "videos/stats/stats12")[1])
    film_rows = (built / "films" / "quantum.html").read_text().count('<li><span class="num">')
    assert film_rows == len(site.manifest(ROOT / "videos/physics/quantum")[1])
    cs = (built / "cs" / "part07.html").read_text()
    assert 'id="zh"' in cs and "习题与解答" in cs and "Glossary" in cs
    film = (built / "films" / "quantum.html").read_text()
    assert "Quantum Mechanics, Visualized" in film and "python tools/build.py quantum" in film


def test_no_markup_leaks(built):
    for path in built.glob("*/*.html"):
        text = path.read_text()
        assert not re.search(r"zzMATH\d", text), f"{path.name}: a math placeholder leaked"
        assert 'href="../README.md"' not in text and 'href="compute.py"' not in text, f"{path}: a relative link"
