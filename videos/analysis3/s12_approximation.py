from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis3.common import load, plain_axes, polyline
from videos.analysis3.compute import c_landau, tent, trap


class Approximation(VoiceoverScene):
    def construct(self):
        self.card()
        self.kernel()
        self.slide()
        self.estimate()
        self.results()
        self.bernstein()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(11, r"Every continuous function is nearly a polynomial",
                            r"Can the simplest functions imitate all the others?", lit=(), part=3)
        with self.voiceover(
            "Chapter eleven. In 1885 Weierstrass proved that every continuous function on a closed interval is a "
            "uniform limit of polynomials."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def kernel(self):
        ax = plain_axes([-1, 1, 0.5], [0, 20, 5], 7.0, 4.4).move_to([-2.8, -0.9, 0])
        t = np.linspace(-1, 1, 2001)
        ns = [10, 100, 1000]
        cols = [C.SEQ, C.APPROX, C.EPS]
        ks = VGroup(*[runs(ax, t, c_landau(n) * (1 - t * t) ** n, col, 3.5) for n, col in zip(ns, cols)])
        labs = VGroup(*[MathTex(rf"n = {n}: \ c_n = {c_landau(n):.2f} < \sqrt{{n}} = {np.sqrt(n):.1f}", font_size=26,
                                color=col) for n, col in zip(ns, cols)]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        labs.move_to([3.8, -0.6, 0])
        for n in ns:
            assert c_landau(n) < np.sqrt(n)
        head = VGroup(label(r"\textbf{Rudin 7.26} \ Rudin's proof, with the Landau kernel", font_size=30),
                      MathTex(r"Q_n(x) = c_n (1 - x^2)^n, \qquad \int_{-1}^{1} Q_n = 1", font_size=34, color=C.FUNC)
                      ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        side = label(r"all its mass crowds into any $[-\delta, \delta]$", font_size=26, color=GREY_A).next_to(labs, DOWN,
                                                                                                    buff=0.3)
        with self.voiceover(
            "However wild the graph, some polynomial stays within any tolerance of it, all along the interval. "
            "<bookmark mark='a'/> Rudin's proof uses a family of polynomials that act like a narrowing bump: c n "
            "times one minus x squared, to the n, with c n chosen so the area is one. <bookmark mark='b'/> As n grows, "
            "the bump gets taller and narrower. The normalizing constant stays below root n, which is what the "
            "estimates need. <bookmark mark='c'/> And for any fixed delta, the fraction of the area outside the "
            "interval from minus delta to delta goes to zero."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax))
            vo.wait_until("a")
            self.play(FadeIn(head[1]), Create(ks[0]), FadeIn(labs[0]))
            vo.wait_until("b")
            self.play(Create(ks[1]), FadeIn(labs[1]))
            self.play(Create(ks[2]), FadeIn(labs[2]))
            vo.wait_until("c")
            self.play(FadeIn(side))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def slide(self):
        n = 60
        c = c_landau(n)
        ax = plain_axes([0, 1, 0.25], [0, 0.75, 0.25], 8.6, 4.4).move_to([-1.6, -1.0, 0])
        xx = np.linspace(0, 1, 801)
        gf = polyline(ax, xx, tent(xx), color=WHITE, stroke_width=3)
        tt = np.linspace(0, 1, 4001)
        ft = tent(tt)
        P = np.array([np.sum(ft * c * np.clip(1 - (tt - x) ** 2, 0, None) ** n) * (tt[1] - tt[0]) for x in xx])
        xT = ValueTracker(0.05)

        def kern():
            x0 = xT.get_value()
            k = c * np.clip(1 - (tt - x0) ** 2, 0, None) ** n
            ks = 0.6 / c  # scale the kernel to fit the axes
            return VGroup(polyline(ax, tt, k * ks, color=C.APPROX, stroke_width=2.5),
                          DashedLine(ax.c2p(x0, 0), ax.c2p(x0, 0.75), color=C.APPROX, stroke_width=1.5))

        kg = always_redraw(kern)
        trace = always_redraw(lambda: polyline(ax, xx[xx <= xT.get_value()], P[xx <= xT.get_value()], color=C.EPS,
                                               stroke_width=4) if xT.get_value() > 0.06 else VMobject())
        dot = always_redraw(lambda: Dot(ax.c2p(xT.get_value(), float(np.interp(xT.get_value(), xx, P))), radius=0.07,
                                        color=C.EPS))
        head = VGroup(MathTex(r"P_n(x) = \int_{-1}^{1} f(x + t)\,Q_n(t)\,dt = \int_0^1 f(t)\,Q_n(t - x)\,dt",
                              font_size=34),
                      label(r"a weighted average of $f$ near $x$; \ and a polynomial in $x$ (expand $Q_n(t - x)$)",
                            font_size=24, color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        side = VGroup(label(r"$f$: \ continuous, \ $f(0) = f(1) = 0$", font_size=24),
                      label(r"(subtract a line first, \ if needed)", font_size=22, color=GREY_B),
                      label(rf"here $n = {n}$", font_size=24, color=C.APPROX)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        side.move_to([4.9, 0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Take a continuous f on the interval from zero to one, vanishing at the ends: any "
            "continuous function can be brought to this form by subtracting a straight line. <bookmark mark='b'/> "
            "Slide the bump along, and at each x record the bump-weighted average of f near x. "
            "<bookmark mark='c'/> That average, as a function of x, is a polynomial, because the bump is a polynomial "
            "in t minus x. Where f has a corner, the average rounds it off. As n grows the bump narrows and the "
            "average hugs f more closely."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax), Create(gf))
            vo.wait_until("a")
            self.play(FadeIn(side))
            vo.wait_until("b")
            self.play(FadeIn(kg), FadeIn(dot))
            self.add(trace)
            self.play(xT.animate.set_value(0.95), run_time=6.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(head[1]))
        for m in (kg, trace, dot):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def estimate(self):
        rows = [
            MathTex(r"|P_n(x) - f(x)|", r"\le", r"\int_{-1}^{1} |f(x + t) - f(x)|\,Q_n(t)\,dt", font_size=32),
            MathTex(r"|P_n(x) - f(x)|", r"\le", r"2M \int_{\delta \le |t| \le 1} Q_n + \frac{\varepsilon}{2}\int_{|t| < \delta} Q_n",
                    font_size=32),
            MathTex(r"|P_n(x) - f(x)|", r"\le", r"4M\sqrt n\,(1 - \delta^2)^n + \frac{\varepsilon}{2} < \varepsilon",
                    font_size=32),
        ]
        whys = [why(r"$\int Q_n = 1$"), why(r"far: \ $|f| \le M$; \ \ near: \ uniform continuity"),
                why(r"$c_n < \sqrt n$; \ then $n$ large, \ the same $n$ for every $x$")]
        for r_ in rows:
            r_.scale(0.88)
        step = ladder(self, rows, whys, keep=3, top=2.95, buff=0.3, x=-1.2)
        head = label(r"Why it converges uniformly", font_size=30).to_edge(UP, buff=0.15)
        # the picture behind the split: the kernel's mass near 0 and far from it
        n, dl = 60, 0.25
        c = c_landau(n)
        tq = np.linspace(-1, 1, 4001)
        Q = c * (1 - tq**2) ** n
        kx = plain_axes([-1, 1, 0.5], [0, 1.08, 0.5], 6.6, 1.45).move_to([-3.2, -2.85, 0])
        near = tq[np.abs(tq) <= dl]
        shade_n = Polygon(*([kx.c2p(near[0], 0)] + [kx.c2p(a, b / Q.max()) for a, b in zip(near[::8], Q[np.abs(tq) <= dl][::8])]
                            + [kx.c2p(near[-1], 0)]), stroke_width=0, fill_color=C.CONNECTED_SET, fill_opacity=0.45)
        far_parts = VGroup()
        for msk in (tq < -dl, tq > dl):
            xs_, ys_ = tq[msk], Q[msk] / Q.max()
            far_parts.add(Polygon(*([kx.c2p(xs_[0], 0)] + [kx.c2p(a, b) for a, b in zip(xs_[::8], ys_[::8])]
                                    + [kx.c2p(xs_[-1], 0)]), stroke_width=0, fill_color=C.PATHOLOGY, fill_opacity=0.6))
        kq = polyline(kx, tq, Q / Q.max(), color=C.APPROX, stroke_width=2.5)
        kl = MathTex(rf"Q_{{{n}}}, \ \delta = {dl}", font_size=24, color=C.APPROX).next_to(kx, UP, buff=0.05)
        kl.align_to(kx, LEFT)
        far_mass = trap(np.where(np.abs(tq) > dl, Q, 0.0), tq)
        bound = 2 * np.sqrt(n) * (1 - dl**2) ** n
        assert far_mass <= bound and abs(trap(Q, tq) - 1) < 1e-6
        nums = VGroup(label(r"near ($|t| < \delta$): \ $|f(x + t) - f(x)| < \varepsilon/2$", font_size=24,
                            color=C.CONNECTED_SET),
                      label(rf"far: \ mass $= {far_mass:.4f} \le 2\sqrt n\,(1 - \delta^2)^n = {bound:.4f}$", font_size=24,
                            color=C.PATHOLOGY),
                      label(r"$\sqrt n\,(1 - \delta^2)^n \to 0$: \ exponential decay beats the square root",
                            font_size=24, color=C.EPS)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        for r_ in nums:
            if r_.width > 6.3:
                r_.width = 6.3
        nums.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.55, -2.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The estimate is the epsilon-over-two trick again. Because the bump has area one, the "
            "error at x is at most the bump-weighted average of the gaps between f near x and f at x. "
            "<bookmark mark='b'/> Split the average. Near x, within delta, the gaps are below epsilon over two, by "
            "uniform continuity. Far from x, the gaps are at most two M, but the bump has almost no mass there. "
            "<bookmark mark='c'/> With c n below root n, the far part is at most four M root n times one minus delta "
            "squared, to the n, which goes to zero. The bound doesn't depend on x, so the convergence is uniform."
        ) as vo:
            self.play(FadeIn(head), Create(kx), Create(kq), FadeIn(kl))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            self.play(FadeIn(shade_n), FadeIn(nums[0]))
            self.play(FadeIn(far_parts), FadeIn(nums[1]))
            vo.wait_until("c")
            step(2)
            self.play(FadeIn(nums[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        d = load("landau")
        ns, x, P, err = d["ns"], d["x"], d["P"], d["err"]
        ax = plain_axes([0, 1, 0.25], [0, 0.65, 0.25], 7.0, 4.4).move_to([-2.9, -0.8, 0])
        gf = polyline(ax, x, tent(x), color=WHITE, stroke_width=3)
        head = label(r"Computed: \ the Landau approximants of a tent", font_size=32).to_edge(UP, buff=0.35)
        show = [0, 2, 4, 6]
        cols = [C.SEQ, C.APPROX, C.CLOSED_SET, C.EPS]
        curves = [polyline(ax, x, P[i], color=col, stroke_width=3) for i, col in zip(show, cols)]
        tab = VGroup(MathTex(r"n", r"\quad \sup|P_n - f|", font_size=28, color=GREY_A))
        for i in range(len(ns)):
            tab.add(MathTex(rf"{int(ns[i])}", rf"\quad {err[i]:.4f}", font_size=28))
        tab.arrange(DOWN, aligned_edge=RIGHT, buff=0.15).move_to([4.2, -0.4, 0])
        note_ = VGroup(label(r"the error is worst at the corners,", font_size=24, color=GREY_A),
                       label(r"and shrinks like $1/\sqrt n$", font_size=24, color=GREY_A)
                       ).arrange(DOWN, buff=0.08).next_to(tab, DOWN, buff=0.35)
        assert np.all(np.diff(err) < 0) and err[-1] < 0.005
        with self.voiceover(
            "<bookmark mark='a'/> Here's the construction carried out for a tent with two corners. "
            "<bookmark mark='b'/> With n equal to ten thousand, the polynomial, of degree twenty thousand, is within "
            "five thousandths of the tent everywhere. The error is largest at the corners, and shrinks roughly like one "
            "over root n."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(gf))
            vo.wait_until("a")
            self.play(Create(curves[0]), FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("b")
            cur = curves[0]
            for k, i in enumerate(show[1:], start=1):
                self.play(ReplacementTransform(cur, curves[k]), LaggedStart(*[FadeIn(tab[j + 1]) for j in
                                                                          range(show[k - 1] + 1, i + 1)], lag_ratio=0.3),
                          run_time=1.2)
                cur = curves[k]
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bernstein(self):
        d = load("landau")
        bns, x, Bv, berr = d["bns"], d["x"], d["Bv"], d["berr"]
        ax = plain_axes([0, 1, 0.25], [0, 0.65, 0.25], 6.6, 3.8).move_to([-3.1, -1.1, 0])
        gf = polyline(ax, x, tent(x), color=WHITE, stroke_width=3)
        head = VGroup(label(r"Another route: \ Bernstein's polynomials (1912)", font_size=32),
                      MathTex(r"B_n f(x) = \sum_{k=0}^{n} f\!\left(\tfrac kn\right) \binom nk x^k (1 - x)^{n-k}",
                              font_size=34)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        curves = [polyline(ax, x, Bv[i], color=C.APPROX, stroke_width=3) for i in range(len(bns))]
        side = VGroup(label(r"flip $n$ coins that land heads with probability $x$;", font_size=24),
                      label(r"average $f$ at the fraction of heads", font_size=24),
                      label(r"law of large numbers: \ the fraction $\to x$", font_size=24, color=C.EPS),
                      VGroup(*[MathTex(rf"n = {int(n)}: \ {e:.4f}", font_size=24) for n, e in zip(bns, berr)]
                             ).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.9, -0.9, 0])
        use = label(r"either way: \ $|x| \approx$ a polynomial on $[-a, a]$, \ which the next chapter needs", font_size=24,
                    color=C.EPS).to_edge(DOWN, buff=0.2)
        assert np.all(np.diff(berr) < 0)
        with self.voiceover(
            "<bookmark mark='a'/> There's a second, probabilistic proof, due to Bernstein. At x, flip n coins that "
            "each land heads with probability x, and average f over the fraction of heads. That average is a "
            "polynomial in x. <bookmark mark='b'/> By the law of large numbers, the fraction of heads concentrates "
            "near x, so the average approaches f of x, uniformly. <bookmark mark='c'/> Either proof gives a fact the "
            "next chapter needs: the absolute value function is a uniform limit of polynomials on any interval."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(gf))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]), Create(curves[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
            cur = curves[0]
            for k in range(1, len(bns)):
                self.play(ReplacementTransform(cur, curves[k]), run_time=0.8)
                cur = curves[k]
            vo.wait_until("c")
            self.play(FadeIn(use))
        self.wait(0.4)
        self.clear_scene()
