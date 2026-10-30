from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import HIST, I_COLOR, J_COLOR, SIG, UC, VC, arrow, chapter, load, plane

A = np.array([[1.4, 1.1], [-0.5, 0.9]])


def svd2(M):
    """U, singular values, V^T with U and V both rotations (det +1); M must have det > 0."""
    U, s, Vt = np.linalg.svd(M)
    if np.linalg.det(U) < 0:
        U[:, 1] *= -1
        Vt[1, :] *= -1
    assert np.linalg.det(U) > 0 and np.linalg.det(Vt) > 0 and np.allclose(U @ np.diag(s) @ Vt, M)
    return U, s, Vt


class SVD(VoiceoverScene):
    def construct(self):
        chapter(self, 7, r"Every matrix: turn, stretch, turn", r"What does any matrix do?",
                "Chapter seven. The singular value decomposition.")
        self.three_moves()
        self.derive()
        self.norm()

    # ------------------------------------------------------------------
    def three_moves(self):
        U, s, Vt = svd2(A)
        pl = plane(faded=True)
        circ = Circle(radius=1.0, color=C.BITS, stroke_width=4)
        v1, v2 = Vt[0], Vt[1]
        a1 = arrow([*v1, 0], color=I_COLOR)
        a2 = arrow([*v2, 0], color=J_COLOR)
        g = VGroup(pl, circ, a1, a2)
        colors = {"A": WHITE, "U": C.TRUE_P, r"\Sigma": C.BITS, r"V^{\top}": C.MODEL_Q}
        f = cmath("A", "=", "U", r"\Sigma", r"V^{\top}", colors=colors, font_size=56).to_corner(UL, buff=0.5)
        fb = BackgroundRectangle(f, color=BACKGROUND, fill_opacity=0.85, buff=0.12)
        steps = [label(r"$V^{\top}$: \ turn", font_size=32, color=C.MODEL_Q),
                 label(rf"$\Sigma$: \ stretch the axes, by ${s[0]:.2f}$ and ${s[1]:.2f}$", font_size=32, color=C.BITS),
                 label(r"$U$: \ turn again", font_size=32, color=C.TRUE_P)]
        for st in steps:
            st.to_edge(DOWN, buff=0.5).add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.1)
        ghost = Circle(radius=1.0, color=WHITE, stroke_width=2).apply_matrix(A)
        ghost = DashedVMobject(ghost, num_dashes=40)
        once = label(r"$A$ in one go: \ the same ellipse", font_size=30, color=GREY_A).to_edge(DOWN, buff=0.5)
        once.add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.1)
        with self.voiceover(
            "Not every matrix is symmetric. Many aren't even square. <bookmark mark='a'/> But every matrix, without "
            "exception, does three things: a turn, then a stretch along the axes, then another turn. "
            "<bookmark mark='b'/> That's the singular value decomposition: A equals U, Sigma, V transpose."
        ) as vo:
            self.play(FadeIn(pl), Create(circ), GrowArrow(a1), GrowArrow(a2))
            vo.wait_until("a")
            for k, M in enumerate([Vt, np.diag(s), U]):
                self.play(FadeIn(steps[k]), run_time=0.4)
                self.play(ApplyMatrix(M, g), run_time=1.6)
                self.play(FadeOut(steps[k]), run_time=0.3)
            self.play(Create(ghost), FadeIn(once))
            vo.wait_until("b")
            self.play(FadeIn(fb), Write(f))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        U, s, Vt = svd2(A)
        colors = {r"\mathbf{v}_i": VC, r"\mathbf{v}_j": VC, r"\mathbf{u}_i": UC, r"\sigma_i": SIG, r"\sigma_i^2": SIG,
                  "U": UC, r"V^{\top}": VC, r"\Sigma": SIG, "V": VC}
        rows = [
            cmath(r"\mathbf{x}^{\top}A^{\top}A\,\mathbf{x}", "=", r"|A\mathbf{x}|^2 \ge 0", font_size=34, colors=colors),
            cmath(r"A^{\top}A\,\mathbf{v}_i", "=", r"\sigma_i^2\,\mathbf{v}_i", font_size=34, colors=colors),
            cmath(r"\mathbf{u}_i", "=", r"A\mathbf{v}_i \,/\, \sigma_i", font_size=34, colors=colors),
            cmath(r"\mathbf{u}_i^{\top}\mathbf{u}_j", "=", r"\frac{\mathbf{v}_i^{\top}A^{\top}A\,\mathbf{v}_j}{\sigma_i\sigma_j}"
                  r" = \frac{\sigma_j^2\,\mathbf{v}_i^{\top}\mathbf{v}_j}{\sigma_i\sigma_j} = \delta_{ij}", font_size=34,
                  colors=colors),
            cmath(r"AV = U\Sigma", r"\;\Rightarrow\;", "A = ", "U", r"\Sigma", r"V^{\top}", font_size=38, colors=colors),
        ]
        whys = [why(r"$A^{\top}A$ is symmetric, \ never negative"), why(r"the spectral theorem: \\ perpendicular "
                                                                         r"$\mathbf{v}_i$, \ $\sigma_i^2 \ge 0$"),
                why(r"define, \ for $\sigma_i > 0$"), why(r"the $\mathbf{u}_i$ are perpendicular too"),
                why(r"$V$ orthogonal: \ $V^{-1} = V^{\top}$")]
        step = ladder(self, rows, whys, keep=5, top=3.3, x=-1.4, buff=0.34, edge=6.9)
        hist = history_card(1873, r"E.~Beltrami (1873), \ C.~Jordan (1874)",
                            r"found it independently; \ E.~Schmidt (1907) took it to infinite dimensions; \ G.~Golub "
                            r"and W.~Kahan (1965) gave the algorithm computers still use", color=HIST, width=6.2)
        hist.to_corner(DL, buff=0.25)
        # the picture the algebra describes: perpendicular v's in, perpendicular stretched u's out
        cc, ce, r = np.array([2.2, -2.75, 0]), np.array([5.3, -2.75, 0]), 0.62
        pic = VGroup(Circle(radius=r, color=GREY_B, stroke_width=2).move_to(cc),
                     arrow(cc + r * np.array([*Vt[0], 0]), start=cc, color=VC, stroke_width=4),
                     arrow(cc + r * np.array([*Vt[1], 0]), start=cc, color=VC, stroke_width=4),
                     MathTex(r"\xrightarrow{\;A\;}", font_size=34).move_to((cc + ce) / 2),
                     Circle(radius=r, color=SIG, stroke_width=3).apply_matrix(A).move_to(ce),
                     arrow(ce + r * s[0] * np.array([*U[:, 0], 0]), start=ce, color=UC, stroke_width=4),
                     arrow(ce + r * s[1] * np.array([*U[:, 1], 0]), start=ce, color=UC, stroke_width=4))
        pl = VGroup(MathTex(r"\mathbf{v}_1, \mathbf{v}_2", font_size=26, color=VC).next_to(pic[0], DOWN, buff=0.08),
                    MathTex(r"\sigma_1\mathbf{u}_1, \sigma_2\mathbf{u}_2", font_size=26, color=UC).next_to(pic[4], DOWN, buff=0.08))
        with self.voiceover(
            "Where do the turns and stretches come from? From the last chapter. <bookmark mark='a'/> A transpose A "
            "is symmetric, and never negative: x transpose A transpose A x is a length squared. "
            "<bookmark mark='b'/> So the spectral theorem gives it perpendicular eigenvectors v, with eigenvalues "
            "that are squares: call them sigma squared. <bookmark mark='c'/> Send each v through A, and divide by "
            "sigma. <bookmark mark='d'/> These new vectors u are perpendicular too, and of length one: the "
            "calculation is a line. <bookmark mark='e'/> So A sends the perpendicular v's to the perpendicular u's, "
            "stretched by the sigmas, and that is the decomposition. <bookmark mark='f'/> Eugenio Beltrami and "
            "Camille Jordan found it independently in 1873 and 1874; Gene Golub and William Kahan gave the "
            "algorithm, in 1965, that computers still use."
        ) as vo:
            self.play(FadeIn(pic), FadeIn(pl))
            for k_, mk in enumerate("abcde"):
                vo.wait_until(mk)
                step(k_)
            vo.wait_until("f")
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def norm(self):
        U, s, Vt = svd2(A)
        c = np.array([-3.6, -0.3, 0])
        k = 1.35  # drawn 1.35 times life size
        circ = Circle(radius=k, color=GREY_B, stroke_width=2).move_to(c)
        ell = Circle(radius=k, color=C.BITS, stroke_width=4).apply_matrix(A).shift(c)
        e1, e2 = [*(k * s[0] * U[:, 0]), 0], [*(k * s[1] * U[:, 1]), 0]
        if e1[0] < 0:  # label the end of the long axis that faces the middle of the screen
            e1 = [-v for v in e1]
        if e2[1] > 0:  # and the bottom end of the short axis
            e2 = [-v for v in e2]
        ax1 = DashedLine(c - e1, c + e1, color=C.BITS, stroke_width=2)
        ax2 = DashedLine(c - e2, c + e2, color=C.BITS, stroke_width=2)
        l1 = MathTex(rf"\sigma_1 = {s[0]:.2f}", font_size=36, color=C.BITS).move_to(c + 1.38 * np.array(e1) + UP * 0.25)
        l2 = MathTex(rf"\sigma_2 = {s[1]:.2f}", font_size=36, color=C.BITS).move_to(c + 1.55 * np.array(e2))
        for m in (l1, l2):
            m.add_background_rectangle(color=BACKGROUND, opacity=0.8, buff=0.06)
        t = ValueTracker(0.0)

        def x():
            return np.array([math.cos(t.get_value()), math.sin(t.get_value())])

        ax = Axes(x_range=[0, 2 * PI, PI / 2], y_range=[0, 2, 0.5], x_length=6.0, y_length=3.6, tips=False,
                          axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([3.6, -0.3, 0])
        xs = np.linspace(0, 2 * PI, 200)
        curve = ax.plot_line_graph(xs, [np.linalg.norm(A @ np.array([math.cos(a), math.sin(a)])) for a in xs],
                                   add_vertex_dots=False, line_color=C.BITS, stroke_width=3)
        top = DashedLine(ax.c2p(0, s[0]), ax.c2p(2 * PI, s[0]), color=WHITE, stroke_width=2)
        top_l = MathTex(r"\sigma_1", font_size=32).next_to(ax.c2p(2 * PI, s[0]), RIGHT, buff=0.1)
        yl = label(r"$|A\mathbf{x}|$ for every direction $\mathbf{x}$", font_size=26, color=GREY_A).next_to(ax, UP, buff=0.2)
        xa = always_redraw(lambda: arrow(c + k * np.array([*x(), 0]), start=c, color=GREY_A, stroke_width=4))
        ya = always_redraw(lambda: arrow(c + k * np.array([*(A @ x()), 0]), start=c, color=C.BITS, stroke_width=5))
        dot = always_redraw(lambda: glow_dot(ax.c2p(t.get_value() % (2 * PI), float(np.linalg.norm(A @ x()))), color=C.BITS,
                                             radius=0.07, layers=3))
        name = label(r"the spectral norm: \ $\|A\| = \sigma_1$, \ the most $A$ can stretch", font_size=30, color=WHITE)
        name.to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The stretches are the singular values. <bookmark mark='a'/> The unit circle always becomes an ellipse, "
            "and the singular values are its half-axes. <bookmark mark='b'/> Sweep a unit vector all the way "
            "around, and watch how long its image is. The longest it ever gets is sigma one: the most the matrix can "
            "stretch any vector. It's called the spectral norm."
        ) as vo:
            self.play(Create(circ), Create(ell))
            vo.wait_until("a")
            self.play(Create(ax1), Create(ax2), FadeIn(l1), FadeIn(l2))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(yl), Create(curve), Create(top), FadeIn(top_l))
            self.add(xa, ya, dot)
            self.play(t.animate.set_value(2 * PI), run_time=4.0, rate_func=linear)
            self.play(FadeIn(name))
        for m in (xa, ya, dot):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
