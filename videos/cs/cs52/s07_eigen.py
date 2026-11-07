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


def mag_color(v: float):
    """Bright yellow for entries of size one or more, fading to the background at 10^-16 (log scale)."""
    a = min(1.0, max(0.0, (math.log10(max(v, 1e-300)) + 16) / 16))
    return interpolate_color(ManimColor(BG), ManimColor(HEAD), a)


def tri_grid(n=8, cell=0.42):
    """An n x n matrix drawn as cells: the diagonal tinted, the two off-diagonals coloured by size later."""
    g = VGroup()
    cells = {}
    for i in range(n):
        for j in range(n):
            sq = Square(side_length=cell, stroke_color=GREY_D, stroke_width=1, fill_color=BG, fill_opacity=1)
            sq.move_to([j * cell, -i * cell, 0])
            if i == j:
                sq.set_fill(LAM, opacity=0.55)
            cells[(i, j)] = sq
            g.add(sq)
    g.cells = cells
    return g


def colour_bar(cell=0.3):
    sw = VGroup(*[Square(side_length=cell, stroke_width=0, fill_color=mag_color(10.0 ** -p), fill_opacity=1)
                  for p in range(0, 17, 2)]).arrange(RIGHT, buff=0)
    sw.add(SurroundingRectangle(sw, buff=0, color=GREY_D, stroke_width=1))
    ends = VGroup(MathTex(r"10^{0}", font_size=20, color=GREY_B).next_to(sw, LEFT, buff=0.1),
                  MathTex(r"10^{-16}", font_size=20, color=GREY_B).next_to(sw, RIGHT, buff=0.1))
    return VGroup(sw, ends)


def log_ticks(ax, x0, ys, size=20):
    return VGroup(*[MathTex(rf"10^{{{p}}}", font_size=size, color=GREY_B).next_to(ax.c2p(x0, p), LEFT, buff=0.1)
                    for p in ys])


