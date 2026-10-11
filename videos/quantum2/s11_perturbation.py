from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum2.common import (label, ladder, lframe, load, mtex, note, part_card, plain_axes, polyline, tick_labels, why)

PARITY = ["#7DD3FC", "#FCA5A5", "#BEF264", "#FDE68A"]  # the four (n1, n2) parity classes of the drum


class Perturbation(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_()
        self.derivation()
        self.stark()
        self.repulsion()
        self.drum()
        self.divergence()

    # ------------------------------------------------------------------
    def card(self):
        c = part_card(3, r"Approximations", r"how real atoms are computed")
        with self.voiceover("Part 3: Approximations."):
            self.play(FadeIn(c))
        self.wait(0.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def setup_(self):
        h = MathTex(r"\hat H", r"=", r"\hat H_0", r"+", r"\lambda\hat V", font_size=64).move_to(UP * 0.6)
        h[2].set_color(C.ENERGY)
        h[4].set_color(C.PERTURB)
        b0 = label(r"solved exactly", font_size=28, color=C.ENERGY).next_to(h[2], DOWN, buff=0.5)
        b1 = label(r"small", font_size=28, color=C.PERTURB).next_to(h[4], DOWN, buff=0.5)
        # three exactly solvable wells, each with its lowest levels; then the small changes that spoil them
        def well(center, V, levels, xr=1.3):
            o = np.array(center)
            xs = np.linspace(-xr, xr, 161)
            pot = VMobject(stroke_color=C.POTENTIAL, stroke_width=3).set_points_as_corners([o + np.array([x, V(x), 0]) for x in xs])
            lv = VGroup()
            for E in levels:
                inside = xs[V(xs) <= E]
                lv.add(Line(o + np.array([inside[0], E, 0]), o + np.array([inside[-1], E, 0]), color=C.ENERGY, stroke_width=3))
            return VGroup(pot, lv)

        box = lambda x: np.where(np.abs(x) < 1.2, -1.0, 1.1)  # noqa: E731
        osc = lambda x: -1.0 + 1.5 * (x / 1.3) ** 2  # noqa: E731
        cou = lambda x: np.maximum(-0.22 / np.maximum(np.abs(x), 1e-3), -1.15)  # noqa: E731
        tilt = lambda x: np.where(np.abs(x) < 1.2, -1.0 - 0.45 * x, 1.1)  # noqa: E731
        anh = lambda x: -1.0 + 1.5 * (x / 1.3) ** 2 - 0.55 * (x / 1.3) ** 3 + 0.5 * (x / 1.3) ** 4  # noqa: E731
        cx = (-4.5, 0.0, 4.5)
        solv = VGroup(well((cx[0], 0.9, 0), box, [-1.0 + 0.2 * n * n for n in (1, 2, 3)]),
                      well((cx[1], 0.9, 0), osc, [-1.0 + 0.36 * (n + 0.5) for n in (0, 1, 2)]),
                      well((cx[2], 0.9, 0), cou, [-0.88, -0.22, -0.098]))
        spoil = VGroup(well((cx[0], 0.9, 0), tilt, []), well((cx[1], 0.9, 0), anh, []), well((cx[2], 0.9, 0), cou, []))
        names = VGroup(*[label(t, font_size=28, color=GREY_A).move_to(RIGHT * x + DOWN * 0.75) for t, x in zip(("box", "oscillator", "hydrogen"), cx)])
        names2 = VGroup(*[label(t, font_size=28, color=GREY_A).move_to(RIGHT * x + DOWN * 0.75) for t, x in zip(("box in a field", "a different shape", "helium"), cx)])
        e2 = VGroup(*[Dot(RIGHT * (cx[2] + dx) + UP * (0.9 - 0.88), radius=0.08, color=C.FERMION) for dx in (-0.12, 0.12)])
        q = VGroup(*[MathTex(r"?", font_size=48, color=C.PERTURB).move_to(RIGHT * x + UP * 1.75) for x in cx])
        ok = label(r"solved exactly", font_size=30, color=C.ENERGY).move_to(DOWN * 1.6)
        no = label(r"no exact solution", font_size=30, color=C.PERTURB).move_to(DOWN * 1.6)
        with self.voiceover(
            "The box, the oscillator and hydrogen are almost the only systems we can solve exactly. <bookmark mark='p'/> "
            "Add a second electron, an electric field, or a slightly different shape, and exact solutions vanish. So most "
            "of quantum mechanics is approximation, done carefully. <bookmark mark='a'/> The workhorse is perturbation "
            "theory: split the Hamiltonian into a part we can solve, H zero, <bookmark mark='b'/> plus a small extra "
            "piece, lambda V."
        ) as vo:
            self.play(LaggedStart(*[Create(w) for w in solv], lag_ratio=0.3), FadeIn(names), FadeIn(ok), run_time=2.4)
            vo.wait_until("p")
            self.play(*[Transform(solv[i][0], spoil[i][0]) for i in range(3)], *[FadeOut(solv[i][1]) for i in range(3)],
                      Transform(names, names2), FadeIn(e2), FadeIn(q), Transform(ok, no), run_time=1.8)
            vo.wait_until("a")
            self.play(FadeOut(VGroup(solv, names, e2, q, ok)), run_time=0.6)
            self.play(Write(h[:3]), FadeIn(b0))
            vo.wait_until("b")
            self.play(Write(h[3:]), FadeIn(b1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derivation(self):
        rows = [
            MathTex(r"(\hat H_0 + \lambda\hat V)\big(\ket{n^0} + \lambda\ket{n^1} + \dots\big)", r"=",
                    r"\big(E^0 + \lambda E^1 + \lambda^2E^2 + \dots\big)\big(\ket{n^0} + \lambda\ket{n^1} + \dots\big)", font_size=32),
            MathTex(r"\lambda^1:\quad \hat H_0\ket{n^1} + \hat V\ket{n^0}", r"=", r"E^0\ket{n^1} + E^1\ket{n^0}", font_size=36),
            MathTex(r"E^1_n", r"=", r"\bra{n^0}\hat V\ket{n^0}", font_size=40),
            MathTex(r"\braket{m^0}{n^1}", r"=", r"\frac{\bra{m^0}\hat V\ket{n^0}}{E^0_n - E^0_m}", font_size=38),
            MathTex(r"E^2_n", r"=", r"\sum_{m\neq n}\frac{|\bra{m^0}\hat V\ket{n^0}|^2}{E^0_n - E^0_m}", font_size=40),
        ]
        for i in (2, 4):
            rows[i][0].set_color(C.ENERGY)
            rows[i][2].set_color(C.PERTURB)
        whys = [
            why(rows[0], r"expand everything in powers of $\lambda$"),
            why(rows[1], r"match the first power of $\lambda$"),
            why(rows[2], r"project on $\bra{n^0}$: the $\hat H_0$ terms cancel ($\hat H_0$ Hermitian)"),
            why(rows[3], r"project on $\bra{m^0}$, $m \ne n$"),
            why(rows[4], r"second order: ground state $\Rightarrow$ every term negative"),
        ]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-1.6, buff=0.5)
        hist = note(r"Rayleigh (1877, vibrating strings); Schr\"odinger (1926, Part III: the Stark effect)").to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Expand both the energy and the state in powers of lambda, put them into the eigenvalue "
            "equation, and match powers. <bookmark mark='b'/> At first order, take the inner product with the "
            "unperturbed state. Because H zero is Hermitian, its terms cancel, <bookmark mark='c'/> and the first-order "
            "energy shift is simply the average of V in the unperturbed state."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        with self.voiceover(
            "<bookmark mark='a'/> Taking the inner product with any other state m gives the first-order change of the "
            "state: V's matrix element, divided by the energy difference. <bookmark mark='b'/> And at second order, the "
            "energy shift is a sum of squared matrix elements over energy differences. For the ground state every "
            "denominator is negative, so second order always pushes the ground state down."
        ) as vo:
            vo.wait_until("a")
            step(3)
            vo.wait_until("b")
            step(4)
            self.play(FadeIn(hist))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stark(self):
        p = load("perturb")
        F, ex, E0, e2 = p["stark_F"], p["stark_exact"], float(p["stark_E0"]), float(p["stark_e2"])
        theory = -(15 - np.pi**2) / (24 * np.pi**4)
        assert abs(e2 / theory - 1) < 1e-4
        sel = F <= 70
        ax = plain_axes((0, 70), (-11, 0.5), 7.0, 4.6).move_to(LEFT * 3.1 + DOWN * 0.6)
        fr = lframe(ax)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(70, 0), color=GREY_D, stroke_width=1.5)
        tks = tick_labels(ax, xs=(0, 20, 40, 60), ys=(-10, -5, 0))
        xl = MathTex(r"F", font_size=30, color=C.PERTURB).next_to(fr[0].get_end(), RIGHT, buff=0.1)
        yl = MathTex(r"E_1(F) - E_1(0)", font_size=28, color=C.ENERGY).next_to(fr[1].get_end(), UP, buff=0.12).align_to(fr[1], LEFT)
        exact = polyline(ax, F[sel], ex[sel] - E0, color=WHITE, stroke_width=4)
        ff = np.linspace(0, 70, 200)
        par = polyline(ax, ff, np.maximum(e2 * ff**2, -11), color=C.APPROX, stroke_width=3)
        r1 = MathTex(r"\hat V = F\,(x - \tfrac L2)", font_size=34)
        r2 = MathTex(r"E^1_1 = F\,\langle x - \tfrac L2\rangle = 0", font_size=32)
        r3 = MathTex(r"E^2_1 = -\frac{15 - \pi^2}{24\pi^4}\,F^2", font_size=34, color=C.APPROX)
        r4 = MathTex(r"= " + f"{e2:.7f}" + r"\,F^2", font_size=30, color=C.APPROX)
        r5 = VGroup(note(r"the sum over 59 states, computed: " + f"{e2:.7f}"), note(r"closed form: " + f"{theory:.7f}")).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        col = VGroup(r1, r2, r3, r4, r5).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        r4.shift(RIGHT * (r3[0][3].get_center()[0] - r4[0][0].get_center()[0]))  # line up the '=' signs
        col.to_edge(RIGHT, buff=0.45).to_edge(UP, buff=0.5)
        leg = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.4, color=WHITE, stroke_width=4), label(r"exact", font_size=24)).arrange(RIGHT, buff=0.12),
                     VGroup(Line(ORIGIN, RIGHT * 0.4, color=C.APPROX, stroke_width=4), label(r"second order", font_size=24, color=C.APPROX)).arrange(RIGHT, buff=0.12)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(ax.c2p(3, -9.5), RIGHT, buff=0.1)
        units = note(r"particle in a box of width $L = 1$, $\hbar = m = 1$").to_corner(DL, buff=0.25)
        with self.voiceover(
            "Try it on a particle in a box, in a uniform field F. <bookmark mark='a'/> The first-order shift is zero: by "
            "symmetry, the average of x minus L over two vanishes. <bookmark mark='b'/> The second-order sum can be done "
            "in closed form: minus fifteen minus pi squared, over twenty-four pi to the fourth, times F squared. "
            "<bookmark mark='c'/> The computed sum agrees to six digits, <bookmark mark='d'/> and the exact energy follows "
            "the parabola at small fields, before higher orders take over."
        ) as vo:
            self.play(Write(r1), FadeIn(units))
            vo.wait_until("a")
            self.play(Write(r2))
            vo.wait_until("b")
            self.play(Write(r3))
            vo.wait_until("c")
            self.play(FadeIn(r4), FadeIn(r5))
            vo.wait_until("d")
            self.play(Create(fr), Create(zero), FadeIn(tks), FadeIn(xl), FadeIn(yl), FadeIn(leg))
            self.play(Create(exact), Create(par), run_time=2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def repulsion(self):
        V = 0.45
        ax = plain_axes((-2.2, 2.2), (-2.4, 2.4), 6.2, 5.0).move_to(LEFT * 3.0 + DOWN * 0.4)
        lam = np.linspace(-2.2, 2.2, 300)
        d1 = DashedLine(ax.c2p(-2.2, -2.2), ax.c2p(2.2, 2.2), color=GREY_C)
        d2 = DashedLine(ax.c2p(-2.2, 2.2), ax.c2p(2.2, -2.2), color=GREY_C)
        up = polyline(ax, lam, np.sqrt(lam**2 + V**2), color=C.ENERGY, stroke_width=4)
        dn = polyline(ax, lam, -np.sqrt(lam**2 + V**2), color=C.ENERGY, stroke_width=4)
        gap = BraceBetweenPoints(ax.c2p(0.05, -V), ax.c2p(0.05, V), direction=RIGHT, color=C.PERTURB)
        gl = MathTex(r"2|V_{12}|", font_size=30, color=C.PERTURB).next_to(gap, RIGHT, buff=0.1)
        m = MathTex(r"\begin{pmatrix} E_1 & V_{12} \\ V_{12}^* & E_2\end{pmatrix}", r"\;\Rightarrow\;",
                    r"E_\pm = \bar E \pm \sqrt{\Big(\frac{E_1 - E_2}{2}\Big)^2 + |V_{12}|^2}", font_size=32).to_edge(UP, buff=0.4).shift(RIGHT * 2.3)
        msg = label(r"levels that come close push each other apart", font_size=28, color=C.PERTURB).move_to(RIGHT * 3.3 + DOWN * 0.6)
        unc = label(r"(uncoupled: dashed; they would cross)", font_size=22, color=GREY_B).next_to(msg, DOWN, buff=0.2)
        with self.voiceover(
            "Notice the energy differences in the denominators: when two levels come close, they push each other apart. "
            "<bookmark mark='a'/> For two levels it's exact: <bookmark mark='b'/> the eigenvalues are hyperbolas, and "
            "the closest approach is twice the coupling."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(m), Create(ax), Create(d1), Create(d2), FadeIn(unc))
            vo.wait_until("b")
            self.play(Create(up), Create(dn), GrowFromCenter(gap), FadeIn(gl), FadeIn(msg))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def drum(self):
        p = load("perturb")
        lam, sym, cls, gen = p["spag_lam"], p["spag_sym"], p["spag_cls"], p["spag_gen"]
        ymax = 140
        def panel(center):
            ax = plain_axes((0, 0.75), (0, ymax), 5.4, 4.6).move_to(center)
            return ax
        axl, axr = panel(LEFT * 3.5 + DOWN * 0.6), panel(RIGHT * 3.5 + DOWN * 0.6)
        lines_l = VGroup()
        for k in range(sym.shape[1]):
            # draw each level in short segments colored by the parity class of the state it holds
            for i in range(len(lam) - 1):
                if sym[i, k] < ymax and sym[i + 1, k] < ymax:
                    lines_l.add(Line(axl.c2p(lam[i], sym[i, k]), axl.c2p(lam[i + 1], sym[i + 1, k]), color=PARITY[cls[i, k]], stroke_width=3))
        lines_r = VGroup(*[polyline(axr, lam, np.minimum(gen[:, k], ymax + 5), color=WHITE, stroke_width=3) for k in range(gen.shape[1]) if gen[:, k].min() < ymax])
        for a in (axl, axr):
            a.add(MathTex(r"\lambda", font_size=28).next_to(a.x_axis.get_end(), RIGHT, buff=0.1))
        tl = label(r"a rectangle (separable)", font_size=28).next_to(axl, UP, buff=0.5)
        tr = label(r"the same, with a small dent", font_size=28).next_to(axr, UP, buff=0.5)
        # a little drum icon of each kind
        def drum_icon(dent=False):
            r = Rectangle(width=1.0, height=0.6, stroke_color=GREY_A, stroke_width=2)
            g = VGroup(r)
            if dent:
                g.add(Dot(r.get_center() + LEFT * 0.19 + DOWN * 0.08, radius=0.07, color=C.PERTURB))
            return g
        il, ir = drum_icon(False).next_to(tl, DOWN, buff=0.12), drum_icon(True).next_to(tr, DOWN, buff=0.12)
        sub = label(r"sides $e^{\lambda} \times e^{-\lambda}$: stretch at fixed area", font_size=22, color=GREY_B).to_edge(UP, buff=0.2)
        cl = label(r"colors: the symmetry class of each state (even/odd in $x$ and $y$)", font_size=22, color=GREY_B).next_to(axl, DOWN, buff=0.15)
        # zoom on the narrowest avoided crossing among the lowest levels shown
        gaps = np.diff(gen, axis=1)
        k = 1  # levels 2 and 3: an exact crossing without the dent, a wide gap with it
        i = int(np.argmin(gaps[:, k]))
        assert gaps[i, k] > 0.5 and np.diff(sym, axis=1)[:, k].min() < 0.05
        zc = axr.c2p(lam[i], 0.5 * (gen[i, k] + gen[i, k + 1]))
        zr = Square(side_length=0.6, color=C.PERTURB, stroke_width=2).move_to(zc)
        gl = MathTex(r"\text{gap} = " + f"{gaps[i, k]:.2f}", font_size=24, color=C.PERTURB).next_to(zr, RIGHT, buff=0.1)
        gl.add_background_rectangle(color=config.background_color, opacity=0.85, buff=0.06)
        res = label(r"same symmetry: never cross (von Neumann \& Wigner, 1929)", font_size=26, color=C.PERTURB).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "<bookmark mark='a'/> Here's a rectangular drum of fixed area, stretched one way and squeezed the other. "
            "<bookmark mark='b'/> Its levels cross freely, because the problem separates into x and y: states with "
            "different symmetries don't talk to each other. <bookmark mark='c'/> Add a small dent off-center, and the "
            "symmetry is gone. <bookmark mark='d'/> Every crossing opens up into a gap: levels of the same symmetry never "
            "cross. Wigner and von Neumann proved this in 1929."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tl), FadeIn(il), FadeIn(sub), Create(axl))
            vo.wait_until("b")
            self.play(Create(lines_l), FadeIn(cl), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(tr), FadeIn(ir), Create(axr))
            self.play(Create(lines_r), run_time=2.5)
            vo.wait_until("d")
            self.play(Create(zr), FadeIn(gl), FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def divergence(self):
        p = load("perturb")
        cf, err, gs = p["bw"], p["bw_err"], p["bw_g"]
        ser = MathTex(r"E_0(g)", r"=", r"\tfrac12 + \tfrac34 g - \tfrac{21}{8}g^2 + \tfrac{333}{16}g^3 - \tfrac{30885}{128}g^4 + \tfrac{916731}{256}g^5 - \cdots",
                      font_size=34).to_edge(UP, buff=0.35)
        hl = MathTex(r"\hat H = \tfrac12\hat p^2 + \tfrac12\hat x^2 + g\,\hat x^4", font_size=30).next_to(ser, DOWN, buff=0.2)
        ex = note(r"all 40 coefficients computed exactly, as fractions").next_to(hl, DOWN, buff=0.1)
        # left: |c_n| grows factorially
        axl = Axes(x_range=[0, 40, 10], y_range=[-1, 66, 20], x_length=5.4, y_length=3.9, tips=False,
                   axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(LEFT * 3.5 + DOWN * 1.35)
        nn = np.arange(len(cf))
        cdots = VGroup(*[Dot(axl.c2p(n, np.log10(abs(c))), radius=0.045, color=C.PERTURB) for n, c in zip(nn, cf)])
        tkl = VGroup(tick_labels(axl, xs=(0, 10, 20, 30, 40)), tick_labels(axl, ys=(0, 20, 40, 60), fmt=lambda v: "1" if v == 0 else f"10^{{{int(v)}}}"))
        frl = lframe(axl)
        ll = MathTex(r"|c_n|", font_size=28, color=C.PERTURB).next_to(frl[1].get_end(), UP, buff=0.05)
        nl = MathTex(r"n", font_size=28).next_to(frl[0].get_end(), RIGHT, buff=0.1)
        asym = MathTex(r"c_n \sim (-1)^{n+1}\,3^n\,\Gamma(n + \tfrac12)", font_size=26, color=C.PERTURB)
        asym.move_to(axl.c2p(0, 54), aligned_edge=LEFT).shift(RIGHT * 0.25)
        # right: error of the partial sums
        axr = Axes(x_range=[0, 40, 10], y_range=[-9, 6, 3], x_length=5.4, y_length=3.9, tips=False,
                   axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(RIGHT * 3.5 + DOWN * 1.35)
        tkr = VGroup(tick_labels(axr, xs=(0, 10, 20, 30, 40)), tick_labels(axr, ys=(-9, -6, -3, 0, 3, 6), fmt=lambda v: "1" if v == 0 else f"10^{{{int(v)}}}"))
        frr = lframe(axr)
        rl = label(r"error of the partial sum", font_size=24).next_to(frr[1].get_end(), UP, buff=0.05)
        nr = MathTex(r"n", font_size=28).next_to(frr[0].get_end(), RIGHT, buff=0.1)
        curves = VGroup()
        cols = [C.APPROX, C.ANGMOM]
        bests = VGroup()
        for i, col in zip((0, 1), cols):
            e = np.clip(np.log10(np.maximum(err[i], 1e-30)), -9, 6)
            keep = np.log10(np.maximum(err[i], 1e-30)) < 6.2
            curves.add(polyline(axr, nn[keep], e[keep], color=col, stroke_width=3))
            k, eb = p[f"bw_best_{i}"]
            bests.add(Dot(axr.c2p(k, np.log10(eb)), radius=0.08, color=col))
        b0 = p["bw_best_0"]
        assert int(b0[0]) == 16 and b0[1] < 4e-8
        gl = VGroup(MathTex(r"g = 0.02", font_size=26, color=cols[0]), MathTex(r"g = 0.05", font_size=26, color=cols[1])).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        gl.next_to(axr.c2p(25, -7), RIGHT, buff=0)
        dys = label(r"Dyson: for $g < 0$ the well opens up and the particle tunnels out, so $E_0(g)$ can't be smooth at $g = 0$",
                    font_size=22, color=GREY_A).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Last, a warning. For the anharmonic oscillator, the energy as a series in the coupling g can be computed "
            "exactly, to any order: <bookmark mark='a'/> one half, plus three quarters g, minus twenty-one eighths g "
            "squared, and on. <bookmark mark='b'/> But the coefficients grow like n factorial. The series converges for "
            "no value of g except zero: Bender and Wu proved it in 1969. <bookmark mark='c'/> Dyson saw why: flip the "
            "sign of g and the well opens up; the particle can tunnel out, and no smooth formula can cover both signs."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(ser), FadeIn(hl), FadeIn(ex))
            vo.wait_until("b")
            self.play(Create(frl), FadeIn(tkl), FadeIn(ll), FadeIn(nl), LaggedStart(*[FadeIn(d, scale=0.5) for d in cdots], lag_ratio=0.03), FadeIn(asym))
            vo.wait_until("c")
            self.play(FadeIn(dys))
        with self.voiceover(
            "Yet the partial sums are wonderfully accurate if you stop in time. <bookmark mark='a'/> At g equals 0.02, "
            "the error falls to three parts in a hundred million at order sixteen, then grows without bound. "
            "<bookmark mark='b'/> At g equals 0.05, the best you can do is order six. <bookmark mark='c'/> Perturbation "
            "series are asymptotic: use them, but stop at the smallest term."
        ) as vo:
            self.play(Create(frr), FadeIn(tkr), FadeIn(rl), FadeIn(nr))
            vo.wait_until("a")
            self.play(Create(curves[0]), FadeIn(bests[0]), FadeIn(gl[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(curves[1]), FadeIn(bests[1]), FadeIn(gl[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Flash(bests[0], color=cols[0]), Flash(bests[1], color=cols[1]))
        self.wait(0.4)
        self.clear_scene()
