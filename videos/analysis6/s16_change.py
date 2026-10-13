from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis6.common import heatmap, load, plain_axes, square_axes


class ChangeOfVariables(VoiceoverScene):
    def construct(self):
        self.card()
        self.polar()
        self.gaussian()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(15, r"Change of variables", r"How does a map change area?", lit=(), part=6)
        with self.voiceover("Chapter fifteen, a short one: changing variables in Lebesgue's integral."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def polar(self):
        d = load("polar")
        r0s, dr, dt, exact = d["r0"], float(d["dr"]), float(d["dt"]), d["exact_area"]
        ax = plain_axes([0, 3, 1], [0, 2 * math.pi, math.pi / 2], 2.6, 4.4).move_to([-5.0, -0.6, 0])
        tl = VGroup(MathTex(r"r", font_size=26, color=GREY_B).next_to(ax.c2p(3, 0), RIGHT, buff=0.12),
                    MathTex(r"\theta", font_size=26, color=GREY_B).next_to(ax.c2p(0, 2 * math.pi), UL, buff=0.08),
                    *[MathTex(str(k), font_size=18, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.1) for k in (1, 2, 3)],
                    *[MathTex(t_, font_size=18, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.12)
                      for t_, v in ((r"\tfrac{\pi}{2}", math.pi / 2), (r"\pi", math.pi), (r"\tfrac{3\pi}{2}", 1.5 * math.pi),
                                    (r"2\pi", 2 * math.pi))])
        grid1 = VGroup()
        for r_ in np.arange(0.25, 3.01, 0.25):
            grid1.add(Line(ax.c2p(r_, 0), ax.c2p(r_, 2 * math.pi), color=C.SEQ, stroke_width=1.2))
        for t_ in np.arange(dt, 2 * math.pi + 1e-9, dt):
            grid1.add(Line(ax.c2p(0, t_), ax.c2p(3, t_), color=C.APPROX, stroke_width=1.2))
        px = square_axes([-3.2, 3.2, 1], [-3.2, 3.2, 1], 0.68).move_to([0.0, -0.6, 0])
        px.set_opacity(0.3)
        grid2 = VGroup()
        for r_ in np.arange(0.25, 3.01, 0.25):
            grid2.add(Circle(radius=px.c2p(r_, 0)[0] - px.c2p(0, 0)[0], color=C.SEQ, stroke_width=1.2).move_to(
                px.c2p(0, 0)))
        for t_ in np.arange(0, 2 * math.pi - 1e-9, dt):
            grid2.add(Line(px.c2p(0, 0), px.c2p(3 * math.cos(t_), 3 * math.sin(t_)), color=C.APPROX, stroke_width=1.2))
        arrow = MathTex(r"\xrightarrow{\ T(r, \theta) = (r\cos\theta,\ r\sin\theta)\ }", font_size=26).move_to([-2.85, 1.85, 0])
        kT = ValueTracker(0)

        def patches():
            k = int(round(kT.get_value()))
            r0, t0 = float(r0s[k]), math.pi / 4
            src = Polygon(ax.c2p(r0, t0), ax.c2p(r0 + dr, t0), ax.c2p(r0 + dr, t0 + dt), ax.c2p(r0, t0 + dt),
                          stroke_color=C.EPS, stroke_width=3, fill_color=C.EPS, fill_opacity=0.5)
            th = np.linspace(t0, t0 + dt, 20)
            pts = [px.c2p(r0 * math.cos(a), r0 * math.sin(a)) for a in th]
            pts += [px.c2p((r0 + dr) * math.cos(a), (r0 + dr) * math.sin(a)) for a in th[::-1]]
            img = Polygon(*pts, stroke_color=C.EPS, stroke_width=3, fill_color=C.EPS, fill_opacity=0.5)
            return VGroup(src, img)

        pt = always_redraw(patches)

        def reads():
            k = int(round(kT.get_value()))
            r0 = float(r0s[k])
            return VGroup(
                MathTex(rf"r_0 = {r0:.2f}", font_size=28),
                MathTex(rf"\text{{area in }} (r, \theta): \ \Delta r\,\Delta\theta = {dr * dt:.4f}", font_size=26),
                MathTex(rf"\text{{area of the image}} = {exact[k]:.4f}", font_size=26, color=C.EPS),
                MathTex(rf"\text{{ratio}} = r_0 + \tfrac{{\Delta r}}{{2}} = {exact[k] / (dr * dt):.3f}", font_size=26,
                        color=C.EPS),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to([2.75, 0.9, 0], RIGHT, buff=0)

        rd = always_redraw(reads)
        assert np.allclose(exact / (dr * dt), r0s + dr / 2)
        thm = VGroup(
            label(r"$|\det T'(r, \theta)| = r$: \ the area factor", font_size=24, color=C.EPS),
            label(r"\textbf{RCA 7.26} \ $T$ one-to-one, \ differentiable:", font_size=24),
            MathTex(r"\int_{T(V)} f\,dm = \int_V (f \circ T)\, |J_T|\,dm", font_size=30, color=C.EPS),
            label(r"Part 4's area factors, \ now for Lebesgue measure", font_size=22, color=GREY_A),
        )
        for r_ in thm:
            if r_.width > 4.2:
                r_.width = 4.2
        thm.arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to([2.75, -1.75, 0], RIGHT, buff=0)
        head = label(r"Polar coordinates: \ a small rectangle becomes a curved patch $r$ times as large", font_size=30).to_edge(
            UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Polar coordinates map a rectangle of radii and angles onto a disk. Each little "
            "rectangle becomes a curved patch. <bookmark mark='b'/> Near the center the patches are small; far out "
            "they're large. The exact area of the image patch, divided by the area of the rectangle, is r zero plus "
            "half the step, <bookmark mark='c'/> and in the limit it's r: the determinant of the derivative, the "
            "area factor from Part 4. <bookmark mark='d'/> Rudin's change of variables theorem says this local "
            "factor is all that changes: integrate over the image, or integrate over the original region with the "
            "Jacobian factor, and you get the same Lebesgue integral."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(tl), Create(grid1), run_time=1.5)
            self.play(FadeIn(arrow), Create(px), Create(grid2), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(pt), FadeIn(rd))
            self.play(kT.animate.set_value(1), run_time=1.5)
            self.play(kT.animate.set_value(2), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(thm[0]))
            vo.wait_until("d")
            self.play(FadeIn(thm[1:]))
        for m in (pt, rd):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gaussian(self):
        d = load("polar")
        R, sq, disk, cart, pol = float(d["R"]), float(d["sq"]), float(d["disk"]), float(d["cart"]), float(d["pol"])
        S = 4.6
        ax = square_axes([-3, 3, 1], [-3, 3, 1], S / 6).move_to([-3.6, -0.6, 0])
        img = heatmap(lambda X, Y: np.exp(-X**2 - Y**2), (-3, 3), (-3, 3), S, S, -1, 1).move_to(ax.c2p(0, 0))
        circles = VGroup(*[Circle(radius=(ax.c2p(r_, 0)[0] - ax.c2p(0, 0)[0]), color=WHITE, stroke_width=1.2)
                           .move_to(ax.c2p(0, 0)).set_stroke(opacity=0.45) for r_ in (0.5, 1, 1.5, 2, 2.5, 3)])
        rows = VGroup(
            MathTex(r"\iint_{\R^2} e^{-(x^2 + y^2)}\,dx\,dy", font_size=32),
            MathTex(r"= \int_0^{2\pi}\!\!\int_0^\infty e^{-r^2}\, r\,dr\,d\theta = 2\pi \cdot \tfrac12 = \pi", font_size=30,
                    color=C.EPS),
            label(r"by Fubini, \ the left side is $\big(\int_\R e^{-x^2}dx\big)^2$, \ so", font_size=24, color=GREY_A),
            MathTex(r"\int_{-\infty}^{\infty} e^{-x^2}\,dx = \sqrt\pi", font_size=36, color=C.EPS),
            label(r"computed, \ on $[-3, 3]^2$ and the disk of radius 3:", font_size=22, color=GREY_A),
            MathTex(rf"\text{{square: }} {cart:.6f} \ (\pi\,\mathrm{{erf}}(3)^2 = {sq:.6f})", font_size=24),
            MathTex(rf"\text{{disk, with the factor }} r\text{{: }} {pol:.6f} \ (\pi(1 - e^{{-9}}) = {disk:.6f})",
                    font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.0, -0.5, 0])
        for r_ in rows:
            if r_.width > 6.6:
                r_.width = 6.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.0, -0.5, 0])
        assert abs(cart - sq) < 1e-6 and abs(pol - disk) < 1e-5 and disk < sq < math.pi
        head = label(r"The integral that has no antiderivative, \ computed by changing variables", font_size=32).to_edge(
            UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> The classic use. e to the minus x squared has no elementary antiderivative, but "
            "its square, the bell over the plane, is easy in polar coordinates. <bookmark mark='b'/> The factor r is "
            "exactly the derivative of minus a half e to the minus r squared, so the radial integral is one half, "
            "and the total is pi. <bookmark mark='c'/> By Fubini the double integral is the square of the single "
            "one, so the bell curve's integral is root pi. <bookmark mark='d'/> Checked numerically: on the square "
            "of side six, and on the disk of radius three with the factor r, both within a thousandth of pi."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(img), Create(ax), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(circles), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:4]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4:]))
        self.wait(0.4)
        self.clear_scene()
