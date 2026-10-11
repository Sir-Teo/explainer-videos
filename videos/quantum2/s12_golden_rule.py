from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum2.common import (label, ladder, lframe, load, mtex, note, plain_axes, polyline, tick_labels, why)
from videos.quantum2.compute import GOLD


class GoldenRule(VoiceoverScene):
    def construct(self):
        self.first_order()
        self.sinc()
        self.rate()
        self.exact_test()
        self.lineshape()
        self.hydrogen()

    # ------------------------------------------------------------------
    def first_order(self):
        rows = [
            MathTex(r"\ket{\psi(t)}", r"=", r"\sum_n c_n(t)\,e^{-iE_nt/\hbar}\ket{n}", font_size=38),
            MathTex(r"i\hbar\,\dot c_f", r"=", r"\sum_n V_{fn}\,e^{i\omega_{fn}t}\,c_n,\qquad \omega_{fn} = \frac{E_f - E_n}{\hbar}", font_size=36),
            MathTex(r"c_f(t)", r"\approx", r"-\frac{i}{\hbar}\int_0^t V_{fi}\,e^{i\omega t'}\,dt'", font_size=38),
            MathTex(r"|c_f(t)|^2", r"=", r"\frac{|V_{fi}|^2}{\hbar^2}\;\frac{\sin^2(\omega t/2)}{(\omega/2)^2}", font_size=42),
        ]
        rows[0][2].set_color(C.QTIME)
        rows[3][2].set_color(C.PERTURB)
        whys = [
            why(rows[0], r"each energy component's clock factored out"),
            why(rows[1], r"exact: the Schr\"odinger equation for the $c$'s"),
            why(rows[2], r"first order: start in $i$, so $c_n \approx \delta_{ni}$"),
            why(rows[3], r"$V$ switched on at $t = 0$, then constant"),
        ]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-1.6, buff=0.55)
        with self.voiceover(
            "So far, energies. Now rates: how fast do things happen? Let a perturbation V act on a system that starts in "
            "state i. <bookmark mark='a'/> Write the state as a sum over energy eigenstates, with each one's clock "
            "factored out. <bookmark mark='b'/> The exact equations for the coefficients involve V's matrix elements, "
            "times phases turning at the Bohr frequencies. <bookmark mark='c'/> To first order, the amplitude to have "
            "jumped to state f is an integral of V times that turning phase."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        with self.voiceover(
            "<bookmark mark='a'/> For a perturbation switched on at time zero and then held fixed, the integral is "
            "elementary, and the probability is V's matrix element squared, over h-bar squared, times this function of "
            "the detuning, omega."
        ) as vo:
            vo.wait_until("a")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sinc(self):
        t = ValueTracker(2.0)
        w = np.linspace(-8, 8, 1601)
        ax = plain_axes((-8, 8), (0, 26), 10.0, 4.6).move_to(DOWN * 0.7)
        wl = MathTex(r"\omega", font_size=30).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)

        def F(tt):
            with np.errstate(divide="ignore", invalid="ignore"):
                f = np.where(np.abs(w) < 1e-9, tt**2, np.sin(w * tt / 2) ** 2 / (w / 2) ** 2)
            return f

        curve = always_redraw(lambda: polyline(ax, w, np.minimum(F(t.get_value()), 26), color=C.PERTURB, stroke_width=4))
        area = always_redraw(lambda: Polygon(*[ax.c2p(a, min(b, 26)) for a, b in zip(w[::4], F(t.get_value())[::4])], ax.c2p(8, 0), ax.c2p(-8, 0),
                                             stroke_width=0, fill_color=C.PERTURB, fill_opacity=0.18))
        tl = always_redraw(lambda: MathTex(f"t = {t.get_value():.1f}", font_size=32, color=C.QTIME).to_corner(DR, buff=0.5))
        f1 = MathTex(r"\frac{\sin^2(\omega t/2)}{(\omega/2)^2}", font_size=40, color=C.PERTURB).to_edge(UP, buff=0.35).shift(LEFT * 3)
        props = VGroup(
            MathTex(r"\text{height } t^2", font_size=30),
            MathTex(r"\text{width} \sim 2\pi/t", font_size=30),
            MathTex(r"\text{area } 2\pi t", font_size=30, color=C.PERTURB),
            MathTex(r"\longrightarrow\; 2\pi t\;\delta(\omega)", font_size=34, color=C.PERTURB),
        ).arrange(RIGHT, buff=0.55).next_to(f1, RIGHT, buff=0.6)
        with self.voiceover(
            "This function controls everything. <bookmark mark='a'/> As time goes on, its peak grows like t squared, "
            "while its width shrinks like one over t. <bookmark mark='b'/> So its area grows exactly like t, "
            "<bookmark mark='c'/> and the function concentrates into a spike: two pi t times a delta function."
        ) as vo:
            self.add(curve, area, tl)
            self.play(Write(f1), Create(ax), FadeIn(wl), FadeIn(curve), FadeIn(area), FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(props[0]), FadeIn(props[1]), t.animate.set_value(3.5), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(props[2]), t.animate.set_value(5.0), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(props[3]))
        for m in (curve, area, tl):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def rate(self):
        r1 = MathTex(r"P(t)", r"=", r"\sum_f |c_f|^2 \approx \int \rho(E_f)\,\frac{|V_{fi}|^2}{\hbar^2}\,\frac{\sin^2(\omega t/2)}{(\omega/2)^2}\,\hbar\,d\omega", font_size=36)
        r2 = MathTex(r"P(t)", r"\approx", r"\frac{2\pi}{\hbar}\,|V_{fi}|^2\,\rho(E_f)\;t", font_size=40)
        r3 = MathTex(r"\Gamma", r"=", r"\frac{2\pi}{\hbar}\,|V_{fi}|^2\,\rho(E_f)", font_size=56)
        g = VGroup(r1, r2, r3).arrange(DOWN, buff=0.6).move_to(UP * 0.4)
        r3.set_color(C.PERTURB)
        box = SurroundingRectangle(r3, color=C.PERTURB, buff=0.2, corner_radius=0.12)
        one = label(r"one final state: the probability just sloshes back and forth", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        name = note(r"Dirac (1927); ``Golden Rule No.\ 2'' in Fermi's \emph{Nuclear Physics} (1950)").next_to(box, DOWN, buff=0.35)
        with self.voiceover(
            "<bookmark mark='a'/> If there's just one final state, that means nothing much: the probability sloshes back "
            "and forth. <bookmark mark='b'/> But if the final states form a continuum, with rho states per unit energy, "
            "adding up the spike over all of them <bookmark mark='c'/> gives a probability that grows in proportion to "
            "t: a constant rate. <bookmark mark='d'/> Gamma equals two pi over h-bar, times V squared, times the density "
            "of states. Dirac derived it in 1927; Fermi called it the golden rule."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(one))
            vo.wait_until("b")
            self.play(Write(r1))
            vo.wait_until("c")
            self.play(Write(r2))
            vo.wait_until("d")
            self.play(Write(r3), Create(box), FadeIn(name))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def exact_test(self):
        g = load("golden")
        t, P0, Gam = g["t"], g["P0"], float(g["Gamma"])
        fit = float(g["fit_rate"])
        assert abs(fit / Gam - 1) < 0.01
        # the comb of levels and the one coupled level
        comb = VGroup(*[Line(LEFT * 0.35, RIGHT * 0.35, color=C.ENERGY, stroke_width=1.5).move_to(LEFT * 5.6 + UP * (k * 0.05 - 0.35))
                        for k in range(-50, 51)])
        lvl = Line(LEFT * 0.45, RIGHT * 0.45, color=C.BORN, stroke_width=5).move_to(LEFT * 4.2 + DOWN * 0.35)
        cpl = VGroup(*[Line(lvl.get_left(), comb[k].get_right(), color=C.PERTURB, stroke_width=0.8).set_stroke(opacity=0.4) for k in range(0, 101, 4)])
        cl = label(r"601 levels, spacing $\delta$\\(dense ladder, only part shown)", font_size=20, color=C.ENERGY).next_to(comb, DOWN, buff=0.15)
        ll = label(r"start here", font_size=20, color=C.BORN).next_to(lvl, DOWN, buff=0.12)
        Vl = MathTex(r"V", font_size=28, color=C.PERTURB).move_to(LEFT * 4.85 + UP * 0.55)
        ax = Axes(x_range=[0, 150, 25], y_range=[-4, 0.15, 1], x_length=8.4, y_length=5.0, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(RIGHT * 2.0 + DOWN * 0.3)
        tks = VGroup(tick_labels(ax, xs=(0, 25, 50, 75, 100, 125, 150)), tick_labels(ax, ys=(-4, -3, -2, -1, 0), fmt=lambda v: "1" if v == 0 else f"10^{{{int(v)}}}"))
        logP = np.log10(np.maximum(P0, 1e-4))
        k = ValueTracker(0)
        cur = always_redraw(lambda: polyline(ax, t[: int(k.get_value()) + 2], logP[: int(k.get_value()) + 2], color=C.BORN, stroke_width=3.5))
        tt = np.linspace(0, 32, 200)
        gr = DashedLine(ax.c2p(0, 0), ax.c2p(4 / (Gam * np.log10(np.e)), -4), color=C.PERTURB, stroke_width=3)
        grl = MathTex(r"e^{-\Gamma t},\ \Gamma = \frac{2\pi V^2}{\hbar\delta}", font_size=28, color=C.PERTURB).next_to(ax.c2p(38, -0.9), RIGHT, buff=0.1)
        fr = lframe(ax)
        yl = MathTex(r"P_{\text{stay}}(t)", font_size=30, color=C.BORN).next_to(fr[1].get_end(), UP, buff=0.1)
        xl = MathTex(r"t", font_size=30, color=C.QTIME).next_to(fr[0].get_end(), RIGHT, buff=0.1)
        fitl = MathTex(r"\text{measured rate: } " + f"{fit:.4f}" + r"\ \text{vs.}\ " + f"{Gam:.4f}", font_size=26, color=C.PERTURB).next_to(grl, DOWN, buff=0.15).align_to(grl, LEFT)
        Tr = float(g["T_rev"])
        rev = DashedLine(ax.c2p(Tr, -4), ax.c2p(Tr, 0.1), color=C.QTIME)
        revl = MathTex(r"t = \frac{2\pi\hbar}{\delta}", font_size=26, color=C.QTIME).next_to(ax.c2p(Tr, -3.3), LEFT, buff=0.15)
        units = note(r"$\hbar = 1$, $\delta = 0.05$, $V = 0.05$; exact solution (eigen-decomposition of the $602 \times 602$ matrix)").to_edge(DOWN, buff=0.2)
        n_end = int(np.searchsorted(t, 40))
        with self.voiceover(
            "Let's test it, exactly. <bookmark mark='a'/> One level, coupled with the same strength to 601 evenly spaced "
            "levels. <bookmark mark='b'/> Solve the Schrödinger equation exactly, and watch the probability of staying "
            "put, on a logarithmic scale. <bookmark mark='c'/> It falls off exponentially, at a rate within one percent "
            "of the golden rule's."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(comb), FadeIn(lvl), FadeIn(cl), FadeIn(ll), Create(cpl), FadeIn(Vl), FadeIn(units))
            vo.wait_until("b")
            self.add(cur)
            self.play(Create(fr), FadeIn(tks), FadeIn(yl), FadeIn(xl))
            self.play(k.animate.set_value(n_end), run_time=3, rate_func=linear)
            vo.wait_until("c")
            self.play(Create(gr), FadeIn(grl), FadeIn(fitl))
        with self.voiceover(
            "<bookmark mark='a'/> Then, at two pi h-bar over the level spacing, every phase lines up again, and the "
            "probability comes back. A finite ladder of levels is not a true continuum; it only acts like one for times "
            "shorter than that."
        ) as vo:
            vo.wait_until("a")
            self.play(k.animate.set_value(len(t) - 2), run_time=4, rate_func=linear)
            self.play(Create(rev), FadeIn(revl))
        cur.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lineshape(self):
        g = load("golden")
        Ej, pj, lor, Gam = g["Ej"], g["pj"], g["lor"], float(g["Gamma"])
        sel = np.abs(Ej) < 2.0
        ax = plain_axes((-2, 2), (0, 1.15), 9.0, 4.0).move_to(DOWN * 0.5)
        sc_ = 1 / lor.max()
        bars = VGroup(*[Line(ax.c2p(e, 0), ax.c2p(e, p * sc_), color=C.ENERGY, stroke_width=2.5) for e, p in zip(Ej[sel], pj[sel])])
        lc = polyline(ax, np.linspace(-2, 2, 400), GOLD["V"] ** 2 / (np.linspace(-2, 2, 400) ** 2 + Gam**2 / 4) * sc_, color=C.PERTURB, stroke_width=3)
        half = BraceBetweenPoints(ax.c2p(-Gam / 2, 0.52), ax.c2p(Gam / 2, 0.52), direction=UP, color=C.PERTURB)
        hl = MathTex(r"\hbar\Gamma", font_size=30, color=C.PERTURB).next_to(half, RIGHT, buff=0.3).shift(UP * 0.25)
        el = MathTex(r"E_f", font_size=30, color=C.ENERGY).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        t1 = label(r"where the probability went: the populations of the 601 levels after the decay", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        t2 = MathTex(r"\text{a Lorentzian of full width } \hbar\Gamma:\quad \Delta E\cdot\tau = \hbar", font_size=34, color=C.PERTURB).next_to(t1, DOWN, buff=0.3)
        short = label(r"a short lifetime means a broad line", font_size=28).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "And the energy of whatever was emitted is spread out. <bookmark mark='a'/> Here are the populations of the "
            "601 levels after the decay: <bookmark mark='b'/> a Lorentzian line whose full width is exactly h-bar gamma. "
            "<bookmark mark='c'/> A short lifetime means a broad line."
        ) as vo:
            self.play(FadeIn(t1), Create(ax), FadeIn(el))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.01), run_time=2)
            vo.wait_until("b")
            self.play(Create(lc), GrowFromCenter(half), FadeIn(hl), Write(t2))
            vo.wait_until("c")
            self.play(FadeIn(short))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hydrogen(self):
        n = load("numbers")
        tau, A, cyc = float(n["tau_2p"]), float(n["A_2p"]), float(n["Q_lyman"]) / (2 * np.pi)
        assert abs(tau * 1e9 - 1.596) < 0.002 and 3.8e6 < cyc < 4.1e6
        r1 = MathTex(r"\Gamma_{2p \to 1s}", r"=", r"\frac{2\pi}{\hbar}\,|V|^2\,\rho", r"\;\longrightarrow\;",
                     r"\frac{\omega^3\,|\bra{1s}e\hat{\mathbf r}\ket{2p}|^2}{3\pi\varepsilon_0\hbar c^3}", font_size=36).to_edge(UP, buff=0.6)
        r1[4].set_color(C.PERTURB)
        w = label(r"the continuum: the photon modes of the vacuum, $\rho \propto \omega^2$", font_size=26, color=GREY_A).next_to(r1, DOWN, buff=0.3)
        d = MathTex(r"\bra{1s}z\ket{2p_0} = \frac{128\sqrt2}{243}\,a_0 = 0.745\,a_0", font_size=34).next_to(w, DOWN, buff=0.45)
        res = MathTex(r"\Gamma = " + f"{A / 1e8:.3f}" + r"\times 10^{8}\ \text{s}^{-1}", r"\quad\Rightarrow\quad", r"\tau = " + f"{tau * 1e9:.3f}" + r"\ \text{ns}",
                      font_size=40).next_to(d, DOWN, buff=0.55)
        res[2].set_color(C.QTIME)
        meas = label(r"measured (NIST): 1.596 ns", font_size=28, color=WHITE).next_to(res, DOWN, buff=0.3)
        slosh = label(r"in that time the charge cloud sloshes " + f"{cyc / 1e6:.1f}" + r" million times at Lyman-$\alpha$ ("
                      + f"{float(n['lyman_alpha_nm']):.1f}" + r" nm)", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In an atom, the continuum is the electromagnetic field itself. <bookmark mark='a'/> An excited hydrogen "
            "atom in its 2p state is coupled to the vacuum's photon modes, whose density grows like the frequency "
            "squared. <bookmark mark='b'/> Put in the dipole matrix element, <bookmark mark='c'/> and the golden rule "
            "gives a lifetime of 1.596 nanoseconds, <bookmark mark='d'/> matching measurement. <bookmark mark='e'/> In "
            "that time the electron cloud sloshes about four million times, at the Lyman-alpha frequency, before the "
            "light gets out."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(r1), FadeIn(w))
            vo.wait_until("b")
            self.play(Write(d))
            vo.wait_until("c")
            self.play(Write(res))
            vo.wait_until("d")
            self.play(FadeIn(meas))
            vo.wait_until("e")
            self.play(FadeIn(slosh))
        self.wait(0.4)
        self.clear_scene()
