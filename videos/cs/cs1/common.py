"""Helpers shared by the scenes of Part 1 ("What Is a Computation?")."""

from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 1

# one meaning per colour, for the whole part (the series' palette, explainer/style.py)
DATA = C.CS_DATA  # symbols, inputs, numbers being worked on
CTRL = C.CS_CONTROL  # states, rules, tables
HEAD = C.CS_HEAD  # the head, the current step
CODE = C.CS_CODE  # descriptions <M>: programs as data
FUNC = C.CS_FUNC  # functions, lambda terms
COST = C.CS_COST  # steps, time
YES = C.CS_TRUE  # halts, accepts, true
NO = C.CS_FALSE  # loops, rejects, false, contradiction
LIMIT = C.CS_LIMIT  # the impossible
INF = C.CS_INF  # infinite lists and sets
ADV = C.CS_ADVERSARY  # the diagonal machine that does the opposite
HIST = C.HUMAN  # people and dates

PEBBLE_COLORS = ["#C9B79C", "#B8A88E", "#D6C7AE", "#A99A82", "#C2B49B"]


def pebble(radius=0.13, seed=0, color=None) -> VGroup:
    """A small stone: a slightly irregular, shaded ellipse."""
    rng = np.random.default_rng(seed)
    col = color or PEBBLE_COLORS[seed % len(PEBBLE_COLORS)]
    w, h = radius * 2 * rng.uniform(1.0, 1.25), radius * 2 * rng.uniform(0.78, 0.95)
    base = Ellipse(width=w, height=h, stroke_width=1.2, stroke_color="#6E6352", fill_color=col, fill_opacity=1)
    shine = Ellipse(width=w * 0.45, height=h * 0.32, stroke_width=0, fill_color=WHITE, fill_opacity=0.28)
    shine.move_to(base.get_center() + np.array([-w * 0.14, h * 0.17, 0]))
    g = VGroup(base, shine).rotate(rng.uniform(-0.6, 0.6))
    return g


def pebble_pile(n: int, center=ORIGIN, cols=6, radius=0.13, seed=0, gap=0.04) -> VGroup:
    """n pebbles in rows of ``cols``, filling from the bottom, slightly jittered."""
    rng = np.random.default_rng(seed + 100)
    g = VGroup()
    step = 2 * radius + gap
    for i in range(n):
        r, c = divmod(i, cols)
        p = pebble(radius, seed + i)
        p.move_to(np.array([(c - (cols - 1) / 2) * step * 1.08, r * step * 0.92, 0])
                  + np.array([rng.uniform(-0.02, 0.02), rng.uniform(-0.02, 0.02), 0]))
        g.add(p)
    return g.move_to(center, aligned_edge=DOWN) if n else g


def bowl(width=2.2, height=0.9, color=GREY_B) -> VGroup:
    """A shallow bowl drawn as an arc with a rim."""
    arc = Arc(radius=width / 2, start_angle=PI + 0.25, angle=PI - 0.5, color=color, stroke_width=3)
    arc.stretch_to_fit_height(height)
    rim = Line(arc.get_start(), arc.get_end(), color=color, stroke_width=1.5, stroke_opacity=0.4)
    return VGroup(arc, rim)


def tape_from(entry: dict, lo: int, tape: int = 0, cell=0.62, font_size=30, show_state=True, **kw) -> TapeView:
    """A TapeView of one recorded configuration (``hist[i]`` from compute; its tape windows start at cell ``lo``)."""
    syms = list(entry["tapes"][tape])
    return TapeView(syms, head=entry["heads"][tape] - lo, state=entry["state"] if show_state else None, cell=cell,
                    font_size=font_size, **kw)


def replay(scene, view: TapeView, hist: list, lo: int, tape: int = 0, table: RuleTable | None = None,
           rule_index=None, per_step=0.8, start=0, stop=None, counter=None):
    """Step a TapeView through a recorded run.  ``hist`` entries carry the state, heads and tapes after each step
    (entry i is the configuration before step i, with ``rule`` the rule applied).  ``rule_index`` maps the rule
    number to a row of ``table``.  ``counter`` (a DecimalNumber) shows the step count."""
    stop = len(hist) - 1 if stop is None else stop
    for i in range(start, stop):
        a, b = hist[i], hist[i + 1]
        anims = []
        if table is not None and a["rule"] is not None:
            row = rule_index(a["rule"]) if rule_index else a["rule"]
            scene.play(table.light(row), run_time=per_step * 0.25)
        new_sym = b["tapes"][tape][a["heads"][tape] - lo]
        move = b["heads"][tape] - a["heads"][tape]
        step = view.step(new_sym, move, b["state"], run_time=per_step * 0.75)
        if counter is not None:
            anims.append(counter.tracker.animate(run_time=per_step * 0.75).set_value(i + 1))
        scene.play(step, *anims)


def spacetime_mob(arr: np.ndarray, width=None, height=None, palette=None) -> ImageMobject:
    """A run as a picture: rows are steps (time runs down), columns are cells.  Values: 0 blank, 1 a '1', 2 another
    symbol, 3 the head."""
    pal = palette or ["#151B26", C.BIT1, C.CS_DATA, C.CS_HEAD]
    return bitmap(arr, pal, width=width, height=height)


def history_spacetime(hist: list, lo: int, tape: int = 0) -> np.ndarray:
    """A recorded run (compute's JSON form, windows starting at cell ``lo``) as a space-time array."""
    rows = []
    for e in hist:
        t = e["tapes"][tape]
        row = [0 if c == "_" else (1 if c == "1" else 2) for c in t]
        h = e["heads"][tape] - lo
        if 0 <= h < len(row):
            row[h] = 3
        rows.append(row)
    return np.array(rows, np.int8)


def fmt(n) -> str:
    """An integer with thousands separators, for Tex."""
    return f"{int(n):,}".replace(",", "{,}")


def live_int(value=0, font_size=32, color=COST) -> Integer:
    """An Integer driven by ``.tracker`` (a ValueTracker): animate the tracker, never the number itself, so a change
    in the number of digits redraws cleanly."""
    d = Integer(value, font_size=font_size, color=color, group_with_commas=True)
    d.tracker = ValueTracker(value)
    d.add_updater(lambda m: m.set_value(int(round(m.tracker.get_value()))))
    return d


def step_counter(text=r"steps", color=COST, font_size=30, value=0) -> VGroup:
    """'steps: N' with a live number: animate ``.tracker``."""
    t = label(text + r":", font_size=font_size, color=GREY_A)
    d = live_int(value, font_size + 2, color)
    g = VGroup(t, d).arrange(RIGHT, buff=0.18)
    d.add_updater(lambda m: m.next_to(t, RIGHT, buff=0.18))
    g.num, g.tracker = d, d.tracker
    return g
