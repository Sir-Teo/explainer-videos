from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import I_COLOR, J_COLOR, arrow, plane


def rot(a):
    return np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])


class Eigen(VoiceoverScene):
    def construct(self):
        self.card()
        self.stay_put()
        self.symmetric()
        self.pca()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(4, r"Directions that stay put", r"What does a matrix do to a direction?", part=3)
        with self.voiceover("Chapter four. Eigenvectors."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

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
        with self.voiceover(
            "Most vectors are knocked off their line by a matrix. <bookmark mark='a'/> But some aren't: they stay on "
            "their own line, and are only stretched or shrunk. <bookmark mark='b'/> Those are the eigenvectors, and "
            "the stretch factor is the eigenvalue."
        ) as vo:
            self.play(Create(pl, lag_ratio=0.05), LaggedStart(*[GrowArrow(a) for a in fan], lag_ratio=0.05), run_time=2)
            vo.wait_until("a")
            self.play(ApplyMatrix(A, VGroup(pl, fan)), run_time=2.5)
            self.play(Create(e1), Create(e2), *[fan[k].animate.set_color(C.BITS) for k in on])
            vo.wait_until("b")
            self.play(FadeIn(eq), FadeIn(lam))
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
            "Symmetric matrices, the ones that equal their own mirror image across the diagonal, behave best of "
            "all. <bookmark mark='a'/> Their eigenvalues are real numbers, and their eigenvectors are perpendicular. "
            "<bookmark mark='b'/> So the map is: turn, so the eigenvectors line up with the axes; stretch along each "
            "axis by its eigenvalue; and turn back. <bookmark mark='c'/> A equals Q, Lambda, Q transpose. The "
            "transpose flips a matrix across its diagonal, and for a turn like Q, that's the same turn, undone. "
            "That's the spectral theorem."
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
    def pca(self):
        g = np.random.default_rng(4)
        C2 = np.array([[2.2, 1.3], [1.3, 1.1]])
        X = g.multivariate_normal([0, 0], C2, size=260)
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
        tag = label(r"illustrative data", font_size=22, color=GREY_B).to_corner(DR, buff=0.4)
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
            "Covariance matrices describe how data spreads out: <bookmark mark='c'/> a table of how much each "
            "coordinate varies, on the diagonal, and how much each pair rises and falls together, off it. They are "
            "symmetric, and their eigenvectors point along the directions in which the data spreads the most. "
            "<bookmark mark='a'/> These are the principal components. <bookmark mark='b'/> Keeping only the top few, and dropping the rest, is how we drew GPT-2's "
            "768-dimensional words in three dimensions at the start of this part."
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
