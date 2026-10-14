from __future__ import annotations

import math

import numpy as np

from scipy.optimize import brentq

from explainer.analysis import *  # noqa: F403
from videos.analysis2.common import load, plain_axes, polyline, runs_in_range


def taylor_poly(coef, x):
    return sum(c * x**k for k, c in enumerate(coef))


class Taylor(VoiceoverScene):
    def construct(self):
        self.card()
        self.hugging()
        self.theorem()
        self.bound()
        self.flat()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(14, r"Taylor's theorem", r"How well can a polynomial imitate a function?", lit=(), part=2)
        with self.voiceover(
            "Chapter fourteen. The derivative is the best line. Higher derivatives give the best parabola, the best "
            "cubic, and so on, and Taylor's theorem says exactly how good they are."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def hugging(self):
        head = MathTex(r"P_n(t) = \sum_{k=0}^{n} \frac{f^{(k)}(\alpha)}{k!}\,(t - \alpha)^k", font_size=38).to_edge(UP,
                                                                                                         buff=0.3)
        specs = [
            (r"$\sin x$", np.sin, [0 if k % 2 == 0 else (-1) ** (k // 2) / math.factorial(k) for k in range(16)],
             [-7, 7], [-2, 2], (1, 3, 5, 7, 9, 11, 13, 15)),
            (r"$\log(1 + x)$", lambda x: np.log1p(x), [0] + [(-1) ** (k + 1) / k for k in range(1, 16)],
             [-1, 2], [-2, 2], (1, 2, 3, 5, 8, 12, 15)),
        ]
        panels = []
        for i, (name, f, coef, xr, yr, degs) in enumerate(specs):
            ax = plain_axes([xr[0], xr[1], 1], [yr[0], yr[1], 1], 6.2, 4.0, numbers=False).move_to(
                [-3.4 + 6.8 * i, -1.0, 0])
            lo = math.exp(yr[0]) - 1 + 1e-3 if i == 1 else xr[0]  # log(1 + x) stays above the axes' bottom
            g = ax.plot(f, x_range=[lo, xr[1], 0.005], color=C.FUNC, stroke_width=4)
            t = label(name, font_size=28, color=C.FUNC).next_to(ax, UP, buff=0.12)

            def poly(n, ax=ax, coef=coef, xr=xr, yr=yr):
                x = np.linspace(xr[0], xr[1], 2400)
                return runs_in_range(ax, x, taylor_poly(coef[:n + 1], x), yr[0], yr[1], C.APPROX)

            panels.append((ax, g, t, poly, degs))
        assert abs(panels[0][0].c2p(0, 0)[1] - panels[1][0].c2p(0, 0)[1]) < 1e-9  # the x-axes line up
        wall = VGroup(DashedLine(panels[1][0].c2p(1, -2), panels[1][0].c2p(1, 2), color=C.PATHOLOGY,
                                 stroke_width=2),
                      DashedLine(panels[1][0].c2p(-1, -2), panels[1][0].c2p(-1, 2), color=C.PATHOLOGY,
                                 stroke_width=2))
        rl = label(r"radius $1$: \ past $x = 1$ they flail", font_size=24, color=C.PATHOLOGY).next_to(panels[1][0], DOWN,
                                                                                                buff=0.15)
        sl = label(r"better and better, on a wider and wider range", font_size=24, color=C.CONNECTED_SET).next_to(
            panels[0][0], DOWN, buff=0.15)
        with self.voiceover(
            "The Taylor polynomial of degree n matches the value and the first n derivatives at a point. "
            "<bookmark mark='a'/> For the sine, adding terms makes the polynomials hug the curve over a wider and wider "
            "range. <bookmark mark='b'/> For the logarithm of one plus x, they improve inside the interval from minus "
            "one to one, and flail outside it, however many terms you take. Same story as the last power series "
            "puzzle: the series has radius one."
        ) as vo:
            self.play(FadeIn(head), *[AnimationGroup(Create(p_[0]), Create(p_[1]), FadeIn(p_[2])) for p_ in panels])
            for mk, (ax, g, t, poly, degs), lab in zip("ab", panels, (sl, rl)):
                vo.wait_until(mk)
                cur = poly(degs[0])
                self.play(Create(cur))
                for n in degs[1:]:
                    self.play(Transform(cur, poly(n)), run_time=0.55)
                self.play(FadeIn(lab), *([Create(wall)] if mk == "b" else []))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        thm = VGroup(label(r"\textbf{Rudin 5.15} \ (Taylor, with Lagrange's remainder) \ For some $x$ between $\alpha$ "
                           r"and $\beta$:", font_size=28),
                     MathTex(r"f(\beta) = P_{n-1}(\beta) + \frac{f^{(n)}(x)}{n!}\,(\beta - \alpha)^n", font_size=38,
                             color=C.EPS)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        # an example: f = e^t, alpha = 0, beta = 2, n = 3; the unknown point is computable here
        ex = plain_axes([0, 2.2, 0.5], [0, 8, 2], 5.2, 4.0, numbers=False).move_to([-3.0, -1.3, 0])
        al, be = 0.0, 2.0
        p2 = lambda t: 1 + t + t * t / 2  # noqa: E731
        ef = ex.plot(np.exp, x_range=[0, 2.1, 0.01], color=C.FUNC, stroke_width=4)
        ep = ex.plot(p2, x_range=[0, 2.1, 0.01], color=C.APPROX, stroke_width=3.5)
        gap = Line(ex.c2p(be, p2(be)), ex.c2p(be, math.exp(be)), color=C.EPS, stroke_width=6)
        xi = math.log((math.exp(be) - p2(be)) * 6 / be**3)  # e^x / 3! * 2^3 = e^2 - P_2(2)
        assert 0 < xi < be and abs(math.exp(xi) / 6 * be**3 + p2(be) - math.exp(be)) < 1e-12
        xm = VGroup(Dot(ex.c2p(xi, 0), radius=0.07, color=C.EPS),
                    MathTex(rf"x = {xi:.3f}", font_size=26, color=C.EPS).next_to(ex.c2p(xi, 0), DOWN, buff=0.15))
        ab_ = VGroup(MathTex(r"\alpha", font_size=28).next_to(ex.c2p(al, 0), DOWN, buff=0.15),
                     MathTex(r"\beta", font_size=28).next_to(ex.c2p(be, 0), DOWN, buff=0.15))
        exl = VGroup(MathTex(r"f(t) = e^t", font_size=30, color=C.FUNC),
                     MathTex(r"P_2(t) = 1 + t + \tfrac{t^2}{2}", font_size=30, color=C.APPROX),
                     MathTex(r"e^2 - P_2(2)", r"=", r"\frac{e^{x}}{3!}\,2^3", font_size=34),
                     MathTex(rf"{math.exp(be) - p2(be):.4f}", r"=", rf"\frac{{e^{{{xi:.3f}}}}}{{6}}\cdot 8", font_size=34)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.2, -1.0, 0])
        exl[2][0].set_color(C.EPS)
        exl[3][0].set_color(C.EPS)
        example = VGroup(ex, ef, ep, gap, xm, ab_, exl)
        rows = [MathTex(r"g(t)", r"=", r"f(t) - P_{n-1}(t) - M (t - \alpha)^n", font_size=32),
                MathTex(r"g(\alpha) = g'(\alpha) = \cdots = g^{(n-1)}(\alpha)", r"=", r"0, \qquad g(\beta) = 0",
                        font_size=32),
                MathTex(r"g^{(n)}(x_n) = f^{(n)}(x_n) - n!\,M", r"=", r"0", font_size=32)]
        whys = [why(r"choose $M$ so that $g(\beta) = 0$"), why(r"$P_{n-1}$ matches $f$ to order $n-1$ at $\alpha$"),
                why(r"mean value theorem, $n$ times")]
        step = ladder(self, rows, whys, keep=3, top=1.45, buff=0.36, x=-0.6, edge=6.6)
        # the same example, f = e^t, n = 3, alpha = 0, beta = 2: g and the points x_1, x_2, x_3 of the proof, computed
        M = (math.exp(be) - p2(be)) / be**3
        gfun = lambda t: np.exp(t) - p2(t) - M * t**3  # noqa: E731
        g1 = lambda t: np.exp(t) - 1 - t - 3 * M * t**2  # noqa: E731
        g2 = lambda t: np.exp(t) - 1 - 6 * M * t  # noqa: E731
        x1 = brentq(g1, 0.5, be)
        x2 = brentq(g2, 0.3, x1)
        x3 = math.log(6 * M)  # the third derivative of g is e^t - 6M
        assert abs(gfun(be)) < 1e-12 and 0 < x3 < x2 < x1 < be and abs(x3 - xi) < 1e-12
        gx = plain_axes([0, 2.1, 0.5], [-0.18, 0.06, 0.1], 8.0, 1.7, numbers=False).move_to([0.9, -2.55, 0])
        tt_ = np.linspace(0, be, 400)
        assert gfun(tt_).min() > -0.18
        gcurve = polyline(gx, tt_, gfun(tt_), color=C.FUNC, stroke_width=3.5)
        g_l = MathTex(r"g", font_size=30, color=C.FUNC).next_to(gx.c2p(0.55, gfun(0.55)), DOWN, buff=0.12)
        ab = VGroup(*[VGroup(Dot(gx.c2p(v, 0), radius=0.07),
                             MathTex(t_, font_size=28).next_to(gx.c2p(v, 0), UL if v == al else UP, buff=0.12))
                      for v, t_ in ((al, r"\alpha"), (be, r"\beta"))])  # alpha beside the vertical axis, not on it
        pts = VGroup(*[VGroup(Dot(gx.c2p(v, 0), radius=0.07, color=C.EPS),
                              MathTex(rf"x_{i + 1}", font_size=28, color=C.EPS).next_to(gx.c2p(v, 0), UP, buff=0.15))
                       for i, v in enumerate((x1, x2, x3))])
        # x_1: g' = 0, a level tangent to g;  x_2: g'' = 0, where g's bending turns
        flat1 = VGroup(Line(gx.c2p(x1 - 0.18, gfun(x1)), gx.c2p(x1 + 0.18, gfun(x1)), color=C.EPS, stroke_width=3),
                       Dot(gx.c2p(x1, gfun(x1)), radius=0.06, color=C.EPS),
                       DashedLine(gx.c2p(x1, gfun(x1)), gx.c2p(x1, 0), color=C.EPS, stroke_width=1.5))
        infl2 = VGroup(Dot(gx.c2p(x2, gfun(x2)), radius=0.06, color=C.EPS),
                       DashedLine(gx.c2p(x2, gfun(x2)), gx.c2p(x2, 0), color=C.EPS, stroke_width=1.5))
        gnote = VGroup(label(r"for $e^t$:", font_size=22, color=GREY_A),
                       label(r"$n = 3$, \ $\alpha = 0$, \ $\beta = 2$", font_size=22, color=GREY_A)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(gx, LEFT, buff=0.35)
        with self.voiceover(
            "<bookmark mark='t'/> Taylor's theorem, in Lagrange's form: f of beta equals the degree n minus one "
            "polynomial, plus one more term with the n-th derivative evaluated at some unknown point x between alpha "
            "and beta. It's the mean value theorem, one level up, and the proof is the mean value theorem applied n "
            "times. <bookmark mark='a'/> Subtract the polynomial and a multiple M of t minus alpha to the n, choosing M "
            "so the difference g vanishes at beta. <bookmark mark='b'/> It also vanishes at alpha, along with its first "
            "n minus one derivatives. <bookmark mark='c'/> So g' has a zero x one between alpha and beta; then g'' has "
            "a zero x two between alpha and x one; and so on, n times. <bookmark mark='d'/> At the last point the n-th "
            "derivative of g is zero, which says M is the n-th derivative of f over n factorial."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(thm))
            self.play(Create(ex), FadeIn(ab_), Create(ef), FadeIn(exl[0]), run_time=1.2)
            self.play(Create(ep), FadeIn(exl[1]), run_time=1.2)
            self.play(Create(gap), FadeIn(exl[2]))
            self.play(FadeIn(xm, shift=UP * 0.2), FadeIn(exl[3]))
            vo.wait_until("a")
            self.play(FadeOut(example), run_time=0.6)
            step(0)
            self.play(Create(gx), Create(gcurve), FadeIn(g_l), FadeIn(gnote))
            vo.wait_until("b")
            step(1)
            self.play(FadeIn(ab))
            vo.wait_until("c")
            self.play(FadeIn(pts[0]), Create(flat1), run_time=0.8)
            self.play(FadeIn(pts[1]), FadeIn(infl2), run_time=0.8)
            self.play(FadeIn(pts[2]), run_time=0.8)
            vo.wait_until("d")
            step(2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bound(self):
        d = load("taylor")
        errs, bounds = d["errs"], d["bounds"]
        N = len(errs)
        ax = plain_axes([0, N, 2], [0, 10, 2], 8.6, 4.4, numbers=False).move_to([0.4, -0.7, 0])  # y = log10 + 8
        yt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=22, color=GREY_B).next_to(ax.c2p(0, k + 8), LEFT, buff=0.15)
                      for k in (-8, -6, -4, -2, 0)])
        assert np.all(np.log10(errs) + 8 > 0) and np.all(np.log10(bounds) + 8 < 10)
        xt = VGroup(*[MathTex(str(k), font_size=22, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.12)
                      for k in (0, 2, 4, 6, 8, 10)])
        n = np.arange(N)
        ed = VGroup(*[Dot(ax.c2p(k, math.log10(e) + 8), radius=0.07, color=C.FUNC) for k, e in zip(n, errs)])
        bd = polyline(ax, n, np.log10(bounds) + 8, color=C.UPPER_SUM, stroke_width=3)
        head = MathTex(r"e - P_n(1)", r"\ \le\ ", r"\frac{e}{(n+1)!}", font_size=38).to_edge(UP, buff=0.3)
        head[0].set_color(C.FUNC)
        head[2].set_color(C.UPPER_SUM)
        sub = label(r"$f = e^x$, \ $\alpha = 0$, \ $\beta = 1$: \ every derivative is $e^x \le e$", font_size=26,
                    color=GREY_A).next_to(head, DOWN, buff=0.15)
        nl = label(r"degree $n$", font_size=24, color=GREY_B).next_to(ax.c2p(N, 0), RIGHT, buff=0.2)
        with self.voiceover(
            "The unknown point is the price, but a bound on the n-th derivative turns the theorem into an error "
            "estimate. <bookmark mark='a'/> For e to the x between zero and one, every derivative is at most e, so the "
            "error of the degree n polynomial at one is at most e over n plus one factorial. <bookmark mark='b'/> On a "
            "log scale, the actual errors sit just under the bound, all the way down."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(nl), Create(bd), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in ed], lag_ratio=0.1), run_time=2.0)
        assert np.all((errs > 0) & (errs <= bounds))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def flat(self):
        d = load("taylor")
        ax = plain_axes([-3, 3, 1], [-0.2, 1.1, 0.5], 7.0, 3.6, numbers=True, font_size=20,
                        axis_config={"decimal_number_config": {"num_decimal_places": 1}}, x_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.0, -0.4, 0])
        f = lambda x: np.where(np.abs(x) < 1e-9, 0.0, np.exp(-1 / np.maximum(x * x, 1e-300)))  # noqa: E731
        g = ax.plot(f, x_range=[-3, 3, 0.005], color=C.FUNC, stroke_width=4)
        zero = Line(ax.c2p(-3, 0), ax.c2p(3, 0), color=C.APPROX, stroke_width=4)
        fl = MathTex(r"f(x) = e^{-1/x^2},\ \ f(0) = 0", font_size=30, color=C.FUNC).next_to(ax, UP, buff=0.2)
        head = label(r"A smooth function its Taylor series cannot see", font_size=34).to_edge(UP, buff=0.3)
        head = VGroup(head, note(r"Rudin, Exercise 8.1").next_to(head, DOWN, buff=0.1).align_to(head, RIGHT))
        facts = VGroup(label(r"every derivative at $0$ is $0$", font_size=26),
                       label(r"(sympy, orders $1$ to $10$: all $0$)", font_size=22, color=GREY_B),
                       label(r"so every Taylor polynomial at $0$ is $0$,", font_size=26, color=C.APPROX),
                       label(r"and the Taylor series converges everywhere,", font_size=26, color=C.APPROX),
                       label(r"to the wrong function", font_size=26, color=C.PATHOLOGY)).arrange(DOWN, aligned_edge=LEFT,
                                                                                               buff=0.15)
        facts.move_to([3.6, 0.9, 0])
        lx = plain_axes([0.0, 0.2, 0.1], [0, 60, 20], 4.9, 2.2, numbers=False).move_to([3.95, -1.95, 0])  # log10 + 60
        lxt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=18, color=GREY_B).next_to(lx.c2p(0, k + 60), LEFT, buff=0.1)
                       for k in (-60, -40, -20, 0)],
                     *[MathTex(f"{v:g}", font_size=18, color=GREY_B).next_to(lx.c2p(v, 0), DOWN, buff=0.1)
                       for v in (0.1, 0.2)])
        xx = np.linspace(0.02, 0.2, 400)
        x1 = np.linspace(math.sqrt(math.log10(math.e) / 60) + 1e-4, 0.2, 400)
        c1 = polyline(lx, x1, -math.log10(math.e) / x1**2 + 60, color=C.FUNC, stroke_width=3)
        c2 = polyline(lx, xx, 10 * np.log10(xx) + 60, color=C.EPS, stroke_width=3)
        ll = VGroup(MathTex(r"x^{10}", font_size=24, color=C.EPS).next_to(lx.c2p(0.06, 10 * math.log10(0.06) + 60), UP,
                                                                         buff=0.1),
                    MathTex(r"e^{-1/x^2}", font_size=24, color=C.FUNC).next_to(
                        lx.c2p(0.1, -math.log10(math.e) / 0.01 + 60), LEFT, buff=0.1),
                    label(r"log scale, $0 < x \le 0.2$", font_size=20, color=GREY_B).next_to(lx, UP, buff=0.05))
        with self.voiceover(
            "And the payoff museum piece. <bookmark mark='a'/> e to the minus one over x squared, with value zero at "
            "zero. It's infinitely differentiable, and it's so flat at zero that every derivative there is zero. "
            "<bookmark mark='b'/> So every Taylor polynomial at zero is the zero polynomial, and the Taylor series "
            "converges everywhere, to zero, which is the wrong function at every point but one. <bookmark mark='c'/> On "
            "a log scale, near zero it lies below x to the tenth, and below any other power you choose."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax), Create(g), FadeIn(fl), FadeIn(facts[0]), FadeIn(facts[1]))
            vo.wait_until("b")
            self.play(Create(zero), FadeIn(facts[2]), FadeIn(facts[3]))
            self.play(FadeIn(facts[4]))
            vo.wait_until("c")
            self.play(Create(lx), FadeIn(lxt), Create(c2), Create(c1), FadeIn(ll))
        assert d["zeros"].sum() == 10
        self.wait(0.3)
        card = museum_card(r"$e^{-1/x^2}$", r"Cauchy, 1823", r"smooth everywhere, but not the sum of its Taylor series",
                           r"Rudin, Exercise 8.1; in $\mathbb{C}$ this cannot happen (Part 7)").move_to([3.3, 0.5, 0])
        promise = VGroup(label(r"Part 7: complex-differentiable functions always equal their Taylor series.",
                               font_size=24, color=GREY_A),
                         label(r"Part 9: this flatness builds the bump functions of distribution theory.", font_size=24,
                               color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.4)
        # the specimen stays beside its card; for the Part 9 line it becomes a bump, e^{-1/(1 - x^2)} on (-1, 1)
        tax = plain_axes([-3, 3, 1], [-0.2, 1.1, 0.5], 5.6, 2.9, numbers=False).move_to([-3.4, 0.5, 0])
        xg = np.linspace(-3, 3, 1201)
        tg = polyline(tax, xg, f(xg), color=C.FUNC, stroke_width=4)
        inside = np.abs(xg) < 1
        bump_y = np.zeros_like(xg)
        bump_y[inside] = np.exp(-1 / (1 - xg[inside] ** 2))
        assert abs(bump_y.max() - math.exp(-1)) < 1e-4 and np.all(bump_y[~inside] == 0)
        tb = polyline(tax, xg, bump_y, color=C.TEST_FN, stroke_width=4)
        t_l = MathTex(r"e^{-1/x^2}", font_size=30, color=C.FUNC).next_to(tax, UP, buff=0.15)
        b_l = MathTex(r"e^{-1/(1 - x^2)} \text{ on } (-1, 1), \ 0 \text{ outside}", font_size=28,
                      color=C.TEST_FN).next_to(tax, UP, buff=0.15)
        others = [m for m in self.mobjects if m is not g and m is not ax]
        with self.voiceover(
            "Smooth isn't the same as analytic. Cauchy pointed this function out in 1823. <bookmark mark='p'/> In the "
            "complex plane this can't happen: a function with one complex derivative has all of them and equals its "
            "Taylor series, which is Part 7's surprise. <bookmark mark='q'/> And in Part 9 this flatness becomes useful, "
            "building the smooth bump functions that distribution theory runs on."
        ) as vo:
            self.play(*[FadeOut(m) for m in others], FadeOut(ax), FadeIn(tax), ReplacementTransform(g, tg),
                      FadeIn(t_l), run_time=1.2)
            self.play(FadeIn(card, scale=0.95))
            vo.wait_until("p")
            self.play(FadeIn(promise[0]))
            vo.wait_until("q")
            self.play(FadeIn(promise[1]), Transform(tg, tb), FadeTransform(t_l, b_l), run_time=1.5)
        self.wait(0.8)
        self.clear_scene()
