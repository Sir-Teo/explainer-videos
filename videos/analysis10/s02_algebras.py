from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis10.common import cplot, heatmap, load, phase_key, plain_axes, square_axes
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
            hx = plain_axes([0, 1.1, 0.25], [0, float(cnt.max()) * 1.1, max(1, int(cnt.max() // 2))], 5.4, 3.2)
            hx.move_to([-3.4 + 6.8 * k_, -0.15, 0])
            bars_ = VGroup(*[Rectangle(width=hx.c2p(bins[1], 0)[0] - hx.c2p(bins[0], 0)[0], height=max(
                hx.c2p(0, c_)[1] - hx.c2p(0, 0)[1], 1e-3), stroke_width=0.5, stroke_color=BLACK, fill_color=col,
                fill_opacity=0.85).move_to(hx.c2p((bins[i] + bins[i + 1]) / 2, c_ / 2)) for i, c_ in enumerate(cnt) if c_])
            one = DashedLine(hx.c2p(1, 0), hx.c2p(1, float(cnt.max()) * 1.1), color=C.EPS, stroke_width=3)
            onel = MathTex("1", font_size=26, color=C.EPS).next_to(hx.c2p(1, 0), DOWN, buff=0.12)
            ttl_ = MathTex(ttl, font_size=24, color=col).next_to(hx, UP, buff=0.15)
            hists.add(VGroup(hx, bars_, one, onel, ttl_))
        assert hists.get_left()[0] > -6.95 and hists.get_right()[0] < 6.95
        rule = VGroup(
            VGroup(label(r"\textbf{RCA 18.1, FA 10.1}", font_size=24, color=GREY_A),
                   MathTex(r"\|xy\| \le \|x\|\,\|y\|, \qquad \|e\| = 1", font_size=36, color=C.EPS)).arrange(RIGHT, buff=0.4),
            MathTex(rf"\text{{largest ratio in 2000 random tries: matrices }} {worst_m:.4f}, \ \ \ell^1 \ {worst_l:.4f}",
                    font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.35)
        assert hists.get_bottom()[1] > rule.get_top()[1] + 0.2
        head = label(r"Banach algebras: \ complete normed spaces with a product", font_size=34).to_edge(UP, buff=0.3)
        assert head.width < 12.6

        def show(m_):  # strokes are drawn, text and images fade in
            if isinstance(m_, VMobject) and not any(isinstance(q, SingleStringMathTex) for q in m_.get_family()):
                return Create(m_)
            return FadeIn(m_)

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
            self.play(FadeIn(head), FadeIn(rule[0]), FadeIn(panels[0][1][0]))
            self.play(*[Create(m_) for m_ in panels[0][1][1:]], run_time=1.5)  # a product, before the list begins
            for k_, mk in enumerate(("b", "b2", "b3", "b4", "b5")):  # each algebra with its product, drawn
                vo.wait_until(mk)
                t_, pic_, cap_ = panels[k_]
                if k_ > 0:
                    self.play(FadeIn(t_), FadeIn(pic_[0]), run_time=0.5)
                    self.play(*[show(m_) for m_ in pic_[1:]], run_time=1.3)
                else:
                    self.play(FadeIn(t_), run_time=0.5)
                self.play(FadeIn(cap_), run_time=0.5)
            vo.wait_until("c")
            self.play(FadeOut(panels))
            for h_ in hists:  # the axes come in with their bars
                self.play(Create(h_[0], run_time=0.6), FadeIn(h_[4], run_time=0.6),
                          LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in h_[1]], lag_ratio=0.03, run_time=1.8))
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
            c_ = MathTex(cap, font_size=22, color=GREY_A).move_to([center[0], center[1] - 0.95, 0])
            assert t_.width <= 4.1 and c_.width <= 4.1 and pic.width <= 4.2, (t_.width, c_.width, pic.width)
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
                      rf"\|fg\| = {nfg:.2f} \le \|f\|\,\|g\| = {nf * ng:.2f}", (-4.4, 1.6)))
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
        # 3. L^1(R), convolution: a box and a signed step (each drawn on its support only, not along the axis)
        h = 0.002
        xx = np.arange(0, 1, h) + h / 2
        fb, gs = np.ones_like(xx), np.where(xx < 0.5, 1.6, -0.8)
        cv = np.convolve(fb, gs) * h
        xc = np.arange(len(cv)) * h + h
        n1f, n1g, n1c = np.abs(fb).sum() * h, np.abs(gs).sum() * h, np.abs(cv).sum() * h
        assert n1c <= n1f * n1g and abs(n1c - 0.7) < 1e-3 and abs(cv[-1]) < 0.01
        cx = plain_axes([-0.2, 2.2, 1], [-1.0, 1.8, 1], 3.4, 1.3)
        pic = VGroup(cx, polyline_(cx, [0, 0, 1, 1], [0, 1, 1, 0], C.FUNC, 2.5),
                     polyline_(cx, [0, 0, 0.5, 0.5, 1, 1], [0, 1.6, 1.6, -0.8, -0.8, 0], C.APPROX, 2.5),
                     polyline_(cx, np.concatenate([[0], xc]), np.concatenate([[0], cv]), C.EPS, 3.5))
        out.add(panel([(r"L^1(\mathbb R): \ ", WHITE), ("f", C.FUNC), (r",\ ", WHITE), ("g", C.APPROX), (r",\ ", WHITE),
                       ("f * g", C.EPS)], pic,
                      rf"\|f * g\|_1 = {n1c:.2f} \le \|f\|_1\|g\|_1 = {n1f * n1g:.2f}", (4.4, 1.6)))
        # 4. l^1(Z), convolution of sequences: a, b and a * b, each on its own index axis from n = 0
        a = np.array([1.0, -0.6, 0.3])
        b = np.array([0.8, 0.5])
        ab = np.convolve(a, b)
        assert np.allclose(ab, [sum(a[k] * b[n - k] for k in range(len(a)) if 0 <= n - k < len(b)) for n in range(4)])
        na, nb, nab = np.abs(a).sum(), np.abs(b).sum(), np.abs(ab).sum()
        assert nab <= na * nb
        minis = VGroup()
        for seq, col, nm in ((a, C.FUNC, "a"), (b, C.APPROX, "b"), (ab, C.EPS, "a * b")):
            mx = plain_axes([-0.6, 3.6, 1], [-0.8, 1.1, 1], 1.05, 1.3)
            mx.y_axis.set_stroke(opacity=0)  # the n = 0 stem stands where the y-axis would be
            st = VGroup(*[Line(mx.c2p(k_, 0), mx.c2p(k_, v_), color=col, stroke_width=5) for k_, v_ in enumerate(seq)])
            tag = MathTex(nm, font_size=22, color=col).move_to(mx.c2p(2.5, 0.8))
            assert all(tag.get_bottom()[1] > s_.get_top()[1] + 0.03 for s_ in st if abs(s_.get_x() - tag.get_x()) < tag.width / 2 + 0.05)
            minis.add(VGroup(mx, st, tag))
        minis.arrange(RIGHT, buff=0.22)
        pic = VGroup(VGroup(*[m_[0] for m_ in minis]), *[m_[1] for m_ in minis], VGroup(*[m_[2] for m_ in minis]))
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
        mdot = Dot(dx.c2p(zmax.real, zmax.imag), radius=0.06, color=WHITE)
        mtag = label(r"max", font_size=20, color=WHITE).next_to(mdot, RIGHT if zmax.real >= 0 else LEFT, buff=0.08)
        key = phase_key(0.22).next_to(dx, RIGHT, buff=0.35)
        pic = Group(dx, img, Circle(radius=dx.c2p(1, 0)[0] - dx.c2p(0, 0)[0], color=GREY_B, stroke_width=2).move_to(
            dx.c2p(0, 0)), mdot, mtag, key)
        out.add(panel([(r"A(\mathbb D): \ fg, \ \ f = 1 + \tfrac z2, \ g = 1 - \tfrac{z^2}{2}", WHITE)], pic,
                      rf"\|fg\| = {nFG:.3f} \le \|f\|\,\|g\| = {nF * nG:.2f}", (2.2, -1.05)))
        return out

    # ------------------------------------------------------------------
    def neumann(self):
        d = load("neumann")
        errs, bound = d["errs"], d["bound"]
        n = np.arange(40)
        # log10 of each norm against n; the n-axis runs along the bottom (y = -7), y = 0 is a thin guide
        ax = plain_axes([0, 40, 10], [-7, 1, 1], 6.2, 4.4, numbers=True, font_size=18,
                        x_axis_config={"include_numbers": False, "include_ticks": False},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0},
                                       "numbers_to_exclude": []}).move_to([-3.2, -0.3, 0])
        ax.x_axis.set_stroke(width=1, opacity=0.6)
        nax = NumberLine(x_range=[0, 40, 10], length=6.2, include_numbers=True, font_size=18, stroke_color=GREY_C,
                         numbers_to_exclude=[0], decimal_number_config={"num_decimal_places": 0})
        nax.shift(ax.c2p(0, -7) - nax.n2p(0))
        assert np.allclose(nax.n2p(40), ax.c2p(40, -7))
        xl = MathTex(r"n", font_size=22).next_to(nax, RIGHT, buff=0.12)
        yl = MathTex(r"\log_{10}\Big\|\sum_{k \le n} A^k - (I - A)^{-1}\Big\|", font_size=22).next_to(ax, UP, buff=0.1)
        bl = polyline_(ax, n, np.log10(bound), C.EPS)
        dots = VGroup(*[Dot(ax.c2p(k, math.log10(e)), radius=0.045, color=C.OPERATOR) for k, e in zip(n, errs)])
        bt = MathTex(r"\frac{0.8^{\,n+1}}{1 - 0.8}", font_size=26, color=C.EPS).next_to(
            ax.c2p(33, math.log10(bound[33])), UR, buff=0.12)
        assert np.all(errs <= bound * (1 + 1e-9))
        assert np.log10(errs).min() > -7 and np.log10(bound).max() < 1
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
            ax.c2p(24, 25 * math.log10(0.8)), UR, buff=0.1)

        def clear_of(lab_, xs, ys, pad=0.05):  # the curve through (xs, ys) stays out of the label's box
            for x_, y_ in zip(xs, ys):
                p_ = ax.c2p(x_, y_)
                if lab_.get_left()[0] - pad < p_[0] < lab_.get_right()[0] + pad:
                    assert not (lab_.get_bottom()[1] - pad < p_[1] < lab_.get_top()[1] + pad), (x_, y_)

        fine = np.linspace(0, 39, 400)
        clear_of(bt, fine, np.log10(0.8 ** (fine + 1) / 0.2))
        clear_of(bt, n, np.log10(errs))
        clear_of(pbl, fine, (fine + 1) * math.log10(0.8))
        clear_of(pbl, n, np.log10(pw))
        clear_of(pdl, n, np.log10(pw))
        yl0 = MathTex(r"\log_{10} \text{ of each norm}", font_size=22).next_to(ax, UP, buff=0.1)
        lad = VGroup(
            MathTex(r"(I - A)(I + A + \cdots + A^n) = I - A^{n+1}", font_size=30),
            MathTex(r"\|A^{n+1}\| \le \|A\|^{n+1} \to 0 \quad \text{if } \|A\| < 1", font_size=30),
            MathTex(r"(I - A)^{-1} = \sum_{n \ge 0} A^n", font_size=36, color=C.EPS),
            MathTex(r"\big\|(I - A)^{-1}\big\| \le \frac{1}{1 - \|A\|}", font_size=30, color=GREY_A),
            label(r"a random $6 \times 6$ complex $A$ with $\|A\| = 0.8$:", font_size=24),
            label(r"every error under the geometric bound", font_size=24, color=C.OPERATOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.6, -0.3, 0])
        assert lad.get_right()[0] <= 6.6 and max(r_.width for r_ in lad) <= 6.0
        head = label(r"The geometric series, \ for operators", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> The first tool is the oldest series there is. Multiply I minus A by one plus A "
            "plus up to A to the n, and everything telescopes to I minus A to the n plus one. "
            "<bookmark mark='b'/> If the norm of A is below one, that last term dies, so I minus A is invertible, "
            "and its inverse is the geometric series: the Neumann series. <bookmark mark='c'/> For a random matrix "
            "of norm 0.8, the partial sums close in on the inverse, always under the geometric bound."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(lad[0]), Create(ax), Create(nax), FadeIn(xl), FadeIn(yl0),
                      LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in pdots], lag_ratio=0.05), FadeIn(pdl), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(lad[1]), Create(pline), FadeIn(pbl))
            self.play(FadeIn(lad[2]), FadeIn(lad[3]))
            vo.wait_until("c")
            self.play(FadeIn(lad[4]), FadeOut(pdots), FadeOut(pdl), FadeOut(pbl), FadeOut(pline), FadeTransform(yl0, yl))
            self.play(Create(bl), FadeIn(bt))
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.05), FadeIn(lad[5]), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def open_set(self):
        # a slice through the 2 x 2 matrices: M(s, t) = [[1 + s, t], [t, 1 - s]], det = 1 - s^2 - t^2
        ax = square_axes([-2.2, 2.8, 1], [-2.2, 2.2, 1], 1.15).move_to([-3.3, -0.4, 0])
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
        rI = 1 / np.linalg.norm(np.linalg.inv(np.eye(2)), 2)
        assert abs(rI - 1) < 1e-12
        # the ball around I fills the singular circle: a tinted disc whose boundary is the red circle itself
        b1 = Circle(radius=unit * rI, stroke_width=0, fill_color=C.EPS, fill_opacity=0.16).move_to(ax.c2p(0, 0))
        b2 = Circle(radius=unit * rA, color=C.EPS, stroke_width=3, fill_color=C.EPS, fill_opacity=0.16).move_to(
            ax.c2p(1.6, 0))
        dI = Dot(ax.c2p(0, 0), radius=0.06, color=WHITE)
        dA = Dot(ax.c2p(1.6, 0), radius=0.06, color=WHITE)
        lI = MathTex(r"I", font_size=26).next_to(dI, DL, buff=0.08)
        lA = MathTex(r"A", font_size=26).next_to(dA, UP, buff=0.1)
        # the two radii, drawn and labelled
        aI, aA = 5 * PI / 6, -PI / 4
        rIl = Line(ax.c2p(0, 0), ax.c2p(rI * math.cos(aI), rI * math.sin(aI)), color=C.EPS, stroke_width=3)
        rAl = Line(ax.c2p(1.6, 0), ax.c2p(1.6 + rA * math.cos(aA), rA * math.sin(aA)), color=C.EPS, stroke_width=3)
        rIt = MathTex(r"1", font_size=26, color=C.EPS).move_to(rIl.get_center() + 0.22 * rotate_vector(
            normalize(rIl.get_vector()), -PI / 2))
        rAt = MathTex(f"{rA:.1f}", font_size=26, color=C.EPS).move_to(rAl.get_center() + 0.26 * rotate_vector(
            normalize(rAl.get_vector()), -PI / 2))
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
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        rows.next_to([0.3, -0.2, 0], RIGHT, buff=0)
        assert max(r_.width for r_ in rows) <= 6.0 and rows.get_right()[0] <= 6.6 and rows.get_left()[0] > img.get_right()[0]
        head = label(r"The invertible elements form an open set", font_size=34).to_edge(UP, buff=0.3)
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
            self.play(FadeIn(dI), FadeIn(lI), FadeIn(b1), Create(rIl), FadeIn(rIt), FadeIn(rows[:2]))
            self.bring_to_front(sing)
            self.play(FadeIn(dA), FadeIn(lA), DrawBorderThenFill(b2), Create(rAl), FadeIn(rAt))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:5]))
            self.play(FadeIn(rows[5]))
        self.wait(0.4)
        self.clear_scene()

def polyline_(ax, xs, ys, color, stroke_width=3):
    m = VMobject(color=color, stroke_width=stroke_width)
    m.set_points_as_corners([ax.c2p(float(a), float(b)) for a, b in zip(xs, ys)])
    return m
