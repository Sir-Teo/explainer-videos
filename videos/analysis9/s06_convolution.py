from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis6.compute import load as load6
from videos.analysis9.common import load, plain_axes, polyline, rho


class Convolution(VoiceoverScene):
    def construct(self):
        self.card()
        self.dipole()
        self.cantor()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(5, r"Convolution and mollifiers", r"How do you smooth a distribution?", lit=(1945,), part=9)
        with self.voiceover("Chapter five: convolution, which turns any distribution into a smooth function."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def dipole(self):
        d = load("mollify")
        eps, sups = d["eps"], d["sups"]
        ax = plain_axes([-1, 1, 0.5], [-120, 120, 60], 6.2, 3.8, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.2, -0.6, 0])
        x = np.linspace(-1, 1, 4001)
        cols = [C.SEQ, C.APPROX, C.EPS]
        curves = []
        for e, c in zip(eps[:3], cols):
            y = np.gradient(rho(x / e) / e, x)
            curves.append(runs(ax, x, y, c, 3))
        labs = [MathTex(rf"\varepsilon = {e}: \ \sup|\delta' * \rho_\varepsilon| = {s:.1f}", font_size=26, color=c).next_to(
            ax, UP, buff=0.1) for e, s, c in zip(eps[:3], sups[:3], cols)]
        tab = VGroup(MathTex(r"\varepsilon", r"\quad \sup|(\rho_\varepsilon)'|", r"\quad \times\varepsilon^2", font_size=24,
                             color=GREY_A))
        for e, s in zip(eps, sups):
            tab.add(MathTex(f"{e:g}", rf"\quad {s:.1f}", rf"\quad {s * e * e:.3f}", font_size=24))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.6, 0.6, 0])
        for row in tab[1:]:
            row[1].align_to(tab[0][1], LEFT)
            row[2].align_to(tab[0][2], LEFT)
        assert np.allclose(sups * eps**2, sups[0] * eps[0] ** 2)
        rows = VGroup(
            label(r"\textbf{FA 6.30} \ $T * \varphi$ is $C^\infty$ \ (a smooth function!)", font_size=24),
            label(r"\textbf{FA 6.32} \ $T * \rho_\varepsilon \to T$ in $\mathcal D'$ \ as $\varepsilon \to 0$", font_size=24,
                  color=C.EPS),
            label(r"so every distribution is a limit of test functions", font_size=22, color=GREY_A),
            label(r"$\delta'$, \ smoothed: \ a dipole of height $\varepsilon^{-2}$", font_size=22, color=C.DISTRIBUTION),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(tab, DOWN, buff=0.3)
        head = label(r"Smoothing $\delta'$: \ convolve with a narrowing bump", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Convolving a distribution with a test function gives an honest smooth function. "
            "With delta prime, it's the derivative of the bump itself: a dipole, up on one side and down on the "
            "other. <bookmark mark='b'/> As the bump narrows, the dipole grows: its height scales like one over "
            "epsilon squared, exactly, because one power comes from the bump and one from the derivative. "
            "<bookmark mark='c'/> And as epsilon goes to zero, the smooth functions converge to delta prime, as "
            "distributions. Every distribution is a limit of test functions."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(curves[0]), FadeIn(labs[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            for k in (1, 2):
                self.play(curves[k - 1].animate.set_stroke(opacity=0.3), Create(curves[k]),
                          FadeTransform(labs[k - 1], labs[k]), run_time=1.2)
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(FadeIn(rows[1:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cantor(self):
        d = load("mollify")
        dens, dd = d["dens"], float(d["d"])
        c6 = load6("cantorac")
        xs, F = c6["xs"], c6["F"]
        ax = plain_axes([0, 1, 0.25], [0, 6, 2], 6.2, 3.6, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.2, -0.6, 0])
        cols = [C.SEQ, C.APPROX, C.EPS]
        curves, labs = [], []
        for k, c in zip((2, 3, 4), cols):
            w = 3.0**-k
            xg = np.linspace(0, 1 - w, 1200)
            avg = (np.interp(xg + w, xs, F) - np.interp(xg, xs, F)) / w
            curves.append(runs(ax, xg + w / 2, avg, c, 2.5))
            labs.append(MathTex(rf"\text{{window }} 3^{{-{k}}}: \ \max = {avg.max():.3f}", font_size=26, color=c).next_to(
                ax, UP, buff=0.1))
        ratios = dens[1:] / dens[:-1]
        assert np.allclose(ratios, 3 ** (1 - dd), rtol=0.05)
        rows = VGroup(
            label(r"the Cantor measure, \ averaged over windows of width $3^{-k}$:", font_size=24),
            MathTex(r"\max \text{ density} = " + r",\ ".join(f"{v:.3f}" for v in dens) + r",\ \ldots", font_size=24,
                    color=C.EPS),
            MathTex(rf"\text{{each step}} \times 1.5 = 3^{{1 - d}}, \quad d = \tfrac{{\log 2}}{{\log 3}} = {dd:.4f}",
                    font_size=26),
            label(r"smoothing reveals the dimension of the set the measure lives on", font_size=22, color=GREY_A),
            label(r"(Part 3's Fej\'er kernel was the same machine: \ an approximate identity)", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.5, -0.5, 0])
        for r_ in rows:
            if r_.width > 6.2:
                r_.width = 6.2
        head = label(r"Smoothing a singular measure", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Smooth the Cantor measure from Part 6, by averaging over windows. "
            "<bookmark mark='b'/> Each narrower window shows more of the fractal structure, and the largest density "
            "grows by a factor of one and a half each time the window shrinks by three. <bookmark mark='c'/> That "
            "factor is three to the one minus d, where d, the log of two over the log of three, is the dimension of "
            "the Cantor set. Smoothing at every scale reveals the geometry of where the measure lives."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(curves[0]), FadeIn(labs[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            for k in (1, 2):
                self.play(curves[k - 1].animate.set_stroke(opacity=0.3), Create(curves[k]),
                          FadeTransform(labs[k - 1], labs[k]), run_time=1.2)
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:]))
        self.wait(0.4)
        self.clear_scene()
