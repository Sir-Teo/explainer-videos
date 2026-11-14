"""Helpers shared by the scenes of Part 10 ("Writing It Down")."""

from __future__ import annotations

from fractions import Fraction

import numpy as np

from explainer.music.kit import *  # noqa: F403
from explainer.music.monochord import score as SC
from explainer.music.notations import (CJK, MONO, PARCHMENT, RED_LINE, byte_row, code_block, gongche, jianpu, light, mensural, mensural_shape,  # noqa: F401
                                       neume_sign, neumes, piano_roll, qin_character, square_staff, tablature, time_sign)
from explainer.music.staff import Staff, glyph, music_font  # noqa: F401

from .compute import CACHE, CLIPS, load  # noqa: F401

PART = 10
clip = clip_loader(CACHE, CLIPS)
P = SC.Pitch.parse
CLAY = "#C9A27A"
INK = "#F5C542"
PAGE = "#EDE6D6"
TUNE_SCORE = SC.tune_score()
WORDS = ["Twin-", "kle,", "twin-", "kle,", "lit-", "tle", "star,"]

# what each notation keeps: 1 yes, 0.5 in part, 0 no
KEEP_COLS = [r"which note", r"how long", r"its spelling", r"how to play it", r"exactly when, \\ and how loud"]
KEEP_ROWS = [
    (r"neumes", (0.5, 0, 0, 0, 0)),
    (r"Guido's staff", (1, 0, 1, 0, 0)),
    (r"mensural notes", (1, 1, 1, 0, 0)),
    (r"tablature", (1, 1, 0, 1, 0)),
    (r"figured bass", (0.5, 1, 1, 0, 0)),
    (r"gongche", (1, 0.5, 0, 0, 0)),
    (r"jianpu", (1, 1, 0, 0, 0)),
    (r"the modern staff", (1, 1, 1, 0.5, 0.5)),
    (r"a piano roll", (1, 1, 0, 0, 1)),
    (r"MIDI", (1, 1, 0, 0, 1)),
    (r"MusicXML, \ MEI", (1, 1, 1, 0.5, 0.5)),
]


def chapter(scene, number, title, question, lit=(), extra=(), spoken=None):
    open_chapter(scene, number, title, question, lit=lit, part=PART, extra=extra, spoken=spoken)


def phrase_score(k: int, bars: int = 2, words: bool = False) -> SC.Score:
    """Phrase ``k`` of the Tune (0 to 5) as a score of its own."""
    src = SC.tune_score(words=words)
    ms = src.measures(0)[2 * k: 2 * k + bars]
    return SC.Score([SC.Voice([e for m in ms for e in m])], key=0, time=src.time, tempo=src.tempo)


def phrase_notes(k: int) -> list:
    return phrase_score(k).voices[0].notes


def steps_of(notes, base: str = "C4") -> list[int]:
    """Scale steps above a note: what a staff's lines and spaces count."""
    b = P(base).diatonic
    return [n.pitch.diatonic - b for n in notes]


def caption(text: str, mob, font_size: int = 22, color=GREY_B, buff: float = 0.18, direction=DOWN) -> VGroup:
    return label(text, font_size=font_size, color=color).next_to(mob, direction, buff=buff)


def panel(mob, title: str, width: float = 6.0, height: float = 3.3, color=GREY_D, font_size: int = 22) -> VGroup:
    """A notation in a frame with its name: ``.body`` is the notation."""
    frame = RoundedRectangle(width=width, height=height, corner_radius=0.15, stroke_color=color, stroke_width=1.5)
    name = label(title, font_size=font_size, color=GREY_A).move_to(frame.get_top() + DOWN * 0.3)
    mob.move_to(frame.get_center() + DOWN * 0.2)
    if mob.width > width - 0.5:
        mob.scale((width - 0.5) / mob.width)
    if mob.height > height - 1.0:
        mob.scale((height - 1.0) / mob.height)
    g = VGroup(frame, name, mob)
    g.body, g.frame, g.name = mob, frame, name
    return g


def page_image(a: np.ndarray, height: float, ink=(30, 28, 26), paper=(237, 230, 214)) -> ImageMobject:
    """A bitmap of a page (1 is ink) as a picture: dark ink on paper."""
    z = np.asarray(a, dtype=float)
    rgb = np.zeros(z.shape + (3,), dtype=np.uint8)
    for c in range(3):
        rgb[..., c] = (paper[c] * (1 - z) + ink[c] * z).astype(np.uint8)
    img = ImageMobject(rgb)
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["linear"])
    img.height = height
    return img


def tick_mark(value: float, size: float = 0.2) -> VMobject:
    """A filled dot for yes, a ring for in part, a faint dash for no."""
    if value >= 1:
        return Dot(radius=size * 0.5, color=GOOD)
    if value > 0:
        return Circle(radius=size * 0.45, color=GOOD, stroke_width=2.5)
    return Line(LEFT * size * 0.4, RIGHT * size * 0.4, color=GREY_D, stroke_width=2.5)


def keep_table(rows=None, font_size: int = 21, row_step: float = 0.44, col_step: float = 1.75, name_width: float = 3.0) -> VGroup:
    """The part's ledger of what each notation keeps.  ``.rows[i]`` is a row (name and marks), ``.head`` the column
    names."""
    rows = KEEP_ROWS if rows is None else rows
    g = VGroup()
    head = VGroup(*[label(c, font_size=font_size - 3, color=GREY_B).move_to([name_width + (j + 0.5) * col_step, 0.55, 0]) for j, c in enumerate(KEEP_COLS)])
    g.head = head
    g.add(head)
    g.rows = []
    for i, (name, marks) in enumerate(rows):
        y = -i * row_step
        nm = label(name, font_size=font_size, color=TUNE).move_to([0, y, 0], aligned_edge=LEFT)
        r = VGroup(nm, *[tick_mark(v).move_to([name_width + (j + 0.5) * col_step, y, 0]) for j, v in enumerate(marks)])
        g.add(r)
        g.rows.append(r)
    g.center()
    return g
