from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis2.common import SQRT2, endpoint, load, plain_axes, polyline


class Connectedness(VoiceoverScene):
    def construct(self):
        self.card()
        self.ivt()
        self.over_q()
        self.kinds()
        self.monotone()
        self.thomae()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(11, r"Continuity and connectedness", r"Why can't a continuous function skip a value?",
                            lit=(1817,), part=2)
        with self.voiceover(
            "Chapter eleven. Bolzano's 1817 paper set out to prove that a continuous function can't get from below a "
            "value to above it without passing through it. The proof needs exactly what Part 1 built."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def ivt(self):
        thm = VGroup(label(r"\textbf{Rudin 4.22} \ A continuous image of a connected set is connected.", font_size=30),
                     label(r"\textbf{Rudin 4.23} \ (intermediate values) \ $f$ continuous on $[a, b]$, \ "
                           r"$f(a) < c < f(b)$ $\Rightarrow$ $f(x) = c$ for some $x$", font_size=28)
                     ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        ax = plain_axes([0, 4, 1], [-1.6, 1.8, 1], 8.4, 4.4, numbers=False).move_to([0.6, -1.0, 0])
        f = lambda x: 0.5 * np.sin(2.2 * x) + 0.55 * (x - 2) + 0.2 * np.cos(5 * x)  # noqa: E731
        a, b = 0.3, 3.8
        g = ax.plot(f, x_range=[a, b, 0.005], color=C.FUNC, stroke_width=4)
        c = -0.3
        lev = DashedLine(ax.c2p(0, c), ax.c2p(4, c), color=C.EPS, stroke_width=2)
        cl = MathTex(r"c", font_size=30, color=C.EPS).next_to(ax.c2p(4, c), RIGHT, buff=0.12)
        fa, fb = float(f(a)), float(f(b))
        assert fa < c < fb
        ends = VGroup(Dot(ax.c2p(a, fa), radius=0.07, color=WHITE), Dot(ax.c2p(b, fb), radius=0.07, color=WHITE),
                      MathTex(r"f(a)", font_size=26).next_to(ax.c2p(a, fa), DOWN, buff=0.15),
                      MathTex(r"f(b)", font_size=26).next_to(ax.c2p(b, fb), RIGHT, buff=0.15),
                      *[VGroup(Line(ax.c2p(v, 0) + DOWN * 0.08, ax.c2p(v, 0) + UP * 0.08, color=GREY_B),
                               MathTex(t_, font_size=26, color=GREY_B).next_to(ax.c2p(v, 0), UP if v == a else DOWN,
                                                                               buff=0.15))
                        for v, t_ in ((a, r"a"), (b, r"b"))])
        xs = np.linspace(a, b, 40001)
        ys = f(xs)
        roots = xs[np.where(np.diff(np.sign(ys - c)) != 0)[0]]
        rd = VGroup(*[Dot(ax.c2p(r, c), radius=0.07, color=C.EPS) for r in roots])
        img = VGroup(Line(ax.c2p(0, ys.min()) + LEFT * 0.18, ax.c2p(0, ys.max()) + LEFT * 0.18, color=C.CONNECTED_SET,
                          stroke_width=8))
        il = VGroup(label(r"$f([a, b])$ is connected,", font_size=24, color=C.CONNECTED_SET),
                    label(r"so an interval (2.47):", font_size=24, color=C.CONNECTED_SET),
                    label(r"it contains $c$", font_size=24, color=C.CONNECTED_SET)).arrange(DOWN, aligned_edge=RIGHT,
                                                                                          buff=0.1)
        il.next_to(img, LEFT, buff=0.2)
        with self.voiceover(
            "<bookmark mark='t'/> Continuous functions carry connected sets to connected sets: if the image split into "
            "two separated pieces, their preimages would split the domain. <bookmark mark='a'/> On an interval, that's "
            "the intermediate value theorem. <bookmark mark='b'/> The image of the interval is connected, so by Part "
            "1 it's an interval, <bookmark mark='c'/> and an interval containing f of a and f of b contains everything "
            "in between: here the level c is crossed three times."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(thm[0]), Create(ax), Create(g))
            vo.wait_until("a")
            self.play(FadeIn(ends))
            self.play(FadeIn(thm[1]))
            vo.wait_until("b")
            self.play(FadeIn(img), FadeIn(il))
            vo.wait_until("c")
            self.play(Create(lev), FadeIn(cl), LaggedStart(*[FadeIn(r, scale=1.5) for r in rd], lag_ratio=0.2))
        assert len(roots) == 3
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def over_q(self):
        ax = plain_axes([1, 2, 0.25], [-1.2, 2.2, 1], 9.0, 4.6, numbers=True, font_size=20,
                        axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                        x_axis_config={"numbers_to_exclude": [1]},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-0.6, -0.9, 0])
        head = MathTex(r"f(x) = x^2 - 2 \quad \text{on } \mathbb{Q} \cap [1, 2]", font_size=36).to_edge(UP, buff=0.3)
        from math import gcd
        # the fractions with denominator up to 12 on the main plot; up to 60 under the magnifier at sqrt 2
        pts = np.array(sorted({p / q for q in range(1, 13) for p in range(q, 2 * q + 1) if gcd(p, q) == 1}))
        dots = VGroup(*[Dot(ax.c2p(x, x * x - 2), radius=0.035, color=C.RATIONAL) for x in pts])
        fine = np.array(sorted({p / q for q in range(1, 61) for p in range(q, 2 * q + 1) if gcd(p, q) == 1}))
        hw = 0.0178
        mag_ax, mag = magnifier(ax, (SQRT2 - hw, SQRT2 + hw), (-0.074, 0.074), center=np.array([-3.4, 0.1, 0]),
                                width=3.2, height=2.0)
        sel = fine[np.abs(fine - SQRT2) < hw]
        assert len(sel) >= 20 and np.all(np.abs(sel**2 - 2) < 0.074)
        m_dots = VGroup(*[Dot(mag_ax.c2p(x, x * x - 2), radius=0.03, color=C.RATIONAL) for x in sel])
        m_zero = DashedLine(mag_ax.c2p(SQRT2 - hw, 0), mag_ax.c2p(SQRT2 + hw, 0), color=GREY_B, stroke_width=1.5)
        m_hole = Circle(radius=0.11, color=C.HOLE, stroke_width=3).move_to(mag_ax.c2p(SQRT2, 0)).set_fill(BACKGROUND, 1)

        zero = DashedLine(ax.c2p(1, 0), ax.c2p(2, 0), color=GREY_B, stroke_width=1.5)
        hole = Circle(radius=0.11, color=C.HOLE, stroke_width=3).move_to(ax.c2p(SQRT2, 0))
        # the hole's label inside the inset, above-left of it, where the (gently rising) curve is not
        hl = MathTex(r"\sqrt2 \notin \mathbb{Q}", font_size=30, color=C.HOLE).move_to(mag_ax.c2p(SQRT2 - 0.009, 0.045))
        assert hl.get_bottom()[1] > mag_ax.c2p(SQRT2, 0)[1] + 0.2
        txt = VGroup(label(r"$f(1) = -1 < 0 < 2 = f(2)$, \ $f$ is continuous on $\mathbb{Q}$,", font_size=26),
                     label(r"and $f$ is never $0$: \ $\mathbb{Q}$ is not connected (Part 1)", font_size=26,
                           color=C.HOLE)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-1.4, 2.4, 0])
        with self.voiceover(
            "Without completeness the theorem fails. <bookmark mark='a'/> Take x squared minus 2, but only at rational "
            "points between one and two. It's continuous there, negative at one and positive at two. "
            "<bookmark mark='b'/> But it's never zero: the only place it could be is root two, and that's not a "
            "rational. The rationals aren't connected, so their image needn't be an interval."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(zero))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.002), FadeIn(txt[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(hole), FadeIn(txt[1]))
            self.play(FadeIn(mag), FadeIn(m_zero), LaggedStart(*[FadeIn(x) for x in m_dots], lag_ratio=0.02),
                      Create(m_hole), FadeIn(hl), run_time=1.5)
        assert not np.any(np.abs(pts * pts - 2) < 1e-12)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kinds(self):
        head = VGroup(label(r"\textbf{Rudin 4.26} \ Discontinuities: \ \emph{first kind} if both one-sided limits "
                            r"$f(x-)$, $f(x+)$ exist,", font_size=28),
                      label(r"\emph{second kind} otherwise", font_size=28)).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.3)

        def panel(x0, title, col, build):
            ax = plain_axes([-1, 1, 1], [-1.3, 1.3, 1], 4.0, 3.2, numbers=False).move_to([x0, -0.3, 0])
            t = label(title, font_size=24, color=col).next_to(ax, UP, buff=0.15)
            return VGroup(ax, t, *build(ax))

        u = np.linspace(1, 220, 20000)
        p1 = panel(-4.5, r"removable: \ $f(x-) = f(x+) \ne f(x)$", GREY_A, lambda A: [
            A.plot(lambda x: 0.5 * x * x, x_range=[-1, -0.03], color=C.FUNC, stroke_width=3),
            A.plot(lambda x: 0.5 * x * x, x_range=[0.03, 1], color=C.FUNC, stroke_width=3),
            endpoint(A.c2p(0, 0), False, C.FUNC), Dot(A.c2p(0, 0.8), radius=0.06, color=C.FUNC)])
        p2 = panel(0.0, r"a jump: \ $f(x-) \ne f(x+)$", GREY_A, lambda A: [
            A.plot(lambda x: 0.3 * x - 0.5, x_range=[-1, 0], color=C.FUNC, stroke_width=3),
            A.plot(lambda x: 0.3 * x + 0.6, x_range=[0, 1], color=C.FUNC, stroke_width=3),
            endpoint(A.c2p(0, -0.5), False, C.FUNC), Dot(A.c2p(0, 0.6), radius=0.06, color=C.FUNC)])
        p3 = panel(4.5, r"second kind: \ $\sin(1/x)$", C.PATHOLOGY, lambda A: [
            polyline(A, 1 / u, np.sin(u), color=C.FUNC, stroke_width=2),
            polyline(A, -1 / u, -np.sin(u), color=C.FUNC, stroke_width=2)])
        foot = label(r"first-kind discontinuities are also called \emph{simple}", font_size=24, color=GREY_B).to_edge(
            DOWN, buff=0.5)
        with self.voiceover(
            "When continuity fails, it fails in one of two ways. <bookmark mark='a'/> If the limits from the left and "
            "the right both exist, the discontinuity is of the first kind, or simple: either the two limits agree and "
            "only the value is wrong, <bookmark mark='b'/> or they disagree, and the graph jumps. <bookmark mark='c'/> "
            "Otherwise it's of the second kind, like sine of one over x, which has no one-sided limits at zero."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(p1))
            vo.wait_until("b")
            self.play(FadeIn(p2))
            vo.wait_until("c")
            self.play(FadeIn(p3), FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def monotone(self):
        d = load("thomae")
        r, cj, grid, F = d["r"], d["c"], d["grid"], d["F"]
        thm = VGroup(label(r"\textbf{Rudin 4.29--4.30} \ A monotone function has only jump discontinuities,", font_size=28),
                     label(r"and at most countably many: \ each jump contains its own rational.", font_size=28)
                     ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        ax = plain_axes([0, 6, 1], [0, 4, 1], 6.4, 4.4, numbers=False).move_to([-3.0, -1.0, 0])
        xs = [0.0, 1.0, 2.2, 3.1, 4.4, 5.2, 6.0]
        ys = [0.3, 0.9, 1.7, 2.0, 2.9, 3.3, 3.8]
        jumps = [(1.0, 0.9, 1.4), (2.2, 1.9, 2.25), (3.1, 2.4, 2.95), (4.4, 3.2, 3.5), (5.2, 3.6, 3.75)]
        segs = VGroup()
        prev = (0.0, 0.3)
        for (xj, ylo, yhi) in jumps:
            segs.add(Line(ax.c2p(prev[0], prev[1]), ax.c2p(xj, ylo), color=C.FUNC, stroke_width=4))
            segs.add(endpoint(ax.c2p(xj, ylo), False, C.FUNC), Dot(ax.c2p(xj, yhi), radius=0.06, color=C.FUNC))
            prev = (xj, yhi)
        segs.add(Line(ax.c2p(prev[0], prev[1]), ax.c2p(6.0, 3.95), color=C.FUNC, stroke_width=4))
        tags = VGroup()
        fracs = [r"\tfrac{11}{10}", r"2", r"\tfrac{8}{3}", r"\tfrac{10}{3}", r"\tfrac{11}{3}"]
        for (xj, ylo, yhi), fr in zip(jumps, fracs):
            br = Line(ax.c2p(xj, ylo), ax.c2p(xj, yhi), color=C.EPS, stroke_width=6)
            t = MathTex(fr, font_size=24, color=C.EPS).next_to(ax.c2p(xj, ylo), DR, buff=0.08)
            tags.add(VGroup(br, t))
        why_ = VGroup(label(r"the gaps $(f(x-), f(x+))$ are disjoint,", font_size=26),
                      label(r"so $x \mapsto$ (a rational in its gap) is one-to-one:", font_size=26),
                      label(r"countably many jumps", font_size=26, color=C.EPS)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.12)
        why_.move_to([3.6, 1.2, 0])
        ax2 = plain_axes([0, 1, 0.5], [0, 1, 0.5], 5.4, 2.7, numbers=False).move_to([3.6, -2.0, 0])
        stair = VMobject(color=C.FUNC, stroke_width=2.5)
        stair.set_points_as_corners([ax2.c2p(x, y) for x, y in zip(grid, F)])
        s_l = label(r"4.31: \ a jump at \emph{every} rational \ (size $\propto 1/q^3$)", font_size=22,
                    color=GREY_A).next_to(ax2, UP, buff=0.1)
        with self.voiceover(
            "Monotone functions are much tamer. <bookmark mark='t'/> An increasing function has one-sided limits "
            "everywhere, so its only discontinuities are jumps. <bookmark mark='a'/> And there can only be countably "
            "many: each jump opens a gap in the values, <bookmark mark='b'/> the gaps don't overlap, and each contains "
            "a rational number, which it can claim as its own. Different jumps claim different rationals, and there are "
            "only countably many rationals. <bookmark mark='c'/> Countably many can still be a lot: Rudin builds an "
            "increasing function that jumps at every single rational. Here it is, with jumps at fractions of denominator "
            "up to forty, each sized by its denominator."
        ) as vo:
            self.play(FadeIn(thm[0]), Create(ax), Create(segs))
            vo.wait_until("a")
            self.play(FadeIn(thm[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t) for t in tags], lag_ratio=0.2), FadeIn(why_))
            vo.wait_until("c")
            self.play(Create(ax2), FadeIn(s_l))
            self.play(Create(stair), run_time=2.0)
        for (xj, ylo, yhi), fr in zip(jumps, (11 / 10, 2, 8 / 3, 10 / 3, 11 / 3)):
            assert ylo < fr < yhi
        assert np.all(np.diff(F) >= 0) and abs(F[-1] - 1) < 1e-12
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def thomae(self):
        d = load("thomae")
        x, y = d["x"], d["y"]
        x0, eps, delta = float(d["x0"]), float(d["eps"]), float(d["delta"])
        ax = plain_axes([0, 1, 0.25], [0, 0.55, 0.1], 11.0, 4.3, numbers=True, font_size=20,
                        axis_config={"decimal_number_config": {"num_decimal_places": 2}}).move_to([0, -0.85, 0])
        keep = y <= 0.55
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.012 + 0.03 * b, color=C.RATIONAL) for a, b in zip(x[keep], y[keep])])
        top = VGroup(Dot(ax.c2p(0, 0.55), radius=0.03, color=C.RATIONAL))
        head = VGroup(MathTex(r"f\big(\tfrac pq\big) = \tfrac1q, \qquad f(\text{irrational}) = 0", font_size=36),
                      label(r"Thomae's function (Rudin, Exercise 4.18)", font_size=24, color=GREY_B)
                      ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        ruler = label(r"the rational ruler of Part 1, \ with tick height $1/q$", font_size=26, color=C.EPS).next_to(
            head, DOWN, buff=0.2)
        with self.voiceover(
            "And the strangest example. <bookmark mark='a'/> Give each fraction p over q in lowest terms the value one "
            "over q, and each irrational the value zero. <bookmark mark='b'/> If this picture looks familiar, it's "
            "because it's the rational ruler we've used since Part 1, with each tick's height set to one over its "
            "denominator."
        ) as vo:
            self.play(FadeIn(head), Create(ax))
            self.play(LaggedStart(*[FadeIn(p) for p in dots], lag_ratio=0.001), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(ruler))
        band = Rectangle(width=ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, eps)[1] - ax.c2p(0, 0)[1],
                         stroke_width=0, fill_color=C.EPS, fill_opacity=0.16).move_to((ax.c2p(0, 0) + ax.c2p(1, eps)) / 2)
        bline = DashedLine(ax.c2p(0, eps), ax.c2p(1, eps), color=C.EPS, stroke_width=2)
        strip = Rectangle(width=ax.c2p(x0 + delta, 0)[0] - ax.c2p(x0 - delta, 0)[0],
                          height=ax.c2p(0, 0.45)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=C.DELTA,
                          fill_opacity=0.25).move_to((ax.c2p(x0 - delta, 0) + ax.c2p(x0 + delta, 0.45)) / 2)
        xm = Dot(ax.c2p(x0, 0), radius=0.07, color=WHITE)
        # left of the dot, clear of the axis's 0.75 (1/sqrt 2 = 0.707 is too close to share its row centred)
        xl = MathTex(r"1/\sqrt2", font_size=26).next_to(xm, DOWN, buff=0.15).align_to(xm, RIGHT).shift(LEFT * 0.12)
        big = VGroup(*[dots[i] for i, (a, b) in enumerate(zip(x[keep], y[keep])) if b >= eps])
        near = Dot(ax.c2p(0.7, 0.1), radius=0.07, color=C.PATHOLOGY)
        nl = MathTex(r"\tfrac{7}{10}", font_size=26, color=C.PATHOLOGY).next_to(near, UL, buff=0.08)
        txt = VGroup(label(r"at an irrational: \ only the finitely many points with $q \le 1/\varepsilon$ reach "
                           r"$\varepsilon$;", font_size=24),
                     label(rf"keep $\delta$ below the distance to the nearest: \ $\delta = {delta:.4f}$ \ (to "
                           r"$\tfrac{7}{10}$)", font_size=24, color=C.DELTA),
                     label(r"so $f$ is \textbf{continuous at every irrational}, \ and discontinuous at every rational",
                           font_size=26, color=C.EPS)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        txt.next_to(head, DOWN, buff=0.25)  # under the heading, where the ruler caption was: clear of the dots
        # under a magnifier (horizontal only): the strip, the band, and every fraction (q <= 60) near 1/sqrt 2
        win_x, win_y = (0.68, 0.735), (0.0, 0.16)
        mag_ax, mag = magnifier(ax, win_x, win_y, center=np.array([4.35, -0.3, 0]), width=2.3, height=1.7,
                                color=GREY_B, tag=rf"x \times {2.3 / (ax.c2p(win_x[1], 0)[0] - ax.c2p(win_x[0], 0)[0]):.0f}")
        sel = (x >= win_x[0]) & (x <= win_x[1]) & (y <= win_y[1])
        m_band = Rectangle(width=2.3, height=mag_ax.c2p(0, eps)[1] - mag_ax.c2p(0, 0)[1], stroke_width=0,
                           fill_color=C.EPS, fill_opacity=0.16).move_to((mag_ax.c2p(win_x[0], 0) + mag_ax.c2p(win_x[1], eps)) / 2)
        m_bline = DashedLine(mag_ax.c2p(win_x[0], eps), mag_ax.c2p(win_x[1], eps), color=C.EPS, stroke_width=1.5)
        m_strip = Rectangle(width=mag_ax.c2p(x0 + delta, 0)[0] - mag_ax.c2p(x0 - delta, 0)[0], height=1.7, stroke_width=0,
                            fill_color=C.DELTA, fill_opacity=0.25).move_to(mag_ax.c2p(x0, win_y[1] / 2))
        m_dots = VGroup(*[Dot(mag_ax.c2p(a, b), radius=0.025 + 0.25 * b,
                              color=C.PATHOLOGY if abs(a - 0.7) < 1e-12 else (C.CLOSED_SET if b >= eps else C.RATIONAL))
                          for a, b in zip(x[sel], y[sel])])
        m_x0 = Dot(mag_ax.c2p(x0, 0), radius=0.05, color=WHITE)
        # 7/10 sits inside the magnifier's frame: its label goes outside, with a leader
        nl.next_to(mag.src, LEFT, buff=0.12).set_y(ax.c2p(0, eps)[1] + 0.1 + nl.height / 2)  # above the band's edge
        nl = VGroup(nl, Line(nl.get_right() + RIGHT * 0.03, near.get_center(), color=C.PATHOLOGY, stroke_width=1.5,
                             buff=0.08))
        assert sel.sum() >= 8 and np.all(y[sel & (np.abs(x - x0) < delta)] < eps)
        with self.voiceover(
            "<bookmark mark='a'/> It's continuous at every irrational. Take one over root two, and epsilon equal to a "
            "tenth. <bookmark mark='b'/> Only the fractions with denominator at most ten reach the band's top edge, "
            "and there are finitely many of them. <bookmark mark='c'/> So a small enough strip avoids them all: here "
            "the nearest is seven tenths, and delta is about seven thousandths. Inside the strip every value is below "
            "epsilon. <bookmark mark='d'/> At a rational, though, the value is positive while irrationals arbitrarily "
            "close have value zero. So this function is continuous exactly at the irrationals."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeOut(ruler), FadeIn(band), Create(bline), FadeIn(xm), FadeIn(xl))
            vo.wait_until("b")
            self.play(FadeIn(txt[0]), big.animate.set_color(C.CLOSED_SET))
            vo.wait_until("c")
            self.play(FadeIn(strip), FadeIn(near), FadeIn(nl), FadeIn(txt[1]))
            self.play(Create(mag.src), FadeIn(mag.frame), Create(mag.guides), FadeIn(mag.tag), run_time=0.8)
            self.play(FadeIn(m_band), Create(m_bline), FadeIn(m_strip), FadeIn(m_dots), FadeIn(m_x0), run_time=1.0)
            vo.wait_until("d")
            self.play(FadeIn(txt[2]))
        assert np.all(y[np.abs(x - x0) < delta] < eps)
        self.wait(0.3)
        card = museum_card(r"Thomae's function", r"Thomae, 1875",
                           r"continuous at every irrational, discontinuous at every rational",
                           r"Rudin, Exercise 4.18; the reverse is impossible (Baire, Part 8)").move_to([3.3, -0.2, 0])
        # the specimen stays beside its card, shrunk
        tax = plain_axes([0, 1, 0.5], [0, 0.55, 0.5], 5.6, 3.4, numbers=False).move_to([-3.35, -0.2, 0])
        tdots = VGroup(*[Dot(tax.c2p(a, b), radius=0.008 + 0.025 * b, color=C.RATIONAL)
                         for a, b in zip(x[keep], y[keep])])
        dset = {id(m) for m in dots}
        others = [m for m in self.mobjects if id(m) not in dset and m is not dots and m is not ax]
        with self.voiceover(
            "Into the museum it goes. And the reverse, a function continuous exactly at the rationals, is impossible, "
            "though proving that needs Baire's theorem, in Part 8."
        ):
            self.play(*[FadeOut(m) for m in others], FadeOut(ax), FadeIn(tax), Transform(dots, tdots), run_time=1.2)
            self.play(FadeIn(card, scale=0.95))
        self.wait(0.8)
        self.clear_scene()
