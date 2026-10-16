from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis.analysis2.common import load, plain_axes, polyline


class NumberE(VoiceoverScene):
    def construct(self):
        self.card()
        self.series()
        self.compound()
        self.irrational()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(5, r"The number $e$", r"Two definitions, one number, and a proof that it is not a fraction",
                            lit=(), part=2)
        with self.voiceover(
            "Chapter five: the number e, defined twice, and a proof, entirely from the tail of a series, that it isn't "
            "a fraction."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def series(self):
        d = load("etail")
        dfn = MathTex(r"e = \sum_{n=0}^{\infty} \frac{1}{n!} = 1 + 1 + \frac12 + \frac16 + \frac1{24} + \cdots",
                      font_size=42).to_edge(UP, buff=0.3)
        ref = note(r"Rudin 3.30").next_to(dfn, DOWN, buff=0.12).align_to(dfn, RIGHT)
        rows = [MathTex(r"e - s_n", r"=", r"\frac{1}{(n+1)!} + \frac{1}{(n+2)!} + \cdots", font_size=38),
                MathTex(r"e - s_n", r"<", r"\frac{1}{(n+1)!}\Big(1 + \frac{1}{n+1} + \frac{1}{(n+1)^2} + \cdots\Big)",
                        font_size=38),
                MathTex(r"0 < e - s_n", r"<", r"\frac{1}{n!\, n}", font_size=38)]
        whys = [why(r"the tail"), why(r"$(n+k)! \ge (n+1)!\,(n+1)^{k-1}$"), why(r"sum the geometric series")]
        step = ladder(self, rows, whys, keep=2, top=1.95, buff=0.42, x=-0.9)
        # the error e - s_n against its bound 1/(n! n), on a log scale
        import mpmath as mp
        mp.mp.dps = 40
        ns = np.arange(1, 13)
        err = np.array([float(mp.e - mp.fsum(1 / mp.factorial(k) for k in range(n + 1))) for n in ns])
        bnd = np.array([1 / (math.factorial(n) * n) for n in ns])
        assert np.all((0 < err) & (err < bnd)) and abs(err[9] - float(d["err_s10"])) < 1e-20
        # heights are log10 + 10, so the horizontal axis runs along the bottom, at 10^-10
        ax = plain_axes([0, 13, 1], [0, 10.5, 5], 10.0, 2.1, numbers=False).move_to([-0.6, -2.45, 0])
        assert np.all(np.log10(err) + 10 > 0) and np.all(np.log10(bnd) + 10 < 10.5)
        ylab = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(0, v + 10), LEFT, buff=0.15)
                        for v in (0, -5, -10)])
        n_l = MathTex(r"n", font_size=24, color=GREY_B).next_to(ax.c2p(13, 0), RIGHT, buff=0.12)
        b_curve = polyline(ax, ns, np.log10(bnd) + 10, color=C.UPPER_SUM, stroke_width=2.5)
        e_dots = VGroup(*[Dot(ax.c2p(n, np.log10(v) + 10), radius=0.06, color=C.SEQ) for n, v in zip(ns, err)])
        b_l = MathTex(r"\frac{1}{n!\, n}", font_size=26, color=C.UPPER_SUM).next_to(ax.c2p(3, np.log10(bnd[2]) + 10), UR,
                                                                                buff=0.12)
        e_l = MathTex(r"e - s_n", font_size=26, color=C.SEQ).next_to(ax.c2p(3, np.log10(err[2]) + 10), DL, buff=0.15)
        fast = label(rf"$s_{{10}}$ is already within ${sci(float(d['err_s10']), 1)}$ of $e$", font_size=28,
                     color=C.EPS).move_to([2.6, -1.75, 0])
        ring = Circle(radius=0.13, color=C.EPS, stroke_width=3).move_to(e_dots[9])
        with self.voiceover(
            "Rudin defines e as the sum of one over n factorial. <bookmark mark='a'/> How fast does it converge? The "
            "error after n terms is the tail. <bookmark mark='b'/> Each later factorial is at least the first one times "
            "a power of n plus one, so the tail is smaller than a geometric series, <bookmark mark='c'/> and summing it, "
            "the error is less than one over n factorial times n. <bookmark mark='d'/> That's fast: s ten, which stops at one over ten "
            "factorial, is within three parts in a hundred million of e. Hold on to this inequality: it will prove that e is irrational."
        ) as vo:
            self.play(FadeIn(dfn), FadeIn(ref), Create(ax), FadeIn(ylab), FadeIn(n_l),
                      LaggedStart(*[FadeIn(x) for x in e_dots], lag_ratio=0.1), FadeIn(e_l))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            self.play(Create(b_curve), FadeIn(b_l))
            vo.wait_until("d")
            self.play(Create(ring), FadeIn(fast))
            self.keep_ineq = rows[2]
        assert float(d["err_s10"]) < 3e-8
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compound(self):
        d = load("etail")
        ns, terms = [int(v) for v in d["tn_n"]], d["tn_terms"]
        K = 5  # k = 0 .. 4; the boxes for k >= 5 would be under 0.03 high
        assert terms.shape[1] >= K
        H, w, x0, base = 3.5, 1.05, -6.4, -2.9
        outl = VGroup()
        for k in range(K):
            h = H / math.factorial(k)
            outl.add(Rectangle(width=w * 0.8, height=max(h, 0.01), stroke_color=C.SEQ, stroke_width=2.5,
                               fill_opacity=0).move_to([x0 + w * (k + 0.5), base + h / 2, 0]))
        klabs = VGroup(*[MathTex(rf"\tfrac{{1}}{{{k}!}}", font_size=24, color=C.SEQ).next_to(
            [x0 + w * (k + 0.5), base, 0], DOWN, buff=0.15) for k in range(K)])
        axis = Line([x0 - 0.1, base, 0], [x0 + w * K + 0.1, base, 0], color=GREY_C, stroke_width=2)

        def fill(i):
            g = VGroup()
            for k in range(K):
                h = H * terms[i][k]
                g.add(Rectangle(width=w * 0.8, height=max(h, 0.003), stroke_width=0, fill_color=C.CUT_HIGH,
                                fill_opacity=0.8).move_to([x0 + w * (k + 0.5), base + h / 2, 0]))
            return g

        head = MathTex(r"\Big(1 + \frac1n\Big)^n", r"=", r"\sum_{k=0}^{n} \frac{1}{k!}\Big(1 - \frac1n\Big)"
                       r"\Big(1 - \frac2n\Big) \cdots \Big(1 - \frac{k-1}{n}\Big)", font_size=36).to_edge(UP, buff=0.3)
        head[0].set_color(C.CUT_HIGH)
        ref = note(r"binomial theorem; \ Rudin 3.31").next_to(head, DOWN, buff=0.1).align_to(head, RIGHT)

        def nlab(i):
            n = ns[i]
            t = (1 + 1 / n) ** n
            return MathTex(rf"n = {n}:\quad \Big(1 + \tfrac1n\Big)^n = {t:.4f}", font_size=34, color=C.CUT_HIGH).move_to(
                [4.3, 1.5, 0])

        bars, nl = fill(0), nlab(0)
        cmp = VGroup(label(r"each orange bar is shorter than its blue box:", font_size=24),
                     label(r"$(1 + \tfrac1n)^n \le s_n < e$", font_size=26),
                     label(r"for fixed $k$, each bar fills its box as $n \to \infty$:", font_size=24),
                     label(r"the limit is at least $s_m$, for every $m$", font_size=26)).arrange(DOWN, aligned_edge=LEFT,
                                                                                            buff=0.12)
        cmp.move_to([4.0, 0.0, 0])
        for r in cmp:
            r.set_color(GREY_A)
        res = MathTex(r"\lim_{n \to \infty} \Big(1 + \frac1n\Big)^n = e", font_size=40, color=C.EPS).move_to([4.0, -1.85, 0])
        with self.voiceover(
            "The other definition of e is compound interest: one plus one over n, to the n-th power. "
            "<bookmark mark='a'/> Expand it with the binomial theorem. The k-th term is one over k factorial, "
            "<bookmark mark='b'/> times k minus one factors, each a little less than one. <bookmark mark='c'/> So in "
            "this picture each orange bar sits inside its blue box, of height one over k factorial: the compound-interest "
            "number is less than the series. <bookmark mark='d'/> As n grows, each shortfall factor tends to one, and "
            "the bars rise to fill their boxes."
        ) as vo:
            self.play(Create(axis), FadeIn(outl), FadeIn(klabs))
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(ref))
            vo.wait_until("b")
            self.play(FadeIn(bars), FadeIn(nl))
            vo.wait_until("c")
            self.play(Indicate(outl, color=C.SEQ, scale_factor=1.03))
            vo.wait_until("d")
            for i in range(1, len(ns)):
                nl2 = nlab(i)
                self.play(Transform(bars, fill(i)), FadeTransform(nl, nl2), run_time=0.9)
                nl = nl2
        with self.voiceover(
            "<bookmark mark='a'/> Squeezed from above by the series and, for each fixed number of terms, from below, "
            "<bookmark mark='b'/> the limit is e. The two definitions agree. <bookmark mark='c'/> But the compound "
            "interest version is slow: at n equal to ten it's still off by an eighth, where the series was off by three "
            "parts in a hundred million."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cmp))
            vo.wait_until("b")
            self.play(FadeIn(res))
            vo.wait_until("c")
            slow = VGroup(label(rf"at $n = 10$: \ off by ${float(d['err_t10']):.3f}$,", font_size=24, color=GREY_B),
                          label(rf"versus ${sci(float(d['err_s10']), 1)}$ for $s_{{10}}$", font_size=24, color=GREY_B)
                          ).arrange(DOWN, buff=0.08).next_to(res, DOWN, buff=0.22)
            self.play(FadeIn(slow))
        assert np.all(np.diff(terms, axis=0) >= -1e-15)
        for k in range(K):
            assert terms[-1][k] <= 1 / math.factorial(k) + 1e-15
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def irrational(self):
        d = load("etail")
        qs, tail = [int(v) for v in d["q"]], d["tail"]
        head = label(r"\textbf{Rudin 3.32} \ $e$ is irrational.", font_size=34).to_edge(UP, buff=0.3)
        rows = [MathTex(r"0 < q!\,(e - s_q)", r"<", r"\frac{1}{q}", font_size=40),
                MathTex(r"q!\, e = p\,(q-1)!,", r"\quad", r"q!\, s_q = q!\Big(1 + 1 + \tfrac12 + \cdots + \tfrac1{q!}\Big)",
                        font_size=36),
                MathTex(r"q!\,(e - s_q)", r"\in", r"\mathbb{Z} \cap \big(0, \tfrac1q\big) = \emptyset", font_size=40)]
        whys = [why(r"the tail estimate, times $q!$"), why(r"if $e = p/q$: \ both are integers"),
                why(r"no integer lies strictly between $0$ and $1$")]
        rows[2][2].set_color(C.PATHOLOGY)
        step = ladder(self, rows, whys, keep=3, top=2.75, buff=0.36, x=-0.4)
        y = -3.0
        X = lambda v: -5.6 + v * 11.2  # noqa: E731
        # a zoom strip above the line: [0, 0.15] spread over the full width, where the window and the dot get close
        yz, zw = -2.15, 0.15
        Z = lambda v: -5.6 + v / zw * 11.2  # noqa: E731
        zline = Line([Z(0), yz, 0], [Z(zw), yz, 0], color=GREY_C, stroke_width=2)
        zguides = VGroup(DashedLine([X(0), y + 0.22, 0], [Z(0), yz - 0.27, 0], color=GREY_B, stroke_width=1.5),
                         DashedLine([X(zw), y + 0.22, 0], [Z(zw), yz - 0.27, 0], color=GREY_B, stroke_width=1.5))
        zsrc = Rectangle(width=X(zw) - X(0), height=0.44, color=GREY_B, stroke_width=1.5).move_to(
            [(X(0) + X(zw)) / 2, y, 0])
        ztag = MathTex(rf"\times {1 / zw:.1f}", font_size=24, color=GREY_B).next_to([Z(zw), yz + 0.27, 0], UP, buff=0.08)
        ztag.align_to([Z(zw), 0, 0], RIGHT)
        zoom = VGroup(zline, zguides, zsrc, ztag)
        line = Line([X(0) - 0.2, y, 0], [X(1) + 0.2, y, 0], color=GREY_C, stroke_width=2)
        ints = VGroup(*[VGroup(Dot([X(v), y, 0], radius=0.07, color=WHITE),
                               MathTex(str(v), font_size=28).next_to([X(v), y, 0], DOWN, buff=0.2)) for v in (0, 1)])
        qv = ValueTracker(0)

        def window():
            i = int(round(qv.get_value()))
            q = qs[i]
            r = Rectangle(width=X(1 / q) - X(0), height=0.5, stroke_width=0, fill_color=C.EPS, fill_opacity=0.22)
            r.move_to([(X(0) + X(1 / q)) / 2, y, 0])
            edge = Line([X(1 / q), y - 0.17, 0], [X(1 / q), y + 0.3, 0], color=C.EPS, stroke_width=3)
            dot = Dot([X(tail[i]), y, 0], radius=0.08, color=C.SEQ)
            # the same on the zoom strip (the window clipped to the strip; the dot only once it is on it)
            zr = Rectangle(width=Z(min(1 / q, zw)) - Z(0), height=0.5, stroke_width=0, fill_color=C.EPS,
                           fill_opacity=0.22).move_to([(Z(0) + Z(min(1 / q, zw))) / 2, yz, 0])
            zedge = Line([Z(1 / q), yz - 0.3, 0], [Z(1 / q), yz + 0.3, 0], color=C.EPS, stroke_width=3).set_opacity(
                1.0 if 1 / q <= zw else 0.0)
            zdot = Dot([Z(min(tail[i], zw)), yz, 0], radius=0.08, color=C.SEQ).set_opacity(1.0 if tail[i] <= zw else 0.0)
            return VGroup(r, edge, dot, zr, zedge, zdot)

        win = always_redraw(window)

        def qlab(i):
            q = qs[i]
            return MathTex(rf"q = {q}:\quad q!\,(e - s_q) = {tail[i]:.4f} < \tfrac{{1}}{{{q}}}", font_size=30,
                           color=C.SEQ).move_to([0, -1.45, 0])

        ql = qlab(0)
        with self.voiceover(
            "Now the proof that e is irrational, as Rudin gives it. <bookmark mark='a'/> Multiply the tail estimate by "
            "q factorial: q factorial times e minus s q lies strictly between zero and one over q. "
            "<bookmark mark='b'/> Now suppose e were a fraction p over q. Then q factorial times e is an integer, and so "
            "is q factorial times s q, since every denominator in s q divides q factorial. <bookmark mark='c'/> So their "
            "difference is an integer strictly between zero and one, and there isn't one. <bookmark mark='d'/> Here's "
            "the actual quantity for q from 1 to 15: always inside the yellow window, which shrinks, and never reaching "
            "an integer."
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(ints), FadeIn(zoom))
            vo.wait_until("a")
            step(0)
            self.play(FadeIn(win), FadeIn(ql))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            self.play(*[Indicate(i_[0], color=C.PATHOLOGY, scale_factor=1.6) for i_ in ints])
            vo.wait_until("d")
            for i in range(1, len(qs)):
                ql2 = qlab(i)
                self.play(qv.animate.set_value(i), FadeTransform(ql, ql2), run_time=0.45)
                ql = ql2
        assert all(0 < t < 1 / q for t, q in zip(tail, qs))
        win.clear_updaters()
        more = label(r"Rudin adds: $e$ is not even algebraic \ (Hermite, 1873: $e$ is transcendental).", font_size=26,
                     color=GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "<bookmark mark='m'/> In fact e isn't a root of any polynomial with integer coefficients: Hermite proved "
            "that in 1873, and Rudin points to a short proof."
        ) as vo:
            vo.wait_until("m")
            self.play(FadeIn(more))
        self.wait(0.5)
        self.clear_scene()
