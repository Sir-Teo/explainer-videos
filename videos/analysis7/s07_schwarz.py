from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis7.common import cplot, load, plain_axes, polyline, square_axes, zcurve


def blaschke(z, a=0.5):
    return z * (z - a) / (1 - a * z)


class Schwarz(VoiceoverScene):
    def construct(self):
        self.card()
        self.lemma()
        self.automorphisms()
        self.three_lines()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(6, r"The Schwarz lemma and three lines", r"How much can a map of the disk stretch?", lit=(),
                            part=7)
        with self.voiceover("Chapter six: the maximum principle, used as a tool."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def lemma(self):
        d = load("schwarz")
        rs, imgs, d0 = d["rs"], d["imgs"], float(d["d0"])
        S = 4.6
        cx = square_axes([-1.05, 1.05, 0.5], [-1.05, 1.05, 0.5], S / 2.1).move_to([-3.6, -0.6, 0])
        img = cplot(cx, blaschke, (-1.05, 1.05), (-1.05, 1.05), mask=lambda Z: np.abs(Z) <= 1)
        u = cx.c2p(1, 0)[0] - cx.c2p(0, 0)[0]
        unit = Circle(radius=u, color=WHITE, stroke_width=2.5).move_to(cx.c2p(0, 0))
        cols = [C.SEQ, C.APPROX, C.EPS]
        rings = VGroup(*[DashedVMobject(Circle(radius=r * u, color=c, stroke_width=2).move_to(cx.c2p(0, 0)), num_dashes=40)
                         for r, c in zip(rs, cols)])
        ims = VGroup(*[zcurve(cx, w, c, 3.5) for w, c in zip(imgs, cols)])
        f_l = MathTex(r"f(z) = z\,\frac{z - \frac12}{1 - \frac12 z}", font_size=28).next_to(cx, UP, buff=0.15)
        rows = VGroup(
            label(r"\textbf{RCA 12.2} \ (Schwarz)", font_size=26),
            label(r"$f: D \to D$ holomorphic, \ $f(0) = 0$:", font_size=26),
            MathTex(r"|f(z)| \le |z|, \qquad |f'(0)| \le 1", font_size=34, color=C.EPS),
            label(r"equality anywhere only for a rotation $f(z) = \lambda z$", font_size=24, color=GREY_A),
            label(r"dashed: \ $|z| = 0.3, 0.6, 0.9$; \ solid: \ their images, \ inside", font_size=24),
            MathTex(rf"|f'(0)| = {d0:.4f}", font_size=30, color=C.EPS),
            label(r"proof: \ $g(z) = f(z)/z$ is holomorphic, \ and on $|z| = r$", font_size=22, color=GREY_A),
            label(r"$|g| \le 1/r$; \ maximum modulus, \ then $r \to 1$", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        rows[1].shift(UP * 0.06)
        rows.align_to(np.array([6.55 - rows.width, 0, 0]), LEFT).set_y(-0.5)
        assert rows.get_right()[0] <= 6.6 and rows.get_left()[0] > cx.get_right()[0] + 0.2
        assert np.all(np.abs(imgs) <= rs[:, None] + 1e-12) and abs(d0 - 0.5) < 1e-6
        head = label(r"A map of the disk that fixes the center can only pull points inward", font_size=34).to_edge(UP,
                                                                                                           buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Take a holomorphic map of the unit disk into itself that keeps the center fixed. "
            "<bookmark mark='b'/> The Schwarz lemma: it can't move any point farther from the center. Here, three "
            "circles and their images: each image stays inside its circle. And the derivative at zero is at most one "
            "in size; here it's one half. <bookmark mark='c'/> The proof is one line: f of z over z is holomorphic, "
            "and by the maximum principle it's at most one over r on the circle of radius r, so at most one in the "
            "limit. Only rotations achieve equality."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(img), Create(unit), FadeIn(f_l))
            vo.wait_until("b")
            self.play(FadeIn(rows[:4]), Create(rings), img.animate.set_opacity(0.35))  # the circles over a dimmed coloring
            self.play(Create(ims), FadeIn(rows[4]), run_time=2.0)
            self.play(FadeIn(rows[5]))
            vo.wait_until("c")
            self.play(FadeIn(rows[6:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def automorphisms(self):
        a = 0.5
        phi = lambda z: (z - a) / (1 - a * z)  # noqa: E731
        ax = square_axes([-1.05, 1.05, 1], [-1.05, 1.05, 1], 1.75).move_to([-4.75, -0.75, 0])
        bx = square_axes([-1.05, 1.05, 1], [-1.05, 1.05, 1], 1.75).move_to([-0.05, -0.75, 0])
        th = np.linspace(0, 2 * np.pi, 361)
        grid_a, grid_b = VGroup(), VGroup()
        for r in (0.2, 0.4, 0.6, 0.8, 1.0):
            z = r * np.exp(1j * th)
            grid_a.add(zcurve(ax, z, C.SEQ, 2 if r < 1 else 3))
            grid_b.add(zcurve(bx, phi(z), C.SEQ, 2 if r < 1 else 3))
        rr = np.linspace(0, 1, 120)
        for k in range(12):
            z = rr * np.exp(2j * np.pi * k / 12)
            grid_a.add(zcurve(ax, z, C.APPROX, 1.6))
            grid_b.add(zcurve(bx, phi(z), C.APPROX, 1.6))
        assert np.allclose(np.abs(phi(np.exp(1j * th))), 1) and abs(phi(a)) < 1e-15
        arrow = Arrow([-2.75, -0.75, 0], [-2.05, -0.75, 0], buff=0, color=GREY_B, stroke_width=4)
        def tag(axk, z, tex, color, fs=28):  # a point's name under the disk, with a dashed leader up to the point
            t = MathTex(tex, font_size=fs, color=color).next_to(axk.c2p(z.real, -1.05), DOWN, buff=0.12)
            return VGroup(DashedLine(axk.c2p(z.real, z.imag) + DOWN * 0.1, t.get_top() + UP * 0.05, color=color,
                                     stroke_width=1.5, dash_length=0.06), t)

        al = VGroup(Dot(ax.c2p(a, 0), radius=0.08, color=C.EPS), tag(ax, a + 0j, r"\alpha = 0.5", C.EPS))
        al_img = VGroup(Dot(bx.c2p(phi(a).real, phi(a).imag), radius=0.08, color=C.EPS),
                        tag(bx, phi(a), r"\varphi_\alpha(\alpha) = 0", C.EPS, 26))
        zero = VGroup(Dot(ax.c2p(0, 0), radius=0.06, color=WHITE))
        zero_img = VGroup(Dot(bx.c2p(phi(0j).real, phi(0j).imag), radius=0.06, color=WHITE))
        assert abs(phi(0j) + a) < 1e-15
        a_l = MathTex(r"\varphi_\alpha(z) = \frac{z - \alpha}{1 - \bar\alpha z}, \ \alpha = 0.5", font_size=28).move_to(
            [-2.4, 1.55, 0])
        rows = VGroup(
            label(r"\textbf{RCA 12.4--12.6}", font_size=24),
            label(r"$\varphi_\alpha$ maps $D$ onto $D$, \ the circle", font_size=22),
            label(r"onto itself, \ and $\alpha$ to $0$", font_size=22),
            label(r"every automorphism of $D$", font_size=22, color=C.EPS),
            label(r"is $\lambda\varphi_\alpha$, \ $|\lambda| = 1$", font_size=22, color=C.EPS),
            label(r"(Schwarz, \ applied to", font_size=22, color=GREY_A),
            label(r"$f \circ \varphi_\alpha^{-1}$)", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to([2.15, -0.6, 0], RIGHT, buff=0)
        head = label(r"The symmetries of the disk", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> The lemma pins down every symmetry of the disk. <bookmark mark='b'/> The map z minus "
            "alpha over one minus alpha bar z slides the point alpha to the center, keeps the circle on itself, and "
            "bends the polar grid into circles that are no longer concentric. <bookmark mark='c'/> Combined with "
            "rotations, these are all the conformal self-maps of the disk: apply Schwarz to any other and it must "
            "be a rotation."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(grid_a))
            vo.wait_until("b")
            self.play(FadeIn(al), FadeIn(zero))
            self.play(GrowArrow(arrow), FadeIn(a_l), TransformFromCopy(grid_a, grid_b), TransformFromCopy(al[0], al_img[0]),
                      TransformFromCopy(zero[0], zero_img[0]), run_time=2.5)
            self.play(FadeIn(al_img[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def three_lines(self):
        d = load("schwarz")
        xs, logM = d["xs"], d["logM"]
        F = lambda Z: np.exp(2 * Z) / (Z + 1) ** 2  # noqa: E731
        cx = square_axes([-0.3, 1.3, 0.5], [-2.0, 2.0, 1], 1.05).move_to([-5.6, -0.6, 0])
        img = cplot(cx, F, (0, 1), (-2.0, 2.0), px=300)
        lines = VGroup(*[Line(cx.c2p(x, -2), cx.c2p(x, 2), color=c, stroke_width=4) for x, c in
                         ((0, C.SEQ), (0.5, C.EPS), (1, C.APPROX))])
        s_l = MathTex(r"0 \le \mathrm{Re}\,z \le 1", font_size=26).next_to(cx, UP, buff=0.1)
        f_l = MathTex(r"f(z) = \frac{e^{2z}}{(z + 1)^2}", font_size=28).next_to(cx, DOWN, buff=0.1)
        bx = plain_axes([0, 1, 0.5], [-0.2, 0.7, 0.2], 3.7, 3.2, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-2.0, -0.5, 0])
        g = polyline(bx, xs, logM, color=C.EPS, stroke_width=3.5)
        chord = DashedLine(bx.c2p(0, logM[0]), bx.c2p(1, logM[-1]), color=WHITE, stroke_width=2)
        b_l = MathTex(r"\log M(x), \ \ M(x) = \sup_y |f(x + iy)|", font_size=26, color=C.EPS).next_to(bx, UP, buff=0.12)
        assert abs(xs[50] - 0.5) < 1e-12 and xs[0] == 0 and xs[-1] == 1
        mid = VGroup(Dot(bx.c2p(0, logM[0]), radius=0.07, color=C.SEQ), Dot(bx.c2p(0.5, logM[50]), radius=0.07, color=C.EPS),
                     Dot(bx.c2p(1, logM[-1]), radius=0.07, color=C.APPROX))
        rows = VGroup(
            label(r"\textbf{RCA 12.8} \ (three lines) \ $f$ bounded and", font_size=24),
            label(r"holomorphic on the strip: \ $\log M(x)$ is convex", font_size=24),
            MathTex(r"M(x) \le M(0)^{1 - x} M(1)^x", font_size=30, color=C.EPS),
            MathTex(rf"M(\tfrac12) = {math.exp(logM[50]):.4f} \le {math.exp((logM[0] + logM[-1]) / 2):.4f}", font_size=26),
            label(r"(Phragm\'en--Lindel\"of: \ boundedness can be", font_size=22, color=GREY_A),
            label(r"relaxed, \ not dropped \ (12.7--12.9))", font_size=22, color=GREY_A),
            label(r"the payoff: \ Riesz--Thorin interpolation,", font_size=22, color=C.INNER),
            label(r"$\|T\|_{p_t} \le \|T\|_{p_0}^{1 - t}\|T\|_{p_1}^t$; \ Hausdorff--Young in Part 9", font_size=22,
                  color=C.INNER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to([0.75, -0.5, 0], RIGHT, buff=0)
        assert rows.get_right()[0] <= 6.6
        assert np.all(logM <= (1 - xs) * logM[0] + xs * logM[-1] + 1e-12)
        head = label(r"The maximum principle on a strip: \ three lines", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> The maximum principle has a quantitative cousin on a strip. Let M of x be the "
            "largest size of f on the vertical line at x. <bookmark mark='b'/> Hadamard's three lines theorem: the "
            "log of M is a convex function of x. Here it lies below its chord, so the size in the middle is at most "
            "the geometric mean of the sizes on the two edges. <bookmark mark='c'/> On an unbounded strip some growth "
            "condition is needed, which is what Phragmén and Lindelöf made precise. <bookmark mark='d'/> The payoff "
            "comes later: Riesz and Thorin turned this into interpolation of operator norms between L p spaces, and "
            "Part 9 uses it for the Fourier transform."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(img), FadeIn(s_l), FadeIn(f_l))
            self.play(Create(lines))
            vo.wait_until("b")
            self.play(Create(bx), FadeIn(b_l), Create(g), run_time=2.0)
            self.play(Create(chord), FadeIn(mid), FadeIn(rows[:4]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4:6]))
            vo.wait_until("d")
            self.play(FadeIn(rows[6:]))
        self.wait(0.4)
        self.clear_scene()
