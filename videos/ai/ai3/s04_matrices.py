from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import HIST, I_COLOR, J_COLOR, arrow, chapter, mat2, plane


class Matrices(VoiceoverScene):
    def construct(self):
        chapter(self, 3, r"Matrices move space", r"What does a matrix do?", "Chapter three. Matrices move space.")
        self.moving()
        self.columns()
        self.composition()
        self.determinant()
        self.rank()

    # ------------------------------------------------------------------
    def moving(self):
        bg = plane(faded=True).set_opacity(0.25)
        pl = plane()
        S = np.array([[1.0, 1.0], [0.0, 1.0]])
        A = np.array([[1.5, -0.5], [0.5, 1.0]])
        with self.voiceover(
            "A matrix moves every vector at once. <bookmark mark='a'/> It keeps the origin where it is, and keeps "
            "grid lines straight, parallel, and evenly spaced: it's a linear map. <bookmark mark='b'/> Watch the "
            "whole plane move."
        ) as vo:
            self.add(bg)
            self.play(Create(pl, lag_ratio=0.05), run_time=1.5)
            vo.wait_until("a")
            self.play(ApplyMatrix(S, pl), run_time=2.0)
            self.play(ApplyMatrix(np.linalg.inv(S), pl), run_time=1.2)
            vo.wait_until("b")
            self.play(ApplyMatrix(A, pl), run_time=2.5)
            self.play(ApplyMatrix(np.linalg.inv(A), pl), run_time=1.2)
        self.bg, self.pl = bg, pl

    # ------------------------------------------------------------------
    def columns(self):
        pl = self.pl
        M = np.array([[2.0, -1.0], [1.0, 1.0]])
        i_hat, j_hat = arrow(RIGHT, color=I_COLOR), arrow(UP, color=J_COLOR)
        li = MathTex(r"\hat\imath", font_size=40, color=I_COLOR).next_to(RIGHT, DOWN, buff=0.12)
        lj = MathTex(r"\hat\jmath", font_size=40, color=J_COLOR).next_to(UP, LEFT, buff=0.12)
        m = mat2(M, font_size=46).to_corner(UL, buff=0.5)
        mbg = BackgroundRectangle(m, color=BACKGROUND, fill_opacity=0.85, buff=0.15)
        x, y = 1.0, 2.0
        v = arrow([x, y, 0], color=C.BITS)
        lv = MathTex(r"\begin{bmatrix} 1 \\ 2 \end{bmatrix}", font_size=36, color=C.BITS).next_to([x, y, 0], RIGHT, buff=0.12)
        Mi = M[:, 0]
        img = M @ np.array([x, y])
        part1 = arrow([*(x * Mi), 0], color=I_COLOR, stroke_width=5)
        part2 = arrow([*img, 0], start=[*(x * Mi), 0], color=J_COLOR, stroke_width=5)
        eq = MathTex(r"\begin{bmatrix} 2 & -1 \\ 1 & 1 \end{bmatrix} \begin{bmatrix} 1 \\ 2 \end{bmatrix} = 1"
                     r"\begin{bmatrix} 2 \\ 1 \end{bmatrix} + 2 \begin{bmatrix} -1 \\ 1 \end{bmatrix} = "
                     r"\begin{bmatrix} 0 \\ 3 \end{bmatrix}", font_size=36).to_corner(DL, buff=0.4)
        ebg = BackgroundRectangle(eq, color=BACKGROUND, fill_opacity=0.9, buff=0.12)
        with self.voiceover(
            "Where does each vector go? <bookmark mark='a'/> Only two arrows decide it: where the two basis arrows "
            "land. Those landing spots are the columns of the matrix. <bookmark mark='b'/> A vector with coordinates "
            "one and two lands at one times the first column, plus two times the second. That's what multiplying "
            "a matrix by a vector means."
        ) as vo:
            self.play(GrowArrow(i_hat), GrowArrow(j_hat), FadeIn(li), FadeIn(lj), GrowArrow(v), FadeIn(lv))
            vo.wait_until("a")
            self.play(ApplyMatrix(M, VGroup(pl, i_hat, j_hat, v)), FadeOut(li), FadeOut(lj), FadeOut(lv), run_time=2.5)
            self.play(FadeIn(mbg), Write(m))
            self.play(Indicate(m.get_columns()[0], color=I_COLOR), Indicate(i_hat, color=WHITE),
                      Indicate(m.get_columns()[1], color=J_COLOR), Indicate(j_hat, color=WHITE))
            vo.wait_until("b")
            self.play(GrowArrow(part1))
            self.play(GrowArrow(part2))
            self.play(FadeIn(ebg), Write(eq))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def composition(self):
        R = np.array([[0.0, -1.0], [1.0, 0.0]])  # a quarter turn
        S = np.array([[1.0, 1.0], [0.0, 1.0]])  # a shear
        panels = []
        for k, (first, second, txt) in enumerate([(R, S, r"turn, then shear"), (S, R, r"shear, then turn")]):
            pl = plane(x_range=(-4, 4), y_range=(-4, 4)).scale(0.42)
            sq = Square(side_length=1.0, stroke_width=0, fill_color=C.BITS, fill_opacity=0.6).move_to([0.5, 0.5, 0])
            sq.scale(0.42, about_point=ORIGIN)
            ih = arrow(RIGHT * 0.42, color=I_COLOR, stroke_width=4)
            jh = arrow(UP * 0.42, color=J_COLOR, stroke_width=4)
            g = VGroup(pl, sq, ih, jh).move_to([-3.5 + 7 * k, -0.4, 0])
            t = label(txt, font_size=30).next_to(g, UP, buff=0.2)
            panels.append((g, t, first, second))
        prod = MathTex(r"S\,R \ne R\,S", font_size=44).to_edge(DOWN, buff=0.4)
        hist = history_card(1858, r"Arthur Cayley, \textit{A Memoir on the Theory of Matrices}",
                            r"matrices as objects that add and multiply, \ and whose products depend on the order; "
                            r"the word \textit{matrix} was J.~J.~Sylvester's, in 1850", color=HIST, width=5.6)
        hist.to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "One map after another is again a map, and its matrix is the product of the two. <bookmark mark='a'/> "
            "But the order matters: turning, then shearing, is not shearing, then turning. <bookmark mark='b'/> "
            "Arthur Cayley made matrices objects in their own right in 1858, with exactly this rule; his friend James "
            "Joseph Sylvester had named them eight years before."
        ) as vo:
            for g, t, _, _ in panels:
                self.play(FadeIn(g), FadeIn(t), run_time=0.6)
            vo.wait_until("a")
            for step in (2, 3):
                anims = []
                for g, t, first, second in panels:
                    M = first if step == 2 else second
                    c = g[0].get_center()
                    anims.append(ApplyMatrix(M, g[1:], about_point=c))
                    anims.append(ApplyMatrix(M, g[0], about_point=c))
                self.play(*anims, run_time=1.8)
            self.play(Write(prod))
            vo.wait_until("b")
            self.play(FadeOut(prod), FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def determinant(self):
        pl = plane(faded=True).set_opacity(0.3)
        t = ValueTracker(0.0)
        A0, A1 = np.array([[1.0, 0.0], [0.0, 1.0]]), np.array([[2.0, 1.0], [0.5, 1.5]])
        flat = np.array([[2.0, 1.0], [1.0, 0.5]])  # determinant 0
        flip = np.array([[1.5, 1.5], [1.2, 0.3]])  # determinant < 0

        def M():
            v = t.get_value()
            if v <= 1:
                return (1 - v) * A0 + v * A1
            if v <= 2:
                return (2 - v) * A1 + (v - 1) * flat
            return (3 - v) * flat + (v - 2) * flip

        def shape():
            m = M()
            pts = [ORIGIN, [*m[:, 0], 0], [*(m[:, 0] + m[:, 1]), 0], [*m[:, 1], 0]]
            det = float(np.linalg.det(m))
            col = C.BITS if det > 0.02 else (C.PENALTY if det < -0.02 else GREY_B)
            return VGroup(Polygon(*pts, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.45),
                          arrow(pts[1], color=I_COLOR, stroke_width=5), arrow(pts[3], color=J_COLOR, stroke_width=5))

        sh = always_redraw(shape)
        dl = MathTex(r"\det =", font_size=46)
        dv = DecimalNumber(1.0, num_decimal_places=2, font_size=46, include_sign=True)
        read = VGroup(dl, dv).arrange(RIGHT, buff=0.2).to_corner(UL, buff=0.6)
        dv.add_updater(lambda m: m.set_value(float(np.linalg.det(M()))))
        rbg = BackgroundRectangle(read, color=BACKGROUND, fill_opacity=0.85, buff=0.15)
        notes = [label(r"area $= |\det|$", font_size=32, color=C.BITS),
                 label(r"$\det = 0$: \ squashed onto a line", font_size=32, color=GREY_A),
                 label(r"$\det < 0$: \ flipped over", font_size=32, color=C.PENALTY)]
        for n_ in notes:
            n_.to_corner(DL, buff=0.6).add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.1)
        with self.voiceover(
            "One number says how much a map stretches area: the determinant. <bookmark mark='a'/> The unit square "
            "becomes a parallelogram, and the determinant is its area. <bookmark mark='b'/> When the determinant "
            "reaches zero, the whole plane is squashed onto a line, and information is lost for good. "
            "<bookmark mark='c'/> Below zero, the plane has been flipped over, like a page turned face down."
        ) as vo:
            self.add(pl, sh, rbg, read)
            vo.wait_until("a")
            self.play(t.animate.set_value(1.0), run_time=2.0)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(t.animate.set_value(2.0), FadeOut(notes[0]), run_time=2.2)
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(t.animate.set_value(3.0), FadeOut(notes[1]), run_time=2.2)
            self.play(FadeIn(notes[2]))
        sh.clear_updaters()
        dv.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rank(self):
        flat = np.array([[2.0, 1.0], [1.0, 0.5]])  # rank one: both columns on the line through (2, 1)
        bg = plane(faded=True).set_opacity(0.25)
        pl = plane()
        null = Line([-2.2, 4.4, 0], [2.2, -4.4, 0], color=C.PENALTY, stroke_width=6)  # the direction (1, -2)
        col = Line([-8, -4, 0], [8, 4, 0], color=C.BITS, stroke_width=6)
        f = mat2(flat, font_size=42).to_corner(UL, buff=0.5)
        fb = BackgroundRectangle(f, color=BACKGROUND, fill_opacity=0.85, buff=0.12)
        cards = VGroup(
            label(r"column space: \ where the plane lands \ (a line: \ \textbf{rank} $1$)", font_size=28, color=C.BITS),
            label(r"null space: \ what is sent to $\mathbf{0}$ \ (a line: \ dimension $1$)", font_size=28,
                  color=C.PENALTY),
            label(r"rank $+$ null-space dimension $=$ number of columns", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(DR, buff=0.4)
        for c_ in cards:
            c_.add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.08)
        with self.voiceover(
            "That squashing has a name, and it will matter for the rest of this part. <bookmark mark='a'/> This "
            "matrix sends the whole plane onto one line: its columns point the same way. <bookmark mark='b'/> The "
            "line where everything lands is the column space, and its dimension is the rank, here one. "
            "<bookmark mark='c'/> A whole line of vectors lands on zero: the null space. <bookmark mark='d'/> The "
            "dimensions always add up: rank plus the null space's dimension is the number of columns. A matrix of "
            "low rank is a big table that carries few independent directions."
        ) as vo:
            self.add(bg)
            self.play(Create(pl, lag_ratio=0.05), FadeIn(fb), Write(f), Create(null), run_time=1.5)
            vo.wait_until("a")
            self.play(ApplyMatrix(flat, VGroup(pl, null)), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(col), FadeIn(cards[0]))
            vo.wait_until("c")
            ghost = Line([-2.2, 4.4, 0], [2.2, -4.4, 0], color=C.PENALTY, stroke_width=4).set_opacity(0.6)
            self.play(Create(ghost), FadeIn(cards[1]))
            self.play(Transform(ghost, Dot(ORIGIN, color=C.PENALTY, radius=0.12)), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(cards[2]))
        self.wait(0.3)
        self.clear_scene()
