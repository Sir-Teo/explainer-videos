from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.stochastic.common import decimate, hero, label, load, mtex, note, num_table, path_curve, tw_axes
from videos.stochastic.compute import ZOOM_T


def smooth_f(t):
    return 0.55 * np.sin(2 * np.pi * 0.9 * t) + 0.45 * t + 0.22 * np.cos(2 * np.pi * 2.3 * t)


def clipped(points: np.ndarray, x0, x1, y0, y1, color, stroke_width) -> VMobject:
    """A polyline cut wherever it leaves the box (no flat lines hugging the border)."""
    m = VMobject(stroke_color=color, stroke_width=stroke_width)
    inside = (points[:, 1] >= y0) & (points[:, 1] <= y1) & (points[:, 0] >= x0) & (points[:, 0] <= x1)
    if not inside.any():
        m.set_points_as_corners([points[0], points[0]])
        m.set_stroke(opacity=0)
        return m
    # runs of consecutive inside points, each extended by one neighbor clamped to the border
    idx = np.flatnonzero(inside)
    breaks = np.flatnonzero(np.diff(idx) > 1)
    starts = np.concatenate([[idx[0]], idx[breaks + 1]])
    ends = np.concatenate([idx[breaks], [idx[-1]]])
    first = True
    for a, b in zip(starts, ends):
        a2, b2 = max(a - 1, 0), min(b + 1, len(points) - 1)
        run = points[a2:b2 + 1].copy()
        run[:, 1] = np.clip(run[:, 1], y0, y1)
        if len(run) < 2:
            continue
        if first:
            m.set_points_as_corners(run)
            first = False
        else:
            m.start_new_path(run[0])
            m.add_points_as_corners(run[1:])
    return m


class ZoomView(VGroup):
    """A framed window onto a curve, zooming about the point (t0, y0).

    At zoom level z the window spans w0 / tx**z in time and h0 / ty**z in value.  The zoom point sits ``yc`` of
    the window height below the window's center (a fraction, so it stays put on screen as the zoom runs)."""

    def __init__(self, sample, t0, y0, w0, h0, tx, ty, z: ValueTracker, width=6.0, height=4.4, color=C.BROWNIAN,
                 stroke_width=2.4, yc=0.0):
        super().__init__()
        self.frame = Rectangle(width=width, height=height, stroke_color=GREY_C, stroke_width=2)
        self.add(self.frame)

        def draw():
            zz = z.get_value()
            w, h = w0 / tx**zz, h0 / ty**zz
            ts, ys = sample(t0 - w / 2, t0 + w / 2)
            c = self.frame.get_center()
            X = c[0] + (ts - t0) / w * width
            Y = c[1] + (ys - y0) / h * height - yc * height
            pts = np.stack([X, Y, np.zeros_like(X)], axis=1)
            return clipped(pts, c[0] - width / 2, c[0] + width / 2, c[1] - height / 2, c[1] + height / 2, color,
                           stroke_width)

        self.curve = always_redraw(draw)
        self.dot = always_redraw(lambda: Dot(self.frame.get_center() + DOWN * yc * height, radius=0.06, color=WHITE))
        self.add(self.curve, self.dot)


def brownian_sampler():
    W = hero()
    N = len(W) - 1

    def sample(a, b):
        i0, i1 = max(0, int(np.floor(a * N))), min(N, int(np.ceil(b * N)))
        ys = W[i0:i1 + 1]
        ts = np.arange(i0, i1 + 1) / N
        return decimate(ts, ys, 1800)

    return sample


def smooth_sampler(a, b):
    ts = np.linspace(a, b, 400)
    return ts, smooth_f(ts)


