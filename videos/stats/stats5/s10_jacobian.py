from __future__ import annotations

import numpy as np

from videos.stats.stats5.common import *  # noqa: F403


class Jacobian(VoiceoverScene):
    def construct(self):
        self.card()
        self.rule()
        self.convolution()
        self.ratio()
        self.polar()

    def card(self):
        card = chapter_card(9, r"Change of variables", r"Densities in many dimensions", lit=(), part=PART)
        with self.voiceover("Chapter nine. Change of variables in many dimensions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def rule(self):
        sq = Square(side_length=1.6, stroke_color=SIM, stroke_width=2.5, fill_color=SIM, fill_opacity=0.2).move_to([-4.2, -0.2, 0])
        par = Polygon([-1.5, -1.0, 0], [0.5, -0.4, 0], [1.3, 1.2, 0], [-0.7, 0.6, 0], stroke_color=COND, stroke_width=2.5,
                      fill_color=COND, fill_opacity=0.2).move_to([-0.8, -0.2, 0])
        arr = Arrow([-3.1, -0.2, 0], [-2.3, -0.2, 0], color=GREY_B, stroke_width=3)
        al = MathTex(r"\mathbf y = g(\mathbf x)", font_size=28).next_to(arr, UP, buff=0.1)
        la = MathTex(r"dA", font_size=30, color=SIM).move_to(sq)
        lb = MathTex(r"|\det J|\, dA", font_size=30, color=COND).move_to(par)
        rows = [
            cmath(r"f_{\mathbf Y}(\mathbf y)\, |\det J_g(\mathbf x)|\, dA", r"=", r"f_{\mathbf X}(\mathbf x)\, dA", font_size=30),
            cmath(r"f_{\mathbf Y}(\mathbf y)", r"=", r"f_{\mathbf X}\big(g^{-1}(\mathbf y)\big)\, \big|\det J_{g^{-1}}(\mathbf y)\big|",
                  font_size=32),
        ]
        rows[1][0].set_color(COND)
        whys = [why(r"$g$ smooth and one-to-one, $\det J\ne0$: conserve probability"), why(r"Part 3's rule, \ with a determinant")]
        intro = label('Conserve probability under a transformation', font_size=36)
        with self.voiceover(
            "Part 3 changed variables in one dimension and previewed the Jacobian. Here's the full picture. "
            "<bookmark mark='a'/> A transformation g maps a tiny square of area d A <bookmark mark='b'/> to a tiny "
            "parallelogram whose area is the absolute determinant of the Jacobian matrix times d A. "
            "<bookmark mark='c'/> Probability is conserved, so the density must shrink where areas grow: "
            "<bookmark mark='d'/> for a smooth one-to-one map with nonzero determinant, the new density is the old one at the preimage, times the absolute Jacobian determinant of the inverse. For multiple preimages we sum their contributions."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(sq), FadeIn(la))
            vo.wait_until("b")
            self.play(GrowArrow(arr), FadeIn(al), TransformFromCopy(sq, par), FadeIn(lb))
            step = ladder(self, rows, whys, keep=2, top=2.9, x=2.0, buff=0.6, edge=6.9)
            vo.wait_until("c")
            step(0, transform=False)
            vo.wait_until("d")
            step(1, transform=False)
        self.clear_scene()

    def convolution(self):
        d = load("jacobian")
        s = np.asarray(d["s"])
        A = axes([0, 2], [0, 1.15], x_length=5.6, y_length=3.6, xlabel=r"$U_1 + U_2$", xticks=[0, 0.5, 1, 1.5, 2],
                 yticks=[0, 0.5, 1], center=[-3.2, -0.8, 0])
        ax = A.ax
        ed = np.linspace(0, 2, 41)
        h = hist_bars(ax, ed, np.histogram(s, ed)[0] / (len(s) * np.diff(ed)), color=SIM)
        tri = VMobject(stroke_color=EXACT, stroke_width=3).set_points_as_corners([ax.c2p(0, 0), ax.c2p(1, 1), ax.c2p(2, 0)])
        rows = [
            cmath(r"(U_1, U_2)", r"\mapsto", r"(S, U_1) = (U_1 + U_2,\ U_1)", font_size=30),
            cmath(r"|\det J|", r"=", r"1", font_size=32),
            cmath(r"f_S(s)", r"=", r"\int f_{U_1}(u)\, f_{U_2}(s - u)\, du", font_size=32),
        ]
        rows[2][0].set_color(EXACT)
        whys = [why(r"add a coordinate to make the map invertible"), why(r"a shear keeps areas"),
                why(r"integrate it out: \ the convolution")]
        tag = note(r"simulated: 40,000 pairs of uniforms").to_corner(DL, buff=0.3)
        intro = label('A sum as a change of variables', font_size=36)
        with self.voiceover(
            "The distribution of a sum is a change of variables in disguise. <bookmark mark='a'/> Map the pair of "
            "uniforms to their sum and the first one: a shear, which keeps areas, so the Jacobian is one. "
            "<bookmark mark='b'/> Integrate out the extra coordinate, and the density of the sum is the "
            "convolution of the two densities, Part 2's polynomial multiplication, for continuous variables. "
            "<bookmark mark='c'/> For two uniforms it's a triangle, peaking at one: forty thousand simulated sums "
            "approximate it."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.9, x=2.6, buff=0.55, edge=6.9)
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            step(0, transform=False)
            step(1, transform=False)
            vo.wait_until("b")
            step(2, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(A), FadeIn(h), Create(tri), FadeIn(tag))
        self.clear_scene()

    def ratio(self):
        d = load("jacobian")
        r = np.asarray(d["ratio"])
        A = axes([-6, 6], [0, 0.36], x_length=6.0, y_length=3.4, xlabel=r"$Z_1 / Z_2$", xticks=[-6, -3, 0, 3, 6],
                 yticks=[0, 0.1, 0.2, 0.3], center=[-3.0, -0.8, 0])
        ax = A.ax
        ed = np.linspace(-6, 6, 61)
        h = hist_bars(ax, ed, np.histogram(r, ed)[0] / (len(r) * np.diff(ed)), color=SIM)
        xs = np.linspace(-6, 6, 300)
        cc = curve(ax, xs, 1 / (np.pi * (1 + xs ** 2)), EXACT, 3)
        rows = [
            cmath(r"(Z_1, Z_2)", r"\mapsto", r"(R, Z_2) = (Z_1/Z_2,\ Z_2)", font_size=30),
            cmath(r"f_R(r)", r"=", r"\int \phi(rz)\,\phi(z)\, |z|\, dz", r"=", r"\frac{1}{\pi(1 + r^2)}", font_size=30),
        ]
        rows[1][4].set_color(EXACT)
        whys = [why(r"$z_1 = r z_2$: \ Jacobian $|z_2|$"), why(r"the Cauchy, \ Part 3's lighthouse")]
        tag = note(r"simulated: 40,000 ratios (shown within $\pm 6$)").to_corner(DL, buff=0.3)
        intro = label('The ratio of two normals', font_size=36)
        with self.voiceover(
            "One more, with a famous answer. <bookmark mark='a'/> Take the ratio of two independent standard normals. "
            "Map the pair to the ratio and the denominator; now the Jacobian is the absolute value of the "
            "denominator. <bookmark mark='b'/> Integrate it out, and the ratio has density one over pi times one plus "
            "r squared: the Cauchy, Part 3's lighthouse, met from a different direction. A ratio of two perfectly "
            "ordinary variables has no mean at all, which is one reason ratios are dangerous statistics."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=2, top=2.9, x=2.4, buff=0.6, edge=6.9)
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            self.play(FadeIn(A), FadeIn(h), Create(cc), FadeIn(tag))
        self.clear_scene()

    def polar(self):
        e = load("extras")["rayleigh"]
        r = np.asarray(e["r"])
        rows = [
            cmath(r"(Z_1, Z_2)", r"\mapsto", r"(R, \Theta)", r",\quad", r"dz_1\, dz_2 = r\, dr\, d\theta", font_size=32),
            cmath(r"f_R(r)", r"=", r"\int_0^{2\pi} \frac{1}{2\pi} e^{-r^2/2}\, r\, d\theta", r"=", r"r\, e^{-r^2/2}", font_size=32),
        ]
        rows[1][4].set_color(EXACT)
        whys = [why(r"polar coordinates: \ the Jacobian is $r$"), why(r"the Rayleigh distribution")]
        A = axes([0, 4.5], [0, 0.7], x_length=5.6, y_length=3.0, xlabel=r"distance of a 2D normal point from the centre",
                 xticks=[0, 1, 2, 3, 4], yticks=[0, 0.3, 0.6], center=[-2.8, -1.8, 0])
        ax = A.ax
        ed = np.linspace(0, 4.5, 46)
        h = hist_bars(ax, ed, np.histogram(r, ed)[0] / (len(r) * np.diff(ed)), color=SIM)
        xs = np.linspace(0, 4.5, 200)
        cv = curve(ax, xs, xs * np.exp(-xs ** 2 / 2), EXACT, 3)
        info = VGroup(MathTex(rf"E R = \sqrt{{\pi/2}} = {e['theory']:.4f}", font_size=28, color=EXACT),
                      MathTex(rf"\text{{simulated: }} {e['mean']:.4f}", font_size=26, color=SIM),
                      label(r"in 3D: \ Maxwell's distribution of molecular speeds", font_size=22, color=GREY_B))
        info.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.6, -1.6, 0])
        tag = note(r"simulated: 20,000 points").to_corner(DR, buff=0.3)
        intro = label('A normal radius: the Rayleigh law', font_size=36)
        with self.voiceover(
            "Polar coordinates give one more classic. <bookmark mark='a'/> How far from the centre does a "
            "two-dimensional standard normal point land? Change to polar coordinates; the area element is r d r d "
            "theta, so the Jacobian is r. <bookmark mark='b'/> Integrate out the angle and the distance has density r "
            "times e to the minus r squared over two: the Rayleigh distribution, with mean root pi over two. Note that "
            "it's zero at the centre, even though the density of points is highest there: there's very little "
            "room near the centre. In three dimensions the same calculation gives Maxwell's distribution of "
            "molecular speeds."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=2, top=2.9, x=0.4, buff=0.6, edge=6.9)
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            self.play(FadeIn(A), FadeIn(h), Create(cv), FadeIn(info), FadeIn(tag))
        self.clear_scene()
