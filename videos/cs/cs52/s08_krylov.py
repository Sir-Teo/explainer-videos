from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs52.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load


def log_ticks(ax, x0, ys, size=20):
    """Powers of ten beside a log-scale y axis whose left edge is at x0."""
    return VGroup(*[MathTex(rf"10^{{{p}}}", font_size=size, color=GREY_B).next_to(ax.c2p(x0, p), LEFT, buff=0.1)
                    for p in ys])


def bowl_paths(A, e0, steps=12):
    """Steepest descent (exact line search) and conjugate gradients on phi(e) = e^T A e / 2, from e0: the
    points visited, in coordinates relative to the minimum.  Used only to draw an illustrative 2 x 2 bowl."""
    sd = [e0.copy()]
    e = e0.copy()
    for _ in range(steps):
        r = -A @ e
        if r @ r < 1e-14:
            break
        e = e + (r @ r) / (r @ A @ r) * r
        sd.append(e.copy())
    e = e0.copy()
    r = -A @ e
    p = r.copy()
    cg = [e.copy()]
    for _ in range(2):
        a = (r @ r) / (p @ A @ p)
        e = e + a * p
        rn = r - a * (A @ p)
        p = rn + (rn @ rn) / (r @ r) * p
        r = rn
        cg.append(e.copy())
    return sd, cg


