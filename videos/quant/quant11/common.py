"""Helpers shared by the scenes of Part 11 (Trading Options)."""

from __future__ import annotations

from explainer.quant import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 11

SPOT = QC.SPOT
GAMMA = QC.GAIN       # gamma, realized moves
THETA = QC.LOSS       # theta, decay
VEGA = QC.IMPLIED     # implied volatility, vega
OPT = QC.OPTION       # option values, books
ALT = QC.IDEA


def real_data(text: str, corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def illustration(text: str = r"illustration", corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def tbar(ax, x, t, color, width=0.5, lo=0.0):
    top, bot = ax.c2p(x, max(t, lo)), ax.c2p(x, min(t, lo))
    w = ax.c2p(width, 0)[0] - ax.c2p(0, 0)[0]
    return Rectangle(width=w, height=max(abs(top[1] - bot[1]), 0.01), stroke_width=0, fill_color=color,
                     fill_opacity=0.85).move_to((top + bot) / 2)


def pause(question: str, width: float = 5.6, font_size=22, corner=DR):
    """A pause-and-predict card, in a corner."""
    return pause_card(question, width=width, font_size=font_size).to_corner(corner, buff=0.3)


def axes3d(x_range, y_range, z_range, x_length=7.4, y_length=5.0, z_length=3.4, shift=DOWN * 0.6):
    ax = ThreeDAxes(x_range=x_range, y_range=y_range, z_range=z_range, x_length=x_length, y_length=y_length,
                    z_length=z_length, tips=False,
                    axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
    return ax.shift(shift)


def hint3d(*rows, corner=UR, font_size=24, ax=None):
    """The axis names of a 3D scene, as a fixed caption: (text, colour) rows, in x, y, z order.

    With ``ax``, each axis takes its row's colour, so the caption reads as a key to the axes."""
    if ax is not None:
        for a, (_, c) in zip((ax.x_axis, ax.y_axis, ax.z_axis), rows):
            a.set_color(c)
    return VGroup(*[label(t, font_size=font_size, color=c) for t, c in rows]).arrange(
        DOWN, aligned_edge=LEFT, buff=0.12).to_corner(corner, buff=0.4)


def surf(ax, f, x_range, y_range, colors, resolution=(32, 24), opacity=0.85):
    """z = f(x, y) coloured by height through ``colors`` [(colour, z), ...]."""
    s = Surface(lambda u, v: ax.c2p(u, v, f(u, v)), u_range=x_range, v_range=y_range, resolution=resolution,
                fill_opacity=opacity, stroke_width=0.3, stroke_color=GREY_D, checkerboard_colors=False)
    s.set_fill_by_value(axes=ax, colorscale=colors, axis=2)
    s.set_fill(opacity=opacity)
    return s


def fixed(scene, *mobs):
    """Pin captions to the frame in a 3D scene (added, then removed so they can be faded in)."""
    scene.add_fixed_in_frame_mobjects(*mobs)
    scene.remove(*mobs)


def day_str(ts):
    from datetime import datetime, timezone
    return datetime.fromtimestamp(float(ts), tz=timezone.utc).strftime("%-d %B %Y")
