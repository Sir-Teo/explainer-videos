"""Shared instruments for the music series (videos/music/music1 ... music68), *Music, Built*.

    from explainer.music import *

Everything of *AI, Built*'s visual language is reused (``explainer.ai``: ``cmath`` and ``morph``, ``axes``, ``curve``,
camera framing, the lecture cards, ``reference_card``, ``cite``) and so are the analysis series' text helpers and
derivation ladder (``label``, ``note``, ``why``, ``ladder``).  Here, the devices that hold this series together
(videos/music/SYLLABUS.md, section 2):

* :class:`SoundScene` (:mod:`explainer.music.sound`): narrated scenes that also play computed clips;
* :func:`chapter_card`, with **the Chain** (the path music travels, the part's links lit) and the **timeline strip**
  (40,000 BCE to 2030 on a compressed scale, the chapter's years lit);
* :func:`series_map`, the sixty-eight parts in twelve acts;
* :func:`variations_ledger`, the Tune's running record, one row per part;
* :func:`sound_tag`, the label every sound carries when it first plays, and :func:`listen_bar`, the strip that
  shows a clip's progress during a listening window;
* :func:`payoff_card` and :func:`practice_card`.

The visual instruments (strings, scopes, partial bars, spectrograms, the monochord) are in :mod:`explainer.music.viz`,
exported here; the colours in :mod:`explainer.music.palette` (``MC``, ``pc_color``).  Monochord itself, the instrument
the series builds, is :mod:`explainer.music.monochord` and imports no manim.
"""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F401,F403
from explainer.ai import _zh, label, note, wrapped_label, zh  # noqa: F401
from explainer.music.palette import MC, harmonic_color, pc_color  # noqa: F401
from explainer.music.sound import (EXAMPLE_LEVEL, PEAK_CEILING_DB, QUIET_LEVEL, SoundScene, SoundTracker,  # noqa: F401
                                   clip_loader)

SERIES_EN = "Music, Built"
SERIES_ZH = "音乐，从零搭建"

