"""The visual instruments of *AI, Built*, in the manner of 3Blue1Brown.

The series' visual language, which every part follows:

1. **One idea per frame, drawn big.**  The object of the sentence fills the frame; words on screen are few and
   large.  The narration explains; the screen shows.
2. **Continuity.**  Objects persist and turn into the next representation (``ReplacementTransform``,
   :func:`morph`, ``MoveToTarget``) instead of fading out and new ones fading in.  ``clear_scene`` is for the end
   of a thought, not the middle of one.
3. **Color is meaning.**  A symbol has the same color in every equation and in the picture it describes
   (:func:`cmath`, with the series' symbol colors in ``explainer.style.C``).
4. **The camera narrates.**  Zoom into the detail that matters (:func:`frame_to`, a ``MovingCameraScene``), and
   orbit a surface when the third dimension is the point (:func:`loss_surface`, a ``ThreeDScene``).
5. **Live quantities.**  Values are ``ValueTracker``\\ s; bars (:class:`LiveBars`), dots on curves (:func:`glow_dot`)
   and readouts follow them, so a change of parameter is seen continuously.
6. **Real numbers.**  What is plotted is computed (the part's ``compute.py``) and asserted in the scene;
   schematics and made-up examples are tagged.

A scene that zooms is ``class X(VoiceoverScene, MovingCameraScene)``; one with a surface is
``class X(VoiceoverScene, ThreeDScene)`` (labels then go through ``add_fixed_in_frame_mobjects``).
"""

from __future__ import annotations

import numpy as np
from manim import *  # noqa: F403

from explainer.style import BACKGROUND, C  # noqa: F401


# ---------------------------------------------------------------------------
# Color-linked mathematics
# ---------------------------------------------------------------------------
def _key(tex: str) -> str:
    return "".join(tex.split())


def cmath(*tex: str, colors: dict | None = None, font_size=44, color=WHITE, **kw) -> MathTex:
    """A formula whose terms are colored by meaning.  Split it into terms with ``{{ }}`` (or pass several strings);
    a term whose TeX equals a key of ``colors`` (spaces ignored) takes that color.  Terms with the same TeX carry
    over between the steps of a derivation, so :func:`morph` slides each one to its new place."""
    m = MathTex(*tex, font_size=font_size, color=color, **kw)
    if colors:
        table = {_key(k): v for k, v in colors.items()}
        for part in m.submobjects:
            s = getattr(part, "tex_string", None)
            if s is not None and _key(s) in table:
                part.set_color(table[_key(s)])
    return m


def morph(scene: Scene, a: Mobject, b: Mobject, run_time: float = 1.4, key_map: dict | None = None,
          path_arc: float = 0.0, **kw) -> None:
    """One step of a derivation, in place: terms present in both formulas move to their new positions, the rest
    fade out and in.  ``b`` should already be positioned."""
    scene.play(TransformMatchingTex(a, b, key_map=key_map or {}, path_arc=path_arc, **kw), run_time=run_time)


def term(m: MathTex, tex: str) -> VMobject:
    """The first term of ``m`` whose TeX is ``tex`` (for braces, boxes and arrows that point at it)."""
    for part in m.submobjects:
        if _key(getattr(part, "tex_string", "")) == _key(tex):
            return part
    raise KeyError(tex)


def brace_note(mob: Mobject, text: str, direction=DOWN, color=GREY_A, font_size=26, buff=0.1) -> VGroup:
    """A brace under (or over) ``mob`` with a short colored note."""
    from explainer.analysis import label

    b = Brace(mob, direction, buff=buff, color=color)
    t = label(text, font_size=font_size, color=color).next_to(b, direction, buff=0.1)
    return VGroup(b, t)


# ---------------------------------------------------------------------------
# Points, glows, bars
# ---------------------------------------------------------------------------
def glow_dot(point, color=YELLOW, radius=0.08, layers=5, spread=3.2, opacity=0.55) -> VGroup:
    """A dot with a soft halo, the marker for "here" on a curve or surface."""
    g = VGroup()
    for k in range(layers, 0, -1):
        r = radius * (1 + (spread - 1) * k / layers)
        g.add(Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=opacity * (1 - k / (layers + 1)) ** 2))
    g.add(Dot(radius=radius, color=color))
    g.move_to(point)
    return g


