"""The watch standard's gate (tools/check_watch.py, videos/cs/SYLLABUS.md 1.2) and the instruments it leans on.

Part 7 is the pilot: it must keep passing.  The other checks make sure the gate fails what it should."""

import sys
import textwrap
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import check_watch  # noqa: E402


def test_the_pilot_passes():
    r = check_watch.check("cs7")
    assert r["problems"] == [], r["problems"]
    assert r["ratio"] >= check_watch.MOTION_FLOOR
    assert r["checkpoint"] >= 2 and r["wrong_idea"] >= 1


def test_the_gate_fails_a_slide_deck(tmp_path):
    src = textwrap.dedent('''
        class Slides(VoiceoverScene):
            def construct(self):
                self.play(FadeIn(objectives_card([])))
                with self.voiceover("This is Part 9. It is important to note that, under these assumptions, the "
                                    "model is illustrative and not necessarily a measured result in this model."):
                    self.play(FadeIn(a), FadeIn(b), FadeIn(c))
    ''')
    p = tmp_path / "s01_slides.py"
    p.write_text(src)
    st = check_watch.chapter_stats(p, "Slides")
    assert st["fade"] == 4 and st["motion"] == 0 and st["predict"] == 0 and st["objectives"] == 1
    assert st["first"].startswith("This is Part 9")
    text = " ".join(st["narration"])
    hedges = sum(1 for h in check_watch.HEDGES for _ in __import__("re").finditer(h, text, flags=2))
    assert hedges >= 3


def test_sentences_split():
    assert len(check_watch.sentences("One two. Three four five? Six seven!")) == 3


@pytest.fixture(scope="module")
def manim():
    return pytest.importorskip("manim")


def test_meter_and_race_follow_their_trackers(manim):
    from explainer.cs import Meter, Race

    t = manim.ValueTracker(0)
    m = Meter("CPI", t, values=np.array([np.nan, 3.0, 2.0, 1.5]), fmt="{:.2f}")
    assert m._text() == "-"
    t.set_value(2.4)
    assert m.value() == 2.0 and m._text() == "2.00"
    r = Race([("fast", 1.0, "#ffffff"), ("slow", 4.0, "#ffffff")], unit="ms")
    assert r.total == 4.0


def test_pipeline_flow_reads_the_chart(manim):
    from explainer.cs import PipelineFlow

    chart = {"chart": [{"IF": 0, "ID": None, "EX": None, "MEM": None, "WB": None, "events": []},
                       {"IF": 1, "ID": 0, "EX": None, "MEM": None, "WB": None, "events": []},
                       {"IF": 2, "ID": 1, "EX": 0, "MEM": None, "WB": None, "events": []}],
             "seq": {"0": {"text": "add a0, a0, a0", "flushed": False}, "1": {"text": "halt", "flushed": False},
                     "2": {"text": "?", "flushed": False}}}
    f = PipelineFlow(chart)
    assert f.state(2) == {"IF": None, "ID": 1, "EX": 0, "MEM": None, "WB": None}  # "?" past halt is empty
    assert f.state(5)["IF"] is None


def test_a_shortened_line_keeps_its_translation(tmp_path, monkeypatch):
    """A line with a hedge cut (the watch retrofit) is spoken in Chinese from the line it was cut from."""
    import json

    from explainer import lang

    table = {"title": "", "chapters": {}, "lines": {
        "k1": {"scene": "Hook", "en": "The core is fast. <bookmark mark='a'/> This is a model, not a measured clock. "
                                     "It wins.", "zh": "核心很快。<bookmark mark='a'/>这是模型。它赢了。"},
        "k2": {"scene": "Other", "en": "The core is fast. <bookmark mark='a'/> It wins.", "zh": "别的场景。<bookmark mark='a'/>"}}}
    (tmp_path / "narration_zh.json").write_text(json.dumps(table, ensure_ascii=False))
    monkeypatch.setattr(lang, "LANG", "zh")
    lang._table.cache_clear()
    out = lang._shortened("The core is fast. <bookmark mark='a'/> It wins.", tmp_path, "Hook")
    assert out == table["lines"]["k1"]["zh"]
    assert lang._shortened("Something else entirely. <bookmark mark='a'/>", tmp_path, "Hook") is None
    assert lang._shortened("The core is fast. It wins.", tmp_path, "Hook") is None  # the bookmark went missing
    lang._table.cache_clear()


def test_fades_get_the_entrance_their_content_suggests(manim, monkeypatch):
    """explainer.cs.watch.lively: arrows grow, lines draw, short formulas are written, small groups cascade."""
    from explainer.cs.watch import lively

    m = manim
    assert type(lively(m.FadeIn(m.Arrow(m.LEFT, m.RIGHT)))) is m.GrowArrow
    assert type(lively(m.FadeIn(m.Line(m.LEFT, m.RIGHT)))) is m.Create
    assert type(lively(m.FadeIn(m.MathTex(r"x^2")))) is m.Write
    assert type(lively(m.FadeIn(m.VGroup(m.Dot(), m.Square(), m.Circle())))) is m.LaggedStart
    long = m.FadeIn(m.MathTex(r"a + b + c + d + e + f + g + h + i + j + k + l + m + n"))
    assert type(lively(long)) is m.FadeIn  # a long formula keeps its fade
    monkeypatch.setenv("EXPLAINER_PLAIN_FADES", "1")
    assert type(lively(m.FadeIn(m.Arrow(m.LEFT, m.RIGHT)))) is m.FadeIn
