from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import GRAD, VALUE


def s(p):
    return math.log2(1 / p)


def ds(p):
    return -1 / (p * math.log(2))


class Derivative(VoiceoverScene):
    def construct(self):
        self.card()
        self.zoom()
        self.tangent()
        self.rules()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(1, r"The derivative", r"How fast does an output change?", part=3)
        with self.voiceover("Chapter one. The derivative."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def axes(self):
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 6, 1], x_length=6.0, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-3.4, -0.3, 0])
        xs = np.concatenate([np.geomspace(2 ** -6, 0.1, 80), np.linspace(0.1, 1, 120)])
        curve = ax.plot_line_graph(xs, [s(x) for x in xs], add_vertex_dots=False, line_color=C.SURPRISE, stroke_width=4)
        lab = label(r"Part 1's surprise: \ $s(p) = \log_2 \frac1p$", font_size=28, color=C.SURPRISE).next_to(ax, UP, buff=0.2)
        return ax, curve, lab

    def zoom(self):
        ax, curve, lab = self.axes()
        p0 = 0.25
        P = ax.c2p(p0, s(p0))
        m = ValueTracker(1.0)
        R = 2.1
        centre = np.array([3.6, -0.3, 0])
        lens = Circle(radius=R, color=WHITE, stroke_width=3).move_to(centre)
        spot = always_redraw(lambda: Circle(radius=max(R / m.get_value() * 0.45, 0.04), color=WHITE, stroke_width=2).move_to(P))
        rays = always_redraw(lambda: VGroup(*[Line(P + spot_r(m, R) * d, centre + R * d, color=GREY_B, stroke_width=1.2,
                                                   stroke_opacity=0.6) for d in (UP, DOWN)]))
        sx, sy = 6.0 / 1.0, 4.6 / 6.0  # the main axes' units per x and per y

        def inset():
            k = m.get_value()
            half = R / (k * sx) * 0.98  # the stretch of p that fills the lens
            ts = np.linspace(max(p0 - half, 1e-3), p0 + half, 80)
            pts = [centre + k * np.array([(t - p0) * sx, (s(t) - s(p0)) * sy, 0]) for t in ts]
            pts = [q for q in pts if np.linalg.norm(q - centre) < R * 0.98]
            return VMobject(color=C.SURPRISE, stroke_width=5).set_points_smoothly(pts) if len(pts) > 3 else VGroup()

        inner = always_redraw(inset)
        dot = glow_dot(centre, color=WHITE, radius=0.07, layers=3)
        mag = always_redraw(lambda: MathTex(rf"\times {m.get_value():.0f}", font_size=36, color=GREY_A)
                            .next_to(lens, UP, buff=0.15))
        tan_dir = np.array([sx, ds(p0) * sy, 0])
        tan_dir /= np.linalg.norm(tan_dir)
        straight = DashedLine(centre - 1.9 * tan_dir, centre + 1.9 * tan_dir, color=GRAD, stroke_width=3)
        slope = label(rf"slope: \ $s'(\tfrac14) = {ds(p0):.2f}$ bits per unit of $p$", font_size=28, color=GRAD)
        slope.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Zoom in on a smooth curve, closer and closer, <bookmark mark='a'/> and it starts to look like a straight "
            "line. <bookmark mark='b'/> The slope of that line is the derivative: how much the output changes, for "
            "each small change of the input."
        ) as vo:
            self.play(Create(ax), Create(curve), FadeIn(lab))
            self.play(Create(lens), FadeIn(spot), FadeIn(rays), FadeIn(inner), FadeIn(dot), FadeIn(mag))
            vo.wait_until("a")
            self.play(m.animate.set_value(60.0), run_time=4.0, rate_func=smooth)
            vo.wait_until("b")
            self.play(Create(straight), FadeIn(slope))
        for x in (spot, rays, inner, mag):
            x.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tangent(self):
        ax, curve, lab = self.axes()
        p0 = 0.25
        h = ValueTracker(0.45)

        def secant():
            a, b = p0, p0 + h.get_value()
            k = (s(b) - s(a)) / (b - a)
            x0, x1 = 0.05, 0.95
            return VGroup(Line(ax.c2p(x0, s(a) + k * (x0 - a)), ax.c2p(x1, s(a) + k * (x1 - a)), color=GRAD, stroke_width=3),
                          Dot(ax.c2p(b, s(b)), radius=0.06, color=GRAD))

        sec = always_redraw(secant)
        d0 = glow_dot(ax.c2p(p0, s(p0)), color=WHITE, radius=0.07, layers=3)
        hl = always_redraw(lambda: MathTex(rf"h = {h.get_value():.3f}", font_size=34, color=GRAD).move_to([3.4, -2.6, 0]))
        colors = {r"f(x + h)": VALUE, r"f(x)": VALUE, r"f'(x)": GRAD, "h": GRAD}
        f = cmath(r"f(x + h)", r"\approx", r"f(x)", "+", r"f'(x)", r"\,", "h", colors=colors, font_size=52)
        f.move_to([3.4, 1.4, 0])
        what = label(r"the best straight-line description \\ of a function, near one point", font_size=28,
                     color=GREY_A).next_to(f, DOWN, buff=0.4)
        with self.voiceover(
            "Written down: f at x plus a small step h, is about f of x, plus the derivative times h. "
            "<bookmark mark='a'/> The smaller the step, the better the guess. A derivative is the best straight-line "
            "description of a function, near one point."
        ) as vo:
            self.play(Create(ax), Create(curve), FadeIn(lab), FadeIn(d0))
            self.add(sec, hl)
            self.play(Write(f))
            vo.wait_until("a")
            self.play(h.animate.set_value(0.004), run_time=3.0, rate_func=smooth)
            self.play(FadeIn(what))
        sec.clear_updaters()
        hl.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rules(self):
        r1 = MathTex(r"\frac{d}{dx} e^{x} = e^{x}", font_size=42).move_to([-5.0, 2.5, 0])
        r2 = MathTex(r"\frac{d}{dx} \ln x = \frac{1}{x}", font_size=42).move_to([-1.7, 2.5, 0])
        colors = {r"f'(g(x))": GRAD, r"g'(x)": C.BITS}
        r3 = cmath(r"\frac{d}{dx} f(g(x))", "=", r"f'(g(x))", r"\,", r"g'(x)", colors=colors, font_size=42).move_to([3.6, 2.5, 0])
        if r3.get_right()[0] > 6.9:
            r3.shift(LEFT * (r3.get_right()[0] - 6.9))
        # the chain rule as stretching: three number lines, a small interval carried along
        x0, g = 1.0, lambda x: x * x
        f = math.exp
        ys = [0.9, -0.6, -2.1]
        lines = VGroup(*[NumberLine(x_range=[0, 3, 1], length=9.0, color=GREY_C, include_numbers=False).move_to([0.4, y, 0])
                         for y in ys])
        names = VGroup(*[MathTex(t, font_size=36).next_to(lines[k], LEFT, buff=0.3) for k, t in
                         enumerate((r"x", r"g(x) = x^2", r"f(g(x)) = e^{x^2}"))])
        dx = 0.12
        ivs = []
        for k, (lo, hi) in enumerate([(x0, x0 + dx), (g(x0), g(x0 + dx)), (f(g(x0)) / 6, f(g(x0 + dx)) / 6)]):
            ivs.append(Line(lines[k].n2p(lo), lines[k].n2p(hi), color=[VALUE, C.BITS, GRAD][k], stroke_width=12))
        stretch = VGroup(MathTex(r"\times g'(1) = 2", font_size=34, color=C.BITS).move_to([5.2, 0.15, 0]),
                         MathTex(r"\times f'(1) = e", font_size=34, color=GRAD).move_to([5.2, -1.35, 0]))
        scale_note = label(r"(the last line is drawn $6$ times smaller)", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.3)
        notation = label(r"$f'$: \ the slope of $f$; \quad $f(g(x))$: \ do $g$ first, then $f$", font_size=28,
                         color=GREY_A).move_to([0.4, 1.7, 0])
        conn = VGroup(*[Line(ivs[k].get_center(), ivs[k + 1].get_center(), color=GREY_B, stroke_width=1.5,
                             stroke_opacity=0.6) for k in range(2)])
        with self.voiceover(
            "A few derivatives come up over and over. <bookmark mark='a'/> The exponential is its own derivative. "
            "<bookmark mark='b'/> The logarithm's derivative is one over x. That's why the surprise climbs so steeply "
            "as p shrinks. <bookmark mark='c'/> And the chain rule, for a composition: f of g of x means do g "
            "first, then f. Writing f prime for the slope of f, the derivative of f of g of x is f prime at g of x, "
            "times g prime at x. Change flows through a composition, multiplying as it goes."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(r1))
            vo.wait_until("b")
            self.play(Write(r2))
            vo.wait_until("c")
            self.play(Write(r3))
            self.play(FadeIn(notation))
            self.play(Create(lines), FadeIn(names), FadeIn(scale_note))
            self.play(Create(ivs[0]))
            self.play(TransformFromCopy(ivs[0], ivs[1]), Create(conn[0]), FadeIn(stretch[0]))
            self.play(TransformFromCopy(ivs[1], ivs[2]), Create(conn[1]), FadeIn(stretch[1]))
        self.wait(0.3)
        self.clear_scene()


def spot_r(m, R):
    return max(R / m.get_value() * 0.45, 0.04)
