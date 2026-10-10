from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum.common import (WaveView, boxed, corner_wheel, label, load, mtex, note, num, phasor, place_whys,
                                   polyline, stack, wave_axes, why)
from videos.quantum.compute import box_E, box_phi

L = 1.0


def walls(ax: Axes, h=None, color=C.POTENTIAL) -> VGroup:
    """The infinite well's walls at x = 0 and x = L, drawn as hatched slabs."""
    y0, y1 = ax.y_range[0], ax.y_range[1] if h is None else h
    g = VGroup()
    for xw, sgn in ((0.0, -1), (L, 1)):
        p0, p1 = ax.c2p(xw, y0), ax.c2p(xw, y1)
        slab = Rectangle(width=0.22, height=abs(p1[1] - p0[1]), stroke_width=0, fill_color=color, fill_opacity=0.35)
        slab.move_to((p0 + p1) / 2 + sgn * RIGHT * 0.11)
        g.add(slab, Line(p0, p1, color=color, stroke_width=3))
    return g


class Box(VoiceoverScene):
    def construct(self):
        self.separation()
        self.shooting()
        self.results()
        self.stationary()
        self.superposition()

    # ------------------------------------------------------------------
    def separation(self):
        l1 = MathTex(r"\psi(x, t)", r"=", r"\varphi(x)\,T(t)", font_size=40)
        l2 = MathTex(r"i\hbar\,\varphi\,T'", r"=", r"T\,\hat H\varphi", font_size=40)
        l3 = MathTex(r"i\hbar\,\frac{T'(t)}{T(t)}", r"=", r"\frac{\hat H\varphi(x)}{\varphi(x)}", r"=", r"E", font_size=40)
        col = stack(l1, l2, l3, buff=0.4, align=1).to_edge(UP, buff=0.4).shift(LEFT * 1.5)
        l3[4].set_color(C.ENERGY)
        w1 = why(l1, r"try a product")
        w2 = why(l2, r"put it in $i\hbar\,\partial_t\psi = \hat H\psi$")
        w3 = why(l3, r"left: only $t$; middle: only $x$.\\So both are one constant")
        place_whys([l1, l2, l3], [w1, w2, w3])
        r1 = MathTex(r"T(t) = e^{-iEt/\hbar}", font_size=42, color=C.QTIME)
        r2 = MathTex(r"\hat H\varphi = E\,\varphi", font_size=46, color=C.ENERGY)
        res = VGroup(r1, r2).arrange(RIGHT, buff=1.4).next_to(col, DOWN, buff=0.7).set_x(0)
        r2b = boxed(r2, color=C.ENERGY, buff=0.18)
        r2l = label(r"the energy eigenvalue problem", font_size=26, color=C.ENERGY).next_to(r2b, DOWN, buff=0.15)
        stat = MathTex(r"|\psi(x,t)|^2", r"=", r"|\varphi(x)|^2", font_size=38).next_to(r2l, DOWN, buff=0.5).set_x(0)
        stat[0].set_color(C.BORN)
        statl = label(r"nothing measurable changes: a \emph{stationary state}", font_size=26, color=GREY_A)
        statl.next_to(stat, DOWN, buff=0.12)
        with self.voiceover(
            "Now let's put the equation to work. A standard trick: look for solutions that are a function of space times "
            "a function of time. <bookmark mark='b'/> Substitute, <bookmark mark='c'/> and divide by phi times T. The "
            "left side depends only on time, the right side only on position, so both must equal the same constant. "
            "Call it E."
        ) as vo:
            self.play(Write(l1), FadeIn(w1))
            vo.wait_until("b")
            self.play(Write(l2), FadeIn(w2))
            vo.wait_until("c")
            self.play(Write(l3), FadeIn(w3))
        with self.voiceover(
            "<bookmark mark='t'/> The time part is just e to the minus i E t over h-bar: a clock, turning at a rate set by "
            "the energy. <bookmark mark='x'/> The space part must satisfy H phi equals E phi. That's an eigenvalue "
            "problem: find the functions that H merely rescales, and the factors E. <bookmark mark='s'/> For these "
            "special solutions the probability density never changes, because a phase factor has length one. They're "
            "called stationary states."
        ) as vo:
            vo.wait_until("t")
            self.play(Write(r1))
            vo.wait_until("x")
            self.play(Write(r2), Create(r2b[0]), FadeIn(r2l))
            vo.wait_until("s")
            self.play(Write(stat), FadeIn(statl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shooting(self):
        Et = ValueTracker(2.0)
        x = np.linspace(0, L, 600)

        def phi(E):
            k = np.sqrt(2 * E)
            return np.sin(k * x) / k

        ax = wave_axes((-0.05, 1.05), (-0.62, 0.62), x_length=6.0, y_length=3.6).move_to(LEFT * 3.4 + UP * 0.6)
        wv = WaveView(ax, x, phi(2.0).astype(complex), mode="real", scale=1.0, x_window=(0, L))
        wv.follow(Et, lambda E: phi(E).astype(complex))
        wl = walls(ax)
        end = always_redraw(lambda: Dot(ax.c2p(L, float(phi(Et.get_value())[-1])), radius=0.08, color=WHITE))
        eq = MathTex(r"\varphi'' = -\frac{2mE}{\hbar^2}\,\varphi", font_size=36).next_to(ax, UP, buff=0.35)
        bc = MathTex(r"\varphi(0) = 0", r",\quad", r"\varphi(L) \overset{?}{=} 0", font_size=32).next_to(ax, DOWN, buff=0.3)
        # endpoint value vs E
        Emax = 48.0
        eax = Axes(x_range=[0, Emax, 10], y_range=[-0.45, 0.45, 0.2], x_length=5.6, y_length=3.0, tips=False,
                   axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(RIGHT * 3.5 + UP * 0.4)
        el = MathTex("E", font_size=30, color=C.ENERGY).next_to(eax.x_axis.get_end(), RIGHT, buff=0.1)
        fl = MathTex(r"\varphi(L)", font_size=30).next_to(eax.y_axis.get_end(), UP, buff=0.1)
        trace = always_redraw(lambda: eax.plot(lambda E: np.sin(np.sqrt(2 * E)) / np.sqrt(2 * E),
                                               x_range=[2.0, max(2.01, Et.get_value())], color=WHITE, stroke_width=2.5))
        edot = always_redraw(lambda: Dot(eax.c2p(Et.get_value(), np.sin(np.sqrt(2 * Et.get_value())) / np.sqrt(2 * Et.get_value())),
                                         radius=0.07, color=C.ENERGY))
        En = [box_E(n) for n in (1, 2, 3)]
        marks = VGroup(*[VGroup(Dot(eax.c2p(E, 0), radius=0.07, color=C.ENERGY),
                                MathTex(f"E_{n}", font_size=28, color=C.ENERGY).next_to(eax.c2p(E, 0), UP, buff=0.12))
                         for n, E in zip((1, 2, 3), En)])
        units = note(r"$\hbar = m = L = 1$").to_corner(DR, buff=0.3)
        wheel = corner_wheel(corner=UR, buff=0.2, radius=0.28)
        with self.voiceover(
            "The simplest place to try it: a particle trapped in a box of length L, with walls it can never cross. "
            "Inside, there's no potential, so H phi equals E phi says phi double prime is minus two m E over h-bar "
            "squared times phi. <bookmark mark='w'/> At the walls the wavefunction must vanish. So start at the left "
            "wall at zero, pick a trial energy, and integrate across the box."
        ) as vo:
            self.play(Create(ax), FadeIn(wl), Write(eq), FadeIn(units), FadeIn(wheel))
            vo.wait_until("w")
            self.play(FadeIn(wv), FadeIn(bc), FadeIn(end))
        with self.voiceover(
            "For most energies, the wave arrives at the right wall at some nonzero height, and the boundary condition "
            "fails. <bookmark mark='s'/> Now sweep the energy upward, and track where the wave ends. "
            "<bookmark mark='z'/> Only at special energies does it land exactly on zero: whole numbers of half "
            "wavelengths fitting in the box, like the notes of a guitar string. That's where quantization comes from: "
            "not from a rule imposed by hand, but from a wave that must fit."
        ) as vo:
            self.play(Create(eax), FadeIn(el), FadeIn(fl), FadeIn(edot))
            self.add(trace)
            vo.wait_until("s")
            for n, E in zip((1, 2, 3), En):
                self.play(Et.animate.set_value(E), run_time=2.0 if n == 1 else 2.6, rate_func=linear)
                self.play(FadeIn(marks[n - 1]), run_time=0.4)
            vo.wait_until("z")
            self.play(Et.animate.set_value(Emax - 0.5), run_time=1.2, rate_func=linear)
            self.play(Et.animate.set_value(En[1]), run_time=1.5)
        for m in (wv, end, trace, edot):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        r1 = MathTex(r"\varphi_n(x)", r"=", r"\sqrt{\tfrac{2}{L}}\,\sin\frac{n\pi x}{L}", font_size=40)
        r2 = MathTex(r"E_n", r"=", r"\frac{n^2\pi^2\hbar^2}{2mL^2}", font_size=44)
        r2[0].set_color(C.ENERGY)
        col = VGroup(r1, r2).arrange(DOWN, buff=0.45, aligned_edge=LEFT).to_corner(UL, buff=0.5)
        nl = MathTex(r"n = 1, 2, 3, \dots", font_size=32).next_to(col, DOWN, buff=0.3, aligned_edge=LEFT)
        e1 = float(load("fd")["E1_eV_1nm"][0])
        ex = label(rf"an electron in a $1$\,nm box: $E_1 = {e1:.3f}$ eV", font_size=28, color=GREY_A)
        ex.next_to(nl, DOWN, buff=0.45, aligned_edge=LEFT)
        # ladder (left) and the eigenfunctions (right), each in its own frame
        lad = Axes(x_range=[0, 1, 1], y_range=[0, 17.5, 4], x_length=1.8, y_length=5.6, tips=False,
                   axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(RIGHT * 1.4 + DOWN * 0.3)
        levels = VGroup(*[Line(lad.c2p(0.05, n * n), lad.c2p(0.95, n * n), color=C.ENERGY, stroke_width=3)
                          for n in (1, 2, 3, 4)])
        lnum = VGroup(*[MathTex(f"{n * n}E_1" if n > 1 else "E_1", font_size=26, color=C.ENERGY).next_to(levels[n - 1], LEFT, buff=0.1)
                        for n in (1, 2, 3, 4)])
        x = np.linspace(0, L, 500)
        frames = VGroup()
        views = []
        for n in (1, 2, 3, 4):
            a = wave_axes((-0.02, 1.02), (-1.6, 1.6), x_length=3.0, y_length=0.82)
            a.move_to(RIGHT * 4.9 + lad.c2p(0, n * n)[1] * UP)
            views.append(WaveView(a, x, box_phi(n, x).astype(complex), mode="real", scale=1.0, x_window=(0, L)))
            frames.add(a)
        conn = VGroup(*[DashedLine(levels[i].get_right(), frames[i].get_left(), color=GREY_D, stroke_width=1.5)
                        for i in range(4)])
        el = MathTex("E", font_size=30, color=C.ENERGY).next_to(lad.y_axis.get_end(), UP, buff=0.1)
        with self.voiceover(
            "The allowed solutions are sine waves with n half-wavelengths in the box, <bookmark mark='e'/> and their "
            "energies grow like n squared: one, four, nine, sixteen times the lowest. <bookmark mark='l'/> Here's the "
            "ladder of allowed energies, and the wave that belongs to each rung. The lowest energy isn't zero: a "
            "confined particle can never be perfectly at rest. <bookmark mark='x'/> For an electron in a box one "
            "nanometer wide, the lowest energy is 0.376 electron volts."
        ) as vo:
            self.play(Write(r1), FadeIn(nl))
            vo.wait_until("e")
            self.play(Write(r2))
            vo.wait_until("l")
            self.play(Create(lad), FadeIn(el), LaggedStart(*[Create(l) for l in levels], lag_ratio=0.2), FadeIn(lnum))
            self.play(LaggedStart(*[AnimationGroup(Create(c), FadeIn(v)) for c, v in zip(conn, views)], lag_ratio=0.2),
                      run_time=2)
            vo.wait_until("x")
            self.play(FadeIn(ex))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stationary(self):
        x = np.linspace(0, L, 500)
        t = ValueTracker(0.0)
        rows, views = VGroup(), []
        for i, n in enumerate((1, 2, 3)):
            a = wave_axes((-0.02, 1.02), (0, 2.2), x_length=5.0, y_length=1.5).move_to(LEFT * 2.5 + UP * (2.0 - 2.0 * i))
            v = WaveView(a, x, box_phi(n, x).astype(complex), mode="abs", scale=1.0, x_window=(0, L))
            v.follow(t, lambda tt, n=n: box_phi(n, x) * np.exp(-1j * box_E(n) * tt))
            lab = MathTex(rf"\varphi_{n}\,e^{{-iE_{n}t/\hbar}}", font_size=30).next_to(a, LEFT, buff=0.2)
            rows.add(VGroup(a, lab, walls(a)))
            views.append(v)
        wheel = corner_wheel(corner=UL, buff=0.2, radius=0.28, labels=False, title=False)
        e = load("extras")
        p = e["boxp_p"]
        pax = wave_axes((-26, 26), (0, 0.1), x_length=4.6, y_length=2.0).move_to(RIGHT * 4.3 + UP * 0.9)
        curves = VGroup(*[polyline(pax, p, np.minimum(e[f"boxp{n}"], 0.1), color=c, stroke_width=3)
                          for n, c in ((1, GREY_A), (2, C.MOMENTUM), (3, GREY_B))])
        curves[0].set_stroke(opacity=0.5)
        curves[2].set_stroke(opacity=0.5)
        pl = MathTex(r"|\phi_2(p)|^2", font_size=30, color=C.MOMENTUM).next_to(pax, UP, buff=0.1)
        pk = VGroup(*[MathTex(s, font_size=24, color=GREY_B).next_to(pax.c2p(v, 0), DOWN, buff=0.1)
                      for v, s in ((-2 * np.pi, r"-\tfrac{2\pi\hbar}{L}"), (2 * np.pi, r"+\tfrac{2\pi\hbar}{L}"))])
        jl = MathTex(r"j = 0", font_size=34, color=C.CURRENT).next_to(pax, DOWN, buff=0.75)
        jn = label(r"a stationary state is not a particle at rest:\\it is moving left and right at once", font_size=26,
                   color=GREY_A).next_to(jl, DOWN, buff=0.2)
        with self.voiceover(
            "Here are the first three, evolving in time. <bookmark mark='c'/> The density of each never changes. Only "
            "the colors turn, the whole wave at once, at rates proportional to the energy: the second turns four times "
            "faster than the first, the third nine times faster."
        ) as vo:
            self.play(FadeIn(rows), *[FadeIn(v) for v in views], FadeIn(wheel))
            vo.wait_until("c")
            self.play(t.animate.set_value(2.2), run_time=vo.remaining() + 1.0, rate_func=linear)
        with self.voiceover(
            "Stationary doesn't mean the particle is sitting still. <bookmark mark='p'/> Measure the momentum of the "
            "second state and you'll find it's sharply peaked near plus or minus two pi h-bar over L: a standing wave is a "
            "sum of a wave moving right and one moving left. <bookmark mark='j'/> Their currents cancel exactly, so "
            "nothing flows, but the momentum is anything but zero."
        ) as vo:
            vo.wait_until("p")
            self.play(Create(pax), Create(curves[1]), FadeIn(pl), FadeIn(pk), t.animate.set_value(3.2), run_time=2,
                      rate_func=linear)
            vo.wait_until("j")
            self.play(FadeIn(jl), FadeIn(jn), t.animate.set_value(4.2), run_time=2, rate_func=linear)
        for v in views:
            v.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def superposition(self):
        x = np.linspace(0, L, 600)
        w21 = box_E(2) - box_E(1)
        T21 = 2 * np.pi / w21
        f1, f2 = box_phi(1, x), box_phi(2, x)
        amp = 16 / (9 * np.pi**2)
        mean_x = lambda tt: float(np.trapezoid(x * np.abs((f1 * np.exp(-1j * box_E(1) * tt) + f2 * np.exp(-1j * box_E(2) * tt)) / np.sqrt(2)) ** 2, x))  # noqa: E731
        for tt in (0.0, T21 / 4, T21 / 2):
            assert abs(mean_x(tt) - (0.5 - amp * np.cos(w21 * tt))) < 1e-4
        t = ValueTracker(0.0)
        ax = wave_axes((-0.02, 1.02), (0, 4.2), x_length=6.2, y_length=3.0).move_to(LEFT * 3.3 + UP * 1.4)

        def psi(tt):
            return (f1 * np.exp(-1j * box_E(1) * tt) + f2 * np.exp(-1j * box_E(2) * tt)) / np.sqrt(2)

        wv = WaveView(ax, x, psi(0), mode="density", x_window=(0, L)).follow(t, psi)
        wl = walls(ax)
        mx = always_redraw(lambda: VGroup(
            DashedLine(ax.c2p(mean_x(t.get_value()), 0), ax.c2p(mean_x(t.get_value()), 4.0), color=WHITE, stroke_width=2),
            MathTex(r"\langle x\rangle", font_size=26).next_to(ax.c2p(mean_x(t.get_value()), 4.0), UP, buff=0.05)))
        # the two clocks
        cc = [LEFT * 4.6 + DOWN * 2.3, LEFT * 2.0 + DOWN * 2.3]
        rings = VGroup(*[Circle(radius=0.75, color=GREY_C, stroke_width=1.5).move_to(c) for c in cc])
        clocks = always_redraw(lambda: VGroup(
            phasor(np.exp(-1j * box_E(1) * t.get_value()), origin=cc[0], unit=0.72, stroke_width=5),
            phasor(np.exp(-1j * box_E(2) * t.get_value()), origin=cc[1], unit=0.72, stroke_width=5)))
        cl = VGroup(MathTex(r"e^{-iE_1t/\hbar}", font_size=26).next_to(rings[0], DOWN, buff=0.12),
                    MathTex(r"e^{-iE_2t/\hbar}", font_size=26).next_to(rings[1], DOWN, buff=0.12))
        # derivation on the right
        d1 = MathTex(r"\psi", r"=", r"\tfrac{1}{\sqrt2}\big(\varphi_1 e^{-iE_1t/\hbar} + \varphi_2 e^{-iE_2t/\hbar}\big)", font_size=30)
        d2 = MathTex(r"|\psi|^2", r"=", r"\tfrac12\varphi_1^2 + \tfrac12\varphi_2^2", r"+", r"\varphi_1\varphi_2\cos\omega_{21}t", font_size=30)
        d3 = MathTex(r"\omega_{21}", r"=", r"\frac{E_2 - E_1}{\hbar}", font_size=32)
        d4 = MathTex(r"\langle x\rangle", r"=", r"\frac{L}{2} - \frac{16L}{9\pi^2}\cos\omega_{21}t", font_size=32)
        col = stack(d1, d2, d3, d4, buff=0.38, align=1).move_to(RIGHT * 3.5 + UP * 1.6)
        d2[4].set_color(C.BORN)
        d3[0].set_color(C.QTIME)
        if col.get_right()[0] > 6.9:
            col.shift(LEFT * (col.get_right()[0] - 6.9))
        # <x>(t) plot
        tax = Axes(x_range=[0, 2 * T21, T21], y_range=[0.2, 0.8, 0.3], x_length=4.6, y_length=1.6, tips=False,
                   axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(RIGHT * 3.4 + DOWN * 2.5)
        tr = always_redraw(lambda: tax.plot(lambda tt: 0.5 - amp * np.cos(w21 * tt), x_range=[0, max(1e-3, t.get_value())],
                                            color=WHITE, stroke_width=2.5))
        tl = MathTex(r"\langle x\rangle(t)", font_size=26).next_to(tax.y_axis.get_end(), UP, buff=0.08)
        sl = float(load("numbers")["slosh"][0]) * 1e15
        assert abs(sl - 3.67) < 0.01
        realn = label(rf"electron, $1$\,nm box: period $2\pi/\omega_{{21}} = {sl:.2f}$ fs", font_size=24, color=GREY_A)
        realn.next_to(tax, DOWN, buff=0.15)
        wheel = corner_wheel(corner=UL, buff=0.2, radius=0.26, labels=False, title=False)
        with self.voiceover(
            "Things get interesting when we add two stationary states. <bookmark mark='g'/> Each part keeps turning at "
            "its own rate, so the angle between the two clocks keeps changing, <bookmark mark='s'/> and the two parts "
            "interfere: constructively on the left, then on the right, then on the left again. The probability sloshes "
            "back and forth."
        ) as vo:
            self.play(Create(ax), FadeIn(wl), FadeIn(wv), FadeIn(rings), FadeIn(clocks), FadeIn(cl), FadeIn(wheel))
            self.add(mx)
            vo.wait_until("g")
            self.play(t.animate.set_value(0.25 * T21), run_time=1.5, rate_func=linear)
            vo.wait_until("s")
            self.play(t.animate.set_value(1.0 * T21), run_time=vo.remaining(), rate_func=linear)
        with self.voiceover(
            "The algebra says the same. <bookmark mark='a'/> Square the sum, and alongside the two static densities "
            "there's a cross term <bookmark mark='b'/> oscillating at the difference of the two energies, divided by "
            "h-bar. <bookmark mark='c'/> So the average position swings back and forth with amplitude sixteen L over nine "
            "pi squared, about eighteen percent of the box. <bookmark mark='d'/> For an electron in a nanometer box, "
            "that's one swing every 3.67 femtoseconds."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(d1), Write(d2), Create(tax), FadeIn(tl))
            self.add(tr)
            vo.wait_until("b")
            self.play(Write(d3), t.animate.set_value(1.5 * T21), run_time=1.5, rate_func=linear)
            vo.wait_until("c")
            self.play(Write(d4), t.animate.set_value(2.0 * T21), run_time=2, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(realn))
        with self.voiceover(
            "Remember this: a superposition of two energies oscillates at the difference frequency, E two minus E one "
            "over h-bar. These are called Bohr frequencies, and when we reach the hydrogen atom they'll turn out to be "
            "the colors of the light it emits."
        ):
            self.play(t.animate.set_value(2.0 * T21 + 0.001), run_time=0.5)
        for m in (wv, mx, clocks, tr):
            m.clear_updaters()
        self.clear_scene()
