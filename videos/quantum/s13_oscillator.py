from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum.common import (WaveView, boxed, label, load, mtex, note, num, num_table, part_card, place_whys,
                                   polyline, stack, wave_axes, why, ylabel)
from videos.quantum.compute import ho_state


class Oscillator(VoiceoverScene):
    def construct(self):
        self.card()
        self.why_oscillator()
        self.factorize()
        self.ladder()
        self.check()
        self.forbidden()
        self.correspondence()

    def card(self):
        c = part_card(4, r"Two exactly solvable worlds", r"the harmonic oscillator and the hydrogen atom")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def why_oscillator(self):
        ax = Axes(x_range=[-3, 3, 1], y_range=[-1.2, 2.2, 1], x_length=7.0, y_length=4.2, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(LEFT * 2.6 + DOWN * 0.3)
        V = lambda x: 0.25 * x**4 - 0.9 * x**2 + 0.25 * x + 0.3 + 0.1 * np.sin(3 * x)  # noqa: E731
        xs = np.linspace(-2.8, 2.8, 400)
        curve = polyline(ax, xs, V(xs), color=C.POTENTIAL, stroke_width=3.5)
        i0 = np.argmin(V(xs) + 10 * (xs > 0))  # the left minimum
        x0 = xs[i0]
        h = 1e-3
        k2 = (V(x0 + h) - 2 * V(x0) + V(x0 - h)) / h**2
        par = polyline(ax, xs[np.abs(xs - x0) < 0.9], V(x0) + 0.5 * k2 * (xs[np.abs(xs - x0) < 0.9] - x0) ** 2,
                       color=C.ENERGY, stroke_width=3)
        t1 = MathTex(r"V(x)", r"\approx", r"V(x_0) + \tfrac12 V''(x_0)\,(x - x_0)^2", font_size=36).to_edge(UP, buff=0.5)
        t1[2].set_color(C.ENERGY)
        h1 = MathTex(r"\hat H", r"=", r"\frac{\hat p^2}{2m}", r"+", r"\frac12 m\omega^2\hat x^2", font_size=46)
        h1[0].set_color(C.ENERGY)
        h1.move_to(RIGHT * 3.6 + UP * 0.6)
        ex = label(r"vibrating molecules, atoms in a crystal,\\every mode of the electromagnetic field", font_size=26,
                   color=GREY_A).next_to(h1, DOWN, buff=0.45)
        with self.voiceover(
            "Next, the most important system in physics: the harmonic oscillator. Why so important? <bookmark mark='m'/> "
            "Take any potential with a smooth minimum, and zoom in. <bookmark mark='p'/> Near the bottom, Taylor's "
            "theorem says it's a parabola. So the oscillator describes anything that vibrates a little around "
            "equilibrium: molecules, crystals, even the modes of light. <bookmark mark='h'/> Its Hamiltonian is p "
            "squared over two m plus one half m omega squared x squared."
        ) as vo:
            self.play(Create(ax), Create(curve))
            vo.wait_until("m")
            self.play(Indicate(Dot(ax.c2p(x0, V(x0)), color=C.ENERGY, radius=0.08)), run_time=1.0)
            vo.wait_until("p")
            self.play(Create(par), Write(t1))
            vo.wait_until("h")
            self.play(Write(h1), FadeIn(ex))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def factorize(self):
        cl = MathTex(r"u^2 + v^2", r"=", r"(u - iv)(u + iv)", font_size=36).to_corner(UL, buff=0.45)
        cln = note(r"for numbers. For operators there's a leftover piece:").next_to(cl, DOWN, buff=0.1, aligned_edge=LEFT)
        a = MathTex(r"\hat a", r"=", r"\sqrt{\frac{m\omega}{2\hbar}}\Big(\hat x + \frac{i\hat p}{m\omega}\Big)", r",\qquad",
                    r"\hat a^\dagger", r"=", r"\sqrt{\frac{m\omega}{2\hbar}}\Big(\hat x - \frac{i\hat p}{m\omega}\Big)", font_size=34)
        a[0].set_color(C.LOWER)
        a[4].set_color(C.RAISE)
        a.next_to(cln, DOWN, buff=0.35).set_x(0)
        l1 = MathTex(r"\hat a^\dagger\hat a", r"=", r"\frac{m\omega}{2\hbar}\Big(\hat x^2 + \frac{\hat p^2}{m^2\omega^2}", r"+ \frac{i}{m\omega}[\hat x, \hat p]",
                     r"\Big)", font_size=34)
        l2 = MathTex(r"\phantom{\hat a^\dagger\hat a}", r"=", r"\frac{\hat H}{\hbar\omega}", r"-", r"\frac12", font_size=36)
        col = stack(l1, l2, buff=0.35, align=1).next_to(a, DOWN, buff=0.45)
        l1[3].set_color(C.HBAR)
        l2[4].set_color(C.HBAR)
        w1 = why(l1, r"multiply out, keeping the order")
        w2 = why(l2, r"$[\hat x, \hat p] = i\hbar$")
        place_whys([l1, l2], [w1, w2])
        H = MathTex(r"\hat H", r"=", r"\hbar\omega\Big(\hat a^\dagger\hat a + \frac12\Big)", font_size=48)
        H[0].set_color(C.ENERGY)
        Hb = boxed(H, color=C.ENERGY, buff=0.2)
        cm = MathTex(r"[\hat a, \hat a^\dagger] = 1", font_size=38, color=C.HBAR)
        VGroup(Hb, cm).arrange(RIGHT, buff=1.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Dirac's trick for solving it: factor the Hamiltonian. For ordinary numbers, u squared plus v squared "
            "factors as u minus i v times u plus i v. <bookmark mark='a'/> So define the operator a, a combination of x "
            "and i p, and its adjoint, a dagger, with the opposite sign. <bookmark mark='m'/> Multiply them in this "
            "order and the cross terms don't quite cancel, because x and p don't commute. "
            "<bookmark mark='c'/> What's left is the commutator, i h-bar, which turns into a constant: minus one half."
        ) as vo:
            self.play(Write(cl), FadeIn(cln))
            vo.wait_until("a")
            self.play(Write(a))
            vo.wait_until("m")
            self.play(Write(l1), FadeIn(w1))
            vo.wait_until("c")
            self.play(Write(l2[1:]), FadeIn(w2))
        with self.voiceover(
            "So the Hamiltonian is h-bar omega times a dagger a, plus one half. <bookmark mark='o'/> And the same "
            "commutator gives a times a dagger minus a dagger times a equals one. That half and that one are the "
            "fingerprints of i h-bar. Everything else follows from algebra."
        ) as vo:
            self.play(Write(H), Create(Hb[0]))
            vo.wait_until("o")
            self.play(Write(cm))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ladder(self):
        ax = Axes(x_range=[-3.6, 3.6, 1], y_range=[0, 5.0, 1], x_length=5.8, y_length=6.2, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(LEFT * 3.7 + DOWN * 0.3)
        par = ax.plot(lambda x: x * x / 2, x_range=[-3.16, 3.16], color=C.POTENTIAL, stroke_width=3)
        levels = VGroup(*[Line(ax.c2p(-np.sqrt(2 * n + 1), n + 0.5), ax.c2p(np.sqrt(2 * n + 1), n + 0.5), color=C.ENERGY,
                               stroke_width=3) for n in range(5)])
        lnum = VGroup(*[MathTex(rf"\tfrac{{{2 * n + 1}}}{{2}}\hbar\omega", font_size=24, color=C.ENERGY)
                        .next_to(ax.c2p(-np.sqrt(2 * n + 1), n + 0.5), LEFT, buff=0.1) for n in range(5)])
        c1 = MathTex(r"[\hat H, \hat a^\dagger] = \hbar\omega\,\hat a^\dagger", font_size=34, color=C.RAISE)
        c2 = MathTex(r"[\hat H, \hat a] = -\hbar\omega\,\hat a", font_size=34, color=C.LOWER)
        e1 = MathTex(r"\hat H(\hat a^\dagger\psi) = (E + \hbar\omega)\,\hat a^\dagger\psi", font_size=34)
        e2 = MathTex(r"\hat H(\hat a\psi) = (E - \hbar\omega)\,\hat a\psi", font_size=34)
        rgt = VGroup(c1, c2, e1, e2).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(RIGHT * 3.3 + UP * 1.9)
        up = Arrow(ax.c2p(2.6, 1.6), ax.c2p(2.6, 2.4), buff=0, color=C.RAISE, stroke_width=5)
        dn = Arrow(ax.c2p(-2.6, 2.4), ax.c2p(-2.6, 1.6), buff=0, color=C.LOWER, stroke_width=5)
        ul = MathTex(r"\hat a^\dagger", font_size=30, color=C.RAISE).next_to(up, RIGHT, buff=0.1)
        dl = MathTex(r"\hat a", font_size=30, color=C.LOWER).next_to(dn, LEFT, buff=0.1)
        with self.voiceover(
            "Now the key commutators. <bookmark mark='c'/> H with a dagger gives h-bar omega a dagger, and H with a "
            "gives minus h-bar omega a. <bookmark mark='e'/> Their meaning: if psi has energy E, then a dagger psi has "
            "energy E plus h-bar omega, and a psi has energy E minus h-bar omega. <bookmark mark='l'/> They're ladder "
            "operators: a dagger climbs one rung, a descends one, and the rungs are evenly spaced, h-bar omega apart."
        ) as vo:
            self.play(Create(ax), Create(par))
            vo.wait_until("c")
            self.play(Write(c1), Write(c2))
            vo.wait_until("e")
            self.play(Write(e1), Write(e2))
            vo.wait_until("l")
            self.play(LaggedStart(*[Create(l) for l in levels], lag_ratio=0.15), GrowArrow(up), GrowArrow(dn), FadeIn(ul),
                      FadeIn(dl))
        b1 = MathTex(r"\langle \hat H\rangle", r"=", r"\hbar\omega\Big(\|\hat a\psi\|^2 + \tfrac12\Big)", r"\ge", r"\tfrac12\hbar\omega",
                     font_size=34)
        b2 = MathTex(r"\hat a\psi_0 = 0", r"\;\Rightarrow\;", r"\Big(x + \frac{\hbar}{m\omega}\frac{d}{dx}\Big)\psi_0 = 0", font_size=34)
        b3 = MathTex(r"\psi_0(x)", r"\propto", r"e^{-m\omega x^2/2\hbar}", r",\qquad", r"E_0 = \tfrac12\hbar\omega", font_size=36)
        b4 = MathTex(r"E_n", r"=", r"\hbar\omega\Big(n + \frac12\Big)", font_size=44)
        b4[0].set_color(C.ENERGY)
        bot = VGroup(b1, b2, b3).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 3.3 + DOWN * 0.8)
        b4b = boxed(b4, color=C.ENERGY, buff=0.18).next_to(bot, DOWN, buff=0.35)
        with self.voiceover(
            "But the ladder can't go down forever. <bookmark mark='b'/> The average energy is h-bar omega times the "
            "length squared of a psi, plus a half, and a length squared is never negative. So there's a bottom rung, "
            "where a has nothing left to lower: <bookmark mark='z'/> a psi zero equals zero. Written out, that's a "
            "first-order differential equation, <bookmark mark='g'/> and its solution is a Gaussian, with energy one "
            "half h-bar omega. <bookmark mark='n'/> Every other state is a dagger applied n times, with energy h-bar "
            "omega times n plus one half. We never solved a second-order differential equation."
        ) as vo:
            self.play(FadeOut(VGroup(c1, c2)), VGroup(e1, e2).animate.to_edge(UP, buff=0.4))
            vo.wait_until("b")
            self.play(Write(b1))
            vo.wait_until("z")
            self.play(Write(b2))
            vo.wait_until("g")
            self.play(Write(b3))
            vo.wait_until("n")
            self.play(Write(b4), Create(b4b[0]), FadeIn(lnum))
        self.wait(0.3)
        self.clear_scene()

        # the states, climbing the ladder
        x = np.linspace(-5, 5, 800)
        lad = Axes(x_range=[-4.2, 4.2, 1], y_range=[0, 5.0, 1], x_length=5.0, y_length=6.2, tips=False,
                   axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(LEFT * 3.9 + DOWN * 0.3)
        par = lad.plot(lambda v: v * v / 2, x_range=[-3.16, 3.16], color=C.POTENTIAL, stroke_width=3)
        levels = VGroup(*[Line(lad.c2p(-np.sqrt(2 * n + 1), n + 0.5), lad.c2p(np.sqrt(2 * n + 1), n + 0.5), color=C.ENERGY,
                               stroke_width=3) for n in range(5)])
        frames, views, labs, conns = VGroup(), [], VGroup(), VGroup()
        for n in range(5):
            a_ = wave_axes((-5, 5), (-0.85, 0.85), x_length=4.4, y_length=1.05).move_to(RIGHT * 3.6 + lad.c2p(0, n + 0.5)[1] * UP)
            frames.add(a_)
            views.append(WaveView(a_, x, ho_state(n, x).astype(complex), mode="real", scale=1.0))
            labs.add(MathTex(rf"\psi_{n}", font_size=28).next_to(a_, LEFT, buff=0.1))
            conns.add(DashedLine(levels[n].get_right(), a_.get_left() + LEFT * 0.45, color=GREY_D, stroke_width=1.5))
        hl = note(r"each $\psi_n = (\hat a^\dagger)^n\psi_0/\sqrt{n!}$ drawn in its own frame: Hermite functions").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Here's the result: a parabola with evenly spaced rungs, <bookmark mark='s'/> and the states that go with "
            "them. Each application of a dagger adds one more node, one more sign change: these are the Hermite "
            "functions. Evenly spaced energies are why a vibrating molecule absorbs light at one sharp frequency."
        ) as vo:
            self.play(Create(lad), Create(par), LaggedStart(*[Create(l) for l in levels], lag_ratio=0.1))
            vo.wait_until("s")
            for n in range(5):
                self.play(Create(conns[n]), FadeIn(views[n]), FadeIn(labs[n]), run_time=0.7)
            self.play(FadeIn(hl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        o = load("oscillator")
        E = o["E_fd"]
        assert np.allclose(E, np.arange(12) + 0.5, atol=2e-4)
        rows = [[str(n), num(E[n], 4), num(n + 0.5, 4)] for n in range(6)]
        tab = num_table([r"n", r"\text{matrix eigenvalue}", r"n + \tfrac12"], rows, font_size=32,
                        col_colors=[WHITE, C.ENERGY, GREY_A]).move_to(DOWN * 0.3)
        t = label(r"check: the $4{,}001 \times 4{,}001$ finite-difference Hamiltonian, $\hbar = m = \omega = 1$", font_size=28,
                  color=GREY_A).to_edge(UP, buff=0.6)
        with self.voiceover(
            "As a check, build the Hamiltonian as a big matrix on a fine grid, the same way we did for the box, and ask "
            "a computer for its eigenvalues. One half, three halves, five halves, to four decimal places."
        ):
            self.play(FadeIn(t), FadeIn(tab.header), Create(tab.rule))
            self.play(LaggedStart(*[FadeIn(r) for r in tab.rows], lag_ratio=0.25), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def forbidden(self):
        o = load("oscillator")
        out = float(o["outside0"][0])
        assert abs(out - 0.1573) < 0.0001
        x = np.linspace(-3.5, 3.5, 900)
        eax = Axes(x_range=[-3.5, 3.5, 1], y_range=[0, 1.6, 0.5], x_length=6.0, y_length=2.6, tips=False,
                   axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(UP * 1.8)
        par = eax.plot(lambda v: v * v / 2, x_range=[-1.75, 1.75], color=C.POTENTIAL, stroke_width=3)
        lev = DashedLine(eax.c2p(-3.5, 0.5), eax.c2p(3.5, 0.5), color=C.ENERGY, stroke_width=2)
        tps = VGroup(*[DashedLine(eax.c2p(s, 0), eax.c2p(s, 1.6), color=C.CLASSICAL, stroke_width=2) for s in (-1, 1)])
        el = MathTex(r"E_0", font_size=28, color=C.ENERGY).next_to(eax.c2p(3.5, 0.5), RIGHT, buff=0.1)
        tl = label(r"classical turning points", font_size=24, color=C.CLASSICAL).next_to(eax.c2p(0, 1.6), UP, buff=0.05)
        wax = wave_axes((-3.5, 3.5), (0, 0.65), x_length=6.0, y_length=2.6).move_to(DOWN * 1.7)
        wv = WaveView(wax, x, ho_state(0, x).astype(complex), mode="density", scale=1.0)
        tails = VGroup(*[wax.get_area(wax.plot(lambda v: ho_state(0, np.array([v]))[0] ** 2, x_range=r), x_range=r,
                                      color=C.CLASSICAL, opacity=0.55) for r in ((-3.5, -1), (1, 3.5))])
        tps2 = VGroup(*[DashedLine(wax.c2p(s, 0), wax.c2p(s, 0.65), color=C.CLASSICAL, stroke_width=2) for s in (-1, 1)])
        yl = ylabel(wax, r"|\psi_0|^2", font_size=28)
        val = MathTex(r"P(\text{outside}) = \operatorname{erfc}(1) = " + f"{out:.3f}", font_size=36, color=C.CLASSICAL)
        val.to_edge(RIGHT, buff=0.4).shift(DOWN * 1.7)
        with self.voiceover(
            "Look closely at the ground state. <bookmark mark='t'/> A classical particle with this energy would turn "
            "around at these two points, where all its energy is potential. <bookmark mark='w'/> The quantum wavefunction "
            "doesn't stop there: its Gaussian tails reach into the region where the kinetic energy would be negative. "
            "<bookmark mark='p'/> The probability of finding the particle out there is the complementary error function "
            "of one: 15.7 percent. Tunneling isn't exotic; it's built into every bound state."
        ) as vo:
            self.play(Create(eax), Create(par), Create(lev), FadeIn(el))
            vo.wait_until("t")
            self.play(Create(tps), FadeIn(tl))
            vo.wait_until("w")
            self.play(Create(wax), FadeIn(wv), FadeIn(yl), Create(tps2))
            vo.wait_until("p")
            self.play(FadeIn(tails), Write(val))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def correspondence(self):
        o = load("oscillator")
        x, p30 = o["x30"], o["p30"]
        A = np.sqrt(61.0)
        sel = np.abs(x) < 9.5
        ax = wave_axes((-9.5, 9.5), (0, 0.25), x_length=11.5, y_length=4.2).shift(DOWN * 0.4)
        psi30 = ho_state(30, x[sel])
        assert np.allclose(psi30**2, p30[sel], atol=1e-10)
        wv = WaveView(ax, x[sel], psi30.astype(complex), mode="density", scale=1.0, opacity=0.7)
        xc = np.linspace(-A + 0.02, A - 0.02, 800)
        cl = polyline(ax, xc, np.minimum(1 / (np.pi * np.sqrt(A**2 - xc**2)), 0.25), color=C.CLASSICAL, stroke_width=4)
        title = MathTex(r"n = 30", font_size=40).to_edge(UP, buff=0.5)
        leg = VGroup(MathTex(r"|\psi_{30}(x)|^2", font_size=32),
                     MathTex(r"\text{classical: } \frac{1}{\pi\sqrt{A^2 - x^2}}", font_size=32, color=C.CLASSICAL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.5)
        cn = label(r"a classical oscillator spends most of its time near the turning points, where it moves slowly",
                   font_size=26, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "And high up the ladder, quantum mechanics starts to look classical. <bookmark mark='q'/> Here's the thirtieth "
            "state. A classical oscillator with the same energy spends most of its time near the turning points, where "
            "it's slowest, <bookmark mark='c'/> so its probability density piles up at the edges. The quantum density "
            "oscillates rapidly, but on average it follows the classical curve. This is Bohr's correspondence "
            "principle, made visible."
        ) as vo:
            self.play(FadeIn(title), Create(ax))
            vo.wait_until("q")
            self.play(FadeIn(wv), FadeIn(leg[0]))
            vo.wait_until("c")
            self.play(Create(cl), FadeIn(leg[1]), FadeIn(cn))
        self.wait(0.4)
        self.clear_scene()
