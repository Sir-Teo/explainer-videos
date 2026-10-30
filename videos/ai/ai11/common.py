"""Helpers shared by the scenes of Part 11 ("Going Downhill")."""

from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 11

# one colour per optimizer, for the whole part
OPT_COLORS = {
    "gd": GREY_B, "sgd": GREY_B, "sgdm": "#7FD3FF", "hb": "#7FD3FF", "momentum": "#7FD3FF", "nesterov": "#4FA3D9",
    "adagrad": "#B39DDB", "rmsprop": "#FFB3C1", "adam": C.MODEL_Q, "adamw": C.BITS, "adam_l2": "#FF6B8B",
    "lion": "#FF8FA3", "shampoo": "#5CD0B3", "kfac": "#5CD0B3", "soap": "#C792EA", "muon": C.INTERVAL,
    "ng": C.TRUE_P, "sfadamw": "#FFB070",
}
OPT_NAMES = {
    "gd": r"gradient descent", "sgd": r"SGD", "sgdm": r"SGD $+$ momentum", "hb": r"heavy ball",
    "momentum": r"momentum", "nesterov": r"Nesterov", "adagrad": r"AdaGrad", "rmsprop": r"RMSProp", "adam": r"Adam",
    "adamw": r"AdamW", "adam_l2": r"Adam $+$ L2", "lion": r"Lion", "shampoo": r"Shampoo", "kfac": r"K-FAC",
    "soap": r"SOAP", "muon": r"Muon", "ng": r"natural gradient", "sfadamw": r"schedule-free AdamW",
}
SAY = {"sgdm": "SGD with momentum", "adamw": "AdamW", "lion": "Lion", "shampoo": "Shampoo", "soap": "SOAP",
       "muon": "Muon", "gd": "gradient descent", "adam": "Adam", "kfac": "K-FAC", "ng": "the natural gradient",
       "hb": "the heavy ball"}
SCHED_COLORS = {"constant": GREY_B, "cosine": "#7FD3FF", "wsd": C.BITS, "ema": "#C792EA", "sf": "#FFB070",
                "small": "#5CD0B3"}
HIST = C.HUMAN  # history cards
PANEL_FILL = "#121722"


def panel(width, height, center=ORIGIN, color=GREY_D) -> RoundedRectangle:
    return RoundedRectangle(width=width, height=height, corner_radius=0.15, stroke_color=color, stroke_width=1.5,
                            fill_color=PANEL_FILL, fill_opacity=1).move_to(center)


def era_strip(events, head_text=r"How we got here", tag_text=r"milestones evenly spaced, \ not to scale",
              y0=-0.2, color=None, font_size=21):
    """An era timeline: events [(year, text)] evenly spaced, alternating above and below; returns the marks."""
    color = color or HIST
    n = len(events)
    xs = np.linspace(-6.0, 6.0, n)
    axis = Line([-6.7, y0, 0], [6.7, y0, 0], color=GREY_C, stroke_width=3)
    marks, skel = [], VGroup()
    for i, ((yr, txt), x) in enumerate(zip(events, xs)):
        up = i % 2 == 0
        stem = Line([x, y0, 0], [x, y0 + (0.9 if up else -0.9), 0], color=color, stroke_width=2.5)
        dot = Dot([x, y0, 0], radius=0.08, color=color)
        yl = label(rf"{yr}", font_size=30, color=color)
        t = label(txt, font_size=font_size, color=WHITE)
        w = VGroup(yl, t).arrange(DOWN, buff=0.06)
        w.next_to(stem.get_end(), UP if up else DOWN, buff=0.08)
        keep_in_frame(w, margin=0.12)
        marks.append(VGroup(stem, dot, w))
        skel.add(VGroup(stem.copy().set_stroke(GREY_D), Dot([x, y0, 0], radius=0.06, color=GREY_D),
                        yl.copy().set_color(GREY_D).move_to(yl)))
    head = label(head_text, font_size=42).to_edge(UP, buff=0.3)
    tag = note(tag_text).to_corner(DR, buff=0.2)
    return head, axis, tag, skel, marks


def lag(anims, **kw) -> Animation:
    anims = list(anims)
    return LaggedStart(*anims, **kw) if anims else Wait(kw.get("run_time", 0.1))


def predict_card(question: str) -> VGroup:
    """'Pause and predict', centred: the question the next experiment answers."""
    return pause_card(question, width=10.0, font_size=30).move_to(UP * 0.3)


