from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis3.common import load, plain_axes, polyline
from videos.analysis3.compute import cantor_intervals


def alpha_smooth(x):
    return x + 0.32 * np.sin(2.4 * x)


class Stieltjes(VoiceoverScene):
    def construct(self):
        self.card()
        self.ruler()
        self.step()
        self.cantor()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(3, r"Integrating against a staircase", r"What if the ruler itself is uneven?", lit=(), part=3)
        with self.voiceover(
            "Chapter three. Rudin's integral has an extra ingredient, an increasing function alpha that measures the "
            "pieces. Stieltjes introduced it in 1894. It looks like a technicality, but it lets one integral cover "
            "lengths, sums, and stranger things."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def ruler(self):
        head = VGroup(MathTex(r"U(P, f, \alpha) = \sum M_i\, \Delta\alpha_i, \qquad \Delta\alpha_i = \alpha(x_i) - "
                              r"\alpha(x_{i-1})", font_size=36),
                      label(r"$\alpha$ increasing; \ $\alpha(x) = x$ gives back Riemann's integral \ (Rudin 6.2)",
                            font_size=26, color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.35)
        X0, X1 = -5.5, 5.5
        yx, ya = -1.5, 0.75
        a_max = alpha_smooth(3.0)
        Xx = lambda v: X0 + (X1 - X0) * v / 3.0  # noqa: E731
        Xa = lambda v: X0 + (X1 - X0) * v / a_max  # noqa: E731
        xline = Line([X0, yx, 0], [X1, yx, 0], color=GREY_C, stroke_width=2)
        aline = Line([X0, ya, 0], [X1, ya, 0], color=GREY_C, stroke_width=2)
        xl = MathTex(r"x", font_size=32, color=GREY_B).next_to(xline, LEFT, buff=0.2)
        al = MathTex(r"\alpha(x)", font_size=32, color=GREY_B).next_to(aline, LEFT, buff=0.2)
        # equal steps in alpha, pulled back to x: the ticks crowd where alpha grows fast
        avals = np.linspace(0, a_max, 25)
        xs = np.interp(avals, alpha_smooth(np.linspace(0, 3, 3001)), np.linspace(0, 3, 3001))
        ticks_a = VGroup(*[Line([Xa(v), ya - 0.1, 0], [Xa(v), ya + 0.1, 0], color=C.EPS, stroke_width=2.5) for v in avals])
        ticks_x = VGroup(*[Line([Xx(v), yx - 0.1, 0], [Xx(v), yx + 0.1, 0], color=C.EPS, stroke_width=2.5) for v in xs])
        links = VGroup(*[Line([Xx(v), yx + 0.12, 0], [Xa(a), ya - 0.12, 0], color=C.EPS, stroke_width=1, stroke_opacity=0.4)
                         for v, a in zip(xs, avals)])
        # Riemann's ruler first: equal pieces of x, each counted by its width
        ticks_r = VGroup(*[Line([Xx(v), yx - 0.1, 0], [Xx(v), yx + 0.1, 0], color=GREY_B, stroke_width=2)
                           for v in np.linspace(0, 3, 25)])
        rl = label(r"Riemann: \ equal widths $\Delta x_i$", font_size=24, color=GREY_B).next_to(xline, DOWN, buff=0.3)
        dens = label(r"where $\alpha$ climbs fast, a short stretch of $x$ counts for a lot", font_size=26,
                     color=C.EPS).move_to([0, -2.35, 0])
        dens2 = MathTex(r"\alpha \text{ smooth:} \quad \int f\,d\alpha = \int f\,\alpha'\,dx \quad (\text{Rudin 6.17})",
                        font_size=32, color=C.FUNC).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In the sums, replace the width of each piece by the increase of alpha across it. <bookmark mark='a'/> "
            "Think of alpha as a stretched ruler. Mark equal steps on the alpha scale, and pull them back to the x "
            "axis. <bookmark mark='b'/> Where alpha climbs fast, the marks crowd together, and a short stretch of x "
            "carries a lot of weight; where alpha is flat, a long stretch counts for little. <bookmark mark='c'/> For "
            "a smooth alpha this is just a density: the integral of f d alpha is the integral of f times alpha prime."
        ) as vo:
            self.play(FadeIn(head), Create(xline), FadeIn(xl), FadeIn(ticks_r), FadeIn(rl))
            vo.wait_until("a")
            self.play(Create(aline), FadeIn(al), FadeIn(ticks_a), FadeOut(rl))
            self.play(TransformFromCopy(ticks_a, ticks_x), FadeOut(ticks_r), Create(links), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(dens))
            vo.wait_until("c")
            self.play(FadeIn(dens2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def step(self):
        ax = plain_axes([0, 1, 0.25], [0, 1.3, 0.5], 5.6, 3.2).move_to([-3.6, 0.45, 0])
        fr = lambda t: 0.4 + 0.5 * t + 0.25 * np.sin(6 * t)  # noqa: E731
        gf = ax.plot(fr, x_range=[0, 1, 0.005], color=C.FUNC, stroke_width=4)
        s = 0.62
        al_ax = plain_axes([0, 1, 0.25], [0, 1.2, 1], 5.6, 1.6).move_to([-3.6, -2.55, 0])
        step_g = VGroup(Line(al_ax.c2p(0, 0), al_ax.c2p(s, 0), color=C.EPS, stroke_width=4),
                        Line(al_ax.c2p(s, 1), al_ax.c2p(1, 1), color=C.EPS, stroke_width=4),
                        Circle(radius=0.06, color=C.EPS, stroke_width=2.5).set_fill(BACKGROUND, 1).move_to(al_ax.c2p(s, 1)),
                        Dot(al_ax.c2p(s, 0), radius=0.06, color=C.EPS))
        al_lab = MathTex(r"\alpha(x) = I(x - s)", font_size=28, color=C.EPS).move_to(al_ax.c2p(0.05, 0.75), aligned_edge=LEFT)
        mark = VGroup(DashedLine(ax.c2p(s, 0), ax.c2p(s, fr(s)), color=C.EPS, stroke_width=2),
                      Dot(ax.c2p(s, fr(s)), radius=0.08, color=C.EPS),
                      MathTex(r"s", font_size=28).next_to(ax.c2p(s, 0), DOWN, buff=0.12))
        # Rudin 6.16 drawn: steps c_n at s_n; the stems at s_n on f's plot are as thick as the steps are tall
        cs_, ss_ = np.array([0.45, 0.3, 0.15, 0.1]), np.array([0.2, 0.45, 0.62, 0.85])
        stair_sum = float(np.sum(cs_ * fr(ss_)))

        def alpha_st(t):
            return np.sum(cs_[None, :] * (np.asarray(t)[:, None] >= ss_[None, :]), axis=1)

        # an independent check: upper and lower Riemann-Stieltjes sums on a fine partition squeeze the series
        pe = np.linspace(0, 1, 20001)
        da = np.diff(alpha_st(pe))
        tt_ = np.linspace(0, 1, 400001)
        ft_ = fr(tt_)
        idx_ = np.minimum((tt_ * 20000).astype(int), 19999)
        Mi, mi = np.full(20000, -np.inf), np.full(20000, np.inf)
        np.maximum.at(Mi, idx_, ft_)
        np.minimum.at(mi, idx_, ft_)
        assert abs(float(np.sum(Mi * da)) - stair_sum) < 2e-3 and abs(float(np.sum(mi * da)) - stair_sum) < 2e-3
        assert abs(cs_.sum() - 1) < 1e-12 and np.all(np.diff(ss_) > 0)
        stair_pts = np.r_[0, ss_, 1]
        stair_lv = np.r_[0, np.cumsum(cs_)]
        stair_g = VGroup(*[Line(al_ax.c2p(a, v), al_ax.c2p(b, v), color=C.EPS, stroke_width=4)
                           for a, b, v in zip(stair_pts[:-1], stair_pts[1:], stair_lv)])
        for k_, (sx, lv) in enumerate(zip(ss_, stair_lv[1:])):
            stair_g.add(Circle(radius=0.055, color=C.EPS, stroke_width=2.5).set_fill(BACKGROUND, 1).move_to(
                al_ax.c2p(sx, stair_lv[k_])), Dot(al_ax.c2p(sx, lv), radius=0.055, color=C.EPS))
        stems = VGroup(*[VGroup(Line(ax.c2p(sx, 0), ax.c2p(sx, fr(sx)), color=C.EPS, stroke_width=3 + 16 * c),
                                Dot(ax.c2p(sx, fr(sx)), radius=0.06, color=C.EPS))
                         for sx, c in zip(ss_, cs_)])
        # above the staircase (it reaches 0.75 before x = 0.62), not across its steps
        st_lab = MathTex(r"\alpha = \sum c_n I(x - s_n)", font_size=28, color=C.EPS).move_to(al_ax.c2p(0.05, 1.12),
                                                                                           aligned_edge=LEFT)
        side = VGroup(
            label(r"\textbf{Rudin 6.15} \ a unit step at $s$, \ $f$ continuous at $s$:", font_size=28),
            MathTex(r"\int f\,d\alpha = f(s)", font_size=40, color=C.EPS),
            label(r"only the piece containing $s$ has $\Delta\alpha_i \ne 0$", font_size=24, color=GREY_A),
            label(r"\textbf{Rudin 6.16} \ steps $c_n \ge 0$ at $s_n$, \ $\sum c_n < \infty$, \ $f$ continuous:", font_size=28),
            MathTex(r"\int f\,d\alpha = \sum_{n} c_n f(s_n)", font_size=38, color=C.EPS),
            MathTex(r"\text{here: } \sum_{n=1}^{4} c_n f(s_n) = " + f"{stair_sum:.4f}", font_size=30, color=C.EPS),
            label(r"an integral can be a series", font_size=26, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([3.4, -0.2, 0])
        for r_ in side:
            if r_.width > 6.5:
                r_.width = 6.5
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([3.4, -0.2, 0])
        assert side.get_right()[0] < 6.9
        with self.voiceover(
            "Now the extreme case. <bookmark mark='a'/> Let alpha be a single unit step at a point s: zero before it, "
            "one after. <bookmark mark='b'/> In any partition, only the piece containing s has an increase in alpha, "
            "and as the partition is refined, that piece closes in on s. <bookmark mark='c'/> So the integral of f d "
            "alpha is simply f of s: all the weight is concentrated at one point. <bookmark mark='d'/> Stack up "
            "countably many steps, of sizes c n at points s n, and the integral becomes the series of c n times f of "
            "s n. Sums and integrals are two cases of one idea, which will grow into measures in Part 5."
        ) as vo:
            self.play(Create(ax), Create(gf))
            vo.wait_until("a")
            self.play(Create(al_ax), FadeIn(step_g), FadeIn(al_lab))
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(Create(mark[0]), FadeIn(mark[1:]), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeOut(step_g), FadeIn(stair_g), FadeOut(al_lab), FadeIn(st_lab), FadeOut(mark),
                      FadeIn(side[3:5]))
            self.play(LaggedStart(*[GrowFromEdge(st, DOWN) for st in stems], lag_ratio=0.2), FadeIn(side[5]))
            self.play(FadeIn(side[6]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cantor(self):
        d = load("stieltjes")
        xs, Cv, I1, I2, gap = d["xs"], d["C"], d["I1"], d["I2"], d["gap"]
        ax = plain_axes([0, 1, 0.25], [0, 1.0, 0.5], 5.6, 4.6).move_to([-3.9, -0.6, 0])
        stair = polyline(ax, xs, Cv, color=C.EPS, stroke_width=3)
        head = VGroup(label(r"$\alpha$ = the Cantor function \ (Part 1): \ continuous, no jumps, \ flat off the "
                            r"Cantor set", font_size=28),
                      label(r"(the Cantor set: Rudin 2.44; \ its staircase: Part 1, chapter 9)", font_size=22, color=GREY_B)
                      ).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.3)
        depth = 4
        a, w = cantor_intervals(depth)
        bars = VGroup()
        for lo in a:
            p0, p1 = ax.c2p(lo, 0), ax.c2p(lo + w, 1)
            bars.add(Rectangle(width=max(p1[0] - p0[0], 0.01), height=p1[1] - p0[1], stroke_width=0, fill_color=C.EPS,
                               fill_opacity=0.18).move_to((p0 + p1) / 2))
        rows = VGroup(
            label(r"$\alpha$ rises by $2^{-d}$ across each of the $2^d$ Cantor intervals of length $3^{-d}$", font_size=24),
            MathTex(r"U - L = \sum_{\text{intervals}} 3^{-d}\, 2^{-d} = 3^{-d}", font_size=30, color=C.EPS),
            MathTex(rf"\int_0^1 x\,d\alpha = {I1[-1]:.6f} = \tfrac12", font_size=32),
            MathTex(rf"\int_0^1 x^2\,d\alpha = {I2[-1]:.6f} = \tfrac38", font_size=32),
            label(r"by self-similarity: \ $\alpha$ is half itself, shrunk by $3$, twice", font_size=22, color=GREY_A),
            label(r"not a sum (no jumps), \ not $\int f\alpha'\,dx$ ($\alpha' = 0$ off a set of length $0$)", font_size=24,
                  color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([3.0, -0.4, 0])
        for r_ in rows:
            if r_.width > 6.2:
                r_.width = 6.2
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([3.05, -0.4, 0])
        assert abs(gap[depth - 1] - 3.0**-depth) < 1e-12 and abs(I1[-1] - 0.5) < 1e-9 and abs(I2[-1] - 0.375) < 1e-6
        with self.voiceover(
            "And now something stranger. <bookmark mark='a'/> Let alpha be the Cantor function from Part 1, the "
            "devil's staircase. It's continuous, so it has no jumps, and it's flat on every gap of the Cantor set, so "
            "its derivative is zero almost everywhere. Yet it climbs from zero to one. <bookmark mark='b'/> All of its "
            "increase happens on the Cantor set. At depth d there are two to the d intervals, each of length three "
            "to the minus d, and alpha rises by two to the minus d across each. <bookmark mark='c'/> For f of x equal "
            "to x, the gap between the upper and lower sums is three to the minus d, which goes to zero, and the "
            "integral is one half, as symmetry demands. The integral of x squared is three eighths. "
            "<bookmark mark='d'/> This integral is neither a sum over jumps nor an ordinary integral with a density. "
            "It's a third kind of thing, and in Part 5 it will have a name: a singular measure."
        ) as vo:
            self.play(FadeIn(head), Create(ax))
            vo.wait_until("a")
            self.play(Create(stair), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(bars), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            self.play(FadeIn(rows[3]), FadeIn(rows[4]))
            vo.wait_until("d")
            self.play(FadeIn(rows[5]))
        self.wait(0.4)
        self.clear_scene()
