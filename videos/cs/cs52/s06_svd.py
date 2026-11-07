from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs52.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


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


def log_ticks(ax, x0, ys, size=20):
    """Powers of ten beside a log-scale y axis whose left edge is at x0."""
    return VGroup(*[MathTex(rf"10^{{{p}}}", font_size=size, color=GREY_B).next_to(ax.c2p(x0, p), LEFT, buff=0.1)
                    for p in ys])


class Svd(VoiceoverScene):
    def construct(self):
        self.card()
        self.geometry()
        self.rank()
        self.naive()
        self.truncate()
        self.lastresort()

    def card(self):
        card = chapter_card(5, r"The SVD", r"What is left when a matrix is nearly singular?",
                            lit=(1873, 1936, 1965), extra=((1873, r"Beltrami: \ the decomposition"),
                                                           (1936, r"Eckart and Young: \ best low rank"),
                                                           (1965, r"Golub and Kahan: \ computing it")), part=PART)
        with self.voiceover("Chapter five. The singular value decomposition."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def geometry(self):
        head = label(r"Rotate, \ stretch, \ rotate", font_size=36).to_edge(UP, buff=0.3)
        A = np.array([[1.2, 0.7], [0.2, 0.9]])          # illustrative: only its geometry is drawn
        U, S, Vt = np.linalg.svd(A)
        if np.linalg.det(U) < 0:                         # choose both factors as rotations (det A > 0)
            U[:, 1] *= -1
            Vt[1, :] *= -1
        if U[0, 0] < 0:                                  # turn both by half a turn so that u_1 points right
            U, Vt = -U, -Vt
        O = np.array([-4.2, -0.5, 0])
        s = 1.05

        def M3(M):
            return np.array([[M[0, 0], M[0, 1], 0], [M[1, 0], M[1, 1], 0], [0, 0, 1]])
        cross = VGroup(Line(O + LEFT * 2.6, O + RIGHT * 2.6, color=GREY_D, stroke_width=1.2),
                       Line(O + DOWN * 2.3, O + UP * 2.3, color=GREY_D, stroke_width=1.2))
        circ = Circle(radius=s, color=GREY_A, stroke_width=3).move_to(O)
        v1 = Line(O, O + s * np.array([Vt[0, 0], Vt[0, 1], 0]), color=DATA, stroke_width=5)
        v2 = Line(O, O + s * np.array([Vt[1, 0], Vt[1, 1], 0]), color=LAM, stroke_width=5)
        shape = VGroup(circ, v1, v2)
        l1 = MathTex(r"v_1", font_size=28, color=DATA).next_to(v1.get_end(), UR, buff=0.05)
        l2 = MathTex(r"v_2", font_size=28, color=LAM).next_to(v2.get_end(), UL, buff=0.05)
        stages = VGroup(label(r"$V^{\mathsf T}$: \ rotate the $v_i$ onto the axes", font_size=19, color=GREY_A),
                        label(r"$\Sigma$: \ stretch the axes by $\sigma_1$ and $\sigma_2$", font_size=19,
                              color=GREY_A),
                        label(r"$U$: \ rotate again; \ the circle is now an ellipse", font_size=19, color=GREY_A))
        for st in stages:
            st.move_to(O + DOWN * 2.75)
        ill = note(r"illustrative $2 \times 2$ matrix", font_size=16).next_to(cross, UP, buff=0.05).align_to(
            cross, LEFT)
        e1 = U[:, 0] * S[0] * s
        e2 = U[:, 1] * S[1] * s
        f1 = MathTex(r"\sigma_1 u_1", font_size=28, color=DATA).next_to(
            O + np.array([*e1, 0]), np.array([*U[:, 0], 0]), buff=0.15)
        f2 = MathTex(r"\sigma_2 u_2", font_size=28, color=LAM).next_to(
            O + np.array([*e2, 0]), np.array([*U[:, 1], 0]), buff=0.15)
        cols = {r"v_i": DATA, r"V": DATA, r"V^{\mathsf T}": DATA, r"\,u_i": LAM, r"U": LAM, r"\sigma_i": HEAD,
                r"\Sigma": HEAD, r"\frac{\sigma_1}{\sigma_n}": KERN}
        rows = VGroup(
            cmath(r"A", r"v_i", r"=", r"\sigma_i", r"\,u_i", colors=cols, font_size=36),
            cmath(r"A", r"V", r"=", r"U", r"\Sigma", colors=cols, font_size=36),
            cmath(r"A", r"=", r"U", r"\Sigma", r"V^{\mathsf T}", colors=cols, font_size=36),
            cmath(r"\kappa(A)", r"=", r"\|A\|\,\|A^{-1}\|", r"=", r"\frac{\sigma_1}{\sigma_n}", colors=cols,
                  font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.62).move_to([2.6, 0.2, 0])
        whys = VGroup(
            label(r"each orthonormal $v_i$ goes to a stretched orthonormal $u_i$", font_size=18, color=GREY_B),
            label(r"all $n$ at once: \ the vectors as columns", font_size=18, color=GREY_B),
            label(r"$V$ is orthogonal, \ so $V^{-1} = V^{\mathsf T}$", font_size=18, color=GREY_B),
            label(r"$\|A\| = \sigma_1$, \ $\|A^{-1}\| = 1/\sigma_n$: \ Chapter 1's $\kappa$", font_size=18,
                  color=KERN),
        )
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.12).align_to(r, LEFT)
        with self.voiceover(
            "Every matrix, of any shape, has a singular value decomposition. <bookmark mark='a'/> Watch this two "
            "by two matrix act on the unit circle. First a rotation, V transposed, turns two special "
            "perpendicular directions onto the axes. <bookmark mark='b'/> Then a diagonal matrix, sigma, "
            "stretches each axis by a singular value. <bookmark mark='c'/> Then a second rotation, U, and the "
            "circle is an ellipse. <bookmark mark='d'/> In symbols, A sends each right singular vector v i to "
            "sigma i times u i. Side by side as columns, and since V is orthogonal, A equals U sigma V "
            "transposed. <bookmark mark='e'/> The longest stretch over the shortest is chapter one's condition "
            "number."
        ) as vo:
            self.play(FadeIn(head), Create(cross), Create(circ), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(v1), Create(v2), FadeIn(l1), FadeIn(l2))
            self.play(FadeOut(l1), FadeOut(l2), FadeIn(stages[0]))
            self.play(ApplyMatrix(M3(Vt), shape, about_point=O), run_time=1.8)
            vo.wait_until("b")
            self.play(FadeOut(stages[0]), FadeIn(stages[1]))
            self.play(ApplyMatrix(M3(np.diag(S)), shape, about_point=O), run_time=1.8)
            vo.wait_until("c")
            self.play(FadeOut(stages[1]), FadeIn(stages[2]))
            self.play(ApplyMatrix(M3(U), shape, about_point=O), run_time=1.8)
            self.play(FadeIn(f1), FadeIn(f2))
            vo.wait_until("d")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]), FadeIn(whys[3]))
        self.wait(0.4)
        self.clear_scene()

    def rank(self):
        d = load("svd")
        sig = d["sigma"]
        n = len(sig)
        eps = 2.0 ** -52
        tol = sig[0] * n * eps
        r_num = sum(1 for v in sig if v > tol)
        noise = 1e-3                                   # the instrument's noise level (linalg.svd_regularize)
        r_noise = sum(1 for v in sig if v > noise)
        head = label(r"Rank, \ in floating point", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"\sigma_1": HEAD, r"\sigma_2": HEAD, r"\sigma_n": HEAD, r"\sigma_k": HEAD,
                r"\sigma_{k+1}": YES}
        rows = VGroup(
            cmath(r"A", r"=", r"\sigma_1", r"u_1 v_1^{\mathsf T}", r"+", r"\sigma_2", r"u_2 v_2^{\mathsf T}", r"+",
                  r"\cdots", r"+", r"\sigma_n", r"u_n v_n^{\mathsf T}", colors=cols, font_size=30),
            cmath(r"A_k", r"=", r"\sigma_1", r"u_1 v_1^{\mathsf T}", r"+", r"\cdots", r"+", r"\sigma_k",
                  r"u_k v_k^{\mathsf T}", colors=cols, font_size=30),
            cmath(r"\min_{\operatorname{rank} B \le k} \|A - B\|", r"=", r"\|A - A_k\|", r"=", r"\sigma_{k+1}",
                  colors=cols, font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.75).move_to([-3.7, 0.5, 0])
        whys = VGroup(
            label(r"multiply $U \Sigma V^{\mathsf T}$ out: \ rank-one pieces, \ largest first", font_size=18,
                  color=GREY_B),
            label(r"keep the first $k$", font_size=18, color=GREY_B),
            label(r"Eckart and Young \ (1936): \ no rank-$k$ matrix is closer", font_size=18, color=YES),
        )
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.12).align_to(r, LEFT)
        ax = CornerAxes(x_range=[0, 80, 10], y_range=[-17, 1, 2], x_length=4.5, y_length=4.4, tips=False,
                        axis_config={"stroke_color": GREY_C})
        ax.move_to([4.15, -0.25, 0])
        yt = log_ticks(ax, 0, (-16, -12, -8, -4, 0))
        xt = VGroup(*[label(rf"{k}", font_size=16, color=GREY_B).next_to(ax.c2p(k, -17), DOWN, buff=0.1)
                      for k in (1, 20, 40, 60, 80)])
        xl = label(r"$i$", font_size=18, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yl = label(r"$\sigma_i$ of an $80 \times 80$ blur, \ computed", font_size=18, color=GREY_A).next_to(
            ax, UP, buff=0.12).align_to(ax, LEFT)
        dots = VGroup(*[Dot(ax.c2p(i + 1, math.log10(v)), radius=0.035,
                            color=HEAD if v > noise else (KERN if v > tol else GREY_B)) for i, v in enumerate(sig)])
        lt = DashedLine(ax.c2p(0, math.log10(tol)), ax.c2p(80, math.log10(tol)), color=NO, stroke_width=2)
        ltl = label(rf"rounding: \ ${n}\,\sigma_1 \varepsilon$; \ {r_num} above it", font_size=17, color=NO)
        ltl.next_to(lt, UP, buff=0.06).align_to(lt, LEFT).shift(RIGHT * 0.15)
        ln = DashedLine(ax.c2p(0, -3), ax.c2p(80, -3), color=YES, stroke_width=2)
        lnl = label(rf"noise in the data, \ $10^{{-3}}$: \ {r_noise} above it", font_size=17, color=YES)
        lnl.next_to(ln, UP, buff=0.1).align_to(ln, RIGHT)
        with self.voiceover(
            "Multiply the decomposition out and a matrix becomes a sum of rank-one pieces, largest first. "
            "<bookmark mark='a'/> Keep the first k, and you have the best rank k approximation there is: Carl "
            "Eckart and Gale Young proved in 1936 that its error is the next singular value, the fact behind the "
            "embeddings of AI, Built, Part 3. <bookmark mark='b'/> Here are the eighty singular values of a "
            "matrix that blurs a signal. <bookmark mark='c'/> Below the rounding level they are noise in the "
            f"arithmetic, so the numerical rank is {r_num}, not eighty. <bookmark mark='d'/> And below the noise "
            f"in our data, one part in a thousand, only {r_noise} carry information. In floating point, rank "
            "depends on a tolerance."
        ) as vo:
            self.play(FadeIn(head), Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("a")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(xl), FadeIn(yl))
            self.play(LaggedStart(*[FadeIn(dt) for dt in dots], lag_ratio=0.04), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(lt), FadeIn(ltl))
            vo.wait_until("d")
            self.play(Create(ln), FadeIn(lnl))
        self.wait(0.4)
        self.clear_scene()

    def signal_axes(self, w=5.6, h=3.0):
        ax = CornerAxes(x_range=[0, 1, 0.25], y_range=[-0.4, 1.4, 0.5], x_length=w, y_length=h, tips=False,
                        axis_config={"stroke_color": GREY_C})
        yt = VGroup(*[label(rf"{v:g}", font_size=16, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (0, 0.5, 1)])
        return ax, yt

    def curve(self, ax, ys, color, width=3):
        n = len(ys)
        pts = [ax.c2p(i / (n - 1), max(-0.4, min(1.4, y))) for i, y in enumerate(ys)]
        return VMobject(color=color, stroke_width=width).set_points_as_corners(pts)

    def naive(self):
        d = load("svd")
        head = label(r"Undoing a blur", font_size=36).to_edge(UP, buff=0.3)
        ax, yt = self.signal_axes()
        VGroup(ax, yt).move_to([-3.4, 0.0, 0])
        cx = self.curve(ax, d["x"], YES)
        cb = self.curve(ax, d["b"], HEAD)
        kx = label(r"the signal $x$", font_size=18, color=YES)
        kb = label(r"observed: \ $b = Kx + e$", font_size=18, color=HEAD)
        VGroup(kx, kb).arrange(RIGHT, buff=0.5).next_to(ax, DOWN, buff=0.3)
        cols = {r"\frac{u_i^{\mathsf T} e}{\sigma_i}": NO, r"x_{\text{true}}": YES}
        rows = VGroup(
            cmath(r"x", r"=", r"K^{-1} b", r"=", r"V \Sigma^{-1} U^{\mathsf T} b", colors=cols, font_size=32),
            cmath(r"x", r"=", r"\sum_i", r"\frac{u_i^{\mathsf T} b}{\sigma_i}", r"\,v_i", colors=cols, font_size=32),
            cmath(r"x", r"=", r"x_{\text{true}}", r"+", r"\sum_i", r"\frac{u_i^{\mathsf T} e}{\sigma_i}", r"\,v_i",
                  colors=cols, font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([3.3, 0.9, 0])
        whys = VGroup(
            label(r"invert each factor: \ the orthogonal ones by transposing", font_size=18, color=GREY_B),
            label(r"one term per singular value", font_size=18, color=GREY_B),
            label(r"the noise $e$ is divided by $\sigma_i$ too", font_size=18, color=NO),
        )
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.12).align_to(r, LEFT)
        res = VGroup(
            label(rf"$\kappa(K) = {sci(d['kappa'])}$", font_size=22, color=KERN),
            label(rf"error of the naive solve: \ ${sci(d['x_naive_error'])}$ times the signal", font_size=22,
                  color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(whys[2], DOWN, buff=0.45).align_to(rows, LEFT)
        with self.voiceover(
            "Here is the experiment. <bookmark mark='a'/> A signal of two boxes, in green, is blurred by that "
            "matrix, and noise of one part in a thousand is added: the yellow curve. Can we undo the blur? "
            "<bookmark mark='b'/> Invert each factor of the decomposition, and the solution is a sum with one "
            "term per singular value, each coefficient divided by its sigma. <bookmark mark='c'/> But the noise "
            "is divided by the singular values too, and the smallest is ten to the minus sixteen. <bookmark "
            "mark='d'/> The condition number is about ten to the sixteen, and the naive solution's error is ten "
            "to the thirteen times the signal. The arithmetic is not at fault: the problem, as posed, cannot be "
            "solved."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yt))
            vo.wait_until("a")
            self.play(Create(cx), FadeIn(kx))
            self.play(Create(cb), FadeIn(kb))
            vo.wait_until("b")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(res[0]))
            self.play(FadeIn(res[1]))
        self.wait(0.4)
        self.clear_scene()

    def truncate(self):
        d = load("svd")
        rows_ = d["rows"]
        kb = d["best_k"]
        best = rows_[kb - 1]
        head = label(r"Truncate: \ regularization", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"\sigma_i": HEAD, r"\frac{\sigma_i^2}{\sigma_i^2 + \lambda^2}": LAM}
        f1 = cmath(r"x_k", r"=", r"\sum_{i=1}^{k}", r"\frac{u_i^{\mathsf T} b}{\sigma_i}", r"\,v_i", colors=cols,
                   font_size=32)
        f2 = cmath(r"x_\lambda", r"=", r"\sum_{i=1}^{n}", r"\frac{\sigma_i^2}{\sigma_i^2 + \lambda^2}",
                   r"\frac{u_i^{\mathsf T} b}{\sigma_i}", r"\,v_i", colors=cols, font_size=32)
        VGroup(f1, f2).arrange(RIGHT, buff=1.4).next_to(head, DOWN, buff=0.35)
        t1 = label(r"truncated SVD: \ drop the small $\sigma_i$", font_size=17, color=GREY_B).next_to(f1, DOWN,
                                                                                                    buff=0.1)
        t2 = label(r"Tikhonov \ (1963): \ damp them smoothly", font_size=17, color=LAM).next_to(f2, DOWN, buff=0.1)
        ax = CornerAxes(x_range=[0, 80, 10], y_range=[-1, 14, 1], x_length=4.6, y_length=3.5, tips=False,
                        axis_config={"stroke_color": GREY_C})
        ax.move_to([-3.5, -1.0, 0])
        yt = log_ticks(ax, 0, (0, 4, 8, 12))
        xt = VGroup(*[label(rf"{k}", font_size=16, color=GREY_B).next_to(ax.c2p(k, -1), DOWN, buff=0.1)
                      for k in (1, 20, 40, 60, 80)])
        xl = label(r"terms kept, \ $k$", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yl = label(r"relative error of $x_k$, \ computed", font_size=17, color=GREY_A).next_to(
            ax, UP, buff=0.1).align_to(ax, LEFT)
        pts = [ax.c2p(r["k"], math.log10(r["error"])) for r in rows_]
        err = VMobject(color=NO, stroke_width=3).set_points_as_corners(pts)
        bd = Dot(ax.c2p(kb, math.log10(best["error"])), radius=0.08, color=YES)
        bl = label(rf"$k = {kb}$: \ {best['error']:.2f}", font_size=18, color=YES).next_to(bd, UP, buff=0.4)
        bl.shift(LEFT * 0.7)
        sx, syt = self.signal_axes(w=4.8, h=2.9)
        VGroup(sx, syt).move_to([3.5, -0.85, 0])
        cx = self.curve(sx, d["x"], GREY_B, width=2)
        cbest = self.curve(sx, d["x_best"], YES)
        kx = label(r"signal", font_size=17, color=GREY_B)
        kk = label(rf"$x_{{{kb}}}$, \ recovered", font_size=17, color=YES)
        VGroup(kx, kk).arrange(RIGHT, buff=0.5).next_to(sx, DOWN, buff=0.25)
        first = rows_[0]["error"]
        with self.voiceover(
            "The cure is to stop dividing by tiny numbers. <bookmark mark='a'/> Keep only the first k terms: the "
            "truncated SVD. Each term dropped loses a little signal; each term kept adds noise divided by its "
            f"sigma. <bookmark mark='b'/> Our instrument tries every k. The error falls from {100 * first:.0f} "
            f"percent with one term to {100 * best['error']:.0f} percent at k equals {kb}, then explodes, back to "
            "ten to the thirteen with all eighty. <bookmark mark='c'/> At the best k the two boxes come back, a "
            "little rounded. <bookmark mark='d'/> Andrey Tikhonov's regularization, from 1963, damps each term "
            "smoothly instead of cutting it off. Either way, we deliberately solve a nearby, well-conditioned "
            "problem."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f1), FadeIn(t1))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(xl), FadeIn(yl))
            self.play(Create(err), run_time=2.5)
            self.play(FadeIn(bd), FadeIn(bl))
            vo.wait_until("c")
            self.play(Create(sx), FadeIn(syt), Create(cx), FadeIn(kx))
            self.play(Create(cbest), FadeIn(kk), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(f2), FadeIn(t2))
        self.wait(0.4)
        self.clear_scene()

    def lastresort(self):
        head = label(r"Computing it, \ and when to reach for it", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(pattern(["xxxx", "xxxx", "xxxx", "xxxx", "xxxx"]),
                       MathTex(r"\xrightarrow{H_1 \,\cdot\,}", font_size=30),
                       pattern(["xxxx", "0xxx", "0xxx", "0xxx", "0xxx"]),
                       MathTex(r"\xrightarrow{\,\cdot\, G_1}", font_size=30),
                       pattern(["xx00", "0xxx", "0xxx", "0xxx", "0xxx"]),
                       MathTex(r"\xrightarrow{\ \cdots\ }", font_size=30),
                       pattern(["xx00", "0xx0", "00xx", "000x", "0000"], color=YES))
        steps.arrange(RIGHT, buff=0.2).scale_to_fit_width(10.6).next_to(head, DOWN, buff=0.45)
        caps = VGroup(
            label(r"a mirror from the left clears a column", font_size=17, color=GREY_B).next_to(steps[2], DOWN,
                                                                                                buff=0.15),
            label(r"one from the right clears a row", font_size=17, color=GREY_B).next_to(steps[4], DOWN, buff=0.15),
            label(r"bidiagonal: \ same $\sigma_i$", font_size=17, color=YES).next_to(steps[6], DOWN, buff=0.15),
        )
        cols = {r"\Sigma^{+}": HEAD}
        pinv = cmath(r"x^{+}", r"=", r"V", r"\Sigma^{+}", r"U^{\mathsf T} b", r",\qquad",
                     r"\sigma_i^{+} = \begin{cases} 1/\sigma_i & \sigma_i > \text{tol} \\ 0 & \text{otherwise}"
                     r"\end{cases}", colors=cols, font_size=32)
        pinv.next_to(caps, DOWN, buff=0.55)
        pl = label(r"the pseudo-inverse: \ the shortest least-squares solution, \ even when $A$ is rank deficient",
                   font_size=19, color=WHITE).next_to(pinv, DOWN, buff=0.2)
        uses = wrapped_label(r"the SVD costs several times as much as QR, \ so it is kept for when the others are not "
                             r"enough: \ numerical rank, \ rank-deficient least squares, \ ill-posed problems, \ "
                             r"principal components \ (\textit{AI, Built} 3), \ and low-rank approximation "
                             r"\ (randomized, \ in Chapter 15)", 12.4, font_size=20, color=HEAD)
        uses.next_to(pl, DOWN, buff=0.7)
        with self.voiceover(
            "How is it computed? Not from A transposed A, which would square the condition number again. "
            "<bookmark mark='a'/> Gene Golub and William Kahan, in 1965, applied Householder mirrors alternately "
            "from the left and the right, clearing a column, then a row. <bookmark mark='b'/> What is left is "
            "bidiagonal, with the same singular values, and a variant of the next chapter's QR algorithm finds "
            "them. <bookmark mark='c'/> The payoff is the pseudo-inverse: invert only the singular values above a "
            "tolerance, and you get the shortest least-squares solution even when the matrix is rank deficient. "
            "<bookmark mark='d'/> The SVD costs several times as much as QR, so it is the tool of last resort: "
            "when other methods fail, it says exactly how much the data can tell you."
        ) as vo:
            self.play(FadeIn(head), FadeIn(steps[0]))
            vo.wait_until("a")
            self.play(FadeIn(steps[1]), FadeIn(steps[2]), FadeIn(caps[0]))
            self.play(FadeIn(steps[3]), FadeIn(steps[4]), FadeIn(caps[1]))
            vo.wait_until("b")
            self.play(FadeIn(steps[5]), FadeIn(steps[6]), FadeIn(caps[2]))
            vo.wait_until("c")
            self.play(Write(pinv), FadeIn(pl))
            vo.wait_until("d")
            self.play(FadeIn(uses))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, KERN, LAM, NO)