class Roughness(VoiceoverScene):
    def construct(self):
        self.smooth_zoom()
        self.brownian_equal_zoom()
        self.self_similar()
        self.secants()
        self.length()

    def zoom_counter(self, z: ValueTracker, base: int, tex_unit: str, color=GREY_A) -> VGroup:
        lbl = MathTex(tex_unit, font_size=32, color=color)
        n = Integer(1, font_size=32, color=color)
        n.add_updater(lambda m: m.set_value(int(round(base ** z.get_value()))))
        g = VGroup(lbl, n).arrange(RIGHT, buff=0.12)
        return g

    # ------------------------------------------------------------------
    def smooth_zoom(self):
        t0 = 0.43
        y0 = float(smooth_f(t0))
        z = ValueTracker(0.0)
        view = ZoomView(smooth_sampler, t0, y0, 1.0, 2.2, 4, 4, z, width=9.0, height=5.2, color=C.DRIFT)
        view.move_to(DOWN * 0.45)
        title = label(r"A smooth curve: zoom in by $4\times$ in both directions", font_size=34).to_edge(UP, buff=0.4)
        counter = self.zoom_counter(z, 4, r"\text{zoom} \times").next_to(view.frame, DOWN, buff=0.2)
        slope = 2 * np.pi * 0.9 * 0.55 * np.cos(2 * np.pi * 0.9 * t0) + 0.45 - 0.22 * 2 * np.pi * 2.3 * np.sin(2 * np.pi * 2.3 * t0)
        c = view.frame.get_center()
        # at full zoom the window is 1/4^4 wide and tall in data units: the tangent's screen slope is slope * (9 / 5.2) * (2.2 / 1.0)
        k = slope * (5.2 / 2.2) / (9.0 / 1.0)
        tangent = DashedLine(c + LEFT * 4.5 + DOWN * 4.5 * k, c + RIGHT * 4.5 + UP * 4.5 * k, color=WHITE, stroke_width=2,
                             dash_length=0.12)
        tl = label(r"its tangent line", font_size=28).next_to(tangent.get_end(), DOWN, buff=0.2).shift(LEFT * 0.6)
        with self.voiceover(
            "Brownian paths are continuous, but they're strange in another way. <bookmark mark='s'/> Here's an ordinary "
            "smooth curve. Let's zoom in on one point, by the same factor in both directions. <bookmark mark='z'/> Four "
            "times, sixteen, sixty-four, two hundred and fifty-six. <bookmark mark='l'/> The curve straightens out, until "
            "it's indistinguishable from a line: its tangent line. That's what having a derivative means: up close, the "
            "curve is a line."
        ) as vo:
            self.play(FadeIn(title), Create(view.frame))
            vo.wait_until("s")
            self.add(view.curve, view.dot, counter)
            vo.wait_until("z")
            self.play(z.animate.set_value(4.0), run_time=vo.until("l"), rate_func=linear)
            self.play(Create(tangent), FadeIn(tl))
        self.wait(0.3)
        self.play(FadeOut(VGroup(tangent, tl, title, counter)), FadeOut(view))
        view.curve.clear_updaters()

    # ------------------------------------------------------------------
    def brownian_equal_zoom(self):
        W = hero()
        t0 = ZOOM_T
        y0 = float(W[int(round(t0 * (len(W) - 1)))])
        z = ValueTracker(0.0)
        view = ZoomView(brownian_sampler(), t0, y0, 0.7, 2.5, 4, 4, z, width=9.0, height=5.2, yc=0.24)
        view.move_to(DOWN * 0.45)
        title = label(r"Brownian motion: the same zoom, $4\times$ in both directions", font_size=34).to_edge(UP, buff=0.4)
        counter = self.zoom_counter(z, 4, r"\text{zoom} \times").next_to(view.frame, DOWN, buff=0.2)
        with self.voiceover(
            "Now do the same to our Brownian path, zooming four times in both directions, again and again. "
            "<bookmark mark='z'/> Instead of straightening out, it gets steeper and wilder: the wiggles shoot off the top "
            "and bottom of the window. <bookmark mark='n'/> There is no tangent line to find."
        ) as vo:
            self.play(FadeIn(title), Create(view.frame))
            self.add(view.curve, view.dot, counter)
            vo.wait_until("z")
            self.play(z.animate.set_value(3.0), run_time=vo.until("n") + 0.6, rate_func=linear)
        self.wait(0.3)
        self.play(FadeOut(VGroup(title, counter)), FadeOut(view))
        view.curve.clear_updaters()

    # ------------------------------------------------------------------
    def self_similar(self):
        W = hero()
        t0 = ZOOM_T
        y0 = float(W[int(round(t0 * (len(W) - 1)))])
        z = ValueTracker(0.0)
        view = ZoomView(brownian_sampler(), t0, y0, 0.7, 2.5, 4, 2, z, width=9.0, height=5.0, yc=0.24)
        view.move_to(DOWN * 0.55 + LEFT * 1.6)
        title = label(r"zoom $4\times$ in time, but only $2\times$ in space", font_size=34).to_edge(UP, buff=0.4)
        ct = self.zoom_counter(z, 4, r"\text{time} \times", color=C.CLOCK)
        cs = self.zoom_counter(z, 2, r"\text{space} \times", color=C.BROWNIAN)
        counters = VGroup(ct, cs).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(view.frame, RIGHT, buff=0.45)
        counters.shift(UP * 1.4)
        law = MathTex(r"W_{ct}", r"\;\overset{d}{=}\;", r"\sqrt{c}\; W_t", font_size=44)
        law[0].set_color(C.BROWNIAN)
        law[2].set_color(C.BROWNIAN)
        law.next_to(counters, DOWN, buff=0.9).align_to(counters, LEFT)
        law_l = label(r"same distribution", font_size=24, color=GREY_B).next_to(law, DOWN, buff=0.15)
        pts = note(r"one path, $4{,}194{,}304$ simulated points").next_to(view.frame, DOWN, buff=0.15)

        with self.voiceover(
            "Here's the zoom that does work. <bookmark mark='z'/> Every time you stretch time by four, stretch space by "
            "only two: the square root of four. <bookmark mark='l'/> Now every level looks like the one before: just as "
            "rough, just as wild, statistically the same picture. These are all one path, simulated at four million "
            "points, and we could keep going forever."
        ) as vo:
            self.play(FadeIn(title), Create(view.frame), FadeIn(pts))
            self.add(view.curve, view.dot)
            vo.wait_until("z")
            self.play(FadeIn(counters))
            self.play(z.animate.set_value(5.0), run_time=vo.remaining() + 2.0, rate_func=linear)
        with self.voiceover(
            "In symbols: Brownian motion with time sped up by a factor c has the same distribution as the original, "
            "scaled up by root c. <bookmark mark='f'/> It's a fractal. And that same square root again: zooming in never "
            "reveals anything smooth."
        ) as vo:
            self.play(Write(law), FadeIn(law_l))
            vo.wait_until("f")
            self.play(z.animate.set_value(0.0), run_time=vo.remaining() + 0.5, rate_func=smooth)
        self.play(FadeOut(VGroup(title, counters, law, law_l, pts)), FadeOut(view))
        view.curve.clear_updaters()
        for c in (ct, cs):
            c[1].clear_updaters()

    # ------------------------------------------------------------------
    def secants(self):
        h = load("hero")
        hs, slopes = h["hs"], h["slopes"]
        W = hero()
        N = len(W) - 1
        t0 = ZOOM_T
        i0 = int(round(t0 * N))
        ax = tw_axes(x_length=6.0, y_range=(-1.0, 1.6, 0.5), y_length=4.0).to_edge(LEFT, buff=0.5).shift(DOWN * 0.6)
        path = path_curve(ax, W, stroke_width=2).set_stroke(opacity=0.8)
        p0 = ax.c2p(t0, W[i0])
        secs = VGroup()
        for hh in hs[:3]:
            j = i0 + int(hh * N)
            p1 = ax.c2p(t0 + hh, W[j])
            d = (p1 - p0) / np.linalg.norm(p1 - p0)
            secs.add(VGroup(Line(p0 - d * 0.6, p1 + d * 0.6, color=C.QV, stroke_width=2.5),
                            Dot(p1, radius=0.05, color=C.QV)))
        dot0 = Dot(p0, radius=0.06, color=WHITE)

        deriv = VGroup(
            MathTex(r"\frac{W_{t+h} - W_t}{h}", r"\;\sim\;", r"\frac{\mathcal N(0,\, h)}{h}", font_size=38),
            MathTex(r"=", r"\;\mathcal N\!\Big(0,\, \frac{1}{h}\Big)", font_size=38),
        )
        deriv[0][0].set_color(C.QV)
        deriv.arrange(RIGHT, buff=0.15).to_edge(UP, buff=0.5).shift(RIGHT * 2.6)
        sd = label(r"typical slope $\approx 1/\sqrt{h} \;\to\; \infty$", font_size=30, color=C.QV).next_to(deriv, DOWN, buff=0.3)
        frac = lambda k: rf"1/{4**k:,}".replace(",", "{,}")
        tab = num_table([r"h", r"\text{secant slope}", r"1/\sqrt h"],
                        [[frac(k + 1), f"{slopes[k]:.1f}".replace("-", "{-}"), f"{2**(k + 1)}"] for k in range(7)],
                        font_size=28, col_colors=[C.CLOCK, C.QV, GREY_B])
        tab.next_to(sd, DOWN, buff=0.35).shift(RIGHT * 0.9)

        with self.voiceover(
            "This kills the derivative for good. <bookmark mark='s'/> A derivative is the limit of secant slopes: the "
            "change in W over a short time h, divided by h. <bookmark mark='d'/> But that change is a bell curve with "
            "variance h, <bookmark mark='e'/> so the slope is a bell curve with variance one over h. "
            "<bookmark mark='b'/> Its typical size is one over root h, and as h shrinks, it blows up."
        ) as vo:
            self.play(Create(ax), Create(path), FadeIn(dot0))
            vo.wait_until("s")
            self.play(LaggedStart(*[Create(s) for s in secs], lag_ratio=0.5), run_time=2)
            vo.wait_until("d")
            self.play(Write(deriv[0]))
            vo.wait_until("e")
            self.play(Write(deriv[1]))
            vo.wait_until("b")
            self.play(FadeIn(sd))
        with self.voiceover(
            "On our path, at the point we zoomed into: <bookmark mark='t'/> each time h shrinks by four, the slope "
            "roughly doubles, from about four, to eight, to over two hundred, right along with one over root h. "
            "Brownian motion is continuous everywhere, and differentiable nowhere."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(tab.header), Create(tab.rule))
            self.play(LaggedStart(*[FadeIn(r) for r in tab.rows], lag_ratio=0.3), run_time=vo.remaining())
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def length(self):
        h = load("hero")
        ns, tv = h["n"], h["tv"]
        rows = [(n, v) for n, v in zip(ns, tv) if n in (16, 256, 4096, 65536, 4194304)]
        ax = tw_axes(x_length=6.2, y_range=(-1.0, 1.6, 0.5), y_length=4.0).to_edge(LEFT, buff=0.5).shift(DOWN * 0.7)
        W = hero()

        def zigzag(n):
            w = hero(n)
            ts = np.linspace(0, 1, n + 1)
            return VGroup(*[Line(ax.c2p(ts[i], w[i]), ax.c2p(ts[i + 1], w[i + 1]),
                                 color=C.BROWNIAN, stroke_width=2.5 if n <= 64 else 1.6) for i in range(n)])

        tvf = MathTex(r"\sum_i \big|W_{t_{i+1}} - W_{t_i}\big|", font_size=40).to_edge(UP, buff=0.5).shift(RIGHT * 2.8)
        tvl = label(r"total distance traveled up and down", font_size=26, color=GREY_A).next_to(tvf, DOWN, buff=0.15)
        exp = [np.sqrt(2 * n / np.pi) for n, _ in rows]
        tab = num_table([r"n \text{ steps}", r"\text{this path}", r"\sqrt{2n/\pi}"],
                        [[f"{n:,}".replace(",", "{,}"), f"{v:,.1f}".replace(",", "{,}"), f"{e:,.1f}".replace(",", "{,}")]
                         for (n, v), e in zip(rows, exp)],
                        font_size=30, col_colors=[C.CLOCK, C.BROWNIAN, GREY_B])
        tab.next_to(tvl, DOWN, buff=0.4).shift(RIGHT * 0.7)
        z16 = zigzag(16)
        z256 = zigzag(256)
        full = path_curve(ax, W, stroke_width=1.6)
        tv16, tv256, tv4k, tv65k, tv4m = [v for _, v in rows]
        with self.voiceover(
            "And there's an even stranger consequence. <bookmark mark='a'/> Walk along the path and add up the size of "
            "every move, up or down: the total distance traveled. <bookmark mark='b'/> Sampled at sixteen steps, our path "
            f"travels {tv16:.1f}. <bookmark mark='c'/> At 256 steps, {tv256:.1f}. <bookmark mark='d'/> At four thousand, "
            f"{tv4k:.1f}. And at four million steps, more than sixteen hundred. <bookmark mark='e'/> Each time the steps get "
            "sixteen times finer, the distance quadruples, exactly as the formula predicts."
        ) as vo:
            self.play(Create(ax))
            vo.wait_until("a")
            self.play(Write(tvf), FadeIn(tvl))
            vo.wait_until("b")
            self.play(Create(z16), FadeIn(tab.header), Create(tab.rule), FadeIn(tab.rows[0][:2]))
            vo.wait_until("c")
            self.play(ReplacementTransform(z16, z256), FadeIn(tab.rows[1][:2]))
            vo.wait_until("d")
            self.play(FadeOut(z256), Create(full), FadeIn(tab.rows[2][:2]))
            self.play(FadeIn(tab.rows[3][:2]), FadeIn(tab.rows[4][:2]))
            vo.wait_until("e")
            self.play(FadeIn(tab.cols[2]))
        punch = label(r"infinite length on every time interval", font_size=34, color=C.QV).next_to(tab, DOWN, buff=0.45)
        rs = note(r"Riemann--Stieltjes $\int H\,dW$ needs finite length", font_size=26).next_to(punch, DOWN, buff=0.2)
        with self.voiceover(
            "In the limit, it's infinite. <bookmark mark='p'/> A Brownian path has infinite length over every interval of "
            "time, however short. <bookmark mark='r'/> And that's a real problem for calculus, because the classical way to "
            "integrate against a curve, the Riemann–Stieltjes integral, needs the curve to have finite length. "
            "<bookmark mark='q'/> So we need a new idea. And it comes from a surprise: add up the squares of those moves "
            "instead, and the sum doesn't blow up at all."
        ) as vo:
            vo.wait_until("p")
            self.play(FadeIn(punch, shift=UP * 0.2))
            vo.wait_until("r")
            self.play(FadeIn(rs))
        self.wait(0.3)
        self.clear_scene()
