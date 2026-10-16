from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis.analysis6.common import area_under, load, plain_axes, polyline


def h(t):
    return 1 + 0.8 * np.sin(4 * t)


class RadonNikodym(VoiceoverScene):
    def construct(self):
        self.card()
        self.ratios()
        self.theorem()
        self.von_neumann()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(11, r"The Radon--Nikodym theorem", r"When does one measure have a density with respect to "
                            r"another?", lit=(), part=6)
        with self.voiceover("Chapter eleven: densities, and the Radon-Nikodym theorem, proved with a Hilbert space."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def ratios(self):
        d = load("radon")
        pts, rs, ratios, hp = d["pts"], d["rs"], d["ratios"], d["hp"]
        ax = plain_axes([0, 1, 0.25], [0, 2, 0.5], 6.4, 3.6, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-2.8, -0.55, 0])
        x = np.linspace(0, 1, 600)
        area = area_under(ax, x, h(x), C.MEASURE, 0.22)
        gh = polyline(ax, x, h(x), color=C.MEASURE, stroke_width=3).set_stroke(opacity=0.0)
        gh_l = MathTex(r"h = \frac{d\lambda}{dm} \ ?", font_size=30, color=C.MEASURE).next_to(ax.c2p(0.62, 1.85), RIGHT,
                                                                                              buff=0.1)
        lam_l = label(r"$\lambda$: \ a measure on $[0, 1]$, \ shown as mass (orange)", font_size=24,
                      color=C.MEASURE).next_to(ax, UP, buff=0.12)
        p0 = float(pts[1])
        rT = ValueTracker(float(rs[0]))

        def window():
            r = rT.get_value()
            t = np.linspace(p0 - r, p0 + r, 200)
            avg = float(np.mean(h(t)))
            return VGroup(area_under(ax, t, h(t), C.EPS, 0.55),
                          Line(ax.c2p(p0 - r, avg), ax.c2p(p0 + r, avg), color=C.EPS, stroke_width=4))

        win = always_redraw(window)
        rl = always_redraw(lambda: MathTex(rf"r = {rT.get_value():.3f}: \ \frac{{\lambda(x - r, x + r)}}{{2r}} = "
                                           rf"{float(np.mean(h(np.linspace(p0 - rT.get_value(), p0 + rT.get_value(), 400)))):.4f}",
                                           font_size=28, color=C.EPS).next_to(ax, DOWN, buff=0.2))
        tab = VGroup(MathTex(r"x", *[rf"\ r = {sci(r_, 0)}" for r_ in rs], font_size=22, color=GREY_A))
        for p, row, hv in zip(pts, ratios, hp):
            tab.add(MathTex(f"{p:.2f}", *[rf"\ {v:.4f}" for v in row], font_size=22))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        widths = [max(r_[j].width for r_ in tab) for j in range(len(rs) + 1)]
        lefts = np.concatenate([[0], np.cumsum(np.array(widths) + 0.3)[:-1]])
        for r_ in tab:  # a real grid: every column starts clear of the widest entry before it
            for j in range(len(rs) + 1):
                r_[j].set_x(lefts[j] + r_[j].width / 2)
        tab.move_to([4.15, 0.5, 0])
        assert tab.get_right()[0] < 6.6
        # the four points of the table, marked on the axis (the window is drawn at the second)
        pdots = VGroup(*[Dot(ax.c2p(float(p_), 0), radius=0.06, color=C.EPS) for p_ in pts])

        concl = VGroup(label(r"the ratios settle on a function: \ the density", font_size=24),
                       MathTex(r"h(x) = 1 + 0.8 \sin 4x \quad (\text{checked to } 10^{-5})", font_size=26,
                               color=C.MEASURE)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(tab, DOWN, buff=0.3)
        assert np.allclose(ratios[:, -1], hp, atol=1e-5)
        head = label(r"A density is a limit of ratios: \ mass over length, \ on shrinking intervals", font_size=34).to_edge(
            UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Here's a measure lambda on the unit interval, drawn as orange mass. Does it have a "
            "density with respect to length? <bookmark mark='b'/> Pick a point and an interval around it, and divide "
            "the interval's lambda-mass by its length. <bookmark mark='c'/> Shrink the interval. The ratio settles. "
            "<bookmark mark='d'/> Do it at four points with radii from 0.2 down to a thousandth, and the ratios "
            "converge to the values of a function, one plus 0.8 sine four x. That function is the density, and lambda "
            "of any set is the integral of h over it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(area), FadeIn(lam_l))
            vo.wait_until("b")
            # the table fills column by column as the window shrinks: first the header, the points and r = 0.2
            self.play(FadeIn(win), FadeIn(rl), FadeIn(pdots), FadeIn(tab[0]),
                      *[FadeIn(r_[0]) for r_ in tab[1:]], *[FadeIn(r_[1]) for r_ in tab[1:]])
            vo.wait_until("c")
            for j, r_target in ((2, float(rs[1])), (3, float(rs[2]))):
                self.play(rT.animate.set_value(r_target), *[FadeIn(r_[j]) for r_ in tab[1:]], run_time=1.7)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r_[4]) for r_ in tab[1:]], lag_ratio=0.3), run_time=1.5)
            self.play(gh.animate.set_stroke(opacity=1.0), FadeIn(gh_l), FadeIn(concl))
        for m in (win, rl):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        thm = VGroup(
            label(r"\textbf{RCA 6.10} \ (Lebesgue, \ Radon 1913, \ Nikodym 1930) \ $\mu$ positive, \ $\sigma$-finite, "
                  r"\ $\lambda$ complex:", font_size=26),
            label(r"(a) \ $\lambda = \lambda_a + \lambda_s$ \ with $\lambda_a \ll \mu$ \ and $\lambda_s \perp \mu$, "
                  r"\ uniquely", font_size=28),
            label(r"(b) \ $d\lambda_a = h\,d\mu$ \ for a unique $h \in L^1(\mu)$", font_size=28, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        head = label(r"The Radon--Nikodym theorem", font_size=34).to_edge(UP, buff=0.3)
        thm.next_to(head, DOWN, buff=0.2)
        ax = plain_axes([0, 1, 0.25], [0, 2, 0.5], 6.0, 3.0).move_to([-3.0, -1.5, 0])
        x = np.linspace(0, 1, 600)
        ac = area_under(ax, x, h(x), C.MEASURE, 0.3)
        # the atom is a mass, not a density value: an arrow from the axis, labelled with its mass
        atom = Arrow(ax.c2p(0.7, 0), ax.c2p(0.7, 2.0), buff=0, color=C.PATHOLOGY, stroke_width=5, tip_length=0.2)
        labs = VGroup(MathTex(r"\lambda_a = h\,dm", font_size=28, color=C.MEASURE).move_to(ax.c2p(0.25, 0.6)),
                      VGroup(MathTex(r"\lambda_s = 0.3\,\delta_{0.7}", font_size=28, color=C.PATHOLOGY),
                             label(r"mass $0.3$", font_size=22, color=C.PATHOLOGY)).arrange(
                          DOWN, aligned_edge=LEFT, buff=0.08).next_to(ax.c2p(0.7, 1.75), RIGHT, buff=0.15))
        side = VGroup(
            label(r"$\lambda = h\,dm + 0.3\,\delta_{0.7}$:", font_size=26),
            label(r"the atom lives on $\{0.7\}$, \ length $0$:", font_size=24, color=C.PATHOLOGY),
            label(r"singular to $m$", font_size=24, color=C.PATHOLOGY),
            label(r"the rest has a density", font_size=24, color=C.MEASURE),
            label(r"every measure splits this way", font_size=24, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.9, -1.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The theorem says every measure splits into a part with a density and a singular "
            "part, uniquely. <bookmark mark='b'/> Take lambda to be the orange density plus an atom of mass 0.3 at "
            "0.7. <bookmark mark='c'/> The atom lives on a single point, a set of length zero, so it's singular. "
            "Everything else has a density. <bookmark mark='d'/> Radon proved it in Euclidean space in 1913, and "
            "Nikodym in general in 1930. Rudin gives a proof by von Neumann, which uses a Hilbert space."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(thm))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(ac), FadeIn(labs[0]), FadeIn(side[0]))
            self.play(GrowArrow(atom), FadeIn(labs[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[1:4]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def von_neumann(self):
        d = load("radon")
        t, g = d["t"], d["g"]
        pm = ProofMap([r"$\varphi = \lambda + \mu$; \ $f \mapsto \int f\,d\lambda$ \ is bounded on $L^2(\varphi)$",
                       r"Riesz (ch.~7): \ $\int f\,d\lambda = \int f g\,d\varphi$, \ $0 \le g \le 1$",
                       r"$\{g = 1\}$ carries $\lambda_s$; \ elsewhere $h = \dfrac{g}{1 - g}$"],
                      font_size=22, width=6.3, buff=0.14, direction=DOWN).move_to([3.6, 1.25, 0])
        head = label(r"Von Neumann's proof: \ find a vector in $L^2(\lambda + \mu)$", font_size=34).to_edge(UP, buff=0.3)
        assert pm.get_top()[1] < head.get_bottom()[1] - 0.15
        ax = plain_axes([0, 1, 0.25], [0, 1.1, 0.5], 6.0, 3.0, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.0, -1.35, 0])
        gg = polyline(ax, t, g, color=C.INNER, stroke_width=4)
        one = DashedLine(ax.c2p(0, 1), ax.c2p(1, 1), color=GREY_B, stroke_width=1.5)
        atom_g = Dot(ax.c2p(0.7, 1.0), radius=0.09, color=C.PATHOLOGY)
        atom_l = MathTex(r"g(0.7) = 1", font_size=24, color=C.PATHOLOGY).next_to(atom_g, UR, buff=0.08).shift(RIGHT * 0.1)
        g_l = MathTex(r"g = \frac{d\lambda}{d\varphi} = \frac{h}{1 + h}", font_size=28, color=C.INNER).next_to(ax, UP,
                                                                                                        buff=0.35)
        assert np.all((g >= 0) & (g < 1)) and np.allclose(g / (1 - g), h(t))
        bnd = VGroup(
            MathTex(r"\Big|\int f\,d\lambda\Big| \le \int |f|\,d\varphi \le \varphi(X)^{1/2}\, \|f\|_{L^2(\varphi)}",
                    font_size=26),
            label(r"(Cauchy--Schwarz): \ a bounded functional", font_size=22, color=GREY_B),
            label(r"at the atom, \ $\varphi(\{0.7\}) = \lambda(\{0.7\}) = 0.3$, \ so $g = 1$ there", font_size=22,
                  color=C.PATHOLOGY),
            label(r"off it, \ $g = \frac{h}{1 + h} < 1$ \ and \ $\frac{g}{1 - g} = h$ \ (checked)", font_size=22,
                  color=C.MEASURE),
            label(r"20 random test functions: \ both sides agree to $10^{-10}$", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.8, -1.25, 0])
        for r_ in bnd:
            if r_.width > 5.6:
                r_.width = 5.6
        bnd.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.8, -1.25, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Von Neumann's trick: add the two measures, phi equals lambda plus mu. Integration "
            "against lambda is a bounded linear functional on L two of phi, by Cauchy-Schwarz. "
            "<bookmark mark='b'/> So by the Riesz theorem of chapter seven, it's an inner product with some function "
            "g, and g lies between zero and one. Here g is h over one plus h. <bookmark mark='c'/> Where g equals one, "
            "mu has no mass: that set carries the singular part. At the atom, g is exactly one. "
            "<bookmark mark='d'/> Everywhere else, the density is g over one minus g, and that's h again. A theorem "
            "about measures, proved by finding a vector in a Hilbert space."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(pm))
            self.play(*pm.light(0), FadeIn(bnd[:2]))
            vo.wait_until("b")
            self.play(*pm.light(1), Create(ax), Create(one), Create(gg), FadeIn(g_l))
            vo.wait_until("c")
            self.play(*pm.light(2), FadeIn(atom_g, scale=2), FadeIn(atom_l), FadeIn(bnd[2]))
            vo.wait_until("d")
            self.play(FadeIn(bnd[3:]))
            self.play(*pm.done())
        self.wait(0.4)
        self.clear_scene()
