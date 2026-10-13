from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis7.common import load, square_axes, zcurve


class RiemannMapping(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.polygon()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(9, r"The Riemann mapping theorem", r"Is every simply connected region a disk in disguise?",
                            lit=(1854,), part=7)
        with self.voiceover("Chapter nine: the Riemann mapping theorem, computed for a real polygon."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def theorem(self):
        thm = VGroup(
            label(r"\textbf{RCA 14.8} \ (Riemann 1851; \ proof by Fej\'er and F.~Riesz, 1922, \ with Montel's theorem)",
                  font_size=26),
            label(r"every simply connected region $\Omega \ne \C$ is conformally equivalent to the disk $D$", font_size=28,
                  color=C.EPS),
        ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        pm = ProofMap([r"$\Sigma$ = one-to-one $\psi: \Omega \to D$, \ $\psi(z_0) = 0$: \ nonempty \ (a square root)",
                       r"maximize $|\psi'(z_0)|$ over $\Sigma$: \ Montel gives a maximizer",
                       r"if it missed a point of $D$, \ a square-root trick would beat it: \ so it is onto"],
                      font_size=20, width=4.0, buff=0.3).move_to([0, -0.4, 0])
        ideas = VGroup(
            label(r"the square root exists because $\Omega$ is simply connected \ (13.11)", font_size=22, color=GREY_A),
            label(r"the maximizer exists because the family is bounded: \ $|\psi| < 1$ \ (14.6)", font_size=22,
                  color=GREY_A),
            label(r"compactness again: \ an extremal problem with a solution", font_size=24, color=C.EPS),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> The Riemann mapping theorem: every simply connected region of the plane, other than "
            "the plane itself, can be mapped one-to-one and conformally onto the disk. <bookmark mark='b'/> The proof "
            "is an extremal problem. Look at all one-to-one maps of the region into the disk that send a chosen point "
            "to zero. There is one, built from a square root, which exists because the region is simply connected. "
            "<bookmark mark='c'/> Among them, pick the one with the largest derivative at the point. Montel's "
            "theorem guarantees a maximizer. <bookmark mark='d'/> And it must be onto: if it missed a point, another "
            "square-root trick would produce a map with a larger derivative. Compactness solves the extremal problem, "
            "and the solution is the map."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm))
            vo.wait_until("b")
            self.play(FadeIn(pm))
            self.play(*pm.light(0), FadeIn(ideas[0]))
            vo.wait_until("c")
            self.play(*pm.light(1), FadeIn(ideas[1]))
            vo.wait_until("d")
            self.play(*pm.light(2))
            self.play(*pm.done(), FadeIn(ideas[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def polygon(self):
        d = load("riemann")
        V, zs, rs, circles, angs, rays = d["V"], d["zs"], d["rs"], d["circles"], d["angs"], d["rays"]
        ang_err, bd, C0, d0 = float(d["ang_err"]), float(d["bd"]), complex(d["C"]), float(d["d0"])
        ax = square_axes([-1.1, 1.1, 1], [-1.1, 1.1, 1], 1.9).move_to([-4.5, -0.7, 0])
        bx = square_axes([-0.1, 2.1, 1], [-0.1, 2.1, 1], 1.9).move_to([0.6, -0.7, 0])
        for a in (ax, bx):
            a.set_opacity(0)
        th = np.linspace(0, 2 * np.pi, circles.shape[1])
        rr = np.linspace(0, 0.985, rays.shape[1])
        cols_c = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.INNER), k / (len(rs) - 1)) for k in range(len(rs))]
        disk = VGroup(*[zcurve(ax, r * np.exp(1j * th), c, 2) for r, c in zip(rs, cols_c)],
                      *[zcurve(ax, rr * np.exp(1j * a), C.APPROX, 1.4) for a in angs])
        image = VGroup(*[zcurve(bx, w, c, 2) for w, c in zip(circles, cols_c)],
                       *[zcurve(bx, w, C.APPROX, 1.4) for w in rays])
        unit = Circle(radius=ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0], color=WHITE, stroke_width=3).move_to(ax.c2p(0, 0))
        poly = Polygon(*[bx.c2p(v.real, v.imag) for v in V], color=WHITE, stroke_width=3)
        pre = VGroup(*[Dot(ax.c2p(z.real, z.imag), radius=0.08, color=C.EPS) for z in zs])
        corners = VGroup(*[Dot(bx.c2p(v.real, v.imag), radius=0.08, color=C.EPS) for v in V])
        c0 = VGroup(Dot(ax.c2p(0, 0), radius=0.07, color=WHITE), Dot(bx.c2p(C0.real, C0.imag), radius=0.07, color=WHITE))
        arrow = Arrow([-2.2, -0.7, 0], [-1.5, -0.7, 0], buff=0, color=GREY_B, stroke_width=4)
        f_l = MathTex(r"f", font_size=30, color=GREY_B).next_to(arrow, UP, buff=0.08)
        sc = MathTex(r"f(z) = A\!\int_0^z \prod_{k=1}^{6}\Big(1 - \frac{w}{z_k}\Big)^{\alpha_k - 1}dw + B", font_size=28)
        sc.to_edge(UP, buff=1.0)
        rows = VGroup(
            label(r"$\alpha_k\pi$ = the corner angles:", font_size=22),
            label(r"five of $\tfrac{\pi}{2}$, \ one of $\tfrac{3\pi}{2}$", font_size=22),
            label(r"prevertices $z_k$ solved for", font_size=22, color=GREY_A),
            label(r"(the side lengths must match)", font_size=22, color=GREY_A),
            MathTex(rf"f(0) = {C0.real:.1f} + {C0.imag:.1f}i", font_size=24),
            MathTex(rf"f'(0) = {d0:.4f} > 0", font_size=24),
            label(r"grid angles: \ $90^\circ$ to", font_size=22, color=C.EPS),
            MathTex(rf"{sci(ang_err, 0)} \text{{ degrees (200 points)}}", font_size=24, color=C.EPS),
            label(r"$|z| = 0.9999$ lands within", font_size=22, color=GREY_A),
            MathTex(rf"{bd:.4f} \text{{ of the boundary}}", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([5.3, -0.75, 0])
        for r_ in rows:
            if r_.width > 3.2:
                r_.width = 3.2
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([5.3, -0.75, 0])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([5.35, -0.75, 0])
        assert ang_err < 1e-4 and bd < 0.02
        head = label(r"The disk, mapped conformally onto an L-shaped hexagon \ (Schwarz--Christoffel)", font_size=30).to_edge(
            UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> The theorem says such a map exists; for a polygon we can compute it. Schwarz and "
            "Christoffel found its form: the derivative is a product of powers, one for each corner, with exponents "
            "set by the angles. <bookmark mark='b'/> The unknowns are the six points on the circle that go to the "
            "corners, solved for numerically so that the side lengths come out right. "
            "<bookmark mark='c'/> Here's the result. The polar grid of the disk flows onto the L-shaped hexagon: "
            "circles become nested loops, rays become curves that bend around the inner corner. "
            "<bookmark mark='d'/> Every little square stays a square: the grid lines meet at ninety degrees to within "
            "ten to the minus seven, and the center goes to the point 0.8 plus 0.8 i. Nothing about the theorem's "
            "proof constructs this map, but the map is really there."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(sc))
            self.play(Create(unit), Create(poly), Create(disk), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(pre, scale=1.5), FadeIn(corners, scale=1.5), FadeIn(rows[:4]))
            vo.wait_until("c")
            self.play(GrowArrow(arrow), FadeIn(f_l), FadeIn(c0))
            self.play(TransformFromCopy(disk, image), run_time=4.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[4:]))
        self.wait(0.4)
        self.clear_scene()
