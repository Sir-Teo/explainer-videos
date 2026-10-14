from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis1.common import SQRT2, Window, endpoint, load, pin


def number_line(a, b, x_left=-6.4, x_right=6.4, y=-1.0, step=None, color=GREY_C, font_size=22):
    """A plain real line from a to b with labeled ticks, and its coordinate map."""
    def X(v):
        return x_left + (v - a) / (b - a) * (x_right - x_left)

    g = VGroup(Line([x_left - 0.1, y, 0], [x_right + 0.1, y, 0], color=color, stroke_width=2.5))
    if step:
        k0, k1 = math.ceil(a / step - 1e-9), math.floor(b / step + 1e-9)
        for k in range(k0, k1 + 1):
            v = k * step
            g.add(Line([X(v), y - 0.07, 0], [X(v), y + 0.07, 0], color=color, stroke_width=2))
            g.add(Text(f"{v:g}", font_size=font_size, color=GREY_B).move_to([X(v), y - 0.35, 0]))
    g.X = X
    return g


class Archimedes(VoiceoverScene):
    def construct(self):
        self.card()
        self.archimedean()
        self.density()
        self.root()
        self.nested()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(3, r"Archimedes, density and decimals",
                            r"What does the least-upper-bound property buy us?", lit=(1817,), part=1)
        with self.voiceover(
            "Chapter three. The real numbers have no holes. What does that buy us? Three things we'll use constantly."
        ) as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def archimedean(self):
        stmt = VGroup(label(r"\textbf{Archimedean property} (Rudin 1.20)", font_size=28, color=GREY_A),
                      label(r"If $x > 0$ and $y \in \R$, then $nx > y$ for some whole number $n$.", font_size=32))
        stmt.arrange(DOWN, buff=0.12).to_edge(UP, buff=0.5)
        nl = number_line(0, 10, y=-0.6, step=1)
        X = nl.X
        x, y = 0.83, 8.6
        y_m = VGroup(Line([X(y), -1.0, 0], [X(y), 0.4, 0], color=WHITE, stroke_width=3),
                     MathTex(r"y", font_size=34).move_to([X(y), 0.65, 0]))
        steps = VGroup()
        for k in range(1, 12):
            a, b = X((k - 1) * x), X(k * x)
            col = C.DELTA if k * x <= y else C.EPS
            steps.add(Arrow([a, -0.25, 0], [b, -0.25, 0], buff=0.02, color=col, stroke_width=4,
                            max_tip_length_to_length_ratio=0.25, tip_length=0.14))
        xl = MathTex(r"x", font_size=30, color=C.DELTA).next_to(steps[0], UP, buff=0.1)
        n_win = next(k for k in range(1, 100) if k * x > y)
        assert n_win == 11
        win_l = MathTex(rf"{n_win}x > y", font_size=34, color=C.EPS).next_to(steps[n_win - 1], UP, buff=0.15)
        win_l.shift(RIGHT * (X(y) + 0.2 - win_l.get_left()[0]))  # clear of the y marker
        with self.voiceover(
            "First, the Archimedean property. <bookmark mark='s'/> Pick any positive x, however tiny, and any y, "
            "however large. <bookmark mark='m'/> Then some whole-number multiple of x passes y."
        ) as vo:
            self.play(FadeIn(stmt))
            vo.wait_until("s")
            self.play(Create(nl), FadeIn(y_m))
            vo.wait_until("m")
            self.play(GrowArrow(steps[0]), FadeIn(xl), run_time=0.6)
            self.play(LaggedStart(*[GrowArrow(s) for s in steps[1:n_win]], lag_ratio=0.6), run_time=2.4)
            self.play(FadeIn(win_l))
        self.play(FadeOut(VGroup(steps, xl, win_l)))

        # schematic of the contradiction: if every multiple were <= y, alpha = sup would satisfy alpha <= y
        xs_, alpha, y_s = 1.5, 7.0, 8.0
        assert alpha <= y_s and (alpha - xs_) < 4 * xs_ <= alpha < 5 * xs_
        y_m2 = VGroup(Line([X(y_s), -0.72, 0], [X(y_s), 0.4, 0], color=WHITE, stroke_width=3),  # above the "8"
                      MathTex(r"y", font_size=34).move_to([X(y_s), 0.65, 0]))
        a_line = DashedLine([X(alpha), -0.72, 0], [X(alpha), 0.9, 0], color=C.UPPER_SUM, stroke_width=3)
        a_l = MathTex(r"\alpha = \sup\{x, 2x, 3x, \ldots\} \le y", font_size=30, color=C.UPPER_SUM)
        a_l.move_to([X(alpha) - 1.0, 1.25, 0])
        am = DashedLine([X(alpha - xs_), -1.0, 0], [X(alpha - xs_), 0.2, 0], color=GREY_B, stroke_width=2)
        am_l = MathTex(r"\alpha - x", font_size=28, color=GREY_B).move_to([X(alpha - xs_), -1.45, 0])
        mx = Dot([X(4 * xs_), -0.6, 0], radius=0.09, color=C.DELTA)
        mx_l = MathTex(r"mx", font_size=30, color=C.DELTA).next_to(mx, UP, buff=0.12)
        nxt = Dot([X(5 * xs_), -0.6, 0], radius=0.09, color=C.PATHOLOGY)
        nxt_l = MathTex(r"(m+1)x > \alpha", font_size=30, color=C.PATHOLOGY).move_to([X(5 * xs_) + 1.6, -1.45, 0])
        arr = CurvedArrow(mx.get_center() + UP * 0.1, nxt.get_center() + UP * 0.1, angle=-TAU / 5, color=C.DELTA,
                          tip_length=0.15)
        hyp = label(r"suppose not: then $nx \le y$ for every $n$", font_size=28, color=GREY_A).next_to(stmt, DOWN, buff=0.35)
        sch = schematic_tag(corner=DR).to_corner(DR, buff=0.45)
        self.play(FadeOut(y_m), FadeIn(y_m2), FadeIn(sch))
        with self.voiceover(
            "It sounds obvious, but it's a consequence of having no holes. <bookmark mark='s'/> Suppose it failed: every "
            "multiple of x stays at or below y. Then the multiples are bounded above, <bookmark mark='a'/> so they have "
            "a least upper bound, alpha. <bookmark mark='b'/> Alpha minus x is smaller than alpha, so it isn't an upper "
            "bound: <bookmark mark='c'/> some multiple, m x, is bigger than alpha minus x. <bookmark mark='d'/> But then "
            "the next one, m plus one times x, is bigger than alpha, which was supposed to be an upper bound. "
            "Contradiction."
        ) as vo:
            vo.wait_until("s")
            self.play(FadeIn(hyp))
            vo.wait_until("a")
            self.play(Create(a_line), FadeIn(a_l))
            vo.wait_until("b")
            self.play(Create(am), FadeIn(am_l))
            vo.wait_until("c")
            self.play(FadeIn(mx, scale=2), FadeIn(mx_l))
            vo.wait_until("d")
            self.play(Create(arr), FadeIn(nxt, scale=2), FadeIn(nxt_l))
            self.play(Flash(nxt, color=C.PATHOLOGY))
        nonarch = label(r"There are ordered fields where it fails: fields with infinitely small elements.", font_size=26,
                        color=GREY_B).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "That's a genuine theorem, not a triviality: <bookmark mark='n'/> there are ordered fields, with infinitely "
            "small elements, where it fails. The real numbers are not one of them."
        ) as vo:
            vo.wait_until("n")
            self.play(FadeIn(nonarch))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def density(self):
        stmt = VGroup(label(r"\textbf{$\Q$ is dense in $\R$} (Rudin 1.20)", font_size=28, color=GREY_A),
                      label(r"If $x < y$, then $x < p < y$ for some $p \in \Q$.", font_size=32))
        stmt.arrange(DOWN, buff=0.12).to_edge(UP, buff=0.5)
        a, b = 0.2, 0.8  # wide enough that the quarter ruler shows several ticks around the gap
        nl = number_line(a, b, y=-1.4, step=0.1)
        X = nl.X
        x, y = SQRT2 - 1, 0.45
        gap = VGroup(Line([X(x), -1.4, 0], [X(y), -1.4, 0], color=C.EPS, stroke_width=10))
        xm = VGroup(Dot([X(x), -1.4, 0], radius=0.08, color=C.EPS), MathTex(r"x = \sqrt2 - 1", font_size=28, color=C.EPS)
                    .move_to([X(x) - 0.6, -2.3, 0]))
        ym = VGroup(Dot([X(y), -1.4, 0], radius=0.08, color=C.EPS), MathTex(r"y = 0.45", font_size=28, color=C.EPS)
                    .move_to([X(y) + 0.4, -2.3, 0]))

        def ruler(n, y0=0.2, color=C.DELTA):
            g = VGroup()
            for k in range(math.ceil(a * n), math.floor(b * n) + 1):
                v = k / n
                inside = x < v < y
                g.add(Line([X(v), y0 - 0.35, 0], [X(v), y0 + 0.35, 0], color=C.EPS if inside else color,
                           stroke_width=5 if inside else 3))
            lab = MathTex(rf"\text{{spacing }} \tfrac{{1}}{{{n}}}", font_size=30, color=color).move_to([-5.3, y0 + 0.75, 0])
            return VGroup(g, lab)

        n_need = math.ceil(1 / (y - x) + 1e-9)
        assert n_need == 28 and 12 / 28 > x and 12 / 28 < y
        assert not any(x < k / 4 < y for k in range(5))
        r4, r28 = ruler(4, 1.25), ruler(28, -0.15)
        why1 = label(r"spacing bigger than the gap: it can miss", font_size=26, color=GREY_A).move_to([2.6, 1.95, 0])
        why2 = label(r"spacing $\tfrac1n < y - x$: some tick $\tfrac{m}{n}$ must land inside", font_size=26, color=C.EPS)
        why2.move_to([2.6, 0.6, 0])
        with self.voiceover(
            "Second: the rationals are dense in the reals. <bookmark mark='g'/> Between any two different reals, however "
            "close, sits a fraction. Take x as root two minus one, and y as 0.45. <bookmark mark='r'/> A ruler with "
            "marks every quarter can miss the gap entirely. <bookmark mark='a'/> But by the Archimedean property, we "
            "can choose n so that n times the gap is bigger than one: here n is 28. <bookmark mark='t'/> Then the marks "
            "of a ruler spaced one over n apart are closer together than x and y, so one of them must land in between: "
            "twelve twenty-eighths, which is three sevenths."
        ) as vo:
            self.play(FadeIn(stmt))
            vo.wait_until("g")
            self.play(Create(nl), FadeIn(gap), FadeIn(xm), FadeIn(ym))
            vo.wait_until("r")
            self.play(FadeIn(r4), FadeIn(why1))
            vo.wait_until("a")
            self.play(FadeIn(r28[1]), LaggedStart(*[Create(t) for t in r28[0]], lag_ratio=0.05), run_time=1.6)
            vo.wait_until("t")
            self.play(FadeIn(why2), Indicate(VGroup(*[t for t in r28[0] if t.get_color() == ManimColor(C.EPS)]),
                                             color=C.EPS, scale_factor=1.6))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def root(self):
        stmt = VGroup(label(r"\textbf{Theorem} (Rudin 1.21, for $n = 2$)", font_size=28, color=GREY_A),
                      label(r"Some $y \in \R$, $y > 0$, has $y^2 = 2$.", font_size=32)).arrange(DOWN, buff=0.12)
        stmt.to_edge(UP, buff=0.5)
        nl = number_line(1.0, 1.8, y=-0.9, step=0.1)
        X = nl.X
        A = VGroup(Line([X(1.0) - 0.1, -0.9, 0], [X(SQRT2), -0.9, 0], color=C.CUT_LOW, stroke_width=8))
        B = VGroup(Line([X(SQRT2), -0.9, 0], [X(1.8) + 0.1, -0.9, 0], color=C.CUT_HIGH, stroke_width=8))
        A_l = MathTex(r"A = \{t > 0 : t^2 < 2\}", font_size=34, color=C.CUT_LOW).move_to([-3.0, 0.3, 0])
        ydot = Dot([X(SQRT2), -0.9, 0], radius=0.1, color=WHITE)
        y_l = MathTex(r"y = \sup A", font_size=34).next_to(ydot, UP, buff=0.35)
        with self.voiceover(
            "Third: the hole at root two really is filled. <bookmark mark='a'/> In the reals, let A be the positive "
            "numbers whose square is less than two. It's bounded above, by two for instance, <bookmark mark='y'/> so it "
            "has a supremum. Call it y. Is y squared equal to two?"
        ) as vo:
            self.play(FadeIn(stmt))
            vo.wait_until("a")
            self.play(Create(nl), Create(A), FadeIn(A_l))
            vo.wait_until("y")
            self.play(FadeIn(ydot, scale=2), FadeIn(y_l))
        c1 = VGroup(MathTex(r"y^2 < 2", font_size=34, color=C.CUT_LOW),
                    MathTex(r"\Rightarrow\ \tfrac{2y+2}{y+2} \in A \text{ and } > y", font_size=32),
                    label(r"so $y$ is not an upper bound", font_size=28, color=C.PATHOLOGY)).arrange(DOWN, buff=0.2)
        c2 = VGroup(MathTex(r"y^2 > 2", font_size=34, color=C.CUT_HIGH),
                    MathTex(r"\Rightarrow\ \tfrac{2y+2}{y+2} < y \text{ is an upper bound}", font_size=32),
                    label(r"so $y$ is not the least one", font_size=28, color=C.PATHOLOGY)).arrange(DOWN, buff=0.2)
        cases = VGroup(c1, c2).arrange(RIGHT, buff=1.2).move_to(DOWN * 2.6)
        verdict = MathTex(r"y^2 = 2", font_size=48, color=C.EPS)
        verdict = boxed(verdict, color=C.EPS).move_to([3.6, 0.6, 0])
        with self.voiceover(
            "Use chapter one's hop again, now on real numbers. <bookmark mark='a'/> If y squared were less than two, the "
            "hop would give a bigger number that's still in A, so y wouldn't be an upper bound. <bookmark mark='b'/> If "
            "y squared were more than two, the hop would give a smaller upper bound, so y wouldn't be the least one. "
            "<bookmark mark='c'/> Only one option is left: y squared is two. The argument that showed the rationals have "
            "a hole, run in the reals, shows the reals don't."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(c1, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(c2, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(B), FadeIn(verdict, scale=1.1))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def nested(self):
        d = load("sqrt2")
        dec = str(d["dec"])
        lo = [int(v) for v in d["lo"]]
        win = Window(1.5, 1.2, x_left=-6.2, x_right=6.2, y=-0.8)  # labels stay 0.4 inside the frame
        axis, labs = win.axis(), win.labels()
        dust = win.dust(height=0.7, target=900)
        band = always_redraw(lambda: VGroup())
        level = ValueTracker(0)

        def band_mob():
            k = int(round(level.get_value()))
            a, b = lo[k] / 10**k, (lo[k] + 1) / 10**k
            xa, xb = win.X(a), win.X(b)
            # clipped to the ruler: mid-zoom the interval can be far wider than the window
            ca, cb = max(xa, win.L), min(xb, win.R)
            r = Rectangle(width=max(0.02, cb - ca), height=0.5, stroke_width=0, fill_color=C.COMPACT_SET,
                          fill_opacity=0.35).move_to([(ca + cb) / 2, win.y + 0.25, 0])
            ends = VGroup(*[Line([x, win.y - 0.15, 0], [x, win.y + 0.65, 0], color=C.COMPACT_SET, stroke_width=4)
                            for x in (xa, xb) if win.L <= x <= win.R])
            return VGroup(r, ends)

        band = always_redraw(band_mob)
        digits_shown = ValueTracker(0)

        def digits_mob():
            k = int(round(digits_shown.get_value()))
            s = dec[: (1 if k == 0 else k + 2)]
            return Text(s, font_size=40, color=C.COMPACT_SET, font="DejaVu Sans Mono").to_edge(UP, buff=0.6)

        digits = always_redraw(digits_mob)

        def interval_tex(k):
            a = f"{lo[k] / 10**k:.{k}f}"
            b = f"{(lo[k] + 1) / 10**k:.{k}f}"
            return MathTex(rf"[\,{a},\ {b}\,]", font_size=32, color=C.COMPACT_SET)

        # the interval changes with the digits (at the middle of each zoom), instead of morphing glyph by glyph
        ivl = always_redraw(lambda: interval_tex(int(round(level.get_value()))).next_to(digits, DOWN, buff=0.3))
        with self.voiceover(
            "Decimal expansions are really a statement about nested intervals. <bookmark mark='a'/> Root two lies "
            "between 1 and 2; <bookmark mark='b'/> between 1.4 and 1.5; between 1.41 and 1.42, and so on: each digit "
            "picks one of ten smaller intervals inside the last one."
        ) as vo:
            self.play(Create(axis), FadeIn(labs), FadeIn(dust))
            vo.wait_until("a")
            self.play(FadeIn(band), FadeIn(digits), FadeIn(ivl))
            vo.wait_until("b")
            for k in range(1, 4):
                w = 1.2 / 10 ** (k - 0) if k else 1.2
                tgt = (lo[k] + 0.5) / 10**k
                self.play(*win.zoom_to(tgt, 12 / 10 ** (k + 1)), level.animate.set_value(k), digits_shown.animate.set_value(k), run_time=1.4)
        with self.voiceover(
            "Keep zooming and the intervals keep shrinking, by a factor of ten each time, <bookmark mark='c'/> pinning "
            "down a single point."
        ) as vo:
            for k in range(4, 12):
                tgt = (lo[k] + 0.5) / 10**k
                self.play(*win.zoom_to(tgt, 12 / 10 ** (k + 1)), level.animate.set_value(k), digits_shown.animate.set_value(k), run_time=0.7)
        assert dec.startswith("1.41421356237")
        for m in (axis, labs, dust, band, digits, ivl):
            m.clear_updaters()
        self.play(FadeOut(VGroup(axis, labs, dust, band, ivl)), digits.animate.scale(0.8).to_corner(UL, buff=0.5))

        stmt = VGroup(label(r"\textbf{Nested intervals.} If $[a_1, b_1] \supset [a_2, b_2] \supset \cdots$,", font_size=32),
                      label(r"then some $x$ lies in every $[a_n, b_n]$.", font_size=32)).arrange(DOWN, buff=0.15)
        stmt.move_to(UP * 2.35)
        pf = VGroup(MathTex(r"x = \sup\{a_1, a_2, a_3, \ldots\}", font_size=36),
                    label(r"exists: every $b_m$ is an upper bound of the $a_n$; \ and $a_n \le x \le b_n$ for all $n$.",
                          font_size=28, color=GREY_A)).arrange(DOWN, buff=0.2).next_to(stmt, DOWN, buff=0.4)
        # five nested closed intervals on [0, 1]: left ends climb, right ends fall, both toward x = sup a_n
        nl1 = number_line(0, 1, y=-2.75, step=0.25)
        X1 = nl1.X
        x_star = 0.58
        an = [x_star - 0.5 * 0.55 ** k for k in range(5)]
        bn = [x_star + 0.4 * 0.6 ** k for k in range(5)]
        assert all(a1 < a2 for a1, a2 in zip(an, an[1:])) and all(b1 > b2 for b1, b2 in zip(bn, bn[1:]))
        assert all(a < x_star < b for a, b in zip(an, bn)) and an[0] >= 0 and bn[0] <= 1
        nest = VGroup()
        for k, (a, b) in enumerate(zip(an, bn)):
            yk = -0.55 - 0.38 * k
            nest.add(VGroup(Line([X1(a), yk, 0], [X1(b), yk, 0], color=C.COMPACT_SET, stroke_width=6),
                            endpoint([X1(a), yk, 0], True, C.COMPACT_SET), endpoint([X1(b), yk, 0], True, C.COMPACT_SET)))
        nest_l = MathTex(r"[a_1, b_1] \supset [a_2, b_2] \supset \cdots", font_size=26, color=C.COMPACT_SET)
        nest_l.next_to([X1(an[0]), -0.55, 0], UP, buff=0.12).align_to([X1(an[0]) - 0.1, 0, 0], LEFT)
        x_line = DashedLine([X1(x_star), -0.3, 0], [X1(x_star), -2.68, 0], color=C.EPS, stroke_width=3)
        x_l = MathTex(r"x", font_size=32, color=C.EPS).next_to([X1(x_star), -0.3, 0], UP, buff=0.08)
        with self.voiceover(
            "That a point is actually there is, again, the least-upper-bound property. <bookmark mark='s'/> If closed "
            "intervals are nested, each inside the last, <bookmark mark='p'/> then the left endpoints are bounded above "
            "by every right endpoint, so they have a supremum x, and x lies in every interval."
        ) as vo:
            vo.wait_until("s")
            self.play(FadeIn(stmt), Create(nl1))
            self.play(LaggedStart(*[FadeIn(n_, shift=DOWN * 0.1) for n_ in nest], lag_ratio=0.3), FadeIn(nest_l),
                      run_time=1.8)
            vo.wait_until("p")
            self.play(FadeIn(pf), Create(x_line), FadeIn(x_l))
        self.wait(0.2)
        self.play(FadeOut(VGroup(nest, nest_l, x_line, x_l, nl1)))
        nl = number_line(0, 1, y=-3.0, step=0.25)
        X = nl.X
        # (0, 1/n), stacked: nested, never empty, and nothing is in all of them
        bars = VGroup()
        for k in range(6):
            yk = -2.5 + 0.2 * k
            bars.add(VGroup(Line([X(0), yk, 0], [X(1 / (k + 1)), yk, 0], color=C.OPEN_SET, stroke_width=6),
                            endpoint([X(0), yk, 0], False, C.OPEN_SET, radius=0.06),
                            endpoint([X(1 / (k + 1)), yk, 0], False, C.OPEN_SET, radius=0.06)))
        zero_ring = endpoint([X(0), -3.0, 0], False, C.PATHOLOGY, radius=0.1)
        zero_l = label(r"$0 \notin$ any of them", font_size=24, color=C.PATHOLOGY)
        zero_l.move_to([0, -3.35, 0]).align_to([X(0) + 0.3, 0, 0], LEFT)  # on the tick-label row, right of "0"
        warn = VGroup(label(r"Both words matter: \ $(0, \tfrac1n)$ are nested and never empty, but", font_size=28),
                      MathTex(r"\bigcap_{n} \big(0, \tfrac1n\big) = \emptyset", font_size=36, color=C.PATHOLOGY)).arrange(DOWN, buff=0.2)
        warn.next_to(pf, DOWN, buff=0.35)
        with self.voiceover(
            "Both hypotheses matter. <bookmark mark='o'/> The open intervals from zero to one over n are nested and "
            "never empty, but no number lies in all of them: zero is excluded from each, and anything positive is "
            "eventually left out. <bookmark mark='q'/> And in the rationals, the decimal intervals of root two have no "
            "fraction in common."
        ) as vo:
            vo.wait_until("o")
            self.play(Create(nl), FadeIn(warn))
            self.play(LaggedStart(*[FadeIn(b_, shift=DOWN * 0.1) for b_ in bars], lag_ratio=0.4), run_time=2.4)
            self.play(FadeIn(zero_ring, scale=2), FadeIn(zero_l))
            vo.wait_until("q")
            self.play(Indicate(digits, color=C.HOLE))
        self.wait(0.3)
        self.clear_scene()

        d2 = load("sqrt2")
        A, B = d2["bis_a"], d2["bis_b"]
        nl = number_line(1.0, 2.0, y=1.0, step=0.25)
        X = nl.X
        title = label(r"The bisection engine", font_size=34).to_edge(UP, buff=0.3)
        sub = label(r"halve the interval; keep the half where $t^2 - 2$ changes sign", font_size=28, color=GREY_A)
        sub.next_to(title, DOWN, buff=0.2)
        rows = VGroup()
        bars = VGroup()
        for k in range(7):
            yb = 0.3 - 0.36 * k
            bars.add(VGroup(Line([X(A[k]), yb, 0], [X(B[k]), yb, 0], color=C.COMPACT_SET, stroke_width=7),
                            Dot([X(A[k]), yb, 0], radius=0.05, color=C.COMPACT_SET),
                            Dot([X(B[k]), yb, 0], radius=0.05, color=C.COMPACT_SET)))
        uses = label(r"It will prove: the intermediate value theorem, Bolzano--Weierstrass, Heine--Borel, \ldots",
                     font_size=26, color=C.EPS).to_edge(DOWN, buff=0.45)
        assert all(A[k] ** 2 < 2 < B[k] ** 2 for k in range(len(A)))
        with self.voiceover(
            "Halving instead of cutting into tenths gives the same thing with a clearer rule: <bookmark mark='h'/> split "
            "the interval in two and keep the half that still contains the point you're hunting, here the half where t "
            "squared minus two changes sign. <bookmark mark='u'/> This bisection engine will prove a surprising number "
            "of theorems in this series: the intermediate value theorem, Bolzano–Weierstrass, Heine–Borel, and more. "
            "Every time, the least-upper-bound property guarantees there's a point at the bottom of the funnel."
        ) as vo:
            self.play(FadeIn(title), FadeIn(sub), Create(nl))
            vo.wait_until("h")
            self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.1) for b in bars], lag_ratio=0.5), run_time=3.5)
            vo.wait_until("u")
            self.play(FadeIn(uses))
        self.wait(0.6)
        self.clear_scene()
