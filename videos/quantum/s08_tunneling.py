from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum.common import (WaveView, boxed, corner_wheel, frames_at, label, load, mtex, note, num, polyline,
                                   sci, stack, wave_axes, why, ylabel)
from videos.quantum.compute import TUNNEL


def barrier_band(ax: Axes, x0, x1, min_width=0.12, color=C.POTENTIAL, opacity=0.3) -> VGroup:
    """The barrier's extent as a vertical band on a wave plot (no energy axis here: the wave and the energy are drawn
    on different panels)."""
    p0, p1 = ax.c2p(x0, ax.y_range[0]), ax.c2p(x1, ax.y_range[1])
    w = max(abs(p1[0] - p0[0]), min_width)
    r = Rectangle(width=w, height=abs(p1[1] - p0[1]), stroke_width=0, fill_color=color, fill_opacity=opacity)
    r.move_to((p0 + p1) / 2)
    edges = VGroup(DashedLine(r.get_corner(DL), r.get_corner(UL), color=color, stroke_width=1.5),
                   DashedLine(r.get_corner(DR), r.get_corner(UR), color=color, stroke_width=1.5))
    return VGroup(r, edges)


class Tunneling(VoiceoverScene):
    def construct(self):
        self.classical()
        self.inside()
        self.formula()
        self.simulation()
        self.energy_filter()
        self.sensitivity()

    # ------------------------------------------------------------------
    def classical(self):
        eax = Axes(x_range=[-6, 6, 1], y_range=[0, 1.3, 0.5], x_length=11, y_length=2.6, tips=False,
                   axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(UP * 1.6)
        V0, E = 1.0, 0.7
        bar = Polygon(eax.c2p(-0.6, 0), eax.c2p(-0.6, V0), eax.c2p(0.6, V0), eax.c2p(0.6, 0), stroke_color=C.POTENTIAL,
                      stroke_width=2.5, fill_color=C.POTENTIAL, fill_opacity=0.25)
        Vl = MathTex(r"V_0", font_size=30, color=C.POTENTIAL).next_to(eax.c2p(0.6, V0), RIGHT, buff=0.1)
        El = DashedLine(eax.c2p(-6, E), eax.c2p(6, E), color=C.ENERGY, stroke_width=2)
        Elab = MathTex(r"E < V_0", font_size=30, color=C.ENERGY).next_to(eax.c2p(-6, E), UP, buff=0.08).shift(RIGHT * 0.8)
        yl = MathTex(r"\text{energy}", font_size=26, color=GREY_B).next_to(eax.c2p(-6, 1.3), RIGHT, buff=0.1)
        s = ValueTracker(0.0)

        def ball_x(v):
            # roll in from the left at constant speed, turn around at the barrier's foot
            return -5.5 + 4.6 * (1 - abs(1 - 2 * v))

        ball = always_redraw(lambda: Dot(eax.c2p(ball_x(s.get_value()), E), radius=0.12, color=C.CLASSICAL))
        tag1 = label(r"classical particle: bounces back", font_size=26, color=C.CLASSICAL).next_to(eax, DOWN, buff=0.1)
        tag1.to_edge(LEFT, buff=0.8)
        sch = note(r"schematic").to_corner(UR, buff=0.3)
        with self.voiceover(
            "Now a question classical physics answers instantly. A particle with energy E approaches a wall of "
            "potential energy V zero, higher than E. <bookmark mark='b'/> It doesn't have enough energy to be inside "
            "the wall at all, so it must turn around. Every time."
        ) as vo:
            self.play(Create(eax), FadeIn(yl), FadeIn(bar), FadeIn(Vl), Create(El), FadeIn(Elab), FadeIn(sch))
            self.add(ball)
            vo.wait_until("b")
            self.play(s.animate.set_value(1.0), FadeIn(tag1), run_time=3.5, rate_func=linear)
        ball.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def inside(self):
        e = load("extras")
        x, psi, T, kap = e["sc_x"], e["sc_psi"], float(e["sc_T"][0]), float(e["sc_kappa"][0])
        a = TUNNEL["a"]
        d1 = MathTex(r"-\frac{\hbar^2}{2m}\varphi''", r"+", r"V_0\varphi", r"=", r"E\varphi", font_size=36)
        d2 = MathTex(r"\varphi''", r"=", r"\kappa^2\,\varphi", r",\qquad", r"\kappa = \frac{\sqrt{2m(V_0 - E)}}{\hbar}",
                     font_size=36)
        d3 = MathTex(r"\varphi", r"=", r"C\,e^{\kappa x} + D\,e^{-\kappa x}", font_size=36)
        col = stack(d1, d2, d3, buff=0.3, align=1).to_edge(UP, buff=0.35).shift(LEFT * 2.0)
        w1 = why(d1, r"inside the barrier, where $V = V_0 > E$", font_size=22)
        w3 = why(d3, r"exponentials, not waves", font_size=22)
        for w in (w1, w3):
            if w.get_right()[0] > 6.9:
                w.shift(LEFT * (w.get_right()[0] - 6.9))
        ax = wave_axes((x[0], x[-1]), (0, 4.0), x_length=12, y_length=2.6).to_edge(DOWN, buff=0.75)
        band = barrier_band(ax, 0, a)
        wv = WaveView(ax, x, psi, mode="density", scale=1.0)
        yl = ylabel(ax, r"|\varphi(x)|^2", font_size=28)
        lab_l = label(r"incoming $+$ reflected: they interfere", font_size=24, color=GREY_A).next_to(ax.c2p(0.5 * x[0], 0), DOWN, buff=0.15)
        lab_r = label(rf"transmitted: $|t|^2 = {T:.3f}$", font_size=24, color=C.BORN).move_to(ax.c2p(10.5, 1.0))
        lab_m = label(r"decays inside", font_size=24, color=C.POTENTIAL).next_to(band, UP, buff=0.1)
        joins = VGroup(*[Circle(radius=0.22, color=WHITE, stroke_width=2).move_to(ax.c2p(xx, float(np.interp(xx, x, np.abs(psi) ** 2))))
                         for xx in (0.0, a)])
        jl = label(r"$\varphi$ and $\varphi'$ continuous at both edges", font_size=24).next_to(lab_m, UP, buff=0.12)
        wheel = corner_wheel(corner=UR, buff=0.2, radius=0.28, labels=False, title=False)
        with self.voiceover(
            "Quantum mechanically, look at the energy equation inside the barrier, where V zero is bigger than E. "
            "<bookmark mark='b'/> Now the second derivative has the same sign as phi itself, so the solutions aren't "
            "waves at all. <bookmark mark='c'/> They're growing and decaying exponentials, with a decay rate kappa set "
            "by how far the energy falls short."
        ) as vo:
            self.play(Write(d1), FadeIn(w1))
            vo.wait_until("b")
            self.play(Write(d2))
            vo.wait_until("c")
            self.play(Write(d3), FadeIn(w3))
        with self.voiceover(
            "So here's the exact solution for a steady stream of particles coming from the left. "
            "<bookmark mark='i'/> Inside the barrier, the wave decays exponentially, but it doesn't reach zero before "
            "the far side. <bookmark mark='j'/> At each edge, the pieces must join smoothly: the wave and its slope "
            "continuous. <bookmark mark='t'/> So on the far side, a smaller wave carries on. On the near side, the "
            "reflected wave interferes with the incoming one, making these ripples."
        ) as vo:
            self.play(Create(ax), FadeIn(band), FadeIn(yl), FadeIn(wheel))
            vo.wait_until("i")
            self.play(FadeIn(wv), FadeIn(lab_m))
            vo.wait_until("j")
            self.play(Create(joins), FadeIn(jl))
            vo.wait_until("t")
            self.play(FadeIn(lab_r), FadeIn(lab_l))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def formula(self):
        t = load("tunnel")
        E, TE = t["E"], t["TE"]
        V0, a = TUNNEL["V0"], TUNNEL["a"]
        f1 = MathTex(r"T", r"=", r"\left[1 + \frac{V_0^2\,\sinh^2(\kappa a)}{4E\,(V_0 - E)}\right]^{-1}", font_size=40)
        f2 = MathTex(r"T", r"\approx", r"16\,\frac{E}{V_0}\Big(1 - \frac{E}{V_0}\Big)", r"e^{-2\kappa a}", font_size=40)
        f2[3].set_color(C.BORN)
        col = VGroup(f1, f2).arrange(DOWN, buff=0.45, aligned_edge=LEFT).to_corner(UL, buff=0.45)
        n1 = note(r"match $\varphi$, $\varphi'$ at both edges: four linear equations").next_to(f1, DOWN, buff=0.08,
                                                                                            aligned_edge=LEFT)
        n2 = note(r"for a thick barrier, $\kappa a \gg 1$").next_to(f2, DOWN, buff=0.08, aligned_edge=LEFT)
        ax = Axes(x_range=[0, 2.0, 0.5], y_range=[0, 1.05, 0.5], x_length=6.0, y_length=3.3, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(RIGHT * 3.2 + DOWN * 1.5)
        curve = polyline(ax, E, TE, color=C.BORN, stroke_width=3)
        v0 = DashedLine(ax.c2p(V0, 0), ax.c2p(V0, 1.02), color=C.POTENTIAL, stroke_width=2)
        v0l = MathTex(r"E = V_0", font_size=26, color=C.POTENTIAL).next_to(ax.c2p(V0, 1.02), UP, buff=0.05)
        xl = MathTex(r"E", font_size=28, color=C.ENERGY).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        yl = MathTex(r"T(E)", font_size=28, color=C.BORN).next_to(ax.y_axis.get_end(), UP, buff=0.08)
        pars = note(r"$V_0 = 0.7$, $a = 2.5$, $\hbar = m = 1$").next_to(ax, DOWN, buff=0.15)
        res = label(r"above the top: $T = 1$ when\\a whole number of half-waves fit", font_size=24, color=GREY_A)
        res.next_to(ax.c2p(1.55, 1.0), UP, buff=0.15)
        with self.voiceover(
            "Matching the pieces at both edges gives four linear equations, and solving them gives the transmission "
            "probability exactly. <bookmark mark='a'/> It involves a hyperbolic sine of kappa times the width. "
            "<bookmark mark='b'/> For a thick barrier that's dominated by a single factor: e to the minus two kappa a. "
            "Exponential in the width, and in the square root of the energy deficit."
        ) as vo:
            self.play(Write(f1[:2]), FadeIn(n1))
            vo.wait_until("a")
            self.play(Write(f1[2:]))
            vo.wait_until("b")
            self.play(Write(f2), FadeIn(n2))
        with self.voiceover(
            "Here's the whole curve. <bookmark mark='c'/> Below the top of the barrier, transmission is small but never "
            "zero. Above the top, where a classical particle would always get through, a quantum one is sometimes "
            "reflected, <bookmark mark='r'/> except at special energies where a whole number of half-waves fits across "
            "the barrier and the reflections cancel."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(pars), Create(v0), FadeIn(v0l))
            vo.wait_until("c")
            self.play(Create(curve), run_time=2.5)
            vo.wait_until("r")
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def simulation(self):
        t = load("tunnel")
        x, ts, fr, PT, PR = t["x"], t["ts"], t["frames"], t["PT"], t["PR"]
        Tp, Tk0 = float(t["T_pred"][0]), float(t["T_k0"][0])
        assert abs(PT[-1] - 0.1416) < 0.0002 and abs(Tp - 0.1418) < 0.0002 and abs(Tk0 - 0.131) < 0.001
        a = TUNNEL["a"]
        tt = ValueTracker(0.0)
        ax = wave_axes((-190, 190), (0, 0.075), x_length=12.4, y_length=3.0).move_to(UP * 0.9)
        band = barrier_band(ax, -a / 2, a / 2, min_width=0.1)
        wv = WaveView(ax, x, fr[0], mode="density", x_window=(-190, 190)).follow(tt, frames_at(ts, fr))
        yl = ylabel(ax, r"|\psi(x,t)|^2", font_size=28)
        # meters
        mx0 = -3.2
        bars_bg = VGroup(*[Rectangle(width=4.2, height=0.36, stroke_color=GREY_C, stroke_width=1.5).move_to([mx0 + 2.1 + 4.6 * i, -2.0, 0])
                           for i in range(2)])
        names = VGroup(label(r"reflected", font_size=26, color=GREY_A).next_to(bars_bg[0], UP, buff=0.12),
                       label(r"transmitted", font_size=26, color=C.BORN).next_to(bars_bg[1], UP, buff=0.12))

        def meters():
            k = int(np.clip(round(np.interp(tt.get_value(), ts, np.arange(len(ts)))), 0, len(ts) - 1))
            g = VGroup()
            for i, v in enumerate((PR[k], PT[k])):
                bg = bars_bg[i]
                w = max(1e-3, 4.2 * v)
                g.add(Rectangle(width=w, height=0.34, stroke_width=0, fill_color=GREY_A if i == 0 else C.BORN,
                                fill_opacity=0.8).align_to(bg, LEFT).set_y(bg.get_y()))
                g.add(MathTex(f"{v:.4f}", font_size=28).next_to(bg, DOWN, buff=0.12))
            return g

        mt = always_redraw(meters)
        pred = VGroup(MathTex(r"\textstyle\int T(k)\,|\phi(k)|^2\,dk = " + f"{Tp:.4f}", font_size=30, color=C.BORN),
                      MathTex(r"T(\text{mean energy}) = " + f"{Tk0:.3f}", font_size=28, color=GREY_B)).arrange(
            DOWN, buff=0.15, aligned_edge=LEFT).to_corner(DR, buff=0.35)
        sim = note(r"simulated: split-operator FFT, $8{,}000$ points; barrier $V_0 = 0.7$, width $2.5$").to_corner(DL, buff=0.3)
        wheel = corner_wheel(corner=UR, buff=0.2, radius=0.26, labels=False, title=False)
        with self.voiceover(
            "Now send in a wave packet, simulated by solving the Schrödinger equation numerically. The packet's average "
            "energy is below the top of the barrier. <bookmark mark='h'/> It hits, and splits in two: most of it reflects, "
            "but part of it appears on the far side and keeps going."
        ) as vo:
            self.play(Create(ax), FadeIn(band), FadeIn(wv), FadeIn(yl), FadeIn(sim), FadeIn(wheel))
            self.play(FadeIn(bars_bg), FadeIn(names))
            self.add(mt)
            vo.wait_until("h")
            self.play(tt.animate.set_value(ts[-1]), run_time=vo.remaining() + 3.0, rate_func=linear)
        with self.voiceover(
            "In the end, 14.16 percent of the probability got through. <bookmark mark='p'/> The formula, averaged over "
            "the packet's spread of energies, predicts 14.18 percent. <bookmark mark='m'/> Notice that's more than the "
            "13.1 percent you'd get by plugging in the average energy alone. That difference is a clue."
        ) as vo:
            vo.wait_until("p")
            self.play(FadeIn(pred[0]))
            vo.wait_until("m")
            self.play(FadeIn(pred[1]))
        for m in (wv, mt):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def energy_filter(self):
        t = load("tunnel")
        kf, ph0, phT, phR = t["kf"], t["ph0"], t["phT"], t["phR"]
        k0, kT, kR = float(t["k0m"][0]), float(t["kT"][0]), float(t["kR"][0])
        assert abs(kT - 1.033) < 0.001 and abs(k0 - 1.0) < 1e-6
        assert abs(float(t["E_ratio"][0]) - 1.067) < 0.003  # "about seven percent higher" 
        ax = Axes(x_range=[0.55, 1.45, 0.25], y_range=[0, 1.1, 0.5], x_length=9.5, y_length=4.0, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).shift(DOWN * 0.5)
        pos = kf > 0
        nrm = lambda v: v / v[pos].max()  # noqa: E731
        c0 = polyline(ax, kf[pos], nrm(ph0)[pos], color=GREY_A, stroke_width=3)
        cT = polyline(ax, kf[pos], nrm(phT)[pos], color=C.BORN, stroke_width=3.5)
        kneg = kf < 0
        cR = polyline(ax, -kf[kneg], nrm(phR)[kneg], color=GREY_B, stroke_width=2.5)
        cR = DashedVMobject(cR, num_dashes=60)
        marks = VGroup(*[DashedLine(ax.c2p(k, 0), ax.c2p(k, 1.05), color=c, stroke_width=2) for k, c in
                         ((k0, GREY_A), (kT, C.BORN))])
        xl = MathTex(r"|k|", font_size=30, color=C.MOMENTUM).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        legend = VGroup(MathTex(r"\text{incoming: } \langle k\rangle = " + f"{k0:.3f}", font_size=28, color=GREY_A),
                        MathTex(r"\text{transmitted: } \langle k\rangle = " + f"{kT:.3f}", font_size=28, color=C.BORN),
                        MathTex(r"\text{reflected: } \langle |k|\rangle = " + f"{kR:.3f}", font_size=28, color=GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.4)
        title = label(r"momentum content, each curve scaled to its own peak", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        title.to_edge(LEFT, buff=0.5)
        with self.voiceover(
            "Look at the momentum of each part. <bookmark mark='i'/> Here's the incoming packet's spread of momenta. "
            "<bookmark mark='t'/> The part that got through is shifted toward higher momentum: the faster components "
            "tunnel more easily. Its average energy is about seven percent higher than the packet's, "
            "<bookmark mark='r'/> and the reflected part is slightly slower. So a particle doesn't lose energy by "
            "tunneling. The barrier acts as a filter that preferentially lets the more energetic components through."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(title))
            vo.wait_until("i")
            self.play(Create(c0), FadeIn(legend[0]), Create(marks[0]))
            vo.wait_until("t")
            self.play(Create(cT), FadeIn(legend[1]), Create(marks[1]))
            vo.wait_until("r")
            self.play(Create(cR), FadeIn(legend[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sensitivity(self):
        t = load("tunnel")
        kap = float(t["kappa_1eV"][0]) * 1e-9
        eh, eo, stm = float(t["e_half"][0]), float(t["e_one"][0]), float(t["stm"][0])
        assert abs(kap - 5.12) < 0.01 and abs(eh - 0.006) < 0.0002 and abs(eo / 3.5e-5 - 1) < 0.02 and abs(stm - 8.8) < 0.05
        rows = VGroup(
            label(r"an electron $1$ eV below the top of a barrier:", font_size=30),
            MathTex(r"\kappa = " + f"{kap:.2f}" + r"\ \text{nm}^{-1}", font_size=34),
            MathTex(r"a = 0.5\ \text{nm}:\quad e^{-2\kappa a} \approx " + f"{eh:.3f}", font_size=34, color=C.BORN),
            MathTex(r"a = 1\ \text{nm}:\quad e^{-2\kappa a} \approx " + sci(eo, 2), font_size=34, color=C.BORN),
        ).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.5)
        uses = VGroup(
            label(r"\textbf{scanning tunneling microscope}: the current changes $\sim 9\times$ per \AA\ of gap", font_size=27),
            label(r"\textbf{alpha decay}: helium nuclei tunnel out of the nucleus \ (Gamow, 1928)", font_size=27),
            label(r"\textbf{Nobel Prize 2025} (Clarke, Devoret, Martinis): ``macroscopic quantum mechanical\\"
                  r"tunnelling and energy quantisation in an electric circuit''", font_size=27),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(rows, DOWN, buff=0.6)
        with self.voiceover(
            "That exponential makes tunneling extremely sensitive to distance. <bookmark mark='a'/> For an electron one "
            "electron volt short of the top, kappa is about five per nanometer. <bookmark mark='b'/> Through half a "
            "nanometer, roughly six in a thousand get through; <bookmark mark='c'/> through one nanometer, about four in "
            "a hundred thousand."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Write(rows[1]))
            vo.wait_until("b")
            self.play(Write(rows[2]))
            vo.wait_until("c")
            self.play(Write(rows[3]))
        with self.voiceover(
            "That sensitivity is useful. <bookmark mark='s'/> A scanning tunneling microscope holds a sharp tip just "
            "above a surface; with a typical work function, the tunneling current changes about ninefold for every "
            "angstrom of gap, enough to map individual atoms. <bookmark mark='g'/> Tunneling is how alpha particles "
            "escape from nuclei, as Gamow explained in 1928. <bookmark mark='n'/> And the 2025 Nobel Prize in physics "
            "went to experiments showing that a whole superconducting circuit, with vast numbers of electrons moving "
            "together as one, can tunnel too."
        ) as vo:
            vo.wait_until("s")
            self.play(FadeIn(uses[0], shift=RIGHT * 0.2))
            vo.wait_until("g")
            self.play(FadeIn(uses[1], shift=RIGHT * 0.2))
            vo.wait_until("n")
            self.play(FadeIn(uses[2], shift=RIGHT * 0.2))
        self.wait(0.5)
        self.clear_scene()