def code_block(lines, font_size=24, color=GREY_A, font="DejaVu Sans Mono", buff=0.14) -> VGroup:
    """Lines of code as Text, one per line, keeping their indentation (Text drops leading spaces)."""
    em = Text("M" * 20, font=font, font_size=font_size).width / 20
    rows = VGroup(*[Text(s.strip() or ".", font=font, font_size=font_size, color=color) for s in lines])
    rows.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    for r, s in zip(rows, lines):
        if not s.strip():
            r.set_opacity(0)
        r.shift(RIGHT * em * (len(s) - len(s.lstrip(" "))))
    return rows


class LiveBars(VGroup):
    """Bars whose heights follow ``ValueTracker``\\ s (``bars.trackers``), so a distribution can reshape on screen.

    ``bars.to(values)`` gives the animations that take it to new heights; ``bars.bar(i)`` is the i-th bar as drawn
    now.  Labels sit under the bars, values (if shown) over them."""

    def __init__(self, values, max_value: float, height=3.2, bar_width=0.55, gap=0.25, colors=None,
                 labels=None, label_font=26, label_color=GREY_A, show_values=False, digits=2, value_font=22,
                 fill_opacity=0.9, baseline_color=GREY_D, label_mobs=None):
        super().__init__()
        n = len(values)
        self.n, self.max_value, self.h, self.bw, self.gap = n, max_value, height, bar_width, gap
        self.trackers = [ValueTracker(float(v)) for v in values]
        colors = colors if colors is not None else [C.TRUE_P] * n
        self.colors = [colors[i] if isinstance(colors, (list, tuple)) else colors for i in range(n)]
        self.width_total = n * bar_width + (n - 1) * gap
        self.x0 = -self.width_total / 2
        self.base = Line([self.x0 - 0.15, 0, 0], [self.x0 + self.width_total + 0.15, 0, 0], color=baseline_color,
                         stroke_width=1.5)
        self.add(self.base)
        self._bars = []
        for i in range(n):
            self._bars.append(always_redraw(self._maker(i, fill_opacity)))
            self.add(self._bars[i])
        self.values = VGroup()
        if show_values:
            for i in range(n):
                d = DecimalNumber(values[i], num_decimal_places=digits, font_size=value_font, color=self.colors[i])
                d.add_updater(self._value_updater(i))
                self.values.add(d)
            self.add(self.values)
        self.labels = VGroup()
        if label_mobs is not None:
            self.labels = VGroup(*label_mobs)
        elif labels is not None:
            from explainer.analysis import label

            self.labels = VGroup(*[label(t, font_size=label_font, color=label_color) for t in labels])
        for i, lab in enumerate(self.labels):
            lab.next_to([self._cx(i), 0, 0], DOWN, buff=0.18)
        self.add(self.labels)

    def _cx(self, i):
        return self.x0 + i * (self.bw + self.gap) + self.bw / 2

    def _maker(self, i, fill_opacity):
        def make():
            v = max(self.trackers[i].get_value(), 0.0)
            h = max(self.h * v / self.max_value, 0.002)
            left = self.base.get_start() + np.array([0.15 + i * (self.bw + self.gap), 0, 0])
            r = Rectangle(width=self.bw, height=h, stroke_width=0, fill_color=self.colors[i], fill_opacity=fill_opacity)
            r.move_to(left + np.array([self.bw / 2, h / 2, 0]))
            return r
        return make

    def _value_updater(self, i):
        def upd(d):
            d.set_value(self.trackers[i].get_value())
            d.next_to(self._bars[i], UP, buff=0.08)
        return upd

    def place(self, base_y: float, x: float = 0.0) -> "LiveBars":
        """Put the baseline at height ``base_y``, centred on ``x`` (moving by the bounding box would depend on the
        bars' current heights)."""
        self.shift(np.array([x - self.base.get_x(), base_y - self.base.get_y(), 0]))
        return self

    def bar(self, i) -> Mobject:
        return self._bars[i]

    def to(self, values) -> list:
        return [t.animate.set_value(float(v)) for t, v in zip(self.trackers, values)]

    def freeze(self) -> "LiveBars":
        """Stop following the trackers (before fading out)."""
        for m in self.get_family():
            m.clear_updaters()
        return self