# ---------------------------------------------------------------------------
# The sixty-eight parts in twelve acts
# ---------------------------------------------------------------------------
ACTS = [
    (r"I.\ Sound", (1, 9)),
    (r"II.\ Notes", (10, 15)),
    (r"III.\ Voices", (16, 22)),
    (r"IV.\ A Thousand Years", (23, 27)),
    (r"V.\ After Tonality", (28, 33)),
    (r"VI.\ Many Musics", (34, 40)),
    (r"VII.\ The Craft", (41, 44)),
    (r"VIII.\ The Mind", (45, 47)),
    (r"IX.\ Electric Sound", (48, 53)),
    (r"X.\ The Studio and the Stage", (54, 60)),
    (r"XI.\ Listening Machines", (61, 66)),
    (r"XII.\ Coda", (67, 68)),
]
PARTS = {
    1: r"One String", 2: r"Waves in Air", 3: r"The Spectrum", 4: r"The Ear", 5: r"Consonance", 6: r"Tuning",
    7: r"Strings, Hammers and Bows", 8: r"Pipes, Reeds and Voices", 9: r"Drums, Bars and Bells",
    10: r"Writing It Down", 11: r"Rhythm and Meter", 12: r"Scales and Modes", 13: r"Intervals and Chords",
    14: r"Melody", 15: r"Key",
    16: r"Two Voices", 17: r"Four Voices", 18: r"Progressions", 19: r"Chromatic Harmony", 20: r"Canon and Fugue",
    21: r"Form", 22: r"Analysis",
    23: r"Chant to Polyphony", 24: r"The Renaissance", 25: r"The Baroque", 26: r"The Classical Style",
    27: r"The Romantic Century",
    28: r"New Scales, New Rhythms", 29: r"Twelve Tones", 30: r"Sound Itself", 31: r"Transformations",
    32: r"The Geometry of Chords", 33: r"The Mathematics of Rhythm and Scale",
    34: r"Raga and Tala", 35: r"Maqam", 36: r"Bronze and Silk", 37: r"Timelines", 38: r"Blues and Swing",
    39: r"Changes", 40: r"The Song",
    41: r"Orchestration", 42: r"Composing", 43: r"Performing", 44: r"Music for Picture and Play",
    45: r"The Scene", 46: r"Expectation and Emotion", 47: r"Origins and Universals",
    48: r"Digital Audio", 49: r"Filters, Delay and Reverb", 50: r"Dynamics, Distortion and Pitch",
    51: r"Synthesis I: Oscillators and Filters", 52: r"Synthesis II: FM, Grains and Physical Models",
    53: r"MIDI, Sequencers and the DAW",
    54: r"Microphones and Loudspeakers", 55: r"Rooms and Space", 56: r"Recording and Mixing",
    57: r"Mastering and Loudness", 58: r"Compression for the Ear", 59: r"Live Sound", 60: r"The Business of Music",
    61: r"Pitch, Onsets and Transcription", 62: r"Beat, Chords and Structure", 63: r"Finding Music",
    64: r"Source Separation", 65: r"Machines that Compose", 66: r"Generative Audio",
    67: r"Doing Research in Music", 68: r"The Variations",
}
# Short names, for the series map and the payoff cards
SHORT = dict(PARTS)
SHORT.update({7: r"Strings and Bows", 8: r"Pipes and Voices", 9: r"Drums and Bells", 13: r"Chords",
              27: r"The Romantics", 28: r"New Scales", 32: r"Chord Geometry", 33: r"Rhythm, Mathematically",
              44: r"Picture and Play", 46: r"Expectation", 47: r"Origins", 49: r"Filters and Reverb",
              50: r"Dynamics and Pitch", 51: r"Synthesis I", 52: r"Synthesis II", 53: r"MIDI and the DAW",
              54: r"Mics and Speakers", 56: r"Recording, Mixing", 57: r"Mastering", 58: r"Codecs",
              60: r"The Business", 61: r"Transcription", 62: r"Beat and Chords", 65: r"Machines Compose",
              67: r"Doing Research"})


def act_of(part: int) -> int:
    """The act (1-12) a part belongs to."""
    for i, (_, (a, b)) in enumerate(ACTS, 1):
        if a <= part <= b:
            return i
    raise ValueError(part)


def series_map(current: int | None = None, done: int = 0, font_size=17, width=13.6, height=7.3) -> VGroup:
    """The twelve acts in two rows of six; each part a line.  Parts up to ``done`` are white, ``current`` is gold and
    boxed, the rest are dim.  ``.part[p]`` is the line of part p; ``.cols[i]`` act i+1."""
    cols = VGroup()
    for act, (a, b) in ACTS:
        head = label(act, font_size=font_size + 3, color=GREY_A)
        rows = VGroup()
        for p in range(a, b + 1):
            color = MC.TUNE if p == current else (WHITE if p <= done else GREY_C)
            rows.add(label(rf"{p}.\ {SHORT[p]}", font_size=font_size, color=color))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.11)
        if head.width > 2.3:
            head.width = 2.3
        col = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        col.head, col.rows = head, rows
        cols.add(col)
    cols.arrange_in_grid(rows=2, cols=6, buff=(0.22, 0.4), cell_alignment=UL)
    if cols.width > width:
        cols.width = width
    if cols.height > height:
        cols.height = height
    g = VGroup(cols)
    g.cols = cols
    g.part = {}
    for col, (_, (a, b)) in zip(cols, ACTS):
        for p, row in zip(range(a, b + 1), col.rows):
            g.part[p] = row
    if current is not None:
        box = SurroundingRectangle(g.part[current], color=MC.TUNE, buff=0.06, corner_radius=0.05, stroke_width=2)
        g.add(box)
        g.box = box
    return g.move_to(ORIGIN)


