from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import (ALPHA27, letter_row, load, plain_axes, surprise_color,
                                  surprise_legend, wrap_words)


class Surprise(VoiceoverScene):
    def construct(self):
        self.card()
        self.intuition()
        self.rules()
        self.derive()
        self.curve()
        self.halvings()
        self.skyline()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(2, r"How surprised to be",
                            r"If something had probability $p$, how much did seeing it tell you?", lit=(1948,), part=1)
        with self.voiceover("Chapter two. How surprised should you be?") as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def intuition(self):
        lt = load("letters")
        bg = load("bigram")
        p = lt["p"]
        pe, pz = float(p[ALPHA27.index("e")]), float(p[ALPHA27.index("z")])
        pu = float(bg["q_u"])
        k = 0.3  # screen units per bit
        line = NumberLine(x_range=[0, 1, 0.1], length=12, color=GREY_C, include_numbers=False).shift(DOWN * 1.2)
        ends = VGroup(MathTex("0", font_size=34, color=GREY_B).next_to(line.n2p(0), DOWN, buff=0.25),
                      MathTex("1", font_size=34, color=GREY_B).next_to(line.n2p(1), DOWN, buff=0.25))
        plab = MathTex("p", font_size=40, color=C.TRUE_P).next_to(line.n2p(0.5), DOWN, buff=0.3)
        head = label(r"how likely it was \ $\longrightarrow$ \ how much it tells you", font_size=38).to_edge(UP, buff=0.45)
        events = [
            (pu, r"\texttt{u} after \texttt{q}", r"no news", UP),
            (0.5, r"a coin lands heads", r"a little", UP),
            (pe, r"the next letter is \texttt{e}", r"some", RIGHT),
            (pz, r"the next letter is \texttt{z}", r"a lot", RIGHT),
        ]
        marks = VGroup()
        for v, name, how, side in events:
            s = math.log2(1 / v)
            d = glow_dot(line.n2p(v), color=C.TRUE_P, radius=0.08)
            h = max(k * s, 0.004)
            bar = Rectangle(width=0.36, height=h, stroke_width=0, fill_color=C.SURPRISE, fill_opacity=0.9)
            bar.move_to(line.n2p(v) + UP * (h / 2 + 0.1))
            t = label(name, font_size=28, color=WHITE)
            w = label(how, font_size=26, color=C.SURPRISE)
            g = VGroup(t, w).arrange(DOWN, buff=0.08, aligned_edge=LEFT if side is RIGHT else ORIGIN)
            if side is RIGHT:
                g.next_to(bar, RIGHT, buff=0.25).align_to(bar, UP)
            else:
                g.next_to(bar, UP, buff=0.2)
            marks.add(VGroup(d, bar, g))
        marks[2][2].shift(RIGHT * 0.15 + DOWN * 0.1)
        marks[0][2].shift(LEFT * 0.9)
        with self.voiceover(
            "If you were sure something would happen, seeing it happen tells you nothing. <bookmark mark='a'/> u "
            "after q: no news. <bookmark mark='b'/> A coin landing heads tells you a little. <bookmark mark='c'/> "
            "A letter e, a bit more. <bookmark mark='d'/> And a z, which turns up about once in two thousand "
            "symbols, tells you a lot. The less likely something was, the more you learn when it happens."
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(ends), FadeIn(plab))
            for j, mark in enumerate("abcd"):
                vo.wait_until(mark)
                d, bar, g = marks[j]
                self.play(FadeIn(d, scale=0.5), GrowFromEdge(bar, DOWN), FadeIn(g, shift=UP * 0.1), run_time=0.8)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rules(self):
        k = 0.75  # screen units per bit, on the number line
        pt = ValueTracker(0.25)
        line = NumberLine(x_range=[0, 1, 0.25], length=7.0, color=GREY_C, include_numbers=False).move_to([-2.8, -2.45, 0])
        nums = VGroup(*[MathTex(t, font_size=30, color=GREY_B).next_to(line.n2p(v), DOWN, buff=0.18)
                        for t, v in (("0", 0), (r"\tfrac12", 0.5), ("1", 1))])
        plab = MathTex("p", font_size=40, color=C.TRUE_P).next_to(line, RIGHT, buff=0.25)

        def s_of(v):
            return math.log2(1 / max(v, 1e-9))

        def bar_at(v):
            h = max(k * s_of(v), 0.002)
            return Rectangle(width=0.42, height=h, stroke_width=0, fill_color=C.SURPRISE, fill_opacity=0.9).move_to(
                line.n2p(v) + UP * (h / 2 + 0.1))

        dot = always_redraw(lambda: glow_dot(line.n2p(pt.get_value()), color=C.TRUE_P, radius=0.085))
        bar = always_redraw(lambda: bar_at(pt.get_value()))
        slab = always_redraw(lambda: MathTex(r"s(p)", font_size=34, color=C.SURPRISE).next_to(bar, UP, buff=0.12))
        items = [r"1.\ \ $s$ depends only on $p$", r"2.\ \ $s$ falls as $p$ rises; \ $s(1) = 0$",
                 r"3.\ \ independent events: \ $s(pq) = s(p) + s(q)$", r"4.\ \ $s$ is continuous"]
        rules = VGroup(*[label(t, font_size=30, color=C.BITS if j == 2 else WHITE) for j, t in enumerate(items)])
        rules.arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_corner(UL, buff=0.5)
        # a coin and a die: probabilities multiply, as areas
        side, gx, gy = 3.0, 4.45, 1.6
        cells = VGroup()
        for c in range(2):
            for r in range(6):
                cells.add(Rectangle(width=side / 2, height=side / 6, stroke_width=1.5, stroke_color=GREY_B)
                          .move_to([gx - side / 4 + c * side / 2, gy + side / 2 - side / 12 - r * side / 6, 0]))
        cols = VGroup(label(r"heads", font_size=24, color=GREY_A), label(r"tails", font_size=24, color=GREY_A))
        for c in range(2):
            cols[c].next_to(cells[6 * c], UP, buff=0.12)
        rows_l = VGroup(*[MathTex(str(r + 1), font_size=26, color=GREY_A).next_to(cells[r], LEFT, buff=0.15)
                          for r in range(6)])
        col_fill = Rectangle(width=side / 2, height=side, stroke_width=0, fill_color=C.TRUE_P, fill_opacity=0.28)
        col_fill.move_to([gx - side / 4, gy, 0])
        cell = cells[4].copy().set_stroke(width=0).set_fill(C.BITS, opacity=0.95)
        prod = mtex(r"\tfrac12 \times \tfrac16 = \tfrac1{12}", font_size=36, color=C.BITS).move_to([1.35, 0.55, 0])
        # surprises add, as lengths
        k2, base = 0.55, -2.35
        def seg(bits, color, x, y0):
            r = Rectangle(width=0.6, height=k2 * bits, stroke_width=0, fill_color=color, fill_opacity=0.92)
            return r.move_to([x, y0 + k2 * bits / 2, 0])
        s2, s6, s12 = 1.0, math.log2(6), math.log2(12)
        left_a = seg(s2, C.SURPRISE, 3.2, base)
        left_b = seg(s6, interpolate_color(ManimColor(C.SURPRISE), ManimColor(WHITE), 0.35), 3.2, base + k2 * s2)
        right = seg(s12, C.SURPRISE, 5.4, base)
        floor = Line([2.4, base, 0], [6.2, base, 0], color=GREY_C, stroke_width=1.5)
        same = DashedLine([2.75, base + k2 * s12, 0], [5.85, base + k2 * s12, 0], color=GREY_A, stroke_width=2)
        eqs = MathTex("=", font_size=44, color=GREY_A).move_to([4.3, base + k2 * s12 / 2, 0])
        lab_l = MathTex(r"s(\tfrac12) + s(\tfrac16)", font_size=28, color=C.SURPRISE).next_to(left_a, DOWN, buff=0.15)
        lab_r = MathTex(r"s(\tfrac1{12})", font_size=28, color=C.SURPRISE).next_to(right, DOWN, buff=0.15)
        with self.voiceover(
            "Let's turn that into mathematics. Call the surprise of an event with probability p, s of p. What "
            "should s be? <bookmark mark='a'/> Shannon asked for a few modest things. It should depend only on p. "
            "<bookmark mark='b'/> It should go down as p goes up, and a certain event should be no surprise at all. "
            "<bookmark mark='c'/> For independent events, surprises should add: <bookmark mark='d'/> a coin landing "
            "heads and a die showing five, together, should be exactly as surprising as each one, added up. "
            "<bookmark mark='e'/> And small changes in p should make small changes in s."
        ) as vo:
            self.play(Create(line), FadeIn(nums), FadeIn(plab))
            self.play(FadeIn(dot, scale=0.5), GrowFromEdge(bar, DOWN), FadeIn(slab))
            vo.wait_until("a")
            self.play(FadeIn(rules[0], shift=RIGHT * 0.15))
            self.play(pt.animate.set_value(0.6), run_time=1.0)
            self.play(pt.animate.set_value(0.25), run_time=1.0)
            vo.wait_until("b")
            self.play(FadeIn(rules[1], shift=RIGHT * 0.15))
            self.play(pt.animate.set_value(1.0), run_time=1.4)
            self.play(pt.animate.set_value(0.15), run_time=1.4)
            vo.wait_until("c")
            self.play(FadeIn(rules[2], shift=RIGHT * 0.15), Create(cells), FadeIn(cols), FadeIn(rows_l))
            self.play(FadeIn(col_fill), run_time=0.7)
            self.play(FadeIn(cell), Write(prod), pt.animate.set_value(1 / 12), run_time=1.2)
            vo.wait_until("d")
            self.play(Create(floor), GrowFromEdge(left_a, DOWN), run_time=0.7)
            self.play(GrowFromEdge(left_b, DOWN), FadeIn(lab_l), run_time=0.7)
            self.play(GrowFromEdge(right, DOWN), FadeIn(lab_r), run_time=0.8)
            self.play(Create(same), FadeIn(eqs))
            vo.wait_until("e")
            self.play(FadeIn(rules[3], shift=RIGHT * 0.15), pt.animate.set_value(0.3), run_time=1.2)
            for v in (0.33, 0.28, 0.3):
                self.play(pt.animate.set_value(v), run_time=0.45)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        ax = plain_axes([0, 6.4, 1], [0, 6.4, 1], 9.0, 5.0).shift(DOWN * 0.45 + LEFT * 0.3)
        xl = VGroup(*[MathTex(str(n), font_size=28, color=C.BITS).next_to(ax.c2p(n, 0), DOWN, buff=0.15)
                      for n in range(7)])
        pv = [r"1", r"\tfrac12", r"\tfrac14", r"\tfrac18", r"\tfrac1{16}", r"\tfrac1{32}", r"\tfrac1{64}"]
        pl = VGroup(*[MathTex(t, font_size=34, color=C.TRUE_P).next_to(xl[n], DOWN, buff=0.1) for n, t in enumerate(pv)])
        xname = MathTex(r"x", font_size=34, color=C.BITS).next_to(xl[0], LEFT, buff=0.55)
        pname = MathTex(r"p = 2^{-x}", font_size=30, color=C.TRUE_P).next_to(pl[0], LEFT, buff=0.3)
        gname = MathTex(r"g(x)", font_size=34, color=C.SURPRISE).next_to(ax.c2p(0, 6.4), LEFT, buff=0.15)
        axes = VGroup(ax, xl, pl, xname, pname, gname)
        S, Y = C.SURPRISE, C.BITS
        colors = {"g(x)": S, "g(y)": S, "g(x+y)": S, "g(n)": S, r"g(\tfrac{m}{n})": S, "s(2^{-x})": S, "s(p)": S,
                  r"\log_2 \tfrac{1}{p}": S, r"n\,": Y, r"\tfrac{m}{n}\,": Y, r"x\,": Y}
        steps = [
            [r"g(x)", "=", r"s(2^{-x})"],
            [r"g(x+y)", "=", r"g(x)", "+", r"g(y)"],
            [r"g(n)", "=", r"n\,", r"g(1)"],
            [r"g(\tfrac{m}{n})", "=", r"\tfrac{m}{n}\,", r"g(1)"],
            [r"g(x)", "=", r"x\,", r"g(1)"],
            [r"s(p)", "=", r"g(1)", r"\log_2 \tfrac{1}{p}"],
        ]
        eqs = [cmath(*st, colors=colors, font_size=52).move_to(UP * 3.15) for st in steps]
        head = label(r"Only one function does all that", font_size=30, color=GREY_A).to_corner(UL, buff=0.35)

        def vbar(x, h, color, w=0.16, y0=0.0):
            a, b = ax.c2p(x, y0), ax.c2p(x, y0 + h)
            return Rectangle(width=w, height=b[1] - a[1], stroke_width=0, fill_color=color, fill_opacity=0.92).move_to(
                (a + b) / 2)

        # rule 3 in pictures: a step of x halvings, then y more, and the surprises stack
        x0, y0 = 2.0, 1.5
        seg_x = Line(ax.c2p(0, 0), ax.c2p(x0, 0), color=C.BITS, stroke_width=7)
        seg_y = Line(ax.c2p(x0, 0), ax.c2p(x0 + y0, 0), color=C.CONTEXT, stroke_width=7)
        bx, by = vbar(x0, x0, C.SURPRISE), vbar(y0, y0, C.CONTEXT)
        bx_l = MathTex(r"g(x)", font_size=28, color=C.SURPRISE).next_to(bx, UP, buff=0.1)
        by_l = MathTex(r"g(y)", font_size=28, color=C.CONTEXT).next_to(by, UP, buff=0.1)
        stack_a = vbar(x0 + y0, x0, C.SURPRISE)
        stack_b = vbar(x0 + y0, y0, C.CONTEXT, y0=x0)
        st_l = MathTex(r"g(x+y)", font_size=28, color=WHITE).next_to(stack_b, UP, buff=0.1)
        additive = VGroup(seg_x, seg_y, bx, by, bx_l, by_l, stack_a, stack_b, st_l)
        # integers: n unit steps
        units = VGroup()
        for n in range(1, 7):
            units.add(VGroup(*[vbar(n, 1, interpolate_color(ManimColor(C.SURPRISE), ManimColor(C.BITS), (j % 2) * 0.35),
                                    w=0.2, y0=j) for j in range(n)]))
        int_dots = VGroup(*[glow_dot(ax.c2p(n, n), color=WHITE, radius=0.06, layers=3) for n in range(1, 7)])
        fr = sorted({m / n for n in range(2, 7) for m in range(1, 6 * n + 1) if m % n and m / n < 6.4})
        frac_dots = VGroup(*[Dot(ax.c2p(v, v), radius=0.04, color=C.BITS) for v in fr])
        gline = ax.plot(lambda x: x, x_range=[0, 6.4, 0.05], color=C.SURPRISE, stroke_width=5)
        with self.voiceover(
            "Remarkably, those rules leave only one choice. Measure probabilities in halvings: <bookmark mark='a'/> "
            "write p as two to the minus x, and let g of x be the surprise of that event. <bookmark mark='b'/> Rule "
            "three says g turns sums into sums. <bookmark mark='c'/> So g of n is n times g of one, for every whole "
            "number n, <bookmark mark='d'/> and the same holds for every fraction. <bookmark mark='e'/> Continuity "
            "fills in the numbers between the fractions, so g of x is x times g of one, for every x."
        ) as vo:
            self.play(FadeIn(head), Create(ax), LaggedStart(*[FadeIn(m) for m in pl], lag_ratio=0.1), FadeIn(pname))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in xl], lag_ratio=0.1), FadeIn(xname),
                      FadeIn(gname), Write(eqs[0]))
            vo.wait_until("b")
            morph(self, eqs[0], eqs[1])
            self.play(Create(seg_x), GrowFromEdge(bx, DOWN), FadeIn(bx_l), run_time=0.8)
            self.play(Create(seg_y), GrowFromEdge(by, DOWN), FadeIn(by_l), run_time=0.8)
            self.play(TransformFromCopy(bx, stack_a), TransformFromCopy(by, stack_b), FadeIn(st_l), run_time=1.2)
            vo.wait_until("c")
            morph(self, eqs[1], eqs[2], run_time=1.0)
            self.play(FadeOut(additive), LaggedStart(*[LaggedStart(*[GrowFromEdge(b, DOWN) for b in u], lag_ratio=0.3)
                                                       for u in units], lag_ratio=0.25), run_time=2.0)
            self.play(FadeIn(int_dots), run_time=0.5)
            vo.wait_until("d")
            morph(self, eqs[2], eqs[3], run_time=1.0)
            self.play(units.animate.set_opacity(0.25), LaggedStart(*[FadeIn(d, scale=0.3) for d in frac_dots],
                                                                     lag_ratio=0.02), run_time=2.0)
            vo.wait_until("e")
            morph(self, eqs[3], eqs[4], run_time=1.0)
            self.play(Create(gline), run_time=1.6)
        unit = cmath(r"s(p)", "=", r"\log_2 \tfrac{1}{p}", r"\ \text{bits}", colors=colors, font_size=56).move_to(UP * 3.15)
        box = SurroundingRectangle(unit, color=C.SURPRISE, buff=0.18, corner_radius=0.1)
        coin = glow_dot(ax.c2p(1, 1), color=WHITE, radius=0.09)
        coin_l = label(r"a fair coin: \ $1$ bit", font_size=28, color=WHITE).next_to(ax.c2p(1, 1), DR, buff=0.12)
        guide = DashedLine(ax.c2p(1, 1), ax.c2p(0, 1), color=GREY_B, stroke_width=2)
        yl = VGroup(*[MathTex(str(n), font_size=26, color=GREY_B).next_to(ax.c2p(0, n), LEFT, buff=0.12)
                      for n in range(1, 7)])
        with self.voiceover(
            "Put the probability back in, and the surprise must be a constant times the log of one over p. "
            "<bookmark mark='a'/> The constant just picks a unit. Choose it so that a fair coin flip carries "
            "exactly one unit, and call that unit a bit. The surprise of an event with probability p is log, base "
            "two, of one over p, bits."
        ) as vo:
            morph(self, eqs[4], eqs[5], run_time=1.2)
            self.play(Indicate(pl, color=C.TRUE_P, scale_factor=1.15), FadeOut(head))
            vo.wait_until("a")
            self.play(FadeIn(coin, scale=0.5), Create(guide), FadeIn(coin_l), FadeIn(yl))
            morph(self, eqs[5], unit, run_time=1.2)
            self.play(Create(box))
        self.wait(0.3)
        self.derived = dict(ax=ax, axes=axes, line=gline, rest=VGroup(units, int_dots, frac_dots, coin, coin_l, guide, yl),
                            unit=VGroup(unit, box))

    # ------------------------------------------------------------------
    def curve(self):
        lt = load("letters")
        bg = load("bigram")
        p = lt["p"]
        d = self.derived
        ax = plain_axes([0, 1, 0.25], [0, 12, 2], 9.0, 5.0).shift(DOWN * 0.45 + LEFT * 0.3)
        xl = VGroup(*[MathTex(t, font_size=28, color=C.TRUE_P).next_to(ax.c2p(v, 0), DOWN, buff=0.15)
                      for t, v in (("0", 0), ("0.5", 0.5), ("1", 1))])
        yl = VGroup(*[MathTex(str(v), font_size=26, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.15)
                      for v in (0, 4, 8, 12)])
        axl = VGroup(MathTex("p", font_size=36, color=C.TRUE_P).next_to(ax.c2p(1, 0), RIGHT, buff=0.2),
                     label(r"$s(p)$, bits", font_size=28, color=C.SURPRISE).next_to(ax.c2p(0, 12), UP, buff=0.15))
        bent = ParametricFunction(lambda t: ax.c2p(2.0 ** -t, t), t_range=[0, 6.4, 0.02], color=C.SURPRISE,
                                  stroke_width=5)
        tail = ParametricFunction(lambda t: ax.c2p(2.0 ** -t, t), t_range=[6.4, 12, 0.02], color=C.SURPRISE,
                                  stroke_width=5)
        pts = [
            (0.5, r"coin: \ $1$ bit", 1.0),
            (1 / 6, r"a die: \ $2.58$", 2.585),
            (float(p[ALPHA27.index("e")]), r"\texttt{e}: \ $3.32$", None),
            (float(p[ALPHA27.index("z")]), r"\texttt{z}: \ $10.9$", None),
            (float(bg["q_u"]), r"\texttt{u} after \texttt{q}: \ $0.002$", None),
        ]
        assert abs(-math.log2(pts[2][0]) - 3.32) < 0.01 and abs(-math.log2(pts[3][0]) - 10.9) < 0.05
        assert -math.log2(pts[4][0]) < 0.0025
        dots = VGroup()
        for v, t, _ in pts:
            dd = glow_dot(ax.c2p(v, -math.log2(v)), color=WHITE, radius=0.07, layers=3)
            lab = label(t, font_size=26).next_to(dd, UR, buff=0.02)
            dots.add(VGroup(dd, lab))
        dots[4][1].next_to(dots[4][0], UP, buff=0.25).shift(LEFT * 0.5)
        dots[3][1].next_to(dots[3][0], RIGHT, buff=0.15)
        with self.voiceover(
            "Here's that function. <bookmark mark='a'/> A coin: one bit. A face of a die: 2.58 bits. "
            "<bookmark mark='b'/> The letter e: 3.32 bits. The letter z: almost eleven. <bookmark mark='c'/> And u, "
            "right after q, carries two thousandths of a bit: almost nothing. <bookmark mark='d'/> As p heads to "
            "zero, the surprise grows without limit."
        ) as vo:
            self.play(FadeOut(d["rest"]), FadeOut(VGroup(*d["axes"][1:])),
                      d["unit"].animate.scale(0.6).to_corner(UR, buff=0.3))
            self.play(ReplacementTransform(d["ax"], ax), ReplacementTransform(d["line"], bent), FadeIn(xl), FadeIn(yl),
                      FadeIn(axl), run_time=2.0)
            self.play(Create(tail), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(dots[0]), FadeIn(dots[1]))
            vo.wait_until("b")
            self.play(FadeIn(dots[2]), FadeIn(dots[3]))
            vo.wait_until("c")
            self.play(FadeIn(dots[4]))
            vo.wait_until("d")
            self.play(Indicate(tail, color=C.BITS), run_time=1.2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def halvings(self):
        head = label(r"A bit is a halving", font_size=40).to_edge(UP, buff=0.4)
        W, y, H = 12.0, 1.3, 0.8
        rng = np.random.default_rng(11)
        choices = rng.integers(0, 2, 10)
        bar = Rectangle(width=W, height=H, stroke_width=0, fill_color=C.BITS, fill_opacity=0.95).move_to([0, y, 0])
        frame = Rectangle(width=W, height=H, stroke_width=2, stroke_color=GREY_B).move_to([0, y, 0])
        bits = VGroup(*[MathTex(str(int(c)), font_size=44, color=C.BIT1 if c else C.BIT0) for c in choices])
        bits.arrange(RIGHT, buff=0.34).move_to(DOWN * 0.9)
        mag_l = label(r"magnified", font_size=26, color=GREY_A)
        mag_x = MathTex(r"\times", font_size=34, color=GREY_A)
        mag_n = Integer(1, font_size=34, color=GREY_A)
        mag = VGroup(mag_l, mag_x, mag_n).arrange(RIGHT, buff=0.15).next_to(frame, UP, buff=0.25).align_to(frame, RIGHT)
        count = MathTex(r"10 \text{ halvings}: \ p = 2^{-10} = \tfrac{1}{1024} \ \Longrightarrow \ s = 10 \text{ bits}",
                        font_size=38).move_to(DOWN * 1.75)
        # the whole range, unmagnified, with the piece still in play
        ym = y - H / 2 - 0.45
        whole = Rectangle(width=W, height=0.14, stroke_width=1, stroke_color=GREY_C, fill_color=GREY_E, fill_opacity=0.6)
        whole.move_to([0, ym, 0])
        piece = Rectangle(width=W, height=0.14, stroke_width=0, fill_color=C.BITS, fill_opacity=0.95).move_to([0, ym, 0])
        whole_l = label(r"the whole range", font_size=22, color=GREY_B).next_to(whole, DOWN, buff=0.1).align_to(whole, LEFT)
        cap = label(r"each yes-or-no answer that halves the possibilities is one bit", font_size=28, color=GREY_A)
        cap.to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "Bits have a concrete meaning. Take the whole range of possibilities, and halve it: <bookmark mark='a'/> "
            "left or right, zero or one. Halve what's left, and again, ten times. <bookmark mark='b'/> You've "
            "narrowed things down to one part in 1024, an event of probability two to the minus ten, and the "
            "surprise of seeing it is ten bits. Each yes-or-no answer that halves the possibilities is one bit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bar), Create(frame), FadeIn(mag), FadeIn(whole), FadeIn(piece),
                      FadeIn(whole_l))
            vo.wait_until("a")
            lo, w = 0.0, 1.0
            for j, c in enumerate(choices):
                w /= 2
                lo += w * int(c)
                halves = [Rectangle(width=W / 2, height=H, stroke_width=0, fill_color=C.BITS, fill_opacity=0.95)
                          .move_to([(s - 0.5) * W / 2, y, 0]) for s in (0, 1)]
                keep, drop = halves[int(c)], halves[1 - int(c)]
                cut = Line([0, y - H / 2 - 0.12, 0], [0, y + H / 2 + 0.12, 0], color=WHITE, stroke_width=3)
                self.remove(bar)
                self.add(*halves)
                self.play(Create(cut), drop.animate.set_fill(GREY_E, 0.6), FadeIn(bits[j], shift=DOWN * 0.15),
                          run_time=0.25)
                self.play(FadeOut(drop), FadeOut(cut), keep.animate.stretch_to_fit_width(W).move_to([0, y, 0]),
                          ChangeDecimalToValue(mag_n, 2 ** (j + 1)),
                          piece.animate.stretch_to_fit_width(max(W * w, 0.004)).move_to([-W / 2 + (lo + w / 2) * W, ym, 0]),
                          run_time=0.3)
                bar = keep
            arrow = Arrow(piece.get_center() + DOWN * 0.6 + RIGHT * 0.6, piece.get_bottom(), buff=0.04, color=C.BITS,
                          stroke_width=3, max_tip_length_to_length_ratio=0.25)
            what = label(r"$\tfrac{1}{1024}$ of the bar", font_size=26, color=C.BITS).next_to(arrow.get_start(), RIGHT,
                                                                                         buff=0.1)
            vo.wait_until("b")
            self.play(GrowArrow(arrow), FadeIn(what), FadeOut(whole_l))
            self.play(Write(count))
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def skyline(self):
        g = load("game")
        sent, bits = g["sentence"], np.asarray(g["sentence_bits"])
        total = float(bits.sum())
        k = int(g["sentence_order"])
        assert abs(total - 182.2) < 0.1 and len(sent) == 101 and k == 5
        lines = wrap_words(sent, 36)
        rows = VGroup(*[letter_row(ln, font_size=27) for ln in lines]).arrange(DOWN, aligned_edge=LEFT, buff=1.5)
        rows.move_to(DOWN * 0.95)
        bars, i = VGroup(), 0
        for t, ln in zip(rows, lines):
            top = t.get_top()[1] + 0.08
            for j in range(len(ln)):
                b = float(bits[i])
                h = max(0.02, 0.115 * b)
                bars.add(Rectangle(width=0.2, height=h, stroke_width=0, fill_color=surprise_color(b), fill_opacity=1)
                         .move_to([t[j].get_x(), top + h / 2, 0]))
                i += 1
        letters = [m for t in rows for m in t]
        rule = mtex(r"\log_2 \frac{1}{P(x_1 \dots x_n)} = \sum_i \log_2 \frac{1}{P(x_i \mid x_{<i})}", font_size=38)
        rule.to_edge(UP, buff=0.35)
        tot = label(rf"total: \ ${total:.0f}$ bits for ${len(sent)}$ symbols \ $=$ \ ${total / len(sent):.2f}$ bits "
                    r"per symbol", font_size=30, color=C.BITS).to_edge(DOWN, buff=0.35)
        leg = surprise_legend(width=3.0).to_corner(DR, buff=0.4).shift(UP * 0.5)
        src = note(rf"each letter's surprise given the previous {k} letters, under a counting model of the $30$ books "
                   r"(Chapter 7); \ computed").next_to(rule, DOWN, buff=0.2)
        with self.voiceover(
            "And because logs turn products into sums, the chain rule turns into something lovely. "
            "<bookmark mark='a'/> The surprise of a whole text is the sum of the surprises of its symbols, each "
            "given everything before it. <bookmark mark='b'/> Here is Shannon's sentence again, with each letter's "
            "surprise drawn as a bar, as judged by a model that knows only the previous five letters."
        ) as vo:
            self.play(Write(rule))
            vo.wait_until("a")
            self.play(FadeIn(src))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in letters], lag_ratio=0.02), run_time=1.5)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02), FadeIn(leg), run_time=3)
        starts = np.array([i == 0 or sent[i - 1] == " " for i in range(len(sent))])
        assert bits[starts].mean() > 2 * bits[~starts].mean()  # the surprise is at the starts of words
        with self.voiceover(
            "The tall bars are where the text surprised the model: the starts of words, and words it didn't "
            "expect. <bookmark mark='a'/> Altogether, 182 bits for 101 symbols: 1.8 bits per symbol, under half of "
            "what the letter frequencies alone would give. Remember that number; it's how we'll keep score."
        ) as vo:
            self.play(*[Indicate(bars[j], color=WHITE, scale_factor=1.3) for j in range(len(sent)) if bits[j] > 4.4],
                      run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(tot, shift=UP * 0.1))
        self.wait(0.5)
        self.clear_scene()