# ---------------------------------------------------------------------------
# The camera
# ---------------------------------------------------------------------------
FRAME_W = 14.222222222222221


def frame_to(scene: Scene, target=None, width: float | None = None, margin: float = 1.25, center=None):
    """The animation that moves a ``MovingCameraScene``'s frame onto ``target`` (a mobject or point), wide enough to
    show it with ``margin`` around it (or exactly ``width`` units wide)."""
    frame = scene.camera.frame
    if center is None:
        center = target.get_center() if isinstance(target, Mobject) else (target if target is not None else ORIGIN)
    if width is None:
        if isinstance(target, Mobject):
            width = max(target.width, target.height * 16 / 9) * margin
        else:
            width = FRAME_W
    return frame.animate.set(width=width).move_to(center)


def frame_home(scene: Scene):
    return scene.camera.frame.animate.set(width=FRAME_W).move_to(ORIGIN)


def frame_scale(scene: Scene) -> float:
    """How much the camera is zoomed out (1 at the default frame): multiply sizes of new labels by this."""
    return scene.camera.frame.width / FRAME_W


# ---------------------------------------------------------------------------
# Surfaces
# ---------------------------------------------------------------------------
SURFACE_COLORS = ("#1B2A6B", "#2E6FB0", "#3FB8AF", "#F2D16B", "#F28C5B")


def loss_surface(axes: ThreeDAxes, f, x_range, y_range, resolution=(40, 40), z_lo=None, z_hi=None,
                 colors=SURFACE_COLORS, opacity=0.88, stroke_width=0.35, stroke_color="#0E1117") -> Surface:
    """``z = f(x, y)`` over a rectangle, colored by height from deep blue (low) to warm (high), with a fine mesh."""
    surf = Surface(lambda u, v: axes.c2p(u, v, f(u, v)), u_range=x_range, v_range=y_range, resolution=resolution,
                   fill_opacity=opacity, stroke_width=stroke_width, stroke_color=stroke_color,
                   checkerboard_colors=False)
    if z_lo is None or z_hi is None:
        xs = np.linspace(*x_range, 25)
        ys = np.linspace(*y_range, 25)
        zs = np.array([[f(x, y) for x in xs] for y in ys])
        z_lo = float(zs.min()) if z_lo is None else z_lo
        z_hi = float(zs.max()) if z_hi is None else z_hi
    stops = np.linspace(z_lo, z_hi, len(colors))
    surf.set_fill_by_value(axes=axes, colorscale=list(zip(colors, stops)), axis=2)
    surf.set_fill(opacity=opacity)
    return surf


def surface_path(axes: ThreeDAxes, f, pts, color=YELLOW, lift=0.04, stroke_width=4) -> VMobject:
    """A path drawn on the surface ``z = f(x, y)`` through the (x, y) points ``pts``."""
    p3 = [axes.c2p(x, y, f(x, y)) + np.array([0, 0, lift]) for x, y in pts]
    return VMobject(color=color, stroke_width=stroke_width).set_points_as_corners(p3)


def surface_ball(axes: ThreeDAxes, f, x, y, color=YELLOW, radius=0.11) -> Mobject:
    """A ball resting on the surface at (x, y)."""
    return Dot3D(axes.c2p(x, y, f(x, y)) + np.array([0, 0, radius * 0.6]), radius=radius, color=color)


