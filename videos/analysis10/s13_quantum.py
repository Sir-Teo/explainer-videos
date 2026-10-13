from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis10.common import load, plain_axes


class QuantumClosure(VoiceoverScene):
    def construct(self):
        self.card()
        self.hydrogen()
        self.commutator()
        self.summary()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(12, r"What this proves about quantum mechanics", r"Which of the quantum videos' assumptions "
                                                                             r"are now theorems?", lit=(1932,), part=10)
        with self.voiceover("Chapter twelve: what the series has proved about quantum mechanics."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def hydrogen(self):
        d = load("hydrogen")
        bound, cont = d["bound"], d["cont"]
        ax = plain_axes([0, 1, 1], [-0.55, 0.06, 0.1], 3.2, 5.6, numbers=True, font_size=16,
                        x_axis_config={"include_numbers": False},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-4.6, -0.4, 0])
        lev = VGroup(*[Line(ax.c2p(0.05, e), ax.c2p(0.95, e), color=C.SPECTRUM, stroke_width=3) for e in bound[:6]])
        band = Rectangle(width=ax.c2p(0.95, 0)[0] - ax.c2p(0.05, 0)[0], height=ax.c2p(0, 0.06)[1] - ax.c2p(0, 0)[1],
                         stroke_width=0, fill_color=C.SPECTRUM, fill_opacity=0.35).move_to(ax.c2p(0.5, 0.03))
        box = VGroup(*[Line(ax.c2p(0.05, e), ax.c2p(0.95, e), color=C.SPECTRUM, stroke_width=1, stroke_opacity=0.6)
                       for e in cont if e < 0.06])
        ll = VGroup(*[MathTex(rf"n = {n}", font_size=18, color=C.SPECTRUM).next_to(ax.c2p(0.95, e), RIGHT, buff=0.08)
                      for n, e in zip(range(1, 4), bound[:3])])
        cl = label(r"continuous spectrum", font_size=18, color=C.SPECTRUM).next_to(ax.c2p(0.95, 0.03), RIGHT, buff=0.08)
        n = np.arange(1, 6)
        assert np.allclose(bound[:5], -1 / (2 * n**2), atol=1e-3)
        tab = VGroup(MathTex(r"n", r"\quad E_n \ (\text{finite differences})", r"\quad -\tfrac{1}{2n^2}", font_size=22,
                             color=GREY_A))
        for k in range(5):
            tab.add(MathTex(f"{k + 1}", rf"\quad {{{bound[k]:.6f}}}", rf"\quad {{{-1 / (2 * (k + 1) ** 2):.6f}}}", font_size=22))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([2.4, 1.3, 0])
        regrid(tab)
        rows = VGroup(
            MathTex(r"H = -\tfrac12 \frac{d^2}{dr^2} - \frac1r \ \ \text{(atomic units, } \ell = 0)", font_size=26),
            label(r"point spectrum below $0$: \ the bound states, \ piling up at $0$", font_size=22),
            label(r"continuous spectrum $[0, \infty)$: \ the electron set free \ (in a box of radius 120: a dense ladder)",
                  font_size=22, color=GREY_A),
            label(r"a state's spectral measure: \ point masses $|\langle\psi, u_n\rangle|^2$ \ $+$ \ a continuous part",
                  font_size=22, color=C.MEASURE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(tab, DOWN, buff=0.35)
        for r_ in rows:
            if r_.width > 8.2:
                r_.width = 8.2
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(tab, DOWN, buff=0.35)
        head = label(r"Hydrogen: \ point spectrum and continuum", font_size=34).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Back to the hook. Hydrogen's Hamiltonian, for states without angular momentum, is "
            "this unbounded self-adjoint operator. <bookmark mark='b'/> Discretized and diagonalized, its lowest "
            "eigenvalues are minus one half over n squared, to six digits: the energy levels whose differences are "
            "the spectral lines. They pile up at zero. <bookmark mark='c'/> Above zero, the spectrum is continuous: "
            "the electron flies free. In a finite box that shows up as a dense ladder. A state's spectral measure has "
            "point masses at the bound states and a continuous part above."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[0]), Create(ax))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l_) for l_ in lev], lag_ratio=0.2), FadeIn(ll), run_time=2.0)
            self.play(FadeIn(tab[0]), LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.2), FadeIn(rows[1]),
                      run_time=1.8)
            vo.wait_until("c")
            self.play(FadeIn(band), Create(box), FadeIn(cl), FadeIn(rows[2]))
            self.play(FadeIn(rows[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def commutator(self):
        d = load("commutator")
        w, near, N = d["w"], int(d["near"]), int(d["N"])
        ax = plain_axes([0, N, 16], [-6, 6, 2], 6.0, 3.6).move_to([-3.4, -0.4, 0])
        ticks = VGroup()
        for v in (-100, -10, -1, 0, 1, 10, 100):
            y = math.asinh(v)
            ticks.add(MathTex(f"{v}", font_size=18).next_to(ax.c2p(0, y), LEFT, buff=0.1))
        dots = VGroup(*[Dot(ax.c2p(i + 0.5, math.asinh(v)), radius=0.045,
                            color=C.EPS if abs(v - 1) < 0.05 else C.PATHOLOGY) for i, v in enumerate(w)])
        one = DashedLine(ax.c2p(0, math.asinh(1)), ax.c2p(N, math.asinh(1)), color=C.EPS, stroke_width=2)
        tl = MathTex(rf"\text{{eigenvalues of }} -i[X, P], \ N = {N}", font_size=24).next_to(ax, UP, buff=0.1)
        assert abs(w.sum()) < 1e-9 and near > 50
        rows = VGroup(
            MathTex(r"[x, p] = xp - px = i\,I \quad (\hbar = 1)", font_size=30, color=C.EPS),
            label(r"for $N \times N$ matrices: \ $\operatorname{tr}(XP - PX) = 0 \ne iN = \operatorname{tr}(iI)$", font_size=22),
            MathTex(rf"\text{{discretized: {near} of {N} eigenvalues near }} 1, \text{{ the rest pay: sum}} = {sci(abs(w.sum()), 0)}",
                    font_size=22, color=GREY_A),
            label(r"bounded operators can't either \ (Wielandt):", font_size=22),
            MathTex(r"AB^n - B^nA = nB^{n-1} \Rightarrow n\|B^{n-1}\| \le 2\|A\|\|B\|\|B^{n-1}\|", font_size=24),
            label(r"so $n \le 2\|A\|\|B\|$ for every $n$: \ absurd", font_size=22, color=C.PATHOLOGY),
            label(r"position and momentum must be unbounded", font_size=24, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.5, -0.3, 0])
        for r_ in rows:
            if r_.width > 6.6:
                r_.width = 6.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.5, -0.3, 0])
        head = label(r"Why $x$ and $p$ cannot be bounded", font_size=34).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> The canonical commutation relation says x p minus p x is i times the identity. "
            "For matrices that's impossible: the trace of a commutator is zero, the trace of i I is not. "
            "<bookmark mark='b'/> Discretize x and p on sixty-four points and look at the eigenvalues of the "
            "commutator divided by i. Fifty-five of them sit near one, as the relation wants, and a few run off "
            "to plus and minus a hundred to make the trace zero. <bookmark mark='c'/> For bounded operators, "
            "Wielandt's argument rules it out too: commuting through powers gives n times the norm of B to the n "
            "minus one at most a fixed constant times it. So position and momentum must be unbounded: the honest "
            "reason the quantum videos needed this part."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(ticks), Create(one), FadeIn(tl))
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.02), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[3:5]))
            self.play(FadeIn(rows[5:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def summary(self):
        items = [
            (r"observables are self-adjoint operators, \ so each has a spectral measure", C.OPERATOR, r"ch. 8, 10"),
            (r"the Born rule: \ $\Pr(\text{value} \in \omega) = \|E(\omega)\psi\|^2$", C.MEASURE, r"ch. 7, 8"),
            (r"position and momentum: \ continuous spectra, \ no eigenvectors", C.SPECTRUM, r"ch. 7, 10"),
            (r"$[x, p] = iI$ forces unbounded operators, \ hence domains", C.PATHOLOGY, r"ch. 9, 12"),
            (r"time evolution is $e^{-itH}$, \ and must be (Stone)", C.EPS, r"ch. 11"),
            (r"hydrogen: \ point spectrum below $0$, \ continuum above", C.SPECTRUM, r"ch. 12"),
        ]
        rows = VGroup()
        for t, c, ch in items:
            mark = MathTex(r"\checkmark", font_size=34, color=C.CONNECTED_SET)
            rows.add(VGroup(mark, label(t, font_size=26, color=c), label(ch, font_size=20, color=GREY_B)).arrange(
                RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 0.3)
        head = label(r"The quantum videos' assumptions, \ now theorems", font_size=36).to_edge(UP, buff=0.4)
        with self.voiceover(
            "So here's what's been proved. Observables are self-adjoint operators, so each has a spectral measure, "
            "and the Born rule is that measure. Position and momentum have continuous spectra and no eigenvectors, "
            "and their commutation relation forces them to be unbounded. Time evolution is e to the minus i t H, and "
            "by Stone's theorem it has to be. And hydrogen's spectrum is points below zero, continuum above."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.6),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.5)
        self.clear_scene()
