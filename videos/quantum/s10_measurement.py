from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum.common import (Projector, WaveView, bar_chart, boxed, corner_wheel, depth_sorted, label, line_3d,
                                   load, mtex, note, num, segments_3d, stack, wave_axes, why, ylabel)
from videos.quantum.compute import box_E, box_phi
from videos.quantum.s06_box import walls


class Measurement(VoiceoverScene):
    def construct(self):
        self.postulates()
        self.geometry()
        self.energy_measurement()
        self.expectation()
        self.other_observables()

    # ------------------------------------------------------------------
    def postulates(self):
        title = label(r"The rules of quantum mechanics", font_size=44).to_edge(UP, buff=0.45)
        items = VGroup(
            label(r"1.\ \ A state is a unit vector $\ket{\psi}$ (an overall phase doesn't matter).", font_size=30),
            label(r"2.\ \ Each observable is a Hermitian operator: \ $\hat A = \sum_a a\,\ket{a}\bra{a}$.", font_size=30),
            label(r"3.\ \ Measuring $\hat A$ gives one of its eigenvalues $a$, with probability $|\braket{a}{\psi}|^2$.",
                  font_size=30),
            label(r"4.\ \ Right after the measurement, the state is $\ket{a}$.", font_size=30),
            label(r"5.\ \ Between measurements, $i\hbar\,\tfrac{d}{dt}\ket{\psi} = \hat H\ket{\psi}$.", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(title, DOWN, buff=0.55)
        items[2].set_color(C.BORN)
        with self.voiceover(
            "We can now state the rules of the whole theory on one screen. <bookmark mark='a'/> A state is a unit "
            "vector, up to an overall phase. <bookmark mark='b'/> Every measurable quantity is a Hermitian operator, "
            "described by its eigenvalues and eigenvectors. <bookmark mark='c'/> A measurement gives one of the "
            "eigenvalues, at random, with probability equal to the squared length of the state's shadow on that "
            "eigenvector: the Born rule. <bookmark mark='d'/> Right after the measurement, the state is that "
            "eigenvector. <bookmark mark='e'/> And between measurements, the state evolves by the Schrödinger equation."
        ) as vo:
            self.play(FadeIn(title))
            for m, it in zip("abcde", items):
                vo.wait_until(m)
                self.play(FadeIn(it, shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def geometry(self):
        proj = Projector(az=-0.75, el=0.38, scale=2.9, center=LEFT * 2.8 + DOWN * 0.6)
        v = np.array([0.48, 0.6, 0.64])
        assert abs(np.linalg.norm(v) - 1) < 1e-12
        state = ValueTracker(0.0)  # 0: superposition, 1: collapsed onto axis 2

        def scene3d():
            vv = (1 - state.get_value()) * v + state.get_value() * np.array([0, 1.0, 0])
            vv = vv / np.linalg.norm(vv)
            parts = []
            for i, col in enumerate((C.ENERGY, C.ENERGY, C.ENERGY)):
                e = np.zeros(3)
                e[i] = 1.15
                parts.append(line_3d(proj, -0.0 * e, e, color=GREY_B, n=10, stroke_width=2.5, depth_range=1.2))
            for i in range(3):
                e = np.zeros(3)
                e[i] = vv[i]
                parts.append(line_3d(proj, vv, e, color=GREY_C, n=8, stroke_width=1.5, depth_range=1.2))
            parts.append(line_3d(proj, [0, 0, 0], vv, color=WHITE, n=12, stroke_width=5, depth_range=1.2))
            g = depth_sorted(*parts)
            tip = Dot(proj.point(vv), radius=0.07, color=WHITE)
            shadows = VGroup()
            for i in range(3):
                e = np.zeros(3)
                e[i] = vv[i]
                shadows.add(Dot(proj.point(e), radius=0.06, color=C.BORN))
            labs = VGroup(*[MathTex(rf"\ket{{a_{i + 1}}}", font_size=30, color=C.ENERGY).move_to(
                proj.point(np.eye(3)[i] * 1.38)) for i in range(3)])
            psi_l = MathTex(r"\ket{\psi}", font_size=32).move_to(proj.point(vv * 1.18))
            return VGroup(g, tip, shadows, labs, psi_l)

        pic = always_redraw(scene3d)
        # squared shadows as stacked bars
        bx = Axes(x_range=[0, 4, 1], y_range=[0, 1.0, 0.5], x_length=3.4, y_length=3.0, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(RIGHT * 3.8 + DOWN * 0.3)

        def bars():
            vv = (1 - state.get_value()) * v + state.get_value() * np.array([0, 1.0, 0])
            vv = vv / np.linalg.norm(vv)
            return bar_chart(bx, [1, 2, 3], vv**2, width=0.6, color=C.BORN)

        bb = always_redraw(bars)
        bl = VGroup(*[MathTex(rf"a_{i}", font_size=28, color=C.ENERGY).next_to(bx.c2p(i, 0), DOWN, buff=0.12) for i in (1, 2, 3)])
        vals = VGroup(*[MathTex(f"{p:.2f}", font_size=26, color=C.BORN).next_to(bx.c2p(i + 1, p), UP, buff=0.08)
                        for i, p in enumerate(v**2)])
        tot = MathTex(r"0.23 + 0.36 + 0.41 = 1", font_size=32, color=C.BORN).next_to(bx, UP, buff=0.45)
        assert np.allclose(np.round(v**2, 2), [0.23, 0.36, 0.41])
        tag = note(r"three real dimensions, so we can draw them").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Picture it with just three dimensions, and real numbers so we can draw it. <bookmark mark='a'/> The three "
            "perpendicular axes are the eigenvectors of some observable, with outcomes a one, a two, a three. The state "
            "is a unit vector pointing somewhere in between. <bookmark mark='s'/> Its shadows on the axes, squared, are "
            "the probabilities of the three outcomes, <bookmark mark='p'/> and by Pythagoras they add up to one. That's "
            "why the Born rule squares: it's the only way to turn the components of a unit vector into probabilities "
            "that always sum to one."
        ) as vo:
            self.add(pic)
            self.play(FadeIn(pic), FadeIn(tag))
            vo.wait_until("a")
            self.play(proj.az.animate.set_value(-0.45), run_time=2)
            vo.wait_until("s")
            self.play(Create(bx), FadeIn(bl), FadeIn(bb), FadeIn(vals))
            vo.wait_until("p")
            self.play(Write(tot))
        coll = label(r"outcome: $a_2$", font_size=32, color=C.ENERGY).next_to(bx, DOWN, buff=0.7)
        with self.voiceover(
            "Now measure. Suppose the outcome is a two. <bookmark mark='c'/> The state jumps onto that axis: measure "
            "again immediately and you're certain to get a two. That jump is the one part of the theory that isn't "
            "described by the Schrödinger equation, and what really happens in it is still debated. But the rule "
            "itself has been tested to great precision."
        ) as vo:
            self.play(FadeOut(vals), FadeOut(tot))
            vo.wait_until("c")
            self.play(state.animate.set_value(1.0), FadeIn(coll), run_time=1.0, rate_func=rush_into)
        pic.clear_updaters()
        bb.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def energy_measurement(self):
        m = load("measure")
        c = load("carpet")
        ns, P, shots = m["ns"], m["P"], m["shots"]
        x, psi0 = c["x"], c["movie"][0]
        ax = wave_axes((-0.02, 1.02), (0, 7.5), x_length=5.2, y_length=2.3).move_to(LEFT * 3.6 + UP * 1.8)
        wv = WaveView(ax, x, psi0, mode="density", x_window=(0, 1))
        wl = walls(ax)
        bax = Axes(x_range=[0, 18, 5], y_range=[0, 0.17, 0.05], x_length=6.0, y_length=3.8, tips=False,
                   axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(RIGHT * 3.2 + DOWN * 0.6)
        theo = VGroup(*[Rectangle(width=0.27, height=max(1e-3, bax.c2p(0, p)[1] - bax.c2p(0, 0)[1]), stroke_color=C.ENERGY,
                                  stroke_width=2, fill_opacity=0).move_to(bax.c2p(n, p / 2)) for n, p in zip(ns[:17], P[:17])])
        k = ValueTracker(0)

        def hist():
            n = int(k.get_value())
            cnt = np.bincount(shots[:n], minlength=18)[1:18] / max(n, 1)
            return bar_chart(bax, np.arange(1, 18), np.minimum(cnt, 0.17), width=0.27, color=C.BORN, opacity=0.85)

        hb = always_redraw(hist)
        cnt_l = always_redraw(lambda: MathTex(r"\text{measurements: }" + f"{int(k.get_value()):,}".replace(",", "{,}"),
                                              font_size=30).next_to(bax, UP, buff=0.25))
        nl = MathTex(r"n", font_size=28).next_to(bax.x_axis.get_end(), RIGHT, buff=0.1)
        leg = VGroup(VGroup(Square(0.22, color=C.ENERGY, stroke_width=2), MathTex(r"|c_n|^2", font_size=26, color=C.ENERGY)).arrange(RIGHT, buff=0.12),
                     VGroup(Square(0.22, color=C.BORN, fill_opacity=0.85, stroke_width=0), label(r"fraction of outcomes", font_size=24, color=C.BORN)).arrange(RIGHT, buff=0.12)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(bax, RIGHT, buff=0.1).shift(UP * 1.2)
        if leg.get_right()[0] > 7.0:
            leg.shift(LEFT * (leg.get_right()[0] - 7.0))
        sim = note(r"2{,}000 outcomes, sampled from $|c_n|^2$ (seeded)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Let's measure the energy of our narrow packet in the box. The possible outcomes are the energies E n, "
            "<bookmark mark='p'/> with probabilities given by the squared coefficients we computed before. "
            "<bookmark mark='m'/> Each measurement gives just one of them. Here are two thousand simulated measurements "
            "on two thousand identical copies of the state. The fractions settle onto the predicted probabilities."
        ) as vo:
            self.play(Create(ax), FadeIn(wl), FadeIn(wv))
            vo.wait_until("p")
            self.play(Create(bax), FadeIn(nl), FadeIn(theo), FadeIn(leg))
            vo.wait_until("m")
            self.add(hb, cnt_l)
            self.play(FadeIn(sim), k.animate.set_value(2000), run_time=vo.remaining() + 0.5, rate_func=lambda a: a**2)
        hb.clear_updaters()
        cnt_l.clear_updaters()
        # three single shots with collapse
        firsts = [int(shots[0]), int(shots[1])]
        assert firsts == [7, 4], firsts  # the narration names these outcomes
        out_l = label(r"one measurement", font_size=28).next_to(ax, DOWN, buff=0.3)
        with self.voiceover(
            "And each individual measurement changes the state. <bookmark mark='a'/> Here the first outcome was E seven: "
            "the packet is replaced by the seventh stationary state, and stays there. <bookmark mark='b'/> Prepare a "
            "fresh packet and measure again. This time: E four, and a different collapse."
        ) as vo:
            self.play(FadeIn(out_l))
            for mk, n in zip(("a", "b"), firsts):
                vo.wait_until(mk)
                tag = MathTex(rf"E_{{{n}}}", font_size=34, color=C.ENERGY).next_to(out_l, RIGHT, buff=0.25)
                self.play(FadeIn(tag), run_time=0.4)
                self.play(UpdateFromAlphaFunc(wv, lambda mm, a, n=n: mm.set_psi((1 - a) * psi0 + a * box_phi(n, x))),
                          run_time=0.5, rate_func=rush_into)
                self.wait(1.0)
                self.play(FadeOut(tag), UpdateFromAlphaFunc(wv, lambda mm, a, n=n: mm.set_psi(a * psi0 + (1 - a) * box_phi(n, x))),
                          run_time=0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def expectation(self):
        m = load("measure")
        Eavg, Eint, Es = float(m["E_avg"][0]), float(m["E_int"][0]), float(m["sample_mean"][0])
        assert abs(Eavg - 484.73) < 0.01 and abs(Eint - 484.73) < 0.01 and abs(Es - 487.1) < 0.05
        l1 = MathTex(r"\langle A\rangle", r"=", r"\sum_a a\,P(a)", font_size=38)
        l2 = MathTex(r"\phantom{\langle A\rangle}", r"=", r"\sum_a a\,\braket{\psi}{a}\braket{a}{\psi}", font_size=38)
        l3 = MathTex(r"\phantom{\langle A\rangle}", r"=", r"\bra{\psi}\Big(\sum_a a\,\ket{a}\bra{a}\Big)\ket{\psi}", font_size=38)
        l4 = MathTex(r"\phantom{\langle A\rangle}", r"=", r"\braket{\psi}{\hat A\psi}", font_size=42)
        col = stack(l1, l2, l3, l4, buff=0.3, align=1).to_edge(UP, buff=0.3).shift(LEFT * 2.2)
        w1 = why(l1, r"average outcome")
        w2 = why(l2, r"Born rule: $|z|^2 = z^* z$")
        w3 = why(l3, r"pull the sum inside")
        w4 = why(l4, r"spectral theorem")
        from videos.quantum.common import place_whys
        place_whys([l1, l2, l3, l4], [w1, w2, w3, w4])
        l4[2].set_color(C.ENERGY)
        nums = VGroup(
            MathTex(r"\sum_n E_n |c_n|^2 = " + num(Eavg, 2), font_size=32),
            MathTex(r"\braket{\psi}{\hat H\psi} = \frac{\hbar^2}{2m}\int|\psi'|^2dx = " + num(Eint, 2), font_size=32),
            MathTex(r"\text{mean of the 2{,}000 outcomes: } " + num(Es, 1), font_size=32, color=C.BORN),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).to_edge(DOWN, buff=0.35)
        un = note(r"$\hbar = m = L = 1$").next_to(nums, RIGHT, buff=0.4)
        assert nums.get_top()[1] < col.get_bottom()[1] - 0.25
        with self.voiceover(
            "With the probabilities in hand, the average outcome follows. <bookmark mark='a'/> It's the sum of each "
            "outcome times its probability. <bookmark mark='b'/> Write the probability as the shadow times its "
            "conjugate, <bookmark mark='c'/> pull the sum inside, <bookmark mark='d'/> and the operator itself appears: "
            "the average of A is psi, A psi. You never need the eigenvectors to compute an average."
        ) as vo:
            self.play(Write(l1[0]))
            vo.wait_until("a")
            self.play(Write(l1[1:]), FadeIn(w1))
            vo.wait_until("b")
            self.play(Write(l2[1:]), FadeIn(w2))
            vo.wait_until("c")
            self.play(Write(l3[1:]), FadeIn(w3))
            vo.wait_until("d")
            self.play(Write(l4[1:]), FadeIn(w4))
        with self.voiceover(
            "For our packet: summing energies times probabilities gives 484.73. <bookmark mark='i'/> Computing psi, H "
            "psi directly, as an integral of the slope squared, gives the same 484.73. <bookmark mark='s'/> And the "
            "average of our two thousand random outcomes is 487.1, within the noise you'd expect from two thousand "
            "samples."
        ) as vo:
            self.play(FadeIn(nums[0]), FadeIn(un))
            vo.wait_until("i")
            self.play(FadeIn(nums[1]))
            vo.wait_until("s")
            self.play(FadeIn(nums[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def other_observables(self):
        rows = VGroup(
            VGroup(label(r"observable", font_size=28, color=GREY_A), label(r"eigenstates", font_size=28, color=GREY_A),
                   label(r"amplitude for outcome", font_size=28, color=GREY_A)),
            VGroup(MathTex(r"\text{energy } \hat H", font_size=32, color=C.ENERGY), MathTex(r"\varphi_n(x)", font_size=32),
                   MathTex(r"c_n = \braket{\varphi_n}{\psi}", font_size=32)),
            VGroup(MathTex(r"\text{position } \hat x", font_size=32, color=C.XPOS), MathTex(r"\delta(x - x_0)", font_size=32),
                   MathTex(r"\braket{x_0}{\psi} = \psi(x_0)", font_size=32)),
            VGroup(MathTex(r"\text{momentum } \hat p", font_size=32, color=C.MOMENTUM),
                   MathTex(r"\frac{e^{ipx/\hbar}}{\sqrt{2\pi\hbar}}", font_size=32),
                   MathTex(r"\braket{p}{\psi} = \phi(p)", font_size=32)),
        )
        for r in rows:
            for j, cell in enumerate(r):
                cell.move_to(np.array([-4.4 + 4.3 * j, 0, 0]))
        rows.arrange(DOWN, buff=0.55).move_to(UP * 0.6)
        for r in rows:
            for j, cell in enumerate(r):
                cell.set_x(-4.4 + 4.3 * j)
        rule = Line(LEFT * 6.4, RIGHT * 6.4, color=GREY_D).next_to(rows[0], DOWN, buff=0.2)
        foot = label(r"one state, many bases: each observable is a different set of axes", font_size=28, color=GREY_A)
        foot.to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The same rules cover every observable; only the axes change. <bookmark mark='e'/> For energy, the axes "
            "are the stationary states. <bookmark mark='x'/> For position, they're infinitely narrow spikes, and the "
            "shadow on the spike at x zero is just psi of x zero. So Born's rule for position, from the start of the "
            "video, is a special case. <bookmark mark='p'/> For momentum, the axes are plane waves, and the shadow is "
            "a new function, phi of p. What is it, and how are these two sets of axes related? That's next."
        ) as vo:
            self.play(FadeIn(rows[0]), Create(rule))
            for mk, r in zip("exp", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()
