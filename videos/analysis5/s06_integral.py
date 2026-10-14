from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis5.common import area_under, cut_graph, escape_arrow, interval_band, load, plain_axes, polyline
from videos.analysis5.compute import trap


class Integral(VoiceoverScene):
    def construct(self):
        self.card()
        self.simple_integral()
        self.mct()
        self.proof()
        self.series()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(5, r"The integral, and monotone convergence",
                            r"How do we integrate, \ and when do limits pass through?", lit=(1902,), part=5)
        with self.voiceover("Chapter five: the integral itself, and its first limit theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def simple_integral(self):
        d = load("simple")
        x, f, S = d["x"], d["f"], d["S"]
        ax = plain_axes([0, 2, 0.5], [0, 6.5, 1], 7.0, 4.4).move_to([-2.9, -0.8, 0])
        fg = polyline(ax, x, f, color=WHITE, stroke_width=3)
        If = trap(f, x)
        ints = [trap(S[k], x) for k in range(len(S))]
        assert all(a <= b + 1e-9 for a, b in zip(ints, ints[1:])) and ints[-1] <= If and If - ints[-1] < 0.01
        shown = [0, 1, 3, 7]
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.MEASURE), k / 7) for k in range(8)]
        areas = [area_under(ax, x[::2], S[k][::2], cols[k], 0.5) for k in shown]
        head = VGroup(label(r"The integral of $f \ge 0$", font_size=34),
                      MathTex(r"\int s\,d\mu = \sum_i \alpha_i\, \mu(A_i), \qquad \int f\,d\mu = \sup\Big\{\int s\,d\mu : "
                              r"0 \le s \le f,\ s \text{ simple}\Big\}", r"\quad \text{\small (RCA 1.23)}", font_size=32,
                              color=C.MEASURE)
                      ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        head[1][1].set_color(GREY_B)
        tab = VGroup(MathTex(r"n", r"\quad \int s_n", font_size=28, color=GREY_A))
        for k in range(8):
            tab.add(MathTex(rf"{k + 1}", rf"\quad {ints[k]:.5f}", font_size=28))
        tab.add(MathTex(r"\int f", rf"\quad {If:.5f}", font_size=28, color=WHITE))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.2, -0.8, 0])
        regrid(tab)
        # one simple function under f, taken apart: values 1, 2.5, 4 on the level sets A_i, and its integral as
        # the sum of value times measure
        lv = [1.0, 2.5, 4.0]
        hi_ = lv[1:] + [np.inf]
        s_ex = np.select([f >= 4.0, f >= 2.5, f >= 1.0], [4.0, 2.5, 1.0], 0.0)
        mus = [float(trap(((f >= a_) & (f < b_)).astype(float), x)) for a_, b_ in zip(lv, hi_)]
        I_ex = sum(a_ * m_ for a_, m_ in zip(lv, mus))
        assert abs(I_ex - float(trap(s_ex, x))) < 5e-3 and np.all(s_ex <= f)
        lcols = [C.SEQ, C.CONNECTED_SET, C.MEASURE]

        def runs_of(mask):
            out, st = [], None
            for i in range(len(x) + 1):
                o = i < len(x) and mask[i]
                if o and st is None:
                    st = i
                elif not o and st is not None:
                    out.append((x[st], x[i - 1]))
                    st = None
            return out

        ex_areas = VGroup(*[area_under(ax, x[::2], np.where(s_ex == a_, a_, 0.0)[::2], c_, 0.55)
                            for a_, c_ in zip(lv, lcols)])
        y0 = ax.c2p(0, 0)[1]
        ex_bands = VGroup(*[interval_band(ax, runs_of((f >= a_) & (f < b_)), y0 - 0.22 - 0.16 * i, c_, height=0.1)
                            for i, (a_, b_, c_) in enumerate(zip(lv, hi_, lcols))])
        ex_txt = VGroup(
            MathTex(r"s = 1 \cdot \mathbf 1_{A_1} + 2.5 \cdot \mathbf 1_{A_2} + 4 \cdot \mathbf 1_{A_3} \le f", font_size=28),
            *[MathTex(rf"\mu(A_{i + 1}) = {m_:.4f}", font_size=28, color=c_) for i, (m_, c_) in enumerate(zip(mus, lcols))],
            MathTex(rf"\int s = 1 \cdot {mus[0]:.4f} + 2.5 \cdot {mus[1]:.4f} + 4 \cdot {mus[2]:.4f}", font_size=26),
            MathTex(rf"= {I_ex:.4f} \le \int f = {If:.4f}", font_size=28, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([4.0, -0.9, 0])
        for r_ in ex_txt:
            if r_.width > 5.6:
                r_.width = 5.6
        ex_txt.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([4.0, -0.9, 0])
        assert ex_txt.get_right()[0] < 6.95 and ex_txt.get_left()[0] > ax.get_right()[0] + 0.15
        assert ex_bands.get_bottom()[1] > -3.95
        with self.voiceover(
            "<bookmark mark='a'/> The integral of a simple function is what it should be: <bookmark mark='s1'/> each "
            "value times the measure of the set where it's taken, added up. <bookmark mark='s2'/> The integral of a "
            "non-negative measurable function is the supremum of the integrals of the simple functions below it. "
            "<bookmark mark='b'/> With the dyadic simple "
            "functions from the last chapter, the areas climb, <bookmark mark='c'/> and close in on the area under "
            "f."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax), Create(fg))
            vo.wait_until("a")
            self.play(FadeIn(head[1]))
            vo.wait_until("s1")
            self.play(LaggedStart(*[FadeIn(a_) for a_ in ex_areas], lag_ratio=0.3), FadeIn(ex_txt[0]), run_time=1.5)
            self.play(LaggedStart(*[AnimationGroup(FadeIn(b_), FadeIn(t_)) for b_, t_ in zip(ex_bands, ex_txt[1:4])],
                                  lag_ratio=0.4), run_time=2.0)
            self.play(FadeIn(ex_txt[4]))
            vo.wait_until("s2")
            self.play(FadeIn(ex_txt[5]))
            vo.wait_until("b")
            self.play(FadeOut(VGroup(ex_areas, ex_bands, ex_txt)))
            self.play(FadeIn(areas[0]), FadeIn(tab[0]), FadeIn(tab[1]))
            cur = areas[0]
            for j, k in enumerate(shown[1:], start=1):
                self.play(ReplacementTransform(cur, areas[j]),
                          LaggedStart(*[FadeIn(tab[i + 1]) for i in range(shown[j - 1] + 1, k + 1)], lag_ratio=0.3),
                          run_time=1.3)
                cur = areas[j]
            vo.wait_until("c")
            self.play(FadeIn(tab[-1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mct(self):
        d = load("mct")
        ns, ints = d["ns"], d["ints"]
        ax = plain_axes([0, 1, 0.25], [0, 8.5, 2], 7.0, 4.1).move_to([-2.9, -0.55, 0])
        x = np.linspace(1e-4, 1, 3000)
        # the limit x^(-1/2) is unbounded: cut where it leaves the window, with an arrow (no false plateau at the top)
        full = cut_graph(ax, x, x**-0.5, WHITE, 3)
        assert len(full) == 1
        up = escape_arrow(ax, 8.5**-2, WHITE)
        nT = ValueTracker(1.0)

        def fn():
            n = max(1, round(nT.get_value()))  # a sequence: n steps through the integers
            y = np.minimum(x**-0.5, n)  # f_n itself (n <= 8 stays inside the window, top 8.5)
            return VGroup(area_under(ax, x, y, C.MEASURE, 0.45), polyline(ax, x, y, color=C.FUNC, stroke_width=3))

        g = always_redraw(fn)
        rd = always_redraw(lambda: MathTex(
            rf"n = {max(1, round(nT.get_value()))}: \ \int_0^1 f_n = 2 - \tfrac1n = {2 - 1 / max(1, round(nT.get_value())):.4f}",
            font_size=28,
            color=C.MEASURE).next_to(ax, DOWN, buff=0.2))
        head = VGroup(label(r"Monotone convergence", font_size=34),
                      MathTex(r"0 \le f_1 \le f_2 \le \dots \to f \text{ pointwise} \ \Rightarrow \ ",
                              r"\int f_n\,d\mu \to \int f\,d\mu", r"\quad \text{\small (RCA 1.26)}", font_size=34)
                      ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        head[1][1].set_color(C.EPS)
        head[1][2].set_color(GREY_B)
        side = VGroup(MathTex(r"f_n = \min\big(x^{-1/2}, n\big) \nearrow x^{-1/2}", font_size=30, color=C.FUNC),
                      MathTex(r"\int_0^1 x^{-1/2}\,dx = 2", font_size=32),
                      label(r"no uniformity, \ no lid: \ only monotonicity", font_size=26, color=C.EPS),
                      label(r"(the limit is unbounded: \ for Riemann an improper integral)", font_size=22,
                            color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -0.6, 0])
        assert np.all(np.diff(ints) > 0) and abs(ints[-1] - (2 - 1 / 40)) < 1e-12
        with self.voiceover(
            "<bookmark mark='a'/> The first limit theorem is the monotone convergence theorem: if non-negative "
            "functions increase to a limit at every point, their integrals increase to the integral of the limit. "
            "<bookmark mark='b'/> Here the functions are one over root x, cut off at height n. Each is bounded; the "
            "limit is not. <bookmark mark='c'/> Their integrals are two minus one over n, climbing to two, the "
            "integral of one over root x. <bookmark mark='d'/> No uniform convergence was needed, and no lid: only "
            "that the functions increase."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax), Create(full), GrowArrow(up))
            vo.wait_until("a")
            self.play(FadeIn(head[1]))
            vo.wait_until("b")
            self.play(FadeIn(g), FadeIn(rd), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(nT.animate.set_value(8.0), run_time=5.0, rate_func=linear)
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2:]))
        for m in (g, rd):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def proof(self):
        ax = plain_axes([0, 2, 0.5], [0, 2.0, 0.5], 7.2, 4.0).move_to([-2.8, -0.55, 0])
        x = np.linspace(0, 2, 1601)
        f = 1.1 + 0.45 * np.sin(4 * x) + 0.15 * x
        edges = np.linspace(0, 2, 9)
        idx = np.clip(np.searchsorted(edges, x, side="right") - 1, 0, 7)
        svals = np.array([f[(x >= a) & (x <= b)].min() * 0.95 for a, b in zip(edges[:-1], edges[1:])])
        s = svals[idx]
        c = 0.8
        assert np.all(s <= f)
        fg = polyline(ax, x, f, color=WHITE, stroke_width=3)
        sg = VGroup(*[Line(ax.c2p(a, v), ax.c2p(b, v), color=C.MEASURE, stroke_width=3) for a, b, v in
                      zip(edges[:-1], edges[1:], svals)])
        csg = VGroup(*[DashedLine(ax.c2p(a, c * v), ax.c2p(b, c * v), color=C.MEASURE, stroke_width=2) for a, b, v in
                       zip(edges[:-1], edges[1:], svals)])
        nT = ValueTracker(1.0)

        def fn_vals(n):
            return f * (1 - np.exp(-n * x))

        def picture():
            n = max(1, round(nT.get_value()))
            y = fn_vals(n)
            E = y >= c * s
            runs_, start = [], None
            for i in range(len(x) + 1):
                o = i < len(x) and E[i]
                if o and start is None:
                    start = i
                elif not o and start is not None:
                    runs_.append((x[start], x[i - 1]))
                    start = None
            return VGroup(polyline(ax, x, y, color=C.FUNC, stroke_width=3),
                          interval_band(ax, runs_, ax.c2p(0, 0)[1] - 0.3, C.CONNECTED_SET, height=0.14))

        pic = always_redraw(picture)

        def int_En(n):
            y = fn_vals(n)
            return trap(np.where(y >= c * s, c * s, 0.0), x)

        rd = always_redraw(lambda: MathTex(
            rf"n = {max(1, round(nT.get_value()))}: \ \int_{{E_n}} c\,s = {int_En(max(1, round(nT.get_value()))):.4f} \to c\int s = "
            rf"{c * trap(s, x):.4f}", font_size=28, color=C.CONNECTED_SET).next_to(ax, DOWN, buff=0.55))
        vals = [int_En(n) for n in (1, 2, 5, 20, 100, 1000)]
        assert all(a <= b + 1e-12 for a, b in zip(vals, vals[1:])) and abs(vals[-1] - c * trap(s, x)) < 1e-2
        rows = VGroup(
            label(r"$\alpha = \lim \int f_n \le \int f$ \ (monotone)", font_size=26),
            label(r"fix a simple $s \le f$ \ and $c < 1$:", font_size=26),
            MathTex(r"E_n = \{x : f_n(x) \ge c\,s(x)\} \nearrow X", font_size=30, color=C.CONNECTED_SET),
            MathTex(r"\int f_n \ge \int_{E_n} f_n \ge c \int_{E_n} s \to c \int s", font_size=30),
            label(r"(continuity from below, 1.19)", font_size=22, color=GREY_A),
            label(r"so $\alpha \ge c \int s$ for all $c < 1$, \ all $s \le f$: \ $\alpha \ge \int f$", font_size=26,
                  color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).move_to([3.7, -0.4, 0])
        for r_ in rows:
            if r_.width > 6.2:
                r_.width = 6.2
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.17).move_to([3.7, -0.4, 0])
        head = label(r"Rudin's proof: \ the sets $E_n$ swallow the whole space", font_size=34).to_edge(UP, buff=0.3)
        labs = VGroup(MathTex("f", font_size=30).next_to(ax.c2p(2, f[-1]), RIGHT, buff=0.1),
                      MathTex("s", font_size=30, color=C.MEASURE).next_to(ax.c2p(2, svals[-1]), RIGHT, buff=0.1),
                      MathTex("cs", font_size=26, color=C.MEASURE).next_to(ax.c2p(2, c * svals[-1]), RIGHT, buff=0.1))
        x_free = max(l_.get_right()[0] for l_ in labs) + 0.25  # the text column starts right of the curve labels
        if rows.get_left()[0] < x_free:
            if rows.width > 6.95 - x_free:
                rows.width = 6.95 - x_free
            rows.shift((x_free - rows.get_left()[0]) * RIGHT)
        with self.voiceover(
            "<bookmark mark='a'/> The proof is short and worth seeing. The integrals of f n increase, so they have a "
            "limit alpha, at most the integral of f. <bookmark mark='b'/> For the other direction, fix a simple "
            "function s below f, and a number c a little less than one. <bookmark mark='c'/> Let E n be the set where "
            "f n has already climbed above c times s. Because f n increases to f, which is above c s wherever s is "
            "positive, these sets grow and swallow everything. <bookmark mark='d'/> On E n, the integral of f n is at "
            "least c times the integral of s over E n, and by continuity of the measure from below, that tends to c "
            "times the integral of s. <bookmark mark='e'/> So alpha is at least c times the integral of s, for every c "
            "less than one and every simple s below f, which by definition means alpha is at least the integral of f."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(fg), FadeIn(labs[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(sg), Create(csg), FadeIn(labs[1:]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(pic), FadeIn(rows[2]), FadeIn(rd))
            self.play(nT.animate.set_value(40.0), run_time=5.0, rate_func=rate_functions.ease_in_quad)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(rows[4]))
            vo.wait_until("e")
            self.play(FadeIn(rows[5]))
        for m in (pic, rd):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def series(self):
        x = np.linspace(0, 1 - 1e-9, 400001)
        g = -np.log1p(-x) / np.where(x == 0, 1, x)
        g[0] = 1.0
        I = trap(g, x)
        assert abs(I - math.pi**2 / 6) < 2e-3
        ax = plain_axes([0, 1, 0.25], [0, 5.0, 1], 6.6, 4.0).move_to([-3.2, -0.8, 0])
        xs = np.linspace(0, 0.995, 800)
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.APPROX), k / 7) for k in range(8)]
        partial = [sum(xs ** (k - 1) / k for k in range(1, K + 1)) for K in range(1, 9)]
        assert max(p_.max() for p_ in partial) < 5.0  # the partial sums stay inside the window
        layers = [polyline(ax, xs, p_, color=cols[k], stroke_width=2.5) for k, p_ in enumerate(partial)]
        # the limit, with its value 1 at x = 0 (the guard must give the limit, not 0), cut where it leaves the window
        gs = np.where(xs == 0, 1.0, -np.log1p(-xs) / np.where(xs == 0, 1, xs))
        assert gs[0] == 1.0 and np.all(np.diff(gs) > 0) and np.allclose(gs[1:6], 1 + xs[1:6] / 2, atol=1e-4)
        fullc = cut_graph(ax, xs, gs, WHITE, 3.5)
        assert len(fullc) == 1
        full = VGroup(fullc[0], escape_arrow(ax, float(np.interp(5.0, gs, xs)), WHITE))
        head = VGroup(label(r"For $f_k \ge 0$: \ $\int \sum_k f_k = \sum_k \int f_k$", font_size=34),
                      MathTex(r"\int_0^1 \frac{-\log(1 - x)}{x}\,dx = \int_0^1 \sum_{k \ge 1} \frac{x^{k-1}}{k}\,dx = "
                              r"\sum_{k \ge 1} \frac{1}{k^2} = \frac{\pi^2}{6}", r"\quad \text{\small (RCA 1.27)}",
                              font_size=32, color=C.EPS)
                      ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        head[1][1].set_color(GREY_B)
        side = VGroup(label(r"every term is $\ge 0$: \ no conditions to check", font_size=26),
                      MathTex(rf"\text{{computed: }} \int_0^1 \frac{{-\log(1 - x)}}{{x}}\,dx = {I:.4f}", font_size=30),
                      MathTex(rf"\pi^2 / 6 = {math.pi**2 / 6:.4f}", font_size=30, color=C.EPS),
                      label(r"Part 3's Basel sum, \ by a third route", font_size=24, color=GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.6, -0.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A corollary: for non-negative functions, the integral of a series is the series of "
            "the integrals, always. <bookmark mark='b'/> The function minus log of one minus x, over x, is the sum of "
            "x to the k minus one over k, all non-negative. <bookmark mark='c'/> Integrate term by term: each term "
            "gives one over k squared. So the integral is pi squared over six, Part 3's Basel sum once more, and the "
            "numerical integral agrees."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l_) for l_ in layers], lag_ratio=0.25), run_time=3.0)
            self.play(Create(full))
            vo.wait_until("c")
            self.play(FadeIn(head[1]))
            self.play(FadeIn(side[1:]))
        self.wait(0.4)
        self.clear_scene()
