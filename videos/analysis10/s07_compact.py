from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis10.common import heatmap, load, plain_axes, polyline, square_axes


class CompactSelfAdjoint(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.peel()
        self.heat()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(6, r"Compact self-adjoint operators", r"Can an infinite matrix be diagonalized?", lit=(1907,),
                            part=10)
        with self.voiceover("Chapter six: the spectral theorem for compact self-adjoint operators, and the vibrating "
                            "string."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def theorem(self):
        ax = square_axes([0, 1, 0.5], [0, 1, 0.5], 3.4).move_to([-4.2, -0.3, 0])
        img = heatmap(lambda X, Y: np.minimum(X, Y) * (1 - np.maximum(X, Y)), (0, 1), (0, 1), 3.4, 3.4, -0.25, 0.25,
                      neg=C.SEQ, pos=C.OPERATOR).move_to(ax.c2p(0.5, 0.5))
        kl = MathTex(r"g(x, y) = \min(x, y)\,\big(1 - \max(x, y)\big)", font_size=24, color=C.OPERATOR).next_to(ax, UP,
                                                                                                         buff=0.1)
        gl = VGroup(MathTex(r"(Gf)(x) = \int_0^1 g(x, y) f(y)\,dy", font_size=22),
                    MathTex(r"-(Gf)'' = f, \ \ Gf(0) = Gf(1) = 0", font_size=22)).arrange(DOWN, buff=0.08).next_to(
            ax, DOWN, buff=0.15)
        pm = ProofMap([
            r"$m = \sup_{\|x\| = 1}|\langle Tx, x\rangle| = \|T\|$ \ (self-adjoint)",
            r"a maximizing sequence has a weak limit; \ $T$ compact makes $Tx_n$ converge",
            r"the maximum is attained: \ $Tx = \pm m\,x$, \ an eigenvector",
            r"restrict $T$ to $x^\perp$ \ (still compact, self-adjoint) \ and repeat",
            r"$|\lambda_1| \ge |\lambda_2| \ge \cdots \to 0$; \ the $u_n$ span $\overline{\operatorname{ran} T}$",
        ], font_size=20, width=6.6, buff=0.12, direction=DOWN).move_to([3.0, -0.2, 0])
        thm = MathTex(r"Tx = \sum_n \lambda_n \langle x, u_n\rangle\, u_n", font_size=32, color=C.EPS).to_edge(DOWN, buff=0.3).shift(
            RIGHT * 3.0)
        head = label(r"\textbf{FA 4.18--4.25, 12.29} \ compact and self-adjoint: \ an eigenbasis", font_size=30).to_edge(
            UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Here's the operator behind Part 8's string: integrate against this kernel, and you "
            "solve minus u double prime equals f with the ends held fixed. It's compact and self-adjoint. "
            "<bookmark mark='b'/> For such operators the finite-dimensional proof works. Maximize T x against x over "
            "unit vectors. A maximizing sequence has a weakly convergent subsequence, and compactness upgrades that "
            "to norm convergence, so the maximum is attained, at an eigenvector. <bookmark mark='c'/> Then restrict "
            "to the orthogonal complement and repeat. The eigenvalues shrink to zero and the eigenvectors span "
            "everything T can reach. <bookmark mark='d'/> T is diagonal in that basis."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(img), Create(ax), FadeIn(kl), FadeIn(gl))
            vo.wait_until("b")
            self.play(FadeIn(pm))
            for i in range(3):
                self.play(*pm.light(i), run_time=0.8)
            vo.wait_until("c")
            for i in (3, 4):
                self.play(*pm.light(i), run_time=0.8)
            vo.wait_until("d")
            self.play(*pm.done(), FadeIn(thm))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def peel(self):
        d = load("green")
        xc, iters, rq, w, exact = d["xc"], d["iters"], d["rq"], d["w"], d["exact"]
        ax = plain_axes([0, 1, 0.25], [-1.6, 1.6, 0.5], 6.0, 3.2).move_to([-3.3, -0.2, 0])
        cols = [C.FUNC, C.APPROX, C.FREQ]
        stage = ValueTracker(0)

        def cur():
            k = int(stage.get_value())
            m = k // 6
            g = VGroup()
            for j in range(m):  # modes already found, faint
                g.add(polyline(ax, xc, iters[6 * j + 5], color=cols[j], stroke_width=2, stroke_opacity=0.35))
            g.add(polyline(ax, xc, iters[k], color=cols[m], stroke_width=4))
            return g

        pic = always_redraw(cur)
        rd = always_redraw(lambda: MathTex(
            rf"\text{{mode }} {int(stage.get_value()) // 6 + 1}, \text{{ step }} {int(stage.get_value()) % 6 + 1}: \ "
            rf"\langle Gy, y\rangle = {rq[int(stage.get_value())]:.6f}", font_size=26).next_to(ax, UP, buff=0.12))
        tab = VGroup(MathTex(r"n", r"\quad \lambda_n \ (N = 2000)", r"\quad 1/(n\pi)^2", font_size=22, color=GREY_A))
        for n in range(6):
            tab.add(MathTex(f"{n + 1}", rf"\quad {w[n]:.8f}", rf"\quad {exact[n]:.8f}", font_size=22))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.6, 1.1, 0])
        for row in tab[1:]:
            row[1].align_to(tab[0][1], LEFT)
            row[2].align_to(tab[0][2], LEFT)
        assert np.allclose(w, exact, rtol=1e-4) and abs(rq[5] - exact[0]) < 1e-5
        rows = VGroup(
            label(r"eigenfunctions: \ $\sin(n\pi x)$, \ to $3 \times 10^{-4}$", font_size=22, color=C.EPS),
            label(r"so $-\frac{d^2}{dx^2}$, \ the inverse of $G$, \ has eigenvalues $(n\pi)^2$:", font_size=22),
            label(r"the Fourier sine series \ \emph{is} \ the spectral theorem for $-\frac{d^2}{dx^2}$", font_size=24,
                  color=C.SPECTRUM),
            label(r"the dictionary: \ diagonalize a symmetric matrix \ $\leftrightarrow$ \ this", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(tab, DOWN, buff=0.35)
        for r_ in rows:
            if r_.width > 6.4:
                r_.width = 6.4
        head = label(r"Peeling off the string's modes", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Watch the proof run. Start with a lopsided function and apply G again and again, "
            "normalizing each time. The largest mode wins: the curve settles into a half sine, and the Rayleigh "
            "quotient into one over pi squared. <bookmark mark='b'/> Now remove that mode and repeat: the next "
            "survivor is a full sine, with one over four pi squared. Then the third. <bookmark mark='c'/> With two "
            "thousand points, the eigenvalues match one over n pi squared to six digits. So minus the second "
            "derivative, the inverse of G, has eigenvalues n pi squared and eigenfunctions the sines: the Fourier "
            "sine series is the spectral theorem for this operator."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(pic), FadeIn(rd))
            for k in range(1, 6):
                self.play(stage.animate.set_value(k), run_time=0.6, rate_func=lambda t: 1.0 if t > 0.5 else 0.0)
            vo.wait_until("b")
            for k in range(6, 18):
                self.play(stage.animate.set_value(k), run_time=0.45, rate_func=lambda t: 1.0 if t > 0.5 else 0.0)
            vo.wait_until("c")
            self.play(FadeIn(tab[0]), LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.2), run_time=1.8)
            self.play(FadeIn(rows[:2]))
            self.play(FadeIn(rows[2:]))
        for m in (pic, rd):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heat(self):
        d = load("green")
        xh, ts, series, cn, err = d["xh"], d["ts"], d["series"], d["cn"], float(d["err_heat"])
        ax = plain_axes([0, 1, 0.25], [0, 1.1, 0.5], 6.4, 3.4, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.1, -0.4, 0])
        box = VGroup(Line(ax.c2p(0, 0), ax.c2p(0.2, 0), color=GREY_B, stroke_width=2),
                     Line(ax.c2p(0.2, 1), ax.c2p(0.5, 1), color=GREY_B, stroke_width=2),
                     Line(ax.c2p(0.5, 0), ax.c2p(1, 0), color=GREY_B, stroke_width=2))
        cols = [C.SEQ, C.APPROX, C.EPS, C.FREQ]
        gs = [polyline(ax, xh, s_, color=c, stroke_width=3.5) for s_, c in zip(series, cols)]
        ds = [VGroup(*[Dot(ax.c2p(a, b), radius=0.03, color=WHITE) for a, b in zip(xh[::16], c_[::16])]) for c_ in cn]
        tl = VGroup(*[MathTex(rf"t = {t_:g}", font_size=22, color=c) for t_, c in zip(ts, cols)]).arrange(
            RIGHT, buff=0.35).next_to(ax, UP, buff=0.12)
        assert err < 2e-3
        rows = VGroup(
            MathTex(r"u_t = u_{xx}: \quad u(x, t) = \sum_n b_n\, e^{-n^2\pi^2 t}\sin(n\pi x)", font_size=28),
            label(r"each mode decays at its own rate: \ the eigenvalue sets the clock", font_size=22, color=GREY_A),
            label(r"curves: \ the eigen-expansion (4000 modes); \ dots: \ Crank--Nicolson", font_size=22),
            MathTex(rf"\max |\text{{difference}}| = {sci(err, 1)} \ \ (t \ge 0.005)", font_size=24, color=C.EPS),
            label(r"the quantum videos' particle in a box: \ the same modes, \ with $e^{-iEt}$", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.6, -0.3, 0])
        for r_ in rows:
            if r_.width > 6.6:
                r_.width = 6.6
        head = label(r"Solving the heat equation by diagonalizing", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Diagonalizing solves equations. For the heat equation on the string, expand the "
            "initial temperature in the sines; each mode just decays, at a rate set by its eigenvalue. "
            "<bookmark mark='b'/> Here's a block of heat spreading out, from the eigen-expansion, <bookmark mark='c'/> "
            "with an independent finite-difference solver as dots, agreeing to about one part in a hundred thousand. "
            "<bookmark mark='d'/> In the quantum videos, the same modes rotate instead of decaying: that's the "
            "particle in a box."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[:2]), Create(ax), Create(box))
            vo.wait_until("b")
            for k in range(4):
                self.play(Create(gs[k]), FadeIn(tl[k]), run_time=0.9)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in ds], lag_ratio=0.3), FadeIn(rows[2:4]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.wait(0.4)
        self.clear_scene()
