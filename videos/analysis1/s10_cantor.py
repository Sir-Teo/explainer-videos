from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis1.common import cantor_function, cantor_intervals, load, polyline, segments_points
from videos.analysis1.s07_open_closed import nbhd


def cantor_bars(depth: int, a: float, b: float, x_left: float, x_right: float, y: float, height=0.22,
                color=WHITE, min_w=0.004) -> VMobject:
    """The depth-n stage of the Cantor set restricted to the window [a, b], drawn as thick strokes on one VMobject."""
    iv = cantor_intervals(depth)
    sel = (iv[:, 1] >= a) & (iv[:, 0] <= b)
    iv = iv[sel]
    sx = (x_right - x_left) / (b - a)
    xa = x_left + (np.clip(iv[:, 0], a, b) - a) * sx
    xb = x_left + (np.clip(iv[:, 1], a, b) - a) * sx
    m = VGroup()
    for x0, x1 in zip(xa, xb):
        w = max(x1 - x0, min_w)
        m.add(Rectangle(width=w, height=height, stroke_width=0, fill_color=color, fill_opacity=1)
              .move_to([(x0 + x1) / 2, y, 0]))
    return m


class Cantor(VoiceoverScene):
    def construct(self):
        self.card()
        self.perfect()
        self.construction()
        self.properties()
        self.digits()
        self.staircase()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(9, r"The Cantor set", r"Can a set be uncountable and have length zero?", lit=(1883,), part=1)
        with self.voiceover(
            "Chapter nine. Compactness gives a second, completely different proof that the real numbers are "
            "uncountable, and it leads to the most famous strange set in analysis."
        ) as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def perfect(self):
        stmt = VGroup(label(r"\textbf{Theorem} (Rudin 2.43)", font_size=28, color=GREY_A),
                      label(r"A nonempty perfect set in $\R^k$ is uncountable.", font_size=32)).arrange(DOWN, buff=0.12)
        stmt.to_edge(UP, buff=0.45)
        steps = VGroup(
            label(r"suppose $P = \{x_1, x_2, x_3, \ldots\}$", font_size=28),
            label(r"choose nested closed disks $\overline{V}_1 \supset \overline{V}_2 \supset \cdots$, each meeting $P$,", font_size=28),
            label(r"with $x_n \notin \overline{V}_{n+1}$ \ (possible: every point of $P$ is a limit point)", font_size=28),
            label(r"$K_n = \overline{V}_n \cap P$: nested, nonempty, compact \ $\Rightarrow$ \ $\bigcap K_n \neq \emptyset$ (2.36)",
                  font_size=28),
            label(r"but no $x_n$ is in it: \ a point of $P$ missing from the list", font_size=28, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([1.6, -1.2, 0])
        for s_ in steps:
            s_.set_max_width(8.8)
        o = np.array([-4.8, 0.3, 0])
        radii = [1.5, 0.95, 0.6, 0.38, 0.24]
        centers = [o, o + np.array([0.4, -0.25, 0]), o + np.array([0.55, -0.1, 0]), o + np.array([0.48, -0.2, 0]),
                   o + np.array([0.52, -0.16, 0])]
        disks = VGroup(*[Circle(radius=r, color=C.COMPACT_SET, stroke_width=3).move_to(c) for r, c in zip(radii, centers)])
        xs = [o + np.array([-0.8, 0.6, 0]), o + np.array([1.0, 0.45, 0]), o + np.array([0.1, -0.55, 0]),
              o + np.array([0.75, -0.42, 0])]
        xd = VGroup(*[VGroup(Dot(p, radius=0.06, color=C.PATHOLOGY),
                             MathTex(rf"x_{i + 1}", font_size=24, color=C.PATHOLOGY).next_to(p, UP, buff=0.06))
                      for i, p in enumerate(xs)])
        for i, p in enumerate(xs):
            assert np.linalg.norm(p - centers[i + 1]) > radii[i + 1]
        with self.voiceover(
            "Recall that a set is perfect if it's closed and every one of its points is a limit point: no isolated "
            "points. <bookmark mark='s'/> Every nonempty perfect set in k-dimensional space is uncountable. "
            "<bookmark mark='a'/> Suppose instead that a perfect set P could be listed: x one, x two, x three. "
            "<bookmark mark='b'/> Choose a closed disk that meets P, <bookmark mark='c'/> then a smaller closed disk inside "
            "it that still meets P but avoids x one. That's possible because every point of P is a limit point, so there "
            "are other points of P nearby to aim for. Then a smaller one avoiding x two, and so on."
        ) as vo:
            vo.wait_until("s")
            self.play(FadeIn(stmt))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(Create(disks[0]), FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            for i in range(4):
                self.play(FadeIn(xd[i]), Create(disks[i + 1]), run_time=0.7)
        with self.voiceover(
            "<bookmark mark='k'/> The pieces of P inside these disks are nested, nonempty and compact, so by last "
            "chapter's theorem something lies in all of them. <bookmark mark='m'/> That something is a point of P, but "
            "it can't be x n for any n, because the n plus first disk avoids x n. So the list missed a point. The real "
            "line is perfect, so this is a second proof that it's uncountable, built from compactness instead of digits."
        ) as vo:
            vo.wait_until("k")
            self.play(FadeIn(steps[3]))
            vo.wait_until("m")
            self.play(FadeIn(steps[4]), Flash(centers[-1], color=C.COMPACT_SET))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def construction(self):
        L, R = -6.0, 2.0
        ys = [2.3 - 0.62 * k for k in range(8)]
        stages = VGroup(*[cantor_bars(k, 0, 1, L, R, ys[k], height=0.2) for k in range(8)])
        labs = VGroup(*[MathTex(rf"E_{k}", font_size=28, color=GREY_A).next_to([L, ys[k], 0], LEFT, buff=0.25)
                        for k in range(8)])
        info = VGroup(*[MathTex(rf"2^{{{k}}} \text{{ pieces, total length }} (2/3)^{{{k}}}", font_size=24, color=GREY_B)
                        .move_to([4.75, ys[k] - 0.0, 0]) for k in range(8)])
        title = label(r"Remove the open middle third, again and again \ (Rudin 2.44)", font_size=30).to_edge(UP, buff=0.3)
        with self.voiceover(
            "The Cantor set, from 1883, is built by removing. <bookmark mark='a'/> Start with the interval from zero to "
            "one. <bookmark mark='b'/> Remove its open middle third, leaving two closed pieces. <bookmark mark='c'/> "
            "Remove the middle third of each of those, leaving four, then eight, then sixteen. <bookmark mark='p'/> The "
            "Cantor set is what survives every step: the intersection of all these stages."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(FadeIn(stages[0]), FadeIn(labs[0]))
            vo.wait_until("b")
            self.play(TransformFromCopy(stages[0], stages[1]), FadeIn(labs[1]))
            vo.wait_until("c")
            for k in range(2, 8):
                self.play(TransformFromCopy(stages[k - 1], stages[k]), FadeIn(labs[k]), run_time=0.6)
            vo.wait_until("p")
            self.play(LaggedStart(*[FadeIn(i_) for i_ in info], lag_ratio=0.1))
        d = load("cantor")
        for k in range(8):
            iv = d[f"iv{k}"]
            assert len(iv) == 2**k and abs((iv[:, 1] - iv[:, 0]).sum() - (2 / 3) ** k) < 1e-12
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def properties(self):
        props = VGroup(
            label(r"\textbf{compact}: an intersection of closed sets inside $[0, 1]$", font_size=30, color=C.COMPACT_SET),
            label(r"\textbf{nonempty}: $0$, $1$, $\tfrac13$, $\tfrac23$, \ldots \ every endpoint survives", font_size=30),
            label(r"\textbf{no interval}: any $(\alpha, \beta)$ contains a removed middle third", font_size=30),
            label(r"\textbf{perfect}: endpoints of later stages crowd up to every point", font_size=30),
            label(r"so \textbf{uncountable} (2.43), \ \ yet the removed lengths add up to", font_size=30, color=C.EPS),
            MathTex(r"\frac13 + \frac29 + \frac4{27} + \cdots = \frac{1/3}{1 - 2/3} = 1", font_size=40, color=C.MEASURE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(DOWN * 0.3)
        props[-1].shift(RIGHT * 1.5)
        head = label(r"What survives?", font_size=40).to_edge(UP, buff=0.45)
        with self.voiceover(
            "What survives? <bookmark mark='a'/> The Cantor set is compact, as an intersection of closed sets inside a "
            "compact interval. <bookmark mark='b'/> It's not empty: zero, one, and every endpoint of every stage is never "
            "removed. <bookmark mark='c'/> It contains no interval at all, since any interval, however short, contains "
            "some removed middle third. <bookmark mark='d'/> And it's perfect: near every point of the set, there are "
            "endpoints of later stages. <bookmark mark='e'/> So, by the theorem, it's uncountable. <bookmark mark='f'/> "
            "And yet, the lengths we removed add up to one third, plus two ninths, plus four twenty-sevenths, and so on: "
            "exactly one. Uncountably many points, total length zero."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcdef", props):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.15))
        card = museum_card(r"The Cantor set", r"Georg Cantor, 1883 (H.~J.~S.~Smith, 1875)",
                           r"``uncountable sets are big''", r"Rudin, \textit{Principles} 2.44").scale(0.9)
        card.to_corner(UR, buff=0.3)
        self.play(FadeIn(card, shift=LEFT * 0.2))
        self.wait(1.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def digits(self):
        d = load("cantor")
        dig = [int(x) for x in d["quarter_digits"]]
        L, R = -6.0, 6.0
        y = -0.4
        title = MathTex(r"\text{Cantor set} = \{\, x \in [0,1] : x \text{ has a base-3 expansion using only } 0 \text{ and } 2 \,\}",
                        font_size=32).to_edge(UP, buff=0.45)
        link = label(r"the zero--one sequences of chapter 4, with $1 \mapsto 2$", font_size=26, color=GREY_A)
        link.next_to(title, DOWN, buff=0.2)
        quarter = MathTex(r"\tfrac14 = 0.020202\ldots_{\,3}", font_size=40, color=C.EPS).next_to(link, DOWN, buff=0.35)
        a_, b_ = ValueTracker(0.0), ValueTracker(1.0)

        def view():
            a, b = a_.get_value(), b_.get_value()
            depth = min(12, int(math.log(max(1e-12, 1 / (b - a)), 3)) + 7)
            return cantor_bars(depth, a, b, L, R, y, height=0.5)

        bars = always_redraw(view)
        mark = always_redraw(lambda: Triangle(color=C.EPS, fill_opacity=1, stroke_width=0).scale(0.12).rotate(PI)
                             .move_to([L + (0.25 - a_.get_value()) / (b_.get_value() - a_.get_value()) * (R - L), y + 0.55, 0]))
        zoom_l = always_redraw(lambda: Text(f"zoom ×{1 / (b_.get_value() - a_.get_value()):,.0f}", font_size=24,
                                            color=GREY_B).to_corner(DR, buff=0.35))
        dig_tx = ValueTracker(0)
        digits_m = always_redraw(lambda: Text("0." + "".join(str(x) for x in dig[: int(round(dig_tx.get_value()))]) + "...",
                                              font_size=34, color=C.EPS, font="DejaVu Sans Mono").move_to([0, -2.2, 0]))
        with self.voiceover(
            "There's a cleaner description in base three. <bookmark mark='t'/> The first removal throws out the numbers "
            "whose first base-three digit has to be a one; the second throws out those whose second digit has to be one; "
            "and so on. The Cantor set is exactly the numbers that can be written in base three using only zeros and "
            "twos. <bookmark mark='l'/> Those are chapter four's zero-one sequences, with ones written as twos. That's why "
            "the map we used there landed here."
        ) as vo:
            self.play(FadeIn(bars))
            vo.wait_until("t")
            self.play(FadeIn(title))
            vo.wait_until("l")
            self.play(FadeIn(link))
        with self.voiceover(
            "Here's a strange member. <bookmark mark='q'/> One quarter, in base three, is 0.0202 repeating: only zeros and "
            "twos, so it's in the Cantor set, but it's never an endpoint of any stage. <bookmark mark='z'/> Zoom in "
            "around it by a factor of nine, and the picture repeats exactly: the set is self-similar. "
            "<bookmark mark='d'/> Each zoom reads off two more digits."
        ) as vo:
            vo.wait_until("q")
            self.play(FadeIn(quarter), FadeIn(mark), FadeIn(digits_m))
            vo.wait_until("z")
            self.add(zoom_l)
            for k in range(1, 5):
                w = 9.0 ** (-k)
                lo = 0.25 - w * 0.25 * 0.0 - (0.25 - 2 / 9) * 9 ** (-(k - 1))
                hi = lo + w * 1.0
                lo, hi = 0.25 - 0.25 * w * 1.0, 0.25 + 0.75 * w * 1.0
                self.play(a_.animate.set_value(lo), b_.animate.set_value(hi), dig_tx.animate.set_value(2 * k), run_time=2.0)
        assert dig[:8] == [0, 2, 0, 2, 0, 2, 0, 2]
        px = note(r"drawn to depth 12 at each zoom; past that, a screen cannot show the gaps").to_edge(DOWN, buff=0.3)
        self.play(FadeIn(px))
        self.wait(0.5)
        for m in (bars, mark, zoom_l, digits_m):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def staircase(self):
        d = load("cantor")
        ax = Axes(x_range=[0, 1, 1 / 3], y_range=[0, 1, 0.5], x_length=7.6, y_length=5.2, tips=False,
                  axis_config={"stroke_color": GREY_C}).shift(LEFT * 2.2 + DOWN * 0.4)
        xs = np.linspace(0, 1, 3001)

        def stair(n):
            return polyline(ax, xs, cantor_function(xs, depth=n), color=C.SEQ, stroke_width=3.5)

        S = stair(1)
        head = label(r"The Cantor function: the devil's staircase", font_size=34).to_edge(UP, buff=0.4)
        rule = VGroup(label(r"read the base-3 digits of $x$ up to the first $1$;", font_size=26),
                      label(r"turn the $2$s into $1$s; read it in base $2$", font_size=26),
                      MathTex(r"\tfrac14 = 0.0202\ldots_3 \;\mapsto\; 0.0101\ldots_2 = \tfrac13", font_size=32, color=C.EPS)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.2, 1.4, 0])
        props = VGroup(label(r"continuous, nondecreasing,", font_size=26),
                       label(r"$F(0) = 0$, \ $F(1) = 1$,", font_size=26),
                       label(r"flat on every removed third:", font_size=26),
                       label(r"it climbs on a set of length $0$", font_size=26, color=C.PATHOLOGY)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        props.move_to([4.2, -1.2, 0])
        assert abs(cantor_function(np.array([0.25]))[0] - 1 / 3) < 1e-12
        with self.voiceover(
            "One more object to keep for later. <bookmark mark='r'/> Define a function on the Cantor set by reading a "
            "number's base-three digits, turning the twos into ones, and reading the result in base two. One quarter, "
            "0.0202 repeating, goes to 0.0101 repeating in binary, which is one third. <bookmark mark='f'/> Fill in each "
            "removed middle third with a flat step. As we add stages, the steps multiply."
        ) as vo:
            self.play(FadeIn(head), Create(ax))
            vo.wait_until("r")
            self.play(FadeIn(rule))
            vo.wait_until("f")
            self.play(Create(S))
            for n in range(2, 9):
                self.play(Transform(S, stair(n)), run_time=0.6)
        with self.voiceover(
            "The limit is the devil's staircase. <bookmark mark='p'/> It's continuous and never decreases, it climbs "
            "from zero to one, and it's flat on every removed interval, which have total length one. All of the climbing "
            "happens on the Cantor set, a set of length zero. <bookmark mark='l'/> So its derivative is zero almost "
            "everywhere, and yet it rises. Keep it in mind: in Part 3 it will be an integrator, in Part 5 a measure, and "
            "in Part 6 the function for which the fundamental theorem of calculus fails."
        ) as vo:
            vo.wait_until("p")
            self.play(FadeIn(props))
            vo.wait_until("l")
            card = museum_card(r"The Cantor function", r"Cantor, 1884", r"``a function that rises has a positive slope''",
                               r"returns in Parts 3, 5, 6").scale(0.85).to_corner(DR, buff=0.25)
            self.play(FadeOut(props), FadeIn(card, shift=LEFT * 0.2))
        self.wait(0.6)
        self.clear_scene()
