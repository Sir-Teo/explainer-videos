from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis4.common import load, mapped_grid, square_axes


def ellipse_pts(M, n=361):
    th = np.linspace(0, 2 * np.pi, n)
    return np.c_[np.cos(th), np.sin(th)] @ np.asarray(M).T


class LinearMaps(VoiceoverScene):
    def construct(self):
        self.card()
        self.grid()
        self.norm()
        self.open_set()
        self.neumann()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(1, r"Linear maps and their norms", r"How much can a matrix stretch a vector?", lit=(),
                            part=4)
        with self.voiceover("Chapter one: linear maps, the raw material of derivatives in many variables."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def grid(self):
        d = load("linmaps")
        A = d["A"]
        ax = square_axes([-4.8, 4.8, 1], [-3.0, 3.0, 1], 0.72).move_to([-2.9, -0.55, 0])
        ax.set_opacity(0.6)
        base = mapped_grid(ax, lambda P: P, (-2, 2), (-1.5, 1.5), n=9, color=GREY_D, stroke_width=1.2)
        img = mapped_grid(ax, lambda P: P @ A.T, (-2, 2), (-1.5, 1.5), n=9, color=C.OPERATOR, stroke_width=2.0)
        corners = np.array([[2, 1.5], [-2, 1.5], [2, -1.5], [-2, -1.5]]) @ A.T
        assert np.all(np.abs(corners[:, 0]) <= 4.8) and np.all(np.abs(corners[:, 1]) <= 3.0)
        e1 = Arrow(ax.c2p(0, 0), ax.c2p(1, 0), buff=0, color=C.SEQ, stroke_width=5, tip_length=0.18)
        e2 = Arrow(ax.c2p(0, 0), ax.c2p(0, 1), buff=0, color=C.APPROX, stroke_width=5, tip_length=0.18)
        Ae1 = Arrow(ax.c2p(0, 0), ax.c2p(*A[:, 0]), buff=0, color=C.SEQ, stroke_width=5, tip_length=0.18)
        Ae2 = Arrow(ax.c2p(0, 0), ax.c2p(*A[:, 1]), buff=0, color=C.APPROX, stroke_width=5, tip_length=0.18)
        mat = MathTex(r"A = \begin{pmatrix} 1.6 & 0.9 \\ 0.3 & 1.1 \end{pmatrix}", font_size=36).move_to([4.4, 1.4, 0])
        mat[0][2:5].set_color(C.SEQ)
        side = VGroup(
            label(r"\textbf{Rudin 9.6} \ $A(x + y) = Ax + Ay$, \ $A(cx) = cAx$", font_size=24),
            label(r"lines go to lines, \ evenly spaced stay evenly spaced,", font_size=24, color=GREY_A),
            label(r"and $0$ stays put", font_size=24, color=GREY_A),
            label(r"the columns are $Ae_1$ and $Ae_2$", font_size=24, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.2, -0.6, 0])
        for r_ in side:
            if r_.width > 5.4:
                r_.width = 5.4
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.2, -0.6, 0])
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.2, -0.6, 0])
        assert np.allclose(np.array([[1.6, 0.9], [0.3, 1.1]]), A)
        with self.voiceover(
            "<bookmark mark='a'/> A linear map of the plane respects addition and scaling. Watch what it does to a "
            "square grid: <bookmark mark='b'/> lines go to lines, equally spaced lines stay equally spaced, and the "
            "origin stays put. <bookmark mark='c'/> It's determined by where it sends the two unit vectors, and those "
            "images are the columns of its matrix."
        ) as vo:
            self.play(Create(base), FadeIn(e1), FadeIn(e2), FadeIn(mat))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(TransformFromCopy(base, img), Transform(e1, Ae1), Transform(e2, Ae2), run_time=2.5)
            self.play(FadeIn(side[1:3]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), Indicate(mat, color=C.EPS))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def norm(self):
        d = load("linmaps")
        A, s = d["A"], d["s"]
        U, S, Vt = np.linalg.svd(A)
        ax = square_axes([-2.6, 2.6, 1], [-2.1, 2.1, 1], 1.15).move_to([-3.2, -0.55, 0])
        ax.set_opacity(0.6)
        circ = VMobject(color=GREY_B, stroke_width=2.5).set_points_as_corners([ax.c2p(*p) for p in ellipse_pts(np.eye(2))])
        ell = VMobject(color=C.OPERATOR, stroke_width=3.5).set_points_as_corners([ax.c2p(*p) for p in ellipse_pts(A)])
        tT = ValueTracker(0.0)

        def vecs():
            t = tT.get_value()
            x = np.array([math.cos(t), math.sin(t)])
            return VGroup(Arrow(ax.c2p(0, 0), ax.c2p(*x), buff=0, color=GREY_A, stroke_width=4, tip_length=0.15),
                          Arrow(ax.c2p(0, 0), ax.c2p(*(A @ x)), buff=0, color=C.OPERATOR, stroke_width=5,
                                tip_length=0.18))

        vv = always_redraw(vecs)
        E = ellipse_pts(A, 721)

        def trace():
            k = int(np.clip(tT.get_value() / (2 * math.pi), 0, 1) * 720)
            if k < 2:
                return VMobject()
            return VMobject(color=C.OPERATOR, stroke_width=3.5).set_points_as_corners([ax.c2p(*p) for p in E[:k + 1]])

        tr = always_redraw(trace)
        rd = always_redraw(lambda: MathTex(
            rf"|Ax| = {np.linalg.norm(A @ np.array([math.cos(tT.get_value()), math.sin(tT.get_value())])):.3f}",
            font_size=32, color=C.OPERATOR).move_to([3.0, 2.0, 0]))
        t_max = math.atan2(Vt[0, 1], Vt[0, 0])
        assert abs(np.linalg.norm(A @ Vt[0]) - s[0]) < 1e-9
        axes_ = VGroup(DashedLine(ax.c2p(0, 0), ax.c2p(*(s[0] * U[:, 0])), color=C.EPS, stroke_width=3),
                       DashedLine(ax.c2p(0, 0), ax.c2p(*(s[1] * U[:, 1])), color=C.CONNECTED_SET, stroke_width=3))
        side = VGroup(
            MathTex(r"\|A\| = \sup_{|x| \le 1} |Ax|", font_size=36),
            label(r"\textbf{Rudin 9.6}: \ the largest stretch", font_size=24, color=GREY_A),
            MathTex(rf"\|A\| = {s[0]:.4f}", r",\quad \min_{|x| = 1}|Ax| = " + f"{s[1]:.4f}", font_size=30),
            label(r"the unit circle's image is an ellipse:", font_size=24, color=GREY_A),
            label(r"$\|A\|$ is its longest semi-axis", font_size=24, color=GREY_A),
            MathTex(r"\|A\| \le \Big(\sum a_{ij}^2\Big)^{1/2} = " + f"{math.sqrt((A**2).sum()):.4f}", font_size=28),
            MathTex(r"\|A + B\| \le \|A\| + \|B\|, \quad \|BA\| \le \|B\|\,\|A\|", font_size=28),
            label(r"(9.7): \ the linear maps form a metric space", font_size=24, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, -0.6, 0])
        side[2][0].set_color(C.EPS)
        side[2][1].set_color(C.CONNECTED_SET)
        for r_ in side:
            if r_.width > 6.2:
                r_.width = 6.2
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, -0.75, 0])
        assert np.linalg.norm(A, 2) <= math.sqrt((A**2).sum())
        with self.voiceover(
            "<bookmark mark='a'/> How big is a linear map? Rudin measures it by the largest stretch: the norm of A is "
            "the supremum of the length of A x over unit vectors x. <bookmark mark='b'/> Run a unit vector around the "
            "circle and watch its image: the length of A x rises and falls. <bookmark mark='c'/> The images trace an "
            "ellipse, and the norm is its longest semi-axis, here about 2.03; the shortest is about 0.73. "
            "<bookmark mark='d'/> The norm is at most the square root of the sum of the squared entries, and it "
            "behaves like a length: the triangle inequality holds, and the norm of a product is at most the product "
            "of the norms. So the linear maps form a metric space of their own."
        ) as vo:
            self.play(Create(ax), Create(circ))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(vv), FadeIn(rd))
            self.add(tr)
            self.play(tT.animate.set_value(2 * math.pi), run_time=6.0, rate_func=linear)
            tr.clear_updaters()
            self.remove(tr)
            self.add(ell)
            vo.wait_until("c")
            self.play(tT.animate.set_value(2 * math.pi + (t_max % math.pi)), run_time=1.5)
            self.play(Create(axes_), FadeIn(side[2]), FadeIn(side[3:5]))
            vo.wait_until("d")
            self.play(FadeIn(side[5]))
            self.play(FadeIn(side[6:]))
        for m in (vv, rd, tr):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def open_set(self):
        d = load("linmaps")
        A, s, safe = d["A"], d["s"], float(d["safe"])
        U, S, Vt = np.linalg.svd(A)
        P = np.outer(U[:, 1], Vt[1])  # the weakest direction of A
        assert abs(safe - s[1]) < 1e-12
        ax = square_axes([-2.6, 2.6, 1], [-2.1, 2.1, 1], 1.15).move_to([-3.2, -0.55, 0])
        ax.set_opacity(0.6)
        tT = ValueTracker(0.0)

        def B():
            return A - tT.get_value() * s[1] * P

        ellA = VMobject(color=GREY_B, stroke_width=2).set_points_as_corners([ax.c2p(*p) for p in ellipse_pts(A)])
        ellB = always_redraw(lambda: VMobject(color=C.OPERATOR, stroke_width=3.5).set_points_as_corners(
            [ax.c2p(*p) for p in ellipse_pts(B())]))

        def readout():
            t = tT.get_value()
            sv = np.linalg.svd(B(), compute_uv=False)
            ok = sv[1] > 1e-6
            return VGroup(MathTex(rf"\|B - A\| = {t * s[1]:.3f}", font_size=30),
                          MathTex(rf"\min_{{|x|=1}} |Bx| = {sv[1]:.3f}", font_size=30, color=C.CONNECTED_SET),
                          MathTex(r"\text{invertible}" if ok else r"\text{singular}", font_size=30,
                                  color=C.CONNECTED_SET if ok else C.PATHOLOGY)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.0, 0.9, 0])

        ro = always_redraw(readout)
        for t in (0.0, 0.5, 0.99):
            assert np.linalg.svd(A - t * s[1] * P, compute_uv=False)[1] > 1e-6
        assert np.linalg.svd(A - s[1] * P, compute_uv=False)[1] < 1e-12
        head = VGroup(label(r"\textbf{Rudin 9.8} \ the invertible maps form an open set", font_size=30),
                      MathTex(r"\|B - A\| < \frac{1}{\|A^{-1}\|} \;\Rightarrow\; B \text{ is invertible}", font_size=34,
                              color=C.EPS)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.25)
        side = VGroup(MathTex(rf"\frac{{1}}{{\|A^{{-1}}\|}} = \min_{{|x|=1}}|Ax| = {safe:.4f}", font_size=30),
                      label(r"push $A$ along its weakest direction:", font_size=24, color=GREY_A),
                      label(r"the ellipse flattens to a segment", font_size=24, color=GREY_A),
                      label(r"exactly when $\|B - A\|$ reaches the radius", font_size=24, color=C.PATHOLOGY),
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.3, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Which linear maps can be undone? Rudin's theorem 9.8: the invertible ones form an "
            "open set. Around an invertible A there's a ball of radius one over the norm of A inverse, and every map "
            "in it is invertible. <bookmark mark='b'/> That radius is the shortest semi-axis of A's ellipse. "
            "<bookmark mark='c'/> Push A along its weakest direction and the ellipse flattens. It collapses to a "
            "segment, and the map becomes singular, exactly when the push reaches the radius: the ball is as large "
            "as it can be."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax), Create(ellA))
            vo.wait_until("a")
            self.play(FadeIn(head[1]))
            vo.wait_until("b")
            self.play(FadeIn(ellB), FadeIn(ro), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1:3]))
            self.play(tT.animate.set_value(1.0), run_time=5.0, rate_func=linear)
            self.play(FadeIn(side[3]))
        for m in (ellB, ro):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def neumann(self):
        d = load("linmaps")
        A, B, errs = d["A"], d["B"], d["errs"]
        Ainv = np.linalg.inv(A)
        Binv = np.linalg.inv(B)
        ax = square_axes([-2.0, 2.0, 1], [-1.8, 1.8, 1], 1.35).move_to([-3.4, -0.65, 0])
        ax.set_opacity(0.6)
        target = VMobject(color=WHITE, stroke_width=3).set_points_as_corners([ax.c2p(*p) for p in ellipse_pts(Binv)])
        Ssum, term, parts = np.zeros((2, 2)), Ainv.copy(), []
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.EPS), k / 5) for k in range(6)]
        for k in range(6):
            Ssum = Ssum + term
            parts.append(VMobject(color=cols[k], stroke_width=3).set_points_as_corners(
                [ax.c2p(*p) for p in ellipse_pts(Ssum)]))
            term = Ainv @ (A - B) @ term
        head = VGroup(label(r"Why: \ a geometric series of maps \ (the Neumann series)", font_size=30),
                      MathTex(r"B^{-1} = \sum_{k \ge 0} \big(A^{-1}(A - B)\big)^k A^{-1}, \qquad "
                              r"\|A^{-1}(A - B)\| < 1", font_size=32)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.25)
        tl = label(r"white: \ the image of the unit circle under $B^{-1}$", font_size=22, color=GREY_A).next_to(
            ax, DOWN, buff=0.1)
        tab = VGroup(MathTex(r"k", r"\quad \|S_k - B^{-1}\|", font_size=28, color=GREY_A))
        for k in range(8):
            tab.add(MathTex(rf"{k}", r"\quad " + (f"{errs[k]:.4f}" if errs[k] > 1e-3 else sci(float(errs[k]), 1)),
                            font_size=28))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([2.4, -0.5, 0])
        regrid(tab)
        note_ = VGroup(label(r"each term shrinks by", font_size=24, color=GREY_A),
                       label(r"at least the ratio", font_size=24, color=GREY_A),
                       MathTex(rf"\|A^{{-1}}(A - B)\| = {float(d['q']):.3f}", font_size=28, color=C.EPS),
                       label(r"Part 10: the same series", font_size=24, color=GREY_B),
                       label(r"runs spectral theory", font_size=24, color=GREY_B),
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([5.4, -0.4, 0])
        assert np.all(np.diff(errs) < 0)
        scalar = VGroup(label(r"the scalar version:", font_size=24, color=GREY_A),
                        MathTex(r"\frac{1}{1 - q} = 1 + q + q^2 + \cdots, \quad |q| < 1", font_size=30),
                        MathTex(r"B = A\big(I - A^{-1}(A - B)\big)", font_size=30, color=C.OPERATOR)
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.3, 0.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The proof is a geometric series. Write B as A times the identity minus a small map; "
            "then B inverse is the sum of the powers of that small map, times A inverse, just as one over one minus q "
            "is the sum of the powers of q. <bookmark mark='b'/> The partial sums, drawn as images of the unit circle, "
            "close in on B inverse's ellipse, <bookmark mark='c'/> with the error shrinking geometrically. "
            "<bookmark mark='d'/> This little series comes back in Part 10, where it runs the theory of the spectrum."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax), Create(target), FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(head[1]), FadeIn(scalar[:2]))
            self.play(FadeIn(scalar[2]))
            vo.wait_until("b")
            self.play(FadeOut(scalar), Create(parts[0]), FadeIn(tab[0]), FadeIn(tab[1]))
            cur = parts[0]
            for k in range(1, 6):
                self.play(cur.animate.set_stroke(opacity=0.3, width=1.5), Create(parts[k]), FadeIn(tab[k + 1]),
                          run_time=0.9)
                cur = parts[k]
            vo.wait_until("c")
            self.play(FadeIn(tab[7:]), FadeIn(note_[:3]))
            vo.wait_until("d")
            self.play(FadeIn(note_[3:]))
        self.wait(0.4)
        self.clear_scene()
