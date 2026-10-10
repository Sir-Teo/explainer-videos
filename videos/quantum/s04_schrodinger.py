from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum.common import (WaveView, boxed, complex_plane, corner_wheel, frames_at, hue, label, load, mtex,
                                   note, num, part_card, phasor, place_whys, polyline, stack, why, wave_axes, ylabel)


class SchrodingerEquation(VoiceoverScene):
    def construct(self):
        self.card()
        self.requirements()
        self.plane_wave_route()
        self.why_complex()
        self.heat_vs_schrodinger()
        self.rotation()
        self.continuity()

    def card(self):
        c = part_card(2, r"The Schr\"odinger equation", r"how the arrows turn")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def requirements(self):
        q = label(r"How does $\psi(x, t)$ change in time?", font_size=44).to_edge(UP, buff=0.7)
        reqs = VGroup(
            label(r"1.\ \ \textbf{linear}: sums of solutions are solutions \ (or there's no interference)", font_size=30),
            label(r"2.\ \ \textbf{first order in time}: today's $\psi$ determines tomorrow's", font_size=30),
            label(r"3.\ \ \textbf{conserves probability}: $\int |\psi|^2\,dx$ stays $1$", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.8)
        with self.voiceover(
            "So a quantum state is a complex number at every point. How does it change in time? Whatever the rule is, "
            "it has to do three things. <bookmark mark='a'/> It must be linear: if two wavefunctions are allowed, so is "
            "their sum, because that's where interference comes from. <bookmark mark='b'/> It should be first order in "
            "time, so the wavefunction now determines the wavefunction later. <bookmark mark='c'/> And it must keep the "
            "total probability equal to one, forever."
        ) as vo:
            self.play(FadeIn(q))
            for m, r in zip("abc", reqs):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plane_wave_route(self):
        pw = MathTex(r"\psi", r"=", r"e^{\,i(kx - \omega t)}", font_size=46).to_edge(UP, buff=0.4)
        rel = VGroup(MathTex(r"E = \hbar\omega", font_size=36, color=C.ENERGY),
                     MathTex(r"p = \hbar k", font_size=36, color=C.MOMENTUM)).arrange(RIGHT, buff=1.4)
        rel.next_to(pw, DOWN, buff=0.35)
        rn = VGroup(note(r"Planck 1900, Einstein 1905"), note(r"de Broglie 1924"))
        for n_, r in zip(rn, rel):
            n_.next_to(r, DOWN, buff=0.08)
        d1 = MathTex(r"i\hbar\,\frac{\partial\psi}{\partial t}", r"=", r"\hbar\omega\,\psi", r"=", r"E\,\psi", font_size=40)
        d2 = MathTex(r"-i\hbar\,\frac{\partial\psi}{\partial x}", r"=", r"\hbar k\,\psi", r"=", r"p\,\psi", font_size=40)
        d3 = MathTex(r"-\hbar^2\,\frac{\partial^2\psi}{\partial x^2}", r"=", r"(\hbar k)^2\,\psi", r"=", r"p^2\,\psi",
                     font_size=40)
        col = stack(d1, d2, d3, buff=0.35, align=1).next_to(rn, DOWN, buff=0.45)
        d1[4].set_color(C.ENERGY)
        d2[4].set_color(C.MOMENTUM)
        d3[4].set_color(C.MOMENTUM)
        w1 = why(d1, r"$\partial_t$ brings down $-i\omega$", font_size=22)
        w2 = why(d2, r"$\partial_x$ brings down $ik$", font_size=22)
        w3 = why(d3, r"twice", font_size=22)
        place_whys([d1, d2, d3], [w1, w2, w3])
        with self.voiceover(
            "Here's the most direct route, the one that guided Schrödinger in 1926. Start with the simplest "
            "wavefunction of all, a plane wave, e to the i k x minus omega t: a helix that spins as time goes on. "
            "<bookmark mark='r'/> We know two facts about it from experiment: its energy is h-bar omega, the "
            "Planck-Einstein relation, and its momentum is h-bar k, de Broglie's."
        ) as vo:
            self.play(Write(pw))
            vo.wait_until("r")
            self.play(FadeIn(rel), FadeIn(rn))
        with self.voiceover(
            "Now differentiate. <bookmark mark='a'/> A time derivative brings down a factor of minus i omega, so i h-bar "
            "times d psi d t is h-bar omega psi: the energy times psi. <bookmark mark='b'/> A space derivative brings "
            "down i k, so minus i h-bar d psi d x is the momentum times psi. <bookmark mark='c'/> Do it twice, and "
            "minus h-bar squared times the second derivative is the momentum squared times psi."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(d1), FadeIn(w1))
            vo.wait_until("b")
            self.play(Write(d2), FadeIn(w2))
            vo.wait_until("c")
            self.play(Write(d3), FadeIn(w3))
        energy = MathTex(r"E", r"=", r"\frac{p^2}{2m}", r"+", r"V(x)", font_size=42)
        energy[0].set_color(C.ENERGY)
        energy[2].set_color(C.MOMENTUM)
        energy[4].set_color(C.POTENTIAL)
        se = MathTex(r"i\hbar\,\frac{\partial\psi}{\partial t}", r"=", r"-\frac{\hbar^2}{2m}\,\frac{\partial^2\psi}{\partial x^2}",
                     r"+", r"V(x)\,\psi", font_size=50)
        se[0].set_color(C.ENERGY)
        se[2].set_color(C.MOMENTUM)
        se[4].set_color(C.POTENTIAL)
        energy.next_to(col, DOWN, buff=0.45)
        seb = boxed(se, color=C.ENERGY, buff=0.25).move_to(DOWN * 2.55)
        name = label(r"the Schr\"odinger equation \ (Schr\"odinger, 1926)", font_size=26, color=GREY_A)
        name.next_to(seb, UP, buff=0.12)
        with self.voiceover(
            "For a particle, energy is kinetic plus potential: p squared over two m, plus V of x. <bookmark mark='e'/> "
            "Replace each side by what it does to psi, <bookmark mark='s'/> and out comes the Schrödinger equation: "
            "i h-bar d psi d t equals minus h-bar squared over two m times the second derivative, plus V psi."
        ) as vo:
            vo.wait_until("e")
            self.play(Write(energy))
            vo.wait_until("s")
            self.play(FadeOut(VGroup(d1, d2, d3, w1, w2, w3, rel, rn, pw)), energy.animate.to_edge(UP, buff=0.6))
            self.play(Write(se), Create(seb[0]), FadeIn(name), seb.animate.move_to(DOWN * 0.3), name.animate.move_to(UP * 1.0))
        ops = VGroup(MathTex(r"\hat p = -i\hbar\,\frac{\partial}{\partial x}", font_size=36, color=C.MOMENTUM),
                     MathTex(r"\hat H = \frac{\hat p^2}{2m} + V", font_size=36, color=C.ENERGY),
                     MathTex(r"i\hbar\,\frac{\partial\psi}{\partial t} = \hat H\psi", font_size=40)).arrange(RIGHT, buff=0.9)
        ops.to_edge(DOWN, buff=0.7)
        caveat = note(r"a plausibility argument, not a derivation: the equation is a postulate, checked by experiment")
        caveat.next_to(ops, DOWN, buff=0.2)
        with self.voiceover(
            "Notice what happened: momentum became an operation, minus i h-bar d by d x, <bookmark mark='h'/> and the "
            "energy became an operator called the Hamiltonian, H. The equation is just i h-bar d psi d t equals H psi. "
            "<bookmark mark='c'/> This isn't a proof. Plane waves made the guess; linearity extends it to every "
            "superposition of plane waves; and a century of experiments confirms it."
        ) as vo:
            self.play(FadeIn(ops[0]))
            vo.wait_until("h")
            self.play(FadeIn(ops[1]), FadeIn(ops[2]))
            vo.wait_until("c")
            self.play(FadeIn(caveat))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why_complex(self):
        k = 2.0
        x = np.linspace(-4, 4, 900)
        t = ValueTracker(0.0)
        ax1 = wave_axes((-4, 4), (-2.2, 2.2), x_length=9, y_length=2.3).move_to(UP * 1.75 + RIGHT * 1.4)
        ax2 = wave_axes((-4, 4), (0, 4.4), x_length=9, y_length=2.1).move_to(DOWN * 1.95 + RIGHT * 1.4)
        real = always_redraw(lambda: polyline(ax1, x, 2 * np.sin(k * x) * np.cos(t.get_value()), color=GREY_A, stroke_width=3))
        cpx = WaveView(ax2, x, 2 * np.cos(k * x), mode="density", scale=1.0)
        cpx.add_updater(lambda m: m.set_psi(2 * np.cos(k * x) * np.exp(-1j * t.get_value())))
        f1 = MathTex(r"\sin(kx - \omega t) + \sin(kx + \omega t)", r"=", r"2\sin kx\,\cos\omega t", font_size=30)
        f1.next_to(ax1, UP, buff=0.05)
        f2 = MathTex(r"e^{i(kx - \omega t)} + e^{i(-kx - \omega t)}", r"=", r"2\cos kx\; e^{-i\omega t}", font_size=30)
        f2.next_to(ax2, UP, buff=0.05)
        l1 = label(r"real\\waves", font_size=28, color=GREY_A).next_to(ax1, LEFT, buff=0.4)
        l2 = label(r"complex\\waves", font_size=28).next_to(ax2, LEFT, buff=0.4)
        zero = label(r"zero everywhere!", font_size=30, color=RED_B).move_to(ax1.c2p(0, 1.4))
        dl = MathTex(r"|\psi|^2 = 4\cos^2 kx", font_size=28, color=C.BORN).next_to(ax2, RIGHT, buff=0.1).shift(UP * 0.6)
        wheel = corner_wheel(corner=DR, buff=0.2, radius=0.3)
        q = label(r"Why does $i$ appear? Could $\psi$ be real?", font_size=40).move_to(UP * 0.3)
        with self.voiceover(
            "Why does i appear at all? Couldn't psi just be a real wave? Try it. <bookmark mark='a'/> Add a real wave "
            "moving right to one moving left. The sum is a standing wave, two sine k x cosine omega t, "
            "<bookmark mark='z'/> and a quarter of a period later it is zero everywhere, at the same instant. If psi "
            "squared were a probability, the particle would have vanished."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(FadeOut(q), Create(ax1), FadeIn(l1), Write(f1))
            self.add(real)
            vo.wait_until("z")
            self.play(t.animate.set_value(PI / 2), run_time=2.0, rate_func=linear)
            self.play(FadeIn(zero))
        with self.voiceover(
            "Now do the same with complex waves. <bookmark mark='c'/> The sum is two cosine k x times e to the minus i "
            "omega t. The overall factor only turns every arrow together, <bookmark mark='p'/> so the probability, four "
            "cosine squared k x, never changes and never vanishes. The colors cycle; the density stands still."
        ) as vo:
            self.play(FadeOut(zero))
            vo.wait_until("c")
            self.play(Create(ax2), FadeIn(l2), Write(f2), FadeIn(cpx), FadeIn(wheel))
            vo.wait_until("p")
            self.play(FadeIn(dl), t.animate.set_value(PI / 2 + 2 * TAU), run_time=vo.remaining() + 0.5, rate_func=linear)
        for m in (real, cpx):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def heat_vs_schrodinger(self):
        e = load("extras")
        x, th = e["trio_x"], e["th"]
        heat, schr = e["heat"], e["schr"]
        nh, ns = e["n_heat"] / e["n_heat"][0], e["n_schr"] / e["n_schr"][0]
        assert abs(nh[-1] - 0.5) < 0.01 and abs(ns[-1] - 1) < 1e-9
        t = ValueTracker(0.0)
        eqh = MathTex(r"\frac{\partial u}{\partial t}", r"=", r"\frac{1}{2}\,\frac{\partial^2 u}{\partial x^2}", font_size=38)
        eqs = MathTex(r"\frac{\partial \psi}{\partial t}", r"=", r"\frac{i}{2}\,\frac{\partial^2 \psi}{\partial x^2}",
                      font_size=38)
        eqs[2][0:3].set_color(C.HBAR)
        axh = wave_axes((-10, 10), (0, 1.1), x_length=5.8, y_length=2.6).move_to(LEFT * 3.4 + DOWN * 0.9)
        axs = wave_axes((-10, 10), (0, 1.1), x_length=5.8, y_length=2.6).move_to(RIGHT * 3.4 + DOWN * 0.9)
        eqh.next_to(axh, UP, buff=0.9)
        eqs.next_to(axs, UP, buff=0.9)
        th_l = label(r"heat equation", font_size=30, color=GREY_A).next_to(eqh, UP, buff=0.2)
        ts_l = label(r"Schr\"odinger equation", font_size=30).next_to(eqs, UP, buff=0.2)
        fh = always_redraw(lambda: polyline(axh, x, heat[int(round(t.get_value() * 10))], color=GREY_A, stroke_width=3))
        wv = WaveView(axs, x, schr[0], mode="abs", scale=1.0, x_window=(-10, 10))
        wv.follow(t, frames_at(th, schr))
        rh = always_redraw(lambda: MathTex(r"\textstyle\int u^2\,dx: \;" + f"{100 * nh[int(round(t.get_value() * 10))]:.0f}" +
                                           r"\%", font_size=28, color=GREY_A).next_to(axh, DOWN, buff=0.35))
        rs = always_redraw(lambda: MathTex(r"\textstyle\int |\psi|^2\,dx: \;" + f"{100 * ns[int(round(t.get_value() * 10))]:.0f}" +
                                           r"\%", font_size=28, color=C.BORN).next_to(axs, DOWN, buff=0.35))
        yl1 = ylabel(axh, "u", color=GREY_A, font_size=28)
        yl2 = ylabel(axs, r"|\psi|", font_size=28)
        with self.voiceover(
            "Here's another way to see what the i does. Strip the Schrödinger equation down to a free particle, in units "
            "where h-bar and m are one. <bookmark mark='h'/> Without the i, it would be the heat equation, the rule for "
            "how temperature smooths out. <bookmark mark='g'/> Start both from the same bump and let them run."
        ) as vo:
            self.play(FadeIn(ts_l), Write(eqs))
            vo.wait_until("h")
            self.play(FadeIn(th_l), Write(eqh))
            vo.wait_until("g")
            self.play(Create(axh), Create(axs), FadeIn(yl1), FadeIn(yl2), FadeIn(fh), FadeIn(wv), FadeIn(rh), FadeIn(rs))
        with self.voiceover(
            "Both spread. But heat flattens and fades: the bump loses half its size, and you can never run it backward to "
            "recover the original. <bookmark mark='s'/> The Schrödinger version spreads too, but its size, the total "
            "probability, stays at exactly one hundred percent. Instead of fading, the shape is stored in the phases, "
            "the color pattern, and the evolution can always be undone. The i turns decay into rotation."
        ) as vo:
            self.play(t.animate.set_value(6.0), run_time=5, rate_func=linear)
            vo.wait_until("s")
            self.play(Indicate(rs))
        for m in (fh, wv, rh, rs):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def rotation(self):
        eq = MathTex(r"\frac{\partial\psi}{\partial t}", r"=", r"-\frac{i}{\hbar}", r"\,\hat H\psi", font_size=50)
        eq[2].set_color(C.HBAR)
        eq[3].set_color(C.ENERGY)
        eq.to_edge(UP, buff=0.5)
        plane = complex_plane(radius=2.6).move_to(LEFT * 2.6 + DOWN * 0.7)
        o = plane[0][0].get_center()
        ang = ValueTracker(0.5)
        R = 1.7

        def arrows():
            z = np.exp(1j * ang.get_value())
            p = o + R * np.array([z.real, z.imag, 0])
            a = phasor(z, origin=o, unit=R, stroke_width=6, tip=0.22)
            Hz = Arrow(o, o + 2.5 * np.array([z.real, z.imag, 0]), buff=0, color=C.ENERGY, stroke_width=3,
                       tip_length=0.18).set_opacity(0.5)
            v = -1j * z
            vel = Arrow(p, p + 1.1 * np.array([v.real, v.imag, 0]), buff=0, color=C.HBAR, stroke_width=5, tip_length=0.2)
            return VGroup(Hz, a, vel)

        g = always_redraw(arrows)
        path = Circle(radius=R, color=GREY_C, stroke_width=1.5).move_to(o)
        expl = VGroup(
            MathTex(r"\hat H\psi = E\,\psi", font_size=36, color=C.ENERGY),
            label(r"multiply by $-i$: a quarter turn", font_size=28),
            label(r"velocity $\perp$ arrow $\Rightarrow$ the arrow spins,\\its length never changes", font_size=28),
            MathTex(r"\psi(t) = e^{-iEt/\hbar}\,\psi(0)", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(RIGHT * 3.4 + DOWN * 0.5)
        expl[2][0].set_color(C.HBAR)
        with self.voiceover(
            "Rearranged, the equation says the rate of change of psi is minus i over h-bar times H psi. Read that "
            "geometrically. <bookmark mark='p'/> For a plane wave, H psi is just the energy times psi: an arrow pointing "
            "the same way. <bookmark mark='q'/> Multiplying by minus i turns it a quarter turn clockwise. "
            "<bookmark mark='v'/> So the velocity of the arrow is always perpendicular to the arrow itself, "
            "<bookmark mark='s'/> and an arrow whose velocity is always perpendicular to it just goes around in a circle, "
            "at angular speed E over h-bar, never changing length."
        ) as vo:
            self.play(Write(eq), FadeIn(plane))
            vo.wait_until("p")
            self.add(g)
            self.play(FadeIn(g), FadeIn(expl[0]))
            vo.wait_until("q")
            self.play(FadeIn(expl[1]))
            vo.wait_until("v")
            self.play(FadeIn(expl[2]), Create(path))
            vo.wait_until("s")
            self.play(ang.animate.set_value(0.5 - TAU), FadeIn(expl[3]), run_time=vo.remaining() + 0.5, rate_func=linear)
        with self.voiceover(
            "For a general wavefunction, H psi isn't parallel to psi, because the second-derivative term depends on how "
            "the wave curves. Each arrow is pushed sideways by its neighbors, and that's what makes waves travel, spread "
            "and interfere. But the quarter turn is always there, and it's what will keep the total probability fixed."
        ):
            self.play(ang.animate.set_value(0.5 - 2 * TAU), run_time=5, rate_func=linear)
        g.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def continuity(self):
        l1 = MathTex(r"\frac{\partial}{\partial t}|\psi|^2", r"=", r"\psi^*\,\frac{\partial\psi}{\partial t} + \psi\,\frac{\partial\psi^*}{\partial t}",
                     font_size=34)
        l2 = MathTex(r"\phantom{\frac{\partial}{\partial t}|\psi|^2}", r"=", r"\frac{i\hbar}{2m}\Big(\psi^*\psi'' - \psi\,\psi^{*\prime\prime}\Big)",
                     font_size=34)
        l3 = MathTex(r"\phantom{\frac{\partial}{\partial t}|\psi|^2}", r"=", r"\frac{\partial}{\partial x}\,\frac{i\hbar}{2m}\Big(\psi^*\psi' - \psi\,\psi^{*\prime}\Big)",
                     font_size=34)
        l4 = MathTex(r"\frac{\partial}{\partial t}|\psi|^2", r"+", r"\frac{\partial j}{\partial x}", r"= 0,", r"\quad j = \frac{\hbar}{m}\,\mathrm{Im}\big(\psi^*\psi'\big)",
                     font_size=38)
        col = stack(l1, l2, l3, buff=0.32, align=1).to_edge(UP, buff=0.35).shift(LEFT * 1.4)
        l4.next_to(col, DOWN, buff=0.4).set_x(-0.8)
        l4[2].set_color(C.CURRENT)
        l4[4].set_color(C.CURRENT)
        l4b = boxed(l4, color=C.CURRENT, buff=0.18)
        w1 = why(l1, r"product rule", font_size=22)
        w2 = why(l2, r"use the equation; the $V$ terms\\cancel (if $V$ is real)", font_size=22)
        w3 = why(l3, r"the cross terms $\psi^{*\prime}\psi'$ cancel", font_size=22)
        place_whys([l1, l2, l3], [w1, w2, w3])
        with self.voiceover(
            "Let's prove that. How fast does the probability density change at one point? <bookmark mark='a'/> By the "
            "product rule, it's psi star times d psi d t, plus psi times d psi star d t. <bookmark mark='b'/> Use the "
            "Schrödinger equation for each time derivative. The potential terms cancel each other, as long as V is "
            "real, <bookmark mark='c'/> and what's left is a perfect derivative with respect to x."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(l1), FadeIn(w1))
            vo.wait_until("b")
            self.play(Write(l2[1:]), FadeIn(w2))
            vo.wait_until("c")
            self.play(Write(l3[1:]), FadeIn(w3))
        with self.voiceover(
            "<bookmark mark='d'/> That's a continuity equation, the same law that says fluid can't appear or disappear, "
            "only flow. The quantity flowing is the probability current, j, h-bar over m times the imaginary part of psi "
            "star psi prime. Probability only moves around; it is never created or destroyed."
        ) as vo:
            vo.wait_until("d")
            self.play(Write(l4), Create(l4b[0]))
        p = load("packet")
        x, ts, fr = p["x"], p["ts"], p["frames"]
        ax = wave_axes((-10, 60), (0, 0.22), x_length=11.5, y_length=1.8).to_edge(DOWN, buff=0.75)
        t = ValueTracker(0.0)
        wv = WaveView(ax, x, fr[0], mode="density", x_window=(-10, 60)).follow(t, frames_at(ts, fr))
        dx = x[1] - x[0]

        def current():
            k = int(np.clip(round(np.interp(t.get_value(), ts, np.arange(len(ts)))), 0, len(ts) - 1))
            psi = fr[k].astype(complex)
            j = np.imag(np.conj(psi) * np.gradient(psi, dx))
            g = VGroup()
            for xx in np.arange(-6, 58, 2.5):
                jj = float(np.interp(xx, x, j))
                if jj > 0.004:
                    base = ax.c2p(xx, 0) + DOWN * 0.32
                    g.add(Arrow(base, base + RIGHT * min(1.6, 9 * jj), buff=0, color=C.CURRENT, stroke_width=3,
                                tip_length=0.12, max_tip_length_to_length_ratio=0.4))
            return g

        jarr = always_redraw(current)
        total = always_redraw(lambda: MathTex(r"\int|\psi|^2dx = " + f"{float(np.sum(np.abs(fr[int(np.clip(round(np.interp(t.get_value(), ts, np.arange(len(ts)))), 0, len(ts) - 1))]) ** 2) * dx):.6f}",
                                              font_size=30, color=C.BORN).next_to(ax, UP, buff=0.1).to_edge(RIGHT, buff=0.5))
        jl = MathTex("j", font_size=30, color=C.CURRENT).next_to(ax, LEFT, buff=0.2).shift(DOWN * 0.35)
        wheel = corner_wheel(corner=DL, buff=0.2, radius=0.28, labels=False, title=False)
        with self.voiceover(
            "Here's a moving packet with its current drawn underneath. <bookmark mark='m'/> The current pushes "
            "probability forward at the front, it drains out at the back, and the total stays at exactly one: here, to "
            "six decimal places, the whole time."
        ) as vo:
            self.play(FadeOut(VGroup(l1, l2, l3, w1, w2, w3)), l4b.animate.to_edge(UP, buff=0.5))
            self.play(Create(ax), FadeIn(wv), FadeIn(jl), FadeIn(wheel))
            self.add(jarr, total)
            vo.wait_until("m")
            self.play(t.animate.set_value(25), run_time=vo.remaining() + 1.0, rate_func=linear)
        for m in (wv, jarr, total):
            m.clear_updaters()
        self.clear_scene()
