"""The narration read back as lecture text (``tools/lecture_text.py``), for the course sites' lecture notes."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import course_site  # noqa: E402
import lecture_text as lt  # noqa: E402


def test_chapters_follow_the_film_and_drop_the_spoken_heading():
    chapters = lt.film_text(ROOT / "videos/stats/stats12")
    assert len(chapters) == 13 and all(paras for _, paras in chapters)
    title, paras = chapters[1]
    assert title == "1. The principle" and paras[0].text.startswith("Here's the principle in one picture")
    # chapter 2 runs in construct's order, which is not the order the methods are written in
    texts = [p.text for p in chapters[2][1]]
    assert texts[0].startswith("Now the picture that explains everything")
    assert texts[1].startswith("You can check the right angle numerically")


def test_computed_values_become_gaps_and_helpers_are_read():
    paras = [p for _, ps in lt.film_text(ROOT / "videos/quant/quant3") for p in ps]
    gap = next(p for p in paras if "Ten payments of five" in p.text)
    assert gap.gaps == 1 and "<span class=\"val\"" in lt.to_html(gap)
    # psychology's section helpers speak a script given as an argument; the chapter card's question leads
    backfire = lt.chapter_text(ROOT / "videos/psychology/psych55/s09_backfire.py", "Backfire", "8. When nudges backfire")
    assert backfire and "Texas displayed the year's road death toll" in " ".join(p.text for p in backfire)


def test_every_film_has_text_for_every_chapter():
    for manifest in sorted(ROOT.glob("videos/*/*/manifest.py")):
        chapters = lt.film_text(manifest.parent)
        empty = [title for title, paras in chapters if not paras]
        assert not empty, f"{manifest.parent.name}: no narration found for {empty}"


def test_solutions_fold_under_their_problems():
    html = course_site.md_to_html(
        "1. **A problem.** State it.\n\n   *Solution.* Solve it.\n\n   ```\n   code\n   ```\n\n2. **Another.** Go.\n\n"
        "   *Solution.* Done.\n", ROOT)
    folded = course_site.fold_solutions(html)
    assert folded.count('<details class="sol">') == 2 and folded.count("</details>") == 2
    assert folded.index("<pre>") < folded.index("</details>"), "the code block stays inside its solution"
    assert "<em>Solution.</em>" not in folded
