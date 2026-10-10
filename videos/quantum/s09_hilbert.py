from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum.common import (WaveView, bar_chart, boxed, corner_wheel, frames_at, label, load, mtex, note, num,
                                   num_table, part_card, phasor, place_whys, polyline, stack, wave_axes, why, ylabel)
from videos.quantum.compute import box_E, box_phi
from videos.quantum.s06_box import walls


class HilbertSpace(VoiceoverScene):
    def construct(self):
        self.card()
        self.sampling()
        self.basis()
        self.matrix()
        self.hermitian()
        self.evolution()

    def card(self):
        c = part_card(3, r"The mathematical framework", r"states are vectors, observables are operators")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def sampling(self):
        c = load("carpet")
        x, mv = c["x"], c["movie"]
        psi = mv[4]  # the packet just after release: complex, with some structure
        ax = wave_axes((-0.02, 1.02), (-2.9, 2.9), x_length=6.2, y_length=3.6).move_to(LEFT * 3.2 + UP * 0.3)
        wv = WaveView(ax, x, psi, mode="real", scale=1.0, x_window=(0, 1))
        yl = ylabel(ax, r"\mathrm{Re}\,\psi", font_size=28)
        N = 9
        xs = np.linspace(0, 1, N + 2)[1:-1]
        vals = np.interp(xs, x, psi.real) + 1j * np.interp(xs, x, psi.imag)
        sticks = VGroup(*[Line(ax.c2p(xx, 0), ax.c2p(xx, v.real), color=WHITE, stroke_width=3) for xx, v in zip(xs, vals)])
        dots = VGroup(*[Dot(ax.c2p(xx, v.real), radius=0.05, color=WHITE) for xx, v in zip(xs, vals)])
        entries = [[rf"\psi_{{{i + 1}}}"] for i in range(N)]
        vec = Matrix(entries, element_to_mobject_config={"font_size": 30}, v_buff=0.42).scale(0.8)
        vec.move_to(RIGHT * 2.4 + UP * 0.5)
        vl = MathTex(r"\ket{\psi} \;=", font_size=38).next_to(vec, LEFT, buff=0.2)
        cn = MathTex(r"\in \mathbb{C}^N", font_size=36).next_to(vec, RIGHT, buff=0.2)
        ip = MathTex(r"\braket{f}{g}", r"=", r"\sum_i f_i^*\, g_i\,\Delta x", r"\;\xrightarrow{\;N\to\infty\;}\;",
                     r"\int f^*(x)\,g(x)\,dx", font_size=34).to_edge(DOWN, buff=1.0)
        nrm = MathTex(r"\braket{\psi}{\psi}", r"=", r"\int |\psi|^2\,dx", r"=", r"1", font_size=34, color=C.BORN).next_to(ip, DOWN, buff=0.22)
        with self.voiceover(
            "Step back and look at what we've been doing. A wavefunction is a list of complex numbers, one for each "
            "point. <bookmark mark='s'/> Sample it at N points, <bookmark mark='v'/> and it literally is a vector with N "
            "complex components. Shrink the spacing, and N goes to infinity. That's the right way to think about "
            "a quantum state: as a vector, written with this angle bracket, called a ket."
        ) as vo:
            self.play(Create(ax), FadeIn(wv), FadeIn(yl), FadeIn(walls(ax)))
            vo.wait_until("s")
            self.play(LaggedStart(*[AnimationGroup(Create(s_), FadeIn(d)) for s_, d in zip(sticks, dots)], lag_ratio=0.08),
                      wv.fade_to(0.35), run_time=1.6)
            vo.wait_until("v")
            self.play(TransformFromCopy(dots, vec.get_entries()), FadeIn(vec.get_brackets()), FadeIn(vl), FadeIn(cn),
                      run_time=1.8)
        with self.voiceover(
            "Vectors have dot products. <bookmark mark='i'/> For complex vectors you conjugate the first one, multiply "
            "component by component, and add. In the limit, the sum becomes an integral: the inner product of two "
            "wavefunctions. <bookmark mark='n'/> And the length squared of psi is exactly the total probability. A "
            "quantum state is a unit vector."
        ) as vo:
            vo.wait_until("i")
            self.play(Write(ip))
            vo.wait_until("n")
            self.play(Write(nrm))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def basis(self):
        x = np.linspace(0, 1, 600)
        ax1 = wave_axes((-0.02, 1.02), (-2.2, 2.2), x_length=5.4, y_length=2.4).move_to(LEFT * 3.4 + UP * 1.8)
        ax2 = wave_axes((-0.02, 1.02), (-2.2, 2.2), x_length=5.4, y_length=2.4).move_to(RIGHT * 3.4 + UP * 1.8)
        p23 = box_phi(2, x) * box_phi(3, x)
        p22 = box_phi(2, x) ** 2
        w23 = WaveView(ax1, x, p23.astype(complex), mode="real", scale=1.0, x_window=(0, 1))
        w22 = WaveView(ax2, x, p22.astype(complex), mode="real", scale=1.0, x_window=(0, 1))
        l23 = MathTex(r"\varphi_2\,\varphi_3", font_size=32).next_to(ax1, UP, buff=0.05)
        l22 = MathTex(r"\varphi_2\,\varphi_2", font_size=32).next_to(ax2, UP, buff=0.05)
        a23 = float(np.trapezoid(p23, x))
        a22 = float(np.trapezoid(p22, x))
        assert abs(a23) < 1e-9 and abs(a22 - 1) < 1e-6
        v23 = MathTex(r"\int = 0", font_size=32).next_to(ax1, DOWN, buff=0.1)
        v22 = MathTex(r"\int = 1", font_size=32).next_to(ax2, DOWN, buff=0.1)
        on = MathTex(r"\braket{\varphi_m}{\varphi_n}", r"=", r"\delta_{mn}", font_size=40).move_to(DOWN * 0.6)
        sgn = note(r"red: positive, cyan: negative (phase $0$ and $\pi$)").next_to(on, DOWN, buff=0.15)
        with self.voiceover(
            "The stationary states of the box make a natural set of axes. <bookmark mark='o'/> Multiply two different "
            "ones together and integrate: the positive and negative areas cancel exactly. <bookmark mark='s'/> Multiply "
            "one by itself and you get one. <bookmark mark='d'/> They're orthonormal: perpendicular unit vectors, in "
            "infinitely many dimensions."
        ) as vo:
            self.play(Create(ax1), Create(ax2))
            vo.wait_until("o")
            self.play(FadeIn(w23), FadeIn(l23))
            self.play(FadeIn(v23))
            vo.wait_until("s")
            self.play(FadeIn(w22), FadeIn(l22), FadeIn(v22))
            vo.wait_until("d")
            self.play(Write(on), FadeIn(sgn))
        self.clear_scene()

        c = load("carpet")
        ns, cs, xc, psi0 = c["ns"], c["cs"], c["x"], c["movie"][0]
        assert abs(np.sum(np.abs(cs) ** 2) - 1) < 1e-7
        ax = wave_axes((-0.02, 1.02), (0, 7.5), x_length=7.4, y_length=3.4).move_to(LEFT * 2.5 + DOWN * 0.3)
        n_t = ValueTracker(1)
        basis = np.array([box_phi(n, xc) for n in ns[:40]])

        def partial(n):
            return cs[:n] @ basis[:n]

        wv = WaveView(ax, xc, partial(1), mode="density", x_window=(0, 1))
        wv.add_updater(lambda m: m.set_psi(partial(int(n_t.get_value()))))
        ghost = polyline(ax, xc, np.abs(psi0) ** 2, color=GREY_B, stroke_width=1.5).set_stroke(opacity=0.6)
        ghost = DashedVMobject(ghost, num_dashes=80)
        exp = MathTex(r"\ket{\psi}", r"=", r"\sum_n c_n\ket{\varphi_n}", r",\qquad", r"c_n = \braket{\varphi_n}{\psi}",
                      font_size=38).to_edge(UP, buff=0.5)
        exp[4].set_color(C.ENERGY)
        cnt = always_redraw(lambda: MathTex(r"\text{terms: }" + str(int(n_t.get_value())), font_size=32)
                            .next_to(ax, RIGHT, buff=0.5).shift(UP * 1.0))
        pars = MathTex(r"\sum_n |c_n|^2 = 1", font_size=36, color=C.BORN).next_to(ax, RIGHT, buff=0.5).shift(DOWN * 0.4)
        parl = note(r"Pythagoras, in Hilbert space").next_to(pars, DOWN, buff=0.12)
        with self.voiceover(
            "Any wavefunction in the box can be written as a combination of these axes, <bookmark mark='c'/> and the "
            "coefficient along each axis is just the inner product: the shadow of psi on that axis. <bookmark mark='a'/> "
            "Adding the terms one by one rebuilds our narrow packet: one term, two, four, eight, sixteen, thirty-two."
        ) as vo:
            self.play(Write(exp[:3]), Create(ax), FadeIn(walls(ax)), Create(ghost))
            vo.wait_until("c")
            self.play(Write(exp[3:]))
            vo.wait_until("a")
            self.add(wv, cnt)
            for n in (2, 4, 8, 16, 32):
                self.play(n_t.animate.set_value(n), run_time=0.8, rate_func=lambda a: float(a >= 1))
                self.wait(0.35)
        with self.voiceover(
            "And since the axes are perpendicular, the squared lengths of the shadows add up to the squared length of "
            "the vector, which is one. That's Pythagoras' theorem, in a space with infinitely many dimensions. This "
            "space of wavefunctions is called a Hilbert space."
        ):
            self.play(Write(pars), FadeIn(parl))
        wv.clear_updaters()
        cnt.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def matrix(self):
        fd = load("fd")
        d1 = MathTex(r"\psi''(x_i)", r"\approx", r"\frac{\psi_{i+1} - 2\psi_i + \psi_{i-1}}{\Delta x^2}", font_size=38)
        d1.to_corner(UL, buff=0.45)
        rows = []
        for i in range(8):
            r = []
            for j in range(8):
                r.append("2" if i == j else ("-1" if abs(i - j) == 1 else "0"))
            rows.append(r)
        M = Matrix(rows, element_to_mobject_config={"font_size": 30}, h_buff=0.62, v_buff=0.5)
        for i, row in enumerate(M.get_rows()):
            for j, e in enumerate(row):
                if i != j and abs(i - j) != 1:
                    e.set_color(GREY_D)
                elif i == j:
                    e.set_color(C.ENERGY)
        pre = MathTex(r"\hat H", r"=", r"\frac{\hbar^2}{2m\,\Delta x^2}", font_size=38)
        pre[0].set_color(C.ENERGY)
        grp = VGroup(pre, M).arrange(RIGHT, buff=0.2).scale(0.8).next_to(d1, DOWN, buff=0.35).to_edge(LEFT, buff=0.5)
        head = label(r"The Hamiltonian as a matrix", font_size=36, color=GREY_A).to_edge(UP, buff=0.45).to_edge(RIGHT, buff=0.6)
        with self.voiceover(
            "If states are vectors, then the Hamiltonian, which acts on states, must be a matrix. Let's build it. "
            "<bookmark mark='d'/> On a grid, the second derivative at one point is the neighbors minus twice the point "
            "itself, over the spacing squared. <bookmark mark='m'/> So minus h-bar squared over two m times the second "
            "derivative is this matrix: twos on the diagonal, minus ones beside it, zeros everywhere else."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("d")
            self.play(Write(d1))
            vo.wait_until("m")
            self.play(FadeIn(pre), FadeIn(M.get_brackets()), LaggedStart(*[FadeIn(e) for e in M.get_entries()], lag_ratio=0.01),
                      run_time=2)
        # its eigenvectors
        vecs = fd["vecs8"]
        bx = Axes(x_range=[0, 9, 1], y_range=[-0.6, 0.6, 0.3], x_length=4.6, y_length=1.25, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False})
        eig = VGroup()
        xx = np.linspace(0, 9, 200)
        for n in range(3):
            a = bx.copy()
            v = vecs[:, n] * np.sign(vecs[0, n])
            bars = VGroup(*[Line(a.c2p(j + 1, 0), a.c2p(j + 1, v[j]), color=WHITE, stroke_width=6) for j in range(8)])
            s_ = np.sin((n + 1) * np.pi * xx / 9) * np.abs(v).max()
            curve = polyline(a, xx, s_, color=C.ENERGY, stroke_width=2).set_stroke(opacity=0.7)
            lab = MathTex(rf"n = {n + 1}", font_size=26, color=C.ENERGY).next_to(a, LEFT, buff=0.15)
            eig.add(VGroup(a, curve, bars, lab))
        eig.arrange(DOWN, buff=0.3).to_edge(RIGHT, buff=0.5).shift(UP * 0.55)  # below the header
        el = label(r"eigenvectors of the $8 \times 8$ matrix:\\exactly the sampled sine waves", font_size=24, color=GREY_A)
        el.next_to(eig, DOWN, buff=0.15)
        r8, r64, r1k = (fd[f"E{N}"][:5] / fd[f"E{N}"][0] for N in (8, 64, 1024))
        tab = num_table([r"N", r"E_2/E_1", r"E_3/E_1", r"E_4/E_1", r"E_5/E_1"],
                        [[str(N)] + [num(v, 2) for v in r[1:5]] for N, r in ((8, r8), (64, r64), (1024, r1k))]
                        + [[r"\text{exact}", "4", "9", "16", "25"]], font_size=28,
                        col_colors=[WHITE, C.ENERGY, C.ENERGY, C.ENERGY, C.ENERGY]).scale(0.9)
        tab.to_corner(DL, buff=0.45)
        assert abs(r1k[1] - 4) < 1e-3 and abs(r1k[4] - 25) < 0.01 and abs(r8[1] - 3.88) < 0.01
        with self.voiceover(
            "Hand this matrix to any linear-algebra routine. <bookmark mark='e'/> Its eigenvectors come out as exactly "
            "the sampled sine waves of the box, <bookmark mark='t'/> and as the grid gets finer, its eigenvalues "
            "approach one, four, nine, sixteen, twenty-five times the lowest. The energy levels of a quantum system "
            "are the eigenvalues of a matrix. That's the sense in which Heisenberg's matrix mechanics and "
            "Schrödinger's wave mechanics, invented separately in 1925 and 1926, are the same theory."
        ) as vo:
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(e) for e in eig], lag_ratio=0.3), FadeIn(el), run_time=2)
            vo.wait_until("t")
            self.play(FadeIn(tab.header), Create(tab.rule))
            self.play(LaggedStart(*[FadeIn(r) for r in tab.rows], lag_ratio=0.4), run_time=2.2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hermitian(self):
        h = MathTex(r"\hat H^\dagger = \hat H", font_size=44, color=C.ENERGY).to_edge(UP, buff=0.4)
        hl = label(r"Hermitian: equal to its own conjugate transpose, \ $\braket{f}{\hat Hg} = \braket{\hat Hf}{g}$",
                   font_size=28, color=GREY_A).next_to(h, DOWN, buff=0.2)
        a1 = MathTex(r"E\braket{\varphi}{\varphi}", r"=", r"\braket{\varphi}{\hat H\varphi}", r"=", r"\braket{\hat H\varphi}{\varphi}",
                     r"=", r"E^*\braket{\varphi}{\varphi}", font_size=36)
        a2 = MathTex(r"\Rightarrow\;E = E^*", font_size=36, color=C.ENERGY)
        b1 = MathTex(r"E_n\braket{\varphi_m}{\varphi_n}", r"=", r"\braket{\varphi_m}{\hat H\varphi_n}", r"=",
                     r"\braket{\hat H\varphi_m}{\varphi_n}", r"=", r"E_m\braket{\varphi_m}{\varphi_n}", font_size=36)
        b2 = MathTex(r"\Rightarrow\;(E_n - E_m)\braket{\varphi_m}{\varphi_n} = 0", font_size=36, color=C.ENERGY)
        ta = label(r"real eigenvalues", font_size=30).next_to(a1, UP, buff=0.2)
        g1 = VGroup(ta, a1, a2.next_to(a1, DOWN, buff=0.2))
        tb = label(r"perpendicular eigenvectors", font_size=30)
        g2 = VGroup(tb, b1, b2)
        b2.next_to(b1, DOWN, buff=0.2)
        tb.next_to(b1, UP, buff=0.2)
        VGroup(g1, g2).arrange(DOWN, buff=0.55).next_to(hl, DOWN, buff=0.5)
        st = MathTex(r"\hat H", r"=", r"\sum_n E_n\,\ket{\varphi_n}\bra{\varphi_n}", font_size=44).to_edge(DOWN, buff=0.45)
        st[0].set_color(C.ENERGY)
        stb = boxed(st, color=C.ENERGY, buff=0.18)
        stl = label(r"the spectral theorem", font_size=26, color=C.ENERGY).next_to(stb, LEFT, buff=0.3)
        with self.voiceover(
            "Our matrix is symmetric, and for complex matrices the right notion is Hermitian: equal to its own "
            "conjugate transpose, which means H can be moved from one side of an inner product to the other. "
            "Two short consequences. <bookmark mark='a'/> First: if phi is an eigenvector with eigenvalue E, move H "
            "across the inner product and you find E equals its own complex conjugate. Energies are real numbers, as "
            "measured quantities should be. <bookmark mark='b'/> Second: for two eigenvectors with different "
            "eigenvalues, the same move shows that their inner product must be zero. They're perpendicular."
        ) as vo:
            self.play(Write(h), FadeIn(hl))
            vo.wait_until("a")
            self.play(FadeIn(ta), Write(a1), run_time=2)
            self.play(Write(a2))
            vo.wait_until("b")
            self.play(FadeIn(tb), Write(b1), run_time=2)
            self.play(Write(b2))
        with self.voiceover(
            "Together these give the spectral theorem: a Hermitian operator is completely described by its "
            "eigenvalues and its perpendicular eigenvectors. Here, H is a sum of energies times projections onto the "
            "stationary states."
        ):
            self.play(Write(st), Create(stb[0]), FadeIn(stl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def evolution(self):
        c = load("carpet")
        x, mv, tm, cs = c["x"], c["early"], c["t_early"], c["cs"]
        u1 = MathTex(r"\hat U(t)", r"=", r"e^{-i\hat Ht/\hbar}", r"=", r"\sum_n e^{-iE_nt/\hbar}\,\ket{\varphi_n}\bra{\varphi_n}",
                     font_size=38).to_edge(UP, buff=0.4)
        u2 = MathTex(r"c_n(t)", r"=", r"c_n\,e^{-iE_nt/\hbar}", r",\qquad", r"\sum_n |c_n(t)|^2 = 1", font_size=36)
        u2[4].set_color(C.BORN)
        u2.next_to(u1, DOWN, buff=0.3)
        un = label(r"unitary: every length is preserved, so evolution is a rotation of the state vector", font_size=26,
                   color=GREY_A).next_to(u2, DOWN, buff=0.15)
        t = ValueTracker(0.0)
        ax = wave_axes((-0.02, 1.02), (0, 7.5), x_length=6.0, y_length=2.4).move_to(RIGHT * 3.2 + DOWN * 1.9)
        wv = WaveView(ax, x, mv[0], mode="density", x_window=(0, 1)).follow(t, frames_at(tm, mv))
        cen = [np.array([-6.0 + 1.05 * (i % 4), -1.0 - 1.15 * (i // 4), 0]) for i in range(8)]
        top = np.abs(cs[:8]).max()
        rings = VGroup(*[Circle(radius=0.45, color=GREY_D, stroke_width=1.2).move_to(cc) for cc in cen])
        clocks = always_redraw(lambda: VGroup(*[phasor(cs[i] * np.exp(-1j * box_E(i + 1) * t.get_value()), origin=cen[i],
                                                        unit=0.43 / top, stroke_width=4, tip=0.1) for i in range(8)]))
        cl = VGroup(*[MathTex(f"c_{i + 1}", font_size=22, color=GREY_B).next_to(rings[i], DOWN, buff=0.04) for i in range(8)])
        arrow = Arrow(LEFT * 1.6 + DOWN * 1.9, LEFT * 0.0 + DOWN * 1.9, buff=0.1, color=GREY_B)
        al = MathTex(r"\sum_n", font_size=30).next_to(arrow, UP, buff=0.05)
        wheel = corner_wheel(corner=DR, buff=0.15, radius=0.24, labels=False, title=False)
        with self.voiceover(
            "And time evolution has the cleanest possible form in this basis. <bookmark mark='u'/> The evolution "
            "operator, e to the minus i H t over h-bar, just multiplies each coefficient by its own phase. "
            "<bookmark mark='c'/> Each coefficient is a clock running at its own rate, and since phases don't change "
            "lengths, the sum of the squares stays one forever. The state vector rotates in Hilbert space. "
            "<bookmark mark='w'/> Everything we saw in the box, the sloshing and the carpet, is this: a set of clocks, "
            "summed."
        ) as vo:
            self.play(Write(u1))
            vo.wait_until("u")
            self.play(Write(u2), FadeIn(un))
            vo.wait_until("c")
            self.play(FadeIn(rings), FadeIn(clocks), FadeIn(cl), Create(ax), FadeIn(wv), GrowArrow(arrow), FadeIn(al),
                      FadeIn(wheel))
            vo.wait_until("w")
            self.play(t.animate.set_value(0.03), run_time=vo.remaining() + 1.5, rate_func=linear)
        for m in (clocks, wv):
            m.clear_updaters()
        self.clear_scene()