# ---------------------------------------------------------------------------
# The Chain: the path a piece of music travels
# ---------------------------------------------------------------------------
CHAIN = [  # the inner loop: one mind to another
    ("mind", r"mind"), ("score", r"score"), ("hands", r"hands"), ("instrument", r"instrument"),
    ("air", r"air"), ("ear", r"ear"), ("listener", r"mind"),
]
DETOUR = [  # the industrial detour, lit from Act IX on
    ("mic", r"microphone"), ("mix", r"mix"), ("master", r"master"), ("codec", r"codec"),
    ("stream", r"stream"), ("speaker", r"loudspeaker"),
]
CHAIN_COLOR = {"mind": "#B39DDB", "score": "#9DD6F0", "hands": "#FFB070", "instrument": MC.STRING, "air": "#7DD3FC",
               "ear": MC.EAR, "listener": "#B39DDB", "mic": "#94A3B8", "mix": "#94A3B8", "master": "#94A3B8",
               "codec": "#94A3B8", "stream": "#94A3B8", "speaker": "#94A3B8"}
# the links each part lights by default (chapter cards may override)
PART_LINKS = {1: ("instrument",), 2: ("air",), 3: ("air", "ear"), 4: ("ear",), 5: ("ear", "listener"),
              6: ("instrument", "ear"), 7: ("instrument",), 8: ("instrument",), 9: ("instrument",),
              **{p: ("score",) for p in range(10, 34)}, **{p: ("mind", "score", "hands") for p in range(34, 41)},
              41: ("score", "instrument"), 42: ("mind", "score"), 43: ("hands",), 44: ("mind", "score"),
              45: ("ear", "listener"), 46: ("listener",), 47: ("mind", "listener"),
              48: ("codec",), 49: ("mix",), 50: ("mix",), 51: ("instrument",), 52: ("instrument",),
              53: ("score", "instrument"), 54: ("mic", "speaker"), 55: ("air", "speaker"), 56: ("mic", "mix"),
              57: ("master",), 58: ("codec",), 59: ("speaker", "air"), 60: ("stream",),
              **{p: ("ear", "score") for p in range(61, 67)},
              67: tuple(k for k, _ in CHAIN), 68: tuple(k for k, _ in CHAIN) + tuple(k for k, _ in DETOUR)}


def chain(lit=(), width=9.4, font_size=18, detour: bool | None = None) -> VGroup:
    """The Chain: mind, score, hands, instrument, air, ear, mind, joined by arrows; the links in ``lit`` glow.
    With ``detour`` (or when a detour link is lit) the second row is drawn: microphone, mix, master, codec, stream,
    loudspeaker, leaving the chain at the air and rejoining it there.  ``.link[key]`` is a link's pill."""
    show_detour = detour if detour is not None else any(k in lit for k, _ in DETOUR)

    def pill(key, name):
        on = key in lit
        col = CHAIN_COLOR[key]
        t = label(name, font_size=font_size, color=BLACK if on else GREY_B)
        r = RoundedRectangle(width=t.width + 0.34, height=0.42, corner_radius=0.2, stroke_width=1.6 if on else 1.0,
                             stroke_color=col if on else GREY_D, fill_color=col, fill_opacity=0.92 if on else 0.08)
        g = VGroup(r, t.move_to(r))
        g.key = key
        return g

    def row(items):
        pills = VGroup(*[pill(k, n) for k, n in items]).arrange(RIGHT, buff=0.42)
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, color=GREY_C, stroke_width=1.6, tip_length=0.11,
                                max_tip_length_to_length_ratio=0.5) for a, b in zip(pills, pills[1:])])
        return pills, arrows

    top, top_arrows = row(CHAIN)
    g = VGroup(top_arrows, top)
    g.link = {p.key: p for p in top}
    if show_detour:
        bot, bot_arrows = row(DETOUR)
        air = g.link["air"]
        VGroup(bot, bot_arrows).next_to(top, DOWN, buff=0.5).set_x(air.get_x())
        down = Arrow(air.get_bottom() + LEFT * 0.12, bot[0].get_top(), buff=0.05, color=GREY_C, stroke_width=1.4,
                     tip_length=0.1, max_tip_length_to_length_ratio=0.5)
        up = Arrow(bot[-1].get_top(), air.get_bottom() + RIGHT * 0.12, buff=0.05, color=GREY_C, stroke_width=1.4,
                   tip_length=0.1, max_tip_length_to_length_ratio=0.5)
        g.add(bot_arrows, bot, down, up)
        g.link.update({p.key: p for p in bot})
    if g.width > width:
        g.width = width
    return g


