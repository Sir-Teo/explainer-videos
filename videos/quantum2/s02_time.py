from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum2.common import (BlochSphere, Projector, bloch_vector, boxed, complex_plane, corner_wheel, hue, label,
                                    ladder, line_3d, mtex, note, part_card, phasor, segments_3d, why)


class TimeSymmetry(VoiceoverScene):
    def construct(self):
        self.card()
        self.what_is_symmetry()
        self.group_law()
        self.derivation()
        self.why_i()
        self.energy()

    # ------------------------------------------------------------------
    def card(self):
        c = part_card(1, r"Symmetry", r"what stays the same decides what changes")
        with self.voiceover("Part 1: Symmetry."):
            self.play(FadeIn(c))
        self.wait(0.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def what_is_symmetry(self):
        proj = Projector(az=-0.6, el=0.35, scale=2.0, center=LEFT * 3.2 + DOWN * 0.4)
        R0 = 1.0
        phi_v = np.array([0.9, 0.25, 0.35])
        psi_v = np.array([0.25, 0.95, -0.2])
        phi_v /= np.linalg.norm(phi_v)
        psi_v /= np.linalg.norm(psi_v)

        def scene3d():
            g = VGroup()
            for v, lab in ((np.eye(3)[0], r"e_1"), (np.eye(3)[1], r"e_2"), (np.eye(3)[2], r"e_3")):
                g.add(line_3d(proj, -0.0 * v, R0 * v * 1.15, color=GREY_C, n=12, stroke_width=1.5))
                g.add(MathTex(lab, font_size=22, color=GREY_C).move_to(proj.point(v * 1.32)))
            o = proj.point(np.zeros(3))
            for v, col, lab in ((phi_v, C.XPOS, r"\ket{\varphi}"), (psi_v, C.MOMENTUM, r"\ket{\psi}")):
                tip = proj.point(v * R0)
                g.add(Arrow(o, tip, buff=0, color=col, stroke_width=5, tip_length=0.18))
                g.add(MathTex(lab, font_size=30, color=col).move_to(o + (tip - o) * 1.25))
            # the angle between them
            ts = np.linspace(0, 1, 30)
            arc = np.array([(1 - t) * phi_v + t * psi_v for t in ts])
            arc = 0.38 * arc / np.linalg.norm(arc, axis=1)[:, None]
            g.add(segments_3d(proj, arc, [C.HBAR] * 29, stroke_width=3, depth_range=1.0))
            return g

        pic = always_redraw(scene3d)
        cap = label(r"Hilbert space, drawn in three real dimensions", font_size=24, color=GREY_B).next_to(proj.point([0, -0.2, 0]), DOWN, buff=1.9)
        pred = MathTex(r"\text{every prediction: }", r"|\braket{\varphi}{\psi}|^2", font_size=34).to_edge(UP, buff=0.6).shift(RIGHT * 2.6)
        pred[1].set_color(C.BORN)
        unit = MathTex(r"\hat U^\dagger \hat U = 1", r"\;\Rightarrow\;", r"\braket{U\varphi}{U\psi} = \braket{\varphi}{\psi}", font_size=34)
        unit.next_to(pred, DOWN, buff=0.55)
        unit[0].set_color(C.HBAR)
        wig = label(r"Wigner (1931): a symmetry is \emph{unitary}, or \emph{antiunitary}\\(the second kind: only time reversal)",
                    font_size=26, color=GREY_A).next_to(unit, DOWN, buff=0.55)
        rigid = label(r"a unitary map is a rigid rotation of Hilbert space:\\lengths and angles never change", font_size=28,
                      color=C.HBAR).next_to(wig, DOWN, buff=0.55)
        examples = label(r"turn the lab, start the clock later, move everything 1 m to the left", font_size=26,
                         color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "What is a symmetry, in quantum mechanics? It's a change in how we describe things that leaves every "
            "prediction unchanged: <bookmark mark='x'/> turn your lab around, start your clock later, move everything a "
            "meter to the left. <bookmark mark='p'/> Every prediction is a probability, the squared size of an inner "
            "product, so a symmetry must preserve the size of every inner product. <bookmark mark='w'/> Eugene Wigner "
            "showed in 1931 that such a map can always be chosen to be unitary, U dagger U equals one, which preserves "
            "inner products exactly, or antiunitary, which also conjugates them; that second kind is needed only for "
            "time reversal. <bookmark mark='r'/> Geometrically, a unitary is a rigid rotation of Hilbert space: lengths "
            "and angles all stay the same."
        ) as vo:
            self.add(pic)
            self.play(FadeIn(pic), FadeIn(cap))
            vo.wait_until("x")
            self.play(FadeIn(examples))
            vo.wait_until("p")
            self.play(Write(pred))
            vo.wait_until("w")
            self.play(Write(unit))
            self.play(FadeIn(wig))
            vo.wait_until("r")
            self.play(FadeIn(rigid), proj.az.animate.set_value(1.2), proj.el.animate.set_value(0.6), run_time=max(3.0, vo.remaining()))
        pic.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def group_law(self):
        ax = NumberLine(x_range=[0, 10, 1], length=11, include_ticks=False, color=GREY_B).move_to(DOWN * 0.6)
        tl = MathTex("t", font_size=32, color=C.QTIME).next_to(ax, RIGHT, buff=0.15)
        p0, ps, pts = ax.n2p(0.6), ax.n2p(3.6), ax.n2p(9.0)
        dots_ = VGroup(*[Dot(p, color=C.QTIME) for p in (p0, ps, pts)])
        labs = VGroup(MathTex("0", font_size=28), MathTex("s", font_size=28), MathTex("s + t", font_size=28))
        for l, p in zip(labs, (p0, ps, pts)):
            l.set_color(C.QTIME).next_to(p, UP, buff=0.18)
        a1 = CurvedArrow(p0 + UP * 0.6, ps + UP * 0.6, angle=-PI / 3, color=C.QTIME)
        a2 = CurvedArrow(ps + UP * 0.6, pts + UP * 0.6, angle=-PI / 3, color=C.QTIME)
        a3 = CurvedArrow(p0 + DOWN * 0.15, pts + DOWN * 0.15, angle=PI / 4, color=WHITE)
        l1 = MathTex(r"\hat U(s)", font_size=30, color=C.QTIME).next_to(a1, UP, buff=0.1)
        l2 = MathTex(r"\hat U(t)", font_size=30, color=C.QTIME).next_to(a2, UP, buff=0.1)
        l3 = MathTex(r"\hat U(s + t)", font_size=30).next_to(a3, DOWN, buff=0.1)
        law = MathTex(r"\hat U(t + s)", r"=", r"\hat U(t)\,\hat U(s)", r",\qquad", r"\hat U(0) = 1", font_size=40).to_edge(UP, buff=0.7)
        law[0].set_color(C.QTIME)
        law[2].set_color(C.QTIME)
        same = label(r"the laws are the same at every moment", font_size=28, color=GREY_A).next_to(law, DOWN, buff=0.3)
        stone = MathTex(r"\hat U(t) = e^{-it\hat H/\hbar}", font_size=44, color=C.QTIME).to_edge(DOWN, buff=1.1)
        stone_l = label(r"Stone (1932): every continuous one-parameter unitary group has this form, for one self-adjoint $\hat H$",
                        font_size=24, color=GREY_A).next_to(stone, DOWN, buff=0.2)
        with self.voiceover(
            "Now apply this to time. <bookmark mark='u'/> Let U of t take any state at time zero to the state at time "
            "t. <bookmark mark='g'/> If the laws are the same at every moment, evolving for s and then for t is the "
            "same as evolving for s plus t: U of t plus s equals U of t times U of s, with U of zero the identity. "
            "<bookmark mark='s'/> A family like this is called a one-parameter group, and Marshall Stone proved in 1932 "
            "that every continuous one has the form e to the minus i t H over h-bar, for a unique self-adjoint "
            "operator H."
        ) as vo:
            self.play(Create(ax), FadeIn(tl), FadeIn(dots_), FadeIn(labs))
            vo.wait_until("u")
            self.play(Create(a1), FadeIn(l1))
            self.play(Create(a2), FadeIn(l2))
            vo.wait_until("g")
            self.play(Create(a3), FadeIn(l3), Write(law), FadeIn(same))
            vo.wait_until("s")
            self.play(Write(stone), FadeIn(stone_l))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derivation(self):
        rows = [
            MathTex(r"\hat U(\epsilon)", r"=", r"1 - \frac{i\epsilon}{\hbar}\hat H + O(\epsilon^2)", font_size=40),
            MathTex(r"\hat U^\dagger \hat U", r"=", r"1 + \frac{i\epsilon}{\hbar}\big(\hat H^\dagger - \hat H\big) + O(\epsilon^2)", r"\;=\;1", font_size=40),
            MathTex(r"\hat H^\dagger", r"=", r"\hat H", font_size=44),
            MathTex(r"\frac{d\hat U}{dt}", r"=", r"\lim_{\epsilon\to 0}\frac{\hat U(\epsilon) - 1}{\epsilon}\;\hat U(t)", font_size=40),
            MathTex(r"\frac{d\hat U}{dt}", r"=", r"-\frac{i}{\hbar}\,\hat H\,\hat U(t)", font_size=40),
            MathTex(r"i\hbar\,\frac{d}{dt}\ket{\psi(t)}", r"=", r"\hat H\ket{\psi(t)}", font_size=48),
        ]
        rows[2].set_color(C.ENERGY)
        rows[5][0].set_color(C.ENERGY)
        rows[5][2].set_color(C.ENERGY)
        whys = [
            why(rows[0], r"near the identity; this \emph{defines} $\hat H$"),
            why(rows[1], r"unitarity: the first-order term must vanish"),
            why(rows[2], r"so $\hat H$ is Hermitian"),
            why(rows[3], r"the group law: $\hat U(t + \epsilon) = \hat U(\epsilon)\hat U(t)$"),
            why(rows[4], r"the first line"),
            why(rows[5], r"act on $\ket{\psi(0)}$"),
        ]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-1.6)
        with self.voiceover(
            "Here's the heart of that argument. <bookmark mark='a'/> For a tiny time epsilon, U is the identity plus "
            "something small: call it minus i epsilon H over h-bar. That defines H. <bookmark mark='b'/> Now demand "
            "unitarity. Multiply out U dagger U: the first-order term is i epsilon over h-bar times H dagger minus H, "
            "and it must vanish. <bookmark mark='c'/> So H equals its own adjoint: it's Hermitian."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        with self.voiceover(
            "<bookmark mark='d'/> Now differentiate the group law: the change in U over a short time is U of epsilon "
            "minus one, over epsilon, times U of t. <bookmark mark='e'/> By the first line, that's minus i over h-bar, "
            "H, U. <bookmark mark='f'/> Act on any state, and you get i h-bar times the time derivative of psi equals H "
            "psi. <bookmark mark='g'/> The Schrödinger equation, with no waves anywhere: only the assumption that the "
            "laws don't change with time, and that probabilities are conserved."
        ) as vo:
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
            vo.wait_until("f")
            step(5)
            box = SurroundingRectangle(rows[5], color=C.ENERGY, buff=0.2, corner_radius=0.12)
            vo.wait_until("g")
            self.play(Create(box))
            src = label(r"from: \textbf{time-translation symmetry} + \textbf{conserved probability}", font_size=28,
                        color=C.QTIME).next_to(box, DOWN, buff=0.4)
            self.play(FadeIn(src))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why_i(self):
        # left: rotating a vector in the plane; its velocity is J v, perpendicular, and J^2 = -1
        o = LEFT * 4.2 + DOWN * 0.4
        th = ValueTracker(0.5)
        circ = Circle(radius=1.6, color=GREY_D, stroke_width=1.5).move_to(o)

        def vecs():
            a = th.get_value()
            v = 1.6 * np.array([math.cos(a), math.sin(a), 0])
            jv = 0.9 * np.array([-math.sin(a), math.cos(a), 0])
            g = VGroup(Arrow(o, o + v, buff=0, color=C.XPOS, stroke_width=5, tip_length=0.2),
                       Arrow(o + v, o + v + jv, buff=0, color=C.HBAR, stroke_width=4, tip_length=0.16))
            g.add(MathTex(r"\vec v", font_size=30, color=C.XPOS).move_to(o + v * 0.55 + np.array([-v[1], v[0], 0]) * 0.18))
            g.add(MathTex(r"J\vec v", font_size=28, color=C.HBAR).move_to(o + v + jv * 1.35))
            return g

        vg = always_redraw(vecs)
        J = MathTex(r"J = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}", r",\quad", r"J^2 = -1", font_size=34).next_to(circ, UP, buff=0.35)
        J[2].set_color(C.HBAR)
        Rr = MathTex(r"R(\theta) = e^{\theta J}", font_size=34).next_to(circ, DOWN, buff=0.35)
        # right: e^{-i theta} built from its power series
        theta = 2.3
        pc = complex_plane(radius=2.2, font_size=22).move_to(RIGHT * 3.4 + DOWN * 0.3)
        O = pc[0][0].get_center()
        unit = 1.35
        uc = Circle(radius=unit, color=GREY_C, stroke_width=1.5).move_to(O)
        terms = [(-1j * theta) ** k / math.factorial(k) for k in range(12)]
        arrs, pos = VGroup(), complex(0)
        for z in terms:
            a = O + unit * np.array([pos.real, pos.imag, 0])
            arrs.add(phasor(z, origin=a, unit=unit, stroke_width=4, tip=0.12))
            pos += z
        target = Dot(O + unit * np.array([math.cos(-theta), math.sin(-theta), 0]), radius=0.08, color=WHITE)
        series = MathTex(r"e^{-i\theta}", r"=", r"1 - i\theta - \frac{\theta^2}{2!} + \frac{i\theta^3}{3!} + \frac{\theta^4}{4!} - \cdots",
                         font_size=32).next_to(pc, UP, buff=0.25)
        tl = MathTex(r"\theta = 2.3", font_size=26, color=GREY_B).next_to(pc, DOWN, buff=0.1)
        wheel = corner_wheel(corner=DR, buff=0.2, radius=0.28)
        anti = MathTex(r"\hat U \approx 1 + \epsilon \hat A,\quad \hat A^\dagger = -\hat A", r"\;\Longrightarrow\;",
                       r"\hat A = -\tfrac{i}{\hbar}\hat H,\ \ \hat H^\dagger = \hat H", font_size=32).to_edge(UP, buff=0.3)
        anti[2].set_color(C.ENERGY)
        with self.voiceover(
            "And the i is no longer mysterious. <bookmark mark='a'/> A unitary operator close to the identity is the "
            "identity plus a small anti-Hermitian operator; writing it as minus i times a Hermitian one is bookkeeping "
            "that makes H's eigenvalues real. <bookmark mark='p'/> You've seen the same thing in the plane: rotating a "
            "vector, its velocity is always perpendicular to it, and the matrix J that turns a vector a quarter turn "
            "squares to minus one. <bookmark mark='s'/> Exponentiate a generator like that, term by term, and the "
            "partial sums spiral onto the circle. Rotations come from an i."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(anti))
            vo.wait_until("p")
            self.add(vg)
            self.play(Create(circ), FadeIn(vg), Write(J))
            self.play(th.animate.set_value(2.2), FadeIn(Rr), run_time=2.0)
            vo.wait_until("s")
            self.play(FadeIn(pc), Create(uc), Write(series), FadeIn(tl), FadeIn(wheel))
            for a in arrs:
                self.play(GrowArrow(a), run_time=0.45)
            self.play(FadeIn(target), Flash(target, color=WHITE))
        vg.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def energy(self):
        gen = MathTex(r"[\hat H, \hat U(t)] = 0", r"\;\Rightarrow\;", r"\langle \hat H\rangle \text{ is conserved}", font_size=36)
        gen.to_edge(UP, buff=0.5).shift(LEFT * 2.6)
        gen[2].set_color(C.ENERGY)
        what = label(r"energy \emph{is} the generator of time translations", font_size=30, color=C.ENERGY).next_to(gen, DOWN, buff=0.3)
        hb = label(r"$\hbar$ converts a rate of turning (rad/s) into joules; its value comes from experiment", font_size=24,
                   color=GREY_B).next_to(what, DOWN, buff=0.3)
        eig = MathTex(r"\hat H\ket{E} = E\ket{E}", r"\;\Rightarrow\;", r"\hat U(t)\ket{E} = e^{-iEt/\hbar}\ket{E}", font_size=34)
        eig.next_to(hb, DOWN, buff=0.45)
        eig[2].set_color(C.QTIME)
        # a clock for the eigenstate
        o = LEFT * 4.6 + DOWN * 2.2
        tt = ValueTracker(0.0)
        dial = Circle(radius=0.75, color=GREY_D, stroke_width=1.5).move_to(o)
        hand = always_redraw(lambda: phasor(np.exp(-1j * tt.get_value()), origin=o, unit=0.75, stroke_width=5))
        cl = MathTex(r"e^{-iEt/\hbar}", font_size=28, color=C.QTIME).next_to(dial, RIGHT, buff=0.2)
        # a spin in a field: U(t) rotates the whole Bloch sphere about the field axis
        proj = Projector(az=-0.5, el=0.3, scale=1.0, center=RIGHT * 4.2 + DOWN * 1.2)
        bs = BlochSphere(proj, radius=1.45, labels=True, font_size=24)
        n = np.array([math.sin(0.5), 0, math.cos(0.5)])
        v0 = bloch_vector(1.25, 0.3)

        def rotated(v, a):
            return v * math.cos(a) + np.cross(n, v) * math.sin(a) + n * (n @ v) * (1 - math.cos(a))

        trail = always_redraw(lambda: segments_3d(proj, BlochSphere.world(np.array([rotated(v0, a) for a in np.linspace(0, tt.get_value(), 80)]) * 1.45),
                                                  [C.BLOCH] * 79, stroke_width=2.5, depth_range=1.45))
        arr = always_redraw(lambda: bs.arrow(rotated(v0, tt.get_value()), stroke_width=5))
        axis = bs.arrow(n * 1.15, color=C.ENERGY, stroke_width=3)
        ax_l = MathTex(r"\vec B", font_size=26, color=C.ENERGY).move_to(bs.bloch_to_screen(n * 1.35)[0])
        sl = label(r"a spin: $\hat U(t)$ turns the Bloch sphere\\rigidly about the field", font_size=24, color=GREY_A).next_to(bs, DOWN, buff=0.15)
        wheel = corner_wheel(corner=UR, buff=0.2, radius=0.26)
        with self.voiceover(
            "What is H? <bookmark mark='a'/> It's the generator of time translations, and it commutes with U, so its "
            "average never changes. <bookmark mark='e'/> That's what energy is, in quantum mechanics and in classical "
            "mechanics alike. <bookmark mark='h'/> The constant h-bar just converts the rate at which phases turn into "
            "units of energy, and its value comes from experiment. <bookmark mark='c'/> For an energy eigenstate the "
            "evolution is a single turning phase, e to the minus i E t over h-bar: Part 1's clocks. "
            "<bookmark mark='s'/> And for a spin in a magnetic field, U of t is a rigid rotation of the whole Bloch "
            "sphere about the field."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(gen))
            vo.wait_until("e")
            self.play(FadeIn(what))
            vo.wait_until("h")
            self.play(FadeIn(hb))
            vo.wait_until("c")
            self.play(Write(eig), Create(dial), FadeIn(hand), FadeIn(cl), FadeIn(wheel))
            self.play(tt.animate.set_value(2 * PI), run_time=2.5, rate_func=linear)
            vo.wait_until("s")
            tt.set_value(0)
            self.add(trail, arr)
            self.play(FadeIn(bs), FadeIn(axis), FadeIn(ax_l), FadeIn(arr), FadeIn(sl))
            self.play(tt.animate.set_value(2 * PI), run_time=max(3.5, vo.remaining()), rate_func=linear)
        for m in (hand, trail, arr):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