class Krylov(VoiceoverScene):
    def construct(self):
        self.card()
        self.downhill()
        self.krylov()
        self.rate()
        self.precondition()
        self.gmres()

    def card(self):
        card = chapter_card(7, r"Conjugate gradients", r"How do we solve a million equations without factoring?",
                            lit=(1950, 1952, 1986), extra=((1950, r"Lanczos"),
                                                           (1952, r"Hestenes and Stiefel: \ CG"),
                                                           (1986, r"Saad and Schultz: \ GMRES")), part=PART)
        with self.voiceover("Chapter seven. Conjugate gradients."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def downhill(self):
        head = label(r"Solving as going downhill", font_size=36).to_edge(UP, buff=0.3)
        A = np.array([[0.6, 0.5], [0.5, 4.0]])          # illustrative: a long, narrow bowl
        e0 = np.array([-2.0, 0.8])
        C = np.array([-3.9, -0.4, 0])
        S = 1.1                                          # scene units per unit of the bowl
        w, V = np.linalg.eigh(A)
        ang = math.atan2(V[1, 0], V[0, 0])              # the long axis lies along the smaller eigenvalue's vector
        phi0 = 0.5 * e0 @ A @ e0
        rings = VGroup()
        for f in (1.0, 0.5, 0.22, 0.07, 0.015):
            c = phi0 * f
            rings.add(Ellipse(width=2 * S * math.sqrt(2 * c / w[0]), height=2 * S * math.sqrt(2 * c / w[1]),
                              color=interpolate_color(ManimColor(GREY_D), ManimColor(DATA), 1 - f),
                              stroke_width=2).rotate(ang).move_to(C))
        star = Dot(C, radius=0.07, color=YES)
        sd, cg = bowl_paths(A, e0)

        def P(e):
            return C + S * np.array([e[0], e[1], 0])
        sdp = VMobject(color=NO, stroke_width=3).set_points_as_corners([P(e) for e in sd])
        cgp = VMobject(color=YES, stroke_width=4).set_points_as_corners([P(e) for e in cg])
        start = Dot(P(e0), radius=0.07, color=WHITE)
        ill = note(r"illustrative $2 \times 2$ bowl", font_size=16).next_to(rings, DOWN, buff=0.3)
        keys = VGroup(label(r"steepest descent", font_size=18, color=NO),
                      label(r"conjugate gradients", font_size=18, color=YES)).arrange(RIGHT, buff=0.5).next_to(
            ill, DOWN, buff=0.15)
        cols = {r"-r": NO, r"Ax - b": KERN}
        rows = VGroup(
            cmath(r"\varphi(x)", r"=", r"\tfrac12\, x^{\mathsf T} A x - b^{\mathsf T} x", font_size=34),
            cmath(r"\nabla\varphi(x)", r"=", r"Ax - b", colors=cols, font_size=34),
            cmath(r"\nabla\varphi(x)", r"=", r"-r", r",\quad r = b - Ax", colors=cols, font_size=34),
            cmath(r"x", r"\leftarrow", r"x + \alpha\, r", r",\quad", r"\alpha = \frac{r^{\mathsf T} r}"
                  r"{r^{\mathsf T} A r}", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([3.0, 0.3, 0])
        whys = VGroup(label(r"$A$ symmetric positive definite: \ a bowl", font_size=18, color=GREY_B),
                      label(r"its gradient", font_size=18, color=GREY_B),
                      label(r"zero exactly at the solution; \ downhill is the residual", font_size=18, color=GREY_B),
                      label(r"steepest descent \ (Part 23), \ as far as the bowl falls", font_size=18, color=NO))
        for wy, r in zip(whys, rows):
            wy.next_to(r, DOWN, buff=0.1).align_to(r, LEFT)
        with self.voiceover(
            "For a symmetric positive definite matrix, solving A x equals b is the same as going downhill. "
            "<bookmark mark='a'/> Define phi of x as a half x transposed A x, minus b transposed x. It is a bowl, "
            "and these ellipses are its contours. <bookmark mark='b'/> Its gradient is A x minus b: "
            "<bookmark mark='c'/> zero exactly at the solution, and minus the residual everywhere else. "
            "<bookmark mark='d'/> So Part 23's gradient descent applies. Step along the residual for as long as "
            "the bowl keeps falling, and repeat. In a long, narrow bowl it zigzags, each step undoing part of the "
            "last. <bookmark mark='e'/> Conjugate gradients, on the same bowl, arrives in two steps."
        ) as vo:
            self.play(FadeIn(head), Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(r_) for r_ in rings], lag_ratio=0.2), FadeIn(star), FadeIn(ill))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(whys[3]))
            self.play(FadeIn(start), Create(sdp), FadeIn(keys[0]), run_time=3)
            vo.wait_until("e")
            self.play(Create(cgp), FadeIn(keys[1]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def krylov(self):
        head = label(r"The best point in a Krylov space", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"\mathcal{K}_k": HEAD}
        rows = VGroup(
            cmath(r"\mathcal{K}_k", r"=", r"\operatorname{span}\{\, b,\ Ab,\ A^2 b,\ \dots,\ A^{k-1} b \,\}",
                  colors=cols, font_size=32),
            cmath(r"x_k", r"=", r"\operatorname*{arg\,min}_{x \,\in\, ", r"\mathcal{K}_k", r"}\ \|x - x_*\|_A",
                  colors=cols, font_size=32),
            cmath(r"p_i^{\mathsf T} A\, p_j", r"=", r"0", r"\quad (i \ne j)", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.75).move_to([-3.3, 0.4, 0])
        whys = VGroup(
            label(r"everything $k$ products by $A$ can build from $b$", font_size=18, color=GREY_B),
            label(r"the best point of the whole space, \ in the bowl's own norm", font_size=18, color=GREY_B),
            label(r"\textbf{conjugate} directions: \ a new step never spoils the old ones", font_size=18,
                  color=YES),
        )
        for wy, r in zip(whys, rows):
            wy.next_to(r, DOWN, buff=0.12).align_to(r, LEFT)
        lines = ["x = zeros(n); r = b.copy(); p = r.copy()", "rr = r @ r",
                 "while norm(r) > tol * norm(b):", "    Ap = A @ p", "    a = rr / (p @ Ap)", "    x += a * p",
                 "    r -= a * Ap", "    rr_new = r @ r", "    p = r + (rr_new / rr) * p", "    rr = rr_new"]
        code = code_block(lines, size=15)
        code[3].set_color(HEAD)
        ct = label(r"our instrument's loop \ (no preconditioner)", font_size=18, color=GREY_A)
        cg_ = VGroup(ct, code).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.6, 0.6, 0])
        cnote = wrapped_label(r"per step: \ one product by $A$, \ two inner products, \ three vector updates; \ "
                              r"memory: \ four vectors", 5.6, font_size=19, color=HEAD).next_to(cg_, DOWN, buff=0.3)
        cnote.align_to(cg_, LEFT)
        foot = wrapped_label(r"in exact arithmetic it ends in at most $n$ steps; \ in practice it is an iteration, "
                             r"\ stopped far sooner", 12.4, font_size=20, color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Why two steps? The conjugate gradient method of Magnus Hestenes and Eduard Stiefel, from 1952, does "
            "more than go downhill. <bookmark mark='a'/> After k steps, the only vectors it can have built from b "
            "are combinations of b, A b, A squared b, and so on: the Krylov space. <bookmark mark='b'/> Conjugate "
            "gradients picks the best point in that whole space, in the bowl's own norm, not just the best along "
            "one line. <bookmark mark='c'/> It can, because its search directions are conjugate, orthogonal in "
            "A's inner product, so a new step never spoils the old ones. <bookmark mark='d'/> The loop is short: "
            "one product with A, two inner products, four vectors of memory. In exact arithmetic it ends within n "
            "steps; in practice, far sooner."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(cg_), FadeIn(cnote))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def rate(self):
        rows_ = load("krylov")["rows"]
        head = label(r"How fast: \ the square root of $\kappa$", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"\frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}": YES, r"\frac{\sqrt\kappa}{2}": YES,
                r"\frac{\kappa}{2}": NO}
        rows = VGroup(
            cmath(r"\|e_k\|_A", r"\le", r"2", r"\left(", r"\frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}", r"\right)^{k}",
                  r"\|e_0\|_A", colors=cols, font_size=32),
            cmath(r"\frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}", r"\approx", r"1 - \frac{2}{\sqrt\kappa}", colors=cols,
                  font_size=32),
            cmath(r"k", r"\approx", r"\frac{\sqrt\kappa}{2}", r"\ln\frac{2}{\text{tol}}", colors=cols,
                  font_size=32),
            cmath(r"k_{\text{steepest}}", r"\approx", r"\frac{\kappa}{2}", r"\ln\frac{1}{\text{tol}}", colors=cols,
                  font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([-3.7, 0.35, 0])
        whys = VGroup(label(r"CG's bound", font_size=18, color=GREY_B),
                      label(r"for large $\kappa$", font_size=18, color=GREY_B),
                      label(r"take logarithms: \ steps grow like $\sqrt\kappa$", font_size=18, color=YES),
                      label(r"steepest descent: \ like $\kappa$", font_size=18, color=NO))
        for wy, r in zip(whys, rows):
            wy.next_to(r, DOWN, buff=0.08).align_to(r, LEFT)
        trs = []
        for r in rows_:
            sd = f"{r['steepest']:,}" if r["steepest"] else r"over 8{,}000"
            trs.append([f"{r['n']:,}", f"{r['kappa']:,.0f}", sd, f"{r['cg']}", f"{r['cg_bound']}"])
        tab = grid_table([r"unknowns", r"$\kappa$", r"steepest", r"CG", r"CG bound"], trs,
                         widths=[1.35, 1.0, 1.55, 0.8, 1.35], row_h=0.48, font_size=19, mono_cols=())
        tab.move_to([3.6, 0.9, 0])
        for c in tab.cells[1:]:
            c[2].set_color(NO)
            c[3].set_color(YES)
        tcap = wrapped_label(r"the Poisson problem on $m \times m$ grids \ (Chapter 8), \ residual to $10^{-8}$, \ "
                             r"computed", 6.0, font_size=17, color=GREY_A).next_to(tab, UP, buff=0.25)
        big = rows_[-1]
        tnote = wrapped_label(rf"$\kappa$ grows with the number of unknowns; \ CG's steps double when the grid's "
                              rf"side doubles, \ at about half the bound; \ steepest descent's bound for the last "
                              rf"grid is {big['steepest_predicted']:,}", 6.0, font_size=18, color=WHITE).next_to(
            tab, DOWN, buff=0.35)
        with self.voiceover(
            "How fast is it? <bookmark mark='a'/> The error falls at least as fast as twice a ratio to the power "
            "k: root kappa minus one, over root kappa plus one. <bookmark mark='b'/> For large kappa that ratio "
            "is about one minus two over root kappa, <bookmark mark='c'/> so the number of steps grows like the "
            "square root of the condition number. <bookmark mark='d'/> Steepest descent has kappa where conjugate "
            "gradients has its square root. <bookmark mark='e'/> Our instrument solves the Poisson problem, "
            "chapter eight's matrix, on three grids; kappa grows with the number of unknowns. Steepest descent "
            "needs thousands of steps, and on the largest grid had not converged after eight thousand. Conjugate "
            f"gradients needs {rows_[0]['cg']}, {rows_[1]['cg']} and {rows_[2]['cg']}, about half of what the "
            "bound allows."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(FadeIn(tcap), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])),
                      LaggedStart(*[FadeIn(VGroup(*c)) for c in tab.cells[1:]], lag_ratio=0.3))
            self.play(FadeIn(tnote))
        self.wait(0.4)
        self.clear_scene()

    def precondition(self):
        k = load("krylov")
        rows_, cur = k["rows"], k["curves"]
        mid = rows_[1]
        head = label(r"Preconditioning", font_size=36).to_edge(UP, buff=0.3)
        ax = CornerAxes(x_range=[0, 400, 100], y_range=[-8, 0, 2], x_length=5.4, y_length=3.9, tips=False,
                        axis_config={"stroke_color": GREY_C})
        ax.move_to([-3.25, -0.25, 0])
        yt = log_ticks(ax, 0, (-8, -6, -4, -2, 0))
        xt = VGroup(*[label(rf"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(v, -8), DOWN, buff=0.1)
                      for v in (0, 100, 200, 300, 400)])
        xl = label(r"steps", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yl = label(rf"residual, \ {mid['n']:,} unknowns, \ computed", font_size=17, color=GREY_A).next_to(
            ax, UP, buff=0.12).align_to(ax, LEFT)

        def series(ys, color, every=1, upto=400):
            pts = [ax.c2p(i * every, max(-8, math.log10(v))) for i, v in enumerate(ys) if i * every <= upto]
            return VMobject(color=color, stroke_width=3).set_points_as_corners(pts)
        s_sd = series(cur["steepest"], NO, every=5)
        s_cg = series(cur["cg"], DATA)
        s_pc = series(cur["ssor"], YES)
        l_sd = label(rf"steepest: \ {mid['steepest']:,} steps", font_size=17, color=NO).next_to(
            ax.c2p(400, math.log10(cur["steepest"][80])), UP, buff=0.15).align_to(ax.c2p(400, 0), RIGHT)
        l_cg = label(rf"CG: \ {mid['cg']} steps", font_size=17, color=DATA).move_to(ax.c2p(150, -5.6),
                                                                                    aligned_edge=LEFT)
        l_pc = label(rf"CG with SSOR: \ {mid['ssor_cg']} steps", font_size=17, color=YES).move_to(
            ax.c2p(150, -6.6), aligned_edge=LEFT)
        cols = {r"M^{-1}": HEAD}
        rows = VGroup(
            cmath(r"M^{-1}", r"A x", r"=", r"M^{-1}", r"b", colors=cols, font_size=34),
            cmath(r"\kappa(", r"M^{-1}", r"A)", r"\ll", r"\kappa(A)", colors=cols, font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([3.0, 1.6, 0])
        whys = VGroup(label(r"the same solution", font_size=18, color=GREY_B),
                      label(r"if $M \approx A$ \ and $M$ is cheap to solve with", font_size=18, color=GREY_B))
        for wy, r in zip(whys, rows):
            wy.next_to(r, DOWN, buff=0.08).align_to(r, LEFT)
        trs = [[r"none", *[f"{r['cg']}" for r in rows_]],
               [r"Jacobi, \ $M = \operatorname{diag}(A)$", *[f"{r['jacobi_cg']}" for r in rows_]],
               [r"SSOR, \ $\omega = 1.5$", *[f"{r['ssor_cg']}" for r in rows_]]]
        tab = grid_table([r"preconditioner", *[f"{r['n']:,}" for r in rows_]], trs, widths=[2.9, 0.95, 0.95, 0.95],
                         row_h=0.46, font_size=18, mono_cols=())
        tab.next_to(whys[1], DOWN, buff=0.5).set_x(3.75)
        for c in tab.cells[3][1:]:
            c.set_color(YES)
        tnote = wrapped_label(r"CG steps by number of unknowns; \ the Poisson diagonal is all fours, \ so Jacobi "
                              r"changes nothing", 5.6, font_size=17, color=GREY_A).next_to(tab, DOWN, buff=0.2)
        with self.voiceover(
            "Since the cost depends on kappa, change kappa. <bookmark mark='a'/> Multiply the system by the "
            "inverse of a matrix M that resembles A but is cheap to solve with. The solution is unchanged, and if "
            "M is a good imitation, M inverse A has a much smaller condition number. <bookmark mark='b'/> The "
            "simplest choice, A's own diagonal, does nothing here: the Poisson matrix has fours all along its "
            "diagonal, and the step counts are identical. <bookmark mark='c'/> Symmetric successive over-"
            f"relaxation, two triangular sweeps, cuts {mid['cg']} steps to {mid['ssor_cg']}, and "
            f"{rows_[2]['cg']} to {rows_[2]['ssor_cg']}. <bookmark mark='d'/> Incomplete Cholesky factors do "
            "better still, and chapter nine's multigrid can make the count independent of the grid."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(xl), FadeIn(yl))
            self.play(Create(s_sd), FadeIn(l_sd), Create(s_cg), FadeIn(l_cg), run_time=2)
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])), FadeIn(VGroup(*tab.cells[1])),
                      FadeIn(VGroup(*tab.cells[2])), FadeIn(tnote))
            vo.wait_until("c")
            self.play(Create(s_pc), FadeIn(l_pc), FadeIn(VGroup(*tab.cells[3])), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def gmres(self):
        g = load("gmres")
        res = g["residuals"]
        head = label(r"Without symmetry: \ GMRES", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"\tilde H_k": KERN, r"Q_k": DATA, r"Q_{k+1}": DATA}
        rows = VGroup(
            cmath(r"A", r"Q_k", r"=", r"Q_{k+1}", r"\tilde H_k", colors=cols, font_size=34),
            cmath(r"x_k", r"=", r"Q_k", r"y", colors=cols, font_size=34),
            cmath(r"\|b - A x_k\|", r"=", r"\|\beta e_1 - ", r"\tilde H_k", r"y\|", colors=cols, font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.75).move_to([-3.6, 0.4, 0])
        whys = VGroup(
            wrapped_label(r"Arnoldi \ (1951): \ an orthonormal basis of $\mathcal{K}_k$ by modified Gram--Schmidt "
                          r"\ (Chapter 4); \ $\tilde H_k$ is Hessenberg \ (Chapter 6)", 5.8, font_size=18,
                          color=GREY_B),
            label(r"look for $x$ in that space", font_size=18, color=GREY_B),
            wrapped_label(r"$Q_{k+1}$ keeps lengths: \ a small $(k+1) \times k$ least-squares problem, \ solved with "
                          r"Givens rotations", 5.8, font_size=18, color=GREY_B),
        )
        for wy, r in zip(whys, rows):
            wy.next_to(r, DOWN, buff=0.12).align_to(r, LEFT)
        ax = CornerAxes(x_range=[0, 90, 10], y_range=[-8, 0, 2], x_length=4.8, y_length=3.6, tips=False,
                        axis_config={"stroke_color": GREY_C})
        ax.move_to([3.9, 0.2, 0])
        yt = log_ticks(ax, 0, (-8, -6, -4, -2, 0))
        xt = VGroup(*[label(rf"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(v, -8), DOWN, buff=0.1)
                      for v in (0, 30, 60, 90)])
        xl = label(r"steps", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yl = label(r"relative residual, \ computed", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(
            ax, LEFT)
        curve = VMobject(color=KERN, stroke_width=3).set_points_as_corners(
            [ax.c2p(i + 1, max(-8.2, math.log10(v))) for i, v in enumerate(res)])
        cl = wrapped_label(rf"convection--diffusion, \ 1{{,}}024 unknowns, \ not symmetric: \ $10^{{-8}}$ in "
                           rf"{g['iterations']} steps", 4.6, font_size=18, color=KERN).next_to(xl, DOWN, buff=0.25)
        foot = wrapped_label(r"the price is memory: \ every basis vector is kept, \ so long runs are restarted every "
                             r"$m$ steps, \ GMRES($m$)", 12.4, font_size=20, color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Conjugate gradients needs a symmetric matrix. Add a flow, convection as well as diffusion, and "
            "symmetry is lost. <bookmark mark='a'/> GMRES, by Yousef Saad and Martin Schultz in 1986, builds an "
            "orthonormal basis of the Krylov space with Arnoldi's process, which is chapter four's modified "
            "Gram–Schmidt. A times the basis is the next basis times a small Hessenberg matrix, chapter six's "
            "shape. <bookmark mark='b'/> It looks for x in that space, <bookmark mark='c'/> and minimizes the "
            "residual through a small least-squares problem, solved with Givens rotations. <bookmark mark='d'/> "
            "On our nonsymmetric problem of a thousand and twenty-four unknowns, it reaches ten to the minus "
            f"eight in {g['iterations']} steps. <bookmark mark='e'/> The price is memory: every basis vector is "
            "kept, so long runs are restarted."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(xl), FadeIn(yl))
            self.play(Create(curve), FadeIn(cl), run_time=2)
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, HEAD, LAM)
