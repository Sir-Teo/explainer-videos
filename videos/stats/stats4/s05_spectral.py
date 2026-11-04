from __future__ import annotations

import numpy as np

from videos.stats.stats4.common import *  # noqa: F403


class Spectral(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.ellipse()
        self.rayleigh()
        self.mahalanobis()
        self.power()

    def card(self):
        card = chapter_card(4, r"The spectral theorem", r"Every symmetric matrix is a stretch along perpendicular axes",
                            lit=(), part=PART)
        with self.voiceover("Chapter four. The spectral theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def theorem(self):
        th = theorem_card(r"The spectral theorem", r"a real symmetric matrix $A$ can be written $A = Q\Lambda Q^\top$, \ "
                          r"$Q$ orthogonal (its columns orthonormal eigenvectors), \ $\Lambda$ diagonal and real",
                          who=r"Cauchy (1829); \ Sylvester; \ Hilbert", color=EIG, width=7.8, font_size=24).to_edge(UP, buff=0.4)
        steps = VGroup(
            label(r"1. \ maximize $\mathbf u^\top A \mathbf u$ over unit vectors: \ a maximum exists (the sphere is compact)",
                  font_size=24),
            label(r"2. \ at the maximum, \ $A\mathbf u_1 = \lambda_1 \mathbf u_1$ \ (Lagrange multipliers)", font_size=24),
            label(r"3. \ $A$ maps $\mathbf u_1^\perp$ to itself: \ $\langle A\mathbf v, \mathbf u_1\rangle = \langle \mathbf v, "
                  r"A\mathbf u_1\rangle = 0$ \ (symmetry)", font_size=24),
            label(r"4. \ repeat inside $\mathbf u_1^\perp$, \ one dimension down", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(th, DOWN, buff=0.5)
        for s_ in steps:
            if s_.width > 12.6:
                s_.width = 12.6
        hdr = label(r"proof sketch", font_size=24, color=GREY_B).next_to(steps, UP, buff=0.15).align_to(steps, LEFT)
        with self.voiceover(
            "Symmetric matrices are everywhere in statistics: covariance matrices, projections, the matrices of "
            "quadratic forms. <bookmark mark='a'/> The spectral theorem says every real symmetric matrix is Q "
            "Lambda Q transpose: a rotation, a stretch along the axes by the eigenvalues, and the rotation back. "
            "<bookmark mark='b'/> Here's the idea of the proof. Look for the unit vector u that makes u transpose A "
            "u as large as possible; the unit sphere is compact, so it exists. <bookmark mark='c'/> At the maximum, "
            "Lagrange's condition says A u is a multiple of u: an eigenvector. <bookmark mark='d'/> Because A is "
            "symmetric, it maps the directions perpendicular to u into themselves. <bookmark mark='e'/> So repeat "
            "the argument there, one dimension down, until the eigenvectors fill the space, every one at right "
            "angles to the others."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(th, shift=DOWN * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(hdr), FadeIn(steps[0], shift=RIGHT * 0.2))
            for k, m in zip(range(1, 4), "cde"):
                vo.wait_until(m)
                self.play(FadeIn(steps[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def ellipse(self):
        d = load("spectral")
        x, y = np.asarray(d["x"]), np.asarray(d["y"])
        S_, ev, V, mu = np.asarray(d["S"]), np.asarray(d["eig"]), np.asarray(d["V"]), np.asarray(d["mean"])
        A = axes([145, 195], [140, 200], x_length=6.0, y_length=6.0 * 60 / 50 * 0.8, xlabel=r"mid-parent (cm)",
                 ylabel=r"child (cm)", xticks=[150, 170, 190], yticks=[150, 170, 190], center=[-3.4, -0.3, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.03, color=DATA, fill_opacity=0.7) for a, b in zip(x, y)])
        th = np.linspace(0, TAU, 200)
        ell_pts = []
        for c_ in (1.0, 2.0):
            pts = [mu + c_ * (np.sqrt(ev[0]) * np.cos(t) * V[:, 0] + np.sqrt(ev[1]) * np.sin(t) * V[:, 1]) for t in th]
            ell_pts.append(VMobject(stroke_color=EIG, stroke_width=2.5, stroke_opacity=0.9 if c_ == 1 else 0.5)
                           .set_points_smoothly([ax.c2p(*p) for p in pts]))
        axes_v = VGroup(*[Arrow(ax.c2p(*mu), ax.c2p(*(mu + 2 * np.sqrt(ev[k]) * V[:, k])), buff=0, color=EIG,
                                stroke_width=4, max_tip_length_to_length_ratio=0.12) for k in (0, 1)])
        info = VGroup(MathTex(r"\Sigma = " + mat_tex(S_, "{:.1f}"), font_size=32),
                      MathTex(rf"\lambda_1 = {ev[0]:.1f},\quad \lambda_2 = {ev[1]:.1f}", font_size=30, color=EIG),
                      MathTex(r"\{\mathbf x : (\mathbf x - \boldsymbol\mu)^\top \Sigma^{-1} (\mathbf x - \boldsymbol\mu) = c^2\}",
                              font_size=28),
                      label(r"axes along the eigenvectors, \ half-lengths $c\sqrt{\lambda_k}$", font_size=22, color=GREY_B))
        info.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 0.6, 0])
        pca = label(r"the long axis: \ the first principal component \ (Part 31)", font_size=24, color=S.ACCENT)
        pca.move_to([3.6, -2.4, 0])
        tag = simulated_tag(r"simulated: 400 of the World's families")
        with self.voiceover(
            "The theorem has a picture. <bookmark mark='a'/> Four hundred of the World's families: parents' average "
            "height against the child's. <bookmark mark='b'/> Their covariance matrix is two by two and symmetric. "
            "Its eigenvalues are about eighty-five and twenty. <bookmark mark='c'/> The quadratic form of its "
            "inverse traces ellipses around the mean. Their axes point along the eigenvectors, and their half-lengths "
            "are proportional to the square roots of the eigenvalues. <bookmark mark='d'/> The long axis is the "
            "direction in which the cloud spreads most: the first principal component, the subject of Part 31."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(dots, lag_ratio=0.005))
            vo.wait_until("b")
            self.play(FadeIn(info[:2]))
            vo.wait_until("c")
            self.play(Create(ell_pts[0]), Create(ell_pts[1]), FadeIn(info[2:]))
            self.play(GrowArrow(axes_v[0]), GrowArrow(axes_v[1]))
            vo.wait_until("d")
            self.play(Indicate(axes_v[0], color=S.ACCENT), FadeIn(pca))
        self.clear_scene()

    def rayleigh(self):
        d = load("spectral")
        th, rq = np.asarray(d["theta"]), np.asarray(d["rq"])
        ev = np.asarray(d["eig"])
        c0 = np.array([-4.2, -0.3, 0])
        R = 1.6
        circ = Circle(radius=R, stroke_color=GREY_C, stroke_width=1.5).move_to(c0)
        t = ValueTracker(0.0)
        u = always_redraw(lambda: Arrow(c0, c0 + R * np.array([np.cos(t.get_value()), np.sin(t.get_value()), 0]), buff=0,
                                        color=EIG, stroke_width=4))
        A = axes([0, np.pi], [0, 100], x_length=6.4, y_length=3.8, xlabel=r"direction of $\mathbf u$ (radians)",
                 ylabel=r"$\mathbf u^\top \Sigma\, \mathbf u$", xticks=[0, 1, 2, 3], yticks=[0, 20, 50, 85], center=[2.6, -0.6, 0])
        ax = A.ax
        trace_path = always_redraw(lambda: curve(ax, th[th <= t.get_value() + 1e-9], rq[th <= t.get_value() + 1e-9], EIG, 3)
                                   if t.get_value() > 0.02 else VectorizedPoint(ax.c2p(0, rq[0])))
        top = DashedLine(ax.c2p(0, ev[0]), ax.c2p(np.pi, ev[0]), color=FIT, stroke_width=2)
        bot = DashedLine(ax.c2p(0, ev[1]), ax.c2p(np.pi, ev[1]), color=FIT, stroke_width=2)
        f = MathTex(r"\lambda_{\min} \le \frac{\mathbf u^\top \Sigma \mathbf u}{\mathbf u^\top \mathbf u} \le \lambda_{\max}",
                    font_size=34).to_edge(UP, buff=0.5)
        sub = label(r"the Rayleigh quotient: \ the variance of the projection $\mathbf u^\top \mathbf x$", font_size=24,
                    color=GREY_B).next_to(f, DOWN, buff=0.2)
        with self.voiceover(
            "The proof's maximization has a statistical meaning. <bookmark mark='a'/> For a unit vector u, u "
            "transpose Sigma u is the variance of the data projected onto u. Turn u around the circle. "
            "<bookmark mark='b'/> The variance rises and falls, and its maximum is the largest eigenvalue, reached "
            "along the first eigenvector; its minimum is the smallest. <bookmark mark='c'/> This ratio is the "
            "Rayleigh quotient, and it always lies between the smallest and largest eigenvalues. Finding the "
            "direction of greatest variance is an eigenvalue problem: that's principal components."
        ) as vo:
            self.add(circ, u)
            self.play(FadeIn(A), Create(top), Create(bot), FadeIn(f), FadeIn(sub))
            vo.wait_until("a")
            self.add(trace_path)
            self.play(t.animate.set_value(np.pi), run_time=7.0, rate_func=linear)
            full = curve(ax, th, rq, EIG, 3)
            trace_path.clear_updaters()
            self.remove(trace_path)
            self.add(full)
            vo.wait_until("b")
            self.play(t.animate.set_value(d["th_max"]), run_time=2.0)
            self.play(FadeIn(Dot(ax.c2p(d["th_max"], d["rq_max"]), radius=0.08, color=FIT)))
            vo.wait_until("c")
            self.play(Indicate(top, color=FIT))
        u.clear_updaters()
        trace_path.clear_updaters()
        self.clear_scene()

    def mahalanobis(self):
        e = load("extras")["maha"]
        x, y = np.asarray(e["x"]), np.asarray(e["y"])
        white = np.asarray(e["white"])
        mu = np.asarray(e["mu"])
        io = e["i_odd"]
        A = axes([145, 195], [140, 200], x_length=5.0, y_length=4.8, xlabel=r"mid-parent (cm)", ylabel=r"child (cm)",
                 xticks=[150, 170, 190], yticks=[150, 170, 190], center=[-3.9, -0.3, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.028, color=DATA, fill_opacity=0.7) for a, b in zip(x, y)])
        odd = Circle(radius=0.14, stroke_color=RES, stroke_width=3).move_to(ax.c2p(x[io], y[io]))
        c1 = np.array([3.0, -0.3, 0])
        sc = 0.75
        frame = VGroup(Line(c1 + LEFT * 3, c1 + RIGHT * 3, color=GREY_D), Line(c1 + DOWN * 2.6, c1 + UP * 2.6, color=GREY_D))
        wdots = VGroup(*[Dot(c1 + sc * np.array([a, b, 0]), radius=0.028, color=DATA, fill_opacity=0.7) for a, b in white])
        wodd = Circle(radius=0.14, stroke_color=RES, stroke_width=3).move_to(c1 + sc * np.array([*white[io], 0]))
        ring = Circle(radius=sc * np.sqrt(e["chi2_95"]), stroke_color=EIG, stroke_width=2).move_to(c1)
        f = MathTex(r"d_M(\mathbf x)^2 = (\mathbf x - \boldsymbol\mu)^\top \Sigma^{-1} (\mathbf x - \boldsymbol\mu) = \|\Sigma^{-1/2}"
                    r"(\mathbf x - \boldsymbol\mu)\|^2", font_size=28).to_edge(UP, buff=0.3)
        arr = Arrow([-1.0, -0.3, 0], [0.0, -0.3, 0], color=GREY_B, stroke_width=3)
        al = MathTex(r"\Sigma^{-1/2}", font_size=28).next_to(arr, UP, buff=0.1)
        pdesc = "tall parents, short child" if x[io] > mu[0] else "short parents, tall child"
        info = label(rf"circled: \ not extreme in either coordinate, \ Mahalanobis distance {e['md_odd']:.1f}: \ {pdesc}",
                     font_size=22, color=RES).to_edge(DOWN, buff=0.35)
        ring_l = label(rf"$\chi^2_2$ 95\% circle: \ {100 * e['frac_out']:.1f}\% outside", font_size=22, color=EIG)
        ring_l.next_to(ring, DOWN, buff=0.1)
        tag = simulated_tag(corner=UR)
        with self.voiceover(
            "The ellipses give the right way to measure how unusual a point is. <bookmark mark='a'/> Distance from "
            "the centre, but measured in the ellipse's own units: the Mahalanobis distance, named for Prasanta "
            "Chandra Mahalanobis, founder of the Indian Statistical Institute. <bookmark mark='b'/> It's the "
            "ordinary distance after multiplying by Sigma to the minus a half, the inverse square root from the "
            "spectral theorem. That map whitens the data: <bookmark mark='c'/> the tilted ellipse becomes a round "
            "cloud with identity covariance. <bookmark mark='d'/> In the whitened picture, the circled family stands "
            f"out. Neither its parents' height nor its child's is far out on its own, but {pdesc} goes against the "
            "correlation, and the Mahalanobis distance sees it. <bookmark mark='e'/> For normal data the "
            "squared distance is chi-squared with two degrees of freedom, so the ninety-five percent circle should "
            f"leave about five percent outside; here it leaves {100 * e['frac_out']:.1f}."
        ) as vo:
            self.play(FadeIn(A), FadeIn(dots, lag_ratio=0.003), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(GrowArrow(arr), FadeIn(al))
            vo.wait_until("c")
            self.play(FadeIn(frame), TransformFromCopy(dots, wdots), run_time=2.5)
            vo.wait_until("d")
            self.play(Create(odd), Create(wodd), FadeIn(info))
            vo.wait_until("e")
            self.play(Create(ring), FadeIn(ring_l))
        self.clear_scene()

    def power(self):
        e = load("extras2")["power"]
        its = e["its"]
        c0 = np.array([-3.6, -0.6, 0])
        R = 2.2
        circ = Circle(radius=R, stroke_color=GREY_D, stroke_width=1.5).move_to(c0)
        vecs = VGroup(*[Arrow(c0, c0 + R * np.array([*it["v"], 0]), buff=0, stroke_width=3,
                              color=interpolate_color(ManimColor(GREY_B), ManimColor(EIG), min(1, k / 4)),
                              max_tip_length_to_length_ratio=0.12) for k, it in enumerate(its[:6])])
        v0 = Arrow(c0, c0 + R * RIGHT, buff=0, stroke_width=3, color=GREY_C)
        rows = VGroup(
            MathTex(r"\mathbf v_{k+1} = \frac{\Sigma\mathbf v_k}{\|\Sigma\mathbf v_k\|}", font_size=34),
            MathTex(r"\Sigma^k \mathbf v_0 = \sum_j c_j \lambda_j^k \mathbf q_j", r"\ \Rightarrow\ \text{the largest } \lambda \text{ wins}",
                    font_size=30),
            MathTex(rf"\text{{error shrinks by }} \lambda_2/\lambda_1 = {e['ratio']:.3f} \text{{ per step}}", font_size=28, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 1.8, 0])
        tbl = VGroup(*[MathTex(rf"k = {k + 1}:\ \ \mathbf v^\top\Sigma\mathbf v = {it['lam']:.4f}", font_size=24,
                               color=EIG if k > 3 else GREY_A) for k, it in enumerate(its[:6])])
        tbl.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.4, -1.4, 0])
        truth = MathTex(rf"\lambda_1 = {e['lam']:.4f}", font_size=26, color=EXACT).next_to(tbl, DOWN, buff=0.2)
        with self.voiceover(
            "How does a computer actually find eigenvectors? The simplest method is beautiful. "
            "<bookmark mark='a'/> Start with any vector, multiply by the matrix, and normalize; repeat. "
            "<bookmark mark='b'/> Written in the eigenvector basis, each multiplication scales every component by "
            "its eigenvalue, so after k steps the largest eigenvalue's component dominates. <bookmark mark='c'/> For "
            "the families' covariance, starting from the horizontal direction, the vector swings onto the long axis "
            "of the ellipse in a handful of steps, <bookmark mark='d'/> and the Rayleigh quotient locks onto the "
            "largest eigenvalue to four decimals. The error shrinks by the ratio of the two eigenvalues each step. "
            "Variants of this power iteration compute Google's PageRank and the principal components of huge data "
            "sets."
        ) as vo:
            self.play(Create(circ), GrowArrow(v0))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1:]))
            vo.wait_until("c")
            for k in range(6):
                self.play(GrowArrow(vecs[k]), FadeIn(tbl[k]), run_time=0.7)
            vo.wait_until("d")
            self.play(FadeIn(truth))
        self.clear_scene()
