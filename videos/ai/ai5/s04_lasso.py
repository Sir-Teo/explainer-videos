from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import AUSTEN, DICKENS, load

WSTAR = np.array([2.2, 0.5])  # the unpenalized best weights (illustrative)
H = np.array([[1.0, 0.3], [0.3, 1.6]])
RIDGE, LASSO = "#7FD3FF", C.BITS


def loss(w):
    d = w - WSTAR
    return float(d @ H @ d)


def project_l2(w, r):
    n = np.linalg.norm(w)
    return w if n <= r else w * r / n


def project_l1(w, r):
    if np.abs(w).sum() <= r:
        return w
    u = np.sort(np.abs(w))[::-1]
    cs = np.cumsum(u)
    k = np.nonzero(u * np.arange(1, len(w) + 1) > (cs - r))[0][-1]
    th = (cs[k] - r) / (k + 1)
    return np.sign(w) * np.maximum(np.abs(w) - th, 0)


def constrained(r, proj):
    w = proj(WSTAR.copy(), r)
    for _ in range(400):
        w = proj(w - 0.25 * 2 * H @ (w - WSTAR), r)
    return w


def ellipse(level, ax, color=GREY_C, sw=1.5):
    vals, vecs = np.linalg.eigh(H)
    ts = np.linspace(0, 2 * math.pi, 80)
    pts = [WSTAR + vecs @ (np.sqrt(level / vals) * np.array([math.cos(t), math.sin(t)])) for t in ts]
    return VMobject(color=color, stroke_width=sw).set_points_smoothly([ax.c2p(*p) for p in pts])