# ---------------------------------------------------------------------------
# The timeline strip, 40,000 BCE to 2030, on a compressed scale
# ---------------------------------------------------------------------------
TIMELINE = [
    (-40000, r"the Hohle Fels flute"),
    (-530, r"Pythagoras"),
    (-433, r"the bells of Marquis Yi"),
    (100, r"Nicomachus tells of the hammers"),
    (510, r"Boethius, \textit{De institutione musica}"),
    (1025, r"Guido's staff"),
    (1584, r"Zhu Zaiyu's equal temperament"),
    (1589, r"Vincenzo Galilei weighs the strings"),
    (1636, r"Mersenne's laws"),
    (1638, r"Galileo on the pendulum and the string"),
    (1677, r"Wallis reports the nodes"),
    (1701, r"Sauveur's harmonics"),
    (1713, r"Taylor's vibrating string"),
    (1722, r"Rameau's \textit{Trait\'e}"),
    (1747, r"d'Alembert's wave equation"),
    (1753, r"Bernoulli: a sum of modes"),
    (1759, r"Lagrange's beaded string"),
    (1807, r"Fourier's series"),
    (1863, r"Helmholtz, \textit{On the Sensations of Tone}"),
    (1877, r"Edison's phonograph; Rayleigh's \textit{Theory of Sound}"),
    (1883, r"Kirchhoff's stretching string"),
    (1945, r"Carrier's nonlinear string"),
    (1957, r"Mathews's MUSIC"),
    (1965, r"Plomp and Levelt"),
    (1983, r"Karplus--Strong; MIDI"),
    (2009, r"Bilbao, \textit{Numerical Sound Synthesis}"),
    (2016, r"the Tsiman\'e experiment"),
]
# (year, fraction of the strip): linear between knots, so the centuries with the most history get the most room
_KNOTS = [(-40000, 0.0), (-3000, 0.05), (-600, 0.12), (1000, 0.26), (1500, 0.36), (1700, 0.56), (1800, 0.70),
          (1900, 0.82), (2000, 0.95), (2030, 1.0)]


def year_fraction(year: float) -> float:
    ys, fs = zip(*_KNOTS)
    return float(np.interp(year, ys, fs))


def year_text(year: int) -> str:
    return rf"{-year:,}\ \textsc{{bce}}".replace(",", "{,}") if year < 0 else str(year)


