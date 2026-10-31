from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import GRAD, HESS, HIST, PART, VALUE, load, log_axes


def s(p):
    return math.log2(1 / p)


def ds(p):
    return -1 / (p * math.log(2))


class Derivative(VoiceoverScene):
    def construct(self):
        self.card()
        self.zoom()
        self.tangent()
        self.best()
        self.derive()
        self.rules()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(1, r"The derivative", r"What is the best straight line through a curve?", part=PART)
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
        h = ValueTracker(0.30)
        k = ds(p0)
        # The derivative fixes one tangent. A secant through the exact new
        # curve value would hide the very approximation error shown here.
        crossings = [p0 + (y - s(p0)) / k for y in (0, 6)]
        x0, x1 = max(0.05, min(crossings)), min(0.95, max(crossings))
        tangent = Line(ax.c2p(x0, s(p0) + k * (x0 - p0)),
                       ax.c2p(x1, s(p0) + k * (x1 - p0)), color=GRAD, stroke_width=3)

        def samples():
            b = p0 + h.get_value()
            actual = ax.c2p(b, s(b))
            predicted = ax.c2p(b, s(p0) + k * h.get_value())
            return VGroup(Line(predicted, actual, color=GREY_A, stroke_width=3),
                          Dot(actual, radius=0.06, color=C.SURPRISE),
                          Dot(predicted, radius=0.06, color=GRAD))

        points = always_redraw(samples)
        d0 = glow_dot(ax.c2p(p0, s(p0)), color=WHITE, radius=0.07, layers=3)
        hl = always_redraw(lambda: MathTex(rf"h = {h.get_value():.3f}", font_size=34, color=GRAD).move_to([3.4, -2.6, 0]))
        colors = {r"f(x + h)": VALUE, r"f(x)": VALUE, r"f'(x)": GRAD, "h": GRAD}
        f = cmath(r"f(x + h)", r"\approx", r"f(x)", "+", r"f'(x)", r"\,", "h", colors=colors, font_size=52)
        f.move_to([3.4, 1.4, 0])
        what = label(r"the best straight-line description \\ of a function, near one point", font_size=28,
                     color=GREY_A).next_to(f, DOWN, buff=0.4)
        legend = VGroup(label(r"curve value $f(x+h)$", font_size=24, color=C.SURPRISE),
                        label(r"linear prediction $f(x)+f'(x)h$", font_size=24, color=GRAD),
                        label(r"gap: approximation error", font_size=22, color=GREY_A))
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.4, -1.1, 0])
        with self.voiceover(
            "Written down: f at x plus a small step h, is about f of x, plus the derivative times h. "
            "<bookmark mark='a'/> The smaller the step, the better the guess. A derivative is the best straight-line "
            "description of a function, near one point."
        ) as vo:
            self.play(Create(ax), Create(curve), FadeIn(lab), FadeIn(d0))
            self.add(tangent, points, hl, legend)
            self.play(Write(f))
            vo.wait_until("a")
            self.play(h.animate.set_value(0.004), run_time=3.0, rate_func=smooth)
            self.play(FadeIn(what))
        points.clear_updaters()
        hl.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def best(self):
        d = load("linapprox")
        hs, err, bad = np.asarray(d["hs"]), np.asarray(d["err"]), np.asarray(d["err_bad"])
        assert abs(d["slope"] - 2) < 0.05 and abs(d["slope_bad"] - 1) < 0.05
        card = definition_card(
            r"the derivative",
            r"$f$ is differentiable at $x$ if there is one number $f'(x)$ with "
            r"$f(x + h) = f(x) + f'(x)\,h + r(h)$, where the error $r(h)$ shrinks faster than $h$: "
            r"$r(h)/h \to 0$ as $h \to 0$.", width=6.2, font_size=25).to_corner(UL, buff=0.35)
        hist = history_card(r"1684", r"Gottfried Leibniz, \textit{Nova Methodus}",
                            r"the first calculus in print, with $dx$ and $dy$; \ Isaac Newton's fluxions date from "
                            r"the 1660s", width=6.2, font_size=22).to_corner(DL, buff=0.35)
        g = log_axes((-4, -0.8), (-8, 0), x_length=5.4, y_length=4.4, xlabel=r"the step $h$",
                     ylabel=r"error of the straight-line guess, \ $|f(x+h) - f(x) - s\,h|$", center=[3.6, -0.2, 0],
                     xticks=[-4, -3, -2, -1], yticks=[-8, -6, -4, -2, 0])
        ax = g.ax
        c_best = curve(ax, np.log10(hs), np.log10(err), GRAD, 4)
        c_bad = curve(ax, np.log10(hs), np.log10(bad), C.SURPRISE, 3)
        l_best = label(rf"$s = f'(x)$: \ slope ${d['slope']:.2f}$", font_size=22, color=GRAD)
        l_best.next_to(ax.c2p(-3.2, np.log10(err[8])), DR, buff=0.1)
        l_bad = label(rf"$s$ off by $10\%$: \ slope ${d['slope_bad']:.2f}$", font_size=22, color=C.SURPRISE)
        # Keep the annotation inside the plot, clear of both the y-axis and
        # the measured red curve instead of hanging it across the axis.
        l_bad.move_to(ax.c2p(-3.8, -1.8), aligned_edge=UL)
        tag = note(r"computed: \ Part 1's surprise at $p = \tfrac14$").next_to(g, DOWN, buff=0.1).align_to(g, RIGHT)
        with self.voiceover(
            "The idea is Leibniz's, in print in 1684, and Newton's, who had worked it out in the 1660s and called it "
            "fluxions. <bookmark mark='a'/> Here is the precise version. A function is differentiable at x if one "
            "number, the derivative, makes the straight-line guess so good that its error shrinks faster than the "
            "step itself. <bookmark mark='b'/> Measure it, for Part 1's surprise curve. On these logarithmic axes, the "
            f"error with the true slope falls with a slope of {d['slope']:.2f}: like h squared. <bookmark mark='c'/> "
            f"Use a slope just ten percent off, and the error falls only like h, a slope of {d['slope_bad']:.2f}. "
            "Exactly one line wins as the step shrinks. That is what best means."
        ) as vo:
            self.play(FadeIn(hist, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(g), FadeIn(tag))
            self.play(Create(c_best), FadeIn(l_best), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(c_bad), FadeIn(l_bad), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        d = load("linapprox")
        col = {r"s(p)": C.SURPRISE, r"s'(p)": GRAD}
        rows = [
            cmath(r"s(p + h) - s(p)", r"=", r"-\tfrac{1}{\ln 2}\,\big(\ln(p + h) - \ln p\big)", font_size=38),
            cmath(r"s(p + h) - s(p)", r"=", r"-\tfrac{1}{\ln 2}\,\ln\!\big(1 + \tfrac{h}{p}\big)", font_size=38),
            cmath(r"s(p + h) - s(p)", r"=", r"-\tfrac{1}{\ln 2}\,\tfrac{h}{p} + o(h)", font_size=38),
            cmath(r"s'(p)", r"=", r"-\frac{1}{p \ln 2}", font_size=42, colors=col),
            cmath(r"s'(\tfrac14)", r"=", rf"-\frac{{4}}{{\ln 2}} = {d['d1']:.2f}", font_size=42, colors={r"s'(\tfrac14)": GRAD}),
        ]
        whys = [why(r"$s(p) = \log_2 \tfrac1p = -\ln p / \ln 2$"), why(r"a difference of logs is a log of a ratio"),
                why(r"$\ln(1 + u) = u + o(u)$: \ the log's own tangent at $1$"),
                why(r"read off the number in front of $h$"), why(r"the slope the lens showed")]
        step = ladder(self, rows, whys, keep=5, top=2.9, x=-1.0, buff=0.45, edge=6.9)
        head = label(r"the derivative of the surprise, \ from the definition", font_size=26, color=GREY_A)
        head.to_corner(UL, buff=0.3)
        with self.voiceover(
            "Let's use the definition once, on the surprise, log base two of one over p. <bookmark mark='a'/> The "
            "change over a step h is a difference of logarithms, <bookmark mark='b'/> which is the logarithm of a "
            "ratio. <bookmark mark='c'/> Near one, the logarithm is its own tangent: log of one plus u is u, plus "
            "an error smaller than u. <bookmark mark='d'/> So the number in front of h is minus one over p log "
            f"two. <bookmark mark='e'/> At a quarter, that's {d['d1']:.2f} bits per unit of p: the slope the lens "
            "showed."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rules(self):
        r1 = MathTex(r"\frac{d}{dx} e^{x}", "=", r"e^{x}", font_size=42).move_to([-5.0, 2.5, 0])
        r2 = MathTex(r"\frac{d}{dx} \ln x", "=", r"\frac{1}{x}", font_size=42).move_to([-1.7, 2.5, 0])
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
        stretch = VGroup(MathTex(r"g'(1) = 2", font_size=34, color=C.BITS).move_to([5.2, 0.15, 0]),
                         MathTex(r"f'(1) = e", font_size=34, color=GRAD).move_to([5.2, -1.35, 0]))
        # The pictured intervals are finite, so their secant stretches are not
        # exactly the derivatives 2 and e. The displayed factors are limits.
        local = label(r"local stretch factors as the step $\to 0$", font_size=22, color=GREY_A)
        local.move_to([3.4, -2.85, 0])
        scale_note = label(r"finite intervals shown; \ the last line is drawn $6$ times smaller", font_size=22,
                           color=GREY_B).to_edge(DOWN, buff=0.3)
        notation = label(r"$f'$: \ the slope of $f$; \quad $f(g(x))$: \ do $g$ first, then $f$", font_size=28,
                         color=GREY_A).move_to([0.4, 1.7, 0])
        conn = VGroup(*[Line(ivs[k].get_center(), ivs[k + 1].get_center(), color=GREY_B, stroke_width=1.5,
                             stroke_opacity=0.6) for k in range(2)])
        # the questions first: each left-hand side, waiting for its answer
        qs = [MathTex(r"?", font_size=46, color=GREY_B).next_to(r[1], RIGHT, buff=0.25) for r in (r1, r2, r3)]
        with self.voiceover(
            "A few derivatives come up over and over. <bookmark mark='a'/> The exponential is its own derivative. "
            "<bookmark mark='b'/> The logarithm's derivative is one over x. That's why the surprise climbs so steeply "
            "as p shrinks. <bookmark mark='c'/> And the chain rule, for a composition: f of g of x means do g "
            "first, then f. Writing f prime for the slope of f, the derivative of f of g of x is f prime at g of x, "
            "times g prime at x. Change flows through a composition, multiplying as it goes."
        ) as vo:
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r[0]), FadeIn(r[1]), FadeIn(q)) for r, q in zip((r1, r2, r3), qs)],
                                  lag_ratio=0.3), run_time=1.5)
            for r, q, mark in zip((r1, r2, r3), qs, "abc"):
                vo.wait_until(mark)
                self.play(FadeOut(q, scale=0.5), Write(VGroup(*r[2:])))
            self.play(FadeIn(notation))
            self.play(Create(lines), FadeIn(names), FadeIn(scale_note), FadeIn(local))
            self.play(Create(ivs[0]))
            self.play(TransformFromCopy(ivs[0], ivs[1]), Create(conn[0]), FadeIn(stretch[0]))
            self.play(TransformFromCopy(ivs[1], ivs[2]), Create(conn[1]), FadeIn(stretch[1]))
        self.wait(0.3)
        self.clear_scene()


def spot_r(m, R):
    return max(R / m.get_value() * 0.45, 0.04)