def takeaway_card(head: str, body: str, link: str = "") -> VGroup:
    """The chapter's takeaway: a headline and a line or two in a card, and (under it) where the idea leads next."""
    c = definition_card(head, body, color=C.BITS, width=10.4, font_size=30, kind=r"Takeaway")
    g = VGroup(c)
    if link:
        g.add(label(link, font_size=24, color=GREY_A).next_to(c, DOWN, buff=0.4))
    return g.move_to(UP * 0.2)


def dec(x: float) -> str:
    """A small positive number as a plain decimal for narration and labels: 0.00025, 0.002, 0.4."""
    if x == 0:
        return "0"
    d = max(0, -int(math.floor(math.log10(abs(x)))) + 1)
    s = f"{x:.{d}f}".rstrip("0").rstrip(".")
    return s


def lr_tex(x: float) -> str:
    """A learning rate for MathTex: 2 \\times 10^{-3}, or a plain decimal when it reads better."""
    if x >= 0.01:
        return dec(x)
    e = int(math.floor(math.log10(x) + 1e-9))
    m = x / 10 ** e
    ms = f"{m:.2f}".rstrip("0").rstrip(".")
    return (rf"{ms} \times 10^{{{e}}}" if ms != "1" else rf"10^{{{e}}}")


def words(n: int) -> str:
    w = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]
    return w[n] if 0 <= n < len(w) else f"{n:,}"


def times(r: float) -> str:
    """A ratio for narration: 'about 3 times', 'about 1.4 times'."""
    return f"{r:.0f}" if r >= 3 else f"{r:.1f}"


def bits_axes(x_range, y_range, x_length=8.0, y_length=4.4, center=ORIGIN, xlabel=r"training steps",
              ylabel=r"held-out bits per character", y_step=None, x_step=None, font_size=22, xfmt=None, yfmt=None):
    """Axes with ticks and tick labels for a training curve."""
    xs = x_step or (x_range[1] - x_range[0]) / 4
    ys = y_step if y_step and y_step > 0 else (y_range[1] - y_range[0]) / 4
    ax = CornerAxes(x_range=[x_range[0], x_range[1], xs], y_range=[y_range[0], y_range[1], ys], x_length=x_length,
                    y_length=y_length, tips=False,
                    axis_config={"stroke_color": GREY_C, "include_ticks": False})
    ax.move_to(center)
    xfmt = xfmt or (lambda v: f"{int(round(v)):,}".replace(",", "{,}"))
    yfmt = yfmt or (lambda v: f"{v:.1f}")
    xt = VGroup(*[MathTex(xfmt(v), font_size=font_size - 2, color=GREY_B).next_to(ax.c2p(v, y_range[0]), DOWN, buff=0.1)
                  for v in np.arange(x_range[0], x_range[1] + 1e-9, xs)])
    # tick labels at round values: the nicest step near a quarter of the range, from the first multiple above the bottom
    nice = min((0.01, 0.02, 0.025, 0.05, 0.1, 0.2, 0.25, 0.5, 1.0, 2.0, 5.0), key=lambda v: abs(math.log(v / ys)))
    y0 = math.ceil(y_range[0] / nice - 1e-9) * nice
    yt = VGroup(*[MathTex(yfmt(v), font_size=font_size - 2, color=GREY_B).next_to(ax.c2p(x_range[0], v), LEFT, buff=0.1)
                  for v in np.arange(y0, y_range[1] + 1e-9, nice)])
    xl = label(xlabel, font_size=font_size, color=GREY_A).next_to(xt, DOWN, buff=0.12) if xlabel else VGroup()
    yl = label(ylabel, font_size=font_size, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT) if ylabel else VGroup()
    g = VGroup(ax, xt, yt, xl, yl)
    g.ax = ax
    return g


def growing(ax, xs, ys, t: ValueTracker, color, stroke_width=3.0, f=lambda v: v):
    """A curve drawn up to the tracker's x (a training replay)."""

    def make():
        n = max(2, int(np.searchsorted(xs, t.get_value(), side="right")))
        pts = [ax.c2p(x, f(y)) for x, y in zip(xs[:n], ys[:n]) if np.isfinite(y)]
        return VMobject(color=color, stroke_width=stroke_width).set_points_as_corners(pts if len(pts) > 1 else pts * 2)

    return always_redraw(make)


def step_counter(t: ValueTracker, anchor, direction=UL, font_size=26):
    return always_redraw(lambda: MathTex(rf"\text{{step }}{int(t.get_value()):,}".replace(",", "{,}"),
                                         font_size=font_size, color=WHITE).next_to(anchor, direction, buff=0.1))