def timeline(lit=(), width=12.4, show_labels=True, font_size=17, extra=()) -> VGroup:
    """The strip; years in ``lit`` glow and get their names.  ``extra``: (year, name) pairs a part adds for its own
    chapter cards."""
    x0 = -width / 2

    def X(y):
        return x0 + width * year_fraction(y)

    events = dict(TIMELINE)
    events.update(dict(extra))
    g = VGroup(Line([X(-40000), 0, 0], [X(2030), 0, 0], color=GREY_D, stroke_width=2))
    for yr, name in ((-40000, r"40{,}000 \textsc{bce}"), (-600, r"600 \textsc{bce}"), (1000, "1000"), (1500, "1500"),
                     (1700, "1700"), (1800, "1800"), (1900, "1900"), (2000, "2000")):
        g.add(Line([X(yr), -0.06, 0], [X(yr), 0.06, 0], color=GREY_D, stroke_width=1.5))
        t = label(name, font_size=13, color=GREY_D).next_to([X(yr), 0, 0], DOWN, buff=0.12)
        if yr == -40000:
            t.align_to([X(yr), 0, 0], LEFT)
        g.add(t)
    labels, anchors = VGroup(), []
    side = 1
    for yr in sorted(events):
        on = yr in lit
        d = Dot([X(yr), 0, 0], radius=0.065 if on else 0.03, color=MC.TUNE if on else GREY_C)
        g.add(d)
        if on and show_labels:
            t = label(rf"{year_text(yr)}\; {events[yr]}", font_size=font_size, color=MC.TUNE)
            t.next_to(d, UP if side > 0 else DOWN, buff=0.14 if side > 0 else 0.4)
            side = -side
            labels.add(t)
            anchors.append(d)
    for row in (1, -1):  # keep the lit labels apart and inside the frame
        same = sorted([t for t in labels if np.sign(t.get_y()) == row], key=lambda t: t.get_x())
        for a, b in zip(same, same[1:]):
            gap = b.get_left()[0] - a.get_right()[0]
            if gap < 0.2:
                b.shift(RIGHT * (0.2 - gap))
        if same and same[-1].get_right()[0] > 6.9:
            same[-1].shift(LEFT * (same[-1].get_right()[0] - 6.9))
            for i in range(len(same) - 2, -1, -1):
                gap = same[i + 1].get_left()[0] - same[i].get_right()[0]
                if gap < 0.2:
                    same[i].shift(LEFT * (0.2 - gap))
        if same and same[0].get_left()[0] < -6.9:
            same[0].shift(RIGHT * (-6.9 - same[0].get_left()[0]))
    leaders = VGroup()  # a displaced label keeps a thin line to its own year
    for t, d in zip(labels, anchors):
        if abs(t.get_x() - d.get_x()) > 0.1:
            above = t.get_y() > 0
            leaders.add(Line(d.get_top() if above else d.get_bottom(), t.get_bottom() if above else t.get_top(),
                             color=MC.TUNE, stroke_width=1, stroke_opacity=0.4))
    g.add(leaders, labels)
    g.labels, g.leaders = labels, leaders
    return g


def chapter_card(number, title: str, question: str = "", lit=(), part: int | None = None, links=None,
                 extra=()) -> VGroup:
    """Chapter title and the question it answers; above, the Chain with the part's links lit (``links`` overrides
    the part's default); below, the timeline strip with this chapter's years lit.  ``card[0]`` is the title group,
    ``card[1]`` the strip, ``card[2]`` the Chain."""
    if zh():
        head_text = (rf"第{part}部分 \textperiodcentered\ " if part else "") + f"第{number}章"
    else:
        head_text = (rf"Part {part} \textperiodcentered\ " if part else "") + f"Chapter {number}"
    head = label(head_text, font_size=28, color=GREY_B)
    t = label(title, font_size=54)
    if t.width > 12.4:
        t.width = 12.4
    g = VGroup(head, t)
    if question:
        q = label(question, font_size=30, color=GREY_A)
        if q.width > 12.4:
            q.width = 12.4
        g.add(q)
    g.arrange(DOWN, buff=0.3).move_to([0, 0.35, 0])
    strip = timeline(lit=lit, extra=extra).to_edge(DOWN, buff=0.9)
    lk = PART_LINKS.get(part, ()) if links is None else links
    ch = chain(lit=lk).to_edge(UP, buff=0.45)
    return VGroup(g, strip, ch)


# ---------------------------------------------------------------------------
# Sound on screen
# ---------------------------------------------------------------------------
SOUND_LABELS = {
    "physical model": r"physical model",
    "synthesized": r"synthesized",
    "illustrative": r"illustrative",
    "rendered": r"rendered from the score",
    "recording": r"recording",
}


