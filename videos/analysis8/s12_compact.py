from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis8.common import boxes_overlap, load, plain_axes, polyline, square_axes


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
        bars = VGroup(Line([-6.55, -2.6, 0], [-2.05, -2.6, 0], color=GREY_C, stroke_width=1.5))  # the baseline 0
        for k in range(10):
            v = float(s[k])
            bars.add(Rectangle(width=0.28, height=4.0 * v / float(s[0]), stroke_width=0, fill_color=C.OPERATOR,
                               fill_opacity=0.85).move_to([-6.3 + 0.45 * k, -2.6 + 2.0 * v / float(s[0]), 0]))
        assert np.allclose(s[:6], 2 / ((2 * np.arange(1, 7) - 1) * math.pi), atol=1e-4)
        b_l = label(r"the semi-axes of $V(B)$: \ $\frac{2}{\pi}, \frac{2}{3\pi}, \frac{2}{5\pi}, \ldots \to 0$", font_size=24,
                    color=C.OPERATOR).next_to(bars, UP, buff=0.2).align_to(bars, LEFT)
        ax = square_axes([-1.3, 1.3, 1], [-1.3, 1.3, 1], 1.25).move_to([0.25, -0.6, 0])
        ax.set_opacity(0.3)
        th = np.linspace(0, 2 * np.pi, 300)
        unit = VMobject(color=GREY_B, stroke_width=2).set_points_as_corners([ax.c2p(math.cos(t), math.sin(t)) for t in th])
        # V(B) cut by the plane of its first two axes: the ellipse with semi-axes s_1 = 2/pi and s_2 = 2/(3 pi), to scale
        # inside the unit ball B
        thin_e = VMobject(color=C.OPERATOR, stroke_width=3, fill_color=C.OPERATOR, fill_opacity=0.2).set_points_as_corners(
            [ax.c2p(float(s[0]) * math.cos(t), float(s[1]) * math.sin(t)) for t in th])
        sch = note(r"$V(B)$: \ its first two axes, \ to scale").next_to(ax, DOWN, buff=0.05)
        assert sch.get_left()[0] > bars.get_right()[0] + 0.3
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
        m_l = MathTex(r"\text{eigenvectors } \sin n\pi x: \ \ n = ", "1", r",\ ", "2", r",\ ", "3", r",\ ", "4",
                      font_size=26, color=GREY_A).next_to(ax, UP, buff=0.08)
        for i_, c_ in zip((1, 3, 5, 7), cols):
            m_l[i_].set_color(c_)
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
        head = label(r"A compact operator: \ the vibrating string's Green's function", font_size=34).to_edge(UP, buff=0.3)
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
            self.play(FadeOut(load_), FadeOut(load_l), FadeOut(u_g), FadeTransform(u_l, m_l))
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
        head = label(r"Riesz--Schauder: \ linear algebra survives for compact operators", font_size=34).to_edge(UP, buff=0.3)
        card.scale(0.85).next_to(head, DOWN, buff=0.3)
        # the spectrum of a non-self-adjoint compact operator, K(x, y) = e^{-(x - y)^2} e^{4ixy} on L^2[0, 1], in the
        # complex plane with radius 4 + log10|lambda| (rings at 10^-1, 10^-2, 10^-3): finitely many outside every ring.
        # A smooth kernel: its eigenvalues fall off fast and sit well clear of the rings, so the counts can be read
        # off the picture
        def spec(N):
            xg = (np.arange(N) + 0.5) / N
            X, Y = np.meshgrid(xg, xg, indexing="ij")
            w = np.linalg.eigvals(np.exp(-(X - Y) ** 2) * np.exp(4j * X * Y) / N)
            return w[np.argsort(-np.abs(w))]

        wa, wb = spec(300), spec(600)
        nb = int((np.abs(wb) > 1e-5).sum())
        assert np.max(np.abs(wa[:nb] - wb[:nb]) / np.abs(wb[:nb])) < 2e-3  # these are the operator's, not the grid's
        eps_ = [1e-1, 1e-2, 1e-3]
        cnt = [int((np.abs(wb) > e_).sum()) for e_ in eps_]
        assert cnt == [int((np.abs(wa) > e_).sum()) for e_ in eps_] == [2, 3, 4]
        lgw = np.log10(np.abs(wb[:nb]))
        assert all(np.min(np.abs(lgw - math.log10(e_))) > 0.3 for e_ in eps_)  # no eigenvalue near a ring
        Rr, ctr = 1.6, np.array([-3.6, -1.85, 0])

        def rho(m):
            return Rr * max(0.0, (math.log10(m) + 4) / 4)

        rings = VGroup(*[Circle(radius=rho(e_), color=GREY_C, stroke_width=1.5).move_to(ctr) for e_ in eps_])
        big = wb[np.abs(wb) > 1e-4]
        dpos = [ctr + rho(abs(z)) * np.array([math.cos(np.angle(z)), math.sin(np.angle(z)), 0]) for z in big]
        sdots = VGroup(*[Dot(p_, radius=0.05, color=C.OPERATOR) for p_ in dpos])
        zero = Dot(ctr, radius=0.06, color=C.EPS)
        # each ring's label just outside it, all on one ray that meets no dot and no other ring
        rlabs = VGroup(*[MathTex(rf"10^{{-{k + 1}}}", font_size=20, color=GREY_B) for k in range(3)])

        def fits(t):
            u = np.array([math.cos(t), math.sin(t), 0])
            for k, (m, e_) in enumerate(zip(rlabs, eps_)):
                m.move_to(ctr + (rho(e_) + Rr / 8) * u)
                dx_, dy_ = abs(m.get_x() - ctr[0]), abs(m.get_y() - ctr[1])
                lo = math.hypot(max(0.0, dx_ - m.width / 2), max(0.0, dy_ - m.height / 2)) - 0.04  # nearest point
                hi = math.hypot(dx_ + m.width / 2, dy_ + m.height / 2) + 0.04  # farthest corner
                if any(lo < rho(r_) < hi for r_ in eps_):
                    return False
                if any(boxes_overlap(m, d_, 0.04) for d_ in sdots):
                    return False
            return True

        ray = next((t for t in np.radians(np.arange(-60, 300, 5)) if fits(t)), None)
        assert ray is not None
        fits(ray)
        sl = MathTex(r"K(x, y) = e^{-(x - y)^2}\,e^{4ixy}", font_size=24, color=C.OPERATOR).next_to(ctr, RIGHT,
                                                                                                buff=Rr + 0.5)
        sl.shift(UP * 0.85)
        cl = VGroup(label(r"its eigenvalues in $\mathbb C$, \ radius $\propto 4 + \log_{10}|\lambda|$ \ (center: $|\lambda| \le 10^{-4}$)", font_size=22, color=GREY_A),
                    MathTex(rf"\#\{{|\lambda| > 10^{{-1}}\}} = {cnt[0]}, \ \ \#\{{|\lambda| > 10^{{-2}}\}} = {cnt[1]}, "
                            rf"\ \ \#\{{|\lambda| > 10^{{-3}}\}} = {cnt[2]}", font_size=24, color=C.EPS),
                    label(r"finitely many outside every circle: \ they can pile up only at $0$", font_size=22,
                          color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        cl.next_to(sl, DOWN, buff=0.25, aligned_edge=LEFT)
        top_ = max([rings.get_top()[1], sdots.get_top()[1], rlabs.get_top()[1]])
        assert cl.get_right()[0] < 6.6 and card.get_bottom()[1] > max(top_, sl.get_top()[1]) + 0.15
        assert max(np.linalg.norm(p_ - ctr) for p_ in dpos) + 0.05 < ctr[1] + 3.6 and sl.get_left()[0] > ctr[0] + Rr + 0.3
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