class Eigen(VoiceoverScene):
    def construct(self):
        self.card()
        self.noformula()
        self.power()
        self.qralg()
        self.shifts()
        self.cubic()

    def card(self):
        card = chapter_card(6, r"Eigenvalues: \ the QR algorithm",
                            r"How do we find eigenvalues when no formula exists?",
                            lit=(1824, 1961), extra=((1824, r"Abel: \ no formula for degree five"),
                                                     (1961, r"Francis; \ Kublanovskaya: \ QR")), part=PART)
        with self.voiceover("Chapter six. Eigenvalues, and the QR algorithm."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def noformula(self):
        q = load("qr")
        lam = q["true"]
        head = label(r"No formula, \ so iterate", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"\lambda": HEAD}
        rows = VGroup(
            cmath(r"A v", r"=", r"\lambda", r"v", colors=cols, font_size=36),
            cmath(r"(A - ", r"\lambda", r"I)\, v", r"=", r"0", colors=cols, font_size=36),
            cmath(r"\det(A - ", r"\lambda", r"I)", r"=", r"0", colors=cols, font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([-3.9, 1.0, 0])
        whys = VGroup(label(r"a direction that $A$ only stretches", font_size=18, color=GREY_B),
                      label(r"$A - \lambda I$ sends $v \ne 0$ to zero: \ singular", font_size=18, color=GREY_B),
                      label(r"a polynomial of degree $n$ in $\lambda$", font_size=18, color=GREY_B))
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.12).align_to(r, LEFT)
        facts = VGroup(
            wrapped_label(r"Abel \ (1824): \ no formula in radicals solves the general polynomial of degree five or "
                          r"more", 5.8, font_size=19, color=NO),
            wrapped_label(r"every polynomial is $\det(C - \lambda I)$ for its companion matrix $C$: \ so no finite "
                          r"recipe finds eigenvalues either; \ every eigenvalue algorithm iterates", 5.8, font_size=19,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(whys[2], DOWN, buff=0.45).align_to(rows, LEFT)
        ax = Axes(x_range=[-8, 5, 1], y_range=[-7, 7, 7], x_length=5.6, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False})
        ax.move_to([3.5, -0.3, 0])
        xt = VGroup(*[label(rf"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.12)
                      for v in (-6, -3, 3)])
        lam_ = np.linspace(-7.9, 4.8, 500)
        p = np.prod(lam_[:, None] - np.array(lam)[None, :], axis=1)
        y = np.sign(p) * np.log10(1 + np.abs(p))
        curve = VMobject(color=DATA, stroke_width=3).set_points_as_corners(
            [ax.c2p(a, b) for a, b in zip(lam_, y)])
        roots = VGroup(*[Dot(ax.c2p(r_, 0), radius=0.07, color=HEAD) for r_ in lam])
        cap = label(r"$\det(A - \lambda I)$ for our symmetric $8 \times 8$ matrix", font_size=18,
                    color=GREY_A).next_to(ax, UP, buff=0.15)
        cap2 = note(r"signed log scale; \ the dots are its computed eigenvalues", font_size=16).next_to(
            ax, DOWN, buff=0.45)
        with self.voiceover(
            "An eigenvector is a direction that a matrix only stretches: A v equals lambda v. "
            "<bookmark mark='a'/> Move everything to one side. A minus lambda I sends v to zero, so it is singular, "
            "and its determinant vanishes. <bookmark mark='b'/> That determinant is a polynomial of degree n, and "
            "the eigenvalues are its roots: here, the eight roots for a random symmetric eight by eight matrix. "
            "<bookmark mark='c'/> Niels Henrik Abel proved in 1824 that no formula in radicals solves the general "
            "polynomial of degree five. <bookmark mark='d'/> And every polynomial is the characteristic polynomial "
            "of some matrix, its companion matrix. So no finite recipe finds eigenvalues in general: every "
            "eigenvalue algorithm must iterate."
        ) as vo:
            self.play(FadeIn(head), Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("a")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xt), FadeIn(cap))
            self.play(Create(curve), run_time=2)
            self.play(LaggedStart(*[GrowFromCenter(r_) for r_ in roots], lag_ratio=0.15), FadeIn(cap2))
            vo.wait_until("c")
            self.play(FadeIn(facts[0]))
            vo.wait_until("d")
            self.play(FadeIn(facts[1]))
        self.wait(0.4)
        self.clear_scene()

    def power(self):
        q = load("qr")
        pe, ie = q["power"]["errors"], q["inverse"]["errors"]
        lam = sorted(q["true"], key=abs, reverse=True)
        ratio = abs(lam[1] / lam[0])
        kp = next(k for k, e in enumerate(pe) if e < 1e-13) + 1
        ki = next(k for k, e in enumerate(ie) if e < 1e-13) + 1
        head = label(r"Power iteration, \ and inverse iteration", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"\lambda_1^k": HEAD, r"\left(\frac{\lambda_2}{\lambda_1}\right)^{k}": YES}
        rows = VGroup(
            cmath(r"x_0", r"=", r"c_1 v_1", r"+", r"c_2 v_2", r"+", r"\cdots", colors=cols, font_size=32),
            cmath(r"A^k x_0", r"=", r"c_1", r"\lambda_1^k", r"v_1", r"+", r"c_2", r"\lambda_2^k", r"v_2", r"+",
                  r"\cdots", colors=cols, font_size=32),
            cmath(r"A^k x_0", r"=", r"\lambda_1^k", r"\Big(", r"c_1", r"v_1", r"+", r"c_2",
                  r"\left(\frac{\lambda_2}{\lambda_1}\right)^{k}", r"v_2", r"+", r"\cdots", r"\Big)", colors=cols,
                  font_size=32),
            cmath(r"(A - \mu I)^{-1}", r"\ \text{has eigenvalues}\ ", r"\frac{1}{\lambda_i - \mu}", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([-3.5, 0.2, 0])
        rows[3][2].set_color(LAM)
        whys = VGroup(label(r"write the start in eigenvectors", font_size=18, color=GREY_B),
                      label(r"each component is multiplied by $\lambda_i^k$", font_size=18, color=GREY_B),
                      label(r"the others die like a ratio to the $k$", font_size=18, color=YES),
                      label(r"the eigenvalue nearest the shift $\mu$ dominates", font_size=18, color=LAM))
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.1).align_to(r, LEFT)
        ax = CornerAxes(x_range=[0, 60, 10], y_range=[-16, 1, 4], x_length=4.6, y_length=4.2, tips=False,
                        axis_config={"stroke_color": GREY_C})
        ax.move_to([4.2, -0.2, 0])
        yt = log_ticks(ax, 0, (-16, -12, -8, -4, 0))
        xt = VGroup(*[label(rf"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(v, -16), DOWN, buff=0.1)
                      for v in (0, 20, 40, 60)])
        xl = label(r"steps", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yl = label(r"eigenvalue error, \ computed", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(
            ax, LEFT)

        def series(es, color):
            pts = [ax.c2p(k + 1, math.log10(e)) for k, e in enumerate(es)]
            return VMobject(color=color, stroke_width=3).set_points_as_corners(pts)
        sp, si = series(pe, YES), series(ie, LAM)
        kpl = label(rf"power: \ $|\lambda_2/\lambda_1| = {ratio:.2f}$; \ {kp} steps to $10^{{-13}}$", font_size=17,
                    color=YES).next_to(ax.c2p(60, 0.5), DOWN, buff=0.1).align_to(ax.c2p(60, 0), RIGHT)
        kil = label(rf"inverse, \ shift 0.3 away: \ {ki} steps", font_size=17, color=LAM).next_to(
            ax.c2p(14, -14.5), RIGHT, buff=0.05)
        with self.voiceover(
            "The simplest iteration is the power method. <bookmark mark='a'/> Write a starting vector in terms of "
            "the eigenvectors. <bookmark mark='b'/> Multiplying by A k times multiplies each component by its "
            "eigenvalue to the k. <bookmark mark='c'/> Factor out the largest: every other component shrinks like "
            "a ratio to the k. Here the ratio is about two thirds, and the error reaches ten to the minus "
            f"thirteen after {kp} steps. <bookmark mark='d'/> Inverse iteration uses the inverse of A minus a "
            "shift, mu, whose eigenvalues are one over lambda minus mu, so the eigenvalue nearest the shift "
            f"dominates overwhelmingly. With a shift nought point three away, {ki} steps suffice, each a linear "
            "solve with chapter three's factors."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            self.play(Create(sp), FadeIn(kpl), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(whys[3]))
            self.play(Create(si), FadeIn(kil), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def qralg(self):
        q = load("qr")
        un = q["unshifted"]
        snaps = un["snapshots"]
        head = label(r"The QR algorithm", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"Q_k": DATA, r"Q_k^{\mathsf T}": DATA, r"R_k": LAM}
        rows = VGroup(
            cmath(r"A_k", r"=", r"Q_k", r"R_k", colors=cols, font_size=36),
            cmath(r"R_k", r"=", r"Q_k^{\mathsf T}", r"A_k", colors=cols, font_size=36),
            cmath(r"A_{k+1}", r"=", r"R_k", r"Q_k", colors=cols, font_size=36),
            cmath(r"A_{k+1}", r"=", r"Q_k^{\mathsf T}", r"A_k", r"Q_k", colors=cols, font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([-4.0, 0.3, 0])
        whys = VGroup(label(r"factor \ (Chapter 4)", font_size=18, color=GREY_B),
                      label(r"$Q_k$ is orthogonal", font_size=18, color=GREY_B),
                      label(r"multiply in the other order", font_size=18, color=GREY_B),
                      label(r"a similarity: \ the same eigenvalues", font_size=18, color=YES))
        for w, r in zip(whys, rows):
            w.next_to(r, RIGHT, buff=0.4)
        x0 = max(w.get_left()[0] for w in whys)
        for w in whys:
            w.align_to([x0, 0, 0], LEFT)
        grid = tri_grid()
        grid.move_to([3.9, 0.15, 0])
        for i in range(7):
            for c in ((i + 1, i), (i, i + 1)):
                grid.cells[c].set_fill(mag_color(1.0))
        cb = colour_bar().next_to(grid, DOWN, buff=0.35)
        it = Integer(0, font_size=26, color=WHITE)
        itl = label(r"iteration", font_size=20, color=GREY_A)
        ctr = VGroup(itl, it).arrange(RIGHT, buff=0.15).next_to(grid, UP, buff=0.25)
        gcap = wrapped_label(r"our symmetric $8 \times 8$ matrix, \ already tridiagonal; \ off-diagonal entries "
                             r"coloured by size, \ computed", 4.4, font_size=17, color=GREY_A).next_to(cb, DOWN,
                                                                                                    buff=0.2)
        tot = label(rf"all eight eigenvalues: \ {un['iterations']} iterations", font_size=19, color=NO).next_to(
            rows, DOWN, buff=0.6).align_to(rows, LEFT)
        with self.voiceover(
            "In 1961 John Francis in England and, independently, Vera Kublanovskaya in the Soviet Union found the "
            "algorithm still used today. <bookmark mark='a'/> Factor the matrix as Q times R. <bookmark "
            "mark='b'/> Since Q is orthogonal, R is Q transposed A. <bookmark mark='c'/> Now multiply the factors "
            "in the other order. <bookmark mark='d'/> The result is Q transposed A Q, a similarity, so the "
            "eigenvalues are unchanged: it is the power method applied to a whole basis at once. <bookmark "
            "mark='e'/> Repeat, and the matrix creeps towards diagonal form, the eigenvalues appearing on its "
            "diagonal. Coloured by size on a log scale, our matrix's last off-diagonal entry fades to ten to the "
            f"minus fifteen in forty iterations. Finishing all eight takes {un['iterations']}."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(FadeIn(grid), FadeIn(cb), FadeIn(ctr), FadeIn(gcap))
            for k, sn in enumerate(snaps):
                anims = []
                for i, v in enumerate(sn):
                    for c in ((i + 1, i), (i, i + 1)):
                        anims.append(grid.cells[c].animate.set_fill(mag_color(v)))
                self.play(*anims, ChangeDecimalToValue(it, k + 1), run_time=0.14)
            self.play(FadeIn(tot))
        self.wait(0.4)
        self.clear_scene()

    def shifts(self):
        q = load("qr")
        sh = q["shifted"]
        head = label(r"Hessenberg form, \ shifts, \ deflation", font_size=36).to_edge(UP, buff=0.3)
        pats = [pattern(["xxxx"] * 4, size=40), pattern(["xxxx", "xxxx", "0xxx", "0xxx"], size=40),
                pattern(["xxxx", "xxxx", "0xxx", "00xx"], size=40, color=YES)]
        for pt in pats:
            pt.scale_to_fit_width(1.5)
        steps = VGroup(pats[0], MathTex(r"\xrightarrow{H_1}", font_size=28), pats[1],
                       MathTex(r"\xrightarrow{H_2}", font_size=28), pats[2])
        steps.arrange(RIGHT, buff=0.1).move_to([-3.6, 1.75, 0])
        hcap = wrapped_label(r"each mirror applied on both sides, \ $H A H$, \ keeps the eigenvalues; \ a "
                             r"symmetric matrix becomes tridiagonal; \ each QR step then costs $O(n^2)$ by Givens "
                             r"rotations, \ not $O(n^3)$", 6.0,
                             font_size=17, color=GREY_A).next_to(steps, DOWN, buff=0.2)
        cols = {r"\mu_k": HEAD}
        rows = VGroup(
            cmath(r"A_k", r"-", r"\mu_k", r"I", r"=", r"Q_k R_k", colors=cols, font_size=32),
            cmath(r"A_{k+1}", r"=", r"R_k Q_k", r"+", r"\mu_k", r"I", colors=cols, font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(hcap, DOWN, buff=0.45).align_to(hcap, LEFT)
        scap = wrapped_label(r"$\mu_k$: \ Wilkinson's shift, \ the eigenvalue of the trailing $2 \times 2$ block "
                             r"nearer its corner", 6.0, font_size=17, color=HEAD).next_to(rows, DOWN, buff=0.15)
        scap.align_to(rows, LEFT)
        dcap = wrapped_label(r"\textbf{deflate}: \ when the last subdiagonal entry is negligible, \ its eigenvalue "
                             r"is found; \ carry on with the smaller block", 6.0, font_size=17, color=YES).next_to(
            scap, DOWN, buff=0.25).align_to(rows, LEFT)
        cell = 0.42
        grid = tri_grid(cell=cell)
        grid.move_to([3.9, 0.1, 0])
        for i in range(7):
            for c in ((i + 1, i), (i, i + 1)):
                grid.cells[c].set_fill(mag_color(1.0))
        tl = grid.cells[(0, 0)].get_corner(UL)

        def block(m):
            r = Rectangle(width=m * cell, height=m * cell, stroke_color=HEAD, stroke_width=3)
            return r.move_to(tl + np.array([m * cell / 2, -m * cell / 2, 0]))
        act = block(8)
        it = Integer(0, font_size=26, color=WHITE)
        ctr = VGroup(label(r"iteration", font_size=20, color=GREY_A), it).arrange(RIGHT, buff=0.15).next_to(
            grid, UP, buff=0.25)
        cb = colour_bar().next_to(grid, DOWN, buff=0.35)
        gcap = label(r"yellow frame: \ the block still being iterated", font_size=17, color=HEAD).next_to(
            cb, DOWN, buff=0.2)
        res = label(rf"all eight: \ {sh['iterations']} iterations, \ not {q['unshifted']['iterations']}",
                    font_size=21, color=YES).next_to(gcap, DOWN, buff=0.25)
        with self.voiceover(
            "Three refinements make it fast. <bookmark mark='a'/> First, reduce the matrix once, with Householder "
            "mirrors on both sides, to Hessenberg form, zero below the first subdiagonal; a symmetric matrix "
            "becomes tridiagonal. The QR algorithm keeps this shape, and each step then costs n squared with "
            "Givens rotations, not n cubed. <bookmark mark='b'/> Second, shift: subtract a guess at an eigenvalue "
            "before factoring, and add it back after. James Wilkinson's shift is an eigenvalue of the bottom two "
            "by two block. <bookmark mark='c'/> Third, deflate: when the last subdiagonal entry is negligible, "
            "the bottom eigenvalue is found, and the iteration carries on with a smaller matrix. <bookmark "
            f"mark='d'/> With all three, our eight eigenvalues take {sh['iterations']} iterations instead of "
            f"{q['unshifted']['iterations']}."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            self.play(FadeIn(steps[1]), FadeIn(steps[2]))
            self.play(FadeIn(steps[3]), FadeIn(steps[4]), FadeIn(hcap))
            vo.wait_until("b")
            self.play(Write(rows[0]))
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(scap))
            vo.wait_until("c")
            self.play(FadeIn(dcap), FadeIn(grid), FadeIn(cb), FadeIn(ctr), Create(act), FadeIn(gcap))
            vo.wait_until("d")
            for k, (sn, tr) in enumerate(zip(sh["snapshots"], sh["trace"])):
                anims = []
                for i, v in enumerate(sn):
                    for c in ((i + 1, i), (i, i + 1)):
                        anims.append(grid.cells[c].animate.set_fill(mag_color(v)))
                self.play(*anims, ChangeDecimalToValue(it, k + 1), run_time=0.35)
                nxt = sh["trace"][k + 1]["m"] if k + 1 < len(sh["trace"]) else 1
                if nxt < tr["m"]:
                    m = tr["m"]
                    self.play(grid.cells[(m - 1, m - 1)].animate.set_fill(YES, opacity=0.8),
                              Transform(act, block(nxt)), run_time=0.3)
            self.play(grid.cells[(0, 0)].animate.set_fill(YES, opacity=0.8), FadeOut(act), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def cubic(self):
        q = load("qr")
        un, sh = q["unshifted"], q["shifted"]
        fb = sh["first_block"]
        orders = sh["orders"]
        head = label(r"Cubic convergence", font_size=36).to_edge(UP, buff=0.3)
        ax = CornerAxes(x_range=[0, 40, 10], y_range=[-42, 0, 7], x_length=5.4, y_length=4.6, tips=False,
                        axis_config={"stroke_color": GREY_C})
        ax.move_to([-3.3, -0.35, 0])
        yt = log_ticks(ax, 0, (-42, -28, -14, 0))
        xt = VGroup(*[label(rf"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(v, -42), DOWN, buff=0.1)
                      for v in (0, 10, 20, 30, 40)])
        xl = label(r"iteration", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yl = label(r"last subdiagonal entry of the active block, \ computed", font_size=17, color=GREY_A).next_to(
            ax, UP, buff=0.12).align_to(ax, LEFT)
        tol = DashedLine(ax.c2p(0, -14), ax.c2p(40, -14), color=GREY_B, stroke_width=1.5)
        toll = label(r"deflate", font_size=16, color=GREY_B).next_to(ax.c2p(40, -14), DOWN, buff=0.1).align_to(
            ax.c2p(40, 0), RIGHT)

        def series(trace, color, n):
            pts = [ax.c2p(t["iter"], max(-42, math.log10(t["sub"]))) for t in trace[:n]]
            return VGroup(VMobject(color=color, stroke_width=3).set_points_as_corners(pts),
                          *[Dot(p, radius=0.045, color=color) for p in pts])
        n8 = sum(1 for t in un["trace"] if t["m"] == un["trace"][0]["m"])   # the first block only
        su = series(un["trace"], NO, n8)
        ss = series(sh["trace"], YES, len(sh["trace"]))
        lu = label(r"no shift: \ a straight line, \ linear", font_size=17, color=NO).move_to(ax.c2p(29, -5))
        ls = label(r"Wilkinson's shift", font_size=17, color=YES).next_to(ax.c2p(17, -38), RIGHT, buff=0.05)
        cols = {r"|h_{k}|^{3}": HEAD}
        law = cmath(r"|h_{k+1}|", r"\approx", r"C\,", r"|h_{k}|^{3}", colors=cols, font_size=36)
        seq = MathTex(sci(fb[0]), r"\ \to\ ", sci(fb[1]), r"\ \to\ ", sci(fb[2]), font_size=28, color=YES)
        digs = label(r"correct digits: \ about " + ", \\ ".join(str(int(-math.log10(v))) for v in fb), font_size=19,
                     color=GREY_A)
        ords = label(rf"measured orders: \ {orders[0]:.2f} \ and \ {orders[1]:.2f}", font_size=21, color=HEAD)
        acc = wrapped_label(rf"largest error against LAPACK's eigenvalues: \ ${sci(sh['error'])}$ with shifts, \ "
                            rf"${sci(un['error'])}$ without", 5.6, font_size=19, color=WHITE)
        VGroup(law, seq, digs, ords, acc).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([3.5, 0.0, 0])
        with self.voiceover(
            "Here is why the shift matters. <bookmark mark='a'/> Without it, the last subdiagonal entry shrinks "
            "by a constant factor each step: a straight line on a log scale, linear convergence. <bookmark "
            "mark='b'/> With Wilkinson's shift it goes from eight times ten to the minus four, to four times ten "
            "to the minus twelve, to three times ten to the minus thirty-five. <bookmark mark='c'/> The number of "
            "correct digits roughly triples each time; the measured orders are about three point seven and three. "
            "That is cubic convergence, and Wilkinson proved in 1968 that, with his shift, the symmetric "
            "iteration always converges. <bookmark mark='d'/> The answers agree with LAPACK's to about ten to the "
            "minus fourteen. Nearly every eigenvalue you have ever been shown was computed this way."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(xl), FadeIn(yl), Create(tol),
                      FadeIn(toll))
            vo.wait_until("a")
            self.play(Create(su), FadeIn(lu), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(ss), FadeIn(ls), run_time=2)
            self.play(Write(law), FadeIn(seq))
            vo.wait_until("c")
            self.play(FadeIn(digs), FadeIn(ords))
            vo.wait_until("d")
            self.play(FadeIn(acc))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, KERN, LAM, NO, YES)