def sound_tag(kind: str, detail: str = "", corner=UR, font_size=20) -> VGroup:
    """What the sound is, said on screen when it first plays: ``physical model``, ``synthesized``, ``illustrative``,
    ``rendered from the score``, ``recording`` (with its source in ``detail``)."""
    text = SOUND_LABELS.get(kind, kind) + (rf": \ {detail}" if detail else "")
    t = label(text, font_size=font_size, color=GREY_A)
    icon = speaker_icon(0.2, GREY_A)
    row = VGroup(icon, t).arrange(RIGHT, buff=0.12)
    box = RoundedRectangle(width=row.width + 0.3, height=row.height + 0.2, corner_radius=0.1, stroke_width=1,
                           stroke_color=GREY_D, fill_color="#0B0F17", fill_opacity=0.9)
    return VGroup(box, row.move_to(box)).to_corner(corner, buff=0.3)


def speaker_icon(size=0.24, color=WHITE) -> VGroup:
    """A small loudspeaker with two sound arcs."""
    body = Polygon([-0.5, -0.22, 0], [-0.22, -0.22, 0], [0.1, -0.5, 0], [0.1, 0.5, 0], [-0.22, 0.22, 0],
                   [-0.5, 0.22, 0], stroke_width=0, fill_color=color, fill_opacity=1)
    arcs = VGroup(*[Arc(radius=r, start_angle=-PI / 4, angle=PI / 2, color=color, stroke_width=2).shift(RIGHT * 0.12)
                    for r in (0.3, 0.55)])
    return VGroup(body, arcs).scale(size / 0.5)


def listen_bar(snd: SoundTracker, text: str = r"listen", width=3.2, color=None, font_size=22) -> VGroup:
    """The strip of a listening window: a loudspeaker, a word or a question, and a line that fills as the clip
    plays.  It is driven by the clip's own clock, so it is the one playhead a window always has."""
    color = color or MC.EAR
    icon = speaker_icon(0.22, color)
    t = label(text, font_size=font_size, color=color)
    head = VGroup(icon, t).arrange(RIGHT, buff=0.14)
    w = max(width, head.width)
    track = Line(ORIGIN, RIGHT * w, color=GREY_D, stroke_width=3)
    fill = Line(ORIGIN, RIGHT * 1e-3, color=color, stroke_width=3)
    bar = VGroup(track, fill)
    g = VGroup(head, bar).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    g.track, g.fill, g.head = track, fill, head
    dur = max(snd.duration, 1e-6)

    def upd(m, t_):
        a = float(np.clip(t_ / dur, 0.0, 1.0))
        m.put_start_and_end_on(track.get_start(), track.get_start() + (track.get_end() - track.get_start()) * max(a, 1e-3))

    snd.drive(fill, upd)
    if text and text != r"listen":
        snd.caption(text)
    return g


# ---------------------------------------------------------------------------
# The Variations: the Tune's running record
# ---------------------------------------------------------------------------
def variations_ledger(rows: list[dict], highlight=(), font_size=22, width=12.6) -> VGroup:
    """One row per variation: ``part``, ``title`` (what was done to the Tune), ``seconds`` and ``measure`` (the
    part's measurement, as Tex).  ``.rows[i]`` is a row."""
    head = VGroup(*[label(h, font_size=font_size - 3, color=GREY_B) for h in
                    (r"Part", r"The Tune \ldots", r"length", r"measured")])
    out = VGroup()
    for i, r in enumerate(rows):
        cells = VGroup(
            label(str(r["part"]), font_size=font_size, color=MC.TUNE),
            wrapped_label(r["title"], width * 0.42, font_size, WHITE),
            label(rf"{r['seconds']:.0f} s", font_size=font_size, color=MC.TIME),
            wrapped_label(r["measure"], width * 0.34, font_size - 1, GREY_A),
        )
        out.add(cells)
    xs = [0.0, 0.9, 0.9 + width * 0.42 + 0.4, 0.9 + width * 0.42 + 1.6]
    for cells in [head, *out]:
        for c, x in zip(cells, xs):
            c.move_to([x, 0, 0], aligned_edge=LEFT)
    table = VGroup(head, *out).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
    for cells in [head, *out]:
        y = cells.get_y()
        for c, x in zip(cells, xs):
            c.move_to([table.get_left()[0] + x, y, 0], aligned_edge=LEFT)
    rule = Line(table.get_left(), table.get_left() + RIGHT * table.width, color=GREY_D, stroke_width=1)
    rule.next_to(head, DOWN, buff=0.1).align_to(table, LEFT)
    g = VGroup(table, rule)
    for i in highlight:
        g.add_to_back(SurroundingRectangle(out[i], color=MC.TUNE, buff=0.1, corner_radius=0.08, stroke_width=1.5,
                                           fill_color=MC.TUNE, fill_opacity=0.06))
    if g.width > width:
        g.width = width
    g.rows, g.head = out, head
    return g.move_to(ORIGIN)


