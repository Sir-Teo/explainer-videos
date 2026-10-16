from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai2.common import I_COLOR, J_COLOR, arrow, load, plane

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
        self.card()
        self.three_moves()
        self.norm()
        self.depth()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(5, r"Every matrix: turn, stretch, turn", r"What does any matrix do?", part=2)
        with self.voiceover("Chapter five. The singular value decomposition."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

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

    # ------------------------------------------------------------------
    def depth(self):
        d = load("depth")
        L = int(d["layers"])
        assert d["gains"] == [0.8, 1.0, 1.2]
        lens = {g: np.asarray(d[f"len{g}"]) for g in d["gains"]}
        assert lens[1.2][-1] > 1500 and lens[0.8][-1] < 2e-3 and 0.5 < lens[1.0][-1] < 3
        ax = Axes(x_range=[0, L, 10], y_range=[-14, 12, 2], x_length=9.5, y_length=5.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to(DOWN * 0.4 + LEFT * 1.0)
        xl = VGroup(*[MathTex(str(v), font_size=24, color=GREY_B).next_to(ax.c2p(v, -14), DOWN, buff=0.12)
                      for v in range(0, L + 1, 10)])
        yl = VGroup(*[MathTex(t, font_size=24, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.12)
                      for t, v in (("2^{-12}", -12), ("2^{-6}", -6), ("1", 0), ("2^{6}", 6), ("2^{12}", 12))])
        xn = label(r"layer", font_size=26, color=GREY_A).next_to(ax, DOWN, buff=0.5)
        yn = label(r"the vector's length", font_size=26, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        cols = {0.8: C.PENALTY, 1.0: WHITE, 1.2: C.BITS}
        lines, tags = VGroup(), VGroup()
        for gain in d["gains"]:
            ys = np.log2(np.maximum(lens[gain], 1e-12))
            ln = ax.plot_line_graph(np.arange(L + 1), ys, add_vertex_dots=False, line_color=cols[gain], stroke_width=4)
            lines.add(ln)
            end = lens[gain][-1]
            txt = rf"\times {end:.4f}" if end < 0.01 else (rf"\times {end:.1f}" if end < 100 else rf"\times {end:,.0f}")
            tags.add(MathTex(rf"\text{{gain }} {gain:g}: \ " + txt.replace(",", "{,}"), font_size=30, color=cols[gain])
                     .next_to(ax.c2p(L, float(ys[-1])), RIGHT, buff=0.15))
        head = label(r"A vector through $40$ layers of random matrices", font_size=34).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Why care how much a matrix stretches? <bookmark mark='a'/> A deep network applies one matrix after "
            "another. Push a vector through forty layers of random matrices. <bookmark mark='b'/> If each layer "
            "stretches a typical vector by 1.2, after forty layers its length has grown two thousand times. "
            "<bookmark mark='c'/> At 0.8, it shrinks to almost nothing. Only near one does the signal survive. That "
            "knife edge is the subject of part eight."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(xn), FadeIn(yn))
            self.play(Create(lines[1]), run_time=1.5)
            self.play(FadeIn(tags[1]))
            vo.wait_until("b")
            self.play(Create(lines[2]), run_time=2.0)
            self.play(FadeIn(tags[2]))
            vo.wait_until("c")
            self.play(Create(lines[0]), run_time=2.0)
            self.play(FadeIn(tags[0]))
        self.wait(0.5)
        self.clear_scene()
