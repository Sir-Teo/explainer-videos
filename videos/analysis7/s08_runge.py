from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis7.common import load, plain_axes, polyline, square_axes, zcurve


def region(ax, gap, color):
    """The closed set K: the annulus 0.75 <= |z| <= 1, minus the sector |arg z| < gap (gap = 0: the full annulus)."""
    t = np.linspace(gap, 2 * np.pi - gap, 300)
    outer = [ax.c2p(math.cos(a), math.sin(a)) for a in t]
    inner = [ax.c2p(0.75 * math.cos(a), 0.75 * math.sin(a)) for a in t[::-1]]
    if gap > 0:
        return Polygon(*(outer + inner), stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.35)
    ring = VGroup(Circle(radius=ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0], color=color, stroke_width=2.5),
                  Circle(radius=ax.c2p(0.75, 0)[0] - ax.c2p(0, 0)[0], color=color, stroke_width=2.5))
    ann = AnnularSector(inner_radius=ax.c2p(0.75, 0)[0] - ax.c2p(0, 0)[0], outer_radius=ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0],
                        angle=2 * np.pi, fill_color=color, fill_opacity=0.35, stroke_width=0)
    return VGroup(ann, ring).move_to(ax.c2p(0, 0))


class Runge(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_sets()
        self.theorem()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(7, r"Runge's theorem", r"Which functions are limits of polynomials?", lit=(), part=7)
        with self.voiceover("Chapter seven: Runge's theorem, Weierstrass's approximation theorem for the complex "
                            "plane."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def two_sets(self):
        d = load("runge")
        degs, eh, ea = d["degs"], d["err_horse"], d["err_annulus"]
        ax = square_axes([-1.2, 1.2, 1], [-1.2, 1.2, 1], 1.35).move_to([-5.0, 0.5, 0])
        bx = square_axes([-1.2, 1.2, 1], [-1.2, 1.2, 1], 1.35).move_to([-5.0, -2.35, 0])
        for a in (ax, bx):
            a.set_opacity(0.3)
        K1 = region(ax, 1.0, C.CONNECTED_SET)
        K2 = region(bx, 0.0, C.PATHOLOGY)
        p1, p2 = Dot(ax.c2p(0, 0), radius=0.07, color=WHITE), Dot(bx.c2p(0, 0), radius=0.07, color=WHITE)
        esc = Arrow(ax.c2p(0, 0), ax.c2p(1.25, 0), buff=0.05, color=C.EPS, stroke_width=3, tip_length=0.15)
        l1 = label(r"the pole can escape", font_size=18, color=C.EPS).next_to(ax, RIGHT, buff=0.05).shift(UP * 0.3)
        l2 = label(r"trapped in the hole", font_size=18, color=C.PATHOLOGY).next_to(bx, RIGHT, buff=0.05).shift(UP * 0.3)
        cx = plain_axes([1, 8, 1], [-4.2, 0.6, 1], 3.9, 4.0).move_to([1.25, -0.7, 0])
        xt = VGroup(*[MathTex(str(int(v)), font_size=20).next_to(cx.c2p(math.log2(v), -4.2), DOWN, buff=0.1)
                      for v in degs])
        yt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=20).next_to(cx.c2p(1, k), LEFT, buff=0.1) for k in (0, -2, -4)])
        xl = label(r"degree of the polynomial", font_size=22, color=GREY_B).next_to(cx, DOWN, buff=0.45)
        yl = MathTex(r"\sup_K |1/z - p|", font_size=24, color=GREY_B).next_to(cx, UP, buff=0.1)
        gh = VGroup(polyline(cx, np.log2(degs), np.log10(eh), color=C.CONNECTED_SET, stroke_width=3.5),
                    *[Dot(cx.c2p(math.log2(v), math.log10(e)), radius=0.06, color=C.CONNECTED_SET) for v, e in zip(degs, eh)])
        ga = VGroup(polyline(cx, np.log2(degs), np.log10(ea), color=C.PATHOLOGY, stroke_width=3.5),
                    *[Dot(cx.c2p(math.log2(v), math.log10(e)), radius=0.06, color=C.PATHOLOGY) for v, e in zip(degs, ea)])
        floor = DashedLine(cx.c2p(1, 0), cx.c2p(8, 0), color=C.PATHOLOGY, stroke_width=1.5)
        side = VGroup(
            label(r"best polynomial fits of $1/z$ \ (least squares, \ computed)", font_size=22, color=GREY_A),
            MathTex(r"\text{horseshoe: } " + sci(float(eh[0]), 2) + r" \to " + sci(float(eh[-1]), 1), font_size=26,
                    color=C.CONNECTED_SET),
            MathTex(r"\text{annulus: } " + f"{ea[0]:.3f}" + r" \to " + f"{ea[-1]:.3f}", font_size=26, color=C.PATHOLOGY),
            label(r"why the annulus is hopeless:", font_size=22),
            MathTex(r"\oint_{|z| = 1}\Big(\frac1z - p\Big)dz = 2\pi i", font_size=26),
            label(r"so $\sup |1/z - p| \ge 1$ on the circle", font_size=22, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([5.6, -0.6, 0])
        for r_ in side:
            if r_.width > 3.45:
                r_.width = 3.45
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to([3.45, -0.6, 0], RIGHT, buff=0)
        assert eh[-1] < 1e-3 and np.all(ea >= 1)
        head = label(r"Can polynomials approximate $1/z$ uniformly on $K$?", font_size=34).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Can polynomials approximate one over z, uniformly on a compact set K that avoids "
            "zero? It depends on the shape of K. <bookmark mark='b'/> On a horseshoe, yes. The best fits improve "
            "steadily, from 1.5 at degree four to two ten-thousandths at degree one twenty-eight. "
            "<bookmark mark='c'/> On the full annulus, never: the error is stuck at 1.33 whatever the degree. "
            "<bookmark mark='d'/> The reason is an integral. Around the unit circle, one over z integrates to two pi i "
            "and every polynomial integrates to zero, so the difference can't be uniformly small. The pole at zero "
            "is trapped in the hole; in the horseshoe it can escape through the gap."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(bx), Create(cx), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("b")
            self.play(FadeIn(K1), FadeIn(p1), FadeIn(side[0]))
            self.play(Create(gh), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(K2), FadeIn(p2))
            self.play(Create(ga), Create(floor), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3:]))
            self.play(GrowArrow(esc), FadeIn(l1), FadeIn(l2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        ax = square_axes([-1.3, 2.3, 1], [-1.3, 1.3, 1], 1.4).move_to([-3.6, -0.8, 0])
        ax.set_opacity(0.3)
        K = region(ax, 1.0, C.CONNECTED_SET)
        poles = [0.0, 0.45, 0.9, 1.35, 1.8]
        pts = VGroup(*[Dot(ax.c2p(p, 0), radius=0.07, color=C.EPS) for p in poles])
        hops = VGroup(*[CurvedArrow(ax.c2p(a, 0.05), ax.c2p(b, 0.05), angle=-1.2, color=C.EPS, stroke_width=2.5,
                                    tip_length=0.12) for a, b in zip(poles[:-1], poles[1:])])
        far = label(r"far away: \ $\frac{1}{z - b}$ is a power series on $K$", font_size=20, color=GREY_A).next_to(
            ax.c2p(1.8, 0), DOWN, buff=0.35)
        sch = note(r"schematic").next_to(ax, DOWN, buff=0.05)
        pm = ProofMap([r"Cauchy's formula on a cycle around $K$",
                       r"a Riemann sum: \ $\sum_k \frac{c_k}{z - a_k}$, \ uniformly close",
                       r"push each pole $a_k$ step by step: \ $\frac{1}{z - a} = \sum_n \frac{(b - a)^n}{(z - b)^{n+1}}$",
                       r"out to $\infty$ if the complement is connected: \ polynomials"],
                      font_size=20, width=5.6, buff=0.2, direction=DOWN).move_to([3.3, -0.7, 0])
        thm = VGroup(label(r"\textbf{RCA 13.6, 13.7} \ (Runge, 1885) \ $K$ compact, \ $f$ holomorphic near $K$:",
                           font_size=26),
                     label(r"$f$ is a uniform limit on $K$ of rational functions with poles in a chosen point of each "
                           r"component of $S^2 \setminus K$", font_size=22, color=C.EPS),
                     label(r"if $\C \setminus K$ is connected: \ of polynomials", font_size=24, color=C.EPS)
                     ).arrange(DOWN, buff=0.08).to_edge(UP, buff=0.2)
        for r_ in thm:
            if r_.width > 13:
                r_.width = 13
        with self.voiceover(
            "<bookmark mark='a'/> That's Runge's theorem. A function holomorphic near a compact set K is a uniform "
            "limit of rational functions, with poles placed anywhere you like, one in each piece of the complement; "
            "if the complement is connected, polynomials suffice. <bookmark mark='b'/> The proof: Cauchy's formula "
            "on a cycle around K, approximated by a Riemann sum, gives a sum of simple poles. "
            "<bookmark mark='c'/> Then push each pole: a pole at a is a convergent series of poles at a nearby b, so "
            "it can hop, step by step, along a path in the complement. <bookmark mark='d'/> Out at infinity, a pole "
            "becomes a polynomial. Part 10 needs exactly this for its functional calculus."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm), Create(ax), FadeIn(K))  # the compact set K under the statement from the start
            vo.wait_until("b")
            self.play(FadeIn(pm), FadeIn(sch))
            self.play(*pm.light(0))
            self.play(*pm.light(1))
            vo.wait_until("c")
            self.play(*pm.light(2), FadeIn(pts[0]))
            for k in range(4):
                self.play(Create(hops[k]), FadeIn(pts[k + 1]), run_time=0.7)
            vo.wait_until("d")
            self.play(*pm.light(3), FadeIn(far))
            self.play(*pm.done())
        self.wait(0.4)
        self.clear_scene()
