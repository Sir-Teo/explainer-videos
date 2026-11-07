from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs52.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, load


def sci(v: float, digits: int = 1) -> str:
    """A number as TeX: 1.6 x 10^{16}."""
    e = math.floor(math.log10(abs(v)))
    m = v / 10 ** e
    if round(m, digits) >= 10:
        m, e = m / 10, e + 1
    return rf"{m:.{digits}f} \times 10^{{{e}}}"


def pattern(rows, size=26, color=WHITE):
    """A matrix of x's and zeros, the shape of a factorization in progress."""
    m = Matrix([[r"\times" if c == "x" else r"0" for c in r] for r in rows],
               element_to_mobject_config={"font_size": size, "color": color}, h_buff=0.55, v_buff=0.45)
    for e, c in zip(m.get_entries(), "".join(rows)):
        if c == "0":
            e.set_color(GREY_C)
    return m


class Qr(VoiceoverScene):
    def construct(self):
        self.card()
        self.normal()
        self.viaqr()
        self.mirrors()
        self.givens()
        self.gramschmidt()

    def card(self):
        card = chapter_card(4, r"Least squares and QR",
                            r"How do we fit more equations than unknowns, \ without squaring the trouble?",
                            lit=(1805, 1958, 1965), extra=((1805, r"Legendre: \ least squares"),
                                                           (1958, r"Householder: \ mirrors"),
                                                           (1965, r"Golub: \ least squares by QR")), part=PART)
        with self.voiceover("Chapter four. Least squares and QR."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def normal(self):
        head = label(r"Least squares, \ and the normal equations", font_size=36).to_edge(UP, buff=0.3)
        plane = Polygon([-6.5, -2.2, 0], [-2.4, -2.2, 0], [-0.9, -0.3, 0], [-5.0, -0.3, 0], stroke_color=GREY_C,
                        stroke_width=1.5, fill_color=DATA, fill_opacity=0.12)
        pl = label(r"the columns of $A$ span this plane", font_size=18, color=GREY_A).next_to(plane, DOWN,
                                                                                            buff=0.15)
        O = np.array([-4.9, -1.6, 0])
        B = np.array([-2.8, 1.9, 0])
        P = np.array([-2.8, -0.85, 0])
        ab = Arrow(O, B, buff=0, color=DATA, stroke_width=4, max_tip_length_to_length_ratio=0.08)
        ap = Arrow(O, P, buff=0, color=YES, stroke_width=4, max_tip_length_to_length_ratio=0.12)
        ar = DashedLine(P, B, color=NO, stroke_width=3)
        corner = VMobject(color=GREY_A, stroke_width=1.5).set_points_as_corners(
            [P + UP * 0.25, P + UP * 0.25 + LEFT * 0.25 + DOWN * 0.1, P + LEFT * 0.25 + DOWN * 0.1])
        bl = MathTex(r"b", font_size=30, color=DATA).next_to(B, UL, buff=0.08)
        pl2 = MathTex(r"A\hat x", font_size=30, color=YES).next_to(ap.get_center(), DOWN, buff=0.15)
        rl = MathTex(r"r = b - A\hat x", font_size=28, color=NO).next_to(ar, RIGHT, buff=0.15)
        cols = {r"A^{\mathsf T}\!A": KERN, r"\kappa(A)^2": NO}
        rows = VGroup(
            cmath(r"\min_x", r"\|Ax - b\|", font_size=36),
            cmath(r"A^{\mathsf T}", r"(b - A\hat x)", r"= 0", font_size=36),
            cmath(r"A^{\mathsf T}\!A", r"\,\hat x", r"=", r"A^{\mathsf T} b", colors=cols, font_size=36),
            cmath(r"\kappa(", r"A^{\mathsf T}\!A", r")", r"=", r"\kappa(A)^2", colors=cols, font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.62).move_to([3.0, 0.3, 0])
        whys = VGroup(label(r"more equations than unknowns: \ the closest fit", font_size=18, color=GREY_B),
                      label(r"the residual is perpendicular to every column", font_size=18, color=GREY_B),
                      label(r"the normal equations: \ small and square", font_size=18, color=GREY_B),
                      label(r"$A^{\mathsf T}\!A$ has the squares of $A$'s singular values", font_size=18,
                            color=NO))
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.12).align_to(r, LEFT)
        with self.voiceover(
            "Least squares, published by Adrien-Marie Legendre in 1805 and claimed by Gauss, fits a model with more "
            "equations than unknowns. <bookmark mark='a'/> We want the x that brings A x as close as possible to "
            "b. <bookmark mark='b'/> The closest A x is the foot of the perpendicular from b to the plane spanned "
            "by A's columns, so the residual is orthogonal to every column: A transposed times the residual is "
            "zero. <bookmark mark='c'/> Rearranged, these are the normal equations, a small square system. "
            "<bookmark mark='d'/> But A transposed A has the squares of A's singular values, so its condition "
            "number is kappa squared. A problem with kappa a million becomes one with kappa a trillion."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plane), FadeIn(pl))
            vo.wait_until("a")
            self.play(GrowArrow(ab), FadeIn(bl), Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(GrowArrow(ap), FadeIn(pl2))
            self.play(Create(ar), Create(corner), FadeIn(rl))
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]))
        self.wait(0.4)
        self.clear_scene()

    def viaqr(self):
        rows_ = load("lsq")["rows"]
        head = label(r"Least squares by QR", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            MathTex(r"A = Q\begin{bmatrix} R \\ 0 \end{bmatrix}", r",\qquad Q^{\mathsf T}Q = I", font_size=32),
            MathTex(r"\|Ax - b\|", r"=", r"\left\| \begin{bmatrix} R\,x \\ 0 \end{bmatrix} - Q^{\mathsf T} b "
                    r"\right\|", font_size=32),
            MathTex(r"R\,\hat x", r"=", r"\big(Q^{\mathsf T} b\big)_{1:n}", font_size=34, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        whys = VGroup(label(r"$Q$ orthogonal, \ $R$ upper triangular", font_size=18, color=GREY_B),
                      label(r"multiplying by $Q^{\mathsf T}$ changes no lengths", font_size=18, color=GREY_B),
                      label(r"solve the top rows: \ $\kappa(R) = \kappa(A)$, \ not squared", font_size=18,
                            color=YES))
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.12).align_to(r, LEFT)
        ax = CornerAxes(x_range=[1, 9, 1], y_range=[-16, 0, 2], x_length=5.2, y_length=4.3, tips=False,
                        axis_config={"stroke_color": GREY_C})
        ax.move_to([3.6, -0.15, 0])
        xt = VGroup(*[MathTex(rf"10^{{{p}}}", font_size=22, color=GREY_B).next_to(ax.c2p(p, -16), DOWN, buff=0.12)
                      for p in (2, 4, 6, 8)])
        yt = VGroup(*[MathTex(rf"10^{{{p}}}", font_size=22, color=GREY_B).next_to(ax.c2p(1, p), LEFT, buff=0.1)
                      for p in (-16, -12, -8, -4, 0)])
        xl = label(r"$\kappa(A)$", font_size=18, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"error in the fit, \ computed", font_size=18, color=GREY_A).next_to(ax, UP,
                                                                                      buff=0.12).align_to(ax, LEFT)

        def series(key, color):
            pts = [ax.c2p(math.log10(r["kappa"]), math.log10(r[key])) for r in rows_]
            return VGroup(VMobject(color=color, stroke_width=3).set_points_as_corners(pts),
                          *[Dot(p, radius=0.06, color=color) for p in pts])
        sn, sq = series("normal", NO), series("qr", YES)
        last = rows_[-1]
        kn = label(rf"normal equations: \ {last['normal']:.2f}", font_size=18, color=NO).next_to(
            sn[-1], LEFT, buff=0.15).shift(UP * 0.1)
        kq = label(rf"QR: \ ${sci(last['qr'])}$", font_size=18, color=YES).next_to(sq[-1], DOWN, buff=0.15).shift(
            LEFT * 0.4)
        with self.voiceover(
            "Gene Golub's answer, in 1965, was never to form A transposed A at all. <bookmark mark='a'/> Factor A "
            "as an orthogonal matrix Q times an upper triangular R. <bookmark mark='b'/> Multiplying by Q "
            "transposed changes no lengths, so the size of the residual is unchanged, and the problem splits in "
            "two. <bookmark mark='c'/> The bottom rows are what no x can fix; the top rows are a triangular system "
            "whose condition number is kappa, not kappa squared. <bookmark mark='d'/> Our instrument fits a tall "
            "system at four condition numbers. The normal equations' error grows like kappa squared, reaching "
            "thirty-seven percent at kappa ten to the eight. <bookmark mark='e'/> The QR solution's error grows "
            "only like kappa."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            self.play(Create(sn), FadeIn(kn), run_time=1.5)
            vo.wait_until("e")
            self.play(Create(sq), FadeIn(kq), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def mirrors(self):
        m = load("mirrors")
        mir = m["mirror2"][0]
        A2, R2 = m["A2"], m["R2"]
        head = label(r"Householder's mirrors", font_size=36).to_edge(UP, buff=0.3)
        O = np.array([-3.7, -0.6, 0])
        s = 0.55

        def P(v):
            return O + s * np.array([v[0], v[1], 0])
        axes_ = VGroup(Line(O + LEFT * 2.95, O + RIGHT * 2.9, color=GREY_D, stroke_width=1.5),
                       Line(O + DOWN * 2.6, O + UP * 2.9, color=GREY_D, stroke_width=1.5))
        e1 = label(r"$e_1$", font_size=20, color=GREY_B).next_to(O + RIGHT * 2.9, DOWN, buff=0.1)
        v = np.array(mir["v"])
        d = np.array([-v[1], v[0]])
        mline = DashedLine(P(-5.6 * d), P(5.6 * d), color=HEAD, stroke_width=2.5)
        ml = label(r"mirror", font_size=18, color=HEAD).next_to(P(5.6 * d), RIGHT, buff=0.1)
        va = Arrow(O, P(2.2 * v), buff=0, color=HEAD, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        vl = MathTex(r"v", font_size=28, color=HEAD).next_to(va.get_end(), DOWN, buff=0.08)
        x = [A2[0][0], A2[1][0]]
        y = [A2[0][1], A2[1][1]]
        hx = [R2[0][0], R2[1][0]]
        hy = [R2[0][1], R2[1][1]]
        ax_ = Arrow(O, P(x), buff=0, color=DATA, stroke_width=4, max_tip_length_to_length_ratio=0.1)
        ay_ = Arrow(O, P(y), buff=0, color=LAM, stroke_width=4, max_tip_length_to_length_ratio=0.12)
        hx_ = Arrow(O, P(hx), buff=0, color=DATA, stroke_width=4, max_tip_length_to_length_ratio=0.1)
        hy_ = Arrow(O, P(hy), buff=0, color=LAM, stroke_width=4, max_tip_length_to_length_ratio=0.12)
        xl = MathTex(rf"x = ({x[0]:g}, {x[1]:g})", font_size=26, color=DATA).next_to(P(x), RIGHT, buff=0.1)
        hxl = MathTex(rf"Hx = ({hx[0]:g}, {hx[1]:g})", font_size=26, color=DATA).next_to(P(hx), DOWN, buff=0.15)
        hxl.align_to(P(hx), LEFT)
        yl = MathTex(rf"({y[0]:g}, {y[1]:g})", font_size=24, color=LAM).next_to(P(y), LEFT, buff=0.1)
        hyl = MathTex(rf"({hy[0]:g}, {hy[1]:g})", font_size=24, color=LAM).next_to(P(hy), UP, buff=0.1)
        tx = DashedLine(P(x), P(hx), color=GREY_B, stroke_width=1.5)
        ty = DashedLine(P(y), P(hy), color=GREY_B, stroke_width=1.5)
        cols = {r"v": HEAD, r"x": DATA}
        rows = VGroup(
            cmath(r"H", r"=", r"I - 2\,v v^{\mathsf T}", r",\quad \|v\| = 1", font_size=32),
            cmath(r"H", r"x", r"=", r"x - 2\,(v^{\mathsf T} x)\,v", font_size=32),
            cmath(r"v", r"\;\propto\;", r"x + \operatorname{sign}(x_1)\,\|x\|\,e_1", font_size=32),
            cmath(r"H", r"x", r"=", r"-\operatorname{sign}(x_1)\,\|x\|\,e_1", font_size=32, colors=cols),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([3.5, 1.2, 0])
        rows[2][0].set_color(HEAD)
        whys = VGroup(label(r"a reflection: \ orthogonal, \ and its own inverse", font_size=17, color=GREY_B),
                      label(r"subtract twice the component along $v$", font_size=17, color=GREY_B),
                      label(r"the sign avoids cancellation \ (Chapter 1)", font_size=17, color=GREY_B),
                      label(r"lengths are kept, \ so $x$ lands on $\pm\|x\|\,e_1$", font_size=17, color=GREY_B))
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.08).align_to(r, LEFT)
        grp = VGroup(rows, whys)
        grp.next_to(head, DOWN, buff=0.4).to_edge(RIGHT, buff=0.35)
        Rm = MathTex(r"H\!A = \begin{bmatrix} " + rf"{R2[0][0]:g} & {R2[0][1]:g} \\ {R2[1][0] + 0:g} & "
                     rf"{R2[1][1]:g}" + r"\end{bmatrix} = R", font_size=30, color=YES)
        steps = VGroup(pattern(["xxx", "xxx", "xxx"]), MathTex(r"\xrightarrow{H_1}", font_size=30),
                       pattern(["xxx", "0xx", "0xx"]), MathTex(r"\xrightarrow{H_2}", font_size=30),
                       pattern(["xxx", "0xx", "00x"])).arrange(RIGHT, buff=0.15)
        steps.scale_to_fit_width(4.6)
        VGroup(Rm, steps).arrange(DOWN, buff=0.3).next_to(grp, DOWN, buff=0.3).set_x(grp.get_x())
        steps.shift(LEFT * max(0, steps.get_right()[0] - 6.7))
        qn = label(r"$Q = H_1 H_2 \cdots$", font_size=19, color=GREY_A).next_to(steps, DOWN, buff=0.1)
        with self.voiceover(
            "How do we find Q and R stably? Alston Householder's answer, in 1958, was mirrors. "
            "<bookmark mark='a'/> Take the first column, x, here three and four. We want a reflection that lays "
            "it on the first axis. Reflections keep lengths, so it must land at plus or minus five. "
            "<bookmark mark='b'/> The mirror is perpendicular to v, which points along x plus five times e one. "
            "Reflecting subtracts twice the component along v, <bookmark mark='c'/> and x lands exactly at minus "
            "five, zero. Choosing the sign this way adds two positive numbers instead of subtracting nearly equal "
            "ones: chapter one's cancellation, avoided. <bookmark mark='d'/> The same mirror carries the second "
            "column to minus three, one, and the matrix is triangular. <bookmark mark='e'/> A bigger matrix needs "
            "one mirror per column, each zeroing everything below the diagonal, and Q is their product."
        ) as vo:
            self.play(FadeIn(head), Create(axes_), FadeIn(e1))
            vo.wait_until("a")
            self.play(GrowArrow(ax_), FadeIn(xl))
            vo.wait_until("b")
            self.play(Create(mline), FadeIn(ml), GrowArrow(va), FadeIn(vl))
            self.play(Write(rows[0]), FadeIn(whys[0]))
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("c")
            self.play(Create(tx))
            self.play(TransformFromCopy(ax_, hx_), FadeIn(hxl), FadeIn(rows[3]), FadeIn(whys[3]), run_time=1.5)
            vo.wait_until("d")
            self.play(GrowArrow(ay_), FadeIn(yl))
            self.play(Create(ty))
            self.play(TransformFromCopy(ay_, hy_), FadeIn(hyl), FadeIn(Rm), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(steps[0]))
            self.play(FadeIn(steps[1]), FadeIn(steps[2]))
            self.play(FadeIn(steps[3]), FadeIn(steps[4]), FadeIn(qn))
        self.wait(0.4)
        self.clear_scene()

    def givens(self):
        m = load("mirrors")
        A = m["A"]
        nrot = m["givens_rotations"]
        head = label(r"Givens rotations: \ one zero at a time", font_size=36).to_edge(UP, buff=0.3)
        O = np.array([-5.4, -1.3, 0])
        s = 0.62
        a, b = A[0][0], A[1][0]
        r = math.hypot(a, b)
        axes_ = VGroup(Line(O + LEFT * 1.2, O + RIGHT * 4.0, color=GREY_D, stroke_width=1.5),
                       Line(O + DOWN * 0.8, O + UP * 3.4, color=GREY_D, stroke_width=1.5))
        vec = Arrow(O, O + s * np.array([a, b, 0]), buff=0, color=DATA, stroke_width=4,
                    max_tip_length_to_length_ratio=0.1)
        vl = MathTex(rf"({a:g}, {b:g})", font_size=26, color=DATA).next_to(vec.get_end(), UP, buff=0.1)
        ang = math.atan2(b, a)
        arc = Arc(radius=s * r * 0.55, start_angle=0, angle=ang, arc_center=O, color=HEAD, stroke_width=2.5)
        th = MathTex(r"\theta", font_size=26, color=HEAD).move_to(O + 0.42 * s * r * np.array(
            [math.cos(ang / 2), math.sin(ang / 2), 0]))
        rl = MathTex(rf"({r:g}, 0)", font_size=26, color=YES).next_to(O + s * np.array([r, 0, 0]), DOWN, buff=0.15)
        cols = {r"\begin{bmatrix} r \\ 0 \end{bmatrix}": YES}
        rows = VGroup(
            cmath(r"G = \begin{bmatrix} c & s \\ -s & c \end{bmatrix}", r",\quad",
                  r"c = \frac{a}{r},\;\; s = \frac{b}{r},\;\; r = \sqrt{a^2 + b^2}", font_size=30),
            cmath(r"G\begin{bmatrix} a \\ b \end{bmatrix}", r"=",
                  r"\frac{1}{r}\begin{bmatrix} a^2 + b^2 \\ -ab + ab \end{bmatrix}", r"=",
                  r"\begin{bmatrix} r \\ 0 \end{bmatrix}", colors=cols, font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([2.8, 1.5, 0])
        Am = Matrix([[f"{v:g}" for v in row] for row in A], element_to_mobject_config={"font_size": 26},
                    h_buff=0.6, v_buff=0.45)
        st = VGroup(Am, MathTex(r"\xrightarrow{G_{12}}", font_size=28), pattern(["xxx", "0xx", "0xx"]),
                    MathTex(r"\xrightarrow{G_{23}}", font_size=28), pattern(["xxx", "0xx", "00x"]))
        st.arrange(RIGHT, buff=0.15).scale_to_fit_width(6.2).next_to(rows, DOWN, buff=0.55)
        st.align_to([6.7, 0, 0], RIGHT)
        Am.get_entries()[6].set_color(YES)
        sl = wrapped_label(rf"our $3 \times 3$ example needs {nrot} rotations, \ not 3: \ its $(3, 1)$ entry is "
                           r"already zero", 6.2, font_size=18, color=GREY_A).next_to(st, DOWN, buff=0.25)
        foot = wrapped_label(r"a rotation touches two rows: \ cheap when most entries are already zero, \ as in the "
                             r"nearly triangular matrices of Chapter 6", 12.4, font_size=20,
                             color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Wallace Givens used rotations instead of mirrors. <bookmark mark='a'/> Rotate the pair a, b, here "
            "three and four, by the angle that lays it on the axis. <bookmark mark='b'/> The cosine is a over r "
            "and the sine b over r, where r is the length. <bookmark mark='c'/> Check: the second entry becomes "
            "minus a b plus a b, which is zero, and the first becomes r, here five. <bookmark mark='d'/> Each "
            "rotation touches only two rows and zeroes one entry. Our three by three example needs only two, "
            "because one entry starts at zero. <bookmark mark='e'/> That economy is why the eigenvalue algorithm "
            "of chapter six applies rotations to its nearly triangular matrices."
        ) as vo:
            self.play(FadeIn(head), Create(axes_))
            vo.wait_until("a")
            self.play(GrowArrow(vec), FadeIn(vl))
            self.play(Create(arc), FadeIn(th))
            vo.wait_until("b")
            self.play(Write(rows[0]))
            vo.wait_until("c")
            self.play(Rotate(vec, angle=-ang, about_point=O), FadeOut(vl), run_time=1.5)
            self.play(FadeIn(rl), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(st[0]))
            self.play(FadeIn(st[1]), FadeIn(st[2]))
            self.play(FadeIn(st[3]), FadeIn(st[4]), FadeIn(sl))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def gramschmidt(self):
        rows_ = load("ortho")["rows"]
        head = label(r"Gram--Schmidt, \ classical and modified", font_size=36).to_edge(UP, buff=0.3)
        lines = ["for j in range(n):", "    v = a[j]", "    for i in range(j):", "        r = q[i] @ a[j]",
                 "        v -= r * q[i]", "    q[j] = v / norm(v)"]
        cgs = code_block(lines, size=15)
        mgs = code_block(lines[:3] + ["        r = q[i] @ v"] + lines[4:], size=15)
        cgs[3].set_color(NO)
        mgs[3].set_color(HEAD)
        ct = label(r"classical", font_size=19, color=NO)
        mt = label(r"modified", font_size=19, color=HEAD)
        left = VGroup(VGroup(ct, cgs).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
                      VGroup(mt, mgs).arrange(DOWN, aligned_edge=LEFT, buff=0.12)).arrange(DOWN, aligned_edge=LEFT,
                                                                                          buff=0.4)
        left.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.45)
        same = label(r"identical in exact arithmetic", font_size=18, color=GREY_A).next_to(left, DOWN, buff=0.3)
        same.align_to(left, LEFT)
        ax = CornerAxes(x_range=[3, 13, 1], y_range=[-16, 2, 2], x_length=4.6, y_length=4.4, tips=False,
                        axis_config={"stroke_color": GREY_C})
        ax.move_to([0.6, -0.1, 0])
        xt = VGroup(*[label(rf"{n}", font_size=17, color=GREY_B).next_to(ax.c2p(n, -16), DOWN, buff=0.12)
                      for n in (4, 6, 8, 10, 12)])
        yt = VGroup(*[MathTex(rf"10^{{{p}}}", font_size=22, color=GREY_B).next_to(ax.c2p(3, p), LEFT, buff=0.1)
                      for p in (-16, -12, -8, -4, 0)])
        xl = label(r"size $n$ of the Hilbert matrix", font_size=18, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"$\|I - Q^{\mathsf T} Q\|$, \ computed", font_size=18, color=GREY_A).next_to(
            ax, UP, buff=0.12).align_to(ax, LEFT)

        def series(key, color):
            pts = [ax.c2p(r["n"], math.log10(r[key])) for r in rows_]
            return VGroup(VMobject(color=color, stroke_width=3).set_points_as_corners(pts),
                          *[Dot(p, radius=0.06, color=color) for p in pts])
        sc, sm, sh = series("cgs", NO), series("mgs", HEAD), series("householder", YES)
        r8, r12 = {r["n"]: r for r in rows_}[8], rows_[-1]
        keys = VGroup(
            label(rf"classical: \ {r8['cgs']:.1f} at $n = 8$", font_size=18, color=NO),
            label(rf"modified: \ {r12['mgs']:.2f} at $n = 12$, \ $\propto \kappa$", font_size=18,
                  color=HEAD),
            label(rf"Householder: \ ${sci(max(r['householder'] for r in rows_))}$ at worst", font_size=18,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ax, RIGHT, buff=0.35).shift(UP * 0.6)
        if keys.get_right()[0] > 6.85:
            keys.shift(LEFT * (keys.get_right()[0] - 6.85))
        with self.voiceover(
            "The textbook way to get Q is Gram–Schmidt: take each column and subtract its components along the "
            "columns before it. <bookmark mark='a'/> Classical Gram–Schmidt measures each component against the "
            "original column. <bookmark mark='b'/> Modified Gram–Schmidt measures it against the column as "
            "updated so far. In exact arithmetic they are the same algorithm. <bookmark mark='c'/> In floating "
            "point, on Hilbert matrices, the classical version's Q is not orthogonal at all by size eight. "
            "<bookmark mark='d'/> The modified one loses orthogonality in proportion to kappa, as Åke Björck "
            "proved in 1967. <bookmark mark='e'/> Householder's mirrors stay orthogonal to machine precision at "
            "every size, because every mirror is exactly orthogonal by construction."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(left[0]))
            vo.wait_until("b")
            self.play(FadeIn(left[1]), FadeIn(same))
            vo.wait_until("c")
            self.play(Create(sc), FadeIn(keys[0]), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(sm), FadeIn(keys[1]), run_time=1.5)
            vo.wait_until("e")
            self.play(Create(sh), FadeIn(keys[2]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN)
