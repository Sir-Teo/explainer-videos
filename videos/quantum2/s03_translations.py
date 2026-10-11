from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum2.common import (WaveView, boxed, corner_wheel, label, ladder, load, mtex, note, plain_axes, polyline,
                                    wave_axes, why)


def packet(x, x0=0.0, s=1.0, k=0.0):
    return (2 * np.pi * s * s) ** -0.25 * np.exp(-((x - x0) ** 2) / (4 * s * s) + 1j * k * x)


class Translations(VoiceoverScene):
    def construct(self):
        self.generator()
        self.commutator()
        self.p_formula()
        self.trace()
        self.boost()
        self.hamiltonian()
        self.weyl()

    # ------------------------------------------------------------------
    def generator(self):
        x = np.linspace(-8, 8, 1600)
        a = ValueTracker(0.0)
        ax = wave_axes((-8, 8), (0, 0.5), x_length=11.0, y_length=2.4).move_to(DOWN * 1.9)
        wv = WaveView(ax, x, packet(x, -2.5, 0.9, 2.0), mode="density").follow(a, lambda v: packet(x, -2.5 + v, 0.9, 2.0))
        xl = MathTex("x", font_size=30, color=C.XPOS).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        ghost = DashedLine(ax.c2p(-2.5, 0), ax.c2p(-2.5, 0.48), color=GREY_C)
        al = always_redraw(lambda: MathTex(f"a = {a.get_value():.1f}", font_size=30, color=C.XPOS).next_to(ax, UP, buff=0.05).to_edge(RIGHT, buff=0.8))
        t1 = MathTex(r"(\hat T(a)\psi)(x)", r"=", r"\psi(x - a)", font_size=40).to_edge(UP, buff=0.5)
        t2 = MathTex(r"\hat T(a)\hat T(b) = \hat T(a + b)", r",\qquad", r"\text{unitary}", font_size=34).next_to(t1, DOWN, buff=0.3)
        t3 = MathTex(r"\hat T(a)", r"=", r"e^{-ia\hat P/\hbar}", font_size=44).next_to(t2, DOWN, buff=0.35)
        t3[2].set_color(C.MOMENTUM)
        dfn = label(r"momentum \emph{is} the generator of translations", font_size=30, color=C.MOMENTUM).next_to(t3, DOWN, buff=0.25)
        cons = MathTex(r"[\hat H, \hat T(a)] = 0", r"\;\Rightarrow\;", r"\hat P \text{ conserved}", font_size=30).next_to(dfn, DOWN, buff=0.2)
        cons[2].set_color(C.MOMENTUM)
        wheel = corner_wheel(corner=DR, buff=0.2, radius=0.26)
        with self.voiceover(
            "Space works the same way. <bookmark mark='t'/> Let T of a be the operator that slides every wavefunction a "
            "distance a to the right: psi of x becomes psi of x minus a. <bookmark mark='g'/> Sliding twice adds the "
            "distances, and nothing about probabilities changes, so T is a one-parameter unitary group, and by Stone's "
            "theorem it has a generator. <bookmark mark='p'/> Call it P: T of a equals e to the minus i a P over h-bar. "
            "<bookmark mark='d'/> This is the definition of momentum: the generator of translations. "
            "<bookmark mark='c'/> If the Hamiltonian doesn't care where things are, H commutes with T, and momentum is "
            "conserved."
        ) as vo:
            self.play(Create(ax), FadeIn(wv), FadeIn(xl), FadeIn(wheel))
            vo.wait_until("t")
            self.add(ghost, al)
            self.play(Write(t1), a.animate.set_value(3.0), run_time=2.5)
            vo.wait_until("g")
            self.play(FadeIn(t2), a.animate.set_value(5.0), run_time=1.5)
            vo.wait_until("p")
            self.play(Write(t3))
            vo.wait_until("d")
            self.play(FadeIn(dfn))
            vo.wait_until("c")
            self.play(FadeIn(cons))
        al.clear_updaters()
        wv.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def commutator(self):
        rows = [
            MathTex(r"\hat T(a)\ket{x}", r"=", r"\ket{x + a}", font_size=38),
            MathTex(r"\hat X\,\hat T(a)\ket{x}", r"=", r"(x + a)\,\hat T(a)\ket{x}", font_size=38),
            MathTex(r"[\hat X, \hat T(a)]", r"=", r"a\,\hat T(a)", font_size=38),
            MathTex(r"\big[\hat X, \,1 - \tfrac{ia}{\hbar}\hat P + \dots\big]", r"=", r"a\,(1 + \dots)", font_size=38),
            MathTex(r"-\tfrac{ia}{\hbar}\,[\hat X, \hat P]", r"=", r"a", font_size=38),
            MathTex(r"[\hat X, \hat P]", r"=", r"i\hbar", font_size=50),
        ]
        rows[5].set_color(C.HBAR)
        whys = [
            why(rows[0], r"a slid position eigenstate"),
            why(rows[1], r"measure position after the slide"),
            why(rows[2], r"subtract $\hat T(a)\hat X\ket{x} = x\,\hat T(a)\ket{x}$; true for every $x$"),
            why(rows[3], r"slide by a tiny $a$"),
            why(rows[4], r"the identity commutes with everything"),
            why(rows[5], r"divide by $a$"),
        ]
        # a picture: the spike at x, slid to x + a
        nl = NumberLine(x_range=[-1, 5, 1], length=5.0, include_ticks=False, color=GREY_B).to_corner(DL, buff=0.7)
        sp0 = Arrow(nl.n2p(1), nl.n2p(1) + UP * 1.1, buff=0, color=C.XPOS, stroke_width=5, tip_length=0.15)
        sp1 = Arrow(nl.n2p(3.2), nl.n2p(3.2) + UP * 1.1, buff=0, color=C.XPOS, stroke_width=5, tip_length=0.15)
        l0 = MathTex(r"\ket{x}", font_size=28, color=C.XPOS).next_to(sp0, UP, buff=0.08)
        l1 = MathTex(r"\ket{x + a}", font_size=28, color=C.XPOS).next_to(sp1, RIGHT, buff=0.1).shift(UP * 0.3)
        slide = CurvedArrow(sp0.get_top() + UP * 0.05 + RIGHT * 0.1, sp1.get_top() + UP * 0.05 + LEFT * 0.1, angle=-PI / 3,
                            color=C.MOMENTUM, stroke_width=3)
        sl = MathTex(r"\hat T(a)", font_size=26, color=C.MOMENTUM).next_to(slide, UP, buff=0.15)
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-0.6)
        with self.voiceover(
            "Now we can derive the commutator, instead of computing it from a guess. <bookmark mark='a'/> A position "
            "eigenstate, slid by a, is the position eigenstate at x plus a. <bookmark mark='b'/> So measuring position "
            "after the slide gives x plus a, and before it gives x: <bookmark mark='c'/> X and T fail to commute, by "
            "exactly a times T. That's true for every x, so it's an operator equation."
        ) as vo:
            self.play(Create(nl), GrowArrow(sp0), FadeIn(l0))
            vo.wait_until("a")
            step(0)
            self.play(Create(slide), FadeIn(sl), GrowArrow(sp1), FadeIn(l1))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        with self.voiceover(
            "<bookmark mark='d'/> Expand T for a small slide: one minus i a P over h-bar. <bookmark mark='e'/> The "
            "identity commutes with everything, and what's left is minus i a over h-bar times X P minus P X, equal to a. "
            "<bookmark mark='f'/> Divide by a: X P minus P X equals i h-bar. <bookmark mark='g'/> The canonical "
            "commutation relation is just the statement that momentum moves position."
        ) as vo:
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
            vo.wait_until("f")
            step(5)
            box = SurroundingRectangle(rows[5], color=C.HBAR, buff=0.2, corner_radius=0.12)
            self.play(Create(box))
            vo.wait_until("g")
            msg = label(r"momentum moves position", font_size=30, color=C.HBAR).next_to(box, DOWN, buff=0.35)
            self.play(FadeIn(msg))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def p_formula(self):
        l1 = MathTex(r"\braket{x}{\hat T(a)\psi}", r"=", r"\psi(x - a)", r"=", r"\psi(x) - a\,\psi'(x) + \dots", font_size=38)
        l2 = MathTex(r"\braket{x}{\hat T(a)\psi}", r"=", r"\braket{x}{\big(1 - \tfrac{ia}{\hbar}\hat P\big)\psi}", r"=",
                     r"\psi(x) - \tfrac{ia}{\hbar}\braket{x}{\hat P\psi} + \dots", font_size=38)
        l3 = MathTex(r"\braket{x}{\hat P\psi}", r"=", r"-i\hbar\,\frac{d\psi}{dx}", font_size=48)
        l3[2].set_color(C.MOMENTUM)
        g = VGroup(l1, l2, l3).arrange(DOWN, buff=0.6).move_to(UP * 0.4)
        w1 = why(l1, r"Taylor", direction=DOWN, buff=0.1).align_to(l1, RIGHT)
        w2 = why(l2, r"the generator", direction=DOWN, buff=0.1).align_to(l2, RIGHT)
        box = SurroundingRectangle(l3, color=C.MOMENTUM, buff=0.2, corner_radius=0.12)
        msg = label(r"Part 1 guessed this; here it is forced", font_size=30, color=GREY_A).next_to(box, DOWN, buff=0.4)
        with self.voiceover(
            "And the formula for momentum follows. <bookmark mark='a'/> In the position basis, the slid wavefunction is "
            "psi of x minus a. Expand both sides to first order in a: <bookmark mark='b'/> Taylor's theorem on one side, "
            "the generator on the other. <bookmark mark='c'/> Matching them, P acting on psi is minus i h-bar times the "
            "derivative. Part 1 guessed this; here it's forced."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(l1), FadeIn(w1))
            vo.wait_until("b")
            self.play(Write(l2), FadeIn(w2))
            vo.wait_until("c")
            self.play(Write(l3), Create(box))
            self.play(FadeIn(msg))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def trace(self):
        d = load("symmetry")["trace_diag"]
        tr1 = MathTex(r"\operatorname{tr}(\hat X\hat P - \hat P\hat X)", r"=", r"\operatorname{tr}\hat X\hat P - \operatorname{tr}\hat P\hat X", r"=", r"0",
                      font_size=38).to_edge(UP, buff=0.5)
        tr2 = MathTex(r"\operatorname{tr}(i\hbar\,I_N)", r"=", r"i\hbar\,N", r"\neq", r"0", font_size=38).next_to(tr1, DOWN, buff=0.35)
        tr2[2].set_color(C.HBAR)
        # the diagonal of a random 5x5 commutator
        cells = VGroup()
        n = len(d)
        for i in range(n):
            for j in range(n):
                sq = Square(side_length=0.62, stroke_color=GREY_D, stroke_width=1.2)
                sq.move_to(np.array([(j - 2) * 0.66, -(i - 2) * 0.66, 0]))
                if i == j:
                    sq.set_fill(C.HBAR, opacity=0.18)
                    t = MathTex(f"{d[i].imag:+.1f}i".replace("+", "{+}").replace("-", "{-}"), font_size=18, color=C.HBAR).move_to(sq)
                    cells.add(VGroup(sq, t))
                else:
                    cells.add(VGroup(sq, Dot(sq.get_center(), radius=0.03, color=GREY_C)))
        cells.move_to(LEFT * 3.3 + DOWN * 1.3)
        mlab = label(r"$[X, P]$ for random $5\times 5$ Hermitian $X$, $P$", font_size=24, color=GREY_B).next_to(cells, UP, buff=0.15)
        s = float(np.sum(d.imag))
        assert abs(s) < 1e-12
        summ = MathTex(r"\text{diagonal sum} = 0", font_size=28, color=C.HBAR).next_to(cells, DOWN, buff=0.2)
        concl = VGroup(
            label(r"$\Rightarrow$ no finite matrices obey $[\hat X, \hat P] = i\hbar$", font_size=28),
            label(r"a particle's Hilbert space is infinite-dimensional", font_size=28, color=C.HBAR),
            label(r"Stone--von Neumann (1931): every solution is $x$ and $-i\hbar\,d/dx$ in disguise", font_size=26),
            label(r"so matrix mechanics and wave mechanics \emph{had} to agree", font_size=26, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        if concl.width > 8.2:
            concl.width = 8.2
        concl.move_to(RIGHT * 2.55 + DOWN * 1.35)
        with self.voiceover(
            "One consequence is startling. No finite matrices can satisfy X P minus P X equals i h-bar. "
            "<bookmark mark='a'/> The trace of any commutator is zero, because the trace of X P equals the trace of P X. "
            "<bookmark mark='m'/> Here's a random five-by-five example, whose diagonal entries cancel exactly. "
            "<bookmark mark='b'/> But the trace of i h-bar times the identity is i h-bar times the dimension. "
            "<bookmark mark='c'/> So the Hilbert space of a particle on a line has to be infinite-dimensional, and, "
            "<bookmark mark='d'/> as Stone and von Neumann proved, any operators satisfying the relation are just x and "
            "minus i h-bar d d x in disguise. That's why Heisenberg's matrices and Schrödinger's waves had to agree."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(tr1))
            vo.wait_until("m")
            self.play(FadeIn(cells), FadeIn(mlab))
            self.play(FadeIn(summ))
            vo.wait_until("b")
            self.play(Write(tr2))
            vo.wait_until("c")
            self.play(FadeIn(concl[0]), FadeIn(concl[1]))
            vo.wait_until("d")
            self.play(FadeIn(concl[2]), FadeIn(concl[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def boost(self):
        x = np.linspace(-8, 8, 1600)
        v = ValueTracker(0.0)
        s0, k0 = 1.0, 0.8
        ax = wave_axes((-8, 8), (0, 0.45), x_length=11.0, y_length=2.0).move_to(UP * 1.1)
        wv = WaveView(ax, x, packet(x, 0, s0, k0), mode="density").follow(v, lambda vv: packet(x, 0, s0, k0 + vv))
        xl = MathTex("x", font_size=30, color=C.XPOS).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        yl = MathTex(r"|\psi|^2", font_size=28, color=C.BORN).next_to(ax.c2p(-8, 0.45), RIGHT, buff=0.1)
        pax = plain_axes((-1, 6), (0, 0.85), 11.0, 1.7).move_to(DOWN * 2.2)
        ks = np.linspace(-1, 6, 600)

        def phi(vv):
            return np.sqrt(2 * s0**2 / np.pi) * np.exp(-2 * s0**2 * (ks - k0 - vv) ** 2)

        pc = always_redraw(lambda: polyline(pax, ks, phi(v.get_value()), color=C.MOMENTUM, stroke_width=3.5))
        p0 = DashedLine(pax.c2p(k0, 0), pax.c2p(k0, 0.85), color=GREY_C)
        pl = MathTex("p", font_size=30, color=C.MOMENTUM).next_to(pax.x_axis.get_end(), RIGHT, buff=0.1)
        phl = MathTex(r"|\phi(p)|^2", font_size=28, color=C.MOMENTUM).next_to(pax.c2p(-1, 0.85), RIGHT, buff=0.1)
        br = always_redraw(lambda: BraceBetweenPoints(pax.c2p(k0, 0.86), pax.c2p(k0 + v.get_value() + 1e-3, 0.86), direction=UP, color=C.MOMENTUM)
                           if v.get_value() > 0.05 else VMobject())
        bl = always_redraw(lambda: MathTex(f"mv = {v.get_value():.1f}", font_size=26, color=C.MOMENTUM).move_to(
            pax.c2p(k0 + v.get_value() / 2, 1.3)) if v.get_value() > 0.05 else VMobject())
        eq = MathTex(r"\psi(x)", r"\;\longrightarrow\;", r"e^{\,imvx/\hbar}", r"\,\psi(x)", font_size=40).to_edge(UP, buff=0.25)
        eq[2].set_color(C.HBAR)
        units = note(r"$\hbar = m = 1$").to_corner(DR, buff=0.25)
        wheel = corner_wheel(corner=UR, buff=0.2, radius=0.26)
        with self.voiceover(
            "Boosts, changing to a frame moving at velocity v, give the rest. <bookmark mark='a'/> Seen from the moving "
            "frame, every momentum shifts by m v, and on a wavefunction that's multiplication by e to the i m v x over "
            "h-bar: <bookmark mark='b'/> a twist of the phase that winds the colors faster, while the density doesn't "
            "change at all. <bookmark mark='c'/> Watch the momentum distribution slide over by exactly m v."
        ) as vo:
            self.play(Create(ax), FadeIn(wv), FadeIn(xl), FadeIn(yl), Create(pax), FadeIn(pc), FadeIn(pl), FadeIn(phl),
                      FadeIn(p0), FadeIn(units), FadeIn(wheel))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.add(br, bl)
            self.play(v.animate.set_value(3.5), run_time=3.5)
            vo.wait_until("c")
            self.play(Indicate(bl, color=C.MOMENTUM))
        for m in (wv, pc, br, bl):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def hamiltonian(self):
        rows = [
            MathTex(r"\hat B(v)^\dagger\,\hat P\,\hat B(v)", r"=", r"\hat P + mv", font_size=38),
            MathTex(r"\frac{d\hat X}{dt} = \frac{i}{\hbar}[\hat H, \hat X]", r"=", r"\frac{\hat P}{m}", font_size=38),
            MathTex(r"[\hat H, \hat X]", r"=", r"-\frac{i\hbar}{m}\hat P", r"=", r"\Big[\frac{\hat P^2}{2m}, \hat X\Big]", font_size=38),
            MathTex(r"\Big[\hat H - \frac{\hat P^2}{2m}, \hat X\Big]", r"=", r"0", font_size=38),
            MathTex(r"\hat H", r"=", r"\frac{\hat P^2}{2m} + V(\hat X)", font_size=48),
        ]
        rows[4].set_color(C.ENERGY)
        whys = [
            why(rows[0], r"a boost shifts momentum by $mv$"),
            why(rows[1], r"velocities add: in every frame, velocity is $P/m$"),
            why(rows[2], r"use $[\hat P^2, \hat X] = -2i\hbar\hat P$"),
            why(rows[3], r"commutes with $\hat X$ $\Rightarrow$ a function of $\hat X$"),
            why(rows[4], r"the Hamiltonian, derived"),
        ]
        step = ladder(self, rows, whys, keep=5, top=3.1, x=-1.6, buff=0.45)
        with self.voiceover(
            "<bookmark mark='a'/> Now require that velocities add properly: <bookmark mark='b'/> the rate of change of "
            "X, which by the Heisenberg equation is i over h-bar times the commutator of H with X, must be P over m in "
            "every frame. <bookmark mark='c'/> The kinetic energy, P squared over 2m, has exactly that commutator with "
            "X. <bookmark mark='d'/> So H minus P squared over 2m commutes with X, and anything that commutes with "
            "position is a function of position. <bookmark mark='e'/> H equals P squared over 2m plus V of X. The form "
            "of the Hamiltonian, derived from Galilean relativity."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
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
    def weyl(self):
        ax = plain_axes((0, 4.2), (0, 3.2), 5.6, 4.3).move_to(LEFT * 3.4 + DOWN * 0.3)
        xl = MathTex("x", font_size=32, color=C.XPOS).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        pl = MathTex("p", font_size=32, color=C.MOMENTUM).next_to(ax.y_axis.get_end(), UP, buff=0.1)
        x0, p0, a, mv = 0.6, 0.6, 2.6, 1.9
        rect = Polygon(ax.c2p(x0, p0), ax.c2p(x0 + a, p0), ax.c2p(x0 + a, p0 + mv), ax.c2p(x0, p0 + mv), stroke_width=0,
                       fill_color=C.HBAR, fill_opacity=0.25)
        r1 = VGroup(Arrow(ax.c2p(x0, p0), ax.c2p(x0 + a, p0), buff=0, color=C.XPOS, stroke_width=5),
                    Arrow(ax.c2p(x0 + a, p0), ax.c2p(x0 + a, p0 + mv), buff=0, color=C.MOMENTUM, stroke_width=5))
        r2 = VGroup(Arrow(ax.c2p(x0, p0), ax.c2p(x0, p0 + mv), buff=0, color=C.MOMENTUM, stroke_width=5),
                    Arrow(ax.c2p(x0, p0 + mv), ax.c2p(x0 + a, p0 + mv), buff=0, color=C.XPOS, stroke_width=5))
        la = MathTex("a", font_size=30, color=C.XPOS).next_to(r1[0], DOWN, buff=0.1)
        lm = MathTex("mv", font_size=30, color=C.MOMENTUM).next_to(r2[0], LEFT, buff=0.1)
        area = MathTex(r"\text{area} = mva", font_size=32, color=C.HBAR).move_to(rect)
        e1 = MathTex(r"\hat B(v)\hat T(a)\psi", r"=", r"e^{\,imvx/\hbar}\,\psi(x - a)", font_size=34)
        e2 = MathTex(r"\hat T(a)\hat B(v)\psi", r"=", r"e^{\,imv(x - a)/\hbar}\,\psi(x - a)", font_size=34)
        e3 = MathTex(r"\hat T\hat B", r"=", r"e^{-i\,mva/\hbar}\;\hat B\hat T", font_size=40)
        e3[2].set_color(C.HBAR)
        col = VGroup(e1, e2, e3).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(RIGHT * 3.2 + UP * 0.9)
        motto = label(r"phase $=$ area in phase space $/\,\hbar$", font_size=34, color=C.HBAR).move_to(RIGHT * 3.2 + DOWN * 1.7)
        later = label(r"(again: magnetic flux, next; Bohr--Sommerfeld, later)", font_size=24, color=GREY_B).next_to(motto, DOWN, buff=0.2)
        with self.voiceover(
            "One last detail will come back again and again. <bookmark mark='a'/> Slide by a and then boost, "
            "<bookmark mark='b'/> or boost and then slide: <bookmark mark='c'/> the results differ only by a phase, e to "
            "the minus i m v a over h-bar. <bookmark mark='d'/> And m v a is the area of a rectangle in phase space, a "
            "wide and m v tall. <bookmark mark='e'/> Phase equals area over h-bar. We'll meet it next with magnetic "
            "flux, and later in the old quantum rules."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(pl))
            vo.wait_until("a")
            self.play(GrowArrow(r1[0]), FadeIn(la))
            self.play(GrowArrow(r1[1]), Write(e1))
            vo.wait_until("b")
            self.play(GrowArrow(r2[0]), FadeIn(lm))
            self.play(GrowArrow(r2[1]), Write(e2))
            vo.wait_until("c")
            self.play(Write(e3))
            vo.wait_until("d")
            self.play(FadeIn(rect), FadeIn(area))
            vo.wait_until("e")
            self.play(FadeIn(motto), FadeIn(later))
        self.wait(0.4)
        self.clear_scene()
