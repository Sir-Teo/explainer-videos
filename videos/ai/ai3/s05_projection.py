from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import HIST, VA, VB, arrow, chapter, dots_on, ex, load, plane

ERRC = C.PENALTY
PC = C.BITS
CGS, MGS, HH = C.PENALTY, C.MODEL_Q, C.REWARD


def right_angle(corner, d1, d2, size=0.22, color=WHITE):
    d1, d2 = np.asarray(d1, float), np.asarray(d2, float)
    d1, d2 = d1 / np.linalg.norm(d1) * size, d2 / np.linalg.norm(d2) * size
    c = np.asarray(corner, float)
    return VMobject(color=color, stroke_width=2).set_points_as_corners([c + d1, c + d1 + d2, c + d2])


class Projection(VoiceoverScene):
    def construct(self):
        chapter(self, 4, r"Projection and least squares", r"What is the closest point in a subspace?",
                "Chapter four. Projections, and the closest point.")
        self.line()
        self.subspace()
        self.fit()
        self.gram_schmidt()
        self.stability()

    # ------------------------------------------------------------------
    def line(self):
        o = np.array([-6.2, -2.6, 0])
        a = np.array([4.6, 1.5, 0])
        b = np.array([2.2, 3.4, 0])
        ua = a / np.linalg.norm(a)
        p = (b @ ua) * ua
        ln = Line(o - 0.3 * a, o + 1.15 * a, color=GREY_C, stroke_width=2)
        aa, ab = arrow(o + a, start=o, color=VA), arrow(o + b, start=o, color=VB)
        ap = arrow(o + p, start=o, color=PC, stroke_width=7)
        e = DashedLine(o + p, o + b, color=ERRC, stroke_width=4)
        ra = right_angle(o + p, -ua, b - p)
        la = MathTex(r"\mathbf{a}", font_size=40, color=VA).next_to(o + a, DOWN, buff=0.15)
        lb = MathTex(r"\mathbf{b}", font_size=40, color=VB).next_to(o + b, UP, buff=0.1)
        lp = MathTex(r"\mathbf{p}", font_size=40, color=PC).next_to(o + p, DOWN, buff=0.2)
        le = MathTex(r"\mathbf{e}", font_size=40, color=ERRC).next_to(o + (p + b) / 2, RIGHT, buff=0.12)
        colors = {r"\mathbf{a}": VA, r"\mathbf{b}": VB, r"\mathbf{p}": PC, r"\hat x": PC, r"\mathbf{a}^{\top}": VA}
        rows = [
            cmath(r"\mathbf{p}", "=", r"\hat x\, \mathbf{a}", font_size=38, colors=colors),
            cmath(r"\mathbf{a}^{\top}", r"(\mathbf{b} - \hat x\,\mathbf{a})", "=", "0", font_size=38, colors=colors),
            cmath(r"\hat x", "=", r"\frac{\mathbf{a}^{\top}\mathbf{b}}{\mathbf{a}^{\top}\mathbf{a}}", font_size=38,
                  colors=colors),
            cmath(r"\mathbf{p}", "=", r"\frac{\mathbf{a}\,\mathbf{a}^{\top}}{\mathbf{a}^{\top}\mathbf{a}}\,\mathbf{b}",
                  font_size=38, colors=colors),
        ]
        whys = [why(r"the closest point lies on the line"), why(r"the error is perpendicular to $\mathbf{a}$"),
                why(r"solve for $\hat x$"), why(r"a matrix, \ $P = \mathbf{a}\mathbf{a}^{\top}/\mathbf{a}^{\top}\mathbf{a}$")]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=2.4, buff=0.38, edge=6.9)
        with self.voiceover(
            "In chapter one, the dot product measured a shadow. Here is the shadow made exact. <bookmark mark='a'/> "
            "Which point on the line through a is closest to b? <bookmark mark='b'/> It is some multiple of a. "
            "<bookmark mark='c'/> And it is the one whose error, b minus that point, is perpendicular to the line: "
            "any other point is farther, by Pythagoras. <bookmark mark='d'/> Solve for the multiple. "
            "<bookmark mark='e'/> The projection is a matrix times b: a times a transpose, over a dot a. A matrix of "
            "rank one, that finds shadows."
        ) as vo:
            self.play(Create(ln), GrowArrow(aa), FadeIn(la))
            vo.wait_until("a")
            self.play(GrowArrow(ab), FadeIn(lb))
            vo.wait_until("b")
            step(0)
            self.play(GrowArrow(ap), FadeIn(lp))
            vo.wait_until("c")
            self.play(Create(e), FadeIn(le), Create(ra))
            step(1)
            vo.wait_until("d")
            step(2)
            vo.wait_until("e")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def subspace(self):
        # a schematic plane in perspective (the column space), b above it, p its shadow
        c0 = np.array([-3.0, -1.9, 0])
        u, v = np.array([2.7, 0.4, 0]), np.array([1.1, 1.2, 0])
        sheet = Polygon(c0 - u - v, c0 + u - v, c0 + u + v, c0 - u + v, stroke_color=GREY_B, stroke_width=2,
                        fill_color=C.TRUE_P, fill_opacity=0.15)
        p = c0 + 0.35 * u + 0.25 * v
        b = p + np.array([0, 2.6, 0])
        ap = arrow(p, start=c0, color=PC)
        ab = arrow(b, start=c0, color=VB)
        e = DashedLine(p, b, color=ERRC, stroke_width=4)
        ra = right_angle(p, -u, UP)
        lab = VGroup(MathTex(r"\mathbf{b}", font_size=38, color=VB).next_to(b, UP, buff=0.1),
                     MathTex(r"\mathbf{p} = A\hat{\mathbf{x}}", font_size=34, color=PC).next_to(p, DOWN + RIGHT, buff=0.1),
                     MathTex(r"\mathbf{e}", font_size=38, color=ERRC).next_to((p + b) / 2, RIGHT, buff=0.1),
                     label(r"the columns of $A$ \\ span this plane", font_size=22, color=GREY_A).move_to(c0 - u * 0.45 - v * 0.6))
        tag = note(r"schematic").to_corner(DL, buff=0.25)
        colors = {r"\mathbf{b}": VB, r"\hat{\mathbf{x}}": PC, "P": PC}
        rows = [
            cmath(r"A^{\top}(\mathbf{b} - A\hat{\mathbf{x}})", "=", r"\mathbf{0}", font_size=36, colors=colors),
            cmath(r"A^{\top}A\,\hat{\mathbf{x}}", "=", r"A^{\top}\mathbf{b}", font_size=36, colors=colors),
            cmath(r"\hat{\mathbf{x}}", "=", r"(A^{\top}A)^{-1}A^{\top}\mathbf{b}", font_size=36, colors=colors),
            cmath("P", "=", r"A\,(A^{\top}A)^{-1}A^{\top}", font_size=40, colors=colors),
            cmath(r"P^2 = P", ",", r"\quad P^{\top} = P", font_size=36, colors=colors),
        ]
        whys = [why(r"$\mathbf{e}$ is perpendicular \\ to every column"), why(r"the normal equations"),
                why(r"independent columns: \\ $A^{\top}A$ is invertible"), why(r"$\mathbf{p} = A\hat{\mathbf{x}}$"),
                why(r"projecting twice \\ changes nothing")]
        step = ladder(self, rows, whys, keep=5, top=3.3, x=2.3, buff=0.3, edge=6.9)
        hist = history_card(1805, r"Legendre (1805), \ Gauss (1809)",
                            r"least squares, \ to fit orbits to observations; \ Gauss had used it to find the "
                            r"lost asteroid Ceres in 1801", color=HIST, width=5.0).to_corner(UL, buff=0.25)
        with self.voiceover(
            "Now project onto a whole plane, or any subspace: everything you can reach by combining the columns of a "
            "matrix A. <bookmark mark='a'/> The closest point is A times some x hat, and again the error is "
            "perpendicular, now to every column at once. <bookmark mark='b'/> Multiply out: the normal equations. "
            "<bookmark mark='c'/> If the columns are independent, A transpose A can be inverted. "
            "<bookmark mark='d'/> And the projection matrix is A, A transpose A inverse, A transpose. "
            "<bookmark mark='e'/> Project twice and nothing more happens; and P is symmetric. <bookmark mark='f'/> "
            "Legendre published this in 1805 as the method of least squares, and Gauss in 1809, who had used it to "
            "find the lost asteroid Ceres."
        ) as vo:
            self.play(FadeIn(sheet), FadeIn(lab[3]), FadeIn(tag), GrowArrow(ab), FadeIn(lab[0]))
            vo.wait_until("a")
            self.play(GrowArrow(ap), FadeIn(lab[1]), Create(e), FadeIn(lab[2]), Create(ra))
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
            vo.wait_until("f")
            self.play(FadeIn(hist, shift=DOWN * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fit(self):
        g = np.random.default_rng(1805)  # illustrative points
        x = np.sort(g.uniform(0.5, 9.5, 14))
        y = 0.9 + 0.55 * x + g.normal(0, 0.8, len(x))
        A = np.stack([np.ones_like(x), x], 1)
        c = np.linalg.solve(A.T @ A, A.T @ y)
        e = y - A @ c
        ax = Axes(x_range=[0, 10, 2], y_range=[0, 8, 2], x_length=7.0, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-2.4, -0.6, 0])
        pts = dots_on(ax, x, y, VB, radius=0.07)
        line = ax.plot(lambda t: c[0] + c[1] * t, x_range=[0, 10], color=PC, stroke_width=4)
        res = VGroup(*[Line(ax.c2p(a, b), ax.c2p(a, c[0] + c[1] * a), color=ERRC, stroke_width=3) for a, b in zip(x, y)])
        model = MathTex(r"y \approx c_0 + c_1 x", font_size=36).to_corner(UR, buff=0.5).shift(LEFT * 0.4)
        cols = MathTex(r"A = \begin{bmatrix} 1 & x_1 \\ \vdots & \vdots \\ 1 & x_{14} \end{bmatrix}", font_size=32)
        cols.next_to(model, DOWN, buff=0.35)
        checks = VGroup(MathTex(rf"\textstyle\sum e_i = {abs(e.sum()):.0e}".replace("e-", r"\times 10^{-") + "}"
                                if abs(e.sum()) > 0 else r"\textstyle\sum e_i = 0", font_size=30, color=ERRC),
                        MathTex(rf"\textstyle\sum x_i e_i = {abs((x * e).sum()):.0e}".replace("e-", r"\times 10^{-") + "}"
                                if abs((x * e).sum()) > 0 else r"\textstyle\sum x_i e_i = 0", font_size=30, color=ERRC))
        checks.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(cols, DOWN, buff=0.4)
        chk = label(r"the error is perpendicular \\ to both columns \\ (zero, up to rounding)", font_size=24,
                    color=GREY_A).next_to(checks, DOWN, buff=0.2)
        tag = note(r"illustrative data").to_corner(DL, buff=0.25)
        with self.voiceover(
            "This is the most used calculation in all of statistics. <bookmark mark='a'/> Fourteen points, and a "
            "line to fit them. The columns of A are a column of ones and the x values; the best line is the "
            "projection of the y values onto the plane those columns span. <bookmark mark='b'/> The leftover errors "
            "are perpendicular to both columns: they sum to zero, and so do the errors times x. "
            "<bookmark mark='c'/> Regression, a linear probe reading a concept out of a network, a network's last "
            "layer trained with squared error: all of them are this projection."
        ) as vo:
            self.play(Create(ax), FadeIn(tag), LaggedStart(*[FadeIn(d, scale=0.5) for d in pts], lag_ratio=0.05))
            vo.wait_until("a")
            self.play(Write(model), FadeIn(cols))
            self.play(Create(line))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(r) for r in res], lag_ratio=0.05))
            self.play(FadeIn(checks), FadeIn(chk))
            vo.wait_until("c")
            self.play(Indicate(line, color=WHITE))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gram_schmidt(self):
        o = np.array([-4.2, -1.6, 0])
        a1, a2 = np.array([2.6, 0.9, 0]), np.array([1.4, 2.4, 0])
        q1 = a1 / np.linalg.norm(a1)
        w = a2 - (a2 @ q1) * q1
        q2 = w / np.linalg.norm(w)
        s = 1.6  # unit vectors drawn 1.6 long
        A1, A2 = arrow(o + a1, start=o, color=VA), arrow(o + a2, start=o, color=VB)
        Q1 = arrow(o + s * q1, start=o, color=C.REWARD, stroke_width=8)
        sh = arrow(o + (a2 @ q1) * q1, start=o, color=PC, stroke_width=5)
        W = arrow(o + w, start=o, color=C.ADVANTAGE)
        Q2 = arrow(o + s * q2, start=o, color=C.REWARD, stroke_width=8)
        drop = DashedLine(o + a2, o + (a2 @ q1) * q1, color=GREY_B)
        labs = [MathTex(r"\mathbf{a}_1", font_size=36, color=VA).next_to(o + a1, RIGHT, buff=0.1),
                MathTex(r"\mathbf{a}_2", font_size=36, color=VB).next_to(o + a2, UP, buff=0.1),
                MathTex(r"\mathbf{q}_1", font_size=36, color=C.REWARD).next_to(o + s * q1, DOWN, buff=0.15),
                MathTex(r"\mathbf{q}_2", font_size=36, color=C.REWARD).next_to(o + s * q2, LEFT, buff=0.15)]
        colors = {r"\mathbf{q}_1": C.REWARD, r"\mathbf{q}_2": C.REWARD, r"\mathbf{a}_1": VA, r"\mathbf{a}_2": VB}
        rows = [
            cmath(r"\mathbf{q}_1", "=", r"\mathbf{a}_1 / |\mathbf{a}_1|", font_size=36, colors=colors),
            cmath(r"\mathbf{w}", "=", r"\mathbf{a}_2 - (\mathbf{q}_1^{\top}\mathbf{a}_2)\,\mathbf{q}_1", font_size=36,
                  colors=colors),
            cmath(r"\mathbf{q}_2", "=", r"\mathbf{w} / |\mathbf{w}|", font_size=36, colors=colors),
            cmath(r"A", "=", r"QR, \quad P = QQ^{\top}", font_size=38, colors=colors),
        ]
        whys = [why(r"normalize"), why(r"remove the shadow on $\mathbf{q}_1$"), why(r"normalize"),
                why(r"$R$ triangular: \\ the coefficients")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=2.6, buff=0.38, edge=6.9)
        hist = note(r"J.~P.~Gram (1883), \ E.~Schmidt (1907); \ Laplace had used it in 1812").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Projections are easiest when the basis is orthonormal: perpendicular arrows of length one. Then the "
            "projection is just Q times Q transpose. <bookmark mark='a'/> Gram and Schmidt's recipe makes one from "
            "any basis. Take the first vector and scale it to length one. <bookmark mark='b'/> From the second, "
            "remove its shadow on the first; what is left is perpendicular. <bookmark mark='c'/> Scale it to length "
            "one, and repeat for as many vectors as you have. <bookmark mark='d'/> Keeping the coefficients writes "
            "A as Q times a triangular R: the QR factorization."
        ) as vo:
            self.play(GrowArrow(A1), GrowArrow(A2), FadeIn(labs[0]), FadeIn(labs[1]))
            vo.wait_until("a")
            step(0)
            self.play(GrowArrow(Q1), FadeIn(labs[2]))
            vo.wait_until("b")
            step(1)
            self.play(Create(drop), GrowArrow(sh))
            self.play(TransformFromCopy(A2, W))
            vo.wait_until("c")
            step(2)
            self.play(Transform(W, Q2), FadeIn(labs[3]), FadeOut(sh), FadeOut(drop))
            vo.wait_until("d")
            step(3)
            self.play(FadeIn(hist))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stability(self):
        d = load("project")
        rows = d["rows"]
        lk = np.log10([r["kappa"] for r in rows])
        eps = float(d["eps"])

        def ly(v):
            return float(np.log10(max(v, 1e-17)))

        def panel(cx, title, series):
            g = axes([0, 17, 4], [-17, 2, 4], x_length=5.4, y_length=3.6, xticks=[0, 4, 8, 12, 16],
                     yticks=[-16, -12, -8, -4, 0], xfmt=lambda v: f"10^{{{int(v)}}}", yfmt=lambda v: f"10^{{{int(v)}}}",
                     xlabel=r"condition number $\kappa(A)$", ylabel=title, center=[cx, -0.5, 0])
            ax = g.ax
            curves = VGroup()
            for key, col in series:
                ys = [ly(r[key]) for r in rows]
                curves.add(VGroup(curve(ax, lk, ys, col, 3), dots_on(ax, lk, ys, col, radius=0.045)))
            return g, curves

        g1, c1 = panel(-3.4, r"loss of orthogonality \ $\|Q^{\top}Q - I\|$",
                       [("cgs", CGS), ("mgs", MGS), ("householder", HH)])
        g2, c2 = panel(3.4, r"error in the least-squares answer", [("err_normal", CGS), ("err_qr", HH)])
        lg1 = legend([(CGS, r"classical Gram--Schmidt"), (MGS, r"modified Gram--Schmidt"),
                      (HH, r"Householder reflections (1958)")], font_size=20).next_to(g1, DOWN, buff=0.15)
        lg2 = legend([(CGS, r"normal equations $A^{\top}A\hat{\mathbf{x}} = A^{\top}\mathbf{b}$"),
                      (HH, r"QR")], font_size=20).next_to(g2, DOWN, buff=0.15)
        head = label(r"In floating point, \ the order of operations matters", font_size=36).to_edge(UP, buff=0.3)
        cap = note(r"computed: \ the first $n$ columns of a $2n \times 2n$ Hilbert matrix, \ $n = 2, \dots, 14$",
                   font_size=20).to_corner(DR, buff=0.15)
        last = rows[-1]
        mid = next(r for r in rows if r["kappa"] > 1e6)
        dead = (" By the end, its vectors are not perpendicular at all." if last["cgs"] > 0.5 else "")
        worst = (" against an error bigger than the answer itself for the normal equations."
                 if last["err_normal"] > 1 else f" against ten to the minus {-ex(last['err_normal'])} for the normal "
                 "equations.")
        with self.voiceover(
            "On paper the recipe is exact. On a computer every step rounds, and the rounding can pile up. We tested "
            "it on Hilbert matrices, which get nearly dependent columns fast. <bookmark mark='a'/> The classical "
            "recipe, which takes every shadow from the original vector, loses orthogonality as the square of the "
            f"condition number: at a condition number of ten to the {ex(mid['kappa'])}, its Q is off by about ten to "
            f"the minus {-ex(mid['cgs'])}.{dead} <bookmark mark='b'/> Taking each shadow from the updated vector, the "
            "modified recipe, loses only in proportion to the condition number. <bookmark mark='c'/> Alston "
            "Householder's reflections, from 1958, stay perpendicular to about ten to the minus "
            f"{-ex(last['householder'])}, the machine's precision, whatever the matrix. <bookmark mark='d'/> The "
            "normal equations have the same flaw as the classical recipe: forming A transpose A squares the condition "
            "number, and the answer's error grows with that square. QR does not: at the hardest case, an error of "
            f"ten to the minus {-ex(last['err_qr'])},{worst} This is why libraries solve least squares with QR."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g1), FadeIn(g2), FadeIn(cap))
            vo.wait_until("a")
            self.play(Create(c1[0]), FadeIn(lg1[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(c1[1]), FadeIn(lg1[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(c1[2]), FadeIn(lg1[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(c2[0]), Create(c2[1]), FadeIn(lg2), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
