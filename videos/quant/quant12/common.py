"""Helpers shared by the scenes of Part 12 (The Volatility Surface)."""

from __future__ import annotations

from explainer.quant import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 12

IV = QC.IMPLIED       # implied volatility
LV = QC.IDEA          # local volatility, models
RV = QC.GAIN          # realized
BAD = QC.LOSS
SPOT = QC.SPOT
OPT = QC.OPTION


def real_data(text: str, corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def illustration(text: str = r"illustration", corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


SIM = QC.Q  # simulated, risk-neutral objects
FAKE = GREY_B


def simulated(text: str = r"simulated", corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def pct(u, d=0):
    return f"{100 * u:.{d}f}\\%"


def axes3(x_range, y_range, z_range, x_length=7.0, y_length=4.6, z_length=3.0, shift=DOWN * 0.5):
    """3D axes in the part's style (no ticks; labels are added fixed in frame)."""
    ax = ThreeDAxes(x_range=x_range, y_range=y_range, z_range=z_range, x_length=x_length, y_length=y_length,
                    z_length=z_length, tips=False,
                    axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
    return ax.shift(shift)


def grid_fn(xs, ys, Z):
    """A smooth function z(x, y) through a grid Z[len(ys), len(xs)] (bilinear, clamped)."""
    import numpy as _np
    from scipy.interpolate import RegularGridInterpolator

    f = RegularGridInterpolator((_np.asarray(ys, float), _np.asarray(xs, float)), _np.asarray(Z, float),
                                bounds_error=False, fill_value=None)

    def z(x, y):
        x = min(max(x, xs[0]), xs[-1])
        y = min(max(y, ys[0]), ys[-1])
        return float(f([[y, x]])[0])
    return z


def surf3(ax, f, x_range, y_range, z_lo, z_hi, colors=None, resolution=(24, 16), opacity=0.8):
    """z = f(x, y) on 3D axes, coloured by height (blue -> orange -> red), clipped to [z_lo, z_hi]."""
    import numpy as _np

    colors = colors or [(QC.SPOT, z_lo), (IV, 0.5 * (z_lo + z_hi)), (QC.LOSS, z_hi)]
    s = Surface(lambda u, v: ax.c2p(u, v, float(_np.clip(f(u, v), z_lo, z_hi))), u_range=list(x_range),
                v_range=list(y_range), resolution=resolution, fill_opacity=opacity, stroke_width=0.3,
                stroke_color=GREY_D)
    s.set_fill_by_value(axes=ax, colorscale=colors, axis=2)
    return s


def fixed(scene, *mobs):
    """Pin 2D labels to the frame of a 3D scene, hidden until faded in."""
    for m in mobs:
        scene.add_fixed_in_frame_mobjects(m)
        scene.remove(m)
