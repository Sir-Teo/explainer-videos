from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import HIST, I_COLOR, J_COLOR, arrow, chapter, plane, rot


class Eigen(VoiceoverScene):
    def construct(self):
        chapter(self, 5, r"Directions that stay put", r"What does a matrix do to a direction?",
                "Chapter five. Eigenvectors, and the spectral theorem.")
        self.stay_put()
        self.symmetric()
        self.proof()
        self.rayleigh()
        self.pca()

    # ------------------------------------------------------------------
    def stay_put(self):
        A = np.array([[2.0, 1.0], [0.0, 1.0]])  # eigenvalues 2 (along (1, 0)) and 1 (along (1, -1))
        w, V = np.linalg.eig(A)
        assert np.allclose(sorted(w), [1.0, 2.0])
        pl = plane()
        fan = VGroup()
        for k in range(16):
            a = 2 * PI * k / 16
            fan.add(arrow([1.6 * math.cos(a), 1.6 * math.sin(a), 0], color=GREY_B, stroke_width=4))
        e1 = Line([-8, 0, 0], [8, 0, 0], color=C.BITS, stroke_width=4)
        e2 = Line([-6, 6, 0], [6, -6, 0], color=C.BITS, stroke_width=4)
        on = [0, 8, 6, 14]  # the fan's arrows that lie on the eigen-lines: angles 0, pi, -pi/4 and 3pi/4
        lam = VGroup(MathTex(r"\lambda = 2", font_size=40, color=C.BITS).move_to([5.5, 0.45, 0]),
                     MathTex(r"\lambda = 1", font_size=40, color=C.BITS).move_to([3.4, -2.6, 0]))
        for m in lam:
            m.add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.08)
        eq = MathTex(r"A\mathbf{v} = \lambda \mathbf{v}", font_size=50).to_corner(UL, buff=0.5)
        eq.add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.12)
        char = MathTex(r"\det(A - \lambda I) = (2-\lambda)(1-\lambda) = 0", font_size=34).next_to(eq, DOWN, buff=0.25,
                                                                                               aligned_edge=LEFT)
        char.add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.1)
        with self.voiceover(
            "Most vectors are knocked off their line by a matrix. <bookmark mark='a'/> Some aren't: they stay on their "
            "line, only stretched, shrunk or flipped. <bookmark mark='b'/> Those are the eigenvectors, and the scale is the "
            "eigenvalue. A minus lambda I must then squash a direction to zero, so its determinant vanishes: a "
            "polynomial equation for lambda."
        ) as vo:
            self.play(Create(pl, lag_ratio=0.05), LaggedStart(*[GrowArrow(a) for a in fan], lag_ratio=0.05), run_time=2)
            vo.wait_until("a")
            self.play(ApplyMatrix(A, VGroup(pl, fan)), run_time=2.5)
            self.play(Create(e1), Create(e2), *[fan[k].animate.set_color(C.BITS) for k in on])
            vo.wait_until("b")
            self.play(FadeIn(eq), FadeIn(lam))
            self.play(FadeIn(char))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def symmetric(self):
        S = np.array([[2.0, 1.0], [1.0, 2.0]])  # eigenvalues 3 along (1, 1), 1 along (1, -1)
        lam, Q = np.linalg.eigh(S)
        assert np.allclose(lam, [1.0, 3.0])
        pl = plane(faded=True)
        circ = Circle(radius=1.0, color=C.BITS, stroke_width=4)
        q1 = arrow([math.sqrt(0.5), math.sqrt(0.5), 0], color=I_COLOR)
        q2 = arrow([math.sqrt(0.5), -math.sqrt(0.5), 0], color=J_COLOR)
        g = VGroup(pl, circ, q1, q2)
        colors = {"A": WHITE, "Q": C.TRUE_P, r"\Lambda": C.BITS, r"Q^{\top}": C.TRUE_P}
        f = cmath("A", "=", "Q", r"\Lambda", r"Q^{\top}", colors=colors, font_size=56).to_corner(UL, buff=0.5)
        fb = BackgroundRectangle(f, color=BACKGROUND, fill_opacity=0.85, buff=0.12)
        sym = MathTex(r"A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix} = A^{\top}", font_size=40).to_corner(UR, buff=0.5)
        sb = BackgroundRectangle(sym, color=BACKGROUND, fill_opacity=0.85, buff=0.12)
        steps = [label(r"$Q^{\top}$: \ turn the eigenvectors onto the axes", font_size=30, color=C.TRUE_P),
                 label(r"$\Lambda$: \ stretch along each axis, by $3$ and by $1$", font_size=30, color=C.BITS),
                 label(r"$Q$: \ turn back", font_size=30, color=C.TRUE_P)]
        for st in steps:
            st.to_edge(DOWN, buff=0.5).add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.1)
        tr = MathTex(r"\begin{bmatrix} a & b \\ c & d \end{bmatrix}^{\top} = \begin{bmatrix} a & c \\ b & d \end{bmatrix}",
                     font_size=34)
        tr_card = gloss(r"transpose \ $Q^{\top}$", r"flip a matrix across its diagonal;\\ for a turn like $Q$, "
                        r"it is the same turn, undone", picture=tr, corner=DR, width=4.4, color=C.TRUE_P)
        Lm = np.diag(lam[::-1])  # 3 on the first axis, 1 on the second
        Qr = rot(-PI / 4)  # turns (1, 1) onto the x axis
        with self.voiceover(
            "Symmetric matrices, equal to their mirror image across the diagonal, behave best. <bookmark mark='a'/> "
            "Their eigenvalues are real, and we can choose an orthonormal eigenvector basis. <bookmark mark='b'/> So the map is: turn "
            "the eigenvectors onto the axes, stretch each axis by its eigenvalue, and turn back. <bookmark mark='c'/> A "
            "equals Q, Lambda, Q transpose; for a turn like Q, the transpose is the same turn, undone. That's the "
            "spectral theorem."
        ) as vo:
            self.play(FadeIn(pl), FadeIn(sb), FadeIn(sym), Create(circ))
            vo.wait_until("a")
            self.play(GrowArrow(q1), GrowArrow(q2))
            vo.wait_until("b")
            for k, M in enumerate([Qr, Lm, Qr.T]):
                self.play(FadeIn(steps[k]), run_time=0.4)
                self.play(ApplyMatrix(M, g), run_time=1.6)
                self.play(FadeOut(steps[k]), run_time=0.3)
            vo.wait_until("c")
            self.play(FadeIn(fb), Write(f))
            self.play(FadeIn(tr_card))
        assert np.allclose(Qr.T @ Lm @ Qr, S)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def proof(self):
        thm = theorem_card(r"the spectral theorem",
                           r"A real symmetric matrix has real eigenvalues and an orthonormal eigenvector basis: \ "
                           r"$A = Q\Lambda Q^{\top}$, \ with $Q$ orthogonal.",
                           who=r"Cauchy (1829), \ for quadratic forms; \ Hilbert (1904--10), \ in infinite dimensions",
                           width=6.6).to_corner(UL, buff=0.25)
        rows = [
            cmath(r"\lambda\,|\mathbf{v}|^2", "=", r"\bar{\mathbf{v}}^{\top}A\mathbf{v}", "=", r"\bar\lambda\,|\mathbf{v}|^2",
                  font_size=34),
            cmath(r"\lambda_1\,\mathbf{v}_2^{\top}\mathbf{v}_1", "=", r"\mathbf{v}_2^{\top}A\mathbf{v}_1", "=",
                  r"\lambda_2\,\mathbf{v}_2^{\top}\mathbf{v}_1", font_size=34),
            cmath(r"\mathbf{v}_1^{\top}(A\mathbf{x})", "=", r"(A\mathbf{v}_1)^{\top}\mathbf{x}", "=",
                  r"\lambda_1\,\mathbf{v}_1^{\top}\mathbf{x} = 0", font_size=34),
        ]
        whys = [why(r"the middle number is its own conjugate \\ ($A$ real, $A = A^{\top}$): \ $\lambda$ is real"),
                why(r"$A = A^{\top}$: \ if $\lambda_1 \ne \lambda_2$, \\ then $\mathbf{v}_1 \perp \mathbf{v}_2$"),
                why(r"$\mathbf{x} \perp \mathbf{v}_1$ stays $\perp \mathbf{v}_1$: \\ repeat inside that space "
                    r"(induction)")]
        step = ladder(self, rows, whys, keep=3, top=0.9, x=-1.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "Why does it always work? The proof has three steps. <bookmark mark='a'/> First, the eigenvalues are real: "
            "sandwich A between an eigenvector and its complex conjugate. Since A is real and symmetric, the middle "
            "number equals its own conjugate, so lambda equals lambda bar. <bookmark mark='b'/> Second, eigenvectors "
            "with different eigenvalues are perpendicular: move A across the dot product, and the eigenvalues must agree "
            "unless the dot product is zero. <bookmark mark='c'/> Third, A maps the space perpendicular to an "
            "eigenvector into itself, so repeat inside it: by induction, a full set. Cauchy proved the first part in "
            "1829; Hilbert took it to infinite dimensions."
        ) as vo:
            self.play(FadeIn(thm, shift=DOWN * 0.2))
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            step(2, transform=False)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rayleigh(self):
        S = np.array([[2.0, 1.0], [1.0, 2.0]])
        lam = np.linalg.eigvalsh(S)
        c = np.array([-4.0, -0.6, 0])
        k = 1.25
        circ = Circle(radius=k, color=GREY_B, stroke_width=2).move_to(c)
        q1 = Line(c - 3.2 * np.array([0.7071, 0.7071, 0]), c + 3.2 * np.array([0.7071, 0.7071, 0]), color=C.BITS,
                  stroke_width=2).set_opacity(0.6)
        q2 = Line(c - 2.4 * np.array([0.7071, -0.7071, 0]), c + 2.4 * np.array([0.7071, -0.7071, 0]), color=C.TRUE_P,
                  stroke_width=2).set_opacity(0.6)
        t = ValueTracker(0.0)

        def x():
            return np.array([math.cos(t.get_value()), math.sin(t.get_value())])

        def R(a):
            v = np.array([math.cos(a), math.sin(a)])
            return float(v @ S @ v)

        g = axes([0, 2 * PI, PI / 2], [0, 3.5, 1], x_length=6.0, y_length=3.4, yticks=[0, 1, 2, 3],
                 xlabel=r"direction of $\mathbf{x}$", ylabel=r"$R(\mathbf{x}) = \mathbf{x}^{\top}A\mathbf{x} \,/\, "
                 r"\mathbf{x}^{\top}\mathbf{x}$", center=[3.3, -0.9, 0])
        ax = g.ax
        xs = np.linspace(0, 2 * PI, 240)
        cv = curve(ax, xs, [R(a) for a in xs], C.BITS, 3)
        hi = DashedLine(ax.c2p(0, lam[1]), ax.c2p(2 * PI, lam[1]), color=C.BITS, stroke_width=1.5)
        lo = DashedLine(ax.c2p(0, lam[0]), ax.c2p(2 * PI, lam[0]), color=C.TRUE_P, stroke_width=1.5)
        hl = MathTex(rf"\lambda_1 = {lam[1]:.0f}", font_size=26, color=C.BITS).next_to(ax.c2p(PI / 4, lam[1]), UP, buff=0.08)
        ll = MathTex(rf"\lambda_2 = {lam[0]:.0f}", font_size=26, color=C.TRUE_P).next_to(ax.c2p(3 * PI / 4, lam[0]), DOWN, buff=0.08)
        xa = always_redraw(lambda: arrow(c + k * np.array([*x(), 0]), start=c, color=WHITE, stroke_width=5))
        dot = always_redraw(lambda: glow_dot(ax.c2p(t.get_value(), R(t.get_value())), color=C.BITS, radius=0.07,
                                             layers=3))
        rows = [cmath(r"R(\mathbf{x})", "=", r"\frac{\sum_i \lambda_i c_i^2}{\sum_i c_i^2}", font_size=36)]
        rows[0].to_corner(UL, buff=0.35).shift(RIGHT * 0.2)
        w0 = why(r"write $\mathbf{x} = \sum_i c_i \mathbf{q}_i$: \ a weighted average of the eigenvalues")
        w0.next_to(rows[0], RIGHT, buff=0.4)
        box = label(r"$\lambda_{\min} \le R(\mathbf{x}) \le \lambda_{\max}$, \ the maximum at the top eigenvector",
                    font_size=28, color=C.BITS).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "One number connects eigenvalues to what follows: the Rayleigh quotient, x transpose A x over x transpose "
            "x. <bookmark mark='a'/> In the eigenvector basis it is a weighted average of the eigenvalues. "
            "<bookmark mark='b'/> So as x turns, it stays between the smallest and the largest eigenvalue, reaching "
            "them along the eigenvectors. <bookmark mark='c'/> The top eigenvector answers a question: which direction "
            "does A favour most? It returns as principal components, power iteration and the SVD."
        ) as vo:
            self.play(Create(circ), Create(q1), Create(q2), FadeIn(g))
            self.add(xa)
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(w0))
            vo.wait_until("b")
            self.play(Create(hi), Create(lo), FadeIn(hl), FadeIn(ll))
            self.add(dot)
            self.play(Create(cv), t.animate.set_value(2 * PI), run_time=5.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(box))
        for m in (xa, dot):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pca(self):
        g = np.random.default_rng(4)
        C2 = np.array([[2.2, 1.3], [1.3, 1.1]])
        X = g.multivariate_normal([0, 0], C2, size=260)
        X -= X.mean(0)  # PCA projects deviations from the empirical mean.
        cov = np.cov(X.T)
        lam, Q = np.linalg.eigh(cov)
        top = Q[:, 1] * np.sign(Q[0, 1])
        dots = VGroup(*[Dot([x, y, 0], radius=0.045, color=C.TRUE_P, fill_opacity=0.8) for x, y in X])
        ell = Ellipse(width=2 * 2 * math.sqrt(lam[1]), height=2 * 2 * math.sqrt(lam[0]), color=C.BITS, stroke_width=3)
        ell.rotate(math.atan2(top[1], top[0]))
        pc1 = arrow([*(2 * math.sqrt(lam[1]) * top), 0], color=C.BITS)
        pc2 = arrow([*(2 * math.sqrt(lam[0]) * np.array([-top[1], top[0]])), 0], color=C.MODEL_Q)
        line = Line([*(-5.5 * top), 0], [*(5.5 * top), 0], color=C.BITS, stroke_width=2, stroke_opacity=0.6)
        proj = VGroup(*[Dot([*((p @ top) * top), 0], radius=0.045, color=C.TRUE_P) for p in X])
        tag = label(r"centred illustrative data", font_size=22, color=GREY_B).to_corner(DR, buff=0.4)
        head = label(r"covariance: \ symmetric; \ its eigenvectors: \ the \textit{principal components}", font_size=30)
        head.to_edge(UP, buff=0.4)
        cv = MathTex(r"\begin{bmatrix} " + rf"{cov[0, 0]:.2f} & {cov[0, 1]:.2f} \\ {cov[1, 0]:.2f} & {cov[1, 1]:.2f}"
                     + r" \end{bmatrix}", font_size=34)
        cv_note = VGroup(label(r"diagonal: \ how much $x$, and $y$, vary", font_size=20, color=GREY_A),
                         label(r"off the diagonal: \ how much they rise and fall together", font_size=20,
                               color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        cov_card = gloss(r"covariance matrix", r"a table of how the data spreads out", picture=VGroup(cv, cv_note).arrange(
            DOWN, buff=0.15), corner=UL, width=4.6, color=C.BITS)
        cov_card.shift(DOWN * 0.7)
        with self.voiceover(
            "Covariance matrices describe how data spreads: <bookmark mark='c'/> how much each coordinate varies, on "
            "the diagonal, and how much pairs vary together, off it. The spread along a unit direction is the "
            "covariance's Rayleigh quotient, so the direction of greatest spread is the top eigenvector. "
            "<bookmark mark='a'/> These are the principal components, Pearson's in 1901 and Hotelling's in 1933. "
            "<bookmark mark='b'/> Keeping the top few is how we drew GPT-2's words in three dimensions."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.004), FadeIn(tag),
                      run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(cov_card))
            vo.wait_until("a")
            self.play(Create(ell), GrowArrow(pc1), GrowArrow(pc2))
            vo.wait_until("b")
            self.play(Create(line), FadeOut(pc2), FadeOut(cov_card))
            self.play(*[ReplacementTransform(d, p) for d, p in zip(dots, proj)], run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
