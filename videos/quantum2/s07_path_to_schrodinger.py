from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum2.common import (WaveView, corner_wheel, label, ladder, lframe, load, mtex, note, plain_axes, polyline,
                                    tick_labels, wave_axes, why)


class PathToSchrodinger(VoiceoverScene):
    def construct(self):
        self.kernel()
        self.derivation()
        self.roughness()
        self.algorithm()

    # ------------------------------------------------------------------
    def kernel(self):
        eta = np.linspace(-4, 4, 2400)
        e = ValueTracker(0.5)

        def k(ee):
            return np.exp(1j * eta**2 / (2 * ee))  # the kernel's phase factor (its constant prefactor dropped)

        ax = wave_axes((-4, 4), (-1.15, 1.15), x_length=11.0, y_length=2.6).move_to(DOWN * 1.2)
        wv = WaveView(ax, eta, k(0.5), mode="real", scale=1.0).follow(e, k)
        el = MathTex(r"\eta = y - x", font_size=30, color=C.XPOS).next_to(ax, DOWN, buff=0.1).align_to(ax, RIGHT)
        win = always_redraw(lambda: BraceBetweenPoints(ax.c2p(-np.sqrt(np.pi * e.get_value()), 1.12), ax.c2p(np.sqrt(np.pi * e.get_value()), 1.12),
                                                       direction=UP, color=C.QTIME))
        wl = always_redraw(lambda: MathTex(r"|\eta| \lesssim \sqrt{\hbar\epsilon/m}", font_size=28, color=C.QTIME).next_to(win, UP, buff=0.05))
        step = MathTex(r"\psi(x, t + \epsilon)", r"=", r"\int \sqrt{\frac{m}{2\pi i\hbar\epsilon}}\;e^{\,im\eta^2/2\hbar\epsilon}\;e^{-i\epsilon V(x)/\hbar}\;\psi(x + \eta, t)\,d\eta",
                       font_size=36).to_edge(UP, buff=0.35)
        step[2].set_color(WHITE)
        cap = label(r"the kernel's phase factor $e^{im\eta^2/2\hbar\epsilon}$ (real part): outside a window $\sim\sqrt{\hbar\epsilon/m}$ it oscillates so fast that it cancels",
                    font_size=24, color=GREY_B).next_to(ax, DOWN, buff=0.45)
        wheel = corner_wheel(corner=UR, buff=0.2, radius=0.26).shift(DOWN * 1.0)
        with self.voiceover(
            "Feynman's formulation has to agree with Schrödinger's, and checking that is a beautiful piece of calculus. "
            "<bookmark mark='a'/> Advance the wavefunction by one short step epsilon: integrate the short-time kernel "
            "against psi, over every displacement eta. <bookmark mark='b'/> The kernel's phase is m eta squared over two "
            "h-bar epsilon. Outside a window of width about the square root of h-bar epsilon over m, it oscillates so "
            "fast that its contributions cancel. <bookmark mark='c'/> As epsilon shrinks, the window shrinks, but only "
            "like the square root of epsilon. That square root is the whole story."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(step))
            vo.wait_until("b")
            self.add(win, wl)
            self.play(Create(ax), FadeIn(wv), FadeIn(el), FadeIn(cap), FadeIn(wheel), FadeIn(win), FadeIn(wl))
            vo.wait_until("c")
            self.play(e.animate.set_value(0.08), run_time=3)
        for m in (wv, win, wl):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def derivation(self):
        rows = [
            MathTex(r"\psi(x + \eta)", r"=", r"\psi + \eta\,\psi' + \tfrac12\eta^2\psi'' + \dots", font_size=38),
            MathTex(r"\int \sqrt{\tfrac{m}{2\pi i\hbar\epsilon}}\,e^{im\eta^2/2\hbar\epsilon}\,\{1, \eta, \eta^2\}\,d\eta", r"=",
                    r"\Big\{1,\; 0,\; \frac{i\hbar\epsilon}{m}\Big\}", font_size=36),
            MathTex(r"\psi + \epsilon\,\partial_t\psi", r"=", r"\Big(1 - \frac{i\epsilon}{\hbar}V\Big)\Big(\psi + \frac{i\hbar\epsilon}{2m}\psi''\Big) + O(\epsilon^2)",
                    font_size=36),
            MathTex(r"\epsilon\,\partial_t\psi", r"=", r"\frac{i\hbar\epsilon}{2m}\,\psi'' - \frac{i\epsilon}{\hbar}V\psi", font_size=38),
            MathTex(r"i\hbar\,\frac{\partial\psi}{\partial t}", r"=", r"-\frac{\hbar^2}{2m}\frac{\partial^2\psi}{\partial x^2} + V\psi", font_size=46),
        ]
        rows[1][2].set_color(C.ACTION)
        rows[4][0].set_color(C.ENERGY)
        rows[4][2].set_color(C.ENERGY)
        whys = [
            why(rows[0], r"Taylor: only small $\eta$ matter"),
            why(rows[1], r"Gaussian moments (the normalization is what makes the first one 1)"),
            why(rows[2], r"keep everything of first order in $\epsilon$; note $\eta^2 \sim \epsilon$"),
            why(rows[3], r"the $\psi$ terms cancel"),
            why(rows[4], r"multiply by $i\hbar/\epsilon$"),
        ]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-1.4, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> Expand psi of x plus eta in a Taylor series. Normally we'd keep only the first-order "
            "term, but here eta squared is as big as epsilon, so the second derivative stays in. "
            "<bookmark mark='b'/> Now we need three Gaussian integrals. The kernel's normalization makes the first one "
            "exactly one. The second vanishes by symmetry. And the third, the average of eta squared, is i h-bar "
            "epsilon over m: the spread of the step, with an i in it."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            box = SurroundingRectangle(rows[1][2], color=C.ACTION, buff=0.1)
            self.play(Create(box))
        with self.voiceover(
            "<bookmark mark='c'/> Collect everything to first order in epsilon. On the left, psi plus epsilon times its "
            "time derivative; on the right, the potential's phase times psi plus i h-bar epsilon over 2m times psi "
            "double prime. <bookmark mark='d'/> The psi terms cancel. <bookmark mark='e'/> Multiply by i h-bar over "
            "epsilon, and out comes the Schrödinger equation, every factor in place: the i, the h-bar squared over 2m, "
            "and the potential. Feynman did exactly this in his 1948 paper."
        ) as vo:
            self.play(FadeOut(box))
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
            self.play(Create(SurroundingRectangle(rows[4], color=C.ENERGY, buff=0.18, corner_radius=0.12)))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def roughness(self):
        s = load("slicing")
        Z = s["bm_zooms"]
        panels = VGroup()
        boxes = VGroup()
        for i in range(4):
            t, W = Z[i]
            ax = plain_axes((t[0], t[-1]), (W.min() - 0.1 * np.ptp(W), W.max() + 0.1 * np.ptp(W)), 3.0, 2.0)
            ax.x_axis.set_stroke(opacity=0.0)
            ax.y_axis.set_stroke(opacity=0.0)
            frame = Rectangle(width=3.1, height=2.1, stroke_color=GREY_D, stroke_width=1.5).move_to(ax)
            ln = polyline(ax, t, W, color=C.XPOS, stroke_width=1.8)
            zl = MathTex(r"\Delta\tau = " + ["1", r"2^{-3}", r"2^{-6}", r"2^{-9}"][i], font_size=24, color=C.QTIME).next_to(frame, DOWN, buff=0.1)
            panels.add(VGroup(frame, ln, zl))
        panels.arrange(RIGHT, buff=0.3).move_to(DOWN * 0.3)
        for i in range(3):
            boxes.add(Arrow(panels[i][0].get_right() + LEFT * 0.05, panels[i + 1][0].get_left() + RIGHT * 0.05, buff=0.05, color=GREY_B,
                            stroke_width=2, tip_length=0.12))
        top = MathTex(r"\langle \eta^2\rangle = \frac{i\hbar\epsilon}{m}", r"\quad\longleftrightarrow\quad", r"(dW)^2 = dt", font_size=40).to_edge(UP, buff=0.5)
        top[0].set_color(C.ACTION)
        top[2].set_color(C.XPOS)
        msg = label(r"typical paths are nowhere smooth: zoom in and they look just as rough", font_size=28).next_to(panels, DOWN, buff=0.55)
        tag = note(r"a computed Brownian path ($2^{18}$ steps; the imaginary-time version of a typical path), zoomed $\times 8$ each time").to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "That i h-bar epsilon over m deserves a second look. <bookmark mark='a'/> A step of size eta, whose square is "
            "proportional to the time step: it's the same rule as d W squared equals d t, the heart of the stochastic "
            "calculus video, just with an i. <bookmark mark='b'/> It means the paths that matter in Feynman's sum are "
            "not smooth curves at all. <bookmark mark='c'/> Here is a typical path, in imaginary time, at four zoom "
            "levels, each eight times closer: it never smooths out. The kinetic term in the Schrödinger equation is the "
            "trace of that roughness."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(top))
            vo.wait_until("b")
            self.play(FadeIn(panels[0]), FadeIn(tag))
            vo.wait_until("c")
            for i in range(3):
                self.play(GrowArrow(boxes[i]), FadeIn(panels[i + 1]), run_time=0.9)
            self.play(FadeIn(msg))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def algorithm(self):
        s = load("slicing")
        eps, err = s["eps"], s["err"]
        ax = Axes(x_range=[np.log10(0.025), np.log10(1.3), 1], y_range=[-3.6, 0.3, 1], x_length=5.6, y_length=4.2, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(RIGHT * 3.4 + DOWN * 0.5)
        pts = VGroup(*[Dot(ax.c2p(np.log10(e), np.log10(r)), color=C.ACTION, radius=0.07) for e, r in zip(eps, err)])
        ref = DashedLine(ax.c2p(np.log10(0.025), np.log10(err[-1] * (0.025 / eps[-1]) ** 2)), ax.c2p(np.log10(1.3), np.log10(err[-1] * (1.3 / eps[-1]) ** 2)),
                         color=GREY_C)
        rl = MathTex(r"\propto \epsilon^2", font_size=28, color=GREY_B).next_to(ref.get_center(), DOWN, buff=0.15).shift(RIGHT * 0.9)
        tks = VGroup()
        for e in (0.03125, 0.125, 0.5):
            p = ax.c2p(np.log10(e), -3.6)
            tks.add(MathTex(f"{e:g}", font_size=20, color=GREY_B).next_to(p, DOWN, buff=0.08))
        for v in (-3, -2, -1, 0):
            p = ax.c2p(np.log10(0.025), v)
            tks.add(MathTex(f"10^{{{v}}}", font_size=20, color=GREY_B).next_to(p, LEFT, buff=0.08))
        fr = lframe(ax)
        xl = MathTex(r"\epsilon", font_size=28, color=C.QTIME).next_to(fr[0].get_end(), RIGHT, buff=0.1)
        yl = label(r"error at $t = 6$", font_size=22, color=GREY_B).next_to(fr[1].get_end(), UP, buff=0.1)
        # left: the split-operator step = one Feynman slice
        f1 = MathTex(r"\hat U(\epsilon)", r"\approx", r"e^{-i\epsilon V/2\hbar}\;\underbrace{e^{-i\epsilon\hat p^2/2m\hbar}}_{\text{free kernel}}\;e^{-i\epsilon V/2\hbar}",
                     font_size=34).move_to(LEFT * 3.2 + UP * 1.6)
        f2 = label(r"the free kernel is a multiplication in momentum space (an FFT away)", font_size=24, color=GREY_A).next_to(f1, DOWN, buff=0.3)
        f3 = label(r"this is how every simulation in Part 1 was computed", font_size=26, color=C.ACTION).next_to(f2, DOWN, buff=0.35)
        slope = float(s["slope"])
        f4 = MathTex(r"\text{measured slope} = " + f"{slope:.2f}", font_size=30, color=C.ACTION).next_to(f3, DOWN, buff=0.5)
        cap = note(r"a packet in an anharmonic well, evolved to $t = 6$ by $N = 6/\epsilon$ slices vs.\ an exact eigen-expansion").to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The time-slicing isn't just a proof device; it's an algorithm. <bookmark mark='a'/> Split each short step "
            "into half a step of potential phase, the free kernel, and another half step of potential. The free kernel "
            "is just multiplication in momentum space, one fast Fourier transform away. <bookmark mark='b'/> That's how "
            "every simulation in Part 1 was computed. <bookmark mark='c'/> Here's a wave packet in an anharmonic well, "
            "evolved with fewer and fewer slices, compared with the exact answer: <bookmark mark='d'/> the error falls "
            "like epsilon squared."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(f1), FadeIn(f2))
            vo.wait_until("b")
            self.play(FadeIn(f3))
            vo.wait_until("c")
            self.play(Create(fr), FadeIn(tks), FadeIn(xl), FadeIn(yl), FadeIn(cap))
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in pts], lag_ratio=0.2))
            vo.wait_until("d")
            self.play(Create(ref), FadeIn(rl), FadeIn(f4))
        self.wait(0.4)
        self.clear_scene()
