from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis6.common import area_under, load, plain_axes, polyline


class Lp(VoiceoverScene):
    def construct(self):
        self.card()
        self.norms()
        self.classes()
        self.inclusions()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(3, r"The spaces $L^p$", r"What exactly is a point of $L^p$?", lit=(), part=6)
        with self.voiceover("Chapter three: the spaces L p, and what their points really are."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def norms(self):
        d = load("lpnorms")
        ps, nv = d["ps"], d["norms"]
        ax = plain_axes([0, 1, 0.25], [0, 5.4, 1], 4.6, 3.8, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-4.0, -0.75, 0])
        x = np.linspace(0, 1, 300)
        g = polyline(ax, x, 2 * x, color=C.FUNC, stroke_width=4)
        hole = Circle(radius=0.05, color=C.FUNC, stroke_width=2).move_to(ax.c2p(0.3, 0.6))
        spike = VGroup(DashedLine(ax.c2p(0.3, 0.6), ax.c2p(0.3, 5), color=C.PATHOLOGY, stroke_width=1.5),
                       Dot(ax.c2p(0.3, 5), radius=0.07, color=C.PATHOLOGY))
        sp_l = MathTex(r"f(0.3) = 5", font_size=24, color=C.PATHOLOGY).next_to(ax.c2p(0.3, 5), RIGHT, buff=0.12)
        f_l = MathTex(r"f(x) = 2x \ \text{ (except at one point)}", font_size=24, color=C.FUNC).next_to(ax, UP, buff=0.12)
        lp = np.linspace(0, 2, 300)
        pp = 10**lp
        curve_y = 2 / (pp + 1) ** (1 / pp)
        nax = plain_axes([0, 2, 1], [0.8, 2.2, 0.4], 4.6, 3.4).move_to([2.2, -0.55, 0])
        ticks = VGroup(*[MathTex(t, font_size=22).next_to(nax.c2p(i, 0.8), DOWN, buff=0.12)
                         for i, t in enumerate(("1", "10", "100"))])
        yt = VGroup(*[MathTex(f"{v:.1f}", font_size=20).next_to(nax.c2p(0, v), LEFT, buff=0.1)
                      for v in (1.2, 1.6, 2.0)])
        p_l = MathTex(r"p", font_size=26, color=GREY_B).next_to(nax, DOWN, buff=0.45)
        ncur = polyline(nax, lp, curve_y, color=C.DIST, stroke_width=3.5)
        ess = DashedLine(nax.c2p(0, 2), nax.c2p(2, 2), color=C.EPS, stroke_width=2)
        ess_l = MathTex(r"\|f\|_\infty = \operatorname{ess\,sup} |f| = 2", font_size=26, color=C.EPS).next_to(
            nax.c2p(1.0, 2.0), UP, buff=0.1)
        pT = ValueTracker(0.0)

        def pnow():
            return 10 ** pT.get_value()

        def marker():
            p = pnow()
            v = 2 / (p + 1) ** (1 / p)
            return VGroup(Dot(nax.c2p(pT.get_value(), v), radius=0.07, color=C.DIST),
                          DashedLine(ax.c2p(0, v), ax.c2p(1, v), color=C.DIST, stroke_width=2))

        mk = always_redraw(marker)
        rd = always_redraw(lambda: MathTex(rf"p = {pnow():.1f}: \ \|f\|_p = \frac{{2}}{{(p + 1)^{{1/p}}}} = "
                                           rf"{2 / (pnow() + 1) ** (1 / pnow()):.4f}", font_size=28,
                                           color=C.DIST).next_to(nax, UP, buff=0.55))
        assert np.allclose(nv, 2 / (ps + 1) ** (1 / ps), rtol=1e-6)
        head = VGroup(MathTex(r"\|f\|_p = \Big(\int |f|^p\,d\mu\Big)^{1/p}", font_size=34),
                      MathTex(r"\|f\|_\infty = \inf\{M : |f| \le M \text{ a.e.}\}", font_size=34)
                      ).arrange(RIGHT, buff=0.8).to_edge(UP, buff=0.3)
        tab = MathTex(r"\|f\|_1, \|f\|_2, \|f\|_4, \|f\|_{10}, \|f\|_{100} = " +
                      r",\ ".join(f"{v:.3f}" for v in nv), font_size=24, color=GREY_A).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "<bookmark mark='a'/> The p-norm of a function is the p-th root of the integral of its absolute value to "
            "the p. The infinity norm is the essential supremum: the smallest bound that holds almost everywhere. "
            "<bookmark mark='b'/> Take f of x equals two x, but with one wild value: five, at the single point 0.3. "
            "<bookmark mark='c'/> As p grows, the p-norm rises: one, then 1.155, then on toward two. The integral "
            "gives more and more weight to where the function is largest. <bookmark mark='d'/> The limit is two, not "
            "five. The spike sits on a set of measure zero, and no integral can see it. So the essential supremum is "
            "two."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(Create(ax), Create(g), FadeIn(f_l))
            self.play(FadeIn(hole), FadeIn(spike), FadeIn(sp_l))
            vo.wait_until("c")
            self.play(Create(nax), FadeIn(ticks), FadeIn(yt), FadeIn(p_l), FadeIn(mk), FadeIn(rd))
            self.play(Create(ncur), pT.animate.set_value(2.0), run_time=5.0, rate_func=linear)
            self.play(FadeIn(tab))
            vo.wait_until("d")
            self.play(Create(ess), FadeIn(ess_l))
            self.play(Indicate(spike, color=C.PATHOLOGY))
        for m in (mk, rd):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def classes(self):
        ax = plain_axes([0, 1, 0.25], [0, 1.3, 0.5], 5.4, 3.4).move_to([-3.5, -0.5, 0])
        x = np.linspace(0, 1, 400)
        f = 0.55 + 0.35 * np.sin(2 * np.pi * x) * np.exp(-x)
        gf = polyline(ax, x, f, color=C.FUNC, stroke_width=4)
        rng = np.random.default_rng(5)
        pts = np.sort(rng.uniform(0.03, 0.97, 9))
        twin = VGroup()
        for t in pts:
            ft = 0.55 + 0.35 * math.sin(2 * math.pi * t) * math.exp(-t)
            twin.add(Circle(radius=0.045, color=C.APPROX, stroke_width=2).move_to(ax.c2p(t, ft)))
            twin.add(Dot(ax.c2p(t, ft + rng.choice([-1, 1]) * rng.uniform(0.25, 0.45)), radius=0.06, color=C.APPROX))
        t_l = label(r"$\tilde f$: \ $f$ changed at nine points", font_size=24, color=C.APPROX).next_to(ax, UP, buff=0.1)
        mapax = plain_axes([-1, 1, 1], [-1, 1, 1], 3.0, 3.0).move_to([3.6, 0.4, 0])
        mapax.set_opacity(0.4)
        dotf = Dot(mapax.c2p(0.2, 0.1), radius=0.09, color=C.FUNC)
        ring = Circle(radius=0.16, color=C.APPROX, stroke_width=3).move_to(dotf)
        m_l = label(r"in $L^p$: \ one point", font_size=24, color=GREY_A).next_to(mapax, UP, buff=0.12)
        facts = VGroup(
            MathTex(r"\|f - \tilde f\|_p = 0", font_size=32, color=C.EPS),
            label(r"$\|\cdot\|_p$ on functions: \ $\|f\| = 0$ only says $f = 0$ a.e.", font_size=24),
            label(r"so a point of $L^p$ is a class: \ $f \sim g$ when $f = g$ a.e.", font_size=24),
            label(r"a class has no value at a single point; \ chapter 13 recovers", font_size=22, color=GREY_A),
            label(r"values almost everywhere \ (Lebesgue points)", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.5, -2.35, 0])
        head = label(r"\textbf{RCA 3.10} \ functions equal almost everywhere are the same element of $L^p$",
                     font_size=30).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> That spike raises an honest question: what is a point of L p? "
            "<bookmark mark='b'/> Change a function at nine points, or at any set of measure zero. Every integral "
            "stays the same, so the distance between the two is zero. <bookmark mark='c'/> Then the p-norm isn't "
            "quite a norm on functions: a function with norm zero is only zero almost everywhere. The fix is to call "
            "two functions the same when they agree almost everywhere. A point of L p is such a class, and on the "
            "classes the p-norm is a genuine norm. <bookmark mark='d'/> The price: an element of L p has no value at "
            "a single point. Chapter 13 will get values back, almost everywhere."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(gf))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in twin], lag_ratio=0.1), FadeIn(t_l), run_time=2.0)
            self.play(FadeIn(facts[0]))
            vo.wait_until("c")
            self.play(Create(mapax), FadeIn(m_l), FadeIn(dotf), Create(ring))
            self.play(FadeIn(facts[1:3]))
            vo.wait_until("d")
            self.play(FadeIn(facts[3:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def inclusions(self):
        d = load("lpnorms")
        eps, half, one, R, two = d["eps"], d["half"], d["one"], d["R"], d["two"]
        ax = plain_axes([0, 1, 0.5], [0, 6, 2], 4.6, 3.2, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.6, -0.2, 0])
        bx = plain_axes([0, 8, 2], [0, 1.1, 0.5], 4.6, 3.2, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([3.0, -0.2, 0])
        x0 = np.linspace(1 / 36, 1, 400)
        f1 = polyline(ax, x0, x0**-0.5, color=C.CONNECTED_SET, stroke_width=4)
        a1 = area_under(ax, x0, x0**-0.5, C.CONNECTED_SET, 0.25)
        f2 = polyline(ax, np.linspace(1 / 6, 1, 300), np.linspace(1 / 6, 1, 300) ** -1, color=C.PATHOLOGY,
                      stroke_width=3)
        l1 = MathTex(r"x^{-1/2}", font_size=28, color=C.CONNECTED_SET).move_to(ax.c2p(0.42, 4.2))
        l2 = MathTex(r"(x^{-1/2})^2 = \tfrac1x", font_size=28, color=C.PATHOLOGY).move_to(ax.c2p(0.62, 2.4))
        x1 = np.linspace(1, 8, 300)
        g1 = polyline(bx, x1, 1 / x1, color=C.CONNECTED_SET, stroke_width=4)
        g2 = polyline(bx, x1, 1 / x1**2, color=C.PATHOLOGY, stroke_width=3)
        k1 = MathTex(r"\tfrac1x", font_size=28, color=C.CONNECTED_SET).move_to(bx.c2p(3.0, 0.55))
        k2 = MathTex(r"(\tfrac1x)^2", font_size=28, color=C.PATHOLOGY).move_to(bx.c2p(1.9, 0.12)).shift(RIGHT * 0.5)
        t1 = VGroup(
            MathTex(r"\varepsilon:\ " + r",\ ".join(sci(e, 0) for e in eps), font_size=24, color=GREY_A),
            MathTex(r"\int_\varepsilon^1 x^{-1/2} = " + r",\ ".join(f"{v:.4f}" for v in half) + r" \to 2",
                    font_size=24, color=C.CONNECTED_SET),
            MathTex(r"\int_\varepsilon^1 x^{-1} = " + r",\ ".join(f"{v:.1f}" for v in one) + r" \to \infty",
                    font_size=24, color=C.PATHOLOGY),
            label(r"on $(0, 1]$: \ in $L^1$, \ not in $L^2$", font_size=24, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(ax, DOWN, buff=0.2)
        t2 = VGroup(
            MathTex(r"R:\ " + r",\ ".join(sci(r_, 0) for r_ in R), font_size=24, color=GREY_A),
            MathTex(r"\int_1^R x^{-1} = " + r",\ ".join(f"{math.log(r_):.1f}" for r_ in R) + r" \to \infty",
                    font_size=24, color=C.CONNECTED_SET),
            MathTex(r"\int_1^R x^{-2} = " + r",\ ".join(f"1 - {sci(1 - v, 0)}" for v in two) + r" \to 1",
                    font_size=24, color=C.PATHOLOGY),
            label(r"on $[1, \infty)$: \ in $L^2$, \ not in $L^1$", font_size=24, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(bx, DOWN, buff=0.2)
        assert np.allclose(one, np.log(1 / eps)) and np.all(half < 2)
        head = VGroup(label(r"Is $L^2$ inside $L^1$, \ or the other way around?", font_size=32),
                      label(r"on a space of finite measure: \ $\|f\|_p \le \mu(X)^{1/p - 1/q}\,\|f\|_q$ \ for $p < q$ "
                            r"\ (H\"older), \ so $L^q \subset L^p$", font_size=24, color=GREY_A)
                      ).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.2)
        with self.voiceover(
            "<bookmark mark='a'/> Which spaces contain which? Near zero, x to the minus a half has a finite "
            "integral, two, but its square, one over x, doesn't: the integrals grow like the log of one over "
            "epsilon. So it's in L one, not in L two. Tall spikes break the higher norms. "
            "<bookmark mark='b'/> Out at infinity it's the other way. One over x has infinite integral, but its "
            "square has integral one. Long tails break the lower norms. <bookmark mark='c'/> On the whole line, "
            "neither space contains the other. On a space of finite measure there are no long tails, and Hölder "
            "gives the inclusion: the higher p, the smaller the space."
        ) as vo:
            self.play(FadeIn(head[0]))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(a1), Create(f1), FadeIn(l1))
            self.play(Create(f2), FadeIn(l2))
            self.play(FadeIn(t1[:3]))
            self.play(FadeIn(t1[3]))
            vo.wait_until("b")
            self.play(Create(bx), Create(g1), FadeIn(k1), Create(g2), FadeIn(k2))
            self.play(FadeIn(t2[:3]))
            self.play(FadeIn(t2[3]))
            vo.wait_until("c")
            self.play(FadeIn(head[1]))
        self.wait(0.4)
        self.clear_scene()
