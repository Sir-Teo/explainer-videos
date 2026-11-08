"""Timeline labels retain their gaps when an edge label needs clamping."""

import pytest
from manim import Rectangle, VGroup

from explainer.philosophy import studio


@pytest.mark.parametrize("years", [
    (-600, -590, -580, -570, -560, -550),
    (2000, 2005, 2010, 2015, 2020, 2025),
])
def test_clustered_labels_fit_without_colliding(monkeypatch, years):
    # Fixed wide boxes reproduce long translated dates without invoking TeX.
    monkeypatch.setattr(studio, "TIMELINE", [(y, "name") for y in years])
    monkeypatch.setattr(studio, "label", lambda *a, **kw: Rectangle(width=2.5, height=0.25))
    strip = studio.timeline(lit=years)
    for sign in (-1, 1):
        row = sorted((t for t in strip.labels if t.get_y() * sign > 0), key=lambda t: t.get_x())
        assert row[0].get_left()[0] >= -6.9 - 1e-6
        assert row[-1].get_right()[0] <= 6.9 + 1e-6
        for left, right in zip(row, row[1:]):
            assert right.get_left()[0] - left.get_right()[0] >= 0.2 - 1e-6


@pytest.mark.parametrize("name_length, count", [(200, 2), (60, 8)])
def test_crowded_event_names_keep_readable_dates(monkeypatch, name_length, count):
    years = list(range(1970, 1970 + count))
    monkeypatch.setattr(studio, "TIMELINE", [(y, "x" * name_length) for y in years])

    def text_box(text, **kw):
        box = VGroup(*[Rectangle(width=0.08, height=0.25).shift([i * 0.08, 0, 0]) for i in range(len(text))])
        box.tex_string, box.tex_strings = text, [text]
        return box

    monkeypatch.setattr(studio, "label", text_box)
    strip = studio.timeline(lit=years)
    # Topic names may be omitted, but the dates must retain their text size.
    assert all(t.height >= 0.25 - 1e-6 for t in strip.labels)
    assert all(t.width <= 5.8 for t in strip.labels)
    # Replacing a long name must not retain duplicate glyphs through Manim's
    # transform alignment; a four-character date has four glyph boxes.
    assert all(len(t.submobjects) == 4 for t in strip.labels if len(t.tex_string) == 4)
    for sign in (-1, 1):
        row = [t for t in strip.labels if t.get_y() * sign > 0]
        assert sum(t.width for t in row) + 0.2 * (len(row) - 1) <= 13.6 + 1e-6
