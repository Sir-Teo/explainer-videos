from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs52.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES


def tile(content, caption, color, TW=3.6, TH=2.3):
    frame = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                             stroke_width=1.5, fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(frame.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(frame.get_bottom() + UP * 0.3)
    return Group(frame, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        head = label(rf"Part {PART}: \ Computing with Real Numbers", font_size=34).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"\kappa = \|A\|\,\|A^{-1}\|", font_size=46, color=HEAD), r"conditioning", HEAD),
            tile(MathTex(r"PA = LU", font_size=56, color=YES), r"stable elimination", YES),
            tile(MathTex(r"H = I - 2vv^{\mathsf T}", font_size=46, color=DATA), r"mirrors and QR", DATA),
            tile(MathTex(r"\left(\tfrac{\sqrt\kappa - 1}{\sqrt\kappa + 1}\right)^{k}", font_size=46, color=KERN),
                 r"conjugate gradients", KERN),
            tile(MathTex(r"z \mapsto z - \tfrac{z^3 - 1}{3z^2}", font_size=44, color=LAM), r"Newton's fractal", LAM),
            tile(label(r"leapfrog keeps energy", font_size=34, color=NO), r"geometric integration", NO),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. The condition number, which says how hard a problem is, separate from "
            "backward stability, which says how good an algorithm is, and the rule that joins them: forward error "
            "is at most the condition number times the backward error. Elimination made stable by pivoting; "
            "Householder's mirrors and the SVD; the QR algorithm, converging cubically; conjugate gradients, "
            "multigrid and sparse orderings for systems with millions of unknowns; Newton's method and its fractal; "
            "Chebyshev points, Gauss quadrature, stiff solvers and symplectic integrators. One idea runs through it: "
            "with rounding everywhere, the right question is not whether an answer is exact, but whether it is the "
            "exact answer to a nearby problem."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"linear algebra on light: \ transforms and solvers", [51]),
            (r"unitary matrices and quantum gates", [53]),
            (r"proving numerical code correct", [54]),
            (r"spectra of graphs", [56]),
            (r"optimization and learning theory", [57]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 51's renderer is linear algebra and integration, done billions of times a "
            "second. Part 53's quantum computer is a unitary matrix acting on a vector. Part 54 proves programs "
            "correct, floating point included. Part 56 reads a graph through the eigenvalues of its matrix. And "
            "Part 57's learning theory rests on the same optimization."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"solve", r"never invert a matrix to solve a system; \ factor it, \ with pivoting"),
            (r"fit", r"least squares by QR or the SVD, \ not the normal equations"),
            (r"check", r"estimate the condition number; \ report residuals, \ not only answers"),
            (r"scale", r"sparse and iterative methods, \ with a preconditioner, \ for big systems"),
            (r"speed", r"call BLAS and LAPACK; \ write matrix multiplication only to learn it"),
        ])
        with self.voiceover(
            "In practice. Never invert a matrix to solve a system: factor it, with pivoting. Fit least squares with "
            "QR or the SVD, not the normal equations. Estimate the condition number and report residuals, not only "
            "answers. Use sparse and iterative methods, with a good preconditioner, for big systems. And call BLAS "
            "and LAPACK: write your own matrix multiplication only to learn how it works."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that the relative condition number of $f(x) = x - 1$ is $|x|/|x - 1|$, \ and explain catastrophic "
            r"cancellation with it.",
            r"Prove that partial pivoting's growth factor is at most $2^{n-1}$, \ and that Wilkinson's matrix "
            r"attains it.",
            r"Show that classical Gram--Schmidt and modified Gram--Schmidt are equal in exact arithmetic, \ and give "
            r"a $3 \times 3$ example where they differ in floating point.",
            r"Derive CG's bound $2\left((\sqrt\kappa - 1)/(\sqrt\kappa + 1)\right)^k$ from Chebyshev polynomials.",
            r"\textit{Build.} \ Write a two-grid solver for the 1D Poisson problem, \ and measure its convergence "
            r"factor against $n$.",
            r"$\bigstar$ \textit{Research.} \ Polynomial smoothed growth for elimination with partial pivoting.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: a two-grid solver for the one-dimensional Poisson problem, whose convergence factor should not "
            "depend on the size of the grid. The last, marked with a star, is a research problem: prove that "
            "partial pivoting's growth is polynomial once the matrix is perturbed by a little noise."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 53, \ Quantum Computation", font_size=40).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"a qubit as a unit vector in $\mathbb{C}^2$", HEAD),
            (r"gates as unitary matrices", YES),
            (r"interference: \ Deutsch--Jozsa and Grover", DATA),
            (r"Shor's algorithm and the end of RSA", LAM))]).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Next time, Part 53: quantum computation. A qubit is a unit vector in a two-dimensional complex space, "
            "a gate is a unitary matrix, and a computation is a product of them, linear algebra again. Interference "
            "makes wrong answers cancel, and one algorithm built on it, Shor's, would end the public-key "
            "cryptography of Part 30."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Trefethen and Bau, \ \textit{Numerical Linear Algebra}; \ Golub and Van Loan, \ \textit{Matrix "
             r"Computations}",
             r"Higham, \ \textit{Accuracy and Stability of Numerical Algorithms}; \ Saad, \ \textit{Iterative "
             r"Methods}; \ Briggs et al., \ \textit{A Multigrid Tutorial}"],
            [r"Wilkinson \ (1963, \ 1965); \ Francis \ (1961); \ Hestenes and Stiefel \ (1952)",
             r"Trefethen and Schreiber \ (1990); \ Halko, \ Martinsson and Tropp \ (2011)",
             r"Trefethen, \ \textit{Approximation Theory and Approximation Practice}; \ Hairer, \ Lubich and Wanner",
             r"Dongarra and Sullivan \ (2000); \ Carson and Higham \ (2018)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(2.0)


_ = (NO, YES, KERN, LAM, DATA)
