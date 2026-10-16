from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis.analysis10.common import load, plain_axes, polyline


class Stone(VoiceoverScene):
    def construct(self):
        self.card()
        self.clocks()
        self.theorem()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(11, r"Stone's theorem", r"Why does a quantum state evolve by a unitary?", lit=(1932,), part=10)
        with self.voiceover("Chapter eleven: Stone's theorem, and time evolution in quantum mechanics."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def clocks(self):
        d = load("stone")
        x, E, wts, err, ts, frames = d["x"], d["E"], d["weights"], float(d["err"]), d["ts"], d["frames"]
        # the coherent state's density is a Gaussian sliding as 2.5 cos t: checked against the spectral computation
        an = np.array([np.exp(-((x - 2.5 * math.cos(t_)) ** 2)) / math.sqrt(math.pi) for t_ in ts])
        assert np.abs(frames - an).max() < 1e-9 and err < 1e-5
        ax = plain_axes([-6, 6, 2], [0, 0.8, 0.2], 6.2, 2.6).move_to([-3.3, 1.3, 0])
        xs = np.linspace(-6, 6, 600)
        pot = runs(ax, xs, xs**2 / 2 * 0.08, GREY_C, 2)  # cut where it leaves the window, not flattened
        pl = MathTex(r"V = \tfrac12 x^2", font_size=22, color=GREY_C).next_to(ax.c2p(4.5, 0.65), RIGHT, buff=0.05)
        tT = ValueTracker(0.0)
        dens = always_redraw(lambda: polyline(ax, xs, np.exp(-((xs - 2.5 * math.cos(tT.get_value())) ** 2)) / math.sqrt(math.pi),
                                              color=C.FUNC, stroke_width=4))
        dl = MathTex(r"|\psi(x, t)|^2", font_size=24, color=C.FUNC).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        rd = VGroup(MathTex(r"t =", font_size=24), DecimalNumber(0, num_decimal_places=2, font_size=24)).arrange(
            RIGHT, buff=0.1).next_to(ax, UP, buff=0.05).align_to(ax, RIGHT)
        rd[1].add_updater(lambda m: m.set_value(tT.get_value()))
        # the bank of clocks: c_n e^(-i E_n t), lengths sqrt(weight)
        n_cl = 8
        centers = [np.array([-6.0 + 1.55 * k, -2.3, 0]) for k in range(n_cl)]
        R = 0.62
        rims = VGroup(*[Circle(radius=R, color=GREY_D, stroke_width=1.5).move_to(c) for c in centers])
        amp = np.sqrt(wts[:n_cl]) / np.sqrt(wts[:n_cl]).max()

        def hands():
            t_ = tT.get_value()
            g = VGroup()
            for k in range(n_cl):
                a = -E[k] * t_ + math.pi / 2
                g.add(Line(centers[k], centers[k] + R * amp[k] * np.array([math.cos(a), math.sin(a), 0]), color=C.SPECTRUM,
                           stroke_width=4))
            return g

        hd = always_redraw(hands)
        el = VGroup(*[MathTex(rf"E_{k} = {E[k]:.1f}", font_size=18, color=GREY_A).next_to(rims[k], DOWN, buff=0.08)
                      for k in range(n_cl)])
        bars = VGroup(*[Rectangle(width=0.5, height=1.1 * w_ / wts.max(), stroke_width=0, fill_color=C.MEASURE,
                                  fill_opacity=0.7).next_to(rims[k], UP, buff=0.12) for k, w_ in enumerate(wts[:n_cl])])
        bl = label(r"$|c_n|^2$: \ the spectral measure of $\psi$ \ (Poisson, fixed in time)", font_size=20,
                   color=C.MEASURE).next_to(bars, UP, buff=0.08).align_to(rims, LEFT)
        rows = VGroup(
            MathTex(r"\psi(t) = e^{-itH}\psi_0 = \sum_n c_n\, e^{-iE_n t}\, u_n", font_size=28, color=C.EPS),
            label(r"each spectral component turns at its own rate $E_n$", font_size=22),
            MathTex(rf"\text{{split-operator vs spectral: }} {sci(err, 1)}; \ \ \|\psi(t)\| = 1", font_size=22,
                    color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.6, 1.1, 0])
        for r_ in rows:
            if r_.width > 6.4:
                r_.width = 6.4
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.6, 1.1, 0])
        head = label(r"Time evolution is a bank of clocks", font_size=34).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> In the quantum videos, a state evolves by e to the minus i t H. Here's a packet in "
            "a harmonic well, sliding back and forth. <bookmark mark='b'/> Expand it in the eigenstates of H, with "
            "energies one half, three halves, and so on. Each coefficient is a clock hand that turns at its own rate, "
            "its energy. The sizes, the spectral measure of the state, never change: a Poisson distribution here. "
            "<bookmark mark='c'/> Computed both ways, by splitting the evolution into small steps and by the spectral "
            "decomposition, the states agree to eight digits, and the norm stays one."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(pot), FadeIn(pl), FadeIn(dens), FadeIn(dl), FadeIn(rd),
                      FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(rims), FadeIn(hd), FadeIn(el), FadeIn(rows[1]))
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.1), FadeIn(bl))
            self.play(tT.animate.set_value(2 * math.pi), run_time=8.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            self.play(tT.animate.set_value(3 * math.pi), run_time=3.0, rate_func=linear)
        for m in (dens, rd[1], hd):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        pm = ProofMap([
            r"$T$ self-adjoint $\Rightarrow$ $U(t) = \int e^{it\lambda}\, dE(\lambda)$: \ a unitary group, \ "
            r"strongly continuous",
            r"conversely, \ given such a group, \ define $Ax = \lim_{t \to 0} \frac{U(t)x - x}{it}$ where it exists",
            r"$A$ is densely defined \ (smooth the orbits: $\int \varphi(t)U(t)x\,dt$) \ and self-adjoint",
            r"$U(t) = e^{itA}$, \ by uniqueness of the spectral representation",
        ], font_size=22, width=11.5, buff=0.12, direction=DOWN).move_to([0, 0.5, 0])
        thm = label(r"\textbf{FA 13.38} \ (Stone, 1932) \ strongly continuous unitary groups are exactly $e^{itA}$, \ "
                    r"$A$ self-adjoint", font_size=26, color=C.EPS).to_edge(UP, buff=0.35)
        rows = VGroup(
            label(r"so the Schr\"odinger equation $i\psi' = H\psi$ \ $\iff$ \ evolution by unitaries: \ "
                  r"self-adjointness of $H$ is the price of conserving probability", font_size=22),
            label(r"\textbf{FA 13.34--13.37} \ semigroups (Hille--Yosida): \ the heat flow $e^{t\Delta}$ is the "
                  r"contraction case, \ chapter 6's modes decaying", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        for r_ in rows:
            if r_.width > 13:
                r_.width = 13
        with self.voiceover(
            "<bookmark mark='a'/> Stone's theorem says this is the only way it can go. Any self-adjoint operator "
            "generates a continuous group of unitaries, e to the i t A, through its spectral measure. "
            "<bookmark mark='b'/> And conversely, every continuous one-parameter group of unitaries has a generator, "
            "the derivative at time zero, which is densely defined and self-adjoint. <bookmark mark='c'/> So if time "
            "evolution preserves probability, it's e to the minus i t H for a self-adjoint H: the assumption the "
            "quantum videos made is forced. Drop unitarity, keep contraction, and you get semigroups like the heat "
            "flow."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm), FadeIn(pm))
            self.play(*pm.light(0))
            vo.wait_until("b")
            for i in (1, 2, 3):
                self.play(*pm.light(i), run_time=0.9)
            vo.wait_until("c")
            self.play(*pm.done(), FadeIn(rows))
        self.wait(0.4)
        self.clear_scene()
