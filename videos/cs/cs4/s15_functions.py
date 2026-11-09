from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs4.common import BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, load, sci


class Functions(VoiceoverScene):
    def construct(self):
        self.card()
        self.reduce()
        self.minimax()
        self.cordic()
        self.cordic_table()

    def card(self):
        card = chapter_card(14, r"Computing sin, exp and log", r"How does a chip compute a sine?", lit=(1959, 1972),
                            part=PART)
        with self.voiceover("Chapter fourteen. Computing sine, exp and log."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def reduce(self):
        head = label(r"Step one: \ make the argument small", font_size=38).to_edge(UP, buff=0.35)
        e1 = MathTex(r"e^x = 2^k \cdot e^r, \qquad x = k \ln 2 + r, \quad |r| \le \tfrac{\ln 2}{2}", font_size=38,
                     color=CODE).move_to(UP * 1.6)
        e1n = label(r"$2^k$: \ adjust exponent for normal, in-range results", font_size=24, color=GREY_A).next_to(e1, DOWN,
                                                                                                   buff=0.2)
        e2 = MathTex(r"\sin x = \pm \sin r \text{ or } \pm \cos r, \qquad x = k \tfrac{\pi}{2} + r, \quad |r| \le "
                     r"\tfrac{\pi}{4}", font_size=38, color=CODE).move_to(DOWN * 0.3)
        e2n = label(r"for $x = 10^{22}$, \ $k\pi/2$ must be subtracted with about 130 correct bits of $\pi$ \ "
                    r"(Payne and Hanek, 1983)", font_size=24, color=NO).next_to(e2, DOWN, buff=0.2)
        e3 = MathTex(r"\log x = e \ln 2 + \log 1.f", font_size=38, color=CODE).move_to(DOWN * 2.2)
        e3n = label(r"the float's own fields do the reduction", font_size=24, color=GREY_A).next_to(e3, DOWN, buff=0.2)
        with self.voiceover(
            "A chip can only add, multiply and divide, so every other function must be built from those. The first "
            "step is always to make the argument small. <bookmark mark='a'/> For the exponential, write x as k times "
            "log two plus a small remainder r; then e to the x is two to the k times e to the r, and multiplying by two "
            "to the k adjusts the exponent for normal, in-range results. Subnormal rounding and overflow need special handling. <bookmark mark='b'/> For the sine, subtract a multiple of pi "
            "over two, and the problem becomes a sine or cosine of something less than pi over four. It sounds easy, "
            "but for an argument like ten to the twenty-two, the subtraction needs pi to over a hundred bits, or the "
            "remainder is pure noise; Mary Payne and Robert Hanek showed how to do it in 1983. "
            "<bookmark mark='c'/> For the logarithm, the float's own exponent field already did most of the work."
        ) as vo:
            self.play(FadeIn(head), FadeIn(e1))
            vo.wait_until("a")
            self.play(Indicate(e1, scale_factor=1.02), FadeIn(e1n))
            vo.wait_until("b")
            self.play(Write(e2), FadeIn(e2n))
            vo.wait_until("c")
            self.play(Write(e3), FadeIn(e3n))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def minimax(self):
        r = load("functions")["remez"]
        head = label(r"Step two: \ the best polynomial, \ not Taylor's", font_size=36).to_edge(UP, buff=0.3)
        x = np.array(r["x"])
        et, em = np.array(r["err_taylor"]), np.array(r["err_minimax"])
        sc = 1e5
        ax = Axes(x_range=[r["a"], r["b"], 0.1], y_range=[-4, 5, 1], x_length=6.0, y_length=4.6, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18}).move_to(LEFT * 3.6 + DOWN * 0.6)
        yl = VGroup(*[MathTex(rf"{k}", font_size=18, color=GREY_B).next_to(ax.c2p(r["a"], k), LEFT, buff=0.1)
                      for k in range(-4, 6)])
        ylab = note(r"error \ $\times 10^{-5}$", font_size=20).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        xlab = VGroup(MathTex(r"-\tfrac{\ln 2}{2}", font_size=22, color=GREY_B).next_to(ax.c2p(r["a"], -4), DOWN, buff=0.1),
                      MathTex(r"\tfrac{\ln 2}{2}", font_size=22, color=GREY_B).next_to(ax.c2p(r["b"], -4), DOWN, buff=0.1))
        ct = VMobject(color=NO, stroke_width=3).set_points_as_corners([ax.c2p(a, b * sc) for a, b in zip(x, et)])
        cm = VMobject(color=YES, stroke_width=3).set_points_as_corners([ax.c2p(a, b * sc) for a, b in zip(x, em)])
        tl = label(rf"Taylor, degree {r['deg']}: \ max error ${sci(r['max_taylor'])}$", font_size=26, color=NO)
        ml = label(rf"minimax, degree {r['deg']}: \ ${sci(r['max_minimax'])}$", font_size=26, color=YES)
        keys = VGroup(tl, ml).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 0.6 + UP * 1.6, aligned_edge=LEFT)
        notes = VGroup(
            label(r"Taylor is perfect at 0, \ and worst at the ends", font_size=24, color=GREY_A),
            label(r"the minimax error \textit{equioscillates}: \\ it touches its maximum $\deg + 2$ times, \ "
                  r"alternating in sign", font_size=24, color=GREY_A),
            label(rf"{r['max_taylor'] / r['max_minimax']:.0f} times smaller, \ for the same five coefficients",
                  font_size=26, color=HEAD),
            note(r"computed by Remez's exchange algorithm \ (1934)", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 0.6 + DOWN * 1.0, aligned_edge=LEFT)
        with self.voiceover(
            "On the small interval, a polynomial does the rest, and the obvious choice, the Taylor series, is the "
            "wrong one. <bookmark mark='a'/> Here is the error of e to the x minus its degree-four Taylor polynomial, "
            "on the reduced interval. It is perfect at zero and worst at the ends, about four times ten to the minus "
            "five. <bookmark mark='b'/> The best polynomial of the same degree, the one that minimizes the largest "
            "error, spreads its error evenly. Its error curve touches its maximum six times, alternating in sign: "
            "Chebyshev's equioscillation theorem says that is exactly what the best polynomial looks like. "
            "<bookmark mark='c'/> With the same five coefficients, the error is seventeen times smaller. Evgeny Remez's "
            "exchange algorithm, from 1934, finds it. Libraries often use near-minimax polynomials, with coefficient "
            "rounding constraints, tables or rational approximations. Our degree-four polynomial can use "
            "Horner's rule: four multiplications and four additions."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yl), FadeIn(ylab), FadeIn(xlab))
            vo.wait_until("a")
            self.play(Create(ct), FadeIn(tl), FadeIn(notes[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(cm), FadeIn(ml), FadeIn(notes[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]), FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cordic(self):
        d = load("functions")["cordic"]
        st = d["steps"]
        head = label(r"CORDIC: \ rotations made of shifts and adds", font_size=36).to_edge(UP, buff=0.3)
        c0 = LEFT * 3.0 + DOWN * 1.4
        R = 3.0
        arc = Arc(radius=R, start_angle=0, angle=PI / 2, color=GREY_D, stroke_width=2, arc_center=c0)
        axes = VGroup(Line(c0, c0 + RIGHT * (R + 0.3), color=GREY_C), Line(c0, c0 + UP * (R + 0.3), color=GREY_C))
        target = DashedLine(c0, c0 + R * np.array([np.cos(d["theta"]), np.sin(d["theta"]), 0]), color=HEAD)
        tl = MathTex(r"\theta = 1", font_size=26, color=HEAD).next_to(target.get_end(), UR, buff=0.05)
        K = d["K"]
        vecs = []
        for s in st[:8]:
            p = np.array([s["x"], s["y"]]) * K
            vecs.append(Arrow(c0, c0 + R * np.array([p[0], p[1], 0]), buff=0, stroke_width=4, color=FUNC,
                              max_tip_length_to_length_ratio=0.06))
        rule = VGroup(
            MathTex(r"\begin{pmatrix} x' \\ y' \end{pmatrix} = \begin{pmatrix} x - d\, 2^{-i} y \\ y + d\, 2^{-i} x "
                    r"\end{pmatrix}", font_size=32, color=CODE),
            MathTex(r"z' = z - d \arctan 2^{-i}, \qquad d = \operatorname{sign}(z)", font_size=30, color=CODE),
            label(r"multiplying by $2^{-i}$ is a shift: \ no multiplier at all", font_size=24, color=YES),
            MathTex(rf"K = \prod_i \frac{{1}}{{\sqrt{{1 + 2^{{-2i}}}}}} = {K:.7f}", font_size=30, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 3.4 + UP * 0.4)
        with self.voiceover(
            "There is also a way to compute sines with no multiplier at all, born in a navigation computer. "
            "<bookmark mark='a'/> Start with a vector along the x axis, and the angle you "
            "want in a register z. <bookmark mark='b'/> At step i, rotate the vector by plus or minus the angle whose "
            "tangent is two to the minus i, whichever moves it towards the target, and subtract that angle from z. "
            "<bookmark mark='c'/> A rotation by such an angle needs only multiplications by two to the minus i, which "
            "are shifts, plus additions. The rotations stretch the vector by the same factor every time, whichever "
            "way they turn, so one constant, K, about zero point six one, fixes it at the end. "
            "<bookmark mark='d'/> Each step adds about one bit of accuracy. Jack Volder invented this in 1959 for the "
            "B-58 bomber's navigation computer, and it is called CORDIC."
        ) as vo:
            self.play(FadeIn(head), Create(axes), Create(arc), Create(target), FadeIn(tl))
            vo.wait_until("a")
            cur = vecs[0]
            self.play(GrowArrow(cur))
            vo.wait_until("b")
            for v in vecs[1:6]:
                self.play(Transform(cur, v), run_time=0.7)
            vo.wait_until("c")
            self.play(FadeIn(rule[0]), FadeIn(rule[1]))
            self.play(FadeIn(rule[2]), FadeIn(rule[3]))
            vo.wait_until("d")
            for v in vecs[6:]:
                self.play(Transform(cur, v), run_time=0.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cordic_table(self):
        d = load("functions")["cordic"]
        head = label(r"Sixteen steps, \ sixteen bits", font_size=38).to_edge(UP, buff=0.35)
        rows = VGroup()
        hdr = VGroup(*[MathTex(t, font_size=24, color=GREY_B) for t in (r"i", r"d", r"\arctan 2^{-i}", r"z \text{ left}")])
        rows.add(hdr)
        for s in d["steps"][:12]:
            rows.add(VGroup(MathTex(str(s["i"]), font_size=24, color=GREY_B),
                            MathTex("+" if s["d"] > 0 else "-", font_size=26, color=YES if s["d"] > 0 else NO),
                            MathTex(f"{s['atan']:.6f}", font_size=24, color=GREY_A),
                            MathTex(f"{s['z']:+.6f}", font_size=24, color=HEAD)))
        for i, r in enumerate(rows):
            for j, m in enumerate(r):
                m.move_to([-5.6 + [0, 1.0, 2.6, 4.6][j], 2.5 - 0.42 * i, 0])
        res = VGroup(
            MathTex(rf"\cos 1 \approx {d['cos']:.7f} \quad ({d['true'][0]:.7f})", font_size=30, color=YES),
            MathTex(rf"\sin 1 \approx {d['sin']:.7f} \quad ({d['true'][1]:.7f})", font_size=30, color=YES),
            label(r"after 16 steps; \ the true values in brackets", font_size=22, color=GREY_B),
            label(r"the HP-35 (1972), \ the first scientific pocket calculator, \\ computed its functions this way",
                  font_size=24, color=HIST),
            label(r"still inside FPGAs, \ radio chips \\ and small processors without a multiplier", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 0.4 + DOWN * 0.2, aligned_edge=LEFT)
        with self.voiceover(
            "Here is the run, for an angle of one radian. <bookmark mark='a'/> Each row turns the vector one way or "
            "the other by a smaller angle, and the angle left in z shrinks, roughly halving each time. "
            "<bookmark mark='b'/> After sixteen steps, the vector's coordinates give the cosine and the sine of one, "
            "right to about five decimal places, using nothing but shifts, additions and a small table of "
            "arctangents. <bookmark mark='c'/> The HP-35 of 1972, the first scientific pocket calculator, computed its "
            "functions with this kind of shift-and-add algorithm, and CORDIC is still used inside FPGAs, radio chips "
            "and small processors that have no multiplier."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.2), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(res[0]), FadeIn(res[1]), FadeIn(res[2]))
            vo.wait_until("c")
            self.play(FadeIn(res[3]), FadeIn(res[4]))
        self.wait(0.3)
        self.clear_scene()
