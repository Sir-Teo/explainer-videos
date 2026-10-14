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
        ax = square_axes([-1.2, 1.2, 1], [-1.2, 1.2, 1], 1.1).move_to([-5.15, 1.0, 0])
        bx = square_axes([-1.2, 1.2, 1], [-1.2, 1.2, 1], 1.1).move_to([-5.15, -2.0, 0])
        for a in (ax, bx):
            a.set_opacity(0.3)
        K1 = region(ax, 1.0, C.CONNECTED_SET)
        K2 = region(bx, 0.0, C.PATHOLOGY)
        p1, p2 = Dot(ax.c2p(0, 0), radius=0.07, color=WHITE), Dot(bx.c2p(0, 0), radius=0.07, color=WHITE)
        esc = Arrow(ax.c2p(0, 0), ax.c2p(1.25, 0), buff=0.05, color=C.EPS, stroke_width=3, tip_length=0.15)
        l1 = label(r"pole escapes", font_size=22, color=C.EPS).next_to(esc.get_end(), RIGHT, buff=0.1)
        l2 = label(r"pole trapped", font_size=22, color=C.PATHOLOGY).next_to(bx.c2p(1.25, 0), RIGHT, buff=0.1)
        # the errors on a log scale: plot log10(err) + 4, so the x-axis sits at 10^-4, the bottom of the plot
        sh = 4.0
        lh, la = np.log10(eh) + sh, np.log10(ea) + sh
        assert lh.min() > 0 and max(lh.max(), la.max()) < 4.6 and abs(math.log10(1.0) + sh - 4.0) < 1e-12
        cx = plain_axes([1, 8, 1], [0, 4.6, 1], 3.6, 3.8).move_to([0.45, -0.55, 0])
        xt = VGroup(*[MathTex(str(int(v)), font_size=20).next_to(cx.c2p(math.log2(v), 0), DOWN, buff=0.1)
                      for v in degs])
        yt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=20).next_to(cx.c2p(1, k + sh), LEFT, buff=0.1) for k in (0, -2, -4)])
        xl = label(r"degree of the polynomial", font_size=22, color=GREY_B).next_to(xt, DOWN, buff=0.15)
        yl = MathTex(r"\sup_K |1/z - p|", font_size=24, color=GREY_B).next_to(cx, UP, buff=0.1)
        gh = VGroup(polyline(cx, np.log2(degs), lh, color=C.CONNECTED_SET, stroke_width=3.5),
                    *[Dot(cx.c2p(math.log2(v), e), radius=0.06, color=C.CONNECTED_SET) for v, e in zip(degs, lh)])
        ga = VGroup(polyline(cx, np.log2(degs), la, color=C.PATHOLOGY, stroke_width=3.5),
                    *[Dot(cx.c2p(math.log2(v), e), radius=0.06, color=C.PATHOLOGY) for v, e in zip(degs, la)])
        floor = DashedLine(cx.c2p(1, sh), cx.c2p(8, sh), color=C.PATHOLOGY, stroke_width=1.5)  # sup >= 1 on the annulus
        side = VGroup(
            label(r"best polynomial fits of $1/z$", font_size=22, color=GREY_A),
            label(r"(least squares, \ computed):", font_size=22, color=GREY_A),
            MathTex(r"\text{horseshoe: } " + sci(float(eh[0]), 2) + r" \to " + sci(float(eh[-1]), 1), font_size=26,
                    color=C.CONNECTED_SET),
            MathTex(r"\text{annulus: } " + f"{ea[0]:.3f}" + r" \to " + f"{ea[-1]:.3f}", font_size=26, color=C.PATHOLOGY),
            label(r"why the annulus is hopeless:", font_size=22),
            MathTex(r"\oint_{|z| = 1}\Big(\frac1z - p\Big)dz = 2\pi i", font_size=26),
            label(r"so $\sup |1/z - p| \ge 1$ on the circle", font_size=22, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        side[1].shift(UP * 0.06)
        side.align_to(np.array([6.55 - side.width, 0, 0]), LEFT).set_y(-0.6)
        assert eh[-1] < 1e-3 and np.all(ea >= 1)
        assert side.get_right()[0] <= 6.6 and side.get_left()[0] > cx.get_right()[0] + 0.3
        assert l1.get_right()[0] < yt.get_left()[0] - 0.1 and l2.get_right()[0] < xt.get_left()[0]
        assert bx.get_bottom()[1] > -3.6 and xl.get_bottom()[1] > -3.65
        head = label(r"Can polynomials approximate $1/z$ uniformly on $K$?", font_size=34).to_edge(UP, buff=0.3)
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
            self.play(FadeIn(head), Create(ax), Create(bx), FadeIn(K1), FadeIn(K2), FadeIn(p1), FadeIn(p2))
            vo.wait_until("b")
            self.play(Indicate(K1, color=C.CONNECTED_SET, scale_factor=1.04), FadeIn(side[:2]))
            self.play(Create(cx), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), Create(gh), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(K2, color=C.PATHOLOGY, scale_factor=1.04))
            self.play(Create(ga), Create(floor), FadeIn(side[3]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[4:]))
            self.play(GrowArrow(esc), FadeIn(l1), FadeIn(l2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        ax = square_axes([-1.3, 2.3, 1], [-1.3, 1.3, 1], 1.4).move_to([-3.6, -0.55, 0])
        ax.set_opacity(0.3)
        K = region(ax, 1.0, C.CONNECTED_SET)
        # the cycle: the curve at distance d around K (arcs of radius 1 + d and 0.75 - d, the two ends of the
        # horseshoe pushed d into the gap, quarter circles of radius d at its four corners)
        d_, g_ = 0.12, 1.0
        q = np.linspace(0, np.pi / 2, 20)
        e1, e4 = np.exp(1j * g_), np.exp(-1j * g_)
        gam = np.concatenate([
            (1 + d_) * np.exp(1j * np.linspace(g_, 2 * np.pi - g_, 240)),
            e4 + d_ * e4 * np.exp(1j * q),  # corner e^{-i}: from outward to into the gap
            np.linspace(e4 + 1j * d_ * e4, 0.75 * e4 + 1j * d_ * e4, 12),
            0.75 * e4 + d_ * 1j * e4 * np.exp(1j * q),  # corner 0.75 e^{-i}: from the gap to inward
            (0.75 - d_) * np.exp(1j * np.linspace(2 * np.pi - g_, g_, 200)),
            0.75 * e1 - d_ * e1 * np.exp(1j * q),  # corner 0.75 e^{i}
            np.linspace(0.75 * e1 - 1j * d_ * e1, e1 - 1j * d_ * e1, 12),
            e1 - 1j * d_ * e1 * np.exp(1j * q),  # corner e^{i}
        ])
        tt = np.linspace(g_, 2 * np.pi - g_, 1500)  # the boundary of K, densely: the cycle keeps distance d from it
        bd = np.concatenate([np.exp(1j * tt), 0.75 * np.exp(1j * tt), np.linspace(0.75, 1, 300) * e1,
                             np.linspace(0.75, 1, 300) * e4])
        dist = np.abs(gam[:, None] - bd[None, :]).min(axis=1)
        assert np.abs(dist - d_).max() < 2e-3 and abs(gam[-1] - gam[0]) < 1e-9
        wnd = np.sum(np.diff(np.unwrap(np.angle(np.append(gam, gam[0]) - 0.875 * np.exp(1j * np.pi))))) / (2 * np.pi)
        assert abs(abs(wnd) - 1) < 1e-6  # it winds once around (a point of) K
        cyc = DashedVMobject(zcurve(ax, gam, WHITE, 2.5), num_dashes=70)
        cyc_l = MathTex(r"\Gamma", font_size=28).next_to(ax.c2p(-0.8, 0.8), UL, buff=0.05)
        seg = np.abs(np.diff(gam))
        arc = np.concatenate([[0], np.cumsum(seg)])
        ak = np.interp(np.linspace(0, arc[-1], 17)[:-1], arc, gam.real) + 1j * np.interp(
            np.linspace(0, arc[-1], 17)[:-1], arc, gam.imag)  # 16 points a_k, evenly spaced along the cycle
        akd = VGroup(*[Dot(ax.c2p(z.real, z.imag), radius=0.05, color=C.EPS) for z in ak])
        poles = [0.0, 0.45, 0.9, 1.35, 1.8]
        pts = VGroup(*[Dot(ax.c2p(p, 0), radius=0.07, color=C.EPS) for p in poles])
        hops = VGroup(*[CurvedArrow(ax.c2p(a, 0.05), ax.c2p(b, 0.05), angle=-1.2, color=C.EPS, stroke_width=2.5,
                                    tip_length=0.12) for a, b in zip(poles[:-1], poles[1:])])
        out = DashedVMobject(Arrow(ax.c2p(1.85, 0), ax.c2p(2.35, 0), buff=0, color=C.EPS, stroke_width=2.5,
                                   tip_length=0.12), num_dashes=4)
        inf = MathTex(r"\infty", font_size=28, color=C.EPS).next_to(out, RIGHT, buff=0.08)
        far = label(r"$|b| > 1$: \ $\frac{1}{z - b}$ is a power series on $K \subset \{|z| \le 1\}$", font_size=22,
                    color=GREY_A).next_to(ax, DOWN, buff=0.08)
        sch = note(r"schematic").next_to(ax, DOWN, buff=0.45)
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
            self.play(*pm.light(0), Create(cyc), FadeIn(cyc_l))
            self.play(*pm.light(1), LaggedStart(*[FadeIn(a_) for a_ in akd], lag_ratio=0.08))
            vo.wait_until("c")
            self.play(*pm.light(2), FadeIn(pts[0]))
            for k in range(4):
                self.play(Create(hops[k]), FadeIn(pts[k + 1]), run_time=0.7)
            vo.wait_until("d")
            self.play(*pm.light(3), FadeIn(far), Create(out), FadeIn(inf))
            self.play(*pm.done())
        self.wait(0.4)
        self.clear_scene()
