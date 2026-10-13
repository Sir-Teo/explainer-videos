from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis10.common import load, plain_axes, square_axes


class SpectralTheorem(VoiceoverScene):
    def construct(self):
        self.card()
        self.resolution()
        self.proof()
        self.ergodic()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(8, r"The spectral theorem", r"In what sense is every normal operator diagonal?", lit=(1932,),
                            part=10)
        with self.voiceover("Chapter eight: the spectral theorem, the proof that uses every part of the series."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def resolution(self):
        d = load("pvm")
        lam, wts, x2 = d["lam"], d["weights"], float(d["x2"])
        ax = plain_axes([-1.5, 1.5, 0.5], [0, 9, 2], 7.0, 3.0, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([0, 0.6, 0])
        ticks = VGroup(*[Line(ax.c2p(l_, -0.15), ax.c2p(l_, 0.15), color=C.SPECTRUM, stroke_width=2) for l_ in lam])
        stems = VGroup(*[Line(ax.c2p(l_, 0), ax.c2p(l_, w_), color=C.MEASURE, stroke_width=4) for l_, w_ in zip(lam, wts)])
        tl = MathTex(r"\sigma(H): \ 50 \text{ eigenvalues}", font_size=22, color=C.SPECTRUM).next_to(ax.c2p(-1.5, 0), DOWN,
                                                                                                  buff=0.45).align_to(
            ax, LEFT)
        wl = MathTex(r"E_{x,x}(\{\lambda_i\}) = |\langle x, u_i\rangle|^2", font_size=26, color=C.MEASURE).next_to(ax, UP,
                                                                                                         buff=0.1)
        om = (-0.4, 0.3)
        inband = (lam >= om[0]) & (lam <= om[1])
        band = Rectangle(width=ax.c2p(om[1], 0)[0] - ax.c2p(om[0], 0)[0], height=ax.c2p(0, 9)[1] - ax.c2p(0, 0)[1],
                         stroke_color=C.EPS, stroke_width=2, fill_color=C.EPS, fill_opacity=0.08).move_to(
            ax.c2p(sum(om) / 2, 4.5))
        bl = MathTex(r"\omega", font_size=26, color=C.EPS).move_to(band.get_corner(UR) + np.array([-0.18, -0.25, 0]))  # inside
        Ew = float(wts[inband].sum())
        assert abs(wts.sum() - x2) < 1e-9 and wts.max() < 9  # every stem inside the axes
        rows = VGroup(
            label(r"\textbf{FA 12.17} \ a resolution of the identity: \ a projection $E(\omega)$ for each Borel set "
                  r"$\omega$,", font_size=22),
            label(r"$E(\sigma) = I$, \ $E(\omega \cap \omega') = E(\omega)E(\omega')$, \ countably additive", font_size=22),
            MathTex(rf"E_{{x,x}}(\omega) = \|E(\omega)x\|^2: \quad \text{{total}} = \|x\|^2 = {x2:.4f}, \quad "
                    rf"E_{{x,x}}(\omega) = {Ew:.4f}", font_size=24, color=C.MEASURE),
            MathTex(r"\langle Hx, x\rangle = \int \lambda\, dE_{x,x}(\lambda), \qquad H = \int \lambda\, dE(\lambda)",
                    font_size=28, color=C.EPS),
            label(r"for $M$: \ $E(\omega) = $ multiplication by $\mathbf 1_\omega$; \ for a compact $T$: \ the "
                  r"eigenprojections in $\omega$", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.25)
        for r_ in rows:
            if r_.width > 13:
                r_.width = 13
        head = label(r"Projection-valued measures", font_size=34).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Diagonalizing a symmetric matrix means splitting space into eigenspaces. Here are "
            "the fifty eigenvalues of a random symmetric matrix, on its spectrum. <bookmark mark='b'/> Pick a vector "
            "x. Its squared coordinates in the eigenbasis put a mass on each eigenvalue, and the masses add up to "
            "the squared length of x. <bookmark mark='c'/> For any set omega, the projection onto the eigenvectors "
            "with eigenvalues in omega, E of omega, carries exactly the mass over omega. That assignment of a "
            "projection to every set is a projection-valued measure. <bookmark mark='d'/> And H is the integral of "
            "lambda against it. For the multiplication operator, E of omega multiplies by the indicator of omega: no "
            "eigenvectors needed."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), LaggedStart(*[Create(t_) for t_ in ticks], lag_ratio=0.02), FadeIn(tl))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(s_) for s_ in stems], lag_ratio=0.03), FadeIn(wl), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(band), FadeIn(bl), FadeIn(rows[:3]),
                      *[s_.animate.set_stroke(opacity=0.25) for s_, ok in zip(stems, inband) if not ok])
            vo.wait_until("d")
            self.play(FadeIn(rows[3:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def proof(self):
        parts = [(3, r"Stone--Weierstrass"), (5, r"Riesz representation"), (6, r"Hilbert space"),
                 (7, r"Liouville, Cauchy"), (8, r"Hahn--Banach, Alaoglu")]
        badges = VGroup()
        for p, nm in parts:
            box = RoundedRectangle(corner_radius=0.1, width=2.4, height=0.8, stroke_color=GREY_D, stroke_width=2)
            t = VGroup(label(rf"Part {p}", font_size=22), label(nm, font_size=16, color=GREY_B)).arrange(DOWN, buff=0.05)
            if t.width > 2.2:
                t.width = 2.2
            badges.add(VGroup(box, t.move_to(box)))
        badges.arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.35)
        pm = ProofMap([
            r"$\mathcal A$: \ the closed algebra generated by $I$, $T$, $T^*$: \ commutative, \ $C^*$",
            r"$\sigma$ nonempty and compact; \ $\Delta$ compact \ (Liouville; \ Alaoglu)",
            r"Gelfand--Naimark: \ $\mathcal A \cong C(\sigma(T))$ \ (Stone--Weierstrass)",
            r"$f \mapsto \langle f(T)x, y\rangle$ is a bounded functional on $C(\sigma(T))$",
            r"Riesz: \ it is $\int f\, d\mu_{x,y}$ \ for a complex measure $\mu_{x,y}$",
            r"$\langle E(\omega)x, y\rangle = \mu_{x,y}(\omega)$ defines projections \ (Hilbert space)",
        ], font_size=22, width=10.5, buff=0.1, direction=DOWN).move_to([0, 0.75, 0])
        uses = {0: [3], 1: [3, 4], 2: [0], 3: [], 4: [1], 5: [2]}
        thm = label(r"\textbf{FA 12.23} \ $T$ normal $\Rightarrow$ $T = \int_{\sigma(T)} \lambda\, dE(\lambda)$, \ $E$ "
                    r"unique, \ commuting with all that commutes with $T$", font_size=24, color=C.EPS).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Rudin's proof of the spectral theorem for a normal operator T uses the whole series. "
            "<bookmark mark='b'/> Take the algebra generated by T and its adjoint: commutative, and a C-star algebra. "
            "Its spectrum is compact and nonempty by Liouville, from Part 7, and its maximal ideal space is compact by "
            "Alaoglu, from Part 8. <bookmark mark='c'/> Gelfand-Naimark identifies it with the continuous functions on "
            "the spectrum, which needs Stone-Weierstrass, from Part 3. <bookmark mark='d'/> For two vectors x and y, "
            "f maps to f of T x against y: a bounded linear functional on continuous functions. By the Riesz "
            "representation theorem, from Part 5, it's integration against a measure. <bookmark mark='e'/> Those "
            "measures define the projections E of omega, in Hilbert space, from Part 6. And T is the integral of "
            "lambda d E."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm), FadeIn(pm), FadeIn(badges))
            for i, mk in zip(range(6), ("b", None, "c", "d", None, "e")):
                if mk:
                    vo.wait_until(mk)
                anims = list(pm.light(i))
                for j in uses[i]:
                    anims.append(badges[j][0].animate.set_stroke(C.CONNECTED_SET, 3).set_fill(C.CONNECTED_SET, 0.12))
                self.play(*anims, run_time=0.9)
            self.play(*pm.done())
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ergodic(self):
        d = load("pvm")
        ns, errs = d["ns"], d["errs"]
        ax = plain_axes([0, 4, 1], [-4, 1, 1], 5.6, 3.4, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.75, -0.5, 0])
        xl = MathTex(r"\log_{10} n", font_size=22).next_to(ax.c2p(4, 0), UR, buff=0.1)
        yl = MathTex(r"\log_{10}\Big\|\tfrac1n\sum_{k < n} U^k y - Py\Big\|", font_size=22).next_to(ax, UP, buff=0.1)
        dots = VGroup(*[Dot(ax.c2p(math.log10(n), math.log10(e)), radius=0.05, color=C.OPERATOR) for n, e in zip(ns, errs)])
        slope = np.polyfit(np.log10(ns[10:]), np.log10(errs[10:]), 1)[0]
        ref = DashedLine(ax.c2p(1, math.log10(errs[0]) - 1 + 0.6), ax.c2p(4, math.log10(errs[0]) - 4 + 0.6),
                         color=GREY_B, stroke_width=2)
        rl = MathTex(r"\propto 1/n", font_size=22, color=GREY_B).next_to(ax.c2p(3.2, math.log10(errs[0]) - 3.2 + 0.6), UR,
                                                                       buff=0.05)
        assert -1.3 < slope < -0.7 and errs[-1] < 1e-3
        cx = square_axes([-1.3, 1.3, 1], [-1.3, 1.3, 1], 0.75).move_to([5.4, 1.6, 0])
        circ = Circle(radius=cx.c2p(1, 0)[0] - cx.c2p(0, 0)[0], color=GREY_B, stroke_width=1.5).move_to(cx.c2p(0, 0))
        ph = d["ph"]
        eig = VGroup(*[Dot(cx.c2p(math.cos(p), math.sin(p)), radius=0.06,
                           color=C.EPS if abs(p) < 1e-12 else C.SPECTRUM) for p in ph])
        el = MathTex(r"\sigma(U)", font_size=22, color=C.SPECTRUM).next_to(cx, DOWN, buff=0.05)
        rows = VGroup(
            label(r"\textbf{FA 12.44} \ (von Neumann's ergodic theorem) \ $U$ unitary:", font_size=22),
            MathTex(r"\frac1n \sum_{k < n} U^k y \ \to \ Py, \quad P = E(\{1\}) \text{ (the fixed vectors)}", font_size=26,
                    color=C.EPS),
            label(r"proof: \ $\int \frac1n \sum_{k<n} \lambda^k\, dE(\lambda)$, \ and the averages of $\lambda^k$ are $0$ in "
                  r"the limit unless $\lambda = 1$", font_size=20, color=GREY_A),
            MathTex(rf"8 \times 8, \ \text{{2 fixed directions: slope }} {{{slope:.2f}}}", font_size=24),
            label(r"also from the calculus: \ square roots of positive operators, \ polar decomposition $T = U|T|$",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.4, -1.3, 0])
        for r_ in rows:
            if r_.width > 6.55:
                r_.width = 6.55
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to([0.3, -1.3, 0], RIGHT, buff=0)
        head = label(r"A payoff: \ averages of a unitary", font_size=34).to_edge(UP, buff=0.3)
        # the proof's picture, large: each eigenvalue's running average (1/n) sum_{k<n} lambda^k as n = 1 .. 60;
        # at lambda = 1 it stays 1, elsewhere it is (1 - lambda^n) / (n (1 - lambda)), which spirals into 0
        big = square_axes([-1.3, 1.3, 1], [-1.3, 1.3, 1], 1.5).move_to([-3.75, -0.6, 0])
        bcirc = Circle(radius=big.c2p(1, 0)[0] - big.c2p(0, 0)[0], color=GREY_B, stroke_width=1.5).move_to(big.c2p(0, 0))
        lams = np.exp(1j * np.asarray(ph))

        def avg(lam, n):
            return 1.0 + 0j if abs(lam - 1) < 1e-12 else (1 - lam ** n) / (n * (1 - lam))

        assert all(abs(avg(l_, 60) - np.mean(l_ ** np.arange(60))) < 1e-12 for l_ in lams)
        assert all(abs(avg(l_, 60)) < 2 / (60 * abs(1 - l_)) + 1e-12 for l_ in lams if abs(l_ - 1) > 1e-12)
        NN = np.arange(1, 61)
        tracks = VGroup(*[VMobject(stroke_color=C.EPS if abs(l_ - 1) < 1e-12 else C.SPECTRUM, stroke_width=1.6,
                                   stroke_opacity=0.7).set_points_as_corners(
            [big.c2p(avg(l_, n).real, avg(l_, n).imag) for n in NN] + ([big.c2p(1.0001, 0)] if abs(l_ - 1) < 1e-12 else []))
            for l_ in lams])
        nv = ValueTracker(1)
        movers = always_redraw(lambda: VGroup(*[Dot(big.c2p(avg(l_, max(1, round(nv.get_value()))).real,
                                                            avg(l_, max(1, round(nv.get_value()))).imag), radius=0.07,
                                                     color=C.EPS if abs(l_ - 1) < 1e-12 else C.SPECTRUM) for l_ in lams]))
        nrd = always_redraw(lambda: MathTex(rf"\tfrac1n \sum_{{k<n}} \lambda^k, \quad n = {max(1, round(nv.get_value()))}",
                                            font_size=26).next_to(big, UP, buff=0.1))
        bdots = VGroup(*[Dot(big.c2p(l_.real, l_.imag), radius=0.06, color=GREY_B) for l_ in lams])
        with self.voiceover(
            "<bookmark mark='a'/> One payoff. Average the powers of a unitary operator applied to a vector. "
            "<bookmark mark='b'/> In the spectral picture, that averages lambda to the k over the spectrum, which "
            "lies on the unit circle; the averages die everywhere except at lambda equal to one. So the averages "
            "converge to the projection onto the fixed vectors: von Neumann's ergodic theorem. "
            "<bookmark mark='c'/> For an eight by eight unitary with two fixed directions, the error falls like one "
            "over n."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[0]), Create(cx), Create(circ), FadeIn(eig), FadeIn(el))
            vo.wait_until("b")
            self.play(FadeIn(rows[1:3]), Create(bcirc), FadeIn(bdots), FadeIn(movers), FadeIn(nrd))
            self.play(nv.animate.set_value(60), Create(tracks), run_time=5.0, rate_func=linear)
            movers.clear_updaters()
            nrd.clear_updaters()
            vo.wait_until("c")
            self.play(FadeOut(VGroup(bcirc, bdots, movers, nrd, tracks)))
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(ref), FadeIn(rl))
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.05), FadeIn(rows[3]), run_time=2.0)
            self.play(FadeIn(rows[4]))
        self.wait(0.4)
        self.clear_scene()