# ---------------------------------------------------------------------------
# Payoffs and practice
# ---------------------------------------------------------------------------
def payoff_card(items, font_size=24, title=r"Where this comes back") -> VGroup:
    """``items``: (idea, [part numbers]).  Each row: the idea, an arrow, the parts that use it (number and name)."""
    head = label(title, font_size=font_size + 12)
    rows = VGroup()
    for idea, parts in items:
        left = label(idea, font_size=font_size, color=MC.TUNE)
        right = label(r",\ ".join(rf"{p}\ \textit{{{SHORT[p]}}}" for p in parts), font_size=font_size - 2,
                      color=GREY_A)
        rows.add(VGroup(left, right))
    lw = max(r[0].width for r in rows)
    for r in rows:
        r[0].align_to(ORIGIN, LEFT)
        arrow = MathTex(r"\longrightarrow", font_size=font_size + 4, color=GREY_C)
        r.insert(1, arrow)
        arrow.next_to(ORIGIN, RIGHT, buff=0).shift(RIGHT * (lw + 0.3))
        r[2].next_to(arrow, RIGHT, buff=0.3)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    for r in rows:
        r[1].set_y(r[0].get_y())
        r[2].set_y(r[0].get_y())
    g = VGroup(head, rows).arrange(DOWN, buff=0.5)
    if g.width > 13.4:
        g.width = 13.4
    g.head, g.rows = head, rows
    return g.move_to(ORIGIN)


def practice_card(items, title=r"In practice", font_size=24, width=12.6) -> VGroup:
    """Where the part's ideas live in the working world: ``items`` are (where, what) pairs, e.g.
    (r"instrument makers", r"string scaling: gauge, length and tension for each note")."""
    head = label(title, font_size=font_size + 12, color=CHAIN_COLOR["mic"])
    rows = VGroup()
    for where, what in items:
        a = label(where, font_size=font_size, color=WHITE)
        b = wrapped_label(what, width - 4.6, font_size - 2, GREY_A)
        rows.add(VGroup(a, b))
    lw = max(r[0].width for r in rows)
    for r in rows:
        r[0].align_to(ORIGIN, LEFT)
        r[1].next_to(ORIGIN, RIGHT, buff=0).shift(RIGHT * (lw + 0.45)).align_to(r[0], UP)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.28)
    g = VGroup(head, rows).arrange(DOWN, buff=0.5)
    if g.width > 13.4:
        g.width = 13.4
    if g.height > 7.2:
        g.height = 7.2
    g.head, g.rows = head, rows
    return g.move_to(ORIGIN)


def listen_card(question: str, color=None, width: float = 8.0, font_size=28) -> VGroup:
    """'Pause and listen': the ear-training question of a chapter, asked before the answer is drawn."""
    from explainer.ai.lecture import _body, _card

    color = color or MC.EAR
    icon = speaker_icon(0.2, color)
    tag = label(r"Pause and listen", font_size=font_size - 6, color=color)
    head = VGroup(icon, tag).arrange(RIGHT, buff=0.18)
    return _card(head, _body(question, width - 0.8, font_size), color, width, accent=False)


from explainer.music.viz import *  # noqa: F401,F403,E402
