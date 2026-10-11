from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum2.common import (corner_wheel, label, ladder, load, mtex, note, num_table, plain_axes, polyline,
                                    signed_img, wave_axes, why)


class WKB(VoiceoverScene):
    def construct(self):
        self.ansatz()
        self.compare()
        self.turning_points()
        self.table()
        self.phase_space()

    # ------------------------------------------------------------------
    def ansatz(self):
        rows = [
            MathTex(r"\psi(x)", r"=", r"A(x)\,e^{\,iS(x)/\hbar}", font_size=40),
            MathTex(r"-\frac{\hbar^2}{2m}\psi'' + V\psi", r"=", r"\Big[\frac{S'^2}{2m} + V - \frac{i\hbar}{2m}\Big(2\frac{A'}{A}S' + S''\Big) - \frac{\hbar^2}{2m}\frac{A''}{A}\Big]\psi",
                    font_size=34),
            MathTex(r"\hbar^0:\quad \frac{S'^2}{2m} + V", r"=", r"E\quad\Rightarrow\quad S' = p(x) = \sqrt{2m(E - V)}", font_size=36),
            MathTex(r"\hbar^1:\quad 2A'S' + AS''", r"=", r"0\quad\Rightarrow\quad (A^2 p)' = 0\quad\Rightarrow\quad A \propto \frac{1}{\sqrt{p}}", font_size=36),
            MathTex(r"\psi(x)", r"\approx", r"\frac{C}{\sqrt{p(x)}}\,\cos\Big(\frac1\hbar\int^x p\,dx' - \frac\pi4\Big)", font_size=42),
        ]
        rows[2][2].set_color(C.CLASSICAL)
        rows[4][2].set_color(C.APPROX)
        whys = [
            why(rows[0], r"an amplitude and a phase, both real"),
            why(rows[1], r"differentiate twice"),
            why(rows[2], r"Hamilton--Jacobi: the phase is the classical action"),
            why(rows[3], r"slow $\Rightarrow$ more likely, like a classical particle"),
            why(rows[4], r"drop $\hbar^2 A''$: the WKB approximation"),
        ]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-1.6, buff=0.5)
        hist = note(r"Wentzel, Kramers, Brillouin (1926); Jeffreys (1925)").to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The third road runs backward, from classical mechanics. <bookmark mark='a'/> Look for solutions with a "
            "classical-looking action in the exponent: an amplitude A times e to the i S over h-bar, both functions of "
            "x. <bookmark mark='b'/> Put that into the time-independent Schrödinger equation, and sort the terms by "
            "powers of h-bar."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
        with self.voiceover(
            "<bookmark mark='a'/> At order h-bar to the zero: S prime squared over 2m plus V equals E. That's the "
            "Hamilton-Jacobi equation of classical mechanics: S prime is the classical momentum, p of x, and the phase is "
            "the integral of p. <bookmark mark='b'/> At the next order, two A prime S prime plus A S double prime equals "
            "zero, which says A squared times p is constant: A goes like one over the square root of p. Where the "
            "particle is slow, it's more likely to be found, just as a classical particle spends more time where it's "
            "slow. <bookmark mark='c'/> Dropping the next order is the WKB approximation, after Wentzel, Kramers and "
            "Brillouin in 1926, and Jeffreys before them."
        ) as vo:
            vo.wait_until("a")
            step(2)
            vo.wait_until("b")
            step(3)
            vo.wait_until("c")
            step(4)
            self.play(FadeIn(hist))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        w = load("wkb")
        x, V, E = w["x"], w["V"], w["E"]
        j = int(w["wkb_n"])
        psi, wk = w["psi"][j], w["wkb_psi"]
        sel = np.abs(x) < 2.6
        top = wave_axes((-2.6, 2.6), (-1.5, 1.5), x_length=11.0, y_length=3.4).move_to(UP * 0.6)
        ex = polyline(top, x[sel], psi[sel], color=WHITE, stroke_width=3.5)
        a = E[j] ** 0.25
        inside = np.abs(x) < a - 0.02
        wk_c = np.clip(wk, -1.45, 1.45)
        wl = polyline(top, x[inside], wk_c[inside], color=C.APPROX, stroke_width=3)
        tps = VGroup(*[DashedLine(top.c2p(s * a, -1.5), top.c2p(s * a, 1.5), color=C.CLASSICAL, stroke_width=2) for s in (-1, 1)])
        tpl = label(r"turning points: $p = 0$", font_size=24, color=C.CLASSICAL).next_to(top.c2p(a, 1.5), UP, buff=0.05)
        legend = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.4, color=WHITE, stroke_width=4), label(r"exact (numerical), $n = 6$", font_size=24)).arrange(RIGHT, buff=0.15),
            VGroup(Line(ORIGIN, RIGHT * 0.4, color=C.APPROX, stroke_width=4), label(r"WKB", font_size=24, color=C.APPROX)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UL, buff=0.35)
        pot = wave_axes((-2.6, 2.6), (0, 26), x_length=11.0, y_length=1.9).move_to(DOWN * 2.45)
        vc = polyline(pot, x[sel], np.clip(V[sel], 0, 26), color=C.POTENTIAL, stroke_width=3)
        el = Line(pot.c2p(-a, E[j]), pot.c2p(a, E[j]), color=C.ENERGY, stroke_width=3)
        ell = MathTex(r"E_6", font_size=26, color=C.ENERGY).next_to(pot.c2p(0, E[j]), UP, buff=0.08)
        vl = MathTex(r"V = x^4", font_size=26, color=C.POTENTIAL).next_to(pot.c2p(-2.6, 14), LEFT, buff=0.1)
        unit = note(r"$\hbar = m = 1$, $H = p^2/2 + x^4$").to_corner(DR, buff=0.25)
        with self.voiceover(
            "Here's how well it works, for a particle in a quartic well, V equals x to the fourth. <bookmark mark='a'/> "
            "The exact sixth state, computed numerically, <bookmark mark='b'/> and the WKB wave: inside the well they're "
            "nearly indistinguishable, with short wavelengths where the particle is fast, and big amplitudes where it's "
            "slow. <bookmark mark='c'/> But at the turning points, where p goes to zero, one over the square root of p "
            "blows up."
        ) as vo:
            self.play(Create(pot), Create(vc), FadeIn(vl), FadeIn(unit))
            self.play(Create(el), FadeIn(ell))
            vo.wait_until("a")
            self.play(Create(top), Create(ex), FadeIn(legend[0]))
            vo.wait_until("b")
            self.play(Create(wl), FadeIn(legend[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(tps), FadeIn(tpl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def turning_points(self):
        from scipy.special import airy
        z = np.linspace(-9, 3, 1200)
        Ai = airy(-(-z))[0]  # Ai(z) with z = (x - x_turn) / scale, classically allowed for z < 0
        ax = wave_axes((-9, 3), (-0.75, 0.75), x_length=8.0, y_length=2.6).move_to(LEFT * 2.4 + DOWN * 0.8)
        ai = polyline(ax, z, Ai, color=WHITE, stroke_width=3.5)
        zz = z[z < -0.25]
        wkbz = np.cos((2 / 3) * (-zz) ** 1.5 - np.pi / 4) / np.sqrt(np.pi) / (-zz) ** 0.25
        wl = polyline(ax, zz, np.clip(wkbz, -0.74, 0.74), color=C.APPROX, stroke_width=3)
        tp = DashedLine(ax.c2p(0, -0.75), ax.c2p(0, 0.75), color=C.CLASSICAL)
        lin = label(r"near a turning point $V$ is a straight line: the exact solution is an Airy function", font_size=24,
                    color=GREY_A).next_to(ax, UP, buff=0.3)
        ail = MathTex(r"\mathrm{Ai}", font_size=30).next_to(ax.c2p(1.0, 0.45), UP, buff=0.05)
        q = MathTex(r"-\frac{\pi}{4}", font_size=40, color=C.HBAR).next_to(ax.c2p(-4, -0.75), DOWN, buff=0.25)
        ql = label(r"each turning point shifts the phase by $\pi/4$:\\an eighth of a cycle", font_size=22, color=C.HBAR).next_to(q, DOWN, buff=0.1)
        cond = VGroup(
            MathTex(r"\frac1\hbar\int_{x_1}^{x_2} p\,dx - \frac\pi4 - \frac\pi4", r"=", r"n\pi", font_size=34),
            MathTex(r"\oint p\,dx", r"=", r"\big(n + \tfrac12\big)\,h", font_size=44),
        ).arrange(DOWN, buff=0.5).move_to(RIGHT * 4.3 + DOWN * 0.3)
        cond[1].set_color(C.HBAR)
        hist = VGroup(label(r"Bohr (1913), Sommerfeld (1916): $\oint p\,dx = nh$", font_size=22, color=GREY_B),
                      label(r"Kramers (1926): \emph{Wellenmechanik und halbzahlige Quantisierung}", font_size=22, color=GREY_B)
                      ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Near a turning point the potential is nearly a straight line, and the exact solution "
            "there is an Airy function. <bookmark mark='b'/> Matching it to the WKB wave shows that each turning point "
            "shifts the phase by pi over four, an eighth of a cycle. <bookmark mark='c'/> So fitting a standing wave between two turning "
            "points requires the integral of p dx, there and back, to be n plus one half, times h. "
            "<bookmark mark='d'/> That's Bohr and Sommerfeld's quantum condition, with the half that Kramers found in "
            "1926: his paper's title is \"wave mechanics and half-integer quantization.\""
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(lin), Create(ax), Create(ai), FadeIn(ail), Create(tp))
            vo.wait_until("b")
            self.play(Create(wl), FadeIn(q), FadeIn(ql))
            vo.wait_until("c")
            self.play(Write(cond[0]))
            self.play(Write(cond[1]))
            vo.wait_until("d")
            self.play(FadeIn(hist))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        w = load("wkb")
        E, wkb, old = w["E"], w["wkb"], w["old"]
        ns = [0, 1, 2, 3, 5, 10, 20]
        rows = []
        for n in ns:
            err = (wkb[n] - E[n]) / E[n]
            rows.append([str(n), f"{E[n]:.4f}", f"{wkb[n]:.4f}", f"{100 * err:+.3f}\\%".replace("+", "{+}").replace("-", "{-}"),
                         f"{old[n]:.3f}" if n else "0"])
        tab = num_table([r"n", r"E_n\ \text{exact}", r"\text{WKB } (n + \tfrac12)", r"\text{error}", r"\text{old rule } (n)"], rows,
                        font_size=30, col_colors=[WHITE, WHITE, C.APPROX, C.APPROX, GREY_B]).move_to(UP * 0.1)
        assert abs((wkb[10] - E[10]) / E[10]) < 4e-4 and abs((wkb[0] - E[0]) / E[0]) > 0.15
        title = label(r"$H = p^2/2 + x^4$: exact energies vs.\ the quantum condition", font_size=30, color=GREY_A).to_edge(UP, buff=0.5)
        msg = label(r"WKB is a short-wavelength approximation: it gets better with every node", font_size=28, color=C.APPROX).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The test: exact energies against this rule. <bookmark mark='a'/> The ground state is off by eighteen "
            "percent: it has barely one bump, hardly a short wavelength. <bookmark mark='b'/> But by the tenth state the "
            "error is three parts in ten thousand, and by the twentieth it's less than one in ten thousand. "
            "<bookmark mark='c'/> The old rule, without the half, is wrong at every n."
        ) as vo:
            self.play(FadeIn(title), FadeIn(tab.header), Create(tab.rule), FadeIn(tab.rows[0]))
            vo.wait_until("a")
            self.play(Indicate(tab.rows[0], color=C.APPROX))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tab.rows[1:]], lag_ratio=0.3), run_time=2)
            self.play(FadeIn(msg))
            vo.wait_until("c")
            self.play(Indicate(tab.cols[4], color=GREY_A))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def phase_space(self):
        w = load("wkb")
        E = w["E"]
        ax = plain_axes((-2.6, 2.6), (-8.5, 8.5), 5.2, 5.8).move_to(LEFT * 3.6 + DOWN * 0.35)
        xl = MathTex("x", font_size=30, color=C.XPOS).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        pl = MathTex("p", font_size=30, color=C.MOMENTUM).next_to(ax.y_axis.get_end(), UP, buff=0.1)

        def orbit(En, n=400):
            a = En ** 0.25
            xs = a * np.sin(np.linspace(-np.pi / 2, np.pi / 2, n))
            ps = np.sqrt(np.clip(2 * (En - xs**4), 0, None))
            X = np.concatenate([xs, xs[::-1]])
            P = np.concatenate([ps, -ps[::-1]])
            return X, P

        rings = VGroup()
        cols = [C.CLASSICAL] * 6
        for n in range(6):
            X, P = orbit(E[n])
            pts = [ax.c2p(a, b) for a, b in zip(X, P)]
            rings.add(Polygon(*pts, stroke_color=cols[n], stroke_width=2.5, fill_opacity=0))
        shade = VGroup()
        for n in range(5, 0, -1):
            X, P = orbit(E[n])
            shade.add(Polygon(*[ax.c2p(a, b) for a, b in zip(X, P)], stroke_width=0, fill_color=C.HBAR, fill_opacity=0.08))
        txt = VGroup(
            MathTex(r"\text{area of orbit } n", r"=", r"\big(n + \tfrac12\big)\,h", font_size=34),
            label(r"neighbors differ by exactly $h$:", font_size=26),
            label(r"one quantum state per cell of area $h$", font_size=26, color=C.HBAR),
        ).arrange(DOWN, buff=0.28).move_to(RIGHT * 3.3 + UP * 2.0)
        txt[0][2].set_color(C.HBAR)
        areas = w["areas"] / (2 * np.pi)
        assert np.all(np.abs(areas[2:6] - (np.arange(2, 6) + 0.5)) < 0.02)
        nums = note(r"computed areas$/h$: " + ", ".join(f"{a:.3f}" for a in areas)).next_to(txt, DOWN, buff=0.2)
        # the Wigner function of n = 8 on its orbit
        W = w["wig"]
        wx, wp = w["wig_x"], w["wig_p"]
        cx, cp = np.abs(wx) <= 2.6, np.abs(wp) <= 8.5
        W = W[np.ix_(cp, cx)]
        bx = plain_axes((-2.6, 2.6), (-8.5, 8.5), 3.2, 3.6).move_to(RIGHT * 4.6 + DOWN * 1.75)
        img = signed_img(W[::-1], height=3.6, width=3.2).move_to(bx)
        X8, P8 = orbit(E[8])
        orb8 = VMobject(stroke_color=C.CLASSICAL, stroke_width=2).set_points_as_corners([bx.c2p(a, b) for a, b in zip(X8, P8)])
        orb8.set_stroke(opacity=0.8)
        wl = label(r"Wigner function of $n = 8$\\(amber $> 0$, blue $< 0$)", font_size=22, color=GREY_A).next_to(bx, LEFT, buff=0.25)
        with self.voiceover(
            "And here's the geometry. <bookmark mark='a'/> Each energy level is a closed orbit in phase space, "
            "<bookmark mark='b'/> and the orbit for level n encloses an area of n plus one half times h. Consecutive "
            "orbits are separated by exactly one h of area: each quantum state occupies one cell of size h. Phase equals "
            "area over h-bar, one more time. <bookmark mark='c'/> And the Wigner function of the eighth state, computed "
            "from the exact wavefunction, lies right along its classical orbit, with interference ripples inside."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(pl))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(shade), FadeIn(txt), FadeIn(nums))
            vo.wait_until("c")
            self.play(FadeIn(img), Create(orb8), FadeIn(wl))
        self.wait(0.4)
        self.clear_scene()
