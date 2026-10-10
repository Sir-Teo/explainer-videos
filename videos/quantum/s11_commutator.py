from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum.common import (WaveView, boxed, corner_wheel, label, load, mtex, note, num, place_whys, polyline,
                                   stack, wave_axes, why, ylabel)


def gauss_x(x, s, k0=0.0):
    return (2 * np.pi * s**2) ** -0.25 * np.exp(-(x**2) / (4 * s**2) + 1j * k0 * x)


def gauss_k(k, s, k0=0.0):
    """Fourier transform of gauss_x (hbar = 1): real and Gaussian, centered at k0, width 1 / (2 s)."""
    return (2 * s**2 / np.pi) ** 0.25 * np.exp(-((k - k0) ** 2) * s**2)


class Commutator(VoiceoverScene):
    def construct(self):
        self.momentum_eigen()
        self.dual()
        self.commutator()
        self.translation()
        self.heisenberg()

    # ------------------------------------------------------------------
    def momentum_eigen(self):
        l1 = MathTex(r"\hat p\,e^{ipx/\hbar}", r"=", r"-i\hbar\,\frac{d}{dx}e^{ipx/\hbar}", r"=", r"p\,e^{ipx/\hbar}", font_size=40)
        l1[4].set_color(C.MOMENTUM)
        l2 = MathTex(r"\braket{x}{p}", r"=", r"\frac{1}{\sqrt{2\pi\hbar}}\,e^{ipx/\hbar}", font_size=40)
        l3 = MathTex(r"\phi(p)", r"=", r"\braket{p}{\psi}", r"=", r"\frac{1}{\sqrt{2\pi\hbar}}\int e^{-ipx/\hbar}\,\psi(x)\,dx", font_size=40)
        l3[0].set_color(C.MOMENTUM)
        col = stack(l1, l2, l3, buff=0.5, align=1).to_edge(UP, buff=0.6)
        w1 = why(l1, r"plane waves are momentum eigenstates")
        w2 = why(l2, r"normalized so $\braket{p'}{p} = \delta(p - p')$")
        w3 = why(l3, r"the shadow on each plane wave")
        place_whys([l1, l2, l3], [w1, w2, w3])
        ft = label(r"the momentum wavefunction is the \textbf{Fourier transform} of the position wavefunction",
                   font_size=30, color=C.MOMENTUM).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "The momentum operator is minus i h-bar times d by d x. <bookmark mark='a'/> Its eigenvectors are the plane "
            "waves: differentiating e to the i p x over h-bar just brings down a factor of p. <bookmark mark='b'/> "
            "Normalized, these are the axes for momentum. <bookmark mark='c'/> So the amplitude to find momentum p, "
            "the shadow of psi on each plane wave, is this integral: <bookmark mark='f'/> the Fourier transform. "
            "Position and momentum are two sets of axes for the same vector, related by a Fourier transform."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(l1), FadeIn(w1))
            vo.wait_until("b")
            self.play(Write(l2), FadeIn(w2))
            vo.wait_until("c")
            self.play(Write(l3), FadeIn(w3))
            vo.wait_until("f")
            self.play(FadeIn(ft))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dual(self):
        s = ValueTracker(1.0)
        k0 = 2.0
        x = np.linspace(-9, 9, 1800)
        k = np.linspace(-1.5, 5.5, 1400)
        axx = wave_axes((-9, 9), (0, 0.95), x_length=6.0, y_length=3.0).move_to(LEFT * 3.4 + UP * 0.4)
        axk = wave_axes((-1.5, 5.5), (0, 1.9), x_length=6.0, y_length=3.0).move_to(RIGHT * 3.4 + UP * 0.4)
        wx = WaveView(axx, x, gauss_x(x, 1.0, k0), mode="density").follow(s, lambda v: gauss_x(x, v, k0))
        wk = WaveView(axk, k, gauss_k(k, 1.0, k0).astype(complex), mode="density").follow(
            s, lambda v: gauss_k(k, v, k0).astype(complex))
        lx = ylabel(axx, r"|\psi(x)|^2", font_size=30)
        lk = ylabel(axk, r"|\phi(p)|^2", color=C.MOMENTUM, font_size=30)
        xl = MathTex("x", font_size=30, color=C.XPOS).next_to(axx.x_axis.get_end(), RIGHT, buff=0.1)
        kl = MathTex("p", font_size=30, color=C.MOMENTUM).next_to(axk.x_axis.get_end(), RIGHT, buff=0.1)
        readout = always_redraw(lambda: VGroup(
            MathTex(r"\sigma_x = " + num(s.get_value(), 2), font_size=34, color=C.XPOS),
            MathTex(r"\sigma_p = " + num(0.5 / s.get_value(), 2), font_size=34, color=C.MOMENTUM),
            MathTex(r"\sigma_x\,\sigma_p = 0.50", font_size=34, color=C.HBAR)).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.9))
        un = note(r"Gaussian packets, $\hbar = 1$").to_corner(DR, buff=0.3)
        wheel = corner_wheel(corner=UR, buff=0.2, radius=0.26, labels=False, title=False)
        with self.voiceover(
            "Watch the two pictures together for a Gaussian packet. <bookmark mark='n'/> Squeeze it in position, and "
            "its momentum distribution spreads out. <bookmark mark='w'/> Spread it in position, and the momentum "
            "distribution sharpens. For a Gaussian, the product of the two widths never changes: it's always h-bar over "
            "two. That's a hint of the uncertainty principle, and it's a property of Fourier transforms, not of any "
            "measuring device."
        ) as vo:
            self.play(Create(axx), Create(axk), FadeIn(wx), FadeIn(wk), FadeIn(lx), FadeIn(lk), FadeIn(xl), FadeIn(kl),
                      FadeIn(un), FadeIn(wheel))
            self.add(readout)
            vo.wait_until("n")
            self.play(s.animate.set_value(0.45), run_time=2.5)
            vo.wait_until("w")
            self.play(s.animate.set_value(2.2), run_time=3.0)
            self.play(s.animate.set_value(1.0), run_time=2.0)
        for m in (wx, wk, readout):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def commutator(self):
        l1 = MathTex(r"\hat x\hat p\,f", r"=", r"x\,\big(-i\hbar f'\big)", r"=", r"-i\hbar\,x f'", font_size=40)
        l2 = MathTex(r"\hat p\hat x\,f", r"=", r"-i\hbar\,\big(x f\big)'", r"=", r"-i\hbar\,f - i\hbar\,x f'", font_size=40)
        l3 = MathTex(r"(\hat x\hat p - \hat p\hat x)\,f", r"=", r"i\hbar\,f", font_size=40)
        col = stack(l1, l2, l3, buff=0.45, align=1).to_edge(UP, buff=0.55).shift(LEFT * 0.5)
        w1 = why(l1, r"momentum first, then position")
        w2 = why(l2, r"position first: the product rule adds a term")
        w3 = why(l3, r"subtract: only that term survives")
        place_whys([l1, l2, l3], [w1, w2, w3])
        l2[4][:5].set_color(C.HBAR)
        cr = MathTex(r"[\hat x, \hat p]", r"=", r"\hat x\hat p - \hat p\hat x", r"=", r"i\hbar", font_size=58)
        cr[4].set_color(C.HBAR)
        crb = boxed(cr, color=C.HBAR, buff=0.25).next_to(col, DOWN, buff=0.6)
        hist = label(r"Born and Jordan, 1925; engraved on Max Born's gravestone\\in G\"ottingen as $pq - qp = \frac{h}{2\pi i}$",
                     font_size=26, color=GREY_A).next_to(crb, DOWN, buff=0.3)
        mean = label(r"no function is both a spike in $x$ and a plane wave in $p$:\\the two sets of axes share no direction",
                     font_size=28).next_to(hist, DOWN, buff=0.35)
        test = label(r"apply $\hat x\hat p$ and $\hat p\hat x$ to any function $f(x)$", font_size=30, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here's the single most important equation in quantum mechanics. Apply position and momentum to a test "
            "function f, in both orders. <bookmark mark='a'/> Momentum first, then position: minus i h-bar x f prime. "
            "<bookmark mark='b'/> Position first, then momentum: the product rule gives an extra term, minus i h-bar f. "
            "<bookmark mark='c'/> Subtract, and everything cancels except i h-bar times f."
        ) as vo:
            self.play(FadeIn(test))
            vo.wait_until("a")
            self.play(Write(l1), FadeIn(w1))
            vo.wait_until("b")
            self.play(Write(l2), FadeIn(w2))
            vo.wait_until("c")
            self.play(Write(l3), FadeIn(w3))
        with self.voiceover(
            "Since f was arbitrary, <bookmark mark='r'/> x p minus p x equals i h-bar: the canonical commutation "
            "relation. Born and Jordan found it in 1925, in the matrix version of the theory, <bookmark mark='g'/> and "
            "it's carved on Max Born's gravestone. <bookmark mark='m'/> It says position and momentum don't share any "
            "eigenvectors: nothing is both a spike in x and a plane wave in p. Almost everything that's strange about "
            "quantum mechanics flows from this one line, starting with the uncertainty principle."
        ) as vo:
            vo.wait_until("r")
            self.play(FadeOut(test), Write(cr), Create(crb[0]))
            vo.wait_until("g")
            self.play(FadeIn(hist))
            vo.wait_until("m")
            self.play(FadeIn(mean))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def translation(self):
        e = load("extras")
        xt, tay, tn, a = e["xt"], e["taylor"], e["taylor_n"], float(e["taylor_a"][0])
        s1 = MathTex(r"e^{-ia\hat p/\hbar}\,\psi(x)", r"=", r"\sum_{n=0}^\infty \frac{1}{n!}\Big(\!-a\frac{d}{dx}\Big)^n\psi(x)",
                     r"=", r"\psi(x - a)", font_size=40).to_edge(UP, buff=0.5)
        s1[4].set_color(C.XPOS)
        sn = label(r"Taylor's theorem: the momentum operator \emph{generates} translations", font_size=28, color=GREY_A)
        sn.next_to(s1, DOWN, buff=0.2)
        ax = wave_axes((-6, 9), (-1.3, 1.3), x_length=11, y_length=3.6).shift(DOWN * 1.2)
        orig = polyline(ax, xt, np.exp(-(xt**2) / 4), color=GREY_B, stroke_width=2)
        orig = DashedVMobject(orig, num_dashes=60)
        target = polyline(ax, xt, np.exp(-((xt - a) ** 2) / 4), color=C.XPOS, stroke_width=6).set_stroke(opacity=0.35)
        k = ValueTracker(0)
        wv = WaveView(ax, xt, tay[0].astype(complex), mode="real", scale=1.0)
        wv.add_updater(lambda m: m.set_psi(tay[int(k.get_value())].astype(complex)))
        cnt = always_redraw(lambda: MathTex(r"\text{terms up to } n = " + str(int(tn[int(k.get_value())])), font_size=32)
                            .to_corner(DR, buff=0.5))
        lo = label(r"dashed: $\psi(x)$; thick: $\psi(x - a)$", font_size=24, color=GREY_B).to_corner(DL, buff=0.4)
        with self.voiceover(
            "There's a deeper way to see what momentum is. Exponentiate it: e to the minus i a p over h-bar. "
            "<bookmark mark='t'/> Expand the exponential as a power series, and since p is a derivative, you get "
            "exactly Taylor's series for psi evaluated at x minus a. <bookmark mark='s'/> Watch the partial sums of "
            "that series, using only derivatives at each point, march the function over by a. Momentum is what "
            "generates translations in space."
        ) as vo:
            self.play(Write(s1))
            vo.wait_until("t")
            self.play(FadeIn(sn), Create(ax), Create(orig), FadeIn(target), FadeIn(lo))
            vo.wait_until("s")
            self.add(wv, cnt)
            for i in range(1, len(tn)):
                self.play(k.animate.set_value(i), run_time=0.6, rate_func=lambda q: float(q >= 1))
                self.wait(0.25)
        wv.clear_updaters()
        cnt.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def heisenberg(self):
        l1 = MathTex(r"\frac{d}{dt}\langle A\rangle", r"=", r"\braket{\dot\psi}{\hat A\psi} + \braket{\psi}{\hat A\dot\psi}", font_size=38)
        l2 = MathTex(r"\phantom{\frac{d}{dt}\langle A\rangle}", r"=", r"\tfrac{i}{\hbar}\braket{\hat H\psi}{\hat A\psi} - \tfrac{i}{\hbar}\braket{\psi}{\hat A\hat H\psi}",
                     font_size=38)
        l3 = MathTex(r"\phantom{\frac{d}{dt}\langle A\rangle}", r"=", r"\tfrac{i}{\hbar}\,\big\langle\,[\hat H, \hat A]\,\big\rangle", font_size=42)
        col = stack(l1, l2, l3, buff=0.4, align=1).to_edge(UP, buff=0.45)
        w1 = why(l1, r"product rule")
        w2 = why(l2, r"$\dot\psi = -\tfrac{i}{\hbar}\hat H\psi$; conjugating flips the sign")
        w3 = why(l3, r"$\hat H$ is Hermitian: move it across")
        place_whys([l1, l2, l3], [w1, w2, w3])
        l3[2].set_color(C.HBAR)
        cons = VGroup(
            MathTex(r"[\hat H, \hat A] = 0", r"\;\Rightarrow\;", r"\langle A\rangle \text{ is conserved}", font_size=38),
            MathTex(r"\hat H = \frac{\hat p^2}{2m}", r"\;\Rightarrow\;", r"[\hat H, \hat p] = 0", r"\;\Rightarrow\;",
                    r"\text{momentum is conserved}", font_size=36),
        ).arrange(DOWN, buff=0.4).next_to(col, DOWN, buff=0.7)
        cons[1][4].set_color(C.MOMENTUM)
        sym = label(r"nothing in $\hat H$ depends on where you are \ $\Rightarrow$ \ momentum never changes", font_size=28,
                    color=GREY_A).next_to(cons, DOWN, buff=0.4)
        with self.voiceover(
            "And commutators also tell us how things change in time. Differentiate an average with the product rule. "
            "<bookmark mark='b'/> Use the Schrödinger equation for each time derivative, <bookmark mark='c'/> move H "
            "across, since it's Hermitian, and the rate of change of any average is i over h-bar times the average of "
            "the commutator of H with A."
        ) as vo:
            self.play(Write(l1), FadeIn(w1))
            vo.wait_until("b")
            self.play(Write(l2[1:]), FadeIn(w2))
            vo.wait_until("c")
            self.play(Write(l3[1:]), FadeIn(w3))
        with self.voiceover(
            "<bookmark mark='z'/> So anything that commutes with the Hamiltonian is conserved. <bookmark mark='f'/> For "
            "a free particle, H is p squared over two m, which commutes with p, so momentum is conserved: exactly why the "
            "momentum distribution of our spreading packet never changed. <bookmark mark='s'/> The Hamiltonian doesn't "
            "care where the particle is, so momentum, the generator of translations, can't change. Symmetries give "
            "conservation laws."
        ) as vo:
            vo.wait_until("z")
            self.play(Write(cons[0]))
            vo.wait_until("f")
            self.play(Write(cons[1]))
            vo.wait_until("s")
            self.play(FadeIn(sym))
        self.wait(0.4)
        self.clear_scene()
