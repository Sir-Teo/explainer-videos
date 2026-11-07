"""Helpers shared by the scenes of Part 16 (Computing Prices)."""

from __future__ import annotations

from explainer.quant import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 16

SPOT = QC.SPOT
OPT = QC.OPTION
BAD = QC.LOSS
GOOD = QC.GAIN
IV = QC.IMPLIED
DELTA = QC.DELTA
VEGA = QC.VEGA

METHOD_COL = {"plain": GREY_B, "antithetic": QC.THETA, "control": QC.GAIN, "sobol": QC.Q, "pseudo-random": GREY_B,
              "Sobol": QC.Q, "Sobol + bridge": QC.OPTION, "Monte Carlo (QE, 50 steps)": GREY_B,
              "ADI (Craig-Sneyd)": QC.DELTA, "COS": QC.GAIN, "Carr-Madan FFT": QC.Q}


def illustration(text: str = r"illustration", corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def loglog(x_lo, x_hi, y_lo, y_hi, xlabel, ylabel, x_length=6.4, y_length=4.2, xt=None, yt=None, font_size=15):
    """Axes in log10 units with tick labels as powers of ten."""
    import numpy as np
    xt = xt or list(range(int(np.ceil(x_lo)), int(np.floor(x_hi)) + 1))
    yt = yt or list(range(int(np.ceil(y_lo)), int(np.floor(y_hi)) + 1))
    return axes([x_lo, x_hi], [y_lo, y_hi], x_length=x_length, y_length=y_length, xlabel=xlabel, ylabel=ylabel,
                xticks=xt, yticks=yt, xfmt=lambda u: f"10^{{{int(round(u))}}}", yfmt=lambda u: f"10^{{{int(round(u))}}}",
                log_x=True, font_size=font_size)


def sci(x: float, digits: int = 0) -> str:
    """A number in scientific notation for MathTex: 2\\times 10^{-2}, not 2e-02."""
    import math
    e = int(math.floor(math.log10(abs(x))))
    m = x / 10 ** e
    if round(m, digits) >= 10:
        m, e = m / 10, e + 1
    return rf"{m:.{digits}f}\times 10^{{{e}}}"


METHOD_COL.update({"Monte Carlo, control variate": QC.THETA, "PCA": QC.GAIN, "Halton": QC.THETA, "random": GREY_B,
                   "euler": QC.LOSS, "milstein": QC.GAIN})


def predict(question: str, width: float = 6.0, font_size=24):
    """The chapter's 'pause and predict' card."""
    return pause_card(question, width=width, font_size=font_size)


def polyline(ax, xs, ys, color, stroke_width=3, dots=True, radius=0.05):
    """A line through (xs, ys) on ``ax``, with a dot at each point."""
    pts = [ax.c2p(a, b) for a, b in zip(xs, ys)]
    g = VGroup(VMobject(stroke_color=color, stroke_width=stroke_width).set_points_as_corners(pts))
    if dots:
        g.add(*[Dot(p_, radius=radius, color=color) for p_ in pts])
    return g


def chapter(scene, n: int, title: str, question: str, say: str, lit=()):
    """The chapter card with its one spoken line."""
    c = chapter_card(n, title, question, lit=lit, part=PART)
    with scene.voiceover(say):
        scene.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
    scene.play(FadeOut(c))


def fixed(scene, *mobs):
    """Pin text to the screen in a 3D scene (added, then removed so it can be faded in)."""
    scene.add_fixed_in_frame_mobjects(*mobs)
    scene.remove(*mobs)
    return mobs


def data_range(*arrays, pad=0.06, zero=False):
    """Full finite support for display, without moving observations to plot edges."""
    import numpy as np
    values = np.concatenate([np.asarray(a, float).ravel() for a in arrays])
    values = values[np.isfinite(values)]
    if zero:
        values = np.r_[values, 0.0]
    if not len(values):
        raise ValueError("No finite observations")
    lo, hi = float(values.min()), float(values.max())
    margin = max(hi - lo, abs(lo) * 0.05, 1e-8) * pad
    return lo - margin, hi + margin


_base_axes = axes


def axes(x_range, y_range, **kwargs):
    """Keep selected tick labels inside the displayed support."""
    for name, support in (("xticks", x_range), ("yticks", y_range)):
        if kwargs.get(name) is not None:
            kwargs[name] = [x for x in kwargs[name] if support[0] <= x <= support[1]]
    return _base_axes(x_range, y_range, **kwargs)


def pause_card(text, width=12.4, font_size=25):
    """Keep this part's prediction-width API local."""
    return wrapped_label(text, max_width=width, font_size=font_size, color=QC.IDEA).to_edge(DOWN, buff=0.3)


def flat_camera(scene):
    """Release pinned labels and restore the normal camera after a 3D segment."""
    scene.remove_fixed_in_frame_mobjects(*list(scene.camera.fixed_in_frame_mobjects))
    scene.set_camera_orientation(phi=0, theta=-90 * DEGREES, gamma=0, zoom=1.0, frame_center=ORIGIN)
