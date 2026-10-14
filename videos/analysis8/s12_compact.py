from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis8.common import load, plain_axes, polyline, square_axes


class Compact(VoiceoverScene):
    def construct(self):
        self.card()
        self.thin()
        self.string()
        self.fredholm()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(11, r"Compact operators", r"Which operators behave like matrices?", lit=(), part=8)
        with self.voiceover("Chapter eleven: compact operators, the ones for which linear algebra survives."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def thin(self):
        d = load("volterra")
        s = d["s"]
        bars = VGroup()
        for k in range(10):
            v = float(s[k])
            bars.add(Rectangle(width=0.3, height=4.0 * v / float(s[0]), stroke_width=0, fill_color=C.OPERATOR,
                               fill_opacity=0.85).move_to([-6.3 + 0.5 * k, -2.6 + 2.0 * v / float(s[0]), 0]))
        b_l = label(r"the semi-axes of $V(B)$: \ $\frac{2}{\pi}, \frac{2}{3\pi}, \frac{2}{5\pi}, \ldots \to 0$", font_size=24,
                    color=C.OPERATOR).next_to(bars, UP, buff=0.2).align_to(bars, LEFT)
        ax = square_axes([-1.3, 1.3, 1], [-1.3, 1.3, 1], 1.0).move_to([0.3, -0.6, 0])
        ax.set_opacity(0.3)
        th = np.linspace(0, 2 * np.pi, 300)
        unit = VMobject(color=GREY_B, stroke_width=2).set_points_as_corners([ax.c2p(math.cos(t), math.sin(t)) for t in th])
        thin_e = VMobject(color=C.OPERATOR, stroke_width=3, fill_color=C.OPERATOR, fill_opacity=0.2).set_points_as_corners(
            [ax.c2p(math.cos(t), 0.33 * math.sin(t)) for t in th])
        sch = note(r"schematic: \ two of infinitely many axes").next_to(ax, DOWN, buff=0.05)
        rows = VGroup(
            label(r"\textbf{FA 4.16} \ $T$ is \emph{compact} if $T(B)$ has", font_size=26),
            label(r"compact closure", font_size=26),
            label(r"in Hilbert space: \ $T$ is a norm limit", font_size=26),
            label(r"of finite-rank operators", font_size=26, color=C.EPS),
            label(r"the unit ball goes to a thin set:", font_size=24, color=GREY_A),
            label(r"its axes shrink to $0$", font_size=24, color=GREY_A),
            label(r"$T$ compact $\Rightarrow$ $T^*$ compact \ (4.19)", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([5.0, -0.4, 0])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to([2.2, -0.4, 0], RIGHT, buff=0)
        head = label(r"Compact operators squeeze the ball into something thin", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> An operator is compact if it sends the unit ball into a set with compact closure. "
            "<bookmark mark='b'/> The Volterra operator from chapter one is an example: it maps the unit ball onto an "
            "infinite-dimensional ellipsoid whose axes are two over pi, two over three pi, two over five pi, falling to "
            "zero. <bookmark mark='c'/> Thin in every direction but finitely many: so in Hilbert space a compact "
            "operator is a limit of finite-rank ones, matrices in disguise."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[:2]), Create(ax), Create(unit))
            vo.wait_until("b")
            self.play(TransformFromCopy(unit, thin_e), FadeIn(sch))
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.1), FadeIn(b_l), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def string(self):
        d = load("compact")
        w, exact, xs, vecs = d["w"], d["exact"], d["xs"], d["vecs"]
        ax = plain_axes([0, 1, 0.25], [-1.2, 1.2, 1], 5.4, 2.8).move_to([-3.5, 0.3, 0])
        cols = [C.SEQ, C.APPROX, C.EPS, C.CONNECTED_SET]
        modes = VGroup(*[polyline(ax, xs, v, color=c, stroke_width=3) for v, c in zip(vecs, cols)])
        m_l = label(r"eigenvectors: \ $\sin n\pi x$", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.08)
        bx = plain_axes([0.5, 30.5, 5], [0, 0.11, 0.05], 5.4, 2.0).move_to([-3.5, -2.45, 0])
        dots = VGroup(*[Dot(bx.c2p(k + 1, v), radius=0.045, color=C.OPERATOR) for k, v in enumerate(w)])
        acc = DashedLine(bx.c2p(0.5, 0), bx.c2p(30.5, 0), color=C.EPS, stroke_width=2)
        b_l = label(r"eigenvalues, \ accumulating only at $0$", font_size=22, color=C.OPERATOR).next_to(bx, UP, buff=0.05)
        rows = VGroup(
            MathTex(r"(Gf)(x) = \int_0^1 G(x, y) f(y)\,dy", font_size=28),
            MathTex(r"G(x, y) = \min(x, y)\,(1 - \max(x, y))", font_size=26),
            label(r"solves $-u'' = f$, \ $u(0) = u(1) = 0$: \ the string", font_size=22, color=GREY_A),
            MathTex(r"\lambda_n = \frac{1}{n^2\pi^2}:", font_size=28, color=C.EPS),
            MathTex(rf"\text{{computed }} (N = 2000): \ {w[0]:.6f},\ {w[1]:.6f},\ {w[2]:.6f}", font_size=22),
            MathTex(rf"\text{{exact}}: \ {exact[0]:.6f},\ {exact[1]:.6f},\ {exact[2]:.6f}", font_size=22, color=GREY_A),
            label(r"each eigenvector agrees with $\sin n\pi x$ to $10^{-3}$", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.4, -0.4, 0])
        for r_ in rows:
            if r_.width > 6.2:
                r_.width = 6.2
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.4, -0.4, 0])
        assert np.allclose(w[:10], exact, rtol=2e-3)
        # what G does: a load c on [l0, l1] pushes the string into u = Gf, the kernel integrated against the load
        l0, l1, c_ = 0.25, 0.55, 12.0
        xg = np.linspace(0, 1, 2001)
        fg = np.where((xg >= l0) & (xg <= l1), c_, 0.0)
        X, Y = np.meshgrid(xg, xg, indexing="ij")
        Gm = np.minimum(X, Y) * (1 - np.maximum(X, Y))
        wt = np.full(xg.size, xg[1] - xg[0])
        wt[[0, -1]] /= 2
        ug = Gm @ (fg * wt)
        # the exact solution of -u'' = f, u(0) = u(1) = 0: u(x) = x int (1 - y) f - int_0^x (x - y) f
        m_ = np.clip(xg, l0, l1)
        u_ex = (xg * c_ * ((l1 - l0) - (l1 ** 2 - l0 ** 2) / 2)
                - c_ * ((np.maximum(xg - l0, 0)) ** 2 - (xg - m_) ** 2 * (xg > l1)) / 2)
        assert np.abs(ug - u_ex).max() < 2e-3 * u_ex.max() and abs(ug[0]) < 1e-12 and abs(ug[-1]) < 1e-12
        load_ = VGroup(*[Arrow(ax.c2p(t, -0.85), ax.c2p(t, -0.2), buff=0, color=C.MEASURE, stroke_width=3,
                               max_tip_length_to_length_ratio=0.25) for t in np.linspace(l0, l1, 6)])
        u_g = polyline(ax, xg, ug, color=C.FUNC, stroke_width=4)
        imax = int(np.argmax(ug))
        load_l = VGroup(
            label(rf"a load $f = {c_:.0f}$ on $[{l0}, {l1}]$", font_size=22, color=C.MEASURE).next_to(
                ax.c2p(l1, -0.6), RIGHT, buff=0.25),
            MathTex(r"u = Gf", font_size=28, color=C.FUNC).next_to(ax.c2p(xg[imax], ug[imax]), UR, buff=0.12),
        )
        u_l = label(r"what $G$ does: \ load in, \ shape of the string out", font_size=24, color=GREY_A).next_to(
            ax, UP, buff=0.08)
        head = label(r"A compact operator: \ the vibrating string's Green's function", font_size=32).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> The model compact operator is an integral operator with a continuous kernel. This "
            "one solves the equation of a string held at both ends: given a load f, it returns the displacement. "
            "<bookmark mark='b'/> Discretize it with two thousand points and diagonalize. The eigenvectors are the "
            "string's modes, sine n pi x, <bookmark mark='c'/> and the eigenvalues are one over n squared pi squared, "
            "to three digits, falling to zero. A compact operator's eigenvalues can only pile up at zero."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[:3]), Create(ax), FadeIn(u_l))
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in load_], lag_ratio=0.1), FadeIn(load_l[0]), run_time=1.5)
            self.play(Create(u_g), FadeIn(load_l[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeOut(load_), FadeOut(load_l), FadeOut(u_g), ReplacementTransform(u_l, m_l))
            self.play(LaggedStart(*[Create(m_) for m_ in modes], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(bx), Create(acc), FadeIn(b_l), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.05),
                      run_time=2.0)
            self.play(FadeIn(rows[3:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fredholm(self):
        card = dictionary_card(r"$n \times n$ matrices", r"compact operators \ (FA 4.18--4.25)", [
            (r"finitely many eigenvalues", r"countably many, \ accumulating only at $0$"),
            (r"each eigenspace finite-dimensional", r"each $\lambda \ne 0$: \ finite multiplicity"),
            (r"$A - \lambda$ one-to-one $\iff$ onto", r"$\dim N(T - \lambda) = \operatorname{codim} R(T - \lambda)$"),
            (r"spectrum = eigenvalues", r"spectrum = eigenvalues, \ and $0$"),
            (r"symmetric: \ an orthonormal eigenbasis", r"the spectral theorem \ (Part 10)"),
        ], font_size=24)
        head = label(r"Riesz--Schauder: \ linear algebra survives for compact operators", font_size=32).to_edge(UP, buff=0.3)
        card.scale(0.85).next_to(head, DOWN, buff=0.3)
        # the spectrum of a non-symmetric compact operator, K(x, y) = e^{-|x - y|} e^{6ixy} on L^2[0, 1], in the
        # complex plane with radius log10|lambda| (rings at 10^-1, 10^-2, 10^-3): finitely many outside every ring
        def spec(N):
            xg = (np.arange(N) + 0.5) / N
            X, Y = np.meshgrid(xg, xg, indexing="ij")
            w = np.linalg.eigvals(np.exp(-np.abs(X - Y)) * np.exp(6j * X * Y) / N)
            return w[np.argsort(-np.abs(w))]

        wa, wb = spec(400), spec(800)
        assert np.max(np.abs(wa[:10] - wb[:10]) / np.abs(wb[:10])) < 2e-3  # these are the operator's, not the grid's
        eps_ = [1e-1, 1e-2, 1e-3]
        cnt = [int((np.abs(wb) > e_).sum()) for e_ in eps_]
        assert cnt == [int((np.abs(wa) > e_).sum()) for e_ in eps_]
        Rr, ctr = 1.45, np.array([-3.6, -2.3, 0])

        def rho(m):
            return Rr * max(0.0, (math.log10(m) + 4) / 4)

        rings = VGroup(*[Circle(radius=rho(e_), color=GREY_C, stroke_width=1.5).move_to(ctr) for e_ in eps_])
        rlabs = VGroup(*[MathTex(rf"10^{{-{k + 1}}}", font_size=20, color=GREY_B).move_to(
            ctr + (rho(e_) + 0.2) * np.array([math.cos(-0.5), math.sin(-0.5), 0])) for k, e_ in enumerate(eps_)])
        big = wb[np.abs(wb) > 1e-4]
        sdots = VGroup(*[Dot(ctr + rho(abs(z)) * np.array([math.cos(np.angle(z)), math.sin(np.angle(z)), 0]),
                             radius=0.045, color=C.OPERATOR) for z in big])
        zero = Dot(ctr, radius=0.06, color=C.EPS)
        sl = MathTex(r"K(x, y) = e^{-|x - y|}\,e^{6ixy}", font_size=24, color=C.OPERATOR).next_to(ctr, RIGHT, buff=Rr + 0.4)
        sl.shift(UP * 0.85)
        cl = VGroup(label(r"its eigenvalues in $\mathbb C$, \ radius $\propto 4 + \log_{10}|\lambda|$ \ (center: $|\lambda| \le 10^{-4}$)", font_size=22, color=GREY_A),
                    MathTex(rf"\#\{{|\lambda| > 10^{{-1}}\}} = {cnt[0]}, \ \ \#\{{|\lambda| > 10^{{-2}}\}} = {cnt[1]}, "
                            rf"\ \ \#\{{|\lambda| > 10^{{-3}}\}} = {cnt[2]}", font_size=24, color=C.EPS),
                    label(r"finitely many outside every circle: \ they can pile up only at $0$", font_size=22,
                          color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        cl.next_to(sl, DOWN, buff=0.25, aligned_edge=LEFT)
        assert cl.get_right()[0] < 6.95 and card.get_bottom()[1] > ctr[1] + Rr + 0.15 and ctr[1] - Rr > -3.95
        with self.voiceover(
            "<bookmark mark='a'/> For compact operators, almost all of finite-dimensional linear algebra survives. "
            "<bookmark mark='b'/> The nonzero spectrum consists of eigenvalues of finite multiplicity, accumulating "
            "only at zero. <bookmark mark='c'/> And Fredholm's alternative holds: T minus lambda is one-to-one exactly "
            "when it's onto, as for square matrices. <bookmark mark='d'/> The symmetric ones even have orthonormal "
            "eigenbases; that's the spectral theorem, which Part 10 proves in full."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(card.titles), Create(rings), FadeIn(rlabs), FadeIn(zero), FadeIn(sl))
            vo.wait_until("b")
            for i in (0, 1):
                self.play(FadeIn(card.rows[i]), FadeIn(card.arrows[i]), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in sdots], lag_ratio=0.03), FadeIn(cl[0]), run_time=2.0)
            self.play(FadeIn(cl[1:]))
            vo.wait_until("c")
            for i in (2, 3):
                self.play(FadeIn(card.rows[i]), FadeIn(card.arrows[i]), run_time=0.7)
            vo.wait_until("d")
            self.play(FadeIn(card.rows[4]), FadeIn(card.arrows[4]))
        self.wait(0.4)
        self.clear_scene()