# ---------------------------------------------------------------------------
# A labelled cloud of points in 3D
# ---------------------------------------------------------------------------
class Cloud3D(VGroup):
    """Points in 3D drawn by projection after turning them by ``cloud.angle`` (a ValueTracker, radians, about the
    vertical axis) and tilting by ``cloud.tilt``: nearer points are larger and brighter, and labels (2D mobjects,
    always facing the viewer) ride along with their points.  ``cloud.zoom`` and ``cloud.focus`` (a point in data
    coordinates) move the view in, without a camera, so labels keep their size."""

    def __init__(self, xyz, colors, scale=3.0, radius=0.075, tilt=0.35, center=ORIGIN, labels: dict | None = None,
                 label_buff=0.1):
        super().__init__()
        self.xyz = np.asarray(xyz, float)
        self.scale_, self.radius, self.center_ = scale, radius, np.asarray(center, float)
        self.angle, self.tilt, self.zoom = ValueTracker(0.0), ValueTracker(tilt), ValueTracker(1.0)
        self.focus = [ValueTracker(0.0) for _ in range(3)]
        self.dots = VGroup(*[Dot(radius=radius, color=c) for c in colors])
        for i, d in enumerate(self.dots):
            d.add_updater(self._dot_updater(i))
        self.labels = VGroup()
        self.label_of = {}
        for i, lab in (labels or {}).items():
            lab.add_updater(self._label_updater(i, label_buff))
            self.labels.add(lab)
            self.label_of[i] = lab
        self.add(self.dots, self.labels)
        self.update()

    def project(self, p):
        f = np.array([t.get_value() for t in self.focus])
        x, y, z = (np.asarray(p, float) - f)
        a, t = self.angle.get_value(), self.tilt.get_value()
        x, z = x * np.cos(a) + z * np.sin(a), -x * np.sin(a) + z * np.cos(a)
        y, z = y * np.cos(t) - z * np.sin(t), y * np.sin(t) + z * np.cos(t)
        s = self.scale_ * self.zoom.get_value()
        return self.center_ + np.array([s * x, s * y, 0.0]), z

    def _dot_updater(self, i):
        def upd(d):
            pos, depth = self.project(self.xyz[i])
            k = float(np.clip(1 + 0.35 * depth, 0.55, 1.5))
            d.set(width=2 * self.radius * k).move_to(pos)
            d.set_opacity(float(np.clip(0.55 + 0.45 * depth, 0.3, 1.0)))
        return upd

    def _label_updater(self, i, buff):
        def upd(m):
            pos, _ = self.project(self.xyz[i])
            m.next_to(pos, UR, buff=buff)
        return upd

    def look_at(self, p, zoom: float) -> list:
        """Animations that bring data point ``p`` to the centre at magnification ``zoom``."""
        return [t.animate.set_value(float(v)) for t, v in zip(self.focus, p)] + [self.zoom.animate.set_value(zoom)]


# ---------------------------------------------------------------------------
# Contour lines
# ---------------------------------------------------------------------------
def contour_segments(xs, ys, Z, level):
    """Marching squares: the segments where the grid values Z[i, j] (at ys[i], xs[j]) cross ``level``."""
    segs = []
    for i in range(len(ys) - 1):
        for j in range(len(xs) - 1):
            c = [(xs[j], ys[i], Z[i, j]), (xs[j + 1], ys[i], Z[i, j + 1]), (xs[j + 1], ys[i + 1], Z[i + 1, j + 1]),
                 (xs[j], ys[i + 1], Z[i + 1, j])]
            pts = []
            for k in range(4):
                (x1, y1, z1), (x2, y2, z2) = c[k], c[(k + 1) % 4]
                if (z1 - level) * (z2 - level) < 0:
                    t = (level - z1) / (z2 - z1)
                    pts.append((x1 + t * (x2 - x1), y1 + t * (y2 - y1)))
            if len(pts) == 2:
                segs.append(pts)
            elif len(pts) == 4:
                segs += [pts[:2], pts[2:]]
    return segs


def contour_lines(ax: Axes, f, x_range, y_range, levels, n=(160, 120), colors=(SURFACE_COLORS[1], SURFACE_COLORS[3]),
                  stroke_width=2.0) -> VGroup:
    """The level sets of f(x, y) on ``ax``: one path per level, colored from low to high."""
    xs, ys = np.linspace(*x_range, n[0] + 1), np.linspace(*y_range, n[1] + 1)
    Z = np.array([[f(x, y) for x in xs] for y in ys])
    out = VGroup()
    lo, hi = min(levels), max(levels)
    for lv in levels:
        col = interpolate_color(ManimColor(colors[0]), ManimColor(colors[1]), (lv - lo) / max(hi - lo, 1e-9))
        path = VMobject(color=col, stroke_width=stroke_width)
        for a, b in contour_segments(xs, ys, Z, lv):
            path.start_new_path(ax.c2p(*a))
            path.add_line_to(ax.c2p(*b))
        out.add(path)
    return out
