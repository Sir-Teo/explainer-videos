from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis1.common import partial_curve, saw_axes, saw_graph
from videos.analysis2.common import load, plain_axes, polyline


class Abel(VoiceoverScene):
    def construct(self):
        self.card()
        self.by_parts()
        self.dirichlet()
        self.sawtooth()
        self.absolute()
        self.product()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(7, r"Summation by parts, and multiplying series",
                            r"How can a series converge when its terms don't shrink fast?", lit=(), part=2)
        with self.voiceover(
            "Chapter seven. Some series converge not because their terms are small, but because they cancel. The tool "
            "for cancellation is summation by parts, and with it we can finally answer a question about the sawtooth."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def by_parts(self):
        a = np.array([1.0, 0.7, 1.3, 0.6, 0.9, 0.8])
        b = np.array([2.4, 1.9, 1.5, 1.0, 0.8, 0.5])
        A = np.cumsum(a)
        N = len(a)
        sx, sy = 1.55, 1.0
        o = np.array([-4.6, -3.0, 0])

        def P(x, y):
            return o + np.array([sx * x, sy * y, 0])

        axes = VGroup(Arrow(P(0, 0), P(A[-1] + 0.5, 0), buff=0, color=GREY_C, stroke_width=2, tip_length=0.15),
                      Arrow(P(0, 0), P(0, 2.9), buff=0, color=GREY_C, stroke_width=2, tip_length=0.15))
        xl = MathTex(r"A_n = a_1 + \cdots + a_n", font_size=26, color=GREY_B).next_to(P(A[-1] + 0.5, 0), DOWN, buff=0.5)
        xl.align_to(P(A[-1] + 0.5, 0), RIGHT)
        yl = MathTex(r"b_n", font_size=28, color=GREY_B).next_to(P(0, 2.9), LEFT, buff=0.1)
        ticks = VGroup(*[MathTex(rf"A_{n + 1}", font_size=22, color=GREY_B).next_to(P(A[n], 0), DOWN, buff=0.1)
                         for n in range(N - 1)])
        cols = [C.SEQ, C.FREQ]
        vert = VGroup()
        for n in range(N):
            x0 = A[n - 1] if n else 0.0
            r = Polygon(P(x0, 0), P(A[n], 0), P(A[n], b[n]), P(x0, b[n]), stroke_color=WHITE, stroke_width=1.5,
                        fill_color=cols[n % 2], fill_opacity=0.6)
            vert.add(r)
        hor = VGroup()
        hcols = [C.EPS, C.DELTA]
        for n in range(N - 1, -1, -1):
            top, bot = b[n], (b[n + 1] if n + 1 < N else 0.0)
            r = Polygon(P(0, bot), P(A[n], bot), P(A[n], top), P(0, top), stroke_color=WHITE, stroke_width=1.5,
                        fill_color=hcols[n % 2], fill_opacity=0.6)
            hor.add(r)
        f1 = MathTex(r"\sum_{n=1}^{N} a_n b_n", font_size=36).move_to([3.4, 2.4, 0])
        f1n = label(r"vertical strips: \ width $a_n$, height $b_n$", font_size=24, color=GREY_A).next_to(f1, DOWN, buff=0.1)
        f2 = MathTex(r"= \sum_{n=1}^{N-1} A_n (b_n - b_{n+1}) + A_N b_N", font_size=36).next_to(f1n, DOWN, buff=0.35)
        f2n = label(r"horizontal slabs: \ width $A_n$, height $b_n - b_{n+1}$", font_size=24, color=GREY_A).next_to(
            f2, DOWN, buff=0.1)
        ref = note(r"summation by parts, Rudin 3.41").next_to(f2n, DOWN, buff=0.3)
        ibp = MathTex(r"\int b\, dA = A b - \int A\, db", font_size=34, color=C.EPS).next_to(ref, DOWN, buff=0.3)
        with self.voiceover(
            "Here's summation by parts as a picture. <bookmark mark='a'/> Lay the terms a n end to end along the "
            "horizontal axis, so the marks are the partial sums A n, and over each one stand a strip of height b n, "
            "with the b n decreasing. <bookmark mark='b'/> The total area is the sum of a n times b n. "
            "<bookmark mark='c'/> Now slice the same region horizontally instead. Each slab has width A n, the partial "
            "sum, and height b n minus b n plus one, the drop between consecutive heights, plus a bottom slab of width A "
            "N. <bookmark mark='d'/> Same area, two ways of adding it up: it's integration by parts, for sums."
        ) as vo:
            self.play(Create(axes), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.2) for r in vert], lag_ratio=0.2), FadeIn(ticks))
            vo.wait_until("b")
            self.play(FadeIn(f1), FadeIn(f1n))
            vo.wait_until("c")
            self.play(FadeOut(vert), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in hor], lag_ratio=0.2))
            self.play(FadeIn(f2), FadeIn(f2n), FadeIn(ref))
            vo.wait_until("d")
            self.play(FadeIn(ibp))
        lhs = float(np.sum(a * b))
        rhs = float(np.sum(A[:-1] * (b[:-1] - b[1:])) + A[-1] * b[-1])
        assert abs(lhs - rhs) < 1e-12
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dirichlet(self):
        thm = VGroup(label(r"\textbf{Dirichlet's test} (Rudin 3.42)", font_size=32),
                     label(r"partial sums $A_n$ of $\sum a_n$ bounded, \ $|A_n| \le M$;", font_size=28),
                     label(r"$b_0 \ge b_1 \ge b_2 \ge \cdots$, \ $b_n \to 0$", font_size=28),
                     label(r"$\Rightarrow$ \ $\sum a_n b_n$ converges", font_size=30, color=C.EPS)
                     ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.4)
        rows = [MathTex(r"\Big|\sum_{n=p}^{q} a_n b_n\Big|", r"\le",
                        r"M\Big(\sum_{n=p}^{q-1} (b_n - b_{n+1}) + b_q + b_p\Big)", font_size=36),
                MathTex(r"\Big|\sum_{n=p}^{q} a_n b_n\Big|", r"\le", r"2 M b_p \to 0", font_size=36)]
        whys = [why(r"summation by parts, every $|A| \le M$"), why(r"the drops telescope: \ Cauchy criterion")]
        step = ladder(self, rows, whys, keep=2, top=0.3, buff=0.45, x=-0.6)
        alt = label(r"$a_n = (-1)^n$: \ the alternating series test (3.43)", font_size=28, color=GREY_A).to_edge(DOWN,
                                                                                                               buff=0.5)
        # the hypotheses, for a_n = sin n (the sawtooth at x = 1) and b_n = 1/n
        K = 40
        nn = np.arange(1, K + 1)
        A = np.cumsum(np.sin(nn))
        M = 1 / math.sin(0.5)
        assert np.abs(A).max() <= M
        axA = plain_axes([0, K + 1, 10], [-2.4, 2.4, 1], 3.1, 1.7, numbers=False).move_to([-5.2, 2.15, 0])
        axB = plain_axes([0, K + 1, 10], [0, 1.1, 0.5], 3.1, 1.7, numbers=False).move_to([5.2, 2.15, 0])
        bandA = Rectangle(width=axA.c2p(K + 1, 0)[0] - axA.c2p(0, 0)[0], height=axA.c2p(0, M)[1] - axA.c2p(0, -M)[1],
                          stroke_width=0, fill_color=C.EPS, fill_opacity=0.14).move_to(axA.c2p((K + 1) / 2, 0))
        edgesA = VGroup(*[DashedLine(axA.c2p(0, v), axA.c2p(K + 1, v), color=C.EPS, stroke_width=1.5) for v in (M, -M)])
        dotsA = VGroup(*[Dot(axA.c2p(k, v), radius=0.03, color=C.SEQ) for k, v in zip(nn, A)])
        dotsB = VGroup(*[Dot(axB.c2p(k, 1 / k), radius=0.03, color=C.FREQ) for k in nn])
        labA = VGroup(MathTex(r"A_n = \sum_{k \le n} \sin k", font_size=22, color=C.SEQ),
                      MathTex(r"\pm M", font_size=22, color=C.EPS)).arrange(RIGHT, buff=0.3).next_to(axA, DOWN,
                                                                                                buff=0.1)
        labB = MathTex(r"b_n = \tfrac1n \downarrow 0", font_size=22, color=C.FREQ).next_to(axB, DOWN, buff=0.1)
        with self.voiceover(
            "Summation by parts goes back to Abel; the test it gives is named for Dirichlet. <bookmark mark='t'/> Suppose the partial sums of the a n stay bounded, by "
            "some M, without converging, and the b n decrease to zero. Then the sum of a n b n converges. "
            "<bookmark mark='a'/> Sum a block by parts: each partial sum is at most M in size, <bookmark mark='b'/> "
            "and the drops in b telescope, leaving at most two M times b p, which goes to zero. That's the Cauchy "
            "criterion. <bookmark mark='c'/> With a n equal to plus and minus one, this is the alternating series test."
        ) as vo:
            self.play(FadeIn(thm[0]))
            self.play(FadeIn(thm[1]), Create(axA), FadeIn(bandA), Create(edgesA), FadeIn(labA))
            self.play(LaggedStart(*[FadeIn(x) for x in dotsA], lag_ratio=0.05), run_time=1.6)
            self.play(FadeIn(thm[2]), Create(axB), FadeIn(labB))
            self.play(LaggedStart(*[FadeIn(x) for x in dotsB], lag_ratio=0.05), run_time=1.4)
            self.play(FadeIn(thm[3]))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            self.play(FadeIn(alt))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sawtooth(self):
        d = load("abel")
        W, c, r, S, target = d["W"], complex(d["c"]), float(d["r"]), d["S"], float(d["target"])
        o = np.array([-4.3, -0.6, 0])
        u = 1.35

        def P(z):
            return o + u * np.array([z.real, z.imag, 0.0])

        plane = NumberPlane(x_range=[-2, 1.4, 1], y_range=[-1, 2.4, 1], x_length=3.4 * u, y_length=3.4 * u,
                            background_line_style={"stroke_color": GREY_D, "stroke_width": 1, "stroke_opacity": 0.5},
                            axis_config={"stroke_color": GREY_C})
        plane.move_to(P(complex(-0.3, 0.7)))
        circ = Circle(radius=u * r, color=GREY_B, stroke_width=1.5).move_to(P(c))
        pts = VGroup(*[Dot(P(w), radius=0.05, color=C.FREQ) for w in W[:40]])
        path = VMobject(color=C.FREQ, stroke_width=1.5, stroke_opacity=0.6)
        path.set_points_as_corners([P(0j)] + [P(w) for w in W[:40]])
        head = MathTex(r"\sum_{k=1}^{\infty} \frac{\sin kx}{k}", r"\quad a_k = \sin kx,\ \ b_k = \tfrac1k", font_size=36)
        head.to_edge(UP, buff=0.35)
        lab = MathTex(r"\sum_{k \le n} e^{ikx} \text{ stays on a circle}", font_size=28, color=C.FREQ).next_to(
            plane, DOWN, buff=0.15)
        bound = MathTex(r"|A_n| \le \frac{1}{|\sin(x/2)|}", font_size=30).next_to(lab, DOWN, buff=0.12)
        ax = plain_axes([0, 201, 50], [0.6, 1.5, 0.2], 6.0, 3.6, numbers=True, font_size=20,
                        axis_config={"decimal_number_config": {"num_decimal_places": 1}}, x_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([3.3, -0.4, 0])
        nn = np.arange(1, 201)
        curve = polyline(ax, nn, S[:200], color=C.APPROX, stroke_width=2.5)
        tl = DashedLine(ax.c2p(0, target), ax.c2p(201, target), color=C.FUNC, stroke_width=2)
        # Dirichlet's tail bound 2M b_{n+1}, with M = 1/|sin(x/2)| = 2r (the circle's diameter)
        M_ = 2 * r
        assert abs(M_ - 1 / abs(math.sin(0.5))) < 1e-9
        assert np.all(np.abs(S[:200] - target) <= 2 * M_ / (nn + 1))
        env_hi = polyline(ax, nn[9:], target + 2 * M_ / (nn[9:] + 1), color=C.EPS, stroke_width=2)
        env_lo = polyline(ax, nn[9:], target - 2 * M_ / (nn[9:] + 1), color=C.EPS, stroke_width=2)
        ax_l = MathTex(r"x = 1:\ \ \sum_{k \le n} \frac{\sin k}{k} \to \frac{\pi - 1}{2}", font_size=28).next_to(ax, UP,
                                                                                                      buff=0.2)
        env_l = label(r"Dirichlet's bound $2M b_{n+1}$", font_size=22, color=C.EPS).next_to(ax.c2p(120, 1.25), UP,
                                                                                         buff=0.05)
        ia = saw_axes(x_length=8.0, y_length=2.8).move_to([0, -0.9, 0])
        ic = partial_curve(ia, 12, stroke_width=3)
        iq = label(r"Part 1: \ does it converge, \ and to what?", font_size=28, color=GREY_A).next_to(ia, DOWN, buff=0.3)
        intro = VGroup(ia, ic, iq)
        with self.voiceover(
            "Now the sawtooth. Part 1 opened with the series sine x, plus sine 2 x over two, plus sine 3 x over three, "
            "and asked whether it even converges. <bookmark mark='a'/> Here a k is sine k x, which doesn't go to zero, "
            "but its partial sums stay bounded: they're imaginary parts of the sums of e to the i k x, "
            "<bookmark mark='b'/> and those just walk around a circle, for x equal to one here. <bookmark mark='c'/> "
            "The b k, one over k, decrease to zero. So Dirichlet's test applies: <bookmark mark='d'/> at x equal to "
            "one, the partial sums close in on pi minus one over two, inside Dirichlet's shrinking bound."
        ) as vo:
            self.play(FadeIn(head))
            self.play(Create(ia), Create(ic), FadeIn(iq), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.5)
            self.play(Create(plane), Create(circ))
            vo.wait_until("b")
            self.play(Create(path), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.05), FadeIn(lab), run_time=2.5)
            self.play(FadeIn(bound))
            vo.wait_until("c")
            self.wait(0.3)
            vo.wait_until("d")
            self.play(Create(ax), FadeIn(ax_l), Create(tl))
            self.play(Create(curve), Create(env_hi), Create(env_lo), FadeIn(env_l), run_time=2.0)
        assert np.allclose(np.abs(W - c), r)
        self.wait(0.3)
        self.clear_scene()

        sa = saw_axes(x_length=11.5, y_length=4.0).move_to([0, -0.7, 0])
        g = saw_graph(sa)
        ns = (3, 10, 40, 160)
        curves = [partial_curve(sa, n) for n in ns]
        cur = curves[0]
        ttl = label(r"Converges at every $x$, \ to the sawtooth", font_size=34).to_edge(UP, buff=0.4)
        nl = MathTex(r"N = 3", font_size=32, color=C.APPROX).next_to(ttl, DOWN, buff=0.2)
        xs = [0.6, 2.0, 4.4]
        probes = VGroup(*[DashedLine(sa.c2p(x, -2.0), sa.c2p(x, 2.0), color=GREY_B, stroke_width=1.5) for x in xs])
        led = label(r"Ledger, row 2, Fourier column: \ \emph{converges at each $x$} \ (by Dirichlet's test)",
                    font_size=26, color=C.EPS).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The same argument works at every x except the multiples of two pi, and there every term is zero anyway. "
            "<bookmark mark='a'/> So the series converges at every single point, <bookmark mark='b'/> and the partial "
            "sums settle onto the sawtooth, each at its own pace, slowest near the jumps. <bookmark mark='c'/> That's "
            "the first entry in the Fourier column of the ledger: the series converges at each point."
        ) as vo:
            self.play(FadeIn(ttl), Create(sa), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(cur), FadeIn(nl), FadeIn(probes))
            vo.wait_until("b")
            for n, cv in zip(ns[1:], curves[1:]):
                nl2 = MathTex(rf"N = {n}", font_size=32, color=C.APPROX).move_to(nl)
                self.play(Transform(cur, cv), FadeTransform(nl, nl2), run_time=1.2)
                nl = nl2
            vo.wait_until("c")
            self.play(FadeIn(led))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def absolute(self):
        head = VGroup(
            label(r"\textbf{Absolute convergence} (Rudin 3.45): \ $\sum |a_n| < \infty \Rightarrow \sum a_n$ converges",
                  font_size=30),
            label(r"(blocks: $|a_n + \cdots + a_m| \le |a_n| + \cdots + |a_m|$)", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.35)
        K = 40
        nn = np.arange(1, K + 1)
        panels = []
        for i, p in enumerate((2, 1)):
            a = (-1.0) ** (nn + 1) / nn**p
            ax = plain_axes([0, K + 1, 10], [0, 4.6, 1], 5.6, 3.2, numbers=True, font_size=18,
                            axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.4 + 6.9 * i, -0.75, 0])
            s_abs, s_sgn = np.cumsum(np.abs(a)), np.cumsum(a)
            c_abs = polyline(ax, nn, s_abs, color=C.SEQ, stroke_width=3)
            c_sgn = polyline(ax, nn, s_sgn, color=C.FREQ, stroke_width=2.5)
            d_sgn = VGroup(*[Dot(ax.c2p(k, v), radius=0.03, color=C.FREQ) for k, v in zip(nn, s_sgn)])
            lim = float(np.pi**2 / 12) if p == 2 else math.log(2)
            tl = DashedLine(ax.c2p(0, lim), ax.c2p(K + 1, lim), color=WHITE, stroke_width=1.2)
            l_abs = MathTex(r"\sum |a_n|" + (r" \to \infty" if p == 1 else ""), font_size=24, color=C.SEQ)
            l_abs.move_to(ax.c2p(31, 2.9 if p == 1 else 2.15))
            l_sgn = MathTex(r"\sum a_n" + (r" \to \ln 2" if p == 1 else ""), font_size=24, color=C.FREQ)
            l_sgn.move_to(ax.c2p(31, lim - 0.42))
            ttl = MathTex(rf"a_n = \frac{{(-1)^{{n+1}}}}{{n{'^2' if p == 2 else ''}}}", font_size=28)
            verdict = label(r"absolutely convergent" if p == 2 else r"\emph{conditionally} convergent", font_size=24,
                            color=C.CONNECTED_SET if p == 2 else C.FREQ)
            VGroup(ttl, verdict).arrange(RIGHT, buff=0.3).next_to(ax, UP, buff=0.15)
            panels.append(VGroup(ax, tl, c_abs, c_sgn, d_sgn, l_abs, l_sgn, ttl, verdict))
            assert abs(s_sgn[-1] - lim) < 0.02 and (s_abs[-1] < 1.7 if p == 2 else s_abs[-1] > 4.2)
        saw = label(r"$\sum \frac{\sin kx}{k}$: \ conditionally, for $x$ not a multiple of $\pi$", font_size=28,
                    color=C.FREQ).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> If the absolute values have a finite sum, the series converges: blocks can only shrink "
            "when you allow cancellation. <bookmark mark='b'/> Series that converge only thanks to cancellation, like "
            "the alternating harmonic series, are called conditionally convergent. <bookmark mark='c'/> The sawtooth's "
            "series is one of them. That matters, as the next chapter will show."
        ) as vo:
            vo.wait_until("a")
            P = panels[0]
            self.play(FadeIn(head), Create(P[0]), FadeIn(P[7]))
            self.play(Create(P[2]), FadeIn(P[5]), run_time=1.2)
            self.play(Create(P[3]), FadeIn(P[4]), Create(P[1]), FadeIn(P[6]), run_time=1.2)
            self.play(FadeIn(P[8]))
            vo.wait_until("b")
            P = panels[1]
            self.play(Create(P[0]), FadeIn(P[7]))
            self.play(Create(P[3]), FadeIn(P[4]), Create(P[1]), FadeIn(P[6]), run_time=1.2)
            self.play(Create(P[2]), FadeIn(P[5]), run_time=1.5)
            self.play(FadeIn(P[8]))
            vo.wait_until("c")
            self.play(FadeIn(saw))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def product(self):
        d = load("product")
        a, c, bound = d["a"], d["c"], d["bound"]
        K = 7
        cs = 0.62
        o = np.array([-5.8, 1.6, 0])
        cells = VGroup()
        for i in range(K):
            for j in range(K):
                sq = Square(side_length=cs * 0.92, stroke_color=GREY_C, stroke_width=1.5, fill_color=GREY_E,
                            fill_opacity=0.6).move_to(o + np.array([j * cs, -i * cs, 0]))
                t = MathTex(rf"a_{i} b_{j}", font_size=20).move_to(sq)
                cells.add(VGroup(sq, t))
        head = MathTex(r"\Big(\sum a_i\Big)\Big(\sum b_j\Big)", r"\;\overset{?}{=}\;", r"\sum_n c_n, \quad c_n = "
                       r"\sum_{k=0}^n a_k b_{n-k}", font_size=34).to_edge(UP, buff=0.3).shift(RIGHT * 1.6)
        diag = []
        for n in range(K):
            g = VGroup(*[cells[i * K + (n - i)] for i in range(n + 1) if 0 <= n - i < K])
            diag.append(g)
        mert = VGroup(label(r"\textbf{Mertens} (Rudin 3.50):", font_size=28),
                      label(r"if $\sum a_n$ converges \emph{absolutely} to $A$", font_size=26),
                      label(r"and $\sum b_n$ converges to $B$,", font_size=26),
                      label(r"then $\sum c_n$ converges to $AB$.", font_size=26)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.1)
        mert.move_to([3.3, 1.3, 0])
        with self.voiceover(
            "How do you multiply two series? <bookmark mark='a'/> The product of the sums is the sum of every product "
            "a i times b j, an infinite grid. <bookmark mark='b'/> The Cauchy product adds the grid along diagonals: c n "
            "collects the terms where the indices add up to n, just as you'd collect powers of x when multiplying power "
            "series. <bookmark mark='c'/> Mertens proved this gives the right answer if one of the two series converges "
            "absolutely. Adding up a doubly infinite array in a different order is the first glimpse of a question that "
            "comes back in Part 5, as Fubini's theorem."
        ) as vo:
            self.play(FadeIn(head[0]), LaggedStart(*[FadeIn(x) for x in cells], lag_ratio=0.01), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(head[1:]))
            for n in range(K):
                self.play(diag[n].animate.set_color(C.EPS if n % 2 == 0 else C.DELTA), run_time=0.35)
            vo.wait_until("c")
            self.play(FadeIn(mert))
        self.wait(0.3)

        ax = plain_axes([0, 61, 10], [-3.5, 3.5, 1], 6.4, 2.6, numbers=True, font_size=18).move_to([3.3, -1.75, 0])
        # |c_n| = sum_k 1/sqrt((k+1)(n-k+1)) climbs toward pi (a Riemann sum for the Beta integral B(1/2, 1/2))
        assert np.abs(c).max() < math.pi and np.abs(c[-1]) > 2.7
        pis = VGroup(*[DashedLine(ax.c2p(0, sg * math.pi), ax.c2p(61, sg * math.pi), color=GREY_C, stroke_width=1.5,
                                  dash_length=0.06) for sg in (1, -1)])
        pil = MathTex(r"\pm\pi", font_size=24, color=GREY_B).next_to(ax.c2p(61, math.pi), RIGHT, buff=0.08)
        dots = VGroup(*[Dot(ax.c2p(n, c[n]), radius=0.04, color=C.PATHOLOGY) for n in range(len(c))])
        bnd = VGroup(polyline(ax, np.arange(len(c)), bound, color=GREY_B, stroke_width=1.5),
                     polyline(ax, np.arange(len(c)), -bound, color=GREY_B, stroke_width=1.5))
        ex = MathTex(r"a_n = b_n = \frac{(-1)^n}{\sqrt{n+1}}", font_size=28).next_to(ax, UP, buff=0.12)
        verdict = label(r"$|c_n| \ge \tfrac{2(n+1)}{n+2}$: \ $c_n \not\to 0$, \ so $\sum c_n$ diverges (Rudin 3.49)",
                        font_size=24, color=C.PATHOLOGY).next_to(ax, DOWN, buff=0.15)
        with self.voiceover(
            "Without absolute convergence it can fail. <bookmark mark='a'/> Take the alternating series of one over "
            "root n plus one, which converges, and multiply it by itself. <bookmark mark='b'/> Every term in the n-th "
            "diagonal has the same sign, so they pile up instead of cancelling: the Cauchy product's terms never shrink. "
            "Their size climbs toward pi, and the product series diverges."
        ) as vo:
            self.play(FadeOut(mert))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(ex))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.02), Create(bnd), FadeIn(verdict),
                      Create(pis), FadeIn(pil), run_time=2)
        assert np.all(np.abs(c) >= bound - 1e-12)
        self.wait(0.5)
        self.clear_scene()
