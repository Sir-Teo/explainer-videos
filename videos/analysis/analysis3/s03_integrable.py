from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis.analysis3.common import load, plain_axes, rects
from videos.analysis.analysis3.compute import smallest_denominators


def g(x):
    return 1.0 + 0.5 * np.sin(2.1 * x) + 0.25 * np.cos(5.3 * x)


def stair(x):
    """An increasing function with jumps at 0.5, 1.2, 1.9, 2.4 and smooth climbs between."""
    x = np.asarray(x, float)
    return 0.15 + 0.12 * x + 0.3 * (x >= 0.5) + 0.25 * (x >= 1.2) + 0.35 * (x >= 1.9) + 0.2 * (x >= 2.4)


class WhoIsIntegrable(VoiceoverScene):
    def construct(self):
        self.card()
        self.continuous()
        self.monotone()
        self.dirichlet()
        self.thomae()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(2, r"Which functions are integrable?", r"How rough can a function be and still have an area?",
                            lit=(1854,), part=3)
        with self.voiceover(
            "Chapter two. Which functions does this integral handle? Continuous ones, monotone ones, ones with a few "
            "jumps, and some surprisingly wild ones. And one simple function it can't handle at all."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def continuous(self):
        ax = plain_axes([0, 3.2, 1], [0, 2.0, 0.5], 8.4, 4.4).move_to([-2.2, -0.9, 0])
        gr = ax.plot(g, x_range=[0, 3.0, 0.005], color=C.FUNC, stroke_width=4).set_z_index(3)
        thm = VGroup(label(r"\textbf{Rudin 6.8} \ continuous on $[a, b]$ $\Rightarrow$ integrable", font_size=30),
                     label(r"(uniform continuity: \ one $\delta$ for the whole interval)", font_size=24, color=GREY_A)
                     ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        eta, delta = 0.5, 0.2
        # with |x - y| < delta the values differ by less than eta (checked on this function)
        t = np.linspace(0, 3.0, 30001)
        lip = np.abs(np.diff(g(t))).max() / (t[1] - t[0])
        assert lip * delta < eta
        e = np.linspace(0, 3.0, int(np.ceil(3.0 / delta)) + 2)  # 16 pieces of width 0.1875 < delta
        M, m = [], []
        for a, b in zip(e[:-1], e[1:]):
            v = g(np.linspace(a, b, 200))
            M.append(v.max())
            m.append(v.min())
        M, m = np.array(M), np.array(m)
        assert np.all(M - m < eta) and np.all(np.diff(e) < delta)
        # the picture of the two numbers: an eta-tall bar beside the tallest box (every box is shorter), and a
        # delta-wide brace under the first piece (every piece is narrower)
        k = int(np.argmax(M - m))
        xb = e[k + 1]
        eta_bar = VGroup(Line(ax.c2p(xb, m[k]) + RIGHT * 0.12, ax.c2p(xb, m[k] + eta) + RIGHT * 0.12, color=C.EPS,
                              stroke_width=5),
                         Line(ax.c2p(xb, m[k]) + RIGHT * 0.04, ax.c2p(xb, m[k]) + RIGHT * 0.2, color=C.EPS, stroke_width=3),
                         Line(ax.c2p(xb, m[k] + eta) + RIGHT * 0.04, ax.c2p(xb, m[k] + eta) + RIGHT * 0.2, color=C.EPS,
                              stroke_width=3))
        eta_l = MathTex(r"\eta", font_size=30, color=C.EPS).next_to(eta_bar, RIGHT, buff=0.08)
        assert M[k] - m[k] < eta
        d_br = BraceBetweenPoints(ax.c2p(0, 0), ax.c2p(delta, 0), direction=DOWN, buff=0.08, color=C.DELTA)
        d_l = MathTex(r"\delta", font_size=30, color=C.DELTA).next_to(d_br, DOWN, buff=0.06)
        boxes = VGroup()
        for a, b, hi, lo in zip(e[:-1], e[1:], M, m):
            p0, p1 = ax.c2p(a, lo), ax.c2p(b, hi)
            boxes.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 1e-3), stroke_color=C.DELTA,
                                stroke_width=2, fill_color=C.EPS, fill_opacity=0.5).move_to((p0 + p1) / 2))
        gapsum = float(np.sum((M - m) * np.diff(e)))
        side = VGroup(MathTex(r"\text{mesh} < \delta \;\Rightarrow\; M_i - m_i < \eta", font_size=30),
                      MathTex(r"U - L < \eta\,(b - a)", font_size=32, color=C.EPS),
                      MathTex(rf"\text{{here: }} \delta = {delta}, \ U - L = {gapsum:.3f}", font_size=26, color=GREY_A),
                      label(r"also integrable: \ monotone $f$ (6.9),", font_size=22, color=GREY_B),
                      label(r"finitely many jumps (6.10), \ $\varphi \circ f$ (6.11)", font_size=22, color=GREY_B)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.5, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Continuous functions on a closed interval are integrable, and the reason is uniform "
            "continuity from Part 2. Pick a small number eta. <bookmark mark='b'/> Because the interval is compact, "
            "one delta works everywhere: points closer than delta have values closer than eta. "
            "<bookmark mark='c'/> So on a partition with pieces shorter than delta, each gap between the supremum and "
            "the infimum is less than eta, and the total gap, U minus L, is less than eta times the length of the "
            "interval. <bookmark mark='d'/> That can be made as small as we like. Other proofs in the same chapter "
            "handle monotone functions, functions with finitely many jumps, and continuous functions of integrable "
            "ones."
        ) as vo:
            self.play(Create(ax), Create(gr))
            vo.wait_until("a")
            self.play(FadeIn(thm))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(bx) for bx in boxes], lag_ratio=0.12), FadeIn(side[0]), run_time=2.0)
            self.play(GrowFromCenter(d_br), FadeIn(d_l), Create(eta_bar), FadeIn(eta_l))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def monotone(self):
        ax = plain_axes([0, 3.0, 1], [0, 1.8, 0.5], 7.0, 4.6).move_to([-2.8, -0.6, 0])
        x = np.linspace(0, 3.0, 3001)
        segs = VGroup()
        cuts = [0, 0.5, 1.2, 1.9, 2.4, 3.0]
        for a, b in zip(cuts[:-1], cuts[1:]):
            xx = np.linspace(a, b - 1e-6, 50)
            segs.add(Line(ax.c2p(a, stair(np.array([a]))[0]), ax.c2p(b, stair(np.array([b - 1e-6]))[0]), color=C.FUNC,
                          stroke_width=4))
        jdots = VGroup()
        for c_ in cuts[1:-1]:
            lo_, hi_ = float(stair(np.array([c_ - 1e-9]))[0]), float(stair(np.array([c_]))[0])
            assert hi_ > lo_ + 0.1  # a jump; f(c) is the upper value (right-continuous)
            jdots.add(Circle(radius=0.07, color=C.FUNC, stroke_width=2.5).set_fill(BACKGROUND, 1).move_to(ax.c2p(c_, lo_)),
                      Dot(ax.c2p(c_, hi_), radius=0.075, color=C.FUNC))
        n = 12
        e = np.linspace(0, 3.0, n + 1)
        lo_v, hi_v = stair(e[:-1]), stair(e[1:] - 1e-9)
        hi_v = np.maximum(hi_v, stair(e[1:]))  # closed pieces: the sup includes the right end
        slivers = VGroup()
        for a, b, lo, hi in zip(e[:-1], e[1:], lo_v, hi_v):
            p0, p1 = ax.c2p(a, lo), ax.c2p(b, hi)
            slivers.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 1e-3), stroke_width=1,
                                  stroke_color=BACKGROUND, fill_color=C.EPS, fill_opacity=0.85).move_to((p0 + p1) / 2))
        targets = []
        for lo, hi in zip(lo_v, hi_v):
            p0, p1 = ax.c2p(3.0 - 3.0 / n, lo), ax.c2p(3.0, hi)
            targets.append((p0 + p1) / 2)
        total = float(np.sum(hi_v - lo_v))
        rise = float(stair(np.array([3.0]))[0] - stair(np.array([0.0]))[0])
        assert abs(total - rise) < 1e-9
        thm = label(r"\textbf{Rudin 6.9} \ monotone on $[a, b]$ $\Rightarrow$ integrable, \ jumps and all",
                    font_size=30).to_edge(UP, buff=0.35)
        side = VGroup(MathTex(r"U - L = \frac{b - a}{n}\,\big(f(b) - f(a)\big)", font_size=32, color=C.EPS),
                      label(r"the slivers stack into one column", font_size=24, color=GREY_A),
                      label(r"of width $\tfrac{b-a}{n}$ and height $f(b) - f(a)$", font_size=24, color=GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.9, 0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Monotone functions are integrable even with jumps, by the stacking trick we saw for x "
            "squared. <bookmark mark='b'/> On each piece the gap is the function's rise across that piece, jumps "
            "included. <bookmark mark='c'/> Slide the slivers to one side: they stack into a single column, one piece "
            "wide and as tall as the total rise. So U minus L is the total rise divided by n, and it goes to zero."
        ) as vo:
            self.play(Create(ax), Create(segs), FadeIn(jdots))
            vo.wait_until("a")
            self.play(FadeIn(thm))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in slivers], lag_ratio=0.08))
            vo.wait_until("c")
            self.play(*[s_.animate.move_to(t_) for s_, t_ in zip(slivers, targets)], run_time=2.0)
            self.play(FadeIn(side))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dirichlet(self):
        ax = plain_axes([0, 1, 0.25], [0, 1.25, 0.5], 9.0, 3.8).move_to([-0.6, -0.9, 0])
        top_pts = VGroup(*[Dot(ax.c2p(v, 1), radius=0.025, color=C.RATIONAL) for v in np.linspace(0, 1, 400)])
        top_pts.set_z_index(3)
        bottom = Line(ax.c2p(0, 0), ax.c2p(1, 0), color=C.FUNC, stroke_width=6).set_z_index(3)
        top_l = MathTex(r"1 \text{ on } \Q", font_size=28, color=C.RATIONAL).next_to(ax.c2p(1, 1), RIGHT, buff=0.15)
        bot_l = MathTex(r"0 \text{ off } \Q", font_size=28, color=C.FUNC).next_to(ax.c2p(1, 0), RIGHT, buff=0.15)
        e = np.linspace(0, 1, 9)
        up = rects(ax, e, np.ones(8), C.UPPER_SUM, opacity=0.25)
        head = VGroup(label(r"Dirichlet's function \ (Rudin, Exercise 6.4)", font_size=30),
                      label(r"every piece contains rationals and irrationals: \ $M_i = 1$, \ $m_i = 0$", font_size=26,
                            color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        res = MathTex(r"U(P, f) = 1, \quad L(P, f) = 0 \quad \text{for every } P", font_size=34, color=C.PATHOLOGY)
        res.next_to(ax, DOWN, buff=0.35)
        card = museum_card(r"Dirichlet's function", r"Dirichlet, 1829", r"Riemann integrability",
                           r"Rudin, Example 4.27 and Exercise 6.4", width=4.4)
        card.to_edge(RIGHT, buff=0.4).set_y(1.6)
        with self.voiceover(
            "Now the function this integral can't handle. <bookmark mark='a'/> Let f be one at every rational and "
            "zero at every irrational. <bookmark mark='b'/> Every piece of every partition contains both kinds of "
            "points, so every supremum is one and every infimum is zero. <bookmark mark='c'/> The upper sum is always "
            "one, the lower sum is always zero, and no refinement ever closes the gap. Dirichlet's function has no "
            "Riemann integral. Remember it: in Part 5 a better integral will give it the value zero, because the "
            "rationals, though dense, are too few to carry any area."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax))
            vo.wait_until("a")
            self.play(FadeIn(top_pts), Create(bottom), FadeIn(top_l), FadeIn(bot_l))
            vo.wait_until("b")
            self.play(FadeIn(head[1]), LaggedStart(*[GrowFromEdge(r, DOWN) for r in up], lag_ratio=0.1))
            vo.wait_until("c")
            self.play(FadeIn(res))
            self.play(FadeIn(card, scale=0.95))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def thomae(self):
        d = load("thomae")
        ks, U, q16 = d["ks"], d["U"], d["q16"]
        ax = plain_axes([0, 1, 0.25], [0, 1.05, 0.5], 8.4, 4.6).move_to([-2.3, -0.7, 0])
        from math import gcd
        pts = [(p / q, 1 / q) for q in range(1, 41) for p in range(0, q + 1) if gcd(p, q) == 1]
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.012 + 0.035 * b, color=C.RATIONAL) for a, b in pts])
        e = np.linspace(0, 1, 17)
        up = rects(ax, e, 1.0 / q16, C.UPPER_SUM, opacity=0.35)
        # finer drawn partitions (2^6, 2^8 pieces): heights 1/q_min, their sums equal the table's U
        ups = {4: up}
        for k in (6, 8):
            qk = smallest_denominators(2**k)
            assert abs(float(np.sum(1.0 / qk)) / 2**k - U[int(np.nonzero(ks == k)[0][0])]) < 1e-12
            ups[k] = rects(ax, np.linspace(0, 1, 2**k + 1), 1.0 / qk, C.UPPER_SUM, opacity=0.35, stroke=0 if k > 6 else 0.6)
        head = VGroup(label(r"Thomae's function \ (Part 2): \ $f(p/q) = 1/q$, \ $0$ off $\Q$", font_size=30),
                      label(r"every lower sum is $0$; \ the upper sums on $2^k$ equal pieces:", font_size=26,
                            color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        tab = VGroup()
        for k in (1, 2, 4, 6, 8, 10, 12, 14):
            i = int(np.nonzero(ks == k)[0][0])
            tab.add(MathTex(rf"2^{{{k}}}:", rf"\ U = {U[i]:.4f}", font_size=28))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.6, -0.3, 0])
        regrid(tab, gap=0.2)
        drawn = {4: 2, 6: 3, 8: 4}  # table rows whose partition is drawn
        concl = label(r"$U \to 0 = L$: \ integrable, \ $\int_0^1 f = 0$, \ though discontinuous at every rational",
                      font_size=26, color=C.EPS).to_edge(DOWN, buff=0.35)
        assert U[-1] < 0.01 and q16[7] == 2
        with self.voiceover(
            "Compare Thomae's function from Part 2: one over q at the fraction p over q in lowest terms, and zero at "
            "irrationals. <bookmark mark='a'/> Again every infimum is zero, so every lower sum is zero. <bookmark mark='b'/> "
            "But the supremum on a short piece is one over the smallest denominator of a fraction in that piece, and "
            "short pieces only contain fractions with large denominators, apart from a few. <bookmark mark='c'/> "
            "Computed exactly on sixteen thousand equal pieces, the upper sum is below one hundredth, and it keeps "
            "falling. <bookmark mark='d'/> So this function, discontinuous at every rational, is integrable, with "
            "integral zero. Being discontinuous somewhere is harmless; the question, as Lebesgue would show, is how "
            "big the set of discontinuities is."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(head[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in up], lag_ratio=0.06))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[:3]], lag_ratio=0.25), run_time=1.2)
            self.play(tab[drawn[4]].animate.set_color(C.UPPER_SUM), run_time=0.4)
            for k_prev, k in ((4, 6), (6, 8)):
                self.play(FadeOut(ups[k_prev]), FadeIn(ups[k]), tab[drawn[k_prev]].animate.set_color(WHITE),
                          FadeIn(tab[drawn[k]].set_color(C.UPPER_SUM)), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(r) for r in tab[5:]], lag_ratio=0.3), run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(concl))
        self.wait(0.4)
        self.clear_scene()
