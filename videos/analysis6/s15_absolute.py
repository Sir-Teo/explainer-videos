from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis6.common import load, plain_axes, polyline


def cantor_intervals(n):
    ivs = [(0.0, 1.0)]
    for _ in range(n):
        ivs = [iv for a, b in ivs for iv in ((a, a + (b - a) / 3), (b - (b - a) / 3, b))]
    return ivs


class AbsolutelyContinuous(VoiceoverScene):
    def construct(self):
        self.card()
        self.staircase()
        self.definition()
        self.wild()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(14, r"The fundamental theorem, for Lebesgue", r"When is $f(b) - f(a) = \int_a^b f'$?", lit=(),
                            part=6)
        with self.voiceover("Chapter fourteen: the fundamental theorem of calculus, rebuilt for Lebesgue's integral."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def staircase(self):
        d = load("cantorac")
        xs, F, removed, total = d["xs"], d["F"], d["removed"], float(d["total_removed"])
        ax = plain_axes([0, 1, 0.25], [0, 1, 0.25], 5.6, 3.9, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 2}}).move_to([-3.4, -0.3, 0])
        g = polyline(ax, xs, F, color=C.MEASURE, stroke_width=3.5)
        flats = VGroup(*[Line(ax.c2p(a, 0), ax.c2p(b, 0), color=C.CONNECTED_SET, stroke_width=9)
                         for a, b in removed])
        flats_l = MathTex(rf"F' = 0 \text{{ on the removed intervals: total length }} \to 1", font_size=24,
                          color=C.CONNECTED_SET).next_to(ax, DOWN, buff=0.2)
        # F is constant on each removed interval: the sampled F agrees at both ends
        for a, b in removed[:15]:
            ia, ib = np.searchsorted(xs, a + 1e-9), np.searchsorted(xs, b - 1e-9) - 1
            if ib > ia:
                assert abs(F[ib] - F[ia]) < 1e-9
        assert abs(total - (1 - (2 / 3) ** 12)) < 1e-12
        rows = VGroup(
            MathTex(r"F(1) - F(0) = 1", font_size=32, color=C.MEASURE),
            MathTex(r"\int_0^1 F'\,dm = 0", font_size=32, color=C.CONNECTED_SET),
            label(r"$F$ is continuous, increasing, \ and $F' = 0$ a.e.", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.4, 1.4, 0])
        card = museum_card(r"The Cantor function", r"Cantor 1884; \ Lebesgue 1904", r"$F(x) - F(0) = \int_0^x F'$",
                           r"RCA 7.16 \ (and Part 1's staircase)", width=5.0).move_to([3.4, -1.15, 0])
        head = label(r"A function that rises by $1$ with derivative $0$ a.e.", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Is a function the integral of its derivative? Here's Part 1's staircase, the Cantor "
            "function. It's continuous and increasing, and it rises from zero to one. <bookmark mark='b'/> On every "
            "removed interval it's flat, so its derivative is zero there, and the removed intervals have total "
            "length one. The derivative is zero almost everywhere. <bookmark mark='c'/> So the integral of the "
            "derivative is zero, but the function rose by one. The fundamental theorem fails, for a continuous "
            "increasing function. Something more than continuity is needed."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(g), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(f_) for f_ in flats], lag_ratio=0.03), FadeIn(flats_l), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[:2]))
            self.play(FadeIn(rows[2]), FadeIn(card))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def definition(self):
        d = load("cantorac")
        xs, F, lens = d["xs"], d["F"], d["lens"]
        defn = VGroup(
            label(r"\textbf{RCA 7.17} \ $f$ is \emph{absolutely continuous} on $[a, b]$ if for every $\varepsilon > 0$ "
                  r"there is $\delta > 0$:", font_size=26),
            MathTex(r"\sum_i (\beta_i - \alpha_i) < \delta \ \Rightarrow \ \sum_i |f(\beta_i) - f(\alpha_i)| < \varepsilon",
                    font_size=32, color=C.EPS),
            label(r"for disjoint intervals $(\alpha_i, \beta_i)$: \ uniform continuity, \ for many intervals at once",
                  font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.25)
        ax = plain_axes([0, 1, 0.5], [0, 1, 0.5], 5.0, 2.9, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.4, -0.85, 0])
        bx = plain_axes([0, 1, 0.5], [0, 1, 0.5], 5.0, 2.9, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([3.4, -0.85, 0])
        x = np.linspace(0, 1, 500)
        gs = polyline(ax, x, np.sqrt(x), color=C.SEQ, stroke_width=3.5)
        gc = polyline(bx, xs, F, color=C.MEASURE, stroke_width=3)
        s_l = MathTex(r"\sqrt x", font_size=28, color=C.SEQ).next_to(ax, UP, buff=0.08)
        c_l = MathTex(r"\text{Cantor } F", font_size=28, color=C.MEASURE).next_to(bx, UP, buff=0.08)
        # the definition, drawn: three disjoint intervals (alpha_i, beta_i) on the x-axis and the rises of sqrt over
        # them on the y-axis; the two sums are the two sides of the definition
        al = np.array([0.10, 0.40, 0.75])
        be = al + 0.04
        rise3 = np.sqrt(be) - np.sqrt(al)
        assert np.all(al[1:] > be[:-1]) and abs(rise3.sum() - 0.1121) < 5e-4
        ill = VGroup()
        for a_, b_ in zip(al, be):
            tt = np.linspace(a_, b_, 20)
            ill.add(Line(ax.c2p(a_, 0), ax.c2p(b_, 0), color=C.EPS, stroke_width=10),
                    polyline(ax, tt, np.sqrt(tt), color=C.EPS, stroke_width=7),
                    DashedLine(ax.c2p(a_, np.sqrt(a_)), ax.c2p(0, np.sqrt(a_)), color=C.EPS, stroke_width=1.5,
                               dash_length=0.06).set_opacity(0.6),
                    DashedLine(ax.c2p(b_, np.sqrt(b_)), ax.c2p(0, np.sqrt(b_)), color=C.EPS, stroke_width=1.5,
                               dash_length=0.06).set_opacity(0.6),
                    Line(ax.c2p(0, np.sqrt(a_)), ax.c2p(0, np.sqrt(b_)), color=C.EPS, stroke_width=10))
        ill_t = VGroup(MathTex(rf"\textstyle\sum_i (\beta_i - \alpha_i) = {np.sum(be - al):.2f}", font_size=24, color=C.EPS),
                       MathTex(rf"\textstyle\sum_i |f(\beta_i) - f(\alpha_i)| = {rise3.sum():.3f}", font_size=24,
                               color=C.EPS)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(ax, DOWN, buff=0.15)
        # sqrt: eps = 0.1, delta = eps^2 = 0.01; the worst placement is one interval at 0
        rng = np.random.default_rng(2)
        worst = 0.0
        for _ in range(4000):
            k = rng.integers(1, 6)
            ls = rng.dirichlet(np.ones(k)) * 0.01
            starts = np.sort(rng.uniform(0, 1 - 0.01, k)) + np.concatenate([[0], np.cumsum(ls)[:-1]])
            starts = np.minimum(starts, 1 - ls)
            rise = float(np.sum(np.sqrt(starts + ls) - np.sqrt(starts)))
            worst = max(worst, rise)
        assert worst <= 0.1 + 1e-12 and abs(math.sqrt(0.01) - 0.1) < 1e-15
        # the worst placement, magnified: the interval [0, 0.01] and the rise 0.1 over it
        xw, yw = (-0.002, 0.02), (-0.03, 0.15)
        ins, decor = magnifier(ax, xw, yw, center=ax.c2p(0.72, 0.3), width=2.3, height=1.3)
        p0, p1 = ax.c2p(xw[0], yw[0]), ax.c2p(xw[1], yw[1])
        kx, ky = 2.3 / (p1[0] - p0[0]), 1.3 / (p1[1] - p0[1])
        decor.remove(decor.tag)
        decor.tag = MathTex(rf"x \times {kx:.0f}, \ y \times {ky:.0f}", font_size=22, color=GREY_B).next_to(
            decor.frame, UP, buff=0.08).align_to(decor.frame, LEFT)
        decor.add(decor.tag)
        tz = np.linspace(0, 0.02, 200)
        zoom = VGroup(polyline(ins, tz, np.sqrt(tz), color=C.SEQ, stroke_width=3),
                      Line(ins.c2p(0, 0), ins.c2p(0.01, 0), color=C.EPS, stroke_width=8),
                      Line(ins.c2p(0.01, 0), ins.c2p(0.01, 0.1), color=C.EPS, stroke_width=5))
        zoom.add(MathTex(r"\delta", font_size=24, color=C.EPS).next_to(ins.c2p(0.005, 0), DOWN, buff=0.04),
                 MathTex(rf"{math.sqrt(0.01):.1f}", font_size=22, color=C.EPS).next_to(ins.c2p(0.0102, 0.05), RIGHT,
                                                                                      buff=0.08))
        sq_t = VGroup(MathTex(r"\varepsilon = 0.1:\ \delta = \varepsilon^2 = 0.01 \text{ works}", font_size=24, color=C.EPS),
                      MathTex(rf"\text{{4000 random placements: max rise }} {worst:.4f} \le 0.1", font_size=22,
                              color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(ax, DOWN, buff=0.15)
        n = 4
        ivs = cantor_intervals(n)
        cb = VGroup(*[Line(bx.c2p(a, -0.04), bx.c2p(b, -0.04), color=C.PATHOLOGY, stroke_width=10) for a, b in ivs])
        ct = VGroup(MathTex(r"2^n \text{ intervals, length } (\tfrac23)^n = " + r",\ ".join(f"{v:.3f}" for v in lens[2:6]),
                            font_size=22, color=C.PATHOLOGY),
                    MathTex(r"\text{total rise across them} = 1: \ \text{no } \delta \text{ for } \varepsilon = \tfrac12",
                            font_size=22, color=C.PATHOLOGY)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(
            bx, DOWN, buff=0.15)
        thm = VGroup(
            label(r"\textbf{RCA 7.20} \ $f$ is absolutely continuous on $[a, b]$ \ $\iff$ \ $f'$ exists a.e., "
                  r"$f' \in L^1$, \ and", font_size=26),
            MathTex(r"f(x) - f(a) = \int_a^x f'\,dm \quad \text{for all } x", font_size=32, color=C.EPS),
            label(r"$\sqrt x$: \ $f' = \frac{1}{2\sqrt x}$ is unbounded, \ but $\int_0^1 f' = 1 = \sqrt 1 - \sqrt 0$",
                  font_size=24, color=C.SEQ),
        ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> The missing condition is absolute continuity: for every epsilon there's a delta, "
            "so that any finite set of disjoint intervals with total length below delta has total rise below "
            "epsilon. <bookmark mark='b'/> The square root passes: with epsilon a tenth, delta a hundredth works, "
            "and the worst placement is one interval at zero, where the curve is steepest. Four thousand random "
            "placements never beat a tenth. <bookmark mark='c'/> The Cantor function fails: the 2 to the n intervals "
            "of the n-th stage have total length shrinking to zero, but the function rises by one across them. "
            "<bookmark mark='d'/> And that's the whole story. A function is absolutely continuous exactly when it's "
            "the integral of its derivative. The square root qualifies, even though its derivative is unbounded."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(defn), Create(ax), Create(gs), FadeIn(s_l))
            self.play(LaggedStart(*[FadeIn(m_) for m_ in ill], lag_ratio=0.08), FadeIn(ill_t), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeOut(ill), FadeOut(ill_t))
            self.play(FadeIn(decor), Create(zoom[0]), FadeIn(zoom[1:]), FadeIn(sq_t))
            vo.wait_until("c")
            self.play(Create(bx), Create(gc), FadeIn(c_l))
            self.play(LaggedStart(*[Create(c_) for c_ in cb], lag_ratio=0.05), FadeIn(ct))
            vo.wait_until("d")
            self.play(FadeOut(defn, shift=UP * 0.2), FadeIn(thm, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def wild(self):
        d = load("ftc")
        eps, var = d["eps"], d["var"]
        ax = plain_axes([0, 0.6, 0.2], [-0.4, 0.4, 0.2], 6.4, 3.4, numbers=False).move_to([-3.0, 0.0, 0])
        ax.y_axis.add_numbers(*[v for v in (-0.4, -0.2, 0.2, 0.4)], num_decimal_places=1, font_size=18)
        # the x numbers along the bottom edge (the curve crosses the x-axis between them)
        xnums = VGroup(*[MathTex(f"{v:.1f}", font_size=18, color=GREY_B).next_to(ax.c2p(v, -0.4), DOWN, buff=0.12)
                         for v in (0.2, 0.4, 0.6)])
        # sampled uniformly in u = 1/x^2 (20 points per period of sin u), down to x = 0.02: every wiggle resolved
        # (drawn from x = 0.6 in toward 0)
        u = np.linspace(1 / 0.6**2, 1 / 0.02**2, int(20 * (1 / 0.02**2 - 1 / 0.6**2) / (2 * np.pi)) + 1)
        xs = u ** -0.5
        fx = xs**2 * np.sin(u)
        assert abs(xs[0] - 0.6) < 1e-12 and abs(xs[-1] - 0.02) < 1e-12 and np.diff(u).min() > 0
        assert np.diff(u).max() <= 2 * np.pi / 19  # at least 19 samples per oscillation everywhere
        assert np.all(np.abs(fx) <= xs**2 + 1e-15)
        g = polyline(ax, xs, fx, color=C.PATHOLOGY, stroke_width=2)
        # below x = 0.02 the wiggles are finer than a pixel: the band between -x^2 and x^2
        xb = np.linspace(0, 0.02, 30)
        band = Polygon(*[ax.c2p(a, a * a) for a in xb], *[ax.c2p(a, -a * a) for a in xb[::-1]], stroke_width=0,
                       fill_color=C.PATHOLOGY, fill_opacity=0.8)
        xe = np.linspace(0, 0.6, 200)
        env = VGroup(polyline(ax, xe, xe**2, color=GREY_C, stroke_width=1.5),
                     polyline(ax, xe, -xe**2, color=GREY_C, stroke_width=1.5))
        env_l = MathTex(r"\pm x^2", font_size=22, color=GREY_B).next_to(ax.c2p(0.55, 0.55**2), UL, buff=0.06)
        f_l = MathTex(r"f(x) = x^2 \sin \frac{1}{x^2}, \quad f(0) = 0", font_size=28, color=C.PATHOLOGY).next_to(
            ax, UP, buff=0.12)
        tab = VGroup(MathTex(r"\varepsilon", r"\quad \int_\varepsilon^1 |f'|", font_size=26, color=GREY_A))
        for e, v in zip(eps, var):
            tab.add(MathTex(f"{e}", rf"\quad {v:.3f}", font_size=26, color=C.PATHOLOGY))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.1, 1.0, 0])
        regrid(tab)
        grow = label(rf"each factor 10 in $\varepsilon$ adds $\frac{{4}}{{\pi}}\log 10 = {4 / math.pi * math.log(10):.2f}$", font_size=22,
                     color=GREY_A).next_to(tab, DOWN, buff=0.15)
        assert abs((var[3] - var[1]) - 4 / math.pi * math.log(10)) < 0.1
        sm = VGroup(
            label(r"differentiable at every point, \ even at $0$", font_size=24),
            label(r"but $f' \notin L^1$: \ not absolutely continuous", font_size=24, color=C.PATHOLOGY),
            label(r"\textbf{RCA 7.21} \ if $f'$ exists everywhere \emph{and} $f' \in L^1$, \ the FTC holds", font_size=24,
                  color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.3)
        head = label(r"Differentiable everywhere is not enough either", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> One more warning. x squared sine of one over x squared is differentiable at every "
            "point, including zero, where the derivative is zero. <bookmark mark='b'/> But near zero it wiggles so "
            "fast that its derivative isn't integrable: the integral of the absolute derivative from epsilon to one "
            "grows without bound, by about 2.93 for every factor of ten. <bookmark mark='c'/> So the function isn't "
            "absolutely continuous, and the Lebesgue integral of f prime doesn't exist. Rudin's theorem asks for "
            "both: a derivative at every point, and an integrable one."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(xnums), Create(env), FadeIn(env_l), FadeIn(f_l), FadeIn(band),
                      Create(g), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(tab[0]))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.4), run_time=2.0)
            self.play(FadeIn(grow))
            vo.wait_until("c")
            self.play(FadeIn(sm[:2]))
            self.play(FadeIn(sm[2]))
        self.wait(0.4)
        self.clear_scene()
