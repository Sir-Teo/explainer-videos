from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis10.common import cplot, heatmap, load, plain_axes, square_axes
from videos.analysis10.compute import rand_matrix


class BanachAlgebras(VoiceoverScene):
    def construct(self):
        self.card()
        self.examples()
        self.neumann()
        self.open_set()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(1, r"Banach algebras", r"What can we do with operators that we do with numbers?", lit=(1932,),
                            part=10)
        with self.voiceover("Chapter one: Banach algebras, where elements can be multiplied as well as added."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def examples(self):
        panels = self.algebra_panels()
        # submultiplicativity, checked on random matrices and random l^1 sequences
        rng = np.random.default_rng(2)
        rat_m, rat_l = [], []
        for _ in range(2000):
            A, B = rng.normal(size=(2, 5, 5))
            rat_m.append(np.linalg.norm(A @ B, 2) / (np.linalg.norm(A, 2) * np.linalg.norm(B, 2)))
        for _ in range(2000):
            a, b = rng.normal(size=(2, 30))
            rat_l.append(np.abs(np.convolve(a, b)).sum() / (np.abs(a).sum() * np.abs(b).sum()))
        rat_m, rat_l = np.array(rat_m), np.array(rat_l)
        worst_m, worst_l = float(rat_m.max()), float(rat_l.max())
        assert worst_m <= 1 + 1e-12 and worst_l <= 1 + 1e-12
        # the 2000 ratios of each kind as histograms, against the line at 1 they never cross
        bins = np.linspace(0, 1.1, 45)
        hists = VGroup()
        for k_, (vals, col, ttl) in enumerate(((rat_m, C.OPERATOR, r"\|AB\| \,/\, (\|A\|\,\|B\|), \ \ 5 \times 5 \text{ matrices}"),
                                             (rat_l, C.FUNCTIONAL, r"\|a * b\|_1 \,/\, (\|a\|_1 \|b\|_1), \ \ \ell^1, \text{ length } 30"))):
            cnt, _ = np.histogram(vals, bins)
            hx = plain_axes([0, 1.1, 0.25], [0, float(cnt.max()) * 1.1, max(1, int(cnt.max() // 2))], 5.4, 2.3)
            hx.move_to([-3.4 + 6.8 * k_, -0.15, 0])
            bars_ = VGroup(*[Rectangle(width=hx.c2p(bins[1], 0)[0] - hx.c2p(bins[0], 0)[0], height=max(
                hx.c2p(0, c_)[1] - hx.c2p(0, 0)[1], 1e-3), stroke_width=0.5, stroke_color=BLACK, fill_color=col,
                fill_opacity=0.85).move_to(hx.c2p((bins[i] + bins[i + 1]) / 2, c_ / 2)) for i, c_ in enumerate(cnt) if c_])
            one = DashedLine(hx.c2p(1, 0), hx.c2p(1, float(cnt.max()) * 1.1), color=C.PATHOLOGY, stroke_width=3)
            onel = MathTex("1", font_size=26, color=C.PATHOLOGY).next_to(hx.c2p(1, 0), DOWN, buff=0.12)
            ttl_ = MathTex(ttl, font_size=24, color=col).next_to(hx, UP, buff=0.15)
            hists.add(VGroup(hx, bars_, one, onel, ttl_))
        assert hists.get_left()[0] > -6.95 and hists.get_right()[0] < 6.95
        rule = VGroup(
            MathTex(r"\|xy\| \le \|x\|\,\|y\|, \qquad \|e\| = 1", font_size=36, color=C.EPS),
            MathTex(rf"\text{{largest ratio in 2000 random tries: matrices }} {worst_m:.4f}, \ \ \ell^1 \ {worst_l:.4f}",
                    font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        head = label(r"\textbf{RCA 18.1, FA 10.1} \ a complete normed space with a product", font_size=32).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> A Banach algebra is a complete normed space where you can also multiply, with the "
            "norm of a product at most the product of the norms. <bookmark mark='b'/> The continuous functions on a "
            "compact set, with the pointwise product. <bookmark mark='b2'/> The bounded operators on a Banach space, "
            "with composition: the main example. <bookmark mark='b3'/> The integrable functions with convolution, "
            "from Part 9, <bookmark mark='b4'/> and summable sequences with convolution, <bookmark mark='b5'/> and "
            "the disc algebra of Part 7. <bookmark mark='c'/> Test the rule: in two thousand random "
            "trials of each kind, the ratio piles up below one and never crosses it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rule[0]))
            for k_, mk in enumerate(("b", "b2", "b3", "b4", "b5")):  # each algebra with its product, drawn
                vo.wait_until(mk)
                t_, pic_, cap_ = panels[k_]
                self.play(FadeIn(t_), FadeIn(pic_[0]), run_time=0.5)
                self.play(*[Create(m_) if isinstance(m_, VMobject) else FadeIn(m_) for m_ in pic_[1:]], run_time=1.3)
                self.play(FadeIn(cap_), run_time=0.5)
            vo.wait_until("c")
            self.play(FadeOut(panels))
            for h_ in hists:
                self.play(Create(h_[0]), FadeIn(h_[4]), run_time=0.6)
                self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in h_[1]], lag_ratio=0.03), run_time=1.4)
                self.play(Create(h_[2]), FadeIn(h_[3]), run_time=0.5)
            self.play(FadeIn(rule[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def algebra_panels(self) -> Group:
        """Five algebras, each as (title, picture, caption): the product drawn, the norm inequality computed."""
        def panel(title, pic, cap, center):  # title: [(tex, color), ...]
            t_ = MathTex(*[tx for tx, _ in title], font_size=22)
            for part_, (_, col_) in zip(t_, title):
                part_.set_color(col_)
            t_.move_to([center[0], center[1] + 1.05, 0])
            pic.move_to([center[0], center[1] - 0.05, 0])
            c_ = MathTex(cap, font_size=19, color=GREY_A).move_to([center[0], center[1] - 0.95, 0])
            for m_ in (t_, c_):
                if m_.width > 4.1:
                    m_.width = 4.1
            return Group(t_, pic, c_)

        out = Group()
        # 1. C[0, 1], pointwise product, sup norm
        x = np.linspace(0, 1, 801)
        f, g = 0.6 + 0.4 * np.sin(2 * math.pi * x), 0.3 + 0.9 * x
        nf, ng, nfg = f.max(), g.max(), (f * g).max()
        assert nfg <= nf * ng
        ax = plain_axes([0, 1, 0.5], [0, 1.3, 1], 3.2, 1.3)
        pic = VGroup(ax, polyline_(ax, x, f, C.FUNC, 2.5), polyline_(ax, x, g, C.APPROX, 2.5),
                     polyline_(ax, x, f * g, C.EPS, 3.5))
        out.add(panel([(r"C[0, 1]: \ ", WHITE), ("f", C.FUNC), (r",\ ", WHITE), ("g", C.APPROX), (r",\ ", WHITE),
                       ("fg", C.EPS)], pic,
                      rf"\|fg\|_\infty = {nfg:.2f} \le \|f\|_\infty\|g\|_\infty = {nf * ng:.2f}", (-4.4, 1.6)))
        # 2. B(R^2), composition, operator norm = the longest semi-axis of the image of the unit circle
        A = np.array([[0.8, -0.3], [0.5, 0.7]])
        B = np.array([[1.0, 0.4], [0.0, 0.6]])
        n2 = lambda M: np.linalg.norm(M, 2)  # noqa: E731
        nA, nB, nAB = n2(A), n2(B), n2(A @ B)
        assert nAB <= nA * nB
        th = np.linspace(0, 2 * math.pi, 241)
        circ = np.stack([np.cos(th), np.sin(th)])
        bx = square_axes([-1.3, 1.3, 1], [-1.3, 1.3, 1], 0.52)
        u, sv, vt = np.linalg.svd(A @ B)
        tip = u[:, 0] * sv[0]
        assert abs(sv[0] - nAB) < 1e-12 and np.abs(A @ B @ circ).max() <= 1.3
        pic = VGroup(bx, polyline_(bx, circ[0], circ[1], GREY_B, 2),
                     polyline_(bx, *(B @ circ), C.APPROX, 2.5), polyline_(bx, *(A @ B @ circ), C.EPS, 3.5),
                     Line(bx.c2p(0, 0), bx.c2p(*tip), color=C.EPS, stroke_width=3))
        out.add(panel([(r"B(\mathbb R^2): \ ", WHITE), (r"\text{circle}", GREY_B), (r"\ \mapsto\ ", WHITE),
                       (r"B", C.APPROX), (r",\ ", WHITE), (r"AB", C.EPS)], pic,
                      rf"\|AB\| = {nAB:.4f} \le \|A\|\,\|B\| = {nA * nB:.4f}", (0.0, 1.6)))
        # 3. L^1(R), convolution: a box and a signed step
        h = 0.002
        xx = np.arange(0, 1, h) + h / 2
        fb, gs = np.ones_like(xx), np.where(xx < 0.5, 1.6, -0.8)
        cv = np.convolve(fb, gs) * h
        xc = np.arange(len(cv)) * h + h
        n1f, n1g, n1c = np.abs(fb).sum() * h, np.abs(gs).sum() * h, np.abs(cv).sum() * h
        assert n1c <= n1f * n1g and abs(n1c - 0.7) < 1e-3
        cx = plain_axes([-0.2, 2.2, 1], [-1.0, 1.8, 1], 3.4, 1.3)
        pic = VGroup(cx, polyline_(cx, [-0.2, 0, 0, 1, 1, 2.2], [0, 0, 1, 1, 0, 0], C.FUNC, 2.5),
                     polyline_(cx, [-0.2, 0, 0, 0.5, 0.5, 1, 1, 2.2], [0, 0, 1.6, 1.6, -0.8, -0.8, 0, 0], C.APPROX, 2.5),
                     polyline_(cx, np.concatenate([[0], xc]), np.concatenate([[0], cv]), C.EPS, 3.5))
        out.add(panel([(r"L^1(\mathbb R): \ ", WHITE), ("f", C.FUNC), (r",\ ", WHITE), ("g", C.APPROX), (r",\ ", WHITE),
                       ("f * g", C.EPS)], pic,
                      rf"\|f * g\|_1 = {n1c:.2f} \le \|f\|_1\|g\|_1 = {n1f * n1g:.2f}", (4.4, 1.6)))
        # 4. l^1(Z), convolution of sequences
        a = np.array([1.0, -0.6, 0.3])
        b = np.array([0.8, 0.5])
        ab = np.convolve(a, b)
        na, nb, nab = np.abs(a).sum(), np.abs(b).sum(), np.abs(ab).sum()
        assert nab <= na * nb
        sx = plain_axes([-0.5, 11.5, 1], [-0.8, 1.1, 1], 3.6, 1.3)
        stems = VGroup()
        for off, seq, col in ((0, a, C.FUNC), (4, b, C.APPROX), (7, ab, C.EPS)):
            for k_, v_ in enumerate(seq):
                stems.add(Line(sx.c2p(off + k_, 0), sx.c2p(off + k_, v_), color=col, stroke_width=5))
        pic = VGroup(sx, stems)
        out.add(panel([(r"\ell^1(\mathbb Z): \ ", WHITE), ("a", C.FUNC), (r",\ ", WHITE), ("b", C.APPROX), (r",\ ", WHITE),
                       ("a * b", C.EPS)], pic,
                      rf"\|a * b\|_1 = {nab:.2f} \le \|a\|_1\|b\|_1 = {na * nb:.2f}", (-2.2, -1.05)))
        # 5. the disc algebra: fg on the closed disc; the sup norm is reached on the circle (maximum modulus)
        z = np.exp(1j * np.linspace(0, 2 * math.pi, 20001))
        F_, G_ = (lambda w: 1 + w / 2), (lambda w: 1 - w * w / 2)
        nF, nG, nFG = np.abs(F_(z)).max(), np.abs(G_(z)).max(), np.abs(F_(z) * G_(z)).max()
        zz = (np.linspace(-1, 1, 301)[None, :] + 1j * np.linspace(-1, 1, 301)[:, None]).ravel()
        zz = zz[np.abs(zz) < 1]
        assert np.abs(F_(zz) * G_(zz)).max() <= nFG + 1e-9 and nFG <= nF * nG
        zmax = z[int(np.argmax(np.abs(F_(z) * G_(z))))]
        dx = square_axes([-1.1, 1.1, 1], [-1.1, 1.1, 1], 0.6)
        img = cplot(dx, lambda w: F_(w) * G_(w), (-1.0, 1.0), (-1.0, 1.0), px=300, mask=lambda w: np.abs(w) <= 1)
        pic = Group(dx, img, Circle(radius=dx.c2p(1, 0)[0] - dx.c2p(0, 0)[0], color=GREY_B, stroke_width=2).move_to(
            dx.c2p(0, 0)), Dot(dx.c2p(zmax.real, zmax.imag), radius=0.06, color=WHITE))
        out.add(panel([(r"A(\mathbb D): \ fg, \ \ f = 1 + \tfrac z2, \ g = 1 - \tfrac{z^2}{2}", WHITE)], pic,
                      rf"\max_{{|z| \le 1}}|fg| = {nFG:.3f} \le \|f\|\,\|g\| = {nF * nG:.2f}", (2.2, -1.05)))
        return out

    # ------------------------------------------------------------------
    def neumann(self):
        d = load("neumann")
        errs, bound = d["errs"], d["bound"]
        n = np.arange(40)
        ax = plain_axes([0, 40, 10], [-7, 1, 1], 6.2, 4.4, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.2, -0.5, 0])
        xl = MathTex(r"n", font_size=22).next_to(ax.x_axis, RIGHT, buff=0.1)
        yl = MathTex(r"\log_{10}\Big\|\sum_{k \le n} A^k - (I - A)^{-1}\Big\|", font_size=22).next_to(ax, UP, buff=0.1)
        bl = polyline_(ax, n, np.log10(bound), C.PATHOLOGY)
        dots = VGroup(*[Dot(ax.c2p(k, math.log10(e)), radius=0.045, color=C.OPERATOR) for k, e in zip(n, errs)])
        bt = MathTex(r"\frac{0.8^{\,n+1}}{1 - 0.8}", font_size=26, color=C.PATHOLOGY).next_to(ax.c2p(30, math.log10(bound[30])),
                                                                                         UP, buff=0.15)
        assert np.all(errs <= bound * (1 + 1e-9))
        # the leftover term of the telescoping, ||A^{n+1}||, for the same matrix (norm 0.8), and its bound 0.8^{n+1}
        A_ = rand_matrix(6, 3)
        A_ *= 0.8 / np.linalg.norm(A_, 2)
        P_, pw = np.eye(6), []
        for _ in range(40):
            P_ = P_ @ A_
            pw.append(np.linalg.norm(P_, 2))
        pw = np.array(pw)
        assert np.all(pw <= 0.8 ** (n + 1) * (1 + 1e-9)) and np.all(errs <= pw / 0.2 * (1 + 1e-9))
        assert np.log10(pw).min() > -7
        pdots = VGroup(*[Dot(ax.c2p(k, math.log10(v)), radius=0.04, color=GREY_B) for k, v in zip(n, pw)])
        pline = DashedVMobject(polyline_(ax, n, (n + 1) * math.log10(0.8), C.EPS, 2.5), num_dashes=40)
        pdl = MathTex(r"\|A^{n+1}\|", font_size=24, color=GREY_B).next_to(ax.c2p(9, math.log10(pw[9])), DL, buff=0.15)
        pbl = MathTex(r"\|A\|^{n+1} = 0.8^{\,n+1}", font_size=24, color=C.EPS).next_to(
            ax.c2p(20, 21 * math.log10(0.8)), DOWN, buff=0.35)
        yl0 = MathTex(r"\log_{10} \text{ of each norm}", font_size=22).next_to(ax, UP, buff=0.1)
        lad = VGroup(
            MathTex(r"(I - A)(I + A + \cdots + A^n) = I - A^{n+1}", font_size=30),
            MathTex(r"\|A^{n+1}\| \le \|A\|^{n+1} \to 0 \quad \text{if } \|A\| < 1", font_size=30),
            MathTex(r"(I - A)^{-1} = \sum_{n \ge 0} A^n", font_size=36, color=C.EPS),
            MathTex(r"\big\|(I - A)^{-1}\big\| \le \frac{1}{1 - \|A\|}", font_size=30, color=GREY_A),
            label(r"a random $6 \times 6$ complex $A$ with $\|A\| = 0.8$:", font_size=24),
            label(r"every error under the geometric bound", font_size=24, color=C.OPERATOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.6, -0.3, 0])
        head = label(r"The geometric series, \ for operators", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> The first tool is the oldest series there is. Multiply I minus A by one plus A "
            "plus up to A to the n, and everything telescopes to I minus A to the n plus one. "
            "<bookmark mark='b'/> If the norm of A is below one, that last term dies, so I minus A is invertible, "
            "and its inverse is the geometric series: the Neumann series. <bookmark mark='c'/> For a random matrix "
            "of norm 0.8, the partial sums close in on the inverse, always under the geometric bound."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(lad[0]), Create(ax), FadeIn(xl), FadeIn(yl0))
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in pdots], lag_ratio=0.05), FadeIn(pdl), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(lad[1]), Create(pline), FadeIn(pbl))
            self.play(FadeIn(lad[2]), FadeIn(lad[3]))
            vo.wait_until("c")
            self.play(FadeIn(lad[4]), pdots.animate.set_opacity(0.35), FadeOut(pdl), FadeOut(pbl), FadeTransform(yl0, yl),
                      pline.animate.set_stroke(opacity=0.35))
            self.play(Create(bl), FadeIn(bt))
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.05), FadeIn(lad[5]), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def open_set(self):
        # a slice through the 2 x 2 matrices: M(s, t) = [[1 + s, t], [t, 1 - s]], det = 1 - s^2 - t^2
        ax = square_axes([-2.2, 2.8, 1], [-2.2, 2.2, 1], 1.15, numbers=True, font_size=16,
                         x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                         y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.3, -0.4, 0])
        img = heatmap(lambda X, Y: np.log10(np.abs(1 - X * X - Y * Y) + 1e-3), (-2.2, 2.8), (-2.2, 2.2),
                      ax.c2p(2.8, 0)[0] - ax.c2p(-2.2, 0)[0], ax.c2p(0, 2.2)[1] - ax.c2p(0, -2.2)[1], -1.5, 1.5,
                      neg=C.PATHOLOGY, pos=C.OPERATOR).move_to(ax.c2p(0.3, 0))
        unit = ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]
        sing = Circle(radius=unit, color=C.PATHOLOGY, stroke_width=4).move_to(ax.c2p(0, 0))
        sl = MathTex(r"\det = 0", font_size=24, color=C.PATHOLOGY).next_to(ax.c2p(-0.72, 0.72), UL, buff=0.05)
        # the Neumann balls: around I (radius 1 / ||I^-1|| = 1) and around A = M(1.6, 0) (radius 1 / ||A^-1|| = 0.6)
        A = np.array([[2.6, 0], [0, -0.6]])
        rA = 1 / np.linalg.norm(np.linalg.inv(A), 2)
        assert abs(rA - 0.6) < 1e-12
        # in this slice ||M(s, t) - M(s', t')|| = |(s, t) - (s', t')|, so the balls are discs, tangent to det = 0
        E1, E2 = np.diag([1.0, -1.0]), np.array([[0.0, 1.0], [1.0, 0.0]])
        rng = np.random.default_rng(4)
        for _ in range(200):
            s, t = rng.normal(size=2)
            assert abs(np.linalg.norm(s * E1 + t * E2, 2) - math.hypot(s, t)) < 1e-12
        b1 = DashedVMobject(Circle(radius=unit * 0.999, color=C.EPS, stroke_width=3).move_to(ax.c2p(0, 0)), num_dashes=40)
        b2 = Circle(radius=unit * rA, color=C.EPS, stroke_width=3, fill_color=C.EPS, fill_opacity=0.15).move_to(
            ax.c2p(1.6, 0))
        dI = Dot(ax.c2p(0, 0), radius=0.06, color=WHITE)
        dA = Dot(ax.c2p(1.6, 0), radius=0.06, color=WHITE)
        lI = MathTex(r"I", font_size=26).next_to(dI, DOWN, buff=0.08)
        lA = MathTex(r"A", font_size=26).next_to(dA, DOWN, buff=0.08)
        sl2 = MathTex(r"M(s, t) = \begin{pmatrix} 1 + s & t \\ t & 1 - s\end{pmatrix}", font_size=26).next_to(ax, UP,
                                                                                                         buff=0.1)
        rows = VGroup(
            label(r"\textbf{RCA 18.4} \ if $x$ is invertible and $\|y\| < 1/\|x^{-1}\|$:", font_size=24),
            MathTex(r"x - y = x\,(e - x^{-1}y) \ \text{ is invertible (Neumann)}", font_size=28),
            label(r"so the invertible elements form an open set,", font_size=24, color=C.EPS),
            label(r"and $x \mapsto x^{-1}$ is continuous", font_size=24, color=C.EPS),
            MathTex(rf"\text{{here: }} 1/\|A^{{-1}}\| = {rA:.1f}, \ \text{{exactly the distance to }} \det = 0", font_size=24,
                    color=GREY_A),
            label(r"Part 4's lemma (PMA 9.8), \ in its final home", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.6, -0.2, 0])
        for r_ in rows:
            if r_.width > 6.4:
                r_.width = 6.4
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.6, -0.2, 0])
        head = label(r"The invertible elements form an open set", font_size=34).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Here's a slice through the two by two matrices, around the identity. The red circle "
            "is where the determinant vanishes. <bookmark mark='b'/> The Neumann series says: if x is invertible, "
            "anything closer to x than one over the norm of x inverse is invertible too. Around the identity that's a "
            "disc of radius one, and around this matrix A, radius 0.6. <bookmark mark='c'/> Both discs touch the "
            "singular circle exactly, so the bound is sharp. The invertible elements form an open set, and inversion "
            "is continuous: the lemma from Part 4, in its final home."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(img), Create(ax), FadeIn(sl2))
            self.play(Create(sing), FadeIn(sl))
            vo.wait_until("b")
            self.play(FadeIn(dI), FadeIn(lI), Create(b1), FadeIn(rows[:2]))
            self.play(FadeIn(dA), FadeIn(lA), DrawBorderThenFill(b2))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:5]))
            self.play(FadeIn(rows[5]))
        self.wait(0.4)
        self.clear_scene()


def polyline_(ax, xs, ys, color, stroke_width=3):
    m = VMobject(color=color, stroke_width=stroke_width)
    m.set_points_as_corners([ax.c2p(float(a), float(b)) for a, b in zip(xs, ys)])
    return m