class Lasso(VoiceoverScene):
    def construct(self):
        self.card()
        self.shapes()
        self.path()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(3, r"Ridge and lasso", r"How do you stop a model from leaning on noise?", part=5)
        with self.voiceover("Chapter three. Keeping the weights small."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def panel(self, center, proj, color, shape_fn, title):
        ax = Axes(x_range=[-1.5, 3, 1], y_range=[-1.5, 2.5, 1], x_length=5.0, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to(center)
        conts = VGroup(*[ellipse(c, ax) for c in (0.15, 0.6, 1.4, 2.6, 4.2)])
        star = Dot(ax.c2p(*WSTAR), radius=0.07, color=WHITE)
        r = ValueTracker(1.8)
        region = always_redraw(lambda: shape_fn(ax, r.get_value(), color))

        def sol():
            w = constrained(r.get_value(), proj)
            return VGroup(ellipse(loss(w), ax, color=WHITE, sw=2.5), glow_dot(ax.c2p(*w), color=color, radius=0.09))

        touch = always_redraw(sol)
        names = VGroup(MathTex(r"w_1", font_size=28, color=GREY_A).next_to(ax.x_axis, RIGHT, buff=0.1),
                       MathTex(r"w_2", font_size=28, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1))
        t = label(title, font_size=28, color=color).next_to(ax, UP, buff=0.35)
        return ax, conts, star, r, region, touch, names, t

    def shapes(self):
        def circle(ax, r, color):
            u = ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]
            return Circle(radius=r * u, color=color, stroke_width=3, fill_color=color, fill_opacity=0.15).move_to(ax.c2p(0, 0))

        def diamond(ax, r, color):
            return Polygon(ax.c2p(r, 0), ax.c2p(0, r), ax.c2p(-r, 0), ax.c2p(0, -r), color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.15)

        L = self.panel([-3.4, -0.6, 0], project_l2, RIDGE, circle, r"ridge: \ $w_1^2 + w_2^2 \le t^2$")
        R = self.panel([3.4, -0.6, 0], project_l1, LASSO, diamond, r"lasso: \ $|w_1| + |w_2| \le t$")
        tag = label(r"illustrative: \ two weights, \ the loss's contour lines", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.2)
        head = label(r"Keep the weights in a budget", font_size=34).to_edge(UP, buff=0.3)
        w_end = constrained(0.9, project_l1)
        assert abs(w_end[1]) < 1e-9 < abs(w_end[0])  # the diamond's corner: w2 exactly zero
        zero = label(r"$w_2 = 0$ \ exactly", font_size=28, color=LASSO).next_to(R[0].c2p(0.9, 0), DR, buff=0.6)
        with self.voiceover(
            "With seventy weights, a model can lean on accidents of its training pages. A classic remedy: keep the "
            "weights small, by giving them a budget. <bookmark mark='a'/> Here are two weights, and the contour lines "
            "of the loss, whose lowest point is out here. <bookmark mark='b'/> Budget the squared length, and the "
            "weights must stay inside a circle: that's ridge regression. Budget the sum of absolute values, and "
            "they must stay inside a diamond: that's the lasso. The best weights are where the lowest contour line "
            "just touches the shape. <bookmark mark='c'/> Now shrink the budget. The circle's answer slides smoothly "
            "toward zero. The diamond's catches on a corner, where one weight is exactly zero."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            for P in (L, R):
                ax, conts, star, r, region, touch, names, t = P
                self.play(Create(ax), FadeIn(names), Create(conts), FadeIn(star), FadeIn(tag), run_time=1.0)
            vo.wait_until("b")
            for P in (L, R):
                ax, conts, star, r, region, touch, names, t = P
                self.play(FadeIn(t), FadeIn(region), FadeIn(touch))
            vo.wait_until("c")
            self.play(L[3].animate.set_value(0.9), R[3].animate.set_value(0.9), run_time=4.0)
            self.play(FadeIn(zero), Indicate(R[5], color=LASSO))
        for P in (L, R):
            P[4].clear_updaters()
            P[5].clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def path(self):
        d = load("lasso")
        p = load("pages")
        vocab = p["vocab"]
        path = np.asarray(d["path"])
        order, k5 = d["order"], int(d["k5"])
        words5 = d["words5"]
        n = len(path)
        top = float(np.abs(path).max()) * 1.05
        ax = Axes(x_range=[0, n - 1, 5], y_range=[-top, top, 1], x_length=8.4, y_length=5.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-1.8, -0.4, 0])
        xl = label(r"the penalty relaxes $\longrightarrow$", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        lines, named = VGroup(), {}
        for j, w in enumerate(vocab):
            ys = path[:, j]
            if not np.any(ys):
                continue
            hot = w in words5
            col = (DICKENS if ys[-1] > 0 else AUSTEN) if hot else GREY_D
            ln = VMobject(color=col, stroke_width=3 if hot else 1.5).set_points_as_corners(
                [ax.c2p(k, v) for k, v in enumerate(ys)])
            lines.add(ln)
            if hot:
                named[w] = ln
        tags = VGroup()
        for w, ln in named.items():
            tags.add(Text(w, font="DejaVu Sans Mono", font_size=20, color=ln.get_color()).next_to(ln.get_end(), RIGHT, buff=0.08))
        # keep the end labels from piling up
        tags = VGroup(*sorted(tags, key=lambda m: m.get_y()))
        for a, b in zip(tags[:-1], tags[1:]):
            if b.get_y() - a.get_y() < 0.28:
                b.set_y(a.get_y() + 0.28)
        mark = DashedLine(ax.c2p(k5, -top), ax.c2p(k5, top), color=WHITE, stroke_width=2)
        ml = label(rf"${len(words5)}$ words: \ ${100 * d['acc5']:.0f}\%$ of test pages right", font_size=26,
                   color=WHITE).next_to(mark, UP, buff=0.1)
        first = label(r"first to come alive: \ " + ", \\ ".join(rf"\texttt{{{w}}}" for w in order[:8]), font_size=24,
                      color=C.BITS).to_edge(UP, buff=0.3)
        sign = VGroup(label(r"above zero: \ Dickens", font_size=24, color=DICKENS),
                      label(r"below zero: \ Austen", font_size=24, color=AUSTEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        sign.to_corner(UR, buff=0.45).shift(DOWN * 0.7)
        cite_ = cite(r"R.~Tibshirani, \textit{Regression Shrinkage and Selection via the Lasso} (1996)", corner=DR)
        assert set(order[:8]) == set(words5)
        # the sweep, live: a cursor at the current penalty, and how many words it uses, and how well it does
        acc = np.asarray(d["acc"])
        u = ValueTracker(0)
        cur = lambda: min(n - 1, int(u.get_value() + 1e-6))  # noqa: E731
        cursor = always_redraw(lambda: Line(ax.c2p(u.get_value(), -top), ax.c2p(u.get_value(), top), color=GREY_B,
                                            stroke_width=1.5, stroke_opacity=0.7))
        nw = Integer(int(np.count_nonzero(path[0])), font_size=30, color=C.BITS)
        nw.add_updater(lambda m: m.set_value(int(np.count_nonzero(path[cur()]))))
        av = DecimalNumber(100 * acc[0], num_decimal_places=0, unit=r"\%", font_size=30, color=WHITE)
        av.add_updater(lambda m: m.set_value(100 * acc[cur()]))
        live = VGroup(VGroup(label(r"words in use:", font_size=24, color=C.BITS), nw).arrange(RIGHT, buff=0.15),
                      VGroup(label(r"test pages right:", font_size=24, color=GREY_A), av).arrange(RIGHT, buff=0.15))
        live.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(sign, DOWN, buff=0.4).align_to(sign, LEFT)
        keep_in_frame(live)
        with self.voiceover(
            "That corner is the lasso's gift: it chooses. Here are all seventy weights of the authorship model, as "
            "the penalty relaxes from total to gentle. <bookmark mark='a'/> The first words to come alive are 'not', "
            "'she', 'very', 'be', 'to', 'out', 'such' and 'mrs'. <bookmark mark='b'/> With just those eight words, "
            f"the classifier gets {100 * d['acc5']:.0f} percent of the test pages right. Ridge, by contrast, keeps "
            "every word, only smaller."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(sign), FadeIn(cite_), FadeIn(live))
            self.add(cursor)
            self.play(*[Create(l_) for l_ in lines], u.animate.set_value(n - 1), run_time=4.0, rate_func=linear)
            for m in (cursor, nw, av):
                m.clear_updaters()
            self.play(FadeOut(cursor), run_time=0.3)
            vo.wait_until("a")
            self.play(FadeIn(first), LaggedStart(*[FadeIn(t) for t in tags], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(Create(mark), FadeIn(ml))
        self.wait(0.3)
        self.clear_scene()
